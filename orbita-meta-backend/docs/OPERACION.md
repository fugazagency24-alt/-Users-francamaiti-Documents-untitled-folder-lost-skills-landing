# Operación e integración

## Despliegue

El servidor HTTP de la biblioteca estándar es un transporte interno sencillo. Ubicarlo en loopback o una red privada detrás del backend de Orbita. Para cruzar hosts, usar TLS/proxy y autenticación de servicio. El cliente TypeScript exige TLS salvo loopback. No publicar el puerto directamente en Internet; el Docker Compose incluido lo enlaza a 127.0.0.1.

Orbita debe autenticar usuarios, autorizar acciones/IDs, limitar solicitudes en su gateway y registrar actor/negocio del lado de Orbita. El publicador solo tiene una clave de servicio y un perfil global. No proporciona RBAC ni aislamiento multitenant. El modelo no recibe la clave ni acceso arbitrario a la API; registrar únicamente sus herramientas permitidas. PUT profile y resolve son administrativos.

Un proceso por base de datos local persistente. El lock usa fcntl y evita dos procesos simultáneos. No correr en serverless efímero ni con múltiples réplicas sin adaptar la persistencia/cola. Conservar SQLite y el volumen al actualizar el contenedor. Para backup consistente usar la API backup de sqlite3 o detener el servicio; no copiar solo el archivo principal mientras WAL esté activo.

`.env` contiene secretos y está ignorado por git. SQLite guarda links (incluidos parámetros de URLs firmadas), copy y datos de campañas, pero no tokens. Proteger volumen/backups y aplicar retención conforme al negocio. El arranque usa umask 077. No guardar el ZIP final con secretos agregados.

## Recuperación

Ante un fallo conocido, corregir la causa externa y POST retry. No editar el plan en SQLite ni reemplazar IDs. Para cambiar copy/destino/presupuesto, crear un borrador nuevo y revisar qué campañas previas deben pausarse; no se implementa edición de anuncios existentes.

Ante UNCERTAIN, mirar el marcador en Ads Manager y reconciliar antes de reintentar. Ante una pausa fallida, consultar Meta y volver a llamar pause. Mantener una vía administrativa para pausar desde Ads Manager si la API o token fallan. La pausa del servicio es best effort y no puede asegurar entrega cero mientras se completa una llamada ya enviada.

Si se perdió SQLite, no volver a ejecutar a ciegas las entradas anteriores: podrían existir campañas reales. Recuperar backup o inventariar/reconciliar objetos remotos. No se incluye importador general de campañas de la cuenta.

No cambiar de mock a live utilizando trabajos de la otra modalidad. El backend bloquea esa mezcla. Generar un nuevo borrador validado después de configurar la cuenta real. Los IDs simulados no existen en Meta.

## Qué observa la IA

`orbita_campaign_status`: progreso persistido local. `orbita_campaign_remote`: estado efectivo de objetos en Meta. `orbita_campaign_insights`: métricas de hoy por campaña. Esto permite informar si está en revisión o entregando sin manejar un navegador. No implementa captura de pantalla, Manus ni optimización continua por resultados.

El adaptador Python recibe tool name + arguments y ejecuta un conjunto cerrado de rutas. El cliente TypeScript es una alternativa server-side. Para usar el adaptador con Claude, registrar el array de `claude-tools.json`, procesar tool_use con la autorización real de Orbita y devolver el resultado como tool_result según el SDK ya usado por Orbita. El ZIP no contiene claves de Anthropic, un modelo ni un bucle de agente autónomo.

## UX recomendada

Configuración inicial persistente; luego un formulario corto con estructura, creativos y personalización. Mostrar resumen “N campañas / N conjuntos / N anuncios · moneda · presupuesto total por día · estado al terminar”. Un clic Publicar puede crear borrador y publicar inmediatamente si la instrucción y parámetros ya están autorizados. No exigir aprobación en cada paso interno.

Progreso: preparando medios → creando estructura → activando, si corresponde. Mostrar las advertencias reales de enlace visible. No mostrar el JSON técnico al usuario final por defecto. Ofrecer detalle de errores a quien administra.

El máximo por lote no controla el total de campañas activas en la cuenta. Si Orbita necesita un límite global, debe sumar presupuestos activos y reservar capacidad de manera transaccional antes de publicar; esa funcionalidad no está incluida. No presentar ese máximo como tope garantizado de gasto de Meta.
