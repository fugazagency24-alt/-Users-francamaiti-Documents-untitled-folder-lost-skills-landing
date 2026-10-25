# Fact-check of 2026 AI image-model claims (as of October 25, 2026)

Method note: page fetches outside GitHub were blocked from this environment (DNS failure for openai.com, ai.google.dev, arxiv.org, artificialanalysis.ai, docs.midjourney.com, bfl.ai, ftc.gov, etc.). Primary confirmation was therefore done against **GitHub sources fetched directly** (official OpenAI Python SDK type definitions and changelog, the OpenAI cookbook, the Google Gemini cookbook, Black Forest Labs repos, QwenLM repos, Krea repo, Mi-Ripple repo, and LiteLLM's price/deprecation registry, which cites ai.google.dev pricing). Everything else comes from WebSearch result snippets of official pages (ai.google.dev changelog/deprecations, docs.midjourney.com, artificialanalysis.ai, arena.ai, ftc.gov, lamoncloa.gob.es) or tech press. Where a verdict rests only on search snippets, that is stated.

Verdict key: TRUE / PARTLY TRUE (core right, detail wrong or outdated) / FALSE / UNVERIFIED.

## Claim 1 — OpenAI GPT Image 2 (Apr 21, 2026) and GPT Image 2.5 "Sunburst"/"Flare" (Sept 8, 2026)

### Takeaway
VERDICT: TRUE, with two corrections. gpt-image-2 shipped April 21, 2026 and GPT Image 2.5 shipped September 8, 2026 as two official API models, `gpt-image-2.5-sunburst` and `gpt-image-2.5-flare`. They are in OpenAI's own SDK and cookbook, so the note saying GPT Image 2.5 "appears only in one community tweet" is FALSE. Correction: the 16-reference-image limit and the 3840×2160 ceiling are not new in 2.5. The SDK documents them for every GPT image model (16 images) and for gpt-image-2 too (3840×2160). Only the `xhigh` and `max` quality levels are exclusive to 2.5.

### Cited Findings
- The official SDK's `ImageModel` enum lists `gpt-image-2`, the snapshot `gpt-image-2-2026-04-21`, `gpt-image-2.5-sunburst`, `gpt-image-2.5-sunburst-2026-09-08`, `gpt-image-2.5-flare` and `gpt-image-2.5-flare-2026-09-08`, plus gpt-image-1.5, gpt-image-1, gpt-image-1-mini and chatgpt-image-latest. It marks dall-e-2 and dall-e-3 as "retired on May 12, 2026". — [openai-python image_model.py](https://github.com/openai/openai-python/blob/main/src/openai/types/image_model.py)
- SDK changelog: v3.10.0 (2026-09-08) "add GPT Image 2.5 models and image options"; v2.13.0 (2025-12-16) "gpt-image-1.5". — [openai-python CHANGELOG.md](https://github.com/openai/openai-python/blob/main/CHANGELOG.md)
- The OpenAI cookbook "GPT Image Generation Models Prompting Guide" is dated 2026-04-21 in the cookbook registry. It says "As of April 21, 2026, OpenAI has the following image models available" and calls `gpt-image-2` the "recommended default for new builds". — [openai-cookbook prompting guide](https://github.com/openai/openai-cookbook/blob/main/examples/multimodal/image-gen-models-prompting-guide.ipynb); [cookbook registry.yaml](https://github.com/openai/openai-cookbook/blob/main/registry.yaml)
- Another OpenAI cookbook notebook uses `gpt-image-2.5-flare` and says that "to compare a model optimized for demanding quality requirements, set IMAGE_MODEL to gpt-image-2.5-sunburst". — [openai-cookbook transparent assets notebook](https://github.com/openai/openai-cookbook/blob/main/examples/multimodal/transparent-image-assets-for-campaigns-and-presentations.ipynb)
- Quality levels: `quality: Literal["low","medium","high","xhigh","max","auto",...]`. Per the docstring, `gpt-image-2.5-sunburst` and `gpt-image-2.5-flare`, including their `2026-09-08` snapshots, "also support `xhigh` and `max`". Other GPT image models support low/medium/high. — [openai-python image_generate_params.py](https://github.com/openai/openai-python/blob/main/src/openai/types/image_generate_params.py); [image_edit_params.py](https://github.com/openai/openai-python/blob/main/src/openai/types/image_edit_params.py)
- Resolution: for gpt-image-2 and both 2.5 models, arbitrary `WIDTHxHEIGHT` sizes are allowed if both edges are divisible by 16 and the aspect ratio is between 1:3 and 3:1. "Resolutions above 2560x1440 are experimental, and the maximum supported resolution is 3840x2160." — [openai-python image_generate_params.py](https://github.com/openai/openai-python/blob/main/src/openai/types/image_generate_params.py)
- The cookbook is stricter for gpt-image-2: the maximum edge must be "less than 3840px", total pixels ≤ 8,294,400, and total pixels ≥ 655,360. It calls 3840x2160 an "experimental upper-end target"; if the max-edge rule is enforced literally, round down to e.g. 3824x2144. — [openai-cookbook prompting guide](https://github.com/openai/openai-cookbook/blob/main/examples/multimodal/image-gen-models-prompting-guide.ipynb)
- Reference images: "For the GPT image models (gpt-image-1, gpt-image-1-mini, gpt-image-1.5, gpt-image-2, … gpt-image-2.5-sunburst, … gpt-image-2.5-flare, … chatgpt-image-latest) … You can provide up to 16 images." — [openai-python image_edit_params.py](https://github.com/openai/openai-python/blob/main/src/openai/types/image_edit_params.py)
- Press coverage dated Sept 8, 2026 calls the release "ChatGPT Images 2.5". Flare is the default for most work, with higher quality than GPT Image 2 and ~50% lower latency; Sunburst targets detailed, premium edits and takes longer. — [9to5Mac, 2026-09-08](https://9to5mac.com/2026/09/08/openai-releases-chatgpt-images-2-5-with-sharper-details-and-more-precise-editing/); [DataCamp](https://www.datacamp.com/blog/chatgpt-images-2-5)
- Artificial Analysis says GPT Images 2.5 takes "the top two spots", generates "in less than half the time", and keeps "the same price as GPT Image 2". — [Artificial Analysis on X](https://x.com/ArtificialAnlys/status/2098477736746713145)
- At gpt-image-2's launch, Arena reported it at #1 across all Image Arena boards, with Text-to-Image at 1512, +242 over #2. — [Arena on X](https://x.com/arena/status/2046670703311884548)
- Azure lists `gpt-image-2.5-flare` and `gpt-image-2.5-sunburst` with deprecation date 2027-09-09, and `gpt-image-2`/`gpt-image-2-2026-04-21` with 2027-10-21. — [LiteLLM model registry (Azure rows)](https://github.com/BerriAI/litellm/blob/main/model_prices_and_context_window.json)
- One search snippet said OpenRouter lists gpt-image-2 as released June 24, 2026, which conflicts with April 21. The SDK snapshot name `gpt-image-2-2026-04-21` supports April 21 as the API release. — [WebSearch summary citing OpenRouter, unverified]; [openai-python image_model.py](https://github.com/openai/openai-python/blob/main/src/openai/types/image_model.py)

### Inferences
- "Sunburst = precision/quality, Flare = speed/default" matches OpenAI's cookbook wording and the press. "Precision" and "speed" are paraphrases, not OpenAI's exact labels.
- The total-pixel cap of 8,294,400 equals 3840×2160 exactly, so "4K UHD" output is the ceiling. Anything above 2560×1440 is officially "experimental".
- The dated snapshot `-2026-09-08` confirms the Sept 8, 2026 launch date.

### Gaps
- I could not open openai.com or developers.openai.com to quote the launch blog posts or the per-image price of 2.5. Fal's per-size prices are in the LiteLLM registry, for example Flare low 1024×1024 at $0.00588, but they are reseller prices.

## Claim 2 — `input_fidelity` must be omitted on gpt-image-2 / 2.5; only applies to gpt-image-1 and 1.5

### Takeaway
VERDICT: TRUE for gpt-image-2. UNVERIFIED in the docs for 2.5. One correction: gpt-image-1-mini also accepts `input_fidelity`, but only `low`. The official SDK says "For gpt-image-2, omit this parameter", and the cookbook says it is "Disabled… output is already high fidelity by default". The SDK docstring does not name the 2.5 models either way.

### Cited Findings
- `input_fidelity: Optional[Literal["high","low"]]`: "Supports high and low on gpt-image-1 and gpt-image-1.5; gpt-image-1-mini supports only low. For gpt-image-2, omit this parameter. Defaults to low on supported models." — [openai-python image_edit_params.py](https://github.com/openai/openai-python/blob/main/src/openai/types/image_edit_params.py); the same text appears in the Responses image tool, [openai-python responses/tool.py](https://github.com/openai/openai-python/blob/main/src/openai/types/responses/tool.py)
- Cookbook model table: gpt-image-2 `input_fidelity` is "Disabled. input_fidelity does not work for this model because output is already high fidelity by default"; gpt-image-1.5 and gpt-image-1 take `low`, `high`. — [openai-cookbook prompting guide](https://github.com/openai/openai-cookbook/blob/main/examples/multimodal/image-gen-models-prompting-guide.ipynb)
- Inconsistency inside the same cookbook: a later example cell, "winter evening" billboard edit, still calls `client.images.edit(model="gpt-image-2", input_fidelity="high", …)`. — [openai-cookbook prompting guide](https://github.com/openai/openai-cookbook/blob/main/examples/multimodal/image-gen-models-prompting-guide.ipynb)

### Inferences
- For 2.5, the safe practice is to omit `input_fidelity`. The SDK lists only gpt-image-1, 1.5 and 1-mini as supporting it, and 2.5 belongs to the gpt-image-2 generation. This is an inference, not a documented statement.

### Gaps
- No official text explicitly states the behavior of `input_fidelity` on `gpt-image-2.5-sunburst`/`-flare`. OpenAI's docs site was not reachable.

## Claim 3 — Google Nano Banana family (Pro, 2, 2.1, 2 Lite), shutdown date, reference limits, resolutions, prices

### Takeaway
VERDICT: mostly TRUE, with three corrections.
1. The "Nano Banana 2 API shutdown on Oct 29, 2026" is FALSE/withdrawn. Google's changelog now says gemini-3.1-flash-image is deprecated with "no shutdown date announced".
2. "6 in high fidelity" is not a people limit. Google's cookbook says "up to 14 input images (with up to 6 in high fidelity)". The "up to 5 people" figure is a separate character-consistency figure, so the two notes don't conflict.
3. "Nano Banana 2 is now the Gemini app default" is likely outdated. Nano Banana 2.1 began rolling out in the Gemini app on Oct 6, 2026.

Other points:
- The Gemini app download limits ("1K free / 2K paid, never 4K") are UNVERIFIED and contested.
- Nano Banana 2.1 at ~$0.034 per 1K image is TRUE ($0.0336).
- Pro at $0.24 per 4K image is TRUE.

### Cited Findings
- Google's Gemini cookbook lists the current family:
  - Nano-Banana 2 Lite = `gemini-3.1-flash-lite-image`: "fastest and most cost-effective", includes a free tier.
  - Nano-Banana 2 = `gemini-3.1-flash-image`: aspect ratios 1:8 to 8:1, Search grounding, image grounding, video-to-image.
  - Nano-Banana 2.1 = `gemini-nano-banana-2.1`: "next-generation… enhanced fidelity".
  - Nano-Banana Pro = `gemini-3-pro-image-preview`: thinking, 4K, typography, multi-image composition.
  — [google-gemini/cookbook Get_Started_Nano_Banana.ipynb](https://github.com/google-gemini/cookbook/blob/main/quickstarts/Get_Started_Nano_Banana.ipynb); [cookbook README](https://github.com/google-gemini/cookbook/blob/main/README.md) ("Nano-Banana 2.1: Go bananas with our latest image generation model"); [quickstarts README](https://github.com/google-gemini/cookbook/blob/main/quickstarts/README.md) ("Nano-Banana 2 Lite… our latest and fastest image generation model")
- Nano Banana Pro is Gemini 3 Pro Image (`gemini-3-pro-image-preview`), a public preview released November 20, 2025; maximum 14 images per prompt. — [Vertex AI Gemini 3 Pro Image docs (via search snippet)](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/models/gemini/3-pro-image)
- Nano Banana 2 was officially announced Feb 26, 2026 and replaced Nano Banana Pro as the Gemini app default (Fast/Thinking/Pro modes). It was rolling out free in the Gemini app before the announcement. — [tech-insider.org (German) via search](https://tech-insider.org/de/?p=1705); [Beebom](https://beebom.com/google-gemini-nano-banana-2-rolling-out/amp/)
- Google's model docs list gemini-3.1-flash-image as GA with "Release date: May 28, 2026". The Feb 2026 launch was the `-preview` model. — [Gemini Enterprise Agent Platform: Gemini 3.1 Flash Image (via search)](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/3-1-flash-image); LiteLLM keeps both `gemini/gemini-3.1-flash-image-preview` and `gemini-3.1-flash-image` (Vertex deprecation 2027-05-28), [LiteLLM registry](https://github.com/BerriAI/litellm/blob/main/model_prices_and_context_window.json)
- Nano Banana 2.1, released October 6, 2026: Google's X post says it rolls out "across Gemini App, AI Mode in Search, Google AI Studio, Flow, Stitch, Google Ads, and Gemini Enterprise Platform". — [Google on X](https://x.com/Google/status/2107501209154204148); [The Decoder](https://the-decoder.com/googles-new-image-model-nano-banana-2-1-generates-better-images-for-less-money/); [Search Engine Roundtable](https://www.seroundtable.com/nano-banana-21-google-ai-mode-42246.html)
- The Oct 29 shutdown was withdrawn. The Oct 6, 2026 changelog entry first carried a 2026-10-29 shutdown date, reported by [Mixed News](https://mixed-news.com/en/google-gemini-3-1-flash-image-shutdown-154-days-23-days-notice/). Google withdrew it. The entry "now reads: 'Deprecation announcement: The gemini-3.1-flash-image model is deprecated (no shutdown date announced). Migrate to gemini-nano-banana-2.1'". The deprecations page row is "gemini-3.1-flash-image | May 28, 2026 | No shutdown date announced | gemini-nano-banana-2.1". — [LiteLLM PR #45491](https://github.com/BerriAI/litellm/pull/45491); [Gemini API deprecations page (via search)](https://ai.google.dev/gemini-api/docs/deprecations); [Gemini API changelog (via search)](https://ai.google.dev/gemini-api/docs/changelog)
- Prices (Gemini API list prices as recorded by LiteLLM from ai.google.dev/pricing):
  - Nano Banana 2.1: `output_cost_per_image` $0.0336 (1K).
  - Nano Banana 2 Lite: $0.0336.
  - Nano Banana 2 (Gemini API): $0.045.
  - Pro: $0.134 per 1K/2K image, $120 per 1M image output tokens (`output_cost_per_image_token` 0.00012).
  — [LiteLLM registry](https://github.com/BerriAI/litellm/blob/main/model_prices_and_context_window.json)
- Secondary per-resolution prices for Nano Banana 2.1: ≈$0.0336 (1K), $0.0504 (2K), $0.113 (4K). — [Origami](https://origami.sa/en/blog/nano-banana-2-1-price-per-image/)
- Pro 4K = $0.24 (2,000 output tokens at $120/M) and 1K/2K = $0.134 (1,120 tokens). — [Magic Hour benchmark post](https://magichour.ai/blog/nano-banana-2-vs-nano-banana-pro-we-benchmarked-both-on-the-same-5-prompts); rate per token from the [LiteLLM registry](https://github.com/BerriAI/litellm/blob/main/model_prices_and_context_window.json)
- Reference images: "up to 3 with Nano-Banana 2 Lite, up to 14 with Nano-Banana 2 and Pro, 6 with high fidelity". Also: "Nano-Banana 2 and Nano-Banana Pro can combine up to 14 input images (with up to 6 in high fidelity)". — [google-gemini/cookbook Get_Started_Nano_Banana.ipynb](https://github.com/google-gemini/cookbook/blob/main/quickstarts/Get_Started_Nano_Banana.ipynb)
- The "up to 14 reference images, character consistency for up to 5 people" figure for Pro appears only in secondary sources in this pass. — [CometAPI](https://www.cometapi.com/tag/gemini-3-pro-image-preview/); [Atlas Cloud guide](https://www.atlascloud.ai/blog/guides/nanobanana-14-reference-images-consistency)
- Resolutions: 512px on Nano-Banana 2 Lite and Nano-Banana 2; 1K (default) on all; "2K / 4K: Supported by Nano-Banana 2 and Nano-Banana Pro". Aspect ratios 1:4/4:1 and 1:8/8:1 are only on Nano-Banana 2 and Pro. — [google-gemini/cookbook Get_Started_Nano_Banana.ipynb](https://github.com/google-gemini/cookbook/blob/main/quickstarts/Get_Started_Nano_Banana.ipynb)
- Gemini app downloads: one third-party guide says AI Plus and AI Pro can download up to 2K (2048×2048), with 1K the default, and that 4K is exclusive to AI Ultra. An Adobe Community thread (June 2026) has a user getting 1K files despite choosing 2K, while another user reports 2K working. — [Workalizer](https://workalizer.com/insights/gemini/gemini-ai-image-resolution-daily-limits-integrating-outputs-into-your-google-file-share-workflow/); [Adobe Community thread](https://community.adobe.com/questions-404/2k-resolution-images-is-1k-while-downloading-in-gemini-1631548)

### Inferences
- "Nano Banana 2 is now Gemini app default" was true from late Feb 2026. Since Oct 6, 2026, Nano Banana 2.1 is rolling out in the Gemini app, so the current app default is probably 2.1. No source in this pass states the default explicitly.
- The cookbook's 2K/4K list names only Nano-Banana 2 and Pro, but third-party pricing quotes 4K for 2.1 ($0.113). "2K/4K only on NB2 and Pro" is probably outdated for 2.1.
- "API 4K ≈ 16 MP" holds for a 1:1 4K image (4096×4096 ≈ 16.8 MP). This is arithmetic; the exact 4K pixel dimensions were not retrieved from Google docs.
- The two reference notes are compatible. "14 total / up to 5 people" is Google's launch framing for Pro; "6 in high fidelity" is the cookbook's high-fidelity image limit, which Google's docs apply to object images.

### Gaps
- I could not open blog.google or ai.google.dev to quote the per-category split of the 14 references. Google's API docs historically gave Pro "up to 6 object images with high fidelity, up to 5 human images", but that exact wording was not retrieved.
- No official Google help page was retrieved for Gemini-app download resolutions, so "1K free / 2K paid, never 4K" remains UNVERIFIED. One source contradicts "never 4K" by saying 4K is for Ultra.

## Claim 4 — Imagen 4 deprecated and shut down in the Gemini API on Aug 17, 2026; no Imagen 5

### Takeaway
VERDICT: TRUE (per a snippet of Google's changelog). On June 15, 2026, Google announced that imagen-4.0-generate-001, imagen-4.0-ultra-generate-001 and imagen-4.0-fast-generate-001 would be shut down on August 17, 2026. No evidence of an "Imagen 5" was found.

### Cited Findings
- Gemini API changelog, June 15, 2026: "The following image generation models are being deprecated and will be shut down on August 17, 2026": imagen-4.0-generate-001, imagen-4.0-ultra-generate-001, imagen-4.0-fast-generate-001. — [Gemini API changelog (via search snippet)](https://ai.google.dev/gemini-api/docs/changelog?authuser=1)
- A tracker checked Sept 4, 2026 says the date passed and that Google names gemini-3.1-flash-image as the replacement. — [Kingy AI launch tracker](https://kingy.ai/ai-launch-tracker/google-will-shut-down-three-imagen-4-api-models-august-17/)
- LiteLLM's current registry has no `gemini/imagen-4*` entries and no `imagen-5` entry at all. Only Imagen 3 Gemini rows and a reseller Imagen 4 Ultra row remain. — [LiteLLM registry](https://github.com/BerriAI/litellm/blob/main/model_prices_and_context_window.json)

### Inferences
- The missing Imagen 4 rows in LiteLLM fit the shutdown, but that is not proof.

### Gaps
- "No Imagen 5" rests on absence of evidence: no search hit and no SDK or registry entry. Vertex AI (not the Gemini API) may have a different Imagen 4 timeline, which was not checked.

## Claim 5 — ByteDance Seedream 5.0 (Pro / Flash / Lite) ~July 8, 2026; native 2K, 4K only via upscaling; reference limits

### Takeaway
VERDICT: PARTLY TRUE. Only Seedream 5.0 **Pro** dates to July 8, 2026 (first on Volcano Ark; OpenRouter lists Aug 12). **Lite** came earlier, around Feb 24, 2026 (BytePlus). **Flash** came later, Sept 15, 2026 (OpenRouter lists Oct 1).

Corrections:
- Resolution: Pro tops out at ~2K natively, but **Lite offers native 4K options**, so "4K only via upscaling" is wrong for Lite and unverified for Pro.
- Reference upper bounds (Pro/Flash ≤10, Lite/4.5/4.0 ≤14) are supported by secondary sources citing ByteDance's API reference. The "2–" lower bound is unverified.

### Cited Findings
- Pro: "Released July 8, 2026 by ByteDance's Seed team, first on the Volcano Ark platform". Artlist's help article is "Published: July 8, 2026". OpenRouter lists Aug 12, 2026. — [Artlist help: Seedream 5.0 Pro](https://help.artlist.io/hc/en-us/articles/37481273737757-Seedream-5-0-Pro); [OpenRouter Seedream 5.0 Pro](https://openrouter.ai/bytedance-seed/seedream-5-0-pro); [TestingCatalog](https://www.testingcatalog.com/bytedance-debuts-seedream-5-0-pro-with-advanced-reasoning/)
- Flash: LLM Gateway says released Sept 15, 2026. The BytePlus model ID is `dola-seedream-5-0-flash-260915`. OpenRouter's snapshot is `seedream-5-0-flash-20261001`. — [LLM Gateway](https://llmgateway.io/models/seedream-5-0-flash); [OpenRouter](https://openrouter.ai/bytedance-seed/seedream-5-0-flash-20261001); [LLMReference BytePlus](https://www.llmreference.com/model/seedream-v5-flash/byteplus)
- Lite: BytePlus launched it Feb 24, 2026; Product Hunt listing Feb 26; built on Seedream 4.5 with reasoning and web search. — [ComfyUI.org](https://www.comfyui.org/en/seedream-50-lite-now-available-in); [Hunted/Product Hunt](https://www.hunted.space/product/pixeldance-seaweed/launches/seedream-5-0-lite); [Picsart comparison](https://picsart.com/blog/seedream-5-0-models-comparison/)
- Resolution:
  - Artlist lists 2K as the Pro maximum and 4K for 5.0 Lite.
  - Krea says Pro is "2K-class" and that Lite supports 2K/3K/4K.
  - APIYI lists only 1K/2K presets for Pro.
  - CometAPI says Pro is limited to about 2K.
  - Hedra lists Lite output up to 2160p (4K UHD).
  - Two reseller pages (Zalify, NoteGPT) claim 4K for Pro, which conflicts with the above.
  — [Artlist help](https://help.artlist.io/hc/en-us/articles/37481273737757-Seedream-5-0-Pro); [Krea](https://canvas.krea.ai/models/seedream-5-pro); [APIYI](https://docs.apiyi.com/en/api-capabilities/seedream-image/historical-versions.md); [CometAPI](https://www.cometapi.com/de/models/doubao/seedream-5-0-pro/); [Hedra](https://www.hedra.com/models/image/bytedance/seedream-50-lite); [Zalify](https://zalify.com/ai-models/seedream-5-0-pro)
- Reference limits: ByteDance's image-generation API reference "states that Pro and Flash accept at most 10 reference images while Lite, 4.5, and 4.0 accept 14". Krea and Artlist also say up to 10 for Pro. — [Picsart comparison](https://picsart.com/blog/seedream-5-0-models-comparison/); [Krea](https://canvas.krea.ai/models/seedream-5-pro)
- Pricing is inconsistent across resellers. One lists $0.075 per image up to 2.36 MP and $0.150 above. — [Picsart comparison](https://picsart.com/blog/seedream-5-0-models-comparison/)

### Inferences
- The "4K via upscaling" phrasing probably came from the Pro model's ~2K native cap. For true 4K inside the family, Lite is the variant with native 4K presets.

### Gaps
- No official ByteDance Seed or BytePlus page could be opened, so all dates and limits here are secondary. The "minimum 2 references" lower bound was not found in any source.

## Claim 6 — Black Forest Labs: FLUX.2 family, FLUX 3 (July 23, 2026), FLUX 3 Image Klein (5.6B, Oct 15, 2026), FLUX.2 API reference limits

### Takeaway
VERDICT: mostly TRUE. The FLUX.2 details are confirmed by BFL's GitHub README: [dev] is 32B with a Mistral-Small-3.2-24B-Instruct-2506 text encoder (released Nov 25, 2025); [klein] 4B is Apache-2.0 and 9B is non-commercial (released Jan 15, 2026). FLUX 3 (July 23, 2026) and FLUX 3 Image Klein (5.6B open weights, Oct 15, 2026; BFL GitHub README) are confirmed. For FLUX.2 [pro] references, 8 via API and 10 in the Playground is confirmed by BFL's help center. The "9 MP cap" is UNVERIFIED in official docs; BFL's help center gives 4 MP max output. Nuance: FLUX 3 launched July 23 as a multimodal model (video, audio, robot action). The image product "FLUX 3 Image" arrived Oct 1, 2026.

### Cited Findings
- "[25.11.2025] We are releasing FLUX.2 [dev], a 32B parameter model…". Prompt upsampling uses "the same model we use for text encoding (Mistral-Small-3.2-24B-Instruct-2506)". — [black-forest-labs/flux2 README](https://github.com/black-forest-labs/flux2/blob/main/README.md)
- "[15.01.2026] … FLUX.2 [klein] family". The table lists [klein] 4B and 4B Base under apache-2.0, and [klein] 9B, 9B KV and 9B Base under the FLUX Non-Commercial License. Klein 4B fits in ~8 GB VRAM. — [black-forest-labs/flux2 README](https://github.com/black-forest-labs/flux2/blob/main/README.md)
- The FLUX.2 [pro] API allows up to 8 multi-reference images and the Playground up to 10 (help article last updated June 12, 2026). Max output is 4 MP. — [BFL Help: FLUX.2 technical specifications](https://help.bfl.ai/articles/6944273991-what-are-the-flux-2-technical-specifications)
- FLUX 3, July 23, 2026: one multimodal model trained jointly on image, video, audio and robot actions; video up to 20 s with synchronized audio; FLUX 3 Video/Action in early access at launch. — [MarkTechPost, 2026-07-26](https://www.marktechpost.com/2026/07/26/black-forest-labs-releases-flux-3-a-multimodal-flow-model-for-image-video-audio-and-robot-action-prediction/); [TechTimes, 2026-07-25](https://www.techtimes.com/articles/321552/20260725/flux-3-launches-black-forest-labs-enters-video-audio-physical-ai-one-model.htm)
- FLUX 3 Image launched Oct 1, 2026, with JSON bounding-box layouts and pixel-locked editing. — [TechTimes, 2026-10-02](https://www.techtimes.com/articles/328502/20261002/black-forest-labs-launches-flux-3-image-json-bounding-boxes-lock-unchanged-pixels-numerically.htm)
- FLUX 3 Image Klein README: "the 5.6B open weights image model… text-to-image, editing with up to 10 reference images, and layout control with bounding boxes".
  - Distilled variant: 16 steps. Base: 50 steps, CFG 4. Resolution up to 4K.
  - License: FLUX Kommunity License. The prompt upsampler (a 9B VLM fine-tuned from Qwen3.5-9B) is Apache 2.0 and "required".
  - [black-forest-labs/flux-3-image-klein README](https://github.com/black-forest-labs/flux-3-image-klein/blob/main/README.md)
- Press release dated Oct 15, 2026: open-weights release of FLUX 3 Image Klein. Coverage says it runs on 8 GB GPUs, with free commercial licensing under $5M revenue. — [GlobeNewswire, 2026-10-15](https://www.globenewswire.com/news-release/2026/10/15/3381905/0/en/black-forest-labs-expands-access-to-frontier-visual-intelligence-with-open-weights-release-of-flux-3-image-klein.html); [Unite.AI](https://www.unite.ai/new-5-6b-parameter-flux-3-image-klein-debuts-as-open-weights-release/)
- A secondary guide claims a combined 9 MP input+output budget for FLUX.2 pro editing. Not found in official BFL text. — [WebSearch summary of promptzone guide, unverified](https://www.promptzone.com/deepa_morales/flux2-online-high-speed-ai-image-generation-unveiled-4mo5.md)

### Inferences
- "FLUX 3 released July 23, 2026" is right for the FLUX 3 platform/model. For still images specifically, the dates that matter are Oct 1 (FLUX 3 Image) and Oct 15 (Klein open weights).

### Gaps
- FLUX.2 [pro]/[flex]/[max] launch dates were not re-verified from a BFL source in this pass; only [dev] and [klein] came from the GitHub README. The 9 MP figure remains unverified.

## Claim 7 — Midjourney V8 / V8.1 / V8.2 (V8.2 default since July 24, 2026), --hd native 2K, --raw, --oref unsupported on V8.x

### Takeaway
VERDICT: TRUE for V8.2 becoming the default on July 24, 2026 (Midjourney X post and the docs Version page). TRUE for --hd rendering natively at 2K and for --raw being available on V8.x. PARTLY OUTDATED on --oref. The `--oref` parameter is still V7-only (on a V8 job it silently renders in V7). However, since Aug 27, 2026, the V8.2-era **Edit Model** (compatible with V8.1/V8.2) officially replaces Omni Reference and Character Reference and takes up to 4 reference images.

### Cited Findings
- "We're releasing V8.2 today and making it the default model on Midjourney… aesthetics, personalization, and image quality." — [Midjourney on X](https://x.com/midjourney/status/2080781271043911807)
- Version docs: "The current default Midjourney version is V8.2. V8.2 released as the default version on July 24, 2026." — [docs.midjourney.com Version (via search)](https://docs.midjourney.com/hc/en-us/articles/32199405667853-Version)
- V8.1 became the default, replacing V7. With HD mode, V8.1 renders "at twice the size and 4x the resolution of V7 images". The date is reported as June 10 or June 11, 2026. — [Midjourney Updates: V8.1 is now the default model](https://updates.midjourney.com/v8-1-is-now-the-default-model); [Blake Crosley guide](https://www.blakecrosley.com/guides/midjourney); [VidMuse](https://vidmuse.ai/blog/midjourney-v8-1-review)
- V8 launched in March 2026 (alpha). V8.1 arrived April 14 (secondary). — [CometAPI](https://www.cometapi.com/midjourney-v8/); [The Decoder](https://the-decoder.com/midjourney-v8-rolls-out-with-5x-faster-generation-but-charges-4x-more-for-its-best-features/)
- "A new --hd mode renders images natively at 2K resolution", plus --q 4. — [The Decoder](https://the-decoder.com/midjourney-v8-rolls-out-with-5x-faster-generation-but-charges-4x-more-for-its-best-features/)
- --oref/--ow are accepted on V8 jobs but annotated "(Uses V7)". Omni Reference, Character Reference, multi-prompts, Quality, Niji and Turbo are listed as unsupported on V8.1. — [Blake Crosley, V8 vs V7](https://blakecrosley.com/blog/midjourney-v8-vs-v7-prompt-anatomy); [Blake Crosley guide (--hd, --raw, --oref)](https://www.blakecrosley.com/guides/midjourney); [TechJack](https://techjacksolutions.com/ai-tools/midjourney/midjourney-v8/)
- Edit Model docs: it generates new images from up to four reference images and "replaces Omni Reference and Character Reference". Public testing began Aug 27, 2026; compatible with V8.1 and V8.2; no Remix and no --tile. — [docs.midjourney.com Edit Model (via search)](https://docs.midjourney.com/hc/en-us/articles/48495453462797); [Miraflow guide](https://miraflow.ai/blog/midjourney-v8-2-edit-model-guide-prompts-2026)

### Inferences
- For identity consistency on V8.x, the current official path is the Edit Model, not `--oref`. Notes that say "no reference support on V8" are outdated after Aug 27, 2026.

### Gaps
- The official docs pages were seen only through search snippets. The V8.1 release date (April 14) is secondary.

## Claim 8 — Qwen-Image-2.1 (Sept 20, 2026; 10 references; research-only license); Qwen-Image-2512 and Qwen-Image-Edit-2511 exist

### Takeaway
VERDICT: TRUE (all from QwenLM's GitHub). Extra details:
- 7B visual-generation DiT with a Qwen3-VL 8B text encoder.
- Turbo (8-step) checkpoint plus Pro/Turbo APIs on Oct 9, 2026.
- Qwen-Image-2512 released Dec 31, 2025; Qwen-Image-Edit-2511 released Dec 23, 2025.
- Qwen-Image-2.0 launched Feb 10, 2026.

### Cited Findings
- "2026.09.20: We released Qwen-Image-2.1!" Weights on HF and ModelScope; Day-0 support in Diffusers (`QwenImage21Pipeline`), ComfyUI, vLLM-Omni, SGLang, LightX2V and OpenVINO. — [QwenLM/Qwen-Image-2.1 README](https://github.com/QwenLM/Qwen-Image-2.1/blob/main/README.md)
- "With just 7B parameters in its visual generation component (32 Single-Stream DiT layers)". "Support up to 10 reference images". "Text Encoder: Qwen3-VL 8B". — [QwenLM/Qwen-Image-2.1 README](https://github.com/QwenLM/Qwen-Image-2.1/blob/main/README.md)
- "This repository is licensed under the Qwen Research License Agreement." — [QwenLM/Qwen-Image-2.1 README](https://github.com/QwenLM/Qwen-Image-2.1/blob/main/README.md)
- "2026.10.09: We released Qwen-Image-2.1-Turbo… 8 denoising steps" and "Qwen-Image-2.1 Pro and Turbo APIs are now officially live" (Alibaba Cloud Model Studio). — [QwenLM/Qwen-Image-2.1 README](https://github.com/QwenLM/Qwen-Image-2.1/blob/main/README.md)
- News entries: "2025.12.31: We released Qwen-Image-2512 weights", "2025.12.23: We released Qwen-Image-Edit-2511 weights", "2026.02.10: We are launching Qwen-Image-2.0" (native 2K, unified generation and editing). — [QwenLM/Qwen-Image README](https://github.com/QwenLM/Qwen-Image/blob/main/README.md)

### Inferences
- "Research-only" matches the license name. The license terms themselves (commercial thresholds) were not read.

### Gaps
- The full text of the Qwen Research License (whether commercial use is barred or capped) was not reviewed.

## Claim 9 — Other 2026 releases (Microsoft, xAI, Meta, Reve, Krea, Ideogram, Tencent, Higgsfield, Adobe)

### Takeaway
VERDICT: mostly TRUE on dates, with corrections:
- MAI-Image-2.6 first appeared Aug 10, 2026 (Arena); Microsoft Foundry/API availability Sept 4, 2026.
- Krea 2 is listed as **12B** parameters (released June 22, 2026), not 12.9B.
- Krea 3 (Oct 15, 2026) is a closed **beta**.
- Higgsfield Soul 2.0 dates to Feb 20, 2026.
- Adobe Firefly Image 5 was unveiled Oct 28, 2025 (public beta), not in 2026.

### Cited Findings
- **MAI-Image-2.6:** DataLearner gives Aug 10, 2026 as first public and Sept 4 for Foundry/Azure. OpenRouter snapshot `mai-image-2.6-20260904`. It reached #2 on Arena behind GPT-Image-2, +79 Elo over MAI-Image-2.5. Up to 5 reference images (OpenRouter). A Flash variant is in public preview. — [Windows Report](https://windowsreport.com/microsoft-releases-mai-image-2-6-surges-to-no-2-on-arena/); [OpenRouter](https://openrouter.ai/microsoft/mai-image-2.6-20260904); [DataLearner](https://www.datalearner.com/ai-models/pretrained-models/mai-image-2-6); [Digg/Neowin](https://digg.com/tech/wbv2epcs)
- **Grok Imagine Image 2.0:** released Aug 7, 2026 as a Quality Mode in the Grok apps. Up to 5 references, Magic Wand regional edit. xAI-reported Elo: 1,439 edit, 1,320 T2I. OpenRouter snapshot 20260811. — [ETV Bharat](https://www.etvbharat.com/en/technology/xai-grok-imagine-image-2-launch-features-enn26081002584); [DataNorth](https://datanorth.ai/news/spacexai-releases-grok-imagine-image-2-0); [OpenRouter](https://openrouter.ai/x-ai/grok-imagine-image-2.0-20260811)
- **Meta Muse Image:** launched July 7, 2026 as the first image model from Meta Superintelligence Labs. In Meta AI, Instagram effects and WhatsApp; multi-reference; works with Muse Spark. — [Bloomberg Law](https://news.bloomberglaw.com/tech-and-telecom-law/meta-debuts-ai-image-generation-model-inside-chatbot-instagram); [AdNews](https://www.adnews.com.au/news/meta-launches-muse-image-generation-model); [QNA, 2026-07-08](https://qna.org.qa/en/News-Area/News/2026-7/8/meta-launches-new-ai-image-generator)
- **Reve 2.0:** launched June 3, 2026. Layout-first, native 4K, #2 on Arena T2I behind GPT Image 2 at launch. — [3D AI Studio explainer](https://www.3daistudio.com/blog/reve-2-4k-image-model-explained); [Design Arena notes](https://notes.designarena.ai/reve-2-0-establishes-reve-as-the-top-independent-foundation-image-model-lab/)
- **Krea 2:** open weights (Raw and Turbo), "Diffusion Transformer with 12 billion parameters", release date June 22, 2026 per the HF model cards, Krea 2 Community License. The official GitHub repo confirms the Raw/Turbo split and community license but gives no parameter count. — [dev.to summary of HF cards](https://dev.to/damogallagher/krea-releases-krea-2-as-open-weights-for-image-generation-13pe); [krea-ai/krea-2 README](https://github.com/krea-ai/krea-2/blob/main/README.md)
- **Krea 3:** an image-editing model that opened in beta on Oct 15, 2026. 2K edits in under 8 s; $0.03 per 1K edit and $0.06 per 2K edit; up to 6 references; API only for beta workspaces. — [TestingCatalog](https://testingcatalog.com/krea-launched-krea-3-for-fast-and-precise-image-editing); [AlphaSignal](https://alphasignal.ai/news/krea-launches-krea-3-to-edit-2k-images-71-cheaper-than-gpt)
- **Ideogram 4.5:** live Sept 30, 2026 (secondary). Closed model focused on precise editing (masks, up to 4 references). API ID `ideogram-4-5`. — [OrcaRouter](https://www.orcarouter.ai/fr/blog/ideogram-4-5-launch-precise-edit-model); [Gradually](https://www.gradually.ai/en/ai-models/ideogram-4-5/)
- **Tencent Hy Image 3.5 Preview:** launched Sept 22, 2026 and added to ComfyUI partner nodes the same day. API ID `hy-image-v3.5-preview`. Sources conflict on references (5 vs 20) and resolution (2K vs 4K). — [ComfyUI Wiki, 2026-09-22](https://comfyui-wiki.com/fr/news/2026-09-22-tencent-hy-image-3-5-preview); [OpenRouter](https://openrouter.ai/tencent/hy-image-v3.5-preview-20260922); [Arabian Post](https://thearabianpost.com/tencent-rolls-out-hy-image-3-5-preview/)
- **Higgsfield Soul 2.0:** released Feb 20, 2026, the first update since Soul 1.0 in June 2025, with Soul ID for character consistency. — [Design Offset](https://design-offset.com/20260220-higgsfield-soul-v2-0/); [Higgsfield Soul intro](https://higgsfield.ai/soul-intro)
- **Adobe Firefly Image 5:** unveiled at Adobe MAX on Oct 28, 2025, with native output up to 4 MP and layers support. Adobe Japan's press PDF calls it a public beta. — [TechCrunch, 2025-10-28](https://techcrunch.com/2025/10/28/adobe-firefly-image-5-brings-support-for-layers-will-let-creators-make-custom-models/); [Adobe press PDF](https://news.adobe.com/ja/news/downloads/pdfs/2025/10/20251028-adobe-firefly-delivers-all.pdf)

### Inferences
- Several "#2 behind GPT Image 2 on Arena" claims (MAI-Image-2.6, Grok Imagine 2.0, Muse Image, Reve 2.0) are each a launch-time snapshot. They are not all true at once, and since Sept 8 both GPT Image 2.5 variants sit above them.

### Gaps
- The 12.9B figure for Krea 2 was not found anywhere; 12B is what was found. The Firefly Image 5 general-availability date was not found. Ideogram's own launch post was not retrieved.

## Claim 10 — Leaderboards (Artificial Analysis T2I top-5 and editing; Arena; AA "30-edit" test)

### Takeaway
VERDICT: TRUE for the current Artificial Analysis AA-Image-T2I **v2.1** board: Sunburst (max) 1222, Flare (max) 1207, GPT Image 2 (high) 1186, Nano Banana 2.1 1176, MAI-Image-2.6 1166. TRUE that Arena (LMArena renamed to "Arena"/arena.ai on Jan 28, 2026) ranks Sunburst #1. TRUE for the AA 30-edit test: Ideogram 4.5 preserved the scene best and GPT Image 2.5 Sunburst drifted most. Caveat: Elo values move between snapshots and board versions. Earlier v2.0 figures (Sunburst 1197, Flare 1191, MAI-Image-2.6 1151) circulate and explain the conflicting notes.

### Cited Findings
- AA-Image-T2I v2.1 (official page, per search snippet): 1. GPT Image 2.5 Sunburst (max) 1222 (95% CI 1212–1232; 13,014 samples), 2. Flare (max) 1207, 3. GPT Image 2 (high) 1186, 4. Nano Banana 2.1 1176, 5. MAI-Image-2.6 1166. Open-weights leaders: FLUX 3 Image Klein 1043, Qwen-Image-2.1 1042, Fibo 2.0 1039. — [Artificial Analysis T2I leaderboard](https://artificialanalysis.ai/image/leaderboard/text-to-image)
- AA-Image-Editing v2.1: Sunburst 1199, Flare 1182 at the top. — [Artificial Analysis editing leaderboard](https://artificialanalysis.ai/image/leaderboard/editing)
- Earlier or alternate snapshots:
  - AA-Image-T2I v2.0 captured Oct 6, 2026: Sunburst 1197, Flare 1191, MAI-Image-2.6 5th at 1151, Nano Banana 2 6th at 1125, Nano Banana 2.1 not yet listed.
  - A capture on Oct 16 put Sunburst at 1218.
  - Another post put Nano Banana 2.1 4th on both boards at 1160.
  - The Sunburst model page shows ~1197.57 on the older board.
  — [OrcaRouter NB 2.1 vs GPT Image 2.5](https://www.orcarouter.ai/es/blog/nano-banana-2-1-vs-gpt-image-2-5); [OrcaRouter NB 2.1 rank](https://www.orcarouter.ai/blog/nano-banana-2-1-artificial-analysis-rank); [AA model page](https://artificialanalysis.ai/image/models/gpt-image-2.5-sunburst-2026-09-08)
- Arena text-to-image, snapshot dated Oct 7, 2026: GPT-Image-2.5 Sunburst #1 at 1425±7, Flare #2 at 1398±7 (6.6M votes, 82 models). Arena's X post says Sunburst is "#1 in the Text-to-Image Arena, the Image Edit Arena, and in the Multi-Image Edit Arena". — [arena.ai T2I leaderboard](https://arena.ai/leaderboard/image/text-to-image); [Arena on X](https://x.com/arena/status/2112199487217434855)
- LMArena rebranded to "Arena" (arena.ai) on Jan 28, 2026. — [Arena blog: LMArena is now Arena](https://arena.ai/blog/lmarena-is-now-arena/); [Wikipedia: Arena (AI platform)](https://en.wikipedia.org/wiki/Arena_(AI_platform))
- AA 30-edit test: "We gave four frontier image editing models the same photo and 30 edits in a row: Ideogram 4.5 keeps most of the room intact, while the others drift, GPT Image 2.5 Sunburst most visibly." — [Artificial Analysis on X](https://x.com/ArtificialAnlys/status/2108600224478572767)
- Coverage of the same test:
  - Sunburst re-renders most of the image each edit, leaving ~1/5 unchanged.
  - Nano Banana 2.1 keeps edits local, but the image gradually darkens.
  - Ideogram 4.5 and FLUX 3 left ≥95% untouched on small edits.
  - Sunburst still led the single-edit board at 1,197, and Ideogram 4.5 ranked #23.
  — [AlphaSignal](https://alphasignal.ai/news/artificial-analysis-runs-30-edits-to-expose-how-image-models-drift)
- Ideogram's own comparison says GPT Image and Nano Banana outputs "become unusable within a few edits". This is vendor marketing. — [Ideogram on X](https://x.com/ideogram_ai/status/2105327258466693238)

### Inferences
- When citing AA numbers, name the board version (v2.1) and the date. The 1197/1191 figures are v2.0 and the 1222/1207 figures are v2.1, so they are not contradictory.
- "Preserved the most pixels" is a fair paraphrase of AA's result. The test used one photo and one 30-step sequence, so it is illustrative, not a benchmark.

### Gaps
- The AA pages could not be opened directly. The v2.1 top-5 numbers come from the search engine's snippet of the official page. No published methodology for the 30-edit test was found beyond the X post and press summaries.

## Claim 11 — Research papers on iterative-edit degradation

### Takeaway
VERDICT:
- FreqEdit: TRUE. CVPR 2026, arXiv 2512.01755. FLUX.1 Kontext and Qwen-Image hold quality for ~5 edits, then degrade.
- Mi-Ripple: TRUE. arXiv 2609.11317, "digital ripple".
- REED-VAE: TRUE, but it dates to April 2025 (arXiv 2504.18989).
- Banana100: TRUE. arXiv 2604.03400. Its focus is that no-reference IQA metrics fail on repeated Nano Banana Pro replications (100 iterations).
- "LME-Bench": UNVERIFIED. No such benchmark was found.

### Cited Findings
- **FreqEdit:** "Preserving High-Frequency Features for Robust Multi-Turn Image Editing" (Sun Yat-sen Univ. et al.). It identifies "progressive loss of high-frequency information as the primary cause" of multi-turn degradation. FLUX.1 Kontext and Qwen-Image "maintain reliable editing quality for approximately five sequential edits before experiencing severe degradation". 10+ iterations lead to catastrophic deterioration. FreqEdit is training-free and stable for 10+ edits. — [arXiv 2512.01755](https://arxiv.org/pdf/2512.01755); [CVPR 2026 poster page](https://cvpr.thecvf.com/virtual/2026/poster/39055)
- BFL's own Kontext paper notes that excessive multi-turn editing introduces artifacts, with a figure after six edits. — [FLUX.1 Kontext paper, arXiv 2506.15742](https://arxiv.org/pdf/2506.15742)
- **Mi-Ripple:** "Restoring Images Degraded by Iterative AI Editing" by Jiayin Chen, Yicheng Xu and Muting Wang (MIYANG). "Digital ripple" names the grid-like and granular textures from chained reference-conditioned edits. The method uses spectral notching, structure-aware smoothing, or regeneration from a cleaned reference. Small evidence set. — [arXiv 2609.11317](https://arxiv.org/pdf/2609.11317); [miyang-ai/Mi-Ripple GitHub](https://github.com/miyang-ai/Mi-Ripple) (its README shows before/after examples labeled "Image 2.5")
- **REED-VAE:** "RE-Encode Decode Training for Iterative Image Editing with Diffusion Models", arXiv 2504.18989 (April 2025). Ablations at 5, 15 and 25 encode-decode cycles. — [arXiv 2504.18989](https://arxiv.org/abs/2504.18989)
- **Banana100:** "Breaking NR-IQA Metrics by 100 Iterative Image Replications with Nano Banana Pro", arXiv 2604.03400. It builds a controlled-degradation dataset and argues BRISQUE/NIQE fail on it. Nano Banana 2 was tested at a smaller scale. — [arXiv 2604.03400](https://arxiv.org/pdf/2604.03400)
- "LME-Bench": no hits. The closest real multi-turn editing benchmarks are EdiVal-Bench (EdiVal-Agent, ICLR 2026), MICE-Bench (Edit-R2, arXiv 2606.05950), ImgEdit-Bench and Omni IIE Bench. — [EdiVal-Agent arXiv 2509.13399](https://arxiv.org/pdf/2509.13399); [Edit-R2 arXiv 2606.05950](https://arxiv.org/pdf/2606.05950)

### Inferences
- "Banana100 shows noise build-up" is roughly right. The paper's main claim, though, is that standard no-reference quality metrics fail to register that degradation.

### Gaps
- The arXiv full texts could not be fetched, so details come from search snippets and abstracts. "LME-Bench" may be a mis-transcription; its origin is unknown.

## Claim 12 — Freepik → Magnific rebrand (Apr 28, 2026); Topaz Gigapixel v1.3.0 (May 13, 2026) with Recover Faces 3

### Takeaway
VERDICT: TRUE on both.

### Cited Findings
- Freepik rebranded as Magnific on April 28, 2026, announced by co-founder Joaquín Cuenca. Freepik had acquired the Magnific upscaler in May 2024. Wikipedia reports ~$230M ARR and >1M paying subscribers as of April 2026. — [Wikipedia: Magnific](https://en.wikipedia.org/wiki/Magnific); [eesel.ai (German)](https://www.eesel.ai/de/blog/freepik-ai-preise); [Vantaige](https://vantaige.io/blog/freepik-ai-is-now-magnific-pricing-changes-2026)
- "Topaz Gigapixel v1.3.0 - Recover Faces 3 & 300% Speed Up for NeuroServer Models", May 13, 2026. Recover Faces 3 removes the 512×512 output cap of Recover Faces 2 and reduces dot artifacts. v1.3.2 shipped June 17, 2026 and v1.3.3 July 27, 2026. Topaz Photo v1.6.0 shipped the same model. — [Topaz community release post](https://community.topazlabs.com/t/topaz-gigapixel-v1-3-0-recover-faces-3-300-speed-up-for-neuroserver-models/102815); [Topaz Gigapixel v1.3.2–1.3.3](https://community.topazlabs.com/t/topaz-gigapixel-v1-3-2-1-3-3/104057)

### Inferences
- None needed.

### Gaps
- The forum index lists a June 11 activity date for the v1.3.0 thread. The release post itself says May 13.

## Claim 13 — Photoshop Generative Fill partner models; per-fill limit 1024 → 2048 px; Harmonize out of beta

### Takeaway
VERDICT:
- Partner models: TRUE. Generative Fill's model picker includes Gemini 3.1 (Nano Banana 2), Gemini 3 (Nano Banana Pro), Gemini 2.5 (Nano Banana), FLUX.2 pro and FLUX.1 Kontext [pro].
- 1024 → 2048 px: UNVERIFIED. No Adobe statement was found; community tests still report 1024 px, and 2048 px is cited for "Generate Image".
- Harmonize: likely TRUE. Adobe community posts say it is "now available" across desktop, web and mobile in Photoshop 27.0 (MAX, Oct 28, 2025), though no formal "GA" wording was found.

### Cited Findings
- Model picker lists Gemini 3.1 (Nano Banana 2), Gemini 3 (Nano Banana Pro), Gemini 2.5 (Nano Banana), FLUX.2 pro, and FLUX Kontext Pro. — [Rangy](https://rangy.ai/blog/photoshop-generative-fill-alternatives)
- Adobe's January 2026 community post on premium credits: Gemini 3 (Nano Banana Pro) 40 credits, Gemini 2.5 (Nano Banana) 10, FLUX.2 pro 20, FLUX.1 Kontext [pro] 10, Firefly 1. — [WebSearch summary of Adobe community post](https://community.adobe.com/featured-content-765/gemini-nano-banana-and-flux-kontext-pro-models-now-in-photoshop-max-update-27-0-1546586)
- The first partner-model rollout (Sept 2025) reportedly output at 1K. — [Capture magazine](https://www.capturemag.com.au/news/photoshop-adds-nano-banana-and-kontext-pro-to-generative-fill)
- Community testing (July 2025) "seems to hold true for 1024", while "Generate Image" (beta) may reach 2048×2048. — [Adobe Community thread](https://community.adobe.com/t5/photoshop-ecosystem-discussions/what-is-the-max-resolution-for-generative-fill-in-photoshop-in-2025/m-p/15417958)
- Harmonize: beta launched July 29, 2025. Adobe community posts dated Oct 28, 2025 and Jan 21, 2026 say it is "now available across Photoshop on desktop and web, and mobile" and "live in Photoshop 27.0". — [TechCrunch, 2025-07-29](https://techcrunch.com/2025/07/29/adobe-adds-new-ai-powered-image-editing-features-to-photoshop); [Adobe Community: Harmonize](https://community.adobe.com/featured-content-765/harmonize-effortless-object-blending-across-any-background-anytime-anywhere-1546663)

### Inferences
- The 2048 px figure may come from Generative Expand guidance ("increments below 2048 px") or from Generate Image, not from Generative Fill itself.

### Gaps
- Adobe's official Photoshop release notes could not be opened, so neither the 2048 px change nor Harmonize's GA date is confirmed.

## Claim 14 — FTC TruHeight case; 16 CFR 465; 2026 civil penalty; EU AI Act Art. 50 and Code of Practice; Spain's AI law

### Takeaway
VERDICT: TRUE overall, with nuances.
- TruHeight: complaint and proposed order April 2026; final order July 14, 2026. The $4M judgment is suspended down to $750k, paid in three installments.
- The Reviews and Testimonials Rule is 16 CFR Part 465.
- The 2026 civil-penalty maximum stays at $53,088, because the FTC made **no 2026 inflation adjustment** after the shutdown delayed CPI data.
- EU AI Act Art. 50 applies from Aug 2, 2026, but the AI Omnibus (adopted June 2026) gives legacy generative systems until **Dec 2, 2026** for the Art. 50(2) marking duty.
- The final Code of Practice on AI-generated content was published June 10, 2026.
- Spain: on May 26, 2026 the Council of Ministers approved the **proyecto** de Ley Orgánica (second reading) and sent it to the Cortes. The first anteproyecto had been approved about a year earlier.

### Cited Findings
- April 2026: Vanilla Chip LLC (d/b/a TruHeight) and two principals settled charges of overstated height-growth claims for children's supplements and of using employee-written and incentivized reviews. The proposed order carried a $4M judgment, partially suspended for inability to pay. The complaint cited the FTC Act and the Reviews and Testimonials Rule. — [FTC press release, April 2026](https://ftc.gov/news-events/news/press-releases/2026/04/ftc-takes-action-against-truheight-deceptive-unsubstantiated-advertising-supposed-height-enhancing); [FTC business blog](https://ftc.gov/business-guidance/blog/2026/04/protecting-kids-deceptive-unsubstantiated-health-claims-ftcs-case-against-truheight); [TruHeight AAPC](https://www.ftc.gov/system/files/ftc_gov/pdf/TruHeight-AAPC.pdf)
- Final order approved July 14, 2026 by a 2-0 vote: $750,000 payable with the remainder of the $4M suspended, plus bans on unsubstantiated claims and fake-reviewer misrepresentations. — [FTC press release, July 2026](https://www.ftc.gov/news-events/news/press-releases/2026/07/ftc-approves-final-order-against-truheight-deceptive-unsubstantiated-advertising-supplements-kids); [NutraIngredients, 2026-07-22](https://www.nutraingredients.com/Article/2026/07/22/ftc-finalizes-truheight-order-over-supplement-growth-claims/); [ConsumerLab](https://www.consumerlab.com/recalls/14989/truheight-to-pay-750000-over-claims-that-supplements-help-children-grow-taller/)
- 16 CFR Part 465 = Trade Regulation Rule on the Use of Consumer Reviews and Testimonials. Final rule published 89 FR 68034 (Aug 22, 2024), effective Oct 21, 2024. — [Federal Register 2024-18519](https://www.govinfo.gov/content/pkg/FR-2024-08-22/html/2024-18519.htm); [Cornell LII 16 CFR Part 465](https://www.law.cornell.edu/cfr/text/16/part-465)
- Civil penalty: the Jan 2025 adjustment raised the Section 5(l)/5(m)(1)(A)/5(m)(1)(B) maximum from $51,744 to $53,088. A 2026 Federal Register notice says no 2026 adjustment will be made because the shutdown left no October 2025 CPI-U data, so the 2025 levels continue. — [Federal Register 2025-01361](https://www.govinfo.gov/content/pkg/FR-2025-01-17/html/2025-01361.htm); [FTC 2025 release](https://search.ftc.gov/news-events/news/press-releases/2025/02/ftc-publishes-inflation-adjusted-civil-penalty-amounts-2025); [Federal Register public inspection 2026-18853 (as listed in search results)](https://public-inspection.federalregister.gov/2026-18853.pdf)
- The Commission published the final Code of Practice on marking and labelling AI-generated content on June 10, 2026, supporting Art. 50(2), (4) and (5). Providers need multi-layered machine-readable marking (at least two layers where necessary). — [Jones Day, June 2026](https://www.jonesday.com/en/insights/2026/06/european-commission-publishes-final-code-of-practice-on-marking-and-labelling-aigenerated-content); [AI Weekly](https://aiweekly.co/alerts/eu-publishes-final-ai-transparency-code-ahead-of-article-50); [Freshfields](https://www.freshfields.com/en/our-thinking/blogs/technology-quotient/eu-ai-act-unpacked-33-the-final-code-of-practice-on-transparency-of-ai-generate-102n4yx)
- AI Omnibus: Art. 50(2) is deferred to Dec 2, 2026 for generative systems already on the market before Aug 2, 2026. Parliament endorsed it June 16, 2026 and the Council adopted it June 29, 2026. Reed Smith reports the Commission and AI Board assessed the Code as adequate; TechPolicy.Press earlier said that assessment was pending. — [William Fry](https://www.williamfry.com/knowledge/eu-ai-act-omnibus-deal-reached-postponed-deadlines-watermarking-compromise-and-the-nudificiation-prohibition/); [iubenda](https://www.iubenda.com/en/blog/ai-omnibus-adopted-august-2-obligations-july-2026/); [Reed Smith](https://www.reedsmith.com/our-insights/blogs/viewpoints/102nbz0/transparency-obligations-for-ai-generated-content-the-code-of-practice-adequacy/); [TechPolicy.Press](https://techpolicy.press/the-eus-ai-transparency-code-of-practice-explained)
- Spain, May 26, 2026: the Council of Ministers approved the "proyecto de Ley Orgánica para el buen uso y la gobernanza de la inteligencia artificial" for submission to the Congreso. Fines range from €6,000 to €35M. The first anteproyecto was approved about a year earlier. — [La Moncloa, referencia 26/05/2026](https://www.lamoncloa.gob.es/consejodeministros/resumenes/Paginas/2026/260526-rueda-prensa-ministros.aspx); [Ministerio para la Transformación Digital press note PDF](https://digital.gob.es/content/dam/portal-mtdfp/comunicacion/comunicacion_ministro/2026/05/2026-05-26/260526%20NP%20CMin%20APL%20IA.pdf); [RTVC](https://rtvc.es/consejo-ministros-ley-limitar-uso-inteligencia-artificial-26-mayo-2026/); [Cuatrecasas](https://www.cuatrecasas.com/es/spain/propiedad-intelectual/art/proyecto-ley-organica-buen-uso-gobernanza-ia)

### Inferences
- "Spain's AI law draft approved May 26, 2026" should read "bill (proyecto de ley) approved and sent to Parliament". It is not yet law.
- For AI-image disclosure timing in the EU: new generative systems must mark outputs from Aug 2, 2026; legacy systems have until Dec 2, 2026, assuming the Omnibus entered into force.

### Gaps
- The Official Journal publication and entry-into-force date of the AI Omnibus were not confirmed. The ftc.gov, eur-lex and lamoncloa pages were seen only via search snippets. The exact Federal Register citation of the "no 2026 adjustment" notice should be double-checked.
