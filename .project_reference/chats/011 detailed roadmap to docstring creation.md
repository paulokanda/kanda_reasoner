Detailed numbered roadmap to implement Step 3 docstring logic
Target box:
Box: Step 3 / docstring_toolGUI label: Third step: insert missing docstringsPrimary owner: kanda_reasoner_app/insert_missing_docstrings_gui/
The roadmap should be implemented in small phases, not one giant patch. The uploaded plan already states the key rule: preserve scan/diff/write, AI-disabled path, AI-enabled path, selected scope logic, project-root filtering, and exclusion rules. 

1. Freeze the active box and scope
Owner paths:
kanda_reasoner_app/insert_missing_docstrings_gui/kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_gui.pykanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_gui_help/kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_help/kanda_reasoner_app/insert_missing_docstrings_gui/ai_docstring_generator.pykanda_reasoner_app/insert_missing_docstrings_gui/ai_docstring_generator_help/kanda_reasoner_app/insert_missing_docstrings_gui/context_builder.pykanda_reasoner_app/insert_missing_docstrings_gui/docstring_validator.pykanda_reasoner_app/insert_missing_docstrings_gui/docstring_policy.py
Forbidden by default:
Tab 1 architecture logicTab 2 workflow logicJSON splitterV10 retrieverruntime collectorstatic collectorreasoner_tools_gui.py layout changes, unless strictly needed for Step 3 displaygenerated architecture artifacts

2. Audit current live source before patching
Do not use old snapshots. First upload or inspect the current live files after the latest working install.
Minimum audit files:
insert_missing_docstrings_gui.pyinsert_missing_docstrings_gui_help/window_state.pyinsert_missing_docstrings_gui_help/layout_builder.pyinsert_missing_docstrings_gui_help/run_controls.pyinsert_missing_docstrings_gui_help/worker_thread.pyinsert_missing_docstrings_help/cli.pyinsert_missing_docstrings_help/run_orchestrator.pyinsert_missing_docstrings_help/file_processing.pyinsert_missing_docstrings_help/ast_safety.pydocstring_validator.pycontext_builder.pyai_docstring_generator.pyai_docstring_generator_help/response_parsing.pyai_docstring_generator_help/heuristics.py
Deliverable:
T3D-000_AUDIT_REPORT.txtNo code changes.

3. Confirm the existing user-facing options
Current Step 3 options are:
[ ] Module header docstring[ ] Classes[ ] Function/method[ ] Insert file address at top if missing[ ] Require confirm before write
The uploaded roadmap confirms this current UI state and says the file-address option was recently connected to real backend logic. 

4. Define the final managed file-address header format
Adopt this as the future canonical format:
# project-path: kanda_reasoner_app/path/to/file.py
Rules:
Use project-relative path.Use POSIX "/" separators.Do not use absolute Windows paths.Do not use bare unmanaged "# kanda_reasoner_app/path.py" long term.
Rationale: project-relative paths remain valid if the project folder moves, and the project-path: prefix prevents confusing normal comments with managed file headers. The uploaded roadmap explicitly recommends project-relative POSIX paths and discourages absolute Windows paths. 

5. Implement four-state header detection
Replace exact-only detection with this policy:
exact_managed:    "# project-path: expected/path.py" exists    action: passstale_managed:    "# project-path: old/path.py" exists    action: update to expected pathlegacy_possible:    a plausible old bare .py header exists    action: pass, do not duplicate, report warning/manual reviewabsent:    no managed or legacy-like file header exists    action: insert new managed header
This is the best balance: update stale managed headers, but do not blindly rewrite random comments that mention .py. 

6. Increase header search depth
Current five-line search is too shallow.
Use:
first 30 lines
or:
header zone until first clear code block
Reason: real files may have shebangs, encoding comments, license/SPDX comments, tool comments, or blank lines before the file-address header. 

7. Define safe insertion position
Insert the file-address header in this order:
#!/usr/bin/env python3# -*- coding: utf-8 -*-# SPDX-License-Identifier: MIT# project-path: kanda_reasoner_app/path/to/file.py"""Module docstring."""from __future__ import annotations
So the insertion index must be:
after shebangafter coding/encoding lineafter SPDX/license/copyright commentsbefore module docstringbefore from __future__ importsbefore importsbefore code
The uploaded audit specifically warns that the header should appear before the module docstring. 

8. Add file-header result model
Create a small internal result object, for example:
@dataclassclass FileHeaderResult:    action: str    expected_header: str    old_header: str    line_number: int | None    reason: str
Allowed actions:
exactinsertedupdated_stale_managedlegacy_possible_skippedskipped_outside_project_rootnot_requestedfailed
Keep this internal to Step 3.

