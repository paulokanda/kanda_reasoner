# ML LAB Phase Boundary / Charter Entry Gate v1

Feature ID: `routing_signal_scorer_v3_ml_lab_phase_boundary_charter_entry_gate_v1`

This box is the documentation-only entry gate for the post-P12 ML LAB phase.

It exists because RG-LAB-000 canonized the required roadmap:

```text
P12 frozen
→ RG-LAB-000 canonization
→ LAB-0 charter only
→ LAB/test reliability
→ ML router prompt logic reliability
→ only then continue ML logic implementation
```

## LAB-0 status

LAB-0 is not a lab implementation.

LAB-0 creates only phase-boundary and charter documentation. It does not create Python lab code, schemas, fixtures, corpus files, runners, metrics engines, candidate harnesses, provider adapters, prompt loaders, persistent ML decision storage, activation keys, field-test flags, runtime Pilot behavior, or Copilot behavior.

## Next safe milestone

After this LAB-0 entry gate is locally validated and frozen with `FREEZE_MEMORY_STATUS: OK`, the next safe milestone is:

```text
LAB-0A — Success Criteria Matrix
```

LAB-0A remains documentation/governance design. It must still not implement a runner, schema code, fixtures, corpus, candidate harness, provider calls, prompt loading, persistence, activation, field testing, runtime Pilot, or Copilot.


## LAB-0A status

LAB-0A adds a success criteria matrix only.

LAB-0A is documentation/governance design. It defines measurable success criteria for later lab evaluation, but it does not implement a runner, schema code, fixtures, corpus, candidate harness, metrics engine, provider calls, prompt loading, persistence, activation, field testing, runtime Pilot, or Copilot.

Feature ID: `routing_signal_scorer_v3_ml_lab_success_criteria_matrix_v1`

## Next safe milestone after LAB-0A

After LAB-0A is locally validated and frozen with `FREEZE_MEMORY_STATUS: OK`, the next safe milestone is:

```text
LAB-0B — Risk-Control Matrix
```

LAB-0B must remain documentation/governance only.


## LAB-0B status

LAB-0B adds a risk-control matrix only.

LAB-0B is documentation/governance design. It maps future LAB risks to required controls, but it does not implement a runner, schema code, fixtures, corpus, candidate harness, metrics engine, provider calls, prompt loading, persistence, activation, field testing, runtime Pilot, or Copilot.

Feature ID: `routing_signal_scorer_v3_ml_lab_risk_control_matrix_v1`

## Next safe milestone after LAB-0B

After LAB-0B is locally validated and frozen with `FREEZE_MEMORY_STATUS: OK`, the next safe milestone is:

```text
LAB-0C — LAB SLO / Critical Error Budget Declaration
```

LAB-0C must remain documentation/governance only.


## LAB-0C status

LAB-0C adds a LAB SLO / Critical Error Budget Declaration only.

LAB-0C is documentation/governance design. It declares the service-level objectives, zero critical boundary error budget, incident-style handling of critical violations, and the rule that soft performance can never compensate for a hard boundary failure.

LAB-0C does not implement a runner, schema code, fixtures, corpus, metrics engine, candidate harness, provider calls, prompt loading, persistence, activation, field testing, runtime Pilot, or Copilot.

Feature ID: `routing_signal_scorer_v3_ml_lab_slo_critical_error_budget_v1`

## Next safe milestone after LAB-0C

After LAB-0C is locally validated and frozen with `FREEZE_MEMORY_STATUS: OK`, the next safe milestone is:

```text
LAB-1 — Lab Box Boundary + Shielding Manifest
```

LAB-1 may continue governance/design work for shielding. LAB implementation machinery still remains blocked unless a later governed milestone explicitly authorizes it.


## LAB-1 status

LAB-1 adds a Lab Box Boundary + Shielding Manifest only.

LAB-1 is documentation/governance design. It declares the LAB box public boundary, private internals, allowed read-only inputs, forbidden imports, forbidden writes, shielding rules, and future enforcement expectations.

LAB-1 does not implement a runner, schema code, fixtures, corpus, scoring engine, metrics engine, candidate harness, live risk detectors, provider calls, prompt loading, persistence, activation, field testing, runtime Pilot, or Copilot.

