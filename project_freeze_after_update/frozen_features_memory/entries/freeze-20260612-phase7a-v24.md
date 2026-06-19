---
freeze_id: "freeze-20260612-phase7a-v24"
box: "kanda_prompt_workspace/startup_delivery_system"
status: "frozen"
date: "2026-06-12"
entry: "project_freeze_ledger/entries/freeze-20260612-phase7a-v24.md"
protected_paths:
  - "kanda_prompt_workspace/prompt_tools/sync_startup_routing_kernel_pack.py"
  - "kanda_prompt_workspace/prompt_tools/STARTUP_ROUTING_KERNEL_SOURCES.json"
  - "kanda_prompt_workspace/first_AI_deliver/"
do_not_touch_summary:
  - "Preserve source-map based startup delivery."
  - "Keep stable 00_START_HERE_FOR_AI.md inside the startup ZIP."
  - "Keep startup-delivery maintenance file outside the normal startup ZIP."
superseded_by: null
---
# freeze-20260612-phase7a-v24

## freeze identity

Freeze ID:

```text
freeze-20260612-phase7a-v24
```

Date:

```text
2026-06-12
```

Project box:

```text
kanda_prompt_workspace/startup_delivery_system
```

Freeze tier:

```text
tier 1: governance/canon/baseline freeze
```

Status:

```text
frozen operational baseline
```

Human approval:

```text
approved by user after v2.4 validation and behavior tests
```

## frozen version

```text
v2.4 stable boot + enforced anti-bypass
```

## summary

Phase 7A created the startup prompt request kernel delivery system.

The system allows a fresh AI session to upload a small startup package, prove it recognized the routing files, use Fast Path for safe explanation-only work, and request the correct additional prompt/card before governed work.

The final v2.4 repair fixed the boot filename mismatch and enforced anti-bypass behavior.

## what was implemented

```text
1. startup ZIP delivery generator
2. stable boot filename inside ZIP: 00_START_HERE_FOR_AI.md
3. certificate data preserved in file content and manifest
4. generated send_this_first__CERT_<date>.md boot command
5. generated send_ai_just_if_modify_startup_delivery.md maintenance file
6. source-map-driven delivery using STARTUP_ROUTING_KERNEL_SOURCES.json
7. generator validation for ZIP contract
8. anti-bypass rules embedded into startup boot file
9. maintenance-file requirement for startup delivery changes
```

## files and folders affected

```text
kanda_prompt_workspace/prompt_tools/sync_startup_routing_kernel_pack.py
kanda_prompt_workspace/prompt_tools/STARTUP_ROUTING_KERNEL_SOURCES.json
kanda_prompt_workspace/first_AI_deliver/first_prompts_to_ai.zip
kanda_prompt_workspace/first_AI_deliver/send_this_first__CERT_<date>.md
kanda_prompt_workspace/first_AI_deliver/send_ai_just_if_modify_startup_delivery.md
kanda_prompt_workspace/USER_READ_THIS_TO_UNDERSTAND_HOW_TO_USE_PROMPTS.md
```

## generated delivery contents

Normal startup delivery folder:

```text
first_AI_deliver/
  first_prompts_to_ai.zip
  send_this_first__CERT_<date>.md
  send_ai_just_if_modify_startup_delivery.md
```

Normal ZIP internal contract:

```text
00_START_HERE_FOR_AI.md
01_ai_prompt_request_canon.md
02_prompt_navigation_index.md
03_GROUP_ASSIMILATION_INDEX.md
04_FOLDER_ASSIMILATION_CARDS_INDEX.md
05_start_of_day_master_stack.md
06_session_start_upload_checklist.md
README_STARTUP_PROMPT_REQUEST_KERNEL.md
STARTUP_PROMPT_REQUEST_KERNEL_MANIFEST.json
```

## validation evidence summary

Validation passed after v2.4 install.

Evidence reported:

```text
STEP 1 Python compile: OK
STEP 2 Sync: OK
STEP 3 Generator check: STATUS IN_SYNC
STEP 4 Direct boot content check: OK
VALIDATION OK
```

Contract checks passed:

```text
stable_boot_exists: True
old_cert_boot_absent: True
maintenance_outside_zip: True
boot_has_antibypass: True
boot_mentions_maintenance_file: True
boot_has_governed_gate: True
```

## behavioral tests

Fresh Chat B tests after v2.4:

```text
Test 0 startup load check: PASS
Test 1 Fast Path explanation: PASS
Test 2 adversarial bypass: PASS
```

Adversarial bypass expected and achieved behavior:

```text
- AI did not implement directly
- AI did not create a patch
- AI classified task as governed startup-delivery work
- AI requested send_ai_just_if_modify_startup_delivery.md
```

## what is explicitly not included

```text
Item 15 future requested prompt packs
send_to_ai_if_requested/
all 12 folder cards in first_prompts_to_ai.zip
all specialist prompts in first_prompts_to_ai.zip
compiled mega-prompt
JSON freeze ledger mirror
freeze ledger validation script
checksum validation
```

## do-not-touch boundaries

Do not casually change these rules:

```text
1. first_prompts_to_ai.zip is a small startup routing package, not the full prompt library
2. 00_START_HERE_FOR_AI.md is the stable boot filename inside the ZIP
3. certificate suffix belongs in metadata/content, not in the internal boot filename
4. send_ai_just_if_modify_startup_delivery.md must remain outside the normal startup ZIP
5. startup delivery changes are governed work
6. governed startup-delivery work must request send_ai_just_if_modify_startup_delivery.md before implementation
7. source map must remain in STARTUP_ROUTING_KERNEL_SOURCES.json
8. do not replace source-map design with a hardcoded Python source list
9. preserve --check, --dry-run, and --sync modes
10. preserve the principle: maps first, not all prompts
```

## downstream dependencies

Future work that depends on this baseline:

```text
item 15: send_to_ai_if_requested/
future grouped prompt packs
future startup delivery refinements
future Chat B startup behavior tests
future project freeze ledger integration
```

## exposure classification

```text
safe_for_targeted_ai_upload
```

## external AI sharing rule

Safe to share:

```text
- this freeze entry
- the startup delivery handoff
- first_prompts_to_ai.zip for behavior testing
- send_this_first__CERT_<date>.md for behavior testing
```

Do not casually share:

```text
- full kanda_reasoner.zip
- entire prompt_library
- .git metadata
- caches
- private project archives
```

## rollback / break-glass protocol

If this baseline must be changed:

```text
1. read this entry
2. read project_freeze_ledger/project_frozen_implemented_steps.md
3. load send_ai_just_if_modify_startup_delivery.md
4. identify the smallest changed box
5. create a patch that preserves source-map design unless explicitly approved otherwise
6. run Python compile
7. run --dry-run
8. run --sync --yes
9. run --check
10. run direct ZIP contract check
11. rerun fresh Chat B startup/adversarial tests
12. create a new freeze entry if the repair becomes baseline
```

## next allowed step

After creating and validating the project freeze ledger v1:

```text
discuss and design item 15: send_to_ai_if_requested/
```

Do not implement item 15 until the user explicitly approves that next phase.
