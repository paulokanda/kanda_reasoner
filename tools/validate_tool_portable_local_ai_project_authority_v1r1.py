"""Validate Local AI Project authority before Tool Portable creation."""

from __future__ import annotations

import argparse
import ast
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from types import SimpleNamespace
from typing import Any

FEATURE_ID = "kanda-reasoner-tool-portable-local-ai-project-authority-v1r1"
SETTINGS_RELATIVE = (
    "kanda_reasoner_app/reasoner_engine/"
    "ai_reasoner_main_window_help/settings_manager.py"
)
BUILDER_RELATIVE = "tools/build_kanda_reasoner_tool_portable.py"
RUNTIME_ALLOWLIST_RELATIVE = "portable/PORTABLE_RUNTIME_ALLOWLIST.json"
BUILDER_MANIFEST_RELATIVE = "portable/PORTABLE_BUILDER_MANIFEST.json"
EXISTING_VALIDATORS = (
    (
        "tools/validate_kanda_reasoner_tool_portable_direct_build_v1r1.py",
        "VALIDATION OK: kanda-reasoner-tool-portable-direct-pyinstaller-v1r2",
    ),
    (
        "tools/validate_tool_portable_functional_smoke_owner_reuse_v1.py",
        "VALIDATION OK: "
        "kanda-reasoner-tool-portable-functional-smoke-owner-reuse-v1",
    ),
    (
        "tools/validate_project_structure_show_project_json_handoff_v1.py",
        "VALIDATION OK: "
        "kanda-reasoner-project-structure-show-project-json-handoff-v1",
    ),
)


def require(condition: bool, code: str) -> None:
    """Raise a deterministic validation error when condition is false."""
    if not condition:
        raise RuntimeError(code)


