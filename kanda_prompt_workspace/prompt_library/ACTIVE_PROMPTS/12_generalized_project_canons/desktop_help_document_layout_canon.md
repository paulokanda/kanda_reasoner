# Desktop Help Document Layout Canon

Version: 1.0
Status: Active special prompt candidate
Prompt ID: desktop_help_document_layout_canon
Load mode: on_request
Owner group: 12_generalized_project_canons
Use: Load when creating or updating local desktop help documents, help-book layout, offline help HTML/CSS, or characterful help illustrations.

## Box Logic Requirement

Before any implementation, repair, refactor, prompt update, governance update, or bundle creation, the AI must:

- Identify the active box before implementation.
- State owner paths.
- State files allowed to change.
- State files explicitly out of scope.
- Declare cross-box touches.
- Preserve public contracts.
- Validate the active box and any touched external box.

## Router Placement Rule

This prompt is the active KANDA prompt-library asset for desktop help document layout.

Active prompt assets live under:

```text
kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/
```

Metadata lives under:

```text
kanda_prompt_workspace/prompt_library/METADATA/
```

Reference notes under `.project_reference/` are not active project prompt artifacts. They may be read only when the human explicitly points to them or when governed reconciliation needs source evidence. Do not treat `.project_reference/CANNON/` as the live prompt library, do not register it as project logic, and do not validate runtime behavior against files there.

When this help-layout rule needs an update, follow the prompt-library lifecycle:

1. Inspect current prompt-library assets and indexes.
2. Check for duplicate or overlapping active prompts.
3. Update this prompt, its metadata, and routing visibility only when needed.
4. Keep runtime help files under the owning application help-docs box, not inside `.project_reference`.

## Purpose

Create user-facing help documents that read like compact technical-book chapters inside a desktop application window. The document must be accurate, local-only, comfortable to read, visually polished, and useful to both technical and non-technical readers.

The canonical creation pipeline is:

```text
Markdown source -> dual-layer explanations -> beautiful hand-made daily-life cartoon illustrations -> deterministic local HTML/CSS -> desktop Qt help window
```

## Desktop Format Decision

Use two layers:

- `.md` files are the canonical editable help source.
- `.html` files are the rendered desktop help documents.
- `.css` files hold the shared book-style layout.
- `assets/drawings/` holds original characterful artwork.
- `assets/diagrams/` holds original technical diagrams.
- `assets/screenshots/` holds annotated local GUI screenshots when needed.

Desktop help opens inside the application, not in an external browser.

Primary renderer:

```text
QWebEngineView
```

Fallback renderer:

```text
QTextBrowser
```

Final fallback:

```text
Plain read-only Qt text widget
```

Rendered HTML must remain local-only. Do not reference `http://`, `https://`, CDN assets, trackers, remote images, remote scripts, or remote fonts.

## Page Design

The document should feel like a professionally typeset programming or AI book, not a web landing page or slide deck.

Use:

- compact technical-book proportions;
- single main text column;
- generous margins and stable page rhythm;
- dark navy body text on white paper;
- sapphire blue for structural accents and cross-references;
- amber-orange for warnings, tips, and key teaching highlights;
- restrained callouts, tables, captions, and figures;
- no gradients, decorative blobs, marketing hero sections, or card-heavy layouts.

Recommended palette:

```css
:root {
  --body-text: #1a1a2e;
  --ink: #0d0d1a;
  --xref: #1a4e8c;
  --blue-mid: #2563a8;
  --blue-light: #dbeafe;
  --blue-chapter: #0f3460;
  --orange-strong: #d97706;
  --orange-mid: #f59e0b;
  --orange-light: #fef3c7;
  --orange-rule: #ea580c;
  --rule: #94a3b8;
  --table-rule: #cbd5e1;
  --paper: #ffffff;
  --sidebar-bg: #f8fafc;
  --subtitle: #475569;
  --tip: #d97706;
  --note: #2563a8;
  --warning: #ea580c;
  --success: #16a34a;
}
```

Typography:

- Body text: Minion Pro preferred; fallback Adobe Garamond Pro, Source Serif 4, Georgia.
- Headings: Myriad Pro Condensed preferred; fallback Source Sans 3 Condensed, Roboto Condensed, Arial Narrow.
- Code: Ubuntu Mono preferred; fallback Consolas, JetBrains Mono, Menlo.
- Captions: italic serif in subtitle color.
- Key terms: bold plus amber-orange underline.

