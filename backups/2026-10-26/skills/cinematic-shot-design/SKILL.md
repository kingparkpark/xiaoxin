---
name: cinematic-shot-design
description: Use when a user wants to turn a scene, emotion, story beat, or video reference image into cinematic shot decisions and production-ready AI video prompts, including automatic or specified film-director references; not for editing or reviewing completed footage.
---

# Cinematic Shot Design

Turn narrative intent into a coherent shot plan and an AI-generation Prompt. Preserve the user's story, characters, environment, reference-image facts, and fixed constraints. Treat camera parameters as visual-language choices, not guarantees of physical simulation.

## Workflow

1. Read [input-routing.md](references/input-routing.md). A scene description is sufficient; do not require platform, duration, aspect ratio, director, or reference image.
2. Read [shot-structure.md](references/shot-structure.md) and choose **单镜头** or **多镜头** before choosing focal length. Use 2–3 shots only when the brief contains a reveal–reaction–action chain, a confrontation, a meaningful environmental reveal, or a location/time change; otherwise default to one shot.
3. Determine the narrative job: establish space, show action, reveal information, express emotion, or transition.
4. Read [visual-style-tags.md](references/visual-style-tags.md) and translate the brief into visible, executable traits.
5. Read [director-matching.md](references/director-matching.md):
   - For a built-in director, load only that profile from [directors/index.md](references/directors/index.md).
   - For an unlisted director, form a temporary profile for this request and do not save it without confirmation.
   - With no specified director, read the routing signatures in [directors/index.md](references/directors/index.md), compare them using the normalized tags, choose one primary match plus two short alternatives, then load only the primary director's full profile and continue without pausing.
   - If the user declines director reference, use the general rules directly.
6. Read [decision-rules.md](references/decision-rules.md), then only the relevant craft references: [optics.md](references/optics.md), [framing.md](references/framing.md), [camera.md](references/camera.md), and [lighting.md](references/lighting.md).
7. For multi-shot sequences, maintain screen direction, eyelines, geography, identity, wardrobe, props, light direction, and motivated changes across every shot.
8. Read [prompt-workflow.md](references/prompt-workflow.md). Director names may appear in analysis, but the executable Prompt must use concrete visual instructions without relying on a name.

## Output contract

### 风格匹配

- Automatic mode: primary director reference, concise reason, and two alternatives with distinct effects.
- Specified mode: selected relevant traits and why they serve this scene.
- Omit when the user explicitly requests no director reference.

### 镜头决策

- Narrative purpose
- Shot size and subject placement
- Focal length/perspective and depth-of-field intent
- Camera height, angle, distance, movement, speed, direction, and motivation
- Lighting direction, quality, contrast, and color
- Continuity constraints

### 镜头模式

- State `单镜头` or `多镜头（2–3镜）` and give the selection reason.
- Add: `如需切换，可直接说“改为单镜头”或“改为3镜分镜”。`
- For multi-shot output, provide each shot's narrative purpose, suggested duration, independent Prompt, and editing order/cut point.
- Also provide one combined Prompt containing all shots in order for convenient copying.

### 可执行 Prompt

- Preserve fixed story facts and reference-image locks.
- Use one coherent visual strategy; do not blend directors in v1.
- Do not reproduce a specific recognizable film scene.
- Do not use a director's name as a substitute for visual instructions.

### 可选附加项

- Negative constraints when they prevent likely failures.
- Recommended platform, duration, or aspect ratio only for fields the user omitted; keep recommendations outside the Prompt by default.
- If metadata must enter a platform-adapted Prompt, state the concrete reason.
- For an unlisted director, ask after delivery whether the user wants a permanent profile added.

Prefer one confident recommendation. Never claim a lens, f-stop, lighting ratio, or named style will be reproduced exactly by a generative model.
