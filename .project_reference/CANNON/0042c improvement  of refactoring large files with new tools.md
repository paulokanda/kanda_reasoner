Final Book-Level Validation

I completed the final validation pass without writing code or changing the current project.

One important methodological note first: there is no authoritative universal ranking of “the five best books” for this exact combination of Python refactoring, static analysis, architecture governance, and PySide6 workflow design. I therefore used cross-source convergence: recognized publisher/author authority, recurrence in professional recommendations, subject relevance, and reader reputation where useful. For example, Refactoring has a strong Goodreads reputation and appears highly on multiple programming/software-craft lists; Working Effectively with Legacy Code has thousands of ratings; Clean Architecture and A Philosophy of Software Design also have substantial reader bases.

The specialist audits remain important inputs, particularly their consensus around analyzer isolation, status separation, baseline deltas, subprocess safety, and evidence provenance, but I am not treating any one audit as authoritative.

1. The 10-book validation set
Five books closest to the subject task
Refactoring: Improving the Design of Existing Code — Martin Fowler
Working Effectively with Legacy Code — Michael Feathers
Architecture Patterns with Python — Harry Percival and Bob Gregory
Clean Code in Python, 2nd Edition — Mariano Anaya
Robust Python — Patrick Viafore

These cover disciplined behavior-preserving change, legacy-code safety, Python architecture boundaries, code-quality contracts, type checking, and robust Python system design. Their publishers and official catalogs explicitly position them around refactoring, maintainability, Python architecture, testing, type checking, and robustness.

Five books closest to the KANDA architecture/shielding problem
Fundamentals of Software Architecture — Mark Richards and Neal Ford
Building Evolutionary Architectures, 2nd Edition — Neal Ford, Rebecca Parsons, Patrick Kua, and Pramod Sadalage
Software Architecture in Practice, 4th Edition — Len Bass, Paul Clements, and Rick Kazman
A Philosophy of Software Design, 2nd Edition — John Ousterhout
Clean Architecture — Robert C. Martin

This set covers modularity, coupling, architecture characteristics, automated governance, fitness functions, incremental evolution, quality attributes, architecture risk, information hiding, module depth, boundaries, dependency direction, and framework/tool isolation.

2. Audit of the current plan against the 10 books
Book 1 — Refactoring
Relevant principle

Fowler describes refactoring as controlled restructuring through small behavior-preserving transformations rather than large speculative rewrites.

Real gain for KANDA: YES

This strongly validates:

Preview H1
    ->
bounded correction
    ->
Preview H2
    ->
invalidate H1 evidence
    ->
rerun validation

It also supports rejecting:

analyzer directly rewrites canonical source

and:

five tools mutate one another's outputs in sequence
Change to plan

ADOPT: every accepted automated correction creates a new Preview generation.

The Advanced Quality Review becomes an evidence producer, not a source rewriter.

Book 2 — Working Effectively with Legacy Code
Relevant principle

The book centers on bringing difficult existing code under control through testability and practical techniques for making changes safely rather than rewriting everything. The official book description emphasizes practical strategies for changing and refactoring existing applications, while the book structure repeatedly addresses creating test harnesses around difficult code.

Real gain for KANDA: YES

This reinforces a point that the analyzer design alone could obscure:

static-analysis success is not behavioral-equivalence proof.

KANDA must maintain:

static evidence
+
structural evidence
+
Shadow/runtime evidence
+
behavior evidence

rather than replacing runtime validation with Ruff + Griffe + Grimp + mypy + Vulture.

Change to plan

ADOPT: Advanced Quality Review remains before the expensive Completion Evidence runtime/behavior stage, but never replaces that stage.

Book 3 — Architecture Patterns with Python
Relevant principle

The book explicitly covers coupling, abstractions, dependency inversion, ports and adapters, fakes, service layers, and dependency injection.

Real gain for KANDA: YES

This supports keeping the analyzer ecosystem behind KANDA-owned interfaces:

KANDA policy/service
        |
        v
Analyzer adapter contract
        |
        v
Ruff / Griffe / Grimp / mypy / Vulture

The Tool should not let the rest of the Workbench know Ruff command syntax or Grimp implementation details.

Change to plan

ADOPT: external analyzers are adapter-side details.

The pure quality-review service owns use-case orchestration. Tool-specific syntax remains inside adapters.

Book 4 — Clean Code in Python
Relevant principles

