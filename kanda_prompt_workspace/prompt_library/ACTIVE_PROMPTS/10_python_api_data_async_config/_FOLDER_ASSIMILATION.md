---
folder_id: 10_python_api_data_async_config
folder_name: Python API, Data, Async, and Configuration
artifact_type: folder_assimilation_card
version: 3.0
status: active
scope: routing_metadata_only
load_mode: selected_when_needed
owner_box: 10_python_api_data_async_config
source_stage: prompt-audit-wave9a-python-specialist-stack-reconciliation-v1
updated_for: prompt-audit-wave9a-python-specialist-stack-reconciliation-v1
---

# Python API, Data, Async, and Configuration - Folder Assimilation Card

## Purpose

Route to the smallest applicable specialist in this folder. This card is
metadata only and does not copy specialist behavior or authorize source work.

## Load rule

Load this folder card only after the routing layer identifies a material concern
owned here. Do not load all specialists as a bundle.

## Current specialists

| Code | Prompt ID | Narrow owner |
|---|---|---|
| `KPR-10-001` | `python_api_design` | API and external interface contracts |
| `KPR-10-002` | `python_async_parallel_distributed` | concurrency and distributed execution |
| `KPR-10-003` | `python_configuration_feature_flags` | configuration and feature-flag lifecycle |
| `KPR-10-004` | `python_database_design_optimisation` | database design, queries, and migrations |

## Canonical identity records

- `KPR-10-001 python_api_design`
- `KPR-10-002 python_async_parallel_distributed`
- `KPR-10-003 python_configuration_feature_flags`
- `KPR-10-004 python_database_design_optimisation`

## Boundaries

- Required companions are not forced by this card.
- Cross-domain concerns are dispatched to their exact current owners.
- Brick Wall and delivery owners retain implementation, validation, package,
  terminal, and freeze authority.
- `tab4_docstring_quality_roadmap` is a deprecated compatibility tombstone and
  is not an active Class 09 route.
