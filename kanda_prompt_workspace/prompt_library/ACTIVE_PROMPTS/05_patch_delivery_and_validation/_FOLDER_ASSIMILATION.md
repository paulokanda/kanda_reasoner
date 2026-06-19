---
folder_id: 05_patch_delivery_and_validation
folder_name: Patch Delivery and Validation
artifact_type: folder_assimilation_card
version: 1.0
status: audited_candidate
scope: routing_metadata_only
load_mode: selected_when_needed
owner_box: Context Routing Layer
created_by_patch: kanda_context_routing_layer_phase2_folder_cards_v1
---

# Patch Delivery and Validation - Folder Assimilation Card

## Purpose
This card is routing metadata. It helps the AI understand when this prompt folder should be requested.
It does not replace the prompts inside this folder and must not become a behavioral master prompt.

## Responsibility
Define surgical patch delivery, install and validation scripts, evidence freshness, local validation, and freeze readiness gates.

## Use When
Use whenever a ZIP, install script, validation script, patch manifest, or validation classification is needed.

## Do Not Use When
Do not use to decide ownership boundaries without the Box Architecture group.

## Required For
- implementation bundle
- validation script
- install script
- patch delivery
- freeze evidence

## Optional For
- read-only patch planning
- delivery model explanation

## Never Load For
- prompt-library routing with no file placement

## Depends On Groups
- 04_box_architecture_and_boundaries

## Common Task Triggers
- zip
- install
- validation
- patch
- bundle
- expected output

## Minimum Viable Context
- implementation_and_delivery_protocol
- universal_delivery_protocol

## Main Prompts In This Folder

| Prompt ID | File Name | Load Type | Short Purpose |
|---|---|---|---|
| `bundle_gated_development_workflow` | `bundle_gated_development_workflow.md` | on_request | Requires focused installable bundles, backup, validation, and freeze discipline. |
| `evidence_freshness_gate` | `evidence_freshness_gate.md` | on_request | Checks whether evidence, generated artifacts, and validation inputs are fresh enough to trust. |
| `implementation_and_delivery_protocol` | `implementation_and_delivery_protocol.md` | on_request | Rules for building, packaging, and delivering code or prompt changes. |
| `implementation_roadmap_builder` | `implementation_roadmap_builder.md` | on_request | Builds a staged implementation roadmap before patch work. |
| `patch_registry_validation_freeze` | `patch_registry_validation_freeze.md` | on_request | Tracks patch provenance, validation status, and freeze readiness. |
| `universal_delivery_protocol` | `universal_delivery_protocol.md` | on_request | Defines consistent delivery style for code, prompts, reports, and install instructions. |

## Routing Rule
Request this folder card only after `GROUP_ASSIMILATION_INDEX.md` selects this folder as required or useful for the task.
Do not load every folder card at session start.

## Boundary Rule
This card may point to prompt files, but it must not copy specialist rules from those prompt files.
If this card needs a new behavioral rule, create or update the correct specialist prompt instead.
