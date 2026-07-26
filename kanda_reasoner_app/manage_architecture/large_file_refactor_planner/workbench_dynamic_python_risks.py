# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_dynamic_python_risks.py
"""Static classification of dynamic Python risks before exact payload execution."""
from __future__ import annotations

import ast
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from .models import SCHEMA_VERSION

__all__ = [
    "DYNAMIC_PYTHON_RISK_FEATURE_ID",
    "DynamicPythonRiskEvidence",
    "DynamicPythonRiskReport",
    "analyze_dynamic_python_risks",
]

DYNAMIC_PYTHON_RISK_FEATURE_ID = (
    "architecture-review-large-file-refactor-workbench-dynamic-python-risk-v1"
)

_BLOCKER_CODES = {
    "DYNAMIC_ALL_UNRESOLVED",
    "SYS_MODULES_MUTATION",
    "MODULE_LEVEL_CONTEXT_MANAGER",
}
_HIGH_RISK_CODES = {
    "MODULE_GETATTR_PRESENT",
    "MODULE_DIR_PRESENT",
    "REGISTRATION_DECORATOR",
    "METACLASS_PRESENT",
    "MODULE_LEVEL_MUTABLE_STATE",
    "LAZY_IMPORT_PRESENT",
    "IMPORTLIB_RESOURCES_PRESENT",
    "ATEXIT_REGISTRATION_PRESENT",
    "QT_MODULE_LEVEL_OBJECT_CREATION",
}
_INFORMATIONAL_CODES = {
    "TYPE_CHECKING_EDGE_PRESENT",
    "QT_OBJECT_SUBCLASS_PRESENT",
    "QT_WIDGET_SUBCLASS_PRESENT",
    "QT_SIGNAL_DESCRIPTOR_PRESENT",
}


