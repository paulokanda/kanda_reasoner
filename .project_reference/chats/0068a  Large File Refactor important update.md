first_prompts_to_ai.zip
Zip Archive
prompt_library.zip
Zip Archive
tell_AI_read_before_all.md
File
zz_read_only_if_modifying_startup_delivery.md
File

_RUN_COLLECTOR_STATUS.txt
Document
kanda_reasoner__ai_handoff_all_in_one.zip
Zip Archive
kanda_reasoner__ai_handoff_upload.zip
Zip Archive
kanda_reasoner__ai_handoff_upload_readme.txt
Document
kanda_reasoner__error_lessons_compact.json
File
kanda_reasoner__error_memory_ai_prompt.md
File
kanda_reasoner__error_memory_full.zip
Zip Archive
kanda_reasoner__error_memory_manifest.json
File
kanda_reasoner__png_assets_part01_of_01.zip
Zip Archive
kanda_reasoner__source_archive_part01_of_01.zip
Zip Archive

0068 using Large File Refactor Workbench.md
File
0068 Large File Refactor Workbench.md
File
Review the tutorial to refactor large files that are written in the uploads, then compare with the code, the real code of the project, and write the tutorial updated.

Pasted markdown.md
File
do this instead


Pasted text.txt
Document
Pasted text (2).txt
Document
this is teh heuristic correction of code  first upload, second uploaded is local AI audit for correctness, which is best , AI add valuable  code?

Pasted text.txt
Document
Split plan contract generated.
Status: blocked
Target file: E:\kanda_reasoner\kanda_reasoner_app\reasoner_symbol_atlas\main_helper_mapper.py
Source hash: 6637b1dde8639665f37f948d1bf7ba0711ecbe4d418ce304a01503f291f99f55

Public API preservation:
  Before: PROJECT_SYMBOL_ATLAS_HELPER_SUFFIXES, PROJECT_SYMBOL_ATLAS_MAIN_HELPER_STATUS_AMBIGUOUS_MAIN, PROJECT_SYMBOL_ATLAS_MAIN_HELPER_STATUS_INSUFFICIENT_EVIDENCE, PROJECT_SYMBOL_ATLAS_MAIN_HELPER_STATUS_NO_HELPERS_FOUND, PROJECT_SYMBOL_ATLAS_MAIN_HELPER_STATUS_READY, PROJECT_SYMBOL_ATLAS_MAIN_HELPER_STATUS_TARGET_NOT_FOUND, ProjectSymbolAtlasMainHelperDecision, ProjectSymbolAtlasMainHelperOptions, build_reasoner_symbol_atlas_main_helper_report, map_reasoner_symbol_atlas_main_helpers
  After expected: PROJECT_SYMBOL_ATLAS_HELPER_SUFFIXES, PROJECT_SYMBOL_ATLAS_MAIN_HELPER_STATUS_AMBIGUOUS_MAIN, PROJECT_SYMBOL_ATLAS_MAIN_HELPER_STATUS_INSUFFICIENT_EVIDENCE, PROJECT_SYMBOL_ATLAS_MAIN_HELPER_STATUS_NO_HELPERS_FOUND, PROJECT_SYMBOL_ATLAS_MAIN_HELPER_STATUS_READY, PROJECT_SYMBOL_ATLAS_MAIN_HELPER_STATUS_TARGET_NOT_FOUND, ProjectSymbolAtlasMainHelperDecision, ProjectSymbolAtlasMainHelperOptions, build_reasoner_symbol_atlas_main_helper_report, map_reasoner_symbol_atlas_main_helpers

Planned modules:
- main_helper_mapper.py
  Role: public_facade
  Estimated lines: 197
  Symbols: PROJECT_SYMBOL_ATLAS_HELPER_SUFFIXES, PROJECT_SYMBOL_ATLAS_MAIN_HELPER_STATUS_AMBIGUOUS_MAIN, PROJECT_SYMBOL_ATLAS_MAIN_HELPER_STATUS_INSUFFICIENT_EVIDENCE, PROJECT_SYMBOL_ATLAS_MAIN_HELPER_STATUS_NO_HELPERS_FOUND, PROJECT_SYMBOL_ATLAS_MAIN_HELPER_STATUS_READY, PROJECT_SYMBOL_ATLAS_MAIN_HELPER_STATUS_TARGET_NOT_FOUND, ProjectSymbolAtlasMainHelperDecision, ProjectSymbolAtlasMainHelperOptions, build_reasoner_symbol_atlas_main_helper_report, map_reasoner_symbol_atlas_main_helpers
  Risks: RELATIVE_IMPORT_RISK
  Status: planned
  Line policy: Original module remains the public facade.
- _main_helper_mapper_function.py
  Role: function_helper
  Estimated lines: 38
  Symbols: _coerce_project_root
  Risks: TOO_SMALL_HELPER
  Status: warning
  Line policy: Below minimum helper size; architectural correction must consolidate the helper before Workbench handoff.
- _main_helper_mapper_dependency_cluster.py
  Role: dependency_cluster_helper
  Estimated lines: 100
  Symbols: _find_target_record, _normalize_path_for_compare, _normalize_record_path
  Risks: <none>
  Status: planned
  Line policy: Cohesive dependency cluster preserved by split planning.
- _main_helper_mapper_dependency_cluster_2.py
  Role: dependency_cluster_helper
  Estimated lines: 371
  Symbols: _record_is_active, _active_records, _target_is_helper_like, _record_is_low_signal_support_file, _target_role, _select_main_record, _main_candidates_for_helper, _select_helper_records, _helper_score, _module_imports, _module_stem, _strip_helper_suffix, _has_helper_suffix, _record_is_private_helper, _public_helper_warnings
  Risks: <none>
  Status: planned
  Line policy: Cohesive dependency cluster preserved by split planning.
- _main_helper_mapper_function_2.py
  Role: function_helper
  Estimated lines: 41
  Symbols: _related_tests_to_run
  Risks: TOO_SMALL_HELPER
  Status: warning
  Line policy: Below minimum helper size; architectural correction must consolidate the helper before Workbench handoff.
- _main_helper_mapper_function_3.py
  Role: function_helper
  Estimated lines: 51
  Symbols: _decision_status
  Risks: TOO_SMALL_HELPER
  Status: warning
  Line policy: Below minimum helper size; architectural correction must consolidate the helper before Workbench handoff.
- _main_helper_mapper_function_4.py
  Role: function_helper
  Estimated lines: 37
  Symbols: _format_decision_summary
  Risks: TOO_SMALL_HELPER
  Status: warning
  Line policy: Below minimum helper size; architectural correction must consolidate the helper before Workbench handoff.

Risks:
- DECORATOR_RISK
- NESTED_SYMBOL_CLUSTER
- PUBLIC_API_RISK
- RELATIVE_IMPORT_RISK
- TOO_SMALL_HELPER

Validation blockers:
- Planned helper _main_helper_mapper_function.py is below minimum helper size of 100 lines.
- Planned helper _main_helper_mapper_function_2.py is below minimum helper size of 100 lines.
- Planned helper _main_helper_mapper_function_3.py is below minimum helper size of 100 lines.
- Planned helper _main_helper_mapper_function_4.py is below minimum helper size of 100 lines.

Important:
- This train does not write preview files.
- This train does not create project split files.
- Patch creation remains blocked until preview validation trains.

Split plan contract generated.
Status: blocked
Target file: E:\kanda_reasoner\kanda_reasoner_app\reasoner_symbol_atlas\main_helper_mapper.py
Source hash: 6637b1dde8639665f37f948d1bf7ba0711ecbe4d418ce304a01503f291f99f55

Public API preservation:
  Before: PROJECT_SYMBOL_ATLAS_HELPER_SUFFIXES, PROJECT_SYMBOL_ATLAS_MAIN_HELPER_STATUS_AMBIGUOUS_MAIN, PROJECT_SYMBOL_ATLAS_MAIN_HELPER_STATUS_INSUFFICIENT_EVIDENCE, PROJECT_SYMBOL_ATLAS_MAIN_HELPER_STATUS_NO_HELPERS_FOUND, PROJECT_SYMBOL_ATLAS_MAIN_HELPER_STATUS_READY, PROJECT_SYMBOL_ATLAS_MAIN_HELPER_STATUS_TARGET_NOT_FOUND, ProjectSymbolAtlasMainHelperDecision, ProjectSymbolAtlasMainHelperOptions, build_reasoner_symbol_atlas_main_helper_report, map_reasoner_symbol_atlas_main_helpers
  After expected: PROJECT_SYMBOL_ATLAS_HELPER_SUFFIXES, PROJECT_SYMBOL_ATLAS_MAIN_HELPER_STATUS_AMBIGUOUS_MAIN, PROJECT_SYMBOL_ATLAS_MAIN_HELPER_STATUS_INSUFFICIENT_EVIDENCE, PROJECT_SYMBOL_ATLAS_MAIN_HELPER_STATUS_NO_HELPERS_FOUND, PROJECT_SYMBOL_ATLAS_MAIN_HELPER_STATUS_READY, PROJECT_SYMBOL_ATLAS_MAIN_HELPER_STATUS_TARGET_NOT_FOUND, ProjectSymbolAtlasMainHelperDecision, ProjectSymbolAtlasMainHelperOptions, build_reasoner_symbol_atlas_main_helper_report, map_reasoner_symbol_atlas_main_helpers

Planned modules:
- main_helper_mapper.py
  Role: public_facade
  Estimated lines: 197
  Symbols: PROJECT_SYMBOL_ATLAS_HELPER_SUFFIXES, PROJECT_SYMBOL_ATLAS_MAIN_HELPER_STATUS_AMBIGUOUS_MAIN, PROJECT_SYMBOL_ATLAS_MAIN_HELPER_STATUS_INSUFFICIENT_EVIDENCE, PROJECT_SYMBOL_ATLAS_MAIN_HELPER_STATUS_NO_HELPERS_FOUND, PROJECT_SYMBOL_ATLAS_MAIN_HELPER_STATUS_READY, PROJECT_SYMBOL_ATLAS_MAIN_HELPER_STATUS_TARGET_NOT_FOUND, ProjectSymbolAtlasMainHelperDecision, ProjectSymbolAtlasMainHelperOptions, build_reasoner_symbol_atlas_main_helper_report, map_reasoner_symbol_atlas_main_helpers
  Risks: RELATIVE_IMPORT_RISK
  Status: planned
  Line policy: Original module remains the public facade.
- _main_helper_mapper_function.py
  Role: function_helper
  Estimated lines: 38
  Symbols: _coerce_project_root
  Risks: TOO_SMALL_HELPER
  Status: warning
  Line policy: Below minimum helper size; architectural correction must consolidate the helper before Workbench handoff.
- _main_helper_mapper_dependency_cluster.py
  Role: dependency_cluster_helper
  Estimated lines: 100
  Symbols: _find_target_record, _normalize_path_for_compare, _normalize_record_path
  Risks: <none>
  Status: planned
  Line policy: Cohesive dependency cluster preserved by split planning.
- _main_helper_mapper_dependency_cluster_2.py
  Role: dependency_cluster_helper
  Estimated lines: 371
  Symbols: _record_is_active, _active_records, _target_is_helper_like, _record_is_low_signal_support_file, _target_role, _select_main_record, _main_candidates_for_helper, _select_helper_records, _helper_score, _module_imports, _module_stem, _strip_helper_suffix, _has_helper_suffix, _record_is_private_helper, _public_helper_warnings
  Risks: <none>
  Status: planned
  Line policy: Cohesive dependency cluster preserved by split planning.
- _main_helper_mapper_function_2.py
  Role: function_helper
  Estimated lines: 41
  Symbols: _related_tests_to_run
  Risks: TOO_SMALL_HELPER
  Status: warning
  Line policy: Below minimum helper size; architectural correction must consolidate the helper before Workbench handoff.
- _main_helper_mapper_function_3.py
  Role: function_helper
  Estimated lines: 51
  Symbols: _decision_status
  Risks: TOO_SMALL_HELPER
  Status: warning
  Line policy: Below minimum helper size; architectural correction must consolidate the helper before Workbench handoff.
- _main_helper_mapper_function_4.py
  Role: function_helper
  Estimated lines: 37
  Symbols: _format_decision_summary
  Risks: TOO_SMALL_HELPER
  Status: warning
  Line policy: Below minimum helper size; architectural correction must consolidate the helper before Workbench handoff.

Risks:
- DECORATOR_RISK
- NESTED_SYMBOL_CLUSTER
- PUBLIC_API_RISK
- RELATIVE_IMPORT_RISK
- TOO_SMALL_HELPER

Validation blockers:
- Planned helper _main_helper_mapper_function.py is below minimum helper size of 100 lines.
- Planned helper _main_helper_mapper_function_2.py is below minimum helper size of 100 lines.
- Planned helper _main_helper_mapper_function_3.py is below minimum helper size of 100 lines.
- Planned helper _main_helper_mapper_function_4.py is below minimum helper size of 100 lines.

Important:
- This train does not write preview files.
- This train does not create project split files.
- Patch creation remains blocked until preview validation trains.

Docstring proposal contract generated.
Proposal count: 7

Important:
- This train does not insert docstrings.
- Existing docstrings are not overwritten.
- Low-confidence proposals require review before preview writing.
- No preview files or project patch payload files are generated.

Proposals:
- planned_module: main_helper_mapper.py
  Provenance: deterministic_template
  Confidence: medium
  Status: proposed
  Reason: Planned module needs a reviewable module docstring before preview writing.
  Risks: RELATIVE_IMPORT_RISK
  Proposed docstring:
    """Preserve the public facade for the original module.
    Generated module docstring proposal; no preview file has been written."""
- planned_module: _main_helper_mapper_function.py
  Provenance: deterministic_template
  Confidence: medium
  Status: proposed
  Reason: Planned module needs a reviewable module docstring before preview writing.
  Risks: TOO_SMALL_HELPER
  Proposed docstring:
    """Group function helper symbols for review.
    Generated module docstring proposal; no preview file has been written."""
- planned_module: _main_helper_mapper_dependency_cluster.py
  Provenance: deterministic_template
  Confidence: medium
  Status: proposed
  Reason: Planned module needs a reviewable module docstring before preview writing.
  Risks: <none>
  Proposed docstring:
    """Group dependency cluster helper symbols for review.
    Generated module docstring proposal; no preview file has been written."""
- planned_module: _main_helper_mapper_dependency_cluster_2.py
  Provenance: deterministic_template
  Confidence: medium
  Status: proposed
  Reason: Planned module needs a reviewable module docstring before preview writing.
  Risks: <none>
  Proposed docstring:
    """Group dependency cluster helper symbols for review.
    Generated module docstring proposal; no preview file has been written."""
- planned_module: _main_helper_mapper_function_2.py
  Provenance: deterministic_template
  Confidence: medium
  Status: proposed
  Reason: Planned module needs a reviewable module docstring before preview writing.
  Risks: TOO_SMALL_HELPER
  Proposed docstring:
    """Group function helper symbols for review.
    Generated module docstring proposal; no preview file has been written."""
- planned_module: _main_helper_mapper_function_3.py
  Provenance: deterministic_template
  Confidence: medium
  Status: proposed
  Reason: Planned module needs a reviewable module docstring before preview writing.
  Risks: TOO_SMALL_HELPER
  Proposed docstring:
    """Group function helper symbols for review.
    Generated module docstring proposal; no preview file has been written."""
- planned_module: _main_helper_mapper_function_4.py
  Provenance: deterministic_template
  Confidence: medium
  Status: proposed
  Reason: Planned module needs a reviewable module docstring before preview writing.
  Risks: TOO_SMALL_HELPER
  Proposed docstring:
    """Group function helper symbols for review.
    Generated module docstring proposal; no preview file has been written."""
audit versions and correct if necessary and also correct:

here in text is heuristic uploaded is Ai, correction copy comprehensive planning for web AI is not active for heuristic plan = comprehensive Planning for web ai  and receive planning form web AI must be active all the time to copy any plan active at tne moment

Pasted text.txt
Document
first check if heuristic and local AI still the same :

ACTIVE PLANNER VERSION: Heuristic

Split plan contract generated.
Status: blocked
Target file: E:\kanda_reasoner\kanda_reasoner_app\reasoner_symbol_atlas\main_helper_mapper.py
Source hash: 6637b1dde8639665f37f948d1bf7ba0711ecbe4d418ce304a01503f291f99f55

Public API preservation:
  Before: PROJECT_SYMBOL_ATLAS_HELPER_SUFFIXES, PROJECT_SYMBOL_ATLAS_MAIN_HELPER_STATUS_AMBIGUOUS_MAIN, PROJECT_SYMBOL_ATLAS_MAIN_HELPER_STATUS_INSUFFICIENT_EVIDENCE, PROJECT_SYMBOL_ATLAS_MAIN_HELPER_STATUS_NO_HELPERS_FOUND, PROJECT_SYMBOL_ATLAS_MAIN_HELPER_STATUS_READY, PROJECT_SYMBOL_ATLAS_MAIN_HELPER_STATUS_TARGET_NOT_FOUND, ProjectSymbolAtlasMainHelperDecision, ProjectSymbolAtlasMainHelperOptions, build_reasoner_symbol_atlas_main_helper_report, map_reasoner_symbol_atlas_main_helpers
  After expected: PROJECT_SYMBOL_ATLAS_HELPER_SUFFIXES, PROJECT_SYMBOL_ATLAS_MAIN_HELPER_STATUS_AMBIGUOUS_MAIN, PROJECT_SYMBOL_ATLAS_MAIN_HELPER_STATUS_INSUFFICIENT_EVIDENCE, PROJECT_SYMBOL_ATLAS_MAIN_HELPER_STATUS_NO_HELPERS_FOUND, PROJECT_SYMBOL_ATLAS_MAIN_HELPER_STATUS_READY, PROJECT_SYMBOL_ATLAS_MAIN_HELPER_STATUS_TARGET_NOT_FOUND, ProjectSymbolAtlasMainHelperDecision, ProjectSymbolAtlasMainHelperOptions, build_reasoner_symbol_atlas_main_helper_report, map_reasoner_symbol_atlas_main_helpers

Planned modules:
- main_helper_mapper.py
  Role: public_facade
  Estimated lines: 197
  Symbols: PROJECT_SYMBOL_ATLAS_HELPER_SUFFIXES, PROJECT_SYMBOL_ATLAS_MAIN_HELPER_STATUS_AMBIGUOUS_MAIN, PROJECT_SYMBOL_ATLAS_MAIN_HELPER_STATUS_INSUFFICIENT_EVIDENCE, PROJECT_SYMBOL_ATLAS_MAIN_HELPER_STATUS_NO_HELPERS_FOUND, PROJECT_SYMBOL_ATLAS_MAIN_HELPER_STATUS_READY, PROJECT_SYMBOL_ATLAS_MAIN_HELPER_STATUS_TARGET_NOT_FOUND, ProjectSymbolAtlasMainHelperDecision, ProjectSymbolAtlasMainHelperOptions, build_reasoner_symbol_atlas_main_helper_report, map_reasoner_symbol_atlas_main_helpers
  Risks: RELATIVE_IMPORT_RISK
  Status: planned
  Line policy: Original module remains the public facade.
- _main_helper_mapper_function.py
  Role: function_helper
  Estimated lines: 38
  Symbols: _coerce_project_root
  Risks: TOO_SMALL_HELPER
  Status: warning
  Line policy: Below minimum helper size; architectural correction must consolidate the helper before Workbench handoff.
- _main_helper_mapper_dependency_cluster.py
  Role: dependency_cluster_helper
  Estimated lines: 100
  Symbols: _find_target_record, _normalize_path_for_compare, _normalize_record_path
  Risks: <none>
  Status: planned
  Line policy: Cohesive dependency cluster preserved by split planning.
- _main_helper_mapper_dependency_cluster_2.py
  Role: dependency_cluster_helper
  Estimated lines: 371
  Symbols: _record_is_active, _active_records, _target_is_helper_like, _record_is_low_signal_support_file, _target_role, _select_main_record, _main_candidates_for_helper, _select_helper_records, _helper_score, _module_imports, _module_stem, _strip_helper_suffix, _has_helper_suffix, _record_is_private_helper, _public_helper_warnings
  Risks: <none>
  Status: planned
  Line policy: Cohesive dependency cluster preserved by split planning.
- _main_helper_mapper_function_2.py
  Role: function_helper
  Estimated lines: 41
  Symbols: _related_tests_to_run
  Risks: TOO_SMALL_HELPER
  Status: warning
  Line policy: Below minimum helper size; architectural correction must consolidate the helper before Workbench handoff.
- _main_helper_mapper_function_3.py
  Role: function_helper
  Estimated lines: 51
  Symbols: _decision_status
  Risks: TOO_SMALL_HELPER
  Status: warning
  Line policy: Below minimum helper size; architectural correction must consolidate the helper before Workbench handoff.
- _main_helper_mapper_function_4.py
  Role: function_helper
  Estimated lines: 37
  Symbols: _format_decision_summary
  Risks: TOO_SMALL_HELPER
  Status: warning
  Line policy: Below minimum helper size; architectural correction must consolidate the helper before Workbench handoff.

Risks:
- DECORATOR_RISK
- NESTED_SYMBOL_CLUSTER
- PUBLIC_API_RISK
- RELATIVE_IMPORT_RISK
- TOO_SMALL_HELPER

Validation blockers:
- Planned helper _main_helper_mapper_function.py is below minimum helper size of 100 lines.
- Planned helper _main_helper_mapper_function_2.py is below minimum helper size of 100 lines.
- Planned helper _main_helper_mapper_function_3.py is below minimum helper size of 100 lines.
- Planned helper _main_helper_mapper_function_4.py is below minimum helper size of 100 lines.

Important:
- This train does not write preview files.
- This train does not create project split files.
- Patch creation remains blocked until preview validation trains.

Docstring proposal contract generated.
Proposal count: 7

Important:
- This train does not insert docstrings.
- Existing docstrings are not overwritten.
- Low-confidence proposals require review before preview writing.
- No preview files or project patch payload files are generated.

Proposals:
- planned_module: main_helper_mapper.py
  Provenance: deterministic_template
  Confidence: medium
  Status: proposed
  Reason: Planned module needs a reviewable module docstring before preview writing.
  Risks: RELATIVE_IMPORT_RISK
  Proposed docstring:
    """Preserve the public facade for the original module.
    Generated module docstring proposal; no preview file has been written."""
