---
prompt_id: pre_output_contract_gates
prompt_code: KPR-03-004
title: Pre-Output Artifact Contract Gate
version: 2.0
status: active
load_type: on_request
owner_box: 03_governance_freeze_and_handoff
source_stage: prompt-audit-wave4a-governance-freeze-handoff-v1
---

# Pre-Output Artifact Contract Gate

## Purpose

This is the final dispatcher before the AI emits an operational or
machine-consumed artifact. It identifies the artifact class, requires the exact
current owner contract, and blocks output when ownership, syntax, provenance, or
validation state is unresolved.

It does not duplicate each artifact's implementation rules.

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
- patch ZIP or installer -> current Class 05 delivery owner;
- freeze hint or form -> `freeze_code_intake_and_form_protocol`;
- Error Memory -> `error_memory_ai_formulary_startup_canon`;
- durable documentary artifact -> `durable_document_artifact_routing_canon`;
- handoff -> current handoff owner;
- prompt insertion or registration -> Class 07 insertion owner;
- source mutation -> Brick Wall plus exact Box and operation owners.

Do not emit an artifact merely because its text looks plausible. Require the
current contract and the evidence that contract demands.

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
