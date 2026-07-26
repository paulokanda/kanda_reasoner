"""Focused validation for complete JSON ZIP and Project Structure 3D ownership."""

from __future__ import annotations

import argparse
import importlib.util
import json
import shutil
import sys
import tempfile
from pathlib import Path
from types import SimpleNamespace

FEATURE_ID = "complete-json-zip-project-structure-3d-v1"


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load module: " + str(path))
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _validate_owner_contract(root: Path, handoff_text: str) -> str:
    """Accept the historical handoff owner or its governed independent successor."""
    if "write_complete_json_zip_family" in handoff_text:
        return "legacy_handoff"

    artifacts_path = (
        root
        / "kanda_reasoner_app/project_structure_visualizer/complete_json_artifacts.py"
    )
    builder_path = (
        root
        / "kanda_reasoner_app/project_structure_visualizer/complete_json_builder.py"
    )
    stream_path = (
        root
        / "kanda_reasoner_app/project_structure_visualizer/complete_json_stream_writer.py"
    )
    controls_path = (
        root
        / "kanda_reasoner_app/project_structure_visualizer/tab_json_controls_mixin.py"
    )
    ui_path = (
        root
        / "kanda_reasoner_app/project_structure_visualizer/tab_ui_builder.py"
    )
    for path in (artifacts_path, builder_path, stream_path, controls_path, ui_path):
        _require(path.is_file(), "Independent Project Structure 3D owner missing: " + str(path))
        _require(
            len(_read(path).splitlines()) <= 500,
            "Module exceeds 500 lines: " + str(path),
        )

    artifacts_text = _read(artifacts_path)
    builder_text = _read(builder_path)
    stream_text = _read(stream_path)
    controls_text = _read(controls_path)
    ui_text = _read(ui_path)
    _require(
        'PROJECT_STRUCTURE_3D_JSON_DIR = "project_structure_3d_json"'
        in artifacts_text,
        "Independent artifact directory contract missing",
    )
    _require(
        "COMPLETE_JSON_PART_LIMIT_BYTES = 450 * 1024 * 1024" in artifacts_text,
        "Independent 450 MB limit missing",
    )
    _require(
        "COMPLETE_JSON_STREAM_ROTATE_BYTES = 400 * 1024 * 1024"
        in artifacts_text,
        "Independent stream rotation threshold missing",
    )
    _require(
        "def build_project_structure_complete_json" in builder_text,
        "Independent JSON builder missing",
    )
    _require(
        "CompleteJsonZipStreamWriter" in stream_text,
        "Independent direct ZIP stream writer missing",
    )
    _require(
        "_update_project_json_incrementally" in controls_text
        and "Update JSON Incrementally" in ui_text,
        "Independent incremental UI contract missing",
    )
    return "project_structure_3d"


