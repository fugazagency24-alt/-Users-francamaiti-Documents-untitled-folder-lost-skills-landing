# Fuentes técnicas y decisiones

Consulta: 22 de octubre de 2026. Se usaron documentación y SDK oficiales de Meta como referencia; no se incluye código del SDK ni se instala como dependencia. Algunas páginas HTML oficiales devolvieron 429 al abrirlas; se contrastaron campos con el código público oficial y los resultados indexados. No se verificó una llamada autenticada a Meta.

| Tema | Fuente primaria |
|---|---|
| Versión Graph/Marketing API | https://developers.facebook.com/blog/post/2026/07/29/introducing-graph-api-v26-and-marketing-api-v26/ |
| Autorización | https://developers.facebook.com/documentation/ads-commerce/marketing-api/get-started/authorization |
| Creatividades | https://developers.facebook.com/documentation/ads-commerce/marketing-api/reference/ad-creative |
| Link data y caption | https://developers.facebook.com/docs/marketing-api/reference/ad-creative-link-data/ |
| CTA value y link_caption | https://developers.facebook.com/docs/marketing-api/reference/ad-creative-link-data-call-to-action-value/ |
| Migración de identidad Instagram | https://developers.facebook.com/docs/graph-api/changelog/version22.0/ |
| SDK oficial: create campaign/adset/image/video | https://github.com/facebook/facebook-python-business-sdk/blob/main/facebook_business/adobjects/adaccount.py |
| SDK oficial: estrategia de puja | https://github.com/facebook/facebook-python-business-sdk/blob/main/facebook_business/adobjects/adset.py |
| SDK oficial: story spec | https://github.com/facebook/facebook-python-business-sdk/blob/main/facebook_business/adobjects/adcreativeobjectstoryspec.py |
| SDK oficial: video data | https://github.com/facebook/facebook-python-business-sdk/blob/main/facebook_business/adobjects/adcreativevideodata.py |
| SDK oficial: link data | https://github.com/facebook/facebook-python-business-sdk/blob/main/facebook_business/adobjects/adcreativelinkdata.py |
| Colección oficial de Meta | https://www.postman.com/meta/facebook-marketing-api/overview |

Decisiones propias del módulo: un negocio por instancia; máximo por lote; URLs visibles del mismo hostname exacto; solo adultos; solo JPG/PNG para imagen; fail-closed ante creación incierta; configuración vía token administrado; perfiles inmutables por borrador. No son afirmaciones de que Meta exija exactamente esas restricciones en todos los casos.

Los campos y compatibilidades de una API pueden cambiar. Al integrar, validar el caso real con la versión y cuenta seleccionadas. La presencia de un campo en el SDK no garantiza que toda combinación de objetivo, placement, cuenta y creatividad lo acepte.
