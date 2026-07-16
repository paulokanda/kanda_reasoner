# HANDOFF — Brick Wall Comprehensive Quality Gate

## Document identity

```text
Feature name:
Brick Wall Comprehensive Quality Gate

Canonical prompt ID:
brick_wall_comprehensive_quality_gate

Prompt code:
KPR-03-001

Prompt type:
Routed governance prompt

Canonical owner:
kanda_prompt_workspace/prompt_library/
ACTIVE_PROMPTS/03_governance_freeze_and_handoff

Primary responsibility:
Display, maintain, and enforce the live Q01–Q40 KANDA Reasoner quality checklist throughout governed work.

Activation phrase:
Brick Wall
```

## Current implementation state

```text
Prompt design: COMPLETE
Q01–Q40 checklist design: COMPLETE
Prompt Library registration package: COMPLETE
Human routing registration: COMPLETE
Machine routing registration: COMPLETE
Startup bridge preparation: COMPLETE
Focused validator preparation: COMPLETE
Freezeable patch ZIP preparation: COMPLETE
Sandbox ZIP validation: COMPLETE
Sandbox source-baseline validation: COMPLETE
Windows project installation: PENDING
User-local validation: PENDING
Freeze Preview: PENDING
Freeze Confirm and Write: PENDING
Error Memory lesson human review: PENDING
```

Brick Wall must not be described as fully installed, locally validated, frozen, or memorized until those remaining human-local phases are completed.

---

# 1. What Brick Wall is

Brick Wall is the visible, persistent quality-control surface for KANDA Reasoner work.

Whenever the user says:

```text
Brick Wall
```

the AI must display the current implementation status and the complete Q01–Q40 quality ledger.

Brick Wall exists to prevent future AIs from forgetting required governance steps during long implementation conversations.

It must show:

* what has already been completed;
* what is currently being worked on;
* what remains pending;
* what has become stale;
* what is blocked;
* which evidence supports each completed item;
* whether coding is authorized;
* whether writing source is authorized;
* whether patch delivery is authorized;
* whether validation may be claimed;
* whether freeze is authorized;
* the next safe action.

Brick Wall is not merely a checklist shown once. It is a live implementation state record.

---

# 2. What Brick Wall is not

Brick Wall does not replace any owner canon or specialist workflow.

It does not replace:

* compact Error Memory;
* full Error Memory when escalation is required;
* exact-source inspection;
* Tool-versus-Project classification;
* Box Architecture;
* NO_LEAK_LOGIC_V1;
* MCard lifecycle;
* patch ZIP contract validation;
* user-local validation;
* Freeze Preview;
* Confirm and Write;
* Error Memory human review.

Brick Wall coordinates and exposes these safeguards. It does not become their implementation owner.

The general Tool-versus-Project boundary remains owned by `project_tool_boundary_canon`. Box responsibilities and public contracts remain governed by Box Architecture. MCard remains the specialist lifecycle for Architecture Review and large-file refactoring.

---

# 3. Why Brick Wall is necessary

KANDA Reasoner has accumulated several strong governance mechanisms:

* Error Memory;
* Freeze Memory;
* Tool-versus-Project protection;
* Box Architecture;
* NO_LEAK logic;
* MCard;
* startup routing;
* patch validation;
* source freshness;
* confirmation gates;
* external project-support ownership.

The risk is no longer only the absence of protections.

The major risk is that a future AI may:

* forget one protection;
* apply it too late;
* treat it as optional;
* assume it was completed in a prior chat;
* fail to reset it when source changes;
* mark it complete without evidence;
* begin coding before Error Memory and exact source are inspected;
* deliver a patch before the final ZIP is validated;
* freeze before local validation;
* forget to create a regression obligation from a known error.

Brick Wall prevents this by making every critical obligation visible and stateful.

---

# 4. Core operating rule

The mandatory implementation sequence is:

```text
STARTUP
-> PROJECT READY
-> TASK CLASSIFICATION
-> VERIFIED PROBLEM
-> ERROR MEMORY FIRST
-> ERROR REGRESSION MATRIX
-> EXACT SOURCE
-> TOOL/PROJECT IDENTITY
-> BOX BOUNDARY
-> NO-LEAK CHECK
-> MCARD, WHEN APPLICABLE
-> OPERATION IDENTITY
-> WRITE AUTHORIZATION
-> SOURCE FRESHNESS
-> VALIDATOR COVERAGE MAP
-> REGRESSION PLAN
-> PRE-CODE AUTHORIZATION
-> IMPLEMENT
-> VALIDATE
-> USER-LOCAL VALIDATION
-> DELIVER
-> FREEZE PREPARATION
-> HUMAN PREVIEW
-> CONFIRM AND WRITE
-> ERROR MEMORY REVIEW
-> FINAL HANDOFF
```

