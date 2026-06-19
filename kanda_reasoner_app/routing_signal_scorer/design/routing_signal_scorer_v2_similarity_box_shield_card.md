# Routing Signal Scorer v2 Similarity Box Shield v1

Feature ID: `routing_signal_scorer_v2_similarity_box_shield_v1`

## Purpose

This shield applies KANDA Box Shielding Canon (KBSC) to the current
`routing_signal_scorer` similarity chain before stronger ML, embeddings,
TF-IDF dependencies, vector stores, self-learning, prompt auto-loading,
dispatcher automation, or cross-box routing authority are added.

A shield is an architectural fitness-function suite for a bounded context.
This card is the local scorer-card and trade-off record for the similarity
chain.

## Bounded context map

Owning bounded context:

```text
kanda_reasoner_app/routing_signal_scorer
```

Allowed public contract:

```text
score_routing_signals
summarize_signal_result
build_routing_advisory
summarize_advisory
build_similarity_runtime_lite_advisory
summarize_similarity_runtime_lite_advisory
build_similarity_ui_preview_adapter
render_similarity_ui_preview_text
build_similarity_prompt_context_preview
render_similarity_prompt_context_preview_text
build_similarity_box_shield_status
render_similarity_box_shield_status_text
```

Forbidden neighboring boxes:

```text
kanda_prompt_workspace
kanda_reasoner_app/freeze_hint_intake
kanda_reasoner_app/freeze_after_update
kanda_reasoner_app/freeze_after_update_gui
project_freeze_ledger
project_freeze_after_update
startup_delivery
prompt_library_runtime_loading
```

Dependency direction rule:

```text
routing_signal_scorer may expose advisory data outward through its public
contract, but must not import, mutate, or decide for prompt library, freeze,
GUI, startup, or project-memory boxes.
```

## Protected architecture characteristics

```text
advisory_only
deterministic
side_effect_free
bounded_execution
schema_validated_output
no_authority_escalation
no_cross_box_mutation
stdlib_only_runtime_lite
candidate_context_only
presentation_only_ui_preview
```

## Truth-source priority ladder

1. The deterministic KANDA routing canon decides final route, required prompts,
   missing context, and May proceed now.
2. The routing_signal_scorer similarity chain provides advisory evidence only.
3. The runtime-lite corpus anchors provide deterministic lexical hints only.
4. UI and prompt-context previews display candidate evidence only.

## Forbidden authority escalation matrix

The similarity chain must not emit or create authority for:

```text
final_route
may_proceed
may_proceed_now
required_prompts
required_prompt_files
auto_load_prompts
load_prompts_now
router_override
freeze_write
startup_mutation
prompt_library_mutation
```

Allowed weaker fields remain non-authoritative:

```text
may_proceed_now_decision=not_provided_by_similarity
required_prompts_final_decision=not_provided_by_similarity
automatic_prompt_loading=False
route_override=None
candidate_contexts_only=True
```

## Shield state machine

```text
NO_MATCH          No visible similarity case; advisory output still contains no authority.
WEAK_MATCH        Visible-low match; not eligible for route-family suggestion promotion.
STRONG_ADVISORY   Promoted-medium match; still advisory and candidate-only.
HIGH_SIGNAL       High similarity anchor; still no final route, prompt, or May-proceed authority.
AMBIGUOUS_MATCH   Close competing anchors must be treated as ambiguous advisory evidence.
ERROR_STATE       Malformed input must degrade to deterministic safe advisory output, not authority.
```

## Trade-off record

Chosen now:

- Keep runtime-lite deterministic lexical similarity.
- Add shield contract and permanent regression tests.
- Use stdlib-only tests rather than external architecture testing tools.
- Keep UI preview and prompt-context preview as display/candidate-only surfaces.
- Keep the full routing canon and KBSC in prompt library, not inside this runtime box.

Rejected for this shield:

- Embeddings.
- TF-IDF dependency.
- Vector store.
- Self-learning state.
- Prompt auto-loading.
- Router override.
- May proceed now decision.
- Cross-box integration with prompt library, freeze, GUI, or startup boxes.

Postponed:

- Stronger ML.
- Dispatcher automation.
- Prompt composer integration.
- Runtime corpus hash rejection system.

## Regression matrix

This shield protects SM-25 through SM-49:

```text
SM-25 deterministic snapshot baseline
SM-26 idempotency
SM-27 ambiguous match visibility without authority
SM-28 error resilience
SM-29 forbidden authority fields absent
SM-30 schema version and feature id
SM-31 no placeholder commitment
SM-32 input sanitization boundary
SM-33 no side effects
SM-34 dependency ceiling
SM-35 decision report language guard
SM-36 candidate label control
SM-37 high-score authority cap
SM-38 box invasion audit
SM-39 bounded execution/model-DoS guard
SM-40 no actionable command surface
SM-41 OWASP-style threat coverage declaration
SM-42 KANDA scorer shield card exists
SM-43 stdlib-only fuzz/property loop
SM-44 runtime forbidden dependency scan
SM-45 dependency direction guard
SM-46 architecture fitness metadata
SM-47 bounded context map
SM-48 trade-off record
SM-49 public-contract-only integration
```

## Final canon

```text
The routing_signal_scorer may emit only bounded, deterministic,
schema-validated, advisory-only evidence. It must never emit an instruction,
authority signal, prompt-loading action, routing decision, May-proceed decision,
file mutation, learned state mutation, or cross-box side effect.
```
