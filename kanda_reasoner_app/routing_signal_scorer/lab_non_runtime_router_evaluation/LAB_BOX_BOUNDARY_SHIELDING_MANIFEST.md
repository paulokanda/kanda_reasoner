# LAB-1 Lab Box Boundary + Shielding Manifest

Feature ID: `routing_signal_scorer_v3_ml_lab_box_boundary_shielding_manifest_v1`

This milestone defines the box boundary and shielding rules for the future KANDA ML LAB.

LAB-1 is documentation/governance only.

LAB-1 does not implement schema code, fixtures, corpus, runner logic, scoring engine, metrics engine, candidate harness, live risk detectors, provider adapters, prompt loaders, persistence, activation, field testing, runtime Pilot, or Copilot behavior.

## Primary box

```text
kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation
```

## Box responsibility

The LAB box is responsible for non-runtime evaluation governance for future ML/router candidate testing.

The LAB box may eventually evaluate candidate output against static fixtures, but only after later governed milestones create schema, fixture, runner, self-validation, corpus, and candidate harness components.

LAB-1 itself only declares the boundary and shielding doctrine.

## Public surface allowed by LAB-1

LAB-1 exposes only Markdown documentation:

- `README.md`
- `LAB_PHASE_BOUNDARY.md`
- `LAB_CHARTER.md`
- `LAB_FORBIDDEN_BEHAVIORS.md`
- `LAB_STOP_CONDITIONS.md`
- `LAB_ALLOWED_ARTIFACTS.md`
- `LAB_SUCCESS_CRITERIA_MATRIX.md`
- `LAB_RISK_CONTROL_MATRIX.md`
- `LAB_SLO_CRITICAL_ERROR_BUDGET.md`
- `LAB_BOX_BOUNDARY_SHIELDING_MANIFEST.md`

LAB-1 exposes no Python package, no callable API, no importable LAB module, no route evaluator, no prompt selector, no candidate runner, no activation flag, and no persistent state writer.

## Private internals allowed by LAB-1

Only Markdown text and manifest metadata are allowed.

No private implementation internals exist in LAB-1.

## Boundary doctrine

The LAB box is a sealed evaluation-design box.

It must not become:

- a runtime router;
- a prompt loader;
- a prompt-library reader;
- a freeze-memory writer;
- a gold-registry writer;
- a provider adapter;
- an embedding/vector adapter;
- a UI controller;
- an activation gate;
- a field-test mode;
- a runtime Pilot;
- a Copilot.

## One-way dependency rule

Production/runtime code must not import the LAB box.

The future LAB may later read static, copied, versioned fixtures that reference canon versions, but it must not reach into live protected boxes during evaluation.

```text
production/runtime boxes  ─X→  LAB box
LAB box                  ─X→  runtime router
LAB box                  ─X→  prompt loader
LAB box                  ─X→  provider/embedding/vector/UI/activation/Copilot boxes
LAB box                  ─✓→  static frozen fixtures only, after a later governed fixture milestone
```

## Forbidden imports

Future LAB code, when separately authorized, must not import from these boxes or module families:

- runtime router modules;
- prompt loading modules;
- prompt-library active prompt readers;
- provider/model API modules;
- embedding or vector-store modules;
- PySide6, Qt, or UI controller modules;
- freeze-memory writer modules;
- gold-registry mutation modules;
- activation-gate modules;
- field-test modules;
- runtime Pilot modules;
- Copilot modules;
- background, async, scheduler, or batch execution modules.

LAB-1 creates no code that performs this enforcement. It declares the rule that later enforcement must validate.

## Forbidden writes

Future LAB code, when separately authorized, must not write to:

- prompt library;
- router canon;
- freeze memory;
- gold registry;
- routing registry;
- project source outside the LAB box;
- startup routing pack;
- activation state;
- human review approval state;
- runtime decision logs;
- persistent ML decision storage.

Any future write target must be explicitly authorized by a later governed milestone.

## Allowed future read model

Later LAB milestones may define static copied fixtures.

Allowed future read model:

```text
frozen canon reference → copied fixture snapshot → fixture hash manifest → deterministic evaluator
```

Forbidden future read model:

```text
live prompt library → evaluator
live freeze memory → evaluator
live router canon → evaluator
runtime router object → evaluator
```

The LAB should evaluate against frozen snapshots, not by reaching into live protected boxes.

## Candidate output shielding

Future ML/router candidate output must enter the LAB only as a non-authoritative evaluation record.

Candidate output must not be executable as:

- a route decision;
- a prompt loading instruction;
- an install command;
- a freeze write;
- a human approval;
- a readiness approval;
- an activation signal;
- a field-test signal;
- a runtime Pilot command;
- a Copilot instruction.

## Fixture shielding

Future fixtures must be immutable snapshots with hash references.

The fixture layer must separate:

- source canon reference;
- copied expected output;
- fixture hash;
- corpus version;
- schema version;
- review status.

Fixtures must not be confused with active prompt canon.

## Human review shielding

Future LAB reports may support human review, but must not record human approval automatically.

Human review remains outside candidate authority.

Any future human-review recording must be authorized by a separate governed milestone.

## Reliability shielding

The LAB may not claim reliability until all later gates are satisfied:

1. LAB self-validation passes.
2. Fixture integrity passes.
3. Critical boundary failures equal zero.
4. Required hard gates pass.
5. Coverage minimums are met.
6. Soft thresholds are met.
7. Human review confirms the result.
8. Freeze memory records the validation evidence.

## Future enforcement expectations

Later governed milestones should add enforcement tests for:

- no Python implementation modules before authorized milestones;
- no production import from LAB;
- no LAB import from forbidden modules;
- no writes outside authorized paths;
- no live canon/prompt/freeze/gold coupling;
- no provider/network/embedding/vector access;
- no activation, field-test, runtime Pilot, or Copilot flags;
- no executable candidate output;
- no reliability claim without LAB self-validation and zero critical failures.

LAB-1 only defines these future enforcement expectations. It does not implement import scanners, filesystem guards, or runtime monitors.

## Critical boundary link

This shielding manifest preserves the LAB-0C rule:

```text
critical_boundary_error_budget = 0
```

Box leakage, forbidden imports, forbidden writes, live canon coupling, executable candidate output, and activation drift are critical failures in future evaluation logic.

## ML implementation continuation lock

ML logic implementation remains blocked until:

```text
LAB/test fulfills its mission
→ LAB self-validation passes
→ ML router prompt logic reliability is tested
→ zero critical boundary violations are demonstrated
→ human review and freeze confirm reliability evidence
→ only then continue ML logic implementation
```

## Non-claims

LAB-1 does not enforce the shield automatically.

LAB-1 does not create import guards.

LAB-1 does not create write guards.

LAB-1 does not create fixture snapshots.

LAB-1 does not create a runner.

LAB-1 does not evaluate a candidate.

LAB-1 does not prove the LAB is reliable.

LAB-1 does not prove ML router prompt logic reliability.

LAB-1 does not authorize continuing ML implementation.

## Next safe milestone

After LAB-1 is locally validated and frozen with `FREEZE_MEMORY_STATUS: OK`, proceed only to:

```text
LAB-2 — Failure Taxonomy + Critical Violation Model
```

LAB-2 remains governed taxonomy/design work and must not create runtime authority, prompt loading, provider calls, persistence, activation, field testing, runtime Pilot, or Copilot behavior.
