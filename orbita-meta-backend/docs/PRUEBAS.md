# Verificación

## 23/10/2026 · v1.2 app local

| Prueba | Resultado |
|---|---|
| `python -m unittest discover` | **44 aprobadas** en Python 3.10, 3.11 y 3.13 (y con `anthropic` 2.1 instalado). |
| Navegador real (Playwright + Chromium, `tests/e2e/ui.mjs`) | **11/11** pasos, sin errores de JavaScript. |
| Iniciador desde cero (`iniciar.command`, HOME vacío) | Crea entorno, instala `anthropic`, arranca y sirve la pantalla. Datos en `~/.orbita-meta-ads` con permisos 0600/0700. |

Recorrido del navegador: navegación **Ejecución → Meta Ads**; sin configuración abre Conexión; modo SIMULACIÓN visible; perfil guardado con «1.000» = mil y UTM normalizado con macros literales; Bid Cap bloquea con 9 creativos; Bid Cap 1:1:10 con override individual publicado **una sola vez pese a doble clic** (puja máxima, `advantage_audience`, UTM y enlace visible verificados en el borrador); activar después sin duplicar y pausar; estado remoto rotulado como simulación; ABO 1:1:1 con enlace de imagen, enlace de video sin portada y archivo subido → 3 campañas y 3× presupuesto; asistente sin API key lleva a Conexión.

Pruebas nuevas de la app local: claves que nunca salen del servidor y archivo 0600; cambio de modo persistido y bloqueos de publicación real (deshabilitada / sin token); archivos subidos usados como imagen, video y portada; rechazo de HTML disfrazado de video; subida de medio incierta reintentable sin bloquear; sesión de pantalla con cookie, Host y Origin (CSRF y DNS rebinding); asistente con cliente simulado que ejecuta herramientas, conserva el historial sin reescribirlo y respeta permisos del backend.

### Hallazgos corregidos por las pruebas de navegador

- «1.000» se interpretaba como 1 en vez de mil.
- El resumen mostraba texto de objetos y «null» por un helper de render.

## 23/10/2026 · v1.1 auditoría del ZIP

36 pruebas: ver `CAMBIOS.md` (advantage_audience, pausa, idempotencia de borradores, errores legibles, enlace visible, UTM, portada de video, enlaces que no son archivos, verificación guiada, fases remotas, permisos de IA).

## No verificado

- **Nada contra Meta real**: la red de este entorno bloquea `graph.facebook.com` y no hay token. La subida por partes de videos locales (`graph-video.facebook.com`, start/transfer/finish) sigue el protocolo documentado, sin prueba real.
- **Asistente contra la API real de Anthropic**: probado con un cliente simulado; falta tu API key.
- **Integración dentro del repositorio de Orbita**: no estuvo disponible. Esta app local es independiente.

## Aceptación pendiente con tu cuenta

Conexión → token → Comprobar (lectura y publicación validadas) → elegir activos → ensayo real **en pausa** → revisar en Ads Manager objetivo, puja, presupuesto, identidad, medios, copy, CTA, destino, `url_tags` y enlace visible → activar solo con instrucción de gasto.
