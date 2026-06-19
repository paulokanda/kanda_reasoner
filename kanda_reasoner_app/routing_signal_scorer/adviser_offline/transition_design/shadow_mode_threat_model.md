# Routing Signal Scorer v3 Shadow Mode Boundary Threat Model

## Scope

This document belongs to M18 - Shadow Mode Boundary Design v1.

M18 is secure design only. It does not implement shadow mode, observation
execution, report writing, persistence, monitoring, kill switch behavior,
Auxiliar/Assistant behavior, or runtime integration.

## Protected doctrine

ML recommends. Canon/router governance decides.

Shadow evidence is not authority. Shadow evidence must not become a route,
prompt-loading action, freeze action, gold mutation, registry mutation,
candidate promotion, or Auxiliar/Assistant behavior.

## Critical boundary error budget

Critical boundary error budget: zero.

Any critical boundary issue blocks progression to M19.

## Critical threat classes

1. Evidence becomes authority.
2. Shadow boundary imports runtime router code.
3. Runtime router imports shadow boundary code.
4. Shadow boundary loads prompts.
5. Shadow boundary reads files or writes files.
6. Shadow boundary creates logs or reports.
7. Shadow boundary mutates gold, registry, freeze memory, or startup files.
8. Shadow boundary calls providers, models, embeddings, or vector indexes.
9. Shadow boundary uses network, subprocess, dynamic import, or code evaluation.
10. Shadow boundary introduces Auxiliar/Assistant behavior.

## Input contamination risk

M18 accepts no routing case input. Future milestones must allow only caller
supplied serialized primitive data and must reject live runtime objects, file
handles, prompt objects, router objects, and mutable external state.

## Output overtrust risk

M18 must avoid confidence, score, probability, readiness, promotion, and forward
motion language. Future outputs must remain non-authority evidence.

## Hidden coupling risk

M18 must be enforced by static tests that scan imports and calls. The boundary
is not a runtime fence by itself. The safety value comes from small scope,
immutability, no side effects, and executable import-boundary tests.

## Future kill-switch and monitoring requirement

Kill switch and monitoring are not implemented in M18. They are future
requirements before any real runtime shadow operation can be considered.

## M18 progression rule

Proceed to M19 only after M18 is installed, validated, frozen, startup freeze
context is refreshed, and freeze memory status is OK.
