#!/usr/bin/env python3
# project-path: tools/validate_freeze_list_frozen_manager_responsive_v1.py
"""Validate responsive background execution for the List Frozen manager."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import py_compile
import shutil
import sys
import tempfile
import time

FEATURE_ID = "freeze-list-frozen-manager-responsive-v1"
TOUCHED = [
    "kanda_reasoner_app/freeze_after_update/frozen_entry_management.py",
    "kanda_reasoner_app/freeze_after_update_gui/_frozen_list_dialog.py",
    "kanda_reasoner_app/freeze_after_update_gui/_frozen_list_model.py",
    "kanda_reasoner_app/freeze_after_update_gui/_frozen_list_worker.py",
    "kanda_reasoner_app/freeze_after_update_gui/_ui_builder.py",
    "kanda_reasoner_app/freeze_after_update_gui/freeze_after_update_tab.py",
    "kanda_prompt_workspace/prompt_tools/startup_freeze_entry_summary.py",
    "tools/validate_freeze_list_frozen_manager_responsive_v1.py",
]


def require(condition: bool, message: str) -> None:
    """Raise one deterministic validation failure."""
    if not condition:
        raise AssertionError(message)


def read(root: Path, relative: str) -> str:
    """Read one exact installed source file."""
    path = root / relative
    require(path.is_file(), "Missing expected file: " + relative)
    return path.read_text(encoding="utf-8-sig")


def write_entry(
    path: Path,
    *,
    freeze_id: str,
    title: str,
    date_text: str,
    status: str = "frozen",
    superseded_by: str = "null",
) -> None:
    """Write one deterministic frozen-entry fixture."""
    path.write_text(
        "---\n"
        f'freeze_id: "{freeze_id}"\n'
        f'feature_title: "{title}"\n'
        'box: "sample.box"\n'
        f'status: "{status}"\n'
        f'date: "{date_text}"\n'
        f"superseded_by: {superseded_by}\n"
        "---\n\n"
        f"# {title}\n",
        encoding="utf-8",
    )


def validate_static(root: Path) -> None:
    """Validate source ownership, virtualized rendering, and line limits."""
    for relative in TOUCHED:
        path = root / relative
        py_compile.compile(str(path), doraise=True)
        require(
            len(read(root, relative).splitlines()) <= 500,
            relative + " exceeds 500 lines",
        )
    ui = read(root, "kanda_reasoner_app/freeze_after_update_gui/_ui_builder.py")
    tab = read(root, "kanda_reasoner_app/freeze_after_update_gui/freeze_after_update_tab.py")
    dialog = read(root, "kanda_reasoner_app/freeze_after_update_gui/_frozen_list_dialog.py")
    model = read(root, "kanda_reasoner_app/freeze_after_update_gui/_frozen_list_model.py")
    worker = read(root, "kanda_reasoner_app/freeze_after_update_gui/_frozen_list_worker.py")
    manager = read(root, "kanda_reasoner_app/freeze_after_update/frozen_entry_management.py")
    startup = read(root, "kanda_prompt_workspace/prompt_tools/startup_freeze_entry_summary.py")

    blueprint_pos = ui.index("freeze_copy_row.addWidget(self.get_blueprint_freeze_button, 0)")
    list_pos = ui.index("freeze_copy_row.addWidget(self.list_frozen_button, 0)")
    require(list_pos > blueprint_pos, "List Frozen is not after Get blueprint Freeze")
    require('QPushButton("List Frozen")' in ui, "List Frozen button missing")
    require("color: #0057B8" in ui, "List Frozen blue font missing")
    require("FreezeFrozenListMixin" in tab, "List Frozen mixin missing from tab")

    require("QThread(self)" in dialog, "Owned List Frozen QThread missing")
    require("FrozenListWorker" in dialog, "Background worker is not used")
    require("QTableView" in dialog, "Virtualized QTableView is missing")
    require("QTableWidget" not in dialog, "Legacy item-heavy QTableWidget remains")
    require("QApplication.processEvents" not in dialog, "GUI-thread processEvents workaround remains")
    require("refresh_ai_compliance_context" not in dialog, "Context refresh still runs in GUI module")
    for token in (
        "activate_frozen_entries",
        "delete_last_deprecated_entry",
        "delete_selected_deprecated_entries",
        "inactivate_frozen_entries",
        "list_managed_frozen_entries",
        "undelete_last_frozen_entry",
    ):
        require(token not in dialog, "Backend operation remains in GUI module: " + token)
        require(token in worker, "Worker is missing backend operation: " + token)
    require("refresh_ai_compliance_context" in worker, "Worker context refresh missing")
    require("completed = Signal(object)" in worker, "Immutable worker result signal missing")
    require("finished = Signal()" in worker, "Terminal worker signal missing")
    require("QAbstractTableModel" in model, "Virtualized table model missing")
    require("beginResetModel" in model and "endResetModel" in model, "Atomic model reset missing")
    require("closeEvent" in dialog and "event.ignore()" in dialog, "Busy close lifecycle guard missing")
    require("setEnabled(not busy)" in dialog, "Busy action lock missing")
    require("thread.finished.connect(thread.deleteLater)" in dialog, "Thread cleanup missing")
    require("worker.finished.connect(worker.deleteLater)" in dialog, "Worker cleanup missing")
    for label in (
        "Delete Last",
        "Delete Selected",
        "Undelete Last Deletion",
        "Inactivate",
        "Activate",
        "Close",
    ):
        require(label in dialog, "List Frozen action missing: " + label)
    for token in (
        "delete_selected_deprecated_entries",
        "delete_last_deprecated_entry",
        "undelete_last_frozen_entry",
        'memory_root / "deleted_entries"',
        "os.replace",
        "Active frozen entries cannot be deleted. Inactivate them first",
        '"status": "frozen" if active else "deprecated"',
        'updates["superseded_by"] = None',
        "write_freeze_index(project_root)",
    ):
        require(token in manager, "Frozen-entry manager missing contract: " + token)
    require(
        "_entry_is_active" in startup and 'status in {"active", "frozen"}' in startup,
        "Startup active-only filter missing",
    )
    print("LIST_FROZEN_BACKGROUND_QTHREAD_OWNERSHIP: PASS")
    print("LIST_FROZEN_GUI_THREAD_FILESYSTEM_ISOLATION: PASS")
    print("LIST_FROZEN_VIRTUALIZED_TABLE_MODEL: PASS")
    print("LIST_FROZEN_BUSY_CLOSE_LIFECYCLE_GUARD: PASS")
    print("LIST_FROZEN_EXISTING_ACTIONS_PRESERVED: PASS")
    print("TOUCHED_SOURCE_MODULES_MAX_500_LINES: PASS")


def validate_backend(root: Path) -> None:
    """Validate existing state-management behavior remains unchanged."""
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    from kanda_reasoner_app.freeze_after_update.frozen_entry_management import (
        activate_frozen_entries,
        delete_last_deprecated_entry,
        delete_selected_deprecated_entries,
        inactivate_frozen_entries,
        list_managed_frozen_entries,
        undelete_last_frozen_entry,
    )
    from kanda_reasoner_app.freeze_after_update.paths import build_paths
    from kanda_prompt_workspace.prompt_tools.startup_freeze_entry_summary import (
        latest_freeze_entry_files,
    )

    with tempfile.TemporaryDirectory(prefix="kanda_list_frozen_responsive_") as temp_dir:
        project_root = Path(temp_dir) / "fixture_project"
        project_root.mkdir()
        paths = build_paths(project_root)
        support_root = paths.box_root.parent
        try:
            paths.entries_root.mkdir(parents=True)
            old_path = paths.entries_root / "freeze-20260701-old.md"
            new_path = paths.entries_root / "freeze-20260702-new.md"
            write_entry(
                old_path,
                freeze_id="freeze-20260701-old",
                title="Old Active Freeze",
                date_text="2026-07-01",
            )
            write_entry(
                new_path,
                freeze_id="freeze-20260702-new",
                title="New Active Freeze",
                date_text="2026-07-02",
            )
            entries = list_managed_frozen_entries(project_root)
            require(
                [item["freeze_id"] for item in entries]
                == ["freeze-20260702-new", "freeze-20260701-old"],
                "Newest-first order failed",
            )
            inactivate_frozen_entries(project_root, [new_path])
            entries = list_managed_frozen_entries(project_root)
            require(not entries[0]["active"], "Inactivate did not deprecate")
            startup_entries = latest_freeze_entry_files(paths.memory_root, limit=10)
            require(
                new_path not in startup_entries and old_path in startup_entries,
                "Deprecated entry remained active in startup context",
            )
            try:
                delete_selected_deprecated_entries(project_root, [old_path])
            except ValueError:
                pass
            else:
                raise AssertionError("Active frozen entry deletion was not blocked")
            deleted = delete_last_deprecated_entry(project_root)
            moved_path = Path(deleted["deleted"][0]["to"])
            require(moved_path.is_file(), "Reversible deleted file missing")
            index = json.loads(paths.freeze_index.read_text(encoding="utf-8"))
            require(len(index["freezes"]) == 1, "Index was not updated after deletion")
            restored = undelete_last_frozen_entry(project_root)
            require(Path(restored["restored_to"]).is_file(), "Undelete failed")
            activate_frozen_entries(project_root, [new_path])
            text = new_path.read_text(encoding="utf-8-sig")
            require(
                'status: "frozen"' in text and "superseded_by: null" in text,
                "Activate did not normalize frontmatter",
            )
        finally:
            shutil.rmtree(support_root, ignore_errors=True)
    print("LIST_FROZEN_BACKEND_BEHAVIOR_PRESERVED: PASS")
    print("LIST_FROZEN_DEPRECATED_STARTUP_EXCLUSION: PASS")
    print("LIST_FROZEN_REVERSIBLE_DELETE_UNDELETE: PASS")


def _wait_until(app, predicate, *, timeout: float = 5.0) -> bool:
    """Pump Qt events until a predicate becomes true or timeout expires."""
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        app.processEvents()
        if predicate():
            return True
        time.sleep(0.01)
    app.processEvents()
    return bool(predicate())


def validate_real_qt(root: Path) -> None:
    """Prove loading and mutations leave the real Qt event loop responsive."""
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    if os.name == "nt" and Path("C:/Windows/Fonts").is_dir():
        os.environ.setdefault("QT_QPA_FONTDIR", "C:/Windows/Fonts")
    try:
        from PySide6.QtCore import QCoreApplication, QEvent, QTimer, Qt
        from PySide6.QtWidgets import QApplication, QPushButton, QTableView
    except ImportError as exc:
        raise AssertionError("PySide6 is required for responsive List Frozen validation") from exc
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    from kanda_reasoner_app.freeze_after_update.paths import build_paths
    from kanda_reasoner_app.freeze_after_update_gui import _frozen_list_worker as worker_module
    from kanda_reasoner_app.freeze_after_update_gui.freeze_after_update_tab import FreezeAfterUpdateTab

    original_list = worker_module.list_managed_frozen_entries
    original_refresh = worker_module.refresh_ai_compliance_context

    def slow_list(project_root):
        time.sleep(0.35)
        return original_list(project_root)

    def slow_refresh(project_root):
        time.sleep(0.35)
        return {"startup_context_refreshed": True, "errors": []}

    worker_module.list_managed_frozen_entries = slow_list
    worker_module.refresh_ai_compliance_context = slow_refresh
    created_app = QApplication.instance() is None
    app = QApplication.instance() or QApplication([])
    with tempfile.TemporaryDirectory(prefix="kanda_list_frozen_qt_responsive_") as temp_dir:
        project_root = Path(temp_dir) / "fixture_project"
        project_root.mkdir()
        paths = build_paths(project_root)
        support_root = paths.box_root.parent
        try:
            paths.entries_root.mkdir(parents=True)
            write_entry(
                paths.entries_root / "freeze-old.md",
                freeze_id="freeze-old",
                title="Old Deprecated",
                date_text="2026-07-01",
                status="deprecated",
            )
            write_entry(
                paths.entries_root / "freeze-new.md",
                freeze_id="freeze-new",
                title="New Active",
                date_text="2026-07-02",
            )
            tab = FreezeAfterUpdateTab()
            tab.set_project_root(project_root)
            list_button = tab.findChild(
                QPushButton,
                "freeze_after_update_list_frozen_button",
            )
            require(list_button is not None, "Real List Frozen button missing")
            load_tick = {"fired": False, "while_busy": False}
            list_button.click()
            dialog = tab._frozen_list_dialog
            require(dialog is not None and dialog.isVisible(), "Floating window did not open")

            def record_load_tick() -> None:
                load_tick["fired"] = True
                load_tick["while_busy"] = bool(dialog._busy)

            QTimer.singleShot(50, record_load_tick)
            require(
                _wait_until(app, lambda: load_tick["fired"], timeout=1.0),
                "Qt timer did not run during background list loading",
            )
            require(load_tick["while_busy"], "List loading completed on or blocked the GUI thread")
            dialog.close()
            app.processEvents()
            require(dialog.isVisible(), "Busy dialog close lifecycle guard failed")
            require(
                _wait_until(app, lambda: not dialog._busy, timeout=4.0),
                "Background list loading did not finish",
            )
            table = dialog.findChild(QTableView, "freeze_list_frozen_table")
            require(table is not None, "Virtualized real QTableView missing")
            require(dialog.table_model.rowCount() == 2, "Frozen table rows missing")
            require(
                dialog.table_model.index(0, 3).data() == "New Active",
                "Newest entry is not at top",
            )
            synthetic = [
                {
                    "path": Path("entry") / f"freeze-{index}.md",
                    "active": index % 2 == 0,
                    "date": "2026-07-24",
                    "feature_title": f"Feature {index}",
                    "freeze_id": f"freeze-{index}",
                    "box": "sample.box",
                }
                for index in range(1200)
            ]
            dialog.table_model.replace_entries(synthetic)
            require(dialog.table_model.rowCount() == 1200, "Virtualized large snapshot failed")
            dialog.table_model.replace_entries(dialog._entries)
            table.selectRow(0)
            dialog._confirm = lambda _title, _message: True
            mutation_tick = {"fired": False, "while_busy": False}
            dialog._inactivate_selected()

            def record_mutation_tick() -> None:
                mutation_tick["fired"] = True
                mutation_tick["while_busy"] = bool(dialog._busy)

            QTimer.singleShot(50, record_mutation_tick)
            require(
                _wait_until(app, lambda: mutation_tick["fired"], timeout=1.0),
                "Qt timer did not run during background mutation",
            )
            require(mutation_tick["while_busy"], "Mutation blocked the GUI thread")
            require(not dialog.close_button.isEnabled(), "Close was not guarded while busy")
            require(
                _wait_until(app, lambda: not dialog._busy, timeout=5.0),
                "Background mutation did not finish",
            )
            require(
                dialog.table_model.index(0, 1).data() == "Deprecated",
                "Inactivate result was not refreshed",
            )
            color = dialog.table_model.index(0, 1).data(Qt.ItemDataRole.ForegroundRole)
            require(color.name().casefold() == "#b00020", "Deprecated row is not red")
            dialog.close()
            app.processEvents()
            QCoreApplication.sendPostedEvents(None, QEvent.Type.DeferredDelete)
            app.processEvents()
            require(tab._frozen_list_dialog is None, "Closed dialog reference was not cleared")
            list_button.click()
            require(tab._frozen_list_dialog is not None, "Window could not reopen")
            require(
                _wait_until(app, lambda: not tab._frozen_list_dialog._busy, timeout=4.0),
                "Reopened background load did not finish",
            )
            tab._frozen_list_dialog.close()
            tab.close()
            tab.deleteLater()
            QCoreApplication.sendPostedEvents(None, QEvent.Type.DeferredDelete)
            app.processEvents()
        finally:
            shutil.rmtree(support_root, ignore_errors=True)
    worker_module.list_managed_frozen_entries = original_list
    worker_module.refresh_ai_compliance_context = original_refresh
    if created_app:
        app.quit()
        QCoreApplication.sendPostedEvents(None, QEvent.Type.DeferredDelete)
        app.processEvents()
    print("REAL_QT_LIST_FROZEN_INITIAL_LOAD_RESPONSIVE: PASS")
    print("REAL_QT_LIST_FROZEN_MUTATION_RESPONSIVE: PASS")
    print("REAL_QT_LIST_FROZEN_BUSY_CLOSE_GUARD: PASS")
    print("REAL_QT_LIST_FROZEN_CLOSE_REOPEN: PASS")
    print("REAL_QT_LIST_FROZEN_1200_ROW_VIRTUAL_MODEL: PASS")


def run_validation(
    *,
    root: Path,
    static_only: bool = False,
    skip_real_qt: bool = False,
    feature_id: str = FEATURE_ID,
) -> int:
    """Run static, backend, and real-Qt responsive validation."""
    try:
        validate_static(root)
        validate_backend(root)
        if not static_only and not skip_real_qt:
            validate_real_qt(root)
        print("VALIDATION OK: " + feature_id)
        print("STATUS: IN_SYNC")
        return 0
    except Exception as exc:
        print("VALIDATION FAILED: " + feature_id)
        print(str(exc))
        return 1


def main() -> int:
    """Parse CLI arguments and run validation."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--static-only", action="store_true")
    parser.add_argument("--skip-real-qt", action="store_true")
    args = parser.parse_args()
    return run_validation(
        root=Path(args.root).expanduser().resolve(),
        static_only=args.static_only,
        skip_real_qt=args.skip_real_qt,
    )


if __name__ == "__main__":
    raise SystemExit(main())
