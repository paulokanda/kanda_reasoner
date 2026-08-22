# KANDA REASONER PRO — LEAN IMPLEMENTATION HANDOFF / CONTINUATION ROADMAP

Generated for continuation across future AI sessions.

Local project root used in current work:

`E:\kanda_reasoner`

Current working date context: 2026-08-21 America/Sao_Paulo.  
Note: some freeze entries are dated 2026-08-22 because freeze provenance may cross UTC/date boundaries. Treat the freeze entry itself as authoritative.

---

# 1. PURPOSE OF THIS HANDOFF

This file is the authoritative continuation guide for the current KANDA Reasoner professionalization program.

The goal is:

> Make KANDA Reasoner genuinely professional without allowing scope creep, feature creep, software/code bloat, unnecessary architecture, or new technical debt.

The next AI must NOT interpret "KANDA Reasoner PRO" as permission to add features, frameworks, abstractions, subsystems, agents, storage layers, concurrency systems, or modernization work merely because they are fashionable or theoretically useful.

KANDA PRO is a hardening, verification, release-quality, recovery, portability, maintainability, and trust program.

It is NOT a product-expansion program.

---

# 2. NON-NEGOTIABLE ANTI-CREEP LAW

Every proposed PRO change must answer all five questions before source is modified:

1. DEFECT / GAIN
   - What concrete existing problem is being fixed?
   - Or what measurable reliability, correctness, release, recovery, performance, maintainability, security, or UX gain is being obtained?

2. EVIDENCE
   - What current source, runtime validation, benchmark, failure reproduction, or release evidence proves the need exists now?

3. OWNER
   - Which existing KANDA box/module/domain owns the behavior?
   - Do not invent a new owner when an existing owner is correct.

4. SMALLEST CHANGE
   - Can the gain be achieved without a new subsystem, framework, service, abstraction layer, database, agent, or architectural expansion?

5. REGRESSION PROOF
   - What exact focused validation and broader regression gate proves the gain was achieved without damaging frozen contracts?

If any one of these cannot be answered clearly:

> DO NOT IMPLEMENT THE CHANGE.

Additional anti-bloat rule:

> A new abstraction/framework is rejected unless current KANDA code demonstrates genuinely repeated semantics and the abstraction produces a measurable net simplification rather than another layer.

No implementation merely because:
- it is newer;
- another framework supports it;
- other applications use it;
- it improves a cosmetic quality score;
- it reduces lint counts without fixing a meaningful defect;
- it makes KANDA "look more professional";
- it anticipates hypothetical future needs.

---

# 3. KANDA PRODUCT ROLE — DO NOT REDESIGN

KANDA Reasoner remains:

`Observe -> Understand -> Preserve Context -> Validate -> Present to Human/AI -> Maintain Continuity`

It is NOT:
- an IDE;
- an autonomous coding agent;
- an autonomous Project source editor;
- a replacement for PyCharm/VS Code/Visual Studio;
- a hidden mutation engine for external selected Projects.

The human remains authoritative.

Do not weaken these frozen boundaries:
- KANDA Reasoner = Tool.
- Selected Project = observed target.
- Selection grants no external Project source-write authority.
- Tool and Project remain logically separate even when physically co-located.
- External Project development remains independent from KANDA.
- Spectator operations remain spectator operations.
- Proposal-only behavior remains proposal-only.
- Tool/Project interpreter and import isolation remain protected.
- lifecycle token = `selection_ticket`.
- Error Memory = Tool-owned.
- Freeze Memory = Project-owned.
- Error Memory = draft-first.
- Human activation is required for Memorize Error.
- Freeze Preview = read-only.
- Confirm and Write = explicit human action.
- No KSI-S8.
- No new AI architecture without a demonstrated defect requiring it.

---

# 4. HARD PROJECT GOVERNANCE RULES

## 4.1 `.project_reference`

`.project_reference` may physically exist inside the project root, but it is NOT canonical Project code.

Treat all `.project_reference/**` as:
- notes;
- memos;
- examples;
- reference-only material.

It is invisible for:
- Ruff;
- architecture/code-quality scans;
- source hygiene;
- automated repair queues;
- refactors;
- formatters;
- validators;
- symbol/source analysis;
- patch generation.

A finding originating only from `.project_reference` is ZERO Project defects.

