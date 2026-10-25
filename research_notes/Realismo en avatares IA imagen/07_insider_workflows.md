# Insider practitioner workflows for ultra-realistic AI avatar STILL images (state as of Oct 2026)

*How this was researched: the session's shared web-search budget ran out after about 13 searches, and the proxy blocked WebFetch for almost every non-GitHub domain (x.com, reddit, ftc.gov, ecfr.gov, higgsfield.ai, magnific.com, note.com, nespol.com.br and others returned DNS/403 errors). So findings marked "(search summary)" come from search-engine summaries of the cited page, not from a full read. Verbatim prompts were taken directly from the raw GitHub READMEs of the community prompt collections, which cite the original X posts. Each prompt's date is the "Published" date shown in that repo.*

---

## 1. End-to-end workflows and tool stacks for avatar stills (2025–2026)

### Takeaway
The pro pipeline that repeats across sources has four stages: (1) create a "hero" or anchor character image, (2) lock identity with a reference image, Higgsfield Soul ID or a LoRA, (3) generate scenes in batches with a fixed base prompt plus small per-shot changes, (4) run a separate skin-texture and upscale pass (Enhancor / Magnific Skin Enhancer), then fix text and logos in Nano Banana Pro or Photoshop. Nano Banana Pro / Nano Banana 2, Higgsfield Soul 2.0 and GPT Image 2.x are the most-cited generators in late 2026. Almost all workflow sources are vendors or affiliates.

