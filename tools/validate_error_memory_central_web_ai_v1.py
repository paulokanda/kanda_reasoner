#!/usr/bin/env python3
# project-path: tools/validate_error_memory_central_web_ai_v1.py
"""Validate Error Memory modes over the central Config Web AI owner."""

from __future__ import annotations

import argparse
import ast
import json
import os
import py_compile
import sys
import tempfile
from pathlib import Path
from typing import Any

FEATURE_ID = "error-memory-central-web-ai-v1"
TOUCHED = (
    "kanda_reasoner_app/error_memory_gui/_ai_mode_runtime.py",
    "kanda_reasoner_app/error_memory_gui/_ai_correction_contracts.py",
    "kanda_reasoner_app/error_memory_gui/_web_ai_corrector_service.py",
    "kanda_reasoner_app/error_memory_gui/_ai_correction_worker.py",
    "kanda_reasoner_app/error_memory_gui/_ai_correction_action.py",
    "kanda_reasoner_app/error_memory_gui/error_memory_tab.py",
    "kanda_reasoner_app/reasoner_tools_gui_shell/lazy_tabs.py",
    "tools/validate_error_memory_correct_with_ai_button_v7.py",
    "tools/validate_error_memory_header_ai_widgets_v1.py",
    "tools/validate_error_memory_central_web_ai_v1.py",
)
MAX_LINES = 500


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def read(root: Path, relative: str) -> str:
    path = root / relative
    require(path.is_file(), "Missing expected file: " + relative)
    return path.read_text(encoding="utf-8")


def validate_compile_and_size(root: Path) -> None:
    for relative in TOUCHED:
        path = root / relative
        py_compile.compile(str(path), doraise=True)
        text = read(root, relative)
        ast.parse(text, filename=str(path))
        require(
            len(text.splitlines()) <= MAX_LINES,
            relative + " exceeds 500 physical lines",
        )
    print("CHANGED_PYTHON_COMPILE: PASS")
    print("TOUCHED_SOURCE_MODULES_MAX_500_LINES: PASS")


