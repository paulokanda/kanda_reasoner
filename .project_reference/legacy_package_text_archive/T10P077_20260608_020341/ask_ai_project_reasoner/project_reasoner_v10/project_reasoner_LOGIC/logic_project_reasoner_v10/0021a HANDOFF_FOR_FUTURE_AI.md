# HANDOFF_FOR_FUTURE_AI.md

## Purpose

This repository has already gone through a substantial cleanup and staged refactor. A future AI should treat the current state as the new baseline and avoid reintroducing legacy names, duplicate logic, or oversized root modules.

The main goals achieved were:

- remove `v10_` prefixes from several core modules without breaking imports
- refactor oversized modules into thin public shells plus helper packages
- create a curated root package API in `project_reasoner_v10/__init__.py`
- keep public behavior stable while improving file structure
- make manifest validation pass for the refactored modules
- keep compile checks and import checks green after each step

The current codebase is already in a stable, validated state after these changes.

---

## 1. Renames that were completed

### 1.1 `v10_query_router.py` → `query_router.py`

This rename was completed safely.

What was done:
- file renamed
- imports rewritten across the package
- compile sweep passed
- symbol checks confirmed `route_query_intent` and `QueryRouteDecision` still exist
- leftover help-text references were cleaned where needed

Current canonical module:
- `kanda_reasoner_app/project_reasoner_v10/query_router.py`

Important public exports:
- `QueryRouteDecision`
- `route_query_intent`

---

### 1.2 `v10_help_index.py` → `help_index.py`

This rename was completed safely.

What was done:
- file renamed
- imports rewritten
- compile checks passed
- import check confirmed the module now resolves as `help_index.py`
- actual public contract is `HELP_INDEX`

Important note:
- `VALIDATED_QUESTION_EXAMPLES` was not a real public symbol in the live module
- the actual public data contract is `HELP_INDEX`

Current canonical module:
- `kanda_reasoner_app/project_reasoner_v10/help_index.py`

Current public export:
- `HELP_INDEX`

---

### 1.3 `v10_ai_bridge.py` → `ai_bridge.py`

This rename was completed safely.

What was done:
- file renamed
- imports rewritten
- help text references cleaned
- compile and import checks passed
- `LocalAIReasoner` remained available

Current canonical module:
- `kanda_reasoner_app/project_reasoner_v10/ai_bridge.py`

Important public exports:
- `AIWorkerBridge`
- `LocalAIReasoner`

---

### 1.4 `v10_prompt_builder.py` → `prompt_builder.py`

This rename was completed safely.

What was done:
- file renamed
- imports rewritten
- test imports fixed
- help text references cleaned
- compile/import checks passed
- `PromptBuilder` remained available

Current canonical module:
- `kanda_reasoner_app/project_reasoner_v10/prompt_builder.py`

Important public exports / compatibility helpers retained:
- `PromptBuilder`
- `_build_answer_style_instructions`
- `_tokenize_query`
- `is_which_method_calls_question`

---

### 1.5 `v10_index_loader.py` → `index_loader.py`

This rename was completed safely.

What was done:
- file renamed
- imports rewritten
- root package curated API mapping fixed
- affected tests updated
- stale top comment updated
- direct import and root-package import both passed
- no leftover `v10_index_loader` references remained

Current canonical module:
- `kanda_reasoner_app/project_reasoner_v10/index_loader.py`

Important public export:
- `JsonProjectIndex`

---

### 1.6 `v10_project_profile.py` → `project_profile.py`

This rename was completed safely.

What was done:
- file renamed
- imports rewritten
- root package curated API mapping fixed
- leftover `v10_project_profile` references removed from `__init__.py`
- direct and root imports both passed

Current canonical module:
- `kanda_reasoner_app/project_reasoner_v10/project_profile.py`

Important public exports:
- `ProjectProfile`
- `GENERIC_PROJECT_PROFILE`
- `get_project_profile`
- `iter_project_profiles`
- `infer_project_profile`
- `infer_project_profile_name_from_metadata`

