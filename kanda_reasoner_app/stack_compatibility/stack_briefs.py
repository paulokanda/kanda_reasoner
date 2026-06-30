# project-path: kanda_reasoner_app/stack_compatibility/stack_briefs.py
"""Build read-only stack compatibility briefs."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import re
from typing import Iterable

STACK_COMPATIBILITY_RISK_LEVELS = ("low", "medium", "high")

_HIGH_RISK_TOKENS = {
    "pyside6": "Qt/PySide GUI compatibility can affect startup and widget behavior.",
    "pyqt": "Qt binding compatibility can affect GUI imports and runtime behavior.",
    "mne": "MNE compatibility can affect EEG data loading and signal processing.",
    "numpy": "NumPy compatibility can affect numerical pipelines and binary wheels.",
    "scipy": "SciPy compatibility can affect signal processing and binary wheels.",
    "torch": "Torch compatibility can affect CUDA and local ML runtime behavior.",
    "cuda": "CUDA compatibility can affect GPU-backed runtime behavior.",
    "ollama": "Local AI runtime compatibility can affect model discovery and calls.",
    "llama": "Local AI runtime compatibility can affect model execution.",
}

_PINNED_RE = re.compile(r"^[A-Za-z0-9_.-]+==[^=].*$")
_UNPINNED_RE = re.compile(r"^[A-Za-z0-9_.-]+(?:\s*(?:#.*)?)$")


@dataclass(frozen=True)
class StackCompatibilityFinding:
    """A single compatibility risk finding."""

    code: str
    package: str
    risk_level: str
    rationale: str
    suggested_action: str
    source: str = "requirements"

    def as_dict(self) -> dict[str, str]:
        """Return a JSON-serializable dictionary."""
        return {
            "code": self.code,
            "package": self.package,
            "risk_level": self.risk_level,
            "rationale": self.rationale,
            "suggested_action": self.suggested_action,
            "source": self.source,
        }


@dataclass(frozen=True)
class StackCompatibilityReport:
    """A read-only stack compatibility report."""

    report_type: str = "stack_compatibility_brief"
    risk_level: str = "low"
    summary: str = "No high-risk stack compatibility signals were found."
    findings: tuple[StackCompatibilityFinding, ...] = field(default_factory=tuple)
    tests_to_run: tuple[str, ...] = field(default_factory=tuple)

    def as_dict(self) -> dict[str, object]:
        """Return a JSON-serializable dictionary."""
        return {
            "report_type": self.report_type,
            "risk_level": self.risk_level,
            "summary": self.summary,
            "findings": [finding.as_dict() for finding in self.findings],
            "tests_to_run": list(self.tests_to_run),
        }


def _normalize_requirement_name(line: str) -> str:
    """Support normalize requirement name behavior.
    
    Parameters
    ----------
    line : str
        The line value.
    
    Returns
    -------
    str
        The string result.
    """
    
    cleaned = line.strip().split("#", 1)[0].strip()
    for separator in ("==", ">=", "<=", "~=", "!=", ">", "<"):
        if separator in cleaned:
            return cleaned.split(separator, 1)[0].strip().lower()
    return cleaned.strip().lower()


def _is_relevant_line(line: str) -> bool:
    """Support is relevant line behavior.
    
    Parameters
    ----------
    line : str
        The line value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    stripped = line.strip()
    return bool(stripped and not stripped.startswith("#") and not stripped.startswith("-"))


