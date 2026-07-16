Today 10:25 AM
first_prompts_to_ai(20).zip
Zip Archive
prompt_library(20).zip
Zip Archive
tell_AI_read_before_all(20).md
File

kanda_reasoner__source_archive_part01_of_01(22).zip
Zip Archive
kanda_reasoner__png_assets_part01_of_01(21).zip
Zip Archive
kanda_reasoner__error_memory_manifest(22).json
File
kanda_reasoner__error_memory_full(22).zip
Zip Archive
kanda_reasoner__error_memory_ai_prompt(22).md
File
kanda_reasoner__error_lessons_compact(22).json
File
kanda_reasoner__ai_handoff_upload_readme(22).txt
Document
kanda_reasoner__ai_handoff_upload(22).zip
Zip Archive
kanda_reasoner__ai_handoff_all_in_one(21).zip
Zip Archive
_RUN_COLLECTOR_STATUS(22).txt
Document

0073 final improvement.md
File
we are going to stop grouing kanda_reasoner , now we are working in quality as discussed  in last part of last chat . dont implement anything yet , review first  last chat

0030b Project Versus KANDA Reasoner Tool Boundary Canon Addendum.md
File
0030b updated Project Versus KANDA Reasoner Tool Boundary Canon Addendum(1).md
File
0018b Box Architecture Canon v1.0 prompt.md
File
and very very important to inforce, tool versus project tool never invade project and vice versa, Mcard, box logic, anti leaking , shielding  = these all very strong. And yes you an add a new feature proven it It must solve a verified problem that the current KANDA Reasoner cannot already solve adequately.

 Mcard Logic KANDA_MACHINE_CARD_LOGIC_BEGIN
Prompt code: KPR-12-005
Prompt id: architecture_review_project_card_machine_canon
Purpose: apply the canonical Architecture Review Machine-Card lifecycle logic.
Source: canonical KANDA prompt-library file.

KANDA_MACHINE_CARD_PROMPT_FILE_BEGIN architecture_review_project_card_machine_canon.md
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

text
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



The analogy is an architecture rule, not decorative wording.

The Tool may read, analyze, plan, validate, preview, apply, verify, and produce receipts. It must not become the owner of the selected project's module, helper files, durable Preview state, transaction truth, mutation-lane state, receipts, or other project-specific durable evidence.

## Core principle

The machine processes the card; it does not become the card owner.

text
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



After eject, the project keeps the results. The Tool forgets card-specific working identity and becomes ready for another active project or another module.

## Required companion boundary

This canon specializes lifecycle behavior and must not replace the general Tool/Project boundary owner.

For any implementation task that can mutate source, change roots, move Workbench state, or confuse Tool and Project ownership, load both:

text
KPR-12-001 project_tool_boundary_canon
KPR-12-005 architecture_review_project_card_machine_canon



project_tool_boundary_canon owns the general Tool-versus-Project identity rule.

architecture_review_project_card_machine_canon owns the Architecture Review card lifecycle:

text
insert -> read -> plan -> workbench -> apply -> verify -> receipt -> eject



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

text
<tool_source_root>



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

text
active project source:
<active_project_root>/...

durable project support:
<active_project_support_root>/...



### 3. Card: selected large module

The card is a module selected from the current Active Project.

Hard rule:

text
selected_target must be inside active_project_root



A browse action, AST handoff, Planner handoff, Workbench snapshot, or restored transaction must not silently load a target from another project.

If target ownership cannot be proven:

text
May proceed: NO
Reason: TARGET_OUTSIDE_ACTIVE_PROJECT_ROOT or TARGET_OWNERSHIP_UNRESOLVED



## Lifecycle state machine

The canonical state machine is:

text
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



Rollback path:

text
APPLYING or APPLIED_NOT_VERIFIED
  -> ROLLBACK_REQUESTED
  -> ROLLBACK_VERIFIED
  -> CARD_EJECTED



The Tool must not claim 
CARD_EJECTED while an open mutation transaction, unresolved apply outcome, or unverified rollback remains.

## Insert rule

A card may be inserted only when:

- an Active Project root is resolved;
- the selected target is inside that root;
- no incompatible card-specific async work is still authoritative;
- no open mutation transaction blocks switching;
- stale state from a previous card has been invalidated.

Insertion establishes a card identity binding:

text
card_identity = {
    active_project_root,
    target_relative_path,
    target_content_hash or freshness basis,
    lifecycle_generation
}



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

text
Tool implementation:
<tool_source_root>/...

Project source truth:
<active_project_root>/...

Durable Workbench state:
<active_project_support_root>/large_file_refactor_workbench/...

Canonical Preview:
<active_project_support_root>/large_file_refactor_workbench/preview/<preview_id>/...

Disposable Shadow:
<transient_garbage_root>/large_file_refactor_shadow/<shadow_id>/...



Preview and Shadow are not interchangeable.

<transient_garbage_root> is garbage-only, owns no Tool or Project state, and must not become durable card memory. Its project-derived name is only a collision-safe staging namespace.

## Write rule

When authorization gates pass, the write target is the Active Project source, never the Tool merely because the Tool performed the operation.

Correct:

text
Tool engine executes refactor
-> writes authorized payload to <active_project_root>
-> resulting module and helper files belong to Active Project



Forbidden:

text
Tool engine executes refactor
-> writes selected-project result into <tool_source_root> because KANDA performed the work



Self-hosting does not remove this logical distinction.

When:

text
tool_source_root == active_project_root



because the selected Active Project is KANDA Reasoner itself, Tool identity and Project identity remain logically separate. Path equality is not permission to collapse ownership semantics.

## Transaction rule

Transaction truth is card/project-specific durable state.

It must live under the selected project support owner, for example:

text
<active_project_support_root>/large_file_refactor_workbench/transactions/...



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

text
project switch -> BLOCK
card switch -> BLOCK
card eject -> BLOCK
snapshot replacement -> BLOCK



Only terminal verified completion or verified rollback may release the card.

### Terminal eject

After terminal completion or verified rollback:

text
clear target-specific Tool memory
retain project-owned source changes
retain generated helper files
retain canonical Preview/evidence
retain transaction records
retain mutation-lane state
retain RefactorReceipt



Eject means the machine forgets the card-specific working context. It does not undo or delete the user's project results.

## Router bridge requirements

For Architecture Review lifecycle implementation, the router bridge must explicitly classify:

text
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



If any ownership or lifecycle field is unresolved, 
May implement must be NO.

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

text
router_bridge_governed_implementation
project_tool_boundary_canon
large_module_refactor_protocol, when large-module refactor behavior changes



## When not to use

Do not load this canon for:

- ordinary explanation-only discussion of card payment systems;
- medical or non-code writing;
- generic UI styling with no lifecycle or ownership consequence;
- project/tool boundary questions that do not involve Architecture Review lifecycle, where KPR-12-001 alone is sufficient;
- ordinary Workbench path ownership questions with no Architecture Review card lifecycle consequence, where KPR-12-001 and the relevant Workbench canon are sufficient.

## Failure patterns this canon must prevent

### Wrong project write

text
module from Project B loaded while Project A is active



### Tool/project collapse

text
project_root passed as tool_root



### Stale result repopulation

text
audit starts on Project A
user switches to Project B
late Project A worker result repopulates current UI



### Partial unload

text
AST target changes
Planner or Workbench still points to previous target



### Transaction/card mismatch

text
open transaction for card A
UI switches to card B



### Sticky machine memory

text
refactor completes
Tool still retains target-specific Planner/Workbench/completion state



### Destructive eject

text
eject clears Tool memory by deleting project source, helpers, receipts, or durable evidence



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
- Shadow and regenerable garbage may be placed under the ownership-free transient garbage root; this placement does not make them Active Project state.
- Self-hosting preserves logical Tool/Project separation even when physical roots coincide.
- Pair KPR-12-005 with KPR-12-001 whenever Tool/Project identity is part of the Architecture Review lifecycle task.
KANDA_MACHINE_CARD_PROMPT_FILE_END architecture_review_project_card_machine_canon.md