The book covers automated checks, type consistency, design by contract, preconditions/postconditions, separation of concerns, cohesion and coupling, SOLID principles, and architecture refactoring.

Real gain for KANDA: YES

The most useful addition is not another generic “clean code” layer.

The useful gain is explicit contracts around each analysis stage.

For example:

Analyzer Preconditions
- environment compatible
- Preview identity sealed
- baseline identity current
- controlled analysis view ready
- configuration hash known

Analyzer Postconditions
- process terminated/reaped
- evidence schema valid
- evidence bound to identity
- analyzed inputs unchanged
- execution status explicit
Change to plan

ADOPT: each adapter gets explicit precondition/postcondition validation enforced by shared runtime and service logic.

Book 5 — Robust Python
Relevant principles

The book explicitly covers type annotations, configuring type checkers, practical type-checking adoption, extensibility, pluggable Python, and multiple testing levels.

Real gain for KANDA: YES

It supports two important decisions:

First:

mypy absolute cleanliness

should not be a universal assumption.

Type checking can be adopted incrementally and strategically.

Second, typed evidence contracts and stable interfaces are useful for a multi-engine system.

Change to plan

ADOPT: mypy becomes capability-driven:

Project type-check capability:
AUTHORITATIVE
AVAILABLE_NON_AUTHORITATIVE
NOT_CONFIGURED
UNAVAILABLE

It is not blindly mandatory for every Python repository.

Architecture literature
Book 6 — Fundamentals of Software Architecture
Relevant principles

The book treats modularity in terms of cohesion, coupling, structural characteristics, architectural characteristics, measurement, governance, trade-offs, and risk—not merely file size.

Real gain for KANDA: YES, major

This changes how we should think about the analyzer aggregator.

The system should not produce a vague scalar:

Quality Score: 84/100

That would hide trade-offs and evidence dimensions.

Instead:

Quality Decision

Local static correctness: PASS
Public API preservation: PASS
Import topology: WARNING
Type regression: PASS
Dead-code advisory: 3 findings
Execution completeness: COMPLETE
Overall authorization status: PASS_WITH_WARNINGS
Change to plan

ADOPT: multidimensional evidence, not one synthetic quality score.

Book 7 — Building Evolutionary Architectures
Relevant principles

The book centers on fitness functions, incremental change, appropriate coupling, and automated architectural governance. Its second edition explicitly includes automated governance and API-consistency validation examples.

Real gain for KANDA: YES, major

This is perhaps the closest conceptual match for KANDA's planned Advanced Quality Review.

The analyzers should be understood as fitness-function engines, not just tools.

For example:

Ruff
    -> local static fitness

Griffe
    -> public contract fitness

Grimp
    -> dependency topology fitness

mypy
    -> type-contract regression fitness

Vulture
    -> dead-code advisory fitness
Change to plan

ADOPT: define each analyzer's explicit architectural fitness responsibility.

The Cross-Check Engine combines evidence; it does not blur tool responsibilities.

Book 8 — Software Architecture in Practice
Relevant principles

The SEI work emphasizes disciplined architecture design, analysis, evolution, quality attributes, and risk. SEI material associated with this body of work uses explicit quality-attribute scenarios because merely naming qualities such as modifiability is insufficiently specific.

Real gain for KANDA: YES

This suggests replacing vague goals such as:

Analyzer system must be safe.

with scenarios:

Scenario:
Preview changes while Ruff is running.

Stimulus:
active Preview hash changes H1 -> H2.

Required response:
- cancel or allow isolated run to terminate;
- discard H1 result at acceptance boundary;
- never persist H1 as evidence for H2;
- report STALE execution status;
- keep GUI responsive.

Another:

Scenario:
mypy exceeds timeout.

Required response:
- terminate contained process tree;
- classify TIMED_OUT;
- no synthetic PASS;
- overall decision INDETERMINATE if mypy is mandatory.
Change to plan

ADOPT: define architecture-quality scenarios before implementation and derive tests from them.

Book 9 — A Philosophy of Software Design
Relevant principle

Ousterhout's material emphasizes managing complexity through information hiding and module boundaries; the book extract explicitly says the decision to split or join modules should be based on complexity, information hiding, and dependency reduction.

Real gain for KANDA: YES, and it corrects our planning method

This is the most important correction to the current module planning process.

We currently have a hard project rule:

