"""Focused tests for JSONCTX010 project context bundle CLI."""

from __future__ import annotations

import contextlib
import io
import json
import subprocess
import sys
import tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.reasoner_context_bundle.cli import main
from kanda_reasoner_app.reasoner_context_bundle.output_paths import bundle_artifact_paths
from kanda_reasoner_app.reasoner_context_bundle.project_context import resolve_project_context


def _make_project(prefix: str = "jsonctx010_project_") -> Path:
    root = Path(tempfile.mkdtemp(prefix=prefix))
    package = root / 'ask_' 'ai_project_reasoner'
    package.mkdir()
    (package / "module.py").write_text("VALUE = 1\n", encoding="utf-8")
    (root / "README.md").write_text("# Demo\n", encoding="utf-8")
    ignored = root / "ignored"
    ignored.mkdir()
    (ignored / "skip.py").write_text("SKIP = True\n", encoding="utf-8")
    prefs = {
        "ignore_rules": {
            "folders": ["ignored", ".git"],
            "files": ["*.log"],
            "extensions": [".tmp"],
        }
    }
    (root / ".reasoner_tools_gui_prefs.json").write_text(
        json.dumps(prefs),
        encoding="utf-8",
    )
    return root


def _write_complete_json(root: Path) -> Path:
    context = resolve_project_context(root)
    paths = bundle_artifact_paths(context)
    paths.complete_json.parent.mkdir(parents=True, exist_ok=True)
    paths.complete_json.write_text(
        json.dumps({"bundle_kind": "complete_graph", "project": context.project_slug}) + "\n",
        encoding="utf-8",
    )
    return paths.complete_json


def _run_cli(args: list[str]) -> tuple[int, dict[str, object], str]:
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        code = main(args)
    output = buffer.getvalue()
    return code, json.loads(output), output


def test_cli_generates_bundle_and_prints_json_without_absolute_project_root() -> None:
    root = _make_project()
    _write_complete_json(root)
    code, payload, output = _run_cli(["--root", str(root), "--write"])
    paths = bundle_artifact_paths(resolve_project_context(root))

    assert code == 0
    assert payload["ok"] is True
    assert payload["project_root_marker"] == "<PROJECT_ROOT>"
    assert paths.exclusion_rules_json.exists()
    assert paths.file_manifest_json.exists()
    assert paths.active_snapshot_json.exists()
    assert paths.validation_state_json.exists()
    assert paths.bundle_manifest_json.exists()
    assert str(root) not in output
    assert "E:\\developer_tools" not in output
    assert "ignored/skip.py" not in output


def test_cli_reports_failure_when_complete_json_is_missing() -> None:
    root = _make_project()
    code, payload, output = _run_cli(["--root", str(root), "--write", "--compact"])

    assert code == 1
    assert payload["ok"] is False
    assert any("complete" in str(item) for item in payload["failures"])
    assert str(root) not in output


def test_module_entrypoint_runs_as_child_process() -> None:
    root = _make_project()
    _write_complete_json(root)
    command = [
        sys.executable,
        "-m",
        "kanda_reasoner_app.reasoner_context_bundle",
        "--root",
        str(root),
        "--write",
        "--compact",
    ]
    completed = subprocess.run(
        command,
        cwd=str(PROJECT_ROOT),
        check=False,
        capture_output=True,
        text=True,
    )
    payload = json.loads(completed.stdout)

    assert completed.returncode == 0
    assert payload["ok"] is True
    assert payload["project_root_marker"] == "<PROJECT_ROOT>"
    assert str(root) not in completed.stdout


def test_public_submodule_contract_is_test_protected() -> None:
    import kanda_reasoner_app.reasoner_context_bundle.cli as cli_module

    assert hasattr(cli_module, "main")
    assert hasattr(cli_module, "_build_parser")
    assert not hasattr(cli_module, "build_parser")


if __name__ == "__main__":
    test_cli_generates_bundle_and_prints_json_without_absolute_project_root()
    test_cli_reports_failure_when_complete_json_is_missing()
    test_module_entrypoint_runs_as_child_process()
    test_public_submodule_contract_is_test_protected()
    print("JSONCTX010 project context bundle CLI tests passed.")
