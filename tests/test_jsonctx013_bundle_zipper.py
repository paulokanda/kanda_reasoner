from __future__ import annotations

import json
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from kanda_reasoner_app.reasoner_context_bundle import (  # noqa: E402
    bundle_artifact_paths,
    generate_ai_context_bundle,
    resolve_project_context,
)
from kanda_reasoner_app.reasoner_context_bundle.bundle_zipper import (  # noqa: E402
    zip_ai_context_bundle,
)


def _write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, sort_keys=True), encoding="utf-8")


def _make_project() -> Path:
    root = Path(tempfile.mkdtemp()) / "sample_project"
    (root / 'ask_' 'ai_project_reasoner').mkdir(parents=True)
    (root / 'ask_' 'ai_project_reasoner' / "module.py").write_text(
        "def value():\n    return 1\n",
        encoding="utf-8",
    )
    context = resolve_project_context(root)
    paths = bundle_artifact_paths(context)
    _write_json(paths.complete_json, {"complete": True})
    _write_json(
        paths.complete_json.with_name("sample_project__complete_runtime_trace.json"),
        {"trace": True},
    )
    return root


def test_zip_ai_context_bundle_creates_foldered_zip_with_required_and_trace_files() -> None:
    root = _make_project()
    result = generate_ai_context_bundle(root)
    assert result["ok"], result

    destination = root.parent / "exported"
    destination.mkdir()
    zip_result = zip_ai_context_bundle(
        root,
        destination,
        timestamp="20260102_030405",
    )

    assert zip_result["ok"], zip_result
    assert zip_result["project_root_marker"] == "<PROJECT_ROOT>"
    assert zip_result["required_artifact_count"] == 7
    assert zip_result["optional_artifact_count"] == 1
    assert zip_result["artifact_count"] == 8

    zip_path = Path(str(zip_result["zip_path"]))
    assert zip_path.exists()
    assert zip_path.parent == destination
    assert zip_path.name == "sample_project__ai_context_bundle__20260102_030405.zip"

    with zipfile.ZipFile(zip_path, "r") as archive:
        names = sorted(archive.namelist())

    prefix = "sample_project__ai_context_bundle__20260102_030405/"
    expected_names = [
        prefix + "project_analysis_evidence/json_complete/sample_project__active_snapshot.json",
        prefix + "project_analysis_evidence/json_complete/sample_project__bundle_manifest.json",
        prefix + "project_analysis_evidence/json_complete/sample_project__complete.json",
        prefix + "project_analysis_evidence/json_complete/sample_project__complete_runtime_trace.json",
        prefix + "project_analysis_evidence/json_complete/sample_project__exclusion_rules.json",
        prefix + "project_analysis_evidence/json_complete/sample_project__file_manifest.json",
        prefix + "project_analysis_evidence/json_complete/sample_project__reconstruction_payload.json",
        prefix + "project_analysis_evidence/json_complete/sample_project__validation_state.json",
    ]
    assert names == expected_names


def test_zip_ai_context_bundle_refuses_missing_destination() -> None:
    root = _make_project()
    result = generate_ai_context_bundle(root)
    assert result["ok"], result

    missing_destination = root.parent / "missing"
    zip_result = zip_ai_context_bundle(root, missing_destination)

    assert not zip_result["ok"]
    assert "Destination folder does not exist" in "\n".join(zip_result["failures"])


if __name__ == "__main__":
    test_zip_ai_context_bundle_creates_foldered_zip_with_required_and_trace_files()
    test_zip_ai_context_bundle_refuses_missing_destination()
    print("JSONCTX013 bundle zipper tests passed.")
