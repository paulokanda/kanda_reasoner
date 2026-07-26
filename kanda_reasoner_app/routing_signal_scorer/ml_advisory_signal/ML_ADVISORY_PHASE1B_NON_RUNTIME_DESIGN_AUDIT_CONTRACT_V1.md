# ML Advisory Signal Phase 1b Non-Runtime Design Audit Contract v1

Feature title: Routing Signal Scorer ML Advisory-Signal Phase 1b Non-Runtime Design Audit Contract v1
Feature ID: rss_ml_adv_phase1b_design_audit_contract_v1

## Reviewed prerequisite

This design audit starts only after the Phase 1a result review gate is
validated and frozen:

Routing Signal Scorer ML Advisory-Signal Phase 1a Result Review Gate v1

Phase 1a established the non-runtime boundary contract. Phase 1b does not
replace it, weaken it, or expand authority. Phase 1b records the readiness
criteria needed before a later offline advisory evaluation harness may be
created.

## Purpose

Phase 1b answers the design questions that must be settled before any future
non-runtime advisory logic is evaluated:

1. Which advisory input fields are sufficient for offline advisory tests.
2. Which output flags and enum reason codes remain safe without rankings.
3. Which failure modes require advisory abstention instead of action.
4. Which route-invariance tests are required before advisory metadata is passed
   near router intake.
5. Which evidence is required before any future real adapter can be considered.
6. Which prompt-intake and manual-code boundaries must remain unchanged.

Phase 1b is an audit contract. It is not a model adapter, not a runtime shadow
mode, not a router integration, and not prompt selection logic.

## Safe advisory input contract for future offline evaluation

Future offline evaluation may use only caller-supplied, in-memory values that
are already available to a governed test harness:

- task text or synthetic test request;
- deterministic route family already selected by governed test setup;
- optional candidate prompt group labels supplied by a test fixture;
- optional manual prompt-code hint supplied by a test fixture;
- expected containment class supplied by a test fixture;
- audit family and case identifier supplied by a test fixture.

Phase 1b forbids source scanning, prompt library reads, freeze-memory reads,
router-canon reads, automatic prompt loading, registry mutation, and discovery
of cases from the live project tree.

## Safe advisory output contract for future offline evaluation

Future offline evaluation may use only bounded telemetry fields already allowed
by the Phase 1a firewall:

- advisory status;
- bounded confidence bucket;
- ambiguity flag;
- containment flag;
- prompt gap flag;
- enum reason codes;
- bounded observations.

Future offline evaluation must not emit route decisions, selected prompts,
final prompts, winners, rankings, free-text explanations, generic metadata
payloads, override requests, or commands to bind prompts.

## Required abstention rules

A future advisor must abstain or degrade to NullAdvisor-equivalent output when:

- input is missing required test fields;
- confidence is below the governed threshold;
- manual prompt code conflicts with canonical prompt lifecycle state;
- reason codes are unknown;
- any forbidden output field is present;
- any provider, embedding, network, file-write, persistence, router-canon,
  prompt-library, or freeze-memory dependency would be needed;
- the advisory signal would need to alter final route selection.

Abstention is a safe outcome. Acting without the contract is not safe.

## Required route-invariance gate

Before a later offline evaluation harness can be considered, it must prove:

- final governed route is identical with NullAdvisor and MockAdvisor;
- advisory output may be recorded only as in-memory test-local telemetry;
- no advisory field can change required prompts or groups;
- no advisory field can bypass freeze, prompt-intake, patch delivery, or startup
  synchronization gates;
- disagreement between advisory signal and canon produces audit evidence only,
  not a route change.

## Explicit non-goals

Phase 1b does not add real ML. Phase 1b does not add provider calls. Phase 1b
does not add embeddings, vector stores, persistence, training data, dataset
creation, model training, calibration, model improvement, prompt loading,
prompt registry mutation, freeze-memory write, router-canon direct access,
runtime shadow mode, router prompt logic modification, router final selection
modification, route authority, runtime Pilot behavior, or runtime Copilot
behavior.

Phase 1b creates no MLRT-113 and adds 0 new real prompt-selection cases.

## Exit condition

Phase 1b may end only by validating and freezing this design audit contract.
The next safe feature after freeze is a Phase 1b result-review gate, not direct
real ML integration:

Routing Signal Scorer ML Advisory-Signal Phase 1b Non-Runtime Design Audit Result Review Gate v1
