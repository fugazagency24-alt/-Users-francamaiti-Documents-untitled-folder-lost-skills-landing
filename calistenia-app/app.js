// Modo Toro — app offline. Datos en localStorage, rutina en data.js.

const KEY = "toro.v1";
const DIAS = ["Dom", "Lun", "Mar", "Mié", "Jue", "Vie", "Sáb"];
const FRASES_PASOS = [
  "10k adentro. Así se construye el toro.",
  "Otro día de 10k. La constancia no se negocia.",
  "Pasos hechos. El déficit trabaja mientras caminás.",
  "10k. Un kilo menos se arma así, día a día.",
  "Caminaste. Ahora el cuerpo responde.",
];

const $ = (sel, el = document) => el.querySelector(sel);
const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

function ymd(d = new Date()) {
  const p = (n) => String(n).padStart(2, "0");
  return `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())}`;
}
function parseYmd(s) {
  const [y, m, d] = s.split("-").map(Number);
  return new Date(y, m - 1, d);
}

// ---------- estado ----------
function load() {
  let s = {};
  try { s = JSON.parse(localStorage.getItem(KEY)) || {}; } catch {}
  return {
    name: "", start: ymd(), ctx: "plaza", weak: "izquierdo",
    log: {}, steps: {}, rehab: {}, free: {}, weights: [],
    ...s,
  };
}
let S = load();
function save() {
  try { localStorage.setItem(KEY, JSON.stringify(S)); } catch {}
}
save();

// Semana y fase según fecha de inicio.
function progreso(date = new Date()) {
  const days = Math.max(0, Math.floor((parseYmd(ymd(date)) - parseYmd(S.start)) / 864e5));
  const semana = Math.floor(days / 7) + 1;
  const fase = Math.min(3, Math.floor((semana - 1) / 4));
  return { semana, fase, descarga: semana % 4 === 0 && semana <= 16 };
}
const rx = (p) => (Array.isArray(p) ? p[progreso().fase] : p);

// ---------- media ----------
let MEDIA = {};
fetch("media/index.json")
  .then((r) => (r.ok ? r.json() : {}))
  .then((m) => { MEDIA = m || {}; render(); })
  .catch(() => {});

function media(id, fallback = "") {
  const f = MEDIA[id];
  if (!f) return fallback;
  const src = "media/" + encodeURIComponent(f);
  return /\.(mp4|webm|mov|m4v)$/i.test(f)
    ? `<video src="${src}" autoplay muted loop playsinline preload="metadata"></video>`
    : `<img src="${src}" alt="" loading="lazy">`;
}
const initials = (id) => (EJ[id]?.n || id).split(" ").map((w) => w[0]).slice(0, 2).join("").toUpperCase();

// ---------- UI helpers ----------
function toast(msg) {
  const t = $("#toast");
  t.textContent = msg;
  t.hidden = false;
  clearTimeout(toast.t);
  toast.t = setTimeout(() => (t.hidden = true), 2800);
}

function exRow(it) {
  const e = EJ[it.e] || { n: it.e };
  return `<button class="ex" data-ex="${it.e}" data-rx="${esc(rx(it.p))}">
    <div class="thumb">${media(it.e, initials(it.e))}</div>
    <div class="nm">${esc(e.n)}${it.nota ? `<small>${esc(it.nota)}</small>` : ""}</div>
    <div class="rx">${esc(rx(it.p))}</div>
  </button>`;
}

function blockCard(b) {
  return `<div class="card block">
    <div class="head"><b>${esc(b.t)}</b><span>${esc(rx(b.f || ""))}</span></div>
    ${b.items.map(exRow).join("")}
  </div>`;
}

function hombroItems() {
  return HOMBRO.items.filter((it) => !it.plaza || S.ctx === "plaza");
}

function ctxSeg() {
  return `<div class="seg" data-ctx>
    <button data-v="plaza" class="${S.ctx === "plaza" ? "on" : ""}">Con plaza</button>
    <button data-v="casa" class="${S.ctx === "casa" ? "on" : ""}">Sin plaza</button>
  </div>`;
}

