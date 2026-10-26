# Avatar identity consistency, image-to-video and extension (Veo 3.1 Lite on Agent Platform, plus Omni as alternative). State as of 2026-10-26

> **Method and reliability note.** Research date 2026-10-26. Sources used:
>
> **Primary sources read in full (files on disk):**
> - Google's official notebooks in `GoogleCloudPlatform/generative-ai` (HEAD `3567247`, 2026-10-26).
> - `google-gemini/cookbook` (HEAD `5506746`, 2026-10-19).
> - The `googleapis/python-genai` SDK `types.py`.
> - Google's sample app `GoogleCloudPlatform/vertex-ai-creative-studio`, renamed `genmedia-creative-studio` on 2026-09-21 (HEAD `214d4ac`, 2026-10-24). I also read its git history for July–Oct 2026.
> - Two Google Cloud blog posts, fetched in full.
>
> **Search summaries only:** `docs.cloud.google.com`, `ai.google.dev`, `blog.google` and every practitioner site (hackernoon, invideo, atlascloud and others) were blocked or unresolvable, so claims from them are tagged **(search summary)**.
>
> **Tags:**
> - **[OFFICIAL]**: Google product docs, official notebooks or Google Cloud blog.
> - **[GOOGLE-SAMPLE]**: code written by Google engineers in sample apps. This shows how Google builds things, but it is not product documentation.
> - **[PRACTITIONER]** / **[VENDOR]**: third-party sources.
> - **[>6 months]**: older than about late April 2026.
>
> Model facts (IDs, Lite capability matrix, pricing) are in `01_veo_vertex_specs.md` and are not repeated here. In brief: the client's "Veo 3 Lite" is **`veo-3.1-lite-generate-001`**, which is Preview. It supports t2v, i2v, and first+last frame. It does **not** support reference images ("ingredients"). Extension support is **contested**.

---

## 1. Image-to-video from a still avatar (first frame): best practices, and how much identity drifts by second 8

### Takeaway
On Lite, image-to-video (i2v) from the approved master still is the **main identity anchor**. The still becomes the literal first frame. Identity then depends on everything that moves after frame 1, so the prompt should spend its words on **motion and audio**, and the text must not contradict the image.

Google's own tooling makes two moves that matter here:
- It gives the prompt-writing LLM the image itself (multimodal).
- In August 2026 it fixed its rewriter because text-only rewriting "could drift from what the user actually supplied as reference."

Google publishes no measurement of face drift between second 0 and second 8. Treat drift as something to QA per clip, not a known constant.

