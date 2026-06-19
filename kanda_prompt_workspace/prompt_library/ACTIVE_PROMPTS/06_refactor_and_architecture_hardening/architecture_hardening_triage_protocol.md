---
audit_id: A044
audit_decision: UPDATE
audit_classification: ACTIVE_ARCHITECTURE_HARDENING_PROTOCOL
audit_batch: prompt_audit_chunk_003
review_status: sandbox_checked
---

> Audit note: This file was reviewed in batch mode. The content below is the real updated file for this audit decision.

# Architecture Hardening Triage Protocol

## Box Logic Requirement

Before any implementation, repair, refactor, prompt update, governance update, or bundle creation, the AI must:

- Identify the active box before implementation.
- State owner paths.
- State files allowed to change.
- State files explicitly out of scope.
- Declare cross-box touches.
- Preserve public contracts.
- Validate the active box and any touched external box.


Version: 1.0
Status: Optional special-purpose hardening protocol
Project: Project Reasoner / developer_tools / kanda_reasoner_app
Use: Upload this prompt only when the task is an architecture-hardening campaign,
not for normal daily implementation.

This prompt is subordinate to:
1. 0000 0.1 PYARCHITECT REASONER PROMPT STACK LOAD ORDER v1.1.md
2. universal_delivery_protocol.md
3. reasoner_startup_canon.md
4. daily_reasoner_startup_loader.md
5. The active Reasoner governance files
6. Current source files, runtime logs, validation output, and user instruction

This prompt does not replace:
- large_module_refactor_protocol.md
- active_governance_freeze_update.md
- current_workflow_handoff_template.md

Purpose
-------

Use this protocol to audit, triage, and safely harden Project Reasoner architecture
when the project has warnings or risks involving:

- public facade noise
- duplicate public symbol ownership
- wildcard imports
- dynamic or unbound __all__
- layer-boundary violations
- box-boundary violations
- static/runtime/reader crossing
- GUI lifecycle risk
- session-state mutation spread
- duplicate normalizers
- responsibility overlap
- shadow paths
- stale generated artifacts
- project-root hardcoding
- direct imports from deprecated or older folders
- prompt/retrieval/AI-bridge ownership drift

This protocol is designed for security-style architectural safety:
import safety, state safety, GUI safety, evidence safety, schema safety, and
refactor safety.

It is not a broad rewrite prompt.

Core rule
---------

Do not start by rewriting runtime source files.

Start by auditing, classifying, and creating focused validation gates.

The workflow is:

audit -> classify -> add or tune checkers if needed -> triage findings ->
separate hard failures from transitional debt -> create precise allowlists only
when justified -> patch the smallest owner box -> validate -> wait for user
validation -> freeze or handoff.

Prompt request rule
-------------------

Before implementation, PyArchitect must orient the user and request the needed
prompt files.

Use this wording:

"For this architecture-hardening task, I need these prompt files before
implementation:
1. 0000 0.1 PYARCHITECT REASONER PROMPT STACK LOAD ORDER v1.1.md
2. universal_delivery_protocol.md
3. reasoner_startup_canon.md
4. daily_reasoner_startup_loader.md
5. Active governance ZIP or the five active governance files
6. Latest 0000 6.0 handoff output
7. architecture_hardening_triage_protocol.md
8. Relevant source ZIP, logs, validation output, or architecture report

If the hardening touches schema, retrieval, prompt building, AI bridge,
runtime collector, GUI lifecycle, or multi-box boundaries, also upload:
- reasoner_professional_engineering_governance.md

If any file above 500 lines must be split or refactored, also upload:
- large_module_refactor_protocol.md"

Delivery rule
-------------

Use the unified KANDA-style direct ZIP delivery.

For source, prompt, checker, documentation, or validation bundles:
- Create or update files in the AI sandbox.
- Validate what can be validated in the sandbox.
- Deliver one ZIP with final project-relative folders.
- Do not require a patch runner just to install files.
- Do not place normal source or prompt bundles under _patch_backups.
- Include a bundle manifest at:
  _bundle_temp\BUNDLE_MANIFEST_<task_slug>.txt

