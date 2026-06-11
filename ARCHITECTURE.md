# ARCHITECTURE

Generated from `architecture_manifest.json`. This file is a derived view.

## Project Purpose

Structural source of truth for packages, modules, public symbols, helper-group relationships, and dependency directions.

## Package Map

### <root>

| Module | Owns | Exposes | Depends On | Used By | Helper Group |
|---|---|---|---|---|---|
| `` |  |  |  |  |  |
| `_inject_missing_module_docstrings` |  | build_docstring, main |  |  |  |
| `reasoner_tools_gui` |  | main | kanda_reasoner_app.reasoner_tools_gui_shell.launch |  |  |

**Public Symbol Quick Reference**

- `build_docstring` -> `_inject_missing_module_docstrings`

### kanda_reasoner_app

| Module | Owns | Exposes | Depends On | Used By | Helper Group |
|---|---|---|---|---|---|
| `kanda_reasoner_app` |  | PERSISTENCE_HINTS, READ_HINTS, WRITE_HINTS, build_persistence_io_hotspots, build_persistence_io_index, build_persistence_io_summary |  |  |  |
| `kanda_reasoner_app.assert_real_project_static_context_smoke` |  | DEFAULT_JSON_PATH, main |  |  |  |
| `kanda_reasoner_app.collector_persistence_io` |  |  |  |  |  |
| `kanda_reasoner_app.reasoner_tools_gui_validate_manifests` |  | main, validate_manifest |  |  |  |
| `kanda_reasoner_app.run_real_project_static_context_smoke` |  | CURRENT_FILE, DEFAULT_OUTPUT_JSON, DEFAULT_PROJECT_ROOT, PACKAGE_PARENT, main | kanda_reasoner_app.reasoner_context_collector.collector_main |  |  |
| `kanda_reasoner_app.run_static_context_test_suite` |  | CURRENT_FILE, PACKAGE_PARENT, TEST_MODULES, main |  |  |  |

**Public Symbol Quick Reference**

- `DEFAULT_JSON_PATH` -> `kanda_reasoner_app.assert_real_project_static_context_smoke`
- `DEFAULT_OUTPUT_JSON` -> `kanda_reasoner_app.run_real_project_static_context_smoke`
- `DEFAULT_PROJECT_ROOT` -> `kanda_reasoner_app.run_real_project_static_context_smoke`
- `TEST_MODULES` -> `kanda_reasoner_app.run_static_context_test_suite`
- `validate_manifest` -> `kanda_reasoner_app.reasoner_tools_gui_validate_manifests`

### kanda_reasoner_app.backend_payloads

| Module | Owns | Exposes | Depends On | Used By | Helper Group |
|---|---|---|---|---|---|
| `kanda_reasoner_app.backend_payloads` |  |  |  |  |  |
| `kanda_reasoner_app.backend_payloads.loader` |  | load_payload |  | kanda_reasoner_app.insert_missing_docstrings_gui.ai_docstring_generator, kanda_reasoner_app.insert_missing_docstrings_gui.ai_docstring_generator_help.docstring_payloads, kanda_reasoner_app.insert_missing_docstrings_gui.ai_docstring_generator_help.heuristics, kanda_reasoner_app.insert_missing_docstrings_gui.ai_docstring_generator_help.response_parsing, kanda_reasoner_app.insert_missing_docstrings_gui.context_builder, kanda_reasoner_app.insert_missing_docstrings_gui.docstring_validator, kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings, kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui, kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.ai_settings, kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.dialogs, kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.run_controls, kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.window_state, kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.ast_safety, kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.cli, kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.file_processing, kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.heuristic_docstrings, kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.insertion_collector, kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.insertion_formatting, kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.reporting, kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.run_orchestrator, kanda_reasoner_app.insert_missing_docstrings_gui.module_summarizer, kanda_reasoner_app.manage_workflows.manage_workflows_gui, kanda_reasoner_app.manage_workflows.manage_workflows_gui_help.workflow_gui_window, kanda_reasoner_app.project_reasoner_v10.ai_reasoner_main_window, kanda_reasoner_app.project_reasoner_v10.main_window_help.profile_controller, kanda_reasoner_app.project_reasoner_v10.main_window_help.runtime_controller, kanda_reasoner_app.project_reasoner_v10.reasoner_retriever, kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.query_intents, kanda_reasoner_app.reasoner_context_collector.collector_runtime_scenarios, kanda_reasoner_app.reasoner_context_collector.collector_runtime_scenarios_help.event_classification, kanda_reasoner_app.reasoner_context_collector.collector_runtime_scenarios_help.hotspots, kanda_reasoner_app.reasoner_runtime_collector.qt_hooks.qt_connection_monitor, kanda_reasoner_app.reasoner_runtime_collector.runtime_runner, kanda_reasoner_app.reasoner_tools_shell.runner |  |
| `kanda_reasoner_app.backend_payloads.payload_a` |  | PAYLOAD_PARTS_A |  |  |  |
| `kanda_reasoner_app.backend_payloads.payload_b` |  | PAYLOAD_PARTS_B |  |  |  |
| `kanda_reasoner_app.backend_payloads.payload_c` |  | PAYLOAD_PARTS_C |  |  |  |
| `kanda_reasoner_app.backend_payloads.payload_d` |  | PAYLOAD_PARTS_D |  |  |  |
| `kanda_reasoner_app.backend_payloads.payload_e` |  | PAYLOAD_PARTS_E |  |  |  |
| `kanda_reasoner_app.backend_payloads.payload_f` |  | PAYLOAD_PARTS_F |  |  |  |
| `kanda_reasoner_app.backend_payloads.payload_g` |  | PAYLOAD_PARTS_G |  |  |  |
| `kanda_reasoner_app.backend_payloads.payload_h` |  | PAYLOAD_PARTS_H |  |  |  |
| `kanda_reasoner_app.backend_payloads.payload_i` |  | PAYLOAD_PARTS_I |  |  |  |
| `kanda_reasoner_app.backend_payloads.payload_j` |  | PAYLOAD_PARTS_J |  |  |  |
| `kanda_reasoner_app.backend_payloads.payload_k` |  | PAYLOAD_PARTS_K |  |  |  |
| `kanda_reasoner_app.backend_payloads.payload_l` |  | PAYLOAD_PARTS_L |  |  |  |
| `kanda_reasoner_app.backend_payloads.payload_m` |  | PAYLOAD_PARTS_M |  |  |  |
| `kanda_reasoner_app.backend_payloads.payload_n` |  | PAYLOAD_PARTS_N |  |  |  |
| `kanda_reasoner_app.backend_payloads.payload_o` |  | PAYLOAD_PARTS_O |  |  |  |
| `kanda_reasoner_app.backend_payloads.payload_p` |  | PAYLOAD_PARTS_P |  |  |  |
| `kanda_reasoner_app.backend_payloads.payload_q` |  | PAYLOAD_PARTS_Q |  |  |  |
| `kanda_reasoner_app.backend_payloads.payload_r` |  | PAYLOAD_PARTS_R |  |  |  |
| `kanda_reasoner_app.backend_payloads.payload_s` |  | PAYLOAD_PARTS_S |  |  |  |
| `kanda_reasoner_app.backend_payloads.payload_t` |  | PAYLOAD_PARTS_T |  |  |  |
| `kanda_reasoner_app.backend_payloads.payload_u` |  | PAYLOAD_PARTS_U |  |  |  |
| `kanda_reasoner_app.backend_payloads.payload_v` |  | PAYLOAD_PARTS_V |  |  |  |
| `kanda_reasoner_app.backend_payloads.payload_w` |  | PAYLOAD_PARTS_W |  |  |  |
| `kanda_reasoner_app.backend_payloads.payload_y` |  | PAYLOAD_PARTS_Y |  |  |  |
| `kanda_reasoner_app.backend_payloads.payload_z` |  | PAYLOAD_PARTS_Z |  |  |  |
| `kanda_reasoner_app.backend_payloads.payload_za` |  | PAYLOAD_PARTS_ZA |  |  |  |
| `kanda_reasoner_app.backend_payloads.payload_zb` |  | PAYLOAD_PARTS_ZB |  |  |  |
| `kanda_reasoner_app.backend_payloads.payload_zc` |  | PAYLOAD_PARTS_ZC |  |  |  |
| `kanda_reasoner_app.backend_payloads.payload_zd` |  | PAYLOAD_PARTS_ZD |  |  |  |
| `kanda_reasoner_app.backend_payloads.payload_zh` |  | PAYLOAD_PARTS_ZH |  |  |  |
| `kanda_reasoner_app.backend_payloads.payload_zi` |  | PAYLOAD_PARTS_ZI |  |  |  |
| `kanda_reasoner_app.backend_payloads.payload_zj` |  | PAYLOAD_PARTS_ZJ |  |  |  |
| `kanda_reasoner_app.backend_payloads.payload_zm` |  | PAYLOAD_PARTS_ZM |  |  |  |
| `kanda_reasoner_app.backend_payloads.payload_zp` |  | PAYLOAD_PARTS_ZP |  |  |  |

**Public Symbol Quick Reference**

- `PAYLOAD_PARTS_A` -> `kanda_reasoner_app.backend_payloads.payload_a`
- `PAYLOAD_PARTS_B` -> `kanda_reasoner_app.backend_payloads.payload_b`
- `PAYLOAD_PARTS_C` -> `kanda_reasoner_app.backend_payloads.payload_c`
- `PAYLOAD_PARTS_D` -> `kanda_reasoner_app.backend_payloads.payload_d`
- `PAYLOAD_PARTS_E` -> `kanda_reasoner_app.backend_payloads.payload_e`
- `PAYLOAD_PARTS_F` -> `kanda_reasoner_app.backend_payloads.payload_f`
- `PAYLOAD_PARTS_G` -> `kanda_reasoner_app.backend_payloads.payload_g`
- `PAYLOAD_PARTS_H` -> `kanda_reasoner_app.backend_payloads.payload_h`
- `PAYLOAD_PARTS_I` -> `kanda_reasoner_app.backend_payloads.payload_i`
- `PAYLOAD_PARTS_J` -> `kanda_reasoner_app.backend_payloads.payload_j`
- `PAYLOAD_PARTS_K` -> `kanda_reasoner_app.backend_payloads.payload_k`
- `PAYLOAD_PARTS_L` -> `kanda_reasoner_app.backend_payloads.payload_l`
- `PAYLOAD_PARTS_M` -> `kanda_reasoner_app.backend_payloads.payload_m`
- `PAYLOAD_PARTS_N` -> `kanda_reasoner_app.backend_payloads.payload_n`
- `PAYLOAD_PARTS_O` -> `kanda_reasoner_app.backend_payloads.payload_o`
- `PAYLOAD_PARTS_P` -> `kanda_reasoner_app.backend_payloads.payload_p`
- `PAYLOAD_PARTS_Q` -> `kanda_reasoner_app.backend_payloads.payload_q`
- `PAYLOAD_PARTS_R` -> `kanda_reasoner_app.backend_payloads.payload_r`
- `PAYLOAD_PARTS_S` -> `kanda_reasoner_app.backend_payloads.payload_s`
- `PAYLOAD_PARTS_T` -> `kanda_reasoner_app.backend_payloads.payload_t`
- `PAYLOAD_PARTS_U` -> `kanda_reasoner_app.backend_payloads.payload_u`
- `PAYLOAD_PARTS_V` -> `kanda_reasoner_app.backend_payloads.payload_v`
- `PAYLOAD_PARTS_W` -> `kanda_reasoner_app.backend_payloads.payload_w`
- `PAYLOAD_PARTS_Y` -> `kanda_reasoner_app.backend_payloads.payload_y`
- `PAYLOAD_PARTS_Z` -> `kanda_reasoner_app.backend_payloads.payload_z`
- `PAYLOAD_PARTS_ZA` -> `kanda_reasoner_app.backend_payloads.payload_za`
- `PAYLOAD_PARTS_ZB` -> `kanda_reasoner_app.backend_payloads.payload_zb`
- `PAYLOAD_PARTS_ZC` -> `kanda_reasoner_app.backend_payloads.payload_zc`
- `PAYLOAD_PARTS_ZD` -> `kanda_reasoner_app.backend_payloads.payload_zd`
- `PAYLOAD_PARTS_ZH` -> `kanda_reasoner_app.backend_payloads.payload_zh`
- `PAYLOAD_PARTS_ZI` -> `kanda_reasoner_app.backend_payloads.payload_zi`
- `PAYLOAD_PARTS_ZJ` -> `kanda_reasoner_app.backend_payloads.payload_zj`
- `PAYLOAD_PARTS_ZM` -> `kanda_reasoner_app.backend_payloads.payload_zm`
- `PAYLOAD_PARTS_ZP` -> `kanda_reasoner_app.backend_payloads.payload_zp`
- `load_payload` -> `kanda_reasoner_app.backend_payloads.loader`

### kanda_reasoner_app.daily_rfctr_report

| Module | Owns | Exposes | Depends On | Used By | Helper Group |
|---|---|---|---|---|---|
| `kanda_reasoner_app.daily_rfctr_report` |  |  |  |  |  |
| `kanda_reasoner_app.daily_rfctr_report.daily_refactor_report` |  |  | kanda_reasoner_app.daily_rfctr_report.daily_refactor_report_help.source_loader_private_impl |  |  |
| `kanda_reasoner_app.daily_rfctr_report.daily_refactor_report_validate_manifests` |  | BASE_DIR, MANIFEST_PATH, main |  |  |  |

**Public Symbol Quick Reference**

- `BASE_DIR` -> `kanda_reasoner_app.daily_rfctr_report.daily_refactor_report_validate_manifests`
- `MANIFEST_PATH` -> `kanda_reasoner_app.daily_rfctr_report.daily_refactor_report_validate_manifests`
- `main` -> `kanda_reasoner_app.daily_rfctr_report.daily_refactor_report_validate_manifests`

### kanda_reasoner_app.daily_rfctr_report.daily_refactor_report_help

| Module | Owns | Exposes | Depends On | Used By | Helper Group |
|---|---|---|---|---|---|
| `kanda_reasoner_app.daily_rfctr_report.daily_refactor_report_help` |  |  |  |  | daily_refactor_report |
| `kanda_reasoner_app.daily_rfctr_report.daily_refactor_report_help.daily_refactor_report_source_part_10_private_impl` |  | DAILY_REFACTOR_REPORT_SOURCE_PART_10 |  | kanda_reasoner_app.daily_rfctr_report.daily_refactor_report_help.source_loader_private_impl | daily_refactor_report |
| `kanda_reasoner_app.daily_rfctr_report.daily_refactor_report_help.daily_refactor_report_source_part_1_private_impl` |  | DAILY_REFACTOR_REPORT_SOURCE_PART_1 |  | kanda_reasoner_app.daily_rfctr_report.daily_refactor_report_help.source_loader_private_impl | daily_refactor_report |
| `kanda_reasoner_app.daily_rfctr_report.daily_refactor_report_help.daily_refactor_report_source_part_2_private_impl` |  | DAILY_REFACTOR_REPORT_SOURCE_PART_2 |  | kanda_reasoner_app.daily_rfctr_report.daily_refactor_report_help.source_loader_private_impl | daily_refactor_report |
| `kanda_reasoner_app.daily_rfctr_report.daily_refactor_report_help.daily_refactor_report_source_part_3_private_impl` |  | DAILY_REFACTOR_REPORT_SOURCE_PART_3 |  | kanda_reasoner_app.daily_rfctr_report.daily_refactor_report_help.source_loader_private_impl | daily_refactor_report |
| `kanda_reasoner_app.daily_rfctr_report.daily_refactor_report_help.daily_refactor_report_source_part_4_private_impl` |  | DAILY_REFACTOR_REPORT_SOURCE_PART_4 |  | kanda_reasoner_app.daily_rfctr_report.daily_refactor_report_help.source_loader_private_impl | daily_refactor_report |
| `kanda_reasoner_app.daily_rfctr_report.daily_refactor_report_help.daily_refactor_report_source_part_5_private_impl` |  | DAILY_REFACTOR_REPORT_SOURCE_PART_5 |  | kanda_reasoner_app.daily_rfctr_report.daily_refactor_report_help.source_loader_private_impl | daily_refactor_report |
| `kanda_reasoner_app.daily_rfctr_report.daily_refactor_report_help.daily_refactor_report_source_part_6_private_impl` |  | DAILY_REFACTOR_REPORT_SOURCE_PART_6 |  | kanda_reasoner_app.daily_rfctr_report.daily_refactor_report_help.source_loader_private_impl | daily_refactor_report |
| `kanda_reasoner_app.daily_rfctr_report.daily_refactor_report_help.daily_refactor_report_source_part_7_private_impl` |  | DAILY_REFACTOR_REPORT_SOURCE_PART_7 |  | kanda_reasoner_app.daily_rfctr_report.daily_refactor_report_help.source_loader_private_impl | daily_refactor_report |
| `kanda_reasoner_app.daily_rfctr_report.daily_refactor_report_help.daily_refactor_report_source_part_8_private_impl` |  | DAILY_REFACTOR_REPORT_SOURCE_PART_8 |  | kanda_reasoner_app.daily_rfctr_report.daily_refactor_report_help.source_loader_private_impl | daily_refactor_report |
| `kanda_reasoner_app.daily_rfctr_report.daily_refactor_report_help.daily_refactor_report_source_part_9_private_impl` |  | DAILY_REFACTOR_REPORT_SOURCE_PART_9 |  | kanda_reasoner_app.daily_rfctr_report.daily_refactor_report_help.source_loader_private_impl | daily_refactor_report |
| `kanda_reasoner_app.daily_rfctr_report.daily_refactor_report_help.source_loader_private_impl` |  | load_daily_refactor_report_source | kanda_reasoner_app.daily_rfctr_report.daily_refactor_report_help.daily_refactor_report_source_part_10_private_impl, kanda_reasoner_app.daily_rfctr_report.daily_refactor_report_help.daily_refactor_report_source_part_1_private_impl, kanda_reasoner_app.daily_rfctr_report.daily_refactor_report_help.daily_refactor_report_source_part_2_private_impl, kanda_reasoner_app.daily_rfctr_report.daily_refactor_report_help.daily_refactor_report_source_part_3_private_impl, kanda_reasoner_app.daily_rfctr_report.daily_refactor_report_help.daily_refactor_report_source_part_4_private_impl, kanda_reasoner_app.daily_rfctr_report.daily_refactor_report_help.daily_refactor_report_source_part_5_private_impl, kanda_reasoner_app.daily_rfctr_report.daily_refactor_report_help.daily_refactor_report_source_part_6_private_impl, kanda_reasoner_app.daily_rfctr_report.daily_refactor_report_help.daily_refactor_report_source_part_7_private_impl, kanda_reasoner_app.daily_rfctr_report.daily_refactor_report_help.daily_refactor_report_source_part_8_private_impl, kanda_reasoner_app.daily_rfctr_report.daily_refactor_report_help.daily_refactor_report_source_part_9_private_impl | kanda_reasoner_app.daily_rfctr_report.daily_refactor_report | daily_refactor_report |

**Helper Groups**

- `daily_refactor_report` -> main `kanda_reasoner_app.daily_rfctr_report.daily_refactor_report`
  - `kanda_reasoner_app.daily_rfctr_report.daily_refactor_report_help`
  - `kanda_reasoner_app.daily_rfctr_report.daily_refactor_report_help.daily_refactor_report_source_part_10_private_impl`
  - `kanda_reasoner_app.daily_rfctr_report.daily_refactor_report_help.daily_refactor_report_source_part_1_private_impl`
  - `kanda_reasoner_app.daily_rfctr_report.daily_refactor_report_help.daily_refactor_report_source_part_2_private_impl`
  - `kanda_reasoner_app.daily_rfctr_report.daily_refactor_report_help.daily_refactor_report_source_part_3_private_impl`
  - `kanda_reasoner_app.daily_rfctr_report.daily_refactor_report_help.daily_refactor_report_source_part_4_private_impl`
  - `kanda_reasoner_app.daily_rfctr_report.daily_refactor_report_help.daily_refactor_report_source_part_5_private_impl`
  - `kanda_reasoner_app.daily_rfctr_report.daily_refactor_report_help.daily_refactor_report_source_part_6_private_impl`
  - `kanda_reasoner_app.daily_rfctr_report.daily_refactor_report_help.daily_refactor_report_source_part_7_private_impl`
  - `kanda_reasoner_app.daily_rfctr_report.daily_refactor_report_help.daily_refactor_report_source_part_8_private_impl`
  - `kanda_reasoner_app.daily_rfctr_report.daily_refactor_report_help.daily_refactor_report_source_part_9_private_impl`
  - `kanda_reasoner_app.daily_rfctr_report.daily_refactor_report_help.source_loader_private_impl`

**Public Symbol Quick Reference**

- `DAILY_REFACTOR_REPORT_SOURCE_PART_1` -> `kanda_reasoner_app.daily_rfctr_report.daily_refactor_report_help.daily_refactor_report_source_part_1_private_impl`
- `DAILY_REFACTOR_REPORT_SOURCE_PART_10` -> `kanda_reasoner_app.daily_rfctr_report.daily_refactor_report_help.daily_refactor_report_source_part_10_private_impl`
- `DAILY_REFACTOR_REPORT_SOURCE_PART_2` -> `kanda_reasoner_app.daily_rfctr_report.daily_refactor_report_help.daily_refactor_report_source_part_2_private_impl`
- `DAILY_REFACTOR_REPORT_SOURCE_PART_3` -> `kanda_reasoner_app.daily_rfctr_report.daily_refactor_report_help.daily_refactor_report_source_part_3_private_impl`
- `DAILY_REFACTOR_REPORT_SOURCE_PART_4` -> `kanda_reasoner_app.daily_rfctr_report.daily_refactor_report_help.daily_refactor_report_source_part_4_private_impl`
- `DAILY_REFACTOR_REPORT_SOURCE_PART_5` -> `kanda_reasoner_app.daily_rfctr_report.daily_refactor_report_help.daily_refactor_report_source_part_5_private_impl`
- `DAILY_REFACTOR_REPORT_SOURCE_PART_6` -> `kanda_reasoner_app.daily_rfctr_report.daily_refactor_report_help.daily_refactor_report_source_part_6_private_impl`
- `DAILY_REFACTOR_REPORT_SOURCE_PART_7` -> `kanda_reasoner_app.daily_rfctr_report.daily_refactor_report_help.daily_refactor_report_source_part_7_private_impl`
- `DAILY_REFACTOR_REPORT_SOURCE_PART_8` -> `kanda_reasoner_app.daily_rfctr_report.daily_refactor_report_help.daily_refactor_report_source_part_8_private_impl`
- `DAILY_REFACTOR_REPORT_SOURCE_PART_9` -> `kanda_reasoner_app.daily_rfctr_report.daily_refactor_report_help.daily_refactor_report_source_part_9_private_impl`
- `load_daily_refactor_report_source` -> `kanda_reasoner_app.daily_rfctr_report.daily_refactor_report_help.source_loader_private_impl`

### kanda_reasoner_app.insert_missing_docstrings_gui

| Module | Owns | Exposes | Depends On | Used By | Helper Group |
|---|---|---|---|---|---|
| `kanda_reasoner_app.insert_missing_docstrings_gui` |  |  |  |  |  |
| `kanda_reasoner_app.insert_missing_docstrings_gui.ai_config` |  | AIConfig |  |  |  |
| `kanda_reasoner_app.insert_missing_docstrings_gui.ai_docstring_generator` |  | AIDocstringGenerator, GenerationResult, GenerationStats | kanda_reasoner_app.backend_payloads.loader |  |  |
| `kanda_reasoner_app.insert_missing_docstrings_gui.ai_docstring_generator_validate_manifests` |  | main, validate_manifest |  |  |  |
| `kanda_reasoner_app.insert_missing_docstrings_gui.context_builder` |  |  | kanda_reasoner_app.backend_payloads.loader |  |  |
| `kanda_reasoner_app.insert_missing_docstrings_gui.context_builder_validate_manifests` |  | HELP_DIR, HELP_IMPL, HELP_INIT, MANIFEST, ORIGIN, REQUIRED_HEADER_FIELDS, ROOT, main |  |  |  |
| `kanda_reasoner_app.insert_missing_docstrings_gui.docstring_policy` |  | DocstringPolicy |  |  |  |
| `kanda_reasoner_app.insert_missing_docstrings_gui.docstring_validator` |  |  | kanda_reasoner_app.backend_payloads.loader |  |  |
| `kanda_reasoner_app.insert_missing_docstrings_gui.gui_scope_helpers` |  | SCOPE_FULL, SCOPE_MODULE, SCOPE_PACKAGE, is_blank_scope_target, is_test_like_scope_target |  |  |  |
| `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings` |  |  | kanda_reasoner_app.backend_payloads.loader |  |  |
| `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui` |  | DocstringRunWorker, MissingDocstringsWindow, main | kanda_reasoner_app.backend_payloads.loader |  |  |
| `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_validate_manifests` |  | REQUIRED_HEADERS, main, validate_manifest |  |  |  |
| `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_validate_manifests` |  | REQUIRED_HEADER_FIELDS, main |  |  |  |
| `kanda_reasoner_app.insert_missing_docstrings_gui.mode_options_hlp` |  | MODE_OPTIONS_HELP_TEXT, tool_limitations_summary |  |  |  |
| `kanda_reasoner_app.insert_missing_docstrings_gui.module_summarizer` |  |  | kanda_reasoner_app.backend_payloads.loader |  |  |
| `kanda_reasoner_app.insert_missing_docstrings_gui.parallel_runner` |  | FileProcessorFn, FileProgress, RunSummary, run_parallel |  |  |  |

**Public Symbol Quick Reference**

