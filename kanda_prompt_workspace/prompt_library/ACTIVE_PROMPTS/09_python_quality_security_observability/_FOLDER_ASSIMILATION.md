---
folder_id: 09_python_quality_security_observability
folder_name: Python Quality, Security, and Observability
artifact_type: folder_assimilation_card
version: 1.0
status: audited_candidate
scope: routing_metadata_only
load_mode: selected_when_needed
owner_box: Context Routing Layer
created_by_patch: kanda_context_routing_layer_phase2_folder_cards_v1
---

# Python Quality, Security, and Observability - Folder Assimilation Card

## Purpose
This card is routing metadata. It helps the AI understand when this prompt folder should be requested.
It does not replace the prompts inside this folder and must not become a behavioral master prompt.

## Responsibility
Guide testing, documentation, resilience, logging, metrics, security, type safety, validation quality, and evidence-first anti-hallucination review.

## Use When
Use when a patch affects tests, docs, error handling, security, observability, serialization, or quality gates.

## Do Not Use When
Do not use as the primary owner for domain architecture or delivery mechanics.

## Required For
- testing strategy
- security-sensitive change
- logging/observability
- type safety
- docstring roadmap

## Optional For
- quality review
- maintainability review

## Never Load For
- pure routing metadata update unless quality gates are being designed

## Depends On Groups
- 05_patch_delivery_and_validation

## Common Task Triggers
- pytest
- security
- logging
- observability
- resilience
- docstrings
- validation
- anti hallucination
- evidence first coding
- verify AI code claims

## Minimum Viable Context
- python_testing_pytest or python_documentation_developer_experience selected by task

## Main Prompts In This Folder

| Prompt ID | File Name | Load Type | Short Purpose |
|---|---|---|---|
| `python_documentation_developer_experience` | `python_documentation_developer_experience.md` | on_request | Improves documentation, onboarding, and developer experience. |
| `python_observability_logging_metrics_tracing` | `python_observability_logging_metrics_tracing.md` | on_request | Designs logging, metrics, tracing, and observability for Python apps. |
| `python_resilience_error_handling` | `python_resilience_error_handling.md` | on_request | Designs resilient error handling, retries, and recovery behavior. |
| `python_security_threat_prevention` | `python_security_threat_prevention.md` | on_request | Checks Python code for security and threat-prevention concerns. |
| `python_testing_pytest` | `python_testing_pytest.md` | on_request | Designs and runs Python tests using pytest. |
| `python_validation_serialisation_type_safety` | `python_validation_serialisation_type_safety.md` | on_request | Improves validation, serialization, and typing safety in Python. |
| `tab4_docstring_quality_roadmap` | `tab4_docstring_quality_roadmap.md` | on_request | Improves docstring quality and Tab 4 documentation workflow. |
| `anti_hallucination_full_group` | `anti_hallucination_full_group.md` | routed | Routes high-risk work through the complete independent-audit, web-disconfirmation, literature, and master-protocol train. |
| `anti_hallucination_short_group` | `anti_hallucination_short_group.md` | routed | Routes routine governed work through the compact anti-hallucination train and escalates high-risk work to the full group. |
| `anti_hallucination_independent_ai_audit_full` | `anti_hallucination_independent_ai_audit_full.md` | on_request | Performs deep independent adversarial review and builds an assumption/claim ledger. |
| `anti_hallucination_web_evidence_audit_full` | `anti_hallucination_web_evidence_audit_full.md` | on_request | Performs current-source verification plus deliberate disconfirmation search. |
| `anti_hallucination_book_literature_audit_full` | `anti_hallucination_book_literature_audit_full.md` | on_request | Performs selective literature-level architecture audit only when justified. |
| `anti_hallucination_master_protocol_full` | `anti_hallucination_master_protocol_full.md` | on_request | Applies the complete evidence-first anti-hallucination engineering protocol. |
| `anti_hallucination_independent_ai_audit_short` | `anti_hallucination_independent_ai_audit_short.md` | on_request | Compact adversarial audit for routine governed work. |
| `anti_hallucination_web_evidence_audit_short` | `anti_hallucination_web_evidence_audit_short.md` | on_request | Compact evidence and disconfirmation audit. |
| `anti_hallucination_book_literature_audit_short` | `anti_hallucination_book_literature_audit_short.md` | on_request | Compact selective literature audit. |
| `anti_hallucination_protocol_short` | `anti_hallucination_protocol_short.md` | on_request | Compact evidence-first anti-hallucination engineering protocol. |

## Routing Rule
Request this folder card only after `GROUP_ASSIMILATION_INDEX.md` selects this folder as required or useful for the task.
Do not load every folder card at session start.

## Boundary Rule
This card may point to prompt files, but it must not copy specialist rules from those prompt files.
If this card needs a new behavioral rule, create or update the correct specialist prompt instead.
