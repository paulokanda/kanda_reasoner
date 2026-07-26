# project-path: kanda_reasoner_app/manage_architecture/large_module_split_safety_classifier.py
"""Refactor safety classifier for Large Module AST Split Audit.

This module keeps the Large Module AST Split Audit read-only. It classifies a
module as a safe or risky refactor candidate from deterministic AST evidence,
with an optional Ruff lint pass when Ruff is installed locally.
"""
from __future__ import annotations

import ast
import importlib.util
import json
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

__all__ = ["classify_refactor_safety", "resolve_large_module_split_ruff_command"]

DYNAMIC_CALL_NAMES = {
    "__import__",
    "compile",
    "eval",
    "exec",
    "getattr",
    "globals",
    "locals",
    "setattr",
    "vars",
}

INSPECT_NAMES = {
    "inspect.getmembers",
    "inspect.getsource",
    "inspect.signature",
}

RUFF_RISK_CODES = {
    "E999",
    "F403",
    "F405",
    "F821",
    "F822",
    "F823",
    "F841",
}


@dataclass(slots=True)
class _ModuleSafetyEvidence:
    """Static evidence used to classify refactor candidate safety."""

    decorators: int = 0
    type_annotations: int = 0
    dynamic_calls: list[str] = field(default_factory=list)
    global_statements: int = 0
    nonlocal_statements: int = 0
    main_guard: bool = False
    module_getattr: bool = False
    top_level_public: list[str] = field(default_factory=list)
    top_level_classes: list[tuple[str, int]] = field(default_factory=list)
    top_level_functions: list[str] = field(default_factory=list)
    module_mutable_assignments: list[str] = field(default_factory=list)
    module_level_calls: int = 0
    star_imports: int = 0


