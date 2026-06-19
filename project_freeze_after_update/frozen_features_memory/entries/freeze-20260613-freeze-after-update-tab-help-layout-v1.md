---
freeze_id: "freeze-20260613-freeze-after-update-tab-help-layout-v1"
box: "freeze_after_update_gui"
status: "frozen"
date: "2026-06-13"
entry: "project_freeze_after_update/frozen_features_memory/entries/freeze-20260613-freeze-after-update-tab-help-layout-v1.md"
protected_paths:
  - "kanda_reasoner_app/freeze_after_update_gui/freeze_after_update_tab.py"
  - "project_freeze_after_update/frozen_features_memory/entries/freeze-20260613-freeze-after-update-tab-help-layout-v1.md"
do_not_touch_summary:
  - "Freeze Feature After Update tab keeps a two-column symmetrical layout: left for active project, status/actions, and generated output; right for the log window."
  - "The tab exposes the dynamic files_to_send_ai path for the active project and includes helpers to open/copy that path."
  - "The tab provides a read-only floating viewer for what_to_say_to_ai_freeze_feature.md with Copy Complete Text and Close actions."
  - "The tab includes a top-right Help button opening a practical, read-only help window."
  - "Generated what_to_say_to_ai_freeze_feature.md must not be edited manually; if the content needs change, update the blueprint generator instead."
---

# Freeze Feature After Update Tab Help/Layout v1

## Frozen scope

This freeze protects the validated GUI improvements added to the **Freeze Feature After Update** tab after the base feature was already frozen.

The frozen GUI behavior includes:

1. **Dynamic `files_to_send_ai` access**
   - The tab displays the active project's output folder:
     `<any_project>\project_freeze_after_update\files_to_send_ai`.
   - The tab lets the user copy that dynamic path.
   - The tab lets the user open that dynamic folder in Windows Explorer.

2. **Read-only `what_to_say_to_ai` viewer**
   - The tab opens a floating window for:
     `<any_project>\project_freeze_after_update\files_to_send_ai\what_to_say_to_ai_freeze_feature.md`.
   - The viewer is read-only.
   - The viewer has a **Copy Complete Text** button.
   - The viewer has a **Close** button.
   - The viewer warns that `what_to_say_to_ai_freeze_feature.md` must not be edited manually.

3. **Two-column layout**
   - The left column contains the active project, status/actions, and generated output controls.
   - The right column contains the log window.
   - The columns are symmetrical and preserve the existing feature logic.

4. **Top-right Help button**
   - The tab has a top-right **Help** button.
   - The help opens in a floating read-only window.
   - The help explains practical usage, project-local freeze memory, generated output, logs, and warnings.

## Validation evidence accepted

The following validation outputs were accepted in sequence:

```text
VALIDATION OK - Freeze Feature After Update tab has dynamic files_to_send_ai path access and read-only what_to_say viewer.
VALIDATION OK - Freeze Feature After Update tab uses symmetrical two-column layout with log window on the right.
VALIDATION OK - Freeze Feature After Update tab has top-right practical Help window.
```

## Box boundary

The protected GUI file is:

```text
kanda_reasoner_app/freeze_after_update_gui/freeze_after_update_tab.py
```

This freeze does not move generator logic. Generator logic remains in:

```text
project_freeze_ledger/freeze_tools/freeze_after_update_generator.py
```

Project-specific freeze memory and generated AI-send files remain in:

```text
<any_project>/project_freeze_after_update/
```

## Future modification rule

Future changes to the tab's layout/help/viewer behavior should be deliberate and validated. Do not remove the user-facing helper buttons, read-only warning, or two-column layout unless replacing them with an explicitly validated better UI.
