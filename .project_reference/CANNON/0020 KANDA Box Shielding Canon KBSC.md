# KANDA Box Shielding Canon (KBSC)

## Complete Recovery and Execution Protocol for Shielding Logic

Canonical name:
KANDA Box Shielding Canon

Short name:
KBSC

Purpose:
This document restores the full shielding method whenever the AI loses control of the method, forgets the steps, confuses shielding with implementation, invades another box, or attempts to continue development without protecting a meaningful milestone.

Master rule:
A box shield is an architectural fitness-function suite for a bounded context.

It protects:

* the box authority boundary
* the box dependency direction
* the box truth-source priority
* the box public contract
* the box side-effect boundary
* the box regression-critical outputs
* the box do-not-invade-other-box boundary

It must not invade neighboring boxes.

---

# 1. Core Definition

A KANDA box shield is not a feature expansion.

A KANDA box shield is a protection milestone.

It is created after a meaningful logic-box milestone and before continuing into stronger, riskier, broader, or cross-box work.

The shield does three things:

1. Defines what the box is allowed to do.
2. Defines what the box is forbidden to do.
3. Adds executable tests and, only when necessary, minimal contract hardening so future patches cannot silently violate the box boundary.

A shield converts a working behavior into protected architecture law.

---

# 2. Why Shielding Exists

KANDA projects are built through incremental patches and freezes.

As a box grows, small changes can accidentally create:

* authority creep
* hidden side effects
* dependency leaks
* cross-box invasion
* stale fallback behavior
* placeholder commitment
* silent regression
* accidental prompt loading
* accidental route decision
* accidental freeze memory mutation
* accidental startup delivery mutation
* stronger ML behavior without governance

The shield prevents this.

The shield is especially important before:

* adding stronger machine-learning logic
* adding embeddings
* adding TF-IDF
* adding vector stores
* adding self-learning
* adding new GUI actions
* adding new caller integration
* connecting advisory output to final workflow decisions
* expanding a box beyond its original purpose

---

# 3. The KANDA Shielding Principle

Use this sentence as the governing principle:

The machine may suggest.
The canon decides.
The box shield prevents regression.
No other box logic is invaded.

For routing and prompt systems:

* advisory output is allowed
* candidate context is allowed
* preview text is allowed
* diagnostic hints are allowed
* explainability is allowed

But unless explicitly governed and frozen:

* final route decisions are forbidden
* final prompt decisions are forbidden
* May proceed now decisions are forbidden
* prompt auto-loading is forbidden
* cross-box mutation is forbidden
* freeze memory writes are forbidden
* startup delivery changes are forbidden
* prompt-library mutations are forbidden

---

# 4. When KBSC Must Be Used

A shield is mandatory when a box reaches a meaningful milestone.

A meaningful milestone exists when the box adds any of the following:

1. A new output type.
2. A new caller.
3. A new data source.
4. A new state machine.
5. A new cross-layer interaction.
6. A new preview/report/decision surface.
7. A new persistence behavior.
8. A new interpretation layer.
9. A new risk boundary.
10. A move toward stronger ML or probabilistic behavior.
11. A feature that could be mistaken for authority.
12. A feature that exposes internal logic to GUI, logs, automation, or another box.
13. A feature that touches validation, freeze, startup, prompt routing, patch delivery, or protected memory.
14. A sequence of individually frozen milestones that now behaves as a combined subsystem.

If any item above is true, stop before continuing and create a shield.

---

# 5. What Shielding Is Not

A shield is not:

* a rewrite
* a refactor for style
* a stronger ML feature
* a new router
* a new freeze workflow
* a new GUI workflow
* a new prompt-library workflow
* an excuse to touch adjacent boxes
* a broad cleanup
* a dependency upgrade
* a corpus tuning patch
* an integration patch disguised as safety
* a way to bypass freeze
* a way to bypass human confirmation

If the patch adds capability, it is probably not a pure shield.

If the patch changes another box's behavior, it is probably not a valid shield.

If the patch changes final authority, it is not a shield.

---

# 6. KBSC Architecture Model

Every shield must describe the box as a bounded context.

A bounded context must define:

1. Owning box.
2. Allowed public contract.
3. Allowed inputs.
4. Allowed outputs.
5. Internal truth sources.
6. External consumers.
7. Forbidden neighboring boxes.
8. Forbidden authority escalation.
9. Forbidden side effects.
10. Protected architecture characteristics.
11. Regression-critical outputs.
12. Validation and freeze requirements.

