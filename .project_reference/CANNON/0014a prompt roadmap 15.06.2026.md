# Updated KANDA Prompt Roadmap — Prompt-Call Accuracy, Freeze-Aware Routing, and Local Governance

Date updated: 2026-06-15
Replaces / evolves: `0014 prompt roadmap 13.06.2026.md`

## 0. Why this roadmap changed

The older roadmap was correct for the earlier stage of the project. It focused on building a staged prompt workspace, prompt schema authority, prompt audit canon, routing indexes, named prompt stacks, validators, dispatcher logic, and later GUI orchestration.

The project has now evolved.

The central goal is no longer only:

"Can the AI classify the task correctly?"

The central goal is now:

"Can the AI request the smallest complete, current, non-stale, box-safe context package before acting?"

This is the core of Phase 2 Prompt-Call Accuracy Testing.

The roadmap must therefore be updated to prioritize:

1. Prompt-call accuracy before dispatcher automation.
2. Exact required prompt/context requests before implementation.
3. Freeze-memory awareness before modifying protected behavior.
4. Local-first freeze workflow before AI-send freeze workflow.
5. Manual pilots before JSON schemas and validators.
6. Dynamic project-specific memory exposure without cross-project contamination.
7. Root-to-staging patch delivery discipline.
8. Sandbox pre-delivery validation before any patch is sent to the user.

## 1. Current confirmed state

### 1.1 Startup prompt kernel

Status: active and loaded.

The startup prompt kernel contains:

* `00_START_HERE_FOR_AI.md`
* `01_ai_prompt_request_canon.md`
* `02_prompt_navigation_index.md`
* `03_GROUP_ASSIMILATION_INDEX.md`
* `04_FOLDER_ASSIMILATION_CARDS_INDEX.md`
* `05_start_of_day_master_stack.md`
* `06_session_start_upload_checklist.md`
* `07_daily_patch_delivery_guardrails.md`
* `08_handoff_at_end_of_work.md`
* `09_active_project_freeze_context.md`
* startup README and manifest

Important update:

`09_active_project_freeze_context.md` now belongs in the startup pack so future AI sessions can see compact active project freeze context when needed.

### 1.2 Phase 1 routing tests

Status: complete for the current sequence.

Phase 1 tested whether AI can classify tasks correctly:

* Fast Path vs Routed Work Path
* May proceed now: YES / NO / PARTIAL
* bypass refusal
* project-specific freeze-memory box selection
* validation evidence handling
* prompt-authoring routing behavior
* startup delivery routing behavior

Important repaired behavior:

When a scenario explicitly states that the patch is installed and validation passed, and lists validation evidence, the AI must treat that validation evidence as already provided for routing-test purposes.

The AI must not ask again for validation evidence that is already present in the scenario.

### 1.3 Pre-Phase 2 Prompt-Call Accuracy scaffold

Status: installed / validated / closed.

Permanent files:

```text
kanda_prompt_workspace/prompt_library/ROUTING_TESTS/PHASE_2_PROMPT_CALL_ACCURACY/README.md
kanda_prompt_workspace/prompt_library/ROUTING_TESTS/PHASE_2_PROMPT_CALL_ACCURACY/phase2_prompt_call_rubric.md
```

Correct non-installed status:

```text
RG-025: not installed as project file
RG-026: not installed as project file
RG-027: not installed as project file
Phase 2 validator: not created
Phase 2 JSON schema: not created
```

Manual pilot status:

```text
RG-025: run in chat / passed
RG-026: run in chat / passed
RG-027: run in chat / passed
```

Manual pilot files must not be installed as permanent project files unless a later explicit roadmap step creates a controlled manual-pilot registry.

### 1.4 Patch delivery prompt discipline

Status: installed / validated.

Current mandatory delivery rule:

1. User downloads patch ZIP to drive root.

Example:

```text
E:\PATCH_NAME.zip
```

2. Installer moves ZIP to:

```text
E:\kanda_reasoner_delete_after_daily_work\PATCH_NAME.zip
```

3. Installer installs only from the delete-after-daily-work folder.

4. Validation helper files must be created under delete-after-daily-work, not in the project root.

5. Before any ZIP/install/validation code is delivered to the user, the AI must test the deliverable in its internal sandbox and report sandbox validation honestly.

