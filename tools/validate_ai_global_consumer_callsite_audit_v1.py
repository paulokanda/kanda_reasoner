# project-path: tools/validate_ai_global_consumer_callsite_audit_v1.py
"""Audit every production Local AI and Web AI invocation against global owners."""

from __future__ import annotations

import argparse
import ast
import importlib
import sys
from pathlib import Path
from types import SimpleNamespace

FEATURE_ID = "ai-global-consumer-callsite-audit-v1r1"

LOCAL_CHAT_CALLERS = {
    "kanda_reasoner_app/error_memory_gui/_ai_corrector_service.py",
    "kanda_reasoner_app/freeze_after_update_gui/_local_ai_formulary.py",
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/planner_local_ai_docstring_review.py",
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/planner_local_ai_staged_protocol.py",
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_diff_review_assistant.py",
}
WEB_CHAT_CALLERS = {
    "kanda_reasoner_app/error_memory_gui/_web_ai_corrector_service.py",
    "kanda_reasoner_app/freeze_after_update_gui/_web_ai_formulary.py",
    "kanda_reasoner_app/insert_missing_docstrings_gui/ai_docstring_generator.py",
    "kanda_reasoner_app/insert_missing_docstrings_gui/module_summarizer.py",
    "kanda_reasoner_app/manage_architecture/ai_review/web_adapter.py",
    "kanda_reasoner_app/tab3_manual_review_runtime/ai_openai_compatible_provider_runtime.py",
    "kanda_reasoner_app/tab3_manual_review_runtime/ai_web_docstring_provider_runtime.py",
}
WEB_STREAM_CALLERS = {
    "kanda_reasoner_app/reasoner_engine/project_web_ai_workers.py",
}
LOCAL_DIRECT_CONNECTOR_CALLERS = {
    "kanda_reasoner_app/reasoner_engine/ai_bridge.py",
}
LOCAL_NETWORK_OWNERS = {
    "kanda_reasoner_app/reasoner_engine/v10_model_registry.py",
    "kanda_reasoner_app/reasoner_engine/v10_qwen_ai_models.py",
}
WEB_NETWORK_OWNERS = {
    "kanda_reasoner_app/web_ai_model_catalog.py",
    "kanda_reasoner_app/web_ai_provider_runtime.py",
}


def _read(root: Path, rel: str) -> str:
    return (root / rel).read_text(encoding="utf-8")


def _active_exclusion_policy(root: Path) -> tuple[dict[str, list[str]], object]:
    """Load the canonical Project exclusion policy used by active-source exports."""
    root_text = str(root)
    if root_text not in sys.path:
        sys.path.insert(0, root_text)
    policy = importlib.import_module("kanda_reasoner_app.project_exclusion_policy")
    rules = policy.load_reasoner_project_exclusion_rules(root)
    return rules, policy.should_exclude_reasoner_project_path


def _production_python_files(root: Path) -> list[Path]:
    """Return only active production Python files under the canonical policy."""
    base = root / "kanda_reasoner_app"
    rules, should_exclude = _active_exclusion_policy(root)
    return sorted(
        path
        for path in base.rglob("*.py")
        if "__pycache__" not in path.parts
        and not should_exclude(path, root, rules)
    )


def _validate_active_source_scope(root: Path) -> None:
    """Prove archived Docstring paths are excluded before call-site scanning."""
    rules, should_exclude = _active_exclusion_policy(root)
    legacy_root = (
        root
        / "kanda_reasoner_app"
        / "insert_missing_docstrings_gui"
        / "LOGIC_insert_mssg_dcstrngs"
    )
    _require(
        should_exclude(legacy_root, root, rules),
        "Canonical Project exclusion policy no longer excludes legacy Docstring logic.",
    )
    active_paths = {_relative(root, path) for path in _production_python_files(root)}
    _require(
        not any("logic_insert_mssg_dcstrngs" in path.lower() for path in active_paths),
        "Excluded legacy Docstring logic leaked into the active-source inventory.",
    )
    print("CENTRAL_PROJECT_EXCLUSION_POLICY_APPLIED: PASS")
    print("EXCLUDED_LEGACY_AI_PATHS_IGNORED: PASS")


