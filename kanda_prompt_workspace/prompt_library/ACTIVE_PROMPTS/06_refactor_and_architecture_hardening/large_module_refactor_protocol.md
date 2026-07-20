# Large Module Creation and Refactor Protocol

Prompt code: `KPR-06-007`
Prompt id: `large_module_refactor_protocol`
Version: 9.1.0
Status: `active`
Load type: `routed`
Owner box: `06_refactor_and_architecture_hardening`

## Purpose

Use this protocol when a new or touched source module would exceed the project
hard maximum, or when current evidence shows that a module has materially mixed
responsibilities, unsafe dependency direction, or unmaintainable complexity.

The protocol owns generic behavior-preserving decomposition law and specialist
dispatch. It does not own KANDA Planner, Workbench, AST-audit implementation,
patch delivery, terminal behavior, validation evidence, or freeze writes.

## Module-size and complexity law

For KANDA Reasoner code/source modules:

- ideal size: 400 physical lines or fewer;
- absolute hard maximum: 500 physical lines or fewer;
- every new or touched code/source module must satisfy the hard maximum after
  normal readable formatting;
- split by cohesive responsibility, not arbitrary line ranges;
- do not create unnecessary micro-files merely to reduce line count;
- do not pad files with comments, repeated docstrings, or trivial wrappers;
- never remove required behavior, contracts, tests, diagnostics, or validation
  solely to satisfy the size gate;
- do not compress formatting to conceal an oversized module;
- measure physical lines after normal PEP 8-compliant formatting;
- preserve required top-level and class-level blank lines;
- preserve SOLID responsibility and dependency direction;
- preserve one authoritative DRY implementation owner.

A line-count pass produced by compressed or non-readable formatting is invalid.
No universal minimum file size is imposed. Cohesion, ownership, and dependency
direction determine whether a helper should exist.

## Owns

This prompt owns:

- large-module admission;
- exact-source and owner evidence requirements;
- public API and consumer preservation rules;
- responsibility-island decomposition;
- dependency-direction and no-leak rules;
- characterization and semantic-equivalence requirements;
- touched-family source-size and architecture obligations;
- refactor veto and rollback requirements;
- dispatch to current KANDA specialists.

## Does not own

Delegate these responsibilities:

- implementation authorization: `KPR-03-001` Brick Wall;
- Box ownership: `KPR-04-001` Box Architecture;
- boundary diagnosis: `KPR-04-006` Boundary-First Repair;
- shielding: `KPR-04-002` KANDA Box Shielding;
- target-specific AST risk repair: `KPR-06-003`;
- reusable safe-refactor runbook: `KPR-06-004 safe_refactor_how_to`;
- architecture-hardening triage when the primary problem is structural risk rather than module decomposition: `KPR-06-005`;
- optional architecture triage record: `KPR-06-006`;
- this governing protocol: `KPR-06-007`;
- optional large-module planning record: `KPR-06-008`;
- external architecture exchange: `KPR-06-001`;
- imported planning bundle profile: `KPR-06-002`;
- patch construction, installation, validation evidence, terminal cleanup, and
  freeze preparation: current Class 05 owners;
- Preview and Confirm and Write: current freeze owners.

## When to load

Load when at least one condition is true:

- a new or touched module is above 500 physical lines;
- the requested change would push a touched module above 500 lines;
- one module owns multiple material responsibilities;
- dependency direction or public-facade ownership requires decomposition;
- a current architecture or AST audit identifies a source-family refactor need;
- the user explicitly requests a behavior-preserving large-module refactor.

Do not load for a small local edit that remains within the size and cohesion
contract.

## Authority order

Use this order:

1. current target source bytes and source identity;
2. current frozen behavior and do-not-regress rules;
3. current Error Memory lessons;
4. current Box, public-contract, and consumer evidence;
5. current behavior characterization and tests;
6. current AST and architecture evidence;
7. this generic protocol;
8. historical examples and earlier refactor reports.

## Required preflight evidence

Before choosing a split, inspect or record:

- exact target relative path;
- source SHA-256 and byte length when available;
- current physical line count;
- primary Box and canonical owner;
- imports, aliases, and known consumers;
- public classes, functions, constants, and `__all__`;
- signatures, defaults, decorators, bases, and annotation behavior;
- side effects, CLI entry points, GUI signals, and lifecycle hooks;
- current tests and characterization gaps;
- dependency direction and private boundaries;
- relevant frozen behavior and Error Memory;
- current architecture and AST findings;
- plausible disconfirming evidence.

Unknown evidence must remain explicit.

## Public-contract rule

Preserve observable behavior unless the user separately authorizes a feature
change. Preserve as applicable:

- public import paths;
- public names and aliases;
- signatures and defaults;
- decorator identity and order;
- class bases and dataclass configuration;
- enum and status values;
- deterministic exceptions and messages;
- serialized output;
- CLI output and exit codes;
- GUI signal and lifecycle behavior;
- externally visible side-effect order.

