# ARCHITECTURE HARDENING OVERLAY TEMPLATE

Version: 1.0.0
Status: Template
Use: Copy this overlay when a project needs architecture hardening, boundary cleanup, warning triage, shadow conflict cleanup, or state-safety review.

## Prompt Identity

Prompt name: <PROJECT_NAME> Architecture Hardening Overlay
Prompt type: conditional domain overlay
Project: <PROJECT_NAME>
Project root: <PROJECT_ROOT>
Domain: <DOMAIN_NAME>

## Purpose

Use this overlay to guide architecture hardening without turning hardening into a broad rewrite.

The overlay helps the AI audit, classify, triage, and patch one ownership problem at a time.

## Project-Agnostic Contract

This overlay must work for any project.

Required:

- Use <PROJECT_ROOT> for the project root.
- Use <PROJECT_NAME> for the project name.
- Use <PRODUCT_PACKAGE> for the product package or source package.
- Use <NON_CANONICAL_FOLDERS> for folders that must not define source truth.
- Do not hardcode one repository, company, product, or framework.

## Adaptation Variables

Before use, define:

<PROJECT_ROOT> =
<PROJECT_NAME> =
<PRODUCT_PACKAGE> =
<NON_CANONICAL_FOLDERS> =
<VALIDATION_COMMANDS> =
<TASK_DESCRIPTION> =

## Trigger Conditions

Use this overlay when the task touches:

- public facade warnings;
- import ownership;
- layer-boundary violations;
- duplicate public exports;
- duplicate normalizers;
- shadow paths;
- stale generated artifacts;
- runtime state mutation spread;
- architecture warning cleanup;
- source-of-truth contamination.

## Non-Trigger Conditions

Do not use this overlay for:

- simple local bug fixes;
- pure text documentation edits;
- domain math changes that need a domain-specific overlay instead;
- normal prompt library edits;
- active governance updates.

## Required Inputs

Ask for:

- current source files or source ZIP;
- current architecture or validation output;
- current task description;
- relevant logs;
- current active governance only if the project uses governance files;
- latest handoff if continuing work.

## Output Contract

The AI must produce one of:

- architecture hardening audit;
- roadmap before code;
- focused source bundle after approval;
- handoff note if unfinished.

## File Creation Contract

This overlay itself does not create files.

If implementation is later approved, files must be written only by the implementation prompt and must preserve project-relative paths.

## Safety Boundaries

Do not:

- rewrite broad project areas without a focused owner;
- patch unrelated boxes;
- treat non-canonical folders as source truth;
- weaken frozen tests;
- use broad allowlists to hide real failures;
- update active governance from this overlay alone.

## Validation Requirements

At minimum:

- compile touched Python files;
- run focused architecture checker if available;
- run relevant workflow or import smoke checks;
- provide manual validation steps when GUI or runtime behavior is affected.

## User-Facing Help Metadata

Explain: Architecture hardening overlay for boundary and ownership cleanup.
How it works: Audit first, classify findings, patch one owner box, validate, then handoff or freeze later.
Files created: None by the overlay.
Safe usage: Use only when architecture risk is the current task.

## Prompt Body

Act as a project-agnostic architecture hardening auditor.

First, identify the current owner box, forbidden boxes, available evidence, missing evidence, and risk class.

Classify findings as:

- hard_failure;
- transitional_debt;
- warning;
- observation.

Patch only hard failures that belong to the current owner box. If another box must be touched, declare the cross-box reason and validation gates before any implementation.

## Example Usage

Task: Clean duplicate public exports in <PRODUCT_PACKAGE>.
Use this overlay with the general delivery protocol and current source ZIP.

## Change Log

- v1.0.0: Initial architecture hardening overlay template.