---

## 2. Major refactors that were completed

### 2.1 `ai_bridge.py` refactor

This was a full help-folder refactor.

Goal:
- reduce a very large orchestration file into a thin public shell
- isolate prompt parsing, prompt mode classification, deterministic answering, focus snippet selection, and grounding validation

What was created:
- `ai_bridge.py` kept as the public shell
- `ai_bridge_help/bridge_signals.py`
- `ai_bridge_help/prompt_extraction.py`
- `ai_bridge_help/prompt_modes.py`
- `ai_bridge_help/focus_snippets.py`
- `ai_bridge_help/deterministic_answers.py`
- `ai_bridge_help/grounding_checks.py`
- `ai_bridge_help.json`
- `ai_bridge_validate_manifests.py`

What stayed in `ai_bridge.py`:
- `AIWorkerBridge`
- `LocalAIReasoner`
- shell orchestration behavior
- completion handling
- wrapper calls into helper modules

Validation status:
- helper modules compiled
- manifest validator passed for `ai_bridge_help.json`

Current canonical public module:
- `ai_bridge.py`

Current helper package:
- `ai_bridge_help/`

---

### 2.2 `help_index.py` refactor

This was a data-module refactor.

Goal:
- remove the huge root-level `HELP_INDEX` literal from the public file
- preserve `HELP_INDEX` as the public contract
- normalize repeated mojibake text patterns at load time

What was created:
- `help_index.py` as a thin public facade
- `help_index_help/__init__.py`
- `help_index_help/help_index_raw.py`
- `help_index_help/help_index_normalization.py`
- `help_index_help/help_index_data.py`

Behavior preserved:
- callers still import `HELP_INDEX` from `help_index.py`

Validation status:
- all help-index helper files compiled successfully

Current canonical public module:
- `help_index.py`

Current helper package:
- `help_index_help/`

---

### 2.3 `prompt_builder.py` refactor

This was a full helper split, but compatibility-sensitive.

Goal:
- keep `PromptBuilder` as the public entry point
- move classification, answer-style rules, call-site prioritization, widget registry formatting, and generic prompt section assembly into helpers

What was created:
- `prompt_builder.py` as orchestrator
- `prompt_builder_help/__init__.py`
- `prompt_builder_help/prompt_classification.py`
- `prompt_builder_help/answer_style.py`
- `prompt_builder_help/callsite_evidence.py`
- `prompt_builder_help/prompt_sections.py`
- `prompt_builder_help/widget_registry_section.py`

Backward compatibility preserved:
- `_norm`
- `_tokenize_query`
- `_build_answer_style_instructions`
- `is_which_method_calls_question`

Validation status:
- all helper modules compiled
- direct imports and root imports worked

Current canonical public module:
- `prompt_builder.py`

Current helper package:
- `prompt_builder_help/`

---

### 2.4 `index_loader.py` refactor

This was a full helper split around a large passive loader.

Goal:
- keep `JsonProjectIndex` as the public owner
- split repetitive state initialization, section loading, path normalization, and index building

What was created:
- `index_loader.py` as public shell
- `index_loader_help/__init__.py`
- `index_loader_help/state_init.py`
- `index_loader_help/section_loading.py`
- `index_loader_help/path_resolution.py`
- `index_loader_help/index_builders.py`

Behavior preserved:
- `JsonProjectIndex` remains the public loader class
- `_build_*` methods remain available as delegating wrappers

Validation status:
- all helper modules compiled
- direct and root-package imports passed

Current canonical public module:
- `index_loader.py`

Current helper package:
- `index_loader_help/`

---

### 2.5 `project_profile.py` refactor

This was a clean responsibility split.

Goal:
- separate profile data type, built-in profiles, registry access, and inference
- keep `project_profile.py` as the public facade

What was created:
- `project_profile.py` as facade
- `project_profile_help/__init__.py`
- `project_profile_help/profile_types.py`
- `project_profile_help/built_in_profiles.py`
- `project_profile_help/registry.py`
- `project_profile_help/inference.py`

