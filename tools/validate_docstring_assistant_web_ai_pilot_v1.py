# project-path: tools/validate_docstring_assistant_web_ai_pilot_v1.py
"""Validate the optional Web AI pilot for KANDA Docstring Assistant."""

from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from pathlib import Path
from types import SimpleNamespace

FEATURE_ID = "docstring-assistant-central-web-ai-config-v1"


def require(condition: bool, message: str) -> None:
    """Raise one focused validation failure."""
    if not condition:
        raise AssertionError(message)


def read(root: Path, relative: str) -> str:
    """Return one UTF-8 source file."""
    return (root / relative).read_text(encoding="utf-8")


def validate_static(root: Path) -> None:
    """Validate ownership, UI, transport, MCard, and line-count contracts."""
    controls = read(
        root,
        "kanda_reasoner_app/tab3_manual_review_runtime/ai_web_controls_runtime.py",
    )
    provider = read(
        root,
        "kanda_reasoner_app/tab3_manual_review_runtime/ai_web_docstring_provider_runtime.py",
    )
    task_contracts = read(
        root,
        "kanda_reasoner_app/tab3_manual_review_runtime/ai_docstring_task_contracts.py",
    )
    async_runtime = read(
        root,
        "kanda_reasoner_app/tab3_manual_review_runtime/ai_docstring_async_runtime.py",
    )
    generator = read(
        root,
        "kanda_reasoner_app/insert_missing_docstrings_gui/ai_docstring_generator.py",
    )
    summarizer = read(
        root,
        "kanda_reasoner_app/insert_missing_docstrings_gui/module_summarizer.py",
    )
    state = read(
        root,
        "kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_gui_help/window_state.py",
    )
    layout = read(
        root,
        "kanda_reasoner_app/tab3_manual_review_runtime/layout_runtime.py",
    )
    run_controls = read(
        root,
        "kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_gui_help/run_controls.py",
    )
    project_paths = read(
        root,
        "kanda_reasoner_app/tab3_manual_review_runtime/project_paths_runtime.py",
    )
    review_support = read(
        root,
        "kanda_reasoner_app/tab3_manual_review_runtime/review_support.py",
    )
    export_summary = read(
        root,
        "kanda_reasoner_app/tab3_manual_review_runtime/export_summary.py",
    )
    shared_transport = read(root, "kanda_reasoner_app/web_ai_provider_runtime.py")

    for marker in (
        'QRadioButton("Heuristic")',
        'QRadioButton("Local AI")',
        'QRadioButton("Web AI")',
        'QPushButton("Open Config AI")',
        "application_web_ai_configuration",
        "request_cloud_approval",
    ):
        require(marker in controls, "missing central mode contract: " + marker)
    require("ProjectWebAIModelCatalogWorker" not in controls, "Docstring owns duplicate Web catalog")
    require("resolve_environment_key" not in controls, "Docstring owns duplicate credential resolution")
    print("DOCSTRING_WEB_AI_SHARED_CONTROLS: PASS")
    print("DOCSTRING_MODE_ONLY_CONTROLS: PASS")

    require("request_chat_completion(" in provider, "shared transport not reused")
    require("urllib.request" not in provider, "second Web AI HTTP client introduced")
    require('"allow_fallbacks": False' in provider, "silent fallback not blocked")
    require('"data_collection": "deny"' in provider, "OpenRouter privacy option missing")
    require('"require_parameters": True' in provider, "parameter capability gate missing")
    require('"additionalProperties": False' in provider, "strict schema shape missing")
    print("STRICT_WEB_DOCSTRING_PROVIDER: PASS")

    for marker in (
        "active_project_id",
        "active_project_slug",
        "active_project_root_fingerprint",
        "active_project_support_root",
        "input_snapshot_hash",
        "privacy_approval_id",
        "resolve_project_tool_boundary_identity",
    ):
        require(marker in task_contracts, "missing task identity field: " + marker)
    require("path.relative_to(project_root" in task_contracts, "source containment missing")
    print("DYNAMIC_ACTIVE_PROJECT_IDENTITY: PASS")

    for marker in (
        "QThread(owner)",
        "DocstringAIDraftWorker",
        "_identity_is_current",
        "source changed; one draft was rejected",
        "row changed; one draft was rejected",
        "stale AI result rejected",
        "_restore_action_state(self._owner)",
    ):
        require(marker in async_runtime, "missing async lifecycle marker: " + marker)
    print("DOCSTRING_MCARD_STALE_RESULT_GUARD: PASS")
    print("DOCSTRING_AI_OFF_GUI_THREAD: PASS")

    require(
        "canonical_project_support_root(self._project_root)" in generator,
        "Docstring cache does not use canonical Project Support",
    )
    require("/.docstring_cache" not in generator, "cache still hardcoded in Project source")
    require("urllib.request" not in generator, "generator owns duplicate HTTP transport")
    require("urllib.request" not in summarizer, "summarizer owns duplicate HTTP transport")
    print("DOCSTRING_CACHE_EXTERNAL_PROJECT_SUPPORT: PASS")
    print("NO_DUPLICATE_DOCSTRING_WEB_TRANSPORT: PASS")

    require("ai_api_key=ai_api_key" in run_controls, "memory-only key not passed to worker")
    require("_run_result_is_current" in run_controls, "batch stale Project guard missing")
    require("request_cloud_approval" in run_controls, "batch Web approval missing")
    require("_heuristic_radio" in controls and "_web_ai_radio" in controls, "mode radios missing")
    require("_review_stop_ai_drafts_button" in layout, "AI stop action missing")
    require("initialize_controls(self, self._prefs)" in state, "control owner not initialized")
    print("DOCSTRING_BATCH_PROJECT_IDENTITY_GUARD: PASS")
    print("DOCSTRING_CLOUD_APPROVAL_REQUIRED: PASS")

    for marker in (
        "resolve_project_tool_boundary_identity",
        "active_project_support_root",
        "docstring_assistant",
        "manual_review_state.json",
        "manual_review_exports",
    ):
        require(marker in project_paths, "missing Project Support path marker: " + marker)
    require("project_freeze_ledger" not in export_summary, "review export targets Tool ledger")
    require("manual_review_state_path(owner)" in review_support, "external state owner missing")
    require("legacy_manual_review_state_path(owner)" in review_support, "legacy read compatibility missing")
    require("return str(run_report_path(self))" in run_controls, "run report remains in source")
    print("DOCSTRING_REPORT_EXTERNAL_PROJECT_SUPPORT: PASS")
    print("DOCSTRING_REVIEW_STATE_EXTERNAL_PROJECT_SUPPORT: PASS")

    require("_ALLOWED_CHAT_REQUEST_OPTIONS" in shared_transport, "request option gate missing")
    require("Unsupported chat request options" in shared_transport, "option rejection missing")
    print("BOUNDED_SHARED_TRANSPORT_OPTIONS: PASS")

    changed_sources = (
        "kanda_reasoner_app/web_ai_credentials.py",
        "kanda_reasoner_app/web_ai_configuration.py",
        "kanda_reasoner_app/reasoner_engine/config_web_ai_tab.py",
        "kanda_reasoner_app/web_ai_provider_runtime.py",
        "kanda_reasoner_app/reasoner_engine/project_web_ai_tab.py",
        "kanda_reasoner_app/insert_missing_docstrings_gui/ai_config.py",
        "kanda_reasoner_app/insert_missing_docstrings_gui/ai_docstring_generator.py",
        "kanda_reasoner_app/insert_missing_docstrings_gui/module_summarizer.py",
        "kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_gui_help/ai_settings.py",
        "kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_gui_help/run_controls.py",
        "kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_gui_help/window_state.py",
        "kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_gui_help/worker_thread.py",
        "kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_help/run_orchestrator.py",
        "kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_help/_run_execution.py",
        "kanda_reasoner_app/tab3_manual_review_runtime/ai_web_controls_runtime.py",
        "kanda_reasoner_app/tab3_manual_review_runtime/ai_web_docstring_provider_runtime.py",
        "kanda_reasoner_app/tab3_manual_review_runtime/ai_docstring_task_contracts.py",
        "kanda_reasoner_app/tab3_manual_review_runtime/ai_docstring_async_runtime.py",
        "kanda_reasoner_app/tab3_manual_review_runtime/ai_docstring_row_bridge_runtime.py",
        "kanda_reasoner_app/tab3_manual_review_runtime/ai_openai_compatible_provider_runtime.py",
        "kanda_reasoner_app/tab3_manual_review_runtime/ai_settings_runtime.py",
        "kanda_reasoner_app/tab3_manual_review_runtime/ai_suggestion.py",
        "kanda_reasoner_app/tab3_manual_review_runtime/inline_corrector_runtime.py",
        "kanda_reasoner_app/tab3_manual_review_runtime/layout_runtime.py",
        "kanda_reasoner_app/tab3_manual_review_runtime/review_bulk_drafts_runtime.py",
        "kanda_reasoner_app/tab3_manual_review_runtime/review_engine_status_runtime.py",
        "kanda_reasoner_app/tab3_manual_review_runtime/project_paths_runtime.py",
        "kanda_reasoner_app/tab3_manual_review_runtime/review_support.py",
        "kanda_reasoner_app/tab3_manual_review_runtime/export_summary.py",
        "kanda_reasoner_app/tab3_manual_review_runtime/scan_report_lifecycle_runtime.py",
        "kanda_reasoner_app/tab3_manual_review_runtime/report_io_runtime.py",
    )
    for relative in changed_sources:
        count = len(read(root, relative).splitlines())
        require(count <= 500, relative + " exceeds 500 physical lines")
    print("TOUCHED_SOURCE_MODULES_MAX_500_LINES: PASS")