def _relative(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def _callers(root: Path, terminal_name: str) -> set[str]:
    found: set[str] = set()
    for path in _production_python_files(root):
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))
        except (OSError, SyntaxError, UnicodeError):
            continue
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            func = node.func
            if isinstance(func, ast.Name):
                name = func.id
            elif isinstance(func, ast.Attribute):
                name = func.attr
            else:
                continue
            if name == terminal_name:
                found.add(_relative(root, path))
    return found


def _files_with_any(root: Path, needles: tuple[str, ...]) -> set[str]:
    found: set[str] = set()
    for path in _production_python_files(root):
        text = path.read_text(encoding="utf-8", errors="replace")
        if any(needle in text for needle in needles):
            found.add(_relative(root, path))
    return found


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def validate_static(root: Path) -> None:
    _validate_active_source_scope(root)
    local_callers = _callers(root, "chat_with_local_model")
    _require(local_callers == LOCAL_CHAT_CALLERS, f"Local chat callers drifted: {sorted(local_callers)}")

    web_callers = _callers(root, "request_chat_completion")
    _require(web_callers == WEB_CHAT_CALLERS, f"Web chat callers drifted: {sorted(web_callers)}")

    web_stream_callers = _callers(root, "stream_chat_completion")
    _require(web_stream_callers == WEB_STREAM_CALLERS, f"Web stream callers drifted: {sorted(web_stream_callers)}")

    direct_connector = _callers(root, "V9QwenAIModels")
    _require(
        direct_connector == LOCAL_DIRECT_CONNECTOR_CALLERS,
        f"Direct Local AI connector callers drifted: {sorted(direct_connector)}",
    )

    local_network = _files_with_any(
        root,
        (
            "requests.get(",
            "requests.post(",
            "urllib.request.urlopen(",
            '["ollama", "list"]',
        ),
    )
    _require(
        local_network <= (LOCAL_NETWORK_OWNERS | WEB_NETWORK_OWNERS),
        "Unexpected production network owner(s): " + str(sorted(local_network - LOCAL_NETWORK_OWNERS - WEB_NETWORK_OWNERS)),
    )

    local_settings = _read(root, "kanda_reasoner_app/tab3_manual_review_runtime/ai_settings_runtime.py")
    for forbidden in (
        "urllib.request",
        "urllib.error",
        "subprocess.run",
        "def _discover_models",
        "def _models_from_tags",
        "def _models_from_v1_models",
        "def _models_from_cli",
    ):
        _require(forbidden not in local_settings, "Legacy Docstring catalog transport remains: " + forbidden)
    for required in (
        "application_local_ai_configuration",
        "controller.refresh_models()",
        "ai_web_controls_runtime",
        "Endpoint and model are application-scoped",
    ):
        _require(required in local_settings, "Global Local AI delegation missing: " + required)

    settings_facade = _read(
        root,
        "kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_gui_help/ai_settings.py",
    )
    _require(
        "global endpoint/model remain Config AI-owned" in settings_facade,
        "Docstring settings facade does not preserve global ownership",
    )
    _require("cfg.base_url" not in settings_facade and "cfg.model" not in settings_facade,
             "Docstring config load can still project endpoint/model")

    local_config = _read(root, "kanda_reasoner_app/local_ai_configuration.py")
    runtime_state = _read(root, "kanda_reasoner_app/local_ai_runtime_state.py")
    local_service = _read(root, "kanda_reasoner_app/reasoner_engine/local_ai_chat_service.py")
    registry = _read(root, "kanda_reasoner_app/reasoner_engine/v10_model_registry.py")
    connector = _read(root, "kanda_reasoner_app/reasoner_engine/v10_qwen_ai_models.py")
    for text, terms, label in (
        (local_config, ("local_ai/base_url", "local_ai/selected_model_id", "_publish_runtime_snapshot"), "local config"),
        (runtime_state, ("LocalAIConfigurationSnapshot", "runtime_local_ai_configuration_snapshot"), "runtime snapshot"),
        (local_service, ("runtime_local_ai_configuration_snapshot", "snapshot.base_url", "snapshot.model_id"), "local service"),
        (registry, ("runtime_local_ai_configuration_snapshot", "snapshot.base_url", "snapshot.model_id"), "local registry"),
        (connector, ("runtime_local_ai_configuration_snapshot", "snapshot.base_url"), "local connector"),
    ):
        for term in terms:
            _require(term in text, f"{label} missing {term}")

    qsettings_writers = set()
    for path in _production_python_files(root):
        text = path.read_text(encoding="utf-8", errors="replace")
        if "QSettings(" in text and ".setValue(" in text and any(
            token in text
            for token in ("selected_model", "local_ai/base_url", "local_ai/selected_model_id")
        ):
            qsettings_writers.add(_relative(root, path))
    _require(
        qsettings_writers == {"kanda_reasoner_app/local_ai_configuration.py"},
        "Competing Local AI settings owner(s): " + str(sorted(qsettings_writers)),
    )

    endpoint_literals = _files_with_any(root, ("https://openrouter.ai", "https://api.kilo.ai"))
    _require(
        endpoint_literals == {"kanda_reasoner_app/web_ai_provider_contracts.py"},
        "Web gateway endpoint ownership drifted: " + str(sorted(endpoint_literals)),
    )
    web_config = _read(root, "kanda_reasoner_app/web_ai_configuration.py")
    web_runtime = _read(root, "kanda_reasoner_app/web_ai_provider_runtime.py")
    web_catalog = _read(root, "kanda_reasoner_app/web_ai_model_catalog.py")
    for text, terms, label in (
        (web_config, ("WebAIConfigurationSnapshot", "resolve_environment_key", "Project identity"), "web config"),
        (web_runtime, ("request_chat_completion", "stream_chat_completion", "request_json_payload"), "web transport"),
        (web_catalog, ("request_json_payload", "fetch_gateway_models"), "web catalog"),
    ):
        for term in terms:
            _require(term in text, f"{label} missing {term}")

    boundary_files = (
        "kanda_reasoner_app/local_ai_configuration.py",
        "kanda_reasoner_app/web_ai_configuration.py",
    )
    for rel in boundary_files:
        text = _read(root, rel)
        for forbidden in ("active_project_root", "active_project_id", "project_support_root", "daily_work_root"):
            _require(forbidden not in text, rel + " stores Project identity: " + forbidden)

    authority_checks = {
        "kanda_reasoner_app/freeze_after_update_gui/_ui_builder.py": ("draft only", "Preview remains read-only", "explicit human authority"),
        "kanda_reasoner_app/error_memory_gui/_ai_correction_action.py": ("preview-only", "will not save"),
        "kanda_reasoner_app/manage_architecture/ai_review/gui_integration.py": ("read-only", "advisory"),
    }
    for rel, terms in authority_checks.items():
        text = _read(root, rel).lower()
        for term in terms:
            _require(term.lower() in text, rel + " lost authority marker: " + term)

    print("AI_CALLSITE_INVENTORY_COMPLETE: PASS")
    print("LOCAL_AI_ALL_CHAT_CONSUMERS_GLOBAL: PASS")
    print("LOCAL_AI_NO_DUPLICATE_CATALOG_TRANSPORT: PASS")
    print("LOCAL_AI_SINGLE_SETTINGS_OWNER: PASS")
    print("WEB_AI_ALL_CHAT_CONSUMERS_CENTRAL: PASS")
    print("WEB_AI_NO_DUPLICATE_TRANSPORT_OR_ENDPOINT: PASS")
    print("AI_TOOL_PROJECT_BOUNDARY: PASS")
    print("AI_AUTHORITY_BOUNDARIES_PRESERVED: PASS")


