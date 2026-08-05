# project-path: tools/validate_shell_active_project_sync_v1.py
"""Validate canonical active-Project synchronization across KANDA tabs."""

from __future__ import annotations

import argparse
import ast
import importlib
import os
import sys
import tempfile
from pathlib import Path


FEATURE_ID = "shell-active-project-sync-v1r1"

FILES = (
    "kanda_reasoner_app/reasoner_tools_gui_shell/main_window.py",
    "kanda_reasoner_app/reasoner_tools_gui_shell/main_window_help/window_project_root.py",
    "kanda_reasoner_app/reasoner_tools_gui_shell/main_window_help/window_tool_patches.py",
    "kanda_reasoner_app/reasoner_tools_gui_shell/project_scope_sync.py",
)


def require(condition: bool, message: str) -> None:
    """Raise one deterministic validation failure."""
    if not condition:
        raise AssertionError(message)


def source(root: Path, relative: str) -> str:
    """Read one required source file."""
    path = root / relative
    require(path.is_file(), "missing source file: " + relative)
    return path.read_text(encoding="utf-8")


def validate_static(root: Path) -> None:
    """Validate ownership, ordering, scope, and frozen boundaries."""
    texts = {relative: source(root, relative) for relative in FILES}
    for relative, text in texts.items():
        ast.parse(text, filename=relative)
        require(
            len(text.splitlines()) <= 500,
            relative + " exceeds 500 physical lines",
        )

    main = texts[FILES[0]]
    roots = texts[FILES[1]]
    patches = texts[FILES[2]]
    sync = texts[FILES[3]]

    require(
        "self._loaded_tools_by_tab_id: dict[str, QWidget] = {}" in main
        and "self._project_switch_epoch = 0" in main,
        "main shell does not own canonical loaded-tab Project state",
    )
    print("CANONICAL_ACTIVE_PROJECT_OWNER: PASS")

    require(
        "PROJECT_SCOPED_TAB_IDS" in sync
        and '"config_web_ai"' not in sync.split("PROJECT_SCOPED_TAB_IDS", 1)[1].split(")", 1)[0]
        and '"prompt_library"' not in sync.split("PROJECT_SCOPED_TAB_IDS", 1)[1].split(")", 1)[0],
        "global configuration tabs entered the project-scoped reset set",
    )
    require(
        "reset_project_scoped_widget" in sync
        and "apply_project_root_to_widget" in sync,
        "project-scoped reset/apply facades are missing",
    )
    print("GLOBAL_CONFIG_AND_PROMPT_LIBRARY_PRESERVED: PASS")

    forbidden_persistence = (
        ".unlink(",
        "rmtree(",
        "write_text(",
        "write_bytes(",
        "project_freeze_ledger",
        "Memorize Error",
    )
    require(
        not any(token in sync for token in forbidden_persistence),
        "transient reset owner contains a durable write/delete primitive",
    )
    print("DURABLE_PROJECT_MEMORY_UNTOUCHED: PASS")

    require(
        "self._loaded_tools_by_tab_id[spec.tab_id] = widget" in patches
        and "self._patch_common_project_root_fields(widget)" in patches,
        "loaded tabs are not registered before canonical root binding",
    )
    require(
        'setProperty(\n                "pyarchitect_project_root_bound",\n                False,' in patches
        and "self._bind_project_root_field(widget.project_root_edit)" in patches,
        "collector root field is not rebound after signal replacement",
    )
    print("ALL_PROJECT_ROOT_FIELDS_AND_BROWSE_RESULTS_BOUND: PASS")

    propagate_block = patches.split(
        "    def _propagate_project_root",
        1,
    )[1].split(
        "    def _apply_project_root_to_collector",
        1,
    )[0]
    reset_index = propagate_block.index("self._reset_loaded_project_scopes()")
    remember_index = propagate_block.index("self._remember_project_boundary(next_boundary)")
    apply_index = propagate_block.index(
        "self._apply_root_to_loaded_widget(widget, project_root)"
    )
    require(
        reset_index < remember_index < apply_index,
        "Project switch does not reset old scope before publishing the new root",
    )
    print("PROJECT_SWITCH_RESET_BEFORE_ROOT_PUBLICATION: PASS")

    require(
        "project_switch_block(tab_id, widget)" in roots
        and "transaction_blocks_project_switch" in sync
        and "_restore_canonical_project_root_fields()" in patches,
        "active or unresolved work does not fail closed",
    )
    print("ACTIVE_PROJECT_WORK_BLOCKS_UNSAFE_SWITCH: PASS")

    require(
        "reset_project_scoped_widget(tab_id, widget)" in roots
        and "_clear_project_text_surfaces(widget)" in sync
        and "_clear_project_collection_surfaces(widget)" in sync
        and 'if tab_id == "project_web_ai":' in sync,
        "global transient reset and frozen Project Web AI ownership are incomplete",
    )
    print("ALL_LOADED_PROJECT_TABS_CLEAR_TRANSIENT_STATE: PASS")

    print("TOUCHED_SOURCE_MODULES_MAX_500_LINES: PASS")


