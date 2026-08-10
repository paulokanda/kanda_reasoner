---
prompt_id: patch_validate_freeze_error_memory_routine_blueprint
prompt_code: KPR-05-005
title: Answer Validate Freeze Memorize Error Routine Blueprint
version: 3.3
status: active
load_type: on_request
owner_box: 05_patch_delivery_and_validation
source_stage: separated-terminal-release-phases-v1
---
# Answer, Validate, Freeze, Memorize Error Routine Blueprint
## Purpose
This is the canonical continuation wrapper copied by the Show Project to AI
`Answer, Validate, Freeze, Memorize Error` button. It resumes the selected
Project release cycle after an answer, implementation, patch, install,
validation, Freeze, or Error Memory phase stops or fails.
Required user-facing delivery:
1. one self-contained feature or update ZIP;
2. one separate installation terminal block;
3. one separate validation terminal block;
4. one separate Freeze preparation terminal block after validation succeeds;
5. one separate Error Memory terminal block only when reusable lessons exist.
Never combine installation, validation, Freeze, and Error Memory in one command.
## Button context envelope
The button must place a `KANDA_ANSWER_VALIDATE_FREEZE_MEMORIZE_CONTEXT` envelope
before this prompt containing:
```text
Selected project slug
Selected project source root
KANDA Reasoner tool root
Same physical root: YES / NO
Selected Project Support root
Selected project-linked transient root
Canonical prompt source
```
If absent, resolve the same fields from the current `PROJECT READY CHECK`, exact
handoff, and `project_tool_boundary_canon` before mutation or artifact output.
## Compact current-work intake
Use current uploaded files, pasted compact updates, exact local output,
validation markers, Freeze snippets, Error Memory evidence, and current source
as one continuation context. Continue from the last reliable marker. Do not ask
the user to repeat evidence already supplied.
Generated archives remain evidence until current source and receiver ownership
are verified. Compact context cannot bypass source, Box, delivery, validation,
Freeze, or Error Memory gates.
## Hard Tool-versus-Project boundary
- The selected Project owns payload, install, live validation, Project Support,
  Freeze memory, and Error Memory.
- KANDA Reasoner owns this prompt and governance UI.
- Do not patch KANDA Reasoner for an external Project failure unless a separate
  Tool defect is proven and authorized.
- If Tool and Project share one physical root, keep logical roles separate.
- Generated handoffs are evidence, not editing authority.
- For a verified external Project, consequential mutation, extraction, package
  preflight, install, restore, move, rename, delete, and Project Python/import
  isolation must pass the Tool-owned public Fire Shield authority or an existing
  public workflow already integrated with it.
- Missing, stale, unavailable, ambiguous, or BLOCKED Fire Shield stops the
  consequential phase. Never substitute prompt approval, direct filesystem
  mutation, or private `_project_fire_shield_*` reach-in.
## Routine classification and identity
Select one class:
- `ROUTINE_POST_IMPLEMENTATION_COMPLETION`;
- `STARTUP_DELIVERY_FAILURE`;
- `PROJECT_HANDOFF_FAILURE`;
- `PATCH_BUILD_OR_DELIVERY_FAILURE`;
- `INSTALLATION_FAILURE`;
- `VALIDATION_FAILURE`;
- `FREEZE_INTAKE_FAILURE`;
- `ERROR_MEMORY_INTAKE_FAILURE`.
Do not combine unrelated defects.
```text
ANSWER VALIDATE FREEZE MEMORIZE ROUTINE IDENTITY
Project slug:
Selected project source root:
KANDA Reasoner tool root:
Same physical root: YES / NO
Project Support root:
Project-linked transient root:
Canonical prompt source:
Selected routine class:
Feature ID:
Patch ZIP identity:
Project interpreter or interpreter-resolution owner:
Current source fingerprint:
Last reliable marker:
Already completed phases:
Next required phase:
May modify selected Project source: YES / NO
May modify KANDA Reasoner Tool source: YES / NO
```
Blank, stale, ambiguous, or conflicting identity blocks output.
## Mandatory owner dispatch
Use only the smallest needed owner set:
- identity and Fire Shield policy: `project_tool_boundary_canon`;
- admission: Brick Wall and the exact Box owner;
- release: `bundle_gated_development_workflow`;
- payload/install/rollback: `implementation_and_delivery_protocol`;
- output gate: `pre_output_contract_gates`;
- regressions: `patch_install_delivery_error_register`;
- terminal blocks: `terminal_cleanup_contract`;
- retention: `durable_document_artifact_routing_canon`;
- Freeze: `freeze_code_intake_and_form_protocol` and, when needed,
  `self_contained_freeze_entry_intake_zip`;
