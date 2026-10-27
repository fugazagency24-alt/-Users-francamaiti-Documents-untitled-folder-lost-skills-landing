# Modo Toro

App personal de calistenia. PWA offline, sin backend.

## Publicar en Cloudflare Pages
1. Cloudflare → Workers & Pages → Create → Pages → Connect to Git.
2. Elegí este repo y la rama.
3. Build command: (vacío) · Output directory: `calistenia-app`.
4. Deploy. Abrí la URL en el celu → Compartir → "Agregar a inicio".

## Fotos y videos
1. Copiá los archivos a `media/` con el id del ejercicio (`dominadas.mp4`, `flex.jpg`). Tu foto de inicio: `yo.jpg`.
2. `node tools/media-index.mjs`
3. Subí `CACHE` en `sw.js` (toro-v2…) y pusheá.

IDs: ver `prompts/RUTINA.md`. Rutina: `data.js`. Tema: tokens en `styles.css` (`:root`).
