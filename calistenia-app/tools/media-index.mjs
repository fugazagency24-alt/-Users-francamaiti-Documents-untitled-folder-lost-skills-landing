// Genera media/index.json a partir de los archivos en media/.
// Nombre del archivo = id del ejercicio (ver data.js). "yo.jpg" = imagen de inicio.
// Uso: node tools/media-index.mjs
import { readdirSync, writeFileSync } from "node:fs";
import { dirname, join, parse } from "node:path";
import { fileURLToPath } from "node:url";

const dir = join(dirname(fileURLToPath(import.meta.url)), "..", "media");
const ok = /\.(jpe?g|png|webp|gif|avif|mp4|webm|mov|m4v)$/i;
const index = {};
for (const f of readdirSync(dir).sort()) {
  if (!ok.test(f)) continue;
  const id = parse(f).name;
  // Si hay video y foto con el mismo id, gana el video.
  if (!index[id] || /\.(mp4|webm|mov|m4v)$/i.test(f)) index[id] = f;
}
writeFileSync(join(dir, "index.json"), JSON.stringify(index, null, 2) + "\n");
console.log(`media/index.json: ${Object.keys(index).length} archivos`);
