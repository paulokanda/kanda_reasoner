---
prompt_code: KPR-03-001
prompt_id: brick_wall_comprehensive_quality_gate
title: Brick Wall - Comprehensive Quality Gate
version: 3.23
status: active
load_type: routed
owner_group: 03_governance_freeze_and_handoff
owner_box: Context Routing and Governance Layer
---
# Brick Wall - Comprehensive Quality Gate
## Purpose
Brick Wall is the mandatory evidence-tracked checkpoint for governed KANDA Reasoner work. It exposes Error Memory, exact source, Tool/Project, Box/NO-LEAK, MCard, regression, validation, delivery, freeze, and handoff status while specialist owner canons remain authoritative.
## Invocation
Load this prompt when the user says or clearly requests:
```text
brick wall | show brick wall | brick wall check | update brick wall
where are we on brick wall
run the quality wall
```
## When to use
Use for governed implementation, repair, refactor, validation, delivery, freeze, Error Memory, architecture, startup, handoff, or quality work; reuse it as evidence changes.
## When not to use
Do not use for unrelated or explanation-only work. Brick Wall never permits skipping exact source, specialist prompts, validation, user confirmation, or freeze gates.
## Source authority and persistence rules
1. Current exact source is implementation truth; Error Memory is prevention guidance, not source truth. 2. Generated handoff, validation, freeze, and routing artifacts require freshness verification; across chats reset evidence-sensitive ticks unless current evidence proves them.
3. Within a chat update the live checklist after each completed step; quality-workflow changes update this canonical prompt through governed prompt-authoring and validation. 4. Never edit generated startup delivery copies as canonical source.
## Status markers
```text
[ ] pending
[~] in progress
[x] completed and verified
[!] blocked
[?] unresolved or insufficient evidence
[N/A] not applicable - reason required
```
An item may be marked `[x]` only when evidence exists.
## Mandatory response whenever Brick Wall is invoked
Return these sections in this order:
1. `BRICK WALL STATUS`; 2. `CURRENT BLOCKERS`
3. `Q01-Q40 LIVE COVERAGE LEDGER`; 4. `NEXT SAFE ACTION`
5. `AUTHORIZATION STATUS`
Do not begin with implementation code.
## BRICK WALL STATUS template
```text
BRICK WALL STATUS
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
```
## Hard stop rules
Coding remains blocked when any mandatory pre-code item is incomplete. Patch delivery remains blocked when the final ZIP contract, validator map, or evidence provenance is incomplete.
Freeze remains blocked without user-local validation and explicit human confirmation through governed Preview and Confirm and Write.
Required blocked output:
```text
MAY PROCEED: NO
Blocked by:
Required evidence:
Next safe action:
```
## Q01-Q40 live coverage ledger
The ledger must be displayed every time Brick Wall is invoked.
| ID | Requirement | Default status rule |
|---|---|---|
| Q01 | Verified-problem admission gate | Must prove a real inadequacy before new feature work |
| Q02 | Visible Error Memory preflight | Mandatory for KANDA Tool work; advisory/non-blocking for independent external Project work |
| Q03 | Error Memory regression-obligation matrix | Required when Q02 is governing; external Project Tool-context may be advisory/N/A |
| Q04 | Lesson freshness verification | Required when Q02 is governing; external Project Tool-context may be advisory/N/A |
| Q05 | Exact-source baseline | Inspect current owner files, contracts, consumers, validators, and freshness basis |
| Q06 | Tool/Project identity enforcement | Resolve reusable Tool and active project separately, including self-hosting |
| Q07 | Visible Tool/Project and NO-LEAK classification | Classify Tool source, project source, durable support, evidence, daily-work, and blocked writes |
| Q08 | Box Boundary Audit | One primary box, owner paths, public contract, private internals, dependencies, state owner |
| Q09 | Public-contract-only communication | No private reach-in or accidental package-root ownership |
| Q10 | Single mutable-state owner | Every mutable state has exactly one declared owner and mutation route |
| Q11 | MCard observer lifecycle enforcement | Apply insert-read-observe-analyze-report-eject when relevant; no Project apply/rollback |
| Q12 | Immutable operation identity | Audit or establish current Tool, project, target, hash, generation, operation, and transaction identity |
| Q13 | Explicit write authorization | A path or boolean alone must not authorize mutation |
| Q14 | Immediate pre-write freshness check | Recheck source, target, generation, transaction, Preview, and ownership immediately before write |
| Q15 | Canonical path-authority contract | One public owner derives support, daily-work, Preview, Shadow, Error Memory, and Freeze paths |
| Q16 | Resolved-path containment | Structural containment; reject traversal, sibling-prefix, drive, UNC, case, and link escape risks |
| Q17 | Preview, Shadow, and source separation | Final source, durable Preview, and transient Shadow must remain distinct authorities |
| Q18 | Stale asynchronous-result rejection | Result identity must match current project, target, hash, operation, and generation |
| Q19 | Real Qt/QSignalSpy validation decision | Use real Qt validation when queued signals or thread affinity are material |
| Q20 | Shared isolated filesystem fixtures | Synthetic validators must not mutate real source, support, or drive-root locations |
| Q21 | Parametrized negative boundary matrix | Cover self-hosting, external projects, paths, generations, transactions, and confirmation bypass |
| Q22 | Public-facade and contract-drift tests | Prove canonical imports, signatures, fallback, and no private dependency |
| Q23 | Deterministic MCard transition tests | Test valid and invalid transitions and durable-state preservation |
| Q24 | Property-based MCard pilot decision | Pilot only after deterministic state tests and demonstrated value |
| Q25 | Mutation-testing pilot decision | Limit to critical guards and expand only after measurable benefit |
| Q26 | ZIP containment and collision hardening | Reject dangerous paths, duplicates, case collisions, links, and undeclared payloads |
| Q27 | Control-byte and encoding guards | Protect PowerShell paths and validation evidence encodings |
| Q28 | Structured exception provenance | Preserve cause, phase, operation, target, root classification, and last marker |
| Q29 | NO-LEAK runtime trace pilot decision | Optional validation observability only; never claim a security sandbox |
| Q30 | Human confirmation and freeze protection | Preserve read-only Preview and explicit Confirm and Write |
| Q31 | Changed-file-to-validator coverage map | Explain why every validator applies or does not apply to each changed file |
| Q32 | Validation and evidence provenance | Record source fingerprints, lessons, prompt/validator revisions, commands, environment, and markers |
| Q33 | Pinned local-model provenance or N/A | Record exact model, tokenizer, code, prompt, settings, and offline mode when AI evidence is used |
| Q34 | Profile-before-optimization gate or N/A | No performance change without named workload and baseline |
| Q35 | Focused performance baseline or N/A | Benchmark only proven bottlenecks in the owning box |
| Q36 | Module-size and cohesion enforcement | Touched Python modules remain within governed limits or use large-module protocol |
| Q37 | Canonical ownership reconciliation or N/A | Remove competing owners, duplicate scanners, schemas, reports, and state authorities |
| Q38 | Handoff freshness and provenance | Verify handoff, source archive, validation, Error Memory, and freeze context freshness |
| Q39 | Task-specific context admission test or N/A | Build a new context summary only after controlled evidence proves current handoff inadequate |
| Q40 | One-primary-box governed release | One primary box, declared supporting touches, exact ZIP contract, honest validation and freeze state |
## Detailed mandatory checks
### Startup and project readiness
Startup/project readiness and active roots are known. Tool Error Memory and KANDA source-archive availability are KANDA-work evidence, not prerequisites for independent external Project development.
### Verified problem
Q01 is an admission decision, not a ceremonial checkbox. Before implementation
planning or coding, return this complete record:
```text
VERIFIED PROBLEM RECORD
Task classification:
Change type: NEW_FEATURE / REPAIR_EXISTING / CONSOLIDATE / VALIDATOR_ONLY / NO_CHANGE
Concrete problem:
Evidence:
Practical impact:
Existing KANDA capability inspected:
Why current capability is inadequate:
Duplication or parallel-owner risk:
Smallest adequate intervention:
Expected measurable gain:
Disconfirming evidence searched:
Admission decision: ADMIT / REPAIR_EXISTING / CONSOLIDATE / NO_CHANGE / BLOCK
May proceed to Error Memory preflight: YES / NO
```
Completion rules:
- Every field must contain current evidence or an explicit evidence-backed N/A.
- `Existing KANDA capability inspected` must name the current owner, public
  contract, validator, prompt, or workflow that was checked.
