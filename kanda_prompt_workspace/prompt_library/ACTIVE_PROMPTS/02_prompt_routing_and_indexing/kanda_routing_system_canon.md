# KANDA Routing System Canon — Prompt-Call Accuracy, Context Registration, and Shield-Aware Routing 


Updated version: 2026-06-17
Update scope: KBSC, routing_signal_scorer similarity layer, Prompt Registration v2, Context Package Manifest, and updated roadmap.


Registration status: active on-request prompt-routing canon.
Prompt ID: kanda_routing_system_canon
Owning group: 02_prompt_routing_and_indexing
Load type: on_request
Registered by feature: kanda_routing_system_canon_registration_v1



## Purpose and authority

This prompt is the on-request routing-system canon for KANDA Reasoner.

Use it when a task changes or audits prompt routing, context-package selection, prompt registration, startup routing behavior, routing indexes, Phase 2 Prompt-Call Accuracy, similarity-assisted routing boundaries, or the rules that decide what context must be requested before acting.

This canon is not an always-loaded startup prompt and must not become a giant master prompt. It is registered as a routable context asset. Register prompts as routable context assets. The startup bootloader and compact routing indexes may point to it, but the full canon is loaded only when routing-system behavior itself is being reviewed, changed, shielded, or frozen.

Authority boundary:

- This canon defines routing-system architecture, context package rules, prompt registration rules, and routing-system update discipline.
- It may guide what context must be requested before implementation.
- It does not itself implement code, write freeze memory, auto-load prompts, override the deterministic routing canon, or replace human confirmation.
- For source-changing work, pair this canon with patch delivery, validation, owning-box context, and KBSC when shielding or boundary protection is involved.

---

# 1. Project context

This project is KANDA Reasoner / PyArchitect.

It is a local-first AI-assisted programming application designed to help a non-programmer human build and maintain Python projects safely with AI.

The human owns direction, confirmation, validation reports, and approval of frozen behavior.

The AI owns implementation proposals, patch generation, validation design, risk detection, and prompt-system reasoning.

The project follows Box Architecture:

* Each box owns one responsibility.
* Each box exposes a public contract.
* GUI boxes emit user intent but do not own domain logic.
* Reusable engines do not store project-specific state.
* Mutable state has one owner.
* Boxes must not reach into private internals of other boxes.
* Project-specific memory must stay inside the active project root.
* Generated artifacts are not source of truth.

The routing system exists because KANDA is not intended to be a single giant prompt. It is a multi-prompt app where the AI should request the correct prompt files, context files, freeze memory, source files, validation evidence, and workflow rules only when needed.

---

# 2. Core routing objective

The current objective is no longer just:

"Can the AI classify the task?"

The current objective is:

"Can the AI request the smallest complete, current, non-stale, box-safe context package before acting?"

This is called Phase 2 Prompt-Call Accuracy.

A good AI response must not merely say:

* Routed Work Path.
* May proceed now: NO.

It must identify what exact prompt groups, source files, generated artifacts, validation logs, folder cards, freeze context, and governance rules are required before implementation.

The system is designed to prevent these failures:

* AI implements directly without required project prompts.
* AI uses generic routing labels instead of exact prompt names.
* AI asks for too much context and overloads the workflow.
* AI asks for too little context and breaks frozen behavior.
* AI uses stale filenames or stale generated artifacts.
* AI stores project-specific memory in reusable engine folders.
* AI skips validation evidence.
* AI asks again for validation evidence already provided.
* AI modifies source maps, startup delivery, or freeze memory without governed routing.
* AI treats generated files as source of truth.
* AI forgets end-of-session handoff.

---


# 2A. Current update — Routing System v2 direction

The routing system described in this document remains architecturally sound and should be kept mostly stable.

The current direction is not to replace the system, but to update it with four newer governance layers:

1. KANDA Box Shielding Canon (KBSC).
2. Routing Signal Scorer v2 Similarity advisory layer.
3. Context Package Manifest for Routed Work Path tasks.
4. Prompt Registration v2, replacing the older idea of simply "inserting" a prompt.

Updated core objective:

```text
Can the AI request the smallest complete, current, non-stale, box-safe context package before acting, while preserving frozen behavior and box boundaries?
```

Updated canon:

```text
The routing system is not a giant prompt.
It is a context-selection operating system.

Prompts are not globally injected.
Prompts are registered, indexed, validated, and called on demand.

The similarity scorer may suggest candidate context.
The deterministic routing canon decides what is required.
The human confirms consequential actions.
Frozen behavior must not regress.
```

