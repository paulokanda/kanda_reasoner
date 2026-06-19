# KANDA BOX SHIELDING CANON (KBSC) v1.0

Status: canonical shielding method for KANDA Reasoner / PyArchitect box-safe development.
Load mode: on_request / routed for meaningful box milestones, shield creation, stronger-ML preparation, authority-boundary protection, cross-layer advisory systems, and regression-critical subsystem hardening.
Owner folder: 04_box_architecture_and_boundaries

---

## 0. Recovery command

When the AI loses control of the shielding method, forgets how shielding is done, tries to continue a stronger feature without a shield, or starts touching another box during a shield, restore this prompt and say:

```text
KBSC RESTORE MODE ACTIVE.
No feature escalation until shield boundary, invariants, regression matrix, validation, and freeze are complete.
```

Then stop feature work and follow this canon.

---

## 1. Core definition

A KANDA box shield is an architectural fitness-function suite for a bounded context.

It is not a feature expansion.
It is not a refactor for style.
It is not stronger ML.
It is not a cross-box integration patch.

A shield protects:

- the box authority boundary;
- the box dependency direction;
- the box truth-source priority;
- the box public contract;
- the box side-effect boundary;
- the box regression-critical outputs;
- the box do-not-invade-other-box boundary.

Master rule:

```text
The machine may suggest.
The canon decides.
The box shield prevents regression.
No other box logic is invaded.
```

A shield converts working behavior into protected architecture law.

---

## 2. When KBSC is mandatory

Use KBSC after any meaningful box milestone and before stronger, riskier, broader, or cross-box work.

A meaningful milestone exists when a box adds any of these:

1. a new output type;
2. a new caller;
3. a new data source;
4. a new state machine;
5. a new cross-layer interaction;
6. a new preview, report, or decision surface;
7. a new persistence behavior;
8. a new interpretation layer;
9. a new risk boundary;
10. a move toward stronger ML or probabilistic behavior;
11. behavior that could be mistaken for authority;
12. output exposed to GUI, logs, automation, or another box;
13. changes touching validation, freeze, startup, prompt routing, patch delivery, or protected memory;
14. a sequence of individually frozen milestones that now behaves as a combined subsystem.

If any item is true, stop before continuing and create a shield.

---

## 3. What a shield must never become

A shield must not:

- add stronger ML;
- add embeddings;
- add vector stores;
- add self-learning;
- tune a corpus unless explicitly justified;
- rewrite unrelated internals;
- change another box's behavior;
- change final authority;
- bypass validation;
- bypass human freeze confirmation;
- become a broad cleanup;
- place temporary files in project root;
- store active project memory in `project_freeze_ledger`.

If the patch adds new capability, verify it is not falsely labeled as a shield.
If the patch touches another box, stop and re-scope or create a separate governed integration patch.

---

## 4. Bounded context map

Every shield must name its bounded context.

Required fields:

```text
Owning box:
Allowed public contract:
Allowed inputs:
Allowed outputs:
Internal truth sources:
External consumers:
Forbidden neighboring boxes:
Forbidden authority escalation:
Forbidden side effects:
Protected architecture characteristics:
Regression-critical outputs:
Validation and freeze requirements:
```

The owning box may expose public output outward.
It must not import, call, mutate, own, or decide for neighboring boxes unless a separate governed integration patch explicitly approves and freezes that relationship.

---

## 5. Dependency direction rule

The shield must preserve dependency direction.

Allowed in a shield:

- internal owning-box contract hardening;
- internal owning-box tests;
- public API schema validation;
- design documentation inside the owning box;
- manifest metadata for the owning box.

Forbidden in a shield unless separately governed:

- changing neighboring box internals;
- calling neighboring private functions;
- duplicating another box's domain logic;
- writing another box's memory;
- modifying another box's GUI;
- modifying startup delivery;
- modifying prompt-library canon or indexes from a non-prompt-library shield;
- changing `project_freeze_ledger` as active project memory.

