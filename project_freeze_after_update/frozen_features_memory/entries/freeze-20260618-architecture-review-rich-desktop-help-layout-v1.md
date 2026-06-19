---
freeze_id: "freeze-20260618-architecture-review-rich-desktop-help-layout-v1"
feature_title: "Architecture Review Rich Desktop Help Layout v1"
box: "reasoner_tools_gui_shell/help_docs"
status: "frozen"
date: "2026-06-18"
entry: "project_freeze_after_update/frozen_features_memory/entries/freeze-20260618-architecture-review-rich-desktop-help-layout-v1.md"
protected_paths:
  - ".project_reference/CANNON/help_layout.md"
  - "kanda_reasoner_app/reasoner_tools_gui_help/tab1_architecture.json"
  - "kanda_reasoner_app/reasoner_tools_gui_shell/gui_support.py"
  - "kanda_reasoner_app/reasoner_tools_gui_shell/lazy_tabs.py"
  - "kanda_reasoner_app/reasoner_tools_gui_shell/help_docs"
  - "tests/test_architecture_review_rich_help_document.py"
  - "project_freeze_after_update/frozen_features_memory"
do_not_touch_summary:
  - "Architecture Review Help must prefer the rich local help document when a matching manifest entry exists."
  - "Legacy tab1_architecture.json must remain available as source data and plain-text fallback content."
  - "Architecture Review rich help must stay local-only: no http, https, CDN, remote font, tracker, or network dependency."
  - "The rich help document must preserve all 25 Architecture Review issue families from tab1_architecture.json."
  - "The renderer must use QWebEngineView only through lazy import and must keep QTextBrowser/plain local fallback behavior."
  - "Help document paths must stay under reasoner_tools_gui_shell/help_docs and reject traversal or absolute paths."
  - "The GUI help system must remain separate from routing, freeze memory, adviser, assistant, copilot, and runtime authority logic."
  - "No prompt auto-loading, router authority, freeze write, or routing-scorer behavior is authorized by help rendering."
  - "The canonical help layout paradigm remains Markdown source -> deterministic local HTML/CSS -> desktop Qt help window."
  - "Project-specific frozen memory must remain under project_freeze_after_update/frozen_features_memory."
superseded_by: null
---

# freeze-20260618-architecture-review-rich-desktop-help-layout-v1

## freeze identity

Freeze ID: `freeze-20260618-architecture-review-rich-desktop-help-layout-v1`

Feature title: `Architecture Review Rich Desktop Help Layout v1`

Date: `2026-06-18`

Primary box: `reasoner_tools_gui_shell/help_docs`

Box type: `desktop_gui_help_documentation/architecture_review_help_sub_box`

Status: `frozen after explicit human confirmation and validation evidence`

## summary

Implements the newly canonical desktop help-file creation paradigm for Architecture Review. The existing JSON help catalog remains source data and fallback. The Help button now prefers a manifest-backed rich local document and falls back to plain-text JSON formatting if no rich page is registered.

## validated files

- `.project_reference/CANNON/help_layout.md`
- `kanda_reasoner_app/reasoner_tools_gui_shell/gui_support.py`
- `kanda_reasoner_app/reasoner_tools_gui_shell/lazy_tabs.py`
- `kanda_reasoner_app/reasoner_tools_gui_shell/help_docs/__init__.py`
- `kanda_reasoner_app/reasoner_tools_gui_shell/help_docs/manifest.json`
- `kanda_reasoner_app/reasoner_tools_gui_shell/help_docs/path_resolver.py`
- `kanda_reasoner_app/reasoner_tools_gui_shell/help_docs/renderer.py`
- `kanda_reasoner_app/reasoner_tools_gui_shell/help_docs/css/book_help.css`
- `kanda_reasoner_app/reasoner_tools_gui_shell/help_docs/assets/architecture_review_pipeline.svg`
- `kanda_reasoner_app/reasoner_tools_gui_shell/help_docs/source/architecture_review.md`
- `kanda_reasoner_app/reasoner_tools_gui_shell/help_docs/rendered/architecture_review.html`
- `tests/test_architecture_review_rich_help_document.py`

