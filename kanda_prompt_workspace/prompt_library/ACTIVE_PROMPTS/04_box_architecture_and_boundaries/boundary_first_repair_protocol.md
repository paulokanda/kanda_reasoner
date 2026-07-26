---
prompt_id: boundary_first_repair_protocol
prompt_code: KPR-04-006
title: Boundary-First Repair Protocol
version: 2.0
status: active
load_type: routed
owner_box: 04_box_architecture_and_boundaries
source_stage: prompt-audit-wave4b-box-architecture-boundaries-v1
---

# Boundary-First Repair Protocol

## Purpose

Diagnose a regression when the visible symptom may not belong to the true repair
owner. Trace authority, state, persistence, lifecycle, public contracts, roots,
and asynchronous generations before choosing a repair location.

```text
Symptom location is not repair ownership.
Trace authority and state flow first.
Repair the earliest causally sufficient proven ownership violation.
```

This is a diagnostic specialist. Box Architecture defines ownership, Shielding
protects selected invariants, and Brick Wall remains the implementation owner.

## Activate when

Use for suspected cross-box, shared-host, persistence, root, lifecycle,
transaction, public-contract, or stale asynchronous-result defects. Do not load
for a proven local syntax error or a new design with no symptom-owner question.

## Evidence identity

Bind the diagnosis to:

- Active Project and current root identities;
- feature, operation, transaction, or MCard generation when applicable;
- exact source fingerprints and event time;
- current public owner and consumers;
- last known good and first known bad evidence.

Do not guess the last relevant change. Classify correlation as `PROVEN_CAUSAL`,
`PLAUSIBLE`, `TEMPORAL_ONLY`, or `UNKNOWN`.

## Diagnostic method

1. Reproduce or precisely describe the symptom.
2. Trace the public call, event, state, persistence, or artifact flow backward.
3. List credible owner hypotheses.
4. Record supporting and disconfirming evidence for each hypothesis.
5. Identify the earliest proven boundary or authority violation.
6. Prove that repairing it is causally sufficient or is the smallest safe
   intervention that preserves the current public contract.
7. Distinguish the primary repair owner from the wider validation scope.
8. Route implementation back to Brick Wall and the exact owner.

## Boundary diagnostic record

```text
BOUNDARY-FIRST DIAGNOSTIC RECORD
Active Project:
Feature / operation / transaction identity:
Current generation:
Exact source fingerprints:
Symptom and reproduction:
Visible symptom box:
Current public contract:
Authoritative state / persistence / lifecycle owners:
Change correlation: PROVEN_CAUSAL / PLAUSIBLE / TEMPORAL_ONLY / UNKNOWN
Owner hypotheses:
Supporting evidence:
Disconfirming evidence:
Earliest proven ownership violation:
Causal sufficiency evidence:
Smallest safe intervention:
Primary repair owner:
Declared supporting touches:
Downstream validation scope:
Reasoned N/A validations:
Stale-evidence check:
Boundary diagnosis status: OWNER_PROVEN / OWNER_PROVISIONAL / OWNER_UNRESOLVED
Brick Wall authorization still required: YES
May begin coding: NO
May write source: NO
```

## Guardrails

- Do not patch the downstream symptom merely because it is visible there.
- Do not call an owner proven without disconfirming-evidence review.
- Do not treat validation scope as repair ownership.
- Do not let a rejected or stale operation acquire authority.
- Do not load delivery or pre-output owners until an operational artifact is
  actually relevant.
- Do not reproduce complete Box, Shielding, Tool Boundary, or lifecycle canons.

## Completion

`OWNER_PROVEN` means the diagnosis can return to Brick Wall. It is not source
write authorization. `OWNER_PROVISIONAL` or `OWNER_UNRESOLVED` remains blocked.
