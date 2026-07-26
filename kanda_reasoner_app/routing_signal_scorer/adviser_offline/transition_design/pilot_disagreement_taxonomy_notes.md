# P3 - Pilot Disagreement Taxonomy Design v1

This file documents the design-only disagreement taxonomy added for P3.

P3 does not implement disagreement detection, route comparison, Pilot projection,
scoring, ranking, recommendation, prompt loading, persistence, training-data use,
batch mode, Limited Shadow Runtime, or runtime authority.

The taxonomy is descriptive only. Its purpose is to name how a future human review
record may describe differences after later governed milestones exist. It must
not be treated as approval, readiness, route selection, prompt selection, or
candidate promotion.

## Categories

- `no_observable_difference`
- `missing_or_insufficient_evidence`
- `task_classification_difference`
- `boundary_condition_difference`
- `supporting_material_hint_difference`
- `freeze_constraint_conflict`
- `safety_governance_boundary_conflict`
- `maturity_path_conflict`
- `authority_drift_attempt`
- `unresolved_ambiguity`

## Evidence rules

All evidence language remains caller-supplied, primitive, and non-authoritative.
P3 must not read project files, load prompts, call the live router, inspect gold
sets, mutate registries, call providers, use embeddings, or write review records.

## Match-before-disagree

No taxonomy label is trusted as a real disagreement until a later reproduction
harness proves the candidate can reproduce frozen router/canon outcomes on
governed cases. Until then, taxonomy labels are design vocabulary only.

## Fixed invariants

- `human_review_mandatory = True`
- `routing_effect = "none"`
- `prompt_loading_effect = "none"`
- `runtime_effect = "none"`
- `activation_effect = "none"`
- `storage_status = "in_memory_only"`
- `critical_boundary_error_budget = 0`

## Next milestone

After P3 validation, freeze, startup refresh, and `FREEZE_MEMORY_STATUS: OK`, the
next safe milestone is P4 - Pilot Gold/Frozen Router Reproduction Harness Design
v1.
