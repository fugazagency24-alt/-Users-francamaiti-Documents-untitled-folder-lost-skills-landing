# Workflow implementado

## Preparación

`PUT /v1/profile` valida y persiste la configuración del único negocio. `POST /v1/drafts` combina perfil → shared → overrides de cada creativo. El borrador contiene una instantánea inmutable y SHA-256 de su plan. Cambiar el perfil no altera borradores existentes.

`POST /v1/preview` hace la misma planificación sin guardar ni contactar Meta. No equivale a `validate_only` remoto ni valida permisos reales. `POST /v1/drafts/from-link` acepta una imagen/video directo o descarga un manifiesto HTTPS de hasta 256 KiB, sujeto a la allowlist.

## Publicación

La API registra un trabajo único por borrador y una clave idempotente. SQLite reclama un trabajo con `BEGIN IMMEDIATE`. Un bloqueo de proceso evita que dos instancias trabajen con la misma base. No desplegar varios workers sobre este SQLite ni sobre filesystem de red.

El worker verifica modo, conexión, moneda y acceso de lectura a los activos. Prepara todos los medios antes de crear campañas. Las imágenes JPG/PNG se descargan con IP pública fijada al socket TLS, límite de 10 MiB y sin redirects; se suben en `bytes` base64 a `/adimages`. Meta descarga videos desde `file_url` en `/advideos`; se espera `status.video_status=ready`. La portada se sube como imagen.

Luego crea campañas, conjuntos, creatividades y anuncios. Cada operación registra IN_FLIGHT antes de enviar el POST y DONE con el ID/hash después. Los nombres remotos incluyen un marcador `[orbita:JOB:STEP]` para reconciliación. No se registra el token ni el contenido binario.

Todos los objetos publicitarios se crean PAUSED. Si se autorizó ACTIVE, se activan primero anuncios, después conjuntos, al final campañas. Una falla intenta pausar todas las campañas padre conocidas; se informa si alguna pausa quedó sin confirmar. Esto no es una transacción atómica remota: si hubo activación parcial puede haber gasto antes de la pausa.

## Reintentos y reinicios

Los GET transitorios tienen hasta tres intentos. Los POST de creación no se repiten automáticamente después de un timeout o error ambiguo. El paso pasa a UNCERTAIN y bloquea el trabajo. Una caída del proceso convierte IN_FLIGHT en UNCERTAIN al iniciar. Los trabajos interrumpidos se marcan para pausa de padres conocidos.

Un error de rechazo conocido deja FAILED y permite `/retry`, conservando los IDs de pasos DONE. Un video que sigue procesándose también permite reintento sin otra subida. Los cambios de status pueden repetirse de forma idempotente; la activación repite todos los status necesarios al reintentar.

No se promete exactly-once frente a Meta: si un POST creó algo y su respuesta se perdió, hace falta reconciliar. `/resolve` es solo administrativo: ATTACH comprueba ID, cuenta, marcador y padre para campañas/adsets/creativos/anuncios; NOT_CREATED registra la evidencia de ausencia comprobada por el administrador. No usar este último solo porque venció un timeout. Para una imagen/video cuya subida quedó incierta no hay auto-adopción: comprobarla administrativamente; un medio ya creado puede reutilizarse en un nuevo borrador por image_hash/video_id después de controlar los objetos anteriores. No se elimina nada automáticamente.

## Estados

| Estado | Significado |
|---|---|
| QUEUED / RUNNING | En cola / ejecutando. |
| SIMULATED | Resultado local mock; nada se publicó en Meta. |
| CREATED_PAUSED | Objetos creados pausados. |
| ACTIVATION_REQUESTED | Meta aceptó las solicitudes de activación; consultar effective_status. |
| FAILED | Error conocido; se puede corregir causa externa y reintentar. |
| NEEDS_RECONCILIATION | Creación incierta, interrupción o pausa compensatoria no confirmada. |
| STOPPED_PAUSED | Se frenó el trabajo o se pausaron los padres conocidos. Si faltan objetos no se puede activar. |
| PAUSE_INCOMPLETE | Alguna pausa no fue confirmada; consultar Meta y volver a pausar. |

Una pausa durante otra operación queda encolada y se procesa al terminar la llamada en curso; no es instantánea. Para activar una estructura pausada, `/activate` exige el hash del plan y que todos sus pasos hayan terminado. No crea otra estructura.

## Personalización y límites de campaña

Copy, titular, descripción y CTA se envían a los campos correspondientes de `object_story_spec`. El destino vive en `link_data.link` o `video_data.call_to_action.value.link`. `url_tags` conserva el UTM. Los parámetros repetidos entre destino y UTM se rechazan.

Solo presupuesto diario por adset, ventas PURCHASE o tráfico LINK_CLICKS. Países, rango adulto y placements automáticos de Meta; no se fijan ubicaciones en targeting. Algunos objetivos, CTA, formatos, países o cuentas pueden requerir campos adicionales: el rechazo de Meta se expone como error, no se cambia la configuración silenciosamente.

`max_batch_daily_budget_minor` limita la suma de presupuestos configurados en este lote. No consulta ni limita otros lotes/campañas existentes. No es un account spending limit, un spend_cap de campaña ni un máximo de pérdida. No hay reglas de escalado ni apagado por rendimiento.
