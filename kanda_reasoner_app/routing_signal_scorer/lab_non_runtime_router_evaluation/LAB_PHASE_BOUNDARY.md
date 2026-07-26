# LAB Phase Boundary

This document opens the ML LAB phase after the frozen P-series and RG-LAB-000 router-canon entry.

## Preconditions

The LAB phase may be discussed only after all of the following are true:

1. P0 through P12 are frozen.
2. P12 local freeze has `FREEZE_MEMORY_STATUS: OK`.
3. RG-LAB-000 ML LAB Phase Entry Router Canon v1 is frozen.
4. RG-LAB-000 local freeze has `FREEZE_MEMORY_STATUS: OK`.
5. The user has been warned that the next phase is LAB/test governance, not direct ML implementation.

## Boundary statement

The LAB phase exists to build a controlled, isolated, non-runtime evaluation environment that can later test whether ML/router candidates can reproduce frozen router prompt logic, detect missing or stale context, reject bypass attempts, preserve box boundaries, explain disagreements without overriding canon, and produce reproducible audit evidence.

The LAB phase does not continue ML implementation directly.

The LAB phase does not create runtime Pilot, Copilot, activation, field-test mode, prompt loading, provider calls, embeddings, persistence, batch mode, training-data use, or route authority.

## Current milestone

This milestone is LAB-0 only.

LAB-0 is documentation-only.

## Next flow lock

```text
LAB-0 frozen
→ LAB-0A Success Criteria Matrix
→ LAB-0B Risk-Control Matrix
→ LAB-0C LAB SLO / Critical Error Budget Declaration
→ LAB-1 Box Boundary + Shielding Manifest
→ later lab implementation only after documentation gates are frozen
```

No later step may be skipped by a generic `next`, `continue`, or `go` request.


## LAB-0A boundary addendum

LAB-0A may define success criteria for later LAB evaluation, but it may not implement the evaluation machinery.

LAB-0A may not create schema code, fixture files, corpus files, runner logic, scoring engines, candidate harnesses, provider adapters, prompt loaders, persistence writers, activation keys, field-test flags, runtime Pilot behavior, or Copilot behavior.

Updated documentation-gate flow:

```text
LAB-0 frozen
→ LAB-0A Success Criteria Matrix frozen
→ LAB-0B Risk-Control Matrix
→ LAB-0C LAB SLO / Critical Error Budget Declaration
→ LAB-1 Box Boundary + Shielding Manifest
→ later lab implementation only after documentation gates are frozen
```


## LAB-0B boundary addendum

LAB-0B may define a risk-control matrix for later LAB evaluation, but it may not implement the evaluation machinery or any live risk detector.

LAB-0B may not create schema code, fixture files, corpus files, runner logic, scoring engines, candidate harnesses, provider adapters, prompt loaders, persistence writers, activation keys, field-test flags, runtime Pilot behavior, or Copilot behavior.

Updated documentation-gate flow:

```text
LAB-0 frozen
→ LAB-0A Success Criteria Matrix frozen
→ LAB-0B Risk-Control Matrix frozen
→ LAB-0C LAB SLO / Critical Error Budget Declaration
→ LAB-1 Box Boundary + Shielding Manifest
→ later lab implementation only after documentation gates are frozen
```


## LAB-0C boundary addendum

LAB-0C may declare LAB SLOs, critical boundary objectives, zero critical boundary error budget, and incident-style handling rules for future LAB evaluation.

LAB-0C may not implement the evaluation machinery, schema code, fixture files, corpus files, runner logic, scoring engines, metrics engines, candidate harnesses, live risk detectors, provider adapters, prompt loaders, persistence writers, activation keys, field-test flags, runtime Pilot behavior, or Copilot behavior.

Updated documentation-gate flow:

```text
LAB-0 frozen
→ LAB-0A Success Criteria Matrix frozen
→ LAB-0B Risk-Control Matrix frozen
→ LAB-0C LAB SLO / Critical Error Budget Declaration frozen
→ LAB-1 Lab Box Boundary + Shielding Manifest
→ later lab implementation only after documentation and shielding gates are frozen
```


## LAB-1 boundary addendum

LAB-1 may define the LAB box boundary, shielding manifest, allowed read-only inputs, forbidden imports, forbidden writes, and future enforcement expectations.

LAB-1 may not implement the evaluation machinery, schema code, fixture files, corpus files, runner logic, scoring engines, metrics engines, candidate harnesses, live risk detectors, provider adapters, prompt loaders, persistence writers, activation keys, field-test flags, runtime Pilot behavior, or Copilot behavior.

