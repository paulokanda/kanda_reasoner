# project-path: tools/validate_integrated_free_api_web_ai_v1.py
"""Validate API-only free Python providers and duplicate-tab rollback."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import py_compile
import sys
from pathlib import Path
from typing import Mapping

FEATURE_ID = "integrated-free-api-web-ai-v1"

CHANGED_CODE = (
    "kanda_reasoner_app/web_ai_provider_contracts.py",
    "kanda_reasoner_app/python_coding_ai_catalog.py",
    "kanda_reasoner_app/web_ai_model_catalog.py",
    "kanda_reasoner_app/web_ai_stream_runtime.py",
    "kanda_reasoner_app/web_ai_configuration.py",
    "kanda_reasoner_app/reasoner_engine/config_web_ai_ui_support.py",
    "kanda_reasoner_app/reasoner_engine/config_web_ai_tab.py",
    "kanda_reasoner_app/reasoner_engine/config_direct_web_ai_tab.py",
    "kanda_reasoner_app/reasoner_engine/config_ai_tab.py",
    "kanda_reasoner_app/reasoner_engine/project_web_ai_tab.py",
    "kanda_reasoner_app/reasoner_engine/project_web_ai_tab_ui.py",
    "tools/validate_config_web_ai_central_v1.py",
    "tools/validate_integrated_free_api_web_ai_v1.py",
)

REMOVED_PATHS = (
    "kanda_reasoner_app/free_python_ai/__init__.py",
    "kanda_reasoner_app/free_python_ai/catalog.py",
    "kanda_reasoner_app/free_python_ai/messages.py",
    "kanda_reasoner_app/free_python_ai/workers.py",
    "kanda_reasoner_app/reasoner_engine/free_python_ai_tab.py",
    "kanda_reasoner_app/reasoner_engine/free_python_ai_tab_ui.py",
    "tools/validate_free_python_project_ai_tab_v1.py",
    "kanda_reasoner_app/reasoner_engine/config_external_ai_tab.py",
    "kanda_reasoner_app/reasoner_engine/project_web_ai_external_handoff.py",
)

PROTECTED_HASHES = {
    "kanda_reasoner_app/local_ai_configuration.py": (
        "9f66737307b4c59f018dcf0e9d02b1313478db1bb022abc06ac40cbcf7030d67"
    ),
    "kanda_reasoner_app/reasoner_engine/config_local_ai_tab.py": (
        "c64c0f0437ed99b47beb079f307e3dc95c8a88424f422483a9945feeaa1dca88"
    ),
    "kanda_reasoner_app/reasoner_engine/ai_reasoner_main_window.py": (
        "a7deda2e9ad4e897d24e14356a1e94bcf04ff00b5b0bbae42db8c1654467c9de"
    ),
    "kanda_reasoner_app/reasoner_engine/project_web_ai_bridge.py": (
        "00f53d04ebfe4cafa4f291d89f79c906082cd5093311eb629e5ac1c140582c01"
    ),
    "kanda_reasoner_app/reasoner_engine/project_web_ai_session.py": (
        "87c7c9b85785f460448fff1829f943dcc8d283cb393f23f513cea344f516c571"
    ),
    "kanda_reasoner_app/reasoner_engine/project_web_ai_workers.py": (
        "e32125dfc3d5c4570df6e4abd193bfd2a899eb1d81c6275d072ef183bcaa68ec"
    ),
    "kanda_reasoner_app/reasoner_engine/project_web_ai_apply_workflow.py": (
        "5e69e2f2ddb9554a427aa61dde3493e717a654835863f5b6677441e7fd370911"
    ),
    "kanda_reasoner_app/reasoner_engine/project_web_ai_agent_runtime.py": (
        "a74628899498dbca9cd182fa59fb5ee1a4a337163a896902ba39298dc6c7226b"
    ),
    "kanda_reasoner_app/project_selection_registry.py": (
        "98dbb376654e0608f9d6863829999ac5bcf0523715c859f3b067cde42b9d7fa1"
    ),
    "kanda_reasoner_app/project_operation_authority.py": (
        "76dc9df9f415c011a360056af9cf66a126aee7f052c67047f05e4358caed5434"
    ),
}


def require(condition: bool, message: str) -> None:
    """Raise one focused validation failure."""
    if not condition:
        raise AssertionError(message)


def source(root: Path, relative: str) -> str:
    """Read one UTF-8 source file."""
    return (root / relative).read_text(encoding="utf-8")


def sha256(path: Path) -> str:
    """Return one file SHA-256."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_code_and_boundaries(root: Path) -> None:
    """Validate code quality, removals, and protected owner boundaries."""
    for relative in CHANGED_CODE:
        path = root / relative
        require(path.is_file(), "changed source missing: " + relative)
        text = path.read_text(encoding="utf-8")
        require(text.isascii(), "non-ASCII changed source: " + relative)
        ast.parse(text, filename=str(path))
        py_compile.compile(str(path), doraise=True)
        lines = len(text.splitlines())
        require(0 < lines <= 500, relative + " exceeds 500 physical lines")
    print("API_ONLY_REMOTE_AI_PYTHON_SYNTAX: PASS")
    print("API_ONLY_REMOTE_AI_MODULE_SIZE: PASS")

    for relative in REMOVED_PATHS:
        require(not (root / relative).exists(), "removed path remains: " + relative)
    for relative in (
        "kanda_reasoner_app/reasoner_tools_gui_shell/tool_specs.py",
        "kanda_reasoner_app/reasoner_tools_gui_shell/_lazy_tab_shell_chrome.py",
        "kanda_reasoner_app/reasoner_tools_gui_shell/project_scope_sync.py",
    ):
        require(
            "free_python_ai" not in source(root, relative),
            "Free Python AI shell reference remains: " + relative,
        )
    print("FREE_PYTHON_AI_TAB_ROLLED_BACK: PASS")
    print("FREE_PYTHON_AI_DUPLICATE_OWNER_ABSENT: PASS")
    print("BROWSER_ONLY_AI_SURFACE_REMOVED: PASS")

    for relative, expected in PROTECTED_HASHES.items():
        path = root / relative
        require(path.is_file(), "protected source missing: " + relative)
        require(sha256(path) == expected, "protected source changed: " + relative)
    print("LOCAL_AI_PROTECTED_HASHES: PASS")
    print("PROJECT_WEB_AI_CORE_PROTECTED_HASHES: PASS")
    print("PROJECT_AUTHORITY_PROTECTED_HASHES: PASS")


