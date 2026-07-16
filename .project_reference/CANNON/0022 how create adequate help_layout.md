# Help Document Layout Prompt

Use this prompt when asking an AI to create a user-facing help document for KANDA Reasoner or related tools.

```text
You are an experienced programmer, technical-book designer, and prompt-engineering documentation specialist. You create help documents that are not only accurate, but also comfortable to read, visually stimulating, and professionally laid out like a high-quality printed technical book.

When creating a document for the user, design it with the following reference characteristics. Do not copy publisher branding, logos, proprietary cover art, or exact page artwork. Instead, reproduce the design language as an original technical-book layout.

Overall document feeling:
- Serious, readable, compact, and editorial.
- Looks like a professionally typeset programming/AI book, not a web landing page.
- Uses generous white space, strong typographic hierarchy, and clean page rhythm.
- Prioritizes comprehension: every image, table, callout, and caption must teach something.

Page format:
- Use a compact technical-book page proportion, close to 7 x 9.2 inches for print/PDF.
- Use a single main text column.
- Keep wide outer margins and stable top/bottom margins.
- Use page footers with a thin horizontal rule.
- Put page number plus chapter/section title in the footer.
- Avoid decorative backgrounds, gradients, cards, and marketing-style hero sections.

Typography:
- Body text: classic book serif, preferably Minion Pro. If unavailable, use Adobe Garamond, Source Serif, Georgia, or another readable literary serif.
- Headings: narrow/condensed sans serif, preferably Myriad Pro Condensed or Myriad Pro Semibold Condensed. If unavailable, use Source Sans 3 Condensed, Roboto Condensed, Arial Narrow, or a similar condensed sans.
- Code and inline technical names: Ubuntu Mono. If unavailable, use Consolas, Menlo, JetBrains Mono, or another clean monospaced font.
- Cover/title typography may use a modern geometric sans such as Gilroy, Avenir, Inter, or Source Sans, with very large bold title text.
- Body text should be around 10.5 pt in print/PDF equivalents.
- Code should be slightly smaller or equal to body size, around 9.5-10 pt.
- Section headings should be bold condensed sans, roughly 1.4-2.4x body size depending on level.
- Use italics for captions, emphasis, book-style terms, and figure/table titles.

Color palette:
- Main body text: black or near-black (#000000 or #231f20).
- Primary accent for links, figure references, table references, and cross-references: deep red (#990000).
- Secondary muted accent for subtitles or cover-style secondary text: muted purple-gray (#735472).
- Tip callout icon/accent: green/teal.
- Note callout icon/accent: blue/indigo.
- Warning/caution callout icon/accent: orange-red.
- Use color sparingly. The interior should remain mostly black text on white paper.

Headings and hierarchy:
- Chapter or major section openers should feel calm and book-like.
- Use large condensed sans headings.
- For table of contents or major structural lists, use dot leaders and strong alignment.
- Use numbered chapter/section labels when useful.
- Keep heading spacing consistent: clear space before headings, tighter space after headings.

Paragraph style:
- Use book-style paragraphs with careful line length.
- Prefer justified or visually even text blocks for print/PDF.
- Do not make paragraphs too wide.
- Avoid excessive bullets; use prose first, lists only when they improve scanning.
- Use compact but readable line spacing.

Images and figures:
- Include illustrative and stimulating images where they help the reader understand.
- Prefer original technical diagrams, workflow illustrations, screenshots, annotated UI examples, evaluation diagrams, router-flow diagrams, data-flow diagrams, or architecture drawings.
- Avoid generic stock images.
- Images should be instructive, not decorative filler.
- Place figures inline near the explanation they support.
- Most figures should be full text-column width with a thin border or clear boundary.
- Use italic captions below figures in the format: "Figure X-Y. Caption text."
- Cross-reference figures in body text using the deep red accent.
- For KANDA documentation, suitable figure types include:
  - prompt router flow diagrams
  - adviser -> assistant -> copilot/piloto maturity diagrams
  - freeze-memory lifecycle diagrams
  - schema boundary diagrams
  - test harness and validation pipeline diagrams
  - GUI screenshots or screenshot-like mockups
  - risk-boundary checklists visualized as flowcharts

Tables:
- Use compact technical tables.
- Header row should be black or very dark with white text.
- Body cells should use thin gray rules.
- Use monospaced font for parameters, field names, paths, and code-like values.
- Use table captions above or below the table, italicized, in the format: "Table X-Y. Caption text."
- Keep tables readable, not ornamental.

Code and command blocks:
- Use monospaced type.
- Keep code examples compact and readable.
- Use light-gray background or simple boxed treatment only when useful.
- Avoid loud syntax colors; if syntax color is used, keep it restrained.
- Inline code should blend with body text and not dominate the page.

Callouts:
- Use three book-style callout types:
  - Tip: green/teal original icon, for practical advice.
  - Note: blue/indigo original icon, for neutral context.
  - Warning/Caution: orange-red original icon, for risks and governance boundaries.
- Callouts should use a small icon at the left and text to the right.
- Do not use copied animal icons or publisher-specific art.
- Keep callouts rare and meaningful.

Footer/running heads:
- Use a thin rule near the bottom.
- Put the page number and current chapter/section title in small condensed sans.
- Alternate left/right placement if making a real book/PDF.

Cover or first page:
- If making a cover or first page, use:
  - a very large bold sans title
  - a restrained subtitle in muted purple-gray
  - author/project name near the lower area
  - one strong original illustrative image related to the document subject
- Do not use any publisher logo or copied cover animal.
- For KANDA, possible original cover images include:
  - a router/control-room illustration
  - a prompt-map diagram
  - a shielded decision pipeline
  - an abstract adviser/assistant/copilot progression

Document behavior:
- Every help document must be useful as a standalone reading artifact.
- Start with the user problem and the mental model.
- Then show the workflow.
- Then show examples.
- Then show risks, boundaries, and validation steps.
- End with a concise operational checklist.

KANDA-specific documentation rule:
- When documenting KANDA Reasoner, preserve governance language:
  - adviser means recommendation only
  - assistant means checked recommendation under stronger validation
  - copilot/piloto means governed participation after promotion criteria
  - freeze memory is durable project state
  - risk boundaries require slow, step-by-step validation
  - no runtime authority should be implied unless explicitly authorized

Quality bar:
- The final document should look like it belongs in a serious AI/programming book.
- It should be beautiful through typography, spacing, diagrams, and clarity, not through decoration.
- If images are needed, create original instructive images or detailed image prompts for them.
- Never copy copyrighted page art, publisher branding, logos, or exact proprietary illustrations.
```

