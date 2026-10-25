# Gap research: (A) a lighting lexicon based on real portrait photography, translated into prompts; (B) open-model realism settings (LoRAs, samplers, steps, guidance) and Midjourney V8.x recipes. State as of Oct 25, 2026

**Scope and how this complements the earlier notes**
- File 02 §4 and §8 already cover the basics:
  - OpenAI's anti-cinematic guidance;
  - the source/direction/quality/Kelvin template;
  - a 12-scene phrase bank;
  - official README defaults (Qwen 50 steps / true-CFG 4; Z-Image-Turbo 9 steps / CFG 0; FLUX.2 [klein] 4 vs 50 steps).
- File 06 already notes that lightning/turbo LoRAs give plastic skin.
- This file does not repeat those. It adds:
  - the physical signatures of each lighting setup (catchlights, shadow edges, falloff, Kelvin, speculars);
  - how to name direction and match light between subject and background;
  - which lighting phrasings make images look fake;
  - **official ComfyUI template settings extracted directly from the JSON workflow files on GitHub**, for FLUX.2 [dev], FLUX.2 [klein], **FLUX 3 Image Klein**, Qwen-Image-2.1 (+Turbo), Z-Image base/Turbo and **Krea 2 RAW/Turbo**;
  - community realism LoRAs with weights;
  - sampler/sigma tools (RES4LYF, Detail Daemon);
  - two-pass skin refinement;
  - Midjourney V8.x parameters.

**Source-access legend**
- **Fetched (GitHub):** read directly. This covers the Comfy-Org/docs and Comfy-Org/workflow_templates repos, krea-ai/krea-2, QwenLM/Qwen-Image, Jonseed/ComfyUI-Detail-Daemon and ClownsharkBatwing/RES4LYF.
- **Search summary:** Civitai, Hugging Face, Reddit, comfyui-wiki, photography sites and Midjourney docs could not be fetched (DNS/proxy blocked). Claims from those come from WebSearch result summaries and are marked as such. Treat the exact numbers in them as needing verification on the page.
- **Legacy flag:** advice from the SD1.5/SDXL/FLUX.1 era is marked **[legacy]**.

---

## 1. Which lighting phrases measurably increase realism in Nano Banana Pro / GPT Image 2 / Seedream / FLUX.2, per practitioner tests?

### Takeaway
No controlled, published A/B test isolates a lighting phrase and measures a realism gain on any of these models. The evidence is practitioner guidance plus vendor claims, and it agrees on four points:
1. **Name one motivated physical source with a direction** (e.g., "window on camera-left") instead of a style label.
2. Avoid "studio-perfect" light in scenes meant to be candid.
3. Put the light where the model will respect it. Seedream and FLUX.2 follow lighting direction literally, and Nano Banana Pro needs explicit direction and can be told to reason about light paths.
4. **Hard, direct light reveals skin texture and soft light hides it.** Krea's own official example uses "harsh, direct lighting highlights intricate skin pores", so lighting choice is also a texture-control lever.

