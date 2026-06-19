---
folder_id: 07_prompt_authoring_and_audit
folder_name: Prompt Authoring and Audit
artifact_type: folder_assimilation_card
version: 1.0
status: audited_candidate
scope: routing_metadata_only
load_mode: selected_when_needed
owner_box: Context Routing Layer
created_by_patch: kanda_context_routing_layer_phase2_folder_cards_v1
---

# Prompt Authoring and Audit - Folder Assimilation Card

## Purpose
This card is routing metadata. It helps the AI understand when this prompt folder should be requested.
It does not replace the prompts inside this folder and must not become a behavioral master prompt.

## Responsibility
Audit, generalize, reconcile, split, deprecate, or improve prompt files without contaminating unrelated prompts.

## Use When
Use when reviewing prompt quality, creating prompt audit reports, extracting integration candidates, or reconciling prompt canons.

## Do Not Use When
Do not use to implement runtime code unless prompt-library files are being changed.

## Required For
- audit prompt
- compare prompts
- deprecate prompt
- generalize prompt
- integration candidate

## Optional For
- prompt writing advice
- library documentation

## Never Load For
- normal runtime bug fix
- GUI app patch without prompt changes

## Depends On Groups
- 02_prompt_routing_and_indexing

## Common Task Triggers
- audit this prompt
- compare prompts
- generalize
- deprecated prompt
- to be inserted

## Minimum Viable Context
- prompt_audit_canon
- prompt_canon_reconciliation_protocol

## Main Prompts In This Folder

| Prompt ID | File Name | Load Type | Short Purpose |
|---|---|---|---|
| `project_specific_prompt_generalization` | `project_specific_prompt_generalization.md` | on_request | Generalizes useful project-specific canons into reusable KANDA prompts. |
| `prompt_audit_canon` | `prompt_audit_canon.md` | on_request | Rules for auditing, updating, generalizing, and deprecating prompt files. |
| `prompt_canon_reconciliation_protocol` | `prompt_canon_reconciliation_protocol.md` | on_request | Reconciles overlapping prompt canons and updates the active prompt set. |

## Routing Rule
Request this folder card only after `GROUP_ASSIMILATION_INDEX.md` selects this folder as required or useful for the task.
Do not load every folder card at session start.

## Boundary Rule
This card may point to prompt files, but it must not copy specialist rules from those prompt files.
If this card needs a new behavioral rule, create or update the correct specialist prompt instead.

<!-- T9T013_KANDA_FOLDER_CARD_START -->

## T9T013 Complete Prompt Authoring Route

For requests such as:

```text
create a new prompt that...
update this prompt so...
make a prompt for...
register this prompt...
```

route to this folder and request the smallest useful set of specialist prompts:

```text
Required:
- prompt_canon_reconciliation_protocol
- prompt_audit_canon when duplicate/overlap detection is needed
- project_specific_prompt_generalization when importing ideas from another project

Required companion for installable bundles:
- bundle_gated_development_workflow
```

Dashboard or routing registration must not be assumed. Update group/routing files only when the user explicitly requests visibility/registration or when the prompt cannot be found without it.

<!-- T9T013_KANDA_FOLDER_CARD_END -->

