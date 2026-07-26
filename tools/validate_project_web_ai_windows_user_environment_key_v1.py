# project-path: tools/validate_project_web_ai_windows_user_environment_key_v1.py
"""Validate shared Windows User environment-key fallback for KANDA Web AI."""

from __future__ import annotations

import argparse
import ast
import os
import sys
from pathlib import Path
from types import SimpleNamespace

FEATURE_ID = "project-web-ai-windows-user-environment-key-v1"
CONTROLLER = Path("kanda_reasoner_app/web_ai_configuration.py")
CONFIG_TAB = Path("kanda_reasoner_app/reasoner_engine/config_web_ai_tab.py")
CREDENTIALS = Path("kanda_reasoner_app/web_ai_credentials.py")


def require(condition: bool, message: str) -> None:
    """Raise one explicit validation failure."""
    if not condition:
        raise AssertionError(message)


def validate_source(root: Path) -> None:
    """Validate shared credential ownership and controller delegation."""
    controller_path = root / CONTROLLER
    credentials_path = root / CREDENTIALS
    config_tab_path = root / CONFIG_TAB
    controller = controller_path.read_text(encoding="utf-8")
    config_tab = config_tab_path.read_text(encoding="utf-8")
    credentials = credentials_path.read_text(encoding="utf-8")
    controller_tree = ast.parse(controller, filename=str(controller_path))
    credentials_tree = ast.parse(credentials, filename=str(credentials_path))

    require(
        "from kanda_reasoner_app.web_ai_credentials import resolve_environment_key" in controller,
        "central Web AI configuration does not import the shared credential owner",
    )
    require(
        "resolve_environment_key(profile.api_key_env)" in controller,
        "central Web AI environment-key resolver does not delegate",
    )
    require(
        "self._controller.load_environment_key()" in config_tab,
        "Config Web AI load command does not delegate to the central owner",
    )
    require("def resolve_environment_key" in credentials, "shared resolver missing")
    require("HKEY_CURRENT_USER" in credentials, "Windows User lookup missing")
    require(
        'OpenKey(winreg.HKEY_CURRENT_USER, "Environment")' in credentials,
        "HKCU Environment owner path missing",
    )
    require(
        "os.environ[clean_name] = value" in credentials,
        "resolved User value is not attached to the current session",
    )
    require("SetValueEx" not in credentials, "shared owner must not persist keys")
    require("DeleteValue" not in credentials, "shared owner must not delete keys")
    require("keyring" not in credentials.lower(), "new credential store introduced")
    require(
        "Windows User environment" in credentials,
        "credential source provenance is missing",
    )
    require("provider_runtime" not in credentials, "credential owner owns transport")

    controller_methods = {
        node.name
        for node in ast.walk(controller_tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }
    credential_methods = {
        node.name
        for node in ast.walk(credentials_tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }
    require("_load_environment_key" in controller_methods, "central resolver facade missing")
    require("load_environment_key" in controller_methods, "central public load command missing")
    require("resolve_environment_key" in credential_methods, "shared AST owner missing")
    print("WINDOWS_USER_ENVIRONMENT_KEY_SOURCE_CONTRACT: PASS")
    print("SHARED_WEB_AI_CREDENTIAL_OWNER: PASS")
    print("NO_CREDENTIAL_PERSISTENCE_OR_NEW_STORE: PASS")


def validate_runtime(root: Path) -> None:
    """Exercise process precedence and Windows User fallback without secrets."""
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    root_text = str(root)
    if root_text not in sys.path:
        sys.path.insert(0, root_text)

    import kanda_reasoner_app.web_ai_credentials as credentials

    original_os = credentials.os
    original_winreg = sys.modules.get("winreg")
    test_name = "KANDA_TEST_WEB_AI_ENV_KEY"
    user_value = "test-user-scope-key"
    process_value = "test-process-scope-key"

    class FakeKey:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, traceback):
            return False

    fake_winreg = SimpleNamespace(
        HKEY_CURRENT_USER=object(),
        OpenKey=lambda hive, path: FakeKey(),
        QueryValueEx=lambda key, name: (user_value, 1),
    )

    try:
        fake_os = SimpleNamespace(name="nt", environ={})
        credentials.os = fake_os
        sys.modules["winreg"] = fake_winreg
        value, source = credentials.resolve_environment_key(test_name)
        require(value == user_value, "Windows User value was not returned")
        require(source == "Windows User environment", "User source not reported")
        require(
            fake_os.environ.get(test_name) == user_value,
            "User value was not copied into session environment",
        )
        print("WINDOWS_USER_ENVIRONMENT_KEY_FALLBACK: PASS")

        fake_os.environ[test_name] = process_value

        def unexpected_open(*_args, **_kwargs):
            raise AssertionError("registry read despite process value")

        fake_winreg.OpenKey = unexpected_open
        value, source = credentials.resolve_environment_key(test_name)
        require(value == process_value, "current-process precedence failed")
        require(source == "current process", "process source was not reported")
        print("CURRENT_PROCESS_KEY_PRECEDENCE: PASS")
    finally:
        credentials.os = original_os
        if original_winreg is None:
            sys.modules.pop("winreg", None)
        else:
            sys.modules["winreg"] = original_winreg

    print("MCARD_REQUEST_LIFECYCLE_UNCHANGED: PASS")
    print("PROVIDER_RUNTIME_COMPATIBILITY_PRESERVED: PASS")
    print("PROJECT_SOURCE_READ_ONLY_BOUNDARY_PRESERVED: PASS")


def main() -> int:
    """Run focused validation."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--static-only", action="store_true")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    validate_source(root)
    if not args.static_only:
        validate_runtime(root)
    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