### Cited Findings
**What i2v does and how Google prompts it**
- [OFFICIAL] The image becomes the literal first frame. In Omni's terms the start image is "Source Media… In image-to-video, the provided image becomes the literal first frame." — [GCP notebook Omni 1.1](https://github.com/GoogleCloudPlatform/generative-ai/blob/main/vision/getting-started/gemini_omni_1_1_flash_video_gen.ipynb)
- [OFFICIAL] The prompt is optional but helps: "If you're generating a video from an image you don't need to provide a prompt… however, a detailed prompt will help with video quality." — [GCP notebook veo3_video_generation](https://github.com/GoogleCloudPlatform/generative-ai/blob/main/vision/getting-started/veo3_video_generation.ipynb)
- [OFFICIAL] Google's i2v prompt optimizer splits the prompt into four motion and audio slots. It does not re-describe the person.
  - **Camera motion**: "the camera movement that occurs while the rest of the scene remains static".
  - **Subject animation**.
  - **Environmental animation**.
  - **Audio**.
  - Its preset micro-motion phrases are: "The subject blinks slowly", "A subtle smile appears on the subject's face", "The subject's head turns slowly", and "The subject's hair and clothes flutter gently in the wind".
  - The meta-prompt sends Gemini the image: "Analyze the provided image and combine its content with the following motion and audio keywords… Integrate the image's subject and scene with the requested motion and audio effects."
  — [GCP notebook veo3_video_generation](https://github.com/GoogleCloudPlatform/generative-ai/blob/main/vision/getting-started/veo3_video_generation.ipynb)
- [GOOGLE-SAMPLE] Google's i2v tips:
  - "Ensure actions and speech descriptions align with the subjects in the image."
  - "If multiple subjects are present, clearly specify who is performing an action (e.g., 'The man in the red hat,' 'The woman in the blue dress')."
  — [veo_guide.md](https://github.com/GoogleCloudPlatform/vertex-ai-creative-studio/blob/main/experiments/veo-genetic-prompt-optimizer/veo_guide.md)

**Text can pull the face away from the image (Aug 2026 fix)**
- [GOOGLE-SAMPLE] On 2026-08-11 a Google engineer committed: "The Veo prompt rewrite button called rewriter(text, VIDEO_REWRITER) with text only, in all image modes… The rewritten prompt could drift from what the user actually supplied as reference." The fix attaches the i2v image (or the first+last frames, or the r2v images) to the rewriter call. It also adds: "If one or more reference images are provided, keep the rewritten prompt consistent with the subjects, setting, and visual details shown in those images." — [commit 27f30b6](https://github.com/GoogleCloudPlatform/vertex-ai-creative-studio/commit/27f30b6d7e03b52a84db3694e26e1ffd11f0b664)
- [GOOGLE-SAMPLE] Google's Veo prompt engineer meta-prompt for image inputs says to identify "every key visual anchor… These elements are non-negotiable. **Crucially, you must repeat these core visual anchors throughout your final prompt to reinforce them and prevent the model from drifting.**" Its example: say "red cup" and "wooden table", not "the cup". — [veo3-character-consistency/prompts.py](https://github.com/GoogleCloudPlatform/vertex-ai-creative-studio/blob/main/experiments/veo3-character-consistency/prompts.py)
- [GOOGLE-SAMPLE] Another Google demo note: "Veo 3.1 is an image/video-to-video model, but it relies heavily on the text prompt for guidance. If the prompt doesn't reiterate the style…, the model might drift." — [run-veo-run continuity_strategy.md](https://github.com/GoogleCloudPlatform/vertex-ai-creative-studio/blob/main/experiments/run-veo-run/docs/continuity_strategy.md)

**Framing, resolution, aspect ratio**
- [OFFICIAL] The SDK has `resize_mode` for the input image: `CROP` ("Crop the image to fit the correct aspect ratio (so we lose parts of the image…)") or `PAD` ("Pad the image… so we don't lose any parts"). An input image whose aspect ratio differs from the output gets cropped or padded. — [python-genai types.py](https://github.com/googleapis/python-genai/blob/main/google/genai/types.py)
- [GOOGLE-SAMPLE] Google's character-consistency pipeline does not feed a mismatched still. It first **reframes the best image to the target aspect ratio** with Nano Banana: "Expand and reframe this image to a 16:9 widescreen aspect ratio… keeping the existing subject unchanged, in-focus, and consistent in identity, lighting, and style. Do not crop, distort, or alter the subject." Only then does it run Veo i2v for 8 s. The item-consistency demo derives `aspect_ratio="9:16" if height > width else "16:9"` from the start image itself. — [models/character_consistency.py](https://github.com/GoogleCloudPlatform/vertex-ai-creative-studio/blob/main/models/character_consistency.py); [extend_video_generator.py](https://github.com/GoogleCloudPlatform/vertex-ai-creative-studio/blob/main/experiments/veo3-item-consistency/extend_video/extend_video_generator.py)
- [VENDOR] Image-to-video guides advise:
  - Match the start frame to the output aspect ratio, or "expect cropping or odd framing".
  - "Your image is just the setup. The prompt controls everything that happens after."
  These are generic and partly outdated (one says 720p and 16:9 only). — [getimg.ai (search summary)](https://getimg.ai/blog/google-veo-3-fast-now-works-with-image-to-video); [Segmind (search summary)](https://blog.segmind.com/veo-3-image-to-video-guide/)

**Drift by second 8**
- I found **no official or independent measurement** of identity drift within one 8 s i2v clip. Search summaries surfaced only general advice. — [search summary of practitioner guides](https://eastondev.com/blog/en/posts/ai/20251207-veo3-long-video-guide/)
- [GOOGLE-SAMPLE] Google's own QA rubric for i2v gives 50% weight to "Image and Prompt Adherence: How accurately does the video animate the subject/scene from the reference image". A further 25% goes to "Visual Quality & Artifacts… distortion, flickering, unnatural textures, or object morphing". So Google treats drift away from the start image as an evaluation problem, not as a solved one. — [veo_video_eval_templates.py](https://github.com/GoogleCloudPlatform/vertex-ai-creative-studio/blob/main/experiments/veo-genetic-prompt-optimizer/veo_genetic_prompt_optimizer/veo_video_eval_templates.py)

### Inferences
- **Start-frame spec for talking UGC avatars:**
  - Generate the start frame **natively at the output aspect ratio** (9:16 for Reels/TikTok) and at least at output resolution (1080×1920 for 1080p). Then CROP/PAD never touches the face.
  - The face should be frontal or a slight three-quarter view, eyes open, **mouth closed or neutral**, in soft even light, with the hands visible and relaxed or out of frame.
  - This follows from the official advice that motion is driven from the frame, and from the observation that faces under extreme pose or expression are harder to hold.
  - A posed mid-speech frame (open mouth, teeth) forces Veo to invent the closing motion. A neutral start gives the lip-sync room. Treat this as an inference to A/B test.
- **Jarvis must be multimodal:** always send Jarvis the avatar still together with the script, the way Google's official i2v optimizer does. Instruct it to describe only what matches the image. A text-only Jarvis that invents "a brunette with green eyes" for a hazel-eyed avatar is the exact drift that Google's August 2026 fix addresses.
- **What the prompt should say about the face:** do not re-describe the face from scratch. Do repeat 3–4 hard anchors that are visible in the frame (hair colour and cut, a mole, glasses, garment colour), word for word. This reconciles the two official patterns: motion-focused i2v, and "repeat the visual anchors".
- **Seconds 6–8 are the riskiest:**
  - Prefer 6 s or 8 s clips with **one** action and one line.
  - Avoid head turns past about 45°, hands crossing the face, and fast camera moves. These are generic diffusion failure modes: occlusion and profile views make the model re-imagine the face.
  - This is inference only; no Veo-specific measurement exists.

### Gaps
- No published identity-similarity curve (for example ArcFace cosine per frame) for Veo 3.1 Lite i2v.
- No official recommended input resolution or format for the start image beyond PNG/JPEG examples. Whether a JPEG-compressed start frame degrades skin in motion is untested.

---

## 2. Reference images ("Ingredients to video" / asset references): how many, which views, how to label them, and is it on Lite?

### Takeaway
Veo 3.1 and Veo 3.1 Fast accept **up to 3 `asset` reference images**, or 1 `style` image. Output is **8 s only**, and since January 2026 it can be **portrait 9:16**. The feature is **not available on Veo 3.1 Lite**.

References cannot be combined with a start frame, a last frame, or an extension video in the same call. Google's prompt pattern names the roles in plain words ("Using the provided images for the detective, the woman, and the office setting…"). There is no numbered tag syntax on Veo; numbered `<IMAGE_REF_n>` tags exist only on **Gemini Omni**.

For which views to supply, Google's own apps build a **multi-view character sheet** (front, side or profile, three-quarter, back, close-up face) from one approved photo.

### Cited Findings
- [OFFICIAL] Agent Platform notebook:
  - "You can include up to 3 `asset` images in a request." Duration "8 seconds", resolution 720p/1080p/4k, aspect 16:9 or 9:16.
  - "Reference-to-Video functionality on Veo 3.1 is optimized for high-energy, short-form narratives. It excels at maintaining consistency across rapid intercutting and dynamic camera transitions."
  - Its first example passes **two people as two asset images**, with a plain prompt: "a woman and a man drinking a cup of coffee in a cafe, chatting about the new restaurant around the block". There are no labels in the prompt. Further examples use a product (vase) and "three distinct reference images (a product, a subject, and a scene)".
  - Models used: `veo-3.1-generate-preview` and `veo-3.1-fast-generate-preview`.
  — [veo3_reference_to_video](https://github.com/GoogleCloudPlatform/generative-ai/blob/main/vision/getting-started/veo3_reference_to_video.ipynb)
- [OFFICIAL] SDK rules:
  - `reference_images`: "If this field is provided, the text prompt field must also be provided. **The image, video, or last_frame field are not supported.** Each image must be associated with a type."
  - Types: `ASSET` ("the scene, an object, a character") and `STYLE` ("colors, lighting, texture").
  - `last_frame`: "Only supported for image to video use cases."
  — [python-genai types.py](https://github.com/googleapis/python-genai/blob/main/google/genai/types.py)
- [OFFICIAL] **Conflict:** the Gemini API cookbook says references-to-video is "only available using Veo 3.1 (not Fast) and in 720p and landscape (16:9)". The Agent Platform notebook shows Fast, 9:16 and 1080p/4k. The cookbook cell likely predates the January 2026 update. — [cookbook Get_started_Veo](https://github.com/google-gemini/cookbook/blob/main/quickstarts/Get_started_Veo.ipynb)
- [OFFICIAL, search summary] The **January 13, 2026** Ingredients update:
  - Makes outputs "more expressive even with simple prompts".
  - Claims characters keep "the same appearance as settings change across multiple scenes", with background and object details steady.
  - Adds native 9:16 and upscaling to 1080p and 4K.
  - Is available in the Gemini app, YouTube, Flow, Vids, the Gemini API and Vertex AI.
  Ars Technica, via the same summary, called the reduced random alterations something the model "will allegedly" do. No independent benchmark was found. — [blog.google, 2026-01-13 (search summary)](https://blog.google/innovation-and-ai/technology/ai/veo-3-1-ingredients-to-video/); [YourStory (search summary)](https://yourstory.com/ai-story/google-veo-3-1-ingredients-to-video-update); [PetaPixel (search summary)](https://petapixel.com/2026/01/19/google-veo-3-1-updates-promise-even-more-realistic-ai-generated-video)
- [OFFICIAL] [>6 months] Google's dialogue-scene workflow with ingredients names each reference by role in every shot prompt:
  - "Using the provided images for the detective, the woman, and the office setting, create a medium shot of the detective behind his desk. He looks up at the woman and says in a weary voice, "Of all the offices in this town, you had to walk into mine.""
  - Next shot: "…create a shot focusing on the woman… she replies, "You were highly recommended.""
  — [Google Cloud blog: Ultimate prompting guide for Veo 3.1](https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-veo-3-1)
- [OFFICIAL] **Not on Lite:** the Agent Platform Veo 3.1 page says "Use reference images: Not supported" for `veo-3.1-lite-generate-001` (search summary). Google's sample-app matrix gives Lite no `r2v` mode. See `01_veo_vertex_specs.md` §2. — [config/veo_models.py](https://github.com/GoogleCloudPlatform/vertex-ai-creative-studio/blob/main/config/veo_models.py)
- [GOOGLE-SAMPLE] Which views, per Google's sample apps:
  - The character-sheet page prompt: "Character sheet of this character, white background, multiple views: front, back, side, three-quarter, close-up face. Consistent style. High quality, detailed. Retain realism of original image." Each scene then uses "…Use the provided character sheet and reference image to ensure character consistency." — [pages/character_sheet.py](https://github.com/GoogleCloudPlatform/vertex-ai-creative-studio/blob/main/pages/character_sheet.py)
  - The Storyboarder prompt: "Multi-view Character asset sheet, white background, 4 views: front, back, profile, three-quarters." The sheet plus the original photo are passed as references to Nano Banana for **every storyboard keyframe**, and each keyframe is then animated with Veo i2v. — [pages/storyboarder.py](https://github.com/GoogleCloudPlatform/vertex-ai-creative-studio/blob/main/pages/storyboarder.py)
- [OFFICIAL] **Omni alternative** (Gemini Omni 1.1 Flash, Preview):
  - "In Reference-to-Video workflows, the provided image is **not** used as the literal starting frame. Instead, the model extracts the subject, character identity…"
  - Tags: `<FIRST_FRAME>` "Binds the image as the exact opening frame" and `<IMAGE_REF_0>`, `<IMAGE_REF_1>`… "Binds images (0-indexed matching the order in `input`) to specific character identities, objects, or wardrobe items".
  - The demo bound 3 characters and 3 accessories "without blending identities".
  — [cookbook Get_started_Omni](https://github.com/google-gemini/cookbook/blob/main/quickstarts/Get_started_Omni.ipynb)
  - Agent Platform: "we recommend supplying no more than 5 reference images and 3 reference videos"; "Audio reference inputs are not currently supported." — [GCP notebook Omni 1.1](https://github.com/GoogleCloudPlatform/generative-ai/blob/main/vision/getting-started/gemini_omni_1_1_flash_video_gen.ipynb)
- [PRACTITIONER] Curate up to three references "that match lighting, palette, and camera angle" (search summary). — [RunDiffusion](https://learn.rundiffusion.com/google-new-veo-3-1-model)

### Inferences
- **For Lite, the ingredients feature does not exist.** Use the reference-image idea **one step earlier**, at keyframe creation. Keep a master still plus a multi-view sheet per avatar, as in the existing image SOP's "identity pack". Generate each new shot's start frame with Nano Banana from that pack, check the face (ArcFace, per the still SOP), and only then animate it with Lite i2v. This is exactly Google's Storyboarder and Character-Consistency pattern, and it needs no r2v.
- **When to pay for Fast or Standard r2v instead of Lite:** use it for shots with **two people together**, product-in-hand shots where the label must survive motion, or rapid multi-angle intercuts. Budget: 3 assets maximum (for example avatar A, avatar B, set; or avatar, product, set), 8 s only. Price per `01_veo_vertex_specs.md`: Fast at 1080p with audio is $0.12/s, against $0.08/s for Lite.
- **Labeling roles on Veo r2v:**
  - Refer to each image by a short, stable role noun plus one visual descriptor, every time: "the provided image of the woman in the mustard sweater".
  - Give each reference image a single subject on a plain background. A sheet with several views of one person may be read as several people. This is an untested inference, so A/B a single hero portrait against a 4-view sheet as one asset.
- **On Omni,** use `<IMAGE_REF_n>` tags per character, plus a fixed order of inputs.

### Gaps
- No official guidance on whether a multi-view sheet or a single portrait works better as one Veo `asset` image.
- The Lite launch stage and any plan to add r2v to Lite are unknown.
- I could not read the January 2026 blog verbatim. The footnote conditions on 4K were not visible.

---

## 3. First+last frame interpolation, and chaining (last frame of clip N becomes the first frame of clip N+1): quality loss, drift, better alternatives

### Takeaway
First+last frame **is** on Lite. Google says it "tends to work best when the starting and ending frames are similar in nature". You cannot give only an end frame.

Chaining clips by reusing the previous clip's last frame **compounds drift**. Practitioners report the character no longer matches clip 1 by about the **3rd–4th hop**. They also report a stutter at every cut, because generators slow the camera near clip end.

Google's own continuation demo uses a better pattern. It takes the **last ~4 frames**, picks the best pose with Gemini, describes the character **from the original reference image** ("absolute ground truth"), reframes, and only then runs a fresh 8 s i2v.

The strongest Lite-compatible pattern is **re-anchoring every clip to the master identity**. Two variants: (a) new start keyframes derived from the master still, or (b) "bookending" with a master-derived last frame. Variant (b) is an untested inference.

### Cited Findings
- [OFFICIAL] "This feature tends to work best when the starting and ending frames are similar in nature." The end frame is passed as `config.last_frame`. — [veo3_advanced_controls](https://github.com/GoogleCloudPlatform/generative-ai/blob/main/vision/getting-started/veo3_advanced_controls.ipynb)
- [OFFICIAL] "You cannot use only an ending image, you always need to also add a starting one." — [cookbook Get_started_Veo](https://github.com/google-gemini/cookbook/blob/main/quickstarts/Get_started_Veo.ipynb)
- [OFFICIAL] Google's MCP veo server lists first+last as `SupportsFirstLast: true` for Lite. — [mcp-common/models.go](https://github.com/GoogleCloudPlatform/vertex-ai-creative-studio/blob/main/experiments/mcp-genmedia/mcp-genmedia-go/mcp-common/models.go)
- [OFFICIAL] [>6 months] Google's first+last example is a camera move between two different points of view of the same singer: "The camera performs a smooth 180-degree arc shot…", with sung dialogue in quotes. — [Cloud blog prompting guide](https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-veo-3-1)
- [GOOGLE-SAMPLE] **Google's own continuation pipeline** (veo3-item-consistency `extend_video`):
  1. `extract_last_frames(video_path, num_frames=4)`.
  2. Gemini profiles each frame and the original character image (temperature 0.1).
  3. Gemini chooses "the best single frame to serve as the starting point for the next action".
  4. Gemini writes a prompt where "The character in the prompt must match the Primary Character Description" taken from the reference image.
  5. The chosen frame is outpainted or reframed.
  6. A new **8 s i2v** runs with `enhance_prompt=True`.
  The Veo meta-prompt states: "The Character Image… is the absolute ground truth for the character's appearance… The character in the final video must look exactly like the person in this image… You must repeat the key visual anchors from both images… throughout your prompt… to prevent the model from drifting." — [extend_image_generator.py](https://github.com/GoogleCloudPlatform/vertex-ai-creative-studio/blob/main/experiments/veo3-item-consistency/extend_video/extend_image_generator.py); [extract_frame.py](https://github.com/GoogleCloudPlatform/vertex-ai-creative-studio/blob/main/experiments/veo3-item-consistency/extend_video/extract_frame.py); [prompts.py EXTEND_VIDEO_PROMPT](https://github.com/GoogleCloudPlatform/vertex-ai-creative-studio/blob/main/experiments/veo3-item-consistency/prompts.py)
- [GOOGLE-SAMPLE] Google's character pipeline goes further. It never chains from a previous clip: it generates the person into each new scene from reference photos, picks the most look-alike candidate, reframes, and runs i2v. A structured "FacialCompositeProfile" (see §5) drives it. — [veo3-character-consistency README](https://github.com/GoogleCloudPlatform/vertex-ai-creative-studio/blob/main/experiments/veo3-character-consistency/README.md); [models/character_consistency.py](https://github.com/GoogleCloudPlatform/vertex-ai-creative-studio/blob/main/models/character_consistency.py)
- [PRACTITIONER, search summary] Drift compounds when chaining last frames: "Errors stack, and by about the third or fourth clip the character no longer matches clip one." The fix is to "Re-anchor each segment to the original character sheet and location references rather than relying only on the previous frame." — [invideo FAQ: fix character drift](https://invideo.io/faq/how-do-you-fix-character-drift-when-chaining-ai-video/); [invideo FAQ: reference-to-video vs start/end chaining](https://invideo.io/faq/reference-to-video-vs-startend-frame-chaining-which/)
- [PRACTITIONER, search summary] Further reports:
  - The mechanism is partly exposure bias, because the model conditions on its own generated frames.
  - A last frame "carries only a still image, so camera movement, lighting, and spatial logic get re-derived each time".
  - Frame-chaining causes a "stutter at each cut, because generators decelerate the camera at clip end. Matching the frame doesn't fix that."
  - One documented production "averaged about three generations per usable shot."
  — [Hackernoon: extend without drift](https://hackernoon.com/how-to-extend-an-ai-generated-video-clip-past-its-length-limit-without-the-drift); [Hackernoon: chain clips without stutter](https://hackernoon.com/how-to-chain-ai-video-clips-into-one-shot-without-the-hidden-stutter-at-every-cut); [Oakgen: extension quality loss](https://oakgen.ai/blog/ai-video-extension-quality-loss)
- [PRACTITIONER] A Hugging Face model, "depth-nano", estimates how many generations a frame sits from a real anchor, so a pipeline can decide when to re-anchor (search summary; I did not evaluate it). — [huggingface resoajoe/depth-nano](https://huggingface.co/resoajoe/depth-nano)
- [VENDOR, search summary] Using the **same image as first and last frame** for a loop:
  - Adobe's community manager calls it "only a workaround… can still lead to issues". A user hit a "generic error" doing it on Veo 3.1 Fast.
  - getimg.ai recommends it for looping posts.
  - Neither reports identity measurements.
  — [Adobe community thread](https://community.adobe.com/bug-reports-403/generic-error-when-using-two-reference-frames-for-video-looping-in-veo-3-1-fast-1553443); [getimg.ai Veo 3.1 review](https://getimg.ai/blog/google-veo-3-1-review)
- [OFFICIAL] Output compression is selectable: `compression_quality` `OPTIMIZED` ("compressed, smaller file size") or `LOSSLESS` ("larger file size"). — [python-genai types.py](https://github.com/googleapis/python-genai/blob/main/google/genai/types.py)

### Inferences
**Ranking for the client (Lite), best first:**
1. **Re-anchored keyframes.** Every clip starts from a fresh keyframe made from the master identity pack (Nano Banana edit, then ArcFace check). Never start from a drifted video frame. Drift then cannot accumulate across clips, because each clip is at most "1 hop" from the master. This is the Google Storyboarder/Character-Consistency pattern.
2. **Bookending for continuous takes** (first + last frame, both on-model). Use it when the same take must continue across a cut:
   - First frame = the best of the last ~4 frames of clip N, picked as Google does. Use it only if its ArcFace against the master passes.
   - Last frame = a master-derived keyframe of the end pose.
   - Clip N+1 is then forced to *end* on-model, so clip N+2 starts clean. This is untested. Google notes first+last works best when the frames are "similar in nature", so keep the pose change small.
3. **Plain last-frame chaining.** Limit it to 1–2 hops, and only when the ArcFace and visual check on the handoff frame passes.

**If you must chain from video frames:**
- Request `compression_quality=LOSSLESS`.
- Decode with ffmpeg to PNG. Never screenshot the player or re-encode to JPEG.
- Pick from the last 4 frames, avoiding blink or motion-blur frames, as Google's `extract_last_frames(…, num_frames=4)` + "select best frame" step does.
- These steps follow from the cited compression option and Google's sample. The size of the quality gain is untested.

**To hide the cut stutter** (deceleration at clip end):
- Cut on action, or cut to a different shot size (medium, then close-up). Do not try to make one invisible "continuous" take from several clips.
- Script each clip as a self-contained beat that ends on a natural pause. This also suits ad editing.

### Gaps
- No Google statement on drift or quality loss for last-frame chaining, or on whether Veo applies any temporal context beyond the single first frame in i2v.
- No measured data on the "same frame as first and last" talking-head loop (mouth motion with both ends pinned).

---

## 4. Veo scene/video extension: mechanism, max length, drift after N extensions, voice continuity

### Takeaway
Veo extension appends a **7 s** continuation to a Veo-generated clip. The Gemini API (search summary) says it is conditioned on the **final second (24 frames)**. The Gemini API caps the total at about **148 s**, roughly 20 hops, with 720p input. Vertex (search summary) accepts **1–30 s MP4 at 24 fps, 720p or 1080p** and outputs **7 s at 720p**.

The extension call **cannot take an image**, so you cannot re-anchor identity during extension. Only the text prompt and the last frames guide it.

Voice carries over only if **speech is present in the final second** (Gemini API, search summary). Practitioners say identity holds for about **3–4 hops** before you should re-anchor with a fresh i2v.

Lite extension is contested: current Vertex docs and Google's sample app say yes (7 s), while the older Gemini API page says no. Omni 1.1 Flash is the documented alternative, adding up to 10 s per call with dialogue in multi-turn.

### Cited Findings
- [OFFICIAL] The Vertex notebook extends with `video=types.Video(uri=gs://…, mime_type="video/mp4")`, `duration_seconds=7`: "You can extend your video by 7 seconds." The model is `veo-3.1-generate-preview`. — [veo3_advanced_controls](https://github.com/GoogleCloudPlatform/generative-ai/blob/main/vision/getting-started/veo3_advanced_controls.ipynb)
- [OFFICIAL] SDK: `video` is "The input video for video extension use cases. Optional if prompt is provided. **Not allowed if image is provided.**" Reference images are also not allowed with `video`. — [python-genai types.py](https://github.com/googleapis/python-genai/blob/main/google/genai/types.py)
- [OFFICIAL, search summary] Vertex extend page:
  - Input MP4, 1–30 s, 24 fps, 720p or 1080p.
  - Output "fixed at 7 seconds, at 24 frames per second and 720p".
  - Models listed: `veo-3.1-generate-preview` and `veo-3.1-fast-generate-preview`.
  — [Extend Veo on Vertex AI-generated videos (search summary)](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/video/extend-a-veo-video)
  - Google's MCP server: "The input video must be MP4, 1-30s, 24fps, and 720p/1080p/4k in 16:9 or 9:16. Output is a 7s extension." — [mcp-veo-go README](https://github.com/GoogleCloudPlatform/vertex-ai-creative-studio/blob/main/experiments/mcp-genmedia/mcp-genmedia-go/mcp-veo-go/README.md)
- [OFFICIAL] Gemini API: "the final video duration can only be up to 148 seconds long which means you can extent your first 8s video about 20 times". Constraints: "Only with 720p resolution", "The input video must be Veo generated", "Less that 141s long". The section is marked "(WIP)". — [cookbook Get_started_Veo](https://github.com/google-gemini/cookbook/blob/main/quickstarts/Get_started_Veo.ipynb)
- [OFFICIAL, search summary, via `02_prompt_veo_estructura.md`] Gemini API docs say:
  - Extension conditions on the last second (24 frames) of the input.
  - Voice does not extend well unless speech is present in that final second.
  I did not re-verify this. My own searches only found third parties repeating "seeded from the final second". — [Gemini API Veo docs (search summary)](https://ai.google.dev/gemini-api/docs/veo); [RunComfy extend-video (search summary)](https://www.runcomfy.com/models/google-deepmind/veo-3-1/extend-video)
- [VENDOR, search summary] Atlas Cloud:
  - Extending returns "the original 8 seconds and their audio intact, followed by the new footage".
  - Advice: let any line **finish before the clip's last second**, so it is not cut off at the seam.
  - Claims the Gemini API Veo 3.1 preview models shut down on Oct 22, 2026. This matches a deprecations snapshot in `01_veo_vertex_specs.md`.
  — [Atlas Cloud: Veo 3 longer than 8 seconds](https://www.atlascloud.ai/blog/tips/veo-3-longer-than-8-seconds)
- [PRACTITIONER, search summary] Identity drift "accumulates per generation", so "keep individual extends short". Identity "holds across cuts for ~3–4 chained extends; beyond that prepare to re-anchor with an i2v". This is a rule of thumb from a single agent-skill doc, not a measurement. — [mcpservers.org video-extend skill](https://mcpservers.org/agent-skills/doany-ai/video-extend)
- [GOOGLE-SAMPLE] Google's "Run, Veo, Run" demo fights extension drift with an **"Analyze & Augment" loop**:
  - After each clip, Gemini returns a context string of "Visual Style… Lighting… Main Subject description (appearance, clothing)… Setting".
  - That string is appended to the next extension prompt, e.g. "She jumps over a car. [Cyberpunk style, neon blue lighting, female runner in red tank top, wet concrete street]".
  - This gives "Veo… both the pixel data and the semantic guardrails".
  — [continuity_strategy.md](https://github.com/GoogleCloudPlatform/vertex-ai-creative-studio/blob/main/experiments/run-veo-run/docs/continuity_strategy.md); [handlers/veo.go](https://github.com/GoogleCloudPlatform/vertex-ai-creative-studio/blob/main/experiments/run-veo-run/server/internal/handlers/veo.go)
- [GOOGLE-SAMPLE] Google's sample app marks Lite `supports_video_extension=True`, `supported_extension_durations=[7]` (present since at least the 2026-05-02 history cut). Its extension test uses `veo-3.1-fast-generate-001`, 720p, `duration_seconds=7`, `enhance_prompt=False`, `generate_audio=True`. **Conflict:** the Gemini API Lite page says Lite "does not support… Extension" (see `01_veo_vertex_specs.md` §2). — [config/veo_models.py](https://github.com/GoogleCloudPlatform/vertex-ai-creative-studio/blob/main/config/veo_models.py); [test/test_veo_extension.py](https://github.com/GoogleCloudPlatform/vertex-ai-creative-studio/blob/main/test/test_veo_extension.py)
- [OFFICIAL] **Omni 1.1 Flash extension:**
  - "analyzes up to 10 seconds of prior context to generate a natural 3–10 second continuation while maintaining temporal continuity, character identity, camera momentum, and environmental lighting."
  - "Generating spoken dialogue or speech is fully supported when extending previously generated videos via multi-turn (`previous_interaction_id`)", but "you cannot extend an uploaded video where someone is talking to add additional dialogue".
  - Reference images can be added during extension ("the traveler shown in <IMAGE_REF_0>").
  - "Append only".
  — [cookbook Get_started_Omni](https://github.com/google-gemini/cookbook/blob/main/quickstarts/Get_started_Omni.ipynb)
  - Agent Platform: "source video (up to 30s long). Each call can add a maximum of 10s." — [GCP notebook Omni 1.1](https://github.com/GoogleCloudPlatform/generative-ai/blob/main/vision/getting-started/gemini_omni_1_1_flash_video_gen.ipynb)

### Inferences
- **Extension is the weakest identity tool on Veo.** It cannot take an image anchor, and the output is 720p, which loses face detail in 9:16 at 1080p delivery. Use it only for short continuous takes of 1–2 hops (about 15–22 s total).
- **Every extension prompt should:**
  1. Repeat the character bible block verbatim (§5).
  2. Include a Gemini-generated "context" line from the previous clip, as in Google's Analyze & Augment loop.
  3. Contain exactly one new action.
  4. If dialogue continues, make the previous clip's line run into its final second. Scripting it to end right at 8.0 s is a practical compromise. Atlas's advice ("finish before the last second") conflicts with Google's ("speech present in the final second" for the voice to carry). Choose per need: for voice continuity, keep speech near the end. For a clean seam, finish the line and accept that the voice may not carry over.
- **For real long-form voice and identity continuity** (podcast or storytelling over 20 s): use one clip per line or beat, from re-anchored keyframes (§3), with one fixed voice. Ideally the voice is replaced or normalised in post by the TTS/dubbing tool (see the voice research file). Alternatively, use Omni 1.1 Flash multi-turn extension, which is documented to keep identity and dialogue (Preview, $0.15/s at 1080p per `01_veo_vertex_specs.md`).
- **Before building on Lite extension,** probe it with one call on the client's project, as Google's `veo_feature_probe.py` does.

### Gaps
- No official number for identity drift per extension hop.
- Not confirmed: whether Vertex returns the combined video or only the 7 s segment. Atlas, via search summary, says the combined video is returned on the Gemini API. The MCP README says "Output is a 7s extension".
- Not confirmed: whether Lite extension works on `veo-3.1-lite-generate-001` today, and whether extension output can be 1080p on Vertex.

---

## 5. A fixed "character bible" text block repeated verbatim in every prompt: what details matter

### Takeaway
Google's own pipelines profile the face into a fixed schema with Gemini at low temperature:
- face shape
- eye colour and shape
- eyebrow shape
- nose
- lips
- hair colour and style
- skin tone
- jawline
- distinguishing marks

The Vertex best-practice guidance (search summary) is to **repeat the same character and voice description in every prompt**, with the same seed. The block should restate only anchors that are **visible in the start frame**, so the text never fights the image. Wardrobe and setting go in a separate per-scene block.

### Cited Findings
- [GOOGLE-SAMPLE] `FacialCompositeProfile` fields: `face_shape`, `eye_color`, `eye_shape`, `eyebrow_shape`, `nose_shape`, `lip_shape`, `hair_color`, `hair_style`, `skin_tone`, `jawline`, `distinguishing_marks` ("scars, moles, or tattoos"). It is used to profile reference photos before generating new scenes. — [character_consistency_models.py](https://github.com/GoogleCloudPlatform/vertex-ai-creative-studio/blob/main/models/character_consistency_models.py)
- [GOOGLE-SAMPLE] Profiling runs with `temperature=0.1`, and a second Gemini pass turns the JSON into "a concise, natural language description". In the older demo, the description prompt is "Provide a two-line description for this person, focusing on their key visual features: clothes and detailed physical and facial traits." — [extend_image_generator.py](https://github.com/GoogleCloudPlatform/vertex-ai-creative-studio/blob/main/experiments/veo3-item-consistency/extend_video/extend_image_generator.py); [veo3-character-consistency/prompts.py](https://github.com/GoogleCloudPlatform/vertex-ai-creative-studio/blob/main/experiments/veo3-character-consistency/prompts.py)
- [OFFICIAL, search summary] Vertex best practices: a three-scene example repeats the same character and voice description in each prompt and uses the same seed to keep visuals and voice consistent. — [Best practices for Veo (search summary)](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/video/best-practice) (as reported in `02_prompt_veo_estructura.md` §8)
- [OFFICIAL] `seed`: "If RNG seed is exactly same for each request with unchanged inputs, the prediction results will be consistent." Google's MCP tool calls it "best-effort reproducible". — [python-genai types.py](https://github.com/googleapis/python-genai/blob/main/google/genai/types.py); [mcp-veo-go README](https://github.com/GoogleCloudPlatform/vertex-ai-creative-studio/blob/main/experiments/mcp-genmedia/mcp-genmedia-go/mcp-veo-go/README.md)
- [GOOGLE-SAMPLE] Use the anchor nouns, not pronouns: "your prompt should reiterate 'red cup' and 'wooden table' rather than just 'the cup'." For continuation: "repeat the key visual anchors… (e.g., 'the woman with the silver bun')". — [prompts.py](https://github.com/GoogleCloudPlatform/vertex-ai-creative-studio/blob/main/experiments/veo3-character-consistency/prompts.py); [item-consistency prompts.py](https://github.com/GoogleCloudPlatform/vertex-ai-creative-studio/blob/main/experiments/veo3-item-consistency/prompts.py)
- [GOOGLE-SAMPLE] The extension context schema covers "Visual Style… Lighting… Main Subject description (appearance, clothing)… Setting description". — [continuity_strategy.md](https://github.com/GoogleCloudPlatform/vertex-ai-creative-studio/blob/main/experiments/run-veo-run/docs/continuity_strategy.md)
- [Client's own still SOP] The descriptor should be short and identical, with at most 3–4 hard markers. Wardrobe and light belong in the scene block so they are not "baked" into identity. Practice is to open and close with the identity lock. — [Realismo en avatares IA imagen.md §12](../../reports/Realismo%20en%20avatares%20IA%20imagen.md) (sources cited inside that file)

### Inferences
**Character bible template for Jarvis** (store per avatar, paste byte-identical; English, because Veo prompt guidance is English; spoken lines stay in Spanish):

```
[CHARACTER A — "Sofi" (internal ID AV-014; never spoken or shown)]
Identity (matches the start frame): a 27-year-old Argentine woman, oval face, light-olive skin
with faint freckles across the nose, almond hazel eyes, thick straight dark-brown eyebrows,
small mole above the left lip corner, shoulder-length wavy chestnut hair with a center part.
Voice: warm, slightly husky female voice, late 20s, relaxed conversational pace, speaks
Rioplatense Spanish from Buenos Aires (voseo, "sh" sound for "ll/y").
```

The voice and accent wording belongs to the voice/accent research file. It is shown here only to make clear that the identity block and the voice block travel together.

**Rules:**
1. **Visible anchors only.** Use features visible in the start frame, and run Jarvis multimodally so it cannot invent features.
2. **Pick 3–4 "hard markers"** (mole, freckles, hair cut and parting, eyebrow shape) and never change their wording.
3. **Wardrobe** goes in a per-scene block. Repeat it verbatim across all clips of the same scene.
4. **Keep the same seed** per avatar and scene, and the **same model ID** across all clips of a video.
5. **Use descriptors, never names,** in action and dialogue lines. Veo has never "met" Sofi (see `02_prompt_veo_estructura.md` §8).
6. **Never include a real person's name** or "looks like [celebrity]". Avatars are fictional. This also avoids policy blocks.

**For multi-character scenes,** give each character a separate block. Characters must differ on at least two visual axes (hair colour or length, garment colour, screen side) and on voice (gender, age, timbre). In the action line, refer to each by screen position plus garment: "the woman on the left in the mustard sweater".

### Gaps
- No official ablation shows which bible fields actually reduce drift in Veo motion. Field importance here is inferred from Google's profiling schema.
- I could not read the official Vertex best-practices page verbatim.

---

## 6. Realism in motion for UGC: what to ask for, the common Veo "tells", and fixes

### Takeaway
Official Google material gives a vocabulary for subtle motion: "The subject blinks slowly", "A subtle smile appears…", "The subject's head turns slowly", "handheld shaky cam". It also gives an evaluation rubric (flicker, morphing, unnatural textures, motion coherence). Google has published **no UGC-specific realism guide**.

Practitioner UGC prompts converge on these points:
- Phone-camera look, either front-camera selfie or a rear lens.
- Slight handheld shake and off-center framing.
- Waist-up framing.
- One action per 8 s.
- Lived-in background, real skin texture and stray hairs.

Documented Veo weak spots are lip detail (vendor claim) and **gibberish text on labels and signs**. For teeth and hands, I found no Veo-specific fix. The defensible fixes are structural: tight framing, few hand actions, no readable text in generation (labels added in post or via r2v), multiple samples, and an automated QA pass.

### Cited Findings
- [OFFICIAL] Subject-animation presets: "The subject blinks slowly", "A subtle smile appears on the subject's face", "The subject's head turns slowly", "The subject's hair and clothes flutter gently in the wind". The camera list includes "Static Shot (or fixed)", "Dolly (In)", "Close-Up" and "Medium Shot". — [veo3_video_generation](https://github.com/GoogleCloudPlatform/generative-ai/blob/main/vision/getting-started/veo3_video_generation.ipynb)
- [GOOGLE-SAMPLE] The camera vocabulary includes "handheld shaky cam" and "POV shot". Google's prompt engineer also adds "Secondary Motion & Texture… ('wisps of her hair flutter in a gentle breeze')". — [veo3-character-consistency/prompts.py](https://github.com/GoogleCloudPlatform/vertex-ai-creative-studio/blob/main/experiments/veo3-character-consistency/prompts.py)
- [GOOGLE-SAMPLE] Google's video QA rubric:
  - "Visual Quality & Artifacts (Weight: 25%)… distracting visual glitches, distortion, flickering, unnatural textures, or object morphing."
  - "Motion Coherence (Weight: 25%): Is the movement… smooth, natural, and physically plausible".
  - Pairwise version: choose A, B or SAME.
  — [veo_video_eval_templates.py](https://github.com/GoogleCloudPlatform/vertex-ai-creative-studio/blob/main/experiments/veo-genetic-prompt-optimizer/veo_genetic_prompt_optimizer/veo_video_eval_templates.py)
- [OFFICIAL] For QA at sub-second precision, Gemini "Agentic Video" (Gemini 3.8/3.7/3.6 Flash, 3.5 Flash-Lite) can replay "`fps=10+` only on critical 3–10s intervals". Default video ingestion is 1 FPS, which "misses sub-second actions (<1s)". — [intro_agentic_video.ipynb](https://github.com/GoogleCloudPlatform/generative-ai/blob/main/gemini/agentic-video/intro_agentic_video.ipynb)
- [PRACTITIONER, search summary] A Veo UGC JSON prompt asks for:
  - "a natural, unposed look with small imperfections visible such as stray hairs and real skin texture"
  - "slightly off center for a candid feel" framing
  - "a small handheld shake"
  - a "smartphone rear-camera lens look"
  - "raw, imperfect UGC vibe"
  It says the phone is never visible. That suits rear-camera UGC; selfie UGC needs a different line. — [ulazai prompt directory](https://ulazai.com/directory/prompt/2c84c47a-8ed9-4395-b1d1-d9be645cc79c/)
- [VENDOR, search summary] More vendor advice:
  - Argil: state the camera first, keep to "one clear action that fits in 8 seconds", and specify framing such as "waist-up".
  - Atlabs: "specific, lived-in details create authenticity" (rumpled bedding, cluttered shelves, natural light).
  - Dupple: a Veo 3.1 tutorial uses a "selfie-mode" prompt where the woman films herself.
  — [Argil docs](https://docs.argil.ai/resources/create-VEO3-videos); [Atlabs guide](https://www.atlabs.ai/blog/create-realistic-ai-ugc-videos-complete-guide); [Dupple tutorial](https://www.dupple.com/tutorial/produce-ugc-style-marketing-videos-with-realistic-camera-angles-using-veo-3-1)
- [VENDOR] [>6 months] Argil (June 2025) says Veo 3 "offers cinematic realism, lacks perfect lips". It describes good lip-sync as "lip tightening, corners lifting in sync with speech". Argil sells a competing avatar tool. — [Argil blog (search summary)](https://www.argil.ai/blog/perfect-lips-ai-how-to-create-realistic-avatar-lip-sync-videos-2025)
- [PRACTITIONER] [>6 months?] On text, the model "generates text that looks plausible at a glance but is actually just a jumble of nonsensical characters". The fix is "a combination of being clever with your prompts & having a good post-production workflow" (search summary; undated). — [Arsturn](https://arsturn.com/blog/how-to-get-clean-text-in-veo-3-a-guide-to-fixing-ai-gibberish)
- [OFFICIAL] r2v includes a "Product reference image… to demonstrate how Veo maintains product consistency while in motion". This is Veo 3.1 or Fast only, not Lite. — [veo3_reference_to_video](https://github.com/GoogleCloudPlatform/generative-ai/blob/main/vision/getting-started/veo3_reference_to_video.ipynb)
- [OFFICIAL] The cookbook's general negative-prompt example is "ugly, low quality, static, weird physics". The dialogue example uses "texts, captions, subtitles". Google also advises describing what you want rather than "no X". — [cookbook Get_started_Veo](https://github.com/google-gemini/cookbook/blob/main/quickstarts/Get_started_Veo.ipynb); [Cloud blog prompting guide](https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-veo-3-1)
- [PRACTITIONER, search summary] Plan for overgeneration: "about three generations per usable shot". — [Hackernoon](https://hackernoon.com/how-to-extend-an-ai-generated-video-clip-past-its-length-limit-without-the-drift)

### Inferences
**Motion block for talking-head UGC** (assembled from the official phrases above and practitioner consensus; A/B test at fixed seed):

```
Camera: vertical 9:16 smartphone front-camera selfie, held at arm's length slightly below eye level,
subtle natural handheld sway, framing chest-up and slightly off-center, no zoom, no cuts.
Performance: she looks directly into the lens, blinks naturally every few seconds, small eyebrow
raises on emphasis, a brief half-smile at the end; one relaxed hand gesture below the chin, the
other hand holding the phone (out of frame). Subtle breathing, natural pauses between phrases.
Scene: lived-in apartment kitchen in daylight from a window on her left, slightly cluttered counter.
Look: unretouched skin with visible pores and faint freckles, fine flyaway hairs, natural phone
exposure, slight sensor noise.
```

**Tells to watch, with structural fixes:**
- **Waxy or over-smooth skin in motion.** Say "unretouched skin with visible pores", and keep the master still's skin realistic (see the still SOP). Do not ask for "flawless" or "beautiful". Add grain in post rather than in the prompt if needed.
- **Mouth and teeth.** Keep lines short (see the word budget in `02_prompt_veo_estructura.md` §4). Start from a closed-mouth frame. Avoid extreme close-ups of the mouth. Reject clips in QA and regenerate with 2–4 samples.
- **Morphing hands.**
  - Allow one simple gesture, or keep hands still and low.
  - Avoid finger counting, hand-over-face, or picking up small objects.
  - For product-in-hand, start from a still where the hand already holds the product correctly.
- **Warping background.** Use a static or near-static camera and a simple, lived-in but not busy background. Avoid mirrors, screens and text on walls.
- **Product label text.**
  - Do not ask Veo to render readable text.
  - Either generate the start frame with the correct label and keep the product still and frontal, or composite the real pack shot or label in post.
  - Or use Fast/Standard r2v with the product as an `asset` (not Lite).
- **Captions burned in.** Add a negative prompt for subtitles and on-screen text (see `02_prompt_veo_estructura.md` §6).

**QA automation:**
- Run Google's pairwise video rubric with Gemini on the 2–4 samples per shot.
- Add an identity check: ArcFace on frames sampled at about 1, 4 and 7.5 s against the master, using the thresholds from the still SOP.
- Use Agentic Video at a higher FPS to catch sub-second mouth, teeth and hand glitches.

### Gaps
- No official or independent Veo-specific guidance on teeth, hand morphing, or "waxy skin in motion". Fixes above are structural inferences.
- No measured effect of "handheld" wording on identity drift. More camera motion plausibly increases drift; this is untested.
- No source tested blinking or eye-contact phrasing on Veo 3.1 Lite specifically.

---

## 7. Upscaling and frame interpolation for final delivery: options, and whether they harm faces

### Takeaway
Lite outputs at most **1080p** (no 4K) at 24 fps. Google's standalone **Veo upscaling** (to 1080p/4K, any source video) was announced April 3, 2026, as **private preview, "coming soon to public preview"**. I found no evidence that it reached public preview by October 2026, and it has no price on the pricing page.

For third-party upscaling, Topaz's own docs recommend **Starlight Precise** (2.5 or 2.6) when "nothing in the frame should change", such as faces and text. "Creative" or Astra modes **invent detail and can change the face**. Run identity QA after upscaling. I found no independent benchmark of face-identity preservation for upscaling Veo output.

### Cited Findings
- [OFFICIAL] "Available in private preview, and coming soon to public preview, the new Veo upscaling capability allows you to enhance your videos up to 1080p and 4K, regardless of whether they were generated by Veo, another AI model, or a traditional camera." — [Google Cloud blog, 2026-04-03](https://cloud.google.com/blog/products/ai-machine-learning/veo-3-1-lite-and-a-new-veo-upscaling-capability-on-vertex-ai)
- [PRACTITIONER, search summary] A developer-forum post requests "allowlist access for Veo 3.1 Upscale (1080p / 4K)", consistent with a gated preview. — [discuss.ai.google.dev](https://discuss.ai.google.dev/t/request-allowlist-access-for-veo-3-1-upscale-1080p-4k/168781)
- [OFFICIAL, search summary] The January 2026 update brought "upscaling to 1080p and 4K" as a resolution option in Flow, the Gemini API and Vertex. — [blog.google 2026-01-13 (search summary)](https://blog.google/innovation-and-ai/technology/ai/veo-3-1-ingredients-to-video/)
- [OFFICIAL] The pricing page has no Veo upscaling SKU; only Imagen image upscaling is listed. See `01_veo_vertex_specs.md` §3. — [Agent Platform pricing](https://cloud.google.com/gemini-enterprise-agent-platform/generative-ai/pricing)
- [VENDOR docs, search summary] Topaz:
  - Recommends **Starlight Precise** "for shots where nothing in the frame should change, such as faces, text, or logos".
  - Recommends Astra 2 for "wide shots or heavily degraded footage, where the model has to invent detail".
  - Has a five-level sharpness control that can lower detail strength on skin, hair and fabric, where full strength "can look artificial".
  - **Version conflict:** the docs name "Starlight Precise 2.6" as the top Precise model, while other sources still call 2.5 current.
  — [Topaz for web video docs](https://docs.topazlabs.com/cloud-apps/topaz-for-web-video)
- [PRACTITIONER/VENDOR, search summary] Starlight 2.5 is described as reducing the "plastic" look of GenAI faces and fabrics, up to 4K. Astra's Creative mode "can invent detail, so faces may change". The model "reconstructs detail from what's there", so "feed it your cleanest generation". These are affiliate-style sources with no face benchmark. — [invideo: Topaz Starlight 2.5 FAQ](https://invideo.io/faq/what-is-topaz-starlight-25-and-why-is-it-used-for-ai/); [invideo: Topaz models](https://invideo.io/blog/topaz-video-enhancement-models/); [MindStudio: Topaz Astra](https://www.mindstudio.ai/blog/topaz-astra-video-upscaler-scene-detection); [Hackernoon: upscale without making artifacts worse](https://hackernoon.com/how-to-upscale-ai-generated-video-without-making-the-artifacts-worse)
- [VENDOR, search summary] API pricing via Runware: Starlight Precise 2.5 is about $0.40 per 5 s clip at 1K and $0.875 at 4K. — [Runware](https://runware.ai/models/topazlabs-starlight-precise-2-5)
- [OFFICIAL] The Veo SDK exposes `fps` ("Frames per second for video generation"). Extension inputs must be 24 fps. — [python-genai types.py](https://github.com/googleapis/python-genai/blob/main/google/genai/types.py); [mcp-veo-go README](https://github.com/GoogleCloudPlatform/vertex-ai-creative-studio/blob/main/experiments/mcp-genmedia/mcp-genmedia-go/mcp-veo-go/README.md)
- [GOOGLE-SAMPLE] For concatenation: "Ensure all clips have matching dimensions and frame rates." — [genmedia-video-editor skill](https://github.com/GoogleCloudPlatform/vertex-ai-creative-studio/blob/main/docs-site/src/content/docs/experiments/mcp-genmedia/skills/genmedia-video-editor.md)

### Inferences
- **Delivery chain for 9:16 social ads:**
  1. Generate natively at 1080p on Lite (9:16).
  2. Request LOSSLESS compression if storage allows.
  3. Edit and concatenate at 24 fps.
  4. Upscale only if a placement needs it (most Reels/TikTok placements are 1080×1920 already), with **Starlight Precise at low or medium sharpness**. Never use Creative or Astra modes on faces.
  5. Re-run ArcFace on upscaled frames against the master, then add light grain last.
  This is consistent with the still SOP's "conservative first, grain last".
- **Frame interpolation** (24 to 30/60 fps) is unnecessary for UGC realism, since phone UGC at 24–30 fps reads natural. It risks "soap-opera" smoothness and mouth warping on fast lip motion. If a platform needs 30 fps, prefer a simple frame-rate conversion. This is untested inference; no source found.
- **Disclosure:** keep SynthID and any C2PA metadata intact. Do not use upscalers or re-encoders as a way to strip provenance (see the still SOP's compliance section).

### Gaps
- Current status (October 2026) of Veo's standalone upscaling: whether it is public preview and what it costs.
- No benchmark of face-identity change from Topaz Starlight or Astra, or Veo upscaling, on Veo talking heads.
- No source on frame interpolation effects on AI lip-sync.

---

## 8. Objective: a recommended identity-lock workflow for the client (Lite first, with escalation paths)

### Takeaway
The cited sources point to one design. Every clip should be **one generation away from the approved master identity**. That means:
- re-anchored keyframes from the identity pack, not chained video frames;
- a byte-identical character bible (visible anchors only), plus a per-scene wardrobe block;
- a multimodal Jarvis that sees the keyframe;
- fixed model, seed and settings;
- 2–4 samples, with automated rubric plus ArcFace QA.

Use extension only for short continuous takes. Escalate to Fast/Standard r2v (two people or products) or Omni 1.1 Flash (multi-character binding, long dialogue extension) when Lite's single-frame anchor is not enough.

### Cited Findings
- Google's keyframe-per-scene pattern (character sheet, then Nano Banana keyframes, then Veo i2v per keyframe). — [pages/storyboarder.py](https://github.com/GoogleCloudPlatform/vertex-ai-creative-studio/blob/main/pages/storyboarder.py); [pages/character_sheet.py](https://github.com/GoogleCloudPlatform/vertex-ai-creative-studio/blob/main/pages/character_sheet.py)
- Google's reference-photo, best-match, reframe, i2v pipeline. — [models/character_consistency.py](https://github.com/GoogleCloudPlatform/vertex-ai-creative-studio/blob/main/models/character_consistency.py)
- Google's continuation from the best of the last 4 frames, with the character described from the reference. — [extend_image_generator.py](https://github.com/GoogleCloudPlatform/vertex-ai-creative-studio/blob/main/experiments/veo3-item-consistency/extend_video/extend_image_generator.py)
- Multimodal rewriter fix (Aug 2026). — [commit 27f30b6](https://github.com/GoogleCloudPlatform/vertex-ai-creative-studio/commit/27f30b6d7e03b52a84db3694e26e1ffd11f0b664)
- Extension cannot take an image; r2v cannot take a first or last frame. — [python-genai types.py](https://github.com/googleapis/python-genai/blob/main/google/genai/types.py)
- Omni per-character binding and dialogue-capable extension. — [cookbook Get_started_Omni](https://github.com/google-gemini/cookbook/blob/main/quickstarts/Get_started_Omni.ipynb)

### Inferences
**Step-by-step (for the SOP writer; every step traces to the findings above, and the thresholds are untested):**

1. **Identity pack per avatar:**
   - A master 9:16 1080×1920 still: neutral, mouth closed, soft light.
   - A 4–5 view sheet (front, three-quarter left and right, profile, close-up).
   - A FacialCompositeProfile JSON produced by Gemini at temperature 0.1, from which the 3–4 hard markers are taken.
   - A fixed voice block.
   - Store all of it with seed, model ID and version.
2. **Per shot:**
   - Jarvis receives the script line plus the identity pack.
   - It generates or edits a **shot keyframe** with Nano Banana, using the master and the sheet as references, at the output aspect ratio.
   - ArcFace against the master centroid: ≥0.60 passes automatically for near-frontal shots, 0.45–0.60 goes to human review (thresholds from the still SOP).
3. **Per clip (Lite i2v):**
   - Settings: `image=keyframe`, `duration_seconds` 6 or 8, `resolution="1080p"`, `aspect_ratio="9:16"`, `number_of_videos` 2–4, fixed `seed`, `generate_audio=True`, `person_generation="allow_adult"`.
   - Prompt order: character bible (verbatim) → scene and wardrobe block (verbatim within a scene) → camera → one action and micro-expressions → one dialogue line → audio bed. Negative prompt for captions and text.
   - Test `enhance_prompt` on and off: Google's apps default it on, but it can paraphrase (see `02_prompt_veo_estructura.md` §7).
4. **QA per sample:**
   - Gemini pairwise rubric plus ArcFace at about 1 s, 4 s and 7.5 s.
   - Agentic-video high-FPS check for mouth and hand glitches.
   - Pick the best sample. If all fail, regenerate; do not edit a drifted clip.
5. **Continuity across clips:**
   - Default: cut between clips, each from its own re-anchored keyframe.
   - For a continuous take: bookend (first frame = best on-model frame from the last 4 of the previous clip, last frame = master-derived end pose), or 1–2 extension hops with the bible and Gemini context appended.
   - Re-anchor before hop 3.
6. **Multi-character formats** (interview, podcast, storytelling):
   - One speaker per clip, from that speaker's own keyframe, with their own bible and voice block.
   - Two-shots only from a keyframe built with both masters. For moving two-shots, use Fast/Standard r2v with each person as an `asset` (2 assets plus a set).
   - For long dialogue in one continuous take, use Omni 1.1 Flash with `<IMAGE_REF_n>` per character and multi-turn extension.
7. **Delivery:**
   - Concatenate at matching resolution and 24 fps.
   - Use a conservative upscale (Starlight Precise) only if needed, then re-check ArcFace, then add grain.
   - Keep SynthID and C2PA.

### Gaps
- **Not A/B tested anywhere in public:**
  - bookend anchoring against plain i2v;
  - a multi-view sheet against a single portrait as a Veo `asset`;
  - the effect of `enhance_prompt` on identity;
  - the real drift per Lite extension hop.
  The client should run these with a fixed seed on 3 avatars × 5 scripts before locking the SOP.
