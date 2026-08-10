"""Focused validation for PNG reuse and Show Project cancellation controls."""

from __future__ import annotations

import hashlib
import tempfile
import zipfile
from pathlib import Path

from kanda_reasoner_app.reasoner_context_bundle.schema_models import ProjectContext
from kanda_reasoner_app.reasoner_context_bundle.source_tree_exporter_inventory import (
    _can_reuse_previous_png_assets,
    _current_png_signature,
    _previous_png_signature,
)
from kanda_reasoner_app.reasoner_tools_shell.runner_help.png_reuse_cancel_controls_private_impl import (
    PNG_REUSE_PROMPT,
    cancel_run,
    consume_cancel_on_finish,
)


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_reuse_signature() -> None:
    current = [
        {
            "path": "docs/image.png",
            "size_bytes": 4,
            "mtime_ns": 999,
            "sha256": "abcd",
            "archive_family": "png_assets",
        }
    ]
    previous = {
        "included_files": [
            {
                "path": "docs/image.png",
                "size_bytes": 4,
                "mtime_ns": 1,
                "sha256": "abcd",
                "archive_family": "png_assets",
            }
        ]
    }
    assert _current_png_signature(current) == _previous_png_signature(previous)
    current[0]["sha256"] = "changed"
    assert _current_png_signature(current) != _previous_png_signature(previous)
    print("PNG_CONTENT_SIGNATURE_IGNORES_MTIME: PASS")
    print("PNG_CONTENT_CHANGE_REBUILDS: PASS")


def validate_full_reuse_contract() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir) / "project"
        output = Path(temp_dir) / "second_prompt_files"
        root.mkdir()
        output.mkdir()
        image = root / "image.png"
        image.write_bytes(b"PNGDATA")
        part = output / "project__png_assets_part01_of_01.zip"
        with zipfile.ZipFile(part, "w", compression=zipfile.ZIP_STORED) as archive:
            archive.write(image, "image.png")
        record = {
            "path": "image.png",
            "absolute_path": str(image),
            "size_bytes": image.stat().st_size,
            "mtime_ns": image.stat().st_mtime_ns + 12345,
            "sha256": _sha(image),
            "archive_family": "png_assets",
        }
        manifest = {
            "included_files": [
                {
                    **record,
                    "mtime_ns": 1,
                    "part": 1,
                    "part_filename": part.name,
                }
            ],
            "png_asset_archive_contract": {
                "enabled": True,
                "compression_method": "ZIP_STORED",
                "selected_size_cap_mb": 500,
                "selected_size_cap_bytes": 500 * 1024 * 1024,
            },
            "png_asset_parts": [
                {
                    "filename": part.name,
                    "actual_size_bytes": part.stat().st_size,
                    "sha256": _sha(part),
                }
            ],
        }
        context = ProjectContext(root=root, project_slug="project", evidence_root=output.parent, json_complete_dir=output, active_project_id="project", active_project_root_fingerprint="test")
        assert _can_reuse_previous_png_assets(
            context=context,
            previous_output_dir=output,
            previous_manifest=manifest,
            png_asset_files=[record],
            part_size_mb=500,
            hard_cap=500 * 1024 * 1024,
        )
        print("PNG_PREVIOUS_ZIP_REUSE_CONTRACT: PASS")


class _FakeProcess:
    def __init__(self) -> None:
        self.terminated = False
        self.killed = False

    def terminate(self) -> None:
        self.terminated = True

    def waitForFinished(self, _milliseconds: int) -> bool:
        return True

    def kill(self) -> None:
        self.killed = True


class _FakeWindow:
    def __init__(self) -> None:
        self._process = _FakeProcess()
        self._cancel_prompt_files_requested = False
        self.logs: list[str] = []

    def _append_log(self, text: str) -> None:
        self.logs.append(text)


def validate_cancel_contract() -> None:
    window = _FakeWindow()
    cancel_run(window)
    assert window._cancel_prompt_files_requested is True
    assert window._process.terminated is True
    statuses: list[str] = []
    assert consume_cancel_on_finish(window, statuses.append) is True
    assert window._process is None
    assert statuses == ["Canceled"]
    assert any("Previous published delivery was preserved" in item for item in window.logs)
    print("CREATE_PROMPT_FILES_CANCEL_PROCESS: PASS")
    print("CREATE_PROMPT_FILES_CANCEL_PRESERVES_FINAL: PASS")