Hard coding rule:

```text
Error Memory incomplete
or exact source incomplete
or Tool/Project unresolved
or Box Boundary unresolved
or regression plan incomplete
= MAY BEGIN CODING: NO
```

Hard delivery rule:

```text
Exact final ZIP contract not passed
= MAY DELIVER PATCH: NO
```

Hard freeze rule:

```text
User-local validation absent
or human confirmation absent
= MAY FREEZE: NO
```

---

# 5. Status markers

Brick Wall must use these markers consistently:

```text
[ ] Pending
[~] In progress
[x] Completed and verified
[!] Blocked
[?] Unresolved or insufficient evidence
[N/A] Not applicable — reason required
```

An item may be marked `[x]` only when evidence exists.

It must not be marked complete because:

* it was discussed;
* a prior AI said it was complete;
* a filename suggests it exists;
* a generated report claims success;
* a canon describes desired behavior;
* the current source has not been inspected;
* validation was planned but not run.

---

# 6. Brick Wall activation behavior

When the user invokes:

```text
Brick Wall
```

the AI must perform the following sequence.

## Step 1 — Load current conversation state

Identify:

* current task;
* current phase;
* project slug;
* Tool root;
* active project root;
* selected target;
* source version or fingerprint;
* latest validation evidence;
* latest patch ZIP;
* current freeze state;
* relevant Error Memory state.

## Step 2 — Reset stale items

Freshness-sensitive checks must return to pending or unresolved when any of these changes:

* source archive;
* exact source;
* active project;
* selected target;
* operation generation;
* patch ZIP contents;
* validation evidence;
* freeze evidence;
* Error Memory export;
* handoff generation;
* user requirements.

Example:

```text
Previous source inspection: [x]
New source uploaded: YES

Updated status:
Exact-source baseline: [ ]
Source freshness: [?]
Regression map: [ ]
Validation plan: [ ]
```

## Step 3 — Display the live dashboard

```text
BRICK WALL STATUS

Project slug:
Current task:
Current phase:
Primary box:

Tool source root:
Active project root:
Project support root:
Daily-work root:
Selected target:

Verified-problem status:
Error Memory status:
Exact-source status:
Tool/Project status:
Box Boundary status:
NO-LEAK status:
MCard status:
Regression status:
Validation status:
Patch status:
Freeze status:
Error Memory promotion status:

May begin coding:
May write source:
May deliver patch:
May claim validation passed:
May freeze:

Current blockers:
Next safe action:
```

## Step 4 — Display Q01–Q40

Every requirement must be shown with:

* status;
* evidence;
* blocker or reason;
* next required action where incomplete.

## Step 5 — State authorization honestly

Brick Wall must explicitly state:

```text
MAY BEGIN CODING: YES / NO
MAY WRITE SOURCE: YES / NO
MAY BUILD PATCH: YES / NO
MAY DELIVER PATCH: YES / NO
MAY CLAIM VALIDATION PASSED: YES / NO
MAY FREEZE: YES / NO
```

---

# 7. Full Q01–Q40 implementation requirements

## Q01 — Verified-problem admission gate

### Purpose

Prevent speculative expansion and duplicated systems.

### Implementation

Before accepting new implementation work, record:

* the concrete problem;
* evidence;
* practical impact;
* existing KANDA capabilities;
* why the existing capability is insufficient;
* duplication risk;
* expected measurable gain.

### Exit condition

```text
Verified problem established: YES
```

Otherwise:

```text
MAY BEGIN CODING: NO
```

---

## Q02 — Visible Error Memory preflight

### Purpose

Ensure previous failures are reviewed before code is designed.

### Implementation

Before coding:

* load compact Error Memory;
* identify relevant lesson IDs;
* classify each match;
* state avoidance rules;
* decide whether full Error Memory is required.

### Exit condition

A visible `ERROR MEMORY CHECK` is present.

---

## Q03 — Error Memory regression-obligation matrix

### Purpose

Prevent lessons from remaining advisory prose.

### Implementation

Every relevant lesson must map to one of:

* existing validator;
* new regression test;
* justified non-applicability;
* stale/partial reinterpretation requirement.

### Exit condition

No relevant lesson remains without an executable or explicit disposition.

---

## Q04 — Lesson freshness verification

### Purpose

Prevent stale Error Memory from controlling current architecture incorrectly.