def validate_static(root: Path) -> None:
    validate_compile_and_size(root)
    tab = read(root, "kanda_reasoner_app/error_memory_gui/error_memory_tab.py")
    mode = read(root, "kanda_reasoner_app/error_memory_gui/_ai_mode_runtime.py")
    action = read(root, "kanda_reasoner_app/error_memory_gui/_ai_correction_action.py")
    worker = read(root, "kanda_reasoner_app/error_memory_gui/_ai_correction_worker.py")
    service = read(root, "kanda_reasoner_app/error_memory_gui/_web_ai_corrector_service.py")
    contracts = read(root, "kanda_reasoner_app/error_memory_gui/_ai_correction_contracts.py")
    lazy = read(root, "kanda_reasoner_app/reasoner_tools_gui_shell/lazy_tabs.py")

    for label in ('QRadioButton("Heuristic"', 'QRadioButton("Local AI"', 'QRadioButton("Web AI"'):
        require(label in mode, "Missing mode choice: " + label)
    for forbidden in ("gateway_combo", "api_key_edit", "model_combo", "refresh_models_button"):
        require(forbidden not in tab, "Error Memory duplicates central config: " + forbidden)
    require("application_web_ai_configuration" in mode, "Central configuration owner is not reused")
    require("build_mode_group(self)" in tab, "Mode selector is not visible in Error Memory")
    print("ERROR_MEMORY_MODE_ONLY_CONTROLS: PASS")
    print("ERROR_MEMORY_NO_DUPLICATE_WEB_CONFIGURATION: PASS")
    print("ERROR_MEMORY_USES_CENTRAL_WEB_CONFIGURATION: PASS")

    header_sources = lazy.split("_LEGACY_HEADER_AI_GROUP_SOURCES = {", 1)[1].split("}", 1)[0]
    require("_ERROR_MEMORY_GUI_SOURCE" not in header_sources, "Repeated header AI configuration remains")
    print("ERROR_MEMORY_HEADER_AI_CONFIG_REMOVED: PASS")

    require("request_chat_completion" in service, "Canonical Web transport is not reused")
    require('"response_format"' in service and '"json_schema"' in service, "Strict JSON Schema missing")
    require('"allow_fallbacks": False' in service, "OpenRouter fallback denial missing")
    require('"data_collection": "deny"' in service, "OpenRouter data-collection denial missing")
    require("for attempt in range(2)" in service, "Bounded one-retry contract missing")
    require("parse_one_lesson_block" in service, "Semantic Error Memory validator missing")
    print("STRICT_WEB_ERROR_MEMORY_PROVIDER: PASS")
    print("NO_DUPLICATE_ERROR_MEMORY_WEB_TRANSPORT: PASS")

    require("QThread" in action and "worker.moveToThread(thread)" in action, "AI work is not off GUI thread")
    require('self._provider_mode == "web"' in worker, "Worker Web dispatch missing")
    require("correct_error_memory_lesson_with_local_ai" in worker, "Local AI path missing")
    require("correct_error_memory_lesson_with_web_ai" in worker, "Web AI path missing")
    print("ERROR_MEMORY_AI_OFF_GUI_THREAD: PASS")
    print("ERROR_MEMORY_HEURISTIC_LOCAL_WEB_DISPATCH: PASS")

    require("Approve Error Memory Web AI Request" in action, "Per-request cloud approval missing")
    require("privacy_approval_id" in contracts, "Approval is absent from request identity")
    require("configuration_revision" in contracts, "Central config revision is absent from identity")
    require("active_project_root_fingerprint" in contracts, "Project root fingerprint missing")
    require("active_project_support_root" in contracts, "Project Support identity missing")
    require("input_snapshot_hash" in contracts, "Input snapshot hash missing")
    require("_identity_is_current" in action, "Complete stale-result gate missing")
    require("snapshot.revision == identity.configuration_revision" in action, "Config-change rejection missing")
    require("project.active_project_id != identity.active_project_id" in action, "Project-change rejection missing")
    print("ERROR_MEMORY_CLOUD_APPROVAL_REQUIRED: PASS")
    print("ERROR_MEMORY_COMPLETE_REQUEST_IDENTITY: PASS")
    print("ERROR_MEMORY_PROJECT_SWITCH_STALE_GUARD: PASS")
    print("ERROR_MEMORY_CONFIG_CHANGE_STALE_GUARD: PASS")

    require("loaded as a preview only" in action, "Preview-only disclosure missing")
    require("did not save, delete, activate, supersede, or memorize any lesson" in action, "Preview boundary missing")
    for forbidden in (
        "save_corrected_selected_draft",
        "consume_duplicate_correction_candidate",
        "memorize_error_from_text_window",
    ):
        require(forbidden not in action, "Correction action crosses persistence boundary: " + forbidden)
    print("ERROR_MEMORY_PREVIEW_ONLY: PASS")


def _sample_lesson() -> dict[str, Any]:
    return {
        "schema_version": "1.0",
        "project_slug": "fixture",
        "lesson_id": "lesson-error-memory-web-fixture-v1",
        "status": "draft",
        "superseded_by": "",
        "operation_phase": "validation",
        "created_at_utc": "2026-07-21T00:00:00Z",
        "updated_at_utc": "2026-07-21T00:00:00Z",
        "source_patch_zip": "fixture.zip",
        "raw_error_text": "Synthetic validation error.",
        "raw_error_snapshot_scrubbed": "Synthetic scrubbed chronology.",
        "symptom": "Synthetic symptom.",
        "root_cause": "Synthetic root cause.",
        "wrong_assumption": "Synthetic wrong assumption.",
        "correct_fix": "Synthetic correct fix.",
        "do_not_repeat_rule": "Synthetic prevention rule.",
        "long_term_prevention": "Synthetic long-term prevention.",
        "redaction": {
            "applied": True,
            "export_safe": True,
            "rules": ["No secrets included."],
        },
        "exception": {
            "type": "SyntheticError",
            "phase": "validation",
            "relative_file_path": "tools/fixture.py",
            "function_or_test_name": "fixture",
            "message_normalized": "synthetic error",
            "stacktrace_scrubbed": "No traceback.",
        },
        "fingerprint": {
            "strategy": "v1_structural_conservative",
            "components": ["SyntheticError", "fixture"],
            "fingerprint_hash": "error_memory_web_fixture_v1",
        },
        "prevention_triggers": ["synthetic trigger"],
        "regression_check": {
            "type": "validation_command",
            "command": "python tools/validate_fixture.py",
            "expected_marker": "VALIDATION OK: fixture",
            "required_before_freeze": True,
        },
        "validation_command_summary": "Run the synthetic validator.",
        "validation_evidence": ["Observed synthetic validation evidence."],
        "install_command_summary": "Install the synthetic fixture.",
        "notes": "Synthetic fixture only.",
    }


