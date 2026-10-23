# Verificación de la entrega

Fecha: 22/10/2026. Python 3.12.14. No se usaron credenciales de Meta ni se realizaron publicaciones reales.

## Ejecutado

`python -m unittest discover -v`: **19 pruebas aprobadas**.

Cobertura funcional: estructura Bid Cap 1:1:10; ABO por creativo y suma de presupuesto; copy/CTA/enlace/UTM; caption de video; rechazo de parámetros inválidos/duplicados; hash de borrador inmutable; idempotencia y conflictos; creación completa simulada; orden de activación; activación posterior sin duplicados; pausa; compensación de fallo de activación; reintento conocido conservando IDs; bloqueo de creación incierta; recuperación tras reinicio; video y portada; píxel requerido; bloqueo de modo live no habilitado; allowlist e IP privada; atajo de link; autenticación y flujo HTTP local.

`python examples/run_mock_demo.py`: tres flujos completos simulados:

| Caso | Campañas | Adsets | Anuncios | Pasos | Estado |
|---|---:|---:|---:|---:|---|
| BID_CAP_1_1_10 | 1 | 1 | 10 | 32 | SIMULATED |
| ABO con tres imágenes | 3 | 3 | 3 | 15 | SIMULATED |
| ABO con video | 1 | 1 | 1 | 7 | SIMULATED |

`python -m compileall -q orbita_ads integration examples`: sintaxis Python correcta.

Contratos JSON generados desde `integration/build_contracts.py`. ZIP validado con comprobación CRC y exclusión de cachés, bases de datos y secretos reales.

## No verificado en esta entrega

No se ejecutó la integración dentro del repositorio real de Orbita, porque no se proporcionó. No se ejecutó el contenedor Docker. No hubo compilador TypeScript disponible para comprobar el adaptador TS. No se conectó un modelo Claude ni se ejecutó un bucle real de herramientas de IA. No se validaron credenciales, permisos, aprobación publicitaria, formatos ni entrega con una cuenta real de Meta. Los mocks prueban el workflow local; no demuestran compatibilidad de todas las cuentas con los payloads.

## Prueba de aceptación en la integración

Configurar perfil real y token, verificar conexión, crear una estructura autorizada PAUSED, inspeccionar los objetos y previews en Meta, comprobar CTA/destino/UTM, luego activar con autorización de presupuesto. Revisar effective_status y confirmar entrega con métricas reales. Si Meta exige campos adicionales, implementarlos y repetir la prueba afectada antes de anunciar la función como operativa.
