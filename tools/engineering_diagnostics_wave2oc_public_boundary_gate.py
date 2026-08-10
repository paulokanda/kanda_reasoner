# project-path: tools/engineering_diagnostics_wave2oc_public_boundary_gate.py
"""Public-boundary and non-mutation gate for Engineering Diagnostics Wave 2O-C."""

from __future__ import annotations

import ast
from pathlib import Path

__all__ = ["validate_engineering_diagnostics_wave2oc_public_boundary"]

_RUFF_ROOTS = (
    Path("kanda_reasoner_app/engineering_diagnostics/collectors"),
    Path("kanda_reasoner_app/engineering_diagnostics/rules"),
)
_CHANGED_MODULES = (
    Path("kanda_reasoner_app/engineering_diagnostics/__init__.py"),
    Path("kanda_reasoner_app/engineering_diagnostics/_store_baseline_ops.py"),
    Path("kanda_reasoner_app/engineering_diagnostics/fingerprinting.py"),
    Path("kanda_reasoner_app/engineering_diagnostics_gui/controller.py"),
    Path("kanda_reasoner_app/engineering_diagnostics_gui/diagnostic_table_model.py"),
    Path("kanda_reasoner_app/engineering_diagnostics_gui/engineering_diagnostics_tab.py"),
)
_FORBIDDEN_IMPORT_PREFIXES = (
    "kanda_reasoner_app.source_hygiene",
    "kanda_reasoner_app.engineering_safety",
    "kanda_reasoner_app.error_memory",
    "kanda_reasoner_app.freeze_hint_intake",
    "kanda_reasoner_app.manage_architecture",
    "kanda_reasoner_app.reasoner_symbol_atlas",
)


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def _imports(tree: ast.AST) -> tuple[str, ...]:
    values: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            values.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            values.append(node.module or "")
    return tuple(values)


def _all_values(tree: ast.Module) -> tuple[str, ...] | None:
    for node in tree.body:
        if not isinstance(node, (ast.Assign, ast.AnnAssign)):
            continue
        targets = node.targets if isinstance(node, ast.Assign) else [node.target]
        if not any(isinstance(item, ast.Name) and item.id == "__all__" for item in targets):
            continue
        value = node.value
        if not isinstance(value, (ast.List, ast.Tuple)):
            return None
        output: list[str] = []
        for item in value.elts:
            if not isinstance(item, ast.Constant) or not isinstance(item.value, str):
                return None
            output.append(item.value)
        return tuple(output)
    return None


def _python_files(root: Path) -> tuple[Path, ...]:
    files: list[Path] = []
    for relative in _RUFF_ROOTS:
        files.extend(sorted((root / relative).glob("*.py")))
    files.extend(root / relative for relative in _CHANGED_MODULES)
    return tuple(files)


def _check_modules(root: Path) -> None:
    for path in _python_files(root):
        _require(path.is_file(), "WAVE2OC_MODULE_MISSING:" + path.as_posix())
        source = path.read_text(encoding="utf-8")
        relative = path.relative_to(root).as_posix()
        _require(source.isascii(), "NON_ASCII_SOURCE:" + relative)
        _require(len(source.splitlines()) <= 500, "MODULE_SIZE_LIMIT_EXCEEDED:" + relative)
        tree = ast.parse(source, filename=str(path))
        compile(source, str(path), "exec")
        imported = _imports(tree)
        forbidden = sorted(
            name
            for name in imported
            if any(
                name == prefix or name.startswith(prefix + ".")
                for prefix in _FORBIDDEN_IMPORT_PREFIXES
            )
        )
        _require(not forbidden, "WAVE2OC_FORBIDDEN_IMPORTS:" + relative + ":" + repr(forbidden))
        direct_sqlite_forbidden = (
            "/collectors/" in "/" + relative
            or "/rules/" in "/" + relative
            or "engineering_diagnostics_gui/" in relative
        )
        if direct_sqlite_forbidden:
            _require("sqlite3" not in imported, "WAVE2OC_DIRECT_SQLITE_ACCESS:" + relative)
    print("WAVE2OC MODULE SIZE MAXIMUM 500: PASS")
    print("WAVE2OC SOURCE HYGIENE PRIVATE IMPORTS: 0")
    print("WAVE2OC ENGINEERING SAFETY PRIVATE IMPORTS: 0")
    print("WAVE2OC DIRECT SQLITE ACCESS: 0")


