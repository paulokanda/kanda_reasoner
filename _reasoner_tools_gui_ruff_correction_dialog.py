# project-path: _reasoner_tools_gui_ruff_correction_dialog.py
"""Private PySide6 adapter for the frozen Ruff correction workflow."""

from __future__ import annotations

from concurrent.futures import Future, ThreadPoolExecutor
import json
from pathlib import Path
import shutil
import subprocess
from typing import Any, Callable, Sequence

__all__: list[str] = []

_DIALOG_OBJECT_NAME = "engineeringSafetyRuffCorrectionDialog"
_DEFAULT_MAX_FILES = 25


def _split_scope_paths(value: str) -> tuple[str, ...]:
    """Return normalized scope entries from newline or semicolon text."""
    output: list[str] = []
    seen: set[str] = set()
    for raw_line in str(value or "").replace(";", "\n").splitlines():
        item = raw_line.strip()
        if not item:
            continue
        marker = item.casefold()
        if marker in seen:
            continue
        seen.add(marker)
        output.append(item)
    return tuple(output)


def _read_ruff_version(executable: str) -> str:
    """Return the semantic version reported by one Ruff executable."""
    completed = subprocess.run(
        [str(executable), "--version"],
        capture_output=True,
        text=True,
        check=False,
        timeout=20.0,
    )
    if completed.returncode != 0:
        return ""
    text = (completed.stdout or completed.stderr or "").strip()
    parts = text.split()
    if len(parts) >= 2 and parts[0].casefold() == "ruff":
        return parts[1].strip()
    return ""


def _ruff_candidates(project_root: Path) -> tuple[str, ...]:
    """Return deterministic candidate executables without installing tools."""
    output: list[str] = []
    path_ruff = shutil.which("ruff")
    if path_ruff:
        output.append(path_ruff)
    daily_root = project_root.parent / (project_root.name + "_delete_after_daily_work")
    output.extend(
        [
            str(daily_root / "ruff_0_15_21_env" / "Scripts" / "ruff.exe"),
            str(daily_root / "ruff_0_15_21_env" / "bin" / "ruff"),
        ]
    )
    unique: list[str] = []
    seen: set[str] = set()
    for item in output:
        marker = str(Path(item)).casefold()
        if marker in seen:
            continue
        seen.add(marker)
        unique.append(item)
    return tuple(unique)


def _resolve_exact_ruff_executable(
    project_root: str | Path,
    candidates: Sequence[str] | None = None,
) -> str:
    """Resolve an existing Ruff executable matching the canonical policy."""
    from kanda_reasoner_app.source_hygiene.ruff_policy_identity import (
        resolve_ruff_policy_identity,
    )

    root = Path(project_root).expanduser().resolve()
    policy = resolve_ruff_policy_identity(root)
    required = policy.required_version.removeprefix("==").strip()
    checked: list[str] = []
    for candidate in tuple(candidates or _ruff_candidates(root)):
        path = Path(candidate).expanduser()
        if not path.is_file():
            continue
        checked.append(str(path))
        if _read_ruff_version(str(path)) == required:
            return str(path.resolve())
    detail = "|".join(checked) if checked else "none"
    raise RuntimeError(
        "RUFF_CORRECTION_EXACT_RUFF_NOT_FOUND:required="
        + required
        + ":checked="
        + detail
    )


def _preview_text(record: Any) -> str:
    """Render a preview manifest and exact diff for human review."""
    manifest = json.dumps(
        record.to_dict(),
        ensure_ascii=True,
        indent=2,
        sort_keys=True,
    )
    diff_path = Path(str(record.diff_path))
    diff_text = diff_path.read_text(encoding="utf-8", errors="strict")
    return manifest + "\n\nEXACT DIFF\n" + diff_text


def _receipt_text(receipt: Any) -> str:
    """Render one apply receipt for the GUI output panel."""
    return json.dumps(
        receipt.to_dict(),
        ensure_ascii=True,
        indent=2,
        sort_keys=True,
    )


