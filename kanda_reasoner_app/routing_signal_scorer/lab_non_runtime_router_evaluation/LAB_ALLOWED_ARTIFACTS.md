# LAB-0 Allowed Artifacts

LAB-0 is documentation-only.

## Allowed in LAB-0

- `README.md`
- `LAB_PHASE_BOUNDARY.md`
- `LAB_CHARTER.md`
- `LAB_FORBIDDEN_BEHAVIORS.md`
- `LAB_STOP_CONDITIONS.md`
- `LAB_ALLOWED_ARTIFACTS.md`
- routing signal scorer manifest metadata declaring the documentation-only LAB box
- validation tests that verify the LAB-0 boundary
- `KANDA_FREEZE_HINT.json` as patch ZIP delivery metadata only

## Not allowed in LAB-0

- LAB implementation Python modules
- schema code
- fixture files
- corpus files
- runner files
- scoring engine files
- candidate harness files
- model/provider/embedding adapters
- prompt loaders
- runtime hooks
- persistence writers
- activation or field-test artifacts
- Copilot artifacts

## Next allowed artifacts after LAB-0 freeze

The next milestone may create success-criteria documentation only. It still must not create lab implementation logic.


## Allowed in LAB-0A

- `LAB_SUCCESS_CRITERIA_MATRIX.md`
- README/boundary/allowed-artifact documentation updates that keep LAB-0 and LAB-0A documentation-only
- routing signal scorer manifest metadata declaring the documentation-only LAB-0A success criteria matrix
- validation tests that verify the LAB-0A documentation-only boundary
- `KANDA_FREEZE_HINT.json` as patch ZIP delivery metadata only

## Not allowed in LAB-0A

- LAB implementation Python modules inside the LAB box
- schema code
- fixture files
- corpus files
- runner files
- scoring engine files
- candidate harness files
- model/provider/embedding adapters
- prompt loaders
- runtime hooks
- persistence writers
- activation or field-test artifacts
- Copilot artifacts

## Next allowed artifacts after LAB-0A freeze

The next milestone may create risk-control matrix documentation only. It still must not create lab implementation logic.


## Allowed in LAB-0B

- `LAB_RISK_CONTROL_MATRIX.md`
- README/boundary/allowed-artifact documentation updates that keep LAB-0, LAB-0A, and LAB-0B documentation-only
- routing signal scorer manifest metadata declaring the documentation-only LAB-0B risk-control matrix
- validation tests that verify the LAB-0B documentation-only boundary
- `KANDA_FREEZE_HINT.json` as patch ZIP delivery metadata only

## Not allowed in LAB-0B

- LAB implementation Python modules inside the LAB box
- schema code
- fixture files
- corpus files
- runner files
- scoring engine files
- candidate harness files
- live risk detector files
- model/provider/embedding adapters
- prompt loaders
- runtime hooks
- persistence writers
- activation or field-test artifacts
- Copilot artifacts

## Next allowed artifacts after LAB-0B freeze

The next milestone may create LAB SLO / Critical Error Budget Declaration documentation only. It still must not create lab implementation logic.


## Allowed in LAB-0C

- `LAB_SLO_CRITICAL_ERROR_BUDGET.md`
- README/boundary/allowed-artifact documentation updates that keep LAB-0 through LAB-0C documentation-only
- routing signal scorer manifest metadata declaring the documentation-only LAB-0C SLO / critical error budget declaration
- validation tests that verify the LAB-0C documentation-only boundary
- `KANDA_FREEZE_HINT.json` as patch ZIP delivery metadata only

## Not allowed in LAB-0C

- LAB implementation Python modules inside the LAB box
- schema code
- fixture files
- corpus files
- runner files
- scoring engine files
- metrics engine files
- candidate harness files
- live risk detector files
- model/provider/embedding adapters
- prompt loaders
- runtime hooks
- persistence writers
- activation or field-test artifacts
- Copilot artifacts

## Next allowed artifacts after LAB-0C freeze

The next milestone may create Lab Box Boundary + Shielding Manifest documentation/design artifacts. Implementation machinery remains blocked unless later explicitly authorized and frozen.


## Allowed in LAB-1

