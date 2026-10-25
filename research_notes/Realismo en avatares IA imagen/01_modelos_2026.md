# AI image models for ultra-photoreal human avatars (still images), state as of late October 2026

> **Method and reliability note (read first).** Research date: 2026-10-25. In this session WebFetch could not resolve any host (DNS errors), and the egress proxy refused direct curl to artificialanalysis.ai, en.wikipedia.org, lmarena/arena.ai and others. So **every finding below comes from search-engine result snippets and summaries**, not from full pages I read. The shared web-search budget (200 calls per turn) also ran out before I covered every model on the list (see Gaps). Many sources are vendor, reseller or SEO blogs with a commercial interest. Where sources conflict, both are given. Dates are given so stale items can be spotted. Anything released before about late April 2026 is flagged **[>6 months old]**.

---

## 1. Which image models lead photorealism of people in late 2026 (roster, versions, release dates)?

### Takeaway
The frontier changed a lot in 2026. OpenAI's **GPT Image 2.5** (Sunburst/Flare, released Sept 8, 2026) now tops the main preference leaderboards. Google's line is **Nano Banana Pro** (Nov 2025, still the Pro tier) plus the cheaper **Nano Banana 2.1** (Oct 6, 2026). New contenders include **MAI-Image-2.6** (Microsoft), **Grok Imagine Image 2.0** (xAI), **Meta Muse Image**, **Seedream 5.0 Pro**, **Reve 2.0**, **Midjourney V8.2**, **Krea 3** (editing), **Ideogram 4.5** (editing), **FLUX 3 / FLUX 3 Image Klein**, **Qwen-Image-2.1** and **Hy Image 3.5**. Imagen 4 is deprecated. For portrait skin specifically, practitioners and reviewers still split between Nano Banana Pro and GPT Image 2/2.5.

### Cited Findings

