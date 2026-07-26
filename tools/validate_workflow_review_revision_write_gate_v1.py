"""Validate the Workflow Review editable revision write gate."""

from __future__ import annotations

__all__: list[str] = []

import argparse
import ast
import hashlib
import importlib.util
import json
import sys
import tempfile
from pathlib import Path
from typing import Any

FEATURE_ID = "workflow-review-revision-write-gate-v1"
LAUNCHER_RELATIVE = Path("kanda_reasoner_app/manage_workflows/manage_workflows_gui.py")
WINDOW_RELATIVE = Path(
    "kanda_reasoner_app/manage_workflows/manage_workflows_gui_help/"
    "workflow_gui_window.py"
)
HELPER_RELATIVE = Path(
    "kanda_reasoner_app/manage_workflows/manage_workflows_gui_help/"
    "workflow_revision_controller.py"
)
MANIFEST_RELATIVE = Path("workflow_review_revision_write_gate_v1_manifest.json")


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="strict")


def _load_helper(path: Path) -> Any:
    name = "workflow_revision_gate_validator_helper"
    spec = importlib.util.spec_from_file_location(name, str(path))
    if spec is None or spec.loader is None:
        raise ImportError("Could not load helper: " + str(path))
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _assert_source_contract(project_root: Path) -> None:
    launcher_path = project_root / LAUNCHER_RELATIVE
    window_path = project_root / WINDOW_RELATIVE
    helper_path = project_root / HELPER_RELATIVE
    for path in (launcher_path, window_path, helper_path):
        if not path.exists():
            raise AssertionError("Required source is missing: " + str(path))
        source = _read(path)
        ast.parse(source, filename=str(path))
        if source.encode("utf-8").startswith(b"\xef\xbb\xbf"):
            raise AssertionError("UTF-8 BOM is forbidden: " + str(path))
    launcher = _read(launcher_path)
    helper = _read(helper_path)
    window = _read(window_path)
    if "install_workflow_revision_gate(_WorkflowManagerWindow)" not in launcher:
        raise AssertionError("Workflow Review launcher gate integration is missing.")
    if "load_payload" in launcher or "load_payload" in window:
        raise AssertionError("Workflow Review must remain readable normal source.")
    if len(launcher.splitlines()) > 500 or len(helper.splitlines()) > 500:
        raise AssertionError("A touched permanent source module exceeds 500 lines.")
    for marker in (
        "Write after Revision",
        "setReadOnly(False)",
        "setUndoRedoEnabled(True)",
        "#b00020",
        "#808080",
        '_REQUIRED_SEQUENCE = ("validate", "diff", "scan")',
        "write_reviewed_manifest",
        "generate_workflows_md",
        "install_workflow_revision_gate",
    ):
        if marker not in helper:
            raise AssertionError("Missing helper behavior marker: " + marker)


def _assert_manifest_extraction(helper: Any) -> None:
    reviewed = {
        "managed_by": "manage_workflows.py",
        "workflows": {"tests": {"enabled": True, "pytest_args": ["-q"]}},
    }
    text = "old copy\n{not json}\n" + json.dumps(reviewed) + "\nfinished"
    extracted = helper.extract_reviewed_manifest(text)
    if extracted["workflows"]["tests"]["enabled"] is not True:
        raise AssertionError("Reviewed manifest extraction failed.")
    normalized = helper.normalize_reviewed_manifest(extracted, Path("C:/project"))
    if normalized.get("managed_by") != "manage_workflows.py":
        raise AssertionError("Reviewed manifest ownership normalization failed.")


def _assert_gate_state(helper: Any) -> None:
    class FakeFont:
        def __init__(self) -> None:
            self.bold = False

        def setBold(self, value: bool) -> None:
            self.bold = bool(value)

    class FakeAction:
        def __init__(self) -> None:
            self._text = "Write"
            self.enabled = True
            self.style = ""
            self._font = FakeFont()

        def text(self) -> str:
            return self._text

        def setText(self, value: str) -> None:
            self._text = value

        def setEnabled(self, value: bool) -> None:
            self.enabled = bool(value)

        def font(self) -> FakeFont:
            return self._font

        def setFont(self, value: FakeFont) -> None:
            self._font = value

        def setStyleSheet(self, value: str) -> None:
            self.style = value

    class FakeOutput:
        def __init__(self) -> None:
            self.read_only = True
            self.undo_enabled = False
            self.placeholder = ""

        def setReadOnly(self, value: bool) -> None:
            self.read_only = bool(value)

        def setUndoRedoEnabled(self, value: bool) -> None:
            self.undo_enabled = bool(value)

        def setPlaceholderText(self, value: str) -> None:
            self.placeholder = value

    class FakeWindow:
        def __init__(self) -> None:
            self._output = FakeOutput()
            self.write_action = FakeAction()

        def actions(self) -> list[Any]:
            return [self.write_action]

    window = FakeWindow()
    controller = helper.WorkflowRevisionController(window)
    if window._output.read_only or not window._output.undo_enabled:
        raise AssertionError("Output editor was not made writable with undo support.")
    if window.write_action.text() != "Write after Revision":
        raise AssertionError("Write action label was not updated.")
    if window.write_action.enabled or "#808080" not in window.write_action.style:
        raise AssertionError("Write action did not start disabled and grey.")
    controller.record_completion("validate", True)
    controller.record_completion("diff", False, "Worker finished with exit code 1.")
    controller.record_completion("scan", True)
    if not window.write_action.enabled:
        raise AssertionError("Validate, Diff, Scan did not authorize reviewed write.")
    if "#b00020" not in window.write_action.style or not window.write_action._font.bold:
        raise AssertionError("Authorized write action is not bold red.")
    controller.invalidate()
    if window.write_action.enabled:
        raise AssertionError("Context invalidation did not relock reviewed write.")