For official governance-only updates:
- Use only 0000 4.11.
- Deliver exactly the five active governance files under:
  _project_reference\ACTIVE_PROJECT_ GOVERNANCE\

No normal implementation or hardening ZIP should require the user to extract a
runner and then execute it to modify files. If the update is risky, include
backup guidance and validation commands, but the ZIP itself must already contain
the final destination paths.

High-level hardening targets
----------------------------

Target 1: Public facade and symbol ownership safety

Detect:
- wildcard imports in __init__.py
- __all__ names not locally bound
- duplicate public exports across package facades
- dynamic __all__
- public facade files that execute runtime work
- generic noise names exported as public API
- broad root facades that re-export unrelated boxes
- support tools becoming second canonical owners

Safe __init__.py types:

1. Package marker
   - module docstring
   - optional __all__ = []

2. Local explicit facade
   - explicit imports only
   - imports from local canonical owner modules only
   - explicit __all__

3. Lazy facade
   - only when needed to avoid circular imports or heavy startup
   - __init__.py imports __getattr__ and __dir__ from a private runtime helper
   - no runtime object construction

Forbidden in __init__.py:
- wildcard imports
- Qt object construction
- filesystem scanning
- model calls
- project analysis
- broad cross-layer re-exports
- duplicate public ownership
- generic noise exports unless explicitly public

Target 2: Layer-boundary safety

Detect:
- static collector importing runtime collector
- runtime collector importing static AST schema parsing
- V10 GUI directly collecting source when collector owns that
- prompt builder directly walking files when index loader/retriever owns evidence access
- AI bridge choosing evidence ranking
- lower layers importing higher GUI/runtime layers
- support tools becoming product owners
- production code importing deprecated, older, backup, or generated copies
- hardcoded analyzed-project path in production source

Reasoner owner map:

- reasoner_context_collector owns static evidence harvesting
- reasoner_runtime_collector owns runtime instrumentation
- project_reasoner_v10 owns GUI, index loading, retrieval, prompt building,
  AI bridge, profile logic, and answer presentation
- manage_architecture owns architecture validation and manifest checks
- manage_workflows owns workflow tooling
- json_splitter owns JSON splitting and reassembly
- daily_rfctr_report owns structural summaries and handoff evidence
- insert_missing_docstrings_gui owns docstring generation workflow

Target 3: Runtime state and GUI lifecycle safety

Detect:
- direct writes to protected state outside the owner box
- scattered writes to GUI runtime state
- stale object cleanup gaps
- Qt timers or signal connections without cleanup
- worker/subprocess lifecycle leaks
- repeated widget reconstruction when state update would suffice
- GUI event loop blocking

Protected state examples:
- PROJECT_ROOT
- OUTPUT_ROOT
- active project selection
- loaded index/evidence state
- runtime trace state
- current profile override
- prompt/retrieval request state
- worker process handles
- Qt timers
- open dialogs/windows
- cached loaded JSON
- generated evidence file paths

Target 4: Duplicate normalizer and responsibility overlap safety

Detect duplicated or competing logic for:
- path normalization
- root detection
- JSON section defaults
- schema version handling
- prompt evidence wording
- retrieval ranking normalization
- project profile detection
- file encoding/BOM handling
- public symbol extraction
- line-count detection
- import graph parsing
- runtime trace event normalization

Rule:
One behavior must have one canonical owner.

If duplicated behavior exists:
- identify the highest-authority current owner
- convert other copies into callers, adapters, or transitional shims
- do not silently create a third copy

Target 5: Generated evidence and JSON safety

Detect:
- manual edits to canonical generated JSON
- stale split manifests
- hash mismatch
- local AI experiment files treated as canonical export
- schema changes without compatibility plan
- generated evidence used as live source truth for implementation

Rules:
- live source files are truth for implementation
- generated JSON is evidence, not source code
- official collector workflow owns canonical JSON export
- local-AI working JSON must not overwrite canonical web-AI JSON
- schema changes require migration statement and index-loader impact review

Workflow
--------

