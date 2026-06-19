---
folder_id: 11_productization_and_release_readiness
folder_name: Productization and Release Readiness
artifact_type: folder_assimilation_card
version: 1.0
status: audited_candidate
scope: routing_metadata_only
load_mode: selected_when_needed
owner_box: Context Routing Layer
created_by_patch: kanda_context_routing_layer_phase2_folder_cards_v1
---

# Productization and Release Readiness - Folder Assimilation Card

## Purpose
This card is routing metadata. It helps the AI understand when this prompt folder should be requested.
It does not replace the prompts inside this folder and must not become a behavioral master prompt.

## Responsibility
Guide release maturity, lifecycle, versioning, deprecation, infrastructure, Kubernetes, SRE, and operational readiness.

## Use When
Use when moving from local tool to product, release, infrastructure, operations, deprecation, or production-readiness planning.

## Do Not Use When
Do not use for early small internal patching unless release readiness is directly affected.

## Required For
- release readiness
- versioning
- deprecation
- SRE
- infrastructure roadmap
- Kubernetes deployment

## Optional For
- future product strategy
- professionalization review

## Never Load For
- minor prompt index update
- simple source collector request

## Depends On Groups
- 05_patch_delivery_and_validation
- 09_python_quality_security_observability

## Common Task Triggers
- release
- production
- deprecation
- versioning
- SRE
- Kubernetes
- infrastructure

## Minimum Viable Context
- productization_readiness_roadmap or python_lifecycle_versioning_deprecation selected by task

## Main Prompts In This Folder

| Prompt ID | File Name | Load Type | Short Purpose |
|---|---|---|---|
| `kubernetes_deployment_operations` | `kubernetes_deployment_operations.md` | on_request | Uses Kubernetes deployment and operations concepts where appropriate. |
| `productization_readiness_roadmap` | `productization_readiness_roadmap.md` | on_request | Roadmap for turning the project into a release-ready product. |
| `professional_ai_assisted_engineering_framework` | `professional_ai_assisted_engineering_framework.md` | on_request | Defines the full professional AI-human engineering operating model. |
| `professional_infrastructure_roadmap` | `professional_infrastructure_roadmap.md` | on_request | Identifies missing infrastructure for professional AI-assisted engineering. |
| `python_lifecycle_versioning_deprecation` | `python_lifecycle_versioning_deprecation.md` | on_request | Manages Python lifecycle, release versioning, deprecation, and legacy transition. |
| `python_site_reliability_engineering` | `python_site_reliability_engineering.md` | on_request | Applies SRE principles to Python systems. |

## Routing Rule
Request this folder card only after `GROUP_ASSIMILATION_INDEX.md` selects this folder as required or useful for the task.
Do not load every folder card at session start.

## Boundary Rule
This card may point to prompt files, but it must not copy specialist rules from those prompt files.
If this card needs a new behavioral rule, create or update the correct specialist prompt instead.
