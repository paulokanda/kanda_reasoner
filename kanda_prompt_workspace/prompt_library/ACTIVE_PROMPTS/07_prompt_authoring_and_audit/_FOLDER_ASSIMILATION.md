---
folder_id: 07_prompt_authoring_and_audit
folder_name: Prompt Authoring and Audit
artifact_type: folder_assimilation_card
version: 2.0
status: active
scope: routing_metadata_only
load_mode: selected_when_needed
owner_box: Context Routing Layer
---

# Prompt Authoring and Audit - Folder Assimilation Card

## Purpose

Route prompt-library audit, generalization, reconciliation, identity, and authorized mutation work to one canonical Class 07 owner per stage.

This card contains routing metadata only. It does not replace the specialist prompts.

## Stage owners

| Stage | Canonical prompt | Load type | Authority |
|---|---|---|---|
| Read-only target audit | `prompt_audit_canon` | on_request | Evidence and recommendation only |
| External-project generalization | `project_specific_prompt_generalization` | on_request | Analysis and recommendation only |
| Canonical lifecycle decision | `prompt_canon_reconciliation_protocol` | on_request | Decision and migration design only |
| Identity and KPR code | `KPR-07-002 prompt_identity_code_registry_canon` | routed | Identity decision only |
| Authorized mutation and registration | `KPR-07-001 prompt_insertion_and_router_registration_protocol` | routed | File mutation only after Brick Wall authorization |

## Required routing rules

- Inspect existing Prompt Library assets before creating a new prompt.
- Decide create, update, link/register, consolidate, overlay, deprecate, delete-after-migration, reference, reject, or block before mutation.
- Use `project_specific_prompt_generalization` only when external-project or domain-specific material is being adapted.
- Use the identity canon only when identity, code, alias, rename, move, split, merge, replacement, or retirement is involved.
- Load `bundle_gated_development_workflow` only when an installable bundle is actually being created.
- Update routing or startup assets only when the approved mutation requires them.

## Minimum viable context

For a read-only audit:

- `prompt_audit_canon`
- exact target source and metadata
- related current owners

For a governed mutation:

- this folder card
- `prompt_audit_canon`
- `prompt_canon_reconciliation_protocol`
- `prompt_identity_code_registry_canon` when identity changes
- `project_specific_prompt_generalization` when importing external material
- `prompt_insertion_and_router_registration_protocol`
- exact current source, metadata, indexes, validators, Error Memory, and Brick Wall authorization

## Boundary rule

Class 07 does not own routing architecture, startup generation, patch delivery, terminal behavior, or freeze transactions. It dispatches those responsibilities to their current canonical owners.
