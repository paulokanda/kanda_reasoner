# project-path: validation/test_large_file_refactor_planner_ast_target_auto_sync_v1.py
"""Focused validation for AST Audit target auto-sync into Refactor Planner."""
from __future__ import annotations

import ast
import importlib.util
import sys
import types
from dataclasses import dataclass
from pathlib import Path

FEATURE_ID = "large-file-refactor-planner-ast-target-auto-sync-v1"


class _TextEdit:
    def __init__(self, text: str = "") -> None:
        self._text = text

    def text(self) -> str:
        return self._text

    def setText(self, value: str) -> None:
        self._text = value

    def setPlainText(self, value: str) -> None:
        self._text = value

    def toPlainText(self) -> str:
        return self._text


class _Spin:
    def __init__(self, value: int) -> None:
        self._value = value

    def value(self) -> int:
        return self._value


class _Table:
    def __init__(self) -> None:
        self.row = -1

    def selectRow(self, row: int) -> None:
        self.row = row

    def currentRow(self) -> int:
        return self.row


class _Button:
    def __init__(self) -> None:
        self.enabled = False

    def setEnabled(self, enabled: bool) -> None:
        self.enabled = bool(enabled)


class _StatusBar:
    def __init__(self) -> None:
        self.message = ""

    def showMessage(self, message: str) -> None:
        self.message = message


@dataclass
class _Candidate:
    path: str
    relative_path: str
    line_count_physical: int = 800


class _Window:
    def __init__(self, root: Path, target: Path) -> None:
        self._root_path_edit = _TextEdit(str(root))
        self._large_module_target_edit = _TextEdit(str(target))
        self._large_file_refactor_target_edit = _TextEdit()
        self._large_file_refactor_candidate_table = _Table()
        self._large_file_refactor_evidence_output = _TextEdit()
        self._large_file_refactor_plan_output = _TextEdit()
        self._large_file_refactor_analyze_button = _Button()
        self._large_file_refactor_ideal_spin = _Spin(400)
        self._large_file_refactor_max_spin = _Spin(500)
        self._large_file_refactor_min_helper_spin = _Spin(100)
        self._bar = _StatusBar()

    def statusBar(self) -> _StatusBar:
        return self._bar


def _install_pyside_stub() -> None:
    try:
        import PySide6  # noqa: F401
        return
    except ImportError:
        pass
    pyside = types.ModuleType("PySide6")
    widgets = types.ModuleType("PySide6.QtWidgets")
    for name in (
        "QApplication",
        "QFileDialog",
        "QGroupBox",
        "QHBoxLayout",
        "QLabel",
        "QLineEdit",
        "QPlainTextEdit",
        "QPushButton",
        "QTableWidget",
        "QTableWidgetItem",
        "QVBoxLayout",
    ):
        setattr(widgets, name, type(name, (), {}))
    pyside.QtWidgets = widgets
    sys.modules["PySide6"] = pyside
    sys.modules["PySide6.QtWidgets"] = widgets


def _assert_source_contracts(project_root: Path) -> None:
    arch_path = project_root / (
        "kanda_reasoner_app/manage_architecture/architecture_review_subtabs.py"
    )
    sync_path = project_root / (
        "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/"
        "ast_audit_planner_sync.py"
    )
    shell_path = project_root / (
        "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/gui_shell.py"
    )
    for path in (arch_path, sync_path, shell_path):
        ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        assert len(path.read_text(encoding="utf-8").splitlines()) <= 500

    arch_text = arch_path.read_text(encoding="utf-8")
    assert "if index == 2:" in arch_text
    assert "sync_planner_from_ast_audit_target(window)" in arch_text
    assert "refresh_large_file_refactor_planner_status(window)" in arch_text

    sync_text = sync_path.read_text(encoding="utf-8")
    for marker in (
        "refresh_warning_input_gate(window)",
        "analyze_python_file(selected_path)",
        "build_split_plan(report, settings)",
        "build_docstring_proposals(report, plan)",
        "blocked_not_warning_candidate",
        "_clear_target_specific_planner_state(window)",
    ):
        assert marker in sync_text, marker