9. Add helper functions in file_processing.py
Add focused helpers:
def expected_project_path_header(root: Path, path: Path) -> str:    ...def audit_project_path_header(text: str, expected_header: str) -> FileHeaderResult:    ...def find_project_path_insert_index(lines: list[str]) -> int:    ...def apply_project_path_header(text: str, root: Path, path: Path) -> tuple[str, FileHeaderResult]:    ...
Scope for first behavioral patch:
file_processing.pypossibly run_orchestrator.py for summary metadatatests if available
Do not touch GUI layout in this patch.

10. Skip files outside project root
Before building a project-relative header:
If file cannot be resolved relative to selected project root:    do not insert    report skipped_outside_project_root
This avoids writing misleading headers into files that do not actually belong to the selected project.

11. Verify AST/comment safety
Audit:
validate_docstring_only_change(original, modified, path)
The key question:
Does it accept comment-only changes?
If it compares ASTs, comments should be safe because comments do not change Python AST. If it rejects comment-only changes, fix the guard or add a separate safe-comment-change allowance before freezing the file-address feature. The uploaded plan flags this as a freeze requirement. 

12. Add tests for file-address hardening
Required tests:
empty filefile without trailing newlinefile with shebangfile with coding linefile with SPDX/license headerfile with exact managed headerfile with stale managed headerfile with legacy bare path headerfile with module docstringfile with from __future__ import annotationsfile outside project rootWindows path inputPOSIX output normalizationsyntax-error filerepeat write does not duplicate header
Acceptance:
# project-path: rel/path.py inserted when absentexact managed header passesstale managed header updateslegacy possible header does not duplicateoutside-root file skippedheader appears before module docstringrunning write twice creates no duplicate

13. Add summary counts to scan/diff/write
Add report counters:
file_address_exactfile_address_insertedfile_address_updated_stalefile_address_legacy_skippedfile_address_outside_root_skippedmodule_docstring_insertedclass_docstring_insertedfunction_docstring_insertedsyntax_error_skipped
Before write, show a compact summary:
File-address header:- 42 files will receive a new project-path header.- 3 stale managed headers will be updated.- 5 legacy possible headers will be skipped/manual-review.- 0 files outside project root will be touched.Docstrings:- 12 module docstrings will be inserted.- 31 class docstrings will be inserted.- 88 function/method docstrings will be inserted.
The uploaded roadmap recommends summary counts because file-address insertion may affect many files. 

14. Add large-write confirmation
If write mode would affect many files, show an extra confirmation.
Suggested thresholds:
>= 20 files changedor>= 50 file-address insertions
This protects against accidentally adding headers to a large project.

15. Add file-address-only fast path
If the user selects only:
Insert file address at top if missing = trueModule header docstring = falseClasses = falseFunction/method = false
then skip:
AST docstring candidate collectionAI generationclass/function analysisfull docstring pipeline
Run only:
file collectionexclusion filteringheader auditheader insert/updatediff/write/report
This is the highest-benefit performance improvement with low risk. The uploaded plan calls it the easiest performance win. 

16. Split Step 3 internally into three lanes
Keep the GUI simple, but internally treat Step 3 as:
Lane A: File-address header- no AI- no AST unless final validation needs it- fastest pathLane B: Deterministic docstrings- AST-based- no AILane C: AI-assisted docstrings- AST candidates- structured AI generation- validation
This keeps file header insertion from becoming tangled with docstring generation. The uploaded roadmap recommends exactly this separation. 

17. Add cheap heuristic pre-filter
Before expensive AST/AI processing:
Read file cheaply.Detect whether file might need work.Skip already-clean files before full processing.
Rules:
False positives are acceptable.False negatives are dangerous.
Meaning:
It is okay to send an extra file to AST.It is not okay to skip a file that needs docstrings.
For module docstring:
Check first meaningful content after shebang/coding/project-path header.
For class/function docstrings:
Use cheap full-text scan for class, def, async def.Do not inspect only first 30 lines, because first class may appear much later.
The uploaded plan recommends a two-pass architecture: cheap scan first, expensive AST/AI processing only when needed. 

18. Fix structured AI rendering before quality upgrades
Before improving AI docstrings, audit/fix the _prettify structured-render issue.
The previous external review identified _prettify missing import in response_parsing.py as the highest-priority AI-quality defect. 
Patch concept:
from .heuristics import _prettify
Required tests:
structured rendering produces non-empty module docstringstructured rendering produces non-empty class docstringstructured rendering produces non-empty function docstringstructured rendering produces non-empty method docstringAI failure does not crash normal fallback mode

