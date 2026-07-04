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

Version: 7.2
Status: Large-module creation and refactor protocol, expanded canon for safe splitting, public API preservation, validation gates, dependency-direction mapping, GUI inventory, optional type-check gates, safe wide responsibility-island extraction, AST-assisted heuristic split audit, safe multi-island batch patches, patch-train delivery bundles, sequential double-refactor delivery trains, practical helper-file granularity, normal `.py` source ownership, and a speed-acceleration layer covering codemod-assisted moves, tiered validation gates, parallel test execution, audit-cache reuse, and parallel-safe backlog batching.
Use: Invoke when creating or refactoring a relevant code module that is above 500 lines, would exceed 500 lines, has high complexity, has too many responsibilities, or the user opens a large-module creation/refactor pass.

## Canonical prompt location

The active maintained prompt belongs in:

```text
kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/06_refactor_and_architecture_hardening/large_module_refactor_protocol.md
```

Legacy prompt-library mirrors, such as `kanda_reasoner_app/prompt_library/active/0000 5.5 PYARCHITECT LARGE MODULE REFACTOR PROTOCOL TEMPLATE v1.0.md`, are historical or app-facing copies unless a separate prompt-library synchronization pass explicitly updates them. Before this canon is updated, back up any legacy active mirror that the human names, but do not treat that legacy mirror as the source of truth.

## Purpose

Safely split large Python code modules into a stable public facade plus responsibility-specific helper files without changing behavior, breaking imports, weakening validation, or creating new architecture debt.

The protocol must favor incremental, validated extraction over cosmetic reorganization, must favor deterministic AST evidence and refactor island manifests over manual guessing, and must favor planning several candidate islands together before implementation while keeping install, validate, and freeze strictly scoped. When several safe follow-up patches can be prepared from the same candidate queue, the AI may deliver them as a sequential double-refactor delivery train. The default train limit is up to four ordered patch ZIPs per response, each containing one island or up to two tightly related independent refactor slices. Each inner patch remains a separate governed unit with its own install, validate, freeze, feature id, freeze hint, validation evidence, and rollback boundary.

When the existing module is very large and many modules remain to refactor, the protocol may use a faster wide-cluster strategy, but only by dependency/responsibility island. When two islands are proven independent by the Multi-Island Execution Layer, they may travel in one governed patch ZIP. When several such governed patches can be prepared safely, they may be delivered together as an ordered delivery train, but they must be installed, validated, and frozen one by one before the next patch is applied. Do not split by physical halves, arbitrary line ranges, visual file position, or line-count-only targets.

## Module-size and complexity law

Module-size law for code modules:

* Ideal: <= 400 lines.
* Maximum: <= 500 lines.
* When creating a new code module, do not create a file above 500 lines; split by responsibility before delivery.
* When refactoring an existing code module above 500 lines, split by responsibility.
* Complexity trigger: consider splitting even under 500 lines if the module has more than 10 top-level functions/classes, more than 5 distinct responsibilities, high cyclomatic complexity, repeated workflow sections, or a clear god-module pattern.
* Gradual exception: a module may remain above 500 lines only when it is explicitly tracked as an active refactor exception with a staged backlog and validation plan.
* This rule applies to code/source modules, especially `.py` files.
* This rule does not apply to plain text, Markdown, documentation, prompt, manifest, JSON, log, report, or other non-code content files.

Practical granularity rule for helper files:

* The 400-line ideal is a healthy target band, not a command to atomize code.
* A cohesive helper file around 250-400 lines is acceptable and often preferable to many tiny files.
* Do not create new source/helper `.py` files with only a few lines merely to satisfy a line-count target.
* Avoid creating helper modules below roughly 80-100 substantive lines unless they are required package markers, public facade/re-export compatibility shims, generated validators, narrowly-scoped constants, or deliberately documented stable seams.
* Before creating a new helper module under roughly 80-100 substantive lines, state why it should not be merged into an adjacent cohesive helper.
* Prefer fewer, cohesive responsibility modules over project hyperpopulation. Hyperpopulated micro-files make features harder to find, increase import-surface risk, and increase missed-feature risk during future maintenance.
* Completion guards should stop a refactor train when remaining files are cohesive and below the practical target band; do not continue splitting tiny cohesive files just to create another train car.

Helper expansion rule:

* When a new or touched code/source module would exceed the 500-physical-line hard maximum, split the work into as many cohesive helper, auxiliary, derived, adapter, or complementary modules as needed to preserve behavior, ownership, readability, and validation safety.
* Additional helper modules are allowed and expected when they are needed to keep the main module and every helper module within the module-size law.
* Every helper, auxiliary, derived, adapter, or complementary code/source module must obey the same size law: ideal <= 400 physical lines, hard maximum <= 500 physical lines, and practical minimum around 100 substantive lines unless a documented exception applies.
* Do not create tiny helper files merely to satisfy a line-count target. A helper below roughly 100 substantive lines is allowed only when it is justified as a facade or re-export shim, package marker, constants module, validation helper, optional dependency adapter, circular-dependency breaker, stable seam, or another explicitly documented cohesive boundary.
* Prefer cohesive responsibility modules over catch-all helpers or project hyperpopulation. Split by responsibility, dependency direction, public API boundary, side-effect isolation, validation boundary, or no-leak ownership boundary, not by arbitrary line ranges.

Traditional source-file rule:

* Runtime/source logic should live in normal importable `.py` files with clear names and ordinary Python imports.
* Do not hide source behavior inside ZIP payload files, embedded archive members, generated source strings, or delivery-package structures as part of normal project logic.
* The `payload/` folder inside an installable patch ZIP is allowed as delivery packaging only. It must not become an application/runtime architecture pattern.
* Use source-preserving shard files only as a temporary, explicitly-labeled stabilization exception when semantic extraction is too risky, and plan later semantic cleanup.

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

6. AST-assisted heuristic split audit

   Use the local read-only AST split audit tool when available and useful. The tool is evidence, not authority. It may inspect the target module and produce:

   * symbol and method names;
   * line spans and estimated line reductions;
   * called `self` methods;
   * `self` attributes read and written;
   * imports used by each symbol;
   * GUI symbols, widgets, signals, timers, threads, dialogs, and clipboard use;
   * file-system, archive, subprocess, template, freeze, or governance side effects;
   * candidate island labels;
   * per-island risk ratings;
   * pairwise independence findings;
   * recommended single-island or two-island patch composition.

   The AST report must be treated as a starting point. The AI must still inspect source context, validate the proposed island names, and reject tool suggestions that conflict with architecture, behavior, or frozen memory.

7. Refactor speed-mode assessment

   * recommend narrow-cluster, wide-cluster, source-preserving facade, or defer;
   * identify candidate responsibility islands large enough to reduce meaningful line count;
   * estimate expected origin-file line reduction per island;
   * state whether each island can move without GUI signal rewiring;
   * state whether each island can move without consumer import migration;
   * state whether each island can move without helper-to-facade imports;
   * state whether each island is a good candidate for codemod-assisted mechanical extraction versus manual move;
   * score candidate islands with the Heuristic Refactor Planner before selecting the next implementation patch;
   * include a Refactor Island Manifest for the selected island before implementation;
   * when beginning a module refactor, build a candidate-island queue and independence matrix before deciding the next patch;
   * state whether the next patch is single-island or multi-island batch mode;
   * state whether the planned helper files have practical size and cohesion, avoiding unnecessary micro-files;
   * reject any plan based only on first half / second half, visual file position, arbitrary line ranges, or making many tiny files to chase the 400-line ideal.

8. Multi-island candidate queue

   Instead of reporting only the single best island, enumerate every plausible candidate island found in this one audit pass, normally 3-6 for a large module. For each candidate island, name it, list its whole symbols, estimate line reduction, list important `self` state, list GUI/side effects, and assign risk.

   For every pair of candidate islands, state explicitly whether they are independent, dependent, or ambiguous under the Multi-Island Execution Layer. Rank the queue by safe value: largest clean independent reduction first; riskiest or most-coupled islands last. This queue is planning output only and does not authorize implementation.

9. Risk assessment

   * circular import risk: high, medium, or low;
   * breaking import risk: high, medium, or low;
   * behavior-change risk: high, medium, or low;
   * test adequacy: sufficient or insufficient;
   * GUI, file-system, subprocess, archive, or path-side-effect risks;
   * rollback difficulty;
   * dependency-direction risk when helpers would import upward or sideways in a way that can create cycles.

10. Blind spots

    * dynamic imports;
    * runtime code generation;
    * monkey-patching;
    * dynamic attribute assignment;
    * hidden CLI entry points;
    * GUI signal binding;
    * external tools or generated files that reference the old module.

11. GUI-specific inventory when the target touches GUI code

    * signals connected and the slots/callbacks they call;
    * widgets created, named, shown, hidden, enabled, disabled, or parented;
    * parent/ownership relationships and lifecycle-sensitive objects;
    * object names, labels, tooltips, status messages, shortcut keys, and button text that must not change;
    * clipboard, file dialog, timer, thread, subprocess, and long-running action interactions;
    * headless-safe smoke checks that can validate imports or builder logic without launching a full GUI.

