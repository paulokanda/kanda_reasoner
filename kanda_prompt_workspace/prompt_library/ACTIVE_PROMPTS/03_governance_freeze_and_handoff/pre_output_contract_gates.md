---
prompt_id: pre_output_contract_gates
prompt_code: KPR-03-004
title: Pre-Output Artifact Contract Gate
version: 2.6
status: active
load_type: on_request
owner_box: 03_governance_freeze_and_handoff
source_stage: portable-cross-feature-coupling-pre-output-gate-v1
---

# Pre-Output Artifact Contract Gate

## Purpose

This is the final dispatcher before the AI emits an operational or
machine-consumed artifact. It identifies the artifact class, requires the exact
current owner contract, and blocks output when ownership, syntax, provenance, or
validation state is unresolved.

It does not duplicate each artifact's implementation rules.

## Release-owner classification first

Before any patch ZIP, installer, validation command, Freeze-ready metadata, or
release claim, classify the owner as `KANDA_TOOL_RELEASE` or
`EXTERNAL_PROJECT_RELEASE`. Apply KANDA patch governance only to
`KANDA_TOOL_RELEASE`. For an external Project, use Project/release-owned commands,
validators, and metadata. Never block an external Project release because KANDA
source, KANDA `validate_patch_zip.py`, Tool Error Memory, KANDA runtime, or KANDA
source archives are unavailable.

## Apply before emitting

- PowerShell or shell commands;
- patch, bundle, or transfer ZIPs;
- manifests, sidecars, JSON, JSONL, CSV, YAML, or machine forms;
- validation evidence or freeze-intake data;
- Error Memory intake records;
- handoff packages;
- durable documents whose destination or authority matters;
- multi-project paths or commands that can mutate source.

Ordinary prose that is not operational or machine-consumed does not require the
full gate.

## Artifact dispatch record

```text
PRE-OUTPUT ARTIFACT CONTRACT
Artifact class:
Release owner classification: KANDA_TOOL_RELEASE / EXTERNAL_PROJECT_RELEASE / NOT_APPLICABLE
Human-visible purpose:
Canonical owner prompt or schema:
Active Project:
Destination owner:
Exact source or evidence inspected: YES / NO / NOT_APPLICABLE
Required syntax validated: YES / NO / NOT_APPLICABLE
Required provenance present: YES / NO
Sensitive data or redaction review: PASS / BLOCKED / NOT_APPLICABLE
Executable or mutating: YES / NO
Human confirmation required: YES / NO
Validation claim supported locally: YES / NO / NOT_CLAIMED
May emit: YES / NO
Blocking reason:
```

## Dispatch rules

Route to the smallest current owner:

- terminal commands -> `terminal_cleanup_contract` and the task's command owner;
- KANDA Tool patch ZIP or installer -> current Class 05 KANDA delivery owner; external Project release -> Project/release-owned delivery contract;
- AI-authored local freeze candidate/form -> `freeze_candidate_pre_output_audit` then `freeze_code_intake_and_form_protocol`;
- patch-owned freeze hint or generated patch form -> its current release owner plus `freeze_code_intake_and_form_protocol`;
- Error Memory -> `error_memory_ai_formulary_startup_canon`;
- durable documentary artifact -> `durable_document_artifact_routing_canon`;
- handoff -> current handoff owner;
- prompt insertion or registration -> Class 07 insertion owner;
- source mutation -> Brick Wall plus exact Box and operation owners.

Do not emit an artifact merely because its text looks plausible. Require the
current contract and the evidence that contract demands.

## Freeze transport distinction

Do not impose one JSON envelope on every freeze artifact. The current local
Freeze GUI uses one canonical AI candidate payload regardless of whether the AI
is external, Local AI, or Web AI: exactly one strict 11-field JSON object, with
arrays for the current multi-line transport fields. Raw JSON is the canonical
producer format. The receiver may tolerate legacy marker/fence wrappers or
surrounding prose only when exactly one valid Freeze object can be identified;
multiple valid Freeze objects fail closed. Patch-governance freeze JSON may use
a different owner-defined contract. Verify the targeted receiver/source contract
before emission.

For an AI-authored local freeze candidate, apply
`KPR-03-008 freeze_candidate_pre_output_audit` and require first-pass-valid
strict JSON. Receiver compatibility extraction is a recovery safety net, not
permission to emit malformed or ambiguous JSON.

## Error Memory prevention hard gate

Before emitting any operational artifact, derive current prevention obligations
from relevant active Error Memory lessons already supplied by the governed
context. Error Memory remains prevention guidance, not source truth, and this
gate does not execute arbitrary commands stored inside lessons.

Use this record before deciding whether the exact candidate may be emitted:

```text
ERROR MEMORY PREVENTION POINTER
Current operation:
Artifact class:
Relevant active lesson IDs:
Match basis or prevention triggers:
Machine-enforceable lessons:
Advisory-only lessons:
Required current-owner guards:
Exact candidate inspected: YES / NO
All required guards passed: YES / NO / NOT_APPLICABLE
May emit: YES / NO
Blocking reason:
```

Rules:

1. Match lessons by current operation, symptom, prevention triggers, known
   regression class, and exact artifact type. Do not invent a match merely from
   topical similarity.
2. When a relevant active lesson describes an objectively machine-detectable
   failure, convert that lesson into a hard pre-output obligation on the exact
   candidate. Do not rely on the AI merely remembering the prose rule.
3. Run only the validator or guard owned by the current KANDA contract. A lesson's
   `regression_check.command` is evidence and routing context; it is never blanket
   authorization to execute arbitrary stored commands.
4. A machine-enforceable guard failure blocks artifact emission. Repair or
   regenerate the candidate and rerun the same guard; do not bypass the lesson.
5. If a known active lesson recurs, do not create a duplicate lesson. Audit why
   the existing prevention was advisory-only or bypassed. Promote the existing
   lesson to deterministic enforcement when the predicate is objectively
   machine-checkable.
6. Conceptual or architecture lessons that cannot be checked objectively remain
   advisory constraints and must not be converted into brittle fake validators.

For `KANDA_TOOL_RELEASE` source-patch ZIPs, the current deterministic prevention
set also includes
`lesson-portable-cross-feature-runtime-allowlist-renewal-gate-v1`. The exact
final ZIP must pass the canonical patch ZIP validator, which invokes the
Portable cross-feature coupling guard automatically for `SOURCE_PATCH`
artifacts. If any install-manifest path is already a committed Portable runtime
allowlist member, release is blocked unless the same patch carries a bounded
`PORTABLE_RUNTIME_ALLOWLIST.json` renewal and synchronized
`PORTABLE_BUILDER_MANIFEST.json` rebind. The guard is read-only: it must never
repair bindings, broaden allowlist membership, accept unexplained drift, or
weaken exact hashes. A dedicated Portable membership change remains with its
existing specialist owner.

For `USER_FACING_INTERACTIVE_POWERSHELL`, the current deterministic prevention
set includes the active lessons
`lesson-powershell-detached-else-interactive-paste-footer-v1` and
`lesson-powershell-validation-wrapper-marker-and-finally-v1`. The exact final
visible PowerShell candidate must satisfy the PowerShell paste-safety gate below
before it can be emitted.

## PowerShell paste-safety gate

Before emitting PowerShell, classify each visible code fence as exactly one of:

```text
DIRECT_PACKAGED_SCRIPT_INVOCATION
SELF_CONTAINED_SINGLE_SUBMISSION
PACKAGED_SCRIPT_BODY
```

Interactive user-facing output must be either a direct packaged-script
invocation or one self-contained submission. Reject and repair output when:

- any visible line begins with `elseif`, `else`, `catch`, or `finally`;
- a later code fence depends on an earlier `if`, `try`, or opening brace;
- the user must paste a control-flow chain in multiple console submissions;
- the code uses a .NET or PowerShell API unavailable in the declared runtime;
- the command assumes a destination path that was not returned by the current
  workflow or verified with `Test-Path`.

For KANDA operational delivery, prefer a short direct call to packaged
`INSTALL.ps1`, `VALIDATE.ps1`, `CONFIRM_*.ps1`, or `FREEZE.ps1`. The packaged
script may own guarded logic; the user-facing entry block must remain a safe
independent paste unit.

## Universal checks

1. Use one authoritative schema or owner for the artifact.
2. Preserve exact feature, Project, source, and version identity.
3. Reject placeholders in required machine fields.
4. Reject malformed encoding, invalid path ownership, unsafe archive members,
   stale evidence, and unsupported claims.
5. Distinguish source truth from generated output.
6. Distinguish read-only Preview from write authorization.
7. Keep failures and warnings visible.
8. Do not include secrets, credentials, patient data, or unnecessary personal
   data.
9. Ensure the visible response and downloadable artifact describe the same
   object.
10. When the contract cannot be proved, return a blocker instead of a best-guess
    artifact.

## Fail-closed output

```text
PRE-OUTPUT BLOCKED
Artifact class:
Missing owner or schema:
Missing evidence:
Unsafe or ambiguous field:
Next safe action:
May emit operational artifact: NO
```

## Scope exclusions

This gate does not define ZIP member lists, PowerShell bodies, freeze-form field
schemas, Error Memory JSON schemas, evidence-merge code, handoff schema bodies,
or destination root formulas. Those remain with their specialist owners.