- planned_module: _main_helper_mapper_function.py
  Provenance: deterministic_template
  Confidence: medium
  Status: proposed
  Reason: Planned module needs a reviewable module docstring before preview writing.
  Risks: TOO_SMALL_HELPER
  Proposed docstring:
    """Group function helper symbols for review.
    Generated module docstring proposal; no preview file has been written."""
- planned_module: _main_helper_mapper_dependency_cluster.py
  Provenance: deterministic_template
  Confidence: medium
  Status: proposed
  Reason: Planned module needs a reviewable module docstring before preview writing.
  Risks: <none>
  Proposed docstring:
    """Group dependency cluster helper symbols for review.
    Generated module docstring proposal; no preview file has been written."""
- planned_module: _main_helper_mapper_dependency_cluster_2.py
  Provenance: deterministic_template
  Confidence: medium
  Status: proposed
  Reason: Planned module needs a reviewable module docstring before preview writing.
  Risks: <none>
  Proposed docstring:
    """Group dependency cluster helper symbols for review.
    Generated module docstring proposal; no preview file has been written."""
- planned_module: _main_helper_mapper_function_2.py
  Provenance: deterministic_template
  Confidence: medium
  Status: proposed
  Reason: Planned module needs a reviewable module docstring before preview writing.
  Risks: TOO_SMALL_HELPER
  Proposed docstring:
    """Group function helper symbols for review.
    Generated module docstring proposal; no preview file has been written."""
- planned_module: _main_helper_mapper_function_3.py
  Provenance: deterministic_template
  Confidence: medium
  Status: proposed
  Reason: Planned module needs a reviewable module docstring before preview writing.
  Risks: TOO_SMALL_HELPER
  Proposed docstring:
    """Group function helper symbols for review.
    Generated module docstring proposal; no preview file has been written."""
- planned_module: _main_helper_mapper_function_4.py
  Provenance: deterministic_template
  Confidence: medium
  Status: proposed
  Reason: Planned module needs a reviewable module docstring before preview writing.
  Risks: TOO_SMALL_HELPER
  Proposed docstring:
    """Group function helper symbols for review.
    Generated module docstring proposal; no preview file has been written."""


ai :


Pasted text.txt
Document
ACTIVE PLANNER VERSION: Heuristic

Split plan contract generated.
Status: planned
Target file: E:\kanda_reasoner\kanda_reasoner_app\reasoner_symbol_atlas\main_helper_mapper.py
Source hash: 6637b1dde8639665f37f948d1bf7ba0711ecbe4d418ce304a01503f291f99f55

Public API preservation:
  Before: PROJECT_SYMBOL_ATLAS_HELPER_SUFFIXES, PROJECT_SYMBOL_ATLAS_MAIN_HELPER_STATUS_AMBIGUOUS_MAIN, PROJECT_SYMBOL_ATLAS_MAIN_HELPER_STATUS_INSUFFICIENT_EVIDENCE, PROJECT_SYMBOL_ATLAS_MAIN_HELPER_STATUS_NO_HELPERS_FOUND, PROJECT_SYMBOL_ATLAS_MAIN_HELPER_STATUS_READY, PROJECT_SYMBOL_ATLAS_MAIN_HELPER_STATUS_TARGET_NOT_FOUND, ProjectSymbolAtlasMainHelperDecision, ProjectSymbolAtlasMainHelperOptions, build_reasoner_symbol_atlas_main_helper_report, map_reasoner_symbol_atlas_main_helpers
  After expected: PROJECT_SYMBOL_ATLAS_HELPER_SUFFIXES, PROJECT_SYMBOL_ATLAS_MAIN_HELPER_STATUS_AMBIGUOUS_MAIN, PROJECT_SYMBOL_ATLAS_MAIN_HELPER_STATUS_INSUFFICIENT_EVIDENCE, PROJECT_SYMBOL_ATLAS_MAIN_HELPER_STATUS_NO_HELPERS_FOUND, PROJECT_SYMBOL_ATLAS_MAIN_HELPER_STATUS_READY, PROJECT_SYMBOL_ATLAS_MAIN_HELPER_STATUS_TARGET_NOT_FOUND, ProjectSymbolAtlasMainHelperDecision, ProjectSymbolAtlasMainHelperOptions, build_reasoner_symbol_atlas_main_helper_report, map_reasoner_symbol_atlas_main_helpers

Planned modules:
- main_helper_mapper.py
  Role: public_facade
  Estimated lines: 197
  Symbols: PROJECT_SYMBOL_ATLAS_HELPER_SUFFIXES, PROJECT_SYMBOL_ATLAS_MAIN_HELPER_STATUS_AMBIGUOUS_MAIN, PROJECT_SYMBOL_ATLAS_MAIN_HELPER_STATUS_INSUFFICIENT_EVIDENCE, PROJECT_SYMBOL_ATLAS_MAIN_HELPER_STATUS_NO_HELPERS_FOUND, PROJECT_SYMBOL_ATLAS_MAIN_HELPER_STATUS_READY, PROJECT_SYMBOL_ATLAS_MAIN_HELPER_STATUS_TARGET_NOT_FOUND, ProjectSymbolAtlasMainHelperDecision, ProjectSymbolAtlasMainHelperOptions, build_reasoner_symbol_atlas_main_helper_report, map_reasoner_symbol_atlas_main_helpers
  Risks: RELATIVE_IMPORT_RISK
  Status: planned
  Line policy: Original module remains the public facade.
- _main_helper_mapper_path_resolution.py
  Role: dependency_cluster_helper
  Estimated lines: 122
  Symbols: _coerce_project_root, _find_target_record, _normalize_path_for_compare, _normalize_record_path
  Risks: <none>
  Status: planned
  Line policy: Cohesive dependency cluster preserved by split planning.
- _main_helper_mapper_helper_selection.py
  Role: dependency_cluster_helper
  Estimated lines: 452
  Symbols: _record_is_active, _active_records, _target_is_helper_like, _record_is_low_signal_support_file, _target_role, _select_main_record, _main_candidates_for_helper, _select_helper_records, _helper_score, _module_imports, _module_stem, _strip_helper_suffix, _has_helper_suffix, _record_is_private_helper, _public_helper_warnings, _related_tests_to_run, _decision_status, _format_decision_summary
  Risks: <none>
  Status: planned
  Line policy: Cohesive dependency cluster preserved by split planning.

Heuristic candidate selection:
  Selected: heuristic:balanced
  Strategy: balanced
  - heuristic:balanced: status=valid; score=0.75933; helpers=2; responsibility=0.849312; topology=0.92; mixed_penalty=0.150688; history=1.0
  - heuristic:responsibility_dominant: status=valid; score=0.75933; helpers=2; responsibility=0.849312; topology=0.92; mixed_penalty=0.150688; history=1.0
  - heuristic:dependency_dominant: status=blocked; score=0.737744; helpers=3; responsibility=1.0; topology=0.84; mixed_penalty=0.0; history=1.0

Git historical coupling:
  Status: ready
  Source: kanda_reasoner_app/reasoner_symbol_atlas/main_helper_mapper.py
  Queried clusters: 6
  History commits observed: 2
  Strongest co-change affinities:
    - dependency:_related_tests_to_run <-> dependency:_format_decision_summary: score=1.0; shared_commits=2
    - dependency:_related_tests_to_run <-> dependency:_decision_status: score=1.0; shared_commits=2
    - dependency:_record_is_active+_active_records+_target_is_helper_like+_record_is_low_signal_support_file+_target_role+_select_main_record+_main_candidates_for_helper+_select_helper_records+_helper_score+_module_imports+_module_stem+_strip_helper_suffix+_has_helper_suffix+_record_is_private_helper+_public_helper_warnings <-> dependency:_related_tests_to_run: score=1.0; shared_commits=2
    - dependency:_record_is_active+_active_records+_target_is_helper_like+_record_is_low_signal_support_file+_target_role+_select_main_record+_main_candidates_for_helper+_select_helper_records+_helper_score+_module_imports+_module_stem+_strip_helper_suffix+_has_helper_suffix+_record_is_private_helper+_public_helper_warnings <-> dependency:_format_decision_summary: score=1.0; shared_commits=2
    - dependency:_record_is_active+_active_records+_target_is_helper_like+_record_is_low_signal_support_file+_target_role+_select_main_record+_main_candidates_for_helper+_select_helper_records+_helper_score+_module_imports+_module_stem+_strip_helper_suffix+_has_helper_suffix+_record_is_private_helper+_public_helper_warnings <-> dependency:_decision_status: score=1.0; shared_commits=2

Responsibility labeling:
  - path_resolution: confidence=high; score=1.0
    Evidence: path, normalize, root, project, compare, find
  - helper_selection: confidence=high; score=1.0
    Secondary: decision_reporting
    Evidence: record, main, target, suffix, active, stem, select, score

Projected dependency topology:
  Status: ready_with_warnings
  Helper topological order: _main_helper_mapper_helper_selection.py -> _main_helper_mapper_path_resolution.py
  Directed edges:
    - _main_helper_mapper_helper_selection.py -> main_helper_mapper.py
    - main_helper_mapper.py -> _main_helper_mapper_helper_selection.py
    - main_helper_mapper.py -> _main_helper_mapper_path_resolution.py
  Facade back-references:
    - _main_helper_mapper_helper_selection.py -> main_helper_mapper.py
  Helper cycles: <none>
  Boundary cycle components: [['_main_helper_mapper_helper_selection.py', 'main_helper_mapper.py']]

Selected candidate quality evidence:
  Responsibility cohesion: 0.849312
  Topology score: 0.92
  Mixed-responsibility penalty: 0.150688
  Mixed-responsibility helpers:
    - primary=helper_selection; secondary=decision_reporting; lines=452; penalty=0.19136

Risks:
- DECORATOR_RISK
- FACADE_BACK_REFERENCE_RISK
- FACADE_BOUNDARY_CYCLE_RISK
- NESTED_SYMBOL_CLUSTER
- PUBLIC_API_RISK
- RELATIVE_IMPORT_RISK

Validation blockers:
- <none>

Important:
- This train does not write preview files.
- This train does not create project split files.
- Patch creation remains blocked until preview validation trains.

Docstring proposal contract generated.
Proposal count: 3

Important:
- This train does not insert docstrings.
- Existing docstrings are not overwritten.
- Low-confidence proposals require review before preview writing.
- No preview files or project patch payload files are generated.

Proposals:
- planned_module: main_helper_mapper.py
  Provenance: deterministic_template
  Confidence: medium
  Status: proposed
  Reason: Planned module needs a reviewable module docstring before preview writing.
  Risks: RELATIVE_IMPORT_RISK
  Proposed docstring:
    """Preserve the public facade for the original module.
    Generated module docstring proposal; no preview file has been written."""
- planned_module: _main_helper_mapper_path_resolution.py
  Provenance: deterministic_template
  Confidence: medium
  Status: proposed
  Reason: Planned module needs a reviewable module docstring before preview writing.
  Risks: <none>
  Proposed docstring:
    """Group dependency cluster helper symbols for review.
    Generated module docstring proposal; no preview file has been written."""
- planned_module: _main_helper_mapper_helper_selection.py
  Provenance: deterministic_template
  Confidence: medium
  Status: proposed
  Reason: Planned module needs a reviewable module docstring before preview writing.
  Risks: <none>
  Proposed docstring:
    """Group dependency cluster helper symbols for review.
    Generated module docstring proposal; no preview file has been written."""


local ai:

compare both

The installer is rejecting the payload because the packaged text contains the begin-marker string more than once—most likely once as the real wrapper and again inside explanatory/instruction text. I’m inspecting the exact ZIP payload and installer check now, then I’ll rebuild a corrected import ZIP whose payload contains exactly one begin marker and one end marker.

PS E:\kanda_reasoner> $ErrorActionPreference = "Stop"
PS E:\kanda_reasoner> 
PS E:\kanda_reasoner> $ZIP = "E:\kanda_imported_web_ai_main_helper_mapper_v1.zip"
PS E:\kanda_reasoner> $PROJECT_ROOT = "E:\kanda_reasoner"
PS E:\kanda_reasoner> 
PS E:\kanda_reasoner> $DRIVE_ROOT = [System.IO.Path]::GetPathRoot($PROJECT_ROOT)
PS E:\kanda_reasoner> $PROJECT_NAME = Split-Path -Leaf $PROJECT_ROOT
PS E:\kanda_reasoner> 
PS E:\kanda_reasoner> $WORK_DIR = [System.IO.Path]::Combine(
>>     $DRIVE_ROOT,
>>     $PROJECT_NAME + "_delete_after_daily_work",
>>     "imported_web_ai_main_helper_mapper_v1"
>> )
PS E:\kanda_reasoner> 
PS E:\kanda_reasoner> if (Test-Path $WORK_DIR) {
>>     Remove-Item 
>>         -Path $WORK_DIR                                                                                    
>>         -Recurse                                                                                           
>>         -Force                                                                                              
>> }                                                                                                           
PS E:\kanda_reasoner>                                                                                          
PS E:\kanda_reasoner> New-Item                                                                                
>>     -ItemType Directory                                                                                    
>>     -Path $WORK_DIR                                                                                        
>>     -Force | Out-Null                                                                                       
PS E:\kanda_reasoner> 
PS E:\kanda_reasoner> Expand-Archive 
>>     -Path $ZIP                                                                                             
>>     -DestinationPath $WORK_DIR                                                                             
>>     -Force                                                                                                  
PS E:\kanda_reasoner> 
PS E:\kanda_reasoner> $INSTALL_SCRIPT = Join-Path 
>>     $WORK_DIR                                                                                              
>>     "INSTALL.ps1"                                                                                           
PS E:\kanda_reasoner> 
PS E:\kanda_reasoner> powershell 
>>     -NoProfile                                                                                             
>>     -ExecutionPolicy Bypass                                                                                
>>     -File $INSTALL_SCRIPT                                                                                  
>>     -ProjectRoot $PROJECT_ROOT                                                                              
Payload must contain exactly one Web AI begin marker.
At E:\kanda_reasoner_delete_after_daily_work\imported_web_ai_main_helper_mapper_v1\INSTALL.ps1:43 char:5
+     throw "Payload must contain exactly one Web AI begin marker."
+     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : OperationStopped: (Payload must co...I begin marker.:String) [], RuntimeExcepti 
   on
    + FullyQualifiedErrorId : Payload must contain exactly one Web AI begin marker.
 
PS E:\kanda_reasoner> 
PS E:\kanda_reasoner> if ($LASTEXITCODE -ne 0) {
>>     throw "Imported Web AI Version installation failed."                                                    
>> }
Imported Web AI Version installation failed.
At line:2 char:5
+     throw "Imported Web AI Version installation failed."
+     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : OperationStopped: (Imported Web AI...llation failed.:String) [], RuntimeExcepti 
   on
    + FullyQualifiedErrorId : Imported Web AI Version installation failed.
 
PS E:\kanda_reasoner> 

I have the full failure trace now. I’m checking the exact archived payload and installer regex/count logic against the delivered ZIP, then I’ll rebuild the import package so the marker contract is provably one begin marker and one end marker before delivery.

I found the exact bug: the payload itself is correct—one begin marker and one end marker. The installer check is wrong. PowerShell’s instance .Split($BeginMarker) does not reliably mean “split on this entire literal string”; overload binding can treat the marker as a character separator set, so the count becomes incorrect.

I’m replacing that check with literal escaped regex matching and rebuilding the ZIP. The imported plan content and hashes do not need to change.

The corrected ZIP is rebuilt and passes exact archive checks:

files: exactly 2
begin marker count: 1
end marker count: 1
installer count method: literal escaped regex
old `.Split($Marker)` logic: removed

I’m also preparing the error-memory intake for this installer bug so the same PowerShell overload mistake is not repeated in future generated installers.

The failure was in the installer, not the Web AI payload.

The original payload already contained exactly:

KANDA_WEB_AI_PLANNING_RESPONSE_BEGIN   × 1
KANDA_WEB_AI_PLANNING_RESPONSE_END     × 1

The bug was this PowerShell logic:

$PayloadText.Split($BeginMarker)

PowerShell/.NET overload binding can interpret that as character-separator splitting rather than literal whole-string splitting. The installer therefore falsely concluded that the marker appeared multiple times.

I replaced it with literal escaped regex counting:

[regex]::Matches(
    $PayloadText,
    [regex]::Escape($BeginMarker)
).Count

Corrected ZIP

SHA-256:

31b6b73a859f14c4fa6232caed19b16e4f6218835a07d2de7d1a813f063b5686

Exact archive validation:

EXACT_ZIP_FILES: PASS
BEGIN_MARKER_COUNT: 1
END_MARKER_COUNT: 1
INSTALLER_LITERAL_REGEX_COUNT: PASS

WEB_AI_MARKER_CONTRACT: PASS
WEB_AI_JSON_PARSE: PASS
WEB_AI_REQUIRED_FIELDS: PASS
VERDICT: valid_or_refine
REASSIGNMENTS: 1

The planning proposal itself is unchanged:

Source hash:
6637b1dde8639665f37f948d1bf7ba0711ecbe4d418ce304a01503f291f99f55

Base plan hash:
5b43bf2d61baf9139da5253121dab42b6733685128e4b5fd73091f9a0eebedb4

Install the corrected version

Place it at:

E:\kanda_imported_web_ai_main_helper_mapper_v1_fixed.zip

Then run:

$ErrorActionPreference = "Stop"
$InstallFailed = $false

