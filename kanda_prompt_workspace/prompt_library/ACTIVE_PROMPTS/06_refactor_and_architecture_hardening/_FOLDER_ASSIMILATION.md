# FOLDER ASSIMILATION CARD

Folder: 06_refactor_and_architecture_hardening
Card type: routing metadata
Status: active metadata card

## Purpose

This folder groups prompts related to refactoring, decomposition, architecture hardening, dependency cleanup, and safer structural changes.

## Use when

Use this folder when the task involves:

- a module that became too large;
- reducing coupling;
- splitting responsibilities;
- improving boundaries without changing behavior;
- replacing fragile structure with a clearer design;
- preparing a safer refactor roadmap.

## Routing role

This folder helps distinguish structural improvement from feature implementation. It should usually pair with box architecture before any file change.

## Companion folders

Common companion folders:

- 04_box_architecture_and_boundaries for boundary ownership.
- 05_patch_delivery_and_validation for install and validation gates.
- 08_python_engineering_core when Python source code changes are needed.
- 09_python_quality_security_observability when risk, logging, or security checks matter.

## Not responsible for

This folder is not the owner of prompt audit, session startup, GUI wiring, or live app integration. It should not absorb delivery rules that belong in the patch delivery folder.

## Load rule

Load only when the user asks for refactor, architecture hardening, decomposition, or structural repair.

## Safe Refactor How To route

Use `safe_refactor_how_to` (`KPR-06-004`) when the AI needs the complete reusable safe-refactor process and delivery refresher, or when the user invokes the `Safe Refactor How To` button.

Do not use it as a substitute for current target-specific KPR-06-003 evidence. For an active RISK REFACTORING target, combine the reusable runbook with the exact current source, hash, AST audit, and fresh family audit authority.

The clipboard bundle may include the current canonical routine guide, current canonical routine implementation, and one explicitly non-authoritative worked report example.