---

## 6. Truth-source priority ladder

Every shield must document source priority.

Template:

```text
Level 1 - Highest authority:
Level 2 - Owning box validated source:
Level 3 - Advisory or derived source:
Level 4 - Presentation-only source:
Fallback:
Forbidden source:
Conflict rule:
No valid source rule:
```

Conflict rule:
Lower levels can never override higher levels.

No valid source rule:
Return explicit `NO_MATCH`, `UNIMPLEMENTED`, `SAFE_FALLBACK`, or a validation error. Never return a placeholder that mimics valid feature data.

---

## 7. Forbidden authority escalation matrix

Every shield must list what the box can never decide.

Common forbidden authorities:

- final route;
- required prompts;
- May proceed now;
- human confirmation;
- prompt loading;
- freeze write;
- startup delivery write;
- project memory write;
- cross-project memory use;
- safety override;
- validation success;
- install success;
- final workflow state;
- neighboring-box state.

For advisory routing boxes, the output may suggest candidate context but must never make final routing decisions.

---

## 8. Architecture characteristics

Every shield must declare the architecture characteristics it protects.

Common characteristics:

- `advisory_only`
- `deterministic`
- `idempotent`
- `side_effect_free`
- `bounded_execution`
- `schema_validated_output`
- `no_authority_escalation`
- `no_cross_box_mutation`
- `no_prompt_auto_loading`
- `no_external_ml_dependency`
- `no_vector_store`
- `no_self_learning`
- `human_confirmed_freeze_only`
- `public_contract_only`
- `dependency_direction_preserved`
- `bounded_context_isolated`
- `safe_fallback_only`

These characteristics should appear in the shield design/card, tests, manifest metadata when useful, validation evidence, and freeze entry.

---

## 9. Tests-first rule

Shielding is tests-first.

Workflow:

1. Write tests that express the invariants.
2. Run tests against current box behavior.
3. If tests pass, do not harden unnecessarily.
4. If a legal public call can produce forbidden behavior, add minimal contract hardening.
5. If tests fail because another box is involved, do not silently patch that box.
6. If intended behavior is unclear, inspect targeted freeze entries.
7. After tests and minimal hardening pass, freeze the shield.

Tests define the law.
Contract hardening enforces the law only when needed.

---

## 10. Minimal contract hardening trigger

Harden `contract.py` only when:

- a legal public call can produce invalid output;
- forbidden authority fields can leave the box;
- output schema can silently drift;
- placeholders can mimic valid state;
- side effects can occur through public API;
- unbounded input can crash the router;
- dependency policy can be violated;
- ambiguity can be misrepresented as certainty;
- downstream callers can mistake output for final authority.

Minimal hardening examples:

- validate advisory payload schema;
- reject forbidden keys;
- force `is_authoritative = False`;
- force `requires_canon_review = True`;
- force `automatic_prompt_loading = False`;
- force `route_override = None`;
- force final-prompt decisions to `not_provided_by_this_box`;
- add explicit states such as `NO_MATCH`, `WEAK_MATCH`, `STRONG_ADVISORY`, `AMBIGUOUS_MATCH`, and `ERROR_STATE`;
- return safe fallback for invalid input;
- bound input length;
- scan for forbidden dependencies;
- keep output deterministic.

Do not rewrite the core algorithm unless the shield proves the algorithm violates the contract.

---

## 11. Standard advisory state machine

When a box has multiple outcomes, define a state machine.

Generic advisory state machine:

```text
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
  +--> WEAK_MATCH
  +--> STRONG_ADVISORY
  +--> HIGH_SIGNAL
  +--> AMBIGUOUS_MATCH
  +--> ERROR_STATE
  |
  v
VALIDATE OUTPUT SCHEMA
  |
  v
RETURN NON-AUTHORITATIVE PAYLOAD
```

Every terminal state must preserve:

- `is_authoritative = False` when the box is advisory;
- `requires_canon_review = True` when final decisions belong to canon;
- no final decision fields;
- no prompt loading;
- no unauthorized side effects;
- no cross-box mutation.

---

## 12. Standard shield invariants

Use these invariant categories as the base for all shield patches.

### Authority invariants

- The box remains within its declared authority.
- The box never decides what another box owns.
- The box never escalates advisory output into final output.
- The box never creates final workflow state unless that is its declared authority.
- The box never bypasses human confirmation, validation, or freeze.

### Output schema invariants

- Public outputs have `schema_version` when machine-consumed.
- Public outputs expose authority status explicitly.
- Public outputs reject forbidden keys.
- Public outputs do not include placeholders that mimic valid state.
- Public outputs distinguish `NO_MATCH`, `UNIMPLEMENTED`, `SAFE_FALLBACK`, and `ERROR_STATE`.

### State invariants

- Every meaningful state has a named outcome.
- Ambiguous states are marked as ambiguous.
- Missing states fail safely.
- Error states do not crash parent workflows.
- Very strong signals do not become authority.

### Stability invariants

- Same input plus same frozen state gives same output.
- Repeated calls are idempotent.
- Representative snapshot outputs are preserved.
- Threshold or state boundary behavior is tested.
- Hidden state is forbidden unless explicitly part of the box.

### Safety invariants

- User input is treated as data.
- User input is not executed as shell, code, macro, or internal instructions.
- Huge input is bounded.
- Invalid input returns safe fallback or handled error.
- Prompt-injection text is treated as opaque text.

### Side-effect invariants

- No file writes unless the box explicitly owns them.
- No neighboring box mutation.
- No startup mutation.
- No prompt-library mutation unless the owning box is the prompt-library routing/update box.
- No freeze memory mutation except human-confirmed freeze workflow.
- No global or environment mutation.
- No cross-project memory mutation.

### Dependency invariants

- No forbidden dependencies.
- No hidden ML dependency.
- No vector store.
- No embeddings.
- No self-learning.
- No network dependency unless explicitly governed.

### Presentation invariants

- Preview is display-only.
- Report text is non-imperative.
- Candidate output is labeled candidate-only.
- UI preview must not imply write authority.

### Boundary invariants

- Patch touches only allowed files.
- Imports follow dependency direction.
- Cross-box tests call public contracts only.
- Neighboring internals are not imported.
- No logic duplication from another box.

---

## 13. No Placeholder Commitment Rule

A placeholder must never look like valid feature data.

Forbidden valid-looking placeholders include:

- `Current validated feature - replace with exact feature title`
- `TODO feature title`
- starter title
- sample route
- example required prompts
- placeholder validation marker
- fake success output
- fallback freeze ID
- default final route
- empty but valid-looking prompt list

Correct behavior:

- `UNIMPLEMENTED`
- `NO_MATCH`
- `SAFE_FALLBACK`
- `VALIDATION_REQUIRED`
- `MISSING_VALIDATED_SOURCE`
- `NOT_PROVIDED_BY_THIS_BOX`
- `CANDIDATE_ONLY`
- `ADVISORY_ONLY`

If the box does not know, it must say it does not know.
It must not pretend to know.

---

## 14. Side-effect boundary rule

A shield must prove the box does not produce unauthorized side effects.

Test pattern:

1. Snapshot relevant protected directories before the call.
2. Call the box public function.
3. Snapshot again.
4. Confirm no forbidden files changed.
5. Confirm no new forbidden files appeared.
6. Confirm no global state was mutated.
7. Confirm no environment variable was altered.
8. Confirm no forbidden module was imported.
9. Confirm repeated calls remain stable.

Common protected areas:

- `project_freeze_after_update/frozen_features_memory`
- `project_freeze_after_update/files_to_send_ai`
- `project_freeze_ledger`
- `kanda_prompt_workspace`
- startup delivery files
- prompt-library canon/index files
- `freeze_hint_intake`
- `freeze_after_update`
- `freeze_after_update_gui`
- other boxes outside the owning box

