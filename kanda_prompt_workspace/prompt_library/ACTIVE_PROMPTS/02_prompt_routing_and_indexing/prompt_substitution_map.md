---
prompt_id: prompt_substitution_map
prompt_code: KPR-02-005
title: Prompt Substitution Map
version: 10.0
status: active
load_type: on_request
owner_box: 02_prompt_routing_and_indexing
source_stage: prompt-audit-wave3a-session-startup-kernel-v1
---

# Prompt Substitution Map

## Mission

Resolve a historical prompt name, filename, ID, or code to its current lifecycle state and canonical destination without reproducing destination behavior or authorizing source changes.

## Authority

The machine-readable identity-history authority is current canonical metadata plus reconciliation records. This prompt provides human-readable lookup behavior only.

## Record model

```text
LEGACY IDENTITY:
Old filename, ID, or code

LIFECYCLE STATE:
active_alias / deprecated_alias / historical_alias / merged / split_replacement / deleted / no_direct_replacement / unresolved_conflict

CURRENT DESTINATION:
Canonical prompt ID or ordered list of owners

CURRENT STATUS:
active / deprecated / deleted / unresolved

MAY LOAD LEGACY PROMPT:
YES / NO

MIGRATION EVIDENCE:
Current metadata, audit, reconciliation, or registration record
```

## Current Wave 2B lifecycle records

### prompt_router / kanda_prompt_router / KANDA_PROMPT_ROUTER

- Lifecycle state: `deprecated_alias`.
- Current destinations: `ai_prompt_request_canon`, `prompt_navigation_index`, `kanda_routing_system_canon`, and `prompt_substitution_map`.
- May load legacy prompt: `NO`, except direct historical inspection.
- Active route: `NO`.

### RG-PILOT-000

- Lifecycle state: `historical_alias` with retired active route.
- Current destinations: exact current P-series closure source, `routing_signal_scorer_v3_semantic_readiness_canon`, `kanda_routing_system_canon`, and Brick Wall when new work is proposed.
- May load legacy prompt: `NO`, except direct historical inspection.
- Active route: `NO`.

### RG-LAB-000

- Lifecycle state: `historical_alias` with retired active route.
- Current destinations: exact current LAB closure source, `routing_signal_scorer_v3_semantic_readiness_canon`, `kanda_routing_system_canon`, and Brick Wall when new work is proposed.
- May load legacy prompt: `NO`, except direct historical inspection.
- Active route: `NO`.


## Wave 3A Class 01 lifecycle records

### daily_reasoner_startup_loader

- Lifecycle: `deprecated_alias`.
- Current destinations: `start_of_day_master_stack` and `session_start_upload_checklist`.
- Active route: `NO`.

### daily_session_start_prompt

- Lifecycle: `deprecated_alias`.
- Current destination: `session_start_upload_checklist`.
- Active route: `NO`.

### general_prompt_stack_load_order

- Lifecycle: `deprecated_alias`.
- Current destinations: `start_of_day_master_stack`, `ai_prompt_request_canon`, and `prompt_navigation_index`.
- Active route: `NO`.

### reasoner_startup_canon

- Lifecycle: `deprecated_alias`.
- Current destinations: current startup, boundary, specialist, and Brick Wall owners.
- Active route: `NO`.

### 0000_2_1_daily_startup_loader_template

- Lifecycle: `migration_alias`.
- Current destination: `KPR-01-005 daily_startup_loader_template`.

### 0000_1_0_project_startup_canon_template

- Lifecycle: `migration_alias`.
- Current destination: `KPR-01-006 project_startup_canon_template`.



## Wave 4A Class 03 lifecycle records

### active_governance_freeze_update

- Lifecycle: `deleted_historical_alias`.
- Current destination: `KPR-03-003 freeze_code_intake_and_form_protocol`.
- Active route: `NO`.
- Missing retired files must not recreate the five-file governance bundle.

### current_workflow_handoff_template

- Lifecycle: `deleted_historical_alias`.
- Current destinations: `handoff_at_end_of_work` for normal KANDA closure and
  `KPR-03-006 workflow_handoff_template` for explicit generic draft authoring.
