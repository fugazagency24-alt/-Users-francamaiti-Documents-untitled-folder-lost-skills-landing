# Alternatives to Veo 3.1 Lite and a catalog of failure modes (state as of 2026-10-26)

> **Method and reliability note (read first).** Research date: 2026-10-26.
>
> **Primary sources read in full (git clones / raw GitHub):**
> - `openai/openai-python` SDK types and CHANGELOG (HEAD 2026-10-26).
> - `openai/openai-cookbook` `examples/sora/sora2_prompting_guide.ipynb` ("Updated - March 2026").
> - `GoogleCloudPlatform/generative-ai` `vision/getting-started/gemini_omni_1_1_flash_video_gen.ipynb` (HEAD `3567247`, 2026-10-26).
> - The daily Arena leaderboard scrape repo `oolong-tea-2026/arena-ai-leaderboards` (snapshot fetched 2026-10-07; Arena's own "last updated" date: Sep 21, 2026).
> - READMEs: `MeiGen-AI/InfiniteTalk`, `Wan-Video/Wan2.2`, `ShmuelRonen/ComfyUI_Hedra`, `gracech0322-cmd/best-seedance-2-api`, `snubroot/Veo-3-Meta-Framework`.
>
> **Blocked hosts.** The egress proxy blocks every vendor site (heygen.com, klingai.com, runwayml.com, minimax.io, byteplus, fal.ai, artificialanalysis.ai, arena.ai, sync.so, hedra.com, openai.com and others). Everything from those hosts is marked **(search summary)**. These are LLM-written summaries of search hits, so treat them as **weaker than primary sources**. Most vendor facts are vendor or reseller claims.
>
> **Labels.** OFFICIAL = vendor docs or code. VENDOR = vendor marketing. THIRD-PARTY = reseller or aggregator blog. PRACTITIONER = creator or community. INFERENCE = my synthesis.
>
> **Age.** Items older than about 6 months (before late April 2026) are flagged **[>6 months]**.
>
> **Cross-references.** Sibling notes 01–06 in this folder already cover Veo specs, prompt structure, voice and accent, identity and extension, multi-character formats, and DubVoice/audio post in depth. Section 4 here consolidates them into one failure catalog and cites the primary URLs those notes verified.

---

## 1. Talking-head avatar tools with exact lip-sync to a fixed voice (HeyGen, OmniHuman, Hedra, Captions, Arcads, Creatify, open source)

### Takeaway
A different class of model solves the client's three worst pain points (voice changes, neutral accent, face drift) **by construction**. These are **audio-driven avatar models**: they take *one image plus your final audio track*, so the voice, the Argentine accent and the exact script come from the audio you supply. Identity comes from the same master still every time.

As of Oct 2026 the leading API options are:
- **ByteDance OmniHuman 2.0** on BytePlus (launched **2026-10-15**, about $0.07/s).
- **Hedra Character-3** (up to about 10 min, multi-speaker audio, about $0.05/s at 720p; no 2026 successor found) **[>6 months, model from ~Mar 2025]**.
- **HeyGen Avatar V** (GA **May 2026**, about $0.05/s API, long-form, but built around a 15 s *recorded* clip, i.e. a digital twin).
- Self-hosted open-weights options: **LongCat-Video-Avatar-1.5** (May 21, 2026) and InfiniteTalk **[>6 months]**.

Arcads, Creatify and Captions are ad-production front-ends with stock "AI actors". I found no verified Spanish or Argentine benchmark for them.

### Cited Findings
**HeyGen (Avatar IV / Avatar V, plus the new "HeyGen Video" model)**
- [VENDOR, search summary] HeyGen's help center announces "Avatar V is now available on HeyGen". Several third parties date GA to **May 2026**. — [HeyGen help center](https://help.heygen.com/en/articles/14602974-avatar-v-is-now-available-on-heygen); [genie-artificiel](https://www.genie-artificiel.com/en/ai-tools/heygen/)
- [VENDOR, search summary] Avatar V page claims:
  - it "maintains a stable identity representation across scenes, camera angles, and extended video durations, without any additional fine-tuning or extra reference input";
  - it needs a **"15-second webcam clip"**;
  - it is "Stable beyond 30 minutes".
  A HeyGen blog says a 30-minute video renders in one pass. The Creator plan supports videos up to 30 min. These are marketing claims. — [HeyGen Avatar V page](https://www.heygen.com/avatars/avatar-v); [HeyGen blog: Photo vs Digital Twin vs Avatar V](https://www.heygen.com/blog/photo-avatar-vs-digital-twin-vs-avatar-v-vs-instant-avatar)
- [THIRD-PARTY, search summary] HeyGen Spanish "covers 22 regional variants across Latin America and Spain". The platform-wide figure is "177+ languages and dialects with 3,200+ accents" (other sources say 175+). I found no Avatar-V-specific list of Argentine voices. — [Artlist HeyGen models](https://artlist.io/ai/models/heygen-ai); [HeyGen blog best avatar generators](https://www.heygen.com/blog/best-ai-avatar-generators)
- [THIRD-PARTY, search summary, **conflicting**] Avatar V API price is about **$0.05/s ($3/min)**, billed separately from subscription credits. Voyager instead lists **$7.20/min** for Avatar V digital twins. Credit costs reported as 20 vs 48 vs about 70 credits/min. — [eesel](https://www.eesel.ai/blog/heygen-pricing); [Voyager](https://voyager.so/blog/heygen-pricing)
- [OFFICIAL, search summary] HeyGen API lip-sync translation: **Speed $0.81/min** and **Precision $1.50/min**. No free API credits from Feb 2026. API credits are separate from web-plan credits. — [HeyGen API pricing explained](https://help.heygen.com/en/articles/10060327-heygen-api-pricing-explained)
- [THIRD-PARTY, search summary] A MindStudio article calls it "Avatar 5" ("A 15-Second AI Twin and Its Limits"). The name is not used elsewhere and is probably the same product. — [MindStudio](https://www.mindstudio.ai/blog/what-is-heygen-avatar-5)
- [VENDOR/THIRD-PARTY, search summary] **HeyGen Video ("heygen-video-1")** is a general prompt-to-scene model, not an avatar model. Details:
  - launched **2026-09-30**;
  - 5–15 s clips from text, images or references, up to 2K, with sound in the same pass;
  - API endpoint `POST /v3/models/videos`, paid keys only;
  - price about $0.02/s at 480p and $0.03/s at 768p with audio (one source says a launch sale halves this through end of October);
  - one reseller says it is "a MiniMax H3 post-train" (single source);
  - HeyGen claims #1 on Artificial Analysis text-to-video in Oct 2026 (company claim).
  — [HeyGen blog: Introducing HeyGen Video](https://www.heygen.com/blog/introducing-heygen-video); [OpenRouter heygen-video-1](https://openrouter.ai/heygen/heygen-video-1); [OrcaRouter](https://www.orcarouter.ai/blog/heygen-video-1-launch); [MindStudio pricing](https://www.mindstudio.ai/blog/heygen-video-pricing)

**ByteDance OmniHuman**
- [THIRD-PARTY, search summary] **OmniHuman 2.0** launched on BytePlus on **2026-10-15** "with support for speech, music, and dialogue".
  - Inputs: a still image plus an audio track, with an optional text prompt for gestures and camera. It is image-sourced only, so a reference video cannot drive the performance.
  - Price: about **$0.07/s** on BytePlus. Older OmniHuman 1.0 listings show $0.12/s.
  - Limits conflict: 5-minute audio and 720p (Supermaker) vs 2 min on one reseller (OpenClips).
  - Known issues: "rough edges, particularly with teeth rendering and fully matching every syllable to mouth shape".
  — [MindStudio: OmniHuman 2.0](https://www.mindstudio.ai/blog/bytedance-omnihuman-2-avatar-video); [MindStudio: pricing/limits](https://www.mindstudio.ai/blog/bytedance-omnihuman-2-0); [Supermaker](https://supermaker.ai/blog/omnihuman-2-0-launch/); [OpenClips](https://openclips.ai/blog/what-is-omnihuman-2-0/)
- [THIRD-PARTY, search summary] WaveSpeed hosts REST endpoints for OmniHuman 1.0 and **1.5**, but none found for 2.0. — [WaveSpeed OmniHuman 1.5](https://wavespeed.ai/models/bytedance/avatar-omni-human-1.5)

**Hedra Character-3**
- [VENDOR, search summary] Hedra calls Character 3 its "latest longform avatar model". It offers "multi-language support and speaker selection for clips up to 10 minutes" and takes image + text + audio together.
  - API: `POST api.hedra.com/v3/models/hedra-character-3`.
  - A start frame and audio are required; up to **4 audio files** for multi-speaker, passed as a list in order.
  - Price per one listing: 540p 2.5¢/s, 720p 5¢/s, 1080p 6.25¢/s, from a prepaid wallet with no free tier.
  - A newer model, "Hedra Omnia", does not replace Character-3's long-form workflow.
  — [Hedra Character 3 API page](https://www.hedra.com/develop/models/video/hedra-character-3); [Magic Hour guide](https://magichour.ai/blog/guide-to-hedra-ai)
- [OFFICIAL-adjacent, community node README] The Hedra ComfyUI node supports 16:9, 9:16 and 1:1 at 540p/720p, "~3.5 to ~7 credits per second of video", and needs "Creator tier or higher" for API access. — [ShmuelRonen/ComfyUI_Hedra README](https://github.com/ShmuelRonen/ComfyUI_Hedra)
- No evidence of a 2026 successor. Character-3 dates to about March 2025 **[>6 months]**. Spanish is not named specifically, only "multi-language". — [aiwiki Hedra Character (search summary)](https://aiwiki.ai/wiki/hedra_character)

**Arcads / Creatify / Captions (ad-production front-ends)**
- [THIRD-PARTY, competitor-authored, search summary]
  - Positioning: Creatify = volume and URL-to-ad, the "strongest… for international markets, with deeper Spanish, Portuguese… voice coverage", 700+ actors. Arcads = the "most convincing AI actors". Captions (Mirage) = mobile/TikTok editing; "solid for mobile consumption but doesn't hold up to HeyGen or Arcads at full resolution".
  - Pricing conflicts: Arcads $110/mo for 10 videos vs "from $77/mo"; Creatify about $39/mo; Captions $9.99/mo.
  - **No source benchmarks Arcads' Spanish voices or lip-sync.**
  — [Lensgo comparison (sells a competing tool)](https://lensgo.ai/blog/best-ai-ugc-ad-tools-2026); [adlibrary](https://adlibrary.com/posts/best-ai-ugc-video-tools-2026); [Wireflow](https://www.wireflow.ai/blog/best-arcads-alternatives-in-2026)

**Open-weights, self-hostable on Google Cloud GPUs**
- [OFFICIAL README] **InfiniteTalk** (weights released **Aug 19, 2025**) **[>6 months]**:
  - "unlimited-length talking video generation" for audio-driven video-to-video dubbing and image-to-video;
  - 480p/720p;
  - "I2V… good results from a single image for up to 1 minute. Beyond 1 minute, color shifts become more pronounced";
  - the FusionX LoRA "exacerbates color shift over 1 minute and reduces ID preservation";
  - "Audio CFG works optimally between 3–5" for lip-sync.
  — [MeiGen-AI/InfiniteTalk README](https://github.com/MeiGen-AI/InfiniteTalk)
- [OFFICIAL README] **LongCat-Video-Avatar-1.5** (**May 21, 2026**): "replaces Wav2Vec2 with Whisper-Large for more accurate lip synchronization", "robust long-video generation", and "supports both single-stream and multi-stream audio inputs" (multi-speaker), with 8-step distilled inference. — [InfiniteTalk README news](https://github.com/MeiGen-AI/InfiniteTalk); [LongCat-Video repo](https://github.com/meituan-longcat/LongCat-Video)
- [OFFICIAL README] **Wan2.2-S2V-14B** (Aug 26, 2025) **[>6 months]**: audio-driven "cinematic" speech-to-video at 480p/720p with optional CosyVoice TTS. **Wan2.2-Animate-14B** (Sep 19, 2025) handles "character animation and replacement". — [Wan-Video/Wan2.2 README](https://github.com/Wan-Video/Wan2.2)

### Inferences
- **Why this class matters for the client.** In Veo every call re-samples the voice, and there is no voice ID (note 03). With audio-driven avatar models the audio *is the input*. Feed them one fixed Argentine TTS/STS track per character (ElevenLabs/DubVoice; notes 03 and 06) and the master still from the image SOP. Then:
  - **voice consistency** (pain 1),
  - **accent** (pain 2),
  - **exact script** (no rushed or cut lines),
  - **identity** (pain 3: every clip restarts from the same still)
  are guaranteed upstream. The trade-off is less cinematic camera and body motion than Veo, plus each tool's own tells (OmniHuman's reported teeth and syllable issues).
- **Suggested routing (to A/B test):**
  - Long single-speaker monologue or VSL, 30 s to 5 min, script locked: OmniHuman 2.0 or Hedra Character-3 from the master still + final Argentine audio.
  - Short UGC hooks with natural motion: stay on Veo 3.1 Lite i2v + STS voice lock.
  - Multi-speaker podcast: Hedra (up to 4 audio tracks) or LongCat multi-stream, or Veo per-speaker single shots (note 05).
- **HeyGen Avatar V is a "digital twin" built from a recorded 15 s webcam clip.** For fictional people the fitting HeyGen paths are photo avatars or stock avatars. Whether HeyGen accepts a *synthetic* 15 s clip, e.g. Veo-generated, as a twin source is unverified (see Gaps), and should not be attempted against HeyGen's consent rules.
- **Price per 60 s of finished talking-head**, from the figures above, before retakes: OmniHuman 2.0 ≈ $4.20; Hedra 720p ≈ $3.00; HeyGen Avatar V API ≈ $3.00 (or $7.20 per the conflicting figure). Veo 3.1 Lite 1080p with audio ≈ $4.80 for 60 s of 8 s clips (note 01: $0.08/s), but needs about 3 generations per usable shot (note 04). So audio-driven avatars are likely **cheaper per usable second** for monologues. This is an inference from list prices.

### Gaps
- No independent test of **Argentine/rioplatense lip-sync quality** for any avatar tool. Spanish support claims are generic.
- I could not verify HeyGen's consent and verification rules for creating avatars from synthetic footage. The site is blocked.
- No primary BytePlus documentation for OmniHuman 2.0 limits (max duration, resolution, languages). All figures are third-party.
- No verified 2026 specs for Captions "Mirage", Creatify "Aurora" or Arcads' underlying models. Search-budget and blocked-host limits.

---

## 2. General video models with native audio as alternatives or escalations (Sora 2, Kling 3.x, Seedance 2.x, Runway Gen-4.5, Wan 3.0, MiniMax H3/Hailuo, Gemini Omni)

### Takeaway
1. **Sora 2 is no longer an option.** OpenAI's SDK marked the Sora video APIs **deprecated on 2026-08-14**, and multiple sources report the **API shutdown on 2026-09-24**.
2. **Gemini Omni 1.1 Flash** (`gemini-omni-1.1-flash-preview`) is on the client's own platform and is the natural escalation. It holds **#1 on Arena text-to-video** as of the Sep 21, 2026 update. It offers ≤5 reference images + 3 reference videos, 3–10 s clips up to 4K, and extension adding 10 s per call. Its limit: **no audio references**.
3. **External models with native audio:**
   - **MiniMax H3/Hailuo 3.0** (Jul 31, 2026): #1 Arena image-to-video; reportedly takes up to 3 *audio* references.
   - **Wan 3.0** (Aug 2026): up to 30 s, closed weights.
   - **Seedance 2.0/2.5**: real-person reference uploads gated by review.
   - **Kling 3.0**: Spanish one of 5 native dialogue languages, multi-shot, voice binding for *video* elements.
   - **Runway Gen-4.5**: audio timeline conflicting; ranks well below the others.

### Cited Findings
**Sora 2 (OpenAI): deprecated and shut down**
- [OFFICIAL-CODE] openai-python CHANGELOG v3.1.0 (**2026-08-14**): "**api:** deprecate Sora video APIs (#3610)". — [openai-python CHANGELOG](https://github.com/openai/openai-python/blob/main/CHANGELOG.md)
- [THIRD-PARTY, search summary] "OpenAI discontinued Sora and shut the API down on September 24, 2026". The Sora app and website reportedly closed on April 26, 2026. — [eesel: Sora 2 API reviews](https://www.eesel.ai/blog/sora-2-in-the-api-reviews); [unifically](https://unifically.com/blogs/sora-api); [framesurfer](https://framesurfer.com/blogs/sora-2-pricing)
- [OFFICIAL, historical] Before shutdown (cookbook "Updated - March 2026"):
  - `sora-2` / `sora-2-pro`, durations 4/8/12/16/20 s, up to 1080p on Pro;
  - **Characters API "(objects and animals)"**, ≤2 per generation;
  - extension "up to 6 times, for a total of 120s".
  Pricing was $0.10/s (sora-2 720p) and $0.30–0.70/s (Pro). — [OpenAI Cookbook Sora 2 prompting guide](https://github.com/openai/openai-cookbook/blob/main/examples/sora/sora2_prompting_guide.ipynb); [eesel pricing (search summary)](https://www.eesel.ai/blog/sora-2-in-the-api-pricing)
- [OFFICIAL, still useful as general guidance] Sora guide, transferable to Veo:
  - "For multi-character scenes, label speakers consistently and use alternating turns".
  - "a 4-second shot will usually accommodate one or two short exchanges… Long, complex speeches are unlikely to sync well".
  - "you may see better results by stitching together two 4 second clips… instead of generating a single 8 second clip".
  - "small changes in phrasing can alter identity… reuse phrasing for continuity".
  - "Naming three to five colors helps keep the palette stable across shots".
  - "If a shot keeps misfiring, strip it back: freeze the camera, simplify the action, clear the background".
  — [OpenAI Cookbook Sora 2 prompting guide](https://github.com/openai/openai-cookbook/blob/main/examples/sora/sora2_prompting_guide.ipynb)

**Gemini Omni 1.1 Flash (Google, same platform as Veo)**
- [OFFICIAL] Model `gemini-omni-1.1-flash-preview`, called through the Interactions API.
  - Tasks: `text_to_video`, `image_to_video`, `reference_to_video`, `extend`, `edit`.
  - Duration 3–10 s; resolution 360p/720p/1080p/4K; 16:9 or 9:16; "Audio will be generated alongside the output video".
  - "we recommend supplying no more than 5 reference images and 3 reference videos".
  - "**Audio reference inputs are not currently supported.**"
  - Extension: "source video (up to 30s long). Each call can add a maximum of 10s", "keeping the characters, setting, and style consistent".
  - Multi-turn editing via `previous_interaction_id`.
  - Output carries C2PA + SynthID.
  — [GCP notebook gemini_omni_1_1_flash_video_gen](https://github.com/GoogleCloudPlatform/generative-ai/blob/main/vision/getting-started/gemini_omni_1_1_flash_video_gen.ipynb)
- Pricing: about $0.10/s at 720p and $0.15/s at 1080p, against $0.05/$0.08 for Veo 3.1 Lite with audio. — see note 01, from the [Agent Platform pricing page](https://cloud.google.com/gemini-enterprise-agent-platform/generative-ai/pricing)

**Kling 3.0 (Kuaishou)**
- [THIRD-PARTY, search summary] Global launch reported **2026-03-25** "with 4K video, native audio, and multi-shot generation" **[~7 months]**.
  - Spanish is one of five native dialogue languages (EN, ZH, JA, KO, ES).
  - "you can control which character speaks which line by pairing characters with their dialogue in the prompt"; up to 6 cuts per generation.
  - Specs vary by platform: VEED lists 720p and 3/5/8 s, others 3–15 s.
  - No independent Spanish lip-sync benchmark.
  — [Cinevva news](https://app.cinevva.com/news/2026-03-25-kling-3-global-launch); [Atlas Cloud review](https://www.atlascloud.ai/blog/tips/kling-3.0-review-features-pricing-ai-alternatives); [VEED Kling 3.0](https://www.veed.io/ai-models/video/kling-3-0)
- [THIRD-PARTY/OFFICIAL-reseller, search summary] Kling credits: 9/s for native audio at 720p, 12/s at 1080p, **+2/s "voice control"**; 6 and 8/s without audio.
  - fal: Pro $0.168/s with audio, $0.196/s with audio + voice control.
  - fal docs: "**voice binding is only supported for video elements, not image elements**".
  — [fal Kling v3 Pro i2v](https://fal.ai/models/fal-ai/kling-video/v3/pro/image-to-video); [evolink](https://evolink.ai/blog/kling-3-o3-api-official-discount-pricing-developers)
- [THIRD-PARTY] A pricing-page title mentions "Kling 4.0". Unverified. — [camclo3d](https://camclo3d.com/blog/kling-ai-pricing)

**Seedance 2.0 / 2.5 (ByteDance, BytePlus ModelArk)**
- [THIRD-PARTY citing BytePlus table "last updated September 2026", search summary] Seedance 2.0: about $0.07/s at 480p, **$0.15/s at 720p, $0.37/s at 1080p**, $0.78/s at 4K. Fast tier $0.12/s at 720p. OpenRouter lists "with audio" and "no audio" rates, so audio is native. — [Atlas Cloud pricing](https://www.atlascloud.ai/blog/case-studies/seedance-2.0-pricing-full-cost-breakdown-2026); [OpenRouter Seedance 2.0](https://openrouter.ai/bytedance/seedance-2.0)
- [THIRD-PARTY, affiliate-linked GitHub guide, Jul 2026] "not every API lets you use your own real-person content". The private asset workflow is "Upload an authorized image or video → Wait for the asset review → Receive an Asset ID". BytePlus's real-person workflow is "more limited for normal indie developers". Replicate and fal: "No" private real-person assets. Tested output length: 15 s. — [gracech0322-cmd/best-seedance-2-api](https://github.com/gracech0322-cmd/best-seedance-2-api)

**Wan 3.0 (Alibaba)**
- [THIRD-PARTY, search summary] Public beta Aug 6–7, 2026; API GA Aug 24, 2026 (single source).
  - Audio "generated in the same pass… dialogue, sound effects and music".
  - Up to **30 s** at up to 1080p; hosted via Wan.video, QwenCloud and Model Studio.
  - Weights not public as of 2 Oct 2026. A conflicting claim of Apache-2.0 open weights is unreliable.
  — [kingy.ai](https://kingy.ai/blog/wan-3-0-analysis/); [Morphic](https://morphic.com/resources/models/wan-3-0); [youart](https://youart.ai/blog/wan-3-0-release-date)

**MiniMax H3 / Hailuo 3.0**
- [OFFICIAL, search summary] MiniMax's post (launch **Jul 31, 2026**): a general-purpose multimodal model generating video with "native stereo audio at up to 2K resolution and 15 seconds". — [MiniMax H3 blog](https://www.minimax.io/blog/minimax-h3)
- [THIRD-PARTY, search summary] References: up to **9 images, 3 video clips and 3 audio clips**, plus instruction-based editing. API model ID `MiniMax-H3`; about $0.78 per 6 s 2K clip with audio. Open weights promised; one source says out Aug 3 (unverified). — [vidmuse](https://vidmuse.ai/blog/hailuo-3-0); [pixo](https://pixo.video/blog/what-is-minimax-h3); [picassoia](https://blog.picassoia.com/hailuo-3-0-release-date-minimax-new-video-model-explained)

**Runway Gen-4.5**
- [THIRD-PARTY, **conflicting**, search summary] TechCrunch (2025-12-11) says a Gen-4.5 update "brings native audio and long-form, multi-shot generation" with "one-minute videos with character consistency, native dialogue". Other listings say audio arrived in May 2026 via ElevenLabs, or that the model is silent with a 10 s max. **[>6 months]** No Gen-5 found. — [TechCrunch](https://techcrunch.com/2025/12/11/runway-releases-its-first-world-model-adds-native-audio-to-latest-video-model); [Phygital+](https://phygital.plus/ai-models/runway-4-5/); [Venice](https://venice.ai/models/runway-gen4-5)

### Inferences
- **Escalation order for the client** (keeps Google Cloud as the home platform):
  1. Veo 3.1 Lite (default).
  2. Veo 3.1 Fast for hero shots or when reference images are needed. Arena puts Fast at ≈ the same score as full Veo 3.1 (§5).
  3. **Gemini Omni 1.1 Flash** for multi-character scenes that need per-character image references, 10 s steps, or conversational fixes ("same clip, but the woman on the left says the line").
  4. External: Kling 3.0 (Spanish dialogue, voice binding from a *video* element) or MiniMax H3 (audio references) **only after a blind test on Argentine Spanish**.
- **MiniMax H3's audio references are the only native in-model route to a "voice lock"** found in this research. Whether a 3-clip audio reference actually fixes timbre and accent is **unverified**. It is worth one controlled test: the same Argentine reference voice across 10 clips, scored by note 03's speaker-similarity check.
- Seedance's real-person asset review suggests some vendors treat **photoreal synthetic faces** like real people. Expect friction uploading ultra-realistic avatar stills. This is an inference, untested.
- Every external model reintroduces pain point 1, because each call samples a new voice, unless voice binding or audio references work. So **post-production voice lock (STS) stays mandatory** whatever model is used (note 06).

### Gaps
- No primary docs reachable for Kling, BytePlus, Alibaba, MiniMax or Runway. Specs and prices are third-party and often conflicting.
- No evidence on Argentine accent fidelity of native audio in Kling, Seedance, Wan, H3 or Omni.
- No evidence any of these models is offered inside Google Cloud's Model Garden (would simplify procurement). Not researched.

---

## 3. Lip-sync models, and which tools creators pair with Veo

### Takeaway
**Sync Labs** is the most API-ready re-lip-sync layer (fully covered in note 06 §Q3):
- `sync-3` (Apr 2026), `lipsync-2-pro`, `react-1`;
- `active_speaker_detection` for multi-face shots;
- per-segment audio.

HeyGen also sells lip-sync translation (Speed $0.81/min, Precision $1.50/min). The common creator stack (vendor content, unverified) splits the work this way:
- **Veo 3.1** for short talking-to-camera hooks;
- **HeyGen** for the long spokesperson cut;
- **Kling** for motion and product inserts (motion transfer);
- **ElevenLabs** for voice;
- **CapCut/Submagic** for assembly and captions.

### Cited Findings
- [OFFICIAL-CODE via note 06] Sync Labs:
  - model enum `"lipsync-2", "lipsync-1.9.0-beta", "lipsync-2-pro", "react-1", "sync-3"`;
  - options `active_speaker_detection` (auto, or `frame_number` + `coordinates`, or `bounding_boxes`), `segments` with per-range audio, `sync_mode` (`bounce|loop|cut_off|silence|remap`), `temperature`, `occlusion_detection_enabled`.
  — [sync-python-sdk model.py](https://github.com/synchronicity-labs/sync-python-sdk/blob/main/src/sync/common/types/model.py); [active_speaker.py](https://github.com/synchronicity-labs/sync-python-sdk/blob/main/src/sync/common/types/active_speaker.py)
- [THIRD-PARTY, search summary] Medux lists HeyGen lip-sync at $0.0333/s (Speed) and $0.0667/s (Precision), consistent with HeyGen's help center. — [Medux 2026 lip-sync tools](https://medux.io/blogs/best-ai-lip-sync-tools-2026.html); [HeyGen API pricing](https://help.heygen.com/en/articles/10060327-heygen-api-pricing-explained)
- [VENDOR, search summary] Veo 3.1 is "the best option for talking-to-camera hook clips… Its main limit is clip length, so it suits single beats rather than full scripts". HeyGen is the avatar layer for testimonial-style UGC. Kling's motion transfer is used for "animating characters or adding product-handling inserts" (character image + reference video). ElevenLabs handles voiceovers and cloning. CapCut and Submagic handle assembly. Note: Oakgen sells a bundle of Veo + Kling + ElevenLabs, and one source is a paid course. — [adlibrary guide](https://adlibrary.com/guides/how-to-create-ai-ugc-ads-that-convert); [Oakgen](https://oakgen.ai/learn/best-ai-ugc-ad-tools-2026); [Skool playbook PDF](https://assets.skool.com/f/0a2fcb7fddb14d6eb190a81b7c20c7a0/6ea752a95e5843d1b48b5701d9ef5e5d3a83c58ac9124f22a646ae3a8171015b)
- [VENDOR, search summary, via note 06] "voiceover overlay for AI-generated UGC ads" avoids "mouth-movement inconsistency". Keep lip-sync for direct-to-camera shots. — [invideo FAQ](https://invideo.io/faq/should-i-use-lip-sync-or-voiceover-overlay-for-ai/)

### Inferences
- **Pairing that fits the client's pain points:**
  - Veo 3.1 Lite i2v for short beats → STS voice lock (ElevenLabs/DubVoice) → re-lip-sync with `sync-3` only when words or timing change.
  - Audio-driven avatar (OmniHuman 2.0 / Hedra) for long monologues.
  - Composite real product label shots in post.
- **For multi-face podcast shots:** re-lip-sync only with `active_speaker_detection` + per-speaker `segments`. Prefer single-face clips (note 05).

### Gaps
- No independent, Spanish-specific lip-sync benchmark across Sync, HeyGen, Hedra, OmniHuman or Kling. Same gap as note 03 §Q5.

---

## 4. Failure-mode catalog for Veo (and video models in general): cause → prompt fix → parameter fix → post fix

### Takeaway
Nearly every failure the client reports traces back to one of four causes:
1. **Too much per clip**: too many words, actions, speakers or camera moves.
2. **No conditioning channel for the thing that drifted**: Veo has no voice ID, no accent parameter, and no reference images on Lite.
3. **Text-rendering habits**: quotes and labels become on-screen gibberish.
4. **Re-sampling on every call**: new seed, forced prompt rewriter.

The defensible fixes are **structural**:
- i2v from the master still every clip;
- one speaker and one action per clip;
- word budgets;
- `negativePrompt` for text;
- voice lock in post;
- an automated QA gate with 2–4 samples per shot.

Few fixes are officially documented. Most are practitioner consensus or inference, and are labeled as such below.

### Cited Findings
Format per failure: **Cause** | **Prompt fix** | **Parameter fix** | **Post fix** — evidence grade and sources.

**F1. Burned-in subtitles or captions appear**
- **Cause:** Quoted dialogue reads to Veo as text to render. Model habit from training data.
- **Prompt:** Write dialogue with a colon and no quotes (`Ella dice: ...`).
- **Parameter:** `negativePrompt: "texts, captions, subtitles, on-screen text, watermark"`.
- **Post:** Crop, or remove with AI text removal. The output is flattened, so subtitles cannot be toggled off.
- Evidence: OFFICIAL (Vertex best practices: "use a colon (:)… avoid using quotation marks"); OFFICIAL sample negative "texts, captions, subtitles". PRACTITIONER: negatives "help some users but aren't reliable". [>6 months] creator report (May 2025): "Veo 3 randomly adds auto-generated subtitles". — [Vertex Best practices for Veo (search summary)](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/video/best-practice); [cookbook Get_started_Veo](https://github.com/google-gemini/cookbook/blob/main/quickstarts/Get_started_Veo.ipynb); [veo3ai.io subtitles fix (search summary)](https://www.veo3ai.io/blog/veo-3-remove-subtitles-captions-fix-2026); [X @henkvaness (search summary)](https://x.com/henkvaness/status/1927327770788479122); [snubroot QC negatives](https://github.com/snubroot/Veo-3-Meta-Framework)

**F2. Gibberish on-screen text, warped product labels, morphing logos**
- **Cause:** The model "draws" text rather than typesetting it, and product geometry is re-rendered every frame.
- **Prompt:** Never ask Veo to render readable text. Keep the product still, frontal and large, with no rotation.
- **Parameter:** Start frame (i2v) already showing the correct label. On Veo 3.1/Fast (not Lite), r2v with the product as an `asset` reference.
- **Post:** Composite the real pack shot or label, or add text overlays in the editor.
- Evidence: PRACTITIONER ("a jumble of nonsensical characters"); OFFICIAL r2v product-consistency sample (not Lite). — [Arsturn (search summary)](https://arsturn.com/blog/how-to-get-clean-text-in-veo-3-a-guide-to-fixing-ai-gibberish); [veo3_reference_to_video](https://github.com/GoogleCloudPlatform/generative-ai/blob/main/vision/getting-started/veo3_reference_to_video.ipynb); detail in note 04 §6

**F3. Voice changes between clips, or after extension**
- **Cause:** No voice ID or audio-reference input in the Veo config. Each call samples a new voice. `seed` only reproduces *identical* requests.
- **Prompt:** A frozen "voice DNA" block repeated verbatim per character (reduces drift, does not eliminate it).
- **Parameter:** Same seed only for re-renders of the same shot. For extension, speech should reach the last second.
- **Post:** **Speech-to-speech the whole edited dialogue track into one fixed voice per character** (ElevenLabs Voice Changer / DubVoice). Timing is preserved, so no re-lip-sync is needed.
- Evidence: OFFICIAL-CODE (python-genai types: no voice field; seed semantics); PRACTITIONER (one-pass Voice Changer "ensures every clip has the exact same voice"). — [python-genai types.py](https://github.com/googleapis/python-genai/blob/main/google/genai/types.py); [TikTok @ai.for.real.life (search summary)](https://www.tiktok.com/@ai.for.real.life/video/7537477893442538766); full detail in notes 03 §Q3 and 06 §Q2

**F4. Accent drifts to neutral Spanish instead of Argentine**
- **Cause:** No accent parameter, and Google publishes no accent guidance. Neutral Spanish is the model's prior. In STS, **accent comes from the source recording, not the target voice**.
- **Prompt:** Name the accent next to every line, and write the line itself in rioplatense (voseo, "che", local lexicon) so the text pulls the accent.
- **Parameter:** none.
- **Post:** For a guaranteed accent, generate the audio first: an Argentine TTS voice, or a human Argentine reading converted via STS. Then use an audio-driven avatar (§1) or re-lip-sync (sync-3).
- Evidence: OFFICIAL (ElevenLabs voice-changer skill: "Accent and cadence transfer from the source, not the target"); PRACTITIONER (accent works sometimes, no controlled test). — [elevenlabs/skills voice-changer SKILL.md](https://github.com/elevenlabs/skills/blob/main/voice-changer/SKILL.md); detail in notes 03 §Q1 and 06 §Q2

**F5. Wrong character speaks, both mouths move, lines swapped, one speaker silent**
- **Cause:** Similar-looking or similar-sounding characters; bare `Man:/Woman:` labels; 3+ turns per clip; expressive listeners read as speakers.
- **Prompt:** Attribute each line to a *visible* descriptor ("the woman in the red hoodie on the left says: …"). Alternate turns. Use one line per speaker per clip. Describe the listener's silent state positively ("listens with lips closed, nodding").
- **Parameter:** none in Veo. On Omni, reference images per character.
- **Post:** `sync-3` with `active_speaker_detection` + `segments`. Better: shoot **one speaking face per clip**.
- Evidence: PRACTITIONER ("smears the dialogue across both mouths"); OFFICIAL Sora guidance "label speakers consistently and use alternating turns". — [veo3ai.io two-character guide (search summary)](https://www.veo3ai.io/blog/veo-3-two-character-dialogue-guide-2026); [OpenAI Sora 2 guide](https://github.com/openai/openai-cookbook/blob/main/examples/sora/sora2_prompting_guide.ipynb); [apipass unwanted dialogue (search summary)](https://apipass.dev/blogs/how-to-solve-veo-3-keep-generating-unwanted-dialogue); detail in note 05 §Q1, Q5

**F6. Speech cut off at the end of the 8 s clip, or rushed delivery**
- **Cause:** The line is too long for the clip. Google publishes no word limit.
- **Prompt:** Budget about 15–20 words per 8 s (English consensus). Note 02's Spanish inference is ≤18–20 words per 8 s, ≤13–14 per 6 s, ≤8–9 per 4 s. End standalone lines about 0.5 s before the end.
- **Parameter:** Pick `durationSeconds` from the measured TTS length (Google's own pipeline measures the voice duration first, then picks 4/6/8 s).
- **Post:** Split the script across clips.
- Evidence: PRACTITIONER (rushed or clipped when overlong); GOOGLE-SAMPLE (duration-first pipeline). — [Replicate blog (search summary)](https://replicate.com/blog/using-and-prompting-veo-3); [veo3ai.io voiceover guide (search summary)](https://www.veo3ai.io/blog/veo-3-text-to-speech-voiceover-guide-2026); [story-generator SKILL.md](https://github.com/GoogleCloudPlatform/vertex-ai-creative-studio/blob/main/experiments/mcp-genmedia/skills/story-generator/SKILL.md); detail in note 02 §4

**F7. Mouth not moving, or moving off-sync**
- **Cause:** Long or dense lines, extreme mouth close-ups, occlusion (hand or product over the mouth). Veo's lip detail is a known weak spot (vendor claim).
- **Prompt:** Shorter lines. Start from a closed-mouth, frontal still. Chest-up framing. Keep hands away from the face.
- **Parameter:** 2–4 samples per request and pick the best.
- **Post:** Re-lip-sync with `sync-3`/`lipsync-2-pro` (`occlusion_detection_enabled` when hands cross the mouth).
- Evidence: VENDOR [>6 months] (Argil: Veo 3 "lacks perfect lips"); PRACTITIONER (long speeches cause drifting lip-sync). — [Argil blog (search summary)](https://www.argil.ai/blog/perfect-lips-ai-how-to-create-realistic-avatar-lip-sync-videos-2025); [eastondev (search summary)](https://eastondev.com/blog/en/posts/ai/20251207-veo3-audio-generation-guide/)

**F8. Unwanted extra dialogue, random speech or music**
- **Cause:** Negatives like "no talking" prime speech. Camera-facing or near-mic subjects are assumed to be speakers.
- **Prompt:** State silence positively ("she stays silent, lips closed; only room tone and keyboard clicks"). Use a closed audio bed: "Audio: only the voice of …".
- **Parameter:** `generateAudio: false` for B-roll inserts.
- **Post:** Replace the audio bed.
- Evidence: PRACTITIONER. — [apipass (search summary)](https://apipass.dev/blogs/how-to-solve-veo-3-keep-generating-unwanted-dialogue); [veo3gen troubleshooting (search summary)](https://www.veo3gen.app/blog/why-your-veo3gen-clip-adds-random-dialogue-or-music-and-how-to-control-it-a-crea)

**F9. Extra people appear, or background people mouth the lines**
- **Cause:** Busy settings (cafés, streets) invite crowds. Ambiguous "they" references.
- **Prompt:** "Only one person in frame". An empty or controlled background.
- **Parameter:** `negativePrompt: "crowd, second person, background people, passers-by"`.
- **Post:** Regenerate. Hard to fix in post.
- Evidence: **INFERENCE only.** Note 05 found no source documenting this failure for Veo.

**F10. Identity drift: face changes across clips or during extension**
- **Cause:** Text-to-video re-imagines the face each call. Chaining last-frame→first-frame compounds error. Extension conditions only on the tail (about the last second). Lite has no reference images.
- **Prompt:** A frozen "character bible" text block that does not contradict the image. Minimal head turns. One camera move.
- **Parameter:** **i2v from the approved master still for every clip** (re-anchor, do not chain). First+last frame from the identity pack. Escalate to Veo 3.1 Fast r2v (≤3 assets) or Omni 1.1 (≤5 images) for multi-angle shots.
- **Post:** ArcFace identity QA against the master. Reject rather than fix.
- Evidence: OFFICIAL and GOOGLE-SAMPLE (see note 04 §1–§5). PRACTITIONER: "Character identity drift — Inconsistent references — Reuse same 1-3 references; keep wardrobe similar". OpenAI general guidance: "small changes in phrasing can alter identity". — [snubroot troubleshooting table](https://github.com/snubroot/Veo-3-Meta-Framework); [OpenAI Sora 2 guide](https://github.com/openai/openai-cookbook/blob/main/examples/sora/sora2_prompting_guide.ipynb); detail in note 04

**F11. Morphing hands, fingers or products in hand**
- **Cause:** Too many concurrent actions; small-object manipulation; hand-over-face.
- **Prompt:** One simple gesture, or hands still and low. No finger-counting or picking up small objects. Describe actions in beats ("raises the jar to chest height, pauses").
- **Parameter:** A start frame where the hand already holds the product correctly. 4–6 s clips.
- **Post:** Cut around the glitch, or regenerate.
- Evidence: PRACTITIONER ("Soft/smeared motion — Too many concurrent actions — Shorten to 4-6s; simplify action"); OFFICIAL OpenAI: "one clear camera move and one clear subject action… described in beats". — [snubroot](https://github.com/snubroot/Veo-3-Meta-Framework); [OpenAI Sora 2 guide](https://github.com/openai/openai-cookbook/blob/main/examples/sora/sora2_prompting_guide.ipynb)

**F12. Unnatural blinking, staring, plastic or waxy skin**
- **Cause:** "Beautiful/flawless" style words, an over-retouched master still, no micro-motion cues.
- **Prompt:** Official micro-motion phrases ("The subject blinks slowly", "A subtle smile appears…"), plus "unretouched skin with visible pores, flyaway hairs, slight sensor noise".
- **Parameter:** A realistic master still (image SOP).
- **Post:** Light film grain. No face-smoothing filters.
- Evidence: OFFICIAL vocabulary (GCP notebook); PRACTITIONER realism cues; inference for the "plastic" cause. — [veo3_video_generation](https://github.com/GoogleCloudPlatform/generative-ai/blob/main/vision/getting-started/veo3_video_generation.ipynb); detail in note 04 §6 and the still SOP

**F13. Camera ignores instructions (framing not held, "jump cut" not executed, unwanted cuts)**
- **Cause:** Image geometry dominates text in i2v. Edit verbs are read as style. Omni may add cinematic cuts.
- **Prompt:** One movement keyword. "One continuous shot with no cuts" (used in Google's own Omni sample).
- **Parameter:** **Compose the start frame as the framing you want**.
- **Post:** Do the cuts in the edit.
- Evidence: GOOGLE-SAMPLE ("may not execute literal edits like 'jump cut'"); PRACTITIONER ("arm's-length framing did not hold"); OFFICIAL Omni sample prompt "One continuous shot with no cuts." — [veo_guide.md](https://github.com/GoogleCloudPlatform/vertex-ai-creative-studio/blob/main/experiments/veo-genetic-prompt-optimizer/veo_guide.md); [dreampixelforge (search summary)](https://www.dreampixelforge.com/blog/veo-3-prompts); [gemini_omni_1_1_flash_video_gen](https://github.com/GoogleCloudPlatform/generative-ai/blob/main/vision/getting-started/gemini_omni_1_1_flash_video_gen.ipynb); detail in note 02 §5

**F14. Lighting, wardrobe or background shift between stitched clips**
- **Cause:** Varying descriptive language between prompts.
- **Prompt:** A fixed set, lighting and wardrobe block copied verbatim. Name 3–5 palette anchor colors.
- **Parameter:** The same master still or set still per scene. Lock aspect ratio for the project.
- **Post:** Color-match in the grade.
- Evidence: PRACTITIONER ("Lighting shifts between clips — Prompt language variance — Standardize 2-3 lighting descriptors"); OFFICIAL OpenAI ("Naming three to five colors helps keep the palette stable"). — [snubroot](https://github.com/snubroot/Veo-3-Meta-Framework); [OpenAI Sora 2 guide](https://github.com/openai/openai-cookbook/blob/main/examples/sora/sora2_prompting_guide.ipynb); [eastondev long-video (search summary)](https://eastondev.com/blog/en/posts/ai/20251207-veo3-long-video-guide/)

**F15. Audio artifacts: silent output, distracting ambience, level mismatch**
- **Cause:** A wrapper defaults audio off; a content filter strips the audio track while the video survives; the audio stage fails under load (third-party claims). Ambience mismatches between clips.
- **Prompt:** An explicit audio line per clip ("Audio: her voice only, quiet room tone").
- **Parameter:** `generateAudio: true` explicitly (Lite with-audio is priced separately). Regenerate on silent output.
- **Post:** Disable the ambience and rebuild the bed in the NLE. Loudness at about -14 LUFS (note 06 §Q4).
- Evidence: THIRD-PARTY (Imaginary: "a content filter can strip the audio track"); PRACTITIONER ("Distracting native audio — Disable and replace in NLE"). — [Imaginary (search summary)](https://www.imaginary.app/blog/veo3-no-audio-problem-guaranteed-sound); [snubroot](https://github.com/snubroot/Veo-3-Meta-Framework)

**F16. Safety refusals or blocked outputs with people**
- **Cause:** An input or output tripped a RAI filter, e.g. resemblance to a real or prominent person, a minor-looking subject, or brand/logo/IP content.
- **Prompt:** Clearly adult, fictional characters. No real names, celebrities or "looks like X". No real brand logos unless the client owns them.
- **Parameter:** `personGeneration: "allow_adult"`. Read the support code in the error or `raiMediaFilteredReasons` to identify the category. "If fewer videos than requested are returned, then some generated output is being blocked."
- **Post:** n/a.
- **Do not try to evade filters.** Use a fictional or licensed subject and the official support channels.
- Evidence: OFFICIAL (Vertex RAI page, search summary); THIRD-PARTY (remove named people and brands, add back only authorized elements). — [Veo responsible AI and usage guidelines (search summary)](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/video/responsible-ai-and-usage-guidelines); [veo3ai.io safety filters (search summary)](https://www.veo3ai.io/blog/veo-3-safety-filters-real-faces-logos-audio-prompt-rewrites-2026); detail in note 01 §3

**F17. Same artifact repeats on every retry, or output ignores small prompt edits**
- **Cause:** A fixed seed stuck in a "look rut", or an over-constrained prompt. Vertex's prompt rewriter (`enhancePrompt`, forced on for Veo 3.1 in Google's sample app) rewrites wording.
- **Prompt:** Change one variable at a time. Reduce adjectives.
- **Parameter:** Change the seed. Request 2–4 samples.
- **Post:** n/a.
- Evidence: PRACTITIONER ("Repeated artifacts — Seed stuck; over-constrained — Change seed; reduce adjectives"); GOOGLE-SAMPLE (rewriter forced on, see note 02 §7). — [snubroot](https://github.com/snubroot/Veo-3-Meta-Framework); [vertex-ai-creative-studio config](https://github.com/GoogleCloudPlatform/vertex-ai-creative-studio/blob/main/config/veo_models.py)

**Generic QA gate (applies to all of the above)**
- Google ships a video rubric:
  - "Visual Quality & Artifacts… flickering, unnatural textures, or object morphing";
  - "Motion Coherence";
  - an audio rubric with "Prompt Fidelity (Style/Tone/Accent)" and "Speaker Consistency".
- Google's agent notebooks reject clips before extending: "Never accept uninspected footage".
- Practitioner planning figure: "about three generations per usable shot".
— [veo_video_eval_templates.py](https://github.com/GoogleCloudPlatform/vertex-ai-creative-studio/blob/main/experiments/veo-genetic-prompt-optimizer/veo_genetic_prompt_optimizer/veo_video_eval_templates.py); [config/evaluators.py](https://github.com/GoogleCloudPlatform/vertex-ai-creative-studio/blob/main/config/evaluators.py); [cookbook Autonomous_video_production](https://github.com/google-gemini/cookbook/blob/main/examples/Autonomous_video_production_with_omni_and_agents.ipynb); [Hackernoon (search summary)](https://hackernoon.com/how-to-extend-an-ai-generated-video-clip-past-its-length-limit-without-the-drift)

### Inferences
- **Map from the client's pain points to failures and the strongest fix:**
  - (1) voice changes → F3 → STS voice lock in post (guaranteed), or audio-driven avatar (§1).
  - (2) neutral accent → F4 → audio-first: an Argentine TTS/STS track, then avatar or lip-sync (guaranteed); in-model wording is only best-effort.
  - (3) identity drift when extending → F10 → re-anchor every clip on the master still; for >8 s continuity use Omni extension or an audio-driven avatar instead of Veo chaining.
  - (4) realism → F7, F11, F12, F13 → micro-motion vocabulary, one action, realistic still, QA.
  - (5) multi-character confusion → F5, F9 → one speaking face per clip, visible-descriptor attribution.
  - (6) "first-try quality" → an automated QA gate with 2–4 samples, because no prompt reaches 100% first-try.
- **Jarvis pre-flight lint** (derived from the catalog), run before every Veo call:
  1. No `"` around dialogue.
  2. Words ≤ budget for `durationSeconds`.
  3. ≤1 speaker with lines per clip, unless the format requires 2.
  4. Each line attributed to a visible descriptor.
  5. Character, voice and set blocks byte-identical to the bible.
  6. Exactly one camera-move keyword.
  7. No readable text requested.
  8. `negativePrompt` includes text/caption terms.
  9. `personGeneration=allow_adult`, `generateAudio=true`.
  10. A start image is attached for every shot with a person.

### Gaps
- No official Google troubleshooting page for Veo 3.1 Lite was readable. docs.cloud.google.com is blocked, so official statements above are search summaries.
- No quantitative failure rates (e.g. % of clips with captions or wrong speaker) for Lite.
- No source documents "extra people" (F9) or silent-audio-by-filter (F15) from Google itself.

---

## 5. Benchmarks and leaderboards for video models (Artificial Analysis, Arena) as of Oct 2026

### Takeaway
On **Arena** (formerly LMArena; the Sep 21, 2026 update, scraped Oct 7):
- **Text-to-video:** Google's **Gemini Omni 1.1 Flash (1516)** and **Omni Flash (1513)** lead, ahead of FLUX 3 Video, Grok Imagine 1.5, Seedance 2.0, Wan 3.0, Seedance 2.5 and MiniMax H3.
- **Image-to-video:** **MiniMax H3 is #1 (1495)**.
- **Veo 3.1 / 3.1 Fast** sit around **#12–15 in T2V (≈1358–1364)** and **#13–17 in I2V (≈1372–1398)**. Fast is statistically tied with full Veo 3.1.
- **Veo 3.1 Lite is not listed** on any board found.

**Artificial Analysis** snapshots conflict by board version: Wan 3.0, Gemini Omni Flash and HeyGen Video 1 each appear at the top in different snapshots. None of these leaderboards measures Spanish accent, voice consistency or identity across clips, so they **cannot decide the client's tool choice alone**.

### Cited Findings
- [Scraped OFFICIAL data] Arena text-to-video, `last_updated: "Sep 21, 2026"`, 48 models:
  1. gemini-omni-1.1-flash 1516 ±15
  2. gemini-omni-flash 1513 ±9
  3. flux-3-video 1493
  4. grok-imagine-video-1.5-agent 1492
  5. dreamina-seedance-2.0-720p 1479
  6. wan3.0 1476
  7. dreamina-seedance-2.5-720p 1474
  8. minimax-h3 1460
  9. muse-video (Meta) 1456
  10. happyhorse-1.0 1427
  11. sora-2-pro 1368
  12. veo-3.1-audio 1364
  13. veo-3.1-audio-1080p 1362
  14. veo-3.1-fast-audio 1362
  15. veo-3.1-fast-audio-1080p 1358
  - 27: runway-gen-4.5 1225
  - 29: kling-2.6-pro 1216
  - 32: hailuo-2.3 1206
  — [arena-ai-leaderboards data/2026-10-07/text-to-video.json](https://github.com/oolong-tea-2026/arena-ai-leaderboards/tree/main/data/2026-10-07); source page [arena.ai text-to-video](https://arena.ai/leaderboard/video/text-to-video)
- [Scraped OFFICIAL data] Arena image-to-video (Sep 21, 2026):
  1. minimax-h3 1495 ±5
  2. gemini-omni-1.1-flash 1488
  3. wan3.0 1480
  4. seedance-2.5 1477
  5. seedance-2.0 1475
  6. gemini-omni-flash 1465
  - 13: veo-3.1-audio 1398
  - 15: veo-3.1-fast-audio 1385
  - 19: kling-v3-pro 1354
  - 29: hailuo-2.3 1262
  - 47: runway-gen4-turbo 1052
  Video-edit (Aug 26, 2026): 1. wan3.0 1414; 2. seedance-2.5 1410; 3. minimax-h3 1392; 4. gemini-omni-flash 1367; 8. kling-o3-pro 1255; 10. runway-gen4-aleph 1182. **No `veo-3.1-lite` entry exists on any board.** — [arena-ai-leaderboards](https://github.com/oolong-tea-2026/arena-ai-leaderboards)
- [OFFICIAL, search summary] Artificial Analysis marked two years of its Video Arena on Oct 21, 2026. It has boards for text-to-video, image-to-video, **video with audio** and video editing, and has benchmarked 140+ models. — [Artificial Analysis on X](https://x.com/ArtificialAnlys/status/2112992234140475837)
- [OFFICIAL pages, search summary, **inconsistent snapshots**]
  - AA-Video-T2V v2.1: Wan 3.0 1175, Utopai X 1167, HeyGen Video 1 1160. Page metadata "about 194 days old", which conflicts with Wan 3.0's Aug 2026 release, so the snapshot is unreliable.
  - AA-Video-I2V v1.1: MiniMax H3 (768p) 1140, FLUX 3 Max 1138.
  - AA-Video-Editing v1.1: Wan 3.0 1198.
  - An August 2026 guide: "Gemini Omni Flash leads text-to-video with audio at 1245 Elo, just ahead of MiniMax-H3".
  — [AA T2V leaderboard](https://artificialanalysis.ai/video/leaderboard/text-to-video); [AA I2V leaderboard](https://artificialanalysis.ai/video/leaderboard/image-to-video); [AA video-editing leaderboard](https://artificialanalysis.ai/video/leaderboard/video-editing); [invideo dated rankings](https://invideo.io/blog/best-ai-video-model/); [benchmarklist scrape](https://benchmarklist.com/arenas/artificial_analysis_text_to_video/)
- [THIRD-PARTY, different scale] llm-stats reports "Kling v3… 1934, followed by Happy Horse 1.0 (1816) and Seedance 2.0 Fast (1747)". This is not comparable with Arena or AA. — [llm-stats](https://llm-stats.com/leaderboards/best-ai-for-video-creation)
- [search summary] LMArena added video in Jan 2026 and rebranded to "Arena" on Jan 28, 2026. — [Wikipedia: Arena (AI platform)](https://en.wikipedia.org/wiki/Arena_(AI_platform))

### Inferences
- **Arena reads Veo 3.1 Fast ≈ Veo 3.1** (1362 vs 1364 T2V, within CI). Fast is $0.12/s vs $0.40/s at 1080p with audio (note 01). So Fast, not full Veo 3.1, is the cost-efficient escalation for hero shots. Lite's relative quality is unmeasured; the client should run its own blind pairwise test (Google's rubric, §4).
- Gemini Omni's ~150-point lead over Veo 3.1 on Arena T2V is large. Combined with reference images and 10 s extension, it is the strongest *same-platform* upgrade path for multi-character storytelling. Cost is roughly 2× Lite.
- Leaderboards reward general visual preference in short, mostly English clips. The client's acceptance criteria are Argentine accent, the same voice across clips, the same face across clips and correct speaker attribution. These need an **internal benchmark**: 20 fixed scripts × candidate tools, scored by the §4 QA gate plus human Argentine raters.

### Gaps
- No live access to arena.ai or artificialanalysis.ai. The Arena data is a third-party scrape (Sep 21 update, fetched Oct 7), and the AA numbers are inconsistent search summaries.
- No leaderboard covers avatar/lip-sync tools (HeyGen, OmniHuman, Hedra) head-to-head, or any Spanish-language audio quality.
- Veo 3.1 Lite has no public benchmark.