### 1.5 Freeze-memory exposure CLI v1

Status: installed / validated / frozen.

Frozen feature:

```text
freeze-20260614-freeze-memory-exposure-cli-v1
```

Protected file:

```text
project_freeze_ledger/freeze_tools/expose_freeze_memory.py
```

Purpose:

Read the selected active project's frozen memory and expose a compact freeze summary without writing, repairing, regenerating, or mutating freeze memory.

Important v1 restrictions:

* CLI only.
* Read-only.
* Explicit `--project-root` required.
* No GUI.
* No startup integration beyond context awareness.
* No app contract integration.
* No ZIP/context publishing.
* No automatic index repair.
* No writing to `frozen_features_memory`.
* No active project memory stored in `project_freeze_ledger`.

### 1.6 Local Freeze Feature After Update workflow

Status: already frozen.

Frozen feature:

```text
freeze-20260615-freeze-feature-after-update-local-freeze-workflow-v1
```

Core behavior:

The Freeze Feature After Update tab is now intended to become the human control center for local freeze workflow.

Normal path:

1. New Local Freeze Entry.
2. Preview Freeze Entry.
3. Confirm and Write.
4. Refresh AI startup freeze context.
5. Optional external AI review/export as fallback.

Important permanent rules:

* Preview must remain read-only.
* Confirm and Write must require valid preview and explicit human confirmation.
* GUI must call the public freeze_after_update contract.
* Local freeze write must refresh AI startup freeze context.
* AI review/export remains fallback, not the normal freeze path.
* Project-specific frozen memory stays under:

```text
project_freeze_after_update/frozen_features_memory
```

* Project-specific frozen memory must not be stored inside:

```text
project_freeze_ledger
```

## 2. Updated master sequence

The old roadmap had this broad order:

```text
re-anchor
schema authority
audit canon
AI NEED vocabulary
machine-readable index
ledgers
prompt stacks
stack tests
validator
dispatcher
receipt protocol
audit workflow
desktop app
meta-AI
handoff discipline
```

The updated order is now:

```text
0. Re-anchor current frozen prompt state
1. Freeze-aware startup and prompt-call contract review
2. Phase 2 Prompt-Call Accuracy manual expansion
3. Context Package Manifest standard
4. Prompt-request canon hardening
5. Prompt authoring / audit canon hardening
6. Prompt schema and machine-readable index normalization
7. Conflict, substitution, and integration ledgers
8. Prompt-call validator design, but not implementation yet
9. First named stacks, after prompt-call accuracy stabilizes
10. Stack-level two-chat testing
11. Validator upgrade
12. CLI dispatcher v0 dry-run
13. CLI dispatcher v1 compose bundle
14. Prompt receipt/load-check protocol
15. Local freeze workflow integration hardening
16. Dynamic freeze context publish mode
17. Desktop orchestration view
18. Meta-AI orchestrator
19. Session handoff and restart discipline
```

Important change:

Dispatcher automation moves later.

The system must first prove that the AI can ask for the correct context package before acting.

## 3. Implementation 0 — Re-anchor current frozen prompt state

### Purpose

Confirm the project’s current state before creating more prompt infrastructure.

This replaces the older generic “re-anchor workspace” step with a freeze-aware re-anchor.

### Primary box

```text
kanda_prompt_workspace/startup_routing_kernel
project_freeze_after_update/frozen_features_memory
```

### Inputs

```text
first_prompts_to_ai.zip
freeze_index.json
project_frozen_implemented_steps.md
09_active_project_freeze_context.md
PHASE_2_PROMPT_CALL_ACCURACY folder
```

### Output

```text
PROMPT_SYSTEM_REANCHOR_REPORT.md
```

### Report must confirm

1. Startup ZIP includes the expected numbered files.
2. Startup ZIP includes active freeze context.
3. Phase 1 routing tests are closed.
4. Pre-Phase 2 rubric exists and is closed.
5. RG-025/RG-026/RG-027 are not installed as project files.
6. Manual pilots passed in chat.
7. Freeze-memory exposure CLI v1 is frozen.
8. Local Freeze Feature workflow v1 is frozen.
9. Patch delivery root-to-staging rule is active.
10. Sandbox pre-delivery gate is active.
11. No stale `paste_after_uploading_startup_zip.md` active reference is reintroduced.
12. No active memory is stored in `project_freeze_ledger`.

