This roadmap is for the first safe patch only: anti-duplication audit + internal engine foundation + Symbol Indexer v1, with no GUI changes yet.

Roadmap: Project Intelligence Foundation v1
1. Confirm implementation scope

Implement only:

project_intelligence internal package.
Base engine contract.
Shared report/data models.
Symbol Indexer / Function Indexer v1.
Validation script for Symbol Indexer.
Patch delivery with install and validation instructions.

Do not implement yet:

Brain Navigator button.
GUI Specs Tool.
Risk Change Radar.
JSON Advice.
Error Memory Correlator.
Health Scan.
ADR Writer.
SAST.
Memory Map.
Any new top-level tab.

Reason: first patch should prove the engine architecture safely before touching UI.

2. Load required safety context before coding

Before any source edit, the implementing AI must confirm:

Startup routing is loaded.
Project handoff is loaded.
Compact Error Memory is loaded.
Full Error Memory is not opened unless compact lessons are insufficient or repeated-error debugging is needed. The uploaded Error Memory preflight explicitly says compact memory is always read and full memory is only opened when needed.
Exact source files are inspected before editing; JSON handoff is helpful but not source truth.

Required pre-coding response:

ERROR MEMORY CHECK

Project slug: kanda_reasoner
Relevant lesson IDs:
Confidence per match:
Applicable avoidance rules:
Full Error Memory ZIP needed: YES / NO
May proceed:
Reason:
Next safe action:

For this first patch, likely relevant lessons:

lesson-delete-after-daily-work-bridge-enforcement-v1
lesson-no-isolated-zip-delivery-contract-v1
lesson-validation-output-status-in-sync-required-v1
3. Run anti-duplication source audit

Before creating files, inspect the current source tree for existing equivalents.

Audit must answer:

PROJECT INTELLIGENCE SOURCE AUDIT

Existing scanner/report utilities:
Existing AST or file-walk utilities:
Existing exclusion-rule API:
Existing validation command logic:
Existing UI report panels:
Existing JSON/report schemas:
Safe integration points:
Potential duplication risks:
Do not touch:
Recommended first patch:

The audit must specifically search for:

Existing AST scanners.
Existing project file walkers.
Existing exclusion-rule loaders.
Existing report/dataclass models.
Existing validation script conventions.
Existing STATUS: IN_SYNC patterns.
Existing source archive / handoff scanners.
Existing Architecture Review scan logic.
Existing Workflow Review scan logic.
Existing Engineering Safety scan logic.

Stop gate:

If existing reusable scanner/report utilities exist, reuse or wrap them.
Do not create duplicate scanner logic unless the audit proves there is no safe reusable interface.
4. Define first patch name and feature ID

Recommended feature ID:

project-intelligence-symbol-indexer-v1

Recommended patch ZIP name:

kanda_project_intelligence_symbol_indexer_v1_patch.zip

Recommended validation marker:

VALIDATION OK: project-intelligence-symbol-indexer-v1
STATUS: IN_SYNC
ZIP CONTRACT: PASS
5. Create isolated package namespace

Add the internal namespace:

kanda_reasoner_app/project_intelligence/

Initial files:

kanda_reasoner_app/project_intelligence/__init__.py
kanda_reasoner_app/project_intelligence/base_engine.py
kanda_reasoner_app/project_intelligence/models.py
kanda_reasoner_app/project_intelligence/symbol_indexer.py

Important: no GUI imports inside this package.

This package must be:

Standard-library only.
ASCII-only.
Windows-compatible.
Read-only against the target project.
Independent from PySide/PyQt.
Safe to test in isolation.
6. Define shared models first

File:

kanda_reasoner_app/project_intelligence/models.py

Required dataclasses:

EngineFinding
EngineReport
SymbolRecord
ImportRecord
FileSymbolSummary

Minimum model fields:

EngineFinding:
- finding_id
- severity
- category
- title
- message
- file_path
- line_number
- evidence
- recommendation

EngineReport:
- engine_id
- engine_version
- status
- generated_at
- project_root_label
- summary
- findings
- warnings
- errors
- next_steps
- ai_must_not_assume

SymbolRecord:
- name
- symbol_type
- file_path
- line_number
- end_line_number
- parent_name
- has_docstring
- is_async

ImportRecord:
- module
- imported_name
- import_type
- file_path
- line_number

FileSymbolSummary:
- file_path
- function_count
- class_count
- method_count
- import_count
- syntax_error