### Cited Findings
- **No controlled tests exist.** A search for systematic light-direction tests on Nano Banana Pro found none: "none of these sources report a systematic side-by-side test of light direction… with measured results" (search summary across) — [Chase Jarvis](https://chasejarvis.com/blog/nano-banana-prompts/); [PicassoIA](https://blog.picassoia.com/prompts-that-work-well-with-nano-banana-pro); [ud.hk](https://www.ud.hk/en-US/resources/ai/nano-banana-pro-tips-2026-07-20)
- **Nano Banana Pro:**
  - It "is capable of rendering realistic human skin, eyes, and hair at high fidelity, but it needs direction on lighting, lens, and distance to get there". Its tested examples state a side ("soft diffused morning light from the left") plus "a warm backlight for rim glow" (search summary) — [PicassoIA](https://blog.picassoia.com/prompts-that-work-well-with-nano-banana-pro)
  - Named-setup phrasing in a Nano Banana guide: "Classic Rembrandt lighting. Key light at 45 degrees elevation"; commercial setup = overhead softbox + bounce cards (search summary) — [Chase Jarvis](https://chasejarvis.com/blog/nano-banana-prompts/)
  - Practitioner tip for wrong-direction shadows: enable "Thinking" mode and instruct the model to calculate light paths from the light-source position. Described as a tip, not a documented feature (search summary) — [Chase Jarvis](https://chasejarvis.com/blog/nano-banana-prompts/)
  - Changing only the described light ("soft window light" vs "hard midday sun") produces a noticeably different photo of the same subject (search summary) — [ud.hk Nano Banana Pro tips](https://www.ud.hk/en-US/resources/ai/nano-banana-pro-tips-2026-07-20)
- **Seedream 5.0 Pro:**
  - "lighting direction get[s] followed with high fidelity". The vendor argues AI images look fake because they are "too polished, with studio-perfect light even in supposedly candid shots", and that realism needs every element sharing **one coherent lighting scheme** / "one coherent camera contract per image" (vendor blog, search summary) — [Atlas Cloud Seedream 5 Pro realistic portraits](https://www.atlascloud.ai/blog/guides/seedream-5-pro-realistic-portraits)
  - Vendor review claims Seedream 5.0 executes technical phrasing like "golden hour backlighting with rim light on subject's left side" (search summary) — [Dzine Seedream 5.0 review](https://www.dzine.ai/blog/seedream-5-0-review/)
  - Krea's Seedream 5.0 Pro guide advises natural language that unites subject, setting and lighting, with the non-negotiable constraint first, because "longer prompts can bury late details" (search summary) — [Krea blog: 15 Seedream 5.0 Pro prompts](https://www.krea.ai/blog/15-powerful-seedream-5-0-pro-prompts-for-photorealism-product-shots-portraits-more)
- **GPT Image 2 vs others on skin (not lighting-specific):** a 17-model realism test found "GPT Image 2 and Nano Banana 2 produced the most convincing skin… natural pores, believable variation". Qwen Image was not among the top skin performers (search summary) — [getimg.ai AI Realism Test](https://getimg.ai/blog/ai-realism-test-comparing-realistic-image-generation-models)
- **FLUX.2 [dev]:** Comfy's official page says it delivers "up to 4MP photorealistic output with far better lighting, skin, fabric, and hand detail" and "real-world lighting behavior". This is a vendor claim, not a test (fetched GitHub) — [Comfy-Org/docs flux-2-dev.mdx](https://github.com/Comfy-Org/docs/blob/main/tutorials/flux/flux-2-dev.mdx)
- **Krea 2 official prompting guide (fetched GitHub), verbatim example prompts:**
  - "Harsh, direct lighting highlights intricate skin pores and bright golden reflections…";
  - "illuminated by soft, diffused natural lighting that highlights the intricate details of the fur";
  - "Soft, directional studio lighting highlights her facial features".

  — [krea-ai/krea-2 docs/prompting.md](https://github.com/krea-ai/krea-2/blob/main/docs/prompting.md)
- **Photography physics behind the texture lever:**
  - hard light shows more skin texture than soft light — [Fujifilm X: hard & soft light](https://fujifilm-x.com/en-us/?p=58542) (search summary);
  - hard sources give "small, pinpoint" high-contrast specular highlights, soft sources a broader "glossy sheen" — [Australian Photography: deconstruct light pt 2](https://australianphotography.com/photo-tips/how-to-deconstruct-light-part-two) (search summary).
- **Single-source naming:** a "how to make AI images look less fake" guide recommends naming one light source in the prompt so the model keeps subject and background consistent (search summary) — [MagicShot: 12 tells](https://magicshot.ai/blog/why-your-ai-images-still-look-fake-12-tells-and-how-to-kill-them)

### Inferences
- **Highest-confidence realism lever:** replace any style word with a sentence giving **source + side + height + quality + one imperfection**. Example: "light from a single window on camera-left, slightly above eye level, soft but directional, shadow side of the face falls about two stops darker, no fill." Every model above reads this kind of physical description. Seedream and FLUX.2 claim literal adherence.
- **Texture trade-off for avatars:** soft/overcast/beauty light makes skin look smoother, which reads "AI-plastic" more easily. Moderately hard, directional light (sun through a window, bare bulb, phone flash) shows pores and micro-shadows. For UGC realism, prefer **directional light with visible texture** over large frontal soft light, and choose softness only for beauty/skincare ads where smoothness is the brief.
- **Nano Banana Pro reasoning:** in Thinking mode, add one constraint such as "make every cast shadow consistent with the window on camera-left". This uses the light-path tip, and costs nothing to test.
- **Prompt upsamplers can override lighting:** FLUX 3 Klein, Qwen-Image-2.1 and Krea 2 Turbo all ship LLM prompt enhancers that are **on by default** in the Comfy templates (see §4). They can re-insert "cinematic/dramatic" vocabulary. Either disable them for lighting-critical shots, or inspect the expanded prompt. This is an inference from the default-on setting; no test of upsampler lighting drift was found.

### Gaps
- No blind, multi-seed test was found that compares, for example, "natural window light" vs "studio lighting" vs "cinematic lighting" on realism scores for Nano Banana Pro, GPT Image 2/2.5, Seedream 5 or FLUX.2. The client should run its own test: fixed seed on open models, 8+ samples per condition on closed models, and blind rating.
- GPT Image 2-specific lighting-phrase tests: none found beyond OpenAI's own guide (covered in file 02).

---

## 2. What are the physical characteristics of each lighting setup that the prompt should mention (catchlights, shadow edges, falloff, color casts, Kelvin, skin speculars)?

### Takeaway
Each real setup has a recognizable signature. The model only needs the signature, not the gear name:
- shadow edge (hard/soft);
- shadow direction and length;
- falloff (how fast light drops toward the background);
- catchlight shape (window rectangle, ring, small point, none);
- specular highlight size on forehead/nose;
- colour temperature (≈2000K sodium → ≈2700–3200K tungsten → ≈4000–4200K cool fluorescent/LED → ≈5500K daylight/flash → ≈6500–8000K overcast/shade).

Mention 2–4 of these per prompt. Avoid stacking setups that cannot coexist.

### Cited Findings
**Colour temperature reference (Kelvin)**
- Tungsten/incandescent: about 2,400K (standard lamp) to 3,200K (professional tungsten photo light). Another chart gives 2,500–3,000K "orangey" (search summary) — [CAMEO: Color temperature](https://cameo.mfa.org/wiki/Color_temperature); [Engineering Toolbox via Google AMP](https://www.google.co.il/amp/s/www.engineeringtoolbox.com/amp/color-temperature-d_1776.html)
- Fluorescent: warm white about 2,950–3,000K, cool white about 4,200K (search summary) — [Crompton lamps guide (PDF)](https://www.superlecdirect.com/media/pdfs/crompton-lamps-colour-temperature-guide.pdf)
- LED: soft white about 2,700K, warm white about 3,000K (search summary) — [FastLED colour enums](https://fastled.io/docs/group___color_enums.html)
- High-pressure sodium: about 2,050–2,100K. Gaseous sources such as sodium "emit discrete spectral bands… they don't actually have a proper Kelvin temperature" (search summary) — [FastLED colour enums](https://fastled.io/docs/group___color_enums.html)
- Camera white-balance presets (vary by maker): Daylight ~5,500–5,600K; Flash ~5,500K (one archived thread measured a 6,518K flash preset); Cloudy ~6,500K (range 6,500–7,500); Shade ~7,500–8,000K; Tungsten ~3,000–3,200K; Fluorescent ~4,000K; sunrise/golden hour ~2,800–3,000K (weak source) (search summary) — [Cameraby WB presets](https://cameraby.com/en/learn/white-balance-presets); [B&C Camera](https://store.bandccamera.com/blogs/how-to/white-balance-photography-what-is-white-balance); [Capture One forum](https://support.captureone.com/hc/es/community/posts/360012080277-WB-Presets-Flash-is-6518-K-not-5600K-why)
- Overcast sky about 7,000K; heavily overcast up to 10,000K (search summary) — [Videvo color temperature 101](https://videvo.net/blog/?p=43944); [Artlist](https://artlist.io/blog/color-temperature/)
- A sunset rendered at the "correct" WB loses the warmth that made it worth shooting, so photographers often pick a warmer preset deliberately (search summary) — [Cameraby](https://cameraby.com/en/learn/white-balance-presets)

**Portrait patterns (key-light angle relative to the camera–subject axis)**
- Moving the key from straight in front of the subject to 90° at the side passes through **butterfly → loop → Rembrandt → split** (search summary):
  - **Butterfly:** light centred, high and in front, giving a butterfly-shaped shadow under the nose and deep shadow under the chin, often with a reflector below;
  - **Loop:** light about 20–45° off-axis; the small nose-shadow loop should not touch the cheek shadow;
  - **Rembrandt:** further around; the nose shadow meets the cheek shadow, leaving a small lit triangle on the shadow-side cheek ("closed loop");
  - **Split:** key about 90° to the side at face level; the dividing line runs down the centre of the nose.

  — [Glass: split lighting](https://glass.photo/photography-terms/split-lighting); [PhotoWorkout lighting patterns](https://www.photoworkout.com/?p=128244); [PictureCorrect 5 setups](https://www.picturecorrect.com/tips/5-essential-portrait-lighting-setups/); [Digital Photography School 4 styles](https://digital-photography-school.com/4-common-lighting-styles-to-get-the-perfect-portrait/)
- Sources differ on Rembrandt detail (triangle joined to the chin shadow vs triangle under the eye), and the loop/Rembrandt boundary is convention (search summary) — same sources as above.

**Window light (side / front / back)**
- **Side** (~45°) defines cheekbones and jaw and produces more shadow across the face. **Front** (photographer's back to the window, subject facing it) gives even, flatter light that "flattens features". **Backlit** (subject between window and camera) gives glow and atmosphere, but the subject goes dark and needs exposure compensation (search summary) — [The Lens Lounge: window light 3 ways](https://thelenslounge.com/window-light/); [Digital Photography School window light](https://digital-photography-school.com/portraits-with-window-light); [Sony: lighting and its effects](https://www.sony.ca/en/electronics/support/e-mount-body-ilce-7-series/ilce-7rm6/articles/00267922)
- **Catchlights:**
  - "If you can see the light source from where the subject's eyes are, there will be catchlights". The further the subject turns from the window, the smaller and more edge-located the catchlight (search summary) — [Daily Photo Tips: catchlights](https://dailyphototips.com/portraits/catchlights/)
  - Window catchlights are "not round". Softboxes give rectangular/square catchlights "just as they could be from a window"; ring lights give a ring (search summary) — [The Lens Lounge softbox](https://thelenslounge.com/what-is-softbox-light/); [SmallRig ring vs softbox](https://www.smallrig.com/blog/ring-light-vs-softbox.html)
- Direct sun through a window is "hard, unpleasant light". A sheer curtain diffuses it (search summary) — [Digital Photography School window light](https://digital-photography-school.com/portraits-with-window-light)
- **Falloff / inverse-square law:**
  - the closer the light is to the subject, the darker the background; with a window, "you would actually move the subject";
  - doubling the light–subject distance gives a quarter of the light (−2 stops);
  - with exposure set for the face, the background goes darker as the subject approaches the light.

  (search summary) — [CreativeLive: inverse square law](https://site.creativelive.com/class/natural-light-basics-scott-robert-lim/lessons/inverse-square-law); [Glass: inverse square law](https://glass.photo/photography-terms/inverse-square-law); [Neil van Niekerk: light fall-off](https://neilvn.com/tangents/photography-using-light-fall-off/)
- The closer the subject is to the window, the starker the highlight/shadow difference; the larger the window, the softer the light (search summary) — [ExpertPhotography window light](https://expertphotography.com/window-light-portraits); [PopPhoto window lighting](https://www.popphoto.com/how-to/2013/07/how-to-illuminate-portraits-window-lighting/)

**Overcast / open shade**
- **Overcast:** cloud cover acts as a giant diffuser. A source large relative to the subject gives softer, more even falloff. Overcast light "skews cool and blue", and nearby surfaces (grass, brick) add their own colour to skin. Eye sockets can go dark and catchlights weak, so the remedy is to face the subject toward the brightest sky or use a reflector (search summary) — [Fstoppers: flat light](https://fstoppers.com/education/how-make-flat-light-work-your-portraits-903227); [PhotographyTalk overcast](https://www.photographytalk.com/portrait-photography-in-overcast-and-rainy-conditions-the-underrated-advantage/); [SLR Lounge cloudy day](https://www.slrlounge.com/cloudy-day-photography-how-to-get-great-pictures-in-bad-weather/)
- **Open shade:** "a shaded area right next to bright, hard light". It gives soft but **directional** light that works like a giant softbox. Shade light is "noticeably bluer than sunlight" (search summary) — [PictureCorrect open shade](https://picturecorrect.com/?p=60240); [lilblueboo](https://www.lilblueboo.com/?p=20827)

**Direct midday sun (hard light)**
- The sun is effectively a point source, so shadows have hard edges. Overhead sun puts brow shadows into the eye sockets ("raccoon eyes") and makes people squint. Standard fixes: turn the subject's back to the sun (adds a rim light and stops the squint), add a reflector at chest level, or use overhead diffusion. Some photographers use noon light deliberately for graphic, high-contrast fashion (search summary) — [Daily Photo Tips: harsh shadows](https://dailyphototips.com/lighting/harsh-shadows/); [Light Stalking: midday light](https://www.lightstalking.com/4-strategies-deal-harsh-midday-light-portrait-work/); [Digital Photography School midday portraits](https://digital-photography-school.com/portraits-in-the-middle-of-the-day/); [CreativePro outdoor portraits](https://creativepro.com/shoot-better-outdoor-portraits/)

**Golden-hour backlight**
- Expose for the face, not the sky (or meter the sky for a silhouette). Rim light shows most on thin edges such as hair, with a low sun directly behind. Flare and spill are common. Golden-hour light is warm because the atmosphere filters out blue near the horizon (search summary) — [Light Stalking backlit golden hour](https://www.lightstalking.com/backlit-portraits-golden-hours/); [PhotoWorkout rim light](https://www.photoworkout.com/?p=128243); [Adobe golden hour](https://www.adobe.com/creativecloud/photography/technique/golden-hour); [Insta360 backlight](https://www.insta360.com/blog/tips/backlight-photography.html)

**On-camera direct flash vs bounce flash**
- **Direct flash** from the camera position gives "flat faces, hard shadows on the wall behind the subject, and red eye". It has "seemingly no depth", and shiny surfaces reflect it back into the lens (search summary) — [Globe and Mail: how to light your pictures](https://www.theglobeandmail.com/multimedia/camera-club/how-to-light-your-pictures/article1214994); [Shutterbug: bounce flash](https://shutterbug.com/node/430076)
- **Bounce flash:**
  - the source grows from a few centimetres to a metre or more, so shadow edges are soft and the light "reads more like ordinary room light";
  - straight-up ceiling bounce can still cast shadows under eyes and chin, and sideways bounce often looks more natural;
  - the light picks up the colour of the bounce surface;
  - a small bounce card adds catchlights.

  (search summary) — [Digital Photography School bounce flash](https://digital-photography-school.com/quick-guide-bounce-flash-more-natural-looking-photos/); [TalkPhotography forum](https://www.talkphotography.co.uk/threads/ceiling-bounced-flash-basic-question.292462/); [Neil van Niekerk: bounce direction](https://neilvn.com/tangents/?p=94); [DIYPhotography: ceiling as softbox](https://www.diyphotography.net/?p=313502)
- **Speculars and shine:** "specular highlights are often seen whenever someone with slightly oily or sweaty skin has been photographed in direct sunlight or with a flash". A counterpoint: shine depends mainly on the skin surface, and a huge softbox can still produce shiny foreheads (search summary) — [Fstoppers: fix shiny faces](https://fstoppers.com/photoshop/how-fix-shiny-faces-person-and-photoshop-521202); [CreativeLive: specular highlights](https://site.creativelive.com/class/understanding-light-light-modifiers-mark-wallace/lessons/specular-highlights)

**Ring light (UGC/beauty)**
- Ring lights are "designed to create shadowless/flat light". Moving the light closer gives more dimension; further away flattens it because falloff is less pronounced. Signature circular "halo-like" catchlight, and the face can look "two-dimensional, almost airbrushed". Cheap bulbs can confuse auto-WB, giving an orange or blue tint (search summary) — [Westcott support: ring light flat](https://help.fjwestcott.com/en-US/why-is-the-light-from-my-ring-light-so-flat-637336); [Kraftgeek: phone video lighting](https://kraftgeek.com/blogs/creator-inspiration/best-lighting-for-phone-video-ring-light-led-panel-or-natural-light); [SmallRig](https://www.smallrig.com/blog/ring-light-vs-softbox.html)

**Overhead light (office ceiling panels, bathroom fixtures, gym high-bays)**
- Top light is blocked by brow, nose and chin, giving raccoon-eye sockets and shadows under nose and chin. Bare bulbs give sharp edges; large diffused sources give gentler falloff. Direct top-down overhead LEDs give "harsh, unflattering shadows, especially under the eyes, nose, and chin". The usual fill is about 45° at lower intensity, or a white reflector below the face (search summary) — [Daily Photo Tips: face shadows](https://dailyphototips.com/portraits/face-shadows/); [Beverly Boy: overhead LEDs](https://beverlyboy.com/film-technology/working-with-overhead-leds-how-to-kill-the-ugly-top-light); [Melies: top light](https://melies.co/cinematic-techniques/lighting/top-light)

**Fluorescent and mixed tungsten + daylight**
- Each source has its own cast, and the eye auto-corrects, so mixes are easy to miss. Fluorescents have spectral "spikes" that one Kelvin setting cannot correct. In a tungsten + daylight case, an orange-and-green cast was likely the camera's AWB over-correcting for the tungsten (search summary) — [Peachpit: mixed colour temperatures](https://www.peachpit.com/articles/article.aspx?p=1963994); [CML: fluorescents & daylight](https://cinematography.net/edited-pages/FluorescentsDaylight.htm); [Photrio colour cast thread](https://www.photrio.com/forum/threads/color-cast-help.161652)

**Night street: sodium vs LED**
- Sodium is "nearly monochromatic yellow light with poor color rendering". Many photographers miss its warm glow on camera. Early LA LED streetlights were about 4,000K and residents called them "clinical… hospital or prison", so cities warmed them to about 3,000K. Astronaut photos show cities switching from orange to white light (PetaPixel, Sept 8, 2026) (search summary) — [PetaPixel (2026-09-08)](https://petapixel.com/2026/09/08/astronauts-before-and-after-photos-show-how-cities-switched-from-orange-to-white-light/); [PMF IAS sodium vs LED](https://www.pmfias.com/sodium-lamps-vs-led-street-lighting-pyq-2021/)

**Rim / hair / kicker**
- A hair light is a rim aimed at the top of the head. A kicker sits behind and to one side so its edge runs along the face or body. The rim separates the subject from the background and reads most strongly against a **dark** background; against a light backdrop it largely disappears. Light pointed back at the lens causes contrast-reducing flare (search summary) — [Glass: rim light](https://glass.photo/photography-terms/rim-light); [Morphic glossary: rim light](https://morphic.com/br/ai-glossary/rim-light)

**Car interior**
- Generic window-light rules apply: face the light, closer means more contrast, overcast days give soft light, a white card fills the dark side. No source covers windshield glare, tint or dashboard light (search summary) — [ExpertPhotography window light](https://expertphotography.com/window-light-portraits); [Masterclass Photographers: photos inside the car](https://masterclassphotographers.com/blog/en/ideas-for-photos-inside-the-car/)

### Inferences
**Copy-paste lighting lexicon.** The physical traits are anchored in the citations above. The prompt wording is my synthesis for LLM-encoder models (GPT Image 2/2.5, Nano Banana Pro, Seedream 5, FLUX.2/3, Qwen-Image-2.x, Z-Image, Krea 2). None of it has been test-rendered here.

| # | Setup | Physical signature to state | Copy-paste phrase (EN, for prompts) | Phrasing that makes it look fake |
|---|---|---|---|---|
| 1 | Window, side (~45–90°) | soft-to-medium edge; shadow side 1–3 stops darker; rectangular catchlight; background darker if subject is close to the window | "lit only by a large window on camera-left, about 45 degrees to her face; soft but directional light, the right side of her face falls into gentle shadow; rectangular window reflection in her eyes; the room behind her is noticeably darker" | "perfectly even lighting", "no shadows", adding a fill/rim the room cannot have |
| 2 | Window, front (subject faces window) | flat, even; large catchlights centred in the eyes; low texture | "she faces a bright window just behind the camera; flat, even daylight on her face, large square catchlights, natural daylight white balance around 5500K" | "studio lighting", "beauty lighting", glowing skin |
| 3 | Window, backlit | face darker than background, low contrast; bright edge on hair/shoulders; window blown out; possible veiling flare | "standing with her back to a bright window; the window is overexposed, her face slightly underexposed but readable, soft wrap-around light on the edges of her hair, a little haze from flare" | perfectly exposed face *and* detailed window view (HDR look) |
| 4 | Overcast / open shade | very soft shadows, little direction; cool cast (~6500–7500K shade); weak catchlights, slightly dark eye sockets; muted colour; skin picks up green/brick bounce | "overcast afternoon, the sky acts like a giant softbox; very soft shadows, slightly cool white balance, muted colours, faint catchlights, a hint of green bounce from the grass on her jaw" | "vibrant colors", "sun-kissed glow" under an overcast sky |
| 5 | Golden-hour backlight | low warm sun behind (~2800–3000K on rim); face in shade, filled by bounce; warm rim on hair; flare/haze; lifted blacks | "late-afternoon sun low behind her, warm orange rim light on her hair and shoulders, her face in soft open shade lit by bounce from the pavement, slight lens flare and haze, warm white balance" | front-lit face *and* backlit hair from the same sun; flawless no-flare contrast |
| 6 | Direct midday sun | hard-edged shadows; short shadows under brows, nose and chin; squint; pinpoint speculars on forehead/nose; high contrast | "harsh midday sun from almost directly overhead, hard-edged shadows under her brows and nose, she squints slightly, small bright specular highlights on her forehead and nose, short hard shadow at her feet" | "soft flattering light" at noon outdoors; no squint in full sun |
| 7 | On-camera direct flash | flat frontal light; hard shadow on the wall just behind/offset from the subject; fast falloff to a dark background; shiny T-zone; possible red-eye; small point catchlight | "photographed with the phone's built-in flash at night, flat frontal light, a hard dark shadow on the wall just behind her, background falls off into darkness, shiny highlights on her forehead and nose, small pinpoint catchlights" | flash-lit face with a perfectly lit, detailed background |
| 8 | Bounce flash (ceiling/wall) | soft, top-or-side-biased room-like light; mild shadows under eyes/chin if straight up; picks up the ceiling/wall colour | "indoor flash bounced off a white ceiling, soft even room light from above, faint shadows under her eyes and chin, natural white balance" | — |
| 9 | Ring light (UGC beauty) | shadowless frontal light; circular catchlight; flat, "airbrushed" face; slight halo shadow around the face if close to a wall | "lit by a ring light directly in front at eye level, ring-shaped catchlight in both pupils, flat shadowless face, slight soft shadow outline on the wall behind her" (add "visible pores, slight shine on nose" to fight the airbrush effect) | ring light *plus* dramatic side shadows; ring light *plus* "glowing skin" |
| 10 | Overhead office fluorescent / LED panels | top light; shadows in eye sockets and under nose/chin; cool, slightly green cast (~4000–4200K); flat, unflattering | "overhead fluorescent ceiling panels, top-down light, mild shadows in her eye sockets and under her chin, slightly cool greenish cast, flat unflattering office light" | "perfect lighting" in an office; warm golden glow under panels |
| 11 | Bathroom vanity | strip or bulbs above the mirror (top-front); shadows under brows; bright specular on forehead; warm (~2700–3000K) or cool LED (~4000K) | "vanity light bar above the mirror, light from slightly above and in front, faint shadow under her brows, bright highlight on her forehead, warm 3000K bulbs, glossy tile reflections" | — |
| 12 | Car interior (day) | side-window key; dark cabin interior; light from the windshield on one side; seatbelt/headrest shadows; reflections in the glass | "daylight from the driver-side window on camera-left lights half her face, the car interior stays dark, soft fill from the windshield, faint reflection on the side glass" | evenly lit cabin; no window direction |
| 13 | Car interior (night) | very low light; small warm dome light from above, or the cool screen/dashboard glow from below; heavy noise; city bokeh | "night inside a parked car, the only light is the dashboard screen glowing cool blue on her chin and lower face, faint warm streetlight through the window, grainy high-ISO phone photo" | clean, noiseless, fully lit face at night |
| 14 | Mixed tungsten + daylight | two casts on one face: warm (~3000K) on one side, cool (~5500K+) on the other; the camera WB splits the difference | "mixed light: cool daylight from the window on camera-left, warm tungsten lamp on camera-right, her face has a cool side and a warm side, white balance in between" | a single neutral cast in a room that visibly has both sources |
| 15 | Phone screen glow | small, close, cool-blue source below/in front; fast falloff; face lit, room dark; noise | "late at night in a dark bedroom, her face lit only by the cool blue glow of the phone screen in her hand, light falls off quickly past her face, grainy low-light photo" | the screen glow lighting the whole room |
| 16 | Night street: sodium / LED | sodium ≈2000–2100K, monochrome orange, poor colour separation; LED ≈3000–4000K whiter; overhead pools of light; hard top shadows | "under an old sodium streetlight, monochrome orange light from above, colours of her clothes barely distinguishable, deep shadows outside the light pool" or "under a white LED streetlight around 4000K, slightly clinical cool-white light from above" | neon rim light everywhere; teal-orange grade |
| 17 | Softbox loop / Rembrandt / butterfly / split | see the angle mapping above; rectangular catchlight; soft edge | "one large softbox camera-left, about 30–45 degrees off-axis and slightly above eye level, small nose shadow pointing down toward the right corner of her mouth (loop lighting), no fill, plain wall behind" (Rembrandt: "…further to the side, a small triangle of light on her shadow-side cheek") | "three-point lighting", "studio lighting" on a UGC shot (reads as a pro set) |
| 18 | Rim / hair light | thin bright edge on hair/shoulder only on the side the source is; needs a darker background; flare if pointing at the lens | "a single warm practical lamp behind her on the right puts a thin rim of light on the right side of her hair; the background stays dim" | "rim light" on both sides with no motivating source; rim against a bright background |

**Specular cue (use in most realism prompts):** "small natural specular highlights on the forehead, nose bridge and lower lip consistent with the light direction". This ties shine to the source and avoids uniform "glow". It follows from the hard-vs-soft specular findings.

**Kelvin wording:** give one Kelvin number per source ("warm 3000K bulb", "daylight about 5500K"). Do not use a Kelvin number as a global style. For sodium, describe the colour ("monochrome orange") rather than a Kelvin value, since sodium has no true colour temperature.

### Gaps
- No photography source with a Kelvin value for **phone/laptop screens** was found. Screens are commonly calibrated near D65 (~6500K), but that is uncited here and needs verification.
- Catchlight shapes from window **mullions/panes** were not covered by any source found.
- No source covers car **dashboard/dome lighting** or windshield glare in portraits. Rows 12–13 are inferred from general window/low-light physics.
- There are no measured highlight-size or shadow-ratio numbers for a typical UGC scene. The "1–3 stops" figure in row 1 is my illustration based on inverse-square behaviour, not a sourced measurement.

---

## 3. How to describe light direction (relative to subject and camera), keep subject light consistent with the background, and avoid descriptions that make images look fake

### Takeaway
- **Direction:** state the source's position in **camera terms** ("camera-left/right", "behind the camera", "behind her") plus a **height** ("at eye level", "slightly above", "overhead", "from below"), and optionally an **angle off the lens axis** (0° = butterfly/frontal, ~30–45° = loop/Rembrandt, 90° = split, >135° = rim/backlight).
- **Consistency:** make the background obey the same source with four checks: direction, hardness, colour temperature, and shadow/falloff.
- **Common AI tells:**
  - shadows that disagree;
  - a subject lit from one side while the background is lit from the other;
  - rim light "painted" on every edge;
  - studio-perfect light in a candid scene;
  - HDR-flat exposure where face and bright window are both perfectly exposed.

### Cited Findings
- **Direction phrasing that practitioners use:**
  - "golden hour backlighting with rim light on subject's left side" (Seedream review) — [Dzine](https://www.dzine.ai/blog/seedream-5-0-review/);
  - "soft diffused morning light from the left" (Nano Banana) — [PicassoIA](https://blog.picassoia.com/prompts-that-work-well-with-nano-banana-pro);
  - "Key light at 45 degrees elevation" — [Chase Jarvis](https://chasejarvis.com/blog/nano-banana-prompts/).

  All via search summary.
- **Pattern angle mapping** (0° → 90°: butterfly → loop → Rembrandt → split) (search summary) — [PhotoWorkout](https://www.photoworkout.com/?p=128244); [PictureCorrect](https://www.picturecorrect.com/tips/5-essential-portrait-lighting-setups/)
- **AI lighting tells:**
  - generators learn statistical patterns rather than 3D geometry, so cast shadows and reflections "often lack consistent perspective", and human vision is poor at catching this (search summary) — [Content Authenticity Initiative: photo forensics](https://contentauthenticity.org/blog/photo-forensics-from-lighting-shadows-and-reflections)
  - shadows disagree with each other or with the scene light, and subjects "float" when shadows are missing (search summary) — [arXiv 2602.19715](https://arxiv.org/pdf/2602.19715); [Rewarx: one thing missing](https://www.rewarx.com/blogs/your-ai-images-look-fake-because-youre-missing-this-one-thing)
  - subject lit from one side while the backdrop is lit from the other (search summary) — [getimg.ai: AI product photos look real](https://getimg.ai/blog/how-to-make-ai-product-photos-look-real); [MagicShot](https://magicshot.ai/blog/why-your-ai-images-still-look-fake-12-tells-and-how-to-kill-them)
  - rim light "painted onto edges" that wraps unnaturally (vendor blogs, search summary) — [Rewarx: studio lighting artifacts](https://www.rewarx.com/blogs/fake-studio-lighting-from-ai-generated-product); [Rewarx: 5 problems](https://www.rewarx.com/blogs/5-ai-image-problems-synthetic-product-photos)
  - "studio-perfect light even in supposedly candid shots" (search summary) — [Atlas Cloud](https://www.atlascloud.ai/blog/guides/seedream-5-pro-realistic-portraits)
  - a V8 complaint that Midjourney "defaults to an almost too-clean, hyper-polished look" (search summary) — [MindStudio V8 alpha](https://www.mindstudio.ai/blog/what-is-midjourney-v8-alpha-strengths-weaknesses)
- **Compositing light-matching checklist** (compositing tutorials, search summary):
  1. light direction (flip the image if opposite);
  2. shadow hardness (crisp = small or distant source; wide transition = large or near source);
  3. colour temperature, judged on neutral references (white, grey, packaging);
  4. shadow direction, softness and intensity aligned with the main source, including a soft contact shadow (one tutorial: 20–40% opacity tapering);
  5. matching depth of field and grain;
  6. edge halos and spill. AI tools handle rim/specular highlights poorly, so fix those by hand.

  — [DEV: why composited people look pasted](https://dev.to/miatanaka/why-composited-people-look-pasted-lighting-and-color-coherence-111o); [Jeff Bullas forum: AI match lighting](https://www.jeffbullas.com/thread/can-ai-match-my-photos-lighting-and-color-for-seamless-composites/); [Pippit: match background to product lighting](https://www.pippit.ai/blog/match-new-background-to-product-lighting); [PictureCorrect composites](https://www.picturecorrect.com/how-to-create-a-composite-image-photographing-editing/)
- **Mixed-light diagnosis:** identify every source and where it falls on the subject first. Each source has its own cast (search summary) — [Peachpit](https://www.peachpit.com/articles/article.aspx?p=1963994)
- **Rim needs a dark background,** and a backlight aimed at the lens causes flare (search summary) — [Glass: rim light](https://glass.photo/photography-terms/rim-light)

### Inferences
**Direction grammar (copy-paste template).** Use camera-relative terms; "subject's left" is ambiguous to models and humans:
```
[SOURCE] [POSITION: camera-left | camera-right | behind the camera | behind her, camera-left | directly overhead | below the face]
[HEIGHT: at eye level | slightly above eye level | high above | from below]
[ANGLE (optional): about 45 degrees off the lens axis | 90 degrees to the side | from behind]
[QUALITY: hard-edged | soft but directional | very soft and diffused]
[RESULT ON FACE: which side is in shadow, where the nose shadow falls, catchlight shape]
[COLOUR: warm ~3000K | neutral daylight ~5500K | cool shade ~7000K]
```
Example: "Key light: a large window camera-left, slightly above eye level, about 60 degrees off the lens axis; soft but directional; her right cheek falls into shadow with a small triangle of light under the eye; rectangular catchlights; neutral daylight about 5500K."

**Light-matching sentence (append to every avatar-in-scene prompt):** "The same window light that lights her face also lights the room: the wall on the left is brighter, shadows in the room fall to the right, matching softness and colour; no separate studio light on her."

For edits that place an avatar into a new background (Nano Banana / GPT Image / Qwen-2.1 edit): "Relight the person to match the background: light comes from [direction] at [colour temperature]; match shadow softness; add a soft contact shadow under her feet/elbows; match the background's grain and depth of field."

**Descriptions that reliably push toward fake** (avoid them, or replace with the physical version):

| Avoid | Why (physics) | Replace with |
|---|---|---|
| "perfect lighting", "flawless lighting", "even lighting", "no shadows" | real faces always have a shadow side unless the light is frontal and flat | name the source and the shadow side |
| "glowing skin", "radiant glow", "luminous skin" | invents an emissive or subsurface bloom no real light produces | "small specular highlights on forehead and nose consistent with the window" |
| "rim light" with no source, or on both sides | a rim exists only on the side of a source behind the subject, and needs a darker background | "a lamp behind her on the right gives a thin edge of light on her right shoulder" |
| "three-point lighting", "studio lighting", "softbox" in a UGC/home scene | implies a pro set the location cannot have | the room's practical sources (window, ceiling bulb, phone flash) |
| HDR combos: "bright window and perfectly exposed face", "detailed sky and face in backlight" | a single exposure cannot hold both | "the window is blown out / her face slightly underexposed" |
| "volumetric light", "god rays" indoors | needs haze or dust in the air | omit, or "dusty air catches the sunbeam" only if motivated |
| several colours of light without sources ("teal and orange", "neon accents") | colour casts need sources | name the neon sign or the screen that emits each colour |
| background lit from a different side or hardness than the face | breaks the inverse-square and shadow logic | the light-matching sentence above |

### Gaps
- No quantitative study was found on how often each model produces mismatched subject/background light, or on whether adding a light-matching sentence reduces it. Evidence is practitioner heuristics plus forensic literature.

---

## 4. Which realism LoRAs and sampler settings are most recommended in 2026 for each open model (with weights and links)?

### Takeaway
- **Start from the official ComfyUI templates.** These were extracted from the JSON workflows on GitHub, and every one of them uses **Euler (or res_multistep/er_sde) with the `simple` scheduler**:
  - FLUX.2 [dev]: guidance 4, 20 steps (8 with Turbo LoRA);
  - FLUX.2 [klein] base: CFG 5, 20 steps; distilled: CFG 1, 4 steps;
  - **FLUX 3 Image Klein** base: CFG 3.5, 50 steps; distilled: CFG 1, 4–16 steps (16 default);
  - **Qwen-Image-2.1**: CFG 1, 25 steps (official pipeline 40–50); Turbo: 8 steps;
  - Z-Image base: CFG 4, 25 steps, res_multistep, shift 3; Turbo: CFG 1, 8 steps, res_multistep, shift 3;
  - **Krea 2 Turbo**: CFG off, 8 steps, up to 2K; **Krea 2 RAW**: CFG 3.5, 52 steps, ≤1K.
- For skin detail, the community moves to higher-order or SDE samplers (RES4LYF `res_2m`/`res_2s` with `beta57`/`bong_tangent`; DPM++ SDE + beta on Z-Image-Turbo). It also uses sigma-detail tricks (Detail Daemon 0.1–1.0; Multiply Sigmas 0.95–0.99) and a **two-pass refine at denoise ≈0.2–0.4**.
- Realism LoRAs are model-specific:
  - **Krea 2** has the richest 2026 realism-LoRA ecosystem (realism V1/V2, Inline Skin, Realism LoRA by gokaygokay);
  - **Z-Image-Turbo** has snapshot LoRAs at 0.6–0.7;
  - **Qwen-Image-2512** uses the phone-look LoRAs (Lenovo/Samsung UltraReal) at about 0.7–1.0;
  - **FLUX.2 Klein 9B** has a realism full fine-tune (True-V2) plus skin LoRAs at 0.5–0.8;
  - **FLUX 3 Klein** (released Oct 15, 2026) has no realism LoRAs yet.

### Cited Findings

**A. Official baseline settings per model (fetched from Comfy-Org GitHub templates/docs unless noted)**

| Model | Sampler / scheduler | Steps | Guidance / CFG | Other | Source |
|---|---|---|---|---|---|
| FLUX.2 [dev] | euler + Flux2Scheduler | 20 (8 with Turbo LoRA at strength 1) | FluxGuidance **4** | up to 4MP; Mistral-3-small text encoder | [image_flux2_text_to_image.json](https://github.com/Comfy-Org/workflow_templates/blob/main/templates/image_flux2_text_to_image.json); [flux-2-dev.mdx](https://github.com/Comfy-Org/docs/blob/main/tutorials/flux/flux-2-dev.mdx) |
| FLUX.2 [klein] 4B/9B **base** | euler + Flux2Scheduler | 20 | CFGGuider **5** | 1024×1024 default | [image_flux2_klein_text_to_image.json](https://github.com/Comfy-Org/workflow_templates/blob/main/templates/image_flux2_klein_text_to_image.json); [image_flux2_text_to_image_9b.json](https://github.com/Comfy-Org/workflow_templates/blob/main/templates/image_flux2_text_to_image_9b.json) |
| FLUX.2 [klein] 4B **distilled** | euler + Flux2Scheduler | **4** | CFG **1** | ~1.2 s on a 5090, 8.4 GB VRAM | same JSON; [flux-2-klein.mdx](https://github.com/Comfy-Org/docs/blob/main/tutorials/flux/flux-2-klein.mdx) |
| **FLUX 3 Image Klein (base)** | euler / simple | **50** | **3.5** | Qwen3.5-9B prompt upsampler **on by default**; Qwen3-VL-4B encoder; FLUX.2 VAE; >24 GB → bf16 weights; ComfyUI ≥0.41.0; FLUX Kommunity License | [image_flux3_klein_t2i.json](https://github.com/Comfy-Org/workflow_templates/blob/main/templates/image_flux3_klein_t2i.json); [flux-3-klein.mdx](https://github.com/Comfy-Org/docs/blob/main/tutorials/flux/flux-3-klein.mdx) |
| **FLUX 3 Image Klein Distilled** | euler / simple | **4–16 (16 default)** | **1** ("raising cfg does not help") | guidance-free, step-distilled | [image_flux3_klein_distilled_t2i.json](https://github.com/Comfy-Org/workflow_templates/blob/main/templates/image_flux3_klein_distilled_t2i.json); [flux-3-klein.mdx](https://github.com/Comfy-Org/docs/blob/main/tutorials/flux/flux-3-klein.mdx) |
| **Qwen-Image-2.1** | euler / simple | **25** in the template; "official pipeline uses about 40–50 with euler… more advanced samplers need fewer steps" | **1** ("keep 1 for the official path. Raise it only if you use a negative prompt") | native 2K (2048×2048); multiples of 32; template default 1 MP; optional Qwen3.5-9B prompt enhancer (turn `thinking_mode` on with it) | [image_qwen_image_2_1_t2i.json](https://github.com/Comfy-Org/workflow_templates/blob/main/templates/image_qwen_image_2_1_t2i.json); [qwen-image-2-1.mdx](https://github.com/Comfy-Org/docs/blob/main/tutorials/image/qwen/qwen-image-2-1.mdx) |
| **Qwen-Image-2.1 Turbo** | euler (SamplerCustomAdvanced) | **8** | 1 | distilled checkpoint of the same model | [image_qwen_image_2_1_turbo_t2i.json](https://github.com/Comfy-Org/workflow_templates/blob/main/templates/image_qwen_image_2_1_turbo_t2i.json) |
| Z-Image (base) | **res_multistep / simple** | **25** | **4** | ModelSamplingAuraFlow shift **3**; responsive to negative prompts | [image_z_image.json](https://github.com/Comfy-Org/workflow_templates/blob/main/templates/image_z_image.json); [z-image.mdx](https://github.com/Comfy-Org/docs/blob/main/tutorials/image/z-image/z-image.mdx) |
| Z-Image-Turbo | **res_multistep / simple** | **8** | **1** | shift **3**; 8 NFEs; fits 16 GB | [image_z_image_turbo.json](https://github.com/Comfy-Org/workflow_templates/blob/main/templates/image_z_image_turbo.json); [z-image-turbo.mdx](https://github.com/Comfy-Org/docs/blob/main/tutorials/image/z-image/z-image-turbo.mdx) |
| **Krea 2 Turbo** | euler / simple | **8** | **0 (CFG off)** (Comfy: cfg 1) | `--mu 1.15` timestep shift recommended; 1K–2K (2048×2048 OK); Qwen3-VL-4B encoder; Qwen-Image VAE; prompt enhancement on by default | [krea-ai/krea-2 README](https://github.com/krea-ai/krea-2/blob/main/README.md); [image_krea2_turbo_t2i.json](https://github.com/Comfy-Org/workflow_templates/blob/main/templates/image_krea2_turbo_t2i.json); [krea-2.mdx](https://github.com/Comfy-Org/docs/blob/main/tutorials/image/krea/krea-2.mdx) |
| **Krea 2 RAW** | full sampler with CFG | **52** | **3.5** | "trained to generate up to 1k resolution"; not tuned for final quality; **train LoRAs on RAW, run on Turbo**; Krea Community License (commercial licence via opensource@krea.ai) | [krea-ai/krea-2 README](https://github.com/krea-ai/krea-2/blob/main/README.md) |
| Qwen-Image-2512 (for reference) | — | 50 (official) or 4 with Lightning LoRA | true CFG 4.0 | Lightning: `lightx2v/Qwen-Image-Lightning-4steps-V1.0` | [qwen-image-2512.mdx](https://github.com/Comfy-Org/docs/blob/main/tutorials/image/qwen/qwen-image-2512.mdx); [QwenLM/Qwen-Image README](https://github.com/QwenLM/Qwen-Image) |

- **Krea 2 facts:**
  - It is "trained from scratch", "the most aesthetic open-source image model available", and "#1 text-to-image model from an independent lab on Artificial Analysis" (vendor claim). It ships with 9 **style** LoRAs (darkbrush, dotmatrix, etc.), none for realism, all at strength 1.0 with trigger words — [krea-ai/krea-2 README](https://github.com/krea-ai/krea-2/blob/main/README.md); [Comfy template note](https://github.com/Comfy-Org/workflow_templates/blob/main/templates/image_krea2_turbo_t2i.json)
  - The release date conflicts: a news summary says June 22, 2026, while the comfyui-wiki model page says 2026-04. Parameter count is about 12–12.9B (search summary) — [comfyui-wiki news](https://comfyui-wiki.com/en/news/2026-06-22-krea-2-open-source-text-to-image); [comfyui-wiki model page](https://comfyui-wiki.com/en/models/krea/krea-2); [Krea open-source page](https://www.krea.ai/krea-2-open-source)
- **FLUX.2 [klein] (BFL/fal):** distilled = about 4 steps at guidance 1.0; base = about 50 steps at guidance 4.0; distilled "guidance_scale is not used". 4B and Base 4B are Apache 2.0; 9B and Base 9B are FLUX Non-Commercial. Distilled models "do not work well if you use too many steps" (search summary) — [fal FLUX.2 klein user guide](https://fal.ai/learn/devs/flux-2-klein-user-guide); [JarvisLabs](https://docs.jarvislabs.ai/tutorials/running-flux2-klein); [Diffusion Doodles](https://diffusiondoodles.substack.com/p/flux2-klein-shrinking-flux2-dev). Note: the Comfy base template uses 20 steps / CFG 5, not 50 / 4.
- **Community FLUX.2 Klein guidance:** Euler + Simple "produces the cleanest results; avoid Euler Ancestral, as it does not converge cleanly on distilled models". More than 4 steps or a higher CFG degrades the distilled model; base 4B/9B at 20–24 steps with CFG 3.5–5.0. Single community source, not BFL (search summary; the exact page within the result set is uncertain, likely [tech-insider: run FLUX locally 2026](https://tech-insider.org/how-to-run-flux-locally-with-comfyui-2026/))
- **FLUX.2 [dev] Turbo LoRA (fal):** a distilled LoRA for 8-step generation, quality "matched or surpassed" (vendor claim), with pre-shifted sigmas `[1.0, 0.6509, 0.4374, 0.2932, 0.1893, 0.1108, 0.0495, 0.00031]`. It inherits the **FLUX.2 [dev] non-commercial** licence (search summary) — [HF fal/FLUX.2-dev-Turbo](https://huggingface.co/fal/FLUX.2-dev-Turbo). The Comfy template loads `Flux_2-Turbo-LoRA_comfyui.safetensors` from [ByteZSzn/Flux.2-Turbo-ComfyUI](https://huggingface.co/ByteZSzn/Flux.2-Turbo-ComfyUI) at strength 1 (fetched template).
- **FLUX 3 Klein extras:** an unofficial `WAS/flux3_klein` repo offers distillation LoRAs so the base model "samples the way the distilled model does in 16 steps" (search summary) — [HF WAS/flux3_klein](https://huggingface.co/WAS/flux3_klein)
- **Qwen-Image-2.1 Lightning:** LightX2V released a 4-step distilled LoRA for Qwen-Image 2.1 on **Oct 13, 2026**, compared against 40 steps with CFG disabled. No skin-texture assessment was published (search summary) — [comfyui-wiki news 2026-10-13](https://comfyui-wiki.com/en/news/2026-10-13-qwen-image-2-1-lightning)

**B. Realism / skin / amateur-photo LoRAs and fine-tunes (search summaries; verify each page before use)**

*Krea 2 (train on RAW, run on Turbo)*
- **Krea-2-Realism-LoRA** (by gokaygokay; HF `bonticario/Krea-2-Realism-LoRA`):
  - trained with the fal Krea LoRA trainer on Krea-2-Raw and used on Turbo; "no trigger word is required"; targets "candid, everyday photorealism";
  - optimal at **1024–1536 px short side**; examples rendered at **1280×1600, 8 steps, guidance 0**;
  - weight not stated.

  — [HF bonticario/Krea-2-Realism-LoRA](https://huggingface.co/bonticario/Krea-2-Realism-LoRA); [HackerNoon](https://hackernoon.com/krea-2-realism-lora-brings-candid-photorealism-to-krea-2)
- **Inline Skin LoRA (Krea 2 RAW):** targets skin pores and "natural subsurface scattering", and carries over to Turbo. Strength not found — [HF inlineresearch/skin-lora-krea-2-raw](https://huggingface.co/inlineresearch/skin-lora-krea-2-raw)
- **Krea2 realism V1:** weight **1.0 general** (1.5–2.0 NSFW) — [HF RudySen/Krea2-realism-V1](https://huggingface.co/RudySen/Krea2-realism-V1)
- **Krea2 realism V2:** "you can hit 1.0 with a good prompt", but the author prefers **1.5–2.0** — [HF cusiman/Krea2-realism-V2](https://huggingface.co/cusiman/Krea2-realism-V2) (mirror: [zeroooo719](https://huggingface.co/zeroooo719/Krea2-realism-V2))
- **Krea2 Realistic Quality Enhancer ("No AI Look"):** **0.8–1.0**, trigger `hdx_v1` — [RunningHub](https://www.runninghub.ai/model/public/2098359220788899841)
- **Sogni krea2-realism slider:** sweet spot around **−1 to +1**. A different BloomGirls LoRA note says texture holds up to about 1.0, flat surfaces patch by 1.5 and fine texture smears at 2.0 — [Sogni krea2-realism](https://www.sogni.ai/loras/krea2-realism); [Sogni BloomGirls](https://www.sogni.ai/loras/krea2-bloomgirls); [Sogni community LoRAs blog](https://blog.sogni.ai/blogs/krea2-community-loras/)
- A "Basic Krea 2 Turbo Realism" workflow exists on Floyo (details not retrieved) — [Floyo](https://floyo.ai/workflows/basic-krea-2-turbo-realism-98b6oshn19my)

*Z-Image-Turbo*
- **RealisticSnapshotZImageTurbo:** strength **0.60–0.70**; tags include "amateur digital snapshot", "smartphone capture", "high ISO noise", "direct on-camera flash", "visible pores", "subsurface scattering", "wide-angle lens", "barrel distortion" — [HF Yuuuna/RealisticSnapshotZImageTurbo](https://huggingface.co/Yuuuna/RealisticSnapshotZImageTurbo)
- **"low impact realism"** LoRA for amateur/real-world photography (Jan 6, 2026; author opinion that Turbo gives the best output) — [Civitai 2283998](https://civitai.com/models/2283998)
- **Realistic_Sa_May** checkpoint merge: Z-Image-Turbo + the creator's Realistic_LoRA, trained on about 5,000 real photos (Dec 2, 2025) — [Civitai 2188147](https://civitai.com/models/2188147)
- **Z-Image-Aesthetic** LoRA (Jan 27, 2026; mostly artistic). The author suggests for Turbo: `heunpp2` + `linear_quadratic`, CFG 1.5, 20 steps, weight 0.8–1.2. Civitai's own generator defaults are CFG 1, 9 steps — [Civitai 2214707](https://civitai.com/models/2214707); [Civitai orchestration docs](https://developer.civitai.com/orchestration/recipes/zimage)
- **Z-Image base:** a Hugging Face commenter noted a lack of base realism fine-tunes, and said base "sticks to prompts way better than Turbo" — [HF discussion](https://huggingface.co/nphSi/Z-Image-Lora/discussions/51)

*Qwen-Image-2512 (and older Qwen-Image)*
- **Lenovo UltraReal** (by Danrisi; HF mirror `gorlamee/LenovoUltraReal`): trigger **`l3n0v0`**; described as "balanced realism for mimicking flagship phone camera tones". Used alongside **Samsung UltraReal** and **Boreal** in a Qwen-Image ComfyUI tutorial (Oct 2025, built for the original Qwen-Image; confirm 2512 compatibility) — [HF gorlamee/LenovoUltraReal](https://huggingface.co/gorlamee/LenovoUltraReal); [Kombitz tutorial](https://www.kombitz.com/2025/10/16/how-to-use-realistic-loras-with-qwen-image-in-comfyui/)
- **Samsung LoRA tagged qwen_image:** "Use 0.7–1.0 weight (depends on artifacts in scene)". It is unverified that this is the same UltraReal LoRA — [CivArchive](https://civarchive.com/tungsten/models/GUkjZTt2gC/versions/GnLUrZzVXn)
- Qwen plastic-skin complaints ("looks like a doll"). One creator's fix: a skin-texture LoRA + a "beauty" LoRA + a RES4LYF sampler, on a 4-step Lightning base. The same guide reports a red-tint issue with one FP8 build — [AIStudyNow Qwen-Image-2512 workflow](https://aistudynow.com/qwen-image-2512-comfyui-workflow/)
- Speed LoRAs (not realism): [lightx2v/Qwen-Image-2512-Lightning](https://huggingface.co/lightx2v/Qwen-Image-2512-Lightning); [Wuli-art/Qwen-Image-2512-Turbo-LoRA](https://huggingface.co/Wuli-art/Qwen-Image-2512-Turbo-LoRA) (via [Scrapbox](https://scrapbox.io/work4ai/Qwen-Image-2512))
- A Qwen-Image-Edit skin retouch LoRA ("enhances pores and tonal variation"; trained for Edit-2509): [Replicate qwen-image-edit-plus-lora-skin](https://replicate.com/qwen/qwen-image-edit-plus-lora-skin); [HF tlennon-ie/qwen-edit-skin](https://huggingface.co/tlennon-ie/qwen-edit-skin)

*Qwen-Image-2.1*
- **"Qwen-Image 2.1 Glamour Realism LoRA"** (Civitai, Oct 5, 2026): "natural-looking skin and photographic colour"; suggested strength **0.6**; 2,000 training steps; 214 reviews / 369 likes. The page is likely [Civitai 2986100](https://civitai.com/models/2986100) (link from the same result set, not confirmed)
- **WarmBloodAban Qwen2.1_Anything2RealCharacters** (edit model, late Sept 2026): turns any art style into a realistic human while keeping pose and framing — [comfyui-wiki news 2026-09-27](https://comfyui-wiki.com/en/news/2026-09-27-qwen-image-2-1-loras)

*FLUX.2 [klein] / [dev]*
- **Flux2-Klein-9B-True-V2** (wikeeyang): a community **full fine-tune** (not a LoRA) of FLUX.2-klein-9B, released **July 1, 2026**. Claims gains in realism, texture fidelity, prompt adherence and LoRA compatibility, "near-Nano-Banana realism"; >187k downloads — [comfyui-wiki news](https://comfyui-wiki.com/en/news/2026-07-01-flux2-klein-9b-true-v2-news)
- **Klein-enhance realistic skin texture v1.1** (FLUX.2-klein-9B portrait skin adapter) — [RunningHub](https://www.runninghub.ai/model/public/2060355823880200193)
- **Flux2-Klein-9B Enhanced Details LoRA** in img2img/edit mode at **0.5–0.8**, with a negative prompt against plastic or over-smoothed skin (Mar 2026, single author) — [Civitai article 27526](https://civitai.com/articles/27526); also [AIStudyNow: fix plastic skin in Klein 9B](https://aistudynow.com/how-to-fix-the-plastic-skin-bug-in-flux-2-klein-9b-enhance-realism/) (claims an exact 16-step setting; unverified)
- **fal FLUX.2 Realism LoRA** (hosted; "skin texture authenticity over stylized outputs"; base model not stated) — [fal flux-2-lora-gallery/realism](https://fal.ai/models/fal-ai/flux-2-lora-gallery/realism)
- **Stacking rule of thumb [legacy, FLUX.1 era]:** each LoRA at 0.4–0.8, total under about 2.0 — [PromptZone](https://www.promptzone.com/tara_suzuki/best-flux-loras-in-2026-for-realism-and-how-to-stack-them-1mck)
- **[legacy FLUX.1-dev]:**
  - CSBW "amateur cell phone" LoRA "significantly reduces the plastic, blurred look of Flux Dev" (fetched GitHub) — [RES4LYF README](https://github.com/ClownsharkBatwing/RES4LYF); file at [HF ClownsharkBatwing/CSBW_Style](https://huggingface.co/ClownsharkBatwing/CSBW_Style/blob/main/amateurphotos_1_amateurcellphonephoto_recapt2.safetensors)
  - boreal-flux-dev-v2 (trigger "photo", reduced strength) — [PromptLayer](https://www.promptlayer.com/models/boreal-flux-dev-v2)
  - UltraRealistic LoRA V2 ("amateurish photo", "GoPro lens") — [RunComfy](https://runcomfy.com/comfyui-workflows/flux-ultrarealistic-lora-v2-lifelike-ai-images)
  - Flux.1 "guidance below 2 for realistic skin" (anecdotal) — [ComfyAI Flux.2 settings](https://comfyai.run/documentation/Flux.2%20Settings) (search summary)

*FLUX 3 Image Klein*
- No realism LoRAs were found as of Oct 25, 2026. The model was released Oct 15, 2026 (see file 01).

**C. Samplers, schedulers and sigma tricks**
- **RES4LYF (fetched GitHub):**
  - "Typically only 20 steps are needed with RES samplers";
  - samplers ending in "s" use substeps, so `res_2s` costs 2 model calls per step and is about 2× slower than Euler, but "the increase in accuracy can be very dramatic, especially when using noise (SDE sampling)";
  - the `res` family are "refinements of the dpmpp family";
  - ClownsharKSampler defaults: **`res_2m`**, scheduler **`beta57`** (beta with alpha 0.5, beta 0.7), **eta 0.5**;
  - with Flux guidance set CFG to 1.0; with de-distilled models, CFG 3.0;
  - the README has a "KILL FLUX BLUR" anti-blur feature;
  - the **`bong_tangent`** scheduler is registered in the code (`sigmas.bong_tangent_scheduler`).

  — [RES4LYF README](https://github.com/ClownsharkBatwing/RES4LYF); [RES4LYF __init__.py](https://github.com/ClownsharkBatwing/RES4LYF/blob/main/__init__.py)
- A user pairing **res_2m + bong_tangent** (RES4LYF) on Wan reports "the level of detail is surprisingly WAY better" than the built-in samplers (feature request, not a benchmark) — [GitHub kijai/ComfyUI-WanVideoWrapper #877](https://github.com/kijai/ComfyUI-WanVideoWrapper/issues/877) (search summary)
- **Z-Image-Turbo skin sampler consensus** (search summary):
  - **DPM++ SDE + Beta** is "the best sampling setting for detail" (Reddit commenter), at about double the cost;
  - DPM++ SDE / DDIM Uniform gives a "slightly more natural appearance and better detail";
  - Euler Ancestral is "softer on fine detail like hair strands and skin texture";
  - `res_2m` + beta (ClownsharKSampler default) is a solid all-rounder;
  - res_multistep (template default) is fast but not rated best for skin.

  — [Reddit snapshot](https://reddit.sentinel-team.org/posts/1rwvtgy/snapshots/2026-03-20T17%3A36%3A49.07391Z); [LoRAtech Patreon: ClownsharKSampler vs KSampler for Z-Image Turbo & Klein](https://www.patreon.com/LoRAtech/posts/clownsharksample-164443476); [Diffusion Doodles Z-Image Turbo](https://diffusiondoodles.substack.com/p/z-image-turbo-fast-and-functional); [StableDiffusionTutorials base vs turbo](https://www.stablediffusiontutorials.com/2026/02/zimagebase-vs-zimageturbo.html)
- **Detail Daemon (fetched GitHub):**
  - lowers the noise removed per step to add detail and "possibly remove unwanted bokeh or background blurring, particularly with Flux… also works with SDXL, SD1.5, Qwen, Z-Image";
  - "If the values are taken too far it results in an oversharpened and/or HDR effect";
  - `detail_amount` "for Flux or Z-Image models… between 0.1–1.0 range, or higher; for SDXL… less than 0.25"; `start` 0.1–0.5; `end` 0.5–0.9;
  - **Multiply Sigmas** factor 0.95–0.99 (lower = more detail, but risks composition change and grain);
  - **Lying Sigma** `dishonesty_factor` −0.1 to −0.01 (−0.05 ≈ detail_amount 0.5);
  - works natively with `SamplerCustomAdvanced` (KSampler needs a Bleh preset).

  — [Jonseed/ComfyUI-Detail-Daemon README](https://github.com/Jonseed/ComfyUI-Detail-Daemon)
- The repo's **Z-Image txt2img example** uses Z-Image-Turbo Q8 GGUF, euler/simple, 8 steps, CFG 1, ModelSamplingAuraFlow shift 5, 1280×1024, Detail Daemon widget values `[2, 0, 1, 0.5, 3, …]`. Read with the node's input order (detail_amount, start, end, bias, exponent), that is detail_amount 2.0, start 0, end 1, bias 0.5, exponent 3. This is a demo, not a recommendation (fetched GitHub) — [Z-Image txt2img-DetailDaemon.json](https://github.com/Jonseed/ComfyUI-Detail-Daemon/blob/main/example_workflows/Z-Image%20txt2img-DetailDaemon.json)

**D. Two-pass / hires refinement for skin**
- **Z-Image-Turbo (NextDiffusion):** 8-step base → model upscale (**4x-UltraSharp** or **4xFaceUpDAT**) → second KSampler at **denoise 0.3** (stay within 0.2–0.4; <0.2 changes little, >0.4 alters the image) with a skin prompt ("skin texture, skin pores, natural sunlight on the face") (search summary) — [NextDiffusion Z-Image Turbo upscaler & detailer](https://www.nextdiffusion.ai/tutorials/z-image-turbo-upscaler-and-detailer-workflow-in-comfyui)
- **Latent upscale + resample (Diffusion Doodles):** doubles generation time; a 1800×2400 output had skin "more realistic than the single sample version"; a latent upscale *with* an upscale model "frequently created issues" (search summary) — [Diffusion Doodles](https://diffusiondoodles.substack.com/p/z-image-turbo-fast-and-functional)
- **Official Comfy Z-Image-Turbo 2K upscaler template:** lower denoise stays closer to the original, higher denoise adds creative detail (search summary) — [comfy.org workflow](https://comfy.org/workflows/utility_z_image_turbo_2k_upscaler.app-b3bbbf217b89/)
- Detail Daemon also ships Flux img2img and upscale example workflows (fetched GitHub) — [Detail Daemon README](https://github.com/Jonseed/ComfyUI-Detail-Daemon)
- Tile-upscale denoise ranges are already in file 05 (0.2–0.35).

### Inferences
**Recommended "realism profile" per model** (starting points synthesised from the above; render-test before production):

| Model | Base pass | Realism add-ons | Two-pass skin refine | Plastic-skin traps |
|---|---|---|---|---|
| **FLUX.2 [dev]** (non-commercial licence unless BFL licence) | euler/simple (Flux2Scheduler), 20–28 steps, FluxGuidance 3–4 (try 2.5–3 for less contrast; the Flux.1 "<2" tip is legacy), 1–2 MP | fal Realism LoRA (hosted) or a FLUX.2 skin LoRA at 0.5–0.8; Detail Daemon 0.2–0.5 to kill background blur | model-upscale ×1.5–2 → same model img2img denoise 0.2–0.35 | Turbo LoRA (8 steps): validate skin against 20 steps before using for hero shots |
| **FLUX.2 [klein] 9B base** (non-commercial) / **4B base** (Apache 2.0) | euler/simple, 20–24 steps, CFG 3.5–5 | **True-V2 fine-tune** (9B) or the Enhanced-Details / skin LoRA at 0.5–0.8 | denoise 0.25–0.35 | **distilled 4-step**: never raise steps or CFG; use it only for drafts |
| **FLUX 3 Image Klein** (FLUX Kommunity Licence; free under $5M revenue per file 01) | **base: euler/simple, 50 steps, CFG 3.5**; turn **off** the prompt upsampler for lighting-critical prompts (or review its output) | none yet; an ai-toolkit LoRA trained on your own real photos is the likely route | denoise 0.2–0.35 with the base | distilled 4–16 steps at CFG 1: more steps help up to 16; CFG does not |
| **Qwen-Image-2.1** (research licence; commercial needs an agreement, per file 01) | euler/simple, **40–50 steps** for finals (25 for drafts), **CFG 1** (raise to about 2.5–4 only with a negative prompt); native 2K, multiples of 32 | Glamour Realism LoRA at 0.6 (verify); res_2s/beta57 to cut steps | upscale model → denoise 0.25–0.35 | Turbo (8 steps) and the Lightning 4-step LoRA are for drafts; compare skin before finals |
| **Qwen-Image-2512** | official 50 steps, true CFG 4 | Lenovo/Samsung UltraReal at 0.7–1.0 (phone-camera tone), plus a skin LoRA | denoise 0.25–0.35 | Lightning 4/8-step = documented doll-skin complaints |
| **Z-Image-Turbo** | 8–9 steps, CFG 1, shift 3; for skin try **dpmpp_sde + beta** or **res_2m + beta57** | RealisticSnapshot LoRA 0.6–0.7 (amateur, flash, high-ISO tags); Detail Daemon 0.3–1.0 | 4x-UltraSharp / 4xFaceUpDAT → denoise 0.3 (0.2–0.4) | low seed diversity (file 02); Euler Ancestral softens skin |
| **Z-Image base** | res_multistep/simple, 25–50 steps, CFG 3–5 (4 in the template), shift 3, use a negative prompt | few realism LoRAs; train your own on base | same as Turbo | — |
| **Krea 2 Turbo** (Krea Community Licence; commercial licence by request) | 8 steps, CFG 0/1, mu 1.15, **1280×1600 or 1024–1536 short side** with realism LoRAs (2K without) | Realism LoRA (gokaygokay) at ~0.8–1.0 (weight not documented), realism V1 at 1.0, Inline Skin, Quality Enhancer `hdx_v1` 0.8–1.0. Keep total realism stack ≤ about 1.5: texture smears at 1.5–2.0 on at least one Krea 2 LoRA | Turbo img2img at low denoise (not documented for Krea 2; test) | prompt enhancer on by default; RAW alone is "not tuned for final-quality generation" |

**General rules**
- **Distilled/turbo models:** keep the documented step count. Distilled FLUX.2 Klein degrades above 4 steps. FLUX 3 Klein distilled goes up to 16 steps. Turbo LoRAs are drafting tools. Final avatar renders go through the undistilled base (or a real-photo-trained LoRA) plus a low-denoise refine.
- **Sigma/detail tools:** Detail Daemon or Multiply Sigmas fix the "background melted into bokeh + waxy skin" look. Overdoing them gives the HDR/oversharpened look, which is itself an AI tell, so cap `detail_amount` around 0.5 for faces and inspect at 100%.
- **Higher-order samplers:** they let you cut steps (RES ~20) but cost 2× per step for `2s`. Use `res_2s` + `beta57`/`bong_tangent` for finals and `res_2m`/euler for exploration.

### Gaps
- Civitai and Hugging Face pages could not be opened. Weights, triggers and dates above come from search summaries and must be re-verified on each page (especially Civitai 2986100 and the CivArchive Samsung page).
- No 2026 side-by-side skin test was found for res_2s/bong_tangent vs euler/simple on Qwen-Image-2.1, FLUX 3 Klein or Krea 2.
- No realism LoRA for **FLUX 3 Image Klein** or **Z-Image base**, and no confirmed Qwen-Image-2512-specific UltraReal version, was found.
- The recommended weight for the gokaygokay Krea-2 Realism LoRA and the Inline Skin LoRA was not found.
- FLUX 3 Image Klein maximum native resolution was not found (the template defaults to 1 MP).

---

## 5. Midjourney V8.x realism parameter recipes (--raw, --stylize, --exp, personalization/moodboards, --hd)

### Takeaway
- **Official docs establish only two things:**
  - `--raw` turns off Midjourney's "auto-pilot" styling, and "simple prompts often give more realistic, photo-like images";
  - `--stylize` defaults to 100 (range 0–1000).
- **V8.2 (default since July 24, 2026) is more stylised** than V8.1: "more creative and edgy", with more contrast, dramatic lighting and bolder grading. Midjourney itself pushes personalization and high stylize, which is the opposite of what realism needs.
- **Practitioner recipe for realistic people:** `--raw`, `--stylize` low (≈50–150; some guides 0–250), `--exp` off or ≤10–25, personalization off (or a profile trained only on candid photos), an optional moodboard of real phone photos, and `--hd` for native 2K.
- No tested V8.2 people-specific recipe was found.

### Cited Findings
- **Official (docs.midjourney.com, via search summary):**
  - Raw "turns off Midjourney's default 'auto-pilot' styling. Simple prompts often give more realistic, photo-like images", is compatible with V5.1+, and can be set as a default in settings — [Midjourney docs: Raw/Style](https://docs.midjourney.com/docs/style)
  - Stylize: "default value for stylize is 100, and you can adjust it anywhere between 0 and 1000 with the current model versions" — [Midjourney docs: Stylize](https://docs.midjourney.com/docs/stylize)
  - The Moodboards page still says compatible with V6 and V7, and not with `--sv`/`--sw` (possibly outdated). Third-party V8 coverage says moodboards default to `--sv 7` and work with `--hd`, personalization, `--stylize` and `--exp` (conflict) — [Midjourney docs article](https://docs.midjourney.com/hc/en-us/articles/39193335040013); [Heather Cooper: V8 alpha](https://heatherbcooper.substack.com/p/midjourney-v8-is-live-on-alpha-heres)
- **V8 alpha announcement and coverage:**
  - V8 leans on the personalization profile more than the text, and Midjourney recommended "crank --stylize up to 1000" (aesthetic advice, not realism);
  - "for photorealistic or controlled output: switch to --raw immediately, or anchor the aesthetic with a moodboard or sref";
  - supported: `--chaos`, `--weird`, `--exp`, `--raw`, `--hd`, `--q 4`.

  (search summary) — [Heather Cooper substack](https://heatherbcooper.substack.com/p/midjourney-v8-is-live-on-alpha-heres); [Midjourney updates: V8 alpha](https://updates.midjourney.com/v8-alpha/)
- **V8 family "executes prompts literally"**, so precise lighting, medium and composition language matters more (search summary) — [Blake Crosley: V8 vs V7 prompt anatomy](https://blakecrosley.com/blog/midjourney-v8-vs-v7-prompt-anatomy); [Blake Crosley: V8 prompting](https://blakecrosley.com/blog/midjourney-v8-prompting)
- **V8.2:**
  - default since July 24, 2026; "more creative and edgy", "a stronger point of view";
  - personalization reads taste signals better;
  - "leans toward more contrast, dramatic lighting, and bolder color grading";
  - fix older settings by "dialing stylize down 50–100 points from your old default".

  (search summary) — [Medium: V8.2 default](https://medium.com/@inchristiely/midjourney-v8-2-is-now-the-default-five-things-that-changed-30c8dffcc492); [Vidmuse V8.2 guide](https://vidmuse.ai/blog/midjourney-8-2); [Tech-Insider V8.2 how-to](https://tech-insider.org/how-to-use-midjourney-v8-2-2026/)
- **Plastic look:** a common complaint is that V8 "defaults to an almost too-clean, hyper-polished look". V8.1 reportedly adjusted the default aesthetic, and raw "now works to strip styling" (search summary) — [MindStudio V8 alpha strengths/weaknesses](https://www.mindstudio.ai/blog/what-is-midjourney-v8-alpha-strengths-weaknesses); [ud.hk V8.1 guide](https://ud.hk/en/blogs/insight/article/2026-05-13-midjourney-v81-power-guide)
- **Stylize ranges from guides (conflicting):**
  - 50–150 for photorealism ("high values tend to add an artificial look"), raw + low stylize for maximum control — [MindStudio: best results V8](https://www.mindstudio.ai/blog/how-to-get-best-results-midjourney-v8);
  - 0–250 "realistic style, faithful to the prompt", 250–750 balanced, 750–1000 strong artistic (vendor parameter guide) — [Temperstack](https://www.temperstack.com/learn/midjourney/master-stylize-parameters/);
  - an older pre-V8.2 guide suggested 500–750 for realism — [Dupple](https://dupple.com/tutorial/create-photorealistic-images-with-midjourney-in-5-steps);
  - "test the same prompt at 50, 200 and 500" — [MindStudio](https://www.mindstudio.ai/blog/how-to-get-best-results-midjourney-v8);
  - file 01 also cites stylize 50–150 + `--raw` from Prompt Architects, Blake Crosley and Geeky Gadgets.

  (all search summary)
- **`--exp`:**
  - integer 0–100, default 0, an aesthetic effect combinable with stylize — [Evolink V8.2 prompt guide](https://evolink.ai/docs/en/api-manual/image-series/midjourney/midjourney-v8-2-prompt-guide.md);
  - V7-era suggested test values 5/10/25/50/100, with the effect changing sharply from 5 to 50 — [Medium: --exp overview](https://medium.com/creativity-ai/midjourney-quick-overview-of-the-exp-parameter-d12f0fa80b96);
  - keep ≤25 when combining, since higher values "can overwhelm… stylize and personalization"; in V8.2 the mechanism is undocumented — [Geeky Curiosity](https://geekycuriosity.substack.com/p/what-the-exp-parameter-actually-does).

  No realism-specific `--exp` value was found (search summary).
- **`--hd`:** native 2048×2048, 1.5× GPU billing; inpaint/outpaint on HD drops to standard; `--oref` was replaced on V8.2 by the V8.2 Edit model. Already in file 01 — [Legnext V8.2](https://legnext.ai/midjourney/v82); [Tech-Insider](https://tech-insider.org/how-to-use-midjourney-v8-2-2026/)
- **Photographic default:** V8 "looks more like photographs than illustrations" (pre-V8.2 comparison) (search summary) — [MindStudio V8 vs V7](https://www.mindstudio.ai/blog/midjourney-v8-vs-v7-comparison)

### Inferences
**Copy-paste MJ V8.2 recipes for realistic avatars** (synthesised; test with a fixed `--seed`):
- **Base candid UGC still:**
  `[plain-language photo description with one physical light source, camera/phone, imperfections] --v 8.2 --raw --s 60 --exp 0 --ar 4:5 --hd`
  Leave out `--p`, so no personalization profile is applied (and switch personalization off in settings if it is on by default), or use a profile trained only on candid phone photos. The exact `--v 8.2` syntax and whether personalization is on by default were not verified against official docs.
- **Slightly more polished testimonial/expert:**
  `… --raw --s 120 --exp 5 --ar 4:5 --hd`
- **Look anchoring:** build a **moodboard of 10–30 real, unretouched phone photos** with the desired lighting (window, flash, office fluorescent) and add it as a moodboard/sref at low style weight. This copies capture characteristics (flash falloff, noise, WB) better than adjectives do. Moodboard–V8 compatibility conflicts between sources, so verify in the web app.
- **If V8.2 is still too "edgy"/graded,** switch to `--v 8.1` (still selectable) with the same raw + low-stylize settings. Consider this the realism fallback.
- **Lighting language for MJ:** because V8 executes prompts literally, the Section 2 lexicon phrases apply directly. Avoid "cinematic/dramatic", since V8.2 already leans toward dramatic lighting and grading.

### Gaps
- No official Midjourney page for V8.2 realism, and no community-tested V8.2 recipe for people (with images) was found. Reddit r/midjourney threads did not surface.
- The current official behaviour of moodboards and `--sv` on V8.x is unconfirmed (official page vs blogs conflict).
- No measured effect of `--exp` or `--q 4` on skin texture was found.
- Whether personalization off vs on improves realism in V8.2 is unknown; no source tested it.
