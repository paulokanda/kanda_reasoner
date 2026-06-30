# Role & Objective

You are a Staff+ Python Architect and Reliability Engineer with 20 years of experience in large-scale, multi-layered production codebases. Your sole task is to produce a comprehensive, production-grade **cleanup plan** for the project described in the validation report below — a plan that is fast to execute (minimal manual effort) but safe, via test-gated, rollback-able batches.

You are not to perform any corrections yourself. Output the plan only.

<constraints>
- Do not modify, run, or simulate running any code.
- Errors must be corrected in their own isolated batch (Batch 0 or Batch 1), separate from any warning-level fixes, with their own dedicated test gate and rollback command. Do not combine error fixes with warning fixes in the same batch — this keeps the gate diagnostic if it fails.
- Within the warning batches, when issue categories are independent (e.g., MISSING_PUBLIC_SURFACE_CONTROL vs MODULE_TOO_LARGE touch different files), chunk them separately rather than combining into one large batch, so a failed gate narrows down to a small, identifiable set of changes.
- Every batch in the plan must have an explicit test gate and an explicit rollback command.
- When a finding is ambiguous (e.g., a "stale variant" that might still be load-bearing), default to a manual-review step rather than an automated fix.
- Target environment for all commands and paths: **Windows 11, PyCharm integrated terminal** (PowerShell syntax, not bash/macOS). Do not give Unix-only command forms (e.g., no bare `rm -rf`, no forward-slash-only path assumptions) without a Windows equivalent alongside.
- Keep the full response under ~2,500 words. Favor a tight, scannable plan over exhaustive prose — use tables and bullets, not paragraphs, wherever the structure below allows it.
</constraints>

---

# Required Research (before drafting)

Before writing the plan, you must search the internet for both of the following — don't rely solely on prior knowledge, since both tooling and recommended practice shift quickly:

**A. Toolchain research**
- Current state of fast Python toolchains: Ruff (lint + format), mypy (incremental mode), autoflake, isort, Vulture.
- Only cite tools/techniques you can verify are current and real — if you're not confident a tool exists or is still maintained, search to confirm before recommending it.

**B. Problem-specific solution research**
For each major issue category in the validation report (deprecated/stale variant handling, missing `__all__` at scale, misplaced tests, oversized modules, mixed-responsibility files, dead code detection, generated-artifact/manifest hygiene), search for how experienced teams or documented case studies have actually solved that specific problem — not just which linter flags it. Look at engineering blogs, PyCQA/Real Python writeups, and Stack Overflow threads on the concrete mechanics (e.g., "safe way to retire a stale code variant still referenced elsewhere," "automating `__all__` generation across a large codebase," "splitting a 2000-line module without breaking imports").

Cite at least 3 specific sources (with URLs) total across A and B that informed your recommendations.

---

<validation_report>
Source: `manage_architecture.py --validate`

## Summary

Issue codes present (severity in parentheses):
DEPRECATED_VARIANT_STILL_REFERENCED (error)

BUNDLE_SAFETY (error)

MISSING_PUBLIC_SURFACE_CONTROL (warning)

MISPLACED_TEST (warning)

GENERATED_ARTIFACT_CONTRACT (warning)

MODULE_TOO_LARGE (warning)

MIXED_RESPONSIBILITY_FILE (warning)

TEST_ASSERTS_INTERNAL_DETAIL (warning)

PROJECT_WIDE_AI_CONFUSION (warning)

DEAD_CODE_UNREACHABLE_FILE (warning)

TEST_PROTECTION_GAP (warning)

PUBLIC_API_INSTABILITY (warning)

HELPER_MANIFEST_CONTRACT (warning)

SIDE_EFFECT_ON_IMPORT (warning)

STALE_VARIANT_SOURCE_OF_TRUTH (warning)

UNSAFE_PATH_PLATFORM_ASSUMPTION (warning)

SYMBOL_SHADOWING (warning)
Noise hint: some findings are stale/reference-source signals — review exclusion rules before starting.
Top issue path groups (highest concentration first, exact figures omitted as they vary per run):

kanda_reasoner_app

validation

_bundle_temp

kanda_prompt_workspace

tests