try {
    $ZIP = "E:\kanda_imported_web_ai_main_helper_mapper_v1_fixed.zip"
    $PROJECT_ROOT = "E:\kanda_reasoner"

    $PROJECT_ROOT = [System.IO.Path]::GetFullPath($PROJECT_ROOT)
    $PROJECT_NAME = Split-Path -Leaf $PROJECT_ROOT
    $DRIVE_ROOT = [System.IO.Path]::GetPathRoot($PROJECT_ROOT)

    $WORK_DIR = [System.IO.Path]::Combine(
        $DRIVE_ROOT,
        $PROJECT_NAME + "_delete_after_daily_work",
        "imported_web_ai_main_helper_mapper_v1_fixed"
    )

    if (-not (Test-Path $ZIP)) {
        throw "Corrected Web AI ZIP not found: $ZIP"
    }

    if (Test-Path $WORK_DIR) {
        Remove-Item `
            -Path $WORK_DIR `
            -Recurse `
            -Force
    }

    New-Item `
        -ItemType Directory `
        -Path $WORK_DIR `
        -Force | Out-Null

    Expand-Archive `
        -Path $ZIP `
        -DestinationPath $WORK_DIR `
        -Force

    $INSTALL_SCRIPT = Join-Path `
        $WORK_DIR `
        "INSTALL.ps1"

    if (-not (Test-Path $INSTALL_SCRIPT)) {
        throw "INSTALL.ps1 not found: $INSTALL_SCRIPT"
    }

    powershell `
        -NoProfile `
        -ExecutionPolicy Bypass `
        -File $INSTALL_SCRIPT `
        -ProjectRoot $PROJECT_ROOT

    if ($LASTEXITCODE -ne 0) {
        throw "Imported Web AI Version installation failed."
    }
}
catch {
    $InstallFailed = $true

    Write-Host ""
    Write-Host "INSTALL ERROR"
    Write-Host $_.Exception.Message

    if ($_.ScriptStackTrace) {
        Write-Host $_.ScriptStackTrace
    }
}

if (-not $InstallFailed) {
    Write-Host ""
    Write-Host "IMPORTED WEB AI ARTIFACT INSTALL: PASS"
    Write-Host ""
    Write-Host "Next:"
    Write-Host "1. Open Large File Refactor Planner"
    Write-Host "2. Press Receive Planning from Web AI"
    Write-Host "3. Review the imported proposal"
    Write-Host "4. Load as Imported Web AI Version"
}

Expected terminal output:

IMPORTED_WEB_AI_PLAN_INSTALLED:
E:\kanda_reasoner_show_project_to_AI\project_large_file_refactor_planner_web_ai_import\pending_imported_web_ai_plan.txt

WEB_AI_BEGIN_MARKER_COUNT: 1
WEB_AI_END_MARKER_COUNT: 1
WEB_AI_PAYLOAD_COPY_VERIFY: PASS

NEXT:
Open Large File Refactor Planner and press Receive Planning from Web AI.

Then:

Large File Refactor Planner
→ Receive Planning from Web AI
→ Review proposal
→ Load as Imported Web AI Version

Error Memory staging

This error should be remembered because the wrong pattern could affect future PowerShell installers.

Run:

$ErrorActionPreference = "Stop"
$ErrorMemoryFailed = $false

try {
    $PROJECT_ROOT = "E:\kanda_reasoner"

    $PROJECT_ROOT = [System.IO.Path]::GetFullPath($PROJECT_ROOT)
    $PROJECT_NAME = Split-Path -Leaf $PROJECT_ROOT
    $DRIVE_ROOT = [System.IO.Path]::GetPathRoot($PROJECT_ROOT)

    $SHOW_PROJECT_ROOT = [System.IO.Path]::Combine(
        $DRIVE_ROOT,
        $PROJECT_NAME + "_show_project_to_AI"
    )

    $PENDING_INTAKE_DIR = [System.IO.Path]::Combine(
        $SHOW_PROJECT_ROOT,
        "project_error_memory",
        "pending_ai_assisted_error_lesson_intake"
    )

    $INTAKE_FILE = [System.IO.Path]::Combine(
        $PENDING_INTAKE_DIR,
        "KANDA_ERROR_LESSON_JSON_web_ai_import_installer_literal_marker_count_v1.txt"
    )

    if (-not (Test-Path $PENDING_INTAKE_DIR)) {
        New-Item `
            -ItemType Directory `
            -Path $PENDING_INTAKE_DIR `
            -Force | Out-Null
    }

    $LESSON = @'
KANDA_ERROR_LESSON_JSON_BEGIN
{
  "schema_version": "1.0",
  "lesson_id": "lesson-web-ai-import-installer-literal-marker-count-v1",
  "status": "active",
  "superseded_by": "",
  "project_slug": "kanda_reasoner",
  "operation_phase": "install",
  "created_at_utc": "2026-07-05T00:00:00Z",
  "updated_at_utc": "2026-07-05T00:00:00Z",
  "source_patch_zip": "kanda_imported_web_ai_main_helper_mapper_v1.zip",
  "raw_error_text": "The Imported Web AI installer rejected a valid payload with: Payload must contain exactly one Web AI begin marker. Exact archive inspection proved the payload contained one begin marker and one end marker.",
  "raw_error_snapshot_scrubbed": "A PowerShell installer falsely rejected a marker-wrapped payload even though exact file inspection showed one literal begin marker and one literal end marker.",
  "symptom": "Installer throws a marker-count validation error for a payload whose literal marker counts are both exactly one.",
  "root_cause": "The installer used String.Split with a string variable to count marker occurrences. PowerShell/.NET overload binding did not reliably express literal whole-string splitting and could bind to separator behavior inconsistent with the intended marker-count contract.",
  "wrong_assumption": "Calling $PayloadText.Split($Marker) was assumed to count occurrences of the complete literal marker string.",
  "correct_fix": "Count literal markers with Regex.Matches using Regex.Escape(marker), or another explicit whole-string occurrence counter. Validate exactly one begin marker, exactly one end marker, correct start position, correct end position, and exact installed-payload copy equality.",
  "long_term_prevention": "Generated PowerShell installers must not use String.Split(markerString) as a literal substring occurrence counter. Installer validators should test the exact archive payload and the exact PowerShell marker-count implementation independently.",
  "do_not_repeat_rule": "Do not use PowerShell String.Split with a marker string to count complete literal marker occurrences.",
  "exception": {
    "type": "WebAIImportInstallerMarkerCountFailure",
    "phase": "install",
    "relative_file_path": "external Web AI import installer/INSTALL.ps1",
    "function_or_test_name": "Web AI marker contract validation",
    "message_normalized": "valid payload falsely rejected because marker count used ambiguous String.Split overload behavior",
    "stacktrace_scrubbed": "Installer stopped at the begin-marker count guard before writing the imported Web AI artifact."
  },
  "fingerprint": {
    "strategy": "v1_structural_conservative",
    "components": [
      "WebAIImportInstallerMarkerCountFailure",
      "PowerShell String.Split overload",
      "literal marker counting",
      "Regex.Escape"
    ],
    "fingerprint_hash": "e372733c94834163d921a9fe8b2226639ed77399e89efb942474a42d7f41a23f"
  },
  "prevention_triggers": [
    "PowerShell installer counts markers with .Split($Marker)",
    "payload marker count fails despite exact file count of one",
    "generated installer validates marker wrappers before artifact staging",
    "marker occurrence count depends on PowerShell method overload resolution"
  ],
  "regression_check": {
    "type": "validation_command",
    "command": "Inspect exact ZIP payload and verify literal begin/end counts are one; verify INSTALL.ps1 uses Regex.Matches with Regex.Escape and does not contain .Split($BeginMarker) or .Split($EndMarker).",
    "expected_marker": "WEB_AI_MARKER_CONTRACT: PASS",
    "required_before_freeze": true
  },
  "validation_command_summary": "Exact corrected ZIP inspection proves exactly one begin marker, exactly one end marker, valid JSON between markers, required Web AI fields present, and literal escaped-regex counting in the installer.",
  "validation_evidence": [
    "Original payload exact inspection found one begin marker.",
    "Original payload exact inspection found one end marker.",
    "Failure was reproduced from the installer guard, not from malformed planning JSON.",
    "Corrected installer uses Regex.Matches with Regex.Escape.",
    "Corrected installer verifies the installed payload exactly matches the packaged payload.",
    "Corrected ZIP payload parses as valid JSON and retains the original source hash and base plan hash."
  ],
  "redaction": {
    "applied": true,
    "export_safe": true,
    "rules": [
      "No credentials or secrets included.",
      "No patient or personal data included.",
      "Project paths are normalized to technical context.",
      "No private repository history is included."
    ]
  },
  "install_command_summary": "The corrected external Web AI import ZIP writes only the pending imported-plan artifact to the Planner-owned external import inbox.",
  "notes": "Permanent memorization remains pending human review and Memorize Error."
}
KANDA_ERROR_LESSON_JSON_END
'@

    $UTF8_NO_BOM = New-Object System.Text.UTF8Encoding($false)

    [System.IO.File]::WriteAllText(
        $INTAKE_FILE,
        $LESSON,
        $UTF8_NO_BOM
    )

    $VERIFY = [System.IO.File]::ReadAllText(
        $INTAKE_FILE,
        [System.Text.Encoding]::UTF8
    )

    if (-not $VERIFY.StartsWith("KANDA_ERROR_LESSON_JSON_BEGIN")) {
        throw "Error Memory begin marker missing."
    }

    if (-not $VERIFY.TrimEnd().EndsWith("KANDA_ERROR_LESSON_JSON_END")) {
        throw "Error Memory end marker missing."
    }

    Write-Host ""
    Write-Host "ERROR_MEMORY_INTAKE_STAGED: $INTAKE_FILE"
    Write-Host "ERROR_MEMORY_INTAKE_MARKERS: PASS"
    Write-Host "LESSONS_WRITE: NOT_PERFORMED"
    Write-Host "HUMAN_REVIEW_REQUIRED: Memorize Error"
}
catch {
    $ErrorMemoryFailed = $true

    Write-Host ""
    Write-Host "ERROR MEMORY STAGING ERROR"
    Write-Host $_.Exception.Message
}

Write-Host ""
Read-Host "Press Enter to clear terminal"
Clear-Host

Then:

Error Memory
→ AI-assisted error lesson intake
→ review
→ Memorize Error

For this specific artifact, do not freeze anything based on the failed install attempt. First install the corrected ZIP, press Receive Planning from Web AI, verify that KANDA validates the proposal, and load it as Imported Web AI Version. The imported planning version should only be treated as accepted evidence after that review/load step.

create the freeze

you said "I found a bounded Web AI improvement that is stronger than simply copying the Heuristic or the unsuccessful Local AI tournament result."
so  create a prompt, to be in prompt library, and in router bridge, that show to "on line"  AI how use that improvement, how improve code received from  button "Copy Compreehsive Planning for web AI" ,  how create the zip correctly , how create install code ,  validate code and freeze  code for the web AI version of refator a large module, be installed  in tab "Large file Refactor  Planner", then create a button "AI refactor Version how to" (orange bold) and insert it after button "Review Refine Plan with Local AI" in tab  Plan Action. also check if content of "Copy Compreehsive Planning for web AI"  needs improvement. go

I’ll add this as a governed, retrievable workflow rather than only a GUI hint. I’m tracing three ownership paths first: the Prompt Library canon location, Router Bridge intent/routing rules, and the Planner GUI/Web-AI exchange code that builds the copied package and Plan & Actions buttons.

The ownership audit is clear now: the new specialist prompt belongs in Folder 06 (refactor and architecture hardening) because its primary purpose is how external Web AI should improve a large-module plan; delivery/freeze rules will be companion requirements from Folder 05, not duplicated as a second canon.

I’m also treating the new GUI button as a prompt retrieval/copy action: it will read the canonical prompt-library file from the KANDA tool root, copy it to the clipboard, and show a concise confirmation in the Planner panel. This keeps the button tied to the real prompt source instead of embedding a stale duplicate string in GUI code.

Pasted text.txt
Document
wait a minute , we already have this , perhaps you just update it or make another version to fit this task//

Yes—good catch. The existing Large Module Creation and Refactor Protocol v7.2 already owns the core refactor canon, so creating a second competing “how to refactor large modules” prompt would be the wrong architecture. the best fit is:

    a v7.3 extension inside the existing canon, or

    a specialized companion prompt that the canon/router explicitly delegates to for the external Web AI planning/import workflow.

My bias is toward a companion prompt plus a small v7.3 delegation section, because the Web AI ZIP/install/receive/freeze workflow is specialized and would bloat the core canon if embedded in full.

Yes. After reading the existing Large Module Creation and Refactor Protocol v7.2, I agree that we should not create a second general large-module refactor canon. The existing protocol already owns the core refactor architecture: audit, decomposition, AST evidence, multi-island rules, helper granularity, delivery, validation, rollback, and freeze.

The better architecture is:

Large Module Creation and Refactor Protocol v7.3
        │
        │ core owner
        │
        ├── Heuristic Planner workflow
        ├── Local AI Planner workflow
        │
        └── delegates specialized external workflow to:
                ↓
        Web AI Large Module Refactor Exchange Protocol

My recommendation
1. Update the existing canon from v7.2 → v7.3

Do not duplicate its existing rules.

Add a focused section such as:

## External Web AI Refactor Version Workflow

This section should define only the relationship:

Large Module Refactor Protocol
        ↓
Planner generates native plan:
Heuristic or Local AI
        ↓
Copy Comprehensive Planning for Web AI
        ↓
External Web AI uses specialist companion protocol
        ↓
returns installable Web AI Version ZIP
        ↓
install external artifact
        ↓
Receive Planning from Web AI
        ↓
deterministic validation
        ↓
human review
        ↓
Load as Imported Web AI Version
        ↓
optional freeze evidence
        ↓
Workbench handoff only after selected-version approval

The existing v7.2 protocol already says the AST report is evidence rather than authority, planning must preserve the public API, helper granularity should be practical, install/validate/freeze must be governed, and delivery artifacts are not runtime source architecture. Those rules should stay canonical rather than be rewritten in another prompt.
2. Create one specialized companion prompt

I would create:

ACTIVE_PROMPTS/
06_refactor_and_architecture_hardening/
web_ai_large_module_refactor_exchange_protocol.md

Suggested title:

# Web AI Large Module Refactor Exchange and Import Protocol

Its purpose is narrower:

    Given the package copied by Copy Comprehensive Planning for Web AI, analyze the native Heuristic or Local AI plan, seek bounded architectural improvements, validate the proposal logically, and return a KANDA-compatible installable Web AI Version ZIP plus install, validation, and freeze-evidence instructions.

This companion should contain the parts that do not belong in the general refactor canon:

1. How to read the Comprehensive Planning package
2. How to compare native Heuristic / Local AI plan evidence
3. How to identify bounded improvements
4. How to avoid simply copying the native plan
5. How to respect known-symbol / known-module constraints
6. How to calculate whether the proposed plan is plausibly better
7. Exact Web AI response marker contract
8. Exact response JSON schema
9. Exact ZIP structure
10. Correct PowerShell installer rules
11. Marker counting rules
12. External import inbox destination
13. Validation contract
14. Freeze-evidence bundle contract
15. No-Leak and Box Shielding constraints
16. How to handle no-improvement cases honestly

That is sufficiently specialized to deserve a companion prompt.
What the button should copy

The proposed orange bold button:

AI Refactor Version How To

should copy the specialist companion prompt, not the entire large-module v7.3 canon.

Position:

Analyze File
Generate Split Plan
Generate Docstring Plan
Review & Refine Plan with Local AI

[ AI Refactor Version How To ]    ← orange + bold

Show Planning Summary
Copy Planning Summary
Copy Comprehensive Planning for Web AI
Receive Planning from Web AI

My preferred exact label is:

AI Refactor Version How To

or, slightly clearer:

Web AI Refactor Version How To

I prefer the second because it immediately distinguishes it from Local AI.
Router Bridge model

The Router Bridge should not duplicate the whole specialist prompt.

It should contain a thin pointer:

Trigger:
- user asks how external Web AI should improve a Large File Refactor Planner plan;
- user supplies Copy Comprehensive Planning for Web AI output;
- user requests a Web AI refactor version;
- user asks Web AI to create an installable imported planning ZIP;
- user requests install, validate, or freeze evidence for an Imported Web AI Version.

Route:
1. Large Module Creation and Refactor Protocol v7.3
2. Web AI Large Module Refactor Exchange and Import Protocol
3. Router Bridge Patch Delivery Contract when a ZIP is emitted
4. Pre-output Contract Gates
5. Freeze Code Intake and Form Protocol when freeze evidence is emitted

This follows the existing prompt-library design principle that router files should contain minimal routing pointers rather than copies of specialist prompts.
Copy Comprehensive Planning for Web AI does need improvement

Yes. Based on the workflow we just exercised, I would improve it.

Currently, the online AI receives planning evidence, but the external workflow needs to be more explicit about what it is expected to do.

The copied package should contain these sections in this order:

KANDA LARGE FILE REFACTOR — WEB AI EXCHANGE PACKAGE

1. TASK
2. ACTIVE NATIVE BASE VERSION
3. SOURCE IDENTITY
4. SOURCE HASH
5. BASE PLAN HASH
6. PUBLIC API CONTRACT
7. CURRENT PLAN
8. HEURISTIC CANDIDATES
9. RESPONSIBILITY EVIDENCE
10. TOPOLOGY EVIDENCE
11. GIT HISTORY EVIDENCE + CONFIDENCE
12. QUALITY SCORES
13. LOCAL AI TOURNAMENT RESULT, when present
14. KNOWN MODULES
15. KNOWN SYMBOLS
16. ATOMIC CLUSTERS / MUST-LINK GROUPS
17. ALLOWED ACTIONS
18. FORBIDDEN ACTIONS
19. IMPROVEMENT GOAL
20. REQUIRED RESPONSE SCHEMA
21. REQUIRED ZIP CONTRACT
22. INSTALLER CONTRACT
23. VALIDATION CONTRACT
24. FREEZE-EVIDENCE CONTRACT

Most important addition: explicit improvement objective

The package should tell the external AI:

Do not merely reproduce the native plan.

First evaluate whether a bounded architecture improvement exists.

Prefer improvements that:
- increase responsibility cohesion;
- reduce mixed-responsibility concentration;
- improve size balance without creating micro-files;
- reduce avoidable facade back-reference pressure;
- preserve helper-cycle safety;
- preserve atomic clusters;
- preserve public-facade ownership;
- beat the native baseline when evaluated by the supplied quality evidence.

If no bounded improvement is defensible, return a truthful no-improvement verdict.

That instruction is important because our useful Web proposal came from noticing:

122 / 452

and testing a bounded reassignment:

_related_tests_to_run
    →
path_resolution

which created:

145 / 429

with better deterministic comparison evidence.

The online AI should be explicitly encouraged to search for this type of small bounded improvement, rather than either:

copy native plan unchanged

or:

invent a completely new architecture

Very important ZIP-generation lesson

The specialist prompt must explicitly include the installer lesson we just learned:

DO NOT use:

$PayloadText.Split($BeginMarker)

to count literal marker occurrences.

Use:

[regex]::Matches(
    $PayloadText,
    [regex]::Escape($BeginMarker)
).Count

and equivalent logic for the end marker.

The ZIP contract should require:

exactly one begin marker
exactly one end marker
valid JSON between markers
source hash match
base plan hash match
known-symbol actions only
known-module actions only
artifact copy equality after install

This belongs in the specialist Web AI protocol because it is an external artifact-generation rule, not a general large-module refactor rule.
Final architecture I recommend

CORE CANON
large_module_refactor_protocol.md
Version 7.3

Owns:
- audit
- decomposition
- module law
- Heuristic foundation
- Local AI relationship
- external Web AI delegation
- validation principles
- Workbench boundary

SPECIALIST COMPANION
web_ai_large_module_refactor_exchange_protocol.md

Owns:
- online AI reasoning procedure
- bounded improvement search
- response schema
- ZIP generation
- correct installer
- installed artifact inbox
- validation
- imported-version review
- freeze-evidence packaging

ROUTER BRIDGE
thin route only

External Web AI refactor intent
    →
large_module_refactor_protocol v7.3
    +
web_ai_large_module_refactor_exchange_protocol
    +
delivery/freeze companion prompts as needed

PLANNER GUI

Review & Refine Plan with Local AI

[ Web AI Refactor Version How To ]   orange bold

...

Copy Comprehensive Planning for Web AI
Receive Planning from Web AI

This is the architecture I would implement next. It avoids duplicating the existing v7.2 canon while giving online AI a precise, reusable protocol for producing a genuinely improved, correctly packaged, installable, validatable, and freeze-preparable Imported Web AI Version.

do it , an  create the button I asked as a wrapper for that prompt 

I

IMPLEMENTATION GATE

Task domain: Prompt Library + Router Bridge + Large File Refactor Planner GUI/Web-AI exchange
Active boxes: Prompt Library routing canon; Large File Refactor Planner
Allowed changes: existing large-module canon v7.3 delegation, new specialist companion prompt + metadata, router registration, Planner button wrapper, Web-AI export guidance improvements, focused validators
Out of scope: Local AI algorithm, Heuristic scoring, Workbench apply/rollback, selected-project source mutation
Cross-box touches: Prompt Library ↔ Planner GUI only through canonical prompt retrieval by path; no embedded duplicate prompt body
Public contracts preserved: existing Heuristic/Local AI/Imported Web AI version state and import schema remain unchanged
Line-count risk: touched Python modules remain below 500 lines; new helper kept focused and small as a stable prompt-retrieval seam
GUI-resolution risk: one additional button in the existing horizontal action row; no fixed window sizing or new dialog geometry
May implement: YES

NO-LEAK CHECK

Canonical source: prompt-library Markdown + metadata and Planner source
Generated artifacts: patch ZIP, validation output, freeze hint only
Blocked writes: selected-project source, Workbench state, canonical freeze memory, Error Memory Lessons
Safe next action: implement the v7.3 delegation + specialist prompt + router entries + thin GUI wrapper + richer exchange package contract.

The implementation is now structurally in place. The existing v7.2 canon is upgraded to v7.3 with a delegation section; the new specialist companion is registered as KPR-06-001; the Router Bridge and routing indexes recognize the external Web AI flow; and the orange bold AI Refactor Version How To button copies the canonical prompt instead of embedding a duplicate.

I’m validating the richer Comprehensive Planning package now, especially that it exposes known helpers/symbols, explicit improvement objectives, governed ZIP contents, correct PowerShell marker counting, validation requirements, and freeze-evidence boundaries.

Implemented.
Delivered behavior
1. Existing large-module canon updated, not duplicated

The existing:

large_module_refactor_protocol.md

is upgraded:

v7.2 → v7.3

with a new delegation section:

External Web AI Planner Version Delegation v7.3

The ownership model is now:

Large Module Refactor Protocol v7.3
        │
        ├── core module-size and architecture law
        ├── Heuristic workflow
        ├── Local AI workflow
        ├── validation and Workbench boundaries
        │
        └── delegates external online AI workflow
                ↓
KPR-06-001
Web AI Large Module Refactor Exchange and Import Protocol

2. New specialist Prompt Library prompt

Created:

KPR-06-001

Prompt ID:

web_ai_large_module_refactor_exchange_protocol

Canonical path:

kanda_prompt_workspace/
prompt_library/
ACTIVE_PROMPTS/
06_refactor_and_architecture_hardening/
web_ai_large_module_refactor_exchange_protocol.md

The prompt teaches online AI how to:

read the Comprehensive Planning package
        ↓
understand the native Heuristic or Local AI base
        ↓
search for bounded improvements
        ↓
avoid blindly copying the native plan
        ↓
avoid unnecessary full redesign
        ↓
compare:
    responsibility cohesion
    mixed responsibility
    helper balance
    dependency topology
    facade back-reference pressure
    atomic clusters
    Git evidence confidence
        ↓
return bounded actions only
        ↓
create correct Imported Web AI Version ZIP
        ↓
create INSTALL.ps1
VALIDATE.ps1
FREEZE.ps1
KANDA_FREEZE_HINT.json
bundle_manifest.json
payload artifact
        ↓
install
        ↓
Receive Planning from Web AI
        ↓
review
        ↓
Load as Imported Web AI Version
        ↓
freeze evidence merge
        ↓
Preview
        ↓
Confirm and Write

3. New requested button

Added in Plan & Actions, immediately after:

Review & Refine Plan with Local AI

The order is now:

Analyze File

Generate Split Plan

Generate Docstring Plan

Review & Refine Plan with Local AI

[ AI Refactor Version How To ]

...

The new button is:

AI Refactor Version How To

with:

orange background
bold text

The button is a thin wrapper.

It does not contain a copied prompt body inside GUI source.

Its flow is:

click button
    ↓
resolve canonical Prompt Library path
    ↓
read KPR-06-001
    ↓
copy exact canonical prompt to clipboard

This prevents the GUI wrapper and Prompt Library source from drifting apart.
4. Router Bridge updated

The Router Bridge now explicitly recognizes:

external Web AI refactor version
online AI improve split plan
Imported Web AI Version
Copy Comprehensive Planning for Web AI
Receive Planning from Web AI
AI Refactor Version How To

and routes to:

large_module_refactor_protocol v7.3
+
KPR-06-001
web_ai_large_module_refactor_exchange_protocol

The registered bridge sequence is:

native Heuristic or Local AI plan
        ↓
Copy Comprehensive Planning for Web AI
        ↓
external Web AI bounded correction
        ↓
governed import ZIP
        ↓
install pending external artifact
        ↓
Receive Planning from Web AI
        ↓
deterministic validation
        ↓
review
        ↓
Load as Imported Web AI Version
        ↓
compare/select version
        ↓
Workbench remains separate

5. Copy Comprehensive Planning for Web AI improved

Yes, I changed its generated package.

It now explicitly provides:

known_helper_modules

known_movable_symbols

improvement_objective

native base identity

source_content_hash

base_plan_hash

native plan

AST analysis

responsibility evidence

topology evidence

Git historical evidence and confidence

Local AI review evidence

architecture questions

Web AI import contract

The copied instructions now explicitly tell online AI:

Do not merely reproduce the native plan.

Search first for a bounded,
evidence-backed architectural improvement.

Prefer small improvements such as:
- one responsibility-outlier reassignment;
- one safe known-helper merge;
- one semantic rename;
- one bounded docstring improvement.

Do not redesign unnecessarily.

If no defensible bounded improvement exists,
return a truthful no-change response.

It also now tells online AI to examine:

responsibility cohesion
mixed-responsibility concentration
helper size balance
dependency topology
facade back-reference pressure
atomic clusters
Git-history confidence

6. Full Web AI ZIP contract included

The copied package and specialist prompt now recommend:

web-ai-version.zip
├── INSTALL.ps1
├── VALIDATE.ps1
├── FREEZE.ps1
├── KANDA_FREEZE_HINT.json
├── bundle_manifest.json
└── pending_imported_web_ai_plan.txt