def _risk_for_requirement(line: str) -> StackCompatibilityFinding | None:
    """Support risk for requirement behavior.
    
    Parameters
    ----------
    line : str
        The line value.
    
    Returns
    -------
    StackCompatibilityFinding | None
        The stack compatibility finding result.
    """
    
    name = _normalize_requirement_name(line)
    if not name:
        return None

    for token, rationale in _HIGH_RISK_TOKENS.items():
        if token in name:
            return StackCompatibilityFinding(
                code="HIGH_RISK_STACK_PACKAGE",
                package=name,
                risk_level="medium",
                rationale=rationale,
                suggested_action="Confirm version, Python compatibility, and import smoke before upgrading.",
            )

    cleaned = line.strip().split("#", 1)[0].strip()
    if _UNPINNED_RE.match(cleaned):
        return StackCompatibilityFinding(
            code="UNPINNED_REQUIREMENT",
            package=name,
            risk_level="medium",
            rationale="Unpinned dependency can change between installs and break reproducibility.",
            suggested_action="Pin or document an accepted version range before release.",
        )

    if _PINNED_RE.match(cleaned):
        return None

    return StackCompatibilityFinding(
        code="VERSION_RANGE_REQUIREMENT",
        package=name,
        risk_level="low",
        rationale="Version range should be checked against the local runtime before broad updates.",
        suggested_action="Run import smoke and project validators after dependency changes.",
    )


def _overall_risk(findings: Iterable[StackCompatibilityFinding]) -> str:
    """Support overall risk behavior.
    
    Parameters
    ----------
    findings : Iterable[StackCompatibilityFinding]
        The findings value.
    
    Returns
    -------
    str
        The string result.
    """
    
    levels = [finding.risk_level for finding in findings]
    if "high" in levels:
        return "high"
    if "medium" in levels:
        return "medium"
    return "low"


def build_stack_compatibility_brief(
    requirement_lines: Iterable[str],
    *,
    python_version: str | None = None,
) -> StackCompatibilityReport:
    """Build a read-only compatibility brief from requirement lines."""
    findings = []
    for line in requirement_lines:
        if not _is_relevant_line(line):
            continue
        finding = _risk_for_requirement(line)
        if finding is not None:
            findings.append(finding)

    if python_version and not python_version.startswith("3.10"):
        findings.append(
            StackCompatibilityFinding(
                code="PYTHON_VERSION_CHECK_REQUIRED",
                package="python",
                risk_level="medium",
                rationale="Kanda Reasoner development targets Python 3.10-compatible code.",
                suggested_action="Validate project import smoke and package compatibility on this Python version.",
                source="runtime",
            )
        )

    findings_tuple = tuple(findings)
    risk_level = _overall_risk(findings_tuple)
    summary = (
        "Stack compatibility risks were found. Review before dependency or runtime updates."
        if findings_tuple
        else "No high-risk stack compatibility signals were found."
    )
    tests_to_run = (
        r"python kanda_reasoner_app\manage_architecture\manage_architecture.py --root <PROJECT_ROOT> --validate",
        r"python kanda_reasoner_app\manage_workflows\manage_workflows.py --root <PROJECT_ROOT> --validate",
        "python -c \"import kanda_reasoner_app; import reasoner_tools_gui; print('import smoke ok')\"",
    )
    return StackCompatibilityReport(
        risk_level=risk_level,
        summary=summary,
        findings=findings_tuple,
        tests_to_run=tests_to_run,
    )


def render_stack_compatibility_markdown(report: StackCompatibilityReport) -> str:
    """Render a stack compatibility report as Markdown."""
    lines = [
        "# Stack Compatibility Brief",
        "",
        "Risk level: " + report.risk_level,
        "",
        report.summary,
        "",
        "## Findings",
    ]
    if not report.findings:
        lines.append("- None")
    for finding in report.findings:
        lines.append(
            "- "
            + finding.code
            + " | "
            + finding.package
            + " | "
            + finding.risk_level
            + " | "
            + finding.rationale
        )
    lines.extend(["", "## Tests to run"])
    for command in report.tests_to_run:
        lines.append("- " + command)
    return "\n".join(lines) + "\n"


def default_stack_compatibility_output_dir(project_root: str | Path) -> Path:
    """Return the default stack compatibility report directory."""
    return Path(project_root) / "workbench" / "stack_compatibility_reports"


__all__ = [
    "STACK_COMPATIBILITY_RISK_LEVELS",
    "StackCompatibilityFinding",
    "StackCompatibilityReport",
    "build_stack_compatibility_brief",
    "default_stack_compatibility_output_dir",
    "render_stack_compatibility_markdown",
]