def create_ruff_correction_dialog(parent: Any, project_root: str | Path) -> Any:
    """Create the non-blocking reviewed Ruff correction dialog."""
    from PySide6.QtCore import QTimer  # type: ignore[import-not-found]
    from PySide6.QtWidgets import (  # type: ignore[import-not-found]
        QDialog,
        QFileDialog,
        QFormLayout,
        QHBoxLayout,
        QLabel,
        QLineEdit,
        QMessageBox,
        QPlainTextEdit,
        QPushButton,
        QSpinBox,
        QVBoxLayout,
        QWidget,
    )

    from kanda_reasoner_app.source_hygiene.ruff_correction_apply import (
        apply_ruff_correction_preview,
        load_ruff_correction_preview,
    )
    from kanda_reasoner_app.source_hygiene.ruff_correction_preview import (
        create_ruff_correction_preview,
    )

    root = Path(project_root).expanduser().resolve()
    dialog = QDialog(parent)
    dialog.setObjectName(_DIALOG_OBJECT_NAME)
    dialog.setWindowTitle("Ruff Reviewed Corrections")
    dialog.resize(980, 760)

    outer = QVBoxLayout(dialog)
    intro = QLabel(
        "Preview is read-only. Ruff fixes run only in a disposable shadow. "
        "Apply requires the exact token and a final confirmation."
    )
    intro.setWordWrap(True)
    outer.addWidget(intro)

    form = QFormLayout()
    root_edit = QLineEdit(str(root))
    root_edit.setReadOnly(True)
    root_edit.setObjectName("ruffCorrectionProjectRoot")
    form.addRow("Active project root", root_edit)

    scope_host = QWidget()
    scope_layout = QHBoxLayout(scope_host)
    scope_layout.setContentsMargins(0, 0, 0, 0)
    scope_edit = QLineEdit(".")
    scope_edit.setObjectName("ruffCorrectionScope")
    scope_edit.setToolTip(
        "Use project-relative files or folders; separate with semicolons."
    )
    browse_file = QPushButton("File")
    browse_folder = QPushButton("Folder")
    scope_layout.addWidget(scope_edit, 1)
    scope_layout.addWidget(browse_file)
    scope_layout.addWidget(browse_folder)
    form.addRow("Scope", scope_host)

    max_files = QSpinBox()
    max_files.setObjectName("ruffCorrectionMaxFiles")
    max_files.setRange(1, 500)
    max_files.setValue(_DEFAULT_MAX_FILES)
    form.addRow("Maximum candidate files", max_files)

    ruff_edit = QLineEdit()
    ruff_edit.setObjectName("ruffCorrectionRuffExecutable")
    ruff_edit.setReadOnly(True)
    form.addRow("Pinned Ruff executable", ruff_edit)

    preview_id_edit = QLineEdit()
    preview_id_edit.setObjectName("ruffCorrectionPreviewId")
    form.addRow("Preview ID", preview_id_edit)

    required_token = QLineEdit()
    required_token.setObjectName("ruffCorrectionRequiredToken")
    required_token.setReadOnly(True)
    form.addRow("Required confirmation token", required_token)

    typed_token = QLineEdit()
    typed_token.setObjectName("ruffCorrectionTypedToken")
    typed_token.setPlaceholderText("Type the exact token only after reviewing the diff")
    form.addRow("Type token to apply", typed_token)
    outer.addLayout(form)

    action_row = QHBoxLayout()
    preview_button = QPushButton("Create Preview")
    preview_button.setObjectName("ruffCorrectionCreatePreview")
    load_button = QPushButton("Load Preview")
    load_button.setObjectName("ruffCorrectionLoadPreview")
    apply_button = QPushButton("Apply Reviewed Preview")
    apply_button.setObjectName("ruffCorrectionApplyPreview")
    apply_button.setEnabled(False)
    close_button = QPushButton("Close")
    action_row.addWidget(preview_button)
    action_row.addWidget(load_button)
    action_row.addWidget(apply_button)
    action_row.addStretch(1)
    action_row.addWidget(close_button)
    outer.addLayout(action_row)

    status_label = QLabel("Ready")
    status_label.setObjectName("ruffCorrectionStatus")
    outer.addWidget(status_label)
    output = QPlainTextEdit()
    output.setObjectName("ruffCorrectionOutput")
    output.setReadOnly(True)
    output.setPlainText(
        "Choose a limited scope, create a Preview, and review the exact diff."
    )
    outer.addWidget(output, 1)

    executor = ThreadPoolExecutor(max_workers=1)
    state: dict[str, Any] = {"future": None, "preview": None, "closed": False}

    def _selected_relative_path(selected: str) -> str:
        selected_path = Path(selected).expanduser().resolve()
        try:
            relative = selected_path.relative_to(root)
        except ValueError as exc:
            raise RuntimeError("RUFF_CORRECTION_GUI_SCOPE_OUTSIDE_PROJECT") from exc
        return relative.as_posix() or "."

    def _choose_file() -> None:
        selected, _ = QFileDialog.getOpenFileName(
            dialog,
            "Select Python file",
            str(root),
            "Python files (*.py *.pyi *.pyw)",
        )
        if selected:
            scope_edit.setText(_selected_relative_path(selected))

    def _choose_folder() -> None:
        selected = QFileDialog.getExistingDirectory(
            dialog,
            "Select project folder",
            str(root),
        )
        if selected:
            scope_edit.setText(_selected_relative_path(selected))

    def _set_busy(busy: bool, message: str) -> None:
        preview_button.setEnabled(not busy)
        load_button.setEnabled(not busy)
        scope_edit.setEnabled(not busy)
        max_files.setEnabled(not busy)
        preview_id_edit.setEnabled(not busy)
        typed_token.setEnabled(not busy)
        status_label.setText(message)
        _refresh_apply_enabled(busy)

    def _refresh_apply_enabled(busy: bool = False) -> None:
        record = state.get("preview")
        token_matches = bool(record) and typed_token.text() == required_token.text()
        ready = bool(record) and str(record.status) == "PREVIEW_READY"
        apply_button.setEnabled(not busy and ready and token_matches)

    def _show_preview(record: Any, executable: str = "") -> None:
        state["preview"] = record
        preview_id_edit.setText(str(record.preview_id))
        required_token.setText(str(record.confirm_token))
        typed_token.clear()
        if executable:
            ruff_edit.setText(executable)
        output.setPlainText(_preview_text(record))
        status_label.setText(
            "Preview loaded: "
            + str(record.changed_file_count)
            + " changed file(s). Review required."
        )
        _refresh_apply_enabled(False)

    def _finish(kind: str, future: Future[Any]) -> None:
        state["future"] = None
        try:
            result = future.result()
            if kind in {"preview", "load"}:
                record, executable = result
                _show_preview(record, executable)
            else:
                receipt = result
                state["preview"] = None
                required_token.clear()
                typed_token.clear()
                output.setPlainText(_receipt_text(receipt))
                status_label.setText("Apply status: " + str(receipt.status))
                _refresh_apply_enabled(False)
        except Exception as exc:  # noqa: BLE001
            output.setPlainText(type(exc).__name__ + ": " + str(exc))
            status_label.setText("Blocked: " + str(exc))
            _set_busy(False, status_label.text())
        else:
            _set_busy(False, status_label.text())

    def _poll(kind: str, future: Future[Any]) -> None:
        if state["closed"]:
            return
        if future.done():
            _finish(kind, future)
            return
        QTimer.singleShot(150, lambda: _poll(kind, future))

    def _start(kind: str, func: Callable[[], Any], message: str) -> None:
        if state.get("future") is not None:
            status_label.setText("Another correction operation is still running.")
            return
        _set_busy(True, message)
        future = executor.submit(func)
        state["future"] = future
        QTimer.singleShot(150, lambda: _poll(kind, future))

    def _create_preview() -> None:
        scope = _split_scope_paths(scope_edit.text())

        def operation() -> tuple[Any, str]:
            executable = _resolve_exact_ruff_executable(root)
            record = create_ruff_correction_preview(
                root,
                scope_paths=scope or (".",),
                max_files=max_files.value(),
                ruff_argv_prefix=(executable,),
            )
            return record, executable

        _start("preview", operation, "Creating disposable correction Preview...")

    def _load_preview() -> None:
        preview_id = preview_id_edit.text().strip()
        if not preview_id:
            status_label.setText("Enter a Preview ID first.")
            return

        def operation() -> tuple[Any, str]:
            record = load_ruff_correction_preview(root, preview_id)
            executable = _resolve_exact_ruff_executable(root)
            return record, executable

        _start("load", operation, "Loading durable Preview evidence...")

    def _apply_preview() -> None:
        record = state.get("preview")
        if record is None:
            status_label.setText("Load or create a Preview first.")
            return
        token = typed_token.text()
        if token != str(record.confirm_token):
            status_label.setText("The exact confirmation token is required.")
            return
        answer = QMessageBox.question(
            dialog,
            "Apply reviewed Ruff Preview",
            "Apply Preview "
            + str(record.preview_id)
            + " to "
            + str(record.changed_file_count)
            + " active project file(s)?\n\n"
            "Backups, post-apply validation, and rollback are enforced.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if answer != QMessageBox.Yes:
            status_label.setText("Apply cancelled by user.")
            return

        def operation() -> Any:
            executable = _resolve_exact_ruff_executable(root)
            return apply_ruff_correction_preview(
                root,
                str(record.preview_id),
                confirm_token=token,
                ruff_argv_prefix=(executable,),
            )

        _start("apply", operation, "Applying reviewed Preview transaction...")

    def _close_dialog() -> None:
        if state.get("future") is not None:
            QMessageBox.warning(
                dialog,
                "Operation running",
                "Wait for the current correction operation to finish.",
            )
            return
        dialog.close()

    def _cleanup() -> None:
        state["closed"] = True
        executor.shutdown(wait=False, cancel_futures=True)

    browse_file.clicked.connect(_choose_file)
    browse_folder.clicked.connect(_choose_folder)
    preview_button.clicked.connect(_create_preview)
    load_button.clicked.connect(_load_preview)
    apply_button.clicked.connect(_apply_preview)
    close_button.clicked.connect(_close_dialog)
    typed_token.textChanged.connect(lambda _text: _refresh_apply_enabled(False))
    dialog.finished.connect(lambda _result: _cleanup())
    return dialog
