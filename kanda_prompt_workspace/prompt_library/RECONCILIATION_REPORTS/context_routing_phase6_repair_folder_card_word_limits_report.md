# PHASE 6 REPAIR REPORT - FOLDER CARD WORD LIMITS

Patch: kanda_context_routing_layer_phase6_repair_folder_card_word_limits_v1
Owner box: Folder Card Word Limit Repair Box
Status: pending local installation and validation

## Trigger

Phase 6 freeze validation failed because the validator reported three folder cards above the hard word limit:

- 01_session_start_and_navigation
- 06_refactor_and_architecture_hardening
- 08_python_engineering_core

## Repair

This patch replaces only those three folder assimilation cards with shorter metadata-only versions.

## What this patch changes

- ACTIVE_PROMPTS/01_session_start_and_navigation/_FOLDER_ASSIMILATION.md
- ACTIVE_PROMPTS/06_refactor_and_architecture_hardening/_FOLDER_ASSIMILATION.md
- ACTIVE_PROMPTS/08_python_engineering_core/_FOLDER_ASSIMILATION.md

## What this patch does not change

- No live app files.
- No Python validator file.
- No routing JSON files.
- No folder count.
- No prompt library GUI.
- No runtime code.

## Expected validator result

After this repair, the Phase 6 freeze validation should pass the folder card hard word limit gate.