- `LAB_BOX_BOUNDARY_SHIELDING_MANIFEST.md`
- README/boundary/allowed-artifact documentation updates that keep LAB-0 through LAB-1 documentation/governance-only
- routing signal scorer manifest metadata declaring the documentation-only LAB-1 shielding manifest
- validation tests that verify the LAB-1 documentation-only boundary and shield doctrine
- `KANDA_FREEZE_HINT.json` as patch ZIP delivery metadata only

## Not allowed in LAB-1

- LAB implementation Python modules inside the LAB box
- schema code
- fixture files
- corpus files
- runner files
- scoring engine files
- metrics engine files
- candidate harness files
- live risk detector files
- model/provider/embedding adapters
- prompt loaders
- runtime hooks
- persistence writers
- activation or field-test artifacts
- Copilot artifacts
- production imports from the LAB box
- LAB imports from runtime router, prompt loader, freeze writer, provider, embedding, vector, UI, activation, or Copilot boxes

## Next allowed artifacts after LAB-1 freeze

The next milestone may create Failure Taxonomy + Critical Violation Model documentation/design artifacts. Implementation machinery remains blocked unless later explicitly authorized and frozen.


## Allowed in LAB-2

- `LAB_FAILURE_TAXONOMY_CRITICAL_VIOLATION_MODEL.md`
- README/boundary/allowed-artifact documentation updates that keep LAB-0 through LAB-2 documentation/governance-only
- routing signal scorer manifest metadata declaring the documentation-only LAB-2 failure taxonomy
- validation tests that verify LAB-2 remains taxonomy/design only and preserves the prior LAB boundary
- `KANDA_FREEZE_HINT.json` as patch ZIP delivery metadata only

## Not allowed in LAB-2

- LAB implementation Python modules inside the LAB box
- schema code
- fixture files
- corpus files
- runner files
- scoring engine files
- metrics engine files
- candidate harness files
- live detector files
- import scanner files
- write guard files
- model/provider/embedding adapters
- prompt loaders
- runtime hooks
- persistence writers
- activation or field-test artifacts
- Copilot artifacts
- production imports from the LAB box
- LAB imports from runtime router, prompt loader, freeze writer, provider, embedding, vector, UI, activation, or Copilot boxes

## Next allowed artifacts after LAB-2 freeze

The next milestone may create Scoring Model + Hard Gates documentation/design artifacts. Implementation machinery remains blocked unless later explicitly authorized and frozen.


## Allowed in LAB-3

- `LAB_SCORING_MODEL_HARD_GATES.md`
- README/boundary/allowed-artifact documentation updates that keep LAB-0 through LAB-3 documentation/governance-only
- routing signal scorer manifest metadata declaring the documentation-only LAB-3 scoring model and hard gates
- validation tests that verify LAB-3 remains scoring/design only and preserves the prior LAB boundary
- `KANDA_FREEZE_HINT.json` as patch ZIP delivery metadata only

## Not allowed in LAB-3

- LAB implementation Python modules inside the LAB box
- executable scoring engine
- executable metrics engine
- schema code
- fixture files
- corpus files
- runner files
- candidate harness files
- live detector files
- import scanner files
- write guard files
- model/provider/embedding adapters
- prompt loaders
- runtime hooks
- persistence writers
- activation or field-test artifacts
- Copilot artifacts
- production imports from the LAB box
- LAB imports from runtime router, prompt loader, freeze writer, provider, embedding, vector, UI, activation, or Copilot boxes

## Next allowed artifacts after LAB-3 freeze

The next milestone may create Test Case Schema + Candidate Output Contract documentation/design artifacts. Implementation machinery remains blocked unless later explicitly authorized and frozen.


## Allowed in LAB-4

- `LAB_TEST_CASE_SCHEMA_CANDIDATE_OUTPUT_CONTRACT.md`
- README/boundary/allowed-artifact documentation updates that keep LAB-0 through LAB-4 documentation/governance-only
- routing signal scorer manifest metadata declaring the documentation-only LAB-4 schema/contract design
- validation tests that verify LAB-4 remains schema/contract design only and preserves the prior LAB boundary
- `KANDA_FREEZE_HINT.json` as patch ZIP delivery metadata only