The installer contract explicitly says:

write only:

<drive>\
<project>_show_project_to_AI\
project_large_file_refactor_planner_web_ai_import\
pending_imported_web_ai_plan.txt

and never:

KANDA Python source
selected-project source
Workbench state
freeze memory
Error Memory Lessons

7. Marker-count bug prevention included

The specialist prompt now explicitly prohibits the bug we encountered:

$PayloadText.Split($BeginMarker)

for literal marker counting.

It teaches the correct method:

$BeginCount = [regex]::Matches(
    $PayloadText,
    [regex]::Escape($BeginMarker)
).Count

$EndCount = [regex]::Matches(
    $PayloadText,
    [regex]::Escape($EndMarker)
).Count

and requires:

BeginCount == 1
EndCount == 1

Patch

SHA-256:

9df31447640fa56021c45d32bd749d5f297e6dbf53affeb96eb05b1cdb7401fd

Feature ID:

large-file-refactor-planner-web-ai-howto-prompt-button-v1

Exact ZIP validation

The exact delivered ZIP passed:

LARGE_MODULE_CANON: V7.3_EXTERNAL_WEB_AI_DELEGATION

SPECIALIST_PROMPT:
KPR-06-001_ROUTED_COMPANION

ROUTER_BRIDGE:
EXTERNAL_WEB_AI_IMPORT_FLOW_REGISTERED

GUI_BUTTON:
AI_REFACTOR_VERSION_HOW_TO_ORANGE_BOLD

GUI_WRAPPER:
CANONICAL_PROMPT_READ_NO_EMBEDDED_DUPLICATE

COMPREHENSIVE_EXPORT:
IMPROVEMENT_OBJECTIVE_KNOWN_OBJECTS_DELIVERY_GATES

WEB_AI_BUNDLE_GUIDANCE:
INSTALL_VALIDATE_FREEZE_HINT_MANIFEST_PAYLOAD

POWERSHELL_MARKER_RULE:
REGEX_MATCHES_REGEX_ESCAPE

WORKBENCH_OWNERSHIP: UNCHANGED
BOX_SHIELD: PASS
NO_LEAK_LOGIC: PASS
MODULE_SIZE_GATE: PASS

VALIDATION OK:
large-file-refactor-planner-web-ai-howto-prompt-button-v1

STATUS: IN_SYNC
ZIP CONTRACT: PASS

All existing Planner regression validators also remained passing:

Step 1: PASS
Step 2: PASS
Step 3: PASS
Step 4: PASS
Step 5: PASS
Step 6: PASS
Quality Hardening: PASS

Archive hygiene:

PAYLOAD_PYTHON_COMPILE: PASS
EXACT_ZIP_CACHE_LEAKAGE: NONE
ZIP CONTRACT: PASS

One limitation: PySide6 visual interaction was not available in the sandbox. Button placement, ordering, styling, callback wiring, canonical-path resolution, and clipboard behavior were source-validated; the final visual click test should be done after restarting KANDA.
1. Install

Place the ZIP at:

E:\kanda_large_file_refactor_planner_web_ai_howto_prompt_button_v1_patch.zip

Run:

$ErrorActionPreference = "Stop"
$InstallFailed = $false

