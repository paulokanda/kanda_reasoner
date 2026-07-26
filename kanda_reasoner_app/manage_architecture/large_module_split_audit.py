# project-path: kanda_reasoner_app/manage_architecture/large_module_split_audit.py
"""Read-only AST split audit for large-module refactor planning.

The tool gives Architecture Review a deterministic evidence report for AI/human
heuristic splitting. It does not refactor, modify source files, or write frozen
memory. Reports are written only to the project daily-work staging area.
"""
from __future__ import annotations

import argparse
import ast
import json
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from kanda_reasoner_app.manage_architecture._large_module_split_audit_analysis import (
    _audit_symbol,
    _group_islands,
    _independence_matrix,
    _iter_auditable_symbols,
    _recommend_patch_shape,
)
from kanda_reasoner_app.manage_architecture.large_module_split_safety_classifier import (
    classify_refactor_safety,
)

__all__ = [
    "IslandAudit",
    "LargeModuleSplitAuditResult",
    "SymbolAudit",
    "run_large_module_split_audit",
]


@dataclass(slots=True)
class SymbolAudit:
    """Public compatibility record for AST-derived symbol evidence."""

    kind: str
    name: str
    qualname: str
    line_start: int
    line_end: int
    line_count: int
    called_self_methods: list[str] = field(default_factory=list)
    self_attr_reads: list[str] = field(default_factory=list)
    self_attr_writes: list[str] = field(default_factory=list)
    imports_used: list[str] = field(default_factory=list)
    gui_touches: list[str] = field(default_factory=list)
    side_effects: list[str] = field(default_factory=list)
    candidate_island: str = "general"
    risk: str = "low"

    def as_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable representation of the symbol audit."""
        return {
            "kind": self.kind,
            "name": self.name,
            "qualname": self.qualname,
            "line_start": self.line_start,
            "line_end": self.line_end,
            "line_count": self.line_count,
            "called_self_methods": self.called_self_methods,
            "self_attr_reads": self.self_attr_reads,
            "self_attr_writes": self.self_attr_writes,
            "imports_used": self.imports_used,
            "gui_touches": self.gui_touches,
            "side_effects": self.side_effects,
            "candidate_island": self.candidate_island,
            "risk": self.risk,
        }


@dataclass(slots=True)
class IslandAudit:
    """Public compatibility record for grouped responsibility-island evidence."""

    name: str
    symbols: list[SymbolAudit]
    line_count: int
    self_attr_reads: list[str]
    self_attr_writes: list[str]
    gui_touches: list[str]
    side_effects: list[str]
    risk: str

    def as_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable representation of the island audit."""
        return {
            "name": self.name,
            "symbols": [symbol.qualname for symbol in self.symbols],
            "line_count": self.line_count,
            "self_attr_reads": self.self_attr_reads,
            "self_attr_writes": self.self_attr_writes,
            "gui_touches": self.gui_touches,
            "side_effects": self.side_effects,
            "risk": self.risk,
        }


@dataclass(slots=True)
class LargeModuleSplitAuditResult:
    """Markdown/JSON payload returned by the split-audit runner."""

    target_path: Path
    project_root: Path
    markdown: str
    data: dict[str, Any]
    markdown_path: Path
    json_path: Path


def _import_aliases(tree: ast.AST) -> dict[str, str]:
    """Support import aliases behavior.
    
    Parameters
    ----------
    tree : ast.AST
        The parsed syntax tree.
    
    Returns
    -------
    dict[str, str]
        The mapped values.
    """
    
    aliases: dict[str, str] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                key = alias.asname or alias.name.split(".", 1)[0]
                aliases[key] = alias.name
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            for alias in node.names:
                if alias.name == "*":
                    aliases["*"] = module + ".*"
                    continue
                key = alias.asname or alias.name
                aliases[key] = f"{module}.{alias.name}" if module else alias.name
    return aliases


