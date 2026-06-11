# prompt_builder refactor notes

## Goal
Reduce `prompt_builder.py` to a thin orchestrator while preserving the public
`PromptBuilder` contract and helper compatibility aliases.

## Split
- `prompt_builder_help/prompt_classification.py`
- `prompt_builder_help/answer_style.py`
- `prompt_builder_help/callsite_evidence.py`
- `prompt_builder_help/prompt_sections.py`
- `prompt_builder_help/widget_registry_section.py`

## Kept in origin
- `PROJECT_SCOPE_GUARDRAIL`
- `PromptBuilder.build(...)`
- backward-compatible helper aliases:
  - `_norm`
  - `_tokenize_query`
  - `_build_answer_style_instructions`
  - `is_which_method_calls_question`

## Notes
- Widget-listing router import remains lazy inside the helper to avoid
  import-time cycles.
- The refactor also normalizes one duplicated phrase in the final instructions
  sentence about implementation truth.