- Active route: `NO`.

### end_of_chat_governance_update_template / 0000_4_0_end_of_chat_governance_update_template

- Lifecycle: `deleted_historical_alias`.
- Current destination: `KPR-03-003 freeze_code_intake_and_form_protocol`.
- Active route: `NO`.

### reasoner_professional_engineering_governance / 0000_3_6_professional_engineering_governance_layer

- Lifecycle: `deleted_historical_alias`.
- Current destinations: Brick Wall, the exact specialist owners, and
  `KPR-03-002 cooperative_implementation_methodology` when option discussion is
  genuinely required.
- Active route: `NO`.

### 0000_6_0_workflow_handoff_template

- Lifecycle: `deleted_application_duplicate`.
- Current destination: `KPR-03-006 workflow_handoff_template` for draft-only
  generic authoring.
- Active route: `NO`.

## Lookup rules

1. inspect exact current metadata and reconciliation records;
2. follow substitution chains with a visited set;
3. reject loops and missing targets;
4. preserve split replacements as an explicit list;
5. never present a deprecated or deleted target as active;
6. distinguish a historical alias from an active alias;
7. return unresolved conflict when source and metadata disagree;
8. do not mutate references from this prompt.

## When to load

Load for old prompt names, rename history, deprecation lookup, reference migration planning, or questions about what replaced a prompt.

Do not load for normal current task routing, implementation, startup, patch delivery, or freeze.

## Mutation boundary

Actual migration uses Class 07 audit, reconciliation, identity, and insertion owners plus focused validation. This lookup cannot authorize or perform source changes.

## Version history

- 9.0: records Wave 8B Class 08 Python architecture, local readability, pattern-selection, and DDD owner boundaries plus historical alias reconciliation.
- 8.0: records Wave 8A reclassification of Peopleware and Practical Field Handbook from Class 08 to bounded Class 12 specialists.
- 7.0: records Wave 6C Web-AI planning, bundle, and target-specific AST-repair boundaries plus complete machine routing.
- 6.0: records Wave 6B Class 06 consolidation, three retirements, and KPR-06-004 scope reduction.
- 5.0: records Wave 5B Router bridge retirement, correction dispatch, terminal ownership, and universal-delivery retirement.
- 4.0: records Wave 5A Class 05 retirement, duplicate reconciliation, and current owner redirects.
- 3.0: records Wave 4A Class 03 retirement, draft-template consolidation, and current owner redirects.
- 2.1: records Wave 2B retirement and current destinations for prompt_router, RG-PILOT-000, and RG-LAB-000.
- 2.0: reframed as historical identity and lifecycle lookup with fail-closed chain resolution.


## Wave 4B Class 04 replacements

- `closed_box_delivery_canon` and `closed_box_delivery_canon.md` ->
  `KPR-04-001 box_architecture_canon`. The ingredient-box public-product law is
  now part of Box Architecture; actual patch delivery remains Class 05.
- `KPR-04-007`, `governed_architecture_companion_handoff`, and the former full
  architecture companion -> use the current canonical owner dispatch and select the smallest owner set:
  Brick Wall plus KPR-04-001, KPR-04-002, KPR-04-003, KPR-04-004, or KPR-04-006
  as applicable. The historical file is a deprecated redirect with no route.

## Wave 5A Class 05 lifecycle records

### evidence_freshness_gate / kanda_evidence_freshness_gate

- Lifecycle: `deleted_historical_ticket`.
- Current destinations: Project Symbol Atlas freshness for generated project
  evidence, JSON Splitter validation for split/reassemble integrity, Brick Wall
  Q14 for immediate pre-write freshness, and the exact artifact owner for patch,
  validation, Error Memory, or freeze evidence.
- Active route: `NO`.

### patch_registry_validation_freeze / kanda_patch_registry_validation_freeze

- Lifecycle: `deleted_historical_roadmap`.
- Current destinations: `KPR-05-002 bundle_gated_development_workflow` for
  release lifecycle, Brick Wall for current gate state, validation owners for
  evidence, handoff owners for continuity, and freeze owners for Preview and
  Confirm and Write.
