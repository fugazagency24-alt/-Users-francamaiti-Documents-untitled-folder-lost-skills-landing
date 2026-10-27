// Offline: precache del shell + media listada en media/index.json. Subí CACHE al cambiar archivos.
const CACHE = "toro-v1";
const MEDIA_CACHE = "toro-media";
const SHELL = [
  "./",
  "index.html",
  "styles.css",
  "app.js",
  "data.js",
  "manifest.webmanifest",
  "icons/icon.svg",
  "icons/icon-192.png",
  "icons/icon-512.png",
  "icons/apple-touch-icon.png",
  "media/index.json",
];

self.addEventListener("install", (e) => {
  e.waitUntil((async () => {
    const c = await caches.open(CACHE);
    await c.addAll(SHELL);
    // Media: best effort, no frena la instalación.
    try {
      const idx = await (await fetch("media/index.json", { cache: "no-store" })).json();
      const m = await caches.open(MEDIA_CACHE);
      await Promise.allSettled(Object.values(idx).map((f) => m.add("media/" + encodeURIComponent(f))));
    } catch {}
    self.skipWaiting();
  })());
});

self.addEventListener("activate", (e) => {
  e.waitUntil((async () => {
    const keys = await caches.keys();
    await Promise.all(keys.filter((k) => k !== CACHE && k !== MEDIA_CACHE).map((k) => caches.delete(k)));
    await self.clients.claim();
  })());
});

self.addEventListener("fetch", (e) => {
  const req = e.request;
  if (req.method !== "GET" || new URL(req.url).origin !== location.origin) return;
  const isMedia = new URL(req.url).pathname.includes("/media/") && !req.url.endsWith("index.json");

  e.respondWith((async () => {
    // Videos piden Range: servimos desde cache completo y el browser se arregla.
    const hit = await caches.match(req, { ignoreSearch: true });
    if (hit) {
      // Shell: refrescamos en segundo plano para la próxima apertura.
      if (!isMedia) e.waitUntil(fetch(req).then((r) => r.ok && caches.open(CACHE).then((c) => c.put(req, r))).catch(() => {}));
      return hit;
    }
    try {
      const res = await fetch(req);
      if (res.ok && res.status === 200) {
        const c = await caches.open(isMedia ? MEDIA_CACHE : CACHE);
        c.put(req, res.clone());
      }
      return res;
    } catch {
      if (req.mode === "navigate") return caches.match("index.html");
      return new Response("", { status: 504 });
    }
  })());
});
