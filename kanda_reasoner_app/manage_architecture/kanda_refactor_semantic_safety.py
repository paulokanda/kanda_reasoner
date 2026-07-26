# project-path: kanda_reasoner_app/manage_architecture/kanda_refactor_semantic_safety.py
"""Semantic safety and shielding checks for AST-safe refactor preparation.

The module is read-only and belongs to Architecture Review -> Large Module AST
Split Audit.  It supplements, but never replaces, the authoritative project AST
Split Audit.  Findings are evidence for AI/human architecture judgment.
"""
from __future__ import annotations

import ast
from pathlib import Path
from typing import Any, Iterable

__all__ = [
    "build_semantic_safety_evidence",
    "check_candidate_dependency_direction",
    "detect_semantic_dynamic_risks",
    "evaluate_box_shielding",
]

DYNAMIC_CALL_TARGETS = {
    "builtins.__import__",
    "builtins.compile",
    "builtins.eval",
    "builtins.exec",
    "builtins.getattr",
    "builtins.globals",
    "builtins.hasattr",
    "builtins.locals",
    "builtins.setattr",
    "builtins.vars",
    "importlib.import_module",
    "inspect.getattr_static",
    "operator.attrgetter",
    "operator.methodcaller",
}

BUILTIN_DYNAMIC_NAMES = {
    "__import__",
    "compile",
    "eval",
    "exec",
    "getattr",
    "globals",
    "hasattr",
    "locals",
    "setattr",
    "vars",
}

DYNAMIC_ATTRIBUTE_NAMES = {
    "__dict__",
    "__getattr__",
    "__getattribute__",
    "__setattr__",
}

DEFAULT_FORBIDDEN_BOX_PREFIXES = (
    "kanda_reasoner_app.manage_architecture.large_file_refactor_planner",
    "kanda_reasoner_app.freeze_after_update",
    "kanda_reasoner_app.freeze_after_update_gui",
    "kanda_reasoner_app.freeze_hint_intake",
)


def _dotted_name(node: ast.AST) -> str:
    """Return a dotted name for Name/Attribute expressions."""
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        parent = _dotted_name(node.value)
        return parent + "." + node.attr if parent else node.attr
    return ""


def _import_aliases(tree: ast.Module) -> dict[str, str]:
    """Build local-name to semantic import target mappings."""
    aliases: dict[str, str] = {}
    for node in tree.body:
        if isinstance(node, ast.Import):
            for alias in node.names:
                local = alias.asname or alias.name.split(".", 1)[0]
                aliases[local] = alias.name
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            for alias in node.names:
                if alias.name == "*":
                    continue
                local = alias.asname or alias.name
                target = module + "." + alias.name if module else alias.name
                aliases[local] = target
    for builtin_name in BUILTIN_DYNAMIC_NAMES:
        aliases.setdefault(builtin_name, "builtins." + builtin_name)
    return aliases


def _assignment_aliases(tree: ast.Module, aliases: dict[str, str]) -> dict[str, str]:
    """Resolve simple one-hop alias assignments for known semantic targets."""
    output = dict(aliases)
    changed = True
    passes = 0
    while changed and passes < 4:
        changed = False
        passes += 1
        for node in tree.body:
            if not isinstance(node, ast.Assign) or len(node.targets) != 1:
                continue
            target = node.targets[0]
            if not isinstance(target, ast.Name):
                continue
            raw_value = _dotted_name(node.value)
            resolved = _resolve_semantic_name(raw_value, output)
            if resolved and output.get(target.id) != resolved:
                output[target.id] = resolved
                changed = True
    return output


def _resolve_semantic_name(raw_name: str, aliases: dict[str, str]) -> str:
    """Resolve the leading local identifier through known alias mappings."""
    if not raw_name:
        return ""
    head, separator, tail = raw_name.partition(".")
    base = aliases.get(head, head)
    return base + separator + tail if separator else base


