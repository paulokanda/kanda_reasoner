# project-path: tools/engineering_diagnostics_wave2oa_public_boundary_gate.py
"""Public-boundary gate for Engineering Diagnostics Wave 2O-A."""

from __future__ import annotations

import ast
from pathlib import Path
import warnings

__all__ = ["validate_engineering_diagnostics_wave2oa_public_boundary"]

_PACKAGE_ROOT = Path("kanda_reasoner_app/engineering_diagnostics")
_PUBLIC_FACADE = _PACKAGE_ROOT / "__init__.py"
_PRIVATE_MODULES = frozenset({"_store_database", "_store_baseline_ops"})
_EXTERNAL_SCAN_EXCLUDED_PARTS = frozenset(
    {
        "snippets",
        "project_reference",
        "project_references",
    }
)
_FORBIDDEN_IMPORT_PREFIXES = (
    "kanda_reasoner_app.engineering_safety",
    "kanda_reasoner_app.source_hygiene",
    "kanda_reasoner_app.reasoner_symbol_atlas",
    "kanda_reasoner_app.manage_architecture",
    "kanda_reasoner_app.freeze_hint_intake",
    "kanda_reasoner_app.error_memory",
)


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def _module_name(path: Path, root: Path) -> str:
    relative = path.relative_to(root).with_suffix("")
    return ".".join(relative.parts)


def _imports(tree: ast.AST) -> tuple[str, ...]:
    names: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            names.append(node.module or "")
    return tuple(names)


def _all_values(tree: ast.Module) -> tuple[str, ...] | None:
    for statement in tree.body:
        if not isinstance(statement, (ast.Assign, ast.AnnAssign)):
            continue
        targets = (
            statement.targets
            if isinstance(statement, ast.Assign)
            else [statement.target]
        )
        if not any(
            isinstance(target, ast.Name) and target.id == "__all__"
            for target in targets
        ):
            continue
        value = statement.value
        if not isinstance(value, (ast.List, ast.Tuple)):
            return None
        result: list[str] = []
        for item in value.elts:
            if not isinstance(item, ast.Constant) or not isinstance(item.value, str):
                return None
            result.append(item.value)
        return tuple(result)
    return None


def _external_scan_excluded(path: Path, root: Path) -> bool:
    try:
        relative = path.relative_to(root)
    except ValueError:
        return True
    return any(part.lower() in _EXTERNAL_SCAN_EXCLUDED_PARTS for part in relative.parts)


def _parse_external_scan_source(source: str, path: Path) -> ast.Module:
    """Parse unrelated source without leaking noisy SyntaxWarning output."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", SyntaxWarning)
        return ast.parse(source, filename=str(path))


def _check_package_modules(root: Path) -> None:
    package = root / _PACKAGE_ROOT
    _require(package.is_dir(), "ENGINEERING_DIAGNOSTICS_PACKAGE_MISSING")
    for path in sorted(package.glob("*.py")):
        source = path.read_text(encoding="utf-8")
        _require(source.isascii(), "NON_ASCII_SOURCE:" + str(path.relative_to(root)))
        _require(
            len(source.splitlines()) <= 500,
            "MODULE_SIZE_LIMIT_EXCEEDED:" + str(path.relative_to(root)),
        )
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
        _require(
            not forbidden,
            "CROSS_BOX_PRIVATE_OR_DIRECT_IMPORT:" + repr(forbidden),
        )
        if path.stem in _PRIVATE_MODULES:
            _require(
                _all_values(tree) == (),
                "PRIVATE_MODULE_EXPORTS_PUBLIC_API:" + path.stem,
            )
    print("ENGINEERING DIAGNOSTICS MODULE SIZE MAXIMUM 500: PASS")
    print("ENGINEERING DIAGNOSTICS CROSS-BOX DIRECT IMPORTS: 0")


def _check_public_facade(root: Path) -> None:
    path = root / _PUBLIC_FACADE
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(path))
    exported = _all_values(tree)
    _require(
        exported is not None and len(exported) == len(set(exported)),
        "PUBLIC_FACADE_EXPORTS_INVALID",
    )
    _require("EngineeringDiagnosticsStore" in exported, "STORE_NOT_EXPORTED")
    _require("build_bom_diagnostic_run" in exported, "BOM_ADAPTER_NOT_EXPORTED")
    _require(not any(name.startswith("_") for name in exported), "PRIVATE_NAME_EXPORTED")
    print("ENGINEERING DIAGNOSTICS PUBLIC FACADE: PASS")
    print("ENGINEERING DIAGNOSTICS PRIVATE EXPORTS: 0")


def _check_external_private_reach_in(root: Path) -> None:
    package = (root / _PACKAGE_ROOT).resolve(strict=False)
    findings: list[str] = []
    for path in root.rglob("*.py"):
        resolved = path.resolve(strict=False)
        try:
            resolved.relative_to(package)
        except ValueError:
            pass
        else:
            continue
        if _external_scan_excluded(path, root):
            continue
        source = path.read_text(encoding="utf-8", errors="replace")
        try:
            tree = _parse_external_scan_source(source, path)
        except SyntaxError:
            continue
        for imported in _imports(tree):
            if any(
                imported == "kanda_reasoner_app.engineering_diagnostics." + name
                or imported.startswith(
                    "kanda_reasoner_app.engineering_diagnostics." + name + "."
                )
                for name in _PRIVATE_MODULES
            ):
                findings.append(str(path.relative_to(root)) + " -> " + imported)
    _require(not findings, "ENGINEERING_DIAGNOSTICS_PRIVATE_REACH_IN:" + repr(findings))
    print("ENGINEERING DIAGNOSTICS EXTERNAL PRIVATE REACH-IN: 0")


def _check_tests_use_public_contract(root: Path) -> None:
    test_path = root / "tests/test_engineering_diagnostics_wave2oa.py"
    _require(test_path.is_file(), "ENGINEERING_DIAGNOSTICS_FOCUSED_TEST_MISSING")
    source = test_path.read_text(encoding="utf-8")
    _require(
        "from kanda_reasoner_app.engineering_diagnostics import" in source,
        "FOCUSED_TEST_DOES_NOT_USE_PUBLIC_FACADE",
    )
    _require(
        "engineering_diagnostics._store" not in source,
        "FOCUSED_TEST_PRIVATE_REACH_IN",
    )
    print("ENGINEERING DIAGNOSTICS TEST PUBLIC CONTRACT: PASS")


def validate_engineering_diagnostics_wave2oa_public_boundary(root: Path) -> None:
    """Validate one owner-pure backend package without another Box touch."""
    project_root = Path(root).expanduser().resolve(strict=False)
    _check_package_modules(project_root)
    _check_public_facade(project_root)
    _check_external_private_reach_in(project_root)
    _check_tests_use_public_contract(project_root)
    print("ENGINEERING DIAGNOSTICS PUBLIC-CONTRACT-ONLY COMMUNICATION: PASS")
