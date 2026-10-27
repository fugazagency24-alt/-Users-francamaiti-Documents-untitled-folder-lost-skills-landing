# Estudio IA para Orbita

Paquete para integrar a Orbita la producción de avatares y anuncios de video con IA (Veo 3.1 Lite en Google Cloud).

## Cómo usarlo

1. Abrí Claude con acceso al repositorio de Orbita.
2. Adjuntá este ZIP.
3. Pegá el contenido de `PROMPT_PARA_CLAUDE.md`.
4. Tus credenciales (Google Cloud, ElevenLabs, Sync, Meta) se cargan como secretos del servidor. No las pegues en el chat.

## Qué trae

| Archivo | Uso |
|---|---|
| `PROMPT_PARA_CLAUDE.md` | El prompt de integración completo. |
| `sop/Video IA con Veo 3 Lite.md` | SOP de video: Veo, voz y acento, Jarvis, pipeline, QA y cumplimiento. |
| `sop/Realismo en avatares IA imagen.md` | SOP de imagen: avatar, pack de identidad, prompts, anti-degradación y upscale. |

## Pendientes antes de producción

- La URL exacta de Dub Voice (prueba P7).
- Las pruebas de calibración P1 a P4, como mínimo, en tu proyecto de Google Cloud (unos USD 40 por las diez).
- Nada de los SOP se renderizó todavía: la primera corrida real es la que valida.
