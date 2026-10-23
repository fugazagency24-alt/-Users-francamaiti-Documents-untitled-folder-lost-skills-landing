"use strict";
// Pantalla local Ejecución → Meta Ads. Todo dato del servidor o del usuario se inserta como texto (nunca como HTML).

const $ = (sel, root = document) => root.querySelector(sel);

function h(tag, attrs, ...kids) {
  const el = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs || {})) {
    if (v === undefined || v === null || v === false) continue;
    if (k === "class") el.className = v;
    else if (k === "text") el.textContent = v;
    else if (k === "on") for (const [ev, fn] of Object.entries(v)) el.addEventListener(ev, fn);
    else if (["value", "checked", "disabled", "selected", "hidden", "multiple"].includes(k)) el[k] = v;
    else el.setAttribute(k, v === true ? "" : v);
  }
  for (const kid of kids.flat(Infinity)) {
    if (kid === null || kid === undefined || kid === false) continue;
    el.append(kid instanceof Node ? kid : document.createTextNode(String(kid)));
  }
  return el;
}

// replaceChildren convierte null en el texto "null": siempre reemplazar contenido por acá.
function put(el, ...kids) {
  el.replaceChildren(...kids.flat(Infinity).filter((k) => k !== null && k !== undefined && k !== false));
}

const uuid = () => (crypto.randomUUID ? crypto.randomUUID() : String(Date.now()) + Math.random()).replace(/-/g, "");

async function api(method, path, body, headers = {}) {
  const init = { method, headers: { ...headers }, credentials: "same-origin" };
  if (body !== undefined) {
    init.headers["Content-Type"] = "application/json";
    init.body = JSON.stringify(body);
  }
  const r = await fetch(path, init);
  const data = await r.json().catch(() => ({}));
  if (!r.ok) {
    const e = new Error((data.error && data.error.message) || `Error ${r.status}`);
    e.code = data.error && data.error.code;
    e.status = r.status;
    throw e;
  }
  return data;
}

let toastTimer;
function toast(text, bad = false) {
  const t = $("#toast");
  t.textContent = text;
  t.className = "toast" + (bad ? " bad" : "");
  t.hidden = false;
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => (t.hidden = true), bad ? 7000 : 3500);
}

const CTAS = [["LEARN_MORE", "Más información"], ["SHOP_NOW", "Comprar"], ["SIGN_UP", "Registrarte"], ["SUBSCRIBE", "Suscribirte"],
  ["CONTACT_US", "Contactarnos"], ["GET_QUOTE", "Pedir cotización"], ["APPLY_NOW", "Postularte"], ["DOWNLOAD", "Descargar"], ["BOOK_TRAVEL", "Reservar"]];
const DISPLAY = [["AUTO", "Automático (dominio del destino)"], ["CUSTOM", "Personalizado"], ["OMIT_CUSTOM", "Sin personalización (lo decide Meta)"]];
const STATES = {
  QUEUED: ["En cola", "info", "Esperando al publicador."],
  RUNNING: ["Creando…", "info", "Subiendo medios y creando la estructura en pausa."],
  SIMULATED: ["Simulado · no está en Meta", "sim", "Prueba local: no se creó nada en Meta."],
  CREATED_PAUSED: ["Creado en pausa", "ok", "Todo existe en Meta en pausa. No gasta hasta que lo actives."],
  ACTIVATION_REQUESTED: ["Activación solicitada", "ok", "Meta recibió la activación. Revisión y entrega: ver «Estado en Meta»."],
  FAILED: ["Falló", "bad", "Error conocido. Corregí la causa y reintentá: se conservan los objetos ya creados."],
  NEEDS_RECONCILIATION: ["Revisar en Meta", "bad", "Una creación quedó sin confirmar. No se reintenta sola: revisá en Ads Manager y resolvé abajo."],
  STOPPED_PAUSED: ["Detenido · pausado", "warn", "Pausaste el trabajo. Reanudar crea lo que falte, siempre en pausa."],
  PAUSE_INCOMPLETE: ["Pausa sin confirmar", "bad", "Meta no confirmó la pausa de alguna campaña. Volvé a pausar o pausala en Ads Manager."],
};
const PHASES = {
  ACTIVO: ["Activo", "ok"], EN_REVISION: ["En revisión", "info"], PROCESANDO: ["Procesando", "info"], RECHAZADO: ["Rechazado", "bad"],
  CON_PROBLEMAS: ["Con problemas", "bad"], FALTA_MEDIO_DE_PAGO: ["Falta medio de pago", "bad"], PAUSADO: ["Pausado", "warn"],
  ARCHIVADO: ["Archivado", ""], ELIMINADO: ["Eliminado", ""], DESCONOCIDO: ["Desconocido", ""],
};
const STRUCT = { BID_CAP_1_1_10: "Bid Cap 1:1:10", ABO_1_1_1: "ABO 1:1:1" };

const state = {
  settings: null, profile: null, jobs: [], selected: null, detail: null,
  creatives: [], form: null, clientKey: uuid(), draft: null, published: null, busy: false,
  conversation: null, assets: null,
};
try { state.conversation = localStorage.getItem("orbita.conversation"); } catch (e) { /* sin almacenamiento local */ }

function money(minor, currency) {
  if (minor === null || minor === undefined || Number.isNaN(minor)) return "—";
  try {
    return new Intl.NumberFormat("es-AR", { style: "currency", currency: currency || "USD" }).format(minor / 100);
  } catch (e) {
    return `${(minor / 100).toFixed(2)} ${currency || ""}`;
  }
}
const toMinor = (major) => {
  // Formato argentino: "1.000" es mil y "1.000,50" lleva coma decimal. También acepta "1000.5".
  let t = String(major || "").trim().replace(/\s/g, "");
  if (t.includes(",")) t = t.replace(/\./g, "").replace(",", ".");
  else if (/^\d{1,3}(\.\d{3})+$/.test(t)) t = t.replace(/\./g, "");
  const n = parseFloat(t);
  return Number.isFinite(n) ? Math.round(n * 100) : NaN;
};
const toMajor = (minor) => (minor ? String(minor / 100).replace(".", ",") : "");
const chip = (text, kind = "") => h("span", { class: "chip " + kind, text });
const field = (label, input, hint) => h("label", { class: "field" }, label, input, hint ? h("small", { text: hint }) : null);
const selectOf = (options, value, attrs = {}) => h("select", attrs, options.map(([v, t]) => h("option", { value: v, selected: v === value, text: t })));

/* ---------- Tabs, modo y arranque ---------- */

function switchTab(name) {
  document.querySelectorAll(".tabs button").forEach((b) => b.setAttribute("aria-selected", String(b.dataset.tab === name)));
  document.querySelectorAll(".tab").forEach((s) => (s.hidden = s.id !== "tab-" + name));
  if (name === "campanas") refreshJobs();
}

