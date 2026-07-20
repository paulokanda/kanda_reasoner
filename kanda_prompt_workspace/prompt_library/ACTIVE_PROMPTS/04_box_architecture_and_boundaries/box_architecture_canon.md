---
prompt_id: box_architecture_canon
prompt_code: KPR-04-001
title: Box Architecture Canon
version: 2.0
status: active
load_type: routed
owner_box: 04_box_architecture_and_boundaries
source_stage: prompt-audit-wave4b-box-architecture-boundaries-v1
---

# Box Architecture Canon

## Purpose

Define stable ownership and boundary laws for one bounded responsibility box.
This canon identifies architectural owners, public contracts, private internals,
dependency direction, authoritative mutable state, lifecycle vocabulary, and the
Box Boundary Audit. It provides evidence to Brick Wall and never authorizes
source mutation by itself.

## Relationship to other owners

- Brick Wall is the final governed implementation-authority coordinator.
- `project_tool_boundary_canon` owns Tool, Active Project, Project Support, and
  transient-root identity.
- `boundary_first_repair_protocol` diagnoses symptom-owner divergence.
- `kanda_box_shielding_canon` converts proven invariants into regression fitness
  functions when shield applicability is established.
- Class 05 owns packaging, installation, validation delivery, and freeze prep.

## Source-first operating order

1. Inspect exact current source and current metadata.
2. Identify current owner evidence and consumers.
3. Resolve root identity through the Tool/Project owner when relevant.
4. Ask the human only when material ambiguity remains.
5. Return architectural evidence to Brick Wall.

## Core box definition

A box is a bounded responsibility owner with:

- one declared purpose;
- one public contract or facade;
- private internals that consumers must not reach into;
- explicit dependencies and communication paths;
- one authoritative mutation owner for each mutable state;
- declared lifecycle and fallback behavior;
- focused validation of its public behavior and boundaries.

A box is not defined by an arbitrary folder, file count, tab, class, or process.
Those may be implementation details.

## Stable box laws

1. One primary responsibility owner per change.
2. Supporting touches must be explicit and bounded.
3. Consumers use public contracts, never private reach-in.
4. Dependencies point toward stable abstractions and declared owners.
5. Derived views, snapshots, caches, and read-only projections may exist, but
   they do not become authoritative mutation owners.
6. Optional features must define unavailable, disabled, replaced, and removed
   behavior.
7. Registries may locate public owners; they must not absorb domain behavior or
   become hidden mutable-state owners.
8. Generated artifacts, previews, evidence, and exports are not source truth.
9. Unknown ownership, stale evidence, or undeclared cross-box mutation fails
   closed.

## Public contract and private internals

A public contract states the supported inputs, outputs, events, commands,
errors, versioning, fallback, and compatibility expectations. Private internals
remain replaceable. A consumer that needs an internal detail must request a
public-contract change rather than import or mutate the private owner.

Commands request an owner action. Events report an owner fact. Shared mutable
objects, callback reach-in, implicit globals, and duplicated writes are not
substitutes for a contract.

## One-primary-owner rule and explicit exception

Normal work uses one primary owner plus declared supporting touches. A governed
atomic multi-owner contract migration is allowed only when:

- a compatible staged path is not viable;
- every producer and consumer owner is explicit;
- the contract version and rollback behavior are explicit;
- every touched boundary is validated;
- Brick Wall authorizes the exact operation.

## Lifecycle vocabulary

`draft`, `active`, `frozen`, `deprecated`, `disabled`, and `tombstone` are common
states. This canon defines the vocabulary only. Current metadata, validation,
freeze, and retirement owners define transition evidence and write procedure.

## Manifest invariants

When a box manifest exists, it should identify at least:

- schema version and box identity;
- owner path and public facade;
- authoritative state owners;
- allowed dependencies and consumers;
- lifecycle and fallback behavior;
- validators and expected markers.

The current schema owner controls the physical manifest shape. This canon does
not embed a competing full schema.

## Box Boundary Audit

```text
BOX BOUNDARY AUDIT
Active Project:
Operation or task ID:
Exact source evidence:
Primary box:
Public owner / facade:
Private internals:
Authoritative mutable-state owners:
Allowed changed files:
Declared supporting touches:
Files explicitly out of scope:
Producer / consumer contracts:
Cross-box commands or events:
Tool / Project root evidence:
Generated-artifact authority check:
Lifecycle and fallback behavior:
Boundary risks:
Disconfirming evidence:
Required focused validators:
Required boundary / state / concurrency / stale-result tests:
Architecture status: COMPLETE / BLOCKED / NOT_APPLICABLE
Brick Wall authorization still required: YES
May begin coding from this audit: NO
```

## Boundary-focused validation

Select only applicable categories and give reasoned `NOT_APPLICABLE` evidence:

- public-contract and consumer compatibility;
- private-reach-in and dependency-direction negatives;
- authoritative-state and transition tests;
- stale asynchronous-result and concurrency tests;
- root/path containment and generated-source authority;
- optional, disabled, removed, and fallback behavior;
- property or mutation pilots only when independently justified.

## NO_LEAK ownership split

This canon owns architectural leak categories and public/private law. Tool
Boundary owns roots. Shielding owns selected invariant protection. Brick Wall
owns completeness and authorization. Specialist validators own concrete paths
and runtime checks.

## Anti-pattern identities

Reject God Box expansion, leaking registries, private reach-in, hidden shared
mutation, duplicate owners, generated-artifact-as-source, ownership-free helper
layers, undeclared supporting touches, and context or coordination super-systems
created only to avoid current owners.

## Authority boundary

This canon does not create a roadmap, package a ZIP, install a patch, write
freeze memory, authorize coding from a generic `go`, or define product-specific
tutorials. Completion means the architectural evidence is ready for its next
canonical owner.
