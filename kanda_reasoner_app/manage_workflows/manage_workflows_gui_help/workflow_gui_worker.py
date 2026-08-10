# project-path: kanda_reasoner_app/manage_workflows/manage_workflows_gui_help/workflow_gui_worker.py
"""Background worker for workflow and architecture GUI commands."""

from __future__ import annotations

import contextlib
import io
import logging
import sys
import traceback
from pathlib import Path

from PySide6.QtCore import QObject, Signal

from kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_python_runtime import (
    resolve_project_python,
)

__all__ = [
    "WorkflowRunWorker",
    "build_workflow_execution_context",
]

_TOOL_ROOT = Path(__file__).resolve().parents[3]
_CANONICAL_MANAGER_SCRIPT = (
    _TOOL_ROOT
    / "kanda_reasoner_app"
    / "manage_workflows"
    / "manage_workflows.py"
).resolve()
_MANAGER_MODULE_NAME = "kanda_reasoner_app.manage_workflows.manage_workflows"


def _require_canonical_manager_script(manager_script_path: str | Path) -> Path:
    """Return the Tool-owned Workflow Review manager or fail closed."""
    script_path = Path(manager_script_path).resolve()
    if script_path != _CANONICAL_MANAGER_SCRIPT:
        raise RuntimeError(
            "WORKFLOW_TOOL_PROVIDER_MISMATCH: " + str(script_path)
        )
    return script_path


def _require_tool_module_origin(module: object, expected_path: Path) -> None:
    """Reject a preloaded or imported workflow module outside Tool source."""
    origin_text = str(getattr(module, "__file__", "") or "").strip()
    if not origin_text:
        raise RuntimeError("TOOL_MODULE_PROVENANCE_VIOLATION: missing __file__")
    origin = Path(origin_text).resolve()
    if origin != expected_path:
        raise RuntimeError(
            "TOOL_MODULE_PROVENANCE_VIOLATION: " + str(origin)
        )


def build_workflow_execution_context(
    manager_script_path: str,
    project_root: str,
    mode: str,
) -> str:
    """Render explicit Tool-versus-Project provenance for one GUI run."""
    script_path = _require_canonical_manager_script(manager_script_path)
    project_path = Path(project_root).resolve()
    same_root = "YES" if project_path == _TOOL_ROOT else "NO"
    try:
        project_python = str(resolve_project_python(project_path))
    except RuntimeError as exc:
        project_python = "UNAVAILABLE - " + str(exc)
    return "\n".join(
        [
            "WORKFLOW REVIEW EXECUTION CONTEXT",
            "Tool role: KANDA TOOL EXECUTION PROVIDER",
            f"Tool source root: {_TOOL_ROOT}",
            f"Tool provider script: {script_path}",
            f"Active Project root: {project_path}",
            f"Active Project Python: {project_python}",
            f"Same canonical resolved Tool/Project root: {same_root}",
            "Tool/Project logical roles merged: NO",
            f"Mode: {mode}",
        ]
    ) + "\n"

class WorkflowRunWorker(QObject):
    """Represent workflow run worker."""
    
    output_ready = Signal(str)
    finished_ok = Signal(str)
    finished_error = Signal(str, str)

    def __init__(self, manager_script_path: str, project_root: str, mode: str) -> None:
        """Support init behavior.
        
        Parameters
        ----------
        manager_script_path : str
            The manager script path value.
        project_root : str
            The project root path.
        mode : str
            The selected mode.
        """
        
        super().__init__()
        self._manager_script_path = Path(manager_script_path)
        self._project_root = Path(project_root)
        self._mode = mode

    def run(self) -> None:
        """Support run behavior.
        """
        
        try:
            module = self._load_manager_module(self._manager_script_path)

            buffer = io.StringIO()
            with contextlib.redirect_stdout(buffer), contextlib.redirect_stderr(buffer):
                if hasattr(module, "run"):
                    exit_code = module.run(self._project_root.resolve(), self._mode)
                elif hasattr(module, "main"):
                    original_argv = sys.argv[:]
                    try:
                        sys.argv = [
                            str(self._manager_script_path),
                            "--root", str(self._project_root.resolve()),
                            f"--{self._mode}",
                        ]
                        exit_code = module.main()
                    finally:
                        sys.argv = original_argv
                else:
                    raise AttributeError(
                        f"{self._manager_script_path.name} must expose "
                        "either run(root, mode) or main()."
                    )

            captured = buffer.getvalue()
            if captured:
                self.output_ready.emit(captured)

            if int(exit_code) == 0:
                self.finished_ok.emit(self._mode)
            else:
                self.finished_error.emit(
                    self._mode,
                    f"Worker finished with exit code {exit_code}.",
                )
        except Exception:
            logging.exception("Workflow worker failed")
            tb = traceback.format_exc()
            self.finished_error.emit(self._mode, tb)

    @staticmethod
    def _load_manager_module(manager_script_path):
        """Load the Tool-owned workflow manager with provenance enforcement."""
        import importlib
        import sys

        script_path = _require_canonical_manager_script(manager_script_path)
        tool_root_text = str(_TOOL_ROOT)
        sys.path[:] = [item for item in sys.path if item != tool_root_text]
        sys.path.insert(0, tool_root_text)

        package = sys.modules.get("kanda_reasoner_app")
        if package is not None:
            package_origin = Path(str(getattr(package, "__file__", ""))).resolve()
            if not package_origin.is_relative_to(_TOOL_ROOT):
                raise RuntimeError(
                    "TOOL_MODULE_PROVENANCE_VIOLATION: " + str(package_origin)
                )

        loaded = sys.modules.get(_MANAGER_MODULE_NAME)
        if loaded is not None:
            _require_tool_module_origin(loaded, script_path)
            return loaded

        module = importlib.import_module(_MANAGER_MODULE_NAME)
        _require_tool_module_origin(module, script_path)
        return module