No Pydantic unless already used by the project and audit approves it.

7. Define base engine contract

File:

kanda_reasoner_app/project_intelligence/base_engine.py

Required objects:

EngineExecutionError
BaseIntelligenceEngine

Minimum methods:

run_scan(project_root, context_filter=None, options=None)
to_markdown(report)

Required behavior:

Engine errors must be localized.
A syntax error in one file must not crash the whole scan.
Engine output must include the advisory warning:
This generated report is advisory evidence. It is not canonical source. Exact source files must be inspected before editing.
8. Implement Symbol Indexer v1

File:

kanda_reasoner_app/project_intelligence/symbol_indexer.py

Use only:

ast
dataclasses
datetime
json
pathlib
typing

Symbol Indexer must detect:

Top-level functions.
Async functions.
Classes.
Methods.
Nested functions if feasible.
import x.
import x as y.
from x import y.
Docstring presence.
File path.
Line number.
Syntax-error files as graceful warnings.

V1 does not need:

Full call graph.
Type inference.
Runtime import execution.
AI summarization.
GUI integration.
Writing reports to disk.
9. Enforce read-only behavior

The indexer must not write files into the target project root.

During tests, assert that no new file appears in the fixture project after scan.

Runtime report writing, if included at all, must go only under:

<drive>:\<project>_delete_after_daily_work\intelligence\

This matters because the active compact Error Memory records that install, temp, correction, patch, validation-helper, and staging files must not be placed in the active project root.

For first patch, safest option:

Do not implement report writing yet.
Return reports in memory only.
10. Respect exclusion rules carefully

First patch has two acceptable options:

Option A — safer if exclusion API is not clear:

Implement a small default exclusion list inside Symbol Indexer v1.
Mark existing Exclusion Rules integration as TODO after audit.

Default skip list:

.git
__pycache__
.venv
venv
env
build
dist
node_modules
*.pyc

Option B — better if audit finds a clean existing exclusion API:

Use the existing Exclusion Rules API.
Do not duplicate exclusion logic.

Stop gate:

Do not guess the Exclusion Rules API.
Inspect exact source first.
11. Create validation fixture inside test script or tests fixture

Preferred first validation: self-contained test script that creates a temporary fixture using Python tempfile.

This avoids adding many fixture files.

Validation fixture should contain:

sample_module.py with:
import
from-import
top-level function with docstring
top-level function without docstring
async function
class
method
nested function
bad_syntax.py with invalid Python syntax.
Excluded folder:
__pycache__/ignored.py
.venv/ignored.py
12. Add validation script

File:

tests/test_project_intelligence_symbol_indexer.py

The script must be runnable directly:

python tests/test_project_intelligence_symbol_indexer.py

Required validation checks:

Imports package successfully.
Builds temporary fixture project.
Runs Symbol Indexer.
Detects expected top-level functions.
Detects expected async function.
Detects expected class.
Detects expected method.
Detects expected imports.
Detects docstring presence and absence.
Handles syntax error gracefully.
Skips excluded folders.
Does not write files to fixture root.
Produces JSON-serializable report.
Produces Markdown/plain report.
Contains advisory non-canonical-source warning.
Prints expected validation markers.

Final prints:

VALIDATION OK: project-intelligence-symbol-indexer-v1
STATUS: IN_SYNC
13. Run syntax validation

Before packaging:

python -m py_compile kanda_reasoner_app/project_intelligence/__init__.py
python -m py_compile kanda_reasoner_app/project_intelligence/base_engine.py
python -m py_compile kanda_reasoner_app/project_intelligence/models.py
python -m py_compile kanda_reasoner_app/project_intelligence/symbol_indexer.py
python -m py_compile tests/test_project_intelligence_symbol_indexer.py

All Python must be standard Python 3.10+ and ASCII-only.

14. Run functional validation

Command:

python tests/test_project_intelligence_symbol_indexer.py

Expected output must include:

VALIDATION OK: project-intelligence-symbol-indexer-v1
STATUS: IN_SYNC

If output lacks STATUS: IN_SYNC, do not freeze. The compact Error Memory includes a prior lesson specifically requiring this marker when the project contract requires sync evidence.

15. Prepare patch ZIP with only updated files

Patch ZIP must include only files changed/added by the patch.

Expected ZIP contents:

kanda_reasoner_app/project_intelligence/__init__.py
kanda_reasoner_app/project_intelligence/base_engine.py
kanda_reasoner_app/project_intelligence/models.py
kanda_reasoner_app/project_intelligence/symbol_indexer.py
tests/test_project_intelligence_symbol_indexer.py
KANDA_FREEZE_HINT.json

Include KANDA_FREEZE_HINT.json because this patch is freezeable after validation.

Do not include:

temporary files
logs
cache files
full source tree
old toolbox archive files
daily-work folder contents
16. Validate ZIP contract

Patch delivery must pass the KANDA ZIP contract.

Expected marker:

ZIP CONTRACT: PASS

Do not deliver the ZIP if the contract cannot be validated.

The active Error Memory includes a prevention lesson against isolated ZIP delivery: a ZIP must not be sent without install code, validation code, expected markers, and freeze/Error Memory handling when applicable.

17. Prepare install instructions

Install instructions must:

Detect project drive from $PROJECT_ROOT.
Stage ZIP under:
<drive>:\<project>_delete_after_daily_work\
Delete any root-drive ZIP copy after staging.
Extract only from the staged ZIP.
Copy only updated files into the active project.
Never place installer/temp/helper files in project root.
Use correct terminal cleanup behavior from the patch delivery contract.

This directly follows the root-cleanliness and dynamic daily-work containment lesson.

18. Prepare user-facing validation instructions

Validation block must include:

python -m py_compile kanda_reasoner_app/project_intelligence/__init__.py
python -m py_compile kanda_reasoner_app/project_intelligence/base_engine.py
python -m py_compile kanda_reasoner_app/project_intelligence/models.py
python -m py_compile kanda_reasoner_app/project_intelligence/symbol_indexer.py
python -m py_compile tests/test_project_intelligence_symbol_indexer.py
python tests/test_project_intelligence_symbol_indexer.py

Expected markers:

VALIDATION OK: project-intelligence-symbol-indexer-v1
STATUS: IN_SYNC
ZIP CONTRACT: PASS
19. Prepare freeze hint

KANDA_FREEZE_HINT.json should summarize:

feature_id: project-intelligence-symbol-indexer-v1
feature_name: Project Intelligence Symbol Indexer v1
status: freezeable_after_local_validation
validated_files:
- kanda_reasoner_app/project_intelligence/__init__.py
- kanda_reasoner_app/project_intelligence/base_engine.py
- kanda_reasoner_app/project_intelligence/models.py
- kanda_reasoner_app/project_intelligence/symbol_indexer.py
- tests/test_project_intelligence_symbol_indexer.py
validation_command:
- python tests/test_project_intelligence_symbol_indexer.py
expected_markers:
- VALIDATION OK: project-intelligence-symbol-indexer-v1
- STATUS: IN_SYNC

Freeze must still require human confirmation through Freeze Feature After Update.

20. Do not update canon unless needed

The first patch should not update the canon document unless source audit reveals that:

package path must change;
model contract must change;
exclusion API requires a different architecture;
current KANDA already has a reusable scanner;
validation conventions differ from expected.

Otherwise, keep the canon stable.

21. First implementation success criteria

The first implementation is successful only if:

Source audit is completed.
No duplicated existing scanner is introduced.
project_intelligence package exists.
Base engine contract exists.
Shared dataclasses exist.
Symbol Indexer detects functions/classes/imports/docstrings.
Syntax errors are handled gracefully.
Excluded folders are skipped.
No files are written to active target project root during scan.
Report is JSON-serializable.
Report can render as Markdown/plain text.
Validation passes.
Output includes VALIDATION OK: project-intelligence-symbol-indexer-v1.
Output includes STATUS: IN_SYNC.
ZIP contract passes.
Patch delivery includes install and validation instructions.
Freeze hint is included.
No GUI behavior is changed.
Final numbered implementation order
Load startup/project/compact Error Memory context.
Return ERROR MEMORY CHECK.
Inspect exact source files.
Run anti-duplication source audit.
Confirm first patch scope.
Create project_intelligence package.
Add models.py.
Add base_engine.py.
Add symbol_indexer.py.
Add direct validation script.
Run py_compile.
Run functional validation.
Confirm no target-root writes.
Prepare freeze hint.
Build patch ZIP with only changed files.
Validate ZIP contract.
Deliver patch with install block.
Deliver validation block.
Include expected markers.
Explain freeze handling.
Stop and wait for local validation result before any freeze-memory action.