Behavior preserved:
- all previously useful public names remain available from `project_profile.py`

Validation status:
- all helper modules compiled
- direct and root imports passed

Current canonical public module:
- `project_profile.py`

Current helper package:
- `project_profile_help/`

---

### 2.6 `reasoner_retriever.py` refactor state

This module went through earlier restructuring and is now already in public-shell form.

Important state:
- it already delegates most heavy behavior to `reasoner_retriever_help/*`
- a later pass on it was intentionally a light refactor only
- no more helper modules were added in the last pass
- `ProjectRetriever` remains the canonical owner
- wrapper methods were preserved

Current canonical public module:
- `reasoner_retriever.py`

Current helper package:
- `reasoner_retriever_help/`

---

## 3. Root package API work

A curated root package API was added to:

- `kanda_reasoner_app/project_reasoner_v10/__init__.py`

Goals:
- expose a stable root-level public API
- keep runtime lazy-ish behavior
- keep IDE support and root imports working
- avoid accidental side effects from a giant package initializer

The root package now exposes a curated public surface including:
- `JsonProjectReasonerV10`
- `main`
- `JsonProjectIndex`
- `ProjectRetriever`
- `LocalAIReasoner`
- `AIWorkerBridge`
- `QueryRouteDecision`
- `route_query_intent`
- `HELP_INDEX`
- `EvidenceItem`
- `SymbolEvidenceItem`
- `RetrievalBundle`
- `ConversationTurn`
- `ProjectProfile`
- `GENERIC_PROJECT_PROFILE`
- `get_project_profile`
- `iter_project_profiles`
- `infer_project_profile`
- `infer_project_profile_name_from_metadata`

This root API was validated by runtime import checks during the rename/refactor work.

---

## 4. Manifest and validator work

A project-wide manifest validation cleanup was also performed.

What happened:
- the validator initially failed because of BOM handling and legacy compliance issues
- the validator was fixed to read helper modules safely
- missing AI CONTEXT docstrings and helper headers were corrected where required
- `reasoner_retriever.py` was restored to a known-good refactored version after a broken docstring edit
- final validator state became green for the tracked refactored modules

Current validator result:
- `ai_bridge_help.json` passes
- `ai_reasoner_main_window_help.json` passes
- `reasoner_retriever_help.json` passes

A future AI should not reopen those manifest fixes unless there is a real regression.

---

## 5. Current canonical file map

These are now the canonical file names to use in all future edits and explanations:

- `query_router.py`
- `help_index.py`
- `ai_bridge.py`
- `prompt_builder.py`
- `index_loader.py`
- `project_profile.py`
- `reasoner_retriever.py`

Legacy names with `v10_` for those modules should not be reintroduced.

---

## 6. Current helper package map

The current helper folders now in use are:

- `ai_bridge_help/`
- `help_index_help/`
- `prompt_builder_help/`
- `index_loader_help/`
- `project_profile_help/`
- `reasoner_retriever_help/`
- `main_window_help/`

Future AI should prefer extending these helper packages rather than stuffing logic back into the public shell modules.

---

## 7. What is already validated

The following categories have already been validated repeatedly through terminal checks:

### Compile checks
These passed after the refactors and renames:
- renamed public modules
- new helper modules
- curated root package
- affected tests for renamed modules

### Import checks
These passed:
- direct module imports
- root package imports
- public symbol checks for key modules

### Validator checks
These passed:
- `ai_bridge_help.json`
- `ai_reasoner_main_window_help.json`
- `reasoner_retriever_help.json`

### Functional smoke checks previously used during retrieval work
These question families were used earlier as smoke/regression checks for retriever behavior:
- startup chain
- topomap rendering
- package metadata lookup
- documentation intent lookup
- exact locator queries
- caller queries
- close-button signal connection questions

A future AI should reuse those smoke patterns when changing retrieval or routing behavior.

---

## 8. Known remaining issue