12. Audit-cache reuse

    * when this Task 0 audit is one of several queued against the same backlog, check whether a prior audit pass already computed the project-wide import graph, AST symbol table, or complexity metrics within the current working session;
    * if a valid cache exists and no relevant source files changed since it was built, reuse it instead of recomputing from scratch;
    * state explicitly whether this audit used a fresh scan or a reused cache, and the cache's age/validity basis.

Stop and wait for approval unless the user explicitly authorized continuous implementation.

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
   * prefer ordinary importable `.py` source modules for logic; do not design runtime logic around ZIP payload files or delivery-package folders;
   * avoid dumping-ground names such as `utils.py`, `helpers.py`, `misc.py`, `common.py`, or `shared.py` unless the project already has a precise documented meaning for the name;
   * avoid unnecessary micro-files: a helper near the 400-line ideal may remain intact when cohesive, and a new tiny helper should be created only for a clear public compatibility seam, package marker, constants seam, or validated responsibility boundary.

3. Refactor speed-mode selection

   * use narrow-cluster mode when dependency boundaries are unclear, test coverage is weak, or the cluster touches GUI wiring;
   * use wide responsibility-island mode when a coherent island can be moved together without changing behavior;
   * target a meaningful origin-file reduction, usually about 120-350 lines per wide cluster when the island is clean;
   * do not split by physical halves, arbitrary line ranges, or visual file position;
   * do not create dumping-ground helpers to maximize line reduction;
   * prefer one named helper module per responsibility island, or a small private helper package when the island is naturally multi-file;
   * keep every new helper code file under the module-size law;
   * prefer helper files in the practical cohesion band, usually 250-400 lines when the responsibility naturally fits there, rather than scattering behavior across tiny files;
   * avoid creating new helper files below roughly 80-100 substantive lines unless the roadmap justifies a stable seam or compatibility wrapper;
   * use the AST split audit report when available to justify or reject the planned island selection.

4. Multi-island patch composition decision

   * from the Task 0 candidate queue, select either one island per patch or up to two islands per patch;
   * selecting a two-island patch is only permitted when the chosen pair passes every independence criterion in the Multi-Island Execution Layer;
   * if independence is ambiguous for any criterion, default to separate patches;
   * state the decision and the independence check result explicitly before implementation begins.

5. Patch-train delivery decision

   * decide whether delivery will be a single governed patch ZIP or an outer patch-train bundle containing multiple separate governed patch ZIPs;
   * use a patch train only when every inner patch has a clear sequential dependency order, its own feature id, its own validator, its own freeze hint, and its own rollback boundary;
   * for one target module, build Patch B against the result of Patch A, and Patch C against the result of Patch B;
   * do not let patch-train packaging change execution order: each inner patch is still install -> validate -> freeze before the next begins;
   * if Patch A fails, do not proceed to Patch B;
   * state the patch-train order explicitly before implementation begins.

5. Public API preservation strategy

   * list every public symbol that must remain importable;
   * if converting a module into a package, make `__init__.py` re-export the preserved public API;
   * define `__all__` in the facade or package `__init__.py`;
   * define `__all__` in helper files for their intended exports;
   * keep consumers working with existing imports whenever possible;
   * do not update consumers to import private helper paths during the first extraction pass unless the approved roadmap explicitly includes a public API migration.

6. Import compatibility matrix

   * existing import statement;
   * consuming file;
   * symbol consumed;
   * preservation route;
   * validation command proving it still works;
   * whether the consumer remains on the public facade path or is explicitly approved for migration.

7. Phased migration plan

   * move one responsibility cluster or one approved independent pair at a time;
   * validate after each cluster/pair using the appropriate gate tier;
   * do not combine behavior changes with extraction;
   * do not combine large-module refactor with unrelated warning cleanup;
   * keep consumer imports stable through the facade in the first pass unless an approved API migration says otherwise.

8. Validation gates

   * py_compile touched Python files;
   * import smoke for the original public import path;
   * characterization tests for protected behavior;
   * focused tests for moved clusters, reported per-island even inside a paired patch;
   * architecture validation for Errors 0 when available;
   * workflow validation when a workflow or GUI path is touched;
   * no new circular imports;
   * no public import regressions;
   * no coverage drop when coverage tooling is available.