101–499 physical lines

That rule remains binding.

But the architecture should not be:

file predicted >500
    ->
split wherever convenient

nor:

one external tool
    ->
one module

The correct order is:

1. Find genuine information-hiding and ownership boundary.
2. Choose cohesive responsibility.
3. Check 101–499 constraint.
4. If oversized, find the next real logical boundary.
5. If undersized, merge with the nearest cohesive owner.
Change to plan

ADOPT: line count becomes a delivery constraint, not the primary architecture algorithm.

This modifies how the proposed module set will be finalized.

Book 10 — Clean Architecture
Relevant principle

The Dependency Rule separates higher-level policy from external details and supports testability and replacement of external mechanisms.

Real gain for KANDA: YES

External analyzers are details:

Ruff
Griffe
Grimp
mypy
Vulture

The policy core should not depend directly on their Python packages.

Therefore:

Quality policy/evidence model
        does not import
Ruff/Griffe/Grimp/mypy/Vulture

Instead:

Quality policy
        |
        v
KANDA adapter interface
        |
        v
process protocol
        |
        v
external analyzer runtime
Change to plan

ADOPT: enforce dependency direction with an import-boundary validator.

3. Conflict synthesis
Conflict A — When should Advanced Quality Review run?

The specialist audits disagreed. Some recommended running analyzers immediately after the internal quality gate; others argued that malformed structural Preview output should be rejected first.

Final resolution

I prioritize:

cheap internal structural correctness;
then advanced static analysis;
then expensive Shadow/runtime/behavior validation.

Final order:

Real Preview
    ->
Internal Preview Quality Gate
    ->
Structural Preview Validation
    ->
Advanced Quality Review
    ->
Preflight
    ->
Payload
    ->
Completion Evidence / Shadow / Runtime / Behavior

Why: this combines Fowler/Feathers' behavior-preservation emphasis with evolutionary architecture's automated fitness functions and avoids spending runtime-validation cost on a Preview already statically invalid.

Conflict B — one module per analyzer vs grouped modules

The audits disagreed between one adapter per tool and grouped adapters.

Final resolution

I prioritize Ousterhout's complexity/information-hiding criterion plus the KANDA 101–499 constraint.

Therefore:

Griffe: separate module;
Grimp: separate module;
mypy/type checking: separate module;
Ruff + Vulture: may share a lint-analysis module only if implementation proves cohesion and 101–499 compliance;
otherwise split along a real responsibility boundary.

This is superior to mechanically equating “one tool” with “one module.”

Conflict C — merge service and Qt worker?

The audits disagree.

Final resolution

Keep them separate.

Service
    pure Python use-case orchestration

Worker
    Qt/QThread ownership and signals

GUI
    presentation and commands

I prioritize Python ports/adapters separation and Clean Architecture dependency direction here.

Conflict D — where should the analyzer environment live?

Audits proposed both Project Support and transient garbage.

Final resolution

Both are rejected for the primary runtime.

Tool-owned analyzer runtime support
    analyzer installation

Project Support
    durable project evidence

Transient garbage
    caches, clones, temporary output

This resolution comes from KANDA's own ownership canon, reinforced by Python's virtual-environment isolation model. Python's documentation establishes isolation behavior, but the exact ownership choice is a KANDA architectural decision.

Conflict E — static analyzer process strategy

The audits ranged from Python APIs, to subprocesses for everything, to process pools.

Final resolution

For v1:

one Qt worker
    ->
one pure orchestration service
        ->
bounded subprocess runtime
            ->
external analyzer environment

No ProcessPoolExecutor.

No QThread per analyzer.

The exact concurrency default is deliberately not canonized without measurement.

Python's subprocess documentation supports explicit timeout/cleanup handling, and Windows documentation confirms that child-process-tree cleanup requires deliberate containment.

4. What changed after the book audit

The literature pass produces six meaningful changes beyond the previous final plan.

Change 1 — Analyzer checks become named architecture fitness functions

Before:

run tools
aggregate reports

After:

each engine has:
- protected characteristic
- input identity
- execution contract
- result semantics
- blocker/advisory authority

Source basis: Building Evolutionary Architectures.

Change 2 — Add explicit architecture-quality scenarios

Before:

must handle stale results
must support timeout

After:

specific stimulus-response scenarios become validation requirements.

Source basis: SEI quality-attribute scenario discipline.

