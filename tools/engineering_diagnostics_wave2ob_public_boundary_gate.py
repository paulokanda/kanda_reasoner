# project-path: tools/engineering_diagnostics_wave2ob_public_boundary_gate.py
"""Public-boundary gate for Engineering Diagnostics GUI Wave 2O-B."""

from __future__ import annotations

import ast
from pathlib import Path

__all__ = ["validate_engineering_diagnostics_wave2ob_public_boundary"]

_GUI_ROOT = Path("kanda_reasoner_app/engineering_diagnostics_gui")
_HOST_HELPER = Path(
    "kanda_reasoner_app/manage_architecture/audit_project_sibling_tabs.py"
)
_FORBIDDEN_IMPORTS = (
    "sqlite3",
    "kanda_reasoner_app.engineering_diagnostics._store_database",
    "kanda_reasoner_app.engineering_diagnostics._store_baseline_ops",
    "kanda_reasoner_app.source_hygiene",
    "kanda_reasoner_app.error_memory",
    "kanda_reasoner_app.freeze_hint_intake",
)


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def _imports(tree: ast.AST) -> tuple[str, ...]:
    found: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            found.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            found.append(node.module or "")
    return tuple(found)


def _all_values(tree: ast.Module) -> tuple[str, ...] | None:
    for node in tree.body:
        if not isinstance(node, (ast.Assign, ast.AnnAssign)):
            continue
        targets = node.targets if isinstance(node, ast.Assign) else [node.target]
        if not any(
            isinstance(target, ast.Name) and target.id == "__all__"
            for target in targets
        ):
            continue
        value = node.value
        if not isinstance(value, (ast.List, ast.Tuple)):
            return None
        values: list[str] = []
        for item in value.elts:
            if not isinstance(item, ast.Constant) or not isinstance(item.value, str):
                return None
            values.append(item.value)
        return tuple(values)
    return None


def _check_gui_modules(root: Path) -> None:
    package = root / _GUI_ROOT
    _require(package.is_dir(), "ENGINEERING_DIAGNOSTICS_GUI_PACKAGE_MISSING")
    for path in sorted(package.glob("*.py")):
        source = path.read_text(encoding="utf-8")
        relative = path.relative_to(root).as_posix()
        _require(source.isascii(), "NON_ASCII_SOURCE:" + relative)
        _require(
            len(source.splitlines()) <= 500,
            "MODULE_SIZE_LIMIT_EXCEEDED:" + relative,
        )
        tree = ast.parse(source, filename=str(path))
        compile(source, str(path), "exec")
        imports = _imports(tree)
        forbidden = sorted(
            name
            for name in imports
            if any(
                name == prefix or name.startswith(prefix + ".")
                for prefix in _FORBIDDEN_IMPORTS
            )
        )
        _require(not forbidden, "GUI_FORBIDDEN_IMPORTS:" + repr(forbidden))
        _require(
            not any(
                name.startswith("kanda_reasoner_app.engineering_diagnostics.")
                for name in imports
            ),
            "GUI_BACKEND_SUBMODULE_REACH_IN:" + relative,
        )
    print("ENGINEERING DIAGNOSTICS GUI MODULE SIZE MAXIMUM 500: PASS")
    print("ENGINEERING DIAGNOSTICS GUI DIRECT SQLITE ACCESS: 0")
    print("ENGINEERING DIAGNOSTICS GUI BACKEND PRIVATE REACH-IN: 0")
    print("ENGINEERING DIAGNOSTICS GUI SOURCE HYGIENE IMPORTS: 0")


def _check_public_facade(root: Path) -> None:
    path = root / _GUI_ROOT / "__init__.py"
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    exported = _all_values(tree)
    _require(exported is not None, "ENGINEERING_DIAGNOSTICS_GUI_PUBLIC_FACADE_MISSING")
    _require(len(exported) == len(set(exported)), "GUI_DUPLICATE_PUBLIC_EXPORT")
    _require(
        "create_engineering_diagnostics_panel" in exported,
        "GUI_PANEL_FACTORY_NOT_EXPORTED",
    )
    _require(
        "EngineeringDiagnosticsController" in exported,
        "GUI_CONTROLLER_NOT_EXPORTED",
    )
    _require(not any(name.startswith("_") for name in exported), "GUI_PRIVATE_EXPORT")
    print("ENGINEERING DIAGNOSTICS GUI PUBLIC FACADE: PASS")


def _check_host(root: Path) -> None:
    helper = root / _HOST_HELPER
    _require(helper.is_file(), "AUDIT_PROJECT_SIBLING_TAB_HELPER_MISSING")
    source = helper.read_text(encoding="utf-8")
    _require(
        '"kanda_reasoner_app.engineering_diagnostics_gui"' in source,
        "AUDIT_PROJECT_GUI_PUBLIC_PACKAGE_IMPORT_MISSING",
    )
    _require(
        '"create_engineering_diagnostics_panel"' in source,
        "AUDIT_PROJECT_GUI_PUBLIC_FACTORY_MISSING",
    )
    _require(
        "engineering_diagnostics_gui." not in source,
        "AUDIT_PROJECT_GUI_SUBMODULE_REACH_IN",
    )
    print("AUDIT PROJECT ENGINEERING DIAGNOSTICS PUBLIC HOST CONTRACT: PASS")


def _check_tests(root: Path) -> None:
    path = root / "tests/test_engineering_diagnostics_wave2ob.py"
    _require(path.is_file(), "ENGINEERING_DIAGNOSTICS_GUI_TEST_MISSING")
    source = path.read_text(encoding="utf-8")
    _require(
        "from kanda_reasoner_app.engineering_diagnostics_gui import" in source,
        "GUI_TEST_NOT_USING_PUBLIC_FACADE",
    )
    tree = ast.parse(source, filename=str(path))
    _require(
        not any(
            name.startswith(
                "kanda_reasoner_app.engineering_diagnostics_gui."
            )
            for name in _imports(tree)
        ),
        "GUI_TEST_PRIVATE_REACH_IN",
    )
    print("ENGINEERING DIAGNOSTICS GUI TEST PUBLIC CONTRACT: PASS")


def validate_engineering_diagnostics_wave2ob_public_boundary(root: Path) -> None:
    """Validate GUI ownership without importing private backend implementations."""
    project_root = Path(root).expanduser().resolve(strict=False)
    _check_gui_modules(project_root)
    _check_public_facade(project_root)
    _check_host(project_root)
    _check_tests(project_root)
    print("ENGINEERING DIAGNOSTICS GUI PUBLIC-CONTRACT-ONLY COMMUNICATION: PASS")
