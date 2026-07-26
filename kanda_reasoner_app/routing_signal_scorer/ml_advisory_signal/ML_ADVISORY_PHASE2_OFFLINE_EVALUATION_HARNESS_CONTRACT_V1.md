# ML Advisory Signal Phase 2 Offline Evaluation Harness Contract v1

Feature title: Routing Signal Scorer ML Advisory-Signal Phase 2 Offline Evaluation Harness Contract v1
Feature ID: rss_ml_adv_phase2_offline_evaluation_harness_contract_v1

## Purpose

Phase 2 creates a non-runtime, in-memory offline evaluation harness for ML
Advisory Signal telemetry. It follows the frozen Phase 1a boundary contract,
Phase 1a review gate, Phase 1b design audit contract, and Phase 1b review gate.

The harness evaluates advisory telemetry against caller-supplied fixtures. It
is not runtime shadow mode. It does not integrate ML into router prompt logic.
It does not choose a route.

## Allowed surface

The harness may:

- accept caller-supplied `OfflineEvaluationFixture` objects in memory;
- call `NullAdvisor` or deterministic `MockAdvisor` through `AdvisorProtocol`;
- validate advisory outputs through the existing output firewall;
- compare caller-supplied governed decision values before and after advisory;
- return immutable in-memory `OfflineEvaluationSummary` values;
- fail open to abstention telemetry if an advisor raises or output is rejected.

## Forbidden surface

The harness must not:

- call a real ML provider;
- call an external API;
- create embeddings;
- use a vector store;
- persist reports;
- write files;
- read the prompt library;
- load prompts;
- mutate prompt registry data;
- read freeze memory;
- write freeze memory;
- read router canon;
- modify router prompt logic;
- modify router final selection;
- create route authority;
- create advisory rankings;
- create free-text advisory explanations;
- create MLRT-113;
- train, calibrate, or improve a model;
- add runtime Pilot or runtime Copilot behavior.

## Route invariance rule

The harness may only compare two caller-supplied governed decision strings. It
must not compute or select the decision. If advisory telemetry is associated
with a changed governed decision, the fixture is rejected as route variance.

## Scope accounting

Phase 2 adds 0 new real prompt-selection cases and creates no MLRT-113. The
harness is contract/stub/evaluation support only.

## Next safe correction

The next safe correction is a result-review gate:

Routing Signal Scorer ML Advisory-Signal Phase 2 Offline Evaluation Harness Result Review Gate v1
