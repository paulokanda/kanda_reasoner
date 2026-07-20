# KANDA Context Routing Layer - Manual Use Tutorial

## 1. What this box is

The `prompt_library` folder is an engineered prompt-orchestration box.

It is not a live app integration.
It is not a dispatcher.
It is not a GUI feature.
It is not an automatic prompt loader.

It is a manual context-routing system that helps the human and AI decide:

- which prompt group is relevant;
- which folder card should be loaded;
- which specialist prompt is required;
- whether the task can proceed with a fast path;
- whether the AI must stop and request more context before implementation.

The purpose is to use many useful prompts without loading all of them at once.

## 2. Main mental model

Think of the system as a hospital triage desk.

The human brings a task:

- "Create a feature"
- "Refactor a large file"
- "Audit this prompt"
- "Freeze this step"
- "Explain this prompt"

The routing layer asks:

- What kind of task is this?
- Which prompt group owns it?
- Which specialist prompt is mandatory?
- Which prompt is optional?
- Can we proceed now?
- Must we stop and ask for missing files?

The routing layer does not replace the specialist prompts.
It only tells the AI which specialist prompts to request.

## 3. The three context tiers

### Tier 0 - Start-of-day kernel

Load these at the beginning of a workday or a new serious session:

1. `ACTIVE_PROMPTS/01_session_start_and_navigation/start_of_day_master_stack.md`
2. `ACTIVE_PROMPTS/01_session_start_and_navigation/ai_prompt_request_canon.md`
3. `ACTIVE_PROMPTS/02_prompt_routing_and_indexing/prompt_navigation_index.md`
4. `ROUTING/GROUP_ASSIMILATION_INDEX.md`

Optional but useful:

5. `ROUTING/FOLDER_ASSIMILATION_CARDS_INDEX.md`
6. Latest handoff, if continuing previous work.
7. Active project overlay, if working inside a concrete project.

### Tier 1 - Folder assimilation card

After the AI classifies the task, load only the selected folder card(s), such as:

- `ACTIVE_PROMPTS/04_box_architecture_and_boundaries/_FOLDER_ASSIMILATION.md`
- `ACTIVE_PROMPTS/05_patch_delivery_and_validation/_FOLDER_ASSIMILATION.md`
- `ACTIVE_PROMPTS/07_prompt_authoring_and_audit/_FOLDER_ASSIMILATION.md`

These cards are not the full rules.
They are short maps that say what the folder is for.

### Tier 2 - Specialist prompts

After reading the folder card, load the exact specialist prompt(s), such as:

- `box_architecture_canon.md`
- `implementation_and_delivery_protocol.md`
- `implementation_and_delivery_protocol.md`
- `large_module_refactor_protocol.md`
- `prompt_audit_canon.md`
- `python_clean_code.md`
- `python_testing_pytest.md`

Only load them when required by the task.

## 4. Recommended beginning-of-day prompt

Paste this into a new chat together with the Tier 0 files:

```text
START_DAY

I am using the KANDA Context Routing Layer manually.
This is not live app integration.
Do not assume all prompts are loaded.
Do not implement yet.

Loaded context:
1. start_of_day_master_stack.md
2. ai_prompt_request_canon.md
3. prompt_navigation_index.md
4. GROUP_ASSIMILATION_INDEX.md

Your job:
- classify my task intent;
- tell me required prompt groups;
- tell me optional prompt groups;
- tell me which folder assimilation cards to load;
- tell me which specialist prompts are required;
- tell me whether this is HARD_STOP, STEP_PAUSE, or DEGRADED_WARNING;
- do not proceed with implementation until required prompts are loaded.

My task:
[write task here]
```

## 5. How to respond when the AI asks for prompts

The AI should answer in this style:

```text
For this task, I need these prompt files before implementation:

Required:
1. box_architecture_canon.md - because ownership and boundaries may change.
2. implementation_and_delivery_protocol.md - because files will be created or modified.
3. implementation_and_delivery_protocol.md - because delivery and validation are required.

Recommended:
1. python_testing_pytest.md - because tests may be needed.

Missing behavior:
HARD_STOP before implementation.

Please upload these prompts or confirm they are already loaded.
```

Then you upload/paste the requested files.

After that, tell the AI:

```text
The requested prompts are now loaded.
Proceed with the next step only.
```

## 6. Missing behavior meanings

### HARD_STOP

