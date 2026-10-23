import json
import sqlite3
import time
import uuid
from contextlib import contextmanager
from pathlib import Path
from .planner import canonical
from .validation import Problem


class Store:
    def __init__(self, path):
        self.path = path
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with self.db() as db:
            db.executescript("""
            PRAGMA journal_mode=WAL;
            CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS drafts (id TEXT PRIMARY KEY, plan TEXT NOT NULL, created REAL NOT NULL);
            CREATE TABLE IF NOT EXISTS jobs (
              id TEXT PRIMARY KEY, draft_id TEXT UNIQUE NOT NULL, idem TEXT UNIQUE NOT NULL,
              mode TEXT NOT NULL, state TEXT NOT NULL, error TEXT, created REAL NOT NULL, updated REAL NOT NULL,
              pause_requested INTEGER NOT NULL DEFAULT 0, activate_requested INTEGER NOT NULL DEFAULT 0);
            CREATE TABLE IF NOT EXISTS steps (
              job_id TEXT NOT NULL, key TEXT NOT NULL, state TEXT NOT NULL, result TEXT, error TEXT,
              PRIMARY KEY(job_id,key));
            CREATE TABLE IF NOT EXISTS events (
              seq INTEGER PRIMARY KEY AUTOINCREMENT, job_id TEXT NOT NULL, at REAL NOT NULL, kind TEXT NOT NULL, detail TEXT NOT NULL);
            """)

    @contextmanager
    def db(self):
        db = sqlite3.connect(self.path, timeout=10)
        db.row_factory = sqlite3.Row
        try:
            with db:
                yield db
        finally:
            db.close()

    def profile(self):
        with self.db() as db:
            r = db.execute("SELECT value FROM settings WHERE key='profile'").fetchone()
        if not r:
            raise Problem("Configurá el perfil primero: PUT /v1/profile", 409, "PROFILE_MISSING")
        return json.loads(r[0])

    def save_profile(self, p):
        with self.db() as db:
            db.execute("INSERT INTO settings VALUES ('profile',?) ON CONFLICT(key) DO UPDATE SET value=excluded.value", (canonical(p),))
        return p

    def draft(self, plan):
        ident = uuid.uuid4().hex
        with self.db() as db:
            db.execute("INSERT INTO drafts VALUES (?,?,?)", (ident, canonical(plan), time.time()))
        return {"draft_id": ident, **plan}

    def get_draft(self, ident):
        with self.db() as db:
            r = db.execute("SELECT plan FROM drafts WHERE id=?", (ident,)).fetchone()
        if not r:
            raise Problem("Borrador no encontrado", 404)
        return json.loads(r[0])

    def enqueue(self, draft_id, key, mode):
        now = time.time()
        with self.db() as db:
            db.execute("BEGIN IMMEDIATE")
            r = db.execute("SELECT * FROM jobs WHERE idem=? OR draft_id=?", (key, draft_id)).fetchall()
            if r:
                if any(x["draft_id"] != draft_id or x["mode"] != mode for x in r):
                    raise Problem("Idempotency-Key o borrador ya usado con otro contenido/modo", 409)
                return self.job(r[0]["id"])
            ident = uuid.uuid4().hex
            db.execute("INSERT INTO jobs(id,draft_id,idem,mode,state,error,created,updated) VALUES (?,?,?,?,?,?,?,?)", (ident, draft_id, key, mode, "QUEUED", None, now, now))
        return self.job(ident)

    def claim(self):
        with self.db() as db:
            db.execute("BEGIN IMMEDIATE")
            r = db.execute("SELECT id FROM jobs WHERE state='QUEUED' ORDER BY created LIMIT 1").fetchone()
            if not r:
                return None
            db.execute("UPDATE jobs SET state='RUNNING', updated=? WHERE id=?", (time.time(), r[0]))
            return r[0]

    def job(self, ident):
        with self.db() as db:
            r = db.execute("SELECT * FROM jobs WHERE id=?", (ident,)).fetchone()
            steps = db.execute("SELECT key,state,result,error FROM steps WHERE job_id=? ORDER BY rowid", (ident,)).fetchall()
            events = db.execute("SELECT seq,at,kind,detail FROM events WHERE job_id=? ORDER BY seq DESC LIMIT 100", (ident,)).fetchall()
        if not r:
            raise Problem("Trabajo no encontrado", 404)
        out = dict(r)
        out.pop("idem")
        out["steps"] = [{**dict(s), "result": json.loads(s["result"]) if s["result"] else None} for s in steps]
        out["events"] = [{**dict(e), "detail": json.loads(e["detail"])} for e in reversed(events)]
        return out

    def state(self, ident, state, error=None):
        with self.db() as db:
            db.execute("UPDATE jobs SET state=?,error=?,updated=? WHERE id=?", (state, error, time.time(), ident))

    def step(self, ident, key, state, result=None, error=None):
        with self.db() as db:
            db.execute("INSERT INTO steps VALUES (?,?,?,?,?) ON CONFLICT(job_id,key) DO UPDATE SET state=excluded.state,result=excluded.result,error=excluded.error",
                       (ident, key, state, canonical(result) if result is not None else None, error))

    def event(self, ident, kind, detail):
        with self.db() as db:
            db.execute("INSERT INTO events(job_id,at,kind,detail) VALUES (?,?,?,?)", (ident, time.time(), kind, canonical(detail)))

    def recover(self):
        # The process lock must be held before this. Never steal a living worker's job.
        with self.db() as db:
            db.execute("UPDATE steps SET state='UNCERTAIN',error='Proceso interrumpido; comprobar en Meta' WHERE state='IN_FLIGHT'")
            db.execute("UPDATE jobs SET state='NEEDS_RECONCILIATION', pause_requested=1, error='Proceso interrumpido; revisar pasos y estado remoto' WHERE state='RUNNING'")

    def retry(self, ident):
        with self.db() as db:
            db.execute("BEGIN IMMEDIATE")
            row = db.execute("SELECT state FROM jobs WHERE id=?", (ident,)).fetchone()
            if not row:
                raise Problem("Trabajo no encontrado", 404)
            if row[0] not in ("FAILED", "NEEDS_RECONCILIATION"):
                raise Problem("Solo se puede reintentar FAILED o NEEDS_RECONCILIATION", 409)
            if db.execute("SELECT 1 FROM steps WHERE job_id=? AND state IN ('UNCERTAIN','IN_FLIGHT')", (ident,)).fetchone():
                raise Problem("Resolver los pasos inciertos antes de reintentar", 409, "RECONCILIATION_REQUIRED")
            db.execute("UPDATE jobs SET state='QUEUED',error=NULL,pause_requested=0,updated=? WHERE id=?", (time.time(), ident))
        return self.job(ident)

    def request_pause(self, ident):
        self.job(ident)
        with self.db() as db:
            db.execute("UPDATE jobs SET pause_requested=1 WHERE id=?", (ident,))

    def clear_pause(self, ident):
        with self.db() as db:
            db.execute("UPDATE jobs SET pause_requested=0 WHERE id=?", (ident,))

    def pending_pause(self):
        with self.db() as db:
            r = db.execute("SELECT id FROM jobs WHERE pause_requested=1 AND state!='RUNNING' ORDER BY updated LIMIT 1").fetchone()
        return r[0] if r else None

    def enqueue_activation(self, ident):
        with self.db() as db:
            db.execute("BEGIN IMMEDIATE")
            r = db.execute("SELECT state,activate_requested FROM jobs WHERE id=?", (ident,)).fetchone()
            if r[0] in ("QUEUED", "RUNNING", "ACTIVATION_REQUESTED") and r[1]:
                return
            if r[0] not in ("CREATED_PAUSED", "SIMULATED", "STOPPED_PAUSED", "ACTIVATION_REQUESTED"):
                raise Problem("Estado no permite activar; completar/reconciliar el trabajo primero", 409)
            db.execute("UPDATE jobs SET state='QUEUED',activate_requested=1,pause_requested=0,error=NULL,updated=? WHERE id=?", (time.time(), ident))
