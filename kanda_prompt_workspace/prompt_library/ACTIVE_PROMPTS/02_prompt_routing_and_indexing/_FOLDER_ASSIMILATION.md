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
Routing metadata for selecting this prompt folder. It does not replace the prompts inside it.

## Responsibility
Map task intent to prompt groups, minimum context, specialist prompts, routing-system rules, semantic-readiness rules, Pilot/Copilot routing, and LAB routing.

## Use When
Use when deciding what prompts or groups are needed for a task.

## Do Not Use When
Do not use as a behavioral prompt that teaches the full protocol of another group.

## Required For
- task, prompt, and context routing
- missing prompt request
- routing-system canonization
- Context Package Manifest and Prompt Registration v2 work
- semantic-readiness and embedding-readiness work
- routing_signal_scorer v3 ML boundary work
- Pilot/Copilot, RG-LAB-000, LAB-0, and ML router reliability routing

## Optional For
- route review

## Never Load For
- direct implementation

## Depends On Groups
- 01_session_start_and_navigation

## Common Task Triggers
- route this
- what prompt
- which group
- find correct prompt
- context router
- semantic readiness canon
- routing_signal_scorer v3
- RG-PILOT-000
- RG-LAB-000
- LAB-0
- router prompt logic reliability

## Minimum Viable Context
- prompt_navigation_index
- GROUP_ASSIMILATION_INDEX
- kanda_routing_system_canon when routing-system behavior is affected
- semantic, Pilot/Copilot, or LAB router canons when those scopes are involved

## Main Prompts In This Folder

| Prompt ID | File Name | Load Type | Short Purpose |
|---|---|---|---|
| `kanda_routing_system_canon` | `kanda_routing_system_canon.md` | on_request | Defines prompt-call accuracy, manifests, registration, and shield-aware routing. |
| `routing_signal_scorer_v3_lab_phase_entry_router_canon` | `routing_signal_scorer_v3_lab_phase_entry_router_canon.md` | on_request | Defines LAB entry and ML router reliability routing. |
| `routing_signal_scorer_v3_semantic_readiness_canon` | `routing_signal_scorer_v3_semantic_readiness_canon.md` | on_request | Defines semantic-readiness and embedding boundaries. |
| `project_overlay_selector` | `project_overlay_selector.md` | on_request | Applies the correct project overlay. |
| `prompt_navigation_index` | `prompt_navigation_index.md` | routing_core | Maps requests to prompt IDs, load rules, exclusions, companions, and priority. |
| `prompt_router` | `prompt_router.md` | on_request | Routes messy requests to prompt families and companions. |
| `prompt_substitution_map` | `prompt_substitution_map.md` | on_request | Maps old prompt concepts to current KANDA concepts. |

## Routing Rule
Request this card only after `GROUP_ASSIMILATION_INDEX.md` selects this folder.

## Boundary Rule
This card may point to prompt files, but must not copy specialist rules from them.
