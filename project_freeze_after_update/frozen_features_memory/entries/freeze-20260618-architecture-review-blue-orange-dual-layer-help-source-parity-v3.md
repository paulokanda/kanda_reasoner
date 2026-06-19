---
freeze_id: "freeze-20260618-architecture-review-blue-orange-dual-layer-help-source-parity-v3"
feature_title: "Architecture Review Blue-Orange Dual-Layer Help Source Parity v3"
box: "reasoner_tools_gui_shell/help_docs"
status: "frozen"
date: "2026-06-18"
entry: "project_freeze_after_update/frozen_features_memory/entries/freeze-20260618-architecture-review-blue-orange-dual-layer-help-source-parity-v3.md"
protected_paths:
  - ".project_reference/CANNON/help_layout.md"
  - ".project_reference/CANNON/0022a updated how create adequate help_layout.md"
  - "kanda_reasoner_app/reasoner_tools_gui_help/tab1_architecture.json"
  - "kanda_reasoner_app/reasoner_tools_gui_shell/gui_support.py"
  - "kanda_reasoner_app/reasoner_tools_gui_shell/lazy_tabs.py"
  - "kanda_reasoner_app/reasoner_tools_gui_shell/help_docs"
  - "tests/test_architecture_review_rich_help_document.py"
  - "project_freeze_after_update/frozen_features_memory"
do_not_touch_summary:
  - "Architecture Review Help must follow the 0022a blue-orange help layout update."
  - "Architecture Review rich help must include an original characterful drawing in assets/drawings and a technical diagram in assets/diagrams."
  - "Architecture Review rich help must keep all 25 issue families from tab1_architecture.json visible."
  - "Both source Markdown and rendered HTML must preserve Technical, In plain English, and Further reading layers for Architecture Review issue families."
  - "Rendered help HTML and CSS must remain local-only: no http, https, CDN, remote font, tracker, or network dependency."
  - "The help manifest must list local source, rendered, CSS, drawing, and diagram dependencies."
  - "The renderer must keep QWebEngineView lazy import behavior and QTextBrowser fallback behavior."
  - "Help document paths must stay under reasoner_tools_gui_shell/help_docs and reject traversal or absolute paths."
  - "Help rendering must not imply prompt auto-loading, router authority, freeze write authority, adviser authority, assistant authority, copilot authority, or runtime authority."
  - "The canonical help paradigm is Markdown source -> dual-layer explanations -> characterful blue-orange drawings -> deterministic local HTML/CSS -> desktop Qt help window."
superseded_by: null
---

# freeze-20260618-architecture-review-blue-orange-dual-layer-help-source-parity-v3

## freeze identity

Freeze ID: `freeze-20260618-architecture-review-blue-orange-dual-layer-help-source-parity-v3`

Feature title: `Architecture Review Blue-Orange Dual-Layer Help Source Parity v3`

Date: `2026-06-18`

Primary box: `reasoner_tools_gui_shell/help_docs`

Box type: `desktop_gui_help_documentation/architecture_review_help_sub_box`

Status: `frozen after explicit human confirmation and validation evidence`

## summary

Finalizes the 0022a Architecture Review help update after source/rendered parity tightening. Supersedes the same-day v2 freeze by adding explicit source Markdown Technical, In plain English, and Further reading coverage for the issue family catalog.

## validated files

- `.project_reference/CANNON/help_layout.md`
- `kanda_reasoner_app/reasoner_tools_gui_shell/help_docs/manifest.json`
- `kanda_reasoner_app/reasoner_tools_gui_shell/help_docs/css/book_help.css`
- `kanda_reasoner_app/reasoner_tools_gui_shell/help_docs/assets/drawings/architecture_review_opener.svg`
- `kanda_reasoner_app/reasoner_tools_gui_shell/help_docs/assets/diagrams/architecture_review_pipeline.svg`
- `kanda_reasoner_app/reasoner_tools_gui_shell/help_docs/source/architecture_review.md`
- `kanda_reasoner_app/reasoner_tools_gui_shell/help_docs/rendered/architecture_review.html`
- `tests/test_architecture_review_rich_help_document.py`

