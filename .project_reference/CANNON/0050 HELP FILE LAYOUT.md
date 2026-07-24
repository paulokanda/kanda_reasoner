HANDOFF TO AI - CREATE KANDA HELP HTML WITH THE CORRECT EXACT LAYOUT

Purpose

Create or update a KANDA Reasoner help file using the same exact visual structure and rendering method as the approved Show Project to AI help page.

This is not only a writing task.

The result is considered correct only when:

The HTML structure is correct.
The shared or approved CSS is applied correctly.
Local images load correctly.
The help window uses a browser-grade renderer.
The final page is visually inspected inside the real KANDA Reasoner application.
The orange-red top line, blue title area, bilateral margins, typography, spacing, image layout, and section rhythm match the canonical KANDA desktop-help design.

Critical rendering rule

Use QWebEngineView as the primary renderer.

Load the real local HTML file using:

from PySide6.QtCore import QUrl
from PySide6.QtWebEngineWidgets import QWebEngineView

view = QWebEngineView()
view.setUrl(QUrl.fromLocalFile(str(html_path.resolve())))

Do not use either of these as the primary rendering method:

QTextEdit.setHtml(...)
QTextBrowser.setHtml(...)

Those rich-text methods do not reliably preserve the complete CSS required by the canonical layout. They may remove or alter:

the orange-red top border;
the dark-blue chapter opener;
bilateral gray margins;
the centered white page;
CSS grid positioning;
title-and-image alignment;
paragraph line height;
paragraph and heading spacing;
responsive behavior;
local stylesheet behavior.

QTextBrowser may exist only as a readable fallback when QWebEngineView is unavailable.

A patch that changes only Markdown or HTML while leaving an incompatible primary renderer in place is incomplete.

Required source and artifact structure

Before editing, identify the current help implementation and locate:

Canonical Markdown source.
Rendered HTML file.
CSS file.
Local image assets.
Manifest or help registry.
Python code that opens the help window.
Existing validator or test.
Existing approved help page to use as the visual reference.

Do not guess these paths.

Inspect the current project source and use the real current owners.

The canonical editable content should remain separate from the rendered artifact.

Preferred structure:

help_source/
    feature_help.md

rendered or feature folder/
    feature_help.html

css/
    book_help.css

assets/
    drawings/
        feature_opener.png
        feature_section_01.png
        feature_section_02.png

The exact project may use different folders. Preserve the current project architecture.

Canonical visual target

The page must appear as a centered white book page on a light-gray background.

Desktop page rules:

body {
    margin: 0;
    background: #e5e7eb;
    color: #1a1a2e;
}

.book-page {
    box-sizing: border-box;
    width: 100%;
    max-width: 7in;
    min-height: 9.2in;
    margin: 24px auto;
    padding: 0.62in 0.66in 0.54in;
    background: #ffffff;
}

The gray background must remain visible on both the left and right sides of the white page.

Do not stretch the white content page to the full application width on desktop.

Chapter opener

The page must begin with the chapter opener.

Required visible elements:

Orange-red horizontal line across the top.
Dark-blue rectangular title area.
Small pale publication label.
Large white page title.
Short pale subtitle.
Small landscape image on the right.
Correct internal padding and vertical alignment.

Recommended structure:

<header class="chapter-opener">
    <div class="chapter-copy">
        <p class="part-label">KANDA Reasoner Help</p>
        <h1>Feature Name</h1>
        <p class="subtitle">
            Short plain-English explanation of what this tab helps the user do.
        </p>
    </div>

    <figure class="chapter-drawing">
        <img
            src="relative/path/to/opener_image.png"
            alt="Meaningful description of the instructional illustration">
    </figure>
</header>

Required styling:

.chapter-opener {
    display: grid;
    grid-template-columns: minmax(0, 1fr) 2in;
    gap: 20px;
    align-items: center;

    margin:
        -0.62in
        -0.66in
        26px;

    padding:
        0.45in
        0.5in
        0.38in;

    border-top: 8px solid #ea580c;
    background: #0f3460;
}

The negative horizontal margins allow the opener to reach the left and right edges of the white page.

Do not place the top rule as an unrelated decorative element. It should be the top border of the chapter opener.

Publication label

.part-label {
    margin: 0 0 8px;
    color: #dbeafe;
    font-family:
        "Myriad Pro Cond",
        "Roboto Condensed",
        "Arial Narrow",
        Arial,
        sans-serif;
    font-size: 12px;
    font-weight: 700;
}

