---
prompt_id: freeze_code_intake_and_form_protocol
title: Freeze Code Intake and Form Protocol
version: 1.0
status: active_candidate
load_type: on_request
owner_group: 03_governance_freeze_and_handoff
created_by_patch: freeze_code_intake_prompt_routing_v1
---

# Freeze Code Intake and Form Protocol

## Purpose

Use this prompt whenever the work is about freezing code, freezing a validated feature, preparing a Freeze Feature After Update form, reviewing a freeze formulary, or delivering a patch that should later become a local freeze entry.

This prompt closes the chat-to-app gap. The AI chat knows the feature title, validation evidence, protected paths, and do-not-regress rules for the current implementation. The KANDA Reasoner app only knows local files and saved intake state. Therefore the AI must carry feature-specific freeze data into patch delivery and freeze review instead of relying on the app heuristic alone.

## Required triggers

Request or apply this prompt when the user says any of the following:

- freeze this code
- freeze this feature
- Freeze Feature After Update
- New Local Freeze Entry
- freeze form
- freeze formulary
- KANDA_FREEZE_HINT.json
- prepare freeze entry
- review freeze JSON
- after validation, freeze it
- patch ZIP should be freeze-ready

## Required behavior for patch ZIPs

When delivering a governed patch ZIP that may be frozen later, include a root-level sidecar named:

```text
KANDA_FREEZE_HINT.json
```

The sidecar must describe the feature implemented by the current patch, not an older local freeze workflow or a nearby heuristic guess.

The sidecar must include at least these fields:

```text
schema_version
kind
patch_name
feature_id
feature_title
primary_box
box_type
validated_files
generated_files
protected_paths
do_not_regress_rules
validation_evidence_summary
known_warnings
planned_next_step
notes
```

If local validation has not yet run, do not invent it. Include only sandbox validation and state what local validation remains missing. After the user provides local validation output, use that output to correct the freeze form.


## Pre-output contract gate requirement

Before returning freeze-form JSON, freeze-ready patch delivery instructions, `KANDA_FREEZE_HINT.json`, or validation evidence intended for a local freeze entry, request or apply `pre_output_contract_gates` from this folder.

Required exact validation marker after local validation passes:

```text
VALIDATION OK: <feature_id>
```

Required startup sync marker when startup delivery was validated:

```text
STATUS: IN_SYNC
```

If the exact validation marker is missing, do not produce freeze-ready JSON. Return:

```text
FREEZE BLOCKED - validation evidence marker missing.
```

Freeze-form JSON must be strict parser-ready output between the exact KANDA markers, without markdown fences, comments, trailing commas, or explanatory text inside the markers.

<!-- PATCH_FREEZE_DELIVERY_SEQUENCE_CANON_V1_START -->
## Canonical freeze-ready patch delivery sequence

For every freezeable KANDA/PyArchitect patch, the delivery order is mandatory and must not be inverted, skipped, or diluted:

1. **Send the patch ZIP only after contract validation.** The ZIP must contain only the changed project files plus a root-level `KANDA_FREEZE_HINT.json` sidecar. If the ZIP contract cannot be verified, block delivery with `CONTRACT NOT MET - PATCH DELIVERY BLOCKED`.
2. **Send the install PowerShell after the ZIP.** The install block must stage the ZIP from `<drive>:\PATCH_NAME.zip` into `<drive>:\<project_name>_delete_after_daily_work\`, delete the root-drive ZIP copy after successful staging, extract only from the staged ZIP, and install only changed project files.
3. **Do not install the freeze sidecar into the project root.** `KANDA_FREEZE_HINT.json` is freeze-intake delivery metadata. It may be scanned or consumed from the staged ZIP / daily-work intake location, but it must not be copied as a normal project source file.
4. **Send the validation PowerShell after the install block.** Validation must be a separate local action after install and must emit recognizable evidence, including `VALIDATION OK: <feature_id>`. When startup delivery, generated evidence, or sync state is validated, it must also emit `STATUS: IN_SYNC`.
5. **Freeze only after local validation passes.** The Freeze Feature After Update flow must use the feature-specific `KANDA_FREEZE_HINT.json` / freeze-intake data plus current validation evidence, then require Preview and explicit human Confirm and Write.
6. **Refresh AI exposure after freeze.** A successful local freeze write must refresh AI-send exposure and startup freeze context so the next startup pack knows the frozen behavior.

Short form:

```text
patch ZIP with root KANDA_FREEZE_HINT.json
-> install changed files only, keeping KANDA_FREEZE_HINT.json out of project root
-> run local validation with VALIDATION OK and STATUS: IN_SYNC when applicable
-> freeze through Preview + Confirm and Write
-> refresh AI-send and startup freeze context
```

Install success is not validation. A freeze hint is not validation evidence. Old feature validation must not be reused for the current feature.
<!-- PATCH_FREEZE_DELIVERY_SEQUENCE_CANON_V1_END -->

## Required behavior for freeze form review

When reviewing a freeze formulary, verify that:

1. feature_title matches the feature that was actually implemented and validated.
2. validation_evidence_summary uses only validation that is actually present in the chat or user output.
3. protected_paths match the feature's actual source, prompt, generated, or state paths.
4. generated_files are not mislabeled as canonical source of truth.
5. project-specific frozen memory remains under project_freeze_after_update/frozen_features_memory.
6. project-specific freeze-intake state remains under project_freeze_after_update/freeze_hint_intake.
7. project-specific memory is never stored inside project_freeze_ledger.
8. Preview Freeze Entry remains read-only.
9. Confirm and Write remains explicitly human-confirmed.
10. After a local freeze write, startup freeze context must be refreshed.

If the app auto-filled an older feature title or old validation list, correct it. Do not approve stale heuristic freeze data.

## Multi-project rule

KANDA Reasoner can operate on multiple active projects.

For the active project root:

```text
<active_project_root>/project_freeze_after_update/freeze_hint_intake
<active_project_root>/project_freeze_after_update/frozen_features_memory
```

are the correct project-local locations.

When KANDA Reasoner itself is the active project, those folders are under the KANDA Reasoner project root. When another project is active, those folders are under that other project's root.

Do not hardcode KANDA Reasoner as the only active project. Do not store another project's freeze intake or frozen memory inside the KANDA Reasoner root.

## App-side intake expectation

If the app supports the Freeze Hint Intake box, New Local Freeze Entry should prefer the latest unused saved freeze hint before falling back to heuristic local freeze inputs. After Confirm and Write succeeds, the used freeze hint should be marked consumed so it is not reused for another unrelated freeze.

## Strict boundaries

Do not bypass Preview Freeze Entry.
Do not bypass Confirm and Write.
Do not write frozen memory silently.
Do not install KANDA_FREEZE_HINT.json into the project root as a source file.
Do not treat generated startup artifacts as canonical source.
Do not store project-specific frozen memory or freeze-intake state inside project_freeze_ledger.
Do not reuse validation evidence from an older feature.

## Output expectations

For a freeze form correction request, return only the requested receive-ready JSON block if the user gave a strict return contract.

For a patch delivery response, explicitly state whether the ZIP contains KANDA_FREEZE_HINT.json and that it is delivery metadata, not an installed source file.

For a handoff, include the current feature title, feature ID or patch name, validated files, generated files, protected paths, validation evidence status, freeze status, and next freeze action.

## Validation evidence marker and post-validation merge rule

When a freeze-ready patch ZIP is delivered before user-local validation runs, `KANDA_FREEZE_HINT.json` may include sandbox evidence and a pending-local-validation note only. Do not invent user-local validation.

After the user runs the validation block and validation passes, the AI must ensure the freeze form receives recognizer-friendly validation evidence. The evidence must include at least one literal marker accepted by the local freeze writer, preferably:

```text
VALIDATION OK: <feature_id>
```

If startup synchronization is part of validation, preserve it as a separate exact line:

```text
STATUS: IN_SYNC
```

Do not write `STATUS IN_SYNC` without the colon.

For future validation blocks, after successful validation the AI should update the saved freeze hint intake record when the `freeze_hint_intake` contract is available by calling `merge_validation_evidence_into_latest_hint(project_root, validation_evidence_summary, feature_id=...)`. This updates `<active_project_root>/project_freeze_after_update/freeze_hint_intake/latest_freeze_hint.json` so `New Local Freeze Entry` can fill `validation_evidence_summary` with the actual validation output rather than the pre-validation sidecar placeholder.

A freeze form must not be approved when `validation_evidence_summary` contains only sandbox evidence, a malformed startup status line, or a pending-validation note. If the form lacks `VALIDATION OK: <feature_id>` after validation has passed, correct the form before Confirm and Write.

## Freeze hint rescan preservation rule

After validation evidence has been merged into `<active_project_root>/project_freeze_after_update/freeze_hint_intake/latest_freeze_hint.json`, the app must not downgrade that saved record by rescanning the same staged patch ZIP and reloading the pre-validation `KANDA_FREEZE_HINT.json` placeholder.

When a staged ZIP sidecar and the latest saved freeze hint describe the same feature or source ZIP, and the saved record already contains recognizer-friendly local validation evidence such as `VALIDATION OK: <feature_id>` or `STATUS: IN_SYNC`, keep the saved record.

This preserves the local validation evidence needed by Confirm and Write while keeping `KANDA_FREEZE_HINT.json` as pre-validation delivery metadata.


<!-- PATCH_VALIDATION_EVIDENCE_MERGE_PARADIGM_V1_BEGIN -->

## Validate-code paradigm for freeze evidence

Local validation evidence is a state transition, not just terminal text. When a
patch has a root-level `KANDA_FREEZE_HINT.json`, passed validation must be merged
into the saved freeze hint intake record before the freeze form is considered
ready.

Required invariant:

```text
local validation passed
-> validation output contains VALIDATION OK: <feature_id>
-> merge_validation_evidence_into_latest_hint updates latest_freeze_hint.json
-> New Local Freeze Entry loads the current validation_evidence_summary
-> Preview remains read-only
-> Confirm and Write remains human-confirmed
```

The current patch's validation evidence must not remain only in chat or terminal
output while the freeze form still contains a pre-validation sidecar note. If the
form says local validation must still confirm the feature after validation has
already passed, the form is stale and must be corrected before freezing.

The Error Memory pending-intake state is independent from this. An Error Memory
lesson package may be frozen as a pending-intake package after staging and local
validation. The lesson does not need to be saved into active Lessons unless the
intended frozen feature is the saved Lesson itself.

<!-- PATCH_VALIDATION_EVIDENCE_MERGE_PARADIGM_V1_END -->

For command-line validation flows, the preferred implementation path is:

```text
python scripts\merge_freeze_validation_evidence.py --project-root <PROJECT_ROOT> --feature-id <feature_id> --feature-title <feature_title> --evidence-file <evidence_file>
```

Require the output marker:

```text
FREEZE_HINT_EVIDENCE_MERGE_OK: <feature_id>
```

<!-- PATCH_VALIDATION_EVIDENCE_MERGE_BY_PATCH_ZIP_V2_BEGIN -->

## Patch ZIP keyed validation evidence merge - v2

When a validation block merges local validation evidence into freeze hint intake,
it must not assume `latest_freeze_hint.json` already belongs to the feature that
was just validated. A previous patch can leave a stale latest hint for another
feature.

For every freeze-capable patch validation block:

1. Capture local validation markers after the validator passes.
2. Call `scripts/merge_freeze_validation_evidence.py` with `--patch-zip` pointing
   to the staged patch ZIP and with the current `--feature-id`.
3. Require the merge helper to load the matching root-level `KANDA_FREEZE_HINT.json`
   from that patch ZIP before merging evidence if the current latest hint is for
   another feature.
4. Treat a feature-id mismatch without a matching `--patch-zip` as a validation
   failure, not as a reason to merge evidence into the wrong freeze form.
5. Freeze-ready evidence must include `VALIDATION OK: <feature_id>` and
   `FREEZE_HINT_EVIDENCE_MERGE_OK: <feature_id>`.

This prevents stale freeze-intake data from causing `FREEZE BLOCKED - no
recognizable validation evidence found` after local validation already passed.

<!-- PATCH_VALIDATION_EVIDENCE_MERGE_BY_PATCH_ZIP_V2_END -->

<!-- ERROR_MEMORY_LESSON_BLOCK_SCHEMA_GATE_V1_BEGIN -->

## Error Memory lesson block schema gate - v1

Any ZIP, patch, direct Error Lesson ZIP, or clipboard receive block that carries
`KANDA_ERROR_LESSON_JSON` must be schema-valid before delivery.

Machine gate:

```text
python scripts\validate_patch_zip.py <staged_patch_zip>
```

must inspect every packaged `KANDA_ERROR_LESSON_JSON_*.txt` file and block the
ZIP if the lesson JSON lacks `schema_version`, `project_slug`, required active
lesson fields, `redaction`, `exception`, `fingerprint`, `prevention_triggers`,
or `validation_evidence` when `status` is `active`.

Required minimum for every packaged lesson block:

```text
schema_version: "1.0"
project_slug: non-empty selected project slug
lesson_id: present
status: draft, active, deprecated, or superseded
redaction.applied: true
redaction.export_safe: true
```

Do not answer with only a corrected manual JSON block when an Error Memory
lesson was generated with missing schema fields. Correct the creation/validation
path so the next generated package is blocked before release.

<!-- ERROR_MEMORY_LESSON_BLOCK_SCHEMA_GATE_V1_END -->