Phase 0 - Baseline audit

Before code, produce:

1. Project root
2. Current active box
3. Current target risk area
4. Files/logs available
5. Files/logs missing
6. Current validation status
7. Known frozen canon that must not regress
8. Expected output of this phase
9. Whether this is LOW, MEDIUM, HIGH, or CRITICAL risk
10. Whether more prompts are required before implementation

Do not patch before the baseline is understood.

Phase 1 - Add or tune checkers first

If hardening gates do not exist or are too noisy, create add-only checker files
first.

Possible checker files:
- tools\architecture\check_public_symbol_ownership.py
- tools\architecture\check_layer_boundaries.py
- tools\architecture\check_duplicate_normalizers.py
- tools\architecture\check_project_root_dynamism.py
- tools\architecture\check_prompt_retrieval_ownership.py
- tools\runtime\check_gui_runtime_lifecycle_contract.py
- tools\architecture\run_reasoner_hardening_checks.py

Checker rules:
- Standard Python 3.10+
- Standard library unless project already uses pytest for tests
- UTF-8 without BOM
- ASCII-safe Python source
- clear exit code: 0 pass, non-zero fail
- human-readable findings
- skip tests, backups, deprecated folders, .venv, __pycache__, build, dist,
  generated split artifacts, and archived copies by default
- include --strict mode when useful
- avoid false positives from local variables unless strict mode is requested

Phase 2 - Triage findings

Classify every finding as one of:

A. Hard failure
   Must be fixed before the gate can pass.

Examples:
- core owner imports GUI owner
- static collector imports runtime collector
- prompt builder directly scans source
- AI bridge ranks evidence
- wildcard import in active public facade
- public symbol exported by multiple active owners
- production hardcoded analyzed-project path
- schema migration without compatibility handling

B. Transitional debt
   Existing issue that is real but cannot be safely fixed in the current pass.

Examples:
- legacy facade still needed by callers
- historical compatibility shim
- temporary adapter with a documented retirement trigger
- broad old API that requires staged migration

C. Warning or observation
   Worth tracking but not blocking this gate.

Examples:
- similarly named private helpers with different real behavior
- broad but inactive historical file
- old docs contradict current source
- generated index is stale but not part of current source change

Phase 3 - Allowlist only transitional debt

Do not weaken checker rules globally.

If transitional debt must remain, create a precise allowlist file, for example:

docs\architecture\reasoner_layer_boundary_allowlist.json

Each entry must include:
- code
- path
- finding
- reason
- owner box
- risk
- removal trigger
- target future gate

Checker behavior:
- allowlisted findings print as warnings
- unallowlisted findings remain hard failures
- new findings must fail
- allowlists must stay short and intentional

Phase 4 - Patch hard failures

Patch order:
1. Public facade/import ownership hard failures
2. Cross-layer import hard failures
3. project-root/path hardcoding
4. schema/index-loader hard failures
5. retrieval/prompt/AI-bridge ownership drift
6. GUI lifecycle and runtime state writes
7. duplicate normalizers
8. responsibility overlaps

Correction strategies:

For public facade problems:
- replace wildcard imports with explicit imports
- remove unbound __all__ entries
- keep package markers simple
- use lazy facade only when needed
- do not make __init__.py a second owner

For cross-layer imports:
- move shared helper to a lower neutral owner
- use dependency injection
- use typed request/result contract
- use local lazy import only for compatibility and document retirement trigger

For project-root hardcoding:
- replace fixed analyzed-project path with PROJECT_ROOT from config, GUI state,
  request object, or typed context
- tests/smokes may keep example paths if clearly marked

For retrieval/prompt drift:
- retrieval ranking belongs in retriever
- final prompt assembly belongs in prompt builder
- AI model transport belongs in AI bridge
- GUI displays and orchestrates but does not rank or invent evidence

For duplicate normalizers:
- choose canonical owner
- update call sites
- leave short compatibility wrapper only if needed
- add retirement note when wrapper remains

Phase 5 - Validate

Every hardening bundle must include commands for Windows/PyCharm terminal.