The AI must not proceed without the required prompt.

Example:

- implementing code without delivery/validation protocol;
- refactoring a large file without large-module refactor protocol;
- changing architecture without box architecture canon.

### STEP_PAUSE

The AI can discuss the task, but must pause before a specific risky step.

Example:

- can summarize validation output, but cannot freeze until all evidence is present;
- can inspect a prompt, but cannot make final overlap decision without related prompt file.

### DEGRADED_WARNING

The AI can proceed, but must warn that confidence is lower.

Example:

- explaining a prompt with only partial context;
- brainstorming architecture without full implementation stack.

## 7. What not to do

Do not load all 12 prompt folders at the beginning.

Do not paste the entire prompt library into every chat.

Do not treat folder cards as the full prompt.

Do not allow the AI to implement from memory when a specialist prompt is required.

Do not update the live app just because the prompt box is frozen.

Do not mark unaudited prompts as active routes.

## 8. Manual routing test mode

Use this exact instruction when you want to test whether the logic is working:

```text
ROUTING_TEST_MODE

Do not solve the task.
Only classify routing.

For the task below, return:

task_intent:
fast_path_allowed:
required_groups:
optional_groups:
folder_cards_to_load:
specialist_prompts_needed:
minimum_viable_context:
missing_behavior:
should_AI_stop_before_implementation:
NEED_message_to_human:
confidence:
```

Then give one of the test tasks below.

## 9. Core test situations

### Test 1 - Start day

```text
Start the working day and prepare context.
```

Expected:

- intent: START_DAY
- required groups: 01_session_start_and_navigation, 02_prompt_routing_and_indexing
- minimum context: start_of_day_master_stack, ai_prompt_request_canon, prompt_navigation_index, GROUP_ASSIMILATION_INDEX
- missing behavior: STEP_PAUSE

### Test 2 - Simple explanation

```text
Explain what this prompt does.
```

Expected:

- intent: EXPLAIN_OR_READ
- fast path allowed: true
- required group: 02_prompt_routing_and_indexing
- no implementation stack required
- do not over-request specialist prompts

### Test 3 - Create code

```text
Create a new feature in the app.
```

Expected:

- intent: CREATE_OR_UPDATE_CODE
- required groups: 04_box_architecture_and_boundaries, 05_patch_delivery_and_validation, 08_python_engineering_core
- optional group: 09_python_quality_security_observability
- missing behavior: HARD_STOP
- required specialist prompts usually include box architecture, delivery, validation, and relevant Python engineering prompts

### Test 4 - Large module refactor

```text
This Python file has more than 500 lines. Refactor it safely.
```

Expected:

- intent: LARGE_MODULE_REFACTOR
- required groups: 04_box_architecture_and_boundaries, 05_patch_delivery_and_validation, 06_refactor_and_architecture_hardening
- optional group: 08_python_engineering_core
- missing behavior: HARD_STOP
- AI must request large_module_refactor_protocol before touching the file

### Test 5 - Freeze after validation

```text
Validation passed. Freeze this step.
```

Expected:

- intent: FREEZE_REVIEW
- required groups: 03_governance_freeze_and_handoff, 05_patch_delivery_and_validation
- missing behavior: STEP_PAUSE
- AI must inspect validation output before freezing

### Test 6 - Prompt audit

```text
Audit this prompt and decide if it is updated, deprecated, or split.
```

Expected:

- intent: PROMPT_AUDIT
- required groups: 02_prompt_routing_and_indexing, 07_prompt_authoring_and_audit
- missing behavior: STEP_PAUSE
- AI must request related previously audited prompts before final overlap decision

### Test 7 - Governance update

```text
Update governance after a validated freeze.
```

Expected:

- intent: GOVERNANCE_UPDATE
- required groups: 03_governance_freeze_and_handoff, 05_patch_delivery_and_validation
- missing behavior: HARD_STOP
- AI must not update governance without validation evidence

### Test 8 - Productization review

```text
Check whether this project is ready for release.
```

Expected:

- intent: PRODUCTIZATION_READINESS
- required group: 11_productization_and_release_readiness
- optional groups: 09_python_quality_security_observability, 10_python_api_data_async_config
- missing behavior: STEP_PAUSE

### Test 9 - Architecture brainstorming only

```text
Brainstorm architecture options only; do not implement.
```

Expected:

- intent: ARCHITECTURE_DISCUSSION
- required group: 04_box_architecture_and_boundaries
- optional group: 12_generalized_project_canons
- fast path allowed: true
- do not request delivery prompts unless implementation begins

### Test 10 - Import error

```text
Fix this Python import error.
```

Expected:

- intent: BUG_FIX_CODE
- required groups: 05_patch_delivery_and_validation, 08_python_engineering_core
- optional groups: 04_box_architecture_and_boundaries, 09_python_quality_security_observability
- minimum context: delivery protocol, validation protocol, relevant source files, traceback
- missing behavior: STEP_PAUSE

## 10. How to judge whether the routing logic works

A test passes if the AI:

1. does not solve the task during routing test mode;
2. classifies the intent correctly;
3. asks for the correct group cards;
4. asks for the correct specialist prompts;
5. uses fast path for simple explanation;
6. does not over-request all 12 folders;
7. hard-stops before code implementation when required prompts are missing;
8. requests validation evidence before freeze;
9. requests related prompt files before final prompt-audit overlap decisions;
10. explains why each requested prompt is needed.

A test fails if the AI:

- begins implementation before asking for required prompts;
- says "I can do it from memory" for a governed task;
- loads all 12 folders by default;
- treats folder cards as full protocols;
- freezes without validation evidence;
- marks unaudited prompts as active;
- edits unrelated prompt logic during an audit.

## 11. Human workflow for real work

### Step A - Start

Load Tier 0 files.

### Step B - State the task

Say what you want, but add:

```text
Before implementation, route this task and tell me which prompts you need.
```

### Step C - AI requests prompts

The AI should tell you required groups, folder cards, and specialist prompts.

### Step D - You load only those prompts

Upload or paste the requested files.

### Step E - AI works only inside the selected scope

For code work, the AI must still follow install + validation workflow.
For prompt-audit Markdown placement, only file-placement verification may be enough.

### Step F - Validate

For code, validation output is mandatory.
For prompt routing tests, compare expected vs actual routing.

## 12. Prompt audit usage

For prompt audit tasks, load:

Tier 0 files:
- start_of_day_master_stack.md
- ai_prompt_request_canon.md
- prompt_navigation_index.md
- GROUP_ASSIMILATION_INDEX.md

Then add:
- ACTIVE_PROMPTS/07_prompt_authoring_and_audit/_FOLDER_ASSIMILATION.md
- ACTIVE_PROMPTS/07_prompt_authoring_and_audit/prompt_audit_canon.md
- ACTIVE_PROMPTS/07_prompt_authoring_and_audit/prompt_canon_reconciliation_protocol.md when overlap/conflict/reconciliation is involved
- ACTIVE_PROMPTS/02_prompt_routing_and_indexing/prompt_substitution_map.md when deprecation or replacement is involved

Important audit rule:

The index can tell us where to look, but the actual prompt file proves what is inside.
No related prompt file means no final overlap decision.

## 13. How the map grows

The Prompt Navigation Index should grow only after prompt audit decisions.

Good update triggers:

- prompt audited and accepted;
- prompt deprecated;
- prompt split;
- prompt converted to project overlay;
- route changed;
- integration candidate created.

Bad update triggers:

- random discussion;
- unreviewed idea;
- unresolved conflict;
- AI assumption that a prompt exists.

## 14. Practical daily checklist

At the start of a serious work session, ask:

1. Did I load the Tier 0 files?
2. Did I provide the active project overlay or task context?
3. Did I ask the AI to route before implementation?
4. Did the AI identify required groups?
5. Did the AI request folder cards before specialist prompts?
6. Did the AI avoid loading all 12 groups?
7. Did the AI use HARD_STOP for implementation without required prompts?
8. Did the AI use Fast Path for simple explanation?
9. Did the AI preserve validation evidence when validation is required?
10. Did the AI avoid live app integration unless explicitly requested?

## 15. One-page quick-start version

Load these first:

- `start_of_day_master_stack.md`
- `ai_prompt_request_canon.md`
- `prompt_navigation_index.md`
- `GROUP_ASSIMILATION_INDEX.md`

Then say:

```text
I am using this prompt box manually.
Route my task before doing it.
Tell me required groups, folder cards, specialist prompts, missing behavior, and whether you must stop before implementation.

Task:
[my task]
```

Then load only what the AI asks for.

That is the core use pattern.