---

## 15. Dependency ceiling rule

Runtime-lite/advisory shields should default to a strict dependency ceiling.

Forbidden unless separately governed:

- numpy
- scipy
- sklearn / scikit-learn
- torch
- tensorflow
- faiss
- sentence_transformers
- transformers
- chromadb
- llama_index
- langchain
- vector database
- embedding backend
- network dependency

Do not fail merely because packages exist in the environment.
Fail only if the owning box imports or depends on them.

---

## 16. Security coverage matrix

For boxes that process user text, prompts, routing signals, or model output, include security coverage.

Prompt injection:
User text is data, not internal instructions.

Insecure output handling:
Output schema is validated and forbidden authority keys are rejected.

Corpus/data poisoning:
Corpus is frozen or human-reviewed; no automated corpus growth.

Denial of service:
Input length and execution time are bounded.

Supply chain:
Dependency ceiling is tested.

Cross-box injection:
Advisory payload cannot mutate another box or become prompt loading.

---

## 17. Positive behavior snapshot rule

Computational boxes need representative output snapshots.

Snapshot examples:

- no-match input;
- weak-match input;
- strong-match input;
- high-risk input;
- ambiguous input;
- invalid input;
- huge input;
- prompt-injection-like input;
- historical regression input;
- Fast Path false-positive input.

Lock only fields that matter.
Do not overfit harmless wording.

---

## 18. Non-imperative output rule

Advisory reports and previews must not sound like final instructions.

Forbidden advisory phrases include:

- load this prompt
- proceed now
- you may proceed
- final route is
- required prompts:
- use this route
- confirm and write
- run this command
- install this now
- freeze this now

Allowed phrases include:

- candidate only
- advisory only
- not provided by this box
- canon decides final route
- human review required
- preview only
- no automatic prompt loading
- no May proceed decision

---

## 19. Shield card requirement

For ML-adjacent, routing-adjacent, or multi-layer boxes, create a local shield card.

Recommended path:

```text
owning_box/design/[feature_id]_shield_card.md
```

Required sections:

1. Feature name.
2. Feature ID.
3. Owning bounded context.
4. Intended use.
5. Out of scope.
6. Public contract.
7. Truth-source priority ladder.
8. Forbidden authority escalation.
9. Architecture characteristics.
10. Corpus or data provenance if applicable.
11. Evaluation approach.
12. Snapshot examples.
13. Security coverage.
14. Dependency policy.
15. Known limitations.
16. Trade-offs accepted.
17. Future work allowed only after freeze.
18. Do-not-invade boundary.

---

## 20. Trade-off record

Every shield should document intentional trade-offs.

Examples:

- lexical runtime-lite now instead of embeddings;
- deterministic advisory behavior now instead of semantic power;
- snapshot validation now instead of runtime corpus hash rejection;
- candidate context preview now instead of final prompt selection;
- no prompt auto-loading until separately governed;
- no stronger ML until shield is frozen;
- no cross-box integration in this shield patch.

Future AI must understand these are deliberate choices, not missing features.

---

## 21. Integration versus invasion

KBSC distinguishes three categories.

### Owning-box internal hardening

Allowed:

- changes inside the owning box;
- public contract validation;
- internal invariant tests;
- owning-box manifest metadata;
- owning-box design card.

### Cross-box integration tests

Allowed only when needed:

- tests that call adjacent public contracts;
- read-only checks;
- no internal imports;
- no writes;
- no mutation;
- no ownership transfer.

### Forbidden box invasion

Always blocked:

- editing another box's files;
- importing another box's internals;
- duplicating another box's logic;
- writing another box's memory;
- deciding another box's state;
- changing startup delivery;
- changing prompt-library canon from a non-prompt-library task;
- changing freeze memory outside human-confirmed freeze workflow.

If in doubt, treat it as invasion and stop.

---

