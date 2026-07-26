# project-path: kanda_reasoner_app/manage_architecture/kanda_refactor_project_index.py
"""Read-only project evidence index for AST-safe refactor preparation.

The module belongs to Architecture Review -> Large Module AST Split Audit.  It
collects bounded consumer and public-contract evidence without modifying source,
GUI state, Planner state, Workbench state, AQR state, or Freeze state.
"""
from __future__ import annotations

import ast
import hashlib
from pathlib import Path
from typing import Any, Iterable

from kanda_reasoner_app.project_exclusion_policy import iter_reasoner_project_files

__all__ = [
    "build_project_refactor_index",
    "capture_public_contract",
    "discover_module_consumers",
    "module_name_from_relative_path",
]


def _sha256(raw: bytes) -> str:
    """Return a lowercase content hash for project evidence identity."""
    return hashlib.sha256(raw).hexdigest()


def _read_source(path: Path) -> tuple[bytes, str]:
    """Read one UTF-8 Python source file without replacement decoding."""
    raw = path.read_bytes()
    source = raw.decode("utf-8", errors="strict")
    return raw, source


def _iter_python_files(project_root: Path) -> Iterable[Path]:
    """Yield active project Python files under the shared exclusion policy."""
    yield from iter_reasoner_project_files(project_root, suffixes={".py"})


def module_name_from_relative_path(relative_path: str) -> str:
    """Convert one project-relative Python path into an import-style name."""
    path = Path(relative_path.replace("\\", "/"))
    parts = list(path.parts)
    if not parts:
        return ""
    if parts[-1] == "__init__.py":
        parts = parts[:-1]
    elif parts[-1].endswith(".py"):
        parts[-1] = parts[-1][:-3]
    return ".".join(part for part in parts if part)


def _literal_all_state(tree: ast.Module) -> dict[str, Any]:
    """Return explicit public-surface state without confusing unknown and absent."""
    for node in tree.body:
        if not isinstance(node, (ast.Assign, ast.AnnAssign)):
            continue
        targets: list[ast.expr] = []
        value: ast.expr | None = None
        if isinstance(node, ast.Assign):
            targets = list(node.targets)
            value = node.value
        else:
            targets = [node.target]
            value = node.value
        if not any(isinstance(target, ast.Name) and target.id == "__all__" for target in targets):
            continue
        if value is None:
            return {"mode": "UNRESOLVED_DYNAMIC", "symbols": []}
        try:
            payload = ast.literal_eval(value)
        except (ValueError, TypeError, SyntaxError):
            return {"mode": "UNRESOLVED_DYNAMIC", "symbols": []}
        if isinstance(payload, (list, tuple)) and all(isinstance(item, str) for item in payload):
            return {"mode": "EXPLICIT_LITERAL", "symbols": list(payload)}
        return {"mode": "UNRESOLVED_DYNAMIC", "symbols": []}
    return {"mode": "ABSENT", "symbols": []}


def _annotation_text(node: ast.expr | None) -> str:
    """Render one annotation expression deterministically when available."""
    if node is None:
        return ""
    try:
        return ast.unparse(node)
    except Exception:
        return "<unparse-error>"


def _decorator_text(node: ast.expr) -> str:
    """Render decorator syntax while preserving declaration order."""
    try:
        return ast.unparse(node)
    except Exception:
        return "<unparse-error>"


def _argument_contract(arguments: ast.arguments) -> dict[str, Any]:
    """Capture Python call-shape boundaries without importing target modules."""
    positional = [arg.arg for arg in arguments.posonlyargs + arguments.args]
    positional_only = [arg.arg for arg in arguments.posonlyargs]
    keyword_only = [arg.arg for arg in arguments.kwonlyargs]
    annotation_map = {
        arg.arg: _annotation_text(arg.annotation)
        for arg in [
            *arguments.posonlyargs,
            *arguments.args,
            *arguments.kwonlyargs,
        ]
    }
    if arguments.vararg is not None:
        annotation_map["*" + arguments.vararg.arg] = _annotation_text(arguments.vararg.annotation)
    if arguments.kwarg is not None:
        annotation_map["**" + arguments.kwarg.arg] = _annotation_text(arguments.kwarg.annotation)
    defaults = [_annotation_text(item) for item in arguments.defaults]
    kw_defaults = [
        _annotation_text(item) if item is not None else "<required>"
        for item in arguments.kw_defaults
    ]
    return {
        "positional": positional,
        "positional_only": positional_only,
        "keyword_only": keyword_only,
        "vararg": arguments.vararg.arg if arguments.vararg is not None else "",
        "kwarg": arguments.kwarg.arg if arguments.kwarg is not None else "",
        "defaults": defaults,
        "keyword_defaults": kw_defaults,
        "annotations": annotation_map,
    }


def _function_contract(node: ast.FunctionDef | ast.AsyncFunctionDef) -> dict[str, Any]:
    """Capture one top-level function contract."""
    return {
        "kind": "async_function" if isinstance(node, ast.AsyncFunctionDef) else "function",
        "name": node.name,
        "decorators": [_decorator_text(item) for item in node.decorator_list],
        "arguments": _argument_contract(node.args),
        "returns": _annotation_text(node.returns),
    }


