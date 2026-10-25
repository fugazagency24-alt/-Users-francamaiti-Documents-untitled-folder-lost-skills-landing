# Prompt engineering for ultra-photorealistic AI avatars: prompt structure, camera/lens language and lighting (state as of Oct 2026)

> Research-process note for the report writer. Many primary pages (docs.bfl.ai, blog.google, ai.google.dev, developers.openai.com, docs.midjourney.com, huggingface.co, fal.ai, Wikipedia) could not be fetched from this sandbox (DNS failure or proxy policy denial), and the shared web-search budget ran out partway through. So:
> - **OpenAI** guidance is quoted **verbatim** from the official cookbook notebooks on GitHub (fully read).
> - **Qwen-Image** and **Z-Image** settings come from their official GitHub READMEs (read).
> - **Google / BFL / Seedream / Midjourney / Imagen** guidance comes from search-engine summaries of the official pages plus third-party mirrors. These are marked where relevant.
> - Community prompts are quoted verbatim from GitHub prompt-collection repos, which credit the original X/Twitter authors.
> - Prompts labelled "SOP-built" are my own syntheses of the cited principles. They are not copied from a source and have not been test-rendered.

---

## 1. Prompt anatomy: order, structure (prose vs tags vs JSON), length, and the role of the text encoder

### Takeaway
Every current model uses an LLM or VLM as its text encoder: GPT Image 2, Nano Banana Pro/2, FLUX.2 (Mistral-Small-3.2-24B), Qwen-Image, and Z-Image. They all reward **natural-language scene descriptions written like a photographer's brief**, ordered roughly **scene/context → subject (identity, age, ethnicity, wardrobe) → action/pose/gaze → environment details → camera/framing → lighting → texture/realism cues → constraints/exclusions**. JSON and labelled-segment prompts work well when a team needs maintainable templates. They are not magic, and OpenAI explicitly says any format works as long as intent and constraints are clear. SD1.5/SDXL-era comma-separated tag soups with weights such as `(masterpiece:1.2)` are legacy for these models.

