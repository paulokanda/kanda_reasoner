---
prompt_id: desktop_help_document_layout_canon
prompt_code: KPR-12-010
title: KANDA Desktop Help Document Layout Profile
version: 2.0.0
status: active
load_type: on_request
owner_box: 12_generalized_project_canons
classification: project_specific_desktop_help_content_layout_overlay
source_stage: prompt-audit-wave10a-final-productization-generalized-canons-closure-v1
updated_for: prompt-audit-wave10a-final-productization-generalized-canons-closure-v1
---

# KANDA Desktop Help Document Layout Profile

## Purpose

Define the optional KANDA desktop-help content, layout, artwork, offline-rendering, accessibility, and source-to-rendered profile without presenting it as a universal documentation canon.

This prompt is a bounded technical contract. It is not a persona, a source-write
authority, a release gate, or proof that implementation or validation occurred.

## When to load

- The KANDA desktop help system is being authored or reviewed.
- Another application explicitly adopts this help profile.
- Help source/rendered output, local assets, accessibility or visual QA is central.

## When not to load

- Generic Python documentation architecture is the task; use KPR-09-011.
- A runtime visual scene shared across tools is central; use KPR-12-013.
- The application has not adopted the KANDA help profile.

## Authority boundaries

This prompt owns:

- KANDA help-page structure and optional visual identity;
- help source-versus-rendered artifact distinction;
- offline local-asset policy and manifest integrity;
- artwork provenance and editorial placement;
- help-specific accessibility, responsive layout and visual inspection criteria.

It delegates:

- technical documentation accuracy and freshness to KPR-09-011;
- runtime visual semantic consistency to KPR-12-013;
- privacy/security of examples and assets to KPR-09-014;
- renderer implementation to the current application owner.

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

- adopted help profile and target audience;
- canonical source and generated output locations;
- renderer and fallback behavior;
- asset manifest, provenance and licensing;
- accessibility and viewport/overflow inspection evidence.

## Governing rules

- Treat colors, cartoons, analogies, illustration counts and book references as profile choices, not universal mandates.
- Keep canonical help source distinct from generated HTML or rendered caches.
- Use local or explicitly approved resources; do not introduce remote tracking or hidden network dependencies.
- Provide semantic headings, keyboard access, focus visibility, text alternatives, readable contrast and scalable layout.
- Do not claim visual quality or no-overflow without current rendered inspection evidence.
- Do not store backup snapshots inside ACTIVE_PROMPTS.
- Bind every generated help artifact to source/version/asset-manifest provenance.

## Validation obligations

For implemented work, require the smallest applicable deterministic checks,
negative or failure-path coverage when risk is material, current-source evidence,
and rollback or reversal evidence. Use `NOT_RUN`, `BLOCKED`, or `INCONCLUSIVE`
when that is the truthful state.

## Required output

Return a `DESKTOP HELP PROFILE RECORD` containing:

- profile/adoption and audience;
- source/rendered/asset identities;
- page and optional artwork structure;
- accessibility/localization/responsive requirements;
- privacy/copyright/provenance controls;
- rendered inspection and freshness evidence.

- unresolved assumptions and risks;
- specialist handoffs;
- source-write authorization: `NO` unless separately granted by Brick Wall.

## Version history

- 2.0.0: reclassified the KANDA-specific design system as an optional project overlay and added accessibility, provenance, offline, and truthful visual-review boundaries.