## Characterful Artwork Canon

The canonical characterful-help-art look is beautiful hand-made daily-life cartoon illustration: original, colorful, human-feeling editorial artwork that uses everyday situations to explain the technical subject.

Final characterful help art should use local `PNG` or `WebP` when artistic quality matters. SVG is reserved for technical diagrams, simple schematic figures, or fallback sketches unless a true hand-drawn vector illustration meets the same quality bar as bitmap artwork.

Artwork rules:

- Use colorful editorial cartoon line art with enough detail to feel finished, not sketched as a placeholder.
- Use expressive faces, hands, posture, and ordinary props.
- People and everyday objects must visibly look hand-drawn, with slightly imperfect outlines, organic curves, varied stroke rhythm, small asymmetries, and visible hatching.
- Use hand-lettered signs, labels, tickets, boxes, sticky notes, shelves, and everyday object text when words appear inside the drawing.
- Prefer funny daily-life situations visibly related to the help topic.
- Use KANDA blue/orange as dominant teaching colors, with small secondary colors allowed for ordinary props.
- Use simple white-paper backgrounds.
- Avoid gradients, glossy digital rendering, stock-illustration polish, copied compositions, signatures, logos, names, exact poses, exact layouts, simple geometric placeholder characters, and diagram props pretending to be illustration.

Every generated characterful drawing should be created from a prompt shaped like this:

```text
Create an original beautiful hand-made daily-life cartoon illustration for a serious technical help book.
Scene: [specific KANDA event/artifact/error].
Daily-life metaphor: [funny everyday situation related to the subject].
Style: rich hand-drawn pen-and-ink editorial cartoon with flat color fills, expressive human figures, everyday props,
white paper background, visible sketch hatching, compact composition, funny but professional, visually finished.
Hand-drawn enforcement: people and everyday objects must have slightly imperfect pen outlines, organic curves,
varied stroke rhythm, small asymmetries, and visible hatching; avoid perfect vector-icon geometry, CAD-like objects,
emoji style, polished clipart, generic stock-illustration shapes, simple geometric placeholder characters, or diagram props
pretending to be illustration.
Hand-lettering enforcement: any words drawn inside the scene should look handwritten or marker-written, with uneven
baseline and human spacing, unless the object is a technical diagram that intentionally needs crisp labels.
Color: KANDA blue (#0f3460 / #2563a8) and amber-orange (#d97706 / #f59e0b) are dominant teaching colors;
small secondary colors are allowed for daily-life props. No gradients, no glossy digital art, no stock illustration look.
Legal/safety: original scene only; do not copy any reference image, signature, character, logo, exact pose, or exact layout.
Output: local PNG or WebP preferred for characterful artwork; SVG is reserved for technical diagrams or fallback sketches.
All assets must be local, listed in the manifest, and rendered offline inside the desktop help window.
```

Drawing density rule:

- Small help files usually need 2 drawings.
- Normal help files need 2 to 3 drawings.
- Larger help files with many events, artifacts, or errors may use 4 or more drawings, but only when each image explains a distinct major section.

For each image asset, record:

- subject/event represented;
- generated asset path;
- asset format and intended display size or source resolution;
- alt text;
- one-sentence caption;
- short image prompt or prompt summary;
- density-rule justification.

## Dual-Audience Explanation Rule

Every event, artifact, implementation step, or error documented in help must include two layers:

```text
Technical: precise implementation meaning, owner, inputs, outputs, invariants, and failure mode.
In plain English: user-facing consequence, ripple effect, and why it must be corrected.
Further reading: local in-document reference to source material used to ground the explanation.
```

Plain-English explanations must be grounded in relevant source research and paraphrased. Rendered desktop help remains local-only, so external sources should be represented as local reading-map references unless a future governed design approves external links.

## Validation Checklist

Before declaring a help-document implementation complete:

- Manifest loads successfully.
- Every source, rendered, CSS, drawing, diagram, and screenshot path exists.
- Rendered HTML references local CSS and local assets only.
- Renderer rejects path traversal.
- Fallback rendering remains available without direct WebEngine imports.
- Palette variables are present in shared CSS.
- Characterful artwork is local, captioned, alt-texted, prompt-documented, and density-rule justified.
- Technical and plain-English explanation layers are present for every event, artifact, and error.
- No runtime or prompt-library test depends on `.project_reference` as an active artifact.
