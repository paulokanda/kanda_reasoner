# DOMAIN DECISION TABLE OVERLAY TEMPLATE

Version: 1.0.0
Status: Template
Use: Copy this overlay when a project has domain decisions that must be explicit, ordered, testable, and safe.

## Prompt Identity

Prompt name: <PROJECT_NAME> Domain Decision Table Overlay
Prompt type: conditional domain overlay
Project: <PROJECT_NAME>
Project root: <PROJECT_ROOT>
Domain: <DOMAIN_NAME>
Decision area: <DECISION_AREA>

## Purpose

Use this overlay to convert domain-specific logic into explicit decision tables.

This is useful when weak evidence, contradictions, manual overrides, or safety-sensitive classifications exist.

## Project-Agnostic Contract

This overlay must not assume a specific domain.

Use:

- <DOMAIN_NAME> for the clinical, financial, legal, scientific, operational, or product domain;
- <DECISION_AREA> for the decision being governed;
- <ALLOWED_OUTPUTS> for output states;
- <EVIDENCE_TYPES> for evidence categories.

## Adaptation Variables

<PROJECT_ROOT> =
<PROJECT_NAME> =
<DOMAIN_NAME> =
<DECISION_AREA> =
<ALLOWED_OUTPUTS> =
<EVIDENCE_TYPES> =
<TASK_DESCRIPTION> =
<VALIDATION_COMMANDS> =

## Trigger Conditions

Use this overlay when the task touches:

- domain classification;
- identity resolution;
- contradiction handling;
- manual override behavior;
- user-visible notices;
- safety-sensitive decision order;
- evidence confidence levels.

## Non-Trigger Conditions

Do not use this overlay for:

- simple UI layout fixes;
- pure packaging or delivery work;
- broad refactor without domain logic changes;
- active governance update alone.

## Required Inputs

Ask for:

- current domain rules;
- current source files that implement the decision;
- examples of valid and invalid inputs;
- known contradictions;
- expected user-visible consequences;
- validation tests or expected test cases.

## Output Contract

The AI must produce:

- ordered decision table;
- allowed outputs;
- evidence priority;
- confidence levels;
- contradiction behavior;
- manual override behavior if relevant;
- validation matrix.

## File Creation Contract

This overlay creates no files by itself.

## Safety Boundaries

Do not:

- upgrade weak evidence into settled truth;
- hide contradictions;
- let UI code invent domain truth;
- allow manual override to break structural integrity;
- change domain decisions without validation and explicit user approval.

## Validation Requirements

At minimum:

- compile touched files;
- focused tests for decision-table cases;
- contradiction test;
- manual override test when applicable;
- user-visible notice checklist when notices are involved.

## User-Facing Help Metadata

Explain: Domain decision-table overlay for ordered, explicit, safe decision logic.
How it works: Converts domain logic into ordered tables with allowed outputs, confidence, consequences, and tests.
Files created: None by this overlay.
Safe usage: Use for domain decisions, not generic refactors.

## Prompt Body

Act as a domain decision-table auditor.

First identify the allowed outputs, evidence hierarchy, confidence levels, contradiction states, and user-visible consequences.

Produce an ordered decision table before implementation. If the current source differs from the table, state whether source or documented rule has higher authority based on the project's governing hierarchy.

## Example Usage

Task: Define decision rules for <DECISION_AREA> in <DOMAIN_NAME>.
Use this overlay to create a table with priority, evidence, decision, confidence, and consequence columns.

## Change Log

- v1.0.0: Initial domain decision-table overlay template.
