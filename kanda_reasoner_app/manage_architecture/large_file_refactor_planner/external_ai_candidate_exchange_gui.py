"""Qt controls for outbound external AI candidate exchange packages."""
from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import (
    QApplication,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QVBoxLayout,
)

from .external_ai_candidate_exchange_service import create_external_ai_candidate_exchange
from .external_ai_candidate_return_dialog import choose_external_ai_return_input
from .external_ai_candidate_return_text_intake import (
    import_external_ai_candidate_answer_text,
)
from .external_ai_exchange_workspace import (
    clean_external_ai_exchange_workspace,
)
from .external_ai_candidate_return_intake import (
    ai_return_import_readiness_blockers,
    import_external_ai_candidate_answer,
)
from .workbench_external_source_stale_state import (
    EXTERNAL_SOURCE_STALE_MESSAGE,
    sync_external_source_stale_state_from_window,
)

__all__ = [
    "build_external_ai_candidate_exchange_box",
    "sync_external_ai_candidate_exchange_controls",
]


def build_external_ai_candidate_exchange_box(
    window: object,
    root_text_callback,
) -> QGroupBox:
    """Build optional outbound exchange controls for the current candidate family."""
    box = QGroupBox("External AI Candidate Exchange")
    layout = QVBoxLayout(box)
    description = QLabel(
        "Optional advanced/fallback review. Build a complete lineage-bound candidate "
        "ZIP for external AI. The default return route is a governed patch ZIP. "
        "Optional Import AI Answer validates lineage and creates a new candidate "
        "generation only; it never applies AI output to canonical source."
    )
    description.setWordWrap(True)
    layout.addWidget(description)

    row = QHBoxLayout()
    copy_button = QPushButton("Path Candidates to AI")
    import_button = QPushButton("Import AI Answer")
    folder_button = QPushButton("Refactoring Folder")
    path_button = QPushButton("Refactoring Folder Path")
    clean_button = QPushButton("Clean Refactoring Folder")
    for button in (
        copy_button,
        import_button,
        folder_button,
        path_button,
        clean_button,
    ):
        button.setEnabled(False)
        row.addWidget(button)
    row.addStretch(1)
    layout.addLayout(row)

    output = QPlainTextEdit()
    output.setReadOnly(True)
    output.setPlainText(
        "Prepare Completion Evidence first. The outbound ZIP will contain the complete "
        "candidate family plus bounded plan, analysis, Preview, AQR, completion-review, "
        "and lineage context."
    )
    layout.addWidget(output)

    window._large_file_refactor_workbench_ai_exchange_copy_button = copy_button
    window._large_file_refactor_workbench_ai_return_import_button = import_button
    window._large_file_refactor_workbench_ai_exchange_folder_button = folder_button
    window._large_file_refactor_workbench_ai_exchange_path_button = path_button
    window._large_file_refactor_workbench_ai_exchange_clean_button = clean_button
    window._large_file_refactor_workbench_ai_exchange_output = output
    window._large_file_refactor_workbench_ai_exchange_result = None
    window._large_file_refactor_workbench_ai_return_result = None
    window._large_file_refactor_workbench_ai_exchange_root_callback = root_text_callback

    copy_button.clicked.connect(lambda: _path_candidates_to_ai(window))
    import_button.clicked.connect(lambda: _import_ai_answer(window))
    folder_button.clicked.connect(lambda: _open_refactoring_folder(window))
    path_button.clicked.connect(lambda: _copy_refactoring_folder_path(window))
    clean_button.clicked.connect(lambda: _clean_refactoring_folder(window))
    return box