def validate_provider_contracts(root: Path) -> None:
    """Validate provider classes, free guards, and exact coding allowlists."""
    sys.path.insert(0, str(root))
    from kanda_reasoner_app.python_coding_ai_catalog import approved_direct_model_ids
    from kanda_reasoner_app.web_ai_provider_contracts import (
        get_gateway_profile,
        provider_profiles,
    )

    gateway_ids = tuple(profile.gateway_id for profile in provider_profiles("gateway"))
    direct_ids = tuple(profile.gateway_id for profile in provider_profiles("direct"))
    require(gateway_ids == ("openrouter", "kilo"), "gateway profile order changed")
    require(
        direct_ids == ("gemini", "mistral", "qwen", "groq"),
        "direct provider set mismatch",
    )
    require("deepseek" not in direct_ids, "metered DeepSeek API admitted")

    openrouter = get_gateway_profile("openrouter")
    kilo = get_gateway_profile("kilo")
    require(openrouter.base_url == "https://openrouter.ai/api/v1", "OpenRouter URL changed")
    require(openrouter.api_key_env == "OPENROUTER_API_KEY", "OpenRouter key changed")
    require(kilo.base_url == "https://api.kilo.ai/api/gateway", "Kilo URL changed")
    require(kilo.anonymous_free_allowed, "Kilo anonymous free contract changed")
    print("EXISTING_GATEWAY_CONTRACTS_PRESERVED: PASS")

    expected = {
        "gemini": (
            "GEMINI_API_KEY",
            "provider_free_tier",
            ("gemini-3.5-flash", "gemini-3.5-flash-lite"),
        ),
        "mistral": (
            "MISTRAL_API_KEY",
            "account_free_mode",
            ("mistral-medium-3-5", "mistral-small-2603"),
        ),
        "qwen": (
            "DASHSCOPE_API_KEY",
            "time_limited_free_quota",
            ("qwen3-coder-flash", "qwen3-coder-next", "qwen3-coder-plus"),
        ),
        "groq": (
            "GROQ_API_KEY",
            "account_free_plan",
            ("openai/gpt-oss-120b", "openai/gpt-oss-20b", "qwen/qwen3.6-27b"),
        ),
    }
    for provider_id, (key_name, access_kind, model_ids) in expected.items():
        profile = get_gateway_profile(provider_id)
        require(profile.provider_class == "direct", provider_id + " class mismatch")
        require(profile.api_key_env == key_name, provider_id + " key mismatch")
        require(profile.free_access_kind == access_kind, provider_id + " free mode mismatch")
        require(profile.requires_free_confirmation, provider_id + " guard missing")
        require(not profile.supports_stream_options, provider_id + " stream options mismatch")
        require(
            approved_direct_model_ids(provider_id) == model_ids,
            provider_id + " model allowlist mismatch",
        )
    require(len(get_gateway_profile("qwen").static_models) == 3, "Qwen static catalog mismatch")
    print("DIRECT_GEMINI_FREE_TIER_CONTRACT: PASS")
    print("DIRECT_MISTRAL_FREE_MODE_CONTRACT: PASS")
    print("DIRECT_QWEN_FREE_QUOTA_ONLY_CONTRACT: PASS")
    print("DIRECT_GROQ_FREE_PLAN_CONTRACT: PASS")
    print("DIRECT_DEEPSEEK_METERED_API_EXCLUDED: PASS")


