# LAB-8 — Alpha Corpus Seed v1

Feature ID: `routing_signal_scorer_v3_ml_lab_alpha_corpus_seed_v1`

Primary box: `kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation`

Schema version: `lab-8-alpha-corpus-seed`

## Purpose

LAB-8 introduces a small governed static alpha corpus seed so later LAB milestones can validate deterministic corpus handling before any candidate evaluation occurs.

This is a static corpus seed only. It is not a runner, not a scorer, not a candidate harness, not reliability evidence, and not permission to continue ML implementation.

## Added static artifacts

- `alpha_corpus/alpha_corpus_seed_v1.json`
- `alpha_corpus/alpha_corpus_seed_v1_hash_manifest.json`

The corpus contains `12` static seed cases covering simple-vs-governed routing, freeze governance, prompt-authoring bypass, box boundaries, prompt-loading prohibition, live-fixture prohibition, missing context, match-before-disagree, and LAB roadmap lock behavior.

## Non-authority declarations

LAB-8 does not evaluate candidates.
LAB-8 does not compare routes.
LAB-8 does not select or execute routes.
LAB-8 does not load prompts.
LAB-8 does not read live prompt-library content.
LAB-8 does not read live freeze memory.
LAB-8 does not read live router canon.
LAB-8 does not import runtime router modules.
LAB-8 does not create actual fixture snapshots.
LAB-8 does not create a runner.
LAB-8 does not create a scoring engine.
LAB-8 does not create a metrics engine.
LAB-8 does not create a candidate harness.
LAB-8 does not write reports.
LAB-8 does not persist ML decisions.
LAB-8 does not call providers.
LAB-8 does not call embedding models.
LAB-8 does not use network or subprocess calls.
LAB-8 does not use batch mode.
LAB-8 does not activate Pilot or Copilot behavior.
LAB-8 does not enable field testing.

## Static corpus rules

Every alpha case must remain a non-authoritative gold seed. Case records may describe expected classification, expected path, required prompt groups, missing context, and hard/critical failure conditions, but they must not become live route decisions.

Every alpha case must declare:

- `case_id`
- `case_version`
- `schema_version`
- `corpus_id`
- `corpus_version`
- `case_category`
- `scenario`
- `expected`
- `rubric`
- `candidate_output_contract`
- `static_seed_status`
- `candidate_evaluation_status`

The only allowed candidate evaluation status in LAB-8 is `not_executed`.

## Hash manifest doctrine

The LAB-8 hash manifest records a SHA-256 hash of the static corpus file. The manifest is static LAB metadata only; it is not a live fixture reader, not a freeze-memory reader, and not a prompt-library reader.

Hash algorithm: `SHA-256`.

Hash input canonicalization: `UTF-8 JSON, sorted keys, 2-space indentation, trailing newline`.

## Review and reliability limits

The alpha corpus seed is not sufficient for reliability claims. Future reliability claims remain blocked until later governed milestones provide self-validation, fixture integrity, scoring, coverage, reporting, human review, and freeze evidence.

The alpha corpus seed does not prove ML router prompt logic reliability and does not authorize continuing ML implementation.

## Critical boundaries

Any attempt to treat LAB-8 cases as runtime route decisions is a critical boundary violation.
Any attempt to load prompts from LAB-8 cases is a critical boundary violation.
Any attempt to use LAB-8 cases to persist ML decisions is a critical boundary violation.
Any attempt to use LAB-8 cases to activate Pilot, Copilot, or field-test mode is a critical boundary violation.
Any attempt to mutate prompt library, router canon, freeze memory, gold registry, startup pack, activation state, field-test state, runtime decision logs, or persistent ML decision storage is a critical boundary violation.

Critical boundary error budget: zero.

## Next safe milestone

After local validation and freeze with `FREEZE_MEMORY_STATUS: OK`, proceed only to:

`LAB-9 — Offline Observability + Experiment Report`

LAB-9 must remain governed/non-runtime and must not grant route authority, prompt loading, provider calls, embeddings, persistent ML decisions, activation, field testing, runtime Pilot, or Copilot behavior.
