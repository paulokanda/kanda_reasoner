---
prompt_id: router_bridge_governed_implementation title: Router Bridge Governed Implementation Gate
version: 5.0 status: deprecated
load_type: never active_route: false
owner_group: 05_patch_delivery_and_validation created_by_patch: brick-wall-q02-visible-error-memory-preflight-enforcement-v1
---
# DEPRECATED HISTORICAL COMPATIBILITY TOMBSTONE

This file is not an active KANDA owner and must never be loaded for current work. Current authority is `brick_wall_comprehensive_quality_gate`. Trigger aliases are preserved in
`prompt_substitution_map.md` and current routing indexes.

The historical contract below remains only because frozen validators and old release provenance still inspect exact compatibility markers. It cannot
authorize implementation, delivery, validation, freeze, Error Memory, or any source write.

---

# Router Bridge Governed Implementation Gate
## Purpose
Require a visible compliance artifact before governed code, prompt, startup, validation, GUI, Error Memory, freeze, or patch-source edits.
## Trigger conditions
Route here when the user request or the AI plan includes any of the following:
```text
implement code
repair code
refactor code
modify source files
create a validation script
edit prompt library files
update router or prompt bridge logic
update startup delivery logic
modify generated startup behavior
modify GUI behavior
create a patch payload
change Error Memory workflow
change freeze workflow
change Large File Refactor Workbench Preview ownership
change Shadow workspace or daily-work semantics
change project-specific durable support-state paths
change Architecture Review card lifecycle, project-root switching, target switching, stale async results, transaction locks, or post-completion eject behavior
use external AI to audit implementation logic or code
verify uncertain API, dependency, platform, security, concurrency, or validation claims
perform a deep anti-hallucination audit before implementation
```
Do not route here for simple explanation-only work that will not edit source, prompts, validation files, startup files, or patch artifacts.
## Required companion prompts
Load or apply the smallest complete set:
```text
ai_prompt_request_canon + prompt_navigation_index
implementation_and_delivery_protocol
box_architecture_canon, when boundary risk exists
boundary_first_repair_protocol or kanda_box_shielding_canon only when their focused Class 04 applicability is proven; the retired architecture companion is never loaded
project_tool_boundary_canon, mandatory when project/tool identity, Workbench Preview, durable project support state, Shadow, daily-work, or self-hosting can be confused
architecture_review_project_card_machine_canon, mandatory when Architecture Review/AST Audit/Planner/Workbench/Completion card lifecycle, project-root switch, target switch, stale async result, transaction lock, apply/rollback, receipt, or eject semantics are involved
pre_output_contract_gates, when terminal, ZIP, freeze, or validation artifacts will be emitted
python_clean_code or relevant Python engineering prompt, when Python files are changed
anti_hallucination_short_group, when governed implementation contains meaningful uncertainty or AI-generated technical claims that need compact evidence-first checking
anti_hallucination_full_group, when work is architectural, unfamiliar, multi-file, dependency-changing, security-sensitive, concurrency-sensitive, cross-box, difficult to roll back, or explicitly requests deep independent audit plus web/literature verification
```
Do not load the entire prompt library. Do not code from memory.
## Anti-hallucination group selection bridge
The anti-hallucination groups are routed companions, not always-startup prompts. Use:
```text
routine governed implementation with meaningful uncertainty
-> anti_hallucination_short_group
high-risk / architectural / unfamiliar / dependency / security / concurrency / cross-box work
-> anti_hallucination_full_group
```
The groups must preserve this evidence train:
```text
source truth -> provisional plan -> independent adversarial review -> claim ledger -> current-source verification plus disconfirmation search -> selective literature audit when justified -> evidence-based synthesis -> implementation -> deterministic validation -> final adversarial verification -> human approval
```
Do not treat agreement between AIs as proof. Do not let web or book advice override current project source truth for project-specific behavior. Do not use literature to verify current API signatures, versions, flags, or runtime behavior.
## Verified-problem admission gate (Q01)
Before emitting the Implementation Gate, emit this evidence-backed admission record:
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
Hard rules:
- Do not admit a new feature merely because it sounds useful.
- Inspect the current canonical owner and overlapping capability first.
- Prefer `REPAIR_EXISTING` or `CONSOLIDATE` when an owner already exists.
- Use `NO_CHANGE` when current behavior is adequate.
- Use `BLOCK` when evidence, ownership, exact source, or measurable gain is unresolved.
- Do not create a parallel scanner, schema, state owner, report, context engine, validator family, or workflow without proving the current owner is inadequate.
- Q01 evidence must remain visible in the implementation handoff and validation plan.
- If the record is incomplete or the decision is `BLOCK`, `May implement` must be `NO`.
## Visible Error Memory preflight (Q02)
After Q01 admits work and before exact-source planning or coding, read the current compact Error Memory prompt, compact lesson export, and manifest. Emit:
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
Hard rules:
- Compact Error Memory is always read before governed implementation planning.
- Error Memory is prevention guidance, never a substitute for exact source.
- Open the full Error Memory ZIP only when the manifest or task justifies it.
- Every relevant lesson must have exactly one complete regression-matrix block.
- The lesson-ID set must match `Relevant lesson IDs` exactly; duplicates, omissions, unknown dispositions, missing protection paths, or missing markers block Q03.
- Every relevant lesson must also have exactly one complete lesson-freshness verification block.
- The freshness lesson-key set must match `Relevant lesson IDs` exactly. Missing or duplicate keys, unknown statuses, unresolved current-source evidence, contradictory supersession, missing owner/facade evidence, triggered invalidation with a `CURRENT` decision, or any blocked row blocks Q04.
- Evidence-backed `N/A` is allowed only when the lesson does not reference the corresponding file, symbol, or public facade.
- Missing, stale, unread, or insufficient Error Memory keeps exact-source progression and coding blocked until disposition is explicit.
- `May begin coding` remains `NO` inside the Q02 record. Coding authorization may change only after Q03-Q19 phase-relevant gates are completed.
## Exact-source baseline gate (Q05)
After Q04 and before the Implementation Gate, emit:
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
Current exact source is mandatory. Handoff-only, stale, missing, unresolved, or blocked evidence keeps Q05 and `May implement` blocked.
## Tool/Project identity gate (Q06)
Load `project_tool_boundary_canon` and emit its exact `TOOL/PROJECT IDENTITY RECORD`. Require `COMPLETE`, Q07 progression `YES`, coding `NO`, and current selection evidence.
Root equality is allowed only for explicit self-hosting with correct write targets and logical separation.
## Ownership and NO-LEAK classification gate (Q07)
Load `box_architecture_canon`; require Brick Wall's exact `OWNERSHIP AND NO-LEAK CLASSIFICATION RECORD`, exactly-once classification, `COMPLETE`, Q08 `YES`, coding `NO`, and no leak or parallel owner.
## Box Boundary Audit gate (Q08)
Require the complete canonical audit plus `Q08 COMPLETION`, one primary box, allowed outside touches, resolved contracts/state/evidence/tests, `COMPLETE`, Q09 `YES`, coding `NO`; do not create a competing box schema.
## Public-contract-only communication gate (Q09)
Load Laws 2-4; require Brick Wall's exact `PUBLIC-CONTRACT COMMUNICATION RECORD`, one verified facade, explicit exports, valid consumers, approved state access/fallback, no private reach-in or duplicate owner, `COMPLETE`, Q10 `YES`, and coding `NO`. Evidence-backed no-route is allowed.
## Single mutable-state owner gate (Q10)
Load Box Architecture Law 5 and State Rules; require Brick Wall's exact `SINGLE MUTABLE-STATE OWNERSHIP RECORD`, each state once, one owner and mutation route, lifecycle/persistence/reset/async guards, no hidden/cross-box/shared-host/registry state, `COMPLETE`, Q11 `YES`, coding `NO`, or evidence-backed no-state.
## MCard applicability and lifecycle gate (Q11)
Load `architecture_review_project_card_machine_canon` with `project_tool_boundary_canon` only for canonical triggers. Require the exact MCard record, explicit APPLIES or NOT_APPLICABLE evidence, complete lifecycle evidence when applicable, Q12 `YES`, and coding `NO`; one edited file alone is not a trigger.
## Immutable operation identity gate (Q12)
Reuse current identity owners. Require Brick Wall's immutable operation record, current root/target/hash/generation/operation/transaction match, Q13 `YES`, and coding `NO`.
## Explicit write authorization gate (Q13)
Brick Wall owns final authorization. Require its current write record tied to Q12 identity, bounded paths, route, Preview when required, hashes, generation, transaction, and human authority; path/helper/boolean evidence is invalid. Require Q14 `YES`, coding and source writing `NO`.
## Immediate pre-write freshness gate (Q14)
Reuse companion reset rules and Q12/Q13 owners. Require Brick Wall's exact freshness record, immediate exact-disk target hashes, current Preview/generation/transaction/owner/authorization/human authority, no intervening identity change, stale-evidence invalidation, `COMPLETE` or evidence-backed `NOT_APPLICABLE`, and Q15 progression `YES`. Q14 itself keeps coding and source writing `NO`.
## Canonical path-authority gate (Q15)
Reuse current root and specialized path owners. Require Brick Wall's exact record, one canonical base-root authority, one public owner per path family, bounded delegation/adapters, no hardcoded or competing formulas, `COMPLETE` or evidence-backed `NOT_APPLICABLE`, Q16 progression `YES`, and coding/source writing `NO`.
## Resolved-path containment gate (Q16)
Reuse Q15 roots and current structural checks. Require resolved owner/candidates, verified existing-parent/link state for new paths, traversal/sibling/cross-drive/UNC/case/link negatives, `COMPLETE` or evidence-backed `NOT_APPLICABLE`, Q17 progression `YES`, and coding/source writing `NO`.
## Preview, Shadow, and source separation gate (Q17)
Before Q18, reuse Q15-Q16 owners and `project_tool_boundary_canon`. Require exactly one FINAL_SOURCE, DURABLE_PREVIEW, and DISPOSABLE_SHADOW authority when applicable; distinct roots/lifetimes; no Preview source truth, Shadow durable truth, Preview-only metadata in final source, or source mutation from Preview/Shadow; exact-byte identity where hashes govern artifacts; `COMPLETE` or evidence-backed `NOT_APPLICABLE`; Q18 progression `YES`. Q17 never grants source-write authority.
## Stale asynchronous-result rejection gate (Q18)
Reuse current Q12 identity, MCard, controller, receiver, and Qt lifecycle owners. Require one complete route row per asynchronous result, matching request/result operation, project, target, source fingerprint, lifecycle and worker generation, a receiver-side acceptance predicate, cancellation/timeout authority revocation, distinct thread settlement, fail-closed late-result disposal, `COMPLETE` or evidence-backed `NOT_APPLICABLE`, and Q19 progression `YES`. Q18 never grants coding or source-write authority.
## Real Qt/QSignalSpy validation decision gate (Q19)
Reuse public Qt facades and existing focused validators. Require one case per material Qt behavior. `QSignalSpy` is mandatory for material queued delivery, signal count/order/payload, or thread-affinity evidence; real widgets are mandatory for click, enabled, visibility, or ancestor projection; static/model sufficiency requires evidence that no material Qt behavior is affected. Require `COMPLETE` or evidence-backed `NOT_APPLICABLE`, Q20 progression `YES`, and coding/source writing `NO`.
## Shared isolated filesystem fixtures gate (Q20)
Reuse current path owners and validation-only fixture helpers. Require one shared fixture owner/facade, sandbox-only write targets, production paths read-only, before/after protected-path snapshots, scoped owner overrides, cleanup proof, VCS/cache exclusions, and no real source/support/transient/drive-root mutation. Require `COMPLETE` or evidence-backed `NOT_APPLICABLE`, Q21 progression `YES`, and coding/source writing `NO`.
## Parametrized negative boundary matrix gate (Q21) — Reuse current Q06/Q12-Q18 boundary validators and one validation-only matrix contract. Require self-hosting and external-project controls, every path/generation/transaction/confirmation negative, deterministic blockers, `COMPLETE` or evidence-backed `NOT_APPLICABLE`, Q22 progression `YES`, and coding/source writing `NO`.
## Public-facade and contract-drift tests gate (Q22) — Reuse Q09 public owners and focused contract validators. Require canonical import paths, explicit package-root export status, preserved signatures/defaults/annotations/docstring policy, preserved fallback, required consumer subset, no private dependency or duplicate public ownership, `COMPLETE` or evidence-backed `NOT_APPLICABLE`, Q23 progression `YES`, and coding/source writing `NO`.
## Deterministic MCard transition tests gate (Q23) — Reuse KPR-12-005, Q11 transition ownership, and existing lifecycle validators. Require deterministic normal and rollback paths, blocked skipped/stale/premature-eject/locked transitions, terminal Tool-memory clearing, durable project-state preservation, `COMPLETE` or evidence-backed `NOT_APPLICABLE`, Q24 progression `YES`, and coding/source writing `NO`.
## Property-based MCard pilot decision gate (Q24) — Reuse KPR-12-005, Q11, and Q23. A bounded property-based or similar pilot is validation-only and optional; require reproducible generation, independent invariants, replay/minimization, explicit bounds, defect-yield and cost evidence, no global dependency, `PILOT_RETAINED`, `PILOT_REJECTED`, or evidence-backed `NOT_APPLICABLE`, Q25 progression `YES`, and coding/source writing `NO`. Broader adoption requires unique meaningful defects.
## Mutation-testing pilot decision gate (Q25) — Reuse Q16/Q18/Q23 focused validators and Q20 isolated fixtures. Require selected critical guards only, deterministic replay, disposable source copies, explicit bounds, baseline pass, killed/surviving/equivalent classification, focused repair for every surviving non-equivalent mutant, measured gain/cost, no global/runtime dependency, `PILOT_RETAINED`, `PILOT_REJECTED`, or evidence-backed `NOT_APPLICABLE`, Q26 progression `YES`, and coding/source writing `NO`. Never run full-project mutation testing by default.
## ZIP containment and collision hardening gate (Q26) — Reuse the canonical patch-governance facade and require pre-extraction rejection of absolute, drive-qualified, UNC, traversal, duplicate, Windows case-fold, file/directory-collision, unexpected-link, and undeclared-install-path archives. The exact final ZIP, manifest declarations, public validator route, and deterministic negative markers must pass; coding/source writing remain `NO`, and only Q27 progression may be authorized.
## Control-byte and encoding guards gate (Q27) — Reuse current PowerShell delivery controls and `scripts/merge_freeze_validation_evidence.py`. Require explicit UTF-8 no-BOM evidence output, BOM-aware legacy reads when needed, UTF-16LE fixtures, strict invalid-byte rejection, C0 rejection except tab/CR/LF, component-wise `Join-Path` construction, `COMPLETE` or evidence-backed `NOT_APPLICABLE`, Q28 progression `YES`, and coding/source writing `NO`.
## Structured exception provenance gate (Q28) — Reuse current Error Memory fields and governed delivery wrappers. Require original cause, operation phase and ID, target, root classification, last successful marker, invocation position, and an explicit SETUP/BEHAVIOR/CLEANUP/EVIDENCE failure class for every material failure path. Require `COMPLETE` or evidence-backed `NOT_APPLICABLE`, Q29 progression `YES`, and coding/source writing `NO`; never create a parallel exception framework.
## NO-LEAK runtime trace pilot decision gate (Q29) — Reuse Q20/Q21/NO_LEAK protection and keep the application Runtime Collector separate. Permit only a bounded standard-library child-process audit pilot for validation observability; inventory writes, deletes, replacements, archive operations, subprocesses, and imports; record path-attribution and child-process limitations; never claim a security sandbox or integrate a runtime tracer. Require `PILOT_RETAINED`, `PILOT_REJECTED`, or evidence-backed `NOT_APPLICABLE`, Q30 progression `YES`, and coding/source writing `NO`. Retention requires a reproducible unique defect and no unresolved false-assurance risk. Human confirmation and freeze protection gate (Q30): reuse the Freeze Feature After Update public contract and GUI; require read-only Preview, explicit human Confirm and Write, exact reviewed-form and selected-project binding, invalidation after form/source-evidence/target/root change, public-contract confirmation and root checks, no automatic Error Memory promotion or frozen-memory write, `COMPLETE` or evidence-backed `NOT_APPLICABLE`, Q31 progression `YES`, and coding/source writing `NO`.
## Mandatory Implementation Gate — required output
```text
IMPLEMENTATION GATE
Task domain:
Verified problem admission decision:
Q01 evidence complete: YES / NO
Q02 Error Memory preflight complete: YES / NO
Relevant Error Memory lesson IDs:
Q03 regression matrix complete: YES / NO
Q04 lesson freshness verification complete: YES / NO
Q05 exact-source baseline complete: YES / NO
Exact-source baseline decision: COMPLETE / BLOCKED
Q06 Tool/Project identity record complete: YES / NO
Tool/Project identity decision: COMPLETE / BLOCKED
Tool task or Project operation:
Tool source root:
Active project root:
Active project support root:
Project support-state ownership:
Transient garbage root:
Self-hosting logical separation preserved: YES / NO
May proceed to Q07 classification: YES / NO
Q07 ownership and NO-LEAK record complete: YES / NO
Ownership/NO-LEAK decision: COMPLETE / BLOCKED
May proceed to Q08 Box Boundary Audit: YES / NO
Q08 Box Boundary Audit complete: YES / NO
Box Boundary decision: COMPLETE / BLOCKED
May proceed to Q09 public-contract gate: YES / NO
Q09 public-contract communication record complete: YES / NO
Public-contract communication decision: COMPLETE / BLOCKED
May proceed to Q10 mutable-state ownership gate: YES / NO
Q10 single mutable-state ownership record complete: YES / NO
Mutable-state ownership decision: COMPLETE / BLOCKED
May proceed to Q11 MCard applicability gate: YES / NO
Q11 MCard applicability and lifecycle record complete: YES / NO
MCard applicability decision: APPLIES / NOT_APPLICABLE / BLOCKED
MCard lifecycle decision: COMPLETE / NOT_APPLICABLE / BLOCKED
May proceed to Q12 operation identity gate: YES / NO
Q12 immutable operation identity record complete: YES / NO
Operation identity decision: COMPLETE / NOT_APPLICABLE / BLOCKED
Current operation ID:
Current feature or patch identity:
Current lifecycle generation:
Current transaction ID or N/A:
May proceed to Q13 write authorization gate: YES / NO
Q13 explicit write authorization record complete: YES / NO
Write authorization decision: COMPLETE / NOT_APPLICABLE / BLOCKED
Current authorization ID or N/A:
Allowed write paths or N/A:
Approved Preview identity or N/A:
Human authorization current: YES / NO / N/A
May proceed to Q14 immediate freshness gate: YES / NO
Q14 immediate pre-write freshness record complete: YES / NO
Freshness decision: COMPLETE / NOT_APPLICABLE / BLOCKED
Freshness checked immediately before write: YES / NO / N/A
Current exact-disk target fingerprints match: YES / NO / N/A
Current Preview, generation, transaction, owner, and authorization match: YES / NO / N/A
No intervening identity change: YES / NO / N/A
May proceed to Q15 canonical path-authority gate: YES / NO
Q15 canonical path-authority record complete: YES / NO
Path-authority decision: COMPLETE / NOT_APPLICABLE / BLOCKED
Canonical support-root owner/facade:
Canonical transient-root owner/facade:
Specialized path families delegated: YES / NO / N/A
Duplicate or hardcoded path authorities absent: YES / NO / N/A
May proceed to Q16 resolved-path containment gate: YES / NO
Q16 resolved-path containment record complete: YES / NO
Containment decision: COMPLETE / NOT_APPLICABLE / BLOCKED
Resolved owner root and candidates structurally contained: YES / NO / N/A
Traversal, sibling-prefix, drive, UNC, case, and link escapes rejected: YES / NO / N/A
May proceed to Q17 Preview/Shadow/source separation gate: YES / NO
Q17 Preview/Shadow/source separation record complete: YES / NO
Separation decision: COMPLETE / NOT_APPLICABLE / BLOCKED
Final source, durable Preview, and disposable Shadow authorities distinct: YES / NO / N/A
Preview/Shadow cross-writes and truth leakage absent: YES / NO / N/A
May proceed to Q18 stale asynchronous-result rejection gate: YES / NO
Q18 stale asynchronous-result rejection record complete: YES / NO
Stale-result rejection decision: COMPLETE / NOT_APPLICABLE / BLOCKED
Request/result identity and receiver acceptance predicate current: YES / NO / N/A
Cancel, timeout, and thread settlement remain fail-closed: YES / NO / N/A
Stale result effects blocked: YES / NO / N/A
May proceed to Q19 real Qt/QSignalSpy decision gate: YES / NO
Q19 decision complete and material Qt modes correct: YES / NO / N/A
May proceed to Q20 shared isolated filesystem fixtures gate: YES / NO
Q20 shared isolated filesystem fixture record complete: YES / NO
Fixture isolation decision: COMPLETE / NOT_APPLICABLE / BLOCKED
Protected real roots unchanged and cleanup verified: YES / NO / N/A
May proceed to Q21 parametrized negative boundary matrix gate: YES / NO
Q21 parametrized negative boundary matrix record complete: YES / NO
Boundary matrix decision: COMPLETE / NOT_APPLICABLE / BLOCKED
Self-hosting and external-project negative coverage complete: YES / NO / N/A
Path, generation, transaction, and confirmation bypass blocked: YES / NO / N/A
May proceed to Q22 public-facade and contract-drift tests gate: YES / NO
Q22 public-facade and contract-drift test record complete: YES / NO
Public-facade contract decision: COMPLETE / NOT_APPLICABLE / BLOCKED
Canonical imports, signatures, fallback, consumers, and private-dependency guards complete: YES / NO / N/A
May proceed to Q23 deterministic MCard transition tests gate: YES / NO
Q23 deterministic MCard transition test record complete: YES / NO
MCard transition decision: COMPLETE / NOT_APPLICABLE / BLOCKED
Normal/rollback, invalid-transition, lock, eject, and durable-state tests complete: YES / NO / N/A
May proceed to Q24 property-based MCard pilot decision gate: YES / NO
Q24 property-based MCard pilot decision record complete: YES / NO
Property-based pilot decision: PILOT_RETAINED / PILOT_REJECTED / NOT_APPLICABLE / BLOCKED
Bounded generation, replay/minimization, unique-defect yield, dependency scope, and cost/benefit evidence complete: YES / NO / N/A
May proceed to Q25 mutation-testing pilot decision gate: YES / NO
Q25 mutation-testing pilot decision record complete: YES / NO
Mutation-testing pilot decision: PILOT_RETAINED / PILOT_REJECTED / NOT_APPLICABLE / BLOCKED
Selected guards, isolation, replay, mutation outcomes, repair, and cost/benefit evidence complete: YES / NO / N/A
May proceed to Q26 ZIP containment and collision hardening gate: YES / NO
Q26 ZIP containment/collision hardening record complete: YES / NO
Exact final ZIP and manifest declaration contract pass: YES / NO
Dangerous path, duplicate, case-fold, file/directory, link, and undeclared-payload negatives pass: YES / NO
May proceed to Q27 control-byte and encoding guards: YES / NO
Q27 control-byte and encoding guards record complete: YES / NO
UTF-8 output, BOM-aware legacy reads, UTF-16LE fixture, and C0 rejection pass: YES / NO
Safe Windows path generation uses component-wise Join-Path: YES / NO
Q28 structured exception provenance record complete: YES / NO | Exception provenance decision: COMPLETE / NOT_APPLICABLE / BLOCKED | cause, phase, operation, target, root classification, last successful marker, invocation position, and failure class preserved: YES / NO / N/A | May proceed to Q29 NO-LEAK runtime trace pilot decision: YES / NO
Q29 NO-LEAK runtime trace pilot decision record complete: YES / NO | Runtime trace pilot decision: PILOT_RETAINED / PILOT_REJECTED / NOT_APPLICABLE / BLOCKED | validation-only, bounded, no runtime integration, no security-sandbox claim: YES / NO / N/A | May proceed to Q30 human confirmation and freeze protection gate: YES / NO | Q30 human confirmation and freeze protection record complete: YES / NO | Preview read-only, exact form/project binding, stale-confirmation invalidation, explicit Confirm and Write, no automatic Error Memory or Freeze Memory write: YES / NO / N/A | May proceed to Q31 changed-file-to-validator coverage map: YES / NO
May write source: NO
Lesson freshness and regression dispositions complete: YES / NO
Router bridge selected:
Required prompt path:
Target box:
Forbidden box:
Source files inspected:
Generated-vs-canonical status:
Preview/Shadow classification, when Workbench-related:
Architecture Review card identity, when lifecycle-related:
Card ownership proven:
Current card lifecycle phase:
Open transaction blocks switch/eject:
Terminal eject condition:
Project results retained after eject:
Line-count risk:
GUI-resolution risk, if GUI:
May implement: YES / NO
```
Hard rule:
```text
No governed implementation may begin unless the VERIFIED PROBLEM RECORD is
complete, its admission decision permits the smallest adequate intervention,
the ERROR MEMORY CHECK is complete with explicit lesson dispositions, and May
implement is YES.
```
Unknown, missing, uninspected, or unsafe fields keep `May implement` `NO`; inspect or request the required source or prompt. Source audit lists actual files, never memory alone; unavailable exact source blocks work.
## Generated-vs-canonical requirement — Edit canonical generators/sources and regenerate after validation; never edit only generated copies unless canonical.
## Box boundary requirement — Identify the active and forbidden boxes. Typical boxes include:
```text
prompt-library
startup-delivery
patch-delivery
validation
Error Memory
freeze-memory
GUI
domain logic
```
If the active project is `kanda_reasoner`, the AI must still distinguish the active target project from the reusable KANDA Reasoner tool role. Shared physical root does not remove the need for logical separation.
## Workbench Preview / Shadow ownership bridge — For Workbench Preview, validation, backup, rollback, cleanup, or Shadow work, `project_tool_boundary_canon` is mandatory. Classify every relevant write target with this model:
```text
reusable Workbench engine code
-> <tool_source_root>
selected-project source mutation
-> <active_project_root>
Durable Workbench support state
-> <active_project_support_root>/large_file_refactor_workbench/...
Canonical Preview
-> <active_project_support_root>/large_file_refactor_workbench/preview/<preview_id>/...
Disposable Shadow
-> <transient_garbage_root>/large_file_refactor_shadow/<shadow_id>/...
Staging/extraction/temp helpers/temp validation assembly/regenerable garbage
-> <transient_garbage_root>/...
```
Hard routing rules:
```text
Preview is durable project-support state, not daily-work garbage.
Shadow is disposable and must not become durable Preview authority.
The transient garbage root is ownership-free and garbage-only. It must not own Preview truth, durable Workbench state, Tool source, Project source, canonical validation evidence, canonical Error Memory, or canonical freeze memory.
Self-hosting does not collapse these logical boxes even when tool_source_root and active_project_root physically coincide.
```
If ownership cannot be classified truthfully, `May implement` must be `NO` until the active project root, support root, transient garbage root, and intended state lifetime are resolved.
## Architecture Review project-card machine bridge
For canonical MCard triggers, pair `architecture_review_project_card_machine_canon` with `project_tool_boundary_canon`; add `large_module_refactor_protocol` only when large-module behavior changes. MCARD APPLICABILITY AND LIFECYCLE RECORD
MCard applicable YES/NO | trigger/not-applicable evidence | owner prompts | card identity/ownership/transition/async validity: Planner/Workbench/Preview/Shadow/transaction owners | locks | apply/rollback | write target | terminal eject | Tool memory cleared:
Project results retained after eject: Self-hosting/tests | decision COMPLETE/NOT_APPLICABLE/BLOCKED | proceed to Q12 YES/NO | May implement: NO
Late async results must prove current root/target lifecycle generation. Unresolved lifecycle evidence blocks Q11; applicable work needs `COMPLETE`, non-applicable work needs explicit evidence.
## Immutable operation identity bridge
IMMUTABLE OPERATION IDENTITY RECORD Operation required YES/NO | evidence | operation/feature identity | Tool/Project roots | relative targets/hashes | generation | transaction | owner/immutable fields | current matches | stale rejection | tests
Decision: COMPLETE / NOT_APPLICABLE / BLOCKED | proceed to Q13 YES/NO | May implement: NO Any reused, stale, duplicate, unsafe, mismatched, or unresolved identity blocks Q12.
## Explicit write authorization bridge
EXPLICIT WRITE AUTHORIZATION RECORD
Writes required YES/NO | evidence | authorization/operation/feature IDs | Active Project | bounded paths/route | Preview | hashes | generation | transaction | owner/human authority | current matches | invalidation | tests
Decision COMPLETE/NOT_APPLICABLE/BLOCKED | proceed Q14 YES/NO | May implement/source-write NO
Path/helper/manifest/boolean evidence or stale approval never authorizes mutation.
## Immediate pre-write freshness bridge
IMMEDIATE PRE-WRITE FRESHNESS RECORD
Writes required YES/NO | evidence | immediate phase/time | operation/authorization/feature IDs | Tool/Project roots | targets with owner/classification and expected/current exact-disk hashes | Preview expected/current | generation expected/current | transaction expected/current | public owner/facade/consumers | authority current | no intervening change | stale evidence invalidated | blockers/tests
Decision COMPLETE/NOT_APPLICABLE/BLOCKED | proceed Q15 YES/NO | May implement/source-write NO
Any stale or mismatched source, target, Preview, generation, transaction, owner, authorization, or requirement resets affected gates and blocks Q14.
## Canonical path-authority bridge
CANONICAL PATH-AUTHORITY CONTRACT RECORD
Paths required YES/NO | evidence | base-root owner/facade | unique path-family owners, bounded formulas/adapters, lifetime, containment, tests, and blocked duplicate formulas
Decision COMPLETE/NOT_APPLICABLE/BLOCKED | proceed Q16 YES/NO | May implement/source-write NO
Independent formulas, nested support roots, competing facades, or durable-state use of transient garbage block Q15.
## Resolved-path containment bridge
RESOLVED-PATH CONTAINMENT RECORD
Containment required YES/NO | evidence | operation/authorization | resolved owner | candidates with bounded input, verified parent, resolved path, drive/share/case, type/link status, structural relation, route, and tests
Negative matrix traversal/sibling/absolute/cross-drive/UNC/case/link | decision COMPLETE/NOT_APPLICABLE/BLOCKED | proceed final pre-code authorization YES/NO | May implement/source-write NO
String-prefix, lexical-only, unresolved-link, mismatched-anchor, or resolved-escape evidence blocks Q16.
## Preview, Shadow, and source separation bridge
PREVIEW, SHADOW, AND SOURCE SEPARATION RECORD
Required/N/A evidence | operation/authorization | Active Project/support/transient roots | exactly one FINAL_SOURCE/DURABLE_PREVIEW/DISPOSABLE_SHADOW authority with path, owner, lifetime, truth, mutation, metadata, byte identity, containment, cleanup, tests, and blocked cross-writes
Pairwise distinct | Preview not source truth | Shadow not durable truth | source metadata clean | decision COMPLETE/NOT_APPLICABLE/BLOCKED | proceed Q18 YES/NO | continue implementation YES/NO | source-write authority remains Q13-Q14 only Wrong-box placement, mixed truth, Preview metadata leak, Shadow durability, byte mismatch, or unresolved cross-write authority blocks Q17.
## Stale asynchronous-result rejection bridge
STALE ASYNCHRONOUS-RESULT REJECTION RECORD Required/N/A evidence | identity basis | one route per async result with owner/controller, request and result identity fields, operation/project/target/source fingerprint, lifecycle/worker generation, acceptance predicate, cancellation/timeout authority revocation, thread settlement, late-result action, authorized effects, tests Cross-check: stale result effects blocked for state mutation, gate open, source write, durable evidence write, and current UI repopulation | decision COMPLETE/NOT_APPLICABLE/BLOCKED | proceed Q19 YES/NO | May implement/source-write NO Unresolved identity, callback-only matching, cancellation without authority revocation, timeout acceptance, premature idle projection, or late-result side effects block Q18. Q18 never grants coding or source-write authority.
## Real Qt/QSignalSpy validation decision bridge
REAL QT/QSIGNALSPY VALIDATION DECISION RECORD: required/N/A evidence | one case per Qt behavior with owner/facade, material signal/thread/widget risks, static/mock limits, REAL_QT_QSIGNALSPY/REAL_QT_WIDGET/STATIC_SUFFICIENT mode, real subjects/trigger, signal/thread/widget assertions, cancel-timeout-late scenario, event-loop/watchdog, validator/markers/environment | decision COMPLETE/NOT_APPLICABLE/BLOCKED | proceed Q20 YES/NO | May implement/source-write NO. QSignalSpy is required for material queued delivery, signal count/order/payload, or thread affinity; real widgets are required for click/enabled/visibility/ancestor projection; static evidence cannot satisfy material Qt behavior.
## Shared isolated filesystem fixture bridge
SHARED ISOLATED FILESYSTEM FIXTURE RECORD: required/N/A evidence | shared owner/facade | protected real roots | one case per synthetic validator with sandbox root class, fixture source/support/transient/evidence roots, production paths read-only, fixture-only write targets, scoped owner overrides, before/after snapshots, cleanup/exclusions, tests/markers | decision COMPLETE/NOT_APPLICABLE/BLOCKED | proceed Q21 YES/NO | May implement/source-write NO. Synthetic validators must not mutate real source, support, transient, or drive-root locations; no production path may appear in fixture write targets.
## Parametrized negative boundary matrix bridge
PARAMETRIZED NEGATIVE BOUNDARY MATRIX RECORD: required/N/A evidence | matrix owner/facade | dimensions | one row per control or negative with project mode, path, lifecycle/worker generation, transaction, confirmation, expected blockers, validators and markers | decision COMPLETE/NOT_APPLICABLE/BLOCKED | proceed Q22 YES/NO | May implement/source-write NO. Both SELF_HOSTING and EXTERNAL_PROJECT require controls and negative coverage; confirmation bypass must block even when paths are valid.
## Public-facade and contract-drift bridge
PUBLIC-FACADE AND CONTRACT-DRIFT TEST RECORD: required/N/A evidence | primary box | one case per public facade with owner/path, canonical import, explicit package-root export status, public symbols/__all__, signature/default/annotation/docstring policy, fallback, required consumer subset/current consumers, private helpers, validators/markers | decision COMPLETE/NOT_APPLICABLE/BLOCKED | proceed Q23 YES/NO | May implement/source-write NO. Package-root assumptions, contract drift, fallback loss, missing required consumers, private reach-in, or duplicate public ownership block Q22.
## Deterministic MCard transition bridge
DETERMINISTIC MCARD TRANSITION TEST RECORD: required/N/A evidence | canonical owner/facade | valid/invalid transition inventory | durable artifacts | one case per normal, rollback, switch, eject, stale, skipped, locked, unresolved, and premature path with generations, transaction/apply/rollback/terminal state, expected blockers, Tool-memory effect, durable-project effect, validators/markers | decision COMPLETE/NOT_APPLICABLE/BLOCKED | proceed Q24 YES/NO | May implement/source-write NO. Terminal eject clears target-specific Tool memory only and preserves project source, helpers, Preview, transaction, mutation-lane, and receipt evidence.
## Property-based MCard pilot bridge
PROPERTY-BASED MCARD PILOT DECISION RECORD: applicable/N/A evidence | Q23 baseline | owner/facade | pilot kind and validation-only dependency scope | properties/generator/replay/minimization/bounds | generated cases/sequences | unique meaningful defects vs known findings | measurable gain/cost | decision PILOT_RETAINED/PILOT_REJECTED/NOT_APPLICABLE/BLOCKED | proceed Q25 YES/NO | May implement/source-write NO. No broad adoption without unique meaningful defects.
## Mutation-testing pilot bridge
MUTATION-TESTING PILOT DECISION RECORD: applicable/N/A evidence | Q24 baseline | selected validator/guard inventory | validation-only engine/dependency scope | operators/replay/isolation/bounds | baseline and mutant outcomes | score before/after repair | meaningful gaps/test repairs | gain/cost | decision PILOT_RETAINED/PILOT_REJECTED/NOT_APPLICABLE/BLOCKED | proceed Q26 YES/NO | May implement/source-write NO. Retention requires reproducible non-equivalent survivors repaired by focused tests; full-project default execution is forbidden.
## ZIP containment and collision hardening bridge — ZIP CONTAINMENT AND COLLISION HARDENING RECORD: required/N/A evidence | Q25 baseline | sole canonical patch-governance owner/facade | exact final ZIP | install-manifest authority | dangerous-path, duplicate, Windows case-fold, file/directory, link, and undeclared-install-path protections | validators/markers | decision COMPLETE/NOT_APPLICABLE/BLOCKED | proceed Q27 YES/NO | May implement/source-write NO.
## Control-byte and encoding guards bridge — CONTROL-BYTE AND ENCODING GUARDS RECORD: required/N/A evidence | Q26 baseline | existing evidence reader and PowerShell delivery owners | explicit UTF-8 no-BOM output | BOM-aware UTF-8/UTF-16LE reads | invalid-byte and forbidden-C0 rejection | component-wise Join-Path | validators/markers | decision COMPLETE/NOT_APPLICABLE/BLOCKED | proceed Q28 YES/NO | May implement/source-write NO.
## Structured exception provenance bridge — STRUCTURED EXCEPTION PROVENANCE RECORD: required/N/A evidence | Q27 baseline | existing Error Memory and delivery-wrapper owners | one case per material failure path with phase, operation ID, target, root classification, last successful marker, failure class, exception and original-cause details, invocation position, validators/markers | decision COMPLETE/NOT_APPLICABLE/BLOCKED | proceed Q29 YES/NO | May implement/source-write NO.
## NO-LEAK runtime trace pilot bridge — NO-LEAK RUNTIME TRACE PILOT DECISION RECORD: applicable/N/A evidence | Q28 baseline | Q20/Q21/NO_LEAK owners and separate Runtime Collector relationship | validation-only child-process audit scope | writes/deletes/replacements/archive/subprocess/import inventory | replay/isolation/bounds | unique defects versus known findings | deterministic path-attribution limitation model and separately reported platform-dependent runtime occurrence | child-process limitations | gain/cost | decision PILOT_RETAINED/PILOT_REJECTED/NOT_APPLICABLE/BLOCKED | proceed Q30 YES/NO | May implement/source-write NO. Optional observability only; never claim a security sandbox, integrate a new runtime tracer, or require platform-specific optional audit events. Human confirmation and freeze protection bridge (Q30): HUMAN CONFIRMATION AND FREEZE PROTECTION RECORD | Q29 baseline | Freeze Feature After Update public owner/facade | read-only Preview | explicit Confirm and Write | exact form and selected-project binding | invalidation after form/source-evidence/target/root changes | confirmation/root checks | no automatic Error Memory promotion or frozen-memory write | focused/real-Qt validators and markers | decision COMPLETE/NOT_APPLICABLE/BLOCKED | proceed Q31 YES/NO | May implement/source-write NO.
## Changed-file-to-validator coverage bridge (Q31) - CHANGED-FILE-TO-VALIDATOR COVERAGE MAP: Q30 frozen baseline | exact changed-file set | one row per file with owner box, public contract, relevant Error Memory lessons, frozen behavior, and focused/boundary/GUI/delivery/negative-test dispositions | explicit validator inventory | no broad substring exclusion | every applicable validator mapped | no orphan required validator, unresolved file, or conflicting disposition | decision COMPLETE/NOT_APPLICABLE/BLOCKED | proceed Q32 YES/NO | May implement/source-write NO. Validation and evidence provenance bridge (Q32) - VALIDATION AND EVIDENCE PROVENANCE RECORD: Q31 frozen baseline | feature/operation/project/root identities | exact source fingerprints | Error Memory export and lesson IDs | prompt/validator revisions and hashes | exact commands | environment/interpreter/dependency state | expected and observed markers | durable project-support evidence path/hash/encoding/time | limitations/blockers | decision COMPLETE/NOT_APPLICABLE/BLOCKED | proceed Q33 YES/NO | May implement/source-write NO. ## Line-count and GUI requirements - For Python changes enforce the module-size law: Ideal module size: <= 400 physical lines; Maximum module size: <= 500 physical lines; PEP 8 compliance: canonical; SOLID responsibility/dependency design: canonical; DRY implementation ownership: canonical. Pinned local-model provenance bridge (Q33) - PINNED LOCAL-MODEL PROVENANCE RECORD: Q32 frozen baseline | applicability and no-model evidence | provider/runtime/model ID | exact model digest/revision | tokenizer revision or provider-bundled digest evidence | code and canonical prompt hashes | complete inference settings | offline/local network policy | input fingerprints | raw/normalized output hash/schema | advisory-only authority classification | durable evidence/validators/limitations | decision COMPLETE/NOT_APPLICABLE/BLOCKED | proceed Q34 YES/NO | May implement/source-write NO. Unpinned model evidence remains advisory and cannot authorize source, validation, freeze, routing, or state mutation. Profile-before-optimization bridge (Q34) - PROFILE-BEFORE-OPTIMIZATION RECORD: Q33 frozen baseline | optimization applicability and N/A evidence | named slow path and owner | representative workload/scale | exact source/workload/environment fingerprints | profiler/tool and command | warmups/repeated measurements | metric/unit/median/mean/stdev/CV | variance threshold/acceptance | bottleneck classification/evidence | simpler alternatives | proposed optimization | expected/minimum gain | complexity budget | rollback condition | durable evidence/validators/limitations | decision COMPLETE/NOT_APPLICABLE/BLOCKED | proceed Q35 YES/NO | May implement/source-write NO. Speculative optimization, single-run timing, unrepresentative workload, unknown bottleneck, or undeclared complexity blocks Q34. Focused performance baseline bridge (Q35) - FOCUSED PERFORMANCE BASELINE RECORD: Q34 frozen baseline and exact evidence hash | applicability and N/A evidence | bottleneck name/classification/owner/public contract | owner-local benchmark scope by default | cross-box framework only with demonstrated necessity, canonical owner, and affected-box inventory | representative workload/scale | exact workload/source/environment fingerprints | benchmark tool/command | warmups/repeated measurements | metric/unit/median/mean/stdev/CV | variance threshold/acceptance | correctness guards | read-only or disposable-fixture isolation | production writes forbidden | durable evidence/validators/limitations | decision COMPLETE/NOT_APPLICABLE/BLOCKED | proceed Q36 YES/NO | May implement/source-write NO. Global benchmark services, owner drift, missing Q34 lineage, single-run timing, unstable results, or production mutation block Q35. Module-size and cohesion enforcement bridge (Q36) - MODULE-SIZE AND COHESION RECORD: Q35 frozen baseline | applicability and N/A evidence | exact changed-file and touched-Python sets | one row per touched Python module with owner/role/responsibility/public contract/physical lines after PEP 8 formatting/ideal and maximum decisions/AST and formatter evidence/compression and padding absence/split basis/helper dependency direction/facade decision/over-ideal rationale/refactor route | exact set reconciliation | durable evidence/validators/limitations | decision COMPLETE/NOT_APPLICABLE/BLOCKED | proceed Q37 YES/NO | May implement/source-write NO. Above-500 touched modules, formatting compression, padding, line-range splitting, responsibility-free helpers, facade growth without justification, helper-to-facade back imports, or undeclared Python files block Q36. Canonical ownership reconciliation bridge (Q37) - CANONICAL OWNERSHIP RECONCILIATION RECORD: Q36 frozen baseline | applicability and N/A evidence | exact changed files | responsibility inventory covering duplicate scanners, schemas, reports, state owners, and consumers | one canonical owner per responsibility | canonical owner path/public contract/source of truth/state mutation owner/current consumers | every competitor receives retirement or evidence-backed coexistence disposition | public adapters remain bounded to the canonical contract | consumer migration complete | duplicate state writes disabled | no new coordination super-system or ownership/scanner/schema/report/state registry | durable evidence/validators/limitations | decision COMPLETE/NOT_APPLICABLE/BLOCKED | proceed Q38 YES/NO | May implement/source-write NO. Unresolved competitors, duplicate state authority, missing consumer migration, or a new coordination super-system block Q37. Handoff freshness and provenance bridge (Q38) - HANDOFF FRESHNESS AND PROVENANCE RECORD: Q37 frozen baseline | exact current source fingerprints | handoff artifact generation time and source linkage | manifest hash/time/source-fingerprint linkage | validation evidence hash/time/markers/source linkage | Error Memory manifest hash/time/lesson freshness | active-project Freeze context hash/time/latest freeze ID | source archive remains generated evidence and never current-source authority | stale-artifact inventory and invalidation reasons | no parallel handoff/context/freshness engine | durable evidence/validators/limitations | decision COMPLETE/NOT_APPLICABLE/BLOCKED | proceed Q39 YES/NO | May implement/source-write NO. Any stale or unlinked handoff, manifest, validation, Error Memory, Freeze context, or source archive blocks Q38. Task-specific context admission bridge (Q39) - TASK-SPECIFIC CONTEXT ADMISSION RECORD: Q38 frozen baseline | new-context applicability and N/A evidence | current handoff/manifest/route owner inventory | identical representative task set and exact input/source/environment fingerprints | baseline and candidate repeated results | correctness/coverage/staleness/latency/cost metrics with thresholds and variance | reproduced current-owner inadequacy | simpler strengthening alternatives | unique bounded owner/public contract/lifecycle/invalidation | no intelligence engine, context registry, source mirror, or coordination super-system | durable evidence/validators/limitations | decision ADMITTED/REJECTED/NOT_APPLICABLE/BLOCKED | proceed Q40 YES/NO | May implement/source-write NO. No new context artifact is admitted without controlled, comparable, thresholded evidence. One-primary-box governed release bridge (Q40) - ONE-PRIMARY-BOX GOVERNED RELEASE RECORD: Q39 frozen baseline | exactly one primary box | bounded supporting touches with owner/reason/public contract | exact changed files and source baselines | regression obligations and one-row-per-file validation map | exact final ZIP contract through the canonical validator | root freeze hint and durable project-support evidence | human-local validation state | read-only Preview | explicit Confirm and Write | no automatic frozen-memory write | no project-specific state in project_freeze_ledger | decision READY_FOR_LOCAL_VALIDATION/VALIDATED_READY_FOR_FREEZE/COMPLETE/NOT_APPLICABLE/BLOCKED | May deliver/claim validation/freeze only when the corresponding evidence state permits. No release registry, coordination super-system, generated-as-source authority, transient durable truth, or multi-primary-box release is allowed.
Canonical precedence rule: format and validate Python for PEP 8 before final line counting; never compress layout, remove required blank lines, combine statements, or duplicate logic to fit. If cohesive compliant code exceeds the limit, route through the Large Module Creation and Refactor Protocol.
Hard routing rule: If a new Python code module is expected to exceed 500 lines, do not create it as one file; route to Large Module Creation and Refactor Protocol v8.0, split by responsibility, and define helper/module structure first.
For existing Python modules:
```text
If a touched Python module is already over 500 lines, or the planned change would push it over 500 lines, the implementation gate must route to large_module_refactor_protocol v8.0 and state whether AST Split Audit handoff is available.
If a touched Python module is near the ideal limit, around 400 lines or more, the implementation gate must state line-count risk and whether the change should be split into a smaller helper/module before delivery.
No governed patch may silently create or enlarge a Python code module above 500 lines without an explicit v8.0 staged refactor exception and validation plan.
Additional v8.0 granularity and external Web AI delegation gate:
If a refactor would create several tiny Python helper files, require a practical-granularity check before delivery. Cohesive helper files near the 400-line ideal are acceptable. Do not create tiny helper crumbs, 5-line modules, or extra train cars merely to reduce line count when a responsibility helper can remain cohesive. Runtime/source logic must live in ordinary importable `.py` files; ZIP `payload/` structure is delivery packaging only, not application logic.
```
The Implementation Gate `Line-count risk` field must include current and projected line-count status when Python code is created or modified:
```text
Line-count risk: current N lines; projected M lines after PEP 8 formatting; valid permanent-source range 101-499; PEP 8/SOLID/DRY preserved YES/NO; architecture must be responsibility-first, not line-target-first; v8.0 routing needed YES/NO.
```
When GUI files are changed, GUI-resolution risk must mention laptop-to-4K usability and avoid fixed-size-only assumptions when possible.
## Sequential double-refactor delivery train rule — For independent or ordered large-module refactor patches, route to Protocol v8.0. Allowed train:
```text
Patch ZIP 1: up to two related refactor slices -> install -> validate -> freeze
Patch ZIP 2: up to two related refactor slices -> install -> validate -> freeze
Patch ZIP 3: up to two related refactor slices -> install -> validate -> freeze
Patch ZIP 4: up to two related refactor slices -> install -> validate -> freeze
```
Hard rules:
```text
Maximum per response: 4 ordered patch ZIPs.
Default maximum per ZIP: 2 related refactor slices.
Each ZIP must have its own feature id, install, validation, ZIP contract check, freeze code, KANDA_FREEZE_HINT.json, rollback boundary, and freeze entry.
Do not install the next ZIP until the current ZIP has passed validation and has been frozen.
Stop the train if any ZIP fails install, validation, ZIP contract, freeze-prep, preview, or freeze.
Do not freeze the outer train as one vague entry.
```
## External Web AI large-module planning bridge
For external Web AI plan improvement or an Imported Web AI Version ZIP, route to both:
```text
large_module_refactor_protocol v8.0
KPR-06-001 web_ai_large_module_refactor_exchange_protocol
KPR-06-002 web_ai_planning_response_bundle_blueprint
KPR-06-003 web_ai_ast_split_risk_repair_protocol, when AST Split Audit reports RISK REFACTORING and external source repair is requested
KPR-06-004 safe_refactor_how_to, when the AI needs the complete safe-refactor process/delivery refresher or the user invokes Safe Refactor How To
```
The companion prompt owns the external exchange details: bounded improvement search, exact marker-wrapped response contract, governed ZIP layout, installer destination, validation, and freeze-evidence code. The core large-module canon remains authoritative for public API, module size, atomic clusters, dependency direction, helper granularity, and implementation safety.
Required bridge shape:
```text
native Heuristic or Local AI plan -> Copy Comprehensive Planning for Web AI -> external bounded correction -> installable Imported Web AI Version bundle -> install external pending artifact only
-> Receive Planning from Web AI -> deterministic validation/review -> Load as Imported Web AI Version -> compare/select -> Workbench handoff remains separate
```
Do not allow the external import installer to patch KANDA Python source, selected-project source, Workbench state, freeze memory, or Error Memory Lessons.
## Failure behavior — If the implementation gate cannot pass, do not implement. Output the missing source, missing prompt, unsafe box boundary, or generated-file conflict that must be resolved first.
