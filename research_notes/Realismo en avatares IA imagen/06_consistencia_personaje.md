# Character / Identity Consistency for Synthetic AI Avatars (Still Images), state as of October 2026

> Method note for the report writer: WebFetch could not reach any page in this session (DNS failure; the official docs domains ai.google.dev, docs.bfl.ai and docs.midjourney.com were also refused by the egress proxy). All findings below come from search-engine result summaries of the cited pages (WebSearch, extended mode), not from reading full pages. Numbers attributed to official docs were relayed by the search tool, which quoted the page. When the search tool grouped a claim across several practitioner blogs without saying which one made it, I cite the group and mark it "(attribution across these guides)". The search budget ran out before I could cover the legal angle, Japanese/Korean/Russian sources, or ComfyUI QA nodes (see Gaps).

## 1. Reference-based methods (no training): which gives the best identity fidelity AND realism in 2026?

### Takeaway
For zero-training consistency, the October 2026 front-runners are Google Nano Banana Pro (Gemini 3 Pro Image: up to 14 refs, up to 5 people), OpenAI GPT Image 2 / 2.5 (up to 16 refs, always-high input fidelity), Seedream 4.5 / 5.0 Lite (2–14 refs), FLUX.2 [pro]/[max]/[flex] (8 refs via the API, 10 in the playground) and Qwen-Image-2.1 (10 refs, open weights). No independent benchmark ranks them on face identity. Practitioner tests disagree: some favor Nano Banana, some GPT Image 2, and some Seedream on keeping skin grain. Midjourney Omni Reference only works properly on V7 and is marked unsupported on V8.x, so it is the weakest choice for a reusable photoreal avatar.

### Cited Findings