Change 3 — Multidimensional decision instead of aggregate score

Before, the architecture left open the possibility of combined scoring.

After:

Execution completeness
Local static quality
Public API
Import topology
Type regression
Dead-code advisory
Overall authorization

remain separately visible.

Source basis: architecture characteristics and trade-off thinking.

Change 4 — Module splitting logic corrected

The 101–499 rule remains absolute for this project, but logical decomposition comes first.

logical boundary
    ->
information hiding
    ->
cohesion/coupling
    ->
then line-count compliance

Source basis: Ousterhout's complexity and information-hiding guidance.

Change 5 — Explicit analyzer contracts

Every adapter now requires defined preconditions and postconditions.

Source basis: Clean Code in Python design-by-contract treatment.

Change 6 — External analyzers are architectural details

The policy core must not import analyzer packages.

Source basis: Clean Architecture's dependency direction and Python ports/adapters architecture.

5. Final objective proposal
Objective

Build Advanced Quality Review as a governed architectural-fitness subsystem inside the Large File Refactor Workbench.

Its purpose is:

Analyze one immutable, structurally valid Refactor Preview using multiple independent, version-pinned analyzers; compare baseline and Preview evidence where meaningful; correlate results without hiding disagreement; persist immutable provenance-bound evidence; and block, warn, or advise before the refactor proceeds to expensive runtime/behavior validation and eventual human authorization.

The final architecture is:

STRUCTURALLY VALID PREVIEW H1
        |
        v
QUALITY REVIEW PREFLIGHT
        |
        +--> runtime compatibility
        +--> exact tool versions
        +--> config identity
        +--> baseline identity
        +--> Preview identity
        |
        v
BOUNDED ANALYZER EXECUTION
        |
        +--> Ruff
        +--> Griffe
        +--> Grimp
        +--> mypy, when authoritative
        +--> Vulture advisory
        |
        v
NORMALIZED EVIDENCE
        |
        v
BASELINE/PREVIEW DELTA
        |
        v
CROSS-CHECK FITNESS RULES
        |
        v
EXECUTION STATUS
        +
MULTIDIMENSIONAL QUALITY DECISION
        |
        v
DURABLE PROJECT EVIDENCE
        |
        v
PREFLIGHT/PAYLOAD
        |
        v
SHADOW/RUNTIME/BEHAVIOR EVIDENCE
        |
        v
DIFF REVIEW + AI REVIEW + HUMAN AUTHORIZATION

Why this approach:

Fowler: refactoring should remain controlled and behavior-preserving.
Feathers: existing-code change needs characterization and behavioral control, not static analysis alone.
Percival/Gregory and Martin: policy should remain separated from external infrastructure details through boundaries and adapters.
Ford et al.: architectural qualities can be protected through automated fitness functions and incremental governance.
SEI: architectural goals need specific scenarios and risk-oriented validation rather than vague labels.
Ousterhout: module boundaries should reduce complexity and hide information, not merely satisfy numerical size targets.

Final recommendation: IMPLEMENT WITH THE SYNTHESIZED ARCHITECTURE ABOVE.

The architectural review phase is now mature enough to move to implementation planning and source-level inspection, but not directly to coding without a human approval gate.

How Deliver Project to AI Use

This is the final implementation roadmap.

Phase 1 — Canonical implementation basis
1. Record the approved feature objective

Create one feature definition for:

Advanced Quality Review for Large File Refactor Workbench

Protected purpose:

provide deterministic, provenance-bound,
multi-analyzer architectural fitness evidence
for a sealed Refactor Preview
without mutating canonical project source
2. Record explicit non-goals

The first implementation must not:

auto-rewrite canonical source
run Ruff --fix on source truth
replace Structural Validation
replace Shadow/runtime/behavior validation
replace human review
create an opaque numeric quality score
treat missing analyzer output as PASS
allow H1 evidence to authorize H2
install packages silently during analysis
3. Freeze the stage position conceptually

Insert the future stage here:

Real Preview
    ->
Internal Preview Static Quality Gate
    ->
Structural Preview Validation
    ->
Advanced Quality Review
    ->
Preflight Backup

Do not move the expensive Shadow/runtime/behavior stages before Advanced Quality Review.

4. Define architecture-quality scenarios before code

At minimum specify and validate these scenarios:

Preview changes while analyzer is running.
Analyzer executable is unavailable.
Analyzer version differs from lock contract.
Ruff returns findings and exit code semantics are valid.
Analyzer returns malformed machine-readable output.
Analyzer exceeds timeout.
Analyzer process spawns descendants and is cancelled.
Baseline source drifts during analysis.
Preview drifts during analysis.
Analyzer unexpectedly modifies its controlled input.
Mandatory analyzer fails.
Optional advisory analyzer fails.
Evidence from H1 is loaded while H2 is active.
Tool runtime exists but Project configuration is incompatible.
GUI user cancels during process execution.
Project card is switched while analysis owns execution.
Durable evidence write fails.
transient garbage is deleted between sessions.

Each scenario needs:

stimulus
precondition
expected response
execution status
quality-decision effect
persistence effect
GUI effect
Phase 2 — Source inspection and boundary proof
5. Inspect the exact current Workbench source

Before coding, inspect current versions of:

workbench_gui.py
workbench_completion_gui.py
workbench_gui_progression.py
real_preview_generation.py
structural_preview_validation.py
preflight backup path
source payload path
completion evidence path
card lifecycle owner
project/tool boundary owner
project-support path owner
transient-garbage path owner

No implementation from memory.

6. Identify the current public Workbench contracts

Document exact public entry points for:

current card identity
current target
current baseline hash
current Preview root
current Preview hash
Structural Validation status
project support root
transient garbage root
card-switch invalidation
worker ownership
completion evidence progression

The new subsystem may consume public contracts only.

No private reach-in.

7. Prove ownership paths

Before implementation:

Tool source:
analyzer integration code

Tool runtime support:
pinned analyzer environment

Project Support:
durable evidence

Transient Garbage:
caches
controlled analysis views
temporary exchange
temporary process artifacts

Project source:
read-only canonical baseline authority

Add No-Leak checks for each.

Phase 3 — Analyzer runtime design
8. Define the reproducible analyzer environment contract

Specify:

runtime identity
Python interpreter identity
lock identity
Ruff version
Griffe version
Grimp version
mypy version
Vulture version
environment schema version

Do not provision it implicitly during analysis.

9. Build environment capability evidence

The environment layer must return structured evidence:

engine
available
version
compatible
execution path
capability mode
configuration source
cache-routing support
mandatory/conditional/advisory role
10. Build the shared controlled process runtime

One cohesive module owns:

spawn
environment
cwd
timeout
cancellation
bounded concurrency
stdout
stderr
output-size limit
exit code
process cleanup
process-tree containment
duration
resource diagnostics where available

Adapters do not duplicate these concerns.

11. Validate Windows process-tree cleanup separately

Create a controlled test:

parent test process
    spawns
child process
    spawns
grandchild

Cancel through the KANDA process runtime.

Validation must prove no descendants survive.

Do not canonize a specific Win32 technique until this passes locally.

Phase 4 — Evidence core
12. Implement immutable evidence models

Use standard Python:

dataclasses
Enums
Protocols where justified
explicit JSON serialization
schema_version

No Pydantic dependency in v1.

13. Separate execution and quality dimensions

Implement separate models:

ExecutionStatus
QualityDecision

Never mix:

TOOL_UNAVAILABLE

with:

BLOCKED

in one enum.

14. Define AnalysisIdentity

At minimum:

project_card_identity
target_relative_path
baseline_hash
preview_hash
refactor_plan_hash
analyzer_lock_hash
analyzer_config_hash
schema_version
15. Define finding provenance

Each normalized finding carries:

engine
engine_version
rule_id
normalized_relative_path
symbol_identity
normalized_message_signature
location
analysis_identity
raw evidence reference

Line number is location metadata, not semantic identity.

Phase 5 — Analyzer adapters
16. Implement Ruff fitness adapter

Responsibilities:

baseline check
Preview check
JSON evidence parsing
format-check evidence if enabled
delta preparation
no --fix
no source mutation

Fitness characteristic:

local static source quality
17. Implement Griffe API fitness adapter

Responsibilities:

baseline API model
Preview API model
breaking-change extraction
public export change
signature change
parameter/default change
alias/export change
uncertainty evidence

Fitness characteristic:

public contract preservation
18. Implement Grimp topology fitness adapter

Responsibilities:

baseline graph
Preview graph
new edges
removed edges
new prohibited paths
cycle evidence
layer evidence
facade bypass evidence

