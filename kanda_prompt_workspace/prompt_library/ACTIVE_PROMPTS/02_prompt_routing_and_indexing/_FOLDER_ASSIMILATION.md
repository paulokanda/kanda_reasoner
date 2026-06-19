---
folder_id: 02_prompt_routing_and_indexing
folder_name: Prompt Routing and Indexing
artifact_type: folder_assimilation_card
version: 1.0
status: audited_candidate
scope: routing_metadata_only
load_mode: selected_when_needed
owner_box: Context Routing Layer
created_by_patch: kanda_context_routing_layer_phase2_folder_cards_v1
---

# Prompt Routing and Indexing - Folder Assimilation Card

## Purpose
This card is routing metadata. It helps the AI understand when this prompt folder should be requested.
It does not replace the prompts inside this folder and must not become a behavioral master prompt.

## Responsibility
Map task intent to required groups, optional groups, minimum viable context, specialist prompt requests, the KANDA Routing System Canon, the semantic-readiness canon for ML/embedding-related routing work, and the RG-PILOT-000 Pilot/Copilot Phase 0 router canon for post-M35 Pilot/Copilot scope work.

## Use When
Use when deciding what prompts or groups are needed for a task.

## Do Not Use When
Do not use as a behavioral prompt that teaches the full protocol of another group.

## Required For
- task routing
- prompt selection
- context routing
- missing prompt request
- routing-system canonization
- Context Package Manifest work
- Prompt Registration v2 work
- semantic-readiness / embedding-readiness canon work
- routing_signal_scorer v3 ML boundary work
- post-M35 Pilot/Copilot Phase 0 router canon work
- P0 scope charter routing
- Pilot/Copilot P-series milestone routing

## Optional For
- prompt-library explanation
- route review

## Never Load For
- direct implementation without owner-box audit
- replacing source evidence

## Depends On Groups
- 01_session_start_and_navigation

## Common Task Triggers
- route this
- what prompt
- which group
- find correct prompt
- context router
- semantic readiness canon
- embedding readiness
- routing_signal_scorer v3
- Metadata Vector Manifest
- RG-PILOT-000
- Pilot/Copilot Phase 0
- post-M35 continuation
- P0 scope charter

## Minimum Viable Context
- prompt_navigation_index
- GROUP_ASSIMILATION_INDEX
- kanda_routing_system_canon when routing-system behavior is affected
- routing_signal_scorer_v3_semantic_readiness_canon when ML/semantic retrieval is involved
- routing_signal_scorer_v3_pilot_copilot_phase0_router_canon when Pilot/Copilot, P0, P-series, post-M35 continuation, or runtime-authority risk is involved

## Main Prompts In This Folder

| Prompt ID | File Name | Load Type | Short Purpose |
|---|---|---|---|
| `kanda_routing_system_canon` | `kanda_routing_system_canon.md` | on_request | Defines the KANDA routing system canon: Prompt-Call Accuracy, Context Package Manifest, Prompt Registration v2, and shield-aware routing boundaries. |
| `routing_signal_scorer_v3_semantic_readiness_canon` | `routing_signal_scorer_v3_semantic_readiness_canon.md` | on_request | Defines semantic-readiness and embedding/ML adoption boundaries before routing_signal_scorer v3 implementation. |
| `project_overlay_selector` | `project_overlay_selector.md` | on_request | Selects and applies the correct project overlay without corrupting the base workflow. |
| `prompt_navigation_index` | `prompt_navigation_index.md` | routing_core | Intent-routing index that maps natural human requests to prompt IDs, load rules, exclusions, companions, and priority. |
| `prompt_router` | `prompt_router.md` | on_request | Routes messy human requests to prompt families and companion prompts. |
| `prompt_substitution_map` | `prompt_substitution_map.md` | on_request | Maps old, generic, or project-specific prompt concepts to current KANDA prompt concepts. |

## Routing Rule
Request this folder card only after `GROUP_ASSIMILATION_INDEX.md` selects this folder as required or useful for the task.
Do not load every folder card at session start.

## Boundary Rule
This card may point to prompt files, but it must not copy specialist rules from those prompt files.
If this card needs a new behavioral rule, create or update the correct specialist prompt instead.
