# Routing Signal Scorer v3 Adviser Candidate v0 Offline Lexical Scorer Design v1

Feature ID: `routing_signal_scorer_v3_adviser_candidate_v0_offline_lexical_scorer_design_v1`  
Schema version: `3.51-adviser-candidate-v0-offline-lexical-scorer-design`  
Status: `design_only_not_implemented`

## Purpose

M10 defines the boundary for the future **Adviser Candidate v0 offline lexical scorer**. It is the first step toward a measurable candidate, but it is not the candidate implementation.

The purpose is to make the future M11 implementation intentionally boring, local, deterministic, and testable.

## Roadmap position

The Adviser roadmap has now completed the safety foundation needed before any candidate exists:

1. M0-M4: Adviser foundations, schema family, guard, severity, and resource limits.
2. M5-M6: pure comparison harness plus supplied-record manifest/registry helpers.
3. M7-M9C: seed cases, draft teacher answers, human review, and a static offline seed gold set.
4. M10: design the first candidate boundary.
5. M11: only later, implement the offline lexical baseline candidate.

## Authority boundary

The future Candidate v0 may produce an **advisory candidate answer** only. It must never produce router authority.

The candidate must not decide:

- final route;
- required prompts as authority;
- whether work may proceed;
- whether a freeze is valid;
- whether prompt-loading should happen;
- whether runtime behavior should change.

Any future candidate output must be treated as untrusted evidence. It must pass:

- the Adviser candidate answer schema;
- the output guard;
- resource limits;
- severity evaluation;
- pure comparison harness evaluation against reviewed gold cases.

## Allowed future algorithm shape

Candidate v0 is intentionally lexical and deterministic:

1. Normalize caller-supplied `input_text` only.
2. Match fixed phrase families and negative/bypass patterns.
3. Produce a schema-shaped advisory candidate answer.
4. Prefer `ABSTAIN` when multiple high-risk meanings conflict.
5. Prefer `OUT_OF_SCOPE` for non-project requests.
6. Never return unconditional `YES`, `AUTO_PROCEED`, or router authority.

No model call is allowed. No embedding is allowed. No vector index is allowed. No provider is allowed. No router authority is allowed.

## Planned lexical families

The future M11 implementation may define static phrase families for:

- freeze workflow;
- patch delivery;
- box boundary;
- startup delivery;
- prompt-library authoring and audit;
- routing-signal-scorer / Adviser milestone requests;
- adversarial bypass attempts;
- ambiguous short commands;
- false-positive explanation-only cases;
- out-of-scope requests.

## Priority rule

If implemented later, the candidate should apply this conservative priority:

```text
critical bypass / authority promotion
> runtime/provider/embedding/dependency/source-scan request
> freeze confirmation or freeze bypass risk
> cross-box or runtime import risk
> patch delivery / manual overwrite risk
> startup delivery and prompt auto-loading risk
> prompt-library anti-audit risk
> Adviser milestone request
> ambiguous short command
> out of scope
> explanation-only false positive
```

The exact implementation remains a separate governed patch.

## Explicitly forbidden in M10

M10 must not add:

- candidate module implementation;
- candidate output files;
- candidate output generation;
- ML execution;
- dependency installation;
- file reading logic;
- source scanning;
- prompt auto-loading;
- artifact reading or writing;
- embeddings or vector indexes;
- provider calls;
- runtime integration;
- router authority;
- public runtime export.

## Required future M11 guardrail

Before M11 is allowed, M10 must remain frozen and M11 must prove:

- standard-library-only implementation;
- pure function over supplied strings/dicts only;
- no filesystem, network, environment, subprocess, importlib, glob, pathlib scans, prompt loader, provider, embedding, vector, runtime router, or startup integration;
- output validated by M3/M4 guard and resource modules;
- comparison against the M9C seed gold set is separate and offline.

## Non-goals

This design does not tune, train, calibrate, learn, embed, retrieve, or select prompts at runtime. It only defines the allowed envelope for a future lexical baseline.