KANDA_MACHINE_CARD_LOGIC_END

lets add these ideas to discussion

0037 kanda-reasoner tool versus kand_reasoner project.md
File
ne more revision on tool versus project , audit if it add usefull information 

Pasted text(46).txt
Document
NOW  GO TO WEB FOR :


Not completely.

The checklist captures most of Q01-Q40, especially the critical safety and implementation controls, but several backlog items are only implied or are missing as explicit checkable rows.
Fully or substantially covered

The checklist clearly covers:

    Q01-Q11: verified problem, Error Memory, exact source, Tool/Project, Box Architecture, NO-LEAK and MCard.

    Q14-Q18: freshness, canonical paths, containment, Preview/Shadow separation and stale async results.

    Q20-Q23: isolated fixtures, negative boundary matrices, facade tests and deterministic MCard tests.

    Q26-Q28: ZIP hardening, encoding/control-byte protection and exception provenance.

    Q30: human confirmation and freeze safety.

    Q36: module-size and cohesion requirements.

    Q40: one primary box per patch and governed release discipline.

Present but not explicit enough

These are covered indirectly but should receive dedicated checklist items:
ID	Missing explicit requirement
Q12	Verify whether one immutable operation identity exists and is used across all downstream stages.
Q13	Verify that mutation requires a formal write-authorization object or equivalent authority, not merely a path and boolean.
Q19	Require a decision on real PySide6/QSignalSpy validation when queued signals or thread affinity are relevant.
Q31	Create a visible changed-file-to-validator coverage map explaining why each validator applies.
Q32	Record complete validation and evidence provenance, including source fingerprints and reviewed Error Memory export.
Q34	Require a formal profile-before-optimization decision, not only a general anti-overengineering statement.
Q37	Explicitly audit and reconcile duplicate canonical ownership across existing analysis systems.
Q38	Verify freshness and provenance of every current AI handoff artifact, not only initial upload dates.
Missing or insufficiently represented

These Q-items are not currently strong checklist obligations:
ID	Required addition
Q24	A decision gate for a property-based MCard testing pilot after deterministic tests exist.
Q25	A decision gate for mutation testing of critical boundary guards.
Q29	An optional validation-time No-Leak runtime trace for unexpected writes, deletes, subprocesses and archive activity.
Q33	Pinned Hugging Face/local-model provenance when AI-generated evidence is involved.
Q35	Focused performance baselines for user-observed or profiler-confirmed bottlenecks.
Q39	A controlled test proving that a task-specific context summary is needed before building one.
Required correction

To claim full Q01-Q40 coverage, the checklist needs a dedicated section such as:

PHASE U - QUALITY BACKLOG COVERAGE

[ ] Q01 Verified-problem gate
[ ] Q02 Visible Error Memory preflight
...
[ ] Q40 Governed one-box release discipline

Each Q-item should be marked:

[x] Already enforced
[ ] Audit required
[~] In progress
[N/A] Rejected or conditional, with reason
[!] Blocked

This final crosswalk is important because otherwise a broad checklist may contain the general concept while still allowing a specific backlog commitment—such as Q24, Q29 or Q33—to be forgotten.

Current verdict: the checklist covers approximately 32 of the 40 items strongly, 4 partially, and 4-6 insufficiently. It should not yet be described as complete Q01-Q40 coverage.

lets cover everything?

Yes. This revised version explicitly covers Q01 through Q40 and supersedes the earlier checklist.
KANDA Reasoner Comprehensive Quality Checklist

Version: 1.1
Status: Mandatory
Coverage: Q01-Q40 complete
Supersedes: KANDA Reasoner Comprehensive Work Checklist v1.0
Purpose

Prevent any AI working on KANDA Reasoner from forgetting:

    Error Memory;

    exact-source inspection;

    Tool-versus-Project separation;

    Box Architecture;

    shielding and NO_LEAK_LOGIC_V1;

    MCard lifecycle;

    regression prevention;

    validation isolation;

    write authorization;

    source freshness;

    delivery safety;

    provenance;

    performance discipline;

    human confirmation;

    freeze and handoff requirements.

This checklist applies to every KANDA Reasoner chat involving:

    architecture;

    coding;

    bug correction;

    refactoring;

    new features;

    quality improvements;

    validation;

    GUI workflows;

    project-root behavior;

    Tool/Project ownership;

    patch or ZIP delivery;

    Error Memory;

    Freeze Memory;

    startup delivery;

    handoff generation.

It does not need to appear in unrelated medical, writing, or general-information conversations.
1. Status markers

Use only these markers:

[ ] Pending
[~] In progress
[x] Completed and verified
[!] Blocked
[?] Unresolved
[N/A] Not applicable - reason required

An item may be marked [x] only when evidence exists.

Do not mark an item complete based on:

    assumption;

    prior memory;

    filename alone;

    generated report alone;

    previous chat alone;

    Error Memory alone;

    a canon alone;

    unverified AI reasoning.

2. Mandatory checklist behavior

At the beginning of every governed KANDA chat:

    Display the live status dashboard.

    Display the Q01-Q40 coverage ledger.

    Mark previously completed items only when their evidence remains current.

    Reset freshness-sensitive items when new source or uploads are provided.

    Update the checklist immediately after completing a step.

    Keep blockers visible.

    Do not hide unresolved items behind a general statement such as "all checks passed."

Hard rule:

Any incomplete mandatory pre-code item
-> MAY BEGIN CODING: NO

Hard delivery rule:

Any incomplete release-contract item
-> MAY DELIVER PATCH: NO

Hard freeze rule:

No user-local validation or human confirmation
-> MAY FREEZE: NO

3. Live status dashboard

KANDA QUALITY WORK STATUS

Project slug:
Task:
Current phase:
Primary box:

Tool source root:
Active project root:
Active project support root:
Active project daily-work root:
Same physical Tool/Project root: YES / NO

Selected target:
Current source fingerprint:
Current MCard generation:
Current transaction:

Verified problem status:
Error Memory status:
Exact-source status:
Tool/Project boundary status:
Box Boundary status:
NO-LEAK status:
MCard status:
Regression plan status:
Validation plan status:
Evidence provenance status:

May begin coding: YES / NO
May write source: YES / NO
May build patch: YES / NO
May claim validation passed: YES / NO
May freeze: YES / NO

Current blockers:
Next safe action:

4. Phase A - Startup and project readiness
A1. Startup pack

    tell_AI_read_before_all.md was read first.

    Startup ZIP was read in the required order.

    Required startup files were recognized.

    Beginning-of-day bridges were loaded.

    Prompt Library was not opened broadly.

    Prompt Library prompts were loaded only through a routed path.

    STARTUP PACK LOAD CHECK was returned.

    Startup status is COMPLETE.

A2. Project handoff

    Collector status was reviewed.

    Project upload README was reviewed.

    Compact Error Memory was loaded.

    AI handoff ZIP was read in the required order.

    Project slug was resolved.

    Active project root was resolved.

    Tool source root was resolved.

    Project support root was resolved.

    Daily-work root was resolved.

    Source archive availability was confirmed.

    PROJECT READY CHECK was returned.

    Project readiness ends in WAIT_FOR_TASK.

A3. Handoff freshness - Q38

    Handoff generation date was checked.

    Handoff source fingerprint was checked.

    Source archive corresponds to the current project state.

    Routing manifest corresponds to the current project.

    Validation state corresponds to the current source snapshot.

    Compact Error Memory corresponds to the current export.

    Freeze context corresponds to the selected active project.

    No newer authoritative source is known to exist.

    Stale artifacts are visibly classified as stale.

    Generated handoff evidence is not treated as source truth.

Result:

HANDOFF FRESHNESS

Current:
Partially current:
Stale:
Unknown:
Exact source still required:

5. Phase B - Task classification

    User request was restated precisely.

    Requested outcome was identified.

    Task was classified:

        explanation;

        audit;

        research;

        architecture;

        implementation;

        repair;

        refactor;

        GUI;

        validation;

        patch delivery;

        freeze;

        handoff;

        startup maintenance;

        mixed governed work.

    Fast Path or Routed Work Path was selected.

    Primary affected capability was identified.

    Likely owner box was identified.

    Supporting boxes were identified.

    High-risk surfaces were identified.

    Source mutation was or was not requested.

    Patch delivery was or was not requested.

    Freeze preparation was or was not requested.

    Any bypass request was identified.

    Audit, confirmation, routing, validation, or ownership bypass was rejected.

6. Phase C - Verified-problem gate - Q01

A feature may be built only after proving a real inadequacy.

    Concrete problem identified.

    Problem is reproducible or supported by reliable evidence.

    Practical consequence documented.

    Current KANDA capability identified.

    Existing boxes that might already solve it identified.

    Existing tools, reports, scanners, validators, or workflows checked.

    Existing implementation was tested or inspected.

    Current capability is inadequate for a specific reason.

    Proposed change does not duplicate an existing capability.

    Expected gain is measurable or independently verifiable.

    Complexity is proportionate to benefit.

    Improvement is consolidation, correction, or proven capability addition.

    Speculative future needs are not being used as present justification.

VERIFIED-PROBLEM GATE

Problem:
Evidence:
Current capability:
Why it is inadequate:
Existing overlapping capabilities:
Duplication risk:
Expected measurable gain:
New feature justified: YES / NO

If New feature justified is NO:

MAY BEGIN CODING: NO

7. Phase D - Error Memory before coding
D1. Visible Error Memory preflight - Q02

    Compact Error Memory read.

    Relevant lesson IDs identified.

    Exact, partial, weak, or no-match classification assigned.

    Reason for each match stated.

    Applicable avoidance rule stated.

    Full Error Memory decision made.

    Error Memory treated as prevention guidance, not source truth.

D2. Regression-obligation matrix - Q03

Every relevant lesson must result in one of:

    Existing validator already protects it.

    New focused regression test required.

    Lesson is not applicable, with reason.

    Lesson is stale or partial and requires reinterpretation from current source.

ERROR MEMORY REGRESSION MATRIX

Lesson ID:
Match confidence:
Historical failure:
Current affected box:
Current affected paths:
Current public contract:
Current-source match:
Avoidance rule:
Existing validator:
Negative regression scenario:
Expected rejection marker:
Expected success marker:
Required action:

No lesson may remain merely as prose.
D3. Lesson freshness - Q04

For every relevant lesson:

    Current file still exists.

    Current symbol still exists.

    Current public facade was identified.

    Current owner box matches the lesson.

    Current source fingerprint was considered.

    Lesson status checked.

    superseded_by checked.

    Last verified context checked when available.

    Invalidation conditions checked.

    Stale lesson was not applied blindly.

D4. Required output

ERROR MEMORY CHECK

Project slug:
Task:
Primary area or box:

Relevant lesson IDs:
- Lesson:
  Confidence:
  Freshness:
  Current-source match:
  Avoidance rule:
  Regression obligation:

Full Error Memory ZIP needed:
YES / NO

Historical regressions to prevent:
Exact source still requiring inspection:

May proceed to source inspection:
YES / NO

May begin coding:
NO

8. Phase E - Exact-source baseline - Q05

    Exact current owner files inspected.

    Public facade inspected.

    Private implementations inspected where necessary.

    Imports inspected.

    Exports inspected.

    Callers inspected.

    Consumers inspected.

    Registries inspected where relevant.

    Controllers and adapters inspected.

    State ownership inspected.

    Persistence owners inspected.

    Path-resolution logic inspected.

    Async behavior inspected.

    GUI wiring inspected when applicable.

    Confirmation gates inspected.

    Existing validators inspected.

    Frozen behavior inspected.

    Module sizes measured.

    Current hashes or freshness basis recorded.

    Accepted behavior documented.

    Proven defects documented.

    Unknown behavior marked unknown.

    Generated artifacts not treated as canonical source.

    Example filenames not treated as exact paths.

EXACT-SOURCE BASELINE

Files inspected:
Public owner:
Private implementation:
Consumers:
State owner:
Path owner:
Current validators:
Current source fingerprints:
Accepted behavior:
Proven defect:
Unresolved questions:

9. Phase F - Tool versus Active Project
F1. Identity enforcement - Q06

    tool_project_slug resolved.

    tool_source_root resolved.

    active_project_slug resolved.

    active_project_root resolved.

    active_project_support_root resolved.

    active_project_daily_work_root resolved.

    Physical root equality checked.

    Logical identity remains separate during self-hosting.

    Operation is classified as Tool modification or project operation.

F2. Visible Tool/Project and NO-LEAK classification - Q07

TOOL/PROJECT OWNERSHIP CHECK

Reusable Tool files:
Active-project source files:
Project durable-support files:
Project Error Memory:
Project Freeze Memory:
Preview and transaction files:
Generated handoff files:
Daily-work files:
Shadow files:
External files:
Out-of-scope files:
Blocked writes:

F3. Canonical path authority - Q15

    One public path owner is identified.

    Support root derives from selected active project.

    Daily-work root derives from selected active project.

    Error Memory path derives from selected active project.

    Freeze Memory path derives from selected active project.

    Preview path derives from selected active project support.

    Shadow path derives from selected active project daily-work.

    No independent root constructor was added.

    No universal hardcoded kanda_reasoner target assumption exists.

F4. Structural path containment - Q16

    Paths are resolved structurally.

    String-prefix containment is not used.

    Target is proven inside active project root.

    Different-drive behavior tested.

    .. traversal tested.

    Sibling-prefix path tested.

    UNC path behavior tested where applicable.

    Symbolic-link or junction escape considered.

    Windows case normalization considered.

    Canonical owner cannot be proven -> write blocked.

F5. Source, Preview and Shadow separation - Q17

    Final source belongs to active project root.

    Durable Preview belongs to project support.

    Transaction truth belongs to project support.

    Receipt belongs to project support.

    Shadow belongs to daily-work.

    Patch staging belongs to daily-work.

    Daily-work owns no canonical truth.

    Preview and Shadow are not interchangeable.

    Cleanup cannot remove durable Preview truth.

    Shadow cannot become durable authority.

10. Phase G - Box Architecture
G1. Box Boundary Audit - Q08

BOX BOUNDARY AUDIT

Patch target:
Primary box:
Box type:
Box size:
Lifecycle state:

Single responsibility:
Owner paths:
Expected changed files:

Outside-owner files:
Reason:
Supporting touch allowed:
YES / NO

Public contract:
Private internals:
Inputs:
Outputs:

Dependencies:
Optional dependencies:
Forbidden dependencies:
Communication route:

Mutable state:
State owner:
Authorized mutators:

Fallback behavior:
Disable/removal behavior:

Circular-dependency risk:
Registry-leakage risk:
GUI/domain-mixing risk:
Private-reach-in risk:
Tool/Project risk:
No-Leak risk:

Focused tests:
Boundary tests:
Contamination tests:
Manual validation:

May proceed:
YES / NO

G2. Public-contract-only communication - Q09

    Other boxes use public facade or contract.

    No private module imported across boxes.

    No private method called across boxes.

    No private attribute mutated across boxes.

    Package-root import used only when symbol is explicitly exported.

    GUI emits intent.

    Commands are used for request-response.

    Events are used for notification.

    Controller does not absorb domain ownership.

    Registry contains metadata, not behavior or mutable runtime state.

G3. Single mutable-state owner - Q10

    Every mutable state object identified.

    One owner box declared.

    Read access route declared.

    Mutation route declared.

    No shared mutable global exists.

    No hidden singleton state exists.

    No two boxes mutate the same state.

    State is invalidated on project or target change where required.

