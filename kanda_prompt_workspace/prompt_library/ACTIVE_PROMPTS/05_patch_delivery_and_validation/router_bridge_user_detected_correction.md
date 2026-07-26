---
prompt_id: router_bridge_user_detected_correction
prompt_code: KPR-05-006
title: User-Detected Correction Incident Dispatcher
version: 2.0
status: active
load_type: routed
owner_box: 05_patch_delivery_and_validation
source_stage: prompt-audit-wave5b-router-terminal-compatibility-v1
---

# User-Detected Correction Incident Dispatcher

## Purpose

Admit and classify a real correction incident, preserve the first reliable
failure evidence, and route the incident to the smallest current owner set.
This prompt owns incident admission and dispatch only. It does not authorize
source writes, define patch or receiver contracts, create freeze entries, or
write Error Memory.

## Activate when

Use when the user or AI identifies an actual prior-answer, source, path,
boundary, install, validation, delivery, startup, freeze, or Error Memory
failure. Do not use for ordinary feature work, speculative planning, or a
request with no demonstrated defect.

## Immediate containment

1. Stop the normal success path.
2. Preserve the exact failure phase, exception type, message, command or action,
   last reliable marker, and affected artifact identity.
3. Do not emit a replacement success marker after a failed phase.
4. Do not rerun mutation, installation, validation, or freeze until current
   source and artifact identity are resolved.
5. Keep the live project unchanged when a disposable reproduction can establish
   the cause safely.

## Correction incident record

```text
CORRECTION INCIDENT RECORD
Incident ID:
Reported by: USER / AI / VALIDATOR / INSTALLER
Failure phase:
Observed symptom:
Exact evidence:
Affected project and root:
Affected source, artifact, or response:
Last reliable marker:
Potential Error Memory match:
Potential PIR match:
Current owner suspected:
Exact source inspection required: YES / NO
Disposable reproduction required: YES / NO
Patch potentially required: YES / NO
Freeze state affected: YES / NO
Disposition: DIAGNOSE / REPAIR_EXISTING / VALIDATOR_ONLY / DELIVERY_ONLY / NO_CHANGE / BLOCK
May inspect exact source: YES / NO
May begin correction coding: NO
Next safe action:
```

Incomplete identity, missing exact evidence, or conflicting owners requires
`BLOCK`. This record never grants write or delivery authority.

## Direct owner dispatch

- Governed source or prompt correction: Brick Wall and the exact current source,
  Tool/Project, Box, Error Memory, and specialist owners.
- Patch or receiver defect: `pre_output_contract_gates`,
  `implementation_and_delivery_protocol`, current patch governance, and
  `patch_install_delivery_error_register`.
- Terminal defect: `terminal_cleanup_contract`.
- Freeze defect: `freeze_code_intake_and_form_protocol`; Preview stays read-only
  and Confirm and Write stays human-confirmed.
- Error Memory candidate: current Error Memory intake and model templates; stage
  pending intake only when reusable evidence exists.
- Startup-delivery defect: the startup-delivery maintenance protocol and
  canonical generator/source map.

The retired `brick_wall_comprehensive_quality_gate` and
`pre_output_contract_gates` are historical aliases only and must not
be loaded.

## Error Memory classification

Always classify Error Memory applicability. Create lesson material only when the
incident supports a reusable prevention rule. Never write directly into Lessons.
Pending intake remains under the selected project's Error Memory support root
and requires human review and Memorize Error. Evidence-backed `N/A` is allowed.

## Correction progression

```text
incident admitted
-> relevant compact Error Memory and PIR classes reviewed
-> exact current source or artifact inspected
-> root cause and disconfirming evidence recorded
-> smallest current owner selected
-> Brick Wall task-specific authorization obtained when writing is needed
-> focused correction or no-change decision
-> exact validation
-> exact release contract when applicable
-> Windows-local evidence when applicable
-> human freeze only when appropriate
```

## Fail-closed output

```text
CORRECTION DISPATCH BLOCKED
Incident:
Missing identity or evidence:
Conflicting owner:
Unsafe action prevented:
May patch: NO
May claim validation: NO
May freeze: NO
Next safe action:
```

## Non-authorization statement

This dispatcher cannot authorize implementation, patch release, validation
claims, freeze, or Error Memory persistence.
