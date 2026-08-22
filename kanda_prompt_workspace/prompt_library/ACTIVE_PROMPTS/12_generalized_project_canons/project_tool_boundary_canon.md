# Project Tool Boundary Canon

Version: 2.5
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

KANDA-managed durable support is external to Project source. It may contain handoff data, Error Memory exports or intake evidence, Freeze Memory, durable validation evidence, and other project-specific support artifacts. Reusable Error Memory lessons remain Tool-owned.

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

## Explicit code-placement and cross-write rule

For every build, update, regression repair, installation, validation, Freeze,
Error Memory, or packaging operation, the AI must enforce this default rule:

```text
KANDA Tool-owned reusable code and files stay under the canonical Tool owner.
Selected-Project-owned code and files stay under the canonical selected Project owner.
Never write KANDA Tool code into an external selected Project source tree.
Never write external selected-Project code into KANDA Tool source.
```

A `MIXED_GOVERNED` operation may write both owners only through two explicit,
owner-pure write sets. Every Tool path must contain Tool-owned behavior and every
Project path must contain Project-owned behavior. Writing both roots is not
authorization to copy one owner's runtime, source, prompt library, installer, or
validator into the other owner's source tree.

### Project Support handoff exception

The selected Project's dynamic support root, normally:

```text
<project_drive>/<project_name>_show_project_to_AI
```

may contain the files needed to show, explain, validate, freeze, or memorize the
selected Project for AI-assisted work. This includes generated handoffs, source
archives or source-part copies, manifests, prompts, screenshots, validation
evidence, Freeze intake and memory, and Error Memory intake and lessons produced
by KANDA Reasoner.

This is a support and evidence exception only. Project Support remains outside
both source owners, is non-authoritative unless a canon assigns authority, and
must never become an import root, install destination, runtime dependency, or
substitute for current exact source. The canonical name uses one separator
underscore: `<project_name>_show_project_to_AI`.

### KANDA Reasoner self-hosting exception

When the selected Project is KANDA Reasoner itself and canonical resolution
proves that the active Project source root and KANDA Tool source root are the
same owner root, Tool work and Project work may physically write the same source
tree. The operation must still classify each change, declare the exact write
set, use current fingerprints, and run owner-appropriate validation and rollback.

Self-hosting does not collapse logical ownership and never authorizes code from
a different selected Project to be written into KANDA Tool source.

## Mixed governed operations

`MIXED_GOVERNED` requires separate Tool and Project write sets, owner-specific validators, explicit ordering, atomicity boundaries, rollback behavior, partial-failure handling, and public-contract migration when both owners change.

A mixed operation remains blocked when one write set, validator set, rollback owner, or dependency order is unresolved.

## Cross-project and external paths

External dependencies, comparison repositories, controlled fixtures, and migration sources may be read when declared. Each path must have an access mode such as `READ`, `COMPARE`, `MIGRATION_SOURCE`, or `AUTHORIZED_WRITE` plus an owner and scope.

The hard prohibition is undeclared or unauthorized cross-project mutation, not every non-empty cross-project path list.

## Fire Shield programmatic authority

The frozen Tool Fire Shield remains a fail-closed boundary for KANDA-managed
Project reads and KANDA-owned writes to Project Support or transient evidence. It
never grants KANDA Reasoner authority to mutate external Project source.

### Actor-scope gate

Classify every external-Project task before applying Tool governance:

```text
KANDA_OBSERVER_ACTOR
    KANDA Reasoner reads Project source or writes only KANDA-owned support or
    transient evidence. Project source mutation is unsupported.

PROJECT_ACTOR
    The Project is edited, installed, tested, executed, validated, released, or
    rolled back through its own IDE, terminal, interpreter, CI, installer, or
    Project-owned delivery package.
```

For `PROJECT_ACTOR` work:

- KANDA Reasoner selection state, registry, portable runtime, Fire Shield, Tool
  interpreter, GUI, validators, Error Memory export, source archive, or
  availability is not an execution prerequisite;
- never request KANDA Tool source or `kanda_reasoner__source_archive_partXX_of_YY.zip`
  to implement, install, validate, release, or roll back an external Project;
- use Project-owned source, safeguards, interpreter, validators, release contract,
  rollback, and human authorization;
- KANDA may observe the resulting source and evidence afterward, but that
  observation neither grants nor revokes Project mutation authority.

For `KANDA_OBSERVER_ACTOR` work:

1. Resolve the current selected-Project identity through public owners.
2. Use `kanda_reasoner_app.project_operation_authority` and Fire Shield only for
   supported read, Project Support, or transient-evidence operations.