**Google: Nano Banana Pro (Gemini 3 Pro Image) / Nano Banana 2 / Nano Banana 2.1**
- Gemini 3 Pro Image takes up to 14 reference images in total. The official table splits them into up to 5 for character consistency (people) and up to 6 for high-fidelity objects. — [Gemini API docs](https://ai.google.dev/gemini-api/docs/image-generation); [DeepMind model page](https://deepmind.google/models/gemini-image/pro/)
- Google's launch post: Nano Banana Pro "can blend more elements than ever before, using up to 14 images and maintaining the consistency and resemblance of up to 5 people." — [Google blog, Nano Banana Pro launch](https://blog.google/innovation-and-ai/products/nano-banana-pro/)
- Google's tips post says the input limit "varies by surface" (6 to 14 images depending on the app or API). — [Google blog, 7 tips for Nano Banana Pro](https://blog.google/products-and-platforms/products/gemini/prompting-tips-nano-banana-pro/)
- Conflict: a Google Cloud model listing describes consistency "up to 14 reference inputs" with no 5-person split. — [Google Cloud docs](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/google-models)
- A third-party guide says the 14 images are a shared pool for objects and characters, not two separate allotments. — [Apiyi guide to the 14-reference feature](https://help.apiyi.com/en/gemini-14-reference-images-object-fidelity-character-consistency-guide-en.html)
- Uploading N references does not guarantee N distinct, faithful people in the output. — [GlobalGPT](https://www.glbgpt.com/hub/can-gemini-3-pro-generate-multiple-images-at-once/)
- Nano Banana 2 (Gemini 3.1 Flash Image, February 2026): the launch post said "up to five characters and up to 14 objects". The current Gemini API docs list 4 characters and 10 objects for `gemini-3.1-flash-image`. — [Google blog, Nano Banana 2](https://blog.google/innovation-and-ai/technology/ai/nano-banana-2/); [Gemini API docs](https://ai.google.dev/gemini-api/docs/image-generation)
- Nano Banana 2.1 (`gemini-nano-banana-2.1`, built on Gemini 3.6 Flash) shipped on October 6, 2026. It takes up to 14 refs, tracks 4 characters and 10 objects, outputs up to 4K, and costs about $0.0336 per 1K image (about half of NB2's $0.067). Google claims better character consistency across conversation turns. Nano Banana 2 (`gemini-3.1-flash-image`) shuts down in the Gemini API on October 29, 2026. One review found Nano Banana Pro's images still look more realistic and natural than 2.1's. — [The Decoder](https://the-decoder.com/googles-new-image-model-nano-banana-2-1-generates-better-images-for-less-money/); [Forklog](https://forklog.com/en/google-launches-nano-banana-2-1-image-generation-model/); [FelloAI](https://felloai.com/nano-banana-2-1/) (attribution across these)
- Practitioner reports on Nano Banana identity drift: identity holds "reliably for 8–10 sequential edits", then slowly drifts. The fix is to re-upload the original reference every few prompts. — [UD.hk, Nano Banana Pro consistent characters (Jun 2026)](https://www.ud.hk/en/blogs/insight/article/2026-06-29-nano-banana-consistent-characters); [SelfieLab Studio](https://selfielabstudio.com/blog/nano-banana-pro-consistent-character-sheets-guide-20260216); [Sider](https://sider.ai/blog/ai-image/nano-banana-pro-cheat-sheet-for-character-consistency) (attribution across these guides)
- Third-party guides claim fidelity is highest with 6 or fewer references, even though 14 are accepted. — [CometAPI](https://www.cometapi.com/how-to-prompt-nano-banana-pro-for-best/); [nanobananapro.org](https://www.nanobananapro.org/blog/nano-banana-prompt-guide) (attribution uncertain)
- Counter-evidence: in one user's selfie test, Nano Banana's outputs "don't look like me", while GPT Image 2 kept the face. — [AI Blew My Mind Substack, NB2 vs GPT Image 2](https://aiblewmymind.substack.com/p/nano-banana-2-vs-gpt-images-2)

**OpenAI: GPT Image 1.5 / 2 / 2.5 (ChatGPT and API)**
- For `gpt-image-2`, leave out `input_fidelity`: image inputs are always processed at high fidelity. `gpt-image-1.5` accepts `input_fidelity` `low` or `high`. — [OpenAI image prompting guide](https://developers.openai.com/api/docs/guides/image-prompting)
- The 1.5 cookbook edit examples use `model="gpt-image-1.5", input_fidelity="high", quality="high"`. — [OpenAI cookbook, gpt-image-1.5 prompting guide](https://developers.openai.com/cookbook/examples/multimodal/image-gen-1.5-prompting_guide)
- OpenAI recommends gpt-image-2 for new builds and keeping 1.5 only "for existing validated workflows during migration". — [OpenAI cookbook, GPT Image models prompting guide](https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide)
- OpenAI guidance for edits: "State which facial features and proportions must remain unchanged." — [OpenAI image prompting guide](https://developers.openai.com/api/docs/guides/image-prompting)
- GPT Image 2 edits accept up to 16 reference images (PNG/WebP/JPG under 50MB each) according to API resellers' docs. Luma lists only 4. — [APIYI docs](https://docs.apiyi.com/en/api-capabilities/gpt-image-2/overview); [RouterBase docs](https://docs.routerbase.com/openai-gpt-image-2-api/edit); contradicted by [Luma guide](https://lumalabs.ai/learning-center/articles/gpt-image-2-complete-guide)
- A benchmark author saw the API return 200 OK with `image_tokens: 0` at 8 references, meaning the references were silently discarded. On re-test it was fixed, and 5–17 references now ingest correctly. — [Moe Lueker, GPT Image 2 benchmark on 12 faces](https://moelueker.com/blog/gpt-image-2-hairstyle-benchmark-what-it-gets-wrong)
- GPT-Image-2.5 ("ChatGPT Images 2.5") shipped on September 8, 2026, as two API models: Flare (default) and Sunburst (more precise across edits, slower). OpenAI claims "stronger reference-subject preservation" and "better consistency across repeated edits", up to 3840×2160 output and up to 16 refs per edit. Outputs carry C2PA metadata (one source also says SynthID; that claim is unverified and odd for OpenAI). — [Unite.AI](https://www.unite.ai/openai-releases-chatgpt-images-2-5-with-sketch-and-two-new-api-models/); [OpenAI Developer Community announcement](https://community.openai.com/t/introducing-gpt-images-2-5-in-the-api-and-chatgpt/1395897); [Morphic spec sheet](https://morphic.com/resources/models/gpt-image-2-5); [DataCamp](https://www.datacamp.com/blog/chatgpt-images-2-5)
- One analysis says GPT-Image-2.5's real gains are in editing ("precise local edits and consistency across multiple turns"), not raw text-to-image quality. — [Kie.ai](https://kie.ai/blog/gpt-image-2-5-release-signals-openai-image-model)

**ByteDance: Seedream 4.0 / 4.5 / 5.0**
- Official BytePlus ModelArk doc: Seedream 5.0 Lite, 4.5 and 4.0 take 2–14 reference images, with input plus output capped at 15 images. `sequential_image_generation: auto` produces a batch of related images. `disabled` produces one image from 2–14 refs. Seedream 5.0 Pro and Flash take only 2–10 refs and do not support sequential generation. — [BytePlus ModelArk image generation API](https://docs.byteplus.com/en/docs/ModelArk/1541523)
- An older BytePlus page lists 2–10 refs for seedream-4.0. — [BytePlus seedream-4.0 page](https://docs.byteplus.com/en/docs/ModelArk/1824718)
- The Seedream 4.0 technical report confirms reference-based editing with more than 10 input images. — [arXiv 2509.20427](https://arxiv.org/pdf/2509.20427)
- Migration guide: going to 5.0 Pro means cutting the reference array from 14 to 10. — [Atlas Cloud](https://www.atlascloud.ai/blog/tips/seedream-4.5-to-5.0-pro-upgrade)
- In a face-restoration comparison, Seedream 5 Pro stayed closest to the original face and kept the photographic grain, while Nano Banana Pro altered the face. — [Rangy, Seedream 5 Pro vs Nano Banana Pro vs GPT Image 2](https://rangy.ai/blog/seedream-5-pro-vs-nano-banana-pro-vs-gpt-image-2/); [CreateVision](https://createvision.ai/guides/seedream-5-vs-nano-banana-2-vs-gpt-image-2) (attribution across these)

**Black Forest Labs: FLUX.2 / FLUX Kontext**
- Official per-model limits: FLUX.2 [max], [pro] and [flex] take up to 8 references via the API and 10 in the playground. [klein] takes up to 4. [dev] is recommended at a maximum of 6. — [BFL FLUX.2 API docs](https://docs.bfl.ai/flux_2); [BFL release notes](https://docs.bfl.ml/release-notes)
- The [pro] API caps input plus output at 9MP in total, so references shrink as resolution grows: 8 refs at 1MP output, 7 at 2MP. BFL recommends stating each image's role in the prompt (for example, subject from image 1, style from image 2). — [BFL FLUX.2 prompting guide](https://docs.bfl.ai/guides/prompting_guide_flux2)
- BFL marketing advertises 10 references and "the best character consistency available today". — [BFL FLUX.2 blog](https://bfl.ai/blog/flux-2)
- One comparison says FLUX.2 reference consistency is weaker and that strong identity comes "only via fine-tuning/LoRA workflows". — [Atlas Cloud, best AI image editing models 2026](https://www.atlascloud.ai/blog/guides/best-ai-image-editing-models-2026); [Morphed](https://morphed.app/blog/flux-2-vs-nano-banana-pro) (attribution across these)
- FLUX Kontext editing docs still exist under the legacy docs domain. — [BFL Kontext image editing](https://docs.bfl.ml/kontext/kontext_image_editing)

**Midjourney: Omni Reference (V7) and V8**
- Omni Reference (`--oref <url>`, weight `--ow`) was announced for V7 in May 2025. `--ow` runs 0–1000 (default 100). Low values such as `--ow 25` are for style changes (photo to anime). — [Midjourney updates, Omni-Reference](https://updates.midjourney.com/omni-reference-oref/)
- Midjourney advises generally staying below `--ow` 400. — [Flowith](https://flowith.io/blog/midjourney-v7-consistent-characters-masterclass/); one guide says weights above about 400 become unpredictable — [UD.hk, Midjourney consistency (Aug 2026)](https://www.ud.hk/en/blogs/insight/article/midjourney-consistent-look-2026-08-07)
- Omni Reference costs 2× regular V7 GPU time. It is marked unsupported on V8, and the docs point V8 users to the Edit model instead. — [Blake Crosley, Midjourney 8.2 guide](https://blakecrosley.com/guides/midjourney)
- Midjourney's compatibility chart shows Character Reference (`--cref`) and `--cw` as unsupported on V8.1 and V8.2. — [ClipDance](https://clipdance.ai/blog/midjourney-v8-character-consistency)
- `--oref` on V8.1 and V8.2 silently reruns the job in V7. — [Prompt Architects](https://prompt-architects.com/blog/92-midjourney-character-consistency-cref-oref)
- A common pattern is pairing `--oref` (identity) with `--sref` (style) for sequences. Style Reference remains supported on V8. — [UD.hk](https://www.ud.hk/en/blogs/insight/article/midjourney-consistent-look-2026-08-07); [ClipDance](https://clipdance.ai/blog/midjourney-v8-character-consistency)

**Alibaba: Qwen-Image-Edit-2509 / 2511 / Qwen-Image-2.1**
- Qwen-Image-Edit-2511 takes 1–3 reference images plus an instruction. It targets image drift, character consistency, and fusing several people into one group photo. — [Chutes docs, Qwen-Image-Edit-2511](https://chutes.ai/docs/models/vonkaiser-qwen-image-edit-2511); [ComfyUI docs, Qwen-Image-Edit-2511](https://docs.comfy.org/tutorials/image/qwen/qwen-image-edit-2511)
- 2509 mainly helped single subjects, and 2511 extends identity preservation to multi-person group photos. — [Vast.ai model page](https://vast.ai/model/qwen-image-edit)
- Research caveat: baseline Qwen-Image-Edit 2509/2511 "spuriously inflate" reference-consistency scores by copying the reference scene. — [arXiv 2607.29025](https://arxiv.org/pdf/2607.29025)
- Qwen-Image-2.1 (September 20, 2026): "supports up to 10 reference images". It is a 7B unified generation, editing and multi-reference model with native RGBA and 2K output. Demos include merging 6 portraits into a group photo. There is no independent benchmark of character accuracy. — [Qwen on X](https://x.com/Alibaba_Qwen/status/2101659314180280769); [qwenimages.com](https://qwenimages.com/blog/qwen-image-2-1-release); [Yage.ai analysis](https://yage.ai/share/qwen-image-21-two-track-strategy-en-20260924.html); [MindStudio review](https://www.mindstudio.ai/blog/qwen-image-2-1-hands-on-review)

**Higgsfield Soul ID / Soul 2.0** (a light hosted training step rather than pure references)
- Official help center: train once on 20 or more photos of one person (up to 80). Training takes about 3 minutes, and generations are then unlimited. — [Higgsfield help center](https://higgsfield.ai/creator-hub/help-center/ai-models/how-do-i-create-and-use-a-soul-id-character)
- July 2025 launch: "Upload 20-25 pics… drop it into any of 60+ fashion-grade presets." — [Higgsfield on X](https://x.com/higgsfield_ai/status/1942985561125589120); an early review reported 10 photos (up to 70) — [302.AI on Medium](https://medium.com/@302.AI/higgsfield-soul-id-test-how-realistic-is-the-character-consistency-1bc8b3250bca)
- Soul 2.0 is Higgsfield's current "high aesthetic" photo model. — [Higgsfield Soul 2.0](https://higgsfield.ai/soul-intro)
- Guides: a smaller set of clean, varied photos beats a larger inconsistent one. Use consistent lighting and include at least one full-height shot. Extreme style shifts or unusual angles still cause small drift. — [Media.io](https://www.media.io/video-tips/soul-id-character-consistency.html); [CropUp AI](https://cropupai.com/blog/higgsfield-ai-prompting-guide/); [Digital Zoom Studio](https://digitalzoomstudio.net/2026/03/train-a-consistent-character-in-higgsfield-soul/) (attribution across these)

**Runway, Ideogram, Krea**
- Runway Gen-4 References takes up to 3 reference images per generation and is available on all paid plans. A neutral-background reference with clear facial features anchors identity most reliably, and references do not guarantee zero drift. — [VentureBeat](https://venturebeat.com/ai/runways-gen-4-ai-solves-the-character-consistency-challenge-making-ai-filmmaking-actually-useful); [Geeky Gadgets](https://www.geeky-gadgets.com/runway-gen-4-references/); [SelfieLab Runway guide](https://selfielabstudio.com/blog/runway-gen-4-consistent-characters-guide-2026-20260310)
- Ideogram Character works from a single reference. It detects face and hair and builds an "identity map", while scene, lighting and pose follow the prompt. An editable mask (face and hair by default) can be widened to keep clothing. Modes are Auto, Fiction and Realistic, with Turbo, Default and Quality speeds. — [Cliprise guide](https://www.cliprise.app/learn/guides/model-guides/ideogram-character-complete-guide); [WaveSpeedAI](https://wavespeed.ai/blog/posts/introducing-ideogram-character-on-wavespeedai/); [The Rundown](https://www.therundown.ai/tools/character)
- Krea hosts Nano Banana among its models (one creator workflow runs Nano Banana through Krea.ai from a Midjourney base image). — [Ciguleva Substack](https://ciguleva.substack.com/p/step-by-step-guide-consistent-characters). Krea's own open model, Krea 2, is covered in section 3 (LoRA).

**Cross-model comparisons**
- No standardized face-identity benchmark ranks NB Pro, GPT Image 2, Seedream and FLUX.2. Blog tests disagree. — [Atlas Cloud](https://www.atlascloud.ai/blog/guides/best-ai-image-editing-models-2026); [Rangy](https://rangy.ai/blog/seedream-5-pro-vs-nano-banana-pro-vs-gpt-image-2/); [CreateVision](https://createvision.ai/guides/seedream-5-vs-nano-banana-2-vs-gpt-image-2); [GenImagePro](https://genimagepro.com/blog/best-ai-model-face-consistency)
- Segmind argued that zero-shot (Nano Banana) makes character LoRAs obsolete "for most needs". Its own table shows 95–98% consistency for zero-shot versus 87–96% for LoRA. These are the author's numbers, and the post predates Nano Banana Pro. — [Segmind blog](https://blog.segmind.com/lora-training-for-consistent-character-is-dead-2/)
- A Chinese Krea 2 tutorial makes the opposite case: "reference image techniques can transfer style but cannot lock facial identity; LoRA training can." — [Bilibili, LoRA vs reference images on Krea 2 Turbo](https://www.bilibili.com/video/BV11cTo6WEfM/)

### Inferences
- For a fictional avatar used in ads, the most robust zero-training path is Nano Banana Pro, with at most 5 people-type references in the 14 slots (in practice 3–6 views of the same synthetic person) plus object refs for products. Its 5-person limit, its realism (still rated above NB 2.1 by one reviewer) and Google's own statements make it the default "master" engine. GPT Image 2/2.5 is the strongest second engine, especially for editing an existing shot. Seedream 4.5/5.0 Lite is worth A/B-testing when skin grain matters.
- Model churn is extreme: NB2 retires on October 29, 2026, gpt-image-1.5 is legacy, and Midjourney V8 dropped `--oref`. An SOP should therefore anchor on the reference pack (the images plus the identity descriptor), not on any one model, and re-validate each new model with the face-similarity QA in section 5.
- Midjourney is unsuitable as the main engine for a reusable photoreal avatar in late 2026. Its identity tools work only on V7 and cost 2× GPU, and it has no API-style multi-reference control.
- FLUX.2 multi-reference has the best documented controls (explicit per-image roles, open [dev] and [klein] weights). Its identity strength is debated, so pair it with a LoRA (section 3) for production work.
- FLUX Kontext (2025) is effectively superseded by FLUX.2's built-in multi-reference editing. That is my inference from BFL's FLUX.2 docs absorbing editing; I found no explicit deprecation notice.

### Gaps
- I could not read the live official tables (Gemini docs, BFL docs, Midjourney docs) directly. All figures were relayed by search summaries.
- I found no reliable official number for how many of GPT Image 2/2.5's 16 refs can be people, and no official OpenAI page for the 16-image limit (only resellers' docs).
- I found no independent, standardized identity-plus-realism benchmark across NB Pro, NB 2.1, GPT Image 2.5, Seedream 5, FLUX.2 and Qwen-Image-2.1. The vendor-blog percentages ("93%", "95–98%") are unverified.
- I found no official Ideogram or Runway documentation (third-party only), no Krea "characters" feature specifics beyond Krea 2 LoRAs, and nothing on whether Higgsfield Soul ID behaves differently with synthetic training photos.

## 2. Character sheets / "identity anchors": building the master reference sheet and the written identity descriptor

### Takeaway
Practitioners converge on one master front-facing, evenly lit, neutral-expression portrait, expanded into a turnaround (front, 3/4, profile, and optionally back and full body) on a plain neutral-grey background. A short fixed written descriptor of the defining traits, worded identically in every prompt, sits alongside it. Reference images carry far more weight than text.

### Cited Findings
- The master reference should be a front-facing, well-lit, neutral-expression portrait. The reference image carries far more weight than text description. "Consistency is not achieved by longer prompts. It's achieved by how you use reference images." — [UD.hk](https://www.ud.hk/en/blogs/insight/article/2026-06-29-nano-banana-consistent-characters); [Techyheaven](https://techyheaven.com/nano-banana-pro-character-consistency/); [Nanobanana.fans](https://www.nanobanana.fans/tutorials/character-consistency) (attribution across these guides)
- Generate 2–3 angle reference sheets (front, 3/4, back plus expressions on a clean background) first, then use the sheet as the reference for later shots. — [SelfieLab Studio, NB Pro character sheets (Feb 2026)](https://selfielabstudio.com/blog/nano-banana-pro-consistent-character-sheets-guide-20260216); [Apiyi storyboard guide](https://help.apiyi.com/en/nano-banana-pro-ai-video-storyboard-character-consistency-guide-en.html) (attribution across these)
- A sheet should include "aligned front, three-quarter and profile views of one character, all under the same even, neutral light". Minimum set: front, left profile, back and three-quarter, "in the same neutral stance and scale". Use a "plain neutral grey" background, because a busy one gets read as part of the character. — [Quest Studio](https://queststudio.io/blog/ai-character-turnaround-sheet); [Apatero turnaround guide 2026](https://apatero.com/blog/ai-character-turnaround-sheet-generation-guide-2026); [Elser.ai](https://www.elser.ai/blog/ai-character-turnaround-prompts-front-side-back-views) (attribution across these)
- Identity descriptor: "Add a short plain-language description of the defining traits, such as hair, build, wardrobe and one memorable marker like a scar." Use "one or two describable markers… named the same way in every prompt." Close with "Keep the same face, hair, proportions, outfit, colors, and rendering style in every view." — [Quest Studio](https://queststudio.io/blog/ai-character-turnaround-sheet); [FXI Studio](https://www.fxi.studio/tutorials/how-to-make-character-sheet-with-ai); [MarketPrompter](https://marketprompter.com/blog/ai-character-prompts) (attribution across these)
- Repeat the 3–4 most distinctive features in every prompt (such as hair, eye color and a distinctive mark). Keep face, hair, clothing and style text fixed and vary only one thing (camera angle, framing or scene). — [UD.hk](https://www.ud.hk/en/blogs/insight/article/2026-06-29-nano-banana-consistent-characters); [Nenobanana 2026 guide](https://www.nenobanana.com/blogs/nano-banana-character-consistency-12-prompts-that-actually-work--2026-guide) (attribution across these)
- The most common mistake is stacking conflicting style cues in one prompt. — [Apiyi, NB Pro face consistency guide](https://help.apiyi.com/en/nano-banana-pro-face-consistency-guide-en.html); [UD.hk](https://www.ud.hk/en/blogs/insight/article/2026-06-29-nano-banana-consistent-characters) (attribution across these)
- For subject consistency, clear, well-lit headshots work best as references. — [Phil Schmid, Nano Banana 2 developer guide](https://www.philschmid.de/nano-banana-2-interactions-api); [Apidog](https://apidog.com/blog/nano-banana-2/) (attribution across these)
- The open "Kontext turnaround sheet" LoRA warns it won't work well on real human photos and wants a full-body input, so photoreal turnarounds may need a different workflow. — [Hugging Face, kontext-turnaround-sheet-lora-v1](https://huggingface.co/reverentelusarca/kontext-turnaround-sheet-lora-v1)
- Character sheets ("model sheets") and stacking references are named as what keeps an AI-influencer character stable. — [Chetan Pujari Substack, AI influencer with Nano Banana](https://chetanpujari.substack.com/p/how-i-created-an-ai-influencer-using)
- Brazilian practitioners start from a neutral "anchor image" (imagem âncora), generated with Seedream or Nano Banana, before any LoRA work. — [Human Academy (PT)](https://www.humanacademy.ai/en/blog/personagem-consistente-ia)
- Chinese practitioner guidance for realistic-person datasets: multiple angles, expressions and lighting at a uniform resolution, with roughly ≥768×768 for face close-ups and about 1024 px for full body. — [Zhihu](https://zhuanlan.zhihu.com/p/1919777826883757486); [FlowPix](https://www.flowpixai.com/ai-art/ai-lora-training-guide.html); [Tahou](https://www.tahou.com/article/203508355810250757) (attribution across these)

### Inferences
- A practical "identity pack" for a synthetic avatar (synthesized from the above, not taken from a single source):
  1. A hero portrait (front, neutral expression, flat soft light, grey background, 2K+).
  2. Front, 3/4 left, 3/4 right and profile headshots under identical light.
  3. A full-body neutral stance.
  4. A macro skin close-up showing pores and the freckle or mole map.
  5. Two or three expressions (smile with teeth, neutral, talking).
  This fits Nano Banana Pro's 5-person slot budget and FLUX.2 [pro]'s 8-ref budget.
- The written descriptor block should be short and identical each time, naming at most 3–4 hard identity markers (eye color, mole position, hairline or brow shape, a scar). Clothing and lighting stay out of the descriptor and go in the per-shot "scene" block, so they are not baked into identity.
- Even, neutral light on the reference sheet matters doubly. It keeps lighting from being treated as identity both by reference-based models and by any LoRA later trained on these images (see section 3).

### Gaps
- I found no official Google, OpenAI or BFL document prescribing an exact turnaround set or a formal "identity descriptor" format. These are practitioner conventions.
- I found no controlled test of whether a skin-texture macro reference improves realism in reference-based models.

## 3. Training-based methods: LoRA for a synthetic person (FLUX.1/FLUX.2, Qwen-Image, Z-Image, Wan 2.x, Krea 2, SDXL legacy)

### Takeaway
LoRA remains the strongest way to hard-lock a face across hundreds of images. It is typically trained on a synthetically generated dataset of about 15–80 consistent images (often made with Nano Banana).
- **Typical settings:** rank 16–32, LR around 1e-4 (8e-5 to 2e-4), batch size 1, and about 1,000–3,000 steps, with intermediate checkpoints saved.
- **Main realism risks:** attributes that are uniform across the dataset (lighting, hair, outfit) get baked into identity, and distillation/turbo LoRAs give plastic skin.
- **Licensing:** commercial use matters. FLUX.2 [klein] 4B is Apache 2.0, while 9B and FLUX.1 dev are non-commercial.

### Cited Findings

**FLUX.2 ([dev], [klein])**
- BFL's [klein] training guide: about 1,500–3,000 steps for character LoRAs at LR 8e-5 to 1e-4 (higher rates for characters, lower for style), watching sample outputs for overfitting. 9B training needs 22GB VRAM. — [BFL FLUX.2 [klein] training](https://docs.bfl.ml/flux_2/flux2_klein_training)
- License: FLUX.2 [klein] 9B weights are non-commercial, while 4B is Apache 2.0. — [BFL klein training docs](https://docs.bfl.ml/flux_2/flux2_klein_training); [fal klein 9B trainer](https://fal.ai/models/fal-ai/flux-2-klein-9b-base-trainer) (attribution across these)
- fal's klein 9B base trainer costs $0.0086/step (about $8.60 for 1,000 steps). The edit-trainer pricing also scales with the reference count. fal launched trainers for both klein 4B and 9B. — [fal klein 9B base trainer](https://fal.ai/models/fal-ai/flux-2-klein-9b-base-trainer); [fal on X](https://x.com/fal/status/2013313891057455265)
- fal: a FLUX.2 LoRA needs "20 to 1,000 images" of the same subject or identity. — [fal blog, Training FLUX.2 LoRAs](https://blog.fal.ai/training-flux-2-loras)
- FLUX.2 [dev] on AI Toolkit: rank 32 is a good default for character LoRAs when VRAM allows, or rank 8–16 with fewer steps if VRAM is tight. Use 20–60+ images and 1,000–3,000 steps at LR 1e-4, at 1024×1024. — [RunComfy, FLUX.2 dev LoRA with AI Toolkit](https://www.runcomfy.com/trainer/ai-toolkit/flux-2-dev-lora-training)
- A 4B klein LoRA tutorial frames training on 50–100 images. — [HackerNoon](https://hackernoon.com/make-flux2-yours-train-a-4b-lora-on-50-100-images)
- ai-toolkit is described as the default trainer recommendation for klein models (secondary blog). — [WorkingNotWorking FLUX.2 LoRA guide 2026](https://workingnotworking.com/flux-2-lora-training-guide/)

**Z-Image Turbo (Tongyi-MAI)**
- In AI Toolkit, choose "Z-Image Turbo (w/ Training Adapter)". The RunComfy preset uses adapter v2, rank 32, LR 0.0001 and batch size 1. — [RunComfy Z-Image Turbo LoRA](https://www.runcomfy.com/trainer/ai-toolkit/z-image-turbo-lora-training)
- Common guidance:
  - Rank 8–16 (16 for complex characters).
  - About 2,500–3,000 steps for 10–30 images, or 1,500–2,200 for fewer than 10. Another guide suggests about 3,000 for 5–15 images.
  - LR 1e-4, dropping to about 5e-5 if samples look noisy or overcooked.
  - Batch size 1, since larger batches destabilize identity on small datasets.

  Sources: [HF blog, Z-Image Turbo LoRA engineering notes](https://huggingface.co/blog/content-and-code/training-a-lora-for-z-image-turbo); [KawaiiPromptLab](https://kawaiipromptlab.com/en/tutorials/lora-training-guide/); [NeuroCanvas](https://neurocanvas.net/blog/zimage-lora-training-guide/) (attribution across these)
- A less authoritative post claims realistic skin texture needs 70–80 photos, 4,000 steps and linear rank 64. — [DEV Community](https://dev.to/czmilo/z-image-turbo-complete-guide-2025-fast-ai-image-generation-lora-training-1013)
- Z-Image captioning: caption the subject's pose and clothing, not their physical appearance. — [DEV Community, Z-Image LoRA best practices 2026](https://dev.to/gary_yan_86eb77d35e0070f5/best-practices-for-training-lora-models-with-z-image-complete-2026-guide-4p7h)
- General AI Toolkit character guidance: 15–40 clean images, rank 8–16, LR 5e-5 to 1e-4. "When results look overcooked… the better fix is reducing learning rate or steps first", not adding images. — [A2A-MCP, Ostris AI Toolkit guide](https://a2a-mcp.org/blog/ostris-ai-toolkit)

**Qwen-Image (2512 / 2.1)**
- For people: 20–30 images minimum, with diminishing returns past about 50. Vary angles, expressions and lighting, since a single-angle set gives a LoRA that only works from that angle. Musubi-tuner is the most stable trainer for Qwen-2512. Resolution matching is critical for face accuracy. — [Apatero, Qwen-Image-2512 character LoRA](https://apatero.com/blog/qwen-image-2512-character-lora-training-real-people-guide-2025)
- A hands-on Qwen Image 2.1 run in ai-toolkit on 12GB VRAM used rank 16, alpha 16, LR 1e-4, batch 1 and 2,000 steps on 31 images at 1024 (stated as a baseline). Musubi-tuner and sd-scripts did not yet support 2.1 as of September 21, 2026. — [note.com, かみもと (JP)](https://note.com/sepiablue/n/n9372886b9e5d?hl=en)
- "When you are training a person or a subject, go with batch size 1, it is the best quality." — [Furkan Gözükara, Qwen training tutorial](https://github.com/FurkanGozukara/Stable-Diffusion/discussions/344)
- The FlyMyAI Qwen trainer needs no trigger word. — [FlyMyAI LoRA trainer](https://github.com/FlyMyAI/flymyai-lora-trainer). Hosted trainers: [fal Qwen-Image-2512 trainer](https://fal.ai/models/fal-ai/qwen-image-2512-trainer/playground); [Replicate qwen-image-lora-trainer (legacy)](https://replicate.com/qwen/qwen-image-lora-trainer-legacy/readme)
- Community realism LoRAs exist for Qwen-Image-2.1 edit. — [Hugging Face, realism-qwen-image-2.1-edit-lora](https://huggingface.co/houseofboern/realism-qwen-image-2.1-edit-lora)

**Krea 2 (open weights, June 2026)**
- Krea 2 is a 12.9B open-weights model, released June 22/23, 2026 (sources differ). It ships as "RAW" (undistilled, for training) and "Turbo" (8-step, for inference). Krea recommends training on Raw and running on Turbo, and offers hosted LoRA training (beta) for Max and Business plans. — [Krea 2 open-source page](https://www.krea.ai/krea-2-open-source); [Krea blog, Krea 2 LoRA training](https://www.krea.ai/blog/krea-2-lora-training); [AlphaSignal](https://alphasignal.ai/news/krea-opens-krea-2-s-12b-image-model-so-anyone-can-train-and-deploy)
- License: the "Krea 2 Community License" reportedly has a revenue cap; I could not confirm the terms. — [DreamPixelForge](https://www.dreampixelforge.com/blog/krea-2); [Bymar blog](https://blog.bymar.co/posts/krea-2-open-weights-image-model/)
- A full ai-toolkit character config:
  - Rank and alpha 32, adamw8bit, FlowMatch, bf16.
  - LR 2e-4, 2,000 steps, at resolutions 512 and 1024.
  - Dataset of 40–80 images; past 100, the extra images mostly repeat.
  - Captioning: the face transfers on its own, but "the body drifts back to the base model's prior unless the text insists", and named attributes get pulled away from the trigger.

  Source: [rkrra, Krea 2 character LoRA guide](https://rkrra.com/guides/krea-2-lora-training/)
- Alternative configs:
  - RunComfy: rank 32, 2,500 steps, LR 1e-4, at 512/768/1024; keep intermediate checkpoints. — [RunComfy, Krea 2 LoRA](https://www.runcomfy.com/trainer/ai-toolkit/krea-2-lora-training)
  - Earngenix: usable results at 1,000–2,000 steps; disable EMA. — [Earngenix](https://www.earngenix.com/tutorials/train-krea-2-lora-ai-toolkit)
  - A community trainer: rank 16, LR 1e-4; likeness typically lands by step 600–900. — [GitHub, krea2-character-lora-trainer](https://github.com/bongobongo2020/krea2-character-lora-trainer)
  - Community defaults: 15–30 sharp photos, a trigger phrase, at least 1,000 steps at 768/1024. — [Imagera](https://imagera.ai/blog/krea-2-lora-training)
- Chinese tutorials push Krea 2 LoRAs specifically for face lock across scenes (rain, snow). — [Bilibili](https://www.bilibili.com/video/BV11cTo6WEfM/); [YouTube (CN)](https://www.youtube.com/watch?v=A32qmJNbl4Q)

**Wan 2.2 (image-mode LoRA)**
- Dataset: at least 10, ideally 15+, high-resolution varied images. "Below 15, the LoRA cannot distinguish between 'features of the person' and 'features of a single photo'." — [Wan27.org guide 2026](https://wan27.org/blog/wan-2-2-lora-training-guide); [The Local Lab](https://www.locallabdigest.com/blog/wan-22-lora-consistent-characters); [SelfieLab Studio](https://selfielabstudio.com/blog/wan-22-lora-training-custom-characters-guide-20260317) (attribution across these)
- Steps conflict: one AI Toolkit tutorial uses 3,000–5,000 steps at LR 2e-4, another guide 800–1,200 steps over 1–2 epochs. Rank is 16–32. In AI Toolkit, set Num Frames to 1 for image datasets. — [YouTube, Ultimate Wan 2.2 LoRA training](https://www.youtube.com/watch?v=bhBZHPvX7gI); [StableDiffusionTutorials](https://www.stablediffusiontutorials.com/2025/10/wan2.2-lora-training.html); [Wan27.org](https://wan27.org/blog/wan-2-2-lora-training-guide) (attribution across these)
- "Trigger-only" training (one trigger word, no per-image captions) worked for one hands-on account. One Wan 2.2 14B expert in bf16 is 28GB, so with the optimizer it won't fit in 32GB; plan on quantization or cloud GPUs. — [ai-muninn, Wan 2.2 character LoRA on RTX 5090](https://ai-muninn.com/en/blog/train-character-lora-wan22-rtx5090). Hosted: [fal wan-22-image-trainer](https://fal.ai/models/fal-ai/wan-22-image-trainer)

**Realism risks (all model families)**
- Plastic skin: the speed-up distillation ("lightning") LoRA trades texture for speed, so output goes "plastic and CG-like". The fix is to drop lightning and run full steps (20 steps, CFG 5). — [ai-muninn, character-LoRA control panel (Wan 2.2)](https://ai-muninn.com/en/blog/character-lora-control-panel-wan22)
- Baked-in attributes: with trigger-only training, whatever is identical in every image becomes identity. In one example, silver hair in all 28 images "became part of the character", and changing it later fights the LoRA. A varied dataset fixes this for free: "if clothes, rooms, and light vary, the person is the only constant." — [ai-muninn control panel](https://ai-muninn.com/en/blog/character-lora-control-panel-wan22)
- Captioning philosophy is not settled:
  - A Hugging Face captioner says to avoid introducing variation in features that should stay constant (for example, skip skin tone unless it varies). — [HF LoRACaptioner system prompt](https://huggingface.co/spaces/rdesai2/LoRACaptioner/blob/713c829a80e7f795112b3f42b3e1f91b34badfde/system_prompt.txt)
  - The Krea 2 guide says to describe the body. — [rkrra](https://rkrra.com/guides/krea-2-lora-training/)
  - The Z-Image guide says to caption pose and clothing only. — [DEV Community](https://dev.to/gary_yan_86eb77d35e0070f5/best-practices-for-training-lora-models-with-z-image-complete-2026-guide-4p7h)
- A lower-trained LoRA "will be more flexible, but may get details wrong" (the overfit vs. flexibility trade-off). — [Hugging Face, Trauter LoRAs README](https://huggingface.co/YoungMasterFromSect/Trauter_LoRAs/blob/fe9664a5f3177883c2b7e52ed0d7ffbe13796a98/README.md?code=true)
- Chinese practitioner tip: before training, manually drop the roughly 20% of images that look least like the target. Captions should describe clothing, background and lighting so the face is the only invariant. — [FlowPix](https://www.flowpixai.com/ai-art/ai-lora-training-guide.html); [Tahou](https://www.tahou.com/article/203508355810250757); [WayToAGI](https://www.waytoagi.com/question/51860) (attribution across these)

**Synthetic dataset generation (references → 20–40+ images → LoRA)**
- LoRA-Dataset-Forge: "Two photos in. Trainer-ready LoRA dataset out." Face plus body references become hundreds of identity-locked, captioned, aspect-bucketed images via Nano Banana 2 (`gemini-3.1-flash-image-preview`). It includes review, Gemini-judge face validation and export for Qwen-Image training. — [GitHub, LoRA-Dataset-Forge](https://github.com/IxMxAMAR/LoRA-Dataset-Forge)
- NanoBananaLoraDatasetGenerator: browser-based, uses FAL.ai and Nano Banana Pro. Its "Reference Image" mode generates variations of an uploaded character and exports a ZIP with a trigger word and vision captions, targeting Flux 2, Z-Image and Qwen Image Edit. — [GitHub, NanoBananaLoraDatasetGenerator](https://github.com/lovisdotio/NanoBananaLoraDatasetGenerator)
- A research paper also used Nano Banana 2 seed images as proxy data for LoRA adaptation. — [arXiv 2607.16351](https://arxiv.org/pdf/2607.16351)
- Unreliable claim to flag: a blog says Nano Banana Pro "is built on Flux 2.0's architecture" and is compatible with Flux LoRAs. This contradicts its status as a Google Gemini model. — [Atlabs](https://www.atlabs.ai/blog/flux-2-0-vs-nano-banana-pro-a-comprehensive-comparison-of-leading-ai-image-generation-models)

**Legacy (flag as outdated in late 2026)**
- FLUX.1 [dev] identity tools (PuLID-Flux and others) inherit FLUX.1 dev's non-commercial terms. — [AIOFM, PuLID vs InstantID vs FaceID (2026)](https://aiofm.info/en/guides/pulid-vs-instantid-vs-faceid)
- InstantID is SDXL-only. — [AIOFM](https://aiofm.info/en/guides/pulid-vs-instantid-vs-faceid)

### Inferences
- **Recommended LoRA recipe** (synthesized from the sources; not one vendor's spec):
  - **Dataset:** generate 40–60 candidates from the identity pack with NB Pro or GPT Image 2.5, then cull to 25–40 that pass face-similarity QA (section 5).
  - **Variety:** vary outfit, location, lighting and focal length in every image, so only the face stays constant.
  - **Captions:** a unique trigger plus captions of the scene, clothing and lighting. Leave out face and eye descriptors.
  - **Training:** rank 16–32, LR 1e-4, batch 1, 1,500–3,000 steps, with checkpoints every 250 steps.
  - **Selection:** pick the earliest checkpoint that passes the identity threshold, to keep flexibility and skin realism.
- **Base model choice for commercial ads:**
  - FLUX.2 [klein] 4B (Apache 2.0), Qwen-Image (Apache-style open weights; I did not verify the 2.1 license), Z-Image Turbo, or Krea 2 (community license; check the revenue cap).
  - Avoid FLUX.1 [dev], FLUX.2 [klein] 9B and FLUX.2 [dev] unless BFL commercial licensing is in place. That FLUX.2 [dev] is non-commercial is my inference from BFL's general [dev] licensing pattern; I did not verify it here.
- **When LoRA is worth it:** high volume (hundreds of images per avatar), a need to run on open models in ComfyUI, or a need to beat the multi-turn drift of reference-only models. For low-volume campaigns, the reference-only identity pack is faster and avoids the baked-lighting risk.
- **Watch item:** LoRA-Dataset-Forge depends on `gemini-3.1-flash-image-preview`, which retires on October 29, 2026, per the NB 2.1 coverage in section 1. Any pipeline built on it must migrate to NB 2.1 or NB Pro.

### Gaps
- I found no authoritative 2026 settings for Kohya/sd-scripts, OneTrainer, FluxGym, the Civitai trainer or Replicate's current FLUX.2 trainers. I also found nothing current on SDXL character LoRAs (legacy).
- I found no controlled study of the best image count for synthetic-person LoRAs, or of regularization images, in 2026. The numbers above are community defaults that conflict.
- Licensing for Qwen-Image-2.1 and Krea 2 (exact commercial terms) is unverified.

## 4. Face swap / identity-transfer adapters as a consistency layer (FaceFusion, ReActor, InstantID, PuLID, IP-Adapter FaceID, ACE++, InfiniteYou, UNO, etc.)

### Takeaway
Face swapping now works as a final "touch-up" layer rather than the core method.
- **FaceFusion:** its default swapper is now HyperSwap 256 (hyperswap_1a_256), not inswapper_128.
- **inswapper_128:** a 128-px face crop that is "noticeable at 4K". Its weights, like InsightFace's buffalo_l, are non-commercial without a paid InsightFace license.
- **Tuning-free FLUX.1 adapters (PuLID-Flux, InfiniteYou, DreamO, ACE++, UNO/USO/UMO):** still used, but they carry FLUX.1 dev non-commercial terms and known realism problems (CG look, copy-paste face, bad hands).

### Cited Findings
- FaceFusion's face-swapper docs list `hyperswap_1a_256` as the default, alongside `hyperswap_1b_256`, `hyperswap_1c_256` and `inswapper_128` variants. — [FaceFusion docs, face swapper](https://docs.facefusion.io/usage/cli-arguments/processors/face-swapper)
- FaceFusion 3.8.1 guide: the HyperSwap internal processing ("pixel boost") can be set to 256, 512, 768 or 1024 px. Higher settings improve detail but raise processing time and VRAM. — [note.com FaceFusion Lab (JP)](https://note.com/fine_dog7291/n/nf5d37fcbb4a2?hl=en)
- Default settings conflict between doc versions: the official CLI docs show a 128×128 default pixel boost. — [FaceFusion docs](https://docs.facefusion.io/usage/cli-arguments/processors/face-swapper)
- hyperswap_1b_256 is "best quality in most cases" but occasionally fails on specific faces. hyperswap_1a_256 is "the most stable, fewer artifacts". — [Hugging Face, FaceFusion-Face-Swap-Hyperswap](https://huggingface.co/prstyaDev/FaceFusion-Face-Swap-Hyperswap)
- Some users still prefer inswapper_128 plus GPEN-BFR-512 restoration for similarity on faces turned more than 45°. This is anecdotal. ReActor users requested HyperSwap 256 support. — [ComfyUI-ReActor issue #143](https://github.com/Gourieff/ComfyUI-ReActor/issues/143)
- The "128" in inswapper_128 is the face-crop resolution: fine for web, noticeable at 4K. Inswapper degrades on extreme angles, heavy occlusion or low-resolution sources. — [WaveSpeedAI, open-source face swap 2026](https://wavespeed.ai/blog/posts/open-source-face-swap-software/)
- Licensing: InsightFace code is MIT, but the pretrained packs (buffalo_l, buffalo_s, antelopev2) are "for non-commercial research purposes only". Commercial use of InSwapper-128 or buffalo_l requires a license from InsightFace. Auto-downloading the weights does not change the terms. — [InsightFace python-package README](https://github.com/deepinsight/insightface/blob/master/python-package/README.md); [InsightFace licensing site](https://www.insightface.ai/); [Hysen Labs](https://hysenlabs.com/projects/deepinsight-insightface)
- InfiniteYou (ByteDance, ICCV 2025 highlight) vs PuLID-FLUX, as reported by the InfiniteYou authors: ID loss 0.209 vs 0.225 (lower is better), CLIPScore 0.318 vs 0.286, PickScore 0.221 vs 0.212. In the user study, 72.8% preferred InfiniteYou. — [InfiniteYou paper, arXiv 2503.16418](https://arxiv.org/pdf/2503.16418)
- PuLID-FLUX has "decent identity similarity" but poor text-image alignment, degraded image quality (bad hands) and aesthetics, plus a face "copy-paste" issue. IP-Adapter on FLUX has weak identity similarity. — [InfiniteYou project page](https://bytedance.github.io/InfiniteYou/)
- InfiniteYou's default variant prioritizes realism and alignment. The `sim_stage1` variant gives higher ID similarity but worse text alignment. — [InfiniteYou GitHub](https://github.com/bytedance/InfiniteYou); [AIModels.fyi](https://www.aimodels.fyi/models/huggingFace/infiniteyou-bytedance)
- In the FaceCLIP-SDXL paper, InstantID scored 0.658 face similarity vs 0.651 for PuLID-SDXL (on Internal-v1). It also says PuLID images "exhibit a strong CG-like appearance and unnatural lighting". — [arXiv 2504.14202](https://arxiv.org/pdf/2504.14202). PuLID's own paper claims higher ID fidelity with less disruption than InstantID. — [PuLID, arXiv 2404.16022](https://arxiv.org/pdf/2404.16022)
- An October 2026 guide: PuLID-Flux is tuning-free from one reference image, needs about 12GB VRAM at 8-bit and is still labeled beta. The PuLID weights are Apache 2.0, but FLUX.1 dev and InsightFace carry non-commercial terms. InstantID is SDXL-only. IP-Adapter FaceID is "mature" for low-setup single-photo work but not state of the art. — [AIOFM, PuLID vs InstantID vs FaceID 2026](https://aiofm.info/en/guides/pulid-vs-instantid-vs-faceid)
- InfiniteYou needs about 24GB VRAM and is listed as the top choice for highest identity match in a 2026 ComfyUI character skill. The same ecosystem points to FLUX.2 (up to 10 refs) for multi-reference consistency. — [ComfyUI-Expert character-gen skill](https://github.com/mckruz/comfyui-expert/blob/master/skills/comfyui-character-gen/SKILL.md); [AIOFM ComfyUI Flux workflow guide 2026](https://aiofm.info/en/guides/comfyui-flux-workflow-builder-2026)
- Other FLUX.1-based subject/identity methods:
  - UNO (ByteDance, ICCV 2025): single and multi-subject customization. UMO, from the same repo, does one-to-many identity. — [GitHub bytedance/UNO](https://github.com/bytedance/UNO)
  - USO: unified style-subject, with a "de-stylizing back to photorealism" expert. — [USO, arXiv 2508.18966](https://arxiv.org/html/2508.18966v1)
  - DreamO: built on Flux-1.0-dev, with an ID mode similar to InstantID/PuLID. — [DreamO, arXiv 2504.16915](https://arxiv.org/html/2504.16915); [Replicate DreamO](https://replicate.com/zsxkib/dream-o/readme)
  - ACE++: an extension of FLUX.1 Fill using LoRAs for ID transfer, face swap and subject transfer from one reference with no training. — [ComfyUI nomadoor ACE++ guide](https://comfyui.nomadoor.net/en/basic-workflows/ace-plus-plus/); [RunComfy ACE++ workflow](https://www.runcomfy.com/comfyui-workflows/ace-plus-plus-character-consistency)
- No head-to-head quality comparison among UNO, USO, DreamO and ACE++ was found. — (search finding; see the sources above)

### Inferences
- **The swap layer is a late-pipeline fix.** Use FaceFusion HyperSwap 256 at pixel boost 512–1024, or a FLUX.2/LoRA inpaint pass, only on the 10–20% of renders that fail the identity threshold. It should not be the main method. Swaps at a 128 px crop (inswapper) are visibly soft on 2K–4K ad assets.
- **Commercial license exposure is large.** inswapper_128, buffalo_l (also used by ReActor and as PuLID/InstantID's face encoder) and FLUX.1 dev all need commercial licenses for a large company's paid ads. This favors closed APIs (NB Pro, GPT Image 2.5, Seedream) or permissively licensed open models (FLUX.2 klein 4B, Qwen, Z-Image) plus LoRA.
- **Mark these as outdated or legacy in October 2026:** IP-Adapter FaceID, InstantID (SDXL), PuLID-SDXL, inswapper_128 as a default, and FLUX.1-based adapters generally. Multi-reference editing models largely superseded them.

### Gaps
- I found no independent 2026 benchmark of HyperSwap vs inswapper vs diffusion inpainting on synthetic faces at 2K/4K.
- ReActor's current maintenance status and its handling of HyperSwap are unverified, as are the exact license terms of FaceFusion's HyperSwap models.
- I found no source evaluating PuLID/InfiniteYou-style adapters on FLUX.2 (as opposed to FLUX.1).

## 5. Identity drift over many generations: how to measure it (ArcFace/InsightFace cosine similarity) and QA thresholds

### Takeaway
There is no universal "same person" ArcFace cosine cutoff. Published operating points are about 0.36 (at a strict 1-in-10,000 false-match rate), about 0.5 (a common rule of thumb) and 0.6 (the "conventional" verification threshold in some papers), and similarity drops naturally with pose change. Teams should calibrate on their own avatar set and track the mean and minimum similarity against the master reference. Practical drift onset in multi-turn editing is reported at around 8–10 sequential edits.

### Cited Findings
- One paper accepts an identity match when cosine similarity "exceeds the conventional threshold 0.6". — [LAFR, arXiv 2505.23462](https://arxiv.org/pdf/2505.23462)
- Another uses an ArcFace threshold tied to a 1-in-10,000 false-match rate, which corresponds to a score of 0.356 on its model. — [Peepers & Pixels, arXiv 2503.20108](https://arxiv.org/pdf/2503.20108)
- Face-Sim guide: "a score of 0.5 or higher is often considered the same person", with typical thresholds ranging 0.3–0.7 by application. — [Zenn, Face-Sim introduction](https://zenn.dev/taku_sid/articles/20250511_face_sim_metric?locale=en)
- Arc2Face kept generated identities distinct by requiring pairwise similarity below 0.3, which is a useful "different person" bound. — [Arc2Face, ECCV 2024](https://www.ecva.net/papers/eccv_2024/papers_ECCV/papers/05442.pdf)
- Average pairwise similarity across random seeds is used to show that outputs converge toward a consistent identity. Face recognition similarity drops when poses vary, so a single threshold can mislead across angles. — [Morphological Addressing of Identity Basins, arXiv 2602.18533](https://arxiv.org/pdf/2602.18533); [SIG synthetic identity pipeline, arXiv 2409.08345](https://arxiv.org/pdf/2409.08345) (attribution across these)
- InfiniteYou reports identity as "ID loss" (1 − cosine), 0.209 vs PuLID-FLUX's 0.225. That implies a mean cosine of about 0.79 vs 0.78 on their benchmark. — [InfiniteYou paper](https://arxiv.org/pdf/2503.16418)
- FaceCLIP-SDXL reports face similarity around 0.65 for InstantID and PuLID-SDXL, giving an idea of typical adapter-level scores. — [arXiv 2504.14202](https://arxiv.org/pdf/2504.14202)
- Drift in practice: Nano Banana holds identity for 8–10 sequential edits, then drifts. Re-upload the original reference every few prompts. — [UD.hk](https://www.ud.hk/en/blogs/insight/article/2026-06-29-nano-banana-consistent-characters) (attribution across the guides in section 1)
- LoRA-Dataset-Forge uses a "Gemini-judge face validation" step (a VLM judge rather than an embedding score) to filter synthetic datasets. — [GitHub, LoRA-Dataset-Forge](https://github.com/IxMxAMAR/LoRA-Dataset-Forge)
- Licensing caveat for QA tooling: InsightFace's buffalo_l and antelopev2 recognition packs are non-commercial research-only. — [InsightFace python-package README](https://github.com/deepinsight/insightface/blob/master/python-package/README.md)

### Inferences
- **Suggested QA protocol** (my synthesis, to calibrate per avatar):
  1. Embed the hero portrait plus the 4–5 sheet views as the anchor set. Average the embeddings into a "centroid".
  2. For each new render, compute the cosine to the centroid and to the nearest same-pose anchor.
  3. For near-frontal shots, auto-pass at ≥0.60, send 0.45–0.60 to human review, and reject below 0.45. Lower the bounds by about 0.05–0.10 for profiles or extreme expressions, because pose depresses scores.
  4. Track rolling mean, minimum and standard deviation per campaign. A downward trend in the mean across a session signals drift: re-anchor by re-uploading the hero refs, or switch to the LoRA.
  These numbers are anchored to the published 0.5–0.6 operating points, but they are not a published standard.
- Add a second axis besides identity: a realism/texture check (human review or an aesthetic/IQA model). A face swap or high-weight adapter can raise ArcFace scores while lowering realism (the CG look, copy-paste face).
- A commercial QA pipeline should use a commercially licensed face-recognition model (or buy the InsightFace license) instead of the default buffalo_l.

### Gaps
- I found no published industry QA thresholds from AI-influencer or UGC agencies.
- I found no ComfyUI node or SaaS tool that is a documented standard for batch face-similarity filtering; the search budget ran out before I could check.
- Non-InsightFace commercial face-embedding alternatives (for example, AdaFace or vendor APIs) and their thresholds were not researched.

## 6. Prompt templates for consistent avatar shoots (official docs and top creators)

### Takeaway
The templates that work best in 2026 share four rules:
- Give every reference image a single explicit role ("Image 1 = face/identity only").
- State explicitly what must not change (face, proportions, hairline, marks).
- Change one variable per shot.
- "Bookend" the identity lock at the start and end of the prompt, with a fixed descriptor block reused verbatim.

### Cited Findings
- BFL (FLUX.2): state each image's role, for example subject from image 1 and style from image 2. — [BFL FLUX.2 prompting guide](https://docs.bfl.ai/guides/prompting_guide_flux2)
- OpenAI (GPT Image): "State which facial features and proportions must remain unchanged." — [OpenAI image prompting guide](https://developers.openai.com/api/docs/guides/image-prompting)
- Third-party GPT Image 2 template: "Use Image 1 only to preserve the character's face, hairline, and hair texture. Use Image 2 to preserve body proportions, outfit silhouette, color palette, and accessories. Use Image 3 only for brushwork, color mood, and rendering style." Also tell the model not to borrow identity details from style references. — [Image3.org, GPT Image 2 character sheet prompts](https://image3.org/blog/gpt-image-2-character-sheet-prompts); [gpt-image2ai.art](https://gpt-image2ai.art/blog/gpt-image2-ai-art-character-consistency-prompt-guide/) (attribution across these)
- Nano Banana: lock the face at the start, change only the scene in the middle, and repeat the lock at the end. Use anchors such as "keep the same facial features and proportions". Repeat the 3–4 most distinctive features each time. — [UD.hk](https://www.ud.hk/en/blogs/insight/article/2026-06-29-nano-banana-consistent-characters); [Nenobanana, 12 prompts that work](https://www.nenobanana.com/blogs/nano-banana-character-consistency-12-prompts-that-actually-work--2026-guide) (attribution across these)
- Google's general prompting advice: be specific about subject, composition, action, location and style. — [Google blog, 7 tips for Nano Banana Pro](https://blog.google/products-and-platforms/products/gemini/prompting-tips-nano-banana-pro/)
- Turnaround prompt closing: "Keep the same face, hair, proportions, outfit, colors, and rendering style in every view." — [Quest Studio](https://queststudio.io/blog/ai-character-turnaround-sheet)
- There is no official "same person" token or identity-lock keyword in Nano Banana; such phrases are informal prompt wording. — (search finding across [Sider](https://sider.ai/blog/ai-image/nano-banana-pro-cheat-sheet-for-character-consistency) and the NB guides above)
- Midjourney V7: `--oref <hero image URL> --ow 100–300` (below 400), plus `--sref` for the look. — [Midjourney updates](https://updates.midjourney.com/omni-reference-oref/); [Flowith](https://flowith.io/blog/midjourney-v7-consistent-characters-masterclass/)

### Inferences
- **Synthesized master template** (composed from the cited principles; not an official template):
  - `[IDENTITY LOCK] Use Image 1–3 ONLY as identity references for the same woman: keep her face shape, eye color (hazel-green), brow shape, hairline, nose, lips, the small mole above the left lip, and her freckle pattern exactly identical. Do not beautify, slim, or age her.`
  - `[SCENE] Now photograph her: <outfit>, <location>, <pose>, <expression>, shot on <camera/lens>, <lighting>, natural skin texture with visible pores, no retouching.`
  - `[PRODUCT] Use Image 4 only for the product's exact shape, label and colors.`
  - `[RE-LOCK] Same person as Image 1; identity unchanged; only the outfit, setting and pose differ.`
- For edits on an existing approved shot (GPT Image 2/2.5 or NB Pro): "Edit this photo: change only <X>. Keep her face, expression, skin texture, hair and body unchanged." This leans on the editing strength these models are reported to have, and keeps drift down compared with regenerating from scratch.

### Gaps
- I could not retrieve the full text of Google's official "7 tips" post or the official Gemini docs' example prompts for character consistency.
- I found no official Seedream or Qwen prompt templates for identity locking.

## 7. Workflow recommendations used by AI influencer / AI UGC agencies in 2026 (including non-English sources)

### Takeaway
Practitioner workflows in 2026 are hybrid:
1. Design the person once (text-to-image hero shot).
2. Build a neutral identity sheet with a multi-reference model (mostly Nano Banana Pro or Seedream).
3. Produce campaigns from that pack zero-shot.
4. For high volume or open-model pipelines, generate a synthetic dataset, cull it by face similarity, and train a LoRA (Krea 2, Z-Image, Qwen, FLUX.2 klein) or a hosted ID (Higgsfield Soul ID).
5. Optionally do a final face-swap or inpaint touch-up.

Chinese and Brazilian sources reflect the same split, with Chinese creators arguing that only a LoRA truly locks identity.

### Cited Findings
- Brazilian (PT) workflow: start from a neutral anchor image (Seedream or Nano Banana), then train a LoRA for the character. — [Human Academy](https://www.humanacademy.ai/en/blog/personagem-consistente-ia)
- PT tutorial on making a consistent character for free with Nano Banana (reference-only). — [Nespol](https://nespol.com.br/blog/nano-banana-como-criar-personagem-consistente-gratis/)
- A Midjourney base image combined with Nano Banana (via Krea.ai) produces angle and detail variations. — [Ciguleva Substack](https://ciguleva.substack.com/p/step-by-step-guide-consistent-characters)
- An end-to-end AI-influencer workflow with only Nano Banana relies on model sheets and reference stacking. — [Chetan Pujari Substack](https://chetanpujari.substack.com/p/how-i-created-an-ai-influencer-using)
- Chinese (CN) sources:
  - "Reference images can transfer style but cannot lock facial identity; LoRA can", and training takes under an hour of GPU (author's claim). — [Bilibili](https://www.bilibili.com/video/BV11cTo6WEfM/)
  - Claims of ">95% consistency" for LoRA workflows (in AI comic-drama production) and for ByteDance USO are not backed by published tests. — [AIGC SDM](https://www.aigcsdm.com/news/121); [Tahou](https://www.tahou.com/article/203508355810250757)
- Higgsfield markets Soul ID (20+ photos, about 3 minutes of training) with 60+ fashion-grade presets, aimed at influencer-style photo dumps. — [Higgsfield help center](https://higgsfield.ai/creator-hub/help-center/ai-models/how-do-i-create-and-use-a-soul-id-character); [Higgsfield photodump blog](https://higgsfield.ai/blog/how-to-create-ai-photodump-higgsfield-soul)
- Ready-made "AI influencer generators" built on Nano Banana promise a consistent face, hairstyle and style across campaigns. — [Media.io (BR)](https://www.media.io/br/image-effects/ai-influencer-generator.html)
- Open-source tooling for the "references → dataset → LoRA" step exists, with VLM face validation. — [LoRA-Dataset-Forge](https://github.com/IxMxAMAR/LoRA-Dataset-Forge); [NanoBananaLoraDatasetGenerator](https://github.com/lovisdotio/NanoBananaLoraDatasetGenerator)
- Provenance: GPT-Image-2.5 outputs carry C2PA metadata. — [Unite.AI](https://www.unite.ai/openai-releases-chatgpt-images-2-5-with-sketch-and-two-new-api-models/)
- Ideogram Character is pitched for real people "provided the user has the necessary rights" (a rights and consent framing). — [The Rundown](https://www.therundown.ai/tools/character)

### Inferences
- **Recommended SOP for the client** (synthesized; every step maps to cited findings above):
  1. **Design.** Generate 50–100 candidate faces with text-to-image on NB Pro, GPT Image 2.5 or Krea 2. Pick one. Verify it does not resemble a real person: run a face search and check that ArcFace similarity is below about 0.3 against any celebrity or face database the client holds (based on Arc2Face's below-0.3 "different person" bound).
  2. **Identity pack.** Produce the hero portrait, the 4 head angles, a full body, a skin macro and 2–3 expressions under even, neutral light on grey (NB Pro or Seedream 4.5). Write the 3–4-marker descriptor block and freeze it in a "character bible".
  3. **Zero-shot production.** Use NB Pro (up to 5 people refs: hero plus 3–4 angles) with the bookended template, plus product refs in the object slots. Use GPT Image 2.5 for edits of approved shots. Re-anchor every 8–10 turns.
  4. **QA.** Run ArcFace cosine against the pack centroid, with thresholds calibrated per avatar (section 5), plus a human realism check.
  5. **Scale-up (optional).** When volume exceeds about 100 images per month per avatar, or when open models or local ComfyUI are needed: generate 40–60 varied images, cull to 25–40 by QA, and train a LoRA on a commercially licensed base (FLUX.2 klein 4B, Z-Image Turbo, Qwen-Image or Krea 2 after a license check). Use rank 16–32, LR 1e-4, batch 1, 1,500–3,000 steps, checkpoints every 250 steps, and pick the earliest passing checkpoint.
  6. **Repair.** Fix failing renders with an identity-preserving edit (NB Pro, GPT Image 2.5 or FLUX.2 multi-ref inpaint) or with FaceFusion HyperSwap at 512+ pixel boost, but only with commercial licensing sorted.
  7. **Versioning.** Store the pack, the descriptor, the model and version, seeds and the QA scores per asset. Re-validate whenever a model is retired (for example, NB2 on October 29, 2026).
- **Legal note (brief, unresearched here):** using fictional synthetic people avoids likeness rights, but the design step should screen for accidental resemblance to real people. Ad disclosure rules for AI-generated people (for example, EU AI Act transparency duties and FTC endorsement rules) should be covered by the legal researcher. I could not research them.

### Gaps
- I found no r/AIInfluencer, r/StableDiffusion or r/comfyui threads in search results, so community consensus from Reddit is not represented. X/Twitter creator workflows are limited to vendor posts.
- Japanese, Korean and Russian sources were not reached (the search budget ran out). The only JP sources found are the Qwen 2.1 LoRA guide and the FaceFusion guide on note.com, and the only RU hit was an unread Habr article ([habr.com](https://habr.com/ru/articles/996692)).
- There is no documented SOP from a named large AI-UGC agency. The SOP above is a synthesis.
- The legal and regulatory specifics (EU AI Act Article 50 timing, FTC rules on AI testimonials, platform ad-policy labeling) were not researched because of the search budget.
