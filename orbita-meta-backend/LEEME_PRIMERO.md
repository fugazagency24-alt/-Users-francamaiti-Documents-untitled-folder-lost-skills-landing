# Orbita · Publicador de campañas Meta

Este ZIP contiene un backend ejecutable, sin interfaz gráfica, para integrar en tu Orbita existente. Incluye conexión real por Marketing API, simulador local, contratos de API, adaptadores para la IA, ejemplos y un prompt completo para Claude.

**Para entregárselo a Claude:** adjuntá este ZIP, dale acceso al código de Orbita y pegá el contenido de `PROMPT_PARA_CLAUDE.md`. No pegues tus tokens en el chat: se configuran como secretos del servidor.

## Lo que hace

| Opción | Resultado |
|---|---|
| BID_CAP_1_1_10 | Una campaña, un conjunto, diez anuncios. Puja máxima obligatoria. Presupuesto en el conjunto. |
| ABO_1_1_1 | Por cada creativo, una campaña, un conjunto y un anuncio. Tres creativos crean tres campañas. |
| Pegar enlace | Imagen JPG/PNG directa, video público con portada, o manifiesto JSON con varios creativos. |
| Personalización | Copy, título, descripción, CTA, URL de destino, enlace visible solicitado y UTM. Defaults más cambios por anuncio. |
| Publicación | Crear pausado o solicitar activación automática al terminar. También activar después, pausar, ver progreso, previews y métricas. |

“BIDCAMP” se interpretó como **Bid Cap**, no como Cost Cap ni CBO. ABO usa `LOWEST_COST_WITHOUT_CAP`. No se presupone ningún monto comercial: los valores de los ejemplos son ficticios.

El UTM se guarda una vez en el perfil y se reutiliza; podés reemplazarlo. Se envía en `url_tags`, separado del destino, preservando macros de Meta.

El enlace visible tiene tres opciones: automático, personalizado o sin personalización. **No existe aquí una promesa de ocultar el dominio en todas las ubicaciones.** Meta controla la presentación final. El texto personalizado debe ser una URL válida del mismo dominio; no texto libre. Para imagen se usa `caption`; para video, `call_to_action.value.link_caption`.

## Estado de esta entrega

Código implementado y probado localmente con Meta simulada. El adaptador HTTP real está incluido, pero **no se conectó ninguna cuenta, no se crearon campañas reales y no se verificó entrega publicitaria real**. Los permisos, límites de cuenta, formatos y aprobación final deben comprobarse con tu cuenta durante la integración.

Es un servicio interno para **un negocio / perfil por instancia**, con SQLite y un worker. No es un SaaS multicliente, ni un servidor para exponer directamente a Internet. Orbita debe aportar autenticación de usuarios, autorización, pantalla y despliegue. Si hay varios negocios, aislar servicio/base/token por negocio o implementar aislamiento antes de habilitarlos.

## Prueba sin Meta

Requiere Python 3.12 o superior, Linux/macOS; Windows puede usar Docker. No necesita paquetes Python externos para funcionar o probarse.

```bash
python -m unittest discover -v
python examples/run_mock_demo.py
```

El segundo comando simula los dos formatos y un anuncio de video. `SIMULATED` es un resultado de prueba.

## Ejecutar el servicio

```bash
cp .env.example .env
python -c 'import secrets; print(secrets.token_urlsafe(48))'
```

Colocá esa clave en `ORBITA_SERVICE_KEY` dentro de `.env`. Para esta primera prueba, mantené `META_MODE=mock`.

```bash
set -a
. ./.env
set +a
python -m orbita_ads
```

En otra terminal con las mismas variables cargadas:

```bash
curl -sS -X PUT http://127.0.0.1:8787/v1/profile \
  -H "Authorization: Bearer $ORBITA_SERVICE_KEY" \
  -H 'Content-Type: application/json' \
  --data-binary @examples/profile.json

curl -sS -X POST http://127.0.0.1:8787/v1/drafts \
  -H "Authorization: Bearer $ORBITA_SERVICE_KEY" \
  -H 'Content-Type: application/json' \
  --data-binary @examples/bid-cap-1-1-10.json
```

La respuesta devuelve `draft_id`, `plan_hash`, resumen y operaciones. Publicar ese borrador es una segunda llamada que puede realizar automáticamente Orbita cuando el usuario ya pidió publicar; no exige otra pantalla de confirmación. Ver `docs/API.md`.

Alternativa: `docker compose up --build`. Docker no fue ejecutado en esta entrega; se incluye la configuración. El puerto queda ligado a loopback en el host y los datos en un volumen persistente.

## Para conectar tu Meta

Seguí `docs/CONECTAR_META.md`. Necesitás token autorizado, cuenta publicitaria, página, moneda, presupuesto, países y, para ventas, píxel. Instagram es opcional. Configurás esto una vez; luego Orbita puede reutilizarlo.

El servicio usa **API oficial**, no una sesión de navegador ni clics de Manus. GitHub puede almacenar el código, pero no concede permisos sobre Meta. Los adaptadores de `integration/` permiten que la IA de Orbita prepare, publique, active, pause y consulte campañas. No se afirma haber integrado Manus ni un repositorio que no fue proporcionado.

## Archivos principales

| Archivo/carpeta | Uso |
|---|---|
| `PROMPT_PARA_CLAUDE.md` | Instrucciones completas para integrarlo a Orbita. |
| `orbita_ads/` | Backend, validación, planificador, cliente Meta, cola, persistencia y HTTP. |
| `integration/orbita-client.ts` | Cliente para backend TypeScript/JavaScript. |
| `integration/agent_tools.py` y `claude-tools.json` | Contrato y ejecución de herramientas para la IA. |
| `integration/openapi.json` | Contrato REST OpenAPI 3.1. |
| `examples/` | Perfil, campañas, video, link y demo ejecutable. |
| `docs/` | API, conexión, workflow, operación, límites, fuentes y pruebas. |

## Límites concretos

Se soportan anuncios de imagen/video hacia un sitio web; objetivo ventas con PURCHASE o tráfico con LINK_CLICKS, edades adultas y países. No se incluyen WhatsApp, formularios, catálogo, carrusel, categorías especiales/reguladas, segmentación avanzada, OAuth de múltiples clientes, importador de carpetas Drive, edición de anuncios existentes, horarios programados ni optimización automática de presupuestos.

El límite configurado es **por lote nuevo**, no un límite global del gasto acumulado de toda la cuenta. Cada lote adicional suma presupuesto. El presupuesto diario de Meta tampoco es un tope rígido por día. No se impone un límite total de duración: una campaña activada continúa hasta que se pause o Meta la detenga. Esto debe quedar claro en Orbita.

Antes del primer uso con gasto: completar credenciales, validar una campaña real pausada, revisar creatividad/CTA/UTM y estados en Meta, y activar con el presupuesto elegido por el usuario.