G4. Module size and cohesion - Q36

    Touched Python modules measured.

    No touched module exceeds 500 physical lines after formatting.

    Ideal target of <=400 code lines considered.

    Formatting not compressed to evade size limits.

    Logic not duplicated to evade size limits.

    Helpers split by cohesive responsibility.

    Public facade remains small.

    Large-module protocol loaded when needed.

G5. Canonical ownership reconciliation - Q37

When overlapping systems exist:

    Competing owners identified.

    Public consumers identified.

    Duplicate scanners identified.

    Duplicate schemas identified.

    Duplicate report families identified.

    Duplicate state owners identified.

    One canonical owner selected per responsibility.

    Compatibility surface documented.

    Deprecation or migration path documented.

    No new super-box created merely to coordinate duplicates.

    Existing functionality preserved during consolidation.

11. Phase H - NO_LEAK_LOGIC_V1

NO-LEAK CHECK

Active box:
Tool-owned files:
Project source:
Project support:
Evidence files:
Daily-work:
External boxes:
Out-of-scope:
State involved:
Public contracts:
Leak risks:
Blocked writes:
Safe next action:

Required protections:

    No wrong-root writes.

    No Tool-to-Project source leakage.

    No Project-to-Tool source leakage.

    No cross-project leakage.

    No cross-box leakage.

    No private reach-in.

    No public-facade ownership leakage.

    No hidden mutable-state leakage.

    No stale-result leakage.

    No Preview-to-daily-work leakage.

    No Shadow-to-durable-support promotion.

    No generated-artifact-as-source leakage.

    No validation-evidence-as-source leakage.

    No freeze-evidence leakage.

    No Error Memory leakage.

    No prompt/canon source leakage.

    No transaction truth in Tool source.

    No support roots inside project source.

    No real drive-root validation fixtures.

12. Phase I - MCard lifecycle

Use when Architecture Review, AST Split Audit, Planner, Workbench, Preview, Apply, rollback, transaction, receipt, target switch, project switch, or eject is involved.
I1. Lifecycle enforcement - Q11

    Current MCard state identified.

    Requested transition is valid.

    Target belongs to current project.

    Open transaction status checked.

    Project-switch lock checked.

    Target-switch lock checked.

    Snapshot-replacement lock checked.

    Eject lock checked.

    Terminal completion or rollback required before eject.

    Eject clears Tool memory only.

    Project-owned results remain intact.

State model:

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

Rollback:

APPLYING / APPLIED_NOT_VERIFIED
-> ROLLBACK_REQUESTED
-> ROLLBACK_VERIFIED
-> CARD_EJECTED

I2. Immutable operation identity - Q12

    Current implementation audited for an operation identity.

    Tool root included.

    Active project root included.

    Active project slug included.

    Target relative path included.

    Target source hash or freshness basis included.

    Lifecycle generation included.

    Operation ID included.

    Transaction ID included when applicable.

    Identity is immutable or equivalently protected.

    Identity constructed only after ownership validation.

    Invalid ownership state cannot be represented.

    Separate loose roots are not passed where one context should be used.

Decision:

Immutable operation identity:
Already adequate / Strengthen / Missing / N/A

I3. Explicit write authorization - Q13

    Current mutation API inspected.

    Mutation requires explicit authority.

    Authority is tied to current operation.

    Authorized roots are explicit.

    Authorized paths are explicit.

    Expected source hashes are explicit.

    Approved Preview ID is explicit.

    Transaction ID is explicit.

    Current generation is explicit.

    Possession of a path alone does not authorize writing.

    Direct low-level write without authority fails.

I4. Immediate pre-write freshness - Q14

Immediately before mutation:

    Active project unchanged.

    Target unchanged.

    Lifecycle generation unchanged.

    Transaction unchanged.

    Preview still current.

    Authorization still current.

    Source hash matches approved Preview baseline.

    Destination ownership unchanged.

    Duplicate durable authority absent.

Failure result:

WRITE BLOCKED
Reason: SOURCE_CHANGED_SINCE_PREVIEW

or equivalent.
I5. Stale asynchronous-result rejection - Q18

    Worker request carries operation ID.

    Worker request carries project identity.

    Worker request carries target identity.

    Worker request carries source hash.

    Worker request carries lifecycle generation.

    Worker result carries the same identity.

    Receiver compares against current authoritative state.

    Old result is discarded.

    Old result cannot update GUI.

    Old result cannot update Planner state.

    Old result cannot update Workbench state.

    Rejection is observable diagnostically.

    Cancellation is not treated as sufficient protection.

I6. Real Qt signal tests - Q19

When queued Qt signals or thread affinity matter:

    Need for real PySide6 validation assessed.

    Real widget or controller instantiated where necessary.

    QSignalSpy or equivalent considered.

    Old-generation signal allowed to arrive in test.

    Receiver rejects stale result.

    Current state remains unchanged.

    No GUI object modified from worker thread.

    Mock-only validation not used when it cannot prove Qt behavior.

I7. Deterministic transition tests - Q23

    Valid transitions tested.

    Invalid transitions tested.

    Project switch during transaction tested.

    Target switch during transaction tested.

    Eject before terminal state tested.

    Rollback flow tested.

    Stale generation tested.

    Self-hosting tested.

    External-project use tested.

    Durable state unchanged after rejected transition.

I8. Property-based MCard pilot - Q24

After deterministic transition tests exist:

    Need for sequence-generation testing assessed.

    Hypothesis availability checked.

    Reference state model defined.

    Pilot scope limited.

    Invariants defined.

    Dependency cost assessed.

    Pilot must identify useful additional failures.

    Global adoption prohibited without demonstrated gain.

Decision:

Property-based pilot:
Adopt / Pilot / Defer / Reject / N/A

Reason:

I9. Mutation-testing pilot - Q25

For critical guards only:

    Critical validator subset selected.

    Mutation-testing tool evaluated.

    Expected guards identified.

    Surviving mutations treated as test gaps.

    Pilot cost measured.

    Full-project mutation testing not enabled automatically.

    Broader adoption requires proven value.

Decision:

Mutation-testing pilot:
Adopt / Pilot / Defer / Reject / N/A

Reason:

13. Phase J - Validation infrastructure
J1. Shared isolated filesystem fixtures - Q20

    Synthetic Tool root isolated.

    Synthetic active project isolated.

    Synthetic support root isolated.

    Synthetic daily-work root isolated.

    Synthetic Preview isolated.

    Synthetic Shadow isolated.

    Synthetic Error Memory isolated.

    Synthetic Freeze Memory isolated.

    Production formulas tested read-only.

    Real production path state unchanged.

    Fixture cleanup verified.

    Canonical public path dependency patched only within controlled scope.

J2. Parametrized negative boundary matrix - Q21

Test matrix includes, as applicable:

    Self-hosting.

    External project.

    Same drive.

    Different drive.

    Target inside project.

    Target outside project.

    .. traversal.

    Sibling-prefix confusion.

    UNC path.

    Junction or symlink escape.

    Windows case collision.

    Stale generation.

    Stale source hash.

    Open transaction.

    Missing optional dependency.

    Duplicate durable authority.

    Preview/daily-work confusion.

    Confirmation bypass attempt.

J3. Public-facade and contract-drift tests - Q22

    Documented facade imports successfully.

    Public symbols exist.

    Expected signatures remain compatible.

    Consumer does not require private implementation.

    Package root does not falsely appear to export symbols.

    Optional implementation can be absent.

    Fallback behavior works.

    Public facade remains canonical.

    Private helper cannot accidentally replace facade ownership.

J4. Control-byte and encoding regression guards - Q27

    Operational PowerShell scanned for hidden control bytes.

    Windows paths constructed safely.

    Validation evidence written as explicit UTF-8 where required.

    Legacy BOM-aware reading supported where required.

    UTF-16LE evidence fixture tested.

    Vertical-tab fixture tested.

    Decode failure reports phase and file clearly.

    Evidence merge preserves required markers.

