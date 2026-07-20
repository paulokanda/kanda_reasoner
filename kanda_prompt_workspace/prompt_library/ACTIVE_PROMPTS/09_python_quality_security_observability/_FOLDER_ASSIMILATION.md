---
folder_id: 09_python_quality_security_observability
folder_name: Python Quality, Security, and Observability
artifact_type: folder_assimilation_card
version: 3.0
status: active
scope: routing_metadata_only
load_mode: selected_when_needed
owner_box: 09_python_quality_security_observability
source_stage: prompt-audit-wave9a-python-specialist-stack-reconciliation-v1
updated_for: prompt-audit-wave9a-python-specialist-stack-reconciliation-v1
---

# Python Quality, Security, and Observability - Folder Assimilation Card

## Purpose

Route to the smallest applicable specialist in this folder. This card is
metadata only and does not copy specialist behavior or authorize source work.

## Load rule

Load this folder card only after the routing layer identifies a material concern
owned here. Do not load all specialists as a bundle.

## Current specialists

| Code | Prompt ID | Narrow owner |
|---|---|---|
| `KPR-09-001` | `anti_hallucination_full_group` | full evidence-verification train |
| `KPR-09-002` | `anti_hallucination_short_group` | compact evidence-verification train |
| `KPR-09-003` | `anti_hallucination_independent_ai_audit_full` | full adversarial audit |
| `KPR-09-004` | `anti_hallucination_web_evidence_audit_full` | current external evidence audit |
| `KPR-09-005` | `anti_hallucination_book_literature_audit_full` | verified literature audit |
| `KPR-09-006` | `anti_hallucination_master_protocol_full` | final evidence synthesis |
| `KPR-09-007` | `anti_hallucination_independent_ai_audit_short` | derived compact adversarial profile |
| `KPR-09-008` | `anti_hallucination_web_evidence_audit_short` | derived compact web profile |
| `KPR-09-009` | `anti_hallucination_book_literature_audit_short` | derived compact literature profile |
| `KPR-09-010` | `anti_hallucination_protocol_short` | derived compact synthesis profile |
| `KPR-09-011` | `python_documentation_developer_experience` | documentation and developer experience |
| `KPR-09-012` | `python_observability_logging_metrics_tracing` | logging, metrics, and tracing |
| `KPR-09-013` | `python_resilience_error_handling` | failure semantics and resilience |
| `KPR-09-014` | `python_security_threat_prevention` | security and threat prevention |
| `KPR-09-015` | `python_testing_pytest` | testing and pytest strategy |
| `KPR-09-016` | `python_validation_serialisation_type_safety` | boundary validation and serialization |

## Canonical identity records

- `KPR-09-001 anti_hallucination_full_group`
- `KPR-09-002 anti_hallucination_short_group`
- `KPR-09-003 anti_hallucination_independent_ai_audit_full`
- `KPR-09-004 anti_hallucination_web_evidence_audit_full`
- `KPR-09-005 anti_hallucination_book_literature_audit_full`
- `KPR-09-006 anti_hallucination_master_protocol_full`
- `KPR-09-007 anti_hallucination_independent_ai_audit_short`
- `KPR-09-008 anti_hallucination_web_evidence_audit_short`
- `KPR-09-009 anti_hallucination_book_literature_audit_short`
- `KPR-09-010 anti_hallucination_protocol_short`
- `KPR-09-011 python_documentation_developer_experience`
- `KPR-09-012 python_observability_logging_metrics_tracing`
- `KPR-09-013 python_resilience_error_handling`
- `KPR-09-014 python_security_threat_prevention`
- `KPR-09-015 python_testing_pytest`
- `KPR-09-016 python_validation_serialisation_type_safety`

## Boundaries

- Required companions are not forced by this card.
- Cross-domain concerns are dispatched to their exact current owners.
- Brick Wall and delivery owners retain implementation, validation, package,
  terminal, and freeze authority.
- `tab4_docstring_quality_roadmap` is a deprecated compatibility tombstone and
  is not an active Class 09 route.