def run_large_module_split_audit(
    project_root: str | Path,
    target_path: str | Path,
    classifier_mode: str = "heuristic",
) -> LargeModuleSplitAuditResult:
    """Run a read-only AST split audit and write Markdown/JSON to daily-work staging."""
    project = Path(project_root).resolve()
    target = _resolve_target(project, Path(target_path))
    if not target.exists():
        raise FileNotFoundError(f"Target module not found: {target}")
    if target.suffix != ".py":
        raise ValueError(f"Target must be a Python file: {target}")
    source = target.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(target))
    imports = _import_aliases(tree)
    symbols = [_audit_symbol(node, imports) for node in _iter_auditable_symbols(tree)]
    islands = _group_islands(symbols)
    matrix = _independence_matrix(islands)
    recommendation = _recommend_patch_shape(islands, matrix)
    rel_target = _safe_relative(target, project)
    generated_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    data: dict[str, Any] = {
        "schema_version": "1.0",
        "kind": "large_module_ast_split_audit",
        "generated_at_utc": generated_at,
        "project_root": str(project),
        "target_path": str(target),
        "target_relative_path": rel_target,
        "line_count": len(source.splitlines()),
        "symbol_count": len(symbols),
        "islands": [island.as_dict() for island in islands],
        "symbols": [symbol.as_dict() for symbol in symbols],
        "independence_matrix": matrix,
        "recommendation": recommendation,
        "caveat": "Read-only AST evidence. AI/human review must confirm islands before implementation.",
    }
    data["refactor_safety_classification"] = classify_refactor_safety(
        project,
        target,
        source,
        tree,
        data,
        classifier_mode=classifier_mode,
    )
    markdown = _format_markdown(data)
    out_dir = _daily_work_dir(project) / "large_module_split_audits"
    out_dir.mkdir(parents=True, exist_ok=True)
    safe_stem = _safe_filename(target.stem)
    md_path = out_dir / f"{safe_stem}_ast_split_audit.md"
    json_path = out_dir / f"{safe_stem}_ast_split_audit.json"
    md_path.write_text(markdown, encoding="utf-8")
    json_path.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")
    return LargeModuleSplitAuditResult(
        target_path=target,
        project_root=project,
        markdown=markdown,
        data=data,
        markdown_path=md_path,
        json_path=json_path,
    )


def _resolve_target(project_root: Path, target_path: Path) -> Path:
    """Support resolve target behavior.
    
    Parameters
    ----------
    project_root : Path
        The project root path.
    target_path : Path
        The target path value.
    
    Returns
    -------
    Path
        The resolved path.
    """
    
    target = (
        target_path.resolve()
        if target_path.is_absolute()
        else (project_root / target_path).resolve()
    )
    root = project_root.resolve()
    try:
        target.relative_to(root)
    except ValueError as exc:
        raise ValueError("TARGET_OUTSIDE_ACTIVE_PROJECT_ROOT") from exc
    return target