There is a pre-existing warning still visible in compile sweeps:

- `ai_reasoner_main_window.py` emits a `SyntaxWarning: invalid escape sequence '\d'`

Cause:
- the AI CONTEXT decorative docstring contains Windows paths like `E:\developer_tools\...` inside a normal triple-quoted string

Important:
- this is a warning, not a current break
- the module still imports and compile sweeps still pass
- it was intentionally not reopened during rename/refactor work because it is unrelated to the structural changes and the module remains functional

A future AI may fix it later by converting that top docstring to a raw string or escaping backslashes properly, but it is not blocking.

---

## 9. What future AI should not do

A future AI should avoid these mistakes:

### Do not reintroduce legacy names
Do not recreate imports pointing to:
- `v10_query_router`
- `v10_help_index`
- `v10_ai_bridge`
- `v10_prompt_builder`
- `v10_index_loader`
- `v10_project_profile`

### Do not collapse helper packages back into giant root modules
The public shell modules have already been intentionally slimmed.

### Do not refactor `reasoner_retriever.py` into more helper packages right now
It is already in the intended shell state and only needed a light cleanup.

### Do not replace the curated root API with an empty `__init__.py`
The root package is now deliberately curated and validated.

### Do not assume `help_index.py` exports `VALIDATED_QUESTION_EXAMPLES`
The real contract is `HELP_INDEX`.

### Do not reopen manifest cleanup unless validation fails again
The validator state is already green for the tracked refactored modules.

---

## 10. Recommended future workflow for more changes

If a future AI continues refactoring this codebase, the safe pattern is:

1. rename first if needed
2. rewrite imports package-wide
3. compile-check the renamed module
4. test direct import
5. test root package import if the symbol is curated in `__init__.py`
6. only then refactor into helper packages
7. re-run validator if the module participates in manifest-governed refactor structure

This rename-then-validate workflow already worked well across multiple modules in this repository.

---

## 11. Suggested current architecture snapshot for future AI

Use this as the short mental model:

- `ai_reasoner_main_window.py` = GUI orchestration entry point, already refactored via `main_window_help/`
- `reasoner_retriever.py` = public retrieval shell over `reasoner_retriever_help/`
- `ai_bridge.py` = public local AI shell over `ai_bridge_help/`
- `prompt_builder.py` = public prompt assembly shell over `prompt_builder_help/`
- `index_loader.py` = public JSON index loader shell over `index_loader_help/`
- `project_profile.py` = public profile facade over `project_profile_help/`
- `help_index.py` = public `HELP_INDEX` facade over `help_index_help/`
- `query_router.py` = live query intent router, already renamed and in canonical location

---

## 12. Exact summary for a future AI to follow

The repository has already completed a staged cleanup. Several `v10_*` modules were renamed to canonical names: `query_router.py`, `help_index.py`, `ai_bridge.py`, `prompt_builder.py`, `index_loader.py`, and `project_profile.py`. These renames were validated by compile checks, import checks, and root-package checks. The public package `project_reasoner_v10/__init__.py` now exposes a curated API and must remain consistent with the canonical module names. Several large modules were refactored into thin public shells plus helper packages: `ai_bridge_help`, `help_index_help`, `prompt_builder_help`, `index_loader_help`, and `project_profile_help`. `reasoner_retriever.py` is already in shell form over `reasoner_retriever_help` and should not be decomposed further unless there is a strong reason. Manifest validation for `ai_bridge_help.json`, `ai_reasoner_main_window_help.json`, and `reasoner_retriever_help.json` is green and should not be reopened casually. The main remaining known issue is a non-blocking `SyntaxWarning` in `ai_reasoner_main_window.py` caused by Windows paths inside a docstring. Future edits should extend helper packages rather than repacking logic into the public shell modules.

---

## 13. Exact public contracts by module

### `query_router.py`
Role:
- central question-intent router
- classifies prompts into deterministic, generative, listing, signal/action, or explanation-style routes

