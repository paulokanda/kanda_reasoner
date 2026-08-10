"""Public-boundary gate for Symbol Atlas active-owner filtering wave 2N."""

from __future__ import annotations

import ast
from pathlib import Path

__all__ = ["validate_wave2n_public_boundary"]

_PRIVATE_MODULES = (
    (
        "kanda_reasoner_app.reasoner_symbol_atlas."
        "existing_code_finder_matching_private"
    ),
    (
        "kanda_reasoner_app.reasoner_symbol_atlas."
        "facade_owner_resolver_helpers_private"
    ),
)
_PRIVATE_TOKENS = tuple(name.rsplit(".", 1)[-1] for name in _PRIVATE_MODULES)
_PRIVATE_PATHS = (
    (
        "kanda_reasoner_app/reasoner_symbol_atlas/"
        "existing_code_finder_matching_private.py"
    ),
    (
        "kanda_reasoner_app/reasoner_symbol_atlas/"
        "facade_owner_resolver_helpers_private.py"
    ),
)
_CANONICAL_VALIDATOR_RELATIVE = (
    "tools/validate_reasoner_symbol_atlas_active_owner_filtering_wave2n_v1r2.py"
)
_CANONICAL_VALIDATOR_MODULE = (
    "validate_reasoner_symbol_atlas_active_owner_filtering_wave2n_v1r2"
)
_OPTIONAL_VALIDATOR_GLOB = (
    "validate_reasoner_symbol_atlas_active_owner_filtering_wave2n_v1*.py"
)
_FORBIDDEN_STATE_NAMES = frozenset(
    {
        "TARGET_HASHES",
        "TARGET_MODULES",
        "TARGET_SOURCE_PATHS",
        "WAVE2M_PROTECTED_HASHES",
    }
)


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def _is_private_module(module_name: str) -> bool:
    return any(
        module_name == private_name
        or module_name.startswith(private_name + ".")
        for private_name in _PRIVATE_MODULES
    )


def _imported_names(node: ast.AST) -> tuple[str, ...]:
    if isinstance(node, ast.Import):
        return tuple(alias.name for alias in node.names)
    if isinstance(node, ast.ImportFrom):
        base = node.module or ""
        return tuple(
            base + "." + alias.name if base else alias.name
            for alias in node.names
        )
    return ()


def _assigned_names(tree: ast.Module) -> frozenset[str]:
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            targets = list(node.targets)
        elif isinstance(node, ast.AnnAssign):
            targets = [node.target]
        else:
            continue
        for target in targets:
            if isinstance(target, ast.Name):
                names.add(target.id)
    return frozenset(names)


def _forbidden_references(path: Path, source: str) -> tuple[str, ...]:
    tree = ast.parse(source, filename=str(path))
    findings: list[str] = []
    for node in ast.walk(tree):
        for imported_name in _imported_names(node):
            if _is_private_module(imported_name):
                findings.append("import:" + imported_name)
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            if _is_private_module(node.value):
                findings.append("string:" + node.value)
    return tuple(sorted(set(findings)))


def _empty_all_contract(tree: ast.Module) -> bool:
    for statement in tree.body:
        if not isinstance(statement, (ast.Assign, ast.AnnAssign)):
            continue
        if isinstance(statement, ast.Assign):
            targets = list(statement.targets)
            value = statement.value
        else:
            targets = [statement.target]
            value = statement.value
        if not any(
            isinstance(target, ast.Name) and target.id == "__all__"
            for target in targets
        ):
            continue
        return isinstance(value, (ast.List, ast.Tuple)) and not value.elts
    return False


def _check_private_structural_contract(root: Path) -> None:
    for relative_path in _PRIVATE_PATHS:
        path = root / relative_path
        _require(path.is_file(), "PRIVATE_MODULE_MISSING: " + relative_path)
        source = path.read_text(encoding="utf-8")
        _require(source.isascii(), "PRIVATE_MODULE_NON_ASCII: " + relative_path)
        _require(
            len(source.splitlines()) <= 500,
            "PRIVATE_MODULE_SIZE_LIMIT_EXCEEDED: " + relative_path,
        )
        tree = ast.parse(source, filename=str(path))
        compile(source, str(path), "exec")
        _require(
            _empty_all_contract(tree),
            "PRIVATE_MODULE_PUBLIC_EXPORT_CONTRACT_INVALID: " + relative_path,
        )
    print("WAVE2N PRIVATE MODULE STRUCTURAL CONTRACT: PASS")


def _check_external_consumers(root: Path) -> None:
    boundary_path = Path(__file__).resolve(strict=False)
    findings: list[str] = []
    for folder_name in ("tests", "tools"):
        folder = root / folder_name
        if not folder.is_dir():
            continue
        for path in sorted(folder.rglob("*.py")):
            if path.resolve(strict=False) == boundary_path:
                continue
            source = path.read_text(encoding="utf-8", errors="replace")
            if not any(token in source for token in _PRIVATE_TOKENS):
                continue
            for finding in _forbidden_references(path, source):
                findings.append(path.relative_to(root).as_posix() + ":" + finding)
    _require(
        not findings,
        "WAVE2N_EXTERNAL_PRIVATE_REACH_IN: " + repr(findings),
    )
    print("WAVE2N EXTERNAL PRIVATE REACH-IN: 0")


def _check_optional_facade(path: Path) -> None:
    source = path.read_text(encoding="utf-8")
    _require(source.isascii(), "OPTIONAL_VALIDATOR_NON_ASCII: " + path.name)
    _require(
        len(source.splitlines()) <= 100,
        "OPTIONAL_VALIDATOR_TOO_LARGE: " + path.name,
    )
    tree = ast.parse(source, filename=str(path))
    imported = {
        name
        for node in ast.walk(tree)
        for name in _imported_names(node)
    }
    _require(
        _CANONICAL_VALIDATOR_MODULE + ".main" in imported,
        "OPTIONAL_VALIDATOR_DOES_NOT_DELEGATE: " + path.name,
    )
    _require(
        not (_assigned_names(tree) & _FORBIDDEN_STATE_NAMES),
        "OPTIONAL_VALIDATOR_DUPLICATES_CANONICAL_STATE: " + path.name,
    )


def _check_single_validator_owner(root: Path) -> None:
    canonical = root / _CANONICAL_VALIDATOR_RELATIVE
    _require(canonical.is_file(), "CANONICAL_VALIDATOR_MISSING")
    tools_root = root / "tools"
    candidates = sorted(tools_root.glob(_OPTIONAL_VALIDATOR_GLOB))
    optional_count = 0
    for path in candidates:
        if path.resolve(strict=False) == canonical.resolve(strict=False):
            continue
        _check_optional_facade(path)
        optional_count += 1
    print("WAVE2N OPTIONAL VALIDATOR FACADES: " + str(optional_count))
    print("WAVE2N SINGLE VALIDATOR STATE OWNER: PASS")


def validate_wave2n_public_boundary(root: Path) -> None:
    """Validate structural privacy and external public-contract communication."""

    _check_private_structural_contract(root)
    _check_external_consumers(root)
    _check_single_validator_owner(root)
    print("WAVE2N PUBLIC-CONTRACT-ONLY COMMUNICATION: PASS")
