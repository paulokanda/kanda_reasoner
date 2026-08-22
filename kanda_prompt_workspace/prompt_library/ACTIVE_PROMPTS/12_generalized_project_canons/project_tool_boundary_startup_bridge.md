---
prompt_code: KPR-12-006
prompt_id: project_tool_boundary_startup_bridge
title: Project Tool Boundary Startup Bridge
version: 2.6
status: active
load_type: always_startup
owner_box: 12_generalized_project_canons
---

# Project Tool Boundary Startup Bridge

## Mission

Keep reusable KANDA Reasoner Tool ownership separate from the selected Project,
its durable Project Support, and its non-authoritative transient workspace.
Prevent a Project release from being built, installed, validated, frozen, or
memorized against the Tool root by mistake.

This bridge is startup context only. Full authority remains with
`KPR-12-001 project_tool_boundary_canon`.

## Four identities

```text
tool_source_root = reusable KANDA Reasoner source and canonical prompt library
active_project_root = selected project source and install/validation target
active_project_support_root = external durable support for the selected project
transient_workspace_root = disposable selected-project staging and diagnostics
```

## Absolute code-placement guard

For build, update, regression, installation, validation, Freeze, Error Memory,
and packaging work:

```text
Never write KANDA Tool-owned code into an external selected Project source tree.
Never write external selected-Project code into KANDA Tool source.
```

Project Support is not a source-mutation exception.
`<project_drive>/<project_name>_show_project_to_AI` may contain selected-Project
source copies and KANDA-generated handoff, prompt, manifest, evidence, Freeze,
and Error Memory evidence/export files required for AI-assisted work. It remains
support, not source, runtime, install target, or the canonical Error Memory lesson
store.

<!-- KANDA_CORRECTION:spectator_self_hosting_source_write_inversion:s7a_v1 -->

## Self-hosting role separation

KANDA Reasoner self-hosting may make the Tool source root and selected Project
source root resolve to the same physical directory. Physical equality never
merges their logical roles and never grants Project-source mutation authority to
KANDA.

For every KANDA-managed Project operation, including explicit self-hosting:

```text
KANDA-managed PROJECT_SOURCE_READ: ALLOWED
KANDA-managed PROJECT_SOURCE_WRITE: DENIED
Project selection grants source-write authority: NO
same physical Tool/Project root grants source-write authority: NO
```

An explicitly invoked KANDA Tool-maintenance/install operation may update KANDA
Reasoner Tool source under its own Tool-maintenance contract. That authority is
independent of Project selection and must not be represented as
`PROJECT_SOURCE_WRITE`. Selecting `kanda_reasoner` as the observed Project is
useful for provenance, validation targeting, support ownership, and evidence;
it is not a write-authority switch.

Independent Project-owned IDE, terminal, interpreter, CI, or installation work
may modify that Project under its own authority. KANDA remains a spectator and
may refresh evidence afterward.

## Cross-project release ownership

For a selected external Project:

```text
Project source observation     = active_project_root
KANDA Project source read      = allowed
KANDA Project source write     = denied
Project patch/install actor    = independent Project-owned workflow
Project release validator      = Project-owned or release-local
KANDA Tool patch validator     = NOT_APPLICABLE to external Project releases
KANDA Tool source archive      = NOT_REQUIRED for Project development
Tool Error Memory              = advisory when available, never a Project blocker
live validator target          = active_project_root
project interpreter owner      = active Project handoff or validator contract
ZIP staging and extraction     = transient_workspace_root
Freeze intake and memory       = active_project_support_root
Error Memory canonical store   = Tool-owned Error Memory runtime
Error Memory Project relevance = context/evidence only
canonical routine prompt       = tool_source_root
Show Project / Freeze / Error UI= KANDA Reasoner Tool
```

A patch may target the active Project for later independent installation, but
KANDA Project selection does not authorize KANDA to apply that patch to Project
source. KANDA Reasoner creating the handoff or providing the UI does not make it
the Project being changed.

Project Support may contain Error Memory evidence or exported context needed for
AI-assisted work, but it is not the canonical owner of reusable Error Memory
lessons.

## Fire Shield startup gate

