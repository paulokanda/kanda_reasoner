# project-path: kanda_reasoner_app/project_intelligence/symbol_indexer.py
"""Read-only AST Symbol Indexer for Project Intelligence Foundation v1."""

from __future__ import annotations

import ast
from dataclasses import dataclass, field
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any, Iterable

from kanda_reasoner_app.project_exclusion_policy import iter_reasoner_project_files

from .base_engine import BaseIntelligenceEngine
from .models import (
    ADVISORY_SOURCE_TRUTH_WARNING,
    EngineFinding,
    EngineReport,
    FileSymbolSummary,
    ImportRecord,
    SymbolRecord,
)

from ._symbol_index_ast_visitor import _SymbolVisitor


@dataclass(frozen=True)
class SymbolIndexResult:
    """Complete in-memory result for the Project Intelligence Symbol Indexer."""

    report: EngineReport
    symbols: list[SymbolRecord] = field(default_factory=list)
    imports: list[ImportRecord] = field(default_factory=list)
    files: list[FileSymbolSummary] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-compatible result dictionary."""
        return {
            "report": self.report.to_dict(),
            "symbol_count": len(self.symbols),
            "import_count": len(self.imports),
            "file_count": len(self.files),
            "symbols": [item.to_dict() for item in self.symbols],
            "imports": [item.to_dict() for item in self.imports],
            "files": [item.to_dict() for item in self.files],
        }

    def to_json_text(self, *, indent: int = 2) -> str:
        """Serialize the result as JSON text without writing to disk."""
        return json.dumps(self.to_dict(), ensure_ascii=True, indent=indent)


class ProjectSymbolIndexer(BaseIntelligenceEngine):
    """Build an in-memory symbol map using deterministic AST parsing only."""

    engine_id = "project-intelligence-symbol-indexer-v1"
    engine_name = "Project Intelligence Symbol Indexer"
    engine_version = "1.0.0"

    def run_scan(
        self,
        project_root: str | Path,
        context_filter: Any = None,
        options: Any = None,
    ) -> SymbolIndexResult:
        """Return a read-only symbol index for Python files under project_root."""
        root = self._coerce_project_root(project_root)
        selected_files = self._iter_selected_files(root, context_filter=context_filter)
        symbols: list[SymbolRecord] = []
        imports: list[ImportRecord] = []
        file_summaries: list[FileSymbolSummary] = []
        warnings: list[str] = []
        errors: list[str] = []

        for file_path in selected_files:
            relative_path = self._relative_path(root, file_path)
            try:
                source_text = file_path.read_text(encoding="utf-8-sig", errors="replace")
            except OSError as exc:
                message = "Read error in " + relative_path + ": " + exc.__class__.__name__
                errors.append(message)
                file_summaries.append(
                    FileSymbolSummary(
                        file_path=relative_path,
                        function_count=0,
                        class_count=0,
                        method_count=0,
                        import_count=0,
                        syntax_error="",
                    )
                )
                continue
            try:
                tree = ast.parse(source_text, filename=str(file_path))
            except SyntaxError as exc:
                syntax_text = "line " + str(exc.lineno or "unknown")
                warnings.append("Syntax error skipped in " + relative_path + " at " + syntax_text + ".")
                file_summaries.append(
                    FileSymbolSummary(
                        file_path=relative_path,
                        function_count=0,
                        class_count=0,
                        method_count=0,
                        import_count=0,
                        syntax_error=syntax_text,
                    )
                )
                continue
            visitor = _SymbolVisitor(relative_path)
            visitor.visit(tree)
            symbols.extend(visitor.symbols)
            imports.extend(visitor.imports)
            file_summaries.append(self._file_summary(relative_path, visitor.symbols, visitor.imports))

        symbols.sort(key=lambda item: (item.file_path, item.line_number, item.name, item.symbol_type))
        imports.sort(key=lambda item: (item.file_path, item.line_number, item.module, item.imported_name))
        file_summaries.sort(key=lambda item: item.file_path)
        status = "ok"
        if errors:
            status = "failed_gracefully"
        elif warnings:
            status = "completed_with_warnings"
        elif symbols or imports:
            status = "completed_with_findings"

        summary = (
            "Project map completed. Found "
            + str(len([item for item in symbols if item.symbol_type in ("function", "async_function", "nested_function", "nested_async_function")]))
            + " functions, "
            + str(len([item for item in symbols if item.symbol_type == "class"]))
            + " classes, "
            + str(len([item for item in symbols if item.symbol_type in ("method", "async_method")]))
            + " methods, and "
            + str(len(imports))
            + " import statements across "
            + str(len(file_summaries))
            + " Python files. "
            + ADVISORY_SOURCE_TRUTH_WARNING
        )
        report = EngineReport(
            engine_id=self.engine_id,
            engine_version=self.engine_version,
            status=status,
            generated_at=datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
            project_root_label=root.name,
            summary=summary,
            findings=self._build_findings(symbols, imports, file_summaries),
            warnings=warnings,
            errors=errors,
            next_steps=[
                "Use this symbol map as advisory evidence for later Project Intelligence engines.",
                "Inspect exact source files before editing any symbol or import.",
                "Run project-specific validation before freezing or patching future integrations.",
            ],
            ai_must_not_assume=[
                ADVISORY_SOURCE_TRUTH_WARNING,
                "Do not assume runtime behavior from AST symbols alone.",
                "Do not assume validation passed because this report was generated.",
            ],
            metadata={
                "python_file_count": len(file_summaries),
                "symbol_count": len(symbols),
                "import_count": len(imports),
                "syntax_error_file_count": len([item for item in file_summaries if item.syntax_error]),
            },
        )
        return SymbolIndexResult(
            report=report,
            symbols=symbols,
            imports=imports,
            files=file_summaries,
        )

    def to_markdown(self, report: SymbolIndexResult | EngineReport) -> str:
        """Return a human-readable advisory report without writing files."""
        if isinstance(report, SymbolIndexResult):
            result = report
            engine_report = report.report
        else:
            result = None
            engine_report = report
        lines = self._standard_markdown_sections(engine_report)
        if result is not None:
            lines.extend(
                [
                    "",
                    "## Symbol summary",
                    "- Files scanned: " + str(len(result.files)),
                    "- Symbols found: " + str(len(result.symbols)),
                    "- Imports found: " + str(len(result.imports)),
                ]
            )
            syntax_files = [item.file_path for item in result.files if item.syntax_error]
            if syntax_files:
                lines.append("- Files skipped for syntax errors: " + str(len(syntax_files)))
            lines.extend(["", "## Suggested validation"])
            lines.append("- python tests/test_project_intelligence_symbol_indexer.py")
        return "\n".join(lines).strip() + "\n"

    def _iter_selected_files(self, root: Path, context_filter: Any = None) -> list[Path]:
        """Support iter selected files behavior.
        
        Parameters
        ----------
        root : Path
            The root path.
        context_filter : Any, optional
            The optional context filter value.
        
        Returns
        -------
        list[Path]
            The list of values.
        """
        
        selected = list(iter_reasoner_project_files(root, suffixes=(".py",)))
        if context_filter is None:
            return selected
        allowed = self._normalize_context_filter(root, context_filter)
        if not allowed:
            return selected
        return [item for item in selected if self._relative_path(root, item) in allowed]

    def _normalize_context_filter(self, root: Path, context_filter: Any) -> set[str]:
        """Support normalize context filter behavior.
        
        Parameters
        ----------
        root : Path
            The root path.
        context_filter : Any
            The context filter value.
        
        Returns
        -------
        set[str]
            The set result.
        """
        
        if isinstance(context_filter, (str, Path)):
            values: Iterable[Any] = [context_filter]
        else:
            try:
                values = list(context_filter)
            except TypeError:
                values = []
        allowed: set[str] = set()
        for value in values:
            candidate = Path(str(value))
            if not candidate.is_absolute():
                candidate = root / candidate
            allowed.add(self._relative_path(root, candidate))
        return allowed

    def _relative_path(self, root: Path, file_path: Path) -> str:
        """Support relative path behavior.
        
        Parameters
        ----------
        root : Path
            The root path.
        file_path : Path
            The file path.
        
        Returns
        -------
        str
            The string result.
        """
        
        try:
            return file_path.resolve(strict=False).relative_to(root).as_posix()
        except ValueError:
            return Path(file_path.name).as_posix()

    def _file_summary(
        self,
        relative_path: str,
        symbols: list[SymbolRecord],
        imports: list[ImportRecord],
    ) -> FileSymbolSummary:
        """Support file summary behavior.
        
        Parameters
        ----------
        relative_path : str
            The relative path value.
        symbols : list[SymbolRecord]
            The symbols value.
        imports : list[ImportRecord]
            The imports value.
        
        Returns
        -------
        FileSymbolSummary
            The file symbol summary result.
        """
        
        function_types = {"function", "async_function", "nested_function", "nested_async_function"}
        method_types = {"method", "async_method"}
        return FileSymbolSummary(
            file_path=relative_path,
            function_count=len([item for item in symbols if item.symbol_type in function_types]),
            class_count=len([item for item in symbols if item.symbol_type == "class"]),
            method_count=len([item for item in symbols if item.symbol_type in method_types]),
            import_count=len(imports),
            syntax_error="",
        )

    def _build_findings(
        self,
        symbols: list[SymbolRecord],
        imports: list[ImportRecord],
        files: list[FileSymbolSummary],
    ) -> list[EngineFinding]:
        """Support build findings behavior.
        
        Parameters
        ----------
        symbols : list[SymbolRecord]
            The symbols value.
        imports : list[ImportRecord]
            The imports value.
        files : list[FileSymbolSummary]
            The files value.
        
        Returns
        -------
        list[EngineFinding]
            The list of values.
        """
        
        findings: list[EngineFinding] = []
        syntax_files = [item for item in files if item.syntax_error]
        if syntax_files:
            findings.append(
                EngineFinding(
                    finding_id="symbol-indexer-syntax-errors",
                    severity="warning",
                    category="syntax",
                    title="Some Python files could not be parsed",
                    message="The indexer skipped files with syntax errors and continued safely.",
                    file_path=syntax_files[0].file_path,
                    line_number=0,
                    evidence="syntax_error_file_count=" + str(len(syntax_files)),
                    recommendation="Inspect syntax-error files before relying on a complete project map.",
                )
            )
        missing_docstrings = [
            item for item in symbols
            if item.symbol_type in {"function", "async_function", "class", "method", "async_method"}
            and not item.has_docstring
        ]
        if missing_docstrings:
            first = missing_docstrings[0]
            findings.append(
                EngineFinding(
                    finding_id="symbol-indexer-missing-docstrings",
                    severity="advisory",
                    category="documentation",
                    title="Some symbols have no docstring",
                    message="The symbol map found public or internal definitions without docstrings.",
                    file_path=first.file_path,
                    line_number=first.line_number,
                    evidence="missing_docstring_count=" + str(len(missing_docstrings)),
                    recommendation="Use Docstring Assistant or exact source review if docstring quality matters for the task.",
                )
            )
        if symbols or imports:
            findings.append(
                EngineFinding(
                    finding_id="symbol-indexer-map-ready",
                    severity="info",
                    category="project_map",
                    title="Project symbol map is available",
                    message="The indexer produced reusable symbol and import evidence for later engines.",
                    file_path="",
                    line_number=0,
                    evidence="symbols=" + str(len(symbols)) + "; imports=" + str(len(imports)),
                    recommendation="Use this as advisory evidence only; inspect exact source before edits.",
                )
            )
        return findings
