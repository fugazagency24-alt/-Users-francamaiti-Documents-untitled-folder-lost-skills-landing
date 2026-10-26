# Voice consistency and Argentine (rioplatense) accent in Veo: research notes (as of 2026-10-26)

> **Method and reliability.** Primary sources read in full were Google-authored GitHub material:
> - `GoogleCloudPlatform/generative-ai` at HEAD `3567247`, 2026-10-26. This includes the new `audio/speech/getting-started/gemini_3_8_flash_tts.ipynb`, first committed **2026-10-01**.
> - `google-gemini/cookbook` at HEAD `5506746`, 2026-10-19: `Get_Started_Voices`, `Get_started_TTS`, `Get_started_Omni`, `Get_started_Veo`, `Autonomous_video_production_with_omni_and_agents`.
> - `GoogleCloudPlatform/vertex-ai-creative-studio` at HEAD `214d4ac`, 2026-10-24.
> - The `googleapis/python-genai` SDK `types.py`.
> - The Google Cloud blog prompting guide.
>
> The proxy blocks page fetches to docs.cloud.google.com, ai.google.dev, blog.google, elevenlabs.io, dubvoice.ai, beehiiv, TikTok/X and most creator blogs. Claims from those sites are marked **(search summary)** and are weaker evidence. Items older than about 6 months (before roughly late April 2026) are flagged **[>6 mo]**. The model under discussion is **Veo 3.1 Lite (`veo-3.1-lite-generate-001`, Preview since 2026-04-02)**. See sibling notes `01_veo_vertex_specs.md`. No source I found tests accents on Lite specifically. Most practitioner evidence is from Veo 3 / 3.1 in 2025.

---

## Q1. Does Veo follow accent instructions? Which phrasing gets a real Argentine (rioplatense) accent instead of neutral Spanish?

### Takeaway
Veo has **no voice, language or accent parameter**. Accent is controlled only by the prompt text, and Google publishes **no accent guidance and no list of supported speech languages** for Veo. Creators report that Veo can produce an Argentine accent when asked explicitly, but nobody has published a controlled test, and some report garbled or "strange" accents in Spanish.

The best-supported recipe has three parts:
- An explicit, very specific accent clause, at city level, per Google's own TTS accent advice.
- Dialogue **written in rioplatense**: voseo plus lexical markers plus words that force sheísmo.
- The same voice block repeated verbatim in every clip.

On top of that, run QA, sample 2–4 takes, and re-voice in post (Q3/Q4) as the guaranteed fallback.

