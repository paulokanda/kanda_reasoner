# project-path: kanda_reasoner_app/project_intelligence/risk_radar.py
"""Deterministic path-based risk radar for proposed project changes."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from .base_engine import BaseIntelligenceEngine
from .models import ADVISORY_SOURCE_TRUTH_WARNING, EngineFinding, EngineReport
from .report_formatter import EngineReportFormatter

__all__ = [
    "RiskRule",
    "RiskRadarResult",
    "RiskChangeRadar",
]


@dataclass(frozen=True)
class RiskRule:
    """One deterministic path rule used by Risk Change Radar v1."""

    category: str
    severity: str
    title: str
    tokens: tuple[str, ...]
    recommendation: str


@dataclass(frozen=True)
class RiskRadarResult:
    """Structured output from Risk Change Radar v1."""

    report: EngineReport
    scanned_paths: tuple[str, ...]
    matched_categories: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-compatible result dictionary."""
        return {
            "report": self.report.to_dict(),
            "scanned_paths": list(self.scanned_paths),
            "matched_categories": list(self.matched_categories),
        }


DEFAULT_RISK_RULES: tuple[RiskRule, ...] = (
    RiskRule(
        category="startup-delivery",
        severity="high",
        title="Startup delivery path touched",
        tokens=(
            "first_prompt_files/",
            "first_prompts_to_ai.zip",
            "tell_ai_read_before_all.md",
            "zz_read_only_if_modifying_startup_delivery.md",
            "startup_routing_kernel_sources.json",
            "sync_startup_routing_kernel_pack.py",
            "startup_prompt_request_kernel_manifest.json",
        ),
        recommendation=(
            "Route through startup-delivery maintenance prompts and validate startup regeneration."
        ),
    ),
    RiskRule(
        category="freeze-memory",
        severity="high",
        title="Freeze memory or freeze workflow path touched",
        tokens=(
            "project_freeze_after_update/",
            "freeze_after_update/",
            "freeze_hint_intake/",
            "frozen_features_memory/",
            "project_freeze_ledger",
        ),
        recommendation=(
            "Preserve Preview as read-only and Confirm and Write as explicitly human-confirmed."
        ),
    ),
    RiskRule(
        category="error-memory",
        severity="high",
        title="Error Memory path touched",
        tokens=(
            "project_error_memory/",
            "error_memory/",
            "error_lessons_compact",
            "error_memory_manifest",
            "kanda_error_lesson_json",
        ),
        recommendation=(
            "Use compact Error Memory first; do not edit or promote lessons without the intake contract."
        ),
    ),
    RiskRule(
        category="prompt-routing",
        severity="high",
        title="Prompt library or routing path touched",
        tokens=(
            "prompt_library/",
            "active_prompts/",
            "prompt_router.md",
            "prompt_navigation_index.md",
            "kanda_routing_system_canon.md",
            "metadata/",
            "groups/",
            "routing/",
        ),
        recommendation=(
            "Audit overlap, metadata, indexes, router bridges, and validation before delivery."
        ),
    ),
    RiskRule(
        category="patch-delivery",
        severity="high",
        title="Patch delivery or installer path touched",
        tokens=(
            "validate_patch_zip.py",
            "validate_ai_response_patch_delivery.py",
            "patch_governance/",
            "patch_delivery",
            "install_block.ps1",
            ".ps1",
            "_patch.zip",
            "kanda_freeze_hint.json",
        ),
        recommendation=(
            "Require ZIP contract validation, daily-work staging, install block, validation block, and freeze handling."
        ),
    ),
    RiskRule(
        category="gui-workflow",
        severity="warning",
        title="GUI or tab workflow path touched",
        tokens=(
            "gui",
            "tab",
            "panel",
            "pyside",
            "pyqt",
            "main_window",
            "tool_specs.py",
            "reasoner_tools_gui",
        ),
        recommendation=(
            "Inspect callbacks, worker behavior, visible labels, and confirmation gates before release."
        ),
    ),
    RiskRule(
        category="validation-contract",
        severity="warning",
        title="Validation path touched",
        tokens=(
            "tests/",
            "validation/",
            "validate_",
            "test_",
            "pytest.ini",
            "tox.ini",
            "pyproject.toml",
        ),
        recommendation=(
            "Run the feature-specific validation and keep expected markers, including STATUS: IN_SYNC when required."
        ),
    ),
    RiskRule(
        category="root-cleanliness",
        severity="warning",
        title="Root cleanliness or transient artifact risk",
        tokens=(
            "_delete_after_daily_work",
            "temp/",
            "tmp/",
            "scratch/",
            "staging/",
            "extract/",
            "backup/",
            "cache/",
        ),
        recommendation=(
            "Keep transient files outside the active project root and stage under the project daily-work folder."
        ),
    ),
    RiskRule(
        category="generated-evidence",
        severity="warning",
        title="Generated evidence or handoff output touched",
        tokens=(
            "_show_project_to_ai/",
            "second_prompt_files/",
            "ai_handoff_upload",
            "source_archive_part",
            "png_assets_part",
            "__pycache__/",
            ".pyc",
        ),
        recommendation=(
            "Treat generated evidence as advisory output, not canonical source for patching."
        ),
    ),
    RiskRule(
        category="unsafe-operation",
        severity="warning",
        title="Potential unsafe-operation implementation path touched",
        tokens=(
            "subprocess",
            "zipfile",
            "shutil.rmtree",
            "delete",
            "remove_item",
            "archive",
            "extractall",
            "shell=true",
        ),
        recommendation=(
            "Inspect exact source for shell, archive extraction, broad delete, and path traversal risk."
        ),
    ),
)