Expected public surface:
- `QueryRouteDecision`
- `route_query_intent`
- route-related helper predicates already exported in `__all__`

Important:
- this file is already renamed and in canonical location
- future edits should preserve route ordering unless there is a strong, tested reason to change it

---

### `help_index.py`
Role:
- public help-data entry point for the UI

Expected public surface:
- `HELP_INDEX` only

Current structure:
- thin facade over `help_index_help/`
- raw giant data moved out of the root file
- normalization layer added to improve garbled text handling

Important:
- do not re-expand this into a huge literal in the root file
- the contract is the `HELP_INDEX` object, not a family of exported helper constants

---

### `ai_bridge.py`
Role:
- public orchestration shell for local AI interaction
- responsible for deterministic fast paths, generative handoff, and grounding rejection handling

Expected public surface:
- `AIWorkerBridge`
- `LocalAIReasoner`

Current structure:
- public shell in `ai_bridge.py`
- implementation details in `ai_bridge_help/`

Helper ownership:
- `bridge_signals.py` = bridge class
- `prompt_extraction.py` = parse evidence pack structure
- `prompt_modes.py` = classify prompt mode
- `focus_snippets.py` = focus-snippet selection and focus message
- `deterministic_answers.py` = deterministic direct answers
- `grounding_checks.py` = grounding validation logic

Important:
- future AI must not move orchestration shell methods entirely out of `ai_bridge.py`
- `LocalAIReasoner` is the public behavior owner

---

### `prompt_builder.py`
Role:
- public prompt assembly shell
- builds the evidence pack and answering instructions for the local model

Expected public surface:
- `PromptBuilder`
- compatibility helpers retained:
  - `_norm`
  - `_tokenize_query`
  - `_build_answer_style_instructions`
  - `is_which_method_calls_question`

Current structure:
- public shell in `prompt_builder.py`
- implementation detail split into `prompt_builder_help/`

Helper ownership:
- `prompt_classification.py` = prompt-type detection helpers
- `answer_style.py` = answer-style rules and formatting guidance
- `callsite_evidence.py` = call-site prioritization logic
- `prompt_sections.py` = repeated prompt section formatting
- `widget_registry_section.py` = widget registry prompt block rendering

Important:
- compatibility helpers were intentionally preserved because tests or older code may still import them
- future AI should preserve those names unless all imports and tests are updated deliberately

---

### `index_loader.py`
Role:
- public JSON loader and normalized in-memory index owner
- central source of `JsonProjectIndex`

Expected public surface:
- `JsonProjectIndex`

Current structure:
- public shell in `index_loader.py`
- implementation details in `index_loader_help/`

Helper ownership:
- `state_init.py` = instance field initialization
- `section_loading.py` = top-level JSON section loading
- `path_resolution.py` = runtime source-file normalization
- `index_builders.py` = repeated `_build_*` index construction routines

Important:
- `_build_*` methods remain visible through wrapper methods on `JsonProjectIndex`
- future AI should not bypass `JsonProjectIndex` and call helper modules directly from the rest of the app

---

### `project_profile.py`
Role:
- public project-profile API
- defines passive project profile types, built-in profiles, registry access, and profile inference

Expected public surface:
- `ProjectProfile`
- `GENERIC_PROJECT_PROFILE`
- `GENERIC_PYTHON_PROJECT_PROFILE`
- `ARCHITECTURE_HEAVY_PYTHON_PROJECT_PROFILE`
- `QT_PYTHON_PROJECT_PROFILE`
- `EEG_PROJECT_PROFILE`
- `PROJECT_PROFILES`
- `get_project_profile`
- `iter_project_profiles`
- `infer_project_profile_name_from_metadata`
- `infer_project_profile`

Current structure:
- public facade in `project_profile.py`
- implementation split into `project_profile_help/`

Helper ownership:
- `profile_types.py` = `ProjectProfile`
- `built_in_profiles.py` = profile constants
- `registry.py` = registry and lookup
- `inference.py` = profile inference logic

