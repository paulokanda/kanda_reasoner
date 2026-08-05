---
prompt_code: KPR-12-006
prompt_id: project_tool_boundary_startup_bridge
title: Project Tool Boundary Startup Bridge
version: 2.3
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

Only these bounded cases are exceptions:

1. `<project_drive>/<project_name>_show_project_to_AI` may contain the selected
   Project source copies and KANDA-generated handoff, prompt, manifest, evidence,
   Freeze, and Error Memory files required for AI-assisted work. It is support,
   not source, runtime, or an install target.
2. When the selected Project is KANDA Reasoner itself and canonical resolution
   proves the Tool and Project source root are the same owner root, both roles may
   physically write that same tree. Logical ownership, exact write sets,
   validation, and rollback remain mandatory.

A mixed governed operation may touch both separate roots only with owner-pure
write sets. It never permits one owner's code to be installed into the other.

## Cross-project release ownership

For a selected external Project:

```text
patch payload owner            = active_project_root
install destination            = active_project_root
live validator target          = active_project_root
project interpreter owner      = active Project handoff or validator contract
ZIP staging and extraction     = transient_workspace_root
Freeze intake and memory       = active_project_support_root
Error Memory intake and lessons= active_project_support_root
canonical routine prompt       = tool_source_root
Show Project / Freeze / Error UI= KANDA Reasoner Tool
```

KANDA Reasoner creating the handoff or providing the UI does not make it the
Project being changed.

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
[ ] One feature ID, owner Box, exact source set, and current fingerprints are recorded.
[ ] KANDA Tool source remains read-only unless a separate Tool defect is proven and authorized.
[ ] No Tool-owned code is placed in an external Project source and no external Project-owned code is placed in Tool source.
[ ] Project Support copies are non-source evidence, or the selected Project is proven KANDA Reasoner self-hosting.
[ ] Patch payload, install destination, and live validator target belong to the selected Project.
[ ] ZIP staging and extraction belong only to the selected Project transient workspace.
[ ] Project-specific evidence, Error Memory, and Freeze Memory belong only to Project Support.
[ ] Installation and validation remain separate, using the selected Project interpreter.
[ ] Memorize Error and Freeze Confirm and Write remain explicit human actions.
[ ] Handoff and startup context are refreshed after governed source or memory changes.
[ ] Work continues from the last reliable marker without repeating completed phases.
[ ] No feature is merged into KANDA Tool, another Project, generated evidence, or transient staging.
[ ] Portable distribution remains a separate explicit productization workflow.
```

Any unresolved item blocks mutation and operational artifact output.

## Hard rules

- Never collapse Tool and Project ownership, including self-hosting.
- Never write Tool-owned code into an external Project source tree or external Project-owned code into Tool source.
- The only physical-content exceptions are non-authoritative Project Support handoffs and proven KANDA Reasoner self-hosting.
- Project source writes, ZIP payloads, installation, and live validation target
  the selected Project owner.
- Reusable Tool writes target the Tool only for an independently verified and
  authorized Tool defect.
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
