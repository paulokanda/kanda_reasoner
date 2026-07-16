# FOLDER ASSIMILATION CARD

Folder: 01_session_start_and_navigation
Card type: routing metadata
Status: active metadata card

## Purpose

This folder contains the minimal session-entry prompts for starting work safely without loading the whole prompt library.

## Use when

Use this folder when the task involves:

- beginning a new working session;
- checking which prompts should be requested;
- deciding whether a task can use the fast path;
- separating simple explanation from implementation work;
- confirming the active navigation stack;
- routing durable generated documentation and validation evidence away from disposable daily-work storage.

## Main artifacts

- start_of_day_master_stack.md
- ai_prompt_request_canon.md
- prompt_router_reasoner_startup_check.md
- durable_document_artifact_routing_canon.md

## Routing role

This folder helps decide the first context boundary. It should keep session startup small and route outward only when a task requires more context. It also owns the Prompt Router Reasoner startup readiness checklist used in the beginning-of-day load check.

## Companion folders

Common companion folders:

- 02_prompt_routing_and_indexing for routing maps.
- 03_governance_freeze_and_handoff for freeze or handoff tasks.
- 04_box_architecture_and_boundaries for implementation or architecture tasks.
- 05_patch_delivery_and_validation for patch delivery.

## Not responsible for

This folder does not define Python implementation rules, patch validation rules, prompt audit rules, or live app integration behavior.

## Load rule

Load only when session startup, prompt-request discipline, or initial routing behavior is relevant.