def sha256(path: Path) -> str:
    """Return the SHA-256 of one file."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_module(path: Path, name: str):
    """Load one source module without importing the GUI main window."""
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, "MODULE_SPEC_FAILED")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def configure_tool_import_path(root: Path) -> None:
    """Make the selected Tool source root importable for source fixtures."""
    root_text = str(root)
    normalized_root = os.path.normcase(os.path.normpath(root_text))
    retained = []
    for entry in sys.path:
        candidate = entry or os.getcwd()
        normalized = os.path.normcase(os.path.normpath(candidate))
        if normalized != normalized_root:
            retained.append(entry)
    sys.path[:] = [root_text, *retained]
    require(
        os.path.normcase(os.path.normpath(sys.path[0])) == normalized_root,
        "TOOL_ROOT_IMPORT_PATH_NOT_ACTIVE",
    )


class FakeTextWidget:
    """Provide the small QLineEdit surface used by the settings manager."""

    def __init__(self, value: str = "") -> None:
        self._value = value

    def text(self) -> str:
        return self._value

    def setText(self, value: str) -> None:
        self._value = str(value)


class FakeToggle:
    """Provide a checked-state widget surface."""

    def __init__(self, checked: bool = False) -> None:
        self._checked = checked

    def isChecked(self) -> bool:
        return self._checked

    def setChecked(self, value: bool) -> None:
        self._checked = bool(value)


class FakeCombo:
    """Provide the QComboBox surface used by the settings manager."""

    def __init__(self, values: tuple[str, ...]) -> None:
        self._values = values
        self._index = 0

    def findText(self, value: str) -> int:
        try:
            return self._values.index(value)
        except ValueError:
            return -1

    def setCurrentIndex(self, index: int) -> None:
        self._index = index

    def currentText(self) -> str:
        return self._values[self._index]


class FakeSettings:
    """Provide deterministic QSettings-like storage."""

    def __init__(self, values: dict[str, Any]) -> None:
        self.values = dict(values)
        self.removed: list[str] = []
        self.synced = False

    def value(
        self,
        key: str,
        default: Any = None,
        **options: Any,
    ) -> Any:
        requested_type = options.get("type")
        value = self.values.get(key, default)
        if requested_type is bool:
            return bool(value)
        if requested_type is str:
            return str(value)
        return value

    def setValue(self, key: str, value: Any) -> None:
        self.values[key] = value

    def remove(self, key: str) -> None:
        self.values.pop(key, None)
        self.removed.append(key)

    def sync(self) -> None:
        self.synced = True


def fake_window(settings: FakeSettings) -> SimpleNamespace:
    """Build one window fixture for settings restore and save."""
    return SimpleNamespace(
        settings=settings,
        project_root_edit=FakeTextWidget(),
        json_path_edit=FakeTextWidget(),
        cache_dir_edit=FakeTextWidget(),
        governance_path_edit=FakeTextWidget(),
        prefer_code_radio=FakeToggle(),
        prefer_prose_radio=FakeToggle(),
        verbosity_combo=FakeCombo(("Concise", "Detailed", "With Code")),
        debug_checkbox=FakeToggle(),
        analysis_auto_load_checkbox=FakeToggle(),
        _settings_ready=True,
    )


def _validate_settings_fixtures(root: Path, settings_module) -> None:
    """Prove stale QSettings cannot grant Project authority."""
    original_registry = settings_module.ProjectSelectionRegistry
    try:
        class NoProjectRegistry:
            def resolve_current_boundary(self):
                return None

        settings_module.ProjectSelectionRegistry = NoProjectRegistry
        stale = FakeSettings(
            {
                "project_root": r"E:\\kanda_reasoner",
                "json_path": r"E:\\stale\\project.json",
                "cache_dir": r"E:\\cache",
                "governance_path": r"E:\\governance.json",
            }
        )
        window = fake_window(stale)
        settings_module.WindowSettingsManager().restore(window)
        require(window.project_root_edit.text() == "", "NO_PROJECT_ROOT_NOT_BLANK")
        require(window.json_path_edit.text() == "", "NO_PROJECT_JSON_NOT_BLANK")
        require(
            window.cache_dir_edit.text() == r"E:\\cache",
            "NON_PROJECT_SETTING_NOT_RESTORED",
        )

        with tempfile.TemporaryDirectory() as temporary:
            project_root = Path(temporary) / "external_project"
            project_root.mkdir()

            class SelectedProjectRegistry:
                def resolve_current_boundary(self):
                    return SimpleNamespace(active_project_root=project_root)

            settings_module.ProjectSelectionRegistry = SelectedProjectRegistry
            selected = FakeSettings(
                {
                    "project_root": r"E:\\wrong_project",
                    "json_path": r"E:\\old_project\\project.json",
                }
            )
            selected_window = fake_window(selected)
            manager = settings_module.WindowSettingsManager()
            manager.restore(selected_window)
            require(
                Path(selected_window.project_root_edit.text()).resolve(strict=False)
                == project_root.resolve(strict=False),
                "REGISTRY_PROJECT_ROOT_NOT_AUTHORITATIVE",
            )

            selected_window.project_root_edit.setText(str(project_root))
            selected_window.json_path_edit.setText(r"E:\\old_project\\project.json")
            manager.save(selected_window)
            require(
                "project_root" not in selected.values,
                "LEGACY_PROJECT_ROOT_KEY_PERSISTED",
            )
            require(
                "project_root" in selected.removed,
                "LEGACY_PROJECT_ROOT_KEY_NOT_REMOVED",
            )
            require(selected.synced, "SETTINGS_NOT_SYNCED")
    finally:
        settings_module.ProjectSelectionRegistry = original_registry

    resolver_path = (
        root
        / "kanda_reasoner_app"
        / "reasoner_engine"
        / "ai_reasoner_main_window_help"
        / "project_json_path_resolver.py"
    )
    resolver_module = load_module(
        resolver_path,
        "kanda_local_ai_project_json_path_resolver_fixture",
    )
    blank_window = SimpleNamespace(
        project_root_edit=FakeTextWidget(""),
        project_index=SimpleNamespace(project_root=""),
    )
    require(
        resolver_module.current_project_root_from_window(blank_window) is None,
        "BLANK_PROJECT_ROOT_DID_NOT_SHORT_CIRCUIT",
    )


def _validate_source_contract(root: Path) -> None:
    """Validate source ownership, module size, and manifest non-membership."""
    settings_path = root / SETTINGS_RELATIVE
    builder_path = root / BUILDER_RELATIVE
    validator_path = root / "tools" / Path(__file__).name
    for path in (settings_path, builder_path, validator_path):
        require(path.is_file(), "TARGET_MISSING:" + str(path))
        source = path.read_text(encoding="utf-8")
        source.encode("ascii")
        ast.parse(source, filename=str(path))
        require(
            len(source.splitlines()) <= 500,
            "MODULE_LINE_LIMIT_EXCEEDED:" + str(path),
        )

    settings_text = settings_path.read_text(encoding="utf-8")
    for token in (
        "ProjectSelectionRegistry",
        "resolve_current_boundary",
        'settings.remove("project_root")',
        "if project_root",
    ):
        require(token in settings_text, "SETTINGS_AUTHORITY_TOKEN_MISSING:" + token)
    for forbidden in (
        'settings.value("project_root"',
        'settings.setValue("project_root"',
        '_set_text("project_root_edit", "project_root")',
    ):
        require(
            forbidden not in settings_text,
            "DUPLICATE_PROJECT_AUTHORITY_REMAINS:" + forbidden,
        )

    builder_text = builder_path.read_text(encoding="utf-8")
    for token in (
        "validate_tool_portable_local_ai_project_authority_v1r1.py",
        "--skip-existing-validators",
        "LOCAL AI PROJECT AUTHORITY PRE-BUILD GATE: PASS",
    ):
        require(token in builder_text, "BUILDER_GATE_TOKEN_MISSING:" + token)

    runtime_allowlist = json.loads(
        (root / RUNTIME_ALLOWLIST_RELATIVE).read_text(encoding="utf-8")
    )
    runtime_items = runtime_allowlist.get("items")
    require(isinstance(runtime_items, list), "RUNTIME_ALLOWLIST_ITEMS_INVALID")
    runtime_paths = {
        str(item.get("source_relative") or "")
        for item in runtime_items
        if isinstance(item, dict)
    }
    require(
        SETTINGS_RELATIVE not in runtime_paths,
        "SETTINGS_FILE_UNEXPECTEDLY_IN_RUNTIME_ALLOWLIST",
    )

    builder_manifest = json.loads(
        (root / BUILDER_MANIFEST_RELATIVE).read_text(encoding="utf-8")
    )
    files = builder_manifest.get("files")
    require(isinstance(files, dict), "BUILDER_MANIFEST_FILES_INVALID")
    require(
        SETTINGS_RELATIVE not in files,
        "SETTINGS_FILE_UNEXPECTEDLY_IN_BUILDER_MANIFEST",
    )
    require(
        BUILDER_RELATIVE not in files,
        "BUILD_SCRIPT_UNEXPECTEDLY_IN_BUILDER_MANIFEST",
    )


def _run_existing_validators(root: Path) -> None:
    """Run the current release guards without creating a Portable."""
    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    previous_pythonpath = environment.get("PYTHONPATH", "")
    environment["PYTHONPATH"] = str(root) + (
        os.pathsep + previous_pythonpath if previous_pythonpath else ""
    )
    for relative, marker in EXISTING_VALIDATORS:
        validator = root / relative
        require(validator.is_file(), "EXISTING_VALIDATOR_MISSING:" + relative)
        completed = subprocess.run(
            [sys.executable, str(validator), "--tool-root", str(root)],
            cwd=str(root),
            env=environment,
            text=True,
            capture_output=True,
            check=False,
            timeout=1200,
        )
        output = (completed.stdout or "") + (completed.stderr or "")
        print(output, end="" if output.endswith("\n") else "\n")
        require(completed.returncode == 0, "EXISTING_VALIDATOR_FAILED:" + relative)
        require(marker in output, "EXISTING_VALIDATOR_MARKER_MISSING:" + relative)


def main() -> int:
    """Run the Local AI Project authority regression suite."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--tool-root", type=Path, required=True)
    parser.add_argument("--skip-existing-validators", action="store_true")
    args = parser.parse_args()
    root = args.tool_root.expanduser().resolve(strict=True)
    configure_tool_import_path(root)

    _validate_source_contract(root)
    settings_module = load_module(
        root / SETTINGS_RELATIVE,
        "kanda_local_ai_settings_manager_fixture",
    )
    _validate_settings_fixtures(root, settings_module)
    if not args.skip_existing_validators:
        _run_existing_validators(root)

    print("VALIDATOR TOOL ROOT IMPORT PATH: PASS")
    print("LOCAL AI PROJECT ROOT REGISTRY AUTHORITY: PASS")
    print("LOCAL AI STALE QSETTINGS ROOT IGNORED: PASS")
    print("LOCAL AI NO-PROJECT JSON STATE CLEARED: PASS")
    print("LOCAL AI SELECTED PROJECT ROOT RESTORED FROM REGISTRY: PASS")
    print("LOCAL AI LEGACY PROJECT ROOT SETTING REMOVED: PASS")
    print("PORTABLE PRE-BUILD AUTHORITY GATE: PASS")
    print("PORTABLE RUNTIME ALLOWLIST MODIFIED: NO")
    print("PORTABLE BUILDER MANIFEST MODIFIED: NO")
    print("PORTABLE BUILD EXECUTED BY VALIDATION: NO")
    print(f"VALIDATION OK: {FEATURE_ID}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