### Freeze condition

This step is freezeable only after the re-anchor report is generated, reviewed, and validated.

## 4. Implementation 1 — Freeze-aware startup and prompt-call contract review

### Purpose

Ensure startup prompts teach the AI the correct current behavior:

* load startup kernel first;
* classify Fast Path vs Routed Work Path;
* request exact prompt/context package;
* respect frozen memory;
* use active freeze context when relevant;
* refuse bypass attempts;
* avoid stale files.

### Primary box

```text
kanda_prompt_workspace/startup_routing_kernel
```

### Files likely reviewed

```text
00_START_HERE_FOR_AI.md
01_ai_prompt_request_canon.md
02_prompt_navigation_index.md
03_GROUP_ASSIMILATION_INDEX.md
04_FOLDER_ASSIMILATION_CARDS_INDEX.md
05_start_of_day_master_stack.md
06_session_start_upload_checklist.md
07_daily_patch_delivery_guardrails.md
08_handoff_at_end_of_work.md
09_active_project_freeze_context.md
```

### Required behavior

For governed work, AI must request exact context, not generic labels.

For freeze-sensitive work, AI must request or use current active project freeze context.

For startup delivery changes, AI must request:

```text
paste_if_modify_startup_delivery.md
sync_startup_routing_kernel_pack.py
STARTUP_ROUTING_KERNEL_SOURCES.json
current first_AI_deliver artifacts
startup delivery validation steps
```

For prompt-authoring anti-bypass requests, AI must explicitly request:

```text
07_prompt_authoring_and_audit
prompt_canon_reconciliation_protocol
prompt_audit_canon
project_specific_prompt_generalization
relevant ACTIVE_PROMPTS folder card or _FOLDER_ASSIMILATION
existing prompt-library assets/indexes
bundle_gated_development_workflow, if creating a bundle
validation command or manual validation steps
```

### Validation

Manual routing tests plus startup sync check.

### Freeze condition

Freeze only if startup behavior remains coherent and no stale routing instructions return.

## 5. Implementation 2 — Phase 2 Prompt-Call Accuracy manual expansion

### Purpose

Expand Phase 2 carefully, without jumping to JSON schema or automation too soon.

Phase 2 asks:

```text
Did the AI request the exact correct prompt files, prompt groups, source files, generated artifacts, validation evidence, and freeze context before acting?
```

### Current closed pilots

```text
RG-025 startup delivery modification: PASS
RG-026 freeze with validation evidence already stated: PASS
RG-027 prompt-authoring anti-bypass request: PASS
```

### Next manual pilots

Add more manual pilots, but do not install them as project files yet.

Candidate pilots:

```text
RG-028 box-boundary patch request with protected freeze paths
RG-029 Python patch request requiring 08/09 Python prompt groups and validation evidence
RG-030 freeze-sensitive prompt-library update requiring active freeze context
RG-031 startup delivery maintenance request with stale filename trap
RG-032 local freeze workflow update requiring GUI public contract
RG-033 external project freeze request verifying no project_freeze_ledger contamination
RG-034 request with already-loaded context where AI must not over-request
RG-035 Fast Path task where AI must not over-route
```

### Manual pilot protocol

For each pilot:

1. Send scenario to tested AI.
2. Require `ROUTING RESPONSE`.
3. Grade completeness.
4. Grade precision.
5. Grade stale-reference handling.
6. Grade freeze-awareness.
7. Grade over-requesting.
8. Grade May proceed now.
9. Record result in chat/handoff.
10. Do not install pilot as file unless later registry step is approved.

### Freeze condition

Freeze only after multiple pilots demonstrate stable behavior and the user approves the manual test set as a project baseline.

## 6. Implementation 3 — Context Package Manifest standard

### Purpose

Create the central standard for what a task-specific context package must contain.

This becomes the heart of Phase 2.

### Primary box

```text
kanda_prompt_workspace/prompt_library/ROUTING_TESTS/PHASE_2_PROMPT_CALL_ACCURACY
```

### Possible file

```text
context_package_manifest_standard.md
```

### Context package fields

Each governed task should identify:

```text
task_type
primary_box
owner_paths
required_prompts
recommended_prompts
required_source_files
required_generated_artifacts
required_validation_evidence
required_freeze_context
forbidden_paths
forbidden_stale_references
may_proceed_now_expected
minimum_complete_context
over_requesting_risk
box_boundary_risk
freeze_memory_risk
```

### Important rule

This is not JSON automation yet.

It is a human-readable standard first.

### Freeze condition

Freeze after it successfully improves at least three manual pilots without creating over-requesting.

## 7. Implementation 4 — Prompt-request canon hardening

### Purpose

Harden the current prompt-request canon around exact prompt-call accuracy.

### Primary box

```text
kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/01_session_start_and_navigation
```

### Files likely involved

```text
ai_prompt_request_canon.md
daily_patch_delivery_guardrails.md
```

### Must enforce

1. Exact prompt names over generic labels.
2. Required vs recommended vs optional context.
3. No implementation before required context.
4. No asking again for validation evidence already provided.
5. Use active freeze context for freeze-sensitive tasks.
6. No stale generated filename references.
7. No project-specific memory in `project_freeze_ledger`.
8. Root-to-staging ZIP rule.
9. Sandbox pre-delivery validation gate.
10. End-of-work handoff rule.

### Freeze condition

Freeze after routing tests confirm the canon improves prompt-call accuracy without causing over-requesting in simple tasks.

## 8. Implementation 5 — Prompt authoring and audit canon hardening

### Purpose

Preserve and harden the prompt-authoring lifecycle.

### Primary box

```text
kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/07_prompt_authoring_and_audit
```

### Protected behavior

Prompt creation/update/register requests must not be implemented directly.

They must inspect:

```text
07_prompt_authoring_and_audit
prompt_canon_reconciliation_protocol
prompt_audit_canon
project_specific_prompt_generalization
relevant folder card
existing prompt-library assets/indexes
metadata rules
workflow registration requirements
validation steps
```

### Anti-bypass rule

If user says:

```text
skip checking existing prompts
```

AI must treat it as unsafe and must not comply.

### Freeze condition

Freeze after RG-015/RG-027-style tests continue passing.

## 9. Implementation 6 — Prompt schema and machine-readable index normalization

### Purpose

Return to the old roadmap’s schema/index work, but only after prompt-call accuracy is stable.

### Primary box

```text
kanda_prompt_workspace/prompt_library/ROUTING
kanda_prompt_workspace/prompt_library/METADATA
```

### Files likely created or updated

```text
prompt_schema_vocabulary.md
prompt_schema_vocabulary.json
prompt_navigation_index.json
PROMPT_NAVIGATION_INDEX.md
```

### Canonical values

Define stable values for:

```text
prompt status
audit status
load mode
missing behavior
dependency field names
conflict field names
date format
version format
hash format
override format
freeze relevance
context package role
```

### New fields to include

```text
canonical_id
status
audit_status
load_mode
required_for_task_types
recommended_for_task_types
context_package_role
freeze_sensitive
box_sensitive
validation_sensitive
stale_aliases
forbidden_aliases
```

### Freeze condition

Freeze only after validator can read the schema and current index without ambiguity.

## 10. Implementation 7 — Conflict, substitution, and integration ledgers

### Purpose

Create machine-readable governance ledgers.

### Files likely created

```text
prompt_conflict_ledger.json
prompt_substitution_map.json
integration_candidate_ledger.json
```

### Must track

Conflict ledger:

```text
prompt A
prompt B
severity
reason
human decision
```

Substitution map:

```text
deprecated prompt
replacement prompt
reason
status
date
```

Integration ledger:

```text
source prompt
target prompt
candidate logic
status
human decision
```

### Important

Do not auto-resolve conflicts.

### Freeze condition

Freeze when ledgers validate and no active routing depends on unresolved blocking conflicts.

## 11. Implementation 8 — Prompt-call validator design, not implementation yet

### Purpose

Design the validator after enough manual pilots exist.

Do not build too early.

### Inputs

```text
phase2_prompt_call_rubric.md
manual pilot results
context_package_manifest_standard.md
routing response examples
```

### Validator should eventually check

```text
required prompts named
required source files named
required generated artifacts named
validation evidence handled correctly
freeze context requested when needed
forbidden stale references avoided
May proceed now correct
over-requesting controlled
```

### Do not create yet