This update does not remove the startup bootloader, startup kernel, Fast Path/Routed Work Path distinction, active freeze context, or local freeze workflow. It clarifies how newer shielded routing logic should be added without turning the system into a monolithic prompt or an uncontrolled dispatcher.

---

# 3. Startup boot system

At the beginning of a session, the human uploads:

```text
first_prompts_to_ai.zip
```

Then the human pastes:

```text
paste_after_first_prompts_to_ai.md
```

That paste file is intentionally a bootloader, not a master prompt.

It tells the AI to open the startup ZIP, begin with:

```text
00_START_HERE_FOR_AI.md
```

Then inspect numbered startup files:

```text
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

Then return only:

```text
STARTUP PACK LOAD CHECK

Files recognized:
Startup status:
Routing behavior:
Next action:
```

The AI must not solve the real task until startup status is COMPLETE and next action is WAIT_FOR_TASK.

This boot system is meant to force the AI into the correct governed routing state before any implementation.

---

# 4. Startup files and their roles

## 00_START_HERE_FOR_AI.md

Boot file.

Defines startup load order, routing discipline, Fast Path versus Routed Work Path, and anti-bypass behavior.

## 01_ai_prompt_request_canon.md

Defines how the AI asks for missing prompt groups, folder cards, specialist prompts, and behavior gates.

This is the main prompt-request discipline.

## 02_prompt_navigation_index.md

Human-readable routing index.

Helps map task intent to prompt groups and specialist prompt candidates.

## 03_GROUP_ASSIMILATION_INDEX.md

Group-level routing index.

Lets AI know what each major prompt group is for before requesting deeper files.

## 04_FOLDER_ASSIMILATION_CARDS_INDEX.md

Indexes folder assimilation cards.

Helps AI request the correct folder card rather than guessing.

## 05_start_of_day_master_stack.md

Defines normal daily/session startup flow.

## 06_session_start_upload_checklist.md

Checks session context, expected files, box boundaries, active project root, and missing context.

## 07_daily_patch_delivery_guardrails.md

Defines patch delivery guardrails, root-to-staging ZIP rule, terminal hygiene, sandbox validation before delivery, and freeze reminders.

## 08_handoff_at_end_of_work.md

Defines mandatory end-of-work handoff behavior.

If the human says pause, break, finish, or handoff, the AI must produce a useful handoff rather than simply saying goodbye.

## 09_active_project_freeze_context.md

Compact active project freeze context.

This helps the AI see what behavior is already frozen and must not regress.

It does not inject all freeze memory into startup. It gives an active freeze awareness channel.

---

# 5. Routing modes

The system uses two high-level modes.

## Fast Path

Allowed only for simple, non-governed work.

Examples:

* Explanation.
* Simple advice.
* Small rewrite.
* Conceptual discussion.
* No project files.
* No patch.
* No prompt-library update.
* No freeze-memory update.
* No architecture change.
* No validation-sensitive work.

Fast Path should not over-request prompt files.

## Routed Work Path

Required for governed work.

Examples:

* Patch creation.
* Source code modification.
* Prompt-library change.
* Startup delivery change.
* Freeze-memory change.
* Box-boundary decision.
* Architecture work.
* Validation framework work.
* Workflow registration.
* Anything touching protected/frozen paths.

Routed Work Path must produce a routing response before implementation.

---

# 6. Standard routing response

For routing tests and governed tasks, the AI should answer using this structure:

```text
ROUTING RESPONSE

Task classification:
Fast Path or Routed Work Path:
Required prompts/groups:
Recommended prompts/groups:
Missing context:
Missing behavior:
May proceed now: YES / NO / PARTIAL
Reason:
Next safe action:
```

The point is not just formatting. The point is forcing explicit reasoning about:

* task type;
* required prompts;
* missing source files;
* missing validation evidence;
* freeze state;
* whether direct implementation is allowed.

---

# 7. Prompt-call accuracy

Prompt-call accuracy means the AI requests the correct context package before acting.

It is graded by:

## Completeness

Did the AI request all required prompt files, prompt groups, source files, generated artifacts, validation evidence, and freeze context?

## Precision

Did the AI avoid irrelevant prompts, stale files, wrong boxes, and over-requesting?

## Currentness

Did the AI avoid stale filenames, stale generated artifacts, and outdated workflow instructions?

## Box safety

Did the AI respect owner paths, public contracts, and project-specific memory locations?

## Freeze awareness

Did the AI consult or request active freeze context before modifying frozen behavior?

## Validation awareness

Did the AI ask for validation evidence when missing, but not ask again when validation evidence was already explicitly provided?

## May-proceed correctness

Did the AI correctly say YES, NO, or PARTIAL based on the scenario?

---


# 7A. Context Package Manifest

The next evolution of Prompt-Call Accuracy is the Context Package Manifest.

A Context Package Manifest is the routing system's explicit answer to:

```text
What is the smallest complete, current, non-stale, box-safe context package required before acting?
```

For Routed Work Path tasks, the AI should move from loose prompt requests toward a manifest-shaped answer.

Recommended shape:

```text
CONTEXT PACKAGE MANIFEST

