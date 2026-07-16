HANDOFF — KANDA Reasoner Routing Signal Scorer Chain

Current project:

E:\kanda_reasoner

Prompt workspace:

E:\kanda_reasoner\kanda_prompt_workspace

Current status:

The routing signal scorer chain is now implemented, validated, behavior-tested, and frozen.

Closed frozen milestones:

1. routing_signal_scorer_v1_diagnostic

Freeze ID:

freeze-20260616-routing-signal-scorer-v1-diagnostic

Status:

INSTALLED / VALIDATED / FROZEN

Purpose:

Adds a diagnostic-only route-signal scorer.

It detects likely task/routing signals such as:

* fast_path_simple_explanation
* governed_prompt_library_update
* patch_delivery
* terminal_install_output
* terminal_validation_output
* freeze_form_json
* freeze_hint_sidecar
* freeze_memory_write
* external_project_root_sensitive
* ambiguous_or_needs_router_context
* pre_output_contract_gate_required
* confirmation_gate_bypass_risk

Hard boundary:

The diagnostic scorer does not override the router.
It does not decide May proceed now.
It does not auto-load prompts.
It does not replace the deterministic canon.

Core rule:

The scorer may suggest.
The canon decides.

2. routing_signal_scorer_manual_pilots_v1

Freeze ID:

freeze-20260616-routing-signal-scorer-manual-pilots-v1

Status:

INSTALLED / VALIDATED / FROZEN

Purpose:

Adds manual-pilot regression tests for the scorer.

It validates 12 scenario classes, including:

* Fast Path protection
* patch/terminal output detection
* freeze hook recommendation
* RG-028 behavior
* RG-029 behavior
* RG-030 behavior
* no-router-override behavior

Hard boundary:

This milestone added tests only.
It did not change scorer behavior.
It did not change router behavior.
It did not change startup delivery.

3. routing_signal_scorer_v1_advisory

Freeze ID:

freeze-20260616-routing-signal-scorer-v1-advisory

Status:

INSTALLED / VALIDATED / FROZEN

Purpose:

Adds advisory-only route-family suggestions and caution flags.

It can recommend:

* likely route family
* caution flags
* pre_output_contract_gates when high-risk output is detected

Hard boundary:

Advisory output remains advisory only.
The canon still decides final routing.
It does not decide May proceed now.
It does not override the router.
It does not auto-load prompts.
It does not introduce real ML, embeddings, TF-IDF, or self-learning.

Current frozen chain:

pre_output_contract_gates_v1: FROZEN
routing_signal_scorer_v1_diagnostic: FROZEN
routing_signal_scorer_manual_pilots_v1: FROZEN
routing_signal_scorer_v1_advisory: FROZEN

Latest freeze memory status:

FREEZE_MEMORY_STATUS: OK

Latest freeze exposure/startup refresh:

AI-send exposure refreshed.
Startup freeze context refreshed.
Context file inside startup ZIP: 09_active_project_freeze_context.md

Important preserved rule:

project_freeze_ledger is reusable freeze engine logic.
Active project freeze memory belongs only under:

<active_project_root>\project_freeze_after_update\frozen_features_memory

For this project:

E:\kanda_reasoner\project_freeze_after_update\frozen_features_memory

Do not store active project freeze memory inside project_freeze_ledger.

Current core principle:

The scorer may suggest.
The canon decides.
Tests judge.
Freeze memory records validated behavior.

What not to do next:

Do not jump directly to real machine learning.
Do not add self-learning.
Do not let the scorer silently update routing behavior.
Do not let fuzzy similarity override frozen canon.
Do not add heavy dependencies.
Do not destabilize startup by loading large scorer data into the startup prompt pack.
Do not modify the deterministic router unless a later governed patch explicitly approves a small integration point.

Next safe topic:

routing_signal_scorer_v2_similarity_design

This should be design-only first.

The next session should discuss whether to add a lightweight similarity design layer before implementation.

Expected next discussion:

Should v2 use:

1. rules-only extensions,
2. local TF-IDF-style similarity,
3. embedding-style similarity later,
4. or no similarity at all?

Recommended answer:

Do not implement similarity yet.

First create a design/spec/test-plan milestone that defines:

* allowed inputs
* route-label examples
* expected outputs
* thresholds
* false-positive risks
* Fast Path protection
* no-router-override guarantees
* no self-learning guarantees
* validation matrix
* rollback criteria

The next patch, if approved later, should probably be:

routing_signal_scorer_v2_similarity_design

Not:

routing_signal_scorer_v2_similarity_runtime

because runtime similarity should only be implemented after the design and tests are frozen.
