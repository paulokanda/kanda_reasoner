"""Focused tests for JSONCTX006 active snapshot generation."""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import kanda_reasoner_app.reasoner_context_bundle.active_snapshot_builder as active_snapshot_builder_module

from kanda_reasoner_app.reasoner_context_bundle import (
    SNAPSHOT_TEXT_EXTENSIONS,
    build_active_snapshot_payload,
    resolve_project_context,
    write_active_snapshot_json,
)


def _make_project(prefix: str = "jsonctx006_project_") -> Path:
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
    (root / "README.md").write_text("hello\n", encoding="utf-8", newline="")
    (root / "binary.dat").write_bytes(b"abc\x00def")
    (root / "ignored").mkdir()
    (root / "ignored" / "skip.py").write_text("print('skip')\n", encoding="utf-8", newline="")
    (root / "sample.log").write_text("log\n", encoding="utf-8", newline="")
    evidence_json = root / "project_analysis_evidence" / "json_complete"
    evidence_json.mkdir(parents=True)
    (evidence_json / "old_snapshot.json").write_text("{}\n", encoding="utf-8", newline="")
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


def _files_by_path(payload: dict[str, object]) -> dict[str, dict[str, object]]:
    files = payload["files"]
    assert isinstance(files, list)
    return {str(item["path"]): item for item in files if isinstance(item, dict)}


def _omitted_by_path(payload: dict[str, object]) -> dict[str, dict[str, object]]:
    files = payload["omitted_files"]
    assert isinstance(files, list)
    return {str(item["path"]): item for item in files if isinstance(item, dict)}


def test_build_active_snapshot_payload_contains_active_text_content() -> None:
    root = _make_project()
    payload = build_active_snapshot_payload(root)
    text = json.dumps(payload, sort_keys=True)
    files = _files_by_path(payload)
    omitted = _omitted_by_path(payload)

    assert payload["schema_version"] == 1
    assert payload["bundle_kind"] == "active_snapshot"
    assert payload["project"]["project_root_marker"] == "<PROJECT_ROOT>"
    assert payload["project"]["evidence_root_relative"] == "project_analysis_evidence"
    assert str(root) not in text

    assert 'ask_' 'ai_project_reasoner' '/module.py' in files
    assert files['ask_' 'ai_project_reasoner' '/module.py']["content"] == "print('ok')\r\n"
    assert files['ask_' 'ai_project_reasoner' '/module.py']["newline"] == "crlf"
    assert files['ask_' 'ai_project_reasoner' '/module.py']["sha256_raw"]
    assert files['ask_' 'ai_project_reasoner' '/module.py']["sha256_normalized"]

    assert "README.md" in files
    assert files["README.md"]["content"] == "hello\n"
    assert 'ask_' 'ai_project_reasoner' '/config.json' in files
    assert "ignored/skip.py" not in files
    assert "sample.log" not in files

    assert "binary.dat" in omitted
    assert omitted["binary.dat"]["reason"] == "binary_file_omitted"
    assert "project_analysis_evidence/json_complete/old_snapshot.json" not in files
    assert "project_analysis_evidence/json_complete/old_snapshot.json" not in omitted
    assert payload["snapshot_policy"]["content_fidelity"] == "text_content_preserves_original_newline_sequences"


def test_write_active_snapshot_json_writes_expected_project_owned_file() -> None:
    root = _make_project()
    context = resolve_project_context(root)
    output_path = write_active_snapshot_json(context)

    assert output_path.name == context.project_slug + "__active_snapshot.json"
    assert output_path.parent == root / "project_analysis_evidence" / "json_complete"
    assert output_path.exists()

    data = json.loads(output_path.read_text(encoding="utf-8"))
    assert data["bundle_kind"] == "active_snapshot"
    assert data["source"]["contract"] == "project_specific_dynamic_rules"
    assert data["files"]


def test_project_specific_exclusions_are_used_by_snapshot() -> None:
    first = _make_project("jsonctx006_first_")
    second = _make_project("jsonctx006_second_")

    (first / "docs").mkdir()
    (first / "docs" / "note.md").write_text("one\n", encoding="utf-8", newline="")
    (second / "docs").mkdir()
    (second / "docs" / "note.md").write_text("two\n", encoding="utf-8", newline="")

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

    first_files = _files_by_path(build_active_snapshot_payload(first))
    second_files = _files_by_path(build_active_snapshot_payload(second))

    assert "docs/note.md" not in first_files
    assert "docs/note.md" in second_files
    assert second_files["docs/note.md"]["content"] == "two\n"


def test_public_submodule_contracts_are_test_protected() -> None:
    assert ".py" in SNAPSHOT_TEXT_EXTENSIONS
    assert hasattr(active_snapshot_builder_module, "build_active_snapshot_payload")
    assert hasattr(active_snapshot_builder_module, "write_active_snapshot_json")


if __name__ == "__main__":
    test_build_active_snapshot_payload_contains_active_text_content()
    test_write_active_snapshot_json_writes_expected_project_owned_file()
    test_project_specific_exclusions_are_used_by_snapshot()
    test_public_submodule_contracts_are_test_protected()
    print("JSONCTX006 active snapshot builder tests passed.")
