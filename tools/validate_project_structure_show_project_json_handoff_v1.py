"""Validate Show Project complete-JSON handoff into Project Structure."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

FEATURE_ID = "kanda-reasoner-project-structure-show-project-json-handoff-v1"


def require(condition: bool, code: str) -> None:
    if not condition:
        raise RuntimeError(code)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tool-root", required=True)
    args = parser.parse_args()
    root = Path(args.tool_root).expanduser().resolve(strict=False)
    target = root / "kanda_reasoner_app/project_structure_visualizer/complete_json_zip_cache.py"
    text = target.read_text(encoding="utf-8")
    require("working_copy_json_path" in text, "WORKING_COPY_PATH_IMPORT_MISSING")
    require("Show Project to AI local complete JSON" in text, "LOCAL_COMPLETE_SOURCE_LABEL_MISSING")
    require("show_project_local" in text, "LOCAL_COMPLETE_STATUS_MISSING")
    require("_load_object(local_copy)" in text, "LOCAL_COMPLETE_JSON_VALIDATION_MISSING")
    print("PROJECT STRUCTURE SHOW-PROJECT LOCAL COPY CONTRACT: PASS")

    producer = root / "kanda_reasoner_app/reasoner_tools_shell/runner_help/zip_json_files_publish_private_impl.py"
    producer_text = producer.read_text(encoding="utf-8")
    refresh_pos = producer_text.find("_refresh_project_qa_local_ai_json_before_cleanup(final_path, project_root)")
    cleanup_pos = producer_text.find("cleanup_loose_json_files_after_success(final_path)")
    require(refresh_pos >= 0, "SHOW_PROJECT_LOCAL_COPY_REFRESH_CALL_MISSING")
    require(cleanup_pos > refresh_pos, "SHOW_PROJECT_LOCAL_COPY_NOT_REFRESHED_BEFORE_CLEANUP")
    print("SHOW PROJECT PRESERVES COMPLETE JSON BEFORE CLEANUP: PASS")

    sys.path.insert(0, str(root))
    from kanda_reasoner_app.project_structure_visualizer import complete_json_zip_cache as cache
    from kanda_reasoner_app.project_structure_visualizer import graph_snapshot_builder as graph
    try:
        from kanda_reasoner_app.project_structure_visualizer import tab_json_controls_mixin as controls
    except ModuleNotFoundError as exc:
        if exc.name != 'PySide6':
            raise
        controls = None

    with tempfile.TemporaryDirectory() as td:
        base = Path(td)
        project = base / "eeg_kanda"
        project.mkdir()
        support_root = base / "eeg_kanda_show_project_to_AI"
        second = support_root / "second_prompt_files"
        second.mkdir(parents=True)
        canonical = second / "eeg_kanda__complete.json"
        local = second / "eeg_kanda__complete_local_AI.json"
        payload = {
            "source_file_index": {
                "app.py": {
                    "file": "app.py",
                    "module_name": "app",
                    "line_count": 20,
                    "symbol_count": 1,
                },
                "pkg/helper.py": {
                    "file": "pkg/helper.py",
                    "module_name": "pkg.helper",
                    "line_count": 12,
                    "symbol_count": 1,
                },
            },
            "symbol_index": {},
            "primary_definition_index": {},
            "import_graph": {},
            "web_ai_file_responsibility_index": {},
        }
        local.write_text(json.dumps(payload), encoding="utf-8")

        old_analysis = cache.analysis_json_complete_dir
        old_working = cache.working_copy_json_path
        old_artifact = cache.complete_json_artifact_dir
        old_graph_resolver = graph.resolve_complete_json_evidence
        old_graph_support = graph.project_analysis_evidence_root
        old_control_resolver = (
            controls.resolve_complete_json_evidence if controls is not None else None
        )
        try:
            cache.analysis_json_complete_dir = lambda _root: second
            cache.working_copy_json_path = lambda _root: local
            cache.complete_json_artifact_dir = lambda _root: support_root / "project_structure_3d_json"

            resolved, source, status = cache.resolve_complete_json_evidence(project)
            require(resolved == local, "LOCAL_COPY_NOT_SELECTED")
            require(source == "Show Project to AI local complete JSON", "LOCAL_COPY_SOURCE_LABEL_WRONG")
            require(status == "show_project_local", "LOCAL_COPY_STATUS_WRONG")
            print("PROJECT STRUCTURE LOCAL COPY RESOLUTION: PASS")

            canonical.write_text(json.dumps(payload), encoding="utf-8")
            resolved2, source2, status2 = cache.resolve_complete_json_evidence(project)
            require(resolved2 == canonical, "CANONICAL_LOOSE_JSON_NOT_PREFERRED")
            require(source2 == "legacy loose complete JSON", "CANONICAL_LOOSE_SOURCE_LABEL_WRONG")
            require(status2 == "legacy", "CANONICAL_LOOSE_STATUS_WRONG")
            canonical.unlink()
            print("PROJECT STRUCTURE CANONICAL SOURCE PRIORITY: PASS")

            graph.resolve_complete_json_evidence = cache.resolve_complete_json_evidence
            graph.project_analysis_evidence_root = lambda _root: support_root
            result = graph.build_project_graph_snapshot(project)
            require(not result.is_fixture, "GRAPH_FELL_BACK_TO_FIXTURE")
            require(result.source_status == "complete_json_ready", "GRAPH_SOURCE_STATUS_WRONG")
            require("Show Project to AI local complete JSON" in result.source_label, "GRAPH_SOURCE_LABEL_WRONG")
            node_ids = {str(item.get("id")) for item in result.snapshot.get("nodes", []) if isinstance(item, dict)}
            require("module:app.py" in node_ids, "GRAPH_MISSING_APP_MODULE")
            require("module:pkg/helper.py" in node_ids, "GRAPH_MISSING_HELPER_MODULE")
            print("PROJECT STRUCTURE GRAPH CONSUMES SHOW-PROJECT COMPLETE JSON: PASS")

            if controls is not None:
                controls.resolve_complete_json_evidence = cache.resolve_complete_json_evidence
                from PySide6.QtWidgets import QApplication, QLabel, QPushButton
                app = QApplication.instance() or QApplication([])
                class Dummy(controls.ProjectStructureJsonControlsMixin):
                    pass
                dummy = Dummy()
                dummy._project_root = project
                dummy._complete_json_process = None
                dummy.create_project_json_button = QPushButton()
                dummy.update_project_json_button = QPushButton()
                dummy.json_artifact_status_label = QLabel()
                dummy._refresh_complete_json_status()
                label = dummy.json_artifact_status_label.text()
                require("JSON ready from Show Project to AI" in label, "GUI_HANDOFF_READY_MESSAGE_MISSING")
                require(str(local) in label, "GUI_HANDOFF_PATH_MISSING")
                print("PROJECT STRUCTURE GUI HANDOFF STATUS: PASS")
            else:
                print("PROJECT STRUCTURE GUI HANDOFF STATUS: SKIPPED_NO_PYSIDE6")
        finally:
            cache.analysis_json_complete_dir = old_analysis
            cache.working_copy_json_path = old_working
            cache.complete_json_artifact_dir = old_artifact
            graph.resolve_complete_json_evidence = old_graph_resolver
            graph.project_analysis_evidence_root = old_graph_support
            if controls is not None and old_control_resolver is not None:
                controls.resolve_complete_json_evidence = old_control_resolver

    core = root / "portable/validate_installed.py"
    if core.is_file():
        completed = subprocess.run(
            [sys.executable, str(core), "--portable-root", str(root / "portable")],
            cwd=str(root),
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1", "PYTHONPATH": str(root), "QT_QPA_PLATFORM": "offscreen"},
            check=False,
            timeout=900,
        )
        require(completed.returncode == 0, "CURRENT_STAGE_1_6_VALIDATOR_FAILED")
        print("CURRENT STAGE 1-6 PORTABLE BUILDER UNCHANGED: PASS")

    print("VALIDATION OK: " + FEATURE_ID)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