Feature ID: `routing_signal_scorer_v3_ml_lab_box_boundary_shielding_manifest_v1`

## Next safe milestone after LAB-1

After LAB-1 is locally validated and frozen with `FREEZE_MEMORY_STATUS: OK`, the next safe milestone is:

```text
LAB-2 — Failure Taxonomy + Critical Violation Model
```

LAB-2 remains governed taxonomy/design work. LAB implementation machinery still remains blocked unless a later governed milestone explicitly authorizes it.


## LAB-2 status

LAB-2 adds a Failure Taxonomy + Critical Violation Model only.

LAB-2 is documentation/governance design. It defines the failure families, critical violation classes, severity levels, hard-gate outcome vocabulary, and classification doctrine that later LAB scoring/schema/runner milestones must obey.

LAB-2 does not implement a schema module, fixture files, corpus files, runner logic, scoring engine, metrics engine, candidate harness, live detectors, import scanner, write guard, provider calls, prompt loading, persistence, activation, field testing, runtime Pilot, or Copilot.

Feature ID: `routing_signal_scorer_v3_ml_lab_failure_taxonomy_critical_violation_model_v1`

## Next safe milestone after LAB-2

After LAB-2 is locally validated and frozen with `FREEZE_MEMORY_STATUS: OK`, the next safe milestone is:

```text
LAB-3 — Scoring Model + Hard Gates
```

LAB-3 remains governed scoring design. It must not create runtime ML implementation or LAB execution machinery unless a later governed milestone explicitly authorizes it.


## LAB-3 status

LAB-3 adds a Scoring Model + Hard Gates design document only.

LAB-3 is documentation/governance design. It defines the future scoring order, hard-gate precedence, critical-failure blocking, LAB_INVALID handling, soft metrics, category-specific score profiles, minimum reliability claim preconditions, and report expectations that later schema/runner milestones must obey.

LAB-3 does not implement a schema module, fixture files, corpus files, runner logic, scoring engine, metrics engine, candidate harness, live detectors, import scanner, write guard, provider calls, prompt loading, persistence, activation, field testing, runtime Pilot, or Copilot.

Feature ID: `routing_signal_scorer_v3_ml_lab_scoring_model_hard_gates_v1`

## Next safe milestone after LAB-3

After LAB-3 is locally validated and frozen with `FREEZE_MEMORY_STATUS: OK`, the next safe milestone is:

```text
LAB-4 — Test Case Schema + Candidate Output Contract
```

LAB-4 remains governed schema/contract design. It must not create runtime ML implementation or LAB execution machinery unless a later governed milestone explicitly authorizes it.


## LAB-4 status

LAB-4 adds a Test Case Schema + Candidate Output Contract design document only.

LAB-4 is documentation/governance design. It defines the future test case record shape, candidate output record shape, two-pass match-before-disagree contract, non-authoritative candidate wrapper, case-specific rubric fields, versioning fields, fixture-reference fields, forbidden candidate output fields, and contract rejection rules that later schema/runner milestones must obey.

LAB-4 does not implement schema code, validators, fixtures, corpus, runner logic, scoring engines, metrics engines, candidate harnesses, live detectors, import scanners, write guards, provider calls, prompt loading, persistence, activation, field testing, runtime Pilot, or Copilot.

Feature ID: `routing_signal_scorer_v3_ml_lab_test_case_schema_candidate_output_contract_v1`

## Next safe milestone after LAB-4

After LAB-4 is locally validated and frozen with `FREEZE_MEMORY_STATUS: OK`, the next safe milestone is:

```text
LAB-5 — Frozen Canon Fixture Format + Hash Manifest
```

LAB-5 remains governed fixture-format/hash-manifest design. It must not create live canon coupling, runtime ML implementation, prompt loading, provider calls, persistence, activation, field testing, runtime Pilot, or Copilot behavior.



## LAB-5 status

LAB-5 adds a Frozen Canon Fixture Format + Hash Manifest design document only.

LAB-5 is documentation/governance design. It defines the future copied fixture snapshot format, fixture hash manifest format, source freeze/canon reference fields, integrity rules, static-fixture read model, and fixture invalidation rules that later LAB fixture and runner milestones must obey.

