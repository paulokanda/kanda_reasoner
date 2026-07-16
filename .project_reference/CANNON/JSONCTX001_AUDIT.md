# JSONCTX001 Audit - AI Context Bundle for Tab 4

Status: read-only audit complete
Source inspected: uploaded developer_tools.zip and json_complete.zip
Source changes made: none
Generated artifacts changed in project source: none

## 1. Scope of this audit

This audit started the roadmap only. It did not implement code.

The goals were to identify:

1. Where Tab 4 Run Collector is built.
2. Where the current destructive refresh behavior lives.
3. Where complete JSON is generated.
4. Where current project evidence paths are resolved.
5. Where Tab 8 exclusion rules are loaded and applied.
6. How Engineering Safety reaches complete JSON.
7. Which owner boxes are involved.
8. What must be done before adding the companion JSON bundle and ZIP export.

## 2. Current high-level flow

The current Tab 4 collection flow is layered:

```text
ReasonerToolsWindow outer shell
    patches embedded CollectorRunnerWindow
    owns project-root propagation
    owns destructive refresh wrapper
        -> CollectorRunnerWindow inner collector UI
            owns Run Collector button and QProcess stages
                -> runtime trace subprocess
                -> collector child subprocess
                    -> collector_main.run_collector(...)
                        -> writes <project_slug>__complete.json
```

Important consequence:

```text
The visible Run Collector behavior is not owned by only one file.
The wrapper owns output cleanup and project-root propagation.
The embedded collector owns the child collector process.
The collector_main module owns complete JSON content generation.
```

## 3. Tab 4 UI audit

### 3.1 Inner collector UI

The inner collector UI creates the Run Collector button in:

```text
kanda_reasoner_app/reasoner_tools_shell/runner_help/window_methods_private_impl.py
```

Relevant current behavior:

```text
self.run_button = QPushButton("Run Collector")
self.close_button = QPushButton("Close")
button_row.addWidget(self.run_button)
button_row.addWidget(self.close_button)
```

Implementation implication:

```text
The new button "Zip and Send to folder" can be added next to Run Collector by adding
self.zip_send_button = QPushButton("Zip and Send to folder")
inside the same button row.
```

This file is a helper used by the source-preserving runner payload. Editing it is less invasive than editing the encoded payload directly.

### 3.2 Inner collector process logic

The inner collector run handler lives in:

```text
kanda_reasoner_app/reasoner_tools_shell/runner_help/window_process_private_impl.py
```

Relevant current behavior:

```text
_run_collector(...)
    resolves project root
    resolves output JSON
    creates empty JSON if missing
    starts runtime trace process

_start_collector_process(...)
    starts runner.py --collector-child <project_root> <output_json> <runtime_trace_json>
```

The child process ultimately calls the source-preserving payload function:

```text
_run_collector_child(project_root, output_json, runtime_trace_json)
    collector_main.run_collector(...)
```

## 4. Destructive refresh audit

The destructive refresh is not in the inner collector child. It is in the outer GUI shell wrapper:

```text
kanda_reasoner_app/reasoner_tools_gui_shell/main_window_help/window_tool_patches.py
kanda_reasoner_app/reasoner_tools_gui_shell/main_window_help/window_output_paths.py
```

Current wrapper behavior:

```text
_run_collector_via_wrapper(widget)
    project_root = normalize from widget.project_root_edit
    remember project root
    if output dirs have content:
        ask confirmation
        if accepted:
            reset output dirs
    set output_json_edit to complete JSON path
    set runtime_trace_json_edit to runtime trace path
    call widget._original_run_collector()
    restore output_json_edit display to json_complete folder
```

Current deletion behavior:

```text
_reset_output_dirs(project_root)
    ensure evidence dirs
    clear json_complete dir
    clear json_splitted dir
```

Current deletion is broad inside both generated-output folders:

```text
<PROJECT_ROOT>/PROJECT_ANALYSIS_EVIDENCE/json_complete
<PROJECT_ROOT>/PROJECT_ANALYSIS_EVIDENCE/json_splitted
```

Implementation implication:

```text
To preserve current user-visible logic, the future Run Collector integration should remain in
_run_collector_via_wrapper rather than bypassing it.
```

Safety note:

```text
The current implementation clears whole output directories. If the new bundle creates ZIPs in
json_complete, ZIP deletion behavior must be decided explicitly. Safer default: do not store ZIPs
inside json_complete, or do not delete exported ZIPs unless explicitly scoped.
```

## 5. Evidence path audit

Current active path helper:

```text
kanda_reasoner_app/project_analysis_evidence_paths.py
```

Current implemented constant:

```text
PROJECT_ANALYSIS_EVIDENCE_DIR = "PROJECT_ANALYSIS_EVIDENCE"
```

