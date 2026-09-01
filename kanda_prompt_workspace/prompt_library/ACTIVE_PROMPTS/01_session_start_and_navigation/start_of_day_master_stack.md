---
prompt_id: start_of_day_master_stack
prompt_code: KPR-01-001
title: Start-of-Day Governance Bridge
version: 2.3
status: active
load_type: always_startup
owner_box: 01_session_start_and_navigation
source_stage: codex-project-governance-bridge-v1
---

# Start-of-Day Governance Bridge

## Mission

Carry the smallest always-loaded governance bridge needed before task-specific routing.

This prompt does not replace the startup upload checklist, current route data, specialist prompts, Brick Wall, exact source, validators, Error Memory, Freeze Memory, or human decisions.

## Startup sequence

1. Read `tell_AI_read_before_all.md` before any startup ZIP content.
2. Load the approved `first_prompts_to_ai.zip` members in source-map order.
3. Keep `prompt_library.zip` available for exact-path retrieval only.
4. Do not accept the real Project task until the second-upload handoff is loaded and the response ends with `WAIT_FOR_TASK`.
5. Classify the task through `KPR-01-014 ai_prompt_request_canon` and locate owners through `KPR-02-004 prompt_navigation_index`.
6. Activate Brick Wall before consequential implementation, mutation, delivery, validation, or freeze work.

## Hard startup bridges

### Codex Project Governance

BEGINNING_OF_DAY_CODEX_PROJECT_GOVERNANCE_BRIDGE_V1_START
CODEX_PROJECT_GOVERNANCE_CANON_V1

For non-Codex AI chats, keep the normal startup and routing behavior.

When the session is running inside Codex, `first_prompt_files` and
`second_prompt_files` are the first KANDA project-governance context after
higher-priority Codex, system, developer, safety, and tool instructions.
Codex must not skip, weaken, reorder, or bypass their read order, readiness
gates, source-truth rules, selected-Project identity, Tool-versus-Project
boundary, validation honesty, freeze confirmation gate, durable-evidence
routing, or Error Memory ownership rules before implementation.

If the startup delivery or selected-Project handoff is missing, stale,
unreadable, or internally conflicting, fail closed and request the exact
missing file, owner prompt, source, or evidence before consequential KANDA
project work.

Use KANDA Reasoner bridge logic to reach exact prompt IDs, prompt paths,
folder cards, and specialist owner prompts whenever deeper task authority is
needed. Prefer already-loaded startup files first. Use `prompt_library.zip`
only for exact-path retrieval of routed prompts that are not already present in
`first_prompts_to_ai.zip`.

BEGINNING_OF_DAY_CODEX_PROJECT_GOVERNANCE_BRIDGE_V1_END

### Code Module Size and Quality

BEGINNING_OF_DAY_CODE_MODULE_SIZE_BRIDGE
BEGINNING_OF_DAY_CODE_MODULE_SIZE_HARD_GATE_V1_START
CODE_MODULE_HARD_MAX_500_LINES
CODE_MODULE_QUALITY_CANON_V1

- Absolute hard maximum code/source module size: 500 physical lines or fewer.
- Every new or touched code/source module must be at most 500 physical lines, including creation, update, modification, refactor, or split.
- Ideal size is 400 lines or fewer.
- PEP 8 compliance is canonical.
- SOLID responsibility and dependency design is canonical.
- DRY implementation is canonical.
- Measure Python physical line counts only after PEP 8-compliant formatting.
- Never remove required blank lines, compress formatting, duplicate logic, or weaken names to fit the limit.
- If the limit would be exceeded, create as many cohesive helper modules as needed and route to `large_module_refactor_protocol.md`.
- Every helper must follow the same quality and line-count rules.
- Do not create, keep, enlarge, or deliver a touched code/source module above the maximum.

BEGINNING_OF_DAY_CODE_MODULE_SIZE_HARD_GATE_V1_END

### Box Logic

BEGINNING_OF_DAY_BOX_LOGIC_BRIDGE
BEGINNING_OF_DAY_BOX_LOGIC_SHIELD_V1_START
BOX_LOGIC_STARTUP_SHIELD

This is mandatory beginning-of-day context. For consequential work, identify the active box, canonical owner paths, allowed files, out-of-scope files, cross-box touches, public contracts, validation scope, and boundary risks before implementation or delivery.