@dataclass(frozen=True)
class DynamicPythonRiskEvidence:
    """One classified dynamic-language risk with stable evidence coordinates."""

    code: str
    severity: str
    line: int
    symbol: str
    detail: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class DynamicPythonRiskReport:
    """Risk classification used by execution feasibility and shadow validation."""

    schema_version: str
    feature_id: str
    source_path: str
    status: str
    evidence: tuple[DynamicPythonRiskEvidence, ...]
    blockers: tuple[str, ...] = field(default_factory=tuple)
    warnings: tuple[str, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["evidence"] = [item.to_dict() for item in self.evidence]
        data["blockers"] = list(self.blockers)
        data["warnings"] = list(self.warnings)
        return data


def analyze_dynamic_python_risks(source_path: str | Path) -> DynamicPythonRiskReport:
    """Classify static evidence of dynamic Python and Qt execution risks."""
    path = Path(source_path).resolve()
    try:
        source = path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        return _blocked(path, f"SOURCE_READ_FAILED:{exc}")
    try:
        tree = ast.parse(source, type_comments=True)
    except SyntaxError as exc:
        return _blocked(path, f"AST_PARSE_FAILED:{exc}")

    evidence: list[DynamicPythonRiskEvidence] = []
    aliases = _import_aliases(tree)
    evidence.extend(_module_level_risks(tree, aliases))
    evidence.extend(_nested_risks(tree, aliases))
    evidence.extend(_qt_risks(tree, aliases))

    unique: dict[tuple[str, int, str, str], DynamicPythonRiskEvidence] = {}
    for item in evidence:
        unique[(item.code, item.line, item.symbol, item.detail)] = item
    ordered = tuple(sorted(unique.values(), key=lambda item: (item.line, item.code, item.symbol)))
    blockers = tuple(sorted({item.code for item in ordered if item.severity == "BLOCKER"}))
    warnings = tuple(sorted({item.code for item in ordered if item.severity == "HIGH_RISK_REVIEW"}))
    if blockers:
        status = "dynamic_risk_blocked"
    elif warnings:
        status = "dynamic_risk_review_required"
    else:
        status = "dynamic_risk_clear"
    return DynamicPythonRiskReport(
        schema_version=SCHEMA_VERSION,
        feature_id=DYNAMIC_PYTHON_RISK_FEATURE_ID,
        source_path=str(path),
        status=status,
        evidence=ordered,
        blockers=blockers,
        warnings=warnings,
    )


def _module_level_risks(tree: ast.Module, aliases: dict[str, str]) -> list[DynamicPythonRiskEvidence]:
    evidence: list[DynamicPythonRiskEvidence] = []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if node.name == "__getattr__":
                evidence.append(_evidence("MODULE_GETATTR_PRESENT", node, node.name, "module hook"))
            elif node.name == "__dir__":
                evidence.append(_evidence("MODULE_DIR_PRESENT", node, node.name, "module hook"))
            evidence.extend(_decorator_risks(node))
        elif isinstance(node, ast.ClassDef):
            evidence.extend(_decorator_risks(node))
            if any(keyword.arg == "metaclass" for keyword in node.keywords):
                evidence.append(_evidence("METACLASS_PRESENT", node, node.name, "class metaclass"))
        elif isinstance(node, (ast.Assign, ast.AnnAssign)):
            evidence.extend(_assignment_risks(node, aliases))
        elif isinstance(node, (ast.With, ast.AsyncWith)):
            evidence.append(_evidence("MODULE_LEVEL_CONTEXT_MANAGER", node, "<module>", "module context manager"))
        elif isinstance(node, ast.If) and _is_type_checking_test(node.test):
            evidence.append(_evidence("TYPE_CHECKING_EDGE_PRESENT", node, "TYPE_CHECKING", "conditional type imports"))
        if _is_atexit_registration(node, aliases):
            evidence.append(_evidence("ATEXIT_REGISTRATION_PRESENT", node, "atexit", "module registration"))
        if _contains_importlib_resources(node, aliases):
            evidence.append(_evidence("IMPORTLIB_RESOURCES_PRESENT", node, "importlib.resources", "resource lookup"))
    return evidence


def _nested_risks(tree: ast.Module, aliases: dict[str, str]) -> list[DynamicPythonRiskEvidence]:
    evidence: list[DynamicPythonRiskEvidence] = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            for child in ast.walk(node):
                if child is node:
                    continue
                if isinstance(child, (ast.Import, ast.ImportFrom)):
                    evidence.append(_evidence("LAZY_IMPORT_PRESENT", child, node.name, "import inside callable"))
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if _is_sys_modules_target(target, aliases):
                    evidence.append(_evidence("SYS_MODULES_MUTATION", node, "sys.modules", "assignment"))
        if isinstance(node, ast.Call) and _call_name(node.func, aliases).startswith("sys.modules."):
            evidence.append(_evidence("SYS_MODULES_MUTATION", node, "sys.modules", "mutating call"))
    return evidence


def _qt_risks(tree: ast.Module, aliases: dict[str, str]) -> list[DynamicPythonRiskEvidence]:
    evidence: list[DynamicPythonRiskEvidence] = []
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            base_names = {_expr_name(base, aliases) for base in node.bases}
            if any(name.endswith("QObject") for name in base_names):
                evidence.append(_evidence("QT_OBJECT_SUBCLASS_PRESENT", node, node.name, "QObject base"))
            if any(name.endswith("QWidget") for name in base_names):
                evidence.append(_evidence("QT_WIDGET_SUBCLASS_PRESENT", node, node.name, "QWidget base"))
            for child in node.body:
                if isinstance(child, (ast.Assign, ast.AnnAssign)) and _assignment_contains_qt_signal(child, aliases):
                    evidence.append(_evidence("QT_SIGNAL_DESCRIPTOR_PRESENT", child, node.name, "Signal descriptor"))
        elif isinstance(node, (ast.Assign, ast.AnnAssign)) and _assignment_creates_qt_object(node, aliases):
            evidence.append(_evidence("QT_MODULE_LEVEL_OBJECT_CREATION", node, "<module>", "Qt object constructor"))
        elif isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
            call_name = _call_name(node.value.func, aliases)
            if _looks_like_qt_constructor(call_name):
                evidence.append(_evidence("QT_MODULE_LEVEL_OBJECT_CREATION", node, "<module>", call_name))
    return evidence


def _assignment_risks(node: ast.Assign | ast.AnnAssign, aliases: dict[str, str]) -> list[DynamicPythonRiskEvidence]:
    evidence: list[DynamicPythonRiskEvidence] = []
    targets = node.targets if isinstance(node, ast.Assign) else [node.target]
    value = node.value
    for target in targets:
        if isinstance(target, ast.Name) and target.id == "__all__":
            if not _literal_string_sequence(value):
                evidence.append(_evidence("DYNAMIC_ALL_UNRESOLVED", node, "__all__", "not a literal string sequence"))
            continue
        if isinstance(target, ast.Name) and _is_mutable_value(value):
            evidence.append(_evidence("MODULE_LEVEL_MUTABLE_STATE", node, target.id, "mutable module value"))
        if _is_sys_modules_target(target, aliases):
            evidence.append(_evidence("SYS_MODULES_MUTATION", node, "sys.modules", "assignment"))
    return evidence


def _decorator_risks(node: ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) -> list[DynamicPythonRiskEvidence]:
    risky_tokens = ("register", "route", "receiver", "hook", "handler", "subscribe")
    evidence: list[DynamicPythonRiskEvidence] = []
    for decorator in node.decorator_list:
        name = _expr_name(decorator, {})
        if any(token in name.casefold() for token in risky_tokens):
            evidence.append(_evidence("REGISTRATION_DECORATOR", decorator, node.name, name))
    return evidence


def _import_aliases(tree: ast.Module) -> dict[str, str]:
    aliases: dict[str, str] = {}
    for node in tree.body:
        if isinstance(node, ast.Import):
            for alias in node.names:
                aliases[alias.asname or alias.name.split(".")[0]] = alias.name
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            for alias in node.names:
                aliases[alias.asname or alias.name] = f"{module}.{alias.name}".strip(".")
    return aliases


def _literal_string_sequence(value: ast.AST | None) -> bool:
    return isinstance(value, (ast.List, ast.Tuple)) and all(
        isinstance(item, ast.Constant) and isinstance(item.value, str) for item in value.elts
    )


def _is_mutable_value(value: ast.AST | None) -> bool:
    if isinstance(value, (ast.List, ast.Dict, ast.Set)):
        return True
    if isinstance(value, ast.Call):
        name = _expr_name(value.func, {})
        return name in {"list", "dict", "set", "defaultdict", "deque"}
    return False


def _is_type_checking_test(node: ast.AST) -> bool:
    return isinstance(node, ast.Name) and node.id == "TYPE_CHECKING" or (
        isinstance(node, ast.Attribute) and node.attr == "TYPE_CHECKING"
    )


def _is_atexit_registration(node: ast.AST, aliases: dict[str, str]) -> bool:
    for child in ast.walk(node):
        if isinstance(child, ast.Call) and _call_name(child.func, aliases).endswith("atexit.register"):
            return True
    return False


def _contains_importlib_resources(node: ast.AST, aliases: dict[str, str]) -> bool:
    return any(
        isinstance(child, (ast.Call, ast.Attribute))
        and "importlib.resources" in _expr_name(child.func if isinstance(child, ast.Call) else child, aliases)
        for child in ast.walk(node)
    )


def _assignment_contains_qt_signal(node: ast.Assign | ast.AnnAssign, aliases: dict[str, str]) -> bool:
    value = node.value
    return isinstance(value, ast.Call) and _call_name(value.func, aliases).endswith(("Signal", "pyqtSignal"))


def _assignment_creates_qt_object(node: ast.Assign | ast.AnnAssign, aliases: dict[str, str]) -> bool:
    value = node.value
    return isinstance(value, ast.Call) and _looks_like_qt_constructor(_call_name(value.func, aliases))


def _looks_like_qt_constructor(name: str) -> bool:
    leaf = name.split(".")[-1]
    return leaf in {"QApplication", "QCoreApplication", "QObject", "QWidget", "QMainWindow", "QTimer"}


def _is_sys_modules_target(node: ast.AST, aliases: dict[str, str]) -> bool:
    if isinstance(node, ast.Subscript):
        return _expr_name(node.value, aliases).endswith("sys.modules")
    return False


def _call_name(node: ast.AST, aliases: dict[str, str]) -> str:
    return _expr_name(node, aliases)


def _expr_name(node: ast.AST, aliases: dict[str, str]) -> str:
    if isinstance(node, ast.Name):
        return aliases.get(node.id, node.id)
    if isinstance(node, ast.Attribute):
        root = _expr_name(node.value, aliases)
        return f"{root}.{node.attr}" if root else node.attr
    if isinstance(node, ast.Call):
        return _expr_name(node.func, aliases)
    return ""


def _evidence(code: str, node: ast.AST, symbol: str, detail: str) -> DynamicPythonRiskEvidence:
    if code in _BLOCKER_CODES:
        severity = "BLOCKER"
    elif code in _HIGH_RISK_CODES:
        severity = "HIGH_RISK_REVIEW"
    elif code in _INFORMATIONAL_CODES:
        severity = "INFORMATIONAL"
    else:
        severity = "INFORMATIONAL"
    return DynamicPythonRiskEvidence(
        code=code,
        severity=severity,
        line=int(getattr(node, "lineno", 0) or 0),
        symbol=symbol,
        detail=detail,
    )


def _blocked(path: Path, blocker: str) -> DynamicPythonRiskReport:
    return DynamicPythonRiskReport(
        schema_version=SCHEMA_VERSION,
        feature_id=DYNAMIC_PYTHON_RISK_FEATURE_ID,
        source_path=str(path),
        status="dynamic_risk_blocked",
        evidence=(),
        blockers=(blocker,),
    )
