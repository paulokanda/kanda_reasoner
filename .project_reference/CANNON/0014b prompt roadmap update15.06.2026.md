# Complete Numbered Roadmap — KANDA Routing Logic Update

## Current strategic decision

Keep KANDA’s routing architecture mostly as-is.

Do not merge the startup bootloader.
Do not collapse the startup kernel now.
Do not build dispatcher automation yet.
Do not build Phase 2 JSON schemas or automated validators yet.

The routing update should be incremental and safety-preserving.

The next goal is to improve:

1. prompt-call accuracy;
2. routing-index clarity;
3. conditional context rules;
4. startup staleness awareness;
5. manual pilot feedback;
6. freeze-aware routing discipline.

---

# 0. Current baseline

## 0.1 Already complete

* Startup prompt kernel exists and is active.
* Pre-Phase 2 Prompt-Call Accuracy scaffold is installed and validated.
* RG-025, RG-026, and RG-027 passed manually in chat.
* Manual pilot files are not installed as permanent project files.
* `cooperative_implementation_methodology_v1` is installed and validated.
* Startup delivery is `IN_SYNC`.
* Freeze-memory exposure CLI v1 is installed, validated, and frozen.
* Local Freeze Feature After Update workflow v1 is already frozen.
* Root-to-staging ZIP rule is active.
* Sandbox pre-delivery validation rule is active.

## 0.2 Current open item

`cooperative_implementation_methodology_v1` is installed and validated, but not yet frozen.

---

# 1. Freeze cooperative_implementation_methodology_v1

## Purpose

Close the current open governance prompt before starting new routing changes.

## Feature to freeze

```text
cooperative_implementation_methodology_v1
```

## Freeze should protect

```text
kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/03_governance_freeze_and_handoff/cooperative_implementation_methodology.md
kanda_prompt_workspace/prompt_library/METADATA/cooperative_implementation_methodology.meta.json
kanda_prompt_workspace/prompt_library/ROUTING/prompt_navigation_index.json
kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/02_prompt_routing_and_indexing/prompt_navigation_index.md
kanda_prompt_workspace/prompt_library/ROUTING/GROUP_ASSIMILATION_INDEX.md
kanda_prompt_workspace/prompt_library/ROUTING/FOLDER_ASSIMILATION_CARDS_INDEX.md
kanda_prompt_workspace/first_AI_deliver/first_prompts_to_ai.zip
```

## Do-not-regress rules

* Keep it as an on-request methodology prompt.
* Do not turn it into a mandatory startup prompt.
* Do not duplicate Box Architecture rules.
* Do not duplicate freeze-memory rules.
* Do not duplicate patch-delivery protocol.
* Do not duplicate prompt-authoring audit rules.
* Use it for consequential implementation methodology, proposal-before-code, escalation, and cooperative workflow discipline.

## Validation needed

Validation already passed:

```text
VALIDATION OK: cooperative_implementation_methodology_v1
STATUS: IN_SYNC
```

## Next action

Use Freeze Feature After Update tab or local freeze workflow to freeze it.

---

# 2. Add routing-index escalation rule

## Purpose

Clarify how the AI should use the three routing indexes.

Current risk:

```text
GROUP_ASSIMILATION_INDEX
FOLDER_ASSIMILATION_CARDS_INDEX
prompt_navigation_index
```

can overlap conceptually. Without a decision rule, the AI may over-request or use them ceremonially.

## Rule to add

```text
1. Use GROUP_ASSIMILATION_INDEX first to identify the broad prompt group.
2. Use FOLDER_ASSIMILATION_CARDS_INDEX only when the group is known but the exact folder, card, or sub-area is ambiguous.
3. Use prompt_navigation_index when the exact prompt file, prompt ID, path, or routing requirement must be selected or verified.
```

## Likely files to update

```text
kanda_prompt_workspace/prompt_library/ROUTING/GROUP_ASSIMILATION_INDEX.md
kanda_prompt_workspace/prompt_library/ROUTING/FOLDER_ASSIMILATION_CARDS_INDEX.md
kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/02_prompt_routing_and_indexing/prompt_navigation_index.md
```

Possibly also:

```text
kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/01_session_start_and_navigation/ai_prompt_request_canon.md
```

## What not to do

* Do not merge the three files now.
* Do not collapse startup kernel.
* Do not create dispatcher logic.
* Do not create a resolver map yet.

## Validation

Manual routing scenarios:

1. task clearly maps to one group;
2. task maps to a group but folder is ambiguous;
3. task needs exact prompt file;
4. task needs startup delivery maintenance;
5. task needs prompt-authoring anti-bypass handling.

## Freeze condition

Freeze after validation proves the AI uses the three indexes in the correct order without over-requesting.