Example:

Owning context:
routing_signal_scorer

Allowed output:
advisory similarity payloads and preview text

Forbidden neighboring contexts:
freeze_hint_intake
freeze_after_update
freeze_after_update_gui
startup delivery
prompt-library canon/index
project_freeze_ledger
project_freeze_after_update

Allowed relationship:
Other boxes may consume the public advisory output later through a public contract.

Forbidden relationship:
routing_signal_scorer must not mutate or decide for them.

---

# 7. Dependency Direction Rule

Every shield must protect dependency direction.

Rule:

The owning box may expose public output outward.
It must not import, call, mutate, own, or make decisions for neighboring boxes unless that integration has its own governed patch and freeze.

For a shield patch:

Allowed:

* internal owning-box contract hardening
* internal owning-box tests
* public API schema validation
* design documentation inside the owning box
* manifest metadata for the owning box

Forbidden:

* changing neighboring box internals
* calling neighboring private functions
* duplicating another box's domain logic
* writing another box's memory
* modifying another box's GUI
* modifying startup delivery
* modifying prompt-library canon or indexes
* changing project_freeze_ledger as active memory

Dependency direction must be tested or audited.

---

# 8. Truth-Source Priority Ladder

Every shield must document the truth-source priority ladder.

This prevents stale fallback bugs and placeholder regressions.

A truth-source ladder must answer:

1. What is the highest authority?
2. What is the box's own source of truth?
3. What is merely advisory?
4. What is a fallback?
5. What source is stale or forbidden?
6. What happens when sources conflict?
7. What happens when no valid source exists?
8. What placeholders are illegal?

Template:

Truth-source priority for this box:

Level 1:
[highest authority]

Level 2:
[owning box validated source]

Level 3:
[advisory or derived source]

Level 4:
[presentation-only source]

Fallback:
[explicit safe fallback]

Forbidden:
[stale placeholder, starter value, unrelated box memory, body/prose mentions, consumed false state, etc.]

Conflict rule:
Lower levels can never override higher levels.

No valid source rule:
Return explicit NO_MATCH, UNIMPLEMENTED, SAFE_FALLBACK, or validation error.
Never return a placeholder that mimics valid feature data.

---

# 9. Forbidden Authority Escalation Matrix

Every shield must include a forbidden authority escalation matrix.

This matrix says what the box can never decide.

Template:

This box must never decide:

* final route
* required prompts
* May proceed now
* user permission
* human confirmation
* prompt loading
* freeze write
* startup delivery write
* project memory write
* cross-project memory use
* safety override
* validation success
* install success
* final workflow state
* neighboring-box state

For routing_signal_scorer specifically:

The scorer may suggest route-family hints.
The scorer may show candidate prompt-context labels.
The scorer may explain similarity.
The scorer may expose preview text.
The scorer must never decide final route, final prompts, May proceed now, prompt loading, or router override.

---

# 10. Architecture Characteristics

Every shield must define the architecture characteristics it protects.

Examples:

* advisory_only
* deterministic
* idempotent
* side_effect_free
* bounded_execution
* schema_validated_output
* no_authority_escalation
* no_cross_box_mutation
* no_prompt_auto_loading
* no_external_ml_dependency
* no_vector_store
* no_self_learning
* human_confirmed_freeze_only
* public_contract_only
* dependency_direction_preserved
* bounded_context_isolated
* safe_fallback_only

These should appear in:

1. Shield design document.
2. box_manifest.json when appropriate.
3. Test names or validation script.
4. Freeze hint summary.
5. Freeze entry.

---

# 11. Shield Patch Boundary

Before writing a shield patch, define the allowed file boundary.

Template:

Allowed:

* owning_box/contract.py
* owning_box/**init**.py only if exports are required
* owning_box/box_manifest.json only for shield metadata/schema declaration
* owning_box/design/[shield_doc].md
* tests/test_[box]_[shield].py
* KANDA_FREEZE_HINT.json as ZIP delivery metadata only

Forbidden:

* neighboring box folders
* startup delivery
* prompt-library canon/index files
* freeze memory except normal human-confirmed freeze output
* project_freeze_ledger as active project memory
* runtime cache files as architecture evidence
* broad cleanup files
* temporary installer files inside project root

A patch that touches forbidden paths is not a valid shield unless the user explicitly approved a separate governed cross-box integration patch.

---

# 12. Tests-First Rule

Shielding is tests-first.

Procedure:

1. Write the shield tests that express the invariants.
2. Run them against the current box.
3. If tests pass, do not harden unnecessarily.
4. If tests fail because the legal public contract permits forbidden behavior, add minimal contract hardening.
5. If tests fail because another box is involved, do not silently patch that box.
6. If tests fail because the current intended behavior is unclear, inspect targeted freeze entries.
7. After tests and minimal hardening pass, freeze the shield.

Tests define the law.

Contract hardening enforces the law only when needed.

---

# 13. Contract Hardening Trigger

Do not harden contract.py speculatively.

Harden contract.py only when:

* a legal public call can produce invalid output
* forbidden authority fields can leave the box
* output schema can silently drift
* placeholders can mimic valid state
* side effects can occur through public API
* unbounded input can crash the router
* dependency policy can be violated
* ambiguity can be misrepresented as certainty
* downstream callers can mistake output for final authority

Minimal hardening examples:

* validate advisory payload schema
* reject forbidden keys
* force is_authoritative = False
* force requires_canon_review = True
* set automatic_prompt_loading = False
* set route_override = None
* set required_prompts_final_decision = not_provided_by_similarity
* add explicit state field such as NO_MATCH, WEAK_MATCH, STRONG_ADVISORY, AMBIGUOUS_MATCH, ERROR_STATE
* return safe fallback for invalid input
* bound input length
* scan for forbidden dependencies
* keep output deterministic

Do not rewrite the core algorithm unless the shield proves the algorithm violates the contract.

---

# 14. Standard Shield State Machine

Every shield should define a state machine when the box has multiple outcomes.

Generic advisory state machine:

INPUT
|
v
NORMALIZE / VALIDATE INPUT
|
v
EVALUATE BOX LOGIC
|
v
CLASSIFY STATE
|
+--> NO_MATCH
|
+--> WEAK_MATCH
|
+--> STRONG_ADVISORY
|
+--> HIGH_SIGNAL
|
+--> AMBIGUOUS_MATCH
|
+--> ERROR_STATE
|
v
VALIDATE OUTPUT SCHEMA
|
v
RETURN NON-AUTHORITATIVE PAYLOAD

Every terminal state must preserve:

* is_authoritative = False
* requires_canon_review = True
* no final decision fields
* no prompt loading
* no side effects
* no cross-box mutation

---

# 15. Standard Shield Invariants

Use these invariants as the base for all shield patches.

Authority invariants:

1. The box remains within its declared authority.
2. The box never decides what another box owns.
3. The box never escalates advisory output into final output.
4. The box never creates final workflow state unless that is its declared authority.
5. The box never bypasses human confirmation.
6. The box never bypasses validation.
7. The box never bypasses freeze.

Output schema invariants:

8. Public outputs have schema_version when machine-consumed.
9. Public outputs expose authority status explicitly.
10. Public outputs reject forbidden keys.
11. Public outputs do not include placeholders that mimic valid state.
12. Public outputs distinguish NO_MATCH, UNIMPLEMENTED, SAFE_FALLBACK, and ERROR_STATE.
13. Public outputs are stable unless a governed schema version changes.

State invariants:

14. Every meaningful state has a named outcome.
15. Ambiguous states are marked as ambiguous.
16. Missing states fail safely.
17. Error states do not crash parent workflows.
18. Very strong signals do not become authority.

Stability invariants:

19. Same input plus same state gives same output.
20. Repeated calls are idempotent.
21. Representative snapshot outputs are preserved.
22. Threshold or state boundary behavior is tested.
23. Time-dependent drift is forbidden unless explicitly part of the box.
24. Hidden state is forbidden unless explicitly part of the box.

Safety invariants:

25. User input is treated as data.
26. User input is not executed.
27. User input does not become shell commands.
28. User input does not become code.
29. User input does not bypass contract gates.
30. Huge input is bounded.
31. Invalid input returns safe fallback or handled error.
32. Prompt injection text is treated as opaque text.

Side-effect invariants:

33. No file writes unless the box explicitly owns them.
34. No neighboring box mutation.
35. No startup mutation.
36. No prompt-library mutation.
37. No freeze memory mutation except human-confirmed freeze workflow.
38. No global state mutation.
39. No environment mutation.
40. No cross-project memory mutation.

Dependency invariants:

41. No forbidden dependencies.
42. No hidden ML dependency.
43. No vector store.
44. No embeddings.
45. No self-learning.
46. No network dependency unless explicitly governed.
47. No runtime package import outside allowed policy.

Presentation invariants:

48. Preview is display-only.
49. Report text is non-imperative.
50. Human-readable output must not instruct final action unless the box owns that action.
51. Candidate output must be labeled candidate-only.
52. UI preview must not imply write authority.

Boundary invariants:

53. The patch touches only allowed files.
54. Imports follow dependency direction.
55. Cross-box tests call public contracts only.
56. Neighboring internals are not imported.
57. No logic duplication from another box.
58. No fallback path from another box is silently used.

---

# 16. No Placeholder Commitment Rule

Placeholders are dangerous.

A placeholder must never look like valid feature data.

Forbidden examples:

* Current validated feature - replace with exact feature title
* TODO feature title
* starter title
* sample route
* example required prompts
* placeholder validation marker
* fake success output
* fallback freeze ID
* default final route
* empty but valid-looking prompt list

Correct behavior:

* UNIMPLEMENTED
* NO_MATCH
* SAFE_FALLBACK
* VALIDATION_REQUIRED
* MISSING_VALIDATED_SOURCE
* NOT_PROVIDED_BY_THIS_BOX
* CANDIDATE_ONLY
* ADVISORY_ONLY

Rule:

If the box does not know, it must say it does not know.
It must not pretend to know.

---

# 17. Side-Effect Boundary Rule

A shield must prove the box does not produce unauthorized side effects.

Test patterns:

1. Snapshot relevant protected directories before the call.
2. Call the box public function.
3. Snapshot again.
4. Confirm no forbidden files changed.
5. Confirm no new files appeared.
6. Confirm no global state was mutated.
7. Confirm no environment variable was altered.
8. Confirm no forbidden module was imported.
9. Confirm repeated calls remain stable.

For KANDA, protected areas commonly include:

* project_freeze_after_update/frozen_features_memory
* project_freeze_after_update/files_to_send_ai
* project_freeze_ledger
* kanda_prompt_workspace
* prompt-library canon/index files
* startup delivery files
* freeze_hint_intake
* freeze_after_update
* freeze_after_update_gui
* other boxes outside the owning box

---

# 18. Dependency Ceiling Rule

A shield must declare dependency policy.

For runtime-lite advisory boxes, default policy:

* Python standard library only
* no numpy
* no scipy
* no sklearn
* no torch
* no tensorflow
* no faiss
* no sentence_transformers
* no transformers
* no chromadb
* no llama_index
* no langchain
* no vector database
* no embedding backend
* no network dependency

Tests should check:

1. Static source text does not import forbidden dependencies.
2. Runtime sys.modules does not load forbidden dependencies because of this box.
3. box_manifest declares dependency policy when appropriate.
4. Stronger ML status is explicit.

Important:
Do not fail just because packages exist in the environment.
Fail only if the box imports or depends on them.

---

# 19. Security Coverage Matrix

A shield should include a security-inspired coverage matrix when the box processes user text, routing signals, prompts, model outputs, or external content.

Coverage areas:

Prompt injection:

* User text is data, not instructions to the box.
* The box does not execute user text.
* The box does not follow user text as internal instructions.

Insecure output handling:

* Output schema is validated.
* Forbidden authority keys are rejected.
* Preview/report text cannot issue final commands.

Corpus/data poisoning:

* Corpus is frozen or human-reviewed.
* No automated corpus growth.
* No self-learning path.

Denial of service:

* Input length is bounded.
* Execution time is bounded.
* Corpus scan is bounded.
* Safe fallback exists.

Supply chain:

* Dependency ceiling is tested.
* No hidden ML/vector dependencies.
* No network dependency unless governed.

Cross-box injection:

* Advisory payload cannot mutate another box.
* Candidate labels cannot become final prompt loading.
* Preview cannot become write action.

---

# 20. Positive Behavior Snapshot Rule

Computational boxes need positive behavior snapshots.

A shield must preserve representative outputs for curated inputs.

Examples:

* simple no-match input
* weak-match input
* strong-match input
* high-risk input
* ambiguous input
* invalid input
* huge input
* prompt-injection-like input
* known historical regression input
* known Fast Path false-positive input

Snapshot checks can include:

* state
* top match ID
* threshold level
* candidate labels
* advisory flags
* forbidden key absence
* preview text boundaries
* non-authority fields
* schema_version
* stable rendering

Precision rule:
Do not overfit irrelevant formatting.
Lock only fields that matter.

---

# 21. Bounded Execution Rule

A shield must prevent the box from becoming a latency or DoS risk.

Tests should verify:

* empty input returns quickly
* huge input returns safely
* repeated calls do not degrade
* binary-like text does not crash
* very long prompt-injection text is treated as text
* no unbounded recursion
* no unbounded file scan
* no unbounded network call
* no unbounded corpus mutation

Use generous time thresholds to avoid flaky tests.

---

# 22. Non-Imperative Output Rule

If a box produces reports, previews, or explanations, it must not accidentally sound authoritative.

Forbidden language in advisory boxes:

* load this prompt
* proceed now
* you may proceed
* final route is
* required prompts:
* use this route
* confirm and write
* run this command
* install this now
* freeze this now

Allowed language:

* candidate only
* advisory only
* not provided by this box
* canon decides final route
* human review required
* preview only
* no automatic prompt loading
* no May proceed decision

A shield can scan report/preview text for imperative final-action phrases.

---

# 23. Model-Card Style Shield Card

For ML-adjacent boxes, add a local shield card.

Recommended path:

owning_box/design/[feature_id]_shield_card.md

Sections:

1. Feature name.
2. Feature ID.
3. Owning bounded context.
4. Intended use.
5. Out of scope.
6. Public contract.
7. Truth-source priority ladder.
8. Forbidden authority escalation.
9. Architecture characteristics.
10. Corpus or data provenance.
11. Evaluation approach.
12. Snapshot examples.
13. Security coverage.
14. Dependency policy.
15. Known limitations.
16. Trade-offs accepted.
17. Future work allowed only after freeze.
18. Do-not-invade boundary.

This card helps future AI restore intent even if conversation context is lost.

---

# 24. Trade-Off Record

Every shield should document trade-offs intentionally accepted.

Example:

Trade-offs accepted for routing_signal_scorer:

* lexical runtime-lite now instead of embeddings
* deterministic advisory behavior now instead of semantic power
* snapshot validation now instead of runtime corpus hash rejection
* candidate context preview now instead of final prompt selection
* no prompt auto-loading until separately governed
* no stronger ML until shield is frozen
* no cross-box integration in this shield patch

Purpose:
Future AI must understand that these are deliberate architectural choices, not missing features.

---

# 25. Integration vs Invasion

KBSC distinguishes three categories:

1. Owning-box internal hardening

Allowed:

* changes inside the owning box
* public contract validation
* internal invariant tests
* owning-box manifest metadata
* owning-box design card

2. Cross-box integration tests

Allowed only when needed:

* tests that call adjacent public contracts
* read-only checks
* no internal imports
* no writes
* no mutation
* no ownership transfer

3. Forbidden box invasion

Always blocked:

* editing another box's files
* importing another box's internals
* duplicating another box's logic
* writing another box's memory
* deciding another box's state
* changing startup delivery
* changing prompt-library canon
* changing freeze memory outside human-confirmed freeze workflow

If in doubt, treat it as invasion and stop.

---

# 26. Full Freeze Entry Loading Rule

Use compact summaries by default.

Load full freeze entries when:

* compact summary hides needed edge cases
* exact schema is needed
* exact math/thresholds are needed
* the box has more than three behavior-affecting freezes
* the shield covers multiple interacting layers
* the test would otherwise invent historical behavior
* a regression references a specific frozen behavior
* a prior freeze introduced a failure mode not fully visible in summary

Do not load all freeze entries blindly.

Load targeted entries only.

For routing_signal_scorer shield, likely useful targeted entries:

* runtime-lite
* calibration
* threshold policy
* policy-runtime alignment
* explainability
* decision report
* UI preview adapter
* prompt-context preview

For freeze-tab shielding, likely useful targeted entries:

* freeze-hint autofill state machine
* consumed newer scan continuation
* frozen entry body mention guard
* false consumed retry guard
* local freeze workflow

Rule:
Load what you need to prevent contradiction.
Do not load so much that you blur box boundaries.

---

# 27. Standard KBSC Workflow

Use this exact step-by-step workflow.

## Step 1 - Stop feature escalation

Before stronger work, state:

Development is paused for shielding.
No stronger ML or cross-box work proceeds until the shield is frozen.

## Step 2 - Name the shield

Format:

[box]*[subsystem]*[purpose]_shield_v[number]

Example:

routing_signal_scorer_v2_similarity_box_shield_v1

## Step 3 - Define owning bounded context

Write:

Owning box:
[box path]

Allowed files:
[list]

Forbidden boxes:
[list]

Allowed outputs:
[list]

Forbidden outputs:
[list]

## Step 4 - Define protected architecture characteristics

List the characteristics the shield protects.

Example:

* advisory_only
* deterministic
* side_effect_free
* bounded_execution
* no_cross_box_mutation

## Step 5 - Define truth-source priority ladder

Write the source priority and conflict rule.

## Step 6 - Define forbidden authority escalation matrix

List what the box must never decide.

## Step 7 - Define state machine

Define terminal states and safe fallback behavior.

## Step 8 - Define regression matrix

Name every test.

Use stable IDs.

Example:
SM-01
SM-02
SM-03

## Step 9 - Decide tests-only vs minimal hardening

Default:
tests first.

If tests expose legal invalid output:
minimal contract hardening.

## Step 10 - Write shield tests

Tests should cover:

* authority
* schema
* state machine
* side effects
* dependencies
* bounded execution
* no placeholders
* snapshots
* non-imperative output
* do-not-invade audit

## Step 11 - Add minimal contract hardening if required

Only harden what tests prove is needed.

## Step 12 - Add shield card

Document:

* intended use
* out of scope
* truth ladder
* forbidden authority
* trade-offs
* limitations
* dependency policy
* future work rule

## Step 13 - Update manifest only if useful

Add:

* shield_version
* authority
* architecture_characteristics
* forbidden_authority
* stronger_ml_status
* dependency_policy

## Step 14 - Build patch ZIP

ZIP contains only updated files plus KANDA_FREEZE_HINT.json.

KANDA_FREEZE_HINT.json is delivery metadata only.

Do not install KANDA_FREEZE_HINT.json into project root.

## Step 15 - Validate

Validation must run:

* new shield tests
* prior owning-box tests
* relevant adjacent regression tests if the patch delivery may affect them
* freeze-hint state-machine tests when KANDA_FREEZE_HINT delivery behavior is involved
* no forbidden dependency tests
* no side-effect tests
* no box-invasion tests

## Step 16 - Freeze

After install and validation pass:

Freeze Feature After Update
Preview Freeze Entry
Confirm and Write

Do not freeze placeholder titles.

## Step 17 - Verify freeze output

Expected:

LOCAL FREEZE WRITE OK
Freeze ID: [shield freeze id]
Freeze hint intake record marked as used
AI-send exposure refreshed
Startup freeze context refreshed
FREEZE_MEMORY_STATUS: OK

## Step 18 - Continue only after freeze

Only after shield is frozen may the next stronger feature begin.

---

# 28. Required Shield Patch Artifacts

Every KBSC patch should normally include:

1. Test file:
   tests/test_[box]_[shield].py

2. Optional minimal contract hardening:
   owning_box/contract.py

3. Optional export update:
   owning_box/**init**.py

4. Optional manifest metadata:
   owning_box/box_manifest.json

5. Shield card:
   owning_box/design/[shield_id]_shield_card.md

6. ZIP delivery metadata:
   KANDA_FREEZE_HINT.json

7. Install PowerShell block.

8. Validation PowerShell block.

9. Validation marker:
   VALIDATION OK: [feature_id]

10. Contract marker:
    CONTRACT_TEST_OK: [summary]

11. Sandbox marker:
    SANDBOX_[FEATURE_ID_UPPER]_VALIDATION_OK

---

# 29. KBSC Validation Template

A validation suite should prove:

1. New shield test passes.
2. All prior owning-box tests pass.
3. Protected adjacent regression tests pass if relevant.
4. KANDA_FREEZE_HINT.json exists inside ZIP.
5. KANDA_FREEZE_HINT.json is not installed into project root.
6. ZIP payload contains only expected files.
7. No forbidden paths changed.
8. No forbidden dependencies loaded.
9. No forbidden authority keys appear.
10. No side effects occurred.
11. No placeholders are accepted.
12. Snapshot outputs are stable.
13. Schema version is present.
14. Safe fallback works.
15. Freeze hint metadata has validation evidence.

---

# 30. KBSC Recovery Procedure

If the AI loses control of shielding, do this:

1. Stop implementation.

2. Restate:
   I am restoring KBSC.

3. Identify current box.

4. Identify latest frozen milestone.

5. Identify whether a meaningful milestone was reached.

6. If yes, do not continue feature development.

7. Define shield name.

8. Define owning bounded context.

9. Define forbidden neighboring boxes.

10. Define architecture characteristics.

11. Define truth-source ladder.

12. Define forbidden authority escalation matrix.

13. Define state machine.

14. Define regression matrix.

15. Decide tests-first.

16. Add minimal hardening only if tests prove gap.

17. Validate.

18. Freeze.

19. Only then continue.

Recovery phrase:

KBSC RESTORE MODE ACTIVE.
No feature escalation until shield boundary, invariants, regression matrix, validation, and freeze are complete.

---

# 31. KBSC Failure Modes and Corrections

Failure:
AI starts implementing next ML feature before shield.

Correction:
Stop. Create shield first.

Failure:
AI touches another box.

Correction:
Stop. Re-scope to owning box. If cross-box work is truly needed, create separate governed integration patch.

Failure:
AI writes tests but no invariants.

Correction:
Define invariants first. Tests must map to invariants.

Failure:
AI hardens contract without tests.

Correction:
Write tests first. Harden only to fix legal invalid output.

Failure:
AI adds dependencies.

Correction:
Reject unless dependency is explicitly governed. Shield patches should avoid new dependencies.

Failure:
AI adds runtime corpus hash enforcement without governance.

Correction:
Use snapshot validation first. Runtime hash enforcement is a separate feature.

Failure:
AI treats advisory output as final.

Correction:
Add forbidden authority tests and schema validation.

Failure:
AI produces placeholder as valid data.

Correction:
Apply No Placeholder Commitment Rule.

Failure:
AI changes prompt-library or startup files.

Correction:
Box invasion. Reject patch.

Failure:
AI freezes placeholder title.

Correction:
Stop. Do not freeze. Diagnose freeze hint intake.

Failure:
AI loads all freeze entries and loses boundary.

Correction:
Load targeted entries only.

---

# 32. KBSC Application to Routing Signal Scorer

Feature:
Routing Signal Scorer v2 Similarity Box Shield v1

Feature ID:
routing_signal_scorer_v2_similarity_box_shield_v1

Owning box:
kanda_reasoner_app/routing_signal_scorer

Allowed:

* kanda_reasoner_app/routing_signal_scorer/contract.py
* kanda_reasoner_app/routing_signal_scorer/**init**.py only if exports are required
* kanda_reasoner_app/routing_signal_scorer/box_manifest.json
* kanda_reasoner_app/routing_signal_scorer/design/routing_signal_scorer_v2_similarity_box_shield_card.md
* tests/test_routing_signal_scorer_v2_similarity_box_shield.py
* KANDA_FREEZE_HINT.json as delivery metadata only

Forbidden:

* freeze_hint_intake
* freeze_after_update
* freeze_after_update_gui
* kanda_prompt_workspace
* project_freeze_ledger
* project_freeze_after_update except human-confirmed freeze output
* startup delivery
* prompt-library canon/index files
* corpus tuning files unless specifically justified
* router canon changes

Protected characteristics:

* advisory_only
* deterministic
* idempotent
* side_effect_free
* bounded_execution
* schema_validated_output
* no_authority_escalation
* no_cross_box_mutation
* no_prompt_auto_loading
* no_external_ml_dependency
* no_vector_store
* no_self_learning
* public_contract_only
* dependency_direction_preserved
* bounded_context_isolated

Truth-source ladder:

Level 1:
Deterministic KANDA routing canon decides final route, required prompts, missing context, and May proceed now.

Level 2:
routing_signal_scorer frozen corpus and calibration policy provide advisory evidence only.

Level 3:
runtime-lite similarity computes deterministic lexical advisory score.

Level 4:
decision report, UI preview, and prompt-context preview present advisory evidence only.

Conflict rule:
Lower levels never override higher levels.

No valid match:
Return NO_MATCH or safe advisory fallback.

Ambiguous match:
Return AMBIGUOUS_MATCH, show ambiguity, suppress prompt-context labels.

Forbidden authority:
The scorer never decides final route, required prompts, May proceed now, prompt loading, or router override.

State machine:

NO_MATCH:
No useful match. Advisory only. No labels.

WEAK_MATCH:
Candidate hint only. No final decision.

STRONG_ADVISORY:
Top match and explanation. Still advisory only.

HIGH_SIGNAL:
High-risk context visibility. Rule hooks remain independent.

AMBIGUOUS_MATCH:
Top results close. Ambiguous flag true. Suppress prompt-context labels.

ERROR_STATE:
Safe fallback. No crash. No side effects.

Regression matrix additions:

SM-25 Deterministic snapshot baseline.
SM-26 Idempotency.
SM-27 Ambiguous match handling.
SM-28 Error resilience.
SM-29 Forbidden fields.
SM-30 Schema version.
SM-31 No placeholder commitment.
SM-32 Input sanitization boundary.
SM-33 No side effects.
SM-34 Dependency ceiling.
SM-35 Decision report non-imperative language.
SM-36 Candidate label control.
SM-37 High-score authority cap.
SM-38 Box invasion audit.
SM-39 Bounded execution.
SM-40 No actionable command surface.
SM-41 Security coverage declaration.
SM-42 KANDA scorer card exists.
SM-43 Stdlib-only fuzz/property loop.
SM-44 Runtime forbidden dependency scan.
SM-45 Dependency direction guard.
SM-46 Architecture fitness metadata.
SM-47 Bounded context map.
SM-48 Trade-off record.
SM-49 Public-contract-only integration.

Validation must also preserve all prior routing_signal_scorer tests.

---

# 33. KBSC Naming Convention

Use this naming pattern:

[box]*[subsystem]*[scope]_shield_v[number]

Examples:

routing_signal_scorer_v2_similarity_box_shield_v1
freeze_hint_intake_state_machine_box_shield_v1
startup_delivery_source_map_box_shield_v1
prompt_library_routing_index_box_shield_v1
freeze_after_update_gui_form_loader_box_shield_v1

Freeze title pattern:

[Human Title] Box Shield v[number]

Example:

Routing Signal Scorer v2 Similarity Box Shield v1

---

# 34. KBSC Freeze Hint Requirements

KANDA_FREEZE_HINT.json for a shield must include:

* kind
* feature_id
* feature_title
* feature_type = shield
* owning_box
* patch_boundary
* forbidden_boxes
* validation_evidence_summary
* protected_architecture_characteristics
* forbidden_authority
* stronger_ml_status if relevant
* dependency_policy if relevant
* freeze_warning
* expected_freeze_title

Example validation marker:

VALIDATION OK: routing_signal_scorer_v2_similarity_box_shield_v1

Example contract marker:

CONTRACT_TEST_OK: routing signal scorer box shield preserves advisory-only authority boundary, dependency direction, no side effects, no prompt loading, no final route or prompt decisions, no stronger ML dependencies, and prior routing-scorer regressions

---

# 35. KBSC Final Checklist Before Patch Delivery

Before delivering a shield patch, answer YES to all:

1. Is the owning box clear?
2. Are forbidden boxes listed?
3. Is the patch boundary minimal?
4. Is the state machine defined?
5. Is the truth-source ladder defined?
6. Is forbidden authority listed?
7. Are architecture characteristics declared?
8. Are tests written first?
9. Is contract hardening minimal?
10. Does the patch avoid stronger capability?
11. Does the patch avoid new dependencies?
12. Does validation check no side effects?
13. Does validation check no forbidden imports?
14. Does validation check no forbidden output keys?
15. Does validation check no placeholders?
16. Does validation check deterministic behavior?
17. Does validation check bounded behavior?
18. Does validation check prior owning-box regressions?
19. Does ZIP contain only expected files?
20. Is KANDA_FREEZE_HINT.json delivery metadata only?
21. Is freeze title exact?
22. Is the user instructed to freeze after validation?
23. Is stronger work blocked until freeze?

If any answer is NO, do not deliver the patch.

---

# 36. KBSC Final Canon

A KANDA shield is an architectural fitness-function suite for a bounded context.

It is required after meaningful milestones and before stronger or cross-box work.

It protects:

* authority boundary
* dependency direction
* truth-source priority
* public contract
* side-effect boundary
* regression-critical outputs
* forbidden authority escalation
* no-placeholder behavior
* no-invasion behavior

It uses:

* tests-first
* minimal contract hardening
* stable validation markers
* delivery metadata
* human-confirmed freeze

It forbids:

* feature escalation during shielding
* neighboring box mutation
* hidden dependencies
* silent placeholders
* advisory-to-authority creep
* prompt auto-loading unless separately governed
* final decisions from advisory boxes
* unvalidated stronger ML

Final sentence:

The shield makes future change safe by making forbidden behavior executable-fail,
visible, and frozen.