class RiskChangeRadar(BaseIntelligenceEngine):
    """Classify proposed changed paths against deterministic governance risk rules."""

    engine_id = "project-intelligence-risk-radar"
    engine_name = "Project Intelligence Risk Change Radar"
    engine_version = "1.0.0"

    def __init__(self, rules: Iterable[RiskRule] | None = None) -> None:
        """Support init behavior.
        
        Parameters
        ----------
        rules : Iterable[RiskRule] | None, optional
            The optional rules value.
        """
        
        self.rules = tuple(rules or DEFAULT_RISK_RULES)

    def run_scan(
        self,
        project_root: str | Path,
        context_filter: Any = None,
        options: Any = None,
    ) -> RiskRadarResult:
        """Analyze selected changed paths without reading or writing project files."""
        root = self._coerce_project_root(project_root)
        changed_paths = self._collect_changed_paths(context_filter, options)
        normalized_paths = tuple(self._normalize_path(path, root) for path in changed_paths)
        normalized_paths = tuple(path for path in normalized_paths if path)

        warnings: list[str] = []
        if not normalized_paths:
            warnings.append(
                "No changed paths were provided. Risk Radar v1 analyzes selected paths only."
            )

        findings = self._build_findings(normalized_paths)
        categories = tuple(sorted({finding.category for finding in findings}))
        status = "completed_with_findings" if findings else "ok"
        summary = self._summary_text(len(normalized_paths), findings)
        report = EngineReport(
            engine_id=self.engine_id,
            engine_version=self.engine_version,
            status=status,
            generated_at=datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
            project_root_label=root.name,
            summary=summary,
            findings=findings,
            warnings=warnings,
            errors=[],
            next_steps=self._next_steps(findings),
            ai_must_not_assume=[
                ADVISORY_SOURCE_TRUTH_WARNING,
                "Risk Radar v1 does not prove a patch is safe or unsafe by itself.",
                "Exact source files and validation output must be inspected before editing or freezing.",
                "Path-based risk matches are advisory and may need human review.",
            ],
            metadata={
                "scanned_path_count": len(normalized_paths),
                "finding_count": len(findings),
                "matched_categories": list(categories),
                "rule_count": len(self.rules),
                "mode": "path_based_v1",
            },
        )
        return RiskRadarResult(
            report=report,
            scanned_paths=normalized_paths,
            matched_categories=categories,
        )

    def to_markdown(self, report: RiskRadarResult | EngineReport) -> str:
        """Return a deterministic human-readable risk report."""
        engine_report = report.report if isinstance(report, RiskRadarResult) else report
        formatter = EngineReportFormatter(max_findings=50)
        return formatter.format_report(
            engine_report,
            title="Project Intelligence Risk Change Radar v1",
            suggested_validation=(
                "Run the patch-specific validation command.",
                "Run scripts/validate_patch_zip.py on the staged patch ZIP when delivering a patch.",
                "Inspect exact source files for every high-risk path before editing.",
            ),
        )

    def _collect_changed_paths(self, context_filter: Any, options: Any) -> list[str]:
        """Collect changed paths from context_filter or options without scanning."""
        candidates: list[str] = []
        candidates.extend(self._coerce_path_list(context_filter))
        if isinstance(options, dict):
            for key in ("changed_paths", "paths", "files", "patch_paths"):
                candidates.extend(self._coerce_path_list(options.get(key)))
        return self._dedupe_preserve_order(candidates)

    def _coerce_path_list(self, value: Any) -> list[str]:
        """Return a list of path strings from common input shapes."""
        if value is None:
            return []
        if isinstance(value, (str, Path)):
            text = str(value).strip()
            return [text] if text else []
        if isinstance(value, dict):
            output: list[str] = []
            for key in ("changed_paths", "paths", "files", "patch_paths"):
                output.extend(self._coerce_path_list(value.get(key)))
            return output
        try:
            iterator = iter(value)
        except TypeError:
            text = str(value).strip()
            return [text] if text else []
        output = []
        for item in iterator:
            output.extend(self._coerce_path_list(item))
        return output

    def _dedupe_preserve_order(self, values: Iterable[str]) -> list[str]:
        """Return unique non-empty values in first-seen order."""
        seen: set[str] = set()
        output: list[str] = []
        for value in values:
            text = str(value or "").strip()
            if not text:
                continue
            key = self._slash(text).lower()
            if key in seen:
                continue
            seen.add(key)
            output.append(text)
        return output

    def _normalize_path(self, value: str, project_root: Path) -> str:
        """Return a stable slash-separated path, relative to project_root when possible."""
        raw = str(value or "").strip().strip('"').strip("'")
        if not raw:
            return ""
        path = Path(raw).expanduser()
        try:
            if path.is_absolute():
                relative = path.resolve(strict=False).relative_to(project_root.resolve(strict=False))
                return relative.as_posix()
        except ValueError:
            pass
        return self._slash(raw)

    def _slash(self, value: str) -> str:
        """Normalize path separators and repeated slashes."""
        text = value.replace("\\", "/").strip()
        while "//" in text:
            text = text.replace("//", "/")
        return text.lstrip("./")

    def _build_findings(self, paths: tuple[str, ...]) -> list[EngineFinding]:
        """Build one advisory finding per matched path and category."""
        findings: list[EngineFinding] = []
        seen: set[tuple[str, str]] = set()
        for path in paths:
            lower_path = path.lower()
            for rule in self.rules:
                if not self._matches_rule(lower_path, rule):
                    continue
                key = (path, rule.category)
                if key in seen:
                    continue
                seen.add(key)
                findings.append(
                    EngineFinding(
                        finding_id=self._finding_id(rule.category, len(findings) + 1),
                        severity=rule.severity,
                        category=rule.category,
                        title=rule.title,
                        message="Changed path matches " + rule.category + " risk rules.",
                        file_path=path,
                        line_number=0,
                        evidence="path=" + path,
                        recommendation=rule.recommendation,
                    )
                )
        return self._sort_findings(findings)

    def _matches_rule(self, lower_path: str, rule: RiskRule) -> bool:
        """Return True when a normalized path matches any token for a rule."""
        return any(token.lower() in lower_path for token in rule.tokens)

    def _finding_id(self, category: str, index: int) -> str:
        """Return a stable finding id prefix."""
        clean = "".join(ch if ch.isalnum() else "-" for ch in category.lower()).strip("-")
        return "risk-radar-" + clean + "-" + str(index)

    def _sort_findings(self, findings: list[EngineFinding]) -> list[EngineFinding]:
        """Return findings ordered by severity then path."""
        order = {"critical": 0, "high": 1, "warning": 2, "advisory": 3, "info": 4}
        return sorted(
            findings,
            key=lambda item: (order.get(item.severity, 5), item.file_path, item.category),
        )

    def _summary_text(self, path_count: int, findings: list[EngineFinding]) -> str:
        """Return a compact human summary."""
        if path_count == 0:
            return "Risk Radar received no changed paths to classify."
        if not findings:
            return (
                "Risk Radar reviewed "
                + str(path_count)
                + " changed path(s) and found no configured high-risk path matches."
            )
        high_count = sum(1 for finding in findings if finding.severity in ("high", "critical"))
        return (
            "Risk Radar reviewed "
            + str(path_count)
            + " changed path(s) and produced "
            + str(len(findings))
            + " advisory risk finding(s), including "
            + str(high_count)
            + " high or critical governance risk finding(s)."
        )

    def _next_steps(self, findings: list[EngineFinding]) -> list[str]:
        """Return advisory next steps based on matched findings."""
        if not findings:
            return [
                "Inspect exact source files before editing.",
                "Run the patch-specific validation command before delivery.",
            ]
        steps = [
            "Inspect every high-risk path before editing or patch delivery.",
            "Run the patch-specific validation command and preserve expected markers.",
            "Keep transient artifacts under the selected project's daily-work folder.",
        ]
        categories = {finding.category for finding in findings}
        if "freeze-memory" in categories:
            steps.append("Do not bypass Freeze Feature Preview or Confirm and Write.")
        if "error-memory" in categories:
            steps.append("Use Error Memory intake contracts; do not hand-edit active lessons.")
        if "patch-delivery" in categories:
            steps.append("Validate ZIP contract and avoid isolated ZIP delivery.")
        if "startup-delivery" in categories:
            steps.append("Apply startup-delivery maintenance protocol before changing startup artifacts.")
        return steps
