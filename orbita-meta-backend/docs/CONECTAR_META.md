# Conectar el negocio a Meta

La conexión real no se hizo en esta entrega porque no se proporcionaron cuenta, token ni activos. El backend incluye un cliente HTTP real con versión Graph configurable; por defecto `v26.0`, identificada en documentación oficial consultada el 22/10/2026. Confirmar disponibilidad y cambios al desplegar.

## Configuración inicial

1. En Meta for Developers, usar una app habilitada para Marketing API, vinculada al negocio cuando corresponda. Revisar el nivel de acceso y requisitos de revisión/verificación para ese caso de uso; los requisitos para activos propios y activos de terceros pueden diferir.
2. Para automatización de tu propio negocio, configurar un usuario del sistema en el negocio y asignarle los activos necesarios, incluyendo la cuenta publicitaria y página. Proveer un token autorizado para la app y los permisos usados. Para escribir publicidad se necesita `ads_management`; para lecturas/reportes, conceder el alcance de lectura que corresponda al token y app. Lecturas de página/Instagram pueden exigir permisos y tareas adicionales. Validarlos en la documentación/panel de la app y con el token real, no asumir que un token con acceso a una cuenta tiene acceso a todos los activos.
3. Guardar `META_ACCESS_TOKEN` en el secret manager del hosting. `META_APP_SECRET` habilita `appsecret_proof` HMAC en las llamadas. No enviar secretos al navegador, al chat, al ZIP ni al repositorio.
4. Completar el perfil con cuenta (`act_...`), página, píxel para ventas, identidad Instagram si se usa, moneda real, países, presupuesto, máximo por lote, bid cap y defaults de anuncios/UTM. No copiar los IDs ficticios de examples.
5. Configurar `ASSET_ALLOWED_HOSTS` con los dominios exactos de tu almacenamiento. Los links deben ser HTTPS públicos o firmados, sin cookies/redirects; Meta también debe poder descargar los videos. Configurar URLs firmadas con duración suficiente para la cola, procesamiento y reintentos. No se siguen enlaces de carpetas ni páginas de login.
6. Poner `META_MODE=live`, mantener inicialmente `ENABLE_LIVE_PUBLISH=false`, reiniciar y llamar `/v1/connection`. Verificar moneda, estado de cuenta y acceso de lectura. Ese resultado no certifica todos los permisos de escritura.
7. Una vez autorizado el primer ensayo, habilitar `ENABLE_LIVE_PUBLISH=true`, reiniciar y publicar un borrador con `target_status=PAUSED`. Esto crea objetos reales aunque no haya entrega. Revisar en Ads Manager objetivo, puja, presupuesto, identidad, medios, copy, CTA, destino y URL tags.
8. Para empezar a entregar, usar `/activate` o un nuevo borrador autorizado con `target_status=ACTIVE`. Consultar `/remote` y posteriormente `/insights`. Revisión, mínimos de presupuesto, restricciones y entrega dependen de Meta.

## Token y vigencia

El módulo usa un token aprovisionado fuera del servicio. **No implementa OAuth, login de Meta, intercambio/renovación de tokens ni selección automática de activos.** Su expiración/revocación debe monitorearse y el secreto rotarse por la infraestructura del negocio; el servicio lee el secreto al iniciar. No se supone que ningún token sea inmortal. Si Orbita ya administra OAuth, integrar su mecanismo seguro en el cliente Meta y conservar los controles de acceso.

No hace falta proporcionar una contraseña de Facebook ni una sesión de navegador. GitHub no sustituye este permiso. No se creó una app Meta ni se solicitó revisión de permisos por vos.

## Lo que puede requerir adaptación real

Algunas cuentas, mercados y objetivos requieren información adicional, validaciones o configuración publicitaria. El perfil actual solo representa ventas web con PURCHASE o tráfico a web, segmentación adulta básica y categorías especiales vacías. No usar este perfil para crédito, empleo, vivienda, política u otras categorías especiales/reguladas. Si el negocio requiere una de ellas, Claude debe ampliar el modelo, campos y pruebas antes de publicar esa campaña.

Un rechazo de Meta no se resuelve quitando silenciosamente el bid cap, cambiando el objetivo o mostrando un éxito falso. El código expone el error y conserva lo creado para que pueda corregirse o revisarse.
