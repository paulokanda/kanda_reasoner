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

Version: 3.4.0
Status: Reusable large-module refactor template aligned with Large Module Creation and Refactor Protocol v8.0 and the final Planner-to-Workbench execution canon.
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
- For KANDA/PyArchitect governed patch work, keep only disposable install ZIPs, extraction trees, correction scratch, Shadow workspaces, and temporary validation helpers under the ownership-free transient garbage root `<drive>/<project>_delete_after_daily_work`. Write durable audits, handoffs, and validation evidence under the selected project's canonical `*_show_project_to_AI` support root.

## Current AST Safe Refactor integration

For KPR-06-003 source-risk repair, consume the exact source identity and current
preflight evidence before choosing architecture. Treat project index, consumer
map, public contract, semantic dynamic-risk findings, dependency evidence, and
known patterns as bounded evidence, not autonomous architecture authority.

Use KPR-06-004 `Safe Refactor How To` as the reusable process refresher when
context may be incomplete; keep it separate from target-specific KPR-06-003 truth.

Before release, require behavior equivalence on meaningful semantic cases,
consumer compatibility, dependency direction, semantic dynamic safety, strict
101-499 line compliance, and a fresh AST Split Audit for every touched permanent
Python source module. Development caches may accelerate iteration but never replace
the final fresh family audit.

Prefer descriptor-driven release assembly. Stage downloaded governed ZIPs from the
active drive root into `<drive>/<project>_delete_after_daily_work` only after hash
verification. Freeze remains preparation-only until human Preview and explicit
Confirm and Write.

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

Helper expansion rule:

- Every resulting Python source module, including facades and helpers, must satisfy `100 < physical_lines < 500`; the exact valid integer range is 101-499.
- There are no facade, constants, adapter, package-marker, or structural-role exceptions in this workflow.
- Do not pad source files. When cohesive architecture cannot satisfy 101-499, return `PLAN_CORRECTION_REQUIRED` with Compliance Veto evidence.
- Do not split by arbitrary line ranges. Split by responsibility, dependency direction, public API boundary, side-effect isolation, validation boundary, or no-leak ownership boundary.
- Do not let helper modules accidentally own facade public API. Facades own public compatibility unless a separate governed architecture decision approves another owner.

## Sequential double-refactor delivery train v7.4

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
- Stop only when the approved architecture is complete and every resulting Python source file satisfies the strict 101-499 law without padding.
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
- enforce 101-499 physical lines for every resulting Python source file without padding or structural-role exceptions;
- create only the cohesive responsibility modules needed to keep every resulting Python source file within 101-499 physical lines;
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

Do not refactor to look organized while changing behavior accidentally. Preserve cohesion while enforcing the strict 101-499 physical-line law; do not pad code and do not invent architecture merely to satisfy line counts.
