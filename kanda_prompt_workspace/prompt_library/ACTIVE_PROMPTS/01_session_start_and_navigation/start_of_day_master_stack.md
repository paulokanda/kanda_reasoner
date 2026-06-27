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

At the beginning of every session, carry this lightweight Box Logic rule into
all implementation, repair, refactor, prompt update, governance update, bundle,
GUI, validation, freeze, and artifact-delivery work:

- Identify the active box before implementation.
- State owner paths.
- State files allowed to change.
- State files explicitly out of scope.
- Declare cross-box touches before touching more than one box.
- Preserve public contracts and avoid private reach-in.
- Validate the active box and any touched external box.
- Do not proceed from memory when box ownership, owner paths, public contracts,
  or allowed supporting touches are unclear; inspect the needed source, prompt,
  manifest, or validation context first.

This bridge is only the startup enforcement layer. It does not replace the full
Box Architecture canon. When a task involves implementation, repair, refactor,
prompt update, governance update, bundle creation, GUI ownership, public
contracts, cross-box behavior, mutable-state ownership, or architecture-boundary
risk, route to `box_architecture_canon.md` before doing the risky step.

Do not load the full Box Architecture prompt during normal startup unless the
current task requires it.

## Code Module Size Bridge

At the beginning of every session, carry this lightweight module-size rule into
all code creation and refactor work:

- Ideal code module size: 400 lines or fewer.
- Maximum code module size: 500 lines or fewer.
- When creating a new code module, do not create a file above 500 lines; split
  the module by responsibility before delivery.
- When refactoring an existing code module above 500 lines, use the approved
  large-module protocol and split by responsibility.
- Prefer cohesive helper modules with clear ownership over large mixed-purpose
  files.
- This rule applies to code/source modules, especially `.py` files.
- This rule does not apply to plain text, Markdown, documentation, prompt,
  manifest, JSON, log, report, or other non-code content files. Files such as
  `.txt`, `.md`, `.json`, documentation artifacts, prompt files, manifests,
  and logs may be larger when their purpose requires it.

If a task needs the full methodology, route to `large_module_refactor_protocol.md`;
do not load the full prompt during normal startup unless needed.

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