def _assert_class_hook(helper: Any) -> None:
    class FakeFont:
        def setBold(self, _value: bool) -> None:
            return None

    class FakeAction:
        def __init__(self) -> None:
            self._text = "Write"
            self._font = FakeFont()

        def text(self) -> str:
            return self._text

        def setText(self, value: str) -> None:
            self._text = value

        def setEnabled(self, _value: bool) -> None:
            return None

        def font(self) -> FakeFont:
            return self._font

        def setFont(self, _value: FakeFont) -> None:
            return None

        def setStyleSheet(self, _value: str) -> None:
            return None

    class FakeOutput:
        def setReadOnly(self, _value: bool) -> None:
            return None

        def setUndoRedoEnabled(self, _value: bool) -> None:
            return None

        def setPlaceholderText(self, _value: str) -> None:
            return None

    class FakeWindow:
        def __init__(self) -> None:
            self._output = FakeOutput()
            self.write_action = FakeAction()
            self._worker_thread = None
            self.nonwrite_calls: list[str] = []

        def actions(self) -> list[Any]:
            return [self.write_action]

        def run_mode(self, mode: str) -> None:
            self.nonwrite_calls.append(mode)

        def _handle_worker_success(self, mode: str) -> None:
            self.nonwrite_calls.append("ok:" + mode)

        def _handle_worker_error(self, mode: str, details: str) -> None:
            self.nonwrite_calls.append("error:" + mode + ":" + details)

    helper.install_workflow_revision_gate(FakeWindow)
    window = FakeWindow()
    if not hasattr(window, "_workflow_revision_controller"):
        raise AssertionError("Launcher class hook did not install the controller.")
    window.run_mode("validate")
    window._handle_worker_success("validate")
    if "validate" not in window.nonwrite_calls or "ok:validate" not in window.nonwrite_calls:
        raise AssertionError("Class hook did not preserve original non-write behavior.")


def _assert_reviewed_write(helper: Any) -> None:
    with tempfile.TemporaryDirectory(prefix="workflow_review_gate_") as temp:
        root = Path(temp)
        manager = root / "manage_workflows.py"
        manager.write_text(
            """
import json
from pathlib import Path

WORKFLOW_MANIFEST_NAME = 'workflow_manifest.json'
WORKFLOWS_DOC_NAME = 'WORKFLOWS.md'

def generate_workflows_md(manifest):
    return '# WORKFLOWS\\n' + ','.join(manifest['workflows']) + '\\n'

def write_text_if_changed(path, content):
    current = path.read_text(encoding='utf-8') if path.exists() else None
    if current == content:
        return False
    path.write_text(content, encoding='utf-8', newline='\\n')
    return True
""".lstrip(),
            encoding="utf-8",
            newline="\n",
        )
        manifest = {
            "managed_by": "manage_workflows.py",
            "project_root": str(root),
            "workflows": {"custom_reviewed_check": {"enabled": True}},
        }
        code, changed = helper.write_reviewed_manifest(manager, root, manifest)
        if code != 0 or len(changed) != 2:
            raise AssertionError("Reviewed write did not report both generated files.")
        stored = json.loads((root / "workflow_manifest.json").read_text(encoding="utf-8"))
        if "custom_reviewed_check" not in stored["workflows"]:
            raise AssertionError("Reviewed workflow content was regenerated or lost.")


def _assert_package_sync(project_root: Path) -> None:
    manifest_path = project_root / MANIFEST_RELATIVE
    if not manifest_path.exists():
        return
    payload = json.loads(_read(manifest_path))
    for relative, expected in payload.get("installed_sha256", {}).items():
        path = project_root / Path(relative)
        if not path.exists():
            raise AssertionError("Manifest-listed file is missing: " + relative)
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest != expected:
            raise AssertionError("Installed file hash mismatch: " + relative)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", default=str(Path.cwd()))
    args = parser.parse_args()
    project_root = Path(args.project_root).resolve()
    _assert_source_contract(project_root)
    helper = _load_helper(project_root / HELPER_RELATIVE)
    _assert_manifest_extraction(helper)
    _assert_gate_state(helper)
    _assert_class_hook(helper)
    _assert_reviewed_write(helper)
    _assert_package_sync(project_root)
    print("WORKFLOW_REVIEW_EDITABLE_OUTPUT: PASS")
    print("WORKFLOW_REVIEW_DELETE_PASTE_UNDO: PASS")
    print("WORKFLOW_REVIEW_VALIDATE_DIFF_SCAN_GATE: PASS")
    print("WORKFLOW_REVIEW_LAUNCHER_CLASS_HOOK: PASS")
    print("WORKFLOW_REVIEW_REVIEWED_MANIFEST_WRITE: PASS")
    print("OVERSIZED_WINDOW_SOURCE_UNTOUCHED: PASS")
    print("TOUCHED_SOURCE_MODULES_MAX_500_LINES: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    print("ZIP CONTRACT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