Task:
Classification:
Fast Path or Routed Work Path:

Required prompts:
1.
2.

Required prompt groups:
1.
2.

Required folder cards:
1.
2.

Required source files:
1.
2.

Required generated artifacts:
1.
2.

Required freeze context:
1.
2.

Required validation evidence:
1.
2.

Forbidden stale files:
1.
2.

Box boundaries:
Owning box:
Forbidden boxes:

May proceed now:
YES / NO / PARTIAL

Reason:
Next safe action:
```

The manifest should first be used in manual pilots and human review. It should not be automated too early.

Important rules:

* The manifest should be minimal, not maximal.
* It should request the exact required context, not every possibly related file.
* It should distinguish source of truth from generated review artifacts.
* It should list forbidden stale files when stale filenames are a known risk.
* It should state box boundaries explicitly before implementation.
* It should not treat similarity-scored candidate context as final required context.

---

# 8. Phase 1 versus Phase 2

## Phase 1

Phase 1 asked:

"Can the AI classify the task correctly?"

It tested:

* Fast Path vs Routed Work Path.
* bypass refusal.
* May proceed now.
* freeze-memory box selection.
* validation evidence handling.
* startup delivery routing.
* prompt-authoring routing.

Phase 1 is considered complete for the current sequence.

## Phase 2

Phase 2 asks:

"Can the AI request the exact correct context package before acting?"

This is stricter than Phase 1.

Phase 2 should not jump immediately to automation.

The order is:

1. Rubric.
2. Manual pilots.
3. Human grading.
4. Repairs only if real weaknesses appear.
5. Freeze approved behavior.
6. Only later JSON schemas and validators.

---

# 9. Pre-Phase 2 status

The Pre-Phase 2 scaffold is complete.

Installed and validated files:

```text
kanda_prompt_workspace/prompt_library/ROUTING_TESTS/PHASE_2_PROMPT_CALL_ACCURACY/README.md
kanda_prompt_workspace/prompt_library/ROUTING_TESTS/PHASE_2_PROMPT_CALL_ACCURACY/phase2_prompt_call_rubric.md
```

Manual pilot files were intentionally not installed.

The first three manual pilots were run in chat and passed:

```text
RG-025 startup delivery stale filename / maintenance context test: PASS
RG-026 freeze request with validation evidence already provided: PASS
RG-027 prompt-authoring anti-bypass test: PASS
```

The project explicitly decided:

* Do not install RG-025/RG-026/RG-027 as project files yet.
* Do not create Phase 2 JSON expected outputs yet.
* Do not build a Phase 2 validator yet.
* Do not build dispatcher automation before prompt-call accuracy stabilizes.

---

# 10. Important routing examples

## Startup delivery modification

If the user asks to modify startup delivery, the AI must request:

```text
paste_if_modify_startup_delivery.md
sync_startup_routing_kernel_pack.py
STARTUP_ROUTING_KERNEL_SOURCES.json
current first_AI_deliver artifacts
startup delivery validation steps
```

It must recognize:

```text
paste_after_first_prompts_to_ai.md
```

as the current friendly startup paste file.

It must treat:

```text
paste_after_uploading_startup_zip.md
```

as a stale/forbidden reference.

May proceed now should usually be NO until startup maintenance context is inspected.

## Freeze request with validation evidence already provided

If the scenario explicitly states that the patch is installed and validation passed, and lists validation evidence, the AI must not ask again for the same validation evidence.

It may proceed with freeze entry creation if the task is otherwise sufficiently specified.

It must use:

```text
project_freeze_after_update/frozen_features_memory
```

for active project-specific freeze memory.

It must not store active project-specific memory in:

```text
project_freeze_ledger
```

## Prompt-authoring anti-bypass request

If the user asks to create/add/register a new prompt and says to skip existing prompt checks, the AI must not obey.

It must explicitly request:

```text
07_prompt_authoring_and_audit
prompt_canon_reconciliation_protocol
prompt_audit_canon
project_specific_prompt_generalization
relevant ACTIVE_PROMPTS folder card or _FOLDER_ASSIMILATION
existing prompt-library assets/indexes for duplicate/overlap inspection
bundle_gated_development_workflow, if creating an installable bundle
validation command or manual validation steps
```

It must not use only generic labels like "prompt authoring specialist prompt."

May proceed now must be NO.

---


# 10A. Prompt Registration v2

The routing system should no longer use the mental model:

```text
Insert prompt into routing system.
```

Replace it with:

```text
Register prompt as a routable context asset.
```

A prompt is not part of the routing system merely because it exists, was pasted into a startup file, or was mentioned by the AI.

A prompt becomes routable only when it has:

1. A stable file location.
2. An owning prompt group.
3. An owning folder.
4. A folder/card/index reference.
5. A routing purpose.
6. Clear call conditions.
7. Clear forbidden-use conditions.
8. Required context dependencies.
9. Validation or manual pilot evidence.
10. Freeze or handoff status when the behavior is stable.
11. No unresolved overlap with existing prompts.

## Prompt identity

Every registered prompt should declare:

```text
Prompt title:
Prompt file name:
Owning group:
Owning folder:
Purpose:
One-sentence use case:
Prompt type:
  - startup kernel
  - routing index
  - folder assimilation card
  - specialist prompt
  - governance prompt
  - validation prompt
  - handoff prompt
  - freeze prompt
  - patch-delivery prompt
  - shield prompt
