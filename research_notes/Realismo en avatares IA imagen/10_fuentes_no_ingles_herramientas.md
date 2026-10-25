# Non-English practitioner knowledge (ES / PT-BR / RU / KO / JA / FR) on ultra-realistic AI avatar stills, plus Higgsfield Soul, Krea, Magnific and Enhancor settings (as of Oct 2026)

How the sources were read: almost every page host was blocked (proxy 403 on CONNECT for habr.com, vc.ru, brunch.co.kr, note.com, lilys.ai, higgsfield.ai, krea.ai, magnific.com, enhancor.ai, substack, youtube and others). Only raw.githubusercontent.com could be fetched. Labels used below:
- **[GH]**: verbatim text fetched from a GitHub raw file (the YouMind-OpenLab prompt repos, which tag each prompt with its original language, author, X link and date).
- **[SNIP]**: verbatim text that appeared in a search-result title or snippet.
- **[SS]**: a search-engine summary of a page I could not open. Treat it as second-hand and possibly paraphrased.

Dates for X posts come from decoding the status-ID timestamp ("snowflake"). I used about 60 web searches.

---

## Spanish (Spain / LatAm): what creators, agencies and course-sellers share

### Takeaway
The Spanish-language material that surfaced is mostly vendor blogs (Atlabs, Media.io, GoEnhance, Morphic, CapCut) and YouTube-summary sites. Real practitioner signal is thin, but it agrees on these points:
- Use 4–6 reference images for one consistent persona.
- Use a "prompt-upgrader" custom GPT before Nano Banana Pro.
- Ask for an iPhone/TikTok "get ready with me" framing.
- Request a single dominant light source.
- Add explicit negatives like "No piel falsa / No brillo artificial".

I found no native Spanish source on fixing pixelation when re-editing.

