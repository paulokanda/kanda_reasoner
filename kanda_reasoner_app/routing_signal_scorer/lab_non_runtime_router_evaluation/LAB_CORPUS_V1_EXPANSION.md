# LAB-11 - Corpus V1 Expansion v1

Feature ID: `routing_signal_scorer_v3_ml_lab_corpus_v1_expansion_v1`

Feature title: `Routing Signal Scorer v3 ML LAB Corpus V1 Expansion v1`

Primary box: `kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation`

Schema label: `lab-11-corpus-v1-expansion`

## Purpose

LAB-11 expands the static non-authoritative ML LAB corpus beyond the LAB-8 alpha seed. It adds a governed Corpus V1 expansion seed with additional static case records and a SHA-256 hash manifest.

This file is the static Corpus V1 expansion seed contract for LAB-11.

The goal is broader coverage for future controlled ML/router evaluation, not reliability evidence and not candidate execution.

## Scope

LAB-11 may add only static corpus artifacts and validation tests for those artifacts.

Allowed LAB-11 artifacts:

- `LAB_CORPUS_V1_EXPANSION.md`
- `corpus_v1/corpus_v1_expansion_seed_v1.json`
- `corpus_v1/corpus_v1_expansion_seed_v1_hash_manifest.json`
- `tests/test_routing_signal_scorer_v3_ml_lab_corpus_v1_expansion.py`
- Updates to `README.md`, `LAB_PHASE_BOUNDARY.md`, `LAB_ALLOWED_ARTIFACTS.md`, and `box_manifest.json`

## Corpus size

LAB-8 created 12 static alpha cases.

LAB-11 adds 48 static Corpus V1 expansion cases.

The combined static corpus coverage after LAB-11 is therefore 60 cases.

This is a governed expansion step toward the later Corpus V1 target. It does not claim that the LAB is complete, reliable, exhaustive, or ready for ML implementation continuation.

## Coverage intent

The LAB-11 expansion covers these governance areas:

- Fast Path versus Routed Work Path distinction
- Freeze governance
- Patch delivery governance
- Prompt-library and prompt-authoring governance
- Startup-delivery governance
- Missing-context detection
- Stale context and stale sidecar rejection
- Box boundary and leakage prevention
- Prompt injection and bypass attempts
- Match-before-disagree doctrine
- Multi-turn shorthand such as `go next` and `continue`
- Medical/document/simple-task distinction
- LAB roadmap lock and ML implementation blocking

## Non-authority declarations

LAB-11 does not:

- execute cases
- score cases
- evaluate candidates
- compare routes
- select routes
- grant route authority
- load prompts
- read live prompt-library files
- read live freeze memory
- read live router canon
- import runtime router modules
- create fixture snapshots
- read actual fixture files
- create a scoring engine
- create a metrics engine
- create an executable candidate harness
- generate reports
- persist reports
- call providers
- call embedding models
- use network calls
- use subprocess calls
- start batch mode
- persist ML decisions
- create activation keys
- create field-test mode
- create runtime Pilot behavior
- create Copilot behavior


Compatibility contract phrases:

- does not evaluate candidates
- does not compare routes
- does not load prompts
- does not read live prompt-library files
- does not read live freeze memory
- does not create a scoring engine

## Reliability boundary

The LAB-11 corpus expansion is not reliability evidence.

A future ML/router candidate may only be tested for reliability after the governed LAB milestones for corpus, self-validation, harness interface, observability, error intake, and closure/readiness are satisfied and frozen.

Critical boundary incidents must not be hidden by aggregate soft metrics.

Critical boundary error budget: zero.

## Next safe milestone

After LAB-11 is locally validated and frozen with `FREEZE_MEMORY_STATUS: OK`, the next safe milestone is:

```text
LAB-12 - Error Canonization Intake Spec
```

LAB-12 must remain governed intake design unless a later frozen scope explicitly authorizes narrower implementation.
