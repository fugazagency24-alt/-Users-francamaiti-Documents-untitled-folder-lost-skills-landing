# Fuentes técnicas y decisiones

## Revisión del 23/10/2026 (integración)

Desde el entorno de trabajo, `developers.facebook.com` y `graph.facebook.com` estaban bloqueados por la política de red; las páginas oficiales se contrastaron mediante resultados de búsqueda que citan esa documentación. **No se hizo ninguna llamada autenticada a Meta.**

| Tema | Fuente |
|---|---|
| v26.0 vigente y cambios del 27/10/2026 | https://developers.facebook.com/docs/graph-api/changelog/version26.0/ · https://developers.facebook.com/documentation/ads-commerce/marketing-api/overview/versioning |
| `is_adset_budget_sharing_enabled` obligatorio sin presupuesto de campaña (desde v24) | https://developers.facebook.com/blog/post/2025/10/08/introducing-graph-api-v24-and-marketing-api-v24/ · https://developers.facebook.com/documentation/ads-commerce/marketing-api/bidding/guides/adset-budget-sharing |
| `targeting_automation.advantage_audience` explícito al crear conjuntos (desde v23) | https://developers.facebook.com/docs/marketing-api/audiences/reference/targeting-expansion/advantage-audience/ · https://developers.facebook.com/blog/post/2025/06/13/marketing-api-changes-to-advantage-plus-audience-behaviors/ |
| Advantage+ unificado (v25) y advantage_state | https://developers.facebook.com/docs/marketing-api/advantage-campaigns |
| `validate_only` | https://developers.facebook.com/documentation/ads-commerce/marketing-api/advantage-shopping-campaigns |
| `instagram_user_id`, `connected_instagram_accounts` | https://developers.facebook.com/documentation/ads-commerce/instagram/ads-api/guides/use-posts-as-ads · https://developers.facebook.com/blog/post/2025/01/21/making-it-easier-to-build-integrations-across-the-instagram-api-and-marketing-api/ |
| Video creative (`image_url`/`image_hash`, `link_description`, CTA) | https://developers.facebook.com/docs/marketing-api/reference/ad-creative-video-data |
| Niveles de acceso | Fuentes de terceros coinciden en acceso estándar para cuentas propias; confirmar en el panel de la app. |

## Revisión original (22/10/2026, ZIP)

| Tema | Fuente primaria |
|---|---|
| Versión Graph/Marketing API | https://developers.facebook.com/blog/post/2026/07/29/introducing-graph-api-v26-and-marketing-api-v26/ |
| Autorización | https://developers.facebook.com/documentation/ads-commerce/marketing-api/get-started/authorization |
| Creatividades | https://developers.facebook.com/documentation/ads-commerce/marketing-api/reference/ad-creative |
| Link data y caption | https://developers.facebook.com/docs/marketing-api/reference/ad-creative-link-data/ |
| CTA value y link_caption | https://developers.facebook.com/docs/marketing-api/reference/ad-creative-link-data-call-to-action-value/ |
| SDK oficial (campos) | https://github.com/facebook/facebook-python-business-sdk |

## Decisiones propias del módulo

Un negocio por instancia; máximo por lote; enlace visible del mismo dominio (www. opcional); solo adultos; imágenes JPG/PNG; fail-closed ante creación incierta; token administrado; borradores inmutables; `advantage_audience=0` por defecto para no cambiar la segmentación sin pedido. No son afirmaciones de que Meta exija exactamente esas restricciones.