def _install_sync_module_stubs(project_root: Path) -> object:
    """Load the sync module without executing an unrelated package __init__."""
    package_name = (
        "kanda_reasoner_app.manage_architecture.large_file_refactor_planner"
    )
    package = types.ModuleType(package_name)
    package.__path__ = [
        str(
            project_root
            / "kanda_reasoner_app/manage_architecture/large_file_refactor_planner"
        )
    ]
    sys.modules[package_name] = package

    target_queue = types.ModuleType(
        "kanda_reasoner_app.manage_architecture.large_module_target_queue"
    )

    def normalize_target_text(root_text: str, path_text: str) -> str:
        root = Path(root_text).resolve()
        path = Path(path_text).resolve()
        try:
            return path.relative_to(root).as_posix()
        except ValueError:
            return str(path)

    target_queue.normalize_target_text = normalize_target_text
    sys.modules[target_queue.__name__] = target_queue

    def stub(relative_name: str, **values: object) -> None:
        name = f"{package_name}.{relative_name}"
        module = types.ModuleType(name)
        for key, value in values.items():
            setattr(module, key, value)
        sys.modules[name] = module

    class PlannerSettings:
        def __init__(self, **kwargs: object) -> None:
            self.values = kwargs

    class PlannerState:
        BLOCKED = types.SimpleNamespace(value="blocked")
        DOCSTRING_READY = types.SimpleNamespace(value="docstring_ready")

    stub("analysis_formatting", format_analysis_report=lambda report: "ANALYSIS")
    stub("ast_analysis", analyze_python_file=lambda path: object())
    stub(
        "docstring_formatting",
        format_docstring_proposals=lambda proposals: "DOCSTRINGS",
    )
    stub(
        "docstring_planner",
        build_docstring_proposals=lambda report, plan: ["docstring"],
    )
    stub(
        "gui_warning_input_gate",
        refresh_warning_input_gate=lambda window: None,
        sync_warning_input_selection=lambda window: None,
    )
    stub("models", PlannerSettings=PlannerSettings, PlannerState=PlannerState)
    stub("split_formatting", format_split_plan=lambda plan: "PLAN")
    stub(
        "split_planner",
        build_split_plan=lambda report, settings: types.SimpleNamespace(status="ready"),
    )

    module_name = f"{package_name}.ast_audit_planner_sync"
    module_path = (
        project_root
        / "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/"
        "ast_audit_planner_sync.py"
    )
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def _assert_runtime_sync(project_root: Path, temp_root: Path) -> None:
    _install_pyside_stub()
    module = _install_sync_module_stubs(project_root)

    target_a = temp_root / "alpha.py"
    target_b = temp_root / "beta.py"
    target_a.write_text("def alpha():\n    return 1\n", encoding="utf-8")
    target_b.write_text("def beta():\n    return 2\n", encoding="utf-8")
    candidates = [
        _Candidate(str(target_a), "alpha.py"),
        _Candidate(str(target_b), "beta.py"),
    ]
    window = _Window(temp_root, target_b)

    def fake_refresh(current: object) -> None:
        current._large_file_refactor_planner_candidates = candidates
        current._large_file_refactor_warning_input_gate_open = True
        current._large_file_refactor_candidate_table.selectRow(0)
        current._large_file_refactor_planner_selected_path = str(target_a)
        current._large_file_refactor_target_edit.setText("alpha.py")

    def fake_sync_selection(current: object) -> None:
        row = current._large_file_refactor_candidate_table.currentRow()
        candidate = current._large_file_refactor_planner_candidates[row]
        current._large_file_refactor_planner_selected_path = candidate.path
        current._large_file_refactor_target_edit.setText(candidate.relative_path)

    report = object()
    plan = types.SimpleNamespace(status="ready")
    proposals = ["docstring"]
    module.refresh_warning_input_gate = fake_refresh
    module.sync_warning_input_selection = fake_sync_selection
    module.analyze_python_file = lambda path: report
    module.build_split_plan = lambda current_report, settings: plan
    module.build_docstring_proposals = lambda current_report, current_plan: proposals
    module.format_analysis_report = lambda current_report: "ANALYSIS"
    module.format_split_plan = lambda current_plan: "PLAN"
    module.format_docstring_proposals = lambda current_proposals: "DOCSTRINGS"

    result = module.sync_planner_from_ast_audit_target(window)
    assert result.status == "populated"
    assert result.candidate_index == 1
    assert result.selected_path == str(target_b)
    assert window._large_file_refactor_candidate_table.currentRow() == 1
    assert window._large_file_refactor_target_edit.text() == "beta.py"
    assert window._large_file_refactor_evidence_output.toPlainText() == "ANALYSIS"
    assert window._large_file_refactor_plan_output.toPlainText() == (
        "PLAN\n\nDOCSTRINGS"
    )
    assert window._large_file_refactor_last_analysis is report
    assert window._large_file_refactor_last_plan is plan
    assert window._large_file_refactor_docstring_proposals == proposals


def validate(project_root: str) -> None:
    """Run source and runtime-focused validation."""
    root = Path(project_root).resolve()
    _assert_source_contracts(root)
    temp_root = root / "_delete_after_daily_work" / "ast_target_auto_sync_fixture"
    temp_root.mkdir(parents=True, exist_ok=True)
    try:
        _assert_runtime_sync(root, temp_root)
    finally:
        for child in temp_root.glob("*"):
            child.unlink(missing_ok=True)
        temp_root.rmdir()
    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python test_large_file_refactor_planner_ast_target_auto_sync_v1.py <project_root>")
    validate(sys.argv[1])