Automated KANDA tooling must NEVER modify it unless the user explicitly asks to work on reference material itself.

If a project-wide scanner reports `.project_reference`, correct the scan scope rather than "repairing" the reference files.

## 4.2 `snippets`

`snippets` is also excluded from canonical Ruff source analysis.

Do not treat findings there as canonical Project defects during this PRO work.

## 4.3 Daily-work garbage

`<project>_delete_after_daily_work` is transient garbage.

For this project:

`E:\kanda_reasoner_delete_after_daily_work`

Use it for:
- extracted patch installers;
- transient helpers;
- temporary validators;
- temporary capture scripts.

Do not treat it as durable project state.

## 4.4 Freeze Memory

Project-specific freeze memory belongs under:

`E:\kanda_reasoner_show_project_to_AI\project_freeze_after_update\frozen_features_memory`

Never put project-specific memory in `project_freeze_ledger`.

Frozen entries:
- are read-only;
- must not be edited directly;
- are governed by frontmatter `status`, `superseded_by`, and newer corrective entries;
- contain historical `planned next step` prose once `status: frozen`.

Do not reopen/refreeze a frozen feature unless a genuine new defect requires a new superseding change.

---

# 5. PATCH / VALIDATION GOVERNANCE

Before producing a patch ZIP or terminal install/validation command:

1. State release owner classification.
   Current KANDA source changes are normally:

   `KANDA_TOOL_RELEASE`

2. Inspect exact current source before editing.

3. Respect current predecessor SHA-256.
   Installers should fail closed if the live source no longer matches the inspected predecessor.

4. Patch ZIP must pass the exact official validator:

   `scripts/validate_patch_zip.py`

   Required marker:

   `ZIP CONTRACT: PASS`

5. Root-level `KANDA_FREEZE_HINT.json` is mandatory when required by the current ZIP contract.
   A previous patch failed because it was missing.
   That failure was correctly blocked before installation.

6. Final ZIP must be validated as the exact final delivered artifact.
   Do not validate an intermediate archive and then mutate/rebuild it afterward.

7. Install success is NOT validation success.

8. Do not auto-freeze because validation passed.
   Freeze only after real local validation + broader evidence + explicit human confirmation.

9. Install-success terminal behavior:
   - about 2 seconds;
   - `Clear-Host`;
   - no extra Enter prompt after success.

10. Diagnostic/validation/freeze/error terminal behavior:
    - Enter;
    - Enter;
    - Clear-Host.

11. External transient patch placement:
    - start at active Project drive root;
    - verify SHA-256;
    - copy/stage to daily-work;
    - verify staged SHA-256;
    - remove drive-root source after successful staging;
    - no Downloads/Desktop fallback.

12. Do not use Ruff `--fix` globally.
    Repairs must be scoped and justified.

13. E501 is last and is NOT a current priority.

14. Architecture warning cleanup is separate from Ruff repair trains unless the exact same source edit genuinely fixes both.

---

# 6. LEAN KANDA PRO ROADMAP — GOVERNING IMPLEMENTATION PLAN

This is the anti-bloat interpretation of the broader professionalization roadmap.

The broad roadmap remains useful as research/reference, but the implementation program below is the governing filter.

---

## LEAN PRO-0 — CURRENT CORRECTNESS AND RELEASE TRUTH

Goal:

Know what is actually broken now and close high-confidence correctness defects without launching a lint-cleanup crusade.

Required work:
- current Architecture baseline;
- current Workflow/static gates;
- canonical-scope Ruff correctness baseline;
- finish current F821 family;
- inspect current F811 family;
- verify current Portable validators;
- run plain canonical Portable build when environment is ready;
- confirm validation/build does not mutate governed source;
- confirm exact-member firewall remains strict;
- characterize current staged publication/failure behavior;
- produce one current PRO-0 baseline report.

Important boundary:

PRO-0 does NOT require:
- F401 = 0;
- F841 = 0;
- E402 = 0;
- E501 = 0;
- warning count = 0.

After F821 and F811:
- reassess;
- repair F401/F841/E402 only when a finding has a concrete correctness, import, startup, architecture, ownership, maintainability, or release consequence.

Do not continue merely to improve lint numbers.

