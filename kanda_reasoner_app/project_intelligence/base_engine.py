# project-path: kanda_reasoner_app/project_intelligence/base_engine.py
"""Base contract for deterministic Project Intelligence engines."""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

from .models import ADVISORY_SOURCE_TRUTH_WARNING, EngineReport


class EngineExecutionError(RuntimeError):
    """Raised when an engine cannot complete its scan safely."""


class BaseIntelligenceEngine(ABC):
    """Shared read-only interface for Project Intelligence engines."""

    engine_id = "base-intelligence-engine"
    engine_name = "Base Intelligence Engine"
    engine_version = "0.0.0"

    @abstractmethod
    def run_scan(
        self,
        project_root: str | Path,
        context_filter: Any = None,
        options: Any = None,
    ) -> Any:
        """Run a deterministic scan and return a JSON-safe report object."""
        raise NotImplementedError

    @abstractmethod
    def to_markdown(self, report: Any) -> str:
        """Render a report object as advisory human-readable text."""
        raise NotImplementedError

    def _coerce_project_root(self, project_root: str | Path) -> Path:
        """Return an existing project root path or raise a localized error."""
        root = Path(project_root).expanduser().resolve(strict=False)
        if not root.exists():
            raise EngineExecutionError("Project root does not exist: " + str(project_root))
        if not root.is_dir():
            raise EngineExecutionError("Project root is not a directory: " + str(project_root))
        return root

    def _standard_markdown_sections(self, report: EngineReport) -> list[str]:
        """Return common markdown sections for all advisory engine reports."""
        data = report.to_dict()
        lines = [
            "# " + self.engine_name,
            "",
            "## What this found",
            str(data.get("summary") or "No summary was provided."),
            "",
            "## Why it matters",
            ADVISORY_SOURCE_TRUTH_WARNING,
            "",
            "## What to inspect next",
        ]
        next_steps = data.get("next_steps") or []
        if next_steps:
            lines.extend("- " + str(item) for item in next_steps)
        else:
            lines.append("- Inspect the exact source files before editing.")
        lines.extend(["", "## What an AI must not assume"])
        for item in data.get("ai_must_not_assume") or [ADVISORY_SOURCE_TRUTH_WARNING]:
            lines.append("- " + str(item))
        lines.extend(["", "## Findings"])
        findings = data.get("findings") or []
        if findings:
            for finding in findings:
                lines.append(
                    "- ["
                    + str(finding.get("severity", "info"))
                    + "] "
                    + str(finding.get("title", "Finding"))
                    + " - "
                    + str(finding.get("file_path", ""))
                    + ":"
                    + str(finding.get("line_number", 0))
                )
        else:
            lines.append("- No advisory findings were produced.")
        lines.extend(["", "## Warnings"])
        warnings = data.get("warnings") or []
        if warnings:
            lines.extend("- " + str(item) for item in warnings)
        else:
            lines.append("- No warnings were produced.")
        lines.extend(["", "## Errors"])
        errors = data.get("errors") or []
        if errors:
            lines.extend("- " + str(item) for item in errors)
        else:
            lines.append("- No engine errors were produced.")
        lines.extend(["", "## Suggested validation"])
        lines.append("- Run the patch-specific validation command before freezing or editing.")
        return lines
