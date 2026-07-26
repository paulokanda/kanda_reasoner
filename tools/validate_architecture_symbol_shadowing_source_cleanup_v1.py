# project-path: tools/validate_architecture_symbol_shadowing_source_cleanup_v1.py
"""Validate strict source-level cleanup of SYMBOL_SHADOWING findings."""

from __future__ import annotations

import argparse
import ast
import hashlib
import importlib
import json
import py_compile
import sys
import tempfile
import zipfile
from pathlib import Path
from typing import Any

__all__ = [
    "main",
]

FEATURE_ID = "architecture-symbol-shadowing-source-cleanup-v1"
STALE_VALIDATOR = "tools/validate_architecture_symbol_shadowing_precision_v1.py"
DYNAMIC_TARGET = (
    "tools/validate_planner_main_workbench_refactoring_path_clipboard_v1.py"
)
TARGET_FILES = (
    "kanda_reasoner_app/manage_architecture/kanda_refactor_project_index.py",
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/"
    "cst_facade_global_import_inserter.py",
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/"
    "cst_real_preview_writer.py",
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/"
    "planner_version_preference_box.py",
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/"
    "workbench_refactor_transaction.py",
    "kanda_reasoner_app/reasoner_runtime_collector/runtime_runner_help/"
    "_runtime_runner_part_1_bindings.py",
    "kanda_reasoner_app/reasoner_runtime_collector/runtime_runner_help/"
    "_runtime_runner_part_2_bindings.py",
    "kanda_reasoner_app/reasoner_runtime_collector/runtime_runner_help/"
    "_runtime_runner_part_2_scenarios.py",
    "kanda_reasoner_app/reasoner_runtime_collector/runtime_runner_help/"
    "_runtime_runner_part_2_window.py",
    "tools/validate_advanced_quality_review_import_boundary_v1.py",
    "tools/validate_architecture_review_running_indicator_ast_safe_refactor_v1.py",
    "tools/validate_large_module_split_audit_analysis_ast_safe_refactor_v1.py",
    DYNAMIC_TARGET,
    "tools/validate_query_router_ast_safe_refactor_v1.py",
)
SHARD_FILES = tuple(
    "kanda_reasoner_app/manage_architecture/manage_architecture_help/"
    f"manage_architecture_source_part_{index}_private_impl.py"
    for index in range(7, 22)
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _read_ascii(path: Path) -> str:
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        raise AssertionError("UTF8_BOM_FORBIDDEN:" + str(path))
    try:
        text = raw.decode("ascii")
    except UnicodeDecodeError as exc:
        raise AssertionError("NON_ASCII_SOURCE:" + str(path)) from exc
    return text


def _validate_zip(project_root: Path, patch_zip: Path) -> dict[str, Any]:
    if not patch_zip.is_file():
        raise AssertionError("PATCH_ZIP_MISSING:" + str(patch_zip))
    with zipfile.ZipFile(patch_zip) as archive:
        names = sorted(
            name
            for name in archive.namelist()
            if not name.endswith("/")
        )
        if "KANDA_FREEZE_HINT.json" not in names:
            raise AssertionError("ROOT_FREEZE_HINT_MISSING")
        hint = json.loads(
            archive.read("KANDA_FREEZE_HINT.json").decode("utf-8")
        )
        if hint.get("feature_id") != FEATURE_ID:
            raise AssertionError("FEATURE_ID_MISMATCH")
        payload_files = tuple(hint.get("validated_files") or ())
        expected_names = sorted((*payload_files, "KANDA_FREEZE_HINT.json"))
        if names != expected_names:
            raise AssertionError("ZIP_MEMBER_CONTRACT_CHANGED")
        payload_hashes = hint.get("payload_sha256") or {}
        for relative in payload_files:
            expected = str(payload_hashes.get(relative) or "")
            actual = hashlib.sha256(archive.read(relative)).hexdigest()
            if not expected or actual != expected:
                raise AssertionError("ZIP_PAYLOAD_HASH_MISMATCH:" + relative)
            installed = project_root / relative
            if not installed.is_file() or _sha256(installed) != expected:
                raise AssertionError("INSTALLED_PAYLOAD_HASH_MISMATCH:" + relative)
    print("ZIP CONTRACT: PASS")
    return hint


def _validate_python(project_root: Path, payload_files: tuple[str, ...]) -> None:
    checked = set(payload_files) | set(TARGET_FILES)
    for relative in sorted(checked):
        if not relative.endswith(".py"):
            continue
        path = project_root / relative
        py_compile.compile(str(path), doraise=True)
        text = _read_ascii(path)
        if len(text.splitlines()) > 500:
            raise AssertionError("TOUCHED_MODULE_OVER_500_LINES:" + relative)
    print("PYTHON_SYNTAX: PASS")
    print("SOURCE_ASCII_UTF8_NO_BOM: PASS")
    print("TOUCHED_MODULES_MAX_500_LINES: PASS")


def _validate_strict_detector_source(project_root: Path) -> None:
    loader = importlib.import_module(
        "kanda_reasoner_app.manage_architecture.manage_architecture_help."
        "source_loader_private_impl"
    )
    source = loader.load_manage_architecture_source()
    required = (
        "class SymbolShadowingVisitor(ast.NodeVisitor):",
        "def detect_symbol_shadowing_issues(",
        "self._record(node.name, node.lineno, \"function definition\")",
        "self._record_target_names(node.target, \"annotated assignment\")",
    )
    forbidden = (
        "_module_import_fallback_depth",
        "_in_direct_class_body",
        "_is_module_import_fallback",
        'if node.module == "__future__":',
    )
    for marker in required:
        if marker not in source:
            raise AssertionError("STRICT_DETECTOR_MARKER_MISSING:" + marker)
    for marker in forbidden:
        if marker in source:
            raise AssertionError("RELAXED_DETECTOR_MARKER_REMAINS:" + marker)
    print("STRICT_SYMBOL_SHADOWING_DETECTOR_RESTORED: PASS")


def _validate_dynamic_event_contract(project_root: Path) -> None:
    path = project_root / DYNAMIC_TARGET
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    event_classes = [
        node
        for node in tree.body
        if isinstance(node, ast.ClassDef) and node.name == "_FakeEvent"
    ]
    if len(event_classes) != 1:
        raise AssertionError("DYNAMIC_FAKE_EVENT_CLASS_COUNT_CHANGED")
    method_names = {
        node.name
        for node in event_classes[0].body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }
    if "type" in method_names:
        raise AssertionError("DYNAMIC_FAKE_EVENT_TYPE_METHOD_REMAINS")
    if "_qt_event_type" not in method_names:
        raise AssertionError("DYNAMIC_FAKE_EVENT_SHIM_METHOD_MISSING")
    text = path.read_text(encoding="utf-8")
    marker = 'setattr(_FakeEvent, "type", _FakeEvent._qt_event_type)'
    if marker not in text:
        raise AssertionError("DYNAMIC_FAKE_EVENT_SETATTR_MISSING")
    print("DYNAMIC_PROTOCOL_SHIM: PASS")


def _target_modules(architecture: Any, project_root: Path) -> dict[str, Any]:
    modules: dict[str, Any] = {}
    for relative in TARGET_FILES:
        module, _warnings = architecture.scan_module(
            project_root,
            project_root / relative,
            set(),
        )
        modules[module.module_id] = module
    return modules


def _validate_live_strict_target_scan(project_root: Path) -> None:
    architecture = importlib.import_module(
        "kanda_reasoner_app.manage_architecture.manage_architecture"
    )
    modules = _target_modules(architecture, project_root)
    issues = architecture.detect_symbol_shadowing_issues(
        project_root,
        modules,
    )
    if issues:
        details = "\n".join(
            f"{issue.path} :: {issue.message}" for issue in issues
        )
        raise AssertionError("TARGET_SYMBOL_SHADOWING_REMAINS:\n" + details)

    with tempfile.TemporaryDirectory() as directory:
        fixture_root = Path(directory)
        fixture = fixture_root / "genuine_shadow.py"
        fixture.write_text(
            "import json as payload\n"
            "payload = None\n"
            "\n"
            "def consume(list):\n"
            "    return list\n",
            encoding="utf-8",
        )
        module, _warnings = architecture.scan_module(
            fixture_root,
            fixture,
            set(),
        )
        fixture_issues = architecture.detect_symbol_shadowing_issues(
            fixture_root,
            {module.module_id: module},
        )
        names = "\n".join(issue.message for issue in fixture_issues)
        if "Symbol 'payload'" not in names or "Symbol 'list'" not in names:
            raise AssertionError("GENUINE_SHADOWING_DETECTION_REGRESSED")

    print("TARGET_SOURCE_SHADOWING_CLEARED_STRICT: PASS")
    print("GENUINE_SHADOWING_DETECTION_PRESERVED: PASS")


def _validate_runtime_smoke(project_root: Path) -> None:
    pref = importlib.import_module(
        "kanda_reasoner_app.manage_architecture.large_file_refactor_planner."
        "planner_version_preference_box"
    )

    class Settings:
        def __init__(self) -> None:
            self.data: dict[str, str] = {}

        def value(self, key: str, default: str = "") -> str:
            return self.data.get(key, default)

        def setValue(self, key: str, value: str) -> None:
            self.data[key] = value

        def sync(self) -> None:
            return None

    settings = Settings()
    factory = lambda: settings
    if pref.load_last_used_planner_route(settings_factory=factory) != (
        pref.PLANNER_ROUTE_LOCAL_AI
    ):
        raise AssertionError("PLANNER_PREFERENCE_DEFAULT_CHANGED")
    if not pref.remember_last_used_planner_route(
        pref.PLANNER_ROUTE_WEB_AI,
        settings_factory=factory,
    ):
        raise AssertionError("PLANNER_PREFERENCE_WRITE_CHANGED")
    if pref.load_last_used_planner_route(settings_factory=factory) != (
        pref.PLANNER_ROUTE_WEB_AI
    ):
        raise AssertionError("PLANNER_PREFERENCE_RESTORE_CHANGED")

    part_1 = importlib.import_module(
        "kanda_reasoner_app.reasoner_runtime_collector.runtime_runner_help."
        "_runtime_runner_part_1_bindings"
    )
    part_2 = importlib.import_module(
        "kanda_reasoner_app.reasoner_runtime_collector.runtime_runner_help."
        "_runtime_runner_part_2_bindings"
    )
    bindings_1 = part_1.build_default_runtime_bindings()
    bindings_2 = part_2.build_default_runtime_bindings()
    if not callable(bindings_1.trace_event):
        raise AssertionError("PART1_TRACE_EVENT_BINDING_CHANGED")
    if not callable(bindings_1.trace_state_snapshot):
        raise AssertionError("PART1_TRACE_STATE_BINDING_CHANGED")
    if not callable(bindings_2.configure_runtime_trace):
        raise AssertionError("PART2_CONFIGURE_TRACE_BINDING_CHANGED")
    if not callable(bindings_2.trace_signal_connection):
        raise AssertionError("PART2_TRACE_SIGNAL_BINDING_CHANGED")

    scenarios = importlib.import_module(
        "kanda_reasoner_app.reasoner_runtime_collector.runtime_runner_help."
        "_runtime_runner_part_2_scenarios"
    )
    window = importlib.import_module(
        "kanda_reasoner_app.reasoner_runtime_collector.runtime_runner_help."
        "_runtime_runner_part_2_window"
    )
    if not callable(scenarios.Slot) or not callable(window.Slot):
        raise AssertionError("QT_SLOT_COMPATIBILITY_CHANGED")

    facade = importlib.import_module(
        "kanda_reasoner_app.manage_architecture.large_file_refactor_planner."
        "cst_facade_global_import_inserter"
    )
    preview = importlib.import_module(
        "kanda_reasoner_app.manage_architecture.large_file_refactor_planner."
        "cst_real_preview_writer"
    )
    if not hasattr(facade, "cst"):
        raise AssertionError("CST_COMPATIBILITY_NAME_MISSING")
    if not callable(preview.is_libcst_available):
        raise AssertionError("LIBCST_AVAILABILITY_ALIAS_MISSING")

    print("PUBLIC_CONTRACT_RUNTIME_SMOKE: PASS")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--patch-zip", required=True)
    args = parser.parse_args()

    project_root = Path(args.project_root).resolve(strict=True)
    patch_zip = Path(args.patch_zip).resolve(strict=True)
    root_text = str(project_root)
    if root_text not in sys.path:
        sys.path.insert(0, root_text)

    hint = _validate_zip(project_root, patch_zip)
    payload_files = tuple(hint.get("validated_files") or ())
    _validate_python(project_root, payload_files)
    _validate_strict_detector_source(project_root)
    _validate_dynamic_event_contract(project_root)
    if (project_root / STALE_VALIDATOR).exists():
        raise AssertionError("STALE_PRECISION_VALIDATOR_REMAINS")
    print("STALE_PRECISION_VALIDATOR_REMOVED: PASS")
    _validate_live_strict_target_scan(project_root)
    _validate_runtime_smoke(project_root)
    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