def _safe_relative(path: Path, root: Path) -> str:
    """Support safe relative behavior.
    
    Parameters
    ----------
    path : Path
        The file or folder path.
    root : Path
        The root path.
    
    Returns
    -------
    str
        The string result.
    """
    
    try:
        return str(path.relative_to(root)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def _daily_work_dir(project_root: Path) -> Path:
    """Support daily work dir behavior.
    
    Parameters
    ----------
    project_root : Path
        The project root path.
    
    Returns
    -------
    Path
        The resolved path.
    """
    
    drive = Path(project_root.anchor) if project_root.anchor else project_root.parent
    return drive / f"{project_root.name}_delete_after_daily_work"


def _safe_filename(value: str) -> str:
    """Support safe filename behavior.
    
    Parameters
    ----------
    value : str
        The input value.
    
    Returns
    -------
    str
        The string result.
    """
    
    text = re.sub(r"[^A-Za-z0-9_.-]+", "_", value).strip("._")
    return text or "large_module"


def _format_markdown(data: dict[str, Any]) -> str:
    """Support format markdown behavior.
    
    Parameters
    ----------
    data : dict[str, Any]
        The input data.
    
    Returns
    -------
    str
        The string result.
    """
    
    lines = [
        "# Large Module AST Split Audit",
        "",
        f"Generated: `{data['generated_at_utc']}`",
        f"Project root: `{data['project_root']}`",
        f"Target: `{data['target_relative_path']}`",
        f"Line count: `{data['line_count']}`",
        f"Audited symbols: `{data['symbol_count']}`",
        "",
    ]
    classification = data.get("refactor_safety_classification", {})
    lines.extend(_format_safety_section(classification))
    lines.extend([
        "## Candidate islands",
        "",
    ])
    for island in data["islands"]:
        lines.extend([
            f"### {island['name']}",
            "",
            f"Risk: `{island['risk']}`",
            f"Estimated lines: `{island['line_count']}`",
            "Methods/symbols:",
        ])
        for symbol in island["symbols"]:
            lines.append(f"- `{symbol}`")
        lines.extend([
            f"Self reads: `{', '.join(island['self_attr_reads']) or 'none'}`",
            f"Self writes: `{', '.join(island['self_attr_writes']) or 'none'}`",
            f"GUI touches: `{', '.join(island['gui_touches']) or 'none'}`",
            f"Side effects: `{', '.join(island['side_effects']) or 'none'}`",
            "",
        ])
    lines.extend(["## Independence matrix", ""])
    if data["independence_matrix"]:
        for row in data["independence_matrix"]:
            reasons = "; ".join(row["reasons"]) if row["reasons"] else "no conflicts detected by AST heuristic"
            lines.append(f"- `{row['left']}` x `{row['right']}`: **{row['relation']}** - {reasons}")
    else:
        lines.append("- Not enough islands for pairwise comparison.")
    recommendation = data["recommendation"]
    lines.extend([
        "",
        "## Recommended patch composition",
        "",
        f"Mode: `{recommendation.get('mode', '')}`",
        f"Islands: `{', '.join(recommendation.get('islands', [])) or 'none'}`",
        f"Reason: {recommendation.get('reason', '')}",
        "",
        "## AI handoff instruction",
        "",
        "Use this read-only AST evidence to build the Task 0 candidate-island queue and Task 1 patch-composition decision. Do not implement until AI/human review confirms the islands, independence result, validation gates, and freeze naming.",
    ])
    return "\n".join(lines) + "\n"


def _format_safety_section(classification: dict[str, Any]) -> list[str]:
    """Format the read-only refactor safety classifier result."""
    if not classification:
        return [
            "## Refactor safety classification",
            "",
            "Label: `not audited`",
            "",
        ]
    lines = [
        "## Refactor safety classification",
        "",
        f"Label: **{classification.get('label', 'not audited')}**",
        f"Engine: `{classification.get('engine', '')}`",
        f"Score: `{classification.get('score', '')}`",
        "",
    ]
    blockers = classification.get("hard_blockers") or []
    warnings = classification.get("warnings") or []
    if blockers:
        lines.append("Hard blockers:")
        for blocker in blockers:
            lines.append(f"- {blocker}")
    else:
        lines.append("Hard blockers: `none detected`")
    lines.append("")
    if warnings:
        lines.append("Warnings:")
        for warning in warnings:
            lines.append(f"- {warning}")
    else:
        lines.append("Warnings: `none detected`")
    ruff = classification.get("ruff") or {}
    if ruff:
        lines.extend([
            "",
            "Static tool status:",
            f"- Ruff available: `{bool(ruff.get('available'))}`",
            f"- Ruff used: `{bool(ruff.get('used'))}`",
            f"- Message: {ruff.get('message', '')}",
        ])
    lines.append("")
    return lines


def main(argv: list[str] | None = None) -> int:
    """Support main behavior.
    
    Parameters
    ----------
    argv : list[str] | None, optional
        The optional argv value.
    
    Returns
    -------
    int
        The integer status code.
    """
    
    parser = argparse.ArgumentParser(description="Run read-only AST split audit for one Python module.")
    parser.add_argument("--root", required=True, help="Project root")
    parser.add_argument("--target", required=True, help="Target .py file, absolute or relative to project root")
    parser.add_argument(
        "--classifier-mode",
        choices=("heuristic", "static_tools"),
        default="heuristic",
        help="Refactor safety classifier mode",
    )
    args = parser.parse_args(argv)
    result = run_large_module_split_audit(
        args.root,
        args.target,
        classifier_mode=args.classifier_mode,
    )
    print(result.markdown)
    print(f"Markdown report: {result.markdown_path}")
    print(f"JSON report: {result.json_path}")
    return 0