3. `PROJECT_SOURCE_WRITE` remains unsupported and must fail with the spectator
   boundary instead of escalating to another KANDA mutation path.
4. KANDA may package read-only handoff/source-copy evidence into Project Support,
   but generated copies never become source or release authority.
5. Tool maintenance is a separate explicit Tool operation and is never inferred
   from a selected external Project defect.

### External Project release independence

For an external Project release, the validation and release authority belongs to
the Project:

```text
Project-owned release validator present
    -> use that Project validator

Release carries a self-contained Project validator
    -> use that release-local validator

No Project validator yet
    -> characterize the missing Project-side validation and, when authorized,
       create a Project-local validator

Never
    -> fall back to KANDA Reasoner scripts/validate_patch_zip.py
    -> require KANDA Reasoner source, runtime, interpreter, or source archives
```

`scripts/validate_patch_zip.py` is the canonical KANDA Tool patch validator for
KANDA-owned release units. It is not a universal validator for selected Projects.

### Source archive provider rule

If exact source for Project `P` is needed, inspect current Project source or request
only `P`'s source archive. Never switch the source provider to KANDA Reasoner
because a Tool prompt, validator, Freeze feature, or Error Memory lesson refers to
Tool code. The only exception is when KANDA Reasoner itself is the Project being
repaired.

### Tool Error Memory scope

Tool Error Memory is mandatory prevention context for governed KANDA Reasoner Tool
repairs. For independent external `PROJECT_ACTOR` development it is advisory when
available; missing Tool Error Memory must not block Project coding, validation, or
release.

Fire Shield is application-level protection for the observer boundary and
KANDA-owned support operations, not an operating-system sandbox or universal gate
over independent Project development.

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
- KANDA-managed external-Project source mutation is unsupported; Fire Shield protects only supported observer reads and KANDA-owned support/transient writes;
- independent Project-actor development does not depend on KANDA selection, registry, portable runtime, Fire Shield, Tool validators, Tool Error Memory, Tool source, or KANDA source archives;
- prompt policy cannot weaken, replace, or bypass Fire Shield programmatic enforcement inside KANDA-managed actor scope;
- generated evidence authority is structured;
- any mixed governance keeps Project source writes Project-actor-owned and Tool writes Tool-owned;
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
- Never treat Fire Shield as authorization for KANDA Reasoner to mutate external Project source.
- Never require KANDA Reasoner selection, registry, portable runtime, or Fire Shield merely because independent Project-owned IDE/terminal work changes an external Project.
- Never bypass the spectator source-write denial with another KANDA-managed mutation path.
- Never write KANDA Tool-owned code into an external Project source tree.
- Never write external Project-owned code into KANDA Tool source.
- Treat `<project_name>_show_project_to_AI` as support/evidence only, never as source or an install target.
- KANDA Reasoner Tool maintenance may write Tool source only through explicit Tool-maintenance authority; selected-Project identity never grants Project-source write authority, including self-hosting observation.
- Never create or refresh `<project>-Windows-Portable.zip` from Show Project to AI; require a separate explicit user request and productization/release workflow.

## Version history

- 2.5: made external Projects observer-only end to end: KANDA source writes are unsupported, Project release validation is Project-owned, Tool Error Memory is advisory for external Project work, and KANDA Tool source archives are never Project-development prerequisites.
- 2.4: added the actor-scope gate: Fire Shield is mandatory for KANDA-managed external-Project operations but never a prerequisite for independent Project-owned IDE, terminal, CI, install, or validation work; KANDA may observe and refresh afterward.
- 2.3: bound KANDA-managed external-Project consequential operations to the frozen Fire Shield public authority, made missing or BLOCKED Fire Shield fail closed, and prohibited prompt-only or private-reach-in bypasses.
- 2.2: made Show Project and Portable Distribution separate Box owners with no
  shared trigger, output owner, folder, lifecycle, or implicit call; portable
  identity is excluded wherever misplaced under Project source.
- 2.1: canonized portable-distribution separation: Show Project to AI never
  creates `<project>-Windows-Portable.zip`; portable builds require a separate
  explicit user request and productization/release workflow outside Project Support.
- 2.0: split compact startup bridge from the full routed owner; added stable Project identity, collision and migration decisions, typed selection and generated-evidence authority, mixed-operation write sets, transient lifecycle, security, concurrent-session, multi-root, and current-resolved-path requirements.
- 1.5: enforced Q06 identity and external Project Support behavior.
