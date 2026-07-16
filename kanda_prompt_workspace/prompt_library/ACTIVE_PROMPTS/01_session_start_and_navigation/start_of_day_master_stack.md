# Start-of-Day Master Stack

Version: 1.0
Status: active_candidate
Scope: KANDA Context Routing Layer - Phase 1 kernel
Owner box: Context Routing Kernel Box
Last updated: 2026-06-12

## Purpose

This file defines the smallest safe daily startup stack for the prompt library.
It is a bootstrap router, not a master prompt.
It prevents loading the full prompt library at session start.

## What this file does not do

- It does not replace specialist prompts.
- It does not replace specialist implementation rules.
- It does not replace specialist validation rules.
- It carries only short startup bridges for high-risk invariants.
- It does not create folder assimilation cards.
- It does not integrate with the live app.
- It does not touch kanda_reasoner_app or Tab Prompt Library GUI.

## Box Logic Startup Bridge

BEGINNING_OF_DAY_BOX_LOGIC_BRIDGE: This bridge is mandatory beginning-of-day
context. Startup load/readiness reporting must make clear that the Box Logic
shield is available from the start of the session, without loading the full Box
Architecture canon unless a task actually needs it.

BEGINNING_OF_DAY_BOX_LOGIC_SHIELD_V1_START
BOX_LOGIC_STARTUP_SHIELD: This is a startup-visible hard gate for all
KANDA/PyArchitect implementation, repair, refactor, prompt update, governance
update, bundle, GUI, validation, freeze, patch, and artifact-delivery work. The
AI must carry this rule at the beginning of every chat and apply it before
planning, changing, validating, or delivering project files.

Mandatory summarized box-boundary rule:

- Identify the active box before implementation or file changes.
- State owner paths when work touches code, prompt, governance, validation,
  startup, GUI, freeze, or artifact-delivery behavior.
- State files allowed to change.
- State files explicitly out of scope.
- Declare cross-box touches before touching more than one box.
- Keep code and responsibility inside the owning box.
- Do not let code, imports, mutable state, UI logic, domain logic, prompt logic,
  validation logic, governance logic, freeze logic, or delivery logic leak from
  one box into another.
- Preserve public contracts between boxes and avoid private reach-in.
- Validate the active box and any touched external box.
- Do not proceed from memory when box ownership, owner paths, public contracts,
  or allowed supporting touches are unclear; inspect the needed source, prompt,
  manifest, or validation context first.
- If boundary risk, cross-box leakage, public-contract risk, mutable-state
  ownership risk, or box-responsibility confusion exists, route to
  `box_architecture_canon.md` before implementation or delivery.
- If the visible symptom may be downstream of another owner, shared host, handoff,
  persistence owner, root decision, or async lifecycle, route to
  `boundary_first_repair_protocol.md` before editing the symptomatic box.

This bridge is only the startup enforcement layer. It does not replace the full
Box Architecture canon. When a task involves implementation, repair, refactor,
prompt update, governance update, bundle creation, GUI ownership, public
contracts, cross-box behavior, mutable-state ownership, or architecture-boundary
risk, route to `box_architecture_canon.md` before doing the risky step.
When symptom location and defect ownership may diverge, route additionally to
`boundary_first_repair_protocol.md`; keep it routed/on-demand rather than
loading the full specialist prompt at startup.

Do not load the full Box Architecture prompt during normal startup unless the
current task requires it.
BEGINNING_OF_DAY_BOX_LOGIC_SHIELD_V1_END


## No-Leak Logic Bridge

BEGINNING_OF_DAY_NO_LEAK_LOGIC_BRIDGE: This bridge is mandatory
beginning-of-day context. Startup load/readiness reporting must make clear
that NO_LEAK_LOGIC_V1 is available from the start of the session, without
loading the full Box Architecture canon unless a task actually needs it.

BEGINNING_OF_DAY_NO_LEAK_LOGIC_V1_START
NO_LEAK_LOGIC_V1: This is a startup-visible hard gate inside Box Logic and
Box Shielding. It prevents ownership, path, state, contract, evidence, and
responsibility from leaking across boxes.

Mandatory summarized no-leak rule:

- Classify every touched item before mutation as tool-owned logic,
  active-project source, project-specific support state, generated/evidence
  artifact, transient garbage artifact, external box dependency, or
  out-of-scope file.
- Prevent wrong-root writes, especially project-specific state written to a
  hardcoded KANDA Reasoner root or reusable tool code written into an
  active-project support/output path.
- Prevent tool/project leakage: reusable engines, GUI tabs, analyzers,
  planners, validators, prompt routing, patch delivery, startup delivery,
  freeze tooling, and source maps are tool-owned; concrete generated or
  refactored files for the selected active project are project-owned.