Main title

.chapter-opener h1 {
    margin: 0 0 12px;
    color: #ffffff;
    font-family:
        "Myriad Pro Cond",
        "Roboto Condensed",
        "Arial Narrow",
        Arial,
        sans-serif;
    font-size: 34px;
    font-weight: 700;
    line-height: 1.05;
}

Subtitle

.subtitle {
    margin: 0;
    color: #e2e8f0;
    font-family:
        "Minion Pro",
        "Adobe Garamond Pro",
        "Source Serif 4",
        Georgia,
        serif;
    font-size: 15px;
    line-height: 1.25;
}

Opener image

.chapter-drawing {
    margin: 0;
}

.chapter-drawing img {
    display: block;
    width: 100%;
    height: auto;
    border: 3px solid #f59e0b;
    background: #ffffff;
}

The image should remain proportionate and must not be stretched.

Typography

Body font stack:

font-family:
    "Minion Pro",
    "Adobe Garamond Pro",
    "Source Serif 4",
    Georgia,
    serif;

Body styling:

.book-page {
    font-size: 10.5pt;
    line-height: 1.36;
}

Heading and interface-label stack:

font-family:
    "Myriad Pro Cond",
    "Roboto Condensed",
    "Arial Narrow",
    Arial,
    sans-serif;

Monospace stack:

font-family:
    "Ubuntu Mono",
    Consolas,
    "JetBrains Mono",
    monospace;

Use the monospace font for:

paths;
file names;
commands;
validation markers;
machine-readable statuses;
code examples.

Paragraph spacing

Use controlled paragraph spacing.

p {
    margin: 0 0 10px;
}

Do not allow browser-default large paragraph gaps.

Do not remove all paragraph spacing.

The body should be compact, readable, and similar to a printed technical manual.

Major section headings

Each major section should use a dark-blue heading with an orange underline.

h2 {
    margin: 28px 0 8px;
    padding-bottom: 5px;

    border-bottom: 2px solid #ea580c;

    color: #0f3460;
    font-family:
        "Myriad Pro Cond",
        "Roboto Condensed",
        "Arial Narrow",
        Arial,
        sans-serif;
    font-size: 22px;
    font-weight: 700;
    line-height: 1.12;
}

Do not put the orange line above the heading.

The line belongs immediately below the heading.

Subheadings

h3 {
    margin: 18px 0 6px;

    color: #0f3460;
    font-family:
        "Myriad Pro Cond",
        "Roboto Condensed",
        "Arial Narrow",
        Arial,
        sans-serif;
    font-size: 16px;
    font-weight: 700;
    line-height: 1.2;
}

Subheadings normally do not use the orange underline.

Lists

Use semantic HTML:

<ol>
    <li>First step.</li>
    <li>Second step.</li>
</ol>
<ul>
    <li>First item.</li>
    <li>Second item.</li>
</ul>

Recommended spacing:

ol,
ul {
    margin: 8px 0 12px 20px;
    padding: 0;
}

li {
    margin-bottom: 5px;
}

Use numbered lists when order matters.

Use bullets for contents, alternatives, or explanations.

Do not manually type fake list numbers inside paragraphs.

Section drawings

Use large instructional images only when they teach a concept.

Recommended structure:

<figure class="section-drawing">
    <img
        src="relative/path/to/section_image.png"
        alt="Meaningful accessible description">
    <figcaption>
        Short instructional caption that reinforces the lesson.
    </figcaption>
</figure>

Recommended styling:

.section-drawing {
    margin: 18px 0;
}

.section-drawing img {
    display: block;
    max-width: 100%;
    height: auto;
    margin: 0 auto;
    border: 1px solid #cbd5e1;
    background: #ffffff;
}

.section-drawing figcaption {
    margin-top: 6px;
    font-size: 10pt;
    font-style: italic;
    line-height: 1.3;
}

Do not use decorative images without instructional value.

Do not distort images.

Do not load remote images.

Use local relative paths.

Callout boxes

Use callouts for:

warnings;
required order;
common mistakes;
first-time user reminders;
important safety gates.

Recommended HTML:

<div class="callout callout-warning">
    <div class="callout-icon">!</div>
    <div>
        <strong>Important:</strong>
        Explanation in plain English.
    </div>
</div>

Recommended shared styling:

.callout {
    display: grid;
    grid-template-columns: 42px minmax(0, 1fr);
    gap: 10px;
    align-items: start;

    margin: 14px 0;
    padding: 12px;

    background: #f8fafc;
    border-left: 5px solid currentColor;
}

