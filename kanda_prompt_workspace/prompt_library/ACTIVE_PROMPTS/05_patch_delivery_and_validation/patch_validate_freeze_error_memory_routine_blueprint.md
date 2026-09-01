---
prompt_id: patch_validate_freeze_error_memory_routine_blueprint
prompt_code: KPR-05-005
title: Answer Validate Freeze Memorize Error Routine Blueprint
version: 4.2
status: active
load_type: on_request
owner_box: 05_patch_delivery_and_validation
source_stage: error-memory-pre-output-prevention-hard-gate-v1
---
# Answer, Validate, Freeze, Memorize Error Routine Blueprint

## Purpose
This is the canonical continuation wrapper copied by the Show Project to AI `Answer, Validate, Freeze, Memorize Error` button.
It resumes the selected Project release cycle from the last reliable answer, patch, install, validation, Freeze, or Error Memory marker.

Required user-facing sequence:
1. one self-contained feature/update ZIP;
2. one paste-safe terminal block running packaged INSTALL then packaged VALIDATE;
3. successful INSTALL preserves output, waits Enter, Enter, clears once, returns, and the same pasted outer block starts VALIDATE;
4. any failed phase stops the chain and blocks every later phase;
5. `VALIDATION OK: <feature_id>` plus `STATUS: IN_SYNC` unlocks Freeze;
6. after the human confirms the Freeze is correct, evaluate verified reusable failures and emit Error Memory only when unique and justified.

INSTALL and VALIDATE remain separate script owners. One outer PowerShell paste unit may orchestrate them sequentially;
INSTALL never validates internally and VALIDATE never installs.

## Pre-response continuation hard gate
Before deciding what to answer, derive `CURRENT LIFECYCLE POINTER` for the exact
current release identity: Project, Feature ID, artifact/revision/fingerprint,
Last reliable marker, Completed phases, First incomplete phase, Blocked by, and Invalidated by.
- Same current release identity + completed phase = never repeat a completed phase unless newer explicit evidence invalidates it or an earlier dependency.
- Current `VALIDATION OK: <feature_id>` + `STATUS: IN_SYNC` = VALIDATE complete; First incomplete phase: Freeze; Do not request another validation command.
- Human-confirmed current validated Freeze = Freeze complete; next is Error Memory uniqueness/reuse review; Do not prepare a duplicate Freeze.
- New artifact/revision/fingerprint/correction invalidates only downstream evidence that depends on the superseded identity.
- Conflicting or ambiguous identity/evidence = fail closed at the first unresolved phase; request only what is missing there; Do not restart the full lifecycle.
This attention gate adds no state store, lifecycle owner, persistence layer, or workflow engine; existing KPR-05-005 transition rules remain canonical.

## Button context envelope
The button must place a `KANDA_ANSWER_VALIDATE_FREEZE_MEMORIZE_CONTEXT` envelope before this prompt containing:
```text
Selected project slug
Selected project source root
KANDA Reasoner tool root
Same physical root: YES / NO
Selected Project Support root
Selected project-linked transient root
Canonical prompt source
```
If absent, resolve the same fields from current Project/Tool identity evidence before mutation or artifact output.

## Compact current-work intake
Use current uploaded files, pasted compact updates, exact local output,
validation markers, Freeze snippets, Error Memory evidence, and current source
as one continuation context. Continue from the last reliable marker. Never ask
the user to repeat evidence already supplied. Generated archives remain evidence
until current source and receiver ownership are verified.

## Hard Tool-versus-Project boundary
- The selected Project owns payload, install, execution, live validation,
  release, rollback, Project Support, and Project Freeze memory.
- Reusable Error Memory remains Tool-owned prevention context.
- KANDA Reasoner owns this prompt and governance UI.
- Do not patch KANDA Reasoner for an external Project failure unless a separate
  Tool defect is proven and authorized.
- If Tool and Project share one physical root, keep logical roles separate.
- Generated handoffs are evidence, not editing authority.
- Independent Project-owned IDE, terminal, CI, install, test, validation,
  release, and rollback must not depend on KANDA observer availability.

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
Release owner classification: KANDA_TOOL_RELEASE / EXTERNAL_PROJECT_RELEASE
Release validator owner:
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
- identity/Fire Shield: `project_tool_boundary_canon`;
- admission: Brick Wall and exact Box owner;
- release: `bundle_gated_development_workflow`;
- payload/install/rollback: `implementation_and_delivery_protocol`;
- output gate: `pre_output_contract_gates`;
- regressions: `patch_install_delivery_error_register`;
- terminal orchestration/cleanup: `terminal_cleanup_contract`;
- retention: `durable_document_artifact_routing_canon`;
- Freeze: `freeze_code_intake_and_form_protocol`,
  `freeze_candidate_pre_output_audit`, and only when required
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

## Paste-safe PowerShell and Error Memory prevention hard gate
Before emitting operational output, apply `KPR-03-004 pre_output_contract_gates`
and derive its `ERROR MEMORY PREVENTION POINTER`. A relevant active lesson with
an objectively machine-detectable predicate is a hard obligation on the exact
final candidate, not advisory prose to remember later.
For interactive PowerShell, bind
`lesson-powershell-detached-else-interactive-paste-footer-v1` and
`lesson-powershell-validation-wrapper-marker-and-finally-v1` when their
prevention triggers match; the exact candidate must pass the current guard.
A guard failure blocks output; repair that candidate rather than duplicating the
known Error Memory lesson. Every user-facing PowerShell fence is one independent paste unit.
Prefer direct packaged `.ps1` invocation. Never emit `elseif`,
`else`, `finally`, a detached `catch`, split interactive control flow,
unsupported runtime APIs, stale paths, or control characters. Use Windows PowerShell 5.1-compatible APIs unless newer is verified.
```text
stage and verify exact ZIP
-> invoke INSTALL.ps1
-> preserve INSTALL success output
-> Enter
-> Enter
-> one final Clear-Host
-> INSTALL returns successfully
-> same pasted outer block invokes VALIDATE.ps1
-> VALIDATE prints current evidence
```
If INSTALL fails, stop before VALIDATE. If VALIDATE fails, stop before Freeze;
never catch a failed phase merely to continue.
## One self-contained feature ZIP
Create exactly one primary feature/update ZIP containing exact payload/manifest,
packaged `INSTALL.ps1`, packaged `VALIDATE.ps1`, focused validators/helpers,
root-level `KANDA_FREEZE_HINT.json` when freezeable, and required README/
receipts. Include `RUN_INSTALL.ps1` or `RUN_VALIDATE.ps1` only when genuinely
used by the delivery contract.

