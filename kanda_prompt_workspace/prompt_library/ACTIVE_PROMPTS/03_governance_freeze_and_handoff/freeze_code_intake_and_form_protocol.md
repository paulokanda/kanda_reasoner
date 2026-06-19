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