---

# 3. Add startup kernel staleness check

## Purpose

Prevent the startup kernel from silently falling behind newer frozen behavior.

The freeze-memory exposure CLI detects stale AI-send artifacts, but startup files themselves can become stale relative to active freeze memory.

## Rule to add

To session startup checklist:

```text
If active project freeze memory contains entries newer than the startup kernel generation time, flag STARTUP_KERNEL_STALENESS_REVIEW.
```

This does not need to block every session. It should warn when review is needed.

## Likely file to update

```text
kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/01_session_start_and_navigation/session_start_upload_checklist.md
```

or its current canonical startup checklist file.

## Optional generated marker

If already available from startup manifest:

```text
STARTUP_PROMPT_REQUEST_KERNEL_MANIFEST.json generated_at
```

compare conceptually with active freeze context timestamp.

## What not to do

* Do not auto-repair startup kernel.
* Do not rebuild startup ZIP silently.
* Do not inject full freeze memory into startup.
* Do not fail startup merely because a newer freeze exists.

## Validation

Manual validation should confirm:

* no warning when startup manifest is current;
* warning when freeze memory is newer than startup manifest;
* no false claim that startup is broken;
* recommendation is review/regenerate, not automatic mutation.

## Freeze condition

Freeze after the warning behavior is validated.

---

# 4. Update Phase 2 rubric with conditional context inclusion

## Purpose

Improve prompt-call accuracy.

Current rubric uses required / recommended / optional / forbidden, but needs clearer handling for prompts that are required only under certain conditions.

## Add this concept

```text
Conditional required context
```

Example:

```text
08_python_engineering_core
Required IF Python source code, generator code, validation code, or install logic may be modified.
```

Another example:

```text
paste_if_modify_startup_delivery.md
Required IF the task modifies startup delivery, startup ZIP generation, source maps, first_AI_deliver, or startup naming.
```

Another example:

```text
active project freeze context
Required IF task touches frozen behavior, protected paths, freeze workflow, project memory, or governance artifacts.
```

## Likely file to update

```text
kanda_prompt_workspace/prompt_library/ROUTING_TESTS/PHASE_2_PROMPT_CALL_ACCURACY/phase2_prompt_call_rubric.md
```

## Add scoring rule

```text
PASS:
The AI correctly identifies conditional required context when the condition is true.

PARTIAL:
The AI lists it as recommended when it should be conditional-required.

FAIL:
The AI omits conditional-required context and proceeds unsafely.
```

## What not to do

* Do not create JSON schema yet.
* Do not create validator yet.
* Do not create formal Context Package Manifest yet.
* Do not install manual pilot files yet.

## Validation

Run manual routing tests where condition is true and false:

1. Python code patch;
2. non-code discussion;
3. startup delivery patch;
4. freeze-sensitive update;
5. prompt-authoring request.

## Freeze condition

Freeze after at least two manual pilots show improved conditional-context behavior.

---

# 5. Add context load awareness to ROUTING RESPONSE

## Purpose

Reduce over-requesting.

Prompt-call accuracy should not mean “ask for everything.” It means ask for the smallest complete safe package.

## Add optional field

```text
Estimated context load:
small / medium / large
```

## Updated routing response

```text
ROUTING RESPONSE

Task classification:
Fast Path or Routed Work Path:
Required prompts/groups:
Recommended prompts/groups:
Missing context:
Missing behavior:
Estimated context load:
May proceed now: YES / NO / PARTIAL
Reason:
Next safe action:
```

## Rule

If Estimated context load is large, the AI should explain why the larger context package is justified.

## Likely files to update

```text
phase2_prompt_call_rubric.md
ai_prompt_request_canon.md
possibly 00_START_HERE_FOR_AI.md
```

## What not to do

* Do not make this a hard token-count calculator.
* Do not require exact token estimation.
* Do not block implementation only because load is large.

## Validation

Manual tests should check:

* simple task stays small;
* prompt-authoring audit is medium/large but justified;
* startup delivery modification is medium/large but justified;
* AI does not request 20 prompts for a narrow task.

## Freeze condition

Freeze after it reduces over-requesting without weakening safety.

---

# 6. Run two to three additional Phase 2 manual pilots

## Purpose

Gather more evidence before building any automation.

## Candidate pilots

```text
RG-028:
Box-boundary patch request touching protected paths.

RG-029:
Python generator patch requiring conditional Python engineering prompts.

RG-030:
Freeze-sensitive prompt-library update requiring active freeze context.

RG-031:
Startup delivery maintenance request with stale filename trap.

RG-032:
Fast Path task where AI must not over-route.
```

## Protocol

Each pilot remains chat-only for now.

For each:

1. Paste scenario into tested AI.
2. Require ROUTING RESPONSE.
3. Grade:

   * completeness;
   * precision;
   * conditional context;
   * stale reference handling;
   * freeze awareness;
   * over-requesting;
   * May proceed now;
   * next safe action.
4. Record PASS / PARTIAL / FAIL in handoff or session notes.

## What not to do

* Do not install pilot files yet.
* Do not build JSON expected outputs yet.
* Do not build validator yet.

## Freeze condition

After at least five total Phase 2 pilots pass across diverse scenarios, decide whether to create a lightweight manual pilot registry.

---

# 7. Create lightweight routing failure log

## Purpose

Create a feedback loop from routing failures into prompt improvement.

This is not automation. It is a human-readable log.

## Suggested file

```text
kanda_prompt_workspace/prompt_library/ROUTING_TESTS/routing_failure_log.md
```

## Log format

```text
Date:
Scenario:
Expected routing:
Actual routing:
Failure type:
- missing required prompt
- over-requested context
- stale reference
- wrong May proceed now
- ignored freeze context
- wrong box
- asked again for already-provided validation
- implemented directly
Root cause:
Prompt/rule likely needing repair:
Decision:
```

## What not to do

* Do not convert to JSON yet.
* Do not create automated failure parser.
* Do not make this part of dispatcher.

## Validation

Add one synthetic example and ensure it is easy to maintain manually.

## Freeze condition

Freeze after the log format is used in at least one real failed or partial pilot.

---

# 8. Review cooperative_implementation_methodology placement and cross-references

## Purpose

The prompt is currently in:

```text
03_governance_freeze_and_handoff
```

This is acceptable, but it is cross-cutting and must be findable from implementation contexts.

## Best approach

Do not move it now.

Instead, add routing hooks from relevant areas:

```text
05_patch_delivery_and_validation
07_prompt_authoring_and_audit
08_python_engineering_core
04_box_architecture_and_boundaries
```

## Rule

When work is consequential and requires proposal-before-code, methodology discussion, handoff, or human-confirmation discipline, request:

```text
cooperative_implementation_methodology.md
```

## What not to do

* Do not move the file immediately.
* Do not duplicate its content into other prompts.
* Do not make it always-loaded startup content.

## Validation

Manual tests:

1. method discussion should request it;
2. simple bug fix should not;
3. architectural patch should request it;
4. prompt-authoring governance task should request it.

## Freeze condition

Freeze after routing confirms it is discoverable but not over-triggered.

---

# 9. Defer formal Context Package Manifest

## Purpose

Avoid premature schema design.

The concept is good, but current advice is to observe more pilots first.

## Current decision

Postpone formal manifest implementation until more manual pilots run.

## Allowed now

Discuss the concept.
Add conditional context rules.
Use manual pilot observations.

## Not allowed yet

```text
context_package_manifest_standard.md
context_package_manifest.json
automated context package validator
resolver map derived from manifest
```

## Trigger to resume

Resume after:

```text
at least 5-8 diverse manual pilots
```

or repeated failures show that a manifest is needed earlier.

---

# 10. Defer prompt resolver map

## Purpose

Avoid creating dispatcher-like machinery too early.

The resolver map idea is useful, but it should be derived from stable manual pilots.

## Current decision

Postpone:

```text
99_PROMPT_RESOLVER_MAP.json
```

## Why

A resolver map could become a premature source of truth before prompt-call behavior is stable.

## Trigger to resume

Resume after:

* manual pilots stabilize;
* conditional context rules are clear;
* routing failure log shows repeated task-to-context patterns;
* human approves schema direction.

---

# 11. Audit prompt version traceability later

## Purpose

Check whether current manifest/hash system is enough before adding new version metadata.

## Current state

Startup already has:

```text
STARTUP_PROMPT_REQUEST_KERNEL_MANIFEST.json
```

and generated startup metadata.

## Decision

Do not start a broad prompt-versioning project now.

## Later audit question

Does the manifest allow us to answer:

```text
Which prompt files and hashes were in the startup ZIP when a behavior occurred?
```

If yes, no new version system needed.

If no, add minimal version metadata.

## What not to do

* Do not add version fields everywhere now.
* Do not create a new prompt registry before schema/index normalization.

---

# 12. Do not condense startup kernel now

## Purpose

Avoid destabilizing validated startup behavior.

One audit suggested reducing nine startup files to three. Another audit warned this would recreate monolithic prompt risk.

## Decision

Reject condensation for now.

## Reason

The current startup architecture is validated, modular, and frozen in several related areas.

The problem to solve is not file count.

The problem to solve is:

```text
clear escalation rules
staleness awareness
prompt-call precision
over-requesting control
```

## Allowed later

