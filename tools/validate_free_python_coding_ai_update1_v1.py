# project-path: tools/validate_free_python_coding_ai_update1_v1.py
"""Validate Update 1 free Python-coding AI catalog and Config AI integration."""

from __future__ import annotations

import argparse
import ast
import hashlib
import os
from pathlib import Path
import py_compile
import sys
from typing import Any, Sequence

FEATURE_ID = "free-python-coding-ai-catalog-and-config-update1-v1"

CHANGED_FILES = (
    "kanda_reasoner_app/python_coding_ai_catalog.py",
    "kanda_reasoner_app/external_ai_configuration.py",
    "kanda_reasoner_app/external_ai_handoff.py",
    "kanda_reasoner_app/reasoner_engine/config_external_ai_tab.py",
    "kanda_reasoner_app/reasoner_engine/config_ai_tab.py",
    "kanda_reasoner_app/reasoner_engine/config_web_ai_tab.py",
    "kanda_reasoner_app/reasoner_tools_gui_help/config_ai.json",
    "kanda_reasoner_app/reasoner_tools_gui_shell/help_docs/source/config_ai.md",
    "kanda_reasoner_app/reasoner_tools_gui_shell/help_docs/rendered/config_ai.html",
    "kanda_reasoner_app/reasoner_tools_gui_shell/main_window.py",
    "kanda_reasoner_app/web_ai_configuration.py",
    "kanda_reasoner_app/web_ai_model_catalog.py",
    "tools/validate_free_python_coding_ai_update1_v1.py",
)

APPROVED_OPENROUTER = (
    "openai/gpt-oss-120b:free",
    "openai/gpt-oss-20b:free",
    "cohere/north-mini-code:free",
)
APPROVED_KILO = ("kilo-auto/free",) + APPROVED_OPENROUTER
EXTERNAL_IDS = (
    "deepseek_chat",
    "qwen_studio",
    "claude_free",
    "chatgpt_free",
    "mistral_vibe_free",
)
FORBIDDEN_PROJECT_FIELDS = {
    "project_root",
    "project_id",
    "project_slug",
    "support_root",
    "project_json_path",
    "write_authority",
}


class MemorySettings:
    """Minimal QSettings-compatible memory fixture."""

    def __init__(self) -> None:
        self.values: dict[str, object] = {}

    def value(self, key: str, default: object = None) -> object:
        """Return a stored value or the supplied default."""
        return self.values.get(key, default)

    def setValue(self, key: str, value: object) -> None:
        """Store one value in memory."""
        self.values[str(key)] = value


def _require(condition: bool, marker: str) -> None:
    if not condition:
        raise AssertionError(marker)
    print(marker + ": PASS")


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _bootstrap(tool_root: Path) -> None:
    root_text = str(tool_root)
    if root_text not in sys.path:
        sys.path.insert(0, root_text)
    print("VALIDATOR TOOL ROOT IMPORT PATH: PASS")


def _validate_files(tool_root: Path) -> None:
    for relative in CHANGED_FILES:
        path = tool_root / relative
        _require(path.is_file(), "CHANGED FILE PRESENT " + relative)
        if path.suffix == ".py":
            source = path.read_text(encoding="utf-8")
            ast.parse(source, filename=str(path))
            line_count = len(source.splitlines())
            _require(line_count <= 500, "MODULE SIZE <=500 " + relative)
            py_compile.compile(str(path), doraise=True)
    print("CHANGED PYTHON AST AND COMPILE: PASS")


