# Prompt Metadata Consistency Checklist

Version: 1.0.0
Status: Text-only manual metadata review checklist
Use: Review .meta.json sidecars for consistency.

## Purpose

This checklist verifies that prompt metadata sidecars are complete,
consistent, project-agnostic, and aligned with their prompt files.

## Required Metadata Fields

For each .meta.json file, confirm:

- [ ] schema_version exists.
- [ ] prompt_id exists and is unique.
- [ ] display_name exists.
- [ ] version exists.
- [ ] status exists.
- [ ] category exists.
- [ ] subcategory exists or is intentionally blank.
- [ ] load_type exists.
- [ ] project_agnostic is true unless explicitly project-specific.
- [ ] safe_to_copy is true or the reason is documented.
- [ ] edit_policy exists.
- [ ] promotion_policy exists.
- [ ] governance_linked exists.
- [ ] modifies_governance exists.
- [ ] creates_files exists.
- [ ] required_placeholders exists.
- [ ] explainer exists.
- [ ] how_it_works exists.
- [ ] risks exists.
- [ ] mitigations exists.
- [ ] validation_requirements exists.
- [ ] change_log exists.

## Prompt-to-Metadata Alignment

- [ ] Metadata version matches prompt header version.
- [ ] Metadata display_name matches prompt purpose.
- [ ] Metadata category matches folder/category.
- [ ] Metadata files_created matches prompt file creation contract.
- [ ] Metadata required_placeholders are present or justified.
- [ ] Metadata risks have matching mitigations.
- [ ] Metadata safe_usage does not contradict prompt body.

## Project-Agnostic Metadata Checks

- [ ] default_output_folder uses <PROJECT_ROOT> or a relative package path.
- [ ] No absolute path appears outside examples.
- [ ] No single project name is required unless marked as example-only.
- [ ] Project-specific terms are documented as adaptation variables.

## Result

- [ ] PASS - Metadata is consistent.
- [ ] FAIL - Metadata needs correction.
- [ ] PARTIAL - Metadata is usable for reference only.

## Notes

<METADATA_REVIEW_NOTES>