PRO-0 acceptance:
- one trustworthy current baseline;
- historical counts replaced by measured current truth;
- no hidden hard failures;
- no suppression merely to improve metrics;
- meaningful correctness families closed or explicitly characterized;
- Portable current implementation verified rather than reimplemented.

---

## LEAN PRO-1 — RELEASE IDENTITY AND ENVIRONMENT RECONSTRUCTION

This combines the useful parts of the former PRO-1 and PRO-2.

Status: REQUIRED.

Concrete gain:
A KANDA release can explain exactly what environment built it and what product/build identity it represents.

Keep this small.

Required:
- exact runtime dependency identity;
- exact build dependency identity;
- exact test/release-gate dependency identity where relevant;
- explicitly govern `pyinstaller-hooks-contrib` alongside PyInstaller;
- record Python identity;
- record PyInstaller identity;
- record hooks identity;
- record PySide6 + Qt identity;
- record Ruff/pytest identity used for release gates;
- capture stable `pip inspect` JSON release evidence;
- one canonical KANDA version owner;
- release/Portable manifest reads that canonical identity;
- include ZIP SHA-256;
- include source/build identity when available/canonical.

Do NOT add:
- Poetry merely for PRO;
- Conda merely for PRO;
- uv merely for PRO;
- a dependency database;
- a package-management service;
- a new environment architecture.

`pylock.toml` may be evaluated, but it is not required as a production single point of failure while installation support remains experimental.

PRO-1 acceptance:
- clean machine reconstruction is possible using governed artifacts;
- one product version owner;
- one release identity;
- dependency/environment evidence is inspectable;
- no duplicated manual version editing across unrelated modules.

---

## LEAN PRO-2 — BUILD REPRODUCIBILITY EXPERIMENT

This is the useful core of former PRO-3.

Status: REQUIRED, EXPERIMENT FIRST.

Concrete gain:
Identify unexplained build variance and remove only variance that matters.

Required:
- clean build A;
- clean build B in a separate root;
- compare:
  - member inventories;
  - manifests;
  - executable metadata;
  - relevant hashes;
  - ZIP metadata;
  - runtime acceptance;
- classify every meaningful difference.

Evaluate:
- `PYTHONHASHSEED`;
- `SOURCE_DATE_EPOCH`;
- deterministic member ordering/timestamps only if needed.

Do NOT:
- build a reproducibility framework before measuring;
- define success solely as identical ZIP SHA if harmless timestamp/metadata variance is intentionally present;
- weaken validation to gain determinism.

PRO-2 acceptance:
Every material A/B difference is removed or explicitly explained.

If current builds are already deterministic enough for KANDA's release contract:
- stop;
- record evidence;
- do not add machinery.

---

## LEAN PRO-3 — TARGETED RELIABILITY VERIFICATION

This folds together only the useful portions of old PRO-6, PRO-7, PRO-8, and PRO-10.

Status: REQUIRED AS AUDIT; PATCH ONLY FAILED CONTRACTS.

### A. High-risk subprocess semantics

Audit only call sites that can:
- hang KANDA;
- block a release;
- leave process descendants;
- consume unbounded output;
- lose useful stderr/stdout evidence;
- misuse shell execution.

Do not invent a global ProcessManager unless genuinely repeated identical contracts prove it would simplify the code.

### B. Critical persistence/recovery

Audit only critical durable owners:
- Error Memory;
- Freeze Memory;
- registries;
- Machine Card or equivalent critical identity state;
- release publication;
- other state where corruption/loss is materially harmful.

Test:
- interrupted write;
- invalid serialized content;
- permission denied;
- read-only destination;
- replace failure;
- stale temp;
- corrupt previous state;
- stale/concurrent write where applicable.

Do not merge domain state into a generic database or storage subsystem.

### C. Qt responsiveness and lifecycle

Verify:
- long user actions do not block GUI materially;
- Project switch rejects stale results;
- window close during work is safe;
- worker timeout is safe;
- worker exception gives useful evidence;
- repeated starts do not create orphan workers.

Do NOT migrate QThread to QThreadPool just because QThreadPool exists.

### D. Portability / negative paths

High-value because KANDA claims drive/path/project agnosticism.

