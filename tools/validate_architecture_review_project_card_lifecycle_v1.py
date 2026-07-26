"""Focused validator for Architecture Review project-card ownership and lifecycle."""
from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace

from kanda_reasoner_app.manage_architecture.architecture_review_card_lifecycle import (
    bind_architecture_review_card_lifecycle,
    release_completed_architecture_review_card,
    tool_source_root,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_project_support_paths import (
    workbench_support_root,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_refactor_transaction import (
    detect_self_hosted_refactor,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_snapshot_bridge import (
    workbench_source_transaction_open,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_transaction_store import (
    default_workbench_transaction_root,
    legacy_workbench_transaction_root,
    migrate_legacy_workbench_transaction_state,
)
from kanda_reasoner_app.manage_architecture.large_module_split_audit import _resolve_target

__all__ = [
    "main",
]

FEATURE_ID = "architecture-review-project-card-machine-lifecycle-boundary-v1"
PROJECT_ROOT = Path(__file__).resolve().parents[1]


class Signal:
    """Minimal signal fixture."""

    def __init__(self) -> None:
        self.callbacks: list[object] = []

    def connect(self, callback: object) -> None:
        self.callbacks.append(callback)

    def emit(self, value: str) -> None:
        for callback in list(self.callbacks):
            callback(value)


class Edit:
    """Minimal line-edit fixture that emits text changes."""

    def __init__(self, text: str = "") -> None:
        self._text = text
        self.textChanged = Signal()
        self.placeholder = ""

    def text(self) -> str:
        return self._text

    def setText(self, value: str) -> None:
        self._text = str(value)
        self.textChanged.emit(self._text)

    def clear(self) -> None:
        self.setText("")

    def setPlaceholderText(self, value: str) -> None:
        self.placeholder = str(value)


class PlainText:
    """Minimal plain-text output fixture."""

    def __init__(self) -> None:
        self.value = ""

    def setPlainText(self, value: str) -> None:
        self.value = str(value)


class Toggle:
    """Minimal button/checkbox fixture."""

    def __init__(self) -> None:
        self.enabled = True
        self.checked = False

    def setEnabled(self, value: bool) -> None:
        self.enabled = bool(value)

    def setChecked(self, value: bool) -> None:
        self.checked = bool(value)




class RunningThread:
    """Minimal running-thread fixture."""

    def isRunning(self) -> bool:
        return True


class StatusBar:
    """Minimal status fixture."""

    def __init__(self) -> None:
        self.message = ""

    def showMessage(self, value: str) -> None:
        self.message = str(value)


class Window:
    """Architecture Review lifecycle fixture."""

    def __init__(self, root: Path, target: str) -> None:
        self._bar = StatusBar()
        self._root_path_edit = Edit(str(root))
        self._large_module_target_edit = Edit(target)
        self._large_module_split_output = PlainText()
        self._large_module_targets = [SimpleNamespace(path=target)]
        self._large_module_target_index = 0
        self._large_module_target_source = "audit"
        self._last_large_module_split_handoff = "handoff"
        self._large_file_refactor_planner_candidates = [SimpleNamespace(path=target)]
        self._large_file_refactor_warning_targets = [target]
        self._large_file_refactor_warning_input_gate_open = True
        self._large_file_refactor_planner_selected_path = target
        self._large_file_refactor_planner_state = "PLAN_READY"
        self._large_file_refactor_last_analysis = object()
        self._large_file_refactor_last_plan = object()
        self._large_file_refactor_docstring_proposals = [object()]
        self._large_file_refactor_target_edit = Edit(target)
        self._large_file_refactor_evidence_output = PlainText()
        self._large_file_refactor_plan_output = PlainText()
        self._large_file_refactor_workbench_plan_snapshot = object()
        self._large_file_refactor_workbench_intake = object()
        self._large_file_refactor_workbench_completion_evidence = object()
        self._large_file_refactor_workbench_completion_transaction = None
        self._large_file_refactor_workbench_completion_apply_outcome = None
        self._large_file_refactor_workbench_completion_rollback_result = None
        self._large_file_refactor_workbench_intake_output = PlainText()
        self._large_file_refactor_workbench_completion_status_output = PlainText()
        self._large_file_refactor_workbench_semantic_review_check = Toggle()
        self._large_file_refactor_workbench_warning_ack_check = Toggle()
        self._large_file_refactor_workbench_transaction_confirm_check = Toggle()
        for name in (
            "_large_file_refactor_workbench_dependency_button",
            "_large_file_refactor_workbench_real_preview_button",
            "_large_file_refactor_workbench_validate_button",
            "_large_file_refactor_workbench_preflight_button",
            "_large_file_refactor_workbench_source_payload_button",
            "_large_file_refactor_workbench_completion_prepare_button",
            "_large_file_refactor_workbench_transaction_prepare_button",
            "_large_file_refactor_workbench_refactor_large_module_button",
            "_large_file_refactor_workbench_transaction_rollback_button",
        ):
            setattr(self, name, Toggle())

    def statusBar(self) -> StatusBar:
        return self._bar

    def _sync_large_module_target_controls(self) -> None:
        return


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _validate_root_and_target_lifecycle() -> None:
    with TemporaryDirectory(prefix="kanda_card_lifecycle_") as raw:
        base = Path(raw)
        project_a = base / "project_a"
        project_b = base / "project_b"
        project_a.mkdir()
        project_b.mkdir()
        target_a = "pkg/large_a.py"
        target_b = "pkg/large_b.py"
        window = Window(project_a, target_a)
        bind_architecture_review_card_lifecycle(window)

        window._large_module_target_edit.setText(target_b)
        _assert(window._large_file_refactor_last_analysis is None, "TARGET_ANALYSIS_NOT_CLEARED")
        _assert(window._large_file_refactor_workbench_intake is None, "TARGET_WORKBENCH_NOT_CLEARED")

        window._large_file_refactor_last_analysis = object()
        window._large_file_refactor_workbench_intake = object()
        window._root_path_edit.setText(str(project_b))
        _assert(window._large_module_targets == [], "ROOT_AST_QUEUE_NOT_CLEARED")
        _assert(window._large_file_refactor_planner_candidates == [], "ROOT_PLANNER_QUEUE_NOT_CLEARED")
        _assert(window._large_file_refactor_workbench_intake is None, "ROOT_WORKBENCH_NOT_CLEARED")


def _validate_running_audit_blocks_root_switch() -> None:
    with TemporaryDirectory(prefix="kanda_card_running_audit_") as raw:
        base = Path(raw)
        project_a = base / "project_a"
        project_b = base / "project_b"
        project_a.mkdir()
        project_b.mkdir()
        window = Window(project_a, "large.py")
        window._worker_thread = RunningThread()
        bind_architecture_review_card_lifecycle(window)
        window._root_path_edit.setText(str(project_b))
        _assert(
            Path(window._root_path_edit.text()).resolve() == project_a.resolve(),
            "RUNNING_AUDIT_ROOT_SWITCHED",
        )


def _validate_open_transaction_blocks_switch() -> None:
    with TemporaryDirectory(prefix="kanda_card_open_tx_") as raw:
        base = Path(raw)
        project_a = base / "project_a"
        project_b = base / "project_b"
        project_a.mkdir()
        project_b.mkdir()
        window = Window(project_a, "large.py")
        bind_architecture_review_card_lifecycle(window)
        window._large_file_refactor_workbench_completion_transaction = object()
        window._root_path_edit.setText(str(project_b))
        _assert(Path(window._root_path_edit.text()).resolve() == project_a.resolve(), "OPEN_TX_ROOT_SWITCHED")
        _assert(workbench_source_transaction_open(window), "OPEN_TX_NOT_DETECTED")
        window._large_file_refactor_workbench_completion_apply_outcome = SimpleNamespace(
            final_transaction_state="COMPLETED_VALIDATED"
        )
        _assert(not workbench_source_transaction_open(window), "TERMINAL_TX_STILL_OPEN")


def _validate_completed_card_release() -> None:
    with TemporaryDirectory(prefix="kanda_card_release_") as raw:
        project = Path(raw) / "project"
        project.mkdir()
        first = "pkg/large_a.py"
        second = "pkg/large_b.py"
        window = Window(project, first)
        window._large_module_targets = [
            SimpleNamespace(path=first),
            SimpleNamespace(path=second),
        ]
        bind_architecture_review_card_lifecycle(window)
        window._large_file_refactor_workbench_completion_apply_outcome = SimpleNamespace(
            final_transaction_state="COMPLETED_VALIDATED"
        )
        release_completed_architecture_review_card(window)
        remaining = [item.path for item in window._large_module_targets]
        _assert(first not in remaining and second in remaining, "COMPLETED_CARD_NOT_EJECTED")
        _assert(window._large_file_refactor_workbench_completion_apply_outcome is None, "TOOL_MEMORY_RETAINED_OUTCOME")
        _assert(window._large_file_refactor_planner_candidates == [], "STALE_WARNING_QUEUE_RETAINED")


def _validate_project_target_containment() -> None:
    with TemporaryDirectory(prefix="kanda_card_target_") as raw:
        base = Path(raw)
        project = base / "project"
        project.mkdir()
        inside = project / "inside.py"
        outside = base / "outside.py"
        inside.write_text("x = 1\n", encoding="utf-8")
        outside.write_text("x = 2\n", encoding="utf-8")
        _assert(_resolve_target(project, inside) == inside.resolve(), "INSIDE_TARGET_REJECTED")
        try:
            _resolve_target(project, outside)
        except ValueError as exc:
            _assert(str(exc) == "TARGET_OUTSIDE_ACTIVE_PROJECT_ROOT", "WRONG_TARGET_BLOCKER")
        else:
            raise AssertionError("OUTSIDE_TARGET_ACCEPTED")


def _validate_tool_project_identity() -> None:
    tool_root = tool_source_root()
    with TemporaryDirectory(prefix="kanda_external_project_") as raw:
        external = Path(raw).resolve()
        _assert(not detect_self_hosted_refactor(external, tool_root), "EXTERNAL_PROJECT_FALSE_SELF_HOSTED")
    _assert(detect_self_hosted_refactor(tool_root, tool_root), "REAL_SELF_HOSTING_NOT_DETECTED")
    completion = (PROJECT_ROOT / "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_completion_gui.py").read_text(encoding="utf-8")
    _assert("tool_root=tool_source_root()" in completion, "COMPLETION_GUI_TOOL_ROOT_NOT_CANONICAL")
    _assert("tool_root=project_root" not in completion, "COMPLETION_GUI_COLLAPSES_TOOL_PROJECT")


def _validate_transaction_project_support_and_migration() -> None:
    with TemporaryDirectory(prefix="kanda_card_tx_root_") as raw:
        base = Path(raw)
        project = base / "project"
        project.mkdir()
        canonical = default_workbench_transaction_root(project)
        expected = workbench_support_root(project) / "transactions"
        _assert(canonical == expected, "TRANSACTION_ROOT_NOT_PROJECT_SUPPORT")
        legacy = legacy_workbench_transaction_root(project)
        legacy.mkdir(parents=True)
        (legacy / "workbench_transactions.sqlite3").write_bytes(b"legacy")
        legacy_lane = legacy.parent / "project_mutation_lane.sqlite3"
        legacy_lane.write_bytes(b"lane")
        migrated = migrate_legacy_workbench_transaction_state(project)
        _assert(migrated == canonical, "MIGRATION_WRONG_DESTINATION")
        _assert((canonical / "workbench_transactions.sqlite3").read_bytes() == b"legacy", "LEGACY_TX_NOT_MOVED")
        _assert((canonical.parent / "project_mutation_lane.sqlite3").read_bytes() == b"lane", "LEGACY_LANE_NOT_MOVED")
        _assert(not legacy.exists(), "LEGACY_TX_ROOT_RETAINED")


def _validate_source_size_and_static_guards() -> None:
    touched = [
        "kanda_reasoner_app/manage_architecture/architecture_review_card_lifecycle.py",
        "kanda_reasoner_app/manage_architecture/architecture_review_subtabs.py",
        "kanda_reasoner_app/manage_architecture/large_module_split_audit_gui.py",
        "kanda_reasoner_app/manage_architecture/large_module_split_audit.py",
        "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/ast_audit_planner_sync.py",
        "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/gui_warning_input_gate.py",
        "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_snapshot_bridge.py",
        "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_completion_gui.py",
        "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_completion_workflow.py",
        "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_transaction_store.py",
    ]
    for relative in touched:
        path = PROJECT_ROOT / relative
        lines = len(path.read_bytes().splitlines())
        _assert(lines <= 500, f"TOUCHED_MODULE_TOO_LARGE:{relative}:{lines}")
    lifecycle = (PROJECT_ROOT / touched[0]).read_text(encoding="utf-8")
    _assert("Project Root changed. Architecture Review unloaded the previous project card." in lifecycle, "ROOT_LIFECYCLE_GUARD_MISSING")
    _assert("current refactor transaction still owns the card" in lifecycle, "OPEN_TRANSACTION_EJECTION_GUARD_MISSING")


def main() -> int:
    _validate_root_and_target_lifecycle()
    print("ROOT_CHANGE_UNLOADS_AST_PLANNER_WORKBENCH: PASS")
    print("TARGET_CHANGE_INVALIDATES_DOWNSTREAM_CARD_STATE: PASS")
    _validate_running_audit_blocks_root_switch()
    print("RUNNING_AUDIT_BLOCKS_PROJECT_CARD_SWITCH: PASS")
    _validate_open_transaction_blocks_switch()
    print("OPEN_TRANSACTION_BLOCKS_CARD_EJECTION: PASS")
    _validate_completed_card_release()
    print("COMPLETED_REFACTOR_RELEASES_TOOL_CARD_MEMORY: PASS")
    _validate_project_target_containment()
    print("AST_TARGET_ACTIVE_PROJECT_ONLY: PASS")
    _validate_tool_project_identity()
    print("TOOL_PROJECT_IDENTITY_NOT_COLLAPSED: PASS")
    _validate_transaction_project_support_and_migration()
    print("WORKBENCH_TRANSACTION_STATE_PROJECT_SUPPORT_ONLY: PASS")
    print("LEGACY_TRANSACTION_STATE_MIGRATION: PASS")
    _validate_source_size_and_static_guards()
    print("TOUCHED_SOURCE_MODULES_MAX_500_LINES: PASS")
    print("ARCHITECTURE_REVIEW_CARD_MACHINE_LIFECYCLE: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
