---
freeze_id: "freeze-20260618-help-layout-image-generation-style-rule-v4"
feature_title: "Help Layout Image Generation Style Rule v4"
box: "reasoner_tools_gui_shell/help_docs"
status: "frozen"
date: "2026-06-18"
entry: "project_freeze_after_update/frozen_features_memory/entries/freeze-20260618-help-layout-image-generation-style-rule-v4.md"
protected_paths:
  - ".project_reference/CANNON/0022a updated how create adequate help_layout.md"
  - ".project_reference/CANNON/help_layout.md"
  - "tests/test_architecture_review_rich_help_document.py"
  - "kanda_reasoner_app/reasoner_tools_gui_shell/help_docs"
  - "project_freeze_after_update/frozen_features_memory"
do_not_touch_summary:
  - "KANDA help-layout prompt must require real local image assets, not placeholders."
  - "Characterful help drawings must use black-and-white editorial cartoon line art as the primary style."
  - "Generated help drawings must use visible hatching, expressive human figures, simple props, and white paper background."
  - "KANDA blue/orange accents must be sparse teaching highlights, not full-color decorative rendering."
  - "Generated drawings must not copy any reference image, signature, character, logo, exact pose, exact label, or exact layout."
  - "Generated drawing assets must be local files, with local SVG preferred and manifest-listed dependencies."
  - "Each generated image asset must be documented with subject, asset path, alt text, caption, and prompt summary."
  - "Rendered help HTML and CSS must remain local-only: no http, https, CDN, remote font, tracker, or network dependency."
superseded_by: null
---

# freeze-20260618-help-layout-image-generation-style-rule-v4

## freeze identity

Freeze ID: `freeze-20260618-help-layout-image-generation-style-rule-v4`

Feature title: `Help Layout Image Generation Style Rule v4`

Date: `2026-06-18`

Primary box: `reasoner_tools_gui_shell/help_docs`

Box type: `desktop_gui_help_documentation/layout_prompt_canon`

Status: `frozen after explicit human confirmation and validation evidence`

## summary

Updates the 0022a help-layout prompt and compact canon so future created help files generate local images in the attached-reference style: black-and-white editorial cartoon line art with sparse KANDA blue/orange teaching accents and explicit no-copy provenance rules.

## validated files

- `.project_reference/CANNON/0022a updated how create adequate help_layout.md`
- `.project_reference/CANNON/help_layout.md`
- `tests/test_architecture_review_rich_help_document.py`
- `kanda_reasoner_app/reasoner_tools_gui_shell/help_docs/manifest.json`
- `kanda_reasoner_app/reasoner_tools_gui_shell/help_docs/rendered/architecture_review.html`
- `kanda_reasoner_app/reasoner_tools_gui_shell/help_docs/css/book_help.css`

## generated files

- None recorded.

## protected paths

- `.project_reference/CANNON/0022a updated how create adequate help_layout.md`
- `.project_reference/CANNON/help_layout.md`
- `tests/test_architecture_review_rich_help_document.py`
- `kanda_reasoner_app/reasoner_tools_gui_shell/help_docs`
- `project_freeze_after_update/frozen_features_memory`

## do-not-regress rules

- `KANDA help-layout prompt must require real local image assets, not placeholders.`
- `Characterful help drawings must use black-and-white editorial cartoon line art as the primary style.`
- `Generated help drawings must use visible hatching, expressive human figures, simple props, and white paper background.`
- `KANDA blue/orange accents must be sparse teaching highlights, not full-color decorative rendering.`
- `Generated drawings must not copy any reference image, signature, character, logo, exact pose, exact label, or exact layout.`
- `Generated drawing assets must be local files, with local SVG preferred and manifest-listed dependencies.`
- `Each generated image asset must be documented with subject, asset path, alt text, caption, and prompt summary.`
- `Rendered help HTML and CSS must remain local-only: no http, https, CDN, remote font, tracker, or network dependency.`

## validation evidence

```text
VALIDATION OK: help_layout_image_generation_style_rule_v4
py_compile passed: tests/test_architecture_review_rich_help_document.py
JSON OK: help_docs/manifest.json parses successfully
unittest OK: python -m unittest tests.test_architecture_review_rich_help_document -> Ran 6 tests, OK
HELP_IMAGE_STYLE_PROMPT_SCAN_OK: both 0022a and compact help_layout canon contain black-and-white editorial cartoon line art, visible hatching, do-not-copy-reference-image, local SVG preferred, and real local image asset rules.
LOCAL_ONLY_OK: rendered Architecture Review HTML/CSS still contains no http://, https://, //cdn., fonts.googleapis, or tracker.
```

## known warnings

This freeze updates the help-layout prompt and canon style rule only. It does not regenerate existing help images.

## planned next step

Use this image-generation style rule when converting the next help page or when refreshing existing help drawings.

## local freeze writer provenance

Generated by `local_freeze_writer_engine_v1` at `2026-06-18T22:00:55Z`.

This entry was created locally for the selected active project. The reusable `project_freeze_ledger` engine remains blueprint logic only and is not the owner of this project-specific memory.