## 22. Full freeze entry loading rule

Use compact summaries by default.

Load targeted full freeze entries when:

- compact summary hides needed edge cases;
- exact schema is needed;
- exact math or thresholds are needed;
- the box has more than three behavior-affecting freezes;
- the shield covers multiple interacting layers;
- the test would otherwise invent historical behavior;
- a regression references a specific frozen behavior.

Do not load all freeze entries blindly.
Load only what prevents contradiction.

---

## 23. Standard KBSC workflow

Use this exact workflow.

1. Stop feature escalation.
2. Name the shield.
3. Define owning bounded context.
4. Define protected architecture characteristics.
5. Define truth-source priority ladder.
6. Define forbidden authority escalation matrix.
7. Define state machine.
8. Define regression matrix.
9. Decide tests-only versus minimal hardening.
10. Write shield tests.
11. Add minimal contract hardening if required.
12. Add shield card when applicable.
13. Update manifest only when useful.
14. Build patch ZIP with only updated files plus `KANDA_FREEZE_HINT.json`.
15. Validate new shield tests, prior owning-box tests, and relevant adjacent regressions.
16. Freeze through human-confirmed Freeze Feature After Update.
17. Verify `LOCAL FREEZE WRITE OK` and `FREEZE_MEMORY_STATUS: OK`.
18. Continue stronger work only after freeze.

---

## 24. Prompt-routing behavior for KBSC

When a user asks to create, improve, canonize, review, or implement shielding logic, use Routed Work Path.

Required prompts/groups for implementation or prompt-system canonization of shielding:

1. `kanda_box_shielding_canon`
2. `04_box_architecture_and_boundaries`
3. `07_prompt_authoring_and_audit`, if the KBSC prompt or routing registration itself is being created or updated
4. `02_prompt_routing_and_indexing`, if routing indexes or prompt-call behavior are being updated
5. `03_governance_freeze_and_handoff`, if freeze, validation evidence, handoff, or governance behavior is involved
6. `05_patch_delivery_and_validation`, if a patch ZIP, install block, validation block, or source-file change is required
7. active project freeze context, if frozen behavior may be changed or shielded
8. relevant owning-box source files and tests
9. validation command or manual validation steps

May proceed now:
NO for implementation until the relevant owning-box context and validation path are available.
PARTIAL only for architectural discussion or drafting.
YES only for Fast Path explanation or reading-only review.

---

## 25. Routing Signal Scorer application

For `routing_signal_scorer_v2_similarity_box_shield_v1`, KBSC requires protecting:

- advisory-only behavior;
- deterministic/idempotent output;
- schema-validated advisory payloads;
- no final route decision;
- no final prompt decision;
- no May proceed now decision;
- no automatic prompt loading;
- no router override;
- no side effects;
- no cross-box mutation;
- no forbidden ML/vector dependencies;
- no self-learning;
- no placeholder commitment;
- bounded execution;
- non-imperative preview/report text;
- controlled candidate labels;
- public-contract-only integration;
- dependency direction;
- bounded context map;
- trade-off record;
- shield card.

The similarity scorer may emit only bounded, deterministic, schema-validated, advisory-only evidence.

It must never emit an instruction, authority signal, prompt-loading action, routing decision, May-proceed decision, file mutation, learned state mutation, or cross-box side effect.

---

## 26. Final canon

A KANDA shield is an architectural fitness-function suite for a bounded context.

It is required after meaningful milestones and before stronger or cross-box work.

It uses:

- tests-first;
- minimal contract hardening;
- stable validation markers;
- delivery metadata;
- human-confirmed freeze.

It forbids:

- feature escalation during shielding;
- neighboring box mutation;
- hidden dependencies;
- silent placeholders;
- advisory-to-authority creep;
- prompt auto-loading unless separately governed;
- final decisions from advisory boxes;
- unvalidated stronger ML.

The shield makes future change safe by making forbidden behavior executable-fail, visible, and frozen.
