---
prompt_id: error_memory_model_template
prompt_code: KPR-12-004
title: Error Memory Human-Readable Lesson Model
version: 2.0.0
status: active
load_type: routed
owner_box: 12_generalized_project_canons
classification: human_readable_error_memory_model_verified_against_application_schema
source_stage: prompt-audit-wave10a-final-productization-generalized-canons-closure-v1
updated_for: prompt-audit-wave10a-final-productization-generalized-canons-closure-v1
---

# Error Memory Human-Readable Lesson Model

## Authority and synchronization

Before use, verify this model against the current machine authority in
`kanda_reasoner_app/error_memory/models.py`, current schema validators, and the
Error Memory intake parser. If fields differ, the application schema wins and
this prompt must be corrected before active output.

Use KPR-12-002 for readiness and KPR-12-003 for the exact output envelope.

## Reusable lesson model

KANDA_ERROR_LESSON_JSON_BEGIN
{
  "schema_version": "<current_schema_version>",
  "project_slug": "<project_slug>",
  "lesson_id": "lesson-<stable-error-slug>-v1",
  "status": "<draft_or_active_after_validation>",
  "superseded_by": "",
  "operation_phase": "<current_allowed_phase>",
  "created_at_utc": "<YYYY-MM-DDTHH:MM:SSZ>",
  "updated_at_utc": "<YYYY-MM-DDTHH:MM:SSZ>",
  "source_patch_zip": "<real_patch_or_artifact_identity>",
  "raw_error_text": "<real concise error>",
  "raw_error_snapshot_scrubbed": "<scrubbed chronology>",
  "symptom": "<observed symptom>",
  "root_cause": "<evidenced root cause>",
  "wrong_assumption": "<false assumption>",
  "correct_fix": "<observed correction>",
  "do_not_repeat_rule": "<enforceable rule>",
  "long_term_prevention": "<durable prevention>",
  "redaction": {
    "applied": true,
    "export_safe": true,
    "rules": ["<concrete redaction rule>"]
  },
  "exception": {
    "type": "<normalized type>",
    "phase": "<phase>",
    "relative_file_path": "<relative path or surface>",
    "function_or_test_name": "<function/test/surface>",
    "message_normalized": "<normalized message>",
    "stacktrace_scrubbed": "<scrubbed traceback or explicit no-trace summary>"
  },
  "fingerprint": {
    "strategy": "v1_structural_conservative",
    "components": ["<stable component>"],
    "fingerprint_hash": "<stable lowercase slug>"
  },
  "prevention_triggers": ["<real trigger>"],
  "regression_check": {
    "type": "validation_command",
    "command": "<exact real command>",
    "expected_marker": "<exact observed/required marker>",
    "required_before_freeze": true
  },
  "validation_command_summary": "<plain-language command and marker summary>",
  "validation_evidence": ["<real observed evidence>"],
  "install_command_summary": "<real install/correction summary>",
  "notes": "<limitations and edge cases>"
}
KANDA_ERROR_LESSON_JSON_END

## Field guidance

- Preserve real chronology and normalized failure identity.
- Use non-empty stable fingerprint components and prevention triggers.
- Never invent validation, installation, freeze, or timestamp evidence.
- Keep `status` non-active until current application validation accepts the
  candidate.
- Return one complete lesson only when KPR-12-003 final-output mode is requested.