## Errors (fix first)
1. **BUNDLE_SAFETY** — `project_freeze_after_update.zip` contains a bundle manifest outside accepted folders: `project_freeze_after_update/_patch_manifests/BUNDLE_MANIFEST_freeze_after_update_bom_index_tolerance_freeze_entry_v3_repair.txt`. Risk: manifest may be installed into runtime folders or missed by governance.
2. **DEPRECATED_VARIANT_STILL_REFERENCED**: `kanda_reasoner_app/local_ai_json_working_copy.py` (referenced by `enrichment_writer`, `runtime_controller`); `kanda_reasoner_app/reasoner_context_bundle/source_archive_exporter.py` (referenced by `handoff_zip_exporter`). Risk: runtime may depend on a stale variant.

## Representative warnings (key categories, full list omitted for brevity)
- MISSING_PUBLIC_SURFACE_CONTROL — modules lack `__all__`.
- MISPLACED_TEST — tests outside canonical `tests/` folder, or testing stale variants.
- GENERATED_ARTIFACT_CONTRACT — bundle manifests outside accepted folders.
- MODULE_TOO_LARGE — modules over 500 lines, some well over 2000.
- MIXED_RESPONSIBILITY_FILE — files mixing UI, AI, and business logic.
- TEST_ASSERTS_INTERNAL_DETAIL — tests depending on private implementation.
- PROJECT_WIDE_AI_CONFUSION — signals likely to mislead AI/dev readers of the codebase.
- DEAD_CODE_UNREACHABLE_FILE — no imports, no test coverage.
- TEST_PROTECTION_GAP — important modules with no direct test imports.
- PUBLIC_API_INSTABILITY — re-exports from modules lacking `__all__`.
- Other: HELPER_MANIFEST_CONTRACT, SIDE_EFFECT_ON_IMPORT, STALE_VARIANT_SOURCE_OF_TRUTH, UNSAFE_PATH_PLATFORM_ASSUMPTION, SYMBOL_SHADOWING.
</validation_report>

---

# Context to Gather

If any of the following aren't already known, ask for them in a single short list at the start of your response. For anything not answered, proceed with a clearly stated reasonable assumption rather than blocking the plan:

1. Python version and major dependencies (e.g., 3.11, PySide6).
2. Test framework, current pass/fail status, approximate coverage.
3. Git status: repo confirmed, any uncommitted changes.
4. Approximate project size (file count, LOC).
5. CI/CD: pipeline exists? what does it check?

Then produce the full plan in the same response — don't wait for a reply before delivering it.

---

# Delivery Format Requirement

Every batch's corrections must be packaged and delivered as a single ZIP following this exact three-part contract — no isolated patch ZIPs without all three parts:

1. **Install** — a script/step that applies the batch's file changes into the project (with a clear list of exactly which files are added/modified/removed).
2. **Validate** — the exact command(s) to re-run `manage_architecture.py --validate` (and any relevant test/lint commands) to confirm the batch succeeded, plus the expected passing markers/output to look for.
3. **Freeze** — the step that records the validated state (consistent with the project's existing freeze-memory convention) only after the validate step has passed — never freeze before validation succeeds.

All commands in this section must use Windows 11 / PowerShell syntax runnable from the PyCharm integrated terminal.

---

# Required Output Structure

## 1. Problem Taxonomy & Priority Matrix
Table: issue category → Critical/Major/Minor → fix effort (Low/Med/High) → automation level (Full/Partial/Manual).

## 2. Chunked Execution Plan (3–5 batches)
Per batch:
- Scope (categories + files/modules)
- Why this batch precedes the next
- Automation strategy (tools used; what stays manual)
- Performance optimizations (parallelism, incremental checks, safe `--fix` use)
- Test gate (exact PowerShell commands)
- Rollback command (exact Git/file-restore command, PowerShell syntax)
- Delivery ZIP contents per the Install / Validate / Freeze contract above

## 3. Recommended Toolchain
Specific tools + commands per problem type, install commands, relevant config snippets. Flag which are fastest for this project's scale. Windows/PyCharm-terminal command forms only.

## 4. Step-by-Step Walkthrough
Phase 0 (prep/branch/baseline) → Phase 1 (quick wins) → Phase 2 (structural fixes) → Phase 3 (deep refactors) → Phase 4 (final validation, target: 0 errors).

## 5. Quality Exit Criteria
Per phase: exact pass conditions before advancing.

## 6. Emergency Stop & Recovery
Red flags that halt the process; exact Git/PowerShell commands to revert to last known good state.

---

# Final Output Format

Markdown. Open with a short executive summary describing the overall scale and severity mix 
(e.g., "a small number of hard errors plus a large volume of structural warnings"), 
the number of batches, and estimated total effort in person-hours.



-------------------

A small number of hard errors are blocking validation, but most findings are structural warnings. I would run this as 5 small, rollback-able batches, with errors isolated first, then warning families split by independence. Estimated effort: 18-32 person-hours if existing tests are healthy; 40+ hours if stale variants require behavior-preserving migration.

Missing context I would confirm before execution, but not block the plan: Python version, pytest/coverage baseline, Git cleanliness, LOC/file count, and CI checks. Assumption: Python 3.10+, PySide6, Git repo, pytest available, project root E:\kanda_reasoner.

Sources used: validation report shows 379 issues: 3 errors and 376 warnings, with errors in BUNDLE_SAFETY and DEPRECATED_VARIANT_STILL_REFERENCED. Ruff is current as a fast linter/formatter, mypy supports incremental cache and daemon mode, autoflake removes unused imports/variables, Vulture detects dead/unreachable code with confidence levels, Real Python recommends focused __all__, and pytest documents standard test discovery.

1. Problem Taxonomy & Priority Matrix
Issue category	Priority	Effort	Automation
BUNDLE_SAFETY	Critical	Low	Partial
DEPRECATED_VARIANT_STILL_REFERENCED	Critical	Med-High	Manual
GENERATED_ARTIFACT_CONTRACT / HELPER_MANIFEST_CONTRACT	Major	Low-Med	Partial
MISSING_PUBLIC_SURFACE_CONTROL / PUBLIC_API_INSTABILITY	Major	Med	Partial
MISPLACED_TEST / TEST_ASSERTS_INTERNAL_DETAIL / TEST_PROTECTION_GAP	Major	Med	Partial
DEAD_CODE_UNREACHABLE_FILE / STALE_VARIANT_SOURCE_OF_TRUTH	Major	Med	Manual-first
SIDE_EFFECT_ON_IMPORT / UNSAFE_PATH_PLATFORM_ASSUMPTION / SYMBOL_SHADOWING	Minor-Major	Low	Partial
MODULE_TOO_LARGE / MIXED_RESPONSIBILITY_FILE	Major	High	Manual
PROJECT_WIDE_AI_CONFUSION	Major	Derived	No direct fix
2. Chunked Execution Plan
Batch 0 — Error-only: bundle safety
Field	Plan
Scope	Fix only project_freeze_after_update.zip manifest placement: move/relocate manifest into accepted manifest folder or exclude it from runtime bundle.
Why first	Validation cannot pass while bundle contract is unsafe. Keep separate from stale-code errors so failure is diagnostic.
Automation	Scripted ZIP repack + manifest-location assertion. Manual review of accepted folder rule.
Test gate	See commands below.
Rollback	git reset --hard cleanup-pre-b0; git clean -fd -- .\workbench\cleanup_batch_0 .\project_freeze_after_update\freeze_hint_intake
ZIP contents	install_batch_0.ps1, changed bundle artifact only, validate_batch_0.ps1, KANDA_FREEZE_HINT.json.
$PROJECT_ROOT = "E:\kanda_reasoner"
Set-Location $PROJECT_ROOT
git tag cleanup-pre-b0 -f
.\workbench\cleanup_batch_0\install_batch_0.ps1
python .\kanda_reasoner_app\manage_architecture\manage_architecture.py --root $PROJECT_ROOT --validate

Expected: BUNDLE_SAFETY: 0 errors; remaining errors should only be deprecated-variant references.

Freeze after validation only:

python .\scripts\merge_freeze_validation_evidence.py --project-root $PROJECT_ROOT --feature-id cleanup-batch-0-bundle-safety
Batch 1 — Error-only: stale referenced variants
Field	Plan
Scope	local_ai_json_working_copy.py referenced by enrichment_writer, runtime_controller; source_archive_exporter.py referenced by handoff_zip_exporter; update tests importing stale targets.
Why now	These are the remaining hard errors and high AI-confusion signals.
Automation	Manual source-of-truth decision first. Either rename to canonical module and update imports, or mark as intentional canonical despite filename via explicit architecture contract/exclusion. Do not auto-delete.
Test gate	Architecture validation plus targeted import tests.
Rollback	git reset --hard cleanup-pre-b1; git clean -fd -- .\workbench\cleanup_batch_1 .\project_freeze_after_update\freeze_hint_intake
ZIP contents	Modified import owners/tests, optional canonical wrapper modules, migration notes, validate/freeze scripts.
$PROJECT_ROOT = "E:\kanda_reasoner"
Set-Location $PROJECT_ROOT
git tag cleanup-pre-b1 -f
.\workbench\cleanup_batch_1\install_batch_1.ps1
python -m pytest .\tests\test_reasoner_static_import_contracts_01.py .\tests\test_show_project_to_ai_hybrid_source_archive_export_v1.py -q
python .\kanda_reasoner_app\manage_architecture\manage_architecture.py --root $PROJECT_ROOT --validate

Expected: Errors: 0. Do not proceed to warnings until this is true. The stale modules are explicitly shown as referenced in runtime/test paths.

Batch 2 — Generated artifacts, manifests, side effects, path hygiene
Field	Plan
Scope	_bundle_temp, kanda_prompt_workspace\prompt_library\_bundle_temp, helper manifest drift, top-level sys.path.insert, non-ASCII source, symbol shadowing.
Why	Low-risk cleanup reduces noise before API and test batches.
Automation	Move generated manifests to accepted folders or exclude; update helper JSON manifests from __all__; move sys.path.insert into main(); replace non-ASCII chars in Python source.
Test gate	Architecture validation and script import smoke tests.
Rollback	git reset --hard cleanup-pre-b2; git clean -fd -- .\workbench\cleanup_batch_2 .\project_freeze_after_update\freeze_hint_intake
ZIP contents	Manifest moves, helper JSON edits, import-safe script edits, validate/freeze scripts.
$PROJECT_ROOT = "E:\kanda_reasoner"
Set-Location $PROJECT_ROOT
git tag cleanup-pre-b2 -f
.\workbench\cleanup_batch_2\install_batch_2.ps1
python -m pytest .\tests -q --maxfail=1
python .\kanda_reasoner_app\manage_architecture\manage_architecture.py --root $PROJECT_ROOT --validate

Expected: no GENERATED_ARTIFACT_CONTRACT, no HELPER_MANIFEST_CONTRACT, no SIDE_EFFECT_ON_IMPORT, no UNSAFE_PATH_PLATFORM_ASSUMPTION, no SYMBOL_SHADOWING.

Batch 3 — Public surface and test placement
Field	Plan
Scope	MISSING_PUBLIC_SURFACE_CONTROL, PUBLIC_API_INSTABILITY, MISPLACED_TEST, TEST_ASSERTS_INTERNAL_DETAIL, TEST_PROTECTION_GAP.
Why	Stable APIs should precede deep refactors. Tests should protect public behavior, not private internals.
Automation	Generate candidate __all__ from public names, but require review before write; relocate validation tests only if project policy agrees; add direct public-contract import tests.
Performance	Run Ruff check on touched files only; run pytest on moved/added tests first.
Rollback	git reset --hard cleanup-pre-b3; git clean -fd -- .\workbench\cleanup_batch_3 .\project_freeze_after_update\freeze_hint_intake
ZIP contents	__all__ edits, test moves or policy exclusions, new public-contract tests, validate/freeze scripts.
$PROJECT_ROOT = "E:\kanda_reasoner"
Set-Location $PROJECT_ROOT
git tag cleanup-pre-b3 -f
.\workbench\cleanup_batch_3\install_batch_3.ps1
ruff check .\kanda_reasoner_app .\tests
python -m pytest .\tests -q --maxfail=1
python .\kanda_reasoner_app\manage_architecture\manage_architecture.py --root $PROJECT_ROOT --validate

Expected: MISSING_PUBLIC_SURFACE_CONTROL substantially reduced or zero; no new errors.

Batch 4 — Structural refactors: large/mixed modules and dead code
Field	Plan
Scope	MODULE_TOO_LARGE, MIXED_RESPONSIBILITY_FILE, DEAD_CODE_UNREACHABLE_FILE, remaining PROJECT_WIDE_AI_CONFUSION.
Why last	Highest risk; needs stable tests and explicit public APIs first.
Automation	Manual slicing by responsibility: GUI shell, transport adapter, pure business logic, file IO. Vulture only as advisory because dynamic imports/plugins cause false positives.
Rollback	git reset --hard cleanup-pre-b4; git clean -fd -- .\workbench\cleanup_batch_4 .\project_freeze_after_update\freeze_hint_intake
ZIP contents	One module family per ZIP subfolder, compatibility re-export shims, focused tests, validate/freeze scripts.
$PROJECT_ROOT = "E:\kanda_reasoner"
Set-Location $PROJECT_ROOT
git tag cleanup-pre-b4 -f
.\workbench\cleanup_batch_4\install_batch_4.ps1
python -m pytest .\tests -q
mypy .\kanda_reasoner_app --cache-dir .\.mypy_cache
python .\kanda_reasoner_app\manage_architecture\manage_architecture.py --root $PROJECT_ROOT --validate

Expected: no errors; warnings reduced with no public import breakage.

3. Recommended Toolchain

Install in the project venv:

$PROJECT_ROOT = "E:\kanda_reasoner"
Set-Location $PROJECT_ROOT
python -m pip install --upgrade ruff mypy autoflake isort vulture pytest pytest-cov

pyproject.toml starter:

[tool.ruff]
target-version = "py310"
line-length = 88
extend-exclude = ["_bundle_temp", "workbench", "project_freeze_after_update"]

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B"]
ignore = []

[tool.mypy]
python_version = "3.10"
cache_dir = ".mypy_cache"
ignore_missing_imports = true

Fast commands:

ruff check .\kanda_reasoner_app .\tests
ruff check .\kanda_reasoner_app .\tests --fix
ruff format .\kanda_reasoner_app .\tests
mypy .\kanda_reasoner_app --cache-dir .\.mypy_cache
vulture .\kanda_reasoner_app .\tests --min-confidence 90
autoflake --remove-all-unused-imports --remove-unused-variables --recursive --in-place .\kanda_reasoner_app

Use autoflake and ruff --fix only on clean Git branches. isort is optional if Ruff’s import sorting is enabled; isort remains useful when you want dedicated import-only changes.

4. Step-by-Step Walkthrough

Phase 0 — Prep

$PROJECT_ROOT = "E:\kanda_reasoner"
Set-Location $PROJECT_ROOT
git status --short
git switch -c cleanup-architecture-20260628
git tag cleanup-start -f
python .\kanda_reasoner_app\manage_architecture\manage_architecture.py --root $PROJECT_ROOT --validate *> .\workbench\architecture_baseline.txt

Phase 1 — Quick wins: Batch 0, Batch 2.

Phase 2 — Hard source-truth: Batch 1.

Phase 3 — Public contract and tests: Batch 3.

Phase 4 — Deep refactor: Batch 4. Split only one large/mixed module family per sub-batch; preserve compatibility imports until all tests pass.

5. Quality Exit Criteria
Phase	Pass condition
Phase 0	Baseline captured; Git branch clean except baseline artifact.
Batch 0	BUNDLE_SAFETY error gone; no new deprecated-variant changes.
Batch 1	Errors: 0 from architecture validation.
Batch 2	Artifact/manifest/import-side-effect/path warnings removed or explicitly excluded.
Batch 3	Public API warnings reduced; pytest passes; no private-detail regression.
Batch 4	No errors; module-size/mixed warnings reduced; no public imports broken.
Final	manage_architecture.py --validate exits 0, or exits nonzero only for documented accepted warnings.
6. Emergency Stop & Recovery

Stop immediately if any occurs:

Architecture errors increase.
A stale variant is found to be runtime-critical but has no canonical replacement.
GUI import smoke test fails after API changes.
Freeze hint says pending validation after validation passed.
Generated files land in runtime folders.

Recovery:

$PROJECT_ROOT = "E:\kanda_reasoner"
Set-Location $PROJECT_ROOT
git status --short
git reset --hard cleanup-start
git clean -fd -- .\workbench .\project_freeze_after_update\freeze_hint_intake
python .\kanda_reasoner_app\manage_architecture\manage_architecture.py --root $PROJECT_ROOT --validate

For a single failed batch:

$PROJECT_ROOT = "E:\kanda_reasoner"
Set-Location $PROJECT_ROOT
git reset --hard cleanup-pre-b<N>
git clean -fd -- .\workbench\cleanup_batch_<N> .\project_freeze_after_update\freeze_hint_intake

Do not freeze any batch unless its validation gate has passed and the batch ZIP includes Install + Validate + Freeze in the same delivery package.