try {
    $PROJECT_ROOT = "E:\kanda_reasoner"
    $FEATURE_ID = "large-file-refactor-planner-web-ai-howto-prompt-button-v1"
    $PATCH_NAME = "kanda_large_file_refactor_planner_web_ai_howto_prompt_button_v1_patch.zip"

    $PROJECT_ROOT = [System.IO.Path]::GetFullPath($PROJECT_ROOT)
    $PROJECT_NAME = Split-Path -Leaf $PROJECT_ROOT
    $DRIVE_ROOT = [System.IO.Path]::GetPathRoot($PROJECT_ROOT)

    $WORK_DIR = [System.IO.Path]::Combine(
        $DRIVE_ROOT,
        $PROJECT_NAME + "_delete_after_daily_work"
    )

    $ROOT_PATCH_ZIP = [System.IO.Path]::Combine(
        $DRIVE_ROOT,
        $PATCH_NAME
    )

    $WORK_PATCH_ZIP = Join-Path `
        $WORK_DIR `
        $PATCH_NAME

    $EXTRACT_ROOT = Join-Path `
        $WORK_DIR `
        ($FEATURE_ID + "_extract")

    if (-not (Test-Path $PROJECT_ROOT)) {
        throw "Project root not found: $PROJECT_ROOT"
    }

    if (-not (Test-Path $WORK_DIR)) {
        New-Item `
            -ItemType Directory `
            -Path $WORK_DIR `
            -Force | Out-Null
    }

    if (Test-Path $ROOT_PATCH_ZIP) {
        Copy-Item `
            -Path $ROOT_PATCH_ZIP `
            -Destination $WORK_PATCH_ZIP `
            -Force

        if (-not (Test-Path $WORK_PATCH_ZIP)) {
            throw "Patch ZIP staging failed: $WORK_PATCH_ZIP"
        }

        Remove-Item `
            -Path $ROOT_PATCH_ZIP `
            -Force
    }

    if (-not (Test-Path $WORK_PATCH_ZIP)) {
        throw "zip is not in root of drive:\ where project is"
    }

    if (Test-Path $EXTRACT_ROOT) {
        Remove-Item `
            -Path $EXTRACT_ROOT `
            -Recurse `
            -Force
    }

    New-Item `
        -ItemType Directory `
        -Path $EXTRACT_ROOT `
        -Force | Out-Null

    Expand-Archive `
        -Path $WORK_PATCH_ZIP `
        -DestinationPath $EXTRACT_ROOT `
        -Force

    $INSTALL_SCRIPT = Join-Path `
        $EXTRACT_ROOT `
        "INSTALL.ps1"

    if (-not (Test-Path $INSTALL_SCRIPT)) {
        throw "INSTALL.ps1 not found: $INSTALL_SCRIPT"
    }

    powershell `
        -NoProfile `
        -ExecutionPolicy Bypass `
        -File $INSTALL_SCRIPT `
        -ProjectRoot $PROJECT_ROOT `
        -SkipFooter

    if ($LASTEXITCODE -ne 0) {
        throw "INSTALL.ps1 returned a nonzero exit code."
    }
}
catch {
    $InstallFailed = $true

    Write-Host ""
    Write-Host "INSTALL ERROR"
    Write-Host $_.Exception.Message

    if ($_.ScriptStackTrace) {
        Write-Host $_.ScriptStackTrace
    }
}

if (-not $InstallFailed) {
    Write-Host ""
    Write-Host "INSTALL OK"
    Write-Host "Restart KANDA before GUI testing."
}

if ($InstallFailed) {
    Write-Host ""
    Read-Host "Press Enter to clear terminal"
    Read-Host "Press Enter again to clear"
    Clear-Host
}

Restart KANDA.
2. Validate

$ErrorActionPreference = "Stop"
$ValidationFailed = $false

try {
    $PROJECT_ROOT = "E:\kanda_reasoner"
    $FEATURE_ID = "large-file-refactor-planner-web-ai-howto-prompt-button-v1"

    $PROJECT_ROOT = [System.IO.Path]::GetFullPath($PROJECT_ROOT)
    $PROJECT_NAME = Split-Path -Leaf $PROJECT_ROOT
    $DRIVE_ROOT = [System.IO.Path]::GetPathRoot($PROJECT_ROOT)

    $WORK_DIR = [System.IO.Path]::Combine(
        $DRIVE_ROOT,
        $PROJECT_NAME + "_delete_after_daily_work"
    )

    $EXTRACT_ROOT = Join-Path `
        $WORK_DIR `
        ($FEATURE_ID + "_extract")

    $VALIDATE_SCRIPT = Join-Path `
        $EXTRACT_ROOT `
        "VALIDATE.ps1"

    if (-not (Test-Path $VALIDATE_SCRIPT)) {
        throw "VALIDATE.ps1 not found: $VALIDATE_SCRIPT"
    }

    powershell `
        -NoProfile `
        -ExecutionPolicy Bypass `
        -File $VALIDATE_SCRIPT `
        -ProjectRoot $PROJECT_ROOT `
        -SkipFooter

    if ($LASTEXITCODE -ne 0) {
        throw "Validation returned a nonzero exit code."
    }
}
catch {
    $ValidationFailed = $true

    Write-Host ""
    Write-Host "VALIDATION ERROR"
    Write-Host $_.Exception.Message

    if ($_.ScriptStackTrace) {
        Write-Host $_.ScriptStackTrace
    }
}

Write-Host ""
Read-Host "Press Enter to clear terminal"
Read-Host "Press Enter again to clear"
Clear-Host

Expected core markers:

LARGE_MODULE_CANON: V7.3_EXTERNAL_WEB_AI_DELEGATION
SPECIALIST_PROMPT: KPR-06-001_ROUTED_COMPANION
ROUTER_BRIDGE: EXTERNAL_WEB_AI_IMPORT_FLOW_REGISTERED
GUI_BUTTON: AI_REFACTOR_VERSION_HOW_TO_ORANGE_BOLD
GUI_WRAPPER: CANONICAL_PROMPT_READ_NO_EMBEDDED_DUPLICATE
COMPREHENSIVE_EXPORT: IMPROVEMENT_OBJECTIVE_KNOWN_OBJECTS_DELIVERY_GATES
WEB_AI_BUNDLE_GUIDANCE: INSTALL_VALIDATE_FREEZE_HINT_MANIFEST_PAYLOAD
POWERSHELL_MARKER_RULE: REGEX_MATCHES_REGEX_ESCAPE
WORKBENCH_OWNERSHIP: UNCHANGED
BOX_SHIELD: PASS
NO_LEAK_LOGIC: PASS
MODULE_SIZE_GATE: PASS
VALIDATION OK: large-file-refactor-planner-web-ai-howto-prompt-button-v1
STATUS: IN_SYNC
ZIP CONTRACT: PASS
VALIDATION COMMAND COMPLETE

3. Local GUI check

After restarting KANDA:

Architecture Review
→ Large File Refactor Planner
→ Plan & Actions

Check the order:

Review & Refine Plan with Local AI

AI Refactor Version How To

The second button should be visibly:

orange
bold

Click it and paste into a text editor.

The clipboard should begin with:

# Web AI Large Module Refactor Exchange and Import Protocol

Prompt code: KPR-06-001
Prompt id: web_ai_large_module_refactor_exchange_protocol

Then test:

Generate Heuristic or Local AI plan
→ Copy Comprehensive Planning for Web AI

The copied package should now contain:

known_helper_modules
known_movable_symbols
improvement_objective
required_bundle_files
validation_requirements
freeze_evidence_requirements

4. Freeze

After validation and local GUI checks succeed:

$ErrorActionPreference = "Stop"
$FreezeFailed = $false

try {
    $PROJECT_ROOT = "E:\kanda_reasoner"
    $FEATURE_ID = "large-file-refactor-planner-web-ai-howto-prompt-button-v1"

    $PROJECT_ROOT = [System.IO.Path]::GetFullPath($PROJECT_ROOT)
    $PROJECT_NAME = Split-Path -Leaf $PROJECT_ROOT
    $DRIVE_ROOT = [System.IO.Path]::GetPathRoot($PROJECT_ROOT)

    $WORK_DIR = [System.IO.Path]::Combine(
        $DRIVE_ROOT,
        $PROJECT_NAME + "_delete_after_daily_work"
    )

    $EXTRACT_ROOT = Join-Path `
        $WORK_DIR `
        ($FEATURE_ID + "_extract")

    $FREEZE_SCRIPT = Join-Path `
        $EXTRACT_ROOT `
        "FREEZE.ps1"

    if (-not (Test-Path $FREEZE_SCRIPT)) {
        throw "FREEZE.ps1 not found: $FREEZE_SCRIPT"
    }

    powershell `
        -NoProfile `
        -ExecutionPolicy Bypass `
        -File $FREEZE_SCRIPT `
        -ProjectRoot $PROJECT_ROOT `
        -SkipFooter

    if ($LASTEXITCODE -ne 0) {
        throw "Freeze evidence merge returned a nonzero exit code."
    }
}
catch {
    $FreezeFailed = $true

    Write-Host ""
    Write-Host "FREEZE ERROR"
    Write-Host $_.Exception.Message

    if ($_.ScriptStackTrace) {
        Write-Host $_.ScriptStackTrace
    }
}

if (-not $FreezeFailed) {
    Write-Host ""
    Write-Host "FREEZE EVIDENCE MERGE OK"
}

if ($FreezeFailed) {
    Write-Host ""
    Write-Host "FREEZE FAILED"
}

Write-Host ""
Read-Host "Press Enter to clear terminal"
Read-Host "Press Enter again to clear"
Clear-Host

Expected:

FREEZE_HINT_EVIDENCE_MERGE_OK:
large-file-refactor-planner-web-ai-howto-prompt-button-v1

FREEZE HINT MERGE OK:
large-file-refactor-planner-web-ai-howto-prompt-button-v1

STATUS: IN_SYNC

Then complete:

Freeze Feature After Update
→ Preview
→ Confirm and Write

The result is now a single coherent workflow: the existing large-module canon remains the owner, the online-AI exchange has a specialized reusable companion prompt, the Router Bridge knows when to load it, the Planner exposes it through the requested orange bold wrapper button, and the Comprehensive Planning export now gives online AI enough explicit guidance to search for real bounded improvement and return a correctly governed Imported Web AI Version bundle.

now ""Large File Refactor Workbench" go until balidate real preview but do not activate  5. re flight
prepare preflight backup readiness, build ssource apply payload,  Apply source changes , rollback las apply ru optional behaviour validation, and there is not a button refactor module = revieu "Large File Refactot Workbench" tab, search web as before for help in how implement the refactor to the end , using our logic and prepare an audit for how correct blocked code and finish implementation to refator module 

I’ll audit the Workbench as a completion pipeline, not just a GUI. I’ll compare its current source/state machine with mature refactoring workflows from Python tooling, IDE/refactor engines, and practitioner guidance, then map every blocked or missing stage from validated preview → preflight → backup → payload → apply → post-apply validation → rollback → optional behavior validation → final “Refactor Module” completion action.

The source audit has already found an important mismatch: workbench_gui.py contains handlers and enablement logic for preflight, payload build, apply, rollback, and behavior validation, but the source archive does not contain the imported workbench_preflight_backup_* modules. That means the Workbench is not merely “missing one final button”; its completion train has a source-integrity gap between GUI wiring and owned implementation modules.

I’m tracing the remaining apply/rollback validators and the tutorial contract now, because the repair should restore a coherent end-to-end state machine rather than simply force-enable disabled buttons.

A second architectural issue is emerging from the cross-tab audit: the Workbench snapshot boundary is good in principle, but the handoff still depends on the Planner’s exported “current plan” pointer. I’m verifying that Imported Web AI / Local AI version selection updates that public handoff correctly; otherwise Workbench could faithfully snapshot the wrong version even while the Planner panel displays another one.
Workbench completion audit
Executive verdict

The Large File Refactor Workbench should not be repaired by simply force-enabling Stage 5 buttons.

The audit shows that the Workbench has a good first half:

Planner selected version
        ↓
immutable Workbench snapshot
        ↓
dependency readiness
        ↓
real preview generation
        ↓
real preview structural validation

but its second half is not yet a single coherent completion pipeline.

The main finding is:

    The Workbench already contains many pieces needed to finish a real refactor, but they are fragmented across overlapping pipelines, partially disconnected from the GUI, and missing several safety transitions required before source mutation.

The correct repair is therefore:

do not bypass blocked buttons
do not create a third apply engine
do not directly connect Validate Preview → Apply Source

instead:

restore one canonical end-to-end transaction pipeline

The existing Large Module Refactor Protocol already requires dependency-direction analysis, public API preservation, behavioral validation, rollback planning, fragmentation audit, and local validation before freeze. The Workbench completion pipeline should enforce those rules rather than merely expose buttons.
1. Current Workbench audit
Current visible pipeline

The effective GUI architecture is approximately:
Stage	Current state	Audit result
1. Plan Intake	implemented	PASS
2. Dependency Readiness	implemented	PASS
3. Generate Real Preview	implemented	PASS, with runtime-boundary caveat
4. Validate Real Preview	implemented	PARTIAL PASS
5. Preflight Backup Readiness	GUI logic exists	SOURCE-INTEGRITY GAP
Build Source Apply Payload	implemented	BLOCKED downstream of preflight
Apply Source Changes	implemented	NEEDS transaction hardening
Post-Apply Validation	implemented	PARTIAL
Rollback Last Apply	implemented	GUI gating defect
Optional Behavior Validation	implemented	PARTIAL / weak integration
Visual Diff	implementation exists	NOT WIRED INTO MAIN FLOW
Import Rewrite Apply	implementation exists	NOT WIRED INTO MAIN FLOW
Refactor Module primary action	absent	MISSING
2. Important: the Planner → Workbench handoff is fundamentally sound

I checked the version-selection path carefully.

The current architecture does preserve the intended isolation model:

Planner
    Heuristic
    Local AI
    Imported Web AI Version
        ↓
selected version
        ↓
active public plan pointer
        ↓
explicit:
Load Latest Planner Plan
        ↓
deep-copied Workbench snapshot

The Workbench then owns its downstream execution state independently.

That means the repair should preserve this architecture.

I do not recommend merging Planner and Workbench state.

The correct ownership remains:

PLANNER
analysis
candidate architecture
version comparison
docstring planning
AI planning

        ↓ explicit handoff

WORKBENCH
readiness
preview
validation
preflight
backup
shadow apply
real apply
post-apply validation
behavior validation
rollback
completion

3. Why Stage 5 apparently does not activate

This is important.

In the audited GUI logic, Preflight is enabled after structural validation when:

status.startswith("passed")

The real preview structural validator can return:

passed_with_warnings

which should satisfy that predicate.

Therefore, based on the source logic alone:

    A successfully validated real preview should allow the Preflight stage to become available.

But in the cumulative source reconstruction I audited, several imported preflight modules are missing:

source_apply_preflight_backup_contract.py

workbench_preflight_backup_readiness.py

workbench_preflight_backup_formatting.py

The cumulative package import also fails in that reconstructed tree because:

source_apply_preflight_backup_contract

cannot be imported.

There is an important caveat: your actual runtime clearly opens the Workbench tab, so your local tree may differ from the source archive I audited. Therefore I would not claim that these files are definitely missing from your installed machine.

But the combination of:

GUI handlers present
        +
preflight imports unresolved in audited source
        +
user-observed non-activation

is strong evidence that the first repair must be a source/runtime synchronization and preflight ownership audit, not a force-enable patch.

The UI also needs explicit gate diagnostics.

Instead of:

Preflight button disabled

the Workbench should show:

PREFLIGHT BLOCKED

Reason:
REAL_PREVIEW_STRUCTURAL_VALIDATION_NOT_ACCEPTED

or

PREFLIGHT_OWNER_MODULE_UNAVAILABLE

or

PREVIEW_HASH_CHANGED

or

SOURCE_DRIFT_DETECTED

A disabled button without a machine-readable blocking reason is not adequate for a governed source-mutation pipeline.
4. Critical finding: two overlapping apply architectures

The current package contains two conceptually overlapping source-apply families.
Older governed apply family

Approximately:

final_guarded_source_apply_planning
source_apply_dry_run_validator
source_apply_preflight_backup_contract
guarded_source_apply_executor
post_apply_validation
source_apply_rollback_recovery

Newer Workbench direct apply family

Approximately:

workbench_preflight_backup_readiness
workbench_source_payload_builder
workbench_guarded_source_apply
workbench_post_apply_validator
workbench_rollback_executor
workbench_behavior_validation

This is dangerous architecture.

The problem is not necessarily that either implementation is individually wrong.

The problem is:

Which one owns:
    backup?
    transaction identity?
    rollback manifest?
    source hashes?
    generated helper deletion?
    post-apply truth?
    final completion?

There should be exactly one active owner.

My recommendation:

    The Workbench pipeline should become the canonical interactive transaction owner, while any older apply modules should either become internal reusable primitives or be explicitly retired from the GUI execution path.

Do not build another Refactor Module executor beside both of them.
5. Critical correctness gap: preview structural validity is not enough

This is, in my judgment, the most important technical finding.

The current Planner can identify:

FACADE_BACK_REFERENCE_RISK
FACADE_BOUNDARY_CYCLE_RISK

and your actual main_helper_mapper.py plan already showed such evidence.

The preview renderer can move a function into a helper while that function still references facade-owned globals, constants, or classes.

The current helper import synthesis can warn about global dependencies, but a warning is not necessarily transformed into a correct import or ownership solution.

Therefore this sequence is possible in principle:

preview generated
        ↓
Python syntax valid
        ↓
AST parses
        ↓
public names appear preserved
        ↓
structural validation passes
        ↓
runtime import or execution later fails

For example:

moved helper function
        ↓
references facade-owned constant
        ↓
helper does not own/import constant correctly
        ↓
runtime NameError

or:

helper imports facade to obtain constant
        ↓
facade imports helper
        ↓
runtime circular initialization problem

This is why the Workbench needs a Shadow Apply Runtime Gate before real mutation.

Python's own tooling separates syntax compilation from runtime import semantics: py_compile and compileall test compilability, while import caches and runtime module loading have separate behavior. A safe pipeline should therefore perform compilation plus real import-smoke tests after creating the projected file layout.
6. The target Workbench state machine

I recommend replacing loose button enablement with one explicit state machine.

NO_PLAN
    ↓
PLAN_SNAPSHOT_READY
    ↓
DEPENDENCY_READY
    ↓
REAL_PREVIEW_READY
    ↓
PREVIEW_STRUCTURAL_PASS
    ↓
PREFLIGHT_READY
    ↓
SHADOW_APPLY_PASS
    ↓
VISUAL_DIFF_REVIEWED
    ↓
SOURCE_PAYLOAD_READY
    ↓
APPLY_ARMED
    ↓
REFACTORING
    ↓
APPLIED
    ↓
POST_APPLY_PASS
    ↓
BEHAVIOR_PASS
or
BEHAVIOR_NOT_RUN_ACCEPTED
    ↓
COMPLETED

Rollback is a parallel capability:

SOURCE_WRITE_STARTED
        ↓
ROLLBACK_AVAILABLE

and should remain available until the transaction is explicitly completed or superseded.
State invalidation

The state machine must also invalidate downstream evidence.

For example:

new Planner plan loaded
        ↓
invalidate:
dependency readiness
preview
preview validation
preflight
shadow validation
payload
apply token

preview regenerated
        ↓
invalidate:
structural validation
preflight
shadow apply
diff review
payload
apply token

source changed externally
        ↓
invalidate:
preflight
backup readiness
shadow validation
payload
apply authorization

This should be centralized rather than duplicated across button handlers.
7. New missing stage: Shadow Apply Validation

This is the most important new stage I recommend.
Current conceptual flow

preview validation
        ↓
preflight
        ↓
payload
        ↓
real source mutation

Recommended flow

preview validation
        ↓
preflight
        ↓
backup readiness
        ↓
build payload
        ↓
SHADOW APPLY
        ↓
runtime validation
        ↓
visual diff review
        ↓
arm real apply
        ↓
Refactor Module

Shadow environment preference
Preferred: Git worktree

When the project is in Git:

temporary worktree
        ↓
apply complete payload there
        ↓
compile
        ↓
import smoke
        ↓
tests
        ↓
diff inspection

Git worktrees are specifically designed to provide additional working trees attached to the same repository, making them suitable for isolated validation without mutating the active working tree.
Fallback: temporary project mirror

When Git worktree is unavailable:

daily-work staging
        ↓
controlled source mirror
        ↓
apply exact payload
        ↓
run same validation

The fallback must preserve project-relative imports and package layout.
8. Visual Diff should become a required Workbench gate

The project already contains visual-diff support, but it is not connected to the main Workbench completion sequence.

I recommend:

Shadow Apply Pass
        ↓
Review Refactor Diff
        ↓
checkbox / explicit confirmation:
Diff Reviewed
        ↓
Apply can become armed

The diff should show:

original module
    ↓ lines removed

new helper modules
    ↓ complete contents

facade imports
    ↓ added/changed imports

public exports
    ↓ any changed __all__

consumer import rewrites
    ↓ when applicable

Mature IDE refactoring tools emphasize previewing affected changes and tracking references during move/rename operations. PyCharm, for example, supports previewing refactoring changes and reference-aware move/rename operations.

KANDA already has a stronger governance model than a typical IDE, so its Workbench should not omit this human review surface.
9. Refactor Module button: recommended semantics

Yes, I agree that the Workbench should have a clear primary action:

REFRACTOR MODULE

But this should not create another execution path.

It should be the human-facing wrapper over the canonical guarded apply transaction.
Recommended layout

Panel 5:

5. Preflight & Refactor

[ Prepare Preflight Backup Readiness ]

[ Run Shadow Apply Validation ]

[ Review Refactor Diff ]

[ Build Source Apply Payload ]

Apply authorization:
[ exact token field ]

[ REFACTOR MODULE ]     ← prominent primary action

[ Rollback Last Refactor ]

The existing technical phrase:

Apply Source Changes

can remain in logs/internal function names, but the main GUI action should use the user's actual intention:

Refactor Module

Enablement

Refactor Module becomes enabled only when:

validated immutable plan snapshot
AND
dependency readiness pass
AND
real preview generated
AND
preview structural pass
AND
preflight backup ready
AND
shadow apply pass
AND
visual diff reviewed
AND
source payload ready
AND
source still matches preflight hash
AND
exact apply token matches

On click:

Refactor Module
        ↓
canonical guarded transaction
        ↓
write source files
        ↓
immediate post-apply validation
        ↓
success:
    behavior validation stage available

failure:
    rollback remains available
    red ROLLBACK RECOMMENDED state

10. High-severity rollback defect

The current GUI enablement logic appears to require:

apply status = applied
AND
post-apply status = post_apply_validated

before enabling rollback.

That is backwards for a recovery tool.

Consider:

source apply succeeds
        ↓
post-apply validation fails
        ↓
this is exactly when rollback may be necessary
        ↓
GUI disables rollback

I classify this as P0 / high severity.

The correct rule is:

if any source mutation occurred
AND rollback manifest is valid
AND rollback has not already completed
        ↓
Rollback must remain available

Post-apply failure should make rollback more visible, not less.

Recommended UI:

POST-APPLY VALIDATION FAILED

[ ROLLBACK RECOMMENDED ]

11. Multi-file transaction hardening

The current apply path uses temporary writes and then individual os.replace operations.

That is good for individual-file replacement safety, but it does not make a multi-file refactor transaction atomic as a whole.

os.replace provides atomic replacement semantics for an individual successful rename/replacement operation where supported, but a loop of several replacements still has a failure window between files. That conclusion is an architectural inference from the API semantics.

Example:

replace facade          PASS
replace helper A        PASS
replace helper B        FAIL

The system is now partially applied.

The solution is not necessarily to chase impossible filesystem-level multi-file atomicity.

Instead create an explicit:

RefactorTransaction

with:

transaction_id
source_snapshot_hashes
backup files
payload hashes
ordered operation list
applied operation index
generated-file list
rollback instructions
post-apply evidence
behavior evidence
completion status

Rope's refactoring model is instructive here: refactoring operations return explicit Change objects, the project applies those changes, and history supports undo/redo of Rope-managed changes. KANDA can use a similar transaction concept while preserving its own stricter validation and freeze rules.
12. Preflight backup design

Preflight should verify and produce:

PREFLIGHT BACKUP READINESS

target source hash: PASS
expected files unchanged: PASS
destination helper collision: NONE
backup directory writable: PASS
backup snapshot created: PASS
backup hashes verified: PASS
rollback manifest prepared: PASS
source payload basis hash: MATCH

Backup copying should preserve file metadata where practical; Python's shutil.copy2 is designed to copy file data plus metadata as far as the platform permits.

I recommend storing backups under:

<project>_delete_after_daily_work/
large_file_refactor_workbench/
transactions/
<TX_ID>/
backup/

not in the active project root.
13. Post-apply validation must be stronger

The current structural post-apply checks are not enough.

Recommended post-apply ladder:
Fast gate

expected files exist
hashes match expected payload
py_compile touched files
compileall affected package
AST parse
public facade import smoke
direct consumer import smoke
dependency-cycle check
git diff --check when Git available

git diff --check can detect whitespace errors and conflict markers in changes, making it useful as a cheap source-integrity gate before completion.
Medium gate

focused characterization tests
focused moved-symbol tests
public API compatibility tests
behavior presets

Pytest supports targeted execution and collection-only discovery, and its exit codes distinguish success, test failure, interruption, collection errors, usage errors, and no-tests-collected conditions. The Workbench should interpret those outcomes explicitly rather than reducing all nonzero statuses to one generic message.
Full gate

At the appropriate phase boundary:

broader project tests
architecture validation
fragmentation audit
workflow validation when relevant

This matches the tiered validation philosophy already present in your Large Module Refactor Protocol.
14. LibCST should be used more deliberately in the final application pipeline

Your protocol already prefers behavior-preserving whole-symbol movement and formatting-preserving edits.

LibCST is well suited to codemod-style transformations because it preserves concrete syntax details and provides codemod composition infrastructure. Its testing support also allows transforms to be verified against source/expected-output fixtures before applying them to real source.

For KANDA, I recommend:

Planner plan
        ↓
Workbench preview transform
        ↓
fixture-backed LibCST transformation
        ↓
shadow apply
        ↓
runtime gates
        ↓
same deterministic transform/payload basis
        ↓
real apply

The key principle is:

    The real apply should not independently reinterpret the plan differently from the preview.

The preview and source payload must share one transformation truth.
15. Import rewrite support needs explicit ownership

The source tree already contains:

workbench_import_rewrite_apply_readiness
workbench_import_rewrite_apply_executor
workbench_import_rewrite_rollback_executor

but they are not integrated into the current primary GUI path.

The current large-module protocol says first-pass consumers should normally remain on the public facade path, which is correct.

Therefore the Workbench should use this policy:

DEFAULT
preserve existing consumer imports through facade

OPTIONAL EXPLICIT MIGRATION
only when approved plan includes import migration

then:
import rewrite readiness
→ shadow rewrite
→ import smoke
→ diff review
→ apply as part of same transaction
→ rollback as part of same transaction

Import rewrites must not be an independent transaction after source splitting, because that creates an intermediate broken state.
16. Behavior Validation integration

The existing behavior validation code has good safety properties:

allowlisted commands
no arbitrary shell
timeout
exit-status validation

but the Workbench GUI should integrate existing behavior-test presets and make their provenance visible.

Recommended:

Behavior Validation

Preset:
○ Focused tests inferred from target
○ Related tests from Planner evidence
○ Custom approved command

Command:
python -m pytest ...

[ Collect Tests ]
[ Run Behavior Validation ]

Before running:

pytest --collect-only

can prove that the intended tests actually exist and collect successfully.

A green command that accidentally ran zero tests should not be mistaken for behavioral proof.
17. Proposed repair train

I recommend six controlled patches.
Patch 1 — Workbench Source Integrity and Preflight Restoration

Purpose:

restore the currently broken/misaligned Stage 5 ownership seam

Work:

audit exact local files
restore or reconcile:
    source_apply_preflight_backup_contract
    workbench_preflight_backup_readiness
    workbench_preflight_backup_formatting

add explicit gate reason model

make package import validation mandatory

repair stale GUI wording

Validation:

package import
preflight owner import
passed_with_warnings → preflight available
blocked status → explicit reason visible
preview hash drift → preflight blocked

Do this first.
Patch 2 — Canonical Workbench Transaction Owner

Purpose:

eliminate active split-brain apply ownership

Create one transaction model:

WorkbenchRefactorTransaction

Own:

snapshot id
source hashes
backup
payload
operation list
apply state
rollback manifest
post-apply state
behavior state

Then:

old pipeline modules
        ↓
either reusable primitives
or retired from active GUI

No third apply engine.
Patch 3 — Shadow Apply and Runtime Readiness

Purpose:

prove generated architecture works before touching source

Pipeline:

preflight ready
        ↓
build payload
        ↓
Git worktree when available
or temporary mirror
        ↓
apply exact payload
        ↓
compileall / py_compile
        ↓
public facade import
        ↓
direct importer smoke tests
        ↓
dependency topology validation
        ↓
focused tests when configured
        ↓
SHADOW_APPLY_PASS

Git worktrees provide the preferred isolated working-tree model when repository conditions permit.
Patch 4 — Workbench Completion GUI

Add/wire:

Preflight status and blocking reason
Shadow Apply Validation
Review Refactor Diff
Build Source Apply Payload
exact authorization token
REFRACTOR MODULE
Rollback Last Refactor
Behavior Validation presets

Critical rules:

Refactor Module = wrapper around canonical apply owner

Rollback available after any write

post-apply failure:
Rollback Recommended

visual diff review before apply

Patch 5 — End-to-End Refactor Validator

Build one real fixture project:

large module >500 lines
public facade
consumer imports
tests
two cohesive helper targets
global dependencies
one intentionally risky dependency

Prove:

Planner plan
        ↓
selected version handoff
        ↓
Workbench snapshot
        ↓
readiness
        ↓
preview
        ↓
structural validation
        ↓
preflight
        ↓
backup
        ↓
payload
        ↓
shadow apply
        ↓
runtime import smoke
        ↓
visual diff
        ↓
Refactor Module
        ↓
post-apply validation
        ↓
behavior validation
        ↓
rollback
        ↓
source exact restoration
        ↓
second apply
        ↓
successful completion

Also verify:

public API preserved
consumer imports preserved
no unrelated file mutation
no helper cycles
no unresolved globals
no rollback residue

Patch 6 — Completion/Freeze Canon Update

Only after the full fixture and one controlled local project refactor succeed.

Then update:

Workbench tutorial
Large Module Refactor Protocol completion section
freeze evidence schema
GUI help text

Do not freeze “Workbench can finish real refactor” until the end-to-end transaction has actually succeeded.
18. Priority ranking
P0 — must repair before real apply

1. Preflight ownership/source integrity gap
2. Runtime unresolved-global/import boundary validation
3. Rollback enablement after failed post-apply validation
4. One canonical apply transaction owner

P1 — required before mature completion

5. Shadow apply
6. Runtime import smoke
7. Visual diff integration
8. Unified import rewrite ownership
9. End-to-end transaction validator

P2 — UX and maturity

10. Refactor Module primary button
11. explicit gate reasons
12. behavior preset integration
13. pytest collection awareness
14. stale UI wording cleanup

The button itself is P2 because adding it before P0/P1 are fixed would only make an unsafe incomplete pipeline look complete.
19. Box boundary audit
Active box

kanda_reasoner_app/
manage_architecture/
large_file_refactor_planner/

Specifically the Workbench-owned execution surface.
In scope

workbench GUI
preflight readiness
backup readiness
source payload
shadow apply
apply transaction
post-apply validation
behavior validation
rollback
visual diff integration
import rewrite integration
transaction state model
Workbench validators
Workbench tutorial

Out of scope

Heuristic scoring redesign
Local AI tournament redesign
Imported Web AI proposal logic
Planner candidate ranking
selected-project business behavior
unrelated Architecture Review tabs
direct frozen-memory writes
Error Memory canonical Lessons writes

Cross-box touches

Potentially:

Architecture Review shell

only for Workbench tab surface integration if necessary.

The Planner → Workbench public handoff should remain unchanged.
20. My final assessment

The Workbench is closer to completion than it looks, because substantial pieces already exist:

real preview
structural validation
preflight concepts
payload creation
guarded apply
post-apply verification
rollback
behavior execution
visual diff
import rewrite support

The problem is that they do not yet form one proven transaction.

The safest completion architecture is:

PLANNER VERSION
        ↓
IMMUTABLE WORKBENCH SNAPSHOT
        ↓
DEPENDENCY READINESS
        ↓
REAL PREVIEW
        ↓
STRUCTURAL VALIDATION
        ↓
PREFLIGHT + BACKUP
        ↓
SOURCE PAYLOAD
        ↓
SHADOW APPLY
        ↓
COMPILE + IMPORT + TEST GATES
        ↓
VISUAL DIFF REVIEW
        ↓
EXACT AUTHORIZATION
        ↓
REFRACTOR MODULE
        ↓
POST-APPLY VALIDATION
        ↓
BEHAVIOR VALIDATION
        ↓
COMPLETED

and from any real write onward:

ROLLBACK AVAILABLE

The safe next implementation train is Patch 1: Workbench Source Integrity and Preflight Restoration, followed by the canonical transaction owner. Force-enabling the existing Stage 5 buttons before those repairs would be the wrong fix.

now we will take a break  explain, in na handoff, to AI what we've done in this chat what is cannon , what is frozen, what we are doing and how we are doing it,  what is next , so that AI can safely continue. Be detailed and write to AI understand it, not necessarily to human understand it.

I’ll produce a continuation handoff as an AI-facing engineering brief: authoritative context first, then current architecture, delivered-but-not-proven-frozen changes, known defects, exact next implementation train, and non-regression rules.

Below is the continuation handoff I would give to the next AI. It is written for an engineering AI agent, not for human readability.


# KANDA Reasoner — Large File Refactor Planner / Workbench Continuation Handoff

Date context: 2026-07-05
Active project/tool root: `E:\kanda_reasoner`
Primary current workstream: Large File Refactor Planner → Large File Refactor Workbench completion pipeline
Human owner: Rafael Kanda

---

# 0. READ THIS FIRST

This handoff is authoritative for continuation of the current workstream, but it does not override canonical KANDA prompts, freeze memory, Router Bridge routing, Box Logic, KANDA Box Shielding, No-Leak Logic, or newer confirmed freeze entries.

Before implementing anything:

1. Load startup context and latest freeze entries newest-first.
2. Inspect the exact current local source tree.
3. Do not assume that every patch described below was installed.
4. Do not assume that every installed patch was frozen.
5. Do not infer canonical freeze status from a ZIP having been generated.
6. Do not infer canonical freeze status from validation success.
7. Freeze evidence merge is not final freeze.
8. Final freeze requires:
   `Freeze Feature After Update -> Preview -> Confirm and Write`.
9. If local source differs from this handoff, inspect:

   * latest freeze entries;
   * current source;
   * installed patch evidence;
   * Error Memory;
     before deciding which state is authoritative.
10. Do not silently repair by bypassing gates.

The human strongly prefers implementation over abstract advice, but correctness and governance are mandatory.

---

# 1. GLOBAL KANDA ARCHITECTURE RULES

## 1.1 Tool/project distinction

KANDA Reasoner is both:

* the tool being developed;
* and, sometimes, the selected current project.

Never confuse:

```text
tool-owned KANDA source
```

with:

```text
selected-project output
```

Tool-level refactor engines, GUI behavior, Planner logic, Workbench logic, routing, prompt-library logic, validation infrastructure, and freeze helpers belong to the KANDA tool root.

Generated refactor output for a selected project must not leak into KANDA source ownership.

---

## 1.2 Active architectural principles

The following are active design principles and must be preserved:

```text
Box Logic
KANDA Box Shielding
No-Leak Logic
```

No-Leak Logic is a named architecture object, not just wording.

It explicitly prevents:

```text
wrong-root writes
tool/project leakage
cross-box leakage
private reach-in
hidden mutable state
public API ownership leakage
generated-artifact-as-source leakage
validation/freeze evidence leakage
```

Before any implementation:

```text
identify active box
identify owner paths
identify allowed files
identify out-of-scope files
declare cross-box touches
preserve public contracts
validate active box
validate every touched external box
```

---

# 2. CONFIRMED PRE-EXISTING FROZEN GOVERNANCE CONTEXT

The following frozen features are known from prior project state and must not regress.

## 2.1 Patch Validate Freeze Recovery Blueprint v1

Active as of 2026-06-29.

Protected behavior includes:

```text
Show Project to AI must provide:
Copy Patch Validate Freeze Recovery Routine
```

The button reads:

```text
patch_validate_freeze_error_memory_routine_blueprint.md
```

from the selected active project root, with app-root fallback only if needed.

The wrapper prompt must remain thin and reference owner canons.

Routing must recognize:

```text
Show Project to AI file/ZIP creation failure
patch validate freeze routine requests
```

Do not bypass:

```text
ZIP contract validation
local validation
freeze evidence merge
Preview
Confirm and Write
```

Error Memory intake must use the governed `KANDA_ERROR_LESSON` workflow.

---

## 2.2 Startup Freeze Context Latest Entries v1

Active as of 2026-06-29.

Startup active-project freeze context must expose latest freeze entries newest-first from canonical external:

```text
<project>_show_project_to_AI/
project_freeze_after_update/
frozen_features_memory/
```

Compact freeze-report truncation must not hide newer frozen entries.

When newer entries conflict with older compact-report lines, newest canonical freeze entry wins.

---

# 3. IMPORTANT STATUS DISTINCTION FOR THIS CHAT

Many features were implemented, packaged, and validated during this workstream.

However:

> Do not assume all of them are canonically frozen.

The conversation contains delivery and freeze code for many patches, but there is no reliable explicit conversational confirmation that every corresponding:

```text
Freeze Feature After Update
-> Preview
-> Confirm and Write
```

was completed locally.

Therefore use these categories:

```text
CONFIRMED FROZEN
    only where latest freeze memory proves it

DELIVERED + VALIDATED
    patch ZIP built and sandbox-validated

INSTALLED
    only if local source/evidence proves installation

FROZEN
    only if canonical freeze memory proves Confirm and Write
```

Never collapse those states.

---

# 4. LARGE MODULE REFACTOR CANON

The existing core canon is:

```text
kanda_prompt_workspace/
prompt_library/
ACTIVE_PROMPTS/
06_refactor_and_architecture_hardening/
large_module_refactor_protocol.md
```

The user supplied the existing v7.2 canon during this chat.

That canon already owns:

```text
module-size law
<=400 ideal
<=500 hard code-module maximum
practical helper granularity
avoid tiny helper hyperpopulation
AST-assisted split audit
public API preservation
dependency-direction mapping
wide responsibility-island mode
multi-island execution layer
patch trains
tiered validation
rollback
fragmentation audit
GUI inventory
freeze requirements
```

Do not create another competing general large-module canon.

An implementation patch was created to advance the intended canon to:

```text
v7.3
```

with a focused external Web AI delegation section.

Do not assume v7.3 is frozen until local canonical freeze proves it.

---

# 5. CURRENT LARGE FILE REFACTOR MENTAL MODEL

The intended architecture is:

```text
AST Split Audit
        ↓
Large File Refactor Planner
        ↓
selected isolated planning version
        ↓
explicit Load Latest Planner Plan
        ↓
immutable Workbench-owned snapshot
        ↓
Large File Refactor Workbench
        ↓
real preview
        ↓
validation
        ↓
preflight
        ↓
backup
        ↓
shadow apply
        ↓
visual diff
        ↓
real refactor transaction
        ↓
post-apply validation
        ↓
behavior validation
        ↓
completion / rollback
```

Planner owns:

```text
analysis
planning
candidate architecture generation
docstring proposals
Local AI bounded planning
Imported Web AI planning review
version comparison
planning summary
```

Planner does not own source mutation.

Workbench owns:

```text
dependency readiness
preview generation
preview structural validation
preflight
backup
source-apply payload
shadow validation
actual apply
post-apply validation
behavior validation
rollback
completion transaction
```

Keep this boundary.

---

# 6. EARLY PLANNER UI / ARCHITECTURE WORK COMPLETED IN THIS STREAM

The following major changes were delivered during the broader Planner workstream.

## 6.1 Child-tab architecture

Planner parent remains under Architecture Review.

Child tabs:

```text
Input & Analysis
Plan & Actions
```

The implementation uses the inner-tab template.

---

## 6.2 Compact settings and Local AI visual treatment

Settings were compacted.

The Local AI checkbox:

```text
Use local AI when available
```

was visually emphasized with bold green text and black frame.

---

## 6.3 Planner action-surface cleanup

Planner `Plan & Actions` was moved toward pre-implementation ownership.

Intended actions included:

```text
Analyze File
Generate Split Plan
Generate Docstring Plan
Review & Refine Plan with Local AI
Show Planning Summary
Copy Planning Summary
```

Implementation actions were removed from Planner ownership.

---

## 6.4 Sonar activity feedback

A reusable green sonar activity monitor was added for long-running Planner actions.

It supports:

```text
start
finish_success
finish_error
set_idle
```

Split generation and Local AI actions use activity feedback.

---

# 7. WORKBENCH SNAPSHOT ISOLATION

A major architecture patch created the intended boundary:

```text
Planner
    ↓ explicit Load Latest Planner Plan
validated immutable Workbench snapshot
    ↓
Workbench owns implementation workflow
```

Important modules include:

```text
planner_workbench_handoff.py
workbench_gui.py
workbench_plan_intake.py
workbench_plan_snapshot.py
workbench_snapshot_bridge.py
```

Protected behavior:

```text
Planner changes must not silently mutate an already-loaded Workbench plan.

Workbench changes its plan only after explicit:
Load Latest Planner Plan
```

This architecture should remain.

---

# 8. PLANNER VERSION ARCHITECTURE

The Planner has three planning-version concepts.

Correct semantics:

```text
Heuristic
Local AI
Imported Web AI Version
```

## 8.1 Heuristic

Generated locally and deterministically.

## 8.2 Local AI

Starts from deterministic Planner evidence and uses bounded Local AI review/correction.

## 8.3 Imported Web AI Version

Not generated locally.

Correct workflow:

```text
Generate Heuristic or Local AI native plan
        ↓
latest native plan recorded
        ↓
Copy Comprehensive Planning for Web AI
        ↓
send package to online AI
        ↓
online AI creates governed import ZIP
        ↓
install pending imported Web AI artifact
        ↓
Receive Planning from Web AI
        ↓
validate against matching native base
        ↓
review
        ↓
Load as Imported Web AI Version
```

The Imported Web AI radio is a selectable imported version, not a local generation strategy.

---

# 9. VERSION ROUTING BEHAVIOR

The version radios are intended to be active before generation.

The selected route controls generation behavior.

Intended native routes:

```text
HEURISTIC
    deterministic plan
    automatic deterministic docstring proposals
    stop

LOCAL AI
    deterministic plan
    automatic deterministic docstring proposals
    staged Local AI architecture process
    tournament
    deterministic selection
```

Imported Web AI Version:

```text
does not locally generate
```

The Proposed Split Plan panel should explicitly rerender the selected isolated version and display:

```text
ACTIVE PLANNER VERSION: Heuristic
```

or:

```text
ACTIVE PLANNER VERSION: Local AI
```

or:

```text
ACTIVE PLANNER VERSION: Imported Web AI Version
```

---

# 10. HEURISTIC EVOLUTION IMPLEMENTED DURING THIS CHAT

A six-step deterministic/AI architecture improvement sequence was developed.

These are important because the next AI should not regress to the original simplistic split heuristic.

---

## STEP 1 — Multi-signal deterministic candidate generation

Original failure:

```text
facade 197

helpers:
38
100
371
41
51
37

4 tiny-helper blockers
status = blocked
```

Step 1 changed the Heuristic from approximately:

```text
dependency connected component
    ≈
one helper module
```

to:

```text
AST dependency clusters
        ↓
must-link atomic groups
        ↓
multi-signal affinity
    structural
    semantic vocabulary
    source proximity
    role compatibility
        ↓
multiple deterministic candidate strategies
        ↓
hard size constraints
        ↓
deterministic ranking
```

Candidate strategies:

```text
dependency-dominant
balanced
responsibility-dominant
```

Real target result:

```text
facade 197
helper 122
helper 452
status planned
```

This converted the original blocked plan to a valid plan.

Feature ID:

```text
large-file-refactor-planner-heuristic-multisignal-candidate-ranking-v1
```

Delivered ZIP:

```text
kanda_large_file_refactor_planner_heuristic_multisignal_candidate_ranking_v1_patch.zip
```

SHA-256:

```text
a92c4b11fb5434da25db76d0266b3b492369c36128beca59d81788228a689f66
```

---

## STEP 2 — Responsibility labeling and semantic naming

Added deterministic responsibility records:

```text
primary responsibility
secondary responsibilities
confidence
confidence score
evidence tokens
per-responsibility scores
```

The real target plan became semantically named:

```text
main_helper_mapper.py                         197

_main_helper_mapper_path_resolution.py       122

_main_helper_mapper_helper_selection.py      452
```

Evidence example:

```text
path_resolution
confidence high
tokens:
path
normalize
root
project
compare
find
```

and:

```text
helper_selection
confidence high
secondary:
decision_reporting
```

Feature ID:

```text
large-file-refactor-planner-responsibility-labeling-semantic-naming-v1
```

ZIP:

```text
kanda_large_file_refactor_planner_responsibility_labeling_semantic_naming_v1_patch.zip
```

SHA-256:

```text
c57c6e96319f797c98ad0a1b523229525ccf4e57c348d42a127714f18cbbe32e
```

---

## STEP 3 — Projected dependency topology and quality scoring

Added deterministic directed module topology evidence.

Important distinction:

```text
helper-only cycle
    = hard blocker

helper -> facade back-reference
    = explicit boundary risk
    not silently treated as clean
    not automatically confused with helper-only cycle
```

Real target evidence:

```text
main_helper_mapper.py
    -> path_resolution
    -> helper_selection

helper_selection
    -> main_helper_mapper.py
```

Risks:

```text
FACADE_BACK_REFERENCE_RISK
FACADE_BOUNDARY_CYCLE_RISK
```

Quality scoring added:

```text
responsibility cohesion
topology score
mixed-responsibility penalty
facade back-reference penalty
```

Real target evidence:

```text
responsibility cohesion = 0.849312
topology score = 0.92
mixed-responsibility penalty = 0.150688
```

Feature ID:

```text
large-file-refactor-planner-topology-responsibility-quality-scoring-v1
```

ZIP:

```text
kanda_large_file_refactor_planner_topology_responsibility_quality_scoring_v1_patch.zip
```

SHA-256:

```text
126de106bd373948382088729856783f8b1304637b8246d6dafb97511409d263
```

---

# 11. LOCAL AI EVOLUTION

## STEP 4 — Staged Local AI protocol

The original Local AI protocol overloaded a 7B model with:

```text
analyze architecture
merge
reassign
rename
answer 8 architecture questions
rationale
warnings
schema compliance
```

in one response.

This repeatedly failed.

Step 4 split Local AI into:

```text
1. Responsibility Analysis
2. Targeted Architecture Repair
3. Deterministic Validation
4. Exact-Rejection Targeted Retry
5. Semantic Naming Review
6. Final Architecture Audit
```

Core principle:

```text
AI suggestions
    ↓
deterministic validation
    ↓
targeted retry with exact rejection reason
```

Architecture actions remain bounded to known objects.

Feature ID:

```text
large-file-refactor-planner-staged-local-ai-protocol-v1
```

ZIP:

```text
kanda_large_file_refactor_planner_staged_local_ai_protocol_v1_patch.zip
```

SHA-256:

```text
b4b101021f0796355a523ca98ed755d618ea86e9446bd55262f60b8e75d99bea
```

---

## STEP 5 — Local AI candidate tournament

Added:

```text
baseline control
Candidate A: conservative/minimal-change
Candidate B: responsibility/cohesion focused
Candidate C: topology/boundary focused
```

Each starts from the same immutable logical baseline.

Not:

```text
baseline -> A -> B -> C
```

but:

```text
          baseline
         /   |   \
        A    B    C
```

Each candidate is independently:

```text
AI-generated
bounded
deterministically validated
deterministically scored
```

KANDA chooses the winner.

The model does not self-select.

Important rule:

```text
AI candidate must beat deterministic baseline threshold
or baseline is preserved
```

Feature ID:

```text
large-file-refactor-planner-local-ai-candidate-tournament-v1
```

ZIP:

```text
kanda_large_file_refactor_planner_local_ai_candidate_tournament_v1_patch.zip
```

SHA-256:

```text
25342cf97708ae704cda4ff83fe5b63f79ff7c15bd9d3ed716c1200251fada88
```

---

# 12. STEP 6 — OPTIONAL GIT CO-CHANGE EVIDENCE

Git history was added only as a supporting signal.

Authority hierarchy:

```text
AUTHORITATIVE

AST evidence
atomic clusters
public facade ownership
size gates
cycle gates
Box Shielding
No-Leak Logic

SUPPORTING

semantic affinity
source proximity
Git historical co-change
```

Git cannot override:

```text
atomic clusters
100–500 size policy
cycle blockers
public API ownership
box boundaries
```

The implementation uses read-only bounded Git queries and graceful fallback.

Feature ID:

```text
large-file-refactor-planner-git-cochange-history-v1
```

ZIP:

```text
kanda_large_file_refactor_planner_git_cochange_history_v1_patch.zip
```

SHA-256:

```text
c9163c36a1a79a0326c5468ec74d4a9e50d9aee4738d5c23bae324c53e2ee65b
```

---

# 13. QUALITY HARDENING AFTER REAL LOCAL AI RUN

A real Heuristic vs Local AI comparison exposed four reporting/protocol weaknesses.

A focused correction patch addressed:

## 13.1 Tournament action accounting

Old ambiguity:

```text
Architecture actions applied: 0
```

while later:

```text
Accepted 22 repair actions
```

Correct distinction:

```text
Candidate exploration actions accepted: N

Final selected-version actions applied: M
```

A candidate may perform exploratory valid actions while baseline still wins.

---

## 13.2 Naming-stage empty array normalization

The Local AI returned:

```json
[]
```

The naming stage now treats this, only in that stage, as:

```json
{
  "module_renames": []
}
```

Do not globally loosen all JSON schemas.

---

## 13.3 Audit retries request missing fields only

Accepted architecture audit answers must be retained.

Retry only unresolved IDs.

Do not ask the 7B model to regenerate already accepted fields.

---

## 13.4 Git confidence weighting

A real project history showed:

```text
observed history commits = 2
raw co-change = 1.0
```

Raw 1.0 with only two commits was misleadingly strong.

Confidence model added:

```text
0 commits     none       0.00
1–2           very_low   0.15
3–5           low        0.35
6–15          moderate   0.65
16+           high       1.00
```

Expose:

```text
raw score
confidence level
confidence weight
effective score
```

Feature ID:

```text
large-file-refactor-planner-quality-hardening-v1
```

ZIP:

```text
kanda_large_file_refactor_planner_quality_hardening_v1_patch.zip
```

SHA-256:

```text
e7ff4308cc69abe04f0ac3922487a9762783efe1748aa669c8f160daa0259bf7
```

Error Memory lesson associated with this correction:

```text
lesson-planner-review-evidence-consistency-and-history-confidence-v1
```

---

# 14. LOCAL AI JSON ADAPTER ERROR HISTORY

Earlier Local AI runs failed four times with:

```text
Local AI response must be JSON only:
Expecting value: line 1 column 1
```

The problem was transport-wrapper brittleness, not necessarily architecture logic.

A focused response adapter repair was created.

It accepts:

```text
plain JSON
fenced JSON
<think>...</think> + JSON
short prose prefix + one JSON object
marker-wrapped JSON
```

while preserving:

```text
schema validation
known symbol restrictions
known module restrictions
atomic cluster validation
size gates
cycle validation
deterministic revalidation
```

Feature ID:

```text
large-file-refactor-planner-local-ai-json-adapter-repair-v1
```

ZIP:

```text
kanda_large_file_refactor_planner_local_ai_json_adapter_repair_v1_patch.zip
```

SHA-256:

```text
53d84b69b3dbfd63762a2ef83ac93e1a3ebcb03b1415becdf8c06a5ce3a787c3
```

Associated Error Memory lesson:

```text
lesson-planner-local-ai-json-wrapper-parse-failure-v1
```

---

# 15. REAL MAIN_HELPER_MAPPER CASE — CURRENT REFERENCE EVIDENCE

Target:

```text
E:\kanda_reasoner\
kanda_reasoner_app\
reasoner_symbol_atlas\
main_helper_mapper.py
```

Source hash:

```text
6637b1dde8639665f37f948d1bf7ba0711ecbe4d418ce304a01503f291f99f55
```

## 15.1 Heuristic result

Current useful Heuristic architecture:

```text
main_helper_mapper.py                         197

_main_helper_mapper_path_resolution.py       122

_main_helper_mapper_helper_selection.py      452
```

Status:

```text
planned
```

No validation blockers.

Current weighted Heuristic candidate evidence from the real run:

```text
heuristic:balanced
score = 0.698662

responsibility = 0.849312
topology = 0.92
mixed_penalty = 0.150688
effective_history = 0.15
```

Git history:

```text
commits observed = 2
confidence = very_low
weight = 0.15
```

This is correct behavior.

---

## 15.2 Local AI result

The Local AI tournament did not improve the final architecture.

Reference result:

```text
baseline_control  0.736690
candidate_a       0.736690
candidate_b       0.640690
candidate_c       0.736690
```

Final selection:

```text
baseline_control
```

Meaning:

```text
Local AI route executed
candidate exploration occurred
inferior alternatives were rejected
deterministic baseline preserved
```

This is now considered a useful guarded-search outcome even though the visible final architecture equals Heuristic.

---

## 15.3 Imported Web AI result

A bounded external Web AI proposal was created.

Native base plan hash:

```text
5b43bf2d61baf9139da5253121dab42b6733685128e4b5fd73091f9a0eebedb4
```

Bounded reassignment:

```text
_related_tests_to_run
```

from:

```text
_main_helper_mapper_helper_selection.py
```

to:

```text
_main_helper_mapper_path_resolution.py
```

Result:

```text
Heuristic:
122 / 452

Imported Web AI:
145 / 429
```

Deterministic comparison evidence:

```text
baseline = 0.736690
Imported Web AI = 0.783250
```

This external proposal was designed to be a small bounded improvement, not a complete redesign.

Corrected import ZIP:

```text
kanda_imported_web_ai_main_helper_mapper_v1_fixed.zip
```

SHA-256:

```text
31b6b73a859f14c4fa6232caed19b16e4f6218835a07d2de7d1a813f063b5686
```

Freeze-evidence bundle:

```text
kanda_imported_web_ai_main_helper_mapper_freeze_v1.zip
```

SHA-256:

```text
0f2a22e5f755a41b019882b11d36743a77aaa9f51816bd87062171991a1af2c7
```

Feature ID for that planning freeze evidence:

```text
imported-web-ai-main-helper-mapper-plan-v1
```

Again: confirm actual canonical freeze status from freeze memory. Do not infer it from bundle existence.

---

# 16. IMPORTED WEB AI INSTALLER BUG AND ERROR MEMORY

The first Web AI import installer falsely reported:

```text
Payload must contain exactly one Web AI begin marker.
```

Exact payload inspection showed one begin marker and one end marker.

Root cause:

```powershell
$PayloadText.Split($BeginMarker)
```

was incorrectly used as a literal substring occurrence counter.

PowerShell/.NET overload behavior can bind to separator semantics inconsistent with intended whole-string counting.

Correct pattern:

```powershell
[regex]::Matches(
    $PayloadText,
    [regex]::Escape($BeginMarker)
).Count
```

and equivalent for the end marker.

Do not repeat:

```powershell
$PayloadText.Split($BeginMarker)
```

for literal marker counting.

Error Memory lesson ID:

```text
lesson-web-ai-import-installer-literal-marker-count-v1
```

Future Web AI installer generation should validate:

```text
exactly one begin marker
exactly one end marker
valid JSON between markers
source hash match
base plan hash match
artifact copy equality
```

---

# 17. IMPORTED WEB AI VERSION SEMANTICS

A dedicated semantic correction changed the wrong earlier interpretation.

Correct model:

```text
Heuristic
    local native generator

Local AI
    local native generator + bounded AI refinement

Imported Web AI Version
    external artifact installed into Planner import inbox
```

`Copy Comprehensive Planning for Web AI` exports:

```text
the most recently generated native plan
```

which may be:

```text
Heuristic
or
Local AI
```

It does not follow the Imported Web AI display radio.

`Receive Planning from Web AI` reads the installed external artifact from:

```text
<drive>\
<project>_show_project_to_AI\
project_large_file_refactor_planner_web_ai_import\
pending_imported_web_ai_plan.txt
```

Then:

```text
validate source hash
validate base plan hash
apply bounded proposal
deterministically validate
show review
Load as Imported Web AI Version
```

Feature ID:

```text
large-file-refactor-planner-imported-web-ai-semantics-v1
```

ZIP:

```text
kanda_large_file_refactor_planner_imported_web_ai_semantics_v1_patch.zip
```

SHA-256:

```text
05266e1c5ea91b391e8cb41c793f197a83cbefe11538c15200899a453cc7fa78
```

Associated Error Memory lesson:

```text
planner_imported_web_ai_semantic_conflation_v1
```

---

# 18. WEB AI SPECIALIST PROMPT / ROUTER / GUI WRAPPER WORK

The user requested a reusable online-AI workflow.

The correct architecture was determined to be:

```text
existing Large Module Refactor Protocol
        ↓
v7.3 delegation section
        ↓
specialist companion prompt
```

not a second competing general refactor canon.

Intended specialist prompt:

```text
KPR-06-001
```

Prompt ID:

```text
web_ai_large_module_refactor_exchange_protocol
```

Canonical intended location:

```text
kanda_prompt_workspace/
prompt_library/
ACTIVE_PROMPTS/
06_refactor_and_architecture_hardening/
web_ai_large_module_refactor_exchange_protocol.md
```

Purpose:

```text
teach online AI how to:
read comprehensive planning package
compare native architecture
search for bounded improvement
avoid merely copying native plan
avoid unnecessary redesign
create correct response
create installable import ZIP
create INSTALL.ps1
create VALIDATE.ps1
create FREEZE.ps1
create freeze hint
create manifest
respect import inbox
validate hashes
preserve Box Shielding / No-Leak
```

Router Bridge intended triggers include:

```text
external Web AI refactor version
online AI improve split plan
Imported Web AI Version
Copy Comprehensive Planning for Web AI
Receive Planning from Web AI
AI Refactor Version How To
```

A GUI wrapper button was added/intended:

```text
AI Refactor Version How To
```

Visual requirement:

```text
orange
bold
```

Position:

```text
immediately after:
Review & Refine Plan with Local AI
```

The button is a thin wrapper:

```text
click
    ↓
resolve canonical prompt-library path
    ↓
read KPR-06-001
    ↓
copy exact canonical prompt to clipboard
```

Do not embed a duplicate specialist prompt body in GUI code.

Feature ID:

```text
large-file-refactor-planner-web-ai-howto-prompt-button-v1
```

ZIP:

```text
kanda_large_file_refactor_planner_web_ai_howto_prompt_button_v1_patch.zip
```

SHA-256:

```text
9df31447640fa56021c45d32bd749d5f297e6dbf53affeb96eb05b1cdb7401fd
```

Verify local install/freeze state before relying on it.

---

# 19. COMPREHENSIVE WEB AI EXPORT REQUIREMENTS

The `Copy Comprehensive Planning for Web AI` package was intentionally improved.

It should provide:

```text
TASK
ACTIVE NATIVE BASE VERSION
SOURCE IDENTITY
SOURCE HASH
BASE PLAN HASH
PUBLIC API CONTRACT
CURRENT PLAN
HEURISTIC CANDIDATES
RESPONSIBILITY EVIDENCE
TOPOLOGY EVIDENCE
GIT HISTORY EVIDENCE + CONFIDENCE
QUALITY SCORES
LOCAL AI TOURNAMENT RESULT
KNOWN MODULES
KNOWN SYMBOLS
ATOMIC CLUSTERS
ALLOWED ACTIONS
FORBIDDEN ACTIONS
IMPROVEMENT GOAL
RESPONSE SCHEMA
ZIP CONTRACT
INSTALLER CONTRACT
VALIDATION CONTRACT
FREEZE-EVIDENCE CONTRACT
```

Core external AI instruction:

```text
Do not merely reproduce the native plan.

First determine whether a bounded,
evidence-backed architecture improvement exists.

Prefer:
one responsibility-outlier reassignment
one safe known-helper merge
one semantic rename
one bounded docstring improvement

Do not invent arbitrary modules or symbols.

If no bounded improvement is defensible,
return truthful no-improvement.
```

Allowed architecture actions remain bounded.

Typical response schema includes:

```text
module_merges
reassignments
module_renames
docstring_updates
architecture_answers
analysis_observations
rationale
warnings
```

Never allow Web AI to bypass deterministic validation.

---

# 20. CURRENT PRIMARY TASK: LARGE FILE REFACTOR WORKBENCH COMPLETION

This is now the next workstream.

The user explicitly requested that the Workbench be taken from current real-preview validation through a complete real refactor pipeline.

The user observed that:

```text
Large File Refactor Workbench
```

gets as far as real preview validation but downstream stages do not become usefully active.

User specifically mentioned:

```text
5. Preflight
Prepare Preflight Backup Readiness
Build Source Apply Payload
Apply Source Changes
Rollback Last Apply
Run Optional Behavior Validation
```

and noted there is no clear:

```text
Refactor Module
```

button.

An architecture audit was performed before implementation.

---

# 21. WORKBENCH AUDIT FINDINGS

## 21.1 Strong first half

The Workbench already has a strong conceptual first half:

```text
Planner selected version
        ↓
explicit Workbench plan intake
        ↓
immutable Workbench snapshot
        ↓
dependency readiness
        ↓
real preview generation
        ↓
real preview structural validation
```

Preserve this.

---

## 21.2 Do not force-enable Stage 5

The correct conclusion of the audit was:

> Do not simply enable downstream buttons.

The completion pipeline has deeper source and transaction issues.

---

## 21.3 Source-integrity gap around preflight

In the audited cumulative source reconstruction:

`workbench_gui.py` referenced preflight modules such as:

```text
source_apply_preflight_backup_contract.py

workbench_preflight_backup_readiness.py

workbench_preflight_backup_formatting.py
```

but these were not found in the provided reconstructed source state.

Important caveat:

The user's actual runtime opens the Workbench, so the live local tree may differ from the source archive used for audit.

Therefore next AI must:

```text
inspect exact local source
do not assume modules are absent
compare imports with actual files
run package import validation
```

The first Workbench patch should restore or reconcile the Stage 5 ownership seam.

---

## 21.4 Two overlapping apply architectures

Audit found two conceptually overlapping source-apply families.

Older governed family, approximately:

```text
final_guarded_source_apply_planning
source_apply_dry_run_validator
source_apply_preflight_backup_contract
guarded_source_apply_executor
post_apply_validation
source_apply_rollback_recovery
```

Newer Workbench family, approximately:

```text
workbench_preflight_backup_readiness
workbench_source_payload_builder
workbench_guarded_source_apply
workbench_post_apply_validator
workbench_rollback_executor
workbench_behavior_validation
```

Next AI must not create a third apply engine.

Required direction:

```text
one canonical interactive Workbench transaction owner
```

Older modules may become:

```text
internal reusable primitives
```

or be retired from active GUI ownership.

Do not leave split-brain ownership over:

```text
backup
transaction id
payload
apply state
rollback manifest
post-apply truth
completion state
```

---

## 21.5 Preview structural validity is not enough

Current Planner evidence can show:

```text
FACADE_BACK_REFERENCE_RISK
FACADE_BOUNDARY_CYCLE_RISK
```

A preview can be:

```text
syntactically valid
AST-valid
structurally plausible
```

while still having runtime problems such as:

```text
moved helper uses facade-owned global
missing runtime import
NameError
circular partial initialization
```

Therefore the Workbench needs a Shadow Apply Runtime Gate before real source mutation.

---

## 21.6 Visual diff exists conceptually but is not integrated into main completion flow

The audit found visual-diff support in the source family but not wired as a required Workbench gate.

Recommended:

```text
shadow apply pass
        ↓
Review Refactor Diff
        ↓
explicit Diff Reviewed state
        ↓
real apply may become armed
```

---

## 21.7 Import rewrite support exists but needs ownership integration

The source family includes import rewrite readiness/apply/rollback concepts.

Policy must remain:

```text
default:
preserve consumer imports through facade

optional explicit migration:
only when approved plan includes import migration
```

When import rewrites are needed, they should be part of the same transaction.

Do not create:

```text
split source transaction
then later separate import rewrite transaction
```

if that creates an intermediate broken state.

---

## 21.8 High-severity rollback enablement defect

The audit found a dangerous conceptual rule:

Rollback appeared to depend on both:

```text
apply status = applied
AND
post-apply status = validated
```

This is wrong.

When:

```text
source write succeeds
post-apply validation fails
```

that is exactly when rollback may be needed.

Correct rule:

```text
if any source mutation occurred
AND rollback manifest is valid
AND rollback has not already completed
    ↓
Rollback remains available
```

Post-apply failure should show:

```text
ROLLBACK RECOMMENDED
```

This is P0.

---

# 22. TARGET WORKBENCH STATE MACHINE

The recommended explicit state machine is:

```text
NO_PLAN
    ↓
PLAN_SNAPSHOT_READY
    ↓
DEPENDENCY_READY
    ↓
REAL_PREVIEW_READY
    ↓
PREVIEW_STRUCTURAL_PASS
    ↓
PREFLIGHT_READY
    ↓
SHADOW_APPLY_PASS
    ↓
VISUAL_DIFF_REVIEWED
    ↓
SOURCE_PAYLOAD_READY
    ↓
APPLY_ARMED
    ↓
REFACTORING
    ↓
APPLIED
    ↓
POST_APPLY_PASS
    ↓
BEHAVIOR_PASS
or
BEHAVIOR_NOT_RUN_ACCEPTED
    ↓
COMPLETED
```

Rollback availability is orthogonal:

```text
SOURCE_WRITE_STARTED
    ↓
ROLLBACK_AVAILABLE
```

until:

```text
rollback complete
or
transaction formally completed/superseded
```

---

# 23. REQUIRED DOWNSTREAM INVALIDATION RULES

Centralize state invalidation.

Examples:

## New Planner plan loaded

Invalidate:

```text
dependency readiness
preview
preview validation
preflight
shadow validation
visual diff review
payload
authorization token
```

## Preview regenerated

Invalidate:

```text
preview validation
preflight
shadow apply
visual diff review
payload
apply authorization
```

## Source changes externally

Invalidate:

```text
preflight
backup readiness
shadow validation
payload
apply authorization
```

Do not scatter this logic across ad hoc button handlers.

---

# 24. SHADOW APPLY REQUIREMENT

Recommended Workbench flow:

```text
preview structural pass
        ↓
preflight
        ↓
backup readiness
        ↓
build source payload
        ↓
SHADOW APPLY
        ↓
compile
        ↓
runtime import smoke
        ↓
dependency validation
        ↓
focused tests
        ↓
visual diff
        ↓
real apply authorization
```

Preferred isolation:

```text
Git worktree
```

when available.

Fallback:

```text
controlled project mirror under daily-work staging
```

Never shadow-apply in the active project root.

The shadow environment must preserve package-relative import behavior.

---

# 25. WORKBENCH TRANSACTION MODEL

Create one explicit transaction object, conceptually:

```text
WorkbenchRefactorTransaction
```

It should own at least:

```text
transaction_id

plan_snapshot_id
source_content_hashes
preview hashes
preflight evidence

backup directory
backup file hashes

payload manifest
payload file hashes
ordered operation list

applied operation index
generated helper list
modified source list

rollback manifest
rollback state

shadow validation evidence
post-apply validation evidence
behavior validation evidence

visual diff reviewed state
authorization state

completion state
```

Do not make the real apply reinterpret the plan independently from preview.

Preview and real apply should share one transformation/payload truth.

---

# 26. PREFLIGHT BACKUP READINESS TARGET

Preflight should prove:

```text
target source hash matches plan basis
expected project files unchanged
destination helper collisions absent
backup destination writable
backup snapshot created
backup hashes verified
rollback manifest prepared
payload basis hash matches preview basis
```

Backups should be under daily-work staging, e.g.:

```text
<project>_delete_after_daily_work/
large_file_refactor_workbench/
transactions/
<TX_ID>/
backup/
```

Do not put transient backup structures into active project root.

---

# 27. REQUIRED `REFACTOR MODULE` BUTTON

The user explicitly wants a clear completion action.

Recommended GUI:

```text
5. Preflight & Refactor

[ Prepare Preflight Backup Readiness ]

[ Run Shadow Apply Validation ]

[ Review Refactor Diff ]

[ Build Source Apply Payload ]

Authorization:
[ exact token ]

[ REFACTOR MODULE ]

[ Rollback Last Refactor ]
```

`Refactor Module` must be a wrapper over the canonical guarded Workbench transaction owner.

It must not become a third apply engine.

Enable only when:

```text
immutable plan snapshot valid
dependency readiness pass
real preview exists
preview structural validation pass
preflight backup ready
shadow apply pass
visual diff reviewed
payload ready
source hashes still match
authorization token exact
```

On click:

```text
REFACTOR MODULE
    ↓
canonical guarded apply transaction
    ↓
source write
    ↓
immediate post-apply validation
```

If validation fails:

```text
ROLLBACK RECOMMENDED
```

and rollback remains enabled.

---

# 28. POST-APPLY VALIDATION TARGET

Fast gate:

```text
expected files exist
file hashes match payload
py_compile touched files
compileall affected package
AST parse
public facade import smoke
direct consumer import smoke
dependency-cycle check
git diff --check when available
```

Medium gate:

```text
focused characterization tests
moved-symbol tests
public API compatibility tests
behavior presets
```

Full gate at phase boundary:

```text
broader project tests
architecture validation
fragmentation audit
workflow validation when applicable
```

Interpret pytest exit statuses explicitly.

A command that collected or ran zero intended tests is not strong behavior evidence.

---

# 29. BEHAVIOR VALIDATION TARGET

Existing behavior-validation safety should preserve:

```text
allowlisted commands
no arbitrary shell
timeout
exit status handling
```

Recommended GUI:

```text
Behavior Validation

Preset:
Focused tests inferred from target
Related tests from Planner evidence
Custom approved command

[ Collect Tests ]
[ Run Behavior Validation ]
```

Use collection evidence to avoid accidentally treating zero-test execution as success.

---

# 30. EXACT NEXT IMPLEMENTATION TRAIN

This is the recommended continuation sequence.

Do not skip directly to the `Refactor Module` button.

---

## PATCH 1 — Workbench Source Integrity and Preflight Restoration

Goal:

```text
restore coherent Stage 5 ownership
```

Tasks:

```text
inspect exact live Workbench source
reconcile missing/stale preflight imports
restore or consolidate preflight owner modules
make package imports pass
add explicit blocking-reason model
verify passed_with_warnings preview validation can advance
verify source/hash drift blocks preflight explicitly
```

Required UI improvement:

Disabled button should have visible reason.

Examples:

```text
PREFLIGHT BLOCKED:
PREVIEW_VALIDATION_NOT_ACCEPTED

PREFLIGHT BLOCKED:
SOURCE_HASH_DRIFT

PREFLIGHT BLOCKED:
PREFLIGHT_OWNER_UNAVAILABLE
```

This patch should not yet create the final Refactor Module action.

---

## PATCH 2 — Canonical Workbench Transaction Owner

Goal:

```text
one active apply ownership model
```

Create transaction model.

Reconcile overlapping apply families.

Decide explicitly which older modules are:

```text
reused primitives
or
retired from active GUI
```

Do not delete potentially useful governed logic without inspection.

---

## PATCH 3 — Shadow Apply and Runtime Readiness

Goal:

```text
prove transformed project works before real mutation
```

Implement:

```text
worktree when possible
or controlled mirror

apply exact payload
compile
import smoke
dependency topology validation
focused test validation
shadow result evidence
```

No real source mutation.

---

## PATCH 4 — Workbench Completion GUI

Wire:

```text
Preflight gate reason
Shadow Apply
Visual Diff Review
Build Payload
Authorization
REFACTOR MODULE
Rollback Last Refactor
Behavior Validation presets
```

Critical fix:

```text
rollback available after any real write
```

---

## PATCH 5 — End-to-End Refactor Transaction Validator

Build a real fixture with:

```text
large >500-line module
public facade
consumer imports
tests
cohesive helper targets
global dependency references
one intentionally risky dependency
```

Prove:

```text
Planner plan
→ Workbench snapshot
→ dependency readiness
→ preview
→ structural validation
→ preflight
→ backup
→ payload
→ shadow apply
→ runtime import
→ visual diff
→ Refactor Module
→ post-apply validation
→ behavior validation
→ rollback
→ exact restoration
→ second apply
→ successful completion
```

Also verify:

```text
public API preserved
consumer imports preserved
no unrelated file mutation
no helper cycles
no unresolved globals
no rollback residue
```

---

## PATCH 6 — Canon / Tutorial / Freeze Completion Update

Only after a successful end-to-end fixture and controlled real local refactor.

Then update:

```text
Workbench tutorial
Large Module Refactor Protocol completion section
freeze evidence schema
GUI help text
```

Do not freeze:

```text
Workbench can complete a real refactor
```

before it actually completes one successfully.

---

# 31. WORKBENCH PRIORITY LEVELS

## P0

```text
preflight source-integrity gap
one canonical transaction owner
runtime unresolved-global/import validation
rollback available after failed post-apply validation
```

## P1

```text
shadow apply
runtime import smoke
visual diff integration
import rewrite ownership
end-to-end validator
```

## P2

```text
Refactor Module primary button
explicit gate reasons
behavior preset integration
pytest collection awareness
stale wording cleanup
```

The button is intentionally after core safety repairs.

---

# 32. RESEARCH-DERIVED DESIGN PRINCIPLES TO KEEP

Prior web research produced several architectural conclusions that should continue guiding implementation.

## Heuristic

Line count is:

```text
a gate
```

not:

```text
the grouping algorithm
```

Use:

```text
structural dependency
semantic responsibility
dependency direction
source proximity
test affinity
optional Git co-change
```

to produce candidates.

Then apply:

```text
100–500 helper constraints
cycle detection
public API ownership
No-Leak
```

---

## Local AI

Local AI should be:

```text
bounded architectural search and critique
```

not:

```text
one-shot sovereign planner
```

Use:

```text
small tasks
targeted rejection feedback
separate naming
separate audit
multiple isolated candidates
deterministic KANDA selection
```

---

## Workbench

Real refactor should follow small, behavior-preserving, validated steps.

The real apply should not independently reinterpret the Planner plan.

Use a transaction model with:

```text
preview truth
payload truth
backup truth
apply truth
rollback truth
validation truth
```

---

# 33. DELIVERY RULES FOR CONTINUATION

For every implementation patch:

```text
deliver ZIP
install code
validate code
freeze-evidence code
```

When the work is a correction/error event:

```text
also deliver Error Memory intake staging code
```

This is an explicit human preference.

Error Memory flow:

```text
ZIP
→ install
→ validate
→ stage pending lesson under:

<project>_show_project_to_AI/
project_error_memory/
pending_ai_assisted_error_lesson_intake/

→ human review
→ Memorize Error
```

Never direct-write canonical Lessons.

---

# 34. POWERSHELL DELIVERY RULES

Use:

```powershell
$DRIVE_ROOT = [System.IO.Path]::GetPathRoot($PROJECT_ROOT)
```

Do not derive drive root with fragile slash trimming.

Wrapper scripts should use independent `if` blocks.

Do not create detachable `else` patterns in copy/paste terminal snippets.

For marker counts:

```powershell
[regex]::Matches(
    $PayloadText,
    [regex]::Escape($Marker)
).Count
```

Do not use:

```powershell
$PayloadText.Split($Marker)
```

as a literal substring occurrence counter.

---

# 35. GUI IMPLEMENTATION STYLE

Do not force-enable actions.

Every blocked stage should expose a reason.

Prefer:

```text
button disabled
+
visible machine-readable reason
```

over silent inactivity.

Long-running actions should use existing sonar/activity feedback patterns.

Do not introduce fixed geometry that breaks smaller displays.

The user prefers a functional strong UI rather than decorative complexity.

---

# 36. CURRENT HUMAN WORKING STYLE / EXPECTATIONS

The human prefers:

```text
implementation rather than prolonged theory
focused patches
exact install code
exact validation code
freeze code every time
Error Memory code on error/correction events
clear comparison of actual outputs
evidence-based architecture decisions
```

When the user says:

```text
go
```

continue the planned next implementation step without reopening settled architectural questions unless source evidence contradicts them.

When a runtime error is reported:

```text
inspect exact error
inspect exact source
repair narrowly
validate exact ZIP
stage Error Memory lesson
provide freeze code
```

Do not simply explain the error.

---

# 37. DO NOT REGRESS THESE SPECIFIC LESSONS

Do not:

```text
make version radios cosmetic
disable route selection before generation
reset selected route during Analyze File
show action completion feedback only on another hidden tab
treat Imported Web AI as a local generation route
export Web AI base according to display radio instead of last native plan
use whole-response json.loads only for local model transport
ask 7B Local AI to solve actions + names + 8 audits in one response
let AI choose tournament winner
treat two Git commits as strong historical evidence
mix exploratory action count with final winner action count
reject [] in the semantic naming stage as a fatal error
repeat all audit fields when only some are missing
count PowerShell markers with String.Split(marker)
create another general refactor canon that competes with large_module_refactor_protocol
embed canonical prompt text inside GUI wrapper
force-enable Workbench preflight/apply buttons without repairing state ownership
disable rollback after post-apply failure
create a third source-apply engine
```

---

# 38. SAFE CONTINUATION ENTRYPOINT

The next AI should begin with:

```text
TASK:
Large File Refactor Workbench Patch 1
Source Integrity and Preflight Restoration
```

First actions:

```text
1. Inspect exact local current source tree.

2. Read:
   - latest freeze context
   - large_module_refactor_protocol current canonical version
   - Workbench tutorial
   - Workbench GUI
   - plan snapshot/intake modules
   - preview renderer
   - structural validator
   - preflight modules/imports
   - payload builder
   - guarded apply modules
   - post-apply validator
   - rollback modules
   - behavior validation modules
   - visual diff modules
   - import rewrite modules

3. Build an ownership map.

4. Reproduce why Stage 5 does not become operational.

5. Do not force-enable it.

6. Repair source ownership and explicit gate reasons.

7. Validate:
   package imports
   stage transition
   passed_with_warnings transition
   blocked reason visibility
   preview/source hash invalidation
   no Workbench/Planner ownership leakage

8. Deliver:
   patch ZIP
   install code
   validation code
   Error Memory intake if a defect is corrected
   freeze-evidence code

9. Stop before Patch 2 unless the user explicitly says go/continue.
```

---

# 39. FINAL STATE SUMMARY

At the pause point:

```text
PLANNER:
substantially improved

Heuristic:
multi-signal
candidate-based
responsibility-aware
topology-aware
Git-confidence-aware

Local AI:
staged
targeted-retry capable
candidate tournament
KANDA-selected

Imported Web AI:
external artifact workflow
bounded validation
review before load
specialist prompt architecture
Router Bridge integration intended
GUI how-to wrapper delivered

WORKBENCH:
strong first half
incomplete second half
must be repaired as one transaction pipeline
```

The current next milestone is not another Planner feature.

The current milestone is:

> Make Large File Refactor Workbench safely complete a real module refactor from validated preview through preflight, backup, shadow apply, visual review, guarded source mutation, post-apply validation, behavior validation, rollback, and completed transaction state.

Do this incrementally.

Do not bypass gates.

Do not create competing owners.

Do not freeze completion claims before real end-to-end proof.


# SESSION_HANDOFF: 2026-07-05 | PROJECT: KANDA Reasoner

# STATUS: PAUSED | CONTEXT_WINDOW_USAGE: HIGH — USE THIS HANDOFF AS PRIMARY CONTINUATION MAP

---

## 1. CANON (IMMUTABLE GROUND TRUTHS)

*Do not alter, bypass, reinterpret loosely, or refactor these principles without an explicit canon update and governed validation/freeze process.*

### Core Architectural Paradigm

* **Architecture model**: Box Logic + KANDA Box Shielding + No-Leak Logic.
* **Active root**: `E:\kanda_reasoner`.
* **Tool/project distinction is mandatory**:

  * KANDA Reasoner tool code belongs to the KANDA tool source tree.
  * Selected-project output must never leak into KANDA tool ownership.
  * Tool-owned refactor engines may analyze and transform selected projects only through explicit governed contracts.

### No-Leak Logic

No-Leak Logic is a named architecture object.

It must explicitly prevent:

* wrong-root writes;
* tool/project leakage;
* cross-box leakage;
* private reach-in;
* hidden mutable state;
* public API ownership leakage;
* generated-artifact-as-source leakage;
* validation/freeze evidence leakage.

Before implementation, the AI must identify:

```text
active box
owner paths
allowed files
out-of-scope files
cross-box touches
public contracts
validation scope
```

### Planner / Workbench Ownership Boundary

The canonical mental model is:

```text
AST Split Audit
        ↓
Large File Refactor Planner
        ↓
selected isolated planning version
        ↓
explicit Load Latest Planner Plan
        ↓
immutable Workbench-owned snapshot
        ↓
Large File Refactor Workbench
        ↓
implementation transaction
```

The Planner owns:

```text
analysis
architecture planning
candidate generation
version comparison
docstring proposals
Local AI bounded review
Imported Web AI planning review
planning summaries
```

The Planner must not mutate source.

The Workbench owns:

```text
dependency readiness
real preview
preview validation
preflight
backup
source payload
shadow apply
real apply
post-apply validation
behavior validation
rollback
transaction completion
```

### Planner Version Semantics

The valid planning versions are:

```text
Heuristic
Local AI
Imported Web AI Version
```

Their meanings are immutable unless canonically updated.

#### Heuristic

Locally generated deterministic architecture.

#### Local AI

Deterministic native architecture plus bounded Local AI architectural search, deterministic validation, candidate tournament, and KANDA-owned winner selection.

#### Imported Web AI Version

An externally generated planning version.

It is not locally generated by selecting its radio.

Correct flow:

```text
Generate Heuristic or Local AI
        ↓
latest generated native plan stored
        ↓
Copy Comprehensive Planning for Web AI
        ↓
external online AI analyzes package
        ↓
external AI returns governed import ZIP
        ↓
install imported artifact
        ↓
Receive Planning from Web AI
        ↓
validate
        ↓
review
        ↓
Load as Imported Web AI Version
```

### Public API Preservation

Large-module refactors must preserve public import contracts unless a separate explicit API migration is approved.

The default first-pass model is:

```text
existing public import path
        ↓
thin public facade
        ↓
private responsibility helpers
```

Consumers should continue importing through the public facade by default.

### Module Size Law

For Python source modules:

```text
ideal: <= 400 physical lines
hard maximum: <= 500 physical lines
practical new-helper minimum: approximately 80–100 substantive lines
```

Small helper exceptions require explicit architectural justification.

Line count is a constraint, not the grouping algorithm.

Group primarily by:

```text
responsibility
dependency direction
semantic cohesion
atomic clusters
public API ownership
topology
test affinity
optional historical coupling
```

### Freeze Law

Never claim something is frozen merely because:

```text
a ZIP was created
a patch installed
validation passed
freeze evidence merged
```

Final canonical freeze requires:

```text
Freeze Feature After Update
→ Preview
→ Confirm and Write
```

Latest canonical freeze memory is authoritative.

### Error Memory Law

On a correction/error event:

```text
repair
→ validate
→ stage KANDA_ERROR_LESSON into pending intake
→ human review
→ Memorize Error
```

Never direct-write canonical Lessons.

Pending intake path:

```text
<project>_show_project_to_AI/
project_error_memory/
pending_ai_assisted_error_lesson_intake/
```

### PowerShell Rules

Use:

```powershell
$DRIVE_ROOT = [System.IO.Path]::GetPathRoot($PROJECT_ROOT)
```

Do not use fragile slash trimming.

For literal marker counting use:

```powershell
[regex]::Matches(
    $PayloadText,
    [regex]::Escape($Marker)
).Count
```

Do not use:

```powershell
$PayloadText.Split($Marker)
```

as a literal whole-marker occurrence counter.

### Delivery Requirement

Every governed implementation patch should provide:

```text
patch ZIP
install terminal code
validation terminal code
freeze-evidence terminal code
```

When fixing an actual error:

```text
also provide Error Memory staging code
```

---

## 2. FROZEN (COMPLETED & LOCKED MODULES)

*Only items whose frozen status is known from existing project context belong here. Do not infer that every patch built in this session is frozen.*

### Patch Validate Freeze Recovery Blueprint v1

Status: frozen feature active as of 2026-06-29.

Protected behavior:

* Show Project to AI exposes `Copy Patch Validate Freeze Recovery Routine`.
* The wrapper reads:
  `patch_validate_freeze_error_memory_routine_blueprint.md`.
* Selected active project root is preferred.
* App-root fallback is allowed only when necessary.
* The wrapper remains thin and references owner canons.
* Routing recognizes:

  * Show Project to AI file/ZIP creation failures;
  * patch/validate/freeze recovery routine requests.
* ZIP validation, local validation, freeze evidence merge, Preview, and Confirm and Write may not be bypassed.

### Startup Freeze Context Latest Entries v1

Status: frozen feature active as of 2026-06-29.

Protected behavior:

* startup freeze context loads latest entries newest-first;
* canonical external freeze memory location is:

```text
<project>_show_project_to_AI/
project_freeze_after_update/
frozen_features_memory/
```

* compact freeze-report truncation may not hide newer entries;
* newer canonical entries override older compact-report lines when they conflict.

### Important Freeze Caution

The Planner patches created during this workstream are not automatically listed here.

Before changing or replacing any of them, inspect:

```text
latest canonical freeze entries
current source tree
installed patch evidence
```

Some session patches were delivered and validated, but canonical freeze completion must be verified locally.

---

## 3. ACTIVE CONTEXT (WHAT WE ARE DOING)

### Current Epic

Complete the KANDA Large File Refactor architecture as a safe end-to-end system:

```text
Planner
        ↓
selected architecture version
        ↓
immutable Workbench snapshot
        ↓
real preview
        ↓
validated implementation transaction
        ↓
successful module refactor
        ↓
post-apply validation
        ↓
behavior validation
        ↓
rollback capability
        ↓
completion state
```

### Current Sprint Goal

Repair and complete the **Large File Refactor Workbench** from the current preview-validation stage through:

```text
Preflight
Backup Readiness
Source Apply Payload
Shadow Apply
Visual Diff Review
Refactor Module
Post-Apply Validation
Behavior Validation
Rollback
Completion
```

### Work Done So Far in This Chat Session

#### Planner architecture was substantially strengthened

The Planner evolved from an initial dependency-cluster splitter that generated:

```text
facade: 197 lines

helpers:
38
100
371
41
51
37

status: blocked
```

into a multi-signal deterministic planner producing:

```text
facade: 197

path_resolution: 122

helper_selection: 452

status: planned
```

#### Step 1 — Multi-signal Heuristic

Implemented:

```text
structural affinity
semantic affinity
source proximity
role compatibility
multiple candidate strategies
hard size gates
deterministic ranking
```

Strategies:

```text
dependency-dominant
balanced
responsibility-dominant
```

Reference feature:

```text
large-file-refactor-planner-heuristic-multisignal-candidate-ranking-v1
```

#### Step 2 — Responsibility Labeling and Semantic Naming

Implemented deterministic labels:

```text
primary responsibility
secondary responsibilities
confidence
evidence tokens
semantic filenames
```

Reference result:

```text
_main_helper_mapper_path_resolution.py
_main_helper_mapper_helper_selection.py
```

Reference feature:

```text
large-file-refactor-planner-responsibility-labeling-semantic-naming-v1
```

#### Step 3 — Topology and Quality Scoring

Added projected module topology and quality evidence.

Distinguishes:

```text
helper-only cycle
    = hard blocker

facade back-reference
    = explicit boundary risk
```

Real case evidence included:

```text
responsibility cohesion: 0.849312
topology score: 0.92
mixed-responsibility penalty: 0.150688
```

Reference feature:

```text
large-file-refactor-planner-topology-responsibility-quality-scoring-v1
```

#### Step 4 — Staged Local AI Protocol

Changed Local AI from one oversized request into:

```text
Responsibility Analysis
        ↓
Targeted Architecture Repair
        ↓
Deterministic Validation
        ↓
Exact-Rejection Targeted Retry
        ↓
Semantic Naming Review
        ↓
Final Architecture Audit
```

Reference feature:

```text
large-file-refactor-planner-staged-local-ai-protocol-v1
```

#### Step 5 — Local AI Candidate Tournament

Added:

```text
baseline control

Candidate A:
conservative/minimal-change

Candidate B:
responsibility/cohesion

Candidate C:
topology/boundary safety
```

Each starts from the same logical baseline.

KANDA deterministically validates and scores them.

The model does not choose the winner.

Reference feature:

```text
large-file-refactor-planner-local-ai-candidate-tournament-v1
```

#### Step 6 — Git Historical Coupling

Added optional read-only Git co-change evidence.

Git evidence is supporting only.

It cannot override:

```text
atomic cluster authority
size gates
cycle gates
public facade ownership
Box Shielding
No-Leak Logic
```

Reference feature:

```text
large-file-refactor-planner-git-cochange-history-v1
```

#### Quality Hardening

Real Local AI output exposed four issues.

Fixed:

```text
exploration action count
vs
final selected action count
```

Naming stage now tolerates:

```json
[]
```

as a stage-specific no-op.

Audit retries request only missing fields.

Git history confidence weighting was added.

Reference model:

```text
0 commits       none       0.00
1–2 commits     very_low   0.15
3–5 commits     low        0.35
6–15 commits    moderate   0.65
16+ commits     high       1.00
```

Reference feature:

```text
large-file-refactor-planner-quality-hardening-v1
```

#### Local AI JSON Adapter Repair

Earlier Local AI outputs failed due to transport-wrapper parsing.

The adapter was expanded to safely extract one bounded JSON object from:

```text
plain JSON
fenced JSON
<think>...</think> + JSON
light prose + JSON
marker-wrapped JSON
```

Schema and architecture validation remain strict.

Reference feature:

```text
large-file-refactor-planner-local-ai-json-adapter-repair-v1
```

#### Imported Web AI Semantics

Corrected the architecture so Imported Web AI is not treated as a local generation route.

Reference feature:

```text
large-file-refactor-planner-imported-web-ai-semantics-v1
```

#### Real Web AI Example

For:

```text
main_helper_mapper.py
```

the Heuristic architecture was:

```text
122 / 452
```

A bounded external Web AI proposal moved:

```text
_related_tests_to_run
```

from:

```text
helper_selection
```

to:

```text
path_resolution
```

producing:

```text
145 / 429
```

Deterministic comparison evidence used during planning:

```text
baseline: 0.736690
Imported Web AI: 0.783250
```

This demonstrated the intended external Web AI role:

```text
small bounded evidence-backed improvement
```

rather than:

```text
copy native plan unchanged
```

or:

```text
invent an entirely unrelated architecture
```

#### Web AI Specialist Prompt Architecture

The existing Large Module Refactor Protocol remains the core owner.

The intended architecture is:

```text
large_module_refactor_protocol v7.3
        ↓ delegates
KPR-06-001
Web AI Large Module Refactor Exchange and Import Protocol
```

The specialist prompt teaches external online AI to:

```text
read Comprehensive Planning package
evaluate native plan
search for bounded improvement
respect known symbols/modules
preserve atomic clusters
create correct response schema
create governed ZIP
create correct installer
validate hashes
create freeze-evidence bundle
```

A thin GUI wrapper was delivered:

```text
AI Refactor Version How To
```

Requirements:

```text
orange
bold
immediately after Review & Refine Plan with Local AI
```

The button should read the canonical specialist prompt and copy it to clipboard.

It must not embed a duplicate prompt body in GUI source.

Reference feature:

```text
large-file-refactor-planner-web-ai-howto-prompt-button-v1
```

---

## 4. METHODOLOGY & STACK (HOW WE ARE DOING IT)

### Language and Runtime

Primary implementation language:

```text
Python
```

GUI:

```text
PySide6 / Qt
```

PowerShell is used for governed:

```text
install
validation
freeze-evidence merge
Error Memory staging
```

### Source Transformation Philosophy

Prefer:

```text
whole-symbol movement
responsibility islands
format-preserving transformation
deterministic evidence
```

Avoid:

```text
arbitrary line slicing
physical half/half splitting
statement-block extraction
source stored as runtime ZIP payload architecture
tiny helper proliferation
```

LibCST or equivalent formatting-preserving editing is preferred for deterministic source edits.

### Planner Methodology

The Planner architecture is:

```text
deterministic evidence first
        ↓
multiple candidates
        ↓
hard gates
        ↓
quality scoring
        ↓
optional bounded Local AI search
        ↓
optional external Web AI proposal
        ↓
deterministic validation
```

### AI Authority Rule

AI may propose.

AI does not become source truth.

KANDA owns:

```text
validation
candidate scoring
winner selection
source mutation
rollback truth
freeze evidence
```

### Testing Strategy

For each implementation patch:

```text
focused validator
Python compilation
package import smoke
box-boundary validation
No-Leak validation
module-size validation
ZIP contract validation
previous-step regression validators
```

For real refactor execution, target validation ladder is:

#### Fast Gate

```text
expected files exist
hashes match
py_compile
compileall
AST parse
public facade import smoke
consumer import smoke
cycle check
git diff --check when available
```

#### Medium Gate

```text
characterization tests
moved-symbol tests
public API compatibility tests
behavior presets
```

#### Full Gate

```text
broader project tests
architecture validation
fragmentation audit
workflow validation when applicable
```

### Error Handling Pattern

Do not silently fail.

Long-running GUI actions should use visible activity feedback.

Disabled actions should expose blocking reasons.

Preferred:

```text
PREFLIGHT BLOCKED:
SOURCE_HASH_DRIFT
```

instead of an unexplained disabled button.

### Delivery Strategy

Each governed patch must be independently:

```text
installable
validatable
freeze-preparable
rollback-aware
```

Sequential patch trains must remain:

```text
Patch A:
install → validate → freeze

Patch B:
install → validate → freeze
```

Never:

```text
install A
install B
install C
validate everything later
```

---

## 5. CURRENT STATE (EXACT CHECKPOINT)

### Active Development Focus

```text
Large File Refactor Workbench
```

### Current Known Good Conceptual Pipeline

```text
Planner selected version
        ↓
explicit Load Latest Planner Plan
        ↓
immutable Workbench snapshot
        ↓
Dependency Readiness
        ↓
Generate Real Preview
        ↓
Validate Real Preview
```

The Workbench's first half is conceptually strong.

### Current Problem

The Workbench does not yet form one proven end-to-end source-refactor transaction.

The user reports the downstream flow around:

```text
5. Preflight

Prepare Preflight Backup Readiness
Build Source Apply Payload
Apply Source Changes
Rollback Last Apply
Run Optional Behavior Validation
```

does not behave as a complete usable pipeline.

There is also no clear primary:

```text
Refactor Module
```

button.

### Important Audit Findings

#### Finding A — Do Not Force-Enable Stage 5

The issue is not merely button enablement.

The completion pipeline has deeper ownership and runtime-validation gaps.

#### Finding B — Possible Preflight Source-Integrity Gap

The audited reconstruction showed GUI references to modules such as:

```text
source_apply_preflight_backup_contract.py
workbench_preflight_backup_readiness.py
workbench_preflight_backup_formatting.py
```

while those modules were not found in the reconstructed archive state.

The live runtime may differ.

Therefore first continuation action is:

```text
inspect exact local source
reproduce exact Stage 5 blocker
validate package imports
```

Do not assume the files are actually missing locally.

#### Finding C — Two Overlapping Apply Architectures

Older apply family approximately:

```text
final_guarded_source_apply_planning
source_apply_dry_run_validator
source_apply_preflight_backup_contract
guarded_source_apply_executor
post_apply_validation
source_apply_rollback_recovery
```

Newer Workbench family approximately:

```text
workbench_preflight_backup_readiness
workbench_source_payload_builder
workbench_guarded_source_apply
workbench_post_apply_validator
workbench_rollback_executor
workbench_behavior_validation
```

There must be one active transaction owner.

Do not create a third apply engine.

#### Finding D — Structural Preview Validation Is Insufficient

A generated preview can be:

```text
syntax-valid
AST-valid
structurally valid
```

while still having runtime errors due to:

```text
unresolved global
missing import
facade back-reference
partial circular initialization
```

Therefore real apply must eventually be preceded by:

```text
Shadow Apply Runtime Validation
```

#### Finding E — Rollback Gating Is Potentially Dangerous

Rollback must remain available after any real source mutation.

Correct model:

```text
SOURCE_WRITE_STARTED
        ↓
ROLLBACK_AVAILABLE
```

Post-apply failure should produce:

```text
ROLLBACK RECOMMENDED
```

not disable rollback.

#### Finding F — Visual Diff Needs Main-Flow Integration

Visual diff support exists conceptually but should become an explicit gate:

```text
Shadow Apply Pass
        ↓
Review Refactor Diff
        ↓
Diff Reviewed
        ↓
real apply may be armed
```

### Branch / Commit Status

Unknown from this handoff.

Upon resume:

```text
inspect git status
inspect current branch
inspect latest commits
do not automatically rewrite history
```

Do not assume any specific branch or commit hash.

### Uncommitted Changes

Unknown.

The AI must inspect the actual local tree before patching.

### Environment Requirements

Known project root:

```text
E:\kanda_reasoner
```

Expected external workflow roots derive from:

```powershell
[System.IO.Path]::GetPathRoot($PROJECT_ROOT)
```

Typical generated external locations include:

```text
E:\kanda_reasoner_delete_after_daily_work\
E:\kanda_reasoner_show_project_to_AI\
```

Do not invent alternate roots.

---

## 6. BLOCKERS / UNRESOLVED EDGE CASES

### 1. Workbench Stage 5 Source Ownership

Need to inspect exact live source and determine whether:

```text
preflight modules are absent
preflight imports are stale
preflight owner exists under another architecture
GUI state transition is incorrect
```

Do not repair by blindly enabling controls.

### 2. Apply Architecture Split-Brain

Two source-apply families appear to overlap.

Need an ownership map for:

```text
preflight
backup
payload
apply
post-apply validation
rollback
behavior validation
completion state
```

Exactly one active GUI transaction owner must emerge.

### 3. Runtime Import Safety

Current preview validation must be audited for:

```text
moved helper unresolved globals
missing synthesized imports
facade-helper circular initialization
consumer import compatibility
```

This is a major reason to add Shadow Apply.

### 4. Multi-File Apply Transaction Safety

Per-file `os.replace` is not equivalent to a whole-refactor atomic transaction.

Need an explicit transaction manifest tracking:

```text
ordered operations
applied operation index
backups
generated helper files
rollback plan
post-apply evidence
```

### 5. Rollback Availability

Rollback must not depend on successful post-apply validation.

Any real write should activate rollback capability.

### 6. Visual Diff Review

Need a human-visible required diff review state before real apply.

### 7. Import Rewrite Ownership

Import migration logic must remain optional and explicit.

Default:

```text
consumers continue importing from facade
```

When import migration is approved, it should be part of the same transaction.

### 8. Behavior Validation Strength

Need to distinguish:

```text
tests truly executed and passed
```

from:

```text
zero intended tests collected
```

Consider collection verification before behavior execution.

### 9. Freeze Status Uncertainty for Session Patches

Do not assume session-delivered Planner patches are frozen.

Check canonical freeze memory before modifying their protected behavior.

---

## 7. IMMEDIATE NEXT ACTIONS (FOR THE AI TO EXECUTE)

Execute sequentially.

### ACTION 1 — Inspect Exact Current Workbench Source

Read and map:

```text
workbench_gui.py

planner_workbench_handoff.py
workbench_plan_intake.py
workbench_plan_snapshot.py
workbench_snapshot_bridge.py

preview renderer modules
real preview validator modules

preflight modules
backup modules

source payload builder
guarded apply modules

post-apply validator
rollback modules

behavior validation modules

visual diff modules
import rewrite modules

Workbench tutorial
current large_module_refactor_protocol.md
latest freeze entries
Error Memory lessons relevant to Workbench
```

### ACTION 2 — Reproduce the Stage 5 Blocker

Determine precisely why:

```text
Prepare Preflight Backup Readiness
```

does not become operational after a valid real preview.

Test at least:

```text
preview status = passed
preview status = passed_with_warnings
preview hash changed
source hash changed
preflight owner import missing
```

Output explicit machine-readable reason.

### ACTION 3 — Produce Box Ownership Audit

State:

```text
active box
owner paths
allowed changes
out-of-scope changes
cross-box touches
public contracts
validation scope
```

Do not implement before this audit.

### ACTION 4 — Build Patch 1

Patch title:

```text
Workbench Source Integrity and Preflight Restoration
```

Goals:

```text
repair/reconcile preflight owner modules
make package imports pass
restore valid preview → preflight transition
add explicit gate-reason model
block stale preview/source hashes
preserve Planner/Workbench isolation
```

Do not yet add the final `Refactor Module` button.

### ACTION 5 — Validate Patch 1

Required proof:

```text
Workbench package import: PASS
preflight owner import: PASS

passed preview:
preflight available

passed_with_warnings:
preflight available when contract allows

blocked preview:
preflight unavailable
blocking reason visible

preview hash drift:
preflight blocked

source hash drift:
preflight blocked

Planner snapshot mutation:
does not silently contaminate Workbench

Box Shielding: PASS
No-Leak Logic: PASS
module-size gate: PASS
ZIP contract: PASS
```

### ACTION 6 — Deliver Governed Artifact

Provide:

```text
patch ZIP
install terminal code
validate terminal code
freeze-evidence terminal code
```

If the repair fixes an actual defect:

```text
also include Error Memory staging terminal code
```

### ACTION 7 — Stop After Patch 1

Do not automatically continue into transaction-owner consolidation unless the human says:

```text
go
continue
```

---

## 8. CONTINUATION PROTOCOL (SAFETY GUARDRAILS)

### First Action Upon Resume

Do not start by editing code.

First:

```text
1. inspect current source tree
2. inspect latest canonical freeze entries
3. inspect git status and current branch
4. inspect relevant Error Memory lessons
5. inspect current Workbench imports/state transitions
6. reproduce Stage 5 blocker
```

### Autonomy Threshold

The AI may autonomously:

```text
inspect source
run static analysis
run focused validation
repair narrowly scoped implementation defects
add focused validators
stage Error Memory pending lesson
package governed patch ZIP
```

The AI must not autonomously:

```text
bypass Workbench gates
force-enable source mutation
direct-write canonical freeze memory
direct-write Error Memory Lessons
replace Planner/Workbench ownership model
invent a third apply engine
alter frozen behavior without explicit override
```

### Stoppage Conditions

Stop the current patch train when:

```text
package import fails unexpectedly
freeze memory conflicts with handoff assumptions
exact local source differs materially from audited architecture
source ownership is ambiguous
a patch would require bypassing validation
rollback cannot be made reliable
cross-box ownership cannot be resolved
```

When blocked, produce exact evidence rather than a speculative patch.

### Error Event Protocol

When a runtime/install/validation/freeze error occurs:

```text
inspect exact traceback
inspect exact source
inspect Error Memory formulary
repair narrowly
validate exact package
stage pending lesson
provide Error Memory terminal code
provide freeze code
```

### Freeze Protocol

Do not say:

```text
feature frozen
```

after only:

```text
validation pass
freeze hint creation
freeze evidence merge
```

Canonical completion is:

```text
Freeze Feature After Update
→ Preview
→ Confirm and Write
```

### Context Compression Rule

When context becomes large, preserve in full:

```text
CANON
FROZEN
ACTIVE CONTEXT
CURRENT STATE
BLOCKERS
IMMEDIATE NEXT ACTIONS
CONTINUATION PROTOCOL
```

Lower-priority raw source excerpts may be dropped.

Never compress away:

```text
Planner/Workbench ownership boundary
No-Leak Logic
version semantics
freeze law
Error Memory law
exact next Workbench patch order
rollback availability rule
do-not-create-third-apply-engine rule
```

### Do-Not-Regress List

Do not:

```text
make version radios cosmetic
disable version selection until after generation
reset selected version during Analyze File
treat Imported Web AI as a local generator
export Web AI package based on display radio instead of latest native plan
embed canonical prompts in GUI wrappers
use whole-response-only JSON parsing for Local AI transport
ask small Local AI models to solve actions + naming + audit in one response
let AI choose tournament winner
treat weak Git history as strong evidence
mix candidate exploration action counts with final applied action counts
reject [] as fatal in naming stage
retry complete audit when only fields are missing
count PowerShell markers with String.Split(marker)
create a competing general large-module refactor canon
force-enable Workbench preflight/apply controls
disable rollback after post-apply failure
create a third source-apply engine
allow real apply to reinterpret the plan differently from preview
freeze end-to-end Workbench completion before proving it
```

### Planned Workbench Train After Patch 1

After explicit human continuation:

```text
PATCH 2
Canonical Workbench Transaction Owner

PATCH 3
Shadow Apply and Runtime Readiness

PATCH 4
Workbench Completion GUI
including:
Refactor Module
Visual Diff Review
Rollback Last Refactor
Behavior Validation integration

PATCH 5
End-to-End Refactor Transaction Validator

PATCH 6
Tutorial / Canon / Freeze Completion Update
```

The final target architecture is:

```text
PLANNER VERSION
        ↓
IMMUTABLE WORKBENCH SNAPSHOT
        ↓
DEPENDENCY READINESS
        ↓
REAL PREVIEW
        ↓
STRUCTURAL VALIDATION
        ↓
PREFLIGHT
        ↓
BACKUP
        ↓
SOURCE PAYLOAD
        ↓
SHADOW APPLY
        ↓
COMPILE + IMPORT + TEST GATES
        ↓
VISUAL DIFF REVIEW
        ↓
EXACT AUTHORIZATION
        ↓
REFACTOR MODULE
        ↓
POST-APPLY VALIDATION
        ↓
BEHAVIOR VALIDATION
        ↓
COMPLETED
```

From the first real source mutation onward:

```text
ROLLBACK AVAILABLE
```

until:

```text
rollback complete
```

or:

```text
transaction formally completed or superseded
```

---

# END OF SESSION HANDOFF

Primary continuation entrypoint:

```text
Large File Refactor Workbench
Patch 1:
Source Integrity and Preflight Restoration
```

Do not begin with the final `Refactor Module` button.

Repair the source ownership seam and state transition first.

Do not bypass gates.

Do not create competing owners.

Do not claim frozen status without canonical evidence.

Do not allow a source write unless rollback remains available afterward.