### Cited Findings
- **Hero-reference method (repeated by several sources):** generate one "hero" character, upload it with every new generation, and prompt "same person in a new scene". Claimed to hold consistency for **5–10 generations** with reference images in Nano Banana Pro — [adlibrary.com UGC prompting guide 2026](https://adlibrary.com/guides/ai-prompting-guide-ugc-content-creators) (search summary). The Portuguese summary of the same guide repeats the 5–10 claim — [adlibrary.com](https://adlibrary.com/guides/ai-prompting-guide-ugc-content-creators).
- **Base prompt + micro-prompts + parallel shots:** write a base prompt that fixes **subject, lens and lighting**, then add micro-prompts for expression and hand action, and **generate five parallel shots and pick the cleanest frame set** — [adlibrary.com](https://adlibrary.com/guides/ai-prompting-guide-ugc-content-creators) (search summary).
- **German UGC stack:** Nano Banana Pro for avatar and scene stills, then Veo 3.1 for animation. The avatar template prompt uses diffused frontal light, everyday clothing, a specific urban setting and no text overlay. The avatar "should look natural and not overly polished" to read as UGC — [Laria.ai (DE)](https://www.laria.ai/en/blog/so-erstellst-du-hochwertige-ki-generierte-ugc-videos-mit-nano-banana-pro-und-veo-3.1) (search summary).
- **Higgsfield Soul ID workflow (the most detailed vendor SOP found):** generate a batch of portraits of the finished character in Influencer Studio, train a Soul ID on them, and use that ID for all later content. Lock the face *before* spending video credits, because going straight from one reference image tends to cause face drift. One source says Soul ID needs **at least 20 photos**, trains in about 3 minutes and can then be reused without limit. Weak or overly uniform training photos encode the wrong face, age, makeup or photographic style. — [Higgsfield blog: consistent AI influencer 2026](https://higgsfield.ai/blog/how-to-create-ai-influencer); [Higgsfield Soul ID blog](https://higgsfield.ai/blog/Soul-ID-AI-Character-Consistency); [The Post Flow](https://thepostflow.com/ai/how-to-create-an-ai-influencer/); [media.io Soul ID guide](https://www.media.io/video-tips/soul-id-character-consistency.html) (search summary; the sources are mostly Higgsfield's own blog).
- **What to train Soul ID on:** recent, well-lit photos with varied angles and expressions, no sunglasses or heavy shadows, and at least one full-height shot — [Higgsfield blog](https://higgsfield.ai/blog/how-to-turn-photo-into-consistent-ai-persona-creator) (search summary).
- **Soul 2.0 modes:** Soul (text-to-image), Soul Reference (match a moodboard or campaign look) and Soul ID (same person across shots). Presets such as "Street Photography" or "Frutiger Aero" set the lighting, color and composition tendencies before any prompt is written — [Tech Surges Insider: Soul 2.0](https://techsurgesinsider.substack.com/p/higgsfield-soul-20); [Chase Jarvis: Higgsfield Soul](https://chasejarvis.com/blog/higgsfield-soul/) (search summary).
- **Cross-tool cleanup step:** take a Soul-generated character into **Nano Banana Pro to fix text on a hat, correct a logo and stabilize the pose** — [Higgsfield-related tutorials, search summary](https://aiidelist.com/blog/higgsfield-ai-influencer); see also [CreatoorHQ: adding products to AI photos](https://creatoorhq.substack.com/p/how-to-add-products-to-ai-photos).
- **Skin and texture finishing pass:** Enhancor's skin models add pores and micro-texture back into AI portraits. It also sells a "Kora Reality" digital-human generator and a human-aware upscaler. Upscale limits conflict: the vendor and some pages say up to 8K, one review says 4K — [Enhancor](https://www.enhancor.ai/); [i10x review](https://i10x.ai/tools/enhancor); [Product Hunt](https://www.producthunt.com/products/enhancor); [TechPilot](https://techpilot.ai/tools/enhancor-ai-fix-the-ai-plastic-skin/) (search summary).
- **Magnific vs Enhancor (one editorial opinion):** Magnific "is aggressive; it often changes the geometry of a face or adds unwanted elements". Enhancor is constrained to preserve identity and geometry, which makes it safer when the subject must not change — [Chase Jarvis: best AI upscaler 2026 guide](https://chasejarvis.com/blog/best-ai-image-upscaler/) (search summary; single source).
- **Magnific Skin Enhancer:** restores pores and soft shadows and can target specific areas. It has an official ComfyUI API workflow — [Magnific blog: fixing plastic skin](https://www.magnific.com/blog/how-to-fix-plastic-skin-ai-skin-enhancer/); [ComfyUI workflow](https://comfy.org/workflows/api_magnific_skin_enhancer-81643690b5e9/) (search summary).
- **Model landscape, late 2026:** Google released **Nano Banana 2**, described as "Pro-level image generation and editing at the speed you expect from Flash" — [Google Cloud blog](https://cloud.google.com/blog/u/1/products/ai-machine-learning/bringing-nano-banana-2-to-enterprise). OpenArt positions Nano Banana 2 for everyday images and Pro for more consistent, polished results — [OpenArt blog](https://openart.ai/blog/best-nano-banana-prompts-for-viral-photos/) (search summary).
- **GPT Image 2.x + JSON style reference + character reference (September 2026 X thread):** "using this json as reference, generate a person holding my product [attach product image]"; "save the generated character photo you're happy with as your reference"; "for future generations, attach the character photo each time and ask it to preserve the same facial features"; "the json gives GPT-Image 2.5 the lighting and color direction, your character reference helps with consistency, and you control the product placement". The post says "GPT-Image 2.5 Sunburst & Flare are available on Higgsfield" — Miko [@Mho_23, 9 Sep 2026](https://x.com/Mho_23/status/2097483045221917131), via [YouMind awesome-gpt-image-2 repo](https://github.com/YouMind-OpenLab/awesome-gpt-image-2). The model names "GPT-Image 2.5" and "GPT-6 Astra" come from this post only and were not independently verified.
- **Seedream vs Nano Banana:** vendor comparisons say Nano Banana keeps facial features, proportions and expressions more consistent than Seedream 4.0. A newer comparison says Seedream 5.0 Lite preserves identity across edits — [ImagineArt: NB vs Seedream 4.0](https://www.imagine.art/blogs/nano-banana-vs-seedream-4.0); [ImagineArt: NB2 vs Seedream 5.0 Lite](https://www.imagine.art/blogs/nano-banana-2-vs-seedream-5-0-lite) (marketing-adjacent).
- **LoRA route (open-source / ComfyUI):** a fixed seed reproduces one image but "does not generalize to new poses, new outfits, or new backgrounds". The usual fix is a LoRA trained on **15–30 images** with varied angles, lighting and expressions — [Ryla.ai consistency guide 2026](https://ryla.ai/en/blog/ai-influencer-consistency/) (search summary; vendor). Community realistic-influencer LoRAs for SDXL/Pony exist on Hugging Face — [Stableyogi LoRA](https://huggingface.co/Stableyogi/Realistic-Virtual-AI-Influencers/blob/main/README.md).
- **Fal hosts Nano Banana Pro via API**, the usual route for agencies that script batches — [fal blog](https://blog.fal.ai/nanobana-pro-is-now-available-on-fal/).

### Inferences
- The canonical 2026 still-image SOP that emerges is: Anchor (hero image or a 20+ image Soul ID / LoRA set) → Scene generation (fixed base prompt + micro-variations, 4–5 parallel takes) → Selection → Skin pass (identity-preserving tool first; Magnific only with low creativity, because it can change faces) → Text/logo fix (NB Pro edit or Photoshop overlay) → Upscale. Higgsfield and Laria/adlibrary all describe the same stages, so stage order is well corroborated. Specific settings are not.
- Practitioners increasingly split "identity", "look" (a JSON or preset for color and light) and "product" into separate inputs (Miko thread, Soul Reference vs Soul ID). This modular reference-stacking looks like the 2026 pro pattern.

### Gaps
- No practitioner write-ups were retrieved on **Weavy / Figma Weave, Krea, Freepik Spaces, OpenArt workflows, FLUX.2, Topaz (Gigapixel/Bloom), Arcads, MakeUGC, Creatify, HeyGen avatar photo or Captions** for stills. Search budget ran out, and docs.topazlabs.com and openart.ai were blocked by the proxy. Their role in the stack is unverified here.
- No exact Magnific or Enhancor settings (creativity, resemblance, HDR, "skin detail" values) could be pulled, because their pages were blocked.
- Higgsfield credit costs, Soul ID training time and photo minimums may have changed. The sources are Higgsfield's own blog posts with varying dates.

---

## 2. Viral "realism" prompts and prompt formulas (verbatim where possible)

### Takeaway
Three families of prompt went viral and keep being reused: (a) the **"extremely ordinary / accidental iPhone snapshot"** formula, (b) **era cameras** (early-2000s digital camera with harsh flash, compact-camera screen, webcam), and (c) **JSON / sectioned spec sheets** that name the phone camera's real parameters (26 mm equivalent, f/1.8, ISO, "no portrait mode") and end with a negative list ("no beauty filter, no poreless skin, no fake portrait-mode blur"). All three appear across EN, ZH and JA creators, in several repos and on X.

### Cited Findings
- **"Extremely Ordinary iPhone Selfie"** by @jiamimaodashu (2025; one of the most-copied realism prompts, also run on GPT-4o). The first paragraph is the reusable template. The original second line named two real celebrities, so it **must be replaced with a fictional subject**:
  ```
  Please draw an extremely ordinary and unremarkable iPhone selfie, with no clear subject or sense of composition — just like a random snapshot taken casually. The photo should include slight motion blur, with uneven lighting caused by sunlight or indoor lights resulting in mild overexposure. The angle is awkward, the composition is messy, and the overall aesthetic is deliberately plain — as if it was accidentally taken while pulling the phone out of a pocket.
  ```
  — [X source](https://x.com/jiamimaodashu/status/1912653073190879410), via [JimmyLv/awesome-nano-banana, Case 54](https://github.com/JimmyLv/awesome-nano-banana). A Japanese write-up says this "too ordinary smartphone photo" style has circulated on Reddit since about 2025 and has resurfaced as a trend with GPT Image 2 — [note.com/petabyte_ai](https://note.com/petabyte_ai/n/n9c83d1c9296b?hl=en) (search summary). **Widely corroborated** (several repos, Reddit, Japanese blogs).
- **"2000s Mirror Selfie" JSON** by @ZaraIrahh (Nov 2025, viral on Nano Banana Pro). The photography and background blocks are verbatim:
  ```json
  "photography": {
    "camera_style": "early-2000s digital camera aesthetic",
    "lighting": "harsh super-flash with bright blown-out highlights but subject still visible",
    "angle": "mirror selfie",
    "shot_type": "tight selfie composition",
    "texture": "subtle grain, retro highlights, V6 realism, crisp details, soft shadows"
  },
  "background": {
    "setting": "nostalgic early-2000s bedroom",
    "wall_color": "pastel tones",
    "elements": ["chunky wooden dresser","CD player","posters of 2000s pop icons","hanging beaded door curtain","cluttered vanity with lip glosses"],
    "atmosphere": "authentic 2000s nostalgic vibe",
    "lighting": "retro"
  }
  ```
  The subject block also uses `"face": {"preserve_original": true, ...}` — [X source](https://x.com/ZaraIrahh/status/1991681614368436468), via [ZeroLu/awesome-nanobanana-pro §1.2](https://github.com/ZeroLu/awesome-nanobanana-pro).
- **"Casual iPhone mirror selfie" JSON camera block.** The photography block of a widely shared NB Pro bathroom mirror-selfie prompt is quoted verbatim below. The subject and styling block was sexualized and is deliberately omitted.
  ```json
  "photography": {
    "camera_style": "casual iPhone mirror selfie, NOT professional",
    "quality": "iPhone camera - good but not studio, realistic social media quality",
    "angle": "eye-level, straight on mirror",
    "shot_type": "3/4 body, close to mirror",
    "aspect_ratio": "9:16 vertical",
    "texture": "natural, slightly grainy iPhone look, not over-processed"
  },
  "background": { "setting": "regular apartment bathroom", "style": "normal NYC apartment bathroom, not luxury", ... }
  ```
  — [ZeroLu/awesome-nanobanana-pro §1.9](https://github.com/ZeroLu/awesome-nanobanana-pro). The insider moves here are explicit **"NOT professional"**, **"not luxury"** and **"not over-processed"** negations *inside* the JSON values.
- **Phone-camera spec sheet** by 宝玉 / @dotey (10 Oct 2025). The camera block is verbatim. It is the clearest example of "describe the real phone, not a DSLR":
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
  — [X source](https://x.com/dotey/status/1976485558319722711), via [YouMind awesome-nano-banana-pro-prompts](https://github.com/YouMind-OpenLab/awesome-nano-banana-pro-prompts). (The original subject block is borderline-revealing; reuse only the camera, lighting and negative structure.)
- **"Consumer-phone snapshot / buyer-show" e-commerce prompt** by 虎小象 @hx831126 (8 Sep 2026, GPT Image 2). Key lines verbatim:
  ```
  Create a realistic vertical smartphone photo of a candid grocery-store shopping moment in a Korean supermarket. [...] The scene contains exactly one main shopper, one black basket, two background shoppers, one shopping cart in the background [...] Use a natural consumer-phone snapshot style, slightly imperfect framing, realistic indoor fluorescent lighting, mild motion softness, neutral colors, glossy gray supermarket floor reflections, deep aisle perspective, and authentic everyday details. Make it look like a casual buyer-show or store social media photo rather than a studio fashion shoot. No glamour lighting, no exaggerated posing, no artificial-looking skin, no extra people, no watermark.
  ```
  — [X source](https://x.com/hx831126/status/2097453683609137635), via [YouMind awesome-gpt-image-2](https://github.com/YouMind-OpenLab/awesome-gpt-image-2). Two insider tricks: **counting every object exactly** ("exactly one... two background shoppers") and the Chinese e-commerce concept **"buyer-show" (买家秀)**, meaning the look of a real customer photo as opposed to a seller photo.
- **Low-res webcam / "old Facebook album" prompt** by @favprompt (21 Oct 2026, NB Pro):
  ```
  A candid couple photo of the Woman's Look and Man's Look in the Setting, engaged in the Activity. Render it as the Camera Type, with soft focus, smeared facial detail, color noise, dim uneven indoor light and low-resolution compression. Use awkward webcam framing from a desk-level angle, with a slight tilt and casually cropped shoulders or arms. [...] The couple should look genuinely close and relaxed, with real skin, messy everyday hair and no heavy retouching. Use Face Reference for the matching faces when applicable. Make it feel like an unedited early-2000s personal photo from an old Facebook album or MSN chat, not a modern image with a retro filter. No date stamp, text, watermark, modern electronics or current fashion.
  ```
  — [X source](https://x.com/favprompt/status/2112947693710360593), via [YouMind NB Pro repo](https://github.com/YouMind-OpenLab/awesome-nano-banana-pro-prompts). Note the phrase **"not a modern image with a retro filter"**: it tells the model to simulate the capture device, not to apply a filter look.
- **Harsh on-camera flash "amateur snapshot" formula** by @Arminn_Ai: "Harsh, direct on-camera flash lighting that creates hard shadows behind the subjects. Authentic film grain, slight motion blur on the edges, and chromatic aberration. It looks like a candid, amateur snapshot as if captured during a chaotic behind-the-scenes moment, not a studio photo." — [ZeroLu §1.12](https://github.com/ZeroLu/awesome-nanobanana-pro).
- **Compact digital camera screen** by @kingofdairyque: "...illuminated by a bright built-in flash that creates sharp highlights on her face and hair. [...] dim, cluttered kitchen background [...] The mood is candid, raw, nostalgic, and reminiscent of early 2000s digital camera snapshots. Colors are slightly muted with cool undertones, strong flash contrast, and natural grain from the display." — [ZeroLu §1.15](https://github.com/ZeroLu/awesome-nanobanana-pro).
- **Film-look lifestyle (WeChat-origin):** "Keep the facial features of the person in the uploaded image exactly consistent. Style: A cinematic, emotional portrait shot on Kodak Portra 400 film. Setting: An urban street coffee shop window at Golden Hour [...] Apply a subtle film grain and soft focus [...] holding a coffee cup, with a relaxed, candid expression." — [ZeroLu §1.6](https://github.com/ZeroLu/awesome-nanobanana-pro).
- **Professional headshot (usable for "expert/coach" avatars)** by @PavolRusnak: "...framed from the chest up, with ample headroom. The person looks directly at the camera. [...] premium smart casual blazer in a subtle charcoal gray. [...] bright and airy soft, diffused studio lighting [...] Captured on an 85mm f/1.8 lens with a shallow depth of field, exquisite focus on the eyes [...] crisp detail on the fabric texture of the blazer, individual strands of hair, and natural, realistic skin texture." — [X source](https://x.com/PavolRusnak/status/1994097306526994558), via [ZeroLu §1.7](https://github.com/ZeroLu/awesome-nanobanana-pro).
- **Reusable negative list for identity plus realism:** "no CGI appearance, no plastic skin, different face, identity drift, face morphing, altered facial structure, asymmetrical eyes caused by errors, plastic skin, excessive retouching, doll-like face, blurry face, unnatural body proportions, extra fingers, missing fingers, fused hands [...] floating accessories, unrealistic fabric, oversaturated colors, CGI, cartoon" — [YouMind NB Pro repo](https://github.com/YouMind-OpenLab/awesome-nano-banana-pro-prompts). "Plastic skin" and "excessive retouching" appear as negatives in dozens of entries across the YouMind repos.
- **Skin imperfection phrase (GPT Image 2, Oct 2026):** "Her skin is fair with visible natural texture, including freckles and small blemishes, giving a raw, unretouched look." — [YouMind awesome-gpt-image-2](https://github.com/YouMind-OpenLab/awesome-gpt-image-2).
- **3x3 contact-sheet JSON** by @SheBuildsAI_ (5 Sep 2026). It produces nine shots of the same person in one generation (`"format": "3x3 contact sheet collage"`, with a `"shots"` list of 9 framings, `"color_temperature": "3200K"`, `"look": "Kodak Vision3 film emulation"` and `"details": [..."realistic skin texture"..."candid documentary photography"...]`) — [X source](https://x.com/SheBuildsAI_/status/2096191621838864712), via [YouMind NB Pro repo](https://github.com/YouMind-OpenLab/awesome-nano-banana-pro-prompts).
- **Paid prompt market:** Gumroad sells "iPhone selfie / realistic" prompt packs and generators priced from about **$5 to $66** — [promptergen](https://promptergen.gumroad.com/l/idxraf), [thebaddiebriefcase](https://thebaddiebriefcase.gumroad.com/l/ygdak), [midnightlab "infucam"](https://midnightlab.gumroad.com/l/infucam) (search summary; contents unverified).

### Inferences
- The shared structure of the viral 2025–26 realism prompts is: **[capture device + mode] + [who is "holding the camera"] + [light that is uneven or from a named practical source] + [composition flaw] + [explicit negation of studio, pro or luxury] + [negative list for skin and identity drift]**. The "photo dump", "Instagram candid" and "mirror selfie with flash" variants are all instances of it.
- JSON is popular less because the model "reads JSON better" and more because it forces creators to fill every slot (camera, light, background props), so nothing is left to the model's glossy default. This is an inference; no source tested JSON against prose head-to-head.

### Gaps
- Could not retrieve the original X threads (x.com blocked) to confirm engagement numbers or exact virality.
- No verbatim "photo dump" or "Instagram candid" prompt from a named 2026 source was found within the search budget.

---

## 3. Tricks to defeat the "AI look" (legitimate realism, not detection evasion)

### Takeaway
English, Chinese and Japanese sources agree that the "AI look" comes from **flawlessness**: poreless skin, perfect symmetry, studio-perfect light and clean backgrounds. The fix is *controlled imperfection*, described in **photographic** language rather than quality adjectives. Examples include awkward angles, mild overexposure, real phone depth of field and lived-in props. Pros also strip "8K, masterpiece, ultra-detailed" from prompts.

### Cited Findings
- AI images without casual framing show "skin that is too smooth, lighting that is too perfect, and backgrounds that are too clean" — [note.com/petabyte_ai (JA)](https://note.com/petabyte_ai/n/n9c83d1c9296b?hl=en) (search summary).
- **Stop stacking "8K / 大师级画质 (masterpiece quality)".** Instead add light film grain and natural skin texture. The AI tell is traced to prompting for "flawless" — [Zhihu: 去除图片AI味 3大提示词技巧](https://zhuanlan.zhihu.com/p/2054517785917760150) (search summary).
- **Use photography language, not painting language:** name the focal length, natural window light and film grain, which works better than "高清精美 (HD, exquisite)". Common AI tells are over-smooth skin and materials, unreal symmetry and plastic-like sheen. **Name the light direction** (e.g., sunlight through foliage casting dappled spots) rather than vague "氛围感 (vibe)" — [Peituka: 8 tips to remove the AI look](https://peituka.com/blog/avoid-ai-look-realistic-images) (search summary).
- **Don't write "Xiaohongshu style / fresh / ins style".** That yields over-beautified, fake images. Describe *the act of shooting* instead — Chinese test write-up surfaced alongside [CSDN: FLUX 小红书 model + ChatGPT prompt optimization](https://agent.csdn.net/6a4e40df10ee7a33f289b58f.html) and [Peituka](https://peituka.com/blog/avoid-ai-look-realistic-images) (search summary; exact attribution between the two is unclear).
- "Adding micro-imperfections, pores, slight uneven texture, a few marks, makes the image dramatically more realistic. Smooth, perfect AI skin is the number one tell" — [Ryla.ai](https://ryla.ai/en/blog/ai-influencer-consistency/) (vendor; search summary). The same guide recommends running images through a skin tool with an "imperfect skin" preset.
- **Ask explicitly for a non-professional look** in Nano Banana Pro: phrases such as "not a professional photo" and "no studio lighting". Also prompt handheld, imperfect framing, grain and uneven light — [adlibrary.com](https://adlibrary.com/guides/ai-prompting-guide-ugc-content-creators) (search summary).
- **Brazilian realism intensifiers:** turn a reference photo into a detailed prompt, add "natural grain" and "slight chromatic aberration", and explicitly avoid "waxy skin / CGI look". Tools named: ChatGPT, Dreamina, Nano Banana 2 — [iAWilker (PT-BR)](https://prompt.iawilker.com/prompts/avatar-realista-ia-prompt/) (search summary).
- **Watch color and grain:** "the basic colours and grainy look are some of the things that can make an image feel AI-generated, so pay attention to those when comparing your results". The fix is a JSON style reference for color grading — Miko [@Mho_23, Sep 2026](https://x.com/Mho_23/status/2097483045221917131) via [YouMind gpt-image-2 repo](https://github.com/YouMind-OpenLab/awesome-gpt-image-2). This **conflicts in part** with the many sources that *add* grain. The reconciliation is that generic, uniform grain also reads as fake; grain must match the simulated device.
- **Real phone optics instead of fake bokeh:** "natural smartphone deep depth of field; background clearly visible with no artificial blur" and negative "Fake portrait-mode blur" — [@dotey via YouMind](https://github.com/YouMind-OpenLab/awesome-nano-banana-pro-prompts).
- **Simulate the device, don't filter:** "not a modern image with a retro filter" — [@favprompt via YouMind](https://github.com/YouMind-OpenLab/awesome-nano-banana-pro-prompts).
- **Negate the beauty bias inside the prompt:** "No glamour lighting, no exaggerated posing, no artificial-looking skin" — [@hx831126 via YouMind gpt-image-2](https://github.com/YouMind-OpenLab/awesome-gpt-image-2); "Beauty filters/over-smoothed skin; poreless skin look" as negatives — [@dotey](https://x.com/dotey/status/1976485558319722711); "normal NYC apartment bathroom, not luxury" — [ZeroLu §1.9](https://github.com/ZeroLu/awesome-nanobanana-pro).
- **Lived-in context props** are listed explicitly (CD player, cluttered vanity, tangled cables, laminate desk, worn carpet) — [ZeroLu §1.2](https://github.com/ZeroLu/awesome-nanobanana-pro); [@favprompt](https://x.com/favprompt/status/2112947693710360593).
- **Real reference images for light, color and pose:** attach a style JSON or inspiration image for lighting and color, then compare against a no-reference version — [Miko via YouMind](https://github.com/YouMind-OpenLab/awesome-gpt-image-2). Soul Reference does the same for moodboards — [Tech Surges Insider](https://techsurgesinsider.substack.com/p/higgsfield-soul-20).

### Inferences
- **"Photo taken by a friend" or "by the shopper's phone"** framing is the de facto pattern: every high-signal prompt names who is capturing (mirror, webcam, buyer, pocket accident). This is triangulated across EN, ZH and JA examples above.
- Diversity and age realism: the sourced prompts that specify age, ethnicity and skin tone explicitly (e.g., @dotey's "Age: around 25 / Ethnicity: East Asian / Skin tone: light neutral tone") suggest that leaving demographics blank lets the model's default "AI face" through. This is an inference; no source measured it.

### Gaps
- **No source was found** supporting the claim that "average-looking" people convert better or build more trust in ads, and no A/B data either. Treat it as unverified folklore until tested.
- No dedicated source on the "same AI face / default face" problem beyond the LoRA and Soul ID advice; no study on ethnic or age realism bias for specific 2026 models.

---

## 4. E-commerce and info-product needs (product holding, labels, expert avatars, testimonials, before/after)

### Takeaway
Product fidelity is still the weak point. Practitioners use **the real product photo as a reference input**, prefer Nano Banana Pro for shadows and reflections, and **put the real label/packaging artwork back in a separate edit step** (Photoshop or an NB Pro text fix) instead of trusting generated text. For expert, doctor or coach avatars, the studio-headshot prompt family is used. Testimonial-style stills run straight into FTC and platform rules (Section 7).

### Cited Findings
- **Fstoppers test (independent-leaning):** Nano Banana Pro wins on natural shadows and reflections when inserting products into photos. The advice is to "handle labels separately in Photoshop, and expect consistency challenges across campaign frames" — [Fstoppers: AI product insertion, NB Pro vs ChatGPT 5](https://fstoppers.com/artificial-intelligence/inserting-products-existing-photos-ai-what-actually-works-901419) (search summary).
- **Vendor claims on text:** fal says NB Pro renders "clean, legible, and accurate text, even in complex environments like signage, labels, packaging, or UI screens" — [fal blog](https://blog.fal.ai/nanobana-pro-is-now-available-on-fal/). Media.io promotes logos, labels and prices in-image — [media.io](https://www.media.io/image-effects/ai-product-photo.html). The Fliki review found multilingual logos good but could not verify Japanese accuracy — [Fliki](https://fliki.ai/blog/nano-banana-pro-review) (search summary).
- **Known failure (2025, base Nano Banana):** it struggles with exact proportions ("logos warp, edges melt") and with complex product poses such as objects held by humans — [Medium: NB for product photography 2025](https://medium.com/ai-product-photography/how-to-use-nano-banana-for-product-photography-2025-guide-a0b91c6c928f) (search summary; older; the author promotes another product).
- **Person-holding-product recipe (Sep 2026):** "using this json as reference, generate a person holding my product [attach product image]", then reuse the saved character photo for later product shots, building "a library of high quality ugc images around your own products" — [Miko @Mho_23](https://x.com/Mho_23/status/2097483045221917131) via [YouMind gpt-image-2](https://github.com/YouMind-OpenLab/awesome-gpt-image-2).
- **Oversized-prop interaction (Chinese e-commerce trend, Oct 2026):** the person holds the prop with "a simple, direct, instantly readable interactive action" (holding up, offering to camera, lifting to chest), and "[Prop] occupies a large portion of the frame, close to the scale of the person's head or upper body" with "shape is complete, outline is distinct". The prompt also states "The person must clearly be an adult" — VoxCat [@VoxcatAI, 8 Oct 2026](https://x.com/VoxcatAI/status/2108192853742456945) via [YouMind gpt-image-2](https://github.com/YouMind-OpenLab/awesome-gpt-image-2). (The default subject is an anime IP character; for commercial use, swap in a fictional person and the client's own product.)
- **Studio product cleanup prompt** (removes hands and clutter for a white-background hero shot): "Cleanly extract the product, completely removing any fingers, hands, or clutter. Background: Place the product on a pure white studio background (RGB 255, 255, 255) with a subtle, natural contact shadow..." — [ZeroLu §4.2](https://github.com/ZeroLu/awesome-nanobanana-pro). This is useful for producing a clean product reference *before* compositing it into avatar shots (inference).
- **Chinese e-commerce rule:** base detail shots on **real product photos**. If part of the original is unclear, re-shoot it rather than let the AI guess — [DEV.to: 双十一 e-commerce main-image prompt collection (ZH)](https://dev.to/aioae/shuang-shi-bei-zhan-dian-shang-zhu-tu-ti-shi-ci-he-ji-bai-di-tu-chang-jing-tu-mo-te-shang-shen-ci-zheng-li-55g5) (search summary).
- **Older SD-era garment-fidelity trick (2024):** inpaint around the garment at denoise **0.3–0.6** to keep the clothing intact, and fix face and hands with ADetailer — [CSDN (2024)](https://blog.csdn.net/Java_Joker/article/details/140374226) (search summary; older).
- **Expert/coach headshot:** see the @PavolRusnak prompt in Section 2 and ZeroLu §1.5 "One-Click Business Photo" ("Render natural skin texture with visible pores", navy suit, three-point light, 85 mm look) — [ZeroLu](https://github.com/ZeroLu/awesome-nanobanana-pro).
- **Brazilian TikTok-influencer structured prompt:** sections for face, hair, clothing, pose, setting, lighting and quality, keeping the same person across frames. Made in Google Flow (Labs) with Nano Banana — [Nespol (PT-BR)](https://nespol.com.br/blog/prompts-gratis-movimentos-realistas-em-influencers-ugc-feitas-com-ia/) (search summary).

### Inferences
- The pro answer to label accuracy is **"never trust generated text on the hero product"**: generate the scene, then composite or overlay the real label, or use an NB Pro targeted text-fix edit, and QA the text at 100% zoom. Fstoppers, Higgsfield-tutorial cleanup and the Chinese "use real product photos" rule all agree.
- For testimonial-style stills, the realism techniques in this document make an image *more* likely to be taken as a real customer. That is exactly what the FTC rule and platform labels target (Section 7). Any "customer" still should be labeled and never paired with a fabricated review.

### Gaps
- **Before/after imagery:** no source retrieved this session on 2026 Meta/TikTok policy for AI before/after images (health, weight loss, skincare). It needs a dedicated compliance check; it is high-risk.
- No quantified data on label-accuracy rates per model (NB Pro vs GPT Image 2 vs Seedream) for products held at an angle.
- **No LatAm/Spain-specific** sources on local trust aesthetics (settings, housing, skin tones, wardrobe) were found within budget; only the Brazilian Nespol and iAWilker pages surfaced.

---

## 5. What non-English communities share that English ones don't

### Takeaway
Chinese creators bring the **"buyer-show" (买家秀) aesthetic**, exact object counting, phone-EXIF spec sheets and a sharp "de-AI-flavor" (去AI味) vocabulary that bans beauty buzzwords. Japanese creators favor **sectioned bracket prompts** ([Overall Theme], Person & Expression, Composition & Camera) tuned for 9:16 phone screens. Brazilian creators package realism into free structured prompt templates for TikTok-style influencers. Russian, Korean and Spanish-specific material could not be retrieved.

### Cited Findings
- **Chinese (ZH):**
  - "Buyer-show / casual store social media photo rather than a studio fashion shoot", exact counts of every object, and "consumer-phone snapshot style" — [@hx831126 (虎小象), Sep 2026](https://x.com/hx831126/status/2097453683609137635) via [YouMind gpt-image-2](https://github.com/YouMind-OpenLab/awesome-gpt-image-2).
  - Phone camera parameters (26 mm equivalent, f/1.8, ISO 100, 1/100 s, EV -0.3, 5200 K, "no portrait/bokeh mode") — [宝玉 @dotey, Oct 2025](https://x.com/dotey/status/1976485558319722711).
  - De-AI vocabulary: avoid "8K / 大师级画质"; use photographic terms; name light direction; avoid "小红书风格/ins风" keywords — [Zhihu](https://zhuanlan.zhihu.com/p/2054517785917760150); [Peituka](https://peituka.com/blog/avoid-ai-look-realistic-images) (search summary).
  - Large Chinese prompt libraries for 女装 (womenswear), 童装 (kidswear), 电商主图 (e-commerce main images) and 小红书封面 (Xiaohongshu covers): "5000+" prompts — [V2EX](https://www.v2ex.com/t/1213012) (search summary).
  - The copy side of "de-AI" stresses that first-person "I used it" claims should only be written when real experience exists, to avoid fabrication — [Sohu: 120 de-AI instructions](https://www.sohu.com/a/1080405402_121124293); [GitCode/CSDN 2026 test](https://gitcode.csdn.net/69d923780a2f6a37c59ead60.html) (search summary). This aligns with FTC rules.
  - WeChat articles are a named source of NB Pro portrait prompts (Kodak Portra coffee-shop prompt, business headshot "visible pores") — [ZeroLu §1.5–1.6](https://github.com/ZeroLu/awesome-nanobanana-pro).
- **Japanese (JA):**
  - Structured section headers ("Subject / Main Subject / Person & Expression / Clothing & Pose / Background & Light / Composition & Camera") with very specific facial geometry ("Small oval face, soft jawline...") — [@CyberTotal2026, Sep 2026](https://x.com/CyberTotal2026/status/2101659894357139704) via [YouMind gpt-image-2](https://github.com/YouMind-OpenLab/awesome-gpt-image-2).
  - "[Overall Theme] A daily snapshot of..." and "Create a vertical portrait image with an aspect ratio of 9:16 optimized for smartphone screens" — [@kawagoe_ai, Oct 2026](https://github.com/YouMind-OpenLab/awesome-nano-banana-pro-prompts).
  - An image-to-image "Shallow Depth of Field" finishing prompt: "Focus center on eyes and face [...] smoothly blur hair, shoulders, costume, and background according to distance. [...] Uniform blurring across the entire screen is prohibited. Do not erase facial details" — [Eris Create Lab, 22 Oct 2026](https://x.com/Eris_Create_Lab/status/2113101283678691396) via [YouMind gpt-image-2](https://github.com/YouMind-OpenLab/awesome-gpt-image-2). This is a *second-pass* edit used to fix flat, uniform AI focus. It is the opposite of the phone deep-DOF approach and fits "pro photo" avatars, not UGC.
  - Japanese blog coverage of the GPT Image 2 "show your face" and "too-ordinary smartphone photo" trends — [note.com/petabyte_ai](https://note.com/petabyte_ai/n/n9c83d1c9296b?hl=en) (search summary).
- **Brazilian Portuguese (PT-BR):** free structured influencer prompts (face/hair/clothing/pose/setting/lighting/quality) for "influencers UGC feitas com IA" — [Nespol](https://nespol.com.br/blog/prompts-gratis-movimentos-realistas-em-influencers-ugc-feitas-com-ia/). Reference-photo → prompt conversion with grain and chromatic-aberration intensifiers, avoiding "pele cerosa" (waxy skin) — [iAWilker](https://prompt.iawilker.com/prompts/avatar-realista-ia-prompt/). General NB prompt roundups in Brazilian media — [Revista Fórum](https://revistaforum.com.br/tecnologia/10-prompts-para-nano-banana/) (all search summary).
- **German:** the 80/20 B-roll/avatar mix and "not overly polished" avatar guidance — [Laria.ai](https://www.laria.ai/en/blog/so-erstellst-du-hochwertige-ki-generierte-ugc-videos-mit-nano-banana-pro-und-veo-3.1) (video-oriented; the stills guidance is the relevant part).

### Inferences
- The most transferable non-English insight is the **Chinese "buyer-show vs seller-show" (买家秀 vs 卖家秀) framing**: write prompts as if the photo were taken by a customer rather than shot by the brand. It maps directly onto UGC ads.
- Japanese prompts lean toward polished "kawaii/editorial" portraiture more than raw UGC, so they suit brand-ambassador stills more than testimonial-style stills (inference from the sampled prompts).

### Gaps
- **Russian (реалистичный аватар нейросеть), Korean (AI 인플루언서 실사), French and Spanish-language (Spain/Argentina/Mexico/Colombia)** practitioner material could not be searched: the web-search budget was exhausted before those queries ran. No claims are made about those communities.
- Xiaohongshu, Douyin, Bilibili and paid-community (Discord/Skool/Hotmart) content was not accessible.

---

## 6. Common beginner mistakes vs pro habits

### Takeaway
Beginner mistakes that sources agree on: piling quality and beauty adjectives on top of each other ("8K, masterpiece, flawless"), using platform-style buzzwords ("ins style"), relying on a fixed seed for consistency, going to video before the face is locked, trusting generated label text, and accepting the model's default studio lighting. Pros fix the camera and light in a base prompt, change one variable at a time, use reference stacks, and run a deliberate skin and text pass.

### Cited Findings
- Quality-adjective stacking ("8K", "大师级画质") is counterproductive for realism — [Zhihu](https://zhuanlan.zhihu.com/p/2054517785917760150); generic "高清精美" loses to concrete photographic terms — [Peituka](https://peituka.com/blog/avoid-ai-look-realistic-images) (search summary).
- Platform-style keywords ("小红书风格、清新、ins风") cause over-beautification — [CSDN FLUX 小红书](https://agent.csdn.net/6a4e40df10ee7a33f289b58f.html) / [Peituka](https://peituka.com/blog/avoid-ai-look-realistic-images) (search summary).
- Seed-locking does not generalize to new poses, outfits or backgrounds — [Ryla.ai](https://ryla.ai/en/blog/ai-influencer-consistency/) (search summary).
- Jumping to video from one reference image causes face drift; lock the face first — [Higgsfield-related guide](https://thepostflow.com/ai/how-to-create-an-ai-influencer/) (search summary).
- Weak or uniform identity-training photos bake in the wrong face, age, makeup or style — [Higgsfield blog](https://higgsfield.ai/blog/how-to-create-ai-influencer) (search summary).
- Trusting in-image label text across a campaign is a mistake: overlay labels separately — [Fstoppers](https://fstoppers.com/artificial-intelligence/inserting-products-existing-photos-ai-what-actually-works-901419) (search summary).
- Using an aggressive upscaler on faces can change identity (Magnific "often changes the geometry of a face") — [Chase Jarvis 2026](https://chasejarvis.com/blog/best-ai-image-upscaler/) (search summary; single source).
- Pro habit: fixed base prompt (subject, lens, light) + micro-prompts + 5 parallel takes, then select — [adlibrary.com](https://adlibrary.com/guides/ai-prompting-guide-ugc-content-creators) (search summary).
- Pro habit: compare outputs with and without the style reference and check color grading and grain specifically — [Miko via YouMind](https://github.com/YouMind-OpenLab/awesome-gpt-image-2).

### Inferences
- "Too many sequential edits degrade the image" and "chat apps return compressed outputs" (both raised in the brief) are plausible, and match API-first workflows such as fal. **No source retrieved this session confirms them.** Treat them as hypotheses to test, for example by comparing the Gemini app download against API/Vertex output at the same prompt.

### Gaps
- No sourced data on output compression in the Gemini app, ChatGPT or Higgsfield web UI versus the API, and no data on quality loss per sequential edit.

---

## 7. Ad-platform reality and disclosure rules (compliance facts only)

### Takeaway
As of October 2026: (1) the **FTC Consumer Review & Testimonials Rule (16 CFR Part 465)** is being actively enforced: warning letters went out in December 2025, the TruHeight order came in July 2026, and commentators say AI-generated testimonials are covered. (2) **Meta** applies an "AI info" label and, from **1 June 2026**, auto-detects third-party AI content via industry signals. Strict mandatory disclosure applies to political and social-issue ads, while blog claims of a blanket rule for all ads conflict. (3) **TikTok** requires AIGC disclosure for realistic AI people in ads, and sources disagree on whether a July 2026 update made it universal. (4) **EU AI Act Article 50** deepfake-disclosure duties applied from **2 August 2026**. A December 2026 grace period applies only to machine-readable marking for systems already on the market. A final EU Code of Practice was published 10 June 2026.

### Cited Findings
- **FTC enforcement:** warning letters to 10 companies in December 2025. The FTC announced the TruHeight case on 13 April 2026, alleging thousands of employee-written five-star reviews. The 15 July 2026 order includes an injunction and a $4M judgment, partially suspended on payment of $750,000. A DOJ complaint against PHS is pending in N.D. Ill., where defendants moved to dismiss on 17 July 2026 arguing the example reviews predate the rule — [DLA Piper, July 2026](https://www.dlapiper.com/en/insights/publications/2026/07/ftcs-2026-enforcement-approach-to-fake-reviews-takes-shape-takeaways-for-companies) (search summary).
- **AI-generated testimonials:** commentary says fake reviews "include AI-generated ones". Under the "knew or should have known" standard, businesses are liable for AI- or vendor-produced fake reviews — [AuditSocials](https://www.auditsocials.com/blog/ftc-consumer-review-rule-2026-fake-reviews-testimonials-ai-social-proof); [Everything-PR](https://everything-pr.com/ftc-fake-reviews) (search summary; commentary, not the rule text). Civil penalties are cited **up to $53,088 per violation** — [Everything-PR](https://everything-pr.com/ftc-fake-review-rule). An older January 2026 source says "exceeding $50,000" — [RegulatoryOversight](https://www.regulatoryoversight.com/2026/01/ftc-warns-companies-over-deceptive-online-review-practices/).
- **Meta:** for political and social-issue ads, advertisers must disclose realistic AI image, video or audio showing a real person doing or saying something they didn't, **a realistic person who doesn't exist**, or altered real events. Undisclosed ads are rejected. For other ads, Meta's own gen-AI tools add an "AI info" label for significant edits or ads containing an AI-generated photorealistic human. **Since 1 June 2026** Meta detects third-party AI via industry-standard signals and shows the label under "About this ad", with no advertiser action required. — [Digital Applied 2026 reference](https://www.digitalapplied.com/blog/ai-content-labeling-rules-advertisers-2026-reference); [Oakgen](https://oakgen.ai/blog/ai-influencer-disclosure-rules-by-platform) (search summary). **Conflict:** other blogs claim a blanket label requirement on all AI-made ads, or claim there is no automated detection — [AdGenZ](https://www.adgenz.ai/blog/meta-ai-ad-disclosure-label-2026-guide); [TechJack](https://techjacksolutions.com/ai-brief/meta-now-requires-advertisers-to-disclose-ai-generated-conte/). One fact-check states that "the widely repeated claim that Meta mandates disclosure on all ads globally is not supported by the primary pages we reviewed" (search summary; exact page among the cited cluster not isolated).
- **TikTok:** ads with AI-generated or significantly AI-edited realistic content need TikTok's AIGC label or the advertiser's own caption, watermark or sticker. Photorealistic AI humans are a trigger; stylized visuals generally are not. Undisclosed content can be rejected or restricted. Commercial Content Disclosure is a separate toggle. On TikTok Shop, AI product images must be labeled identically in the ad and the listing — [Cinerads](https://www.cinerads.com/blog/tiktok-ai-content-policy); [UGCVids](https://ugcvids.ai/blog/tiktok-ai-content-disclosure-rules-2026); [AuditSocials](https://www.auditsocials.com/blog/tiktok-ai-content-disclosure-rules-2026) (search summary). **Conflict:** one source says that on 21 July 2026 TikTok made disclosure mandatory on *all* AI-generated ad content — [Common Thread Co.](https://commonthreadco.com/blogs/coachs-corner/tiktok-ai-ad-disclosure-rules-ecommerce-2026). Another cites the ad-disclaimer page last updated September 2025 as covering fully AI-generated or significantly modified non-Spark ads. TikTok has offered official AI avatars of creators and stock actors since 2024 — [TechCrunch 2024](https://techcrunch.com/2024/06/17/tiktok-ads-and-branded-content-will-now-include-ai-avatars-of-creators-and-stock-actors) (older).
- **EU AI Act Art. 50:** Art. 50(2), (4) and (5) became applicable on **2 August 2026** — [European Commission FAQ](https://digital-strategy.ec.europa.eu/en/faqs/signing-code-practice-transparency-ai-generated-content). Art. 50 was **not** deferred by the Digital Omnibus — [CSA research note, 29 Jul 2026](https://labs.cloudsecurityalliance.org/research/csa-research-note-eu-ai-act-article-50-transparency-20260729/). Generative systems on the market before 2 August 2026 have until **2 December 2026** for the Art. 50(2) marking and detection duty. Deployers publishing deepfakes must disclose — [Technology.org, 13 Oct 2026](https://www.technology.org/2026/10/13/eu-ai-act-deadlines-after-the-digital-omnibus-what-applies-from-december-2026-to-august-2028/). The final voluntary **Code of Practice on Transparency of AI-generated Content** was published 10 June 2026: Section 1 covers providers (marking and detection) and Section 2 covers deployers (labelling deepfakes). Signatures were encouraged until 27 July 2026 — [EC Code page](https://digital-strategy.ec.europa.eu/en/policies/code-practice-ai-generated-content). Non-binding Commission guidelines were issued on 20 July 2026 — [Saudi Audit Times](https://thesauditimes.net/en/labels-disclosures-and-deepfakes-inside-the-eu-ai-acts-article-50-rules-now-in-force/). Background reading: [artificialintelligenceact.eu Art. 50 guide](https://artificialintelligenceact.eu/transparency-rules-article-50/).

### Inferences
- For a legitimate company: **label every photorealistic synthetic person** on Meta and TikTok, keep C2PA/provenance metadata intact (Meta's June 2026 detection relies on industry signals, so stripping them would be both a policy risk and a credibility risk), never present a synthetic avatar as a real customer giving a review, and treat EU distribution as deepfake-disclosure-required since August 2026.
- 16 CFR 465.2 is widely described (from background knowledge, **not verified against ecfr.gov this session**) as prohibiting consumer reviews or testimonials that misrepresent that they come from a reviewer who does not exist. Synthetic "customer testimonial" stills paired with endorsement copy are therefore the highest-risk use case. Verify the exact rule text with counsel.

### Gaps
- Primary-source pages (ftc.gov, ecfr.gov, Meta Business Help Center, TikTok Ads policy) were blocked by the proxy. All platform details above are secondary and **conflict in places**; confirm them on the official pages before the SOP is finalized.
- No data on whether AI-avatar ads get *reach-limited* (as opposed to labeled) on Meta or TikTok in 2026.
- Health-claim and before/after rules for AI imagery were not researched.

---

## 8. Pricing, throughput and batch production

### Takeaway
Hard numbers on agency cost per final avatar still were **not found**. The only batch mechanics sourced are 4–5 parallel takes per base prompt, 3x3 contact sheets to get nine framings per generation, 20+ image Soul ID training sets, 15–30 image LoRA sets, and reusable JSON "look" templates. Human UGC creators are cited at $200–$800 per video as the cost being replaced (vendor claim).

### Cited Findings
- Generate **five parallel shots** per base prompt and keep the cleanest frame set — [adlibrary.com](https://adlibrary.com/guides/ai-prompting-guide-ugc-content-creators) (search summary).
- **3x3 contact sheet** in one NB Pro call (nine shot types listed in the JSON) — [@SheBuildsAI_, Sep 2026](https://x.com/SheBuildsAI_/status/2096191621838864712) via [YouMind](https://github.com/YouMind-OpenLab/awesome-nano-banana-pro-prompts).
- Identity assets: Soul ID needs **≥20 photos** (one source) — [Higgsfield blog](https://higgsfield.ai/blog/how-to-create-ai-influencer). LoRA needs **15–30 images** — [Ryla.ai](https://ryla.ai/en/blog/ai-influencer-consistency/) (search summaries).
- Reusable library approach: one saved character photo + one JSON look + the product image produces "variations without writing everything from scratch" — [Miko via YouMind](https://github.com/YouMind-OpenLab/awesome-gpt-image-2).
- Japanese and Chinese template prompts use `{argument name="..." default="..."}` variables (e.g., hair color, hat color, setting), effectively parameterized prompts for batch variation — [YouMind repos](https://github.com/YouMind-OpenLab/awesome-gpt-image-2).
- AI UGC is pitched as replacing human creators at **$200–$800 per video** — [VidAU](https://www.vidau.ai/awesome-nano-banana-pro-make-stunning-free-real-ai-ugc-ads/) (promotional; unverified).
- Prompt packs sell at $5–$66 on Gumroad — [promptergen](https://promptergen.gumroad.com/l/idxraf) (search summary).

### Inferences
- A defensible batch SOP from the sourced pieces: for each persona, build an identity pack (20+ curated stills) → a parameterized base prompt with `{variables}` for outfit, setting and product → contact sheet or 4–5 parallel takes per variant → human QA on identity match, hands, product/label text and the "AI tells" checklist (skin, symmetry, light, background cleanliness) → skin pass and upscale only for the winners. The QA rubric items come from the AI-tell lists in Sections 3 and 6. No source published a numeric QA scoring rubric.

### Gaps
- No sourced **cost per final image**, Nano Banana Pro or Higgsfield per-image pricing, agency day rates or throughput (images per operator-hour). Pricing pages for fal, Higgsfield, Enhancor and Magnific could not be fetched.
- No published QA scoring rubric or acceptance rate (e.g., "1 keeper in N") from any agency.