- `AIConfig` -> `kanda_reasoner_app.insert_missing_docstrings_gui.ai_config`
- `AIDocstringGenerator` -> `kanda_reasoner_app.insert_missing_docstrings_gui.ai_docstring_generator`
- `DocstringPolicy` -> `kanda_reasoner_app.insert_missing_docstrings_gui.docstring_policy`
- `DocstringRunWorker` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui`
- `FileProcessorFn` -> `kanda_reasoner_app.insert_missing_docstrings_gui.parallel_runner`
- `FileProgress` -> `kanda_reasoner_app.insert_missing_docstrings_gui.parallel_runner`
- `GenerationResult` -> `kanda_reasoner_app.insert_missing_docstrings_gui.ai_docstring_generator`
- `GenerationStats` -> `kanda_reasoner_app.insert_missing_docstrings_gui.ai_docstring_generator`
- `HELP_DIR` -> `kanda_reasoner_app.insert_missing_docstrings_gui.context_builder_validate_manifests`
- `HELP_IMPL` -> `kanda_reasoner_app.insert_missing_docstrings_gui.context_builder_validate_manifests`
- `HELP_INIT` -> `kanda_reasoner_app.insert_missing_docstrings_gui.context_builder_validate_manifests`
- `MANIFEST` -> `kanda_reasoner_app.insert_missing_docstrings_gui.context_builder_validate_manifests`
- `MODE_OPTIONS_HELP_TEXT` -> `kanda_reasoner_app.insert_missing_docstrings_gui.mode_options_hlp`
- `MissingDocstringsWindow` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui`
- `ORIGIN` -> `kanda_reasoner_app.insert_missing_docstrings_gui.context_builder_validate_manifests`
- `REQUIRED_HEADERS` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_validate_manifests`
- `ROOT` -> `kanda_reasoner_app.insert_missing_docstrings_gui.context_builder_validate_manifests`
- `RunSummary` -> `kanda_reasoner_app.insert_missing_docstrings_gui.parallel_runner`
- `SCOPE_FULL` -> `kanda_reasoner_app.insert_missing_docstrings_gui.gui_scope_helpers`
- `SCOPE_MODULE` -> `kanda_reasoner_app.insert_missing_docstrings_gui.gui_scope_helpers`
- `SCOPE_PACKAGE` -> `kanda_reasoner_app.insert_missing_docstrings_gui.gui_scope_helpers`
- `is_blank_scope_target` -> `kanda_reasoner_app.insert_missing_docstrings_gui.gui_scope_helpers`
- `is_test_like_scope_target` -> `kanda_reasoner_app.insert_missing_docstrings_gui.gui_scope_helpers`
- `run_parallel` -> `kanda_reasoner_app.insert_missing_docstrings_gui.parallel_runner`
- `tool_limitations_summary` -> `kanda_reasoner_app.insert_missing_docstrings_gui.mode_options_hlp`

### kanda_reasoner_app.insert_missing_docstrings_gui.ai_docstring_generator_help

| Module | Owns | Exposes | Depends On | Used By | Helper Group |
|---|---|---|---|---|---|
| `kanda_reasoner_app.insert_missing_docstrings_gui.ai_docstring_generator_help` |  | GenerationResult, GenerationStats | kanda_reasoner_app.insert_missing_docstrings_gui.ai_docstring_generator_help.models |  | ai_docstring_generator |
| `kanda_reasoner_app.insert_missing_docstrings_gui.ai_docstring_generator_help.docstring_payloads` |  |  | kanda_reasoner_app.backend_payloads.loader |  | ai_docstring_generator |
| `kanda_reasoner_app.insert_missing_docstrings_gui.ai_docstring_generator_help.heuristics` |  |  | kanda_reasoner_app.backend_payloads.loader |  | ai_docstring_generator |
| `kanda_reasoner_app.insert_missing_docstrings_gui.ai_docstring_generator_help.models` |  | GenerationResult, GenerationStats |  | kanda_reasoner_app.insert_missing_docstrings_gui.ai_docstring_generator_help | ai_docstring_generator |
| `kanda_reasoner_app.insert_missing_docstrings_gui.ai_docstring_generator_help.response_parsing` |  |  | kanda_reasoner_app.backend_payloads.loader |  | ai_docstring_generator |

**Helper Groups**

- `ai_docstring_generator` -> main `kanda_reasoner_app.insert_missing_docstrings_gui.ai_docstring_generator`
  - `kanda_reasoner_app.insert_missing_docstrings_gui.ai_docstring_generator_help`
  - `kanda_reasoner_app.insert_missing_docstrings_gui.ai_docstring_generator_help.docstring_payloads`
  - `kanda_reasoner_app.insert_missing_docstrings_gui.ai_docstring_generator_help.heuristics`
  - `kanda_reasoner_app.insert_missing_docstrings_gui.ai_docstring_generator_help.models`
  - `kanda_reasoner_app.insert_missing_docstrings_gui.ai_docstring_generator_help.response_parsing`

**Public Symbol Quick Reference**

- `GenerationResult` -> `kanda_reasoner_app.insert_missing_docstrings_gui.ai_docstring_generator_help.models`
- `GenerationStats` -> `kanda_reasoner_app.insert_missing_docstrings_gui.ai_docstring_generator_help.models`

### kanda_reasoner_app.insert_missing_docstrings_gui.context_builder_help

| Module | Owns | Exposes | Depends On | Used By | Helper Group |
|---|---|---|---|---|---|
| `kanda_reasoner_app.insert_missing_docstrings_gui.context_builder_help` |  |  |  |  | context_builder |
| `kanda_reasoner_app.insert_missing_docstrings_gui.context_builder_help.inference_private_impl` |  |  |  |  | context_builder |

**Helper Groups**

- `context_builder` -> main `kanda_reasoner_app.insert_missing_docstrings_gui.context_builder`
  - `kanda_reasoner_app.insert_missing_docstrings_gui.context_builder_help`
  - `kanda_reasoner_app.insert_missing_docstrings_gui.context_builder_help.inference_private_impl`

### kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help

| Module | Owns | Exposes | Depends On | Used By | Helper Group |
|---|---|---|---|---|---|
| `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help` |  |  |  |  | insert_missing_docstrings_gui |
| `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.ai_settings` |  | build_ai_config, load_config_from_file, ollama_tags_url, persist_runtime_config, refresh_models, save_config_to_file | kanda_reasoner_app.backend_payloads.loader |  | insert_missing_docstrings_gui |
| `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.constants` |  | DEFAULT_BASE_URL, DEFAULT_MODEL, DEFAULT_PROJECT_ROOT, DEFAULT_WORKER_NAME |  |  | insert_missing_docstrings_gui |
| `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.dialogs` |  | browse_report_path, browse_root, confirm_write, save_output, show_help | kanda_reasoner_app.backend_payloads.loader |  | insert_missing_docstrings_gui |
| `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.layout_builder` |  | build_ui, set_ai_controls_enabled, wire_events |  |  | insert_missing_docstrings_gui |
| `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.preferences` |  | PREFS_FILENAME, load_prefs, prefs_path, safe_bool, safe_int, safe_text, save_prefs |  |  | insert_missing_docstrings_gui |
| `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.report_review_panel` |  | load_report_rows, matches_review_filter, populate_review_list, refresh_review_summary, review_action_hint_for_row, review_severity_for_row, review_status_for_row, row_needs_review, show_review_item_details |  |  | insert_missing_docstrings_gui |
| `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.run_controls` |  | append_text, cleanup_worker, effective_report_path, handle_worker_error, handle_worker_success, run_mode, run_selected_mode | kanda_reasoner_app.backend_payloads.loader |  | insert_missing_docstrings_gui |
| `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.scope_controls` |  | browse_target_path, effective_target_module, effective_target_package, update_scope_controls |  |  | insert_missing_docstrings_gui |
| `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.tab1_audit_docstring_source` |  | MISSING_DOCSTRING_CODE, TAB1_AUDIT_SOURCE_LABEL, Tab1AuditDocstringSourceResult, Tab1MissingDocstringFinding, extract_missing_docstring_findings, read_missing_docstrings_from_tab1_audit, refresh_tab1_audit_docstring_source, tab1_audit_source_is_enabled |  |  | insert_missing_docstrings_gui |
| `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.tab1_audit_write_contracts` |  | TAB1_AUDIT_WRITE_ROUTE_STATUS_EMPTY, TAB1_AUDIT_WRITE_ROUTE_STATUS_READY, TAB1_AUDIT_WRITE_ROUTE_STATUS_SKIPPED, Tab1AuditWritePlan, Tab1AuditWriteTarget |  |  | insert_missing_docstrings_gui |
| `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.window_state` |  | current_prefs_payload, initialize_window | kanda_reasoner_app.backend_payloads.loader |  | insert_missing_docstrings_gui |
| `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.worker_thread` |  | DocstringRunWorker |  |  | insert_missing_docstrings_gui |

**Helper Groups**

- `insert_missing_docstrings_gui` -> main `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui`
  - `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help`
  - `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.ai_settings`
  - `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.constants`
  - `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.dialogs`
  - `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.layout_builder`
  - `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.preferences`
  - `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.report_review_panel`
  - `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.run_controls`
  - `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.scope_controls`
  - `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.tab1_audit_docstring_source`
  - `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.tab1_audit_write_contracts`
  - `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.window_state`
  - `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.worker_thread`

**Public Symbol Quick Reference**

- `DEFAULT_BASE_URL` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.constants`
- `DEFAULT_MODEL` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.constants`
- `DEFAULT_PROJECT_ROOT` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.constants`
- `DEFAULT_WORKER_NAME` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.constants`
- `DocstringRunWorker` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.worker_thread`
- `MISSING_DOCSTRING_CODE` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.tab1_audit_docstring_source`
- `PREFS_FILENAME` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.preferences`
- `TAB1_AUDIT_SOURCE_LABEL` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.tab1_audit_docstring_source`
- `TAB1_AUDIT_WRITE_ROUTE_STATUS_EMPTY` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.tab1_audit_write_contracts`
- `TAB1_AUDIT_WRITE_ROUTE_STATUS_READY` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.tab1_audit_write_contracts`
- `TAB1_AUDIT_WRITE_ROUTE_STATUS_SKIPPED` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.tab1_audit_write_contracts`
- `Tab1AuditDocstringSourceResult` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.tab1_audit_docstring_source`
- `Tab1AuditWritePlan` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.tab1_audit_write_contracts`
- `Tab1AuditWriteTarget` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.tab1_audit_write_contracts`
- `Tab1MissingDocstringFinding` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.tab1_audit_docstring_source`
- `append_text` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.run_controls`
- `browse_report_path` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.dialogs`
- `browse_root` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.dialogs`
- `browse_target_path` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.scope_controls`
- `build_ai_config` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.ai_settings`
- `build_ui` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.layout_builder`
- `cleanup_worker` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.run_controls`
- `confirm_write` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.dialogs`
- `current_prefs_payload` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.window_state`
- `effective_report_path` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.run_controls`
- `effective_target_module` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.scope_controls`
- `effective_target_package` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.scope_controls`
- `extract_missing_docstring_findings` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.tab1_audit_docstring_source`
- `handle_worker_error` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.run_controls`
- `handle_worker_success` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.run_controls`
- `initialize_window` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.window_state`
- `load_config_from_file` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.ai_settings`
- `load_prefs` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.preferences`
- `load_report_rows` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.report_review_panel`
- `matches_review_filter` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.report_review_panel`
- `ollama_tags_url` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.ai_settings`
- `persist_runtime_config` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.ai_settings`
- `populate_review_list` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.report_review_panel`
- `prefs_path` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.preferences`
- `read_missing_docstrings_from_tab1_audit` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.tab1_audit_docstring_source`
- `refresh_models` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.ai_settings`
- `refresh_review_summary` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.report_review_panel`
- `refresh_tab1_audit_docstring_source` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.tab1_audit_docstring_source`
- `review_action_hint_for_row` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.report_review_panel`
- `review_severity_for_row` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.report_review_panel`
- `review_status_for_row` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.report_review_panel`
- `row_needs_review` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.report_review_panel`
- `run_mode` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.run_controls`
- `run_selected_mode` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.run_controls`
- `safe_bool` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.preferences`
- `safe_int` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.preferences`
- `safe_text` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.preferences`
- `save_config_to_file` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.ai_settings`
- `save_output` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.dialogs`
- `save_prefs` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.preferences`
- `set_ai_controls_enabled` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.layout_builder`
- `show_help` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.dialogs`
- `show_review_item_details` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.report_review_panel`
- `tab1_audit_source_is_enabled` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.tab1_audit_docstring_source`
- `update_scope_controls` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.scope_controls`
- `wire_events` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.layout_builder`

### kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help

| Module | Owns | Exposes | Depends On | Used By | Helper Group |
|---|---|---|---|---|---|
| `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help` |  |  |  |  | insert_missing_docstrings |
| `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.ast_safety` |  | docstring_free_ast_dump, validate_docstring_only_change | kanda_reasoner_app.backend_payloads.loader |  | insert_missing_docstrings |
| `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.cli` |  | build_parser, main | kanda_reasoner_app.backend_payloads.loader |  | insert_missing_docstrings |
| `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.diff_output` |  | diff_text |  |  | insert_missing_docstrings |
| `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.file_processing` |  | collect_changes, load_manifest | kanda_reasoner_app.backend_payloads.loader |  | insert_missing_docstrings |
| `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.heuristic_docstrings` |  | build_class_docstring, build_function_docstring, build_module_docstring, class_summary, function_summary, iter_function_parameters, module_summary | kanda_reasoner_app.backend_payloads.loader |  | insert_missing_docstrings |
| `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.insertion_collector` |  | collect_missing_docstring_insertions | kanda_reasoner_app.backend_payloads.loader |  | insert_missing_docstrings |
| `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.insertion_formatting` |  | apply_insertions_to_text, build_module_header_payload, has_inline_body, indentation_for_body, is_overload_function, module_insert_index, module_path_comment, payload_with_optional_uncertainty, render_docstring_body, wrap_docstring_lines | kanda_reasoner_app.backend_payloads.loader |  | insert_missing_docstrings |
| `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.project_exclusion_rules` |  | is_relaxed_path, is_test_like_path, iter_python_files, iter_selected_python_files, load_project_exclusion_rules, normalize_rel_path, resolve_target_module_path, resolve_target_package_path, should_exclude_path |  |  | insert_missing_docstrings |
| `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.reporting` |  | build_report_row, function_report_kind_and_name, mark_report_rows_for_write_result, print_post_write_verification, result_confidence, result_failure_reason, result_generation_source, result_issues, result_review_action_hint, result_review_severity, result_review_status, result_source, write_report_jsonl | kanda_reasoner_app.backend_payloads.loader |  | insert_missing_docstrings |
| `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.run_orchestrator` |  | run | kanda_reasoner_app.backend_payloads.loader |  | insert_missing_docstrings |
| `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.source_io` |  | UTF8_BOM, parse_source, read_source_text, write_source_text |  |  | insert_missing_docstrings |
| `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.symbol_naming` |  | expr_to_text, extract_internal_import_modules, extract_public_symbols, prettify_name, split_words, to_module_id |  |  | insert_missing_docstrings |

**Helper Groups**

- `insert_missing_docstrings` -> main `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings`
  - `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help`
  - `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.ast_safety`
  - `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.cli`
  - `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.diff_output`
  - `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.file_processing`
  - `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.heuristic_docstrings`
  - `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.insertion_collector`
  - `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.insertion_formatting`
  - `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.project_exclusion_rules`
  - `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.reporting`
  - `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.run_orchestrator`
  - `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.source_io`
  - `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.symbol_naming`

**Public Symbol Quick Reference**

