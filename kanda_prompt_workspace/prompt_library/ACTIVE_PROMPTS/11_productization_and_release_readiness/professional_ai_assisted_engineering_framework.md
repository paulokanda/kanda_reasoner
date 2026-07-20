---
prompt_id: professional_ai_assisted_engineering_framework
prompt_code: KPR-11-003
title: AI-Assisted Engineering Operating Model Overview
version: 2.0.0
status: active
load_type: on_request
owner_box: 11_productization_and_release_readiness
classification: thin_non_authoritative_human_ai_operating_model_overview
source_stage: prompt-audit-wave10a-final-productization-generalized-canons-closure-v1
updated_for: prompt-audit-wave10a-final-productization-generalized-canons-closure-v1
---

# AI-Assisted Engineering Operating Model Overview

## Purpose

Provide a concise map of human responsibility, AI responsibility, work states, evidence discipline, and dispatch to current specialist owners.

This prompt is a bounded technical contract. It is not a persona, a source-write
authority, a release gate, or proof that implementation or validation occurred.

## When to load

- The user asks how the human and AI should divide responsibilities.
- A concise orientation to the current governed engineering workflow is useful.
- A task needs the high-level work-state model before specialist routing.

## When not to load

- A current specialist already owns the technical decision.
- The prompt would be used as a master implementation, patch, validation, or freeze authority.
- A historical KANDA roadmap is being treated as current project truth.

## Authority boundaries

This prompt owns:

- human-versus-AI responsibility overview;
- high-level work states and evidence expectations;
- specialist-dispatch orientation;
- non-authorization and uncertainty rules.

It delegates:

- session initialization to current Class 01 owners;
- routing to Class 02;
- box ownership to Class 04;
- implementation authorization to Brick Wall;
- delivery/validation to Class 05;
- technical decisions to the exact current specialist;
- freeze and Error Memory to their current owners.

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

- the user objective and decision authority;
- current task state and exact project identity;
- available source/evidence and material gaps;
- the current prompt navigation index.

## Governing rules

- The human sets goals, priorities, acceptance decisions, and explicit approvals.
- The AI inspects evidence, proposes bounded options, implements only when authorized, validates honestly, and reports uncertainty.
- Do not copy specialist rules into this overview.
- Do not claim current source access, execution, PASS, installation, or freeze without observed evidence.
- Route to the smallest current owner rather than loading a universal stack.
- A historical book or framework is advisory and never overrides current project governance.

## Validation obligations

For implemented work, require the smallest applicable deterministic checks,
negative or failure-path coverage when risk is material, current-source evidence,
and rollback or reversal evidence. Use `NOT_RUN`, `BLOCKED`, or `INCONCLUSIVE`
when that is the truthful state.

## Required output

Return a `AI-ASSISTED ENGINEERING OPERATING MODEL` containing:

- human responsibilities;
- AI responsibilities;
- current work state;
- evidence available and missing;
- selected specialist routes;
- approval or blocker state.

- unresolved assumptions and risks;
- specialist handoffs;
- source-write authorization: `NO` unless separately granted by Brick Wall.

## Version history

- 2.0.0: replaced the 544-line mega-framework with a thin, non-authoritative operating-model and dispatch overview.