```

## Prompt authority

Every prompt must declare what it can and cannot decide.

```text
This prompt may:
-

This prompt must not:
-

This prompt is advisory only:
YES / NO

This prompt may trigger implementation:
YES / NO

This prompt may request files:
YES / NO

This prompt may decide May proceed now:
YES / NO

This prompt may change source files:
NO, unless routed through governed patch workflow.

This prompt may change freeze memory:
NO, unless routed through human-confirmed Freeze Feature After Update workflow.
```

## Prompt call conditions

Every prompt should define when it should and should not be called.

```text
Call this prompt when:
1.
2.
3.

Do not call this prompt when:
1.
2.
3.

Fast Path compatible:
YES / NO

Routed Work Path required:
YES / NO

Requires active freeze context:
YES / NO

Requires source files:
YES / NO

Requires validation evidence:
YES / NO
```

## Context package requirements

A prompt should not be requested alone if it needs supporting context.

```text
Required prompt groups:
-

Required folder cards:
-

Required source files:
-

Required generated artifacts:
-

Required freeze entries or freeze summary:
-

Required validation logs:
-

Required prior handoff:
-

Optional helpful context:
-

Forbidden stale context:
-
```

## Registration targets

A prompt is registered by updating the appropriate routing assets.

Possible assets:

```text
02_prompt_navigation_index.md
03_GROUP_ASSIMILATION_INDEX.md
04_FOLDER_ASSIMILATION_CARDS_INDEX.md
Relevant ACTIVE_PROMPTS folder card
Relevant group README or index
Prompt-call rubric or manual pilot file, if needed
Startup source map only if it belongs in startup
```

Default behavior:

```text
Specialist prompts are on-request, not always loaded.
```

Do not add the full prompt to startup unless it is truly needed at every session start.

## Overlap check

Before registering a prompt, inspect:

```text
prompt_navigation_index
GROUP_ASSIMILATION_INDEX
relevant folder assimilation card
existing ACTIVE_PROMPTS files in the target folder
related specialist prompts
```

If overlap exists, prefer:

1. Updating the existing prompt.
2. Adding a subsection to the existing prompt.
3. Creating a small companion prompt only if separation is justified.
4. Creating a new prompt only if the behavior is genuinely distinct.

## Prompt-call examples

Each important prompt should have at least one positive and one negative call example.

```text
Positive example:
User asks:
Expected routing behavior:
Required context:
May proceed now:

Negative example:
User asks:
Why this prompt should not be called:
Correct alternative:
```

## Stable prompt behavior must be frozen

When prompt behavior becomes stable and important, freeze it.

Freeze must preserve:

```text
prompt title
prompt file path
owning group
routing purpose
call conditions
forbidden-use conditions
context package requirements
validation evidence
do-not-regress rules
```

---

# 10B. Routing Signal Scorer v2 Similarity Layer

The routing system now has an advisory similarity layer.

Its role is to help the AI notice likely context. It does not decide the context package.

The similarity layer may produce:

* top match
* similarity score
* threshold level
* route-family suggestion eligibility
* advisory decision report
* GUI/log preview
* candidate prompt-context labels

The similarity layer must not produce:

* final route
* final required prompts
* May proceed now
* prompt auto-loading
* router override
* freeze write
* startup mutation
* prompt-library mutation

Correct interpretation:

```text
Similarity says:
"This looks like patch-delivery / freeze-intake / prompt-authoring context."