J5. Structured exception provenance - Q28

    Original cause preserved.

    Domain wrapper preserves exception chaining.

    Operation phase recorded.

    Operation ID recorded.

    Target identity recorded.

    Root classification recorded.

    Last successful validation marker recorded.

    Setup failure distinguished from behavior failure.

    Cleanup failure distinguished from primary failure.

    Error Memory receives meaningful evidence.

J6. Changed-file-to-validator coverage map - Q31

CHANGED-FILE VALIDATION MAP

Changed file:
Owner box:
Public contract affected:
Historical lessons:
Frozen behavior:
Focused validator:
Boundary validator:
GUI validator:
Delivery validator:
Negative tests:
Reason each validator applies:
Reason excluded validators do not apply:

    Every changed source file mapped.

    Supporting files mapped.

    Contract changes mapped.

    Relevant validators selected.

    Irrelevant validators explicitly excluded with reason.

    No validator selected merely by filename similarity.

14. Phase K - ZIP and release safety
K1. ZIP containment and collision hardening - Q26

    No absolute ZIP members.

    No drive-qualified members.

    No UNC members.

    No .. members.

    No duplicate member names.

    No Windows case-fold collisions.

    No file/directory collisions.

    No unexpected symbolic links.

    No extraction outside staging root.

    Payload paths match declared install roots.

    Hashes match extracted content.

    Root sidecar not duplicated inside payload.

    Final exact ZIP passes contract validator.

K2. Human confirmation and freeze safeguards - Q30

    Preview remains read-only.

    Confirm and Write remains explicit.

    No automatic freeze-memory write.

    No automatic Error Memory promotion.

    User confirmation is tied to current Preview.

    User confirmation invalidated by source or target change.

    Freeze requires user-local validation.

    Freeze requires explicit human approval.

K3. One primary box and governed release - Q40

    One primary box declared.

    Supporting touches declared.

    No unrelated cleanup included.

    Source baseline hashes checked.

    Patch contains only intended files.

    Changed box boundaries documented.

    Error Memory matrix attached.

    Validation map attached.

    Final ZIP contract passed.

    Freeze metadata generated from one source.

    Release status reported honestly.

15. Phase L - Evidence and AI provenance
L1. Validation and evidence provenance - Q32

Evidence records:

    Active project slug.

    Active project root.

    Source fingerprints.

    Operation ID.

    Target identity.

    Error Memory export hash or revision.

    Lesson IDs reviewed.

    Freeze context revision.

    Prompt revision where applicable.

    Validation command.

    Validator version.

    Expected markers.

    Actual markers.

    Date and time.

    Sandbox or user-local environment.

    Known limitations.

Evidence cannot claim current status when source fingerprints differ.
L2. Pinned local-model provenance - Q33

When Hugging Face or another local model contributes to a decision:

    Model repository or local identifier recorded.

    Exact revision or commit recorded.

    Tokenizer revision recorded.

    Custom code revision recorded where relevant.

    Prompt ID recorded.

    Prompt hash recorded.

    Inference settings recorded.

    Offline/local mode recorded.

    Input source fingerprints recorded.

    Output hash recorded.

    Unpinned output remains advisory only.

    AI output is not deterministic validation evidence by itself.

If no local model is involved:

[N/A] Q33 - no local or Hugging Face model involved.

L3. Task-specific context summary admission test - Q39

Before building a new task-specific context feature:

    Current handoff tested on representative tasks.

    Failure to identify owner files demonstrated.

    Failure to identify validators demonstrated.

    Failure to retrieve relevant memories demonstrated.

    Context-size problem measured.

    Current routing could not be strengthened more simply.

    Proposed summary reuses existing manifests.

    No new graph or database created unnecessarily.

    Controlled comparison shows improvement.

Decision:

Task-specific context feature:
Build / Strengthen existing handoff / Defer / Reject

Verified gain:

16. Phase M - Performance discipline
M1. Profile-before-optimization - Q34

    Named slow operation identified.

    User-observed or measured problem exists.

    Workload defined.

    Baseline measured.

    Repeated runs performed.

    Variance considered.

    CPU, I/O, memory, GUI-thread, or model bottleneck classified.

    Target improvement defined.

    Complexity cost defined.

    Optimization not justified by theory alone.

    No dependency added before measurement.

M2. Focused performance baselines - Q35

For proven bottlenecks only:

    Benchmark scope limited to owning box.

    Representative project used.

    Warm-up considered.

    Repeat count documented.

    Timing method documented.

    Memory measurement documented where relevant.

    Before/after results compared.

    Readability and maintenance cost reviewed.

    Specialized acceleration rejected unless benefit is material.

    No global benchmark framework created without need.

17. Phase N - Optional No-Leak runtime observability - Q29

A validation-time trace may be piloted for high-risk mutation operations.

    Need for runtime side-effect tracing assessed.

    File opens observed where useful.

    Writes observed.

    Renames/replacements observed.

    Deletes observed.

    Archive operations observed.

    Imports observed where relevant.

    Subprocess launches observed.

    Every mutation matched to a declared root.

    Unexpected side effects fail validation.

    Trace is validation-only.

    Trace is not described as a security sandbox.

    Python audit hooks are not relied upon as complete enforcement.

Decision:

No-Leak runtime trace:
Pilot / Defer / Reject / N/A

Reason:

18. Phase O - Formal pre-code authorization

PRE-CODE AUTHORIZATION

[ ] Q01 Verified problem
[ ] Q02 Visible Error Memory preflight
[ ] Q03 Regression-obligation matrix
[ ] Q04 Lesson freshness
[ ] Q05 Exact-source baseline
[ ] Q06 Tool/Project identity
[ ] Q07 Visible ownership and NO-LEAK classification
[ ] Q08 Box Boundary Audit
[ ] Q09 Public-contract-only communication
[ ] Q10 Single mutable-state owner
[ ] Q11 MCard lifecycle or N/A
[ ] Q12 Immutable operation identity assessed
[ ] Q13 Write authorization assessed
[ ] Q14 Immediate freshness gate defined
[ ] Q15 Canonical path owner
[ ] Q16 Structural containment
[ ] Q17 Preview/Shadow/source separation
[ ] Q18 Stale async-result protection
[ ] Q19 Real Qt validation decision
[ ] Q20 Isolated fixture strategy
[ ] Q21 Negative boundary matrix
[ ] Q22 Public-facade tests
[ ] Q23 MCard transition tests
[ ] Q24 Property-based pilot decision
[ ] Q25 Mutation-testing pilot decision
[ ] Q26 ZIP contract requirements
[ ] Q27 Encoding/control-byte protections
[ ] Q28 Exception provenance
[ ] Q29 Runtime trace decision
[ ] Q30 Human confirmation gates
[ ] Q31 Changed-file validation map
[ ] Q32 Evidence provenance
[ ] Q33 Local-model provenance or N/A
[ ] Q34 Profiling gate or N/A
[ ] Q35 Performance baseline or N/A
[ ] Q36 Module-size and cohesion
[ ] Q37 Ownership reconciliation or N/A
[ ] Q38 Handoff freshness
[ ] Q39 Context-summary admission test or N/A
[ ] Q40 One-box release discipline

User authorization to implement:
YES / NO

MAY BEGIN CODING:
YES / NO

Reason:

19. Phase P - Implementation discipline

    One primary box modified.

    Supporting touches remain declared.

    No unrelated cleanup included.

    Public facade preserved.

    Private internals remain private.

    No new dependency cycle.

    No duplicate logic.

    No duplicate source of truth.

    No hidden mutable global.

    No hardcoded active-project assumption.

    No independent path formula.

    No generated artifact used as source.

    No confirmation gate removed.

    No stale worker result accepted.

    Writes require current authority.

    Source freshness checked before mutation.

    Exception cause preserved.

    Temporary resources cleaned reliably.

    Module-size gate respected.

    Existing behavior outside scope preserved.

20. Phase Q - Validation execution
Q1. Static validation

    Changed Python files compile.

    Public imports resolve.

    Module-size gate passes.

    No private cross-box imports.

    No circular dependency.

    No GUI import in pure data box.

    No registry leakage.

    No duplicate root constructor.

    No nested support root.

    No generated source used as authority.

