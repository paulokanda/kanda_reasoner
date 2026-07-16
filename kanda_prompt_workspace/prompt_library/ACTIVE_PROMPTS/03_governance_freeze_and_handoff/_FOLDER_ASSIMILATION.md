---
folder_id: 03_governance_freeze_and_handoff
folder_name: Governance, Freeze, and Handoff
artifact_type: folder_assimilation_card
version: 1.0
status: audited_candidate
scope: routing_metadata_only
load_mode: selected_when_needed
owner_box: Context Routing Layer
created_by_patch: kanda_context_routing_layer_phase2_folder_cards_v1
---

# Governance, Freeze, and Handoff - Folder Assimilation Card

## Purpose
Routing metadata for freeze decisions, governance updates, handoffs, state transfer, methodology, freeze-code intake/forms, and pre-output gates.

## Use When
Use when validation output must be classified, a step frozen, governance updated, a handoff made, or implementation methodology clarified.

## Do Not Use When
Do not use for brainstorming, unvalidated patch acceptance, or as a substitute for specialist prompts.

## Required For
- freeze review
- governance update
- session handoff
- validated state transfer
- consequential implementation methodology discussion
- freeze-code intake and freeze form correction
- output-time contract checks
- live Q01-Q40 implementation quality checkpoint

## Optional For
- roadmap closeout
- risk summary

## Depends On Groups
- 05_patch_delivery_and_validation

## Common Task Triggers
- freeze
- handoff
- end of chat
- update governance
- validated output
- implementation methodology
- KANDA_FREEZE_HINT.json
- New Local Freeze Entry
- freeze form
- freeze formulary
- pre-output contract gates
- terminal cleanup contract
- strict freeze JSON
- validation evidence marker
- brick wall
- Q01-Q40 checklist
- implementation status checkpoint

## Minimum Viable Context
- current_workflow_handoff_template
- active_governance_freeze_update

## Main Prompts In This Folder

| Prompt ID | File Name | Load Type | Short Purpose |
|---|---|---|---|
| `brick_wall_comprehensive_quality_gate` | `brick_wall_comprehensive_quality_gate.md` | routed | Displays and maintains the evidence-backed Q01-Q40 Brick Wall status for governed implementation work. |
| `active_governance_freeze_update` | `active_governance_freeze_update.md` | on_request | Freeze validated changes into active governance. |
| `current_workflow_handoff_template` | `current_workflow_handoff_template.md` | on_request | Current workflow handoff. |
| `end_of_chat_governance_update_template` | `end_of_chat_governance_update_template.md` | on_request | End-of-session governance update. |
| `professional_engineering_governance_template` | `professional_engineering_governance_template.md` | on_request | Generic engineering governance. |
| `reasoner_professional_engineering_governance` | `reasoner_professional_engineering_governance.md` | on_request | KANDA engineering governance. |
| `workflow_handoff_template` | `workflow_handoff_template.md` | on_request | Generic workflow handoff. |
| `cooperative_implementation_methodology` | `cooperative_implementation_methodology.md` | on_request | Proposal-before-code, escalation, and methodology discipline. |
| `freeze_code_intake_and_form_protocol` | `freeze_code_intake_and_form_protocol.md` | on_request | Carries feature-specific freeze data through patch ZIP sidecars and freeze form review. |
| `pre_output_contract_gates` | `pre_output_contract_gates.md` | on_request | Applies output-time contracts before terminal code, patch delivery, freeze JSON, evidence, sidecars, and multi-project paths. |

## Routing Rule
Request this folder card only after `GROUP_ASSIMILATION_INDEX.md` selects this folder as required or useful.
Do not load every folder card at session start.

## Boundary Rule
This card must not copy specialist rules. If behavior must change, update the correct specialist prompt.
