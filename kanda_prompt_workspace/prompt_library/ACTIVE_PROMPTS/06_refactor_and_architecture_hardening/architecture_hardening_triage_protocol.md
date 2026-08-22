# Architecture Hardening Triage Protocol

Prompt code: `KPR-06-005`
Prompt id: `architecture_hardening_triage_protocol`
Version: 2.1.0
Status: `active`
Load type: `routed`
Owner box: `06_refactor_and_architecture_hardening`

## Purpose

Use this protocol to classify a demonstrated architecture risk, identify the
current owner and existing protection, and select the smallest justified
hardening response.

Hardening is not rewriting. Do not turn warning cleanup into broad redesign.

## Project-agnostic operating rule

This prompt defines standalone Project engineering logic. It must remain usable
when no particular host tool, prompt router, memory system, freeze/snapshot
system, validator suite, or support-root convention exists.

- The active Project owns its source, runtime, tests, validation, delivery,
  release, and implementation authorization through its own declared workflow.
- Host-specific quality gates, lesson/error-memory systems, freeze/snapshot
  systems, routers, validators, and support artifacts are optional adapters.
  Their absence must not block this prompt's technical reasoning.
- References to local prompt IDs or companion names are routing hints only when
  that prompt library is present; they are not execution prerequisites.
- This prompt never grants source-write, validation, release, or freeze/snapshot
  authority by itself.

## Owns

This prompt owns only:

- architecture-hardening admission;
- risk classification;
- current-owner discovery;
- existing-protection and validator coverage review;
- protection-gap classification;
- smallest-intervention selection;
- a bounded triage record.

## Does not own

This prompt does not authorize or own:

- source mutation;
- Box law;
- shielding law;
- patch construction or installation;
- validation claims;
- snapshot/freeze writes;
- lesson/error-memory writes;
- project-specific checker implementation;
- one hardcoded architecture-owner map.

Use the current owners instead:

- `KPR-03-001 brick_wall_comprehensive_quality_gate` for coding authority;
- `KPR-04-001 box_architecture_canon` for Box ownership and boundaries;
- the current shielding/invariant-protection owner for justified shielding;
- `KPR-04-006 boundary_first_repair_protocol` when this prompt library is present for symptom-owner divergence;
- the active Project root/ownership authority for path and owner identity;
- current project validators for executable protection;
- the active Project delivery owners for delivery, validation evidence, and optional snapshot/freeze preparation.

## Admission gate

Open a hardening triage only when current evidence shows at least one concrete
risk, such as:

- a boundary or ownership violation;
- duplicate public or mutable-state ownership;
- a stale or conflicting generated artifact;
- a public-facade or dependency-direction defect;
- hidden state or lifecycle leakage;
- an unprotected regression repeatedly observed in current source or runtime;
- an architecture validator error requiring owner-level interpretation.

Do not admit a campaign merely because a broad cleanup sounds useful.

## Authority order

Use this order:

1. current explicit user requirement;
2. exact current source and operation identity;
3. current frozen behavior and do-not-regress rules;
4. relevant current Project error/lesson records, when available;
5. current Box, Tool/Project, and public-contract owners;
6. current runtime, test, and architecture evidence;
7. this triage protocol;
8. historical reports and examples.

Historical findings never override current source truth.

## Required evidence

Record what is available and mark missing evidence explicitly:

- project root and selected target;
- source SHA-256 or equivalent current fingerprint;
- primary Box and owner paths;
- public contracts and active consumers;
- current architecture findings with source locations;
- current validators and their coverage;
- relevant frozen behavior;
- relevant Project error/lesson records, when available;
- generated-artifact provenance when involved;
- evidence that could disconfirm the suspected problem.

Unknown is not equivalent to absent.

## Finding classes

Classify every admitted finding as exactly one of:

### HARD_FAILURE

Current evidence proves an active contract, boundary, ownership, safety, or
validation violation. The release cannot proceed while it remains unresolved.

### PROTECTION_GAP

A verified behavior or boundary exists, but current executable protection is
missing or insufficient. Add or strengthen the smallest current owner only
when the gap is demonstrated.

### TRANSITIONAL_DEBT

The issue is real, but repairing it in the current operation would create
unbounded risk or violate a frozen boundary. Keep it visible with an owner and
exit condition. Do not weaken validators globally to hide it.

### WARNING

The evidence does not justify blocking or mutation. Record the observation and
close the triage unless new evidence appears.

### NOT_APPLICABLE

The suspected architecture issue is disproved or belongs to another owner.
Record the disconfirming evidence and route to the correct owner when needed.

## Triage workflow

1. Bind the exact project, target, source fingerprint, operation, and lifecycle
   generation.
2. State the primary Box and every bounded supporting touch.
3. Identify the current canonical behavior owner.
4. Identify existing validators, tests, shielding, and frozen protection.
5. Reproduce or verify the architecture finding using current evidence.
6. Search for disconfirming evidence and alternate owners.
7. Classify the finding.
8. Compare the smallest plausible responses:
   - no change;
   - current-validator repair;
   - owner-local source repair;
   - boundary or facade repair;
   - narrow shielding;
   - bounded refactor through the large-module owner;
   - defer as transitional debt.
9. Select one response and state why broader alternatives are rejected.
10. Hand the result to the active Project's declared implementation authority for implementation admission.

## Detector coverage record

When a historical or proposed detector category is raised, map it to current
owners before proposing implementation:

```text
Finding family:
Current owner:
Implemented detector or validator:
Evidence source and version:
Coverage: COMPLETE / PARTIAL / NONE / NOT_AUTOMATABLE / NOT_APPLICABLE
Severity policy:
False-positive risks:
Expected success and rejection markers:
Relevant Project error/lesson records, if available:
Concrete current gap:
Smallest justified extension:
```

A new detector is justified only when a concrete current failure is demonstrated,
current owners do not already detect it, a measurable contract exists, and the
smallest owner-local extension plus regression protection is identified. Tab or
GUI labels are not stable architecture identities.

## Protection-gap rule

Do not create a new checker, scanner, registry, graph, schema, or engine when an
existing owner can be strengthened. A new protection surface requires a
verified gap that current owners cannot cover adequately.

## Allowlist rule

Allowlist only verified transitional debt with:

- exact finding identity;
- current owner;
- justification;
- expiration or removal condition;
- validator behavior that keeps new findings visible.

Never weaken a general rule to make one current report green.

## Triage output contract

Return one record with:

```text
ARCHITECTURE HARDENING TRIAGE
Project:
Target:
Source fingerprint:
Operation identity:
Primary box:
Current owner:
Public contract:
Verified finding:
Finding class:
Existing protection:
Protection gap:
Disconfirming evidence:
Smallest justified response:
Rejected broader responses:
Required validators:
Current blockers:
May begin coding: YES / NO
Next safe action:
```

`May begin coding` is `YES` only when the active Project's declared implementation authority separately authorizes it.

## Stop conditions

Stop and report `BLOCKED` when:

- exact source identity is unresolved;
- two owners appear equally authoritative;
- a required current file is unavailable;
- the finding cannot be reproduced or disproved safely;
- the proposed response crosses a private Box boundary;
- validation ownership is unknown;
- a snapshot/freeze-protected behavior would be changed without explicit admission, when such protection exists.

## Final rule

Classify first, strengthen the current owner second, and change the smallest
possible surface only after separate implementation authorization.