Do not require a separate installer, validator, external runner, or disposable
validation-report download. Do not split one update across multiple feature
ZIPs. A separate Freeze/Error Memory intake ZIP is allowed only when its distinct
receiver schema requires one and must not reinstall feature source.

## Required user-visible delivery shape
### Artifact - one update ZIP
Provide exactly one feature/update ZIP link and final SHA-256.

### Terminal - INSTALL then VALIDATE
Provide one PowerShell fence that stages/verifies the ZIP and sequentially
invokes packaged INSTALL and VALIDATE. The wrapper must not reproduce their
internal logic. INSTALL remains install-only. On success it preserves output,
asks Enter twice, clears once, and returns. The outer paste unit then invokes
VALIDATE.

Required live success evidence:
```text
VALIDATION OK: <feature_id>
STATUS: IN_SYNC
```
`INSTALL IS NOT VALIDATION`, even when both are orchestrated by one paste unit.

### After successful validation - FREEZE
When current `VALIDATION OK: <feature_id>` and `STATUS: IN_SYNC` are supplied,
do not ask for another validation command. Immediately run the KPR-03-008
pre-output audit, inspect the current Freeze store, and prepare the receive-ready
Freeze candidate or exact governed intake artifact required by the current
owner. Preview and Confirm and Write remain human-only.

```text
FREEZE DISPOSITION: PREPARED_FOR_HUMAN_CONFIRMATION
```
Freeze preparation failure stops the workflow.

### End of workflow - ERROR MEMORY
Only after the human confirms the validated Freeze candidate is correct, evaluate
actual failures observed during the workflow. Create Error Memory only for a
verified reusable failure after duplicate, overlap, and supersession checks.
When none is justified:
```text
ERROR MEMORY DISPOSITION: NOT_REQUIRED
```
Freeze and Error Memory use different strict receiver envelopes. Never concatenate
a receive-ready Freeze candidate and receive-ready Error Memory lesson in one
machine-transport response. Finish Freeze first; emit Error Memory separately
when required. `Memorize Error` remains human-only.

## Fail-stop lifecycle
```text
answer/implement
-> build exact ZIP
-> INSTALL
-> Enter
-> Enter
-> Clear-Host
-> VALIDATE
-> require VALIDATION OK and STATUS: IN_SYNC
-> prepare Freeze
-> human Preview and Confirm and Write
-> evaluate verified reusable errors
-> human Memorize Error only when justified
```
Failure policy:
- ZIP/staging failure: stop;
- INSTALL failure: stop before VALIDATE;
- VALIDATE failure: stop before Freeze;
- Freeze audit/intake failure: stop before Error Memory;
- Error Memory schema/duplicate/admission failure: stop without memorizing.

When a phase fails, diagnose/repair only that phase and invalidated later phases.
Never emit later-phase success markers or artifacts.

## No-orphan-report rule
Do not create/deliver `*_VALIDATION_REPORT.txt`, external runners, duplicate
manifests, or summary files without a named future consumer, owner, retention
path, and reuse purpose. Temporary logs/receipts belong under Project daily-work;
durable validation evidence belongs under Project Support through its owner.

## Release, Freeze, and Error Memory rules
For KANDA Tool releases, freezeable feature ZIPs require one root-level
`KANDA_FREEZE_HINT.json` not installed as source. Transient artifacts belong
under `<project_drive>/<project_name>_delete_after_daily_work`; never use
Downloads/Desktop fallback or generic Python when a governed interpreter exists.

Freeze is eligible only after live validation and synchronization. Preview is
read-only; Confirm and Write is human-only. The writer owns post-write startup
Freeze-context refresh. Error Memory requires verified reusable evidence and
duplicate checks; Memorize Error remains human-only.

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
The GUI owns identity envelope, clipboard behavior, label, tooltip, and feedback.
The canonical prompt is read from the KANDA Reasoner Tool root at the existing
path; never copy prompt text into GUI source. The adjacent terminal-flow helper
button must copy `terminal_cleanup_contract.md`, not embed terminal instructions.

## Non-authorization statement
This wrapper does not itself authorize implementation, release, validation
claims, Freeze writes, or Error Memory persistence.

## Version history
- 4.0: one fail-closed INSTALL -> Enter x2 -> Clear-Host -> VALIDATE paste unit;
  separate script ownership preserved; successful validation unlocks Freeze;
  Error Memory is evaluated last after human Freeze confirmation.
- 3.5: external Project implementation/release observer-independence.
- 3.4: actor-scoped Fire Shield for KANDA-managed external-Project phases.
- 3.3: frozen Fire Shield public authority for KANDA-managed consequential work.
- 3.2: one ZIP plus separate install/validate/Freeze/Error Memory terminal phases.
- 3.1: paste-safe PowerShell and Windows PowerShell 5.1 gates.
- 3.0: cross-project identity and no-retraining continuation.
- 2.0: owner-dispatch wrapper.