.callout-icon {
    display: flex;
    width: 34px;
    height: 34px;
    align-items: center;
    justify-content: center;

    border: 2px solid currentColor;
    border-radius: 50%;

    font-family:
        "Myriad Pro Cond",
        "Roboto Condensed",
        "Arial Narrow",
        Arial,
        sans-serif;
    font-weight: 700;
}

Semantic colors:

.callout-note {
    color: #2563a8;
}

.callout-warning {
    color: #ea580c;
}

.callout-tip {
    color: #d97706;
}

.callout-success {
    color: #16a34a;
}

.callout > div:last-child {
    color: #1a1a2e;
}

Important class rule

Do not create HTML classes that the stylesheet does not define.

For example, do not use:

<div class="callout note">

when the CSS expects:

<div class="callout callout-note">

Verify that the HTML class names and CSS selectors agree exactly.

Tables

Use tables only when comparison is clearer than prose.

Recommended styling:

table {
    width: 100%;
    margin: 14px 0;
    border-collapse: collapse;
    table-layout: fixed;
    font-size: 9.5pt;
}

th,
td {
    padding: 7px 8px;
    border: 1px solid #cbd5e1;
    vertical-align: top;
    overflow-wrap: anywhere;
}

th {
    background: #0f3460;
    color: #ffffff;
    font-family:
        "Myriad Pro Cond",
        "Roboto Condensed",
        "Arial Narrow",
        Arial,
        sans-serif;
    font-weight: 700;
}

Code and paths

Long paths must wrap.

code,
pre {
    font-family:
        "Ubuntu Mono",
        Consolas,
        "JetBrains Mono",
        monospace;
    overflow-wrap: anywhere;
    word-break: break-word;
}

pre {
    padding: 10px 12px;
    overflow-x: auto;
    border: 1px solid #cbd5e1;
    background: #f8fafc;
}

Do not allow paths to create horizontal overflow.

Responsive behavior

At narrow widths, the page must remain usable.

@media (max-width: 760px) {
    .book-page {
        max-width: none;
        min-height: 0;
        margin: 0;
        padding: 24px 18px;
    }

    .chapter-opener {
        grid-template-columns: 1fr;

        margin:
            -24px
            -18px
            24px;

        padding:
            28px
            24px
            24px;
    }

    .chapter-drawing {
        max-width: 280px;
    }
}

The image should move below the title on narrow windows.

The page must not create horizontal scrolling.

HTML base structure

Use semantic HTML.

<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta
        name="viewport"
        content="width=device-width, initial-scale=1">
    <title>KANDA Help - Feature Name</title>

    <link
        rel="stylesheet"
        href="relative/path/to/book_help.css">
</head>

<body>
    <article class="book-page">
        <header class="chapter-opener">
            <div class="chapter-copy">
                <p class="part-label">
                    KANDA Reasoner Help
                </p>

                <h1>
                    Feature Name
                </h1>

                <p class="subtitle">
                    Short practical description for a first-time user.
                </p>
            </div>

            <figure class="chapter-drawing">
                <img
                    src="relative/path/to/opener.png"
                    alt="Accessible description">
            </figure>
        </header>

        <section>
            <h2>What This Tab Does</h2>

            <p>
                <strong>In plain English:</strong>
                Explain the purpose without programming jargon.
            </p>
        </section>

        <section>
            <h2>Before You Start</h2>

            <figure class="section-drawing">
                <img
                    src="relative/path/to/section.png"
                    alt="Accessible description">

                <figcaption>
                    Instructional caption.
                </figcaption>
            </figure>

            <ol>
                <li>First step.</li>
                <li>Second step.</li>
            </ol>

            <div class="callout callout-warning">
                <div class="callout-icon">!</div>

                <div>
                    <strong>Important:</strong>
                    Explain the warning in plain English.
                </div>
            </div>
        </section>
    </article>
</body>
</html>

Plain-English writing requirements

Write for a first-time non-programmer user.

Assume the user:

does not know what a manifest is;
does not know what a project root is;
may not understand validation;
may not understand generated files;
may be afraid of damaging the project;
needs to know exactly what button to press;
needs to know what success looks like;
needs to know what not to do.

For every important control, explain:

What it is.
Why it exists.
When to use it.
What happens after clicking it.
What a successful result looks like.
What common mistake to avoid.
What to do if it fails.

Prefer wording such as:

In plain English:
Use this when:
What happens next:
You should see:
Do not do this:
If this fails:

Avoid unexplained jargon.

When technical terms are required, explain them immediately.

Markdown source requirements

The Markdown source is canonical.

The HTML is the rendered output.

The Markdown should include:

page title;
subtitle;
section headings;
plain-English instructions;
ordered procedures;
warnings;
paths and markers in backticks;
image notes;
alt text;
captions;
asset paths;
image provenance or status when required.

Recommended image note:

Image note:

- Subject: A person reviewing a validated feature before preserving it.
- Asset path: assets/drawings/freeze_opener.png
- Alt text: A user reviewing a completed feature before placing it into protected memory.
- Caption: Validate first, preview second, confirm only when everything is correct.
- Artwork status: primary_characterful_raster

Do not silently edit only the HTML and leave the canonical Markdown outdated.

Manifest or registry requirements

Register every help file using the project’s current manifest or registry.

Include, where supported:

unique page ID;
title;
tab ID;
canonical Markdown source path;
rendered HTML path;
CSS path;
complete asset list;
legacy catalog reference;
renderer or help route.

Do not invent a second help registry if one already exists.

PNG asset reuse rule

Do not regenerate, copy, or package PNG assets merely because text or HTML changed.

Reuse existing PNG files when:

the relative path is unchanged;
the file content is unchanged;
the SHA-256 is unchanged;
the image inventory is unchanged;
the archive contract is unchanged.

Regenerate or update the PNG package only when:

an image is added;
an image is removed;
an image is renamed;
image bytes change;
a PNG is corrupted;
selected package-size or archive rules change.

The help patch may update Markdown, HTML, CSS, or renderer code without replacing unchanged PNGs.

Renderer implementation

Primary:

from pathlib import Path

from PySide6.QtCore import QUrl
from PySide6.QtWebEngineWidgets import QWebEngineView


def create_help_view(html_path: Path) -> QWebEngineView:
    """Create the primary browser-grade local help view."""
    resolved_path = html_path.resolve()

    if not resolved_path.is_file():
        raise FileNotFoundError(
            f"Help HTML file does not exist: {resolved_path}"
        )

    view = QWebEngineView()
    view.setUrl(QUrl.fromLocalFile(str(resolved_path)))
    return view

Fallback:

from pathlib import Path

from PySide6.QtWidgets import QTextBrowser


def create_help_fallback(html_path: Path) -> QTextBrowser:
    """Create a readable fallback when QWebEngine is unavailable."""
    resolved_path = html_path.resolve()

    if not resolved_path.is_file():
        raise FileNotFoundError(
            f"Help HTML file does not exist: {resolved_path}"
        )

    browser = QTextBrowser()
    browser.setOpenExternalLinks(False)
    browser.setSource(QUrl.fromLocalFile(str(resolved_path)))
    return browser

Do not feed the complete HTML string into setHtml() as the exact-layout path.

Loading the local file URL is important because it preserves:

stylesheet resolution;
image resolution;
local relative paths;
browser layout behavior;
CSS grid;
responsive CSS;
page background and margins.

Application restart rule

If Python renderer code changes, close and reopen KANDA Reasoner before evaluating the result.

Do not claim that the new renderer works based only on source inspection.

The running process may still contain the old Python code.

Visual inspection checklist

Inspect the help inside the real KANDA Reasoner application.

Do not rely only on static HTML inspection.

Confirm all of the following:

[ ] Light-gray outer background is visible.
[ ] White page is centered.
[ ] Gray margin is visible on both left and right.
[ ] Orange-red line is visible across the opener top.
[ ] Dark-blue chapter opener is visible.
[ ] KANDA Reasoner Help label is visible.
[ ] Main title is large, white, and readable.
[ ] Subtitle uses pale text.
[ ] Opener image appears on the right.
[ ] Image retains its aspect ratio.
[ ] Major headings are dark blue.
[ ] Orange underline appears beneath each major heading.
[ ] Body text uses compact serif typography.
[ ] Paragraph line height is approximately 1.36.
[ ] Paragraph gaps are consistent.
[ ] Lists are aligned correctly.
[ ] Callouts display correctly.
[ ] Tables stay within the page.
[ ] Long paths wrap.
[ ] No horizontal overflow exists.
[ ] Narrow-window behavior remains readable.

Renderer-first diagnosis rule

When any of these are missing:

orange-red top line;
dark-blue title opener;
bilateral margins;
title-and-image grid;
correct fonts;
correct paragraph spacing;
correct line height;

