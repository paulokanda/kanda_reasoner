"""Focused tests for JSONCTX005 file manifest generation."""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import kanda_reasoner_app.reasoner_context_bundle.file_manifest_builder as file_manifest_builder_module

from kanda_reasoner_app.reasoner_context_bundle import (
    TEXT_FILE_EXTENSIONS,
    build_file_manifest_payload,
    iter_active_project_files,
    resolve_project_context,
    write_file_manifest_json,
)


def _make_project(prefix: str = "jsonctx005_project_") -> Path:
    root = Path(tempfile.mkdtemp(prefix=prefix))
    package = root / 'ask_' 'ai_project_reasoner'
    package.mkdir()
    (package / "module.py").write_text(
        "print('ok')\r\n",
        encoding="utf-8",
        newline="",
    )
    (package / "config.json").write_text(
        json.dumps({"enabled": True}),
        encoding="utf-8",
    )
    (root / "README.md").write_text("hello\n", encoding="utf-8")
    (root / "binary.dat").write_bytes(b"abc\x00def")
    (root / "ignored").mkdir()
    (root / "ignored" / "skip.py").write_text("print('skip')\n", encoding="utf-8")
    (root / "sample.log").write_text("log\n", encoding="utf-8")
    (root / "scratch.tmp").write_text("tmp\n", encoding="utf-8")
    prefs = {
        "ignore_rules": {
            "folders": ["ignored"],
            "files": ["*.log"],
            "extensions": [".tmp"],
        }
    }
    (root / ".reasoner_tools_gui_prefs.json").write_text(
        json.dumps(prefs),
        encoding="utf-8",
    )
    return root


def test_iter_active_project_files_uses_project_specific_exclusions() -> None:
    root = _make_project()
    paths = sorted(
        path.relative_to(root).as_posix()
        for path in iter_active_project_files(root)
    )

    assert 'ask_' 'ai_project_reasoner' '/module.py' in paths
    assert 'ask_' 'ai_project_reasoner' '/config.json' in paths
    assert "README.md" in paths
    assert "binary.dat" in paths
    assert "ignored/skip.py" not in paths
    assert "sample.log" not in paths
    assert "scratch.tmp" not in paths


def test_build_file_manifest_payload_has_hashes_and_no_absolute_root() -> None:
    root = _make_project()
    payload = build_file_manifest_payload(root)
    text = json.dumps(payload, sort_keys=True)
    files = {item["path"]: item for item in payload["files"]}

    assert payload["schema_version"] == 1
    assert payload["bundle_kind"] == "file_manifest"
    assert payload["project"]["project_root_marker"] == "<PROJECT_ROOT>"
    assert payload["project"]["evidence_root_relative"] == "project_analysis_evidence"
    assert str(root) not in text
    assert 'ask_' 'ai_project_reasoner' '/module.py' in files
    assert files['ask_' 'ai_project_reasoner' '/module.py']["kind"] == "text"
    assert files['ask_' 'ai_project_reasoner' '/module.py']["newline"] == "crlf"
    assert files['ask_' 'ai_project_reasoner' '/module.py']["sha256_raw"]
    assert files['ask_' 'ai_project_reasoner' '/module.py']["sha256_normalized"]
    assert files['ask_' 'ai_project_reasoner' '/module.py']["included_in_active_snapshot"] is True
    assert files["binary.dat"]["kind"] == "binary"
    assert files["binary.dat"]["included_in_active_snapshot"] is False
    assert payload["counts"]["active_files"] == len(payload["files"])
    assert payload["counts"]["text_files"] >= 3
    assert payload["counts"]["binary_files"] == 1
    assert payload["excluded_path_samples"]


def test_write_file_manifest_json_writes_expected_project_owned_file() -> None:
    root = _make_project()
    context = resolve_project_context(root)
    output_path = write_file_manifest_json(context)

    assert output_path.name == context.project_slug + "__file_manifest.json"
    assert output_path.parent == root / "project_analysis_evidence" / "json_complete"
    assert output_path.exists()

    data = json.loads(output_path.read_text(encoding="utf-8"))
    assert data["bundle_kind"] == "file_manifest"
    assert data["source"]["contract"] == "project_specific_dynamic_rules"
    assert data["files"]


def test_project_specific_rules_can_differ_between_projects() -> None:
    first = _make_project("jsonctx005_first_")
    second = _make_project("jsonctx005_second_")

    (first / "docs").mkdir()
    (first / "docs" / "note.md").write_text("one\n", encoding="utf-8")
    (second / "docs").mkdir()
    (second / "docs" / "note.md").write_text("two\n", encoding="utf-8")

    first_prefs = {
        "ignore_rules": {
            "folders": ["ignored", "docs"],
            "files": ["*.log"],
            "extensions": [".tmp"],
        }
    }
    (first / ".reasoner_tools_gui_prefs.json").write_text(
        json.dumps(first_prefs),
        encoding="utf-8",
    )

    first_files = {item["path"] for item in build_file_manifest_payload(first)["files"]}
    second_files = {item["path"] for item in build_file_manifest_payload(second)["files"]}

    assert "docs/note.md" not in first_files
    assert "docs/note.md" in second_files


def test_public_submodule_contracts_are_test_protected() -> None:
    assert ".py" in TEXT_FILE_EXTENSIONS
    assert hasattr(file_manifest_builder_module, "build_file_manifest_payload")
    assert hasattr(file_manifest_builder_module, "write_file_manifest_json")
    assert hasattr(file_manifest_builder_module, "iter_active_project_files")


if __name__ == "__main__":
    test_iter_active_project_files_uses_project_specific_exclusions()
    test_build_file_manifest_payload_has_hashes_and_no_absolute_root()
    test_write_file_manifest_json_writes_expected_project_owned_file()
    test_project_specific_rules_can_differ_between_projects()
    test_public_submodule_contracts_are_test_protected()
    print("JSONCTX005 file manifest builder tests passed.")