- Active route: `NO`.

### kanda_bundle_gated_development_workflow / KANDA_BUNDLE_GATED_DEVELOPMENT_WORKFLOW.md

- Lifecycle: `deprecated_application_duplicate`.
- Current destination: `KPR-05-002 bundle_gated_development_workflow`.
- Active route: `NO`.

## Wave 5B Router and terminal compatibility records

### router_bridge_governed_implementation

- Lifecycle: `deprecated_historical_compatibility_tombstone`.
- Current destination: `brick_wall_comprehensive_quality_gate` plus only the
  task-specific current owners selected by routing.
- Active route: `NO`.

### router_bridge_patch_delivery_contract

- Lifecycle: `deprecated_historical_compatibility_tombstone`.
- Current destination: `pre_output_contract_gates`, current patch governance,
  and the exact receiver and terminal owners.
- Active route: `NO`.

### universal_delivery_protocol

- Lifecycle: `retired_active_kanda_authority`.
- Current KANDA destinations: `bundle_gated_development_workflow`,
  `implementation_and_delivery_protocol`, `pre_output_contract_gates`, and
  `terminal_cleanup_contract` as applicable.
- Generic residue: draft-only application template with no governance authority.
- Active route: `NO`.

## Wave 6B Class 06 consolidation and retirement records

### problem_set_roadmap_solver

- Lifecycle: `deleted_duplicate_roadmap`.
- Current destinations: `KPR-05-004 implementation_roadmap_builder` for an
  explicitly requested draft record and Brick Wall/current specialist owners
  for actual sequencing, dependencies, risk, validation, and authorization.
- Useful record already covered: owner, supporting owners, dependencies, risk,
  validation owner, rollback boundary, and relationship to other problems.
- Active route: `NO`.

### refactor_fragmentation_audit_runner

- Lifecycle: `deleted_historical_runner_roadmap`.
- Current destinations: `KPR-06-007 large_module_refactor_protocol`, current
  AST/static validators, architecture/boundary validators, public-contract and
  feature-specific validators, and runtime smoke owners as applicable.
- New universal fragmentation runner: `NOT JUSTIFIED` without a demonstrated
  uncovered failure.
- Active route: `NO`.

### tab1_tab2_audit_taxonomy

- Lifecycle: `deleted_historical_detector_taxonomy`.
- Current destinations: current Architecture Review and Workflow Review owners,
  `KPR-06-005 architecture_hardening_triage_protocol` for disposition and
  coverage-gap classification, and Brick Wall for implementation admission.
- New detector engines: `NOT JUSTIFIED` by the historical taxonomy alone.
- Active route: `NO`.

### safe_refactor_how_to / KPR-06-004

- Lifecycle: `active_reduced_dispatcher`.
- Current role: user-facing KANDA safe-refactor refresher, support-artifact
  interpreter, and bounded specialist dispatcher.
- Implementation, generic refactor law, delivery, evidence, terminal, and freeze
  authority remain with their current owners.

## Wave 6C Web-AI exchange boundary records

### KPR-06-001 web_ai_large_module_refactor_exchange_protocol

- Lifecycle: `active_bounded_planning_reasoner`.
- Owns: external review of an exact existing Planner plan and bounded action
  selection.
- Does not own: source implementation, bundle mechanics, terminal, validation
  infrastructure, evidence writes, or final freeze.

### KPR-06-002 web_ai_planning_response_bundle_blueprint

- Lifecycle: `active_bundle_profile`.
- Owns: exact Imported Web AI payload identity, bundle member profile, and Panel
  4 byte-identical fallback.
- Does not own: architecture reasoning or general package/freeze governance.

### KPR-06-003 web_ai_ast_split_risk_repair_protocol

- Lifecycle: `active_target_specific_ast_repair`.
- Owns: exact source repair from current target identity and AST evidence.
- Module size: obey current supplied workflow policy; absent one, use KPR-06-007
  400-line ideal and 500-line hard maximum with no universal minimum.
