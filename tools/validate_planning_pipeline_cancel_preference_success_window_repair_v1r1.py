# project-path: tools/validate_planning_pipeline_cancel_preference_success_window_repair_v1r1.py
"""Validate the Planner docstring-path symbol repair and prior v1 contracts."""

from __future__ import annotations

import argparse
import ast
import builtins
import hashlib
import importlib.util
import json
import symtable
import zipfile
from pathlib import Path, PurePosixPath
from types import SimpleNamespace
from typing import Any

FEATURE_ID = "planning-pipeline-cancel-preference-success-window-repair-v1r1"
PREDECESSOR_FEATURE_ID = "planning-pipeline-cancel-preference-success-window-repair-v1"
PLANNER_BOX = Path(
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner"
)
SHELL = PLANNER_BOX / "gui_shell.py"
PREDECESSOR_VALIDATOR = (
    Path("tools")
    / "validate_planning_pipeline_cancel_preference_success_window_repair_v1.py"
)
VALIDATOR = Path("tools") / Path(__file__).name
EXPECTED_PAYLOAD = {SHELL, VALIDATOR}
EXPECTED_ROOT_FILES = {
    "INSTALL.ps1",
    "KANDA_FREEZE_HINT.json",
    "PATCH_MANIFEST.json",
    "README.txt",
    "VALIDATE.ps1",
}
EXPECTED_PREDECESSOR_SHELL_SHA256 = (
    "638009fe9504e6081f96c1e6d5bbb59ccd2b4a2220d167b4143d9d11b82cf36c"
)
REQUIRED_HINT_FIELDS = {
    "schema_version",
    "kind",
    "patch_name",
    "feature_id",
    "feature_title",
    "primary_box",
    "box_type",
    "validated_files",
    "generated_files",
    "protected_paths",
    "do_not_regress_rules",
    "validation_evidence_summary",
    "known_warnings",
    "planned_next_step",
    "notes",
}


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit("VALIDATION ERROR: " + message)


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _read(project_root: Path, relative_path: Path) -> str:
    return (project_root / relative_path).read_text(encoding="utf-8")


