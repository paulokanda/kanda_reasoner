# Web AI AST Split Risk Repair Protocol

Prompt code: `KPR-06-003`
Prompt id: `web_ai_ast_split_risk_repair_protocol`
Version: 2.0.0
Status: `active`
Load type: `routed`
Owner box: `06_refactor_and_architecture_hardening`

## Purpose

Use this protocol when the exact source of one selected Python target and its
current AST Split Audit evidence are sent to an external Web AI for
behavior-preserving source repair.

It supports:

1. a truthful `RISK REFACTORING` to `SAFE REFACTORING` repair; or
2. an already-SAFE target that still requires a cohesive split under the
   current supplied module-size policy.

This prompt owns target-specific AST repair reasoning. It does not own generic
large-module law, Planner architecture exchange, bundle formatting, terminal
behavior, validation infrastructure, or final freeze writes.

## Distinct ownership

- KPR-06-003: exact target-specific source repair from AST evidence.
- KPR-06-007: generic decomposition, cohesion, public-contract, and current
  module-size law.
- KPR-06-001: bounded external Planner architecture exchange.
- KPR-06-002: Imported Web AI planning-response bundle profile.
- current Class 05 owners: package, Install, Validate, terminal, evidence, and
  rollback mechanics.

## Required input

Require this exact wrapper identity:

```text
TARGET_RELATIVE_PATH
SOURCE_SHA256
SOURCE_BYTE_LENGTH
SOURCE_TEXT_ENDS_WITH_NEWLINE
CURRENT_SAFETY_LABEL
AST_SAFE_REFACTOR_PREFLIGHT_EVIDENCE_BEGIN ... END
AST_AUDIT_RESULT_BEGIN ... END
TARGET_SOURCE_BEGIN ... END
```

Treat the target path, bytes, length, newline state, and SHA-256 as immutable
repair identity. Never repair a different file or infer omitted source.

## Evidence authority

The complete source and current AST audit are primary evidence. The preflight
block may summarize consumers, public contracts, decorators, annotations,
dependency direction, dynamic-risk findings, and workflow-specific size gates.
It is read-only support, not autonomous architecture authority.

## Mode A — RISK input

For `RISK REFACTORING`:

1. map each hard blocker to exact source behavior;
2. separate blockers from warnings;
3. remove the real unsafe mechanism without hiding it;
4. preserve observable behavior and public contracts;
5. rerun the same current classifier on every touched source-family module;
6. claim success only when the fresh result is `SAFE REFACTORING` with zero
   hard blockers.

## Mode B — SAFE structural split

For an already-SAFE target:

- do not invent a RISK narrative;
- preserve SAFE status and zero hard blockers for the complete touched family;
- split only for a verified cohesion, dependency, or current size obligation;
- preserve the original facade when consumer compatibility requires it;
- avoid duplicate public ownership and helper-to-facade back references;
- rerun the current classifier on all touched permanent Python modules.

## Current size-policy rule

Do not hardcode a universal 101-line minimum. Apply the exact current
workflow-specific size policy supplied in the preflight evidence. When no
specialized workflow policy is supplied, defer to KPR-06-007:

```text
ideal: 400 physical lines or fewer
hard maximum: 500 physical lines or fewer
universal minimum: none
```

Never add padding, compressed formatting, arbitrary wrappers, or artificial
line-range splits to satisfy a number.

## Anti-gaming law

Forbidden shortcuts include:

- weakening the AST classifier or its threshold;
- deleting required behavior to remove a finding;
- renaming or wrapping a dangerous call to evade detection;
- moving the same risk into an unaudited helper;
- using `eval`, `exec`, `getattr`, `setattr`, `globals`, `locals`,
  `__import__`, or importlib indirection merely to hide evidence;
- suppressing reports or omitting touched modules from the rerun;
- changing public names or signatures without explicit current evidence.

## Repair workflow

1. Verify target path and exact source identity.
2. Read complete source, audit, and preflight evidence.
3. Classify the current mode truthfully.
4. Map blockers or structural obligations to exact code.
5. Inspect consumers, public contract, decorators, annotations, and side effects.
6. Compare the smallest behavior-preserving repair options.
7. Record a bounded plan before editing.
8. Preserve public names, signatures, return contracts, exceptions, and import
   paths.
9. Preserve decorator order and annotation runtime semantics.
10. Keep dependency direction one-way and cohesive.
11. Apply the current supplied size policy without inventing a universal floor.
12. Build one reversible candidate under current Class 05 package rules.
13. Validate syntax, imports, consumers, public API, behavior, dependency
    direction, source identity, and fresh AST classification.
14. Claim success only from fresh rerun evidence produced by the current classifier.
15. Prepare freeze evidence only after validation passes.

## Required validation evidence

Use current truthful markers, including as applicable:

```text
SOURCE_IDENTITY_GUARD: PASS
PYTHON_SYNTAX: PASS
PUBLIC_API_PRESERVATION: PASS
CONSUMER_COMPATIBILITY_FITNESS: PASS
BEHAVIOR_EQUIVALENCE_FITNESS: PASS
DEPENDENCY_DIRECTION_FITNESS: PASS
CURRENT_MODULE_SIZE_POLICY: PASS
AST_SPLIT_AUDIT_FRESH_RERUN: PASS
SOURCE_FAMILY_SAFE_REFACTORING: PASS
ZERO_HARD_BLOCKERS: PASS
STATUS: IN_SYNC
```

Do not print a PASS marker that was not produced by local validation.

## Required delivery

Return:

1. exact diagnosis and selected mode;
2. concise behavior-preserving transformation rationale;
3. complete candidate source family or governed patch artifact;
4. current Class 05 Install instructions;
5. current Class 05 Validate instructions;
6. fresh AST rerun evidence;
7. freeze-evidence preparation only after validation passes;
8. one complete Markdown replacement for the existing single AST Split Audit
   text window.

## Single-window report

The report must replace, not append to, the current target-specific text:

```text
# Large Module AST Split Audit

Target: `<relative path>`
Source SHA-256: `<validated hash>`
Safety label: `SAFE REFACTORING`
Hard blockers: `0`
Current size-policy result: `PASS`

## Refactor safety classification
<fresh evidence>

## Candidate islands
<current source-family structure>

## Independence matrix
<current dependency evidence>

## Recommended patch composition
<exact touched files and validators>

## AI handoff instruction
<next governed action>
```

Keep exactly one AST Split Audit text window. Clear stale target-specific text
when the target changes.

## Freeze boundary

The patch may include a root `KANDA_FREEZE_HINT.json`, but final freeze remains
local and human-confirmed:

```text
validation passes
-> evidence merge
-> Preview Freeze Entry
-> explicit Confirm and Write
```

## Do not regress

- Do not weaken classifier or audit authority.
- Keep exact source identity and complete current evidence.
- Keep initially SAFE families SAFE after the split.
- Do not restore a universal 101-line minimum.
- Keep one AST Split Audit output window.
- Keep implementation delivery and final freeze with current owners.
