# Folder Assimilation Cards Index

Status: audited_candidate
Purpose: list the selected-when-needed folder assimilation cards created by Phase 2.

## Routing-index escalation discipline

Use this file only after `GROUP_ASSIMILATION_INDEX.md` has identified the broad group or groups.

1. Do not load every `_FOLDER_ASSIMILATION.md` card at startup.
2. Load a folder card only when the group is relevant and the task needs folder-level boundaries, prompt placement, or group-specific routing details.
3. If the exact specialist prompt or prompt ID is still unclear after the folder card, escalate to `prompt_navigation_index.md`.
4. If this file conflicts with `GROUP_ASSIMILATION_INDEX.md`, stop and flag `ROUTING_INDEX_CONFLICT` for human review.
5. If a simple Fast Path answer does not need folder-level context, do not request a folder card.

| Folder | Card Path | Responsibility | Prompt Count |
|---|---|---|---|
| `01_session_start_and_navigation` | `ACTIVE_PROMPTS/01_session_start_and_navigation/_FOLDER_ASSIMILATION.md` | Start the work session, establish minimum context, and control when the AI must request more prompts before acting. | 9 |
| `02_prompt_routing_and_indexing` | `ACTIVE_PROMPTS/02_prompt_routing_and_indexing/_FOLDER_ASSIMILATION.md` | Map task intent to required groups, optional groups, minimum viable context, specialist prompt requests, routing-system canon context, semantic-readiness canon context, RG-PILOT-000 Pilot/Copilot Phase 0 router canon context, and RG-LAB-000 post-P12 LAB phase entry router canon context. | 8 |
| `03_governance_freeze_and_handoff` | `ACTIVE_PROMPTS/03_governance_freeze_and_handoff/_FOLDER_ASSIMILATION.md` | Control validated freeze decisions, governance updates, end-of-chat state transfer, handoff creation, cooperative implementation methodology, freeze-code intake/form review, and pre-output contract gates. | 9 |
| `04_box_architecture_and_boundaries` | `ACTIVE_PROMPTS/04_box_architecture_and_boundaries/_FOLDER_ASSIMILATION.md` | Define owner boxes, public contracts, forbidden touches, dependency boundaries, anti-contamination rules, and KBSC box shielding. | 5 |
| `05_patch_delivery_and_validation` | `ACTIVE_PROMPTS/05_patch_delivery_and_validation/_FOLDER_ASSIMILATION.md` | Define surgical patch delivery, install and validation scripts, evidence freshness, local validation, and freeze readiness gates. | 6 |
| `06_refactor_and_architecture_hardening` | `ACTIVE_PROMPTS/06_refactor_and_architecture_hardening/_FOLDER_ASSIMILATION.md` | Plan and control large-module refactors, architecture hardening, fragmentation audits, and problem-set solving order. | 7 |
| `07_prompt_authoring_and_audit` | `ACTIVE_PROMPTS/07_prompt_authoring_and_audit/_FOLDER_ASSIMILATION.md` | Audit, generalize, reconcile, split, deprecate, or improve prompt files without contaminating unrelated prompts. | 3 |
| `08_python_engineering_core` | `ACTIVE_PROMPTS/08_python_engineering_core/_FOLDER_ASSIMILATION.md` | Provide broad Python engineering judgment for clean architecture, refactoring, DDD, performance, patterns, legacy code, and professional practice. | 12 |
| `09_python_quality_security_observability` | `ACTIVE_PROMPTS/09_python_quality_security_observability/_FOLDER_ASSIMILATION.md` | Guide testing, documentation, resilience, logging, metrics, security, type safety, and validation quality. | 7 |
| `10_python_api_data_async_config` | `ACTIVE_PROMPTS/10_python_api_data_async_config/_FOLDER_ASSIMILATION.md` | Guide API design, async/parallel architecture, database design, configuration, and feature-flag decisions. | 4 |
| `11_productization_and_release_readiness` | `ACTIVE_PROMPTS/11_productization_and_release_readiness/_FOLDER_ASSIMILATION.md` | Guide release maturity, lifecycle, versioning, deprecation, infrastructure, Kubernetes, SRE, and operational readiness. | 6 |
| `12_generalized_project_canons` | `ACTIVE_PROMPTS/12_generalized_project_canons/_FOLDER_ASSIMILATION.md` | Provide reusable domain-specific canons for plugins, visual rendering, desktop help-document layout, practical quick-start help blocks, transform resolvers, data pipelines, and decision tables. | 6 |



Selected exact prompt addition for `04_box_architecture_and_boundaries`:

```text
kanda_box_shielding_canon -> ACTIVE_PROMPTS/04_box_architecture_and_boundaries/kanda_box_shielding_canon.md
Use for KBSC, box shielding, meaningful milestone protection, and stronger ML preparation.
```

These cards are routing metadata only. They must not become behavioral prompts or replace specialist prompt files.


## RG-LAB-000 Post-P12 ML LAB Phase Entry Routing Hint

routing_signal_scorer_v3_lab_phase_entry_router_canon -> ACTIVE_PROMPTS/02_prompt_routing_and_indexing/routing_signal_scorer_v3_lab_phase_entry_router_canon.md
Use for post-P12 LAB phase entry, LAB-0, ML lab/test, ML router prompt logic reliability testing, and continuation of ML implementation after LAB reliability. After P12, canonize LAB entry first; LAB-0 is the first allowed milestone and is documentation-only.

## Routing System Canon Routing Hint

kanda_routing_system_canon -> ACTIVE_PROMPTS/02_prompt_routing_and_indexing/kanda_routing_system_canon.md
Use for routing-system canonization, Prompt-Call Accuracy, Context Package Manifest, Prompt Registration v2, and prompt-registration/not-global-insertion rules.


## RG-PILOT-000 Pilot/Copilot Phase 0 Routing Hint

routing_signal_scorer_v3_pilot_copilot_phase0_router_canon -> ACTIVE_PROMPTS/02_prompt_routing_and_indexing/routing_signal_scorer_v3_pilot_copilot_phase0_router_canon.md
Use for post-M35 Pilot/Copilot Phase 0, P0, P-series, Pilot projection/simulation, Pilot implementation gates, reproduction-before-disagreement, and Copilot boundary routing. If P0 is not frozen, P0 is the only safe implementation milestone.
