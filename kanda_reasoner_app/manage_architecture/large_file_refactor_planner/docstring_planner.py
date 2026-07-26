# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/docstring_planner.py
"""Deterministic docstring proposal contracts for the large-file planner."""
from __future__ import annotations

import ast
from pathlib import Path

from .models import (
    FEATURE_ID,
    SCHEMA_VERSION,
    DocstringProposal,
    ModuleAnalysisReport,
    RefactorPlan,
    RefactorSymbol,
)

__all__ = ["build_docstring_proposals"]

_ALLOWED_PROVENANCE = {
    "existing",
    "deterministic_template",
    "llm_drafted",
    "low_confidence_needs_review",
    "manual_required",
}
_SIDE_EFFECT_RISKS = {
    "GLOBAL_STATE",
    "DYNAMIC_IMPORT",
    "STAR_IMPORT",
    "RELATIVE_IMPORT_RISK",
    "PRIVATE_REACH_IN_RISK",
}


def build_docstring_proposals(
    report: ModuleAnalysisReport,
    plan: RefactorPlan | None = None,
) -> list[DocstringProposal]:
    """Build reviewable docstring proposals without changing source files."""
    proposals: list[DocstringProposal] = []
    target = Path(report.target_file)
    tree = _parse_source(target)
    if not report.module_docstring_present:
        proposals.append(_module_proposal(report))
    for symbol in report.symbols:
        proposal = _symbol_proposal(report, symbol)
        if proposal is not None:
            proposals.append(proposal)
    if tree is not None:
        proposals.extend(_method_proposals(report, tree))
    if plan is not None:
        proposals.extend(_generated_module_proposals(report, plan))
    _assert_provenance(proposals)
    return proposals


def _parse_source(path: Path) -> ast.Module | None:
    """Parse source for method-level docstring evidence."""
    try:
        source = path.read_text(encoding="utf-8", errors="replace")
        return ast.parse(source)
    except (OSError, SyntaxError):
        return None


def _module_proposal(report: ModuleAnalysisReport) -> DocstringProposal:
    """Return a module-level docstring proposal."""
    target_name = Path(report.target_file).stem
    reason = "Module docstring is missing."
    confidence = "medium"
    provenance = "deterministic_template"
    risks = ["MISSING_DOCSTRING"]
    if report.risk_flags:
        confidence = "low"
        provenance = "low_confidence_needs_review"
        risks.extend(report.risk_flags)
    text = _triple(
        f"Describe the {target_name} module.",
        "This proposal was generated from static planner evidence and requires review.",
    )
    return _proposal(report, "module", target_name, text, provenance, confidence, risks, reason)


def _symbol_proposal(
    report: ModuleAnalysisReport,
    symbol: RefactorSymbol,
) -> DocstringProposal | None:
    """Return a proposal for a top-level symbol when appropriate."""
    if symbol.has_docstring:
        return None
    if symbol.visibility == "private" and symbol.physical_lines < 40:
        return None
    kind = "class" if symbol.kind == "class" else "function"
    provenance, confidence, risks = _confidence_for_symbol(symbol)
    reason = f"{kind.capitalize()} docstring is missing."
    summary = f"Describe {symbol.name}."
    extra = "Generated from static symbol evidence only; review before insertion."
    text = _function_text(summary, extra, symbol) if kind == "function" else _triple(summary, extra)
    return _proposal(report, kind, symbol.name, text, provenance, confidence, risks, reason)


def _method_proposals(report: ModuleAnalysisReport, tree: ast.Module) -> list[DocstringProposal]:
    """Return proposals for missing public class method docstrings."""
    proposals: list[DocstringProposal] = []
    public_classes = {symbol.name for symbol in report.symbols if symbol.kind == "class"}
    for node in tree.body:
        if not isinstance(node, ast.ClassDef) or node.name not in public_classes:
            continue
        for child in node.body:
            if not isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            if child.name.startswith("_") or ast.get_docstring(child):
                continue
            name = f"{node.name}.{child.name}"
            risks = ["MISSING_DOCSTRING"]
            if _contains_explicit_raise(child):
                risks.append("RAISES_DETECTED")
            text = _method_text(child)
            proposals.append(
                _proposal(
                    report,
                    "method",
                    name,
                    text,
                    "deterministic_template",
                    "medium",
                    risks,
                    "Public method docstring is missing.",
                )
            )
    return proposals