def sync_external_ai_candidate_exchange_controls(window: object) -> None:
    """Project current evidence and exchange-folder readiness onto the controls."""
    stale_state = sync_external_source_stale_state_from_window(window)
    completion = getattr(window, "_large_file_refactor_workbench_completion_evidence", None)
    aqr_context = getattr(window, "_large_file_refactor_workbench_aqr_context", None)
    aqr_outcome = getattr(window, "_large_file_refactor_workbench_advanced_quality_review", None)
    preview = getattr(window, "_large_file_refactor_workbench_real_preview", None)
    snapshot = getattr(window, "_large_file_refactor_workbench_plan_snapshot", None)
    copy_ready = all(
        (completion, aqr_context, aqr_outcome, preview, snapshot)
    ) and not stale_state.stale
    result = getattr(window, "_large_file_refactor_workbench_ai_exchange_result", None)
    exchange_root = Path(str(getattr(result, "exchange_root", "") or ""))
    folder_ready = bool(result and exchange_root.is_dir())
    import_blockers = ai_return_import_readiness_blockers(
        exchange_result=result,
        aqr_context=aqr_context,
    )
    import_ready = bool(
        result and not import_blockers and not stale_state.stale
    )
    _set_enabled(window, "_large_file_refactor_workbench_ai_exchange_copy_button", copy_ready)
    _set_enabled(window, "_large_file_refactor_workbench_ai_return_import_button", import_ready)
    _set_enabled(window, "_large_file_refactor_workbench_ai_exchange_folder_button", folder_ready)
    _set_enabled(window, "_large_file_refactor_workbench_ai_exchange_path_button", folder_ready)
    _set_enabled(window, "_large_file_refactor_workbench_ai_exchange_clean_button", folder_ready)


def _path_candidates_to_ai(window: object) -> None:
    output = getattr(window, "_large_file_refactor_workbench_ai_exchange_output", None)
    try:
        stale_state = sync_external_source_stale_state_from_window(window)
        if stale_state.stale:
            raise ValueError(
                "STALE_AFTER_EXTERNAL_SOURCE_MUTATION:"
                + EXTERNAL_SOURCE_STALE_MESSAGE
            )
        root_callback = window._large_file_refactor_workbench_ai_exchange_root_callback
        active_root = str(root_callback(window))
        result = create_external_ai_candidate_exchange(
            active_project_root=active_root,
            plan_snapshot=getattr(window, "_large_file_refactor_workbench_plan_snapshot", None),
            preview_result=getattr(window, "_large_file_refactor_workbench_real_preview", None),
            aqr_context=getattr(window, "_large_file_refactor_workbench_aqr_context", None),
            aqr_outcome=getattr(window, "_large_file_refactor_workbench_advanced_quality_review", None),
            completion_evidence=getattr(window, "_large_file_refactor_workbench_completion_evidence", None),
        )
        window._large_file_refactor_workbench_ai_exchange_result = result
        QApplication.clipboard().setText(result.workspace_root)
        if output is not None:
            output.setPlainText(_format_result(result))
    except Exception as error:
        if output is not None:
            output.setPlainText(
                "EXTERNAL AI CANDIDATE EXCHANGE BLOCKED\n\n"
                + type(error).__name__
                + ":"
                + str(error)
            )
    sync_external_ai_candidate_exchange_controls(window)


def _import_ai_answer(window: object) -> None:
    """Import optional structured text or ZIP as a new candidate generation only."""
    output = getattr(window, "_large_file_refactor_workbench_ai_exchange_output", None)
    stale_state = sync_external_source_stale_state_from_window(window)
    if stale_state.stale:
        if output is not None:
            output.setPlainText(
                "IMPORT AI ANSWER BLOCKED\n\n"
                + "STALE_AFTER_EXTERNAL_SOURCE_MUTATION\n"
                + EXTERNAL_SOURCE_STALE_MESSAGE
            )
        sync_external_ai_candidate_exchange_controls(window)
        return
    result = _required_result(window)
    start = result.workspace_root if Path(result.workspace_root).is_dir() else str(Path.cwd())
    mode, value = choose_external_ai_return_input(start_path=start)
    if not mode:
        return
    try:
        root_callback = window._large_file_refactor_workbench_ai_exchange_root_callback
        active_root = str(root_callback(window))
        context = getattr(window, "_large_file_refactor_workbench_aqr_context", None)
        identity = context.request.analysis_identity
        common = {
            "active_project_root": active_root,
            "exchange_result": result,
            "active_project_card_identity": identity.project_card_identity,
            "active_target_relative_path": identity.target_relative_path,
            "active_preview_hash": identity.preview_hash,
        }
        if mode == "text":
            imported = import_external_ai_candidate_answer_text(
                answer_text=value,
                **common,
            )
        elif mode == "zip":
            imported = import_external_ai_candidate_answer(
                answer_zip_path=value,
                **common,
            )
        else:
            raise ValueError("AI_RETURN_INPUT_MODE_INVALID:" + mode)
        window._large_file_refactor_workbench_ai_return_result = imported
        if output is not None:
            output.setPlainText(_format_return_result(imported))
    except Exception as error:
        if output is not None:
            output.setPlainText(
                "IMPORT AI ANSWER BLOCKED\n\n"
                + type(error).__name__
                + ":"
                + str(error)
            )
    sync_external_ai_candidate_exchange_controls(window)