function renderMode() {
  const s = state.settings;
  const badge = $("#mode-badge");
  const banner = $("#banner");
  if (!s) return;
  if (s.mode === "mock") {
    badge.textContent = "SIMULACIÓN";
    badge.className = "mode sim";
    banner.textContent = "Modo simulación: nada se publica en Meta. Cambialo en Conexión cuando la verificación esté OK.";
    banner.hidden = false;
  } else if (!s.live_enabled) {
    badge.textContent = "REAL · publicación deshabilitada";
    badge.className = "mode live-off";
    banner.textContent = "Conectado en modo real con la publicación deshabilitada: podés verificar sin crear nada.";
    banner.hidden = false;
  } else {
    badge.textContent = "REAL · publica en Meta";
    badge.className = "mode live";
    banner.hidden = true;
  }
}

async function loadSettings() {
  state.settings = await api("GET", "/v1/settings");
  renderMode();
}

async function loadProfile() {
  try {
    state.profile = await api("GET", "/v1/profile");
  } catch (e) {
    if (e.code !== "PROFILE_MISSING") throw e;
    state.profile = null;
  }
}

function freshForm() {
  const p = state.profile;
  const d = (p && p.defaults) || {};
  return {
    structure: "BID_CAP_1_1_10", name: "", target: "PAUSED",
    budget: toMajor(p && p.daily_budget_minor), bid: toMajor(p && p.bid_cap_minor),
    shared: {
      primary_text: d.primary_text || "", headline: d.headline || "", description: d.description || "", cta: d.cta || "LEARN_MORE",
      destination_url: d.destination_url || "", display_url_mode: d.display_url_mode || "AUTO", display_url: d.display_url || "",
      utm_template: d.utm_template || "",
    },
  };
}

function touched() {
  // Cada cambio del formulario es un intento nuevo; reintentar sin cambios reutiliza la misma clave (sin duplicar).
  state.clientKey = uuid();
  state.draft = null;
  state.published = null;
  renderSummary();
}

/* ---------- Publicar ---------- */

function kindFromUrl(url) {
  return /\.(mp4|mov|m4v)(\?|$)/i.test(url) ? "video" : "image";
}

async function checkCreative(c) {
  if (c.upload) return;
  c.check = { status: "pending", text: "Verificando enlace…" };
  renderCreatives();
  try {
    const r = await api("POST", "/v1/assets/check", { url: c.url, kind: c.kind });
    c.check = { status: "ok", text: r.kind === "image" ? `${r.format}${r.width ? ` ${r.width}×${r.height}` : ""}` : r.format };
  } catch (e) {
    c.check = { status: "bad", text: e.message };
  }
  renderCreatives();
}

function addLinks(text) {
  const urls = text.split(/\s+/).map((x) => x.trim()).filter(Boolean);
  for (const url of urls) {
    const c = { id: uuid(), url, kind: kindFromUrl(url), overrides: {}, open: false };
    state.creatives.push(c);
    checkCreative(c);
  }
  touched();
  renderCreatives();
}

function uploadFile(file, onProgress) {
  return new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest();
    xhr.open("POST", "/v1/uploads");
    xhr.setRequestHeader("X-File-Name", encodeURIComponent(file.name));
    xhr.setRequestHeader("Content-Type", "application/octet-stream");
    xhr.upload.onprogress = (e) => e.lengthComputable && onProgress(Math.round((e.loaded / e.total) * 100));
    xhr.onload = () => {
      let data = {};
      try { data = JSON.parse(xhr.responseText); } catch (e) { /* respuesta vacía */ }
      if (xhr.status >= 200 && xhr.status < 300) resolve(data);
      else reject(new Error((data.error && data.error.message) || `Error ${xhr.status}`));
    };
    xhr.onerror = () => reject(new Error("No se pudo subir el archivo"));
    xhr.send(file);
  });
}

async function addFiles(files) {
  for (const file of files) {
    const c = { id: uuid(), name: file.name, kind: file.type.startsWith("video") ? "video" : "image", overrides: {}, open: false,
      check: { status: "pending", text: "Subiendo 0%" } };
    state.creatives.push(c);
    renderCreatives();
    try {
      c.upload = await uploadFile(file, (pct) => { c.check = { status: "pending", text: `Subiendo ${pct}%` }; renderCreatives(); });
      c.kind = c.upload.kind;
      c.check = { status: "ok", text: `${c.upload.format}${c.upload.width ? ` ${c.upload.width}×${c.upload.height}` : ""} · subido a Orbita` };
    } catch (e) {
      c.check = { status: "bad", text: e.message };
    }
    touched();
    renderCreatives();
  }
}

function copyEditor(values, onChange, partial) {
  // partial: campos por anuncio; vacío = hereda del lote.
  const set = (k) => (e) => { values[k] = e.target.value; if (k === "display_url_mode" && values[k] !== "CUSTOM") values.display_url = ""; onChange(k); };
  const ph = partial ? "Igual que el lote" : "";
  const displayName = "display-" + uuid();
  const modes = partial ? [["", "Igual que el lote"], ...DISPLAY] : DISPLAY;
  return h("div", { class: "grid" },
    field("Texto principal", h("textarea", { value: values.primary_text || "", placeholder: ph, on: { input: set("primary_text") } })),
    h("div", { class: "grid g2" },
      field("Título", h("input", { type: "text", value: values.headline || "", placeholder: ph, on: { input: set("headline") } })),
      field("Descripción", h("input", { type: "text", value: values.description || "", placeholder: partial ? ph : "Opcional", on: { input: set("description") } }))),
    h("div", { class: "grid g2" },
      field("Llamado a la acción", selectOf(partial ? [["", "Igual que el lote"], ...CTAS] : CTAS, values.cta || "", { on: { change: set("cta") } })),
      field("URL de destino", h("input", { type: "url", value: values.destination_url || "", placeholder: partial ? ph : "https://tu-sitio.com/landing", on: { input: set("destination_url") } }),
        partial ? null : "La landing a la que lleva el anuncio. No es el archivo del creativo.")),
    field("Enlace visible", h("div", { class: "radios" }, modes.map(([v, t]) => h("label", {},
      h("input", { type: "radio", name: displayName, value: v, checked: (values.display_url_mode || "") === v, on: { change: (e) => { set("display_url_mode")(e); renderAgain(); } } }), t)))),
    (values.display_url_mode === "CUSTOM") ? field("URL visible", h("input", { type: "text", value: values.display_url || "", placeholder: "tu-sitio.com/oferta", on: { input: set("display_url") } }),
      "Debe ser del mismo dominio que el destino.") : null,
    h("div", { class: "note" }, "Meta decide cómo se ve el enlace en cada ubicación y no lo usa en Instagram. Ninguna opción garantiza ocultar el dominio."),
  );
  function renderAgain() { partial ? renderCreatives() : renderPublish(); }
}

