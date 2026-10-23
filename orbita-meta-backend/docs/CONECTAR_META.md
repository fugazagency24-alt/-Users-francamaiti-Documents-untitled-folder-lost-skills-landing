# Conectar tu negocio a Meta

Camino: **API oficial de Marketing + token de usuario del sistema** de tu propio portfolio comercial, guardado solo en el servidor. No incluye OAuth: para un solo negocio propio no hace falta y evita una pantalla “Conectar con Meta” sin flujo real detrás. Si Orbita ya tiene OAuth de Meta, se reutiliza su almacenamiento seguro del token.

## Qué está verificado (23/10/2026)

| Tema | Estado |
|---|---|
| Versión | Marketing API **v26.0** es la vigente (publicada 29/07/2026). No se encontró v27. |
| Cambios del 27/10/2026 | Aplican a todas las versiones. Afectan anuncios de encuesta, `applink_treatment=web_only` con destino web+app, categorías especiales y placements de Messenger Stories/Explore. **Ninguno toca los payloads de este módulo.** |
| Campaña sin presupuesto de campaña | Meta exige `is_adset_budget_sharing_enabled` (error 100/4834011 si falta). Se envía `false`. |
| Conjunto | Desde v23 Meta exige declarar `targeting_automation.advantage_audience`. **El ZIP original no lo enviaba**: ahora se envía 0 (respeta tu segmentación) o 1 si lo activás. |
| Bid Cap | `bid_strategy=LOWEST_COST_WITH_BID_CAP` + `bid_amount` en el conjunto. Sin presupuesto de campaña, la campaña queda fuera de Advantage+ (advantage_state DISABLED). |
| Identidad Instagram | `instagram_user_id` (reemplazó a `instagram_actor_id`). Descubrimiento: `act_…/connected_instagram_accounts`. |
| Enlace visible | Imagen: `link_data.caption` (URL real del negocio; no se usa en Instagram). Video: `call_to_action.value.link_caption`. |
| Validar escritura sin crear | `execution_options=["validate_only"]` devuelve `{"success":true}` sin crear el objeto. |
| Acceso para tu propio negocio | Acceso estándar alcanza para cuentas propias; revisión de app y verificación del negocio se exigen para administrar cuentas de terceros. Confirmalo en el panel de tu app. |

Fuentes en `docs/FUENTES.md`. Lo que solo se comprueba con tu cuenta real: permisos efectivos del token, mínimos de presupuesto/puja de tu moneda y aprobación de los anuncios.

## Pasos (uno por vez)

1. **Portfolio comercial.** En https://business.facebook.com/settings confirmá que tu portfolio tiene la cuenta publicitaria y la página. Resultado: los dos activos figuran en *Cuentas*.
2. **App.** En https://developers.facebook.com/apps creá una app tipo *Business* (o usá una existente), vinculada a ese portfolio, y agregá el producto *Marketing API*. Resultado: el ID de la app (no es secreto).
3. **Usuario del sistema.** En *Configuración del negocio → Usuarios → Usuarios del sistema* creá uno *Administrador* y asignale: cuenta publicitaria (*Administrar campañas*), página (*Crear anuncios*) y píxel. Resultado: los tres activos asignados.
4. **Token.** En ese usuario del sistema: *Generar token* para tu app con `ads_management` y `ads_read`. Para listar páginas por nombre sumá `pages_show_list` y `pages_read_engagement`; `business_management` si querés descubrir activos del portfolio. Elegí vencimiento y anotá cuándo rotarlo. **No lo pegues en el chat.**
5. **Guardarlo en el servidor.** Cargalo como secreto `META_ACCESS_TOKEN` en el gestor de secretos del hosting de Orbita (o en el campo administrativo seguro de Orbita). `META_APP_SECRET` (en *Configuración básica* de la app) habilita `appsecret_proof`. Nunca en Git, navegador, logs ni SQLite.
6. **Comprobar.** Con `META_MODE=live` y `ENABLE_LIVE_PUBLISH=false`, ejecutar `POST /v1/setup/verify` y `GET /v1/setup/assets?account_id=act_…`. Resultado esperado: `read_verified: true` (cuenta, moneda, página, píxel con nombres) y `write_validated: true`.
7. **Ensayo real pausado.** Con tus datos de prueba definidos, `ENABLE_LIVE_PUBLISH=true` y un borrador `target_status=PAUSED`. Revisar en Ads Manager y con `/remote` y `/previews`. Queda pausado: activar es una instrucción aparte, con gasto.

## Lectura vs. publicación

- `read_verified`: el token lee cuenta (activa, moneda correcta), página, píxel e Instagram configurados.
- `write_validated`: Meta aceptó una creación de campaña en modo `validate_only`. Prueba el permiso de escritura en la cuenta, sin crear nada.
- Creatividades con tu página y anuncios completos: solo los prueba el **ensayo real pausado**.

## Token y vigencia

El servicio lee el token al iniciar. No implementa intercambio ni renovación: si vence o se revoca, `/v1/setup/verify` lo muestra en `checks.token`; se genera otro (paso 4) y se reinicia el servicio. No hace falta contraseña de Facebook ni sesión de navegador. GitHub no otorga permisos sobre Meta.

## Límites del perfil

Ventas web con PURCHASE o tráfico a web, segmentación adulta por países, sin categorías especiales. Para crédito, empleo, vivienda, política u otras categorías reguladas hay que ampliar el modelo y las pruebas antes de publicar. Un rechazo de Meta no se “arregla” quitando el bid cap o cambiando el objetivo: se muestra el error y se conserva lo creado.