Test:
- Tool and Project roots separated;
- non-E drive;
- paths with spaces;
- read-only directories;
- missing files;
- malformed JSON;
- corrupt ZIP/manifest;
- permission denied;
- stale worker result;
- partial write;
- Project switch during work;
- extracted actual Portable ZIP.

PRO-3 acceptance:
- audit results documented;
- only failed high-value contracts patched;
- no new global architecture without evidence.

---

## LEAN PRO-4 — CONTROLLED RUNTIME COMPATIBILITY

Status: CONDITIONAL / AFTER CORE HARDENING.

Python 3.12 remains current governed production authority until a candidate lane proves a newer line is better.

Test Python 3.14 in an isolated candidate environment.

Run:
- dependency installation;
- compile/static gates;
- focused tests;
- GUI smoke;
- full Portable build;
- extracted-ZIP acceptance;
- relocation/path-space acceptance;
- startup/performance comparison where useful.

PyInstaller upgrade belongs here only when:
- newer Python requires it;
- a relevant defect is fixed;
- support/security requires it;
- or measured packaging benefit justifies it.

No "upgrade because newer."

Acceptance:
Either:
A. newer runtime promoted with full evidence; or
B. 3.12 retained temporarily with a documented blocker and re-test trigger.

---

## LEAN PRO-5 — RELEASE SECURITY / PUBLIC DISTRIBUTION MATURITY

Status: CONDITIONAL.

Always reasonable:
- `pip-audit` as one dependency vulnerability signal.

Only when useful:
- dependency inventory / SBOM.

Only when real public automated release exists:
- artifact provenance/attestation.

Only when public Windows distribution maturity justifies it:
- code signing;
- timestamping;
- signature verification.

Do not sign, attest, or build release-security infrastructure merely to make a private/local development build look professional.

---

# 7. ITEMS EXPLICITLY NOT TO BECOME PRO PROJECTS

Do NOT create these unless a new concrete defect later proves one necessary:

- new AI agents;
- KSI-S8;
- another memory subsystem;
- autonomous Project editing;
- a database migration "for professionalism";
- a generic global process framework;
- a generic global storage framework;
- QThreadPool migration campaign;
- async framework rewrite;
- GUI framework rewrite;
- repository-wide `src/` migration;
- one-file packaging for appearance;
- Nuitka/cx_Freeze/pyside6-deploy migration for novelty;
- free-threaded Python adoption without evidence;
- global formatter migration;
- global typing campaign;
- global logging rewrite;
- global cache layer;
- mass module split;
- mass architecture warning cleanup;
- mass Ruff autofix;
- lint-zero campaign;
- E501 cleanup before correctness/release work;
- refactors of frozen/historical material for aesthetics.

---

# 8. PERFORMANCE POLICY

Performance is not a standalone architecture project.

Rule:

> Profile before optimizing.

Use existing Python tooling such as:
- `cProfile`;
- `tracemalloc`;

only when a meaningful slow or memory-heavy path is demonstrated.

No:
- telemetry framework;
- performance database;
- caching subsystem;
- concurrency layer;

unless a measured bottleneck proves the need.

A performance change must have:
- representative workload;
- baseline measurement;
- identified bottleneck;
- measurable target;
- post-change measurement;
- correctness regression proof.

Never trade validation, ownership, determinism, or recovery for benchmark numbers.

---

# 9. OFFICIAL DOWNLOAD POLICY

Do not count every bounded PRO-0 repair ZIP as an "official KANDA Reasoner PRO download."

Current F821 patch ZIPs are development repair artifacts.

Official downloads should correspond to cumulative professional milestones / governed deliverables.

Working planning estimate from the current state:

- approximately 8–14 official downloads remaining;
- center estimate: about 10.

This is a planning estimate, not a frozen official count.

The count can shrink if multiple lean phases are safely consolidated.

Do not inflate the count by creating artificial packaging milestones.

---

# 10. CURRENT PRO-0 VALIDATED BASELINE

Latest authoritative canonical Ruff state after the frozen Window Process repair:

- canonical Python files: 2645
- functional findings total: 760
- invalid-syntax: 0
- F821: 31
- F811: 5
- F401: 231
- F841: 31
- E402: 462

Canonical exclusions:
- `.project_reference`: EXCLUDED
- `snippets`: EXCLUDED
- Ruff findings from excluded paths: 0

