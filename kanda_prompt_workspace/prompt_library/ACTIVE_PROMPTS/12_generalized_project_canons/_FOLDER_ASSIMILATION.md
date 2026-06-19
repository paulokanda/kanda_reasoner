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
This card is routing metadata. It helps the AI understand when this prompt folder should be requested.
It does not replace the prompts inside this folder and must not become a behavioral master prompt.

## Responsibility
Provide reusable domain-specific canons for plugins, visual rendering, desktop help-document layout, transform resolvers, data pipelines, and decision tables.

## Use When
Use when the project needs reusable architectural canons that are not Reasoner-specific.

## Do Not Use When
Do not use as the initial session kernel or as a generic patch protocol.

## Required For
- plugin package import canon
- desktop help document layout
- shared render engine
- transform resolver
- data pipeline invariant
- domain decision table

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
- visual render
- transform resolver
- pipeline invariant
- decision table

## Minimum Viable Context
- one selected generalized canon matching the task

## Main Prompts In This Folder

| Prompt ID | File Name | Load Type | Short Purpose |
|---|---|---|---|
| `data_transform_pipeline_invariants` | `data_transform_pipeline_invariants.md` | on_request | Preserves source truth, canonical working base, and derived runtime output boundaries. |
| `desktop_help_document_layout_canon` | `desktop_help_document_layout_canon.md` | on_request | Defines local desktop help layout, offline HTML/CSS rendering, and characterful help artwork rules. |
| `domain_decision_table_template` | `domain_decision_table_template.md` | on_request | Template for converting domain rules into explicit decision tables. |
| `plugin_package_import_canon` | `plugin_package_import_canon.md` | on_request | Defines safe import and validation rules for plugin packages. |
| `shared_visual_render_engine_canon` | `shared_visual_render_engine_canon.md` | on_request | Protects shared visual rendering contracts across tools. |
| `transform_resolver_architecture_contract` | `transform_resolver_architecture_contract.md` | on_request | Defines base identity plus active transform resolver behavior. |

## Routing Rule
Request this folder card only after `GROUP_ASSIMILATION_INDEX.md` selects this folder as required or useful for the task.
Do not load every folder card at session start.

## Boundary Rule
This card may point to prompt files, but it must not copy specialist rules from those prompt files.
If this card needs a new behavioral rule, create or update the correct specialist prompt instead.
