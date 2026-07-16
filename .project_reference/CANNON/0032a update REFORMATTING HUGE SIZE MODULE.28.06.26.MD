# Large Module Creation and Refactor Protocol

## Box Logic Requirement

Before any implementation, repair, refactor, prompt update, governance update, or bundle creation, the AI must:

* Identify the active box before implementation.
* State owner paths.
* State files allowed to change.
* State files explicitly out of scope.
* Declare cross-box touches.
* Preserve public contracts.
* Validate the active box and any touched external box.

Version: 6.2
Status: Large-module creation and refactor protocol, expanded canon for safe splitting, public API preservation, validation gates, dependency-direction mapping, GUI inventory, optional type-check gates, and safe wide responsibility-island extraction
Use: Invoke when creating or refactoring a relevant code module that is above 500 lines, would exceed 500 lines, has high complexity, has too many responsibilities, or the user opens a large-module creation/refactor pass.

## Canonical prompt location

The active maintained prompt belongs in:

```text
kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/06_refactor_and_architecture_hardening/large_module_refactor_protocol.md
```

Legacy prompt-library mirrors, such as `kanda_reasoner_app/prompt_library/active/0000 5.5 PYARCHITECT LARGE MODULE REFACTOR PROTOCOL TEMPLATE v1.0.md`, are historical or app-facing copies unless a separate prompt-library synchronization pass explicitly updates them. Before this canon is updated, back up any legacy active mirror that the human names, but do not treat that legacy mirror as the source of truth.

## Purpose

Safely split large Python code modules into a stable public facade plus responsibility-specific helper files without changing behavior, breaking imports, weakening validation, or creating new architecture debt.

The protocol must favor incremental, validated extraction over cosmetic reorganization.

When the existing module is very large and many modules remain to refactor, the protocol may use a faster wide-cluster strategy, but only by dependency/responsibility island. Do not split by physical halves, arbitrary line ranges, or visual file position.

## Module-size and complexity law

Module-size law for code modules:

* Ideal: <= 400 lines.
* Maximum: <= 500 lines.
* When creating a new code module, do not create a file above 500 lines; split by responsibility before delivery.
* When refactoring an existing code module above 500 lines, split by responsibility.
* Complexity trigger: consider splitting even under 500 lines if the module has more than 10 top-level functions/classes, more than 5 distinct responsibilities, high cyclomatic complexity, repeated workflow sections, or a clear god-module pattern.
* Gradual exception: a module may remain above 500 lines only when it is explicitly tracked as an active refactor exception with a staged backlog and validation plan.
* This rule applies to code/source modules, especially `.py` files.
* This rule does not apply to plain text, Markdown, documentation, prompt, manifest, JSON, log, report, or other non-code content files. Files such as `.txt`, `.md`, `.json`, documentation artifacts, prompt files, manifests, and logs may be larger when their purpose requires it.

## Mandatory phases

### Task 0 - Audit only

Task 0 is read-only. Inspect exact source files. Do not implement.

Report:

1. Target identity

   * target file path;
   * current line count and projected line count;
   * owner box;
   * in-scope behavior;
   * out-of-scope behavior.

2. Import analysis

   * all modules that import the target;
   * all imports made by the target;
   * internal dependencies that may move during extraction;
   * star imports;
   * dynamic imports through `__import__`, `importlib`, plugin loaders, or runtime discovery;
   * import compatibility risks;
   * dependency-direction map, showing intended flow from facade to orchestration helpers to low-level pure helpers;
   * any helper that would import the facade, because helpers must not depend upward on the public facade unless explicitly justified;
   * any non-GUI helper that would import Qt/PySide, tkinter, or other GUI symbols.

3. Public API inventory

   * public symbols imported by other modules;
   * current `__all__`, if present;
   * if `__all__` is missing, assume all top-level non-private symbols may be public until proven otherwise;
   * public facade symbols that must remain import-compatible;
   * `__init__.py` re-export needs if the module becomes a package;
   * first-pass consumer-import rule: consumers should keep importing through the existing public origin path unless a separate public API migration is explicitly approved.

4. Test and characterization assessment

   * existing tests that cover the module;
   * existing import-smoke tests;
   * untested critical paths;
   * characterization tests needed before moving behavior;
   * whether coverage is sufficient for a behavior-preserving refactor.

