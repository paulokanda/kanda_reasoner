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

## Purpose

Define a risk-based method for converting important architectural invariants of
one bounded context into executable regression fitness functions. A shield is
not feature expansion, routine unit testing, a style refactor, a delivery
workflow, or an automatic milestone ceremony.

## Relationship to other owners

Box Architecture identifies the box and public contract. Boundary-First Repair
locates a suspected ownership defect. Brick Wall decides whether shield work is
admitted and authorized. Class 05 owns packaging and freeze preparation.

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
Brick Wall authorization still required: YES
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
4. Implement only the smallest contract hardening admitted by Brick Wall.
5. Run focused, boundary, negative, and consumer regressions.
6. Record limitations and unprotected risks.
7. Return evidence to the validation and freeze owners.

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
May freeze from this record: NO
```

## Scope exclusions

A generic shield does not define product-specific advisory states, model output
language, dependency blacklists, security profiles, routing authority, patch ZIP
membership, Project Support paths, or freeze-write procedure. Those belong to
the owning box and current specialist canons.

## Do-not-regress rules

- Shielding is risk-based, not milestone-automatic.
- A shield protects a bounded public contract and cannot invade another box.
- Advisory output never becomes authority without its canonical owner.
- No new cross-project shield registry or runtime coordination service.
- Completion never authorizes source writes or human freeze confirmation.