Important:
- this file is intentionally passive and side-effect free
- future AI should keep profile inference lightweight and metadata-driven

---

### `reasoner_retriever.py`
Role:
- public retrieval shell
- canonical owner of `ProjectRetriever`

Expected public surface:
- `ProjectRetriever`
- a curated set of retrieval helpers re-exported from the shell, especially query-intent helpers and query-text helpers already listed in `__all__`

Current structure:
- public shell in `reasoner_retriever.py`
- implementation already split into `reasoner_retriever_help/`

Important:
- this file was intentionally not decomposed further in the last pass
- current architecture is already shell + helpers
- the correct next action for this file is only cleanup or bugfixes, not another structural explosion of helper files

---

## 14. Helper-package ownership map

Future AI should know which package owns what, so it does not place new code in the wrong place.

### `main_window_help/`
Owns:
- UI wiring
- settings/state helpers
- session service
- runtime/static-context controllers
- answer presentation
- UI builder pieces

Public owner remains:
- `ai_reasoner_main_window.py`

### `reasoner_retriever_help/`
Owns:
- file retrieval
- symbol retrieval
- snippet retrieval
- snippet expansion
- query intent parsing
- query text normalization
- profile support
- section retrieval
- bundle merge
- advanced file-context scoring

Public owner remains:
- `reasoner_retriever.py`

### `ai_bridge_help/`
Owns:
- prompt parsing
- prompt mode classification
- deterministic answer extraction
- focus snippet logic
- grounding enforcement

Public owner remains:
- `ai_bridge.py`

### `prompt_builder_help/`
Owns:
- prompt classification
- answer-style rules
- call-site evidence prioritization
- prompt section formatting
- widget registry rendering

Public owner remains:
- `prompt_builder.py`

### `index_loader_help/`
Owns:
- loader state initialization
- full-section assignment
- runtime path normalization
- index-building routines

Public owner remains:
- `index_loader.py`

### `project_profile_help/`
Owns:
- profile dataclass
- built-in profiles
- registry and lookup
- inference

Public owner remains:
- `project_profile.py`

### `help_index_help/`
Owns:
- raw help payload
- normalization
- fully prepared help data

Public owner remains:
- `help_index.py`

---

## 15. Validation history and what counts as done

A future AI should not repeat unnecessary work that has already been validated.

A rename/refactor was considered done only after most or all of these were checked:

1. renamed file exists at canonical path
2. import rewrites completed
3. leftover legacy references searched for
4. direct import works
5. root-package import works if the symbol is curated in `__init__.py`
6. compile check passes
7. full compile sweep is acceptable
8. validator stays green where relevant

That exact workflow was applied repeatedly during this work and is the reason the current state is trustworthy.

---

## 16. Regression checks already used during this work

These question types were repeatedly used as smoke tests for retriever/routing/prompt behavior. Future AI should reuse them after any retrieval or prompt changes.

### Exact locator checks
Examples:
- Where is `on_close_clicked` defined?
- Which method calls `on_close_clicked`?
- Which file defines the main window class?
- Which symbol owns `build_and_show`?

These are mainly deterministic retrieval tests.

### Signal/slot checks
Examples:
- Show the close-button signal connections.
- What signal connects the apply button?
- What signal connects the close button?

These test routing, signal evidence boosts, and prompt evidence selection.

### Flow / chain checks
Examples:
- Explain the startup chain.
- Explain how the topomap is rendered.
- Describe the reset flow.
- Trace the topomap chain with code.

These test chain classification, retrieval coverage, snippets, and prompt builder behavior.

### Packaging / documentation checks
Examples:
- Where is the package metadata defined?
- Where is the documentation for the retriever behavior?

These test section-priority logic and canonical section-only bundle behavior in retriever flow.

---

## 17. Root package guidance

The package root `project_reasoner_v10/__init__.py` is now intentionally curated.

That means future AI should follow these rules:

### Keep the root API curated
Only export stable, high-value entry points and shared contracts.

### Do not make `__init__.py` huge
No real business logic belongs there.

