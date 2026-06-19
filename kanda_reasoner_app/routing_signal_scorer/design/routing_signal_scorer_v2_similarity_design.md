# Routing Signal Scorer v2 Similarity Design

Feature ID: routing_signal_scorer_v2_similarity_design
Implementation status: DESIGN_ONLY
Runtime status: NOT_IMPLEMENTED
Authority status: NON_AUTHORITATIVE_DESIGN

## Purpose

This document defines the safe design boundary for a possible future similarity
layer in the KANDA routing signal scorer. It does not implement similarity
scoring. It does not change deterministic routing. It does not add machine
learning dependencies.

The goal is to decide whether a lightweight similarity helper would be useful
for prompt-call accuracy before any runtime code is written.

Core rule:

The scorer may suggest. The canon decides. Tests judge. Freeze memory records
validated behavior.

## Current frozen baseline

The following milestones must be treated as the current baseline:

- pre_output_contract_gates_v1
- routing_signal_scorer_v1_diagnostic
- routing_signal_scorer_manual_pilots_v1
- routing_signal_scorer_v1_advisory

The v2 similarity design must preserve all frozen behavior from that chain.

## Non-goals

This milestone must not:

- implement TF-IDF runtime scoring
- implement embedding runtime scoring
- add sklearn, numpy, torch, faiss, sentence-transformers, or vector databases
- add self-learning behavior
- add global cross-project memory
- auto-load prompts
- decide May proceed now
- output final required prompts or groups
- override the deterministic router
- silently modify startup delivery
- write project freeze memory outside the freeze workflow

## Allowed design outputs

A future similarity layer, if ever implemented, may only produce advisory data:

- candidate route-family labels
- candidate prompt-group labels
- confidence scores
- evidence snippets
- caution flags
- recommendation to run pre_output_contract_gates when needed

The output must explicitly state:

- authority: advisory_only
- canon_decides_final_route: true
- does_not_override_router: true
- may_proceed_now_decision: not_provided_by_similarity
- route_override: null

## Proposed future inputs

If runtime similarity is later approved, allowed inputs should be limited to:

- the user request text
- an explicit in-memory list of canonical route examples
- a small in-memory list of prompt group descriptions
- frozen test scenarios used for regression

Forbidden inputs:

- hidden global memories
- mutable self-training stores
- uncontrolled cross-project logs
- direct writes into startup ZIP sources
- direct writes into frozen feature memory

## Proposed future output schema

A future runtime function could return a dictionary like this:

```text
{
  "schema_version": "2.0-draft",
  "feature_id": "routing_signal_scorer_v2_similarity_runtime",
  "authority": "advisory_only",
  "does_not_override_router": true,
  "canon_decides_final_route": true,
  "may_proceed_now_decision": "not_provided_by_similarity",
  "route_override": null,
  "similarity_method": "rules_or_tfidf_or_embedding_declared_here",
  "candidate_route_families": [
    {
      "family": "patch_delivery_or_code_update",
      "score": 0.82,
      "evidence": ["patch ZIP", "install block"]
    }
  ],
  "candidate_prompt_groups": [],
  "caution_flags": [],
  "recommended_hooks": []
}
```

## Candidate route-label inventory

The initial label inventory should remain small:

- fast_path_simple_explanation
- governed_prompt_library_update
- patch_delivery_or_code_update
- terminal_install_artifact
- terminal_validation_artifact
- freeze_form_json_artifact
- freeze_hint_sidecar_artifact
- freeze_memory_workflow
- startup_delivery_change
- external_project_root_sensitive
- ambiguous_governed_request

New labels require tests before runtime use.

## Threshold policy draft

Similarity thresholds must be conservative:

- 0.00 to 0.29: ignore or low confidence
- 0.30 to 0.69: caution or secondary hint only
- 0.70 to 0.84: advisory candidate only
- 0.85 to 1.00: strong advisory candidate only

Even a high score must not become a route override.

## False-positive risks

Known risk classes:

- simple explanation requests that mention patch words historically
- medical or clinical text containing words like validation, diagnosis, or evidence
- freeze workflow requests that look like normal UI improvement requests
- prompt-library requests that include bypass wording
- startup delivery repair requests that look like simple file maintenance
- terminal cleanup requests that may conflict with validation-output retention rules

Fast Path protection must remain a first-class regression test.

## Future runtime decision gate

Before any runtime similarity implementation, a separate milestone must prove:

1. The design is frozen.
2. Baseline v1 diagnostic tests still pass.
3. Manual pilot tests still pass.
4. Advisory tests still pass.
5. New similarity tests preserve no-router-override behavior.
6. False-positive tests protect Fast Path.
7. No heavyweight dependency is introduced without explicit approval.
8. No startup ZIP size or load behavior is changed accidentally.

## Rollback criteria

A future similarity runtime must be reverted or disabled if it:

- over-routes simple explanation tasks
- weakens Confirm and Write human confirmation
- bypasses pre_output_contract_gates for high-risk outputs
- changes final routing behavior without explicit governed approval
- introduces hidden self-learning
- makes startup delivery stale or unstable
- stores active project memory in project_freeze_ledger

## Recommended next milestone after this design

Do not implement runtime similarity immediately.

The next safe milestone after freezing this design would be:

routing_signal_scorer_v2_similarity_test_corpus

That milestone should add a small fixed corpus of examples and expected labels.
It should still avoid runtime TF-IDF, embeddings, or self-learning.