### Implementation

Check:

* file existence;
* symbol existence;
* current facade;
* current box;
* source fingerprint;
* lesson status;
* `superseded_by`;
* invalidation conditions.

---

## Q05 — Exact-source baseline

### Purpose

Make current source the implementation authority.

### Implementation

Inspect:

* owner files;
* public facade;
* private implementations;
* consumers;
* imports and exports;
* validators;
* state ownership;
* path ownership;
* current hashes;
* accepted behavior.

No implementation may rely only on handoffs or generated artifacts.

---

## Q06 — Tool-versus-Project identity enforcement

### Purpose

Prevent self-hosting from collapsing logical ownership.

### Implementation

Resolve separately:

```text
tool_source_root
active_project_root
active_project_support_root
active_project_daily_work_root
```

Even if physical paths overlap, ownership must remain logically distinct.

---

## Q07 — Visible Tool/Project and NO-LEAK classification

### Purpose

Make artifact ownership explicit.

### Implementation

Classify every affected artifact as:

* Tool source;
* active-project source;
* project support;
* Preview;
* transaction evidence;
* Error Memory;
* Freeze Memory;
* handoff output;
* daily-work;
* Shadow;
* external;
* out of scope.

---

## Q08 — Box Boundary Audit

### Purpose

Prevent local fixes from contaminating other boxes.

### Implementation

Declare:

* one primary box;
* responsibility;
* owner paths;
* public contract;
* private internals;
* state owner;
* dependencies;
* supporting touches;
* contamination risks;
* validation scope.

---

## Q09 — Public-contract-only communication

### Purpose

Prevent private reach-in and accidental ownership changes.

### Implementation

Cross-box use must occur through:

* public facade;
* explicit contract;
* controller route;
* command;
* event;
* bridge;
* adapter.

Private imports and private mutation across boxes are prohibited.

---

## Q10 — Single mutable-state owner

### Purpose

Prevent hidden shared state and conflicting mutation.

### Implementation

For each mutable state:

* name one owner;
* declare readers;
* declare authorized mutators;
* declare invalidation rules.

---

## Q11 — MCard lifecycle enforcement

### Purpose

Govern Architecture Review, Planner, Preview, Apply, rollback, receipt, and eject.

### Implementation

Use the MCard state model:

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

Rollback:

```text
APPLYING
-> ROLLBACK_REQUESTED
-> ROLLBACK_VERIFIED
-> CARD_EJECTED
```

Use `[N/A]` with reason when the task does not involve MCard.

---

## Q12 — Immutable operation identity

### Purpose

Prevent root, target, hash, generation, and transaction values from becoming inconsistent.

### Implementation target

One protected operation identity should contain:

* Tool root;
* active project;
* target relative path;
* source fingerprint;
* lifecycle generation;
* operation ID;
* transaction ID where applicable.

The exact source must be audited before deciding whether a new object is necessary.

---

## Q13 — Explicit write authorization

### Purpose

Prevent a path or helper function from implicitly granting mutation authority.

### Implementation target

Mutation must require explicit current authority tied to:

* operation;
* active project;
* allowed paths;
* approved Preview;
* expected source hashes;
* generation;
* transaction.

---

## Q14 — Immediate pre-write freshness check

### Purpose

Prevent writing from stale Preview or stale Planner state.

### Implementation

Immediately before mutation verify:

* project unchanged;
* target unchanged;
* generation unchanged;
* transaction unchanged;
* Preview current;
* source fingerprint unchanged;
* destination ownership unchanged.

Failure must block writing.

---

## Q15 — Canonical path-authority contract

### Purpose

Prevent duplicate or contradictory root formulas.

### Implementation

Use one public owner for deriving:

* support root;
* daily-work root;
* Preview;
* Shadow;
* Error Memory;
* Freeze Memory;
* handoff paths.

---

## Q16 — Resolved-path containment

### Purpose

Prevent traversal, sibling-prefix confusion, drive escape, and junction/symlink escape.

### Implementation

Containment must be structural, not string-prefix based.

Test:

* `..`;
* sibling paths;
* different drives;
* UNC;
* junctions/symlinks;
* Windows case normalization;
* ambiguous paths.

---

## Q17 — Preview, Shadow, and source separation

### Purpose

Protect durable truth.

### Implementation

```text
Final source:
active_project_root

Durable Preview and transaction truth:
active_project_support_root

Shadow and disposable staging:
active_project_daily_work_root
```

Daily-work must never own canonical truth.

---

## Q18 — Stale asynchronous-result rejection

### Purpose

