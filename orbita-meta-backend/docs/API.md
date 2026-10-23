# API de integración

Base local: `http://127.0.0.1:8787`. Todas las rutas salvo `/health` requieren `Authorization: Bearer ORBITA_SERVICE_KEY`. Llamar desde backend, no desde navegador: se rechazan solicitudes con Origin. JSON de hasta 256 KiB, sin campos desconocidos. Contrato: `integration/openapi.json`; esquemas `*.schema.json`. Las reglas entre campos se implementan en `validation.py`.

| Método / ruta | Función |
|---|---|
| GET /health | Salud del proceso y modo; no verifica Meta. |
| GET /v1/profile | Configuración guardada, sin secretos. |
| PUT /v1/profile | Reemplazar perfil completo. Solo configuración administrativa. |
| GET /v1/connection | Verificar lectura de cuenta/página/píxel/Instagram configurados y moneda. |
| POST /v1/preview | Planificar sin persistencia ni llamadas Meta. |
| POST /v1/drafts | Guardar borrador y devolver draft_id, plan_hash, summary, operations, warnings. |
| POST /v1/drafts/from-link | Atajo para URL de archivo o manifiesto. |
| GET /v1/drafts/{draft_id} | Recuperar el borrador congelado. |
| POST /v1/drafts/{draft_id}/publish | Encolar; body plan_hash y header Idempotency-Key. |
| GET /v1/jobs/{job_id} | Estado, pasos, resultados, último error y últimos 100 eventos. |
| POST /v1/jobs/{job_id}/activate | Activar estructura ya completa; body plan_hash. |
| POST /v1/jobs/{job_id}/pause | Pausar padres del trabajo; body vacío o `{}`. |
| POST /v1/jobs/{job_id}/retry | Reencolar FAILED/NEEDS_RECONCILIATION ya resuelto; body `{}`. |
| POST /v1/jobs/{job_id}/resolve | Resolver un paso UNCERTAIN; solo administrador. |
| GET /v1/jobs/{job_id}/remote | status/effective_status actuales, por objeto conocido. |
| GET /v1/jobs/{job_id}/previews | Previews DESKTOP_FEED_STANDARD de los anuncios creados. No garantiza todas las ubicaciones. |
| GET /v1/jobs/{job_id}/insights | Métricas de hoy a nivel campaña: impressions, clicks, spend, actions. |

El cliente debe guardar los IDs. Un trabajo repetido devuelve el mismo job. La misma Idempotency-Key con otro borrador devuelve conflicto. Un borrador solo puede producir un trabajo, incluso si cambia la clave. No hay endpoint público de búsqueda global/listado: Orbita mantiene su lista de trabajos y controla su acceso.

## Perfil

Ver `examples/profile.json`. `account_id` usa prefijo `act_`; los otros IDs son strings numéricos. `pixel_id` es obligatorio para SALES. `instagram_user_id` es opcional y debe corresponder a una identidad publicitaria accesible. Las monedas admitidas en esta implementación son ARS, USD, EUR y BRL.

Todo importe es entero en unidades menores: **100000 ARS = $1.000 ARS; 1500 USD = US$15**. La moneda proviene de la cuenta, no de la ubicación del usuario. No se convierten monedas. `daily_budget_minor` es por adset; `max_batch_daily_budget_minor` limita la suma del lote; `bid_cap_minor` es la puja máxima de Bid Cap, no un CPA garantizado.

`defaults.primary_text` y `defaults.destination_url` son obligatorios. Título y descripción pueden ser vacíos. CTA por defecto LEARN_MORE. No hay auto-copy. Para borrar un enlace visible heredado usar `display_url_mode: "AUTO"` o `"OMIT_CUSTOM"` junto con `display_url: ""`.

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