def _check_non_mutation(root: Path) -> None:
    collector = root / "kanda_reasoner_app/engineering_diagnostics/collectors/ruff_collector.py"
    source = collector.read_text(encoding="utf-8")
    _require('"--output-format"' in source and '"json"' in source, "RUFF_NATIVE_JSON_COMMAND_MISSING")
    _require('"--no-fix"' in source, "RUFF_NO_FIX_GUARD_MISSING")
    _require('"--fix"' not in source, "RUFF_FIX_EXECUTION_FLAG_PRESENT")
    forbidden_calls = ("write_text(", "write_bytes(", "unlink(", "rename(")
    _require(
        not any(token in source for token in forbidden_calls),
        "RUFF_COLLECTOR_SOURCE_MUTATION_CALL_PRESENT",
    )
    print("RUFF MACHINE-READABLE JSON ONLY: PASS")
    print("RUFF FIX EXECUTION: 0")
    print("RUFF PROJECT SOURCE MUTATION CALLS: 0")


def _check_public_facade(root: Path) -> None:
    path = root / "kanda_reasoner_app/engineering_diagnostics/__init__.py"
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    exported = _all_values(tree)
    _require(exported is not None, "ENGINEERING_DIAGNOSTICS_PUBLIC_FACADE_MISSING")
    _require(len(exported) == len(set(exported)), "ENGINEERING_DIAGNOSTICS_DUPLICATE_EXPORT")
    required = {
        "BOM_PRODUCER_ID",
        "EngineeringDiagnosticsStore",
        "RUFF_PRODUCER_ID",
        "RuffCollectionResult",
        "build_ruff_diagnostic_run",
        "collect_ruff_json",
        "ruff_rule_profile",
    }
    _require(required.issubset(set(exported)), "WAVE2OC_PUBLIC_EXPORT_MISSING")
    _require(not any(name.startswith("_") for name in exported), "WAVE2OC_PRIVATE_EXPORT")
    print("WAVE2OC ENGINEERING DIAGNOSTICS PUBLIC FACADE: PASS")


def _check_gui_consumer(root: Path) -> None:
    controller = root / "kanda_reasoner_app/engineering_diagnostics_gui/controller.py"
    tree = ast.parse(controller.read_text(encoding="utf-8"), filename=str(controller))
    imports = _imports(tree)
    _require(
        not any(name.startswith("kanda_reasoner_app.engineering_diagnostics.") for name in imports),
        "WAVE2OC_GUI_BACKEND_SUBMODULE_REACH_IN",
    )
    tab = (root / "kanda_reasoner_app/engineering_diagnostics_gui/engineering_diagnostics_tab.py").read_text(encoding="utf-8")
    _require("collect_ruff_candidate" in tab, "WAVE2OC_GUI_RUFF_WORKER_ROUTE_MISSING")
    _require("ThreadPoolExecutor" in tab, "WAVE2OC_GUI_BACKGROUND_EXECUTOR_MISSING")
    _require("RUFF_PRODUCER_ID" in tab, "WAVE2OC_GUI_RUFF_SELECTOR_MISSING")
    print("WAVE2OC GUI PUBLIC BACKEND CONTRACT: PASS")
    print("WAVE2OC GUI BACKEND PRIVATE REACH-IN: 0")
    print("WAVE2OC GUI BACKGROUND COLLECTION: PASS")


def _check_tests(root: Path) -> None:
    path = root / "tests/test_engineering_diagnostics_wave2oc.py"
    _require(path.is_file(), "WAVE2OC_TEST_MISSING")
    source = path.read_text(encoding="utf-8")
    _require("from kanda_reasoner_app.engineering_diagnostics import" in source, "WAVE2OC_TEST_NOT_PUBLIC_BACKEND")
    _require("from kanda_reasoner_app.engineering_diagnostics_gui import" in source, "WAVE2OC_TEST_NOT_PUBLIC_GUI")
    tree = ast.parse(source, filename=str(path))
    imports = _imports(tree)
    _require(
        not any(name.startswith("kanda_reasoner_app.engineering_diagnostics.") for name in imports),
        "WAVE2OC_TEST_BACKEND_PRIVATE_REACH_IN",
    )
    _require(
        not any(name.startswith("kanda_reasoner_app.engineering_diagnostics_gui.") for name in imports),
        "WAVE2OC_TEST_GUI_PRIVATE_REACH_IN",
    )
    print("WAVE2OC TEST PUBLIC CONTRACT: PASS")


def validate_engineering_diagnostics_wave2oc_public_boundary(root: Path) -> None:
    """Validate owner purity, public communication, and read-only Ruff behavior."""
    project_root = Path(root).expanduser().resolve(strict=False)
    _check_modules(project_root)
    _check_non_mutation(project_root)
    _check_public_facade(project_root)
    _check_gui_consumer(project_root)
    _check_tests(project_root)
    print("WAVE2OC PUBLIC-CONTRACT-ONLY COMMUNICATION: PASS")