def validate_architecture(root: Path) -> None:
    """Require zero architecture warnings and zero symbol shadowing."""
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    architecture = importlib.import_module(
        "kanda_reasoner_app.manage_architecture.manage_architecture"
    )
    modules = {}
    for relative in (*FILES, "tools/validate_shell_active_project_sync_v1.py"):
        module, warnings = architecture.scan_module(
            root,
            root / relative,
            set(),
        )
        require(not warnings, relative + " warnings: " + repr(warnings))
        modules[module.module_id] = module
    issues = architecture.detect_symbol_shadowing_issues(root, modules)
    require(not issues, "Symbol shadowing remains: " + repr(issues))
    print("SHELL_ACTIVE_PROJECT_SYNC_ARCHITECTURE_WARNINGS_ZERO: PASS")
    print("SHELL_ACTIVE_PROJECT_SYNC_SYMBOL_SHADOWING_ZERO: PASS")


def _is_missing_pyside6_dependency(exc: ImportError) -> bool:
    """Return True only for an unavailable PySide6 or shiboken6 dependency."""
    module_name = str(getattr(exc, "name", "") or "")
    message = str(exc)
    return (
        module_name == "PySide6"
        or module_name.startswith("PySide6.")
        or module_name == "shiboken6"
        or module_name.startswith("shiboken6.")
        or "PySide6" in message
        or "shiboken6" in message
    )


