---
prompt_id: kanda_box_shielding_canon
prompt_code: KPR-04-002
title: KANDA Box Shielding Canon
version: 2.0
status: active
load_type: routed
owner_box: 04_box_architecture_and_boundaries
source_stage: prompt-audit-wave4b-box-architecture-boundaries-v1
---

# KANDA Box Shielding Canon

The stable prompt ID and title are retained for routing compatibility. The shielding doctrine below is project-agnostic and does not require KANDA Reasoner or any other host tool.

## Purpose

Define a risk-based method for converting important architectural invariants of
one bounded context into executable regression fitness functions. A shield is
not feature expansion, routine unit testing, a style refactor, a delivery
workflow, or an automatic milestone ceremony.

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

## Relationship to other owners

Box Architecture identifies the box and public contract. Boundary-First Repair
locates a suspected ownership defect. The active Project's declared implementation authority decides whether shield work is admitted and authorized. Packaging and snapshot/freeze preparation remain with the active Project or host-specific delivery owners.

## Shield applicability decision

Create or strengthen a shield only when current evidence shows at least one of:

- meaningful authority or state-owner risk;
- cross-box or public-contract regression risk;
- stale-result, concurrency, path, side-effect, or fallback risk;
- a high-impact invariant not protected by current focused tests;
- stronger or cross-box work whose safety depends on preserved invariants.

Do not require a new shield merely because a milestone, refactor, or model
version changed. Prefer existing focused tests when they already prove the
necessary contract.

```text
SHIELD APPLICABILITY DECISION
Box and public owner:
Proposed stronger or risky change:
Current protected invariants:
Existing validators and gaps:
Unique shield value:
Simpler existing-test strengthening sufficient: YES / NO
Decision: REQUIRED / STRENGTHEN_EXISTING / NOT_APPLICABLE / BLOCKED
Separate Project implementation authorization still required: YES
May begin coding: NO
```

## Shield contract

A bounded shield records:

- exact box, facade, source, feature, and operation identity;
- protected public behavior and forbidden authority escalation;
- authoritative mutable-state owners;
- allowed dependencies, side effects, and outputs;
- unavailable, disabled, fallback, and removal behavior;
- positive controls and negative boundary cases;
- stale-result, transaction, concurrency, and path checks when applicable;
- validator commands, expected markers, and durable evidence.

## Tests-first workflow

1. Prove applicability and inventory current tests.
2. State the invariant in public-contract language.
3. Add a failing focused regression or equivalent characterization when safe.
4. Implement only the smallest contract hardening admitted by the active Project's declared implementation authority.
5. Run focused, boundary, negative, and consumer regressions.
6. Record limitations and unprotected risks.
7. Return evidence to the active Project validation owner and any optional snapshot/freeze owner.

## Shield evidence record

```text
BOX SHIELD EVIDENCE
Feature / operation identity:
Protected box and facade:
Source fingerprints:
Invariant set:
Forbidden authority:
Allowed dependencies and side effects:
Positive controls:
Negative boundary cases:
State / stale-result / concurrency coverage:
Fallback and removal coverage:
Existing tests reused:
New focused fitness functions:
Commands and exact markers:
Durable evidence path:
Limitations:
Shield status: COMPLETE / PARTIAL / BLOCKED / NOT_APPLICABLE
May begin coding from this record: NO
May write snapshot/freeze state from this record: NO
```

## Scope exclusions

A generic shield does not define product-specific advisory states, model output
language, dependency blacklists, security profiles, routing authority, patch ZIP
membership, support-artifact paths, or snapshot/freeze-write procedure. Those belong to
the owning box and current specialist canons.

## Do-not-regress rules

- Shielding is risk-based, not milestone-automatic.
- A shield protects a bounded public contract and cannot invade another box.
- Advisory output never becomes authority without its canonical owner.
- No new cross-project shield registry or runtime coordination service.
- Completion never authorizes source writes or any host-specific snapshot/freeze confirmation.
