---
folder_id: 08_python_engineering_core
folder_name: Python Engineering Core
artifact_type: folder_assimilation_card
version: 3.0
status: active
scope: routing_metadata_only
load_mode: selected_when_needed
owner_box: 08_python_engineering_core
source_stage: prompt-audit-wave9a-python-specialist-stack-reconciliation-v1
updated_for: prompt-audit-wave9a-python-specialist-stack-reconciliation-v1
---

# Python Engineering Core - Folder Assimilation Card

## Purpose

Route to the smallest applicable specialist in this folder. This card is
metadata only and does not copy specialist behavior or authorize source work.

## Load rule

Load this folder card only after the routing layer identifies a material concern
owned here. Do not load all specialists as a bundle.

## Current specialists

| Code | Prompt ID | Narrow owner |
|---|---|---|
| `KPR-08-001` | `python_clean_architecture` | dependency direction and ports/adapters |
| `KPR-08-002` | `python_clean_code` | local readability and cohesion |
| `KPR-08-003` | `python_design_patterns` | evidence-based pattern selection |
| `KPR-08-004` | `python_domain_driven_design` | domain modeling and bounded contexts |
| `KPR-08-005` | `python_enterprise_architecture` | enterprise application patterns and transactions |
| `KPR-08-006` | `python_high_performance` | performance evidence and optimization |
| `KPR-08-007` | `python_legacy_code_workflow` | legacy stabilization and characterization |
| `KPR-08-008` | `python_pragmatic_programmer` | pragmatic trade-offs and reversibility |
| `KPR-08-009` | `python_refactoring` | bounded behavior-preserving refactoring |
| `KPR-08-010` | `software_engineering_books_master` | non-authoritative books synthesis and dispatch |

## Canonical identity records

- `KPR-08-001 python_clean_architecture`
- `KPR-08-002 python_clean_code`
- `KPR-08-003 python_design_patterns`
- `KPR-08-004 python_domain_driven_design`
- `KPR-08-005 python_enterprise_architecture`
- `KPR-08-006 python_high_performance`
- `KPR-08-007 python_legacy_code_workflow`
- `KPR-08-008 python_pragmatic_programmer`
- `KPR-08-009 python_refactoring`
- `KPR-08-010 software_engineering_books_master`

## Boundaries

- Required companions are not forced by this card.
- Cross-domain concerns are dispatched to their exact current owners.
- Brick Wall and delivery owners retain implementation, validation, package,
  terminal, and freeze authority.
- `tab4_docstring_quality_roadmap` is a deprecated compatibility tombstone and
  is not an active Class 09 route.
