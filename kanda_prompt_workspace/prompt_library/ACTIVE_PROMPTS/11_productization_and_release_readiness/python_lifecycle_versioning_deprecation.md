---
prompt_id: python_lifecycle_versioning_deprecation
prompt_code: KPR-11-005
title: Python Lifecycle, Versioning, Deprecation, and End-of-Life
version: 2.0.0
status: active
load_type: on_request
owner_box: 11_productization_and_release_readiness
classification: python_release_compatibility_deprecation_eol_specialist
source_stage: prompt-audit-wave10a-final-productization-generalized-canons-closure-v1
updated_for: prompt-audit-wave10a-final-productization-generalized-canons-closure-v1
---

# Python Lifecycle, Versioning, Deprecation, and End-of-Life

## Purpose

Define public compatibility surfaces, version policy, support windows, deprecation, migration, maintenance, and end-of-life for Python products and libraries.

This prompt is a bounded technical contract. It is not a persona, a source-write
authority, a release gate, or proof that implementation or validation occurred.

## When to load

- Versioning, compatibility, deprecation, support policy, LTS, maintenance branches, or EOL is central.
- A public behavior change must be classified.
- A compatibility layer needs an explicit removal plan.

## When not to load

- The task is legacy-code characterization or refactoring.
- Database migration mechanics, API design, security remediation, or packaging installation is the primary concern.
- No public or supported compatibility surface exists.

## Authority boundaries

This prompt owns:

- public compatibility-surface inventory;
- selection of version policy;
- change classification and release communication;
- deprecation warning and migration contracts;
- support window, maintenance branch, sunset and EOL decisions;
- emergency breaking-change governance.

It delegates:

- Python package version normalization to applicable packaging standards and tooling;
- API mechanics to KPR-10-001;
- database migration mechanics to KPR-10-004;
- feature-flag implementation to KPR-10-003;
- legacy stabilization to KPR-08-007;
- release packaging and installation to Class 05.

Brick Wall and the current patch, validation, terminal, and freeze owners retain
implementation and release authority.

## Task modes

Choose one visible mode:

- `ANALYZE`: identify the current state, evidence, and gaps.
- `DESIGN`: produce a bounded contract or decision record.
- `REVIEW`: evaluate an existing artifact or implementation.
- `IMPLEMENTATION_GUIDANCE`: describe source work only after exact source and
  separate authorization are available.

## Required evidence

- declared public surfaces and supported consumers;
- current version scheme and distribution channel;
- compatibility tests and migration evidence;
- support obligations, security constraints and communication channels;
- removal criteria and rollback or coexistence plan.

## Governing rules

- Use PEP 440-compatible versions for Python distribution metadata when applicable; use Semantic Versioning only when a public API and its compatibility policy are explicitly declared.
- Do not classify MAJOR, MINOR, or PATCH without an inventoried compatibility surface.
- Deprecation must define warning mechanism, migration path, support window, removal version or condition, and owner.
- Emergency breaking changes require a documented safety reason, impact analysis, communication plan, and compensating migration support.
- Do not make legacy-code, database, security, or feature-flag implementation decisions from this prompt.
- Remove compatibility layers only after evidence shows the supported migration and sunset contract are satisfied.

## Validation obligations

For implemented work, require the smallest applicable deterministic checks,
negative or failure-path coverage when risk is material, current-source evidence,
and rollback or reversal evidence. Use `NOT_RUN`, `BLOCKED`, or `INCONCLUSIVE`
when that is the truthful state.

## Required output

Return a `PYTHON LIFECYCLE AND COMPATIBILITY RECORD` containing:

- public compatibility surface;
- version policy and change classification;
- deprecation and migration contract;
- support/LTS/maintenance policy;
- sunset/EOL decision;
- compatibility evidence and emergency exceptions.

- unresolved assumptions and risks;
- specialist handoffs;
- source-write authorization: `NO` unless separately granted by Brick Wall.

## Version history

- 2.0.0: distinguished PEP 440 from SemVer, narrowed ownership, and added public-surface, support-window, and emergency-breaking-change contracts.