Fitness characteristic:

dependency topology integrity

Box Logic and No-Leak Logic remain policy owners.

19. Implement conditional mypy fitness adapter

First classify project capability:

AUTHORITATIVE
AVAILABLE_NON_AUTHORITATIVE
NOT_CONFIGURED
UNAVAILABLE

Then run baseline/Preview comparison only under the correct capability policy.

Fitness characteristic:

type-contract regression
20. Implement Vulture advisory adapter

Preserve raw engine confidence.

Do not interpret it as statistical probability.

Fitness characteristic:

newly orphaned code candidate advisory

Maximum unilateral authority:

ADVISORY
Phase 6 — Delta logic
21. Implement analyzer-specific delta strategies

Do not force every engine into one simplistic comparison algorithm.

Ruff:
structured rule/path/symbol/message comparison

Griffe:
native breakage semantics

Grimp:
graph-set and topology comparison

mypy:
semantic relocation-aware comparison

Vulture:
symbol/scope candidate comparison
22. Implement conservative mypy relocation matching

Statuses:

EXACT_MATCH
RELOCATED_MATCH
AMBIGUOUS_MATCH
NEW_FINDING
RESOLVED_FINDING

Never transform:

AMBIGUOUS_MATCH

into:

RELOCATED_MATCH

automatically.

Phase 7 — Cross-check architecture
23. Implement typed Tool-owned fitness rules

Version 1 rules live in Python source.

No YAML.

Every rule declares:

rule_id
required engines
required finding patterns
execution completeness requirements
result severity
explanation template
24. Start with a small rule set

Examples:

PUBLIC_API_REMOVED
+
EXTERNAL_CONSUMER_EDGE
=
BLOCKED
NEW_PROHIBITED_IMPORT_CYCLE
=
BLOCKED
NEW_TYPE_REGRESSION
+
PUBLIC_CONTRACT_SYMBOL
=
BLOCKED or REVIEW_REQUIRED
according to authoritative type-check contract
VULTURE_UNUSED_PRIVATE
+
NO_INBOUND_EDGE
+
NOT_PUBLIC_API
=
ADVISORY_HIGH

Do not create speculative rules without a concrete failure scenario.

25. Preserve analyzer disagreement

The combined view must show:

Ruff: PASS
Griffe: WARNING
Grimp: BLOCKER
mypy: INDETERMINATE
Vulture: ADVISORY

before displaying:

Overall:
BLOCKED

No information compression that hides disagreement.

Phase 8 — Service and worker
26. Build pure orchestration service

The service must not import PySide6.

Sequence:

validate input identity
prepare controlled views
request analyzer execution
collect execution evidence
rehash baseline/Preview
reject stale evidence
run delta analysis
run cross-check rules
build final immutable evidence
request durable persistence
27. Build Qt worker shell

Worker responsibilities only:

QThread ownership
progress signals
stage signals
cancellation bridge
final evidence signal
failure signal
stale GUI-return guard

No analyzer policy.

28. Use bounded concurrency

Do not canonize an arbitrary value such as 3.

Define:

max_parallel_analyzers

with a conservative initial default selected during benchmark validation.

The architecture must support:

1
2
3
...

without redesign.

Phase 9 — Persistence and caches
29. Route analyzer caches to transient garbage

Conceptual path:

*_delete_after_daily_work/
analyzer_cache/
<engine>/
<engine-version>/
<config-hash>/
<analysis-key>/

Caches remain completely regenerable.

30. Route durable evidence to Project Support

Conceptual path:

*_show_project_to_AI/
large_file_refactor_workbench/
quality_evidence/
<project-card-id>/
baseline/
previews/
<preview-hash>/

Store:

capability manifest
execution evidence
normalized findings
delta evidence
cross-check evidence
quality decision
invalidation state
31. Use immutable run records

Never overwrite an old H1 run to make it look like H2.

Instead:

H1 remains historical
H1 becomes STALE for authorization
H2 receives new evidence
Phase 10 — GUI integration
32. Add one primary action
[ Run Advanced Quality Review ]

not five equally prominent buttons.

33. Add execution controls
[ Cancel ]

and progress:

Environment Preflight
Ruff
API Review
Import Graph
Type Review
Dead Code
Delta
Cross-Check
Persistence
34. Show two independent statuses
Execution:
SUCCEEDED

