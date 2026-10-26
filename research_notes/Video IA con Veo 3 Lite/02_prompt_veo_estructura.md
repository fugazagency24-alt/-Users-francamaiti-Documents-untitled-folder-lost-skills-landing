# Official and expert Veo prompt structure (Veo 3.1 / 3.1 Fast / 3.1 Lite), state as of 2026-10-26

> **How this was researched, and how far to trust it (read first).** Research date: 2026-10-26. Primary sources I read in full:
> (a) Google's official notebooks and sample apps in `GoogleCloudPlatform/generative-ai`, repo HEAD dated 2026-10-26: `veo3_video_generation`, `veo3_advanced_controls`, `veo3_reference_to_video`, `gemini_omni_1_1_flash_video_gen`, and the V-Start prompting toolkit.
> (b) `google-gemini/cookbook`, HEAD 2026-10-19: `Get_started_Veo`, `Get_started_Omni`.
> (c) `GoogleCloudPlatform/vertex-ai-creative-studio`, HEAD 2026-10-24. This includes `veo_guide.md`, a copy of the Vertex AI Veo prompt guide from the Veo 3.0 preview era, the model registries, and Google's agent skills.
> (d) The `googleapis/python-genai` SDK source, HEAD 2026-10-24.
> (e) Two Google Cloud blog posts, fetched in full.
>
> Google's docs sites (docs.cloud.google.com, ai.google.dev) and deepmind.google were blocked by the proxy. Claims from them are marked **(search summary)**: I saw a search engine's summary, not the page. Practitioner claims are labeled as such. Most practitioner pages are vendor or SEO blogs. Items more than about 6 months old (before late April 2026) are flagged **[>6 mo]**.
>
> Naming: Google now calls Vertex AI the **"Gemini Enterprise Agent Platform"** ("Agent Platform"). The official notebooks say "Veo 3.1 on Agent Platform", and the docs pages are titled "Gemini Enterprise Agent Platform | Google Cloud Documentation". Model specs are covered in depth in sibling note `01_veo_vertex_specs.md`. This note repeats only what bears on prompting.

---

## 0. Which model is the client actually prompting, and what prompt-relevant controls does it expose?

### Takeaway
Nothing is called "Veo 3 Lite". The model is **Veo 3.1 Lite**: on Vertex/Agent Platform it is `veo-3.1-lite-generate-001` (Preview, released Apr 2–3, 2026), and on the Gemini API it is `veo-3.1-lite-generate-preview`. Lite takes the same prompt language as Veo 3.1. Its prompt-relevant controls are text prompt, first frame, last frame, `negativePrompt`, `seed`, `generateAudio`, 4/6/8 s, 16:9 or 9:16, 720p/1080p and up to 4 samples. It does **not** accept reference ("ingredients") images. Google's own sample app **forces the prompt rewriter on** for all Veo 3.1 models.