def validate(root: Path) -> None:
    exporter_path = (
        root
        / "kanda_reasoner_app/reasoner_context_bundle/complete_json_zip_exporter.py"
    )
    cache_path = (
        root
        / "kanda_reasoner_app/project_structure_visualizer/complete_json_zip_cache.py"
    )
    handoff_path = (
        root / "kanda_reasoner_app/reasoner_context_bundle/handoff_zip_exporter.py"
    )
    graph_path = (
        root
        / "kanda_reasoner_app/project_structure_visualizer/graph_snapshot_builder.py"
    )
    publish_path = (
        root
        / "kanda_reasoner_app/reasoner_tools_shell/runner_help/zip_json_files_publish_private_impl.py"
    )
    for path in (exporter_path, cache_path, handoff_path, graph_path, publish_path):
        _require(path.is_file(), "Missing compatibility file: " + str(path))
        _require(
            len(_read(path).splitlines()) <= 500,
            "Module exceeds 500 lines: " + str(path),
        )

    exporter_text = _read(exporter_path)
    cache_text = _read(cache_path)
    handoff_text = _read(handoff_path)
    graph_text = _read(graph_path)
    publish_text = _read(publish_path)
    _require("450 * 1024 * 1024" in exporter_text, "Legacy 450 MB limit missing")
    owner_mode = _validate_owner_contract(root, handoff_text)
    _require(
        "resolve_complete_json_evidence" in graph_text,
        "3D cache integration missing",
    )
    _require(
        "__complete_json_manifest.json" in publish_text,
        "Manifest cleanup exception missing",
    )
    _require(
        "complete_json_cache_building" in cache_text,
        "Atomic build cache missing",
    )

    temp_root = Path(tempfile.mkdtemp(prefix="kanda_complete_json_zip_test_"))
    try:
        project_root = temp_root / "demo_project"
        support_root = temp_root / "demo_project_show_project_to_AI"
        evidence_dir = support_root / "second_prompt_files"
        project_root.mkdir()
        evidence_dir.mkdir(parents=True)
        complete_json = evidence_dir / "demo_project__complete.json"
        payload = {
            "source_file_index": {
                "demo.py": {
                    "file": "demo.py",
                    "module_name": "demo",
                    "line_count": 5,
                    "symbol_count": 1,
                }
            },
            "import_graph": {},
            "padding": "x" * 200000,
        }
        complete_json.write_text(json.dumps(payload), encoding="utf-8")

        package_name = (
            "kanda_reasoner_app.reasoner_context_bundle.complete_json_zip_exporter"
        )
        exporter = _load_module(package_name, exporter_path)
        original_paths = exporter.bundle_artifact_paths
        exporter.bundle_artifact_paths = lambda _context: SimpleNamespace(
            complete_json=complete_json
        )
        try:
            result = exporter.write_complete_json_zip_family(
                SimpleNamespace(project_slug="demo_project"), evidence_dir
            )
        finally:
            exporter.bundle_artifact_paths = original_paths
        _require(bool(result.get("ok")), "Legacy ZIP family export failed")
        manifest_path = Path(str(result["manifest_path"]))
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        _require(manifest["part_count"] == 1, "Small JSON should use one ZIP")
        _require(
            all(
                int(item["size_bytes"]) <= 450 * 1024 * 1024
                for item in manifest["parts"]
            ),
            "Legacy ZIP limit violated",
        )
        complete_json.unlink()

        cache_name = (
            "kanda_reasoner_app.project_structure_visualizer.complete_json_zip_cache"
        )
        cache = _load_module(cache_name, cache_path)
        cache.analysis_json_complete_dir = lambda _root: evidence_dir
        cache.project_analysis_evidence_root = lambda _root: support_root
        resolved, label, status = cache.resolve_complete_json_evidence(project_root)
        _require(resolved is not None and resolved.is_file(), "Cache reconstruction failed")
        _require(status == "rebuilt", "First cache status should be rebuilt")
        _require(
            json.loads(resolved.read_text(encoding="utf-8"))["source_file_index"],
            "Reconstructed JSON invalid",
        )
        resolved_again, _label_again, status_again = cache.resolve_complete_json_evidence(
            project_root
        )
        _require(resolved_again == resolved, "Cache reuse path drifted")
        _require(status_again == "reused", "Second cache status should be reused")
        _require(label == "complete JSON ZIP cache", "Unexpected source label")
    finally:
        shutil.rmtree(temp_root, ignore_errors=True)

    if owner_mode == "legacy_handoff":
        print("LEGACY_HANDOFF_COMPLETE_JSON_OWNER: PASS")
    else:
        print("HANDOFF_COMPLETE_JSON_INTEGRATION_RETIRED: PASS")
        print("PROJECT_STRUCTURE_3D_INDEPENDENT_JSON_OWNER: PASS")
    print("COMPLETE_JSON_ZIP_450MB_CONTRACT: PASS")
    print("COMPLETE_JSON_ZIP_MANIFEST: PASS")
    print("PROJECT_STRUCTURE_3D_CACHE_REBUILD: PASS")
    print("PROJECT_STRUCTURE_3D_CACHE_REUSE: PASS")
    print("LOOSE_COMPLETE_JSON_NOT_REQUIRED: PASS")
    print("MODULE_SIZE_GATE: PASS")
    print("VALIDATION OK: " + FEATURE_ID)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    args = parser.parse_args()
    validate(Path(args.root).expanduser().resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