- Does not own: generic Planner reasoning, package mechanics, or final freeze.

## Wave 8A Class 08 to Class 12 reclassification records

### peopleware_team_boundary / KPR-12-007

- Lifecycle: `active_reclassified_human_process_specialist`.
- Current path: `ACTIVE_PROMPTS/12_generalized_project_canons/peopleware_team_boundary.md`.
- Old Class 08 path: retired after exact move.
- Owns: technical-versus-human-process classification and bounded,
  privacy-preserving software-team guidance.
- Does not own: medical diagnosis, personnel ranking, surveillance, technical
  implementation, validation evidence, terminal, Error Memory, or freeze.

### practical_field_handbook_template / KPR-12-008

- Lifecycle: `active_reclassified_source_grounded_template`.
- Current path: `ACTIVE_PROMPTS/12_generalized_project_canons/practical_field_handbook_template.md`.
- Old Class 08 path: retired after exact move.
- Owns: source access mode, edition identity, provenance, evidence limits,
  copyright-safe synthesis, and adaptive handbook structure.
- Does not own: invented source detail, substitute reproduction, source
  implementation, package delivery, validation claims, or freeze.

## Wave 8B Class 08 identity and boundary records

### clean_code_python

- Lifecycle: `historical_source_alias`.
- Current destination: `KPR-08-002 python_clean_code`.
- Active route: `NO`; use the canonical current ID or code.

### A023 / Domain-Driven Design Prompt for AI Code Generation

- Lifecycle: `historical_audit_identity`.
- Current destination: `KPR-08-004 python_domain_driven_design`.
- Active route: `NO`; use the canonical current ID or code.

### Broad historical Python-engineering aliases

Generic aliases such as `clean`, `code`, `design`, `software design`, and
`python engineering` do not directly select KPR-08-001 through KPR-08-004.
Resolve the demonstrated concern first and load only the smallest exact owner.

## Wave 8C Class 08 identity and alias records

### A022 / Working Effectively with Legacy Code Python Prompt

- Lifecycle: `historical_audit_identity`.
- Current destination: `KPR-08-007 python_legacy_code_workflow`.
- Active route: `NO`; use the current canonical ID or code.

### Broad enterprise, performance, and legacy aliases

Generic aliases such as `enterprise`, `performance`, `high`, `code`, `legacy`,
`workflow`, `software design`, and `python engineering` do not directly select
KPR-08-005 through KPR-08-007. Resolve whether the request is about enterprise
application patterns, measured performance, or legacy-code stabilization, then
load only the exact specialist.



## Wave 9A Python specialist identity records

- Historical `A024_PRAGMATIC_PROGRAMMER_PYTHON` routes only to `KPR-08-008`.
- Historical Master Reasoner Engineering bodies do not route; the surviving
  `software_engineering_books_master` identity is the thin `KPR-08-010` map.
- Short anti-hallucination prompts are derived profiles bound to KPR-09-003
  through KPR-09-006; they are not independent canonical owners.
- `tab4_docstring_quality_roadmap` is deprecated with no global active route.
- Broad aliases such as `code`, `quality`, `security`, `API`, `data`, `books`,
  or `engineering` do not directly select a Wave 9A specialist. Resolve the
  demonstrated concern and load the smallest exact owner.


## Wave 10A final closure identity records

- Historical `productization_readiness_roadmap` routes to no global active
  prompt; use current project capability evidence and exact active Class 11
  specialists.
- Historical `professional_infrastructure_roadmap` routes to no global active
  prompt; do not resurrect its missing-module list as source authority.
- Historical `professional_ai_assisted_engineering_framework` now resolves only
  to thin `KPR-11-003`, not to a master governance or implementation stack.
- Desktop help requests route to `KPR-12-010` only when the KANDA profile is
  explicitly adopted.
- Data lineage routes to `KPR-12-009`; transform selection resolution routes to
  `KPR-12-014`; do not merge the two owners.
- Shared visual semantics route to `KPR-12-013`; one physical renderer is not
  mandatory when backends preserve the same semantic contract.
