# API de integración

Base local: `http://127.0.0.1:8787`. Dos formas de autenticarse: `Authorization: Bearer ORBITA_SERVICE_KEY` desde un backend (con Origin se rechaza), o la sesión de la pantalla local (cookie + Host local + Origin propio en cambios). JSON de hasta 256 KiB, sin campos desconocidos. Contrato: `integration/openapi.json`; esquemas `*.schema.json`. Las reglas entre campos se implementan en `validation.py`.

| Método / ruta | Función |
|---|---|
| GET /health | Salud del proceso y modo; no verifica Meta. |
| GET / | Pantalla local (solo Host 127.0.0.1/localhost). Entrega la cookie de sesión de la pantalla. |
| GET /v1/settings · PUT /v1/settings/runtime | Modo (`mock`/`live`), publicación real habilitada y estado de claves (solo si están cargadas). |
| PUT /v1/secrets/{meta_access_token\|meta_app_secret\|anthropic_api_key} · DELETE | Guardar o borrar una clave en el servidor. La respuesta nunca la incluye. |
| POST /v1/uploads | Cuerpo binario + `X-File-Name`. Devuelve `id` para usar como `upload_id` / `thumbnail_upload_id`. |
| GET /v1/uploads/{id}[/file] | Metadatos o el archivo (para la vista de la pantalla). |
| POST /v1/assistant/messages | `{conversation_id?, text}` → respuesta del asistente y acciones ejecutadas. |
| GET /v1/assistant/conversations/{id} | Mensajes visibles de una conversación. |
| GET /v1/profile | Configuración guardada, sin secretos. |
| PUT /v1/profile | Reemplazar perfil completo. Solo configuración administrativa. |
| PUT /v1/profile/defaults | Guardar solo defaults de anuncio (copy, CTA, destino, enlace visible, UTM). No toca cuenta, presupuesto ni puja. |
| GET /v1/connection | Verificar lectura de cuenta/página/píxel/Instagram configurados y moneda. |
| POST /v1/setup/verify | Comprobación guiada: token, permisos, cuenta, página, píxel, Instagram con nombres; escritura con `validate_only` (no crea nada). |
| GET /v1/setup/assets?account_id=act_… | Descubrir cuentas, páginas, píxeles e Instagram visibles para el token. Cada sección informa su error de permisos. |
| POST /v1/assets/check | `{url, kind}`: confirma que el enlace es el archivo directo (formato, medidas) y no una carpeta o página. |
| GET /v1/jobs?limit=N | Publicaciones recientes con estado y resumen. |
| GET /v1/drafts?limit=N | Borradores recientes con su trabajo, si existe. |
| POST /v1/preview | Planificar sin persistencia ni llamadas Meta. |
| POST /v1/drafts | Guardar borrador y devolver draft_id, plan_hash, summary, operations, warnings. Header opcional `Idempotency-Key`: misma clave + mismo contenido = mismo borrador. |
| POST /v1/drafts/from-link | Atajo para URL de archivo o manifiesto. |
| GET /v1/drafts/{draft_id} | Recuperar el borrador congelado. |
| POST /v1/drafts/{draft_id}/publish | Encolar; body plan_hash y header Idempotency-Key. |
| GET /v1/jobs/{job_id} | Estado, pasos, resultados, último error y últimos 100 eventos. |
| POST /v1/jobs/{job_id}/activate | Activar estructura ya completa; body plan_hash. |
| POST /v1/jobs/{job_id}/pause | Pausar padres del trabajo; body vacío o `{}`. |
| POST /v1/jobs/{job_id}/retry | Reencolar FAILED/NEEDS_RECONCILIATION ya resuelto, o reanudar STOPPED_PAUSED; body `{}`. Reanudar no activa: para eso, /activate. |
| POST /v1/jobs/{job_id}/resolve | Resolver un paso UNCERTAIN; solo administrador. |
| GET /v1/jobs/{job_id}/remote | status/effective_status/issues por objeto, fase legible (EN_REVISION, RECHAZADO, ACTIVO, PAUSADO…) y `delivering` solo si Meta informa impresiones. |
| GET /v1/jobs/{job_id}/previews?format=… | Previews por formato (DESKTOP_FEED_STANDARD, MOBILE_FEED_STANDARD, INSTAGRAM_STANDARD, INSTAGRAM_STORY, INSTAGRAM_REELS, FACEBOOK_REELS_MOBILE). |
| GET /v1/jobs/{job_id}/insights | Métricas de hoy a nivel campaña: impressions, clicks, spend, actions. |

El cliente debe guardar los IDs. Un trabajo repetido devuelve el mismo job. La misma Idempotency-Key con otro borrador devuelve conflicto. Un borrador solo puede producir un trabajo, incluso si cambia la clave. No hay endpoint público de búsqueda global/listado: Orbita mantiene su lista de trabajos y controla su acceso.

## Perfil

Ver `examples/profile.json`. `account_id` usa prefijo `act_`; los otros IDs son strings numéricos. `pixel_id` es obligatorio para SALES. `instagram_user_id` es opcional y debe corresponder a una identidad publicitaria accesible. Las monedas admitidas en esta implementación son ARS, USD, EUR y BRL.

