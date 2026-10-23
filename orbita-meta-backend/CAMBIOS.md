# Cambios sobre el ZIP (v1.0 → v1.1)

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