If evidence shows startup file count causes failures, then consider a simplification patch.

## Not allowed now

* No merge of bootloader and kernel.
* No removal of `paste_after_first_prompts_to_ai.md`.
* No removal of `STARTUP PACK LOAD CHECK`.
* No collapse of routing indexes.

---

# 13. Do not build dispatcher yet

## Purpose

Prevent automated wrong routing.

## Current decision

Postpone:

```text
CLI dispatcher
prompt composer
automatic stack selector
MCP/tool routing layer
auto prompt bundle composition
```

## Resume condition

Only after:

```text
at least 10-20 diverse Phase 2 pilots
>90% prompt-call accuracy
stable conditional context rules
routing failure log reviewed
human approval
```

---

# 14. Do not build Phase 2 JSON validator yet

## Purpose

Avoid freezing expectations before behavior stabilizes.

## Current decision

Postpone:

```text
phase2_prompt_call_expected_outputs.json
phase2_prompt_call_validator.py
batch grading harness
```

## Resume condition

Only after:

* rubric stable;
* conditional context rules stable;
* enough manual pilots;
* failure patterns known;
* expected outputs are no longer changing frequently.

---

# 15. Future schema/index normalization

## Purpose

Return to the older roadmap only after routing logic stabilizes.

## Future files

```text
prompt_schema_vocabulary.md
prompt_schema_vocabulary.json
prompt_navigation_index.json normalization
prompt_conflict_ledger.json
prompt_substitution_map.json
integration_candidate_ledger.json
```

## Not immediate

This remains important, but not before the near-term routing logic corrections.

---

# 16. Recommended implementation order

## Immediate

```text
1. Freeze cooperative_implementation_methodology_v1.
```

## Next routing update package

```text
2. Add routing-index escalation rule.
3. Add startup kernel staleness check.
4. Update Phase 2 rubric with conditional context inclusion.
5. Add Estimated context load field to ROUTING RESPONSE.
```

## Then test

```text
6. Run RG-028 and RG-029.
7. If useful, run RG-030.
8. Record any PARTIAL/FAIL in routing_failure_log.md.
```

## Then decide

```text
9. If pilots pass, freeze routing logic update.
10. If pilots fail, repair only the weak rule.
```

## Later

```text
11. Consider manual pilot registry.
12. Consider Context Package Manifest.
13. Consider resolver map.
14. Consider schema/index normalization.
15. Consider validator.
16. Consider dispatcher.
```

---

# 17. Proposed named patch sequence

## Patch 1

```text
cooperative_implementation_methodology_v1_freeze_patch
```

Purpose:

Freeze the installed validated methodology prompt.

## Patch 2

```text
routing_index_escalation_and_staleness_v1_patch
```

Purpose:

Add index escalation rule and startup kernel staleness warning.

Possible files:

```text
GROUP_ASSIMILATION_INDEX.md
FOLDER_ASSIMILATION_CARDS_INDEX.md
prompt_navigation_index.md
session_start_upload_checklist.md
first_prompts_to_ai.zip
paste_after_first_prompts_to_ai.md if generated
```

## Patch 3

```text
phase2_conditional_context_rubric_v1_patch
```

Purpose:

Update Phase 2 rubric with conditional required context and estimated context load.

Possible file:

```text
phase2_prompt_call_rubric.md
```

Possibly:

```text
ai_prompt_request_canon.md
```

## Patch 4

```text
routing_failure_log_v1_patch
```

Purpose:

Add a lightweight manual failure log.

Possible file:

```text
kanda_prompt_workspace/prompt_library/ROUTING_TESTS/routing_failure_log.md
```

## Patch 5

```text
routing_logic_update_freeze_v1_patch
```

Purpose:

Freeze the accepted routing logic update after validation.

---

# 18. Final next action

The next exact action should be:

```text
Freeze cooperative_implementation_methodology_v1.
```

After that:

```text
Create routing_index_escalation_and_staleness_v1_patch.
```

Do not jump to resolver map, dispatcher, JSON validator, or startup condensation.

---

# 19. Permanent constraints

1. Keep KANDA as a multi-prompt system.
2. Keep startup bootloader small.
3. Keep startup kernel modular.
4. Keep freeze memory project-specific.
5. Keep project_freeze_ledger as reusable engine logic.
6. Keep local freeze workflow as default.
7. Keep AI-send as fallback.
8. Keep proposal-before-code for consequential changes.
9. Keep sandbox pre-delivery validation.
10. Keep root-to-staging ZIP install flow.
11. Keep manual pilots before automation.
12. Keep dispatcher postponed.
13. Keep validator postponed.
14. Keep JSON schema postponed.
15. Keep human confirmation mandatory for governed writes.