LAB-5 does not create actual fixture files, hash manifest data files, corpus cases, schema code, validators, runner logic, scoring engines, metrics engines, candidate harnesses, live canon readers, live freeze-memory readers, import scanners, write guards, provider calls, prompt loading, persistence, activation, field testing, runtime Pilot, or Copilot.

Feature ID: `routing_signal_scorer_v3_ml_lab_frozen_canon_fixture_format_hash_manifest_v1`

## Next safe milestone after LAB-5

After LAB-5 is locally validated and frozen with `FREEZE_MEMORY_STATUS: OK`, the next safe milestone is:

```text
LAB-6 — Deterministic Runner Skeleton
```

LAB-6 may only be started under a separate governed scope after LAB-5 freeze. LAB-6 must remain non-runtime and must not create route authority, prompt loading, provider calls, embeddings, persistence of ML decisions, activation, field testing, runtime Pilot, or Copilot behavior.


## LAB-6 status

LAB-6 adds the first non-runtime deterministic runner skeleton source file for the ML LAB.

LAB-6 is still governed LAB infrastructure only. It creates a pure in-memory, non-authoritative skeleton module that can describe a future deterministic runner contract and build NOT_EVALUATED run-plan records from caller-supplied metadata.

LAB-6 does not load prompt files, read live freeze memory, read live router canon, read live prompt library files, read fixtures from disk, create actual fixtures, create a corpus, execute candidate evaluation, score candidates, compare routes, approve readiness, persist ML decisions, write reports, call providers, use embeddings, start batch mode, activate Pilot, field-test anything, or implement Copilot.

Feature ID: `routing_signal_scorer_v3_ml_lab_deterministic_runner_skeleton_v1`

## Next safe milestone after LAB-6

After LAB-6 is locally validated and frozen with `FREEZE_MEMORY_STATUS: OK`, the next safe milestone is:

```text
LAB-7 — Lab Self-Validation Gate
```

LAB-7 must validate the LAB itself before any candidate evaluation. It must remain non-runtime and must not grant route authority, prompt loading, provider calls, embeddings, persistent ML decisions, activation, field testing, runtime Pilot, or Copilot behavior.


## LAB-7 status

LAB-7 adds the governed non-runtime Lab Self-Validation Gate.

LAB-7 validates LAB readiness controls from caller-supplied in-memory facts before any future candidate evaluation is allowed by later milestones. It does not evaluate candidates and does not grant routing authority.

The self-validation gate checks whether required LAB control probes have been demonstrated, including gold-vs-gold pass, wrong-route negative control, missing-prompt negative control, forbidden-action critical control, fixture-hash mismatch control, match-before-disagree critical control, zero critical-boundary budget enforcement, LAB-6 NOT_EVALUATED behavior, no live project reads, and no authority fields.

Feature ID: `routing_signal_scorer_v3_ml_lab_self_validation_gate_v1`

## Next safe milestone after LAB-7

After LAB-7 is locally validated and frozen with `FREEZE_MEMORY_STATUS: OK`, the next safe milestone is:

```text
LAB-8 — Alpha Corpus Seed
```

LAB-8 may introduce a small governed alpha corpus only under a separate scope. It must still not grant route authority, prompt loading, provider calls, embeddings, persistent ML decisions, activation, field testing, runtime Pilot, or Copilot behavior.


## LAB-8 — Alpha Corpus Seed v1

LAB-8 adds a small static alpha corpus seed and static hash manifest under `alpha_corpus/`.
It remains non-runtime and non-authoritative. It does not evaluate candidates, compare routes, load prompts, read live canon/freeze memory, persist ML decisions, or activate Pilot/Copilot/field-test behavior.

Next safe milestone after LAB-8 freeze: `LAB-9 — Offline Observability + Experiment Report`.


## LAB-9 — Offline Observability + Experiment Report v1

LAB-9 adds a static offline observability and experiment-report contract plus one static report template under `report_templates/`.
It remains non-runtime and non-authoritative. It does not generate reports, persist reports, evaluate candidates, compare routes, load prompts, read live canon/freeze memory, persist ML decisions, or activate Pilot/Copilot/field-test behavior.

