// Prueba de punta a punta de la pantalla en modo simulación.
// Uso: BASE=http://127.0.0.1:8799 SHOTS=/ruta node tests/e2e/ui.mjs  (requiere Playwright y el servidor corriendo con datos vacíos)
import { chromium } from "playwright";
import assert from "node:assert/strict";
import { writeFileSync } from "node:fs";

const BASE = process.env.BASE || "http://127.0.0.1:8799";
const SHOTS = process.env.SHOTS || ".";
const PNG = Buffer.from("89504e470d0a1a0a0000000d49484452000004380000043808060000000000000000", "hex");
const log = (...a) => console.log("✔", ...a);

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1360, height: 900 } });
page.on("dialog", (d) => d.accept());
const errors = [];
page.on("pageerror", (e) => errors.push(e.message));
page.on("console", (m) => m.type() === "error" && !/Failed to load resource/.test(m.text()) && errors.push(m.text()));

await page.goto(BASE + "/");
// Navegación: sección Ejecución → Meta Ads
const group = page.locator(".nav-group");
assert.equal(await group.locator(".nav-label").textContent(), "Ejecución");
assert.equal(await group.locator('a[data-nav="meta-ads"]').innerText(), "Meta Ads");
assert.equal(await page.locator("h1").innerText(), "Meta Ads");
log("Navegación Ejecución → Meta Ads");
assert.equal(await page.locator('[data-tab="conexion"]').getAttribute("aria-selected"), "true");
assert.match(await page.locator("#mode-badge").innerText(), /SIMULACIÓN/);
log("Sin configuración abre Conexión; modo SIMULACIÓN visible");

// Configuración una sola vez
const fill = async (sel, v) => page.fill(sel, v);
await fill("#pf-account_id", "act_123456");
await fill("#pf-page_id", "234567");
await fill("#pf-pixel_id", "345678");
await fill("#pf-countries", "AR, UY");
await fill("#pf-budget", "1.000");
await fill("#pf-max_batch", "20000");
await fill("#pf-bid", "500");
const conn = page.locator("#tab-conexion");
await conn.locator("textarea").first().fill("Conocé nuestro producto.");
await conn.locator('input[type="url"]').first().fill("https://tienda.example/producto");
await conn.locator('label.field:has-text("UTM predeterminado") input').fill("?utm_source={{site_source_name}}&utm_content=%7B%7Bad.id%7D%7D");
await page.screenshot({ path: `${SHOTS}/1-conexion.png`, fullPage: true });
await page.click("#save-profile");
await page.waitForSelector("#toast:has-text('Configuración guardada')");
const prof = await page.evaluate(() => fetch("/v1/profile").then((r) => r.json()));
assert.equal(prof.defaults.utm_template, "utm_source={{site_source_name}}&utm_content={{ad.id}}");
assert.equal(prof.daily_budget_minor, 100000);
log("Perfil guardado; UTM normalizado y macros literales");

// Verificación en simulación
await page.click("#btn-verify");
await page.waitForSelector("#verify-result:has-text('simulación')");
log("Comprobar en simulación lo dice explícitamente");