## generated files

- `.project_reference/CANNON/help_layout.md`
- `kanda_reasoner_app/reasoner_tools_gui_shell/help_docs/assets/drawings/architecture_review_opener.svg`
- `kanda_reasoner_app/reasoner_tools_gui_shell/help_docs/assets/diagrams/architecture_review_pipeline.svg`

## protected paths

- `.project_reference/CANNON/help_layout.md`
- `.project_reference/CANNON/0022a updated how create adequate help_layout.md`
- `kanda_reasoner_app/reasoner_tools_gui_help/tab1_architecture.json`
- `kanda_reasoner_app/reasoner_tools_gui_shell/gui_support.py`
- `kanda_reasoner_app/reasoner_tools_gui_shell/lazy_tabs.py`
- `kanda_reasoner_app/reasoner_tools_gui_shell/help_docs`
- `tests/test_architecture_review_rich_help_document.py`
- `project_freeze_after_update/frozen_features_memory`

## do-not-regress rules

- `Architecture Review Help must follow the 0022a blue-orange help layout update.`
- `Architecture Review rich help must include an original characterful drawing in assets/drawings and a technical diagram in assets/diagrams.`
- `Architecture Review rich help must keep all 25 issue families from tab1_architecture.json visible.`
- `Both source Markdown and rendered HTML must preserve Technical, In plain English, and Further reading layers for Architecture Review issue families.`
- `Rendered help HTML and CSS must remain local-only: no http, https, CDN, remote font, tracker, or network dependency.`
- `The help manifest must list local source, rendered, CSS, drawing, and diagram dependencies.`
- `The renderer must keep QWebEngineView lazy import behavior and QTextBrowser fallback behavior.`
- `Help document paths must stay under reasoner_tools_gui_shell/help_docs and reject traversal or absolute paths.`
- `Help rendering must not imply prompt auto-loading, router authority, freeze write authority, adviser authority, assistant authority, copilot authority, or runtime authority.`
- `The canonical help paradigm is Markdown source -> dual-layer explanations -> characterful blue-orange drawings -> deterministic local HTML/CSS -> desktop Qt help window.`

## validation evidence

```text
VALIDATION OK: architecture_review_blue_orange_dual_layer_help_source_parity_v3
py_compile passed: gui_support.py, lazy_tabs.py, help_docs/path_resolver.py, help_docs/renderer.py, tests/test_architecture_review_rich_help_document.py
JSON OK: help_docs/manifest.json parses successfully
JSON OK: reasoner_tools_gui_help/tab1_architecture.json parses successfully
unittest OK: python -m unittest tests.test_architecture_review_rich_help_document -> Ran 6 tests, OK
LOCAL_ONLY_OK: rendered Architecture Review HTML/CSS contains no http://, https://, //cdn., fonts.googleapis, or tracker
CONTRACT_TEST_OK: manifest maps tab1_architecture.json to rich help, assets resolve under help_docs, all 25 issue families are present, blue-orange palette variables are present, drawing and diagram folders are used, every rendered issue card includes Technical, In plain English, and Further reading layers, and the source Markdown contains the same dual-layer/further-reading contract.
```

## known warnings

This freeze updates Architecture Review help only. Other GUI tabs have not yet been converted to the 0022a blue-orange dual-layer help layout.

## planned next step

Convert the next GUI help target using the same 0022a pattern after separate validation.

## local freeze writer provenance

Generated by `local_freeze_writer_engine_v1` at `2026-06-18T21:37:27Z`.

This entry was created locally for the selected active project. The reusable `project_freeze_ledger` engine remains blueprint logic only and is not the owner of this project-specific memory.
