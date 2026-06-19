# KANDA Prompts — Clean Reconciled prompt_library v2

This folder is a clean replacement for `E:\kanda_reasoner\KANDA_PROMPTS_AUDITED\prompt_library`.

It promotes the reconciled active prompt set into intuitive filenames and 12 use-based groups.

## Counts

- Active prompts: 72
- Metadata files: 72
- Prompt groups: 12
- Deprecated/reference/audit artifacts promoted as active: 0
- Active alias map: none

## Main folders

```text
ACTIVE_PROMPTS/
  01_session_start_and_navigation/
  02_prompt_routing_and_indexing/
  03_governance_freeze_and_handoff/
  04_box_architecture_and_boundaries/
  05_patch_delivery_and_validation/
  06_refactor_and_architecture_hardening/
  07_prompt_authoring_and_audit/
  08_python_engineering_core/
  09_python_quality_security_observability/
  10_python_api_data_async_config/
  11_productization_and_release_readiness/
  12_generalized_project_canons/
METADATA/
GROUPS/
ROUTING/
RECONCILIATION_REPORTS/
```

## Principle

Old audit names are not kept as live aliases. Old names were mechanically rewritten to the clean names where they appeared in promoted active files.



## v3 Navigation Index Upgrade

This folder now includes a complete intent-routing navigation index. Each active prompt has:

- trigger phrases
- user intent examples
- aliases
- load rules
- exclusion rules
- required companion prompts
- priority for multi-match routing

Primary route files:

- `ROUTING/PROMPT_NAVIGATION_INDEX.md`
- `ROUTING/prompt_navigation_index.json`
- `ROUTING/prompt_route_coverage_table.csv`

## v4 Human ↔ AI Action Appendix

This folder now includes a human-facing operational appendix:

- `HUMAN_APPENDIX/KANDA_HUMAN_AI_PROJECT_ACTION_APPENDIX.md`

Purpose:

- show what the human can ask the AI to do in the project
- map common human phrases to the correct project action type
- remind when to provide Box Logic prompts/evidence
- define when the AI must ask for missing prompts or evidence instead of improvising

This appendix is not an active prompt and is not counted in the 72 active prompt files.