def _generated_module_proposals(
    report: ModuleAnalysisReport,
    plan: RefactorPlan,
) -> list[DocstringProposal]:
    """Return module docstring proposals for planned modules."""
    proposals: list[DocstringProposal] = []
    for module in plan.proposed_modules:
        if module.role == "public_facade":
            summary = "Preserve the public facade for the original module."
        else:
            summary = f"Group {module.role.replace('_', ' ')} symbols for review."
        text = _triple(
            summary,
            "Generated module docstring proposal; no preview file has been written.",
        )
        proposals.append(
            _proposal(
                report,
                "planned_module",
                module.filename,
                text,
                "deterministic_template",
                "medium",
                list(module.risk_flags),
                "Planned module needs a reviewable module docstring before preview writing.",
            )
        )
    return proposals


def _confidence_for_symbol(symbol: RefactorSymbol) -> tuple[str, str, list[str]]:
    """Return provenance, confidence, and risk flags for one proposal."""
    risks = ["MISSING_DOCSTRING", *symbol.risk_flags]
    if set(symbol.risk_flags) & _SIDE_EFFECT_RISKS:
        return "low_confidence_needs_review", "low", sorted(set(risks))
    if symbol.return_annotation or symbol.signature:
        return "deterministic_template", "medium", sorted(set(risks))
    return "manual_required", "low", sorted(set(risks + ["UNCLEAR_RETURN_SEMANTICS"]))


def _function_text(summary: str, extra: str, symbol: RefactorSymbol) -> str:
    """Build a conservative Google-style function docstring."""
    lines = [summary, "", extra]
    params = _signature_names(symbol.signature)
    if params:
        lines.extend(["", "Args:"])
        lines.extend(f"    {name}: Review implementation before final wording." for name in params)
    if symbol.return_annotation:
        lines.extend(["", "Returns:", "    Review implementation before final wording."])
    return _triple(*lines)


def _method_text(node: ast.FunctionDef | ast.AsyncFunctionDef) -> str:
    """Build a conservative method docstring proposal."""
    lines = [f"Describe {node.name}.", "", "Generated from static method evidence; review before insertion."]
    params = [arg.arg for arg in node.args.args if arg.arg != "self"]
    if params:
        lines.extend(["", "Args:"])
        lines.extend(f"    {name}: Review implementation before final wording." for name in params)
    if node.returns is not None:
        lines.extend(["", "Returns:", "    Review implementation before final wording."])
    if _contains_explicit_raise(node):
        lines.extend(["", "Raises:", "    Review explicit raise statements before final wording."])
    return _triple(*lines)


def _signature_names(signature: str) -> list[str]:
    """Return best-effort parameter names from a symbol signature string."""
    if not signature or "(" not in signature or ")" not in signature:
        return []
    inside = signature.split("(", 1)[1].rsplit(")", 1)[0].strip()
    if not inside:
        return []
    names: list[str] = []
    for raw in inside.split(","):
        name = raw.strip().split(":", 1)[0].split("=", 1)[0].strip()
        if name and name not in {"self", "cls", "*", "/"}:
            names.append(name.lstrip("*"))
    return names


def _contains_explicit_raise(node: ast.AST) -> bool:
    """Return whether a node contains an explicit raise statement."""
    return any(isinstance(child, ast.Raise) for child in ast.walk(node))


def _triple(*lines: str) -> str:
    """Return a triple-double-quoted docstring proposal."""
    body = "\n".join(lines).strip()
    return '"""' + body + '"""'


def _proposal(
    report: ModuleAnalysisReport,
    target_kind: str,
    target_name: str,
    text: str,
    provenance: str,
    confidence: str,
    risks: list[str],
    reason: str,
) -> DocstringProposal:
    """Create one normalized proposal record."""
    return DocstringProposal(
        schema_version=SCHEMA_VERSION,
        feature_id=FEATURE_ID,
        target_file=report.target_file,
        target_kind=target_kind,
        target_name=target_name,
        proposed_docstring=text,
        provenance=provenance,
        confidence=confidence,
        risk_flags=sorted(set(risks)),
        reason=reason,
        status="review_required" if confidence == "low" else "proposed",
    )


def _assert_provenance(proposals: list[DocstringProposal]) -> None:
    """Guard against accidental unsupported provenance values."""
    for proposal in proposals:
        if proposal.provenance not in _ALLOWED_PROVENANCE:
            raise ValueError("Unsupported docstring provenance: " + proposal.provenance)