### Keep root exports aligned with canonical module names
All current root exports should point to the canonical renamed modules:
- `.index_loader`
- `.project_profile`
- `.prompt_builder`
- `.ai_bridge`
- `.reasoner_retriever`
- `.query_router`
- `.help_index`
- `.ai_reasoner_main_window`

### Preserve editor/IDE friendliness
The current pattern was updated to be more IDE-friendly than a pure lazy-export approach.

---

## 18. Why certain files were intentionally not deeply refactored

Future AI should understand the reasoning, not just the outcome.

### `reasoner_retriever.py`
Not deeply re-refactored because:
- it is already a public shell
- most heavy logic already lives in `reasoner_retriever_help/`
- creating more helper layers would have reduced clarity, not improved it

### `help_index.py`
Was refactored because:
- it was essentially a huge data blob
- moving raw data out improved clarity and maintainability without semantic risk

### `project_profile.py`
Was refactored because:
- it had very clean separable responsibilities
- splitting dataclass / profiles / registry / inference is natural and stable

### `index_loader.py`
Was refactored because:
- repetitive section loading and index-builder code dominated the file
- helper extraction gave real structural payoff

---

## 19. Known repo-level conventions established during this work

These conventions are now part of the project style.

### Thin public shell pattern
Canonical public modules keep the public API, while helper packages own detail.

### Rename-first strategy
When a file still had a `v10_` prefix but was clearly meant to be current live code, it was renamed first and then validated before refactoring.

### Helper folders are explicit and named after the owner
Examples:
- `ai_bridge_help`
- `prompt_builder_help`
- `index_loader_help`

### Compatibility helpers stay when tests might depend on them
This was done in `prompt_builder.py` and should be repeated when useful.

### Root package should expose a curated public API
The package root is no longer just an empty marker.

---

## 20. Suggested future safe next targets

If future AI continues, the safest next work categories are:

### Good next tasks
- clean the `SyntaxWarning` in `ai_reasoner_main_window.py`
- clean mojibake or duplicated decorative docstrings
- run broader test suite updates for renamed modules
- keep shrinking other oversized modules using the same shell + helper pattern

### Lower-priority tasks
- cosmetic cleanup in already-stable shells
- help text wording normalization
- docstring consistency cleanup

### Avoid unless necessary
- another deep structural rewrite of `reasoner_retriever.py`
- undoing the curated root package API
- recreating `v10_*` aliases unless required for an external compatibility layer

---

## 21. If future AI needs to verify current state quickly

Use this minimal checklist:

1. compile the public shell module
2. compile all helper modules in its paired helper folder
3. verify direct import
4. verify root-package import if curated
5. search for leftover legacy `v10_` references
6. run manifest validator if that module participates in manifest-governed structure

That is the shortest high-confidence safety loop for this repo.

---

## 22. Final condensed handoff block for future AI

Use this block verbatim in future sessions if needed:

> This repository has already completed a staged rename-and-refactor program. Canonical live modules are now `query_router.py`, `help_index.py`, `ai_bridge.py`, `prompt_builder.py`, `index_loader.py`, `project_profile.py`, and `reasoner_retriever.py`. Several of these are intentionally thin public shells over helper packages: `ai_bridge_help`, `help_index_help`, `prompt_builder_help`, `index_loader_help`, `project_profile_help`, `reasoner_retriever_help`, and `main_window_help`. The curated root package API in `project_reasoner_v10/__init__.py` is intentional and should remain aligned with the canonical module names. `reasoner_retriever.py` is already in shell form and should not be structurally decomposed further without a strong reason. Manifest validation is already green for `ai_bridge_help.json`, `ai_reasoner_main_window_help.json`, and `reasoner_retriever_help.json`. A pre-existing non-blocking `SyntaxWarning` remains in `ai_reasoner_main_window.py` due to Windows paths inside a decorative docstring. Future changes should extend helper packages rather than expanding shell modules or reintroducing legacy `v10_*` imports.