function faseChip() {
  const p = progreso();
  const f = FASES[p.fase];
  return `<div class="row" style="flex-wrap:wrap">
    <span class="tag">Semana ${p.semana}</span>
    <span class="tag">Fase ${f.n} · ${f.nombre}</span>
    ${p.descarga ? `<span class="tag acc">Descarga · 2/3 de las series</span>` : ""}
  </div>`;
}

// ---------- vistas ----------
let tab = "hoy";
let sel = null; // sesión elegida hoy
let libre = { min: 15, foco: "empuje", seed: 0 };

const today = () => ymd();
const doneToday = (id) => (S.log[today()] || []).some((x) => x.s === id);

function saludo() {
  const h = new Date().getHours();
  const base = h < 13 ? "Buen día" : h < 20 ? "Buenas tardes" : "Buenas noches";
  return `${base}, ${S.name || "toro"}.`;
}

function vHoy() {
  const id = sel || SEMANA[new Date().getDay()];
  const s = SESIONES[id];
  const blocks = s[S.ctx];
  const warm = CALENTAMIENTO[S.ctx];
  const done = doneToday(id);
  const pasos = !!S.steps[today()];
  const sugerida = SEMANA[new Date().getDay()];

  return `
  <section class="hero">
    ${media("yo", `<div class="ph">TORO</div>`)}
    <div class="hi"><h1>${esc(saludo())}</h1><p>${esc(FASES[progreso().fase].meta)}</p></div>
  </section>
  <div class="stack">
    ${faseChip()}
    ${ctxSeg()}
    <div class="chips" data-ses>
      ${Object.keys(SESIONES).map((k) => `<button class="chip ${k === id ? "on" : ""} ${doneToday(k) ? "done" : ""}" data-v="${k}">${k === sugerida ? "Hoy · " : ""}${esc(SESIONES[k].nombre.replace("Extra · ", "+ "))}</button>`).join("")}
    </div>

    <div class="row between" style="margin-top:22px">
      <div><h2>${esc(s.nombre)}</h2><div class="muted small">${esc(s.foco)}</div></div>
      <span class="tag">${s.min}'</span>
    </div>
    ${s.nota ? `<div class="note">${esc(s.nota)}</div>` : ""}

    ${blockCard({ t: "Calentamiento", f: "1 ronda · sin pausa", items: warm })}
    ${blocks.map(blockCard).join("")}
    ${s.hombro ? blockCard({ t: "Rutina de hombro", f: "D = débil · F = fuerte", items: hombroItems() }) : ""}

    <button class="btn ${done ? "done" : ""}" data-act="done">${done ? "✓ Completada" : "Completé esta sesión"}</button>
    <div class="grid2">
      <button class="btn ghost sm" data-act="guiado">▶ Modo guiado</button>
      <button class="btn ghost sm ${pasos ? "done" : ""}" data-act="pasos">${pasos ? "✓ 10k hoy" : "👟 Hice 10k"}</button>
    </div>
  </div>`;
}

function weekDates() {
  const d = new Date();
  const monday = new Date(d.getFullYear(), d.getMonth(), d.getDate() - ((d.getDay() + 6) % 7));
  return [...Array(7)].map((_, i) => new Date(monday.getFullYear(), monday.getMonth(), monday.getDate() + i));
}
const sesionesDia = (k) => (S.log[k] || []).length + (S.free[k] || []).length;

function racha() {
  let n = 0;
  const d = new Date();
  if (!sesionesDia(ymd(d))) d.setDate(d.getDate() - 1);
  while (sesionesDia(ymd(d))) { n++; d.setDate(d.getDate() - 1); }
  return n;
}