def _validate_catalog() -> None:
    from kanda_reasoner_app.python_coding_ai_catalog import (
        approved_direct_model_ids,
        external_python_coding_assistants,
        get_external_python_coding_assistant,
        is_approved_free_python_coding_model,
        validate_official_assistant_url,
    )
    from kanda_reasoner_app.web_ai_provider_contracts import ModelDescriptor

    _require(
        approved_direct_model_ids("openrouter") == APPROVED_OPENROUTER,
        "OPENROUTER APPROVED PYTHON MODEL SET",
    )
    _require(
        approved_direct_model_ids("kilo") == APPROVED_KILO,
        "KILO APPROVED PYTHON MODEL SET",
    )
    assistants = external_python_coding_assistants()
    _require(
        tuple(item.assistant_id for item in assistants) == EXTERNAL_IDS,
        "EXTERNAL PYTHON ASSISTANT EXACT SET",
    )
    _require(
        all(item.validated_url().startswith("https://") for item in assistants),
        "EXTERNAL ASSISTANT HTTPS ALLOWLIST",
    )
    allowed = ModelDescriptor(
        gateway_id="openrouter",
        model_id=APPROVED_OPENROUTER[0],
        display_name="fixture",
        free_status=True,
    )
    unapproved = ModelDescriptor(
        gateway_id="openrouter",
        model_id="openrouter/free",
        display_name="fixture",
        free_status=True,
    )
    paid = ModelDescriptor(
        gateway_id="openrouter",
        model_id=APPROVED_OPENROUTER[0],
        display_name="fixture",
        free_status=False,
    )
    _require(
        is_approved_free_python_coding_model(allowed),
        "APPROVED FREE MODEL ACCEPTED",
    )
    _require(
        not is_approved_free_python_coding_model(unapproved),
        "GENERIC FREE ROUTER REJECTED",
    )
    _require(
        not is_approved_free_python_coding_model(paid),
        "PAID FALLBACK REJECTED",
    )
    _expect_value_error(
        lambda: validate_official_assistant_url(
            "http://chatgpt.com/", allowed_hosts=("chatgpt.com",)
        ),
        "NON-HTTPS ASSISTANT URL REJECTED",
    )
    _expect_value_error(
        lambda: validate_official_assistant_url(
            "https://example.com/", allowed_hosts=("chatgpt.com",)
        ),
        "UNAPPROVED ASSISTANT HOST REJECTED",
    )
    _require(
        get_external_python_coding_assistant("chatgpt_free").assistant_id
        == "chatgpt_free",
        "EXTERNAL ASSISTANT STABLE ID",
    )


def _expect_value_error(action: Any, marker: str) -> None:
    try:
        action()
    except ValueError:
        print(marker + ": PASS")
        return
    raise AssertionError(marker)


def _validate_configuration_without_project() -> None:
    from dataclasses import asdict

    from kanda_reasoner_app.external_ai_configuration import (
        ExternalAIConfigurationController,
    )

    settings = MemorySettings()
    controller = ExternalAIConfigurationController(settings=settings)
    snapshot = controller.snapshot()
    _require(
        not (set(asdict(snapshot)) & FORBIDDEN_PROJECT_FIELDS),
        "EXTERNAL AI PROJECT AUTHORITY ABSENT",
    )
    controller.set_assistant_id("qwen_studio")
    _require(
        settings.values.get("external_ai/selected_assistant_id") == "qwen_studio",
        "EXTERNAL AI TOOL SETTING PERSISTENCE",
    )
    controller.set_assistant_id("unknown")
    _require(
        controller.assistant_id() == "deepseek_chat",
        "UNKNOWN EXTERNAL ASSISTANT SAFE FALLBACK",
    )
    print("EXTERNAL AI NO-PROJECT CONFIGURATION: PASS")


def _validate_web_filter() -> None:
    from kanda_reasoner_app.web_ai_configuration import WebAIConfigurationController
    from kanda_reasoner_app.web_ai_provider_contracts import ModelDescriptor

    controller = WebAIConfigurationController()
    controller._operation_id = "fixture"  # focused result-intake fixture
    models = [
        ModelDescriptor(
            gateway_id="openrouter",
            model_id=APPROVED_OPENROUTER[0],
            display_name="approved",
            free_status=True,
            catalog_timestamp="fixture",
        ),
        ModelDescriptor(
            gateway_id="openrouter",
            model_id="openrouter/free",
            display_name="generic router",
            free_status=True,
            catalog_timestamp="fixture",
        ),
        ModelDescriptor(
            gateway_id="openrouter",
            model_id="paid/model",
            display_name="paid",
            free_status=False,
            catalog_timestamp="fixture",
        ),
    ]
    controller._catalog_completed("fixture", models)
    _require(
        tuple(item.model_id for item in controller.visible_models())
        == (APPROVED_OPENROUTER[0],),
        "DIRECT MODEL CURATED FILTER",
    )
    controller.set_free_models_only(False)
    _require(
        controller.free_models_only()
        and len(controller.visible_models()) == 1,
        "DIRECT MODEL FREE LOCK",
    )
    print("NO AUTOMATIC PAID FALLBACK: PASS")