def _class_contract(node: ast.ClassDef) -> dict[str, Any]:
    """Capture one top-level class contract and method call shapes."""
    methods = [
        _function_contract(child)
        for child in node.body
        if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef))
    ]
    return {
        "kind": "class",
        "name": node.name,
        "decorators": [_decorator_text(item) for item in node.decorator_list],
        "bases": [_annotation_text(item) for item in node.bases],
        "keywords": {
            item.arg or "**": _annotation_text(item.value)
            for item in node.keywords
        },
        "methods": methods,
    }


def capture_public_contract(project_root: Path | str, target_relative_path: str) -> dict[str, Any]:
    """Capture static public contract evidence for one target module."""
    root = Path(project_root).resolve()
    target = (root / target_relative_path).resolve()
    try:
        target.relative_to(root)
    except ValueError as exc:
        raise ValueError("TARGET_OUTSIDE_ACTIVE_PROJECT_ROOT") from exc
    raw, source = _read_source(target)
    tree = ast.parse(source, filename=str(target))
    symbols: list[dict[str, Any]] = []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            symbols.append(_function_contract(node))
        elif isinstance(node, ast.ClassDef):
            symbols.append(_class_contract(node))
    return {
        "target_relative_path": target_relative_path.replace("\\", "/"),
        "source_sha256": _sha256(raw),
        "all_state": _literal_all_state(tree),
        "top_level_symbols": symbols,
    }


def _resolve_import_from_module(current_module: str, node: ast.ImportFrom) -> str:
    """Resolve a relative ImportFrom module name against the consumer module."""
    module = node.module or ""
    if node.level <= 0:
        return module
    package_parts = current_module.split(".")[:-1]
    keep_count = max(0, len(package_parts) - node.level + 1)
    base = package_parts[:keep_count]
    if module:
        base.extend(module.split("."))
    return ".".join(base)


def _consumer_records_for_tree(
    tree: ast.Module,
    *,
    consumer_relative_path: str,
    consumer_module: str,
    target_module: str,
) -> list[dict[str, Any]]:
    """Return direct import records that point at the target module."""
    records: list[dict[str, Any]] = []
    module_aliases: dict[str, str] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == target_module:
                    local_name = alias.asname or alias.name.split(".", 1)[0]
                    module_aliases[local_name] = alias.name
                    records.append({
                        "consumer": consumer_relative_path,
                        "kind": "import_module",
                        "symbol": "",
                        "alias": alias.asname or "",
                        "line": int(node.lineno),
                    })
        elif isinstance(node, ast.ImportFrom):
            resolved_module = _resolve_import_from_module(consumer_module, node)
            if resolved_module == target_module:
                for alias in node.names:
                    records.append({
                        "consumer": consumer_relative_path,
                        "kind": "from_import",
                        "symbol": alias.name,
                        "alias": alias.asname or "",
                        "line": int(node.lineno),
                    })
    for node in ast.walk(tree):
        if not isinstance(node, ast.Attribute) or not isinstance(node.value, ast.Name):
            continue
        alias_target = module_aliases.get(node.value.id, "")
        if alias_target == target_module:
            records.append({
                "consumer": consumer_relative_path,
                "kind": "module_attribute",
                "symbol": node.attr,
                "alias": node.value.id,
                "line": int(node.lineno),
            })
    return records


def discover_module_consumers(
    project_root: Path | str,
    target_relative_path: str,
    *,
    max_records: int = 250,
) -> dict[str, Any]:
    """Discover bounded direct consumer evidence for one project module."""
    root = Path(project_root).resolve()
    target_relative = target_relative_path.replace("\\", "/")
    target_module = module_name_from_relative_path(target_relative)
    records: list[dict[str, Any]] = []
    scanned_files = 0
    parse_failures: list[str] = []
    for path in _iter_python_files(root):
        relative = path.relative_to(root).as_posix()
        if relative == target_relative:
            continue
        scanned_files += 1
        try:
            source = path.read_text(encoding="utf-8", errors="strict")
            tree = ast.parse(source, filename=str(path))
        except (OSError, UnicodeError, SyntaxError):
            if len(parse_failures) < 25:
                parse_failures.append(relative)
            continue
        consumer_module = module_name_from_relative_path(relative)
        records.extend(
            _consumer_records_for_tree(
                tree,
                consumer_relative_path=relative,
                consumer_module=consumer_module,
                target_module=target_module,
            )
        )
    records.sort(key=lambda item: (item["consumer"], item["line"], item["kind"], item["symbol"]))
    truncated = len(records) > max_records
    return {
        "target_module": target_module,
        "scanned_python_files": scanned_files,
        "record_count": len(records),
        "records_truncated": truncated,
        "records": records[:max_records],
        "parse_failures": parse_failures,
    }


def build_project_refactor_index(
    project_root: Path | str,
    target_relative_path: str,
) -> dict[str, Any]:
    """Build the bounded project index consumed by Web AI preflight evidence."""
    root = Path(project_root).resolve()
    contract = capture_public_contract(root, target_relative_path)
    consumers = discover_module_consumers(root, target_relative_path)
    identity_material = (
        contract["source_sha256"]
        + "\n"
        + str(consumers["record_count"])
        + "\n"
        + consumers["target_module"]
    ).encode("utf-8")
    return {
        "schema_version": "1.0",
        "kind": "ast_safe_refactor_project_index",
        "index_identity_sha256": _sha256(identity_material),
        "public_contract": contract,
        "consumers": consumers,
        "authority": "read_only_evidence_not_source_truth",
    }
