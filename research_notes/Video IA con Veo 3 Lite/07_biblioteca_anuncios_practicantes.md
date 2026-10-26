# 07 — Ad library and practitioner sweep: what the market teaches about prompting Veo for UGC ads (state as of 2026-10-26)

> **Method and limits. Read this first.**
> - **This is an INDIRECT sweep.** I could not load the Meta Ad Library or the TikTok Creative Center. The proxy refuses connections to facebook.com, and also to socialmediatoday.com, marketingdive.com, ftc.gov, transparency.meta.com, ads.tiktok.com and dev.to. All of these were tested with curl on 2026-10-26. WebFetch failed for every non-GitHub host I tried.
> - What I did instead:
>   1. Ran 18 web searches (EN/ES/PT) for ads, landing pages, courses and offers that sell Veo 3 prompt methods.
>   2. Cloned the public GitHub prompt collections and read them in full.
>   3. Read Google Cloud pages directly (cloud.google.com was reachable).
> - **Source labels:**
>   - **(search summary)** means the claim comes from a search-engine summary, not a page I read. It is weaker evidence.
>   - **[>6 mo]** marks items older than about late April 2026.
>   - Everything from GitHub or cloud.google.com was read directly.
> - **Model context.** The client's "Veo 3 Lite" is **Veo 3.1 Lite**. Google's Cloud blog post of **2026-04-03** calls it "our most cost-effective model, empowering businesses to build high-volume video applications and rapidly iterate and scale" ([Google Cloud blog, read directly](https://cloud.google.com/blog/products/ai-machine-learning/veo-3-1-lite-and-a-new-veo-upscaling-capability-on-vertex-ai)). For the exact ID (`veo-3.1-lite-generate-001`) and its feature limits, see sibling note `01_veo_vertex_specs.md`. Lite has **no reference images ("ingredients")**.
> - **"Dub Voice"** is most likely DubVoice.ai; see sibling note `03_voz_acento_argentino.md`. I found nothing new on it in this sweep.
> - **What was not found:** no repository named "awesome-veo3-prompts" could be located. The GitHub search API is blocked, and the obvious owner/name guesses do not exist. The closest real collections are analyzed in Q2.

---

## Q1. Ad library and course/offer sweep (ES/PT/EN): what is being sold to teach "Veo 3 prompts for ads/UGC", and what concrete techniques do the offers claim?

### Takeaway
The ES/PT/EN market for this (seen indirectly through course and offer pages) sells four kinds of product:
- generic Veo 3 courses on Hotmart and Udemy;
- cheap prompt packs on Gumroad;
- SaaS "UGC builders" that wrap Veo.

The techniques these products advertise are generic:
- character consistency through structured, repeated prompts;
- JSON prompts;
- "viral prompt generators";
- an "AI influencer" lesson;
- hook → problem → solution → CTA.

None of them shows a tested method for a **specific regional accent** such as rioplatense. I could not verify any syllabus or results claim.

The most informative real case is a large brand, Cimed (Brazil). It made its synthetic spokesperson "Sônia" with Veo 3, then **replaced the AI-generated voice with professional dubbing**. That fits the post-production voice-lock approach in note 03.

### Cited Findings
**Hotmart offers (Spanish and Portuguese info-product market; this is the kind of offer the client's niche advertises on Meta)**
- **"Método VEO3 Viral"** (RFA Digital, ES) advertises step-by-step video lessons, "IA gratis durante 15 meses", a lesson on creating an influencer with Veo 3, and a "generador de prompts virales". — [Hotmart (search summary)](https://hotmart.com/es/marketplace/productos/metodo-veo3-viral/E100889392V)
- **"Curso Voe com Veo 3"** (PT) promises "Como estruturar os prompts para manter a consistência dos personagens". — [Hotmart (search summary)](https://hotmart.com/pt-br/marketplace/produtos/curso-voe-com-veo-3/V102334286X)
- **"Domina VEO 3"** (LouisEditorial, ES) targets "principiantes como para creadores de contenido, emprendedores y profesionales del marketing". — [Hotmart (search summary)](https://hotmart.com/es/marketplace/productos/domina-veo-3/T101598459T)
- **"Visual IA"** (Gigi Toneatti, ES) is a mini-course on "generación de videos con herramientas como VEO 3 y Gemini". — [Hotmart (search summary)](https://hotmart.com/es/marketplace/productos/visual-ai/Y100343734K)
- Other offers: "VEO3 Na Pratica" (PT) and "Curso VEO3: Potencia tu presencia en redes sociales con videos de IA". No syllabus or reviews were retrievable for either. — [Hotmart (search summary)](https://hotmart.com/pt-br/marketplace/produtos/veo3-na-pratica/O100171869C); [pay.hotmart (search summary)](https://pay.hotmart.com/T102275531I)

**Udemy courses**
- **"Veo3: Crea Videos con IA desde Cero"** (ES), updated July 2026, includes a lesson "Cómo crear anuncios impactantes con inteligencia artificial" (4:08). — [Udemy (search summary)](https://www.udemy.com/course/veo3-video/)
- **"Veo 3 Dominio Total: De Principiante a Experto en 2026"** (ES) offers "150+ plantillas" by level, covering prompt engineering, audio and Flow. — [Udemy (search summary)](https://www.udemy.com/course/veo-3-dominio-total-principiante-a-experto/)
- **"Google Veo 3.1 Complete Mastery"** (EN) has a UGC-ads module built on **hook → problem → solution → CTA**. — [Udemy (search summary)](https://www.udemy.com/course/google-veo-complete-mastery-from-text-to-cinema/)
- **"Google Veo 3.1 – AI Generates Real Videos with Prompts 2026"** (EN) has lessons on one-shot ads and on writing better ad prompts. — [Udemy (search summary)](https://www.udemy.com/course/google-veo3/)
- **"Veo 3 Mastery Course"** (EN) has a prompt library for product ads, viral marketing and social. Its value and results claims are unverified marketing copy. — [Udemy (search summary)](https://www.udemy.com/course/veo-3-mastery/)
- **"VEO 3 Mastery – AI consistent characters, UGC ads, AI films"** covers JSON prompts, character consistency and UGC ads. It is rated 4.7 from 9 ratings, has 28 students, was updated Dec 2025, and is in Hindi **[>6 mo]**. — [Udemy (search summary)](https://www.udemy.com/course/veo-3-mastery-ai-consistent-characters-ugc-ads-ai-films/)
- **Diego Galvão's Udemy course** teaches Veo 3 through Google Flow, prompt writing, and "consistent characters and voices with ChatGPT and ElevenLabs". It is 1h20 long and was updated Oct 2025 **[>6 mo]**. — [Udemy (search summary)](https://www.udemy.com/course/dgikaos1/)

**Gumroad prompt packs (low-ticket)**
- A street-interview prompt "vault" sells for $8.88. It claims "250,000+ views and 30,000+ likes", which is self-reported and unverified. The search summary did not say which of the two listings below is the $8.88 one. — [Gumroad listing A (search summary)](https://thedailysatan.gumroad.com/l/uglsu); [Gumroad listing B (search summary)](https://riukster.gumroad.com/l/odyjme)
- A free "JSON prompt pack" for fashion and aesthetic ads, made for Veo 3. It has no Spanish or UGC-avatar content. — [Gumroad (search summary)](https://fashsplash.gumroad.com/l/jsonprompts)
- A paid pack of "50+ cinematic prompts" focused on film and product shots, not testimonials. — [Gumroad (search summary)](https://thinkaiprompt.gumroad.com/l/jkhvch)
- A Veo 3 guide product. — [Gumroad (search summary)](https://digitechdojox.gumroad.com/l/veo3guide)
- **No Spanish or Latino-accent UGC prompt pack was found**: "Ese paquete exacto no aparece en los resultados… ninguno es un pack de prompts para UGC en español con acento latino." — [search summary over Gumroad, Synthesys, Workana and others](https://help.synthesys.io/article/342-ugc-veo-sora)
- A LatAm freelance job post asks for an "Editor creativo experto en IA Veo 3 para videos UGC de marca de moda". This signals demand; I saw only the title. — [Workana (search summary)](https://www.workana.com/job/editor-creativo-experto-en-ia-veo-3-para-videos-ugc-de-marca-de-moda)

**SaaS "UGC builders" that wrap Veo, and what their controls reveal**
- **Higgsfield UGC Builder** puts **voice type, emotion, language and accent** in a separate audio-settings panel. The accent list "adjusts automatically to the uploaded image". — [Higgsfield UGC Builder guide (search summary)](https://higgsfield-ai.notion.site/ugc-builder-guide); [Higgsfield UGC Factory post, Sept 3 2025 (search summary) [>6 mo]](https://higgsfield.ai/posts/4Mh0pmSl3kqvd5OpNw1Ie2)
- **Synthesys** UGC lets you choose Veo 3, WAN 2.5 or Sora 2, then pick an actor or upload a product. Gender cannot be selected manually, so it **must be stated in the script**. — [Synthesys help (search summary)](https://help.synthesys.io/article/342-ugc-veo-sora)
- **UlazAI** has a UGC-ads page built on Veo 3, with example prompts that state the aspect ratio, the 8 s duration and the camera type. **HeyGen** sells UGC avatars in 175+ languages, with a focus on A/B testing scripts. — [UlazAI AI UGC Ads (search summary)](https://ulazai.com/ai-ugc-ads/); [HeyGen UGC avatars (search summary)](https://www.heygen.com/pt-br/avatars/ugc)

**Real brand cases, from Google's own customer list (read directly) and press**
- Google's list: "Cimed uses Veo 3 via Gemini Enterprise Agent Platform to create 'Sônia', an AI-generated character who stars in the Lavitan Night campaign." — [Google Cloud, 101 real-world gen AI use cases (read directly)](https://cloud.google.com/transform/101-real-world-generative-ai-use-cases-from-industry-leaders)
- Sônia's persona came from a consumer survey: most sleep complaints came from women around 34, class B. The campaign has two phases: she struggles to switch off at night, then she shares her results. It launched around **2025-09-19** **[>6 mo]**. — [acontecendoaqui.com.br (search summary)](https://acontecendoaqui.com.br/propaganda/lavitan-estreia-campanha-com-o-uso-de-inteligencia-artificial/)
- **Cimed replaced the AI-generated voice with professional dubbing.** — [V4 Company blog, dated June 2026 (search summary)](https://v4company.com/blog/cimed/cimed-ia-sonia-para-divulgar-suplemento)
- Other Veo ad users on Google's list:
  - LATAM Airlines: "Veo-powered marketing videos produced up to 95% faster at 99% lower cost";
  - Kraft Heinz: "speeding up campaign creations from eight weeks to eight hours";
  - RTL Deutschland: "Project Octopus … generates personalized video ad content";
  - Scorpion: "uses Google's Veo AI to scale video ad production".

  All of these are vendor-reported. — [Google Cloud, 101 use cases (read directly)](https://cloud.google.com/transform/101-real-world-generative-ai-use-cases-from-industry-leaders)
- A Brazilian tech outlet headlines "Marisa Maiô" as "the first AI character to win an advertising contract (OLX and Magalu)". I saw only the headline. — [Showmetech (search result title)](https://www.showmetech.com.br/quem-e-marisa-maio-personagem-criada-por-ia/)

### Inferences
- The courses and packs the client's niche promotes on Meta mostly repackage Google's public guidance: 5-part formula, repeated character description, timestamps, JSON. There is no evidence that they hold a proprietary, validated method. **Their claims should not outrank Google's official notes (02/04/05) in the SOP.**
- The SaaS builders give **accent, voice and emotion separate controls next to the visual**. The Cimed case shows a major brand **putting a human or fixed voice over Veo visuals**. Both support the SOP decision: state the accent in the prompt, but **lock the voice in post-production** with STS or dubbing (see note 03 for DubVoice and ElevenLabs).
- Spanish-language low-ticket offers sell "influencer IA" and "prompts virales". The client could differentiate on **identity and voice consistency across clips**, the problem these offers say least about.

### Gaps
- No direct Meta Ad Library or TikTok Creative Center data: no ad counts, run lengths, ad copy or creatives. A human should run the Ad Library manually with keywords such as "Veo 3", "prompts Veo", "UGC con IA", "avatar IA", "curso Veo 3", "anuncios con IA" and "vídeos com IA", in AR/MX/ES/BR. The client's `keywords-ads-library` skill can generate the keyword combos.
- No course syllabus, student results or refund data could be verified, and no Argentina-specific Veo course was found.
- Cimed's campaign performance results were not found.

---

## Q2. Viral Veo prompt formats (JSON, street interview, selfie vlog, ASMR, podcast) and the full text of the best ones from GitHub collections

### Takeaway
Practitioner prompt lore has gone through three generations, and parts of it contradict each other:
1. **Mid-2025 viral tricks** (snubroot v2, July 2025): "(thats where the camera is)", **colon instead of quotes** to avoid subtitles, and the "A selfie video of…" formula.
2. **Mid-2025 JSON "brand assembly" prompts** copied from viral X posts (kaymen99, July 2025).
3. **2026 beat-timed prose with "fidelity guard" sentences** (LichAmnesia, June 2026). In this generation snubroot v3 (Jan 2026) **deprecated the camera trick and switched dialogue to quotes**.

For the client, the useful, still-valid patterns are:
- the **single-speaker selfie or testimonial** skeleton;
- **2-second beat timing** within 8 s;
- explicit **identity and product "fidelity guard"** sentences;
- negatives for text and subtitles.

The quote vs. colon question remains **unsettled** and should be A/B tested on Lite (Google's own docs disagree too; see note 02).

### Cited Findings
**A. snubroot "Veo 3 Meta Framework": the most-copied practitioner guide, two versions**
- **v3.0, "Updated for Veo 3.1 / Flow", January 2026.** Verbatim migration notes:
  - "**BREAKING**: The '(thats where the camera is)' camera positioning syntax is deprecated; use standard cinematography terms instead"
  - "**UPDATE**: Dialogue now uses quotation marks with 'says:' format (e.g., `The character says: "dialogue"`)"
  - "Simplified Dialogue Syntax: … (colon format no longer required for subtitle prevention)"

  — [snubroot/Veo-3-Meta-Framework README, commit 2026-01-23](https://github.com/snubroot/Veo-3-Meta-Framework/blob/main/README.md)
- **v2 (July 25, 2025) [>6 mo]**, the version most 2025 courses copied. Verbatim:
  - "**Key Technique**: Veo 3 requires explicit camera positioning using the '(thats where the camera is)' syntax"
  - "✅ EFFECTIVE - Colon Format (Prevents Subtitles)" vs "❌ PROBLEMATIC - Direct Quote Format (Causes Subtitles)"

  — [snubroot README @59c2e07](https://github.com/snubroot/Veo-3-Meta-Framework/blob/59c2e07/README.md)
- v2's **selfie formula** (verbatim, [>6 mo]): `"A selfie video of [CHARACTER]..." + "holds the camera at arm's length" + "His/her [body part] arm is clearly visible in the frame" + "occasionally looking into the camera before [ACTION]" + "The image is slightly grainy, looks very film-like"`. — [snubroot README @59c2e07](https://github.com/snubroot/Veo-3-Meta-Framework/blob/59c2e07/README.md)
- v2's **selfie template** (verbatim, [>6 mo]): `A selfie video of a [CHARACTER_DESCRIPTION] exploring [LOCATION]. [He/She] is wearing [CLOTHING] and has [EMOTION] in [his/her] eyes. [LIGHTING_DESCRIPTION]. [He/She] is [ACTIVITY] while talking, occasionally looking into the camera before [SPECIFIC_ACTION]. The image is slightly grainy, looks very film-like. [He/She] speaks in a [ACCENT] and says: "[DIALOGUE_8_SECONDS_MAX]" [He/She] ends with [GESTURE].` — [snubroot README @59c2e07](https://github.com/snubroot/Veo-3-Meta-Framework/blob/59c2e07/README.md)
- v3 **Character Consistency Template** (verbatim): `[NAME/ROLE], a [AGE] [ETHNICITY] [GENDER] with [HAIR_DETAILS], [EYE_COLOR] eyes, [FACIAL_FEATURES], [BUILD], wearing [CLOTHING], with [POSTURE/MANNERISMS], [EMOTIONAL_STATE]`. Its rules: "**Identical Descriptions**: Use exact same wording across all prompts in a series", "**Wardrobe Lock**", "**Pose Similarity**", "**Aspect Ratio Lock**: Don't switch between 16:9 and 9:16 mid-project". v2's template also included `[VOICE_CHARACTERISTICS]` at the end. — [snubroot README (v3)](https://github.com/snubroot/Veo-3-Meta-Framework/blob/main/README.md); [v2](https://github.com/snubroot/Veo-3-Meta-Framework/blob/59c2e07/README.md)
- v3 **known limitations** (verbatim): "Character identity can drift across shots without consistent reference images"; "Exact lip-sync is not guaranteed; plan for VO alignment in post"; "Native audio may need replacement for brand work or precise dialogue". — [snubroot README (v3)](https://github.com/snubroot/Veo-3-Meta-Framework/blob/main/README.md)
- v3 **troubleshooting** (verbatim): "Repeated artifacts | Seed stuck; over-constrained | Change seed; reduce adjectives; adjust one variable"; "Move one variable at a time - Adjust camera OR lighting, not both"; "Keep language plain - Replace poetic metaphors with visual specifics". — [snubroot README (v3)](https://github.com/snubroot/Veo-3-Meta-Framework/blob/main/README.md)
- v3 **QC negative list** (verbatim): `subtitles, captions, watermark, text overlays, words on screen, logo, blurry footage, low resolution, artifacts, distorted hands, compression noise, camera shake`. Note that "camera shake" conflicts with the handheld-UGC look. For UGC, drop it. — [snubroot README (v3)](https://github.com/snubroot/Veo-3-Meta-Framework/blob/main/README.md)

**B. kaymen99/viral-ai-vids: an LLM meta-prompt for "selfie found-footage" clips, plus JSON ad prompts (July 2025) [>6 mo]**
- The selfie-clip meta-prompt (verbatim excerpts):
  - "You are an AI agent that writes hyper-realistic, cinematic video prompts for Google VEO3. Each prompt should describe a short, vivid selfie-style video clip featuring one unnamed character speaking or acting in a specific moment … like found footage or documentary-style film."
  - Rules: "Single paragraph only, 750–1500 characters. No line breaks or headings." / "Only one human character. Never give them a name." / "Include one spoken line of dialogue and describe how it's delivered." / "Character must do something physical, even if subtle (e.g. glance, smirk, pan camera)." / "Always include the five key technical elements: Time of Day, Lens, Film Stock, Audio, and Background." / "Don't describe subtitles or on-screen text."

  — [viral-video-generation/prompts.py](https://github.com/kaymen99/viral-ai-vids/blob/main/viral-video-generation/prompts.py)
- Required fill-in skeleton (verbatim): `- **Main character:** … - **They say:** [one line of dialogue] - **They** [physical action or subtle camera movement] - **Time of Day:** … - **Lens:** … - **Audio:** (implied) [ambient sounds] - **Background:** …`. — [prompts.py](https://github.com/kaymen99/viral-ai-vids/blob/main/viral-video-generation/prompts.py)
- **JSON ad prompts** copied from viral X posts (IKEA, Amazon, Nike, Tesla and others, July 2025). They use a `"timeline"` array of beats (`"timestamp": "00:00-00:01"`, `"action"`, `"audio"`), `"camera_setup": "A single, fixed, wide-angle shot. The camera does not move for the entire 8-second duration."`, and `"negative_prompts": ["no people", "no text overlays", "no distracting music"]`. The Nike example embeds a `"lip_sync_line"` and a `"voiceover": {"delivery": "confident, clean baritone, slightly reverbed"}` block. — [video-ads-generation/prompts.py](https://github.com/kaymen99/viral-ai-vids/blob/main/video-ads-generation/prompts.py)
- The repo's own claims: "Under $0.60 per marketing video using VEO3" and "~$0.32 per 8-second viral video via Kie.ai". Kie.ai is a third-party reseller, and these are 2025 prices. — [kaymen99 README](https://github.com/kaymen99/viral-ai-vids/blob/main/README.md)

**C. LichAmnesia/awesome-ad-video-prompts: 52 ad prompts, last commit 2026-06-15**
- The repo is the "open-source craft companion" to the vendor HeyDreaming. It is **multi-model** (Seedance 2.0, Veo 3, Kling, Runway); one UGC prompt runs 10 s, which Veo does not support.
- Its key claim: "Keep the multi-beat timing and the 'no deformation/drift/artifacts' fidelity guard — they materially improve output." This is **unverified vendor opinion**.
- Its other advice: "avoid baking in text overlays (add captions in post)".

  — [awesome-ad-video-prompts README](https://github.com/LichAmnesia/awesome-ad-video-prompts/blob/main/README.md)
- Its best UGC testimonial prompt, **"Bathroom Mirror Skincare Truth"** (6 s, 9:16), verbatim: `Handheld phone selfie shot into a slightly steamed bathroom mirror, woman early-30s in an oversized tee, dewy bare skin, no makeup. 0-2s: she leans toward the glass and taps the [brand] serum bottle against the camera, half-laughing mid-sentence. 2-4s: micro-zoom in as she presses two drops onto her cheekbone, fingertips spreading in small circles, window light catching the sheen. 4-6s: she turns her face slowly side to side, raising one eyebrow at her own reflection, caught genuinely off guard. Warm morning window light, soft skin texture with visible pores, faint water droplets streaking the mirror. Face shape and skin finish stay consistent across beats, no deformation, drift, or artifacts. Implied sound: muffled running tap, a quiet 'okay... wow.'` — [README](https://github.com/LichAmnesia/awesome-ad-video-prompts/blob/main/README.md)
- **"Car Vlog Supplement Confession"** (written as 10 s; for Veo, shorten to 8 s), verbatim: `Phone clamped to a car dashboard, 28-year-old man in the driver's seat of a parked car in a sunny lot, vlog-style confession, [brand] supplement bottle in the cupholder. 0-2s: he flicks a glance at the lens and rattles the bottle, 'thirty days, real talk.' 2-4s: he holds two capsules in his open palm to camera under dappled windshield light, then dry-swallows with a swig from a water bottle. 4-7s: he talks with his hands, counting points off his fingers, animated and genuinely energized. 7-10s: he leans in close and drops his voice like he's letting you in on a secret, a knowing smirk. Natural through-windshield light with moving leaf shadows, realistic skin and fabric texture. Bottle keeps consistent label, cap, and shape, no deformation, drift, or artifacts. Implied sound: muffled cabin hum, a soft capsule rattle.` — [README](https://github.com/LichAmnesia/awesome-ad-video-prompts/blob/main/README.md)
- **Identity guard phrase** from the "Glow-Up Transformation" prompt: "no morphing of the face into a different person, no deformation, drift, or artifacts". Other UGC formats in the collection: POV skincare, green-screen spec reveal, "this or that" split-screen, expectation vs. reality, unboxing on stairs, try-on street spin. — [README](https://github.com/LichAmnesia/awesome-ad-video-prompts/blob/main/README.md)

**D. Street interview, podcast, ASMR and JSON (practitioner pages behind the proxy)**
- **Street interview.** Creator templates describe a "high-energy, vertical, smartphone-style interview". A confident interviewer approaches a pedestrian in a busy public spot with a playful or provocative question, and the mic is "clearly visible and near the speaker". The format is used for opinion-based comedy, where unexpected answers drive shares. — [rpn.beehiiv "How to go Viral with Veo 3" (search summary)](https://rpn.beehiiv.com/p/how-to-go-viral-with-veo-3); [Avocado AI guide on Notion (search summary)](https://avocado-ai-guides.notion.site/The-Ultimate-Guide-to-Crafting-Viral-Videos-with-Veo-3-A-Blueprint-for-Success-2307b2ce31d08086ac02f077491cc408); [Filmora ES "ai street interview" (search summary)](https://filmora.wondershare.es/ai-prompt/ai-street-interview.html)
- **Podcast (two speakers).** A hands-on Veo 3.1 tutorial, dated by its article ID to about **2025-12-23**, says to **keep the camera fixed** and to specify **who speaks, in what tone, and when the reaction lands**. It reports that turn-taking worked "without many regenerations". This is a single anecdote. — [PicLumen hub article (search summary)](https://www.piclumen.com/es/hub/article/how-i-made-a-talking-pet-podcast-video-with-veo-31-694a298b3a774b1e8bdf9b0e/?from=home)
- A Vietnamese 2026 guide argues that multi-speaker dialogue "needs its own prompting discipline": who speaks when, distinct voices, lip-sync, and chaining clips past 8 s. — [veo3ai.io two-character dialogue guide 2026 (search summary)](https://www.veo3ai.io/vi/blog/veo-3-two-character-dialogue-guide-2026)
- **ASMR.** In practitioner prompts it is an audio-bed instruction, not a separate mode. Example (verbatim): "A cascade of satisfying, fast-paced ASMR sounds: whirring, clicking, wood snapping into place." — [kaymen99 video-ads-generation/prompts.py](https://github.com/kaymen99/viral-ai-vids/blob/main/video-ads-generation/prompts.py)
- **JSON.** A practitioner Substack claims JSON organizes scene, character, camera and audio per second, helps continuity between takes, and should be **syntax-validated before generating**. — [livebreatheseo Substack (search summary)](https://livebreatheseo.substack.com/p/how-i-use-json-to-actually-control). Google's own V-Start tool includes a blind "JSON vs Plain Text" study but publishes no result, and Google's meta-prompts output plain prose (see note 02). — [V-Start eval.js](https://github.com/GoogleCloudPlatform/generative-ai/blob/main/vision/sample-apps/V-Start/src/features/eval.js)
- **Prompt length.** One guide claims "Google Cloud's official recommendation is to keep prompts around 10–25 words". I found no official source for this, and it conflicts with kaymen99's 750–1,500 characters and with Google's own long sample prompts. — [BetterLink/eastondev (search summary)](https://eastondev.com/blog/en/posts/dev/20251204-veo3-prompt-writing-guide)

### Inferences
- **Do not import 2025 tricks into the SOP as rules.** "(thats where the camera is)" has been deprecated by its own author, and the "colon prevents subtitles" belief has been reversed by its own author while Google's docs still disagree on it. Fix subtitles with `negativePrompt: "subtitles, captions, text overlays, words on screen"` plus an A/B test of colon vs. quotes on Lite at fixed seed.
- The kaymen99 rules ("one human character", "one spoken line", "describe how it's delivered", "do something physical") and the LichAmnesia **2-second beats + fidelity guard** pattern fit the client's single-avatar 8 s testimonial clips well. They are the most transferable practitioner patterns.
- **Do not copy brand-assembly JSON prompts that use third-party trademarks** (IKEA, Nike, Louis Vuitton, etc.). Use only the client's own brands.
- Practitioner-derived template for Veo 3.1 Lite. It is image-to-video from the approved avatar still, Spanish rioplatense, one speaker. It assembles the cited patterns and is **untested**; validate it by A/B test:
  ```
  Vertical 9:16 handheld smartphone selfie video at arm's length, natural slight hand sway, eye-level. [CHARACTER BIBLE — verbatim, identical in every clip]. She is sitting in the driver's seat of her parked car on a sunny afternoon, phone on the dashboard. 0-2s: she glances at the lens and lifts the [product] to camera. 2-6s: she talks with her hands, relaxed and genuine, natural blinks and small head tilts. 6-8s: she leans in slightly with a knowing half-smile. Natural light through the windshield with soft moving leaf shadows, realistic skin texture with visible pores, no beauty filter. Her face shape, hairline, eye color and skin finish stay identical throughout; no morphing into a different person, no drift, no artifacts. She speaks Argentine Rioplatense Spanish from Buenos Aires, warm mid-pitch voice, casual pace, and says: "Che, te juro que probé de todo… y esto es lo único que me funcionó." Audio: quiet car cabin hum, faint street traffic outside. No music.
  negativePrompt: subtitles, captions, text overlays, words on screen, watermark, extra people, distorted hands, plastic skin, beauty filter
  ```

### Gaps
- The repository the user called "awesome-veo3-prompts" could not be identified, because GitHub search is blocked and no guessed name resolved.
- The full text of the best-selling street-interview and podcast prompt packs is behind Gumroad or blocked pages.
- There is no controlled evidence that JSON, the fidelity-guard sentence, or quote vs. colon changes Veo 3.1 Lite output.

---

## Q3. What top AI-UGC agencies and creators (EN/ES/PT) say works for realism, voice consistency, accent and multi-clip ads, and the common beginner mistakes

### Takeaway
Practitioners converge on six points:
1. **One fixed visual anchor** (the same reference or first-frame image) plus a **word-for-word repeated bible** for character, wardrobe, room and light.
2. **Short, self-contained clips**: one speaker, one line, about 2–3 words per second.
3. A **voice and accent description in every prompt**.
4. Above all, **re-voicing the whole edit with one fixed voice in post** (ElevenLabs Voice Changer or professional dubbing), because native Veo voices drift.
5. Realism comes from **phone-camera language and imperfections**, not "cinematic" adjectives.
6. Packaging text, spoken claims and extensions need **manual QC**.

None of the practitioner material includes Argentine-accent tests.

### Cited Findings
- **Voice-lock workflow, creator consensus.** A creator's Veo 3 tutorial (TikTok, dated by its ID to about **2025-08-11** **[>6 mo]**) gives three steps:
  1. "Always include a short voice and accent description in your prompt. You want the voice to change slightly if needed, but not the accent."
  2. Assemble the clips in CapCut and export the vocals or the full video.
  3. "Head to ElevenLabs. Select the voice changer, choose the voice you want for your character, drop in your complete vocal track … This ensures every clip has the exact same voice."

  — [TikTok @ai.for.real.life (search summary)](https://www.tiktok.com/@ai.for.real.life/video/7537477893442538766)
- Courses teach the same pairing: "consistent characters and voices with ChatGPT and ElevenLabs" **[>6 mo]**. — [Udemy, Diego Galvão (search summary)](https://www.udemy.com/course/dgikaos1/)
- The brand case: Cimed **replaced the Veo-generated voice of "Sônia" with professional dubbing**. — [V4 Company (search summary)](https://v4company.com/blog/cimed/cimed-ia-sonia-para-divulgar-suplemento)
- **Multi-clip continuity.** The cluster of 2026 vendor and creator guides below says the following. Per-claim attribution within the cluster was not resolved.
  - "The hard part of multi-clip Veo is continuity. Reuse the same reference image, repeat the wardrobe, room and lighting description word for word across clips, and keep the same aspect ratio."
  - "Save exact character descriptions … and copy-paste identical details across prompts."
  - Script "roughly 2 to 3 words per second", and "generate each line as its own clip and stitch them, or use clip extension".
  - A ~30 s UGC structure: **hook → product demo → proof → CTA**, keeping the same person and room across clips.
  - "Watch for dialogue leaking into an extension or changing between versions. Forum users have specifically reported dialogue and continuity problems when extending generated clips."

  — [vo3ai.com TikTok UGC workflow 2026-08-31 (search summary)](https://www.vo3ai.com/blog/tiktok-ugc-ads-tested-workflow-for-viral-consistency-with-vo3-ai-2026-2026-08-31); [vo3ai.com storyboard-to-ad 2026-07-07 (search summary)](https://www.vo3ai.com/blog/tested-tiktok-ugc-video-in-vo3-aistoryboard-to-ad-workflow-goes-viral-2026-07-07); [zeely.ai Veo 3.1 for video ads (search summary)](https://zeely.ai/blog/how-veo-3-1-works-for-video-advertising/); [ugcvids.ai Veo 3.1 product-ad prompts (search summary)](https://ugcvids.ai/blog/how-to-write-veo-3-1-prompts-for-product-ads); [veo3ai.io TTS/voiceover guide 2026 (search summary)](https://www.veo3ai.io/blog/veo-3-text-to-speech-voiceover-guide-2026)
- **Realism and mistakes,** from the same cluster: generic prompts give bland, obviously-AI results, so "describe camera movement, shooting style, and micro-details". "Reference images raise the odds of consistency, but they do not create a legal lock on every logo, label, color, or face." "Packaging text … model-generated labels warp and mis-spell." "Check every spoken claim against the landing page." Avoid drastic outfit or background changes between clips. — [ugcvids.ai (search summary)](https://ugcvids.ai/blog/how-to-write-veo-3-1-prompts-for-product-ads); [imagine.art UGC ads (search summary)](https://www.imagine.art/blogs/how-to-make-ugc-ads-with-ai); [godofprompt Veo 3 guide (search summary)](https://godofprompt.ai/blog/guide-to-veo-3-tutorial/); [veotutorials Substack (search summary)](https://veotutorials.substack.com/p/7-ways-to-get-better-results-with)
- **Veo has "no character memory".** Each generation can produce a different look, so the character block must repeat identically in every prompt. "If the lip movements don't match the speech, the ad looks artificial." — [search summary over Higgsfield/UlazAI/livebreatheseo pages](https://ulazai.com/nl/character-consistency/)
- **Realism vocabulary in the 2026 collection:** "dewy bare skin, no makeup", "soft skin texture with visible pores", "slight handheld shake", "realistic skin and fabric texture", "caught genuinely off guard", "half-laughing mid-sentence", "talks with his hands". — [LichAmnesia README](https://github.com/LichAmnesia/awesome-ad-video-prompts/blob/main/README.md)
- **Older realism fixes [>6 mo], unverified:** "Add 'natural movement'", "realistic physics governing all actions", "authentic human behavior patterns", "fluid, lifelike motion". For audio hallucinations: "Always specify expected background audio environment" and "Include 'no unwanted background music' in negative prompts". — [snubroot v2 @59c2e07](https://github.com/snubroot/Veo-3-Meta-Framework/blob/59c2e07/README.md)
- **Duration vs. complexity:** "Complex multi-action scenes may fragment; use one major action per shot". "Use 4-6s for complex action; 8s for atmospheric shots". — [snubroot v3](https://github.com/snubroot/Veo-3-Meta-Framework/blob/main/README.md)
- **Gender and voice must be explicit in the script** (Synthesys UGC on Veo/Sora/WAN). — [Synthesys help (search summary)](https://help.synthesys.io/article/342-ugc-veo-sora)
- **Accent.** I found no practitioner source showing a reliable *Argentine* accent from Veo. One source claims Veo 3 "admite doblaje en más de 40 idiomas" with a Vietnamese example; this is weak and unverified. — [search summary citing Synthesys/Promptus](https://www.promptus.ai/blog/google-veo-3-ai-video-generation-tool)

**Beginner-mistake list (practitioner consensus across the sources above):**
1. Re-describing the character differently in each clip.
2. Changing aspect ratio or wardrobe between clips.
3. Several actions or several speakers in one 8 s clip.
4. Overlong dialogue, which comes out rushed or cut off.
5. Trusting native audio for brand claims or voice continuity.
6. Letting the model render text or labels.
7. Changing several variables per iteration.
8. Staying on a "stuck" seed.
9. Using "cinematic" adjectives instead of phone-camera specifics.
10. Expecting extensions to keep dialogue intact.

— [snubroot v3](https://github.com/snubroot/Veo-3-Meta-Framework/blob/main/README.md); [ugcvids.ai (search summary)](https://ugcvids.ai/blog/how-to-write-veo-3-1-prompts-for-product-ads); [vo3ai.com (search summary)](https://www.vo3ai.com/blog/tiktok-ugc-ads-tested-workflow-for-viral-consistency-with-vo3-ai-2026-2026-08-31)

### Inferences
- Practitioner consensus and Google's official material (notes 02/04/05) agree. The SOP can state with confidence: **fixed first-frame image + verbatim bible + one speaker per clip + voice fixed in post**.
- Much practitioner advice assumes **Ingredients or reference images**. These are **not available on Veo 3.1 Lite**. On Lite, the "same reference image" advice becomes **image-to-video from the same approved still for every clip** (re-anchoring, not chaining). For shots that truly need reference images, escalate to Veo 3.1 Fast (see notes 01/04).
- The "voice may vary slightly but the accent must not" framing suits the client. Put the accent cue and **dialect-written lines** (voseo, "che", local vocabulary) in the prompt to get Argentine prosody and lip motion. Then **lock timbre and accent in post** with a fixed rioplatense voice via STS or DubVoice, the same move Cimed made with human dubbing.

### Gaps
- Agencies known for AI UGC (Arcads, Creatify, HeyGen, Higgsfield) do not publish their internal Veo prompts. Only product UIs and marketing claims were visible.
- No practitioner A/B data on accent adherence, voice drift rates or identity drift on Veo 3.1 Lite specifically. Most practitioner evidence is Veo 3/3.1 from 2025.
- Reddit and X threads, where many Veo tips circulate, were blocked. I did not use them.

---

## Q4. What ad-performance and creative-strategy sources say about AI-UGC video ads in 2026, and platform and regulatory compliance for AI-generated people in ads (facts only)

### Takeaway
**Performance.** 2026 creative-strategy content, almost all vendor- or agency-authored, agrees on four points:
- the **first ~3 s decide the ad**: a 3-second hold rate above roughly 25–30% is strong, below 20% is a hook problem;
- test **3–5 hook variants per concept**, changing only the opening;
- use the **hook → problem/demo → proof → CTA** structure;
- keep ads short: Google's own ad-agent sample budgets **12–24 s from three 4/6/8 s Veo shots**.

I found no independent benchmark separating AI UGC from human UGC.

**Compliance.**
- **Meta** applies an "AI info" label, and secondary sources say photorealistic AI people need disclosure.
- **TikTok** reportedly made disclosure of realistic AI ad creative mandatory in July 2026. This is secondary-source only.
- **US FTC:** the rule on fake reviews (16 CFR Part 465, in force since Oct 2024) explicitly covers **AI-generated testimonials**.
- **EU AI Act Art. 50** deepfake transparency applies from **2026-08-02**. This matters for Spain.

### Cited Findings
**Performance and creative strategy (vendor sources; directional only)**
- Hook benchmarks from a 2026 vendor and agency cluster (per-claim attribution not resolved):
  - "Three-second hold rate is the primary hook metric. A hold rate above 30% is strong. Below 20% … the hook is actively losing the audience";
  - "25-40% is strong for Meta prospecting. Below 20% signals a hook problem — not a targeting or budget problem";
  - categorize openers "problem-first, result-first, curiosity-first, controversy-first";
  - "test 3-5 hook variations per concept";
  - "A high hold rate with a low watch-through rate usually means the hook created a curiosity gap the ad didn't fill".

  — [Pixis, UGC in 2026 (search summary)](https://pixis.ai/blog/ugc-in-2026-whats-working-whats-stale-and-how-to-refresh-your-hook-library/); [adlibrary.com UGC ads guide (search summary)](https://adlibrary.com/posts/ugc-ads-guide); [Launchpoint, AI UGC hooks July 2026 (search summary)](https://www.launchpointhq.com/blog/ugc-ai-content-insights-hooks-creators-performance); [Magic Hour UGC-style ads 2026 (search summary)](https://magichour.ai/blog/how-to-make-ugc-style-video-ads); [Hawky UGC ads 2026 (search summary)](https://hawky.ai/blog/ugc-ads)
- Widely repeated, **unverified** stats: "10.38x conversion lift for UGC posts" (attributed to Emplifi Q3 2025) and "35% higher watch-through for UGC video ads". Also a vendor claim that AI-UGC gets "comparable or better click-through rates at significantly lower cost per creative", mainly through faster hook testing. — [search summary over vidmuse.ai, futurefactors.ai, novapixeldev.com](https://vidmuse.ai/blog/ai-ugc); [futurefactors.ai](https://futurefactors.ai/ai-ugc-ads-2026-guide/); [novapixeldev.com](https://novapixeldev.com/blog/ai-generated-ugc-ads-2026-what-actually-works)
- Practitioner guide, "Marketing & Social Media" section: "Hook within first 2 seconds". Its "Vertical Social Teaser (9:16)" playbook: "3-4 clips at 4-6s each", "720p for iteration, 1080p final", "Keep text-safe zones for captions". — [snubroot v3](https://github.com/snubroot/Veo-3-Meta-Framework/blob/main/README.md)
- **Google's official ADK "ad-creative-director" sample**, updated 2026-10-24:
  - "Each shot becomes a Veo-3 clip, and Veo-3 supports clip durations of **only 4, 6, or 8 seconds**. So 3 shots × {4,6,8}s = **12–24 seconds** of distinct hero footage — squarely a short-form / bumper ad";
  - the pipeline makes "a still and a motion clip for each hero shot, a music bed, a voiceover";
  - it asks for longer ads "plans to the ceiling and tells you rather than inventing filler shots".

  — [vertex-ai-creative-studio ad-creative-director README](https://github.com/GoogleCloudPlatform/vertex-ai-creative-studio/blob/main/experiments/mcp-genmedia/sample-agents/adk-genmedia-series/ad-creative-director/README.md)

**Meta (Facebook/Instagram)**
- Meta automatically applies an "AI info" label when advertisers use Meta's gen-AI ad features: Background Generation, Image Generation, Add Animation. Meta also uses industry-standard signals (e.g. **C2PA**) to detect content made with outside gen-AI tools. The label appears in the "About this ad" menu. — [Marketing Dive (search summary)](https://marketingdive.com/news/sociable-meta-adds-updated-disclosure-tags-for-ai-generated-ads/824833); [Social Media Today (search summary)](https://socialmediatoday.com/news/meta-adds-updated-disclosure-tags-for-ai-generated-ads/824658)
- Secondary sources say ads with **photorealistic AI-generated people** must show the AI label next to "Sponsored", and that minor edits may not trigger it. — [Common Thread Co, 2026 (search summary)](https://commonthreadco.com/blogs/coachs-corner/meta-ai-ad-labels-mandatory-disclosure-ecommerce-2026); [Cinerads (search summary)](https://www.cinerads.com/blog/ai-ugc-facebook-ad-policy)
- **Disputed:** one source calls the label "a transparency notice, not a penalty". Others claim undisclosed AI content causes "14 percent of all rejections" (early 2026) and that "a first violation kills the ad and adds a policy strike". **None of this was verified against Meta's own Business Help Center.** — [Cinerads (search summary)](https://www.cinerads.com/blog/ai-ugc-facebook-ad-policy); [Storrito (search summary)](https://storrito.com/resources/meta-rejects-14-percent-of-ads-for-undisclosed-ai-content/); [Coinis (search summary)](https://coinis.com/blog/meta-ai-content-labeling-facebook-instagram-ads-2026)

**TikTok**
- Agency blogs report a TikTok ads-policy revision around **2026-07-21** making a disclosure label **required** for realistic AI-generated ad creative. The scope reportedly covers "AI imagery, synthetic voices, or realistic digital avatars", and "a realistic AI actor delivering a script" counts. TikTok reportedly reads **C2PA Content Credentials** and auto-labels some uploads. — [Stellar Search (search summary)](https://www.stellarsearch.co.uk/insight/tiktoks-ai-ad-disclosure-rules-are-live-what-brands-running-ai-creative-need-to-do-now); [Common Thread Co (search summary)](https://commonthreadco.com/blogs/coachs-corner/tiktok-ai-ad-disclosure-rules-ecommerce-2026); [Cinerads TikTok AI policy 2026 (search summary)](https://www.cinerads.com/blog/tiktok-ai-content-policy)
- An independent news report from **March 2026** says required disclosures are often missing in practice and cites unlabeled AI-looking videos from Samsung. — [ainauten (search summary)](https://news.ainauten.com/en/story/tiktoks-policy-for-ai-ads-isnt-working)
- **Not verified** against TikTok's own Business Help Center or Newsroom, including the claimed "permanent ban for repeat violations". — [Cinerads disclosure comparison (search summary)](https://www.cinerads.com/blog/ai-ad-disclosure-requirements)

**US FTC: Rule on the Use of Consumer Reviews and Testimonials (16 CFR Part 465)**
- The final rule was announced in August 2024 and took effect in October 2024 **[>6 mo, still in force per the sources]**. It prohibits reviews and testimonials that misrepresent who wrote them, "including those generated by artificial intelligence". It bars businesses from creating, buying or disseminating them when they "knew or should have known" they were fake. — [Hunton (search summary)](https://hunton.com/hunton-retail-law-resource/ftc-issues-final-rule-targeting-fake-consumer-reviews-and-testimonials-including-those-generated-by-artificial-intelligence-ai-and-online-bots); [Davis Wright Tremaine (search summary)](https://dwt.com/insights/2024/08/ftc-finalizes-rule-banning-fake-consumer-reviews); [Search Engine Land (search summary)](https://searchengineland.com/ftc-fake-reviews-testimonials-445209)
- Civil penalties apply to knowing violators: up to **$53,088 per violation** at the 2025 inflation-adjusted level. An older figure of $51,744 reflects an earlier year. — [HotHardware (search summary)](https://hothardware.com/news/ftc-cracks-down-ai-generated-fake-reviews); [etcentric (search summary)](https://www.etcentric.org/ftc-rule-prohibiting-fake-and-paid-reviews-goes-into-effect/)

**EU AI Act Article 50 (relevant if any ads run in Spain or elsewhere in the EU)**
- Article 50 transparency obligations, including deployers having to **disclose deepfakes** (Art. 50(4)), apply from **2026-08-02**. The Digital Omnibus did **not** postpone them.
- The only relief is for **machine-readable marking** (Art. 50(2)): providers of generative systems already on the market before Aug 2, 2026 get until **2026-12-02**.
- The Commission's Article 50 guidelines were published **2026-07-20**.
- Penalty figures conflict between sources: "€35M/7%" vs. "€7.5M/1.5%".

  — [Cloud Security Alliance research note, 2026-07-29 (search summary)](https://labs.cloudsecurityalliance.org/research/csa-research-note-eu-ai-act-article-50-transparency-20260729/); [Reed Smith (search summary)](https://www.reedsmith.com/our-insights/blogs/viewpoints/102nfqg/always-read-the-label-eu-ai-transparency-rules-and-questions-that-remain-unanswe/); [Dastra (search summary)](https://www.dastra.eu/en/blog/ai-act-transparency-rules-what-changes-august-2-2026/60164)
- None of the EU sources addresses advertising specifically. Whether a fictional-avatar ad counts as a "deepfake" (content that resembles real persons or events) is not settled in what I found. — [Reed Smith (search summary)](https://www.reedsmith.com/our-insights/blogs/viewpoints/102nfqg/always-read-the-label-eu-ai-transparency-rules-and-questions-that-remain-unanswe/)

**Provenance**
- Practitioner guide: "Digital Watermarking: All videos marked with SynthID". — [snubroot v3](https://github.com/snubroot/Veo-3-Meta-Framework/blob/main/README.md). Official SynthID details are in note 01.

### Inferences
- **Creative implication.** Veo's 4/6/8 s grid fits the hook-testing workflow: **one 4–6 s hook clip with several variants**, plus a shared body and CTA built from re-anchored clips. Only the opening needs regenerating, which keeps the avatar identical in the rest of the ad. This is an inference from the hook-testing advice and the Google 3-shot budget.
- **Compliance-safe design**, facts-based and not legal advice:
  1. Keep provenance metadata (C2PA/SynthID) intact.
  2. Disclose AI use where the platform asks, and do not try to avoid labels.
  3. Do not present a synthetic avatar as a real customer reporting real results. Under the FTC rule this is the core "fake testimonial" risk, and similar consumer-protection logic is likely elsewhere.
  4. Write scripts as dramatizations or spokesperson lines.
  5. Never use real people's likeness or voice.

### Gaps
- Meta's and TikTok's own policy pages were blocked. All label and enforcement details are secondary. Verify in Meta's Business Help Center ("AI disclosure for ads") and TikTok's Ads Policy before the SOP states them as rules.
- I did not research **Argentina-specific rules** on AI in advertising or on testimonials (consumer-protection or advertising self-regulation codes). No source surfaced in this sweep. The same is true for Mexico and other LatAm markets.
- No independent, platform-published 2026 data compares AI-UGC with human UGC performance. All performance figures above are vendor-sourced.
