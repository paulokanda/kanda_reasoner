---
prompt_id: error_memory_active_ready_correction_blueprint
prompt_code: KPR-12-002
title: Error Memory Active-Ready Correction Blueprint
version: 2.1.0
status: active
load_type: routed
owner_box: 12_generalized_project_canons
classification: error_memory_draft_readiness_promotion_workflow
source_stage: prompt-freeze-error-memory-lifecycle-alignment-v1
updated_for: prompt-freeze-error-memory-lifecycle-alignment-v1
---

# Error Memory Active-Ready Correction Blueprint

## Purpose

Route a real Error Memory draft or rejected lesson through evidence recovery,
current-schema validation, correction, and explicit human memorization readiness.

## Authority model

- `kanda_reasoner_app/error_memory/models.py` and current application schema and
  validators are machine authority for active-ready fields.
- `KPR-12-003` owns only the marker-wrapped output envelope.
- `KPR-12-004` is the human-readable model and must remain synchronized with the
  application schema.
- The Error Memory GUI owns intake, parsing, validation and the explicit human
  `Memorize Error` action.
- This prompt does not memorize a lesson, install patches, or create validation evidence automatically.

## When to load

- A draft is rejected by `active_ready_missing_reasons` or equivalent current
  application validation.
- The user asks to correct, promote, or validate an Error Memory lesson.
- Real correction, installation and validation evidence must be assembled.

## Readiness workflow

1. Record the raw error/draft and operation identity.
2. Inspect the current application schema and active-ready validator.
3. Recover only evidence that is present in the supplied logs/artifacts.
4. Classify every required field as present, missing, contradictory, or stale.
5. Keep the lesson draft/needs-review while any active-ready requirement lacks
   evidence.
6. When complete, render through KPR-12-003 and KPR-12-004.
7. Validate the exact outgoing JSON against current application rules.
8. Leave final memorization to the explicit human GUI action.

## Required evidence

- real error and scrubbed chronology;
- root cause, wrong assumption, correction and prevention rule;
- patch/artifact identity when applicable;
- install summary and exact validation command;
- observed validation markers and evidence path/hash when available;
- redaction/export-safety assessment;
- supersession relationship when applicable.

## Do not regress

- Do not duplicate the complete machine schema in this workflow prompt.
- Do not invent patch names, commands, PASS markers, timestamps or evidence.
- Do not convert heuristic normalization into proof of active readiness.
- Do not emit `status: active` when current application validation would reject
  the lesson.
- Do not memorize automatically.

## Required output

Return either:

- ordinary chat beginning with `DRAFT_ONLY`, followed by the exact
  missing/contradictory/stale fields; or
- one receive-ready Error Memory transport block rendered exactly through
  `KPR-12-003` and consistent with the current `KPR-12-004` model. The final
  visible receive-ready output must contain exactly one JSON object between
  `KANDA_ERROR_LESSON_JSON_BEGIN` and `KANDA_ERROR_LESSON_JSON_END`, with no
  prose, validation result, reminder, Markdown fence, or second machine object
  before or after the markers. Current-schema validation and the human-action
  reminder must be completed before the final transport block is emitted, not
  appended to it.