## Canonical Add-On: Desktop Help File Creation Paradigm

This add-on defines the standard way KANDA Reasoner help files should be authored, rendered, and opened inside the desktop GUI.

### Canonical Format Decision

Use two layers:

- `.md` files are the canonical editable source.
- `.html` files are the rendered desktop help documents.
- `.css` files hold the shared book-style layout.
- `assets/` holds original diagrams, screenshots, and instructional images.
- Optional `.pdf` exports may be generated later for printable manuals, but PDF is not the primary in-app format.

Do not use Markdown alone for the desktop help experience. Markdown is good for editing, but it cannot reliably preserve the book-like design language: font hierarchy, page rhythm, callouts, figure captions, table styling, running footers, and image treatment.

Do not use PDF as the primary in-app help format. PDF is useful for export, but local HTML is easier to render, navigate, update, test, and integrate inside a Qt desktop window.

### Desktop Rendering Rule

Help must open from a KANDA desktop window, not from an external browser.

Primary renderer:

- Use `QWebEngineView` to render local offline HTML/CSS inside the desktop app.
- Load only local project help files and local help assets.
- Do not require network access.
- Do not load remote scripts, fonts, trackers, CDNs, or web resources.

Fallback renderers:

- If `QWebEngineView` is unavailable, use `QTextBrowser` with simplified HTML.
- If rich HTML cannot be rendered, fall back to plain text in a read-only Qt text widget.
- The fallback must preserve the help content even if it cannot preserve the full book layout.

### Canonical Folder Structure

Use this structure for in-app help:

```text
kanda_reasoner_app/reasoner_tools_gui_shell/help_docs/
  manifest.json
  css/
    book_help.css
  assets/
    adviser_flow.png
    freeze_lifecycle.png
    router_boundary.png
  source/
    adviser_overview.md
    freeze_memory.md
    shadow_mode_boundary.md
  rendered/
    adviser_overview.html
    freeze_memory.html
    shadow_mode_boundary.html
```

`source/` is for human-editable help content.

`rendered/` is for generated HTML consumed by the GUI.

`css/book_help.css` is the shared style system that implements the book-like visual language from this canon.

`assets/` must contain original images only. Do not copy publisher art, logos, exact page art, or proprietary illustrations.

`manifest.json` should list every help page, title, source path, rendered path, asset dependencies, and intended GUI entry point.

### Help Page Authoring Rules

Every source `.md` help page should use a predictable structure:

```text
# Page Title

Short mental model.

## What Problem This Solves

## How The Workflow Works

## Step-by-Step Use

## Examples

## Risks And Boundaries

## Validation Or Safety Checks

## Operational Checklist
```

For KANDA Reasoner help, every page that touches routing, adviser, assistant, pilot/copilot, freeze memory, prompt loading, or runtime behavior must explicitly state the authority boundary.

Examples:

- Adviser means recommendation only.
- Assistant means checked recommendation under stronger validation.
- Copilot/piloto means governed participation after promotion criteria.
- Freeze memory is durable project state.
- Risk boundaries require slow, step-by-step validation.
- Runtime authority must not be implied unless explicitly authorized.

### HTML Generation Rules

Generated HTML must be local, static, and deterministic.

Each rendered page should:

- Reference `../css/book_help.css`.
- Use semantic HTML: `article`, `section`, `figure`, `figcaption`, `table`, `thead`, `tbody`, `code`, `pre`.
- Use relative paths for assets.
- Include no remote resources.
- Include no inline network calls.
- Include no tracking scripts.
- Include no JavaScript unless a specific help interaction is governed and tested.