5. Complexity and responsibility metrics

   * physical lines and logical lines when available;
   * number of top-level functions, classes, constants, and side-effect sections;
   * obvious cyclomatic complexity hotspots when available;
   * responsibility clusters;
   * dead-code or unreachable-code candidates.

6. Refactor speed-mode assessment

   * recommend narrow-cluster, wide-cluster, source-preserving facade, or defer;
   * identify candidate responsibility islands large enough to reduce meaningful line count;
   * estimate expected origin-file line reduction per island;
   * state whether the island can move without GUI signal rewiring;
   * state whether the island can move without consumer import migration;
   * state whether the island can move without helper-to-facade imports;
   * reject any plan based only on first half / second half, visual file position, or arbitrary line ranges.

7. Risk assessment

   * circular import risk: high, medium, or low;
   * breaking import risk: high, medium, or low;
   * behavior-change risk: high, medium, or low;
   * test adequacy: sufficient or insufficient;
   * GUI, file-system, subprocess, archive, or path-side-effect risks;
   * rollback difficulty;
   * dependency-direction risk when helpers would import upward or sideways in a way that can create cycles.

8. Blind spots

   * dynamic imports;
   * runtime code generation;
   * monkey-patching;
   * dynamic attribute assignment;
   * hidden CLI entry points;
   * GUI signal binding;
   * external tools or generated files that reference the old module.

9. GUI-specific inventory when the target touches GUI code

   * signals connected and the slots/callbacks they call;
   * widgets created, named, shown, hidden, enabled, disabled, or parented;
   * parent/ownership relationships and lifecycle-sensitive objects;
   * object names, labels, tooltips, status messages, shortcut keys, and button text that must not change;
   * clipboard, file dialog, timer, thread, subprocess, and long-running action interactions;
   * headless-safe smoke checks that can validate imports or builder logic without launching a full GUI.

Stop and wait for approval.

### Task 1 - Roadmap and decomposition

Task 1 plans the refactor. Do not implement unless the user explicitly authorized implementation.

Define:

1. Target structure

   * whether the original module remains a thin facade;
   * whether the module becomes a package with `__init__.py`;
   * helper folder name or helper module names;
   * responsibility-based helper names.

2. Helper naming rules

   * prefer names that describe responsibility, such as `_parsers.py`, `_validators.py`, `_models.py`, `_storage.py`, `_rendering.py`, `_workflow.py`;
   * avoid dumping-ground names such as `utils.py`, `helpers.py`, `misc.py`, `common.py`, `shared.py`, or `temp.py` unless the project already has a precise documented meaning for the name.

3. Refactor speed-mode selection

   * use narrow-cluster mode when dependency boundaries are unclear, test coverage is weak, or the cluster touches GUI wiring;
   * use wide responsibility-island mode when a coherent island can be moved together without changing behavior;
   * wide mode may extract multiple related helper functions/classes in one patch when they belong to the same island and can be validated together;
   * target a meaningful origin-file reduction, usually about 120-350 lines per wide cluster when the island is clean;
   * do not split by physical halves, arbitrary line ranges, or visual file position;
   * do not create dumping-ground helpers to maximize line reduction;
   * prefer one named helper module per responsibility island, or a small private helper package when the island is naturally multi-file;
   * keep every new helper code file under the module-size law.

4. Public API preservation strategy

   * list every public symbol that must remain importable;
   * if converting a module into a package, make `__init__.py` re-export the preserved public API;
   * define `__all__` in the facade or package `__init__.py`;
   * define `__all__` in helper files for their intended exports;
   * keep consumers working with existing imports whenever possible;
   * do not update consumers to import private helper paths during the first extraction pass unless the approved roadmap explicitly includes a public API migration.

Example:

```python
# module/__init__.py
from ._parsers import parse_config
from ._validators import validate_input

__all__ = [
    "parse_config",
    "validate_input",
]
```

5. Import compatibility matrix

   * existing import statement;
   * consuming file;
   * symbol consumed;
   * preservation route;
   * validation command proving it still works;
   * whether the consumer remains on the public facade path or is explicitly approved for migration.

6. Phased migration plan

   * move one responsibility cluster at a time;
   * validate after each cluster;
   * do not combine behavior changes with extraction;
   * do not combine large-module refactor with unrelated warning cleanup;
   * keep consumer imports stable through the facade in the first pass unless an approved API migration says otherwise.

