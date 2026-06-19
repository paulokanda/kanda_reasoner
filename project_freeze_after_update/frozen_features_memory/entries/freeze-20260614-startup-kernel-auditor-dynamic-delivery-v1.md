---
freeze_id: "freeze-20260614-startup-kernel-auditor-dynamic-delivery-v1"
box: "kanda_prompt_workspace/startup_kernel_auditor_and_dynamic_delivery"
status: "frozen"
date: "2026-06-14"
entry: "project_freeze_after_update/frozen_features_memory/entries/freeze-20260614-startup-kernel-auditor-dynamic-delivery-v1.md"
protected_paths:
  - "kanda_prompt_workspace/prompt_tools/audit_startup_candidates.py"
  - "kanda_prompt_workspace/prompt_tools/sync_startup_routing_kernel_pack.py"
  - "kanda_prompt_workspace/prompt_tools/STARTUP_ROUTING_KERNEL_SOURCES.json"
  - "kanda_prompt_workspace/prompt_tools/STARTUP_ROUTING_KERNEL_SOURCES_UPDATE_CANDIDATE.md"
  - "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/01_session_start_and_navigation/daily_patch_delivery_guardrails.md"
  - "kanda_prompt_workspace/first_AI_deliver/first_prompts_to_ai.zip"
  - "kanda_prompt_workspace/first_AI_deliver/paste_after_first_prompts_to_ai.md"
  - "kanda_prompt_workspace/first_AI_deliver/paste_if_modify_startup_delivery.md"
do_not_touch_summary:
  - "Preserve audit_startup_candidates.py as the governed startup-candidate auditor that only acts on explicit .meta.json startup sidecars."
  - "When missing startup candidates are found, the auditor must explain each candidate, show the proposed source-map entry, and require the user to type YES before changing STARTUP_ROUTING_KERNEL_SOURCES.json."
  - "If the user answers NO or anything other than YES, the auditor must leave STARTUP_ROUTING_KERNEL_SOURCES.json and first_AI_deliver unchanged."
  - "If the user answers YES, the auditor may update STARTUP_ROUTING_KERNEL_SOURCES.json, validate it, and run sync_startup_routing_kernel_pack.py --ensure-sync --yes."
  - "Preserve sync_startup_routing_kernel_pack.py dynamic generation from STARTUP_ROUTING_KERNEL_SOURCES.json so newly approved files appear in first_prompts_to_ai.zip, 00_START_HERE_FOR_AI.md, paste_after_first_prompts_to_ai.md, README, and manifest."
  - "The human-facing startup paste file is paste_after_first_prompts_to_ai.md; do not reintroduce paste_after_uploading_startup_zip.md in active generated delivery or active generator references."
  - "Keep paste_if_modify_startup_delivery.md outside the normal startup ZIP."
  - "Do not store this freeze memory in project_freeze_ledger; use project_freeze_after_update/frozen_features_memory only."
superseded_by: null
---
# freeze-20260614-startup-kernel-auditor-dynamic-delivery-v1

## freeze identity

Freeze ID:

```text
freeze-20260614-startup-kernel-auditor-dynamic-delivery-v1
```

Date:

```text
2026-06-14
```

Project box:

```text
kanda_prompt_workspace/startup_kernel_auditor_and_dynamic_delivery
```

Freeze tier:

```text
tier 1: startup delivery / prompt-tool governance freeze
```

Status:

```text
frozen after install validation, live auditor fixture validation, dynamic startup delivery validation, and generated paste-file rename validation
```

Human approval:

```text
accepted by user after v4 auditor/dynamic-generator validation and v5 paste-file rename validation
```

## frozen version

```text
Startup kernel auditor, dynamic source-map delivery, and human-friendly paste file rename v1
```

## summary

This freeze locks the validated startup-kernel tooling update that added a governed auditor for always-startup candidates, repaired startup delivery generation so it is fully dynamic from `STARTUP_ROUTING_KERNEL_SOURCES.json`, and renamed the human-facing startup paste file to a clearer name.

The active human startup delivery is now:

```text
kanda_prompt_workspace/first_AI_deliver/first_prompts_to_ai.zip
kanda_prompt_workspace/first_AI_deliver/paste_after_first_prompts_to_ai.md
```

The old generated file name is retired:

```text
kanda_prompt_workspace/first_AI_deliver/paste_after_uploading_startup_zip.md
```

## frozen auditor behavior

The auditor is:

```text
kanda_prompt_workspace/prompt_tools/audit_startup_candidates.py
```

Frozen behavior:

```text
1. Scan approved prompt-library locations for explicit .meta.json startup sidecars.
2. Ignore random project files and prompts that do not explicitly opt into startup inclusion.
3. Generate STARTUP_ROUTING_KERNEL_SOURCES_UPDATE_CANDIDATE.md.
4. If no candidate is missing from STARTUP_ROUTING_KERNEL_SOURCES.json, return STATUS: NO_UPDATE_NEEDED.
5. If candidates are missing, explain each candidate to the human.
6. Show canonical_source, generated_filename, prompt_id, load_mode, role, sidecar, size, proposed load_order, and proposed source-map entry.
7. Ask the human to type YES before applying.
8. If the human answers NO or anything other than YES, change nothing.
9. If the human answers YES, update STARTUP_ROUTING_KERNEL_SOURCES.json and then run sync_startup_routing_kernel_pack.py --ensure-sync --yes.
10. Reject duplicate prompt_id and other audit errors.
```

## frozen dynamic generator behavior

The startup delivery generator is:

```text
kanda_prompt_workspace/prompt_tools/sync_startup_routing_kernel_pack.py
```

Frozen behavior:

```text
1. The generator reads STARTUP_ROUTING_KERNEL_SOURCES.json as the approved startup source map.
2. It creates first_prompts_to_ai.zip from the source map.
3. It creates paste_after_first_prompts_to_ai.md from the source map.
4. It creates paste_if_modify_startup_delivery.md as the maintenance-only startup delivery file.
5. It dynamically lists all approved startup files in 00_START_HERE_FOR_AI.md.
6. It dynamically lists all approved startup files in paste_after_first_prompts_to_ai.md.
7. It includes approved new files, such as 08_new_prompt.md, in the ZIP, boot file, paste file, README, and manifest during validation fixtures.
8. It keeps paste_if_modify_startup_delivery.md outside the normal startup ZIP.
```

## frozen rename behavior

The old generated paste file name:

```text
paste_after_uploading_startup_zip.md
```

is replaced by:

```text
paste_after_first_prompts_to_ai.md
```

The word `zip` at the end of the old filename was misleading because the file is a human paste instruction file, not a ZIP file.

Protected rename rules:

```text
1. first_AI_deliver must contain paste_after_first_prompts_to_ai.md.
2. first_AI_deliver must not contain paste_after_uploading_startup_zip.md after regeneration.
3. sync_startup_routing_kernel_pack.py must not contain the old literal filename in active logic.
4. paste_if_modify_startup_delivery.md must use the new paste filename.
5. STARTUP_PROMPT_REQUEST_KERNEL_MANIFEST.json must reference the new paste filename.
6. README_STARTUP_PROMPT_REQUEST_KERNEL.md inside the startup ZIP must reference the new paste filename.
```

## validation evidence

### v4 auditor and dynamic generator validation

The user pasted clean validation output showing:

```text
VALIDATION OK
Installed auditor compiles.
Installed sync generator compiles.
Real workspace report-only audit runs without fatal audit errors.
Real workspace startup delivery is in sync.
Answering NO changes nothing.
Answering YES updates STARTUP_ROUTING_KERNEL_SOURCES.json.
Answering YES regenerates first_AI_deliver.
Dynamic generator adds 08_new_prompt.md to ZIP.
Dynamic generator adds 08_new_prompt.md to boot file.
Dynamic generator adds 08_new_prompt.md to paste_after_uploading_startup_zip.md.
Dynamic generator adds 08_new_prompt.md to manifest.
No temporary files were placed in the project root.
```

The validation fixture also showed the user-facing candidate explanation and confirmation gate:

```text
STARTUP CANDIDATES FOUND
These prompts have explicit .meta.json startup sidecars but are not in STARTUP_ROUTING_KERNEL_SOURCES.json.
Only answer YES if they should be loaded in every future startup ZIP.

Update STARTUP_ROUTING_KERNEL_SOURCES.json with these candidates and regenerate startup delivery? Type YES to proceed:
```

When the test answered `NO`, validation confirmed:

```text
UPDATE CANCELLED BY HUMAN
No source-map or delivery files were changed.
EXIT_CODE: 1
```

When the test answered `YES`, validation confirmed:

```text
SOURCE MAP UPDATE OK
RUNNING STARTUP DELIVERY SYNC
ENSURE SYNC RESULT: IN_SYNC_AFTER_SYNC
SYNC OK
STARTUP ROUTING KERNEL SOURCE MAP UPDATE COMPLETE
EXIT_CODE: 0
```

### v5 human-friendly paste-file rename validation

The user pasted clean validation output showing:

```text
STATUS: IN_SYNC
Paste-after-uploading file: paste_after_first_prompts_to_ai.md
VALIDATION OK
sync_startup_routing_kernel_pack.py compiles.
Startup delivery is in sync.
New paste file exists: paste_after_first_prompts_to_ai.md.
Old paste file is removed: paste_after_uploading_startup_zip.md.
Generated paste file uses the new name.
Maintenance file uses the new name.
Generator source does not contain the old literal filename.
Manifest uses the new name.
README inside ZIP uses the new name.
```

## what is frozen

```text
- audit_startup_candidates.py interactive candidate explanation and YES-gated source-map update behavior
- sync_startup_routing_kernel_pack.py dynamic startup source-map generation for ZIP, boot, paste file, README, and manifest
- paste_after_first_prompts_to_ai.md as the active human startup paste filename
- retirement of paste_after_uploading_startup_zip.md from active generated delivery and active generator references
- first_AI_deliver regeneration after approved source-map updates
- PowerShell-compatible install/validation behavior that clears the terminal without closing it
```

## what is not frozen

```text
- Any particular future candidate prompt file
- Automatic inclusion of prompts without an explicit .meta.json sidecar
- Automatic source-map changes without human YES confirmation
- Any use of project_freeze_ledger as project-specific freeze memory
- The old paste_after_uploading_startup_zip.md filename
```

## future change rule

Future changes to these files are allowed only through governed startup-delivery maintenance, with validation evidence:

```text
kanda_prompt_workspace/prompt_tools/audit_startup_candidates.py
kanda_prompt_workspace/prompt_tools/sync_startup_routing_kernel_pack.py
kanda_prompt_workspace/prompt_tools/STARTUP_ROUTING_KERNEL_SOURCES.json
kanda_prompt_workspace/first_AI_deliver/
```

Any future change must validate at least:

```text
python -m py_compile kanda_prompt_workspace/prompt_tools/audit_startup_candidates.py
python -m py_compile kanda_prompt_workspace/prompt_tools/sync_startup_routing_kernel_pack.py
python kanda_prompt_workspace/prompt_tools/audit_startup_candidates.py --report
python kanda_prompt_workspace/prompt_tools/sync_startup_routing_kernel_pack.py --check
```

For rename-sensitive changes, validation must also prove that obsolete active references are absent.
