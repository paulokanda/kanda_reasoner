"""Validate independent Project Structure 3D JSON creation and updates."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import tempfile
import zipfile
from pathlib import Path


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _static_contracts(root: Path) -> None:
    package = root / "kanda_reasoner_app" / "project_structure_visualizer"
    required = [
        package / "complete_json_artifacts.py",
        package / "complete_json_stream_writer.py",
        package / "complete_json_index.py",
        package / "complete_json_builder.py",
        package / "complete_json_cli.py",
        package / "tab_json_controls_mixin.py",
        package / "tab_ui_builder.py",
        package / "project_structure_3d_tab.py",
        package / "complete_json_zip_cache.py",
        package / "graph_snapshot_builder.py",
        package / "tab_evidence_mixin.py",
        package / "tab_style.py",
    ]
    for path in required:
        _assert(path.is_file(), "Missing required source: " + str(path))
        compile(_read(path), str(path), "exec")
        _assert(
            len(_read(path).splitlines()) <= 500,
            "Touched Python module exceeds 500 lines: " + str(path),
        )
    ui = _read(package / "tab_ui_builder.py")
    mixin = _read(package / "tab_json_controls_mixin.py")
    artifacts = _read(package / "complete_json_artifacts.py")
    writer = _read(package / "complete_json_stream_writer.py")
    cache = _read(package / "complete_json_zip_cache.py")
    builder = _read(package / "complete_json_builder.py")
    tab = _read(package / "project_structure_3d_tab.py")
    _assert('QPushButton("Create Project JSON")' in ui, "Create button missing")
    _assert(
        'QPushButton("Update JSON Incrementally")' in ui,
        "Incremental button missing",
    )
    _assert(
        'QLabel("JSON is necessary for visualization")' in ui,
        "Required visualization label missing",
    )
    _assert(
        'setObjectName("projectStructure3DContainer")' in ui,
        "Loaded controls were not moved into the 3D container",
    )
    _assert("GreenSonarActivityMonitor" in mixin, "Sonar monitor missing")
    _assert("QProcess" in mixin, "JSON work is not isolated in a process")
    _assert("project_structure_3d_json" in artifacts, "Independent folder missing")
    _assert("450 * 1024 * 1024" in artifacts, "450 MB hard limit missing")
    _assert("400 * 1024 * 1024" in artifacts, "Safe stream rotation missing")
    _assert("archive.open" in writer, "ZIP member is not streamed directly")
    _assert("complete_json_artifact_dir" in cache, "3D cache uses wrong owner")
    _assert("analysis_json_complete_dir" not in builder, "Builder writes to prompt folder")
    _assert("ProjectStructureJsonControlsMixin" in tab, "JSON controls not installed")
    print("PROJECT_STRUCTURE_3D_JSON_UI_CONTRACT: PASS")
    print("PROJECT_STRUCTURE_3D_JSON_INDEPENDENT_OWNER: PASS")
    print("PROJECT_STRUCTURE_3D_JSON_QPROCESS_ISOLATION: PASS")
    print("PROJECT_STRUCTURE_3D_JSON_SONAR_ANIMATION: PASS")
    print("PROJECT_STRUCTURE_3D_JSON_MODULE_SIZE_GATE: PASS")


def _dynamic_contracts(root: Path) -> None:
    from kanda_reasoner_app.project_structure_visualizer.complete_json_artifacts import (
        COMPLETE_JSON_PART_LIMIT_BYTES,
        complete_json_artifact_dir,
        inspect_complete_json_artifacts,
    )
    from kanda_reasoner_app.project_structure_visualizer.complete_json_builder import (
        build_project_structure_complete_json,
    )
    from kanda_reasoner_app.project_structure_visualizer.complete_json_zip_cache import (
        resolve_complete_json_evidence,
    )
    from kanda_reasoner_app.project_structure_visualizer.graph_snapshot_builder import (
        build_project_graph_snapshot,
    )

    temp_root = Path(tempfile.mkdtemp(prefix="kanda_ps3d_json_validator_"))
    project = temp_root / "sample_project"
    try:
        (project / "pkg").mkdir(parents=True)
        (project / "pkg" / "__init__.py").write_text("\n", encoding="utf-8")
        (project / "pkg" / "alpha.py").write_text(
            "from pkg.beta import Beta\n"
            "class Alpha(Beta):\n"
            "    def run(self):\n"
            "        return helper()\n"
            "def helper():\n"
            "    return 1\n",
            encoding="utf-8",
        )
        (project / "pkg" / "beta.py").write_text(
            "class Beta:\n    pass\n",
            encoding="utf-8",
        )
        created = build_project_structure_complete_json(project, mode="create")
        _assert(created["ok"] is True, "Create Project JSON failed")
        status = inspect_complete_json_artifacts(project, verify_hashes=True)
        _assert(status["valid"] is True, "Created ZIP family is invalid")
        _assert(status["incremental_ready"] is True, "SQLite baseline missing")
        artifact_dir = complete_json_artifact_dir(project)
        _assert(
            artifact_dir.name == "project_structure_3d_json",
            "Artifact folder identity is wrong",
        )
        _assert(
            not (project.parent / (project.name + "_show_project_to_AI") / "second_prompt_files").exists(),
            "Project Structure JSON leaked into second_prompt_files",
        )
        loose_json = artifact_dir / (project.name + "__complete.json")
        _assert(not loose_json.exists(), "Loose complete JSON was published")
        for record in status["manifest"]["parts"]:
            part = artifact_dir / record["filename"]
            _assert(part.stat().st_size <= COMPLETE_JSON_PART_LIMIT_BYTES, "ZIP part too large")
            with zipfile.ZipFile(part, "r") as archive:
                _assert(
                    archive.namelist() == [record["member_name"]],
                    "ZIP part does not contain exactly one streamed member",
                )
        json_path, _label, _cache = resolve_complete_json_evidence(project)
        _assert(json_path is not None and json_path.is_file(), "ZIP reconstruction failed")
        payload = json.loads(json_path.read_text(encoding="utf-8"))
        for section in (
            "files",
            "source_file_index",
            "symbol_index",
            "primary_definition_index",
            "import_graph",
            "call_edges",
            "web_ai_file_responsibility_index",
        ):
            _assert(section in payload, "Missing complete JSON section: " + section)
        graph = build_project_graph_snapshot(project)
        _assert(not graph.is_fixture, "3D graph did not consume created JSON")

        (project / "pkg" / "beta.py").unlink()
        (project / "pkg" / "alpha.py").write_text(
            "def helper():\n    return 2\n",
            encoding="utf-8",
        )
        (project / "pkg" / "gamma.py").write_text(
            "class Gamma:\n    pass\n",
            encoding="utf-8",
        )
        updated = build_project_structure_complete_json(project, mode="incremental")
        metrics = updated["metrics"]
        _assert(metrics["changed"] == 2, "Incremental changed count is wrong")
        _assert(metrics["removed"] == 1, "Incremental removed count is wrong")
        _assert(metrics["unchanged"] >= 1, "Unchanged files were reparsed")
        json_path, _label, _cache = resolve_complete_json_evidence(project)
        payload = json.loads(json_path.read_text(encoding="utf-8"))
        _assert("pkg/beta.py" not in payload["source_file_index"], "Deleted file remained")
        _assert("pkg/gamma.py" in payload["source_file_index"], "New file missing")
        print("PROJECT_STRUCTURE_3D_JSON_DIRECT_ZIP_STREAM: PASS")
        print("PROJECT_STRUCTURE_3D_JSON_450MB_PART_GATE: PASS")
        print("PROJECT_STRUCTURE_3D_JSON_NO_LOOSE_PUBLISH: PASS")
        print("PROJECT_STRUCTURE_3D_JSON_CREATE_RUNTIME: PASS")
        print("PROJECT_STRUCTURE_3D_JSON_INCREMENTAL_RUNTIME: PASS")
        print("PROJECT_STRUCTURE_3D_JSON_VISUALIZER_CONSUMER: PASS")
    finally:
        shutil.rmtree(temp_root, ignore_errors=True)
        support = project.parent / (project.name + "_show_project_to_AI")
        shutil.rmtree(support, ignore_errors=True)


def _qt_contract() -> None:
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    os.environ.setdefault("QTWEBENGINE_DISABLE_SANDBOX", "1")
    from PySide6.QtWidgets import QApplication
    from kanda_reasoner_app.project_structure_visualizer.project_structure_3d_tab import (
        ProjectStructure3DWidget,
    )

    app = QApplication.instance() or QApplication([])
    widget = ProjectStructure3DWidget()
    _assert(widget.create_project_json_button.text() == "Create Project JSON", "Qt create label")
    _assert(
        widget.update_project_json_button.text() == "Update JSON Incrementally",
        "Qt update label",
    )
    _assert(
        widget.json_required_label.text() == "JSON is necessary for visualization",
        "Qt required label",
    )
    from PySide6.QtWidgets import QFrame
    _assert(
        widget.findChild(QFrame, "projectStructure3DContainer") is not None,
        "3D container is missing",
    )
    widget.close()
    app.processEvents()
    print("REAL_QT_PROJECT_STRUCTURE_3D_JSON_CONTROLS: PASS")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--skip-qt", action="store_true")
    args = parser.parse_args()
    root = Path(args.root).expanduser().resolve()
    _static_contracts(root)
    _dynamic_contracts(root)
    if not args.skip_qt:
        _qt_contract()
    print("STATUS: IN_SYNC")
    print("VALIDATION OK: project-structure-3d-json-owner-v1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
