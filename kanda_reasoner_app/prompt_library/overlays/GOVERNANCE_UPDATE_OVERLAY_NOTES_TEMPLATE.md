# GOVERNANCE UPDATE OVERLAY NOTES TEMPLATE

Version: 1.0.0
Status: Template
Use: Copy this overlay as read-only planning notes before deciding whether a project needs an official governance update.

## Prompt Identity

Prompt name: <PROJECT_NAME> Governance Update Overlay Notes
Prompt type: conditional planning overlay
Project: <PROJECT_NAME>
Project root: <PROJECT_ROOT>
Governance folder: <GOVERNANCE_FOLDER>

## Purpose

Use this overlay to decide whether a validated change should become official governance.

This overlay is not a governance update prompt. It does not create, modify, or freeze governance files.

## Project-Agnostic Contract

Use placeholders only:

- <PROJECT_ROOT>
- <PROJECT_NAME>
- <GOVERNANCE_FOLDER>
- <VALIDATED_GATE>
- <USER_APPROVAL_STATEMENT>

## Adaptation Variables

<PROJECT_ROOT> =
<PROJECT_NAME> =
<GOVERNANCE_FOLDER> =
<VALIDATED_GATE> =
<USER_APPROVAL_STATEMENT> =
<TASK_DESCRIPTION> =


## Bundle-Gated Readiness Check

Use this overlay to decide whether a completed bundle-gated cycle is ready for
official governance.

Check:

```text
bundle installed locally:
focused validation passed:
architecture validation passed:
workflow validation passed:
manual validation passed:
user approval statement:
```

If any item is missing, recommend a handoff instead of a governance update.

## Trigger Conditions

Use this overlay when:

- a validated result may need to become a do-not-regress rule;
- a project needs to decide between handoff and governance update;
- the user asks whether a freeze/canon update is appropriate.

## Non-Trigger Conditions

Do not use this overlay to:

- modify governance files;
- generate governance ZIPs;
- update accepted-warning baselines;
- canonize proposals;
- replace the official governance update protocol.

## Required Inputs

Ask for:

- validation output;
- user approval statement if any;
- baseline governance files if an actual governance update is later requested;
- current handoff if relevant.

## Output Contract

The AI must produce one of:

- governance update not required;
- handoff recommended;
- official governance update may be appropriate, request official governance protocol.

## File Creation Contract

This overlay creates no files.

## Safety Boundaries

Do not:

- write active governance;
- change canon version;
- modify accepted warning baseline;
- claim validation that was not shown;
- freeze proposals or unvalidated work.

## Validation Requirements

No code validation applies because this is text-only planning.

If a real governance update is later approved, use the official governance update protocol and validate its checker and tests.

## User-Facing Help Metadata

Explain: Read-only planning overlay for deciding whether governance update is appropriate.
How it works: Separates validated freezes from proposals and points to the official governance protocol when needed.
Files created: None.
Safe usage: Use only to decide whether to run the official governance update flow.

## Prompt Body

Act as a governance-readiness auditor.

List the validated gates, user approval evidence, affected boxes, and what remains not frozen. If evidence is incomplete, state that governance update is not ready and recommend a handoff.

Do not generate governance files from this overlay.

## Example Usage

Task: Decide whether <VALIDATED_GATE> should be frozen into <GOVERNANCE_FOLDER>.

## Change Log

- v1.0.0: Initial governance update overlay notes template.