Updated documentation-gate flow:

```text
LAB-0 frozen
→ LAB-0A Success Criteria Matrix frozen
→ LAB-0B Risk-Control Matrix frozen
→ LAB-0C LAB SLO / Critical Error Budget Declaration frozen
→ LAB-1 Lab Box Boundary + Shielding Manifest frozen
→ LAB-2 Failure Taxonomy + Critical Violation Model
→ later lab implementation only after documentation, shielding, taxonomy, scoring, and schema gates are frozen
```


## LAB-2 boundary addendum

LAB-2 may define failure taxonomy, critical violation classes, severity labels, hard-gate outcome terms, and future classification expectations.

LAB-2 may not implement schema code, fixtures, corpus, runner logic, scoring engines, metrics engines, candidate harnesses, live risk detectors, import scanners, write guards, provider adapters, prompt loaders, persistence writers, activation keys, field-test flags, runtime Pilot behavior, or Copilot behavior.

Updated documentation-gate flow:

```text
LAB-0 frozen
→ LAB-0A Success Criteria Matrix frozen
→ LAB-0B Risk-Control Matrix frozen
→ LAB-0C LAB SLO / Critical Error Budget Declaration frozen
→ LAB-1 Lab Box Boundary + Shielding Manifest frozen
→ LAB-2 Failure Taxonomy + Critical Violation Model frozen
→ LAB-3 Scoring Model + Hard Gates
→ later lab implementation only after documentation, shielding, taxonomy, scoring, and schema gates are frozen
```


## LAB-3 boundary addendum

LAB-3 may define scoring-model doctrine, hard-gate order, soft-score categories, category-specific score profiles, minimum reliability claim preconditions, and future report expectations.

LAB-3 may not implement schema code, fixtures, corpus, runner logic, scoring engines, metrics engines, candidate harnesses, live risk detectors, import scanners, write guards, provider adapters, prompt loaders, persistence writers, activation keys, field-test flags, runtime Pilot behavior, or Copilot behavior.

Updated documentation-gate flow:

```text
LAB-0 frozen
→ LAB-0A Success Criteria Matrix frozen
→ LAB-0B Risk-Control Matrix frozen
→ LAB-0C LAB SLO / Critical Error Budget Declaration frozen
→ LAB-1 Lab Box Boundary + Shielding Manifest frozen
→ LAB-2 Failure Taxonomy + Critical Violation Model frozen
→ LAB-3 Scoring Model + Hard Gates frozen
→ LAB-4 Test Case Schema + Candidate Output Contract
→ later lab implementation only after documentation, shielding, taxonomy, scoring, and schema gates are frozen
```


## LAB-4 boundary addendum

LAB-4 may define test case schema doctrine, candidate output contract doctrine, non-authoritative candidate wrappers, two-pass match-before-disagree contract fields, case-specific rubric fields, version/reference fields, and forbidden candidate-output fields.

LAB-4 may not implement schema code, validators, fixture files, corpus files, runner logic, scoring engines, metrics engines, candidate harnesses, live risk detectors, import scanners, write guards, provider adapters, prompt loaders, persistence writers, activation keys, field-test flags, runtime Pilot behavior, or Copilot behavior.

Updated documentation-gate flow:

```text
LAB-0 frozen
→ LAB-0A Success Criteria Matrix frozen
→ LAB-0B Risk-Control Matrix frozen
→ LAB-0C LAB SLO / Critical Error Budget Declaration frozen
→ LAB-1 Lab Box Boundary + Shielding Manifest frozen
→ LAB-2 Failure Taxonomy + Critical Violation Model frozen
→ LAB-3 Scoring Model + Hard Gates frozen
→ LAB-4 Test Case Schema + Candidate Output Contract frozen
→ LAB-5 Frozen Canon Fixture Format + Hash Manifest
→ later lab implementation only after documentation, shielding, taxonomy, scoring, schema, and fixture-format gates are frozen
```



## LAB-5 boundary addendum

LAB-5 may define frozen canon fixture format doctrine, fixture snapshot metadata doctrine, hash manifest doctrine, static fixture read rules, and fixture invalidation rules.

LAB-5 may not create actual fixture files, hash manifest data files, corpus cases, schema code, validators, runner logic, scoring engines, metrics engines, candidate harnesses, live canon readers, live freeze-memory readers, import scanners, write guards, provider adapters, prompt loaders, persistence writers, activation keys, field-test flags, runtime Pilot behavior, or Copilot behavior.