def _finding(
    *,
    kind: str,
    semantic_target: str,
    raw_name: str,
    line: int,
) -> dict[str, Any]:
    """Build one deterministic semantic-risk finding."""
    return {
        "kind": kind,
        "semantic_target": semantic_target,
        "raw_name": raw_name,
        "line": line,
    }


def detect_semantic_dynamic_risks(source: str, filename: str = "<source>") -> list[dict[str, Any]]:
    """Detect direct, qualified, aliased, and simple indirect dynamic behavior."""
    tree = ast.parse(source, filename=filename)
    aliases = _assignment_aliases(tree, _import_aliases(tree))
    findings: list[dict[str, Any]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            raw_name = _dotted_name(node.func)
            semantic_target = _resolve_semantic_name(raw_name, aliases)
            if semantic_target in DYNAMIC_CALL_TARGETS:
                findings.append(
                    _finding(
                        kind="dynamic_call",
                        semantic_target=semantic_target,
                        raw_name=raw_name,
                        line=int(node.lineno),
                    )
                )
        elif isinstance(node, ast.Attribute) and node.attr in DYNAMIC_ATTRIBUTE_NAMES:
            raw_name = _dotted_name(node)
            findings.append(
                _finding(
                    kind="dynamic_attribute_access",
                    semantic_target=node.attr,
                    raw_name=raw_name,
                    line=int(node.lineno),
                )
            )
    unique: dict[tuple[str, str, str, int], dict[str, Any]] = {}
    for item in findings:
        key = (
            str(item["kind"]),
            str(item["semantic_target"]),
            str(item["raw_name"]),
            int(item["line"]),
        )
        unique[key] = item
    return sorted(
        unique.values(),
        key=lambda item: (item["line"], item["kind"], item["semantic_target"]),
    )


def _module_imports(source: str, filename: str) -> list[dict[str, Any]]:
    """Return module import edges for dependency-direction checks."""
    tree = ast.parse(source, filename=filename)
    edges: list[dict[str, Any]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                edges.append({
                    "module": alias.name,
                    "symbol": "",
                    "line": int(node.lineno),
                })
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            for alias in node.names:
                edges.append({
                    "module": module,
                    "symbol": alias.name,
                    "line": int(node.lineno),
                })
    return sorted(edges, key=lambda item: (item["module"], item["symbol"], item["line"]))


def _path_to_module(relative_path: str) -> str:
    """Convert a project-relative Python file path into an import module name."""
    path = Path(relative_path.replace("\\", "/"))
    parts = list(path.parts)
    if not parts:
        return ""
    if parts[-1] == "__init__.py":
        parts = parts[:-1]
    elif parts[-1].endswith(".py"):
        parts[-1] = parts[-1][:-3]
    return ".".join(part for part in parts if part)


def check_candidate_dependency_direction(
    project_root: Path | str,
    *,
    facade_relative_path: str,
    helper_relative_paths: Iterable[str],
) -> dict[str, Any]:
    """Fail closed on helper-to-facade and helper-family cycle import edges."""
    root = Path(project_root).resolve()
    facade_module = _path_to_module(facade_relative_path)
    helper_paths = [item.replace("\\", "/") for item in helper_relative_paths]
    helper_modules = {_path_to_module(item) for item in helper_paths}
    violations: list[dict[str, Any]] = []
    graph: dict[str, list[str]] = {}
    for relative_path in helper_paths:
        path = (root / relative_path).resolve()
        try:
            path.relative_to(root)
        except ValueError as exc:
            raise ValueError("HELPER_OUTSIDE_ACTIVE_PROJECT_ROOT") from exc
        source = path.read_text(encoding="utf-8", errors="strict")
        current_module = _path_to_module(relative_path)
        imported_modules = [item["module"] for item in _module_imports(source, str(path))]
        graph[current_module] = sorted(set(imported_modules))
        for imported in imported_modules:
            if imported == facade_module:
                violations.append({
                    "kind": "helper_to_facade_import",
                    "helper": current_module,
                    "imported": imported,
                })
            if imported in helper_modules and imported != current_module:
                peer_imports = graph.get(imported, [])
                if current_module in peer_imports:
                    violations.append({
                        "kind": "helper_cycle",
                        "helper": current_module,
                        "imported": imported,
                    })
    return {
        "facade_module": facade_module,
        "helper_modules": sorted(helper_modules),
        "graph": graph,
        "violations": violations,
        "pass": not violations,
    }


def evaluate_box_shielding(
    source_by_relative_path: dict[str, str],
    *,
    allowed_owner_prefix: str = "kanda_reasoner_app.manage_architecture",
    forbidden_prefixes: Iterable[str] = DEFAULT_FORBIDDEN_BOX_PREFIXES,
) -> dict[str, Any]:
    """Check ownership and forbidden cross-box import reach-ins for source text."""
    forbidden = tuple(forbidden_prefixes)
    violations: list[dict[str, Any]] = []
    files: list[dict[str, Any]] = []
    for relative_path, source in sorted(source_by_relative_path.items()):
        module_name = _path_to_module(relative_path)
        ownership_ok = module_name.startswith(allowed_owner_prefix + ".") or module_name == allowed_owner_prefix
        imports = _module_imports(source, relative_path)
        forbidden_hits = [
            item
            for item in imports
            if any(
                item["module"] == prefix or item["module"].startswith(prefix + ".")
                for prefix in forbidden
            )
        ]
        if not ownership_ok:
            violations.append({
                "kind": "owner_boundary",
                "path": relative_path,
                "module": module_name,
            })
        for hit in forbidden_hits:
            violations.append({
                "kind": "forbidden_box_import",
                "path": relative_path,
                "module": hit["module"],
                "line": hit["line"],
            })
        files.append({
            "path": relative_path,
            "module": module_name,
            "ownership_ok": ownership_ok,
            "forbidden_imports": forbidden_hits,
        })
    return {
        "allowed_owner_prefix": allowed_owner_prefix,
        "forbidden_prefixes": list(forbidden),
        "files": files,
        "violations": violations,
        "pass": not violations,
    }


def _advisory_patterns(findings: list[dict[str, Any]], source: str) -> list[dict[str, str]]:
    """Return advisory-only known patterns without granting architecture authority."""
    patterns: list[dict[str, str]] = []
    dynamic_targets = {str(item["semantic_target"]) for item in findings}
    if "builtins.getattr" in dynamic_targets and "__post_init__" in source:
        patterns.append({
            "observed_pattern": "reflection_loop_in_dataclass_invariants",
            "candidate_pattern": "public_facade_plus_explicit_invariants_helper",
            "confidence": "high",
            "authority": "advisory_only_ai_human_must_confirm",
        })
    if "importlib.import_module" in dynamic_targets or "builtins.__import__" in dynamic_targets:
        patterns.append({
            "observed_pattern": "runtime_import_discovery",
            "candidate_pattern": "explicit_dependency_or_registry_review",
            "confidence": "medium",
            "authority": "advisory_only_ai_human_must_confirm",
        })
    return patterns


def build_semantic_safety_evidence(
    source: str,
    *,
    target_relative_path: str,
) -> dict[str, Any]:
    """Build bounded semantic-risk evidence for the Web AI preflight packet."""
    findings = detect_semantic_dynamic_risks(source, target_relative_path)
    return {
        "schema_version": "1.0",
        "kind": "ast_safe_refactor_semantic_safety",
        "target_relative_path": target_relative_path.replace("\\", "/"),
        "dynamic_or_reflection_findings": findings,
        "advisory_patterns": _advisory_patterns(findings, source),
        "fresh_ast_audit_still_required": True,
        "architecture_authority": "ai_human_judgment_not_pattern_automation",
    }
