# Large Module AST Split Audit

Generated: `2026-07-09T22:03:52Z`
Project root: `/mnt/data/runtime_part2_refactor/install_sim`
Target: `kanda_reasoner_app/reasoner_runtime_collector/runtime_runner_help/runtime_runner_part_2_private_impl.py`
Line count: `169`
Audited symbols: `23`

## Refactor safety classification

Label: **SAFE REFACTORING**
Engine: `AST heuristic`
Score: `1`

Hard blockers: `none detected`

Warnings:
- Type annotations may require import preservation in helper modules.

Static tool status:
- Ruff available: `False`
- Ruff used: `False`
- Message: Ruff not requested.

## Candidate islands

### audit_runner

Risk: `low`
Estimated lines: `44`
Methods/symbols:
- `_run_builtin_qt_interaction_scenario`
- `_run_rich_automatic_scenario`
- `_rr__run_builtin_qt_interaction_scenario_impl`
- `_rr__run_rich_automatic_scenario_impl`
- `_rr__run_headless_impl`
- `_run_builtin_collector_component_scenario`
- `_run_entry_script`
- `_run_named_scenario_module`
- `_rr_run_headless_impl`
Self reads: `none`
Self writes: `none`
GUI touches: `none`
Side effects: `none`

### general

Risk: `low`
Estimated lines: `30`
Methods/symbols:
- `_bindings`
- `_rr_RuntimeCollectorWindow__connect_signals_impl`
- `_rr_RuntimeCollectorWindow__append_log_impl`
- `_rr_RuntimeCollectorWindow__start_spinner_impl`
- `_rr_RuntimeCollectorWindow__tick_spinner_impl`
- `_rr_RuntimeCollectorWindow__update_spinner_line_impl`
- `_rr_RuntimeCollectorWindow__stop_spinner_impl`
- `_resolve_headless_config`
- `_ensure_qapplication`
- `_save_prefs`
Self reads: `none`
Self writes: `none`
GUI touches: `none`
Side effects: `none`

### project_root_paths

Risk: `low`
Estimated lines: `12`
Methods/symbols:
- `_bind_root_globals`
- `_rr_RuntimeCollectorWindow__browse_project_root_impl`
- `_rr_RuntimeCollectorWindow__browse_output_json_impl`
Self reads: `none`
Self writes: `none`
GUI touches: `none`
Side effects: `none`

### ui_builder

Risk: `low`
Estimated lines: `3`
Methods/symbols:
- `_rr_RuntimeCollectorWindow__build_ui_impl`
Self reads: `none`
Self writes: `none`
GUI touches: `none`
Side effects: `none`

## Independence matrix

- `audit_runner` x `general`: **independent** - no conflicts detected by AST heuristic
- `audit_runner` x `project_root_paths`: **independent** - no conflicts detected by AST heuristic
- `audit_runner` x `ui_builder`: **independent** - no conflicts detected by AST heuristic
- `general` x `project_root_paths`: **independent** - no conflicts detected by AST heuristic
- `general` x `ui_builder`: **independent** - no conflicts detected by AST heuristic
- `project_root_paths` x `ui_builder`: **independent** - no conflicts detected by AST heuristic

## Recommended patch composition

Mode: `two_island_batch_candidate`
Islands: `audit_runner, general`
Reason: Largest independent non-high-risk pair.

## AI handoff instruction

Use this read-only AST evidence to build the Task 0 candidate-island queue and Task 1 patch-composition decision. Do not implement until AI/human review confirms the islands, independence result, validation gates, and freeze naming.