7. Validation gates

   * py_compile touched Python files;
   * import smoke for the original public import path;
   * characterization tests for protected behavior;
   * focused tests for moved clusters;
   * architecture validation for Errors 0 when available;
   * workflow validation when a workflow or GUI path is touched;
   * no new circular imports;
   * no public import regressions;
   * no coverage drop when coverage tooling is available.

8. Dependency-direction plan

   * draw the intended import direction before implementation;
   * facade may import helpers;
   * orchestration helpers may import low-level pure helpers;
   * low-level helpers must not import orchestration helpers or the facade;
   * non-GUI helpers must not import GUI frameworks or GUI widgets;
   * any exception must be named, justified, and validated.

9. Rollback plan

   * baseline tag or checkpoint;
   * per-cluster backup or commit;
   * specific files to restore;
   * emergency stop conditions.

Stop and wait for approval unless the user explicitly authorized implementation.

### Task 2 - Implementation

Task 2 implements only the approved roadmap.

#### 2.1 Pre-refactor setup

Before moving code:

* create or identify a dedicated refactor branch/checkpoint when version control is available;
* record baseline validation output;
* add characterization tests first if tests are insufficient;
* preserve the public import path before moving consumers;
* keep first-pass consumer imports on the facade/public origin path unless a separate API migration is approved;
* record the dependency-direction map that the implementation must preserve;
* select and name the speed mode for this patch: narrow-cluster, wide responsibility-island, or source-preserving facade;
* for wide responsibility-island mode, list the whole symbols/classes/methods that move together and why they belong together;
* do not start broad formatting changes.

#### 2.2 Per-cluster extraction

For each responsibility cluster:

If using wide responsibility-island mode, one cluster may include multiple related whole symbols/classes/methods, but only when they share one responsibility island and one validation story.

1. Create the helper file or package.
2. Move whole top-level functions, whole internal classes, or whole methods only.
3. Do not slice statement blocks, loop bodies, partial functions, or arbitrary line ranges.
4. Update internal imports.
5. Update facade or `__init__.py` re-exports.
6. Update `__all__`.
7. Run the per-cluster validation gate.
8. For wide responsibility-island mode, run focused tests for every moved sub-area inside the island.
9. Stop or checkpoint before the next cluster if validation fails.

#### 2.3 Tool-assisted refactoring

Use tools only when available in the project environment and only when their changes are reviewed.

Allowed optional tools:

* Ruff for linting and safe autofix when configured;
* pytest and coverage for behavior validation when configured;
* pyright or mypy for static type checking when already configured;
* pyrefact for rule-based cleanup only after review;
* modguard, import-linter, or equivalent dependency-boundary checks when configured;
* wily, radon, or equivalent complexity reporting when configured;
* IDE refactoring tools for safe symbol moves.

Do not introduce these tools as mandatory dependencies in a patch unless the user explicitly approves that toolchain change.

#### 2.4 Circular import prevention

Before and after each extraction:

* inspect new imports between facade and helpers;
* compare actual imports to the dependency-direction map;
* prefer lower-level helpers that do not import the facade;
* prevent helpers from importing upward into the facade unless explicitly justified;
* use `from __future__ import annotations` for type references when useful;
* use local/lazy imports only as documented tactical fixes;
* restructure dependencies rather than hiding cycles when possible;
* document any remaining unavoidable cycle risk.

#### 2.5 Public/private boundary enforcement

Every helper file must clearly mark intended exports:

* helper internals should use leading underscores;
* helper files should declare `__all__` when they expose symbols to a facade;
* facade or package `__init__.py` should own the public API;
* do not let private helper symbols become accidental public API;
* do not import generated shards directly as public owner modules unless explicitly intended.

## Normal decomposition

* Keep the origin file path and public imports stable.
* Keep first-pass consumers on the public facade/origin import path unless API migration is explicitly approved.
* Extract by whole top-level private functions, whole internal classes, or whole methods.
* Do not slice statement blocks, loop bodies, or partial functions.
* Use clear responsibility names, not generic dumping-ground helper names.
* Define explicit `__all__` for public exports.
* Avoid circular imports.
* Validate after every extracted cluster.

## Optimized wide responsibility-island mode

Use this mode when slow tiny extractions are technically safe but impractically inefficient for a very large module backlog.

This mode is faster, but still behavior-preserving. It is not a permission to split files by line count.

### Core idea

Move a whole dependency/responsibility island at once while keeping the original module as the public facade.

Acceptable wide islands include groups such as:

* import/export parsing and formatting;
* clipboard payload composition;
* project-root/path resolution;
* pending-file discovery and pending-row assembly;
* status transition helpers;
* validation/report formatting;
* model conversion helpers;
* GUI-builder subpanels only after non-GUI logic is stable.

Unacceptable wide islands include:

* first half of the file;
* second half of the file;
* all functions that happen to be adjacent;
* all functions with similar length;
* arbitrary line ranges;
* generic utilities created only to reduce line count.

### Wide-mode criteria

Use wide mode only when all are true:

* the island has a single clear responsibility name;
* each moved item is a whole function, class, or method;
* helper modules do not import upward into the facade;
* first-pass consumers remain on the facade/public origin import path;
* GUI signal wiring is not changed, or the GUI island has explicit signal/widget inventory and headless-safe validation;
* every new helper file stays within the module-size law;
* focused tests cover the island;
* py_compile and import-smoke validation pass;
* no new circular import or dependency-direction violation is introduced.

### Mikado-style acceleration

When a direct large extraction fails or appears risky:

1. State the larger desired end state.
2. Attempt the dependency analysis mentally or in a scratch branch, not as final delivery.
3. Identify the blockers that prevent the larger move.
4. Revert or avoid the unsafe move.
5. Extract prerequisite islands first.
6. Repeat until the larger move becomes safe.

This allows faster convergence without committing unsafe changes.

### Patch sizing

Prefer fewer, larger validated islands over many tiny helper crumbs when the dependency boundary is clean.

Typical target for a clean wide cluster:

```text
120-350 lines removed from the origin module
1-3 private helper modules
focused tests for each moved sub-area
no public import migration
```

A patch may exceed this range only when the island is mechanically obvious, strongly covered by tests, and has low circular-import risk.

A patch should be smaller when the island touches GUI lifecycle, signal wiring, file deletion, subprocesses, external tools, archive creation, or freeze/governance behavior.

### Wide-mode stop conditions

Stop immediately and fall back to narrow mode if:

* the helper would need to import the facade;
* consumers would need to import private helpers;
* signal wiring becomes ambiguous;
* import smoke fails;
* test coverage is too weak to characterize the behavior;
* the island cannot be named without using generic labels like helpers/utils/misc/common.

## Source-preserving facade option

Use only when semantic extraction is too risky, such as:

* huge public function;
* central CLI/module;
* previous whole-symbol extraction cannot reduce below 500 lines;
* public behavior must remain stable before deeper maintainability work.

Rules for source-preserving facade:

* Keep the original file as a small public facade.
* Store preserved implementation source in private helper shards.
* Use unique private source-part symbols.
* Keep each generated file below 500 lines.
* Do not duplicate exported shard symbols.
* Preserve behavior as a tactical stabilization step.
* Mark this as not a true maintainability refactor.
* Plan later semantic extraction if maintainability is the goal.

## Delivery model

Use the active project delivery contract.

For KANDA/PyArchitect governed patch work:

* deliver a patch ZIP with Install, Validate, and Freeze instructions;
* stage transient install, extract, correction, and validation-helper files under `<drive>:\<project>_delete_after_daily_work`;
* do not put transient files in the active project root;
* include a root-level `KANDA_FREEZE_HINT.json` when the patch is freezeable;
* do not write frozen memory before local validation passes and the user confirms Confirm and Write.

For non-governed projects, use the equivalent local validation and backup procedure, but still preserve source-truth, public API, rollback, and validation evidence.

## Backup and rollback guidance

Before risky extraction:

* use version control if available;
* create a baseline branch, tag, or checkpoint;
* keep per-phase rollback instructions;
* back up named legacy prompt or source files when the user explicitly requests backup;
* never make source safety depend on untracked temporary files.

Emergency stop conditions:

* any core test failure;
* import errors in dependent modules;
* public import compatibility break;
* new circular dependency;
* coverage drop beyond approved threshold when coverage is available;
* unresolved critical architecture validation error;
* validator output lacks required success markers.

## Minimum validation

Minimum validation for code refactors:

* py_compile touched Python files;
* import smoke for the origin module when possible;
* import compatibility checks for every preserved public import;
* characterization tests when existing tests are insufficient;
* wide responsibility-island tests for every moved sub-area when wide mode is used;
* helper manifest validation when helpers are created;
* circular import check when import graph changed;
* relevant tab/box validation;
* architecture validation with Errors 0 when project canon requires it;
* workflow validation when workflow behavior changed;
* local user validation before freeze.

