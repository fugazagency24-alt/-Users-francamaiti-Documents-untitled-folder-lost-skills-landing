// Genera prompts/RUTINA.md (versión legible) a partir de data.js.
// Uso: node tools/rutina-md.mjs
import { readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const src = readFileSync(join(root, "data.js"), "utf8");
const D = new Function(`${src}; return { FASES, EJ, CALENTAMIENTO, SESIONES, HOMBRO, FREEFLOW, SEMANA, REGLAS };`)();
const DIAS = ["Dom", "Lun", "Mar", "Mié", "Jue", "Vie", "Sáb"];
const p = (x) => (Array.isArray(x) ? x.join(" → ") : x);
const items = (arr) => arr.map((it) => `- **${D.EJ[it.e].n}** — ${p(it.p)}${it.nota ? ` _(${it.nota})_` : ""}`).join("\n");

let md = `# Rutina Modo Toro\n\n> Generado desde \`calistenia-app/data.js\`. Prescripciones: Fase 1 → 2 → 3 → 4 (4 semanas c/u; semana 4, 8, 12, 16 = descarga).\n\n`;
md += `## Fases\n\n${D.FASES.map((f) => `${f.n}. **${f.nombre}** — ${f.meta}`).join("\n")}\n\n`;
md += `## Semana\n\n${[1, 2, 3, 4, 5, 6, 0].map((d) => `- ${DIAS[d]}: ${D.SESIONES[D.SEMANA[d]].nombre}`).join("\n")}\n\n`;
md += `## Reglas\n\n${D.REGLAS.map((r) => `- ${r}`).join("\n")}\n\n`;
md += `## Calentamiento\n\n### Con plaza\n${items(D.CALENTAMIENTO.plaza)}\n\n### Sin plaza\n${items(D.CALENTAMIENTO.casa)}\n\n`;
for (const [k, s] of Object.entries(D.SESIONES)) {
  md += `## ${k} · ${s.nombre} (${s.min}')\n\n_${s.foco}_${s.nota ? ` — ${s.nota}` : ""}\n\n`;
  for (const ctx of ["plaza", "casa"]) {
    md += `### ${ctx === "plaza" ? "Con plaza" : "Sin plaza"}\n\n`;
    for (const b of s[ctx]) md += `**${b.t}** · ${p(b.f)}\n${items(b.items)}\n\n`;
    if (s.hombro) md += `**+ Rutina de hombro completa**\n\n`;
  }
}
md += `## Hombro (${D.HOMBRO.min}') · D = débil, F = fuerte\n\n${items(D.HOMBRO.items)}\n\n${D.HOMBRO.reglas.map((r) => `- ${r}`).join("\n")}\n\n`;
md += `## Free flow\n\n${Object.entries(D.FREEFLOW.formatos).map(([m, f]) => `- **${m}'** → ${f.t}: ${f.f}`).join("\n")}\n\nFocos: ${Object.values(D.FREEFLOW.focos).map((f) => f.nombre).join(", ")}.\n\n`;
md += `## IDs para fotos/videos (media/<id>.jpg|mp4)\n\n- \`yo\` — imagen de inicio (nueva identidad)\n${Object.entries(D.EJ).map(([id, e]) => `- \`${id}\` — ${e.n}`).join("\n")}\n`;
writeFileSync(join(root, "..", "prompts", "RUTINA.md"), md);
console.log("prompts/RUTINA.md listo");