class _Response:
    def __init__(self, payload: dict[str, Any]) -> None:
        self._raw = json.dumps(payload).encode("utf-8")

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return False

    def read(self, _limit: int = -1) -> bytes:
        return self._raw


def validate_strict_service(root: Path) -> None:
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    from kanda_reasoner_app.error_memory_gui._web_ai_corrector_service import (
        correct_error_memory_lesson_with_web_ai,
    )

    lesson = _sample_lesson()
    payload = {
        "id": "fixture-response",
        "model": "fixture/model",
        "choices": [
            {
                "message": {"content": json.dumps(lesson)},
                "finish_reason": "stop",
            }
        ],
        "usage": {},
    }

    def opener(_request, timeout=None):
        require(timeout is not None, "Timeout was not supplied")
        return _Response(payload)

    with tempfile.TemporaryDirectory() as temp:
        project = Path(temp) / "nested" / "fixture_project"
        project.mkdir(parents=True)
        result = correct_error_memory_lesson_with_web_ai(
            intake_text="Synthetic validation error.",
            editor_text="",
            project_root=project,
            gateway_id="openrouter",
            model_id="fixture/model",
            api_key="session-key",
            request_id="fixture-request",
            opener=opener,
        )
    require(result.ok, result.message)
    require(result.lesson_block is not None, "Strict service returned no lesson block")
    require(
        result.lesson_block.lesson.get("lesson_id") == lesson["lesson_id"],
        "Strict service altered lesson identity",
    )
    print("STRICT_WEB_ERROR_MEMORY_RUNTIME: PASS")
    print("NESTED_ACTIVE_PROJECT_ROOT_SUPPORTED: PASS")