## generated files

- `.project_reference/CANNON/help_layout.md`
- `kanda_reasoner_app/reasoner_tools_gui_shell/help_docs/__init__.py`
- `kanda_reasoner_app/reasoner_tools_gui_shell/help_docs/manifest.json`
- `kanda_reasoner_app/reasoner_tools_gui_shell/help_docs/path_resolver.py`
- `kanda_reasoner_app/reasoner_tools_gui_shell/help_docs/renderer.py`
- `kanda_reasoner_app/reasoner_tools_gui_shell/help_docs/css/book_help.css`
- `kanda_reasoner_app/reasoner_tools_gui_shell/help_docs/assets/architecture_review_pipeline.svg`
- `kanda_reasoner_app/reasoner_tools_gui_shell/help_docs/source/architecture_review.md`
- `kanda_reasoner_app/reasoner_tools_gui_shell/help_docs/rendered/architecture_review.html`
- `tests/test_architecture_review_rich_help_document.py`

## protected paths

- `.project_reference/CANNON/help_layout.md`
- `kanda_reasoner_app/reasoner_tools_gui_help/tab1_architecture.json`
- `kanda_reasoner_app/reasoner_tools_gui_shell/gui_support.py`
- `kanda_reasoner_app/reasoner_tools_gui_shell/lazy_tabs.py`
- `kanda_reasoner_app/reasoner_tools_gui_shell/help_docs`
- `tests/test_architecture_review_rich_help_document.py`
- `project_freeze_after_update/frozen_features_memory`

## do-not-regress rules

- `Architecture Review Help must prefer the rich local help document when a matching manifest entry exists.`
- `Legacy tab1_architecture.json must remain available as source data and plain-text fallback content.`
- `Architecture Review rich help must stay local-only: no http, https, CDN, remote font, tracker, or network dependency.`
- `The rich help document must preserve all 25 Architecture Review issue families from tab1_architecture.json.`
- `The renderer must use QWebEngineView only through lazy import and must keep QTextBrowser/plain local fallback behavior.`
- `Help document paths must stay under reasoner_tools_gui_shell/help_docs and reject traversal or absolute paths.`
- `The GUI help system must remain separate from routing, freeze memory, adviser, assistant, copilot, and runtime authority logic.`
- `No prompt auto-loading, router authority, freeze write, or routing-scorer behavior is authorized by help rendering.`
- `The canonical help layout paradigm remains Markdown source -> deterministic local HTML/CSS -> desktop Qt help window.`
- `Project-specific frozen memory must remain under project_freeze_after_update/frozen_features_memory.`

## validation evidence

```text
VALIDATION OK: architecture_review_rich_desktop_help_layout_v1
py_compile passed: gui_support.py, lazy_tabs.py, help_docs/path_resolver.py, help_docs/renderer.py, tests/test_architecture_review_rich_help_document.py
JSON OK: help_docs/manifest.json and reasoner_tools_gui_help/tab1_architecture.json parse successfully
unittest OK: python -m unittest tests.test_architecture_review_rich_help_document
CONTRACT_TEST_OK: Architecture Review rich desktop help maps legacy tab1_architecture.json to local HTML/CSS, preserves all 25 issue families, uses local original asset, rejects path traversal/absolute help paths, keeps canonical catalog fallback, avoids remote resources, and keeps QWebEngineView lazy with QTextBrowser fallback.
```

## known warnings

This patch updates only the Architecture Review help experience. It does not convert other tabs yet and does not alter architecture detectors or routing/adviser runtime logic.

## planned next step

Convert the next GUI help target, likely Workflow Review, using the same Markdown source -> local HTML/CSS -> desktop Qt help-window paradigm after separate validation.

## local freeze writer provenance

Generated by `local_freeze_writer_engine_v1` at `2026-06-18T20:30:07Z`.

This entry was created locally for the selected active project. The reusable `project_freeze_ledger` engine remains blueprint logic only and is not the owner of this project-specific memory.
