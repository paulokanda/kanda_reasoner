---
freeze_id: "freeze-20260613-freeze-after-update-generator-delivery-commands-v2"
box: "freeze_after_update"
status: "frozen"
date: "2026-06-13"
entry: "project_freeze_after_update/frozen_features_memory/entries/freeze-20260613-freeze-after-update-generator-delivery-commands-v2.md"
protected_paths:
  - "project_freeze_ledger/freeze_tools/freeze_after_update_generator.py"
  - "kanda_reasoner_app/freeze_after_update/blueprint_adapter.py"
  - "kanda_reasoner_app/freeze_after_update/send_pack_builder.py"
  - "kanda_reasoner_app/freeze_after_update/box_bootstrapper.py"
  - "project_freeze_after_update/frozen_features_memory/"
  - "project_freeze_after_update/files_to_send_ai/"
do_not_touch_summary:
  - "The Freeze Feature After Update instruction generator belongs in KANDA Reasoner's blueprint freeze box: project_freeze_ledger/freeze_tools/."
  - "The GUI/app box must remain a controller/adapter and must not own canonical instruction-template logic."
  - "Generated instructions must be recreated into each selected project's project_freeze_after_update/files_to_send_ai/ folder."
  - "The generated what_to_say_to_ai_freeze_feature.md must require ZIP delivery, install code, and validation code in one AI response."
  - "Delivery ZIP paths must be derived from PROJECT_ROOT drive root, not hardcoded to E: and not assumed to be inside the project root."
  - "PowerShell validation must set PYTHONPATH before project imports, must not use Bash heredoc syntax, and must not validate guessed/private result attributes."
superseded_by: null
---
# freeze-20260613-freeze-after-update-generator-delivery-commands-v2

## freeze identity

Freeze ID:

```text
freeze-20260613-freeze-after-update-generator-delivery-commands-v2
```

Date:

```text
2026-06-13
```

Project box:

```text
freeze_after_update
```

Freeze tier:

```text
tier 1: blueprint generator workflow freeze
```

Status:

```text
frozen operational baseline
```

Human approval:

```text
approved after local validation and after a GUI-tab regeneration test produced a what_to_say_to_ai_freeze_feature.md containing the corrected ZIP/install/validation delivery workflow
```

## frozen version

```text
Freeze After Update blueprint generator delivery commands v2
```

## summary

This freeze records the validated update that moved and hardened the instruction-generation responsibility for the **Freeze Feature After Update** workflow.

The canonical generator for the project-local AI-send instruction file is now owned by the KANDA blueprint freeze box:

```text
project_freeze_ledger/freeze_tools/freeze_after_update_generator.py
```

The generated project-specific instruction file remains in the selected project's local output box:

```text
<project_root>/project_freeze_after_update/files_to_send_ai/what_to_say_to_ai_freeze_feature.md
```

This preserves the architecture:

```text
kanda_reasoner_app/
  GUI/controller adapter only

project_freeze_ledger/freeze_tools/
  blueprint generator logic

<any_project>/project_freeze_after_update/
  project-specific freeze memory and generated AI-send output
```

## protected architectural decision

The following rule is frozen:

```text
Generated what_to_say_to_ai_freeze_feature.md files are output artifacts.
They are not the source of truth.
```

The source of truth for recreating that instruction file is:

```text
project_freeze_ledger/freeze_tools/freeze_after_update_generator.py
```

The generator writes fresh output into:

```text
<any_project>/project_freeze_after_update/files_to_send_ai/
```

The app-facing Freeze Feature After Update tab may call the generator through an adapter, but the app box must not own the canonical template logic.

## protected generated instruction behavior

Every generated:

```text
what_to_say_to_ai_freeze_feature.md
```

must explicitly tell AI that freeze-patch delivery requires three things in one response:

```text
1. a ZIP file to download
2. a complete install terminal block
3. a complete validation terminal block
```

It must also preserve these rules:

```text
1. The ZIP must be saved to the root of the drive where the target project lives.
2. The drive must be derived from <PROJECT_ROOT>, not hardcoded.
3. The ZIP is not assumed to be inside the project root.
4. The install block must check that the ZIP exists before extraction.
5. The install block must extract to a drive-root temporary patch folder.
6. The install script must show success, wait 5 seconds, and clear the terminal only on success.
7. The install script must leave the terminal visible on failure.
8. The validation block must be separate from the install block.
9. The validation block must set PYTHONPATH before project imports.
10. The validation script must not use Bash heredoc syntax such as python - <<'PY' in PowerShell.
11. If Python helper code is needed, the validation script must write a temporary .py file and run it.
12. Validation must check public files, public commands, and real generated output.
13. Validation must not depend on guessed/private result attributes.
14. Validation output must remain visible after validation.
15. Validation may clear only after the user presses Enter once after copying output and Enter a second time to confirm clearing.
16. The process is complete only after validation passes and the user pastes clean validation evidence.
17. The patch is freezeable only after clean validation evidence.
```

## validation evidence

The generator update was validated locally with this clean validation result:

```text
VALIDATION OK - generator now recreates what_to_say with correct ZIP, install, and validation commands.
```

Then the Freeze Feature After Update tab was used as a real smoke test for project:

```text
E:\kanda_reasoner
```

The tab regenerated:

```text
E:\kanda_reasoner\project_freeze_after_update\files_to_send_ai\freeze_feature_ai_send_pack_20260613_151908.zip
E:\kanda_reasoner\project_freeze_after_update\files_to_send_ai\what_to_say_to_ai_freeze_feature.md
```

The regenerated instruction file included the corrected section:

```text
Required AI delivery workflow for freeze patches
```

and included the corrected command workflow for:

```text
ZIP placement
install block
validation block
PowerShell compatibility
completion and freeze rule
```

## protected paths

The following paths are protected by this freeze:

```text
project_freeze_ledger/freeze_tools/freeze_after_update_generator.py
kanda_reasoner_app/freeze_after_update/blueprint_adapter.py
kanda_reasoner_app/freeze_after_update/send_pack_builder.py
kanda_reasoner_app/freeze_after_update/box_bootstrapper.py
project_freeze_after_update/frozen_features_memory/
project_freeze_after_update/files_to_send_ai/
```

## do not regress

Do not regress to any of the previous failed delivery patterns:

```text
Do not tell the user to run validation before the ZIP is extracted.
Do not assume the ZIP exists in the project root.
Do not hardcode E:\ for all projects.
Do not use python - <<'PY' inside PowerShell.
Do not forget PYTHONPATH before importing project modules.
Do not validate guessed attributes such as result.freeze_entry_count when the public result is a dict or generated file.
Do not consider a patch complete before validation.
Do not freeze without validation evidence.
```

## accepted result

After this freeze entry is installed, the project should have 8 frozen feature entry files, and the regenerated instruction file should report:

```text
This project currently has 8 frozen feature entry file(s).
```