def validate_real_qt(root: Path) -> None:
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    if os.name == "nt" and Path("C:/Windows/Fonts").is_dir():
        os.environ.setdefault("QT_QPA_FONTDIR", "C:/Windows/Fonts")
    try:
        from PySide6.QtCore import QCoreApplication, QEvent
        from PySide6.QtWidgets import QApplication, QMessageBox
    except ImportError as exc:
        raise AssertionError("PySide6 is required for real-widget validation") from exc

    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    from unittest.mock import patch

    from kanda_reasoner_app.error_memory_gui import _ai_mode_runtime
    from kanda_reasoner_app.error_memory_gui._ai_correction_action import (
        _identity_is_current,
        _request_web_approval,
    )
    from kanda_reasoner_app.error_memory_gui._ai_correction_contracts import (
        build_correction_identity,
    )
    from kanda_reasoner_app.error_memory_gui.error_memory_tab import ErrorMemoryTab
    from kanda_reasoner_app.reasoner_tools_gui_shell.lazy_tabs import LazyToolTab
    from kanda_reasoner_app.reasoner_tools_gui_shell.tool_specs import TOOLS
    from kanda_reasoner_app.web_ai_configuration import application_web_ai_configuration
    from kanda_reasoner_app.web_ai_provider_contracts import ModelDescriptor

    app = QApplication.instance() or QApplication([])
    tab = ErrorMemoryTab()
    lazy = None
    temp = tempfile.TemporaryDirectory()
    try:
        require(tab._error_memory_heuristic_radio.isChecked(), "Heuristic default missing")
        require(tab._error_memory_local_ai_radio.text() == "Local AI", "Local AI radio missing")
        require(tab._error_memory_web_ai_radio.text() == "Web AI", "Web AI radio missing")
        require(not tab.heuristic_correction_button.isVisible(), "Legacy heuristic action is duplicated")

        spec = next(spec for spec in TOOLS if spec.tab_id == "error_memory")
        lazy = LazyToolTab(spec, lambda *_args: None)
        require(lazy.tab_header_template.ai_model_combo is None, "Error Memory header model combo remains")
        require(lazy.tab_header_template.refresh_ai_models_button is None, "Error Memory header refresh remains")

        project = Path(temp.name) / "nested" / "fixture_project"
        project.mkdir(parents=True)
        tab._project_root = project
        controller = application_web_ai_configuration()
        model = ModelDescriptor(
            gateway_id="openrouter",
            model_id="fixture/model",
            display_name="Fixture Model",
            free_status=True,
            supported_parameters=("response_format",),
            catalog_timestamp="fixture",
        )
        controller._gateway_id = "openrouter"
        controller._all_models = [model]
        controller._selected_model_id = model.model_id
        controller.set_api_key("session-key", source="validator session")
        controller._touch()
        tab._error_memory_web_ai_radio.setChecked(True)
        app.processEvents()
        require(
            _ai_mode_runtime.central_configuration(tab) is controller,
            "Error Memory does not share the application controller",
        )
        require(tab.correct_with_ai_button.text() == "Correct with Web AI", "Web mode label missing")

        tab.raw_error_edit.setPlainText("Synthetic validation error.")
        tab.received_preview_edit.setPlainText("")
        with patch.object(
            QMessageBox,
            "question",
            return_value=QMessageBox.StandardButton.Yes,
        ):
            approval = _request_web_approval(
                tab,
                tab,
                intake_text=tab.raw_error_edit.toPlainText().strip(),
                editor_text="",
            )
        require(bool(approval), "Exact Web request approval was not created")
        identity, _project = build_correction_identity(
            tab,
            generation=1,
            intake_text=tab.raw_error_edit.toPlainText().strip(),
            editor_text="",
            approval_id=approval,
        )
        job = {
            "identity": identity,
            "intake_text": tab.raw_error_edit.toPlainText().strip(),
            "editor_text": "",
            "local_model_text": "",
            "current_local_model": "",
        }
        require(_identity_is_current(tab, job), "Fresh Error Memory identity rejected")
        controller.set_selected_model_id("")
        require(not _identity_is_current(tab, job), "Central config change did not stale the request")
        controller._selected_model_id = model.model_id
        controller._touch()
        changed_project = Path(temp.name) / "other_project"
        changed_project.mkdir()
        tab._project_root = changed_project
        require(not _identity_is_current(tab, job), "Project change did not stale the request")
        print("SHARED_CONFIGURATION_PROPAGATES_TO_ERROR_MEMORY: PASS")
        print("ERROR_MEMORY_EXACT_WEB_APPROVAL_RUNTIME: PASS")
        print("ERROR_MEMORY_MCARD_STALE_RESULT_GUARD: PASS")
        print("REAL_ERROR_MEMORY_CENTRAL_WEB_AI_WIDGET: PASS")
    finally:
        timer = getattr(tab, "_pending_intake_live_refresh_timer", None)
        if timer is not None:
            timer.stop()
        if lazy is not None:
            lazy.close()
            lazy.deleteLater()
        tab.close()
        tab.deleteLater()
        temp.cleanup()
        app.processEvents()
        QCoreApplication.sendPostedEvents(None, QEvent.Type.DeferredDelete)
        app.processEvents()
    print("ERROR_MEMORY_QT_TEARDOWN_CLEAN: PASS")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--static-only", action="store_true")
    args = parser.parse_args()
    root = args.root.expanduser().resolve(strict=True)
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    validate_static(root)
    validate_strict_service(root)
    if not args.static_only:
        validate_real_qt(root)
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