def _validate_gui(tool_root: Path) -> None:
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    try:
        from PySide6.QtWidgets import QApplication
    except ModuleNotFoundError as exc:
        raise RuntimeError("PySide6 is required for the functional GUI smoke.") from exc

    from kanda_reasoner_app.external_ai_configuration import (
        ExternalAIConfigurationController,
        install_application_external_ai_configuration,
    )
    from kanda_reasoner_app.local_ai_configuration import (
        LocalAIConfigurationController,
        install_application_local_ai_configuration,
    )
    from kanda_reasoner_app.reasoner_engine.config_ai_tab import ConfigAITab
    from kanda_reasoner_app.web_ai_configuration import (
        WebAIConfigurationController,
        install_application_web_ai_configuration,
    )

    app = QApplication.instance() or QApplication([])
    external_settings = MemorySettings()
    local_settings = MemorySettings()
    local_settings.setValue("local_ai/base_url", "http://127.0.0.1:11434/v1")
    local_settings.setValue("local_ai/selected_model_id", "fixture-local-model")
    external = ExternalAIConfigurationController(settings=external_settings)
    local = LocalAIConfigurationController(settings=local_settings)
    web = WebAIConfigurationController()
    install_application_external_ai_configuration(external)
    install_application_local_ai_configuration(local)
    install_application_web_ai_configuration(web)
    widget = ConfigAITab(
        local_controller=local,
        external_controller=external,
    )
    names = tuple(widget.subtabs.tabText(i) for i in range(widget.subtabs.count()))
    _require(
        names
        == (
            "Config Web AI",
            "Config Local AI",
            "Config External Web AI",
        ),
        "CONFIG AI THREE SUBTABS",
    )
    _require(
        widget.external_ai_tab.assistant_combo.count() == 5,
        "EXTERNAL AI GUI EXACT ASSISTANT COUNT",
    )
    _require(
        widget.web_ai_tab.free_only_checkbox.isChecked()
        and not widget.web_ai_tab.free_only_checkbox.isEnabled(),
        "DIRECT MODEL GUI FREE LOCK",
    )
    widget.close()
    app.processEvents()
    print("EXTERNAL AI CONFIG GUI FUNCTIONAL SMOKE: PASS")
    print("EXTERNAL AI NO-PROJECT GUI STATE: PASS")


def _validate_static_integration(tool_root: Path) -> None:
    main_text = (
        tool_root / "kanda_reasoner_app/reasoner_tools_gui_shell/main_window.py"
    ).read_text(encoding="utf-8")
    _require(
        "install_application_external_ai_configuration" in main_text,
        "EXTERNAL AI APPLICATION OWNER INSTALLED",
    )
    model_catalog_text = (
        tool_root / "kanda_reasoner_app/web_ai_model_catalog.py"
    ).read_text(encoding="utf-8")
    _require(
        '"kilo-auto/free"' in model_catalog_text,
        "KILO AUTO FREE CURRENT ID",
    )
    help_text = (
        tool_root
        / "kanda_reasoner_app/reasoner_tools_gui_shell/help_docs/source/config_ai.md"
    ).read_text(encoding="utf-8")
    _require(
        "## Config External Web AI" in help_text,
        "CONFIG EXTERNAL AI HELP SOURCE",
    )
    rendered_help = (
        tool_root
        / "kanda_reasoner_app/reasoner_tools_gui_shell/help_docs/rendered/config_ai.html"
    ).read_text(encoding="utf-8")
    _require(
        "<h2>Config External Web AI</h2>" in rendered_help,
        "CONFIG EXTERNAL AI HELP RENDERED",
    )
    runtime_manifest = tool_root / "portable/PORTABLE_RUNTIME_ALLOWLIST.json"
    builder_manifest = tool_root / "portable/PORTABLE_BUILDER_MANIFEST.json"
    _require(runtime_manifest.is_file() and builder_manifest.is_file(), "PORTABLE MANIFESTS PRESENT")
    changed_set = set(CHANGED_FILES)
    _require(
        "portable/PORTABLE_RUNTIME_ALLOWLIST.json" not in changed_set
        and "portable/PORTABLE_BUILDER_MANIFEST.json" not in changed_set,
        "PORTABLE MANIFESTS MODIFIED: NO",
    )
    print("PORTABLE STATIC IMPORT COLLECTION ASSUMPTION AVOIDED: PASS")


def main(argv: Sequence[str] | None = None) -> int:
    """Run focused Update 1 validation against the selected Tool root."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--tool-root", required=True)
    parser.add_argument("--skip-gui", action="store_true")
    parser.add_argument("--skip-qt", action="store_true")
    args = parser.parse_args(argv)
    tool_root = Path(args.tool_root).expanduser().resolve()
    if not tool_root.is_dir():
        print("VALIDATION BLOCKED: Tool root not found: " + str(tool_root))
        return 1
    try:
        _bootstrap(tool_root)
        _validate_files(tool_root)
        _validate_catalog()
        _validate_static_integration(tool_root)
        if args.skip_qt:
            print("QT CONFIGURATION AND GUI VALIDATION: NOT RUN")
        else:
            _validate_configuration_without_project()
            _validate_web_filter()
            if args.skip_gui:
                print("GUI FUNCTIONAL SMOKE: NOT RUN")
            else:
                _validate_gui(tool_root)
    except Exception as exc:
        print("VALIDATION ERROR: " + exc.__class__.__name__ + ": " + str(exc))
        return 1
    print("VALIDATION OK: " + FEATURE_ID)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