Current output pattern:

```text
<PROJECT_ROOT>/PROJECT_ANALYSIS_EVIDENCE/json_complete/<project_slug>__complete.json
<PROJECT_ROOT>/PROJECT_ANALYSIS_EVIDENCE/json_complete/<project_slug>__complete_runtime_trace.json
<PROJECT_ROOT>/PROJECT_ANALYSIS_EVIDENCE/json_splitted/...
```

Canonical correction from user:

```text
<PROJECT_ROOT>/project_analysis_evidence/json_complete/...
```

Important implication:

```text
Lowercasing the folder is not only a display change. It affects production helpers, Project Symbol Atlas helpers, and tests.
This should be implemented as its own focused task before or alongside the bundle skeleton.
```

Related files that currently assume uppercase evidence folder:

```text
kanda_reasoner_app/project_analysis_evidence_paths.py
kanda_reasoner_app/reasoner_symbol_atlas/evidence_paths.py
kanda_reasoner_app/reasoner_symbol_atlas/evidence_producer_status.py
kanda_reasoner_app/reasoner_symbol_atlas/final_status.py
kanda_reasoner_app/reasoner_symbol_atlas/_related_file_finder_support.py
kanda_reasoner_app/reasoner_context_collector/collector_web_ai_complete_json_audit.py
```

Tests that currently assert uppercase evidence paths include:

```text
tests/test_project_analysis_evidence_paths.py
tests/test_pa007c_tab4_complete_json_output_path.py
tests/test_pa007d_tab5_split_json_output_path.py
tests/test_pa007e_project_analysis_evidence_status.py
tests/test_pa007a_project_analysis_evidence_paths.py
tests/test_pa008_complete_json_atlas_adapter.py
tests/test_pa009_evidence_freshness_checker.py
tests/test_pa010_live_and_json_evidence_merger.py
tests/test_pa022_reasoner_symbol_atlas_final_status.py
```

## 6. Complete JSON generation audit

The current complete JSON is generated by:

```text
kanda_reasoner_app/reasoner_context_collector/collector_main.py
```

This is a source-preserving facade that loads private source parts from:

```text
kanda_reasoner_app/reasoner_context_collector/collector_main_help/
```

Decoded source behavior inspected:

```text
run_collector(project_root, output_json, runtime_trace_json=None)
    root = Path(project_root).expanduser().resolve()
    output_path = Path(output_json).expanduser().resolve()
    config = CollectorConfig()
    python_files = walk_python_files_filtered(root, config)
    parse each Python file
    build many indexes
    safe_json_dump(output, output_path)
```

The current complete JSON is Python-centric:

```text
walk_python_files_filtered(...)
source_file_index has Python file records
files list contains Python file records
active_code_index contains Python file records
```

The uploaded complete JSON had:

```text
collector_version: 1.8
source_file_index count: 522
files count: 522
active_code_index count: 522
symbol_index count: 2029
primary_definition_index count: 2047
```

Important implication:

```text
The companion active_snapshot.json should not be implemented by changing complete.json.
It should use a new active-file walker that includes active non-Python files as well.
```

## 7. Complete JSON contract audit

Current complete JSON is already an internal contract for Project Symbol Atlas and Engineering Safety.

Direct complete JSON adapter:

```text
kanda_reasoner_app/reasoner_symbol_atlas/complete_json_adapter.py
```

It expects required sections:

```text
source_file_index
symbol_index
primary_definition_index
```

It selects files under canonical evidence directory and accepts filenames ending with:

```text
__complete.json
_complete.json
```

Engineering Safety integration path:

```text
kanda_reasoner_app/engineering_safety/reasoner_symbol_atlas_integration.py
    -> ProjectSymbolAtlasExistingCodeFinderOptions
    -> ProjectSymbolAtlasPrePatchGateOptions
    -> Project Symbol Atlas complete JSON adapter / evidence freshness logic
```

Implementation implication:

```text
Do not change complete.json schema or meaning in this roadmap.
Add companion files only.
Use names that do not end with __complete.json except the existing complete file.
```

The planned companion names are safe for the adapter selection rule:

```text
<project_slug>__active_snapshot.json
<project_slug>__file_manifest.json
<project_slug>__exclusion_rules.json
<project_slug>__validation_state.json
<project_slug>__bundle_manifest.json
```

None of these end with __complete.json.

## 8. Tab 8 exclusion audit

There is now a unified project exclusion policy:

```text
kanda_reasoner_app/project_exclusion_policy.py
```

It loads rules from:

```text
environment variables
.reasoner_tools_gui_prefs.json
.collector_runner_prefs.json
project_ignore_rules
ignore_rules
tab8_ignore_rules
project_exclusion_rules
```

The Tab 4 scope guard also propagates exclusion rules into child processes:

```text
kanda_reasoner_app/reasoner_tools_shell/tab4_scope_guard.py
PROJECT_REASONER_TAB8_IGNORE_RULES_JSON
PROJECT_REASONER_IGNORE_RULES_JSON
KANDA_REASONER_TAB8_IGNORE_RULES_JSON
```

The collector scope module delegates to the unified policy:

```text
kanda_reasoner_app/reasoner_context_collector/collector_scope.py
```

Important current default exclusion includes:

```text
_project_reference
```

Current GUI preference file contains project-specific rules for developer_tools in:

```text
.reasoner_tools_gui_prefs.json
```

Implementation implication:

```text
The future project_context_bundle box should reuse project_exclusion_policy.py through a read-only adapter.
It should not duplicate Tab 8 rules manually.
```

## 9. Recommended owner box

New feature owner:

```text
kanda_reasoner_app/project_context_bundle/
```

This box should own:

```text
project context resolution
bundle output path resolution
exclusion rules export
file manifest generation
active snapshot generation
validation state capture
bundle manifest generation
bundle checker
bundle zipper
remembered destination adapter
```

This box should not own:

```text
Tab 8 GUI internals
Engineering Safety internals
Project Symbol Atlas complete JSON adapter
Tab 1 architecture validation
Tab 2 workflow validation
Tab 9 prompt library
active governance files
```

## 10. Required cross-box handoffs later

### 10.1 Tab 4 GUI handoff

The new button must appear in Tab 4 next to Run Collector.

Touched likely files:

```text
kanda_reasoner_app/reasoner_tools_shell/runner_help/window_methods_private_impl.py
kanda_reasoner_app/reasoner_tools_gui_shell/main_window_help/window_tool_patches.py
kanda_reasoner_app/reasoner_tools_gui_shell/main_window_help/window_state.py or existing prefs helper if destination is stored there
```

Reason:

```text
The closed-box bundle API needs a GUI trigger.
```

Boundary rule:

```text
Tab 4 GUI should call project_context_bundle APIs; it should not implement bundle logic itself.
```

### 10.2 Evidence path lowercase handoff

Current uppercase evidence paths are shared by multiple boxes.

Touched likely files:

```text
kanda_reasoner_app/project_analysis_evidence_paths.py
kanda_reasoner_app/reasoner_symbol_atlas/evidence_paths.py
Project Symbol Atlas status/freshness tests
Tab 4/Tab 5 evidence path tests
```

Reason:

```text
User made lowercase project_analysis_evidence canonical.
```

This should be a separate focused task before bundle generation becomes official.

### 10.3 Engineering Safety guard

No Engineering Safety behavior change is needed in additive mode, but guard tests are needed.

Reason:

```text
Engineering Safety depends on complete JSON through Project Symbol Atlas.
```

Required guard:

```text
Companion generation must not alter complete.json schema or make the complete JSON adapter select the wrong file.
```

## 11. Findings that change the roadmap

### Finding 1 - Lowercase evidence path is a prerequisite task

Because current source and tests still use PROJECT_ANALYSIS_EVIDENCE, the next code task should not be the full bundle generator yet.

Recommended next task:

```text
JSONCTX002A - Lowercase project_analysis_evidence path contract
```

### Finding 2 - Destructive refresh already clears json_complete and json_splitted

The existing behavior clears both generated-output folders. The future plan should either preserve that exactly or explicitly narrow it. Since the user said to keep the current behavior, the default should be to preserve it.

### Finding 3 - Complete JSON is already rich but Python-only

The current complete JSON includes full Python source in source_file_index, but it does not replace an active project snapshot because it is not an all-active-file manifest.

### Finding 4 - Additive companion files are safe with complete JSON adapter naming

The planned companion filenames do not match the complete JSON adapter's complete-file suffix rules.

### Finding 5 - ZIP export should be separated from Run Collector

This matches user requirement and avoids accidental export of stale or partially generated bundles.

## 12. Updated next-task sequence after audit

### JSONCTX002A - Lowercase project_analysis_evidence path contract

Goal:

```text
Change active project evidence folder casing from PROJECT_ANALYSIS_EVIDENCE to project_analysis_evidence.
```

Must remain dynamic:

```text
<PROJECT_ROOT>/project_analysis_evidence
```

Do not use:

```text
<PROJECT_ROOT>/_project_reference/project_analysis_evidence
```

Focused tests:

```text
test_project_analysis_evidence_paths.py
test_pa007c_tab4_complete_json_output_path.py
test_pa007d_tab5_split_json_output_path.py
test_pa007e_project_analysis_evidence_status.py
test_pa007a_project_analysis_evidence_paths.py
Project Symbol Atlas path tests
```

### JSONCTX002B - Closed-box skeleton