Next safe milestone after LAB-9 freeze: `LAB-10 — Candidate Evaluation Harness Interface`.

## LAB-10 — Candidate Evaluation Harness Interface v1

LAB-10 adds a non-runtime, in-memory candidate evaluation harness interface only.
It adds `candidate_evaluation_harness_interface.py` as the third allowed LAB Python file.
The interface creates non-authoritative `NOT_EVALUATED` or `HARNESS_INTERFACE_REJECTED` envelopes from caller-supplied metadata only.

LAB-10 does not evaluate candidates, execute cases, score cases, compare routes, generate reports, persist reports, grant route authority, load prompts, call providers, use embeddings, activate Pilot/Copilot, enable field testing, or implement Copilot behavior.

Next safe milestone after LAB-10 freeze: LAB-11 — Corpus V1 Expansion.

## LAB-11 - Corpus V1 Expansion v1

LAB-11 adds a static Corpus V1 expansion seed under `corpus_v1/`.
It adds 48 static non-authoritative expansion cases. Together with the 12 LAB-8 alpha cases, the LAB now has 60 static cases for future controlled evaluation coverage.

LAB-11 remains non-runtime and non-authoritative. It does not execute cases, score cases, evaluate candidates, compare routes, select routes, load prompts, read live prompt-library files, read live freeze memory, read live router canon, import runtime router modules, create fixture snapshots, generate reports, persist reports, call providers, use embeddings, activate Pilot/Copilot, enable field testing, or continue ML implementation.

LAB-11 is not reliability evidence. It expands coverage only.

Next safe milestone after LAB-11 freeze: `LAB-12 - Error Canonization Intake Spec`.

## LAB-12 status

LAB-12 adds an Error Canonization Intake Spec only.

LAB-12 is documentation/governance design. It defines how future observed LAB failures may be proposed as non-authoritative regression candidates, with human review and a separate governed patch required before any corpus, fixture, canon, prompt-library, freeze-memory, gold-registry, or routing behavior can change.

LAB-12 does not create an error library, automatic error canonization, regression cases, corpus mutation, fixture mutation, schema code, validators, runner execution, scoring execution, reports, candidate evaluation, provider calls, prompt loading, persistence, activation, field testing, runtime Pilot, or Copilot.

Feature ID: `routing_signal_scorer_v3_ml_lab_error_canonization_intake_spec_v1`

## Next safe milestone after LAB-12

After LAB-12 is locally validated and frozen with `FREEZE_MEMORY_STATUS: OK`, the next safe milestone is:

```text
LAB-13 - Lab Closure / Next-Phase Readiness Review
```

LAB-13 remains a closure/readiness review milestone. It must not continue ML implementation directly and must not grant runtime route authority, prompt loading, provider calls, embeddings, persistent ML decisions, activation, field testing, runtime Pilot, or Copilot behavior.

## LAB-13 status

LAB-13 adds a Lab Closure / Next-Phase Readiness Review only.

LAB-13 is documentation/governance design. It reviews whether the governed LAB construction sequence from RG-LAB-000 and LAB-0 through LAB-12 has enough isolated, non-runtime infrastructure to permit a later separate controlled ML/router candidate reliability testing plan.

LAB-13 does not execute cases, score cases, evaluate candidates, compare routes, generate reports, persist reports, grant route authority, load prompts, call providers, call embeddings, persist ML decisions, create activation, enable field testing, create runtime Pilot, or implement Copilot behavior.

Feature ID: `routing_signal_scorer_v3_ml_lab_closure_next_phase_readiness_review_v1`

## Next safe milestone after LAB-13

After LAB-13 is locally validated and frozen with `FREEZE_MEMORY_STATUS: OK`, the next safe milestone is:

```text
MLRT-0 - Controlled Non-Runtime ML/Router Candidate Reliability Test Plan
```

MLRT-0 must be a separate governed scope. It may plan controlled non-runtime candidate reliability testing, but it must not continue ML implementation directly and must not grant runtime route authority, prompt loading, provider calls, embeddings, persistent ML decisions, activation, field testing, runtime Pilot, or Copilot behavior.
