# Upscaling, skin-texture enhancement and post-processing for photoreal AI portraits/avatars (state as of Oct 2026)

> Method note for the report writer: the session's egress policy blocked every direct page fetch (HTTP 403 on CONNECT for docs.magnific.com, docs.comfy.org, openart.ai, docs.topazlabs.com, etc.). Every finding below therefore comes from search-engine extracts and summaries of the cited pages, not from full-page reads. When one search returned several URLs, matching a claim to a specific URL is best-effort. Treat exact numbers as "reported by the cited page" and re-check them on the live page before using them in a client SOP. Scope is still images only.

## 1. Which 2026 upscalers/enhancers add realistic skin texture, and which over-sharpen, hallucinate or produce the "Magnific face"/plastic look?

### Takeaway
The tools fall into two groups. Conservative, identity-preserving upscalers are SeedVR2, Topaz Gigapixel Redefine *Realistic*/Standard, Magnific Precision v2 (Photo), Krea at 2x with low strength, and LetsEnhance Prime. Generative "re-imaginers" are Magnific Creative at high Creativity/HDR, Topaz Bloom, Clarity-style SD upscalers and high-creativity Redefine *Creative*: they add the most texture but drift faces and cause the plastic "Magnific face". For AI avatars, the consensus in the sources is to upscale conservatively first and then add skin texture with a dedicated skin tool (Magnific/Freepik Skin Enhancer, Enhancor) at low intensity.