### Cited Findings
**Official / primary (Google)**
- The Veo request config (`GenerateVideosConfig`) has exactly these fields: `number_of_videos, output_gcs_uri, fps, duration_seconds, seed, aspect_ratio, resolution, person_generation, pubsub_topic, negative_prompt, enhance_prompt, generate_audio, last_frame, reference_images, mask, compression_quality, labels, webhook_config, resize_mode`. **None selects a voice, speaker, language or accent.** — [python-genai types.py](https://github.com/googleapis/python-genai/blob/main/google/genai/types.py)
- Google's Veo 3.1 prompting guide (Oct 16, 2025) **[>6 mo]** gives this audio syntax:
  - "Dialogue: Use quotation marks for specific speech (e.g., A woman says, "We have to leave now.")."
  - "SFX: …"
  - "Ambient noise: …"

  Its only voice descriptor is inline: "He looks up at the woman and says in a weary voice, "…"". It calls the audio features "experimental and actively improving". The page gives **no guidance on voice, accent, or voice selection**. — [Google Cloud Blog: Ultimate prompting guide for Veo 3.1](https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-veo-3-1)
- Google's Veo cookbook dialogue example uses plain attribution: "The first character start saying "oh my god, it is really hot in here!" - then the second answers "right? I'm melting down!"", with `negative_prompt = "texts, captions, subtitles"`. — [cookbook Get_started_Veo](https://github.com/google-gemini/cookbook/blob/main/quickstarts/Get_started_Veo.ipynb)
- Google's sample app marks all three Veo 3.1 models, Lite included, `requires_prompt_enhancement=True`. In that app the prompt rewriter is always on for these models. — [vertex-ai-creative-studio config/veo_models.py](https://github.com/GoogleCloudPlatform/vertex-ai-creative-studio/blob/main/config/veo_models.py)
- Google's TTS team's accent advice, written for Gemini TTS rather than Veo: "**Accent** — Be specific when requesting an accent, e.g. *"British English accent as heard in Brixton, London"*." Its director's-notes template is `AUDIO PROFILE: … / THE SCENE: … / DIRECTOR'S NOTES: - Style: … - Pace: … - Accent: Brixton, London Estuary accent.` — [cookbook Get_started_TTS](https://github.com/google-gemini/cookbook/blob/main/quickstarts/Get_started_TTS.ipynb)

**Practitioner reports (anecdotal, mostly 2025, Veo 3 / 3.1, not Lite)**
- A TikTok street-interview clip has a protester speaking Spanish with an Argentine accent. The creator's prompt said "todos los personajes hablan en español con acento argentino". Date unknown. — [TikTok discover "Google Veo 3 como usar en español" (search summary)](https://www.tiktok.com/discover/google-veo-3-como-usar-en-espa%C3%B1ol)
- An X post from 2025-05-27 **[>6 mo]** says Veo 3 "es capaz de crear con acentos, chistes … y hasta trabalenguas" in Spanish. — [Ruben Villegas on X (search summary)](https://x.com/RubenEVillegas/status/1927207500513689835)
- Alan Daitch, an Argentine creator, publishes a Veo 3 prompt asking the artist to "speak Spanish with Rioplatense accent". He also has prompts that ask for "español latino neutro" or a Mexican accent. — [alandaitch.com/prompts (search summary)](https://www.alandaitch.com/prompts)
- Juan Merodio recommends a reusable "ADN de voz" block (timbre, acento, ritmo) pasted into the base prompt. His example uses "acento neutro español", which you would swap for rioplatense. — [juanmerodio.com/google-veo3 (search summary)](https://www.juanmerodio.com/google-veo3/)
- Noviai says Veo 3 has no predefined voice categories. To get Spanish you "write the exact Spanish words … directly in your prompt" and can add "español argentino". — [noviai.ai (search summary)](https://www.noviai.ai/models-prompts/how-to-prompt-for-speaking-in-veo-3/)
- Arsturn says to state that the dialogue is in Spanish and to name the accent. It warns the dialogue "could come out garbled, in English, or with a strange accent". — [arsturn.com (search summary)](https://www.arsturn.com/blog/your-ultimate-guide-to-using-veo-3-for-spanish-language-video-content)
- Prompt-architects (single source, unverified) says the documented Veo 3.1 interface has no voice-selection parameter and recommends stating the accent in the attribution clause ("says in a … accent"). It also claims that "Google's own wording lists the languages it evaluated, and Spanish isn't among them". I could not confirm that against a Google model card. — [prompt-architects.com (search summary)](https://prompt-architects.com/blog/101-veo-dialogue-prompts)
- A vendor comparison calls Veo 3.1's speech "English-centric". This is promotional and lists no tested languages. — [Atlas Cloud (search summary)](https://www.atlascloud.ai/blog/guides/ai-video-models-native-audio-compared)
- **Conflict on dialogue formatting:**
  - Replicate suggests putting speech "after a colon" instead of in quotes, plus "(no subtitles)", to avoid burned-in captions. — [Replicate blog (search summary)](https://replicate.com/blog/using-and-prompting-veo-3)
  - Google's guide uses quotation marks. — [Google Cloud Blog](https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-veo-3-1)

**Rioplatense markers (for writing the script)**
- For a porteño sound, write in voseo ("vos tenés", "mirá", "vení") and avoid "tú". This advice comes from a TTS guide. — [Socialecho "Voz argentina" (search summary)](https://www.socialecho.net/es/free-tools/voz-argentina/)
- Voseo, using *vos* instead of *tú*, is standard across Argentina and Uruguay. — [Wikipedia: Voseo](https://en.wikipedia.org/wiki/Voseo); [Wikipedia: Rioplatense Spanish](https://en.wikipedia.org/wiki/Rioplatense_Spanish)
- Sheísmo ("ll/y" pronounced "sh") is cited as the defining feature on es-AR TTS vendor pages. — [speechgen es-AR (search summary)](https://speechgen.io/en/tts-spanish-argentina/)

**Evidence that accent prompts are fragile in Google's audio models (adjacent: TTS)**
- A Google AI forum user got a Castilian accent from Gemini 2.5 Pro TTS one day and lost it on later days with the same style instructions ("seems broken"). Adding **phonetic spellings to the text** worked more consistently. Date unknown, likely 2025 **[>6 mo?]**. — [discuss.ai.google.dev thread (search summary)](https://discuss.ai.google.dev/t/gemini-2-5-pro-tts-language-codes/108683)
- On OpenAI TTS, Spanish defaults to Latin American accents, and a Spain-accent instruction did not fully fix it. This shows the "defaults to neutral" problem across vendors. — [OpenAI community (search summary)](https://community.openai.com/t/spanish-spain-openai-tts-models/1355551)

### Inferences
- **Why the client gets neutral Spanish.** Inferred from the findings above:
  - "Spanish" or "Latin American Spanish" with neutral *tú/usted* lines lets the model fall back to a pan-Latin default.
  - A prompt rewriter that is always on may paraphrase or drop a short accent tag. This is a risk, not proven.

  The fix is to make the accent **redundant**: name it, describe it acoustically, and embed it in the words themselves.
- **Recommended accent clause.** Keep the scaffolding in English to match Google's own guides, which are English-only. Write the dialogue in rioplatense. Paste this block verbatim in every clip:
  `Voice & accent: native Argentine speaker from Buenos Aires; speaks Rioplatense Spanish (español rioplatense, acento porteño), NOT neutral Latin American Spanish. Clear sheísmo ("yo" sounds like "sho", "calle" like "cashe", "lluvia" like "shuvia"), voseo, and the melodic, Italian-like porteño intonation with long stressed vowels. Casual, conversational delivery.`
- **Write lines that force the accent.** Use stressed-final voseo verbs (tenés, sabés, mirá, probá, querés, dale) and words with *ll/y* (yo, ya, llegó, calle, posta). Add markers like "che", "re" (as in "re bueno") and "¿viste?". Avoid *tú, usted, vosotros* and Mexican or Spain lexicon. Example UGC line: *"Che, mirá, yo ya lo probé y posta que me re sirvió. ¿Vos lo conocías?"*
- **Do not** put phonetic respellings such as "sho" inside the quoted dialogue on Veo without an A/B test. It may help, as it did for Gemini TTS, but it may also produce misspelled burned-in subtitles. Keep phonetic hints in the description only. Treat this as a test hypothesis.
- **Getting it right first time.** Generate `sampleCount` 2–4 per shot. Per sibling notes, 4 Lite 1080p 8 s samples cost about $2.56. Then auto-screen accent fidelity with a Gemini model, using Google's TTS QA rubric idea (see Q3 findings), before a human picks one.

### Gaps
- I found no controlled test of accent fidelity on **Veo 3.1 Lite** in any Spanish variety.
- I found no Google statement of supported or evaluated speech languages for Veo 3.1. The claim that Spanish is not evaluated is single-source and unverified.
- I found no evidence on whether an English or Spanish prompt scaffold gives better rioplatense output.
- It is undocumented whether `enhancePrompt` can be turned off on Lite. The sample app says it is required. It is also unknown whether the rewriter translates or paraphrases Spanish dialogue or accent tags.

---

## Q2. Which voice-description vocabulary stabilizes a voice? How do you keep each character's voice in multi-character formats (interview, podcast, storytelling)?

### Takeaway
Veo has no voice ID, so the only in-model lever is a **fixed "voice DNA" block tied to a fixed character description**, repeated word for word in every clip. Google's TTS team has the best-sourced vocabulary: age and gender, accent and origin, timbre, pacing, and archetype.

For multi-character scenes, sources agree on three things:
- Make characters **clearly different in look and voice**.
- **Attribute every line explicitly**, by visual description plus a verb like "says" or "replies".
- **Prefer one speaking character per shot**. Google's own two-character example does this.

### Cited Findings
- Google's voice-design best-practice dimensions (Gemini 3.8 TTS): **Age & Gender** ("woman in her 60s"), **Accent & Origin** ("warm Scottish Highlands accent"), **Vocal Quality & Timbre** ("deep and gravelly", "velvety contralto"), **Pacing & Cadence** ("brisk and articulate"), **Character Archetype**. The guide adds: "Use CreateVoice … to define **who the speaker is** (their permanent vocal identity), and use `speech_metadata` … to control **how they deliver a specific line**." — [cookbook Get_Started_Voices](https://github.com/google-gemini/cookbook/blob/main/quickstarts/Get_Started_Voices.ipynb)
- Google's guidance for Gemini 3.8 TTS is to set permanent traits like regional accent in the voice description, not in the per-line style prompt. — [blog.google Gemini 3.8 TTS (search summary)](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-8-text-to-speech/); [Agent Platform TTS docs (search summary)](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/text-to-speech/overview)
- Practitioners on keeping the same voice:
  - "Use the same character description every time… this description must be identical in every prompt, or the AI will generate different characters with different voices." — [veo3ai.io two-character dialogue guide 2026 (search summary)](https://www.veo3ai.io/blog/veo-3-two-character-dialogue-guide-2026)
  - If two characters "look or sound similar, Veo 3 smears the dialogue across both mouths or puts the wrong voice on the wrong person". A plain "Man: / Woman:" script gave cases where "only one person had sound". — [veo3ai.io (search summary)](https://www.veo3ai.io/blog/veo-3-two-character-dialogue-guide-2026)
  - "Fix #3: Voices don't match the character (describe voice traits + consistency anchors)" and "Fix #2: Lip-sync feels off (shorter lines, beats, and on-screen actions)". — [Veo3Gen blog (search summary)](https://www.veo3gen.app/blog/veo3gen-audio-keeps-going-wrong-9-fixes-for-dialogue-sfx-timing-and-music-mix-as)
- A TikTok creator (2025-08-11) **[>6 mo]** says to "Always include a short voice and accent description in your prompt… [the voice may] change slightly … but not the accent." — [TikTok @ai.for.real.life (search summary)](https://www.tiktok.com/@ai.for.real.life/video/7537477893442538766)
- Google's multi-shot conversation workflow puts one character per shot. Shot 1: "…create a medium shot of the detective… He looks up at the woman and says in a weary voice, "…"". Shot 2: "…a shot focusing on the woman… she replies, "…"". This uses "Ingredients" (reference images). — [Google Cloud Blog prompting guide](https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-veo-3-1)
- **Veo 3.1 Lite does not support reference images (no "r2v" mode)**. Lite therefore lacks the Ingredients identity anchor that Google's multi-character workflow relies on. — [vertex-ai-creative-studio config/veo_models.py](https://github.com/GoogleCloudPlatform/vertex-ai-creative-studio/blob/main/config/veo_models.py)
- Google's Omni agent example times speech explicitly: "At 4 seconds, the robot stops… and speaks aloud in a friendly synthetic voice: "…" The robot concludes speaking at 8.2 seconds". Dialogue is ended "to preserve acoustic cleanliness before the 10s boundary". — [cookbook Autonomous_video_production_with_omni_and_agents](https://github.com/google-gemini/cookbook/blob/main/examples/Autonomous_video_production_with_omni_and_agents.ipynb)
- Google's timestamp syntax `[00:00-00:02] …` directs multi-beat shots inside one generation. — [Google Cloud Blog prompting guide](https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-veo-3-1)

### Inferences
- **Character sheet for Jarvis.** Store this per character and inject it verbatim into every prompt:
  `CHARACTER A = "Lucía, 28-year-old Argentine woman, shoulder-length wavy chestnut hair, light freckles, white oversized tee" + VOICE A = "warm mid-pitched female voice, slightly husky, fast-but-clear porteño cadence, upbeat; Rioplatense Spanish, Buenos Aires accent with sheísmo; close-mic'd phone audio in a small quiet room"`.

  Add mic and room descriptors so tone stays constant between clips ("close-mic'd smartphone", "small untreated bedroom"). No source tests mic proximity, so treat this as a hypothesis.
- **Maximise contrast between characters.** Use different gender, age bracket, pitch and energy (for example, "gravelly baritone man in his 50s, slow" vs "bright young woman, fast"). Different accents within Argentina, such as porteño vs cordobés, are risky. Keep everyone porteño unless the script needs otherwise.
- **Attribution pattern per line.** Write `[visual identifier] + speech verb + (voice tag) + quoted line`. For example: `The woman with chestnut hair (VOICE A) turns to the man and says: "…". The bearded man in the grey hoodie (VOICE B) replies: "…"`. Keep it to 1–2 short lines per 8 s clip.
- **Interview and podcast formats.** Shoot shot / reverse-shot so that **only one face is speaking per clip** and the listener is silent ("listens silently, nodding, mouth closed"). This also makes per-character re-voicing and single-face lip-sync possible (Q4/Q5).
- **Storytelling with narration.** Treat the narrator as an off-screen voice-over generated by TTS with a fixed voice ID, not by Veo. Use Veo only for on-camera lines.

### Gaps
- No published study measures which descriptors make Veo voices more stable.
- No data shows whether "voice tags" like "(VOICE A)" help or get spoken aloud. Test this.
- I found no Google guidance specific to multi-speaker dialogue on Veo 3.1 Lite.

---

## Q3. Why do voices change between generations and extensions, and what actually keeps them stable (seed, extend, first/last frame, post-production replacement)?

### Takeaway
Each Veo call samples a fresh voice. There is no voice conditioning input: no voice ID and no audio reference.
- `seed` only reproduces **identical** requests, so it cannot lock a voice across different lines.
- First/last-frame and the start image lock **visuals, not voice**.
- **Extension** continues from the tail of the previous clip. It is the best in-model continuity option but not a guarantee.

The only deterministic lock is **post-production**: convert the dialogue track to one fixed voice per character with speech-to-speech, which keeps timing so lips stay in sync, or use TTS plus lip-sync.

### Cited Findings
- `seed`: "If RNG seed is exactly same for each request with unchanged inputs, the prediction results will be consistent. Otherwise, a random RNG seed will be used." Google's MCP server calls it "best-effort reproducible". — [python-genai types.py](https://github.com/googleapis/python-genai/blob/main/google/genai/types.py); [mcp-veo-go README](https://github.com/GoogleCloudPlatform/vertex-ai-creative-studio/blob/main/experiments/mcp-genmedia/mcp-genmedia-go/mcp-veo-go/README.md)
- The Veo config has no audio or voice reference input (field list in Q1). — [python-genai types.py](https://github.com/googleapis/python-genai/blob/main/google/genai/types.py)
- **Omni audio references conflict:**
  - The Gemini API cookbook comparison table says Gemini Omni Flash supports "Up to 5 reference images & 5 audio tracks". — [cookbook Get_started_Omni](https://github.com/google-gemini/cookbook/blob/main/quickstarts/Get_started_Omni.ipynb)
  - The Agent Platform (Vertex) Omni 1.1 notebook says "**Audio reference inputs are not currently supported.**" — [GCP gemini_omni_1_1_flash_video_gen](https://github.com/GoogleCloudPlatform/generative-ai/blob/main/vision/getting-started/gemini_omni_1_1_flash_video_gen.ipynb)
- Veo extension adds 7 s. The official notebook extends with `veo-3.1-generate-preview`, which is not Lite. — [GCP veo3_advanced_controls](https://github.com/GoogleCloudPlatform/generative-ai/blob/main/vision/getting-started/veo3_advanced_controls.ipynb)
- Third-party claims, not confirmed by Google:
  - Veo 3.1 extend "samples the last 1 second of your input".
  - It "carries over native audio continuation" and generates "dialogue without abrupt changes".
  - The sources conflict on whether the addition is 7 s or 8 s. — [eachlabs Veo 3.1 Extend (search summary)](https://www.eachlabs.ai/google/veo3-1/veo3-1-extend-video); [DataCamp Veo 3.1 guide (search summary)](https://www.datacamp.com/tutorial/veo-3-1-complete-guide-with-examples)
- Omni extension "maintain[s] temporal continuity, character identity". "Generating spoken dialogue or speech is fully supported when extending previously generated videos via multi-turn (`previous_interaction_id`)", but "you cannot extend an uploaded video where someone is talking to add additional dialogue". — [cookbook Get_started_Omni](https://github.com/google-gemini/cookbook/blob/main/quickstarts/Get_started_Omni.ipynb)
- Google's guide says first-and-last-frame generates a transition "complete with audio". Nothing there claims voice continuity. — [Google Cloud Blog prompting guide](https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-veo-3-1)
- Generative voices are random by design. In Google's own TTS, "each call to `client.voices.create` produces a unique voice variation matching your prompt", even with an identical description. — [cookbook Get_Started_Voices](https://github.com/google-gemini/cookbook/blob/main/quickstarts/Get_Started_Voices.ipynb)
- The practitioner fix that comes up most is to arrange all clips, export the vocals or the whole video, run **everything at once** through ElevenLabs Voice Changer with one chosen voice, then replace the original audio. "This ensures every clip has the exact same voice." — [TikTok @ai.for.real.life, 2025-08-11 (search summary)](https://www.tiktok.com/@ai.for.real.life/video/7537477893442538766); [ai-for-real-life newsletter (search result title)](https://ai-for-real-life.beehiiv.com/p/the-secret-to-consistent-characters-in-veo-3-and-how-to-fix-the-voices-too)
- "A consistent face does not prove a consistent voice". If re-voicing changes pauses or word timing, the mouths stop matching. — [GlobalGPT (search summary)](https://www.glbgpt.com/hub/how-to-make-characters-speak-in-veo-3-1-the-ultimate-guide-to-dialogue-audio-lip-sync/)
- Google's sample app ships an LLM audio-QA rubric. It includes "**B. Prompt Fidelity (Style/Tone/Accent)**" and "**E. Speaker Consistency (If Multi-Speaker)**", scored 1–100 in JSON. — [vertex-ai-creative-studio config/evaluators.py](https://github.com/GoogleCloudPlatform/vertex-ai-creative-studio/blob/main/config/evaluators.py)
- Google's Omni agent notebook uses a Gemini Pro reviewer to auto-reject clips before extending: "Always review every generated clip before extending. Never accept uninspected footage." — [cookbook Autonomous_video_production_with_omni_and_agents](https://github.com/google-gemini/cookbook/blob/main/examples/Autonomous_video_production_with_omni_and_agents.ipynb)

### Inferences
- **Root cause of pain point (1).** Every new Veo call, new seed or new text re-samples timbre, and a mandatory prompt rewriter adds further variation. Expect drift by default. Seed is useful only for re-rendering the *same* shot with tiny changes, and even then it is best-effort.
- **In-model best practice:**
  1. Keep each character's voice block identical.
  2. Prefer one continuous clip per speaker turn.
  3. To lengthen a talking take, use **extension on the same model ID** rather than a fresh generation. Mixing Lite base clips with a non-Lite extension model may change voice or look.
  4. End each segment on a complete sentence.
- **Open conflict.** The "last 1 second" claim suggests voice should still be present at the tail for continuity. Google's Omni example ends speech about 1.8 s before the boundary for clean audio. Test both on Lite.
- **Production rule for multi-clip ads.** Treat Veo's voice as a **guide track**. Lock the final voice in post with one fixed target voice per character (Q4). This is the only way to *guarantee* the same voice across clips and extensions.
- Automate a QA step in Jarvis's pipeline. Send each candidate clip to Gemini with the Google rubric, extended with:
  - "Is the accent Rioplatense (sheísmo, voseo, porteño intonation) rather than neutral or Mexican/Spain?"
  - "Is this the same voice as reference clip X?"

  Reroll failures before human review.

### Gaps
- There is no official Google statement on how Veo 3.1 extension handles audio and voice. The "last 1 second" claim is third-party only.
- No test shows whether the same seed plus an identical voice block keeps a voice when only the dialogue changes.
- Extension support on Lite is contested (see `01_veo_vertex_specs.md`).

---

## Q4. What is the post-production route (re-voice with a fixed voice plus lip-sync)? Which Argentine voices exist in major TTS catalogs? What is "Dub Voice"?

### Takeaway
**Most reliable path:** generate in Veo **with audio on**, so lip motion follows Spanish speech rhythm. Then convert each character's whole dialogue track to **one fixed voice** with **speech-to-speech** (ElevenLabs Voice Changer, or DubVoice if it offers STS). Timing is preserved, so no re-lip-sync is needed. Choose an Argentine target voice to reinforce the accent.

**Google's stack** has no Argentine locale:
- Chirp 3 HD has es-ES and es-US.
- Gemini-TTS has es-ES, es-419, es-MX and es-US.
- I found no Google speech-to-speech voice changer.
- The new **Gemini 3.8 Flash TTS** (Preview, late Sept 2026) adds prompt-designed voices, a 2,000+ voice library with accent metadata, and consented voice replication. Use it for **TTS replacement plus lip-sync**, or for off-screen narration.

**"Dub Voice"** is most likely **DubVoice.ai**. It is a credit-based aggregator for TTS, cloning, dubbing and video, including Veo 3.1. Its exact features are unverified.

### Cited Findings
**Google voices and Spanish locales**
- Locale lists in Google's sample app:
  - Chirp 3 HD Spanish locales are only "Spanish (Spain)": es-ES and "Spanish (United States)": es-US.
  - Gemini-TTS Spanish locales are es-ES, es-419 ("Spanish (Latin America)") and es-MX.
  - There is **no es-AR**. — [vertex-ai-creative-studio config/gemini_tts.py](https://github.com/GoogleCloudPlatform/vertex-ai-creative-studio/blob/main/config/gemini_tts.py)
- Google's Gemini-TTS notebook lists "es-es", "es-419", "es-mx", "es-us" among 80+ locales, with no es-ar. It says Gemini-TTS lets you dictate "style, accent, pace, tone, and even emotional expression, all steerable through natural-language prompts". — [GCP get_started_with_gemini_tts_voices](https://github.com/GoogleCloudPlatform/generative-ai/blob/main/audio/speech/getting-started/get_started_with_gemini_tts_voices.ipynb)
- The Chirp 3 HD docs list es-ES and es-US only, not es-AR. — [Chirp 3 HD docs (search summary)](https://docs.cloud.google.com/text-to-speech/docs/chirp3-hd)

**Gemini 3.8 Flash TTS (new)**
- Model IDs are `gemini-3.8-flash-tts` and `gemini-3.8-flash-lite-tts` on Agent Platform. Google says Flash suits "complex multi-speaker dialogue… **regional or minority dialects**, and long-form narration that needs a stable voice". "For regional or minority dialects, use Gemini 3.8 Flash TTS." Google's notebook was first committed 2026-10-01. — [GCP gemini_3_8_flash_tts](https://github.com/GoogleCloudPlatform/generative-ai/blob/main/audio/speech/getting-started/gemini_3_8_flash_tts.ipynb)
- There are four voice types: 30 prebuilt; **Extended Voice Library** of "more than 2,000 curated preset voices across languages, regional accents, character personas"; **prompted (designed) voices** "stored in your project"; and **replicated voices**. Library voices can be searched with `client.voices.list(type_=["prebuilt"], search="…")` and carry `language_code, accent, gender, pitch, persona, description`. — [GCP gemini_3_8_flash_tts](https://github.com/GoogleCloudPlatform/generative-ai/blob/main/audio/speech/getting-started/gemini_3_8_flash_tts.ipynb)
- **Library-size conflict:** the Gemini API docs reportedly say "hundreds" of library voices. — [Gemini API docs (search summary)](https://ai.google.dev/gemini-api/docs/models/gemini-3.8-flash-tts)
- Docs list Preview with release date **2026-09-28** and "regional accents and minority dialects in 130 languages" (Flash-Lite: 101). MarkTechPost dated the release **2026-09-23**, so the launch date is uncertain. Google reports an accent-modeling score of 60.8 on Hume AI's Voice Design Benchmark (Google-reported). The model is available via the Gemini Enterprise (Agent Platform) API, not the Cloud TTS API. Intro price is $0.50 per 1M text input tokens through 2026-12-31. — [Agent Platform 3.8 Flash TTS page (search summary)](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/3-8-flash-tts); [MarkTechPost (search summary)](https://www.marktechpost.com/2026/09/23/google-releases-gemini-3-8-flash-tts-and-flash-lite-tts-with-prompt-based-voice-design/); [blog.google (search summary)](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-8-text-to-speech/)
- "Voice remixing", meaning picking a library voice and adjusting its accent with prompts, is described as **coming soon**. — [blog.google (search summary)](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-8-text-to-speech/)
- Designed-voice persistence on the Gemini API: the returned Voice ID is "stored for **7 days** (`expire_time`)". — [cookbook Get_Started_Voices](https://github.com/google-gemini/cookbook/blob/main/quickstarts/Get_Started_Voices.ipynb)
- On Agent Platform, stored replicated voices "expire 1 year after last use", and replication keys expire 7 days after creation. — [GCP gemini_3_8_flash_tts](https://github.com/GoogleCloudPlatform/generative-ai/blob/main/audio/speech/getting-started/gemini_3_8_flash_tts.ipynb)
- Replication requirements:
  - It needs 10–30 s reference audio of a real adult speaker plus a consent recording of the exact consent statement. — [GCP gemini_3_8_flash_tts](https://github.com/GoogleCloudPlatform/generative-ai/blob/main/audio/speech/getting-started/gemini_3_8_flash_tts.ipynb)
  - "**AI-generated voices cannot be used as reference or consent audio**" (anti-spoofing, SynthID/C2PA checks). — [cookbook Get_Started_Voices](https://github.com/google-gemini/cookbook/blob/main/quickstarts/Get_Started_Voices.ipynb)
- Multi-speaker TTS: "You can include up to **2** different speakers" per request. — [GCP gemini_3_8_flash_tts](https://github.com/GoogleCloudPlatform/generative-ai/blob/main/audio/speech/getting-started/gemini_3_8_flash_tts.ipynb)
- In Gemini 3.8 TTS "`text` is synthesized **verbatim**". Put accent and style in `speech_metadata.style`, not in the text. — [cookbook Get_started_TTS](https://github.com/google-gemini/cookbook/blob/main/quickstarts/Get_started_TTS.ipynb)
- "By default, all audio generated with Gemini 3.8 Flash TTS utilizes SynthID." — [GCP gemini_3_8_flash_tts](https://github.com/GoogleCloudPlatform/generative-ai/blob/main/audio/speech/getting-started/gemini_3_8_flash_tts.ipynb)

**ElevenLabs**
- "The accent used when generating audio comes from the voice that you use". A voice not trained on the target language "might retain its native accent, or drift between different accents". Pick "a voice that has been trained on audio in the language you're generating, with your preferred accent". — [ElevenLabs help center: language and accent (search summary)](https://elevenlabs.io/docs/help-center/product/core-capabilities/text-to-speech/how-do-i-select-the-language-and-accent.md); [ElevenLabs: why does my voice change accent (search result)](https://elevenlabs.io/docs/help-center/troubleshooting/why-does-my-voice-change-accent-or-language/llms.txt)
- ElevenLabs markets Argentine-accent voices. — [elevenlabs.io/languages/argentine-accent (search summary)](https://elevenlabs.io/languages/argentine-accent)
- Third-party catalogs list ElevenLabs Argentine voices such as Valeria ("young, cheerful Argentine female… Rioplatense (Buenos Aires) accent"), Agustín, Malena and Javier. Another catalog lists six Argentine-tagged voices (Adrian, Agus, Agustina…). These reseller counts may not match ElevenLabs' own library. — [Famulor (search summary)](https://www.famulor.io/voices/elevenlabs/languages/es/accents/argentine); [json2video (search summary)](https://json2video.com/ai-voices/languages/spanish/argentina/)

**Other es-AR options**
- Speechgen offers native es-AR neural speakers "Abegail" and "Tomas". — [speechgen (search summary)](https://speechgen.io/en/tts-spanish-argentina/)
- Gradium creates a rioplatense voice from a text description. — [gradium.ai (search summary)](https://gradium.ai/voices/accents/rioplatense-spanish)
- An open XTTS-v2 fine-tune for Argentine Spanish exists on Hugging Face. — [surus-ai/XTTS-v2-argentinian-spanish (search summary)](https://huggingface.co/surus-ai/XTTS-v2-argentinian-spanish)

**"Dub Voice" identification**
- DubVoice.ai describes itself as "an all-in-one AI content creation platform". It bundles text-to-speech (17,800+ voices), voice cloning, AI video ("Veo 3.1, Grok and more"), image models, music, speech-to-text, "voice tools" and translation. It is credit-based from $4.99 with no subscription.
- A July 2026 vendor post says the library grew "from 10,500 to 17,800+ voices across six providers" and added UGC/YouTube video features.
- Dubbing is "50+ languages" on one page and "36+" on another (conflict). The site claims dubbing "matches lip-sync quality of human dubs at ~10% of the cost", which is unverified.
- No independent 2026 roundup (Smartcat, ToolRadar, ai-dubbing.app) includes it. — [dubvoice.ai (search summary)](https://www.dubvoice.ai/); [DubVoice "What's New 2026" (search summary)](https://www.dubvoice.ai/blog/whats-new-2026-new-voice-providers-video-models-youtube-ugc); [DubVoice AI dubbing guide (search summary)](https://www.dubvoice.ai/blog/ai-voice-dubbing-guide)
- Similar names that are different products: "Dubbing AI", a real-time voice-changer app with conflicting voice counts and flagged reviews, and "Dubverse". — [dubbingai.io (search summary)](https://dubbingai.io/articles/en/use-case/spanish-portuguese-voice-changer-accent-translation); [FutureTools Dubbing AI (search summary)](https://www.futuretools.io/tools/dubbing-ai)

**Cost note**
- Veo 3.1 Lite video-only SKUs are about 40% cheaper than with-audio ($0.05 vs $0.08 per second at 1080p). — [Agent Platform pricing, read in full in sibling notes 01](https://cloud.google.com/gemini-enterprise-agent-platform/generative-ai/pricing)

### Inferences
- **Decision tree for the SOP:**
  - **A. Single clip, single speaker.** Use Veo native audio with the accent block, take the best of 2–4 samples, and run QA. No post needed if it passes.
  - **B. Multi-clip or extended, or multiple characters.** Keep Veo audio on, since it gives natural mouth motion. Isolate each character's dialogue (stem separation). Run **all of that character's lines in one STS pass** to a fixed Argentine target voice, remix with room tone, music and SFX, and spot-check sync.
  - **C. Script changes after generation, or narrator.** Use TTS (ElevenLabs Argentine voice, or Gemini 3.8 Flash TTS with a library or designed voice and an accent in the description), then a lip-sync model on single-face shots.

  **Do not** generate video-only to save 40% if you plan to use STS. STS needs Veo's speech as the source performance.
- **Persistent voice IDs on Google.** Designed voices expire, at 7 days on the Gemini API, and **cannot be re-cloned** because synthetic audio is rejected as a replication source. A recurring synthetic avatar therefore needs one of these:
  - (a) an **Extended Voice Library preset ID**, which is persistent. Filter `search` for Spanish/Argentine and check `accent`.
  - (b) a **licensed, consenting human voice actor** replicated on Agent Platform, which persists for 1 year after last use.
  - (c) a saved ElevenLabs voice.
- **Accent via STS (inference, unverified).** STS keeps the source's prosody and timing. If Veo's take was neutral, the target voice's own accent probably helps only partly. Fix the accent in the Veo take first (Q1), then STS for timbre consistency. Test whether an Argentine-native ElevenLabs voice "pulls" a neutral source toward rioplatense.
- **DubVoice.** If the client's "Dub Voice" is DubVoice.ai, it aggregates third-party voice providers. The Argentine voices and STS quality will be whatever the underlying provider (likely including ElevenLabs) offers. Ask the vendor for its provider list, STS or voice-changer availability, lip-sync capability and API access before building it into Jarvis.
- **Ethics guardrail.** Use only synthetic designed voices or consented, licensed voice talent. Never clone a real person without consent. Keep SynthID and other AI labels intact.

### Gaps
- DubVoice.ai's actual features (STS, lip-sync, API, which providers, Argentine voices) could not be verified. The site was unreachable and only vendor claims were found. It is also not confirmed that this is the tool the user means.
- ElevenLabs Voice Changer's handling of accent (source vs target) is not documented in anything I could read. The STS docs pages were not reachable.
- I could not query the Gemini Extended Voice Library to check whether **es-AR or rioplatense** voices exist. That needs a `voices.list` call in the client's project.
- There is no independent test of Gemini 3.8 Flash TTS rioplatense quality.
- Designed-voice expiry on **Agent Platform**, as opposed to the Gemini API, is not stated in the notebook.

---

## Q5. Lip-sync accuracy issues in Spanish

### Takeaway
There is **no independent, Spanish-specific lip-sync benchmark**. The evidence is vendor claims plus one mixed third-party rating (sync.so: medium quality, single-face only). The lowest-risk path is to keep Veo's own lip motion and change only the timbre via STS. Re-sync with a lip-sync model only when words or timing change, and only on single-face shots.

### Cited Findings
- Re-voicing that changes "pauses or word timing" breaks existing mouth movements, so an alignment or lip-sync pass is needed. — [GlobalGPT (search summary)](https://www.glbgpt.com/hub/how-to-make-characters-speak-in-veo-3-1-the-ultimate-guide-to-dialogue-audio-lip-sync/)
- Shorter lines with visible action beats improve Veo lip-sync. — [Veo3Gen (search summary)](https://www.veo3gen.app/blog/veo3gen-audio-keeps-going-wrong-9-fixes-for-dialogue-sfx-timing-and-music-mix-as)
- sync.so `lipsync-2-pro`:
  - Described as lipsync-2 with "diffusion-based enhancement for studio-grade lip synchronization", API-only. — [Runware (search summary)](https://runware.ai/creator/sync)
  - Claimed strong on "fine facial textures, teeth, and emotional nuance" for multilingual dubbing. This is vendor-style copy. — [Scenario (search summary)](https://www.scenario.com/models/sync-lipsync-2-pro)
  - sync.so's own blog (late 2025 to Jan 2026) has no measurements. — [sync.so blog (search summary)](https://ai.sync.so/blog/flawless-lip-syncing-original-audio-preservation); [sync.so Spanish page (search summary)](https://ai.sync.so/best-ai-tool-translate-video-spanish-lip-sync)
- A June 2026 comparison rates sync.so video lip-sync "Medium" quality and "Single-face only", below several competitors. Its methodology is unverified. — [Vozo best lip-sync 2026 (search summary)](https://www.vozo.ai/zh/blogs/best-lip-sync-software)
- Google's guide includes a customer quote praising Veo 3.1's "lifelike lip-sync". This is a testimonial, not a test. — [Google Cloud Blog prompting guide](https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-veo-3-1)

### Inferences
- Podcast or interview **two-shots** with both faces visible are the worst case for post lip-sync, since many tools are single-face. Shoot one speaking face per clip (Q2).
- Lip-sync QA checklist for Jarvis or a human reviewer:
  - Bilabials (p/b/m) close the lips.
  - "sh" sounds (sheísmo) show rounded, protruded lips.
  - No mouth motion on the silent listener.
  - Speech ends before the cut.
  - No burned-in subtitles. Use a negative prompt like "texts, captions, subtitles", as Google's cookbook does.

### Gaps
- No measured lip-sync accuracy data exists for Spanish or rioplatense for Veo 3.1 Lite, sync.so lipsync-2-pro, or DubVoice.
- No source compares lip-sync error between Veo-native audio and post TTS replacement.
