# Routing Signal Scorer v3 Adviser System Card Bug Bar Threat Model Design v1

Feature ID: `routing_signal_scorer_v3_adviser_system_card_bug_bar_threat_model_design_v1`

Schema version: `3.40-adviser-system-card-bug-bar-threat-model-design`

Status: design-only, standard-library-only governance reference. No candidate scorer, no machine-learning execution, no runtime router integration, no prompt auto-loading, no artifact I/O, no embeddings, no providers, and no router authority are introduced by this milestone.


## Purpose

This system card defines the intended and forbidden use of the future Adviser layer before any candidate scorer or comparison harness is implemented.

The Adviser is a boxed, offline, advisory-only helper for prompt-router logic. Its future job is to produce structured evidence that may help humans and deterministic governance understand whether a user request likely needs a specific prompt, context package, risk flag, or human-confirmation gate.

## Intended use

The future Adviser may eventually suggest, as advisory evidence only:

- likely governance domain;
- likely prompt group;
- likely specialist prompt;
- required context;
- missing context;
- risk flags;
- box-boundary concerns;
- freeze, patch, startup-delivery, and prompt-library governance concerns;
- whether the request resembles bypass or authority-promotion language;
- whether human confirmation is probably required;
- whether the safe output should be ABSTAIN, AMBIGUOUS, OUT_OF_SCOPE, or UNKNOWN.

## Non-use cases

The Adviser must not be used to:

- choose the final route;
- load prompts;
- change router authority;
- bypass canon;
- bypass freeze confirmation;
- write freeze memory;
- record human decisions;
- generate artifacts;
- read artifacts;
- write artifacts;
- scan source trees;
- install dependencies;
- call providers or models;
- create embeddings;
- create vector indexes;
- change startup behavior;
- change runtime behavior;
- invade neighboring boxes.

## Authority limits

Adviser output is evidence, not authority.

ML recommends. Canon/router governance decides.

Teacher answers are not ground truth until reviewed, versioned, validated, and frozen into gold evidence.

ABSTAIN, AMBIGUOUS, OUT_OF_SCOPE, and UNKNOWN must never permit action.

The future router must not consume adviser_offline output as an authoritative route decision.

## Known failure modes

The future Adviser must be designed against these failure modes:

- teacher-answer contamination;
- gold-set poisoning;
- schema drift;
- lexical negation failure;
- false fast-path on governed work;
- unsafe proceed recommendation;
- missed freeze confirmation bypass;
- missed startup-delivery bypass;
- missed prompt-library anti-audit bypass;
- missed box-boundary risk;
- authority-promotion acceptance;
- rationale overreach;
- candidate output mistaken as router authority;
- resource exhaustion from long or malformed input.

## Supported domains for future evaluation

Initial future evaluation domains are:

- freeze;
- patch;
- box;
- shield;
- startup-delivery;
- prompt-library;
- ambiguous commands;
- false-positive safety cases;
- out-of-scope cases;
- adversarial or bypass attempts.

## Unsupported in this milestone

This milestone does not implement any scorer, schema validator, output guard, severity evaluator, harness, candidate, registry, gold set, scratch writer, shadow mode, or runtime integration.

## Review expectation

Any future Adviser candidate must be tested against reviewed gold evidence, output guards, severity-as-code, and red-path cases before being trusted as helpful advisory signal.

## Promotion limit

This system card does not authorize Adviser-to-Assistant promotion. Promotion requires a later quantitative gate and explicit human approval tied to an evaluation run ID.