```text
phase2_prompt_call_expected_outputs.json
phase2_prompt_call_validator.py
batch validator
```

### Freeze condition

Validator design freezes before code implementation.

## 12. Implementation 9 — First named prompt stacks

### Purpose

Only now return to prompt stacks.

Stacks should be built from already-indexed, audited prompts.

### First stacks

```text
SESSION_START
PROMPT_CALL_ACCURACY_TEST
PROMPT_AUTHORING_AUDIT
CREATE_CODE_PATCH
STARTUP_DELIVERY_MAINTENANCE
FREEZE_FEATURE_AFTER_UPDATE
BOX_BOUNDARY_REVIEW
VALIDATE_STEP
HANDOFF_SESSION
```

### Each stack must define

```text
stack_id
purpose
entry_condition
exit_condition
required_prompt_ids
recommended_prompt_ids
minimum_viable_context
required_freeze_context
missing_behavior
status
last_tested
test_status
auto_dispatch_allowed
```

### Freeze condition

A stack freezes only after two-chat testing passes.

## 13. Implementation 10 — Stack-level two-chat testing

### Purpose

A stack passes only if a fresh AI chat can use it without relying on previous chat memory.

### Two-chat protocol

Chat A:

```text
creates or updates stack
```

Chat B:

```text
receives stack and task
must return load check / routing response before acting
```

### Test categories

```text
SESSION_START
PROMPT_CALL_ACCURACY_TEST
CREATE_CODE_PATCH
STARTUP_DELIVERY_MAINTENANCE
FREEZE_FEATURE_AFTER_UPDATE
PROMPT_AUTHORING_AUDIT
HANDOFF_SESSION
```

### Freeze condition

Freeze after independent Chat B passes.

## 14. Implementation 11 — Validator upgrade

### Purpose

Upgrade existing validators after schema, ledgers, manifests, and stacks stabilize.

### Must validate

```text
schema vocabulary exists
prompt IDs unique
relative paths exist
no absolute Windows paths in prompt indexes
statuses valid
load modes valid
stale aliases registered
forbidden aliases blocked
stacks valid
required prompts exist
conflicts valid
substitution map valid
integration ledger valid
manual pilot registry valid, if created
no forbidden live app paths
startup ZIP in sync
active freeze context present
```

### Freeze condition

Freeze when validator reports clean gates or classified warnings only.

## 15. Implementation 12 — CLI Dispatcher v0 dry-run

### Purpose

Build automation only after prompt-call accuracy and stack validation are stable.

### v0 allowed behavior

```text
read prompt index
read prompt stacks
resolve stack
check required prompts
check conflicts
print dry-run manifest
```

### v0 forbidden behavior

```text
compose final prompt
copy to clipboard
call AI APIs
modify prompt files
auto-fix missing files
auto-resolve conflicts
```

### Freeze condition

Freeze when valid stacks pass and invalid stacks fail safely.

## 16. Implementation 13 — CLI Dispatcher v1 compose bundle

### Purpose

Compose prompt bundles after v0 is reliable.

### Output

```text
composed_prompt.md
dispatch_manifest.json
dispatch_audit.jsonl
```

### Required header

```text
STACK LOAD CHECK REQUIRED
Before solving the task, return:
- stack_id
- prompts recognized
- prompts missing
- conflicts detected
- freeze context status
- next action
```

### Freeze condition

Freeze when at least three stacks compose correctly and manifests match the composed files.

## 17. Implementation 14 — Prompt receipt/load-check protocol

### Purpose

Receiving AI must prove it loaded the correct prompts before acting.

### Required response

```text
STACK LOAD CHECK

Stack recognized:
Prompt files recognized:
Missing prompts:
Conflicts:
Freeze context recognized:
Routing behavior:
Next action:
```

### Freeze condition

Freeze when receiving AI consistently performs the load check first.

## 18. Implementation 15 — Local freeze workflow integration hardening

### Purpose

Continue hardening the now-frozen local freeze workflow.

### Primary boxes

```text
project_freeze_ledger/freeze_tools
kanda_reasoner_app/freeze_after_update
kanda_reasoner_app/freeze_after_update_gui
startup freeze context channel
```

### Next improvements

1. Improve local draft generation.
2. Improve editable form fields.
3. Improve AI-suggestion formulary round trip.
4. Keep preview read-only.
5. Keep Confirm and Write human-gated.
6. Refresh startup freeze context after write.
7. Keep AI review/export fallback only.

