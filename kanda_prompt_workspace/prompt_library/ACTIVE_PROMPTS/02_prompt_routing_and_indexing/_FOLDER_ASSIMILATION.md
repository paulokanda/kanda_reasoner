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
- KANDA_ROUTING_CHOICE manual capture blocks
- browser ChatGPT to local Prompt Router Reasoner round trip

## Minimum Viable Context
- prompt_navigation_index
- GROUP_ASSIMILATION_INDEX
- chatgpt_kanda_routing_choice_output_protocol when startup output must be machine-readable for Prompt Router Reasoner
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
| `chatgpt_kanda_routing_choice_output_protocol` | `chatgpt_kanda_routing_choice_output_protocol.md` | always_startup | Teaches browser ChatGPT to emit safe advisory KANDA_ROUTING_CHOICE blocks for manual Prompt Router Reasoner capture. |

## Routing Rule
Request this card only after `GROUP_ASSIMILATION_INDEX.md` selects this folder.

## Boundary Rule
This card may point to prompt files, but must not copy specialist rules from them.

<!-- KANDA_FOLDER_TRIGGER:error_memory_direct_error_lesson_zip:v1 -->

## Additional trigger: Direct Error Lesson ZIP route

Use this routing folder when deciding whether a user request is a normal patch ZIP delivery or a Direct Error Lesson ZIP for the Error Memory tab.

Signals:

```text
Error Lesson ZIP
formatted Error Memory lesson ZIP
direct import ZIP
new error and solution JSON
AI-assisted error lesson intake
Error Editor
Memorize Error
```

Routing boundary:

```text
Direct Error Lesson ZIP packages are not code patches. They are imported through the Error Memory tab and must use the canonical payload/error_memory_receive_blocks structure.
```

<!-- KANDA_FOLDER_TRIGGER:error_memory_default_autoload_insertion:v2 -->

## Error Memory default insertion autoload trigger

This routing folder recognizes Error Memory insertion requests and separates three modes:

```text
Mode 1 default: ZIP -> install -> validate -> populate AI-assisted error lesson intake and Error Editor.
Mode 2 explicit: Direct Error Lesson ZIP -> manual Import Error Lesson ZIP.
Mode 3 clipboard: Copy error/draft to AI -> Paste error formatted from AI.
```

Default trigger language includes:

```text
zip install validate error appear in AI assisted error lesson intake
send to EM tab
populate Error Memory tab automatically
zipped error install and validation code
```

The default mode must derive the dynamic project Error Memory folder from PROJECT_ROOT:

```text
<drive>:\<project>_show_project_to_AI\project_error_memory
```
