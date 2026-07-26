"""Validate real PySide controls for optional external AI return import."""

from __future__ import annotations

import os
from pathlib import Path
import sys
from types import SimpleNamespace

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")


def _configure_offscreen_font_directory() -> str:
    if os.name != "nt":
        return "NOT_REQUIRED_NON_WINDOWS"
    configured = os.environ.get("QT_QPA_FONTDIR", "").strip()
    if configured:
        path = Path(configured)
        if not path.is_dir():
            raise RuntimeError("QT_QPA_FONTDIR_DOES_NOT_EXIST:" + str(path))
        return str(path)
    candidates = []
    for name in ("WINDIR", "SystemRoot"):
        value = os.environ.get(name, "").strip()
        if value:
            candidate = Path(value) / "Fonts"
            if candidate not in candidates:
                candidates.append(candidate)
    for candidate in candidates:
        if candidate.is_dir():
            os.environ["QT_QPA_FONTDIR"] = str(candidate)
            return str(candidate)
    raise RuntimeError(
        "QT_OFFSCREEN_FONT_DIRECTORY_NOT_FOUND:"
        + "|".join(str(item) for item in candidates)
    )


FONTDIR = _configure_offscreen_font_directory()
print("AI_RETURN_QT_OFFSCREEN_FONTDIR_READY: PASS")

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from PySide6.QtWidgets import QApplication, QCheckBox, QMainWindow  # noqa: E402

from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.external_ai_candidate_exchange_gui import (  # noqa: E402
    build_external_ai_candidate_exchange_box,
    sync_external_ai_candidate_exchange_controls,
)

FEATURE_ID = "external-ai-return-import-real-widget-v1"


def main() -> None:
    app = QApplication.instance() or QApplication([])
    window = QMainWindow()
    box = build_external_ai_candidate_exchange_box(
        window,
        lambda _window: str(PROJECT_ROOT),
    )
    box.show()
    app.processEvents()

    import_button = window._large_file_refactor_workbench_ai_return_import_button
    assert import_button.text() == "Import AI Answer"
    assert not import_button.isEnabled()
    print("AI_RETURN_REAL_WIDGET_INITIAL_FAIL_CLOSED: PASS")

    human_review = QCheckBox()
    warning_ack = QCheckBox()
    transaction_confirm = QCheckBox()
    window._large_file_refactor_workbench_semantic_review_check = human_review
    window._large_file_refactor_workbench_warning_ack_check = warning_ack
    window._large_file_refactor_workbench_transaction_confirm_check = transaction_confirm

    identity = SimpleNamespace(
        project_card_identity="widget-card-001",
        target_relative_path="pkg/module.py",
        preview_hash="widget-preview-hash-001",
    )
    window._large_file_refactor_workbench_aqr_context = SimpleNamespace(
        request=SimpleNamespace(analysis_identity=identity)
    )
    window._large_file_refactor_workbench_ai_exchange_result = SimpleNamespace(
        exchange_root=str(PROJECT_ROOT),
        candidate_files=("helper.py", "module.py"),
        exchange_identity=SimpleNamespace(
            project_card_identity=identity.project_card_identity,
            target_relative_path=identity.target_relative_path,
            source_preview_hash=identity.preview_hash,
        ),
    )
    sync_external_ai_candidate_exchange_controls(window)
    app.processEvents()
    assert import_button.isEnabled()
    print("AI_RETURN_REAL_WIDGET_IMPORT_READY_AFTER_CURRENT_EXCHANGE: PASS")

    window._large_file_refactor_workbench_aqr_context = SimpleNamespace(
        request=SimpleNamespace(
            analysis_identity=SimpleNamespace(
                project_card_identity=identity.project_card_identity,
                target_relative_path=identity.target_relative_path,
                preview_hash="different-preview-hash",
            )
        )
    )
    sync_external_ai_candidate_exchange_controls(window)
    app.processEvents()
    assert not import_button.isEnabled()
    print("AI_RETURN_REAL_WIDGET_STALE_PREVIEW_FAILS_CLOSED: PASS")

    assert not human_review.isChecked()
    assert not warning_ack.isChecked()
    assert not transaction_confirm.isChecked()
    print("AI_RETURN_REAL_WIDGET_HUMAN_GATES_UNCHANGED: PASS")

    box.close()
    app.processEvents()
    print("EXTERNAL_AI_RETURN_IMPORT_REAL_WIDGET: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")


if __name__ == "__main__":
    main()
