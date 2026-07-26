---
prompt_id: kanda_desktop_help_exact_layout_blueprint
prompt_code: KPR-12-015
title: KANDA Desktop Help Exact Layout Blueprint
version: 1.1.0
status: active
load_type: companion_on_request
owner_box: 12_generalized_project_canons
classification: project_specific_desktop_help_exact_layout_design_model
source_stage: kanda-help-exact-layout-renderer-contract-v1r1
---

# KANDA Desktop Help Exact Layout Blueprint

## Purpose

Provide the exact reusable layout and design model for KANDA desktop help files that adopt the current book-style local HTML help profile. This prompt is an auxiliary implementation blueprint for `desktop_help_document_layout_canon`; it does not replace that profile, authorize source writes, or prove that rendering and visual validation occurred.

## Load bridge

Load this prompt together with `desktop_help_document_layout_canon` when the user asks to create, rebuild, restyle, or visually align a KANDA help file with the established Show Project to AI help layout.

## Required source inspection before authoring

Inspect the current application implementation before producing or editing help content:

1. Canonical Markdown source under `help_docs/source/`.
2. Generated HTML under `help_docs/rendered/`.
3. Shared stylesheet `help_docs/css/book_help.css`.
4. Help manifest and complete local asset registration.
5. Renderer and fallback behavior, including local-file loading.
6. The current rendered page at the target desktop viewport and a narrow viewport.

Generated HTML is not source authority. Do not hand-edit only the rendered file.

## Non-negotiable rendering-path contract

The visual layout is not achieved by HTML text alone. The rendering component and
loading method are part of the layout contract. Before authoring or patching a help
file, inspect the current help-window implementation and confirm how the HTML is
actually displayed.

For help pages that depend on the canonical book layout, full CSS, grid positioning,
bilateral page margins, local images, responsive behavior, and exact typography:

1. Use `QWebEngineView` as the primary renderer.
2. Load the real local HTML file through `QUrl.fromLocalFile(...)` and
   `QWebEngineView.setUrl(...)`.
3. Keep CSS and image paths relative to that local HTML file.
4. Keep `QTextBrowser` as a readable fallback only.
5. Do not use `QTextEdit.setHtml()` or `QTextBrowser.setHtml()` as the primary
   rendering path for this profile. Those methods support only a limited subset of
   browser CSS and can silently remove the orange top rule, dark-blue chapter
   opener, bilateral gray margins, CSS grid, and intended line spacing.
6. Do not declare the layout correct from source inspection alone. Open the real
   help window in the application after restarting the process and inspect the
   rendered page.

A patch that changes only Markdown or HTML while leaving an incompatible primary
renderer in place is incomplete. Correct the rendering boundary first, then refine
content and styling.

### Required renderer pattern

```python
from pathlib import Path

from PySide6.QtCore import QUrl
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QTextBrowser


def create_help_view(html_path: Path):
    try:
        view = QWebEngineView()
        view.setUrl(QUrl.fromLocalFile(str(html_path.resolve())))
        return view
    except Exception:
        fallback = QTextBrowser()
        fallback.setOpenExternalLinks(False)
        fallback.setSource(QUrl.fromLocalFile(str(html_path.resolve())))
        return fallback
```

The exact owner implementation may differ, but it must preserve the same behavior:
browser-grade primary rendering from a local-file URL and a safe readable fallback.

### Visual failure diagnosis

When the page lacks the top orange rule, blue title banner, bilateral margins, grid
placement, or correct paragraph rhythm, investigate the renderer and loading path
before rewriting the CSS. These failures commonly indicate that a rich-text widget
is interpreting the HTML instead of a browser engine.

## Exact visual model

### Page shell

- Center a white book page on a light gray application background.
- Desktop page maximum width: `7in`.
- Desktop minimum page height: `9.2in`.
- Outer vertical margin: `24px`.
- Internal padding: approximately `0.62in 0.66in 0.54in`.
- Page background: `#ffffff`.
- Surrounding background: `#e5e7eb`.
- Use one continuous vertical article without a permanent sidebar.

### Font system

Body and explanatory text:

```css
"Minion Pro", "Adobe Garamond Pro", "Source Serif 4", Georgia, serif
```

- Typical body size: `10.5pt`.
- Typical line height: `1.36`.
- Body color: `#1a1a2e`.

Titles and labels:

```css
"Myriad Pro Cond", "Roboto Condensed", "Arial Narrow", Arial, sans-serif
```

Code and paths:

```css
"Ubuntu Mono", Consolas, "JetBrains Mono", monospace
```

Use only local/system font fallbacks. Do not add remote font dependencies.

### Chapter opener

- Use a full-width dark navy banner with `background: #0f3460`.
- Use an orange top rule with `border-top: 8px solid #ea580c`.
- Desktop grid: `grid-template-columns: minmax(0, 1fr) 2in`.
- Column gap: `20px`.
- Internal spacing: approximately `0.45in 0.5in 0.38in`.
- Bottom separation from body: `26px`.
- Left column order: publication label, main title, subtitle.
- Right column: one small landscape opener image.

Publication label:

- Text: `KANDA Reasoner Help`.
- Color: `#dbeafe`.
- Condensed sans-serif, bold, approximately `12px`.
- Bottom margin: `8px`.

Main title:

- White, bold, condensed sans-serif.
- Approximately `34px` with line-height `1.05`.
- Bottom margin: approximately `12px`.

Subtitle:

- Color: `#e2e8f0`.
- Serif, approximately `15px`, line-height `1.25`.
- Keep to one or two short lines.

Opener image:

- Landscape image filling the `2in` column.
- Preserve aspect ratio.
- Use `border: 3px solid #f59e0b`.
- Provide meaningful alt text.

### Major headings

- Use dark navy `#0f3460`.
- Condensed sans-serif, bold, approximately `22px`.
- Line-height: `1.12`.
- Top margin: `28px`.
- Bottom margin: `8px`.
- Bottom padding: `5px`.
- Orange underline: `border-bottom: 2px solid #ea580c`.

### Paragraphs and lists

- Paragraph spacing: `margin: 0 0 10px`.
- One idea per paragraph; normally one to three sentences.
- Use bold selectively for interface labels and critical terms.
- Ordered lists are mandatory for procedures where sequence matters.
- List spacing: `margin: 8px 0 12px 20px; padding: 0`.
- Keep semantic HTML list elements; do not manually type list numbers.

### Section drawings

Use semantic figure markup:

```html
<figure class="section-drawing">
  <img src="../assets/drawings/example.png" alt="Meaningful description">
  <figcaption>Instructional caption.</figcaption>
</figure>
```

- Center images and preserve aspect ratio.
- Use `max-width: 100%; height: auto`.
- Use a subtle `1px` border in `#cbd5e1`.
- Use white image background.
- Figure margin: `18px 0`.
- Caption: left aligned, italic serif, approximately `10pt`, top margin `6px`.
- Captions must reinforce the instruction, not merely name the scene.

### Artwork direction

- Prefer narrative editorial illustrations with warm paper/watercolor character.
- Use blue uniforms and restrained orange/rust accents when consistent with the adopted page set.
- Every image must teach a difficult concept through a clear visual analogy.
- Avoid decorative filler, remote images, and unlicensed assets.
- Keep opener art simpler than section art.
- Reuse unchanged PNG archives; regenerate them only when PNG inventory, bytes, names, archive contract, or size cap changes.

### Callouts

Use a pale rectangular callout with a colored left rule and circular icon:

```html
<div class="callout callout-warning">
  <div class="callout-icon">!</div>
  <div>Warning text.</div>
</div>
```

Layout contract:

```css
display: grid;
grid-template-columns: 42px minmax(0, 1fr);
gap: 10px;
margin: 14px 0;
padding: 12px;
align-items: start;
background: #f8fafc;
border-left: 5px solid currentColor;
```

Icon contract:

- `34px` by `34px`.
- `2px` circular border.
- Centered bold condensed sans-serif character.
- Use `1`, `!`, or `i` according to meaning.

Semantic colors:

- Note: `#2563a8`.
- Warning: `#ea580c`.
- Tip: `#d97706`.
- Success: `#16a34a`.

Use the class names actually supported by the current stylesheet. Reconcile HTML and CSS naming before generation.

### Subheadings, code, tables, footer

- Subheadings: approximately `16px`, dark navy, top margin `18px`, bottom margin `6px`, no orange underline.
- Inline code and paths use the monospace stack and wrap safely.
- Tables use full width, collapsed borders, dark navy header, white header text, compact padding, and wrapped cells.
- Optional footer uses a `3px` dark navy top border, `32px` top margin, `8px` top padding, and approximately `9pt` condensed sans-serif text.

### Responsive behavior

At `max-width: 760px`:

- Remove outer page margin.
- Use page padding `24px 18px`.
- Change opener from two columns to one column.
- Move the opener image below the text.
- Remove desktop minimum height.
- Preserve all semantic content and prevent horizontal overflow.

## Exact HTML skeleton

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>KANDA Help - PAGE TITLE</title>
  <link rel="stylesheet" href="../css/book_help.css">
</head>
<body>
  <article class="book-page">
    <header class="chapter-opener">
      <div>
        <p class="part-label">KANDA Reasoner Help</p>
        <h1>PAGE TITLE</h1>
        <p class="subtitle">SHORT PRACTICAL DESCRIPTION.</p>
      </div>
      <figure class="chapter-drawing">
        <img src="../assets/drawings/IMAGE.png" alt="MEANINGFUL DESCRIPTION">
      </figure>
    </header>
    <section>
      <h2>What This Tab Does</h2>
      <p><strong>In plain English:</strong> ...</p>
    </section>
    <section>
      <h2>Before You Start</h2>
      <figure class="section-drawing">
        <img src="../assets/drawings/IMAGE.png" alt="MEANINGFUL DESCRIPTION">
        <figcaption>Instructional caption.</figcaption>
      </figure>
      <ol>
        <li>Step one.</li>
        <li>Step two.</li>
      </ol>
      <div class="callout callout-warning">
        <div class="callout-icon">!</div>
        <div>Warning text.</div>
      </div>
    </section>
  </article>
</body>
</html>
```

## Content rhythm

Use this recurring order:

1. Major heading and orange underline.
2. Optional instructional image.
3. Optional italic caption.
4. Plain-language paragraph.
5. Procedure, list, table, or path example.
6. Optional warning or high-value callout.
7. Whitespace before the next major heading.

Do not place two large illustrations back-to-back without explanatory content.

## Source, manifest, and renderer contract

- Canonical source remains Markdown under the current source directory.
- Rendered HTML is generated output and must remain traceable to source identity and version.
- Register page ID, title, tab ID, source, rendered HTML, CSS, legacy catalog, and complete local asset list in the help manifest.
- Use relative local paths only.
- Primary renderer must use `QWebEngineView` with a real local-file URL for the exact profile; fallback must remain readable in `QTextBrowser`.
- Do not require JavaScript or a network connection for core reading.

## Validation checklist

Before claiming completion, verify:

1. Canonical Markdown and generated HTML agree.
2. Shared CSS is reused rather than duplicated.
3. All assets exist and are listed in the manifest.
4. Every image has meaningful alt text.
5. Desktop rendering matches the adopted page profile.
6. Narrow rendering has no horizontal overflow.
7. Headings, lists, paths, tables, and callouts remain readable in fallback rendering.
8. No remote fonts, remote images, tracking, or hidden network dependencies were introduced.
9. PNG archives were rebuilt only when their content or archive contract changed.
10. The real help window uses `QWebEngineView` with `QUrl.fromLocalFile(...)` and `setUrl(...)` as the primary path.
11. No primary path uses `QTextEdit.setHtml()` or `QTextBrowser.setHtml()` for the exact profile.
12. The restarted application was visually inspected for the orange top rule, dark-blue chapter opener, bilateral margins, image placement, and paragraph rhythm; otherwise report `NOT_RUN` or `INCONCLUSIVE`.

## Failure conditions

Return `BLOCKED` or `INCONCLUSIVE` rather than claiming success when any of these apply:

- the primary help renderer is unknown;
- the page is displayed only through `setHtml()` on a rich-text widget;
- CSS is correct in source but the real help window has not been inspected;
- local CSS or image URLs do not resolve from the rendered HTML location;
- the application process was not restarted after changing the Python renderer;
- the top rule, blue opener, bilateral margins, or line spacing differs from the adopted model.

## Required output

Return a `KANDA HELP EXACT LAYOUT RECORD` containing:

- target help page and audience;
- source, rendered HTML, CSS, manifest, renderer, and asset identities;
- exact layout elements applied;
- image and caption plan;
- accessibility and responsive checks;
- PNG reuse decision;
- renderer identity and local-file loading evidence;
- restarted-application rendered inspection evidence;
- unresolved differences from the adopted model;
- source-write authorization: `NO` unless separately granted.

## Version history

- 1.1.0: made browser-grade local-file rendering a non-negotiable layout contract; prohibited rich-text `setHtml()` as the primary path; added renderer-first diagnosis and real-window visual gates.
- 1.0.0: introduced the exact reusable KANDA desktop-help layout blueprint.
