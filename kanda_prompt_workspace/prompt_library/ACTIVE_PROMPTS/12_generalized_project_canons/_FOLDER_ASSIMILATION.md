---
folder_id: 12_generalized_project_canons
folder_name: Generalized Project Canons
artifact_type: folder_assimilation_card
version: 1.0
status: audited_candidate
scope: routing_metadata_only
load_mode: selected_when_needed
owner_box: Context Routing Layer
created_by_patch: kanda_context_routing_layer_phase2_folder_cards_v1
---

# Generalized Project Canons - Folder Assimilation Card

## Purpose
Routing metadata for selecting this prompt folder. It does not replace the prompts inside it.

## Responsibility
Provide reusable canons for project/tool boundaries, plugins, visual rendering, desktop help layout, quick-start help blocks, transforms, data pipelines, and decision tables.

## Use When
Use when the project needs reusable architectural canons.

## Do Not Use When
Do not use as the session kernel or patch protocol.

## Required For
- plugin package import canon
- desktop help document layout
- help quick start
- non-technical help explanation
- book-grounded help references
- shared render engine
- transform resolver
- data pipeline invariant
- domain decision table
- project tool boundary
- active project identity
- selected project root
- architecture review card machine
- card lifecycle
- insert module to refactor
- eject module after completion

## Optional For
- new project canon creation
- cross-project reuse planning

## Never Load For
- routine freeze
- simple prompt audit without domain canon impact

## Depends On Groups
- 04_box_architecture_and_boundaries
- 08_python_engineering_core

## Common Task Triggers
- plugin
- desktop help
- help document layout
- help quick start
- non-technical help
- book-grounded help
- visual render
- transform resolver
- pipeline invariant
- decision table
- project versus tool
- project vs tool
- active project root
- target project

## Minimum Viable Context
- one selected generalized canon matching the task

## Main Prompts In This Folder

| Prompt ID | File Name | Load Type | Short Purpose |
|---|---|---|---|
| `architecture_review_project_card_machine_canon` | `architecture_review_project_card_machine_canon.md` | routed | Defines Architecture Review as a project-card machine lifecycle: insert project module, read/plan/refactor/verify, then eject target-specific Tool memory while retaining project-owned results. |
| `data_transform_pipeline_invariants` | `data_transform_pipeline_invariants.md` | on_request | Preserves source truth, canonical working base, and derived runtime output boundaries. |
| `desktop_help_document_layout_canon` | `desktop_help_document_layout_canon.md` | on_request | Defines desktop help layout, quick-start blocks, non-technical artifact explanation, book grounding, and help artwork rules. |
| `domain_decision_table_template` | `domain_decision_table_template.md` | on_request | Template for converting domain rules into explicit decision tables. |
| `plugin_package_import_canon` | `plugin_package_import_canon.md` | on_request | Defines safe import and validation rules for plugin packages. |
| `project_tool_boundary_canon` | `project_tool_boundary_canon.md` | always_startup | Mandatory Tool-versus-Project boundary; forbids any nested `*_show_project_to_AI` root inside active Project source. |
| `shared_visual_render_engine_canon` | `shared_visual_render_engine_canon.md` | on_request | Protects shared visual rendering contracts across tools. |
| `transform_resolver_architecture_contract` | `transform_resolver_architecture_contract.md` | on_request | Defines base identity plus active transform resolver behavior. |

## Routing Rule
Request this card only after `GROUP_ASSIMILATION_INDEX.md` selects this folder.

## Boundary Rule
This card may point to prompt files, but must not copy specialist rules from them.