def validate_runtime(root: Path) -> None:
    """Exercise dynamic roots, cache ownership, strict transport, and key lookup."""
    root_text = str(root)
    if root_text not in sys.path:
        sys.path.insert(0, root_text)

    from kanda_reasoner_app.insert_missing_docstrings_gui.ai_config import AIConfig
    from kanda_reasoner_app.insert_missing_docstrings_gui.ai_docstring_generator import (
        AIDocstringGenerator,
    )
    from kanda_reasoner_app.insert_missing_docstrings_gui.docstring_policy import (
        DocstringPolicy,
    )
    from kanda_reasoner_app.project_support_boundary import (
        resolve_project_tool_boundary_identity,
    )
    from kanda_reasoner_app.tab3_manual_review_runtime.ai_docstring_provider_runtime import (
        AIProviderRequest,
    )
    from kanda_reasoner_app.tab3_manual_review_runtime.ai_web_docstring_provider_runtime import (
        build_web_docstring_provider,
    )
    from kanda_reasoner_app.tab3_manual_review_runtime.project_paths_runtime import (
        manual_review_export_root,
        manual_review_state_path,
        run_report_path,
    )
    from kanda_reasoner_app.web_ai_provider_contracts import (
        ProviderConfigurationError,
        get_gateway_profile,
    )
    from kanda_reasoner_app.web_ai_provider_runtime import request_chat_completion

    with tempfile.TemporaryDirectory() as temp_dir:
        project = Path(temp_dir) / "nested" / "sample_project"
        project.mkdir(parents=True)
        identity = resolve_project_tool_boundary_identity(
            project,
            tool_source_root=Path(temp_dir) / "tool",
        )
        require(identity.active_project_root == project.resolve(), "exact Project root lost")
        require(
            identity.active_project_support_root != identity.active_project_root,
            "Project Support collapsed into source",
        )
        generator = AIDocstringGenerator(
            config=AIConfig(),
            project_root=project,
            policy=DocstringPolicy(),
        )
        require(
            project.resolve() not in generator._cache_path.parents,
            "Docstring cache remains inside active Project source",
        )

        class Edit:
            def text(self) -> str:
                return str(project)

        owner = SimpleNamespace(_root_path_edit=Edit())
        expected_support = identity.active_project_support_root / "docstring_assistant"
        for candidate in (
            run_report_path(owner),
            manual_review_state_path(owner),
            manual_review_export_root(owner),
        ):
            require(expected_support in candidate.parents, "Docstring state left support root")
            require(project.resolve() not in candidate.parents, "Docstring state entered source")
    print("NESTED_ACTIVE_PROJECT_ROOT_SUPPORTED: PASS")
    print("DYNAMIC_PROJECT_SUPPORT_ROOT: PASS")
    print("DYNAMIC_DOCSTRING_SUPPORT_STATE: PASS")

    captured: list[dict[str, object]] = []

    class Response:
        def __init__(self, payload: dict[str, object]) -> None:
            self._raw = json.dumps(payload).encode("utf-8")

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, traceback):
            return False

        def read(self, size: int = -1) -> bytes:
            return self._raw if size < 0 else self._raw[:size]

    def opener(request, timeout):
        del timeout
        body = json.loads(request.data.decode("utf-8"))
        captured.append(body)
        return Response(
            {
                "choices": [
                    {
                        "message": {
                            "content": json.dumps(
                                {"docstring_body": "Return the calculated value."}
                            )
                        },
                        "finish_reason": "stop",
                    }
                ]
            }
        )

    provider = build_web_docstring_provider(
        gateway_id="openrouter",
        model_id="test/model",
        api_key="secret",
        opener=opener,
    )
    result = provider(
        AIProviderRequest(
            project_root="C:/project",
            relative_file_path="module.py",
            symbol_kind="function",
            symbol_name="calculate",
            signature="calculate(value)",
            source_snippet="def calculate(value):\n    return value",
            heuristic_draft="Return the value.",
        )
    )
    require(result.success, "strict Web provider did not return a draft")
    require(captured, "strict Web provider did not call shared transport")
    require(
        captured[0]["response_format"]["json_schema"]["strict"] is True,
        "strict JSON Schema was not transmitted",
    )
    require(
        captured[0]["provider"]["data_collection"] == "deny",
        "OpenRouter data collection was not denied",
    )
    print("STRICT_WEB_PROVIDER_RUNTIME: PASS")

    try:
        request_chat_completion(
            get_gateway_profile("openrouter"),
            "test/model",
            [{"role": "user", "content": "test"}],
            "secret",
            request_options={"model": "forbidden override"},
            opener=opener,
        )
    except ProviderConfigurationError:
        pass
    else:
        raise AssertionError("core request override was accepted")
    print("CORE_REQUEST_OVERRIDE_BLOCKED: PASS")


