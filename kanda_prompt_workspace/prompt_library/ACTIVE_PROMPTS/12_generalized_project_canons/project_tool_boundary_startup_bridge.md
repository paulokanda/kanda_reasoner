---
prompt_code: KPR-12-006
prompt_id: project_tool_boundary_startup_bridge
title: Project Tool Boundary Startup Bridge
version: 1.0
status: active
load_type: always_startup
owner_box: 12_generalized_project_canons
---

# Project Tool Boundary Startup Bridge

## Mission

Keep Tool identity, selected Project identity, durable Project Support, and the non-authoritative transient workspace separate before consequential work begins.

This bridge is startup context only. It is not a second boundary canon. The full owner is `KPR-12-001 project_tool_boundary_canon`.

## Four identities

```text
tool_source_root = reusable KANDA Reasoner source
active_project_root = selected project source
active_project_support_root = external durable support for that project
transient_workspace_root = disposable project-linked staging and diagnostics
```

## Hard rules

- Never collapse Tool and Project ownership, including self-hosting when the resolved roots are equal.
- Project source writes target the selected Project owner; reusable Tool writes target the Tool owner.
- KANDA-managed Project Support must remain external to Project source.
- The transient workspace is non-authoritative and must not own source truth, Preview truth, validation truth, Error Memory, or Freeze Memory.
- Generated handoffs and archives are evidence, not source authority.
- A missing, stale, ambiguous, or wrong-root identity blocks mutation.
- Preview remains read-only; frozen memory requires explicit human Confirm and Write.

## Route to the full canon

Load `KPR-12-001 project_tool_boundary_canon` before coding, patching, validation, freeze, handoff generation, root migration, mixed Tool/Project writes, cross-project access, or any operation whose owner or write target is not already proven.

Startup bridge decision:

```text
Boundary identity clear: YES / NO
Wrong-root risk: YES / NO
Full KPR-12-001 required: YES / NO
May mutate from this bridge alone: NO
```
