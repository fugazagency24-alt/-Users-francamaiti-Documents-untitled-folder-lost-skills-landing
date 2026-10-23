# Orbita · Meta Ads en tu computadora

## Abrirlo

1. Descomprimí la carpeta donde quieras.
2. Doble clic en `iniciar.command`. La primera vez macOS puede bloquearlo: clic derecho → **Abrir** → **Abrir**.
3. Se abre el navegador en `http://127.0.0.1:8787` → **Ejecución → Meta Ads**.

Para cerrarlo: Ctrl+C en la ventana de Terminal. Para volver a usarlo: doble clic otra vez.

Necesita Python 3.10 o más nuevo; si no está, el iniciador ofrece instalarlo solo para tu usuario. Tus datos (borradores, trabajos, IDs, archivos subidos y claves) quedan en `~/.orbita-meta-ads/`, con permisos solo para tu usuario. No están en esta carpeta ni en Git.

## Primer uso (una sola vez, en la pestaña Conexión)

1. **Token de Meta**: pegalo en el campo seguro. Queda en tu computadora; la pantalla nunca lo vuelve a mostrar. Cómo sacarlo: `docs/CONECTAR_META.md`.
2. **Modo real** con la publicación todavía deshabilitada → **Comprobar** → **Buscar mis activos** → elegí cuenta, página, píxel e Instagram.
3. **Datos habituales**: presupuesto, máximo por lote, puja Bid Cap, texto, destino, enlace visible y UTM → **Guardar configuración**.
4. Cuando «Comprobar» dé lectura y publicación OK: **Habilitar publicación real**.
5. Opcional: API key de Anthropic para el **Asistente IA**.

## Publicar

Pestaña **Publicar**: elegí Bid Cap 1:1:10 o ABO 1:1:1, pegá enlaces directos o subí archivos, ajustá texto si querés y **Publicar en pausa**. Seguimiento, activar, pausar, estado real en Meta, métricas y vistas previas: pestaña **Campañas**.

El presupuesto diario agregado es solo de ese lote: no limita otras campañas de tu cuenta.