First classify the actor.

If KANDA Reasoner reads an external Project or writes KANDA-owned Project Support
or transient evidence, use the public observer authority and Fire Shield where
that supported operation requires it. KANDA-managed `PROJECT_SOURCE_WRITE` is
unsupported and must never become allowed because Fire Shield passes.

If the Project is edited, installed, tested, executed, validated, released, or
rolled back through its own IDE, terminal, interpreter, CI, or Project-owned
delivery package, KANDA Reasoner is a spectator. Do not require KANDA Project
selection, registry state, portable runtime, Fire Shield, Tool interpreter, GUI,
Tool validator, Tool Error Memory, Tool source, or KANDA source archive. Use the
Project's own root, write-set, fingerprint, interpreter, validation, release, and
rollback contracts. KANDA may re-scan or refresh evidence afterward.

Never use `_project_fire_shield_*`. Prompt approval cannot bypass the spectator
source-write denial. Path equality alone never grants self-hosting.

KANDA Tool-maintenance authority is explicit Tool-operation authority and is
never derived from selected-Project identity, self-hosting mode, or path equality.

Fire Shield is application-level protection for KANDA-managed operations, not an
OS sandbox or universal authority over independent Project development.

## Portable-distribution separation

```text
Show Project to AI output = handoff, manifests, source parts, PNG parts, and Error Memory export
Portable distribution = <project>-Windows-Portable.zip
Portable build owner = separate productization/release workflow
Portable build trigger = explicit user request only
Portable build destination = outside active_project_support_root
```

Show Project to AI and Portable Distribution are different Boxes. They must
never share a trigger, output owner, output folder, lifecycle, or implicit call.
Show Project to AI must never create, refresh, publish, move, delete, or
implicitly request a portable distribution. An existing or misplaced portable
ZIP is excluded from source and recorded as generated evidence wherever it is
found under the selected Project. Creating a portable build requires a separate
user request and independently routed release workflow.

## Routine-button identity rule

The `Answer, Validate, Freeze, Memorize Error` button must copy a resolved
context envelope containing selected Project root, Tool root, Project Support
root, transient root, and same-physical-root status before the canonical routine
prompt. The AI must use those values and must not ask the user to retrain it.

## Selected Project feature handling checklist

For every feature that KANDA Reasoner creates, corrects, validates, freezes, or
memorizes for the selected Project, confirm all items before consequential
output:

```text
[ ] Selected Project ID and root are current and explicit.
[ ] Tool root, Project Support root, transient root, and self-hosting state are explicit.
[ ] Operation is classified as PROJECT_OPERATION, TOOL_CHANGE, MIXED_GOVERNED, or BLOCKED.
[ ] KANDA-managed PROJECT_SOURCE_WRITE is denied, including explicit self-hosting and same-root observation.
[ ] Any source mutation is owned by an explicit Tool-maintenance/install operation or an independent Project-owned actor, never by Project selection.
[ ] One feature ID, owner Box, exact source set, and current fingerprints are recorded.
[ ] KANDA Tool source remains read-only unless a separate Tool defect is proven and authorized.
[ ] No Tool-owned code is placed in an external Project source and no external Project-owned code is placed in Tool source.
[ ] Project Support copies are non-source evidence, or the selected Project is proven KANDA Reasoner self-hosting.
[ ] Patch payload, install destination, live validator, and release contract belong to the selected Project; KANDA Tool validator/source are not fallbacks.
[ ] ZIP staging and extraction belong only to the selected Project transient workspace.
[ ] Project validation/freeze evidence and Project Freeze Memory belong to Project Support; reusable Tool Error Memory remains Tool-owned and advisory for external Project work.
[ ] Installation and validation remain separate, using the selected Project interpreter.
[ ] Memorize Error and Freeze Confirm and Write remain explicit human actions.
[ ] Handoff and startup context are refreshed after governed source or memory changes.
[ ] Work continues from the last reliable marker without repeating completed phases.
[ ] No feature is merged into KANDA Tool, another Project, generated evidence, or transient staging.
[ ] Portable distribution remains a separate explicit productization workflow.
```