def _fixture_payload(items: list[Mapping[str, object]]) -> bytes:
    return json.dumps({"data": items}).encode("utf-8")


class _Headers:
    def get(self, _key: str, default: str = "") -> str:
        return default


class _Response:
    def __init__(self, body: bytes) -> None:
        self._body = body
        self.headers = _Headers()

    def __enter__(self) -> "_Response":
        return self

    def __exit__(self, *_args: object) -> None:
        return None

    def read(self, maximum: int = -1) -> bytes:
        return self._body if maximum < 0 else self._body[:maximum]


class _Opener:
    def __init__(self, body: bytes) -> None:
        self._body = body

    def __call__(self, *_args: object, **_kwargs: object) -> _Response:
        return _Response(self._body)


def validate_catalog_and_controller(root: Path) -> None:
    """Validate catalog normalization and fail-closed readiness gates."""
    from kanda_reasoner_app.web_ai_model_catalog import fetch_gateway_models
    from kanda_reasoner_app.web_ai_provider_contracts import get_gateway_profile

    fixtures = {
        "gemini": [
            {"id": "models/gemini-3.5-flash", "display_name": "Gemini Flash"},
            {"id": "models/gemini-3.6-flash", "display_name": "Not approved"},
        ],
        "mistral": [
            {"id": "mistral-small-2603", "name": "Mistral Small 4"},
            {"id": "mistral-large-2512", "name": "Not approved"},
        ],
        "groq": [
            {"id": "openai/gpt-oss-120b", "name": "GPT OSS 120B"},
            {"id": "llama-3.1-8b-instant", "name": "Not approved"},
        ],
    }
    for provider_id, items in fixtures.items():
        models = fetch_gateway_models(
            get_gateway_profile(provider_id),
            "fixture",
            opener=_Opener(_fixture_payload(items)),
        )
        free_ids = [model.model_id for model in models if model.free_status]
        require(len(free_ids) == 1, provider_id + " exact allowlist failed")

    qwen_models = fetch_gateway_models(get_gateway_profile("qwen"), "fixture")
    require(
        tuple(model.model_id for model in qwen_models)
        == ("qwen3-coder-flash", "qwen3-coder-next", "qwen3-coder-plus"),
        "Qwen static catalog mismatch",
    )
    controller_source = source(root, "kanda_reasoner_app/web_ai_configuration.py")
    for token in (
        "def free_access_confirmation_required",
        "def free_access_confirmed",
        "def set_free_access_confirmed",
        "if not self.free_access_confirmed():",
    ):
        require(token in controller_source, "controller free guard missing: " + token)
    require("QSettings" not in controller_source, "direct provider key persistence added")
    print("DIRECT_PROVIDER_EXACT_MODEL_ALLOWLISTS: PASS")
    print("DIRECT_PROVIDER_UNAPPROVED_MODELS_REJECTED: PASS")
    print("DIRECT_PROVIDER_FREE_ACCESS_GATES: PASS")
    print("DIRECT_PROVIDER_KEYS_SESSION_ONLY: PASS")