Quality:
PASS_WITH_WARNINGS

Never one ambiguous status.

35. Show multidimensional evidence

Example:

Local static quality: PASS
Public API: PASS
Import topology: WARNING
Type regression: PASS
Dead-code advisory: 3

Then overall authorization status.

36. Keep detailed engine views separate

The main GUI remains concise.

Detailed evidence views handle:

Ruff
API Diff
Import Topology
Type Delta
Dead Code
Combined Evidence
Phase 11 — File architecture validation
37. Apply logical decomposition first

For every module:

identify owner
identify hidden knowledge
identify public interface
identify change reason
identify dependencies

Then enforce:

101–499 physical lines
38. Reject fake size-compliance splits

Not allowed:

helper_a.py
helper_b.py
helper_c.py

created only to satisfy line count.

Every split must have a real ownership or information-hiding boundary.

39. Merge undersized modules cohesively

If implementation produces a module under 101 lines:

find nearest cohesive owner
merge there
rerun architecture review

Do not pad files.

Phase 12 — Validation
40. Unit-test adapters with controlled outputs

Each adapter gets fixtures for:

clean output
warning output
blocking output
malformed output
unexpected exit code
stderr diagnostics
timeout
version mismatch
41. Validate process runtime independently

Test:

timeout
cancel
process descendants
large stdout
large stderr
non-zero exit
zero exit with stderr
Unicode paths
spaces in paths
Windows path handling
42. Validate identity and stale-result logic

Test:

start H1
switch to H2 before completion
H1 finishes
result discarded
no H1 evidence authorized for H2
43. Validate source immutability

Hash:

canonical source before
canonical source after

and controlled analysis views before/after.

Any unexpected mutation:

ANALYZER_MUTATION_DETECTED

and hard failure.

44. Validate each fitness rule independently

Feed synthetic normalized evidence combinations into the Cross-Check Engine.

Assert exact:

ExecutionStatus
QualityDecision
blockers
warnings
advisories
explanation
45. Run real Windows PySide workflow validation

Exercise:

Load Plan
Dependency Readiness
Real Preview
Structural Validation
Advanced Quality Review
Preflight
Payload
Completion Evidence
Assisted Review
Transaction Summary

Confirm:

GUI responsive
cancel works
no stale evidence
no project-source mutation
card lifecycle preserved
Phase 13 — Governed delivery
46. Return Implementation Preview before patching

AI provides:

exact files to touch
new files
owner box
public interfaces
expected physical line counts
dependency environment changes
validation plan
freeze feature proposal
Error Memory implications

Human reviews and approves or rejects.

47. Only after human confirmation, implement

The AI role is to:

inspect exact source
implement complete feature
build self-installing ZIP
include INSTALL
include VALIDATE
include freeze hint
run contract guards
deliver beginner-safe commands

The human does not write code.

48. Follow the standard release train
ZIP
    ->
INSTALL
    ->
VALIDATE
    ->
Error Memory review/memorize where applicable
    ->
Freeze Preview
    ->
Human review
    ->
Confirm and Write
49. Freeze only after real evidence

Freeze requires:

all mandatory validators PASS
real Windows widget validation PASS
source immutability proof PASS
evidence merge PASS
STATUS: IN_SYNC

No freeze from static source inspection alone.

50. Canonize the feature only after human acceptance

The frozen entry should preserve:

analyzer environment isolation;
no direct source mutation;
structurally valid Preview prerequisite;
immutable Preview identity;
execution-status/quality-decision separation;
multidimensional evidence;
baseline/Preview delta semantics;
typed cross-check rules;
bounded subprocess execution;
Windows process-tree cleanup;
Project Support evidence ownership;
transient garbage cache ownership;
Qt-safe worker execution;
stale-result rejection;
continued Shadow/runtime/behavior validation;
explicit human review and transaction confirmation.
Final conclusion

After the specialist audits, official web documentation, and the ten-book literature pass, the strongest architecture is not “install five tools and run them one after another.”

It is:

a governed architectural-fitness subsystem in which independently isolated analyzers inspect the same immutable, structurally valid Preview; produce provenance-bound evidence; compare against a stable baseline where appropriate; remain individually visible; are correlated through explicit typed rules; and feed, but never replace, KANDA's existing structural, runtime, behavioral, AI-assisted, and human authorization gates.

That is the logic I recommend canonizing as the implementation basis.