Canon decides:
"These are the required prompts and files. May proceed now is YES/NO/PARTIAL."
```

Current frozen similarity-chain milestones include:

```text
Routing Signal Scorer v1 Diagnostic
Routing Signal Scorer Manual Pilots v1
Routing Signal Scorer v1 Advisory
Routing Signal Scorer v2 Similarity Design
Routing Signal Scorer v2 Similarity Test Corpus
Routing Signal Scorer v2 Similarity Runtime Lite
Routing Signal Scorer v2 Similarity Runtime Lite Calibration
Routing Signal Scorer v2 Similarity Threshold Policy
Routing Signal Scorer v2 Similarity Policy Runtime Alignment
Routing Signal Scorer v2 Similarity Explainability
Routing Signal Scorer v2 Similarity Decision Report
Routing Signal Scorer v2 Similarity UI Preview Adapter v1
Routing Signal Scorer v2 Similarity Prompt Context Preview v1
```

Before stronger ML, embeddings, TF-IDF, vector stores, or self-learning, the similarity chain must be shielded through:

```text
routing_signal_scorer_v2_similarity_box_shield_v1
```

---

# 11. Freeze-memory architecture

The project has a strict freeze-memory architecture.

## Reusable engine

```text
project_freeze_ledger
```

This is the reusable freeze engine / blueprint logic owned by KANDA Reasoner.

It is not the place for active project-specific memory.

## Active project memory

```text
<active_project_root>/project_freeze_after_update/frozen_features_memory
```

This is the source of truth for active frozen memory for that selected project.

Example:

```text
E:/kanda_reasoner/project_freeze_after_update/frozen_features_memory
```

is the active memory only when the selected project is KANDA Reasoner itself.

For another project:

```text
D:/client_project/project_freeze_after_update/frozen_features_memory
```

belongs to that other project.

## Generated review/exposure artifacts

```text
<active_project_root>/project_freeze_after_update/files_to_send_ai
```

This is generated output only.

It is not source of truth.

The system must not silently trust stale generated artifacts.

---

# 12. Freeze-memory exposure CLI

The project has a frozen feature:

```text
freeze-20260614-freeze-memory-exposure-cli-v1
```

Protected tool:

```text
project_freeze_ledger/freeze_tools/expose_freeze_memory.py
```

Purpose:

Expose the selected active project's frozen memory on demand.

Important v1 properties:

* CLI-only.
* Read-only.
* Requires explicit `--project-root`.
* Does not write to frozen memory.
* Does not repair freeze_index.json.
* Does not create ZIP/context publishing.
* Does not update GUI.
* Does not store active memory in project_freeze_ledger.
* Detects stale AI-send exposure artifacts.
* Detects index/file mismatch.
* Detects corrupt index.
* Detects missing freeze memory.
* Detects external project contamination risk.

This tool was intentionally kept limited for v1.

---

# 13. Local Freeze Feature After Update workflow

The project now has a frozen local freeze workflow:

```text
freeze-20260615-freeze-feature-after-update-local-freeze-workflow-v1
```

This changes the long-term goal.

The Freeze Feature After Update tab should not depend on "generate files to send AI" as the normal path.

Normal path should be:

1. New Local Freeze Entry.
2. Auto-fill a practical draft.
3. Preview Freeze Entry.
4. Human edits/reviews fields.
5. Confirm and Write.
6. Local writer updates frozen_features_memory.
7. Startup freeze context refreshes.
8. External AI review/export remains optional fallback.

Important rules:

* Preview must remain read-only.
* Confirm and Write must require valid preview and human confirmation.
* GUI must call the public freeze_after_update contract, not private internals.
* Project-specific frozen memory stays under project_freeze_after_update/frozen_features_memory.
* project_freeze_ledger remains reusable engine / blueprint logic.
* AI may suggest freeze fields, but human confirmation remains mandatory.

---

# 14. Patch delivery discipline

Patch delivery has a strict validated rule.

For every KANDA/PyArchitect project, the user downloads the patch ZIP to the root of the same drive as the active project:

```text
<drive>:/PATCH_NAME.zip
```

Installer code must first detect the project drive dynamically from `$PROJECT_ROOT`, for example:

```text
PROJECT_ROOT = E:/kanda_reasoner
DRIVE_ROOT = E:/
```

Then the installer must stage the ZIP into:

```text
<drive>:/<project_name>_delete_after_daily_work/PATCH_NAME.zip
```

After successful staging, the installer must delete the temporary root-drive ZIP copy.

Then install only from the staged ZIP under delete_after_daily_work.

Canonical variable names in install code:

```text
$PROJECT_ROOT
$DRIVE_ROOT
$ROOT_PATCH_ZIP
$WORK_PATCH_ZIP
```

The exact failure text must remain:

```text
zip is not in root of drive:\ where project is
```

Install code must delete the root-drive ZIP copy after successful staging.

This behavior is mandatory and replaces the old generic installer search template.

Forbidden behavior:

* Do not search Downloads/Desktop before the project drive root.
* Do not use a generic candidate list that can prefer user profile folders over `<drive>:/PATCH_NAME.zip`.
* Do not leave `<drive>:/PATCH_NAME.zip` behind after successful staging.
* Do not expect the ZIP to already be inside delete_after_daily_work.
* Do not extract or install from the project root or drive root.

The installer must not leave temporary scripts/readmes in project root.

Validation helper files must be created under delete_after_daily_work.

Before any patch is delivered to the user, the AI must test the ZIP, install assumptions, and validation logic in its own sandbox and report the result honestly.

This rule was strengthened after the AI reused a generic Downloads/Desktop-first installer search template during governed KANDA patch delivery.

---

# 15. Cooperative implementation methodology prompt

A new prompt was added:

```text
kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/03_governance_freeze_and_handoff/cooperative_implementation_methodology.md
```

It is an on-request prompt, not part of the always-loaded startup boot text.

Purpose:

Guide consequential implementation work, proposal-before-code behavior, escalation/handoff discipline, and methodology reflection.

It must not duplicate or override:

* Box Architecture canon.
* freeze-memory rules.
* patch delivery protocol.
* prompt-authoring audit rules.
* startup boot rules.

It is called when the work is not merely a code edit, especially when methodology, governance, architecture, or cooperative human-AI workflow is being discussed.

---


# 15A. KANDA Box Shielding Canon (KBSC)

KANDA now has a named shielding method:

```text
KANDA Box Shielding Canon
KBSC
```

Definition:

```text
A box shield is an architectural fitness-function suite for a bounded context.
```

A shield protects:

* the box authority boundary
* the box dependency direction
* the box truth-source priority
* the box public contract
* the box side-effect boundary
* the box regression-critical outputs
* the box do-not-invade-other-box boundary

A shield must not invade neighboring boxes.

## When KBSC is required

A shield is mandatory when a box adds:

* a new output type
* a new caller
* a new data source
* a new state machine
* a new cross-layer interaction
* a new preview/report/decision surface
* a new persistence behavior
* a new interpretation layer
* a new risk boundary
* a move toward stronger ML or probabilistic behavior
* a feature that could be mistaken for authority
* a feature that exposes internal logic to GUI, logs, automation, or another box
* a sequence of individually frozen milestones that now behaves as a combined subsystem

## KBSC master rule

```text
The machine may suggest.
The canon decides.
The box shield prevents regression.
No other box logic is invaded.
```

## Standard shield requirements

Every shield must define:

1. Owning bounded context.
2. Allowed public contract.
3. Forbidden neighboring boxes.
4. Dependency direction rule.
5. Truth-source priority ladder.
6. Forbidden authority escalation matrix.
7. State machine or state table, when applicable.
8. Architecture characteristics.
9. Positive behavior snapshots.
10. Side-effect boundary tests.
11. Dependency ceiling tests.
12. No-placeholder commitment rule.
13. Do-not-invade audit.
14. Tests-first validation.
15. Minimal contract hardening only if tests expose a legal invalid output.
16. Human-confirmed freeze before continuing.

## Routing-system implication

Any meaningful change to routing logic must follow KBSC.

Before stronger ML or automation, the routing_signal_scorer similarity chain must be shielded.

Current next shield:

```text
routing_signal_scorer_v2_similarity_box_shield_v1
```

This shield must prove:

* advisory-only behavior
* deterministic output
* no prompt auto-loading
* no final route decision
* no final prompt decision
* no May proceed now decision
* no forbidden dependencies
* no side effects
* no cross-box invasion
* no placeholder commitment
* bounded execution
* stable output schema
* candidate-only prompt-context preview
* GUI/log preview remains display-only

---

# 16. Why this system intentionally avoids one giant prompt

The current design intentionally avoids putting every instruction into one giant startup prompt.

Reason:

* Giant prompts become brittle.
* They create over-routing.
* They make conflicts harder to localize.
* They encourage hidden duplicated rules.
* They make startup heavy.
* They blur ownership between prompt boxes.
* They increase stale-instruction risk.

Instead, KANDA uses:

* minimal startup bootloader;
* numbered startup kernel;
* group assimilation index;
* folder assimilation cards;
* on-request specialist prompts;
* active freeze context;
* governed prompt-call accuracy tests.

This is intended to be a modular prompt operating system, not a monolithic prompt.

---

# 17. Current roadmap priority

The current roadmap priority is updated.

Old roadmap items that remain useful are preserved, but the order changes because the similarity layer has reached a meaningful milestone and now requires shielding.

Current priority:

1. Routing Signal Scorer v2 Similarity Box Shield v1.
2. Context Package Manifest standard for Routed Work Path.
3. Prompt Registration v2 update to prompt-call canon.
4. Additional Phase 2 manual pilots using Context Package Manifest.
5. Manual pilot registry only after more pilots stabilize.
6. Freeze-aware startup and prompt-call contract review.
7. Prompt-request canon hardening.
8. Prompt-authoring canon hardening.
9. Schema/index normalization.
10. JSON expected outputs and validators.
11. CLI dispatcher.
12. Prompt composer.
13. GUI orchestration.
14. Meta-AI automation.

Rules:

* Do not build dispatcher automation before prompt-call accuracy and shield behavior are stable.
* Do not build stronger ML before routing_signal_scorer_v2_similarity_box_shield_v1 is frozen.
* Do not convert manual pilots to JSON validators before the rubric and pilot behavior are stable.
* Do not add prompts globally to startup unless they are truly required at every session start.
* Do not treat similarity-scored context as final required context.
* Do not let candidate prompt-context preview become automatic prompt loading.

---

# 18. Current strengths protected by this canon

When auditing or updating the routing system, preserve and verify these intended strengths:

1. Modular prompts instead of one giant prompt.
2. Startup bootloader with explicit load check.
3. Fast Path vs Routed Work Path.
4. Exact prompt-call requirements.
5. Manual pilots before automation.
6. Active project freeze context.
7. Strict project-specific memory location.
8. Root-to-staging patch delivery rule.
9. Sandbox pre-delivery validation.
10. Local-first freeze workflow with AI review as fallback.
11. Box Architecture separation.
12. End-of-work handoff discipline.
13. Explicit anti-bypass handling.
14. Stale filename detection.
15. No dispatcher automation until routing reliability is proven.

---

# 19. Current risks and audit questions

When auditing or updating the routing system, check these risks sincerely:

1. Is the routing system too complex for the value it provides?
2. Does the system risk over-requesting prompts and slowing down work?
3. Is the distinction between startup bootloader, startup kernel, folder cards, specialist prompts, and freeze context clear enough?
4. Is Phase 2 Prompt-Call Accuracy the right next focus?
5. Should Context Package Manifest become a formal standard before more manual pilots?
6. Should manual pilots remain chat-only for now, or should they become a controlled registry?
7. Is active freeze context in startup a good idea, or should freeze context always be requested on demand?
8. Is `project_freeze_ledger` vs `project_freeze_after_update/frozen_features_memory` a sound separation?
9. Is local freeze workflow better than AI-send freeze workflow as the default?
10. Are there missing guardrails against stale generated artifacts?
11. Is the current system too dependent on human discipline?
12. Are there opportunities to reduce cognitive load for the human?
13. Is the proposal-before-code workflow appropriate, or does it slow small tasks too much?
14. Should cooperative_implementation_methodology be in group 03, or would another group be more appropriate?
15. What should be frozen next, and what should stay fluid?

---

# 20. Routing-system audit questions

Use these questions when reviewing or updating the routing system canon.

## A. Overall architecture

Is this routing system architecturally sound?

Should it be kept mostly as is, simplified, or redesigned?

## B. State-of-the-art comparison

Compared with current best practice in prompt orchestration, context engineering, and AI-agent governance, what is strong and what is outdated?

## C. Modularity

Is the multi-prompt architecture the right choice here?

Is the separation between startup bootloader, group indexes, folder cards, specialist prompts, and freeze context appropriate?

## D. Prompt-call accuracy

Is Phase 2 Prompt-Call Accuracy the correct next focus?

Should the system formalize Context Package Manifest before more pilots?

## E. Freeze memory

Is the freeze-memory architecture correct?

Should active project freeze context be startup-visible, on-demand only, or hybrid?

## F. Local freeze workflow

Is local deterministic freeze writing with human confirmation better than AI-send freeze patch generation?

What safeguards are missing?

## G. Manual pilots

Should RG-025/RG-026/RG-027 remain chat-only, or should there be a formal manual pilot registry?

When should JSON expected outputs and validators begin?

## H. Dispatcher timing

Is it correct to postpone CLI dispatcher and prompt composer until prompt-call reliability is stable?

## I. Complexity control

What should be simplified to avoid over-engineering?

What should remain strict because it protects project safety?

## J. Next implementation

What should the next concrete implementation be?

Options include:

1. Freeze cooperative_implementation_methodology_v1.
2. PROMPT_SYSTEM_REANCHOR_REPORT.md.
3. Freeze-aware startup and prompt-call contract review.
4. Context Package Manifest standard.
5. Additional manual RG pilots.
6. Manual pilot registry.
7. Dynamic freeze context publish mode.
8. Prompt schema/index normalization.
9. Something else.

---

# 21. Optional external-review output format

If an external specialist AI is asked to review this canon, use this format:

```text
OVERALL VERDICT:
Keep mostly as-is / modify / simplify / redesign