**OpenAI**
- GPT Image 2 (`gpt-image-2`) launched in the API and Codex on **April 21, 2026**, and in ChatGPT as "ChatGPT Images 2.0" on April 22, 2026. It has Instant and Thinking modes. Thinking adds web search, layout reasoning, multi-image batching and output verification, and is limited to Plus/Pro/Business/Enterprise — [Interesting Engineering](https://interestingengineering.com/ai-robotics/chatgpt-images-2-0-2k-output); [BuildFastWithAI](https://www.buildfastwithai.com/blogs/chatgpt-images-2-0-gpt-image-2-2026); [MindStudio](https://www.mindstudio.ai/blog/what-is-gpt-image-2)
- GPT Image 2 can return up to 8 coherent images from one prompt while keeping characters consistent — [MindStudio](https://www.mindstudio.ai/blog/what-is-gpt-image-2)
- GPT Image 2.5 was released **September 8, 2026** in ChatGPT, ChatGPT Work, Codex and the API as two models. **Flare** is the default and prioritizes speed. **Sunburst** is slower and gives more precision and control across edits. Reported specs: up to 4K output, up to 16 reference images, new `xhigh` and `max` quality tiers, and up to 50% lower latency than Images 2.0 — [Picsart](https://picsart.com/ai-models/gpt-image-2-5/); [Morphic](https://morphic.com/resources/models/gpt-image-2-5); [Imagine.art](https://www.imagine.art/insights/gpt-image-2-5-overview); [OpenPR press release](https://www.openpr.com/news/4629771/gpt-image-2-5-launches-openai-introduces-flare-and-sunburst)
- Secondary sources say GPT Image 2.5 outputs carry C2PA metadata and an invisible SynthID watermark "from Google DeepMind". **Unverified and unusual for an OpenAI model**, so check it against OpenAI docs — [Morphic](https://morphic.com/resources/models/gpt-image-2-5); [Imagine.art](https://www.imagine.art/insights/gpt-image-2-5-overview)
- GPT Image 1.5 is still listed on Arena as "GPT-Image-1.5-high-fidelity" (#15 on Image Edit at the time of the Qwen-Image-2.1 post, Sept 2026) — [Arena on X](https://x.com/arena/status/2102416020678008986). **[>6 months old; superseded]**

**Google**
- Nano Banana Pro (Gemini 3 Pro Image) was released **Nov 20, 2025** — [TechCrunch](https://techcrunch.com/2025/11/20/google-releases-nano-banana-pro-its-latest-image-generation-model). **[>6 months old]** It became generally available on Google Cloud later; one source dates the GA announcement to May 28, 2026 — [Google Cloud blog](https://cloud.google.com/blog/products/ai-machine-learning/nano-banana-2-and-nano-banana-pro-are-generally-available); [macmyths](https://macmyths.com/google-gemini-3-pro-and-nano-banana-pro-launch-history-current-availability-and-what-changed/)
- Nano Banana 2 (Gemini 3.1 Flash Image) rolled out **Feb 26, 2026** — [Atlas Cloud blog](https://www.atlascloud.ai/blog/tips/best-ai-image-generation-models-2026). **[>6 months old]** Some sources say it shuts down on Oct 29, 2026; TechAIWire says no shutdown date was announced (conflict) — [Unite.AI](https://www.unite.ai/nano-banana-2-1-debuts-at-half-the-image-cost-of-its-predecessor/); [TechAIWire](https://techaiwire.com/articles/nano-banana-2-1-gemini-image-model-half-price/)
- **Nano Banana 2.1** was released **Oct 6, 2026**. It is built on Gemini 3.6 Flash, has model ID `gemini-nano-banana-2.1`, and is GA in the Gemini API, AI Studio and Gemini Enterprise Agent Platform. It also rolled out to the Gemini app, AI Mode in Search, Flow, Stitch and Google Ads — [Unite.AI](https://www.unite.ai/nano-banana-2-1-debuts-at-half-the-image-cost-of-its-predecessor/); [CellCog](https://cellcog.ai/blog/nano-banana-2-1/); [DEV](https://dev.to/alifar/google-nano-banana-21-brings-ga-image-generation-and-editing-to-gemini-2gl1)
- Nano Banana 2.1 adds multi-image fusion for up to 4 characters and 10 objects, search grounding, and fixed tiling artifacts on panoramic aspect ratios at 2K/4K — [Fuser](https://fuser.studio/articles/nano-banana-2-1); [BananaProAI](https://bananaproai.app/blog/nano-banana-2-1)
- The Decoder: 2.1 beats the earlier Pro model on some benchmarks at lower cost, but "in practice, Nano Banana Pro often still produces noticeably better images" — [The Decoder](https://the-decoder.com/googles-new-image-model-nano-banana-2-1-generates-better-images-for-less-money/)
- No "Gemini 3.5 Pro Image" was found. A successor, "Nano Banana 3 Pro" (internal name "Gempix 3 Pro"), reportedly surfaced in Google tooling on Oct 12, 2026. It is a **rumor from a single source**, with a speculative Nov–Dec 2026 window — [bananabanana.pro](https://bananabanana.pro/nano-banana-3-pro)
- **Imagen 4 is deprecated.** The Gemini API says the Imagen 4 standard, ultra and fast endpoints shut down **Aug 17, 2026**, and recommends migrating to Gemini 3.1 Flash Image — [Google AI for Developers](https://ai.google.dev/gemini-api/docs/models/imagen). Vertex AI release notes list `imagen-4.0-ultra-generate-001` as discontinued on Mar 24, 2026; another Google page says June 30, 2026 (conflict) — [Vertex AI release notes](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/release-notes). No Imagen 5 was found — [invideo](https://invideo.io/blog/imagen-ai-image-generator/)

**Microsoft**
- MAI-Image-2.6 and MAI-Image-2.6-Flash: Artificial Analysis says it was announced Aug 10, 2026. The model card lists Aug 14 for 2.6 and Sept 4 for Flash; OpenRouter gives Sept 4 (conflict). It is available in MAI Playground and as a private preview on Microsoft Foundry. Microsoft highlights portraits, photorealism and text rendering, reports +79 Elo over MAI-Image-2.5, and lists about 20B parameters — [MAI-Image-2.6 model card (PDF)](https://microsoft.ai/pdf/MAI-Image-2.6-Model-Card.pdf); [Microsoft Tech Community](https://techcommunity.microsoft.com/blog/azure-ai-foundry-blog/mai-image-2-6-and-mai-image-2-6-flash-quality-and-speed-at-production-scale/4550970); [Artificial Analysis on X](https://x.com/ArtificialAnlys/status/2092284543705456991); [OpenRouter](https://openrouter.ai/microsoft/mai-image-2.6)

**xAI**
- Grok Imagine Image 2.0 shipped **Aug 7, 2026** as "Quality Mode" in Grok Imagine. The API (`grok-imagine-image-2.0`) followed on Aug 11, 2026 — [OrcaRouter](https://www.orcarouter.ai/blog/grok-imagine-image-2-0-quality-mode); [Kie.ai](https://kie.ai/blog/what-is-grok-imagine-image-2-0); [OpenRouter](https://openrouter.ai/x-ai/grok-imagine-image-2.0)

**Meta**
- **Muse Image** launched **July 7, 2026**. It is Meta Superintelligence Labs' first image model (codename "Mango"), free in Meta AI, WhatsApp and Instagram, with paid tiers for heavy use. It is "agentic": it searches the web for grounding and reflects in a chain of thought. It will power advertiser tools in Advantage+ creative — [CNBC](https://www.cnbc.com/2026/07/07/meta-ai-muse-image.html); [Axios](https://www.axios.com/2026/07/07/ai-meta-image-generator); [DataCamp](https://www.datacamp.com/blog/meta-muse-image)

**ByteDance**
- Seedream 5.0 Lite launched Feb 2026 **[>6 months old]**. **Seedream 5.0 Pro** launched **July 8, 2026**, with built-in web search and "deep-thinking" prompt reasoning — [Pexo](https://pexo.ai/blog/what-is-seedream-5-0-pro-5247); [Kie.ai](https://kie.ai/blog/what-is-seedream-5); [Fello AI](https://felloai.com/seedream-5/); [ByteDance Seed blog](https://seed.bytedance.com/en/blog/beyond-generation-it-understands-design-introducing-seedream-5-0-pro)
- ByteDance claims Seedream 5.0 Pro "faithfully reproduces skin texture", with three-dimensional facial lines and rough skin details (vendor claim) — [ByteDance Seed blog](https://seed.bytedance.com/en/blog/beyond-generation-it-understands-design-introducing-seedream-5-0-pro)

**Black Forest Labs (FLUX)**
- The FLUX.2 series (Pro, Flex, Dev, Klein) was announced **Nov 25, 2025** **[>6 months old]** — [Wikipedia: Flux](https://en.wikipedia.org/wiki/Flux_(text-to-image_model)) (via search snippet); [fal.ai FLUX.2](https://fal.ai/flux-2)
- **FLUX 3** was released **July 23, 2026** as a multimodal model (image, video, audio, robot action), with variants FLUX 3 Video, Image, Action and Dev. It is in Early Access, Video came first, and FLUX 3 Image was to follow "in coming weeks". No independent benchmarks at launch — [MarkTechPost](https://www.marktechpost.com/2026/07/26/black-forest-labs-releases-flux-3-a-multimodal-flow-model-for-image-video-audio-and-robot-action-prediction/); [DataNorth](https://datanorth.ai/news/black-forest-labs-releases-flux-3); [TechJack](https://techjacksolutions.com/ai-brief/black-forest-labs-flux-3-multimodal-model-images-video-audio/)
- **FLUX 3 Image Klein**: 5.6B parameters, open weights, released **Oct 15, 2026**. It does text-to-image, editing and multi-reference composition, and needs at least 8GB VRAM with the INT8 build. License is the FLUX Kommunity License, reportedly free commercial use for organizations under $5M annual revenue — [Unite.AI](https://www.unite.ai/new-5-6b-parameter-flux-3-image-klein-debuts-as-open-weights-release/); [Mervin Praison](https://mer.vin/news/flux-3-klein-open-weights-image-model/); [eesel](https://www.eesel.ai/blog/flux-3-klein); [ExplainX](https://explainx.ai/blog/flux-3-image-klein-open-weights-5-6b-guide-2026)

**Midjourney**
- V8.0 was alpha only (Mar 17 to July 24, 2026). V8.1 has been stable since Apr 14, 2026, and **V8.2 has been the default since July 24, 2026** — [Wikipedia: Midjourney](https://en.wikipedia.org/wiki/Midjourney) (via snippet); [Blake Crosley guide](https://blakecrosley.com/guides/midjourney)
- V8 is described as "a deliberate turn toward naturalism", with default output leaning photographic — [Picassoia](https://blog.picassoia.com/midjourney-v8-whats-new-latest-version); [DEV (Oct 2026 comparison)](https://dev.to/paullovelace/6-ai-image-generators-compared-honest-breakdown-october-2026-5gg4)

**Alibaba**
- **Qwen-Image-2.1** was released **Sept 20, 2026**. It has a 7B DiT (32 single-stream layers) and loads an 8B Qwen3-VL encoder. One model does both generation and editing, with native RGBA transparency. Weights are on Hugging Face and ModelScope under a **research-only license** (commercial use needs a separate agreement) — [MarkTechPost](https://www.marktechpost.com/2026/09/21/alibaba-qwen-releases-qwen-image-2-1/); [The Decoder](https://the-decoder.com/alibabas-open-weight-qwen-image-2-1-claims-to-beat-closed-models-in-image-generation-with-just-7-billion-parameters/); [note.com (JP)](https://note.com/ai_driven/n/n02680c93c735?hl=en); [Comfy blog](https://blog.comfy.org/p/qwen-image-21-in-comfyui-open-weight)
- A Qwen-Image-2.0 technical report exists (arXiv, May 2026) — [arXiv 2605.10730](https://arxiv.org/pdf/2605.10730)
- Z-Image-Turbo (Tongyi-MAI, 6B, 8-step distilled) was released 2025-11-26, and the base Z-Image (undistilled, 50-step) on 2026-01-27 **[>6 months old]**. No official "Turbo V2" as of Aug 2026 — [GitHub Tongyi-MAI/Z-Image](https://github.com/Tongyi-MAI/Z-Image); [ComfyUI Wiki](https://comfyui-wiki.com/en/news/2025-11-27-alibaba-z-image-turbo-release); [invideo](https://invideo.io/blog/z-image-ai-image-generator/)

**Tencent**
- **Hy Image 3.5 Preview** (formerly Hunyuan Image) launched **Sept 22, 2026** via Tencent Cloud TokenHub (`hy-image-v3.5-preview`) and the Yuanbao and ima apps. It merges generation and editing, raises reference images from 3 to 20, and is **not open weights** (only 3.0 is open). No "HunyuanImage 4" was found — [CellCog](https://cellcog.ai/blog/hy-image-3-5-preview/); [KuCoin news](https://www.kucoin.com/news/flash/tencent-hunyuan-hy-image3-5-preview-launches-with-20-reference-images-and-4k-output); [AIbase](https://news.aibase.com/news/31258); [AlphaSignal](https://alphasignal.ai/news/tencent-s-hy-image-3-5-merges-generation-and-editing-into-one-model)

**Others**
- **Reve 2.0** launched **June 3, 2026**. It is layout-based (it builds an editable layout before rendering pixels) and was marketed as "the best 4K image model in the world". It placed #2 on the Arena text-to-image board at launch, behind GPT Image 2 — [Digg (Reve X post)](https://digg.com/ai/h1c3pjri); [3D AI Studio](https://www.3daistudio.com/blog/reve-2-4k-image-model-explained); [Decrypt review](https://decrypt.co/371033/reve-2-review-best-ai-image-generator-layout-control)
- **Krea 3** (released Oct 15, 2026) is an in-house **image-editing** foundation model with Fast and Ultra modes. Ultra came out of beta around Oct 19–20. It offers bounding-box regional edits, multi-turn editing and a "trainable" editor — [Krea](https://www.krea.ai/krea-3); [Krea blog](https://www.krea.ai/blog/krea-3-benchmarks); [Artificial Analysis on X](https://x.com/ArtificialAnlys/status/2112577841418428564); [Glitchwire](https://glitchwire.com/news/krea-3-hits-benchmark-second-place-and-ships-the-first-trainable-image-editor/)
- **Ideogram 4.5** (Sept 30, 2026) is a precision **edit** model whose pitch is no artifact buildup over multi-turn edits. Ideogram 4.0 came out June 3, 2026 and is the last version with open weights; 4.5 weights are "soon" — [Ideogram](https://ideogram.ai/models/4.5/); [Ideogram on X](https://x.com/ideogram_ai/status/2105327223431737780); [OrcaRouter](https://www.orcarouter.ai/blog/ideogram-4-5)
- **Bria Fibo 2.0** (8B, open weights) is #1 open-weights on AA-Image-Editing v2.1 and statistically tied with Qwen-Image-2.1 among open models on T2I — [Artificial Analysis on X](https://x.com/ArtificialAnlys/status/2112573259606884640)
- **Higgsfield Soul 2.0** launched Feb 20, 2026 per a Japanese news site (the API lists 02/01/2026; one third-party page says Sept 2026, conflict). It is aimed at fashion and editorial photo realism ("designed to feel shot rather than generated") — [Design Offset (JP)](https://design-offset.com/20260220-higgsfield-soul-v2-0/); [Higgsfield API playground](https://open.higgsfield.ai/models/higgsfield-ai/soul/v2/standard/playground); [Higgsfield Soul intro](https://higgsfield.ai/soul-intro); [Layer](https://layer.ai/models/higgsfield-soul-2). **[>6 months old if Feb date is right]**
- **Adobe Firefly Image Model 5** launched at Adobe MAX in Oct 2025 (public beta) with native 4MP and claims of "lifelike portraits… with anatomic accuracy". It is trained on licensed/Adobe Stock and public-domain content **[>6 months old]** — [Adobe newsroom](https://news.adobe.com/news/2025/10/adobe-max-2025-firefly); [Unite.AI](https://www.unite.ai/adobe-unveils-firefly-image-model-5-with-layered-editing-and-custom-ai-creation/); [Adobe community guide](https://community.adobe.com/p/firefly-image-guide)

### Inferences
- The "realism leader" depends on the measure. **Aggregate preference boards** (which mix all prompt categories) favor GPT Image 2.5. **Portrait-specific hands-on tests** are split, and several favor Nano Banana Pro's "candid/documentary" skin over GPT Image 2.5's glossier "stock photo" look (see section 4). An avatar company should A/B both on its own prompts.
- Nano Banana Pro is **11 months old** but is still Google's Pro tier and is still cited as the most realistic Google model. A Pro successor appears to be imminent but is unconfirmed.
- Krea 3 and Ideogram 4.5 are editing tools, not base-avatar generators. They matter for job (b).

### Gaps
- I could not access official launch posts (openai.com, blog.google, bfl.ai) to confirm specs; all specs come from secondary sources.
- The search budget ran out before I could check **Leonardo Lucid (Origin/Realism), Kling Kolors image, Luma Photon, Runway Gen-4 image/References, Recraft V4, Grok Aurora (legacy), Krea 1 / Krea text-to-image, Wan 2.x image, Seedream 4.5 and Nano Banana 2 detailed specs, and GPT Image 1.5 details**. One search summary mentioned Recraft V4 launching Feb 17, 2026 for design work, but I could not tie it to a specific source.
- No confirmation of whether FLUX 3 Image (non-Klein, closed tier) is generally available as of late October 2026.

---

## 2. What do the leaderboards say (Arena/LMArena, Artificial Analysis), with dates?

### Takeaway
OpenAI dominates every major board. **GPT Image 2.5 Sunburst is #1 and Flare is #2** on Artificial Analysis T2I v2.1 and Editing v2.1, and on all three Arena image boards (T2I, Image Edit, Multi-Image Edit). Below them, **Nano Banana 2.1, MAI-Image-2.6, GPT Image 2, Grok Imagine Image 2.0 and Krea 3 Ultra** cluster closely. The open-weights leaders are **FLUX 3 Image Klein ≈ Qwen-Image-2.1 ≈ Fibo 2.0**. LMArena has rebranded to **Arena (arena.ai)**.

### Cited Findings

**Artificial Analysis, AA-Image-T2I v2.1 (current; snapshot date not shown, appears mid/late Oct 2026)**
- 1. GPT Image 2.5 Sunburst (max), **Elo 1222 ±10** (95% CI 1212–1232, 13,014 samples); 2. GPT Image 2.5 Flare (max) 1207; 3. GPT Image 2 (high) 1186; 4. Nano Banana 2.1 1176; 5. MAI-Image-2.6 1166 — [AA T2I leaderboard](https://artificialanalysis.ai/image/leaderboard/text-to-image); [Layer](https://layer.ai/models/openai-gpt-image-2-5-sunburst)
- Open weights on T2I v2.1: FLUX 3 Image Klein 1043, Qwen-Image-2.1 1042, Fibo 2.0 1039 — [AA T2I leaderboard](https://artificialanalysis.ai/image/leaderboard/text-to-image); [AA on X](https://x.com/ArtificialAnlys/status/2112573259606884640)
- Earlier v2.0 snapshot (around early October; the board was re-anchored in early Sept so FLUX.2 [dev] = 1000): Sunburst 1196, Flare 1190, GPT Image 2 (high) 1171, Grok Imagine Image 2.0 1157. These are not directly comparable to v2.1 — [AA model page](https://artificialanalysis.ai/image/models/gpt-image-2.5-sunburst-2026-09-08); [AA on X (GPT Images 2.5 takes top two)](https://x.com/ArtificialAnlys/status/2098477736746713145)
- At launch (August), MAI-Image-2.6-Preview was #1 on AA Image Editing and #2 on T2I — [AA on X](https://x.com/ArtificialAnlys/status/2092284543705456991)
- Grok Imagine Image 2.0 was reported at #4 on AA at one point — [OrcaRouter](https://www.orcarouter.ai/blog/grok-imagine-image-2-0-quality-mode)

**Artificial Analysis, AA-Image-Editing v2.1**
- 1. GPT Image 2.5 Sunburst (max) 1199; 2. Flare (max) 1182; then MAI-Image-2.6 1151, Krea 3 (Ultra) 1151 and Nano Banana 2.1 1151, a statistical tie for 3rd. Krea 3 Ultra is listed #5 (rank range 3–6) and is the top editor from outside OpenAI, Google and Microsoft — [AA Editing leaderboard](https://artificialanalysis.ai/image/leaderboard/editing); [Krea blog](https://www.krea.ai/blog/krea-3-benchmarks); [AA on X](https://x.com/ArtificialAnlys/status/2112577841418428564)
- Fibo 2.0 is #1 open weights on AA-Image-Editing v2.1 — [AA on X](https://x.com/ArtificialAnlys/status/2112573259606884640)

**Arena (formerly LMArena; arena.ai)**
- Arena: "GPT-Image-2.5-Sunburst is #1 and Flare is #2 across the Text-to-Image Arena, the Image Edit Arena, and the Multi-Image Edit Arena", with significant gains over GPT-Image-2 (medium) — [Arena on X](https://x.com/arena/status/2097400515546255754). A later post says Sunburst is ranked #1 in all three and offers free Direct Mode access for 14 days (one outlet says 72 hours, conflict) — [Arena on X](https://x.com/arena/status/2112199487217434855); [CryptoBriefing](https://cryptobriefing.com/arena-free-openai-sunburst-72-hours/); [The Rundown](https://www.therundown.ai/news/openai-chatgpt-images-2-5-speed-editing-arena)
- Arena single-image edit (Oct 19, 2026 snapshot, 60 models): Sunburst 1514 (preliminary), Flare 1481; Nano Banana 2.1 and MAI-Image-2.6 around 1425–1426; Krea 3 Ultra #8 at 1411 (preliminary, 2,619 votes) — [Arena single-image edit](https://arena.ai/leaderboard/image/image-edit/single-image); [Krea blog](https://www.krea.ai/blog/krea-3-benchmarks)
- Arena multi-image edit: Krea 3 Ultra #4 at 1435±11 (preliminary). Krea: "only surpassed by OpenAI models… the only company valued under $1T in the top-10" — [Krea on X](https://x.com/krea_ai/status/2112567020353102324); [Krea blog](https://www.krea.ai/blog/krea-3-benchmarks)
- Arena T2I scrape dated **Aug 28, 2026** (before GPT Image 2.5): gpt-image-2 (medium) 1381.7, mai-image-2.6-preview 1330.7, Grok Imagine Image 2.0 1315.6 — [BenchmarkList](https://benchmarklist.com/arenas/arena_ai_text_to_image/)
- Qwen-Image-2.1 is #1 open model in Arena Image Edit (1367 pts, #16 overall, 3 pts behind GPT-Image-1.5-high-fidelity at #15) and Text-to-Image (1228 pts) — [Arena on X](https://x.com/arena/status/2102416020678008986)
- Grok Imagine Image 2.0 debuted around #2 on both Arena T2I and Edit at about 1,320 (preliminary) in August — [OrcaRouter](https://www.orcarouter.ai/blog/grok-imagine-image-2-0-quality-mode)
- Reve 2.0 was #2 on Arena T2I at its June launch, with about 1280 from 3,455 votes — [3D AI Studio](https://www.3daistudio.com/blog/reve-2-4k-image-model-explained); [Digg](https://digg.com/ai/h1c3pjri)

**Third-party / community boards (different scales, lower authority)**
- BudgetPixel community arena (Oct 24, 2026; 58,657 votes; 20 models): Flare and Sunburst tied at 1609, Nano Banana 2.1 1547, **Midjourney V8.2 #6** — [BudgetPixel](https://budgetpixel.com/arena/leaderboard)
- LLM Stats (Oct 24, 2026): GPT Image 2 506, Grok Imagine Image 2.0 362, MAI-Image-2.5 257. Its editing board (Oct 8) puts Gemini 3.1 Flash Image first at 2858 — [LLM Stats generation](https://llm-stats.com/leaderboards/best-ai-for-image-generation); [LLM Stats editing](https://llm-stats.com/leaderboards/best-ai-for-image-editing)
- Lumenfall (Oct 11): GPT Image 2 #1 at 1285. Lumenfall editing (Oct 10): Nano Banana Pro #1 at 1250 — [Lumenfall T2I](https://lumenfall.ai/arena/text-to-image); [Lumenfall editing](https://lumenfall.ai/arena/image-editing)
- A prediction market on "which company ranks #1 on Text-to-Image Arena at end of October" shows OpenAI at 89% — [Versus market](https://app.versusapp.com/market/0c6d1295-04b3-415d-bd76-e1f9a58aca4d)

### Inferences
- **Nano Banana Pro does not appear in the AA T2I v2.1 top 5**, even though Nano Banana 2.1 is #4. Practitioner reviews still rate Pro above 2.1 for portraits (section 4), which suggests aggregate Elo is not a reliable proxy for "skin realism of people".
- Midjourney is mostly absent from AA and Arena (no official API). Its only placement found is the community BudgetPixel board (#6).
- These boards rank general prompts, not human portraits specifically. A "photorealistic/people" category filter seems to exist on AA (a URL with `style=general-and-photorealistic` appeared), but I could not read it.

### Gaps
- I could not read the full AA or Arena tables (ranks 6 to 20, Seedream 5.0 Pro, Nano Banana Pro, Midjourney, Reve 2.0, Muse Image, Hy Image 3.5 positions) because both sites were unreachable.
- I could not get the AA **photorealistic / people category** sub-rankings, which would be the most relevant for this client.
- A Hacker News thread titled "A big wtf at the LM Arena scores" exists, which signals community skepticism, but I could not read it — [HN](https://news.ycombinator.com/item?id=49615301).

---

## 3. Max native output resolution, aspect ratios, native vs. upscaled

### Takeaway
True native 4K is offered by **Nano Banana Pro** (1K/2K/4K tiers) and **GPT Image 2.5** (up to 3840×2160, and 3840 px per edge on GPT Image 2 via fal). Native ~4MP comes from **FLUX.2** and **Adobe Firefly 5**. **Native 2K** is the ceiling for Seedream 5.0 (4K via enhancement), Qwen-Image-2.1, Ideogram 4.5, Midjourney V8.2 `--hd`, Grok Imagine 2.0, and Reve 2.0 (2K render upscaled to 4K, disputed). **MAI-Image-2.6 (~1.5K)** and **Higgsfield Soul 2 (1080p)** are lower.

### Cited Findings
- **GPT Image 2:** sources differ. One says up to 2K, with 2560×1440 labeled experimental in OpenAI docs; another lists "2K standard, 4K beta via API". Aspect ratios range from 3:1 to 1:3 — [BuildFastWithAI](https://www.buildfastwithai.com/blogs/chatgpt-images-2-0-gpt-image-2-2026); [Handy AI](https://handyai.substack.com/p/model-drop-gpt-image-2); [Interesting Engineering](https://interestingengineering.com/ai-robotics/chatgpt-images-2-0-2k-output). On fal.ai, both edges must be multiples of 16, max edge 3840 px, aspect ratio up to 3:1, and total pixels between 655,360 and 8,294,400 (about 8.3MP, i.e. 4K UHD) — [fal.ai GPT Image 2](https://fal.ai/models/openai/gpt-image-2)
- **GPT Image 2.5:** max 3840×2160, custom sizes up to 3840 px per edge, quality tiers auto/low/medium/high/xhigh/max, up to 16 reference images per edit — [GlobalGPT](https://www.glbgpt.com/hub/gpt-image-2-5-api-guide/); [ToolColumn](https://www.toolcolumn.com/pricing/gpt-image-pricing); [OpenPR](https://www.openpr.com/news/4629771/gpt-image-2-5-launches-openai-introduces-flare-and-sunburst)
- **Nano Banana Pro:** priced per 1K/2K and 4K tiers ($0.134 vs $0.24), so 4K is a native output tier. Up to 14 reference images; Pro can use up to 6 high-fidelity object references plus up to 5 character-consistency references (other sources say 8, conflict) — [AIFreeAPI](https://www.aifreeapi.com/en/posts/nano-banana-pro-reference-images); [Tech-Insider](https://tech-insider.org/au/how-to-use-nano-banana-pro-2026/); [WaveSpeed](https://wavespeed.ai/blog/posts/google-nano-banana-pro-complete-guide-2026/)
- **Nano Banana 2.1:** 2K and 4K outputs, with panoramic tiling artifacts fixed — [Fuser](https://fuser.studio/articles/nano-banana-2-1); [BananaProAI](https://bananaproai.app/blog/nano-banana-2-1)
- **Seedream 5.0:** the more reliable sources say **native 2K, with 4K via AI enhancement/upscaling**. Pro is "up to 2K native"; Lite supports 2K/3K. Overchat claims native 4K "without external upscaling" (conflict, marketing page) — [Pexo](https://pexo.ai/blog/what-is-seedream-5-0-pro-5247); [Kie.ai](https://kie.ai/blog/what-is-seedream-5); [Overchat](https://overchat.ai/models/seedream-5)
- **FLUX.2 (Pro/Flex/Max/Dev):** up to **4 megapixels** output. Multi-reference up to 10 images on Pro/Flex/Max (other sources say 8) — [fal.ai FLUX.2](https://fal.ai/flux-2); [WaveSpeed](https://wavespeed.ai/blog/posts/flux-2-complete-guide-2026/); [APIMart](https://apimart.ai/model/flux-2)
- **Qwen-Image-2.1:** native 2K, up to 2752×2752 px; up to 10 reference images — [DataNorth](https://datanorth.ai/news/qwen-releases-qwen-image-2-1); [MarkTechPost](https://www.marktechpost.com/2026/09/21/alibaba-qwen-releases-qwen-image-2-1/)
- **MAI-Image-2.6:** maximum output about **1536×1536 total pixel count**; up to 5 input images; 32K-token context — [MAI-Image-2.6 model card](https://microsoft.ai/pdf/MAI-Image-2.6-Model-Card.pdf)
- **Grok Imagine Image 2.0:** 1K or 2K across a range of aspect ratios; up to 5 reference images — [Kie.ai](https://kie.ai/grok-imagine-image-2); [OpenRouter](https://openrouter.ai/x-ai/grok-imagine-image-2.0)
- **Midjourney V8.2:** `--hd` outputs 2048×2048 natively (vs 1024×1024 standard) and bills at 1.5× (about 1.3 vs 0.8 GPU-min). Inpainting/outpainting an HD image drops it back to standard resolution — [Legnext](https://legnext.ai/midjourney/v82); [Tech-Insider](https://tech-insider.org/how-to-use-midjourney-v8-2-2026/)
- **Ideogram 4.5:** native 2K output. Source images up to about 24.2MP can be edited via crop-and-stitch — [Ideogram](https://ideogram.ai/models/4.5/); [Miraheze wiki](https://ai.miraheze.org/wiki/Ideogram_4.5)
- **Reve 2.0:** one profile says it renders 2048×2048 and **upscales** to 4096×4096; another calls 4K "native" (conflict) — [3D AI Studio](https://www.3daistudio.com/blog/reve-2-4k-image-model-explained); [Toolworthy](https://www.toolworthy.ai/tool/reve-2-0)
- **Hy Image 3.5 Preview:** "up to 4096×4096" per one source, "up to 2K" per another (conflict) — [KuCoin](https://www.kucoin.com/news/flash/tencent-hunyuan-hy-image3-5-preview-launches-with-20-reference-images-and-4k-output); [SuperpowerDaily](https://superpowerdaily.com/posts/tencent-releases-hy-image-3-5-preview-with-multi-round-editing-and-4k-output)
- **Higgsfield Soul 2.0:** renders at 720p or 1080p in portrait, square and landscape — [Reel-Stack](https://reel-stack.com/news/higgsfield-soul-2-0-a-photorealistic-ai-image-generator-2026-03-04); [Higgsfield API](https://open.higgsfield.ai/models/higgsfield-ai/soul/v2/standard/playground)
- **Adobe Firefly Image 5:** native 4MP for text-to-image only; the prompt-to-edit model (Generative Fill / Edit) is capped at 2MP — [Lustra AI](https://lustrastudio.co/blog/adobe-firefly-image-model-5-product-photos-4mp-editing); [Adobe newsroom](https://news.adobe.com/news/2025/10/adobe-max-2025-firefly)
- **Krea 3:** a 2K edit completes in under 8 s end to end (vendor claim) — [Krea](https://www.krea.ai/krea-3)

### Inferences
- For a "final 4K hero image of a face", the native options are Nano Banana Pro 4K and GPT Image 2.5 at up to 3840 px. Any 2K-native model (Seedream 5, Qwen, Midjourney, Grok, Ideogram) needs an upscaler for 4K deliverables, and upscalers can introduce their own skin artifacts.
- Midjourney's note that inpainting drops HD back to standard matters for an edit-heavy avatar workflow.

### Gaps
- No primary-source (OpenAI/Google docs) confirmation of exact pixel limits. I could not verify whether Nano Banana Pro's 4K is truly native or internally upscaled (Google docs not reachable).
- Specs for Seedream 4.5, Nano Banana 2, Muse Image, FLUX 3 Image and Klein output resolution were not found.

---

## 4. Characteristic realism failures ("AI tells") per model

### Takeaway
The universal tell is still **plastic or over-retouched skin**, inherited from stock and ad training data. Model-specific patterns reported in 2026:
- GPT Image 2/2.5: "polished / stock-photo / glossy" realism; the old GPT yellow tint is reportedly fixed in 2.x.
- Nano Banana: color drift and darkening across edits; 2.1 has less natural skin than Pro.
- FLUX.2: over-sharp, slightly plastic; legacy "Flux chin".
- Seedream: clean studio and commercial look; 4.0 had plasticky skin.
- Midjourney: aesthetic bias unless `--raw` and low stylize.
- Grok 2.0: good pores, but uneven on production-critical details.
- Reve 2.0: filmic and less glossy, but details turn to mush when zoomed.

Most evidence is small-sample blog testing, not systematic benchmarks.

### Cited Findings
**General**
- Plastic skin is "the single most recognizable tell in an AI portrait", because most models were trained on ad and stock photography that is already retouched (vendor-blog opinion) — [Oakgen](https://oakgen.ai/blog/fix-plastic-skin-ai-portraits)
- Typical "AI sheen": plastic skin, "airport-lounge lighting", dead eyes. Prompt counter-terms used in 2026 include "no beauty filters" and "no AI-perfect sharpness" to push toward a phone-photo look — [Atlas Cloud (Seedream 5 Pro portraits)](https://www.atlascloud.ai/blog/tips/seedream-5-pro-realistic-portraits); [Atlas Cloud prompt guide](https://www.atlascloud.ai/blog/tips/seedream-5-pro-prompt-guide)
- In a September 2026 multi-model test, non-winning models produced "a competent but posed stock-photo smile", and Seedream 5.0 Lite produced smooth skin (snippet; exact source page among the 2026 comparison roundups) — [Melies comparison](https://melies.co/compare/ai-image-models); [TeamDay](https://www.teamday.ai/blog/best-ai-image-models-2026)

**OpenAI GPT Image**
- GPT Image 1.5 had a "well-known warm yellow tint"; vendor pages claim GPT Image 2 "fixes this completely" — [GPTImager](https://gptimager.com/styles/photorealistic); [gpt-image2.art](https://gpt-image2.art/) (vendor claims)
- SeaArt's informal 50-portrait test of GPT Image 2 (harsh studio, window and overcast light) found no yellow or orange tint, and pore-level micro-texture — [SeaArt review](https://www.seaart.ai/blog/gpt-image-2-review)
- MindStudio: GPT Image 2 faces look polished, a slightly "cleaned up" realism — [MindStudio](https://www.mindstudio.ai/blog/gpt-image-2-vs-gemini-image-generation). PixVerse: GPT Image 2 "can look a bit plastic" despite leading rankings (+242 Elo over Nano Banana 2 at launch per that source) — [PixVerse](https://pixverse.ai/en/blog/gpt-image-2-vs-nano-banana-2)
- GPT Image 2.5: in a three-way test all models passed as photos, but GPT Image 2.5 gave the "glossier, more stock photo" result and Nano Banana Pro the most candid, documentary look — [Turbologo](https://turbologo.com/articles/nano-banana-pro-vs-nano-banana-2/). Decrypt praised its skin micro-texture but said "the skin is too smooth, but the overall scenery is very realistic" — [Decrypt](https://decrypt.co/377998/chatgpt-images-2-5-vs-nano-banana-2-review)
- Counter-view: GPT Image 2.5 was "the superior pick for human portraits" with a "very natural photographic feel" vs Nano Banana 2.1 — [DEV](https://dev.to/_bccf48fa79cc929c1634d5/gpt-image-25-vs-nano-banana-21-head-to-head-comparison-of-modern-ai-image-generators-2768). MagicCreator picked Sunburst for photoreal portraits, citing the most complete skin and clothing detail — [MagicCreator](https://magiccreator.ai/posts/gpt-image-2-5-vs-nano-banana-2)

**Google Nano Banana**
- Nano Banana Pro is credited with micro-detail portraits: pores, catchlights, hair strands — [OpenArt](https://openart.ai/blog/best-ai-image-generators-for-realistic-photos/)
- Oakgen's 20-prompt test scored Nano Banana Pro about 9.4–9.5 vs about 7.5–7.8 for GPT Image 2 on skin prompts — [Oakgen](https://oakgen.ai/blog/gpt-image-2-vs-nano-banana-pro)
- Pro beats 2.1 on light and texture in side-lit portraits and gave the closest likeness (face shape, curls, freckles) in a same-person test — [DEV (deepfox)](https://dev.to/deepfox/nano-banana-21-vs-nano-banana-vs-nano-banana-pro-same-prompt-three-generations-1bik); [Fuser](https://fuser.studio/articles/nano-banana-2-1-vs-nano-banana-2-vs-pro)
- Chinese test (302.AI, about 228 days old, so around March 2026): Nano Banana 2 close-ups render pores, blemishes and fine vellus hair, but it is weaker at Chinese text — [302.AI](https://302.ai/blog/302-ai-benchmark-lab-review-on-nano-banana-2-vs-seedream-5/); [Zhihu copy](https://zhuanlan.zhihu.com/p/2010792167879238164)
- Failure modes: Nano Banana "introduces undesirable global color shifts across editing rounds" (10-turn test) — [FreqEdit, arXiv 2512.01755](https://arxiv.org/pdf/2512.01755). One head-to-head found Nano Banana "failed on a fundamental level on anatomy" in a specific test — [Lovart](https://blogs.lovart.ai/flux-vs-nano-banana-ai-image-model-comparison-2026.html)

**FLUX**
- FLUX.2 [max] "becomes a little plastic when you look hard enough… that classic 'over-sharp' look" (snippet from a 2026 blind-style comparison) — [Definition](https://www.thisisdefinition.com/insights/best-ai-image-models)
- "Plastic skin and the Flux chin" were named as Flux's main weaknesses in a post from about 400 days ago (FLUX.1 era), the only source on the chin tell **[old]** — [WeirdWonderfulAI](https://weirdwonderfulai.art/general/flux-plastic-skin-finally-fixed/)

**ByteDance Seedream**
- Seedream defaults toward clean studio looks, which can read as too polished for casual influencer content; it is rated strongest for commercial and product realism — [OpenArt](https://openart.ai/blog/best-ai-image-generators-for-realistic-photos/); [Morphed](https://morphed.app/blog/realistic-ai-image-generator)
- ZenCreator rates **Seedream 4.5 above 5.0 Pro** for photoreal portraits, skin and fabric detail, and says 4.0 had "slightly plastier skin and flatter shadows" — [ZenCreator](https://zencreator.pro/ai-university/guides/seedream-image-complete-guide)
- Chinese reviewers call Seedream 5.0 Pro a "visual production middle platform": good at control, editability and batch delivery, but its photoreal realism is "good, more commercial", weaker than GPT Image 2 and Nano Banana 2 — [CSDN](https://blog.csdn.net/qq_40374604/article/details/163865481); [Zhihu](https://zhuanlan.zhihu.com/p/2058627990901241271)
- WeShop: 5.0 Pro is "less likely to turn close-up faces smooth"; Clipia: wrinkles, stubble and skin tone read as photographic — [WeShop](https://www.weshop.ai/blog/seedream-5-0-pro-review-what-early-tests-reveal/); [Clipia](https://clipia.ai/en/blog/seedream-5-0-pro-review)

**Midjourney**
- Raw mode (now `--raw`; `--style raw` is documented for V5/V6 and works via `--raw` on V7/V8.1/V8.2) removes Midjourney's default aesthetic pass. For photorealism, use stylize 50–150, since high stylize "often adds an artificial quality" — [Prompt Architects](https://prompt-architects.com/blog/91-midjourney-style-raw-2026); [Blake Crosley](https://blakecrosley.com/guides/midjourney); [Geeky Gadgets](https://www.geeky-gadgets.com/midjourney-v8-1-raw-prompt-test/)

**xAI Grok Imagine Image 2.0**
- A hands-on test found correct portrait hand anatomy, pore-level skin, subsurface scattering, and natural catchlight and rim light, but weaknesses "in production-critical areas". Another review said it "did not produce the strongest human-realism result in our test set" — [PicLumen](https://www.piclumen.com/blog/grok-imagine-image-2-0-review/); [OrcaRouter](https://www.orcarouter.ai/blog/grok-imagine-image-2-0-quality-mode)

**Reve 2.0**
- Avoids "the waxy smoothing that used to give AI away", with lens-like shallow depth of field and a filmic, photojournalistic look. Less glossy than Nano Banana 2, but GPT Image 2 keeps "a slight edge" in pure realism (Decrypt). Fine details like lit windows "melt into mush when you zoom in" — [Decrypt](https://decrypt.co/371033/reve-2-review-best-ai-image-generator-layout-control); [Bitkan](https://bitkan.com/news/detail/943789); [Yahoo Tech](https://tech.yahoo.com/ai/deals/articles/reve-2-0-review-best-191133496.html)

### Inferences
- Across 2026 tests, the **direction of failure** differs. GPT Image 2.x errs toward polished, "stock photo" retouching. Nano Banana Pro errs less on skin but drifts in color when editing. Seedream errs toward commercial and studio polish. FLUX.2 errs toward over-sharp and plastic. For UGC-style ads, where "phone-shot, imperfect" is the goal, this argues for Nano Banana Pro or Reve-style candid output, or for adding imperfections with prompts or post-processing, over the glossiest top-Elo model.
- Classic tells from the brief (symmetric faces, perfect teeth, dead eyes, HDR look) were mentioned only generically ("dead eyes", "posed stock smile"). No per-model systematic evidence was found.

### Gaps
- No independent, controlled benchmark of skin, hair or fabric realism per model was found. Everything is small-sample reviews, often vendor-written.
- I could not reach Reddit (r/StableDiffusion, r/nanobanana, etc.), because the search tool blocks reddit.com, so community-reported tells are missing.
- No data on teeth, eye or catchlight artifacts or hand failures per model in 2026 beyond the anecdotes above.

---

## 5. Which models are best at image editing while preserving identity and pixel quality (and which degrade with repeated edits)?

### Takeaway
By **human preference** on single edits, GPT Image 2.5 Sunburst leads, followed by a tie of MAI-Image-2.6, Krea 3 Ultra and Nano Banana 2.1. But for **pixel preservation over many edits**, GPT Image 2.5 drifts the most visibly, because it re-renders roughly 80% of the image on every edit. **Ideogram 4.5** keeps untouched pixels intact. Nano Banana edits locally but gradually shifts color and darkens. Every model degrades over long chains. Best practice is to edit from the original, mask or regionally edit, and restate preservation constraints each turn.

### Cited Findings
- Artificial Analysis gave four frontier editors the same photo and 30 edits in a row. **Ideogram 4.5 kept most of the room intact. GPT Image 2.5 Sunburst drifted most visibly**: it re-renders most of the image on every edit, leaving only about a fifth unchanged, so small colour and detail shifts compound. **Nano Banana 2.1 sat in between**: edits stay local, but the rest of the image shifts slightly and gradually darkens (social-media post, methodology not fully visible) — [Artificial Analysis on X](https://x.com/ArtificialAnlys/status/2108600224478572767)
- Ideogram 4.5: "With each edit, leading models add artifacts, pixel shifts, and color changes. Ideogram 4.5 eliminates artifact buildup." It copies untouched pixels from the source and confines changes to a mask or prompt region. It is live in Ideogram, the API, Higgsfield, Pika and Morphic. It still ranks only around 23rd–24th on general editing preference leaderboards — [Ideogram on X](https://x.com/ideogram_ai/status/2105327223431737780); [Morphic](https://morphic.com/resources/models/ideogram-4-5); [AlphaSignal](https://alphasignal.ai/news/ideogram-4-5-fights-edit-drift-with-27x-pricing-spread-and-multi-turn-precision); [AlphaSignal (Higgsfield)](https://alphasignal.ai/news/higgsfield-brings-ideogram-4-5-to-stop-repeated-edits-from-destroying-images); [OrcaRouter](https://www.orcarouter.ai/blog/ideogram-4-5)
- Banana100 paper: across 100 iterative replications with Nano Banana Pro, "minor artifacts accumulate, rapidly leading to a severe accumulation of visible noise". None of 21 popular no-reference quality metrics consistently scored the degraded images lower, so automated QA cannot be trusted to catch drift — [arXiv 2604.03400](https://arxiv.org/html/2604.03400v1)
- FreqEdit (10 turns): Nano Banana "exhibits strong subject consistency and editing fidelity; however, it introduces undesirable global color shifts across editing rounds" — [arXiv 2512.01755](https://arxiv.org/pdf/2512.01755)
- EdiVal-Agent: GPT-Image-1 held steady over 3 turns while Nano Banana 2 dropped at turn 3 (a different setup from the AA test) — [arXiv 2509.13399](https://arxiv.org/pdf/2509.13399)
- Google's claim that Nano Banana 2.1 improves multi-turn consistency is not independently verified; "improved multi-turn consistency is not the same as repeated edits no longer degrade an image" — [Medium analysis](https://medium.com/@dremfind/gemini-nano-banana-2-1-real-fix-for-image-edit-drift-or-a-minor-refresh-1c6de9612e4c)
- Prompt guides recommend restating preservation constraints every turn and inspecting every result — [Promptessor](https://promptessor.com/compare/gpt-image-vs-nano-banana)
- Krea 3 "changes only what you ask", with bounding-box regional edits, multi-turn editing and a trainable editor. Krea claims it is 4× faster than Nano Banana Pro. Glitchwire reports CPI-Bench 4.81/5, second only to GPT Image 2.5. No independent benchmarks or technical report yet — [Krea](https://www.krea.ai/krea-3); [AGTP on X](https://x.com/AGTPinsights/status/2112593147742306598); [Glitchwire](https://glitchwire.com/news/krea-3-hits-benchmark-second-place-and-ships-the-first-trainable-image-editor/); [EachLabs](https://www.eachlabs.ai/blog/krea-3-out-of-beta-ultra-benchmarks)
- Nano Banana Pro "usually preserves facial identity across edits", which matters for one consistent influencer persona — [OpenArt](https://openart.ai/blog/best-ai-image-generators-for-realistic-photos/); [Reboot/Boss Magazine](https://thebossmagazine.com/post/best-ai-image-models/)
- GPT Image 2.5 Sunburst is positioned for "greater precision and control across edits" (vendor positioning) — [Morphic](https://morphic.com/resources/models/gpt-image-2-5)
- Qwen-Image-2.1 is a unified gen and edit model: up to 10 reference images, edits transparent layers without flattening, and #1 open model on Arena Image Edit — [DataNorth](https://datanorth.ai/news/qwen-releases-qwen-image-2-1); [Arena on X](https://x.com/arena/status/2102416020678008986)
- Hy Image 3.5 Preview adds multi-round editing with up to 20 reference images — [SuperpowerDaily](https://superpowerdaily.com/posts/tencent-releases-hy-image-3-5-preview-with-multi-round-editing-and-4k-output)
- Midjourney V8.2: `--oref` (Omni Reference) is rejected on V8.2 and replaced by the V8.2 Edit model (announced Aug 27, 2026, an "early test"). Inpaint/outpaint on HD drops to standard resolution. One tutorial claims `--oref` still works (conflict) — [Legnext](https://legnext.ai/midjourney/v82); [Reel-Stack](https://reel-stack.com/tools/midjourney); [Tech-Insider](https://tech-insider.org/how-to-use-midjourney-v8-2-2026/)
- A 2026 UGC guide recommends Nano Banana 2 for generating the character, then **FLUX Kontext for preserving the face through outfit and accessory swaps** — [Martini](https://martini.art/en/blog/how-to-build-consistent-ai-character); [Lovart](https://www.lovart.ai/blog/complete-guide-consistent-ai-character-design)
- Firefly Image 5's edit model is capped at 2MP, below its 4MP text-to-image output — [Lustra AI](https://lustrastudio.co/blog/adobe-firefly-image-model-5-product-photos-4mp-editing)

### Inferences
- For **"fix this one thing without touching the rest"** (job b), use a region- or mask-based, pixel-copying editor: Ideogram 4.5, Krea 3 (bounding box), or a mask workflow in ComfyUI with Qwen-Image-2.1 or FLUX. For **"re-imagine this avatar in a new scene with the same identity"**, use GPT Image 2.5 Sunburst or Nano Banana Pro, but restart from the clean master each time rather than chaining edits.
- Because GPT Image 2.5 re-renders the whole frame, skin micro-texture and background pixels are regenerated on every pass. Its top preference rank for single edits does not mean it preserves pixels.

### Gaps
- No controlled identity-similarity metric (e.g., face-embedding cosine across N edits) comparing GPT Image 2.5, Nano Banana Pro and 2.1, Seedream 5, Qwen 2.1 and FLUX 3 Klein was found.
- I could not confirm whether GPT Image 2.5 has an `input_fidelity`-style parameter (GPT Image 1 had one); the search returned nothing.

---

## 6. Access points and approximate cost per image

### Takeaway
Rough per-image cost for a 1K–2K portrait in late 2026:
- Nano Banana 2.1 (~$0.034 at 1K)
- Hy Image 3.5 (~$0.024)
- FLUX.2 Pro (~$0.03/MP)
- Grok 2.0 (from $0.04)
- Seedream 5.0 Pro (~$0.075)
- Nano Banana Pro ($0.134; $0.24 at 4K)
- GPT Image 2/2.5 (token-billed; about $0.21 for 1024² at high/max, about $0.41 at 4K high)

Higgsfield Soul 2 is far cheaper ($0.003–0.006) but capped at 1080p. Most models are on fal.ai, Replicate, OpenRouter and aggregator apps (Higgsfield, Krea, Freepik, OpenArt).

### Cited Findings
- **GPT Image 2 (official):** token-billed, not per image. Reported $8/M image input, $2/M cached image input and $30/M image output tokens. Another source lists $10/$37.50 (conflict). Estimated 1024×1024 high about $0.211, 4K high about $0.41 (also about $0.41 via fal) — [WaveSpeed](https://wavespeed.ai/blog/posts/gpt-image-2-pricing-2026/); [Together AI](https://www.together.ai/models/gpt-image-2); [fal.ai](https://fal.ai/models/openai/gpt-image-2); [ChatlyAI](https://chatlyai.app/blog/gpt-image-2-pricing). Reseller flat rates: $0.03 (1K), $0.05 (2K), $0.08 (4K) at UnificAlly; $0.025–0.05 at APIMODELS; $0.03 flat at APIYI (unofficial) — [UnificAlly](https://unifically.com/blogs/gpt-image-2); [APIMODELS](https://apimodels.app/models/gpt-image-2); [APIYI](https://help.apiyi.com/en/gpt-image-2-vip-size-resolution-complete-guide-en.html)
- **GPT Image 2.5 (official):** Flare and Sunburst have the same rates: $5/M text input, $8/M image input, $30/M image output ($15/M with Batch). Output-only 1024² estimates run from about $0.006 (low) to about $0.211 (max). AA says 2.5 keeps "the same price as GPT Image 2". Also on OpenRouter and ChatGPT, and free on Arena Direct Mode for a limited window — [OpenAI Flare model page](https://developers.openai.com/api/docs/models/gpt-image-2.5-flare); [eesel](https://www.eesel.ai/blog/chatgpt-images-2-5-pricing); [OpenRouter Sunburst](https://openrouter.ai/openai/gpt-image-2.5-sunburst); [AA on X](https://x.com/ArtificialAnlys/status/2098477736746713145); [Arena on X](https://x.com/arena/status/2112199487217434855)
- **Nano Banana Pro (official Gemini API):** about $0.134 per 1K/2K image and $0.24 per 4K image (reported as current on Mar 28 and Oct 20, 2026). Batch is about $0.067 (1K/2K) and $0.12 (4K). fal.ai charges $0.15/image, with 4K at double (about $0.30) — [AIFreeAPI](https://www.aifreeapi.com/en/posts/nano-banana-pro-api-pricing); [Tech-Insider](https://tech-insider.org/au/how-to-use-nano-banana-pro-2026/); [fal.ai NB Pro edit](https://fal.ai/models/fal-ai/nano-banana-pro/edit); [fal.ai NB Pro vs NB2](https://fal.ai/learn/tools/nano-banana-pro-vs-nano-banana-2)
- **Nano Banana 2.1:** 1K about $0.0336 (vs $0.067 for Nano Banana 2). The 4K price conflicts: $0.113 vs $0.0756 — [TechAIWire](https://techaiwire.com/articles/nano-banana-2-1-gemini-image-model-half-price/); [CellCog](https://cellcog.ai/blog/nano-banana-2-1/); [LLM Stats blog](https://llm-stats.com/blog/research/nano-banana-2-1-launch). Nano Banana 2 at 4K on fal: $0.16 — [fal.ai](https://fal.ai/learn/tools/nano-banana-pro-vs-nano-banana-2)
- **FLUX.2 (BFL rates via OpenRouter):**
  - Max: $0.07 first MP + $0.03 per extra MP; references $0.03/MP.
  - Pro: $0.03 first MP + $0.015 per extra MP; references $0.015/MP.
  - Flex: $0.06/MP in and out.
  - fal lists dev $0.012/MP, pro $0.03/MP, flex $0.05/MP, max $0.07/MP.
  - Sources: [OpenRouter FLUX.2 Max](https://openrouter.ai/black-forest-labs/flux.2-max); [OpenRouter FLUX.2 Pro](https://openrouter.ai/black-forest-labs/flux.2-pro); [fal.ai FLUX.2](https://fal.ai/flux-2)
- **FLUX 3 Image Klein:** open weights on Hugging Face (base and distilled), runnable locally/ComfyUI on 8GB VRAM (INT8); FLUX Kommunity License — [Unite.AI](https://www.unite.ai/new-5-6b-parameter-flux-3-image-klein-debuts-as-open-weights-release/); [eesel](https://www.eesel.ai/blog/flux-3-klein)
- **Seedream 5.0:** Pro $0.075/image up to 2.36MP; Lite $0.035 on Replicate. Also on Higgsfield — [Kie.ai](https://kie.ai/blog/what-is-seedream-5); [Higgsfield Seedream 5.0](https://higgsfield.ai/seedream-5.0)
- **Grok Imagine Image 2.0:** from $0.04/image (low/medium tiers); on xAI API, OpenRouter, fal.ai, Venice and Scenario — [OpenRouter](https://openrouter.ai/x-ai/grok-imagine-image-2.0); [fal.ai](https://fal.ai/grok-imagine); [Venice](https://venice.ai/models/grok-imagine-image-2-0); [Scenario](https://help.scenario.com/articles/6027124401-grok-imagine-the-complete-guide-to-ai-generation-and-editing)
- **MAI-Image-2.6:** $8 input / $38 output per M tokens (OpenRouter); Foundry private preview; MAI Playground — [OpenRouter](https://openrouter.ai/microsoft/mai-image-2.6); [Microsoft Tech Community](https://techcommunity.microsoft.com/blog/azure-ai-foundry-blog/mai-image-2-6-and-mai-image-2-6-flash-quality-and-speed-at-production-scale/4550970)
- **Hy Image 3.5 Preview:** $0.024/image on Tencent Cloud API, reference images free. AIbase says about 1.5 cents for a 2K image — [CellCog](https://cellcog.ai/blog/hy-image-3-5-preview/); [AIbase](https://news.aibase.com/news/31258)
- **Ideogram 4.5:** four quality tiers from about $0.008 to $0.22 per image ("27× pricing spread") — [Ideogram](https://ideogram.ai/models/4.5/); [AlphaSignal](https://alphasignal.ai/news/ideogram-4-5-fights-edit-drift-with-27x-pricing-spread-and-multi-turn-precision)
- **Higgsfield Soul 2.0 API:** $0.0032 (720p) and $0.0057 (1080p) per image; commercial use allowed per the FAQ. Soul ID trains a reusable identity from at least 20 photos in about 3 minutes — [Higgsfield API](https://open.higgsfield.ai/models/higgsfield-ai/soul/v2/standard/playground); [Reel-Stack](https://reel-stack.com/news/higgsfield-soul-2-0-a-photorealistic-ai-image-generator-2026-03-04); [Medium](https://mhuzaifariz.medium.com/higgsfield-soul-2-0-81ede0c040da)
- **Midjourney V8.2:** subscription GPU-minutes (`--hd` about 1.3 vs 0.8 GPU-min, 1.5× billing). API access appears only via third-party wrappers (Legnext, EvoLink, Atlas Cloud) — [Legnext](https://legnext.ai/midjourney/v82); [EvoLink](https://evolink.ai/midjourney-v8-2); [Atlas Cloud](https://www.atlascloud.ai/models/midjourney-8.2)
- **Meta Muse Image:** free in the Meta AI app, WhatsApp and Instagram with limits; paid "Meta One" plan (one aggregator says $7.99/mo, unverified); advertisers via Advantage+ creative — [CNBC](https://www.cnbc.com/2026/07/07/meta-ai-muse-image.html); [The Tech Outlook](https://www.thetechoutlook.com/new-release/software-apps/meta-introduces-its-first-image-generation-model-muse-image-now-available-in-meta-ai/)
- **Qwen-Image-2.1:** Hugging Face, ModelScope and ComfyUI native support, but research license — [Comfy](https://comfy.org/qwen-image-2.1); [note.com](https://note.com/ai_driven/n/n02680c93c735?hl=en)
- **Imagen 4:** shut down, no longer an option — [Google AI for Developers](https://ai.google.dev/gemini-api/docs/models/imagen)

### Inferences
- At enterprise scale (thousands of avatars), the price gap between Nano Banana 2.1 (about $0.034) and Nano Banana Pro or GPT Image 2.5 high/max (about $0.13–0.24) is 4–7×. That supports a tiered pipeline: cheap exploration, then a premium model for finals.
- Licensing matters more than price for open models. Qwen-Image-2.1 is research-only, and FLUX 3 Klein is free only under $5M revenue, so a "large company" needs commercial agreements for both.

### Gaps
- Pricing for Krea 3, Reve 2.0, Muse Image (API), Seedream 4.5 and FLUX 3 Image (non-Klein) was not found.
- Pricing and plans on Freepik, Krea, Higgsfield subscriptions, Weavy and OpenArt for these models were not found.

---

## 7. What professional AI-UGC / AI-influencer creators report as their go-to stack for realistic avatar stills in 2026

### Takeaway
Across English, Portuguese and Chinese sources, the **most-recommended model for realistic skin and identity is the Nano Banana line (Pro first, then 2/2.1)**. GPT Image 2/2.5 is the common alternative or co-pick: top of the leaderboards, stronger on text and layout, but sometimes "polished/plastic". Seedream is preferred for polished commercial and product shots. Higgsfield (Soul 2 + Soul ID) is the go-to app layer for UGC creators. For identity, creators save a "master face", use multi-reference models, and run a roster of 3–5 personas. Direct Reddit and practitioner-thread evidence could not be gathered (blocked).

### Cited Findings
- Nano Banana Pro is the most common pick for realistic skin ("remarkably natural" textures, lighting and environments) and usually preserves facial identity across edits. Its downside is cost (15 credits/image on one platform). Seedream 4.5 is seen as strongest for commercial and product realism at 4K, but "too polished" for casual influencer content — [Reboot/Boss Magazine](https://thebossmagazine.com/post/best-ai-image-models/); [OpenArt](https://openart.ai/blog/best-ai-image-generators-for-realistic-photos/); [InfluencerStudio NB Pro vs Seedream 4.5](https://influencerstudio.com/models/compare/nano-banana-pro-vs-seedream-4-5)
- One 2026 realism ranking puts FLUX.2 and Imagen 4 ahead on pure photorealism, with Nano Banana Pro preferred when editing and identity matter. (Imagen 4 has since been shut down.) — [Morphed](https://morphed.app/blog/realistic-ai-image-generator)
- Brazilian Portuguese sources: Nano Banana 2 is the most-cited model for photorealism and skin texture, with character consistency for up to 5 characters and 14 objects. GPT Image 2 leads rankings and is better for text and layouts but "pode parecer um pouco plástico" (can look a bit plastic). An Oct 2026 ranking puts GPT Image 2 API (1172), Nano Banana 2.1 (1160) and Grok Imagine Image 2.0 (1155) on top — [PixVerse](https://pixverse.ai/en/blog/gpt-image-2-vs-nano-banana-2); [Morphic BR](https://morphic.com/br/resources/how-to/nano-banana-2-vs-chatgpt-images-2-0-comparison); [Dreamina PT-BR](https://dreamina.capcut.com/pt-br/ai-image/best-ai-image-generators-for-realistic-images-2026); [Terra](https://www.terra.com.br/byte/nano-banana-gpt-ou-midjourney-saiba-qual-ia-escolher-para-fotos-montagens-e-imagens-do-zero,f3ce1f5d0199726cfc50846b9b52e35br6hs1tme.html)
- Chinese sources (Zhihu, CSDN, 302.AI): the Nano Banana series rates highest for skin; GPT Image 2 is very strong on "photo feel"; Seedream 5.0 Pro is more commercially controllable but less photoreal — [302.AI](https://302.ai/blog/302-ai-benchmark-lab-review-on-nano-banana-2-vs-seedream-5/); [Zhihu](https://zhuanlan.zhihu.com/p/2058627990901241271); [CSDN](https://blog.csdn.net/qq_40374604/article/details/163865481)
- UGC persona practice: a roster of 3–5 AI personas per audience segment or content style, saving a face once and reusing it — [Imagine.art UGC playbook](https://www.imagine.art/blogs/ai-ugc-content-creation-playbook)
- Higgsfield SoulID trains a reusable identity model from reference images, and HeyGen offers similar training. "For static images, Flux or Midjourney with reference inputs is still the cleaner path" (Substack opinion) — [AgentStack Substack](https://agentstackai.substack.com/p/ai-ugc-character-consistency-persistent-creator-persona)
- A September 2026 five-model consistency test: most providers now offer reference-image consistency, but "few of them actually behave the same way when you push them". It names Nano Banana 2 (several references per call) and Qwen-Image-2.1 — [Tech-Insider consistent character test](https://tech-insider.org/consistent-ai-character-generator-test-2026/)
- Workflow recommendation: Nano Banana 2 to generate the character, then FLUX Kontext to keep the face through outfit and accessory swaps — [Martini](https://martini.art/en/blog/how-to-build-consistent-ai-character)
- Higgsfield integrates many third-party models (Seedream 5.0, Ideogram 4.5, Soul 2) — [Higgsfield Seedream 5.0](https://higgsfield.ai/seedream-5.0); [AlphaSignal](https://alphasignal.ai/news/higgsfield-brings-ideogram-4-5-to-stop-repeated-edits-from-destroying-images)
- Local and open-source: guides still recommend SDXL realism checkpoints (RealVisXL, Juggernaut XL) for portrait skin and hair, and Z-Image for "good realism, lower hardware". These are SEO guides, some about a year old — [Cubix](https://www.cubix.co/blog/best-model-for-stable-diffusion/); [Aiarty](https://www.aiarty.com/stable-diffusion-guide/best-stable-diffusion-models.htm); [QWE](https://www.qwe.edu.pl/tutorial/stable-diffusion-best-models-realistic-images/)
- Compliance: an AI avatar giving a fabricated testimonial is not compliant (ad-policy warning in UGC guides) — [Shhots](https://shhots.ai/blog/best-ai-avatar-solutions-for-ugc-product-ads/)
- Video-avatar context (out of scope, noted for pipeline fit): HeyGen Avatar V (Apr 2026) is marketed on identity consistency — [HeyGen](https://www.heygen.com/)

### Inferences (job-by-job recommendation for the client, synthesized from all sections)
- **(a) Base avatar from text:**
  - Shortlist: **Nano Banana Pro** for the most candid, documentary skin, which suits UGC, and **GPT Image 2.5 Sunburst** (#1 on every board, up to 3840 px; watch for the glossy "stock" look).
  - Alternates to test: Midjourney V8.2 with `--raw` and stylize 50–150 for an editorial look (no official API); Higgsfield Soul 2 for a cheap fashion/UGC look (1080p cap); Reve 2.0 for a filmic look; Seedream 5.0 Pro or 4.5 for polished e-commerce.
- **(b) Editing/correcting without losing quality:**
  - Pixel-preserving local edits: **Ideogram 4.5** or **Krea 3** (regional bounding box). Mask-based ComfyUI with Qwen-Image-2.1 or FLUX 3 Klein for in-house work, subject to license.
  - Nano Banana Pro/2.1 for semantic edits that keep identity (watch the color shift and darkening).
  - Avoid long GPT Image 2.5 edit chains. Always edit from the master, never chain.
- **(c) Multi-reference / identity-consistent:**
  - GPT Image 2.5: up to 16 references.
  - Nano Banana Pro: up to 14 references, 5 of them characters. Nano Banana 2.1: 4 characters + 10 objects.
  - Hy Image 3.5: 20 references.
  - Qwen-Image-2.1: 10 references.
  - FLUX.2: 8–10 references.
  - Grok Imagine 2.0 and MAI-Image-2.6: 5 each.
  - Trained identity: Higgsfield Soul ID (≥20 photos).
  - Midjourney V8.2 lost Omni Reference.
- **(d) Native high resolution:** Nano Banana Pro 4K ($0.24) and GPT Image 2.5 (up to 3840×2160) are the only top-tier models with credible native 4K. FLUX.2 and Firefly 5 give native about 4MP. Seedream 5, Qwen-Image-2.1, Midjourney V8.2 and Grok 2.0 are native 2K and need upscaling.

### Gaps
- **Reddit could not be searched** (the tool blocks reddit.com), and the search budget ran out before X/YouTube creator-specific queries and Spanish, Japanese and Russian (Habr) sources. So the "what pros actually use" evidence relies on blogs and comparison sites, many of them vendors (InfluencerStudio, OpenArt, Higgsfield, PixVerse, Morphic).
- No survey-type or quantified data on creator tool share in 2026 was found.
- The often-reported practitioner step of "skin-texture upscaling" (Magnific, Topaz, SeedVR2, Enhancor-type tools) was not verified this session because the search budget ran out.