function renderCreatives() {
  const box = $("#creatives");
  if (!box) return;
  put(box);
  const n = state.creatives.length;
  const need = state.form.structure === "BID_CAP_1_1_10" ? 10 : null;
  put($("#creative-count"), need ? chip(`${n}/10`, n === 10 ? "ok" : "warn") : chip(`${n} creativo${n === 1 ? "" : "s"}`, n ? "ok" : ""));
  state.creatives.forEach((c, i) => {
    const thumb = c.upload && c.upload.kind === "image" ? h("img", { class: "thumb", src: `/v1/uploads/${c.upload.id}/file`, alt: "" })
      : (!c.upload && c.kind === "image" && c.check && c.check.status === "ok") ? h("img", { class: "thumb", src: c.url, alt: "", referrerpolicy: "no-referrer" })
      : h("div", { class: "thumb" }, c.kind === "video" ? "VIDEO" : "IMG");
    const status = c.check ? chip(c.check.text, c.check.status === "ok" ? "ok" : c.check.status === "bad" ? "bad" : "info") : null;
    const cover = c.kind !== "video" ? null : h("div", { class: "row" },
      h("span", { class: "hint", text: "Portada:" }),
      c.thumbUpload ? chip("imagen subida", "ok") : null,
      h("input", { type: "url", placeholder: "Enlace JPG/PNG (opcional; si no, la genera Meta)", value: c.thumbUrl || "",
        on: { input: (e) => { c.thumbUrl = e.target.value.trim(); c.thumbUpload = null; touched(); } } }),
      h("label", { class: "btn small" }, "Subir portada", h("input", { type: "file", accept: "image/jpeg,image/png", hidden: true,
        on: { change: async (e) => { try { c.thumbUpload = await uploadFile(e.target.files[0], () => {}); c.thumbUrl = ""; touched(); renderCreatives(); } catch (err) { toast(err.message, true); } } } })));
    const row = h("div", { class: "creative", "data-creative": String(i) },
      thumb,
      h("div", {},
        h("div", { class: "row" }, h("strong", { text: `Anuncio ${i + 1}` }),
          c.upload ? null : selectOf([["image", "Imagen"], ["video", "Video"]], c.kind, { on: { change: (e) => { c.kind = e.target.value; touched(); checkCreative(c); } } }),
          status),
        h("div", { class: "src", text: c.upload ? `Archivo: ${c.upload.name || c.name}` : c.url || c.name || "" }),
        cover),
      h("div", { class: "row" },
        h("button", { class: "btn small", type: "button", text: c.open ? "Cerrar" : "Personalizar", on: { click: () => { c.open = !c.open; renderCreatives(); } } }),
        h("button", { class: "btn small danger", type: "button", text: "Quitar", on: { click: () => { state.creatives.splice(i, 1); touched(); renderCreatives(); } } })),
      c.open ? h("div", { class: "overrides" }, h("h3", { text: "Cambios solo para este anuncio" }), copyEditor(c.overrides, touched, true)) : null);
    box.append(row);
  });
  renderSummary();
}

function buildRequest() {
  const f = state.form;
  const media = state.creatives.map((c) => {
    const m = { kind: c.kind };
    if (c.upload) m.upload_id = c.upload.id; else m.url = c.url;
    if (c.kind === "video") {
      if (c.thumbUpload) m.thumbnail_upload_id = c.thumbUpload.id;
      else if (c.thumbUrl) m.thumbnail_url = c.thumbUrl;
    }
    const ov = {};
    for (const [k, v] of Object.entries(c.overrides)) if (v !== "" && v !== undefined) ov[k] = v;
    if (ov.display_url_mode && ov.display_url_mode !== "CUSTOM") ov.display_url = "";
    if (Object.keys(ov).length) m.overrides = ov;
    return m;
  });
  const shared = { ...f.shared };
  if (shared.display_url_mode !== "CUSTOM") shared.display_url = "";
  const req = { name: f.name.trim(), structure: f.structure, media, shared, daily_budget_minor: toMinor(f.budget), target_status: f.target };
  if (f.structure === "BID_CAP_1_1_10") req.bid_cap_minor = toMinor(f.bid);
  return req;
}

function renderSummary() {
  const box = $("#summary");
  if (!box || !state.form) return;
  const f = state.form;
  const n = state.creatives.length;
  const campaigns = f.structure === "BID_CAP_1_1_10" ? 1 : n;
  const cur = (state.profile && state.profile.currency) || "";
  const per = toMinor(f.budget);
  const s = state.draft ? state.draft.summary : null;
  const rows = [
    ["Estructura", STRUCT[f.structure]],
    ["Campañas", s ? s.campaigns : campaigns], ["Conjuntos", s ? s.adsets : campaigns], ["Anuncios", s ? s.ads : n],
    ["Moneda", cur || "—"],
    ["Presupuesto por conjunto", money(per, cur)],
    f.structure === "BID_CAP_1_1_10" ? ["Puja máxima (Bid Cap)", money(toMinor(f.bid), cur)] : ["Puja", "Sin tope (menor costo)"],
    ["Al terminar", f.target === "ACTIVE" ? "Activar (gasta)" : "Queda en pausa"],
  ];
  const total = s ? s.total_daily_budget_minor : campaigns * per;
  const need10 = f.structure === "BID_CAP_1_1_10" && n !== 10;
  put(box, 
    h("h2", { text: "Resumen del lote" }),
    h("dl", {}, rows.map(([k, v]) => [h("dt", { text: k }), h("dd", { text: String(v) })])),
    h("hr"),
    h("div", { class: "row" }, h("span", { class: "muted", text: "Presupuesto diario agregado" })),
    h("div", { class: "total", text: money(total, cur), "data-total": String(total) }),
    h("div", { class: "note" }, "Corresponde solo a este lote: no limita el gasto de otras campañas existentes. El diario de Meta no es un tope estricto."),
    state.draft ? h("div", { class: "note" }, h("strong", { text: "Borrador verificado por el servidor. " }), state.draft.warnings.join(" ")) : null,
    need10 ? h("div", { class: "note warn", text: `Bid Cap 1:1:10 necesita exactamente 10 creativos (tenés ${n}).` }) : null,
    h("div", { class: "row end" },
      h("button", { class: "btn", type: "button", id: "btn-review", text: "Revisar", disabled: state.busy || !n, on: { click: () => prepare(false) } }),
      state.published
        ? h("button", { class: "btn primary", type: "button", text: "Ver en Campañas", on: { click: () => { state.selected = state.published; switchTab("campanas"); } } })
        : h("button", { class: "btn primary", type: "button", id: "btn-publish", disabled: state.busy || !n || need10,
          text: state.busy ? "Publicando…" : (f.target === "ACTIVE" ? "Publicar y activar" : "Publicar en pausa"), on: { click: () => prepare(true) } })),
  );
}