class _StreamResponse:
    def __init__(self, lines: tuple[bytes, ...]) -> None:
        self._lines = lines
        self.headers = _Headers()

    def __enter__(self) -> "_StreamResponse":
        return self

    def __exit__(self, *_args: object) -> None:
        return None

    def __iter__(self):
        return iter(self._lines)


class _RecordingStreamOpener:
    def __init__(self) -> None:
        self.bodies: list[dict[str, object]] = []

    def __call__(self, request: object, **_kwargs: object) -> _StreamResponse:
        raw = bytes(getattr(request, "data", b"") or b"")
        self.bodies.append(json.loads(raw.decode("utf-8")))
        lines = (
            b'data: {"id":"r1","model":"fixture","choices":[{"delta":{"content":"ok"},"finish_reason":"stop"}]}\n',
            b"data: [DONE]\n",
        )
        return _StreamResponse(lines)


def validate_transport_contract() -> None:
    """Validate provider-compatible streaming payloads without network access."""
    from kanda_reasoner_app.web_ai_provider_contracts import get_gateway_profile
    from kanda_reasoner_app.web_ai_provider_runtime import stream_chat_completion

    for provider_id, expects_stream_options in (
        ("openrouter", True),
        ("gemini", False),
        ("mistral", False),
        ("qwen", False),
        ("groq", False),
    ):
        opener = _RecordingStreamOpener()
        result = stream_chat_completion(
            get_gateway_profile(provider_id),
            "fixture-model",
            [{"role": "user", "content": "test"}],
            "fixture-key",
            opener=opener,
            allow_non_stream_fallback=False,
        )
        require(result.content == "ok", provider_id + " stream mismatch")
        has_stream_options = "stream_options" in opener.bodies[0]
        require(
            has_stream_options == expects_stream_options,
            provider_id + " stream_options mismatch",
        )
    print("DIRECT_PROVIDER_STREAM_COMPATIBILITY: PASS")


def validate_ui_sources(root: Path) -> None:
    """Validate API-only Config AI and one shared Web AI conversation owner."""
    config_ai = source(root, "kanda_reasoner_app/reasoner_engine/config_ai_tab.py")
    gateway_ui = source(root, "kanda_reasoner_app/reasoner_engine/config_web_ai_tab.py")
    direct_ui = source(root, "kanda_reasoner_app/reasoner_engine/config_direct_web_ai_tab.py")
    project_ui = source(root, "kanda_reasoner_app/reasoner_engine/project_web_ai_tab.py")
    project_layout = source(root, "kanda_reasoner_app/reasoner_engine/project_web_ai_tab_ui.py")

    for token in (
        'addTab(self.web_ai_tab, "Config Web AI")',
        'addTab(self.direct_web_ai_tab, "Direct API Providers")',
        'addTab(self.local_ai_tab, "Config Local AI")',
        "self._web_controller = application_web_ai_configuration()",
    ):
        require(token in config_ai, "Config AI composition missing: " + token)
    for forbidden in (
        "Manual Web Assistants",
        "ConfigExternalAITab",
        "manual_web_tab",
        "ProjectWebAIExternalHandoffMixin",
        "Copy and Open External AI",
        "external_handoff_button",
    ):
        require(
            forbidden not in config_ai + project_ui + project_layout,
            "browser-only AI surface remains: " + forbidden,
        )
    require('provider_profiles("gateway")' in gateway_ui, "gateway UI not isolated")
    require('provider_profiles("direct")' in direct_ui, "direct UI not isolated")
    for name in ("Gemini", "Mistral", "Qwen", "Groq"):
        require(name in direct_ui, "direct provider guidance missing: " + name)
    require("DeepSeek direct" in direct_ui, "DeepSeek metered exclusion missing")
    require("application_web_ai_configuration" in project_ui, "central Web AI owner lost")
    require("ProjectWebAIModelCatalogWorker" not in project_ui, "duplicate catalog added")
    print("API_ONLY_CONFIG_AI_COMPOSITION: PASS")
    print("ONE_PROJECT_WEB_AI_CONVERSATION_OWNER: PASS")
    print("LOCAL_AI_BOX_UNCHANGED: PASS")
    print("MCARD APPLICABILITY: NOT_APPLICABLE")


