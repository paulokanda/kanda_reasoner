---
prompt_id: error_memory_active_ready_json_template
prompt_code: KPR-12-003
title: Error Memory Marker-Wrapped JSON Output Envelope
version: 2.1.0
status: active
load_type: routed
owner_box: 12_generalized_project_canons
classification: error_memory_marker_output_envelope
source_stage: prompt-audit-wave10a-final-productization-generalized-canons-closure-v1
updated_for: error-memory-lesson-pre-output-envelope-guard-v1
---

# Error Memory Marker-Wrapped JSON Output Envelope

## Purpose

Define only the marker-wrapped output envelope for text pasted into the Error Memory
AI-assisted intake surface. Current application schema/models remain field
authority. KPR-12-004 supplies the synchronized human-readable model.

## Exact envelope

The final active-ready candidate must contain exactly one JSON object between:

```text
KANDA_ERROR_LESSON_JSON_BEGIN
{ ... one current-schema lesson object ... }
KANDA_ERROR_LESSON_JSON_END
```

## Output rules

- Do not wrap the final block in markdown fences.
- Do not add prose before or after the final block.
- Use valid JSON with double-quoted keys and strings.
- Use forward slashes in command/path strings when the application contract
  requires them; reject control-character corruption.
- Replace every placeholder with concrete evidence.
- Emit `status: active` only after KPR-12-002 readiness and current application
  validation succeed.
- When evidence is incomplete, do not fabricate an active lesson; return to the
  correction workflow instead of emitting a misleading block.

## Non-ownership

This envelope does not define the authoritative field schema, install behavior,
validation evidence, GUI parsing, or human memorization action.
## Mandatory pre-output machine check

Before releasing a receive-ready Error Memory lesson, audit the COMPLETE outgoing
text as transport data. Do not validate only the inner JSON.

The check must prove all of the following:

- `text.startswith("KANDA_ERROR_LESSON_JSON_BEGIN")`;
- `text.endswith("KANDA_ERROR_LESSON_JSON_END")`;
- the begin marker count is exactly one;
- the end marker count is exactly one;
- no non-whitespace content exists outside the marker pair;
- the marker payload contains no Markdown fence token such as triple backticks;
- the marker names contain no Markdown escape backslashes;
- parsing the content between the markers yields one JSON object, not an array,
  scalar, multiple objects, or free text;
- there is no prose, writing-block syntax, citation token, comment, or trailing
  material after the end marker.

If any check fails, do not emit a receive-ready lesson block. Correct the output
privately first.

### Receiver failure signature

The current GUI may report:

```text
The AI answer could not be parsed. Ask AI to return exactly one valid JSON object
between KANDA_ERROR_LESSON_JSON_BEGIN and KANDA_ERROR_LESSON_JSON_END, with no
markdown and no prose.

Error: MCARD_FORMATTED_LESSON_JSON_REQUIRED
```

Treat this as definitive evidence that the Error Memory transport contract was
not satisfied. The historical `MCARD_` token is an implementation compatibility
name only; it does not transfer semantic ownership to Architecture Review MCard.

### Anti-rendering rule

Machine-consumed transport outranks chat presentation styling. Never add a fenced
`json` block merely to improve readability. Never escape underscores in the
markers. The text supplied to the user must already be the exact text that can be
pasted into Error Memory intake.

