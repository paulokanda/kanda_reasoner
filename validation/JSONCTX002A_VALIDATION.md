# JSONCTX002A validation summary

Scope: lowercase the project-owned evidence folder contract from PROJECT_ANALYSIS_EVIDENCE to project_analysis_evidence, without changing the complete.json schema.

Touched boxes:
- project_analysis_evidence path helpers
- Project Symbol Atlas evidence path/status consumers
- Tab 2 workflow detectors for generated-artifact path expectations
- manage_architecture source loader policy patch for generated artifact paths
- focused tests

Protected contract:
- complete.json schema and content contract were not changed.
- Engineering Safety code was not modified.

Focused checks run in sandbox:
- python -m py_compile on touched source modules and the new focused test.
- PYTHONPATH=. python tests/test_jsonctx002a_lowercase_project_analysis_evidence.py
- PYTHONPATH=. python tests/test_project_analysis_evidence_paths.py
- PYTHONPATH=. python tests/test_pa007a_project_analysis_evidence_paths.py
- PYTHONPATH=. python tests/test_pa007b_project_analysis_evidence_migration.py
- PYTHONPATH=. python tests/test_pa007c_tab4_complete_json_output_path.py
- PYTHONPATH=. python tests/test_pa007d_tab5_split_json_output_path.py
- PYTHONPATH=. python tests/test_pa007e_project_analysis_evidence_status.py
- PYTHONPATH=. python tests/test_manage_workflows_artifact_route_detectors.py
- PYTHONPATH=. python tests/test_manage_workflows_step_target_detectors.py
- PYTHONPATH=. python tests/test_pa008_complete_json_atlas_adapter.py
- PYTHONPATH=. python tests/test_pa009_evidence_freshness_checker.py
- PYTHONPATH=. python tests/test_pa010_live_and_json_evidence_merger.py
- PYTHONPATH=. python tests/test_reasoner_symbol_atlas_final_status.py
- PYTHONPATH=. python tests/test_pa022_reasoner_symbol_atlas_final_status.py

Focused result: all listed focused checks passed.

Global checks run in sandbox:
- PYTHONPATH=. python kanda_reasoner_app/manage_architecture/manage_architecture.py --root /mnt/data/devtools_extract/developer_tools --validate
- PYTHONPATH=. python kanda_reasoner_app/manage_workflows/manage_workflows.py --root /mnt/data/devtools_extract/developer_tools --validate

Global result:
- Architecture validation: exit code 0, Errors 0, Warnings 3.
- Workflow validation: Summary pass=8 fail=0 warn=0 skip=3.

Architecture validation warnings observed in sandbox:
- MISPLACED_TEST in workbench/_bundle_temp/pa023b_sources/test_pa023_json_canonical_atlas_output_quality.py
- MISPLACED_TEST in workbench/_bundle_temp/pa023b_sources/test_pa023b_atlas_output_policy_active_scope.py
- MISSING_PUBLIC_SURFACE_CONTROL in <LEGACY_PRODUCT_PACKAGE>/reasoner_symbol_atlas/output_policy.py

These warnings were not repaired in JSONCTX002A because they are outside the lowercase evidence path contract scope.
