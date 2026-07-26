# Architecture Review Project Card Machine Canon

Version: 1.0  
Status: Active prompt-library canon  
Prompt ID: architecture_review_project_card_machine_canon  
Prompt code: KPR-12-005  
Owner group: 12_generalized_project_canons  
Load type: routed

## Purpose

Define the canonical ownership and lifecycle model for Architecture Review, its subtabs, and the Large File Refactor flow.

Use this model:

```text
KANDA Reasoner Tool = reusable card machine
Active Project = card owner
Selected large module = inserted card
Architecture Review / AST Split Audit = read card
Planner = interpret card information and prepare the operation
Workbench Preview = governed project-owned operation preview and evidence
Apply / Refactor Large Module = write the approved transformation to the card
Generated helper modules = part of the updated card/project result
Receipt / transaction evidence = durable project-owned evidence of the operation
Card eject = clear target-specific Tool memory after terminal completion or verified rollback
```

The analogy is an architecture rule, not decorative wording.

The Tool may read, analyze, plan, validate, preview, apply, verify, and produce receipts. It must not become the owner of the selected project's module, helper files, durable Preview state, transaction truth, mutation-lane state, receipts, or other project-specific durable evidence.

## Core principle

The machine processes the card; it does not become the card owner.

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

After eject, the project keeps the results. The Tool forgets card-specific working identity and becomes ready for another active project or another module.

## Required companion boundary

This canon specializes lifecycle behavior and must not replace the general Tool/Project boundary owner.

For any implementation task that can mutate source, change roots, move Workbench state, or confuse Tool and Project ownership, load both:

```text
KPR-12-001 project_tool_boundary_canon
KPR-12-005 architecture_review_project_card_machine_canon
```

`project_tool_boundary_canon` owns the general Tool-versus-Project identity rule.

`architecture_review_project_card_machine_canon` owns the Architecture Review card lifecycle:

```text
insert -> read -> plan -> workbench -> apply -> verify -> receipt -> eject
```

Do not merge these prompts and do not create a competing Tool/Project canon.

## Canonical actors and ownership

### 1. Card machine: KANDA Reasoner Tool

Tool-owned responsibilities:

- Architecture Review UI and subtab implementation;
- AST audit engines;
- Planner engines;
- Workbench engines;
- validators;
- routing and prompt logic;
- patch delivery engines;
- reusable transaction and mutation-lane implementation code;
- lifecycle guards and card-ejection logic.

Canonical owner:

```text
<tool_source_root>
```

The Tool may hold bounded in-memory state while a card is inserted. That state must be attributable to one active project root and one active target identity.

### 2. Card owner: Active Project

The selected active project owns:

- source module being refactored;
- resulting updated module;
- generated helper modules;
- project-specific durable Workbench state;
- canonical Preview runs;
- transaction records;
- mutation-lane state;
- RefactorReceipt;
- durable validation evidence assigned to project support;
- project-specific Error Memory and freeze memory in their canonical project-support owners.

Canonical owners:

```text
active project source:
<active_project_root>/...

durable project support:
<active_project_support_root>/...
```

### 3. Card: selected large module

The card is a module selected from the current Active Project.

Hard rule:

```text
selected_target must be inside active_project_root
```

A browse action, AST handoff, Planner handoff, Workbench snapshot, or restored transaction must not silently load a target from another project.

If target ownership cannot be proven:

```text
May proceed: NO
Reason: TARGET_OUTSIDE_ACTIVE_PROJECT_ROOT or TARGET_OWNERSHIP_UNRESOLVED
```

## Lifecycle state machine

The canonical state machine is:

```text
EMPTY
  -> CARD_INSERTED
  -> CARD_READ
  -> PLAN_READY
  -> WORKBENCH_READY
  -> PREVIEW_VALIDATED
  -> AUTHORIZED
  -> APPLYING
  -> VERIFIED_TERMINAL
  -> CARD_EJECTED
```

Rollback path:

```text
APPLYING or APPLIED_NOT_VERIFIED
  -> ROLLBACK_REQUESTED
  -> ROLLBACK_VERIFIED
  -> CARD_EJECTED
```

The Tool must not claim `CARD_EJECTED` while an open mutation transaction, unresolved apply outcome, or unverified rollback remains.

## Insert rule

