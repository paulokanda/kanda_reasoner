# Safe Refactor How To

Prompt code: `KPR-06-004`
Prompt id: `safe_refactor_how_to`
Version: 2.0.0
Status: `active`
Load type: `routed`
Owner box: `06_refactor_and_architecture_hardening`

## Purpose

Use this prompt as a user-facing safe-refactor refresher and specialist
dispatcher. It helps an AI interpret current source and appended support
artifacts, select the smallest current owner set, and identify the next safe
action for a behavior-preserving refactor.

This prompt does not own implementation authorization, target-specific AST
repair, generic large-module law, patch delivery, terminal behavior, validation
evidence, or snapshot/freeze writes.

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

## When to use

Load only when the user explicitly invokes Safe Refactor How To or asks for the
safe-refactor process before a consequential module refactor.

Do not load for a small local edit, a generic Python explanation, or as a
replacement for exact current target evidence.

## Current authority order

1. current target source bytes and source identity;
2. current protected/frozen behavior applicable to the target, when such memory exists;
3. current Project error/lesson records applicable to the operation, when available;
4. current Box, shielding, public-contract, and consumer evidence;
5. current behavior characterization and executable validators;
6. current AST and architecture findings;
7. current canonical specialist prompts;
8. this refresher and appended support artifacts;
9. historical worked examples.

Unknown evidence remains unknown. Historical examples never override current
source or current validation truth.

## Specialist dispatch

- the active Project's declared implementation authority: implementation admission and blockers.
- `KPR-04-001 box_architecture_canon` when this prompt library is present, or the Project-equivalent Box owner: owner Box and allowed boundaries.
- the current Project invariant-protection owner, when available: justified shielding.
- `KPR-04-006 boundary_first_repair_protocol`: symptom-owner divergence.
- `KPR-06-003 web_ai_ast_split_risk_repair_protocol`: exact target-specific AST
  exchange and repair evidence.
- `KPR-06-005 architecture_hardening_triage_protocol`: demonstrated structural
  risk and protection-gap triage.
- `KPR-06-007 large_module_refactor_protocol`: generic behavior-preserving
  decomposition, public-contract, cohesion, and module-size law.
- the active Project delivery owners: installable package, validation evidence, and terminal behavior.
- optional Project or host-specific snapshot/freeze owners: preparation, preview, and explicit confirmation when such a lifecycle exists.

Load only the smallest owner set required by the verified problem.

## Six non-negotiable safety principles

1. Bind the exact project, target path, source fingerprint, and operation before
   mutation.
2. Preserve public imports, names, signatures, decorators, annotations,
   exceptions, serialized output, side effects, and consumer behavior unless a
   separate feature change is explicitly authorized.
3. Split by cohesive responsibility and one-way dependency direction, never by
   arbitrary line ranges or formatting compression.
4. Apply the active Project's supplied module-size policy. When this prompt library's default policy is explicitly selected, use an ideal of 400 physical lines or fewer and a hard maximum of 500 physical lines after normal readable formatting. There is no universal 101-line minimum.
5. Require semantic behavior comparison plus current focused and regression
   validators for the complete touched source family.
6. Stop on source mismatch, unresolved owner conflict, stale target evidence,
   private cross-Box reach-in, or unapproved frozen-behavior change.

## High-level sequence

```text
1. bind exact source and owner
2. inspect consumers, public contracts, protected/frozen behavior, and Project error/lesson records when available
3. verify the real size, cohesion, dependency, or AST problem
4. compare the smallest plausible architectures
5. obtain separate authorization from the active Project's declared implementation authority
6. construct one reversible behavior-preserving candidate
7. run semantic comparison and current touched-family validation
8. hand delivery, terminal, evidence, and optional snapshot/freeze preparation to current Project owners
```

This sequence is guidance, not source-write authority.

## Post-refactor verification route

Do not create a second universal fragmentation runner. Route current evidence to
existing owners:

- unresolved names or missing imports: current AST/static validator;
- facade binding or public import drift: current public-contract and
  feature-specific validators;
- cross-Box or GUI leakage: architecture and boundary validators;
- import or headless smoke failure: current feature/runtime validator;
- module-size or cohesion regression: `KPR-06-007` and current module-quality
  validators.

Record, when relevant:

```text
module
source fingerprint
root facade
unresolved names
binding or export gaps
missing imports
cross-Box or GUI leaks
import/headless smoke status
public-contract impact
current owner
current validator
next safe action
```

A new checker or runner requires a demonstrated gap that current owners cannot
adequately cover.

## Appended support-artifact roles

The Safe Refactor How To button may append exactly three support artifacts:

1. `AST_SAFE_REFACTOR_ROUTINE.md`: current process support;
2. a host-specific read-only AST-safe-refactor helper, if supplied (for KANDA-hosted sessions this may be `kanda_ast_safe_refactor_routine.py`);
3. `runtime_activation_refactor_routine_report_example.json`: explicitly
   non-authoritative historical evidence-shape example.

The guide and helper are support context, not independent governance owners. The
worked report example must never supply current paths, hashes, findings, or PASS
claims.

If target source, audit evidence, or support-artifact identity is missing or
stale, stop and request or regenerate only the missing current evidence.

## Output

Return a concise record:

```text
SAFE REFACTOR DISPATCH
Project:
Target:
Source fingerprint:
Verified trigger:
Primary box:
Current implementation authority:
Selected specialist owners:
Public contracts and consumers:
Relevant frozen behavior:
Relevant Project error/lesson records, if available:
Evidence gaps:
Smallest next safe action:
Required validators:
May begin coding: YES / NO
```

`May begin coding` is `YES` only when the active Project's declared implementation authority separately authorizes it.

## Non-authorization statement

This refresher cannot authorize source mutation, package installation,
validation claims, or frozen-memory writes. Preview remains read-only and final
any snapshot/freeze write requires the explicit confirmation contract of the active Project or host, when such a lifecycle exists.
