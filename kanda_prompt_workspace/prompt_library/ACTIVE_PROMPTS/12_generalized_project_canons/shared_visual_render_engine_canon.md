---
prompt_id: shared_visual_render_engine_canon
prompt_code: KPR-12-013
title: Shared Visual Semantic Contract
version: 2.0.0
status: active
load_type: on_request
owner_box: 12_generalized_project_canons
classification: canonical_visual_semantics_multi_backend_contract
source_stage: prompt-audit-wave10a-final-productization-generalized-canons-closure-v1
updated_for: prompt-audit-wave10a-final-productization-generalized-canons-closure-v1
---

# Shared Visual Semantic Contract

## Purpose

Keep multiple consumers semantically consistent when they represent the same conceptual visual object or scene, while allowing compatible rendering backends.

This prompt is a bounded technical contract. It is not a persona, a source-write
authority, a release gate, or proof that implementation or validation occurred.

## When to load

- Multiple views, tools, exports, or renderers show the same conceptual object.
- Identity, geometry, selection, interaction, style meaning or export semantics can drift.
- A shared visual contract or backend adapter boundary is needed.

## When not to load

- Only static editorial artwork is involved.
- One isolated view has no shared semantic object.
- The task is generic UI styling.

## Authority boundaries

This prompt owns:

- canonical visual object identity and semantic model;
- coordinate, geometry and transform conventions;
- selection, hover, focus and interaction semantics;
- style-token meaning and state mapping;
- backend adapter and export equivalence requirements;
- visual resource lifecycle and accessibility semantics.

It delegates:

- backend implementation to Qt/QML/web/SVG/other owners;
- editorial help artwork to KPR-12-010;
- domain meaning to the domain owner;
- security/privacy of rendered data to KPR-09-014.

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

- visual object IDs and canonical data model;
- coordinate systems, units, transforms and precision;
- consumer/backends and supported interactions;
- accessibility and reduced-motion/contrast requirements;
- snapshot, semantic or visual-inspection evidence.

## Governing rules

- Require one canonical visual semantic contract, not necessarily one physical rendering engine.
- Use stable visual IDs across views, selections, exports and persisted state.
- Define coordinate spaces, origin, orientation, units, transforms and clipping explicitly.
- Backend adapters may differ internally but must preserve declared semantic states and interactions.
- Accessibility semantics, keyboard behavior, focus, text alternatives and contrast must be part of the contract.
- Manage resource creation/disposal and stale async render results explicitly.
- Do not claim pixel or semantic equivalence without current evidence appropriate to the backends.

## Validation obligations

For implemented work, require the smallest applicable deterministic checks,
negative or failure-path coverage when risk is material, current-source evidence,
and rollback or reversal evidence. Use `NOT_RUN`, `BLOCKED`, or `INCONCLUSIVE`
when that is the truthful state.

## Required output

Return a `SHARED VISUAL SEMANTIC CONTRACT RECORD` containing:

- canonical visual model and IDs;
- coordinate/geometry/style semantics;
- interaction/accessibility states;
- backend adapter boundaries;
- export and resource lifecycle;
- semantic/snapshot/visual evidence.

- unresolved assumptions and risks;
- specialist handoffs;
- source-write authorization: `NO` unless separately granted by Brick Wall.

## Version history

- 2.0.0: replaced single-engine dogma with one semantic contract plus compatible backends and added identity, accessibility, interaction, lifecycle, and evidence rules.
