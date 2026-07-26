# Transient Garbage Root Non-Ownership Reconciliation v1

Status: implemented reconciliation candidate
Scope: prompt-library terminology and ownership semantics for `*_delete_after_daily_work`
Owner canon: `project_tool_boundary_canon` (KPR-12-001)
Companion canon: `architecture_review_project_card_machine_canon` (KPR-12-005)

## Decision

`<project_drive>/<active_project_slug>_delete_after_daily_work` is canonically a transient garbage/staging root. It is neither Tool-owned nor Active-Project-owned. The project-derived name is only a deterministic namespace for collision avoidance and cleanup routing.

Anything stored there must be disposable or regenerable. Tool source, Active Project source, durable Workbench Preview state, canonical validation evidence, Error Memory, freeze intake, frozen memory, and other durable support state must never depend on that root for authority or survival.

## Prompt audit result

The prompt library was searched for `_delete_after_daily_work`, `daily-work`, and `active_project_daily_work_root` references. Operational staging instructions remain valid, but ownership language was reconciled so staging path derivation no longer implies project ownership.

Updated owner and routing surfaces:

- `ACTIVE_PROMPTS/12_generalized_project_canons/project_tool_boundary_canon.md`
- `ACTIVE_PROMPTS/12_generalized_project_canons/architecture_review_project_card_machine_canon.md`
- `ACTIVE_PROMPTS/02_prompt_routing_and_indexing/prompt_navigation_index.md`
- `ACTIVE_PROMPTS/02_prompt_routing_and_indexing/prompt_router.md`
- `ACTIVE_PROMPTS/02_prompt_routing_and_indexing/kanda_routing_system_canon.md`
- `ACTIVE_PROMPTS/05_patch_delivery_and_validation/router_bridge_governed_implementation.md`
- `ACTIVE_PROMPTS/05_patch_delivery_and_validation/patch_validate_freeze_error_memory_routine_blueprint.md`
- `ACTIVE_PROMPTS/01_session_start_and_navigation/start_of_day_master_stack.md`
- `ACTIVE_PROMPTS/01_session_start_and_navigation/daily_patch_delivery_guardrails.md`
- `ACTIVE_PROMPTS/04_box_architecture_and_boundaries/box_architecture_canon.md`
- `ACTIVE_PROMPTS/06_refactor_and_architecture_hardening/large_module_refactor_protocol.md`
- `ACTIVE_PROMPTS/06_refactor_and_architecture_hardening/large_module_refactor_template.md`
- `ACTIVE_PROMPTS/06_refactor_and_architecture_hardening/web_ai_large_module_refactor_exchange_protocol.md`
- associated metadata records for KPR-12-001, KPR-12-005, the governed implementation bridge, Large Module Refactor Protocol, and patch/freeze routine metadata.

## Preserved operational behavior

The reconciliation does not remove use of the folder for:

- patch ZIP staging;
- fresh extraction;
- temporary installer backups;
- temporary helpers;
- temporary validation assembly;
- disposable Shadow workspaces;
- regenerable diagnostics and one-use artifacts.

Durable audit reports, AI handoffs, validation evidence, Preview state, Error Memory, freeze intake, and frozen memory are explicitly routed to canonical `*_show_project_to_AI` support owners instead.

These uses remain transient and non-authoritative.

## Rejected interpretations

The following interpretations are forbidden:

```text
project-derived folder name -> project ownership
staged validation log -> canonical validation evidence
Shadow under garbage root -> durable Workbench state
temporary extracted patch -> Tool source truth
latest file in garbage root -> authoritative current project state
```

## Validation

`tools/validate_transient_garbage_root_prompt_canon_v1.py` checks:

- owner-canon non-ownership markers;
- required routing surfaces;
- absence of deprecated ownership terminology;
- metadata JSON validity;
- preservation of operational `_delete_after_daily_work` path usage;
- routing of durable audits, handoffs, and validation evidence to `*_show_project_to_AI` support ownership.
