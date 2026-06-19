# Large Module Refactor Protocol

## Box Logic Requirement

Before any implementation, repair, refactor, prompt update, governance update, or bundle creation, the AI must:

- Identify the active box before implementation.
- State owner paths.
- State files allowed to change.
- State files explicitly out of scope.
- Declare cross-box touches.
- Preserve public contracts.
- Validate the active box and any touched external box.


Version: 5.8
Status: Large-module refactor protocol, unified delivery model
Use: Invoke when a relevant Python file is above 500 lines or the user opens a refactor pass.

Module-size law:
- Ideal: <= 400 lines.
- Maximum: <= 500 lines.
- Above 500 lines: split by responsibility.

Mandatory phases:
Task 0 - Audit only:
- inspect actual file;
- line count;
- public API;
- imports;
- side effects;
- owner box;
- current tests/checks;
- risk;
- proposed validation.
Stop and wait for approval.

Task 1 - Roadmap:
- propose helper folder;
- public API preservation plan;
- manifest plan;
- validator plan;
- tests/checks;
- rollback guidance;
- delivery ZIP contents.
Stop and wait for approval unless the user explicitly authorized implementation.

Task 2 - Implementation:
- create or update files in the sandbox;
- preserve project-relative paths;
- run available validation;
- package final files in one ZIP;
- include _bundle_temp\BUNDLE_MANIFEST_<task_slug>.txt;
- provide Windows validation commands.

Normal decomposition:
- Keep the origin file path and public imports stable.
- Extract by whole top-level private functions, whole internal classes, or whole methods.
- Do not slice statement blocks, loop bodies, or partial functions.
- Use sibling helper folder: <origin_stem>_help.
- Use clear helper names, not utils.py, helpers.py, misc.py, common.py, shared.py, temp.py.
- Define explicit __all__ for public exports.
- Avoid circular imports.

Source-preserving facade option:
Use only when semantic extraction is too risky, such as:
- huge public function;
- central CLI/module;
- previous whole-symbol extraction cannot reduce below 500 lines;
- public behavior must remain stable before deeper maintainability work.

Rules for source-preserving facade:
- Keep the original file as a small public facade.
- Store preserved implementation source in private helper shards.
- Use unique private source-part symbols.
- Keep each generated file below 500 lines.
- Do not duplicate exported shard symbols.
- Preserve behavior as a tactical stabilization step.
- Mark this as not a true maintainability refactor.
- Plan later semantic extraction if maintainability is the goal.

Delivery model:
- Do not create a required install script.
- Do not require a separate backup-script folder.
- Do not require the user to run a install script.
- Deliver the final origin file, helper files, manifests, validators, checks, and tests directly in the ZIP.
- The ZIP must extract directly into <PROJECT_ROOT>.
- The manifest goes in _bundle_temp.

Backup guidance:
For risky changes, advise the user to use version control or create a project
checkpoint before extracting the ZIP. Do not make the correction depend on a
custom install script.

Minimum validation:
- py_compile touched Python files;
- import smoke for the origin module when possible;
- helper manifest validation when helpers are created;
- relevant Tab/box validation;
- Tab 1/Tab 2 safety gates when project canon requires them.

Success markers should be reported in the manifest, not as install-script output.

Final rule:
One large-module target per pass. Audit first, roadmap second, implement after
approval, deliver one direct ZIP, wait for validation before freeze.


---

## v5.8 Addendum - Post-Refactor Fragmentation Audit

After large-module splitting or source-preserving facade work, run a read-only
fragmentation audit before treating the refactor as safe.

### Purpose

Large-module splits can leave unresolved names, missing imports, import leaks,
facade binding gaps, or helper modules that only work by accident. The audit must
find these before the user freezes the refactor.

### Read-only Task 0 audit runner

For complex helper-folder splits, design a Task 0 audit runner that performs:

```text
Phase 1: discover helper modules
Phase 2: AST-based name resolution per module
Phase 3: standard import, runtime API, GUI leak, and binding-gap detection
Phase 4: import smoke and targeted headless smoke when safe
Phase 5: Markdown + JSON report generation
```

The runner must not modify source. It should write reports only to the approved
maintenance/audit output area for that pass.

### Minimum findings

The audit should report:

- unresolved names;
- missing standard-library imports;
- runtime API imports missing after split;
- Qt/GUI symbols leaking into non-GUI helpers;
- facade/helper binding gaps;
- symbols present in sibling helpers but not imported;
- import smoke failures;
- helper files that are not safe to import standalone when the architecture
  expects facade-only import.

### False-positive guard

Before applying import-smoke results, ask whether helpers are intended to be
standalone importable or facade-only private shards. A source-preserving facade
may intentionally make helper shards private implementation details.

### Validation rule

A large-module refactor is not ready for freeze until:

```text
focused refactor tests pass
fragmentation audit has no critical unresolved findings
Tab 1 architecture validation has Errors 0
Tab 2 workflow validation has fail 0
user validates locally
```

### Change log

- v5.8: Added post-refactor fragmentation audit requirement for helper-folder and
  source-preserving facade refactors.