A card may be inserted only when:

- an Active Project root is resolved;
- the selected target is inside that root;
- no incompatible card-specific async work is still authoritative;
- no open mutation transaction blocks switching;
- stale state from a previous card has been invalidated.

Insertion establishes a card identity binding:

```text
card_identity = {
    active_project_root,
    target_relative_path,
    target_content_hash or freshness basis,
    lifecycle_generation
}
```

Every asynchronous result and downstream handoff must prove that it still belongs to the current card identity before it can repopulate state.

## Read rule

Architecture Review and AST Split Audit may read information from the inserted card and its project context.

They may compute:

- structure;
- imports;
- symbols;
- responsibilities;
- dependency topology;
- test protection;
- architecture warnings;
- candidate split islands;
- bounded project context needed for planning.

Reading does not transfer ownership to the Tool.

Analysis artifacts that are transient may remain in bounded memory or daily-work. Durable project-specific evidence must be written only to its canonical project-support owner.

## Plan rule

Planner state belongs to the current inserted card identity.

On target change or project-root change, invalidate:

- candidate queue;
- selected candidate;
- analysis result;
- local-AI review result;
- plan versions;
- Planner-to-Workbench handoff;
- target-specific async generations.

A late async result from an old root or old target must fail closed and must not repopulate the current machine state.

## Workbench rule

The reusable Workbench engine is Tool-owned, but card-specific durable state is project-owned.

Canonical split:

```text
Tool implementation:
<tool_source_root>/...

Project source truth:
<active_project_root>/...

Durable Workbench state:
<active_project_support_root>/large_file_refactor_workbench/...

Canonical Preview:
<active_project_support_root>/large_file_refactor_workbench/preview/<preview_id>/...

Disposable Shadow:
<active_project_daily_work_root>/large_file_refactor_shadow/<shadow_id>/...
```

Preview and Shadow are not interchangeable.

Daily-work is garbage-only and must not become durable card memory.

## Write rule

When authorization gates pass, the write target is the Active Project source, never the Tool merely because the Tool performed the operation.

Correct:

```text
Tool engine executes refactor
-> writes authorized payload to <active_project_root>
-> resulting module and helper files belong to Active Project
```

Forbidden:

```text
Tool engine executes refactor
-> writes selected-project result into <tool_source_root> because KANDA performed the work
```

Self-hosting does not remove this logical distinction.

When:

```text
tool_source_root == active_project_root
```

because the selected Active Project is KANDA Reasoner itself, Tool identity and Project identity remain logically separate. Path equality is not permission to collapse ownership semantics.

## Transaction rule

Transaction truth is card/project-specific durable state.

It must live under the selected project support owner, for example:

```text
<active_project_support_root>/large_file_refactor_workbench/transactions/...
```

Mutation-lane state and receipts follow their canonical project-support owners.

Do not place transaction truth in:

- Tool source;
- daily-work;
- hidden process-global mutable state;
- a hardcoded KANDA-specific path when another project is selected.

If legacy and canonical durable transaction stores both contain truth, fail closed. Do not silently merge two durable authorities.

## Switch and eject rules

### Project-root switch

Changing Active Project root means unloading the current project card context.

Before the new project becomes authoritative, clear or invalidate all card-specific Tool memory:

- AST queue and selection;
- audit output tied to the old root;
- Planner candidate and plan state;
- Planner async generations;
- Workbench in-memory snapshot/result;
- completion evidence references;
- completion transaction references;
- apply outcome references;
- rollback result references;
- target-specific GUI selection.

Do not delete project-owned durable artifacts while unloading Tool memory.

### Target switch inside the same project

Changing from module A to module B unloads A-specific downstream state before B becomes authoritative.

The machine may retain project-level context that is explicitly safe and root-scoped, but must invalidate target-specific state.

### Transaction lock

While an open mutation transaction or unresolved apply outcome exists:

```text
project switch -> BLOCK
card switch -> BLOCK
card eject -> BLOCK
snapshot replacement -> BLOCK
```

Only terminal verified completion or verified rollback may release the card.

### Terminal eject

After terminal completion or verified rollback:

```text
clear target-specific Tool memory
retain project-owned source changes
retain generated helper files
retain canonical Preview/evidence
retain transaction records
retain mutation-lane state
retain RefactorReceipt
```