def validate_ui_source(root: Path) -> None:
    ui_path = root / "kanda_reasoner_app/reasoner_tools_shell/runner_help/window_methods_private_impl.py"
    helper_path = root / "kanda_reasoner_app/reasoner_tools_shell/runner_help/png_reuse_cancel_controls_private_impl.py"
    ui_text = ui_path.read_text(encoding="utf-8")
    helper_text = helper_path.read_text(encoding="utf-8")
    assert "_png_controls.install_controls(self, project_root_row)" in ui_text
    assert 'QPushButton("Reuse PNG")' in helper_text
    assert 'QColor("#ff4d00")' in helper_text
    assert 'QPushButton("Cancel")' in helper_text
    assert 'QColor("#008000")' in helper_text
    assert "clipboard().setText(PNG_REUSE_PROMPT)" in helper_text
    assert "Do not rebuild unchanged PNG archives" in PNG_REUSE_PROMPT
    print("REUSE_PNG_ORANGE_CLIPBOARD_BUTTON: PASS")
    print("CANCEL_GREEN_BUTTON: PASS")



def validate_optional_save_prefs(root: Path) -> None:
    path = (
        root
        / "kanda_reasoner_app"
        / "reasoner_tools_shell"
        / "runner_help"
        / "window_process_private_impl.py"
    )
    text = path.read_text(encoding="utf-8")
    assert 'def _safe_save_prefs(*args) -> None:' in text
    assert 'globals().get("_save_prefs")' in text
    assert text.count('_safe_save_prefs(') == 3
    direct = '_save_prefs(self._pending_project_root'
    assert direct not in text.replace('_safe_save_prefs(', '')
    print("SHOW_PROJECT_OPTIONAL_PREFS_HOOK: PASS")



def validate_optional_runtime_event(root: Path) -> None:
    path = (
        root
        / "kanda_reasoner_app"
        / "reasoner_tools_shell"
        / "runner_help"
        / "window_process_private_impl.py"
    )
    text = path.read_text(encoding="utf-8")
    assert "def _safe_emit_runtime_event(**kwargs) -> None:" in text
    assert 'globals().get("_safe_log_runtime_event")' in text
    assert text.count("_safe_emit_runtime_event(") == 6
    direct = "_safe_log_runtime_event(event_type="
    assert direct not in text
    print("SHOW_PROJECT_OPTIONAL_RUNTIME_LOG_HOOK: PASS")


def validate_sys_import_for_child_launch(root: Path) -> None:
    path = (
        root
        / "kanda_reasoner_app"
        / "reasoner_tools_shell"
        / "runner_help"
        / "window_process_private_impl.py"
    )
    text = path.read_text(encoding="utf-8")
    assert "import sys" in text
    assert text.count("sys.executable") >= 4
    print("SHOW_PROJECT_SYS_IMPORT_FOR_CHILD_LAUNCH: PASS")


def validate_safe_child_mode_arg(root: Path) -> None:
    path = (
        root
        / "kanda_reasoner_app"
        / "reasoner_tools_shell"
        / "runner_help"
        / "window_process_private_impl.py"
    )
    text = path.read_text(encoding="utf-8")
    assert "globals().get('_CHILD_MODE_ARG') or '--collector-child'" in text
    assert "child_mode_arg" in text
    direct = ", _CHILD_MODE_ARG, self._pending_project_root"
    assert direct not in text
    print("SHOW_PROJECT_SAFE_CHILD_MODE_ARG: PASS")


def validate_complete_json_sequence(root: Path) -> None:
    path = root / "kanda_reasoner_app/reasoner_tools_shell/runner_help/window_process_private_impl.py"
    text = path.read_text(encoding="utf-8")
    assert "project_slug + '__complete.json'" in text
    assert "project_slug + '__complete_runtime_trace.json'" in text
    assert "Hybrid mode skips old heavy complete.json" not in text
    run_body = text[text.index("def _run_collector"): ]
    assert "_start_collector_process(self)" in run_body
    assert "_start_ai_context_bundle_process(self)" not in run_body
    print("SHOW_PROJECT_COMPLETE_JSON_SEQUENCE_RESTORED: PASS")

def main() -> int:
    root = Path(__file__).resolve().parents[1]
    validate_reuse_signature()
    validate_full_reuse_contract()
    validate_cancel_contract()
    validate_ui_source(root)
    validate_optional_save_prefs(root)
    validate_optional_runtime_event(root)
    validate_sys_import_for_child_launch(root)
    validate_safe_child_mode_arg(root)
    validate_complete_json_sequence(root)
    module_paths = [
        root / "kanda_reasoner_app/reasoner_context_bundle/source_tree_exporter_inventory.py",
        root / "kanda_reasoner_app/reasoner_tools_shell/runner_help/window_methods_private_impl.py",
        root / "kanda_reasoner_app/reasoner_tools_shell/runner_help/window_process_private_impl.py",
        root / "kanda_reasoner_app/reasoner_tools_shell/runner_help/zip_json_files_process_private_impl.py",
        root / "kanda_reasoner_app/reasoner_tools_shell/runner_help/png_reuse_cancel_controls_private_impl.py",
    ]
    for path in module_paths:
        assert len(path.read_text(encoding="utf-8").splitlines()) <= 500, path
    print("MODULE_SIZE_GATE: PASS")
    print("VALIDATION OK: show-project-png-reuse-cancel-controls-v1r5")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