- `Why current capability is inadequate` must identify the observed gap; a
  preference for a new abstraction is not evidence.
- `Duplication or parallel-owner risk` must state whether the change would create
  another scanner, schema, state owner, report, context engine, or workflow.
- `Smallest adequate intervention` must prefer repairing or consolidating the
  current owner over creating a new owner.
- `Expected measurable gain` must describe an observable reliability, safety,
  correctness, usability, or maintainability outcome.
- Search for disconfirming evidence that the current capability may already be
  adequate.
- Use `NO_CHANGE` when the current capability is adequate.
- Use `BLOCK` when evidence is insufficient or ownership remains unresolved.
- Q01 may be `[x]` only when the record is complete and the admission decision is
  `ADMIT`, `REPAIR_EXISTING`, `CONSOLIDATE`, or evidence-backed `NO_CHANGE`.
- Coding remains blocked until Q02-Q17 phase-relevant pre-code gates also pass.
### Error Memory first
For KANDA Reasoner Tool implementation, read the current compact Error Memory
prompt, compact lesson export, and manifest before exact-source planning or coding.
For independent external `PROJECT_ACTOR` work, Tool Error Memory is advisory: use it
when available, but missing/stale Tool Error Memory does not block exact Project
source inspection, coding, testing, validation, or release. Then return the record
with an explicit governing/advisory scope:
```text
ERROR MEMORY CHECK
Project slug:
Compact export identity and freshness:
Relevant lesson IDs:
Confidence per match: exact / partial / weak / none
Lesson freshness:
Applicable avoidance rules:
Regression obligations:
ERROR MEMORY REGRESSION MATRIX
Repeat one block for every Relevant lesson ID. The Lesson ID set must match exactly.
Lesson ID:
Match confidence: exact / partial / weak
Freshness: current / stale / partial / unresolved
Disposition: EXISTING_VALIDATOR / NEW_FOCUSED_TEST / NOT_APPLICABLE / CURRENT_SOURCE_REINTERPRETATION
Protection owner:
Validator or test path:
Expected success marker:
Expected rejection marker:
Disposition reason:
Status: COMPLETE / BLOCKED
ERROR MEMORY LESSON FRESHNESS VERIFICATION
Repeat one block for every Relevant lesson ID. The freshness lesson-key set must match exactly.
Freshness lesson key:
Lesson status: active / draft / deprecated / superseded
Superseded by:
Referenced file:
File exists: YES / NO / N/A
Referenced symbol:
Symbol exists: YES / NO / N/A
Current public facade:
Current facade verified: YES / NO / N/A
Current box:
Current owner:
Current source fingerprint:
Lesson fingerprint comparison: EXACT / PARTIAL / MISMATCH / UNRESOLVED
Invalidation conditions reviewed:
Invalidation condition triggered: YES / NO / UNRESOLVED
Freshness decision: CURRENT / STALE / PARTIAL / BLOCKED
Freshness evidence:
Freshness status: COMPLETE / BLOCKED
Full Error Memory ZIP needed: YES / NO
Full ZIP open reason:
May proceed to exact-source inspection: YES / NO
May begin coding: NO
Reason:
Next safe action:
```
Every relevant lesson must have exactly one matrix block. Allowed dispositions are `EXISTING_VALIDATOR`, `NEW_FOCUSED_TEST`, `NOT_APPLICABLE`, and `CURRENT_SOURCE_REINTERPRETATION`. The lesson-ID set must match the relevant lesson-ID set exactly. A missing or duplicate row, unknown disposition, missing protection path, missing marker, or unsupported reason keeps Q03 blocked.
Every relevant lesson must also have exactly one lesson-freshness verification block. The freshness lesson-key set must match `Relevant lesson IDs` exactly. Q04 remains blocked when file, symbol, facade, box, owner, source fingerprint, lesson status, supersession, or invalidation evidence is missing, contradictory, unresolved for a `CURRENT` decision, or marked `BLOCKED`. An explicit evidence-backed `N/A` is allowed only when that lesson does not reference the corresponding file, symbol, or public facade.
For KANDA Tool work, missing/stale/insufficient Error Memory blocks Q02-Q04 until resolved. For independent external Project work, Tool Error Memory may be marked advisory or `NOT_APPLICABLE_EXTERNAL_PROJECT_TOOL_CONTEXT`; Project progression must not be blocked solely because KANDA Error Memory is unavailable.
### Exact source
Before Q05 can be complete, emit this record:
```text
EXACT SOURCE BASELINE
Source snapshot identity and freshness:
Canonical owner files, public facade, and private implementations inspected:
Consumers, imports, and exports inspected:
Validators and accepted behavior inspected:
State owner, path owner, async behavior, confirmation gates, and frozen behavior:
Generated artifacts and canonical source classification:
Module sizes:
Current source fingerprints:
Unresolved source or authority:
Baseline decision: COMPLETE / BLOCKED
May proceed to Tool/Project classification: YES / NO
May begin coding: NO
```
Use current exact source, not handoff-only or generated evidence. Missing, stale,
unresolved, or blocked evidence keeps Q05 and coding blocked.
### Tool versus Project (Q06)
Load `project_tool_boundary_canon` and emit its complete `TOOL/PROJECT IDENTITY RECORD`. Q06 requires `COMPLETE`, Q07 progression `YES`, and `May begin coding:
NO`. Physical root equality never collapses logical ownership. Current project selection requires session/project-ready evidence; handoff-only or generated evidence is insufficient.
### Ownership and NO-LEAK classification (Q07)
Load `box_architecture_canon`, reuse its seven classifications, and create no aliases, a parallel classifier, or new NO-LEAK authority. Emit:
```text
OWNERSHIP AND NO-LEAK CLASSIFICATION RECORD
Identity basis | primary task owner | active box:
Touched-item classifications, once per item:
Item/path | classification | logical owner | owner root | authority role | allowed action | contract/bridge | leak risk | blocked write
Completeness: exactly once YES/NO; unclassified items; duplicate classifications
Source/lifetime: canonical-vs-generated YES/NO; durable-vs-transient YES/NO
Boundary findings: public routes; private reach-ins; wrong-root; cross-project; cross-box; mutable-state; generated-as-source; Preview/daily-work; Shadow/durable
Evidence placement: validation; freeze; Error Memory; prompt/canon
Leak risks | blocked writes | unresolved classifications:
Decision: COMPLETE/BLOCKED | proceed to Q08 YES/NO | may begin coding NO
```
Missing, duplicate, contradictory, unresolved, wrong-root, private-reach-in, generated-as-source, or lifetime evidence blocks Q07.
### Box Boundary Audit (Q08)
Load `box_architecture_canon`, emit its complete current `BOX BOUNDARY AUDIT`, then:
```text
Q08 COMPLETION
Coverage / one primary box / allowed outside touches: YES / NO
Public-contract communication / state and evidence owners: YES / NO
Unresolved fields:
Decision: COMPLETE/BLOCKED | proceed to Q09 YES/NO | may begin coding NO
```
Unknown, undeclared, leaking, owner, outside-touch, or test gaps block Q08; do not create a competing box schema.
### Public-contract-only communication (Q09)
Load `box_architecture_canon` Laws 2-4 and emit:
```text
PUBLIC-CONTRACT COMMUNICATION RECORD
Identity basis | primary box | communication required YES/NO | no-route evidence:
Routes, once per caller-callee/package boundary:
Caller/callee box | public owner/facade | contract symbol | import/call path | approved route | consumer evidence | signature/behavior | state access | fallback/removal | tests | blocked private route
Ownership/exports: unique public owner YES/NO; explicit exports YES/NO; package-root export verified YES/NO/N/A; duplicate owners
Consumers: required subset preserved YES/NO; current consumers validated YES/NO; star-import ambiguity
Boundary findings: private reach-ins; private reexports in __all__; direct private-state mutation; hidden globals; accidental package-root ownership
Unresolved fields:
Decision: COMPLETE/BLOCKED | proceed to Q10 YES/NO | may begin coding NO
```
A private route, unverified export, duplicate owner, invalid consumer, ambiguous star
import, private-state mutation, or unresolved field blocks Q09. Evidence-backed no-route
is allowed. `COMPLETE` requires Q10 `YES`, coding `NO`, and no parallel API authority.
### Single mutable-state owner (Q10)
Load `box_architecture_canon` Law 5 and State Rules; emit:
```text
SINGLE MUTABLE-STATE OWNERSHIP RECORD
Identity basis | primary box | mutable state required YES/NO | no-state evidence:
States, once per mutable state:
State ID/description | owner box | canonical storage/truth | initializer | mutation owner/route | authorized mutators | external request/read routes | lifetime/persistence owner | reset/invalidation | async/concurrency guard | consumers/tests | blocked direct mutators
Completeness: exactly once YES/NO; duplicate owners/storage authorities; hidden globals; registry runtime state; shared-host feature caches; cross-box aliases/mutations; persistence-owner mismatches; stale async writes
Unresolved fields:
Decision: COMPLETE/BLOCKED | proceed to Q11 YES/NO | may begin coding NO
```
Every mutable state has one owner box, one canonical truth, and one mutation route.
Missing, duplicate, cross-box, hidden, shared-host, persistence, async, or unresolved
evidence blocks Q10. Evidence-backed no-state is allowed; create no parallel state owner.
### MCard applicability and lifecycle (Q11)
Load `architecture_review_project_card_machine_canon` with `project_tool_boundary_canon`; use `large_module_refactor_protocol` only for canonical triggers.
```text
MCARD APPLICABILITY AND LIFECYCLE RECORD
MCard applicable YES/NO | trigger or not-applicable evidence | owner prompts loaded
Applicable card: root/target/path/hash/generation | ownership | observer transition | async validity | Planner/Workbench/Preview/report owners | observer locks | cancel/eject | Tool cleanup | Project retention | source untouched | tests
Decision: COMPLETE/NOT_APPLICABLE/BLOCKED | proceed to Q12 YES/NO | may begin coding NO
```
Canonical rule: one edited file alone does not activate MCard; unresolved lifecycle evidence blocks Q11 and no parallel lifecycle authority is allowed.
### Immutable operation identity (Q12)
Reuse `governed_architecture_companion_handoff` identity rules and current owner canons.
```text
IMMUTABLE OPERATION IDENTITY RECORD
operation required YES/NO | no-operation evidence | Operation ID/type | feature/patch identity | Tool/Project roots | target-relative paths and source fingerprints | lifecycle generation | transaction applicable/ID | owner/immutable fields | current identity match | stale rejection | mismatch invalidation | tests
Decision: COMPLETE/NOT_APPLICABLE/BLOCKED | proceed to Q13 YES/NO | may begin coding NO
```
Identity must precede downstream work. Any identity mismatch invalidates Q13 authority; no parallel runtime identity owner is allowed.
### Explicit write authorization (Q13)
Brick Wall owns KANDA Tool write authorization. For an external Project, source writes belong only to the independent Project actor; KANDA never authorizes or performs those writes.
```text
EXPLICIT WRITE AUTHORIZATION RECORD
writes required YES/NO | Authorization ID | operation/feature IDs | Active Project | allowed relative paths | authorized write route | approved Preview required/ID/fingerprint | expected source fingerprints | lifecycle generation | transaction applicable/ID | owner/evidence | human authorization required/current | current matches | invalidation/expiry | blocked paths | tests
Decision: COMPLETE/NOT_APPLICABLE/BLOCKED | proceed to Q14 YES/NO | may begin coding NO | may write source NO
```
A writable path, helper, manifest field, or boolean alone never grants mutation authority; stale, broad, mismatched, or unresolved authority blocks Q13.
### Immediate pre-write freshness (Q14)
Reuse companion reset rules and Q12/Q13 owners; create no parallel runtime freshness authority.
```text
IMMEDIATE PRE-WRITE FRESHNESS RECORD
Writes required YES/NO | no-write evidence | check phase/timestamp | operation/authorization/feature IDs | Tool/Project roots | allowed targets
Per target: relative path | logical owner/classification | expected SHA-256 | current exact-disk SHA-256 | exists/type/link status | canonical-vs-generated | current match
Preview required/ID/expected/current exact-byte fingerprint | generation expected/current | transaction applicable/expected/current | public owner/facade/consumers | authorization/human authority current | no intervening identity change | stale evidence invalidated | blockers/tests
Decision: COMPLETE/NOT_APPLICABLE/BLOCKED | proceed to Q15 canonical path-authority YES/NO | may begin coding NO | may write source NO
```
Run immediately before a KANDA-authorized write after all preparation. External Project source writes are outside KANDA authority and use the Project-owned freshness contract. Any relevant KANDA identity change invalidates Q12-Q14.
### Canonical path authority (Q15)
Reuse current public path owners; do not create a global super-resolver or independent formulas.
```text
CANONICAL PATH-AUTHORITY CONTRACT RECORD
Paths required YES/NO | no-path evidence | identity basis | primary box | canonical base-root owner/facade
Path families, once per family:
Family/artifact | public owner/facade/symbol | base root class | delegated formula | bounded child | consumers | compatibility adapter | create/write authority | lifetime | containment/blockers | tests | blocked duplicate formulas
Coverage: support | transient garbage | Preview | Shadow | Error Memory | Freeze | validation/handoff when relevant
Decision: COMPLETE/NOT_APPLICABLE/BLOCKED | proceed to Q16 resolved-path containment YES/NO | may begin coding NO | may write source NO
```
Require one public owner per path family. Hardcoded paths, independent suffix joins, competing facades, nested support roots, durable state in transient garbage, or unresolved adapters block Q15.
### Resolved-path containment (Q16)
Reuse Q15 owners and current structural path checks; create no parallel containment service.
```text
RESOLVED-PATH CONTAINMENT RECORD
Containment required YES/NO | no-path evidence | operation/authorization IDs | owner root/facade | resolved owner | candidates
Per candidate: ID | bounded relative input | nearest existing parent | resolved candidate | drive/share and case key | exists/type | symlink/junction/reparse status | structural relative path | result | write route | tests
Negative matrix: traversal | sibling-prefix | absolute escape | other drive | UNC server/share | case collision/ambiguity | symlink/junction escape | unresolved parent/link
Decision: COMPLETE/NOT_APPLICABLE/BLOCKED | proceed to Q17 Preview/Shadow/source separation YES/NO | may begin coding NO | may write source NO
```
Resolve owner and candidate before structural comparison. String-prefix or lexical-only checks, `..`, mismatched anchors, unresolved link/reparse state, or a resolved escape block Q16. New paths require a verified existing parent and clean relative tail.
### Preview, Shadow, and source separation (Q17)
Reuse Q15-Q16 path owners and `project_tool_boundary_canon`; create no parallel runtime store.
```text
PREVIEW, SHADOW, AND SOURCE SEPARATION RECORD
Separation required YES/NO | no-artifact evidence | operation/authorization IDs | Active Project/support/transient roots
Authorities, exactly once each: FINAL_SOURCE | DURABLE_PREVIEW | DISPOSABLE_SHADOW
Per authority: path/facade | logical owner | lifetime | source/durable truth | mutation authority | metadata policy | exact-byte identity | containment | cleanup/retention | consumers/tests | blocked cross-writes
Cross-checks: pairwise-distinct roots | Preview not source truth | Shadow not durable truth | final source excludes Preview-only metadata | no durable evidence under Shadow | no source mutation from Preview/Shadow
Decision: COMPLETE/NOT_APPLICABLE/BLOCKED | proceed to Q18 stale async-result rejection YES/NO | may continue implementation YES/NO | source writes authorized only by current Q13-Q14 evidence
```
Preview may contain candidate source-like files but never canonical source truth. Wrong-box placement, mixed authority, Preview metadata in final source, Shadow as durable evidence, byte-identity mismatch, or unresolved cross-write authority blocks Q17.
### Stale asynchronous-result rejection (Q18)
Reuse current Q12 identity, MCard, controller, receiver, and Qt lifecycle owners; create no global worker registry.
```text
STALE ASYNCHRONOUS-RESULT REJECTION RECORD
Async work required YES/NO | no-async evidence | identity basis | primary box | routes
Per route: owner/controller | request and result identity fields | operation/project/target/source fingerprint | lifecycle and worker generation | acceptance predicate | cancellation revokes result authority | timeout revokes result authority | thread settlement remains distinct from cancel request | late-result action | authorized effects | tests
Cross-checks: stale results cannot mutate state, open gates, write source, write durable evidence, or repopulate current UI | unresolved routes/blockers
Decision: COMPLETE/NOT_APPLICABLE/BLOCKED | proceed to Q19 real Qt/QSignalSpy decision YES/NO | may begin coding NO | may write source NO
```
A matching callback name, cancellation request, or worker completion alone is insufficient. Every accepted result must prove current identity and result authority at the receiver. Q18 never grants coding or source-write authority.
### Real Qt/QSignalSpy validation decision (Q19)
Reuse public Qt facades and focused validators; create no parallel GUI test framework.
```text
REAL QT/QSIGNALSPY VALIDATION DECISION RECORD
Qt behavior affected YES/NO | no-Qt evidence | primary box | cases
Per case: behavior/owner/facade | queued signal material | thread affinity material | widget projection material | static/mock limitation | mode REAL_QT_QSIGNALSPY/REAL_QT_WIDGET/STATIC_SUFFICIENT | real subjects/trigger | signals/count-order-payload | thread/queued assertions | widget/ancestor assertions | cancel-timeout-late scenario | event-loop/watchdog | validator/markers/environment
Cross-checks: QSignalSpy for material signal delivery/count/order/payload or thread affinity; real widgets for click/enable/visibility/ancestor projection; static sufficiency only with no material Qt behavior and explicit evidence | blockers
Decision: COMPLETE/NOT_APPLICABLE/BLOCKED | proceed to Q20 isolated filesystem fixtures YES/NO | may begin coding NO | may write source NO
```
Mocks or source inspection alone cannot prove queued delivery, signal payload/order, thread affinity, event-loop settlement, or real widget projection. Missing PySide6 may define a user-local requirement but cannot convert a material real-Qt case into `STATIC_SUFFICIENT`.
### Shared isolated filesystem fixtures (Q20)
Reuse current path owners and validation helpers; create no production filesystem service.
```text
SHARED ISOLATED FILESYSTEM FIXTURE RECORD
Fixture required YES/NO | no-fixture evidence | shared owner/facade | protected real roots | cases
Per case: validator/owner/purpose | root class | fixture source/support/transient/durable evidence | production paths read-only | write targets/owner overrides | before/after snapshots | cleanup/exclusions | no real/source/drive-root mutation | tests/markers
Cross-checks: synthetic validators must not mutate real source, support, transient, or drive-root locations | durable evidence outside transient | formulas read-only | cleanup verified | blockers
Decision: COMPLETE/NOT_APPLICABLE/BLOCKED | proceed to Q21 parametrized negative boundary matrix YES/NO | may begin coding NO | may write source NO
```
Production formulas may be asserted read-only only; missing snapshots or cleanup, writes outside the sandbox, drive-root creation, source-tree fixtures, durable evidence under transient garbage, or unresolved ownership block Q20.
### Parametrized negative boundary matrix (Q21)
Reuse current boundary validators and one validation-only matrix contract; create no second authorization or containment engine.
```text
PARAMETRIZED NEGATIVE BOUNDARY MATRIX RECORD
Matrix required YES/NO | no-matrix evidence | identity basis | primary box | matrix owner/facade | dimensions | rows
Per row: case ID | SELF_HOSTING/EXTERNAL_PROJECT | path variant | lifecycle/worker generation | transaction state | confirmation state | expected outcome/blockers | canonical validators/markers
Cross-checks: self-hosting and external-project controls | path, generation, transaction, and confirmation-bypass negatives | deterministic blockers | no authority granted | unresolved coverage/blockers
Decision: COMPLETE/NOT_APPLICABLE/BLOCKED | proceed to Q22 public-facade and contract-drift tests YES/NO | may begin coding NO | may write source NO
```
Every negative dimension must be covered, each project mode must carry path, generation, transaction, and confirmation negatives, and confirmation bypass must block even when paths are valid.
### Public-facade and contract-drift tests (Q22)
Reuse current Q09 facade owners and focused validators; create no parallel API registry.
```text
PUBLIC-FACADE AND CONTRACT-DRIFT TEST RECORD
Tests required YES/NO | no-test evidence | primary box | cases
Per case: facade owner/path | canonical import path | package-root export explicit YES/NO | public symbols/__all__ | signature/defaults/annotations/docstring policy | fallback contract | required consumer subset/current consumers | private helper paths | validators/markers
Cross-checks: canonical imports resolve | package root used only when explicit | exact or declared compatible signature preserved | fallback preserved | required consumers preserved | no private reach-in or duplicate public ownership | blockers
Decision: COMPLETE/NOT_APPLICABLE/BLOCKED | proceed to Q23 deterministic MCard transition tests YES/NO | may begin coding NO | may write source NO
```
Package-root assumptions, signature/default/docstring drift, fallback loss, missing required consumers, new private dependencies, or duplicate public ownership block Q22.
### Deterministic MCard transition tests (Q23)
Reuse KPR-12-005, Q11 transition ownership, and existing lifecycle validators; create no second state machine.
```text
DETERMINISTIC MCARD TRANSITION TEST RECORD
Tests required YES/NO | no-test evidence | primary box | canonical owner/facade | valid transitions | invalid transitions | durable artifacts | cases
Per case: case ID | from/to state | normal/rollback/switch/eject path | lifecycle and async generation | transaction/apply/rollback/terminal state | expected allowed/blockers | expected Tool-memory effect | expected durable-project effect | validators/markers
Cross-checks: normal and rollback paths complete | skipped, stale, premature-eject, open-transaction, unresolved-apply, and unverified-rollback transitions block | terminal eject clears target-specific Tool memory only | source/helpers/Preview/transactions/mutation lane/receipt remain | blockers
Decision: COMPLETE/NOT_APPLICABLE/BLOCKED | proceed to Q24 property-based MCard pilot decision YES/NO | may begin coding NO | may write source NO
```
Any transition outside the canonical Q11 set, stale generation, missing lock, premature eject, destructive eject, or durable-state loss blocks Q23.
### Property-based MCard pilot decision (Q24)
Reuse KPR-12-005, Q11, and Q23; property-based testing is an optional validation pilot, never a global runtime dependency.
```text
PROPERTY-BASED MCARD PILOT DECISION RECORD
Pilot applicable YES/NO | no-pilot evidence | Q23 deterministic baseline complete | primary box | canonical owner/facade | pilot kind/dependency scope | properties/generator/replay/minimization | bounds | generated cases/sequences | unique meaningful defects | known/duplicate findings | measurable gain/cost | broader-adoption decision
Cross-checks: bounded and reproducible | optional validation-only dependency | independent invariants | counterexamples replayable/minimized | retain or expand only after unique meaningful defects | no authority/state-machine duplication | blockers
Decision: PILOT_RETAINED/PILOT_REJECTED/NOT_APPLICABLE/BLOCKED | proceed to Q25 mutation-testing pilot decision YES/NO | may begin coding NO | may write source NO
```
Zero unique meaningful defects, deterministic-only rediscovery, unbounded generation, unreplayable failures, global dependency pressure, or absent cost/benefit evidence forbid broader adoption.
### Mutation-testing pilot decision (Q25)
Reuse selected critical validators and Q20 isolated fixtures; mutation testing is bounded validation-only and never full-project by default.
```text
MUTATION-TESTING PILOT DECISION RECORD
Pilot applicable YES/NO | no-pilot evidence | Q24 decision complete | primary box | selected validator/guard inventory | mutation engine/dependency scope | operators/replay/isolation/bounds | baseline pass | mutants generated/killed/survived/equivalent | mutation score before/after repair | meaningful protection gaps | test repairs | measurable gain/cost | broader-adoption decision
Cross-checks: selected critical guards only | source copied into disposable sandbox | production paths unchanged | each mutant deterministic and replayable | surviving non-equivalent mutant requires focused test repair | full-project/default execution forbidden | blockers
Decision: PILOT_RETAINED/PILOT_REJECTED/NOT_APPLICABLE/BLOCKED | proceed to Q26 ZIP containment/collision hardening YES/NO | may begin coding NO | may write source NO
```
Retain only a bounded critical-guard pilot after reproducible surviving mutants reveal a meaningful gap and repaired validators kill them; otherwise reject broader adoption.
### ZIP containment and collision hardening (Q26)
ZIP CONTAINMENT AND COLLISION HARDENING RECORD — Reuse `kanda_reasoner_app.patch_governance.validate_patch_zip` as the sole public owner; private helpers may support it but must not become a competing validator. Hardening required YES/NO | N/A evidence | Q25 complete | primary box | canonical owner/facade | exact final ZIP | protections: absolute/drive/UNC/traversal/duplicate/case-fold/file-directory/link/undeclared install paths | manifest authority | validators/markers | blockers. Decision: COMPLETE/NOT_APPLICABLE/BLOCKED | proceed to Q27 control-byte and encoding guards YES/NO | may begin coding NO | may write source NO. Every final downloadable ZIP must fail closed on dangerous names, collisions, unexpected links, missing declarations, or payload/manifest mismatch before extraction or installation.
### Control-byte and encoding guards (Q27)
CONTROL-BYTE AND ENCODING GUARDS RECORD — Reuse current PowerShell delivery controls and `scripts/merge_freeze_validation_evidence.py`; create no parallel encoding service. Guards required YES/NO | N/A evidence | Q26 complete | primary box | operational scripts | UTF-8 no-BOM producer contract | BOM-aware legacy reads | UTF-16LE fixture | allowed C0 tab/CR/LF | forbidden control-byte rejection | component-wise `Join-Path` generation | validators/markers | blockers. Decision: COMPLETE/NOT_APPLICABLE/BLOCKED | proceed to Q28 structured exception provenance YES/NO | may begin coding NO | may write source NO. Invalid UTF-8, hidden C0 controls, escape-sensitive Windows path literals, host-default evidence serialization, or unverified legacy decoding block Q27.
### Structured exception provenance (Q28)
STRUCTURED EXCEPTION PROVENANCE RECORD — Reuse current Error Memory fields and governed delivery wrappers; create no parallel exception framework. Provenance required YES/NO | N/A evidence | Q27 complete | primary box | cases. Per case: operation phase and ID | target | root classification | last successful marker | failure class SETUP/BEHAVIOR/CLEANUP/EVIDENCE | exception type/message | original cause type/message | invocation position | validators/markers | blockers. Decision: COMPLETE/NOT_APPLICABLE/BLOCKED | proceed to Q29 NO-LEAK runtime trace pilot decision YES/NO | may begin coding NO | may write source NO. Missing cause chains, vague phases, absent operation or target identity, unknown root ownership, missing last marker, or conflated failure classes block Q28.
### NO-LEAK runtime trace pilot decision (Q29) — NO-LEAK RUNTIME TRACE PILOT DECISION RECORD: optional bounded validation observability only; writes/deletes/replacements/archive operations/subprocesses/imports; never claim a security sandbox or integrate a runtime tracer; preserve deterministic attribution evidence plus separately reported platform-dependent runtime occurrence; decision PILOT_RETAINED/PILOT_REJECTED/NOT_APPLICABLE/BLOCKED | proceed to Q30 human confirmation and freeze protection YES/NO | may begin coding NO | may write source NO.
### Human confirmation and freeze protection (Q30) — HUMAN CONFIRMATION AND FREEZE PROTECTION RECORD: reuse `kanda_reasoner_app.freeze_after_update.contract` and the existing Freeze Feature After Update GUI; create no parallel writer. Protection required YES/NO | N/A evidence | Q29 complete | primary box | read-only Preview | explicit Confirm and Write action | exact form and selected-project binding | invalidation after form, source-evidence, target, or project-root change | public-contract confirmation and root checks | no automatic Error Memory promotion | no automatic Freeze Memory write | focused and real-Qt validators/markers | blockers. Decision COMPLETE/NOT_APPLICABLE/BLOCKED | proceed Q31 changed-file-to-validator coverage map YES/NO | may begin coding NO | may write source NO. A cached preview, stale form, changed project root, implicit confirmation, automatic promotion, or any write outside the confirmed contract blocks Q30.
### Changed-file-to-validator coverage map (Q31) - CHANGED-FILE-TO-VALIDATOR COVERAGE MAP: reuse current manifests, Error Memory, frozen behavior, public contracts, and validator owners; create no parallel registry or runtime service. Coverage required YES/NO | N/A evidence | Q30 complete/frozen | primary box | exact changed-file set | explicit validator inventory/discovery method. Per file: path | owner box | public contract | Error Memory lessons | frozen behavior | focused, boundary, GUI, delivery, and negative-test dispositions with APPLIES/NOT_APPLICABLE reason, validator paths, and expected markers. Cross-checks: every changed file exactly once | every applicable validator inventoried | no orphan required validator | no broad substring exclusion | no unresolved or conflicting disposition. Decision COMPLETE/NOT_APPLICABLE/BLOCKED | proceed to Q32 validation and evidence provenance YES/NO | may begin coding NO | may write source NO.
### Validation and evidence provenance (Q32) - VALIDATION AND EVIDENCE PROVENANCE RECORD: reuse current source, Error Memory export, prompt metadata, validators, durable project-support evidence, and environment facts; create no parallel evidence registry or runtime service. Provenance required YES/NO | N/A evidence | Q31 complete/frozen | feature/operation/project identities | Tool, Project, support, and evidence owners | exact source fingerprints | relevant lesson IDs/export identity | prompt and validator revisions/hashes | exact commands | environment/interpreter/dependency state | expected and observed markers | durable evidence path/hash/encoding/time | limitations | blockers. Decision COMPLETE/NOT_APPLICABLE/BLOCKED | proceed Q33 pinned local-model provenance YES/NO | may begin coding NO | may write source NO. Missing, stale, mismatched, invented, or transient-only provenance blocks Q32. After Q40, all applicable pre-code items must be `[x]` or evidence-backed `[N/A]`.
```text
### Pinned local-model provenance (Q33) - PINNED LOCAL-MODEL PROVENANCE RECORD: applies whenever a local model, embedding model, or AI-assisted output is used as evidence or materially influences a candidate, plan, decision, or correction; reuse current model registry, chat, feature, Q32 durable-evidence, and deterministic validation owners; create no parallel model registry, runtime service, or authority path. AI/model evidence used YES/NO | N/A evidence | Q32 complete/frozen | feature/operation/run IDs | provider/runtime | model ID | exact model digest/revision and basis | tokenizer ID/revision or explicit provider-bundled digest evidence | code revision/hash | canonical prompt/messages hash and serialization | inference settings including temperature, seed, sampling, context/output limits, stops, and options hash | offline/local mode and network policy | exact input fingerprints | raw/normalized output hash and schema | advisory/authority classification | durable evidence path | validators/markers | limitations/blockers. Decision COMPLETE/NOT_APPLICABLE/BLOCKED | proceed Q34 profile-before-optimization YES/NO | may begin coding NO | may write source NO. An unpinned model or tokenizer, incomplete prompt/settings/input/output identity, external network ambiguity, or model output presented as direct source/validation/freeze/routing authority blocks Q33; unpinned AI output remains advisory.
### Profile-before-optimization gate (Q34) - PROFILE-BEFORE-OPTIMIZATION RECORD: applies before any performance-motivated change to algorithms, data structures, caching, batching, concurrency, parallelism, vectorization, memory strategy, I/O, database access, startup, rendering, or latency-sensitive behavior; reuse current specialist performance prompts, owning-box code, Q32 evidence, and deterministic validators; create no parallel profiler, benchmark framework, telemetry service, cache owner, or optimization runtime. Optimization proposed YES/NO | N/A evidence | Q33 complete/frozen | feature/operation IDs | primary and slow-path owner boxes | named slow path | representative workload and scale | exact workload/source/environment fingerprints | profiler/tool and exact command | warmups and repeated measurements | baseline metric/unit/measurements/median/mean/stdev/coefficient of variation | variance threshold and acceptance | bottleneck classification and evidence hash | simplest alternatives considered | proposed change | expected and minimum acceptable improvement | complexity budget | rollback condition | durable evidence path | validators/markers | limitations/blockers. Decision COMPLETE/NOT_APPLICABLE/BLOCKED | proceed Q35 focused performance baseline YES/NO | may begin coding NO | may write source NO. A guessed slow path, synthetic or unrepresentative workload, single timing, missing variance, unresolved bottleneck, absent expected gain, or undeclared complexity budget blocks Q34; no optimization may be admitted merely because code appears slow.
### Focused performance baseline (Q35) - FOCUSED PERFORMANCE BASELINE RECORD: applies only after Q34 has identified and frozen a real bottleneck; reuse the bottleneck owning box, its public contract, Q34 profiler evidence, Q20 isolated fixtures, Q31 coverage, and Q32 provenance; create no global benchmark registry, shared performance service, telemetry runtime, cache owner, or cross-box benchmark framework without explicit necessity evidence. Baseline required YES/NO | N/A evidence | Q34 decision COMPLETE/NOT_APPLICABLE and frozen baseline | feature/operation IDs | primary box | bottleneck name/classification/owner/public contract | Q34 evidence hash | benchmark scope OWNER_LOCAL/CROSS_BOX_APPROVED | benchmark owner/path | broader-framework necessity evidence/owner/affected boxes | representative workload and scale | exact workload/source/environment fingerprints | benchmark tool and exact command | metric/unit | warmups/repeated measurements | median/mean/stdev/coefficient of variation | variance threshold/acceptance | correctness validators/markers | read-only or disposable-fixture isolation | production writes forbidden | baseline evidence hash | durable evidence path | validators/markers | limitations/blockers. Decision COMPLETE/NOT_APPLICABLE/BLOCKED | proceed Q36 module-size and cohesion enforcement YES/NO | may begin coding NO | may write source NO. A benchmark outside the bottleneck owner, a synthetic or unrepresentative workload, missing Q34 lineage, single-run timing, excessive variance, absent correctness guards, production mutation, or an unjustified shared framework blocks Q35.
### Module-size and cohesion enforcement (Q36) - MODULE-SIZE AND COHESION RECORD: applies whenever Python source is created or touched; reuse the beginning-of-day Code Module Size Bridge, `large_module_refactor_protocol` v8.0, the canonical `module_size_policy`, Q22 facade ownership, Q31 changed-file coverage, and Q32 durable provenance; create no parallel line counter, refactor engine, facade registry, helper registry, or automatic splitter. Enforcement required YES/NO | N/A evidence | Q35 decision COMPLETE/NOT_APPLICABLE and frozen baseline | feature/operation IDs | primary box | exact changed-file set | exact touched-Python set | per module: path/owner/role/responsibility/public contract/physical lines after formatting/ideal <=400/max <=500/AST parse/formatter and markers/compression absent/artificial padding absent/split basis RESPONSIBILITY or NONE/helper dependency direction/facade size decision/over-ideal justification/refactor route | exact Python-set reconciliation | validators/markers | durable evidence path | limitations/blockers. Decision COMPLETE/NOT_APPLICABLE/BLOCKED | proceed Q37 canonical ownership reconciliation YES/NO | may begin coding NO | may write source NO. Any touched Python module above 500 lines, non-PEP-8 compression, artificial padding, arbitrary line-range split, responsibility-free micro-helper, helper-to-facade back dependency, unexplained facade growth, missing touched-file reconciliation, or a broad module-size exception blocks Q36.
### Canonical ownership reconciliation (Q37) - CANONICAL OWNERSHIP RECONCILIATION RECORD: identify duplicate scanners, duplicate schemas, duplicate reports, duplicate state owners, and duplicate consumers; reuse Q07 ownership classification, Q09 public contracts, Q10 state ownership, Q22 consumer/facade drift, Q31 coverage, Q32 provenance, `boundary_first_repair_protocol`, and `kanda_box_shielding_canon`; select one canonical owner per responsibility; require retirement or evidence-backed coexistence for every competitor; migrate consumers through the canonical public contract; disable duplicate state writes; create no new coordination super-system, ownership registry, scanner registry, schema registry, report registry, or state registry. When a local repair is proposed for reusable-contract extraction or broader infrastructure adoption, enforce exactly `RECONCILE -> REPAIR -> VALIDATE -> SHIELD -> FREEZE -> EXTRACT -> ADOPT`: reconcile existing owners before repair; validate the bounded repair before extraction; obtain a risk-based shield disposition from KPR-04-002; require the repaired source behavior to have a human-confirmed frozen baseline before extraction; extract only the smallest proven contract into the existing canonical owner unless a verified responsibility gap proves a new owner is necessary; and adopt one bounded consumer at a time. Reconciliation required YES/NO | N/A evidence | Q36 complete/frozen | feature/operation IDs | primary box | exact changed files | responsibility inventory | per responsibility: canonical owner box/path/public contract/source of truth/state mutation owner/current consumers/duplicate candidates by kind/disposition/reason/adapter or migration target/consumer migration/validators/markers/unresolved fields | reusable contract extraction proposed YES/NO | no-extraction evidence | strategy sequence | repair validated before extraction | shield decision | freeze baseline before extraction | extraction owner path | new owner created YES/NO | new owner gap proven YES/NO | adoption scope | extraction blockers | cross-checks: one canonical owner per responsibility | all competitors dispositioned | duplicate state writes disabled | consumers migrated | no super-system | durable evidence/limitations/blockers. Decision COMPLETE/NOT_APPLICABLE/BLOCKED | proceed Q38 handoff freshness and provenance YES/NO | may begin coding NO | may write source NO. Unresolved competing ownership, missing consumer migration, duplicate mutable-state authority, coordination-only super-systems, coexistence without distinct-responsibility evidence, extraction before a validated repair, missing shield disposition, missing human-confirmed frozen baseline for repaired source behavior, new-owner creation without a verified gap, or broad unbounded adoption blocks Q37.
### Handoff freshness and provenance (Q38) - HANDOFF FRESHNESS AND PROVENANCE RECORD: prevent generated AI handoff, source-archive, manifest, validation, Error Memory, and Freeze-context artifacts from being mistaken for current source; reuse `handoff_at_end_of_work`, startup source-map/sync owners, Q05 exact source, Q14 immediate freshness, Q27 encoding, Q32 durable provenance, Error Memory export, and active-project freeze context; create no parallel handoff engine, context service, source mirror, freshness registry, or mutable authority. Freshness required YES/NO | N/A evidence | Q37 complete/frozen | feature/operation IDs | primary box | exact current source fingerprints | handoff artifact identity/generation time/source fingerprint set | manifest identity/hash/generation time/source linkage | validation evidence identity/hash/time/source linkage/markers | Error Memory manifest identity/hash/time/lesson freshness | Freeze context identity/hash/time/latest freeze ID | source-archive status/fingerprint/authority classification | stale artifacts and invalidation reasons | validators/markers | durable evidence/limitations/blockers. Decision COMPLETE/NOT_APPLICABLE/BLOCKED | proceed Q39 task-specific context admission test YES/NO | may begin coding NO | may write source NO. Missing timestamps, mismatched source fingerprints, older manifests or validation, stale Error Memory, unrefreshed Freeze context, authoritative generated archives, unresolved stale artifacts, or a new context/freshness engine blocks Q38. PRE-CODE AUTHORIZATION
### Task-specific context admission test (Q39) - TASK-SPECIFIC CONTEXT ADMISSION RECORD: prevent creation of another context summary, intelligence layer, context service, or routing authority without controlled evidence that current handoff, manifests, and routes fail representative tasks; reuse Q01 verified-problem admission, Q05 exact source, Q14 freshness, Q21 controlled negative matrices, Q22 public contracts, Q37 ownership reconciliation, and Q38 handoff freshness. New context proposed YES/NO | N/A evidence | Q38 complete/frozen | exact current context-owner inventory | representative task set and input fingerprints | baseline owner/results/failures | candidate owner/results | same source/environment/evaluator | comparison metrics and thresholds | repeated trials/variance | reproduced baseline inadequacy | simpler manifest/route/handoff strengthening options | unique bounded responsibility | public contract/lifecycle/invalidation | no parallel intelligence engine/context registry/coordination super-system | durable evidence/validators/limitations/blockers. Decision ADMITTED/REJECTED/NOT_APPLICABLE/BLOCKED | proceed Q40 one-primary-box governed release YES/NO | may begin coding NO | may write source NO. Missing controlled comparison, mismatched tasks or source snapshot, unreproduced failure, no measurable thresholded gain, a simpler existing-owner fix, vague ownership, or a new super-system blocks admission.
### One-primary-box governed release (Q40) - ONE-PRIMARY-BOX GOVERNED RELEASE RECORD: every release must remain small, attributable, and independently verifiable by declaring exactly one primary box; bounded supporting touches; the exact changed-file set; exact source baselines and source-fingerprint-set hash; Error Memory and frozen-behavior regression obligations; one validator-coverage row per changed file; the canonical exact-final-ZIP contract; freeze-hint and durable-evidence ownership; human-local validation state; and explicit Preview plus Confirm and Write state. Reuse Q06 Tool/Project identity, Q07-Q10 ownership and public contracts, Q15 path authority, Q26 ZIP validation, Q27 encoding, Q30 confirmation protection, Q31 coverage, Q32 provenance, Q36 size/cohesion, Q37 canonical ownership, Q38 freshness, and Q39 admission. Release applicable YES/NO | N/A evidence | Q39 complete/frozen | feature/operation/release IDs | exactly one primary box | supporting touches with owner/reason/public contract | exact changed files | source baseline hashes | source-fingerprint-set hash | regression obligations | validation map | exact ZIP name/member set/canonical validator/external delivery hash state | freeze hint count and evidence path | automatic freeze write false | Preview read-only | human confirmation required | human-local validation PENDING/COMPLETE/FAILED | durable evidence path | limitations/blockers. Decision READY_FOR_LOCAL_VALIDATION/VALIDATED_READY_FOR_FREEZE/COMPLETE/NOT_APPLICABLE/BLOCKED | MAY DELIVER PATCH YES/NO | MAY CLAIM VALIDATION PASSED YES/NO | MAY FREEZE YES/NO. Multiple primary boxes, unbounded supporting touches, missing changed-file or baseline coverage, orphan validators, broad exclusions, unverified exact ZIP, generated-as-source, transient durable truth, automatic freeze writes, stale validation, or a release coordination super-system block Q40. PRE-CODE AUTHORIZATION Q01-Q40 complete YES/NO | architecture/regression/validator coverage complete YES/NO | user authorization current YES/NO | MAY BEGIN CODING: YES/NO | MAY WRITE SOURCE: YES/NO | reason/next safe action ### Implementation discipline - One primary box; no unrelated cleanup; preserve/migrate public contracts intentionally; forbid private cross-box imports, duplicate truth, hidden state, hardcoded project assumptions, generated-as-source, stale results, and removed confirmation gates. Writes require current Q13-Q14 authority/freshness and module-size compliance.
```
### Validation — Validate structure, contracts, behavior, boundaries, regressions, negatives, material Qt/MCard behavior, isolated filesystems, ZIP/encoding, provenance, self-hosting, and external-project behavior; never claim unrun checks passed.
### Patch delivery
Before any ZIP link: exact final ZIP contract passes; root freeze hint is present and not duplicated; changed-file map is complete; installer stages drive-root ZIP into daily-work; no Downloads/Desktop fallback exists; terminal cleanup is canonical; Error Memory intake is evidence-backed.
### Freeze
Freeze only after user-local validation. Preview remains read-only; Confirm and Write requires explicit human action. Project frozen memory belongs under active project support, never reusable tool source or project_freeze_ledger.
### Error Memory after failure or correction
Capture phase, source, symptom, proven cause/uncertainty, assumption, fix, prevention, ownership/fingerprint, regression markers, redaction, and human review; never auto-promote.
### Handoff — Report changed files, owners/touches/contracts, Tool/Project and lifetime ownership, lessons/frozen behavior, validation, risks, blockers, and next action.
## Companion routing — Brick Wall should request the smallest necessary owner prompts. Typical companions include:
- `project_tool_boundary_canon`, `box_architecture_canon`, and `kanda_box_shielding_canon` for identity/boundaries; compact Error Memory and exact source before coding; `architecture_review_project_card_machine_canon` when MCard applies. `bundle_gated_development_workflow` for patches; `pre_output_contract_gates` before artifacts; `freeze_code_intake_and_form_protocol` for freeze. Do not load every companion automatically when it is not relevant.
## Validation requirements for this prompt
Registration is valid only when tests prove:
- prompt code is `KPR-03-001`; prompt ID and metadata match;
- exact `brick wall` trigger is registered;
- folder card and human/machine routing indexes reference the prompt exactly once;
- startup-generated prompt navigation contains the Brick Wall bridge;
- Q01 through Q40 are all present;
- unrelated prompts are not changed;
- a KANDA-owned final patch ZIP passes the KANDA ZIP contract; an external Project release uses its Project/release-owned contract;
- freeze remains human-confirmed;
- any Error Memory lesson is evidence-backed and active-ready.
## Do-not-regress rules
- Brick Wall is routed, not a full always-startup prompt.
- The startup layer carries only a compact route bridge.
- Every direct `brick wall` invocation displays the live status and Q01-Q40 ledger.
- Evidence-sensitive ticks reset when current evidence is absent or stale.
- Brick Wall coordinates but does not replace the owner or specialist owner canons.
- KANDA Tool coding never precedes governed Error Memory and exact-source review; independent external Project coding is never blocked by missing Tool Error Memory.
- Tool/Project, Box, shielding, NO-LEAK, MCard, validation, confirmation, and freeze protections remain hard gates.
- No item is marked complete from assumption alone.
