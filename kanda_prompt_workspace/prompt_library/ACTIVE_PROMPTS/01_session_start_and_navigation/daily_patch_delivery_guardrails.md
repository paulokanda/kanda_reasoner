---
prompt_id: daily_patch_delivery_guardrails
prompt_code: KPR-01-007
title: Daily Patch Delivery Guardrails
version: 3.2
status: active
load_type: always_startup
owner_box: 01_session_start_and_navigation
source_stage: prompt-audit-wave3b-specialist-startup-bridges-v1
---

# Daily Patch Delivery Guardrails

## Purpose

This is the compact always-startup bridge for governed patch delivery. It keeps
high-risk release invariants visible before any ZIP link, PowerShell block,
validation command, freeze instruction, or Error Memory delivery is shown.

Detailed implementation belongs to the current Class 05 delivery owners. This
prompt routes to those owners and must not become a second installer, validator,
freeze protocol, terminal contract, or Error Memory schema.

## Activation

Apply this bridge whenever the response may contain any of the following:

- a patch or bundle ZIP;
- install, validation, recovery, diagnostic, or freeze PowerShell;
- patch manifests, payload lists, or source fingerprints;
- validation evidence intended for durable storage or freeze;
- a correction caused by an install, validation, packaging, or delivery error.

For explanation-only discussion with no deliverable, use the smallest relevant
owner and do not invent release evidence.

## Required owner route

Before patch-related output, load or apply the current owners needed by the
specific task:

- `pre_output_contract_gates` for the visible output gate;
- `terminal_cleanup_contract` for terminal footer behavior;
- `implementation_and_delivery_protocol` for patch construction;
- `pre_output_contract_gates` for same-response delivery duties;
- `patch_install_delivery_error_register` for active regression classes;
- `freeze_code_intake_and_form_protocol` for freeze intake and human confirmation;
- `error_memory_ai_formulary_startup_canon` when a corrected error has durable
  prevention value;
- `durable_document_artifact_routing_canon` for durable documentary evidence;
- Brick Wall and the active Box owner for authorization and scope.

## Hard invariants

1. A patch is a governed release event, not an isolated ZIP attachment.
2. Exact current source and source fingerprints are required before mutation.
3. Unknown source states, unknown hashes, or ambiguous ownership fail closed.
4. Generated startup ZIPs, extracted bundles, and validation outputs are not
   canonical source authority.
5. Every externally delivered transient work artifact first arrives at the
   root of the active Project's drive. That drive-root copy is an inbox source,
   not the working copy.
6. Before use, derive the current Project drive, Project name, and transient
   root from the active Project root; copy the artifact into
   `<project>_delete_after_daily_work`, verify exact SHA-256 equality, and only
   then remove the drive-root source. Work proceeds from the verified staged
   copy. Everything remaining under `_delete_after_daily_work` is disposable at
   end of work/day, so durable evidence must be promoted first.
7. Durable evidence is routed by `durable_document_artifact_routing_canon`.
8. Installation, validation, and freeze are separate authorization states.
9. Validation success must be supported by local evidence; terminal text alone
   does not authorize freeze.
10. Freeze Preview remains read-only. Confirm and Write remains explicitly
    human-confirmed.
11. A corrected delivery error triggers Error Memory admission review, but this
    prompt does not create or define lesson schemas.
12. User-facing PowerShell must obey the current terminal and project delivery
    contracts. Do not duplicate those implementations here.

## Patch delivery readiness record

Before showing a patch artifact, determine:

```text
PATCH DELIVERY READINESS
Active Project:
Primary owner box:
Exact source inspected: YES / NO
Current source fingerprints recorded: YES / NO
Relevant Error Memory checked: YES / NO
Required delivery owners loaded: YES / NO
Patch ZIP validated: YES / NO / NOT_BUILT
Install block ready: YES / NO / NOT_APPLICABLE
Validation block ready: YES / NO / NOT_APPLICABLE
Durable evidence path identified: YES / NO
Freeze path identified: YES / NO / NOT_APPLICABLE
Human confirmation still required: YES
May release: YES / NO
Blocking reason:
```

If any required field is unresolved, do not show a ZIP link or claim readiness.

## Root and artifact summary

The stable summary is:

```text
<drive>:\ARTIFACT_NAME
    -> initial transient inbox only; do not use as the working copy
<drive>:\<project>_delete_after_daily_work\ARTIFACT_NAME
    -> verified staged working copy for transient delivery, extraction,
       helpers, validation, and execution
<drive>:\<project>_show_project_to_AI\
    -> durable project-support artifacts and evidence
<drive>:\<project>_delete_after_daily_work\
    -> disposable at end of work/day after durable evidence is promoted
```

The active `project_tool_boundary_canon` owns the actual Tool, Project, Project
Support, and transient-root formulas. Do not hardcode one project's paths into a
reusable patch.

## Failure behavior

When the gate cannot prove safe delivery, return:

```text
PATCH DELIVERY BLOCKED
Missing owner or evidence:
Unknown source state:
Next safe action:
May emit patch ZIP: NO
May claim validation: NO
May freeze: NO
```

## Scope exclusions

This prompt does not define:

- ZIP member lists or payload schemas;
- `INSTALL.ps1`, `VALIDATE.ps1`, or `FREEZE.ps1` implementations;
- PowerShell cleanup footers;
- freeze-hint or freeze-form field schemas;
- Error Memory field lists or lesson JSON templates;
- validation-evidence merge commands;
- startup-delivery regeneration logic;
- implementation authorization.

## Do-not-regress rules

- Keep this file compact and always-startup.
- Keep detailed patch behavior in Class 05.
- Never ask the user to pre-place a delivered artifact directly inside
  `_delete_after_daily_work`; the incoming source begins at the active Project
  drive root and KANDA derives the staging destination programmatically.
- Re-derive the drive root, Project name, and transient root whenever the
  selected Project changes. Never cache another Project's transient path.
- Use copy -> SHA-256 verify -> root-source delete. A failed verification must
  preserve the drive-root source and must not accept a partial staged copy.
- Keep terminal behavior with `terminal_cleanup_contract`.
- Keep durable evidence out of transient-only storage.
- Keep exact-source, validation, and human-freeze gates fail closed.
- Never repair a delivery regression by weakening fingerprint or validation
  requirements.