9. Dependency-direction plan

   * draw the intended import direction before implementation;
   * facade may import helpers;
   * orchestration helpers may import low-level pure helpers;
   * low-level helpers must not import orchestration helpers or the facade;
   * non-GUI helpers must not import GUI frameworks or GUI widgets;
   * any exception must be named, justified, and validated.

10. Rollback plan

    * baseline tag or checkpoint;
    * per-cluster backup or commit;
    * for paired-island patches, per-island file lists and a whole-ZIP rollback route;
    * if surgical per-island rollback cannot be clean because both islands modify the same facade body, prefer smaller or single-island patches;
    * specific files to restore;
    * emergency stop conditions.

11. Backlog parallelization plan

    * list other modules in the current backlog that are candidates for concurrent drafting;
    * confirm independence: no shared owner box, no direct cross-imports, no shared GUI signal wiring;
    * confirm that gating and freezing remain per-module and serial even when drafting is concurrent.

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
* select and name the speed mode for this patch;
* for wide responsibility-island mode, list the whole symbols/classes/methods that move together and why they belong together;
* state whether this cluster will use codemod-assisted mechanical extraction or manual extraction, and why;
* state whether this patch contains one island or an approved independent pair, and restate the independence check result inline;
* if this delivery is part of a sequential double-refactor train, state the inner patch id, the required predecessor patch, and the rule that later patches must not be installed until this patch has passed validation and freeze;
* do not start broad formatting changes.

#### 2.2 Per-cluster extraction

For each responsibility cluster or each island within an approved pair:

1. Create the helper file or package.
2. Move whole top-level functions, whole internal classes, or whole methods only.
3. Do not slice statement blocks, loop bodies, partial functions, or arbitrary line ranges.
4. Update internal imports.
5. Update facade or `__init__.py` re-exports.
6. Update `__all__`.
7. Run the fast gate immediately; run the medium gate before considering the cluster/island complete.
8. For wide responsibility-island mode, run focused tests for every moved sub-area inside the island.
9. If this patch contains a second independent island, complete and gate the first island before starting the second; never interleave their file edits.
10. Stop or checkpoint before the next cluster/island if validation fails.

#### 2.3 Tool-assisted refactoring

Use tools only when available in the project environment and only when their changes are reviewed.

Allowed optional tools:

* the local AST split audit runner for read-only evidence generation;
* Ruff for linting and safe autofix when configured;
* pytest and coverage for behavior validation when configured;
* pytest-xdist for parallel test execution when the relevant test slice is large enough;
* LibCST codemods for mechanical, whole-symbol move/rename/import-update transforms after fixture-first verification;
* Rope, or IDE-native refactoring for safe rename/move/reference tracking;
* pyright or mypy for static type checking when already configured;
* pyrefact for rule-based cleanup only after review;
* modguard, import-linter, or equivalent dependency-boundary checks when configured;
* wily, radon, or equivalent complexity reporting when configured.

Do not introduce optional tools as mandatory dependencies in a patch unless the user explicitly approves that toolchain change. Tooling speeds up evidence gathering or mechanical movement; it does not replace validation.

#### 2.4 Circular import prevention

Before and after each extraction:

* inspect new imports between facade and helpers;
* compare actual imports to the dependency-direction map;
* prefer lower-level helpers that do not import the facade;
* prevent helpers from importing upward into the facade unless explicitly justified;
* use `from __future__ import annotations` for type references when useful;
* use local/lazy imports only as documented tactical fixes;
* restructure dependencies rather than hiding cycles when possible.

#### 2.5 Public/private boundary enforcement

Every helper file must clearly mark intended exports:

* helper internals should use leading underscores;
* helper files should declare `__all__` when they expose symbols to a facade;
* facade or package `__init__.py` should own the public API;
* do not let private helper symbols become accidental public API;
* do not import generated shards directly as public owner modules unless explicitly intended.

## Tool-assisted Heuristic Split Audit

This section defines the local AST tool that supports, but does not replace, AI judgment.

### Human interface

The preferred KANDA interface is the Architecture Review tab:

```text
Architecture Review
  Run AST Split Audit
  Copy Split Handoff for AI
  Save/Export Audit Results
```

The user selects the active project root and a target `.py` module. The tool runs read-only, displays the Markdown report in the audit output panel, writes Markdown and JSON reports to daily-work staging, and copies or exports an AI handoff on request.

### Output location

For governed KANDA work, audit outputs must be staged under:

```text
<drive>/<project>_delete_after_daily_work/large_module_split_audits/
```

The tool must not write transient audit files into the project root. It may copy human-approved handoff content to the clipboard. It must not write frozen memory, modify source, or create refactor patches.