19. Add fallback observability
Fallbacks must be visible.
Report:
generation_source:- ai_structured_json_schema- ai_structured_json_object- heuristic_fallback- cache- skipped_privatefailure_reason:- none- structured_render_error- model_invalid_json- validation_rejected- timeout- connection_error
Do not silently hide when AI fails and heuristics are used.

20. Add benchmark corpus before prompt/schema changes
Create 20 to 30 manually reviewed symbols across:
moduleclass__init__propertycached_propertydataclassprivate helperparservalidatorGUI callbackorchestration functionasync functiongenerator function
Metrics:
summary vaguenessparameter coverageraises coverageTODO densityvalidator pass/failconfidence distributionheuristic fallback rateAI actually used rateidempotency
The uploaded AI-quality review recommends a benchmark corpus before major implementation. 

21. Expand SymbolContext with deterministic AST signals
Add only AST-derived, no-runtime fields:
complexity_tiernum_branchesnum_return_sitescalled_functionsexternal_callsassigns_to_selfreads_from_selfmutated_parametersawaited_namesis_generatorhas_io_signalhas_subprocess_signalhas_logging_signalhas_global_writelocal_call_countkind_hint
These fields allow the AI prompt to use structured facts instead of guessing from raw source.

22. Upgrade ModuleSummary
Make module summary structured, not just a flat string.
Fields:
@dataclassclass ModuleSummary:    package_name: str    module_role: str    public_api: list[str]    key_dependencies: list[str]    has_cli: bool    has_gui: bool    primary_class: str | None    constant_count: int    function_count: int    class_count: int    avg_function_complexity: float
The AI-quality review specifically recommends stronger module summaries so prompts know whether a file is a facade, helper, entry point, config module, or GUI module. 

23. Add semantic validator in warning-only mode first
Add semantic checks, but initially do not hard-reject except for obvious hallucinations already covered by the existing validator.
Checks:
summary_vaguenessbool-return summary consistencyasync summary consistencyproperty has no Parameters sectionraises condition presentclaimed raise exists in ASTclaimed parameter existssummary contains no TODOside-effect claim supported by ASTmutated-parameter claim supported by AST
The review correctly says the current validator is structurally strong but does not judge whether the docstring actually describes the behavior. 

24. Add kind-specific prompt strategies
Stop using one prompt style for all symbols.
Strategies:
module:    package purpose, public API, usage entry pointsclass:    representation, lifecycle, invariants, important attributes__init__:    state initialized, parameter contracts, side effectsproperty:    document as attribute, no Parameters sectioncached_property:    property behavior plus cached result only if decorator confirms itdataclass:    field semantics from annotations/defaultsGUI callback:    triggering event, UI state mutation, return behaviorvalidator/checker:    input rules, rejection conditions, exceptionsparser/loader:    input format, output shape, parse errorsorchestrator:    high-level steps, IO/state mutation, concurrency if presentprivate helper:    brief caller-facing contract
The review identifies lack of symbol-category differentiation as a major quality problem. 

25. Improve heuristic fallback with three tiers
Current fallback is safe but can be low quality. Add:
Tier 1: trivial- no branches- one return- clear name or annotation- no TODO if safe factual description is possibleTier 2: simple- known prefix pattern- limited branches- deterministic parameter/return/raise sectionsTier 3: complex or ambiguous- minimal safe summary- specific TODO only where evidence is insufficient
Do not hallucinate. Prefer precise TODO over invented behavior. The AI review recommends stratified heuristics because current templates treat trivial getters and complex orchestrators too similarly. 

26. Add one AI repair pass behind a feature flag
Do not jump to full multi-pass AI immediately.
Add:
quality_mode=Truemax_repair_attempts=1
Flow:
draft structured JSONstructural validationsemantic warning analysisif repairable and quality_mode=True:    send deterministic validation issues back to model oncefinal validationfallback if allowed
Do not add LLM-as-judge as a hard gate yet.

27. Add staged schema v2
Do not add a huge schema in one pass.
Start with:
{  "summary": "string",  "extended_description": "string",  "parameters": [],  "returns": {},  "raises": [],  "attributes": [],  "notes": [],  "side_effects": [],  "mutated_state": [],  "preconditions": [],  "uncertain_fields": []}
Rules:
Model self-confidence is telemetry only.Validator owns acceptance.Do not let model self-score decide acceptance.

