# Project Tool Boundary Canon

Version: 2.2
Status: Active prompt-library canon
Prompt ID: project_tool_boundary_canon
Prompt code: KPR-12-001
Owner group: 12_generalized_project_canons
Load type: routed

## Purpose

Own the KANDA-specific Tool-versus-selected-Project identity and root-ownership contract.

This canon defines logical owners and the identity evidence required before consequential work. It does not own Box Architecture, durable-document routing, Workbench storage implementation, patch staging, MCard lifecycle, or final coding authorization.

## Canonical ownership model

```text
Tool identity = reusable KANDA Reasoner machinery
Project identity = selected project and its source
Project Support = durable project-specific support outside source
Transient workspace = non-authoritative disposable staging
Generated evidence = non-source artifact unless a canon explicitly grants authority
```

Self-hosting may make Tool and Project roots equal. Root equality never collapses logical ownership.

## Owner boundaries

KPR-12-001 owns:

- Tool and selected-Project logical identity;
- source-root and write-target ownership classification;
- Project Support and transient-workspace class separation;
- self-hosting separation;
- wrong-root and unresolved-identity hard stops.

Other owners remain authoritative:

- `box_architecture_canon`: responsibility and module boundaries;
- `durable_document_artifact_routing_canon`: durable document and evidence destinations;
- Class 05 delivery prompts: patch staging and installation;
- `architecture_review_project_card_machine_canon`: Architecture Review target lifecycle;
- Workbench and transaction contracts: Preview, Shadow, transaction, and receipt implementation;
- Brick Wall: final coding, source-write, delivery, validation-claim, and freeze authorization.

## Required identity record

Before Brick Wall Q06 is complete, produce:

```text
TOOL/PROJECT IDENTITY RECORD
Task classification:
Operation class: TOOL_CHANGE / PROJECT_OPERATION / MIXED_GOVERNED / BLOCKED
Session ID:
Operation ID:
Selection timestamp:
Selection source:
Tool project ID:
Tool source root:
Active Project ID:
Active Project slug:
Active Project root:
Active Project source roots:
Selected mutation root:
Project root fingerprint or immutable identity:
Same canonical resolved Tool/Project root: YES / NO / UNRESOLVED
Self-hosting mode: YES / NO / UNRESOLVED
Active Project Support root:
Support-root identity and collision status:
Transient workspace root:
Transient namespace and cleanup owner:
Requested source write targets:
Tool write set:
Project write set:
External or cross-project paths:
Cross-project access modes:
Generated evidence authority: NON_AUTHORITATIVE / CANON_ASSIGNED / UNRESOLVED
Generated evidence owner reference:
Support security and retention profile:
Identity invalidation conditions:
Identity ambiguities:
Identity decision: COMPLETE / BLOCKED
May proceed to Q07 classification: YES / NO
May begin coding: NO
```

## Identity evidence requirements

The selection record must be current and typed. It must identify the selected root, Project ID, selection source, session, timestamp, and freshness basis. Keyword presence in prose is not evidence.

The Project ID must remain stable across ordinary display-name changes. The slug is a readable label, not a sufficient uniqueness key. If two projects can resolve to the same support-root name, the support-root resolver must detect the collision and block until an explicit disambiguation or migration decision is approved.

Use `Same canonical resolved Tool/Project root`, not `same physical root`, unless true filesystem identity has been proven. Path strings alone do not prove equivalence across links, junctions, substituted drives, UNC aliases, network mappings, or case aliases.

## Root profiles

### Tool source

Reusable engines, GUI, validators, prompt machinery, startup machinery, patch governance, and reusable freeze tooling remain Tool-owned.

### Active Project source

The selected Project owns its source and authorized generated source results. A multi-root workspace must list all source roots and identify one selected mutation root for the operation.

### Project Support

KANDA-managed durable support is external to Project source. It may contain handoff data, Error Memory, Freeze Memory, durable validation evidence, and other project-specific support artifacts.

The default sibling/drive-root naming profile is valid only after collision checks and canonical resolution. A rename, move, drive change, or workspace reassignment must not silently orphan, merge, or overwrite support state. Migration requires source and destination identity checks, conflict detection, explicit provenance, and verified completion.

For KANDA-managed Project Support roots, this nested form is forbidden:

```text
<active_project_root>/<active_project_slug>_show_project_to_AI
```

Detection blocks new support writes until conflict-safe migration and removal complete.

### Non-authoritative transient workspace

The project-linked transient workspace owns no durable truth. It requires an explicit path owner, cleanup owner, session/operation namespace, containment rule, storage budget, maximum age, crash-recovery cleanup, and secure deletion policy when sensitive content may exist.

Disposable clones and Shadow artifacts may be removed. A failed operation that must remain auditable writes only a scrubbed durable summary, fingerprints, failure markers, and reproduction reference to the appropriate Project Support owner.

## Path and write safety

Before mutation:

1. resolve canonical paths with the platform-aware public path owner;
2. classify links, junctions, aliases, UNC or drive semantics as applicable;
3. prove containment against the current resolved owner root;
4. recheck containment and source freshness immediately before write;
5. use safe write/open behavior appropriate to the platform;
6. reject path replacement or identity drift between validation and write.