def validate_help(root: Path) -> None:
    """Validate human-facing API-only guidance."""
    files = (
        "kanda_reasoner_app/reasoner_tools_gui_help/config_ai.json",
        "kanda_reasoner_app/reasoner_tools_gui_help/web_ai.json",
        "kanda_reasoner_app/reasoner_tools_gui_shell/help_docs/source/config_ai.md",
        "kanda_reasoner_app/reasoner_tools_gui_shell/help_docs/rendered/config_ai.html",
    )
    combined = "\n".join(source(root, relative) for relative in files)
    for token in (
        "Direct API Providers",
        "Gemini",
        "Mistral",
        "Qwen",
        "Groq",
        "Free Quota Only",
        "DeepSeek",
        "metered",
        "browser-only",
    ):
        require(token.casefold() in combined.casefold(), "help missing: " + token)
    require(
        "Manual Web Assistants" not in combined,
        "help still advertises Manual Web Assistants",
    )
    print("CONFIG_AI_API_ONLY_HELP_IN_SYNC: PASS")

def validate_real_qt(root: Path) -> None:
    """Exercise real Config AI and Project Web AI with one central controller."""
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    if os.name == "nt" and Path("C:/Windows/Fonts").is_dir():
        os.environ.setdefault("QT_QPA_FONTDIR", "C:/Windows/Fonts")
    try:
        from PySide6.QtCore import QCoreApplication, QEvent
        from PySide6.QtWidgets import QApplication
    except ImportError as exc:
        raise AssertionError("PySide6 is required for real-widget validation") from exc

    from kanda_reasoner_app.reasoner_engine.config_ai_tab import ConfigAITab
    from kanda_reasoner_app.reasoner_engine.project_web_ai_tab import ProjectWebAITab
    from kanda_reasoner_app.web_ai_configuration import application_web_ai_configuration
    from kanda_reasoner_app.web_ai_provider_contracts import ModelDescriptor

    app = QApplication.instance() or QApplication([])
    config = ConfigAITab()
    project = ProjectWebAITab()
    try:
        controller = application_web_ai_configuration()
        require(config._web_controller is controller, "Config AI controller mismatch")
        require(project._web_config is controller, "Project Web AI controller mismatch")
        labels = tuple(
            config.subtabs.tabText(index)
            for index in range(config.subtabs.count())
        )
        require(
            labels == (
                "Config Web AI",
                "Direct API Providers",
                "Config Local AI",
            ),
            "Config AI subtab order mismatch",
        )
        require(config.direct_web_ai_tab.provider_combo.count() == 4, "direct providers missing")
        require(not hasattr(project, "external_handoff_button"), "browser handoff button remains")

        controller.set_gateway_id("groq")
        controller.set_api_key("fixture")
        controller.set_free_access_confirmed(True)
        model = ModelDescriptor(
            gateway_id="groq",
            model_id="openai/gpt-oss-120b",
            display_name="GPT OSS 120B",
            free_status=True,
            free_access_label="requires the provider Free Plan",
            catalog_timestamp="fixture",
        )
        controller._all_models = [model]
        controller.set_selected_model_id(model.model_id)
        controller._touch()
        app.processEvents()
        require("openai/gpt-oss-120b" in project.web_config_summary_value.text(), "Web AI did not receive direct provider")
        require("Groq API Free Plan" in project.web_config_summary_value.text(), "provider label missing")
        require(controller.ready_for_chat(), "direct provider not ready")
        print("DIRECT_PROVIDER_SHARED_WITH_PROJECT_WEB_AI_REAL_QT: PASS")
        print("CONFIG_EXTERNAL_WEB_AI_REAL_QT: PASS")
    finally:
        for widget in (project, config):
            widget.close()
            widget.deleteLater()
        app.processEvents()
        QCoreApplication.sendPostedEvents(None, QEvent.Type.DeferredDelete)
        app.processEvents()
    print("INTEGRATED_FREE_API_WEB_AI_REAL_QT: PASS")


def main() -> int:
    """Run focused static and real-Qt validation."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--static-only", action="store_true")
    args = parser.parse_args()
    root = args.root.expanduser().resolve(strict=True)
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    validate_code_and_boundaries(root)
    validate_provider_contracts(root)
    validate_catalog_and_controller(root)
    validate_transport_contract()
    validate_ui_sources(root)
    validate_help(root)
    if not args.static_only:
        validate_real_qt(root)
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