def validate_real_qt(root: Path) -> bool:
    """Exercise field synchronization, reset, lazy load, and switch blocking."""
    try:
        from PySide6.QtWidgets import (
            QApplication,
            QLineEdit,
            QListWidget,
            QPlainTextEdit,
            QWidget,
        )
    except ImportError as exc:
        if not _is_missing_pyside6_dependency(exc):
            raise
        print("REAL_QT_ACTIVE_PROJECT_SYNC: NOT_APPLICABLE")
        return False

    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    sys.path.insert(0, str(root))
    from kanda_reasoner_app.reasoner_tools_gui_shell.main_window import (
        ReasonerToolsWindow,
    )
    from kanda_reasoner_app.reasoner_tools_gui_shell.tool_specs import ToolSpec

    app = QApplication.instance() or QApplication([])
    window = ReasonerToolsWindow()
    warning_reasons: list[str] = []
    window._show_project_switch_block = warning_reasons.append

    class ProjectTab(QWidget):
        def __init__(self) -> None:
            super().__init__()
            self.project_root_edit = QLineEdit()
            self.output = QPlainTextEdit()
            self.items = QListWidget()
            self.applied_roots: list[str] = []

        def set_project_root(self, project_root: Path) -> None:
            root_text = str(project_root)
            self.applied_roots.append(root_text)
            if self.project_root_edit.text() != root_text:
                self.project_root_edit.setText(root_text)

    class GlobalTab(QWidget):
        def __init__(self) -> None:
            super().__init__()
            self.notes = QPlainTextEdit()

    with tempfile.TemporaryDirectory(prefix="kanda-project-a-") as a_dir:
        with tempfile.TemporaryDirectory(prefix="kanda-project-b-") as b_dir:
            project_a = Path(a_dir).resolve()
            project_b = Path(b_dir).resolve()
            tab_a = ProjectTab()
            tab_b = ProjectTab()
            global_tab = GlobalTab()
            tab_a.output.setPlainText("old architecture log")
            tab_a.items.addItem("old architecture evidence")
            tab_b.output.setPlainText("old local AI answer")
            tab_b.items.addItem("old local AI memory")
            global_tab.notes.setPlainText("global configuration survives")

            window.current_project_root = project_a
            window._loaded_tools_by_tab_id = {
                "architecture_review": tab_a,
                "project_qa": tab_b,
                "config_web_ai": global_tab,
            }
            window._patch_common_project_root_fields(tab_a)
            window._patch_common_project_root_fields(tab_b)
            require(
                tab_a.project_root_edit.text() == str(project_a)
                and tab_b.project_root_edit.text() == str(project_a),
                "initial canonical root did not reach loaded tabs",
            )

            previous_epoch = window._project_switch_epoch
            tab_a.project_root_edit.setText(str(project_b))
            app.processEvents()

            require(window.current_project_root == project_b, "canonical root did not switch")
            require(
                tab_a.project_root_edit.text() == str(project_b)
                and tab_b.project_root_edit.text() == str(project_b),
                "root fields are not synchronized across loaded tabs",
            )
            require(
                not tab_a.output.toPlainText()
                and not tab_b.output.toPlainText()
                and tab_a.items.count() == 0
                and tab_b.items.count() == 0,
                "old Project text or collection state survived the switch",
            )
            require(
                global_tab.notes.toPlainText() == "global configuration survives",
                "global configuration state was cleared",
            )
            require(
                window._project_switch_epoch == previous_epoch + 1,
                "canonical Project epoch did not advance exactly once",
            )
            print("REAL_QT_ANY_TAB_ROOT_CHANGE_SYNCS_ALL_TABS: PASS")
            print("REAL_QT_OLD_PROJECT_TRANSIENT_STATE_CLEARED: PASS")
            print("REAL_QT_DIRECT_OWNED_SURFACES_CLEARED: PASS")
            print("REAL_QT_GLOBAL_CONFIGURATION_PRESERVED: PASS")

            lazy_tab = ProjectTab()
            spec = ToolSpec(
                step_title="Lazy fixture",
                source_hint="fixture/lazy.py",
                tab_id="docstring_assistant",
            )
            window._on_tool_loaded(spec, lazy_tab)
            require(
                lazy_tab.project_root_edit.text() == str(project_b)
                and lazy_tab.applied_roots[-1] == str(project_b),
                "newly loaded tab did not inherit canonical Project root",
            )
            print("REAL_QT_LAZY_TAB_INHERITS_CANONICAL_PROJECT: PASS")

            class RunningThread:
                def isRunning(self) -> bool:
                    return True

            tab_b._worker_thread = RunningThread()
            tab_a.output.setPlainText("must remain because switch is blocked")
            tab_a.project_root_edit.setText(str(project_a))
            app.processEvents()
            require(window.current_project_root == project_b, "blocked switch changed root")
            require(
                tab_a.project_root_edit.text() == str(project_b)
                and tab_b.project_root_edit.text() == str(project_b),
                "blocked switch did not restore canonical fields",
            )
            require(
                tab_a.output.toPlainText() == "must remain because switch is blocked",
                "blocked switch cleared state before admission",
            )
            require(warning_reasons, "blocked switch did not expose its reason")
            print("REAL_QT_ACTIVE_JOB_SWITCH_FAILS_CLOSED: PASS")

    window.close()
    app.processEvents()
    print("REAL_QT_ACTIVE_PROJECT_SYNC: PASS")
    return True


def main() -> int:
    """Run focused validation."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    args = parser.parse_args()
    root = Path(args.root).expanduser().resolve()
    validate_static(root)
    validate_architecture(root)
    validate_real_qt(root)
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