Prevent old workers from repopulating new project or target state.

### Implementation

Worker request and result identity must include:

* operation;
* project;
* target;
* hash;
* generation.

The receiver must reject mismatched results.

Cancellation alone is insufficient.

---

## Q19 — Real Qt/QSignalSpy validation decision

### Purpose

Ensure real queued-signal and thread-affinity behavior is validated where mocks are insufficient.

### Implementation

For relevant Qt work, decide whether to use:

* real controller;
* real widget;
* `QSignalSpy`;
* queued signal;
* actual stale-result arrival.

---

## Q20 — Shared isolated filesystem fixtures

### Purpose

Prevent validators from writing into real production roots.

### Implementation

Synthetic Tool, project, support, daily-work, Preview, Shadow, Error Memory, and Freeze Memory roots must be isolated.

Production formulas may be tested read-only.

---

## Q21 — Parametrized negative boundary matrix

### Purpose

Prevent one-off validation gaps.

### Required cases where applicable

* self-hosting;
* external project;
* same drive;
* different drive;
* target outside root;
* traversal;
* sibling prefix;
* UNC;
* case collision;
* stale generation;
* stale hash;
* transaction lock;
* Preview/Shadow confusion;
* confirmation bypass.

---

## Q22 — Public-facade and contract-drift tests

### Purpose

Protect package and box public surfaces.

### Implementation

Test:

* documented imports;
* exported symbols;
* signatures;
* fallback behavior;
* optional dependency absence;
* private implementation independence.

---

## Q23 — Deterministic MCard transition tests

### Purpose

Turn the MCard lifecycle into executable protection.

### Implementation

Test all valid and invalid transitions, locks, rollback, eject, project switch, target switch, and self-hosting.

---

## Q24 — Property-based MCard pilot decision

### Purpose

Explore unexpected state sequences after deterministic tests exist.

### Implementation rule

Hypothesis or similar testing is a pilot, not a mandatory global dependency.

Adopt more broadly only if it finds meaningful defects.

---

## Q25 — Mutation-testing pilot decision

### Purpose

Verify critical guards are truly protected by tests.

### Implementation rule

Apply only to selected critical validators.

Do not run full-project mutation testing by default.

---

## Q26 — ZIP containment and collision hardening

### Purpose

Prevent unsafe delivery archives.

### Required protections

Reject:

* absolute paths;
* drive-qualified paths;
* UNC paths;
* traversal;
* duplicate members;
* Windows case-fold collisions;
* file/directory collisions;
* unexpected symlinks;
* undeclared install paths.

The exact final downloadable ZIP must pass the contract validator.

---

## Q27 — Control-byte and encoding guards

### Purpose

Prevent operational-script and evidence corruption.

### Implementation

Test:

* UTF-8 output;
* BOM-aware legacy reads where required;
* UTF-16LE fixtures;
* hidden vertical tab/control bytes;
* safe Windows path generation.

---

## Q28 — Structured exception provenance

### Purpose

Improve Error Memory and debugging quality.

### Implementation

Preserve:

* original cause;
* operation phase;
* operation ID;
* target;
* root classification;
* last successful marker;
* distinction between setup, behavior, cleanup, and evidence failure.

---

## Q29 — No-Leak runtime trace pilot decision

### Purpose

Detect hidden side effects during high-risk validation.

### Possible observed actions

* writes;
* deletes;
* replacements;
* archive operations;
* subprocesses;
* imports.

This is validation observability, not a security sandbox.

---

## Q30 — Human confirmation and freeze protection

### Purpose

Prevent automated canonical writes without human review.

### Implementation

Preserve:

* read-only Preview;
* explicit Confirm and Write;
* no automatic Error Memory promotion;
* no automatic Freeze Memory write;
* confirmation invalidation after source or target change.

---

## Q31 — Changed-file-to-validator coverage map

### Purpose

Ensure every changed file has appropriate validation.

### Implementation

Map each file to:

* owner box;
* public contract;
* Error Memory lessons;
* frozen behavior;
* focused tests;
* boundary tests;
* GUI tests;
* delivery tests;
* negative tests.

---

## Q32 — Validation and evidence provenance

### Purpose

Prevent stale evidence from appearing current.

### Implementation

Record:

* project;
* root;
* source hashes;
* operation;
* lesson IDs;
* Error Memory export;
* prompt version;
* validation command;
* validator version;
* date;
* environment;
* markers;
* limitations.

---

## Q33 — Pinned local-model provenance

### Purpose

Make AI-assisted results reproducible when local models are used.

### Implementation

