"""Validate canonical complete JSON generation for Project Structure 3D."""

from __future__ import annotations

import argparse
import ast
from pathlib import Path


FEATURE_ID = "show-project-complete-json-for-3d-v1r4"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def read_text(path: Path) -> str:
    require(path.is_file(), f"Missing file: {path}")
    return path.read_text(encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    args = parser.parse_args()

    root = Path(args.root).resolve()
    app = root / "kanda_reasoner_app"

    process_path = (
        app
        / "reasoner_tools_shell"
        / "runner_help"
        / "window_process_private_impl.py"
    )
    runner_path = app / "reasoner_tools_shell" / "runner.py"
    orchestrator_path = (
        app / "reasoner_context_bundle" / "bundle_orchestrator.py"
    )
    manifest_path = (
        app / "reasoner_context_bundle" / "bundle_manifest_builder.py"
    )
    graph_path = (
        app / "project_structure_visualizer" / "graph_snapshot_builder.py"
    )
    evidence_paths_path = app / "project_analysis_evidence_paths.py"
    adapter_path = (
        app / "reasoner_symbol_atlas" / "complete_json_adapter.py"
    )

    process = read_text(process_path)
    runner = read_text(runner_path)
    orchestrator = read_text(orchestrator_path)
    manifest = read_text(manifest_path)
    graph = read_text(graph_path)
    evidence_paths = read_text(evidence_paths_path)
    adapter = read_text(adapter_path)

    for path, text in (
        (process_path, process),
        (runner_path, runner),
        (orchestrator_path, orchestrator),
        (manifest_path, manifest),
        (graph_path, graph),
    ):
        ast.parse(text, filename=str(path))
    print("SHOW_PROJECT_COMPLETE_JSON_PYTHON_SYNTAX: PASS")

    require(
        'output_json = build_output_dir / (project_slug + "__complete.json")'
        in process,
        "Show Project does not target canonical complete JSON.",
    )
    require(
        'project_slug + "__complete_runtime_trace.json"' in process,
        "Complete JSON runtime trace path missing.",
    )
    require(
        "self._start_collector_process()" in process,
        "Show Project does not launch the canonical collector.",
    )
    require(
        "_start_complete_json_enrichment_process(self)" in process,
        "Complete JSON enrichment stage missing.",
    )
    require(
        "_start_ai_context_bundle_process(self)" in process,
        "Companion bundle stage missing.",
    )
    print("SHOW_PROJECT_COMPLETE_JSON_SEQUENCE: PASS")

    require(
        "_save_runner_prefs_if_available" in process,
        "Safe preference compatibility helper is missing.",
    )
    require(
        'globals().get("_save_prefs")' in process,
        "Preference helper does not resolve the optional hook safely.",
    )
    require(
        "_save_prefs(self._pending_project_root" not in process,
        "A bare undefined _save_prefs call remains.",
    )
    print("SHOW_PROJECT_OPTIONAL_PREFS_HOOK: PASS")

    require(
        "_safe_runtime_event_if_available" in process,
        "Safe runtime-event compatibility helper is missing.",
    )
    require(
        'globals().get("_safe_log_runtime_event")' in process,
        "Runtime-event helper does not resolve the optional hook safely.",
    )
    require(
        "_safe_log_runtime_event(" not in process,
        "A bare undefined _safe_log_runtime_event call remains.",
    )
    print("SHOW_PROJECT_OPTIONAL_RUNTIME_LOG_HOOK: PASS")

    require(
        "_collector_child_mode_arg" in process,
        "Safe collector child-mode resolver is missing.",
    )
    require(
        'globals().get("_CHILD_MODE_ARG")' in process,
        "Collector child-mode resolver does not check the runtime symbol.",
    )
    require(
        'return "--collector-child"' in process,
        "Canonical collector child-mode fallback is missing.",
    )
    require(
        "_CHILD_MODE_ARG," not in process,
        "A bare undefined _CHILD_MODE_ARG launch reference remains.",
    )
    require(
        "_collector_child_mode_arg()," in process,
        "Collector process arguments do not use the safe resolver.",
    )
    print("SHOW_PROJECT_SAFE_CHILD_MODE_ARG: PASS")

    require(
        "import sys" in process,
        "Process helper uses sys.executable without importing sys.",
    )
    require(
        "sys.executable" in process,
        "Collector launcher no longer uses the active Python executable.",
    )
    print("SHOW_PROJECT_SYS_IMPORT_FOR_CHILD_LAUNCH: PASS")

    require(
        "_install_show_project_complete_json_process_patch" in runner,
        "Runner process patch installer missing.",
    )
    require(
        "CollectorRunnerWindow._run_collector = _process_impl._run_collector"
        in runner,
        "Runtime collector method is not bound to corrected source.",
    )
    require(
        "CollectorRunnerWindow._on_process_finished" in runner,
        "Runtime process-finished handler binding missing.",
    )
    print("SHOW_PROJECT_RUNTIME_BINDING: PASS")

    require(
        '"complete_json_generated_by_second_prompt_files": True'
        in orchestrator,
        "Bundle orchestrator complete JSON contract is false.",
    )
    require(
        '"complete_json_generated_by_second_prompt_files": True'
        in manifest,
        "Bundle manifest complete JSON contract is false.",
    )
    require(
        '"complete_json_removed_from_normal_output": False' in manifest,
        "Manifest still claims complete JSON is removed.",
    )
    print("SHOW_PROJECT_BUNDLE_CONTRACT_UPDATED: PASS")

    require(
        "__complete.json" in evidence_paths
        and "primary_evidence_json_path" in evidence_paths,
        "Canonical complete JSON naming contract changed.",
    )
    require(
        'if name == expected_name:' in adapter,
        "Complete JSON adapter does not prioritize the project filename.",
    )
    require(
        'selected = candidates[0]' in graph,
        "Project Structure 3D candidate selection missing.",
    )
    require(
        "_build_from_complete_json(root, selected, payload)" in graph,
        "Project Structure 3D does not build from complete JSON.",
    )
    print("PROJECT_STRUCTURE_3D_COMPLETE_JSON_CONSUMER: PASS")

    require(
        "Run Show Project to AI for this Project" in graph,
        "3D missing-evidence recovery guidance missing.",
    )
    require(
        "second_prompt_files publication" in graph,
        "3D publication guidance missing.",
    )
    print("PROJECT_STRUCTURE_3D_RECOVERY_GUIDANCE: PASS")

    require(
        "The exact source archive remains reconstruction authority" in process,
        "Source-authority boundary missing from Show Project log.",
    )
    require(
        '"authoritative": False' in graph,
        "3D evidence is incorrectly marked authoritative.",
    )
    require(
        '"authority_scope": "read_only_visualization_input"' in graph,
        "3D read-only authority scope missing.",
    )
    print("COMPLETE_JSON_READ_ONLY_AUTHORITY_BOUNDARY: PASS")

    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