class _Widget:
    def __init__(self, value: object = "") -> None:
        self.value_data = value

    def text(self) -> str:
        return str(self.value_data)

    def setText(self, value: object) -> None:
        self.value_data = value

    def currentText(self) -> str:
        return str(self.value_data)

    def setCurrentText(self, value: object) -> None:
        self.value_data = value

    def value(self) -> int:
        return int(self.value_data)

    def setValue(self, value: object) -> None:
        self.value_data = int(value)

    def isChecked(self) -> bool:
        return bool(self.value_data)

    def setChecked(self, value: object) -> None:
        self.value_data = bool(value)


class _FakeConfig:
    base_url = "http://stale.invalid/v1"
    model = "stale-model"
    workers = 7
    include_private = False
    min_confidence = "high"
    uncertain_annotation = False

    @classmethod
    def from_json(cls, _path: str) -> "_FakeConfig":
        return cls()


class _FakeController:
    def __init__(self) -> None:
        self.refresh_count = 0

    def refresh_models(self) -> bool:
        self.refresh_count += 1
        return True


def validate_runtime(root: Path) -> None:
    sys.path.insert(0, str(root))
    try:
        module = importlib.import_module("kanda_reasoner_app.tab3_manual_review_runtime.ai_settings_runtime")
        fake_controller = _FakeController()
        original_import = module.import_module

        def fake_import(name: str):
            if name == "kanda_reasoner_app.local_ai_configuration":
                return SimpleNamespace(application_local_ai_configuration=lambda: fake_controller)
            if name == "kanda_reasoner_app.tab3_manual_review_runtime.ai_web_controls_runtime":
                return SimpleNamespace(build_ai_config=lambda owner: ("global", owner))
            return original_import(name)

        module.import_module = fake_import
        owner = SimpleNamespace()
        statuses: list[str] = []
        module._show_status = lambda _owner, message: statuses.append(str(message))
        module._runtime_refresh_models(owner)
        _require(fake_controller.refresh_count == 1, "Legacy refresh did not delegate globally")
        _require("Config AI" in statuses[-1], "Delegated refresh status is unclear")
        _require(module._runtime_build_ai_config(owner) == ("global", owner), "Build config did not delegate globally")

        owner = SimpleNamespace(
            _config_path_edit=_Widget(""),
            _base_url_edit=_Widget("http://global.example/v1"),
            _model_combo=_Widget("global-model"),
            _workers_spin=_Widget(2),
            _include_private_checkbox=_Widget(True),
            _min_confidence_combo=_Widget("low"),
            _no_uncertain_checkbox=_Widget(False),
        )
        module._get_open_file_name = lambda *_args: ("fake.json", "")
        module._ai_config_class = lambda: _FakeConfig
        module._save_preferences = lambda _owner: None
        module._show_status = lambda _owner, _message: None
        module._runtime_load_config_from_file(owner)
        _require(owner._base_url_edit.text() == "http://global.example/v1", "Config load overrode global endpoint")
        _require(owner._model_combo.currentText() == "global-model", "Config load overrode global model")
        _require(owner._workers_spin.value() == 7, "Task worker option was not loaded")
        _require(owner._include_private_checkbox.isChecked() is False, "Task private option was not loaded")
        _require(owner._min_confidence_combo.currentText() == "high", "Task confidence option was not loaded")
        _require(owner._no_uncertain_checkbox.isChecked() is True, "Task uncertainty option was not loaded")
        print("DOCSTRING_LEGACY_REFRESH_DELEGATES_GLOBAL: PASS")
        print("DOCSTRING_TASK_CONFIG_CANNOT_OVERRIDE_GLOBAL_AI: PASS")
    finally:
        if str(root) in sys.path:
            sys.path.remove(str(root))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    args = parser.parse_args()
    root = Path(args.root).resolve()
    validate_static(root)
    validate_runtime(root)
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
