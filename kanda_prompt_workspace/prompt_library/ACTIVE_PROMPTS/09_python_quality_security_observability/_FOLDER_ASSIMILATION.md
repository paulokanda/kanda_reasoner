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
Guide testing, documentation, resilience, logging, metrics, security, type safety, and validation quality.

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

## Routing Rule
Request this folder card only after `GROUP_ASSIMILATION_INDEX.md` selects this folder as required or useful for the task.
Do not load every folder card at session start.

## Boundary Rule
This card may point to prompt files, but it must not copy specialist rules from those prompt files.
If this card needs a new behavioral rule, create or update the correct specialist prompt instead.