async function prepare(publish) {
  if (!state.profile) { toast("Primero completá la configuración en Conexión", true); switchTab("conexion"); return; }
  if (!state.form.name.trim()) { toast("Poné un nombre al lote", true); $("#batch-name").focus(); return; }
  state.busy = true;
  renderSummary();
  try {
    // Misma clave mientras no cambie el formulario: doble clic, recarga o timeout devuelven el mismo borrador.
    state.draft = await api("POST", "/v1/drafts", buildRequest(), { "Idempotency-Key": state.clientKey });
    if (publish) {
      const job = await api("POST", `/v1/drafts/${state.draft.draft_id}/publish`, { plan_hash: state.draft.plan_hash },
        { "Idempotency-Key": "orbita-" + state.draft.draft_id });
      state.published = job.id;
      state.selected = job.id;
      toast(state.settings.mode === "mock" ? "Publicación simulada en curso" : "Publicando en Meta…");
      refreshJobs();
    }
  } catch (e) {
    toast(e.message, true);
  } finally {
    state.busy = false;
    renderSummary();
  }
}

function renderPublish() {
  const root = $("#tab-publicar");
  if (!state.form) state.form = freshForm();
  const f = state.form;
  const p = state.profile;
  const cur = (p && p.currency) || "";
  const linkBox = h("textarea", { id: "links", placeholder: "https://cdn.tu-sitio.com/anuncio-1.jpg\nhttps://cdn.tu-sitio.com/video-2.mp4" });
  put(root, h("div", { class: "split" },
    h("div", {},
      !p ? h("div", { class: "card" }, h("strong", { text: "Falta la configuración. " }), "Completá cuenta, página y datos habituales en ",
        h("button", { class: "btn small", type: "button", text: "Conexión", on: { click: () => switchTab("conexion") } })) : null,
      h("div", { class: "card" },
        h("h2", { text: "Estructura" }),
        h("div", { class: "choice" },
          [["BID_CAP_1_1_10", "Bid Cap 1:1:10", "1 campaña · 1 conjunto · 10 anuncios. Puja máxima y presupuesto en el conjunto."],
            ["ABO_1_1_1", "ABO 1:1:1", "1 campaña + 1 conjunto + 1 anuncio por creativo. Presupuesto por conjunto, sin tope de puja."]].map(([v, t, d]) =>
            h("label", {}, h("input", { type: "radio", name: "structure", value: v, checked: f.structure === v,
              on: { change: () => { f.structure = v; touched(); renderPublish(); } } }), h("span", {}, h("strong", { text: t }), h("span", { class: "hint", text: d }))))),
        h("div", { class: "grid g2" },
          field("Nombre del lote", h("input", { type: "text", id: "batch-name", value: f.name, placeholder: "Lanzamiento noviembre", on: { input: (e) => { f.name = e.target.value; touched(); } } })),
          field("Al terminar", selectOf([["PAUSED", "Dejar en pausa"], ["ACTIVE", "Activar al terminar (empieza a gastar)"]], f.target,
            { on: { change: (e) => { f.target = e.target.value; touched(); } } })))),
      h("div", { class: "card" },
        h("div", { class: "row" }, h("h2", { text: "Creativos" }), h("span", { id: "creative-count" })),
        h("p", { class: "hint", text: "Enlace directo al archivo (.jpg, .png, .mp4, .mov), no la landing ni una carpeta de Drive. O subí los archivos." }),
        linkBox,
        h("div", { class: "row" },
          h("button", { class: "btn", type: "button", text: "Agregar enlaces", on: { click: () => { addLinks(linkBox.value); linkBox.value = ""; } } }),
          h("label", { class: "btn" }, "Subir archivos",
            h("input", { type: "file", multiple: true, hidden: true, accept: "image/jpeg,image/png,video/mp4,video/quicktime", "data-upload": "media",
              on: { change: (e) => { addFiles([...e.target.files]); e.target.value = ""; } } })),
          state.creatives.length ? h("button", { class: "btn small danger", type: "button", text: "Quitar todos", on: { click: () => { state.creatives = []; touched(); renderCreatives(); } } }) : null),
        h("div", { class: "creatives", id: "creatives" })),
      h("div", { class: "card" },
        h("h2", { text: "Texto y destino (para todo el lote)" }),
        h("p", { class: "hint", text: "Vienen de tus datos habituales. Cada anuncio puede cambiarlos con «Personalizar»." }),
        copyEditor(f.shared, touched, false),
        h("hr"),
        field("Parámetros UTM", h("input", { type: "text", id: "utm", value: f.shared.utm_template, placeholder: "utm_source={{site_source_name}}&utm_medium=paid&utm_campaign={{campaign.name}}",
          on: { input: (e) => { f.shared.utm_template = e.target.value; touched(); } } }),
          "Se envían aparte de la URL (url_tags). Las macros {{...}} de Meta se conservan tal cual. No repitas parámetros que ya tenga la URL de destino."),
        h("div", { class: "row" },
          h("button", { class: "btn small", type: "button", id: "save-utm", text: "Guardar como predeterminado", on: { click: saveUtm } }),
          p && p.defaults.utm_template ? h("span", { class: "hint", text: "Predeterminado actual guardado." }) : null)),
      h("div", { class: "card" },
        h("h2", { text: "Presupuesto" }),
        h("div", { class: "grid g2" },
          field(`Diario por conjunto (${cur || "moneda de la cuenta"})`, h("input", { type: "text", inputmode: "decimal", id: "budget", value: f.budget, on: { input: (e) => { f.budget = e.target.value; touched(); } } })),
          f.structure === "BID_CAP_1_1_10" ? field(`Puja máxima (${cur})`, h("input", { type: "text", inputmode: "decimal", id: "bid", value: f.bid, on: { input: (e) => { f.bid = e.target.value; touched(); } } }),
            "Bid Cap: tope de puja en la subasta. No es Cost Cap ni un CPA garantizado.") : h("div", { class: "hint", text: "ABO usa menor costo sin tope de puja." })))),
    h("div", { class: "card summary sticky", id: "summary" })));
  renderCreatives();
}

async function saveUtm() {
  try {
    const p = await api("PUT", "/v1/profile/defaults", { utm_template: state.form.shared.utm_template });
    state.profile = p;
    state.form.shared.utm_template = p.defaults.utm_template;
    $("#utm").value = p.defaults.utm_template;
    toast("UTM guardado como predeterminado");
  } catch (e) {
    toast(e.message, true);
  }
}

/* ---------- Campañas ---------- */