28. Add AI batching later, not now
Only after deterministic flow is stable:
collect candidatesgroup by file or batchbuild numbered promptcall local AI once per batchparse structured responsevalidate each generated docstringapply only safe insertions
Do not call local AI once per function long term, but do not implement batching before file-address hardening and validation are stable.

29. Harden encoding/BOM handling
Audit and preserve:
UTF-8 BOMline endingsfinal newlineencoding commentsread/write round trip
Add tests before broad encoding changes.

30. Add atomic writes only as a later patch
If write mode modifies many files, use safe write:
write sibling temp fileflushreplace original
Only implement after auditing current write behavior.

31. Validation commands for every bundle
Minimum:
cd E:\developer_toolspython.exe -m py_compile reasoner_tools_gui.pypython.exe -m py_compile kanda_reasoner_app\insert_missing_docstrings_gui\insert_missing_docstrings_gui.pypython.exe -m py_compile kanda_reasoner_app\insert_missing_docstrings_gui\insert_missing_docstrings_gui_help\window_state.pypython.exe -m py_compile kanda_reasoner_app\insert_missing_docstrings_gui\insert_missing_docstrings_gui_help\layout_builder.pypython.exe -m py_compile kanda_reasoner_app\insert_missing_docstrings_gui\insert_missing_docstrings_gui_help\run_controls.pypython.exe -m py_compile kanda_reasoner_app\insert_missing_docstrings_gui\insert_missing_docstrings_gui_help\worker_thread.pypython.exe -m py_compile kanda_reasoner_app\insert_missing_docstrings_gui\insert_missing_docstrings_help\cli.pypython.exe -m py_compile kanda_reasoner_app\insert_missing_docstrings_gui\insert_missing_docstrings_help\run_orchestrator.pypython.exe -m py_compile kanda_reasoner_app\insert_missing_docstrings_gui\insert_missing_docstrings_help\file_processing.pypython.exe -m py_compile kanda_reasoner_app\insert_missing_docstrings_gui\docstring_validator.py
Manual GUI:
Open KANDA Reasoner.Open Step 3.Run scan.Run diff.Run write only on a tiny test project.Run write twice.Confirm no duplicate headers.Confirm module/class/function docstring insertion still works.Confirm AI-disabled path still works.Confirm AI-enabled path does not crash.

32. Bundle discipline
Every ZIP must include:
changed files onlyno __pycache__manifest under _project_reference\BUNDLE_MANIFESTrollback notevalidation noteblast radiuswhat changedwhat did not change
Never ship full-file replacements from stale source.

33. Recommended exact implementation order
Use this order:
1. T3D-000 Audit current live Step 3 source.2. T3D-001 Add tests for current file-address behavior.3. T3D-002 Implement managed "# project-path:" format.4. T3D-003 Implement exact/stale/legacy/absent detection.5. T3D-004 Fix insertion location before module docstring.6. T3D-005 Skip outside-root files.7. T3D-006 Verify/fix AST guard for comment-only changes.8. T3D-007 Add scan/diff/write summary counts.9. T3D-008 Add large-write confirmation.10. T3D-009 Add file-address-only fast path.11. T3D-010 Add cheap heuristic pre-filter.12. T3D-011 Fix structured AI rendering / _prettify issue.13. T3D-012 Add fallback observability.14. T3D-013 Add benchmark corpus.15. T3D-014 Expand SymbolContext.16. T3D-015 Upgrade ModuleSummary.17. T3D-016 Add semantic validator warning-only.18. T3D-017 Add kind-specific prompt strategy.19. T3D-018 Upgrade heuristic fallback tiers.20. T3D-019 Add one AI repair pass behind quality_mode.21. T3D-020 Add staged schema v2.22. T3D-021 Add AI batching.23. T3D-022 Harden encoding/BOM.24. T3D-023 Add atomic writes if missing.25. T3D-024 Canon update after validation.

34. Highest-priority next patch
The next implementation should be only:
File-address hardening patch
Scope:
file_processing.pypossibly run_orchestrator.py for summary metadatatests if available
Do not touch GUI layout.
Acceptance:
# project-path: rel/path.py inserted when absentexact managed header passesstale managed header updateslegacy possible header does not duplicateoutside-root file skippedheader appears before module docstringrunning write twice creates no duplicatescan/diff/write reports counts

35. Freeze definition
Step 3 is freeze-ready only when:
scan/diff/write all workfile-address headers do not duplicatestale managed headers update safelylegacy headers are not overwritten blindlyoutside-root files are skippedfile-address-only mode is fastdocstring mode still preserves AST safetyAI mode does not regressreports show clear countslarge writes require confirmationwrite twice is idempotent