# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/analysis_formatting.py
"""Text formatting helpers for large-file planner AST evidence."""
from __future__ import annotations

from .models import ModuleAnalysisReport

__all__ = ["format_analysis_report"]


def format_analysis_report(report: ModuleAnalysisReport) -> str:
    """Return a readable analysis summary for the GUI evidence panel."""
    lines: list[str] = []
    lines.append("AST analysis evidence")
    lines.append("")
    lines.append(f"Target file: {report.target_file}")
    lines.append(f"Physical lines: {report.line_count_physical}")
    lines.append(f"Source hash: {report.source_content_hash}")
    lines.append(f"Module docstring: {_yes_no(report.module_docstring_present)}")
    if report.module_docstring_preview:
        lines.append(f"Module docstring preview: {report.module_docstring_preview}")
    lines.append(f"__all__ detected: {_yes_no(bool(report.all_names))}")
    lines.append(f"Public API symbols: {_join_or_none(report.public_api_symbols)}")
    lines.append(f"Top-level symbols: {len(report.symbols)}")
    lines.append(f"Imports: {len(report.imports)}")
    lines.append(f"Constants: {_join_or_none(report.constants)}")
    lines.append(f"Assignments: {_join_or_none(report.assignments)}")
    lines.append(f"Global statements: {_join_or_none(report.global_statements)}")
    lines.append(f"Nonlocal statements: {_join_or_none(report.nonlocal_statements)}")
    lines.append(f"Module-level calls: {_join_or_none(report.module_level_calls)}")
    lines.append(f"if __name__ == '__main__': {_yes_no(report.if_main_present)}")
    lines.append(f"Nested symbols: {report.nested_symbol_count}")
    lines.append(f"Missing docstrings: {report.missing_docstring_count}")
    lines.append(f"Risk badges: {_join_or_none(report.risk_flags)}")
    if report.analysis_errors:
        lines.append("")
        lines.append("Analysis errors")
        lines.extend(f"- {item}" for item in report.analysis_errors)
    lines.append("")
    lines.append("Imports")
    lines.extend(_format_imports(report))
    lines.append("")
    lines.append("Symbols")
    lines.extend(_format_symbols(report))
    lines.append("")
    lines.append("No-leak status")
    lines.append("- Read-only AST analysis only.")
    lines.append("- No preview files were written.")
    lines.append("- No project split files were generated.")
    lines.append("- Patch creation remains blocked until later validation trains.")
    return "\n".join(lines)


def _format_imports(report: ModuleAnalysisReport) -> list[str]:
    """Return formatted import evidence lines."""
    if not report.imports:
        return ["- none"]
    lines: list[str] = []
    for item in report.imports[:80]:
        risk = f" [{', '.join(item.risk_flags)}]" if item.risk_flags else ""
        alias = f" as {item.alias}" if item.alias else ""
        span = f"L{item.line_span[0]}-L{item.line_span[1]}"
        lines.append(f"- {item.imported_name}{alias} ({span}){risk}")
    if len(report.imports) > 80:
        lines.append(f"- ... {len(report.imports) - 80} more imports omitted")
    return lines


def _format_symbols(report: ModuleAnalysisReport) -> list[str]:
    """Return formatted symbol evidence lines."""
    if not report.symbols:
        return ["- none"]
    lines: list[str] = []
    for symbol in report.symbols:
        doc = "docstring" if symbol.has_docstring else "missing docstring"
        risks = f" [{', '.join(symbol.risk_flags)}]" if symbol.risk_flags else ""
        lines.append(
            f"- {symbol.kind} {symbol.name} "
            f"L{symbol.start_line}-L{symbol.end_line} "
            f"({symbol.physical_lines} lines, {symbol.visibility}, {doc}){risks}"
        )
        if symbol.signature:
            lines.append(f"  signature: {symbol.signature}")
        if symbol.references:
            lines.append(f"  references: {_join_or_none(symbol.references[:20])}")
    return lines


def _yes_no(value: bool) -> str:
    """Return yes/no for Boolean evidence."""
    return "yes" if value else "no"


def _join_or_none(values: list[str] | tuple[str, ...]) -> str:
    """Return a compact comma-separated list or none."""
    return ", ".join(values) if values else "none"