Architecture:
- hard errors: 0 in the focused validation trains.

Workflow:
- previously established PASS:
  - pass=7
  - fail=0
  - warn=0
  - skip=3
  - Architecture inside Workflow: Errors 0, Warnings 63

Do not treat Architecture warnings as an automatic repair queue.

---

# 11. COMPLETED / FROZEN PRO-0 REPAIR TRAINS

Do not reopen these merely because their frozen entry contains historical "planned next step" prose.

## 11.1 Architecture public facade ownership

Frozen:
`freeze-20260821-pro-0-freeze-hint-intake-public-facade-ownership-v1`

Result:
- Architecture hard errors = 0.

## 11.2 Workflow direct-script package bootstrap

Frozen:
`freeze-20260821-pro-0-workflow-direct-script-package-bootstrap-v1`

Result:
- Workflow PASS.
- Do not reopen/refreeze.

## 11.3 Window Methods runtime-bound F821

Frozen:
`freeze-20260821-pro-0-window-methods-runtime-bound-f821-v1`

Target:
`kanda_reasoner_app/reasoner_tools_shell/runner_help/window_methods_private_impl.py`

Result:
- 56 F821 removed from canonical count through rigorously proven runtime-binding treatment.
- narrow file-scoped F821 treatment;
- runtime bind chain preserved;
- no duplicate imports.

## 11.4 Snippet Retrieval explicit dependencies F821

Frozen:
`freeze-20260821-pro-0-snippet-retrieval-explicit-dependencies-f821-v1`

Result:
- F821 90 -> 59
- explicit helper-owned dependencies;
- no suppression.

## 11.5 Source Tree Exporter Planning Any F821

Completed/frozen before later trains.

Target:
`kanda_reasoner_app/reasoner_context_bundle/source_tree_exporter_planning.py`

Result:
- all 12 F821 were missing `typing.Any`;
- explicit import;
- F821 59 -> 47.

## 11.6 Comparison Engine Support Any F821

Frozen:
`freeze-20260821-pro-0-comparison-engine-support-any-f821-v1`

Target:
`kanda_reasoner_app/routing_signal_scorer/adviser_offline/harness/_comparison_engine_support.py`

Result:
- all 6 F821 were `Any`;
- explicit `typing.Any`;
- F821 47 -> 41.

## 11.7 Responsibility Overlap explicit constant bindings

Frozen:
`freeze-20260822-pro-0-responsibility-overlap-explicit-constant-bindings-f821-v1`

Target:
`kanda_reasoner_app/reasoner_context_collector/collector_responsibility_overlap_help/extraction.py`

Diagnosis:
- five F821 findings from `GENERIC_TOKENS` / `GENERIC_CALL_ROOTS`;
- values were locally created through `globals().update(...)`;
- not missing runtime dependencies.

Repair:
- converted PASS_068A constant binding block to explicit module-level assignments;
- preserved exact values;
- no suppression.

Final delivery:
`kanda_pro0_responsibility_overlap_explicit_constant_bindings_f821_v1r1_patch.zip`

SHA-256:
`749584615c6a28f9d20eb5970ca954fec5d47089acecccec7ee700e866c78626`

Result:
- F821 41 -> 36.

Important packaging lesson:
- original v1 ZIP failed `ZIP CONTRACT` because root `KANDA_FREEZE_HINT.json` was missing;
- install was blocked before source mutation;
- v1r1 was metadata-corrected and exact-final ZIP validated.

## 11.8 Window Process runtime-bound F821

Frozen:
`freeze-20260822-pro-0-window-process-runtime-bound-f821-v1`

Target:
`kanda_reasoner_app/reasoner_tools_shell/runner_help/window_process_private_impl.py`

Undefined names:
- `_safe_log_runtime_error`
- `QMessageBox`

Live runtime binding audit proved:
- target `_bind_globals` contract PASS;
- runner ZP payload activation PASS;
- payload wrappers PASS;
- bind-before-delegate PASS;
- runtime-bound name coverage 2/2;
- missing before bind: NONE;
- target pre-repair F821 = 5.

Repair:
- narrow file-scoped `# ruff: noqa: F821`;
- no duplicate imports;
- runtime architecture preserved.

Patch:
`kanda_pro0_window_process_runtime_bound_f821_v1_patch.zip`