### Cited Findings
- **Reference count and prompt-upgrader GPT (YouTube summary, Dec 2025):** a summarized Spanish video, "Cómo Hacer UGC VIRAL con Nano Banana Pro (AL INSTANTE)", says you can upload 4–6 reference images to get the same person across outfits, scenes, angles and emotions. Snippet: "Se pueden subir 4 a 6 imágenes de referencia para obtener la misma persona con diferentes atuendos, escenas, ángulos y emociones". The video uses a custom GPT that "toma un prompt básico y lo convierte en un prompt específico optimizado para Nano Banana Pro" (takes a basic prompt and turns it into one optimized for NBP, with camera terms and aspect ratio). Video is then made in Arcads. [SS/SNIP] — [lilys.ai ES note](https://lilys.ai/es/notes/nano-banana-pro-20251207/viral-ugc-nano-banana-pro); same video in PT: [lilys.ai PT](https://lilys.ai/notes/pt/nano-banana-pro-20251209/viral-ugc-nano-banana-pro). Single source, though the 4–6 reference figure also appears in English material.
- **UGC phone framing (vendor, Spanish/English):** Atlabs' character prompt uses "iPhone UGC style photo, as if she is a tiktoker filming a get ready with me video" and suggests a low angle "as if the phone is propped on the table". [SNIP] — [Atlabs ES](https://www.atlabs.ai/es/blog/viral-nano-banana-pro-prompts-that-are-mind-blowing). Atlabs also has a Spanish 2026 guide arguing that informal, to-camera UGC blends into the Meta feed better than brand video, and that a persona (accent, age, name) can be tuned per audience segment. — [Atlabs ES 2026 Meta guide](https://www.atlabs.ai/es/blog/como-crear-anuncios-de-ugc-con-ia-que-realmente-conviertan-en-meta-en-2026)
- **Spanish creator prompt (Luis Garau, X, ~26 Apr 2026):**
  - Workflow: "1. Hazte un selfie con buena iluminación 2. Abre Gemini y activa Nano Banana 2 3. Carga tu selfie y usa este prompt: 'Toma la imagen que te adjunto como referencia facial exacta y cr…'" [SNIP]. In English: "1. Take a well-lit selfie 2. Open Gemini and turn on Nano Banana 2 3. Upload the selfie and use this prompt: 'Take the attached image as an exact facial reference and cr[eate]…'".
  - Per [SS], the prompt is an editorial headshot (studio light, head-and-shoulders, 85 mm-equivalent, 4:5). It asks for realistic skin detail with no plastic effect and has a negative block with "No piel falsa" ("no fake skin") and "No brillo artificial" ("no artificial shine").
  - Source: [x.com/luisgarau_](https://x.com/luisgarau_/status/2048303817436049524). This is a real-person selfie use case; the negatives carry over to fictional avatars.
- **Common Spanish skin vocabulary (vendor):**
  - Media.io: "Incluye palabras clave como 'piel realista', 'poros naturales' o 'luz suave' para mejorar la textura y evitar el efecto plástico" ("Include keywords like 'realistic skin', 'natural pores' or 'soft light' to improve texture and avoid the plastic effect"). [SNIP] — [Media.io ES](https://www.media.io/es/image-effects/realistic-ai-skin-prompt.html)
  - GoEnhance prompt: "Crea una foto realista de una persona, centrándote en detalles realistas de la piel humana, poros naturales, imperfecciones sutiles e iluminación auténtica, evitando cualquier estilo artístico o ilustrativo" ("Create a realistic photo of a person, focusing on realistic human-skin detail, natural pores, subtle imperfections and authentic lighting, avoiding any artistic or illustrative style"). [SNIP] — [GoEnhance ES](https://www.goenhance.ai/es/prompts/image-prompts/realistic-human-portrait-study)
- **One dominant light (vendor):** StarryAI ES: "'Hora dorada', 'softbox de estudio' y 'flash directo' en un mismo prompt suelen crear una iluminación confusa. Elige una configuración dominante y deja que las demás la apoyen" ("Putting golden hour, studio softbox and direct flash in one prompt usually gives confused lighting. Pick one dominant setup and let the others support it"). [SNIP] — [StarryAI ES](https://starryai.com/es/blog/realistic-ai-image)
- **Named skin "finish levels" (vendor):** Morphic ES separates "Pore Definition (definición de poros): poros visibles, líneas finas, grano de piel natural a nivel micro" (visible pores, fine lines, micro-level skin grain) from natural softness, glass skin and retouched editorial. Each suits a different project. [SNIP] — [Morphic ES](https://morphic.com/es/resources/how-to/fix-ai-generated-skin-realistic)
- **Ask for imperfections and asymmetry (Spanish agency blog):** WeAreCentric recommends asking for texture, wrinkles and asymmetry because skin detail makes faces credible. [SS] — [wearecentric.com](https://wearecentric.com/como-crear-rostros-hiperrealistas-con-nano-banana/)
- **Course-seller tool stack (Hotmart, Spanish listing "IA UGC Express"):** the course teaches building avatars "desde cero", realistic images, face-swap video, UGC editing and AI voices with: ChatGPT, Higgsfield AI, GeminiGen IA, CapCut, Nano Banana Pro, Motion Control 3.0, Kling 3.0, "Deep Fake", Fish Audio and FineVoice. [SS] — [Hotmart IA UGC Express](https://hotmart.com/es/marketplace/productos/ia-ugc-express/L105892142Y). This is seller marketing. The face-swap/deepfake modules are outside this project's scope (fictional people only).
- **Platform context (Spanish press):**
  - Instagram added an "AI-generated profile" label for accounts whose protagonist is fully synthetic. Per Instagram, unlabeled accounts in that category may see limited reach; real people using AI as an editing tool are not covered. [SS] — [pasqualepillitteri.it ES](https://pasqualepillitteri.it/es/news/13825/instagram-etiqueta-perfiles-generados-ia-influencers-falsos); [Notebookcheck ES](https://www.notebookcheck.org/Instagram-persigue-a-los-influencers-generados-por-IA-que-no-admiten-que-son-falsos.1386571.0.html)
  - This bears directly on a client running synthetic-avatar accounts or ads, and argues for disclosure rather than evasion.
- **Kitchen / smartphone templates in es-419:** YouMind's Latin-American Spanish gallery has "Realismo de cocina captado por accidente", "Retrato realista en cocina" and "Retrato realista de restaurante con smartphone". They share a template: vertical smartphone framing, person, kitchen, lighting, phone-camera perspective, "looks like an unedited photo", plus an exclusions list ("fondo ordenado, sin texto, sin marcas de agua, sin personas adicionales": tidy background, no text, no watermarks, no extra people). The examples default to East Asian women, not Latinas. [SS/SNIP] — [YouMind es-419 accidental kitchen](https://youmind.com/es-419/prompts/accidental-kitchen-candid-18704); [YouMind es-419 smartphone restaurant](https://youmind.com/es-419/prompts/realistic-smartphone-restaurant-portrait-29292)

### Inferences
- Spanish-speaking practitioners appear to mostly reuse English or Chinese prompt templates and tools (NBP, Higgsfield, Kling, Arcads, CapCut) and add Spanish-language framing. Native Spanish innovation on still-image realism was not visible in what surfaced.
- The useful additions for the client are workflow habits: the reference-image count, the prompt-upgrader GPT, and a short Spanish negative block ("No piel falsa. No brillo artificial. Sin retoque excesivo").
- The kitchen/smartphone templates need deliberate casting and set localization. Their default subject is East Asian, so an unlocalized template will not read as LatAm.

### Gaps
- No native Spanish practitioner post was found on "se pixela al editar nano banana" (pixelates when editing); the related query returned the English Banana100 paper. Creators in Argentina, Mexico, Colombia and Spain (e.g., Spanish AI YouTubers) were not identifiable with verbatim prompts because YouTube, TikTok and Threads could not be fetched.
- I found no Spanish-language Magnific/Krea/Enhancor settings tutorial.

---

## Portuguese (Brazil): UGC com IA, realistic avatars, info-producers

### Takeaway
Brazil had the most practitioner-flavored material. The standout source is a Brazilian TikTok Shop prompt newsletter (Higor Cruz). Its point: what makes AI influencer images look fake is the scenario, not the face. Real influencer rooms have mess (a charger in the socket, a water bottle, an unmade bed), and the prompt should describe only the environment, letting the reference photo define the person. Brazilian mainstream tech media (TechTudo, Canaltech, Catai) mostly translate viral English prompts and add Portuguese preservation clauses.

### Cited Findings
- **Scenario over face (Higor Cruz, "higorprompts" Substack, PT/EN, TikTok Shop niche):**
  - Article: "[Influencer I.A] O detalhe idiota que faz a IA parecer gravação real".
  - Main argument: AI makes rooms too clean, while real influencer photos have mess. The prompt should describe only the environment; the person comes from the attached reference photo, because describing the person makes the AI create a different person and breaks consistency. [SS]
  - Verbatim clutter list [SNIP]: "Garrafa d'água em cima da cômoda, carregador enfiado na tomada, toalha jogada, cama meio desfeita, uma plantinha no canto do banheiro." In English: "Water bottle on top of the dresser, charger plugged into the socket, towel tossed aside, half-made bed, a little plant in the corner of the bathroom."
  - The Brazilian-bedroom mirror-selfie prompt in the same piece specifies: beige wall, light laminate floor, bed in the background, charger in the socket, natural window light, vertical 9:16, and keeping the reference person's face, hair and clothes. [SS]
  - Source: [higorprompts.substack.com](https://higorprompts.substack.com/p/influencer-ia-o-detalhe-idiota-que)
  - Related posts from the same author: unboxing "POV ou influencer" prompts, "engenharia reversa" (reverse-engineering viral profiles' prompts), and an unverified claim of a faceless profile billing "mais de R$300 mil por mês". — [higorprompts reverse engineering](https://higorprompts.substack.com/p/pare-de-mendigar-prompt-a-engenharia); [higorprompts R$300k](https://higorprompts.substack.com/p/o-perfil-que-fatura-mais-de-r300)
  - Corroboration: the "lived-in clutter" idea also appears independently in Japanese note.com ("生活感のノイズ", see the Japanese section), so it is attested in two languages.
- **Translated viral prompts (TechTudo, Dec 2025):** reporters took three viral English selfie prompts from X, ran them through Google Tradutor, and changed details (clothing color, hair color, expression, morning→evening light) to test NBP's realism. [SS] — [TechTudo selfies](https://www.techtudo.com.br/dicas-e-tutoriais/2025/12/testamos-3-prompts-para-selfies-realistas-com-nano-banana-pro-veja-o-resultado-edsoftwares.ghtml). TechTudo advice [SNIP]: "informe que deseja uma imagem realista, descreva a cena, a iluminação, o ângulo e até pequenas imperfeições, como poros na pele" ("say you want a realistic image; describe the scene, lighting, angle and even small imperfections such as skin pores"). — [TechTudo prompt guide](https://www.techtudo.com.br/dicas-e-tutoriais/2025/09/prompt-para-nano-banana-domine-a-criacao-de-imagens-com-ia-usando-esse-comando-edsoftwares.ghtml)
- **Preservation clause (Canaltech):** "gere um retrato realista da pessoa da imagem, preservando tom de pele, fisionomia e expressão" ("generate a realistic portrait of the person in the image, preserving skin tone, physiognomy and expression"). [SNIP] — [Canaltech](https://canaltech.com.br/apps/6-prompts-para-aproveitar-o-melhor-do-nano-banana-ao-editar-fotos-no-gemini/)
- **Mirror selfie with face lock (Catai):** prompt that keeps the face ("o rosto não deve ser alterado": the face must not be altered), plus lighting-fix prompts that keep skin texture intact. [SS/SNIP] — [Catai](https://catai.com.br/revelamos-os-prompts-do-nano-banana-pro-que-transformam-suas-fotos-pessoais-em-cinema/)
- **Brazilian creator blog (Alvaro Mendonça):** ask explicitly for detailed skin texture with visible pores plus a resolution cue (8K). Example subject: "um homem de pele negra, por volta de 30 anos, em retrato fotorrealista de estúdio profissional" ("a Black man around 30, in a photorealistic professional studio portrait"). [SNIP] — [alvaromendonca.com](https://alvaromendonca.com/nano-banana/)
- **"Phone photo with authentic imperfections" (Treinamento SAF, 30 Gemini prompts for natural female photos):** ask that the output look like a real phone photo with authentic imperfections, not digital illustration; keep facial features; avoid overly smooth skin. [SS] — [treinamentosaf.com.br](https://treinamentosaf.com.br/30-prompts-gemini-feminino-natural-ar-livre-praia-golden-hour/)
- **Free UGC influencer prompts (Nespol):** iPhone UGC language, simple domestic set, window light. [SS] — [nespol.com.br](https://nespol.com.br/blog/prompts-gratis-movimentos-realistas-em-influencers-ugc-feitas-com-ia/)
- **Persona-stability clause (Vini Ensina):** a planning prompt asks that appearance stay stable without changing apparent age, face shape, hair color, eye color or overall style. [SS] — [viniensina.com.br](https://viniensina.com.br/?p=3882)
- **Editing advice (Fast Company Brasil):** start with short, objective descriptions and test small variations before complex changes. [SS] — [Fast Company Brasil](https://fastcompanybrasil.com/ia/nano-banana-3-truques-para-criar-imagens-profissionais-com-a-ia/)
- **Info-product market size (Hotmart):** more than 340k users bought AI courses/solutions on Hotmart in 2025. A Hotmart blog post of 28 May 2026 on AI for info-products stresses personalizing to avoid generic output. [SS] — [Hotmart blog](https://hotmart.com/pt-br/blog/como-usar-ia-para-criar-infoprodutos)
- **Legal caution (search engine note, not a source):** an AI testimonial presented as a real customer may constitute misleading advertising. CONAR/CDC rules were not researched. [SS]

### Inferences
- The Higor Cruz recipe works directly for the client's synthetic avatars:
  1. Lock the person with a reference image (a generated fictional character sheet).
  2. Spend the prompt budget on a specific Brazilian domestic set: beige or painted-block walls, light laminate or ceramic floor, charger cable, water bottle, towel, half-made bed.
  3. Avoid re-describing the face.
- Brazilian mainstream media prompts are largely translated English prompts, so Portuguese wording itself is not a realism lever. The local set and casting are.

### Gaps
- The Hotmart/Kiwify course pages for Brazilian "influenciadora IA" products could not be opened; only one Spanish Hotmart listing surfaced.
- I found no Brazilian source naming typical phones to emulate (e.g., Samsung Galaxy A-series, Motorola) or quantifying which "phone look" converts.

---

## Russian: реалистичный аватар / кожа / Nano Banana Pro (Habr, VC.ru, T-Zh, prompt sites)

### Takeaway
Russian practitioner content is heavily list-style ("21/30/50 prompts" on VC.ru and Habr corporate blogs) but has distinctive phrasing:
- A face-lock and anti-doll-skin negative block ("не менять лицо и волосы, не делать кукольную кожу, не размывать веснушки").
- Phone-pipeline artifacts written into the prompt: slight digital noise, soft JPEG compression, slight under-exposure, micro-smear.
- "Shot on the move": slight motion blur and an off-center subject.

Sources disagree on whether "noise" belongs in the positive or the negative prompt.

### Cited Findings
- **Negative block (VC.ru "21 промт для генерации ультрареалистичных фото!", NBP):** [SNIP] "не менять лицо и волосы, не делать кукольную кожу, не размывать веснушки". In English: "do not change the face and hair, do not make doll-like skin, do not blur the freckles". The article also lists hand- and artifact-related constraints. — [vc.ru 2647149](https://vc.ru/ai/2647149-21-promt-dlya-generatsii-realistichnykh-foto)
- **Other VC.ru negatives [SNIP]:** "любые изменения лица, другая внешность, сглаженная кожа, бьюти-ретушь" ("any changes to the face, a different appearance, smoothed skin, beauty retouching"). Another article puts "cartoon, illustration, painting, CGI, 3D render" in the negative. — [vc.ru list of VC articles](https://vc.ru/ai/2804035-gotovye-promty-dlya-izobrazheniy-neyroseti) (exact article of each snippet not confirmed; [SS])
- **Explicit-instruction advice (VC.ru, Nano Banana prompt guide):** write explicitly "сохрани лицо" (keep the face), "не меняй возраст" (don't change the age) and "оставь естественную кожу" (leave natural skin), and say the photo should look like a real shoot. Detailed prompts beat short ones. [SS] — [vc.ru 2960489](https://vc.ru/services/2960489-promty-dlya-nano-banana)
- **Phone-pipeline artifacts (neuroluv.ru "Снято на iPhone" series, NBP-based):**
  - "Зимний стрит" (winter street) camera/processing block [SS]: "лёгкий цифровой шум, мягкое JPEG-сжатие, отсутствие ретуши и фильтров, лёгкая микросмазка" ("slight digital noise, soft JPEG compression, no retouching or filters, slight micro-smear").
  - "Реалистичный iPhone-кадр после дождя": "снимок без фильтров с лёгким цифровым шумом iPhone" ("an unfiltered shot with slight iPhone digital noise").
  - Every prompt in the series includes keeping the face from the uploaded photo 1:1.
  - Sources: [neuroluv winter street](https://neuroluv.ru/prompts/zimniy-strit-realistichnyy-iphone-kadr-108); [neuroluv after rain](https://neuroluv.ru/prompts/realistichnyy-iphone-kadr-posle-dozhdya-v-gorode-43); [neuroluv night iPhone](https://neuroluv.ru/prompts/snyato-na-iphone-nochnoy-iphone-kadr-243)
- **Real phone-frame aesthetic (prompt1.ru "съемка на iPhone"):** [SNIP] "слегка заниженная экспозиция, естественный шум, без глянцевой ретуши" ("slightly under-exposed, natural noise, no glossy retouching"). The prompt also places the phone very close to the lens (extreme perspective) and keeps facial features from the upload. — [prompt1.ru](https://prompt1.ru/listing/prompt-semka-na-iphone/)
- **"Shot on the move" plus off-center framing (Klerk.ru):** a "снято на ходу" approach with slight motion blur and natural daylight. Move the subject off-center, because perfect symmetry often gives the generator away. [SS] — [klerk.ru](https://www.klerk.ru/blogs/oplatymru/680639/)
- **Contradiction on noise:** VC.ru's "Промпты для селфи 2026" puts "шум" (noise) in the negative prompt, the opposite of neuroluv/prompt1. [SS] — [vc.ru selfie 2026](https://vc.ru/reviews/2681566-prompty-dlya-selfi-2026-luchshie-neyroseti-i-sovety)
- **Evaluation heuristics (Habr review of realistic-photo networks):** judge outputs by skin micro-detail and lighting logic; good frames show pores and slight asymmetry of facial expression. [SS] — [Habr 1009882](https://habr.com/ru/articles/1009882)
- **Prompt formula (T—Zh):** photorealistic portrait + scene + soft side light + ~50 mm lens + explicit skin texture, hair shine and reflections. [SS] — [t-j.ru](https://t-j.ru/short/nano-banana-prompts/)
- **Camera defaults in RU photo-session blogs (Habr/StudyAI):** 85 mm, f/1.8, bokeh, softbox. [SS] — [Habr StudyAI 1023696](https://habr.com/ru/companies/studyai/articles/1023696/)
- **Model claims (Tproger):** NBP avoids "plastic" skin and keeps pores and small wrinkles; another Tproger piece claims NBP keeps facial features "almost fully". These are author claims. [SS] — [tproger realistic](https://tproger.ru/articles/nejroset-dlya-realistichnyh-foto--kak-ii-nauchilsya-sozdavat-izobrazheniya-neotlichimye-ot-nastoyashhih); [tproger new-year shoot](https://tproger.ru/articles/novogodnyaya-fotosessiya-s-ii--kak-nano-banana-pro-sozdayot-studijnye-kadry-za-2-minuty)
- **Higgsfield Soul from a Russian reviewer (Habr):** more photorealistic than Flux/SD and its presets are more interesting out of the box, but it is a closed model ("нет возможности скачать лору": no way to download a LoRA). [SS] — [Habr 930074](https://habr.com/en/articles/930074). The Russian teletype explainer on Soul says it needs no prompt engineering, and presets (iPhone flash etc.) carry the look. [SS] — [teletype ru_com](https://teletype.in/@ru_com/chto-takoe-higgsfield-soul-i-kak-im-polzovatsya)
- **Provenance context (AppleInsider RU):** iOS 27 beta 5 reportedly contains an "Apple Reference Image" tool meant to certify that a photo came from the iPhone camera; unannounced. [SS] — [appleinsider.ru](https://appleinsider.ru/ios/apple-v-ios-27-nauchit-iphone-dokazyvat-chto-foto-nastoyashhee-a-ne-narisovano-nejrosetyu.html). This is a provenance signal, reported here for context only and not as something to circumvent.

### Inferences
- The Russian "pipeline artifact" vocabulary (soft JPEG compression, micro-smear, slight under-exposure) is more specific than the common English "film grain". It targets the computational-photography look of a real phone.
- The noise contradiction suggests testing per model. A plausible split: slight sensor/JPEG noise for phone-UGC frames, and noise in the negative for clean e-commerce or studio frames.
- "Не размывать веснушки" is a useful edit-time guard: it protects existing micro-features when re-editing an avatar.

### Gaps
- No Telegram channel content could be read (Telegram was not in reach), and Russian traffic-arbitrage ("арбитраж") practitioners' UGC-creative methods did not surface beyond vendor pages.
- The full texts of the VC.ru 21-prompt article and the Habr 30/50-prompt lists could not be retrieved.

---

## Korean: AI 인플루언서 실사, 나노바나나 프로 실사 프롬프트, 피부 질감

### Takeaway
The most original non-English ideas came from Korea:
1. Words like "고퀄리티 / 매우 사실적 / 완벽한 피부" (high quality / very realistic / perfect skin) backfire into doll-like results.
2. Realism comes from designing flaws (결함 설계) and region-specific skin detail (pores around the nose, redness on the cheeks, faint T-zone oil, baby hairs), not from negatives.
3. A "실사화" (illustration-to-photo) prompt that locks identity from an attached image.
4. A warning that "high-res / rich detail" requests can cause "fish-scale skin" in GPT Image close-ups.

### Cited Findings
- **CCFM blog, "AI로 극사실적인 인물 만드는 법 - 나노바나나 프롬프트 공유" (8 Jan 2026):**
  - Key idea: whether there are flaws ('결함'). Words like "고퀄리티", "매우 사실적", "완벽한 피부" produce doll-like results.
  - The guide's sections [SS]: 약간의 결함 만들기 (create slight flaws); 인물의 결함 설계하기 (design the person's flaws); 배경을 공간이 아닌 질감으로 표현하기 (render the background as texture, not as space); 빛의 방향보다 성격을 설정하기 (set the light's character rather than its direction); 인물 중심의 구도 설계하기 (person-centred composition).
  - It also describes an iterative loop: after generating, ask the AI how to make it feel like a real shoot.
  - Source: [blog.ccfmedu.co.kr](https://blog.ccfmedu.co.kr/ai-realistic-portrait-creation)
- **i-boss marketing community post, "AI로 사실적인 인물 치트키 + 나노바나나 멱살잡는 씨드림4.0 가이드":** repeating "사실적" and "고퀄리티" makes the AI produce an overly perfect, artificial texture, so deliberately add slight flaws and imbalance. Add human flaws such as acne (여드름), freckles (주근깨) and pores (모공), and take care over pupils and hair. The full guide is distributed by DM. [SS] — [i-boss 68347](https://www.i-boss.co.kr/ab-6141-68347)
- **Region-specific skin cues; detail beats negatives:** one Korean guide says "'네거티브 프롬프트'보다 '디테일 묘사'가 답" (detail description, not negative prompts, is the answer). Examples: 코 주변 모공 (pores around the nose), 볼의 붉은기 (redness on the cheeks), 주근깨 (freckles), T존의 은은한 유분 (faint T-zone oil), and 헤어 잔머리 (baby hairs/flyaways). [SS] — attributed to the i-boss/CCFM guides (exact page unclear): [i-boss](https://www.i-boss.co.kr/ab-6141-68347); [CCFM](https://blog.ccfmedu.co.kr/ai-realistic-portrait-creation)
- **"나노바나나 프로 | 인물 사진 프롬프트 종합 가이드" (brunch @codept):**
  - [SNIP] "피부 질감과 피부톤을 구체적으로 명시해야 한다. 'natural skin texture', 'visible pores', 'fine lines' 같은 표현은 과도한 스무딩을 방지" ("Skin texture and skin tone must be stated specifically; expressions like 'natural skin texture', 'visible pores', 'fine lines' prevent excessive smoothing").
  - Negative [SNIP]: "plastic skin, overly smooth, poreless, beauty filter, airbrushed".
  - Skin tone: specify via the **Fitzpatrick scale or undertone (warm, cool, olive)** for accurate tone.
  - Example [SNIP]: "porcelain fair skin with subtle freckles and visible pores, cool undertone, 85mm f/1.8, soft left key light, natural texture no smoothing, photorealistic".
  - It also advises a descriptive paragraph over a keyword list.
  - Source: [brunch.co.kr/@codept/45](https://brunch.co.kr/@codept/45)
- **"실사화" identity-lock prompt (Min.5 @2_dam_e on X, ~4 Oct 2026, for GPT image):** verbatim opening [SNIP]: "첨부한 이미지를 인물의 외형 기준 이미지로 사용해줘. 얼굴 생김새, 얼굴형, 눈·코·입의 형태와 비율, 헤어스타일, 머리색, 눈동자색, 체형, 나이대, 전체적인 인상과 정체성은 최대한 그대로 유지해줘. 단순히 원본 그림에 피부 질감만 덧씌우는 방식이 아니라, 이 인물이 현실에 실제로 존재하고 카메라로 촬영되었다면 어떤 모습일지를 자연스럽게 재해석해줘. 일러스트·AI 그림 같은 느낌을 제거하고 실제 인물 사진처럼 표현해줘. 피부는 지나치게 매끈하거…"
  - English: "Use the attached image as the appearance reference for the person. Keep the facial features, face shape, shape and proportions of eyes/nose/mouth, hairstyle, hair color, eye color, body type, age range, and overall impression and identity as unchanged as possible. Don't just overlay skin texture on the original drawing; naturally reinterpret what this person would look like if they really existed and were photographed with a camera. Remove the illustration / AI-drawing feel and render it like a real portrait photo. The skin should not be overly smooth or…"
  - The rest, per [SS]: keep pores, fine skin grain and micro colour variation; avoid over-glossy or doll-like hair, eyes and lips; emulate real camera lighting and lens; avoid excessive HDR, beauty filters, skin retouching and artificial sharpening; forbid beautification such as eye enlargement or chin reduction.
  - Source: [x.com/2_dam_e](https://x.com/2_dam_e/status/2106696827307516412)
- **Skincare model-shot prompt (Carat gallery, GPT Image 2):** [SNIP] "85mm macro-portrait editorial photograph. Medium-format skincare campaign quality." and "SKIN FOCUS: bare skin minimal coverage, natural pore texture visible". Skin sheen sits between semi-matte and semi-gloss. [SS] — [carat.im cosmetics-model](https://carat.im/prompt-gallery/cosmetics-model)
- **Natural-look keywords (Midjourney "내추럴 인플루언서" style post):** "natural light", "candid shot", "freckles", "minimal makeup" make results far more natural and real-looking. [SS] — [brunch @sobrief/78](https://brunch.co.kr/@sobrief/78)
- **"Fish-scale skin" warning (pixo, KR blog on GPT Image):** honeycomb/scale texture appears on wide bare-skin close-ups. Pixo's claimed causes: low-quality training noise learned as "skin", and the model reading "고화질 / 풍부한 디테일" (high-res / rich detail) as "fill every pixel"; prompt overload is often the trigger. This is a vendor blog with promotional intent. [SS] — [pixo.video](https://pixo.video/ko/blog/gpt-image-fish-scale-fix)
- **Model bias note (Dropshot AI blog, KR 2026 comparison):** Seedream is strong at people and tends to render Asians with refined faces. [SS] — [dropshot](https://aistudio.dropshot.io/ko/blog/generated-ai-site-comparison)
- **Korean Higgsfield review (brunch @sukistory):** Soul 2.0 is Higgsfield's flagship realistic image model. Aesthetic presets (Y2K, film camera, street snap) set the mood without long prompts. "Photodump" makes a 15-image set without a prompt. [SS] — [brunch @sukistory/136](https://brunch.co.kr/@sukistory/136)

### Inferences
- The Korean "flaw design" principle and the Japanese "lower the finish" principle (next section) are independent statements of the same rule, giving cross-language corroboration. The pixo "fish-scale" claim gives a mechanism for why quality-booster words hurt.
- Fitzpatrick/undertone specification is directly useful for LatAm/Brazil casting (e.g., "Fitzpatrick IV, warm olive undertone"). It lets you control skin tone instead of relying on vague ethnicity words, which may also counter the Asian-face bias some models show.
- The "실사화" route (design a fictional character as an illustration or character sheet, then photorealize it with an identity-lock prompt) is a clean way to create fully fictional avatars that resemble no real person. Japanese note.com has the same practice (anime→実写化), so two languages attest it.

### Gaps
- Naver Blog/Cafe posts did not surface. The full i-boss Seedream guide is DM-only. I found no Korean practitioner settings for Magnific, Krea or Enhancor, and no Korean reports on Nano Banana edit degradation ("화질 저하").

---

## Japanese: リアル人物プロンプト, AI美女 肌質感, note.com

### Takeaway
Japanese creators on note.com and X share long, bracket-structured prompts and JSON prompts for NBP and GPT Image 2. Recurring rules:
- Don't make the face too complete ("顔を完成させすぎない").
- Lower the finish (完成度を下げる) and add everyday-life noise (生活感のノイズ).
- Specify pores and vellus hair (産毛) to avoid doll skin.
- Use the smartphone front camera with slight wide-angle distortion and low-light graininess.
- Keep the lighting vague (window, everyday light).
- Fix one or two axes at a time.

A notable local aesthetic difference: popular JP prompts still request "滑らかで輝くような肌" (smooth, glowing skin) alongside "RAW 写真".

### Cited Findings
- **note.com "AIで実写と見分けがつかない美女を作るには" (そら, 2 Jan 2026, NBP):** the author says few people could tell which of four posted images were real, and gives three principles: lower the completeness (完成度を下げる), add everyday-life noise (生活感のノイズを入れる), don't over-complete the face (顔を完成させすぎない). Don't erase pores too much, weaken reflections, and keep lighting vague (window-side, ambient household light). [SS] — [note.com/sora2_yu0516](https://note.com/sora2_yu0516/n/nfdea80ba8204)
- **JSON prompts for "super-real" NBP portraits (Neiju @petabyte_ai, note):** specify pores and 産毛 (vellus hair) to avoid a doll texture. For phone feel use "スマホの前面カメラ" (phone front camera), selfie-style snap, "わずかな広角歪み" (slight wide-angle distortion) and "低照度のざらつき" (low-light graininess). [SS] — [note petabyte_ai 1](https://note.com/petabyte_ai/n/ndb4c1a006ebc); [note petabyte_ai 2](https://note.com/petabyte_ai/n/n914ab7f03be2)
- **Akari (note, "eradicating the AI look" with NBP JSON prompts):** write "自然な毛穴と軽い不完全さがあり、強いレタッチはしない" ("natural pores and slight imperfections, no heavy retouching") to avoid AI's slick skin. [SS] — [note open_duck7893](https://note.com/open_duck7893/n/n88745b943c30?hl=en)
- **CreativeEdge (note, video creators on NBP, 19 Dec 2025):** add guardrails: "自然な肌の微細テクスチャ、控えめな毛穴、ワックスのような肌を避ける、過度なシャープ化をしない" ("natural micro skin texture, subtle pores, avoid waxy skin, no excessive sharpening"). [SS] — [note creative_edge](https://note.com/creative_edge/n/nc548c6949157)
- **itou (note "マスタークラス"):** keep stray hairs / messy strands (後れ毛) for live-action realism. [SS] — [note itou_writing](https://note.com/itou_writing/n/n3f6ffa161138)
- **Bracketed prompt structure (川越あい @kawagoe_ai, X, 13 & 15 Oct 2026, NBP).** Verbatim [GH]:
  > [全体テーマ] 夕暮れの田舎道で、自分の靴を見て微笑む少女の日常スナップ。 [被写体 - 顔/服装] 顔と服装は添付画像を参照してください。 [被写体 - 表情] … [動作] … [被写体 - ポーズ] … [構図/撮影] 目線の高さでの全身ショット、被写体を中央に配置。… [光/雰囲気] 側面からの柔らかく拡散した太陽光が… フォトリアル。RAW 写真。滑らかで輝くような肌。スマートフォン画面向けに最適化された、9:16 の縦長ポートレート画像を作成してください。

  English: "[Overall theme] An everyday snapshot of a girl smiling while looking at her shoe on a country road at dusk. [Subject – face/outfit] Refer to the attached image for face and outfit. [Subject – expression] … [Action] … [Subject – pose] … [Composition/shot] Eye-level full-body shot, subject centred… [Light/mood] Soft diffused side sunlight… Photoreal. RAW photo. Smooth, glowing skin. Create a 9:16 vertical portrait optimized for smartphone screens."

  The ponytail variant ends the same way: "フォトリアリスティック。RAW 写真。滑らかで輝く肌。… 9:16…" and uses "浅い被写界深度により白い壁の背景が柔らかくぼかされています。側面からの自然な窓光" (shallow DOF softly blurring a white wall; natural side window light). The structure separates expression, action and pose into distinct blocks, with the pose described physically (weight on the left foot, right knee bent…), and delegates face and outfit to the reference image. — [YouMind repo (JA)](https://github.com/YouMind-OpenLab/awesome-nano-banana-pro-prompts/blob/main/README_ja-JP.md); [x.com/kawagoe_ai 1](https://x.com/kawagoe_ai/status/2110832080339042727); [x.com/kawagoe_ai 2](https://x.com/kawagoe_ai/status/2109970958341861447)
- **Section-structured GPT Image 2 prompt (Prompt アトリエ @CyberTotal2026, ~20 Sep 2026)** [GH]:
  - Sections: 主題 / 主要被写体 / 人物と表情 / 服装とポーズ / 背景と光 / 構図とカメラ / 質感とスタイル / ネガティブプロンプト (theme / main subject / person & expression / outfit & pose / background & light / composition & camera / texture & style / negative prompt).
  - Texture line: "フォトリアルな実写写真。サテン、ベルベット、大理石、ガラスの高解像度かつ深い光沢感、自然な肌の輝き。" ("Photoreal live-action photo. High-resolution, deep sheen of satin, velvet, marble and glass; natural skin glow.")
  - The negative is task-specific, not generic: "ドレスの色の変更、脚を組み替えること；グラスまたはバー照明の省略" ("changing the dress colour, re-crossing the legs; omitting the glass or bar lighting").
  - Source: [YouMind awesome-gpt-image-2 (JA)](https://github.com/YouMind-OpenLab/awesome-gpt-image-2/blob/main/README_ja-JP.md); [x.com/CyberTotal2026](https://x.com/CyberTotal2026/status/2101659894357139704)
- **Preservation-first edit wording (Eris Create Lab, X, ~22 Oct 2026, GPT Image 2 i2i)** [GH]:
  - Opening: "元画像の人物、衣装、構図、画風をそのまま維持し、被写界深度の浅い立体的なフォーカス表現を適用してください。ピントの中心は目と顔に合わせます。瞳孔、まつ毛、顔の主要な輪郭線はくっきりと保ってください。" ("Keep the person, outfit, composition and style of the original exactly; apply a shallow-DOF focus. Focus on the eyes and face; keep pupils, lashes and the main facial contours crisp.")
  - Closing guard: "画面全体を均一にぼかすことは禁止です。顔のディテールを消したりせず、元の線画や描画の質感をそのまま維持してください。" ("Uniformly blurring the whole frame is forbidden. Don't erase facial detail; keep the original texture.")
  - Source: [YouMind awesome-gpt-image-2 (JA)](https://github.com/YouMind-OpenLab/awesome-gpt-image-2/blob/main/README_ja-JP.md); [x.com/Eris_Create_Lab](https://x.com/Eris_Create_Lab/status/2113101283678691396)
- **"Shot on a phone" as a de-AI lever (WEBST8 blog):** turning it into an amateur snapshot ("スマホで撮ったような写真に") keeps colours from going over-vivid and pushes skin texture toward natural. [SS] — [webst8.com](https://webst8.com/blog/ai-image-howto/)
- **Fix 1–2 axes at a time (アレコレ散歩):** split fixes into 7 axes (光・構図・質感・生活感・動作・色・仕上げ: light, composition, texture, lived-in feel, motion, colour, finish) and change only one or two per iteration rather than all at once. [SS] — [arekoresanpo.com](https://arekoresanpo.com/ai-image-natural-prompt/)
- **Ten de-AI tactics for characters (kanekul):** avoid perfectly symmetrical faces, hide hands/fingers, simplify backgrounds, no in-image text, avoid naming existing styles; listed in priority order. [SS] — [kanekul.com](https://kanekul.com/articles/ai-character-shizensa-prompt)
- **Negatives against over-retouch (JP gallery summary):** "glossy plastic skin", "excessive retouching", "artificial skin glow". Stating an adult age (e.g., "30代の成人女性", a woman in her 30s) keeps faces from looking too young. [SS] — [media.io JP](https://www.media.io/ai/jp/explore/zone/chatgpt-ai-bijo-portrait-prompts)
- **Anime→photo ("実写化") practice:** a note.com article on naturally photorealizing anime illustrations with Nano Banana. [SS] — [note aliphyca](https://note.com/aliphyca/n/nf2545df936ea)
- **"Glass skin" contradiction:** a JP YouMind template asks for "iPhone で撮影したようなリアルなガラススキンの自撮りポートレート" (a realistic glass-skin selfie as if shot on iPhone) — [youmind JA](https://youmind.com/ja-JP/prompts/realistic-iphone-selfie-portrait-29759). Other guides warn that "glass skin" tends to produce plastic-looking results and recommend specular/highlight roll-off control instead. [SS] (search summary of mixed EN guides)

### Inferences
- Japanese popular prompts encode a local beauty norm (美肌, smooth radiant skin) even when asking for "RAW photo". For LatAm/Brazil UGC trust, the Korean/Russian/Brazilian "imperfection + lived-in" approach fits better. JP-style templates should be stripped of "滑らかで輝く肌" when localized.
- The bracketed/sectioned formats (theme → face via reference → expression → action → pose → composition → light → final realism line) are a reusable template for the client's prompt library, with the face always delegated to the reference image.
- Use task-specific negatives (what must not change in this image), as in Prompt アトリエ, rather than long generic negative lists.

### Gaps
- Full note.com article texts (JSON prompt bodies) were not retrievable; most JP items are [SS].
- No Japanese practitioner settings were found for Higgsfield Soul, Krea, Magnific or Enhancor, nor JP reports on edit degradation (画質劣化).

---

## French: prompt avatar IA réaliste, UGC IA

### Takeaway
French coverage was the thinnest: mostly vendor pages (Atlabs FR, Creatify FR, Morphic FR, Predis). Two practitioner items stand out: Génération IA's "photo-audit to JSON" loop (ChatGPT lists a photo's defects as JSON corrections, which are pasted with the photo into Nano Banana), and Azuro AI's macro skin template ("No makeup, no retouching", neutral white balance, no crushed blacks or blown highlights).

### Cited Findings
- **Génération IA newsletter (flint.media):** ask ChatGPT to spot a photo's defects and output the corrections as JSON, then paste that JSON with the photo into Nano Banana. Verbatim [SNIP]: "Je récupère le prompt Json et je le colle avec ma photo dans Nano Banana" ("I take the JSON prompt and paste it with my photo into Nano Banana"). The author notes you can prompt in French, and that the strength is edit and combination instructions. The article describes Gemini 2.5 Flash Image, so it is an older (2025) model. — [generationia.flint.media](https://generationia.flint.media/p/nano-banana-shooting-photo-virtuel-json-prompting)
- **Azuro AI "le prompt ultime pour Nano Banana Pro (réalisme parfait)":** an extreme macro template with placeholders for the facial zone and textures, natural imperfections, no makeup or retouching, razor-thin depth of field, soft but directional light, neutral white balance, cinematic contrast "without crushed blacks or blown highlights". [SS] The fragment [SNIP] "Natural imperfections including [SUBTLE FLAWS eg redness, uneven tone, tiny blemishes]. No makeup, no retouching." appeared in the French results and is probably from this template (attribution not fully confirmed). The page promotes a paid live course. — [azuro-ai.com](https://azuro-ai.com/blog/je-lai-trouve-le-prompt-ultime-pour-nano-banana-pro-realisme-parfait)
- **Base reference template (French gallery results):** [SNIP] "reference image of [subject], high resolution, natural skin texture, realistic lighting, soft shadows, clear facial features, clean details, [background], [camera angle], [style]". [SS] — [ideart.ai FR](https://ideart.ai/fr/nano-banana-pro-prompts)
- **French texture vocabulary:** "diffusion sous-surfacique" (subsurface scattering), "grain de film", "micro-textures de peau". [SS] — [starryai FR](https://starryai.com/fr/blog/nano-banana-prompts)
- **Morphic FR:** fix plastic skin by adding micro-texture (pores, fine lines), subtle colour variation between skin zones, and light imperfections. [SS] — [Morphic FR](https://morphic.com/fr/resources/how-to/fix-ai-generated-skin-realistic)
- **Atlabs FR:** describes NBP + Veo 3.1 UGC and lists over-smoothed skin among the classic defects. [SS] — [Atlabs FR](https://www.atlabs.ai/fr/blog/creer-videos-ugc-ia-realistes-guide-complet)
- **Higgsfield FR-language doc summaries:** iterate at 1K, then render finals at 2K or native 4K. Up to 14 character-reference images. NB2 keeps up to 5 consistent characters per scene. NBP has a "reasoning core" for faces, text and perspective. [SS] — [Higgsfield NB help](https://higgsfield.ai/creator-hub/help-center/ai-models/how-do-i-use-nano-banana)

### Inferences
- The "critic-to-JSON" loop (French) and CCFM's "ask the AI how to make it feel like a real shoot" (Korean) are the same practice: a vision model critiques the output and emits structured corrections. Attested in two languages.
- Splitting skin into zones with colour variation (Morphic FR) lines up with the Korean region-specific cues (cheek redness, nose pores, T-zone oil).

### Gaps
- No French influencer-agency or YouTuber practitioner prompts were retrievable (YouTube was blocked; searches surfaced vendors). French UGC-ad specifics are a gap.

---

## LatAm / Spain / Brazil scene and casting realism (local homes, kitchens, streets, phones, skin tones, styling)

### Takeaway
Only one source gave concrete Brazilian set dressing (Higor Cruz's beige-wall, light-laminate, charger-in-socket bedroom). Everything else for LatAm localization has to be built by the client: available kitchen/smartphone templates default to East Asian subjects, and some models (Seedream) skew toward refined Asian faces. Tools that help: Fitzpatrick/undertone skin-tone specification (Korean guide) and environment-only prompting with a reference-locked person (Brazilian guide).

### Cited Findings
- **Brazilian domestic set:** beige wall, light laminate floor, bed in background, charger in the socket, window light, 9:16. Clutter: "Garrafa d'água em cima da cômoda, carregador enfiado na tomada, toalha jogada, cama meio desfeita, uma plantinha no canto do banheiro." [SS/SNIP] — [higorprompts](https://higorprompts.substack.com/p/influencer-ia-o-detalhe-idiota-que)
- **Template default skew:** the es-419 kitchen/smartphone templates surfaced describe East Asian women. [SS] — [YouMind es-419 kitchen](https://youmind.com/es-419/prompts/realistic-kitchen-portrait-28844); [YouMind es-419 East Asian kitchen](https://youmind.com/es-419/prompts/asian-woman-modern-kitchen-portrait-29587)
- **Model casting bias:** Seedream tends to render Asians with refined faces (KR blog). [SS] — [dropshot](https://aistudio.dropshot.io/ko/blog/generated-ai-site-comparison)
- **Skin-tone control:** specify the Fitzpatrick type or undertone (warm/cool/olive). [SS] — [brunch @codept/45](https://brunch.co.kr/@codept/45)
- **Diversity-oriented generator (vendor):** WeShop's "AI Latina generator" page claims variety of skin tones and settings but gives no prompts. [SS] — [weshop.ai ES](https://www.weshop.ai/es/tools/ai-latina-generator)
- **Brazilian creator example subject:** "um homem de pele negra, por volta de 30 anos…" (a Black man around 30). [SNIP] — [alvaromendonca.com](https://alvaromendonca.com/nano-banana/)
- **Off-center framing and on-the-move capture (RU),** and **front-camera wide-angle distortion with low-light grain (JP):** these phone cues carry over to LatAm street and home UGC. — [klerk.ru](https://www.klerk.ru/blogs/oplatymru/680639/); [note petabyte_ai](https://note.com/petabyte_ai/n/n914ab7f03be2)

### Inferences
- Build per-market set libraries. Example props a search summarizer suggested for Mexico ("azulejos, comal, molcajete, olla de barro, ventana con reja") are not from a source; treat them as hypotheses to validate with local reviewers.
- Cast by Fitzpatrick type and undertone plus a region-plausible styling line (hair texture, everyday clothing, modest jewelry), and delegate the face to a reference sheet. This avoids the generic "latina" token, which may stereotype.
- Keep Instagram's synthetic-profile labelling in mind for organic accounts (see Spanish section).

### Gaps
- No source on typical LatAm phone models (e.g., Samsung Galaxy A, Motorola, Xiaomi) and how to emulate their rendering.
- No LatAm/Spain/Brazil-specific street or kitchen prompt from a native practitioner beyond the Brazilian bedroom.
- No CONAR (Brazil) or Spanish/LatAm ad-regulation research on AI testimonials (out of scope for this pass).

---

## Avoiding quality degradation when editing (reports from these language communities)

### Takeaway
Non-English sources confirm the degradation problem but give only lightweight fixes:
- Do edits in one step and edit from the original, not from edited copies.
- Select the whole image rather than small regions in some hosts.
- Iterate at 1K and render finals at 2K/4K.
- Add explicit "what must not change" clauses (face, hair, freckles, skin tone, composition), and forbid beautification and over-sharpening.

The only systematic evidence is an April 2026 arXiv paper showing that 100 iterative NBP replications degrade images in ways common no-reference quality metrics miss.

### Cited Findings
- **Banana100 (arXiv 2604.03400):** builds a dataset from 100 iterative image replications with Nano Banana Pro (chosen for popularity and Image Edit Arena standing). It finds that the no-reference quality metrics BRISQUE and NIQE fail to capture the degradation. It is a diagnosis, not a user-level fix. — [arXiv 2604.03400](https://arxiv.org/pdf/2604.03400)
- **Adobe community reports (NB inside Adobe, found via PT search):**
  - Regenerating from an NB output shifted tone and colour (more saturated/vibrant) and over-sharpened. — [Adobe bug report](https://community.adobe.com/bug-reports-403/generate-from-nano-banana-for-the-2nd-time-always-changed-the-image-tone-1483534)
  - Selecting a small area to edit produced distorted, stretched dimensions; selecting the whole image worked better. — [Adobe community](https://community.adobe.com/questions-700/nano-banan-issue-670360)
  - Both are user reports [SS].
- **Google AI dev forum:** a user reported that the NBP API returned visibly lower-quality images with possible pixelation or JPEG-like compression. [SS] — [discuss.ai.google.dev](https://discuss.ai.google.dev/t/nano-banana-pro-image-quality/134922)
- **Iterate low, finish high (Higgsfield doc):** start at 1K to iterate, then 2K or native 4K for finals. [SS] — [Higgsfield NB help](https://higgsfield.ai/creator-hub/help-center/ai-models/how-do-i-use-nano-banana)
- **Preservation clauses across languages:**
  - RU: "не менять лицо и волосы, не делать кукольную кожу, не размывать веснушки". — [vc.ru 2647149](https://vc.ru/ai/2647149-21-promt-dlya-generatsii-realistichnykh-foto)
  - PT: "preservando tom de pele, fisionomia e expressão". — [Canaltech](https://canaltech.com.br/apps/6-prompts-para-aproveitar-o-melhor-do-nano-banana-ao-editar-fotos-no-gemini/)
  - JA: "元画像の人物、衣装、構図、画風をそのまま維持し… 顔のディテールを消したりせず". — [YouMind GPT-Image-2 JA](https://github.com/YouMind-OpenLab/awesome-gpt-image-2/blob/main/README_ja-JP.md)
  - KO: forbid eye enlargement, chin reduction and beautification; avoid HDR, beauty filter, skin retouching and artificial sharpening. — [x.com/2_dam_e](https://x.com/2_dam_e/status/2106696827307516412)
  - JA: "過度なシャープ化をしない" (no excessive sharpening). — [note creative_edge](https://note.com/creative_edge/n/nc548c6949157)
- **Small steps:** change only 1–2 axes per iteration (JP) — [arekoresanpo](https://arekoresanpo.com/ai-image-natural-prompt/); start short and objective, then small variations (PT) — [Fast Company Brasil](https://fastcompanybrasil.com/ia/nano-banana-3-truques-para-criar-imagens-profissionais-com-a-ia/)

### Inferences
- Recommended SOP from this evidence:
  1. Keep a master file and always branch edits from it, not from the last edit.
  2. Batch the requested changes into a single edit prompt.
  3. Include a language-appropriate "do-not-change" clause: face, hair, freckles/moles, skin tone, composition.
  4. Avoid "high quality / ultra detail / sharpen" words in edit prompts (they risk over-sharpening and fish-scale artifacts).
  5. Do the resolution step last, with a fidelity upscaler (see Tools).
- Because BRISQUE/NIQE miss NBP iterative degradation, QA should rely on side-by-side human review at 100% zoom or reference-based comparison against the master, not no-reference scores.

### Gaps
- No native Spanish/Portuguese/Korean/Japanese source quantified how many NBP edit rounds are safe before visible loss.

---

## Tools: practitioner settings for Higgsfield Soul 2.0 / Soul ID, Krea, Magnific (formerly Freepik) Skin Enhancer / Upscaler / Precision, and Enhancor; which preserves identity best

### Takeaway
- **Higgsfield Soul:** presets carry the look, so write short prompts after choosing a preset. Soul ID wants about 20–80 clean, varied photos. Official help says Soul ID is for real people and points fictional characters to AI Influencer Studio or Soul Cast, but Higgsfield's own guide also suggests training Soul ID on 20+ generated portraits (conflict).
- **Magnific (Freepik rebranded to Magnific on 28 Apr 2026):**
  - The Skin Enhancer has Creative/Faithful/Flexible modes, sharpen 0–100, smart grain 0–100, and skin detail 0–100 (Faithful only, default 80).
  - Precision V2 defaults are sharpen 7, smart grain 7, ultra detail 30, with the "photo" flavor for portraits.
- **Krea Enhancer:** Strength vs Resemblance plus face-specific sliders. Krea's own recipe for real-looking portraits is 2x with near-zero creativity.
- **Enhancor:** exposes Skin Realism Level (default 0.10) and Skin Refinement Level, and is the one most often described as identity-preserving.

None of these rankings come from independent head-to-head tests, and no non-English practitioner shared numeric settings.

### Cited Findings
#### Higgsfield Soul 2.0 / Soul ID / AI Influencer / Soul Cast
- **Soul ID photo count:**
  - Official help center: train once on 20+ photos of one person, up to 80; the face then holds across styles, poses and lighting. — [Higgsfield help: Soul ID](https://higgsfield.ai/creator-hub/help-center/ai-models/how-do-i-create-and-use-a-soul-id-character)
  - A Higgsfield blog says 5+ photos inside Soul 2.0 or Soul Cinema. — [Higgsfield blog persona](https://higgsfield.ai/blog/how-to-turn-photo-into-consistent-ai-persona-creator)
  - A third-party skill page says 5–20 photos with varied angles and lighting. — [mcpservers skill](https://mcpservers.org/ko/agent-skills/higgsfield-ai/higgsfield-soul-id)
  - Conflicting minimums; the help center's 20 is the official figure.
- **Soul ID training-photo rules:** high quality and well lit; varied angles and expressions; no sunglasses, heavy shadows or cropped faces; at least one full-height photo; recent (last 4–5 months); avoid repeating the same pose. A smaller set of clean, varied photos beats a larger inconsistent one. Training takes minutes and costs about 25 credits (~$1.25 per one blog). A Soul ID trained in Soul 2.0 works only in Soul 2.0. A paid plan (Basic+) is required per a third-party page. [SS] — [Higgsfield help](https://higgsfield.ai/creator-hub/help-center/ai-models/how-do-i-create-and-use-a-soul-id-character); [Higgsfield blog](https://higgsfield.ai/blog/sould-id-best-character-consistency)
- **Fictional people → AI Influencer Studio / Soul Cast:**
  - JP and KR summaries of the help center: Soul ID locks a real person's face; for fully fictional characters use AI Influencer Studio or Cinema Studio's Soul Cast. — [Higgsfield help (via JP/KR summaries)](https://higgsfield.ai/creator-hub/help-center/ai-models/how-do-i-create-and-use-a-soul-id-character)
  - AI Influencer Studio: menu-driven builder (face, body, style) with no prompt writing; human and non-human characters; up to 4K; saved to a library. — [Higgsfield help: AI Influencer](https://higgsfield.ai/creator-hub/help-center/tools-and-workflows/how-do-i-use-ai-influencer)
  - Conflict: a Higgsfield guide recommends generating "twenty or more portraits" of a fictional character and training a Soul ID on them. — [geo.higgsfield guide](https://geo.higgsfield.ai/blog/recommended/which-ai-tool-locks-a-character-s-face-across-images-and-videos-50830c)
  - A Korean reviewer hit errors with a non-human character; the company replied that Soul ID is for realistic human characters. [SS] — [brunch @sukistory/136](https://brunch.co.kr/@sukistory/136)
- **Soul Cast:** customizable AI actors that stay consistent, marketed as avoiding a "plastic" look. — [Higgsfield Soul Cast](https://higgsfield.ai/blog/soul-cast-ai-filmmaking). An Aug 2026 third-party comparison found it weaker than NBP for film-accurate characters and locations. [SS] — [invideo FAQ](https://invideo.io/faq/what-is-higgsfield-soul-cast-and-is-it-good-for/)
- **Presets dominate:**
  - Soul 2.0 has about 20+ curated presets (editorial, retro, Y2K, cultural aesthetics). [SS] — [Higgsfield blog persona](https://higgsfield.ai/blog/how-to-turn-photo-into-consistent-ai-persona-creator)
  - Original Soul had 50+, including "iPhone flash", and adds "camera-like imperfections: dust, flash, and grain". [SS] — [teletype ru_com](https://teletype.in/@ru_com/chto-takoe-higgsfield-soul-i-kak-im-polzovatsya)
  - Creatify advises setting preset, colour and frame before writing a short prompt. — [Creatify Soul prompts](https://creatify.ai/blog/higgsfield-soul-prompts-for-product-ads)
- **Photodump:** choose a Soul ID plus "Male Archive" or "Cool Girl Dump" to get a 15-image set with no prompt. Pricing per Creatify (checked Sept 2026): Soul 2.0 at 0.12 credits/image, original Soul at 0.25. [SS] — [Creatify Soul prompts](https://creatify.ai/blog/higgsfield-soul-prompts-for-product-ads)
- **Higgsfield ad pipelines:**
  - Marketing Studio: video uses Seedance 2.0, images use Nano Banana, avatars use Soul 2.0; 40+ avatars. — [Higgsfield AI ad generator](https://higgsfield.ai/ai-ad-generator)
  - UGC Factory (Sep 2025): Nano Banana-powered, 40+ templates, 4 product keyframes per generation. — [Higgsfield UGC Factory](https://higgsfield.ai/blog/Higgsfield-UGC-Factory-Explained)
- **Higgsfield Skin Enhancer:** modes from subtle to heavy. A reviewer advises against "Imperfect Skin" because it adds excessive blemishes. One-click, built-in 4K, less manual control. [SS] — [Creative Pad Media](https://www.creativepadmedia.com/make-ai-skin-realistic-with-1-click-higgsfield-skin-enhancer/); [imageat compare](https://imageat.com/compare/magnific-vs-higgsfield)

#### Krea
- **Enhancer controls (official docs, also localized in ja/ru/pt-BR/fr):**
  - Strength sets how much extra detail the AI invents; higher is sharper with more interpretation.
  - Higher Resemblance keeps output closer to the original.
  - Face detection unlocks Face Creativity and Face Strength (for Topaz and all models).
  - Higher upscale factors give the AI more room to modify textures and edges.
  - Sources: [Krea docs Enhancer](https://docs.krea.ai/user-guide/features/enhancer); [Krea docs RU](https://www.krea.ai/docs/ru/user-guide/features/enhancer); [Krea docs pt-BR](https://www.krea.ai/docs/pt-BR/user-guide/features/enhancer)
- **Krea's own 2026 upscaler recipes:** fidelity upscalers suit real people and products, and picking the wrong family is "why upscaled portraits grow strange skin". Real photos: 2x, creativity at or near 0, mask faces and logos if region control exists. AI images: 2–4x, medium creativity, one pass, inspect edges, then one low-creativity pass if geometry drifted. [SS] — [Krea blog upscalers 2026](https://www.krea.ai/blog/best-ai-image-upscalers-in-2026)
- **Krea 1:** 1.5K native resolution; Enhancer up to 4K; marketed as photoreal skin. [SS] — [Krea docs JA Krea 1](https://www.krea.ai/docs/ja/user-guide/features/krea-1.md)

#### Magnific (formerly Freepik)
- **Rebrand:** Freepik consolidated its AI suite under the Magnific name at magnific.com on 28 Apr 2026; magnific.ai remains as the legacy service. [SS] — [Jerrod Lew newsletter](https://jerrodlew.beehiiv.com/p/freepik-is-now-magnific); [Oakgen (competitor-disclosed)](https://oakgen.ai/blog/magnific-ai-freepik-rebrand-pricing)
- **Skin Enhancer parameters (ComfyUI node docs and Wireflow):**
  - Modes: creative (artistic), faithful (preserve original), flexible (targeted fixes).
  - Sharpen 0–100 and Smart Grain 0–100.
  - Skin Detail 0–100, applies only in Faithful, default 80.
  - "Optimized for" (Flexible only): enhance_skin, improve_lighting, enhance_everything, transform_to_real, no_make_up.
  - Input at least 160 px; aspect ratio 1:3 to 3:1 (not strictly enforced).
  - Sources: [ComfyUI Magnific Skin Enhancer node (KO)](https://docs.comfy.org/ko/built-in-nodes/MagnificImageSkinEnhancerNode); [Wireflow node docs](https://www.wireflow.ai/docs/nodes/process--magnific_skin_enhancer)
- **Freepik/Magnific guidance:** don't over-correct, keep natural marks (freckles, wrinkles), avoid extra filters that undo the result ("improve, don't erase"). — [Freepik blog plastic skin](https://www.freepik.com/blog/how-to-fix-plastic-skin-ai-skin-enhancer/)
- **Precision V2 (Magnific API docs):**
  - Sharpen default 7; Smart Grain default 7 ("adds natural texture to avoid artificial smoothing"); Ultra Detail default 30; all 0–100. Start from the defaults.
  - Flavors: sublime (art/illustration), photo (natural colours, realistic detail; positioned for portraits, editorial and campaigns), photo_denoiser (noisy photos).
  - Sources: [Magnific Precision V2 API](https://docs.magnific.com/api-reference/image-upscaler-precision-v2/overview); [Magnific Precision v2 blog](https://www.magnific.com/blog/magnific-precision-v2/)
  - The video-upscaler guidance (Natural flavor at 0% creativity for close-ups and portraits; high sharpen causes halos and brittle hair; too much grain hides real detail) is for video but is the closest official portrait advice. [SS] — [seedance.tv guide](https://www.seedance.tv/blog/magnific-ai-video-upscaler-settings)
- **Upscaler modes and presets:** Creative (reimagine) vs Precision (preserve structure); a "Portraits" preset "perfects facial features, skin tones, and softness". A Spanish 2025 review says the portrait setting improves skin, facial details and eyes without an unnatural look. Magnific Precision is listed at 90 credits per 2K image (single source). [SS] — [Freepik docs upscale](https://cn.freepik.com/ai/docs/upscale-images); [wwwhatsnew ES 2025](https://wwwhatsnew.com/2025/02/12/el-nuevo-upscaler-de-magnific-en-freepik-revolucion-en-la-mejora-de-imagenes/)

#### Enhancor
- **Official controls:** Skin Refinement Level (raw → refined); Skin Realism Level (default 0.10, scale ending at "stylized"); Freckle Control with intensity for V3 and V4; selective-area enhancement; HD up to 4K on higher tiers; in-app tutorials ("Enhancor University") including AI-influencer workflows. [SS] — [enhancor.ai](https://www.enhancor.ai/); [Enhancor University](https://app.enhancor.ai/university); [aitoolcurator](https://www.aitoolcurator.com/ai-tools/design-creativity/enhancor/)
- **Reviewer usage:** "Heavy Mode" plus the Texture Control slider turned a plastic Midjourney portrait into one with believable pores and micro-texture; no numbers given. [SS] — [techpilot.ai](https://techpilot.ai/tools/enhancor-ai-fix-the-ai-plastic-skin/)
- **Generic tutorial:** Auto/Light/Heavy modes; Auto recommended for most users; high intensity "can sometimes introduce artifacts or alter facial structure slightly". [SS] — [aiindigo tutorial](https://aiindigo.com/tutorials/getting-started-with-enhancor-fixing-plastic-ai-skin)
- **Competitor critique:** entry tier capped at 1080p; reliability complaints. From Upsampler, a competitor. [SS] — [upsampler.com](https://upsampler.com/best-enhancor-ai-alternative)

#### Which preserves identity best (as reported)
- Vendor/affiliate guides rate Enhancor as constrained to preserve identity and geometry, and Magnific (especially creative modes) as most aggressive, sometimes changing face geometry or adding elements. Higgsfield is the one-click all-in-one. — [chasejarvis.com 2026 upscaler guide](https://chasejarvis.com/blog/best-ai-image-upscaler/); [letsenhance.io](https://letsenhance.io/blog/all/best-ai-image-enhancers/); [imageat](https://imageat.com/compare/magnific-vs-higgsfield)
- Caveats:
  - One summary claimed Magnific's skin results come only as a side effect of general re-generation, which conflicts with the existence of the dedicated Skin Enhancer with a Faithful mode. [SS]
  - A Higgsfield-vs-Magnific comparison rates Higgsfield's face consistency as a strength and Magnific's as limited, but that comparison is about generation, not skin enhancement. — [imageat](https://imageat.com/compare/magnific-vs-higgsfield)
  - No independent same-portrait test across Enhancor, Magnific, Higgsfield and Krea was found.

### Inferences
- For fictional avatars at scale on Higgsfield: build the character in AI Influencer Studio (or generate a reference set elsewhere), then confirm with Higgsfield whether Soul ID training on generated portraits is allowed for your plan and terms. The help center and the guides conflict.
- Starting points for identity-safe skin realism (derived from the docs, not tested):
  - Magnific Skin Enhancer in Faithful mode, skin detail at or below the 80 default, smart grain and sharpen low (e.g., 5–15).
  - Magnific Precision V2 with the photo flavor at defaults (sharpen 7, grain 7, ultra detail 30), lowering ultra detail if skin turns crunchy.
  - Krea at 2x with low Strength and high Resemblance, face creativity low.
  - Enhancor at a low Skin Realism Level (0.10 default) with Freckle Control off or low for brand-safe faces.
  - Composite skin-only with a mask if eyes or teeth drift.
- Avoid "Imperfect Skin"/heavy modes on hero shots; reviewers report excessive blemishes and facial-structure drift at high intensity.

### Gaps
- No non-English practitioner (ES/PT/RU/KO/JA/FR) shared numeric settings for Magnific, Krea or Enhancor. All numbers above are vendor or API defaults.
- No published head-to-head identity-drift measurement exists across these tools.
- Higgsfield's position on Soul ID for generated (fictional) faces is inconsistent across its own pages.
- Krea 2 / Krea 3 enhancer behaviour for portraits was not found in non-English sources (Krea 3, released 15 Oct 2026, is covered in note 01).

---

## Unique tricks from these communities not common in English sources (with corroboration level)

### Takeaway
The most distinctive non-English contributions:
1. Quality-booster words backfire (KR, JA; mechanism claimed by KR pixo).
2. Design the flaws and describe skin region by region instead of piling on negatives (KR).
3. Put the realism budget into lived-in environmental clutter and let the reference image carry the face (PT-BR, JA).
4. Phone-pipeline artifacts in the prompt, such as soft JPEG compression, micro-smear and slight under-exposure (RU).
5. Photorealize an illustrated or designed character ("실사화 / 実写化") to make a fully fictional face (KR, JA).
6. A vision-model critic loop that emits JSON corrections (FR, KR).

### Cited Findings
- **Quality words backfire** — corroborated in 2 languages, 4 sources:
  - KR CCFM: "고퀄리티", "매우 사실적", "완벽한 피부" lead to doll-like results. — [CCFM](https://blog.ccfmedu.co.kr/ai-realistic-portrait-creation)
  - KR i-boss: repeating "사실적/고퀄리티" makes the texture overly perfect. — [i-boss](https://www.i-boss.co.kr/ab-6141-68347)
  - KR pixo: "고화질/풍부한 디테일" leads to fish-scale skin in GPT Image. — [pixo](https://pixo.video/ko/blog/gpt-image-fish-scale-fix)
  - JA そら: 完成度を下げる (lower the finish). — [note sora](https://note.com/sora2_yu0516/n/nfdea80ba8204)
- **Flaw design and region-specific skin** — 2–3 KR sources: nose pores, cheek redness, freckles, faint T-zone oil, baby hairs; "detail description beats negatives". — [i-boss](https://www.i-boss.co.kr/ab-6141-68347); [CCFM](https://blog.ccfmedu.co.kr/ai-realistic-portrait-creation); [brunch @codept](https://brunch.co.kr/@codept/45). A zone-wise colour-variation idea also appears in FR Morphic. — [Morphic FR](https://morphic.com/fr/resources/how-to/fix-ai-generated-skin-realistic)
- **"Background as texture, not space" and "light's character over direction"** — single KR source (CCFM). — [CCFM](https://blog.ccfmedu.co.kr/ai-realistic-portrait-creation)
- **Lived-in clutter and environment-only prompting** — 2 languages:
  - PT-BR Higor Cruz (clutter list; describe only the environment). — [higorprompts](https://higorprompts.substack.com/p/influencer-ia-o-detalhe-idiota-que)
  - JA そら (生活感のノイズ) and アレコレ散歩 (生活感 as one of 7 axes). — [note sora](https://note.com/sora2_yu0516/n/nfdea80ba8204); [arekoresanpo](https://arekoresanpo.com/ai-image-natural-prompt/)
- **Phone-pipeline artifacts** — 2 RU sites agree, 1 RU site contradicts:
  - neuroluv: "мягкое JPEG-сжатие… лёгкая микросмазка" (soft JPEG compression… slight micro-smear). — [neuroluv](https://neuroluv.ru/prompts/zimniy-strit-realistichnyy-iphone-kadr-108)
  - prompt1: "слегка заниженная экспозиция, естественный шум" (slightly under-exposed, natural noise). — [prompt1.ru](https://prompt1.ru/listing/prompt-semka-na-iphone/)
  - Contradicted by VC.ru's selfie list, which puts noise in the negative. — [vc.ru 2681566](https://vc.ru/reviews/2681566-prompty-dlya-selfi-2026-luchshie-neyroseti-i-sovety)
  - JA adds front-camera slight wide-angle distortion and low-light grain. — [note petabyte_ai](https://note.com/petabyte_ai/n/n914ab7f03be2)
- **Break symmetry and center** — 3 sources, 2 languages: RU Klerk (off-center; symmetry gives it away), JA kanekul (avoid perfectly symmetric faces), RU Habr (slight expression asymmetry as a realism cue). — [klerk.ru](https://www.klerk.ru/blogs/oplatymru/680639/); [kanekul](https://kanekul.com/articles/ai-character-shizensa-prompt); [Habr 1009882](https://habr.com/ru/articles/1009882)
- **실사화 / 実写化 (illustration → photo) with an identity lock** — 2 languages:
  - KR Min.5 prompt (verbatim opening above). — [x.com/2_dam_e](https://x.com/2_dam_e/status/2106696827307516412)
  - JA note on anime→photo with Nano Banana. — [note aliphyca](https://note.com/aliphyca/n/nf2545df936ea)
- **Critic loop to structured corrections** — 2 languages:
  - FR Génération IA: ChatGPT lists defects as JSON, which are pasted with the photo into Nano Banana. — [flint.media](https://generationia.flint.media/p/nano-banana-shooting-photo-virtuel-json-prompting)
  - KR CCFM: ask the AI how to make it feel like a real shoot. — [CCFM](https://blog.ccfmedu.co.kr/ai-realistic-portrait-creation)
  - ES: a custom GPT upgrades basic prompts to NBP-optimized ones. — [lilys.ai ES](https://lilys.ai/es/notes/nano-banana-pro-20251207/viral-ugc-nano-banana-pro)
- **Fitzpatrick/undertone skin-tone specification** — single KR source; useful for LatAm casting. — [brunch @codept](https://brunch.co.kr/@codept/45)
- **Separate expression / action / pose blocks with physical pose description and face delegated to the reference** — JA @kawagoe_ai (2 prompts, Oct 2026). — [YouMind JA repo](https://github.com/YouMind-OpenLab/awesome-nano-banana-pro-prompts/blob/main/README_ja-JP.md)
- **Task-specific negatives** (only what must not change in this image) — JA Prompt アトリエ. — [YouMind GPT-Image-2 JA](https://github.com/YouMind-OpenLab/awesome-gpt-image-2/blob/main/README_ja-JP.md)
- **Edit-time micro-feature guard** "не размывать веснушки" (don't blur freckles) — RU VC.ru. — [vc.ru 2647149](https://vc.ru/ai/2647149-21-promt-dlya-generatsii-realistichnykh-foto)
- **Local aesthetic divergence** — JA prompts still ask for "滑らかで輝く肌" (smooth, glowing skin) with "RAW 写真". — [YouMind JA repo](https://github.com/YouMind-OpenLab/awesome-nano-banana-pro-prompts/blob/main/README_ja-JP.md)

### Inferences
- The client's prompt standard can combine these into one template:
  1. Reference-locked face (character sheet; optionally a 실사화 of a designed illustration).
  2. Physically described pose, separate from expression and action.
  3. Environment-heavy, market-specific clutter.
  4. Region-specific skin cues with a Fitzpatrick/undertone tag.
  5. One dominant, loosely described everyday light.
  6. Phone-pipeline cues for UGC only (front/rear camera, slight wide-angle, mild JPEG/noise, off-center).
  7. A short, task-specific "do-not-change" negative.
  8. No "high quality / ultra-realistic / perfect skin" boosters.
- The parallel ideas across Korean, Japanese, Brazilian and Russian sources were reached independently, which raises confidence beyond any single vendor blog. They should still be A/B-tested per model (NBP, NB2, GPT Image 2, Seedream, Soul 2.0).

### Gaps
- Most items are [SS]. Verbatim full prompts from note.com, brunch, VC.ru and Substack could not be fetched. A follow-up with page access, or manual retrieval, should capture the full texts of: CCFM's 6-step guide, the i-boss Seedream guide, the VC.ru 21-prompt article, Neiju's JSON prompts, Higor Cruz's 5 Brazilian prompts, and Azuro AI's template.
- I did not verify that any of these tricks improves ad performance (CTR or conversion) in LatAm or Brazil. No such data was found.