### Freeze condition

Freeze each GUI/contract improvement separately after local validation.

## 19. Implementation 16 — Dynamic freeze context publish mode

### Purpose

After the read-only exposure CLI v1, add explicit publish mode.

### Possible command

```text
python project_freeze_ledger\freeze_tools\expose_freeze_memory.py --project-root E:\kanda_reasoner --publish --yes
```

### Allowed outputs

```text
project_freeze_after_update/files_to_send_ai/current_freeze_memory_context.md
project_freeze_after_update/files_to_send_ai/freeze_exposure_report.json
```

### Forbidden

```text
no writing to frozen_features_memory
no repairing freeze_index.json
no active memory in project_freeze_ledger
no GUI in this patch
no startup injection of full memory
no ZIP by default
```

### Freeze condition

Freeze after validation proves only the two allowed generated files are written.

## 20. Implementation 17 — Desktop orchestration view

### Purpose

Only after CLI and prompt-call logic stabilize, create or update GUI orchestration.

### GUI may show

```text
prompt browser
stack viewer
dispatch preview
manual pilot results
freeze context status
conflict ledger
substitution map
integration candidates
validation queue
```

### GUI must not own

```text
routing logic
freeze logic
prompt audit decisions
conflict resolution
stack validation
```

### Freeze condition

Freeze when GUI wraps public contracts only.

## 21. Implementation 18 — Meta-AI orchestrator

### Purpose

Gradual automation after prompt graph is stable.

### Stages

Stage 0:

```text
deterministic selector, no LLM
```

Stage 1:

```text
AI recommends stack; human approves
```

Stage 2:

```text
AI prepares dispatch preview; human approves
```

Stage 3:

```text
automatic only for frozen low-risk stacks
```

### Permanent prohibitions

Meta-AI must not:

```text
create prompts directly
update prompt index directly
update stack definitions directly
resolve conflicts automatically
override human governance
invent prompt IDs
write freeze memory silently
```

### Freeze condition

Automatic mode is allowed only after extensive evidence.

## 22. Implementation 19 — Session handoff and restart discipline

### Purpose

Every long session must end with a usable handoff.

### Handoff must include

```text
current implementation number
completed steps
files created
files modified
validation run
validation summary
frozen or not frozen
open decisions
next exact action
what not to touch
```

### Restart behavior

At the next chat:

```text
load latest startup pack
load active freeze context
load latest handoff
identify active implementation number
continue only that implementation
do not jump forward
```

## 23. Updated immediate next actions

The next safe action is not dispatcher work.

The next safe action is:

```text
Implementation 0 — Re-anchor current frozen prompt state
```

Create or update:

```text
PROMPT_SYSTEM_REANCHOR_REPORT.md
```

The report should confirm:

```text
Pre-Phase 2 scaffold/rubric is complete.
RG-025/RG-026/RG-027 were passed manually but not installed.
freeze_memory_exposure_cli_v1 is frozen.
freeze-feature local workflow v1 is frozen.
startup freeze context is active.
root-to-staging ZIP and sandbox pre-delivery rules are active.
```

After that, proceed to:

```text
Implementation 1 — Freeze-aware startup and prompt-call contract review
```

Only after these are stable should the roadmap return to schema/index normalization and dispatcher design.

## 24. Permanent roadmap rules

1. Do not install manual pilot tests unless explicitly creating a controlled registry.
2. Do not build JSON schemas before manual pilots stabilize.
3. Do not build validators before the rubric and context package manifest are stable.
4. Do not build dispatcher automation before prompt-call accuracy is reliable.
5. Do not inject full freeze memory into the normal startup ZIP.
6. Do not store active project freeze memory in project_freeze_ledger.
7. Do not create project_freeze_ledger inside external projects.
8. Do not use stale `paste_after_uploading_startup_zip.md` as an active delivery filename.
9. Do not deliver patches without sandbox validation first.
10. Do not tell the user a patch is complete until local validation passes.
11. Do not freeze unvalidated behavior.
12. Do not skip end-of-work handoff.
13. Do not let GUI boxes own domain logic.
14. Do not let generated files become source of truth.
15. Do not bypass Box Architecture owner paths.