### Required report content

The AST report should include:

* target module path and line count;
* every top-level function/class method with line span;
* called `self` methods;
* `self` attributes read and written;
* imports used;
* GUI symbols/widgets/signals touched;
* side-effect categories;
* candidate island labels;
* per-island method list and estimated line count;
* per-island risk score;
* pairwise independence matrix;
* recommended patch composition: single island, two-island batch, or manual audit required;
* explicit caveat that AI/human review must confirm the result before implementation.

### Independence evidence rule

Tool-generated independence is advisory. The AI must confirm the result before implementation. A two-island patch is allowed only when all are true:

* moved whole symbols are disjoint;
* helper files are disjoint;
* no conflicting writes to the same mutable state;
* shared read-only state is acceptable when it is named and non-conflicting;
* no overlapping GUI signal rewiring;
* no overlapping GUI widget mutation unless explicitly inventoried and validated;
* neither helper imports the facade upward;
* neither helper imports the other unless explicitly planned and acyclic;
* each island has distinct focused validation;
* the freeze entry names both islands.

If any criterion is ambiguous or unverified, use separate patches.

## Normal decomposition

* Keep the origin file path and public imports stable.
* Keep first-pass consumers on the public facade/origin import path unless API migration is explicitly approved.
* Extract by whole top-level private functions, whole internal classes, or whole methods.
* Do not slice statement blocks, loop bodies, or partial functions.
* Use clear responsibility names, not generic dumping-ground helper names.
* Use normal importable `.py` source files for moved logic; delivery ZIP payload folders are installer packaging, not runtime design.
* Do not create tiny helper crumbs solely to keep every file far below 400 lines; cohesive helper files near the 400-line ideal are acceptable.
* Define explicit `__all__` for public exports.
* Avoid circular imports.
* Validate after every extracted cluster, using the fast gate at minimum and the medium gate before the cluster is considered done.

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

### Patch sizing

Prefer fewer, larger validated islands over many tiny helper crumbs when the dependency boundary is clean.

Typical target for a clean wide cluster:

```text
120-350 lines removed from the origin module
1-3 private helper modules
focused tests for each moved sub-area
no public import migration
```

Helper-file granularity guidance:

```text
Preferred cohesive helper size: roughly 250-400 substantive lines when the responsibility naturally fits.
Allowed small wrappers: public facades, package markers, re-export compatibility files, generated validators, and documented constants seams.
Avoid by default: new helper modules under roughly 80-100 substantive lines when they only move a few functions and increase file count.
Stop condition: if all remaining helpers are cohesive and below the 400-line ideal, stop with a completion guard rather than manufacturing more files.
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
* Store preserved implementation source in normal private `.py` helper modules whenever possible.
* Do not store preserved implementation as ZIP payload logic, embedded archive members, or runtime-loaded delivery artifacts.
* Use unique private source-part symbols.
* Keep each generated file below 500 lines, while avoiding needless micro-shards when a cohesive helper can remain near the 400-line ideal.
* Do not duplicate exported shard symbols.
* Preserve behavior as a tactical stabilization step.
* Mark this as not a true maintainability refactor.
* Plan later semantic extraction if maintainability is the goal.

## Speed Acceleration Layer

This section defines how the protocol moves faster without weakening any safety gate above. None of the following permits skipping a validation step; they change how a step is performed, not whether it happens.

### Tiered validation gates

Define three gate tiers and apply the cheapest tier that still proves the cluster is safe; reserve the most expensive tier for batch/phase boundaries rather than every cluster:

```text
Fast gate    - py_compile on touched files + import smoke for the public path.
Medium gate  - characterization tests + focused tests for the moved island.
Full gate    - whole project test suite, architecture validation, and workflow validation when applicable.
```

Run the fast and medium gates after every cluster/island. Run the full gate once per batch/phase boundary and always before freeze. Do not require a full-gate run after every micro-cluster.

### Codemod-assisted whole-symbol extraction

When wide-mode criteria are met and the island consists of cleanly-bounded whole symbols:

1. Write a small fixture that mirrors the shape of the real island.
2. Write the move/import-update transform using a codemod framework's test harness against that fixture first.
3. Only after the fixture test passes, run the transform against real source files.
4. Run the fast gate immediately afterward, then the medium gate.
5. Treat the transform script as disposable scratch tooling unless it will be reused.

IDE-native safe-move/rename with reference tracking is an acceptable equivalent for moves too small or too one-off to justify a codemod.

### Backlog parallel-safe batching

When several modules in the project need this same refactor treatment:

* identify modules with no shared owner box, no direct cross-imports, and no shared GUI signal wiring;
* independent modules may be drafted concurrently in separate branches/worktrees/sessions;
* gating and freezing remain strictly per-module and serial;
* modules that share an owner box, import each other, or share GUI wiring must stay serial.

### Audit-cache reuse

When running Task 0 repeatedly across a backlog in the same working session:

* reuse a previously computed project-wide import graph, AST symbol table, or complexity report if no relevant source file has changed since it was built;
* state in the Task 0 report whether the audit used a fresh scan or a reused cache;
* never reuse a cache across a session boundary without re-validating that the underlying files are unchanged.

## Multi-Island Execution Layer

This layer governs whether more than one responsibility island, found within the same module-refactor pass, may travel together in one patch. It is planning-and-execution discipline, not a relaxation of validation, freeze, or rollback granularity.

### What this layer is for

The Task 0 multi-island candidate queue may surface several plausible islands in one audit pass. Discovering them together is always safe because it is read-only planning. Combining them into one implementation patch is only safe under strict conditions.

### Independence test

Two islands may be paired only when all are true:

* moved whole symbols are disjoint;
* helper files are disjoint;
* no conflicting writes to the same mutable state;
* shared read-only state is acceptable when it is named and non-conflicting;
* no overlapping GUI signal rewiring;
* no overlapping GUI widget mutation unless explicitly inventoried and validated;
* neither island's new helper imports the other island's helper unless explicitly planned and acyclic;
* neither island imports the facade upward;
* each island independently satisfies every wide-mode criterion on its own;
* each island has distinct focused test coverage;
* file-level overlap is limited to the shared origin facade file itself.

If any single criterion is ambiguous or unverified, treat the pair as dependent and fall back to separate patches. Ambiguity favors safety, not speed.

### Patch composition limit

* a single patch may contain at most two independent islands from the same module-refactor pass;
* never combine three or more islands into one patch;
* a two-island patch must extract and gate the first island before starting the second; never interleave edits.

### What a two-island patch must contain

* one install block, with file list explicitly partitioned by island;
* one validate block, with per-island validation results reported separately before the combined ZIP contract marker;
* one freeze block and one freeze entry, with both islands explicitly named;
* a Batch Island Manifest;
* a pairwise independence result and rollback plan.

### Failure handling inside a two-island patch

* if Island A passes and Island B fails, prefer rolling back only Island B's files when this is clean;
* whole-ZIP rollback must always remain safe;
* if per-island rollback cannot cleanly isolate the failed island because both islands modify the same facade body, repair or roll back the whole ZIP and use smaller patches next;
* do not partially freeze a failed batch.

### Serial install/validate/freeze across separate patches

When islands are not paired into one patch, process them as separate patches in strict series:

```text
Patch A: install -> validate -> freeze
Patch B: install -> validate -> freeze
Patch C: install -> validate -> freeze
```

Never install patch A, B, and C and validate or freeze only at the end.

### Relationship to backlog parallel-safe batching

Backlog parallel-safe batching concerns different modules drafted concurrently. This layer concerns islands within one module. The two mechanisms do not stack permissions.

### Sequential double-refactor delivery train v7.1

A sequential double-refactor delivery train is a prepared series of separate governed patch ZIPs. It is allowed to reduce chat/download friction when several independent or dependency-ordered refactor patches can be prepared from the same AST-assisted candidate queue or roadmap. It is not one giant patch, not one giant freeze, and not permission to install several patches before validation.

Default safe train shape:

```text
Patch ZIP 1: slice A1 + optional related slice A2 -> install -> validate -> freeze
Patch ZIP 2: slice B1 + optional related slice B2 -> install -> validate -> freeze
Patch ZIP 3: slice C1 + optional related slice C2 -> install -> validate -> freeze
Patch ZIP 4: slice D1 + optional related slice D2 -> install -> validate -> freeze
```

Rules:

* a single assistant response may prepare up to four ordered inner patch ZIPs only when each ZIP is independently installable, validatable, contract-checkable, freeze-preppable, and freezeable;
* each inner patch ZIP may contain one refactor slice by default, or two tightly related slices when the Multi-Island Execution Layer proves they are independent or mechanically coupled and safer as one atomic patch;
* do not pack more than two substantive refactor slices into one governed patch ZIP;
* an exception for three or four micro-slices is allowed only when they are one mechanical atomic move, such as rename helper, update imports, move tests, and update manifest references, and the validation script names that atomic set;
* do not combine unrelated workflow surfaces in one ZIP just to reduce downloads;
* each inner patch must have its own feature id, install command, validate command, freeze command, validator, freeze hint, rollback boundary, and freeze entry;
* the delivery must include a train manifest or clearly ordered list stating Patch 1, Patch 2, Patch 3, and Patch 4, with predecessor dependency for each patch after the first;
* for one target module, Patch 2 is built against the result of Patch 1, Patch 3 is built against the result of Patch 2, and Patch 4 is built against the result of Patch 3;
* execution is strictly serial: install Patch 1 -> validate Patch 1 -> freeze Patch 1 before installing Patch 2;
* if any patch fails install, validation, ZIP contract validation, freeze-prep, or freeze preview, stop the train and do not install later patches;
* never freeze the train as one vague outer entry; freeze each inner patch separately with its own named islands/slices and evidence;
* do not use delivery trains to hide behavior changes, unrelated warning cleanup, cross-module ambiguity, or missing tests.

Unsafe model:

```text
install Patch 1
install Patch 2
install Patch 3
install Patch 4
validate everything only at the end
freeze everything as one vague entry
```

Safe model:

```text
Patch 1: install -> validate -> freeze
Patch 2: install -> validate -> freeze
Patch 3: install -> validate -> freeze
Patch 4: install -> validate -> freeze
```

Maximum guidance:

```text
Maximum per response: 4 ordered patch ZIPs.
Default maximum per ZIP: 2 related refactor slices.
Maximum total substantive slices in one train: 8, but only as four separately validated and separately frozen ZIPs.
Preferred practical limit: 1 or 2 ZIPs unless the roadmap is unusually clean.
```

The train may reduce download and chat friction, but it must not reduce traceability, attribution, rollback safety, validation evidence, or freeze quality.

## Delivery model

Use the active project delivery contract.

For KANDA/PyArchitect governed patch work:

* deliver a patch ZIP with Install, Validate, and Freeze instructions;
* a governed patch ZIP may contain one island, or up to two islands that passed the Multi-Island Execution Layer independence test;
* a sequential double-refactor delivery train may contain up to four ordered governed patch ZIPs in one response, but each inner patch must be installed, validated, ZIP-contract-checked, freeze-prepped, previewed, and frozen in strict sequence;
* stage transient install, extract, correction, validation-helper, and audit files under `<drive>/<project>_delete_after_daily_work`;
* do not put transient files in the active project root;
* keep delivery ZIP `payload/` structure as packaging only; do not make runtime source logic depend on zipped payload files or generated delivery artifacts;
* include a root-level `KANDA_FREEZE_HINT.json` when the patch is freezeable, naming every island the patch contains;
* do not write frozen memory before local validation passes for every island in the patch and the user confirms Confirm and Write;
* do not write one freeze entry for a delivery train; write one freeze entry per validated inner patch.

For non-governed projects, use the equivalent local validation and backup procedure, but still preserve source-truth, public API, rollback, and validation evidence.

## Backup and rollback guidance

Before risky extraction:

* use version control if available;
* create a baseline branch, tag, or checkpoint;
* keep per-phase rollback instructions;
* for multi-island patches, keep per-island rollback instructions distinct when possible;
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
* wide responsibility-island tests for every moved sub-area when wide mode is used, reported per-island when the patch contains two islands;
* helper manifest validation when helpers are created;
* circular import check when import graph changed;
* relevant tab/box validation;
* architecture validation with Errors 0 when project canon requires it;
* workflow validation when workflow behavior changed;
* local user validation before freeze.

For AST split audit tooling, minimum validation is:

* py_compile for the AST tool and GUI integration;
* import smoke for the AST tool without PySide;
* fixture-based AST audit proving symbol extraction, self-state detection, side-effect detection, candidate island grouping, report writing, and AI handoff generation;
* GUI source check proving Architecture Review exposes Run AST Split Audit and Copy Split Handoff for AI;
* freeze-hint contract check.

When optional tools are already configured, add Ruff, pytest coverage, pyright/mypy, import-linter, pyrefact, wily/radon, or pytest-xdist only as approved/configured.

## Post-refactor fragmentation audit

After large-module splitting or source-preserving facade work, run a read-only fragmentation audit before treating the refactor as safe.

The audit should report unresolved names, missing imports, runtime API imports missing after split, Qt/GUI symbols leaking into non-GUI helpers, dependency-direction violations, facade/helper binding gaps, symbols present in sibling helpers but not imported, import smoke failures, dumping-ground helpers, unnecessary micro-files, hyperpopulated helper families, and missed cross-island coupling in multi-island patches.

A large-module refactor is not ready for freeze until focused refactor tests pass, fragmentation audit has no critical unresolved findings, dependency-direction map has no unapproved violations, wide-mode islands are not generic dumping grounds, multi-island patches have no missed cross-island coupling, architecture validation has Errors 0, workflow validation has fail 0 when workflow behavior is touched, and the user validates locally.

## Approval gates

Approval flow:

```text
Task 0: audit only, including AST split audit evidence when available and multi-island candidate queue -> approval
Task 1: roadmap, decomposition, and patch composition decision -> approval
Task 2: implementation per cluster/island -> validation -> checkpoint
Final validation -> approval before freeze
```

Per-cluster approval is optional only when the user explicitly authorized continuous implementation. Validation after each cluster/island is mandatory.

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
* Do not let codemod, IDE-assisted, AST-assisted, or parallel-execution speed tooling skip or weaken a validation gate that manual extraction would otherwise require.
* Do not treat AST split audit output as automatic approval; it is evidence for AI/human review.
* Do not write AST audit reports into the active project root; use daily-work staging.
* Do not pair more than two substantive islands/slices in one governed patch ZIP.
* Do not pair two islands unless every Multi-Island Execution Layer independence criterion holds; ambiguity defaults to separate patches.
* Do not install multiple patches and validate or freeze only at the end.
* Do not deliver more than four ordered patch ZIPs in one sequential double-refactor train.
* Do not put more than two related refactor slices in one patch ZIP unless they are one documented mechanical atomic micro-slice set.
* Do not freeze a sequential train as one outer bundle; freeze every inner ZIP separately after its own validation.
* Do not proceed to the next train patch after any install, validation, ZIP contract, freeze-prep, preview, or freeze failure.
* Do not write a single vague freeze entry covering an unnamed combination of islands; every island in a patch must be named in its freeze entry.
* Do not let GUI signal rewiring travel inside a paired-island patch unless each island's signal scope was independently inventoried and shown not to overlap.
* Do not create 5-line or otherwise tiny helper files merely to reduce line count; merge tiny cohesive logic into the nearest responsibility helper unless a stable seam is documented.
* Do not treat the 400-line ideal as a reason to hyperpopulate the project with micro-files.
* Do not place normal runtime/source logic inside ZIP payload files or delivery-package folders; use ordinary `.py` modules and ordinary imports.

## Change log

* v5.8: Added post-refactor fragmentation audit requirement for helper-folder and source-preserving facade refactors.
* v5.9: Extended module-size law to new code module creation and clarified that the 400/500 line limit applies to code/source modules, not text/Markdown/documentation/prompt/manifest/JSON/log/report files.
* v6.0: Added import graph audit, characterization test planning, public API inventory, `__init__.py` re-export strategy, import compatibility matrix, `__all__` enforcement, circular import risk assessment, optional modern tooling integration, per-cluster validation, rollback details, and KANDA daily-work containment.
* v6.1: Added dependency-direction mapping before extraction, GUI-specific signal/widget inventory, optional pyright/mypy and import-linter boundary gates when configured, and first-pass public facade import preservation.
* v6.2: Added safe wide responsibility-island extraction mode, Mikado-style acceleration, explicit rejection of binary/line-range splitting, speed-mode assessment, patch sizing guidance, and wide-mode validation/stop conditions.
* v6.3: Added Speed Acceleration Layer covering tiered validation gates, codemod-assisted whole-symbol extraction with fixture-first verification, parallel test execution guidance, backlog parallel-safe batching, and audit-cache reuse.
* v7.0: Added AST-assisted heuristic split audit as a local read-only evidence tool, Multi-Island Execution Layer for at most two independent islands per patch, strict independence criteria using non-conflicting writes rather than impossible no-shared-read rules, per-island validation/freeze naming, daily-work audit staging, patch-train delivery bundles for multiple separate governed patches in one outer ZIP, and an explicit rule against stacking multiple patches before validation or freeze.
* v7.1: Replaced vague patch-train bundle wording with the sequential double-refactor delivery train protocol: up to four ordered patch ZIPs per response, each normally containing at most two related refactor slices, each with independent install, validation, ZIP contract, freeze-prep, freeze hint, freeze preview, Confirm and Write, and rollback boundary.
* v7.2: Added practical helper-file granularity and traditional source-file rules: cohesive helpers near the 400-line ideal are acceptable, needless micro-files should be avoided, refactor trains should stop when remaining helpers are small/cohesive, and normal runtime/source logic should live in ordinary importable `.py` files rather than ZIP payload/delivery structures.