let pollTimer;
async function refreshJobs() {
  try {
    state.jobs = (await api("GET", "/v1/jobs?limit=100")).jobs;
    if (state.selected) state.detail = await api("GET", `/v1/jobs/${state.selected}`);
  } catch (e) {
    toast(e.message, true);
  }
  renderJobs();
  clearTimeout(pollTimer);
  const active = state.jobs.some((j) => j.state === "QUEUED" || j.state === "RUNNING");
  if (active || !$("#tab-campanas").hidden) pollTimer = setTimeout(refreshJobs, active ? 1500 : 6000);
}

function stateChip(s) {
  const [t, k] = STATES[s] || [s, ""];
  return chip(t, k);
}

function renderJobs() {
  const root = $("#tab-campanas");
  const rows = state.jobs.map((j) => h("tr", { "data-id": j.id, class: j.id === state.selected ? "sel" : "", on: { click: () => { state.selected = j.id; state.remote = null; refreshJobs(); } } },
    h("td", {}, h("strong", { text: j.summary.name || "(sin nombre)" }), h("div", { class: "hint", text: new Date(j.created * 1000).toLocaleString("es-AR") })),
    h("td", { text: STRUCT[j.summary.structure] || j.summary.structure || "" }),
    h("td", { text: `${j.summary.campaigns} / ${j.summary.adsets} / ${j.summary.ads}` }),
    h("td", { text: money(j.summary.total_daily_budget_minor, j.summary.currency) }),
    h("td", {}, stateChip(j.state), " ", j.mode === "mock" ? chip("SIM", "sim") : chip("REAL", "info"))));
  put(root, 
    h("div", { class: "card" },
      h("div", { class: "row" }, h("h2", { text: "Publicaciones" }), h("button", { class: "btn small", type: "button", text: "Actualizar", on: { click: refreshJobs } })),
      state.jobs.length ? h("table", { class: "list" },
        h("thead", {}, h("tr", {}, ["Lote", "Estructura", "Camp. / conj. / anuncios", "Diario agregado", "Estado"].map((t) => h("th", { text: t })))),
        h("tbody", {}, rows)) : h("p", { class: "muted", text: "Todavía no publicaste nada." })),
    state.detail ? renderDetail(state.detail) : null);
}

function renderDetail(job) {
  const item = state.jobs.find((j) => j.id === job.id) || {};
  const summary = item.summary || {};
  const done = job.steps.filter((s) => s.state === "DONE").length;
  const [label, , help] = STATES[job.state] || [job.state, "", ""];
  const bar = h("div", { class: "progress" }, h("div"));
  bar.firstChild.style.width = `${job.steps.length ? Math.round((done / job.steps.length) * 100) : 0}%`;
  const complete = job.steps.length && done === job.steps.length;
  const uncertain = job.steps.filter((s) => s.state === "UNCERTAIN");
  const act = (label, fn, cls = "btn") => h("button", { class: cls, type: "button", text: label, on: { click: fn } });
  return h("div", { class: "card", id: "job-detail" },
    h("div", { class: "row" }, h("h2", { text: summary.name || "Publicación" }), stateChip(job.state)),
    h("p", { class: "hint", text: help }),
    bar,
    h("p", { class: "hint", text: `${done} de ${job.steps.length} pasos · ${summary.campaigns} campañas, ${summary.adsets} conjuntos, ${summary.ads} anuncios · ${money(summary.total_daily_budget_minor, summary.currency)} por día` }),
    job.error ? h("div", { class: "note warn", text: job.error }) : null,
    h("div", { class: "row" },
      ["CREATED_PAUSED", "ACTIVATION_REQUESTED", "STOPPED_PAUSED", "PAUSE_INCOMPLETE", "RUNNING", "QUEUED", "FAILED", "NEEDS_RECONCILIATION", "SIMULATED"].includes(job.state)
        ? act("Pausar", () => jobAction(job, "pause")) : null,
      complete && ["CREATED_PAUSED", "STOPPED_PAUSED", "SIMULATED", "ACTIVATION_REQUESTED"].includes(job.state)
        ? act("Activar", () => jobAction(job, "activate", item), "btn primary") : null,
      ["FAILED", "STOPPED_PAUSED", "NEEDS_RECONCILIATION"].includes(job.state) && !(job.state === "STOPPED_PAUSED" && complete)
        ? act(job.state === "STOPPED_PAUSED" ? "Reanudar (queda en pausa)" : "Reintentar", () => jobAction(job, "retry")) : null,
      act("Estado en Meta", () => loadRemote(job, "remote")),
      act("Métricas de hoy", () => loadRemote(job, "insights")),
      act("Vista previa", () => loadRemote(job, "previews"))),
    uncertain.length ? reconcileForm(job, uncertain) : null,
    h("div", { id: "remote" }, state.remote && state.remote.job === job.id ? state.remote.node : null),
    h("details", {}, h("summary", { text: "Pasos e IDs" }),
      h("table", { class: "list" }, h("tbody", {}, job.steps.map((s) => h("tr", {},
        h("td", { class: "mono", text: s.key }), h("td", {}, chip(s.state, s.state === "DONE" ? "ok" : s.state === "FAILED" || s.state === "UNCERTAIN" ? "bad" : "info")),
        h("td", { class: "mono", text: s.result ? (s.result.id || s.result.hash || s.result.url || "") : (s.error || "") })))))));
}

async function jobAction(job, action, item) {
  try {
    if (action === "activate") {
      const s = item.summary;
      const ok = window.confirm(`Activar empieza a gastar: ${money(s.total_daily_budget_minor, s.currency)} por día en ${s.campaigns} campaña(s). ¿Activar?`);
      if (!ok) return;
      await api("POST", `/v1/jobs/${job.id}/activate`, { plan_hash: item.plan_hash });
    } else {
      await api("POST", `/v1/jobs/${job.id}/${action}`, {});
    }
    toast({ pause: "Pausa enviada", activate: "Activación encolada", retry: "Reintento encolado" }[action]);
  } catch (e) {
    toast(e.message, true);
  }
  refreshJobs();
}

function reconcileForm(job, steps) {
  const sel = selectOf(steps.map((s) => [s.key, s.key]), steps[0].key);
  const res = selectOf([["ATTACH", "Existe en Meta: adjuntar ID"], ["NOT_CREATED", "Verifiqué que NO se creó"]], "ATTACH");
  const rid = h("input", { type: "text", placeholder: "ID del objeto en Meta" });
  const ev = h("input", { type: "text", placeholder: "Qué verificaste en Ads Manager" });
  return h("div", { class: "card" },
    h("h3", { text: "Resolver creación sin confirmar" }),
    h("p", { class: "hint", text: "Buscá en Ads Manager el nombre con el marcador [orbita:…]. No elijas «no se creó» sin comprobarlo." }),
    h("div", { class: "grid g2" }, field("Paso", sel), field("Resultado", res), field("ID en Meta", rid), field("Evidencia", ev)),
    h("div", { class: "row end" }, h("button", { class: "btn", type: "button", text: "Guardar resolución", on: { click: async () => {
      const body = { step_key: sel.value, resolution: res.value, evidence: ev.value };
      if (res.value === "ATTACH") body.remote_id = rid.value.trim();
      try { await api("POST", `/v1/jobs/${job.id}/resolve`, body); toast("Resolución guardada"); refreshJobs(); } catch (e) { toast(e.message, true); }
    } } })));
}