def _load_predecessor_validator(project_root: Path) -> Any:
    path = project_root / PREDECESSOR_VALIDATOR
    _assert(path.is_file(), "predecessor validator is missing")
    spec = importlib.util.spec_from_file_location("planner_repair_v1", path)
    _assert(spec is not None and spec.loader is not None, "cannot load predecessor validator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _validate_predecessor_contracts(project_root: Path) -> None:
    module = _load_predecessor_validator(project_root)
    module._validate_success_window_import(project_root)
    module._validate_selector_contract(project_root)
    module._validate_lifecycle_contract(project_root)
    module._validate_shell_contract(project_root)
    module._validate_cancel_runtime(project_root)
    module._validate_lifecycle_runtime(project_root)
    module._validate_preference_sessions(project_root)
    print("PREDECESSOR_V1_RUNTIME_CONTRACTS: PASS")


def _module_bound_names(table: symtable.SymbolTable) -> set[str]:
    return {
        symbol.get_name()
        for symbol in table.get_symbols()
        if symbol.is_imported()
        or symbol.is_assigned()
        or symbol.is_namespace()
        or symbol.is_parameter()
    }


def _referenced_unbound_globals(source: str, filename: str) -> list[tuple[str, str]]:
    table = symtable.symtable(source, filename, "exec")
    module_bound = _module_bound_names(table)
    missing: set[tuple[str, str]] = set()

    def walk(current: symtable.SymbolTable) -> None:
        for symbol in current.get_symbols():
            name = symbol.get_name()
            if (
                symbol.is_referenced()
                and symbol.is_global()
                and name not in module_bound
                and not hasattr(builtins, name)
            ):
                missing.add((current.get_name(), name))
        for child in current.get_children():
            walk(child)

    walk(table)
    return sorted(missing)


def _validate_shell_symbol_resolution(project_root: Path) -> None:
    source = _read(project_root, SHELL)
    tree = ast.parse(source, filename=str(SHELL))
    imports: set[str] = set()
    for node in tree.body:
        if isinstance(node, ast.ImportFrom) and node.module == "planner_bounded_refinement":
            imports.update(alias.name for alias in node.names)
    _assert(
        "plan_allows_ai_architecture_correction" in imports,
        "gui_shell does not import plan_allows_ai_architecture_correction",
    )
    missing = _referenced_unbound_globals(source, str(SHELL))
    _assert(not missing, "unresolved gui_shell globals: " + repr(missing))
    print("PLANNER_GUI_SHELL_GLOBAL_SYMBOL_RESOLUTION: PASS")
    print("DOCSTRING_PLAN_AI_CORRECTION_GUARD_IMPORT: PASS")


def _extract_function(source: str, name: str, filename: str) -> Any:
    tree = ast.parse(source, filename=filename)
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == name:
            module = ast.Module(body=[node], type_ignores=[])
            ast.fix_missing_locations(module)
            return compile(module, filename, "exec")
    raise SystemExit("VALIDATION ERROR: function not found: " + name)


class _FakeOutput:
    def __init__(self) -> None:
        self.text = ""

    def setPlainText(self, text: str) -> None:
        self.text = text


def _validate_docstring_plan_runtime(project_root: Path) -> None:
    source = _read(project_root, SHELL)
    code = _extract_function(source, "_generate_docstring_plan", str(SHELL))
    calls: list[str] = []
    plan = SimpleNamespace(status="ready")
    bundle = SimpleNamespace(plan=plan, docstring_proposals=[])
    namespace: dict[str, Any] = {
        "__name__": "planner_gui_shell_docstring_validation",
        "get_planner_version_bundle": lambda _window, _route: bundle,
        "PLANNER_VERSION_HEURISTIC": "heuristic",
        "build_docstring_proposals": lambda _report, _plan: ["proposal"],
        "attach_docstring_proposals_to_plan": lambda current, _items: current,
        "store_heuristic_version": lambda _window, _plan, _items: calls.append("store"),
        "refresh_planner_version_selector": lambda _window: calls.append("refresh"),
        "format_split_plan": lambda _plan: "PLAN",
        "format_docstring_proposals": lambda _items: "DOCSTRINGS",
        "PlannerState": SimpleNamespace(
            DOCSTRING_READY=SimpleNamespace(value="docstring_ready"),
            BLOCKED=SimpleNamespace(value="blocked"),
        ),
        "plan_allows_ai_architecture_correction": lambda _plan: calls.append("guard") or True,
        "_update_status": lambda _window: calls.append("status"),
    }
    exec(code, namespace)
    window = SimpleNamespace(
        _large_file_refactor_last_analysis=SimpleNamespace(),
        _large_file_refactor_plan_output=_FakeOutput(),
    )
    namespace["_generate_docstring_plan"](window)
    _assert("guard" in calls, "docstring path did not call the AI correction guard")
    _assert("store" in calls and "refresh" in calls, "docstring state was not stored/refreshed")
    _assert("status" in calls, "docstring path did not refresh status")
    _assert(
        window._large_file_refactor_planner_state == "docstring_ready",
        "docstring path did not project ready state",
    )
    _assert(window._large_file_refactor_plan_output.text == "PLAN\n\nDOCSTRINGS", "output changed")
    print("DOCSTRING_PLAN_RUNTIME_PATH: PASS")
    print("DOCSTRING_PLAN_NAMEERROR_REGRESSION: PASS")


def _validate_source_health(project_root: Path) -> None:
    for relative_path in EXPECTED_PAYLOAD:
        path = project_root / relative_path
        _assert(path.is_file(), "missing installed file: " + str(relative_path))
        raw = path.read_bytes()
        _assert(not raw.startswith(b"\xef\xbb\xbf"), "UTF-8 BOM: " + str(relative_path))
        raw.decode("ascii")
        compile(raw, str(relative_path), "exec")
        _assert(len(raw.splitlines()) <= 500, "module exceeds 500 lines: " + str(relative_path))
    print("PYTHON_SYNTAX: PASS")
    print("SOURCE_ASCII_UTF8_NO_BOM: PASS")
    print("TOUCHED_MODULES_MAX_500_LINES: PASS")


def _validate_zip_contract(project_root: Path, patch_zip: Path) -> None:
    _assert(patch_zip.is_file(), "patch ZIP not found: " + str(patch_zip))
    with zipfile.ZipFile(patch_zip) as archive:
        names = archive.namelist()
        _assert(len(names) == len(set(names)), "duplicate ZIP members")
        for name in names:
            path = PurePosixPath(name)
            _assert(not path.is_absolute(), "absolute ZIP member: " + name)
            _assert(".." not in path.parts, "path traversal ZIP member: " + name)
        root_files = {name for name in names if "/" not in name and not name.endswith("/")}
        _assert(EXPECTED_ROOT_FILES.issubset(root_files), "required root files missing")
        _assert("payload/KANDA_FREEZE_HINT.json" not in names, "freeze hint duplicated")
        payload_paths = {
            Path(name.removeprefix("payload/"))
            for name in names
            if name.startswith("payload/")
            and not name.endswith("/")
            and not name.startswith("payload/error_memory_receive_blocks/")
        }
        _assert(payload_paths == EXPECTED_PAYLOAD, "unexpected payload file set")
        manifest = json.loads(archive.read("PATCH_MANIFEST.json").decode("utf-8"))
        _assert(manifest.get("feature_id") == FEATURE_ID, "manifest feature ID mismatch")
        entries = manifest.get("files", [])
        by_path = {Path(item["path"]): item for item in entries}
        _assert(set(by_path) == EXPECTED_PAYLOAD, "manifest file set mismatch")
        shell_entry = by_path[SHELL]
        _assert(
            shell_entry.get("expected_old_sha256") == EXPECTED_PREDECESSOR_SHELL_SHA256,
            "predecessor shell hash guard changed",
        )
        for relative_path, item in by_path.items():
            payload = archive.read("payload/" + relative_path.as_posix())
            _assert(_sha256(payload) == item.get("new_sha256"), "payload hash mismatch")
            installed = (project_root / relative_path).read_bytes()
            _assert(_sha256(installed) == item.get("new_sha256"), "installed file out of sync")
        hint = json.loads(archive.read("KANDA_FREEZE_HINT.json").decode("utf-8"))
        _assert(REQUIRED_HINT_FIELDS.issubset(hint), "freeze hint fields missing")
        _assert(hint.get("feature_id") == FEATURE_ID, "freeze hint feature ID mismatch")
        for field in ("validated_files", "generated_files", "protected_paths", "do_not_regress_rules"):
            _assert(isinstance(hint.get(field), list), "freeze hint list field invalid: " + field)
        error_blocks = [
            name
            for name in names
            if name.startswith("payload/error_memory_receive_blocks/")
            and not name.endswith("/")
        ]
        _assert(len(error_blocks) == 2, "Error Memory intake pair missing")
    print("PATCH_ZIP_CONTRACT: PASS")
    print("KANDA_FREEZE_HINT_ROOT_ONLY: PASS")
    print("ERROR_MEMORY_INTAKE_PAIR: PASS")


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--patch-zip", required=True)
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    project_root = Path(args.project_root).resolve()
    patch_zip = Path(args.patch_zip).resolve()
    _validate_predecessor_contracts(project_root)
    _validate_shell_symbol_resolution(project_root)
    _validate_docstring_plan_runtime(project_root)
    _validate_source_health(project_root)
    _validate_zip_contract(project_root, patch_zip)
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")


if __name__ == "__main__":
    main()