## Not allowed in LAB-4

- LAB implementation Python modules inside the LAB box
- executable schema validators
- JSON schema files treated as executable or authoritative runtime validators
- fixture files
- corpus files
- runner files
- executable scoring engine
- executable metrics engine
- candidate harness files
- live detector files
- import scanner files
- write guard files
- model/provider/embedding adapters
- prompt loaders
- runtime hooks
- persistence writers
- activation or field-test artifacts
- Copilot artifacts
- production imports from the LAB box
- LAB imports from runtime router, prompt loader, freeze writer, provider, embedding, vector, UI, activation, or Copilot boxes

## Next allowed artifacts after LAB-4 freeze

The next milestone may create Frozen Canon Fixture Format + Hash Manifest documentation/design artifacts. It must not create live canon coupling, fixture corpus content, runner execution, candidate evaluation, runtime ML implementation, prompt loading, provider calls, persistence, activation, field-test mode, runtime Pilot, or Copilot behavior.



## Allowed in LAB-5

- `LAB_FROZEN_CANON_FIXTURE_FORMAT_HASH_MANIFEST.md`
- README/boundary/allowed-artifact documentation updates that keep LAB-0 through LAB-5 documentation/governance-only
- routing signal scorer manifest metadata declaring the documentation-only LAB-5 frozen canon fixture format and hash manifest design
- validation tests that verify LAB-5 remains fixture-format/hash-manifest design only and preserves the prior LAB boundary
- `KANDA_FREEZE_HINT.json` as patch ZIP delivery metadata only

## Not allowed in LAB-5

- actual fixture files
- hash manifest data files
- corpus files or corpus cases
- LAB implementation Python modules inside the LAB box
- executable schema validators
- executable fixture validators
- live canon readers
- live freeze-memory readers
- live prompt-library readers
- runtime router readers
- runner files
- executable scoring engine
- executable metrics engine
- candidate harness files
- live detector files
- import scanner files
- write guard files
- model/provider/embedding adapters
- prompt loaders
- runtime hooks
- persistence writers
- activation or field-test artifacts
- Copilot artifacts
- production imports from the LAB box
- LAB imports from runtime router, prompt loader, freeze writer, provider, embedding, vector, UI, activation, or Copilot boxes

## Next allowed artifacts after LAB-5 freeze

The next milestone is LAB-6 — Deterministic Runner Skeleton.

The next milestone may create a Deterministic Runner Skeleton only under a separate governed scope. Any future runner remains non-runtime and evaluation-only; it must not route, load prompts, call providers, use embeddings, persist ML decisions, activate Pilot/Copilot, or field-test anything.


## Allowed in LAB-6

- `LAB_DETERMINISTIC_RUNNER_SKELETON.md`
- `deterministic_runner_skeleton.py`
- README/boundary/allowed-artifact documentation updates that mark LAB-6 as the first non-runtime runner-skeleton source milestone
- routing signal scorer manifest metadata declaring the non-runtime deterministic runner skeleton
- validation tests that verify the LAB-6 skeleton remains deterministic, non-authoritative, in-memory, and unable to route, load prompts, call providers, persist ML decisions, activate Pilot/Copilot, or field-test anything
- compatibility updates to earlier LAB documentation contract tests so they permit the exact LAB-6 skeleton source file while still rejecting prohibited runtime or authority behavior
- `KANDA_FREEZE_HINT.json` as patch ZIP delivery metadata only

## Not allowed in LAB-6

- live prompt-library reads
- live freeze-memory reads
- live router-canon reads
- runtime router imports or route comparison execution
- prompt loader imports or prompt loading
- fixture discovery from live project files
- actual fixture files
- hash manifest data files
- corpus files or corpus cases
- executable scoring engine
- executable metrics engine
- candidate evaluation harness
- provider adapters or provider calls
- embedding/vector adapters or embedding calls
- network calls
- subprocess calls
- async/event-loop runners
- batch mode
- report persistence
- persistent ML decision storage
- freeze memory writes
- gold registry writes
- prompt library writes
- router canon writes
- human approval writes
- readiness approval writes
- activation keys or activation state
- field-test flags
- runtime Pilot behavior
- Copilot behavior
- production imports from the LAB box