Record:

* model ID;
* exact revision;
* tokenizer revision;
* prompt hash;
* inference settings;
* offline/local mode;
* input fingerprints;
* output hash.

Unpinned AI output remains advisory.

---

## Q34 — Profile-before-optimization gate

### Purpose

Prevent speculative performance complexity.

### Implementation

Require:

* named slow path;
* workload;
* baseline;
* repeated runs;
* variance;
* bottleneck classification;
* expected improvement;
* acceptable complexity.

---

## Q35 — Focused performance baseline

### Purpose

Measure only real bottlenecks.

### Implementation

Benchmarks should remain local to the owning box unless a broader framework is demonstrably necessary.

---

## Q36 — Module-size and cohesion enforcement

### Purpose

Prevent unmaintainable large modules.

### Implementation

* touched Python modules must not exceed the governed limit;
* formatting compression is forbidden;
* helpers must be split by responsibility;
* public facades should remain small.

---

## Q37 — Canonical ownership reconciliation

### Purpose

Consolidate duplicated existing systems safely.

### Implementation

Identify:

* duplicate scanners;
* duplicate schemas;
* duplicate reports;
* duplicate state owners;
* duplicate consumers.

Select one canonical owner per responsibility.

Do not create a new super-system merely to coordinate duplicates.

---

## Q38 — Handoff freshness and provenance

### Purpose

Prevent AI handoff artifacts from being mistaken for current source.

### Implementation

Check:

* generation time;
* source fingerprint;
* manifest freshness;
* validation freshness;
* Error Memory freshness;
* Freeze context freshness.

---

## Q39 — Task-specific context admission test

### Purpose

Prevent creation of another context or intelligence system without evidence.

### Implementation

Before building a new context summary, prove current handoff failure through controlled task comparison.

Prefer strengthening current manifests and routes.

---

## Q40 — One-primary-box governed release

### Purpose

Keep patches small, attributable, and independently verifiable.

### Implementation

Every release must declare:

* one primary box;
* supporting touches;
* changed files;
* source baseline;
* regression obligations;
* validation map;
* exact ZIP contract;
* freeze evidence;
* human-local validation state.

---

# 8. Brick Wall implementation phases

## Phase 1 — Canonical prompt creation

### Required implementation

Create:

```text
brick_wall_comprehensive_quality_gate.md
```

The prompt must define:

* activation phrase;
* dashboard format;
* status markers;
* Q01–Q40 ledger;
* freshness-reset behavior;
* authorization outputs;
* stop conditions;
* next-safe-action behavior.

### Exit criteria

* prompt body validated;
* no duplicate equivalent prompt exists;
* canonical owner selected.

---

## Phase 2 — Prompt metadata

### Required implementation

Create the prompt metadata record containing:

* prompt ID;
* title;
* prompt code;
* status;
* load type;
* owner group;
* purpose;
* trigger terms;
* routing aliases;
* applicable tasks.

### Exit criteria

* identity matches prompt body;
* load type is routed;
* no competing prompt code exists.

---

## Phase 3 — Human routing registration

### Required implementation

Register Brick Wall in:

* folder assimilation card;
* human prompt navigation index;
* group assimilation index;
* relevant governance routing documentation.

### Trigger requirements

The exact phrase:

```text
Brick Wall
```

must resolve to the canonical prompt.

Related natural-language requests may include:

* show the complete quality checklist;
* where are we in implementation;
* show Q01–Q40;
* show current blockers;
* check coding authorization;
* check freeze readiness.

---

## Phase 4 — Machine routing registration

### Required implementation

Update:

* prompt navigation JSON;
* group assimilation JSON;
* route coverage CSV;
* metadata index where applicable.

### Exit criteria

Human and machine routing must resolve to the same canonical prompt.

---

## Phase 5 — Startup bridge

### Required implementation

Add a compact startup bridge that informs future AIs:

* Brick Wall exists;
* it is routed;
* it must be invoked when requested;
* it does not replace specialist canons;
* the full Q01–Q40 body need not be loaded in every startup unless invoked.

### Reason

The user requires the protection to persist across chats, but loading the complete prompt at every startup could unnecessarily expand context.

The startup bridge provides awareness; the routed prompt provides the full checklist.

---

## Phase 6 — Focused validator

### Required validation

Verify:

* prompt file exists;
* metadata exists;
* prompt ID matches;
* prompt code matches;
* owner group matches;
* status is active;
* routing indexes contain the prompt;
* JSON routing contains the prompt;
* CSV coverage contains the route;
* startup bridge mentions Brick Wall;
* all Q01–Q40 markers exist;
* authorization outputs exist;
* freshness-reset rule exists;
* stop conditions exist.