class _SafetyVisitor(ast.NodeVisitor):
    """Collect deterministic AST risk signals for module split safety."""

    def __init__(self) -> None:
        """Initialize the visitor."""
        self.evidence = _ModuleSafetyEvidence()
        self._scope_depth = 0

    def visit_Module(self, node: ast.Module) -> Any:
        """Visit module body with top-level context awareness."""
        for item in node.body:
            if isinstance(item, ast.ImportFrom):
                self._check_star_import(item)
            if isinstance(item, (ast.Assign, ast.AnnAssign)):
                self._record_module_assignment(item)
            if isinstance(item, ast.Expr) and isinstance(item.value, ast.Call):
                self.evidence.module_level_calls += 1
            if isinstance(item, ast.If) and _is_main_guard(item.test):
                self.evidence.main_guard = True
            if isinstance(item, ast.ClassDef):
                self._record_class(item)
            elif isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                self._record_function(item)
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> Any:
        """Track decorators, annotations, and scope depth for functions."""
        self._record_callable_details(node)
        self._scope_depth += 1
        self.generic_visit(node)
        self._scope_depth -= 1

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> Any:
        """Track decorators, annotations, and scope depth for async functions."""
        self._record_callable_details(node)
        self._scope_depth += 1
        self.generic_visit(node)
        self._scope_depth -= 1

    def visit_ClassDef(self, node: ast.ClassDef) -> Any:
        """Track decorators, base classes, and scope depth for classes."""
        self.evidence.decorators += len(node.decorator_list)
        self.evidence.type_annotations += len(node.bases)
        self._scope_depth += 1
        self.generic_visit(node)
        self._scope_depth -= 1

    def visit_Global(self, node: ast.Global) -> Any:
        """Record global statement use."""
        self.evidence.global_statements += 1
        self.generic_visit(node)

    def visit_Nonlocal(self, node: ast.Nonlocal) -> Any:
        """Record nonlocal statement use."""
        self.evidence.nonlocal_statements += 1
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> Any:
        """Record dynamic, reflection, and import-sensitive calls."""
        name = _call_name(node.func)
        if name in DYNAMIC_CALL_NAMES or name in INSPECT_NAMES:
            self.evidence.dynamic_calls.append(name)
        if name == "importlib.import_module":
            self.evidence.dynamic_calls.append(name)
        self.generic_visit(node)

    def _check_star_import(self, node: ast.ImportFrom) -> None:
        """Record star imports because they weaken static name evidence."""
        if any(alias.name == "*" for alias in node.names):
            self.evidence.star_imports += 1

    def _record_module_assignment(self, node: ast.Assign | ast.AnnAssign) -> None:
        """Record mutable module-level assignments."""
        targets: list[ast.AST]
        if isinstance(node, ast.Assign):
            targets = list(node.targets)
            value = node.value
        else:
            targets = [node.target]
            value = node.value
        if value is None or not _looks_mutable_literal(value):
            return
        for target in targets:
            name = _assigned_name(target)
            if name:
                self.evidence.module_mutable_assignments.append(name)

    def _record_class(self, node: ast.ClassDef) -> None:
        """Record top-level class evidence."""
        line_start = int(getattr(node, "lineno", 0) or 0)
        line_end = int(getattr(node, "end_lineno", line_start) or line_start)
        self.evidence.top_level_classes.append((node.name, max(1, line_end - line_start + 1)))
        if not node.name.startswith("_"):
            self.evidence.top_level_public.append(node.name)

    def _record_function(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> None:
        """Record top-level function evidence."""
        self.evidence.top_level_functions.append(node.name)
        if node.name == "__getattr__":
            self.evidence.module_getattr = True
        if not node.name.startswith("_"):
            self.evidence.top_level_public.append(node.name)

    def _record_callable_details(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> None:
        """Record callable decorators and annotation usage."""
        self.evidence.decorators += len(node.decorator_list)
        args = list(node.args.args) + list(node.args.kwonlyargs)
        if node.args.vararg is not None:
            args.append(node.args.vararg)
        if node.args.kwarg is not None:
            args.append(node.args.kwarg)
        self.evidence.type_annotations += sum(1 for arg in args if arg.annotation is not None)
        if node.returns is not None:
            self.evidence.type_annotations += 1


def classify_refactor_safety(
    project_root: str | Path,
    target_path: str | Path,
    source: str,
    tree: ast.Module,
    audit_data: dict[str, Any],
    classifier_mode: str = "heuristic",
) -> dict[str, Any]:
    """Classify large-module refactor safety from AST and optional Ruff evidence."""
    mode = _normalize_mode(classifier_mode)
    visitor = _SafetyVisitor()
    visitor.visit(tree)
    evidence = visitor.evidence
    blockers, warnings, score = _classify_from_ast(evidence, audit_data)
    ruff_result = _run_ruff_if_requested(project_root, target_path, mode)
    if ruff_result["used"]:
        ruff_score, ruff_blockers, ruff_warnings = _classify_from_ruff(ruff_result)
        score += ruff_score
        blockers.extend(ruff_blockers)
        warnings.extend(ruff_warnings)
    label = "RISK REFACTORING" if blockers or score >= 6 else "SAFE REFACTORING"
    level = "risk" if label.startswith("RISK") else "safe"
    return {
        "schema_version": "1.0",
        "classifier_mode": mode,
        "engine": _engine_label(mode, ruff_result),
        "label": label,
        "level": level,
        "score": score,
        "hard_blockers": sorted(set(blockers)),
        "warnings": sorted(set(warnings)),
        "signals": _signals_from_evidence(evidence, audit_data),
        "ruff": ruff_result,
    }


def _normalize_mode(value: str) -> str:
    """Normalize user-facing classifier mode."""
    lowered = str(value or "").strip().lower().replace("-", "_")
    if lowered in {"static_tools", "tool", "tools", "ruff", "tool_assisted"}:
        return "static_tools"
    return "heuristic"


def _engine_label(mode: str, ruff_result: dict[str, Any]) -> str:
    """Return a human-readable classifier engine label."""
    if mode == "static_tools" and ruff_result.get("used"):
        return "AST heuristic + Ruff static lint"
    if mode == "static_tools":
        return "AST heuristic; Ruff not available"
    return "AST heuristic"


def _classify_from_ast(
    evidence: _ModuleSafetyEvidence,
    audit_data: dict[str, Any],
) -> tuple[list[str], list[str], int]:
    """Convert AST evidence into blockers, warnings, and a score."""
    blockers: list[str] = []
    warnings: list[str] = []
    score = 0
    islands = list(audit_data.get("islands", []))
    matrix = list(audit_data.get("independence_matrix", []))
    if len(islands) < 2:
        warnings.append("Only one responsibility island was detected.")
        score += 2
    if not any(row.get("relation") == "independent" for row in matrix):
        warnings.append("No independent responsibility-island pair was detected.")
        score += 2
    if any(island.get("risk") == "high" for island in islands):
        blockers.append("At least one candidate island has high AST risk.")
        score += 4
    if evidence.dynamic_calls:
        blockers.append("Dynamic or reflection calls were detected.")
        score += 4
    if evidence.global_statements or evidence.nonlocal_statements:
        blockers.append("global or nonlocal statements were detected.")
        score += 4
    if evidence.module_getattr:
        warnings.append("Module-level __getattr__ may hide dynamic public API behavior.")
        score += 2
    if evidence.main_guard:
        warnings.append("The module has an if __name__ == '__main__' block that should stay in the facade.")
        score += 1
    if evidence.decorators:
        warnings.append("Decorated functions or classes require decorator preservation checks.")
        score += 1
    if evidence.type_annotations:
        warnings.append("Type annotations may require import preservation in helper modules.")
        score += 1
    if evidence.star_imports:
        blockers.append("Star imports weaken static dependency evidence.")
        score += 3
    if len(evidence.module_mutable_assignments) >= 3:
        warnings.append("Several mutable module-level assignments were detected.")
        score += 2
    if evidence.module_level_calls >= 3:
        warnings.append("Several module-level calls may indicate import-time side effects.")
        score += 2
    oversized_classes = [name for name, lines in evidence.top_level_classes if lines > 500]
    if oversized_classes:
        blockers.append("A top-level class is over 500 lines and should not be auto-split by methods.")
        score += 4
    if len(evidence.top_level_public) > 20 and "__all__" not in evidence.top_level_public:
        warnings.append("Large inferred public API; preserve facade exports carefully.")
        score += 1
    return blockers, warnings, score


def _run_ruff_if_requested(
    project_root: str | Path,
    target_path: str | Path,
    mode: str,
) -> dict[str, Any]:
    """Run Ruff read-only when static tool mode is requested and Ruff exists."""
    ruff_command, ruff_invocation = resolve_large_module_split_ruff_command()
    result: dict[str, Any] = {
        "available": bool(ruff_command),
        "used": False,
        "issue_count": 0,
        "risk_issue_count": 0,
        "codes": [],
        "message": "Ruff not requested.",
        "invocation": ruff_invocation,
    }
    if mode != "static_tools":
        return result
    if not ruff_command:
        result["message"] = "Ruff executable/package not found; AST heuristic used."
        return result
    target = Path(target_path)
    command = [
        *ruff_command,
        "check",
        "--output-format=json",
        "--exit-zero",
        str(target),
    ]
    try:
        completed = subprocess.run(
            command,
            cwd=str(Path(project_root)),
            capture_output=True,
            text=True,
            timeout=20,
            check=False,
        )
    except Exception as exc:
        result["message"] = f"Ruff check could not run: {exc}"
        return result
    if completed.returncode == 2:
        result["message"] = completed.stderr.strip() or "Ruff terminated abnormally."
        return result
    try:
        issues = json.loads(completed.stdout or "[]")
    except json.JSONDecodeError:
        result["message"] = "Ruff output was not valid JSON."
        return result
    codes = sorted({str(item.get("code", "")) for item in issues if item.get("code")})
    risk_codes = sorted(code for code in codes if code in RUFF_RISK_CODES)
    result.update(
        {
            "used": True,
            "issue_count": len(issues),
            "risk_issue_count": sum(1 for item in issues if item.get("code") in RUFF_RISK_CODES),
            "codes": codes,
            "message": "Ruff read-only lint completed.",
            "risk_codes": risk_codes,
        }
    )
    return result


def resolve_large_module_split_ruff_command() -> tuple[list[str], str]:
    """Return a Ruff command, preferring the executable and falling back to module mode."""
    ruff_path = shutil.which("ruff")
    if ruff_path:
        return [ruff_path], ruff_path
    if importlib.util.find_spec("ruff") is not None:
        return [sys.executable, "-m", "ruff"], f"{sys.executable} -m ruff"
    return [], ""


# Backward-compatible private alias for existing internal consumers.
_resolve_ruff_command = resolve_large_module_split_ruff_command


def _classify_from_ruff(result: dict[str, Any]) -> tuple[int, list[str], list[str]]:
    """Translate Ruff JSON evidence into refactor-safety signals."""
    blockers: list[str] = []
    warnings: list[str] = []
    score = 0
    risk_count = int(result.get("risk_issue_count") or 0)
    codes = list(result.get("risk_codes") or [])
    if risk_count:
        blockers.append("Ruff found name/import issues that can make refactor movement unsafe: " + ", ".join(codes))
        score += min(6, risk_count * 2)
    issue_count = int(result.get("issue_count") or 0)
    if issue_count > risk_count:
        warnings.append("Ruff found additional lint issues; review before refactoring.")
        score += 1
    return score, blockers, warnings


def _signals_from_evidence(
    evidence: _ModuleSafetyEvidence,
    audit_data: dict[str, Any],
) -> dict[str, Any]:
    """Return compact JSON signals for report and GUI use."""
    return {
        "decorator_count": evidence.decorators,
        "type_annotation_count": evidence.type_annotations,
        "dynamic_calls": sorted(set(evidence.dynamic_calls)),
        "global_statement_count": evidence.global_statements,
        "nonlocal_statement_count": evidence.nonlocal_statements,
        "main_guard_present": evidence.main_guard,
        "module_getattr_present": evidence.module_getattr,
        "public_symbol_count": len(evidence.top_level_public),
        "top_level_class_count": len(evidence.top_level_classes),
        "top_level_function_count": len(evidence.top_level_functions),
        "mutable_module_assignments": sorted(set(evidence.module_mutable_assignments)),
        "module_level_call_count": evidence.module_level_calls,
        "star_import_count": evidence.star_imports,
        "island_count": len(audit_data.get("islands", [])),
    }


def _call_name(node: ast.AST) -> str:
    """Return a dotted name for simple call expressions."""
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        prefix = _call_name(node.value)
        return f"{prefix}.{node.attr}" if prefix else node.attr
    return ""


def _assigned_name(node: ast.AST) -> str:
    """Return an assigned simple name, if available."""
    if isinstance(node, ast.Name):
        return node.id
    return ""


def _looks_mutable_literal(node: ast.AST) -> bool:
    """Return whether a module assignment creates obvious mutable state."""
    return isinstance(node, (ast.Dict, ast.List, ast.Set, ast.ListComp, ast.DictComp, ast.SetComp))


def _is_main_guard(node: ast.AST) -> bool:
    """Return whether a condition is if __name__ == '__main__'."""
    if not isinstance(node, ast.Compare):
        return False
    if not isinstance(node.left, ast.Name) or node.left.id != "__name__":
        return False
    if len(node.ops) != 1 or not isinstance(node.ops[0], ast.Eq):
        return False
    if len(node.comparators) != 1:
        return False
    right = node.comparators[0]
    return isinstance(right, ast.Constant) and right.value == "__main__"