SHA-256:
`60632aed13fe8a458c1497439217f24b495f3a32e318b8f73f1831d5326da09b`

Result:
- F821 36 -> 31;
- functional findings 765 -> 760;
- Architecture errors 0;
- frozen.

---

# 12. CURRENT F821 OWNER LIST

Latest current top F821 owners after Window Process freeze:

4 |
`kanda_reasoner_app/insert_missing_docstrings_gui/ai_docstring_generator_help/response_parsing.py`

4 |
`kanda_reasoner_app/manage_workflows/_workflow_command_isolation.py`

3 |
`kanda_reasoner_app/insert_missing_docstrings_gui/ai_docstring_generator_help/docstring_payloads.py`

3 |
`kanda_reasoner_app/reasoner_symbol_atlas/existing_code_finder_matching_private.py`

2 |
`kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_help/file_processing.py`

2 |
`kanda_reasoner_app/manage_architecture/large_file_refactor_planner/_preview_delivery_models.py`

1 each:
- `kanda_prompt_workspace/prompt_tools/audit_startup_candidates_report.py`
- `kanda_reasoner_app/engineering_diagnostics/store.py`
- `kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_gui_help/window_state.py`
- `kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_help/insertion_collector.py`
- `kanda_reasoner_app/project_structure_visualizer/project_structure_3d_tab.py`
- `kanda_reasoner_app/reasoner_context_collector/collector_responsibility_overlap_help/scoring.py`
- `kanda_reasoner_app/reasoner_engine/ai_reasoner_main_window.py`
- `kanda_reasoner_app/reasoner_runtime_collector/runtime_runner_help/runtime_runner_part_1_private_impl.py`
- `kanda_reasoner_app/reasoner_symbol_atlas/complete_json_adapter_helpers_private.py`
- `kanda_reasoner_app/reasoner_symbol_atlas/import_analyzer_ast_private.py`
- `kanda_reasoner_app/reasoner_tools_gui_shell/main_window_help/window_help.py`
- `kanda_reasoner_app/routing_signal_scorer/scoring.py`
- `reasoner_tools_gui_engineering_safety_panel.py`

F811:
5 |
`kanda_reasoner_app/reasoner_context_collector/collector_scope.py`

---

# 13. EXACT CURRENT CHECKPOINT — RESUME HERE

Current active target:

`kanda_reasoner_app/insert_missing_docstrings_gui/ai_docstring_generator_help/response_parsing.py`

Current canonical findings in this file:
- F821 count: 4
- unique undefined names: 3

Names:
- `Any`
- `DocstringPolicy`
- `SymbolContext`

Read-only exact-source capture already completed:

`PRO-0 RESPONSE PARSING CAPTURE: PASS`

Evidence path:

`E:\kanda_reasoner_show_project_to_AI\validation_evidence\pro0_current_baseline_20260821\pro0_response_parsing_f821_exact_source_contract.txt`

No source modification has yet been authorized/performed for this target in the current train.

The immediate next action is NOT to patch blindly.

The next AI must verify:
- whether `Any` is absent from the target import block;
- canonical owner of `SymbolContext`;
- canonical owner of `DocstringPolicy`;
- whether either project type is intentionally runtime-bound;
- whether importing those owners creates an import cycle;
- exact current target SHA-256;
- target physical line count;
- no current F821 suppression;
- no dynamic binding contract requiring the runtime-bound treatment used in Window Methods/Window Process.

A dependency probe was already prepared conceptually with the expected likely owners:

`SymbolContext` likely from:
`kanda_reasoner_app/insert_missing_docstrings_gui/context_builder.py`

`DocstringPolicy` likely from:
`kanda_reasoner_app/insert_missing_docstrings_gui/docstring_policy.py`

DO NOT assume these owners without live current-source proof.

Likely repair if live proof confirms:
- explicit `typing.Any`;
- explicit canonical `SymbolContext`;
- explicit canonical `DocstringPolicy`;
- no F821 suppression.

Expected canonical transition if exactly four findings disappear and nothing else changes:

`F821 31 -> 27`

This expected count must be MEASURED after repair, never claimed in advance as fact.

---

# 14. DECISION TREE FOR EACH REMAINING F821 OWNER

For every remaining F821 file:

## Step 1 — canonical count