### Required markers

```text
BRICK_WALL_PROMPT_BODY: PASS
BRICK_WALL_METADATA_IDENTITY: PASS
BRICK_WALL_FOLDER_REGISTRATION: PASS
BRICK_WALL_MACHINE_ROUTING: PASS
BRICK_WALL_HUMAN_ROUTING: PASS
BRICK_WALL_ROUTE_COVERAGE_TABLE: PASS
BRICK_WALL_STARTUP_ROUTE_BRIDGE: PASS
VALIDATION OK: <feature_id>
STATUS: IN_SYNC
```

---

## Phase 7 — Freezeable patch ZIP

The patch delivery follows the governed answer/install/validate/freeze/error routine. The wrapper prompt defines that a freezeable patch must contain the patch ZIP, Windows installation flow, validation-before-freeze behavior, freeze evidence preparation, and evidence-backed Error Memory intake when a real error occurred.

### Required ZIP contents

```text
INSTALL.ps1
VALIDATE.ps1
FREEZE.ps1
PATCH_README.txt
KANDA_FREEZE_HINT.json
PATCH_MANIFEST.json
tools/<focused_validator>.py
updated source files
Error Memory lesson intake when applicable
```

### ZIP contract

The exact downloadable ZIP must be validated.

Required marker:

```text
ZIP CONTRACT: PASS
```

If not:

```text
CONTRACT NOT MET - PATCH DELIVERY BLOCKED
```

---

## Phase 8 — Windows installation

### Required flow

The user places the ZIP at the project drive root.

The installation block must:

1. resolve `PROJECT_ROOT`;
2. derive project name;
3. derive drive root;
4. derive project daily-work root;
5. find the ZIP at the drive root;
6. stage it into daily-work;
7. confirm staging;
8. remove the drive-root copy;
9. inspect ZIP members;
10. extract only from the staged ZIP;
11. run `INSTALL.ps1`.

### Prohibitions

Do not:

* require the user to extract an outer bundle first;
* search Downloads or Desktop;
* install from the root-drive ZIP;
* leave the root-drive ZIP behind;
* place transient install files in project source;
* hard-code daily-work for KANDA regardless of selected project.

---

## Phase 9 — User-local validation

Install success is not validation.

The validation phase must run from the extracted daily-work patch.

It must verify:

* exact final ZIP;
* installed files;
* source hashes;
* routing;
* metadata;
* startup regeneration;
* no project-root freeze hint;
* durable validation evidence;
* Error Memory intake staging;
* no support-root leakage;
* no unexpected source changes.

Required markers include:

```text
ZIP CONTRACT: PASS
VALIDATION OK: <feature_id>
STATUS: IN_SYNC
```

Validation failure must block freeze.

---

## Phase 10 — Freeze evidence preparation

Freeze preparation may run only after validation succeeds.

It must:

* locate current freeze hint;
* merge real validation evidence;
* preserve project-specific support ownership;
* avoid manually mutating frozen memory;
* avoid creating a freeze entry automatically.

Required markers:

```text
FREEZE_HINT_EVIDENCE_MERGE_OK: <feature_id>
FREEZE HINT MERGE OK: <feature_id>
STATUS: IN_SYNC
```

---

## Phase 11 — Human freeze

The human must use:

```text
Freeze Feature After Update
-> New Local Freeze Entry
-> Preview
-> review current evidence
-> Confirm and Write
```

Preview remains read-only.

Confirm and Write must remain explicit.

Brick Wall must not mark freeze complete before this human action is confirmed.

---

## Phase 12 — Error Memory

When a real error occurs during:

* planning;
* implementation;
* patch creation;
* installation;
* validation;
* freeze preparation;
* handoff;
* previous answer;

one evidence-backed Error Memory lesson should be staged.

The lesson must:

* use the active-ready template;
* contain exact evidence;
* include the wrong assumption;
* identify the correction;
* identify regression prevention;
* identify the source patch ZIP;
* include installation summary;
* include validation markers;
* be wrapped in the canonical begin/end markers;
* remain pending human review.

Brick Wall must report:

```text
Error Memory lesson staged: YES
Human reviewed: YES / NO
Memorized: YES / NO
```

A staged lesson is not a memorized lesson.

---

# 9. Errors already discovered during Brick Wall delivery

The Brick Wall process itself exposed useful failures.

## Error 1 — Loose startup artifact assumption

The validator assumed a generated navigation file would exist as a loose file, while the canonical generator packaged it inside the startup ZIP.