Q2. Behavioral validation

    Contract tests pass.

    Focused tests pass.

    Boundary tests pass.

    Contamination tests pass.

    Negative tests pass.

    Historical regression tests pass.

    Existing accepted behavior passes.

    Real PySide6 tests pass when relevant.

    Async stale-result tests pass when relevant.

    MCard tests pass when relevant.

    Confirmation tests pass.

    Self-hosting tests pass.

    External-project tests pass.

Q3. Filesystem validation

    Synthetic roots isolated.

    No real drive-root fixture created.

    Production paths unchanged.

    Disposable content cleaned.

    Durable Preview preserved.

    Shadow remains disposable.

Q4. Release validation

    Exact final ZIP validated.

    ZIP collisions rejected.

    Payload ownership correct.

    Sidecar placement correct.

    Hashes correct.

    Required markers present.

Q5. Honest validation result

VALIDATION STATUS

Static:
Focused:
Boundary:
Regression:
GUI:
Filesystem:
Delivery:
Evidence:
User-local:

May claim validation passed:
YES / NO

Unrun validation:
Limitations:

21. Phase R - User-local validation

    Exact commands provided.

    Commands use dynamic active-project root.

    Commands correspond to exact patch.

    User ran validation.

    Complete output reviewed.

    Required markers present.

    Warnings investigated.

    GUI visually confirmed when relevant.

    No root leakage observed.

    Accepted behavior confirmed.

    User approved or rejected result.

22. Phase S - Freeze readiness

    Freeze protocol loaded.

    Current feature data used.

    Current validation used.

    Active project selected correctly.

    Freeze intake under project support.

    Frozen memory under project support.

    Reusable freeze engine does not own project memory.

    Preview remains read-only.

    Confirm and Write remains explicit.

    Freeze JSON is valid.

    Sidecar and form share one source.

    Protected paths current.

    User-local validation passed.

    Human explicitly approved freeze.

FREEZE READINESS

May freeze:
YES / NO

Reason:

23. Phase T - Error Memory after failure

    Exact failure phase identified.

    Exact exception captured.

    Current source inspected.

    Symptom separated from cause.

    Root cause proven or marked uncertain.

    Repair validated.

    Negative regression scenario added.

    Long-term prevention rule created.

    Lesson does not overgeneralize.

    Current box recorded.

    Current contract recorded.

    Current paths/fingerprint recorded.

    Staleness conditions recorded.

    Regression command recorded.

    Expected markers recorded.

    Lesson staged for human review.

    Lesson not promoted automatically.

    Human approved memorization.

24. Phase U - Final handoff

    Work completed summarized.

    Files changed listed.

    Primary box listed.

    Supporting touches listed.

    Public contracts listed.

    Tool/Project ownership listed.

    Project-support artifacts listed.

    Daily-work artifacts classified disposable.

    Error Memory lessons listed.

    Frozen behavior listed.

    Validation commands listed.

    Validation results reported honestly.

    Unrun checks reported.

    Remaining risks reported.

    Remaining blockers reported.

    Next safe action stated.

    Final checklist updated.

25. Q01-Q40 live coverage ledger

This ledger must appear in every governed KANDA chat.
ID	Requirement	Status	Evidence or reason
Q01	Verified-problem admission gate	[ ]	
Q02	Visible Error Memory preflight	[ ]	
Q03	Error Memory regression-obligation matrix	[ ]	
Q04	Lesson freshness verification	[ ]	
Q05	Exact-source baseline	[ ]	
Q06	Tool/Project identity enforcement	[ ]	
Q07	Visible Tool/Project and NO-LEAK check	[ ]	
Q08	Box Boundary Audit	[ ]	
Q09	Public-contract-only communication	[ ]	
Q10	Single mutable-state owner	[ ]	
Q11	MCard lifecycle enforcement	[ ]	
Q12	Immutable operation identity	[ ]	
Q13	Explicit write authorization	[ ]	
Q14	Immediate pre-write freshness check	[ ]	
Q15	Canonical path-authority contract	[ ]	
Q16	Resolved-path containment	[ ]	
Q17	Preview, Shadow and source separation	[ ]	
Q18	Stale asynchronous-result rejection	[ ]	
Q19	Real Qt/QSignalSpy validation decision	[ ]	
Q20	Shared isolated filesystem fixtures	[ ]	
Q21	Parametrized negative boundary matrix	[ ]	
Q22	Public-facade and contract-drift tests	[ ]	
Q23	Deterministic MCard transition tests	[ ]	
Q24	Property-based MCard pilot decision	[ ]	
Q25	Mutation-testing pilot decision	[ ]	
Q26	ZIP containment and collision hardening	[ ]	
Q27	Control-byte and encoding guards	[ ]	
Q28	Structured exception provenance	[ ]	
Q29	No-Leak runtime trace pilot decision	[ ]	
Q30	Human confirmation and freeze protection	[ ]	
Q31	Changed-file-to-validator coverage map	[ ]	
Q32	Validation and evidence provenance	[ ]	
Q33	Pinned local-model provenance or N/A	[ ]	
Q34	Profile-before-optimization gate or N/A	[ ]	
Q35	Focused performance baseline or N/A	[ ]	
Q36	Module-size and cohesion enforcement	[ ]	
Q37	Canonical ownership reconciliation or N/A	[ ]	
Q38	Handoff freshness and provenance	[ ]	
Q39	Task-specific context admission test or N/A	[ ]	
Q40	One-primary-box governed release	[ ]	
26. Absolute stop conditions

Immediately stop before coding when:

    Error Memory was not checked.

    Exact source was not inspected.

    Verified problem was not established.

    Tool or active project identity is unresolved.

    Target ownership cannot be proven.

    Primary box is unresolved.

    Public contract is unresolved.

    Private reach-in would be required.

    Mutable state ownership is ambiguous.

    Duplicate capability may be created.

    Regression obligations are undefined.

    Validation scope is undefined.

    Source freshness is unknown.

    Confirmation gate would be bypassed.

    Open transaction blocks operation.

    Stale async result can repopulate state.

    Durable state would live in daily-work.

    Synthetic validation would touch production roots.

Stop before delivery when:

    Final ZIP contract has not passed.

    Changed files are not mapped to validators.

    Evidence provenance is incomplete.

    Patch touches undeclared boxes.

    Sidecar and payload disagree.

Stop before freeze when:

    User-local validation is absent.

    Explicit human confirmation is absent.

    Freeze paths are unresolved.

    Validation evidence is stale.

    Source changed after validation.

Required output:

MAY PROCEED: NO

Blocked by:
Required evidence:
Next safe action:

27. Mandatory compact sequence

STARTUP
-> PROJECT READY
-> TASK CLASSIFICATION
-> VERIFIED PROBLEM
-> ERROR MEMORY FIRST
-> ERROR REGRESSION MATRIX
-> EXACT SOURCE
-> TOOL/PROJECT IDENTITY
-> BOX BOUNDARY
-> NO-LEAK SHIELD
-> MCARD, WHEN APPLICABLE
-> OPERATION IDENTITY
-> WRITE AUTHORIZATION
-> FRESHNESS CHECK
-> VALIDATOR COVERAGE MAP
-> REGRESSION PLAN
-> PRE-CODE AUTHORIZATION
-> IMPLEMENT
-> VALIDATE
-> USER CONFIRMATION
-> DELIVER
-> FREEZE, IF REQUESTED
-> ERROR MEMORY, IF NEEDED
-> HANDOFF

This version now has explicit coverage for every item from Q01 to Q40, including the previously underrepresented pilots, provenance, performance, Qt validation, ownership reconciliation, handoff freshness, and task-specific context admission test.

now you will call this check list "brick wall" make it a prompt, insert it in prompt library , each time I call "brick wall" we will check were we are related to evolution of implementation, brick wall will be updated as long as  we are updating implementation , now do it zip- install - freeze - error lesson