async function loadRemote(job, kind) {
  const holder = $("#remote");
  put(holder, h("p", { class: "muted", text: "Consultando…" }));
  try {
    let node;
    if (kind === "remote") {
      const r = await api("GET", `/v1/jobs/${job.id}/remote`);
      node = h("div", { class: "card" },
        h("div", { class: "row" }, h("h3", { text: "Estado en Meta" }), r.summary.delivering ? chip("Entregando (hay impresiones)", "ok") : chip("Sin impresiones todavía", "")),
        h("p", { class: "hint", text: r.summary.note }),
        h("table", { class: "list" }, h("tbody", {}, r.results.map((x) => {
          const [t, k] = PHASES[x.data.phase] || [x.data.phase, ""];
          const fb = x.data.ad_review_feedback ? JSON.stringify(x.data.ad_review_feedback) : "";
          return h("tr", {}, h("td", { text: { campaign: "Campaña", adset: "Conjunto", ad: "Anuncio" }[x.kind] }), h("td", { text: x.data.name || x.data.id }),
            h("td", {}, chip(t, k)), h("td", { class: "mono", text: x.data.effective_status || "" }), h("td", { class: "hint", text: fb }));
        }))));
    } else if (kind === "insights") {
      const r = await api("GET", `/v1/jobs/${job.id}/insights`);
      const rows = r.results.flatMap((x) => (x.data.data || []).map((d) => h("tr", {}, h("td", { class: "mono", text: d.campaign_id || x.step }),
        h("td", { text: d.impressions || "0" }), h("td", { text: d.clicks || "0" }), h("td", { text: d.spend || "0" }))));
      node = h("div", { class: "card" }, h("h3", { text: "Métricas de hoy (zona horaria de la cuenta)" }),
        rows.length ? h("table", { class: "list" }, h("thead", {}, h("tr", {}, ["Campaña", "Impresiones", "Clics", "Gasto"].map((t) => h("th", { text: t })))), h("tbody", {}, rows))
          : h("p", { class: "muted", text: r.mode === "mock" ? "Simulación: no hay métricas reales." : "Sin datos todavía." }));
    } else {
      const fmt = selectOf([["DESKTOP_FEED_STANDARD", "Feed escritorio"], ["MOBILE_FEED_STANDARD", "Feed móvil"], ["INSTAGRAM_STANDARD", "Instagram feed"],
        ["INSTAGRAM_STORY", "Instagram stories"], ["INSTAGRAM_REELS", "Instagram reels"], ["FACEBOOK_REELS_MOBILE", "Facebook reels"]], state.previewFormat || "MOBILE_FEED_STANDARD",
      { on: { change: (e) => { state.previewFormat = e.target.value; loadRemote(job, "previews"); } } });
      const r = await api("GET", `/v1/jobs/${job.id}/previews?format=${encodeURIComponent(state.previewFormat || "MOBILE_FEED_STANDARD")}`);
      const frames = r.results.map((x) => {
        const body = (x.data.data && x.data.data[0] && x.data.data[0].body) || "";
        // Se toma solo la URL del iframe de Meta; el HTML remoto nunca se inserta en esta página.
        const frame = new DOMParser().parseFromString(body, "text/html").querySelector("iframe");
        const src = frame && frame.getAttribute("src");
        return src && /^https:\/\/(www\.)?facebook\.com\//.test(src)
          ? h("iframe", { src, sandbox: "allow-scripts allow-same-origin allow-popups", loading: "lazy", referrerpolicy: "no-referrer", title: `Vista previa ${x.step}` })
          : h("div", { class: "note", text: r.mode === "mock" ? "Simulación: no hay vista previa real de Meta." : "Meta no devolvió una vista previa para este formato." });
      });
      node = h("div", { class: "card" }, h("div", { class: "row" }, h("h3", { text: "Vista previa" }), fmt), h("div", { class: "previews" }, frames));
    }
    state.remote = { job: job.id, node };
    put(holder, node);
  } catch (e) {
    put(holder, h("div", { class: "note warn", text: e.message }));
  }
}

/* ---------- Conexión ---------- */

function secretCard(name, title, hint, link) {
  const st = state.settings.secrets[name];
  const input = h("input", { type: "password", autocomplete: "off", placeholder: st.configured ? "Cargado. Pegá uno nuevo para reemplazarlo" : "Pegalo acá (queda solo en este servidor)" });
  return h("div", { class: "grid" },
    h("div", { class: "row" }, h("strong", { text: title }),
      st.configured ? chip(st.source === "env" ? "Desde variable de entorno" : "Guardado en el servidor", "ok") : chip("Falta", "warn")),
    hint ? h("span", { class: "hint" }, hint, link ? [" ", h("a", { href: link, target: "_blank", rel: "noopener noreferrer", text: "Abrir" })] : null) : null,
    h("div", { class: "row" }, input,
      h("button", { class: "btn", type: "button", text: "Guardar", "data-secret": name, on: { click: async () => {
        try { state.settings = await api("PUT", `/v1/secrets/${name}`, { value: input.value }); input.value = ""; toast("Guardado en el servidor"); renderMode(); renderConnection(); }
        catch (e) { toast(e.message, true); }
      } } }),
      st.configured && st.source !== "env" ? h("button", { class: "btn danger", type: "button", text: "Borrar", on: { click: async () => {
        try { state.settings = await api("DELETE", `/v1/secrets/${name}`); toast("Borrado"); renderMode(); renderConnection(); } catch (e) { toast(e.message, true); }
      } } }) : null));
}