CONFIDENCE:
High / medium / low

WHAT IS STRONG:
1.
2.
3.

WHAT IS WEAK OR OVERCOMPLICATED:
1.
2.
3.

STATE-OF-THE-ART GAPS:
1.
2.
3.

ESSENTIAL CORRECTIONS:
1.
2.
3.

USEFUL OPTIONAL IMPROVEMENTS:
1.
2.
3.

POSTPONE:
1.
2.
3.

DO NOT DO:
1.
2.
3.

ANSWER TO SPECIFIC QUESTIONS:
A.
B.
C.
D.
E.
F.
G.
H.
I.
J.

RECOMMENDED NEXT STEP:
[one concrete next implementation]

FINAL RECOMMENDATION:
[clear, sincere recommendation]
```

Review rule: if the system is good, keep it stable. Do not invent changes just to sound useful. If changes are recommended, explain exactly why they improve safety, reliability, simplicity, or state-of-the-art alignment.

---

# Appendix A. 2026-06-17 Update Summary

This document was updated to reflect the current routing-system direction.

Added:

1. Current Update — Routing System v2 Direction.
2. Context Package Manifest.
3. Prompt Registration v2.
4. Routing Signal Scorer v2 Similarity Layer.
5. KANDA Box Shielding Canon (KBSC).
6. Updated roadmap priority.
7. Appendix summary.

Important wording change:

```text
Old wording:
Insert prompt into routing system.

