# Cambios

## v1.2 · app local

| Qué | Detalle |
|---|---|
| Pantalla Ejecución → Meta Ads | Servida por el mismo proceso en `127.0.0.1`. Pestañas Publicar, Campañas, Conexión y Asistente IA. Sesión por cookie HttpOnly SameSite=Strict, control de Host (anti DNS rebinding) y de Origin (anti CSRF), CSP estricta. |
| Claves en el servidor | Token de Meta, app secret y API key de Anthropic se cargan en un campo seguro, se guardan en `~/.orbita-meta-ads/secrets.json` (0600) y nunca vuelven al navegador. |
| Modo desde la pantalla | Simulación / real y habilitar publicación real, persistidos. Sin token no se publica en real. |
| Subida de archivos | JPG/PNG (hasta 30 MB) y MP4/MOV (hasta 4 GB), identificados por contenido. Imágenes se suben por bytes; videos por subida por partes a la cuenta. |
| Medios reintentables | Una subida de medio sin confirmar ya no bloquea el trabajo: reintentar solo puede dejar una copia en la biblioteca, nunca campañas duplicadas. |
| Asistente IA | Claude (`claude-opus-5-5`) con loop de herramientas propio: las mismas funciones del servicio y permisos aplicados en el backend (`ORBITA_AI_PERMISSIONS`). Conversación guardada sin reescribir. |
| Montos en formato argentino | «1.000» = mil, «1.000,50», «1000,5» y «1000.5» se interpretan bien. |
| Iniciador | `iniciar.command`: busca Python 3.10+, ofrece instalarlo si falta, crea el entorno y abre el navegador. |

## v1.1 · auditoría del ZIP

| # | Problema en el ZIP | Corrección |
|---|---|---|
| 1 | No enviaba `targeting_automation.advantage_audience`; Meta lo exige al crear conjuntos desde v23 → la publicación real habría fallado. | Se envía siempre (0 por defecto). Opción de perfil con los límites de edad de Meta. |
| 2 | Carrera: pausar un trabajo justo cuando el worker lo tomaba dejaba que igual se creara todo. | `run()` revisa el estado bajo el lock. |
| 3 | Un trabajo pausado a mitad de la creación quedaba sin salida (ni retry ni activate). | `/retry` reanuda STOPPED_PAUSED. |
| 4 | Reanudar un borrador ACTIVE después de una pausa manual lo habría activado solo. | La pausa retiene la activación hasta `/activate`. |
| 5 | Doble clic o recarga en “Publicar” podía crear dos borradores → dos estructuras. | `Idempotency-Key` también en borradores. |
| 6 | Errores de Meta solo con códigos; imposible saber por qué falló una pausa o creación. | Se agrega el texto para usuario de Meta, saneado. |
| 7 | AUTO y “sin personalización” enviaban exactamente lo mismo. | AUTO = dominio limpio del destino; OMIT = nada (decide Meta); CUSTOM admite www. y falta de `https://`. |
| 8 | UTM pegado con `?` o macros codificadas daba error. | Se normaliza; el error de duplicados nombra la clave. |
| 9 | Video exigía siempre portada propia. | Si falta, se usa la miniatura que genera Meta. |
| 10 | Enlaces de Drive/Dropbox/WeTransfer/YouTube solo fallaban como “dominio no autorizado”. | Mensaje específico; `/v1/assets/check` valida formato y medidas antes de publicar. Videos se verifican (no HTML) antes de subirlos. |
| 11 | Sin descubrimiento de activos ni prueba de escritura. | `/v1/setup/assets` y `/v1/setup/verify` (`validate_only`, sin crear nada). |
| 12 | `/remote` devolvía estados crudos. | Fases legibles, motivo de rechazo, `delivering` por impresiones. |
| 13 | Sin listados; la IA no podía ver publicaciones previas ni defaults. | `/v1/jobs`, `/v1/drafts`, herramientas `orbita_get_settings`, `orbita_list_campaign_jobs`, `orbita_check_asset`, `orbita_save_ad_defaults`. |
| 14 | Herramientas de IA sin autorización propia. | `execute_tool(..., permissions=…)` exige permisos de Orbita por herramienta; publicar ACTIVE exige también `activate`. |
| 15 | Allowlist de hosts obligatoria por host. | `ASSET_ALLOWED_HOSTS=*` opcional (sigue la protección por IP pública). |
