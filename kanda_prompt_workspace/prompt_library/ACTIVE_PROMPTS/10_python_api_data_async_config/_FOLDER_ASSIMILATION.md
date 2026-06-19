---
folder_id: 10_python_api_data_async_config
folder_name: Python API, Data, Async, and Config
artifact_type: folder_assimilation_card
version: 1.0
status: audited_candidate
scope: routing_metadata_only
load_mode: selected_when_needed
owner_box: Context Routing Layer
created_by_patch: kanda_context_routing_layer_phase2_folder_cards_v1
---

# Python API, Data, Async, and Config - Folder Assimilation Card

## Purpose
This card is routing metadata. It helps the AI understand when this prompt folder should be requested.
It does not replace the prompts inside this folder and must not become a behavioral master prompt.

## Responsibility
Guide API design, async/parallel architecture, database design, configuration, and feature-flag decisions.

## Use When
Use when the task touches APIs, data storage, async work, distributed work, configuration, or feature flags.

## Do Not Use When
Do not use for GUI-only layout changes or prompt-only audit work.

## Required For
- API design
- database design
- async architecture
- configuration system
- feature flags

## Optional For
- data model review
- backend architecture planning

## Never Load For
- read-only explanation of existing prompt routing

## Depends On Groups
- 08_python_engineering_core
- 09_python_quality_security_observability

## Common Task Triggers
- API
- database
- async
- parallel
- config
- feature flag

## Minimum Viable Context
- one selected specialist prompt matching the technical area

## Main Prompts In This Folder

| Prompt ID | File Name | Load Type | Short Purpose |
|---|---|---|---|
| `python_api_design` | `python_api_design.md` | on_request | Designs REST, GraphQL, and interface APIs for Python systems. |
| `python_async_parallel_distributed` | `python_async_parallel_distributed.md` | on_request | Guides async, parallel, and distributed Python design. |
| `python_configuration_feature_flags` | `python_configuration_feature_flags.md` | on_request | Designs configuration, settings, and feature-flag behavior. |
| `python_database_design_optimisation` | `python_database_design_optimisation.md` | on_request | Improves database design, query behavior, and data persistence. |

## Routing Rule
Request this folder card only after `GROUP_ASSIMILATION_INDEX.md` selects this folder as required or useful for the task.
Do not load every folder card at session start.

## Boundary Rule
This card may point to prompt files, but it must not copy specialist rules from those prompt files.
If this card needs a new behavioral rule, create or update the correct specialist prompt instead.