def _open_refactoring_folder(window: object) -> None:
    result = _required_result(window)
    QDesktopServices.openUrl(QUrl.fromLocalFile(result.workspace_root))


def _copy_refactoring_folder_path(window: object) -> None:
    result = _required_result(window)
    QApplication.clipboard().setText(result.workspace_root)
    output = getattr(window, "_large_file_refactor_workbench_ai_exchange_output", None)
    if output is not None:
        output.setPlainText(
            "REFACTORING FOLDER PATH COPIED\n\n" + result.workspace_root
        )


def _clean_refactoring_folder(window: object) -> None:
    result = _required_result(window)
    answer = QMessageBox.question(
        None,
        "Clean Refactoring Folder",
        "Delete all EXCH folders, return generations, and outbound ZIPs created "
        "for this card/target workspace?\n\n" + result.workspace_root,
        QMessageBox.Yes | QMessageBox.No,
        QMessageBox.No,
    )
    if answer != QMessageBox.Yes:
        return
    root_callback = window._large_file_refactor_workbench_ai_exchange_root_callback
    removed = clean_external_ai_exchange_workspace(
        active_project_root=str(root_callback(window)),
        project_card_identity=result.candidate_identity.project_card_identity,
        target_relative_path=result.candidate_identity.target_relative_path,
    )
    window._large_file_refactor_workbench_ai_exchange_result = None
    window._large_file_refactor_workbench_ai_return_result = None
    output = getattr(window, "_large_file_refactor_workbench_ai_exchange_output", None)
    if output is not None:
        output.setPlainText(
            "REFACTORING WORKSPACE CLEANED\n\n"
            + result.workspace_root
            + "\n\nRemoved artifacts: "
            + str(len(removed))
        )
    sync_external_ai_candidate_exchange_controls(window)

def _required_result(window: object):
    result = getattr(window, "_large_file_refactor_workbench_ai_exchange_result", None)
    if result is None:
        raise ValueError("AI_EXCHANGE_ACTIVE_RESULT_MISSING")
    return result


def _format_result(result) -> str:
    return "\n".join(
        [
            "EXTERNAL AI CANDIDATE EXCHANGE READY",
            "",
            "exchange_id: " + result.exchange_id,
            "candidate_files: " + str(len(result.candidate_files)),
            "package_files: " + str(result.package_file_count),
            "candidate_set_hash: " + result.candidate_identity.candidate_set_hash,
            "exchange_identity_hash: " + result.exchange_identity.identity_hash,
            "zip_sha256: " + result.zip_sha256,
            "",
            "ZIP:",
            result.zip_path,
            "",
            "The ZIP was created and the containing workspace path was copied to the "
            "clipboard. The folder was not opened. EXTERNAL_AI_TASK.md inside the ZIP "
            "contains the complete governed patch-return and optional structured-text "
            "Import AI Answer instructions.",
        ]
    )


def _format_return_result(result) -> str:
    return "\n".join(
        [
            "AI ANSWER IMPORTED AS NEW CANDIDATE GENERATION",
            "",
            "exchange_id: " + result.exchange_id,
            "return_id: " + result.return_id,
            "candidate_files: " + str(len(result.candidate_files)),
            "return_candidate_set_hash: " + result.candidate_set_hash,
            "response_identity_hash: " + result.response_identity.identity_hash,
            "",
            "Project Support return generation:",
            result.return_root,
            "",
            "No canonical Project source was changed. Preview, transaction state, "
            "warning acknowledgment, and human authorization were not promoted.",
        ]
    )


def _set_enabled(window: object, attribute: str, enabled: bool) -> None:
    button = getattr(window, attribute, None)
    if button is not None:
        button.setEnabled(bool(enabled))