def validate_real_qt(root: Path) -> None:
    """Instantiate central config and Docstring mode-only controls."""
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    root_text = str(root)
    if root_text not in sys.path:
        sys.path.insert(0, root_text)
    try:
        from PySide6.QtWidgets import QApplication, QLineEdit
    except ImportError as exc:
        raise AssertionError("PySide6 is required for real-widget validation") from exc
    from kanda_reasoner_app.reasoner_engine.config_web_ai_tab import ConfigWebAITab
    from kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui import MissingDocstringsWindow
    from kanda_reasoner_app.web_ai_configuration import application_web_ai_configuration

    app = QApplication.instance() or QApplication([])
    config = ConfigWebAITab()
    window = MissingDocstringsWindow()
    try:
        controller = application_web_ai_configuration()
        require(config._controller is controller, "Config tab does not own shared controller")
        require(config.gateway_combo.count() == 2, "central gateway options missing")
        require(config.api_key_edit.echoMode() == QLineEdit.EchoMode.Password, "central key visible")
        print("DOCSTRING_QT_PASSWORD_ENUM_VALIDATOR: PASS")
        require(config.free_only_checkbox.isChecked(), "central free filter default changed")
        require(window._heuristic_radio.isChecked(), "heuristic default missing")
        require(hasattr(window, "_local_ai_radio") and hasattr(window, "_web_ai_radio"), "mode radios missing")
        require(not window._open_web_ai_config_button.isHidden(), "Config Web AI shortcut missing")
        window._web_ai_radio.setChecked(True)
        app.processEvents()
        require(window._ai_enabled_checkbox.isChecked(), "Web mode compatibility state missing")
        require(window._ai_provider_mode_combo.currentText() == "Web AI", "Web mode not synchronized")
    finally:
        window.close()
        config.close()
        app.processEvents()
    print("REAL_DOCSTRING_ASSISTANT_WEB_AI_WIDGET: PASS")
    print("REAL_DOCSTRING_MODE_ONLY_CONTROLS: PASS")


def main() -> int:
    """Run focused static, runtime, and optional real-Qt validation."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--static-only", action="store_true")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    validate_static(root)
    validate_runtime(root)
    if not args.static_only:
        validate_real_qt(root)
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
