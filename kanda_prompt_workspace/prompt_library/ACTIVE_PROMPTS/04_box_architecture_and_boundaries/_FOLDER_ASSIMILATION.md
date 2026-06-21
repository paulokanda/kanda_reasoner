---
folder_id: 04_box_architecture_and_boundaries
folder_name: Box Architecture and Boundaries
artifact_type: folder_assimilation_card
version: 1.0
status: audited_candidate
scope: routing_metadata_only
load_mode: selected_when_needed
owner_box: Context Routing Layer
created_by_patch: kanda_context_routing_layer_phase2_folder_cards_v1
---

# Box Architecture and Boundaries - Folder Assimilation Card

## Purpose
Routing metadata for selecting this prompt folder. It does not replace the prompts inside it.

## Responsibility
Define owner boxes, audits, public contracts, private internals, forbidden touches, dependencies, fallback behavior, anti-contamination rules, and KBSC shielding.

## Use When
Use before code, architecture, module splitting, cross-box wiring, GUI ownership changes, prompt-library updates, bundle creation, shielding, milestone hardening, stronger ML prep, or ownership-boundary changes.

## Do Not Use When
Do not use as a substitute for delivery scripts, validation scripts, or prompt audit decisions.

## Required For
- implementation patch
- architecture change
- cross-box touch
- module split
- new feature with ownership
- box shield after a meaningful milestone
- stronger ML or probabilistic routing preparation

## Optional For
- architecture explanation
- boundary teaching

## Never Load For
- pure text editing with no implementation consequence

## Depends On Groups
- 05_patch_delivery_and_validation

## Common Task Triggers
- owner box
- box boundary
- box boundary audit
- box architecture
- architecture
- dependencies
- public contract
- private internals
- private reach-in
- god box
- leaking registry
- one primary box

## Minimum Viable Context
- box_architecture_canon

## Main Prompts In This Folder

| Prompt ID | File Name | Load Type | Short Purpose |
|---|---|---|---|
| `box_architecture_canon` | `box_architecture_canon.md` | on_request | Defines Box Architecture, audits, ownership, allowed touches, contracts, internals, and cross-box validation. |
| `closed_box_delivery_canon` | `closed_box_delivery_canon.md` | on_request | Generalized closed-box delivery rules for safe project modifications. |
| `project_folder_organization_canon` | `project_folder_organization_canon.md` | on_request | Defines project folder boundaries and placement discipline. |
| `stateful_control_regression_canon` | `stateful_control_regression_canon.md` | on_request | Protects dropdowns and stateful controls from regression during UI changes. |
| `kanda_box_shielding_canon` | `kanda_box_shielding_canon.md` | on_request | Defines KBSC: tests-first box shielding as an architectural fitness-function suite for bounded contexts before stronger or cross-box work. |

## Routing Rule
Request this card only after `GROUP_ASSIMILATION_INDEX.md` selects this folder.

## Boundary Rule
This card may point to prompt files, but must not copy specialist rules from them.
