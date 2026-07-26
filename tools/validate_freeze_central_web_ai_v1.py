# project-path: tools/validate_freeze_central_web_ai_v1.py
"""Validate Freeze Feature After Update over central Config Web AI."""

from __future__ import annotations

import argparse
import json
import os
import py_compile
import sys
import tempfile
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
FEATURE_ID = "freeze-central-web-ai-v1"
TOUCHED = [
    "kanda_reasoner_app/freeze_after_update_gui/__init__.py",
    "kanda_reasoner_app/freeze_after_update_gui/freeze_after_update_tab.py",
    "kanda_reasoner_app/freeze_after_update_gui/_freeze_formulary_contracts.py",
    "kanda_reasoner_app/freeze_after_update_gui/_freeze_formulary_ai_runtime.py",
    "kanda_reasoner_app/freeze_after_update_gui/_web_ai_formulary.py",
    "kanda_reasoner_app/freeze_after_update_gui/_local_freeze_dialog_runtime.py",
    "kanda_reasoner_app/freeze_after_update_gui/_local_freeze_dialog_widgets.py",
    "kanda_reasoner_app/freeze_after_update_gui/_ui_builder.py",
    "tools/validate_freeze_dialog_no_confirmation_close_v1.py",
    "tools/validate_freeze_central_web_ai_v1.py",
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def read(relative: str) -> str:
    path = PROJECT_ROOT / relative
    require(path.is_file(), "Missing file: " + relative)
    return path.read_text(encoding="utf-8")


def validate_static() -> None:
    for relative in TOUCHED:
        py_compile.compile(str(PROJECT_ROOT / relative), doraise=True)
        require(len(read(relative).splitlines()) <= 500, relative + " exceeds 500 lines")
    widgets = read("kanda_reasoner_app/freeze_after_update_gui/_local_freeze_dialog_widgets.py")
    runtime = read("kanda_reasoner_app/freeze_after_update_gui/_freeze_formulary_ai_runtime.py")
    authority = read("kanda_reasoner_app/freeze_after_update_gui/_local_freeze_dialog_runtime.py")
    web = read("kanda_reasoner_app/freeze_after_update_gui/_web_ai_formulary.py")
    contracts = read("kanda_reasoner_app/freeze_after_update_gui/_freeze_formulary_contracts.py")
    tab = read("kanda_reasoner_app/freeze_after_update_gui/freeze_after_update_tab.py")

    for token in (
        "freeze_formulary_mode_heuristic",
        "freeze_formulary_mode_local_ai",
        "freeze_formulary_mode_web_ai",
        "Open Config AI",
    ):
        require(token in widgets, "Missing mode-only control: " + token)
    for forbidden in ("QComboBox", "AI model:", "Refresh AI Models"):
        require(forbidden not in widgets, "Duplicated AI configuration remains: " + forbidden)
    print("FREEZE_MODE_ONLY_CONTROLS: PASS")
    print("FREEZE_NO_DUPLICATE_WEB_CONFIGURATION: PASS")

    require("application_web_ai_configuration" in runtime, "Central config not reused")
    require("request_open_configuration" in runtime, "Config tab shortcut missing")
    require("request_chat_completion" in web, "Canonical Web transport not reused")
    require('"additionalProperties": False' in web, "Strict schema is missing")
    require("range(2)" in web, "One bounded retry contract is missing")
    require('"data_collection": "deny"' in web, "OpenRouter privacy contract missing")
    print("FREEZE_USES_CENTRAL_WEB_CONFIGURATION: PASS")
    print("NO_DUPLICATE_FREEZE_WEB_TRANSPORT: PASS")
    print("STRICT_WEB_FREEZE_FORMULARY_PROVIDER: PASS")

    for token in (
        "active_project_id",
        "active_project_slug",
        "active_project_root_fingerprint",
        "active_project_support_root",
        "form_snapshot_hash",
        "configuration_revision",
        "privacy_approval_id",
        "operation_id",
    ):
        require(token in contracts, "Request identity missing: " + token)
    require("identity.form_snapshot_hash" in runtime, "Form stale guard missing")
    require("snapshot.revision == identity.configuration_revision" in runtime, "Config stale guard missing")
    require("Project Support:" in runtime and "Form SHA-256:" in runtime, "Exact approval details missing")
    require("threading.Thread" in runtime and "daemon=True" in runtime, "Provider work is not off GUI thread")
    print("FREEZE_COMPLETE_REQUEST_IDENTITY: PASS")
    print("FREEZE_EXACT_WEB_APPROVAL_REQUIRED: PASS")
    print("FREEZE_MCARD_STALE_RESULT_GUARD: PASS")
    print("FREEZE_MODEL_WORK_OFF_GUI_THREAD: PASS")

    require("preview_freeze_entry" in authority, "Preview authority moved out of human runtime")
    require("write_confirmed_freeze_entry" in authority, "Confirmed write authority missing")
    require("confirmation=True" in authority, "Explicit write confirmation missing")
    require("refresh_ai_compliance_context" in authority, "Startup refresh after write missing")
    require("write_confirmed_freeze_entry" not in runtime + web, "AI provider gained write authority")
    require("mark_latest_freeze_hint_used" not in runtime + web, "AI provider gained hint-consumption authority")
    require("FreezeLocalEntryRuntimeMixin" in tab, "Freeze tab does not delegate bounded runtime")
    print("FREEZE_DETERMINISTIC_PREVIEW_WRITE_AUTHORITY: PASS")
    print("FREEZE_AI_DRAFT_ONLY_AUTHORITY: PASS")
    print("TOUCHED_SOURCE_MODULES_MAX_500_LINES: PASS")


def sample_form() -> dict[str, str]:
    return {
        "feature_title": "Synthetic central Web AI freeze fixture",
        "primary_box": "kanda_reasoner_app/freeze_after_update_gui/_web_ai_formulary.py",
        "box_type": "Tool-owned Freeze formulary provider adapter",
        "validated_files": "kanda_reasoner_app/freeze_after_update_gui/_web_ai_formulary.py",
        "generated_files": "tools/validate_freeze_central_web_ai_v1.py",
        "protected_paths": "kanda_reasoner_app/freeze_after_update_gui",
        "do_not_regress_rules": "Preview remains read-only.\nConfirm and Write remains human.",
        "validation_evidence_summary": "VALIDATION OK: synthetic-fixture\nSTATUS: IN_SYNC",
        "known_warnings": "Synthetic fixture only.",
        "planned_next_step": "Run real Qt validation.",
        "notes": "No source write is performed by this fixture.",
    }


class Response:
    def __init__(self, payload: dict[str, Any]) -> None:
        self.raw = json.dumps(payload).encode("utf-8")

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return False

    def read(self, _limit: int = -1) -> bytes:
        return self.raw


def validate_runtime(root: Path) -> None:
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    from kanda_reasoner_app.freeze_after_update_gui._freeze_formulary_contracts import (
        build_freeze_formulary_identity,
        form_snapshot_hash,
    )
    from kanda_reasoner_app.freeze_after_update_gui._web_ai_formulary import (
        WebFreezeAIFormularyRunner,
    )

    baseline = sample_form()
    with tempfile.TemporaryDirectory(prefix="kanda_freeze_web_identity_") as temp:
        project = Path(temp) / "nested" / "fixture_project"
        project.mkdir(parents=True)
        identity, resolved = build_freeze_formulary_identity(
            project_root=project,
            generation=3,
            inputs=baseline,
            assistant_mode="web",
            approval_id="approval",
            gateway_id="openrouter",
            model_id="fixture/model",
            configuration_revision="revision",
        )
        require(identity.active_project_slug == "fixture_project", "Wrong Project slug")
        require(identity.active_project_support_root == str(resolved.active_project_support_root), "Wrong support root")
        require(identity.form_snapshot_hash == form_snapshot_hash(baseline), "Wrong form hash")
        require(identity.privacy_approval_id == "approval", "Approval identity lost")
    print("DYNAMIC_FREEZE_PROJECT_IDENTITY: PASS")
    print("NESTED_ACTIVE_PROJECT_ROOT_SUPPORTED: PASS")

    payload = {
        "id": "fixture-response",
        "model": "fixture/model",
        "choices": [{"message": {"content": json.dumps(baseline)}, "finish_reason": "stop"}],
        "usage": {},
    }
    request_seen: dict[str, Any] = {}

    def opener(request, timeout=None):
        require(timeout is not None, "Web timeout missing")
        body = json.loads(request.data.decode("utf-8"))
        request_seen.update(body)
        return Response(payload)

    runner = WebFreezeAIFormularyRunner(
        inputs=baseline,
        project_root=Path("/tmp/nested/fixture"),
        gateway_id="openrouter",
        model_id="fixture/model",
        api_key="session-key",
        request_id="fixture-request",
        opener=opener,
    )
    ok, content, model = runner.run()
    require(ok, content)
    require(model == "fixture/model", "Returned model lost")
    require(json.loads(content) == baseline, "Strict result changed baseline")
    require(request_seen["response_format"]["json_schema"]["strict"] is True, "Strict response_format missing")
    require(request_seen["provider"]["data_collection"] == "deny", "OpenRouter privacy option missing")
    print("STRICT_WEB_FREEZE_FORMULARY_RUNTIME: PASS")
    print("BOUNDED_SHARED_TRANSPORT_OPTIONS: PASS")


def validate_real_qt(root: Path) -> None:
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    if os.name == "nt" and Path("C:/Windows/Fonts").is_dir():
        os.environ.setdefault("QT_QPA_FONTDIR", "C:/Windows/Fonts")
    try:
        from PySide6.QtCore import QCoreApplication, QEvent
        from PySide6.QtWidgets import QApplication, QComboBox, QLabel, QPushButton, QRadioButton
    except ImportError as exc:
        raise AssertionError("PySide6 is required for real-widget validation") from exc
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    from kanda_reasoner_app.freeze_after_update_gui.freeze_after_update_tab import (
        FreezeAfterUpdateTab,
    )

    created_app = QApplication.instance() is None
    app = QApplication.instance() or QApplication([])
    with tempfile.TemporaryDirectory(prefix="kanda_freeze_central_qt_") as temp:
        project = Path(temp) / "nested" / "fixture_project"
        project.mkdir(parents=True)
        tab = FreezeAfterUpdateTab()
        tab.set_project_root(project)
        tab._open_local_freeze_entry_dialog()
        dialog = tab._local_freeze_dialog
        require(dialog is not None, "Freeze formulary dialog did not open")
        app.processEvents()
        heuristic = dialog.findChild(QRadioButton, "freeze_formulary_mode_heuristic")
        local = dialog.findChild(QRadioButton, "freeze_formulary_mode_local_ai")
        web = dialog.findChild(QRadioButton, "freeze_formulary_mode_web_ai")
        require(heuristic is not None and local is not None and web is not None, "Mode radios missing")
        require(heuristic.isChecked(), "Heuristic must remain default")
        require(not dialog.findChildren(QComboBox), "Freeze dialog still contains a model dropdown")
        web.setChecked(True)
        app.processEvents()
        summary = dialog.findChild(QLabel, "freeze_formulary_web_config_summary")
        require(summary is not None and "Web AI:" in summary.text(), "Central Web summary missing")
        opened: list[bool] = []
        tab._freeze_web_ai_configuration.open_configuration_requested.connect(lambda: opened.append(True))
        button = dialog.findChild(QPushButton, "freeze_formulary_open_config_web_ai")
        require(button is not None, "Open Config Web AI button missing")
        button.click()
        app.processEvents()
        require(opened, "Config Web AI request signal was not emitted")
        dialog.close()
        tab.close()
        tab.deleteLater()
        QCoreApplication.sendPostedEvents(None, QEvent.Type.DeferredDelete)
        app.processEvents()
    if created_app:
        app.quit()
        QCoreApplication.sendPostedEvents(None, QEvent.Type.DeferredDelete)
        app.processEvents()
    print("REAL_FREEZE_CENTRAL_WEB_AI_WIDGET: PASS")
    print("FREEZE_QT_TEARDOWN_CLEAN: PASS")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--static-only", action="store_true")
    args = parser.parse_args()
    root = PROJECT_ROOT
    validate_static()
    validate_runtime(root)
    if not args.static_only:
        validate_real_qt(root)
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