function profileForm() {
  const p = state.profile || {};
  const d = p.defaults || {};
  const v = {
    account_id: p.account_id || "", page_id: p.page_id || "", pixel_id: p.pixel_id || "", instagram_user_id: p.instagram_user_id || "",
    currency: p.currency || "ARS", objective: p.objective || "SALES", countries: (p.countries || ["AR"]).join(", "),
    age_min: p.age_min || 18, age_max: p.age_max || 65, advantage_audience: !!p.advantage_audience,
    budget: toMajor(p.daily_budget_minor), max_batch: toMajor(p.max_batch_daily_budget_minor), bid: toMajor(p.bid_cap_minor),
    defaults: { primary_text: d.primary_text || "", headline: d.headline || "", description: d.description || "", cta: d.cta || "LEARN_MORE",
      destination_url: d.destination_url || "", display_url_mode: d.display_url_mode || "AUTO", display_url: d.display_url || "", utm_template: d.utm_template || "" },
  };
  state.profileDraft = v;
  const inp = (k, attrs = {}) => h("input", { type: "text", value: v[k], id: "pf-" + k, ...attrs, on: { input: (e) => { v[k] = e.target.value; } } });
  const a = state.assets;
  const pick = (items, key, label, fmt) => (items && items.length) ? selectOf([["", `Elegir ${label}…`], ...items.map((x) => [String(x.id), fmt(x)])], v[key],
    { on: { change: (e) => { v[key] = e.target.value; $("#pf-" + key).value = e.target.value; if (key === "account_id") discover(e.target.value); } } }) : null;
  return h("div", { class: "grid" },
    h("div", { class: "grid g2" },
      field("Cuenta publicitaria", h("div", { class: "grid" }, pick(a && a.ad_accounts && a.ad_accounts.items, "account_id", "cuenta", (x) => `${x.name} · ${x.currency} · ${x.id}`), inp("account_id", { placeholder: "act_123…" }))),
      field("Página de Facebook", h("div", { class: "grid" }, pick(a && ((a.promote_pages && a.promote_pages.items.length && a.promote_pages.items) || (a.pages && a.pages.items)), "page_id", "página", (x) => `${x.name} · ${x.id}`), inp("page_id", { placeholder: "ID numérico" }))),
      field("Píxel (obligatorio para Ventas)", h("div", { class: "grid" }, pick(a && a.pixels && a.pixels.items, "pixel_id", "píxel", (x) => `${x.name} · ${x.id}`), inp("pixel_id", { placeholder: "ID numérico" }))),
      field("Instagram (opcional)", h("div", { class: "grid" }, pick(a && a.instagram_accounts && a.instagram_accounts.items, "instagram_user_id", "Instagram", (x) => `@${x.username || x.id}`), inp("instagram_user_id", { placeholder: "ID numérico" })))),
    h("div", { class: "grid g3" },
      field("Moneda de la cuenta", selectOf([["ARS", "ARS"], ["USD", "USD"], ["EUR", "EUR"], ["BRL", "BRL"]], v.currency, { on: { change: (e) => (v.currency = e.target.value) } }), "Debe coincidir con la de Meta."),
      field("Objetivo", selectOf([["SALES", "Ventas (compras con píxel)"], ["TRAFFIC", "Tráfico al sitio"]], v.objective, { on: { change: (e) => (v.objective = e.target.value) } })),
      field("Países", inp("countries", { placeholder: "AR, UY" }), "Códigos de 2 letras.")),
    h("div", { class: "grid g3" },
      field("Edad mínima", inp("age_min", { type: "number", min: "18", max: "65" })),
      field("Edad máxima", inp("age_max", { type: "number", min: "18", max: "65" })),
      field("Advantage+ audiencia", h("label", { class: "row" }, h("input", { type: "checkbox", checked: v.advantage_audience, on: { change: (e) => (v.advantage_audience = e.target.checked) } }), "Dejar que Meta amplíe el público"),
        "Apagado respeta tu segmentación. Encendido exige edad mínima 18-25 y máxima 65.")),
    h("div", { class: "grid g3" },
      field(`Presupuesto diario habitual por conjunto`, inp("budget", { inputmode: "decimal" })),
      field("Máximo diario por lote", inp("max_batch", { inputmode: "decimal" }), "Freno de seguridad: suma de un lote. No limita otras campañas."),
      field("Puja máxima habitual (Bid Cap)", inp("bid", { inputmode: "decimal" }))),
    h("h3", { text: "Anuncio por defecto" }),
    copyEditor(v.defaults, () => {}, false),
    field("UTM predeterminado", h("input", { type: "text", value: v.defaults.utm_template, on: { input: (e) => (v.defaults.utm_template = e.target.value) } })),
    h("div", { class: "row end" }, h("button", { class: "btn primary", type: "button", id: "save-profile", text: "Guardar configuración", on: { click: saveProfile } })));
}

async function saveProfile() {
  const v = state.profileDraft;
  const body = {
    account_id: v.account_id.trim(), page_id: v.page_id.trim(), currency: v.currency, objective: v.objective,
    countries: v.countries.split(/[\s,]+/).filter(Boolean).map((x) => x.toUpperCase()),
    age_min: parseInt(v.age_min, 10), age_max: parseInt(v.age_max, 10), advantage_audience: v.advantage_audience,
    daily_budget_minor: toMinor(v.budget), max_batch_daily_budget_minor: toMinor(v.max_batch), defaults: { ...v.defaults },
  };
  if (v.pixel_id.trim()) body.pixel_id = v.pixel_id.trim();
  if (v.instagram_user_id.trim()) body.instagram_user_id = v.instagram_user_id.trim();
  if (v.bid.trim()) body.bid_cap_minor = toMinor(v.bid);
  if (body.defaults.display_url_mode !== "CUSTOM") body.defaults.display_url = "";
  try {
    state.profile = await api("PUT", "/v1/profile", body);
    state.form = freshForm();
    touched();
    renderPublish();
    renderConnection();
    toast("Configuración guardada");
  } catch (e) {
    toast(e.message, true);
  }
}

async function discover(accountId) {
  try {
    state.assets = await api("GET", "/v1/setup/assets" + (accountId ? `?account_id=${encodeURIComponent(accountId)}` : ""));
    if (state.assets.simulated) toast("Simulación: no hay activos reales para buscar");
  } catch (e) {
    toast(e.message, true);
  }
  renderConnection();
}

async function verify() {
  const box = $("#verify-result");
  put(box, h("p", { class: "muted", text: "Comprobando con Meta…" }));
  try {
    const r = await api("POST", "/v1/setup/verify", {});
    if (r.simulated) {
      put(box, h("div", { class: "note", text: "Estás en simulación: pasá a modo real para comprobar tu cuenta." }));
      return;
    }
    const names = { token: "Token", permissions: "Permisos", account: "Cuenta publicitaria", page: "Página", pixel: "Píxel", instagram: "Instagram", write_campaign: "Permiso de publicación (validado sin crear nada)" };
    const detail = (k, c) => {
      if (!c.ok) return c.error;
      if (k === "token") return c.identity && c.identity.name;
      if (k === "permissions") return c.granted.join(", ") + (c.ads_management ? "" : " · falta ads_management");
      if (k === "account") return `${c.name} · ${c.currency} · ${c.timezone}`;
      if (k === "write_campaign") return "Meta aceptó una creación de prueba en modo validate_only";
      return c.name;
    };
    put(box, 
      h("div", { class: "row" }, r.read_verified ? chip("Lectura verificada", "ok") : chip("Lectura con problemas", "bad"),
        r.write_validated ? chip("Publicación validada", "ok") : chip("Publicación sin validar", "bad")),
      h("ul", { class: "checks" }, Object.entries(r.checks).map(([k, c]) => h("li", {}, chip(c.ok ? "OK" : "Error", c.ok ? "ok" : "bad"), h("strong", { text: names[k] || k }), h("span", { class: "hint", text: detail(k, c) || "" })))),
      h("div", { class: "note", text: r.note }));
  } catch (e) {
    put(box, h("div", { class: "note warn", text: e.message }));
  }
}

