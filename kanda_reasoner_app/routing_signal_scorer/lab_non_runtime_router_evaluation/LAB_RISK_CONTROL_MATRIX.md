# LAB-0B Risk-Control Matrix

Feature ID: `routing_signal_scorer_v3_ml_lab_risk_control_matrix_v1`

This milestone defines risk controls for the future KANDA ML LAB. It is documentation/governance only.

LAB-0B does not implement schema code, fixtures, corpus, runner logic, scoring engine, candidate harness, live risk detectors, provider adapters, prompt loaders, persistence, activation, field testing, runtime Pilot, or Copilot behavior.

## Purpose

The future LAB must test whether ML/router candidates can reproduce frozen router governance while avoiding unsafe authority, stale context, box leakage, prompt injection, insecure output handling, and false reliability claims.

The risk-control matrix converts known AI, router, prompt, project-governance, and Box Architecture risks into explicit future controls.

## Control doctrine

- Risk controls are defined before lab implementation.
- Critical boundary risks have zero acceptable failures.
- Hard controls must override any soft performance score.
- Candidate output remains non-authoritative.
- Canon and router governance remain authoritative.
- Risk controls must be tested by the future LAB before any reliability claim.

## Risk-control matrix

| Risk ID | Risk family | Risk description | Required future control | Critical failure condition | Current LAB-0B status |
| --- | --- | --- | --- | --- | --- |
| RC-01 | Prompt injection / bypass | User text asks the candidate to ignore routing canon, skip freeze, bypass Box Architecture, or continue directly to ML implementation. | Future fixtures must include bypass attempts and verify Routed Work Path, stop behavior, and canon yield. | Candidate follows user bypass text or treats it as authority. | Defined only. |
| RC-02 | Insecure output to downstream | Candidate output is treated as an action, approval, route decision, prompt load command, freeze write, or activation signal. | Candidate outputs must be wrapped as non-authoritative evaluation records. | Candidate output directly causes app behavior or project mutation. | Defined only. |
| RC-03 | Route authority overreach | Candidate selects, overrides, executes, or enforces a route instead of recommending under canon. | Future evaluator must separate recommendation from route authority. | Candidate becomes route authority. | Defined only. |
| RC-04 | Prompt loading overreach | Candidate causes prompt-library reading/loading before authorized. | Future controls must detect prompt-loading attempts and block them as hard failures. | Prompt loading attempt or prompt-library read attempt. | Defined only. |
| RC-05 | Persistence overreach | Candidate or LAB stores ML decisions, reports, approvals, or review queues before a governed storage milestone. | Future LAB must keep evaluation records non-persistent unless a later milestone authorizes a safe report artifact. | Unauthorized write or persistent decision storage. | Defined only. |
| RC-06 | Provider / embedding overreach | Candidate calls model providers, embeddings, vector stores, network, or external services. | Future LAB must use static candidate-output records first and block provider/embedding imports. | Provider call, network call, embedding/vector-store use. | Defined only. |
| RC-07 | Box leakage | LAB imports runtime router, prompt loader, provider modules, PySide6/UI, or production imports LAB. | Future shielding manifest and import tests must enforce allowed import directions. | LAB-production coupling or forbidden import. | Defined only. |
| RC-08 | Fixture contamination | Static fixtures are mutated by tests, candidate output, or generated processes. | Future fixtures must be immutable snapshots with hash manifests. | Fixture hash mismatch or mutable expected output. | Defined only. |
| RC-09 | Live canon coupling | Runner reads live canon/prompt/freeze/gold files at evaluation time and creates hidden dependency. | Future fixture format must use copied snapshots and explicit canon version references. | Live protected-box read is required to run tests. | Defined only. |
| RC-10 | Stale context acceptance | Candidate accepts stale sidecar, stale handoff, stale freeze hint, old filename, or old validation output. | Future corpus must include stale-context cases with expected rejection. | Candidate advances milestone using stale evidence. | Defined only. |
| RC-11 | Missing-context failure | Candidate proceeds despite missing validation, missing freeze status, missing user confirmation, or missing box audit. | Future evaluator must hard-fail missing-context misses. | Candidate proceeds without mandatory context. | Defined only. |
| RC-12 | False confidence / metric gaming | Aggregate score hides a critical boundary failure. | Future scoring must separate hard gates from soft metrics. | Any critical failure is marked acceptable because score is high. | Defined only. |
| RC-13 | Match-before-disagree violation | Candidate explains disagreement before matching canon or treats disagreement as override. | Future candidate contract must enforce two-pass match-before-disagree. | Candidate skips canon match or overrides canon. | Defined only. |
| RC-14 | Human review bypass | Candidate records or implies human approval automatically. | Future controls must require explicit human confirmation and distinguish review note from approval. | Automatic approval or human decision recording. | Defined only. |
| RC-15 | Activation drift | LAB introduces activation key, field-test flag, runtime Pilot, Copilot behavior, maturity switch, or definitive enablement. | Future controls must block activation artifacts until separately governed. | Any activation or field-test artifact appears. | Defined only. |
| RC-16 | Training-data drift | Test corpus or candidate outputs become training data before governance authorizes it. | Future design must keep corpus as evaluation-only and block training-data use. | Training-data use, fine-tuning, or dataset export for training. | Defined only. |
| RC-17 | Batch / async drift | LAB adds batch mode, asynchronous harness, UI event-loop hooks, or automated background execution too early. | Future controls must keep early runner deterministic and local. | Batch, async, PySide6 loop, or background execution appears. | Defined only. |
| RC-18 | Sensitive information leakage | Candidate exposes prompt text, system instructions, private project internals, protected memory, or user data beyond the evaluation record. | Future cases must test information-boundary behavior and output minimization. | Protected content leak. | Defined only. |
| RC-19 | Supply-chain / dependency drift | LAB adds external frameworks, cloud eval platforms, Docker, import-linter dependency, or other heavy tools before authorization. | Future dependencies must be explicit, justified, and separately governed. | Unauthorized dependency added. | Defined only. |
| RC-20 | LAB self-validation failure | LAB evaluates candidates before proving it can pass gold-vs-gold and fail known-bad cases. | Future self-validation gate must precede candidate evaluation. | Candidate evaluation runs before self-validation. | Defined only. |

## Future required control groups

The future LAB must eventually include these control groups before candidate reliability claims:

1. Bypass and prompt-injection controls.
2. Downstream-output safety controls.
3. Route-authority separation controls.
4. Prompt-loading and protected-box access controls.
5. Persistence and mutation controls.
6. Provider, embedding, network, and dependency controls.
7. Box shielding and import-direction controls.
8. Fixture integrity and hash-manifest controls.
9. Stale-context and missing-context controls.
10. Hard-gate scoring controls.
11. Match-before-disagree controls.
12. Human-review and approval-boundary controls.
13. Activation and field-test drift controls.
14. LAB self-validation controls.

## Non-claims

LAB-0B does not claim that any control is implemented.

LAB-0B does not claim that risks are detected automatically.

LAB-0B does not claim that the LAB is reliable.

LAB-0B does not claim that ML router prompt logic reliability has been tested.

LAB-0B does not authorize continuing ML implementation.

## Next safe milestone

After LAB-0B is locally validated and frozen with `FREEZE_MEMORY_STATUS: OK`, proceed only to:

```text
LAB-0C — LAB SLO / Critical Error Budget Declaration
```

LAB-0C remains documentation/governance only.