BRICK WALL STATUS
Step	Status	Evidence
Verified need established	[x]	Prevents Q01-Q40 safeguards from being forgotten across implementation chats
Existing-prompt duplicate audit	[x]	No equivalent canonical prompt found
Canonical prompt created	[x]	brick_wall_comprehensive_quality_gate
Prompt code assigned	[x]	KPR-03-001
Canonical owner selected	[x]	03_governance_freeze_and_handoff
Load mode selected	[x]	Routed, with a compact startup bridge
Folder card updated	[x]	Prompt registered in owning folder
Human routing updated	[x]	Exact Brick Wall trigger included
Machine routing updated	[x]	JSON and CSV routing updated
Q01-Q40 coverage	[x]	All 40 requirements explicitly included
Startup delivery regeneration	[x]	Sandbox regeneration passed
Focused validator created	[x]	All Brick Wall routing and content markers passed
Patch ZIP created	[x]	Final exact ZIP produced
ZIP contract	[x]	ZIP CONTRACT: PASS
Sandbox installation	[x]	Clean-copy installation simulation passed
Sandbox validation	[x]	VALIDATION OK and STATUS: IN_SYNC
Freeze-intake preparation	[x]	Hint discovery and evidence merge passed in isolation
Evidence-backed Error Memory lesson	[x]	One real validator error documented
User-local Windows installation	[ ]	Must be run on E:\kanda_reasoner
User-local validation	[ ]	Required before freeze
Freeze Preview	[ ]	Must be reviewed by you
Freeze Confirm and Write	[ ]	Explicit human confirmation required
Error Memory memorization	[ ]	Lesson is staged, not automatically promoted

Current authorization

Patch delivery: YES
User-local installation confirmed: NO
User-local validation confirmed: NO
May freeze now: NO
May claim frozen: NO

What “Brick Wall” now means

When you write:

Brick Wall

I will display and update:

    BRICK WALL STATUS

    current blockers;

    the Q01-Q40 live coverage ledger;

    completed evidence;

    the next safe action;

    coding, patch, validation and freeze authorization.

Freshness-sensitive checks will reset when source, handoff, validation or freeze evidence changes.

Brick Wall coordinates the safeguards but does not replace Error Memory, exact-source inspection, Tool/Project separation, Box Architecture, NO_LEAK_LOGIC_V1, MCard, validation or freeze canons. This preserves the canonical ownership rules already established for KANDA’s self-hosting workflow.
PATCH DELIVERY GATE

Feature:
Brick Wall Comprehensive Quality Gate Prompt Registration v1

Primary box:
kanda_prompt_workspace/prompt_library

Files installed:
10

Canonical prompt:
brick_wall_comprehensive_quality_gate

Prompt code:
KPR-03-001

Freeze sidecar:
Present at ZIP root

Error Memory lesson:
Present and schema-validated

Install script:
Present

Validation script:
Present

Freeze-preparation script:
Present

Final exact ZIP contract:
PASS

Patch SHA-256:
6c5cf2f0860a0c6352e7ea151d759c89c97dc5c067c8420031a8ff262490602f

GATE STATUS:
PASS

Files

Installation

Place the ZIP at:

E:\kanda_brick_wall_prompt_registration_v1.zip

Save brick_wall_INSTALL.ps1 anywhere convenient and run it using its actual saved path:

powershell -NoProfile -ExecutionPolicy Bypass -File "C:\Path\brick_wall_INSTALL.ps1" -ProjectRoot "E:\kanda_reasoner"

The installer will:

    detect the project drive;

    move the ZIP from E:\ into E:\kanda_reasoner_delete_after_daily_work;

    fresh-extract the staged ZIP;

    verify the audited source hashes;

    back up changed files under daily-work;

    install the exact prompt and routing files;

    regenerate startup delivery from canonical sources;

    stage the Error Memory lesson for human review;

    avoid writing freeze memory automatically.

Expected marker:

INSTALL OK: brick-wall-comprehensive-quality-gate-prompt-registration-v1

Validation

Run:

powershell -NoProfile -ExecutionPolicy Bypass -File "C:\Path\brick_wall_VALIDATE.ps1" -ProjectRoot "E:\kanda_reasoner"

Required final markers:

ZIP CONTRACT: PASS
BRICK_WALL_PROMPT_BODY: PASS
BRICK_WALL_METADATA_IDENTITY: PASS
BRICK_WALL_FOLDER_REGISTRATION: PASS
BRICK_WALL_STARTUP_ROUTE_BRIDGE: PASS
BRICK_WALL_MACHINE_ROUTING: PASS
BRICK_WALL_HUMAN_ROUTING: PASS
BRICK_WALL_ROUTE_COVERAGE_TABLE: PASS
BRICK_WALL_GROUP_ROUTING: PASS
BRICK_WALL_STARTUP_GENERATED_ARTIFACT: PASS
BRICK_WALL_ERROR_LESSON_STAGED: PASS
BRICK_WALL_PROJECT_ROOT_FREEZE_HINT_ABSENT: PASS
VALIDATION OK: brick-wall-comprehensive-quality-gate-prompt-registration-v1
STATUS: IN_SYNC

Freeze preparation

Only after the complete local validation passes:

powershell -NoProfile -ExecutionPolicy Bypass -File "C:\Path\brick_wall_FREEZE.ps1" -ProjectRoot "E:\kanda_reasoner"

Expected markers:

FREEZE_HINT_SCAN: PASS
FREEZE_VALIDATION_EVIDENCE_MERGE: PASS
VALIDATION OK: brick-wall-comprehensive-quality-gate-prompt-registration-v1
STATUS: IN_SYNC

Then use:

Freeze Feature After Update
-> New Local Freeze Entry
-> Preview
-> review all current data
-> Confirm and Write

The script intentionally does not write frozen memory. Preview and explicit human confirmation remain protected.
Error Memory lesson

One real error occurred during development:

lesson-brick-wall-validator-startup-artifact-packaging-assumption-v1

The original validator incorrectly expected 02_prompt_navigation_index.md to exist as a loose generated startup file. The canonical generator places it inside first_prompts_to_ai.zip. The validator was corrected to inspect the ZIP member.

The installer stages the lesson under the active project’s external Error Memory intake for your review. It is not automatically memorized.

After installation and validation, send me the complete terminal output and invoke:

Brick Wall

The ledger will then mark local installation and validation complete and identify the remaining freeze and Error Memory actions.

continue

BRICK WALL — CURRENT STATUS

The first package has been superseded after the checklist exposed three additional delivery defects before user installation:

    ZIP members were not inspected before Expand-Archive.

    Validation evidence was stored only in disposable daily-work.

    Manifest paths were not independently proven to remain under payload, project, and backup roots.