## Next allowed artifacts after LAB-6 freeze

The next milestone is LAB-7 — Lab Self-Validation Gate.

LAB-7 may add self-validation fixtures or self-checks only under a separate governed scope. Candidate evaluation remains blocked until the LAB self-validation gate is locally validated and frozen.


## Allowed in LAB-7

- `LAB_SELF_VALIDATION_GATE.md`
- `lab_self_validation_gate.py`
- README/boundary/allowed-artifact documentation updates that mark LAB-7 as the in-memory LAB self-validation gate milestone
- routing signal scorer manifest metadata declaring the non-runtime self-validation gate
- validation tests that verify the self-validation gate remains deterministic, in-memory, non-authoritative, and unable to evaluate candidates, route, load prompts, call providers, persist ML decisions, activate Pilot/Copilot, or field-test anything
- compatibility updates to earlier LAB contract tests so they permit exactly the LAB-6 skeleton plus LAB-7 self-validation gate Python source files while still rejecting prohibited runtime or authority behavior
- `KANDA_FREEZE_HINT.json` as patch ZIP delivery metadata only

## Not allowed in LAB-7

- candidate output evaluation
- route comparison or route selection
- prompt loading
- live prompt-library reads
- live freeze-memory reads
- live router-canon reads
- runtime router imports
- fixture discovery from live project files
- fixture file reads from disk
- actual fixture files
- hash manifest data files
- corpus files or corpus cases
- executable scoring engine
- executable metrics engine
- candidate evaluation harness
- provider adapters or provider calls
- embedding/vector adapters or embedding calls
- network calls
- subprocess calls
- async/event-loop runners
- batch mode
- report persistence
- persistent ML decision storage
- freeze memory writes
- gold registry writes
- prompt library writes
- router canon writes
- human approval writes
- runtime readiness approval writes
- activation keys or activation state
- field-test flags
- runtime Pilot behavior
- Copilot behavior
- production imports from the LAB box

## Next allowed artifacts after LAB-7 freeze

The next milestone is LAB-8 — Alpha Corpus Seed.

LAB-8 may introduce a small static alpha corpus only under a separate governed scope. Candidate evaluation remains blocked until later harness/scoring/corpus gates are locally validated and frozen.


## LAB-8 allowed artifacts

LAB-8 may add the following static, non-runtime artifacts:

- `LAB_ALPHA_CORPUS_SEED.md`
- `alpha_corpus/alpha_corpus_seed_v1.json`
- `alpha_corpus/alpha_corpus_seed_v1_hash_manifest.json`
- `tests/test_routing_signal_scorer_v3_ml_lab_alpha_corpus_seed.py`

LAB-8 must not add route authority, prompt loading, provider calls, embeddings, persistent ML decisions, candidate evaluation, route comparison, scoring engine, metrics engine, candidate harness, activation, field testing, runtime Pilot, or Copilot behavior.


## LAB-9 allowed artifacts

LAB-9 may add the following static, non-runtime artifacts:

- `LAB_OFFLINE_OBSERVABILITY_EXPERIMENT_REPORT.md`
- `report_templates/offline_experiment_report_template_v1.json`
- `tests/test_routing_signal_scorer_v3_ml_lab_offline_observability_experiment_report.py`

LAB-9 must not add report generation, report persistence, candidate evaluation, route comparison, route authority, prompt loading, provider calls, embeddings, persistent ML decisions, scoring engine, metrics engine, candidate harness, activation, field testing, runtime Pilot, or Copilot behavior.

## LAB-10 allowed artifacts

LAB-10 may add:

- `LAB_CANDIDATE_EVALUATION_HARNESS_INTERFACE.md`
- `candidate_evaluation_harness_interface.py`
- `tests/test_routing_signal_scorer_v3_ml_lab_candidate_evaluation_harness_interface.py`

The Python file must remain pure, in-memory, non-runtime, and non-authoritative. It may only create interface envelopes from caller-supplied metadata and must return `NOT_EVALUATED` or `HARNESS_INTERFACE_REJECTED`.

LAB-10 may update earlier LAB tests only to recognize the new allowed Python file without weakening the historical frozen contracts.