### Cited Findings
- The official Agent Platform notebook loads `video_model = "veo-3.1-generate-001"`, `video_model_fast = "veo-3.1-fast-generate-001"`, `video_model_lite = "veo-3.1-lite-generate-001"`. It describes Lite as "ideal for rapid prototyping and iteration". Its Lite example uses `duration_seconds=8, resolution="720p", person_generation="allow_adult", generate_audio=True`. — [GCP notebook veo3_video_generation](https://github.com/GoogleCloudPlatform/generative-ai/blob/main/vision/getting-started/veo3_video_generation.ipynb)
- Google Cloud blog, **Apr 3, 2026**: "We are introducing Veo 3.1 Lite, Google's most cost-effective video model on Vertex AI." All three Veo 3.1 tiers "feature native audio generation capabilities". The post contains no prompting advice and links to the Oct 2025 "ultimate prompting guide for Veo 3.1". — [Google Cloud blog: Veo 3.1 Lite](https://cloud.google.com/blog/products/ai-machine-learning/veo-3-1-lite-and-a-new-veo-upscaling-capability-on-vertex-ai)
- Release notes give Veo 3.1 Lite public preview on **April 2, 2026**. The Veo 3.1 model page lists Lite as Preview and "Use reference images: Not supported". — [Vertex AI release notes (search summary)](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/release-notes); [Veo 3.1 model page (search summary)](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/models/veo/3-1-generate)
- Google's MCP model registry lists `veo-3.1-lite-generate-001` with `SupportsGenerateAudio: true`, `SupportsFirstLast: true`, `SupportsReferenceImage: false`, `SupportsExtend: true`, durations 4/6/8, 16:9 and 9:16, MaxVideos 4. — [vertex-ai-creative-studio mcp-common/models.go](https://github.com/GoogleCloudPlatform/vertex-ai-creative-studio/blob/main/experiments/mcp-genmedia/mcp-genmedia-go/mcp-common/models.go)
- Google's Creative Studio app config marks `veo-3.1-lite-generate-001`, `veo-3.1-generate-001` and `veo-3.1-fast-generate-001` with `supports_prompt_enhancement=True, requires_prompt_enhancement=True`. The request builder then does "# Force True if model mandates it … enhance_prompt_for_api = True". — [config/veo_models.py](https://github.com/GoogleCloudPlatform/vertex-ai-creative-studio/blob/main/config/veo_models.py); [models/veo.py](https://github.com/GoogleCloudPlatform/vertex-ai-creative-studio/blob/main/models/veo.py)
- In the SDK, Vertex requests carry `seed`, `negativePrompt`, `enhancePrompt` and `generateAudio` in `parameters`. Gemini API requests raise `ValueError` for `seed`, `generate_audio`, `output_gcs_uri`, `fps`, `pubsub_topic`, `mask`, `compression_quality` and `labels`, so **seed and the audio on/off switch exist only on Vertex**. — [python-genai models.py](https://github.com/googleapis/python-genai/blob/main/google/genai/models.py); [python-genai types.py](https://github.com/googleapis/python-genai/blob/main/google/genai/types.py)
- `seed` is described as "best-effort reproducible video generation". — [mcp-veo-go README](https://github.com/GoogleCloudPlatform/vertex-ai-creative-studio/blob/main/experiments/mcp-genmedia/mcp-genmedia-go/mcp-veo-go/README.md)
- Gemini Omni 1.1 Flash (`gemini-omni-1.1-flash-preview` on Agent Platform, location `global`) is a separate Google video family. Its prompting differs from Veo: Interactions API, 3–10 s, `<IMAGE_REF_n>` binding tags, multi-turn edits. — [GCP notebook gemini_omni_1_1_flash_video_gen](https://github.com/GoogleCloudPlatform/generative-ai/blob/main/vision/getting-started/gemini_omni_1_1_flash_video_gen.ipynb)
- No Veo 4 had been announced as of Aug 2026 (third-party checks), and I found no Sept–Oct 2026 Veo launch. — [aireiter (Aug 2026)](https://aireiter.com/blog/veo-4); [queststudio (Aug 2026)](https://queststudio.io/blog/when-is-veo-4-coming-out)

### Inferences
- Since Lite has **no reference images**, identity on Lite can be anchored only through the **first frame** (image-to-video), optionally the **last frame**, the **verbatim character description**, and the **seed**. Prompt structure has to compensate for the missing ingredients feature (see §8).
- If the rewriter cannot be turned off on Veo 3.1 (see §7), Jarvis's prompts should be **complete and unambiguous** so Gemini's rewrite has nothing to invent: dialogue, voice and accent spelled out, a speaker for every line, and an explicit audio bed.

### Gaps
- I could not open the live Veo 3.1 model page. Whether `enhancePrompt=false` is rejected, ignored or honored on `veo-3.1-lite-generate-001` is not confirmed by an official doc; the only evidence is Google's sample-app flag (see §7).

---

## 1. Official prompt anatomy: elements, order, length, wording

### Takeaway
Google gives two compatible orderings. The Oct 2025 Cloud blog formula is **[Cinematography] + [Subject] + [Action] + [Context] + [Style & Ambiance]**. The Vertex prompt guide and notebooks list Subject → Action → Scene → Camera angle/movement → Lens → Style → Temporal → Audio. Audio goes in **separate sentences**. Google asks for "descriptive, specific, and clear" prose and **one continuous scene per short clip**. No official word limit exists.

### Cited Findings
- Cloud blog **[>6 mo; Oct 16, 2025]**: "**[Cinematography] + [Subject] + [Action] + [Context] + [Style & Ambiance]**". Verbatim example: "Medium shot, a tired corporate worker, rubbing his temples in exhaustion, in front of a bulky 1980s computer in a cluttered office late at night. The scene is lit by the harsh fluorescent overhead lights and the green glow of the monochrome monitor. Retro aesthetic, shot as if on 1980s color film, slightly grainy." — [Google Cloud blog: Ultimate prompting guide for Veo 3.1](https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-veo-3-1)
- Official notebook (current HEAD) checklist: "**Subject** … **Action** … **Scene** … **Camera angles** … **Camera movements** … **Lens effects** … **Style** … **Temporal elements** … **Audio:** Various sound effects or dialogue that guides the visuals through sound". For image-to-video the list is "Camera motion … Subject animation … Environmental animation … Audio". — [GCP notebook veo3_video_generation](https://github.com/GoogleCloudPlatform/generative-ai/blob/main/vision/getting-started/veo3_video_generation.ipynb)
- Vertex prompt guide, copy from the Veo 3.0 era **[>6 mo]**: the core components are "Subject, Action, Scene/Context, Cinematography, Visual Style, Ambiance, Audio". On audio: "Clearly specify if you want audio, using **separate sentences** to describe it." On realism: "**Photorealistic**: 'hyperrealistic,' 'shot on 8K camera,' 'sharp focus.'" — [vertex-ai-creative-studio veo_guide.md](https://github.com/GoogleCloudPlatform/vertex-ai-creative-studio/blob/main/experiments/veo-genetic-prompt-optimizer/veo_guide.md)
- The same guide's best practices say: "**Use Clear Language**: Write direct and unambiguous prompts. Avoid conversational or vague phrasing." and "**Focus on a Single Scene**: … Trying to describe multiple distinct events will likely result in a muddled or incomplete video. Generate complex sequences as separate clips." — [veo_guide.md](https://github.com/GoogleCloudPlatform/vertex-ai-creative-studio/blob/main/experiments/veo-genetic-prompt-optimizer/veo_guide.md)
- Vertex best-practices page (search summary): favors specific, direct wording, matching aspect ratio to platform, and dedicating each short prompt to a single scene. — [Best practices for Veo (search summary)](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/video/best-practice)
- Image-to-video: "If you're generating a video from an image you don't need to provide a prompt … however, a detailed prompt will help with video quality." — [GCP notebook veo3_video_generation](https://github.com/GoogleCloudPlatform/generative-ai/blob/main/vision/getting-started/veo3_video_generation.ipynb)
- Google's own Gemini→Veo meta-prompt in the notebook (model `gemini-3.8-flash`): "You are an expert video prompt engineer for Google's Veo model. Your task is to construct the most effective and optimal prompt string using the following keywords. **Every single keyword MUST be included.** Synthesize them into a single, cohesive, and cinematic instruction. **Do not add any new core concepts.** Output ONLY the final prompt string…" — [GCP notebook veo3_video_generation](https://github.com/GoogleCloudPlatform/generative-ai/blob/main/vision/getting-started/veo3_video_generation.ipynb)
- Google's V-Start toolkit builds prompts "based on the ideal structure for Veo" and links Google engineer Wafae Bakkali's guide. It also ships an **Alignment Eval** autorater: it breaks the prompt into sub-questions, and Gemini scores the video by visual question answering (VQA), 0–100%. — [V-Start README](https://github.com/GoogleCloudPlatform/generative-ai/blob/main/vision/sample-apps/V-Start/README.md)
- The same guide's "Using Gemini to Enhance Prompting" section suggests "Prompt Rewriting (Gemini → Veo)" with few-shot examples, and "Video Evaluation (Veo → Gemini)" as a critic. — [veo_guide.md](https://github.com/GoogleCloudPlatform/vertex-ai-creative-studio/blob/main/experiments/veo-genetic-prompt-optimizer/veo_guide.md)

### Inferences
- For talking UGC avatars, a practical order that merges both official orderings is: **Format/camera → Subject (verbatim identity block) → Action → Scene/lighting → Style/realism → Voice → Dialogue → Audio bed**, with audio and dialogue as separate sentences at the end. It follows the blog's "cinematography first" and the guide's "audio in separate sentences".
- Jarvis should copy Google's meta-prompt constraint, "every element MUST be included … do not add new core concepts". That stops Jarvis, and then Veo's own rewriter, from inventing extra people, music or captions.
- The "single scene" rule from the older guide conflicts with the newer timestamp/multi-shot workflow (see §3). For single-speaker UGC, follow the single-scene rule.

### Gaps
- No official prompt length or token limit was found for Veo 3.1. Google's examples run about 40–120 words. Whether very long prompts (200+ words) degrade adherence on Lite is untested in any source I found.
- No Google source says whether English scaffolding with Spanish dialogue beats an all-Spanish prompt for Spanish-language videos.

---

## 2. Audio prompting syntax: dialogue, subtitles, SFX, ambience, music, silence, accent

### Takeaway
**Google's own sources disagree on dialogue punctuation.** The Cloud blog and Gemini API guide use **quotes** (`A woman says, "We have to leave now."`). The **Vertex best-practices page says to use a colon and NO quotes**, because quotes can make Veo render the words as on-screen text (`A woman says: My name is Clara.`). Several current official Vertex samples also use the colon form. Label sound with `SFX:` and `Ambient noise:`. Suppress captions through `negativePrompt` ("texts, captions, subtitles"). No official source covers accent; practitioner consensus is to name the accent next to the line and write the script in local dialect.

### Cited Findings
**Dialogue: quotes (blog / Gemini API)**
- Cloud blog **[>6 mo]**: dialogue syntax `A woman says, "We have to leave now."`. Ingredients example: "He looks up at the woman and says in a weary voice, "Of all the offices in this town, you had to walk into mine."" and "…she replies, "You were highly recommended."" — [Google Cloud blog: Ultimate prompting guide](https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-veo-3-1)
- Gemini API Veo guide (search summary): use quotation marks for specific speech, e.g. `"This must be the key," he murmured.` — [Gemini API Veo docs (search summary)](https://ai.google.dev/gemini-api/docs/veo)
- Gemini cookbook dialogue example: `The first character start saying "oh my god, it is really hot in here!" - then the second answers "right? I'm melting down!"`, paired with `negative_prompt = "texts, captions, subtitles"`. — [cookbook Get_started_Veo](https://github.com/google-gemini/cookbook/blob/main/quickstarts/Get_started_Veo.ipynb)
- Google's agent skills (2026): "For Veo 3 models, use quotation marks for specific dialogue: `a robot says "HELLO WORLD"`." — [genmedia-video-editor SKILL.md](https://github.com/GoogleCloudPlatform/vertex-ai-creative-studio/blob/main/experiments/mcp-genmedia/skills/genmedia-video-editor/SKILL.md)

**Dialogue: colon, no quotes (Vertex docs and samples)**
- Vertex "Best practices for Veo" (search summary): "To prevent the model from rendering text in the video, use a colon (:) after the speaker's action to denote speech and avoid using quotation marks ("). Example `A woman says: My name is Clara.`, with the quoted version marked "not recommended". — [Best practices for Veo (search summary)](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/video/best-practice)
- Official Vertex notebook (current): `"sculpting a bowl on a pottery wheel while the person sculpting remarks: wow, I love this one"` (colon, no quotes). — [GCP notebook veo3_video_generation](https://github.com/GoogleCloudPlatform/generative-ai/blob/main/vision/getting-started/veo3_video_generation.ipynb)
- Google V-Start gallery "Dialogue" example (colon, no quotes, two speakers): "A medium shot in a dimly lit interrogation room. The seasoned detective says: Your story has holes. The nervous informant, sweating under a single bare bulb, replies: I'm telling you everything I know. The only other sounds are the slow, rhythmic ticking of a wall clock and the faint sound of rain against the window." — [V-Start gallery.js](https://github.com/GoogleCloudPlatform/generative-ai/blob/main/vision/sample-apps/V-Start/src/features/gallery.js)
- The V-Start prompt generator wraps user dialogue as `A character says: '<line>'` (colon plus single quotes). — [V-Start generator.js](https://github.com/GoogleCloudPlatform/generative-ai/blob/main/vision/sample-apps/V-Start/src/features/generator.js)
- Older Vertex guide **[>6 mo]**: "**Speech**: 'The man in the red hat says, 'Where is the rabbit?' Then the woman in the green dress next to him replies, 'There, in the woods.''" — [veo_guide.md](https://github.com/GoogleCloudPlatform/vertex-ai-creative-studio/blob/main/experiments/veo-genetic-prompt-optimizer/veo_guide.md)
- Practitioners (search summary): community workarounds include the colon form plus an explicit "no subtitles"/"no on-screen text" note. A dissenting vendor guide (Akool) says colon *and* quotes are "crucial triggers" for lip-sync. — [screenweaver](https://www.screenweaver.ai/blog/prompting-veo-guide); [akool](https://akool.com/blog-posts/google-veo-3-1-video-prompt-guide)

**SFX, ambience, emotion, music**
- Cloud blog: `SFX: thunder cracks in the distance`; `Ambient noise: the quiet hum of a starship bridge`; the timestamp example uses `Emotion: Wonder and reverence.` and `SFX: A swelling, gentle orchestral score begins to play.` Veo 3.1 "excels at generating realistic, synchronized sound, from multi-person conversations to precisely timed sound effects." — [Google Cloud blog: Ultimate prompting guide](https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-veo-3-1)
- Older Vertex guide: "The audio features water splashing in the background." / "Add soft music in the background." — [veo_guide.md](https://github.com/GoogleCloudPlatform/vertex-ai-creative-studio/blob/main/experiments/veo-genetic-prompt-optimizer/veo_guide.md)
- Google's Creative Studio skills write SFX in brackets: "`[loud thunder]`, `[gentle rain background]`". — [genmedia-video-editor SKILL.md](https://github.com/GoogleCloudPlatform/vertex-ai-creative-studio/blob/main/experiments/mcp-genmedia/skills/genmedia-video-editor/SKILL.md)
- Gemini Omni (Google, 2026; Omni not Veo): "Sound design: gentle wind, distant birdsong, and a soft orchestral swell. No dialogue." and "No dialogue or voiceover. No text overlay on screen." — [cookbook Get_started_Omni](https://github.com/google-gemini/cookbook/blob/main/quickstarts/Get_started_Omni.ipynb); [GCP notebook gemini_omni_1_1_flash](https://github.com/GoogleCloudPlatform/generative-ai/blob/main/vision/getting-started/gemini_omni_1_1_flash_video_gen.ipynb)

**Silence / no music**
- On Vertex, audio is a request flag (`generate_audio=True/False`). The Gemini API SDK path raises an error for `generate_audio`, so audio is always on there. — [python-genai models.py](https://github.com/googleapis/python-genai/blob/main/google/genai/models.py); [bananabanana (search summary)](https://bananabanana.pro/blog/veo-3-1-prompt-guide)
- Practitioners: unrequested soundtrack is a common failure. State "no music" once, or name only the sounds you want. Flow examples add "no music" to the sound cue. — [bananabanana (search summary)](https://bananabanana.pro/blog/veo-3-1-prompt-guide); [nereo](https://www.nereo.io/blog/google-flow-prompts)

**Delivery and accent**
- Google's Veo 3 tips, as quoted in a practitioner PDF: add delivery direction to the line, such as "whispering nervously" or "shouting angrily". — [Veo3 Prompting Guide PDF (search summary)](https://www.xavierstuder.com/wp-content/uploads/2025/07/Veo3-Prompting-Guide.pdf)
- **No official Google guidance on accents was found.** Practitioners: name the accent explicitly (e.g. "All dialogue must be in Spanish with a clear Argentinian rioplatense accent"), place it next to the line, use voseo and local vocabulary in the script, and expect hit-or-miss results; Spanish output "can sound a bit generic". — [arsturn](https://www.arsturn.com/blog/your-ultimate-guide-to-using-veo-3-for-spanish-language-video-content); [alandaitch](https://www.alandaitch.com/prompts)
- Google's own TTS story skill notes that with Gemini TTS "the voice itself carries gender and accent". That is TTS, where a voice is a fixed asset, unlike Veo's prompt-only voices. — [story-generator SKILL.md](https://github.com/GoogleCloudPlatform/vertex-ai-creative-studio/blob/main/experiments/mcp-genmedia/skills/story-generator/SKILL.md)

### Inferences
- **Default for this client (Vertex, Lite):** use the Vertex-documented form, `<visual speaker descriptor> says in <language/accent>, <delivery>: <line>`, without quotes. Put `subtitles, captions, on-screen text, text overlay, watermark` in `negativePrompt`, as the cookbook does. If a line comes out silent or mumbled, A/B test the quoted form with the same seed.
- Keep the word "subtitles" **out of the positive prompt**. Google's negative-prompt guidance says to describe what to exclude in the negative field rather than writing "no X" (see §6), so mentioning captions in the main prompt risks priming them. This inference is untested, but it is consistent with that guidance.
- Accent is a **probabilistic voice trait** in Veo; nothing pins a voice. Put three redundant cues in every clip: (1) the voice line ("native Argentine Rioplatense Spanish from Buenos Aires, sheísmo, voseo"), (2) the dialogue written in real rioplatense (vos, tenés, che, posta, re), (3) the same voice description verbatim across clips. Plan voice replacement in post as the guaranteed fix; that is covered by other notes.

### Gaps
- No Google source states which punctuation (colon or quotes) gives better lip-sync and fewer captions on **Veo 3.1 Lite** specifically. The conflict is unresolved, and the guidance comes from different pages.
- No source tests accent fidelity (Rioplatense vs neutral) on Veo 3.1 Lite. No source covers Spanish-specific dialogue syntax.

---

## 3. Timestamp / shot-list prompting, multi-shot within 8 s, JSON prompts: does it work?

### Takeaway
Timestamp prompting is **official**. The Cloud blog shows four 2-second beats in one 8 s generation using `[00:00-00:02]` syntax, and Google's V-Start tool builds such timelines (total ≤ 8 s). Practitioner tests say beat **order** is followed but exact **timecodes are loose**. JSON prompting has **no rigorous evidence** of better output. Google built a JSON vs plain-text A/B study into V-Start but published no results, and the most careful practitioner test found "better structure but not necessarily superior … quality".

### Cited Findings
- Cloud blog **[>6 mo]**, verbatim multi-shot example:
  `[00:00-00:02] Medium shot from behind a young female explorer with a leather satchel and messy brown hair in a ponytail, as she pushes aside a large jungle vine to reveal a hidden path.`
  `[00:02-00:04] Reverse shot of the explorer's freckled face, her expression filled with awe as she gazes upon ancient, moss-covered ruins in the background. SFX: The rustle of dense leaves, distant exotic bird calls.`
  `[00:04-00:06] Tracking shot following the explorer as she steps into the clearing and runs her hand over the intricate carvings on a crumbling stone wall. Emotion: Wonder and reverence.`
  `[00:06-00:08] Wide, high-angle crane shot, revealing the lone explorer standing small in the center of the vast, forgotten temple complex, half-swallowed by the jungle. SFX: A swelling, gentle orchestral score begins to play.`
  Note that each beat **re-describes the character**. — [Google Cloud blog: Ultimate prompting guide](https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-veo-3-1)
- Google V-Start "Timeline Prompting" errors if the "Total duration exceeds 8 seconds". Its meta-prompt outputs `timestamp: "00:00-00:02"` on one line, then "a single, detailed paragraph". "If the user's input mentions sound, incorporate it naturally into the description. If not, describe only the visuals." — [V-Start timeline.js](https://github.com/GoogleCloudPlatform/generative-ai/blob/main/vision/sample-apps/V-Start/src/features/timeline.js)
- Practitioner test (dreampixelforge, 2026): the timestamp syntax produced one cut and two shots in the order written, but "treat the exact timecodes loosely". — [dreampixelforge](https://www.dreampixelforge.com/blog/veo-3-prompts)
- Older Vertex guide: "the model may not execute literal edits like 'jump cut,' it will interpret them as stylistic cues." It also says to keep a short clip to one scene. — [veo_guide.md](https://github.com/GoogleCloudPlatform/vertex-ai-creative-studio/blob/main/experiments/veo-genetic-prompt-optimizer/veo_guide.md)
- Gemini Omni (2026; Omni, not Veo): it supports natural-language timing ("after 3 seconds, a woman enters") or `[0-3s] … [3-6s] …`. "By default, Omni may introduce multi-shot cinematic cuts … To force a continuous, single-camera perspective, explicitly specify: 'In a single unbroken scene…' / 'Continuous handheld shot, no scene cuts…'". — [cookbook Get_started_Omni](https://github.com/google-gemini/cookbook/blob/main/quickstarts/Get_started_Omni.ipynb)
- Veo 3.1 Reference-to-Video "is optimized for high-energy, short-form narratives. It excels at maintaining consistency across rapid intercutting and dynamic camera transitions" (not available on Lite). — [GCP notebook veo3_reference_to_video](https://github.com/GoogleCloudPlatform/generative-ai/blob/main/vision/getting-started/veo3_reference_to_video.ipynb)
- **JSON:** V-Start's preloaded study is titled "Veo Prompt Format Evaluation — Comparing JSON vs Plain Text prompts" (20 YouTube video pairs, blind A/B), and V-Start can convert prompts into "Plain Text, JSON, YAML or XML". No results are included in the repo. — [V-Start eval.js](https://github.com/GoogleCloudPlatform/generative-ai/blob/main/vision/sample-apps/V-Start/src/features/eval.js); [V-Start data/veo-youtube-study.json](https://github.com/GoogleCloudPlatform/generative-ai/blob/main/vision/sample-apps/V-Start/data/veo-youtube-study.json); [V-Start README](https://github.com/GoogleCloudPlatform/generative-ai/blob/main/vision/sample-apps/V-Start/README.md)
- VP-Land's hands-on Veo 3 test (search summary): JSON matched the envisioned scene more closely in one shot, but "JSON prompting offers better structure but not necessarily superior creative control or output quality." Other pro-JSON claims, including first-try success-rate percentages, come from vendor blogs with no stated method. — [VP-Land newsletter (search summary)](https://newsletter.vp-land.com/p/we-tested-json-prompting-in-veo-3-useful-hack-or-just-influencer-hype); [imagine.art](https://www.imagine.art/blogs/veo-3-json-prompting-guide)
- Google's own meta-prompts output **plain prose**: "Output ONLY the video prompt text - no analysis, no markdown, no asterisks, no explanations." — [V-Start generator.js](https://github.com/GoogleCloudPlatform/generative-ai/blob/main/vision/sample-apps/V-Start/src/features/generator.js)

### Inferences
- **Single-speaker UGC:** don't ask for multi-shot cuts. Ask for "single continuous take, no cuts" and use timestamps only to time **beats inside one take**, e.g. `[00:00-00:04]` line 1, `[00:04-00:08]` show product + line 2. Cuts are where faces and voices drift.
- **Interview, podcast or story with 2+ characters:** prefer **one speaker per clip or beat**, as in the Cloud blog's ingredients workflow, which gives each speaker a separate shot. Repeat each character's full descriptor in every beat, as the official timestamp example does.
- **JSON:** let Jarvis keep a JSON "shot spec" internally for QA and versioning, but render it to labeled plain prose before sending it to Veo. That matches Google's own pipelines, and since the rewriter (likely forced on) is an LLM, prose input is the safer assumption.

### Gaps
- The results of Google's V-Start JSON vs plain-text study were not found.
- No source measures timecode accuracy, or how often Veo 3.1 **Lite** inserts unrequested cuts.

---

## 4. Dialogue length: words per second in 4/6/8 s clips, and what happens when a line is too long

### Takeaway
Google publishes **no word limit**. Practitioner consensus for an 8 s English clip is about **15–20 words, up to roughly 22–26** with fast delivery. Overlong lines come out **rushed or cut off**. Split long scripts across clips, or continue them with extension.

### Cited Findings
- About 15–20 English words per 8 s clip to avoid the model speeding up. — [dramapixel (search summary)](https://dramapixel.ai/blogs/stop-veo-3-unwanted-dialogues)
- About 16–22 words for comfortable pacing, about 26 if quick. Overlong lines bring rushed delivery or a clipped ending. Split dialogue across clips, or use extension. — [veo3ai.io (2026, search summary)](https://www.veo3ai.io/blog/veo-3-text-to-speech-voiceover-guide-2026)
- Packing in too much text makes the character talk too fast. — [Replicate blog (search summary)](https://replicate.com/blog/using-and-prompting-veo-3)
- Keep each line under about 5 seconds. — [eastondev (search summary)](https://eastondev.com/blog/en/posts/ai/20251207-veo3-audio-generation-guide/)
- Veo 3.1 supports 4, 6 or 8 s, so the speech budget scales with duration. — [prompt-architects (search summary)](https://prompt-architects.com/blog/101-veo-dialogue-prompts); durations confirmed in [GCP notebook veo3_video_generation](https://github.com/GoogleCloudPlatform/generative-ai/blob/main/vision/getting-started/veo3_video_generation.ipynb)
- Google's TTS→Veo pipeline measures the voice duration first, then requests a matching Veo length (4, 6 or 8 s). — [story-generator SKILL.md](https://github.com/GoogleCloudPlatform/vertex-ai-creative-studio/blob/main/experiments/mcp-genmedia/skills/story-generator/SKILL.md)
- For extension, voice carries over poorly unless speech is present in the **last second** of the source clip. — [Gemini API Veo docs (search summary)](https://ai.google.dev/gemini-api/docs/veo)

### Inferences
- Working budget for **Spanish UGC** (inference: about 2.3–2.6 spoken words/s at natural pace, leaving roughly 0.5–1 s of head/tail):
  - **8 s:** ≤ 18–20 words.
  - **6 s:** ≤ 13–14 words.
  - **4 s:** ≤ 8–9 words.
  - At most 2 sentences per clip, and at most 1 line per speaker per clip in multi-character scenes.
- **Tail rule:** for a **standalone** clip, end the line about 0.5 s before the end to avoid cut-off. For a clip that **will be extended**, let speech run into the last second so the voice carries over. Jarvis has to know which case applies.
- Jarvis should count words (or estimate TTS duration) before sending, and split automatically when a line is over budget.

### Gaps
- No measured words-per-second data exists for Veo in Spanish, and none for Lite vs full 3.1.

---

## 5. Camera language that works (and what Veo ignores)

### Takeaway
Veo understands the standard film vocabulary Google lists: shot size, angle, movement, lens/DOF. For realistic UGC, practitioners combine **selfie or handheld framing + one camera move + natural light + "no beauty filter"-style realism cues**. Two documented failure points: specific selfie geometry ("arm's length") often isn't held, and literal edit instructions ("jump cut") are read as style, not executed.

### Cited Findings
- Official term lists in the current notebook. **Angles:** "Eye-Level Shot, Low-Angle, High-Angle, Bird's-Eye, Top-Down, Worm's-Eye, Dutch Angle, Close-Up, Extreme Close-Up, Medium Shot, Full Shot, Long Shot, Wide Shot, Establishing Shot, Over-the-Shoulder Shot, Point-of-View (POV) Shot". **Movements:** "Static Shot (or fixed), Pan, Tilt, Dolly (In/Out), Zoom, Truck, Pedestal, Crane Shot, Aerial, Drone, **Handheld, Shaky Cam**, Whip Pan, Arc Shot". **Lens:** "Wide-Angle Lens (e.g., 24mm), Telephoto Lens (e.g., 85mm), Shallow Depth of Field, Bokeh, Deep Depth of Field, Lens Flare, Rack Focus, Fisheye, Vertigo Effect". — [GCP notebook veo3_video_generation](https://github.com/GoogleCloudPlatform/generative-ai/blob/main/vision/getting-started/veo3_video_generation.ipynb)
- Cloud blog: "Dolly shot, tracking shot, crane shot, aerial view, slow pan, POV shot"; "Wide shot, close-up, extreme close-up, low angle, two-shot"; "Shallow depth of field, wide-angle lens, soft focus, macro lens, deep focus". — [Google Cloud blog: Ultimate prompting guide](https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-veo-3-1)
- Gemini cookbook: shot composition "single shot", "two shot", "over-the-shoulder shot"; positioning "eye level", "high angle", "worms eye", "dolly shot", "zoom shot", "pan shot", "tracking shot". — [cookbook Get_started_Veo](https://github.com/google-gemini/cookbook/blob/main/quickstarts/Get_started_Veo.ipynb)
- Official handheld example: "An intense handheld camera shot during a chaotic marketplace chase. The camera struggles to keep up, with jerky movements and quick, unstable pans…" — [V-Start gallery.js](https://github.com/GoogleCloudPlatform/generative-ai/blob/main/vision/sample-apps/V-Start/src/features/gallery.js)
- "While the model may not execute literal edits like 'jump cut,' it will interpret them as stylistic cues." — [veo_guide.md](https://github.com/GoogleCloudPlatform/vertex-ai-creative-studio/blob/main/experiments/veo-genetic-prompt-optimizer/veo_guide.md)
- Practitioner test: a selfie talking-head prompt returned the quoted dialogue word for word, but "the arm's-length framing did not hold". The output was a tighter head-and-shoulders crop with the arm out of frame. — [dreampixelforge](https://www.dreampixelforge.com/blog/veo-3-prompts)
- Practitioners: one camera move per clip (nereo). Selfie recipes add "slight handheld sway" and "no makeup" for realism (viralmint). — [nereo](https://www.nereo.io/blog/google-flow-prompts); [viralmint](https://viralmint.net/tools/veo-3-prompts/)
- Image-to-video tip: "Ensure actions and speech descriptions align with the subjects in the image." — [veo_guide.md](https://github.com/GoogleCloudPlatform/vertex-ai-creative-studio/blob/main/experiments/veo-genetic-prompt-optimizer/veo_guide.md)

### Inferences
- For UGC on Lite, **frame the start image as the selfie/handheld composition you want**: phone-front-camera crop, eye level, slight wide-angle look. Then the prompt only has to say "keep this framing, subtle handheld sway". On image-to-video, the first frame governs geometry far better than words do.
- Use **one** movement keyword per clip (e.g. "subtle handheld sway" OR "slow push-in"). Avoid stacking crane/arc/whip moves in talking clips, because they force re-rendering of the face from new angles, which is when identity drift appears.

### Gaps
- No source tests whether numeric focal lengths (24mm vs 85mm) or "iPhone front camera" phrasing change Veo output reliably.

---

## 6. Negative prompts on Veo: the field, best use, and the "no subtitles" pitfall

### Takeaway
Vertex supports a separate **`negativePrompt`** field. Google's guidance is to **list the unwanted things as plain nouns/adjectives** ("urban background, man-made structures"), not with "no"/"don't". Google's own dialogue sample uses `negative_prompt = "texts, captions, subtitles"`. Inside the main prompt, phrase exclusions positively.

### Cited Findings
- "Specify what to *exclude* from your video. Describe what you want to discourage, rather than using words like 'no' or 'don't'." Example: "**Negative prompt**: urban background, man-made structures, dark, stormy, or threatening atmosphere." — [veo_guide.md](https://github.com/GoogleCloudPlatform/vertex-ai-creative-studio/blob/main/experiments/veo-genetic-prompt-optimizer/veo_guide.md); same guidance on the Vertex prompt guide (search summary) — [Gemini API / Vertex guides (search summary)](https://bananabanana.pro/blog/veo-3-1-prompt-guide)
- Cloud blog: specify "a desolate landscape with no buildings or roads" instead of "no man-made structures". — [Google Cloud blog: Ultimate prompting guide](https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-veo-3-1)
- Gemini cookbook: the dialogue example uses `negative_prompt = "texts, captions, subtitles"`; image-to-video and extend examples use `"ugly, low quality, static, weird physics"`. — [cookbook Get_started_Veo](https://github.com/google-gemini/cookbook/blob/main/quickstarts/Get_started_Veo.ipynb)
- Google agent skill: "Explicitly exclude unwanted elements using the `negative_prompt` parameter (e.g., 'blurry', 'static', 'distorted faces')." — [genmedia-video-editor SKILL.md](https://github.com/GoogleCloudPlatform/vertex-ai-creative-studio/blob/main/experiments/mcp-genmedia/skills/genmedia-video-editor/SKILL.md)
- SDK: `negative_prompt` — "Explicitly state what should not be included in the generated videos"; it is sent as `parameters.negativePrompt` on Vertex. — [python-genai types.py](https://github.com/googleapis/python-genai/blob/main/google/genai/types.py); [python-genai models.py](https://github.com/googleapis/python-genai/blob/main/google/genai/models.py)
- Lite supports a negative prompt (third-party listing). The Gemini API docs reportedly don't list the field, while Vertex accepts it. — [therundown (search summary)](https://www.therundown.ai/tools/veo-3-1-lite); [bananabanana (search summary)](https://bananabanana.pro/blog/veo-3-1-prompt-guide)
- Omni, a different model, accepts natural-language prohibitions inside the prompt: "No dialogue or voiceover. No text overlay on screen." — [cookbook Get_started_Omni](https://github.com/google-gemini/cookbook/blob/main/quickstarts/Get_started_Omni.ipynb)

### Inferences
- Recommended standing negative prompt for avatar UGC on Vertex, in noun form, no "no": `subtitles, captions, on-screen text, text overlay, watermark, logo, background music, extra people, second speaker, face morphing, distorted face, extra fingers, plastic skin, airbrushed skin, cartoon, CGI, 3D render, low quality, blurry`. Drop "background music" when music is wanted. Drop "second speaker" in multi-character clips.
- Keep the negative list short and stable across clips. Changing it changes the sampling and can shift the face and voice, like changing the prompt.

### Gaps
- No quantitative evidence on how much `negativePrompt` reduces captions on Veo 3.1 Lite. No source says whether negatives also steer the **audio** track, e.g. "background music".

---

## 7. The prompt rewriter (`enhancePrompt`): on or off for precise control?

### Takeaway
On Vertex, `enhancePrompt` defaults to **true** (Gemini rewrites your prompt), and the docs warn that turning it off may hurt quality and adherence. Google's own Creative Studio app marks **every Veo 3.1 model, Lite included, as `requires_prompt_enhancement=True`** and forces it on. The practical lever is therefore **prompt completeness, not the toggle**.

### Cited Findings
- "Turn off Veo's prompt rewriter" (search summary): the REST field is `parameters.enhancePrompt`; default `true` "uses Gemini to enhance the prompt"; turning it off means "the quality of the videos and how well the output resembles the prompt that you supplied may be impacted". The rewritten prompt is returned in the response "only if the original prompt is fewer than 30 words". The doc's code example uses `veo-2.0-generate-001`. — [Turn off the prompt rewriter (search summary)](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/video/turn-the-prompt-rewriter-off)
- Google Creative Studio config: `veo-3.1-generate-001`, `veo-3.1-fast-generate-001` and `veo-3.1-lite-generate-001` all have `supports_prompt_enhancement=True, requires_prompt_enhancement=True, default_prompt_enhancement=True`, and the request builder says "# Force True if model mandates it". — [config/veo_models.py](https://github.com/GoogleCloudPlatform/vertex-ai-creative-studio/blob/main/config/veo_models.py); [models/veo.py](https://github.com/GoogleCloudPlatform/vertex-ai-creative-studio/blob/main/models/veo.py)
- The SDK exposes `enhance_prompt` ("Whether to use the prompt rewriting logic") and forwards it to Vertex as `parameters.enhancePrompt`. — [python-genai types.py](https://github.com/googleapis/python-genai/blob/main/google/genai/types.py); [python-genai models.py](https://github.com/googleapis/python-genai/blob/main/google/genai/models.py)
- Google's genetic prompt-optimizer experiment treats Gemini rewriting of Veo prompts, plus video autorating, as the path to quality. It scores "Intent Fidelity", i.e. whether the augmented prompt "accurately preserves the core meaning and intent of the original user prompt". — [veo-genetic-prompt-optimizer doc](https://github.com/GoogleCloudPlatform/vertex-ai-creative-studio/blob/main/docs-site/src/content/docs/experiments/veo-genetic-prompt-optimizer/index.md)

### Inferences
- Assume the rewriter is **always on** for Veo 3.1 Lite unless a test proves otherwise. Send `enhancePrompt=false` once with a fixed seed and check whether the output changes or an error comes back.
- Rewriter-proof prompts:
  - Exceed about 30 words; the rewriter clearly targets short prompts.
  - Specify everything the rewriter might otherwise "improve": music or none, number of people, cuts or none, language and accent, exact line.
  - Avoid ambiguous style words like "cinematic". They invite the rewriter to add dramatic score, camera moves and lighting, which runs against raw UGC realism.
- A Gemini rewriter writing in English may "neutralize" a Spanish accent instruction or translate the dialogue. Keeping the dialogue and the accent cue verbatim in the prompt is the only control available.

### Gaps
- No official doc confirms that Veo 3.1 (or Lite) rejects or ignores `enhancePrompt=false`; the evidence is Google's sample-app flag. No source shows what the rewriter does to non-English dialogue.

---

## 8. Identity and voice consistency, and multi-character attribution (client pain points 1, 3, 5)

### Takeaway
Official levers:
1. Repeat the **identical** character + voice description in every prompt.
2. Reuse the same **seed** (Vertex best practices, search summary).
3. Anchor the face with a **first-frame image**. Reference images are not available on Lite.
4. Attribute every line to a **visible, distinctive descriptor** ("the man in the red hat says…"), with explicit turn order ("then … replies").

For extension, the voice carries over only if speech is present in the source clip's final second.

### Cited Findings
- Vertex best practices (search summary): a three-scene example **repeats the same character and voice description** in each prompt and recommends **the same seed** to keep visuals, style and voice consistent across scenes. — [Best practices for Veo (search summary)](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/video/best-practice)
- A secondary source attributes to Google: "copy and paste the entire, unchanged character description into your prompt for every new scene"; a seed "only slightly improves determinism". Exact page unconfirmed; it came from one of these, in one search summary: [ulazai](https://ulazai.com/character-consistency/); [arsturn](https://www.arsturn.com/blog/veo-3-character-consistency-guide); [sider](https://sider.ai/blog/ai-tools/how-veo-3_1-maintains-character-scene-consistency-in-ai-video)
- Image-to-video with multiple people: "If multiple subjects are present, clearly specify who is performing an action (e.g., 'The man in the red hat,' 'The woman in the blue dress')." — [veo_guide.md](https://github.com/GoogleCloudPlatform/vertex-ai-creative-studio/blob/main/experiments/veo-genetic-prompt-optimizer/veo_guide.md)
- Official two-speaker pattern: "The seasoned detective says: … The nervous informant, sweating under a single bare bulb, replies: …" — [V-Start gallery.js](https://github.com/GoogleCloudPlatform/generative-ai/blob/main/vision/sample-apps/V-Start/src/features/gallery.js). Also "The man in the red hat says, … Then the woman in the green dress next to him replies, …" — [veo_guide.md](https://github.com/GoogleCloudPlatform/vertex-ai-creative-studio/blob/main/experiments/veo-genetic-prompt-optimizer/veo_guide.md)
- Official multi-shot dialogue workflow: one shot per speaker. "Using the provided images for the detective, the woman, and the office setting, create a medium shot of the detective behind his desk. He looks up at the woman and says in a weary voice, …", then "create a shot focusing on the woman … she replies, …". This uses ingredients, which Lite lacks. — [Google Cloud blog: Ultimate prompting guide](https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-veo-3-1)
- Practitioners (search summary): speaker mix-ups are common when characters have similar descriptions. Anchor each line to a visual description, not a name ("The model has never met 'Sarah.' It has met 'the woman in the red coat.'"). Make turn-taking explicit and keep lines short. One tester found bare `Man: … / Woman: …` script labels produced one silent speaker or mismatched lines. If the description changes between segments, "the voices may change". — Sources in that search summary, exact page attribution unconfirmed: [prompt-architects](https://prompt-architects.com/blog/101-veo-dialogue-prompts); [eastondev](https://eastondev.com/blog/en/posts/ai/20251207-veo3-audio-generation-guide/); [glbgpt](https://www.glbgpt.com/hub/how-to-make-characters-speak-in-veo-3-1-the-ultimate-guide-to-dialogue-audio-lip-sync/); [replicate](https://replicate.com/blog/using-and-prompting-veo-3)
- First/last frame "tends to work best when the starting and ending frames are similar in nature." — [GCP notebook veo3_advanced_controls](https://github.com/GoogleCloudPlatform/generative-ai/blob/main/vision/getting-started/veo3_advanced_controls.ipynb)
- Extension on Gemini API: voice doesn't carry over well unless speech is in the final second. Extension conditions on the last second (24 frames). Input must be Veo-generated. Total up to 148 s (about 20 extensions of 7 s). — [Gemini API Veo docs (search summary)](https://ai.google.dev/gemini-api/docs/veo); [cookbook Get_started_Veo](https://github.com/google-gemini/cookbook/blob/main/quickstarts/Get_started_Veo.ipynb)
- Vertex extend: input MP4, 1–30 s, 24 fps, 720p/1080p/4k, 16:9 or 9:16; output is a 7 s extension. — [mcp-veo-go README](https://github.com/GoogleCloudPlatform/vertex-ai-creative-studio/blob/main/experiments/mcp-genmedia/mcp-genmedia-go/mcp-veo-go/README.md); [Extend Veo videos (search summary)](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/video/extend-a-veo-video)
- Google's character-consistency demo pipeline: Gemini writes a detailed facial profile from photos → Imagen generates the person in the new scene → the most look-alike image is selected and outpainted → that image goes to Veo with a Gemini-written video prompt. — [veo3-character-consistency doc](https://github.com/GoogleCloudPlatform/vertex-ai-creative-studio/blob/main/docs-site/src/content/docs/experiments/veo3-character-consistency/index.md)
- Omni 1.1 Flash (alternative): `<IMAGE_REF_0>`, `<IMAGE_REF_1>` "Binds images … to specific character identities". It was shown binding 3 characters without "blending identities", and multi-turn extension "fully supports" dialogue. — [cookbook Get_started_Omni](https://github.com/google-gemini/cookbook/blob/main/quickstarts/Get_started_Omni.ipynb)

### Inferences
- **Character Bible (Jarvis):** store per avatar a frozen **IDENTITY BLOCK** (age, ethnicity/nationality, skin tone and marks, hair, eyes, distinctive accessory, wardrobe) and a frozen **VOICE BLOCK** (gender, age, timbre, pace, accent). Paste both **byte-identical** into every clip, plus the same seed and the same approved first-frame still. Never paraphrase.
- **Multi-character:**
  - Give each character a **visually unmistakable, permanent tag**: hair colour, garment colour and screen position ("the woman on the left in the mustard sweater"). Characters must differ on at least two of these axes, plus clearly different voice blocks (e.g. "deep raspy male voice, 50s" vs "bright female voice, 20s").
  - Use the descriptor, not the name, in the dialogue line.
  - Use "then … replies:" for order.
  - Use at most 2 speakers per clip, ideally 1 line each.
  - For long conversations, cut to **one speaker per clip** from that speaker's own first frame.
- **Extension:** extend only from clips where the avatar's face is frontal and well lit in the last second. If the dialogue continues, the speech must reach the final second. Otherwise, start a fresh image-to-video clip from the same approved still, not from a drifted last frame.
- **First = last frame (untested inference):** Lite supports first+last frame. Passing the same approved avatar still as both ends could pin identity at both ends of an 8 s talking clip. A/B test it.

### Gaps
- No official, measured comparison of identity drift (I2V-only vs reference images vs extension) on Lite.
- The Vertex best-practices three-scene example could not be read verbatim (search summary only).

---

## 9. Objective: the definitive prompt anatomy and copy-paste patterns (synthesis for the SOP)

### Takeaway
The best-supported recipe for the client's case (Veo 3.1 Lite on Vertex, Spanish UGC avatars) is: labeled plain-prose sections in a fixed order; a byte-identical identity and voice block; one scene and one camera move; dialogue in colon form with a speaker descriptor, an accent cue and a word budget; an explicit audio bed; a stable `negativePrompt`; fixed seed, first-frame still, 2–4 samples; and Gemini-based alignment QA. The templates below are **inferences assembled from the cited official patterns**. They are not Google-published templates, so validate them with A/B tests at fixed seed.

### Cited Findings
- Official ingredients: the formula order ([Cloud blog](https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-veo-3-1)); audio in separate sentences ([veo_guide.md](https://github.com/GoogleCloudPlatform/vertex-ai-creative-studio/blob/main/experiments/veo-genetic-prompt-optimizer/veo_guide.md)); colon dialogue without quotes ([Best practices (search summary)](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/video/best-practice)); `SFX:` and `Ambient noise:` labels ([Cloud blog](https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-veo-3-1)); a caption negative prompt ([cookbook](https://github.com/google-gemini/cookbook/blob/main/quickstarts/Get_started_Veo.ipynb)); the same description plus the same seed ([Best practices (search summary)](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/video/best-practice)); 1–4 samples per request ([veo3_advanced_controls](https://github.com/GoogleCloudPlatform/generative-ai/blob/main/vision/getting-started/veo3_advanced_controls.ipynb)); a Gemini VQA alignment autorater ([V-Start README](https://github.com/GoogleCloudPlatform/generative-ai/blob/main/vision/sample-apps/V-Start/README.md)).

### Inferences

**A. Standard request settings (Vertex, Lite)**
```
model: veo-3.1-lite-generate-001
image: <approved avatar still, 9:16, same file every clip>   # identity anchor (Lite has no reference images)
config: aspect_ratio="9:16", resolution="1080p" (or 720p for drafts), duration_seconds=8,
        number_of_videos=2..4, seed=<fixed per avatar/campaign>, person_generation="allow_adult",
        generate_audio=True, negative_prompt=<standard list>, enhance_prompt=<test; likely forced True>
```

**B. Single-avatar UGC talking clip (8 s, ≤ 18–20 Spanish words)**
```
Vertical smartphone selfie video, single continuous take with no cuts. Medium close-up at eye level,
the phone held by the woman herself, subtle natural handheld sway.
Subject: [IDENTITY BLOCK — pasted verbatim every clip, e.g. a 29-year-old Argentine woman with olive
skin, light freckles across the nose, shoulder-length wavy dark-brown hair with a middle part, brown
eyes, thin gold hoop earrings, oversized cream knit sweater].
Action: she looks straight into the lens, smiles briefly, then lifts the serum bottle next to her cheek.
Scene: small sunlit bedroom in a Buenos Aires apartment, plants and an unmade bed softly out of focus
behind her, warm late-afternoon window light from camera left.
Style: photorealistic, raw phone front-camera footage, natural skin texture with visible pores,
true-to-life color, no beauty filter look.
Voice: [VOICE BLOCK — verbatim, e.g. warm, confident female voice in her late twenties, native
Rioplatense Spanish from Buenos Aires, with sheísmo and voseo, relaxed conversational pace].
Dialogue: the woman in the cream sweater says in Argentine Rioplatense Spanish, casually and smiling:
Che, ¿vos sabés lo que me cambió la piel este sérum? En dos semanas, posta.
Audio: only her voice, close to the phone microphone, with quiet room tone.
negative_prompt: subtitles, captions, on-screen text, text overlay, watermark, logo, background music,
extra people, face morphing, distorted face, plastic skin, airbrushed skin, cartoon, CGI, blurry
```

**C. Two-person interview/podcast clip (8 s, 1 line each, ≤ 9–10 words per line)**
```
Static medium two-shot at eye level, single continuous take with no cuts, a small podcast studio with
foam panels, two microphones on boom arms, soft key light.
On the left: [IDENTITY BLOCK A — e.g. a 45-year-old Argentine man with a grey-streaked beard, black
round glasses, navy denim shirt]. On the right: [IDENTITY BLOCK B — e.g. a 27-year-old Argentine woman
with a high red-brown ponytail, mustard-yellow sweater].
Voices: the man on the left has [VOICE BLOCK A — deep, slightly raspy male voice, Rioplatense
Spanish from Buenos Aires]; the woman on the right has [VOICE BLOCK B — bright, quick female voice,
Rioplatense Spanish from Buenos Aires].
The man on the left with the grey beard leans into his microphone and says: ¿Y cuánto tardaste en
recuperar la inversión?
Then the woman on the right in the mustard sweater laughs and replies: Tres semanas, posta, ni yo lo creía.
Only the speaking person's lips move. Audio: their two voices with close-mic studio sound and quiet room tone.
negative_prompt: (standard list), third person, voice-over narrator
```
For longer conversations: one clip per speaker turn, from that speaker's own approved still, with the listener off-screen or seen from behind.

**D. Storytelling beats inside 8 s (Veo 3.1 / Fast with references; on Lite keep ≤ 2 beats and one location)**
```
[00:00-00:04] Medium close-up, handheld, [IDENTITY BLOCK A] sits at a kitchen table at night,
staring at her phone. The young woman in the green hoodie says, worried, in Rioplatense Spanish:
No puede ser, otra vez sin luz. Ambient noise: refrigerator hum, distant traffic.
[00:04-00:08] Same shot continues, the camera drifts to reveal [IDENTITY BLOCK B] in the doorway.
The older man in the grey cardigan replies calmly in Rioplatense Spanish: Tranqui, ya lo resolvemos.
SFX: a light switch clicks.
```

**E. Extension continuation prompt (voice must be audible in the source clip's last second)**
```
Continue the same continuous shot with no cut: [IDENTITY BLOCK verbatim] keeps talking to the camera
in the same voice, [VOICE BLOCK verbatim]. She says in Rioplatense Spanish: <≤ 15 words>.
Audio: only her voice and the same quiet room tone.
```

**F. Rules for Jarvis (system-prompt bullets)**
1. Output plain prose in the fixed section order (format/camera → subject → action → scene → style → voice → dialogue → audio). No markdown and no JSON sent to Veo.
2. Paste the IDENTITY and VOICE blocks byte-identically, and never paraphrase them. Use the same seed and the same first-frame still per avatar.
3. One scene, one camera move, and "single continuous take with no cuts" unless cuts are explicitly required.
4. Every line is attributed to a visible descriptor plus a position. Use "then … replies:" for turns, at most 2 speakers and 1 line each per clip.
5. Dialogue format: `<descriptor> says in Argentine Rioplatense Spanish, <delivery>: <line>`, with no quotes. Write the line in real rioplatense, not neutral Spanish.
6. Word budget: 8 s ≤ 18–20, 6 s ≤ 13–14, 4 s ≤ 8–9. Split anything over budget into new clips.
7. Always state the audio bed (voice + room tone / SFX) and whether there is music. Keep caption, music and extra-people suppression in `negativePrompt`, not the main prompt.
8. Avoid vague style words ("cinematic", "epic") for UGC. Use concrete realism cues instead (phone footage, natural skin texture, true-to-life colour).
9. Generate 2–4 samples, auto-score them with a Gemini VQA rubric (identity match against the still, lip-sync, accent, captions, extra people, cut-offs), and keep the best. Re-roll only failures.

### Gaps
- The templates have not been run on Veo 3.1 Lite in this research. Colon vs quotes, first=last frame, and the word budgets each need an A/B test at fixed seed.
- Google's current official guidance on the 2026 behaviour of Veo 3.1 Lite (rewriter, accent handling, caption suppression) could not be read directly, because the docs domains were blocked.
- "Dub Voice" / "DubVoice" (the client's upcoming voice tool) was out of scope for this note and is not covered here.