Minimum validation:
- py_compile every touched Python file
- run focused checker
- run relevant global safety gates if available
- import smoke for affected public imports
- GUI smoke checklist if GUI lifecycle is affected

Recommended commands:

cd <PROJECT_ROOT>

python.exe -m py_compile <touched_file_1.py> <touched_file_2.py>

python.exe tools\architecture\run_reasoner_hardening_checks.py

python.exe -c "import kanda_reasoner_app; print('Reasoner import: OK')"

If GUI changed:
- launch Reasoner GUI through the normal entry point
- load or select a project
- run or load analysis
- open evidence/static-context view
- ask one simple architecture question
- confirm no crash and evidence remains visible

Testing honesty:
- If the complete project and runnable environment were not provided, say:
  "Regular targeted testing was performed on the provided files only. This is
  not exhaustive runtime testing."
- Do not claim full runtime validation unless the complete runnable project was
  provided and actually tested.

Phase 6 - Deliver

For source/checker/documentation bundles:
- deliver one ZIP
- paths must be project-relative from <PROJECT_ROOT>
- include _bundle_temp\BUNDLE_MANIFEST_<task_slug>.txt
- no patch runner required
- no _patch_backups delivery requirement
- include validation commands
- include rollback guidance

For risky direct replacements:
- tell the user to back up or use version control first
- still deliver final destination files directly in the ZIP
- do not require a runner for normal installation

For official canon updates:
- stop and use 0000 4.11 instead
- do not include runtime/source/checker changes in governance-only ZIP

Output format for a hardening audit
-----------------------------------

Use this structure:

ARCHITECTURE HARDENING TRIAGE

Project:
- <project>

Current box:
- <box>

Risk class:
- LOW | MEDIUM | HIGH | CRITICAL

Available evidence:
- <source files/logs/checker output>

Missing evidence:
- <files/logs needed or NONE>

Findings:
1. <finding>
   - class: hard_failure | transitional_debt | warning
   - owner: <box>
   - evidence: <source/log>
   - recommended action: <action>

Prompt files needed before implementation:
1. <prompt>
2. <prompt>

Roadmap:
1. <phase>
2. <phase>

First safe patch:
- <one narrow task>

Validation required:
- <commands/checks>

Do not touch:
- <boxes/paths>

Output format for a hardening delivery
--------------------------------------

Use this structure:

ARCHITECTURE HARDENING DELIVERY

Changed box:
- <box>

Risk class:
- LOW | MEDIUM | HIGH | CRITICAL

Files changed:
- <path>
- <path>

Files not touched:
- <paths/boxes>

What changed:
- <summary>

What did not change:
- <out-of-scope>

Safety boundaries preserved:
- PROJECT_ROOT dynamic
- GUI-first workflow
- static/runtime/reader separation
- retrieval/prompt/AI bridge ownership
- generated evidence safety
- no patch runner requirement

Validation performed:
- <sandbox py_compile/checks or targeted only>

User validation commands:
```powershell
cd <PROJECT_ROOT>
python.exe -m py_compile <touched files>
python.exe <focused checker>
```

Manual validation:
- <GUI/app steps if relevant>

Testing honesty:
- <targeted or exhaustive statement>

Next safe step:
- <one step>

Freeze rule
-----------

Do not freeze architecture-hardening behavior until:
- focused checker passes
- relevant global gates pass or accepted external warnings are clearly labeled
- user validates locally
- any canon update is explicitly approved

If the work is not ready for canon:
- create a 0000 6.0 handoff instead of updating governance

If the work is ready for canon:
- ask for 0000 4.11 and the active governance files
- update only the five governance files

Deprecation note
----------------

This prompt replaces the old ad hoc hardening guidance from historical chats
and old KANDA security-hardening prompts.

Do not use old prompts that require patch runners, _patch_backups, or manifest
at ZIP root for normal Reasoner hardening work.

Final rule
----------

Hardening is not rewriting.

Hardening means:
- identify the owner
- enforce the boundary
- preserve working behavior
- reduce ambiguity
- validate the gate
- document transitional debt
- patch one risk class at a time