When optional tools are already configured, add:

* Ruff check;
* pytest with coverage and no unapproved coverage drop;
* pyright or mypy static type check;
* modguard, import-linter, or equivalent boundary checks;
* pyrefact only for reviewed rule-based cleanup;
* wily/radon complexity report if available.

Success markers must be captured in validation evidence before freeze.

## Post-refactor fragmentation audit

After large-module splitting or source-preserving facade work, run a read-only fragmentation audit before treating the refactor as safe.

### Purpose

Large-module splits can leave unresolved names, missing imports, import leaks, facade binding gaps, or helper modules that only work by accident. The audit must find these before the user freezes the refactor.

### Read-only Task 0 audit runner

For complex helper-folder splits, design a Task 0 audit runner that performs:

```text
Phase 1: discover helper modules
Phase 2: AST-based name resolution per module
Phase 3: standard import, runtime API, GUI leak, and binding-gap detection
Phase 4: import smoke and targeted headless smoke when safe
Phase 5: Markdown + JSON report generation
```

The runner must not modify source. It should write reports only to the approved maintenance/audit output area for that pass.

### Minimum findings

The audit should report:

* unresolved names;
* missing standard-library imports;
* runtime API imports missing after split;
* Qt/GUI symbols leaking into non-GUI helpers;
* dependency-direction violations, including helpers importing the facade or low-level helpers importing orchestration layers;
* facade/helper binding gaps;
* symbols present in sibling helpers but not imported;
* import smoke failures;
* helper files that are not safe to import standalone when the architecture expects facade-only import;
* wide-mode islands that accidentally became generic dumping grounds.

### False-positive guard

Before applying import-smoke results, ask whether helpers are intended to be standalone importable or facade-only private shards. A source-preserving facade may intentionally make helper shards private implementation details.

### Validation rule

A large-module refactor is not ready for freeze until:

```text
focused refactor tests pass
fragmentation audit has no critical unresolved findings
dependency-direction map has no unapproved violations
wide-mode island has no generic dumping-ground helper
architecture validation has Errors 0
workflow validation has fail 0 when workflow behavior is touched
user validates locally
```

## Approval gates

Approval flow:

```text
Task 0: audit only -> approval
Task 1: roadmap and decomposition -> approval
Task 2: implementation per cluster -> validation -> checkpoint
Final validation -> approval before freeze
```

Per-cluster approval is optional only when the user explicitly authorized continuous implementation. Validation after each cluster is mandatory.

## Do-not-regress rules

* Do not refactor to look organized while changing behavior accidentally.
* Do not break imports that existing consumers rely on.
* Do not move consumers from public facade imports to private helper imports unless an API migration was explicitly approved.
* Do not omit `__init__.py` re-export strategy when converting a module into a package.
* Do not omit `__all__` when creating facade/helper public boundaries.
* Do not add helper dumping grounds.
* Do not split by physical halves, arbitrary line ranges, or visual file position.
* Do not use wide responsibility-island mode unless the island has one clear responsibility, no upward helper imports, and focused tests.
* Do not introduce circular imports.
* Do not remove code as dead code unless reachability analysis and user-approved scope support deletion.
* Do not treat optional external tools as mandatory unless approved.
* Do not combine large-module refactor with unrelated warning cleanup.
* Do not freeze without local validation evidence.

## Change log

* v5.8: Added post-refactor fragmentation audit requirement for helper-folder and source-preserving facade refactors.
* v5.9: Extended module-size law to new code module creation and clarified that the 400/500 line limit applies to code/source modules, not text, Markdown, documentation, prompt, manifest, JSON, log, report, or other non-code files.
* v6.0: Added import graph audit, characterization test planning, public API inventory, `__init__.py` re-export strategy, import compatibility matrix, `__all__` enforcement, circular import risk assessment, optional modern tooling integration, per-cluster validation, rollback details, and KANDA daily-work containment for governed patch delivery.
* v6.1: Added dependency-direction mapping before extraction, GUI-specific signal/widget inventory, optional pyright/mypy and import-linter boundary gates when already configured, and a first-pass rule that consumers stay on public facade imports unless an API migration is explicitly approved.
* v6.2: Added safe wide responsibility-island extraction mode, Mikado-style acceleration, explicit rejection of binary/line-range splitting, speed-mode assessment in Task 0/Task 1, patch sizing guidance, and wide-mode validation/stop conditions.