// Bid Cap 1:1:10
await page.click('[data-tab="publicar"]');
await page.fill("#batch-name", "E2E Bid Cap");
const links = Array.from({ length: 10 }, (_, i) => `https://cdn.example/ad-${i}.jpg`).join("\n");
await page.fill("#links", links.split("\n").slice(0, 9).join("\n"));
await page.click("text=Agregar enlaces");
assert.equal(await page.locator("#creative-count").innerText(), "9/10");
assert.equal(await page.locator("#btn-publish").isDisabled(), true);
log("Bid Cap bloquea con 9 creativos");
await page.fill("#links", "https://cdn.example/ad-9.jpg");
await page.click("text=Agregar enlaces");
assert.equal(await page.locator("#creative-count").innerText(), "10/10");
const total = await page.locator("[data-total]").getAttribute("data-total");
assert.equal(total, "100000");
assert.match(await page.locator("#summary").innerText(), /no limita el gasto de otras campañas/);
// Personalización individual
await page.locator('[data-creative="0"] >> text=Personalizar').click();
await page.locator('[data-creative="0"] .overrides input[type="text"]').first().fill("Título solo del anuncio 1");
await page.screenshot({ path: `${SHOTS}/2-publicar-bidcap.png`, fullPage: true });
// Doble clic: un solo borrador y un solo trabajo
await page.locator("#btn-publish").dblclick();
await page.waitForSelector("text=Ver en Campañas");
await page.click("text=Ver en Campañas");
await page.waitForSelector("#job-detail .chip:has-text('Simulado')", { timeout: 15000 });
let jobs = (await page.evaluate(() => fetch("/v1/jobs").then((r) => r.json()))).jobs;
assert.equal(jobs.length, 1);
assert.deepEqual([jobs[0].summary.campaigns, jobs[0].summary.adsets, jobs[0].summary.ads], [1, 1, 10]);
const draft = await page.evaluate((id) => fetch(`/v1/drafts/${id}`).then((r) => r.json()), jobs[0].draft_id);
const adset = draft.operations.find((o) => o.kind === "adset").body;
assert.equal(adset.bid_strategy, "LOWEST_COST_WITH_BID_CAP");
assert.equal(adset.bid_amount, 50000);
assert.deepEqual(adset.targeting.targeting_automation, { advantage_audience: 0 });
const creatives = draft.operations.filter((o) => o.kind === "creative").map((o) => o.body);
assert.equal(creatives[0].object_story_spec.link_data.name, "Título solo del anuncio 1");
assert.equal(creatives[0].url_tags, "utm_source={{site_source_name}}&utm_content={{ad.id}}");
assert.equal(creatives[0].object_story_spec.link_data.caption, "https://tienda.example");
log("Bid Cap 1:1:10 publicado (simulado) una sola vez pese al doble clic; puja, override, UTM y enlace visible OK");
await page.screenshot({ path: `${SHOTS}/3-campanas.png`, fullPage: true });

// Activar después y pausar
await page.click("#job-detail >> text=Activar");
await page.waitForFunction(() => document.querySelector("#toast")?.innerText.includes("Activación"));
await page.waitForTimeout(2500);
await page.click("#job-detail >> text=Pausar");
await page.waitForSelector("#job-detail .chip:has-text('Detenido')", { timeout: 15000 });
jobs = (await page.evaluate(() => fetch("/v1/jobs").then((r) => r.json()))).jobs;
assert.equal(jobs[0].state, "STOPPED_PAUSED");
const ev = (await page.evaluate((id) => fetch(`/v1/jobs/${id}`).then((r) => r.json()), jobs[0].id)).events.map((e) => e.kind);
assert.ok(ev.includes("activation_requested") && ev.includes("paused"));
log("Activar después sin duplicar y pausar: OK");
await page.click("#job-detail >> text=Estado en Meta");
await page.waitForSelector("#remote:has-text('Simulación')");
log("Estado remoto muestra que es simulación");

// ABO con archivo subido + 2 enlaces
await page.click('[data-tab="publicar"]');
await page.click('input[value="ABO_1_1_1"]');
await page.click("text=Quitar todos");
await page.fill("#batch-name", "E2E ABO");
await page.fill("#links", "https://cdn.example/a.jpg\nhttps://cdn.example/b.mp4");
await page.click("text=Agregar enlaces");
await page.setInputFiles('input[data-upload="media"]', { name: "foto.png", mimeType: "image/png", buffer: PNG });
await page.waitForSelector(".creative .chip:has-text('subido a Orbita')");
assert.equal(await page.locator("[data-total]").getAttribute("data-total"), "300000");
await page.screenshot({ path: `${SHOTS}/4-publicar-abo.png`, fullPage: true });
await page.click("#btn-publish");
await page.click("text=Ver en Campañas");
await page.waitForSelector("#job-detail .chip:has-text('Simulado')", { timeout: 15000 });
jobs = (await page.evaluate(() => fetch("/v1/jobs").then((r) => r.json()))).jobs;
assert.deepEqual([jobs[0].summary.campaigns, jobs[0].summary.ads, jobs[0].summary.total_daily_budget_minor], [3, 3, 300000]);
log("ABO 1:1:1 con 3 creativos (1 archivo subido, 1 video sin portada) → 3 campañas, total 3× presupuesto");

// Asistente sin API key
await page.click('[data-tab="asistente"]');
await page.fill("#chat-input", "¿Qué campañas tengo?");
await page.click("#chat-send");
await page.waitForSelector("#tab-conexion:not([hidden])");
log("Asistente sin API key lleva a Conexión");

assert.deepEqual(errors, []);
log("Sin errores de JavaScript");
writeFileSync(`${SHOTS}/e2e-ok.txt`, "ok\n");
await browser.close();