Keep public facades thin but real. Do not move public ownership into a private
helper merely to lower a line count.

## Responsibility-island method

Build a candidate-island queue before implementation. Each candidate island
must have:

- one clear responsibility;
- a proposed owner path;
- dependencies it may read;
- state it may own or mutate;
- public and private boundary effects;
- consumer and import impact;
- expected line-count range;
- focused characterization and validation coverage.

Select the smallest island or compatible bounded set that resolves the verified
problem. Do not combine unrelated cleanup.

## Dependency-direction rule

Prefer one-way flow:

```text
public facade -> cohesive private implementation owner -> lower-level pure owner
```

Do not create:

- helper-to-facade back references without explicit design need;
- sibling cycles;
- cross-Box private imports;
- hidden mutable state on a shared GUI host;
- dynamic import or monkey-patch workarounds that conceal ownership;
- generated artifacts as source authority.

## Refactor workflow

### Phase 0 - Admission

State the verified size, cohesion, ownership, or dependency problem. Search for
an in-place repair before admitting a split.

### Phase 1 - Exact source and owner binding

Bind project root, target path, source fingerprint, primary Box, current owner,
public contract, consumers, and operation identity. Stop on mismatch.

### Phase 2 - Characterization

Create or identify meaningful baseline cases. Signature comparison alone is not
behavior equivalence.

### Phase 3 - Architecture options

Compare at least the plausible options:

- smallest in-place repair;
- facade plus one cohesive helper;
- facade plus multiple justified responsibility owners;
- package conversion with stable re-exports;
- defer because evidence or tests are insufficient.

Select the smallest adequate architecture and reject broader options explicitly.

### Phase 4 - Transformation plan

Define an ordered, reversible plan. Keep feature changes separate from the
structural refactor.

### Phase 5 - Candidate construction

Move complete responsibilities, preserve public ownership, and keep normal
runtime logic in ordinary importable source files.

### Phase 6 - Behavior comparison

Run the same meaningful semantic inputs against baseline and candidate. Compare
outputs, exceptions, side effects, consumer imports, and repeated-call behavior
as applicable.

### Phase 7 - Touched-family validation

Validate every touched permanent source module, including the facade, new
helpers, and supporting source changes. Require:

- physical line compliance;
- syntax and importability;
- public-contract compatibility;
- consumer compatibility;
- dependency direction;
- Box and No-Leak compliance;
- relevant semantic and GUI behavior;
- current architecture or AST evidence when applicable.

### Phase 8 - Release handoff

Hand the exact changed-file set and validator obligations to current Class 05
owners. Do not embed or recreate delivery, terminal, validation-evidence, or
freeze workflows here.

## Post-refactor verification ownership

After a split, do not create a parallel universal fragmentation runner. Verify
the complete touched source family through current owners:

- AST/static owner for unresolved names and missing imports;
- public-contract and feature validators for facade bindings, exports, aliases,
  and consumer imports;
- architecture/boundary owners for cross-Box, GUI, state, or dependency leaks;
- runtime owner for import and headless smoke behavior;
- module-quality owners for size, cohesion, and dependency direction.

A finding record may include module, root facade, source fingerprint, unresolved
names, binding/export gaps, missing imports, GUI or boundary leaks, smoke status,
public-contract impact, current owner, current validator, and next safe action.
Integrate a new check only when a demonstrated current gap remains after review
of existing owners.

## GUI-specific evidence

When GUI code is involved, inventory:

- signals and slots;
- widget ownership and parentage;
- event filters and lifecycle hooks;
- thread or worker ownership;
- stale-result identity checks;
- current state hydration;
- externally visible labels, enabled states, and actions.

Use real-widget validation when a protected interaction cannot be proven from
static inspection.

## Veto conditions

Do not proceed when:

- exact current source is unavailable;
- public consumers cannot be identified sufficiently;
- characterization is too weak for the proposed move;
- the split would create private cross-Box reach-in;
- a new helper would have no cohesive responsibility;
- the proposed architecture depends on padding or hidden dynamic behavior;
- rollback cannot restore the exact predecessor;
- a frozen contract would change without separate admission.

## Output contract

Before implementation, return:

```text
LARGE MODULE REFACTOR DECISION
Project:
Target:
Source fingerprint:
Physical lines:
Verified trigger:
Primary box:
Canonical owner:
Public contract:
Known consumers:
Characterization status:
Candidate islands:
Selected architecture:
Rejected alternatives:
Expected file sizes:
Behavior-equivalence plan:
Required validators:
Rollback obligation:
Current blockers:
May begin coding: YES / NO
Next safe action:
```

`May begin coding` requires separate Brick Wall authorization.

## Final rule

Preserve behavior, preserve public ownership, split only along real
responsibility boundaries, and delegate release mechanics to their current
owners.