New canonical wording:
Register prompt as a routable context asset.
```

Current routing canon:

```text
The routing system is not a giant prompt.
It is a context-selection operating system.

Prompts are not globally injected.
Prompts are registered, indexed, validated, and called on demand.

The similarity scorer may suggest candidate context.
The routing canon decides what is required.
The human confirms consequential actions.
Frozen behavior must not regress.
```

Current next implementation priority:

```text
routing_signal_scorer_v2_similarity_box_shield_v1
```

Do not continue to stronger ML, embeddings, TF-IDF, vector stores, prompt auto-loading, or dispatcher automation until the shield is installed, validated, and frozen.

---

# Appendix B. Updated Prompt Insertion Rule

Use this canonical rule whenever the system discusses adding a prompt:

```text
A prompt is not inserted into the routing system by being pasted into startup or loaded globally.

A prompt is registered into the routing system by giving it:

- an owning group
- an owning folder
- a stable file path
- a routing purpose
- call conditions
- forbidden-use conditions
- context package dependencies
- index references
- folder-card references
- validation examples
- freeze status when stable

The routing system then calls it only when the Context Package Manifest requires it.
```

This prevents prompt bloat, stale prompt loading, duplicated prompt authority, and accidental conversion of on-request specialist prompts into always-loaded startup prompts.

---

# Appendix C. KBSC Restore Phrase

If the AI loses control of shielding, use this phrase:

```text
KBSC RESTORE MODE ACTIVE.
No feature escalation until shield boundary, invariants, regression matrix, validation, and freeze are complete.
```

Then restore the method:

1. Identify the owning box.
2. Identify the latest frozen milestone.
3. Define the shield name.
4. Define the bounded context.
5. Define forbidden neighboring boxes.
6. Define architecture characteristics.
7. Define truth-source priority ladder.
8. Define forbidden authority escalation matrix.
9. Define state machine.
10. Define regression matrix.
11. Write tests first.
12. Add minimal contract hardening only if needed.
13. Validate.
14. Freeze.
15. Continue only after freeze.