## LAB-11 allowed artifacts

LAB-11 may add the following static, non-runtime artifacts:

- `LAB_CORPUS_V1_EXPANSION.md`
- `corpus_v1/corpus_v1_expansion_seed_v1.json`
- `corpus_v1/corpus_v1_expansion_seed_v1_hash_manifest.json`
- `tests/test_routing_signal_scorer_v3_ml_lab_corpus_v1_expansion.py`

LAB-11 may update:

- `README.md`
- `LAB_PHASE_BOUNDARY.md`
- `LAB_ALLOWED_ARTIFACTS.md`
- `box_manifest.json`

LAB-11 must not add new LAB Python modules. After LAB-11, the only allowed LAB Python source files remain:

- `candidate_evaluation_harness_interface.py`
- `deterministic_runner_skeleton.py`
- `lab_self_validation_gate.py`

LAB-11 must not add case execution, scoring, candidate evaluation, route comparison, route authority, prompt loading, live prompt-library reads, live freeze-memory reads, live router-canon reads, runtime router imports, actual fixture snapshots, scoring engine, metrics engine, executable candidate harness, report generation, report persistence, provider calls, embeddings, network calls, subprocess calls, batch mode, persistent ML decisions, activation key, field-test mode, runtime Pilot, or Copilot behavior.

After LAB-11 is locally validated and frozen with `FREEZE_MEMORY_STATUS: OK`, the next safe milestone is LAB-12 - Error Canonization Intake Spec.

## LAB-12 allowed artifacts

LAB-12 may add or update these documentation/governance artifacts:

- `LAB_ERROR_CANONIZATION_INTAKE_SPEC.md`
- `README.md`
- `LAB_PHASE_BOUNDARY.md`
- `LAB_ALLOWED_ARTIFACTS.md`
- `box_manifest.json`
- `tests/test_routing_signal_scorer_v3_ml_lab_error_canonization_intake_spec.py`

LAB-12 must not add new LAB Python source files. After LAB-12, the only allowed LAB Python source files remain:

- `candidate_evaluation_harness_interface.py`
- `deterministic_runner_skeleton.py`
- `lab_self_validation_gate.py`

LAB-12 must not add actual regression cases, mutate existing corpus files, mutate fixture/hash manifest files, implement an error library, implement automatic error canonization, implement candidate evaluation, implement scoring, generate reports, persist reports, load prompts, read live canon or freeze memory, call providers, call embeddings, use network, use subprocess, use batch mode, persist ML decisions, activate Pilot/Copilot, field-test anything, or implement Copilot behavior.

After LAB-12 is locally validated and frozen with `FREEZE_MEMORY_STATUS: OK`, the next safe milestone is LAB-13 - Lab Closure / Next-Phase Readiness Review.

## LAB-13 allowed artifacts

LAB-13 may add or update these documentation/governance artifacts:

- `LAB_CLOSURE_NEXT_PHASE_READINESS_REVIEW.md`
- `README.md`
- `LAB_PHASE_BOUNDARY.md`
- `LAB_ALLOWED_ARTIFACTS.md`
- `box_manifest.json`
- `tests/test_routing_signal_scorer_v3_ml_lab_closure_next_phase_readiness_review.py`

LAB-13 must not add new LAB Python source files. After LAB-13, the only allowed LAB Python source files remain:

- `candidate_evaluation_harness_interface.py`
- `deterministic_runner_skeleton.py`
- `lab_self_validation_gate.py`

LAB-13 must not execute cases, score cases, evaluate candidates, compare routes, grant route authority, load prompts, read live canon or freeze memory, mutate corpus, mutate fixtures, mutate router canon, mutate prompt library files, mutate freeze memory, mutate gold registry, create an error library, generate reports, persist reports, call providers, call embeddings, use network, use subprocess, use batch mode, persist ML decisions, activate Pilot/Copilot, field-test anything, or implement Copilot behavior.

After LAB-13 is locally validated and frozen with `FREEZE_MEMORY_STATUS: OK`, the next safe milestone is MLRT-0 - Controlled Non-Runtime ML/Router Candidate Reliability Test Plan.
