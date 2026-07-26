---
prompt_id: error_memory_active_ready_json_template
prompt_code: KPR-12-003
title: Error Memory Marker-Wrapped JSON Output Envelope
version: 2.0.0
status: active
load_type: routed
owner_box: 12_generalized_project_canons
classification: error_memory_marker_output_envelope
source_stage: prompt-audit-wave10a-final-productization-generalized-canons-closure-v1
updated_for: prompt-audit-wave10a-final-productization-generalized-canons-closure-v1
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