Use the latest canonical-scope Ruff JSON.

Never use raw unrestricted:

`ruff check .`

as authoritative project state because it includes excluded/noncanonical material.

## Step 2 — exact source capture

Capture:
- target SHA-256;
- physical lines;
- exact F821 locations;
- unique undefined names;
- full target source;
- relevant sibling/owner sources;
- binding markers.

No edit yet.

## Step 3 — classify every undefined name

Choose exactly one class:

### A. Genuine missing explicit dependency

Examples already seen:
- `typing.Any`;
- lightweight helper functions/models with clear canonical owner.

Preferred repair:
- explicit import / explicit dependency ownership.

Do not suppress.

### B. Local dynamic binding that should become static

Example:
- Responsibility Overlap constants created by local `globals().update(...)`.

If values belong to the same module and explicit assignments simplify static ownership without behavioral change:
- convert to explicit assignments.

Do not suppress merely because dynamic binding exists.

### C. Intentional external/runtime namespace binding

Examples:
- Window Methods;
- Window Process.

Before suppression, prove:
- `_bind_globals(namespace)` or equivalent;
- payload/facade activation;
- binding happens before delegate/use;
- every undefined name exists in the supplied namespace;
- behavior depends on this moved-method/runtime architecture;
- duplicate imports would blur or duplicate ownership.

Only then:
- narrow file-level `# ruff: noqa: F821` is acceptable.

### D. Dead/stale code

If evidence shows the referenced code is unreachable/deprecated and not a valid runtime contract:
- do not import/suppress just to satisfy Ruff;
- characterize removal separately;
- do not mix a structural deletion into a small dependency repair without justification.

### E. Ambiguous

If ownership cannot be proven:
- stop;
- capture more source/runtime evidence;
- do not guess.

---

# 15. F821 REPAIR TRAIN PROCEDURE

For each coherent target/family:

1. Read current Freeze context.
2. Search active Error Memory for an existing exact lesson/pattern.
3. Capture exact live source.
4. Classify undefined names.
5. State:
   - gain;
   - evidence;
   - owner;
   - smallest change;
   - regression gate.
6. Build focused patch only.
7. Keep touched source modules <=499 physical lines when governed by that law.
8. ASCII check when current validator contract requires it.
9. Add root `KANDA_FREEZE_HINT.json`.
10. Run exact final ZIP validator.
11. Deliver exact final ZIP SHA-256.
12. Stage/install from active Project drive root using daily-work.
13. Run focused validation.
14. Run canonical exclusion-aware Ruff baseline.
15. Confirm exact count reduction.
16. Prepare Freeze form.
17. Human Confirm and Write.
18. When `status: frozen` returns:
    - close feature;
    - do not reopen;
    - continue next owner.

Do not create a new Error Memory lesson if an existing lesson already exactly covers the failure class.

---

# 16. CANONICAL RUFF CAPTURE POLICY

Authoritative baseline must use KANDA's canonical project exclusion policy.

Known helper used during this session:

`E:\kanda_reasoner_delete_after_daily_work\pro0_ruff_canonical_scope_capture_v1.py`

It uses KANDA's project exclusion logic rather than raw filesystem traversal.

Required invariants:
- `PRO-0 RUFF CANONICAL SCOPE CAPTURE: PASS`
- `CANONICAL PROJECT EXCLUSION POLICY: PASS`
- `PROJECT_REFERENCE EXCLUDED: PASS`
- `SNIPPETS EXCLUDED: PASS`
- `RUFF FINDINGS FROM EXCLUDED PATHS: 0`
- `invalid-syntax: 0`

Do not invent a `_project_reference` requirement.

The actual hard invariant is `.project_reference`.

---

# 17. AFTER F821 REACHES ZERO

Do NOT automatically begin F401/F841/E402 cleanup.

Next:

## A. Characterize F811

Current:
- 5 findings;
- all in `kanda_reasoner_app/reasoner_context_collector/collector_scope.py`.

Use the same exact-source / ownership / smallest-change protocol.

F811 can represent duplicate/redefined names and is a high-confidence correctness/maintainability family worth understanding.

## B. PRO-0 REASSESSMENT CHECKPOINT

After F821 = 0 and F811 is resolved or precisely characterized:

Ask:

1. Are there any remaining hard Architecture failures?
2. Any Workflow hard failures?
3. Any remaining Ruff finding that corresponds to an actual runtime/import/correctness defect?
4. Has current Portable implementation been revalidated?
5. Does plain canonical Portable build pass?
6. Does Portable validation/build preserve governed source?
7. Is exact-member validation intact?
8. Has staged publication/failure behavior been characterized adequately?
9. Is there a trustworthy current baseline report?

If yes:
- close PRO-0.

Do NOT force F401/F841/E402/E501 to zero merely to declare PRO-0 complete.

---

# 18. PORTABLE WORK NEEDED BEFORE PRO-0 CLOSE

Earlier Portable work is largely already implemented.

Do not rebuild:
- bytecode isolation;
- staged publication;
- exact member firewall.

Verify them.

Known current design includes:
- `PYTHONDONTWRITEBYTECODE=1`;
- `PYTHONPYCACHEPREFIX=<run_root>/pycache`;
- controlled candidate ZIP;
- candidate validation;
- extracted acceptance;
- `.partial` promotion flow;
- `os.replace`;
- hash/size checks;
- rollback/failure evidence.

PRO-0 Portable verification should include:
- plain canonical build;
- source hash before/after;
- no governed `__pycache__`/`.pyc` contamination;
- exact members;
- extracted acceptance;
- path with spaces;
- relocation / different drive where practical;
- failed candidate does not replace previous good artifact;
- failed final promotion leaves recoverable state.

Only patch if actual current validation exposes a defect.

---

# 19. WHAT THE NEXT AI MUST NOT DO

Do not:
- start PRO-1 before the current F821 correctness train is sensibly closed unless user explicitly reprioritizes;
- mass-run Ruff fixes;
- repair `.project_reference`;
- repair `snippets`;
- interpret frozen planned-next-step text as pending;
- change frozen files just to conform to a new style;
- add new AI architecture;
- add a new memory system;
- add a DB;
- add QThreadPool as modernization;
- add a global subprocess framework;
- add a global persistence framework;
- switch Python/PyInstaller because newer versions exist;
- create a logging framework before a diagnostic blind spot is demonstrated;
- create a cache before profiling proves repeated work is materially costly;
- chase all architecture warnings;
- chase all F401/F841/E402/E501 counts;
- conflate official PRO milestone downloads with daily repair ZIPs;
- claim validation success from static source inspection;
- claim a predicted Ruff count until it is measured.

---

# 20. COMMUNICATION / DELIVERY STYLE FOR CONTINUATION

The user prefers:
- decisive continuation;
- exact PowerShell blocks;
- minimal unnecessary clarification;
- English interaction;
- clear PASS/FAIL markers;
- exact SHA-256 where relevant;
- freeze form when requested;
- no hand-wavy "probably fixed" claims;
- no unnecessary re-explanation of already-frozen work.

When a task is complex:
- briefly state what is being verified;
- show decisive partial findings early;
- then give exact command/artifact.

Do not promise background work.

---

# 21. RECOMMENDED NEXT SESSION OPENING

When this handoff is supplied in a future session, the AI should say approximately:

> Loaded. I will continue under the Lean KANDA PRO anti-bloat rules. The current authoritative Ruff baseline is F821 31 / F811 5 / F401 231 / F841 31 / E402 462 with `.project_reference` and `snippets` excluded. The current active target is `response_parsing.py` with four F821 findings (`Any`, `DocstringPolicy`, `SymbolContext`). No repair has yet been applied to that target. I will first prove the canonical owners/import-cycle/binding contract, then make the smallest owner-correct change and validate it before proceeding.

Then continue from Section 13.

---

# 22. FINAL DEFINITION OF "KANDA REASONER PRO"

KANDA Reasoner PRO is NOT defined by having more features.

It is defined by being easier to:
- trust;
- understand;
- reproduce;
- validate;
- diagnose;
- recover;
- move between environments;
- release safely;
- maintain without architectural drift.

A professional KANDA must preserve its original role while reducing uncertainty and failure risk.

The governing principle is:

> Harden what exists. Measure what matters. Upgrade only when evidence shows a net gain.

And the anti-creep implementation principle is:

> No demonstrated gain + no current evidence + no owner-correct smallest change + no regression proof = no implementation.

