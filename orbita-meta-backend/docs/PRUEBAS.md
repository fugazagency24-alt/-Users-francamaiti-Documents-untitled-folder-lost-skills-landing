# Verificación

## 23/10/2026 · integración v1.1 (Python 3.13)

`python -m unittest discover -v`: **36 pruebas aprobadas** (19 originales, una ajustada porque `?a=b` ahora se normaliza; 17 nuevas).

Nuevas coberturas: `advantage_audience` explícito y sus límites de edad; UTM pegado con `?`, URL completa o macros codificadas; error que nombra el parámetro repetido; enlace visible AUTO/CUSTOM/OMIT para imagen y video; video sin portada usando la miniatura de Meta; pausa entre `claim` y ejecución sin crear nada; pausa manual que retiene la activación hasta `/activate`; errores de Meta legibles sin tokens ni querystrings; enlaces de carpeta/página rechazados; detección HTML vs. MP4 y medidas de PNG; UTM predeterminado reutilizado con override explícito; fases remotas y listados; verificación guiada en modo live sin crear objetos (solo `validate_only`); moneda distinta informada; permisos de herramientas de IA aplicados en backend; idempotencia de borrador ante doble clic; rutas HTTP nuevas.

`python examples/run_mock_demo.py`: Bid Cap 1:1:10 (32 pasos), ABO ×3 (15), ABO video (7): SIMULATED.

Servicio real (`python -m orbita_ads`, modo mock) por HTTP: perfil → borrador Bid Cap → publicar dos veces con la misma clave → mismo trabajo → worker → SIMULATED → `/remote` con 10 anuncios PAUSADO.

Migración: una base creada con la versión del ZIP abre con la v1.1, lista y pausa sus trabajos.

## No verificado

- **Nada contra Meta real**: la red del entorno bloquea `graph.facebook.com` y no hay token configurado.
- **Integración en Orbita**: el código de Orbita no estuvo disponible.
- Adaptador TypeScript sin compilar (no hay proyecto TS donde montarlo todavía). Docker no ejecutado.

## Aceptación pendiente con tu cuenta

`/v1/setup/verify` con `read_verified` y `write_validated` en true → ensayo real PAUSED → revisar objetos, CTA, destino, `url_tags`, enlace visible y previews en Meta → activar solo con instrucción de gasto.
