# Architecture Review Project Card Machine Principle

Identity:

```text
Prompt code: KPR-12-005
Prompt id: architecture_review_project_card_machine_canon
Title: Architecture Review Project Card Machine Canon
```

## Principle

KANDA Reasoner must treat Architecture Review like a reusable card machine.

```text
KANDA Reasoner Tool = reusable card machine
Active Project = card owner
Selected large module = inserted card
AST Split Audit = read the card
Planner = interpret the card and plan the operation
Workbench Preview = governed project-owned preview and evidence
Apply / Refactor Large Module = write the approved transformation to the Active Project
Generated helper modules = part of the Project result
Transaction record / mutation lane / RefactorReceipt = durable Project-owned evidence
Card eject = clear target-specific Tool memory only after verified terminal completion or verified rollback
```

The machine may read, analyze, plan, preview, validate, authorize, apply, verify, and produce receipts. It must not become the owner of the card or of the Project's durable results.

Canonical lifecycle:

```text
INSERT
-> READ
-> ANALYZE
-> PLAN
-> PREVIEW
-> VALIDATE
-> AUTHORIZE
-> WRITE TO ACTIVE PROJECT
-> VERIFY
-> RECEIPT
-> EJECT TARGET-SPECIFIC TOOL MEMORY
```

## Ownership rule

Tool-owned:

- Architecture Review UI and subtab implementation
- AST audit engine
- Planner engine
- Workbench engine
- validators
- lifecycle guards
- reusable transaction/mutation implementation code
- routing and prompt logic

Project-owned:

- selected source module
- updated source module
- generated helper modules
- durable Workbench support state
- canonical Preview
- transaction records
- mutation-lane state
- RefactorReceipt
- project-specific durable validation evidence

## Card insertion rule

A selected module may be loaded only when it belongs to the current Active Project:

```text
selected_target must be inside active_project_root
```

Cross-project card insertion must fail closed.

## Switch rule

Changing Project Root unloads all card-specific Tool state before the new Project becomes authoritative.

Changing target module unloads all downstream target-specific state before the new target becomes authoritative.

The unload must cover, as applicable:

```text
AST queue and selection
Planner candidates and plans
Planner async generations
Planner-to-Workbench handoff
Workbench in-memory snapshot/result
Completion evidence references
Completion transaction references
Apply outcome references
Rollback result references
Target-specific GUI selection
```

The unload must not delete Project-owned durable artifacts.

## Async-result rule

Every late asynchronous result must prove that it still belongs to the current Project Root, target, and lifecycle generation before repopulating state.

Old Project or old target results must fail closed.

## Transaction lock rule

While an open mutation transaction or unresolved apply outcome exists:

```text
project switch -> BLOCK
card switch -> BLOCK
snapshot replacement -> BLOCK
card eject -> BLOCK
```

Only verified terminal completion or verified rollback may release the card.

## Write rule

The reusable Tool performs the operation, but the authorized write target is the Active Project source.

```text
Tool engine executes refactor
-> write authorized payload to active_project_root
-> resulting module and helper files belong to Active Project
```

Self-hosting does not collapse Tool and Project identity. Even when the physical paths are equal, the logical roles remain separate.

## Workbench ownership rule

```text
Tool implementation:
<tool_source_root>/...

Project source:
<active_project_root>/...

Durable Workbench support:
<active_project_support_root>/large_file_refactor_workbench/...

Canonical Preview:
<active_project_support_root>/large_file_refactor_workbench/preview/<preview_id>/...

Disposable Shadow:
<active_project_daily_work_root>/large_file_refactor_shadow/<shadow_id>/...
```

Daily-work is garbage-only. It must not become durable card memory.

## Eject rule

After verified terminal completion or verified rollback:

```text
clear target-specific Tool memory
retain Project source changes
retain generated helper files
retain canonical Preview and evidence
retain transaction records
retain mutation-lane state
retain RefactorReceipt
```

Eject means the machine forgets the card-specific working context. It does not undo or delete the user's Project results.

## Companion canon rule

This principle specializes Architecture Review lifecycle and must be paired with the general Tool/Project boundary when ownership can be confused:

```text
KPR-12-001 project_tool_boundary_canon
KPR-12-005 architecture_review_project_card_machine_canon
```

KPR-12-001 owns the general Tool-versus-Project boundary.

KPR-12-005 owns the Architecture Review lifecycle:

```text
insert -> read -> plan -> workbench -> apply -> verify -> receipt -> eject
```

Do not merge them and do not create a competing Tool/Project canon.