### Cited Findings
- **OpenAI (gpt-image-2 guide, dated April 21 2026), verbatim:** "Write prompts in a consistent order (background/scene → subject → key details → constraints) and include the intended use (ad, UI mock, infographic) to set the 'mode' and level of polish. For complex requests, use short labeled segments or line breaks instead of one long paragraph." — [OpenAI Cookbook: GPT Image Generation Models Prompting Guide](https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide) / [notebook source on GitHub](https://github.com/openai/openai-cookbook/blob/main/examples/multimodal/image-gen-models-prompting-guide.ipynb)
- **OpenAI, verbatim:** "Use the format that is easiest to maintain. Minimal prompts, descriptive paragraphs, JSON-like structures, instruction-style prompts, and tag-based prompts can all work well as long as the intent and constraints are clear. For production systems, prioritize a skimmable template over clever prompt syntax." — [OpenAI Cookbook (GitHub)](https://github.com/openai/openai-cookbook/blob/main/examples/multimodal/image-gen-models-prompting-guide.ipynb)
- **OpenAI on people, verbatim:** "For people in scenes, describe scale, body framing, gaze, and object interactions. Examples: 'full body visible, feet included,' … 'looking down at the open book, not at the camera,' or 'hands naturally gripping the handlebars.' These details help with body proportion, action geometry, and gaze alignment." — [OpenAI Cookbook (GitHub)](https://github.com/openai/openai-cookbook/blob/main/examples/multimodal/image-gen-models-prompting-guide.ipynb)
- **OpenAI on iteration, verbatim:** "Long prompts can work well, but debugging is easier when you start with a clean base prompt and refine with small, single-change follow-ups ('make lighting warmer,' 'remove the extra tree,' 'restore the original background')." — [OpenAI Cookbook (GitHub)](https://github.com/openai/openai-cookbook/blob/main/examples/multimodal/image-gen-models-prompting-guide.ipynb)
- **Google (Gemini 2.5 Flash Image / Nano Banana guide):** recommends thinking like a photographer, naming camera angles, lens types, lighting and fine details. Its photorealistic template has four parts: (1) shot type + subject + setting, (2) lighting and mood, (3) camera/lens with emphasis on texture, (4) aspect ratio. The worked example is a close-up portrait of an elderly ceramicist in a sunlit workshop, using an 85mm lens with a soft, blurred background, in vertical orientation. — [Google Developers Blog: How to prompt Gemini 2.5 Flash Image Generation for the best results](https://developers.googleblog.com/en/how-to-prompt-gemini-2-5-flash-image-generation-for-the-best-results/) (content via search summary)
- The same Google guidance is commonly paraphrased as "describe the scene, don't just list keywords": "a descriptive paragraph will almost always produce a better image than a list of disconnected words." — [MindPal summary of Google's guide](https://mindpal.space/blog/how-to-prompt-gemini-2-5-flash-image-generation-for-the-best-results-a1b2c3)
- A community skill distils Google's guide into the template "Photorealistic [SHOT TYPE] of [SUBJECT], [ACTION], in [ENVIRONMENT]." It adds camera/lighting lines such as "Shot with 85mm f/2.0, studio three-point lighting creates gentle shadows defining facial features." — [secondsky/claude-skills nano-banana-prompts SKILL.md](https://github.com/secondsky/claude-skills/blob/main/plugins/nano-banana-prompts/skills/nano-banana-prompts/SKILL.md)
- **Google Cloud (March 5 2026):** the Nano Banana models "are built on the Gemini 3 family of models" and reason through a prompt before generating an image. — [Google Cloud Blog: The ultimate Nano Banana prompting guide](https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-nano-banana) (via search summary)
- Current Gemini image model IDs listed in Google's official cookbook: `gemini-3-pro-image-preview` (Nano Banana Pro), `gemini-3.1-flash-image` (Nano Banana 2), `gemini-3.1-flash-lite-image` (Nano Banana 2 Lite), `gemini-nano-banana-2.1` (Nano Banana 2.1). By default the model outputs 1:1 unless it is matching input images. Aspect ratio is set through `image_generation_config`. — [google-gemini/cookbook Get_Started_Nano_Banana.ipynb](https://github.com/google-gemini/cookbook/blob/main/quickstarts/Get_Started_Nano_Banana.ipynb)
- **FLUX.2 text encoder:** FLUX.2 [dev] uses **Mistral-Small-3.2-24B-Instruct-2506** for text encoding. The README says it "benefits significantly from prompt upsampling", which can run locally with that same Mistral model or through any model on OpenRouter. — [black-forest-labs/flux2 README](https://github.com/black-forest-labs/flux2)
- BFL's upsampling doc says upsampling is "particularly effective for prompts requiring reasoning or complex interpretation" (text in images, annotated image instructions, code/math visualisations) and may add little for simple prompts. — [flux2 docs: flux2_with_prompt_upsampling.md](https://github.com/black-forest-labs/flux2/blob/main/docs/flux2_with_prompt_upsampling.md)
- **FLUX.2 JSON:** BFL's guide says FLUX.2 is trained to understand structured JSON prompts, which give precise control over subjects, composition, lighting and camera settings. Third-party mirrors of the template use keys for scene, subjects, style, colour palette, lighting, mood, background, composition and camera. — [BFL FLUX.2 prompting guide](https://docs.bfl.ai/guides/prompting_guide_flux2); [Atlabs FLUX.2 prompting guide](https://www.atlabs.ai/blog/flux-2-prompting-guide); [Pletor FLUX.2 docs](https://docs.pletor.ai/model-library/image-models/flux-2) (via search summary)
- **Nano Banana Pro JSON (third-party claim):** key-value JSON prompts are said to reduce "concept bleeding" between elements. — [Atlabs: Nano Banana Pro JSON prompting guide](https://www.atlabs.ai/blog/nano-banana-pro-json-prompting-guide-master-structured-ai-image-generation). VEED also lists JSON-structured prompts as a Nano Banana Pro best practice. — [VEED Nano Banana Pro guide](https://www.veed.io/learn/nano-banana-pro-prompts)
- **Qwen-Image official prompt rewriter** (the system prompt Qwen uses to expand prompts):
  - Write **one continuous descriptive block**; lists, headings and numbering are prohibited.
  - About **200 words for English portraits**, and **under 150 Chinese characters** for Chinese portraits ("人像场景下…输出控制在150字以内").
  - Portrait order: ethnicity, gender and a specific age or narrow age range first, then prominent features, then pose and environment. The Chinese version fixes the order as identity → clothing/accessories → face/skin → pose/action → background.
  - Always name the overall style. Put visible text in double quotes, or state that the image contains no recognizable text.
  - [QwenLM/Qwen-Image prompt_utils_2512.py](https://github.com/QwenLM/Qwen-Image/blob/main/src/examples/tools/prompt_utils_2512.py)
- **Seedream 4.5 (third-party):** lead with the subject, then style, lighting and composition. Overly long prompts can confuse the model. — [fal Seedream 4.5 prompt guide](https://fal.ai/learn/devs/seedream-v4-5-prompt-guide). Fliki recommends ~30–100 words and says the model weights earlier concepts more heavily. — [Fliki: Seedream 4.5](https://fliki.ai/models/image/seedream-4-5)
- **Imagen 4 (Vertex AI):** the official guide frames prompts around subject, context/background and style. It says prompts "don't need to be long or complex" but should be descriptive and clear. — [Vertex AI prompt and image attribute guide](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/image/img-gen-prompt-guide). The prompt rewriter is **enabled by default** for Imagen 4 generate models, and the API returns the rewritten prompt only when the original has fewer than 30 words. — [Vertex AI: use prompt rewriter](https://cloud.google.com/vertex-ai/generative-ai/docs/image/use-prompt-rewriter?hl=es-419)
- Atlabs (Oct 2025) recommends opening Imagen 4 prompts with "A photo of..." to engage its photorealistic mode. — [Atlabs Imagen 4 prompting guide](https://www.atlabs.ai/blog/imagen-4-prompting-guide)
- **Conflicting specs and overload:** VEED warns against contradictory specs (e.g., "shallow depth of field" paired with "f/16") and against stacking more than ~10 competing style directions. — [VEED Nano Banana Pro guide](https://www.veed.io/learn/nano-banana-pro-prompts)

### Inferences
- **Recommended SOP anatomy**, consistent with the OpenAI, Google, Qwen and Seedream ordering advice:
  1. **Medium + use-case line:** "Photorealistic smartphone photo for a UGC-style skincare ad…"
  2. **Subject identity:** age range, ethnicity, gender, build, hair, wardrobe with fabric.
  3. **Action / pose / gaze / hands:** what they are doing with the product.
  4. **Environment:** 3–6 specific, mundane props.
  5. **Camera:** device class, lens/focal-length class, angle, distance, framing, DOF.
  6. **Lighting:** source, direction, quality, colour temperature, plus any mixed sources.
  7. **Texture/realism cues:** skin, fabric, sensor noise.
  8. **Constraints:** no text, no watermark, no retouching, keep identity. For Nano Banana, FLUX and Seedream, phrase these as positive descriptions where possible.
- Because the encoders are LLMs, **grammar and relationships matter.** "Her left hand holds the jar at chin height, label facing camera" is parsed correctly. CLIP-era tag lists lose these relations.
- **Use JSON when** (a) a team of operators fills fields at scale, (b) you need to swap one variable (outfit, location) while freezing the others, or (c) you want HEX-locked brand colours (FLUX.2). **Use prose when** you want natural scene coherence. A good hybrid is **labelled segments** (Scene / Subject / Camera / Lighting / Texture / Constraints), which OpenAI explicitly endorses.
- **Length guidance by model, synthesised from the sources above:**

  | Model | Suggested length |
  |---|---|
  | GPT Image 2 | 80–200 words in labelled segments |
  | Nano Banana Pro/2 | 60–180-word narrative paragraph |
  | FLUX.2 pro/max | 40–150 words, or JSON |
  | FLUX.2 dev | run upsampling, or write long prompts yourself |
  | Seedream 4.5/5 | 30–100 words, subject first |
  | Qwen-Image | ~200 words in one block |
  | Imagen 4 | >30 words, so the rewriter doesn't heavily reinterpret it, or disable the rewriter if available |
  | Midjourney | short (see section 2) |

### Gaps
- I could not fetch BFL's FLUX.2 guide verbatim. Claims I remember but could not re-verify this session: the "Subject + Action + Style + Context" framework, the statement that word order/priority matters (earlier words weighted more), and the short/medium/long length bands.
- I could not verify the claim that the official ByteDance Seedream guide recommends "[Subject + Action + Setting] + [Style]" and under 600 words. It appeared only as a third-party paraphrase in search results, and I did not find the original page.
- The Qwen-Image and Z-Image text encoders were not confirmed in the pages read (believed to be Qwen2.5-VL and Qwen3-4B respectively; unverified).
- No official Google statement on JSON prompts was found. The JSON trend for Nano Banana is community-driven.

---

## 2. Official guides: exact recommendations per model

### Takeaway
The official guides converge on the same points: photographic language, explicit real-world texture, natural light, and explicit invariants. They differ in mechanics:

| Model | Mechanics |
|---|---|
| OpenAI | wants the word "photorealistic", intended use, and `quality="high"` for close-up portraits |
| Google | wants narrative paragraphs and "cinematographer" direction |
| FLUX.2 | wants named camera/lens/film stocks, supports JSON and HEX, and has no negative prompts |
| Qwen-Image | ships a negative-prompt list aimed at the "AI look", plus CFG/steps defaults |
| Z-Image Turbo | must run at guidance 0 |
| Midjourney V8 | uses `--raw` plus low stylize |

### Cited Findings
**OpenAI (gpt-image-2; gpt-image-1.5 guide has the same photorealism section)**
- Model lineup as of April 21 2026: `gpt-image-2` (recommended default; "Use for highest-quality generation and editing … photorealism … identity-sensitive edits"), `gpt-image-1.5`, `gpt-image-1`, `gpt-image-1-mini`. For gpt-image-2, `input_fidelity` "does not work for this model because output is already high fidelity by default." — [OpenAI Cookbook (GitHub)](https://github.com/openai/openai-cookbook/blob/main/examples/multimodal/image-gen-models-prompting-guide.ipynb)
- Verbatim: "For photorealism, include the word 'photorealistic' directly in the prompt to strongly engage the model's photorealistic mode. Similar phrases like 'real photograph,' 'taken on a real camera,' 'professional photography,' or 'iPhone photo' can also help, but detailed camera specs may be interpreted loosely, so use them mainly for high-level look and composition rather than exact physical simulation." — [OpenAI Cookbook (GitHub)](https://github.com/openai/openai-cookbook/blob/main/examples/multimodal/image-gen-models-prompting-guide.ipynb)
- Section 4.3 "Photorealistic Images that Feel 'natural'", verbatim: "To get believable photorealism, prompt the model as if a real photo is being captured in the moment. Use photography language (lens, lighting, framing) and explicitly ask for real texture (pores, wrinkles, fabric wear, imperfections). Avoid words that imply studio polish or staging. When detail matters, set quality="high"." — [OpenAI Cookbook (GitHub)](https://github.com/openai/openai-cookbook/blob/main/examples/multimodal/image-gen-models-prompting-guide.ipynb)
- Quality setting, verbatim: "For small or dense text, detailed infographics, close-up portraits, identity-sensitive edits, and high-resolution outputs, compare `medium` or `high` before shipping." — [OpenAI Cookbook (GitHub)](https://github.com/openai/openai-cookbook/blob/main/examples/multimodal/image-gen-models-prompting-guide.ipynb)
- Ads, verbatim: write ad prompts "like a creative brief rather than a purely technical image spec." Person-in-scene compositing, verbatim: "Anchor realism by specifying a grounded photographic look (natural lighting, believable detail, no cinematic grading), and lock what must not change about the subject." — [OpenAI Cookbook (GitHub)](https://github.com/openai/openai-cookbook/blob/main/examples/multimodal/image-gen-models-prompting-guide.ipynb)
- Identity-lock edit language, verbatim from the virtual try-on example: "Do not change her face, facial features, skin tone, body shape, pose, or identity in any way. Preserve her exact likeness, expression, hairstyle, and proportions … Match lighting, shadows, and color temperature to the original photo so the outfit integrates photorealistically, without looking pasted on." — [OpenAI Cookbook (GitHub)](https://github.com/openai/openai-cookbook/blob/main/examples/multimodal/image-gen-models-prompting-guide.ipynb)

**Google Nano Banana Pro / Nano Banana 2**
- Google's "7 tips" post recommends directing the shot like a cinematographer. Its example combines a low-angle shot, shallow depth of field at f/1.8, golden-hour backlighting and cinematic colour grading. It also recommends stating exact text in quotes and **assigning each uploaded reference image a specific role**. — [Google: 7 tips to get the most out of Nano Banana Pro](https://blog.google/products/gemini/prompting-tips-nano-banana-pro/) (via search summary)
- A third-party summary of Google's guide says naming a specific camera changes the look. Per that guide: a GoPro gives an immersive, slightly distorted action feel, a Fujifilm gives more authentic colour, and a disposable camera gives a raw flash look. — [ud.hk Nano Banana Pro tips (2026-07-20)](https://ud.hk/en/blogs/insight/article/nano-banana-pro-tips-2026-07-20)
- Hands-on coverage reports that Nano Banana Pro outputs look like phone-camera photos. One review says it can add phone-style watermarks/overlays without being asked. — [Feedbagel](https://feedbagel.com/post/googles-nano-banana-pro-ai-generates-realistic-smartphone-style-photos); [LetsDataScience](https://letsdatascience.com/news/nano-banana-pro-produces-photo-realistic-phone-images-e5fb8253)

**Black Forest Labs FLUX.2 ([pro], [max], [flex], [dev], [klein])**
- FLUX.2 handles photorealism from natural-language prompts. The guide recommends naming specific cameras, lenses and film stocks. Its style table includes "Analog Film" → "shot on Kodak Portra 400, natural grain, organic colors". It states that "Shot on Fujifilm X-T5, 35mm f/1.4" produces more authentic results than just "professional photo." — [BFL FLUX.2 prompting guide (docs.bfl.ml mirror)](https://docs.bfl.ml/guides/prompting_guide_flux2) (via search summary)
- The JSON example's lighting value is "Three-point softbox setup creating soft, diffused highlights with no harsh shadows." — [BFL FLUX.2 prompting guide](https://docs.bfl.ai/guides/prompting_guide_flux2) (via search summary)
- **HEX colours:** put the word "color" or "hex" before the code (e.g., "The vase has color #02eb3c"). Vague references like "use #FF0000 somewhere" give inconsistent results. Colours can be attached to a specific object in JSON. — [BFL FLUX.2 prompting guide](https://docs.bfl.ai/guides/prompting_guide_flux2) (via search summary)
- Third-party guides state FLUX.2 **does not support negative prompts**, so describe what you want instead. — [Atlabs FLUX.2 guide](https://www.atlabs.ai/blog/flux-2-prompting-guide) (via search summary)
- Variants: [max], [pro], [dev], [flex]. [flex] exposes `guidance_scale` and `steps`. — [Together AI FLUX.2 quickstart](https://docs.together.ai/docs/quickstart-flux-2). [klein] distilled (4B/9B) runs at **4 steps**, and [klein] Base runs at **50 steps**. — [flux2 README](https://github.com/black-forest-labs/flux2)

**ByteDance Seedream 4.5 / 5.0 Pro**
- Seedream 4.5 renders at 2K–4K and keeps fine detail and legible small text. — [Runware Seedream 4.5 prompting](https://runware.ai/docs/models/bytedance-seedream-4-5/guides/prompting). Example photoreal cues used by platforms: "85mm lens, shallow depth of field, soft morning light" ([fal](https://fal.ai/learn/devs/seedream-v4-5-prompt-guide)); "85mm at f/4", "35mm at f/2.8" ([Fliki](https://fliki.ai/models/image/seedream-4-5)).
- Seedream 5.0 Pro exists as of 2026. One vendor comparison lists it at $0.054/image vs $0.08 for Nano Banana 2, and describes Seedream 5.0 Pro's look as tending toward "dramatic lighting, spatial logic, and layered detail". It cites a 302.AI test where Nano Banana 2 close-ups showed pores and fine hair. — [Atlas Cloud: Seedream 5.0 Pro vs Nano Banana 2](https://www.atlascloud.ai/it/blog/guides/seedream-5-pro-vs-nano-banana-2) (single vendor source; its community data is admittedly thin)

**Midjourney V7 / V8 / V8.1**
- Midjourney's docs describe Raw as turning off the default "auto-pilot" aesthetic. In current versions it is added as `--raw` at the end of the prompt. `--style raw` is the older syntax. — [Midjourney docs: Style](https://docs.midjourney.com/docs/style) (via search summary)
- The V8.1 guide describes `--exp` as "similar to --stylize but stackable", with recommended values of 5/10/25/50/100. High `--exp` may override `--stylize` effects above ~25–50. `--stylize` ranges 0–1000, and lower values are more natural. — [Evolink Midjourney V8.1 prompt guide](https://evolink.ai/docs/en/api-manual/image-series/midjourney/midjourney-v8-1-prompt-guide.md)
- Reviewers report noticeably better photoreal detail and portraits in V8, with Raw "stripping back the model's aesthetic interpretation almost entirely". — [MindStudio: Midjourney V8 alpha strengths/weaknesses](https://www.mindstudio.ai/blog/what-is-midjourney-v8-alpha-strengths-weaknesses); [MindStudio: best results V8](https://www.mindstudio.ai/blog/how-to-get-best-results-midjourney-v8)

**Qwen-Image / Qwen-Image-2512**
- Official defaults: `num_inference_steps=50`, `true_cfg_scale=4.0`. Edit-2509/2511 use 40 steps, `true_cfg_scale=4.0`, `guidance_scale=1.0`. — [QwenLM/Qwen-Image README](https://github.com/QwenLM/Qwen-Image)
- Native resolutions:

  | Ratio | Size |
  |---|---|
  | 1:1 | 1328×1328 |
  | 16:9 | 1664×928 |
  | 9:16 | 928×1664 |
  | 4:3 | 1472×1104 |
  | 3:4 | 1104×1472 |
  | 3:2 | 1584×1056 |
  | 2:3 | 1056×1584 |

  — [Qwen-Image README](https://github.com/QwenLM/Qwen-Image)
- Official `positive_magic` suffix: EN ", Ultra HD, 4K, cinematic composition."; ZH ", 超清，4K，电影级构图." Default negative prompt is a single space `" "`. — [Qwen-Image README](https://github.com/QwenLM/Qwen-Image)
- Qwen-Image-2512 "Enhanced Human Realism" claims "dramatically reduced 'AI look,' richer facial & age details". The README notes that the original model struggled to render aged features such as wrinkles. One of its Chinese example prompts specifies "皮肤呈现真实毛孔纹理与细微光影变化" (skin showing realistic pore texture and subtle light/shadow variation). — [Qwen-Image README](https://github.com/QwenLM/Qwen-Image)
- Qwen recommends its official prompt-enhancement tool (Qwen-Plus) for text-to-image, and warns that edit results "may become unstable if prompt rewriting is not used." — [Qwen-Image README](https://github.com/QwenLM/Qwen-Image)

**Z-Image (Tongyi-MAI)**
- Z-Image-Turbo: 1024×1024, `num_inference_steps=9` (= 8 DiT forwards), `guidance_scale=0.0`. Verbatim: "Guidance should be 0 for the Turbo models." It "excels in photorealistic image generation", but diversity is rated "Low". — [Tongyi-MAI/Z-Image README](https://github.com/Tongyi-MAI/Z-Image)
- Z-Image (base):
  - guidance 3.0–5.0, 28–50 steps, 512²–2048² pixel area at any aspect ratio;
  - **CFG normalization `True` for realism** (`False` for general stylism);
  - negative prompts are supported and "Strongly recommended for better control."
  - [Z-Image README](https://github.com/Tongyi-MAI/Z-Image)

**Higgsfield Soul**
- SOUL ships 50+ curated presets, including an **"iPhone flash"** look, and is designed so users "type a simple idea — no prompt engineering required." Presets add "camera-like imperfections: dust, flash, and grain." — [Higgsfield blog: SOUL](https://higgsfield.ai/blog/Higgsfield-SOUL-Turns-Prompts-Into-Fashion-Ready-Shots); [Higgsfield: 20 new experimental presets](https://higgsfield.ai/blog/Introducing-20-New-Experimental-Presets)
- SOUL ID locks a persona's face across outfits and poses. A third-party guide recommends uploading 20+ photos of the persona. — [Apiframe Higgsfield API guide](https://apiframe.ai/guides/higgsfield-api-guide) (third-party)

### Inferences
- **Per-model SOP deltas:**
  - **GPT Image 2:** include "photorealistic" and the intended use. Use labelled segments and end with explicit exclusions. Use `quality="high"` for faces.
  - **Nano Banana Pro/2:** use a narrative paragraph with photographer direction. Give each reference image a named role ("Image 1 = face identity; Image 2 = product"). Set aspect ratio in config.
  - **FLUX.2:** name a real camera/lens/film, use HEX for wardrobe and brand colours, and do not write "no X". Describe the alternative instead.
  - **Seedream:** subject first and concise. Explicitly ask for flat/natural light, because the model leans dramatic.
  - **Midjourney V8:** `--raw --stylize 0–100` and keep `--exp` low (0–10) for realism. These values are an extrapolation of the docs, not a tested preset.
  - **Qwen-Image-2512:** one block of ~200 words, plus the official anti-AI-look negative prompt, true CFG 4, 50 steps.
  - **Z-Image Turbo:** 9 steps, CFG 0, so negatives do nothing. Put everything in the positive prompt.
- **Conflict to flag:** Qwen's official `positive_magic` ("Ultra HD, 4K, cinematic composition") contradicts the general advice to avoid "4K/cinematic". For UGC/phone realism, I would drop the "cinematic composition" part, since it pushes toward staged framing. This is an inference to A/B test, not a documented result. Notably, Qwen's own 2512 rewriter defines the magic string but never appends it.

### Gaps
- I could not read Google's "7 tips" post or the Gemini 2.5 Flash Image guide verbatim (fetch blocked), so the exact wording of templates and of "semantic negative prompts" is unverified.
- Midjourney personalization profiles (`--p`), moodboards and V8-specific realism guidance from the official docs could not be retrieved. No source gave a tested realism preset.
- No official ByteDance (seed.bytedance.com / Volcengine) Seedream prompt guide was retrieved. Only third-party platform guides were found.
- Krea (Krea 1 / FLUX Krea) prompting guidance: no sources retrieved.
- Unverified community claim: a September 2026 tweet references "GPT-Image 2.5" (with "Sunburst & Flare" variants on Higgsfield) and "GPT-6 Astra". — [YouMind GPT Image 2 prompt collection, No. 117, by @Mho_23](https://github.com/YouMind-OpenLab/awesome-gpt-image-2-prompts). I found no official OpenAI source for these names; treat them as unconfirmed.

---

## 3. Camera & lens language: what increases realism, and what is placebo

### Takeaway
**Device class** and **optical behaviour** reliably change the result in modern models: phone front camera vs rear camera, DSLR/mirrorless, compact digital/CCD, disposable/film, webcam. So do focal-length class (wide 24–26mm phone vs 50mm vs 85mm), depth of field (deep phone DOF vs shallow), flash vs no flash, and film stock. **Exact numeric EXIF** (shutter 1/250, ISO 400, EV −0.3) is mostly interpreted loosely. OpenAI says so explicitly, so treat numbers as soft hints that matter mainly when they are physically coherent with the device. The biggest realism win for UGC is **matching optics to the device**: a phone selfie has a wide lens, deep focus and no creamy 85mm bokeh.

### Cited Findings
- OpenAI: detailed camera specs "may be interpreted loosely, so use them mainly for high-level look and composition rather than exact physical simulation." Phrases like "real photograph," "taken on a real camera," and "iPhone photo" help. — [OpenAI Cookbook (GitHub)](https://github.com/openai/openai-cookbook/blob/main/examples/multimodal/image-gen-models-prompting-guide.ipynb)
- Runware's GPT Image 2 guide: lens focal lengths, depth of field, film stock and exposure hints guide the overall look, but the model interprets them loosely. — [Runware: GPT Image 2 prompting](https://runware.ai/docs/models/openai-gpt-image-2/guides/prompting.md)
- One third-party GPT Image 2 guide says lens model, sensor size and ISO are look-and-feel cues, while naming imperfections ("pores, fine lines, asymmetry, fabric wear, available light") is the bigger lever. The search summary did not say which page in the result set this came from: candidates are [Cuty.ai](https://www.cuty.ai/article/models/gpt-image-2-prompting-guide), [PixVerse](https://pixverse.ai/en/blog/gpt-image-2-review-and-prompt-guide) and [ImagineArt](https://www.imagine.art/blogs/gpt-image-2-prompt-guide). Treat the attribution as uncertain.
- BFL: "Shot on Fujifilm X-T5, 35mm f/1.4" beats "professional photo"; "shot on Kodak Portra 400, natural grain, organic colors" for an analog look. — [BFL FLUX.2 prompting guide](https://docs.bfl.ml/guides/prompting_guide_flux2) (via search summary)
- Google's guide (as summarised by ud.hk): GoPro → immersive, slightly distorted; Fujifilm → more authentic colour; disposable camera → raw flash look. — [ud.hk](https://ud.hk/en/blogs/insight/article/nano-banana-pro-tips-2026-07-20)
- OpenAI's official photoreal example uses film-camera framing language: "Shot like a 35mm film photograph, medium close-up at eye level, using a 50mm lens. Soft coastal daylight, shallow depth of field, subtle film grain, natural color balance." — [OpenAI Cookbook (GitHub)](https://github.com/openai/openai-cookbook/blob/main/examples/multimodal/image-gen-models-prompting-guide.ipynb)
- A highly detailed, physically coherent **phone camera spec block** from Chinese creator 宝玉 (@dotey, Oct 10 2025), quoted verbatim from the "Camera" section of a Nano Banana mirror-selfie prompt:
  - "Mode: smartphone rear camera shooting via the mirror (no portrait/bokeh mode)"
  - "Equivalent focal length (mm): 26"
  - "Aperture (f): 1.8 / ISO: 100 / Shutter speed (s): 0.01 / Exposure compensation (EV): -0.3"
  - "Depth of field: natural smartphone deep depth of field; background clearly visible with no artificial blur"
  - "Composition note: keep the subject centered; to avoid wide-angle edge distortion, have her stand a bit further away and crop to a square later."
  - Source: [YouMind awesome-nano-banana-pro-prompts, No. 8](https://github.com/YouMind-OpenLab/awesome-nano-banana-pro-prompts) / [original post](https://x.com/dotey/status/1976485558319722711)
- Community "photography" block for an iPhone mirror selfie, verbatim:
  - `"camera_style": "casual iPhone mirror selfie, NOT professional"`
  - `"quality": "iPhone camera - good but not studio, realistic social media quality"`
  - `"texture": "natural, slightly grainy iPhone look, not over-processed"`
  - Source: [ZeroLu/awesome-nanobanana-pro §1.9](https://github.com/ZeroLu/awesome-nanobanana-pro), credited to [@gaucheai](https://x.com/gaucheai/status/1996184483343520186)
- A Nano Banana Pro "amateur iPhone photo" template uses: "slightly tilted horizon, RAW image, jpeg compression, moderate grain, natural color tones, no retouching, shallow depth of field." — [Hooked template](https://www.hooked.so/templates/nano-banana-pro/profile-avatar-amateur-iphone-photo-portrait)
- CCD/compact and film cues used in viral GPT Image 2 prompts: "CCD compact camera direct on-camera flash" ([@BubbleBrain via magiccreator-ai repo](https://github.com/magiccreator-ai/awesome-gpt-image-2-prompts)); "Analog 35mm film photography … intense on-camera direct flash (CCD hard flash style)" ([magiccreator-ai repo](https://github.com/magiccreator-ai/awesome-gpt-image-2-prompts)); "Render it as the Camera Type … Low-resolution built-in webcam capture from a chunky desktop computer" ([YouMind No. 7 by @favprompt, Oct 21 2026](https://github.com/YouMind-OpenLab/awesome-nano-banana-pro-prompts)).
- A full EXIF-style DSLR spec appears in a GPT Image 2 showcase prompt: "captured on a Canon EOS R5 DSLR camera, 24-105mm f/4L lens at 35mm, f/5.6 aperture, 1/250s shutter, ISO 400". — [magiccreator-ai/awesome-gpt-image-2-prompts](https://github.com/magiccreator-ai/awesome-gpt-image-2-prompts). (Note: the R5 is mirrorless, not a DSLR. The model doesn't care, which illustrates that the specs act as style tokens.)
- Headshot example using a body and lens for "portrait compression": "Shot on a Sony A7III with an 85mm f/1.4 lens, creating a flattering portrait compression." — [ZeroLu §1.5 (from a WeChat article)](https://github.com/ZeroLu/awesome-nanobanana-pro)

### Inferences
- **What works (behaviourally meaningful):**
  - device class: "iPhone front camera selfie", "rear camera through a mirror", "compact digital camera with built-in flash", "disposable film camera", "laptop webcam", "dashcam/bodycam", "GoPro";
  - focal-length class: 24–26mm phone wide / 35mm documentary / 50mm natural / 85mm portrait;
  - DOF intent: "deep focus, background in focus" vs "shallow DOF";
  - flash state: "direct on-camera flash" vs "available light only";
  - film stock: Portra 400 = warm, soft, pastel skin; Fuji = cooler greens; Ilford HP5 = B&W grain;
  - processing: "phone HDR", "JPEG compression", "sensor noise in shadows".
- **Likely placebo or weak:** exact shutter speeds, ISO numbers, EV values, and specific body names when a lens/look description is missing. One exception: numeric values can help as coherence anchors. ISO 100 + f/1.8 + 26mm signals "phone in daylight"; ISO 3200 signals "night, noisy".
- **Common realism-killer:** pairing "iPhone selfie" with "85mm, f/1.4, creamy bokeh". Real phone front cameras are wide-angle with deep DOF; any blur comes from portrait mode, which has edge artefacts. Use "no portrait-mode blur" or "slight portrait-mode blur" deliberately.
- **Arm-length selfie geometry:** a front camera at 30–50 cm with a ~24–26mm-equivalent lens gives mild nose/forehead enlargement and a slightly-above-eye-level angle. Describing "held at arm's length, slightly above eye level, mild wide-angle perspective stretch at the frame edges" is more effective than naming the phone model alone. This is standard photographic optics, not tested here.
- **"Shot on iPhone 16/17 Pro" vs "iPhone photo":** no source showed a measurable difference between model numbers. OpenAI only endorses the generic "iPhone photo". Treat specific model numbers as optional flavour.

### Gaps
- No controlled A/B evidence was found for "Live Photo", "RAW photo", "unedited", "no filter" or "front camera" phrases. Only community usage exists. "RAW photo" also appears alongside contradictory terms ("Photorealistic. RAW photo. Smooth, glowing skin" in a YouMind prompt), which undermines it.
- No source tested Pixel vs iPhone colour science prompts, Leica "look", or Ilford/Fuji stocks per model.

---

## 4. Lighting: realistic vocabulary, setups, and what makes images look fake

### Takeaway
Describe light the way a photographer would log it: **source** (window, overhead bulb, phone flash, monitor, car dome light, fluorescent tubes), **direction** (from camera-left, from above, behind), **quality** (soft/diffused vs hard), **colour temperature** (warm tungsten ~2700–3200K, daylight ~5000–5600K, or a numeric white balance), and **imperfections** (uneven exposure, mixed colour casts, slight overexposure, hard flash shadow on the wall). Generic labels like "cinematic lighting", "studio lighting", "dramatic", "volumetric" and "glamour lighting" push toward staged, graded, poster-like images. OpenAI's official guide explicitly prompts against "cinematic lighting, dramatic color grading, or stylized composition" for photo-real results.

### Cited Findings
- OpenAI, verbatim: "The image should look like a real photograph someone could have taken, not an overly enhanced or cinematic movie-poster image … with natural lighting and realistic colors. Everything should feel grounded, authentic, and unstyled, as if captured in a real moment. Avoid cinematic lighting, dramatic color grading, or stylized composition." — [OpenAI Cookbook (GitHub)](https://github.com/openai/openai-cookbook/blob/main/examples/multimodal/image-gen-models-prompting-guide.ipynb)
- OpenAI, verbatim: "For wide, cinematic, low-light, rain, or neon scenes, add extra detail about scale, atmosphere, and color so the model does not trade mood for surface realism." It lists lighting/mood examples "(soft diffuse, golden hour, high-contrast)". — [OpenAI Cookbook (GitHub)](https://github.com/openai/openai-cookbook/blob/main/examples/multimodal/image-gen-models-prompting-guide.ipynb)
- OpenAI's lighting-transformation section says to change only "lighting direction/quality, shadows, atmosphere" while preserving identity and geometry "so it still reads as the same original photo." — [OpenAI Cookbook (GitHub)](https://github.com/openai/openai-cookbook/blob/main/examples/multimodal/image-gen-models-prompting-guide.ipynb)
- Flat-looking images usually mean the light wasn't described, so treat light as a variable you set. — [ud.hk Nano Banana Pro tips](https://ud.hk/en/blogs/insight/article/nano-banana-pro-tips-2026-07-20)
- Named portrait setups (Rembrandt, butterfly, split) and modifiers (softbox, reflector cards) are recognised by Nano Banana Pro. — [VEED Nano Banana Pro guide](https://www.veed.io/learn/nano-banana-pro-prompts)
- BFL's JSON example lighting string: "Three-point softbox setup creating soft, diffused highlights with no harsh shadows." A third-party FLUX.2 guide recommends specifying "Lighting (source + quality)". — [BFL guide](https://docs.bfl.ai/guides/prompting_guide_flux2); the third-party claim comes from the same search result set (e.g., [LTX FLUX.2 guide](https://ltx.io/blog/flux-prompting-guide), [Prompt Architects FLUX.2 recipes](https://prompt-architects.com/blog/472-flux-2-photorealism-recipes-10-prompt-formulas)), and the exact page is uncertain.
- Qwen's official rewriter asks for lighting **direction, intensity and colour temperature**. Its portrait examples favour "soft and even" or "warm and diffused" light. — [Qwen prompt_utils_2512.py](https://github.com/QwenLM/Qwen-Image/blob/main/src/examples/tools/prompt_utils_2512.py)
- Kelvin and source-based lighting used in a high-quality community prompt, verbatim: "Light source: daylight coming from a large window on the left side of the camera, through sheer curtains / Light quality: soft, diffused light / White balance (K): 5200". — [YouMind No. 8 by @dotey](https://github.com/YouMind-OpenLab/awesome-nano-banana-pro-prompts)
- Phone-flash vocabulary in viral prompts:
  - "Harsh, direct on-camera flash lighting that creates hard shadows behind the subjects. Authentic film grain, slight motion blur on the edges, and chromatic aberration." — [ZeroLu §1.12](https://github.com/ZeroLu/awesome-nanobanana-pro)
  - "Harsh on-camera direct flash from front/slightly above creates strong catchlights, sharp shadows behind the subject, crisp highlights on skin" — [magiccreator-ai repo](https://github.com/magiccreator-ai/awesome-gpt-image-2-prompts)
  - "harsh super-flash with bright blown-out highlights but subject still visible" — [@ZaraIrahh via ZeroLu §1.2](https://github.com/ZeroLu/awesome-nanobanana-pro)
- Mundane practical lighting in realistic GPT Image 2 prompts: "realistic indoor fluorescent lighting" (supermarket, [@hx831126, Sept 8 2026](https://x.com/hx831126/status/2097453683609137635)); "fluorescent store lighting, believable candid photo style" and "shot with direct flash … casual home lighting" ([@WolfRiccardo](https://x.com/WolfRiccardo/status/2041573176681918728), via [magiccreator-ai repo](https://github.com/magiccreator-ai/awesome-gpt-image-2-prompts)).
- @jiamimaodashu's "extremely ordinary iPhone selfie" uses lighting imperfection as the realism lever: "uneven lighting caused by sunlight or indoor lights resulting in mild overexposure". — [JimmyLv/awesome-nano-banana Case 54](https://github.com/JimmyLv/awesome-nano-banana); [original](https://x.com/jiamimaodashu/status/1912653073190879410)
- A Japanese-language Nano Banana template deliberately requests camera shake, uneven lighting, awkward angles and cluttered framing so the image reads as an accidental snapshot. — [Fotor JP](https://www.fotor.com/jp/blog/nano-banana-model-prompts)
- Seedream 5.0 Pro is described as leaning toward "dramatic lighting". — [Atlas Cloud](https://www.atlascloud.ai/it/blog/guides/seedream-5-pro-vs-nano-banana-2)

### Inferences
**Lighting phrase bank for UGC avatars** (my synthesis; terminology is standard portrait-photography usage, but no photography reference page could be fetched this session to cite):

| Scene | Copy-paste lighting phrase |
|---|---|
| Kitchen daytime | "soft daylight from a window on camera-left, mixed with a warm overhead ceiling bulb (~3000K), slightly uneven exposure, gentle shadow under the chin" |
| Overcast outdoor | "overcast midday sky as a giant softbox, flat even light, soft shadows, muted colours, no sun flare" |
| Golden hour street | "low warm sun behind her (backlight), hair rim-lit, face in open shade lit by bounce from a light-coloured wall, slight lens flare" |
| Car selfie | "daylight through the windshield and side window, face lit softly from the side window, darker car interior, small specular reflections on the glass" (night: "dim warm dome light from above, dashboard glow on the chin, city lights soft through the window") |
| Bathroom mirror | "vanity light strip above the mirror, cool-white LED ~4000–4500K, slight overhead shadow under brows, glossy reflections on tiles" |
| Office | "overhead fluorescent panels, slight greenish-cool cast, plus window light from the right; flat, unflattering, realistic" |
| Ring light UGC | "ring light directly in front at eye level, circular catchlight in both eyes, flat even face, slight falloff on the background" |
| Night party | "direct on-camera flash, hard shadow on the wall behind, slightly blown highlights on forehead and nose, dark background falling off quickly" |
| Desk/webcam | "laptop screen glow (cool) on the face plus a warm desk lamp from the side; mixed colour temperature; low-light noise" |
| Gym | "overhead industrial LED high-bay lights, top-down hard light, sheen of sweat catching highlights, mirror reflections" |
| Clinic/expert | "bright even overhead clinic lighting plus soft window light from behind camera, clean neutral white balance ~5000K" |
| Testimonial (semi-pro) | "single large soft key light 45° camera-left at eye level (loop lighting), white bounce fill on the right, practical lamp warm in the background, soft natural falloff" |

- **Why the generic words look fake:**
  - "cinematic" invokes colour grading (teal-orange), anamorphic framing and dramatic contrast;
  - "studio lighting" invokes seamless backdrops and multi-light beauty setups;
  - "volumetric" invokes haze/god-rays, rare in phone photos;
  - "dramatic" invokes chiaroscuro.
  
  All of these are associated with professional or CG imagery, not phone snapshots. OpenAI's anti-cinematic phrasing supports this direction.
- **The "AI glow" (over-clean HDR, glowing skin, uniform rim light everywhere):**
  - counter it with a *single dominant source*, *one named imperfection* (uneven exposure, mixed colour cast, hard flash shadow), "natural colour balance", and "no glow, no bloom, no heavy HDR";
  - avoid "glowing skin" and "radiant";
  - "subtle film grain" or "light sensor noise" breaks the too-clean gradient look (OpenAI's photoreal example itself includes "subtle film grain, natural color balance").
- **Classic patterns** (Rembrandt, loop, butterfly, split): use them for "studio-ish testimonial" and "expert headshot" avatars. Prefer loop or soft Rembrandt for approachable realism. Butterfly reads as beauty or glamour. Split reads as dramatic. Pair any named pattern with motivated sources ("window to camera-left") so it doesn't read as a studio.

### Gaps
- No photography reference (e.g., Wikipedia, B&H, Strobist) could be fetched to cite exact definitions of Rembrandt/loop/butterfly/split or Kelvin values for sources. These definitions are standard knowledge but uncited here.
- No controlled tests were found comparing "cinematic lighting" vs "natural light" realism scores per model. The evidence is official guidance plus practitioner consensus.

---

## 5. The UGC / smartphone aesthetic: how to prompt "a real person shot on a phone", plus viral prompts

### Takeaway
UGC realism comes from **deliberate ordinariness**:
- a casual purpose ("recording a quick review for followers");
- device-true optics (front-camera wide, deep focus);
- imperfect framing (tilt, cropped limbs, off-centre);
- mild motion blur or softness;
- phone processing artefacts (HDR, noise, JPEG);
- mundane, slightly messy real environments with specific props;
- unretouched skin;
- an explicit "not a studio shoot / not glamour" contrast clause.

Current viral prompts for GPT Image 2 and Nano Banana Pro rely heavily on "authentic phone selfie", "candid", "smartphone snapshot", "direct flash" and "slightly imperfect framing".

### Cited Findings
- @jiamimaodashu, "Extremely Ordinary iPhone Selfie", verbatim, first paragraph: "Please draw an extremely ordinary and unremarkable iPhone selfie, with no clear subject or sense of composition — just like a random snapshot taken casually. The photo should include slight motion blur, with uneven lighting caused by sunlight or indoor lights resulting in mild overexposure. The angle is awkward, the composition is messy, and the overall aesthetic is deliberately plain — as if it was accidentally taken while pulling the phone out of a pocket." — [JimmyLv/awesome-nano-banana Case 54](https://github.com/JimmyLv/awesome-nano-banana); [original](https://x.com/jiamimaodashu/status/1912653073190879410) (Chinese creator; the original prompt names two celebrities, omitted here)
- @hx831126 (Sept 8 2026), GPT Image 2 supermarket UGC, verbatim excerpt: "Use a natural consumer-phone snapshot style, slightly imperfect framing, realistic indoor fluorescent lighting, mild motion softness, neutral colors, glossy gray supermarket floor reflections, deep aisle perspective, and authentic everyday details. Make it look like a casual buyer-show or store social media photo rather than a studio fashion shoot. No glamour lighting, no exaggerated posing, no artificial-looking skin, no extra people…". The prompt also counts objects precisely ("exactly one main shopper, one black basket, two background shoppers…"). — [YouMind awesome-gpt-image-2-prompts No. 118](https://github.com/YouMind-OpenLab/awesome-gpt-image-2-prompts); [original](https://x.com/hx831126/status/2097453683609137635)
- @PurzBeats, GPT Image 2, verbatim: "Create a realistic close-up vacation selfie of a heavyset middle-aged man with short gray hair and a gray beard, making an excited wide-eyed expression from a hotel balcony in Hawaii. Show palm trees, high-rise buildings, blue sky, and bright daylight in the background. Make it feel like an authentic phone selfie." — [magiccreator-ai/awesome-gpt-image-2-prompts](https://github.com/magiccreator-ai/awesome-gpt-image-2-prompts); [original](https://x.com/PurzBeats/status/2040627147774284008)
- @WolfRiccardo, GPT Image 2, verbatim: "A candid apartment doorway photo of a young woman in a simple black dress holding a small decorated birthday cake, shot with direct flash, realistic skin texture, casual home lighting, slightly messy interior, authentic smartphone photo look." Also: "A warm indoor lifestyle portrait of a young woman sitting on a sofa in a black top and white skirt, looking at her phone, soft evening light, natural pose, cozy apartment background, photorealistic smartphone snapshot." — [magiccreator-ai repo](https://github.com/magiccreator-ai/awesome-gpt-image-2-prompts); [original](https://x.com/WolfRiccardo/status/2042011687746990464)
- @WolfRiccardo POV, verbatim: "First-person view from the driver's seat of a Tesla at a red light in a modern city, hands on the steering wheel, dashboard screen visible, realistic windshield reflections, natural daylight, smartphone photo realism." — [magiccreator-ai repo](https://github.com/magiccreator-ai/awesome-gpt-image-2-prompts); [original](https://x.com/WolfRiccardo/status/2041573176681918728)
- @phasE89 shows that a minimal non-English prompt can read as real. Verbatim (Czech): "Amatérská fotka staršího páru sedícího v yorkshirské hospodě, amatérská kompozice, momentka." ("Amateur photo of an older couple sitting in a Yorkshire pub, amateur composition, snapshot.") — [magiccreator-ai repo](https://github.com/magiccreator-ai/awesome-gpt-image-2-prompts); [original](https://x.com/phasE89/status/2043641310226042910)
- @favprompt (Oct 21 2026), webcam realism, verbatim excerpt: "Render it as the Camera Type, with soft focus, smeared facial detail, color noise, dim uneven indoor light and low-resolution compression. Use awkward webcam framing from a desk-level angle, with a slight tilt and casually cropped shoulders or arms … real skin, messy everyday hair and no heavy retouching … Make it feel like an unedited early-2000s personal photo from an old Facebook album or MSN chat, not a modern image with a retro filter. No date stamp, text, watermark…" — [YouMind awesome-nano-banana-pro-prompts No. 7](https://github.com/YouMind-OpenLab/awesome-nano-banana-pro-prompts); [original](https://x.com/favprompt/status/2112947693710360593)
- @ZaraIrahh's viral "2000s Mirror Selfie" JSON for Nano Banana Pro uses keys `subject{description, age, expression, hair, clothing, face{preserve_original, makeup}}`, `accessories{…device{type:"smartphone"}}`, `photography{camera_style:"early-2000s digital camera aesthetic", lighting:"harsh super-flash with bright blown-out highlights but subject still visible", angle:"mirror selfie", shot_type:"tight selfie composition", texture:"subtle grain, retro highlights, V6 realism, crisp details, soft shadows"}` and `background{setting, wall_color, elements[…], atmosphere, lighting}`. — [ZeroLu/awesome-nanobanana-pro §1.2](https://github.com/ZeroLu/awesome-nanobanana-pro); [original](https://x.com/ZaraIrahh/status/1991681614368436468)
- @Mho_23 (Sept 9 2026) describes a UGC e-commerce workflow:
  - use a JSON style reference for lighting and colour grading;
  - generate a person holding the product;
  - save the best character image and re-attach it each time with "preserve the same facial features" to build a reusable avatar.
  
  He notes: "the basic colours and grainy look are some of the things that can make an image feel AI-generated, so pay attention to those when comparing your results." — [YouMind awesome-gpt-image-2-prompts No. 117](https://github.com/YouMind-OpenLab/awesome-gpt-image-2-prompts); [original](https://x.com/Mho_23/status/2097483045221917131)
- Higgsfield SOUL's iPhone-flash preset bakes in "dust, flash, and grain … for authentic camera imperfections". — [Higgsfield](https://higgsfield.ai/blog/Introducing-20-New-Experimental-Presets)
- OpenAI's guidance to include the intended use ("ad") in the prompt "to set the 'mode' and level of polish". — [OpenAI Cookbook (GitHub)](https://github.com/openai/openai-cookbook/blob/main/examples/multimodal/image-gen-models-prompting-guide.ipynb)
- Risk context: coverage notes that Nano Banana Pro's phone-photo realism makes synthetic images harder to detect, raising misinformation concerns. — [LetsDataScience](https://letsdatascience.com/news/nano-banana-pro-produces-photo-realistic-phone-images-e5fb8253)

### Inferences
- **UGC realism checklist (SOP):**
  1. **Purpose verb:** "filming a quick review", "showing her followers".
  2. **Device + camera:** "front camera at arm's length" or "rear camera via mirror".
  3. **Geometry:** "slightly above eye level", "mild wide-angle stretch".
  4. **Focus:** "everything in focus, no portrait-mode blur".
  5. **Framing flaw:** "slightly tilted", "shoulder cut off", "off-centre".
  6. **Motion:** "slight motion softness in the hand".
  7. **Processing:** "phone HDR, light sensor noise in shadows, mild JPEG compression".
  8. **Mess:** 3–6 specific everyday props, such as "a charging cable on the counter".
  9. **Skin:** "visible pores, faint redness around the nose, slight shine on the forehead, natural unretouched".
  10. **Contrast clause:** "not a studio shoot, no beauty filter, no glamour lighting".
- **Colour realism:** per @Mho_23, the default saturated "AI colour" and uniform added grain can betray AI. Prefer "neutral, slightly muted phone colours, auto white balance, a touch warm indoors" over simply "add grain".
- **Avoid over-imperfection for ads.** Ads need the product legible. Keep motion blur on hands or background, not on the product label. Keep a mild tilt (≤5°).
- **Consistency for avatar programmes:** combine (a) an identity reference image (Nano Banana Pro/GPT Image 2 edits, or Higgsfield SOUL ID) with (b) a fixed style/lighting JSON and (c) per-scene variable fields. This mirrors both @Mho_23's workflow and OpenAI's "repeat the preserve list on each iteration".

### Gaps
- Spanish, Portuguese (Brazilian infoprodutores), Russian and Japanese creator sources could not be searched beyond one Japanese Fotor page, because the search budget was exhausted. Chinese sources are represented only through @dotey, @jiamimaodashu and @hx831126, plus the Qwen/Z-Image official Chinese prompts.
- No Reddit threads were retrieved (search results returned blogs, not Reddit).

---

## 6. Negative prompts: which models support them, best avoid-lists, and positive rephrasing

### Takeaway
| Model | Negative-prompt support |
|---|---|
| **Qwen-Image** (true CFG) | true negative prompts; Qwen even publishes an anti-"AI look" list |
| **Z-Image base** | true negative prompts, "strongly recommended" |
| **Z-Image Turbo** (CFG 0) | effectively none |
| **FLUX.2** | none |
| **GPT Image 2 / Nano Banana / Seedream** | no separate negative field; they accept in-prompt exclusions ("No glamorization, no heavy retouching"), which OpenAI uses in its own official example |
| **Midjourney** | `--no` (not verified this session) |

For diffusion-style models without negatives, describe the desired alternative positively ("an empty street" rather than "no cars").

### Cited Findings
- Qwen-Image-2512 official example negative prompt (Chinese), verbatim: "低分辨率，低画质，肢体畸形，手指畸形，画面过饱和，蜡像感，人脸无细节，过度光滑，画面具有AI感。构图混乱。文字模糊，扭曲。" Translation: low resolution, low quality, deformed limbs, deformed fingers, oversaturated image, waxy look, face lacking detail, over-smooth, image has an AI feel; chaotic composition; blurry, distorted text. Default when unused: `" "`. — [Qwen-Image README](https://github.com/QwenLM/Qwen-Image)
- Z-Image base: negative prompts "Strongly recommended for better control". Z-Image Turbo runs with guidance 0 (CFG unsupported), so it has no effective negative prompt. — [Z-Image README](https://github.com/Tongyi-MAI/Z-Image)
- FLUX.2 does not support negative prompts; describe what you want instead. — [Atlabs FLUX.2 guide](https://www.atlabs.ai/blog/flux-2-prompting-guide) (via search summary)
- OpenAI, verbatim: "State exclusions and invariants explicitly (e.g., 'no watermark,' 'no extra text,' 'no logos/trademarks,' 'preserve identity/geometry/layout/brand elements')." The official photoreal example ends with "No glamorization, no heavy retouching." — [OpenAI Cookbook (GitHub)](https://github.com/openai/openai-cookbook/blob/main/examples/multimodal/image-gen-models-prompting-guide.ipynb)
- Community Nano Banana negative block (@dotey), verbatim items:
  - "Beauty filters/over-smoothed skin; poreless skin look"
  - "Exaggerated or distorted anatomy"
  - "Logos, brand names, or readable user interface text"
  - "Fake portrait-mode blur, CGI/illustration feel"
  - [YouMind No. 8](https://github.com/YouMind-OpenLab/awesome-nano-banana-pro-prompts)
- Community lists commonly include "plastic skin," "CGI look," "over-smoothed skin". One source advises preferring specific positive outcomes (e.g., "visible pores and restrained retouching") over long negative lists. None of the sources tested efficacy. — [GenImagePro](https://genimagepro.com/blog/how-to-make-ai-images-look-realistic); [AI Pro Photography](https://www.aiprophotography.com/ai-tools-and-generation/photorealistic-ai-prompts/)
- @hx831126's GPT Image 2 exclusion tail, verbatim: "No glamour lighting, no exaggerated posing, no artificial-looking skin, no extra people". — [YouMind GPT Image 2 No. 118](https://github.com/YouMind-OpenLab/awesome-gpt-image-2-prompts)

### Inferences
- **SOP negative list for Qwen-Image / Z-Image base / SDXL-type pipelines**:

  ```
  low resolution, low quality, deformed hands, extra fingers, distorted anatomy, oversaturated, waxy skin, plastic skin, airbrushed, beauty filter, poreless skin, over-smoothed, overly sharp, HDR glow, bloom, cinematic color grading, teal and orange, studio backdrop, glamour lighting, CGI, 3D render, illustration, doll-like face, symmetrical perfect face, text, watermark, logo, AI look
  ```

  For Qwen, use the Chinese list verbatim; it is official.
- **Positive rephrasings for FLUX.2 / Nano Banana / Seedream:**

  | Instead of | Write |
  |---|---|
  | "no plastic skin" | "natural skin with visible pores, faint redness and fine lines, unretouched" |
  | "no bokeh" | "deep focus, background sharp and readable" |
  | "no studio" | "in her real cluttered kitchen" |
  | "no HDR" | "natural contrast, shadows allowed to go dark" |
  | "no cinematic" | "ordinary phone snapshot colours" |
  | "no text" | "plain unlabelled surfaces" |
- For GPT Image 2, keep a short explicit "No …" tail. OpenAI's own examples do this, so it is officially sanctioned.

### Gaps
- I could not verify Google's official "semantic negative prompt" wording for Nano Banana. I recall that it exists, but it was not retrieved.
- I could not verify Midjourney `--no` behaviour in V8 or Seedream negative-prompt support on its API.

---

## 7. Words and phrases that hurt realism, and better replacements

### Takeaway
Generic quality boosters ("8K", "ultra-detailed", "masterpiece", "award-winning", "hyperrealistic", "trending on artstation", "octane render", "unreal engine") carry CLIP-era aesthetic baggage. They push toward over-sharpened, over-saturated, CG or poster renders. OpenAI's gpt-image-1.5 guide states outright that camera/composition terms steer realism "more reliably than generic '8K/ultra-detailed.'" Beauty words ("perfect skin", "flawless", "glowing", "beautiful", "gorgeous") trigger airbrushed, plastic faces. Replace them with photographic and observational language.

### Cited Findings
- OpenAI (gpt-image-1.5 guide), verbatim: "For photorealism, camera/composition terms (lens, aperture feel, lighting) often steer realism more reliably than generic '8K/ultra-detailed.'" — [OpenAI Cookbook: gpt-image-1.5 prompting guide (GitHub)](https://github.com/openai/openai-cookbook/blob/main/examples/multimodal/image-gen-1.5-prompting_guide.ipynb)
- OpenAI (gpt-image-2): "Avoid words that imply studio polish or staging"; "No glamorization, no heavy retouching"; "not an overly enhanced or cinematic movie-poster image". — [OpenAI Cookbook (GitHub)](https://github.com/openai/openai-cookbook/blob/main/examples/multimodal/image-gen-models-prompting-guide.ipynb)
- Rangy advises against stacked hype adjectives like "8K" and "award-winning" as diffusion-model habits, and recommends opening GPT Image 2 prompts with "Style: photorealism" plus concrete material and camera details. — [Rangy: How to prompt GPT Image 2](https://rangy.ai/blog/how-to-prompt-gpt-image-2-with-llm)
- Fal argues that vague praise does little ("excitement does not render"). It recommends the structure scene → subject → important details → use case → constraints. — [fal: GPT Image 2 prompting guide](https://fal.ai/learn/tools/prompting-gpt-image-2) (via search summary)
- Practitioner guides say "8K," "hyperrealistic" and "masterpiece" push toward an over-sharpened, over-saturated, plainly artificial render, and that asking for flawless features pushes the model "straight back to the plastic look". — Search result set including [GenImagePro](https://genimagepro.com/blog/how-to-make-ai-images-look-realistic) and [AI Pro Photography](https://www.aiprophotography.com/ai-tools-and-generation/photorealistic-ai-prompts/). This is opinion, not tested, and the summary did not say which quote came from which page.
- Several of the most-shared 2025–2026 prompts still contain legacy boosters next to good realism cues. Examples:
  - a headshot prompt ending "Final image should be an ultra-realistic, 8k professional headshot" right after "Render natural skin texture with visible pores, not an airbrushed look" ([ZeroLu §1.5](https://github.com/ZeroLu/awesome-nanobanana-pro));
  - a YouMind prompt beginning "Photorealistic. RAW photo. Smooth, glowing skin." ([YouMind NB Pro collection](https://github.com/YouMind-OpenLab/awesome-nano-banana-pro-prompts)).
- "Hyper-realistic" shows up in prompts that explicitly want CG, e.g., "A hyper-realistic 3D render of the person in the image standing and taking a selfie." — [PicoTrex/Awesome-Nano-Banana-images](https://github.com/PicoTrex/Awesome-Nano-Banana-images)
- Counterpoint: Qwen-Image's official `positive_magic` appends "Ultra HD, 4K, cinematic composition." — [Qwen-Image README](https://github.com/QwenLM/Qwen-Image). Runware and OpenAI both recommend including the word "photorealistic". — [Runware GPT Image 2](https://runware.ai/docs/models/openai-gpt-image-2/guides/prompting.md); [OpenAI Cookbook](https://github.com/openai/openai-cookbook/blob/main/examples/multimodal/image-gen-models-prompting-guide.ipynb)

### Inferences
**Replacement table (SOP):**

| Hurts realism | Why (inferred) | Use instead |
|---|---|---|
| hyperrealistic, ultra realistic | Associated with CG/3D renders and hyperrealist painting | "photorealistic" (GPT Image), "a real photograph", "candid smartphone photo" |
| 8K, 4K, ultra-detailed, ultra HD, masterpiece, best quality | CLIP-era quality tokens. They oversharpen and add uniform micro-detail; OpenAI says camera terms work better | "sharp where in focus, natural softness elsewhere", a resolution parameter instead of words |
| trending on artstation, octane render, unreal engine, CGI, 3D | Explicit render/illustration styles | omit entirely |
| cinematic, cinematic lighting, dramatic lighting, volumetric, epic, moody grading | Film grading and staged contrast | "natural light from [source]", "ordinary phone colours", "natural colour balance" |
| studio lighting, professional photoshoot, glamour, editorial (for UGC) | Staging and polish (OpenAI: avoid) | "shot by a friend on a phone", "self-recorded", "real home" |
| perfect skin, flawless, smooth skin, glowing skin, porcelain, beautiful, gorgeous, stunning | Beauty-filter priors that yield plastic or wax skin | "natural skin texture, visible pores, slight unevenness, faint freckles, fine lines, a little shine on the T-zone, no retouching" |
| perfect symmetry, model-like | Average "AI face" | "slightly asymmetrical smile", "ordinary, approachable face", specific age and ethnicity |
| bokeh everywhere, f/1.2 (for phone UGC) | Optically wrong for phones | "deep focus phone image", or "slight portrait-mode blur with soft edges" |

- **Skin micro-texture vocabulary that does work** (adapted from a viral GPT Image 2 prompt by @BubbleBrain; use without the beauty adjectives): "visible fine pores on cheeks and nose, soft peach fuzz on jawline and cheekbones catching light, subtle subsurface scattering at ear edges and nose tip, natural skin micro-texture with faint expression lines, matte healthy glow with zero oiliness or plastic sheen". — [magiccreator-ai repo](https://github.com/magiccreator-ai/awesome-gpt-image-2-prompts). Caution: "subsurface scattering" is a 3D-rendering term and may pull toward CG in some models. Test it.

### Gaps
- No controlled, per-model benchmark exists in the retrieved sources quantifying how much "8K/hyperrealistic" degrades realism in GPT Image 2, Nano Banana Pro, FLUX.2 or Seedream. Only OpenAI's statement is official.

---

## 8. Seeds, CFG/guidance, steps, samplers for open models, and realism LoRAs

### Takeaway
Use each open model's official defaults first:

| Model | Steps | Guidance / CFG | Negative prompt |
|---|---|---|---|
| **Qwen-Image(-2512)** | 50 | true CFG 4.0 | use one |
| **Z-Image-Turbo** | 9 | 0 | not effective |
| **Z-Image base** | 28–50 | 3–5, with CFG-normalization on for realism | recommended |
| **FLUX.2 [klein] distilled** | 4 | — | — |
| **FLUX.2 [klein] base** | 50 | — | — |
| **FLUX.2 [dev]** | not documented | guidance-distilled, value not documented | — |

FLUX.2 [dev] benefits greatly from prompt upsampling. Realism LoRA recommendations could not be researched this session.

### Cited Findings
- Qwen-Image / 2512: `num_inference_steps=50`, `true_cfg_scale=4.0`, with the native resolutions listed in section 2. — [Qwen-Image README](https://github.com/QwenLM/Qwen-Image)
- Z-Image-Turbo: 9 steps, `guidance_scale=0.0`, 1024×1024. Z-Image base: guidance 3.0–5.0, 28–50 steps, CFG normalization True for realism. — [Z-Image README](https://github.com/Tongyi-MAI/Z-Image)
- FLUX.2 [klein] distilled: 4 steps (production/real-time). [klein] Base: 50 steps (fine-tuning/LoRA training/max flexibility). FLUX.2 [dev] is guidance-distilled, needs ~H100-class VRAM unless quantized, and "benefits significantly from prompt upsampling". — [flux2 README](https://github.com/black-forest-labs/flux2)
- FLUX.2 [flex] (API) exposes `guidance_scale` and `steps` for maximum customization. — [Together AI](https://docs.together.ai/docs/quickstart-flux-2)

### Inferences
- **Seeds:** for avatar programmes, lock the seed while iterating one variable (lighting or wardrobe) on open models. This mirrors OpenAI's "single-change follow-ups" principle. For closed models (GPT Image, Nano Banana), consistency comes from reference images and repeated invariants, not seeds.
- **Z-Image-Turbo** has low diversity ("Low" in the README), so faces may converge. To vary demographics, specify ethnicity, age, face shape and distinguishing features explicitly in the prompt, since you cannot rely on seeds alone.
- **CFG:** higher CFG generally increases contrast/saturation and the "AI look" in diffusion models. Stay at the documented defaults (Qwen 4.0; Z-Image base 3–5, low end for realism). This is general diffusion knowledge, not verified for these models here.

### Gaps
- **Realism LoRAs** (e.g., commonly cited Civitai realism/amateur-photo LoRAs for FLUX.2 dev, Qwen-Image or Z-Image): not researched, because the search budget was exhausted. No names or settings are given, to avoid fabrication.
- Sampler/scheduler recommendations (e.g., Euler, res_2s, beta schedules in ComfyUI) and FLUX.2 [dev] guidance values: no sources retrieved.

---

## 9. Complete example prompts (at least 10) for realistic avatars

### Takeaway
Below are (A) verbatim community prompts, credited, that already produce convincing realism, and (B) SOP-built prompts that apply the cited principles to the requested scenarios. Every SOP prompt follows the same skeleton: use-case + "photorealistic" → identity → action → environment → camera → lighting → texture → constraints. Per-model adaptation notes follow each one.

### Cited Findings (verbatim, credited)
- **A1. Official OpenAI photoreal baseline (gpt-image-2):**

  ```
  Create a photorealistic candid photograph of an elderly sailor standing on a small fishing boat.
  He has weathered skin with visible wrinkles, pores, and sun texture, and a few faded traditional sailor tattoos on his arms.
  He is calmly adjusting a net while his dog sits nearby on the deck. Shot like a 35mm film photograph, medium close-up at eye level, using a 50mm lens.
  Soft coastal daylight, shallow depth of field, subtle film grain, natural color balance.
  The image should feel honest and unposed, with real skin texture, worn materials, and everyday detail. No glamorization, no heavy retouching.
  ```

  — [OpenAI Cookbook (GitHub)](https://github.com/openai/openai-cookbook/blob/main/examples/multimodal/image-gen-models-prompting-guide.ipynb)
- **A2. Authentic vacation selfie (GPT Image 2), @PurzBeats:** quoted in full in section 5. — [magiccreator-ai repo](https://github.com/magiccreator-ai/awesome-gpt-image-2-prompts)
- **A3. Doorway direct-flash snapshot (GPT Image 2), @WolfRiccardo:** quoted in full in section 5. — [magiccreator-ai repo](https://github.com/magiccreator-ai/awesome-gpt-image-2-prompts)
- **A4. Extremely ordinary iPhone selfie (Nano Banana / GPT-4o era), @jiamimaodashu:** quoted in section 5. Replace the celebrity line with your avatar's description. — [JimmyLv repo](https://github.com/JimmyLv/awesome-nano-banana)
- **A5. Supermarket UGC (GPT Image 2), @hx831126:** excerpt quoted in section 5. The full prompt is in [YouMind GPT Image 2 No. 118](https://github.com/YouMind-OpenLab/awesome-gpt-image-2-prompts).
- **A6. Car back-seat candid (GPT Image 2), @Itx_Sophie, Oct 25 2026, verbatim:**

  ```
  Candid lifestyle portrait of a young woman sitting in the back seat of a moving car, head tilted back against the seat with eyes gently closed, face turned toward the open window and soaking in the sunlight and breeze. Long, dark brown-black hair with wispy bangs, blowing back in the wind with loose strands flying. Soft, natural makeup, dewy skin, relaxed peaceful expression with slightly parted peach-toned lips. Wearing a plain white oversized crew-neck t-shirt and light grey sweatpants, one knee pulled up with her arms wrapped around it. Dark car interior with a black door panel and silver door handle in the foreground. Outside the window, fast-moving green trees heavily blurred by motion. Warm, bright midday sunlight streaming in, with soft highlights on her face and neck. Dreamy, carefree summer road-trip mood, Korean-style cinematic aesthetic, motion blur in the background, shallow depth of field, 50mm lens, f/2, photorealistic, ultra-detailed skin and hair texture, vertical 9:16 composition.
  ```

  — [YouMind GPT Image 2 collection](https://github.com/YouMind-OpenLab/awesome-gpt-image-2-prompts); [original](https://x.com/Itx_Sophie/status/2114202791904412102). Note: this is a lifestyle/editorial look. "Korean-style cinematic aesthetic" and "ultra-detailed" make it less UGC.
- **A7. Phone-camera spec block for a mirror selfie (Nano Banana Pro), @dotey:** see section 3. — [YouMind No. 8](https://github.com/YouMind-OpenLab/awesome-nano-banana-pro-prompts)
- **A8. Webcam couple, early-2000s (Nano Banana Pro), @favprompt:** see section 5. — [YouMind No. 7](https://github.com/YouMind-OpenLab/awesome-nano-banana-pro-prompts)
- **A9. Professional headshot from a selfie (Nano Banana Pro), @PavolRusnak.** Uses "natural, realistic skin texture" and "subtle catchlight in the eyes", plus HEX background "#562226". — [ZeroLu §1.7](https://github.com/ZeroLu/awesome-nanobanana-pro); [original](https://x.com/PavolRusnak/status/1994097306526994558)

### Inferences (SOP-built prompts: my synthesis of the cited principles, not test-rendered)

**P1. Kitchen UGC selfie: Latina woman, early 30s (GPT Image 2 labelled-segment format)**
```
Use case: photorealistic smartphone selfie for a UGC-style social ad; it must look like a real customer filmed it herself.
Subject: a Latina woman in her early 30s, olive skin, dark brown hair in a loose claw-clip bun with flyaway strands, small gold hoops, faded grey crewneck sweatshirt with the sleeves pushed up.
Action: holding the [PRODUCT] up beside her cheek with the label facing the camera, mid-sentence with a natural half-smile, eyes on the phone screen rather than the lens.
Environment: her small apartment kitchen in the morning — white cabinets, a dish rack with two mugs, a fruit bowl with bananas, a kettle, a phone charger cable on the counter, a window over the sink.
Camera: iPhone front camera held at arm's length, slightly above eye level, roughly 24mm-equivalent wide lens with mild perspective stretch near the frame edges, everything in focus with no portrait-mode blur, framing slightly off-centre with her right shoulder cropped, vertical 9:16.
Lighting: soft daylight from the window on camera-left mixed with a warm overhead ceiling bulb, slightly uneven exposure, the window side of her face a little brighter.
Texture: real skin with visible pores, faint under-eye shadows, light shine on the forehead and nose, a few baby hairs; ordinary phone processing — auto HDR, light noise in the shadows, mild JPEG compression, neutral slightly warm colours.
Constraints: product label legible and unchanged; no beauty filter, no retouching, no studio or glamour lighting, no cinematic colour grading, no extra text, no watermark.
```
Model notes:
- **Nano Banana Pro/2:** convert to one narrative paragraph. Pass the product photo as "Image 1: the product, keep label exactly", and the avatar face as "Image 2: identity reference".
- **FLUX.2:** replace the "no …" list with positive phrasing ("natural unretouched skin, everyday phone colours") and add HEX for the sweatshirt ("sweatshirt color #9A9A96").
- **Seedream:** cut to about 90 words, keeping subject, action, camera and light.

**P2. Car selfie: Black man, mid-40s, business coach (info-product)**
```
Photorealistic phone selfie taken by a man sitting in the driver's seat of his parked car, recorded as a quick motivational update for his followers. He is a Black man in his mid-40s, short tapered hair with a little grey at the temples, neatly trimmed beard, navy quarter-zip over a white tee, seatbelt off. He holds the phone at arm's length with one hand, slightly below eye level, looking straight into the front camera with a relaxed, confident expression, mouth slightly open as if talking. Behind him: the passenger seat headrest, the rear window with a blurred parking lot and trees, a sunglasses case on the dashboard edge. Daylight comes through the windshield and the side window, lighting the left side of his face more brightly, with soft shadows under the brow and small reflections on the glass. Wide-angle front-camera look, background mostly in focus, slight phone sharpening, light noise in the darker car interior. Natural skin texture with visible pores, a few razor bumps along the jawline, slight shine on the forehead. Ordinary, unretouched social-media photo, vertical 9:16, no text, no logos.
```
Model notes:
- **Midjourney V8:** shorten to about 40 words and append `--ar 9:16 --raw --stylize 50`. The stylize value is extrapolated from the docs; test 0–100.
- **Z-Image-Turbo:** keep the full text and use 9 steps, CFG 0.

**P3. Gym mirror selfie: South Asian woman, late 20s (fitness supplement)**
```
Photorealistic gym mirror selfie, taken with the phone's rear camera in the mirror of a busy commercial gym. A South Asian woman in her late 20s, medium-brown skin, long black hair in a high ponytail with loose strands stuck to her neck, slightly flushed cheeks and a light sheen of sweat, wearing a black sports bra with a loose grey cropped tee over it and olive leggings. She holds the phone at chest height partially covering her chin, the other hand holding a shaker bottle of [PRODUCT], weight shifted to one hip, casual unposed stance. Mirror shows dumbbell racks, a bench, rubber floor tiles, and another gym-goer out of focus in the background. Lighting: overhead industrial LED panels giving top-down light, highlights on the forehead and shoulders, slightly cool white balance. Phone camera look: about 26mm equivalent, deep depth of field so the background stays readable, a faint smudge on the mirror catching light, mild noise. Real skin texture, no airbrushing, no fitness-magazine polish, vertical 4:5.
```

**P4. Home-office testimonial: white woman, mid-50s (semi-pro "studio-ish" talking-head still)**
```
Photorealistic testimonial portrait for an online course ad, styled like a frame from a self-recorded video interview. A white woman in her mid-50s with chin-length ash-blonde hair, natural grey roots showing slightly, reading glasses pushed up on her head, light makeup, a soft sage-green cardigan over a cream top. She sits at her home desk turned three-quarters toward the camera, hands loosely clasped, mid-laugh while speaking. Background: a bookshelf with mismatched books, a potted pothos, a framed family photo, a warm table lamp switched on. Camera: mirrorless camera on a tripod at eye level, 35mm lens at about f/2.8, background softly out of focus but recognisable, medium close-up from mid-chest up. Lighting: a large window to camera-left as the key light creating soft loop lighting on her face, a white wall bouncing gentle fill on the right, the warm lamp in the background at about 2700K against the cooler daylight. Natural skin with fine lines around the eyes and mouth, light age spots, visible pores, no retouching. Natural colour balance, no cinematic grading, no studio backdrop, no text.
```
Model notes:
- **FLUX.2:** add "Shot on Sony A7 IV, 35mm f/2.8". The BFL guide favours named bodies and lenses.

**P5. Bathroom mirror selfie: East Asian woman, early 20s (skincare)**
```
Photorealistic casual bathroom mirror selfie, taken on an iPhone rear camera through the mirror in a normal rented apartment bathroom (not luxury). An East Asian woman in her early 20s, bare-faced after cleansing, hair pulled back with a fabric headband, a few small blemishes on her chin and faint redness around her nose, wearing an oversized white T-shirt. She holds the phone at chest level with one hand and a small [PRODUCT] bottle near her cheek with the other, slight head tilt, relaxed. Environment: white subway tiles, a basic mirror with a few water spots, a vanity strip light above the mirror, toothbrush cup, a towel hanging on a hook, skincare bottles crowded on the sink edge. Lighting: cool-white vanity light from above casting soft shadows under her brows, slight glare on the tiles. Camera: about 26mm phone lens, deep depth of field, no portrait-mode blur, slight tilt to the frame. Texture: real skin with visible pores and texture, a little dampness at the hairline, natural slightly grainy iPhone look, not over-processed. Vertical 9:16, no text overlays, no watermark.
```
(Camera and texture lines adapted from [@gaucheai via ZeroLu §1.9](https://github.com/ZeroLu/awesome-nanobanana-pro) and [@dotey YouMind No. 8](https://github.com/YouMind-OpenLab/awesome-nano-banana-pro-prompts).)

**P6. Outdoor street: Middle-Eastern man, 60s (candid, shot by a friend)**
```
Photorealistic candid street photo of a man in his 60s of Middle-Eastern descent, olive-tan skin with deep smile lines, short white hair and a salt-and-pepper moustache, wearing a tan linen shirt and a light quilted vest, laughing while holding a takeaway coffee on a busy weekday sidewalk. Shot by a friend on a phone from about two metres away, eye level, slightly tilted horizon, a passer-by partially cropped at the frame edge. Background: café tables, parked scooters, shop awnings, a crosswalk. Overcast late-morning sky acting as soft even light, gentle shadows, muted realistic colours, no sun flare. Phone wide lens with mostly deep focus, slight motion softness in his hand, mild HDR. Natural weathered skin with pores, sunspots and wrinkles, unretouched, everyday documentary feel, vertical 4:5.
```

**P7. Doctor/expert: South Asian male dermatologist, early 50s (authority avatar)**
```
Photorealistic workplace photo of a dermatologist taken by a colleague for the clinic's social media — believable, not a stock photo. A South Asian man in his early 50s with short greying hair, rimless glasses and a neatly trimmed beard, wearing a white coat over a light-blue shirt with a stethoscope draped around his neck, standing in a real exam room and explaining something while holding a small [PRODUCT] tube. Background: an exam chair with paper roll, a wall-mounted magnifier lamp, a sharps container, a skin-anatomy poster with unreadable small text, a window with blinds. Lighting: bright even overhead clinic lights at neutral white (about 5000K) plus soft daylight through the blinds from the right, mild specular highlight on his glasses. Camera: smartphone at chest height, around 26mm, background in focus, medium shot from the waist up, natural slightly cool colour. Real skin with pores and fine lines, slight under-eye creases, no retouching, no cinematic lighting, no logos, no readable text.
```
Note: compliance (impersonating licensed professionals, health claims) is outside this research scope. See Gaps.

**P8. Night party/flash snapshot: mixed group, 20s (fashion/e-commerce)**
```
Photorealistic flash snapshot at a friend's apartment party at night, taken with a compact digital camera with a built-in flash. Two friends in their mid-20s — a Black woman with braided hair in a yellow slip dress and a white man with curly hair in an open denim shirt — squeeze together laughing, her holding a small [PRODUCT] bag up to the lens. Direct on-camera flash: bright highlights on foreheads and noses, crisp catchlights, a hard shadow cast on the wall behind them, dark room falling off quickly, a few string lights blurred in the background. Slightly crooked framing, cropped elbows, a little red-eye-free flash glare. Realistic skin with pores and a little shine, mild noise, slightly blown highlights, unedited look. 3:2 landscape, no date stamp, no text.
```
(Flash vocabulary adapted from [ZeroLu §1.12](https://github.com/ZeroLu/awesome-nanobanana-pro) and [magiccreator-ai](https://github.com/magiccreator-ai/awesome-gpt-image-2-prompts).)

**P9. Living-room couple: older Hispanic couple, 70s (supplements)**
```
Photorealistic candid smartphone photo taken by their grandchild: a Hispanic couple in their 70s sitting close together on a floral sofa in their living room, the woman with short silver curls and a lilac cardigan, the man with a bald crown, white stubble and a plaid flannel shirt, both looking at a [PRODUCT] bottle she is holding and smiling. Room details: crocheted throw on the sofa back, framed family photos, a TV remote and reading glasses on the coffee table, a standing lamp. Late-afternoon window light from camera-right mixed with the warm lamp, slightly uneven exposure, the far side of the room a bit dark. Phone camera at seated eye level, about 26mm, mostly deep focus, framing slightly loose with the coffee table edge in the foreground. Real aged skin with wrinkles, age spots, visible pores, no retouching, warm natural colours, vertical 4:5.
```

**P10. Dorm desk at night: Gen-Z student, East African, 19 (study app / info-product)**
```
Photorealistic late-night laptop webcam-style still of a 19-year-old East African university student, dark brown skin, short natural hair, wearing an oversized hoodie, leaning toward the screen with a tired but excited smile, one hand holding a highlighter. Small dorm room: stacked textbooks, sticky notes on the wall, an energy drink can, tangled earphones, a string of fairy lights. Lighting: cool blue-white laptop screen glow on her face from below-front, plus a warm desk lamp from the left at about 3000K — mixed colour temperature. Camera: built-in laptop webcam at desk level, slight upward angle, soft focus, visible low-light noise and mild compression, slightly cropped top of the head. Real skin texture, no beauty filter, unedited, 16:9.
```

**P11. FLUX.2 JSON version of P1 (with HEX)**
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
(Keys follow the BFL JSON pattern reported by [Atlabs](https://www.atlabs.ai/blog/flux-2-prompting-guide). Exclusions are expressed positively because FLUX.2 has no negatives.)

**P12. Qwen-Image-2512 run settings (for any of P1–P10)**

Settings:
- prompt: one continuous ~200-word English block;
- `negative_prompt`: the official Chinese list from section 6;
- `true_cfg_scale=4.0`, 50 steps;
- size 928×1664 for 9:16;
- omit "cinematic composition" from `positive_magic` for UGC (an inference to A/B test).

Source for the defaults: [Qwen-Image README](https://github.com/QwenLM/Qwen-Image).

### Gaps
- None of the SOP-built prompts (P1–P12) were test-rendered in this session. They should be A/B tested per model before being codified.
- No examples were retrieved from Spanish/Portuguese/Russian creators, Reddit, Civitai or PromptHero (search budget exhausted, and most of those domains were unreachable by fetch).
- **Legal/compliance:** using realistic AI avatars as fake "customers", "testimonials" or "doctors" in ads raises disclosure and consumer-protection issues (e.g., rules on fake reviews/endorsements and platform AI-labelling policies). This was not researched here and should be covered by another workstream before the SOP ships.