- Error Memory: `error_memory_ai_formulary_startup_canon` and, when justified,
  `self_contained_error_memory_lesson_intake_zip` plus active-ready templates.
Never load deprecated `router_bridge_patch_delivery_contract`.
## Continuation contract
```text
ROUTINE CONTINUATION STATE
Feature ID:
Exact ZIP or artifact identity:
Completed phases:
Last reliable marker:
Current blocked or active phase:
Next exact action:
User execution required: YES / NO
Need new training prompt: NO
```
Invalidate only later phases affected by changed identity or evidence.
## Paste-safe PowerShell hard gate
Every user-facing PowerShell code fence is one independent paste unit. Prefer a
direct packaged `.ps1` invocation. Never emit `elseif`, `else`, `finally`, a
detached `catch`, split control flow, unsupported runtime APIs, stale paths, or
control characters. Use Windows PowerShell 5.1-compatible APIs unless newer is
verified. Resolve Python as an executable plus optional prefix arguments, never
as a single-item array whose index may collapse to one character.
Do not duplicate existing lessons
`lesson-powershell-detached-else-interactive-paste-footer-v1` or
`lesson-powershell-validation-wrapper-marker-and-finally-v1`.
## One self-contained feature ZIP
Create exactly one primary feature/update ZIP containing:
- exact source payload and manifest;
- packaged `INSTALL.ps1`, `VALIDATE.ps1`, `RUN_INSTALL.ps1`, and
  `RUN_VALIDATE.ps1` when used by the delivery contract;