Goal:

```text
Add kanda_reasoner_app/project_context_bundle/ with no Tab 4 GUI integration yet.
```

### JSONCTX003 - Exclusion export

Goal:

```text
Use project_exclusion_policy.py to generate <project_slug>__exclusion_rules.json.
```

### JSONCTX004 - File manifest and active snapshot

Goal:

```text
Generate <project_slug>__file_manifest.json and <project_slug>__active_snapshot.json.
```

### JSONCTX005 - Validation state and bundle manifest

Goal:

```text
Generate <project_slug>__validation_state.json and <project_slug>__bundle_manifest.json.
```

### JSONCTX006 - Run Collector integration

Goal:

```text
Run Collector deletes old generated evidence after confirmation, creates complete JSON, then creates companion JSONs.
```

### JSONCTX007 - Zip and Send to folder

Goal:

```text
Add Tab 4 button, folder picker, remembered destination, bundle ZIP export.
```

## 13. Suggested tests for next implementation stage

Minimum focused tests before touching GUI:

```text
python tests/test_project_analysis_evidence_paths.py
python tests/test_pa007c_tab4_complete_json_output_path.py
python tests/test_pa007d_tab5_split_json_output_path.py
python tests/test_pa007e_project_analysis_evidence_status.py
python tests/test_pa008_complete_json_atlas_adapter.py
```

After project_context_bundle exists:

```text
python tests/test_project_context_bundle_paths.py
python tests/test_project_context_bundle_exclusions.py
python tests/test_project_context_bundle_manifest.py
python tests/test_project_context_bundle_snapshot.py
python tests/test_project_context_bundle_bundle_manifest.py
```

After Tab 4 ZIP button exists:

```text
python tests/test_tab4_ai_context_bundle_button.py
python tests/test_project_context_bundle_zipper.py
```

Global gates after each bundle:

```text
python kanda_reasoner_app/manage_architecture/manage_architecture.py --root <PROJECT_ROOT> --validate
python kanda_reasoner_app/manage_workflows/manage_workflows.py --root <PROJECT_ROOT> --validate
```

## 14. Implementation recommendations

1. Do not edit complete JSON schema.
2. Do not put bundle generation inside Engineering Safety.
3. Do not duplicate Tab 8 exclusion rules.
4. Do not hardcode any root path or drive.
5. Do not generate active evidence under _project_reference.
6. Do not store ZIP export destination globally without project association.
7. Add the ZIP button through Tab 4 GUI integration, but keep all ZIP logic in project_context_bundle.
8. Treat lowercase path migration as the next focused implementation task.

## 15. ASCII map of audited current system

```text
+--------------------------------------------------------------+
| ReasonerToolsWindow outer shell                              |
| reasoner_tools_gui_shell/main_window.py                      |
+-----------------------------+--------------------------------+
                              |
                              v
+--------------------------------------------------------------+
| Collector widget patch wrapper                               |
| main_window_help/window_tool_patches.py                      |
| - patches Run Collector                                      |
| - owns destructive refresh before collector run              |
+-----------------------------+--------------------------------+
                              |
                              v
+--------------------------------------------------------------+
| Output path and delete helpers                               |
| main_window_help/window_output_paths.py                      |
| - json_complete dir                                          |
| - json_splitted dir                                          |
| - reset output dirs                                          |
+-----------------------------+--------------------------------+
                              |
                              v
+--------------------------------------------------------------+
| Embedded CollectorRunnerWindow                               |
| reasoner_tools_shell/runner.py facade -> payload_zp          |
| helper UI: runner_help/window_methods_private_impl.py        |
| helper process: runner_help/window_process_private_impl.py   |
+-----------------------------+--------------------------------+
                              |
                              v
+--------------------------------------------------------------+
| Collector child process                                      |
| runner.py --collector-child                                  |
| calls collector_main.run_collector                           |
+-----------------------------+--------------------------------+
                              |
                              v
+--------------------------------------------------------------+
| Complete JSON generator                                      |
| reasoner_context_collector/collector_main.py        |
| writes <project_slug>__complete.json                         |
+-----------------------------+--------------------------------+
                              |
                              v
+--------------------------------------------------------------+
| Project Analysis Evidence                                    |
| current: <PROJECT_ROOT>/PROJECT_ANALYSIS_EVIDENCE            |
| canonical target: <PROJECT_ROOT>/project_analysis_evidence   |
+--------------------------------------------------------------+
```

## 16. Audit conclusion

JSONCTX001 is complete.

The safest next task is:

```text
JSONCTX002A - Lowercase project_analysis_evidence path contract
```

Reason:

```text
The bundle output path must be canonical before companion JSON generation is added.
Current source and tests still use uppercase PROJECT_ANALYSIS_EVIDENCE.
```