No reusable Tool code may be installed into Project Support. No selected-Project result may be installed into reusable Tool source merely because KANDA performed the work.

## Mixed governed operations

`MIXED_GOVERNED` requires separate Tool and Project write sets, owner-specific validators, explicit ordering, atomicity boundaries, rollback behavior, partial-failure handling, and public-contract migration when both owners change.

A mixed operation remains blocked when one write set, validator set, rollback owner, or dependency order is unresolved.

## Cross-project and external paths

External dependencies, comparison repositories, controlled fixtures, and migration sources may be read when declared. Each path must have an access mode such as `READ`, `COMPARE`, `MIGRATION_SOURCE`, or `AUTHORIZED_WRITE` plus an owner and scope.

The hard prohibition is undeclared or unauthorized cross-project mutation, not every non-empty cross-project path list.


## Portable-distribution ownership

A portable distribution such as:

```text
<project>-Windows-Portable.zip
```

is not a Show Project to AI artifact and is never created by Show Project to
AI. Show Project and Portable Distribution are different Box owners and must
never share an output owner, trigger, output folder, lifecycle, or implicit
cross-box call. Portable creation is allowed only through an independently
routed productization/release workflow after an explicit user request. It must
be published outside the selected Project Support root and must not be silently
regenerated during handoff, source-archive, backup, Freeze, or Error Memory
operations.

Portable identity is semantic and filename-owned, not location-owned. When such
an archive already exists or is misplaced anywhere inside Project source, Show
Project may only classify and exclude it from AI source packaging and record
exclusion provenance. It may also fail closed for an unclassified suspicious
large root archive. Exclusion is not authorization to create, refresh, publish,
move, or delete the portable distribution.

## Generated evidence authority

Generated handoffs, archives, summaries, and reports are non-authoritative by default. Authority may be granted only through a current canonical owner and must be recorded as a structured enum with that owner reference.

Generated archives remain evidence and never replace exact source inspection.

## Security, privacy, and retention

Project Support and transient artifacts may contain source excerpts, private paths, logs, customer or patient data, and accidentally captured secrets. The operation must identify applicable redaction, access permission, encryption, retention, backup, and secure-deletion requirements. Unresolved high-risk handling blocks durable write or export.

## Concurrent sessions

Session and operation namespaces must prevent collisions. Concurrent operations against the same source or durable support identity require a lease, lock, compare-and-swap rule, or another explicit conflict detector owned by the relevant implementation contract.

## Specialist routing

Load specialist overlays rather than copying their contracts here:

- Architecture Review target lifecycle: `KPR-12-005`;
- Workbench Preview, Shadow, transaction, and receipt paths: current Workbench owner;
- patch staging and install: Class 05;
- durable documents and validation evidence: durable-document routing;
- Box and No-Leak classification: Box Architecture and NO_LEAK_LOGIC_V1.

## Validation requirements

Validation must prove, as applicable:

- source and metadata identity alignment;
- one active KPR-12-001 owner;
- compact startup bridge routes to this canon without duplicating authority;
- self-hosting preserves logical separation;
- KANDA-managed support stays external to Project source;
- nested support writes fail closed;
- cross-project access is typed and unauthorized mutation is rejected;
- generated evidence authority is structured;
- mixed write sets and rollback owners are complete;
- session/operation conflict protection is declared;
- current resolved containment is rechecked before write;
- startup delivery is regenerated and in sync after bridge changes.

## Required decision

```text
Tool/Project identity gate: COMPLETE / BLOCKED
May proceed to Q07 classification: YES / NO
May begin coding: NO
```

## Do-not-regress rules

- Never collapse Tool and Project ownership, including self-hosting.
- Never treat slug equality or path-string equality as complete identity proof.
- Never place KANDA-managed Project Support inside Project source.
- Never let the transient workspace own durable truth.
- Never hardcode KANDA Reasoner as the selected Project for project-specific state.
- Never authorize coding from Q06 alone.
- Never duplicate MCard, Workbench, delivery, or durable-document owner contracts in this canon.
- Never silently merge support state after project rename, move, or collision.
- Never allow undeclared or unauthorized cross-project mutation.
- Never create or refresh `<project>-Windows-Portable.zip` from Show Project to AI; require a separate explicit user request and productization/release workflow.

## Version history

- 2.2: made Show Project and Portable Distribution separate Box owners with no
  shared trigger, output owner, folder, lifecycle, or implicit call; portable
  identity is excluded wherever misplaced under Project source.
- 2.1: canonized portable-distribution separation: Show Project to AI never
  creates `<project>-Windows-Portable.zip`; portable builds require a separate
  explicit user request and productization/release workflow outside Project Support.
- 2.0: split compact startup bridge from the full routed owner; added stable Project identity, collision and migration decisions, typed selection and generated-evidence authority, mixed-operation write sets, transient lifecycle, security, concurrent-session, multi-root, and current-resolved-path requirements.
- 1.5: enforced Q06 identity and external Project Support behavior.
