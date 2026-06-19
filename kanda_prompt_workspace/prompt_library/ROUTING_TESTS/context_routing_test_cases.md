# Context Routing Test Cases - Phase 3

Status: audit candidate
Patch: kanda_context_routing_layer_phase3_routing_tests_v1
Owner box: Routing Test Box

Purpose: validate the Context Routing Layer without touching the live app. These cases test whether human requests route to the correct group bundles, whether Fast Path prevents over-asking, and whether implementation tasks request the required prompts before work begins.

Rules:
- These are routing tests, not behavioral prompts.
- Do not load all prompt folders by default.
- Simple explanation or brainstorming may use Fast Path.
- Implementation, governance, freeze, and prompt-audit tasks must request the correct specialist context.
- Missing required context produces HARD_STOP or STEP_PAUSE.

## Test cases

### T001_START_DAY

Input: Start the working day and prepare context.

Expected intent: START_DAY

Required groups:
- 01_session_start_and_navigation
- 02_prompt_routing_and_indexing

Optional groups:
- 03_governance_freeze_and_handoff

Missing behavior: STEP_PAUSE
Fast path allowed: false
Expected AI action: Ask for active overlay, latest handoff if continuing work, and task description.

### T002_EXPLAIN_PROMPT

Input: Explain what this prompt does.

Expected intent: EXPLAIN_OR_READ

Required groups:
- 02_prompt_routing_and_indexing

Optional groups:
- none

Missing behavior: DEGRADED_WARNING
Fast path allowed: true
Expected AI action: Proceed with explanation using provided context; do not over-request specialist prompts.

### T003_CREATE_CODE_PATCH

Input: Create a new feature in the app.

Expected intent: CREATE_OR_UPDATE_CODE

Required groups:
- 04_box_architecture_and_boundaries
- 05_patch_delivery_and_validation
- 08_python_engineering_core

Optional groups:
- 09_python_quality_security_observability

Missing behavior: HARD_STOP
Fast path allowed: false
Expected AI action: Request Box Architecture, delivery, and validation prompts before implementation.

### T004_LARGE_MODULE_REFACTOR

Input: This Python file has more than 500 lines. Refactor it safely.

Expected intent: LARGE_MODULE_REFACTOR

Required groups:
- 04_box_architecture_and_boundaries
- 05_patch_delivery_and_validation
- 06_refactor_and_architecture_hardening

Optional groups:
- 08_python_engineering_core

Missing behavior: HARD_STOP
Fast path allowed: false
Expected AI action: Request large-module refactor protocol before touching the file.

### T005_FREEZE_AFTER_VALIDATION

Input: Validation passed. Freeze this step.

Expected intent: FREEZE_REVIEW

Required groups:
- 03_governance_freeze_and_handoff
- 05_patch_delivery_and_validation

Optional groups:
- 02_prompt_routing_and_indexing

Missing behavior: STEP_PAUSE
Fast path allowed: false
Expected AI action: Review validation evidence; freeze only if output is complete and clean.

### T006_PROMPT_AUDIT

Input: Audit this prompt and decide if it is updated, deprecated, or split.

Expected intent: PROMPT_AUDIT

Required groups:
- 02_prompt_routing_and_indexing
- 07_prompt_authoring_and_audit

Optional groups:
- 03_governance_freeze_and_handoff

Missing behavior: STEP_PAUSE
Fast path allowed: false
Expected AI action: Request related previously audited prompt files before final overlap decisions.

### T007_GOVERNANCE_UPDATE

Input: Update governance after a validated freeze.

Expected intent: GOVERNANCE_UPDATE

Required groups:
- 03_governance_freeze_and_handoff
- 05_patch_delivery_and_validation

Optional groups:
- 02_prompt_routing_and_indexing

Missing behavior: HARD_STOP
Fast path allowed: false
Expected AI action: Do not update governance without validation evidence and the relevant governance prompt.

### T008_PRODUCTIZATION_REVIEW

Input: Check whether this project is ready for release.

Expected intent: PRODUCTIZATION_READINESS

Required groups:
- 11_productization_and_release_readiness

Optional groups:
- 09_python_quality_security_observability
- 10_python_api_data_async_config

Missing behavior: STEP_PAUSE
Fast path allowed: false
Expected AI action: Route to productization readiness prompts before giving release advice.

### T009_BRAINSTORM_ARCHITECTURE

Input: Brainstorm architecture options only; do not implement.

Expected intent: ARCHITECTURE_DISCUSSION

Required groups:
- 04_box_architecture_and_boundaries

Optional groups:
- 12_generalized_project_canons

Missing behavior: DEGRADED_WARNING
Fast path allowed: true
Expected AI action: Discuss options; do not request delivery prompts unless implementation begins.

### T010_FIX_IMPORT_ERROR

Input: Fix this Python import error.

Expected intent: BUG_FIX_CODE

Required groups:
- 05_patch_delivery_and_validation
- 08_python_engineering_core

Optional groups:
- 04_box_architecture_and_boundaries
- 09_python_quality_security_observability

Missing behavior: STEP_PAUSE
Fast path allowed: false
Expected AI action: Request source files and traceback; identify owner box before patching.