Updated documentation-gate flow:

```text
LAB-0 frozen
→ LAB-0A Success Criteria Matrix frozen
→ LAB-0B Risk-Control Matrix frozen
→ LAB-0C LAB SLO / Critical Error Budget Declaration frozen
→ LAB-1 Lab Box Boundary + Shielding Manifest frozen
→ LAB-2 Failure Taxonomy + Critical Violation Model frozen
→ LAB-3 Scoring Model + Hard Gates frozen
→ LAB-4 Test Case Schema + Candidate Output Contract frozen
→ LAB-5 Frozen Canon Fixture Format + Hash Manifest frozen
→ LAB-6 Deterministic Runner Skeleton
→ later lab evaluation only after fixture-format, runner, self-validation, and corpus gates are frozen
```

No later step may be skipped by a generic `next`, `continue`, or `go` request.


## LAB-6 boundary addendum

LAB-6 is the first milestone allowed to add a non-runtime LAB Python source file.

Allowed LAB-6 implementation scope is limited to a deterministic runner skeleton that operates on caller-supplied in-memory metadata and returns non-authoritative NOT_EVALUATED records.

LAB-6 may define immutable dataclasses, constants, pure canonicalization helpers, SHA-256 text hashing helpers, and a run-plan builder that records why candidate evaluation is not yet performed.

LAB-6 may not load files, read live prompt library data, read live freeze memory, read live router canon, read runtime router objects, read fixtures from disk, discover fixtures, create actual fixtures, create hash manifest data files, create a corpus, execute candidate evaluation, score candidates, compare routes, generate routing decisions, approve readiness, record human approval, write reports, write freeze memory, write gold registries, write prompt libraries, write router canon, write persistent ML decisions, call providers, use embeddings, use network calls, use subprocesses, start async/batch execution, activate Pilot, field-test anything, or implement Copilot behavior.

Updated LAB flow:

```text
LAB-0 frozen
→ LAB-0A frozen
→ LAB-0B frozen
→ LAB-0C frozen
→ LAB-1 frozen
→ LAB-2 frozen
→ LAB-3 frozen
→ LAB-4 frozen
→ LAB-5 frozen
→ LAB-6 Deterministic Runner Skeleton frozen
→ LAB-7 Lab Self-Validation Gate
→ later corpus/candidate evaluation only after self-validation gates pass
```

No later step may be skipped by a generic `next`, `continue`, or `go` request.


## LAB-7 boundary addendum

LAB-7 adds a non-runtime Lab Self-Validation Gate.

Allowed LAB-7 implementation scope is limited to in-memory validation of caller-supplied LAB control results. It can determine whether the LAB self-validation preconditions are satisfied, but it cannot evaluate candidate outputs, compare candidate routes, score candidates, read live project state, approve readiness for runtime, or grant any routing authority.

LAB-7 may define immutable dataclasses, constants, required self-validation control names, pure deterministic gate evaluation, and read-only mapping helpers.

LAB-7 may not load files, read live prompt library data, read live freeze memory, read live router canon, read runtime router objects, discover fixtures, read fixtures from disk, create actual fixtures, create hash manifest data files, create corpus cases, execute candidate evaluation, score candidates, compare routes, select routes, execute routes, approve runtime readiness, record human approval, write reports, write freeze memory, write gold registries, write prompt libraries, write router canon, write persistent ML decisions, call providers, use embeddings, use network calls, use subprocesses, start async/batch execution, activate Pilot, field-test anything, or implement Copilot behavior.

Updated LAB flow:

```text
LAB-0 frozen
→ LAB-0A frozen
→ LAB-0B frozen
→ LAB-0C frozen
→ LAB-1 frozen
→ LAB-2 frozen
→ LAB-3 frozen
→ LAB-4 frozen
→ LAB-5 frozen
→ LAB-6 frozen
→ LAB-7 Lab Self-Validation Gate frozen
→ LAB-8 Alpha Corpus Seed
→ later candidate evaluation only after governed corpus and harness milestones are frozen
```

No later step may be skipped by a generic `next`, `continue`, or `go` request.


## LAB-8 boundary addendum — Alpha Corpus Seed

LAB-8 may contain static alpha corpus data files and a static hash manifest data file.
LAB-8 may not execute those cases, score candidate outputs, compare routes, load prompts, call providers, call embeddings, persist ML decisions, activate Pilot/Copilot, enable field testing, or claim reliability.

Allowed new static data files:

- `alpha_corpus/alpha_corpus_seed_v1.json`
- `alpha_corpus/alpha_corpus_seed_v1_hash_manifest.json`

Next safe milestone after LAB-8 freeze: `LAB-9 — Offline Observability + Experiment Report`.


## LAB-9 boundary addendum — Offline Observability + Experiment Report

LAB-9 may contain a static offline report template. LAB-9 may not generate reports, persist reports, evaluate candidates, execute or score alpha cases, compare routes, load prompts, call providers, call embeddings, persist ML decisions, activate Pilot/Copilot, enable field testing, or claim reliability.

Allowed new static template file:

- `report_templates/offline_experiment_report_template_v1.json`

Next safe milestone after LAB-9 freeze: `LAB-10 — Candidate Evaluation Harness Interface`.

## LAB-10 boundary update

LAB-10 permits exactly one additional LAB Python source file:

- `candidate_evaluation_harness_interface.py`

After LAB-10, the allowed LAB Python files are:

- `candidate_evaluation_harness_interface.py`
- `deterministic_runner_skeleton.py`
- `lab_self_validation_gate.py`

This boundary update does not permit candidate evaluation, case execution, scoring, route comparison, route authority, prompt loading, live project reads, report generation, report persistence, provider calls, embeddings, batch mode, activation, field testing, runtime Pilot behavior, or Copilot behavior.

## LAB-11 boundary addendum - Corpus V1 Expansion

LAB-11 may contain static Corpus V1 expansion data files and a static hash manifest data file.

Allowed new static data files:

- `corpus_v1/corpus_v1_expansion_seed_v1.json`
- `corpus_v1/corpus_v1_expansion_seed_v1_hash_manifest.json`

LAB-11 may not execute cases, score cases, evaluate candidates, compare routes, select routes, grant route authority, load prompts, read live prompt-library files, read live freeze memory, read live router canon, import runtime router modules, create actual fixture snapshots, generate reports, persist reports, call providers, call embedding models, use network calls, use subprocess calls, start batch mode, persist ML decisions, create activation keys, create field-test mode, create runtime Pilot behavior, create Copilot behavior, or continue ML implementation.

LAB-11 expands static coverage only. It is not reliability evidence.

Next safe milestone after LAB-11 freeze: `LAB-12 - Error Canonization Intake Spec`.

## LAB-12 status

LAB-12 adds an Error Canonization Intake Spec only.

LAB-12 is documentation/governance design. It defines a future human-reviewed intake path for converting observed LAB failures into proposed regression candidates. It does not create an error library, automatic regression writing, corpus mutation, fixture mutation, canon mutation, prompt-library mutation, freeze-memory mutation, gold-registry mutation, runner execution, scoring execution, report generation, candidate evaluation, route comparison, route authority, prompt loading, provider calls, embeddings, persistence, activation, field testing, runtime Pilot, or Copilot behavior.

Feature ID: `routing_signal_scorer_v3_ml_lab_error_canonization_intake_spec_v1`

## Next safe milestone after LAB-12

After LAB-12 is locally validated and frozen with `FREEZE_MEMORY_STATUS: OK`, the next safe milestone is:

```text
LAB-13 - Lab Closure / Next-Phase Readiness Review
```

LAB-13 must remain a governed closure/readiness review. It must not continue ML implementation directly, and it must not grant runtime route authority, prompt loading, provider calls, embeddings, persistent ML decisions, activation, field testing, runtime Pilot, or Copilot behavior.

## LAB-13 boundary addendum - Lab Closure / Next-Phase Readiness Review

LAB-13 is a documentation-only closure/readiness review milestone.

LAB-13 may define closure questions, readiness labels, mandatory preconditions, and next-phase boundary rules. It may not execute cases, score cases, evaluate candidates, compare routes, select routes, grant route authority, load prompts, read live prompt-library files, read live freeze memory, read live router canon, import runtime router modules, mutate corpus files, mutate fixture manifests, mutate router canon, mutate prompt library files, mutate freeze memory, mutate gold registry, generate reports, persist reports, call providers, call embedding models, use network calls, use subprocess calls, start batch mode, persist ML decisions, create activation keys, create field-test mode, create runtime Pilot behavior, or create Copilot behavior.

LAB-13 is not ML/router reliability evidence. It does not unlock direct ML implementation.

Next safe milestone after LAB-13 freeze: `MLRT-0 - Controlled Non-Runtime ML/Router Candidate Reliability Test Plan`.

MLRT-0 must be a separate governed non-runtime scope and must not be started by silently continuing ML implementation.
