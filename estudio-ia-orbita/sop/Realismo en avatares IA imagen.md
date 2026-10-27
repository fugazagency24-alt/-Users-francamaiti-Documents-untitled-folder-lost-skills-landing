# Dominá el fotorrealismo de avatares IA en 2026

En octubre de 2026 el fotorrealismo de un avatar en imagen fija ya no depende de "encontrar el modelo mágico". Los modelos de punta (GPT Image 2.5 Sunburst/Flare, Nano Banana Pro y 2.1, Seedream 5.0, FLUX.2/FLUX 3) pueden entregar algo que pasa por foto. Lo que separa una foto de un render es cómo escribís el prompt y cómo cuidás el archivo después. El prompt que funciona **describe un momento de cámara, no un render**: un dispositivo concreto con su óptica real (una selfie de celular es gran angular con foco profundo, no un bokeh de 85 mm), **una sola fuente de luz motivada** con dirección y temperatura, entre 3 y 5 imperfecciones de piel dosificadas según la edad, un entorno vivido con objetos concretos y ningún "booster" tipo 8K, masterpiece o perfect skin. OpenAI lo dice casi textual en su guía oficial ([OpenAI Cookbook](https://github.com/openai/openai-cookbook/blob/main/examples/multimodal/image-gen-models-prompting-guide.ipynb)). Para modelos, lo más sólido es un stack de dos motores. Nano Banana Pro da la piel más "documental". GPT Image 2.5 lidera todos los rankings, pero tiende al brillo de foto de stock. Para corregir conviene un editor que copie los píxeles que no tocás (Ideogram 4.5, Krea 3 o máscaras propias). La degradación al corregir no es mala suerte. Casi toda "edición" regenera el cuadro entero a través de un cuello de botella VAE que pierde información, y la calidad aguanta unas cinco pasadas antes de colapsar ([FreqEdit, CVPR 2026](https://arxiv.org/pdf/2512.01755)). Por eso el SOP se apoya en cinco hábitos: un máster congelado, ramas que salen siempre del máster, un cambio por pasada, componer solo la zona corregida, y upscale más grano una sola vez, al final. La identidad del avatar se sostiene con un pack de referencias y un descriptor fijo. Si hace falta escala, se suma un LoRA entrenado sobre una base con licencia comercial y QA de similitud facial. Como el cliente es comercial, hay tres reglas sin excepción: etiquetado visible, metadatos C2PA intactos y nunca presentar a un avatar como cliente real. En EE. UU. un testimonio falso puede costar hasta USD 53.088 por infracción bajo 16 CFR 465 ([Federal Register](https://www.govinfo.gov/content/pkg/FR-2025-01-17/html/2025-01361.htm)). En la UE, el Art. 50 del AI Act rige desde el 2 de agosto de 2026. Sobre la evidencia: casi no hay benchmarks controlados de piel humana. Lo que sigue combina guía oficial, consenso de practicantes y blogs de vendors, así que cada plantilla se valida con un A/B propio antes de entrar al SOP.

**Cómo leer este informe.** Las etiquetas marcan el nivel de evidencia:

| Etiqueta | Qué significa |
|---|---|
| **[OFICIAL]** | Documentación del fabricante leída de primera mano: SDK y cookbooks en GitHub, READMEs. |
| **[RESUMEN]** | El dato llegó solo por el resumen de un buscador. La página no se pudo abrir. |
| **[1 FUENTE]** | Hay una sola fuente, sin corroborar. |
| **[NO TESTEADO]** | Síntesis propia, no renderizada. |
| **[LICENCIA]** | Advierte de un uso comercial restringido. |

Cuando las notas se contradicen, manda la verificación de datos. Cinco correcciones tienen consecuencias directas:
- GPT Image 2.5 Sunburst/Flare es oficial.
- El apagado de Nano Banana 2 previsto para el 29/10 se retiró.
- REED-VAE es de 2025.
- Firefly Image 5 salió en octubre de 2025.
- Krea 2 tiene 12B parámetros.

Además, "LME-Bench" no se pudo verificar y no se usa. Los prompts van en inglés porque los modelos responden mejor así. Cada uno lleva una nota en castellano.

## 1) Reglas de oro: quince leyes que separan una foto de un render

Estas leyes resumen todo el informe. Cada una se desarrolla en su sección.

1. **Pedí una foto que se está sacando, no una imagen que se está renderizando.** OpenAI recomienda escribir "como si se estuviera capturando una foto real en el momento", usar lenguaje fotográfico, pedir textura real (poros, arrugas, desgaste de tela) y evitar palabras de estudio o puesta en escena. También recomienda incluir la palabra "photorealistic" **[OFICIAL]** ([OpenAI Cookbook](https://github.com/openai/openai-cookbook/blob/main/examples/multimodal/image-gen-models-prompting-guide.ipynb)).
2. **La óptica tiene que coincidir con el dispositivo.** Una selfie de celular es un gran angular de unos 24–26 mm equivalentes, con foco profundo y sin bokeh cremoso. El 85 mm f/1.8 queda para looks de "creador pro". OpenAI aclara que las especificaciones exactas de cámara se interpretan de forma laxa, así que funcionan como pistas de estilo, no como física ([OpenAI Cookbook](https://github.com/openai/openai-cookbook/blob/main/examples/multimodal/image-gen-models-prompting-guide.ipynb)).
3. **Una sola luz dominante, descripta como física.** Nombrá la fuente, el lado respecto de la cámara, la altura, la calidad, los Kelvin y una imperfección. "Cinematic", "studio", "dramatic" y "volumetric" empujan a lo escenificado. OpenAI pide literalmente "Avoid cinematic lighting, dramatic color grading, or stylized composition" **[OFICIAL]**.
4. **Dosificá las imperfecciones: 3 a 5 rasgos sutiles y acordes a la edad.** Las listas largas hacen que el modelo exagere acné, arrugas y manchas. Agregá siempre "slight" o "subtle" ([1min.ai](https://1min.ai/zh-TW/realistic-skin-texture-ai-prompts); [CSDN](https://blog.csdn.net/Fang_YuanAI/article/details/163130903)) **[RESUMEN]**.
5. **Cero boosters.** "8K", "ultra-detailed", "masterpiece", "hyperrealistic" y "flawless/glowing skin" traen sobrenitidez y piel de plástico. OpenAI escribe que los términos de cámara y composición guían el realismo "more reliably than generic '8K/ultra-detailed'" ([guía gpt-image-1.5](https://github.com/openai/openai-cookbook/blob/main/examples/multimodal/image-gen-1.5-prompting_guide.ipynb)). Fuentes coreanas llegan a lo mismo: "고퀄리티 / 완벽한 피부" (alta calidad / piel perfecta) da cara de muñeca ([CCFM](https://blog.ccfmedu.co.kr/ai-realistic-portrait-creation)).
6. **El escenario vende la realidad más que la cara.** Poné entre 4 y 7 objetos cotidianos concretos y la aclaración "not luxury, not staged". Un practicante brasileño lo resume así: lo que delata a una influencer IA es el cuarto demasiado limpio ([Higor Cruz](https://higorprompts.substack.com/p/influencer-ia-o-detalhe-idiota-que)) **[RESUMEN]**.
7. **Texto: exacto o ninguno.** O citás el texto literal entre comillas, o escribís "no readable text". La etiqueta real del producto se compone después, en edición ([Fstoppers](https://fstoppers.com/artificial-intelligence/inserting-products-existing-photos-ai-what-actually-works-901419)).
8. **Manos con guion.** Especificá qué mano, qué dedos, dónde va el pulgar y por qué está ahí. Usá una sola mano y pasá el producto como imagen de referencia. Los errores "funcionales", como agarrar algo de forma imposible, son los que menos detecta la gente ([Kellogg Insight](https://insight.kellogg.northwestern.edu/article/ai-photos-identification)).
9. **Generá el máster a la resolución nativa máxima, por API y en PNG.** Pedí 2K o más para primeros planos y `quality="high"` o superior en GPT Image. Nunca uses como máster una descarga de app de chat.
10. **Máster congelado y ramas.** Cada corrección sale del máster, o del último compuesto aprobado, y nunca de la última salida del modelo.
11. **Un cambio por pasada, y la preservación se garantiza componiendo.** Repetí la cláusula de "no cambiar" en cada pasada, pero recordá que solo componer la zona editada sobre el máster asegura que el resto no se degrade.
12. **Presupuesto de pasadas.** Como máximo 3 regeneraciones por zona y 5 pasadas de cuadro completo por rama. Si se supera, reconstruís desde cero con las referencias.
13. **Upscale, piel, sharpen y grano, una sola vez y al final.** El orden es upscale → piel → grade → sharpen con máscara → grano. Los upscalers borran el grano, así que el grano va después ([seedvr2.ai](https://www.seedvr2.ai/blog/upscale-ai-generated-images)).
14. **La identidad vive en el pack de referencias, no en el modelo.** El pack más el descriptor fijo es lo que se versiona. El QA combina similitud facial (ArcFace) con revisión humana al 100 % de zoom. Hay que revalidar cada vez que un modelo se retira o cambia.
15. **Etiquetá, conservá la procedencia y no inventes clientes.** Etiqueta "IA" visible, toggles de plataforma activados, C2PA intacto en los másteres y ningún avatar presentado como consumidor real (16 CFR 465; EU AI Act Art. 50).

## 2) Stack de modelos 2026: dos motores para generar y un editor que copie píxeles

Los rankings agregados favorecen a OpenAI. En el tablero AA-Image-T2I v2.1 de Artificial Analysis el orden es:

| Puesto | Modelo | Elo |
|---|---|---|
| 1 | GPT Image 2.5 Sunburst (max) | 1222 |
| 2 | Flare (max) | 1207 |
| 3 | GPT Image 2 (high) | 1186 |
| 4 | Nano Banana 2.1 | 1176 |
| 5 | MAI-Image-2.6 | 1166 |

Entre los modelos de pesos abiertos encabezan FLUX 3 Image Klein (1043), Qwen-Image-2.1 (1042) y Fibo 2.0 (1039) ([Artificial Analysis](https://artificialanalysis.ai/image/leaderboard/text-to-image)) **[RESUMEN del snippet oficial]**. En Arena (ex-LMArena), Sunburst era #1 en text-to-image con 1425±7 el 7 de octubre ([Arena](https://arena.ai/leaderboard/image/text-to-image)). Circulan también cifras de la versión v2.0 del tablero (Sunburst 1197, Flare 1191). No contradicen las anteriores: son otra versión, así que siempre citá versión y fecha.

El problema es que estos tableros mezclan todas las categorías de prompt, y en retratos la cosa se divide. Nano Banana Pro no aparece en el top 5 de AA, pero varias pruebas lo prefieren para piel:
- En una prueba de tres modelos, GPT Image 2.5 dio el resultado "glossier, more stock photo" y Nano Banana Pro el más cándido y documental ([Turbologo](https://turbologo.com/articles/nano-banana-pro-vs-nano-banana-2/)).
- Decrypt elogió la microtextura de 2.5, pero concluyó que "the skin is too smooth" ([Decrypt](https://decrypt.co/377998/chatgpt-images-2-5-vs-nano-banana-2-review)).
- Una prueba de 20 prompts puntuó la piel de Nano Banana Pro en ~9,4–9,5 contra ~7,5–7,8 de GPT Image 2 ([Oakgen](https://oakgen.ai/blog/gpt-image-2-vs-nano-banana-pro)) **[1 FUENTE, vendor]**.

En sentido contrario, MagicCreator eligió Sunburst para retratos por el detalle de piel y ropa ([MagicCreator](https://magiccreator.ai/posts/gpt-image-2-5-vs-nano-banana-2)). Un test de 17 modelos encontró la piel más convincente en GPT Image 2 y Nano Banana 2 ([getimg.ai](https://getimg.ai/blog/ai-realism-test-comparing-realistic-image-generation-models)) **[RESUMEN]**. La conclusión operativa es hacer un A/B propio entre los dos motores con tus prompts. El Elo no mide realismo de piel humana.

| Modelo (lanzamiento) | Mejor uso en el SOP | Resolución nativa | Referencias | Precio aprox. por imagen | Licencia / estado | "Tell" típico |
|---|---|---|---|---|---|---|
| **GPT Image 2.5 Sunburst / Flare** (8/9/2026) **[OFICIAL]** | Sunburst: finales y ediciones semánticas exigentes. Flare: default rápido, ~50 % menos latencia | Hasta 3840×2160. Más de 2560×1440 es "experimental". `xhigh`/`max` son exclusivos de 2.5 | 16 | Por tokens, mismo precio que GPT Image 2. ~USD 0,006 (low) a ~0,21 (max) en 1024², estimación de terceros | API cerrada; C2PA | Piel "stock" brillosa o demasiado lisa. En edición re-renderiza ~4/5 del cuadro |
| **GPT Image 2** (21/4/2026) | Base y edición; omitir `input_fidelity` | Igual que 2.5 | 16 | ~0,21 en high 1024² (terceros) | API cerrada | Realismo "limpiado" |
| **Nano Banana Pro** (`gemini-3-pro-image-preview`, 20/11/2025) | Base UGC con piel más cándida; identidad | 1K/2K/4K | 14 (6 en alta fidelidad). "Hasta 5 personas" sale de Google y de fuentes secundarias | 0,134 (1K/2K); 0,24 (4K) | API; C2PA + SynthID | Deriva de color y oscurecimiento en ediciones. Puede agregar overlays tipo celular sin que los pidas **[1 FUENTE]** |
| **Nano Banana 2.1** (`gemini-nano-banana-2.1`, 6/10/2026) | Exploración y volumen barato | 1K/2K/4K (4K según precios de terceros) | 14; 4 personajes + 10 objetos **[secundario]** | 0,0336 (1K); ~0,05 (2K); ~0,113 (4K) | GA | Piel menos natural que Pro. Ediciones locales, pero oscurece la imagen |
| **Nano Banana 2** (`gemini-3.1-flash-image`) | Migrar a 2.1 | 1K/2K/4K | 14 | 0,045 | Deprecado **sin fecha de apagado** (se retiró el aviso del 29/10) | — |
| **Seedream 5.0 Pro** (8/7/2026), **Lite** (24/2/2026), **Flash** (15/9/2026) | E-commerce pulido y producto | Pro ~2K; Lite 4K nativo | Pro/Flash ≤10; Lite/4.5 ≤14 | Pro ~0,075 (≤2,36 MP), reventa | API cerrada | Acabado comercial; piel más lisa que 4.5; luz dramática; texto largo con errores |
| **FLUX.2 [pro]/[max]/[flex]** (25/11/2025) | Control fino, JSON, colores HEX | 4 MP | 8 por API / 10 en playground | pro ~0,03/MP | API comercial | Sobrenítido, "un poco plástico" |
| **FLUX.2 [dev] 32B / [klein] 4B-9B** | Uso local y LoRA | 4 MP | dev ≤6 recomendado; klein ≤4 | Local | **[LICENCIA]** [dev] y klein 9B no comerciales; klein 4B Apache 2.0 | — |
| **FLUX 3 Image Klein** 5,6B (15/10/2026) | El mejor de pesos abiertos en AA | Hasta 4K | 10 | Local (8 GB VRAM) | **[LICENCIA]** FLUX Kommunity: gratis para uso comercial solo con ingresos < USD 5M (prensa) | El upsampler, obligatorio, puede reescribir la luz |
| **Qwen-Image-2.1** (20/9/2026) | Generación + edición local, RGBA | 2K nativo | 10 | Local o API Pro/Turbo | **[LICENCIA]** Qwen Research License: no comercial sin acuerdo | No figura entre los mejores en piel **[1 FUENTE]** |
| **Midjourney V8.2** (default 24/7/2026) | Look editorial | `--hd` 2048 nativo | Edit Model hasta 4 (desde 27/8/2026); `--oref` solo en V7 | Suscripción; sin API oficial | — | "Demasiado limpio"; más contraste y grading |
| **MAI-Image-2.6** (Microsoft, 10/8/2026) | Alternativa | ~1536×1536 | 5 | Tokens | Foundry | Resolución baja |
| **Grok Imagine Image 2.0** (7/8/2026) | Alternativa | 1K/2K | 5 | Desde 0,04 | API | Detalles de producción irregulares |
| **Reve 2.0** (3/6/2026) | Look fílmico | Render 2K → 4K (disputado) | — | — | — | El detalle se vuelve "papilla" con zoom |
| **Ideogram 4.5** (30/9/2026) | **Edición que copia píxeles** | 2K | 4 | 0,008–0,22 | Cerrado | Puesto bajo (#23) en preferencia general de edición |
| **Krea 3** (15/10/2026, beta) | Edición regional rápida por bounding box | 2K | 6 | 0,03 (1K) / 0,06 (2K) por edición | API solo en beta | Sin benchmarks independientes |
| **Higgsfield Soul 2.0** (20/2/2026) | UGC y moda baratos, presets | 720p/1080p | Soul ID ≥20 fotos | 0,0032–0,0057 | Uso comercial permitido según su FAQ | Tope de 1080p |
| **Krea 2** 12B (22/6/2026, abierto) | Base para LoRA | 1K–2K | — | Local | **[LICENCIA]** Krea 2 Community License; licencia comercial a pedido | Enhancer de prompt activado por defecto |
| **Firefly Image 5** (28/10/2025) | Fills "comercialmente seguros" | 4 MP (edición 2 MP) | — | Créditos | Entrenado con contenido licenciado | — |

Fuentes de la tabla:
- OpenAI: [openai-python image_model.py](https://github.com/openai/openai-python/blob/main/src/openai/types/image_model.py); [image_generate_params.py](https://github.com/openai/openai-python/blob/main/src/openai/types/image_generate_params.py); [9to5Mac](https://9to5mac.com/2026/09/08/openai-releases-chatgpt-images-2-5-with-sharper-details-and-more-precise-editing/).
- Google: [Gemini cookbook](https://github.com/google-gemini/cookbook/blob/main/quickstarts/Get_Started_Nano_Banana.ipynb); [LiteLLM registry](https://github.com/BerriAI/litellm/blob/main/model_prices_and_context_window.json); [LiteLLM PR #45491](https://github.com/BerriAI/litellm/pull/45491); [The Decoder](https://the-decoder.com/googles-new-image-model-nano-banana-2-1-generates-better-images-for-less-money/).
- Seedream: [Artlist](https://help.artlist.io/hc/en-us/articles/37481273737757-Seedream-5-0-Pro); [Picsart](https://picsart.com/blog/seedream-5-0-models-comparison/); [ZenCreator](https://zencreator.pro/ai-university/guides/seedream-image-complete-guide).
- FLUX: [BFL flux2 README](https://github.com/black-forest-labs/flux2/blob/main/README.md); [BFL Help](https://help.bfl.ai/articles/6944273991-what-are-the-flux-2-technical-specifications); [FLUX 3 Image Klein README](https://github.com/black-forest-labs/flux-3-image-klein/blob/main/README.md); [GlobeNewswire](https://www.globenewswire.com/news-release/2026/10/15/3381905/0/en/black-forest-labs-expands-access-to-frontier-visual-intelligence-with-open-weights-release-of-flux-3-image-klein.html).
- Qwen: [Qwen-Image-2.1 README](https://github.com/QwenLM/Qwen-Image-2.1/blob/main/README.md).
- Midjourney: [docs](https://docs.midjourney.com/hc/en-us/articles/32199405667853-Version); [Edit Model](https://docs.midjourney.com/hc/en-us/articles/48495453462797); [Legnext](https://legnext.ai/midjourney/v82).
- Microsoft: [MAI model card](https://microsoft.ai/pdf/MAI-Image-2.6-Model-Card.pdf).
- Grok: [OpenRouter](https://openrouter.ai/x-ai/grok-imagine-image-2.0-20260811).
- Reve: [Decrypt](https://decrypt.co/371033/reve-2-review-best-ai-image-generator-layout-control).
- Ideogram: [Ideogram 4.5](https://ideogram.ai/models/4.5/).
- Krea: [TestingCatalog](https://testingcatalog.com/krea-launched-krea-3-for-fast-and-precise-image-editing); [Krea 2 README](https://github.com/krea-ai/krea-2/blob/main/README.md).
- Higgsfield: [Higgsfield API](https://open.higgsfield.ai/models/higgsfield-ai/soul/v2/standard/playground).
- Adobe: [TechCrunch](https://techcrunch.com/2025/10/28/adobe-firefly-image-5-brings-support-for-layers-will-let-creators-make-custom-models/).

Fuera de juego: Imagen 4 se apagó en la Gemini API el 17/8/2026 ([changelog](https://ai.google.dev/gemini-api/docs/changelog?authuser=1)). DALL-E 2 y 3 quedaron retirados el 12/5/2026, y gpt-image-1.5 queda solo para flujos ya validados ([openai-python](https://github.com/openai/openai-python/blob/main/src/openai/types/image_model.py)). Hy Image 3.5 Preview de Tencent (22/9/2026) tiene especificaciones contradictorias (5 o 20 referencias, 2K o 4K), así que no la uses hasta confirmarlas. Meta Muse Image (7/7/2026) es gratis en las apps de Meta y va a alimentar Advantage+ ([CNBC](https://www.cnbc.com/2026/07/07/meta-ai-muse-image.html)).

**Qué usar para cada trabajo.**
- **Avatar base desde texto.** Shortlist: Nano Banana Pro (piel cándida, ideal para UGC) y GPT Image 2.5 Sunburst (tope de rankings y hasta 3840 px, pero vigilá el brillo "stock"). Alternativas a testear:
  - Midjourney V8.2 con `--raw` y stylize bajo, para editorial.
  - Seedream 4.5 o 5.0 Pro, para e-commerce pulido. ZenCreator califica a 4.5 por encima de 5.0 Pro en poros ([ZenCreator](https://zencreator.pro/ai-university/guides/seedream-image-complete-guide)).
  - Higgsfield Soul 2, para UGC de moda barato con tope de 1080p.
- **Editar sin perder calidad.** Para cambios locales que deben dejar intacto el resto: Ideogram 4.5 o Krea 3, o máscaras en ComfyUI/Photoshop. Para cambios semánticos que respeten la identidad: Nano Banana Pro/2.1, vigilando la deriva de color. Evitá cadenas largas en GPT Image 2.5: en el test de 30 ediciones de AA dejó intacto apenas un quinto del cuadro ([AlphaSignal](https://alphasignal.ai/news/artificial-analysis-runs-30-edits-to-expose-how-image-models-drift)).
- **Consistencia multi-referencia.** GPT Image 2/2.5 acepta 16 referencias, Nano Banana Pro/2 14 (6 en alta fidelidad), Qwen-Image-2.1 y FLUX 3 Klein 10, FLUX.2 [pro] 8 por API, Seedream 5.0 Pro 10, Grok y MAI 5. Las cifras son oficiales o secundarias según el caso; ver la sección 12.
- **Alta resolución nativa.** Solo Nano Banana Pro en 4K (USD 0,24) y GPT Image 2/2.5 hasta 3840×2160 tienen un 4K nativo creíble en el tier alto. FLUX.2 y Firefly 5 llegan a ~4 MP. Seedream 5 Pro, Qwen-Image-2.1, Midjourney V8.2 y Grok son 2K nativos y necesitan upscale.
- **Pesos abiertos dentro de la empresa.** El único sin asterisco de licencia es FLUX.2 [klein] 4B (Apache 2.0). FLUX 3 Klein, Krea 2 y Qwen-Image-2.1 requieren acuerdo comercial para una empresa grande **[LICENCIA]**.

## 3) Anatomía del prompt realista: orden, largo y formato según el modelo

Todos los modelos actuales usan un LLM o un VLM como codificador de texto. FLUX.2 [dev], por ejemplo, usa Mistral-Small-3.2-24B ([BFL README](https://github.com/black-forest-labs/flux2/blob/main/README.md)) y Qwen-Image-2.1 usa Qwen3-VL 8B ([Qwen README](https://github.com/QwenLM/Qwen-Image-2.1/blob/main/README.md)). Por eso importan la gramática y las relaciones entre elementos. "Her left hand holds the jar at chin height, label facing camera" se entiende. Una lista de tags al estilo SD1.5, con pesos tipo `(masterpiece:1.2)`, ya es legado.

OpenAI recomienda un orden consistente: escena/fondo → sujeto → detalles clave → restricciones. También pide declarar el uso ("ad") para fijar el "modo" y el nivel de pulido ([OpenAI Cookbook](https://github.com/openai/openai-cookbook/blob/main/examples/multimodal/image-gen-models-prompting-guide.ipynb)). Google propone una plantilla fotorrealista en cuatro partes: plano + sujeto + lugar, luz y clima, cámara y lente con foco en textura, y aspect ratio, siempre en párrafo narrativo ([Google Developers Blog](https://developers.googleblog.com/en/how-to-prompt-gemini-2-5-flash-image-generation-for-the-best-results/)) **[RESUMEN]**. El reescritor oficial de Qwen exige un bloque continuo de ~200 palabras para retratos en inglés, sin listas, en el orden identidad → ropa → cara/piel → pose → fondo ([prompt_utils_2512.py](https://github.com/QwenLM/Qwen-Image/blob/main/src/examples/tools/prompt_utils_2512.py)) **[OFICIAL]**.

**Orden del SOP:**
1. Medio + uso ("Photorealistic smartphone photo for a UGC-style skincare ad").
2. Identidad: edad, etnia o fototipo, contextura, pelo, rasgos marcadores.
3. Acción, pose, mirada y manos.
4. Entorno con 3 a 6 objetos concretos.
5. Cámara: dispositivo, focal, ángulo, distancia, encuadre, profundidad de campo.
6. Luz: fuente, dirección, calidad, Kelvin y una imperfección.
7. Textura: piel, tela, procesado del sensor.
8. Restricciones: sin texto, sin marca de agua, sin retoque, identidad fija.

**Prosa, JSON o segmentos.** OpenAI dice que cualquier formato sirve si la intención y las restricciones quedan claras, y que en producción se priorice "a skimmable template over clever prompt syntax" **[OFICIAL]**. El JSON sirve cuando varios operadores llenan campos a escala, cuando querés cambiar una sola variable congelando el resto, o cuando necesitás colores HEX en FLUX.2. BFL dice que FLUX.2 está entrenado para entender JSON estructurado ([BFL FLUX.2 guide](https://docs.bfl.ai/guides/prompting_guide_flux2)) **[RESUMEN]**. La virtud del JSON es más práctica que mágica: obliga a llenar todos los casilleros (cámara, luz, utilería), así el modelo no rellena con su default brilloso. El mejor híbrido son los segmentos rotulados (Scene / Subject / Camera / Lighting / Texture / Constraints), que OpenAI respalda explícitamente.

| Modelo | Largo sugerido | Formato | Particularidades |
|---|---|---|---|
| GPT Image 2 / 2.5 | 80–200 palabras | Segmentos rotulados + cola "No…" | Incluir "photorealistic" y el uso. `quality="high"` para caras; `xhigh`/`max` solo en 2.5. Omitir `input_fidelity` |
| Nano Banana Pro / 2.1 | 60–180 palabras | Párrafo narrativo, "dirigí como cinematógrafo" | Darle un rol a cada referencia ("Image 1 = face identity only"). Aspect ratio y `image_size` por config, no en el texto |
| FLUX.2 pro/max | 40–150 palabras, o JSON | Prosa o JSON, HEX con la palabra "color" delante | **Sin negativos**: describí el estado deseado. Nombrar cámara, lente o película real sirve |
| FLUX.2 [dev] | Largo, o con upsampling | Prosa | "benefits significantly from prompt upsampling" |
| FLUX 3 Image Klein | Medio | Prosa / JSON con bounding boxes | Upsampler "required". Revisá que no reescriba la luz |
| Seedream 4.5 / 5.0 | 30–100 palabras | Sujeto primero, restricción no negociable al principio | Tiende a lo dramático: pedí luz plana o natural de forma explícita |
| Qwen-Image-2512 / 2.1 | ~200 palabras en un bloque | Prosa continua | Usá el negativo oficial (sección 10). En 2.1 la CFG va en 1 salvo que uses negativo |
| Z-Image Turbo | Largo y todo en positivo | Prosa | CFG 0/1: los negativos no hacen nada |
| Midjourney V8.2 | Corto | Prosa + parámetros | `--raw --s 50–150`; V8 "ejecuta literal" |

Fuentes: [OpenAI Cookbook](https://github.com/openai/openai-cookbook/blob/main/examples/multimodal/image-gen-models-prompting-guide.ipynb); [Google 7 tips](https://blog.google/products/gemini/prompting-tips-nano-banana-pro/); [Atlabs FLUX.2](https://www.atlabs.ai/blog/flux-2-prompting-guide); [BFL upsampling](https://github.com/black-forest-labs/flux2/blob/main/docs/flux2_with_prompt_upsampling.md); [FLUX 3 Klein README](https://github.com/black-forest-labs/flux-3-image-klein/blob/main/README.md); [fal Seedream](https://fal.ai/learn/devs/seedream-v4-5-prompt-guide); [Krea Seedream 5 Pro](https://www.krea.ai/blog/15-powerful-seedream-5-0-pro-prompts-for-photorealism-product-shots-portraits-more); [Z-Image README](https://github.com/Tongyi-MAI/Z-Image); [Comfy Qwen 2.1](https://github.com/Comfy-Org/docs/blob/main/tutorials/image/qwen/qwen-image-2-1.mdx); [Blake Crosley](https://blakecrosley.com/blog/midjourney-v8-vs-v7-prompt-anatomy).

Hay dos trampas de anatomía. La primera son las contradicciones internas: "shallow depth of field" con "f/16", o más de ~10 direcciones de estilo apiladas ([VEED](https://www.veed.io/learn/nano-banana-pro-prompts)). Otra variante es mezclar "golden hour, softbox y flash directo": como advierte una guía en castellano, elegí una configuración dominante ([StarryAI ES](https://starryai.com/es/blog/realistic-ai-image)). La segunda trampa son los enhancers de prompt activados por defecto en FLUX 3 Klein, Qwen-Image-2.1 y Krea 2 Turbo, que pueden reinsertar vocabulario "cinematic" ([Comfy templates](https://github.com/Comfy-Org/workflow_templates/blob/main/templates/image_flux3_klein_t2i.json)). Para tomas donde la luz es crítica, apagalos o revisá el prompt expandido **[NO TESTEADO]**. Un hábito que aparece en cuatro idiomas es el "crítico": un modelo de visión lista los defectos de la imagen como JSON de correcciones y esa lista se pega junto con la foto en la siguiente generación ([Génération IA](https://generationia.flint.media/p/nano-banana-shooting-photo-virtuel-json-prompting); [CCFM](https://blog.ccfmedu.co.kr/ai-realistic-portrait-creation)). Usalo para decidir la próxima *generación desde el máster*, no para encadenar ediciones.

## 4) Iluminación: una fuente física con firma visible vale más que cualquier adjetivo

No existe un A/B publicado y controlado que aísle una frase de luz y mida cuánto realismo agrega. Una búsqueda específica no encontró "a systematic side-by-side test of light direction" para Nano Banana Pro ([Chase Jarvis](https://chasejarvis.com/blog/nano-banana-prompts/)) **[RESUMEN]**. Lo que sí hay es un consenso fuerte, de cuatro puntos:

1. **Nombrá una fuente motivada con dirección** en lugar de una etiqueta de estilo.
2. **No pongas luz de estudio perfecta en una escena "cándida".** Un vendor de Seedream culpa exactamente a eso, "studio-perfect light even in supposedly candid shots", y pide "one coherent lighting scheme" por imagen ([Atlas Cloud](https://www.atlascloud.ai/blog/guides/seedream-5-pro-realistic-portraits)).
3. **La dirección de la luz se respeta.** Seedream y FLUX.2 la siguen de forma literal; Nano Banana Pro "needs direction on lighting, lens, and distance".
4. **La luz dura revela textura y la suave la esconde.** Esto lo explica la física fotográfica ([Fujifilm](https://fujifilm-x.com/en-us/?p=58542)), y la guía oficial de Krea 2 lo usa a propósito: "Harsh, direct lighting highlights intricate skin pores" ([krea-2 prompting.md](https://github.com/krea-ai/krea-2/blob/main/docs/prompting.md)) **[OFICIAL]**.

La consecuencia para UGC es contraintuitiva: la luz grande, frontal y suave "de belleza" alisa la piel y la acerca al plástico. Una luz direccional moderada (sol por la ventana, foco pelado, flash del celular) muestra poros y microsombras. Dejá la luz suavísima para cuando el brief de skincare pida justamente piel lisa.

Un truco **[1 FUENTE]** para Nano Banana Pro: si las sombras salen en la dirección equivocada, activá Thinking y pedí que calcule el recorrido de la luz desde la fuente. Por ejemplo: "make every cast shadow consistent with the window on camera-left" ([Chase Jarvis](https://chasejarvis.com/blog/nano-banana-prompts/)).

**Referencia de temperatura de color (Kelvin):**

| Fuente | Kelvin aproximados |
|---|---|
| Sodio | ~2050–2100 K. Es casi monocromático, así que describilo como "monochrome orange" y no con un número |
| Tungsteno | 2400–3200 K |
| LED cálido | 2700–3000 K |
| Hora dorada | ~2800–3000 K |
| Fluorescente | ~3000 K (cálido) / ~4200 K (frío) |
| Día y flash | ~5500 K |
| Nublado | ~6500–7000 K |
| Sombra | ~7500–8000 K |

Fuentes: [CAMEO](https://cameo.mfa.org/wiki/Color_temperature); [Cameraby](https://cameraby.com/en/learn/white-balance-presets); [PetaPixel](https://petapixel.com/2026/09/08/astronauts-before-and-after-photos-show-how-cities-switched-from-orange-to-white-light/) **[RESUMEN]**.

**Patrones de retrato.** Al llevar la luz principal desde el frente hacia los 90° se pasa por cuatro patrones ([PhotoWorkout](https://www.photoworkout.com/?p=128244)):
- **Butterfly**: frontal y alta. Lee como glamour.
- **Loop**: unos 20–45°. Es la opción accesible.
- **Rembrandt**: el triángulo de luz queda en la mejilla en sombra.
- **Split**: luz a 90°. Lee dramático.

### Léxico de iluminación (firma física + frase lista para copiar)

Los rasgos físicos están citados en las fuentes ([Lens Lounge](https://thelenslounge.com/what-is-softbox-light/); [Globe and Mail](https://www.theglobeandmail.com/multimedia/camera-club/how-to-light-your-pictures/article1214994); [Westcott](https://help.fjwestcott.com/en-US/why-is-the-light-from-my-ring-light-so-flat-637336); [Daily Photo Tips](https://dailyphototips.com/portraits/face-shadows/); [Glass](https://glass.photo/photography-terms/rim-light)). La redacción de las frases es síntesis **[NO TESTEADO]**.

| Setup | Firma física para mencionar | Frase (EN) | Lo que lo vuelve falso |
|---|---|---|---|
| Ventana lateral (45–90°) | Borde suave a medio; lado en sombra 1–3 pasos más oscuro; brillo rectangular en los ojos; fondo más oscuro | "lit only by a large window on camera-left, about 45 degrees to her face; soft but directional light, the right side of her face falls into gentle shadow; rectangular window reflection in her eyes; the room behind her is noticeably darker" | "perfectly even lighting", "no shadows", fill o rim imposibles en ese cuarto |
| Ventana frontal | Luz plana y pareja; brillos grandes centrados; poca textura | "she faces a bright window just behind the camera; flat, even daylight on her face, large square catchlights, natural daylight white balance around 5500K" | "studio/beauty lighting", "glowing skin" |
| Contraluz de ventana | Cara un poco subexpuesta; borde luminoso en el pelo; ventana quemada; algo de velo | "standing with her back to a bright window; the window is overexposed, her face slightly underexposed but readable, soft wrap-around light on the edges of her hair, a little haze from flare" | Cara perfecta *y* vista detallada de la ventana (look HDR) |
| Nublado / sombra abierta | Sombras muy suaves; dominante fría; brillos débiles; color apagado; rebote verde o de ladrillo | "overcast afternoon, the sky acts like a giant softbox; very soft shadows, slightly cool white balance, muted colours, faint catchlights, a hint of green bounce from the grass on her jaw" | "vibrant colors", "sun-kissed glow" con cielo cubierto |
| Contraluz de hora dorada | Sol bajo detrás; rim cálido en el pelo; cara en sombra abierta con rebote; flare | "late-afternoon sun low behind her, warm orange rim light on her hair and shoulders, her face in soft open shade lit by bounce from the pavement, slight lens flare and haze, warm white balance" | Cara iluminada de frente *y* pelo en contraluz por el mismo sol |
| Sol de mediodía | Sombras duras y cortas bajo cejas y nariz; ojos entrecerrados; especulares puntuales | "harsh midday sun from almost directly overhead, hard-edged shadows under her brows and nose, she squints slightly, small bright specular highlights on her forehead and nose" | "soft flattering light" al mediodía; nadie entrecierra los ojos |
| Flash directo (celular o compacta) | Luz frontal plana; sombra dura en la pared; caída rápida a negro; zona T brillante; brillo puntual | "photographed with the phone's built-in flash at night, flat frontal light, a hard dark shadow on the wall just behind her, background falls off into darkness, shiny highlights on her forehead and nose, small pinpoint catchlights" | Cara con flash y fondo perfectamente iluminado |
| Ring light (UGC beauty) | Luz sin sombras; brillo en anillo; cara "aerografiada" | "lit by a ring light directly in front at eye level, ring-shaped catchlight in both pupils, flat shadowless face, slight soft shadow outline on the wall behind her" + "visible pores, slight shine on nose" | Ring light *con* sombras laterales dramáticas o "glowing skin" |
| Oficina con paneles fluorescentes | Luz cenital; sombras en las cuencas y bajo el mentón; dominante verdosa fría (~4000–4200 K) | "overhead fluorescent ceiling panels, top-down light, mild shadows in her eye sockets and under her chin, slightly cool greenish cast, flat unflattering office light" | Brillo dorado cálido bajo paneles |
| Espejo de baño | Barra de luz arriba del espejo; sombra bajo las cejas; brillo en la frente | "vanity light bar above the mirror, light from slightly above and in front, faint shadow under her brows, bright highlight on her forehead, warm 3000K bulbs, glossy tile reflections" | — |
| Auto, de día | Ventanilla lateral como luz principal; habitáculo oscuro; reflejos en el vidrio | "daylight from the driver-side window on camera-left lights half her face, the car interior stays dark, soft fill from the windshield, faint reflection on the side glass" | Habitáculo parejo, sin dirección |
| Auto, de noche | Pantalla fría desde abajo o luz de techo cálida; mucho ruido | "night inside a parked car, the only light is the dashboard screen glowing cool blue on her chin and lower face, faint warm streetlight through the window, grainy high-ISO phone photo" | Cara limpia, sin ruido y totalmente iluminada |
| Mixta tungsteno + día | Dos dominantes en la misma cara | "mixed light: cool daylight from the window on camera-left, warm tungsten lamp on camera-right, her face has a cool side and a warm side, white balance in between" | Una sola dominante neutra en un cuarto que tiene dos fuentes |
| Pantalla del celular | Fuente chica, fría y cercana; caída rápida | "late at night in a dark bedroom, her face lit only by the cool blue glow of the phone screen in her hand, light falls off quickly past her face, grainy low-light photo" | La pantalla ilumina todo el cuarto |
| Calle de noche (sodio / LED) | Sodio naranja monocromo; LED ~4000 K "clínico" | "under an old sodium streetlight, monochrome orange light from above, colours of her clothes barely distinguishable, deep shadows outside the light pool" | Neón por todos lados, grading teal-orange |
| Gimnasio | Paneles LED industriales cenitales, luz dura; brillo de sudor | "overhead industrial LED high-bay lights, top-down hard light, sheen of sweat catching highlights, mirror reflections" | — |
| Testimonio semi-pro (loop) | Softbox a 30–45°, sin fill; brillo rectangular | "one large softbox camera-left, about 30–45 degrees off-axis and slightly above eye level, small nose shadow pointing down toward the right corner of her mouth (loop lighting), no fill, plain wall behind" | "three-point lighting" o "studio lighting" en una casa |
| Rim práctico | Borde fino solo del lado de la fuente; necesita un fondo oscuro | "a single warm practical lamp behind her on the right puts a thin rim of light on the right side of her hair; the background stays dim" | Rim de ambos lados sin fuente; rim contra un fondo claro |

**Gramática de dirección** (usá términos relativos a la cámara; "subject's left" es ambiguo):

```
[SOURCE] [POSITION: camera-left | camera-right | behind the camera | behind her | directly overhead | below the face]
[HEIGHT: at eye level | slightly above eye level | high above | from below]
[ANGLE (optional): about 45 degrees off the lens axis | 90 degrees to the side | from behind]
[QUALITY: hard-edged | soft but directional | very soft and diffused]
[RESULT ON FACE: which side is in shadow, where the nose shadow falls, catchlight shape]
[COLOUR: warm ~3000K | neutral daylight ~5500K | cool shade ~7000K]
```
Nota: esta plantilla obliga a describir la luz como un fotógrafo la anotaría. Todos los modelos con codificador LLM la leen **[NO TESTEADO]**.

**Frase de coherencia sujeto-fondo** (agregala a todo prompt de avatar en escena). Ataca la incoherencia de sombras, uno de los "tells" que persisten en 2026, porque los generadores aprenden patrones estadísticos y no geometría 3D ([Content Authenticity Initiative](https://contentauthenticity.org/blog/photo-forensics-from-lighting-shadows-and-reflections)):
```
The same window light that lights her face also lights the room: the wall on the left is brighter, shadows in the room fall to the right, matching softness and colour; no separate studio light on her.
```
Nota: amarra fondo y sujeto a la misma fuente **[NO TESTEADO]**.

**Frase para ediciones que cambian el fondo:**
```
Relight the person to match the background: light comes from [direction] at [colour temperature]; match shadow softness; add a soft contact shadow under her feet/elbows; match the background's grain and depth of field.
```
Nota: es el checklist de composición (dirección, dureza, Kelvin, sombra de contacto, grano y profundidad de campo) convertido en prompt ([DEV](https://dev.to/miatanaka/why-composited-people-look-pasted-lighting-and-color-coherence-111o)) **[NO TESTEADO]**.

**Descripciones que empujan a lo falso:**

| Evitá | Por qué (física) | Reemplazá por |
|---|---|---|
| "perfect / flawless / even lighting", "no shadows" | Toda cara real tiene un lado en sombra | La fuente y el lado de la sombra |
| "glowing / radiant / luminous skin" | Inventa una luz emitida que no existe | "small specular highlights on forehead and nose consistent with the window" |
| "rim light" sin fuente o de ambos lados | El rim solo aparece del lado de una fuente trasera | "a lamp behind her on the right gives a thin edge of light on her right shoulder" |
| "three-point lighting", "studio lighting", "softbox" en UGC | Implica un set profesional | Las fuentes prácticas del lugar |
| Combos HDR ("bright window and perfectly exposed face") | Una sola exposición no sostiene ambas cosas | "the window is blown out / her face slightly underexposed" |
| "volumetric", "god rays" en interiores | Hace falta humo o polvo en el aire | Omitilo, o "dusty air catches the sunbeam" si está motivado |
| "teal and orange", "neon accents" sin fuentes | Cada dominante de color necesita una fuente | Nombrá el cartel o la pantalla que emite ese color |

Hay dos sesgos por modelo a compensar. Seedream 5.0 Pro "tiende a luz dramática" ([Atlas Cloud](https://www.atlascloud.ai/it/blog/guides/seedream-5-pro-vs-nano-banana-2)) **[1 FUENTE]**. Midjourney V8.2 "leans toward more contrast, dramatic lighting, and bolder color grading" ([Medium](https://medium.com/@inchristiely/midjourney-v8-2-is-now-the-default-five-things-that-changed-30c8dffcc492)) **[RESUMEN]**. En los dos, pedí la luz plana o natural de forma explícita. Para las especulares sirve una frase comodín: "small natural specular highlights on the forehead, nose bridge and lower lip consistent with the light direction". Ata el brillo a la fuente en vez de pedir un "glow" uniforme.

## 5) Piel: poros, pecas y arrugas en dosis chicas y con lógica anatómica

Todos los modelos de 2026 alisan la piel por defecto, salvo que les pidas preservar la textura ([Prompt Architects](https://prompt-architects.com/blog/361-getting-realistic-skin-in-ai-images)) **[RESUMEN]**. La explicación más citada es que se entrenaron con fotografía publicitaria y de stock ya retocada ([Oakgen](https://oakgen.ai/blog/fix-plastic-skin-ai-portraits)). Practicantes chinos lo describen como un error de física de la luz: el modelo trata la piel como una superficie opaca y lisa, sin dispersión subsuperficial ([Zhihu](https://zhuanlan.zhihu.com/p/2056321651587995280)) **[RESUMEN]**.

La guía oficial de OpenAI pide textura de forma explícita ("pores, wrinkles, fabric wear, imperfections") y `quality="high"` cuando el detalle importa. Su ejemplo de referencia describe "weathered skin with visible wrinkles, pores, and sun texture" ([OpenAI Cookbook](https://github.com/openai/openai-cookbook/blob/main/examples/multimodal/image-gen-models-prompting-guide.ipynb)) **[OFICIAL]**. El reescritor oficial de Qwen-Image-2512 pide definir tono y textura con ejemplos como "matte with a light dusting of freckles, weathered laugh lines" ([prompt_utils_2512.py](https://github.com/QwenLM/Qwen-Image/blob/main/src/examples/tools/prompt_utils_2512.py)) **[OFICIAL]**.

**La dosis es la clave.** Elegí 3 a 5 rasgos y calificalos siempre con "slight/subtle". Sin ese calificador, la imagen parece envejecida a propósito ([CSDN](https://blog.csdn.net/Fang_YuanAI/article/details/163130903)) **[RESUMEN]**. Varias guías coreanas, independientes entre sí, sostienen que "la descripción del detalle, no el prompt negativo, es la respuesta". Proponen describir la piel por zonas: poros alrededor de la nariz, rojez en las mejillas, brillo leve en la zona T, pelitos cortos en el nacimiento del pelo ([i-boss](https://www.i-boss.co.kr/ab-6141-68347); [CCFM](https://blog.ccfmedu.co.kr/ai-realistic-portrait-creation)) **[RESUMEN]**. Para el tono, una guía coreana recomienda especificar la **escala Fitzpatrick o el subtono** (warm/cool/olive) ([brunch @codept](https://brunch.co.kr/@codept/45)) **[1 FUENTE]**. Es muy útil para castear en LatAm y Brasil sin depender del token "latina", que tiende al estereotipo.

**Sobredosis.** El autor de un fine-tune de piel advierte que empujar demasiado el término de textura produce "exaggerated detail and plastic-looking skin" ([Ultraskin](https://huggingface.co/VegaKH/Ultraskin)), y un blog coreano describe "piel de escamas de pez" en primeros planos de GPT Image cuando se piden "alta resolución / detalle rico" ([pixo](https://pixo.video/ko/blog/gpt-image-fish-scale-fix)) **[1 FUENTE, vendor]**. La lección es que más detalle de piel no equivale a más realismo.

**Pecas y arrugas.** Las pecas se ven pintadas cuando son uniformes, de alto contraste y "encima" de la piel. Usar "pigmentation" ayuda a que se lean debajo de la superficie ([AIPromptHub](https://www.aiprompthub.ai/blog/12-grok-prompts-realistic-skin-textures-high-quality-portraits)) **[RESUMEN]**. "Blemishes" a secas produce demasiadas marcas; es mejor "subtle freckles" u "occasional redness". Si poros o pecas forman una grilla repetida, el modelo está alucinando textura. En caras chicas, además, las pecas finas se empastan por falta de píxeles, así que generá a 2K o más ([MyAIForce](https://myaiforce.com/fix-plastic-skin/)) **[RESUMEN]**. Las arrugas se leen como anatomía cuando se atan a una expresión ("laugh lines when smiling"), no cuando se piden como textura genérica.

**Brillo y maquillaje.** Pedí brillo solo donde la piel real es grasa: zona T, puente de la nariz, pómulos bajo la luz principal. "Dewy" y "glass skin" son señales editoriales de belleza que devuelven el acabado brilloso de IA. Los prompts japoneses populares siguen pidiendo "滑らかで輝く肌" (piel lisa y brillante) junto a "RAW 写真"; al localizar para LatAm, sacá esa frase ([YouMind JA](https://github.com/YouMind-OpenLab/awesome-nano-banana-pro-prompts/blob/main/README_ja-JP.md)).

**Por modelo:**
- **GPT Image.** La vieja dominante amarilla (gpt-image-1.5) se corrige en el prompt *original* con "neutral white balance, accurate skin tones". Pedir después "make this less yellow" regenera la imagen entera ([TechRadar](https://www.techradar.com/ai-platforms-assistants/chatgpt/tired-of-that-yellow-tint-in-chatgpt-images-heres-how-to-fix-it-with-simple-color-correction)).
- **Seedream 5.0 Pro.** La queja más repetida es la piel "over-smoothed compared to Seedream 4.5". Agregá ruido de sensor y suavidad de cámara en mano, y prohibí los filtros de belleza ([Atlas Cloud](https://www.atlascloud.ai/blog/tips/seedream-5-pro-prompt-guide)).
- **Midjourney.** `--raw` apaga la embellecida por defecto.

**Edad → dosis** (inferencia a partir de "matches the person's age" y "age details"; **[NO TESTEADO]**):

| Edad | Rasgos que corresponden | No pongas |
|---|---|---|
| 20–29 | Poros, algún granito, ojeras leves, pelitos en la frente | Arrugas marcadas |
| 30–39 | + patas de gallo tenues y surcos nasogenianos al sonreír | Piel sin poros |
| 40–59 | + líneas en la frente, risa más profunda, manchas de sol | Piel "de 25" |
| 60+ | + arrugas profundas, manchas de edad, piel fina y laxa | Brillo "glass skin" |

**Bloques de piel para pegar** (síntesis de fragmentos citados; **[NO TESTEADO]**):

```
Photorealistic candid photo. Natural skin texture with visible pores on the nose and cheeks, faint fine lines that match a [AGE]-year-old, slightly uneven skin tone with mild redness around the nostrils, a little natural shine on the forehead and nose (not all-over gloss), fine peach fuzz visible where the light grazes the cheek. Light or no makeup. No heavy retouching, no beauty filter, no airbrushing.
```
Nota: bloque base para GPT Image, Nano Banana y Seedream. Elegí 3 a 5 rasgos, no todos.

```
...matte skin with visible pores and faint fine lines, slight redness around the nose, soft natural highlight on the forehead, unretouched...
```
Nota: versión para FLUX.2 y Z-Image Turbo, que no tienen negativos efectivos. Todo va en positivo.

```
a light, uneven dusting of small sun freckles concentrated across the nose bridge and upper cheeks, fading toward the jaw, varying slightly in size and tone, soft-edged pigmentation under the skin rather than dots on top
```
Nota: pecas creíbles. Si la marca no quiere pecas, no escribas "no freckles": directamente no las nombres, porque algunos modelos se enganchan con el sustantivo.

```
[AGE]-year-old with age-appropriate fine lines: faint crow's feet that deepen when she smiles, light nasolabial folds, a couple of shallow horizontal forehead lines
```
Nota: arrugas atadas a la expresión, que se leen como anatomía.

```
eyes with natural moisture and a single soft catchlight from the window on the left, identical in both eyes; slight redness at the inner corners; natural, slightly asymmetric features (one eyebrow a touch higher, a small mole near the jaw); relaxed mid-sentence expression, lips slightly parted; natural teeth, slightly uneven, off-white, not veneers — or a small closed-mouth smile
```
Nota: ojos, cara y dientes. Ojos "muertos" aparecen cuando no hay fuente de luz definida, la mirada no apunta a nada o el iris está sobresaturado. La sonrisa amplia es el punto débil de 2026, porque los bordes de los dientes se funden ([WeDetect](https://wedetect.ai/how-to-tell-if-an-image-is-ai-generated)) **[RESUMEN]**. La investigación sobre brillos corneales que no coinciden entre los dos ojos viene de la era GAN ([Hu, Li y Lyu](https://arxiv.org/abs/2009.11924v2)). Igual sirve como control de QA: compará los dos brillos al 200 %.

## 6) Pelo: romper el "casco" con mechones que se cruzan

El pelo IA falla cuando se renderiza como un "casco": una superficie continua de mechones paralelos. El pelo real tiene mechones que se cruzan, pelos sueltos que se levantan en la coronilla, pelitos cortos en las sienes y mechones que tocan la cara. La luz dura y plana lo apelmaza, la luz suave y difusa lo separa ([FreeAIPromptMaker](https://freeaipromptmaker.com/blog/2026-05-13-master-ai-hair-prompts-styles-textures-dynamics)) **[RESUMEN]**. En retoque pasa lo mismo: sacar todos los pelos sueltos produce el casco, y dejar algunos vuelve el retrato más auténtico ([Imagera](https://imagera.ai/blog/remove-flyaway-hair-from-photo)) **[RESUMEN]**.

Los modelos nuevos ayudan. Qwen documenta que la versión 2512 "renders individual strands with precision" donde la anterior los fundía ([Qwen README](https://github.com/QwenLM/Qwen-Image)) **[OFICIAL]**. El mismo vocabulario aparece en varios idiomas:
- inglés: "stray hairs", "baby hairs", "peach fuzz";
- japonés: 後れ毛 (mechones sueltos) ([note itou](https://note.com/itou_writing/n/n3f6ffa161138));
- coreano: 잔머리 (pelitos sueltos);
- chino: 细小绒毛 (vello fino).

Hay una tensión con la sección 4. La luz dura muestra poros pero apelmaza el pelo. La solución práctica es una luz **direccional pero no plana**, como una ventana lateral o el sol filtrado, en vez de la frontal dura del flash, salvo que el look sea justamente de flash. Dá además la *causa* del estado del pelo ("tied up quickly in a loose bun after the gym, damp strands at the nape"): el contexto causal le da al modelo un look físicamente coherente. Evitá "silky, flowing, voluminous, salon-perfect" en UGC, porque son señales de retoque publicitario.

**Bloques de pelo** (síntesis; **[NO TESTEADO]**):

```
hair with natural, uneven strands: a few flyaways lifting off the crown, fine baby hairs along the hairline and temples, a couple of loose strands touching her cheek and resting on the shoulder, slightly uneven part, soft natural sheen (not glossy), no perfectly sculpted waves
```
Nota: el bloque anti-casco básico.

```
light uneven stubble, slightly patchier on the cheeks than the chin, individual whiskers visible at the jawline; eyebrows with individual hairs, a few going in different directions
```
Nota: barba y cejas de "hombre real". Qwen pide describir el estilo y el arreglo del vello facial ("a neatly trimmed beard, a five o'clock shadow") ([prompt_utils_2512.py](https://github.com/QwenLM/Qwen-Image/blob/main/src/examples/tools/prompt_utils_2512.py)).

Para editar el pelo, nombrá exactamente qué cambia y listá qué queda fijo: nacimiento, raya, largo, color, cara y luz ([Sider](https://sider.ai/blog/ai-tools/how-to-use-chatgpt-prompts-to-nail-professional-ai-headshots-without-looking-like-a-wax-figure)) **[RESUMEN]**.

## 7) Ropa, manos y productos: peso, agarre y etiqueta real

**Ropa.** La ropa delata a la IA cuando no tiene peso (flota, está perfectamente lisa o parece pegada), cuando los accesorios flotan o se funden con el cuerpo, y cuando las estampas traen texto ilegible. OpenAI nombra "fabric wear" y "worn materials" como señales de realismo. Su receta de prueba virtual exige "realistic fit (draping, folds, occlusion) plus consistent lighting/shadows so the outfit looks naturally worn—not pasted on" ([guía gpt-image-1.5](https://github.com/openai/openai-cookbook/blob/main/examples/multimodal/image-gen-1.5-prompting_guide.ipynb)) **[OFICIAL]**. Qwen pide tipo de prenda más textura de tela, y casi todos sus ejemplos cierran con "The image contains no recognizable text" ([prompt_utils_2512.py](https://github.com/QwenLM/Qwen-Image/blob/main/src/examples/tools/prompt_utils_2512.py)). El peso se sugiere con gravedad y pose: "heavy knit sweater sagging at the elbows", "thin linen shirt clinging slightly where she leans on the counter". Para anuncios, el default más seguro es ropa lisa sin marca ("plain, unbranded clothing, no text or logos"): en una sola línea saca el texto ilegible y el riesgo de marca registrada. Para la bijouterie, especificá cantidad y lugar ("one thin gold hoop in each ear, a single simple ring on the left index finger"). Los accesorios flotantes y los aros asimétricos son negativos recurrentes en la comunidad ([YouMind](https://github.com/YouMind-OpenLab/awesome-nano-banana-pro-prompts)).

```
wearing a faded heather-grey cotton t-shirt, slightly stretched at the collar, soft creases across the stomach from sitting, a little lint near the hem; mid-blue denim with natural fading at the thighs and whiskering at the hips; plain fabric with no logos and no printed text
```
Nota: tela con uso, pliegues causados por la pose y sin texto **[NO TESTEADO]**.

**Manos.** En 2026 las manos en reposo casi siempre salen bien. Los errores se concentran en manos que agarran objetos en ángulos raros, manos superpuestas y manos tapadas a medias por pelo o ropa ([WeDetect](https://wedetect.ai/how-to-tell-if-an-image-is-ai-generated)) **[RESUMEN]**. El estudio de Northwestern/Kellogg (CHI 2025) encontró que las implausibilidades *funcionales*, como un sándwich agarrado de costado o un estetoscopio con los auriculares fundidos, son las que la gente detecta **peor** ([Kellogg](https://insight.kellogg.northwestern.edu/article/are-we-any-good-at-spotting-ai-fakes)). Un comprador atento sí las nota. OpenAI recomienda describir framing, mirada e interacciones ("hands naturally gripping the handlebars") ([OpenAI Cookbook](https://github.com/openai/openai-cookbook/blob/main/examples/multimodal/image-gen-models-prompting-guide.ipynb)).

Las poses de bajo riesgo son:
- una sola mano;
- el producto junto a la cara;
- el producto sobre la mesada con la yema de un dedo tocándolo;
- manos abriendo una caja, vistas desde arriba.

Las de alto riesgo son:
- dos manos entrelazadas alrededor de un objeto chico;
- manos cruzando delante de la cara;
- pinzas sobre objetos diminutos, como goteros o anillos.

Describí siempre *por qué* está la mano ahí ("about to unscrew the cap").

```
She holds the [PRODUCT, exact name/label as in reference image 2] in her right hand at chest height, label facing the camera and fully legible, four fingers wrapped around the back of the bottle and thumb resting on the front edge, fingernails short and natural; left hand relaxed out of frame. The product keeps its exact shape, colour, cap and label text from the reference.
```
Nota: agarre con guion y producto atado a su referencia **[NO TESTEADO]**.

**Productos y etiquetas.** Hay tres reglas:
1. **Usá la foto real del producto como referencia.** Nano Banana Pro/2 aceptan 14 imágenes (6 en alta fidelidad), así que entran el packshot y las referencias del avatar juntos ([Gemini cookbook](https://github.com/google-gemini/cookbook/blob/main/quickstarts/Get_Started_Nano_Banana.ipynb)). OpenAI pide "label integrity (text stays sharp and unchanged)" y texto literal entre comillas o en mayúsculas.
2. **No confíes en el texto generado en el producto héroe.** En una prueba de Fstoppers, Nano Banana Pro ganó en sombras y reflejos naturales al insertar productos, y la recomendación fue "handle labels separately in Photoshop" ([Fstoppers](https://fstoppers.com/artificial-intelligence/inserting-products-existing-photos-ai-what-actually-works-901419)) **[RESUMEN]**. La regla del e-commerce chino es la misma: basar los detalles en fotos reales y, si una parte no se ve clara, volver a fotografiarla en vez de dejar que la IA adivine ([DEV](https://dev.to/aioae/shuang-shi-bei-zhan-dian-shang-zhu-tu-ti-shi-ci-he-ji-bai-di-tu-chang-jing-tu-mo-te-shang-shen-ci-zheng-li-55g5)) **[RESUMEN]**.
3. **Separá identidad, look y producto en entradas distintas.** Un hilo de septiembre de 2026 describe el flujo: un JSON de estilo para luz y color, el personaje guardado como referencia en cada generación con "preserve the same facial features", y la foto del producto. Su autor advierte que "the basic colours and grainy look" son de lo que más delata a la IA ([@Mho_23](https://x.com/Mho_23/status/2097483045221917131)) **[1 FUENTE]**.

Antes de componer, conviene tener un packshot limpio. Este prompt es de una colección comunitaria ([ZeroLu §4.2](https://github.com/ZeroLu/awesome-nanobanana-pro)):
```
Cleanly extract the product, completely removing any fingers, hands, or clutter. Background: Place the product on a pure white studio background (RGB 255, 255, 255) with a subtle, natural contact shadow...
```
Nota: genera la referencia limpia del producto, que después se usa dentro de la escena con el avatar.

Las imágenes de antes/después y los claims de salud con avatares IA no se investigaron en estas notas y son de alto riesgo regulatorio. Pasalas siempre por revisión legal.

## 8) Fondo y entorno: el cuarto vivido convence más que la cara

En 2026 el fondo es donde más se "caza" una imagen IA. Los problemas típicos son texto deforme en carteles, etiquetas o lomos de libros; patrones que se repiten (azulejos, ladrillos, rejas); líneas rectas que no continúan detrás de un objeto; y sombras o reflejos que no coinciden con la luz ([WeDetect](https://wedetect.ai/how-to-tell-if-an-image-is-ai-generated); [Optic Flux](https://www.opticflux.com/how-to-spot-an-ai-generated-image-in-2026-the-tells-that-still-work/79504/)) **[RESUMEN]**. La taxonomía de Kellogg incluye las "violaciones de la física" (sombras y reflejos inconsistentes) como una de sus cinco categorías ([Kellogg](https://insight.kellogg.northwestern.edu/article/ai-photos-identification)). Desde la producción, son defectos de calidad que conviene evitar desde el prompt. No son algo para "esconder".

La receta tiene cinco partes:
1. **Un lugar específico y común.** "Regular apartment bathroom", "normal NYC apartment bathroom, not luxury" ([ZeroLu §1.9](https://github.com/ZeroLu/awesome-nanobanana-pro)).
2. **Entre 4 y 7 objetos cotidianos con nombre.**
3. **"Not luxury, not staged".**
4. **Una sola fuente de luz que actúe sobre el sujeto y sobre el cuarto** (la frase de coherencia de la sección 4).
5. **Texto exacto o ninguno.** Qwen cierra casi todos sus ejemplos oficiales con "The image contains no recognizable text". Uno de sus ejemplos de selfie aclara: "Lighting is typical indoor illumination—no staged lighting—and the image resembles a casual iPhone snapshot" ([Qwen README](https://github.com/QwenLM/Qwen-Image)) **[OFICIAL]**.

Sacá de detrás del sujeto la geometría repetitiva y el texto (azulejos, pósters, lomos de libros, carteles), o mandalos fuera de foco. Una guía coreana sugiere describir el fondo "como textura, no como espacio" ([CCFM](https://blog.ccfmedu.co.kr/ai-realistic-portrait-creation)) **[1 FUENTE]**.

**Profundidad de campo.** En UGC "shot on iPhone", un bokeh cremoso contradice la cámara que dice el prompt. La cámara principal de un celular a un brazo de distancia deja la habitación bastante legible. El desenfoque fuerte se lee como modo retrato o como IA. Pedí "background slightly soft but recognisable" y guardá el "85mm f/1.8 shallow depth of field" para looks de cámara profesional. Un creador chino pone "Fake portrait-mode blur" en su lista negativa ([@dotey vía YouMind](https://github.com/YouMind-OpenLab/awesome-nano-banana-pro-prompts)). La comunidad china aporta además un marco útil: **买家秀 vs 卖家秀**, la foto del comprador frente a la del vendedor. Escribí el prompt como si la foto la hubiera sacado un cliente, no la marca ([@hx831126 vía YouMind](https://github.com/YouMind-OpenLab/awesome-gpt-image-2-prompts)).

**Localización LatAm y Brasil.** La única escenografía local concreta en las notas viene de Higor Cruz, un practicante brasileño de TikTok Shop. Su tesis es que el escenario delata más que la cara: "Garrafa d'água em cima da cômoda, carregador enfiado na tomada, toalha jogada, cama meio desfeita, uma plantinha no canto do banheiro". En castellano: botella de agua sobre la cómoda, cargador enchufado, toalla tirada, cama a medio hacer, una plantita en el rincón del baño. Su dormitorio brasileño lleva pared beige, piso laminado claro, cama al fondo, cargador en el enchufe, luz de ventana y formato 9:16. Además, recomienda describir **solo el entorno** y dejar que la foto de referencia defina a la persona, porque describirla de nuevo hace que el modelo invente a otra ([higorprompts](https://higorprompts.substack.com/p/influencer-ia-o-detalhe-idiota-que)) **[RESUMEN/1 FUENTE]**. La idea del "ruido de vida cotidiana" (生活感のノイズ) aparece de forma independiente en Japón ([note そら](https://note.com/sora2_yu0516/n/nfdea80ba8204)).

Hay que cuidar el casting por defecto de las plantillas. Las plantillas es-419 de cocina y smartphone que aparecieron describen mujeres de Asia oriental ([YouMind es-419](https://youmind.com/es-419/prompts/accidental-kitchen-candid-18704)). Un blog coreano reporta que Seedream tiende a rostros asiáticos "refinados" ([Dropshot](https://aistudio.dropshot.io/ko/blog/generated-ai-site-comparison)) **[1 FUENTE]**. Casteá por fototipo Fitzpatrick y subtono más una línea de estilismo plausible para la región (textura de pelo, ropa cotidiana, bijouterie modesta), y delegá la cara al pack de identidad. Armá **bibliotecas de sets por mercado** y validalas con revisores locales. Las notas no traen fuentes sobre utilería mexicana ni argentina, ni sobre qué celulares emular por región; cualquier lista de ese tipo es una hipótesis a testear. En cuentas orgánicas, recordá que Instagram agregó una etiqueta de "perfil generado con IA" para cuentas cuyo protagonista es totalmente sintético. Según la plataforma, las cuentas no etiquetadas de esa categoría pueden ver su alcance limitado ([Notebookcheck ES](https://www.notebookcheck.org/Instagram-persigue-a-los-influencers-generados-por-IA-que-no-admiten-que-son-falsos.1386571.0.html)) **[RESUMEN]**.

```
in her small rented-apartment kitchen in the evening: a few unwashed mugs by the sink, a half-used roll of paper towels, a fridge with two magnets and a takeout menu, a dish towel hanging off the oven handle, warm overhead ceiling light plus cooler daylight from a window on the left; ordinary, slightly messy, not staged, not a showroom. No readable text except the product label.
```
Nota: fondo vivido genérico con luz coherente **[NO TESTEADO]**.

```
Brazilian apartment bedroom: beige painted wall, light laminate floor, bed half-made in the background, phone charger plugged into the wall socket, a water bottle on the dresser, a towel tossed over a chair, soft natural window light, vertical 9:16. Keep the person exactly as in the reference image; do not redescribe or change her face, hair or clothes.
```
Nota: el set de Higor Cruz convertido en bloque de entorno, con la persona delegada a la referencia. La escenografía está citada; la redacción es síntesis **[NO TESTEADO]**.

## 9) Cámara y estética UGC: simulá el dispositivo, no un filtro

Hay elementos que cambian el resultado de forma confiable:
- **la clase de dispositivo**: cámara frontal o trasera del celular, réflex o mirrorless, compacta con flash, descartable, webcam, GoPro;
- **la clase de focal**: 24–26 mm del celular, 35 mm documental, 50 mm natural, 85 mm retrato;
- **la intención de profundidad de campo**: "deep focus" o "shallow DOF";
- **el estado del flash**: "direct on-camera flash" o "available light only";
- **la película**: BFL dice que "Shot on Fujifilm X-T5, 35mm f/1.4" rinde más auténtico que "professional photo" ([BFL guide](https://docs.bfl.ml/guides/prompting_guide_flux2)) **[RESUMEN]**;
- **el procesado**: HDR del celular, compresión JPEG, ruido en sombras.

Los EXIF exactos (1/250 s, ISO 400, EV −0,3) se interpretan de forma laxa, como dice OpenAI. Valen como anclas de coherencia: ISO 100 + f/1.8 + 26 mm le dice al modelo "celular de día", ISO 3200 le dice "noche con ruido". Ninguna fuente mostró diferencia medible entre "iPhone 17 Pro" e "iPhone photo", y OpenAI solo respalda el genérico ([OpenAI Cookbook](https://github.com/openai/openai-cookbook/blob/main/examples/multimodal/image-gen-models-prompting-guide.ipynb)).

El error que más realismo mata es combinar "iPhone selfie" con "85mm, f/1.4, creamy bokeh". La geometría de una selfie a un brazo de distancia (30–50 cm con un gran angular de ~24–26 mm) agranda un poco nariz y frente y toma la cara desde apenas arriba de los ojos. Escribir "held at arm's length, slightly above eye level, mild wide-angle perspective stretch at the frame edges" funciona mejor que nombrar el modelo de teléfono **[NO TESTEADO]**.

Los prompts virales de realismo de 2025–2026 repiten la misma estructura: **[dispositivo + modo] + [quién sostiene la cámara] + [luz despareja o de una fuente práctica nombrada] + [un defecto de composición] + [negación explícita de estudio, pro o lujo] + [lista negativa de piel e identidad]**. Aparece en creadores de habla inglesa, china y japonesa ([JimmyLv](https://github.com/JimmyLv/awesome-nano-banana); [ZeroLu](https://github.com/ZeroLu/awesome-nanobanana-pro); [YouMind](https://github.com/YouMind-OpenLab/awesome-nano-banana-pro-prompts)).

Practicantes rusos agregan artefactos del pipeline del celular: "лёгкий цифровой шум, мягкое JPEG-сжатие… лёгкая микросмазка" (ruido digital leve, compresión JPEG suave, un leve microborroneo) y "слегка заниженная экспозиция" (exposición un poco baja) ([neuroluv](https://neuroluv.ru/prompts/zimniy-strit-realistichnyy-iphone-kadr-108); [prompt1.ru](https://prompt1.ru/listing/prompt-semka-na-iphone/)) **[RESUMEN]**. Los japoneses suman la leve distorsión de gran angular de la cámara frontal y el grano en baja luz ([note petabyte_ai](https://note.com/petabyte_ai/n/n914ab7f03be2)). Las fuentes se contradicen sobre el ruido: una lista rusa lo pone en el negativo ([vc.ru](https://vc.ru/reviews/2681566-prompty-dlya-selfi-2026-luchshie-neyroseti-i-sovety)), y @Mho_23 advierte que el grano genérico también delata. La reconciliación: el grano tiene que corresponder al dispositivo simulado. Usá ruido o JPEG leve en UGC de celular y sacalo en e-commerce limpio o de estudio. La frase de @favprompt lo resume bien: "not a modern image with a retro filter". Hay que simular la captura, no aplicarle un filtro encima ([YouMind No. 7](https://github.com/YouMind-OpenLab/awesome-nano-banana-pro-prompts)).

**Checklist UGC para el prompt** (síntesis de las fuentes citadas):
1. **Verbo de propósito**: "filming a quick review for her followers".
2. **Dispositivo y cámara**: "front camera at arm's length" o "rear camera via mirror".
3. **Geometría**: "slightly above eye level, mild wide-angle stretch".
4. **Foco**: "everything in focus, no portrait-mode blur".
5. **Un defecto de encuadre**: "slightly tilted", "shoulder cut off", "off-centre". Fuentes rusas y japonesas coinciden en que la simetría perfecta y el sujeto centrado delatan ([klerk.ru](https://www.klerk.ru/blogs/oplatymru/680639/); [kanekul](https://kanekul.com/articles/ai-character-shizensa-prompt)).
6. **Movimiento**: "slight motion softness in the hand".
7. **Procesado**: "phone HDR, light sensor noise in shadows, mild JPEG compression".
8. **Desorden**: 3 a 6 objetos concretos.
9. **Piel**: el bloque de la sección 5.
10. **Cláusula de contraste**: "not a studio shoot, no beauty filter, no glamour lighting".

**No te pases de imperfección en un aviso.** El producto tiene que leerse. El motion blur va en manos o fondo, nunca en la etiqueta, y la inclinación se queda en 5° o menos. Para producir, la práctica que más se repite es un prompt base que fija sujeto, lente y luz, más micro-prompts de expresión y gesto, con cinco tomas en paralelo y elegir la mejor ([adlibrary](https://adlibrary.com/guides/ai-prompting-guide-ugc-content-creators)) **[RESUMEN]**. También se usa un contact sheet 3×3 en una sola llamada para conseguir nueve encuadres de la misma persona ([@SheBuildsAI_ vía YouMind](https://github.com/YouMind-OpenLab/awesome-nano-banana-pro-prompts)). En Higgsfield, los presets como "iPhone flash" ya traen "dust, flash, and grain", así que conviene elegir el preset antes y escribir un prompt corto ([Higgsfield](https://higgsfield.ai/blog/Introducing-20-New-Experimental-Presets)).

## 10) Palabras prohibidas y negativos: qué sacar, qué decir en su lugar y dónde funciona un negativo

Los boosters de calidad vienen de la era CLIP y arrastran estética de render: sobrenitidez, saturación, aspecto CG o de póster. OpenAI lo dice en forma oficial ([guía gpt-image-1.5](https://github.com/openai/openai-cookbook/blob/main/examples/multimodal/image-gen-1.5-prompting_guide.ipynb)). Lo confirman fuentes chinas ("deja de apilar 8K / 大师级画质", [Zhihu](https://zhuanlan.zhihu.com/p/2054517785917760150)), coreanas ([CCFM](https://blog.ccfmedu.co.kr/ai-realistic-portrait-creation)) y japonesas ("完成度を下げる", bajar la terminación; [note そら](https://note.com/sora2_yu0516/n/nfdea80ba8204)). Etiquetas de plataforma como "estilo Xiaohongshu / ins风" también producen sobre-embellecimiento ([Peituka](https://peituka.com/blog/avoid-ai-look-realistic-images)) **[RESUMEN]**.

| Prohibido | Por qué | Usá en su lugar |
|---|---|---|
| hyperrealistic, ultra realistic, 매우 사실적 | Se asocia a render 3D y pintura hiperrealista | "photorealistic" (OpenAI), "a real photograph", "candid smartphone photo" |
| 8K, 4K, ultra-detailed, ultra HD, masterpiece, best quality, 고퀄리티 | Sobrenitidez y microdetalle uniforme; posible "piel de escamas" | El parámetro de resolución; "sharp where in focus, natural softness elsewhere" |
| trending on artstation, octane render, unreal engine, CGI, 3D | Estilos de render explícitos | Nada: sacalos |
| cinematic, cinematic lighting, dramatic, volumetric, epic, moody grading | Grading de cine y contraste escenificado | "natural light from [source]", "ordinary phone colours", "natural colour balance" |
| studio lighting, professional photoshoot, glamour, editorial (en UGC) | Pulido de set profesional | "shot by a friend on a phone", "self-recorded", "real home" |
| perfect / flawless / smooth / glowing skin, porcelain, 완벽한 피부, 滑らかで輝く肌 | Activa los priors de filtro de belleza: piel de cera | "natural skin texture, visible pores, slight unevenness, a little shine on the T-zone, no retouching" |
| beautiful, gorgeous, stunning, model-like, perfect symmetry | Producen la "cara IA promedio" | "slightly asymmetrical smile", "ordinary, approachable face", edad y fototipo específicos |
| bokeh everywhere, f/1.2 (en UGC de celular) | Ópticamente imposible para un teléfono | "deep focus phone image" o "slight portrait-mode blur with soft edges" |
| dewy, glass skin (fuera de un brief beauty) | Acabado editorial brilloso | "soft natural highlight on the forehead and nose" |
| subsurface scattering (con cuidado) | Es un término de render 3D y puede tirar a CG | Testealo; mejor "light passes slightly through the ear edges" **[NO TESTEADO]** |

Fuentes: [OpenAI Cookbook](https://github.com/openai/openai-cookbook/blob/main/examples/multimodal/image-gen-models-prompting-guide.ipynb); [Rangy](https://rangy.ai/blog/how-to-prompt-gpt-image-2-with-llm); [pixo](https://pixo.video/ko/blog/gpt-image-fish-scale-fix); [magiccreator-ai](https://github.com/magiccreator-ai/awesome-gpt-image-2-prompts).

**Dónde funciona un prompt negativo:**

| Modelo | ¿Negativo real? | Cómo usarlo |
|---|---|---|
| Qwen-Image-2512 | Sí (true CFG 4,0, 50 pasos) | Lista oficial en chino, abajo **[OFICIAL]** |
| Qwen-Image-2.1 | Sí, pero el camino oficial usa CFG 1 | "Raise it only if you use a negative prompt", a ~2,5–4 ([Comfy docs](https://github.com/Comfy-Org/docs/blob/main/tutorials/image/qwen/qwen-image-2-1.mdx)) |
| Z-Image base | Sí, "strongly recommended" | CFG 3–5, `cfg_normalization=True` para realismo ([Z-Image README](https://github.com/Tongyi-MAI/Z-Image)) **[OFICIAL]** |
| Z-Image Turbo | No (guidance 0) | Todo va en el positivo |
| FLUX.2 / FLUX 3 Klein distilled | No (sin negativos; distilled con CFG 1) | Describí el estado deseado ([Atlabs](https://www.atlabs.ai/blog/flux-2-prompting-guide)) **[RESUMEN]** |
| Krea 2 Turbo | No (CFG apagado) | Positivo **[inferencia]** |
| GPT Image 2 / 2.5 | No hay campo, pero la cola "No…" está avalada | OpenAI cierra su ejemplo con "No glamorization, no heavy retouching." **[OFICIAL]** |
| Nano Banana | No hay campo; exclusiones dentro del texto | Las exclusiones cortas rinden más que las listas largas ([Sider](https://sider.ai/blog/ai-image/best-prompt-structure-for-nano-banana-pro-realism-a-practical-guide)) **[RESUMEN]** |
| Seedream | Sin campo en algunos playgrounds | Exclusión breve dentro del texto |
| Midjourney V8 | `--no` | Comportamiento en V8 no verificado |

**Negativo oficial de Qwen-Image-2512** (copialo literal; [Qwen README](https://github.com/QwenLM/Qwen-Image)):
```
低分辨率，低画质，肢体畸形，手指畸形，画面过饱和，蜡像感，人脸无细节，过度光滑，画面具有AI感。构图混乱。文字模糊，扭曲。
```
Nota: dice "baja resolución, baja calidad, extremidades deformes, dedos deformes, imagen sobresaturada, aspecto de figura de cera, cara sin detalle, demasiado lisa, la imagen tiene sensación de IA; composición caótica; texto borroso y distorsionado". Es la única lista "anti-look IA" publicada por un fabricante.

**Negativo del SOP para Qwen, Z-Image base y pipelines tipo SDXL** **[NO TESTEADO]**:
```
low resolution, low quality, deformed hands, extra fingers, distorted anatomy, oversaturated, waxy skin, plastic skin, airbrushed, beauty filter, poreless skin, over-smoothed, overly sharp, HDR glow, bloom, cinematic color grading, teal and orange, studio backdrop, glamour lighting, CGI, 3D render, illustration, doll-like face, symmetrical perfect face, text, watermark, logo, AI look
```
Nota: en Qwen, usá primero la lista oficial en chino y sumá solo los términos que falten.

**Reformulaciones en positivo para FLUX.2, Nano Banana y Seedream:**

| En vez de | Escribí |
|---|---|
| "no plastic skin" | "natural skin with visible pores, faint redness and fine lines, unretouched" |
| "no bokeh" | "deep focus, background sharp and readable" |
| "no studio" | "in her real cluttered kitchen" |
| "no HDR" | "natural contrast, shadows allowed to go dark" |
| "no cinematic" | "ordinary phone snapshot colours" |
| "no text" | "plain unlabelled surfaces" |

**Colas cortas probadas por sus autores**, para GPT Image y Nano Banana:
- "No glamour lighting, no exaggerated posing, no artificial-looking skin, no extra people" ([@hx831126](https://github.com/YouMind-OpenLab/awesome-gpt-image-2-prompts)).
- "Beauty filters/over-smoothed skin; poreless skin look; Fake portrait-mode blur, CGI/illustration feel" ([@dotey](https://github.com/YouMind-OpenLab/awesome-nano-banana-pro-prompts)).

En castellano circula "No piel falsa. No brillo artificial" ([Luis Garau](https://x.com/luisgarau_/status/2048303817436049524)) **[RESUMEN]**. En ruso, como guarda de edición: "не менять лицо и волосы, не делать кукольную кожу, не размывать веснушки", es decir, no cambiar cara ni pelo, no hacer piel de muñeca, no borrar las pecas ([vc.ru](https://vc.ru/ai/2647149-21-promt-dlya-generatsii-realistichnykh-foto)) **[RESUMEN]**. La práctica japonesa de negativos *específicos de la tarea*, que listan solo lo que no debe cambiar en esa imagen, rinde más que una lista genérica larga ([YouMind JA](https://github.com/YouMind-OpenLab/awesome-gpt-image-2/blob/main/README_ja-JP.md)).

Un conflicto a resolver: el sufijo oficial `positive_magic` de Qwen (", Ultra HD, 4K, cinematic composition.") contradice todo lo anterior. El propio reescritor de Qwen-2512 lo define pero no lo agrega. Para UGC, sacá "cinematic composition" o reemplazalo por "casual smartphone snapshot, natural indoor light" **[NO TESTEADO, A/B]**.

## 11) Anti-degradación: por qué cada corrección empeora la imagen y cómo blindarte

### Por qué pasa: cinco mecanismos que se suman

Lo que el cliente ve (borroso → ruido o texturas raras → piel lavada → corrimiento de color → "parece IA") tiene causas técnicas documentadas:

1. **El cuello de botella del VAE.** Codificar y decodificar la misma imagen con un VAE de difusión latente, sin editar nada, produce artefactos visibles en 5 a 10 ciclos. El VAE pierde alta frecuencia (poros, pelo, trama de tela) y a la vez agrega ruido de alta frecuencia ([REED-VAE, abril 2025](https://arxiv.org/abs/2504.18989)).
2. **Pérdida progresiva de alta frecuencia en ediciones encadenadas.** FLUX.1 Kontext y Qwen-Image mantienen calidad confiable por **unas 5 ediciones seguidas**. Después aparecen deformación del sujeto, sobrenitidez de bordes y colapso de textura, y con 10 o más el deterioro es catastrófico. Si la imagen fuente ya estaba sobreafilada o borrosa, la distorsión aparece desde la tercera edición ([FreqEdit, CVPR 2026](https://arxiv.org/pdf/2512.01755)). BFL muestra un ejemplo propio de falla "after six iterative edits" ([BFL blog](https://bfl.ai/blog/flux-1-kontext); [paper Kontext](https://arxiv.org/pdf/2506.15742)).
3. **El modelo se alimenta de su propia salida imperfecta.** Se entrenó con entradas limpias, así que el error crece en cada vuelta ([EdiVal-Agent](https://arxiv.org/pdf/2509.13399)).
4. **Casi toda edición es una regeneración del cuadro completo.** En el test de 30 ediciones de Artificial Analysis, GPT Image 2.5 Sunburst re-renderizó la mayor parte de la imagen en cada paso, dejando intacto apenas ~1/5. Nano Banana 2.1 mantuvo las ediciones locales, pero el resto se corrió levemente y se fue oscureciendo. Ideogram 4.5 y FLUX 3 dejaron ≥95 % sin tocar en ediciones chicas ([AA en X](https://x.com/ArtificialAnlys/status/2108600224478572767); [AlphaSignal](https://alphasignal.ai/news/artificial-analysis-runs-30-edits-to-expose-how-image-models-drift)). Es una sola foto con una sola secuencia, así que tomalo como ilustrativo y no como benchmark.
5. **Prior de color, deriva geométrica y compresión.**
   - Nano Banana "introduces undesirable global color shifts across editing rounds" ([FreqEdit](https://arxiv.org/pdf/2512.01755)).
   - El amarillo de ChatGPT tiene hasta apodo ([Wikipedia](https://en.wikipedia.org/wiki/Piss_filter)).
   - Qwen-Image-Edit-2509 se desplaza ~8 px por edición porque ComfyUI reescala la referencia a ~1 MP. Con la referencia a tamaño nativo vía `ReferenceLatent` baja a ~1 px ([lilting.ch](https://lilting.ch/en/articles/qwen-image-edit-pixel-perfect-referencelatent); [issue #229](https://github.com/QwenLM/Qwen-Image/issues/229)).
   - En el foro de Google hay reportes de salidas 4K de Nano Banana Pro que parecen 1K y de compresión tipo JPEG ([Google AI forum](https://discuss.ai.google.dev/t/nano-banana-pro-image-quality/134922)).

Hay un agravante. Mi-Ripple bautizó **"digital ripple"** a las grillas, los patrones de panal y las texturas granulosas que dejan las ediciones encadenadas con referencias. Son "inconspicuous in thumbnails", así que se descubren a zoom 100 % cuando ya hay más ediciones apiladas encima ([Mi-Ripple, arXiv 2609.11317](https://arxiv.org/abs/2609.11317)). Y el paper Banana100 mostró que, tras 100 réplicas iterativas con Nano Banana Pro, ninguna de las 21 métricas de calidad sin referencia más usadas (BRISQUE, NIQE y otras) puntuó peor a las imágenes degradadas de forma consistente ([arXiv 2604.03400](https://arxiv.org/pdf/2604.03400)). **El QA automático sin referencia no detecta la deriva.** Hace falta comparar contra el máster y revisar a ojo al 100 %. Un preprint que dice que FreqEdit empeora el rendimiento en ediciones largas se apoya en un "LME-Bench" que no se pudo verificar, así que este informe no lo usa.

### Cómo se comporta cada herramienta al editar

| Herramienta | Qué hace al editar | Degradación conocida | Controles útiles |
|---|---|---|---|
| GPT Image 2.5 Sunburst / Flare | Re-renderiza la mayor parte del cuadro | La deriva más visible en el test de 30 ediciones de AA | Máscara alpha (transparente = editar; en fal es al revés: blanco = editar). En la práctica la máscara funciona como guía y no siempre se respeta su forma ([foro OpenAI](https://community.openai.com/t/gpt-image-1-problems-with-mask-edits/1240639)) **[RESUMEN]**. Omití `input_fidelity` (en 2.5 es inferencia) |
| GPT Image 1 / 1.5 | Igual | — | `input_fidelity="high"` + `quality="high"`. Solo la **primera** imagen recibe la "riqueza extra", así que poné la cara primero y armá un compuesto si hay varias personas ([OpenAI Cookbook](https://cookbook.openai.com/examples/generate_images_with_high_input_fidelity)) |
| Nano Banana Pro / 2.1 | Ediciones semánticas, bastante locales | Corrimiento global de color y oscurecimiento. La identidad aguanta ~8–10 ediciones y después deriva **[RESUMEN, practicantes]** | Volvé a subir la referencia original cada pocos prompts ([UD.hk](https://www.ud.hk/en/blogs/insight/article/2026-06-29-nano-banana-consistent-characters)). En la API multi-turno, devolvé todo el historial y las `thought_signature` sin cambios **[tercero]** |
| Ideogram 4.5 | Copia los píxeles intactos y limita el cambio a la máscara o región | La menor deriva en el test de AA | Máscaras, hasta 4 referencias ([Ideogram](https://ideogram.ai/models/4.5/)) |
| Krea 3 | Ediciones regionales por bounding box | Sin benchmark independiente | 2K en menos de 8 s **[vendor]** ([Krea](https://www.krea.ai/krea-3)) |
| FLUX 3 Image | Edición con "pixel-locked" de lo no cambiado | ≥95 % intacto en ediciones chicas (AA) | Bounding boxes JSON ([TechTimes](https://www.techtimes.com/articles/328502/20261002/black-forest-labs-launches-flux-3-image-json-bounding-boxes-lock-unchanged-pixels-numerically.htm)) |
| FLUX.1 Kontext / FLUX.2 | Regenera el cuadro completo | ~5–6 ediciones | Secuencias cortas y dirigidas |
| Qwen-Image-Edit 2509 / 2511 | Regenera; efecto zoom | ~8 px de corrimiento por pasada con el redimensionado por defecto | `ReferenceLatent` a tamaño nativo; LockPixelQwenEncode; volver a enmascarar el original encima. 2511 dice mitigar la deriva |
| Photoshop Generative Fill (Firefly, Gemini, FLUX.2 pro, Kontext pro) | **Capa nueva limitada a la selección**: el resto queda intacto | Fills de ~1024 px estirados a la selección. La subida a 2048 px **no está verificada** ([Adobe Community](https://community.adobe.com/t5/photoshop-ecosystem-discussions/what-is-the-max-resolution-for-generative-fill-in-photoshop-in-2025/m-p/15417958)) | Selecciones de ≤1024 px o por tiles ([Rangy](https://rangy.ai/blog/photoshop-generative-fill-alternatives)) |
| Midjourney V8.2 | Edit Model | Inpaint u outpaint sobre `--hd` vuelve a resolución estándar ([Legnext](https://legnext.ai/midjourney/v82)) | Editá antes de pedir HD |
| Firefly Image 5 | Edición por prompt | Tope de edición en 2 MP (texto a imagen llega a 4 MP) ([Lustra](https://lustrastudio.co/blog/adobe-firefly-image-model-5-product-photos-4mp-editing)) | — |

### Protocolo de prevención

Es síntesis de las fuentes citadas. Los umbrales son elecciones conservadoras, no especificaciones de los fabricantes:
1. **Generá el máster a la resolución nativa máxima por API**: Nano Banana Pro con `image_size="2K"` o `"4K"`; GPT Image con `quality="high"` (o `xhigh`/`max` en 2.5); FLUX.2 a 4 MP. Siempre en PNG. Los límites de descarga de la app de Gemini están en disputa (1K/2K, y 4K solo en Ultra según una guía; [Workalizer](https://workalizer.com/insights/gemini/gemini-ai-image-resolution-daily-limits-integrating-outputs-into-your-google-file-share-workflow/)), así que no la uses para el máster.
2. **Congelá el máster** (`AVATAR_v000_master.png`, solo lectura) y trabajá sobre una copia TIFF/PSD de 16 bits.
3. **Cada corrección es una rama que sale del máster** o del último compuesto aprobado, con nombre de versión. Nunca sale de la salida cruda anterior.
4. **Un cambio por generación**: ropa, mano, fondo o expresión, nunca varios a la vez.
5. **Preservá por construcción, no por prompt.** Generá el arreglo con cualquier herramienta y traé al máster solo la región cambiada, con máscara calada en la costura y color o curvas igualados a la base. Así los píxeles intactos nunca acumulan pérdida. En ComfyUI, usá Crop & Stitch: el stitch "does not modify the unmasked part of the image, not even passing it through VAE encode and decode". Va con target de 1024 y `InpaintModelConditioning` ([CropAndStitch](https://github.com/lquesada/ComfyUI-Inpaint-CropAndStitch)), más "Color Match (Masked)" para el corrimiento de color ([Acly](https://github.com/Acly/comfyui-inpaint-nodes)).
6. **Presupuesto**: más de 3 regeneraciones seguidas de una zona, o más de 5 ediciones de cuadro completo en una rama, significan reconstruir. Extraé un prompt detallado del compuesto aprobado, cargá el máster original y las referencias de identidad, y usá la versión degradada solo como guía de layout ([creador en TikTok](https://www.tiktok.com/@ai.for.real.life/video/7606747072712248589); Mi-Ripple formaliza la "regeneración desde una referencia limpia").
7. **Entradas limpias**: no edites sobre imágenes sobreafiladas o con filtro, porque se rompen antes (FreqEdit, turno 3).
8. **Color**: medí un neutro (blanco del ojo, prenda blanca, pared gris) en el máster y en cada salida, y corregí con curvas *antes* de componer. Nunca le pidas al modelo que "arregle el color" con otra pasada generativa.
9. **Upscale, grano y sharpen una sola vez, al final**, sobre el compuesto final. Nunca escales versiones intermedias para seguir editándolas.
10. **Usá API en lugar de app** y PNG en lugar de JPEG/WebP. En la API de OpenAI, `output_compression` solo aplica a JPEG/WebP.

### Cómo redactar el prompt de edición

Google lo hace así en su ejemplo oficial: "…while keeping everything else the same" ([Google 7 tips](https://blog.google/products/gemini/prompting-tips-nano-banana-pro/)). Las guías coinciden en cuatro pautas:
- Listá lo que se queda antes de lo que cambia.
- Repetí esa lista en cada pasada.
- Hacé un cambio por mensaje ([fal](https://fal.ai/learn/tools/nano-banana-pro-prompting-guide)).
- Describí solo el cambio, sin redescribir la imagen.

Ninguna redacción frena el re-render del cuadro completo. Lo reduce, nada más.

```
Change ONLY [element] to [precise target]. Keep the person's face, identity, skin texture, expression, hairstyle, pose, body proportions, camera framing, scale and position, lighting direction and color temperature, colors, background and image sharpness exactly the same. Do not retouch, smooth, sharpen or recolor anything else.
```
Nota: plantilla maestra de edición. Incluir "skin texture" y "sharpness" apunta a las dos fallas típicas (colapso de textura y sobrenitidez) **[NO TESTEADO]**.

```
Do not change her face, facial features, skin tone, body shape, pose, or identity in any way. Preserve her exact likeness, expression, hairstyle, and proportions. Match lighting, shadows, and color temperature to the original photo so the change integrates photorealistically, without looking pasted on.
```
Nota: el bloqueo de identidad de OpenAI (de su ejemplo de prueba virtual), adaptado a cualquier cambio **[OFICIAL, adaptado]** ([OpenAI Cookbook](https://github.com/openai/openai-cookbook/blob/main/examples/multimodal/image-gen-models-prompting-guide.ipynb)).

Guardas en otros idiomas que vale la pena copiar:
- japonés: "元画像の人物、衣装、構図、画風をそのまま維持し… 顔のディテールを消したりせず" (mantené persona, vestuario, composición y estilo; no borres el detalle facial);
- coreano: prohibir agrandar ojos, achicar mentón y "embellecer"; evitar HDR, filtro de belleza y nitidez artificial ([@2_dam_e](https://x.com/2_dam_e/status/2106696827307516412));
- japonés: "過度なシャープ化をしない" (sin sobreafilado) ([note creative_edge](https://note.com/creative_edge/n/nc548c6949157)) **[RESUMEN]**.

Sacá de los prompts de edición "high quality", "ultra detail" y "sharpen".

### Escalera de recuperación de un avatar ya degradado

Un upscale no devuelve el detalle que destruyeron las ediciones: hay que re-sintetizarlo. De más fiel a menos fiel:
- (a) Si existe el máster, enmascará la zona defectuosa y rehacela desde el máster.
- (b) Diagnosticá el tipo de artefacto. Las grillas o panales periódicos salen con un notch espectral, que en 14 corridas dejó un residual de apenas 0,08–0,44 unidades L de CIELAB sobre el resto de la imagen. La textura granulosa mezclada con el contenido necesita suavizado estructural o regeneración desde una referencia limpia, que en un ejemplo pareado redujo la densidad de "debris" un 45 % ([Mi-Ripple](https://arxiv.org/abs/2609.11317)).
- (c) Hacé una sola pasada de restauración conservadora: SeedVR2 con corrección de color `lab` y `input_noise_scale` entre 0,1 y 0,3 si hay artefactos a alta resolución ([numz SeedVR2](https://github.com/numz/ComfyUI-SeedVR2_VideoUpscaler)), o Topaz en modo realista.
- (d) Para piel plástica, usá un skin enhancer con ajustes bajos (sección 13) y compuesto **solo sobre la piel**, para que no reinvente ojos, dientes, logos ni ropa.
- (e) Igualá el color contra un neutro con curvas.
- (f) Grano igualado, al final.
- (g) Si la identidad ya derivó, la única vía confiable es regenerar desde el pack de identidad con un prompt nuevo, usando la versión degradada solo como layout.

### Umbrales numéricos

| Dato | Valor | Fuente |
|---|---|---|
| Ediciones confiables (Kontext / Qwen) | ~5; desde el turno 3 si la fuente está sobreafilada o borrosa | [FreqEdit](https://arxiv.org/pdf/2512.01755) |
| Ejemplo de falla de BFL | 6 ediciones | [BFL](https://bfl.ai/blog/flux-1-kontext) |
| Ciclos VAE puros con artefactos visibles | 5–10 | [REED-VAE](https://arxiv.org/abs/2504.18989) |
| MSE-Bench, éxito a 5 turnos | Nano Banana 99,7 → 64,3; GPT Image 1 96,7 → 64 (agregador; verificar) | [SOTA2](https://www.sota2.com/research/sota/multi-turn-image-editing-on-mse-bench) |
| Identidad en Nano Banana | ~8–10 ediciones antes de derivar (practicantes) | [UD.hk](https://www.ud.hk/en/blogs/insight/article/2026-06-29-nano-banana-consistent-characters) |
| Deriva de Qwen-Edit | ~8 px/edición (≈40 px en 5) → ~1 px con referencia nativa | [lilting.ch](https://lilting.ch/en/articles/qwen-image-edit-pixel-perfect-referencelatent) |
| GPT Image 2.5 Sunburst en 30 ediciones | ~1/5 del cuadro intacto | [AlphaSignal](https://alphasignal.ai/news/artificial-analysis-runs-30-edits-to-expose-how-image-models-drift) |
| Regla del SOP | ≤3 regeneraciones por zona; ≤5 de cuadro completo por rama | Inferencia conservadora |
| Fills de Photoshop | ~1024 px por fill (2048 sin verificar) | [Adobe Community](https://community.adobe.com/t5/photoshop-ecosystem-discussions/what-is-the-max-resolution-for-generative-fill-in-photoshop-in-2025/m-p/15417958) |

## 12) Consistencia del avatar: el pack de referencias es el activo, el modelo es reemplazable

Ningún benchmark independiente ordena a los modelos por fidelidad de identidad facial, y las pruebas de blogs se contradicen. Rangy, por ejemplo, encontró que Seedream 5 Pro preservó mejor la cara y el grano que Nano Banana Pro en una restauración ([Rangy](https://rangy.ai/blog/seedream-5-pro-vs-nano-banana-pro-vs-gpt-image-2/)), y un usuario reportó que Nano Banana "no se parecía" a él donde GPT Image 2 sí ([Substack](https://aiblewmymind.substack.com/p/nano-banana-2-vs-gpt-images-2)). Como además los modelos cambian cada trimestre, el SOP se ancla en el **pack de identidad más el descriptor**, no en un modelo.

| Motor | Referencias | Notas |
|---|---|---|
| GPT Image 2 / 2.5 | Hasta 16 **[OFICIAL]** | Un benchmark vio referencias descartadas en silencio (`image_tokens: 0`) que después se corrigieron ([Moe Lueker](https://moelueker.com/blog/gpt-image-2-hairstyle-benchmark-what-it-gets-wrong)). Revisá el uso de tokens en la respuesta |
| Nano Banana Pro / 2 | 14 (6 en alta fidelidad) **[OFICIAL]**; "hasta 5 personas" según el lanzamiento | Según terceros, la fidelidad es mejor con ≤6 referencias **[RESUMEN]** ([Gemini cookbook](https://github.com/google-gemini/cookbook/blob/main/quickstarts/Get_Started_Nano_Banana.ipynb)) |
| Nano Banana 2.1 | 14; 4 personajes + 10 objetos **[secundario]** | Google promete mejor consistencia multi-turno, sin verificación independiente ([Medium](https://medium.com/@dremfind/gemini-nano-banana-2-1-real-fix-for-image-edit-drift-or-a-minor-refresh-1c6de9612e4c)) |
| Seedream 5.0 Pro / Flash | 2–10; Lite / 4.5 / 4.0: 2–14 | [BytePlus ModelArk](https://docs.byteplus.com/en/docs/ModelArk/1541523) **[RESUMEN]** |
| FLUX.2 [pro]/[max]/[flex] | 8 por API / 10 en playground; [dev] ≤6; [klein] ≤4 | Asigná un rol explícito a cada imagen ([BFL Help](https://help.bfl.ai/articles/6944273991-what-are-the-flux-2-technical-specifications)) |
| Qwen-Image-2.1 / Edit-2511 | 10 / 1–3 | **[LICENCIA]** 2.1 es solo para investigación |
| FLUX 3 Image Klein | 10 | **[LICENCIA]** Kommunity |
| Midjourney V8.2 | Edit Model, hasta 4 | `--oref` en V8 corre en V7 sin avisar ([docs](https://docs.midjourney.com/hc/en-us/articles/48495453462797)) |
| Higgsfield Soul ID | Entrenamiento con 20–80 fotos, ~3 min | La ayuda oficial lo plantea para personas reales y deriva los personajes ficticios a AI Influencer Studio o Soul Cast. Otra guía de Higgsfield sugiere entrenarlo con 20+ retratos generados: es un **conflicto, confirmalo con Higgsfield** ([Higgsfield help](https://higgsfield.ai/creator-hub/help-center/ai-models/how-do-i-create-and-use-a-soul-id-character)) |

**El pack de identidad** (síntesis de prácticas de UD.hk, Quest Studio y SelfieLab):
1. Un retrato héroe frontal, con expresión neutra, luz suave y pareja, fondo gris y 2K o más.
2. Vistas de frente, 3/4 izquierda, 3/4 derecha y perfil, con la misma luz.
3. Un cuerpo entero en postura neutra.
4. Un macro de piel con el mapa de pecas y lunares.
5. Dos o tres expresiones: sonrisa con dientes, neutra, hablando.

El fondo va "plain neutral grey" porque un fondo cargado se lee como parte del personaje ([Quest Studio](https://queststudio.io/blog/ai-character-turnaround-sheet)) **[RESUMEN]**. La luz pareja importa doble: evita que la iluminación quede leída como rasgo de identidad, tanto por los modelos de referencia como por cualquier LoRA que se entrene después.

**El descriptor** es corto e idéntico en cada prompt. Lleva como máximo 3 o 4 marcadores duros: color de ojos, posición de un lunar, forma del nacimiento del pelo o de las cejas, alguna cicatriz. La ropa y la luz no van en el descriptor sino en el bloque de escena, para que no se "horneen" en la identidad ([UD.hk](https://www.ud.hk/en/blogs/insight/article/2026-06-29-nano-banana-consistent-characters)). La práctica que más se repite es **abrir y cerrar con el bloqueo de identidad**: fijar la cara al principio, cambiar solo la escena en el medio y repetir el bloqueo al final. Cada referencia recibe un rol único, como "Use Image 1 only to preserve the character's face, hairline, and hair texture", y se aclara que no hay que tomar rasgos de identidad de las referencias de estilo ([Image3.org](https://image3.org/blog/gpt-image-2-character-sheet-prompts)) **[RESUMEN]**. En Nano Banana conviene volver a subir el héroe cada 8–10 turnos.

**Un camino limpio para crear caras 100 % ficticias** es el "실사화 / 実写化", atestiguado en dos idiomas: primero se diseña el personaje como ilustración o hoja de personaje y después se "fotorrealiza" con un prompt de bloqueo de identidad ([@2_dam_e](https://x.com/2_dam_e/status/2106696827307516412); [note aliphyca](https://note.com/aliphyca/n/nf2545df936ea)). Igual hacé un control de originalidad (abajo).

### LoRA: cuándo conviene y con qué ajustes

Un LoRA conviene en tres casos: cuando el volumen pasa de ~100 imágenes por mes por avatar, cuando necesitás correr en modelos abiertos o ComfyUI, o cuando tenés que ganarle a la deriva multi-turno de los métodos por referencia. Para campañas chicas, el pack sin entrenamiento es más rápido y evita el riesgo de luz "horneada".

| Base | Licencia | Rank | LR | Pasos | Dataset | Fuente |
|---|---|---|---|---|---|---|
| FLUX.2 [klein] 4B / 9B | 4B Apache 2.0; **9B no comercial** | — | 8e-5 a 1e-4 | 1.500–3.000 | — (9B pide 22 GB de VRAM) | [BFL klein training](https://docs.bfl.ml/flux_2/flux2_klein_training) **[RESUMEN]** |
| FLUX.2 [dev] | **No comercial** sin licencia BFL | 32 (8–16 si falta VRAM) | 1e-4 | 1.000–3.000 | 20–60+ a 1024 | [RunComfy](https://www.runcomfy.com/trainer/ai-toolkit/flux-2-dev-lora-training) |
| Z-Image Turbo (con adapter v2) | Verificar | 8–32 | 1e-4 (bajar a 5e-5 si se "pasa") | 1.500–3.000 | 10–30; caption de pose y ropa, no de la cara | [RunComfy](https://www.runcomfy.com/trainer/ai-toolkit/z-image-turbo-lora-training); [HF blog](https://huggingface.co/blog/content-and-code/training-a-lora-for-z-image-turbo) |
| Qwen-Image 2512 / 2.1 | 2512: verificar; **2.1 solo investigación** | 16 (alpha 16) | 1e-4 | ~2.000 | 20–30 como mínimo, rendimiento decreciente desde ~50; batch 1 | [note.com](https://note.com/sepiablue/n/n9372886b9e5d?hl=en) |
| Krea 2 (se entrena en RAW y se corre en Turbo) | Community License; licencia comercial a pedido | 16–32 | 1e-4 a 2e-4 | 2.000–2.500 (parecido logrado a los 600–900 en un trainer) | 40–80 | [rkrra](https://rkrra.com/guides/krea-2-lora-training/); [Krea 2 README](https://github.com/krea-ai/krea-2/blob/main/README.md) |

**Receta del SOP** **[NO TESTEADO]**:
1. Generá 40–60 candidatas desde el pack con Nano Banana Pro o GPT Image 2.5.
2. Filtrá hasta quedarte con 25–40 que pasen el QA facial.
3. Variá ropa, lugar, luz y focal en cada imagen, para que solo la cara quede constante. Si el mismo pelo plateado aparece en las 28 imágenes, "became part of the character" ([ai-muninn](https://ai-muninn.com/en/blog/character-lora-control-panel-wan22)).
4. Escribí captions de escena, ropa y luz, nunca de la cara.
5. Entrená con batch 1 y guardá checkpoints cada 250 pasos.
6. Quedate con el **checkpoint más temprano que pase el umbral de identidad**, que es el que conserva más flexibilidad y realismo de piel.

Los LoRAs de destilación tipo "lightning" o turbo cambian textura por velocidad, y la piel sale "plastic and CG-like": usalos para borradores. Las herramientas de dataset sintético como LoRA-Dataset-Forge dependen de `gemini-3.1-flash-image-preview`, deprecado y sin fecha de apagado, así que conviene migrarlas a Nano Banana 2.1 o Pro ([LoRA-Dataset-Forge](https://github.com/IxMxAMAR/LoRA-Dataset-Forge); [deprecations](https://ai.google.dev/gemini-api/docs/deprecations)).

### Face swap: capa de retoque final, nunca el método base

FaceFusion usa hoy por defecto `hyperswap_1a_256`, y su "pixel boost" interno llega a 512, 768 o 1024 px ([FaceFusion docs](https://docs.facefusion.io/usage/cli-arguments/processors/face-swapper)). `inswapper_128` recorta la cara a 128 px: alcanza para web pero "noticeable at 4K" ([WaveSpeed](https://wavespeed.ai/blog/posts/open-source-face-swap-software/)). **[LICENCIA]** El código de InsightFace es MIT, pero los paquetes preentrenados (buffalo_l, antelopev2) y el uso comercial de inswapper_128 son "for non-commercial research purposes only" sin licencia paga ([InsightFace README](https://github.com/deepinsight/insightface/blob/master/python-package/README.md)). Los adaptadores sobre FLUX.1 [dev], como PuLID-Flux o InfiniteYou, heredan su licencia no comercial y arrastran problemas de realismo: aspecto CG y "copy-paste face". Usá HyperSwap a 512 px o más, o un inpaint con FLUX.2 o LoRA, **solo sobre los renders de tu propio avatar sintético que fallen el umbral**, con la licencia en regla. Quedan como legado IP-Adapter FaceID, InstantID (SDXL), PuLID-SDXL e inswapper_128 como default.

### QA de identidad con ArcFace

No existe un umbral universal de "misma persona". Los puntos de operación publicados son:
- **~0,356** a una tasa de falso match de 1 en 10.000 ([arXiv 2503.20108](https://arxiv.org/pdf/2503.20108));
- **~0,5** como regla práctica ([Zenn](https://zenn.dev/taku_sid/articles/20250511_face_sim_metric?locale=en));
- **0,6** como "conventional threshold" ([arXiv 2505.23462](https://arxiv.org/pdf/2505.23462));
- **<0,3** para "otra persona" ([Arc2Face](https://www.ecva.net/papers/eccv_2024/papers_ECCV/papers/05442.pdf)).

Los adaptadores rondan ~0,65–0,79. La similitud además baja con la pose.

**Protocolo** **[NO TESTEADO]**:
1. Calculá los embeddings del héroe y de las 4–5 vistas del pack y promediá un "centroide".
2. Para cada render, medí el coseno contra el centroide y contra la vista de pose más cercana.
3. En planos casi frontales: pasa automático con ≥0,60, va a revisión humana entre 0,45 y 0,60, se rechaza debajo de 0,45. Bajá los umbrales 0,05–0,10 para perfiles o expresiones extremas.
4. Seguí la media, el mínimo y el desvío por campaña. Si la media baja, re-anclá o pasá al LoRA.
5. Sumá un segundo eje de realismo y textura con revisión humana, porque un swap puede subir el ArcFace y bajar el realismo.
6. **Control de originalidad al diseñar**: verificá que el avatar quede por debajo de ~0,3 contra cualquier base de caras reales a la que tengas acceso, para no parecerte por accidente a una persona existente.
7. Usá un modelo de reconocimiento facial con licencia comercial, no el buffalo_l por defecto.

**Versionado:** por cada asset, guardá el pack, el descriptor, el modelo y su versión, la semilla, los puntajes de QA y el manifiesto C2PA. Revalidá todo cuando un modelo se retire.

## 13) Upscale y post-proceso: conservador primero, piel enmascarada después, grano al final, y etiqueta siempre

### Herramientas: fidelidad contra reinvención

Las herramientas se dividen en dos familias:
- **Conservadoras**: SeedVR2, Topaz Gigapixel Redefine *Realistic*, Magnific Precision v2 (flavor *photo*), Krea a 2x con fuerza baja, LetsEnhance Prime.
- **Generativas**: Magnific Creative con Creativity y HDR altos, Topaz Bloom, Redefine *Creative* alto, upscalers tipo Clarity. Agregan más textura, pero corren la cara y producen la "Magnific face" plástica ([Vantaige](https://vantaige.io/ai-tool/magnific); [AIarty](https://www.aiarty.com/ai-image-enhancer/topaz-bloom.htm)).

Un probador de Topaz Bloom en creatividad mínima vio que los ojos se abrían y concluyó "not the same person". Para un avatar recurrente, el consenso es escalar de forma conservadora y agregar textura con una herramienta de piel separada, a baja intensidad ([ComfyUI docs](https://docs.comfy.org/tutorials/utility/image-upscale)). En 2026 Freepik pasó a llamarse **Magnific** (28/4/2026), así que "Freepik Skin Enhancer" y "Magnific Skin Enhancer" son el mismo producto ([Wikipedia](https://en.wikipedia.org/wiki/Magnific)). Topaz Gigapixel v1.3.0 (13/5/2026) trae **Recover Faces 3**, sin el tope de 512×512 y sin los puntitos de v2 ([Topaz](https://community.topazlabs.com/t/topaz-gigapixel-v1-3-0-recover-faces-3-300-speed-up-for-neuroserver-models/102815)).

| Herramienta | Modo | Ajustes de partida | Riesgo |
|---|---|---|---|
| Magnific Precision v2 | Flavor `photo` (retrato y editorial) | Defaults de la API: sharpen 7, smart_grain 7, ultra_detail 30 ([API](https://docs.magnific.com/api-reference/image-upscaler-precision-v2/post-image-upscaler-precision-v2)) **[OFICIAL]**. En caras, sharpen 0–5 y ultra detail 15–30 **[inferencia]** | Poros algo exagerados en primeros planos ([Curious Refuge](https://curiousrefuge.com/blog/magnific-ai-image-upscaler-review)) |
| Magnific Skin Enhancer | `faithful` | Skin detail con default 80 (bajalo a medio), sharpen 0, grain 0–5. En `flexible`, el ejemplo oficial usa sharpen 0, smart_grain 2, preset `enhance_skin` ([API](https://docs.magnific.com/api-reference/skin-enhancer/post-flexible); [Comfy node](https://docs.comfy.org/ko/built-in-nodes/MagnificImageSkinEnhancerNode)) | Sobrecorregir. Magnific dice "improve, don't erase" |
| Magnific Creative | Preset Soft Portraits | Creativity baja (0–3), Resemblance alta, HDR ≈0. El ejemplo viejo (creativity 3, HDR 0, resemblance −1) usa otra escala | HDR alto = manchas y piel de plástico |
| Topaz Gigapixel | Redefine Realistic (Subtle) | Para imágenes IA de 1024² ([media.io](https://www.media.io/comparison/topaz-labs-image-upscaler-review.html)). Creative solo en niveles 1–3, porque "la fantasía empieza entre el 3 y el 4" ([DPReview](https://www.dpreview.com/forums/threads/topaz-bloom.4806341/)); texture ≤5 solo en zonas | Recover Faces 3 "may include subtle changes to expressions" ([Topaz docs](https://developer.topazlabs.com/image-models/gigapixel/face-recovery-3)). Usalo solo si la cara está blanda |
| Krea Enhancer | 2x | Strength baja, Resemblance alta, Face Creativity baja. 1x si solo hace falta claridad ([Krea docs](https://www.krea.ai/docs/user-guide/features/enhancer); [Krea blog](https://www.krea.ai/blog/best-ai-image-upscalers-in-2026)) | Multiplicadores altos = más invención |
| SeedVR2 (ComfyUI) | 3B alisa, 7B da detalle | Bajá la entrada a ~0,35 MP; probá a 2K antes de 4K; color `lab`; `input_noise_scale` 0,1–0,3; `latent_noise_scale` 0,05–0,15; tile 1024 / overlap 128; batch 1 ([numz](https://github.com/numz/ComfyUI-SeedVR2_VideoUpscaler)) | Las variantes "sharp" pueden poner la piel "plasticky or scaly". Hacé después una pasada ADetailer ([comfy.icu](https://comfy.icu/node/SeedVR2)) |
| Ultimate SD Upscale / Flux tile | Tiles | Denoise 0,2–0,3 limpia; 0,35–0,45 agrega detalle; ≥0,5 corre caras. Padding 32–64; 4x-UltraSharp ([ComfyLab](https://comfylab.dev/blog/workflows/comfyui-upscale-workflow-ultimate-sd-upscale/)) | — |
| FaceDetailer / ADetailer | Antes del upscale | Denoise ~0,35–0,45. "Upscaling a bad face scales the badness" | — |
| Enhancor | Skin Fix | Skin Realism Level con default 0,10; Freckle Control bajo o apagado en caras de marca ([Enhancor](https://www.enhancor.ai/)) | Heavy Mode puede alterar la estructura facial |
| Higgsfield Skin Enhancer | Sutil | Evitá el preset "Imperfect Skin", que agrega granos de más ([Creative Pad](https://www.creativepadmedia.com/make-ai-skin-realistic-with-1-click-higgsfield-skin-enhancer/)) | — |

Un editorial considera a Enhancor el más conservador con identidad y geometría, y a Magnific Creative el más agresivo ([Chase Jarvis](https://chasejarvis.com/blog/best-ai-image-upscaler/)) **[1 FUENTE]**. Re-renderizar en 4K con Nano Banana Pro sobreafiló los poros en una prueba, mientras que escalar desde 1080p dejó artefactos tipo "cierre" en las luces fuera de foco ([WaveSpeed](https://wavespeed.ai/blog/posts/blog-nano-banana-pro-4k-output-settings/)) **[1 FUENTE]**. Probá las dos vías con tu avatar.

**Escala y tamaño de entrega.** Escalá 2x + 2x en vez de un salto de 4x, y revisá la cara al 100 % entre pasos. Según resúmenes de terceros, Meta pide 1440×1800 (4:5), 1440×1440 (1:1) y 1440×2560 (9:16), JPG o PNG de hasta 30 MB ([AdsUploader](https://adsuploader.com/blog/meta-ads-aspect-ratios)) **[RESUMEN]**. Un máster de 2880–4096 px en el lado largo sobra. Ir a 8K suma riesgo (poros exagerados, piel con escamas) sin beneficio visible después de la recompresión de la plataforma.

### Cadena de terminación (orden y números)

1. **Arreglo de anatomía y cara** a la resolución base: ojos, dientes, manos, orejas, bijouterie.
2. **Relight opcional** (Magnific Relight con `light_transfer_strength` bajo). Puede cambiar caras chicas o grupos ([The Decoder](https://the-decoder.com/magnific-ais-relight-uses-prompts-to-transform-image-lighting-and-backgrounds/)).
3. **Harmonize** para el producto compuesto. Funciona solo en capas de píxeles y está disponible desde Photoshop 27.0 según la comunidad de Adobe ([Adobe Community](https://community.adobe.com/featured-content-765/harmonize-effortless-object-blending-across-any-background-anytime-anywhere-1546663)). Para fundir un fill, usá Curves recortada y un ajuste global al 10–15 % ([ImageWork](https://imageworkindia.com/match-color-generative-fill-lighting-gaps/)).
4. **Upscale 2x conservador.**
5. **Pasada de piel enmascarada solo a la piel**, sin ojos, labios ni nacimiento del pelo, fundida con opacidad parcial y comparada con el héroe.
6. **Retoque**: pincel corrector y tampón; separación de frecuencias para manchas de color sin tocar la textura.
7. **Grade**: curva suave, saturación natural, balance de blancos apenas imperfecto, y nada de Clarity, Dehaze o Texture altos sobre la piel.
8. **Sharpen para el tamaño de salida**: Amount 60, Radius 1,0, Detail 20–30 en retratos y Masking ≥40, previsualizando la máscara con Alt ([RevelRaw](https://revelraw.com/blog/camera-raw-sharpening.html); [Envato](https://photography.tutsplus.com/tutorials/adobe-camera-raw-for-beginners-the-detail-tool--photo-2767)). En Photoshop, Smart Sharpen con "Lens Blur".
9. **Grano al final**, monocromo porque el speckle de color se lee como ruido de sensor: Amount 18–25, Size 24–30, Roughness 45–52, o 1–3 % de ruido. Más suave sobre la piel y más en los medios tonos ([Legendary Presets](https://legendarypresets.com/realistic-film-grain-without-losing-detail/); [RAWCraft](https://rawcraft.app/guides/add-film-grain-iphone-photos)).
10. **Aberración cromática solo en bordes de alto contraste y viñeta suave.** Si falta del todo la aberración, también se nota ([nat.io](https://nat.io/blog/achieving-photorealism-guide)) **[RESUMEN]**.
11. **Export**: máster PNG/TIFF y entrega en sRGB, JPEG de alta calidad o WebP. Revisá al 100 %. No hace falta "pre-degradar" a un JPEG de baja calidad, porque Meta y TikTok vuelven a codificar todo.

Ninguna fuente dio valores numéricos para aberración cromática, distorsión, desenfoque de movimiento, offset de balance de blancos ni calidad JPEG de entrega. Esos ajustes se calibran a ojo.

### Procedencia: C2PA y SynthID como cumplimiento

Las imágenes de Nano Banana Pro y Nano Banana 2 llevan C2PA Content Credentials y la marca de agua SynthID ([Google blog](https://blog.google/innovation-and-ai/technology/ai/nano-banana-2/)). Las de GPT Image 2.5 llevan C2PA ([Unite.AI](https://www.unite.ai/openai-releases-chatgpt-images-2-5-with-sketch-and-two-new-api-models/)). Que OpenAI use SynthID es una afirmación **sin verificar**. Una captura de pantalla pierde el C2PA, mientras que SynthID vive en los píxeles y resiste JPEG, redimensionado y recorte ([c2paviewer](https://c2paviewer.com/articles/verify-ai-generated-image-c2pa-synthid)). El post-proceso generativo pesado puede debilitar o desincronizar estas señales, pero **eso no elimina ninguna obligación legal**: según las guías de la Comisión Europea, la agencia que usa la herramienta es "deployer" y no puede apoyarse en la marca de agua de la herramienta ([McCann FitzGerald](https://www.mccannfitzgerald.com/knowledge/data-privacy-and-cyber-risk/ai-transparency-european-commissions-guidelines-on-article-50-part-2-deployer-obligations)). La política del SOP es conservar el manifiesto C2PA en los másteres para auditoría, no despojar metadatos y agregar la divulgación propia en el paso de export. Que Lightroom o Photoshop preserven el C2PA al exportar no está verificado en las notas: comprobalo en tu pipeline.

### Cumplimiento: lo que no se negocia en un negocio comercial

- **EE. UU., FTC 16 CFR Part 465.** La regla final se publicó en 89 FR 68034 (22/8/2024) y rige desde el 21/10/2024 ([Federal Register](https://www.govinfo.gov/content/pkg/FR-2024-08-22/html/2024-18519.htm); [Cornell LII](https://www.law.cornell.edu/cfr/text/16/part-465)). Prohíbe reseñas y testimonios falsos; los comentaristas aclaran que eso incluye los generados por IA ([DLA Piper](https://www.dlapiper.com/en/insights/publications/2026/07/ftcs-2026-enforcement-approach-to-fake-reviews-takes-shape-takeaways-for-companies)). La multa civil máxima sigue en **USD 53.088 por infracción**: no hubo ajuste por inflación en 2026 ([Federal Register 2025](https://www.govinfo.gov/content/pkg/FR-2025-01-17/html/2025-01361.htm); [aviso 2026](https://public-inspection.federalregister.gov/2026-18853.pdf)). El caso **TruHeight** muestra que la regla se aplica: la denuncia de abril de 2026 incluía reseñas escritas por empleados e incentivadas, y la orden final del **14/7/2026** fijó una sentencia de USD 4M suspendida a USD 750.000 ([FTC](https://www.ftc.gov/news-events/news/press-releases/2026/07/ftc-approves-final-order-against-truheight-deceptive-unsubstantiated-advertising-supplements-kids)). Una foto de "cliente" sintético junto a texto de reseña es el uso de mayor riesgo. Confirmá la redacción exacta de 465.2 con un abogado.
- **UE, AI Act Art. 50.** Rige desde el **2/8/2026** para el 50(2), el 50(4) y el 50(5) ([Orrick](https://www.orrick.com/en/Insights/2026/08/EU-AI-Act-Transparency-Obligations-for-AI-Generated-Content-Article-50)). El AI Omnibus da a los sistemas generativos que ya estaban en el mercado hasta el **2/12/2026** para el marcado del 50(2) ([William Fry](https://www.williamfry.com/knowledge/eu-ai-act-omnibus-deal-reached-postponed-deadlines-watermarking-compromise-and-the-nudificiation-prohibition/)); su publicación en el Diario Oficial no está confirmada. El Código de Práctica final (10/6/2026) pide a los proveedores al menos dos capas de marcado legibles por máquina, y a los deployers etiquetas "immediately recognisable" con un set opcional de íconos UE ([Jones Day](https://www.jonesday.com/en/insights/2026/06/european-commission-publishes-final-code-of-practice-on-marking-and-labelling-aigenerated-content); [Bird & Bird](https://www.twobirds.com/en/insights/2026/taking-the-eu-ai-act-to-practice-the-final-transparency-code-of-practice)). Un deployer de fuera de la UE también queda alcanzado si es previsible que el contenido se use en la UE. La definición de deepfake del Art. 3(60) habla de parecido con "existing persons…": si una persona inventada entra o no está en debate. **La lectura conservadora es etiquetar.**
- **Meta.** En anuncios políticos y sociales es obligatorio declarar imágenes fotorrealistas creadas o alteradas, incluida "a realistic person who doesn't exist". En anuncios comerciales, Meta aplica "AI info" en sus propias herramientas y, desde junio de 2026, detectaría IA de terceros por señales de la industria ([Digital Applied](https://www.digitalapplied.com/blog/ai-content-labeling-rules-advertisers-2026-reference)) **[RESUMEN]**. Que exista una obligación general para todos los anuncios está **en disputa** ([AdRiseLab](https://adriselab.com/blog/meta-ads-ai-disclosure-rules-2026)).
- **TikTok.** Los anuncios con contenido IA realista llevan la etiqueta AIGC o un disclaimer propio. En los anuncios que no son Spark, se activa el toggle "This ad contains AI-generated content" ([Cinerads](https://www.cinerads.com/blog/tiktok-ai-content-policy); [Novoads](https://novoads.ai/en/blog/ai-ad-label-rules-2026)) **[RESUMEN]**. En TikTok Shop la etiqueta tiene que ser idéntica en el anuncio y en la ficha.
- **España.** El 26/5/2026 el Consejo de Ministros aprobó el **proyecto** de Ley Orgánica para el buen uso y la gobernanza de la IA y lo envió a las Cortes. Prevé multas de €6.000 a €35M y supervisión de AESIA, y exige identificar los deepfakes como contenido generado o alterado con IA. **Todavía no es ley** ([La Moncloa](https://www.lamoncloa.gob.es/consejodeministros/resumenes/Paginas/2026/260526-rueda-prensa-ministros.aspx); [Cuatrecasas](https://www.cuatrecasas.com/es/spain/propiedad-intelectual/art/proyecto-ley-organica-buen-uso-gobernanza-ia); [Infobae](https://www.infobae.com/espana/2026/05/26/el-gobierno-aprueba-la-ley-de-ia-multas-de-hasta-35-millones-prohibicion-de-los-deepfakes-sexuales-y-mas-control-sobre-contenidos-manipulados/)).
- **Brasil.** El PL 2338/2023 sigue pendiente en la Cámara de Diputados, con multas previstas de hasta el 2 % de la facturación y un tope de R$50M por infracción ([CASRAI](https://casrai.org/guides/brazil-ai-bill-pl-2338-status)). No se investigaron CONAR ni las normas del resto de LatAm.

**Protocolo de cumplimiento en el export**:
1. Etiqueta visible ("Imagen generada con IA" o el ícono UE).
2. Toggles de plataforma activados (TikTok AIGC; Meta donde corresponda).
3. Ninguna afirmación de que el avatar es un cliente real, ninguna reseña fabricada y ninguna credencial profesional inventada.
4. Revisión legal de claims de salud y de antes/después.
5. C2PA intacto y un log por asset.

## 14) Biblioteca de prompts plantilla: lo probado por sus autores y lo sintetizado para el SOP

La biblioteca tiene dos niveles de confianza:
- **[PROBADO POR LA FUENTE]**: prompts textuales y acreditados. Su autor los publicó con resultados, pero **no fueron re-renderizados para este informe**.
- **[SÍNTESIS NO TESTEADA]**: prompts armados con los principios citados. Hay que pasarlos por un A/B por modelo antes de codificarlos.

Reemplazá siempre a cualquier persona real por un sujeto ficticio y respetá las notas de cumplimiento.

### A. Probados por la fuente (textuales)

**A1. Línea base oficial de OpenAI (gpt-image-2)** **[PROBADO POR LA FUENTE, OFICIAL]** — [OpenAI Cookbook](https://github.com/openai/openai-cookbook/blob/main/examples/multimodal/image-gen-models-prompting-guide.ipynb)
```
Create a photorealistic candid photograph of an elderly sailor standing on a small fishing boat.
He has weathered skin with visible wrinkles, pores, and sun texture, and a few faded traditional sailor tattoos on his arms.
He is calmly adjusting a net while his dog sits nearby on the deck. Shot like a 35mm film photograph, medium close-up at eye level, using a 50mm lens.
Soft coastal daylight, shallow depth of field, subtle film grain, natural color balance.
The image should feel honest and unposed, with real skin texture, worn materials, and everyday detail. No glamorization, no heavy retouching.
```
Nota: el esqueleto de referencia, en el orden escena → sujeto → textura → cámara → luz → cola de exclusiones. Copiá la estructura, no el marinero.

**A2. Selfie de vacaciones, @PurzBeats (GPT Image 2)** **[PROBADO POR LA FUENTE]** — [magiccreator-ai](https://github.com/magiccreator-ai/awesome-gpt-image-2-prompts)
```
Create a realistic close-up vacation selfie of a heavyset middle-aged man with short gray hair and a gray beard, making an excited wide-eyed expression from a hotel balcony in Hawaii. Show palm trees, high-rise buildings, blue sky, and bright daylight in the background. Make it feel like an authentic phone selfie.
```
Nota: muestra que un prompt corto con un sujeto "común" y la frase "authentic phone selfie" ya sale del look de modelo publicitario.

**A3. Flash en la puerta, @WolfRiccardo (GPT Image 2)** **[PROBADO POR LA FUENTE]** — [magiccreator-ai](https://github.com/magiccreator-ai/awesome-gpt-image-2-prompts)
```
A candid apartment doorway photo of a young woman in a simple black dress holding a small decorated birthday cake, shot with direct flash, realistic skin texture, casual home lighting, slightly messy interior, authentic smartphone photo look.
```
Nota: es la fórmula mínima: flash directo, interior desordenado y "smartphone photo look".

**A4. "Selfie extremadamente común", @jiamimaodashu** **[PROBADO POR LA FUENTE]** — [JimmyLv Case 54](https://github.com/JimmyLv/awesome-nano-banana)
```
Please draw an extremely ordinary and unremarkable iPhone selfie, with no clear subject or sense of composition — just like a random snapshot taken casually. The photo should include slight motion blur, with uneven lighting caused by sunlight or indoor lights resulting in mild overexposure. The angle is awkward, the composition is messy, and the overall aesthetic is deliberately plain — as if it was accidentally taken while pulling the phone out of a pocket.
```
Nota: es de los prompts de realismo más copiados. El original nombraba a dos celebridades en la segunda línea: **reemplazalas siempre por tu avatar ficticio**. Para anuncios, bajá el "messy" para que el producto se lea.

**A5. Supermercado "buyer-show", @hx831126 (GPT Image 2, 8/9/2026; extracto)** **[PROBADO POR LA FUENTE]** — [YouMind GPT Image 2](https://github.com/YouMind-OpenLab/awesome-gpt-image-2-prompts)
```
Create a realistic vertical smartphone photo of a candid grocery-store shopping moment in a Korean supermarket. [...] The scene contains exactly one main shopper, one black basket, two background shoppers, one shopping cart in the background [...] Use a natural consumer-phone snapshot style, slightly imperfect framing, realistic indoor fluorescent lighting, mild motion softness, neutral colors, glossy gray supermarket floor reflections, deep aisle perspective, and authentic everyday details. Make it look like a casual buyer-show or store social media photo rather than a studio fashion shoot. No glamour lighting, no exaggerated posing, no artificial-looking skin, no extra people, no watermark.
```
Nota: tiene dos trucos: contar cada objeto y usar el marco "buyer-show" (la foto del cliente, no la del vendedor).

**A6. Ficha de cámara de celular, @dotey (Nano Banana Pro; bloques de luz, cámara y negativos)** **[PROBADO POR LA FUENTE]** — [YouMind NB Pro](https://github.com/YouMind-OpenLab/awesome-nano-banana-pro-prompts)
```
### Lighting
* Light source: daylight coming from a large window on the left side of the camera, through sheer curtains
* Light quality: soft, diffused light
* White balance (K): 5200
### Camera
* Mode: smartphone rear camera shooting via the mirror (no portrait/bokeh mode)
* Equivalent focal length (mm): 26
* Distances (m): Subject to mirror: 0.6 / Camera to mirror: 0.5
* Exposure: Aperture (f): 1.8 / ISO: 100 / Shutter speed (s): 0.01 / Exposure compensation (EV): -0.3
* Depth of field: natural smartphone deep depth of field; background clearly visible with no artificial blur
* Composition note: keep the subject centered; to avoid wide-angle edge distortion, have her stand a bit further away and crop to a square later.
### Negative prompts
* Beauty filters/over-smoothed skin; poreless skin look
* Exaggerated or distorted anatomy
* Logos, brand names, or readable user interface text
* Fake portrait-mode blur, CGI/illustration feel
```
Nota: el ejemplo más claro de "describí el teléfono real, no una réflex". Reutilizá solo estos bloques, porque el bloque de sujeto original no es apto para marca.

**A7. Espejo de baño "NOT professional", @gaucheai (Nano Banana Pro; bloque fotográfico)** **[PROBADO POR LA FUENTE]** — [ZeroLu §1.9](https://github.com/ZeroLu/awesome-nanobanana-pro)
```json
"photography": {
  "camera_style": "casual iPhone mirror selfie, NOT professional",
  "quality": "iPhone camera - good but not studio, realistic social media quality",
  "angle": "eye-level, straight on mirror",
  "shot_type": "3/4 body, close to mirror",
  "aspect_ratio": "9:16 vertical",
  "texture": "natural, slightly grainy iPhone look, not over-processed"
},
"background": { "setting": "regular apartment bathroom", "style": "normal NYC apartment bathroom, not luxury" }
```
Nota: las negaciones van *dentro* de los valores ("NOT professional", "not luxury", "not over-processed"). El bloque de sujeto original se omitió.

**A8. Webcam de los 2000, @favprompt (Nano Banana Pro, 21/10/2026)** **[PROBADO POR LA FUENTE]** — [YouMind No. 7](https://github.com/YouMind-OpenLab/awesome-nano-banana-pro-prompts)
```
A candid couple photo of the Woman's Look and Man's Look in the Setting, engaged in the Activity. Render it as the Camera Type, with soft focus, smeared facial detail, color noise, dim uneven indoor light and low-resolution compression. Use awkward webcam framing from a desk-level angle, with a slight tilt and casually cropped shoulders or arms. [...] The couple should look genuinely close and relaxed, with real skin, messy everyday hair and no heavy retouching. Use Face Reference for the matching faces when applicable. Make it feel like an unedited early-2000s personal photo from an old Facebook album or MSN chat, not a modern image with a retro filter. No date stamp, text, watermark, modern electronics or current fashion.
```
Nota: es una plantilla parametrizada (Woman's Look, Setting, Camera Type). La clave está en "not a modern image with a retro filter".

**A9. Flash amateur, @Arminn_Ai** **[PROBADO POR LA FUENTE]** — [ZeroLu §1.12](https://github.com/ZeroLu/awesome-nanobanana-pro)
```
Harsh, direct on-camera flash lighting that creates hard shadows behind the subjects. Authentic film grain, slight motion blur on the edges, and chromatic aberration. It looks like a candid, amateur snapshot as if captured during a chaotic behind-the-scenes moment, not a studio photo.
```
Nota: un bloque de luz y procesado listo para pegar en escenas de noche o de evento.

**A10. Rescate de piel plástica, Dan Scalco (edición en Nano Banana Pro)** **[PROBADO POR LA FUENTE, RESUMEN]** — [X](https://x.com/DanScalco/status/1992969985782636711)
```
Upscale this image to 4K resolution. Enhance the skin with realistic pores and skin texture that matches the person's age and features. Keep the enhancement subtle and true to life. Do not over-smooth or add artificial shine. Maintain natural imperfections and very subtle fine lines and very subtle small blemishes for authenticity. Ensure overall tone, lighting, and detail look the same.
```
Nota: cuenta como una pasada generativa de cuadro completo, así que usala una vez, sobre el máster. Pedí la resolución con `image_size`: escribir "4K" en el texto no cambia el tamaño. Si la usás, componé solo la piel encima del máster.

**A11. Bloqueo de identidad para ropa, OpenAI (prueba virtual; dos fragmentos del mismo ejemplo)** **[PROBADO POR LA FUENTE, OFICIAL]** — [OpenAI Cookbook](https://github.com/openai/openai-cookbook/blob/main/examples/multimodal/image-gen-models-prompting-guide.ipynb); [guía 1.5](https://github.com/openai/openai-cookbook/blob/main/examples/multimodal/image-gen-1.5-prompting_guide.ipynb)
```
Do not change her face, facial features, skin tone, body shape, pose, or identity in any way. Preserve her exact likeness, expression, hairstyle, and proportions … Replace only the clothing, fitting the garments naturally to her existing pose and body geometry with realistic fabric behavior. Match lighting, shadows, and color temperature to the original photo so the outfit integrates photorealistically, without looking pasted on. Do not change the background, camera angle, framing, or image quality, and do not add accessories, text, logos, or watermarks.
```
Nota: la plantilla oficial para cambiar ropa sin tocar a la persona.

**A12. Fotorrealizar un personaje diseñado ("실사화"), @2_dam_e (GPT Image; traducción del fragmento inicial)** **[PROBADO POR LA FUENTE, traducido y truncado]** — [X](https://x.com/2_dam_e/status/2106696827307516412)
```
Use the attached image as the appearance reference for the person. Keep the facial features, face shape, shape and proportions of eyes/nose/mouth, hairstyle, hair color, eye color, body type, age range, and overall impression and identity as unchanged as possible. Don't just overlay skin texture on the original drawing; naturally reinterpret what this person would look like if they really existed and were photographed with a camera. Remove the illustration / AI-drawing feel and render it like a real portrait photo. The skin should not be overly smooth or…
```
Nota: según el resumen, el original sigue pidiendo conservar poros y variación de color, evitar pelo y ojos de muñeca, evitar HDR y filtros, y prohíbe agrandar ojos o achicar el mentón. Es la vía limpia para crear una cara 100 % ficticia.

### B. Síntesis para el SOP

Todas estas plantillas son **[SÍNTESIS NO TESTEADA]** y usan el mismo esqueleto: uso + "photorealistic" → identidad → acción → entorno → cámara → luz → textura → restricciones. Los corchetes son variables.

**B1. Selfie UGC en la cocina, en segmentos rotulados (GPT Image 2 / 2.5)**
```
Use case: photorealistic smartphone selfie for a UGC-style social ad; it must look like she filmed it herself on her own phone.
Subject: a Latina woman in her early 30s, olive skin, dark brown hair in a loose claw-clip bun with flyaway strands, small gold hoops, faded grey crewneck sweatshirt with the sleeves pushed up.
Action: holding the [PRODUCT] up beside her cheek with the label facing the camera, mid-sentence with a natural half-smile, eyes on the phone screen rather than the lens.
Environment: her small apartment kitchen in the morning — white cabinets, a dish rack with two mugs, a fruit bowl with bananas, a kettle, a phone charger cable on the counter, a window over the sink.
Camera: iPhone front camera held at arm's length, slightly above eye level, roughly 24mm-equivalent wide lens with mild perspective stretch near the frame edges, everything in focus with no portrait-mode blur, framing slightly off-centre with her right shoulder cropped, vertical 9:16.
Lighting: soft daylight from the window on camera-left mixed with a warm overhead ceiling bulb, slightly uneven exposure, the window side of her face a little brighter.
Texture: real skin with visible pores, faint under-eye shadows, light shine on the forehead and nose, a few baby hairs; ordinary phone processing — auto HDR, light noise in the shadows, mild JPEG compression, neutral slightly warm colours.
Constraints: product label legible and unchanged; no beauty filter, no retouching, no studio or glamour lighting, no cinematic colour grading, no extra text, no watermark.
```
Nota: la plantilla madre del SOP. En "Subject" va el descriptor del pack. Usá `quality="high"` o `xhigh`.

**B2. La misma escena en párrafo narrativo con roles de referencia (Nano Banana Pro / 2.1)**
```
Image 1 is the identity reference: use it only for her face, hairline and hair texture. Image 2 is the product: keep its exact shape, colours, cap and label text. Create a photorealistic smartphone selfie for a UGC-style skincare ad, as if she filmed it herself on her own phone. The same woman from Image 1, early 30s, olive skin, dark brown hair in a loose claw-clip bun with flyaway strands, wearing a faded grey crewneck sweatshirt, holds the product from Image 2 beside her cheek with the label facing the camera, mid-sentence with a natural half-smile, eyes on the phone screen. She is in her small apartment kitchen in the morning, with white cabinets, a dish rack with two mugs, a fruit bowl, a kettle and a charger cable on the counter. The front camera is held at arm's length slightly above eye level, wide-angle with mild stretch at the edges, everything in focus with no portrait-mode blur, framing slightly off-centre. Soft daylight from a window on camera-left mixes with a warm ceiling bulb, slightly uneven exposure. Real skin with visible pores, faint under-eye shadows and a little shine on the forehead; ordinary phone processing with light shadow noise. Same person as Image 1, identity unchanged; no beauty filter, no retouching, no extra text.
```
Nota: fijá `aspect_ratio="9:16"` y `image_size="2K"` en la configuración, no en el texto. El bloqueo de identidad abre y cierra el prompt.

**B3. Versión JSON con HEX (FLUX.2)**
```json
{
  "scene": "Morning in a small apartment kitchen; a customer self-recording a quick product review on her phone for a UGC ad",
  "subjects": [
    {
      "description": "Latina woman, early 30s, olive skin, dark brown hair in a loose claw-clip bun with flyaway strands, small gold hoop earrings",
      "wardrobe": "faded grey crewneck sweatshirt, sleeves pushed up, color #9A9A96",
      "action": "holds the product beside her cheek, label facing camera, mid-sentence half-smile, eyes on the phone screen",
      "skin": "natural unretouched skin, visible pores, faint under-eye shadows, light shine on forehead and nose"
    }
  ],
  "style": "candid smartphone photo, everyday social-media realism, natural slightly warm phone colours",
  "lighting": "soft daylight from a window camera-left mixed with a warm overhead ceiling bulb, slightly uneven exposure",
  "background": "white cabinets, dish rack with two mugs, fruit bowl, kettle, charger cable on the counter, window over the sink",
  "composition": "vertical 9:16, slightly off-centre, right shoulder cropped, slightly above eye level",
  "camera": {
    "device": "iPhone front camera at arm's length",
    "lens": "24mm-equivalent wide, mild edge stretch",
    "depth_of_field": "deep focus, background readable",
    "processing": "auto HDR, light shadow noise, mild JPEG compression"
  }
}
```
Nota: todo va en positivo porque FLUX.2 no tiene negativos. Usá el HEX con la palabra "color" delante.

**B4. Selfie en el auto, coach de 45 años (infoproducto)**
```
Photorealistic phone selfie taken by a man sitting in the driver's seat of his parked car, recorded as a quick motivational update for his followers. He is a Black man in his mid-40s, short tapered hair with a little grey at the temples, neatly trimmed beard, navy quarter-zip over a white tee, seatbelt off. He holds the phone at arm's length with one hand, slightly below eye level, looking straight into the front camera with a relaxed, confident expression, mouth slightly open as if talking. Behind him: the passenger seat headrest, the rear window with a blurred parking lot and trees, a sunglasses case on the dashboard edge. Daylight comes through the windshield and the side window, lighting the left side of his face more brightly, with soft shadows under the brow and small reflections on the glass. Wide-angle front-camera look, background mostly in focus, slight phone sharpening, light noise in the darker car interior. Natural skin texture with visible pores, a few razor bumps along the jawline, slight shine on the forehead. Ordinary, unretouched social-media photo, vertical 9:16, no text, no logos.
```
Nota: en Midjourney V8, recortalo a ~40 palabras y agregá `--ar 9:16 --raw --stylize 50`. En Z-Image Turbo, dejá el texto completo con CFG 0/1.

**B5. Selfie en el espejo del gimnasio (suplemento)**
```
Photorealistic gym mirror selfie, taken with the phone's rear camera in the mirror of a busy commercial gym. A South Asian woman in her late 20s, medium-brown skin, long black hair in a high ponytail with loose strands stuck to her neck, slightly flushed cheeks and a light sheen of sweat, wearing a black sports bra with a loose grey cropped tee over it and olive leggings. She holds the phone at chest height partially covering her chin, the other hand holding a shaker bottle of [PRODUCT], weight shifted to one hip, casual unposed stance. Mirror shows dumbbell racks, a bench, rubber floor tiles, and another gym-goer out of focus in the background. Lighting: overhead industrial LED panels giving top-down light, highlights on the forehead and shoulders, slightly cool white balance. Phone camera look: about 26mm equivalent, deep depth of field so the background stays readable, a faint smudge on the mirror catching light, mild noise. Real skin texture, no airbrushing, no fitness-magazine polish, vertical 4:5.
```
Nota: luz cenital dura más sudor dan textura creíble. El "smudge" en el espejo es la imperfección motivada.

**B6. Presentadora en su escritorio (curso online; semi-pro)**
```
Photorealistic talking-head portrait for an online course ad, styled like a frame from a self-recorded video lesson. A white woman in her mid-50s with chin-length ash-blonde hair, natural grey roots showing slightly, reading glasses pushed up on her head, light makeup, a soft sage-green cardigan over a cream top. She sits at her home desk turned three-quarters toward the camera, hands loosely clasped, mid-laugh while speaking. Background: a bookshelf with mismatched books, a potted pothos, a framed family photo, a warm table lamp switched on. Camera: mirrorless camera on a tripod at eye level, 35mm lens at about f/2.8, background softly out of focus but recognisable, medium close-up from mid-chest up. Lighting: a large window to camera-left as the key light creating soft loop lighting on her face, a white wall bouncing gentle fill on the right, the warm lamp in the background at about 2700K against the cooler daylight. Natural skin with fine lines around the eyes and mouth, light age spots, visible pores, no retouching. Natural colour balance, no cinematic grading, no studio backdrop, no text.
```
Nota: adaptado del prompt "testimonial" de las notas a "presentadora". **Cumplimiento: no la uses como testimonio de una alumna real** (16 CFR 465). En FLUX.2, agregá "Shot on Sony A7 IV, 35mm f/2.8".

**B7. Espejo de baño, skincare (22 años)**
```
Photorealistic casual bathroom mirror selfie, taken on an iPhone rear camera through the mirror in a normal rented apartment bathroom (not luxury). An East Asian woman in her early 20s, bare-faced after cleansing, hair pulled back with a fabric headband, a few small blemishes on her chin and faint redness around her nose, wearing an oversized white T-shirt. She holds the phone at chest level with one hand and a small [PRODUCT] bottle near her cheek with the other, slight head tilt, relaxed. Environment: white subway tiles, a basic mirror with a few water spots, a vanity strip light above the mirror, toothbrush cup, a towel hanging on a hook, skincare bottles crowded on the sink edge. Lighting: cool-white vanity light from above casting soft shadows under her brows, slight glare on the tiles. Camera: about 26mm phone lens, deep depth of field, no portrait-mode blur, slight tilt to the frame. Texture: real skin with visible pores and texture, a little dampness at the hairline, natural slightly grainy iPhone look, not over-processed. Vertical 9:16, no text overlays, no watermark.
```
Nota: los azulejos son geometría repetitiva y conviene revisarlos al 100 %. Para LatAm, cambiá casting y set.

**B8. Calle, foto sacada por un amigo (60 y pico)**
```
Photorealistic candid street photo of a man in his 60s of Middle-Eastern descent, olive-tan skin with deep smile lines, short white hair and a salt-and-pepper moustache, wearing a tan linen shirt and a light quilted vest, laughing while holding a takeaway coffee on a busy weekday sidewalk. Shot by a friend on a phone from about two metres away, eye level, slightly tilted horizon, a passer-by partially cropped at the frame edge. Background: café tables, parked scooters, shop awnings, a crosswalk. Overcast late-morning sky acting as soft even light, gentle shadows, muted realistic colours, no sun flare. Phone wide lens with mostly deep focus, slight motion softness in his hand, mild HDR. Natural weathered skin with pores, sunspots and wrinkles, unretouched, everyday documentary feel, vertical 4:5.
```
Nota: "shot by a friend" define quién sostiene la cámara, uno de los rasgos que comparten los prompts virales. Mantené los carteles fuera de foco.

**B9. Avatar de autoridad sin credenciales inventadas (educador de skincare)**
```
Photorealistic workplace photo taken by a colleague for a brand's social media — believable, not a stock photo. A South Asian man in his early 50s with short greying hair, rimless glasses and a neatly trimmed beard, wearing a light-blue shirt under a navy cardigan, standing in a bright consultation room and explaining something while holding a small [PRODUCT] tube. Background: a consultation chair, a wall-mounted magnifier lamp, a small plant, a window with blinds; no diplomas, no badges, no readable text. Lighting: bright even overhead lights at neutral white (about 5000K) plus soft daylight through the blinds from the right, mild specular highlight on his glasses. Camera: smartphone at chest height, around 26mm, background in focus, medium shot from the waist up, natural slightly cool colour. Real skin with pores and fine lines, slight under-eye creases, no retouching, no cinematic lighting, no logos.
```
Nota: el prompt de "dermatólogo" de las notas se adaptó **a propósito**: sin bata, sin estetoscopio y sin diplomas. Presentar un avatar como profesional de la salud con licencia, o asociarlo a claims de salud, es de altísimo riesgo regulatorio. Pasalo por revisión legal.

**B10. Flash de fiesta en un depto (moda o e-commerce)**
```
Photorealistic flash snapshot at a friend's apartment party at night, taken with a compact digital camera with a built-in flash. Two friends in their mid-20s — a Black woman with braided hair in a yellow slip dress and a white man with curly hair in an open denim shirt — squeeze together laughing, her holding a small [PRODUCT] bag up to the lens. Direct on-camera flash: bright highlights on foreheads and noses, crisp catchlights, a hard shadow cast on the wall behind them, dark room falling off quickly, a few string lights blurred in the background. Slightly crooked framing, cropped elbows, a little flash glare without red-eye. Realistic skin with pores and a little shine, mild noise, slightly blown highlights, unedited look. 3:2 landscape, no date stamp, no text.
```
Nota: la firma del flash directo completa: sombra dura en la pared, caída rápida a negro y zona T brillante.

**B11. Pareja mayor en el living (suplementos)**
```
Photorealistic candid smartphone photo taken by their grandchild: a Hispanic couple in their 70s sitting close together on a floral sofa in their living room, the woman with short silver curls and a lilac cardigan, the man with a bald crown, white stubble and a plaid flannel shirt, both looking at a [PRODUCT] bottle she is holding and smiling. Room details: crocheted throw on the sofa back, framed family photos, a TV remote and reading glasses on the coffee table, a standing lamp. Late-afternoon window light from camera-right mixed with the warm lamp, slightly uneven exposure, the far side of the room a bit dark. Phone camera at seated eye level, about 26mm, mostly deep focus, framing slightly loose with the coffee table edge in the foreground. Real aged skin with wrinkles, age spots, visible pores, no retouching, warm natural colours, vertical 4:5.
```
Nota: el "grandchild" sostiene la cámara y la piel envejecida va sin pudor. Validá la utilería con revisores del mercado.

**B12. Webcam de noche en una residencia estudiantil (app de estudio)**
```
Photorealistic late-night laptop webcam-style still of a 19-year-old East African university student, dark brown skin, short natural hair, wearing an oversized hoodie, leaning toward the screen with a tired but excited smile, one hand holding a highlighter. Small dorm room: stacked textbooks, sticky notes on the wall, an energy drink can, tangled earphones, a string of fairy lights. Lighting: cool blue-white laptop screen glow on her face from below-front, plus a warm desk lamp from the left at about 3000K — mixed colour temperature. Camera: built-in laptop webcam at desk level, slight upward angle, soft focus, visible low-light noise and mild compression, slightly cropped top of the head. Real skin texture, no beauty filter, unedited, 16:9.
```
Nota: luz mixta más el pipeline de webcam (ruido y compresión) simulan el dispositivo, no un filtro.

**B13. Selfie en el espejo de un dormitorio brasileño, con referencia bloqueada (Nano Banana Pro)**
```
Image 1 is the identity reference: use it only for her face, hair and body proportions; do not redescribe or change them. Photorealistic casual mirror selfie taken with the phone's rear camera in a modest Brazilian apartment bedroom: beige painted wall, light laminate floor, a half-made bed in the background, a phone charger plugged into the wall socket, a water bottle on the dresser, a towel tossed over a chair, a small plant in the corner. Soft natural light from a window on camera-left, slightly uneven, the corner behind the bed a little darker. The phone is held at chest height, about 26mm equivalent, deep focus, framing slightly off-centre with a small tilt. Natural skin texture with visible pores, a little shine on the forehead, everyday unretouched look, mild phone noise. Same person as Image 1, identity unchanged. Vertical 9:16, no readable text, no watermark.
```
Nota: aplica la regla de Higor Cruz: todo el texto se gasta en el entorno y la cara queda en la referencia. Es la plantilla base para Brasil y se adapta a otros mercados cambiando el set, después de validarlo con revisores locales.

**B14. Pack de identidad (hoja de referencia del avatar)**
```
Photorealistic identity reference sheet of one fictional woman: [DESCRIPTOR — age, Fitzpatrick type and undertone, face shape, eye colour, brow shape, hairline, 1–2 marks such as a small mole above the left lip and a light freckle pattern across the nose]. Five aligned head-and-shoulders views of the same person — front, three-quarter left, three-quarter right, left profile, right profile — all at the same scale with a neutral expression. Plain neutral grey background, soft even frontal light with no strong shadows, neutral white balance around 5500K, natural skin texture with visible pores and her freckle and mole map clearly visible, light or no makeup, plain fitted grey t-shirt, hair in its usual style. Keep the same face, hair, proportions, outfit and colours in every view. No text, no labels, no watermark.
```
Nota: el cierre viene de las guías de turnaround ([Quest Studio](https://queststudio.io/blog/ai-character-turnaround-sheet)). Para más detalle, generá además cada vista por separado a 2K, el macro de piel y 2–3 expresiones. Antes de aprobarlo, corré el control de originalidad (ArcFace por debajo de ~0,3 contra caras reales).

**B15. Plantilla maestra de producción con bloqueo de identidad al principio y al final**
```
[IDENTITY LOCK] Use Images 1–3 ONLY as identity references for the same woman: keep her face shape, eye color (hazel-green), brow shape, hairline, nose, lips, the small mole above the left lip, and her freckle pattern exactly identical. Do not beautify, slim, or age her.
[SCENE] Now photograph her: <outfit>, <location with 4–7 everyday objects>, <pose and hand action>, <expression>, shot on <device/lens>, <one motivated light source with direction and Kelvin>, natural skin texture with visible pores, no retouching.
[PRODUCT] Use Image 4 only for the product's exact shape, label and colors.
[RE-LOCK] Same person as Image 1; identity unchanged; only the outfit, setting and pose differ.
```
Nota: es la estructura recomendada por practicantes de Nano Banana y GPT Image ([UD.hk](https://www.ud.hk/en/blogs/insight/article/2026-06-29-nano-banana-consistent-characters)). El bloque [IDENTITY LOCK] es el descriptor congelado del pack.

**B16. Recetas para Midjourney V8.2**
```
[plain-language photo description with one physical light source, camera/phone, imperfections] --v 8.2 --raw --s 60 --exp 0 --ar 4:5 --hd
[…same, slightly more polished presenter/expert…] --raw --s 120 --exp 5 --ar 4:5 --hd
```
Nota: lo oficial es que `--raw` apaga el "auto-pilot" y que stylize va por defecto en 100 sobre una escala de 0–1000 ([MJ docs](https://docs.midjourney.com/docs/style)). Las guías recomiendan entre 50 y 150 para fotorrealismo ([MindStudio](https://www.mindstudio.ai/blog/how-to-get-best-results-midjourney-v8)). Dejá la personalización apagada o usá un moodboard de fotos reales de celular. Si V8.2 sale demasiado "edgy", volvé a `--v 8.1`. El editado en HD vuelve a resolución estándar. La sintaxis exacta de `--v 8.2` no está verificada **[NO TESTEADO]**.

**B17. Fichas de ejecución para modelos abiertos** (parámetros base de los templates oficiales de ComfyUI y de los READMEs; los LoRAs vienen de resúmenes y hay que verificarlos en su página)

| Modelo | Base | Agregados de realismo | Refinado de piel | Trampas y licencia |
|---|---|---|---|---|
| FLUX.2 [dev] | euler / Flux2Scheduler, 20–28 pasos, FluxGuidance 3–4 ([template](https://github.com/Comfy-Org/workflow_templates/blob/main/templates/image_flux2_text_to_image.json)) | LoRA de piel a 0,5–0,8; Detail Daemon 0,2–0,5 | ×1,5–2 → img2img con denoise 0,2–0,35 | Turbo LoRA de 8 pasos solo para borradores. **[LICENCIA] no comercial** |
| FLUX.2 [klein] 4B / 9B base | euler / simple, 20–24 pasos, CFG 3,5–5 | 9B: fine-tune True-V2 ([comfyui-wiki](https://comfyui-wiki.com/en/news/2026-07-01-flux2-klein-9b-true-v2-news)) o LoRA de detalle a 0,5–0,8 | Denoise 0,25–0,35 | El distilled de 4 pasos no tolera más pasos ni más CFG. **4B Apache; 9B no comercial** |
| FLUX 3 Image Klein | Base: 50 pasos, CFG 4 (README) / 3,5 (template Comfy). Distilled: 16 pasos, CFG 1 ([README](https://github.com/black-forest-labs/flux-3-image-klein/blob/main/README.md)) | Todavía no hay LoRAs de realismo | Denoise 0,2–0,35 con la base | Upsampler obligatorio: revisá la luz. **[LICENCIA] Kommunity** |
| Qwen-Image-2.1 | euler / simple, 40–50 pasos en finales, CFG 1 (2,5–4 solo con negativo), 2K nativo, múltiplos de 32 ([Comfy docs](https://github.com/Comfy-Org/docs/blob/main/tutorials/image/qwen/qwen-image-2-1.mdx)) | "Glamour Realism" a 0,6 **[RESUMEN]** | Denoise 0,25–0,35 | Turbo de 8 pasos y Lightning de 4 solo para borradores. **[LICENCIA] solo investigación** |
| Qwen-Image-2512 | 50 pasos, true CFG 4, negativo oficial | Lenovo/Samsung UltraReal a 0,7–1,0 (tono de celular) ([HF](https://huggingface.co/gorlamee/LenovoUltraReal)) | Denoise 0,25–0,35 | Lightning da "doll skin". Licencia: verificar |
| Z-Image Turbo | 8–9 pasos, CFG 1 (o 0), shift 3; para piel, dpmpp_sde + beta o res_2m + beta57 | RealisticSnapshot a 0,6–0,7 ([HF](https://huggingface.co/Yuuuna/RealisticSnapshotZImageTurbo)) | 4x-UltraSharp → denoise 0,3, dentro de 0,2–0,4 ([NextDiffusion](https://www.nextdiffusion.ai/tutorials/z-image-turbo-upscaler-and-detailer-workflow-in-comfyui)) | Baja diversidad de caras; Euler Ancestral ablanda la piel |
| Z-Image base | res_multistep, 25–50 pasos, CFG 3–5, `cfg_normalization=True`, negativo | Pocos LoRAs; entrená uno propio | Igual que Turbo | Licencia: verificar |
| Krea 2 Turbo | 8 pasos, CFG apagado, mu 1,15, 1024–1536 px de lado corto con LoRAs ([README](https://github.com/krea-ai/krea-2/blob/main/README.md)) | Realism LoRA ~0,8–1,0; mantené el stack total ≤1,5, porque la textura se empasta entre 1,5 y 2,0 ([Sogni](https://www.sogni.ai/loras/krea2-bloomgirls)) | Img2img con denoise bajo (sin documentar) | Enhancer activado por defecto. **[LICENCIA] Community** |

Nota: para finales, los samplers de orden superior (RES4LYF `res_2s` con `beta57`) dan más detalle a costa de duplicar el costo por paso ([RES4LYF](https://github.com/ClownsharkBatwing/RES4LYF)). En Detail Daemon, poné el tope de `detail_amount` en ~0,5 para caras, porque de más da el look sobreafilado o HDR ([Detail Daemon](https://github.com/Jonseed/ComfyUI-Detail-Daemon)) **[NO TESTEADO en retratos]**.

## 15) SOP paso a paso y checklist de QA: diez fases, del diseño al archivo

El orden de las fases sale de las reglas citadas en las secciones anteriores. Las fuentes coinciden en el orden de las etapas, pero no en los valores exactos. Higgsfield, Laria y adlibrary describen las mismas etapas ([Higgsfield](https://higgsfield.ai/blog/how-to-create-ai-influencer); [adlibrary](https://adlibrary.com/guides/ai-prompting-guide-ugc-content-creators)). Ninguna agencia grande publicó un SOP propio, así que este es una síntesis.

**Fase 0. Diseño del avatar (una sola vez por persona).**
- Generá 50–100 caras candidatas con Nano Banana Pro, GPT Image 2.5 o Krea 2 (este último con licencia), o diseñá una ilustración y fotorrealizala (A12).
- Elegí una.
- Corré el **control de originalidad**: ArcFace por debajo de ~0,3 contra las bases de caras reales a las que tengas acceso, para no parecerte a una persona existente.
- Escribí el descriptor de 3–4 marcadores y la "biblia" del personaje: nombre interno, fototipo Fitzpatrick y subtono, edad, estilismo base.

**Fase 1. Pack de identidad.**
- Generá la hoja (B14) y cada vista por separado a 2K, más el macro de piel y 2–3 expresiones.
- Usá luz pareja y fondo gris.
- Calculá el centroide ArcFace del pack.
- Congelá todo como `AVATAR_v000` (PNG de solo lectura y PSD de 16 bits), con el manifiesto C2PA intacto.

**Fase 2. Del brief al prompt.**
1. Elegí la plantilla (B1, B2 o B3 según el motor; B4–B13 según la escena).
2. Completá las variables en orden:
   - propósito y quién sostiene la cámara;
   - dispositivo y óptica (sección 9);
   - una luz del léxico (sección 4) con la frase de coherencia;
   - dosis de piel según la edad (sección 5);
   - set del mercado (sección 8);
   - producto como referencia (sección 7).
3. Pasá el filtro de palabras prohibidas (sección 10) y adaptá el prompt al modelo (sección 3).

**Fase 3. Generación.**
- Usá la API con resolución nativa máxima: Nano Banana Pro en 2K/4K, GPT Image en `high`/`xhigh`/`max`, FLUX.2 a 4 MP.
- Bajá en PNG.
- Hacé 4–5 tomas en paralelo o un contact sheet 3×3 para exploración.
- Si pasás muchas referencias, verificá en la respuesta que entraron todas (uso de tokens de imagen).

**Fase 4. Selección y QA primario.**
- Elegí el cuadro por identidad y anatomía, no por detalle: el detalle se recupera, la identidad no.
- Aplicá los umbrales ArcFace (≥0,60 pasa; 0,45–0,60 a revisión; <0,45 se rechaza).
- Corré la checklist de abajo al 100 % de zoom.

**Fase 5. Correcciones.**
- Cada corrección es una rama nueva que sale del máster: un cambio, la plantilla de edición (sección 11) y el editor que preserve píxeles (Ideogram 4.5, Krea 3, Photoshop con selecciones de ≤1024 px, o Crop & Stitch).
- Componé **solo la región** con máscara calada y curvas igualadas contra un neutro.
- Presupuesto: ≤3 regeneraciones por zona y ≤5 de cuadro completo por rama. Si se supera, reconstruís desde el pack.

**Fase 6. Cara, upscale y piel.**
1. Arreglo de anatomía a la resolución base (FaceDetailer con denoise 0,35–0,45, o Generative Fill).
2. Upscale 2x conservador (SeedVR2, Topaz Redefine Realistic, Magnific Precision v2 *photo* o Krea a 2x con fuerza baja).
3. Pasada de piel enmascarada solo a la piel (Magnific Skin Enhancer *faithful* o Enhancor con nivel bajo), fundida con opacidad parcial y comparada con el héroe.
4. Segundo 2x solo si el máster necesita pasar de ~3–4K.

**Fase 7. Terminación.** Retoque, grade suave, sharpen con máscara (Radius 1,0, Masking ≥40), grano monocromo al final, aberración cromática solo en bordes y viñeta suave.

**Fase 8. Export y cumplimiento.**
- Máster en PNG/TIFF con C2PA.
- Entregas en sRGB JPEG o PNG en los tamaños de la plataforma (Meta: 1440×1800, 1440×1440, 1440×2560).
- Etiqueta visible y toggles de plataforma.
- El copy no presenta al avatar como cliente ni como reseña.
- Sin credenciales profesionales inventadas.
- Claims de salud y antes/después pasan por revisión legal.

**Fase 9. Archivo y revalidación.**
- Guardá un log por asset: modelo y versión, prompt, semilla, referencias, ramas y pasadas, puntajes de QA, ajustes de post y etiqueta aplicada.
- Revalidá el pack y las plantillas cada vez que un modelo cambie o se deprecie. Por ejemplo, migrá de Nano Banana 2 a 2.1 ([deprecations](https://ai.google.dev/gemini-api/docs/deprecations)).

### Checklist de QA (al 100 % de zoom y lado a lado con el máster)

El QA automático sin referencia no detecta la degradación iterativa: BRISQUE y NIQE fallaron en Banana100 ([arXiv 2604.03400](https://arxiv.org/pdf/2604.03400)). Por eso esta lista es humana y comparativa.

- [ ] **Identidad:** el ArcFace contra el centroide cumple el umbral. Lunares y pecas están en su lugar. La edad no derivó. No hay "embellecimiento" (ojos agrandados, mentón afinado).
- [ ] **Piel:** los poros varían por zona y no son uniformes. No hay grilla, panal ni "escamas". El brillo está solo en la zona T. Los granos no están exagerados. No hay acabado de cera.
- [ ] **Ojos:** el mismo brillo en ambos ojos, coherente con la fuente. La mirada apunta a algo. El iris no se ve vidrioso ni sobresaturado.
- [ ] **Dientes:** los bordes de cada diente se leen, el blanco es natural (no carillas), o la sonrisa es cerrada.
- [ ] **Pelo:** hay pelos sueltos y mechones que se cruzan. No hay casco ni halos en el nacimiento.
- [ ] **Manos:** cinco dedos, el pulgar del lado correcto, un agarre posible y uñas coherentes.
- [ ] **Producto:** forma, color, tapa y etiqueta idénticos al SKU. Si hace falta, la etiqueta real se compone encima.
- [ ] **Texto:** no hay texto deforme en ninguna parte. Los carteles quedan fuera de foco o fuera de cuadro.
- [ ] **Ropa y accesorios:** los pliegues son coherentes con la pose. La cantidad de aros es correcta. Nada flota ni se funde con el cuerpo.
- [ ] **Luz:** una sola lógica de fuente. Sujeto y fondo con sombras en la misma dirección. Ningún rim sin fuente. Ninguna doble exposición tipo HDR.
- [ ] **Óptica:** la profundidad de campo coincide con el dispositivo. No hay modo retrato falso ni bokeh de 85 mm en una selfie.
- [ ] **Fondo:** los azulejos y patrones no se rompen. Las líneas continúan detrás de los objetos. El cuarto se ve vivido, pero el producto se lee.
- [ ] **Color:** el neutro de control coincide con el máster (sin amarilleo ni oscurecimiento acumulado) y el balance de blancos es plausible.
- [ ] **Degradación:** no hay "digital ripple" (grillas, panal o textura granulosa) ni bordes sobreafilados, y las pasadas están dentro del presupuesto.
- [ ] **Overlays no pedidos:** no aparece una interfaz de celular ni marcas de agua inventadas por el modelo.
- [ ] **Resolución:** el tamaño final es el de la plataforma, el máster PNG está archivado y en la cadena no hay ninguna descarga de app.
- [ ] **Cumplimiento:** la etiqueta "IA" es visible, los toggles están activos, el C2PA del máster se conserva, el copy no presenta al avatar como consumidor real ni le inventa credenciales, y el control de originalidad está hecho.

### Lo que cambia de fondo

El cuello de botella del fotorrealismo dejó de estar en la generación y pasó a la custodia de los píxeles. Los modelos de punta ya dan fotos creíbles en la primera pasada; lo que arruina el resultado es tratar a la IA como un editor de capas cuando en realidad es una fotocopiadora con pérdida. Cada pasada generativa conviene pensarla como una recompresión JPEG con presupuesto. El activo de la empresa no es el modelo, que va a cambiar varias veces por año, sino el pack de identidad, la biblioteca de sets por mercado, las plantillas versionadas y el log de cada asset. Una consecuencia práctica: el ranking Elo general no es la métrica que importa. Conviene armar un set interno de 30–50 prompts de retrato, hacer pruebas a ciegas con cada lanzamiento y decidir con eso.

La segunda conclusión es que realismo y cumplimiento convergen. La disciplina que vuelve consistente a un avatar (pack, descriptor, C2PA, log) es la misma que lo vuelve auditable ante la FTC, el AI Act o una plataforma. Y el formato donde el ultra-realismo más rinde, el "cliente que da su testimonio", es justamente el de mayor exposición legal. Un SOP de referencia debería orientar el realismo hacia formatos honestos: presentadores, creadores declarados como IA y demostraciones de producto. También debería tratar la etiqueta como parte del diseño de la pieza y no como un parche al final.

## 16) Fuentes

Casi todas las páginas fuera de GitHub se leyeron solo a través de resúmenes de buscador. Las fuentes oficiales leídas de primera mano son el SDK y los cookbooks de OpenAI, el cookbook de Gemini, los READMEs de BFL, Qwen, Z-Image y Krea, y los templates de ComfyUI.

**Documentación oficial de modelos**
- OpenAI: [GPT Image prompting guide](https://github.com/openai/openai-cookbook/blob/main/examples/multimodal/image-gen-models-prompting-guide.ipynb) · [guía gpt-image-1.5](https://github.com/openai/openai-cookbook/blob/main/examples/multimodal/image-gen-1.5-prompting_guide.ipynb) · [image_model.py](https://github.com/openai/openai-python/blob/main/src/openai/types/image_model.py) · [image_generate_params.py](https://github.com/openai/openai-python/blob/main/src/openai/types/image_generate_params.py) · [image_edit_params.py](https://github.com/openai/openai-python/blob/main/src/openai/types/image_edit_params.py) · [high input fidelity](https://cookbook.openai.com/examples/generate_images_with_high_input_fidelity)
- Google: [Get Started Nano Banana](https://github.com/google-gemini/cookbook/blob/main/quickstarts/Get_Started_Nano_Banana.ipynb) · [Gemini API deprecations](https://ai.google.dev/gemini-api/docs/deprecations) · [changelog](https://ai.google.dev/gemini-api/docs/changelog?authuser=1) · [7 tips Nano Banana Pro](https://blog.google/products/gemini/prompting-tips-nano-banana-pro/) · [Nano Banana 2](https://blog.google/innovation-and-ai/technology/ai/nano-banana-2/)
- Black Forest Labs: [FLUX.2 README](https://github.com/black-forest-labs/flux2/blob/main/README.md) · [FLUX.2 specs](https://help.bfl.ai/articles/6944273991-what-are-the-flux-2-technical-specifications) · [FLUX 3 Image Klein README](https://github.com/black-forest-labs/flux-3-image-klein/blob/main/README.md) · [FLUX.2 prompting guide](https://docs.bfl.ai/guides/prompting_guide_flux2) · [Kontext blog](https://bfl.ai/blog/flux-1-kontext)
- Qwen: [Qwen-Image-2.1 README](https://github.com/QwenLM/Qwen-Image-2.1/blob/main/README.md) · [Qwen-Image README](https://github.com/QwenLM/Qwen-Image) · [prompt_utils_2512.py](https://github.com/QwenLM/Qwen-Image/blob/main/src/examples/tools/prompt_utils_2512.py)
- Otros: [Z-Image README](https://github.com/Tongyi-MAI/Z-Image) · [Krea 2 README](https://github.com/krea-ai/krea-2/blob/main/README.md) · [Krea 2 prompting](https://github.com/krea-ai/krea-2/blob/main/docs/prompting.md) · [Midjourney Version](https://docs.midjourney.com/hc/en-us/articles/32199405667853-Version) · [Midjourney Edit Model](https://docs.midjourney.com/hc/en-us/articles/48495453462797) · [MAI-Image-2.6 model card](https://microsoft.ai/pdf/MAI-Image-2.6-Model-Card.pdf) · [Ideogram 4.5](https://ideogram.ai/models/4.5/) · [BytePlus ModelArk](https://docs.byteplus.com/en/docs/ModelArk/1541523)
- ComfyUI: [templates de workflows](https://github.com/Comfy-Org/workflow_templates) · [docs de Qwen-Image-2.1](https://github.com/Comfy-Org/docs/blob/main/tutorials/image/qwen/qwen-image-2-1.mdx) · [upscale tutorial](https://docs.comfy.org/tutorials/utility/image-upscale)

**Rankings y comparativas**
- [Artificial Analysis T2I](https://artificialanalysis.ai/image/leaderboard/text-to-image) · [AA Editing](https://artificialanalysis.ai/image/leaderboard/editing) · [AA, test de 30 ediciones](https://x.com/ArtificialAnlys/status/2108600224478572767) · [AlphaSignal](https://alphasignal.ai/news/artificial-analysis-runs-30-edits-to-expose-how-image-models-drift) · [Arena T2I](https://arena.ai/leaderboard/image/text-to-image)
- [Turbologo](https://turbologo.com/articles/nano-banana-pro-vs-nano-banana-2/) · [Decrypt](https://decrypt.co/377998/chatgpt-images-2-5-vs-nano-banana-2-review) · [Oakgen](https://oakgen.ai/blog/gpt-image-2-vs-nano-banana-pro) · [getimg.ai](https://getimg.ai/blog/ai-realism-test-comparing-realistic-image-generation-models) · [The Decoder](https://the-decoder.com/googles-new-image-model-nano-banana-2-1-generates-better-images-for-less-money/) · [ZenCreator](https://zencreator.pro/ai-university/guides/seedream-image-complete-guide) · [LiteLLM registry](https://github.com/BerriAI/litellm/blob/main/model_prices_and_context_window.json)

**Papers sobre degradación y percepción**
- [FreqEdit (CVPR 2026)](https://arxiv.org/pdf/2512.01755) · [REED-VAE (2025)](https://arxiv.org/abs/2504.18989) · [Mi-Ripple](https://arxiv.org/abs/2609.11317) · [Banana100](https://arxiv.org/pdf/2604.03400) · [FLUX.1 Kontext](https://arxiv.org/pdf/2506.15742) · [EdiVal-Agent](https://arxiv.org/pdf/2509.13399) · [Kamali et al., CHI 2025](https://arxiv.org/abs/2406.08651v1) · [Hu, Li y Lyu (brillos corneales)](https://arxiv.org/abs/2009.11924v2)

**Edición, consistencia y QA**
- [Crop & Stitch](https://github.com/lquesada/ComfyUI-Inpaint-CropAndStitch) · [Acly inpaint nodes](https://github.com/Acly/comfyui-inpaint-nodes) · [lilting.ch (deriva de Qwen-Edit)](https://lilting.ch/en/articles/qwen-image-edit-pixel-perfect-referencelatent)
- [FaceFusion](https://docs.facefusion.io/usage/cli-arguments/processors/face-swapper) · [InsightFace (licencia)](https://github.com/deepinsight/insightface/blob/master/python-package/README.md) · [InfiniteYou](https://arxiv.org/pdf/2503.16418) · [Arc2Face](https://www.ecva.net/papers/eccv_2024/papers_ECCV/papers/05442.pdf) · [arXiv 2503.20108](https://arxiv.org/pdf/2503.20108) · [arXiv 2505.23462](https://arxiv.org/pdf/2505.23462)
- [BFL klein training](https://docs.bfl.ml/flux_2/flux2_klein_training) · [RunComfy, FLUX.2 dev LoRA](https://www.runcomfy.com/trainer/ai-toolkit/flux-2-dev-lora-training) · [rkrra, Krea 2 LoRA](https://rkrra.com/guides/krea-2-lora-training/) · [ai-muninn](https://ai-muninn.com/en/blog/character-lora-control-panel-wan22) · [UD.hk](https://www.ud.hk/en/blogs/insight/article/2026-06-29-nano-banana-consistent-characters) · [Higgsfield Soul ID](https://higgsfield.ai/creator-hub/help-center/ai-models/how-do-i-create-and-use-a-soul-id-character)

**Upscale y post-proceso**
- [SeedVR2 (numz)](https://github.com/numz/ComfyUI-SeedVR2_VideoUpscaler) · [Magnific Precision v2 API](https://docs.magnific.com/api-reference/image-upscaler-precision-v2/post-image-upscaler-precision-v2) · [Magnific Skin Enhancer API](https://docs.magnific.com/api-reference/skin-enhancer/overview) · [Topaz Gigapixel 1.3.0](https://community.topazlabs.com/t/topaz-gigapixel-v1-3-0-recover-faces-3-300-speed-up-for-neuroserver-models/102815) · [Topaz Face Recovery 3](https://developer.topazlabs.com/image-models/gigapixel/face-recovery-3) · [Krea Enhancer](https://www.krea.ai/docs/user-guide/features/enhancer) · [Enhancor](https://www.enhancor.ai/) · [ComfyLab](https://comfylab.dev/blog/workflows/comfyui-upscale-workflow-ultimate-sd-upscale/)
- [Legendary Presets](https://legendarypresets.com/realistic-film-grain-without-losing-detail/) · [RevelRaw](https://revelraw.com/blog/camera-raw-sharpening.html) · [Rangy, Photoshop](https://rangy.ai/blog/photoshop-generative-fill-alternatives) · [Wikipedia, Magnific](https://en.wikipedia.org/wiki/Magnific)

**Cumplimiento y procedencia**
- FTC: [16 CFR 465, Federal Register](https://www.govinfo.gov/content/pkg/FR-2024-08-22/html/2024-18519.htm) · [Cornell LII](https://www.law.cornell.edu/cfr/text/16/part-465) · [multa civil 2025](https://www.govinfo.gov/content/pkg/FR-2025-01-17/html/2025-01361.htm) · [aviso de 2026 sin ajuste](https://public-inspection.federalregister.gov/2026-18853.pdf) · [orden TruHeight](https://www.ftc.gov/news-events/news/press-releases/2026/07/ftc-approves-final-order-against-truheight-deceptive-unsubstantiated-advertising-supplements-kids) · [DLA Piper](https://www.dlapiper.com/en/insights/publications/2026/07/ftcs-2026-enforcement-approach-to-fake-reviews-takes-shape-takeaways-for-companies)
- UE: [Jones Day, Code of Practice](https://www.jonesday.com/en/insights/2026/06/european-commission-publishes-final-code-of-practice-on-marking-and-labelling-aigenerated-content) · [William Fry, AI Omnibus](https://www.williamfry.com/knowledge/eu-ai-act-omnibus-deal-reached-postponed-deadlines-watermarking-compromise-and-the-nudificiation-prohibition/) · [Orrick](https://www.orrick.com/en/Insights/2026/08/EU-AI-Act-Transparency-Obligations-for-AI-Generated-Content-Article-50) · [McCann FitzGerald](https://www.mccannfitzgerald.com/knowledge/data-privacy-and-cyber-risk/ai-transparency-european-commissions-guidelines-on-article-50-part-2-deployer-obligations) · [Bird & Bird](https://www.twobirds.com/en/insights/2026/taking-the-eu-ai-act-to-practice-the-final-transparency-code-of-practice)
- España y Brasil: [La Moncloa, 26/5/2026](https://www.lamoncloa.gob.es/consejodeministros/resumenes/Paginas/2026/260526-rueda-prensa-ministros.aspx) · [Cuatrecasas](https://www.cuatrecasas.com/es/spain/propiedad-intelectual/art/proyecto-ley-organica-buen-uso-gobernanza-ia) · [CASRAI, PL 2338](https://casrai.org/guides/brazil-ai-bill-pl-2338-status)
- Plataformas y procedencia: [Digital Applied (Meta)](https://www.digitalapplied.com/blog/ai-content-labeling-rules-advertisers-2026-reference) · [Cinerads (TikTok)](https://www.cinerads.com/blog/tiktok-ai-content-policy) · [c2paviewer](https://c2paviewer.com/articles/verify-ai-generated-image-c2pa-synthid)

**Practicantes y colecciones de prompts**
- [YouMind GPT Image 2](https://github.com/YouMind-OpenLab/awesome-gpt-image-2-prompts) · [YouMind Nano Banana Pro](https://github.com/YouMind-OpenLab/awesome-nano-banana-pro-prompts) · [ZeroLu](https://github.com/ZeroLu/awesome-nanobanana-pro) · [magiccreator-ai](https://github.com/magiccreator-ai/awesome-gpt-image-2-prompts) · [JimmyLv](https://github.com/JimmyLv/awesome-nano-banana) · [@Mho_23](https://x.com/Mho_23/status/2097483045221917131) · [adlibrary](https://adlibrary.com/guides/ai-prompting-guide-ugc-content-creators) · [Fstoppers](https://fstoppers.com/artificial-intelligence/inserting-products-existing-photos-ai-what-actually-works-901419)

**Fuentes no inglesas**
- Brasil: [Higor Cruz](https://higorprompts.substack.com/p/influencer-ia-o-detalhe-idiota-que)
- Corea: [CCFM](https://blog.ccfmedu.co.kr/ai-realistic-portrait-creation) · [brunch @codept](https://brunch.co.kr/@codept/45) · [pixo](https://pixo.video/ko/blog/gpt-image-fish-scale-fix) · [@2_dam_e](https://x.com/2_dam_e/status/2106696827307516412)
- Japón: [note そら](https://note.com/sora2_yu0516/n/nfdea80ba8204) · [note petabyte_ai](https://note.com/petabyte_ai/n/n914ab7f03be2)
- Rusia: [vc.ru](https://vc.ru/ai/2647149-21-promt-dlya-generatsii-realistichnykh-foto) · [neuroluv](https://neuroluv.ru/prompts/zimniy-strit-realistichnyy-iphone-kadr-108)
- Francia: [Génération IA](https://generationia.flint.media/p/nano-banana-shooting-photo-virtuel-json-prompting)
- Hispanohablantes: [StarryAI ES](https://starryai.com/es/blog/realistic-ai-image) · [Notebookcheck ES](https://www.notebookcheck.org/Instagram-persigue-a-los-influencers-generados-por-IA-que-no-admiten-que-son-falsos.1386571.0.html)
