# Routing Signal Scorer v2 Similarity UI Preview Adapter v1

Feature ID: routing_signal_scorer_v2_similarity_ui_preview_adapter_v1

## Purpose

Expose the existing runtime-lite similarity decision report as a plain text
GUI/log preview payload. This milestone is presentation-only. It does not
change routing decisions, prompt loading, May proceed now behavior, required
prompt selection, or similarity authority.

## Allowed behavior

- Build a preview payload from the existing advisory similarity runtime.
- Show compact human-readable decision report lines.
- Include explicit advisory-only and canon-authority guardrails in the preview.
- Keep output suitable for GUI text boxes, logs, diagnostics, and validation.

## Forbidden behavior

- Do not override deterministic routing.
- Do not decide May proceed now.
- Do not decide final required prompts.
- Do not auto-load prompts.
- Do not add embeddings, TF-IDF dependencies, vector stores, external ML
  dependencies, self-learning, or cross-project memory.
- Do not make preview output authoritative.

## Public contract

- build_similarity_ui_preview_adapter(text, max_matches=3, min_similarity=0.18)
- render_similarity_ui_preview_text(preview)

Both functions are presentation adapters over the existing runtime-lite advisory.
The canon still decides final route, required prompts, missing context, and May
proceed now.
