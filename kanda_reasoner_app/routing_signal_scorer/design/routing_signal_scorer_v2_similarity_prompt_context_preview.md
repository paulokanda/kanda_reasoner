# Routing Signal Scorer v2 Similarity Prompt Context Preview v1

Feature ID: routing_signal_scorer_v2_similarity_prompt_context_preview_v1

## Purpose

This milestone adds a candidate prompt-context preview adapter on top of the
advisory-only similarity runtime and UI preview adapter.

The adapter helps logs or GUI panes show which prompt/context areas may be
worth inspecting. It does not decide required prompts, does not load prompts,
does not change May proceed now, and does not override deterministic routing.

## Scope

Included:

- Build candidate context labels from advisory route-family hints.
- Preserve recommended hook visibility.
- Render plain text preview lines for GUI/log display.
- Keep all output explicitly candidate-only.

Excluded:

- Final required prompt decisions.
- Automatic prompt loading.
- Router override.
- May proceed now decisions.
- Embeddings, TF-IDF dependency, vector stores, self-learning, or stronger ML.
- GUI rewrite.

## Authority boundary

The adapter authority is advisory_only. The deterministic KANDA routing canon
continues to decide final route, missing context, required prompts, and whether
work may proceed.

## Candidate context rules

Candidate context labels are derived from advisory route families and hooks.
They are readable hints only. They are not a substitute for folder cards,
specialist prompts, prompt-library indexes, startup delivery rules, freeze
workflow rules, or pre-output contract gates.

## Regression requirements

Tests must verify:

- The feature ID and public exports exist.
- Candidate labels are shown for patch, freeze, startup, ambiguous, and
  Fast Path scenarios.
- High-risk hooks remain visible.
- Candidate labels do not become final required prompts.
- Automatic prompt loading remains false.
- May proceed now remains not_provided_by_similarity.
- Router override remains None.
- Prior runtime-lite, UI preview, decision report, explainability, policy,
  corpus, and freeze-hint state-machine tests remain passing.
