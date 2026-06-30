# Large Module Refactor Template

## Box Logic Requirement

Before any implementation, repair, refactor, prompt update, governance update, or bundle creation, the AI must:

- Identify the active box before implementation.
- State owner paths.
- State files allowed to change.
- State files explicitly out of scope.
- Declare cross-box touches.
- Preserve public contracts.
- Validate the active box and any touched external box.

Version: 3.2.0
Status: Reusable large-module refactor template aligned with Large Module Creation and Refactor Protocol v7.2, including AST-assisted heuristic split audit, safe multi-island batch patch mode, sequential double-refactor delivery trains, practical helper-file granularity, and normal `.py` source-file ownership.
Use: Load only when a file is above 500 lines, would exceed 500 lines, has high complexity, has too many responsibilities, or helper splitting is required.

## Purpose

Safely split large modules into a stable public facade plus responsibility-specific helper files without changing behavior, breaking imports, or weakening validation.

## Project-Agnostic Contract

Required variables:

```text
<PROJECT_ROOT>
<PROJECT_NAME>
<PRODUCT_PACKAGE>
<TASK_DESCRIPTION>
<TASK_SLUG>
<GOVERNANCE_FOLDER>
<VALIDATION_COMMANDS>
<OUTPUT_FOLDER>
<SOURCE_FILES>
<LOG_FILES>
```

Rules:

- Do not hardcode one project root.
- Do not assume one product package.
- Do not treat examples as active project truth.
- Use current source files, logs, audit output, and validation output as evidence.
- If evidence is missing, request it before implementation unless the user explicitly authorized best-effort continuation.
- For KANDA/PyArchitect governed patch work, keep transient install, extract, correction, audit, and validation-helper files under `<drive>/<project>_delete_after_daily_work`.

## Approval Gates

Task 0: audit only, then stop for approval.
Task 1: roadmap and decomposition only, then stop for approval.
Task 2: implementation per cluster only after approval; validate after each cluster.
Final: local validation evidence before freeze.

## Task 0 Audit

Report:

- line count and complexity trigger;
- import graph and import compatibility risks;
- dependency-direction map from facade to helpers to low-level pure modules;
- public API inventory, including `__all__` and consumers;
- `__init__.py` re-export need if converting module to package;
- tests available and characterization tests needed;
- classes, functions, constants, side effects, and responsibilities;
- GUI signal/widget inventory when the target touches GUI code;
- blind spots such as dynamic imports, monkey-patching, runtime code generation, GUI signal binding, and generated-file references;
- AST-assisted split audit evidence when available: method line spans, called self methods, self attributes read/written, imports used, GUI symbols, side effects, candidate islands, risk, and independence matrix;
- speed-mode assessment: narrow, wide responsibility-island, source-preserving facade, or defer;
- candidate-island queue at module start;
- independence matrix for possible multi-island batch patches.

## Task 1 Roadmap

Define:

- target structure;
- helper files with responsibility-based names;
- practical helper-file size/cohesion plan, avoiding unnecessary micro-files;
- normal `.py` source-file ownership plan, avoiding runtime logic hidden in ZIP payload/delivery structures;
- public API preservation plan;
- `__init__.py` re-export strategy;
- `__all__` strategy for facade and helpers;
- import compatibility matrix;
- phased migration plan, one responsibility cluster or one approved independent pair at a time;
- validation plan, including tiered fast/medium/full gates;
- Refactor Island Manifest for any wide-mode extraction;
- Batch Island Manifest for any two-island batch patch;
- expected architecture-warning impact;
- rollback plan, including whole-ZIP rollback and per-island rollback when clean;
- delivery ZIP contents;
- patch-train delivery plan when several separate governed patches will be packaged together in one outer bundle.

## Sequential double-refactor delivery train v7.2

Use this only when several governed refactor patches are prepared together from one clean roadmap.