function renderConnection() {
  const root = $("#tab-conexion");
  const s = state.settings;
  const live = s.mode === "live";
  put(root, 
    h("div", { class: "card step" },
      h("h2", { text: "1 · Modo" }),
      h("div", { class: "radios" },
        h("label", {}, h("input", { type: "radio", name: "mode", checked: !live, on: { change: () => setRuntime({ mode: "mock" }) } }), "Simulación (no publica)"),
        h("label", {}, h("input", { type: "radio", name: "mode", checked: live, on: { change: () => setRuntime({ mode: "live" }) } }), "Real (API oficial de Meta)")),
      live ? h("label", { class: "row" }, h("input", { type: "checkbox", id: "live-enabled", checked: s.live_enabled, on: { change: (e) => setRuntime({ live_enabled: e.target.checked }) } }),
        "Habilitar publicación real (crea objetos en tu cuenta)") : null,
      h("p", { class: "hint", text: "Recomendado: modo real con publicación deshabilitada hasta que «Comprobar» dé todo OK." })),
    h("div", { class: "card step" },
      h("h2", { text: "2 · Token de Meta" }),
      secretCard("meta_access_token", "Token de acceso",
        "Token de un usuario del sistema de tu portfolio con ads_management y ads_read. Se guarda solo en este servidor; no se muestra ni se envía al navegador.",
        "https://business.facebook.com/settings/system-users"),
      h("hr"),
      secretCard("meta_app_secret", "Clave secreta de la app (opcional)", "Activa appsecret_proof en cada llamada.", "https://developers.facebook.com/apps")),
    h("div", { class: "card step" },
      h("h2", { text: "3 · Comprobar conexión" }),
      h("div", { class: "row" }, h("button", { class: "btn primary", type: "button", id: "btn-verify", text: "Comprobar", on: { click: verify } }),
        h("button", { class: "btn", type: "button", text: "Buscar mis activos", on: { click: () => discover(state.profileDraft && state.profileDraft.account_id) } })),
      h("div", { id: "verify-result" }),
      state.assets && !state.assets.simulated ? h("div", { class: "note" }, Object.entries(state.assets).filter(([, x]) => x && x.ok === false).map(([k, x]) => h("div", { text: `${k}: ${x.error}` }))) : null),
    h("div", { class: "card step" }, h("h2", { text: "4 · Datos habituales" }),
      h("p", { class: "hint", text: "Se configuran una vez y se reutilizan en cada publicación. Importes en la moneda de la cuenta (ej.: 1000,50)." }),
      profileForm()),
    h("div", { class: "card step" }, h("h2", { text: "5 · Asistente IA" }),
      secretCard("anthropic_api_key", "API key de Anthropic", "Para que el asistente prepare, publique y consulte campañas con estas mismas reglas.", "https://console.anthropic.com/settings/keys")));
}

async function setRuntime(change) {
  try {
    state.settings = await api("PUT", "/v1/settings/runtime", change);
    renderMode();
    renderConnection();
    toast(state.settings.mode === "mock" ? "Modo simulación" : state.settings.live_enabled ? "Publicación real habilitada" : "Modo real (publicación deshabilitada)");
  } catch (e) {
    toast(e.message, true);
  }
}

/* ---------- Asistente ---------- */

async function renderAssistant() {
  const root = $("#tab-asistente");
  const log = h("div", { class: "chat", id: "chat" });
  const input = h("textarea", { id: "chat-input", placeholder: "Ej.: Publicá estos 10 videos en Bid Cap con el presupuesto guardado, en pausa…" });
  const send = h("button", { class: "btn primary", type: "button", id: "chat-send", text: "Enviar" });
  const add = (role, text, actions) => {
    log.append(h("div", { class: "msg " + role, text }));
    if (actions && actions.length) log.append(h("div", { class: "row" }, actions.map((a) => chip(`${a.ok ? "✓" : "✗"} ${a.tool.replace("orbita_", "")}`, a.ok ? "ok" : "bad"))));
    log.scrollTop = log.scrollHeight;
  };
  send.addEventListener("click", async () => {
    const text = input.value.trim();
    if (!text) return;
    input.value = "";
    add("user", text);
    send.disabled = true;
    send.textContent = "Pensando…";
    try {
      const r = await api("POST", "/v1/assistant/messages", { conversation_id: state.conversation || undefined, text });
      state.conversation = r.conversation_id;
      try { localStorage.setItem("orbita.conversation", r.conversation_id); } catch (e) { /* sin almacenamiento local */ }
      add("assistant", r.reply || "(sin texto)", r.actions);
      refreshJobs();
    } catch (e) {
      add("assistant", e.message);
      if (e.code === "AI_KEY_MISSING") switchTab("conexion");
    } finally {
      send.disabled = false;
      send.textContent = "Enviar";
    }
  });
  put(root, h("div", { class: "card" },
    h("div", { class: "row" }, h("h2", { text: "Asistente de Meta Ads" }),
      h("button", { class: "btn small", type: "button", text: "Nueva conversación", on: { click: () => { state.conversation = null; try { localStorage.removeItem("orbita.conversation"); } catch (e) { /* idem */ } renderAssistant(); } } })),
    h("p", { class: "hint", text: "Usa las mismas acciones y validaciones que esta pantalla. Si ya le pediste publicar con los datos definidos, lo hace sin pedirte confirmar cada paso." }),
    log, h("div", { class: "grid" }, input, h("div", { class: "row end" }, send))));
  if (state.conversation) {
    try {
      const r = await api("GET", `/v1/assistant/conversations/${state.conversation}`);
      r.messages.forEach((m) => add(m.role, m.text));
    } catch (e) { /* conversación inexistente */ }
  }
}

async function init() {
  document.querySelectorAll(".tabs button").forEach((b) => b.addEventListener("click", () => switchTab(b.dataset.tab)));
  try {
    await loadSettings();
    await loadProfile();
  } catch (e) {
    toast(e.message, true);
    return;
  }
  renderPublish();
  renderConnection();
  renderAssistant();
  await refreshJobs();
  if (!state.profile) switchTab("conexion");
}

document.addEventListener("DOMContentLoaded", init);