Keep code and responsibility inside the owning box.
Do not let code, imports, mutable state, UI logic, domain logic, generated evidence, or project data leak across private boundaries.
Route uncertain boundary work to `box_architecture_canon.md` before implementation or delivery.

BEGINNING_OF_DAY_BOX_LOGIC_SHIELD_V1_END

### Class 04 Architecture Owner Dispatch

BEGINNING_OF_DAY_GOVERNED_ARCHITECTURE_COMPANION_BRIDGE_V1_START
Class 04 Architecture Owner Dispatch Bridge

Brick Wall remains the final coding-authorization owner.
Do not load the retired compiled architecture companion.
Route to the smallest current set of `box_architecture_canon`, `boundary_first_repair_protocol`, `kanda_box_shielding_canon`, `project_folder_organization_canon`, and `stateful_control_regression_canon`.

BEGINNING_OF_DAY_GOVERNED_ARCHITECTURE_COMPANION_BRIDGE_V1_END

### Terminal Cleanup

BEGINNING_OF_DAY_TERMINAL_CLEANUP_CONTRACT_BRIDGE_V1_START
TERMINAL_CLEANUP_CONTRACT_STARTUP_BRIDGE

Route every user-facing terminal block through `KPR-05-007 terminal_cleanup_contract` and `pre_output_contract_gates`. Begin long interactive blocks at a clean `PS ...>` prompt; if `>>` is visible, require Ctrl+C first.
Install success asks for Enter, asks for Enter again, then uses one final `Clear-Host`; automatic timed clearing is not allowed.
Validation, freeze, errors, diagnostics, recovery, and other interactive terminal flows use the same Enter, Enter, one-final-`Clear-Host` sequence.
Never close the terminal. Noninteractive automation uses exit codes and captured output instead of Read-Host or Clear-Host.
Every user-facing PowerShell code fence must be one independent paste unit. Prefer direct packaged-script invocation; do not use user-facing `else`, `elseif`, or `finally`, do not detach `catch`, and keep APIs compatible with the declared PowerShell runtime.

BEGINNING_OF_DAY_TERMINAL_CLEANUP_CONTRACT_BRIDGE_V1_END

### Durable documentation and evidence

BEGINNING_OF_DAY_DURABLE_DOCUMENT_ROUTING_BRIDGE_V1_START
DURABLE_DOCUMENT_ARTIFACT_ROUTING_CANON_V1
DURABLE_VALIDATION_EVIDENCE_OWNER_V1

Daily-work is transient.
Generated project-specific `.txt`, `.md`, reports, receipts, and successful validation evidence that must survive the session belong under the selected Project support root, including `project_validation_evidence\<feature_id>` when applicable.
Canonical source documentation remains in its source owner.
If ownership, sensitivity, redaction, purpose, lifetime, or authority is unresolved: `DURABLE DOCUMENT ROUTING BLOCKED`.

BEGINNING_OF_DAY_DURABLE_DOCUMENT_ROUTING_BRIDGE_V1_END

### Runtime Evidence Escalation

BEGINNING_OF_DAY_RUNTIME_EVIDENCE_ESCALATION_BRIDGE_V1_START
RUNTIME_EVIDENCE_ESCALATION_BRIDGE_V1

When a conclusion depends on actual runtime behavior that exact source and current execution tests cannot prove, route through `KPR-01-014 ai_prompt_request_canon` and request the smallest scenario-specific runtime evidence package.

This applies especially to signal or callback order, workers and threads, cancellation, stale results, timing or races, GUI state transitions, subprocess or filesystem side effects, environment-dependent branches, intermittent defects, and performance.

Do not over-request runtime evidence for purely structural, documentary, syntactic, or source-sufficient questions. Prefer existing current tests, traces, logs, and validation before requesting a new capture. Static-only conclusions remain labeled as inference and must not be presented as execution-verified.

BEGINNING_OF_DAY_RUNTIME_EVIDENCE_ESCALATION_BRIDGE_V1_END

## Readiness boundary

Normal startup has two separate checkpoints:

- `STARTUP PACK LOAD CHECK`: startup pack loaded; wait for second upload.
- `PROJECT READY CHECK`: selected Project handoff loaded and Tool Error Memory context status reported; may end with `WAIT_FOR_TASK`.

Neither checkpoint authorizes coding. Brick Wall and task-specific evidence determine authorization.

## No-growth rule

Reuse, repair, simplify, consolidate, or strengthen existing owners before proposing a new prompt, registry, context engine, routing system, or coordination layer.