### Prevention

Validators must inspect the generator’s real artifact contract rather than assume output layout.

## Error 2 — Missing ZIP-member prevalidation

An early installer used archive extraction without first applying KANDA’s own member-name contract.

### Prevention

Inspect all ZIP member names before extraction.

## Error 3 — Durable evidence stored only in daily-work

Validation evidence was initially left only in disposable storage.

### Prevention

Durable validation evidence must be stored in project support; daily-work is transient only.

## Error 4 — Manifest containment incomplete

ZIP member names were validated, but manifest-defined paths were not independently proven to remain under their owner roots.

### Prevention

Validate both archive paths and manifest paths.

## Error 5 — Nonexistent extracted bundle assumption

The previous user-facing answer assumed:

```text
C:\KANDA_DELIVERIES\brick_wall_v1r2_all_in_one
```

already existed after extraction.

It did not.

### Prevention

Deliver one self-contained patch ZIP and provide root-drive staging code that requires no prior extracted bundle folder.

These lessons demonstrate the intended Brick Wall function: the quality gate must expose and correct its own delivery weaknesses before freeze.

---

# 10. Current Brick Wall Q01–Q40 status

This reflects the implementation package and conversation evidence, not yet user-local completion.

| ID  | Requirement                              |                          Current status |
| --- | ---------------------------------------- | --------------------------------------: |
| Q01 | Verified-problem gate                    |                                     [x] |
| Q02 | Visible Error Memory preflight           |                                     [x] |
| Q03 | Regression-obligation matrix             |                                     [x] |
| Q04 | Lesson freshness                         |                                     [x] |
| Q05 | Exact-source baseline                    |                                     [x] |
| Q06 | Tool/Project identity                    |                                     [x] |
| Q07 | Ownership and NO-LEAK classification     |                                     [x] |
| Q08 | Box Boundary Audit                       |                                     [x] |
| Q09 | Public-contract-only communication       |                                     [x] |
| Q10 | Single mutable-state owner               |              [N/A] No new runtime state |
| Q11 | MCard lifecycle                          |                 [N/A] Not an MCard task |
| Q12 | Immutable operation identity             |  [N/A] No runtime operation model added |
| Q13 | Explicit write authorization             | [x] Governed manifest and human install |
| Q14 | Pre-write freshness                      |            [x] Baseline hashes required |
| Q15 | Canonical path authority                 |                                     [x] |
| Q16 | Structural containment                   |                                     [x] |
| Q17 | Preview/Shadow/source separation         |                                     [x] |
| Q18 | Stale async-result rejection             |                     [N/A] No async work |
| Q19 | Real Qt validation                       |                      [N/A] No Qt change |
| Q20 | Isolated fixtures                        |                                     [x] |
| Q21 | Negative boundary matrix                 |                                     [x] |
| Q22 | Facade and contract tests                |                                     [x] |
| Q23 | MCard transition tests                   |                                   [N/A] |
| Q24 | Property-based pilot                     |                                   [N/A] |
| Q25 | Mutation-testing pilot                   |                                   [N/A] |
| Q26 | ZIP hardening                            |                                     [x] |
| Q27 | Encoding/control-byte guards             |                                     [x] |
| Q28 | Structured error provenance              |                                     [x] |
| Q29 | Runtime No-Leak trace                    |                                   [N/A] |
| Q30 | Human confirmation and freeze safeguards |                     [x] Design complete |
| Q31 | Changed-file validation map              |                                     [x] |
| Q32 | Evidence provenance                      |                                     [x] |
| Q33 | Local-model provenance                   |                                   [N/A] |
| Q34 | Profile-before-optimization              |                                   [N/A] |
| Q35 | Performance baseline                     |                                   [N/A] |
| Q36 | Module-size enforcement                  |                                     [x] |
| Q37 | Ownership reconciliation                 |                                     [x] |
| Q38 | Handoff freshness                        |                                     [x] |
| Q39 | Context-summary admission test           |             [N/A] No new context engine |
| Q40 | One-box governed release                 | [~] Local validation and freeze pending |

---

# 11. Current blockers

```text
[ ] Install v1r3 on E:\kanda_reasoner
[ ] Run user-local VALIDATE.ps1
[ ] Confirm all expected validation markers
[ ] Run FREEZE.ps1 evidence merge
[ ] Review Freeze Preview
[ ] Use Confirm and Write
[ ] Review staged Error Memory lesson
[ ] Approve or reject memorization
```

Current authorization:

```text
May continue implementation planning: YES
May install patch locally: YES
May claim local validation passed: NO
May claim frozen: NO
May claim Error Memory memorized: NO
```

---

# 12. Files expected in the implementation

## Prompt Library source

```text
kanda_prompt_workspace/prompt_library/
ACTIVE_PROMPTS/03_governance_freeze_and_handoff/
brick_wall_comprehensive_quality_gate.md
```

## Metadata

```text
kanda_prompt_workspace/prompt_library/
METADATA/
brick_wall_comprehensive_quality_gate.meta.json
```

## Human routing

```text
ACTIVE_PROMPTS/02_prompt_routing_and_indexing/
prompt_navigation_index.md

ACTIVE_PROMPTS/03_governance_freeze_and_handoff/
_FOLDER_ASSIMILATION.md

ROUTING/PROMPT_NAVIGATION_INDEX.md
ROUTING/GROUP_ASSIMILATION_INDEX.md
```

## Machine routing

```text
ROUTING/prompt_navigation_index.json
ROUTING/group_assimilation_index.json
ROUTING/prompt_route_coverage_table.csv
```

## Validator

```text
tools/validate_brick_wall_prompt_registration_v1.py
```

## Patch delivery

```text
INSTALL.ps1
VALIDATE.ps1
FREEZE.ps1
PATCH_README.txt
PATCH_MANIFEST.json
KANDA_FREEZE_HINT.json
```

---

# 13. Brick Wall response shape for future AIs

When invoked, respond using this structure:

```text
# BRICK WALL STATUS

## Current work
Project:
Task:
Phase:
Primary box:
Target:
Source freshness:

## Authorization
May begin coding:
May write source:
May build patch:
May deliver patch:
May claim validation:
May freeze:

## Current blockers
- ...

## Next safe action
...

## Q01–Q40 ledger
| ID | Requirement | Status | Evidence / blocker |

## Changes since last Brick Wall
- newly completed:
- reset due to freshness:
- newly blocked:
- no longer applicable:

## Evidence
- Error Memory:
- exact source:
- validation:
- patch:
- freeze:
- handoff:
```

The response must be operational, not ceremonial.

---

# 14. Handoff instructions to the next AI

The next AI must:

1. Recognize `Brick Wall` as an explicit governance command.
2. Display the Q01–Q40 ledger.
3. Preserve statuses only when evidence remains current.
4. Reset source-sensitive checks after any new source upload or patch revision.
5. Keep coding blocked until mandatory pre-code gates pass.
6. Keep patch delivery blocked until the exact final ZIP passes.
7. Keep freeze blocked until user-local validation and explicit confirmation.
8. Never infer Error Memory memorization from staging.
9. Never infer freeze completion from freeze evidence merge.
10. Never replace specialist canons with Brick Wall.
11. Never collapse Tool and Project identities during self-hosting.
12. Never allow daily-work to own durable truth.
13. Always show the next safe action.
14. Always state remaining blockers honestly.

---

# 15. Final implementation acceptance criteria

Brick Wall implementation is fully complete only when all of the following are true:

```text
[x] Canonical prompt exists
[x] Metadata exists
[x] Human routing exists
[x] Machine routing exists
[x] Startup bridge exists
[x] Q01–Q40 body validated
[x] Focused validator passes in sandbox
[x] Exact final patch ZIP contract passes
[ ] Patch installed on the active Windows project
[ ] User-local validation passes
[ ] Durable evidence exists under project support
[ ] Freeze evidence merge passes
[ ] Freeze Preview reviewed
[ ] Confirm and Write completed
[ ] Error Memory lesson reviewed
[ ] Approved lesson memorized or explicitly rejected
[ ] Final handoff updated with frozen status
```

Until all remaining items are completed:

```text
BRICK WALL IMPLEMENTATION STATUS:
SOURCE AND DELIVERY PACKAGE COMPLETE
LOCAL INSTALLATION AND GOVERNED FINALIZATION PENDING
```

---

# 16. Final compact definition

```text
Brick Wall is the routed, visible, continuously updated Q01–Q40 quality gate for KANDA Reasoner.

It shows where implementation currently stands, what evidence exists, what is blocked, what must be reset after source changes, and whether coding, writing, patch delivery, validation claims, and freeze are authorized.

Brick Wall coordinates Error Memory, exact-source inspection, Tool/Project boundaries, Box Architecture, NO_LEAK_LOGIC_V1, MCard, regression protection, validation, delivery, freeze, and handoff.

It does not replace those systems.

When the user says "Brick Wall", the AI must display and update the live ledger immediately.
```