do not immediately rewrite the content.

First inspect:

Which Qt widget is rendering the help?
Is QWebEngineView actually being used?
Is the real local HTML file loaded through QUrl.fromLocalFile()?
Is the external CSS file resolving?
Are image paths relative to the HTML file and valid?
Was the application restarted after Python changes?
Is a fallback rich-text widget being used unexpectedly?
Is the page being loaded through setHtml() instead of setUrl()?

A visually broken page with correct HTML is often a renderer problem.

Validation requirements

The validator should check both source contracts and runtime behavior.

Static checks should confirm:

canonical Markdown exists;
rendered HTML exists;
stylesheet exists;
asset paths exist;
manifest registration exists;
orange-red border rule exists;
dark-blue opener rule exists;
centered page and bilateral margin rules exist;
line-height rule exists;
responsive breakpoint exists;
semantic structure exists;
meaningful alt text exists;
QWebEngineView is the primary renderer;
QUrl.fromLocalFile is used;
setUrl is used;
QTextEdit.setHtml is not the primary route;
QTextBrowser.setHtml is not the primary exact-layout route.

Recommended success markers:

HELP_CANONICAL_SOURCE: PASS
HELP_RENDERED_HTML: PASS
HELP_LOCAL_ASSETS: PASS
HELP_RED_TOP_RULE: PASS
HELP_BLUE_CHAPTER_OPENER: PASS
HELP_BILATERAL_PAGE_MARGINS: PASS
HELP_LINE_SPACING: PASS
HELP_PRIMARY_QWEBENGINE_RENDERER: PASS
HELP_LOCAL_FILE_URL_LOADING: PASS
HELP_RICH_TEXT_PRIMARY_REJECTED: PASS
HELP_TEXT_BROWSER_FALLBACK: PASS
HELP_IMAGE_REUSE_UNCHANGED: PASS
HELP_RESPONSIVE_LAYOUT: PASS
HELP_MANIFEST_REGISTRATION: PASS
HELP_VISUAL_INSPECTION_REQUIRED: PASS

Runtime or real-widget validation should confirm, when feasible:

QWebEngine imports successfully;
local HTML loads;
loadFinished reports success;
the stylesheet is accessible;
expected DOM elements exist;
opener background computes to the expected color;
the white page has a constrained width;
body background differs from page background;
images load successfully;
renderer startup is bounded by a timeout;
diagnostics are preserved if loading fails.

Do not interpret a QWebEngine runtime failure as an HTML defect until the exact Python/QWebEngine environment passes a minimal local-file HTML and JavaScript control.

Completion rule

Do not report the task as complete until:

Canonical source is updated.
Rendered HTML is updated.
CSS is correct.
Assets are registered.
Renderer uses QWebEngineView.
HTML loads through a local file URL.
Rich-text widgets remain fallback only.
Focused validation passes.
The application is restarted.
The actual help window is visually inspected.
The user confirms the result when final visual approval is required.

A patch that changes only Markdown or HTML while leaving an incompatible primary renderer in place is incomplete.

A validator that confirms only file existence is insufficient.

A static CSS pass does not prove the actual Qt help window is visually correct.

Expected AI response before implementation

Before changing the project, report:

HELP IMPLEMENTATION CHECK

Target help page:
Canonical Markdown owner:
Rendered HTML owner:
Shared CSS owner:
Help manifest or registry:
Current primary renderer:
Current fallback renderer:
Local asset directory:
Reference help page:
Exact source files requiring inspection:
PNG assets changed: YES / NO / UNRESOLVED
May begin implementation: YES / NO
Reason:

Expected AI response after implementation

After implementation and validation, report:

HELP COMPLETION CHECK

Canonical Markdown updated:
Rendered HTML updated:
CSS updated or reused:
Manifest updated:
QWebEngineView primary:
Local HTML URL loading:
QTextBrowser fallback:
QTextEdit.setHtml rejected as primary:
PNG assets reused or changed:
Static validation:
Runtime validation:
Application restart required:
Visual inspection completed:
Known limitations:
Status: COMPLETE / BLOCKED

Final governing statement

Use the approved Show Project to AI help file as the exact visual and architectural reference.

Do not imitate only the screenshot.

Reproduce the full system:

canonical Markdown;
semantic HTML;
approved CSS;
local assets;
manifest registration;
QWebEngineView;
local-file URL loading;
fallback behavior;
application restart;
real-window visual inspection;
focused validation.

The correct result depends on both the HTML and the renderer.