Any unresolved item blocks mutation and operational artifact output.

## Hard rules

- Never collapse logical Tool and Project roles. Same-root self-hosting does not merge authority.
- KANDA-managed Project source writes are denied for external and self-hosted Projects.
- Never write Tool-owned code into an external Project source tree or external Project-owned code into Tool source.
- Project Support handoffs are non-source evidence copies, never source-mutation exceptions.
- Patch payloads may target Project source for an independent Project-owned installer, but KANDA Project selection does not authorize applying them.
- Reusable Tool writes target the Tool only through an independently verified and authorized Tool-maintenance/install operation; that authority is not Project authority.
- Never patch the Tool merely because an external Project package, validator,
  Freeze intake, or Error Memory intake is incomplete.
- KANDA-managed Project Support remains external to Project source.
- The transient workspace owns no source truth, validation truth, Freeze memory,
  or Error Memory.
- Generated handoffs and archives are evidence, not source authority.
- Installation is not validation.
- Use the selected Project interpreter or its resolution owner; do not assume
  generic `python` when a governed interpreter is known.
- Preview is read-only. Frozen memory requires explicit human Confirm and Write.
- Error Memory requires duplicate review, current-schema validation, and explicit
  human Memorize Error.
- A missing, stale, ambiguous, or wrong-root identity blocks mutation and
  operational artifact output.
- KANDA-managed external-Project source mutation is unsupported. Fire Shield may protect supported observer/support operations but never grants Project source-write authority.
- Independent Project-owned IDE, terminal, CI, install, validation, and release work must not depend on KANDA selection, registry, runtime, Fire Shield, Tool interpreter, GUI, KANDA validator, Tool Error Memory, Tool source, or KANDA source archives.
- If exact source for Project P is needed, request only Project P source/current archive; never request KANDA source archives unless KANDA Reasoner itself is the Project being repaired.

## Route to the full canon

Load `KPR-12-001 project_tool_boundary_canon` before coding, patching, ZIP
release, installation instructions, live validation, Freeze, Error Memory,
handoff generation, root migration, mixed Tool/Project writes, or any operation
whose owner or target is not proven.

Startup bridge decision:

```text
Selected Project identity clear: YES / NO
Tool identity clear: YES / NO
Project Support and transient roots derived from selected Project: YES / NO
Wrong-root risk: YES / NO
Full KPR-12-001 required: YES / NO
May mutate from this bridge alone: NO
```

## Version history

- 2.6: made external Project implementation and release fully KANDA-independent, scoped KANDA patch validation to Tool releases, made Tool Error Memory advisory for Project actors, and added the same-project source-archive provider rule.
- 2.5 + S7A corrective migration: preserves actor-scope separation and supersedes
  the earlier self-hosting Project-source mutation allowance. Same-root selection
  remains useful observation context but never grants KANDA-managed
  `PROJECT_SOURCE_WRITE`; Tool maintenance is separate explicit Tool-operation
  authority.
- 2.5: added actor-scope separation: KANDA Reasoner is spectator-only for independent external-Project IDE/terminal development, while Fire Shield remains mandatory only when KANDA itself is the actor touching the external Project.
- 2.4 + self-hosting mutation addendum v1: historical and superseded by the S7A
  corrective migration above. It previously described a same-root mutation
  allowance and must not be treated as current authority.
- 2.4: added the always-startup Fire Shield gate for external-Project consequential work, including public-surface-only use and fail-closed no-fallback behavior.
- 2.3: added the selected-Project feature handling checklist covering identity,
  owner classification, exact source, patch/install/validation targets, Project
  Support, Error Memory, Freeze, continuation state, and no-merge rules.
- 2.2: made Box Logic explicit: Show Project and Portable Distribution must
  never share triggers, output ownership, folders, lifecycle, or implicit calls;
  portable identity is excluded wherever misplaced under Project source.
- 2.1: canonized that portable builds are separate, explicit-user-requested
  release work outside Project Support, never Show Project output.
- 2.0: added cross-project release ownership and the resolved routine-button
  identity envelope after the EEG Kanda Tool-versus-Project failure.
- 1.0: initial compact boundary bridge.