- `UTF8_BOM` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.source_io`
- `apply_insertions_to_text` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.insertion_formatting`
- `build_class_docstring` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.heuristic_docstrings`
- `build_function_docstring` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.heuristic_docstrings`
- `build_module_docstring` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.heuristic_docstrings`
- `build_module_header_payload` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.insertion_formatting`
- `build_parser` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.cli`
- `build_report_row` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.reporting`
- `class_summary` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.heuristic_docstrings`
- `collect_changes` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.file_processing`
- `collect_missing_docstring_insertions` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.insertion_collector`
- `diff_text` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.diff_output`
- `docstring_free_ast_dump` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.ast_safety`
- `expr_to_text` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.symbol_naming`
- `extract_internal_import_modules` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.symbol_naming`
- `extract_public_symbols` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.symbol_naming`
- `function_report_kind_and_name` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.reporting`
- `function_summary` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.heuristic_docstrings`
- `has_inline_body` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.insertion_formatting`
- `indentation_for_body` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.insertion_formatting`
- `is_overload_function` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.insertion_formatting`
- `is_relaxed_path` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.project_exclusion_rules`
- `is_test_like_path` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.project_exclusion_rules`
- `iter_function_parameters` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.heuristic_docstrings`
- `iter_python_files` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.project_exclusion_rules`
- `iter_selected_python_files` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.project_exclusion_rules`
- `load_manifest` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.file_processing`
- `load_project_exclusion_rules` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.project_exclusion_rules`
- `main` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.cli`
- `mark_report_rows_for_write_result` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.reporting`
- `module_insert_index` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.insertion_formatting`
- `module_path_comment` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.insertion_formatting`
- `module_summary` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.heuristic_docstrings`
- `normalize_rel_path` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.project_exclusion_rules`
- `parse_source` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.source_io`
- `payload_with_optional_uncertainty` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.insertion_formatting`
- `prettify_name` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.symbol_naming`
- `print_post_write_verification` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.reporting`
- `read_source_text` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.source_io`
- `render_docstring_body` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.insertion_formatting`
- `resolve_target_module_path` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.project_exclusion_rules`
- `resolve_target_package_path` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.project_exclusion_rules`
- `result_confidence` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.reporting`
- `result_failure_reason` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.reporting`
- `result_generation_source` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.reporting`
- `result_issues` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.reporting`
- `result_review_action_hint` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.reporting`
- `result_review_severity` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.reporting`
- `result_review_status` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.reporting`
- `result_source` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.reporting`
- `run` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.run_orchestrator`
- `should_exclude_path` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.project_exclusion_rules`
- `split_words` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.symbol_naming`
- `to_module_id` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.symbol_naming`
- `validate_docstring_only_change` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.ast_safety`
- `wrap_docstring_lines` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.insertion_formatting`
- `write_report_jsonl` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.reporting`
- `write_source_text` -> `kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.source_io`

### kanda_reasoner_app.json_splitter

| Module | Owns | Exposes | Depends On | Used By | Helper Group |
|---|---|---|---|---|---|
| `kanda_reasoner_app.json_splitter` |  | JsonSplitterWindow, LeafSlot, MAX_FILE_BYTES, MIN_PART_BYTES, PartSpec, SplitPlan, SplitterWorker, build_document_for_spec, collect_container_paths, expand_to_slots, get_entries, get_nested_value, get_wrapper, json_bytes_indented, main, pack_slots, parse_target_path, rebuild_container, set_nested_value, stable_hash |  |  |  |
| `kanda_reasoner_app.json_splitter.json_splitter_8` |  |  | kanda_reasoner_app.json_splitter.json_splitter_8_help.source_loader_private_impl |  |  |
| `kanda_reasoner_app.json_splitter.json_splitter_8_validate_manifests` |  | main |  |  |  |
| `kanda_reasoner_app.json_splitter.json_splitter_chunk_balancing` |  | merge_excess_tail_chunks |  |  |  |
| `kanda_reasoner_app.json_splitter.json_splitter_split_reassemble_validation` |  | CHUNK_SCHEMA, main, stable_hash, validate_split_reassemble_output | kanda_reasoner_app.json_splitter.json_splitter_split_reassemble_validation_help.core |  |  |
| `kanda_reasoner_app.json_splitter.json_splitter_split_reassemble_validation_validate_manifests` |  | ROOT_PUBLIC_API, has_star_import, main, module_all, read_text |  |  |  |
| `kanda_reasoner_app.json_splitter.json_splitter_web_ai_route_manifest` |  | QUESTION_ROUTE_DEFINITIONS, WEB_AI_ROUTE_MANIFEST_SCHEMA, build_web_ai_route_manifest, web_ai_route_manifest_filename |  |  |  |

**Public Symbol Quick Reference**

- `CHUNK_SCHEMA` -> `kanda_reasoner_app.json_splitter.json_splitter_split_reassemble_validation`
- `QUESTION_ROUTE_DEFINITIONS` -> `kanda_reasoner_app.json_splitter.json_splitter_web_ai_route_manifest`
- `ROOT_PUBLIC_API` -> `kanda_reasoner_app.json_splitter.json_splitter_split_reassemble_validation_validate_manifests`
- `WEB_AI_ROUTE_MANIFEST_SCHEMA` -> `kanda_reasoner_app.json_splitter.json_splitter_web_ai_route_manifest`
- `build_web_ai_route_manifest` -> `kanda_reasoner_app.json_splitter.json_splitter_web_ai_route_manifest`
- `has_star_import` -> `kanda_reasoner_app.json_splitter.json_splitter_split_reassemble_validation_validate_manifests`
- `merge_excess_tail_chunks` -> `kanda_reasoner_app.json_splitter.json_splitter_chunk_balancing`
- `module_all` -> `kanda_reasoner_app.json_splitter.json_splitter_split_reassemble_validation_validate_manifests`
- `read_text` -> `kanda_reasoner_app.json_splitter.json_splitter_split_reassemble_validation_validate_manifests`
- `stable_hash` -> `kanda_reasoner_app.json_splitter.json_splitter_split_reassemble_validation`
- `validate_split_reassemble_output` -> `kanda_reasoner_app.json_splitter.json_splitter_split_reassemble_validation`
- `web_ai_route_manifest_filename` -> `kanda_reasoner_app.json_splitter.json_splitter_web_ai_route_manifest`

### kanda_reasoner_app.json_splitter.json_splitter_8_help

| Module | Owns | Exposes | Depends On | Used By | Helper Group |
|---|---|---|---|---|---|
| `kanda_reasoner_app.json_splitter.json_splitter_8_help` |  |  |  |  | json_splitter_8 |
| `kanda_reasoner_app.json_splitter.json_splitter_8_help.source_loader_private_impl` |  | load_json_splitter_8_source | kanda_reasoner_app.json_splitter.json_splitter_8_help.source_part_1_private_impl, kanda_reasoner_app.json_splitter.json_splitter_8_help.source_part_2_private_impl | kanda_reasoner_app.json_splitter.json_splitter_8 | json_splitter_8 |
| `kanda_reasoner_app.json_splitter.json_splitter_8_help.source_part_1_private_impl` |  | SOURCE_PART_1 |  | kanda_reasoner_app.json_splitter.json_splitter_8_help.source_loader_private_impl | json_splitter_8 |
| `kanda_reasoner_app.json_splitter.json_splitter_8_help.source_part_2_private_impl` |  | SOURCE_PART_2 |  | kanda_reasoner_app.json_splitter.json_splitter_8_help.source_loader_private_impl | json_splitter_8 |

**Helper Groups**

- `json_splitter_8` -> main `kanda_reasoner_app.json_splitter.json_splitter_8`
  - `kanda_reasoner_app.json_splitter.json_splitter_8_help`
  - `kanda_reasoner_app.json_splitter.json_splitter_8_help.source_loader_private_impl`
  - `kanda_reasoner_app.json_splitter.json_splitter_8_help.source_part_1_private_impl`
  - `kanda_reasoner_app.json_splitter.json_splitter_8_help.source_part_2_private_impl`

**Public Symbol Quick Reference**

- `SOURCE_PART_1` -> `kanda_reasoner_app.json_splitter.json_splitter_8_help.source_part_1_private_impl`
- `SOURCE_PART_2` -> `kanda_reasoner_app.json_splitter.json_splitter_8_help.source_part_2_private_impl`
- `load_json_splitter_8_source` -> `kanda_reasoner_app.json_splitter.json_splitter_8_help.source_loader_private_impl`

### kanda_reasoner_app.json_splitter.json_splitter_split_reassemble_validation_help

| Module | Owns | Exposes | Depends On | Used By | Helper Group |
|---|---|---|---|---|---|
| `kanda_reasoner_app.json_splitter.json_splitter_split_reassemble_validation_help` |  |  |  |  | json_splitter_split_reassemble_validation |
| `kanda_reasoner_app.json_splitter.json_splitter_split_reassemble_validation_help.core` |  | CHUNK_SCHEMA, stable_hash |  | kanda_reasoner_app.json_splitter.json_splitter_split_reassemble_validation | json_splitter_split_reassemble_validation |

**Helper Groups**

- `json_splitter_split_reassemble_validation` -> main `kanda_reasoner_app.json_splitter.json_splitter_split_reassemble_validation`
  - `kanda_reasoner_app.json_splitter.json_splitter_split_reassemble_validation_help`
  - `kanda_reasoner_app.json_splitter.json_splitter_split_reassemble_validation_help.core`

**Public Symbol Quick Reference**

- `CHUNK_SCHEMA` -> `kanda_reasoner_app.json_splitter.json_splitter_split_reassemble_validation_help.core`
- `stable_hash` -> `kanda_reasoner_app.json_splitter.json_splitter_split_reassemble_validation_help.core`

### kanda_reasoner_app.live_source_verification

| Module | Owns | Exposes | Depends On | Used By | Helper Group |
|---|---|---|---|---|---|
| `kanda_reasoner_app.live_source_verification` |  | DEFAULT_CONTEXT_LINES, DEFAULT_MAX_TEXT_FILE_SIZE_BYTES, LiveSourcePathResult, LiveSourceSnippetResult, batch_verify_sources, extract_live_source_snippet, read_live_source_text, verify_live_source_path |  | kanda_reasoner_app.local_ai_json_enrichment.enrichment_writer, kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.live_source_fallback |  |
| `kanda_reasoner_app.live_source_verification.verifier` |  | LiveSourcePathResult, LiveSourceSnippetResult, batch_verify_sources, extract_live_source_snippet, read_live_source_text, verify_live_source_path |  |  |  |

**Public Symbol Quick Reference**

- `LiveSourcePathResult` -> `kanda_reasoner_app.live_source_verification.verifier`
- `LiveSourceSnippetResult` -> `kanda_reasoner_app.live_source_verification.verifier`
- `batch_verify_sources` -> `kanda_reasoner_app.live_source_verification.verifier`
- `extract_live_source_snippet` -> `kanda_reasoner_app.live_source_verification.verifier`
- `read_live_source_text` -> `kanda_reasoner_app.live_source_verification.verifier`
- `verify_live_source_path` -> `kanda_reasoner_app.live_source_verification.verifier`

### kanda_reasoner_app.local_ai_json_enrichment

| Module | Owns | Exposes | Depends On | Used By | Helper Group |
|---|---|---|---|---|---|
| `kanda_reasoner_app.local_ai_json_enrichment` |  | DEFAULT_ENRICHMENT_KEY, LocalAIJsonEnrichmentResult, enrich_local_ai_json_with_live_sources, load_local_ai_enrichment |  |  |  |
| `kanda_reasoner_app.local_ai_json_enrichment.enrichment_writer` |  | DEFAULT_ENRICHMENT_KEY, LocalAIJsonEnrichmentResult, enrich_local_ai_json_with_live_sources, load_local_ai_enrichment, main | kanda_reasoner_app.live_source_verification, kanda_reasoner_app.local_ai_json_working_copy |  |  |

**Public Symbol Quick Reference**

- `DEFAULT_ENRICHMENT_KEY` -> `kanda_reasoner_app.local_ai_json_enrichment.enrichment_writer`
- `LocalAIJsonEnrichmentResult` -> `kanda_reasoner_app.local_ai_json_enrichment.enrichment_writer`
- `enrich_local_ai_json_with_live_sources` -> `kanda_reasoner_app.local_ai_json_enrichment.enrichment_writer`
- `load_local_ai_enrichment` -> `kanda_reasoner_app.local_ai_json_enrichment.enrichment_writer`
- `main` -> `kanda_reasoner_app.local_ai_json_enrichment.enrichment_writer`

### kanda_reasoner_app.manage_architecture

| Module | Owns | Exposes | Depends On | Used By | Helper Group |
|---|---|---|---|---|---|
| `kanda_reasoner_app.manage_architecture` |  |  |  |  |  |
| `kanda_reasoner_app.manage_architecture.manage_architecture` |  |  | kanda_reasoner_app.manage_architecture.manage_architecture_help.source_loader_private_impl |  |  |
| `kanda_reasoner_app.manage_architecture.manage_architecture_gui` |  | ArchitectureManagerWindow, ArchitectureRunWorker, DEFAULT_MANAGER_NAME, DEFAULT_PROJECT_ROOT, main |  |  |  |
| `kanda_reasoner_app.manage_architecture.manage_architecture_gui_validate_manifests` |  | main, validate_manifest |  |  |  |
| `kanda_reasoner_app.manage_architecture.manage_architecture_validate_manifests` |  | BASE_DIR, MANIFEST_PATH, main |  |  |  |

**Public Symbol Quick Reference**

- `ArchitectureManagerWindow` -> `kanda_reasoner_app.manage_architecture.manage_architecture_gui`
- `ArchitectureRunWorker` -> `kanda_reasoner_app.manage_architecture.manage_architecture_gui`
- `BASE_DIR` -> `kanda_reasoner_app.manage_architecture.manage_architecture_validate_manifests`
- `DEFAULT_MANAGER_NAME` -> `kanda_reasoner_app.manage_architecture.manage_architecture_gui`
- `DEFAULT_PROJECT_ROOT` -> `kanda_reasoner_app.manage_architecture.manage_architecture_gui`
- `MANIFEST_PATH` -> `kanda_reasoner_app.manage_architecture.manage_architecture_validate_manifests`
- `validate_manifest` -> `kanda_reasoner_app.manage_architecture.manage_architecture_gui_validate_manifests`

### kanda_reasoner_app.manage_architecture.manage_architecture_gui_help

| Module | Owns | Exposes | Depends On | Used By | Helper Group |
|---|---|---|---|---|---|
| `kanda_reasoner_app.manage_architecture.manage_architecture_gui_help` |  |  |  |  | manage_architecture_gui |
| `kanda_reasoner_app.manage_architecture.manage_architecture_gui_help.mode_options_hlp` |  | MODE_OPTIONS_HELP_TEXT, mode_help_summary |  |  | manage_architecture_gui |

**Helper Groups**

- `manage_architecture_gui` -> main `kanda_reasoner_app.manage_architecture.manage_architecture_gui`
  - `kanda_reasoner_app.manage_architecture.manage_architecture_gui_help`
  - `kanda_reasoner_app.manage_architecture.manage_architecture_gui_help.mode_options_hlp`

**Public Symbol Quick Reference**

- `MODE_OPTIONS_HELP_TEXT` -> `kanda_reasoner_app.manage_architecture.manage_architecture_gui_help.mode_options_hlp`
- `mode_help_summary` -> `kanda_reasoner_app.manage_architecture.manage_architecture_gui_help.mode_options_hlp`

### kanda_reasoner_app.manage_architecture.manage_architecture_help

| Module | Owns | Exposes | Depends On | Used By | Helper Group |
|---|---|---|---|---|---|
| `kanda_reasoner_app.manage_architecture.manage_architecture_help` |  |  |  |  | manage_architecture |
| `kanda_reasoner_app.manage_architecture.manage_architecture_help.manage_architecture_source_part_10_private_impl` |  | MANAGE_ARCHITECTURE_SOURCE_PART_10 |  | kanda_reasoner_app.manage_architecture.manage_architecture_help.source_loader_private_impl | manage_architecture |
| `kanda_reasoner_app.manage_architecture.manage_architecture_help.manage_architecture_source_part_11_private_impl` |  | MANAGE_ARCHITECTURE_SOURCE_PART_11 |  | kanda_reasoner_app.manage_architecture.manage_architecture_help.source_loader_private_impl | manage_architecture |
| `kanda_reasoner_app.manage_architecture.manage_architecture_help.manage_architecture_source_part_12_private_impl` |  | MANAGE_ARCHITECTURE_SOURCE_PART_12 |  | kanda_reasoner_app.manage_architecture.manage_architecture_help.source_loader_private_impl | manage_architecture |
| `kanda_reasoner_app.manage_architecture.manage_architecture_help.manage_architecture_source_part_13_private_impl` |  | MANAGE_ARCHITECTURE_SOURCE_PART_13 |  | kanda_reasoner_app.manage_architecture.manage_architecture_help.source_loader_private_impl | manage_architecture |
| `kanda_reasoner_app.manage_architecture.manage_architecture_help.manage_architecture_source_part_14_private_impl` |  | MANAGE_ARCHITECTURE_SOURCE_PART_14 |  | kanda_reasoner_app.manage_architecture.manage_architecture_help.source_loader_private_impl | manage_architecture |
| `kanda_reasoner_app.manage_architecture.manage_architecture_help.manage_architecture_source_part_15_private_impl` |  | MANAGE_ARCHITECTURE_SOURCE_PART_15 |  | kanda_reasoner_app.manage_architecture.manage_architecture_help.source_loader_private_impl | manage_architecture |
| `kanda_reasoner_app.manage_architecture.manage_architecture_help.manage_architecture_source_part_16_private_impl` |  | MANAGE_ARCHITECTURE_SOURCE_PART_16 |  | kanda_reasoner_app.manage_architecture.manage_architecture_help.source_loader_private_impl | manage_architecture |
| `kanda_reasoner_app.manage_architecture.manage_architecture_help.manage_architecture_source_part_17_private_impl` |  | MANAGE_ARCHITECTURE_SOURCE_PART_17 |  | kanda_reasoner_app.manage_architecture.manage_architecture_help.source_loader_private_impl | manage_architecture |
| `kanda_reasoner_app.manage_architecture.manage_architecture_help.manage_architecture_source_part_18_private_impl` |  | MANAGE_ARCHITECTURE_SOURCE_PART_18 |  | kanda_reasoner_app.manage_architecture.manage_architecture_help.source_loader_private_impl | manage_architecture |
| `kanda_reasoner_app.manage_architecture.manage_architecture_help.manage_architecture_source_part_19_private_impl` |  | MANAGE_ARCHITECTURE_SOURCE_PART_19 |  | kanda_reasoner_app.manage_architecture.manage_architecture_help.source_loader_private_impl | manage_architecture |
| `kanda_reasoner_app.manage_architecture.manage_architecture_help.manage_architecture_source_part_1_private_impl` |  | MANAGE_ARCHITECTURE_SOURCE_PART_1 |  | kanda_reasoner_app.manage_architecture.manage_architecture_help.source_loader_private_impl | manage_architecture |
| `kanda_reasoner_app.manage_architecture.manage_architecture_help.manage_architecture_source_part_20_private_impl` |  | MANAGE_ARCHITECTURE_SOURCE_PART_20 |  | kanda_reasoner_app.manage_architecture.manage_architecture_help.source_loader_private_impl | manage_architecture |
| `kanda_reasoner_app.manage_architecture.manage_architecture_help.manage_architecture_source_part_21_private_impl` |  | MANAGE_ARCHITECTURE_SOURCE_PART_21 |  | kanda_reasoner_app.manage_architecture.manage_architecture_help.source_loader_private_impl | manage_architecture |
| `kanda_reasoner_app.manage_architecture.manage_architecture_help.manage_architecture_source_part_2_private_impl` |  | MANAGE_ARCHITECTURE_SOURCE_PART_2 |  | kanda_reasoner_app.manage_architecture.manage_architecture_help.source_loader_private_impl | manage_architecture |
| `kanda_reasoner_app.manage_architecture.manage_architecture_help.manage_architecture_source_part_3_private_impl` |  | MANAGE_ARCHITECTURE_SOURCE_PART_3 |  | kanda_reasoner_app.manage_architecture.manage_architecture_help.source_loader_private_impl | manage_architecture |
| `kanda_reasoner_app.manage_architecture.manage_architecture_help.manage_architecture_source_part_4_private_impl` |  | MANAGE_ARCHITECTURE_SOURCE_PART_4 |  | kanda_reasoner_app.manage_architecture.manage_architecture_help.source_loader_private_impl | manage_architecture |
| `kanda_reasoner_app.manage_architecture.manage_architecture_help.manage_architecture_source_part_5_private_impl` |  | MANAGE_ARCHITECTURE_SOURCE_PART_5 |  | kanda_reasoner_app.manage_architecture.manage_architecture_help.source_loader_private_impl | manage_architecture |
| `kanda_reasoner_app.manage_architecture.manage_architecture_help.manage_architecture_source_part_6_private_impl` |  | MANAGE_ARCHITECTURE_SOURCE_PART_6 |  | kanda_reasoner_app.manage_architecture.manage_architecture_help.source_loader_private_impl | manage_architecture |
| `kanda_reasoner_app.manage_architecture.manage_architecture_help.manage_architecture_source_part_7_private_impl` |  | MANAGE_ARCHITECTURE_SOURCE_PART_7 |  | kanda_reasoner_app.manage_architecture.manage_architecture_help.source_loader_private_impl | manage_architecture |
| `kanda_reasoner_app.manage_architecture.manage_architecture_help.manage_architecture_source_part_8_private_impl` |  | MANAGE_ARCHITECTURE_SOURCE_PART_8 |  | kanda_reasoner_app.manage_architecture.manage_architecture_help.source_loader_private_impl | manage_architecture |
| `kanda_reasoner_app.manage_architecture.manage_architecture_help.manage_architecture_source_part_9_private_impl` |  | MANAGE_ARCHITECTURE_SOURCE_PART_9 |  | kanda_reasoner_app.manage_architecture.manage_architecture_help.source_loader_private_impl | manage_architecture |
| `kanda_reasoner_app.manage_architecture.manage_architecture_help.source_loader_private_impl` |  | load_manage_architecture_source | kanda_reasoner_app.manage_architecture.manage_architecture_help.manage_architecture_source_part_10_private_impl, kanda_reasoner_app.manage_architecture.manage_architecture_help.manage_architecture_source_part_11_private_impl, kanda_reasoner_app.manage_architecture.manage_architecture_help.manage_architecture_source_part_12_private_impl, kanda_reasoner_app.manage_architecture.manage_architecture_help.manage_architecture_source_part_13_private_impl, kanda_reasoner_app.manage_architecture.manage_architecture_help.manage_architecture_source_part_14_private_impl, kanda_reasoner_app.manage_architecture.manage_architecture_help.manage_architecture_source_part_15_private_impl, kanda_reasoner_app.manage_architecture.manage_architecture_help.manage_architecture_source_part_16_private_impl, kanda_reasoner_app.manage_architecture.manage_architecture_help.manage_architecture_source_part_17_private_impl, kanda_reasoner_app.manage_architecture.manage_architecture_help.manage_architecture_source_part_18_private_impl, kanda_reasoner_app.manage_architecture.manage_architecture_help.manage_architecture_source_part_19_private_impl, kanda_reasoner_app.manage_architecture.manage_architecture_help.manage_architecture_source_part_1_private_impl, kanda_reasoner_app.manage_architecture.manage_architecture_help.manage_architecture_source_part_20_private_impl, kanda_reasoner_app.manage_architecture.manage_architecture_help.manage_architecture_source_part_21_private_impl, kanda_reasoner_app.manage_architecture.manage_architecture_help.manage_architecture_source_part_2_private_impl, kanda_reasoner_app.manage_architecture.manage_architecture_help.manage_architecture_source_part_3_private_impl, kanda_reasoner_app.manage_architecture.manage_architecture_help.manage_architecture_source_part_4_private_impl, kanda_reasoner_app.manage_architecture.manage_architecture_help.manage_architecture_source_part_5_private_impl, kanda_reasoner_app.manage_architecture.manage_architecture_help.manage_architecture_source_part_6_private_impl, kanda_reasoner_app.manage_architecture.manage_architecture_help.manage_architecture_source_part_7_private_impl, kanda_reasoner_app.manage_architecture.manage_architecture_help.manage_architecture_source_part_8_private_impl, kanda_reasoner_app.manage_architecture.manage_architecture_help.manage_architecture_source_part_9_private_impl | kanda_reasoner_app.manage_architecture.manage_architecture | manage_architecture |

**Helper Groups**

- `manage_architecture` -> main `kanda_reasoner_app.manage_architecture.manage_architecture`
  - `kanda_reasoner_app.manage_architecture.manage_architecture_help`
  - `kanda_reasoner_app.manage_architecture.manage_architecture_help.manage_architecture_source_part_10_private_impl`
  - `kanda_reasoner_app.manage_architecture.manage_architecture_help.manage_architecture_source_part_11_private_impl`
  - `kanda_reasoner_app.manage_architecture.manage_architecture_help.manage_architecture_source_part_12_private_impl`
  - `kanda_reasoner_app.manage_architecture.manage_architecture_help.manage_architecture_source_part_13_private_impl`
  - `kanda_reasoner_app.manage_architecture.manage_architecture_help.manage_architecture_source_part_14_private_impl`
  - `kanda_reasoner_app.manage_architecture.manage_architecture_help.manage_architecture_source_part_15_private_impl`
  - `kanda_reasoner_app.manage_architecture.manage_architecture_help.manage_architecture_source_part_16_private_impl`
  - `kanda_reasoner_app.manage_architecture.manage_architecture_help.manage_architecture_source_part_17_private_impl`
  - `kanda_reasoner_app.manage_architecture.manage_architecture_help.manage_architecture_source_part_18_private_impl`
  - `kanda_reasoner_app.manage_architecture.manage_architecture_help.manage_architecture_source_part_19_private_impl`
  - `kanda_reasoner_app.manage_architecture.manage_architecture_help.manage_architecture_source_part_1_private_impl`
  - `kanda_reasoner_app.manage_architecture.manage_architecture_help.manage_architecture_source_part_20_private_impl`
  - `kanda_reasoner_app.manage_architecture.manage_architecture_help.manage_architecture_source_part_21_private_impl`
  - `kanda_reasoner_app.manage_architecture.manage_architecture_help.manage_architecture_source_part_2_private_impl`
  - `kanda_reasoner_app.manage_architecture.manage_architecture_help.manage_architecture_source_part_3_private_impl`
  - `kanda_reasoner_app.manage_architecture.manage_architecture_help.manage_architecture_source_part_4_private_impl`
  - `kanda_reasoner_app.manage_architecture.manage_architecture_help.manage_architecture_source_part_5_private_impl`
  - `kanda_reasoner_app.manage_architecture.manage_architecture_help.manage_architecture_source_part_6_private_impl`
  - `kanda_reasoner_app.manage_architecture.manage_architecture_help.manage_architecture_source_part_7_private_impl`
  - `kanda_reasoner_app.manage_architecture.manage_architecture_help.manage_architecture_source_part_8_private_impl`
  - `kanda_reasoner_app.manage_architecture.manage_architecture_help.manage_architecture_source_part_9_private_impl`
  - `kanda_reasoner_app.manage_architecture.manage_architecture_help.source_loader_private_impl`

**Public Symbol Quick Reference**

- `MANAGE_ARCHITECTURE_SOURCE_PART_1` -> `kanda_reasoner_app.manage_architecture.manage_architecture_help.manage_architecture_source_part_1_private_impl`
- `MANAGE_ARCHITECTURE_SOURCE_PART_10` -> `kanda_reasoner_app.manage_architecture.manage_architecture_help.manage_architecture_source_part_10_private_impl`
- `MANAGE_ARCHITECTURE_SOURCE_PART_11` -> `kanda_reasoner_app.manage_architecture.manage_architecture_help.manage_architecture_source_part_11_private_impl`
- `MANAGE_ARCHITECTURE_SOURCE_PART_12` -> `kanda_reasoner_app.manage_architecture.manage_architecture_help.manage_architecture_source_part_12_private_impl`
- `MANAGE_ARCHITECTURE_SOURCE_PART_13` -> `kanda_reasoner_app.manage_architecture.manage_architecture_help.manage_architecture_source_part_13_private_impl`
- `MANAGE_ARCHITECTURE_SOURCE_PART_14` -> `kanda_reasoner_app.manage_architecture.manage_architecture_help.manage_architecture_source_part_14_private_impl`
- `MANAGE_ARCHITECTURE_SOURCE_PART_15` -> `kanda_reasoner_app.manage_architecture.manage_architecture_help.manage_architecture_source_part_15_private_impl`
- `MANAGE_ARCHITECTURE_SOURCE_PART_16` -> `kanda_reasoner_app.manage_architecture.manage_architecture_help.manage_architecture_source_part_16_private_impl`
- `MANAGE_ARCHITECTURE_SOURCE_PART_17` -> `kanda_reasoner_app.manage_architecture.manage_architecture_help.manage_architecture_source_part_17_private_impl`
- `MANAGE_ARCHITECTURE_SOURCE_PART_18` -> `kanda_reasoner_app.manage_architecture.manage_architecture_help.manage_architecture_source_part_18_private_impl`
- `MANAGE_ARCHITECTURE_SOURCE_PART_19` -> `kanda_reasoner_app.manage_architecture.manage_architecture_help.manage_architecture_source_part_19_private_impl`
- `MANAGE_ARCHITECTURE_SOURCE_PART_2` -> `kanda_reasoner_app.manage_architecture.manage_architecture_help.manage_architecture_source_part_2_private_impl`
- `MANAGE_ARCHITECTURE_SOURCE_PART_20` -> `kanda_reasoner_app.manage_architecture.manage_architecture_help.manage_architecture_source_part_20_private_impl`
- `MANAGE_ARCHITECTURE_SOURCE_PART_21` -> `kanda_reasoner_app.manage_architecture.manage_architecture_help.manage_architecture_source_part_21_private_impl`
- `MANAGE_ARCHITECTURE_SOURCE_PART_3` -> `kanda_reasoner_app.manage_architecture.manage_architecture_help.manage_architecture_source_part_3_private_impl`
- `MANAGE_ARCHITECTURE_SOURCE_PART_4` -> `kanda_reasoner_app.manage_architecture.manage_architecture_help.manage_architecture_source_part_4_private_impl`
- `MANAGE_ARCHITECTURE_SOURCE_PART_5` -> `kanda_reasoner_app.manage_architecture.manage_architecture_help.manage_architecture_source_part_5_private_impl`
- `MANAGE_ARCHITECTURE_SOURCE_PART_6` -> `kanda_reasoner_app.manage_architecture.manage_architecture_help.manage_architecture_source_part_6_private_impl`
- `MANAGE_ARCHITECTURE_SOURCE_PART_7` -> `kanda_reasoner_app.manage_architecture.manage_architecture_help.manage_architecture_source_part_7_private_impl`
- `MANAGE_ARCHITECTURE_SOURCE_PART_8` -> `kanda_reasoner_app.manage_architecture.manage_architecture_help.manage_architecture_source_part_8_private_impl`
- `MANAGE_ARCHITECTURE_SOURCE_PART_9` -> `kanda_reasoner_app.manage_architecture.manage_architecture_help.manage_architecture_source_part_9_private_impl`
- `load_manage_architecture_source` -> `kanda_reasoner_app.manage_architecture.manage_architecture_help.source_loader_private_impl`

### kanda_reasoner_app.manage_workflows

| Module | Owns | Exposes | Depends On | Used By | Helper Group |
|---|---|---|---|---|---|
| `kanda_reasoner_app.manage_workflows` |  |  |  |  |  |
| `kanda_reasoner_app.manage_workflows.manage_workflows` |  | CheckResult, clear_history, collect_generated_outputs, command_list_results, generate_manifest, generate_workflows_md, get_history_roots, load_manifest_or_default, main, print_history, print_results, run_import_checks, run_tests, scan_project, summarize_results, validate_project | kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_cli, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_command_runner, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_constants, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_generation, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_history, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_import_checks, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_io, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_models, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_project_scan, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_reporting |  |  |
| `kanda_reasoner_app.manage_workflows.manage_workflows_gui` |  | DEFAULT_MANAGER_NAME, WorkflowManagerWindow, WorkflowRunWorker, get_recent_roots, get_recent_scripts, main, record_root, record_script | kanda_reasoner_app.backend_payloads.loader |  |  |
| `kanda_reasoner_app.manage_workflows.manage_workflows_gui_validate_manifests` |  | main, validate_manifest |  |  |  |
| `kanda_reasoner_app.manage_workflows.manage_workflows_validate_manifests` |  | main, validate_manifest |  |  |  |

**Public Symbol Quick Reference**

- `CheckResult` -> `kanda_reasoner_app.manage_workflows.manage_workflows`
- `DEFAULT_MANAGER_NAME` -> `kanda_reasoner_app.manage_workflows.manage_workflows_gui`
- `WorkflowManagerWindow` -> `kanda_reasoner_app.manage_workflows.manage_workflows_gui`
- `WorkflowRunWorker` -> `kanda_reasoner_app.manage_workflows.manage_workflows_gui`
- `clear_history` -> `kanda_reasoner_app.manage_workflows.manage_workflows`
- `collect_generated_outputs` -> `kanda_reasoner_app.manage_workflows.manage_workflows`
- `command_list_results` -> `kanda_reasoner_app.manage_workflows.manage_workflows`
- `generate_manifest` -> `kanda_reasoner_app.manage_workflows.manage_workflows`
- `generate_workflows_md` -> `kanda_reasoner_app.manage_workflows.manage_workflows`
- `get_history_roots` -> `kanda_reasoner_app.manage_workflows.manage_workflows`
- `get_recent_roots` -> `kanda_reasoner_app.manage_workflows.manage_workflows_gui`
- `get_recent_scripts` -> `kanda_reasoner_app.manage_workflows.manage_workflows_gui`
- `load_manifest_or_default` -> `kanda_reasoner_app.manage_workflows.manage_workflows`
- `print_history` -> `kanda_reasoner_app.manage_workflows.manage_workflows`
- `print_results` -> `kanda_reasoner_app.manage_workflows.manage_workflows`
- `record_root` -> `kanda_reasoner_app.manage_workflows.manage_workflows_gui`
- `record_script` -> `kanda_reasoner_app.manage_workflows.manage_workflows_gui`
- `run_import_checks` -> `kanda_reasoner_app.manage_workflows.manage_workflows`
- `run_tests` -> `kanda_reasoner_app.manage_workflows.manage_workflows`
- `scan_project` -> `kanda_reasoner_app.manage_workflows.manage_workflows`
- `summarize_results` -> `kanda_reasoner_app.manage_workflows.manage_workflows`
- `validate_project` -> `kanda_reasoner_app.manage_workflows.manage_workflows`

### kanda_reasoner_app.manage_workflows.manage_workflows_gui_help

| Module | Owns | Exposes | Depends On | Used By | Helper Group |
|---|---|---|---|---|---|
| `kanda_reasoner_app.manage_workflows.manage_workflows_gui_help` |  | WorkflowManagerWindow, WorkflowRunWorker, get_recent_roots, get_recent_scripts, main, record_root, record_script | kanda_reasoner_app.manage_workflows.manage_workflows_gui_help.workflow_gui_history, kanda_reasoner_app.manage_workflows.manage_workflows_gui_help.workflow_gui_window, kanda_reasoner_app.manage_workflows.manage_workflows_gui_help.workflow_gui_worker |  | manage_workflows_gui |
| `kanda_reasoner_app.manage_workflows.manage_workflows_gui_help.workflow_gui_constants` |  |  |  |  | manage_workflows_gui |
| `kanda_reasoner_app.manage_workflows.manage_workflows_gui_help.workflow_gui_history` |  | get_recent_roots, get_recent_scripts, record_root, record_script |  | kanda_reasoner_app.manage_workflows.manage_workflows_gui_help | manage_workflows_gui |
| `kanda_reasoner_app.manage_workflows.manage_workflows_gui_help.workflow_gui_window` |  | WorkflowManagerWindow, main | kanda_reasoner_app.backend_payloads.loader | kanda_reasoner_app.manage_workflows.manage_workflows_gui_help | manage_workflows_gui |
| `kanda_reasoner_app.manage_workflows.manage_workflows_gui_help.workflow_gui_worker` |  | WorkflowRunWorker |  | kanda_reasoner_app.manage_workflows.manage_workflows_gui_help | manage_workflows_gui |

**Helper Groups**

- `manage_workflows_gui` -> main `kanda_reasoner_app.manage_workflows.manage_workflows_gui`
  - `kanda_reasoner_app.manage_workflows.manage_workflows_gui_help`
  - `kanda_reasoner_app.manage_workflows.manage_workflows_gui_help.workflow_gui_constants`
  - `kanda_reasoner_app.manage_workflows.manage_workflows_gui_help.workflow_gui_history`
  - `kanda_reasoner_app.manage_workflows.manage_workflows_gui_help.workflow_gui_window`
  - `kanda_reasoner_app.manage_workflows.manage_workflows_gui_help.workflow_gui_worker`

**Public Symbol Quick Reference**

- `WorkflowManagerWindow` -> `kanda_reasoner_app.manage_workflows.manage_workflows_gui_help.workflow_gui_window`
- `WorkflowRunWorker` -> `kanda_reasoner_app.manage_workflows.manage_workflows_gui_help.workflow_gui_worker`
- `get_recent_roots` -> `kanda_reasoner_app.manage_workflows.manage_workflows_gui_help.workflow_gui_history`
- `get_recent_scripts` -> `kanda_reasoner_app.manage_workflows.manage_workflows_gui_help.workflow_gui_history`
- `main` -> `kanda_reasoner_app.manage_workflows.manage_workflows_gui_help.workflow_gui_window`
- `record_root` -> `kanda_reasoner_app.manage_workflows.manage_workflows_gui_help.workflow_gui_history`
- `record_script` -> `kanda_reasoner_app.manage_workflows.manage_workflows_gui_help.workflow_gui_history`

### kanda_reasoner_app.manage_workflows.manage_workflows_help

| Module | Owns | Exposes | Depends On | Used By | Helper Group |
|---|---|---|---|---|---|
| `kanda_reasoner_app.manage_workflows.manage_workflows_help` |  | CheckResult, DEFAULT_WORKFLOW_DETECTOR_REGISTRY, WorkflowDetector, WorkflowDetectorContext, WorkflowDetectorRegistry, WorkflowIssue, clear_history, collect_generated_outputs, command_list_results, detect_workflow_step_target_integrity, generate_manifest, generate_workflows_md, get_history_roots, load_manifest_or_default, main, print_history, print_results, record_root, register_workflow_detector, run_import_checks, run_tests, run_workflow_detector_results, run_workflow_detectors, scan_project, summarize_results, validate_project, workflow_issue_to_check_result | kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_cli, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_command_runner, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_detector_context, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_detector_registry, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_generation, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_history, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_import_checks, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_issue_models, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_models, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_project_scan, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_reporting, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_step_target_detectors |  | manage_workflows |
| `kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_artifact_route_detectors` |  | detect_workflow_artifact_route_issues | kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_detector_context, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_issue_models |  | manage_workflows |
| `kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_cli` |  | main, run_workflow_detector_results, validate_project | kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_command_runner, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_constants, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_detector_context, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_detector_registry, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_generation, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_history, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_import_checks, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_io, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_issue_models, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_models, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_project_scan, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_reporting | kanda_reasoner_app.manage_workflows.manage_workflows, kanda_reasoner_app.manage_workflows.manage_workflows_help | manage_workflows |
| `kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_command_runner` |  | command_list_results, run_tests | kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_file_contract, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_models, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_output_contract, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_placeholder_contract, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_project_scan | kanda_reasoner_app.manage_workflows.manage_workflows, kanda_reasoner_app.manage_workflows.manage_workflows_help, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_cli | manage_workflows |
| `kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_constants` |  |  |  | kanda_reasoner_app.manage_workflows.manage_workflows, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_cli, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_generation, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_history, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_import_checks, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_io, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_project_scan | manage_workflows |
| `kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_cross_project_generalization_detectors` |  | detect_workflow_cross_project_generalization_issues | kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_detector_context, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_issue_models | kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_detector_registry | manage_workflows |
| `kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_detector_context` |  | WorkflowDetectorContext |  | kanda_reasoner_app.manage_workflows.manage_workflows_help, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_artifact_route_detectors, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_cli, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_cross_project_generalization_detectors, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_detector_registry, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_documentation_drift_detectors, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_environment_contract_detectors, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_idempotency_detectors, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_interaction_contract_detectors, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_reader_ai_contract_detectors, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_rollback_fail_safe_detectors, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_step_order_detectors, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_step_target_detectors, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_structure_detectors, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_validation_reference_detectors | manage_workflows |
| `kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_detector_registry` |  | DEFAULT_WORKFLOW_DETECTOR_REGISTRY, WorkflowDetector, WorkflowDetectorRegistry, register_workflow_detector, run_workflow_detectors | kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_cross_project_generalization_detectors, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_detector_context, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_documentation_drift_detectors, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_environment_contract_detectors, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_idempotency_detectors, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_issue_models, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_reader_ai_contract_detectors, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_rollback_fail_safe_detectors, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_validation_reference_detectors | kanda_reasoner_app.manage_workflows.manage_workflows_help, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_cli | manage_workflows |
| `kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_documentation_drift_detectors` |  | detect_workflow_documentation_drift_issues | kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_detector_context, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_issue_models | kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_detector_registry | manage_workflows |
| `kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_environment_contract_detectors` |  | detect_workflow_environment_contract_issues | kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_detector_context, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_issue_models | kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_detector_registry | manage_workflows |
| `kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_file_contract` |  | validate_expected_json_files, validate_expected_output_files | kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_output_contract, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_structure_detectors | kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_command_runner | manage_workflows |
| `kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_generation` |  | collect_generated_outputs, generate_manifest, generate_workflows_md, load_manifest_or_default | kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_constants, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_io | kanda_reasoner_app.manage_workflows.manage_workflows, kanda_reasoner_app.manage_workflows.manage_workflows_help, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_cli | manage_workflows |
| `kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_history` |  | clear_history, get_history_roots, print_history, record_root | kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_constants | kanda_reasoner_app.manage_workflows.manage_workflows, kanda_reasoner_app.manage_workflows.manage_workflows_help, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_cli | manage_workflows |
| `kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_idempotency_detectors` |  | detect_workflow_idempotency_issues | kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_detector_context, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_issue_models | kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_detector_registry | manage_workflows |
| `kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_import_checks` |  | run_import_checks | kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_constants, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_models | kanda_reasoner_app.manage_workflows.manage_workflows, kanda_reasoner_app.manage_workflows.manage_workflows_help, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_cli | manage_workflows |
| `kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_interaction_contract_detectors` |  | detect_workflow_interaction_contract_issues | kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_detector_context, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_issue_models |  | manage_workflows |
| `kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_io` |  |  | kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_constants | kanda_reasoner_app.manage_workflows.manage_workflows, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_cli, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_generation, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_project_scan | manage_workflows |
| `kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_issue_models` |  | WorkflowIssue, workflow_issue_to_check_result |  | kanda_reasoner_app.manage_workflows.manage_workflows_help, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_artifact_route_detectors, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_cli, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_cross_project_generalization_detectors, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_detector_registry, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_documentation_drift_detectors, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_environment_contract_detectors, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_idempotency_detectors, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_interaction_contract_detectors, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_reader_ai_contract_detectors, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_rollback_fail_safe_detectors, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_step_order_detectors, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_step_target_detectors, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_structure_detectors, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_validation_reference_detectors | manage_workflows |
| `kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_models` |  | CheckResult |  | kanda_reasoner_app.manage_workflows.manage_workflows, kanda_reasoner_app.manage_workflows.manage_workflows_help, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_cli, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_command_runner, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_import_checks, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_reporting | manage_workflows |
| `kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_output_contract` |  | validate_command_output_content |  | kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_command_runner, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_file_contract | manage_workflows |
| `kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_placeholder_contract` |  |  |  | kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_command_runner | manage_workflows |
| `kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_project_scan` |  | scan_project | kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_constants, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_io | kanda_reasoner_app.manage_workflows.manage_workflows, kanda_reasoner_app.manage_workflows.manage_workflows_help, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_cli, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_command_runner | manage_workflows |
| `kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_reader_ai_contract_detectors` |  | detect_workflow_reader_ai_contract_issues | kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_detector_context, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_issue_models | kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_detector_registry | manage_workflows |
| `kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_reporting` |  | print_results, summarize_results | kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_models | kanda_reasoner_app.manage_workflows.manage_workflows, kanda_reasoner_app.manage_workflows.manage_workflows_help, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_cli | manage_workflows |
| `kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_rollback_fail_safe_detectors` |  | detect_workflow_rollback_fail_safe_issues | kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_detector_context, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_issue_models | kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_detector_registry | manage_workflows |
| `kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_step_order_detectors` |  | detect_workflow_step_order_issues | kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_detector_context, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_issue_models |  | manage_workflows |
| `kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_step_target_detectors` |  | detect_workflow_step_target_integrity | kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_detector_context, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_issue_models | kanda_reasoner_app.manage_workflows.manage_workflows_help | manage_workflows |
| `kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_structure_detectors` |  |  | kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_detector_context, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_issue_models | kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_file_contract | manage_workflows |
| `kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_validation_reference_detectors` |  | detect_validation_reference_misroutes | kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_detector_context, kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_issue_models | kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_detector_registry | manage_workflows |

**Helper Groups**

- `manage_workflows` -> main `kanda_reasoner_app.manage_workflows.manage_workflows`
  - `kanda_reasoner_app.manage_workflows.manage_workflows_help`
  - `kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_artifact_route_detectors`
  - `kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_cli`
  - `kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_command_runner`
  - `kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_constants`
  - `kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_cross_project_generalization_detectors`
  - `kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_detector_context`
  - `kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_detector_registry`
  - `kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_documentation_drift_detectors`
  - `kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_environment_contract_detectors`
  - `kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_file_contract`
  - `kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_generation`
  - `kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_history`
  - `kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_idempotency_detectors`
  - `kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_import_checks`
  - `kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_interaction_contract_detectors`
  - `kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_io`
  - `kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_issue_models`
  - `kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_models`
  - `kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_output_contract`
  - `kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_placeholder_contract`
  - `kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_project_scan`
  - `kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_reader_ai_contract_detectors`
  - `kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_reporting`
  - `kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_rollback_fail_safe_detectors`
  - `kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_step_order_detectors`
  - `kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_step_target_detectors`
  - `kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_structure_detectors`
  - `kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_validation_reference_detectors`

**Public Symbol Quick Reference**

- `CheckResult` -> `kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_models`
- `DEFAULT_WORKFLOW_DETECTOR_REGISTRY` -> `kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_detector_registry`
- `WorkflowDetector` -> `kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_detector_registry`
- `WorkflowDetectorContext` -> `kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_detector_context`
- `WorkflowDetectorRegistry` -> `kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_detector_registry`
- `WorkflowIssue` -> `kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_issue_models`
- `clear_history` -> `kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_history`
- `collect_generated_outputs` -> `kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_generation`
- `command_list_results` -> `kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_command_runner`
- `detect_validation_reference_misroutes` -> `kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_validation_reference_detectors`
- `detect_workflow_artifact_route_issues` -> `kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_artifact_route_detectors`
- `detect_workflow_cross_project_generalization_issues` -> `kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_cross_project_generalization_detectors`
- `detect_workflow_documentation_drift_issues` -> `kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_documentation_drift_detectors`
- `detect_workflow_environment_contract_issues` -> `kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_environment_contract_detectors`
- `detect_workflow_idempotency_issues` -> `kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_idempotency_detectors`
- `detect_workflow_interaction_contract_issues` -> `kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_interaction_contract_detectors`
- `detect_workflow_reader_ai_contract_issues` -> `kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_reader_ai_contract_detectors`
- `detect_workflow_rollback_fail_safe_issues` -> `kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_rollback_fail_safe_detectors`
- `detect_workflow_step_order_issues` -> `kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_step_order_detectors`
- `detect_workflow_step_target_integrity` -> `kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_step_target_detectors`
- `generate_manifest` -> `kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_generation`
- `generate_workflows_md` -> `kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_generation`
- `get_history_roots` -> `kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_history`
- `load_manifest_or_default` -> `kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_generation`
- `main` -> `kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_cli`
- `print_history` -> `kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_history`
- `print_results` -> `kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_reporting`
- `record_root` -> `kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_history`
- `register_workflow_detector` -> `kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_detector_registry`
- `run_import_checks` -> `kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_import_checks`
- `run_tests` -> `kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_command_runner`
- `run_workflow_detector_results` -> `kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_cli`
- `run_workflow_detectors` -> `kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_detector_registry`
- `scan_project` -> `kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_project_scan`
- `summarize_results` -> `kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_reporting`
- `validate_command_output_content` -> `kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_output_contract`
- `validate_expected_json_files` -> `kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_file_contract`
- `validate_expected_output_files` -> `kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_file_contract`
- `validate_project` -> `kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_cli`
- `workflow_issue_to_check_result` -> `kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_issue_models`

### kanda_reasoner_app.project_reasoner_v10

| Module | Owns | Exposes | Depends On | Used By | Helper Group |
|---|---|---|---|---|---|
| `kanda_reasoner_app.project_reasoner_v10` |  | AIWorkerBridge, ConversationTurn, EvidenceItem, GENERIC_PROJECT_PROFILE, HELP_INDEX, JsonProjectIndex, JsonProjectReasonerV10, LocalAIReasoner, ProjectProfile, ProjectRetriever, QueryRouteDecision, RetrievalBundle, SymbolEvidenceItem, get_project_profile, infer_project_profile, infer_project_profile_name_from_metadata, iter_project_profiles, main, route_query_intent | kanda_reasoner_app.project_reasoner_v10.ai_bridge, kanda_reasoner_app.project_reasoner_v10.ai_reasoner_main_window, kanda_reasoner_app.project_reasoner_v10.help_index, kanda_reasoner_app.project_reasoner_v10.index_loader, kanda_reasoner_app.project_reasoner_v10.project_profile, kanda_reasoner_app.project_reasoner_v10.query_router, kanda_reasoner_app.project_reasoner_v10.reasoner_retriever, kanda_reasoner_app.project_reasoner_v10.v10_models |  |  |
| `kanda_reasoner_app.project_reasoner_v10.ai_bridge` |  | AIWorkerBridge, LocalAIReasoner | kanda_reasoner_app.project_reasoner_v10.ai_bridge_help.bridge_signals, kanda_reasoner_app.project_reasoner_v10.ai_bridge_help.deterministic_answers, kanda_reasoner_app.project_reasoner_v10.ai_bridge_help.focus_snippets, kanda_reasoner_app.project_reasoner_v10.ai_bridge_help.grounding_checks, kanda_reasoner_app.project_reasoner_v10.ai_bridge_help.prompt_extraction, kanda_reasoner_app.project_reasoner_v10.ai_bridge_help.prompt_modes, kanda_reasoner_app.project_reasoner_v10.v10_qwen_ai_models | kanda_reasoner_app.project_reasoner_v10 |  |
| `kanda_reasoner_app.project_reasoner_v10.ai_bridge_validate_manifests` |  | HEADER_FIELDS, find_manifests, has_ai_context_docstring, helper_files, load_json, main, parse_header_fields, parse_module_exports, validate_manifest |  |  |  |
| `kanda_reasoner_app.project_reasoner_v10.ai_reasoner_main_window` |  |  | kanda_reasoner_app.backend_payloads.loader | kanda_reasoner_app.project_reasoner_v10, kanda_reasoner_app.project_reasoner_v10.run_project_reasoner_v10 |  |
| `kanda_reasoner_app.project_reasoner_v10.ai_reasoner_main_window_validate_manifests` |  | HEADER_FIELDS, main |  |  |  |
| `kanda_reasoner_app.project_reasoner_v10.help_index` |  | HELP_INDEX | kanda_reasoner_app.project_reasoner_v10.help_index_help.help_index_data | kanda_reasoner_app.project_reasoner_v10, kanda_reasoner_app.project_reasoner_v10.main_window_help.ui_components |  |
| `kanda_reasoner_app.project_reasoner_v10.help_index_validate_manifests` |  | main, validate_manifest |  |  |  |
| `kanda_reasoner_app.project_reasoner_v10.index_loader` |  | JsonProjectIndex | kanda_reasoner_app.project_reasoner_v10.index_loader_help.index_builders, kanda_reasoner_app.project_reasoner_v10.index_loader_help.path_resolution, kanda_reasoner_app.project_reasoner_v10.index_loader_help.section_loading, kanda_reasoner_app.project_reasoner_v10.index_loader_help.state_init | kanda_reasoner_app.project_reasoner_v10, kanda_reasoner_app.project_reasoner_v10.v10_static_context_dialog |  |
| `kanda_reasoner_app.project_reasoner_v10.index_loader_validate_manifests` |  | main, validate_manifest |  |  |  |
| `kanda_reasoner_app.project_reasoner_v10.project_profile` |  | ARCHITECTURE_HEAVY_PYTHON_PROJECT_PROFILE, EEG_PROJECT_PROFILE, GENERIC_PROJECT_PROFILE, GENERIC_PYTHON_PROJECT_PROFILE, PROJECT_PROFILES, ProjectProfile, QT_PYTHON_PROJECT_PROFILE, get_project_profile, infer_project_profile, infer_project_profile_name_from_metadata, iter_project_profiles | kanda_reasoner_app.project_reasoner_v10.project_profile_help | kanda_reasoner_app.project_reasoner_v10, kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.profile_support |  |
| `kanda_reasoner_app.project_reasoner_v10.project_profile_validate_manifests` |  | main, validate_manifest |  |  |  |
| `kanda_reasoner_app.project_reasoner_v10.prompt_builder` |  | PROJECT_SCOPE_GUARDRAIL, PromptBuilder, is_which_method_calls_question | kanda_reasoner_app.project_reasoner_v10.prompt_builder_help.answer_style, kanda_reasoner_app.project_reasoner_v10.prompt_builder_help.callsite_evidence, kanda_reasoner_app.project_reasoner_v10.prompt_builder_help.prompt_classification, kanda_reasoner_app.project_reasoner_v10.prompt_builder_help.prompt_sections, kanda_reasoner_app.project_reasoner_v10.prompt_builder_help.widget_registry_section, kanda_reasoner_app.project_reasoner_v10.v10_models |  |  |
| `kanda_reasoner_app.project_reasoner_v10.prompt_builder_validate_manifests` |  | main, validate_manifest |  |  |  |
| `kanda_reasoner_app.project_reasoner_v10.query_router` |  | QueryRouteDecision, is_code_localization_question, is_exact_file_locator_question, is_exact_symbol_locator_question, is_explanatory_question, is_listing_or_discovery_question, is_locator_plus_explanation_question, is_one_line_locator_question, is_responsibility_question, is_signal_or_action_question, is_which_calls_question, is_widget_listing_question, route_query_intent |  | kanda_reasoner_app.project_reasoner_v10, kanda_reasoner_app.project_reasoner_v10.main_window_help.session_service, kanda_reasoner_app.project_reasoner_v10.prompt_builder_help.widget_registry_section |  |
| `kanda_reasoner_app.project_reasoner_v10.reasoner_retriever` |  |  | kanda_reasoner_app.backend_payloads.loader | kanda_reasoner_app.project_reasoner_v10 |  |
| `kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_validate_manifests` |  | HEADER_FIELDS, IGNORED_DIR_NAMES, main |  |  |  |
| `kanda_reasoner_app.project_reasoner_v10.run_project_reasoner_v10` |  |  | kanda_reasoner_app.project_reasoner_v10.ai_reasoner_main_window |  |  |
| `kanda_reasoner_app.project_reasoner_v10.v10_conversation_memory` |  | ConversationMemory | kanda_reasoner_app.project_reasoner_v10.v10_models |  |  |
| `kanda_reasoner_app.project_reasoner_v10.v10_intent_detection` |  | is_explanatory_question, is_which_method_calls_question, norm_text |  |  |  |
| `kanda_reasoner_app.project_reasoner_v10.v10_model_registry` |  | LocalModelRegistry, OLLAMA_MODELS_URL, OLLAMA_TAGS_URL, TIMEOUT |  |  |  |
| `kanda_reasoner_app.project_reasoner_v10.v10_models` |  | ConversationTurn, EvidenceItem, RetrievalBundle, SymbolEvidenceItem |  | kanda_reasoner_app.project_reasoner_v10, kanda_reasoner_app.project_reasoner_v10.main_window_help.answer_presenter, kanda_reasoner_app.project_reasoner_v10.main_window_help.session_service, kanda_reasoner_app.project_reasoner_v10.main_window_help.state_models, kanda_reasoner_app.project_reasoner_v10.prompt_builder, kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.bundle_merge, kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.live_source_fallback, kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.retriever_consensus_private_impl, kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.retriever_routing_private_impl, kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.section_retrieval, kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.snippet_retrieval, kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.symbol_retrieval_evidence_private_impl, kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.symbol_retrieval_retrieve_private_impl, kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.symbol_retrieval_support_private_impl, kanda_reasoner_app.project_reasoner_v10.v10_conversation_memory |  |
| `kanda_reasoner_app.project_reasoner_v10.v10_qwen_ai_models` |  | V9QwenAIModels |  | kanda_reasoner_app.project_reasoner_v10.ai_bridge |  |
| `kanda_reasoner_app.project_reasoner_v10.v10_scoring_config` |  | ScoringConfig |  |  |  |
| `kanda_reasoner_app.project_reasoner_v10.v10_static_context_dialog` |  | StaticContextDialog | kanda_reasoner_app.project_reasoner_v10.index_loader, kanda_reasoner_app.project_reasoner_v10.v10_static_context_inspector_widget | kanda_reasoner_app.project_reasoner_v10.main_window_help.static_context_controller |  |
| `kanda_reasoner_app.project_reasoner_v10.v10_static_context_evidence_formatter` |  | build_static_context_evidence_preview |  | kanda_reasoner_app.project_reasoner_v10.v10_static_context_inspector_widget |  |
| `kanda_reasoner_app.project_reasoner_v10.v10_static_context_inspector_widget` |  | StaticContextInspectorWidget | kanda_reasoner_app.project_reasoner_v10.v10_static_context_evidence_formatter | kanda_reasoner_app.project_reasoner_v10.v10_static_context_dialog |  |

**Public Symbol Quick Reference**

- `AIWorkerBridge` -> `kanda_reasoner_app.project_reasoner_v10.ai_bridge`
- `ARCHITECTURE_HEAVY_PYTHON_PROJECT_PROFILE` -> `kanda_reasoner_app.project_reasoner_v10.project_profile`
- `ConversationMemory` -> `kanda_reasoner_app.project_reasoner_v10.v10_conversation_memory`
- `ConversationTurn` -> `kanda_reasoner_app.project_reasoner_v10.v10_models`
- `EEG_PROJECT_PROFILE` -> `kanda_reasoner_app.project_reasoner_v10.project_profile`
- `EvidenceItem` -> `kanda_reasoner_app.project_reasoner_v10.v10_models`
- `GENERIC_PROJECT_PROFILE` -> `kanda_reasoner_app.project_reasoner_v10.project_profile`
- `GENERIC_PYTHON_PROJECT_PROFILE` -> `kanda_reasoner_app.project_reasoner_v10.project_profile`
- `HELP_INDEX` -> `kanda_reasoner_app.project_reasoner_v10.help_index`
- `IGNORED_DIR_NAMES` -> `kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_validate_manifests`
- `JsonProjectIndex` -> `kanda_reasoner_app.project_reasoner_v10.index_loader`
- `LocalAIReasoner` -> `kanda_reasoner_app.project_reasoner_v10.ai_bridge`
- `LocalModelRegistry` -> `kanda_reasoner_app.project_reasoner_v10.v10_model_registry`
- `OLLAMA_MODELS_URL` -> `kanda_reasoner_app.project_reasoner_v10.v10_model_registry`
- `OLLAMA_TAGS_URL` -> `kanda_reasoner_app.project_reasoner_v10.v10_model_registry`
- `PROJECT_PROFILES` -> `kanda_reasoner_app.project_reasoner_v10.project_profile`
- `PROJECT_SCOPE_GUARDRAIL` -> `kanda_reasoner_app.project_reasoner_v10.prompt_builder`
- `ProjectProfile` -> `kanda_reasoner_app.project_reasoner_v10.project_profile`
- `PromptBuilder` -> `kanda_reasoner_app.project_reasoner_v10.prompt_builder`
- `QT_PYTHON_PROJECT_PROFILE` -> `kanda_reasoner_app.project_reasoner_v10.project_profile`
- `QueryRouteDecision` -> `kanda_reasoner_app.project_reasoner_v10.query_router`
- `RetrievalBundle` -> `kanda_reasoner_app.project_reasoner_v10.v10_models`
- `ScoringConfig` -> `kanda_reasoner_app.project_reasoner_v10.v10_scoring_config`
- `StaticContextDialog` -> `kanda_reasoner_app.project_reasoner_v10.v10_static_context_dialog`
- `StaticContextInspectorWidget` -> `kanda_reasoner_app.project_reasoner_v10.v10_static_context_inspector_widget`
- `SymbolEvidenceItem` -> `kanda_reasoner_app.project_reasoner_v10.v10_models`
- `TIMEOUT` -> `kanda_reasoner_app.project_reasoner_v10.v10_model_registry`
- `V9QwenAIModels` -> `kanda_reasoner_app.project_reasoner_v10.v10_qwen_ai_models`
- `build_static_context_evidence_preview` -> `kanda_reasoner_app.project_reasoner_v10.v10_static_context_evidence_formatter`
- `find_manifests` -> `kanda_reasoner_app.project_reasoner_v10.ai_bridge_validate_manifests`
- `get_project_profile` -> `kanda_reasoner_app.project_reasoner_v10.project_profile`
- `has_ai_context_docstring` -> `kanda_reasoner_app.project_reasoner_v10.ai_bridge_validate_manifests`
- `helper_files` -> `kanda_reasoner_app.project_reasoner_v10.ai_bridge_validate_manifests`
- `infer_project_profile` -> `kanda_reasoner_app.project_reasoner_v10.project_profile`
- `infer_project_profile_name_from_metadata` -> `kanda_reasoner_app.project_reasoner_v10.project_profile`
- `is_code_localization_question` -> `kanda_reasoner_app.project_reasoner_v10.query_router`
- `is_exact_file_locator_question` -> `kanda_reasoner_app.project_reasoner_v10.query_router`
- `is_exact_symbol_locator_question` -> `kanda_reasoner_app.project_reasoner_v10.query_router`
- `is_listing_or_discovery_question` -> `kanda_reasoner_app.project_reasoner_v10.query_router`
- `is_locator_plus_explanation_question` -> `kanda_reasoner_app.project_reasoner_v10.query_router`
- `is_one_line_locator_question` -> `kanda_reasoner_app.project_reasoner_v10.query_router`
- `is_responsibility_question` -> `kanda_reasoner_app.project_reasoner_v10.query_router`
- `is_signal_or_action_question` -> `kanda_reasoner_app.project_reasoner_v10.query_router`
- `is_which_calls_question` -> `kanda_reasoner_app.project_reasoner_v10.query_router`
- `is_widget_listing_question` -> `kanda_reasoner_app.project_reasoner_v10.query_router`
- `iter_project_profiles` -> `kanda_reasoner_app.project_reasoner_v10.project_profile`
- `load_json` -> `kanda_reasoner_app.project_reasoner_v10.ai_bridge_validate_manifests`
- `norm_text` -> `kanda_reasoner_app.project_reasoner_v10.v10_intent_detection`
- `parse_header_fields` -> `kanda_reasoner_app.project_reasoner_v10.ai_bridge_validate_manifests`
- `parse_module_exports` -> `kanda_reasoner_app.project_reasoner_v10.ai_bridge_validate_manifests`
- `route_query_intent` -> `kanda_reasoner_app.project_reasoner_v10.query_router`

### kanda_reasoner_app.project_reasoner_v10.ai_bridge_help

| Module | Owns | Exposes | Depends On | Used By | Helper Group |
|---|---|---|---|---|---|
| `kanda_reasoner_app.project_reasoner_v10.ai_bridge_help` |  |  |  |  | ai_bridge |
| `kanda_reasoner_app.project_reasoner_v10.ai_bridge_help.bridge_signals` |  | AIWorkerBridge |  | kanda_reasoner_app.project_reasoner_v10.ai_bridge | ai_bridge |
| `kanda_reasoner_app.project_reasoner_v10.ai_bridge_help.deterministic_answer_core` |  |  | kanda_reasoner_app.project_reasoner_v10.ai_bridge_help.deterministic_answer_core_parts, kanda_reasoner_app.project_reasoner_v10.ai_bridge_help.deterministic_answer_parts, kanda_reasoner_app.project_reasoner_v10.ai_bridge_help.prompt_extraction, kanda_reasoner_app.project_reasoner_v10.ai_bridge_help.prompt_modes | kanda_reasoner_app.project_reasoner_v10.ai_bridge_help.deterministic_answers | ai_bridge |
| `kanda_reasoner_app.project_reasoner_v10.ai_bridge_help.deterministic_answer_core_parts` |  |  | kanda_reasoner_app.project_reasoner_v10.ai_bridge_help.prompt_extraction, kanda_reasoner_app.project_reasoner_v10.ai_bridge_help.prompt_modes | kanda_reasoner_app.project_reasoner_v10.ai_bridge_help.deterministic_answer_core | ai_bridge |
| `kanda_reasoner_app.project_reasoner_v10.ai_bridge_help.deterministic_answer_parts` |  |  | kanda_reasoner_app.project_reasoner_v10.ai_bridge_help.prompt_extraction, kanda_reasoner_app.project_reasoner_v10.ai_bridge_help.prompt_modes | kanda_reasoner_app.project_reasoner_v10.ai_bridge_help.deterministic_answer_core, kanda_reasoner_app.project_reasoner_v10.ai_bridge_help.deterministic_answers | ai_bridge |
| `kanda_reasoner_app.project_reasoner_v10.ai_bridge_help.deterministic_answers` |  | answer_deterministic_from_prompt, answer_one_line_from_prompt, repair_one_line_symbol_ids, score_file_locator_candidate | kanda_reasoner_app.project_reasoner_v10.ai_bridge_help.deterministic_answer_core, kanda_reasoner_app.project_reasoner_v10.ai_bridge_help.deterministic_answer_parts, kanda_reasoner_app.project_reasoner_v10.ai_bridge_help.prompt_extraction, kanda_reasoner_app.project_reasoner_v10.ai_bridge_help.prompt_modes | kanda_reasoner_app.project_reasoner_v10.ai_bridge | ai_bridge |
| `kanda_reasoner_app.project_reasoner_v10.ai_bridge_help.focus_snippets` |  | build_generative_focus_message, score_snippet_candidate, select_focus_snippets_from_prompt | kanda_reasoner_app.project_reasoner_v10.ai_bridge_help.prompt_extraction, kanda_reasoner_app.project_reasoner_v10.ai_bridge_help.prompt_modes | kanda_reasoner_app.project_reasoner_v10.ai_bridge | ai_bridge |
| `kanda_reasoner_app.project_reasoner_v10.ai_bridge_help.grounding_checks` |  | answer_ignored_required_snippets, grounding_failure_reason, has_forbidden_ids, has_forbidden_paths, has_forbidden_symbols, looks_ungrounded_deterministic, looks_ungrounded_generative, sanitize_invalid_ids | kanda_reasoner_app.project_reasoner_v10.ai_bridge_help.prompt_extraction, kanda_reasoner_app.project_reasoner_v10.ai_bridge_help.prompt_modes | kanda_reasoner_app.project_reasoner_v10.ai_bridge | ai_bridge |
| `kanda_reasoner_app.project_reasoner_v10.ai_bridge_help.prompt_extraction` |  | extract_allowed_file_paths, extract_allowed_ids, extract_allowed_symbols, extract_cited_ids, extract_file_evidence_blocks, extract_file_id_map, extract_file_score_map, extract_locator_target, extract_one_line_triplet, extract_path_like_mentions, extract_runtime_anchors_from_detail, extract_snippet_blocks, extract_snippet_text_blob, extract_symbol_evidence_blocks, extract_symbol_id_map, extract_symbol_like_mentions, extract_symbol_score_map, extract_user_question |  | kanda_reasoner_app.project_reasoner_v10.ai_bridge, kanda_reasoner_app.project_reasoner_v10.ai_bridge_help.deterministic_answer_core, kanda_reasoner_app.project_reasoner_v10.ai_bridge_help.deterministic_answer_core_parts, kanda_reasoner_app.project_reasoner_v10.ai_bridge_help.deterministic_answer_parts, kanda_reasoner_app.project_reasoner_v10.ai_bridge_help.deterministic_answers, kanda_reasoner_app.project_reasoner_v10.ai_bridge_help.focus_snippets, kanda_reasoner_app.project_reasoner_v10.ai_bridge_help.grounding_checks, kanda_reasoner_app.project_reasoner_v10.ai_bridge_help.prompt_modes | ai_bridge |
| `kanda_reasoner_app.project_reasoner_v10.ai_bridge_help.prompt_modes` |  | is_code_localized_prompt, is_deterministic_prompt, is_direct_responsibility_prompt, is_generative_prompt, is_locator_plus_explanation_prompt, is_one_line_prompt, is_runtime_heavy_prompt | kanda_reasoner_app.project_reasoner_v10.ai_bridge_help.prompt_extraction | kanda_reasoner_app.project_reasoner_v10.ai_bridge, kanda_reasoner_app.project_reasoner_v10.ai_bridge_help.deterministic_answer_core, kanda_reasoner_app.project_reasoner_v10.ai_bridge_help.deterministic_answer_core_parts, kanda_reasoner_app.project_reasoner_v10.ai_bridge_help.deterministic_answer_parts, kanda_reasoner_app.project_reasoner_v10.ai_bridge_help.deterministic_answers, kanda_reasoner_app.project_reasoner_v10.ai_bridge_help.focus_snippets, kanda_reasoner_app.project_reasoner_v10.ai_bridge_help.grounding_checks | ai_bridge |

**Helper Groups**

- `ai_bridge` -> main `kanda_reasoner_app.project_reasoner_v10.ai_bridge`
  - `kanda_reasoner_app.project_reasoner_v10.ai_bridge_help`
  - `kanda_reasoner_app.project_reasoner_v10.ai_bridge_help.bridge_signals`
  - `kanda_reasoner_app.project_reasoner_v10.ai_bridge_help.deterministic_answer_core`
  - `kanda_reasoner_app.project_reasoner_v10.ai_bridge_help.deterministic_answer_core_parts`
  - `kanda_reasoner_app.project_reasoner_v10.ai_bridge_help.deterministic_answer_parts`
  - `kanda_reasoner_app.project_reasoner_v10.ai_bridge_help.deterministic_answers`
  - `kanda_reasoner_app.project_reasoner_v10.ai_bridge_help.focus_snippets`
  - `kanda_reasoner_app.project_reasoner_v10.ai_bridge_help.grounding_checks`
  - `kanda_reasoner_app.project_reasoner_v10.ai_bridge_help.prompt_extraction`
  - `kanda_reasoner_app.project_reasoner_v10.ai_bridge_help.prompt_modes`

**Public Symbol Quick Reference**

- `AIWorkerBridge` -> `kanda_reasoner_app.project_reasoner_v10.ai_bridge_help.bridge_signals`
- `answer_deterministic_from_prompt` -> `kanda_reasoner_app.project_reasoner_v10.ai_bridge_help.deterministic_answers`
- `answer_ignored_required_snippets` -> `kanda_reasoner_app.project_reasoner_v10.ai_bridge_help.grounding_checks`
- `answer_one_line_from_prompt` -> `kanda_reasoner_app.project_reasoner_v10.ai_bridge_help.deterministic_answers`
- `build_generative_focus_message` -> `kanda_reasoner_app.project_reasoner_v10.ai_bridge_help.focus_snippets`
- `extract_allowed_file_paths` -> `kanda_reasoner_app.project_reasoner_v10.ai_bridge_help.prompt_extraction`
- `extract_allowed_ids` -> `kanda_reasoner_app.project_reasoner_v10.ai_bridge_help.prompt_extraction`
- `extract_allowed_symbols` -> `kanda_reasoner_app.project_reasoner_v10.ai_bridge_help.prompt_extraction`
- `extract_cited_ids` -> `kanda_reasoner_app.project_reasoner_v10.ai_bridge_help.prompt_extraction`
- `extract_file_evidence_blocks` -> `kanda_reasoner_app.project_reasoner_v10.ai_bridge_help.prompt_extraction`
- `extract_file_id_map` -> `kanda_reasoner_app.project_reasoner_v10.ai_bridge_help.prompt_extraction`
- `extract_file_score_map` -> `kanda_reasoner_app.project_reasoner_v10.ai_bridge_help.prompt_extraction`
- `extract_locator_target` -> `kanda_reasoner_app.project_reasoner_v10.ai_bridge_help.prompt_extraction`
- `extract_one_line_triplet` -> `kanda_reasoner_app.project_reasoner_v10.ai_bridge_help.prompt_extraction`
- `extract_path_like_mentions` -> `kanda_reasoner_app.project_reasoner_v10.ai_bridge_help.prompt_extraction`
- `extract_runtime_anchors_from_detail` -> `kanda_reasoner_app.project_reasoner_v10.ai_bridge_help.prompt_extraction`
- `extract_snippet_blocks` -> `kanda_reasoner_app.project_reasoner_v10.ai_bridge_help.prompt_extraction`
- `extract_snippet_text_blob` -> `kanda_reasoner_app.project_reasoner_v10.ai_bridge_help.prompt_extraction`
- `extract_symbol_evidence_blocks` -> `kanda_reasoner_app.project_reasoner_v10.ai_bridge_help.prompt_extraction`
- `extract_symbol_id_map` -> `kanda_reasoner_app.project_reasoner_v10.ai_bridge_help.prompt_extraction`
- `extract_symbol_like_mentions` -> `kanda_reasoner_app.project_reasoner_v10.ai_bridge_help.prompt_extraction`
- `extract_symbol_score_map` -> `kanda_reasoner_app.project_reasoner_v10.ai_bridge_help.prompt_extraction`
- `extract_user_question` -> `kanda_reasoner_app.project_reasoner_v10.ai_bridge_help.prompt_extraction`
- `grounding_failure_reason` -> `kanda_reasoner_app.project_reasoner_v10.ai_bridge_help.grounding_checks`
- `has_forbidden_ids` -> `kanda_reasoner_app.project_reasoner_v10.ai_bridge_help.grounding_checks`
- `has_forbidden_paths` -> `kanda_reasoner_app.project_reasoner_v10.ai_bridge_help.grounding_checks`
- `has_forbidden_symbols` -> `kanda_reasoner_app.project_reasoner_v10.ai_bridge_help.grounding_checks`
- `is_code_localized_prompt` -> `kanda_reasoner_app.project_reasoner_v10.ai_bridge_help.prompt_modes`
- `is_deterministic_prompt` -> `kanda_reasoner_app.project_reasoner_v10.ai_bridge_help.prompt_modes`
- `is_direct_responsibility_prompt` -> `kanda_reasoner_app.project_reasoner_v10.ai_bridge_help.prompt_modes`
- `is_generative_prompt` -> `kanda_reasoner_app.project_reasoner_v10.ai_bridge_help.prompt_modes`
- `is_locator_plus_explanation_prompt` -> `kanda_reasoner_app.project_reasoner_v10.ai_bridge_help.prompt_modes`
- `is_one_line_prompt` -> `kanda_reasoner_app.project_reasoner_v10.ai_bridge_help.prompt_modes`
- `is_runtime_heavy_prompt` -> `kanda_reasoner_app.project_reasoner_v10.ai_bridge_help.prompt_modes`
- `looks_ungrounded_deterministic` -> `kanda_reasoner_app.project_reasoner_v10.ai_bridge_help.grounding_checks`
- `looks_ungrounded_generative` -> `kanda_reasoner_app.project_reasoner_v10.ai_bridge_help.grounding_checks`
- `repair_one_line_symbol_ids` -> `kanda_reasoner_app.project_reasoner_v10.ai_bridge_help.deterministic_answers`
- `sanitize_invalid_ids` -> `kanda_reasoner_app.project_reasoner_v10.ai_bridge_help.grounding_checks`
- `score_file_locator_candidate` -> `kanda_reasoner_app.project_reasoner_v10.ai_bridge_help.deterministic_answers`
- `score_snippet_candidate` -> `kanda_reasoner_app.project_reasoner_v10.ai_bridge_help.focus_snippets`
- `select_focus_snippets_from_prompt` -> `kanda_reasoner_app.project_reasoner_v10.ai_bridge_help.focus_snippets`

### kanda_reasoner_app.project_reasoner_v10.core

| Module | Owns | Exposes | Depends On | Used By | Helper Group |
|---|---|---|---|---|---|
| `kanda_reasoner_app.project_reasoner_v10.core` |  | SECTION_PRIORITY_BY_QUERY_KIND, get_section_priority, normalize_query_kind | kanda_reasoner_app.project_reasoner_v10.core.retrieval_section_priorities |  |  |
| `kanda_reasoner_app.project_reasoner_v10.core.retrieval_section_priorities` |  | SECTION_PRIORITY_BY_QUERY_KIND, get_section_priority, normalize_query_kind |  | kanda_reasoner_app.project_reasoner_v10.core |  |

**Public Symbol Quick Reference**

- `SECTION_PRIORITY_BY_QUERY_KIND` -> `kanda_reasoner_app.project_reasoner_v10.core.retrieval_section_priorities`
- `get_section_priority` -> `kanda_reasoner_app.project_reasoner_v10.core.retrieval_section_priorities`
- `normalize_query_kind` -> `kanda_reasoner_app.project_reasoner_v10.core.retrieval_section_priorities`

### kanda_reasoner_app.project_reasoner_v10.help_index_help

| Module | Owns | Exposes | Depends On | Used By | Helper Group |
|---|---|---|---|---|---|
| `kanda_reasoner_app.project_reasoner_v10.help_index_help` |  | HELP_INDEX | kanda_reasoner_app.project_reasoner_v10.help_index_help.help_index_data |  | help_index |
| `kanda_reasoner_app.project_reasoner_v10.help_index_help.help_index_data` |  | HELP_INDEX | kanda_reasoner_app.project_reasoner_v10.help_index_help.help_index_normalization, kanda_reasoner_app.project_reasoner_v10.help_index_help.help_index_raw | kanda_reasoner_app.project_reasoner_v10.help_index, kanda_reasoner_app.project_reasoner_v10.help_index_help | help_index |
| `kanda_reasoner_app.project_reasoner_v10.help_index_help.help_index_normalization` |  | normalize_help_payload, normalize_help_text |  | kanda_reasoner_app.project_reasoner_v10.help_index_help.help_index_data | help_index |
| `kanda_reasoner_app.project_reasoner_v10.help_index_help.help_index_raw` |  | RAW_HELP_INDEX | kanda_reasoner_app.project_reasoner_v10.help_index_help.help_index_raw_parts.raw_part_1_private_impl, kanda_reasoner_app.project_reasoner_v10.help_index_help.help_index_raw_parts.raw_part_2_private_impl | kanda_reasoner_app.project_reasoner_v10.help_index_help.help_index_data | help_index |

**Helper Groups**

- `help_index` -> main `kanda_reasoner_app.project_reasoner_v10.help_index`
  - `kanda_reasoner_app.project_reasoner_v10.help_index_help`
  - `kanda_reasoner_app.project_reasoner_v10.help_index_help.help_index_data`
  - `kanda_reasoner_app.project_reasoner_v10.help_index_help.help_index_normalization`
  - `kanda_reasoner_app.project_reasoner_v10.help_index_help.help_index_raw`

**Public Symbol Quick Reference**

- `HELP_INDEX` -> `kanda_reasoner_app.project_reasoner_v10.help_index_help.help_index_data`
- `RAW_HELP_INDEX` -> `kanda_reasoner_app.project_reasoner_v10.help_index_help.help_index_raw`
- `normalize_help_payload` -> `kanda_reasoner_app.project_reasoner_v10.help_index_help.help_index_normalization`
- `normalize_help_text` -> `kanda_reasoner_app.project_reasoner_v10.help_index_help.help_index_normalization`

### kanda_reasoner_app.project_reasoner_v10.help_index_help.help_index_raw_parts

| Module | Owns | Exposes | Depends On | Used By | Helper Group |
|---|---|---|---|---|---|
| `kanda_reasoner_app.project_reasoner_v10.help_index_help.help_index_raw_parts` |  |  |  |  |  |
| `kanda_reasoner_app.project_reasoner_v10.help_index_help.help_index_raw_parts.raw_part_1_private_impl` |  |  |  | kanda_reasoner_app.project_reasoner_v10.help_index_help.help_index_raw |  |
| `kanda_reasoner_app.project_reasoner_v10.help_index_help.help_index_raw_parts.raw_part_2_private_impl` |  |  |  | kanda_reasoner_app.project_reasoner_v10.help_index_help.help_index_raw |  |

### kanda_reasoner_app.project_reasoner_v10.index_loader_help

| Module | Owns | Exposes | Depends On | Used By | Helper Group |
|---|---|---|---|---|---|
| `kanda_reasoner_app.project_reasoner_v10.index_loader_help` |  | build_boundary_indexes, build_core_file_and_symbol_indexes, build_hotspot_indexes, build_import_and_call_graph_indexes, build_runtime_indexes, build_snippet_lookup_index, build_ui_action_indexes, build_widget_indexes, initialize_index_state, load_full_sections, rebuild_indexes, resolve_runtime_source_file | kanda_reasoner_app.project_reasoner_v10.index_loader_help.index_builders, kanda_reasoner_app.project_reasoner_v10.index_loader_help.path_resolution, kanda_reasoner_app.project_reasoner_v10.index_loader_help.section_loading, kanda_reasoner_app.project_reasoner_v10.index_loader_help.state_init |  | index_loader |
| `kanda_reasoner_app.project_reasoner_v10.index_loader_help.index_builders` |  | build_boundary_indexes, build_core_file_and_symbol_indexes, build_hotspot_indexes, build_import_and_call_graph_indexes, build_runtime_indexes, build_snippet_lookup_index, build_ui_action_indexes, build_widget_indexes |  | kanda_reasoner_app.project_reasoner_v10.index_loader, kanda_reasoner_app.project_reasoner_v10.index_loader_help | index_loader |
| `kanda_reasoner_app.project_reasoner_v10.index_loader_help.path_resolution` |  | resolve_runtime_source_file |  | kanda_reasoner_app.project_reasoner_v10.index_loader, kanda_reasoner_app.project_reasoner_v10.index_loader_help | index_loader |
| `kanda_reasoner_app.project_reasoner_v10.index_loader_help.section_loading` |  | load_full_sections |  | kanda_reasoner_app.project_reasoner_v10.index_loader, kanda_reasoner_app.project_reasoner_v10.index_loader_help | index_loader |
| `kanda_reasoner_app.project_reasoner_v10.index_loader_help.state_init` |  | initialize_index_state |  | kanda_reasoner_app.project_reasoner_v10.index_loader, kanda_reasoner_app.project_reasoner_v10.index_loader_help | index_loader |

**Helper Groups**

- `index_loader` -> main `kanda_reasoner_app.project_reasoner_v10.index_loader`
  - `kanda_reasoner_app.project_reasoner_v10.index_loader_help`
  - `kanda_reasoner_app.project_reasoner_v10.index_loader_help.index_builders`
  - `kanda_reasoner_app.project_reasoner_v10.index_loader_help.path_resolution`
  - `kanda_reasoner_app.project_reasoner_v10.index_loader_help.section_loading`
  - `kanda_reasoner_app.project_reasoner_v10.index_loader_help.state_init`

**Public Symbol Quick Reference**

- `build_boundary_indexes` -> `kanda_reasoner_app.project_reasoner_v10.index_loader_help.index_builders`
- `build_core_file_and_symbol_indexes` -> `kanda_reasoner_app.project_reasoner_v10.index_loader_help.index_builders`
- `build_hotspot_indexes` -> `kanda_reasoner_app.project_reasoner_v10.index_loader_help.index_builders`
- `build_import_and_call_graph_indexes` -> `kanda_reasoner_app.project_reasoner_v10.index_loader_help.index_builders`
- `build_runtime_indexes` -> `kanda_reasoner_app.project_reasoner_v10.index_loader_help.index_builders`
- `build_snippet_lookup_index` -> `kanda_reasoner_app.project_reasoner_v10.index_loader_help.index_builders`
- `build_ui_action_indexes` -> `kanda_reasoner_app.project_reasoner_v10.index_loader_help.index_builders`
- `build_widget_indexes` -> `kanda_reasoner_app.project_reasoner_v10.index_loader_help.index_builders`
- `initialize_index_state` -> `kanda_reasoner_app.project_reasoner_v10.index_loader_help.state_init`
- `load_full_sections` -> `kanda_reasoner_app.project_reasoner_v10.index_loader_help.section_loading`
- `resolve_runtime_source_file` -> `kanda_reasoner_app.project_reasoner_v10.index_loader_help.path_resolution`

### kanda_reasoner_app.project_reasoner_v10.main_window_help

| Module | Owns | Exposes | Depends On | Used By | Helper Group |
|---|---|---|---|---|---|
| `kanda_reasoner_app.project_reasoner_v10.main_window_help` |  |  |  |  | main_window |
| `kanda_reasoner_app.project_reasoner_v10.main_window_help.analysis_controller` |  | AnalysisController | kanda_reasoner_app.project_reasoner_v10.main_window_help.ui_components |  | main_window |
| `kanda_reasoner_app.project_reasoner_v10.main_window_help.answer_presenter` |  | AnswerPresenter, ConfidenceStatus | kanda_reasoner_app.project_reasoner_v10.main_window_help.ui_components, kanda_reasoner_app.project_reasoner_v10.v10_models |  | main_window |
| `kanda_reasoner_app.project_reasoner_v10.main_window_help.json_track` |  | CANONICAL_COMPLETE_JSON_NAME, LOCAL_AI_COMPLETE_JSON_NAME, classify_loaded_json_track |  |  | main_window |
| `kanda_reasoner_app.project_reasoner_v10.main_window_help.profile_controller` |  |  | kanda_reasoner_app.backend_payloads.loader |  | main_window |
| `kanda_reasoner_app.project_reasoner_v10.main_window_help.runtime_controller` |  |  | kanda_reasoner_app.backend_payloads.loader |  | main_window |
| `kanda_reasoner_app.project_reasoner_v10.main_window_help.session_service` |  | SessionExecutionError, SessionExecutionResult, SessionService | kanda_reasoner_app.project_reasoner_v10.query_router, kanda_reasoner_app.project_reasoner_v10.v10_models |  | main_window |
| `kanda_reasoner_app.project_reasoner_v10.main_window_help.settings_manager` |  | WindowSettingsManager |  |  | main_window |
| `kanda_reasoner_app.project_reasoner_v10.main_window_help.signal_wiring` |  | connect_main_window_signals |  |  | main_window |
| `kanda_reasoner_app.project_reasoner_v10.main_window_help.state_models` |  | AnalysisState, ProfileSelectionState, WindowSessionState | kanda_reasoner_app.project_reasoner_v10.v10_models |  | main_window |
| `kanda_reasoner_app.project_reasoner_v10.main_window_help.static_context_controller` |  | StaticContextController | kanda_reasoner_app.project_reasoner_v10.v10_static_context_dialog |  | main_window |
| `kanda_reasoner_app.project_reasoner_v10.main_window_help.ui_builder` |  | build_main_window_ui |  |  | main_window |
| `kanda_reasoner_app.project_reasoner_v10.main_window_help.ui_components` |  | CopyableListWidget, HelpDialog, shorten_path | kanda_reasoner_app.project_reasoner_v10.help_index | kanda_reasoner_app.project_reasoner_v10.main_window_help.analysis_controller, kanda_reasoner_app.project_reasoner_v10.main_window_help.answer_presenter | main_window |

**Helper Groups**

- `main_window` -> main `None`
  - `kanda_reasoner_app.project_reasoner_v10.main_window_help`
  - `kanda_reasoner_app.project_reasoner_v10.main_window_help.analysis_controller`
  - `kanda_reasoner_app.project_reasoner_v10.main_window_help.answer_presenter`
  - `kanda_reasoner_app.project_reasoner_v10.main_window_help.json_track`
  - `kanda_reasoner_app.project_reasoner_v10.main_window_help.profile_controller`
  - `kanda_reasoner_app.project_reasoner_v10.main_window_help.runtime_controller`
  - `kanda_reasoner_app.project_reasoner_v10.main_window_help.session_service`
  - `kanda_reasoner_app.project_reasoner_v10.main_window_help.settings_manager`
  - `kanda_reasoner_app.project_reasoner_v10.main_window_help.signal_wiring`
  - `kanda_reasoner_app.project_reasoner_v10.main_window_help.state_models`
  - `kanda_reasoner_app.project_reasoner_v10.main_window_help.static_context_controller`
  - `kanda_reasoner_app.project_reasoner_v10.main_window_help.ui_builder`
  - `kanda_reasoner_app.project_reasoner_v10.main_window_help.ui_components`

**Public Symbol Quick Reference**

- `AnalysisController` -> `kanda_reasoner_app.project_reasoner_v10.main_window_help.analysis_controller`
- `AnalysisState` -> `kanda_reasoner_app.project_reasoner_v10.main_window_help.state_models`
- `AnswerPresenter` -> `kanda_reasoner_app.project_reasoner_v10.main_window_help.answer_presenter`
- `CANONICAL_COMPLETE_JSON_NAME` -> `kanda_reasoner_app.project_reasoner_v10.main_window_help.json_track`
- `ConfidenceStatus` -> `kanda_reasoner_app.project_reasoner_v10.main_window_help.answer_presenter`
- `CopyableListWidget` -> `kanda_reasoner_app.project_reasoner_v10.main_window_help.ui_components`
- `HelpDialog` -> `kanda_reasoner_app.project_reasoner_v10.main_window_help.ui_components`
- `LOCAL_AI_COMPLETE_JSON_NAME` -> `kanda_reasoner_app.project_reasoner_v10.main_window_help.json_track`
- `ProfileSelectionState` -> `kanda_reasoner_app.project_reasoner_v10.main_window_help.state_models`
- `SessionExecutionError` -> `kanda_reasoner_app.project_reasoner_v10.main_window_help.session_service`
- `SessionExecutionResult` -> `kanda_reasoner_app.project_reasoner_v10.main_window_help.session_service`
- `SessionService` -> `kanda_reasoner_app.project_reasoner_v10.main_window_help.session_service`
- `StaticContextController` -> `kanda_reasoner_app.project_reasoner_v10.main_window_help.static_context_controller`
- `WindowSessionState` -> `kanda_reasoner_app.project_reasoner_v10.main_window_help.state_models`
- `WindowSettingsManager` -> `kanda_reasoner_app.project_reasoner_v10.main_window_help.settings_manager`
- `build_main_window_ui` -> `kanda_reasoner_app.project_reasoner_v10.main_window_help.ui_builder`
- `classify_loaded_json_track` -> `kanda_reasoner_app.project_reasoner_v10.main_window_help.json_track`
- `connect_main_window_signals` -> `kanda_reasoner_app.project_reasoner_v10.main_window_help.signal_wiring`
- `shorten_path` -> `kanda_reasoner_app.project_reasoner_v10.main_window_help.ui_components`

### kanda_reasoner_app.project_reasoner_v10.project_profile_help

| Module | Owns | Exposes | Depends On | Used By | Helper Group |
|---|---|---|---|---|---|
| `kanda_reasoner_app.project_reasoner_v10.project_profile_help` |  | ARCHITECTURE_HEAVY_PYTHON_PROJECT_PROFILE, EEG_PROJECT_PROFILE, GENERIC_PROJECT_PROFILE, GENERIC_PYTHON_PROJECT_PROFILE, PROJECT_PROFILES, ProjectProfile, QT_PYTHON_PROJECT_PROFILE, get_project_profile, infer_project_profile, infer_project_profile_name_from_metadata, iter_project_profiles | kanda_reasoner_app.project_reasoner_v10.project_profile_help.built_in_profiles, kanda_reasoner_app.project_reasoner_v10.project_profile_help.inference, kanda_reasoner_app.project_reasoner_v10.project_profile_help.profile_types, kanda_reasoner_app.project_reasoner_v10.project_profile_help.registry | kanda_reasoner_app.project_reasoner_v10.project_profile | project_profile |
| `kanda_reasoner_app.project_reasoner_v10.project_profile_help.built_in_profiles` |  | ARCHITECTURE_HEAVY_PYTHON_PROJECT_PROFILE, EEG_PROJECT_PROFILE, GENERIC_PROJECT_PROFILE, GENERIC_PYTHON_PROJECT_PROFILE, QT_PYTHON_PROJECT_PROFILE | kanda_reasoner_app.project_reasoner_v10.project_profile_help.profile_types | kanda_reasoner_app.project_reasoner_v10.project_profile_help, kanda_reasoner_app.project_reasoner_v10.project_profile_help.inference, kanda_reasoner_app.project_reasoner_v10.project_profile_help.registry | project_profile |
| `kanda_reasoner_app.project_reasoner_v10.project_profile_help.inference` |  | infer_project_profile, infer_project_profile_name_from_metadata | kanda_reasoner_app.project_reasoner_v10.project_profile_help.built_in_profiles, kanda_reasoner_app.project_reasoner_v10.project_profile_help.profile_types, kanda_reasoner_app.project_reasoner_v10.project_profile_help.registry | kanda_reasoner_app.project_reasoner_v10.project_profile_help | project_profile |
| `kanda_reasoner_app.project_reasoner_v10.project_profile_help.profile_types` |  | ProjectProfile |  | kanda_reasoner_app.project_reasoner_v10.project_profile_help, kanda_reasoner_app.project_reasoner_v10.project_profile_help.built_in_profiles, kanda_reasoner_app.project_reasoner_v10.project_profile_help.inference, kanda_reasoner_app.project_reasoner_v10.project_profile_help.registry | project_profile |
| `kanda_reasoner_app.project_reasoner_v10.project_profile_help.registry` |  | PROJECT_PROFILES, get_project_profile, iter_project_profiles | kanda_reasoner_app.project_reasoner_v10.project_profile_help.built_in_profiles, kanda_reasoner_app.project_reasoner_v10.project_profile_help.profile_types | kanda_reasoner_app.project_reasoner_v10.project_profile_help, kanda_reasoner_app.project_reasoner_v10.project_profile_help.inference | project_profile |

**Helper Groups**

- `project_profile` -> main `kanda_reasoner_app.project_reasoner_v10.project_profile`
  - `kanda_reasoner_app.project_reasoner_v10.project_profile_help`
  - `kanda_reasoner_app.project_reasoner_v10.project_profile_help.built_in_profiles`
  - `kanda_reasoner_app.project_reasoner_v10.project_profile_help.inference`
  - `kanda_reasoner_app.project_reasoner_v10.project_profile_help.profile_types`
  - `kanda_reasoner_app.project_reasoner_v10.project_profile_help.registry`

**Public Symbol Quick Reference**

- `ARCHITECTURE_HEAVY_PYTHON_PROJECT_PROFILE` -> `kanda_reasoner_app.project_reasoner_v10.project_profile_help.built_in_profiles`
- `EEG_PROJECT_PROFILE` -> `kanda_reasoner_app.project_reasoner_v10.project_profile_help.built_in_profiles`
- `GENERIC_PROJECT_PROFILE` -> `kanda_reasoner_app.project_reasoner_v10.project_profile_help.built_in_profiles`
- `GENERIC_PYTHON_PROJECT_PROFILE` -> `kanda_reasoner_app.project_reasoner_v10.project_profile_help.built_in_profiles`
- `PROJECT_PROFILES` -> `kanda_reasoner_app.project_reasoner_v10.project_profile_help.registry`
- `ProjectProfile` -> `kanda_reasoner_app.project_reasoner_v10.project_profile_help.profile_types`
- `QT_PYTHON_PROJECT_PROFILE` -> `kanda_reasoner_app.project_reasoner_v10.project_profile_help.built_in_profiles`
- `get_project_profile` -> `kanda_reasoner_app.project_reasoner_v10.project_profile_help.registry`
- `infer_project_profile` -> `kanda_reasoner_app.project_reasoner_v10.project_profile_help.inference`
- `infer_project_profile_name_from_metadata` -> `kanda_reasoner_app.project_reasoner_v10.project_profile_help.inference`
- `iter_project_profiles` -> `kanda_reasoner_app.project_reasoner_v10.project_profile_help.registry`

### kanda_reasoner_app.project_reasoner_v10.prompt_builder_help

| Module | Owns | Exposes | Depends On | Used By | Helper Group |
|---|---|---|---|---|---|
| `kanda_reasoner_app.project_reasoner_v10.prompt_builder_help` |  | append_callsite_evidence_section, append_file_evidence_section, append_memory_section, append_project_summary, append_source_snippets_section, append_symbol_evidence_section, append_widget_registry_section, build_answer_style_instructions, extract_exact_call_targets, is_chain_or_flow_question, is_code_localized_explanation_question, is_explain_implementation_question, is_which_method_calls_question, norm_text, prioritize_callsite_snippets, tokenize_query | kanda_reasoner_app.project_reasoner_v10.prompt_builder_help.answer_style, kanda_reasoner_app.project_reasoner_v10.prompt_builder_help.callsite_evidence, kanda_reasoner_app.project_reasoner_v10.prompt_builder_help.prompt_classification, kanda_reasoner_app.project_reasoner_v10.prompt_builder_help.prompt_sections, kanda_reasoner_app.project_reasoner_v10.prompt_builder_help.widget_registry_section |  | prompt_builder |
| `kanda_reasoner_app.project_reasoner_v10.prompt_builder_help.answer_style` |  | build_answer_style_instructions | kanda_reasoner_app.project_reasoner_v10.prompt_builder_help.prompt_classification | kanda_reasoner_app.project_reasoner_v10.prompt_builder, kanda_reasoner_app.project_reasoner_v10.prompt_builder_help | prompt_builder |
| `kanda_reasoner_app.project_reasoner_v10.prompt_builder_help.callsite_evidence` |  | append_callsite_evidence_section, extract_exact_call_targets, prioritize_callsite_snippets | kanda_reasoner_app.project_reasoner_v10.prompt_builder_help.prompt_classification | kanda_reasoner_app.project_reasoner_v10.prompt_builder, kanda_reasoner_app.project_reasoner_v10.prompt_builder_help | prompt_builder |
| `kanda_reasoner_app.project_reasoner_v10.prompt_builder_help.prompt_classification` |  | is_chain_or_flow_question, is_code_localized_explanation_question, is_explain_implementation_question, is_which_method_calls_question, norm_text, tokenize_query |  | kanda_reasoner_app.project_reasoner_v10.prompt_builder, kanda_reasoner_app.project_reasoner_v10.prompt_builder_help, kanda_reasoner_app.project_reasoner_v10.prompt_builder_help.answer_style, kanda_reasoner_app.project_reasoner_v10.prompt_builder_help.callsite_evidence, kanda_reasoner_app.project_reasoner_v10.prompt_builder_help.widget_registry_section | prompt_builder |
| `kanda_reasoner_app.project_reasoner_v10.prompt_builder_help.prompt_sections` |  | append_file_evidence_section, append_live_source_evidence_section, append_memory_section, append_project_summary, append_source_snippets_section, append_symbol_evidence_section, is_live_source_snippet |  | kanda_reasoner_app.project_reasoner_v10.prompt_builder, kanda_reasoner_app.project_reasoner_v10.prompt_builder_help | prompt_builder |
| `kanda_reasoner_app.project_reasoner_v10.prompt_builder_help.widget_registry_section` |  | append_widget_registry_section | kanda_reasoner_app.project_reasoner_v10.prompt_builder_help.prompt_classification, kanda_reasoner_app.project_reasoner_v10.query_router | kanda_reasoner_app.project_reasoner_v10.prompt_builder, kanda_reasoner_app.project_reasoner_v10.prompt_builder_help | prompt_builder |

**Helper Groups**

- `prompt_builder` -> main `kanda_reasoner_app.project_reasoner_v10.prompt_builder`
  - `kanda_reasoner_app.project_reasoner_v10.prompt_builder_help`
  - `kanda_reasoner_app.project_reasoner_v10.prompt_builder_help.answer_style`
  - `kanda_reasoner_app.project_reasoner_v10.prompt_builder_help.callsite_evidence`
  - `kanda_reasoner_app.project_reasoner_v10.prompt_builder_help.prompt_classification`
  - `kanda_reasoner_app.project_reasoner_v10.prompt_builder_help.prompt_sections`
  - `kanda_reasoner_app.project_reasoner_v10.prompt_builder_help.widget_registry_section`

**Public Symbol Quick Reference**

- `append_callsite_evidence_section` -> `kanda_reasoner_app.project_reasoner_v10.prompt_builder_help.callsite_evidence`
- `append_file_evidence_section` -> `kanda_reasoner_app.project_reasoner_v10.prompt_builder_help.prompt_sections`
- `append_live_source_evidence_section` -> `kanda_reasoner_app.project_reasoner_v10.prompt_builder_help.prompt_sections`
- `append_memory_section` -> `kanda_reasoner_app.project_reasoner_v10.prompt_builder_help.prompt_sections`
- `append_project_summary` -> `kanda_reasoner_app.project_reasoner_v10.prompt_builder_help.prompt_sections`
- `append_source_snippets_section` -> `kanda_reasoner_app.project_reasoner_v10.prompt_builder_help.prompt_sections`
- `append_symbol_evidence_section` -> `kanda_reasoner_app.project_reasoner_v10.prompt_builder_help.prompt_sections`
- `append_widget_registry_section` -> `kanda_reasoner_app.project_reasoner_v10.prompt_builder_help.widget_registry_section`
- `build_answer_style_instructions` -> `kanda_reasoner_app.project_reasoner_v10.prompt_builder_help.answer_style`
- `extract_exact_call_targets` -> `kanda_reasoner_app.project_reasoner_v10.prompt_builder_help.callsite_evidence`
- `is_chain_or_flow_question` -> `kanda_reasoner_app.project_reasoner_v10.prompt_builder_help.prompt_classification`
- `is_code_localized_explanation_question` -> `kanda_reasoner_app.project_reasoner_v10.prompt_builder_help.prompt_classification`
- `is_explain_implementation_question` -> `kanda_reasoner_app.project_reasoner_v10.prompt_builder_help.prompt_classification`
- `is_live_source_snippet` -> `kanda_reasoner_app.project_reasoner_v10.prompt_builder_help.prompt_sections`
- `is_which_method_calls_question` -> `kanda_reasoner_app.project_reasoner_v10.prompt_builder_help.prompt_classification`
- `norm_text` -> `kanda_reasoner_app.project_reasoner_v10.prompt_builder_help.prompt_classification`
- `prioritize_callsite_snippets` -> `kanda_reasoner_app.project_reasoner_v10.prompt_builder_help.callsite_evidence`
- `tokenize_query` -> `kanda_reasoner_app.project_reasoner_v10.prompt_builder_help.prompt_classification`

### kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help

| Module | Owns | Exposes | Depends On | Used By | Helper Group |
|---|---|---|---|---|---|
| `kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help` |  | bundle_merge, file_context_scoring, file_retrieval, profile_support, query_intents, query_text, section_retrieval, snippet_expansion, snippet_retrieval, symbol_retrieval |  |  | reasoner_retriever |
| `kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.bundle_merge` |  | merge_retrieval_bundles | kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.query_text, kanda_reasoner_app.project_reasoner_v10.v10_models |  | reasoner_retriever |
| `kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.file_context_scoring` |  | collect_file_context_blobs, get_runtime_anchor_summary, score_advanced_file_context, score_runtime_signal_matches | kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.query_text |  | reasoner_retriever |
| `kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.file_retrieval` |  | build_compact_file_evidence, retrieve_files | kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.file_retrieval_help |  | reasoner_retriever |
| `kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.file_retrieval_validate_manifests` |  |  |  |  | reasoner_retriever |
| `kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.live_source_fallback` |  | augment_bundle_with_live_source_fallback, extract_live_identifier_terms, find_live_source_candidates | kanda_reasoner_app.live_source_verification, kanda_reasoner_app.project_reasoner_v10.v10_models |  | reasoner_retriever |
| `kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.profile_support` |  | get_profile_alias_terms, get_profile_owner_paths, question_has_profile_alias, resolve_project_profile, text_has_profile_alias | kanda_reasoner_app.project_reasoner_v10.project_profile, kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.query_text |  | reasoner_retriever |
| `kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.query_intents` |  |  | kanda_reasoner_app.backend_payloads.loader | kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.retriever_consensus_private_impl, kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.section_retrieval, kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.snippet_retrieval, kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.symbol_retrieval_evidence_private_impl, kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.symbol_retrieval_retrieve_private_impl, kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.symbol_retrieval_support_private_impl | reasoner_retriever |
| `kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.query_text` |  | file_name_from_path, is_allowed_project_path, is_auxiliary_ui_path, last_part_match_in_query, norm_text, safe_read_text, tokenize_query |  | kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.bundle_merge, kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.file_context_scoring, kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.profile_support, kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.retriever_consensus_private_impl, kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.section_retrieval, kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.snippet_retrieval, kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.symbol_retrieval_evidence_private_impl, kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.symbol_retrieval_retrieve_private_impl, kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.symbol_retrieval_support_private_impl | reasoner_retriever |
| `kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.retriever_consensus_private_impl` |  |  | kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.query_intents, kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.query_text, kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.snippet_expansion, kanda_reasoner_app.project_reasoner_v10.v10_models |  | reasoner_retriever |
| `kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.retriever_routing_private_impl` |  |  | kanda_reasoner_app.project_reasoner_v10.v10_models |  | reasoner_retriever |
| `kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.section_retrieval` |  | retrieve_documentation_intent, retrieve_packaging_metadata | kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.query_intents, kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.query_text, kanda_reasoner_app.project_reasoner_v10.v10_models |  | reasoner_retriever |
| `kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.snippet_expansion` |  |  |  | kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.retriever_consensus_private_impl | reasoner_retriever |
| `kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.snippet_retrieval` |  | build_runtime_anchor_snippets, extract_runtime_anchors_from_detail, find_anchor_line_in_file, read_snippet, resolve_existing_project_file_path, retrieve_snippets, score_file_snippet_candidate, score_runtime_anchor_for_question, score_symbol_snippet_candidate, snippet_radius_for_symbol | kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.query_intents, kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.query_text, kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.snippet_retrieval_help, kanda_reasoner_app.project_reasoner_v10.v10_models |  | reasoner_retriever |
| `kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.snippet_retrieval_validate_manifests` |  |  |  |  | reasoner_retriever |
| `kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.symbol_retrieval` |  | build_symbol_evidence, retrieve_symbols | kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.symbol_retrieval_evidence_private_impl, kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.symbol_retrieval_retrieve_private_impl |  | reasoner_retriever |
| `kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.symbol_retrieval_evidence_private_impl` |  |  | kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.query_intents, kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.query_text, kanda_reasoner_app.project_reasoner_v10.v10_models | kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.symbol_retrieval, kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.symbol_retrieval_retrieve_private_impl | reasoner_retriever |
| `kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.symbol_retrieval_retrieve_private_impl` |  |  | kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.query_intents, kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.query_text, kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.symbol_retrieval_evidence_private_impl, kanda_reasoner_app.project_reasoner_v10.v10_models | kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.symbol_retrieval | reasoner_retriever |
| `kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.symbol_retrieval_support_private_impl` |  |  | kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.query_intents, kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.query_text, kanda_reasoner_app.project_reasoner_v10.v10_models |  | reasoner_retriever |

**Helper Groups**

- `reasoner_retriever` -> main `kanda_reasoner_app.project_reasoner_v10.reasoner_retriever`
  - `kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help`
  - `kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.bundle_merge`
  - `kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.file_context_scoring`
  - `kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.file_retrieval`
  - `kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.file_retrieval_validate_manifests`
  - `kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.live_source_fallback`
  - `kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.profile_support`
  - `kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.query_intents`
  - `kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.query_text`
  - `kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.retriever_consensus_private_impl`
  - `kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.retriever_routing_private_impl`
  - `kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.section_retrieval`
  - `kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.snippet_expansion`
  - `kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.snippet_retrieval`
  - `kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.snippet_retrieval_validate_manifests`
  - `kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.symbol_retrieval`
  - `kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.symbol_retrieval_evidence_private_impl`
  - `kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.symbol_retrieval_retrieve_private_impl`
  - `kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.symbol_retrieval_support_private_impl`

**Public Symbol Quick Reference**

- `augment_bundle_with_live_source_fallback` -> `kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.live_source_fallback`
- `build_compact_file_evidence` -> `kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.file_retrieval`
- `build_runtime_anchor_snippets` -> `kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.snippet_retrieval`
- `build_symbol_evidence` -> `kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.symbol_retrieval`
- `collect_file_context_blobs` -> `kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.file_context_scoring`
- `extract_live_identifier_terms` -> `kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.live_source_fallback`
- `extract_runtime_anchors_from_detail` -> `kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.snippet_retrieval`
- `file_name_from_path` -> `kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.query_text`
- `find_anchor_line_in_file` -> `kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.snippet_retrieval`
- `find_live_source_candidates` -> `kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.live_source_fallback`
- `get_profile_alias_terms` -> `kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.profile_support`
- `get_profile_owner_paths` -> `kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.profile_support`
- `get_runtime_anchor_summary` -> `kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.file_context_scoring`
- `is_allowed_project_path` -> `kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.query_text`
- `is_auxiliary_ui_path` -> `kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.query_text`
- `last_part_match_in_query` -> `kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.query_text`
- `merge_retrieval_bundles` -> `kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.bundle_merge`
- `norm_text` -> `kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.query_text`
- `question_has_profile_alias` -> `kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.profile_support`
- `read_snippet` -> `kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.snippet_retrieval`
- `resolve_existing_project_file_path` -> `kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.snippet_retrieval`
- `resolve_project_profile` -> `kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.profile_support`
- `retrieve_documentation_intent` -> `kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.section_retrieval`
- `retrieve_files` -> `kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.file_retrieval`
- `retrieve_packaging_metadata` -> `kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.section_retrieval`
- `retrieve_snippets` -> `kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.snippet_retrieval`
- `retrieve_symbols` -> `kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.symbol_retrieval`
- `safe_read_text` -> `kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.query_text`
- `score_advanced_file_context` -> `kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.file_context_scoring`
- `score_file_snippet_candidate` -> `kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.snippet_retrieval`
- `score_runtime_anchor_for_question` -> `kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.snippet_retrieval`
- `score_runtime_signal_matches` -> `kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.file_context_scoring`
- `score_symbol_snippet_candidate` -> `kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.snippet_retrieval`
- `snippet_radius_for_symbol` -> `kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.snippet_retrieval`
- `text_has_profile_alias` -> `kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.profile_support`
- `tokenize_query` -> `kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.query_text`

### kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.file_retrieval_help

| Module | Owns | Exposes | Depends On | Used By | Helper Group |
|---|---|---|---|---|---|
| `kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.file_retrieval_help` |  |  |  | kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.file_retrieval, kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.file_retrieval_help.file_retrieval_impl_private_impl | file_retrieval |
| `kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.file_retrieval_help.file_retrieval_impl_private_impl` |  |  | kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.file_retrieval_help |  | file_retrieval |
| `kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.file_retrieval_help.file_retrieval_source_part_1_private_impl` |  |  |  |  | file_retrieval |
| `kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.file_retrieval_help.file_retrieval_source_part_2_private_impl` |  |  |  |  | file_retrieval |
| `kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.file_retrieval_help.file_retrieval_source_part_3_private_impl` |  |  |  |  | file_retrieval |

**Helper Groups**

- `file_retrieval` -> main `kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.file_retrieval`
  - `kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.file_retrieval_help`
  - `kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.file_retrieval_help.file_retrieval_impl_private_impl`
  - `kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.file_retrieval_help.file_retrieval_source_part_1_private_impl`
  - `kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.file_retrieval_help.file_retrieval_source_part_2_private_impl`
  - `kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.file_retrieval_help.file_retrieval_source_part_3_private_impl`

### kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.snippet_retrieval_help

| Module | Owns | Exposes | Depends On | Used By | Helper Group |
|---|---|---|---|---|---|
| `kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.snippet_retrieval_help` |  |  |  | kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.snippet_retrieval | snippet_retrieval |
| `kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.snippet_retrieval_help.snippet_retrieval_part_1_private_impl` |  |  |  |  | snippet_retrieval |
| `kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.snippet_retrieval_help.snippet_retrieval_part_2_private_impl` |  |  |  |  | snippet_retrieval |
| `kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.snippet_retrieval_help.snippet_retrieval_part_3_private_impl` |  |  |  |  | snippet_retrieval |

**Helper Groups**

- `snippet_retrieval` -> main `kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.snippet_retrieval`
  - `kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.snippet_retrieval_help`
  - `kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.snippet_retrieval_help.snippet_retrieval_part_1_private_impl`
  - `kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.snippet_retrieval_help.snippet_retrieval_part_2_private_impl`
  - `kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.snippet_retrieval_help.snippet_retrieval_part_3_private_impl`

### kanda_reasoner_app.reasoner_context_collector

| Module | Owns | Exposes | Depends On | Used By | Helper Group |
|---|---|---|---|---|---|
| `kanda_reasoner_app.reasoner_context_collector` |  | run_collector | kanda_reasoner_app.reasoner_context_collector.collector_main |  |  |
| `kanda_reasoner_app.reasoner_context_collector.collector_active_code` |  | build_active_code_index, build_active_code_summary, build_untested_critical_hotspots |  |  |  |
| `kanda_reasoner_app.reasoner_context_collector.collector_ast` |  | parse_python_file | kanda_reasoner_app.reasoner_context_collector.collector_control_flow, kanda_reasoner_app.reasoner_context_collector.collector_data_flow, kanda_reasoner_app.reasoner_context_collector.collector_docstrings, kanda_reasoner_app.reasoner_context_collector.collector_utils, kanda_reasoner_app.reasoner_context_collector.collector_warnings |  |  |
| `kanda_reasoner_app.reasoner_context_collector.collector_boundaries` |  | CONTROLLER_KEYWORDS, DOMAIN_KEYWORDS, SERVICE_KEYWORDS, build_boundary_handoffs, build_boundary_index, build_boundary_summary |  |  |  |
| `kanda_reasoner_app.reasoner_context_collector.collector_boundary_violations` |  | DISALLOWED_HANDOFFS, HIGH_CROSS_BUCKET_THRESHOLD, MIXED_ROLE_THRESHOLD, build_boundary_violation_hotspots, build_boundary_violation_index, build_boundary_violation_summary |  |  |  |
| `kanda_reasoner_app.reasoner_context_collector.collector_bucket_insights` |  | build_bucket_hotspots, build_bucket_insights, build_bucket_priority_summary, build_bucket_warning_summary |  |  |  |
| `kanda_reasoner_app.reasoner_context_collector.collector_buckets` |  | build_bucket_index, build_bucket_summary, classify_file_bucket |  |  |  |
| `kanda_reasoner_app.reasoner_context_collector.collector_canonical_conflicts` |  | CANONICAL_PREFERENCE_HINTS, LEGACY_TOKENS, TRANSITION_TOKENS, build_canonical_conflict_index, build_canonical_conflict_summary, build_legacy_shadow_hotspots |  |  |  |
| `kanda_reasoner_app.reasoner_context_collector.collector_centrality` |  | build_module_centrality_index, build_symbol_centrality_index, build_top_project_hotspots |  |  |  |
| `kanda_reasoner_app.reasoner_context_collector.collector_chains` |  | build_execution_chains, derive_reset_chain, derive_startup_chain, derive_timeline_chain, derive_topomap_chain |  |  |  |
| `kanda_reasoner_app.reasoner_context_collector.collector_change_impact` |  | build_change_impact_index, build_change_impact_summary, build_high_risk_edit_hotspots |  |  |  |
| `kanda_reasoner_app.reasoner_context_collector.collector_config` |  | CollectorConfig |  | kanda_reasoner_app.reasoner_context_collector.collector_edit_ready_source, kanda_reasoner_app.reasoner_context_collector.collector_filters, kanda_reasoner_app.reasoner_context_collector.collector_output, kanda_reasoner_app.reasoner_context_collector.collector_walker, kanda_reasoner_app.reasoner_context_collector.collectors.static_context.collector_documentation_intent, kanda_reasoner_app.reasoner_context_collector.collectors.static_context.collector_packaging_metadata |  |
| `kanda_reasoner_app.reasoner_context_collector.collector_config_schema` |  | CONFIG_KEY_HINTS, build_config_schema_registry, build_config_schema_summary, build_schema_risk_hotspots |  |  |  |
| `kanda_reasoner_app.reasoner_context_collector.collector_control_flow` |  | build_control_flow |  | kanda_reasoner_app.reasoner_context_collector.collector_ast |  |
| `kanda_reasoner_app.reasoner_context_collector.collector_coverage` |  | collect_coverage_for_file |  |  |  |
| `kanda_reasoner_app.reasoner_context_collector.collector_data_flow` |  | build_data_flow |  | kanda_reasoner_app.reasoner_context_collector.collector_ast |  |
| `kanda_reasoner_app.reasoner_context_collector.collector_docstrings` |  | build_docstring_summary |  | kanda_reasoner_app.reasoner_context_collector.collector_ast |  |
| `kanda_reasoner_app.reasoner_context_collector.collector_dump_mapper` |  | build_change_impact, build_event_propagation, build_local_change_impact, build_local_event_propagation, build_local_symbol_index_with_enrichment, build_symbol_index_with_enrichment, extract_global_state, extract_localization |  |  |  |
| `kanda_reasoner_app.reasoner_context_collector.collector_duplicates` |  | find_duplicate_symbols |  |  |  |
| `kanda_reasoner_app.reasoner_context_collector.collector_edit_ready_source` |  | build_edit_ready_source_summary, build_edit_ready_symbol_index, build_legacy_snippet_index_from_edit_ready, build_source_file_index | kanda_reasoner_app.reasoner_context_collector.collector_config, kanda_reasoner_app.reasoner_context_collector.collector_utils |  |  |
| `kanda_reasoner_app.reasoner_context_collector.collector_entry_bucket_flows` |  | NOISE_BUCKETS, build_entry_bucket_flow_summary, build_entry_bucket_flows |  |  |  |
| `kanda_reasoner_app.reasoner_context_collector.collector_entry_points_detail` |  | build_entry_points_detail, build_entry_points_detail_summary |  |  |  |
| `kanda_reasoner_app.reasoner_context_collector.collector_event_propagation` |  | build_event_propagation_hotspots, build_event_propagation_index, build_event_propagation_summary |  |  |  |
| `kanda_reasoner_app.reasoner_context_collector.collector_feature_registry` |  | FEATURE_RULES, build_feature_hotspots, build_feature_registry, build_feature_summary |  |  |  |
| `kanda_reasoner_app.reasoner_context_collector.collector_filters` |  | should_exclude_dir, should_exclude_file | kanda_reasoner_app.reasoner_context_collector.collector_config | kanda_reasoner_app.reasoner_context_collector.collector_walker |  |
| `kanda_reasoner_app.reasoner_context_collector.collector_git` |  | collect_git_metadata_for_file |  |  |  |
| `kanda_reasoner_app.reasoner_context_collector.collector_implementation_chronology` |  | CANONICAL_HINTS, LEGACY_HINTS, TRANSITION_HINTS, build_implementation_chronology_index, build_implementation_chronology_summary, build_migration_transition_hotspots |  |  |  |
| `kanda_reasoner_app.reasoner_context_collector.collector_insights` |  | get_entry_chain_summary, get_project_hotspot_summary, get_top_central_symbols, get_top_priority_files |  |  |  |
| `kanda_reasoner_app.reasoner_context_collector.collector_main` |  |  |  | kanda_reasoner_app.reasoner_context_collector, kanda_reasoner_app.run_real_project_static_context_smoke |  |
| `kanda_reasoner_app.reasoner_context_collector.collector_main_validate_manifests` |  | main |  |  |  |
| `kanda_reasoner_app.reasoner_context_collector.collector_module_summary` |  | build_module_responsibility_summary |  |  |  |
| `kanda_reasoner_app.reasoner_context_collector.collector_orchestration` |  | build_orchestration_hotspots, build_orchestration_index, build_orchestration_summary |  |  |  |
| `kanda_reasoner_app.reasoner_context_collector.collector_output` |  | build_collection_config, build_collector_info, build_collector_scope, build_limitations_section | kanda_reasoner_app.reasoner_context_collector.collector_config |  |  |
| `kanda_reasoner_app.reasoner_context_collector.collector_ownership` |  | build_object_ownership_map |  |  |  |
| `kanda_reasoner_app.reasoner_context_collector.collector_persistence_io` |  | PERSISTENCE_HINTS, READ_HINTS, WRITE_HINTS, build_persistence_io_hotspots, build_persistence_io_index, build_persistence_io_summary |  |  |  |
| `kanda_reasoner_app.reasoner_context_collector.collector_primary_definition_index` |  | build_primary_definition_index, build_primary_definition_summary |  |  |  |
| `kanda_reasoner_app.reasoner_context_collector.collector_priority` |  | build_file_priority_index, build_priority_ranking |  |  |  |
| `kanda_reasoner_app.reasoner_context_collector.collector_qt` |  | extract_qt_signal_map |  |  |  |
| `kanda_reasoner_app.reasoner_context_collector.collector_responsibility_overlap` |  | build_overlap_hotspots, build_responsibility_overlap_index, build_responsibility_overlap_summary | kanda_reasoner_app.reasoner_context_collector.collector_responsibility_overlap_help.extraction, kanda_reasoner_app.reasoner_context_collector.collector_responsibility_overlap_help.scoring |  |  |
| `kanda_reasoner_app.reasoner_context_collector.collector_responsibility_overlap_validate_manifests` |  | EXPECTED_ROOT_ALL, HELPER_FILES, HELP_DIR, ROOT, TARGET, has_star_import, line_count, literal_all, main, read_text |  |  |  |
| `kanda_reasoner_app.reasoner_context_collector.collector_roles` |  | ROLE_HINTS, summarize_file_semantics, summarize_symbol_semantics | kanda_reasoner_app.reasoner_context_collector.collector_utils |  |  |
| `kanda_reasoner_app.reasoner_context_collector.collector_runtime_feature_attribution` |  | build_runtime_feature_attribution_hotspots, build_runtime_feature_attribution_index, build_runtime_feature_attribution_summary |  |  |  |
| `kanda_reasoner_app.reasoner_context_collector.collector_runtime_scenarios` |  |  | kanda_reasoner_app.backend_payloads.loader |  |  |
| `kanda_reasoner_app.reasoner_context_collector.collector_runtime_scenarios_validate_manifests` |  | PUBLIC_ALL, fail, has_star_import, literal_all, main, read_text |  |  |  |
| `kanda_reasoner_app.reasoner_context_collector.collector_runtime_trace` |  | build_runtime_trace_index |  |  |  |
| `kanda_reasoner_app.reasoner_context_collector.collector_scope` |  | DOC_SUFFIXES, FORBIDDEN_ROOT_RELATIVE_PARTS, FORBIDDEN_TEXT_FRAGMENTS, HARD_EXCLUDED_PARTS, PACKAGING_NAMES, assert_no_forbidden_fragments, is_inside_project, iter_project_documentation_files, iter_project_files, iter_project_packaging_files, iter_project_python_files, resolve_project_root, sanitize_collector_outputs, sanitize_json_file |  | kanda_reasoner_app.reasoner_context_collector.complete_json_web_ai_enrichment, kanda_reasoner_app.reasoner_context_collector.parsers.static_context.documentation_intent_parser, kanda_reasoner_app.reasoner_context_collector.parsers.static_context.packaging_metadata_parser |  |
| `kanda_reasoner_app.reasoner_context_collector.collector_stable_evidence_id_index` |  | build_stable_evidence_id_index, build_stable_evidence_id_summary |  |  |  |
| `kanda_reasoner_app.reasoner_context_collector.collector_state` |  | build_attribute_state_map |  |  |  |
| `kanda_reasoner_app.reasoner_context_collector.collector_state_lifecycle` |  | STATE_CREATE_HINTS, STATE_REHYDRATE_HINTS, STATE_RESET_HINTS, STATE_UPDATE_HINTS, build_state_lifecycle_hotspots, build_state_lifecycle_index, build_state_lifecycle_summary |  |  |  |
| `kanda_reasoner_app.reasoner_context_collector.collector_state_mutations` |  | build_state_mutation_hotspots, build_state_mutation_index, build_state_mutation_summary |  |  |  |
| `kanda_reasoner_app.reasoner_context_collector.collector_subsystems` |  | build_subsystem_summaries |  |  |  |
| `kanda_reasoner_app.reasoner_context_collector.collector_tests` |  | link_tests_to_sources |  |  |  |
| `kanda_reasoner_app.reasoner_context_collector.collector_ui_actions` |  | build_ui_action_hotspots, build_ui_action_index, build_ui_action_summary |  |  |  |
| `kanda_reasoner_app.reasoner_context_collector.collector_utils` |  | compact_whitespace, normalize_path, safe_json_dump, sanitize_for_json, short_hash |  | kanda_reasoner_app.reasoner_context_collector.collector_ast, kanda_reasoner_app.reasoner_context_collector.collector_edit_ready_source, kanda_reasoner_app.reasoner_context_collector.collector_roles |  |
| `kanda_reasoner_app.reasoner_context_collector.collector_walker` |  | walk_python_files_filtered | kanda_reasoner_app.reasoner_context_collector.collector_config, kanda_reasoner_app.reasoner_context_collector.collector_filters |  |  |
| `kanda_reasoner_app.reasoner_context_collector.collector_warnings` |  | normalize_file_warning_records, parse_python_source_with_warnings |  | kanda_reasoner_app.reasoner_context_collector.collector_ast |  |
| `kanda_reasoner_app.reasoner_context_collector.collector_web_ai_complete_json_audit` |  | CANONICAL_COMPLETE_JSON_RELATIVE_PATH, REQUIRED_WEB_AI_KEYS, audit_complete_json_file, audit_complete_json_payload, main |  |  |  |
| `kanda_reasoner_app.reasoner_context_collector.collector_web_ai_contract` |  | CANONICAL_JSON_ROLE, KEY_CLASSIFICATIONS, LARGE_SECTION_KEYS, RECOMMENDED_FUTURE_WEB_AI_KEYS, REQUIRED_TOP_LEVEL_KEYS, build_collector_output_audit, validate_collector_output_contract |  |  |  |
| `kanda_reasoner_app.reasoner_context_collector.collector_web_ai_file_responsibility_index` |  | build_web_ai_file_responsibility_index, build_web_ai_file_responsibility_summary |  |  |  |
| `kanda_reasoner_app.reasoner_context_collector.collector_web_ai_readme` |  | build_web_ai_readme, build_web_ai_readme_summary |  |  |  |
| `kanda_reasoner_app.reasoner_context_collector.collector_web_ai_symbol_index` |  | build_web_ai_symbol_index, build_web_ai_symbol_summary |  |  |  |
| `kanda_reasoner_app.reasoner_context_collector.collector_web_ai_test_protection_index` |  | build_web_ai_test_protection_index, build_web_ai_test_protection_summary |  |  |  |
| `kanda_reasoner_app.reasoner_context_collector.collector_widget_layout_index` |  | build_widget_layout_hotspots, build_widget_layout_index |  |  |  |
| `kanda_reasoner_app.reasoner_context_collector.collector_widget_registry` |  | build_widget_registry | kanda_reasoner_app.reasoner_context_collector.collector_widget_registry_help |  |  |
| `kanda_reasoner_app.reasoner_context_collector.collector_widget_registry_validate_manifests` |  | main |  |  |  |
| `kanda_reasoner_app.reasoner_context_collector.collector_widget_summary` |  | build_widget_hotspots, build_widget_summary |  |  |  |
| `kanda_reasoner_app.reasoner_context_collector.collector_widget_text_index` |  | build_widget_text_hotspots, build_widget_text_index |  |  |  |
| `kanda_reasoner_app.reasoner_context_collector.collector_widget_ui_action_bridge` |  | build_widget_ui_action_bridge, build_widget_ui_action_hotspots | kanda_reasoner_app.reasoner_context_collector.collector_widget_ui_action_bridge_help |  |  |
| `kanda_reasoner_app.reasoner_context_collector.collector_widget_ui_action_bridge_validate_manifests` |  | EXPECTED_ROOT_ALL, HELPER_FILES, has_module_docstring, has_star_import, literal_all, main, read_text |  |  |  |
| `kanda_reasoner_app.reasoner_context_collector.complete_json_web_ai_enrichment` |  | REQUIRED_WEB_AI_SECTIONS, build_web_ai_sections, complete_json_path_for_project, enrich_complete_json_for_web_ai, enrich_project_complete_json | kanda_reasoner_app.reasoner_context_collector.collector_scope |  |  |
| `kanda_reasoner_app.reasoner_context_collector.runner` |  | CollectorRunnerWindow, TRACE_PATH_EXPORT, main, make_empty_index_payload, resolve_output_json_path |  |  |  |

**Public Symbol Quick Reference**

- `CANONICAL_COMPLETE_JSON_RELATIVE_PATH` -> `kanda_reasoner_app.reasoner_context_collector.collector_web_ai_complete_json_audit`
- `CANONICAL_HINTS` -> `kanda_reasoner_app.reasoner_context_collector.collector_implementation_chronology`
- `CANONICAL_JSON_ROLE` -> `kanda_reasoner_app.reasoner_context_collector.collector_web_ai_contract`
- `CANONICAL_PREFERENCE_HINTS` -> `kanda_reasoner_app.reasoner_context_collector.collector_canonical_conflicts`
- `CONFIG_KEY_HINTS` -> `kanda_reasoner_app.reasoner_context_collector.collector_config_schema`
- `CONTROLLER_KEYWORDS` -> `kanda_reasoner_app.reasoner_context_collector.collector_boundaries`
- `CollectorConfig` -> `kanda_reasoner_app.reasoner_context_collector.collector_config`
- `CollectorRunnerWindow` -> `kanda_reasoner_app.reasoner_context_collector.runner`
- `DISALLOWED_HANDOFFS` -> `kanda_reasoner_app.reasoner_context_collector.collector_boundary_violations`
- `DOC_SUFFIXES` -> `kanda_reasoner_app.reasoner_context_collector.collector_scope`
- `DOMAIN_KEYWORDS` -> `kanda_reasoner_app.reasoner_context_collector.collector_boundaries`
- `FEATURE_RULES` -> `kanda_reasoner_app.reasoner_context_collector.collector_feature_registry`
- `FORBIDDEN_ROOT_RELATIVE_PARTS` -> `kanda_reasoner_app.reasoner_context_collector.collector_scope`
- `FORBIDDEN_TEXT_FRAGMENTS` -> `kanda_reasoner_app.reasoner_context_collector.collector_scope`
- `HARD_EXCLUDED_PARTS` -> `kanda_reasoner_app.reasoner_context_collector.collector_scope`
- `HELP_DIR` -> `kanda_reasoner_app.reasoner_context_collector.collector_responsibility_overlap_validate_manifests`
- `HIGH_CROSS_BUCKET_THRESHOLD` -> `kanda_reasoner_app.reasoner_context_collector.collector_boundary_violations`
- `KEY_CLASSIFICATIONS` -> `kanda_reasoner_app.reasoner_context_collector.collector_web_ai_contract`
- `LARGE_SECTION_KEYS` -> `kanda_reasoner_app.reasoner_context_collector.collector_web_ai_contract`
- `LEGACY_HINTS` -> `kanda_reasoner_app.reasoner_context_collector.collector_implementation_chronology`
- `LEGACY_TOKENS` -> `kanda_reasoner_app.reasoner_context_collector.collector_canonical_conflicts`
- `MIXED_ROLE_THRESHOLD` -> `kanda_reasoner_app.reasoner_context_collector.collector_boundary_violations`
- `NOISE_BUCKETS` -> `kanda_reasoner_app.reasoner_context_collector.collector_entry_bucket_flows`
- `PACKAGING_NAMES` -> `kanda_reasoner_app.reasoner_context_collector.collector_scope`
- `PERSISTENCE_HINTS` -> `kanda_reasoner_app.reasoner_context_collector.collector_persistence_io`
- `PUBLIC_ALL` -> `kanda_reasoner_app.reasoner_context_collector.collector_runtime_scenarios_validate_manifests`
- `READ_HINTS` -> `kanda_reasoner_app.reasoner_context_collector.collector_persistence_io`
- `RECOMMENDED_FUTURE_WEB_AI_KEYS` -> `kanda_reasoner_app.reasoner_context_collector.collector_web_ai_contract`
- `REQUIRED_TOP_LEVEL_KEYS` -> `kanda_reasoner_app.reasoner_context_collector.collector_web_ai_contract`
- `REQUIRED_WEB_AI_KEYS` -> `kanda_reasoner_app.reasoner_context_collector.collector_web_ai_complete_json_audit`
- `REQUIRED_WEB_AI_SECTIONS` -> `kanda_reasoner_app.reasoner_context_collector.complete_json_web_ai_enrichment`
- `ROLE_HINTS` -> `kanda_reasoner_app.reasoner_context_collector.collector_roles`
- `ROOT` -> `kanda_reasoner_app.reasoner_context_collector.collector_responsibility_overlap_validate_manifests`
- `SERVICE_KEYWORDS` -> `kanda_reasoner_app.reasoner_context_collector.collector_boundaries`
- `STATE_CREATE_HINTS` -> `kanda_reasoner_app.reasoner_context_collector.collector_state_lifecycle`
- `STATE_REHYDRATE_HINTS` -> `kanda_reasoner_app.reasoner_context_collector.collector_state_lifecycle`
- `STATE_RESET_HINTS` -> `kanda_reasoner_app.reasoner_context_collector.collector_state_lifecycle`
- `STATE_UPDATE_HINTS` -> `kanda_reasoner_app.reasoner_context_collector.collector_state_lifecycle`
- `TARGET` -> `kanda_reasoner_app.reasoner_context_collector.collector_responsibility_overlap_validate_manifests`
- `TRACE_PATH_EXPORT` -> `kanda_reasoner_app.reasoner_context_collector.runner`
- `TRANSITION_HINTS` -> `kanda_reasoner_app.reasoner_context_collector.collector_implementation_chronology`
- `TRANSITION_TOKENS` -> `kanda_reasoner_app.reasoner_context_collector.collector_canonical_conflicts`
- `WRITE_HINTS` -> `kanda_reasoner_app.reasoner_context_collector.collector_persistence_io`
- `assert_no_forbidden_fragments` -> `kanda_reasoner_app.reasoner_context_collector.collector_scope`
- `audit_complete_json_file` -> `kanda_reasoner_app.reasoner_context_collector.collector_web_ai_complete_json_audit`
- `audit_complete_json_payload` -> `kanda_reasoner_app.reasoner_context_collector.collector_web_ai_complete_json_audit`
- `build_active_code_index` -> `kanda_reasoner_app.reasoner_context_collector.collector_active_code`
- `build_active_code_summary` -> `kanda_reasoner_app.reasoner_context_collector.collector_active_code`
- `build_attribute_state_map` -> `kanda_reasoner_app.reasoner_context_collector.collector_state`
- `build_boundary_handoffs` -> `kanda_reasoner_app.reasoner_context_collector.collector_boundaries`
- `build_boundary_index` -> `kanda_reasoner_app.reasoner_context_collector.collector_boundaries`
- `build_boundary_summary` -> `kanda_reasoner_app.reasoner_context_collector.collector_boundaries`
- `build_boundary_violation_hotspots` -> `kanda_reasoner_app.reasoner_context_collector.collector_boundary_violations`
- `build_boundary_violation_index` -> `kanda_reasoner_app.reasoner_context_collector.collector_boundary_violations`
- `build_boundary_violation_summary` -> `kanda_reasoner_app.reasoner_context_collector.collector_boundary_violations`
- `build_bucket_hotspots` -> `kanda_reasoner_app.reasoner_context_collector.collector_bucket_insights`
- `build_bucket_index` -> `kanda_reasoner_app.reasoner_context_collector.collector_buckets`
- `build_bucket_insights` -> `kanda_reasoner_app.reasoner_context_collector.collector_bucket_insights`
- `build_bucket_priority_summary` -> `kanda_reasoner_app.reasoner_context_collector.collector_bucket_insights`
- `build_bucket_summary` -> `kanda_reasoner_app.reasoner_context_collector.collector_buckets`
- `build_bucket_warning_summary` -> `kanda_reasoner_app.reasoner_context_collector.collector_bucket_insights`
- `build_canonical_conflict_index` -> `kanda_reasoner_app.reasoner_context_collector.collector_canonical_conflicts`
- `build_canonical_conflict_summary` -> `kanda_reasoner_app.reasoner_context_collector.collector_canonical_conflicts`
- `build_change_impact` -> `kanda_reasoner_app.reasoner_context_collector.collector_dump_mapper`
- `build_change_impact_index` -> `kanda_reasoner_app.reasoner_context_collector.collector_change_impact`
- `build_change_impact_summary` -> `kanda_reasoner_app.reasoner_context_collector.collector_change_impact`
- `build_collection_config` -> `kanda_reasoner_app.reasoner_context_collector.collector_output`
- `build_collector_info` -> `kanda_reasoner_app.reasoner_context_collector.collector_output`
- `build_collector_output_audit` -> `kanda_reasoner_app.reasoner_context_collector.collector_web_ai_contract`
- `build_collector_scope` -> `kanda_reasoner_app.reasoner_context_collector.collector_output`
- `build_config_schema_registry` -> `kanda_reasoner_app.reasoner_context_collector.collector_config_schema`
- `build_config_schema_summary` -> `kanda_reasoner_app.reasoner_context_collector.collector_config_schema`
- `build_control_flow` -> `kanda_reasoner_app.reasoner_context_collector.collector_control_flow`
- `build_data_flow` -> `kanda_reasoner_app.reasoner_context_collector.collector_data_flow`
- `build_docstring_summary` -> `kanda_reasoner_app.reasoner_context_collector.collector_docstrings`
- `build_edit_ready_source_summary` -> `kanda_reasoner_app.reasoner_context_collector.collector_edit_ready_source`
- `build_edit_ready_symbol_index` -> `kanda_reasoner_app.reasoner_context_collector.collector_edit_ready_source`
- `build_entry_bucket_flow_summary` -> `kanda_reasoner_app.reasoner_context_collector.collector_entry_bucket_flows`
- `build_entry_bucket_flows` -> `kanda_reasoner_app.reasoner_context_collector.collector_entry_bucket_flows`
- `build_entry_points_detail` -> `kanda_reasoner_app.reasoner_context_collector.collector_entry_points_detail`
- `build_entry_points_detail_summary` -> `kanda_reasoner_app.reasoner_context_collector.collector_entry_points_detail`
- `build_event_propagation` -> `kanda_reasoner_app.reasoner_context_collector.collector_dump_mapper`
- `build_event_propagation_hotspots` -> `kanda_reasoner_app.reasoner_context_collector.collector_event_propagation`
- `build_event_propagation_index` -> `kanda_reasoner_app.reasoner_context_collector.collector_event_propagation`
- `build_event_propagation_summary` -> `kanda_reasoner_app.reasoner_context_collector.collector_event_propagation`
- `build_execution_chains` -> `kanda_reasoner_app.reasoner_context_collector.collector_chains`
- `build_feature_hotspots` -> `kanda_reasoner_app.reasoner_context_collector.collector_feature_registry`
- `build_feature_registry` -> `kanda_reasoner_app.reasoner_context_collector.collector_feature_registry`
- `build_feature_summary` -> `kanda_reasoner_app.reasoner_context_collector.collector_feature_registry`
- `build_file_priority_index` -> `kanda_reasoner_app.reasoner_context_collector.collector_priority`
- `build_high_risk_edit_hotspots` -> `kanda_reasoner_app.reasoner_context_collector.collector_change_impact`
- `build_implementation_chronology_index` -> `kanda_reasoner_app.reasoner_context_collector.collector_implementation_chronology`
- `build_implementation_chronology_summary` -> `kanda_reasoner_app.reasoner_context_collector.collector_implementation_chronology`
- `build_legacy_shadow_hotspots` -> `kanda_reasoner_app.reasoner_context_collector.collector_canonical_conflicts`
- `build_legacy_snippet_index_from_edit_ready` -> `kanda_reasoner_app.reasoner_context_collector.collector_edit_ready_source`
- `build_limitations_section` -> `kanda_reasoner_app.reasoner_context_collector.collector_output`
- `build_local_change_impact` -> `kanda_reasoner_app.reasoner_context_collector.collector_dump_mapper`
- `build_local_event_propagation` -> `kanda_reasoner_app.reasoner_context_collector.collector_dump_mapper`
- `build_local_symbol_index_with_enrichment` -> `kanda_reasoner_app.reasoner_context_collector.collector_dump_mapper`
- `build_migration_transition_hotspots` -> `kanda_reasoner_app.reasoner_context_collector.collector_implementation_chronology`
- `build_module_centrality_index` -> `kanda_reasoner_app.reasoner_context_collector.collector_centrality`
- `build_module_responsibility_summary` -> `kanda_reasoner_app.reasoner_context_collector.collector_module_summary`
- `build_object_ownership_map` -> `kanda_reasoner_app.reasoner_context_collector.collector_ownership`
- `build_orchestration_hotspots` -> `kanda_reasoner_app.reasoner_context_collector.collector_orchestration`
- `build_orchestration_index` -> `kanda_reasoner_app.reasoner_context_collector.collector_orchestration`
- `build_orchestration_summary` -> `kanda_reasoner_app.reasoner_context_collector.collector_orchestration`
- `build_overlap_hotspots` -> `kanda_reasoner_app.reasoner_context_collector.collector_responsibility_overlap`
- `build_persistence_io_hotspots` -> `kanda_reasoner_app.reasoner_context_collector.collector_persistence_io`
- `build_persistence_io_index` -> `kanda_reasoner_app.reasoner_context_collector.collector_persistence_io`
- `build_persistence_io_summary` -> `kanda_reasoner_app.reasoner_context_collector.collector_persistence_io`
- `build_primary_definition_index` -> `kanda_reasoner_app.reasoner_context_collector.collector_primary_definition_index`
- `build_primary_definition_summary` -> `kanda_reasoner_app.reasoner_context_collector.collector_primary_definition_index`
- `build_priority_ranking` -> `kanda_reasoner_app.reasoner_context_collector.collector_priority`
- `build_responsibility_overlap_index` -> `kanda_reasoner_app.reasoner_context_collector.collector_responsibility_overlap`
- `build_responsibility_overlap_summary` -> `kanda_reasoner_app.reasoner_context_collector.collector_responsibility_overlap`
- `build_runtime_feature_attribution_hotspots` -> `kanda_reasoner_app.reasoner_context_collector.collector_runtime_feature_attribution`
- `build_runtime_feature_attribution_index` -> `kanda_reasoner_app.reasoner_context_collector.collector_runtime_feature_attribution`
- `build_runtime_feature_attribution_summary` -> `kanda_reasoner_app.reasoner_context_collector.collector_runtime_feature_attribution`
- `build_runtime_trace_index` -> `kanda_reasoner_app.reasoner_context_collector.collector_runtime_trace`
- `build_schema_risk_hotspots` -> `kanda_reasoner_app.reasoner_context_collector.collector_config_schema`
- `build_source_file_index` -> `kanda_reasoner_app.reasoner_context_collector.collector_edit_ready_source`
- `build_stable_evidence_id_index` -> `kanda_reasoner_app.reasoner_context_collector.collector_stable_evidence_id_index`
- `build_stable_evidence_id_summary` -> `kanda_reasoner_app.reasoner_context_collector.collector_stable_evidence_id_index`
- `build_state_lifecycle_hotspots` -> `kanda_reasoner_app.reasoner_context_collector.collector_state_lifecycle`
- `build_state_lifecycle_index` -> `kanda_reasoner_app.reasoner_context_collector.collector_state_lifecycle`
- `build_state_lifecycle_summary` -> `kanda_reasoner_app.reasoner_context_collector.collector_state_lifecycle`
- `build_state_mutation_hotspots` -> `kanda_reasoner_app.reasoner_context_collector.collector_state_mutations`
- `build_state_mutation_index` -> `kanda_reasoner_app.reasoner_context_collector.collector_state_mutations`
- `build_state_mutation_summary` -> `kanda_reasoner_app.reasoner_context_collector.collector_state_mutations`
- `build_subsystem_summaries` -> `kanda_reasoner_app.reasoner_context_collector.collector_subsystems`
- `build_symbol_centrality_index` -> `kanda_reasoner_app.reasoner_context_collector.collector_centrality`
- `build_symbol_index_with_enrichment` -> `kanda_reasoner_app.reasoner_context_collector.collector_dump_mapper`
- `build_top_project_hotspots` -> `kanda_reasoner_app.reasoner_context_collector.collector_centrality`
- `build_ui_action_hotspots` -> `kanda_reasoner_app.reasoner_context_collector.collector_ui_actions`
- `build_ui_action_index` -> `kanda_reasoner_app.reasoner_context_collector.collector_ui_actions`
- `build_ui_action_summary` -> `kanda_reasoner_app.reasoner_context_collector.collector_ui_actions`
- `build_untested_critical_hotspots` -> `kanda_reasoner_app.reasoner_context_collector.collector_active_code`
- `build_web_ai_file_responsibility_index` -> `kanda_reasoner_app.reasoner_context_collector.collector_web_ai_file_responsibility_index`
- `build_web_ai_file_responsibility_summary` -> `kanda_reasoner_app.reasoner_context_collector.collector_web_ai_file_responsibility_index`
- `build_web_ai_readme` -> `kanda_reasoner_app.reasoner_context_collector.collector_web_ai_readme`
- `build_web_ai_readme_summary` -> `kanda_reasoner_app.reasoner_context_collector.collector_web_ai_readme`
- `build_web_ai_sections` -> `kanda_reasoner_app.reasoner_context_collector.complete_json_web_ai_enrichment`
- `build_web_ai_symbol_index` -> `kanda_reasoner_app.reasoner_context_collector.collector_web_ai_symbol_index`
- `build_web_ai_symbol_summary` -> `kanda_reasoner_app.reasoner_context_collector.collector_web_ai_symbol_index`
- `build_web_ai_test_protection_index` -> `kanda_reasoner_app.reasoner_context_collector.collector_web_ai_test_protection_index`
- `build_web_ai_test_protection_summary` -> `kanda_reasoner_app.reasoner_context_collector.collector_web_ai_test_protection_index`
- `build_widget_hotspots` -> `kanda_reasoner_app.reasoner_context_collector.collector_widget_summary`
- `build_widget_layout_hotspots` -> `kanda_reasoner_app.reasoner_context_collector.collector_widget_layout_index`
- `build_widget_layout_index` -> `kanda_reasoner_app.reasoner_context_collector.collector_widget_layout_index`
- `build_widget_registry` -> `kanda_reasoner_app.reasoner_context_collector.collector_widget_registry`
- `build_widget_summary` -> `kanda_reasoner_app.reasoner_context_collector.collector_widget_summary`
- `build_widget_text_hotspots` -> `kanda_reasoner_app.reasoner_context_collector.collector_widget_text_index`
- `build_widget_text_index` -> `kanda_reasoner_app.reasoner_context_collector.collector_widget_text_index`
- `build_widget_ui_action_bridge` -> `kanda_reasoner_app.reasoner_context_collector.collector_widget_ui_action_bridge`
- `build_widget_ui_action_hotspots` -> `kanda_reasoner_app.reasoner_context_collector.collector_widget_ui_action_bridge`
- `classify_file_bucket` -> `kanda_reasoner_app.reasoner_context_collector.collector_buckets`
- `collect_coverage_for_file` -> `kanda_reasoner_app.reasoner_context_collector.collector_coverage`
- `collect_git_metadata_for_file` -> `kanda_reasoner_app.reasoner_context_collector.collector_git`
- `compact_whitespace` -> `kanda_reasoner_app.reasoner_context_collector.collector_utils`
- `complete_json_path_for_project` -> `kanda_reasoner_app.reasoner_context_collector.complete_json_web_ai_enrichment`
- `derive_reset_chain` -> `kanda_reasoner_app.reasoner_context_collector.collector_chains`
- `derive_startup_chain` -> `kanda_reasoner_app.reasoner_context_collector.collector_chains`
- `derive_timeline_chain` -> `kanda_reasoner_app.reasoner_context_collector.collector_chains`
- `derive_topomap_chain` -> `kanda_reasoner_app.reasoner_context_collector.collector_chains`
- `enrich_complete_json_for_web_ai` -> `kanda_reasoner_app.reasoner_context_collector.complete_json_web_ai_enrichment`
- `enrich_project_complete_json` -> `kanda_reasoner_app.reasoner_context_collector.complete_json_web_ai_enrichment`
- `extract_global_state` -> `kanda_reasoner_app.reasoner_context_collector.collector_dump_mapper`
- `extract_localization` -> `kanda_reasoner_app.reasoner_context_collector.collector_dump_mapper`
- `extract_qt_signal_map` -> `kanda_reasoner_app.reasoner_context_collector.collector_qt`
- `fail` -> `kanda_reasoner_app.reasoner_context_collector.collector_runtime_scenarios_validate_manifests`
- `find_duplicate_symbols` -> `kanda_reasoner_app.reasoner_context_collector.collector_duplicates`
- `get_entry_chain_summary` -> `kanda_reasoner_app.reasoner_context_collector.collector_insights`
- `get_project_hotspot_summary` -> `kanda_reasoner_app.reasoner_context_collector.collector_insights`
- `get_top_central_symbols` -> `kanda_reasoner_app.reasoner_context_collector.collector_insights`
- `get_top_priority_files` -> `kanda_reasoner_app.reasoner_context_collector.collector_insights`
- `has_module_docstring` -> `kanda_reasoner_app.reasoner_context_collector.collector_widget_ui_action_bridge_validate_manifests`
- `is_inside_project` -> `kanda_reasoner_app.reasoner_context_collector.collector_scope`
- `iter_project_documentation_files` -> `kanda_reasoner_app.reasoner_context_collector.collector_scope`
- `iter_project_files` -> `kanda_reasoner_app.reasoner_context_collector.collector_scope`
- `iter_project_packaging_files` -> `kanda_reasoner_app.reasoner_context_collector.collector_scope`
- `iter_project_python_files` -> `kanda_reasoner_app.reasoner_context_collector.collector_scope`
- `line_count` -> `kanda_reasoner_app.reasoner_context_collector.collector_responsibility_overlap_validate_manifests`
- `link_tests_to_sources` -> `kanda_reasoner_app.reasoner_context_collector.collector_tests`
- `make_empty_index_payload` -> `kanda_reasoner_app.reasoner_context_collector.runner`
- `normalize_file_warning_records` -> `kanda_reasoner_app.reasoner_context_collector.collector_warnings`
- `normalize_path` -> `kanda_reasoner_app.reasoner_context_collector.collector_utils`
- `parse_python_file` -> `kanda_reasoner_app.reasoner_context_collector.collector_ast`
- `parse_python_source_with_warnings` -> `kanda_reasoner_app.reasoner_context_collector.collector_warnings`
- `resolve_output_json_path` -> `kanda_reasoner_app.reasoner_context_collector.runner`
- `resolve_project_root` -> `kanda_reasoner_app.reasoner_context_collector.collector_scope`
- `safe_json_dump` -> `kanda_reasoner_app.reasoner_context_collector.collector_utils`
- `sanitize_collector_outputs` -> `kanda_reasoner_app.reasoner_context_collector.collector_scope`
- `sanitize_for_json` -> `kanda_reasoner_app.reasoner_context_collector.collector_utils`
- `sanitize_json_file` -> `kanda_reasoner_app.reasoner_context_collector.collector_scope`
- `short_hash` -> `kanda_reasoner_app.reasoner_context_collector.collector_utils`
- `should_exclude_dir` -> `kanda_reasoner_app.reasoner_context_collector.collector_filters`
- `should_exclude_file` -> `kanda_reasoner_app.reasoner_context_collector.collector_filters`
- `summarize_file_semantics` -> `kanda_reasoner_app.reasoner_context_collector.collector_roles`
- `summarize_symbol_semantics` -> `kanda_reasoner_app.reasoner_context_collector.collector_roles`
- `validate_collector_output_contract` -> `kanda_reasoner_app.reasoner_context_collector.collector_web_ai_contract`
- `walk_python_files_filtered` -> `kanda_reasoner_app.reasoner_context_collector.collector_walker`

### kanda_reasoner_app.reasoner_context_collector.collector_main_help

| Module | Owns | Exposes | Depends On | Used By | Helper Group |
|---|---|---|---|---|---|
| `kanda_reasoner_app.reasoner_context_collector.collector_main_help` |  |  |  |  | collector_main |
| `kanda_reasoner_app.reasoner_context_collector.collector_main_help.collector_main_source_part_1_private_impl` |  |  |  |  | collector_main |
| `kanda_reasoner_app.reasoner_context_collector.collector_main_help.collector_main_source_part_2_private_impl` |  |  |  |  | collector_main |
| `kanda_reasoner_app.reasoner_context_collector.collector_main_help.collector_main_source_part_3_private_impl` |  |  |  |  | collector_main |
| `kanda_reasoner_app.reasoner_context_collector.collector_main_help.collector_main_source_part_4_private_impl` |  |  |  |  | collector_main |
| `kanda_reasoner_app.reasoner_context_collector.collector_main_help.collector_main_source_part_5_private_impl` |  |  |  |  | collector_main |

**Helper Groups**

- `collector_main` -> main `kanda_reasoner_app.reasoner_context_collector.collector_main`
  - `kanda_reasoner_app.reasoner_context_collector.collector_main_help`
  - `kanda_reasoner_app.reasoner_context_collector.collector_main_help.collector_main_source_part_1_private_impl`
  - `kanda_reasoner_app.reasoner_context_collector.collector_main_help.collector_main_source_part_2_private_impl`
  - `kanda_reasoner_app.reasoner_context_collector.collector_main_help.collector_main_source_part_3_private_impl`
  - `kanda_reasoner_app.reasoner_context_collector.collector_main_help.collector_main_source_part_4_private_impl`
  - `kanda_reasoner_app.reasoner_context_collector.collector_main_help.collector_main_source_part_5_private_impl`

### kanda_reasoner_app.reasoner_context_collector.collector_responsibility_overlap_help

| Module | Owns | Exposes | Depends On | Used By | Helper Group |
|---|---|---|---|---|---|
| `kanda_reasoner_app.reasoner_context_collector.collector_responsibility_overlap_help` |  |  |  |  | collector_responsibility_overlap |
| `kanda_reasoner_app.reasoner_context_collector.collector_responsibility_overlap_help.extraction` |  |  |  | kanda_reasoner_app.reasoner_context_collector.collector_responsibility_overlap | collector_responsibility_overlap |
| `kanda_reasoner_app.reasoner_context_collector.collector_responsibility_overlap_help.scoring` |  |  |  | kanda_reasoner_app.reasoner_context_collector.collector_responsibility_overlap | collector_responsibility_overlap |

**Helper Groups**

- `collector_responsibility_overlap` -> main `kanda_reasoner_app.reasoner_context_collector.collector_responsibility_overlap`
  - `kanda_reasoner_app.reasoner_context_collector.collector_responsibility_overlap_help`
  - `kanda_reasoner_app.reasoner_context_collector.collector_responsibility_overlap_help.extraction`
  - `kanda_reasoner_app.reasoner_context_collector.collector_responsibility_overlap_help.scoring`

### kanda_reasoner_app.reasoner_context_collector.collector_runtime_scenarios_help

| Module | Owns | Exposes | Depends On | Used By | Helper Group |
|---|---|---|---|---|---|
| `kanda_reasoner_app.reasoner_context_collector.collector_runtime_scenarios_help` |  |  |  |  | collector_runtime_scenarios |
| `kanda_reasoner_app.reasoner_context_collector.collector_runtime_scenarios_help.event_classification` |  |  | kanda_reasoner_app.backend_payloads.loader |  | collector_runtime_scenarios |
| `kanda_reasoner_app.reasoner_context_collector.collector_runtime_scenarios_help.hotspots` |  |  | kanda_reasoner_app.backend_payloads.loader |  | collector_runtime_scenarios |
| `kanda_reasoner_app.reasoner_context_collector.collector_runtime_scenarios_help.normalization` |  |  |  |  | collector_runtime_scenarios |

**Helper Groups**

- `collector_runtime_scenarios` -> main `kanda_reasoner_app.reasoner_context_collector.collector_runtime_scenarios`
  - `kanda_reasoner_app.reasoner_context_collector.collector_runtime_scenarios_help`
  - `kanda_reasoner_app.reasoner_context_collector.collector_runtime_scenarios_help.event_classification`
  - `kanda_reasoner_app.reasoner_context_collector.collector_runtime_scenarios_help.hotspots`
  - `kanda_reasoner_app.reasoner_context_collector.collector_runtime_scenarios_help.normalization`

### kanda_reasoner_app.reasoner_context_collector.collector_widget_registry_help

| Module | Owns | Exposes | Depends On | Used By | Helper Group |
|---|---|---|---|---|---|
| `kanda_reasoner_app.reasoner_context_collector.collector_widget_registry_help` |  |  |  | kanda_reasoner_app.reasoner_context_collector.collector_widget_registry | collector_widget_registry |
| `kanda_reasoner_app.reasoner_context_collector.collector_widget_registry_help.widget_registry_methods_part_1_private_impl` |  |  |  |  | collector_widget_registry |

**Helper Groups**

- `collector_widget_registry` -> main `kanda_reasoner_app.reasoner_context_collector.collector_widget_registry`
  - `kanda_reasoner_app.reasoner_context_collector.collector_widget_registry_help`
  - `kanda_reasoner_app.reasoner_context_collector.collector_widget_registry_help.widget_registry_methods_part_1_private_impl`

### kanda_reasoner_app.reasoner_context_collector.collector_widget_ui_action_bridge_help

| Module | Owns | Exposes | Depends On | Used By | Helper Group |
|---|---|---|---|---|---|
| `kanda_reasoner_app.reasoner_context_collector.collector_widget_ui_action_bridge_help` |  |  | kanda_reasoner_app.reasoner_context_collector.collector_widget_ui_action_bridge_help.indexing, kanda_reasoner_app.reasoner_context_collector.collector_widget_ui_action_bridge_help.matching, kanda_reasoner_app.reasoner_context_collector.collector_widget_ui_action_bridge_help.normalization | kanda_reasoner_app.reasoner_context_collector.collector_widget_ui_action_bridge | collector_widget_ui_action_bridge |
| `kanda_reasoner_app.reasoner_context_collector.collector_widget_ui_action_bridge_help.indexing` |  |  | kanda_reasoner_app.reasoner_context_collector.collector_widget_ui_action_bridge_help.normalization | kanda_reasoner_app.reasoner_context_collector.collector_widget_ui_action_bridge_help | collector_widget_ui_action_bridge |
| `kanda_reasoner_app.reasoner_context_collector.collector_widget_ui_action_bridge_help.matching` |  |  | kanda_reasoner_app.reasoner_context_collector.collector_widget_ui_action_bridge_help.normalization | kanda_reasoner_app.reasoner_context_collector.collector_widget_ui_action_bridge_help | collector_widget_ui_action_bridge |
| `kanda_reasoner_app.reasoner_context_collector.collector_widget_ui_action_bridge_help.normalization` |  |  |  | kanda_reasoner_app.reasoner_context_collector.collector_widget_ui_action_bridge_help, kanda_reasoner_app.reasoner_context_collector.collector_widget_ui_action_bridge_help.indexing, kanda_reasoner_app.reasoner_context_collector.collector_widget_ui_action_bridge_help.matching | collector_widget_ui_action_bridge |

**Helper Groups**

- `collector_widget_ui_action_bridge` -> main `kanda_reasoner_app.reasoner_context_collector.collector_widget_ui_action_bridge`
  - `kanda_reasoner_app.reasoner_context_collector.collector_widget_ui_action_bridge_help`
  - `kanda_reasoner_app.reasoner_context_collector.collector_widget_ui_action_bridge_help.indexing`
  - `kanda_reasoner_app.reasoner_context_collector.collector_widget_ui_action_bridge_help.matching`
  - `kanda_reasoner_app.reasoner_context_collector.collector_widget_ui_action_bridge_help.normalization`

### kanda_reasoner_app.reasoner_context_collector.collectors

| Module | Owns | Exposes | Depends On | Used By | Helper Group |
|---|---|---|---|---|---|
| `kanda_reasoner_app.reasoner_context_collector.collectors` |  | collect_documentation_intent, collect_packaging_metadata | kanda_reasoner_app.reasoner_context_collector.collectors.static_context |  |  |

### kanda_reasoner_app.reasoner_context_collector.collectors.static_context

| Module | Owns | Exposes | Depends On | Used By | Helper Group |
|---|---|---|---|---|---|
| `kanda_reasoner_app.reasoner_context_collector.collectors.static_context` |  | collect_documentation_intent, collect_packaging_metadata | kanda_reasoner_app.reasoner_context_collector.collectors.static_context.collector_documentation_intent, kanda_reasoner_app.reasoner_context_collector.collectors.static_context.collector_packaging_metadata | kanda_reasoner_app.reasoner_context_collector.collectors |  |
| `kanda_reasoner_app.reasoner_context_collector.collectors.static_context.collector_documentation_intent` |  | collect_documentation_intent | kanda_reasoner_app.reasoner_context_collector.collector_config, kanda_reasoner_app.reasoner_context_collector.parsers | kanda_reasoner_app.reasoner_context_collector.collectors.static_context |  |
| `kanda_reasoner_app.reasoner_context_collector.collectors.static_context.collector_packaging_metadata` |  | collect_packaging_metadata | kanda_reasoner_app.reasoner_context_collector.collector_config, kanda_reasoner_app.reasoner_context_collector.parsers | kanda_reasoner_app.reasoner_context_collector.collectors.static_context |  |

**Public Symbol Quick Reference**

- `collect_documentation_intent` -> `kanda_reasoner_app.reasoner_context_collector.collectors.static_context.collector_documentation_intent`
- `collect_packaging_metadata` -> `kanda_reasoner_app.reasoner_context_collector.collectors.static_context.collector_packaging_metadata`

### kanda_reasoner_app.reasoner_context_collector.developer_tools

| Module | Owns | Exposes | Depends On | Used By | Helper Group |
|---|---|---|---|---|---|
| `kanda_reasoner_app.reasoner_context_collector.developer_tools` |  | collect_documentation_intent, collect_packaging_metadata | kanda_reasoner_app.reasoner_context_collector.developer_tools.collector_documentation_intent, kanda_reasoner_app.reasoner_context_collector.developer_tools.collector_packaging_metadata |  |  |

### kanda_reasoner_app.reasoner_context_collector.developer_tools.project_reasoner

| Module | Owns | Exposes | Depends On | Used By | Helper Group |
|---|---|---|---|---|---|
| `kanda_reasoner_app.reasoner_context_collector.developer_tools.project_reasoner` |  | collect_documentation_intent, collect_packaging_metadata | kanda_reasoner_app.reasoner_context_collector.developer_tools.project_reasoner.collector_documentation_intent, kanda_reasoner_app.reasoner_context_collector.developer_tools.project_reasoner.collector_packaging_metadata |  |  |

### kanda_reasoner_app.reasoner_context_collector.developer_tools.project_reasoner.reasoner_context_collector

| Module | Owns | Exposes | Depends On | Used By | Helper Group |
|---|---|---|---|---|---|
| `kanda_reasoner_app.reasoner_context_collector.developer_tools.project_reasoner.reasoner_context_collector` |  | collect_documentation_intent, collect_packaging_metadata | kanda_reasoner_app.reasoner_context_collector.developer_tools.project_reasoner.reasoner_context_collector.collector_documentation_intent, kanda_reasoner_app.reasoner_context_collector.developer_tools.project_reasoner.reasoner_context_collector.collector_packaging_metadata |  |  |

### kanda_reasoner_app.reasoner_context_collector.developer_tools.project_reasoner.reasoner_context_collector.outputs

| Module | Owns | Exposes | Depends On | Used By | Helper Group |
|---|---|---|---|---|---|
| `kanda_reasoner_app.reasoner_context_collector.developer_tools.project_reasoner.reasoner_context_collector.outputs` |  | collect_documentation_intent, collect_packaging_metadata | kanda_reasoner_app.reasoner_context_collector.developer_tools.project_reasoner.reasoner_context_collector.outputs.collector_documentation_intent, kanda_reasoner_app.reasoner_context_collector.developer_tools.project_reasoner.reasoner_context_collector.outputs.collector_packaging_metadata |  |  |

### kanda_reasoner_app.reasoner_context_collector.parsers

| Module | Owns | Exposes | Depends On | Used By | Helper Group |
|---|---|---|---|---|---|
| `kanda_reasoner_app.reasoner_context_collector.parsers` |  | parse_documentation_intent, parse_packaging_metadata | kanda_reasoner_app.reasoner_context_collector.parsers.static_context | kanda_reasoner_app.reasoner_context_collector.collectors.static_context.collector_documentation_intent, kanda_reasoner_app.reasoner_context_collector.collectors.static_context.collector_packaging_metadata |  |

### kanda_reasoner_app.reasoner_context_collector.parsers.static_context

| Module | Owns | Exposes | Depends On | Used By | Helper Group |
|---|---|---|---|---|---|
| `kanda_reasoner_app.reasoner_context_collector.parsers.static_context` |  | parse_documentation_intent, parse_packaging_metadata | kanda_reasoner_app.reasoner_context_collector.parsers.static_context.documentation_intent_parser, kanda_reasoner_app.reasoner_context_collector.parsers.static_context.packaging_metadata_parser | kanda_reasoner_app.reasoner_context_collector.parsers |  |
| `kanda_reasoner_app.reasoner_context_collector.parsers.static_context.documentation_intent_parser` |  | DEFAULT_DOCUMENTATION_GLOB_PATTERNS, parse_documentation_intent | kanda_reasoner_app.reasoner_context_collector.collector_scope | kanda_reasoner_app.reasoner_context_collector.parsers.static_context |  |
| `kanda_reasoner_app.reasoner_context_collector.parsers.static_context.packaging_metadata_parser` |  | DEFAULT_PACKAGING_FILE_PATTERNS, parse_packaging_metadata | kanda_reasoner_app.reasoner_context_collector.collector_scope | kanda_reasoner_app.reasoner_context_collector.parsers.static_context |  |

**Public Symbol Quick Reference**

- `DEFAULT_DOCUMENTATION_GLOB_PATTERNS` -> `kanda_reasoner_app.reasoner_context_collector.parsers.static_context.documentation_intent_parser`
- `DEFAULT_PACKAGING_FILE_PATTERNS` -> `kanda_reasoner_app.reasoner_context_collector.parsers.static_context.packaging_metadata_parser`
- `parse_documentation_intent` -> `kanda_reasoner_app.reasoner_context_collector.parsers.static_context.documentation_intent_parser`
- `parse_packaging_metadata` -> `kanda_reasoner_app.reasoner_context_collector.parsers.static_context.packaging_metadata_parser`

### kanda_reasoner_app.reasoner_context_collector.project_reasoner_data_collector_logic

| Module | Owns | Exposes | Depends On | Used By | Helper Group |
|---|---|---|---|---|---|
| `kanda_reasoner_app.reasoner_context_collector.project_reasoner_data_collector_logic` |  | FolderSelectionWindow, build_part_document, get_entries, get_nested_value, json_bytes, parse_target_path, rebuild_container, set_nested_value, split_json, stable_hash |  |  |  |

### kanda_reasoner_app.reasoner_runtime_collector

| Module | Owns | Exposes | Depends On | Used By | Helper Group |
|---|---|---|---|---|---|
| `kanda_reasoner_app.reasoner_runtime_collector` |  |  | kanda_reasoner_app.reasoner_runtime_collector.runtime_trace_api |  |  |
| `kanda_reasoner_app.reasoner_runtime_collector.runtime_runner` |  | DEFAULT_OUTPUT_JSON, RuntimeCollectorWindow, main | kanda_reasoner_app.backend_payloads.loader |  |  |
| `kanda_reasoner_app.reasoner_runtime_collector.runtime_runner_validate_manifests` |  | BASE, HELPERS, HELP_DIR, MANIFEST, ORIGIN, ROOT, main |  |  |  |
| `kanda_reasoner_app.reasoner_runtime_collector.runtime_trace_api` |  | configure_runtime_trace, get_runtime_trace_writer, is_runtime_trace_configured, reset_runtime_trace, save_runtime_trace, trace_error, trace_event, trace_signal_connection, trace_state_snapshot | kanda_reasoner_app.reasoner_runtime_collector.runtime_trace_writer | kanda_reasoner_app.reasoner_runtime_collector |  |
| `kanda_reasoner_app.reasoner_runtime_collector.runtime_trace_decorators` |  | trace_runtime_event |  |  |  |
| `kanda_reasoner_app.reasoner_runtime_collector.runtime_trace_models` |  | TraceEvent, TraceIssue, TraceSignalConnection, TraceStateSnapshot |  | kanda_reasoner_app.reasoner_runtime_collector.runtime_trace_writer |  |
| `kanda_reasoner_app.reasoner_runtime_collector.runtime_trace_state` |  | collect_visualizer_state |  |  |  |
| `kanda_reasoner_app.reasoner_runtime_collector.runtime_trace_utils` |  | now_iso, safe_json_dump, sanitize_data, sanitize_text |  | kanda_reasoner_app.reasoner_runtime_collector.runtime_trace_writer |  |
| `kanda_reasoner_app.reasoner_runtime_collector.runtime_trace_writer` |  | RuntimeTraceWriter | kanda_reasoner_app.reasoner_runtime_collector.runtime_trace_models, kanda_reasoner_app.reasoner_runtime_collector.runtime_trace_utils | kanda_reasoner_app.reasoner_runtime_collector.runtime_trace_api |  |

**Public Symbol Quick Reference**

- `BASE` -> `kanda_reasoner_app.reasoner_runtime_collector.runtime_runner_validate_manifests`
- `DEFAULT_OUTPUT_JSON` -> `kanda_reasoner_app.reasoner_runtime_collector.runtime_runner`
- `HELPERS` -> `kanda_reasoner_app.reasoner_runtime_collector.runtime_runner_validate_manifests`
- `HELP_DIR` -> `kanda_reasoner_app.reasoner_runtime_collector.runtime_runner_validate_manifests`
- `MANIFEST` -> `kanda_reasoner_app.reasoner_runtime_collector.runtime_runner_validate_manifests`
- `ORIGIN` -> `kanda_reasoner_app.reasoner_runtime_collector.runtime_runner_validate_manifests`
- `ROOT` -> `kanda_reasoner_app.reasoner_runtime_collector.runtime_runner_validate_manifests`
- `RuntimeCollectorWindow` -> `kanda_reasoner_app.reasoner_runtime_collector.runtime_runner`
- `RuntimeTraceWriter` -> `kanda_reasoner_app.reasoner_runtime_collector.runtime_trace_writer`
- `TraceEvent` -> `kanda_reasoner_app.reasoner_runtime_collector.runtime_trace_models`
- `TraceIssue` -> `kanda_reasoner_app.reasoner_runtime_collector.runtime_trace_models`
- `TraceSignalConnection` -> `kanda_reasoner_app.reasoner_runtime_collector.runtime_trace_models`
- `TraceStateSnapshot` -> `kanda_reasoner_app.reasoner_runtime_collector.runtime_trace_models`
- `collect_visualizer_state` -> `kanda_reasoner_app.reasoner_runtime_collector.runtime_trace_state`
- `configure_runtime_trace` -> `kanda_reasoner_app.reasoner_runtime_collector.runtime_trace_api`
- `get_runtime_trace_writer` -> `kanda_reasoner_app.reasoner_runtime_collector.runtime_trace_api`
- `is_runtime_trace_configured` -> `kanda_reasoner_app.reasoner_runtime_collector.runtime_trace_api`
- `now_iso` -> `kanda_reasoner_app.reasoner_runtime_collector.runtime_trace_utils`
- `reset_runtime_trace` -> `kanda_reasoner_app.reasoner_runtime_collector.runtime_trace_api`
- `safe_json_dump` -> `kanda_reasoner_app.reasoner_runtime_collector.runtime_trace_utils`
- `sanitize_data` -> `kanda_reasoner_app.reasoner_runtime_collector.runtime_trace_utils`
- `sanitize_text` -> `kanda_reasoner_app.reasoner_runtime_collector.runtime_trace_utils`
- `save_runtime_trace` -> `kanda_reasoner_app.reasoner_runtime_collector.runtime_trace_api`
- `trace_error` -> `kanda_reasoner_app.reasoner_runtime_collector.runtime_trace_api`
- `trace_event` -> `kanda_reasoner_app.reasoner_runtime_collector.runtime_trace_api`
- `trace_runtime_event` -> `kanda_reasoner_app.reasoner_runtime_collector.runtime_trace_decorators`
- `trace_signal_connection` -> `kanda_reasoner_app.reasoner_runtime_collector.runtime_trace_api`
- `trace_state_snapshot` -> `kanda_reasoner_app.reasoner_runtime_collector.runtime_trace_api`

### kanda_reasoner_app.reasoner_runtime_collector.hooks

| Module | Owns | Exposes | Depends On | Used By | Helper Group |
|---|---|---|---|---|---|
| `kanda_reasoner_app.reasoner_runtime_collector.hooks` |  | CURRENT_DIR, PROJECT_DIR, TestQtConnectionMonitor |  |  |  |
| `kanda_reasoner_app.reasoner_runtime_collector.hooks.qt_connection_monitor` |  | CURRENT_DIR, PROJECT_DIR, TestQtConnectionMonitor |  |  |  |

**Public Symbol Quick Reference**

- `CURRENT_DIR` -> `kanda_reasoner_app.reasoner_runtime_collector.hooks.qt_connection_monitor`
- `PROJECT_DIR` -> `kanda_reasoner_app.reasoner_runtime_collector.hooks.qt_connection_monitor`
- `TestQtConnectionMonitor` -> `kanda_reasoner_app.reasoner_runtime_collector.hooks.qt_connection_monitor`

### kanda_reasoner_app.reasoner_runtime_collector.qt_hooks

| Module | Owns | Exposes | Depends On | Used By | Helper Group |
|---|---|---|---|---|---|
| `kanda_reasoner_app.reasoner_runtime_collector.qt_hooks` |  |  |  |  |  |
| `kanda_reasoner_app.reasoner_runtime_collector.qt_hooks.qt_connection_monitor` |  |  | kanda_reasoner_app.backend_payloads.loader |  |  |

### kanda_reasoner_app.reasoner_runtime_collector.runtime_runner_help

| Module | Owns | Exposes | Depends On | Used By | Helper Group |
|---|---|---|---|---|---|
| `kanda_reasoner_app.reasoner_runtime_collector.runtime_runner_help` |  |  |  |  | runtime_runner |
| `kanda_reasoner_app.reasoner_runtime_collector.runtime_runner_help.runtime_runner_part_1_private_impl` |  |  |  |  | runtime_runner |
| `kanda_reasoner_app.reasoner_runtime_collector.runtime_runner_help.runtime_runner_part_2_private_impl` |  |  |  |  | runtime_runner |
| `kanda_reasoner_app.reasoner_runtime_collector.runtime_runner_help.runtime_runner_part_3_private_impl` |  |  |  |  | runtime_runner |

**Helper Groups**

- `runtime_runner` -> main `kanda_reasoner_app.reasoner_runtime_collector.runtime_runner`
  - `kanda_reasoner_app.reasoner_runtime_collector.runtime_runner_help`
  - `kanda_reasoner_app.reasoner_runtime_collector.runtime_runner_help.runtime_runner_part_1_private_impl`
  - `kanda_reasoner_app.reasoner_runtime_collector.runtime_runner_help.runtime_runner_part_2_private_impl`
  - `kanda_reasoner_app.reasoner_runtime_collector.runtime_runner_help.runtime_runner_part_3_private_impl`

### kanda_reasoner_app.reasoner_tools_gui_shell

| Module | Owns | Exposes | Depends On | Used By | Helper Group |
|---|---|---|---|---|---|
| `kanda_reasoner_app.reasoner_tools_gui_shell` |  |  |  |  |  |
| `kanda_reasoner_app.reasoner_tools_gui_shell.app_constants` |  | APP_DISPLAY_NAME, APP_ICON_PATH, APP_TITLE_DETAIL |  | kanda_reasoner_app.reasoner_tools_gui_shell.gui_support, kanda_reasoner_app.reasoner_tools_gui_shell.main_window, kanda_reasoner_app.reasoner_tools_gui_shell.main_window_help.window_help, kanda_reasoner_app.reasoner_tools_gui_shell.main_window_help.window_state, kanda_reasoner_app.reasoner_tools_gui_shell.main_window_help.window_tool_patches |  |
| `kanda_reasoner_app.reasoner_tools_gui_shell.error_panels` |  | ToolLoadErrorPanel |  | kanda_reasoner_app.reasoner_tools_gui_shell.lazy_tabs |  |
| `kanda_reasoner_app.reasoner_tools_gui_shell.gui_support` |  |  | kanda_reasoner_app.reasoner_tools_gui_shell.app_constants | kanda_reasoner_app.reasoner_tools_gui_shell.lazy_tabs, kanda_reasoner_app.reasoner_tools_gui_shell.main_window, kanda_reasoner_app.reasoner_tools_gui_shell.main_window_help.window_tool_patches |  |
| `kanda_reasoner_app.reasoner_tools_gui_shell.ignore_rules_tab` |  | IgnoreRulesTab | kanda_reasoner_app.reasoner_tools_gui_shell.ignore_rules_tab_help.browse_state, kanda_reasoner_app.reasoner_tools_gui_shell.ignore_rules_tab_help.list_actions, kanda_reasoner_app.reasoner_tools_gui_shell.ignore_rules_tab_help.prefs_io, kanda_reasoner_app.reasoner_tools_gui_shell.ignore_rules_tab_help.rule_defaults, kanda_reasoner_app.reasoner_tools_gui_shell.ignore_rules_tab_help.ui_builders | kanda_reasoner_app.reasoner_tools_gui_shell.main_window |  |
| `kanda_reasoner_app.reasoner_tools_gui_shell.ignore_rules_tab_validate_manifests` |  | main, validate_manifest |  |  |  |
| `kanda_reasoner_app.reasoner_tools_gui_shell.launch` |  |  | kanda_reasoner_app.reasoner_tools_gui_shell.main_window | reasoner_tools_gui |  |
| `kanda_reasoner_app.reasoner_tools_gui_shell.lazy_tabs` |  | LazyToolTab | kanda_reasoner_app.reasoner_tools_gui_shell.error_panels, kanda_reasoner_app.reasoner_tools_gui_shell.gui_support, kanda_reasoner_app.reasoner_tools_gui_shell.tool_specs, kanda_reasoner_app.templates.floating_windows.float_window | kanda_reasoner_app.reasoner_tools_gui_shell.main_window |  |
| `kanda_reasoner_app.reasoner_tools_gui_shell.main_window` |  | ReasonerToolsWindow | kanda_reasoner_app.reasoner_tools_gui_shell.app_constants, kanda_reasoner_app.reasoner_tools_gui_shell.gui_support, kanda_reasoner_app.reasoner_tools_gui_shell.ignore_rules_tab, kanda_reasoner_app.reasoner_tools_gui_shell.lazy_tabs, kanda_reasoner_app.reasoner_tools_gui_shell.main_window_help.window_help, kanda_reasoner_app.reasoner_tools_gui_shell.main_window_help.window_output_paths, kanda_reasoner_app.reasoner_tools_gui_shell.main_window_help.window_project_root, kanda_reasoner_app.reasoner_tools_gui_shell.main_window_help.window_state, kanda_reasoner_app.reasoner_tools_gui_shell.main_window_help.window_tool_patches, kanda_reasoner_app.reasoner_tools_gui_shell.tool_specs | kanda_reasoner_app.reasoner_tools_gui_shell.launch |  |
| `kanda_reasoner_app.reasoner_tools_gui_shell.main_window_validate_manifests` |  | main, validate_manifest |  |  |  |
| `kanda_reasoner_app.reasoner_tools_gui_shell.tool_specs` |  | TOOLS, ToolSpec |  | kanda_reasoner_app.reasoner_tools_gui_shell.lazy_tabs, kanda_reasoner_app.reasoner_tools_gui_shell.main_window, kanda_reasoner_app.reasoner_tools_gui_shell.main_window_help.window_tool_patches |  |

**Public Symbol Quick Reference**

- `APP_DISPLAY_NAME` -> `kanda_reasoner_app.reasoner_tools_gui_shell.app_constants`
- `APP_ICON_PATH` -> `kanda_reasoner_app.reasoner_tools_gui_shell.app_constants`
- `APP_TITLE_DETAIL` -> `kanda_reasoner_app.reasoner_tools_gui_shell.app_constants`
- `IgnoreRulesTab` -> `kanda_reasoner_app.reasoner_tools_gui_shell.ignore_rules_tab`
- `LazyToolTab` -> `kanda_reasoner_app.reasoner_tools_gui_shell.lazy_tabs`
- `ReasonerToolsWindow` -> `kanda_reasoner_app.reasoner_tools_gui_shell.main_window`
- `TOOLS` -> `kanda_reasoner_app.reasoner_tools_gui_shell.tool_specs`
- `ToolLoadErrorPanel` -> `kanda_reasoner_app.reasoner_tools_gui_shell.error_panels`
- `ToolSpec` -> `kanda_reasoner_app.reasoner_tools_gui_shell.tool_specs`

### kanda_reasoner_app.reasoner_tools_gui_shell.ignore_rules_tab_help

| Module | Owns | Exposes | Depends On | Used By | Helper Group |
|---|---|---|---|---|---|
| `kanda_reasoner_app.reasoner_tools_gui_shell.ignore_rules_tab_help` |  | IgnoreRulesBrowseStateMixin, IgnoreRulesDefaultsMixin, IgnoreRulesListActionsMixin, IgnoreRulesPrefsMixin, IgnoreRulesUiMixin | kanda_reasoner_app.reasoner_tools_gui_shell.ignore_rules_tab_help.browse_state, kanda_reasoner_app.reasoner_tools_gui_shell.ignore_rules_tab_help.list_actions, kanda_reasoner_app.reasoner_tools_gui_shell.ignore_rules_tab_help.prefs_io, kanda_reasoner_app.reasoner_tools_gui_shell.ignore_rules_tab_help.rule_defaults, kanda_reasoner_app.reasoner_tools_gui_shell.ignore_rules_tab_help.ui_builders |  | ignore_rules_tab |
| `kanda_reasoner_app.reasoner_tools_gui_shell.ignore_rules_tab_help.browse_state` |  | IgnoreRulesBrowseStateMixin |  | kanda_reasoner_app.reasoner_tools_gui_shell.ignore_rules_tab, kanda_reasoner_app.reasoner_tools_gui_shell.ignore_rules_tab_help | ignore_rules_tab |
| `kanda_reasoner_app.reasoner_tools_gui_shell.ignore_rules_tab_help.list_actions` |  | IgnoreRulesListActionsMixin |  | kanda_reasoner_app.reasoner_tools_gui_shell.ignore_rules_tab, kanda_reasoner_app.reasoner_tools_gui_shell.ignore_rules_tab_help | ignore_rules_tab |
| `kanda_reasoner_app.reasoner_tools_gui_shell.ignore_rules_tab_help.prefs_io` |  | IgnoreRulesPrefsMixin |  | kanda_reasoner_app.reasoner_tools_gui_shell.ignore_rules_tab, kanda_reasoner_app.reasoner_tools_gui_shell.ignore_rules_tab_help | ignore_rules_tab |
| `kanda_reasoner_app.reasoner_tools_gui_shell.ignore_rules_tab_help.rule_defaults` |  | IgnoreRulesDefaultsMixin |  | kanda_reasoner_app.reasoner_tools_gui_shell.ignore_rules_tab, kanda_reasoner_app.reasoner_tools_gui_shell.ignore_rules_tab_help | ignore_rules_tab |
| `kanda_reasoner_app.reasoner_tools_gui_shell.ignore_rules_tab_help.ui_builders` |  | IgnoreRulesUiMixin |  | kanda_reasoner_app.reasoner_tools_gui_shell.ignore_rules_tab, kanda_reasoner_app.reasoner_tools_gui_shell.ignore_rules_tab_help | ignore_rules_tab |

**Helper Groups**

- `ignore_rules_tab` -> main `kanda_reasoner_app.reasoner_tools_gui_shell.ignore_rules_tab`
  - `kanda_reasoner_app.reasoner_tools_gui_shell.ignore_rules_tab_help`
  - `kanda_reasoner_app.reasoner_tools_gui_shell.ignore_rules_tab_help.browse_state`
  - `kanda_reasoner_app.reasoner_tools_gui_shell.ignore_rules_tab_help.list_actions`
  - `kanda_reasoner_app.reasoner_tools_gui_shell.ignore_rules_tab_help.prefs_io`
  - `kanda_reasoner_app.reasoner_tools_gui_shell.ignore_rules_tab_help.rule_defaults`
  - `kanda_reasoner_app.reasoner_tools_gui_shell.ignore_rules_tab_help.ui_builders`

**Public Symbol Quick Reference**

- `IgnoreRulesBrowseStateMixin` -> `kanda_reasoner_app.reasoner_tools_gui_shell.ignore_rules_tab_help.browse_state`
- `IgnoreRulesDefaultsMixin` -> `kanda_reasoner_app.reasoner_tools_gui_shell.ignore_rules_tab_help.rule_defaults`
- `IgnoreRulesListActionsMixin` -> `kanda_reasoner_app.reasoner_tools_gui_shell.ignore_rules_tab_help.list_actions`
- `IgnoreRulesPrefsMixin` -> `kanda_reasoner_app.reasoner_tools_gui_shell.ignore_rules_tab_help.prefs_io`
- `IgnoreRulesUiMixin` -> `kanda_reasoner_app.reasoner_tools_gui_shell.ignore_rules_tab_help.ui_builders`

### kanda_reasoner_app.reasoner_tools_gui_shell.main_window_help

| Module | Owns | Exposes | Depends On | Used By | Helper Group |
|---|---|---|---|---|---|
| `kanda_reasoner_app.reasoner_tools_gui_shell.main_window_help` |  |  |  |  | main_window |
| `kanda_reasoner_app.reasoner_tools_gui_shell.main_window_help.window_help` |  |  | kanda_reasoner_app.reasoner_tools_gui_shell.app_constants | kanda_reasoner_app.reasoner_tools_gui_shell.main_window | main_window |
| `kanda_reasoner_app.reasoner_tools_gui_shell.main_window_help.window_output_paths` |  |  |  | kanda_reasoner_app.reasoner_tools_gui_shell.main_window | main_window |
| `kanda_reasoner_app.reasoner_tools_gui_shell.main_window_help.window_project_root` |  |  |  | kanda_reasoner_app.reasoner_tools_gui_shell.main_window | main_window |
| `kanda_reasoner_app.reasoner_tools_gui_shell.main_window_help.window_state` |  |  | kanda_reasoner_app.reasoner_tools_gui_shell.app_constants | kanda_reasoner_app.reasoner_tools_gui_shell.main_window | main_window |
| `kanda_reasoner_app.reasoner_tools_gui_shell.main_window_help.window_tool_patches` |  |  | kanda_reasoner_app.reasoner_tools_gui_shell.app_constants, kanda_reasoner_app.reasoner_tools_gui_shell.gui_support, kanda_reasoner_app.reasoner_tools_gui_shell.tool_specs | kanda_reasoner_app.reasoner_tools_gui_shell.main_window | main_window |

**Helper Groups**

- `main_window` -> main `kanda_reasoner_app.reasoner_tools_gui_shell.main_window`
  - `kanda_reasoner_app.reasoner_tools_gui_shell.main_window_help`
  - `kanda_reasoner_app.reasoner_tools_gui_shell.main_window_help.window_help`
  - `kanda_reasoner_app.reasoner_tools_gui_shell.main_window_help.window_output_paths`
  - `kanda_reasoner_app.reasoner_tools_gui_shell.main_window_help.window_project_root`
  - `kanda_reasoner_app.reasoner_tools_gui_shell.main_window_help.window_state`
  - `kanda_reasoner_app.reasoner_tools_gui_shell.main_window_help.window_tool_patches`

### kanda_reasoner_app.reasoner_tools_shell

| Module | Owns | Exposes | Depends On | Used By | Helper Group |
|---|---|---|---|---|---|
| `kanda_reasoner_app.reasoner_tools_shell` |  |  |  |  |  |
| `kanda_reasoner_app.reasoner_tools_shell.runner` |  |  | kanda_reasoner_app.backend_payloads.loader |  |  |
| `kanda_reasoner_app.reasoner_tools_shell.runner_validate_manifests` |  | main |  |  |  |
| `kanda_reasoner_app.reasoner_tools_shell.tab4_scope_guard` |  | apply_tab4_scope_environment, is_broad_scan_root, is_inside_project_root, load_tab8_ignore_rules, resolve_tab4_project_root, tab8_rules_to_env_json |  |  |  |

**Public Symbol Quick Reference**

- `apply_tab4_scope_environment` -> `kanda_reasoner_app.reasoner_tools_shell.tab4_scope_guard`
- `is_broad_scan_root` -> `kanda_reasoner_app.reasoner_tools_shell.tab4_scope_guard`
- `is_inside_project_root` -> `kanda_reasoner_app.reasoner_tools_shell.tab4_scope_guard`
- `load_tab8_ignore_rules` -> `kanda_reasoner_app.reasoner_tools_shell.tab4_scope_guard`
- `main` -> `kanda_reasoner_app.reasoner_tools_shell.runner_validate_manifests`
- `resolve_tab4_project_root` -> `kanda_reasoner_app.reasoner_tools_shell.tab4_scope_guard`
- `tab8_rules_to_env_json` -> `kanda_reasoner_app.reasoner_tools_shell.tab4_scope_guard`

### kanda_reasoner_app.reasoner_tools_shell.runner_help

| Module | Owns | Exposes | Depends On | Used By | Helper Group |
|---|---|---|---|---|---|
| `kanda_reasoner_app.reasoner_tools_shell.runner_help` |  |  |  |  | runner |
| `kanda_reasoner_app.reasoner_tools_shell.runner_help.window_methods_private_impl` |  |  |  |  | runner |
| `kanda_reasoner_app.reasoner_tools_shell.runner_help.window_process_private_impl` |  |  |  |  | runner |

**Helper Groups**

- `runner` -> main `kanda_reasoner_app.reasoner_tools_shell.runner`
  - `kanda_reasoner_app.reasoner_tools_shell.runner_help`
  - `kanda_reasoner_app.reasoner_tools_shell.runner_help.window_methods_private_impl`
  - `kanda_reasoner_app.reasoner_tools_shell.runner_help.window_process_private_impl`

### kanda_reasoner_app.runtime_scenarios

| Module | Owns | Exposes | Depends On | Used By | Helper Group |
|---|---|---|---|---|---|
| `kanda_reasoner_app.runtime_scenarios` |  | DEFAULT_KEEP_LATEST_RUNTIME_TRACES, ENV_KEEP_LATEST_RUNTIME_TRACES, MAX_KEEP_LATEST_RUNTIME_TRACES, MIN_KEEP_LATEST_RUNTIME_TRACES, resolve_keep_latest_runtime_traces |  |  |  |
| `kanda_reasoner_app.runtime_scenarios.collector_scenario_traces` |  | finalize_runtime_scenario, get_runtime_scenario_output_path, get_runtime_scenario_writer, has_active_runtime_scenario, log_runtime_error, log_runtime_event, reset_runtime_scenario_state, start_runtime_scenario | kanda_reasoner_app.runtime_scenarios.runtime_scenario_writer, kanda_reasoner_app.runtime_scenarios.runtime_trace_retention, kanda_reasoner_app.runtime_scenarios.runtime_trace_retention_config | kanda_reasoner_app.runtime_scenarios.runtime_hotspot_hooks |  |
| `kanda_reasoner_app.runtime_scenarios.runtime_hotspot_hooks` |  | install_runtime_hotspot_hooks | kanda_reasoner_app.runtime_scenarios.collector_scenario_traces |  |  |
| `kanda_reasoner_app.runtime_scenarios.runtime_scenario_runtime` |  | finalize_runtime_scenario, log_runtime_event, start_runtime_scenario | kanda_reasoner_app.runtime_scenarios.runtime_scenario_writer |  |  |
| `kanda_reasoner_app.runtime_scenarios.runtime_scenario_writer` |  | RuntimeScenarioWriter, SCENARIO_DIR, TRACE_VERSION |  | kanda_reasoner_app.runtime_scenarios.collector_scenario_traces, kanda_reasoner_app.runtime_scenarios.runtime_scenario_runtime |  |
| `kanda_reasoner_app.runtime_scenarios.runtime_trace_retention` |  | TRACE_GLOB, delete_runtime_trace_files, list_runtime_trace_files, prune_runtime_trace_files_by_age_days, prune_runtime_trace_files_by_count |  | kanda_reasoner_app.runtime_scenarios.collector_scenario_traces |  |
| `kanda_reasoner_app.runtime_scenarios.runtime_trace_retention_config` |  | DEFAULT_KEEP_LATEST_RUNTIME_TRACES, ENV_KEEP_LATEST_RUNTIME_TRACES, MAX_KEEP_LATEST_RUNTIME_TRACES, MIN_KEEP_LATEST_RUNTIME_TRACES, resolve_keep_latest_runtime_traces |  | kanda_reasoner_app.runtime_scenarios.collector_scenario_traces |  |

**Public Symbol Quick Reference**

- `DEFAULT_KEEP_LATEST_RUNTIME_TRACES` -> `kanda_reasoner_app.runtime_scenarios.runtime_trace_retention_config`
- `ENV_KEEP_LATEST_RUNTIME_TRACES` -> `kanda_reasoner_app.runtime_scenarios.runtime_trace_retention_config`
- `MAX_KEEP_LATEST_RUNTIME_TRACES` -> `kanda_reasoner_app.runtime_scenarios.runtime_trace_retention_config`
- `MIN_KEEP_LATEST_RUNTIME_TRACES` -> `kanda_reasoner_app.runtime_scenarios.runtime_trace_retention_config`
- `RuntimeScenarioWriter` -> `kanda_reasoner_app.runtime_scenarios.runtime_scenario_writer`
- `SCENARIO_DIR` -> `kanda_reasoner_app.runtime_scenarios.runtime_scenario_writer`
- `TRACE_GLOB` -> `kanda_reasoner_app.runtime_scenarios.runtime_trace_retention`
- `TRACE_VERSION` -> `kanda_reasoner_app.runtime_scenarios.runtime_scenario_writer`
- `delete_runtime_trace_files` -> `kanda_reasoner_app.runtime_scenarios.runtime_trace_retention`
- `get_runtime_scenario_output_path` -> `kanda_reasoner_app.runtime_scenarios.collector_scenario_traces`
- `get_runtime_scenario_writer` -> `kanda_reasoner_app.runtime_scenarios.collector_scenario_traces`
- `has_active_runtime_scenario` -> `kanda_reasoner_app.runtime_scenarios.collector_scenario_traces`
- `install_runtime_hotspot_hooks` -> `kanda_reasoner_app.runtime_scenarios.runtime_hotspot_hooks`
- `list_runtime_trace_files` -> `kanda_reasoner_app.runtime_scenarios.runtime_trace_retention`
- `log_runtime_error` -> `kanda_reasoner_app.runtime_scenarios.collector_scenario_traces`
- `prune_runtime_trace_files_by_age_days` -> `kanda_reasoner_app.runtime_scenarios.runtime_trace_retention`
- `prune_runtime_trace_files_by_count` -> `kanda_reasoner_app.runtime_scenarios.runtime_trace_retention`
- `reset_runtime_scenario_state` -> `kanda_reasoner_app.runtime_scenarios.collector_scenario_traces`
- `resolve_keep_latest_runtime_traces` -> `kanda_reasoner_app.runtime_scenarios.runtime_trace_retention_config`

### kanda_reasoner_app.tab1_audit_write_support

| Module | Owns | Exposes | Depends On | Used By | Helper Group |
|---|---|---|---|---|---|
| `kanda_reasoner_app.tab1_audit_write_support` |  |  |  |  |  |
| `kanda_reasoner_app.tab1_audit_write_support.planning` |  | build_tab1_audit_write_plan, module_name_from_python_file, tab1_audit_write_route_should_handle |  |  |  |
| `kanda_reasoner_app.tab1_audit_write_support.worker` |  | Tab1AuditWriteRouteWorker, start_tab1_audit_write_worker |  |  |  |

**Public Symbol Quick Reference**

- `Tab1AuditWriteRouteWorker` -> `kanda_reasoner_app.tab1_audit_write_support.worker`
- `build_tab1_audit_write_plan` -> `kanda_reasoner_app.tab1_audit_write_support.planning`
- `module_name_from_python_file` -> `kanda_reasoner_app.tab1_audit_write_support.planning`
- `start_tab1_audit_write_worker` -> `kanda_reasoner_app.tab1_audit_write_support.worker`
- `tab1_audit_write_route_should_handle` -> `kanda_reasoner_app.tab1_audit_write_support.planning`

### kanda_reasoner_app.templates

| Module | Owns | Exposes | Depends On | Used By | Helper Group |
|---|---|---|---|---|---|
| `kanda_reasoner_app.templates` |  |  |  |  |  |

### kanda_reasoner_app.templates.floating_windows

| Module | Owns | Exposes | Depends On | Used By | Helper Group |
|---|---|---|---|---|---|
| `kanda_reasoner_app.templates.floating_windows` |  | HoverFloatingWindowController, attach_floating_window | kanda_reasoner_app.templates.floating_windows.float_window |  |  |
| `kanda_reasoner_app.templates.floating_windows.float_window` |  | HoverFloatingWindowController, attach_floating_window |  | kanda_reasoner_app.reasoner_tools_gui_shell.lazy_tabs, kanda_reasoner_app.templates.floating_windows |  |

**Public Symbol Quick Reference**

- `HoverFloatingWindowController` -> `kanda_reasoner_app.templates.floating_windows.float_window`
- `attach_floating_window` -> `kanda_reasoner_app.templates.floating_windows.float_window`

### profiling

| Module | Owns | Exposes | Depends On | Used By | Helper Group |
|---|---|---|---|---|---|
| `profiling` |  |  |  |  |  |
| `profiling.eeg_profiler` |  | RealTimePerformanceProfiler |  |  |  |
| `profiling.run_with_trace` |  | run_with_trace_main, test_governance_probe |  |  |  |

**Public Symbol Quick Reference**

- `RealTimePerformanceProfiler` -> `profiling.eeg_profiler`
- `run_with_trace_main` -> `profiling.run_with_trace`
- `test_governance_probe` -> `profiling.run_with_trace`

## Validation Issues

No validation issues.

## Need Professional Help in Developing Your Architecture?

Please contact me at [sammuti.com](https://sammuti.com) :)