All three were corrected. The final replacement is v1r2.
Q01–Q40 ledger
ID	Requirement	Status	Evidence
Q01	Verified-problem gate	[x]	Persistent Q01–Q40 tracking is a verified governance need
Q02	Visible Error Memory preflight	[x]	Compact lessons reviewed before correction
Q03	Regression-obligation matrix	[x]	Four lessons have executable regression markers
Q04	Lesson freshness	[x]	Lessons checked against current source and delivery canons
Q05	Exact-source baseline	[x]	All old manifest hashes matched the uploaded source archive
Q06	Tool/Project identity	[x]	Dynamic Tool, project, support, and daily-work ownership preserved
Q07	Visible ownership/NO-LEAK check	[x]	Source, support, evidence, and transient files classified
Q08	Box Boundary Audit	[x]	Primary box: prompt library; delivery helpers remain transient
Q09	Public-contract-only communication	[x]	Human, JSON, CSV, group, and startup routes updated
Q10	Single mutable-state owner	[N/A]	Prompt registration introduces no persistent runtime mutable state
Q11	MCard lifecycle	[N/A]	No Architecture Review card lifecycle involved
Q12	Immutable operation identity	[N/A]	Delivery identity uses exact feature, ZIP, manifest, and source hashes
Q13	Explicit write authorization	[x]	Human-run installer plus exact audited manifest/hash authority
Q14	Immediate freshness check	[x]	Every existing target must match its audited old or new hash
Q15	Canonical path authority	[x]	Roots derive dynamically from ProjectRoot
Q16	Structural path containment	[x]	ZIP and manifest paths independently validated and contained
Q17	Source/support/daily separation	[x]	Durable evidence moved to support; staging remains disposable
Q18	Stale async-result rejection	[N/A]	No asynchronous worker introduced
Q19	Real Qt validation	[N/A]	No Qt behavior changed
Q20	Isolated filesystem validation	[x]	Clean-copy and isolated startup-output tests passed
Q21	Negative boundary matrix	[x]	Unsafe ZIP/manifest path categories explicitly rejected
Q22	Facade and contract tests	[x]	Prompt identity and all canonical routing surfaces validated
Q23	MCard transition tests	[N/A]	No MCard state machine involved
Q24	Property-based pilot	[N/A]	No lifecycle sequence problem in this patch
Q25	Mutation-testing pilot	[N/A]	Not proportionate for prompt registration
Q26	ZIP hardening	[x]	Exact final ZIP and local extraction guards passed
Q27	Encoding/control-byte protection	[x]	All PowerShell scripts UTF-8 without forbidden control bytes
Q28	Exception provenance	[x]	Install, validation, freeze, and lessons preserve failure phase
Q29	Runtime No-Leak trace	[N/A]	Static and isolated delivery validation sufficient here
Q30	Human confirmation/freeze safety	[x]	Freeze remains Preview plus Confirm and Write
Q31	Changed-file validator map	[x]	Included in validation report
Q32	Evidence provenance	[x]	Exact ZIP hash, source baseline, commands, and markers recorded
Q33	Local-model provenance	[N/A]	No Hugging Face or local model used
Q34	Profile-before-optimization	[N/A]	No performance change
Q35	Performance baseline	[N/A]	No performance work
Q36	Module-size/cohesion	[x]	Focused validator remains within governed size
Q37	Ownership reconciliation	[x]	Duplicate prompt audit completed; no competing prompt created
Q38	Handoff freshness	[x]	Current source archive and routing source inspected
Q39	Context-summary admission test	[N/A]	Brick Wall reuses current routing; no new context engine
Q40	Governed one-box release	[~]	Sandbox complete; local validation and freeze remain pending
Remaining blockers

[ ] Windows installation into E:\kanda_reasoner
[ ] User-local validation
[ ] Freeze Preview review
[ ] Explicit Confirm and Write
[ ] Human review of four Error Memory lessons

May begin local installation: YES
May claim user-local validation passed: NO
May freeze: NO
May claim Error Memory lessons memorized: NO

PATCH DELIVERY GATE

ZIP purpose:
Install and register the routed Brick Wall Q01-Q40 prompt.

ZIP placement:
E:\kanda_brick_wall_prompt_registration_v1r2.zip

What this ZIP is:
A governed prompt-library source patch with installation, validation,
freeze-preparation, and Error Memory intake artifacts.

What this ZIP is not:
It is not a source archive, full project replacement, frozen-memory record,
or automatically approved Error Memory update.

Install code present: YES
Validation code present: YES
Freeze preparation present: YES
Error Memory payload: YES — four marker-wrapped lessons

Allowed writes:
- E:\kanda_reasoner audited prompt-library and focused validator paths
- E:\kanda_reasoner_show_project_to_AI project support
- E:\kanda_reasoner_delete_after_daily_work transient staging

Forbidden writes:
- KANDA_FREEZE_HINT.json into the project root
- durable evidence only in daily-work
- source outside the audited manifest
- Tool/project cross-owner leakage

Exact final ZIP contract: PASS
GATE STATUS: PASS

Final replacement package

Do not install v1 or v1r1. Use only v1r2.

SHA-256

9b60ab2eceb8b35e97fffbc934842e642c02a1dd9dbcf5d3108a1472260b3521

1. Install

Place the ZIP here without extracting it:

E:\kanda_brick_wall_prompt_registration_v1r2.zip

Run the downloaded installer using its actual saved location:

$ProjectRoot = "E:\kanda_reasoner"
$Installer = "C:\Path\To\brick_wall_v1r2_INSTALL.ps1"

powershell -NoProfile -ExecutionPolicy Bypass `
    -File $Installer `
    -ProjectRoot $ProjectRoot

Expected marker:

ZIP MEMBER SAFETY: PASS
INSTALL OK: brick-wall-comprehensive-quality-gate-prompt-registration-v1r2

The installer now:

    validates ZIP members before extraction;

    rejects traversal, absolute paths, duplicates, and case collisions;

    validates every manifest path independently;

    proves source, target, and backup containment;

    checks exact baseline hashes;

    creates backups;

    rolls changed files back if installation fails;

    regenerates startup files;

    stages all four Error Memory lessons for human review.

2. Validate, then prepare freeze

Run these in one PowerShell session. Freeze preparation runs only after validation returns success.

$ProjectRoot = "E:\kanda_reasoner"
$Validator = "C:\Path\To\brick_wall_v1r2_VALIDATE.ps1"
$FreezePrep = "C:\Path\To\brick_wall_v1r2_FREEZE.ps1"

powershell -NoProfile -ExecutionPolicy Bypass `
    -File $Validator `
    -ProjectRoot $ProjectRoot

if ($LASTEXITCODE -ne 0) {
    throw "Brick Wall validation failed. Freeze preparation was blocked."
}

powershell -NoProfile -ExecutionPolicy Bypass `
    -File $FreezePrep `
    -ProjectRoot $ProjectRoot

Required validation markers include:

ZIP CONTRACT: PASS
BRICK_WALL_MANIFEST_PATH_SET: PASS
BRICK_WALL_INSTALLER_ZIP_MEMBER_PREVALIDATION: PASS
BRICK_WALL_INSTALLER_ROLLBACK_GUARD: PASS
BRICK_WALL_MANIFEST_PATH_CONTAINMENT: PASS
BRICK_WALL_DURABLE_EVIDENCE_CONTRACT: PASS
BRICK_WALL_FREEZE_EXACT_PATCH_GUARD: PASS
BRICK_WALL_ERROR_LESSON_SCHEMA: PASS
BRICK_WALL_DELIVERY_CONTRACT: PASS
BRICK_WALL_PROMPT_BODY: PASS
BRICK_WALL_MACHINE_ROUTING: PASS
BRICK_WALL_HUMAN_ROUTING: PASS
BRICK_WALL_STARTUP_GENERATED_ARTIFACT: PASS
BRICK_WALL_DURABLE_VALIDATION_EVIDENCE: PASS
VALIDATION OK: brick-wall-comprehensive-quality-gate-prompt-registration-v1r2
STATUS: IN_SYNC

Required freeze-preparation markers:

FREEZE_HINT_SCAN: PASS
FREEZE_HINT_EVIDENCE_MERGE_OK: brick-wall-comprehensive-quality-gate-prompt-registration-v1r2
FREEZE HINT MERGE OK: brick-wall-comprehensive-quality-gate-prompt-registration-v1r2
STATUS: IN_SYNC

3. Human freeze

After all markers pass:

Freeze Feature After Update
-> New Local Freeze Entry
-> Preview
-> review the current feature and evidence
-> Confirm and Write

The scripts do not write frozen memory automatically.
4. Error Memory

The installer stages these lessons in the active project’s pending AI-assisted Error Memory intake:

    Startup validator incorrectly assumed a loose generated navigation file.

    Installer omitted ZIP-member prevalidation.

    Validation evidence was stored only in daily-work.

    Manifest paths were not independently contained under their owner roots.

They remain pending until reviewed and explicitly accepted in the Error Memory interface.

After running the commands, provide the complete terminal output and write:

Brick Wall

That will update Q40, local validation, freeze, and Error Memory status.