Eject means the machine forgets the card-specific working context. It does not undo or delete the user's project results.

## Router bridge requirements

For Architecture Review lifecycle implementation, the router bridge must explicitly classify:

```text
Active Project root:
Inserted card target:
Card ownership proven:
Current lifecycle phase:
Async result/root generation valid:
Planner state owner:
Workbench state owner:
Preview owner:
Shadow owner:
Transaction owner:
Open transaction blocks switch/eject:
Write target:
Terminal eject condition:
Tool memory cleared after completion:
Project durable results retained:
Self-hosting logical separation preserved:
May implement: YES / NO
```

If any ownership or lifecycle field is unresolved, `May implement` must be `NO`.

## Routing triggers

Load this canon when a task mentions or implies:

- Architecture Review tab;
- Architecture Review subtabs;
- AST Split Audit;
- card machine principle;
- insert module to refactor;
- selected large module;
- change project root during audit;
- change target module;
- stale async audit result;
- Planner target lifecycle;
- Planner-to-Workbench handoff;
- Workbench snapshot replacement;
- completion transaction;
- apply outcome;
- rollback result;
- RefactorReceipt;
- clear state after refactor;
- eject module after completion;
- Tool retaining project-specific module state;
- external project being misclassified as self-hosted.

For implementation tasks, pair with:

```text
router_bridge_governed_implementation
project_tool_boundary_canon
large_module_refactor_protocol, when large-module refactor behavior changes
```

## When not to use

Do not load this canon for:

- ordinary explanation-only discussion of card payment systems;
- medical or non-code writing;
- generic UI styling with no lifecycle or ownership consequence;
- project/tool boundary questions that do not involve Architecture Review lifecycle, where KPR-12-001 alone is sufficient;
- ordinary Workbench path ownership questions with no Architecture Review card lifecycle consequence, where KPR-12-001 and the relevant Workbench canon are sufficient.

## Failure patterns this canon must prevent

### Wrong project write

```text
module from Project B loaded while Project A is active
```

### Tool/project collapse

```text
project_root passed as tool_root
```

### Stale result repopulation

```text
audit starts on Project A
user switches to Project B
late Project A worker result repopulates current UI
```

### Partial unload

```text
AST target changes
Planner or Workbench still points to previous target
```

### Transaction/card mismatch

```text
open transaction for card A
UI switches to card B
```

### Sticky machine memory

```text
refactor completes
Tool still retains target-specific Planner/Workbench/completion state
```

### Destructive eject

```text
eject clears Tool memory by deleting project source, helpers, receipts, or durable evidence
```

## Validation requirements

A change governed by this canon is valid only when focused validation proves, as applicable:

- root change unloads AST, Planner, and Workbench target state;
- target change invalidates downstream card state;
- running audit or Planner work cannot repopulate a new root with stale results;
- open transaction blocks project switch, target switch, snapshot replacement, and eject;
- completed refactor releases target-specific Tool memory;
- AST/manual target selection remains inside Active Project root;
- external projects are not misclassified as self-hosted;
- transaction truth lives under project support;
- Preview stays under project support;
- Shadow stays disposable under daily-work;
- project source and generated helpers remain in Active Project ownership;
- Tool/Project logical separation survives self-hosting;
- touched Python source modules remain within governed size limits or route to the large-module protocol.

## Do-not-regress rules

- KANDA Reasoner Tool is the reusable card machine, not the owner of the inserted project module.
- The Active Project owns the selected module and resulting helper files.
- A card target must remain inside the current Active Project root.
- Root change unloads card-specific Tool memory before the new root becomes authoritative.
- Target change invalidates downstream target-specific Planner, Workbench, and completion state.
- Late async results must prove current root/target generation before repopulating state.
- Open transactions block switch, snapshot replacement, and eject.
- Terminal completion or verified rollback is required before eject.
- Eject clears Tool memory only; it does not delete project-owned durable results.
- Project source mutations write to the Active Project root.
- Durable Preview and transaction truth belong under Active Project support.
- Shadow and regenerable garbage belong under Active Project daily-work.
- Self-hosting preserves logical Tool/Project separation even when physical roots coincide.
- Pair KPR-12-005 with KPR-12-001 whenever Tool/Project identity is part of the Architecture Review lifecycle task.
