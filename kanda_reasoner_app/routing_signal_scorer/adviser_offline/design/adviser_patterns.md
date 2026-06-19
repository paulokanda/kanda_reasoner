# Routing Signal Scorer v3 Adviser System Card Bug Bar Threat Model Design v1

Feature ID: `routing_signal_scorer_v3_adviser_system_card_bug_bar_threat_model_design_v1`

Schema version: `3.40-adviser-system-card-bug-bar-threat-model-design`

Status: design-only, standard-library-only governance reference. No candidate scorer, no machine-learning execution, no runtime router integration, no prompt auto-loading, no artifact I/O, no embeddings, no providers, and no router authority are introduced by this milestone.


## Purpose

This file names the KANDA Adviser design patterns that future patches must preserve.

## Pattern 1 - Advisory-Only Prediction

The future candidate may recommend. It may not decide.

## Pattern 2 - Abstain First

When uncertain, ambiguous, out-of-scope, or under-specified, the future Adviser must prefer ABSTAIN, AMBIGUOUS, OUT_OF_SCOPE, or UNKNOWN over unsafe action.

## Pattern 3 - Teacher-Not-Ground-Truth

Teacher answers are draft evidence until reviewed, versioned, validated, and frozen.

## Pattern 4 - Human-Reviewed Gold

Gold evidence requires human review status, provenance, schema version, teacher version, and hashes.

## Pattern 5 - Gold-Set Versioning

Gold sets must be versioned, append-only, checksummed, and traceable.

## Pattern 6 - Output Guard

Every future candidate output must pass a hard output guard before comparison, reporting, or trust.

## Pattern 7 - Severity-as-Code

Critical, high, medium, and low disagreement classes must be computed by one canonical module.

## Pattern 8 - Scratch-Only Candidate Output

Candidate outputs and disagreement reports are generated scratch evidence. They are not gold and not router authority.

## Pattern 9 - No Runtime Import

Runtime router code must not import adviser_offline, and adviser_offline must not import runtime router code.

## Pattern 10 - Red Path Dominance

Bypass, freeze, startup, prompt-library, box, authority-promotion, ambiguous, and out-of-scope safety cases dominate promotion decisions.

## Pattern 11 - Resource Budget First

Even standard-library code must have future size, runtime, and side-effect limits.

## Pattern 12 - Candidate Registry

Future candidates must be tied to candidate ID, version, code hash, gold-set version, run ID, and critical failure count.

## Deferred patterns

The following are deferred until later governed milestones:

- embeddings;
- vector indexes;
- provider calls;
- real model training;
- online learning;
- shadow mode;
- runtime integration;
- Assistant promotion;
- Copilot/Piloto authority.
