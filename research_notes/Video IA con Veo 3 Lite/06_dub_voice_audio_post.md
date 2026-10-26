# Dub Voice and audio post-production for AI UGC video (Veo 3.1 Lite pipeline)

> **Research date:** 2026-10-26.
>
> **Source access.** The proxy blocked page fetches to dubvoice.ai, elevenlabs.io, sync.so, vp-land.com and Product Hunt. Claims from those sites are marked **(search summary)** and are weaker evidence.
>
> **Primary sources read in full**, cloned from public GitHub:
> - `elevenlabs/skills`. HEAD 2026-10-23, maintained by ElevenLabs and synced weekly from its changelog.
> - `elevenlabs/elevenlabs-python/reference.md`. HEAD 2026-10-20, the auto-generated SDK reference.
> - `synchronicity-labs/sync-python-sdk` and `sync-typescript-sdk`. HEAD 2026-04-06. These are **more than 6 months old** and may lag the live API.
> - Google's `GoogleCloudPlatform/generative-ai` audio notebooks. HEAD 2026-10-26.
>
> **Related sibling notes:**
> - `01_veo_vertex_specs.md`: model ID `veo-3.1-lite-generate-001`, `generateAudio`, video-only SKUs.
> - `03_voz_acento_argentino.md`: Veo accent prompting, Gemini 3.8 Flash TTS, first DubVoice pass.
> - `04_identidad_extension.md`
>
> This note does not repeat those notes. It adds vendor-level detail and the post-production pipeline. Synthetic or fictional people only. Nothing here is meant to remove or evade AI labels or watermarks.

---

## Q1. What is "Dub Voice" / "DubVoice" / "Dove Voice"?

### Takeaway
The only product that matches the name and the client's use is **DubVoice.ai** (www.dubvoice.ai). It is a credit-based **aggregator**, not a model maker. It offers:
- TTS with 17,800+ voices "across 6 providers".
- Voice cloning from about 10 s of audio.
- A voice changer (STS).
- Auto-dubbing in "50+" languages.
- Video generation: Veo 3.1, Grok Imagine, Omni Flash.
- A "UGC Studio" with lip-synced AI creators.
- A REST API at `/api/v1`.

No product called "Dove Voice" exists. The company, founders and launch date could not be found. Every DubVoice fact below is the vendor's own claim, and its pages contradict each other.