- focused validators and required helpers;
- root-level `KANDA_FREEZE_HINT.json` when freezeable;
- required README and receipts.
Do not require a separate installer, validator, external runner, or standalone
validation-report download. Do not split one update across multiple feature
ZIPs.
A separate Freeze intake ZIP or Error Memory intake ZIP is allowed only for its
distinct schema and human approval gate. It must not contain or reinstall the
feature source.
## Required user-visible delivery shape
Use these phases in order. Each terminal phase gets its own heading and separate
PowerShell fence.
### Artifact - one update ZIP
Provide exactly one feature/update ZIP link and final SHA-256. It contains update
code plus packaged install and validation logic.
### Terminal 1 - INSTALL
Invoke only the packaged installer. It may stage, verify, extract, back up,
install, roll back, and verify installed hashes. It must not run live
validation, Freeze, or Error Memory.
```text
INSTALL PHASE COMPLETE: <feature_id>
```
### Terminal 2 - VALIDATE
Invoke only the packaged validator after installation. It may verify hashes,
run focused/regression validators, validate synchronization, and write durable
evidence through its canonical owner. It must not install, Freeze, or stage
Error Memory.
```text
VALIDATION OK: <feature_id>
STATUS: IN_SYNC
```
`INSTALL IS NOT VALIDATION`.
### Terminal 3 - FREEZE
After live validation and synchronization, provide a separate Freeze preparation
terminal block. Use the current Freeze owner and a separate self-contained
Freeze intake ZIP when required. It may load `New Local Freeze Entry`, but must
not run Preview or Confirm and Write.
```text
FREEZE DISPOSITION: PREPARED_FOR_HUMAN_CONFIRMATION
```
```text
Freeze Feature After Update
-> New Local Freeze Entry
-> Preview Freeze Entry
-> Confirm and Write
```
### Terminal 4 - ERROR MEMORY
Only after actual failures produce reusable evidence, check duplicates,
overlap, supersession, and schema status. When lessons are justified, provide one
separate Error Memory intake ZIP and a separate terminal block staging all
current lessons for human review.
Do not fabricate lessons to satisfy the phase list. If none is justified, state
`ERROR MEMORY DISPOSITION: NOT_REQUIRED` and create no no-op loader or report.
The terminal must never execute `Memorize Error`.
```text
KANDA Reasoner
-> select the correct Project
-> Error Memory
-> review each pending lesson
-> Memorize Error only after approval
```
## Strict phase isolation
- One terminal block never executes two lifecycle phases.
- Install cannot invoke validation, Freeze, or Error Memory.
- Validate cannot invoke install, Freeze, or Error Memory.
- Freeze cannot install source or stage lessons.
- Error Memory cannot install, validate, write Freeze memory, or memorize.
- Never present an all-in-one command.
- Continue from the last passed marker.
## No-orphan-report rule
Do not create or deliver `*_VALIDATION_REPORT.txt`, external runners, duplicate
manifests, or summary files without a named future consumer, owner, retention
path, and reuse purpose. Keep temporary logs and receipts under the Project
daily-work root. Keep durable validation evidence under Project Support through
its canonical owner. Do not expose disposable reports as downloads.
## Safe sequence
```text
answer from current source and compact update
-> resolve Tool/Project identity and Fire Shield applicability
-> authorize and repair the smallest owner
-> build and contract-validate one feature ZIP
-> deliver ZIP plus separate INSTALL command
-> install and verify hashes
-> deliver separate VALIDATE command
-> require VALIDATION OK and STATUS: IN_SYNC
-> deliver separate FREEZE command
-> human Preview and Confirm and Write
-> evaluate actual failures
-> when justified, deliver separate ERROR MEMORY command
-> human review and Memorize Error
```
## Release, Freeze, and Error Memory rules
No ZIP link may be emitted alone. Freezeable feature ZIPs require one root-level
`KANDA_FREEZE_HINT.json` that is not installed as source. Transient artifacts
belong under `<project_drive>/<project_name>_delete_after_daily_work`. Do not use
Downloads/Desktop fallback or generic Python when a governed interpreter exists.
Freeze is eligible only after local validation and synchronization. Preview is
read-only; Confirm and Write is human-only. Refresh startup Freeze context after
write.
Create Error Memory only for verified reusable failures after duplicate checks.
Stage active-ready lessons for review; do not write canonical lessons.
Memorize Error remains human-only.
## Fail-closed response
```text
ANSWER VALIDATE FREEZE MEMORIZE ROUTINE BLOCKED
Routine class:
Selected Project identity problem:
Missing exact source or artifact:
Missing owner or validator:
Unresolved fingerprint, interpreter, or ZIP identity:
Last reliable marker:
May build patch: NO
May show ZIP link: NO
May claim live validation: NO
May freeze: NO
May stage Error Memory: NO
Next safe action:
```
## Button integration
The GUI owns identity envelope, clipboard behavior, label, tooltip, and user
feedback. The canonical prompt is read from the KANDA Reasoner Tool root at the
existing path. Keep the button linked to that path; never copy prompt text into
GUI source or make an external Project prompt authority.
## Non-authorization statement
This wrapper does not itself authorize implementation, release, validation
claims, Freeze writes, or Error Memory persistence.
## Version history
- 3.3: required the frozen Fire Shield public authority for consequential external-Project phases and prohibited prompt-only, direct-filesystem, or private-reach-in fallback.
- 3.2: one primary update ZIP; separate install, validation, Freeze, and Error
  Memory terminal phases; compact intake; no orphan reports.
- 3.1: paste-safe PowerShell and Windows PowerShell 5.1 gates.
- 3.0: cross-project identity and no-retraining continuation.
- 2.0: owner-dispatch wrapper.