```text
Patch ZIP 1: slice A1 + optional related slice A2 -> install -> validate -> freeze
Patch ZIP 2: slice B1 + optional related slice B2 -> install -> validate -> freeze
Patch ZIP 3: slice C1 + optional related slice C2 -> install -> validate -> freeze
Patch ZIP 4: slice D1 + optional related slice D2 -> install -> validate -> freeze
```

Rules:

- Maximum per response: 4 ordered patch ZIPs.
- Default maximum per ZIP: 2 related refactor slices.
- Do not create more train cars or helper files once remaining modules are cohesive and below the 400-line ideal; use a completion guard instead.
- Each ZIP has its own feature id, install, validate, ZIP contract check, freeze code, freeze hint, and freeze entry.
- Freeze Patch 1 before Patch 2; freeze Patch 2 before Patch 3; freeze Patch 3 before Patch 4.
- Stop the train immediately if any patch fails install, validation, ZIP contract, freeze-prep, preview, or freeze.
- Do not freeze the train as one outer bundle.

## Task 2 Implementation

Move logic by responsibility only.

Rules:

- preserve public API;
- keep first-pass consumers on public facade/origin imports unless API migration is explicitly approved;
- move whole functions, whole classes, or whole methods only;
- avoid circular imports;
- avoid catch-all helper files;
- avoid micro-files created only to chase a line-count target; cohesive helpers around 250-400 lines are acceptable;
- use ordinary importable `.py` files for runtime/source logic, not ZIP payload files or delivery-package structures;
- add characterization tests before moving insufficiently tested behavior;
- validate after every cluster;
- do not mix behavior changes into refactor;
- use optional tools such as AST split audit, Ruff, pytest coverage, pytest-xdist, LibCST codemods, Rope, modguard, pyrefact, wily, or radon only when already configured or explicitly approved;
- do not run codemods against real source before fixture verification;
- do not skip validation gates because a tool performed the move or audit.

## AST-assisted Heuristic Split Audit

At module start, run or request the read-only AST split audit tool when available. Use it to produce a candidate-island queue and pairwise independence matrix before deciding patch shape.

The audit should report:

- target module path and line count;
- every top-level function/class method with line span;
- called self methods;
- self attributes read and written;
- imports used;
- GUI symbols/widgets/signals touched;
- side-effect categories;
- candidate island labels;
- per-island method list and estimated line count;
- per-island risk score;
- pairwise independence matrix;
- recommended patch composition.

The tool is evidence, not authority. AI/human review still approves the actual patch plan.

## Multi-island Batch Patch Mode

Use only when the independence matrix is clean. A batch patch has one ZIP, one install, one validate, one freeze, and one freeze entry that lists every island. Do not stack several ZIPs and validate only at the end. Do not partially freeze a failed batch.

A two-island patch is allowed only when:

- moved whole symbols are disjoint;
- helper files are disjoint;
- there are no conflicting writes to the same mutable state;
- shared read-only state is named and non-conflicting;
- there is no overlapping GUI signal rewiring;
- neither helper imports the facade upward;
- each island has distinct focused validation;
- the freeze entry names both islands.

## Patch-train Delivery Bundle

A patch train is allowed when the AI prepares several separate governed patch ZIPs and packages them together in one outer delivery ZIP for convenience.

Rules:

- each inner patch has its own feature id, SHA, install command, validate command, freeze command, validator, freeze hint, and freeze entry;
- each inner patch may contain one island or one approved two-island batch;
- inner patches targeting the same module are sequential: Patch B is built against Patch A, Patch C is built against Patch B;
- install, validate, and freeze each inner patch before proceeding to the next;
- if one inner patch fails, stop the train and do not install later patches;
- never freeze the outer bundle as one vague entry;
- never use patch trains to combine unrelated warning cleanup or behavior changes.

Safe execution:

```text
Patch A: install -> validate -> freeze
Patch B: install -> validate -> freeze
Patch C: install -> validate -> freeze
```

## Final Rule

Do not refactor to look organized while changing behavior accidentally. Do not hyperpopulate the project with tiny helper files when cohesive modules near the 400-line ideal would be safer and easier to maintain.
