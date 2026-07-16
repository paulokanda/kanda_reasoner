# Error Memory Model Template

## Purpose

This is the reusable model for the text AI must create for the KANDA Reasoner **Error Memory tab -> AI-assisted error lesson intake** text window.

Use this after reading:

```text
kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/12_generalized_project_canons/error_memory_active_ready_json_template.md
```

## How AI must use this model

Replace every placeholder. Keep the marker lines exactly. Return one complete lesson only. Do not wrap the final answer in markdown fences.

Use `status: active` only when the lesson is active-ready and evidence-backed. If any required field is unknown, do not fabricate it.

## Reusable active-ready lesson model

KANDA_ERROR_LESSON_JSON_BEGIN
{
"schema_version": "1.0",
"project_slug": "<project_slug>",
"lesson_id": "lesson-<short-error-slug>-v1",
"status": "active",
"superseded_by": "",
"operation_phase": "<patch-delivery|validation|freeze|runtime|prompt-sync|startup-sync|unknown>",
"created_at_utc": "[YYYY-MM-DDTHH:MM:SSZ](YYYY-MM-DDTHH:MM:SSZ)",
"updated_at_utc": "[YYYY-MM-DDTHH:MM:SSZ](YYYY-MM-DDTHH:MM:SSZ)",
"source_patch_zip": "<patch_zip_name_or_relevant_artifact>",
"raw_error_text": "<concise but complete raw error or user-reported failure text>",
"raw_error_snapshot_scrubbed": "<scrubbed snapshot of what happened, including commands, visible markers, failure text, and repair result when available>",
"symptom": "<what the user/app observed>",
"root_cause": "<why the failure happened>",
"wrong_assumption": "<false assumption that caused the error>",
"correct_fix": "<correct repair or behavior>",
"do_not_repeat_rule": "<one enforceable rule AI must not violate again>",
"long_term_prevention": "<how future patches/prompts/validators should prevent recurrence>",
"redaction": {
"applied": true,
"export_safe": true,
"rules": [
"No secrets, credentials, API keys, tokens, patient data, or private external service data are included.",
"The lesson contains only project workflow, patch-delivery, validation, error, or architecture context needed to prevent recurrence.",
"Local absolute paths are avoided or normalized where possible; retain only technical project identifiers needed for KANDA Reasoner context."
]
},
"exception": {
"type": "<NormalizedExceptionOrRegressionType>",
"phase": "<patch-delivery|validation|freeze|runtime|prompt-sync|startup-sync|unknown>",
"relative_file_path": "<relative file path, UI surface, prompt path, or command surface involved>",
"function_or_test_name": "<function, method, validator, test, GUI action, or workflow gate involved>",
"message_normalized": "<normalized failure message>",
"stacktrace_scrubbed": "<scrubbed traceback or explicit no-traceback operational failure summary>"
},
"fingerprint": {
"strategy": "v1_structural_conservative",
"components": [
"<exception.type>",
"<primary file or workflow>",
"<failure marker>",
"<missing field or violated rule>",
"<validator or UI gate>"
],
"fingerprint_hash": "<stable_lowercase_slug_for_this_failure>"
},
"prevention_triggers": [
"<trigger phrase or workflow where this lesson must be recalled>",
"<button, command, validator, or patch type involved>",
"<specific warning/error marker>",
"<related artifact or path>"
],
"regression_check": {
"type": "validation_command",
"command": "<exact validation command using forward slashes when possible>",
"expected_marker": "<expected validation marker, e.g. VALIDATION OK: feature-id\nSTATUS: IN_SYNC>",
"required_before_freeze": true
},
"validation_command_summary": "<plain-language summary of the validation command and required markers>",
"validation_evidence": [
"<real observed validation evidence item 1>",
"<real observed validation evidence item 2>",
"<real observed repair/freeze/contract marker when available>"
],
"install_command_summary": "<how the correction was or should be installed; state if install was not the failing step>",
"notes": "<extra constraints, edge cases, or do-not-confuse guidance>"
}
KANDA_ERROR_LESSON_JSON_END

## Field guidance

* `lesson_id`: stable, lowercase, starts with `lesson-`, and includes a version suffix.
* `raw_error_text`: preserve the real user/app-facing failure in concise form.
* `raw_error_snapshot_scrubbed`: include enough chronology to understand what failed and what fixed it.
* `exception.phase`: must not be empty.
* `exception.relative_file_path`: may be a UI surface or command surface if no code file caused the failure.
* `exception.stacktrace_scrubbed`: if there is no traceback, explicitly say so and summarize the operational failure.
* `fingerprint.components`: non-empty list of stable identifying parts.
* `fingerprint.fingerprint_hash`: stable lowercase slug; do not use random hashes unless the project requires them.
* `regression_check.expected_marker`: include every marker required by the project contract.
* `validation_evidence`: real evidence only; do not invent sandbox validation or freeze output.