### Cited Findings
**Brand and product status (needed to read 2026 sources correctly)**
- Freepik rebranded as **Magnific** on 28 April 2026. Freepik had acquired Magnific AI in May 2024, and accounts and subscriptions carried over. magnific.ai now redirects to magnific.com, and the upscaler, Relight and Skin Enhancer are tools inside one credit-based suite. So "Freepik Skin Enhancer" and "Magnific Skin Enhancer" are the same product in 2026 — [DreamDrive](https://www.dreamdrive.ai/learn/magnific/freepik-is-now-magnific/); [Oakgen](https://oakgen.ai/blog/magnific-ai-freepik-rebrand-pricing); [AIarty review](https://www.aiarty.com/knowledge-base/freepik-reviews.htm). Sources conflict on whether a "legacy" standalone magnific.ai service still exists, and on pricing — [Woska](https://www.woska.space/blog/magnific-ai-is-now-freepik-2026); [tooldirectory](https://tooldirectory.ai/tools/magnific-ai).
- Topaz Gigapixel v1.3.0 (13 May 2026) introduced **Recover Faces 3**. It removed v2's 512×512 output cap and the dot artifacts that v2 produced at high strength — [Topaz Community release notes](https://community.topazlabs.com/t/topaz-gigapixel-v1-3-0-recover-faces-3-300-speed-up-for-neuroserver-models/102815). A forum thread on "skin artifacts in generative models" is marked "Resolved in v1.3.0" — [Topaz Community](https://community.topazlabs.com/t/resolved-in-v1-3-0-skin-artifacts-generative-models/90293). The latest release found was v1.3.6 (31 Aug 2026), a bug-fix release — [Topaz Community](https://community.topazlabs.com/t/topaz-gigapixel-v1-3-5-v1-3-6/104643).

**Conservative / faithful group**
- ComfyUI's official upscaling tutorial classes **SeedVR2** as a "conservative" upscaler and points to **Magnific Skin Enhancer** as the portrait-specific option — [ComfyUI docs](https://docs.comfy.org/tutorials/utility/image-upscale). Comfy's workflow page says SeedVR2 keeps pores, edges and natural texture — [Comfy workflows](https://comfy.org/workflows/use-cases/ai-image-upscaler/).
- A community "Battle of the Image Upscalers" pack ranks SeedVR2 as the best all-around option, Flux DyPE + Upscale as best for detail, and SRPO + Upscale as best for skin — [GitHub rik-python](https://github.com/rik-python/Comfyu--Image-detailer-and-skin-detailer-workflows). The SeedVR2 + SRPO two-stage combo is also described for 8 GB GPUs — [MyAIForce](https://myaiforce.com/seedvr2-srpo-upscaling/).
- SeedVR2 can still go wrong on faces. The ComfyUI Cloud node page warns that the sharper models "can tip plasticky on faces" and can turn close-up skin "plasticky or scaly", and it advises a separate ADetailer/inpaint pass for recognizable faces — [ComfyUI Cloud (comfy.icu)](https://comfy.icu/node/SeedVR2). Chinese community tutorials say the **3B model mainly smooths skin (磨皮)** and **7B gives more detail** — [Bilibili](https://www.bilibili.com/video/BV1RBCTBQEcK/); [CSDN](https://blog.csdn.net/gitblog_00299/article/details/157195624). A "SeedVR2.5" is referenced in a late-2025/2026 Chinese guide — [cnblogs](https://www.cnblogs.com/AlayaNeW/p/19274255).
- One user called SeedVR2 the best diffusion-based enhancer they had used, better than Topaz Starlight (single anecdote) — [itch.io forum](https://itch.io/t/5504508/seedvr2-model-request).
- **Topaz Gigapixel**: Redefine is split into a *Realistic* mode (refines existing detail) and a *Creative* mode (reimagines detail) — [Topaz Community](https://community.topazlabs.com/t/topaz-gigapixel-v1-3-1/103355); [media.io review](https://www.media.io/comparison/topaz-labs-image-upscaler-review.html). Gigapixel works well when the face is already clean, but flaws scale up with it — [Skylum blog](https://blog.skylum.com/topaz-photo-ai-vs-gigapixel/). A 2026 review recommends **Redefine Realistic (Subtle)** for 1024×1024 AI images because it cleans AI artifacts while enlarging — [media.io](https://www.media.io/comparison/topaz-labs-image-upscaler-review.html); [Morphed](https://morphed.app/blog/topaz-gigapixel-ai-image-upscaler).
- Topaz's own Face Recovery 3 developer doc says it is reconstructive, "may include subtle changes to expressions or fine facial characteristics", and is meant for faces that standard upscaling cannot recover — [Topaz developer docs](https://developer.topazlabs.com/image-models/gigapixel/face-recovery-3). A review says Topaz warns that applying it to already high-quality faces can remove real detail — [Morphed](https://morphed.app/blog/topaz-gigapixel-ai-image-upscaler).
- **LetsEnhance Prime** is marketed as built "to avoid plastic skin, identity drift, and over-processing", with no sliders — [LetsEnhance portrait guide](https://letsenhance.io/blog/all/enhance-portraits-guide/). Topaz's own (vendor-biased) comparison ranks it a close second, "a half-step behind on fine texture" — [Topaz Labs](https://www.topazlabs.com/best-image-upscalers).
- **Krea Enhancer**: for portraits, "stop at 2x and low strength" because extra invented detail makes the face stop looking like the person — [Krea blog](https://www.krea.ai/blog/best-ai-image-upscalers-in-2026); [Krea docs](https://www.krea.ai/docs/user-guide/features/enhancer).

**Generative / risk-of-plastic group**
- **Magnific Creative**: with Creativity and HDR both raised, reviewers describe "plastic skin". HDR adds micro-contrast, and too much produces blotches. High creativity can change identity "in ways that are cosmetically plausible but factually wrong" — [Vantaige 2026 review](https://vantaige.io/ai-tool/magnific); [note.com/climbrice (JP)](https://note.com/climbrice/n/nd4ba0f1f5bae?hl=en); [AI Tool Lab](https://www.aitoolbox.hk/tools/magnific-ai/).
- **Magnific Precision v2**: a review found that on close-up AI portraits skin "could feel a bit over-sharpened, with pores appearing slightly exaggerated" — [Curious Refuge](https://curiousrefuge.com/blog/magnific-ai-image-upscaler-review) (best-effort attribution).
- **Topaz Bloom** is a cloud diffusion "creative upscaler" aimed at AI art. Point it at a real portrait "and it will happily alter faces". One tester at minimum creativity saw facial features change and the subject's eyes open: "not the same person" — [AIarty Bloom review](https://www.aiarty.com/ai-image-enhancer/topaz-bloom.htm); [Arjen Roos](https://www.arjenroos.com/topaz-bloom-vs-magnific-ai/); [Cascade Hub](https://thecascadehub.com/topaz-gigapixel-vs-magnific-vs-bloom-ai-upscaling/). The common recommendation is "Gigapixel for the photo, Bloom for the art" — [Cascade Hub](https://thecascadehub.com/topaz-gigapixel-vs-magnific-vs-bloom-ai-upscaling/).
- **Redefine Creative** can "alter the character of a face" — [Chase Jarvis](https://chasejarvis.com/blog/topaz-ai-image-upscaler/). One review says Face Recovery is disabled on Redefine because it would conflict with the generative layer (unverified third-party claim) — [Morphed](https://morphed.app/blog/topaz-gigapixel-ai-image-upscaler).
- **Clarity Upscaler** and Crystal-style SD-backbone upscalers "add creative sharpening that recovers skin pores… more aggressively", which makes them the riskiest for drifted or over-textured faces unless creativity stays near the bottom — [Ropewalk](https://ropewalk.ai/blog/best-ai-image-upscaler-2026); [OpenArt](https://openart.ai/blog/best-ai-image-upscalers-for-skin-texture/).
- **Leonardo Universal Upscaler** sits "between faithful and creative" and is described as best for AI art. No portrait-specific skin test was found — [DIY AI](https://diyai.io/ai-tools/image-generation/best-ai-image-upscalers/); [AI Photo Generator](https://www.aiphotogenerator.net/blog/2026/03/best-ai-image-upscalers-2026). Users "repeatedly flag plastic skin, invented texture and edge halos once enhancement gets aggressive" — [DIY AI](https://diyai.io/ai-tools/image-generation/best-ai-image-upscalers/).
- **SUPIR**: the only "beats Magnific/Topaz" and "almost 100% faithful" claims come from its main tutorial author (promotional, not independent) — [FurkanGozukara wiki](https://github.com/FurkanGozukara/Stable-Diffusion/wiki/SUPIR:-New-SOTA-Open-Source-Image-Upscaler-&-Enhancer-Model-Better-Than-Magnific-&-Topaz-AI-Tutorial); [HF blog](https://huggingface.co/blog/MonsterMMORPG/supir-sota-image-upscale-better-than-magnific-ai).
- **Nano Banana Pro 4K re-render**: in one test, native 4K oversharpened pores, so the author preferred a 1080p render plus an external upscale and a slight clarity bump. The upscaled 1080p version, however, showed "zipper" artifacts in out-of-focus highlights, where native 4K was smoother — [WaveSpeed](https://wavespeed.ai/blog/posts/blog-nano-banana-pro-4k-output-settings/). A widely shared re-render prompt asks for 4K "preserving 100% character consistency, original facial features…" — [X @ChillaiKalan__](https://x.com/ChillaiKalan__/status/2000176258135871840).

### Inferences
- For a company's recurring avatar (identity matters across many ads), the safe default is a conservative upscaler (SeedVR2 3B/7B with a face check, Topaz Redefine Realistic Subtle, Magnific Precision v2 Photo near defaults, or Krea 2x low strength). Texture should come from a separate, controllable skin pass, not from a high-creativity upscale.
- The "Magnific face" and plastic look reported in the sources come from combining a high creativity/HDR-type slider with large scale factors. The symptom is pores that are uniformly exaggerated or skin that looks waxy and blotchy.
- Generative re-render approaches (Nano Banana Pro 4K, Bloom, Redefine Creative) are best used only when the base image is weak, and they need a strict identity check afterwards.

### Gaps
- No independent, controlled 2026 face benchmark across Magnific, Topaz, Krea, SeedVR2, SUPIR and Enhancer tools was found. The comparisons are vendor blogs, reviews and anecdotes.
- Nothing usable was found on **4x-UltraSharp / Nomos / RealESRGAN** face behaviour in 2026, beyond 4x-UltraSharp being the usual upscale model inside Ultimate SD Upscale (see Q2).
- No source evaluated **GPT image (OpenAI) "high quality"** output as an upscaling or re-render step for skin.
- **CCSR** returned no 2026 results.
- **Magnific "Skin Enhancer" vs "Enhancor"**: no head-to-head test was found.

## 2. Exact settings (Magnific sliders, Topaz Redefine creativity/texture, tile denoise, scale factors, final resolution for ads)

### Takeaway
None of the vendors publishes an official "portrait preset with numbers". The reported starting points are:
- **Magnific Creative:** low Creativity (≈0–3), Resemblance high or at a slightly negative offset, HDR ≈0, a Portrait preset.
- **Magnific Precision v2:** sharpen ≈7 / smart grain ≈7 / ultra detail ≈30 (API defaults), lowered for faces.
- **Magnific Skin Enhancer:** sharpen 0, grain ≈2.
- **Topaz Redefine Creative:** creativity levels 1–3 only; texture very low (≈5) where used.
- **Tile upscales:** denoise 0.2–0.35 (0.35–0.45 adds detail; ≥0.5 shifts faces).
- **Scale factor:** 2x steps, not a single 4x jump.
- **Delivery size:** Meta's 1440-px-wide specs.

### Cited Findings
**Magnific (Creative "classic" upscaler)**
- Magnific launched a **"Portraits (Hard)"** preset — [Magnific Substack](https://magnific.substack.com/p/super-reimagined-hi-res-upscaling). The Flora integration lists Standard, **Soft Portraits** and Hard Portraits styles and suggests Soft Portraits for faces — [Flora docs](https://docs.flora.ai/models/image-models/magnific-upscaler-and-enhancer).
- An old official portrait example used **Creativity 3, HDR 0, Resemblance −1, Fractality 3**. It is about 1,000 days old and uses an earlier slider scale, so it is OUTDATED as a literal recipe — [Magnific Substack](https://magnific.substack.com/p/super-reimagined-hi-res-upscaling).
- A Japanese guide's tip: if Creativity 2 changes little, try Resemblance −1 or −2 before raising Creativity to 3–4 — [note.com/climbrice](https://note.com/climbrice/n/nd4ba0f1f5bae?hl=en). A 2026 review: "keep the Creativity slider low and Resemblance high for anything with human faces" — [Vantaige](https://vantaige.io/ai-tool/magnific).
- Adjust Sharpen, HDR, Fractality, Smart Grain and Ultra Detail **one at a time** so you can see what each change did — [Phygital+](https://phygital.plus/ai-models/magnific-upscale/).
- Magnific's own explainer separates Creative and Precision modes — [Magnific blog](https://www.magnific.com/blog/understanding-freepiks-upscaler-modes/).

**Magnific Precision v2**
- The API example and defaults are **sharpen 7, smart_grain 7, ultra_detail 30**. Sharpen runs 0 (none) to 100. Higher smart grain "adds more fine-grained texture to keep the image from looking too smooth or artificial". Ultra detail controls how much micro-detail the AI adds — [Magnific API](https://docs.magnific.com/api-reference/image-upscaler-precision-v2/post-image-upscaler-precision-v2); [overview](https://docs.magnific.com/api-reference/image-upscaler-precision-v2/overview).
- The model flavors are **v2 (sublime), v2 (photo), v2 (photo denoiser)**. The *Photo* model is described as ideal for portraits and editorials because it keeps an "authentic photographic atmosphere" — [Magnific blog](https://www.magnific.com/blog/magnific-precision-v2/); [Runway help](https://help.runwayml.com/hc/en-us/articles/51243511607827-Upscaling-an-image-with-Magnific-Precision-v2); [RunComfy node](https://www.runcomfy.com/comfyui-nodes/ComfyUI/magnific-image-upscaler-precise-v2-node).

**Magnific Skin Enhancer**
- It has three modes, **Creative / Faithful / Flexible**. Sharpen and smart grain each run 0–100, Faithful adds a **skin detail** control, and Flexible offers five optimization presets, including one aimed at realism — [Magnific API overview](https://docs.magnific.com/api-reference/skin-enhancer/overview).
- The official Flexible example request uses **sharpen 0, smart_grain 2, preset "enhance_skin"** — [Magnific API Flexible](https://docs.magnific.com/api-reference/skin-enhancer/post-flexible).
- The web UI exposes Detail, Grain and Sharpness sliders. Choose *Faithful* to preserve the original look — [OpenArt](https://openart.ai/blog/best-ai-image-upscalers-for-skin-texture/). It is also available as a ComfyUI API node — [Comfy hub](https://comfy.org/hub/models/magnific-skin-enhancer/); [Comfy workflow](https://comfy.org/workflows/api_magnific_skin_enhancer-81643690b5e9/).

**Magnific Relight** (lighting fix before finishing)
- There are two modes. *Relight* has virtual lights with color, Rotate, Elevation and Intensity sliders plus Top/Front/Left/Right/Back/Bottom presets. *Light transfer* takes a reference image — [Magnific docs](https://www.magnific.com/ai/docs/relight).
- The API/Comfy node exposes `light_transfer_strength` (0% = closest to the original, 100% = max), `interpolate_from_original` and `change_background` — [ComfyUI node docs](https://docs.comfy.org/built-in-nodes/MagnificImageRelightNode).
- It can cause unwanted facial changes with multiple people or small faces, but performs well on standard portraits — [The Decoder](https://the-decoder.com/magnific-ais-relight-uses-prompts-to-transform-image-lighting-and-backgrounds/).

**Topaz Gigapixel**
- Redefine Creative reportedly has creativity levels Low/Medium/High/Max plus texture sliders — [media.io](https://www.media.io/comparison/topaz-labs-image-upscaler-review.html). A forum user counts 6 creativity levels, says "fantasy starts between levels 3 & 4", and says photographers should use levels 1–3 for realism — [DPReview forum](https://www.dpreview.com/forums/threads/topaz-bloom.4806341/). The level count conflicts between sources, likely because of different versions.
- Texture "controls degrees of definition". Auto Mode for Redefine Creative clears the prompt and sets Texture automatically — [Topaz docs](https://docs.topazlabs.com/gigapixel-ai/filters-panel/settings).
- One user's workflow applies Redefine Creative with **texture 5** only to selected areas, especially the eyes, and blends it — [NikonCafe](https://www.nikoncafe.com/threads/catching-up-with-topaz-photo-ai-gigapixel-ai.365197/).
- The older Face Recovery strength slider ran 0–100 with auto override. Whether Face Recovery 3 keeps that range is unconfirmed — [Topaz Community](https://community.topazlabs.com/t/topaz-gigapixel-v1-3-0-recover-faces-3-300-speed-up-for-neuroserver-models/102815).

**Krea Enhancer**
- Scale options are 1x/2x/4x/8x, and the controls are **Strength, Resemblance, Clarity**. Use 1x when resolution is fine and only clarity is needed, since higher multipliers give the AI more room to invent — [Krea docs](https://www.krea.ai/docs/user-guide/features/enhancer).
- Recipes: real photo = **2x, creativity at or near zero, mask faces/logos**. Portrait = stop at 2x, low strength. AI-generated image = medium strength, iterate — [Krea blog upscalers](https://www.krea.ai/blog/best-ai-image-upscalers-in-2026); [Krea blog enhancers](https://www.krea.ai/blog/best-ai-photo-enhancers-in-2026).

**SeedVR2 (ComfyUI)**
- The official tip is to downscale the input to about **0.35 MP** (ImageScaleToTotalPixels) before SeedVR2 — [ComfyUI docs](https://docs.comfy.org/tutorials/utility/image-upscale).
- Test at **2K before 4K**, since 4K makes artifacts more visible — [seedvr2.net](https://seedvr2.net/blog/tutorials/seedvr2-zimage-4k-upscaling-8gb-vram-2026). A guide suggests cfg_scale 2.0–3.0 for richer texture (general images, not portrait-tested) — [seedvr2.net](https://seedvr2.net/blog/tutorials/seedvr2-zimage-4k-upscaling-8gb-vram-2026).
- Chinese workflows tile at **1024×1024** with SeedVR2 resolution 1024 — [GitHub zwchyt](https://github.com/zwchyt/SeedVR2-ultra-realistic-resolution). Tile count is 2–3 by default for 4K, or 4 when faces or text are small in frame — [RunningHub](https://www.runninghub.cn/post/1989503162178523137).
- VRAM: at least **12 GB for 3B, 16 GB+ for 7B** — [Bilibili](https://www.bilibili.com/video/BV1kkvTz8EyB/) / [CSDN](https://blog.csdn.net/sanwei12345/article/details/153494781). Beginner config is 3B fp8 at 1080 target; advanced is 7B fp16 at 1440+ (a video-oriented guide) — [CSDN](https://blog.csdn.net/gitblog_00299/article/details/157195624).

**Ultimate SD Upscale / Flux tile / detailers**
- Denoise bands: **0.2–0.3 = cleanup/sharpen with little change; 0.35–0.45 = adds detail; ≥0.5 can shift faces and backgrounds** — [ComfyLab](https://comfylab.dev/blog/workflows/comfyui-upscale-workflow-ultimate-sd-upscale/). Another guide gives 0.3–0.5 with 4x-UltraSharp — [VideoProc](https://www.videoproc.com/resource/ultimate-sd-upscale.htm).
- **FaceDetailer ≈0.45** for a face-repair pass. Fix faces *before* upscaling, because "upscaling a bad face scales the badness" — [ComfyLab](https://comfylab.dev/blog/workflows/comfyui-upscale-workflow-ultimate-sd-upscale/).
- Tile padding **32–64** with Chess mode reduces seams, and 512 px tiles are usually enough for 2K — [ComfyUI nomadoor](https://comfyui.nomadoor.net/en/basic-workflows/ultimate-sd-upscale/); [Civitai upscaling guide](https://civitai.com/articles/8456/upscaling-guide).
- Flux upscale workflows suggest low denoise (**0.2–0.4**) if major details are getting lost — [RunComfy Flux Upscaler](https://www.runcomfy.com/comfyui-workflows/flux-upscaler-4k-8k-16k-32k-image-upscaler).

**Target final resolution for ads**
- Meta (third-party summaries of Meta's specs): Feed **1440×1800 (4:5)** or **1440×1440 (1:1)**; Stories/Reels **1440×2560 (9:16)**; JPG/PNG up to 30 MB; keep roughly 14% at the top and 20% at the bottom free as safe zones. One source still lists 1080×1350 for 4:5 — [AdsUploader](https://adsuploader.com/blog/meta-ads-aspect-ratios); [AdMake](https://admakeai.com/blog/facebook-ad-image-sizes-2026); [Cropink](https://cropink.com/facebook-ad-sizes-and-specs).
- TikTok image ads, per third-party summaries: 1:1, 1080×1080, JPG/PNG, with a "<50 KB" cap (this probably refers to the ad *display image*/profile image rather than the creative; verify) — [MegaDigital](https://megadigital.ai/en/blog/tiktok-ad-formats-and-specs/); [Udonis](https://www.blog.udonis.co/advertising/tiktok-ad-specs). TikTok's recommended video ratio is 9:16 at 1080×1920 — [Nestscale](https://nestscale.com/blog/tiktok-ads-specs.html).

### Inferences
- **2x + 2x instead of one 4x jump**: Krea says higher multipliers give the AI more room to invent, and the SeedVR2 guidance is to test at 2K before going to 4K. Both point to a staged path: generate at ~1–2 MP, run 2x conservatively to ~2.5–4 MP, check the face at 100%, then do one more 2x only if a print or hero asset needs it.
- Because Meta delivers at 1440 px on the short side, a master of roughly 2880–4096 px on the long edge is plenty. Downscaling that master to 1440×1800 or 1440×2560 hides any remaining upscaler micro-artifacts. Going to 8K adds risk (exaggerated pores, scaly skin) with no visible benefit after platform recompression.
- Workable starting values for an AI avatar:
  - **Magnific Precision v2 Photo:** sharpen 0–5, smart grain 5–7, ultra detail 15–30.
  - **Magnific Skin Enhancer:** Faithful, skin detail low-to-mid, sharpen 0, grain 0–5.
  - **Topaz:** Redefine Realistic Subtle, or Creative at level 1–2 with texture ≤5; Recover Faces only if the face is soft.
  - **Tile upscale:** USDU/Flux denoise 0.25–0.35.

  These are extrapolated from the cited defaults and examples, not published presets.

### Gaps
- No official Magnific numeric portrait preset for the current (2026) slider scale was found.
- No official Topaz table of creativity/texture ranges for Redefine in v1.3.x was obtainable (the docs page fetch was blocked).
- Meta's and TikTok's official spec pages could not be accessed directly. The figures are from third-party summaries and partly conflict (1080×1350 vs 1440×1800).
- No SeedVR2 portrait-specific values for steps, color correction or noise injection were found.

## 3. Skin-texture enhancement tools/workflows (Enhancor, Magnific Skin Enhancer, skin LoRAs, FaceDetailer/ADetailer): over-texturing risk and identity preservation

### Takeaway
Dedicated skin tools (Magnific/Freepik Skin Enhancer, Enhancor) and skin-detail LoRAs reliably fix "plastic skin". Over-texturing (uniform pores, sandpaper or scaly skin, extra wrinkles) and identity drift rise with strength, heavy modes and high denoise. The cited practice is to:
- run the face fix *before* upscaling;
- keep detailer denoise around 0.4–0.45 or lower;
- keep a skin LoRA at 0.4–0.7, lowered when an identity LoRA already carries skin texture;
- prefer "Faithful" modes;
- check the face at 100% zoom.

### Cited Findings
- **Enhancor** (official): removes "plastic-looking skin" and restores texture, pores and detail. Its main model is "Skin Fix", and the site also lists a realistic upscaler up to 8K, a Human Generator and a newer "Kora Reality" model — [Enhancor](https://www.enhancor.ai/); [enhancorai.com](https://enhancorai.com/).
- Enhancor works best on head-and-shoulders framing — [MOGE](https://moge.ai/product/enhancorai); [Navi](https://navi.tools/tools/enhancor). Its Skin Editor has a **texture slider and a "Heavy Mode"** — [TechPilot](https://techpilot.ai/tools/enhancor-ai-fix-the-ai-plastic-skin/). It can target face, skin, eyes, nose or mouth, and paid plans export up to 4K — [Overchat](https://overchat.ai/ai-hub/best-ai-skin-enhancers). It is listed as less useful for real photographs. All "indistinguishable from real skin" claims are vendor or directory copy — [There's An AI For That](https://theresanaiforthat.com/ai/enhancor-ai/); [Future Tools](https://futuretools.io/tools/enhancor).
- **Magnific Skin Enhancer** restores pores and soft shadows and adds photographic grain. Magnific's blog gives no numeric values — [Magnific blog (via translate)](https://translate.google.com/translate?u=https%3A%2F%2Fwww.magnific.com%2Fblog%2Fhow-to-fix-plastic-skin-ai-skin-enhancer%2F&hl=es&sl=en&tl=es&client=srp). A competitor suggests low-to-medium creativity with face preservation on for plastic AI portraits — [Upsampler](https://upsampler.com/blog/magnific-ai-alternative-free).
- **Skin LoRAs**: use a Flux skin-texture LoRA at about **0.5–0.7** for close-ups. If a trained face/identity LoRA already has skin texture baked in, drop the detail LoRA to about **0.4**, and keep total LoRA weight at or below about 2.0 — [aiofm Flux realism LoRAs 2026](https://aiofm.info/en/guides/best-flux-loras-realism).
- The **Portrait Engine** LoRA (Flux / Flux 2 Klein / Z-Image) uses Z-Image settings euler, 8+ steps, CFG 1 — [Civitai](https://civitai.com/models/2067704/portrait-engine-flux-flux-2-klein-z-image-detailed-skin-lora).
- **PhotorealTouch** (Z-Image) claims to add pore detail "without forcing a new identity" (listing claim only) — [Civitai](https://civitai.com/models/1464286/photorealtouch). The **Flux Skin Detailer DoRA** can be used inside an Ultimate Upscaler pass — [Civitai](https://civitai.com/models/1018511/flux-skin-detailer-realistic-skin-dora). A multi-model "Realistic Skin Texture" LoRA (XL / SD1.5 / F1D / ZIT / ZIB) is also available — [Civitai](https://civitai.com/models/580857/realistic-skin-texture-style-detailed-skin-xl-sd15-f1d-pony-illu-zit-zib).
- RunComfy's **Z-Image Real Skin** workflow (Z-Image Turbo + Qwen-VL prompt extraction + realism LoRA) targets pores and fine lines without a plastic look — [RunComfy](https://www.runcomfy.com/comfyui-workflows/z-image-real-skin-workflow-in-comfyui-natural-texture-portraits). MyAIForce's Flux skin-realism workflow deliberately skips FaceDetailer because of memory cost — [MyAIForce](https://myaiforce.com/flux-skin-realism/).
- Run FaceDetailer at about 0.45 for face repair, before upscaling — [ComfyLab](https://comfylab.dev/blog/workflows/comfyui-upscale-workflow-ultimate-sd-upscale/). Give recognizable faces a separate ADetailer/inpaint pass after SeedVR2 if skin turns plasticky or scaly — [comfy.icu](https://comfy.icu/node/SeedVR2).
- A **Flux realism LoRA** may do little for skin in Flux dev — [HF XLabs discussion](https://huggingface.co/XLabs-AI/flux-RealismLora/discussions/5).
- **Nano Banana Pro skin prompts**: community prompts use phrases such as "hyper-realistic skin texture with visible pores and natural micro-details" plus macro-lens specs — [X @dhumann](https://x.com/dhumann/status/2002904155837648898?lang=en). Guides recommend "natural pores and microtexture" as an explicit fidelity cue — [Sider](https://sider.ai/blog/ai-image/best-prompt-structure-for-nano-banana-pro-realism-a-practical-guide).
- Topaz's **Gigapixel Texture slider applies to the whole image**, not just the face — [OpenArt](https://openart.ai/blog/best-ai-image-upscalers-for-skin-texture/) (summary attribution).

### Inferences
- To keep identity:
  1. Lock identity at generation (identity LoRA or reference).
  2. Do face repair at low-to-moderate denoise *before* upscaling.
  3. Apply skin texture as a masked, low-strength layer (skin only; exclude eyes, lips and hairline).
  4. Blend the enhanced layer at partial opacity in Photoshop.
  5. Compare against the identity master image side by side.

  This follows from the cited warnings: denoise ≥0.5 shifts faces, Face Recovery 3 may change expressions, Bloom and high-creativity modes change features, and skin LoRAs conflict with identity LoRAs.
- Signs of over-texturing to check: pores of equal size across the forehead, nose and cheeks; texture on lips and eyelids; "scaly" cheeks; halos at the hairline. Real skin texture varies by facial zone. This is general retouching knowledge, not cited.

### Gaps
- No published, measured method was found for quantifying identity drift (for example, face-embedding similarity thresholds) in commercial skin tools.
- No Enhancer/Enhancor numeric slider recommendations were found from the vendor.
- No ADetailer settings specific to 2026 Flux 2 / Z-Image were found beyond the ~0.45 FaceDetailer figure.

## 4. Finishing chain for a "real camera / phone" look: grain/noise, chromatic aberration, vignette, lens distortion, motion blur, white balance, JPEG, color grading, sharpening, avoiding over-HDR

### Takeaway
The sources agree that AI images read as fake because they are *too clean*. The fix is subtle, physically plausible imperfection applied **after** upscaling, in roughly this order: grade, then sharpen with masking, then grain, then lens effects, then export.
- **Grain:** monochrome (luminance) grain, low amount. Lightroom portraits use roughly Amount 18–25, Size 24–30, Roughness 45–52, or "1–3%" added noise.
- **Chromatic aberration:** only on high-contrast edges.
- **Vignette:** gentle.
- **Sharpening:** Radius ≈1.0 and Masking ≈40+ to keep sharpening off skin.
- **Export:** PNG master, moderate-quality JPEG for delivery.

### Cited Findings
**Grain / sensor noise**
- Lightroom grain lives under Effects as Amount / Size / Roughness. Portrait starting points are **Amount 18–25, Size 24–30, Roughness 45–52**. A "classic film" look uses **Amount 30–40, Size 28, Roughness 40–50**. Keep grain lighter on skin, place more of it in the midtones, and reduce clarity and sharpness as grain increases — [Legendary Presets](https://legendarypresets.com/realistic-film-grain-without-losing-detail/); [Presets.io](https://presets.io/a/blog/how-to-add-realistic-film-grain-in-lightroom); [Loumarks](https://loumarkspresets.com/blogs/lightroom/how-to-get-a-film-look-in-lightroom).
- For a phone look, keep grain **monochrome**, because colored speckle reads as sensor noise. Maximum roughness "looks like sandpaper" — [RAWCraft](https://rawcraft.app/guides/add-film-grain-iphone-photos).
- "Adding 1–3% grain can restore photographic texture." Generative upscalers can treat grain as noise and strip it, so **upscale first, add grain afterwards** — [seedvr2.ai blog](https://www.seedvr2.ai/blog/upscale-ai-generated-images); [MakeAIPhotos](https://www.makeaiphotos.com/blog/how-to-make-ai-photos-look-realistic/).
- Real sensor noise is heaviest in shadows and at high ISO. Ask for "fine grain at ISO 400" rather than "grainy", which tends to produce a stylized filter — [nat.io](https://nat.io/blog/achieving-photorealism-guide); [BetterPrompt](https://betterprompt.com/image/imperfections).

**Chromatic aberration, vignette, other lens cues**
- Generators suppress chromatic aberration, and its complete absence is itself a giveaway. Keep it to **high-contrast edges**, because uniform CA across the frame looks wrong — [nat.io](https://nat.io/blog/achieving-photorealism-guide); [Sider](https://sider.ai/blog/ai-tools/photorealism-in-ai-images-isn-t-magic_it-s-a-recipe).
- Use a gentle corner falloff, since heavy vignetting looks like an Instagram preset. A frame that is evenly lit corner to corner can read as a composite — [Imagera](https://imagera.ai/blog/make-ai-images-look-natural-2026); [MakeAIPhotos](https://www.makeaiphotos.com/blog/how-to-make-ai-photos-look-realistic/).
- Apply grain, vignette and edge CA as a **final layer**, keep each subtle, and run a checklist before export — [MakeAIPhotos](https://www.makeaiphotos.com/blog/how-to-make-ai-photos-look-realistic/); [Sozee](https://www.sozee.ai/resources/make-ai-photos-real-photography/).
- Prompt-side realism cues include film grain, chromatic aberration, motion blur, visible pores, a named camera/ISO, and "shot on iPhone, grainy" — [Miraflow](https://miraflow.ai/blog/how-to-make-ai-images-look-like-real-photos-prompt-tricks); [Pixova](https://www.pixova.io/blog/how-to-make-ai-images-look-less-like-ai).
- Background on the physical phenomena: [Wikipedia — Vignetting](https://en.wikipedia.org/wiki/Vignetting); [Wikipedia — Purple fringing](https://en.wikipedia.org/wiki/Purple_fringing).

**Sharpening (Lightroom / Camera Raw)**
- Keep Radius near **1.0** (slightly higher only for very high-megapixel files) — [f64 Academy](https://f64academy.com/sharpening-adobe-camera-raw-lightroom/); [RockyNook](https://rockynook.com/article/how-to-sharpen-your-images/).
- Keep **Detail** around **20–30** for portraits so flat skin areas don't get noisy — [Envato Tuts+](https://photography.tutsplus.com/tutorials/adobe-camera-raw-for-beginners-the-detail-tool--photo-2767).
- A starting recipe is **Amount 60, Radius 1.0, Detail 25–50, Masking 40**, previewing the mask with Alt/Option (white = sharpened, black = protected skin) — [RevelRaw 2026](https://revelraw.com/blog/camera-raw-sharpening.html); [Tahquechi](https://blog.tahquechi.com/lightroom-camera-raw-photo-sharpening-guide/).
- In Photoshop Smart Sharpen, use Remove: **Lens Blur** for halo-free sharpening — [Photoshop Training Channel](https://photoshoptrainingchannel.com/sharpen-photos-in-photoshop/).

**Export / JPEG**
- Heavy JPEG compression throws away the detail the upscaler just added. Keep a **PNG master** and deliver as WebP or moderate-quality JPEG — [EveryFreeTool](https://everyfreetool.com/blog/best-free-image-upscalers-2026); [Lovart](https://www.lovart.ai/blog/how-to-upscale-images-ai-bing).
- Inspect at **100% zoom** for artifacts in faces and fine detail before export — [EveryFreeTool](https://everyfreetool.com/blog/best-free-image-upscalers-2026).
- Film-look grading references for Lightroom — [Fstoppers](https://fstoppers.com/lightroom/how-make-digital-photos-look-film-lightroom-691210); [Alik Griffin](https://alikgriffin.com/how-to-edit-like-film/).

### Inferences
- **Upscale before grain** is directly sourced. **Sharpen before grain** is an inference, because sharpening grain amplifies it into "sandpaper".
- A deliberately degraded "phone" JPEG (low quality, heavy chroma noise) is unnecessary for ads. Meta and TikTok re-encode uploads anyway, so a clean high-quality master with subtle monochrome grain survives recompression better than pre-degraded files.
- Avoid over-HDR in two places. In Magnific, high HDR produces blotches and plastic skin (Q1/Q2). In Lightroom, high Clarity, Texture and Dehaze on skin push in the same direction. Grade with gentle tone curves and a slightly imperfect white balance instead of global HDR. The white-balance point is an inference; no source gave numbers.

### Gaps
- No sourced numeric values were found for: synthetic chromatic aberration (pixels of shift), lens distortion percentage, motion blur, white-balance offsets, or a JPEG quality number for final delivery.
- No Snapseed or VSCO preset settings specific to AI avatars were found.
- No named LUTs or Lightroom presets used by top AI-UGC creators were found.
- No Reddit (r/StableDiffusion, r/AIInfluencer) threads with concrete numbers surfaced in search.

## 5. Removing AI artifacts in post (frequency separation, healing, Generative Fill/Remove, Harmonize, eyes/teeth/hands)

### Takeaway
Photoshop 2026 adds AI-assisted fixes. Harmonize (out of beta, pixel layers only) matches light and color for composites, and Generative Fill now offers a choice of models (Firefly, Gemini 3, FLUX.2 Pro). The sources still say faces, hands and text need manual finishing with masks, Clone Stamp, Healing Brush and color matching (a clipped Curves layer or a low-opacity adjustment layer).

### Cited Findings
- **Harmonize** is out of beta. It matches a placed subject's color, light, tone and shadows to the background and works only on pixel layers, not smart objects or adjustment layers — [We and the Color](https://weandthecolor.com/ai-features-in-adobe-photoshop-that-actually-changed-how-i-work-a-designers-field-report/208072); [PhotoshopNews](https://www.photoshopnews.com/2026/03/10/photoshop-2026-biggest-ai-features-changed-design-workflows). Adobe says manual compositing may still be needed: check that the subject is isolated and the light direction matches — [Adobe Help](https://helpx.adobe.com/photoshop/desktop/generative-ai/generative-ai-features-overview.html).
- **Generative Fill model choice**: Firefly (commercially safe), Google Gemini 3 (character consistency), Black Forest Labs FLUX.2 Pro (photoreal + text) — [ThatPainter](https://thatpainter.com/photoshops-2026-ai-rollout-explained-how-to-try-the-new-tools-and-ai-assistant/); [pixel4it](https://pixel4it.com/photoshop-2026-features-guide/); [Adobe Help](https://helpx.adobe.com/photoshop/desktop/generative-ai/generative-ai-features-overview.html).
- For anything with people, "expect additional retouching". Hands and text have "improved but are not solved" — [vhiz.ai](https://vhiz.ai/tools/adobe-photoshop-generative-fill/). For bad output, Adobe advises redrawing the selection, trying another model, and finishing with masks, Clone Stamp, Healing Brush or manual painting — [Adobe Help](https://helpx.adobe.com/photoshop/desktop/generative-ai/generative-ai-features-overview.html).
- **Eyes**: select the iris, prompt for an iris pattern, then refine in Camera Raw — [Glyn Dewis](https://glyndewis.com/blog/ai-eyes-photoshop).
- To blend an AI fill, use a clipped **Curves** layer, plus a global adjustment layer at about **10–15% opacity** — [ImageWork India](https://imageworkindia.com/match-color-generative-fill-lighting-gaps/).
- Sources disagree on version numbering (v26 vs v27) and on Harmonize's release status — [Disruptiv-e](https://www.disruptiv-e.com/article/whats-new-in-photoshop-2026-game-changing-ai-updates-from-adobe-max).

### Inferences
- Order: fix anatomy (eyes, teeth, hands, ears, jewelry, hairline) at the *generation resolution* or right after the first 2x. This follows the "fix faces before upscaling" logic in Q2–Q3. Later fixes on 4K files cost more Generative Fill passes and can mismatch the texture already added.
- Frequency separation is still useful as a manual alternative to AI skin tools. It lets you even out blotchy color on the low-frequency layer without touching the pore texture on the high-frequency layer. This is general retouching practice; no 2026 source was found.

### Gaps
- No 2026 source specifically on frequency-separation settings (Gaussian radius and similar) for AI skin was found.
- No sources specific to fixing AI teeth or hands in 2026 were found beyond the generic Generative Fill advice.
- No details were found on Photoshop's 2026 "Remove tool" behaviour on faces.

## 6. Metadata, provenance and legal/disclosure requirements (C2PA, SynthID, platform AI labels, FTC, EU AI Act Art. 50, Meta/TikTok ad policies, Spain/LatAm)

### Takeaway
- **Provenance:** Google's Nano Banana Pro outputs carry both C2PA Content Credentials (metadata, lost on screenshot or re-encode) and SynthID (a pixel watermark that survives JPEG, resizing and cropping, but is not invulnerable to diffusion re-editing). Meta's "AI info" label is driven mainly by C2PA/IPTC metadata plus self-disclosure.
- **EU:** Article 50 has applied since **2 August 2026**. Deployers must label deepfakes, and the agency or brand using the tool cannot rely on the tool's watermark. A final, voluntary Code of Practice (10 June 2026) asks for at least two machine-readable marks plus visible labels.
- **US:** the FTC's rule (in force since 21 Oct 2024) bans fake testimonials, including AI-generated ones, with penalties of about $53k per violation.
- **Platforms:** TikTok requires an AIGC label or toggle on ads. Meta strictly requires disclosure for political/social ads and auto-labels other ads.
- **Spain:** a national AI bill (approved by the Council of Ministers in May 2026, still in Parliament) adds fines of up to €35M/7%.
- For a legitimate company, the practical answer is disclosure by design, not watermark removal.

### Cited Findings
**C2PA / SynthID technical behaviour**
- Nano Banana Pro images in the Gemini app, Vertex AI and Google Ads include **C2PA metadata**. Google says generated images include both C2PA Content Credentials and a **SynthID** watermark — [C# Corner news](https://www.c-sharpcorner.com/news/google-expands-ai-transparency-with-synthid-detection-in-gemini-c2pa-metadata-for-nano-banana-pro); [Google blog — Nano Banana 2](https://blog.google/innovation-and-ai/technology/ai/nano-banana-2/); [Google Cloud blog](https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-nano-banana).
- A **screenshot drops the C2PA metadata** (it creates a new file), while **SynthID survives** because it lives in the pixels. SynthID is listed as surviving JPEG compression, resizing and cropping. C2PA usually fails through transcoders that strip container metadata — [c2paviewer — verify](https://c2paviewer.com/articles/verify-ai-generated-image-c2pa-synthid); [JammyJar](https://jammyjar.com/blog/c2pa-content-credentials-and-synthid-explained).
- Google DeepMind reports over 100 billion items watermarked with SynthID since 2023. A blog claims OpenAI adopted SynthID in May 2026 (secondary source, unverified) — [c2paviewer — OpenAI/Google](https://c2paviewer.com/articles/openai-google-c2pa-synthid-2026). Another source says SynthID applies only to Google's models, not DALL-E — [nenobanana](https://www.nenobanana.com/blogs/nano-banana-synthid-and-c2pa). These two conflict.
- Academic work: diffusion-based image editing can defeat "robust" watermarks — [arXiv 2603.12949](https://arxiv.org/pdf/2603.12949). Provenance metadata and watermarks can also desynchronize and contradict each other — [arXiv 2603.02378](https://arxiv.org/pdf/2603.02378). Wikipedia cites an October 2026 demonstration of a C2PA signature weakness (single source, unverified) — [Wikipedia — Content Credentials](https://en.wikipedia.org/wiki/Content_Credentials).

**Meta "AI info"**
- Meta's 6 February 2024 announcement named the "AI generated" fields of the **C2PA and IPTC** standards as the signals it reads, covering images from Google, OpenAI, Microsoft, Adobe, Midjourney and Shutterstock. The label is metadata-driven, not a pixel detector, so real photos can also get labelled. It was renamed from "Made with AI" to **"AI info"** in July 2024 — [SignUnder](https://signunder.com/labels/meta); [Versely](https://www.versely.studio/blog/how-meta-decides-to-show-an-ai-label); [AIMetadataCleaner](https://aimetadatacleaner.com/blog/why-instagram-labels-photos-ai-minor-edits-2025).
- **Meta ads**: since 11 January 2024, social-issue, election and political ads must disclose photorealistic images that were digitally created or altered, including a realistic person who doesn't exist. Undisclosed ads are rejected — [Digital Applied](https://www.digitalapplied.com/blog/ai-content-labeling-rules-advertisers-2026-reference); [Political Marketer](https://politicalmarketer.com/meta-rules-for-ai-in-political-ads/).
- For ordinary commercial ads, Meta auto-applies "AI info" for its own generative AI tools when an edit is significant or the ad contains an AI-generated photorealistic human. From June 2026 it reportedly detects third-party AI ads through industry-standard signals, shown in "About this ad" — [Digital Applied](https://www.digitalapplied.com/blog/ai-content-labeling-rules-advertisers-2026-reference). Other blogs claim a broader mandatory self-disclosure for all ads with realistic AI people. One source explicitly says that claim is "not supported by the primary pages" — [AdRiseLab](https://adriselab.com/blog/meta-ads-ai-disclosure-rules-2026); [Novoads](https://novoads.ai/en/blog/ai-ad-label-rules-2026); [Mockingbird](https://www.mockingbirdhouse.com/learning/ai-ad-creative/does-meta-allow-ai-generated-ads). This is unresolved.

**TikTok**
- Ads with fully AI-generated or significantly AI-modified image, video or audio need TikTok's **AIGC label** or the advertiser's own clear disclaimer, caption, watermark or sticker. For non-Spark ads, the advertiser enables the toggle **"This ad contains AI-generated content"** (TikTok ad disclaimer page, last updated September 2025) — [Novoads](https://novoads.ai/en/blog/ai-ad-label-rules-2026); [Cinerads](https://www.cinerads.com/blog/ai-ad-disclosure-requirements); [The Social Outline](https://thesocialoutline.com/blog/ai-ugc-disclosure-rules).
- TikTok's Community Guidelines, in force since **24 September 2026**, "require creators to label AI-generated or significantly edited content that shows realistic-looking scenes or people" — [Oakgen](https://oakgen.ai/blog/ai-influencer-disclosure-rules-by-platform) (best-effort attribution; verify against TikTok's page).

**FTC (US)**
- The Consumer Reviews and Testimonials Rule, **16 CFR Part 465**, has been fully effective since **21 October 2024**. It bans fake or false reviews and testimonials, *including AI-generated ones*, along with bought reviews conditioned on sentiment, undisclosed insider reviews, company-controlled "independent" review sites, review suppression and fake social-media indicators — [Fenwick](https://www.fenwick.com/insights/publications/the-ftc-cracks-down-on-fake-reviews-with-new-rule); [Fourscore Law](https://www.fourscorelaw.com/resources/ftc-bans-fake-reviews-and-testimonials); [Crowell](https://www.crowell.com/en/insights/client-alerts/final-rule-announced-the-ftc-strengthens-its-enforcement-capacity-against-deceptive-reviews-and-testimonials).
- Civil penalties are **$53,088 per violation (2026, inflation-adjusted; $51,744 at launch)**, under a "knew or should have known" standard — [ReviewTactic](https://reviewtactic.com/resources/guides/ftc-rules-fake-paid-reviews/); [Raveneye](https://raveneyeglobal.com/insights/articles/ftc-rule-on-fake-reviews-16-cfr-465-plain-terms/); [Consumer Finance Monitor](https://www.consumerfinancemonitor.com/2024/08/20/ftc-issues-final-rule-to-fight-fake-product-reviews/).
- At the end of 2025 the FTC sent warning letters to nearly a dozen companies — [Legal500](https://www.legal500.com/intelligence/united-states/consumer-protection/five-stars-zero-tolerance-ftc-turns-up-enforcement-under-consumer-review-rule); [FTC warning letter template](https://www.ftc.gov/system/files/ftc_gov/pdf/2025-Fake-Review-Warning-Template.pdf).

**EU AI Act Article 50**
- Article 50 has applied since **2 August 2026** — [artificialintelligenceact.eu](https://artificialintelligenceact.eu/transparency-rules-article-50/); [Orrick, Aug 2026](https://www.orrick.com/en/Insights/2026/08/EU-AI-Act-Transparency-Obligations-for-AI-Generated-Content-Article-50).
- The **Code of Practice on transparency of AI-generated content** is final: it was published 10 June 2026 and is voluntary. Section 1 covers providers' marking and detection duties under Art. 50(2) and requires **at least two machine-readable techniques** (for example signed metadata plus a watermark). Section 2 covers deployers' labelling under Art. 50(4): labels must be "immediately recognisable without user interaction", embedded in the content where possible, and there is an optional EU icon set (Annex I) — [Bird & Bird](https://www.twobirds.com/en/insights/2026/taking-the-eu-ai-act-to-practice-the-final-transparency-code-of-practice); [European Commission FAQ](https://digital-strategy.ec.europa.eu/en/faqs/signing-code-practice-transparency-ai-generated-content); [EC policy page](https://digital-strategy.ec.europa.eu/en/policies/code-practice-ai-generated-content); [Paul Weiss](https://www.paulweiss.com/insights/client-memos/eu-finalises-transparency-rules-for-ai-generated-content); [Lewis Silkin](https://www.lewissilkin.com/insights/2026/07/24/the-eus-new-ai-labelling-rules-what-every-organisation-needs-to-know-102ne35).
- An AI Omnibus proposal reportedly includes "targeted grandfathering" for the Art. 50(2) marking duties. The details could not be confirmed — [Lewis Silkin](https://www.lewissilkin.com/insights/2026/07/24/the-eus-new-ai-labelling-rules-what-every-organisation-needs-to-know-102ne35).
- **Deepfake definition**, Art. 3(60): AI-generated or manipulated image, audio or video that resembles existing persons, objects, places, entities or events and would falsely appear authentic — [Orrick](https://www.orrick.com/en/Insights/2026/08/EU-AI-Act-Transparency-Obligations-for-AI-Generated-Content-Article-50); [NicFab](https://www.nicfab.eu/en/posts/ai-transparency-disclosure/).
- **Evidently artistic, creative, satirical or fictional works** get a lighter regime: they still need disclosure, just one that does not hamper enjoyment of the work. Under the Commission guidelines, a **marketing agency using a third-party tool is a deployer and cannot rely on the tool's watermark**. A brand that only commissions an ad, without deciding how AI is used, is not a deployer. Non-EU deployers are caught if EU use of the output is foreseeable — [McCann FitzGerald](https://www.mccannfitzgerald.com/knowledge/data-privacy-and-cyber-risk/ai-transparency-european-commissions-guidelines-on-article-50-part-2-deployer-obligations); [IP Global Guard](https://ipglobalguard.com/en/blog/ai-act-article-50-guidelines-deepfakes/).

**Spain**
- The Council of Ministers approved Spain's AI bill on 26 May 2026, and it is now in parliamentary processing:
  - Fines range from **€6,000 to €35M or 7% of annual turnover**.
  - Non-consensual sexual deepfakes are banned.
  - Other deepfakes remain legal but **must be identified as AI-generated or altered**.
  - AI texts must show "AI", and fully AI videos must be labelled for their whole duration.
  - Labelling is expected from 2 August, though sanctions depend on the law's entry into force.
  - The supervisor is **AESIA**, and public administrations receive only warnings.

  Sources: [Infobae](https://www.infobae.com/espana/2026/05/26/el-gobierno-aprueba-la-ley-de-ia-multas-de-hasta-35-millones-prohibicion-de-los-deepfakes-sexuales-y-mas-control-sobre-contenidos-manipulados/); [El Español](https://www.elespanol.com/invertia/disruptores/politica-digital/espana/20260527/ley-ia-gobierno-detalle-deepfakes-sexuales-marcas-agua-contenidos-artificiales/1003744260242_0.html); [El Debate](https://www.eldebate.com/sociedad/20260527/ley-ia-prohibira-deepfakes-sexuales-bajo-multas-hasta-35-millones_422000.html); [Deia](https://www.deia.eus/politica/2026/05/26/gobierno-espanol-aprueba-ley-inteligencia-ia-11119163.html); [La Silla Rota](https://lasillarota.com/mundo/2026/5/27/ley-de-inteligencia-artificial-prohibira-deepfakes-sexuales-endurecera-castigos-511943.html); [Alberto Pampín](https://www.albertopampin.es/blog/nueva-ley-de-inteligencia-artificial-en-espana-2026-guia-practica/); [El Día (BO), Jul 2026](https://www.eldia.com.bo/2026-07-12/internacional/espana-impondra-fuertes-multas-por-no-etiquetar-los-contenidos-generados-por-ia.html).

**Brazil / LatAm**
- Brazil's **PL 2338/2023** (AI framework) passed the Senate unanimously on 10 December 2024. As of September 2026 it was still awaiting a vote in the Chamber of Deputies (Special Committee, rapporteur Aguinaldo Ribeiro). Planned fines are up to 2% of Brazilian revenue, capped at R$50M per infraction. Projections put sanction in 2027 and entry into force in 2028–29 — [CASRAI](https://casrai.org/guides/brazil-ai-bill-pl-2338-status); [Desinformante](https://desinformante.com.br/votacao-do-marco-da-ia-fica-para-2026-em-meio-a-impasses-politicos-e-criticas-ao-texto); [IALocus](https://ialocus.com.br/blog/post-pl-2338-marco-legal-ia-brasil-2026.html).

### Inferences
- A photoreal AI "customer" giving a testimonial in a UGC-style ad is the highest-risk use case. In the US it can be a "fake testimonial" under 16 CFR 465 if presented as a real consumer. In the EU it likely triggers Art. 50(4) deepfake labelling when it "would falsely appear authentic". Art. 3(60) refers to resemblance to "existing persons…", and whether an *invented* person qualifies is debated, but the conservative reading is to label. Recommended practice:
  - Visible "AI-generated" / "Imagen generada con IA" labels, or the EU icon.
  - Platform toggles: TikTok AIGC; Meta disclosure where applicable.
  - No claims that the avatar is a real customer.
  - Keep the C2PA manifest intact on masters for auditability.
- Heavy generative post-processing (re-render, Bloom, diffusion upscale) may weaken or desynchronize provenance signals (see the arXiv papers above). That does **not** remove the legal duty: deployer obligations are independent of the tool's watermark (McCann FitzGerald). The client's SOP should therefore add its own disclosure at the export step rather than depend on embedded marks.

### Gaps
- Meta's and TikTok's primary policy pages could not be read directly. Meta's commercial-ad disclosure scope is contested among secondary sources.
- Meta's policy specifically on AI-generated *testimonials* and "people who don't exist" in commercial ads was not found.
- No primary source was found on OpenAI GPT-image C2PA/SynthID behaviour in 2026, or on Adobe Lightroom/Photoshop preserving C2PA on export.
- No LatAm rules beyond Brazil (Mexico, Argentina, Colombia, Chile) and no Brazil CONAR guidance on AI in ads were found.
- No Spanish final text (BOE) was found; the bill was still in Parliament per the sources.

## 7. Typical end-to-end post pipeline (order of operations) used by pro AI-UGC creators/agencies

### Takeaway
No single published "agency SOP" was found. Combining the sourced rules gives the order below: fix the face/anatomy first, then a conservative 2x upscale, a separate low-strength skin pass, optional relight/harmonize, retouch, grade, masked sharpening, grain and lens imperfections **last**, export at platform size from a lossless master, and add disclosure.

### Cited Findings
- **Fix faces before upscaling** — [ComfyLab](https://comfylab.dev/blog/workflows/comfyui-upscale-workflow-ultimate-sd-upscale/).
- **Clean the source before upscaling**, because compression blocks get preserved or amplified — [Lovart](https://www.lovart.ai/blog/how-to-upscale-images-ai-bing); [EveryFreeTool](https://everyfreetool.com/blog/best-free-image-upscalers-2026).
- **Two-stage upscale + skin**: SeedVR2, then SRPO or a skin pass — [MyAIForce](https://myaiforce.com/seedvr2-srpo-upscaling/); [GitHub rik-python](https://github.com/rik-python/Comfyu--Image-detailer-and-skin-detailer-workflows).
- **Downscale to about 0.35 MP before SeedVR2** — [ComfyUI docs](https://docs.comfy.org/tutorials/utility/image-upscale).
- **Test at 2K before 4K** — [seedvr2.net](https://seedvr2.net/blog/tutorials/seedvr2-zimage-4k-upscaling-8gb-vram-2026).
- **Upscale first, then add grain**, since upscalers strip grain — [MakeAIPhotos](https://www.makeaiphotos.com/blog/how-to-make-ai-photos-look-realistic/); [seedvr2.ai](https://www.seedvr2.ai/blog/upscale-ai-generated-images).
- **Grain, vignette and edge CA as the final layer** — [MakeAIPhotos](https://www.makeaiphotos.com/blog/how-to-make-ai-photos-look-realistic/).
- **Check at 100%**, then export a PNG master and a moderate JPEG/WebP for delivery — [EveryFreeTool](https://everyfreetool.com/blog/best-free-image-upscalers-2026).
- **Deployer must label deepfakes**, independent of tool watermarks — [McCann FitzGerald](https://www.mccannfitzgerald.com/knowledge/data-privacy-and-cyber-risk/ai-transparency-european-commissions-guidelines-on-article-50-part-2-deployer-obligations).

### Inferences
Proposed SOP for the client, synthesized from the cited rules above. Numbers are starting points, not vendor presets.

1. **Generate** at native max resolution (about 1–2 MP; Nano Banana Pro at 2K/4K, Flux/Z-Image with an identity LoRA plus a skin LoRA at ≤0.5–0.7). Pick the frame for identity, not detail.
2. **Anatomy/face fix** at base resolution: FaceDetailer/ADetailer denoise ≈0.35–0.45, or Photoshop Generative Fill on eyes, teeth, hands, ears and jewelry. Choose the model per fix (Firefly, Gemini 3 or FLUX.2 Pro).
3. **Optional relight** (Magnific Relight, light-transfer strength low) if the lighting looks "AI-flat". Then Harmonize any composited product.
4. **Upscale 2x conservatively** with one of:
   - SeedVR2 (3B for softer skin, 7B for detail, with a face check);
   - Topaz Redefine Realistic (Subtle), or Creative level 1–2 with texture ≤5;
   - Magnific Precision v2 Photo (sharpen 0–7, grain ≈7, ultra detail ≤30);
   - Krea 2x with low strength and high resemblance;
   - USDU/Flux tile at denoise 0.25–0.35, padding 32–64.
5. **Skin pass**, masked to skin only: Magnific Skin Enhancer Faithful (sharpen 0, grain low, skin detail low-to-mid), or Enhancor Skin Fix (texture slider moderate, avoid Heavy Mode on hero faces). Blend at partial opacity in Photoshop and compare with the identity master.
6. **Optional second 2x** only if the master needs to exceed about 3–4K. Re-check the face at 100%.
7. **Retouch**: healing and Clone Stamp for leftover artifacts (stray hairs, asymmetric earrings, teeth). Even out color blotches with frequency separation or low-opacity adjustment layers.
8. **Grade** in Lightroom/ACR: gentle tone curve, natural saturation, slightly imperfect white balance, no high Clarity/Dehaze/Texture on skin.
9. **Sharpen** for output size: Radius ≈1.0, Detail 20–30, Masking ≥40 so sharpening stays off skin.
10. **Imperfections**, last: monochrome grain (Lightroom Amount ≈18–25, Size ≈24–30, Roughness ≈45–52, or about 1–3% noise), lighter on skin and stronger in midtones; gentle vignette; slight chromatic aberration on high-contrast edges only.
11. **Export**: PNG/TIFF master (keep the C2PA manifest where present, for audit). Deliver at Meta 1440×1800 / 1440×1440 / 1440×2560 or TikTok sizes, as sRGB high-quality JPEG/PNG under the 30 MB Meta limit.
12. **Disclosure**: apply a visible AI label or the EU icon, turn on the TikTok "AI-generated content" toggle, use Meta disclosure where required, and avoid presenting avatars as real customers or testimonials (FTC 16 CFR 465; EU Art. 50(4); Spain bill).

### Gaps
- No primary documentation or interview from a named top AI-UGC agency describing its exact image post pipeline was found. The SOP above is a synthesis of cited component rules, not a copied industry standard.
- No quantitative A/B data was found on whether "real camera" finishing (grain, CA) changes ad performance (CTR/CPA), or on how platform AI labels affect performance.