- Prevent cross-box leakage, private reach-in, public API ownership leakage,
  hidden mutable-state leakage, generated-artifact-as-source leakage, and
  validation/freeze/Error Memory evidence leakage.
- If no-leak risk exists, output `NO-LEAK CHECK` before implementation or
  delivery.
- If ownership, root, box, public contract, generated/source status, or
  freeze/validation location is unclear, inspect the needed source, prompt,
  manifest, or validation context before writing.

This bridge is only the startup enforcement layer. It does not replace the
full Box Architecture, Box Shielding, or Project Tool Boundary canons.
BEGINNING_OF_DAY_NO_LEAK_LOGIC_V1_END

## Governed Architecture Companion Startup Bridge

BEGINNING_OF_DAY_GOVERNED_ARCHITECTURE_COMPANION_BRIDGE_V1_START
GOVERNED_ARCHITECTURE_COMPANION_STARTUP_BRIDGE: For governed KANDA code,
patch, prompt-library, startup, GUI, workflow, persistence, validation, freeze,
Error Memory, refactor, or durable-support work, carry these rules from the
start of the session:

- Brick Wall remains the final coding-authorization owner.
- Resolve Tool-versus-Project identity, the primary box, public contract,
  mutable-state owner, and NO_LEAK classification before writing.
- Use exact current source, current validators, compact Error Memory, and
  current freeze context; generated handoffs and ZIPs are not source truth.
- Load MCard only for its canonical Architecture Review/Planner/Workbench/
  transaction/eject triggers.
- Load Shield Logic only when a meaningful milestone or authority/boundary risk
  requires a tests-first shield.
- Route to `governed_architecture_companion_handoff` on demand when the task is
  architecture-sensitive, self-hosting, cross-box, lifecycle-heavy, or needs
  the unified architecture gate.
- The full companion is non-canonical and must never replace its current
  canonical prompt owners.

Do not load the full companion during normal startup.
BEGINNING_OF_DAY_GOVERNED_ARCHITECTURE_COMPANION_BRIDGE_V1_END

## Durable Documentation Artifact Routing Bridge

BEGINNING_OF_DAY_DURABLE_DOCUMENT_ROUTING_BRIDGE: This bridge is mandatory
beginning-of-day context. Startup load/readiness reporting must make clear that
daily-work is disposable and that important generated documentation and
validation evidence belong to the selected Active Project support root.

BEGINNING_OF_DAY_DURABLE_DOCUMENT_ROUTING_BRIDGE_V1_START
DURABLE_DOCUMENT_ARTIFACT_ROUTING_CANON_V1: `<project>_delete_after_daily_work`
is transient garbage/staging only. It must never be the sole owner of important
project documentation, validation evidence, handoffs, reports, receipts, or
other generated documentary artifacts needed after the session.

Mandatory summarized durable-document rule:

- Derive the durable sibling support root from the selected Active Project:
  `<project_drive>\<project_name>_show_project_to_AI\`.
- Generated project-specific `.txt`, `.md`, and similar documentary artifacts
  default to durable Project Support unless explicitly classified as transient.
- Canonical source documentation remains in its Tool or Project source owner;
  do not move repository source docs merely because they use `.txt` or `.md`.
- Validation evidence is durable. A temporary operational copy may exist in
  `_delete_after_daily_work`, but successful evidence must also be persisted to
  `<project>_show_project_to_AI\project_validation_evidence\<feature_id>\`.
- Existing specialized owners such as `project_error_memory`,
  `project_freeze_after_update`, `large_file_refactor_workbench`,
  `first_prompt_files`, and `second_prompt_files` take precedence over the
  general `project_documentation` folder.
- Never hardcode `kanda_reasoner_show_project_to_AI` when another Active Project
  is selected.
- If durable ownership cannot be resolved, fail closed with
  `DURABLE DOCUMENT ROUTING BLOCKED`.

The full canonical owner is `durable_document_artifact_routing_canon.md`.
DURABLE_VALIDATION_EVIDENCE_OWNER_V1: Daily-work evidence may support the live
operation, but freeze, handoff, and next-session reasoning must not depend on a
daily-work-only copy.
BEGINNING_OF_DAY_DURABLE_DOCUMENT_ROUTING_BRIDGE_V1_END

## Code Module Size Bridge

BEGINNING_OF_DAY_CODE_MODULE_SIZE_BRIDGE: This bridge is mandatory
beginning-of-day context. Startup load/readiness reporting must make clear that
the module-size guardrail is available from the start of the session, without
loading the full large-module protocol unless a task actually needs it.

BEGINNING_OF_DAY_CODE_MODULE_SIZE_HARD_GATE_V1_START
CODE_MODULE_HARD_MAX_500_LINES: This is a startup-visible hard gate for all
KANDA/PyArchitect code creation, updates, modifications, refactors, and splits.
The AI must carry this rule at the beginning of every chat and apply it before
writing, changing, refactoring, or delivering code modules.

Mandatory summarized line-count and quality rule:

CODE_MODULE_QUALITY_CANON_V1: For Python source, PEP 8 compliance, SOLID responsibility and dependency design, and DRY implementation are canonical. The line-count law must be satisfied through cohesive architecture, never through degraded formatting or duplicated logic.

- Ideal code/source module size: 400 physical lines or fewer.
- Absolute hard maximum code/source module size: 500 physical lines or fewer.
- Measure Python physical line counts only after PEP 8-compliant formatting has
  been applied or verified.
- Never remove required blank lines, collapse imports or declarations, combine
  statements, compress class or function layout, or otherwise violate PEP 8 to
  keep a module at or below the line-count maximum.
- Apply SOLID and DRY when assigning module responsibilities, public seams, and
  dependency direction. Do not duplicate logic merely to avoid creating a
  helper, and do not create meaningless wrappers or micro-modules merely to hit
  a line target.
- If PEP 8-compliant, SOLID, and DRY code would exceed 500 physical lines, keep
  the compliant formatting and create as many cohesive helper modules as needed.
  Every helper must follow the same quality and line-count rules.
- Every new or touched code/source module must be at most 500 physical lines
  after the change, including creation, update, modification, refactor, or
  split work.
- Do not create, keep, enlarge, or deliver a touched code/source module above
  500 physical lines as normal implementation work.
- If the requested work would create or preserve an over-limit touched module,
  route to `large_module_refactor_protocol.md`, split by cohesive ownership,
  and validate line counts before patch delivery.
- If a module would exceed the 500-line hard maximum, the AI may and should
  create as many cohesive helper, auxiliary, derived, adapter, or complementary
  code/source modules as needed, as long as every created or touched module also
  follows this bridge.
- Every helper module must have a clear responsibility, must stay at or below
  500 physical lines, should target 400 physical lines or fewer, and should not
  be below roughly 100 substantive lines unless a documented exception applies
  such as a facade/re-export shim, package marker, constants module, validation
  helper, optional dependency adapter, circular-dependency breaker, stable seam,
  or another cohesive boundary.
- Split by responsibility, dependency direction, public API boundary,
  side-effect isolation, validation boundary, or no-leak ownership boundary; do
  not split by arbitrary line ranges or create micro-files only to satisfy a
  line-count target.
- For Python work, check physical line counts for every touched `.py` file
  whenever source files are available before patch delivery.
- This rule applies to code/source modules, especially `.py` files and other
  implementation files.
- This rule does not apply to plain text, Markdown, documentation, prompt,
  manifest, JSON, log, report, or other non-code content files when their
  purpose requires larger content.

If a task needs the full methodology, route to `large_module_refactor_protocol.md`;
do not load the full prompt during normal startup unless needed.
BEGINNING_OF_DAY_CODE_MODULE_SIZE_HARD_GATE_V1_END

## Terminal Cleanup Bridge

BEGINNING_OF_DAY_TERMINAL_CLEANUP_BRIDGE: This bridge is mandatory
beginning-of-day context. Startup load/readiness reporting must make clear that
terminal cleanup behavior is available from the start of the session, because it
applies to install, validation, freeze, recovery, error, diagnostic, and other
terminal blocks.

The canonical owner prompt is `terminal_cleanup_contract.md`. This startup bridge
is the beginning-of-day visible summary of that contract so the AI can apply the
rule before loading specialist output prompts.

BEGINNING_OF_DAY_TERMINAL_CLEANUP_CONTRACT_BRIDGE_V1_START
TERMINAL_CLEANUP_CONTRACT_STARTUP_BRIDGE: Before writing any Windows 11
PowerShell terminal block, classify it as install success or non-install-success.

Mandatory startup-visible terminal cleanup rule:

- Install success only: show `INSTALL OK. Terminal will clear in 2 seconds...`,
  wait about 2 seconds, run one `Clear-Host`, keep the terminal open, and do not
  ask for Enter.
- Install errors, validation, freeze, recovery, diagnostics, validation errors,
  freeze errors, and every other non-install-success terminal block: show all
  relevant output, ask for Enter, ask for Enter again, run one final
  `Clear-Host`, and keep the terminal open.
- Never close the terminal from install, validation, freeze, recovery,
  diagnostic, or error blocks.
- Never mix the install-success 2-second footer with the Enter, Enter footer.
- Never auto-clear validation, freeze, diagnostic, recovery, or error output
  after a timer.
- Install blocks must include a fail-safe error path so install errors cannot
  bypass the Enter, Enter, `Clear-Host` cleanup.
- Freeze-prep, validation-evidence merge, recovery, and repair commands must not
  use inline `python -c`; write and run a temporary UTF-8 `.py` helper under the
  transient `_delete_after_daily_work` garbage folder named from the selected project slug.

This bridge does not replace `terminal_cleanup_contract.md`; it makes the
contract visible at startup. When producing an install, validation, freeze,
recovery, diagnostic, or error command, apply `terminal_cleanup_contract.md` and
`pre_output_contract_gates.md` before output.
BEGINNING_OF_DAY_TERMINAL_CLEANUP_CONTRACT_BRIDGE_V1_END

## Tier model

### Tier 0 - Session kernel

Load at the beginning of the day or session:

1. start_of_day_master_stack
2. session_start_upload_checklist
3. ai_prompt_request_canon
4. prompt_navigation_index

Optional if continuing previous work:

5. latest handoff or checkpoint
6. current task description
7. current source/evidence ZIP when implementation is requested

### Tier 1 - Group routing

Load only after task intent is known:

1. GROUP_ASSIMILATION_INDEX.md
2. selected group metadata from group_assimilation_index.json
3. selected folder assimilation card only after Phase 2 creates it

Phase 1 rule: do not require all 12 folder cards.

### Tier 2 - Specialist prompt payload

Load only before real work:

- exact task prompt(s)
- box_architecture_canon when implementation, architecture, refactor, or ownership boundaries are involved
- bundle_gated_development_workflow or delivery/validation prompt when code, files, ZIPs, install, validation, or freeze are involved
- prompt_audit_canon when auditing prompt files
- governance/freeze prompt only when validation evidence exists or freeze/governance is explicitly requested

## Fast Path

If the user asks for explanation, discussion, brainstorming, or reading only, proceed with loaded context.
Do not block by requesting specialist prompts unless the answer would change files, canon, governance, architecture, freeze state, or produce a patch.

## Blocking rule

If the user asks for implementation, refactor, architecture change, prompt canon update, governance update, freeze, or artifact-producing work, the AI must route the task before acting.

Use this sequence:

1. classify task intent;
2. check prompt_navigation_index;
3. check GROUP_ASSIMILATION_INDEX if group-level routing is needed;
4. request missing required groups or prompts;
5. state whether missing context is HARD STOP, STEP PAUSE, or DEGRADED WARNING;
6. proceed only inside the approved box.

## Missing-context levels

HARD STOP:
The task cannot safely proceed without the missing prompt, source file, validation output, or human decision.

STEP PAUSE:
The task may be discussed or planned, but the risky implementation/freeze/integration step must wait.

DEGRADED WARNING:
The task may proceed, but the AI must state the limitation and avoid final canon or freeze decisions.

## Primary routes

| Human intent | First route | Usually required groups |
|---|---|---|
| Start session | Tier 0 kernel | 01, 02 |
| Ask explanation only | Fast Path | none beyond loaded context |
| Create/update code | Implementation route | 04, 05, selected Python group |
| Refactor large module | Refactor route | 04, 05, 06 |
| Update UI/layout | GUI/implementation route | 04, 05, 08 or project-specific UI prompt |
| Create database/storage | Data/API route | 04, 05, 09, 10 |
| Audit prompt | Prompt audit route | 02, 07 |
| Resolve prompt conflict | Prompt audit/conflict route | 02, 07, relevant prompt files |
| Freeze work | Governance/freeze route | 03, 05, validation evidence |
| Create handoff | Session handoff route | 03 |
| Productize/release | Productization route | 05, 09, 11 |

## Phase boundary

Current phase: Phase 1 - Context Routing Kernel.

Allowed outputs in this phase:

- start_of_day_master_stack.md
- ai_prompt_request_canon.md
- prompt_navigation_index.md
- ROUTING/GROUP_ASSIMILATION_INDEX.md
- ROUTING/group_assimilation_index.json
- reconciliation report

Forbidden in this phase:

- creating all 12 _FOLDER_ASSIMILATION.md cards
- changing live app files
- changing kanda_reasoner_app
- changing prompt_library_gui
- implementing a dispatcher

## AI response pattern

When a task requires routing, respond:

```text
This appears to be a <task type> task.
Routing level: <Fast Path / Tier 1 / Tier 2>
Required groups:
- <group_id>: <reason>
Required prompts before action:
- <prompt_id>: <reason>
Missing-context level: <HARD STOP / STEP PAUSE / DEGRADED WARNING>
Next safe action: <roadmap / ask for files / proceed / wait>
```

## Final rule

Route context before loading prompts.
Load groups before specialist prompts.
Do not load the whole library when a small route is enough.