Todo importe es entero en unidades menores: **100000 ARS = $1.000 ARS; 1500 USD = US$15**. La moneda proviene de la cuenta, no de la ubicación del usuario. No se convierten monedas. `daily_budget_minor` es por adset; `max_batch_daily_budget_minor` limita la suma del lote; `bid_cap_minor` es la puja máxima de Bid Cap, no un CPA garantizado.

`defaults.primary_text` y `defaults.destination_url` son obligatorios. Título y descripción pueden ser vacíos. CTA por defecto LEARN_MORE. No hay auto-copy.

Enlace visible (`display_url_mode`): `AUTO` envía el dominio limpio del destino (`https://dominio`); `CUSTOM` envía `display_url`, que debe ser del mismo dominio (www. opcional; si se pega sin `https://` se agrega); `OMIT_CUSTOM` no envía nada y Meta usa su valor por defecto. Imagen: `link_data.caption`. Video: `call_to_action.value.link_caption`. Meta no usa ese campo en Instagram y decide la presentación final.

UTM: se aceptan `?` inicial, una URL completa (se toma su query) y macros codificadas `%7B%7B…%7D%7D`; se guardan normalizadas y literales. Si la URL de destino ya trae una clave del UTM, el error nombra la clave a quitar.

`advantage_audience` (opcional, default `false`): se envía siempre `targeting.targeting_automation.advantage_audience` porque Meta lo exige al crear conjuntos. `true` requiere age_min 18–25 y age_max 65.

## Crear un borrador desde enlaces

```json
{
  "name": "Lanzamiento octubre",
  "structure": "ABO_1_1_1",
  "target_status": "PAUSED",
  "shared": {
    "primary_text": "Conocé nuestra propuesta.",
    "headline": "Más información",
    "cta": "LEARN_MORE",
    "destination_url": "https://tienda.example/producto"
  },
  "media": [
    {"kind": "image", "url": "https://cdn.example/anuncio.jpg"},
    {
      "kind": "video",
      "url": "https://cdn.example/video.mp4",
      "thumbnail_url": "https://cdn.example/portada.jpg",
      "overrides": {"primary_text": "Un copy diferente para este video."}
    }
  ]
}
```

Genera dos campañas. Para Bid Cap usar diez elementos exactamente y estructura BID_CAP_1_1_10. Los hashes de imágenes y video_id ya existentes pueden reemplazar `url`, no coexistir con ella. Meta valida su acceso/compatibilidad.

## Encolar y activar

```http
POST /v1/drafts/DRAFT_ID/publish
Authorization: Bearer SERVICE_KEY
Content-Type: application/json
Idempotency-Key: orbita-DRAFT_ID

{"plan_hash":"HASH_DEVUELTO_POR_EL_BORRADOR"}
```

Devuelve HTTP 202 con `id`, `state`, `mode`, `steps` y `events`. Consultar `/v1/jobs/ID` cada 2–5 segundos mientras QUEUED/RUNNING. Si una llamada de publicación pierde su respuesta, repetir sobre el mismo draft_id/hash/clave. Si se creó pausado y luego se autoriza activar:

```http
POST /v1/jobs/JOB_ID/activate
Authorization: Bearer SERVICE_KEY
Content-Type: application/json

{"plan_hash":"HASH_DEL_BORRADOR_ORIGINAL"}
```

Consultar `/remote` después para distinguir activación solicitada, revisión, rechazo, pausa y entrega. Los estados remotos se devuelven tal como los informa Meta. Métricas son para hoy según la cuenta, no según el navegador; `spend` es el importe reportado por Meta, no unidades menores del presupuesto.

## Pegar un solo link

```json
{"source_url":"https://cdn.example/anuncio.jpg","source_type":"image","name":"Mi anuncio","target_status":"PAUSED"}
```

O, para un lote, `{"source_url":"https://cdn.example/lote.json","source_type":"manifest"}`. El JSON remoto debe contener el mismo cuerpo de `/v1/drafts`. No puede aportar credenciales, cambiar perfil ni aumentar su límite de presupuesto. No se ejecuta código remoto. Su contenido se congela al preparar el borrador.

## Errores

Forma: `{"error":{"code":"...","message":"..."}}`. Para errores de Meta se conservan código, subcódigo y trace ID, sin mensaje completo del proveedor que pueda repetir datos sensibles. Detalles operativos aparecen en el job. Código HTTP 400 = entrada inválida; 401/403 = autorización/origen; 409 = estado incompatible; 422 = medio no disponible/procesable; 502 = error de Meta. HTTP 202 no significa publicado.

## Reconciliación administrativa

`{"step_key":"campaign0","resolution":"ATTACH","remote_id":"123...","evidence":"Verificado en Meta: cuenta, nombre y marcador coinciden"}` adopta el ID tras controles remotos. `{"step_key":"campaign0","resolution":"NOT_CREATED","evidence":"Verificación realizada y evidencia de ausencia"}` permite reenviar el paso. Este último depende de una revisión real: el backend no puede demostrar automáticamente la ausencia de un objeto cuyo POST perdió respuesta. Nunca exponer resolve como herramienta autónoma del modelo.

Los previews contienen HTML externo; aislarlos en iframe con política restrictiva. No insertar mediante HTML sin sanitización en el origen principal de Orbita.