function vSemana() {
  const dates = weekDates();
  const hechas = dates.reduce((a, d) => a + (S.log[ymd(d)] || []).length, 0);
  const libres = dates.reduce((a, d) => a + (S.free[ymd(d)] || []).length, 0);
  const pasos = dates.filter((d) => S.steps[ymd(d)]).length;
  const total = Object.values(S.log).reduce((a, x) => a + x.length, 0);

  return `<div class="stack">
    <h1>Semana</h1>
    ${faseChip()}
    <div class="card">
      <div class="row between">
        <div><div class="big">${hechas}<span class="muted" style="font-size:22px">/6</span></div><div class="muted small">sesiones esta semana</div></div>
        <div style="text-align:right"><div class="big">${racha()}</div><div class="muted small">días de racha</div></div>
      </div>
      <div class="gap"></div>
      <div class="bar"><i style="width:${Math.min(100, (hechas / 6) * 100)}%"></i></div>
    </div>
    <div class="days">
      ${dates.map((d) => {
        const k = ymd(d);
        const dots = (S.log[k] || []).map(() => "<i></i>").join("") + (S.free[k] || []).map(() => "<i></i>").join("") + (S.steps[k] ? '<i class="s"></i>' : "") + (S.rehab[k] ? '<i class="h"></i>' : "");
        return `<div class="day ${k === today() ? "today" : ""}">${DIAS[d.getDay()]}<b>${d.getDate()}</b><div class="dots">${dots}</div></div>`;
      }).join("")}
    </div>
    <div class="legend"><span><i style="background:var(--ok)"></i>Sesión</span><span><i style="background:#4aa3ff"></i>10k</span><span><i style="background:var(--accent)"></i>Hombro</span></div>
    <div class="card">
      <div class="row between"><span>Libres</span><b>${libres}</b></div>
      <div class="row between" style="margin-top:8px"><span>Días con 10k</span><b>${pasos}/7</b></div>
      <div class="row between" style="margin-top:8px"><span>Sesiones totales</span><b>${total}</b></div>
    </div>
    <h3 style="margin-top:22px">Plan</h3>
    <div class="card">
      ${[1, 2, 3, 4, 5, 6, 0].map((d) => {
        const s = SESIONES[SEMANA[d]];
        return `<div class="row between" style="padding:6px 0"><span class="muted">${DIAS[d]}</span><span>${esc(s.nombre)}${s.extra ? ' <span class="tag">opcional</span>' : ""}</span></div>`;
      }).join("")}
    </div>
    <h3 style="margin-top:22px">Reglas</h3>
    <div class="card"><ul class="rules">${REGLAS.map((r) => `<li>${esc(r)}</li>`).join("")}</ul></div>
  </div>`;
}

function vHombro() {
  const done = !!S.rehab[today()];
  return `<div class="stack">
    <h1>Hombro</h1>
    <div class="muted">Rehab clavícula · ${HOMBRO.min}' · 3–5 veces por semana.</div>
    <div class="note">D = lado débil (${esc(S.weak)}) · F = lado fuerte.</div>
    ${ctxSeg()}
    ${blockCard({ t: "Circuito", f: "Lento · sin dolor", items: hombroItems() })}
    <h3 style="margin-top:22px">Reglas</h3>
    <div class="card"><ul class="rules">${HOMBRO.reglas.map((r) => `<li>${esc(r)}</li>`).join("")}</ul></div>
    <button class="btn ${done ? "done" : ""}" data-act="rehab">${done ? "✓ Hombro hecho hoy" : "Completé el hombro"}</button>
  </div>`;
}

