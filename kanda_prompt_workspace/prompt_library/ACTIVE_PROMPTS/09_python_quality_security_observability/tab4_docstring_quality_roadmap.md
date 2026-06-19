# Tab 4 Docstring Quality Roadmap

## Box Logic Requirement

Before any implementation, repair, refactor, prompt update, governance update, or bundle creation, the AI must:

- Identify the active box before implementation.
- State owner paths.
- State files allowed to change.
- State files explicitly out of scope.
- Declare cross-box touches.
- Preserve public contracts.
- Validate the active box and any touched external box.


Version: 1.0.0
Status: Tab 4 quality improvement roadmap
Prompt ID: kanda_tab4_docstring_quality_roadmap
Prompt type: implementation roadmap / quality protocol
Scope: Improve missing-docstring generation quality without breaking Tab 4 safety.

## Purpose

Improve Tab 4 docstring creation quality while preserving scan/diff/write safety,
AST guards, AI-optional behavior, and deterministic fallback.

## Active box

```text
tab_4_docstring_tool
```

Owner paths include:

```text
kanda_reasoner_app/insert_missing_docstrings_gui/
kanda_reasoner_app/insert_missing_docstrings_gui/ai_docstring_generator.py
kanda_reasoner_app/insert_missing_docstrings_gui/ai_config.py
kanda_reasoner_app/insert_missing_docstrings_gui/context_builder.py
kanda_reasoner_app/insert_missing_docstrings_gui/docstring_policy.py
kanda_reasoner_app/insert_missing_docstrings_gui/docstring_validator.py
kanda_reasoner_app/insert_missing_docstrings_gui/ai_docstring_generator_help/
kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_help/
kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_gui_help/
```

Out of scope by default: Tab 1, Tab 2, JSON splitter, retriever, prompt builder,
AI bridge, runtime collector, static collector, and governance.

## Safety contract to preserve

- scan / diff / write separation;
- AST parse before and after insertion;
- docstring-only AST guard;
- heuristic fallback unless strict mode is requested;
- report rows with source and confidence;
- ability to run without AI;
- Windows/PyCharm compatibility;
- standard Python 3.10+;
- no unrelated tab changes.

## Roadmap

### T4Q-000 Task 0 audit

Audit response parsing, AI generator, heuristics, context builder, validator,
collection, insertion formatting, and AST safety. No code changes.

Key question: does structured rendering call `_prettify` without importing it?

### T4Q-001 Structured-rendering repair

If confirmed, fix `_prettify` import from the actual owner module and add focused
tests for module, class, function, and method structured rendering.

### T4Q-002 Fallback observability

Make AI fallback and low-confidence events visible in report rows and warnings.
Do not hide structured-rendering failures behind normal output.

### T4Q-003 Baseline quality benchmark

Create a small golden corpus before major prompt/schema changes. Track:

```text
structured_render_success_rate
AI_used_rate
heuristic_fallback_rate
validator_rejection_rate
TODO_density
invented_parameter_count
invented_raise_count
summary_vagueness_count
docstring_only_AST_safety_pass
idempotency_pass
```

### T4Q-004 Expand SymbolContext evidence

Add deterministic AST-derived signals only: branch count, return count, called
functions, external calls, self mutations, parameter mutations, awaited names,
yield usage, IO/subprocess/logging/global-write hints, and kind hints.

### T4Q-005 Semantic validator warning-only

Add semantic quality checks first as warnings, not hard gates. Examples:
summary vagueness, boolean-return consistency, async consistency, property
section misuse, side-effect claim support, and mutation claim support.

### T4Q-006 Kind-specific prompt strategy

Differentiate modules, classes, `__init__`, properties, cached properties,
dataclasses, GUI callbacks, validators, parsers/loaders, orchestrators, private
helpers, async functions, and generator functions.

### T4Q-007 Staged schema v2

Do not jump to a huge schema. Add only:

```json
{
  "summary": "string",
  "extended_description": "string",
  "parameters": [],
  "returns": {},
  "raises": [],
  "attributes": [],
  "notes": [],
  "side_effects": [],
  "mutated_state": [],
  "preconditions": [],
  "uncertain_fields": []
}
```

Model self-confidence is telemetry only, not an acceptance gate.

### T4Q-008 Heuristic quality floor

Reduce generic TODO placeholders. Prefer safe factual docstrings for trivial and
simple symbols; allow precise TODO only when evidence is insufficient.

### T4Q-009 One repair pass behind quality mode

Behind `quality_mode=True`, allow one deterministic-validator-driven repair pass.
Do not add LLM-as-judge as a hard gate initially.

## Avoid

- broad Tab 4 rewrites;
- hardcoding model size or vendor;
- disabling fallback by default;
- model self-confidence as acceptance gate;
- LLM-as-judge hard gates before deterministic benchmarks exist;
- claiming semantic quality without a benchmark.