### Cited Findings
**What it is**
- DubVoice.ai describes itself as "17,800+ voices across 6 providers in 50+ languages, Veo 3.1 / Grok Imagine / Omni Flash video, 6 image models, AI music, speech-to-text, voice cloning and a developer API — all on one credit balance". — [dubvoice.ai (search summary)](https://www.dubvoice.ai/); [What is DubVoice.ai (search summary)](https://www.dubvoice.ai/ru/what-is-dubvoice)
- A July 2026 vendor post, "What's New on DubVoice.ai", announces "3 New Voice Providers, Meta AI Video, YouTube Videos & UGC". An older dubbing page cites "10500+ premium voices across 3 providers", so the counts conflict between pages. — [DubVoice What's New 2026 (search summary)](https://www.dubvoice.ai/blog/whats-new-2026-new-voice-providers-video-models-youtube-ugc); [DubVoice AI dubbing page (search summary)](https://www.dubvoice.ai/use-cases/text-to-speech-use-cases/ai-voice-dubbing)
- The names of the six providers are **not published** in anything I could reach. — [search summary, no provider list found](https://www.dubvoice.ai/llms-full.txt)

**Features**
- **API.** "a full REST API at /api/v1 that covers text-to-speech, voice cloning, and speech-to-text". — [DubVoice FAQ (search summary)](https://www.dubvoice.ai/faq)
- **Cloning.** "record or upload a 10-second clean voice sample… the clone is ready for TTS, dialogue, and dubbing". Clones "never expire" and "a commercial license is included". Other pages say 5–15 s. — [DubVoice FAQ (search summary)](https://www.dubvoice.ai/faq)
- **Voice changer (STS).** It transforms audio into any of the 17,800+ target voices "at 2,000 credits/minute". — [DubVoice FAQ / pricing (search summary)](https://www.dubvoice.ai/pricing)
- **Auto Dubbing.** "50+ languages with synced SRT, 30,000 credits/task", stated elsewhere as about $0.60–$0.90 per file. — [DubVoice dubbing guide (search summary)](https://www.dubvoice.ai/blog/ai-voice-dubbing-guide)
- **UGC Studio.** You pick one of **20 AI creators**, or upload your own. You write the script and attach a product photo. The script is "split into clips, filmed and stitched into one video — with lip-sync generated alongside the footage". **UGC Studio is dashboard-only with no API.** — [DubVoice FAQ (search summary)](https://www.dubvoice.ai/faq)
- **Lip-sync conflict.** Marketing copy calls dubs "lip-sync ready", but the company's July 2026 post reportedly says lip sync on generated video is still not solved. — [DubVoice What's New 2026 (search summary)](https://www.dubvoice.ai/blog/whats-new-2026-new-voice-providers-video-models-youtube-ugc)

**Pricing (one-time credit packs, "credits never expire", no auto-renew)**

The site's own pages disagree on prices:

| Pack | Credits | FAQ | Pricing page | Homepage |
|---|---|---|---|---|
| Starter | 250K | $4.99 | $4.99 | $4.99 |
| Business | 10M | — | $34.99 | $49.99 |
| Enterprise | 20M | — | $64.99 | $94.99 |
| Ultimate | 40M | $110 | — | $179.99 |

- Optional monthly plans exist, such as "Image Max" ($15/mo) and "Veo Max". Monthly plans don't apply to API usage. — [DubVoice pricing (search summary)](https://www.dubvoice.ai/pricing); [DubVoice FAQ (search summary)](https://www.dubvoice.ai/faq)

**Consent and licensing (Terms)**
- Users must confirm they have the legal consents and rights to clone what they upload. "Explicit written permission" is needed to clone another person's voice, and a consent checkbox must be ticked for every cloning attempt.
- Prohibited uses are fraud, deepfakes, misinformation and impersonation. Cloning public figures needs their explicit authorization.
- The FAQ's "clone any voice" wording sits uneasily with the Terms. — [DubVoice Terms (search summary)](https://www.dubvoice.ai/terms); [DubVoice FAQ (search summary)](https://www.dubvoice.ai/faq)

**Argentine Spanish**
- No DubVoice page found lists Argentine or rioplatense voices.
- The underlying market does have them: ElevenLabs has an Argentine-accent library (e.g. "Agustín, Conversational, Argentine"), and JSON2Video catalogs 47 Spanish-Argentina TTS voices from ElevenLabs and Microsoft Azure. — [ElevenLabs Argentine accent (search summary)](https://elevenlabs.io/text-to-speech/argentine-accent); [json2video (search summary)](https://json2video.com/ai-voices/languages/spanish/argentina/)

**Other names checked**
- **"Dove Voice":** a search found no product. Results were only Dove Cameron voice imitations, which are a consent problem and must not be used, and Dove the soap brand's no-AI pledge. — [search results: Fish Audio](https://fish.audio/m/1d447bcb23404d778277c3f891597d53); [ContentGrip on Dove campaign](https://www.contentgrip.com/doves-new-campaign-rejecting-ai-alterations/)
- **Similar names that are different products:**
  - **VoiceDub**: AI song covers and cloning. — [toolify (search summary)](https://www.toolify.ai/tool/voicedub-ai)
  - **Dub AI**: an iOS cloning app at $7.99/week. — [App Store (search summary)](https://apps.apple.com/mt/app/dub-ai-voice-cloning-ai/id6474446615)
  - **Dubbing AI**: a real-time voice-changer app. — [dubbingai.io (search summary)](https://dubbingai.io/voice-changer)
  - **Dubverse**: Indian AI dubbing SaaS founded 2021, Product Hunt Jan 2022. — [YourStory](https://yourstory.com/2022/07/dubverse-saas-startup-breaking-language-barriers-ai)

### Inferences
- **Most likely match: DubVoice.ai.** It is the only exact name match, it was active in 2026, and it explicitly bundles Veo 3.1, UGC and Spanish dubbing. "Dove Voice" is almost certainly a transcription of "Dub Voice".
- **Quality depends on the underlying providers.** Because DubVoice aggregates other providers' engines, its quality for voice changing, Argentine accent and lip-sync will equal whichever provider it routes to. The ElevenLabs, Sync and Google facts in Q2–Q4 are therefore the real technical constraints. One example: STS keeps the **source** accent, which very likely applies on DubVoice too, though this is unverified.
- **Credit cost at pack prices (my arithmetic):**
  - Voice changer at 2,000 credits/min is about **$0.04/min** on Starter ($4.99/250K) and about **$0.0055–0.009/min** on Ultimate.
  - A 30 s ad costs under $0.02 to re-voice.
  - Dubbing at 30,000 credits/task is about $0.60 on Starter.
- **Prefer the API over UGC Studio for production.** UGC Studio has no API and its 20 stock creators cannot be driven by Jarvis. Use DubVoice's API for TTS, cloning and STS, and keep Veo 3.1 Lite on Vertex for video. Don't hand identity to DubVoice's UGC Studio.
- **Questions to ask the vendor before integrating:**
  1. Which 6 providers it uses, and which one serves STS.
  2. Whether it has Argentine or rioplatense voice IDs, and whether voice IDs are stable.
  3. Whether the API exposes the voice changer and dubbing, or only TTS, cloning and STT.
  4. Whether it offers lip-sync via API.
  5. Data retention terms.
  6. Whether output carries C2PA or a watermark.
  7. Whether it supports a seed or determinism.

### Gaps
- I could not identify the company, founders or launch date. There is no Product Hunt listing in the results and the site was unreachable.
- The provider list, STS model, Argentine voices and API endpoints beyond the FAQ are unverified.
- There are no independent reviews of DubVoice. No 2026 roundup cited it (see also `03_voz_acento_argentino.md`).
- It is not confirmed that DubVoice.ai is the tool the client means. The client should confirm the URL or login.

---

## Q2. Keep Veo native audio or replace it? How to lock one voice per avatar and get a real Argentine accent

### Takeaway
**The key 2026 fact:** in voice-changer (STS) tools, **accent and cadence come from the source recording, not the target voice**. This is official ElevenLabs guidance.

So STS fixes **timbre drift**: different-sounding voices between clips. It does **not** fix a neutral accent. There are three deterministic routes to a guaranteed rioplatense accent with one fixed voice:
- **(a)** Keep a Veo take whose accent already passed QA, then run STS to one fixed voice.
- **(b)** Use TTS with an Argentine-native or designed voice, then lip-sync.
- **(c)** Record a consenting Argentine human "guide track", run STS to the avatar's fixed synthetic voice, then lip-sync.

Veo itself has no voice-ID or voice-persistence parameter.

### Cited Findings
**Veo side**
- Veo 3.1 Lite exposes `generateAudio`. Video-only SKUs cost about 40% less ($0.05 vs $0.08/s at 1080p). — [sibling note 01, from Agent Platform pricing](https://cloud.google.com/gemini-enterprise-agent-platform/generative-ai/pricing)
- A third-party page that says it checked Google docs in Aug 2026 reports "no voice selection parameter in the documented Veo 3.1 interface". It says "Google publishes no voice-persistence mechanism" and calls cross-clip voice matching "a known weak spot".
  - The same page claims audio is always on. That **conflicts** with the official `generateAudio` parameter.
  - The search summary did not clearly attribute which result page said this. — [search summary; results incl. prompt-architects.com](https://prompt-architects.com/blog/101-veo-dialogue-prompts); [versely.studio](https://www.versely.studio/blog/veo-3-1-complete-guide-google-ai-video-model)

**ElevenLabs Voice Changer (STS)**

All points below come from [elevenlabs/skills voice-changer SKILL.md](https://github.com/elevenlabs/skills/blob/main/voice-changer/SKILL.md). The accent note was added 2026-05-01. The file was last edited 2026-10-18.
- STS "keeps the original performance — emotion, pacing, intonation, breaths, whispers, laughs, cries — and only swaps who is speaking".
- Official warning: "**Accent and cadence transfer from the source, not the target.** If you read in an American accent and target the British 'George' voice, you get George's timbre with an American accent. To dub *into* a different accent or language, record someone speaking in that target accent/language and convert into a cloned/library voice."
- Limits: 5 min and 50 MB per request.
- Cost: "1,000 characters per minute of audio processed".
- Recommended model: `eleven_multilingual_sts_v2` (29 languages). Its Spanish is listed as "Spanish (ES, MX)", with no AR variant.
- Parameters:
  - `voice_settings`: stability, similarity_boost, style, speaker boost.
  - `seed`: "best-effort deterministic".
  - `remove_background_noise`.
- Input rules: "Be expressive… Flat input gives you flat output". "Clean up noise first… Noise hurts more here than in TTS." "Cut at natural pauses" when chunking.

**ElevenLabs TTS (Eleven v4, new)**

From [elevenlabs/skills text-to-speech SKILL.md](https://github.com/elevenlabs/skills/blob/main/text-to-speech/SKILL.md) and [voice-settings.md](https://github.com/elevenlabs/skills/blob/main/text-to-speech/references/voice-settings.md). The release dates come from the [elevenlabs/skills commit history](https://github.com/elevenlabs/skills/commits/main).
- **Release:** `eleven_v4` and `eleven_v4_turbo` were added to the skills in the update from the **2026-09-28 changelog**. They became the default on **2026-10-05**.
- **Capabilities:** 90+ languages. Positioned as "Highest quality, emotional range, audio tags, voice cloning accuracy".
- **Limits:** v4 supports only `stability` and `similarity_boost`, with no `style` or `speed` and **no SSML**. Pacing and emotion come from audio tags (`[whispers]`, `[laughs]`, `[sighs]`, `[excited]`) and punctuation: "ellipses for pauses, capitals for emphasis".
- **`language_code`:** an ISO 639-1 code that "enforce[s] a language". This is language level only (`es`), with no regional tag.
- **Request stitching:** `previous_text` / `next_text` so that multi-request audio has no "pops, unnatural pauses, or tone shifts at the boundaries".
- **Presets:** conversational `stability=0.4, similarity_boost=0.75`. Character/drama `0.3 / 0.8`.
- **Accent rule (from sibling note 03):** "The accent used when generating audio comes from the voice that you use". — [ElevenLabs help center (search summary, cited in note 03)](https://elevenlabs.io/docs/help-center/product/core-capabilities/text-to-speech/how-do-i-select-the-language-and-accent.md)

**Voice design (fictional, persistent voices)**

From [elevenlabs-python reference.md](https://github.com/elevenlabs/elevenlabs-python/blob/main/reference.md):
- `client.text_to_voice.design(voice_description=…, model_id="eleven_ttv_v3" | "eleven_multilingual_ttv_v2", text=… [100–1000 chars])` returns previews, each with a `generated_voice_id`.
- `client.text_to_voice.create(generated_voice_id=…)` saves the voice.
- `text_to_voice.remix(voice_id, voice_description="…")` edits an existing voice.
- `client.voices.accents.get(language=…, model_id=…)` lists available accents in the shared library.
- Voices can carry `labels` with keys "language, accent, gender, or age".

**Multi-character dialogue TTS**
- **ElevenLabs:** `client.text_to_dialogue.convert(inputs=[DialogueInput(text, voice_id), …])`. "The maximum number of unique voice IDs is 10." For reliable generation keep "≤2,000 characters per request". A `convert_with_timestamps` variant returns timestamps plus **voice segments**. — [elevenlabs-python reference.md](https://github.com/elevenlabs/elevenlabs-python/blob/main/reference.md)
- **Google (official sample):** "Gemini Text-to-Speech can only generate audio with 2 speakers maximum, so each line is synthesized separately (in parallel) and stitched back together in script order."
  - The sample maps each character to a prebuilt voice (e.g. narrator "Zubenelgenubi") using `random.shuffle` by gender.
  - Output is 24 kHz 16-bit mono PCM.
  - The TTS model in the sample is `gemini-3.1-flash-tts-preview`. — [GCP storytelling.ipynb](https://github.com/GoogleCloudPlatform/generative-ai/blob/main/audio/speech/use-cases/storytelling/storytelling.ipynb); [GCP multi-speaker-podcast.ipynb](https://github.com/GoogleCloudPlatform/generative-ai/blob/main/audio/speech/use-cases/podcast/multi-speaker-podcast.ipynb)
- **Gemini 3.8 Flash TTS:** "up to 2 different speakers" per request. Designed voices expire after 7 days on the Gemini API. AI-generated audio can't be used as replication reference. See [sibling note 03 / GCP gemini_3_8_flash_tts](https://github.com/GoogleCloudPlatform/generative-ai/blob/main/audio/speech/getting-started/gemini_3_8_flash_tts.ipynb).

**Dubbing APIs (when the source isn't Spanish)**
- The ElevenLabs Dubbing Projects API (`dubbing.project.*`) takes BCP-47 targets "for example `fr` or `es-MX`" and requires "a region-qualified tag must be one of the supported dialects".
- `cloning_strength` runs 0–10, default 7, and "controls how strongly dubbed speakers clone the source voices".
- The legacy `dubbing.create` has an "[Experimental]" `target_accent` "to inform translation of the dialect to prefer".
- Transcript editing and regeneration are enterprise-only. — [elevenlabs/skills dubbing SKILL.md](https://github.com/elevenlabs/skills/blob/main/dubbing/SKILL.md); [elevenlabs-python reference.md](https://github.com/elevenlabs/elevenlabs-python/blob/main/reference.md)

### Inferences
**Decision tree for the SOP** (refines note 03's A/B/C)

1. **Single 8 s clip, one speaker, Veo accent passes QA.** Keep Veo native audio. No post needed beyond loudness (Q4).
2. **Several clips, or an extended video, of the same avatar, accent OK.** Keep Veo audio, since its lip motion is native. Then:
   - Isolate dialogue with Voice Isolator or `remove_background_noise=True`.
   - Run STS on **all of that character's lines** to the avatar's **one fixed `voice_id`**, with a fixed `seed` and fixed `voice_settings`.
   - Remix.
   - Timing is unchanged, so **no re-lip-sync** is needed.
   This kills voice drift. It cannot add accent.
3. **Veo keeps giving neutral Spanish (pain point 2).** STS will NOT fix it. Use one of:
   - **3a. TTS route.** Use an Argentine-native library voice or a designed rioplatense voice with Eleven v4, `language_code="es"`, a script written in voseo, and audio tags. Then lip-sync the Veo clip to the new audio (Q3).
   - **3b. Guide-track route** (best prosody, inference). A paid, consenting Argentine voice actor reads the lines. STS converts them to the avatar's synthetic `voice_id`. Then lip-sync. This is exactly ElevenLabs' documented recipe for dubbing "into a different accent".
4. **Script edit after generation.** TTS for the changed line, plus lip-sync on that shot only.

**Voice bible per avatar** (pairs with the image SOP's identity sheet). Jarvis stores and reuses:
- `avatar_id`
- `voice_provider`
- `voice_id`
- `model_id`
- `voice_settings`
- `seed`
- `language_code`
- `audio_effects` preset
- 2–3 reference lines

Never re-pick voices per job. Google's sample uses `random.shuffle`, which would cause pain point 1 in production.

**Designed voices fit synthetic avatars** (inference). They are fictional, so there is no real person to consent, and they persist as a saved `voice_id`. Gemini designed voices expire in 7 days, so for recurring avatars prefer ElevenLabs or DubVoice saved voices, or a Gemini Extended Voice Library preset ID.

Example design prompt (Spanish, since the description drives accent; to test):

> "Mujer argentina de 27 años, porteña, acento rioplatense marcado con sheísmo y voseo, voz cálida y cercana, ritmo conversacional rápido, grabada con celular en un living, sin tono de locutora."

Check the result with `voices.accents.get(language="es")` and label it `accent: argentine`.

**Multi-character formats (pain point 5)**
- One `voice_id` per character, kept in the voice bible.
- Generate dialogue audio with **ElevenLabs Text to Dialogue** (up to 10 voices, ≤2,000 characters per request). Use `convert_with_timestamps` to get per-speaker segments, then cut the audio per shot.
- With Gemini TTS, synthesize **line by line** (2-speaker limit) and keep the speaker→voice map fixed.
- Then lip-sync each shot to its speaker's segment (Q3).

**Cost of keeping Veo audio on.** When post will replace the voice, pay for Veo audio only on the STS route (2). Routes 3a and 3b still benefit from a Veo take *with* speech (natural jaw, head and breath motion as input to lip-sync), but this is untested. Testing video-only plus lip-sync could save about $0.03/s.

### Gaps
- It is unclear whether ElevenLabs' Dubbing Projects API accepts `es-AR` as a "supported dialect". The supported-dialect page was blocked.
- There is no independent test of Eleven v4 rioplatense quality, or of whether a designed voice reliably keeps sheísmo and voseo intonation.
- The exact `voices.accents.get(language="es")` output is unknown, so it is unverified whether "argentine" is a filterable accent label. Run it in the client's account.
- DubVoice's STS engine and whether it shares ElevenLabs' accent behaviour are unverified.
- No source compares STS-on-Veo-audio against TTS+lip-sync for perceived realism in Spanish UGC.

---

## Q3. Lip-sync re-alignment after re-voicing (Sync Labs sync-3 / lipsync-2-pro / react-1, others)

### Takeaway
Re-sync lips only when words or timing change (routes 3a, 3b and 4). STS that keeps timing doesn't need it.

**Sync Labs** (sync.so) is the most API-ready option and the only one whose parameters I could verify from code. Its models are `sync-3` (launched about 2026-04-06), `lipsync-2-pro`, `lipsync-2` and `react-1`. Options include:
- `active_speaker_detection` for multi-person shots.
- `segments` with different audio per time range.
- `sync_mode` for length mismatch.
- `temperature` for expressiveness.
- `occlusion_detection_enabled`.

Independent quality evidence is thin and conflicting.

### Cited Findings
**Model enum and options (SDK code, 2026-04-06)**
- Model enum: `"lipsync-2", "lipsync-1.9.0-beta", "lipsync-2-pro", "react-1", "sync-3"`. — [sync-python-sdk model.py](https://github.com/synchronicity-labs/sync-python-sdk/blob/main/src/sync/common/types/model.py); [sync-typescript-sdk](https://github.com/synchronicity-labs/sync-typescript-sdk)
- `GenerationOptions` (from [generation_options.py](https://github.com/synchronicity-labs/sync-python-sdk/blob/main/src/sync/common/types/generation_options.py)):
  - `sync_mode` handles "duration mismatches between video and audio". Values are `bounce | loop | cut_off | silence | remap`. — [sync_mode.py](https://github.com/synchronicity-labs/sync-python-sdk/blob/main/src/sync/common/types/sync_mode.py)
  - `temperature`: "how expressive lipsync can be. 0 -> least expressive, 1 -> most expressive. default:0.5".
  - `active_speaker_detection`: "automatically detects and applies lipsync only to the active speaker in videos with multiple people". Sub-fields are `auto_detect`, `frame_number` + `coordinates` [x,y] for manual selection, or per-frame `bounding_boxes`. — [active_speaker.py](https://github.com/synchronicity-labs/sync-python-sdk/blob/main/src/sync/common/types/active_speaker.py)
  - `occlusion_detection_enabled`: "slows down generation speed".
  - `model_mode` (react-1 only) sets the edit region: "lips/face/head". "When head is selected, model generates natural talking head movements along with emotions + lipsync".
  - `prompt` (react-1 only) is an emotion prompt. "Only single word emotions are supported".
- **`segments`:** "defining one or more video segments with different audio inputs for each segment". Each has `startTime`/`endTime` and an audio `refId`. — [generation_segment.py](https://github.com/synchronicity-labs/sync-python-sdk/blob/main/src/sync/common/types/generation_segment.py); [create_generation_dto.py](https://github.com/synchronicity-labs/sync-python-sdk/blob/main/src/sync/common/types/create_generation_dto.py)
- **Audio input:** either a recorded audio URL or a TTS input whose only provider type is `ElevenLabs`. — [tts_provider_config.py](https://github.com/synchronicity-labs/sync-python-sdk/blob/main/src/sync/common/types/tts_provider_config.py)
- **Webhooks:** a `webhook_url` gets a POST on completion. — [create_generation_dto.py](https://github.com/synchronicity-labs/sync-python-sdk/blob/main/src/sync/common/types/create_generation_dto.py)

**sync-3 launch and claims**
- Launch date: early April 2026. VP Land covered it on 2026-04-06, and Sync's blog post is dated 2026-04-06. Other listings say May or Aug 2026 (conflict). — [VP Land (search summary)](https://www.vp-land.com/stories/sync-labs-launches-sync-3-to-handle-the-complex-scenes-that-break-other-lipsync-models); [sync.so blog (search summary)](https://sync.so/blog/sync-3-most-intelligent-lipsync-model)
- Sync's claims: "up to 4K at 60fps". It targets "multiple speakers in frame, low-light interiors, overlapping dialogue, and long continuous takes with shifting camera angles". — [VP Land (search summary)](https://www.vp-land.com/stories/sync-labs-launches-sync-3-to-handle-the-complex-scenes-that-break-other-lipsync-models)
- WaveSpeed describes it as a "16-billion-parameter… zero-shot" model needing no "speaker enrollment". This is a third-party claim. — [WaveSpeedAI (search summary)](https://wavespeed.ai/blog/posts/introducing-sync-lipsync-3-on-wavespeedai/)
- A "real dubbing mode" (lipsync plus translation in one click) was added to sync-3. — [Quasa (search summary)](https://quasa.io/media/sync-just-added-real-dubbing-mode-to-sync-3-lipsync-translation-in-one-click)

**Independent evidence**
- A June 2026 comparison rated sync.so "Medium" quality and "Single-face only". The methodology is unknown, and it may predate sync-3 adoption. This conflicts with sync-3's multi-speaker claims. — [Vozo (search summary, cited in note 03)](https://www.vozo.ai/zh/blogs/best-lip-sync-software)
- A vendor recommends "voiceover overlay for AI-generated UGC ads", keeping lip-sync for direct-to-camera shots, "since overlay avoids mouth-movement inconsistency". — [invideo FAQ (search summary)](https://invideo.io/faq/should-i-use-lip-sync-or-voiceover-overlay-for-ai/)
- Kling's separate lip-sync and Runway's speech tools are mentioned as alternatives for adding speech after silent generation. — [search summary of Veo 3.1 guides](https://www.versely.studio/blog/veo-3-1-complete-guide-google-ai-video-model)

### Inferences
**Recommended Sync call for a re-voiced single-speaker UGC shot** (parameters from the SDK; values are starting points to test):
- `model="sync-3"`. Fall back to `lipsync-2-pro`.
- `input=[Video(url=<Veo clip>), Audio(url=<final voice WAV>)]`
- `options`:
  - `sync_mode="cut_off"`. Trim the audio to the shot so nothing loops.
  - `temperature` 0.4–0.6.
  - `occlusion_detection_enabled=True` when hands or product cross the mouth.
- `webhook_url` for Jarvis.

**Two-shot or podcast with both faces visible:**
- Use `segments` (one per line, `refId` per character's audio).
- Add `active_speaker_detection` with `frame_number` + `coordinates` per speaker, or `bounding_boxes`.
- Better (lower risk): shoot **one speaking face per clip**, as notes 02 and 04 recommend, so lip-sync never has to choose.

**react-1 for flat performances.** Use react-1 with `model_mode="lips"` or `"face"` when the Veo performance is fine but the expression is flat. **Avoid `head`** on identity-critical avatars. Regenerating head motion is a new source of feature drift (pain point 3). This is an inference and untested.

**Lip-sync QA** (extends note 03's checklist):
- Bilabials p/b/m close.
- Rioplatense "sh" (ll/y) shows rounded lips.
- Teeth and tongue don't smear.
- The face crop matches the identity sheet. Lip-sync models re-render the lower face, so compare chin, lip shape and moles against the reference.
- No mouth motion on the listener.

### Gaps
- The Sync docs repo on GitHub is from 2024, and the SDKs are from 2026-04-06. sync.so pricing per second, max duration, max resolution per model, and any post-April models (e.g. a "sync-3 pro") could not be verified.
- There is no independent measured comparison (LSE-C/LSE-D, human preference) of sync-3, HeyGen, Kling lip-sync or DubVoice on Spanish or rioplatense speech.
- HeyGen's and Kling's 2026 lip-sync APIs, parameters and pricing were not researched, due to the search budget.
- It is unknown whether lip-sync models preserve Veo's SynthID or C2PA in the output.

---

## Q4. Mixing, loudness and avoiding "AI voice" tells in UGC ads

### Takeaway
No platform (Meta, Instagram, TikTok) publishes an official loudness spec. Practitioner consensus is **-14 LUFS integrated** (range -16 to -14) with a **-1 dBTP true-peak ceiling**.

Realism comes mostly from the source:
- an expressive, clean performance;
- STS that preserves breaths and pacing;
- a voice placed in a believable room and mic.

ElevenLabs' new `audio_effects` (room reverb, distance, background bed) can do the placement on TTS. Making AI voices sound "less AI" must not mean removing disclosure labels.

### Cited Findings
**Loudness**
- "TikTok has never published an official LUFS target or documented their normalisation behaviour". — [APU Software (search summary)](https://apu.software/tiktok-instagram-reels-loudness/)
- -14 LUFS integrated with a -1 dBTP ceiling is the most cited target for TikTok and Reels. — [mixingandmastering.ai (search summary)](https://mixingandmastering.ai/blog/lufs-for-tiktok-and-reels)
- Ranges seen elsewhere:
  - -16 to -14 LUFS. — [OpusClip (search summary)](https://www.opus.pro/blog/best-loudness-normalizers)
  - -12 to -10 LUFS, a louder outlier. — [search summary](https://magicmaster.pro/blog/tiktok-mastering-loudness)
  - -14 LUFS called "Instagram's standard", a vendor claim with no Meta source. — [LoudFix (search summary)](https://www.loudfix.com/lufs-standard-instagram-2026/)
- -1 dBTP is "non-negotiable" because lossy encoding "can push peaks above 0dB and cause distortion". If normalization applies, mastering louder gains nothing. — [search summary of the above guides](https://apu.software/tiktok-instagram-reels-loudness/)

**Room and mic placement (official TTS feature)**
- ElevenLabs `audio_effects` on TTS has these fields:
  - `filter_preset_id` (e.g. `phone`, `old_radio`)
  - `distance` (0–1)
  - `environment_id` reverb (e.g. `small_room`, `hall`)
  - `send_level`
  - `background_noise_id` (e.g. `cafe`, `keyboard`)
  - `pan`
- "Effects do not change the cost". The catalog is at `GET /v1/audio-effects/catalog`. Reverb or pan forces stereo and is rejected for `pcm_*` outputs. The feature was added to the skill in the 2026-10-12 changelog update. — [elevenlabs/skills text-to-speech SKILL.md](https://github.com/elevenlabs/skills/blob/main/text-to-speech/SKILL.md)

**Performance realism**
- STS keeps "breaths, whispers, laughs". — [voice-changer SKILL.md](https://github.com/elevenlabs/skills/blob/main/voice-changer/SKILL.md)
- Eleven v4 delivery is controlled with tags (`[sighs]`, `[excited]`) plus "ellipses for pauses, capitals for emphasis". Lower stability gives more expressiveness. — [voice-settings.md](https://github.com/elevenlabs/skills/blob/main/text-to-speech/references/voice-settings.md)
- Practitioner and concept ideas:
  - Add room ambience under a clean AI voice.
  - Insert breaths before long sentences.
  - Vary the pacing.
  - EQ away "studio" depth so the voice sounds like a phone or laptop mic.
  This is a concept for a tool, not a validated method. — [machina.notion.site "The Un-AI Audio Filter" (search summary)](https://machina.notion.site/The-Un-AI-Audio-Filter-2bdc6b3f876980bf99a9ca52eb32f333)
- Recording advice: avoid one flat tone, leave 0.5–1 s pauses after big on-screen actions, and know that a quiet room beats EQ. — [Visla (search summary)](https://www.visla.us/blog/?p=5570); [Clueso (search summary)](https://www.clueso.io/cluebooks/tasteful-screen-recording--recording-voiceovers)

**Cleanup**
- Voice Isolator accepts MP4 and other containers and returns isolated speech. Use cases include "Extract dialogue from mixed tracks" and "Pre-processing for Voice Changer". — [elevenlabs/skills voice-isolator SKILL.md](https://github.com/elevenlabs/skills/blob/main/voice-isolator/SKILL.md)

### Inferences
**Mix recipe for the SOP** (practitioner consensus plus inference; validate on-device):
1. **Extract.** Pull the Veo audio and isolate the dialogue.
2. **Re-voice** (STS or TTS) at 44.1 or 48 kHz WAV/PCM, not 22 kHz MP3, so the transcode keeps headroom.
3. **Rebuild the bed.** Use Veo's ambience if it is separable, or a quiet matching room tone. A UGC phone-in-living-room look needs a short, dry room: `environment_id=small_room`, low `send_level`, `distance` about 0.1–0.2. Avoid "radio announcer" closeness.
4. **Music** under the voice, ducked about 15–20 dB below dialogue. This figure is not sourced: treat it as a starting point.
5. **Master** to about -14 LUFS integrated, -1 dBTP. Check on a phone with the screen at normal volume.
6. Keep the same room, mic character and loudness **for every clip of the same avatar**. Changing room tone between clips is heard as "a different person" even when the timbre matches.

**Script-level realism for Jarvis:**
- Short sentences.
- Voseo and Argentine fillers ("tipo", "posta", "che") used sparingly. See note 03.
- One audio tag or one ellipsis per line at most.
- No reading of numbers or URLs. Write them out the way people speak.

**Prompt Veo for a clean bed** (inference). When post is planned, ask Veo for "quiet room, no music, no background chatter". Replacing dialogue is easier when Veo's ambience is minimal.

### Gaps
- There is no official Meta, Instagram or TikTok loudness or normalization spec. All targets are practitioner consensus.
- There is no validated, measured method for making AI voices perceptually indistinguishable in UGC, and the SOP should not aim to defeat detection.
- There is no tested source on separating Veo's ambience from its dialogue, as opposed to isolating the voice only. Residual-bed extraction was not researched.

---

## Q5. Consent, legal and labeling of AI voices in ads

### Takeaway
For **fictional** avatars, the safest base is a **designed or synthetic voice** that resembles no real person, plus platform AI labels.

Use consent where a real human is involved. A guide-track actor or a cloned voice actor needs written consent and a contract that covers AI conversion. Vendors enforce this: DubVoice has a consent checkbox per clone, ElevenLabs PVC uses captcha or manual verification, and Google replication needs a consent recording.

Labeling rules now in force:
- **EU AI Act Art. 50:** from 2026-08-02, if ads reach the EU, e.g. Spain.
- **TikTok:** an AI disclosure label on realistic AI ad creative since 2026-07-21 (secondary sources).
- **Meta:** auto "AI info" labeling, with third-party AI detection since 2026-06-01 (secondary sources). Mandatory self-disclosure applies only to political and social-issue ads.

I found no Argentina-specific rule on AI voices in ads.

### Cited Findings
**Vendor consent mechanics**
- **DubVoice:** consent checkbox per cloning attempt, written permission for another person's voice, and authorization to clone public figures. — [DubVoice Terms (search summary)](https://www.dubvoice.ai/terms)
- **ElevenLabs Professional Voice Clone:** verification endpoints `voices.pvc.verification.captcha.get/verify` and `voices.pvc.verification.request(files=[verification documents])` for manual verification. — [elevenlabs-python reference.md](https://github.com/elevenlabs/elevenlabs-python/blob/main/reference.md)
- **Google Gemini 3.8 Flash TTS replication:** 10–30 s of a real adult speaker plus a consent recording. "AI-generated voices cannot be used as reference or consent audio". Output carries SynthID by default. — [sibling note 03 / GCP gemini_3_8_flash_tts](https://github.com/GoogleCloudPlatform/generative-ai/blob/main/audio/speech/getting-started/gemini_3_8_flash_tts.ipynb)

**EU AI Act Article 50**
- Obligations apply from **2 August 2026**.
- The Commission published the final, voluntary **Code of Practice on marking and labelling AI-generated content** (press release 10 June 2026). Deepfakes must be "clearly labelled". — [European Commission](https://digital-strategy.ec.europa.eu/en/news/commission-publishes-code-practice-marking-and-labelling-ai-generated-content); [Legalithm (search summary)](https://www.legalithm.com/en/blog/ai-act-transparency-obligations-article-50-deepfake-labeling)
- The Article 50 guidelines were finalised 20 July 2026. The code asks providers for "at least two machine-readable techniques", such as signed metadata plus imperceptible watermarking. C2PA is the reference for images, video and audio. — [Paul Weiss (search summary)](https://www.paulweiss.com/insights/client-memos/eu-finalises-transparency-rules-for-ai-generated-content); [Legalithm (search summary)](https://www.legalithm.com/en/blog/ai-act-transparency-obligations-article-50-deepfake-labeling)
- Art. 50(4) allows "minimal disclosure for evidently artistic, satirical or fictional works". — [aiacto.eu (search summary)](https://www.aiacto.eu/en/blog/article-50-ai-act-transparence-deepfakes-contenu-ia)
- **Single-source and unverified:** providers already on the market before 2 Aug 2026 may have until 2 Dec 2026 for marking. — [search summary, voice-cloning law trackers](https://www.spirelight.ai/guides/voice-cloning-laws)

**Meta**
- Mandatory AI disclosure applies to political and social-issue ads (since Jan 2024).
- Other ads get an automatic "AI info" label, e.g. when they show an AI-generated photorealistic human.
- Since **June 1, 2026** Meta reportedly detects third-party AI via industry-standard signals, shown under "About this ad". This is from secondary blogs. One says to confirm with Meta's Business Help Center. — [digitalapplied (search summary)](https://www.digitalapplied.com/blog/ai-content-labeling-rules-advertisers-2026-reference); [Mockingbird (search summary)](https://www.mockingbirdhouse.com/learning/ai-ad-creative/does-meta-allow-ai-generated-ads); [CineRads (search summary)](https://www.cinerads.com/blog/ai-ugc-facebook-ad-policy)

**TikTok**
- Since **July 21, 2026**, ads with realistic AI-generated content reportedly need an AI disclosure label before they can run. Organic AIGC labeling has been required since 2023.
- A March 2026 report found enforcement lagging.
- One guide claims synthetic media of real private individuals is banned even with a label. This is unconfirmed. — [Common Thread Co (search summary)](https://commonthreadco.com/blogs/coachs-corner/tiktok-ai-ad-disclosure-rules-ecommerce-2026); [Stellar Search (search summary)](https://www.stellarsearch.co.uk/insight/tiktoks-ai-ad-disclosure-rules-are-live-what-brands-running-ai-creative-need-to-do-now); [CineRads TikTok (search summary)](https://www.cinerads.com/blog/tiktok-ai-content-policy); [ainauten (search summary)](https://news.ainauten.com/markdown/tiktoks-policy-for-ai-ads-isnt-working)
- Platforms reportedly auto-detect C2PA Content Credentials. — [Common Thread Co (search summary)](https://commonthreadco.com/blogs/coachs-corner/tiktok-ai-ad-disclosure-rules-ecommerce-2026)

**US (relevant if any ads reach the US)**
- The **NO FAKES Act** of 2026 (S. 4591 / H.R. 8915) was introduced 2026-05-20. The Senate Judiciary Committee advanced it on 2026-06-18. It is **not law** as of mid-Oct 2026. — [GovTrack](https://www.govtrack.us/congress/bills/119/s4591); [Manatt](https://www.manatt.com/insights/newsletters/client-alert/congress-reintroduces-the-no-fakes-act-what-s-new-in-the-2026-bill); [Holland & Knight](https://www.hklaw.com/en/insights/publications/2026/06/senate-judiciary-committee-advances-legislation-to-protect-name)
- **State laws:**
  - Tennessee's ELVIS Act (since 2024-07-01) covers voice simulations.
  - California Civ. Code §3344 and New York Civil Rights Law §50 cover written consent for a living person's voice in advertising.
  - A NY law requiring disclosure of AI "synthetic performers" in ads reportedly took effect 2026-06-09. This is single-source. — [search summary, voice-cloning law trackers](https://www.spirelight.ai/guides/voice-cloning-laws); [anyvoice tracker (search summary)](https://anyvoice.io/blog/ai-voice-cloning-regulation-news)

### Inferences
**SOP compliance rules:**
1. Avatars use **designed or synthetic voices only**. Never "sound-alike" a celebrity or real creator. The Dove Cameron voice-model results show this temptation exists.
2. Any human guide-track or cloned voice actor signs written consent covering AI cloning, STS conversion, territories and term. Keep a copy linked to the `voice_id`.
3. Keep SynthID and C2PA metadata intact through post, and switch on the platform AI-disclosure toggle. On TikTok it is effectively required for realistic AI people.
4. For EU or Spain campaigns, add a visible AI notice.

**Testimonials (inference).** Synthetic "customers" giving testimonials raise a separate consumer-protection issue beyond voice labeling. A fictional person presenting results as their own real experience can be deceptive. Have legal review this, per market, before scaling low-ticket info-product ads.

### Gaps
- I found no Argentine law, regulation or ad-industry rule on AI voices or synthetic presenters in ads. Not covered: Argentina's consumer-protection law (Ley 24.240), any AI bills, and whether CONARP or a self-regulation code mentions AI.
- I did not verify the FTC's fake-reviews/testimonials rule and its application to AI-generated testimonials in this session.
- Meta's and TikTok's official policy pages could not be read. All 2026 specifics are from secondary agency blogs.
- The EU "until 2 Dec 2026" grace period is single-source and needs checking against the Official Journal or Digital Omnibus outcome.