Recommended generated HTML shape:

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>KANDA Help - Adviser Overview</title>
  <link rel="stylesheet" href="../css/book_help.css">
</head>
<body>
  <article class="book-page">
    <header class="page-header">
      <p class="part-label">KANDA Reasoner Help</p>
      <h1>Adviser Overview</h1>
    </header>

    <section>
      <h2>What Problem This Solves</h2>
      <p>...</p>
    </section>

    <figure>
      <img src="../assets/adviser_flow.png" alt="Adviser recommendation flow">
      <figcaption>Figure 1-1. Adviser recommendations remain non-authoritative.</figcaption>
    </figure>

    <footer class="running-footer">
      <span>Adviser Overview</span>
      <span>1</span>
    </footer>
  </article>
</body>
</html>
```

### CSS Implementation Rules

The shared CSS should implement the technical-book style:

- White page background.
- Near-black body text.
- Serif body font stack.
- Condensed sans heading font stack.
- Monospace code font stack.
- Deep red cross-reference accent.
- Muted purple-gray subtitle accent.
- Thin footer rules.
- Full-width figures with captions.
- Compact tables with dark header rows.
- Tip, note, and warning callouts with restrained color.

Recommended CSS foundations:

```css
:root {
  --body-text: #231f20;
  --ink: #000000;
  --xref: #990000;
  --subtitle: #735472;
  --rule: #9a9a9a;
  --paper: #ffffff;
  --table-rule: #b8b8b8;
  --tip: #079b7a;
  --note: #465da8;
  --warning: #e8663f;
}

body {
  margin: 0;
  background: #d8d8d8;
  color: var(--body-text);
  font-family: "Minion Pro", "Adobe Garamond Pro", "Source Serif 4", Georgia, serif;
}

.book-page {
  box-sizing: border-box;
  width: min(100%, 7in);
  min-height: 9.2in;
  margin: 24px auto;
  padding: 0.72in 0.72in 0.58in;
  background: var(--paper);
}

h1,
h2,
h3,
.running-footer {
  font-family: "Myriad Pro Cond", "Roboto Condensed", "Arial Narrow", Arial, sans-serif;
}

h1 {
  font-size: 31px;
  line-height: 1.05;
}

h2 {
  font-size: 22px;
  line-height: 1.12;
  margin-top: 28px;
}

p {
  font-size: 10.5pt;
  line-height: 1.36;
}

code,
pre {
  font-family: "Ubuntu Mono", Consolas, "JetBrains Mono", monospace;
}

a,
.xref {
  color: var(--xref);
}

figure {
  margin: 18px 0;
}

figure img {
  max-width: 100%;
  border: 1px solid var(--table-rule);
}

figcaption {
  margin-top: 6px;
  font-style: italic;
}

table {
  width: 100%;
  border-collapse: collapse;
  font-size: 9.5pt;
}

thead th {
  background: var(--ink);
  color: white;
}

td,
th {
  border: 1px solid var(--table-rule);
  padding: 5px 7px;
  vertical-align: top;
}

.running-footer {
  display: flex;
  justify-content: space-between;
  margin-top: 32px;
  padding-top: 8px;
  border-top: 1px solid var(--rule);
  font-size: 9pt;
  font-weight: 700;
}
```

### Code Architecture Rules

The GUI should not embed help text directly in Python widgets.

Preferred architecture:

- A help manifest lists available pages.
- A help document loader resolves safe local paths.
- A help renderer opens the selected rendered HTML in a desktop Qt help window.
- A fallback renderer opens simplified HTML or plain text if WebEngine is unavailable.

Suggested implementation modules:

```text
kanda_reasoner_app/reasoner_tools_gui_shell/help_docs/
  __init__.py
  manifest.py
  path_resolver.py
  renderer.py
  fallback_renderer.py
```

The renderer must:

- Use project-local paths only.
- Reject paths outside the help-docs directory.
- Prefer read-only rendering.
- Avoid network requests.
- Avoid runtime mutation of help source files.
- Keep help rendering separate from routing, freeze memory, adviser, assistant, and copilot logic.

### Validation Rules

Every help-doc implementation patch should include tests for:

- Manifest loads successfully.
- Every source and rendered path exists.
- Every rendered HTML file references local CSS only.
- No rendered HTML file references `http://`, `https://`, CDN, tracker, or remote font URL.
- Every image path is local and exists.
- Renderer rejects path traversal.
- Fallback renderer can show content without `QWebEngineView`.
- Help code does not import or mutate routing-scorer runtime logic.

### Canonical Decision

For KANDA Reasoner, the help system paradigm is:

```text
Markdown source -> deterministic local HTML/CSS -> desktop Qt help window
```

Use `QWebEngineView` for the full book-like experience, with `QTextBrowser` and plain text as safe fallbacks.

This is the standard help-file creation and rendering pattern unless a future governed design explicitly replaces it.
