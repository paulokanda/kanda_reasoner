#!/usr/bin/env python3
# project-path: tools/validate_audit_project_central_web_ai_v1.py
"""Validate Audit Project modes over the central Config Web AI owner."""

from __future__ import annotations

import argparse
import ast
import json
import os
import py_compile
import sys
import tempfile
from pathlib import Path

FEATURE_ID = "audit-project-central-web-ai-v1"
MAX_LINES = 500
TOUCHED = (
    "kanda_reasoner_app/manage_architecture/ai_review/models.py",
    "kanda_reasoner_app/manage_architecture/ai_review/heuristic.py",
    "kanda_reasoner_app/manage_architecture/ai_review/contracts.py",
    "kanda_reasoner_app/manage_architecture/ai_review/web_adapter.py",
    "kanda_reasoner_app/manage_architecture/ai_review/controller.py",
    "kanda_reasoner_app/manage_architecture/ai_review/adapter.py",
    "kanda_reasoner_app/manage_architecture/ai_review/qt_worker.py",
    "kanda_reasoner_app/manage_architecture/ai_review/gui_integration.py",
    "kanda_reasoner_app/manage_architecture/ai_review/running_indicator.py",
    "kanda_reasoner_app/manage_architecture/architecture_audit_actions_gui.py",
    "tools/validate_architecture_review_warning_model_resolver_v1.py",
    "tools/validate_audit_project_central_web_ai_v1.py",
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def read(root: Path, relative: str) -> str:
    path = root / relative
    require(path.is_file(), "Missing expected file: " + relative)
    return path.read_text(encoding="utf-8")


def validate_static(root: Path) -> None:
    for relative in TOUCHED:
        path = root / relative
        py_compile.compile(str(path), doraise=True)
        text = read(root, relative)
        ast.parse(text, filename=relative)
        require(len(text.splitlines()) <= MAX_LINES, relative + " exceeds 500 lines")
    print("CHANGED_PYTHON_COMPILE: PASS")
    print("TOUCHED_SOURCE_MODULES_MAX_500_LINES: PASS")

    gui = read(root, "kanda_reasoner_app/manage_architecture/ai_review/gui_integration.py")
    controller = read(root, "kanda_reasoner_app/manage_architecture/ai_review/controller.py")
    worker = read(root, "kanda_reasoner_app/manage_architecture/ai_review/qt_worker.py")
    contracts = read(root, "kanda_reasoner_app/manage_architecture/ai_review/contracts.py")
    web = read(root, "kanda_reasoner_app/manage_architecture/ai_review/web_adapter.py")
    actions = read(root, "kanda_reasoner_app/manage_architecture/architecture_audit_actions_gui.py")

    for fragment in ('QRadioButton("Heuristic"', 'QRadioButton("Local AI"', 'QRadioButton("Web AI"'):
        require(fragment in gui, "Missing Audit Project mode: " + fragment)
    for forbidden in (
        "QComboBox",
        "QSettings",
        "Refresh AI Models",
        "SETTINGS_KEY_SELECTED_MODEL",
    ):
        require(forbidden not in gui, "Audit Project repeats removed model configuration: " + forbidden)
    require("application_web_ai_configuration" in gui, "Central configuration is not reused")
    require("_ai_review_refresh_models_button = None" in gui, "Legacy refresh control remains")
    require('model_selection = ""' in actions, "Warning resolver does not auto-resolve Local AI")
    print("AUDIT_PROJECT_MODE_ONLY_CONTROLS: PASS")
    print("AUDIT_PROJECT_NO_DUPLICATE_WEB_CONFIGURATION: PASS")
    print("AUDIT_PROJECT_USES_CENTRAL_WEB_CONFIGURATION: PASS")
    print("AUDIT_PROJECT_HEADER_MODEL_SELECTOR_REMOVED: PASS")

    require("HEURISTIC_MODE" in controller and "WEB_AI_MODE" in controller, "Mode dispatch missing")
    require("review_audit_with_heuristic" in controller, "Heuristic dispatch missing")
    require("Tab1WebAIReviewAdapter" in controller, "Web dispatch missing")
    require("QThread" not in gui or "moveToThread(thread)" in gui, "Model work is not off GUI thread")
    require("worker.moveToThread(thread)" in gui, "Review worker is not moved to QThread")
    require("provider_mode=self._provider_mode" in worker, "Worker mode dispatch missing")
    print("AUDIT_PROJECT_HEURISTIC_LOCAL_WEB_DISPATCH: PASS")
    print("AUDIT_PROJECT_MODEL_WORK_OFF_GUI_THREAD: PASS")

    require("request_chat_completion" in web, "Canonical Web provider runtime is not reused")
    require('"response_format"' in web and '"json_schema"' in web, "Strict JSON Schema missing")
    require('"allow_fallbacks": False' in web, "OpenRouter fallback denial missing")
    require('"data_collection": "deny"' in web, "OpenRouter data collection denial missing")
    require("for _attempt in range(2)" in web, "Bounded one-retry contract missing")
    require("additionalProperties\": False" in web, "Strict schema additionalProperties gate missing")
    print("STRICT_WEB_AUDIT_PROJECT_PROVIDER: PASS")
    print("NO_DUPLICATE_AUDIT_PROJECT_WEB_TRANSPORT: PASS")

    for field in (
        "active_project_id",
        "active_project_root_fingerprint",
        "active_project_support_root",
        "audit_snapshot_hash",
        "configuration_revision",
        "privacy_approval_id",
    ):
        require(field in contracts, "Audit request identity missing: " + field)
    require("Approve Audit Project Web AI Review" in gui, "Exact Web approval missing")
    require("_identity_is_current" in gui, "Stale-result guard missing")
    require("snapshot.revision == identity.configuration_revision" in gui, "Config stale gate missing")
    require("project.active_project_id != identity.active_project_id" in gui or "project.active_project_id\n        != identity.active_project_id" in gui, "Project stale gate missing")
    require("write code" in web and "Freeze readiness" in web, "Advisory authority prompt missing")
    print("AUDIT_PROJECT_EXACT_WEB_APPROVAL_REQUIRED: PASS")
    print("AUDIT_PROJECT_COMPLETE_REQUEST_IDENTITY: PASS")
    print("AUDIT_PROJECT_MCARD_STALE_RESULT_GUARD: PASS")
    print("AUDIT_PROJECT_READ_ONLY_AUTHORITY: PASS")


def _web_payload() -> dict[str, object]:
    content = {
        "advisory_summary": "One deterministic warning requires inspection.",
        "highest_risks": [
            {
                "severity": "WARNING",
                "finding": "Synthetic warning remains.",
                "evidence": "WARNING fixture",
                "suggested_file": "kanda_reasoner_app/fixture.py",
            }
        ],
        "suggested_next_files": ["kanda_reasoner_app/fixture.py"],
        "safest_next_actions": ["Inspect the deterministic warning and rerun validation."],
        "deterministic_authority": "Deterministic Project Audit decides pass/fail and write eligibility.",
    }
    return {
        "id": "fixture-response",
        "model": "fixture/model",
        "choices": [{"message": {"content": json.dumps(content)}, "finish_reason": "stop"}],
        "usage": {},
    }


class _Response:
    def __init__(self, payload: dict[str, object]) -> None:
        self._raw = json.dumps(payload).encode("utf-8")

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return False

    def read(self, _limit: int = -1) -> bytes:
        return self._raw


def validate_runtime(root: Path) -> None:
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    from kanda_reasoner_app.manage_architecture.ai_review.controller import (
        build_tab1_ai_review_request,
        run_tab1_ai_review,
    )
    from kanda_reasoner_app.manage_architecture.ai_review.models import (
        HEURISTIC_MODE,
        WEB_AI_MODE,
    )
    from kanda_reasoner_app.manage_architecture.ai_review.web_adapter import (
        Tab1WebAIReviewAdapter,
    )

    audit = "WARNING fixture in kanda_reasoner_app/fixture.py\nErrors: 0"
    heuristic = run_tab1_ai_review(
        build_tab1_ai_review_request(
            audit_text=audit,
            project_root="/tmp/nested/fixture",
            provider_mode=HEURISTIC_MODE,
            request_id="heuristic-request",
        )
    )
    require(heuristic.success, heuristic.error_message)
    require("deterministic Project Audit" in heuristic.text, "Heuristic authority banner missing")

    def opener(_request, timeout=None):
        require(timeout is not None, "Web timeout missing")
        return _Response(_web_payload())

    web = Tab1WebAIReviewAdapter(opener=opener).review(
        build_tab1_ai_review_request(
            audit_text=audit,
            project_root="/tmp/nested/fixture",
            provider_mode=WEB_AI_MODE,
            gateway_id="openrouter",
            model_name="fixture/model",
            api_key="session-key",
            request_id="web-request",
        )
    )
    require(web.success, web.error_message)
    require(web.request_id == "web-request", "Web request identity was lost")
    require("Synthetic warning remains" in web.text, "Strict Web result was not formatted")
    print("AUDIT_PROJECT_HEURISTIC_RUNTIME: PASS")
    print("STRICT_WEB_AUDIT_PROJECT_RUNTIME: PASS")


def validate_real_qt(root: Path) -> None:
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    if os.name == "nt" and Path("C:/Windows/Fonts").is_dir():
        os.environ.setdefault("QT_QPA_FONTDIR", "C:/Windows/Fonts")
    from unittest.mock import patch

    try:
        from PySide6.QtCore import QCoreApplication, QEvent
        from PySide6.QtWidgets import QApplication, QHBoxLayout, QMessageBox, QWidget
    except ImportError as exc:
        raise AssertionError("PySide6 is required for real-widget validation") from exc
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))

    from kanda_reasoner_app.manage_architecture.ai_review.contracts import (
        build_audit_review_identity,
    )
    from kanda_reasoner_app.manage_architecture.ai_review.gui_integration import (
        _identity_is_current,
        _request_web_approval,
    )
    from kanda_reasoner_app.manage_architecture.manage_architecture_gui import (
        ArchitectureManagerWindow,
    )
    from kanda_reasoner_app.web_ai_configuration import application_web_ai_configuration
    from kanda_reasoner_app.web_ai_provider_contracts import ModelDescriptor

    app = QApplication.instance() or QApplication([])
    temp = tempfile.TemporaryDirectory()
    window = ArchitectureManagerWindow()
    host = QWidget()
    host_layout = QHBoxLayout(host)
    try:
        project = Path(temp.name) / "nested" / "fixture_project"
        project.mkdir(parents=True)
        window._root_path_edit.setText(str(project))
        window._output.setPlainText("WARNING fixture\nErrors: 0")
        require(window._ai_review_heuristic_radio.isChecked(), "Heuristic default missing")
        require(window._ai_review_local_radio.text() == "Local AI", "Local AI mode missing")
        require(window._ai_review_web_radio.text() == "Web AI", "Web AI mode missing")
        require(window._ai_review_refresh_models_button is None, "Legacy refresh control remains")
        window.move_ai_review_controls_to_layout(host_layout)
        require(host_layout.indexOf(window._ai_review_mode_host) >= 0, "Mode controls did not relocate")
        require(host_layout.indexOf(window._ai_review_button) >= 0, "Review action did not relocate")

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
        window._ai_review_web_radio.setChecked(True)
        app.processEvents()
        require(window._ai_review_button.text() == "Review with Web AI", "Web mode action missing")

        audit_text = window._output.toPlainText().strip()
        with patch.object(QMessageBox, "question", return_value=QMessageBox.StandardButton.Yes):
            approval = _request_web_approval(window, audit_text)
        require(bool(approval), "Exact Web approval was not created")
        identity, _project = build_audit_review_identity(
            window,
            generation=1,
            audit_text=audit_text,
            provider_mode="web",
            approval_id=approval,
        )
        window._ai_review_generation = 1
        require(_identity_is_current(window, identity), "Fresh audit identity rejected")
        controller.set_selected_model_id("")
        require(not _identity_is_current(window, identity), "Config change did not stale request")
        controller._selected_model_id = model.model_id
        controller._touch()
        changed = Path(temp.name) / "other_project"
        changed.mkdir()
        window._root_path_edit.setText(str(changed))
        require(not _identity_is_current(window, identity), "Project change did not stale request")
        print("AUDIT_PROJECT_EXACT_WEB_APPROVAL_RUNTIME: PASS")
        print("AUDIT_PROJECT_PROJECT_AND_CONFIG_STALE_GUARD: PASS")
        print("REAL_AUDIT_PROJECT_CENTRAL_WEB_AI_WIDGET: PASS")
    finally:
        indicator = getattr(window, "_tab1_activity_indicator", None)
        if indicator is not None:
            indicator.set_idle()
        thread = getattr(window, "_ai_review_thread", None)
        if thread is not None and thread.isRunning():
            thread.requestInterruption()
            thread.quit()
            thread.wait(1000)
        host.close()
        host.deleteLater()
        window.close()
        window.deleteLater()
        temp.cleanup()
        app.processEvents()
        QCoreApplication.sendPostedEvents(None, QEvent.Type.DeferredDelete)
        app.processEvents()
    print("AUDIT_PROJECT_QT_TEARDOWN_CLEAN: PASS")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--static-only", action="store_true")
    args = parser.parse_args()
    root = args.root.expanduser().resolve(strict=True)
    validate_static(root)
    validate_runtime(root)
    if not args.static_only:
        validate_real_qt(root)
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