function shuffle(arr, seed) {
  const a = arr.slice();
  let x = seed * 9301 + 49297;
  for (let i = a.length - 1; i > 0; i--) {
    x = (x * 9301 + 49297) % 233280;
    const j = Math.floor((x / 233280) * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

function libreSesion() {
  const foco = FREEFLOW.focos[libre.foco];
  if (foco.circuito) {
    const items = hombroItems();
    if (libre.min === 10) return { t: "Hombro exprés", f: "1 ronda", items: items.slice(0, 6) };
    if (libre.min === 15) return { t: "Hombro completo", f: "1 ronda lenta", items };
    const extra = items.filter((it) => ["rot_ext", "remo_mochila", "press_uni"].includes(it.e)).map((it) => ({ e: it.e, p: "2ª ronda · solo débil" }));
    return { t: "Hombro + débil", f: "Circuito + ronda extra lado débil", items: [...items, ...extra] };
  }
  const fmt = FREEFLOW.formatos[libre.min];
  const pool = libre.seed ? shuffle(foco[S.ctx], libre.seed) : foco[S.ctx];
  return { t: fmt.t, f: fmt.f, items: pool.slice(0, fmt.n).map(([e, p]) => ({ e, p })) };
}

function vLibre() {
  const n = (S.free[today()] || []).length;
  return `<div class="stack">
    <h1>Libre</h1>
    <div class="muted">¿Querés más? Elegí tiempo y foco.</div>
    <div class="seg three" data-min>
      ${[10, 15, 20].map((m) => `<button data-v="${m}" class="${libre.min === m ? "on" : ""}">${m}'</button>`).join("")}
    </div>
    <div class="chips" data-foco>
      ${Object.entries(FREEFLOW.focos).map(([k, f]) => `<button class="chip ${k === libre.foco ? "on" : ""}" data-v="${k}">${f.nombre}</button>`).join("")}
    </div>
    ${ctxSeg()}
    ${blockCard(libreSesion())}
    <div class="grid2">
      <button class="btn ghost sm" data-act="shuffle">↻ Otra</button>
      <button class="btn ghost sm" data-act="guiado-libre">▶ Guiado</button>
    </div>
    <button class="btn" data-act="libre">Hecho${n ? ` · hoy van ${n}` : ""}</button>
  </div>`;
}

function vYo() {
  const ws = S.weights.slice().sort((a, b) => a.d.localeCompare(b.d));
  const ini = ws[0]?.kg ?? 83;
  const act = ws.at(-1)?.kg ?? ini;
  const pct = Math.max(0, Math.min(100, ((ini - act) / (ini - 70)) * 100));
  return `<div class="stack">
    <h1>Yo</h1>
    <div class="card">
      <div class="row between">
        <div><div class="big">${act}<span class="muted" style="font-size:20px"> kg</span></div><div class="muted small">actual</div></div>
        <div style="text-align:right"><div class="big">70</div><div class="muted small">meta · 75 al 31/12</div></div>
      </div>
      <div class="gap"></div>
      <div class="bar"><i style="width:${pct}%"></i></div>
      <div class="muted small" style="margin-top:8px">${(ini - act).toFixed(1)} kg bajados · faltan ${(act - 70).toFixed(1)}</div>
    </div>
    <div class="row">
      <div class="field" style="flex:1"><input id="kg" type="number" inputmode="decimal" step="0.1" placeholder="Peso de hoy (kg)"></div>
      <button class="btn sm" style="width:auto;padding:14px 20px" data-act="peso">Anotar</button>
    </div>
    ${ws.length ? `<ul class="list">${ws.slice(-6).reverse().map((w) => `<li><span class="muted">${w.d}</span><b>${w.kg} kg</b></li>`).join("")}</ul>` : ""}

    <h3 style="margin-top:22px">Ajustes</h3>
    <div class="field"><label>Nombre</label><input id="name" value="${esc(S.name)}" placeholder="toro"></div>
    <div class="field"><label>Inicio del plan (define semana y fase)</label><input id="start" type="date" value="${S.start}"></div>
    <div class="field"><label>Hombro débil</label>
      <div class="seg" data-weak>
        <button data-v="izquierdo" class="${S.weak === "izquierdo" ? "on" : ""}">Izquierdo</button>
        <button data-v="derecho" class="${S.weak === "derecho" ? "on" : ""}">Derecho</button>
      </div>
    </div>
    <button class="btn ghost sm" data-act="offline">⬇ Guardar fotos y videos offline</button>
    <button class="btn ghost sm" data-act="backup">Copiar backup de datos</button>
    <button class="btn ghost sm" data-act="reset" style="color:var(--accent)">Borrar todo</button>
    <div class="muted small" style="text-align:center;margin-top:10px">Modo Toro · funciona sin internet</div>
  </div>`;
}

// ---------- detalle y guiado ----------
function openSheet(html) {
  const sh = $("#sheet");
  sh.innerHTML = `<div class="inner">${html}</div>`;
  sh.hidden = false;
  sh.scrollTop = 0;
}
function closeSheet() {
  clearInterval(timer.i);
  $("#sheet").hidden = true;
  $("#sheet").innerHTML = "";
}

function openEx(id, r) {
  const e = EJ[id] || { n: id, c: "" };
  openSheet(`
    <button class="close" data-act="close">×</button>
    <div class="stack">
      <div class="media">${media(id, initials(id))}</div>
      <h2>${esc(e.n)}</h2>
      <div class="big" style="font-size:34px">${esc(r)}</div>
      <div class="note">${esc(e.c)}</div>
    </div>`);
}

let guia = null;
const timer = { i: null };

function startGuia(blocks, onFinish) {
  const steps = blocks.flatMap((b) => b.items.map((it) => ({ ...it, b })));
  guia = { steps, i: 0, onFinish };
  drawGuia();
}

function drawGuia(rest = 0) {
  clearInterval(timer.i);
  const { steps, i } = guia;
  if (i >= steps.length) {
    openSheet(`<div class="stack" style="text-align:center;padding-top:30vh">
      <div class="big">Hecho.</div><div class="muted">Sesión terminada.</div>
      <button class="btn" data-act="guia-fin">Marcar completada</button>
      <button class="btn ghost sm" data-act="close">Cerrar</button></div>`);
    return;
  }
  const st = steps[i];
  const e = EJ[st.e] || { n: st.e, c: "" };
  openSheet(`
    <div class="row between"><button class="close" data-act="close">×</button><span class="muted small">${i + 1}/${steps.length} · ${esc(st.b.t)}</span></div>
    <div class="stack">
      <div class="muted small">${esc(rx(st.b.f || ""))}</div>
      <div class="media" style="aspect-ratio:1">${media(st.e, initials(st.e))}</div>
      <h2>${esc(e.n)}</h2>
      <div class="big" style="font-size:34px">${esc(rx(st.p))}</div>
      <div class="note">${esc(e.c)}</div>
      ${rest ? `<div class="timer" id="tm">${rest}</div>` : ""}
      <div class="seg three" data-rest>
        ${[60, 90, 120].map((s) => `<button data-v="${s}">${s}s</button>`).join("")}
      </div>
      <div class="grid2">
        <button class="btn ghost sm" data-act="guia-prev">← Atrás</button>
        <button class="btn sm" data-act="guia-next">Siguiente →</button>
      </div>
    </div>`);
  if (rest) {
    let left = rest;
    timer.i = setInterval(() => {
      left--;
      const tm = $("#tm");
      if (tm) tm.textContent = left;
      if (left <= 0) {
        clearInterval(timer.i);
        if (tm) tm.textContent = "¡Dale!";
        navigator.vibrate?.([200, 100, 200]);
      }
    }, 1000);
  }
}

// ---------- acciones ----------
function toggleDone(id) {
  const k = today();
  const list = S.log[k] || [];
  const ix = list.findIndex((x) => x.s === id);
  if (ix >= 0) list.splice(ix, 1);
  else list.push({ s: id, ctx: S.ctx });
  if (list.length) S.log[k] = list; else delete S.log[k];
  save();
  if (ix < 0) {
    const n = weekDates().reduce((a, d) => a + (S.log[ymd(d)] || []).length, 0);
    toast(`${SESIONES[id].nombre}: hecha. Semana ${n}/6.`);
  }
}

function currentBlocks() {
  const id = sel || SEMANA[new Date().getDay()];
  const s = SESIONES[id];
  return [
    { t: "Calentamiento", f: "1 ronda", items: CALENTAMIENTO[S.ctx] },
    ...s[S.ctx],
    ...(s.hombro ? [{ t: "Hombro", f: "D = débil · F = fuerte", items: hombroItems() }] : []),
  ];
}

document.addEventListener("click", async (ev) => {
  const t = ev.target.closest("button");
  if (!t) return;

  if (t.dataset.tab) {
    tab = t.dataset.tab;
    document.querySelectorAll(".tabs button").forEach((b) => b.classList.toggle("on", b === t));
    render();
    window.scrollTo(0, 0);
    return;
  }
  if (t.dataset.ex) return openEx(t.dataset.ex, t.dataset.rx);

  const group = t.parentElement?.dataset || {};
  if ("ctx" in group) { S.ctx = t.dataset.v; save(); return render(); }
  if ("ses" in group) { sel = t.dataset.v; return render(); }
  if ("min" in group) { libre.min = +t.dataset.v; return render(); }
  if ("foco" in group) { libre.foco = t.dataset.v; libre.seed = 0; return render(); }
  if ("weak" in group) { S.weak = t.dataset.v; save(); return render(); }
  if ("rest" in group) return drawGuia(+t.dataset.v);

  const k = today();
  switch (t.dataset.act) {
    case "done": toggleDone(sel || SEMANA[new Date().getDay()]); break;
    case "pasos":
      if (S.steps[k]) delete S.steps[k];
      else { S.steps[k] = true; toast(FRASES_PASOS[Math.floor(Math.random() * FRASES_PASOS.length)]); }
      save(); break;
    case "rehab":
      if (S.rehab[k]) delete S.rehab[k]; else { S.rehab[k] = true; toast("Hombro hecho. Ese brazo vuelve."); }
      save(); break;
    case "libre":
      (S.free[k] ||= []).push({ f: libre.foco, min: libre.min });
      save(); toast(`+${libre.min}' de ${FREEFLOW.focos[libre.foco].nombre.toLowerCase()}. Bestia.`); break;
    case "shuffle": libre.seed = (libre.seed % 997) + 1 + Math.floor(Math.random() * 50); break;
    case "guiado":
      return startGuia(currentBlocks(), () => { if (!doneToday(sel || SEMANA[new Date().getDay()])) toggleDone(sel || SEMANA[new Date().getDay()]); });
    case "guiado-libre":
      return startGuia([libreSesion()], () => { (S.free[k] ||= []).push({ f: libre.foco, min: libre.min }); save(); });
    case "guia-next": guia.i++; return drawGuia();
    case "guia-prev": guia.i = Math.max(0, guia.i - 1); return drawGuia();
    case "guia-fin": guia.onFinish?.(); closeSheet(); break;
    case "close": closeSheet(); return;
    case "peso": {
      const kg = parseFloat(($("#kg").value || "").replace(",", "."));
      if (!(kg > 30 && kg < 250)) return toast("Poné un peso válido.");
      S.weights = S.weights.filter((w) => w.d !== k).concat({ d: k, kg });
      save(); toast(`${kg} kg anotado.`); break;
    }
    case "offline": {
      const files = Object.values(MEDIA);
      if (!files.length) return toast("Todavía no hay fotos ni videos en media/.");
      toast("Descargando…");
      const c = await caches.open("toro-media");
      let ok = 0;
      for (const f of files) {
        try { await c.add("media/" + encodeURIComponent(f)); ok++; } catch {}
      }
      return toast(`${ok}/${files.length} archivos listos offline.`);
    }
    case "backup":
      try { await navigator.clipboard.writeText(JSON.stringify(S)); toast("Backup copiado."); }
      catch { toast("No se pudo copiar."); }
      return;
    case "reset":
      if (confirm("¿Borrar todo el historial?")) { localStorage.removeItem(KEY); S = load(); save(); }
      break;
    default: return;
  }
  render();
});

document.addEventListener("change", (ev) => {
  if (ev.target.id === "name") { S.name = ev.target.value.trim(); save(); }
  if (ev.target.id === "start" && ev.target.value) { S.start = ev.target.value; save(); render(); }
});

function render() {
  const v = { hoy: vHoy, semana: vSemana, hombro: vHombro, libre: vLibre, yo: vYo }[tab];
  $("#view").innerHTML = v();
}
render();

// Al volver a la app otro día, refrescar "hoy".
document.addEventListener("visibilitychange", () => { if (!document.hidden && $("#sheet").hidden) render(); });

if ("serviceWorker" in navigator) {
  window.addEventListener("load", () => navigator.serviceWorker.register("sw.js").catch(() => {}));
}
