# Prompt — App "Modo Toro" (para Claude Code)

> Prompt usado para construir `calistenia-app/`. Reusalo para cambios grandes.

## Objetivo

App personal de calistenia, **PWA instalable y 100% offline**, hosteada en **Cloudflare Pages**. Sin backend, sin cuentas, sin build step. HTML + CSS + JS vanilla. Datos en `localStorage`.

## Fuente de la rutina

`calistenia-app/data.js` (salida del prompt maestro `01-PROMPT-MAESTRO-RUTINA.md`). La app NO inventa ejercicios: solo renderiza esos datos. Prescripciones por fase → la app elige según la semana actual (fecha de inicio guardada; semana 4 de cada fase = descarga).

## Pantallas (tab bar abajo)

1. **Hoy**
   - Imagen de "nueva identidad" arriba (`media/yo.*`) con saludo según la hora + nombre.
   - Chip: semana N · fase · descarga.
   - Toggle **Plaza / Casa** (se recuerda).
   - Sesión sugerida del día (semana fija) + chips para cambiarla (A–E, X1, X2).
   - Rutina **en macro**: bloques → ejercicios con miniatura, nombre y series×reps. Tocar un ejercicio abre foto/video grande + 1 indicación.
   - Botón grande **Completé** (toggle). Botón **10k pasos** que, al marcarlo, te felicita.
   - Opcional: **Modo guiado** (un ejercicio por pantalla + timer de descanso). No es el default.
2. **Semana**: 7 días con estado, sesiones de la semana vs meta 6, racha.
3. **Hombro**: rutina de rehab con reglas de dolor y check del día.
4. **Libre**: elegir 10 / 15 / 20 min + foco → sesión armada al instante. Check.
5. **Yo**: peso (83 → 70), nombre, fecha de inicio, lado débil, descargar media offline, borrar datos.

## Estilo

Oscuro, minimalista, tipografía del sistema, un solo color de acento definido como token CSS (`--accent`) para cambiar el tema fácil. Mobile-first, botones grandes, cero ruido. Nada de alimentación.

## Offline

- `sw.js`: precache del shell + `media/index.json` y todo lo que liste. Cache-first. Versión en `CACHE`.
- `manifest.webmanifest` + íconos 192/512 + apple-touch-icon → "Agregar a inicio" en iPhone y Android.

## Media

El usuario deja fotos/videos en `media/` con el nombre = id del ejercicio (`dominadas.mp4`, `flex.jpg`, `yo.jpg`). `node tools/media-index.mjs` genera `media/index.json`. Sin media, la app funciona igual.
