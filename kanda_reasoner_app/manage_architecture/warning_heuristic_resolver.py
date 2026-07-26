# project-path: kanda_reasoner_app/manage_architecture/warning_heuristic_resolver.py
"""Route Architecture Review warnings to heuristic or Web AI handling lanes."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
import re

__all__ = [
    "ROUTE_HEURISTIC",
    "ROUTE_META",
    "ROUTE_WEB_AI",
    "WarningFinding",
    "WarningResolutionDecision",
    "WarningResolutionReport",
    "format_warning_resolution_report",
    "parse_warning_findings",
    "resolve_warning_audit",
]

ROUTE_HEURISTIC = "heuristic"
ROUTE_WEB_AI = "web_ai"
ROUTE_META = "meta"

_WARNING_LINE_RE = re.compile(
    r"^WARNING\s+([A-Z0-9_]+)\s+(.+?)\s+::\s+(.*)$"
)

_HEURISTIC_WARNING_RULES: dict[str, tuple[str, str]] = {
    "EXPOSES_MISMATCH": (
        "public_surface_alignment_v1",
        "Declared and observed public surface can be compared structurally before any edit.",
    ),
    "HELPER_MANIFEST_CONTRACT": (
        "helper_manifest_contract_v1",
        "Helper exports and manifest declarations can be compared deterministically.",
    ),
    "MISSING_DOCSTRING": (
        "missing_docstring_candidate_v1",
        "Missing module docstrings can be detected and prepared as bounded heuristic candidates.",
    ),
    "MISSING___ALL___FOR_EXPOSES": (
        "explicit_all_from_declared_exports_v1",
        "Declared exports provide a deterministic candidate surface for __all__ review.",
    ),
    "PRIVATE_SYMBOL_EXPORTED": (
        "private_export_candidate_v1",
        "Private-name exports can be identified structurally and prepared for bounded review.",
    ),
    "TEST_PROTECTION_GAP": (
        "test_protection_gap_candidate_v1",
        "Test imports, public contracts, and existing protection links can be analyzed structurally.",
    ),
}

_WEB_AI_DEFAULT_REASON = (
    "No bounded heuristic resolver is registered for this warning code. "
    "Keep the finding in the Web AI lane until exact source context supports a safe rule."
)


@dataclass(frozen=True, slots=True)
class WarningFinding:
    """Represent one parsed Architecture Review warning line."""

    code: str
    path: str
    message: str


@dataclass(frozen=True, slots=True)
class WarningResolutionDecision:
    """Represent one conservative warning routing decision."""

    finding: WarningFinding
    route: str
    resolver_id: str
    reason: str


@dataclass(frozen=True, slots=True)
class WarningResolutionReport:
    """Hold all routing decisions produced from one audit text."""

    decisions: tuple[WarningResolutionDecision, ...]

    @property
    def total_findings(self) -> int:
        """Return the number of parsed warning findings."""
        return len(self.decisions)

    @property
    def heuristic_count(self) -> int:
        """Return the number of heuristic-lane findings."""
        return sum(1 for item in self.decisions if item.route == ROUTE_HEURISTIC)

    @property
    def web_ai_count(self) -> int:
        """Return the number of Web AI-lane findings."""
        return sum(1 for item in self.decisions if item.route == ROUTE_WEB_AI)

    @property
    def meta_count(self) -> int:
        """Return the number of suppression or informational warning notices."""
        return sum(1 for item in self.decisions if item.route == ROUTE_META)

    def decisions_for_route(self, route: str) -> tuple[WarningResolutionDecision, ...]:
        """Return decisions assigned to one route."""
        return tuple(item for item in self.decisions if item.route == route)


def parse_warning_findings(audit_text: str) -> tuple[WarningFinding, ...]:
    """Parse standard Architecture Review WARNING lines from audit text."""
    findings: list[WarningFinding] = []
    for raw_line in str(audit_text).splitlines():
        match = _WARNING_LINE_RE.match(raw_line.strip())
        if match is None:
            continue
        code, path, message = match.groups()
        findings.append(
            WarningFinding(
                code=code.strip(),
                path=path.strip(),
                message=message.strip(),
            )
        )
    return tuple(findings)


def _is_meta_warning(finding: WarningFinding) -> bool:
    """Return True for warning lines that only summarize suppressed findings."""
    message = finding.message.lower()
    return finding.path == "." and "suppressed after" in message


def _route_finding(finding: WarningFinding) -> WarningResolutionDecision:
    """Route one warning through the conservative resolver registry."""
    if _is_meta_warning(finding):
        return WarningResolutionDecision(
            finding=finding,
            route=ROUTE_META,
            resolver_id="suppression_notice_v1",
            reason=(
                "Suppression notices describe hidden finding volume and are not direct source edits."
            ),
        )

    rule = _HEURISTIC_WARNING_RULES.get(finding.code)
    if rule is not None:
        resolver_id, reason = rule
        return WarningResolutionDecision(
            finding=finding,
            route=ROUTE_HEURISTIC,
            resolver_id=resolver_id,
            reason=reason,
        )

    return WarningResolutionDecision(
        finding=finding,
        route=ROUTE_WEB_AI,
        resolver_id="web_ai_contextual_review_v1",
        reason=_WEB_AI_DEFAULT_REASON,
    )


def resolve_warning_audit(audit_text: str) -> WarningResolutionReport:
    """Parse and conservatively route all warning findings in audit text."""
    decisions = tuple(_route_finding(item) for item in parse_warning_findings(audit_text))
    return WarningResolutionReport(decisions=decisions)


def _format_code_counts(decisions: tuple[WarningResolutionDecision, ...]) -> list[str]:
    """Return stable warning-code counts for one route."""
    counts = Counter(item.finding.code for item in decisions)
    return [f"- {code}: {counts[code]}" for code in sorted(counts)]


def _format_route_details(
    title: str,
    decisions: tuple[WarningResolutionDecision, ...],
) -> list[str]:
    """Render one route section without creating parseable WARNING lines."""
    lines = [title]
    if not decisions:
        lines.append("- none")
        return lines

    grouped: dict[tuple[str, str, str], list[WarningResolutionDecision]] = {}
    for item in decisions:
        key = (item.finding.code, item.resolver_id, item.reason)
        grouped.setdefault(key, []).append(item)

    for key in sorted(grouped):
        code, resolver_id, reason = key
        lines.append(f"- {code} | resolver={resolver_id}")
        lines.append(f"  reason: {reason}")
        for item in grouped[key]:
            lines.append(f"  path: {item.finding.path}")
    return lines


def _format_web_ai_handoff(
    decisions: tuple[WarningResolutionDecision, ...],
) -> list[str]:
    """Render a bounded Web AI task containing only difficult warning findings."""
    lines = [
        "WEB AI HANDOFF",
        "Review only the findings listed below.",
        "Use exact project source context before proposing edits.",
        "Do not modify findings assigned to the heuristic queue.",
        "Preserve box ownership, public contracts, and current validation behavior.",
    ]
    if not decisions:
        lines.append("- none")
        return lines

    for item in decisions:
        finding = item.finding
        lines.append(f"- {finding.code} | {finding.path} :: {finding.message}")
    return lines


def format_warning_resolution_report(report: WarningResolutionReport) -> str:
    """Format a complete routing report for the Architecture Review output panel."""
    heuristic = report.decisions_for_route(ROUTE_HEURISTIC)
    web_ai = report.decisions_for_route(ROUTE_WEB_AI)
    meta = report.decisions_for_route(ROUTE_META)

    lines = [
        "WARNING HEURISTIC RESOLVER REPORT",
        "Authority: routing and triage only; no project source files were changed.",
        f"Total warning findings: {report.total_findings}",
        f"Heuristic queue: {report.heuristic_count}",
        f"Web AI queue: {report.web_ai_count}",
        f"Meta/suppression notices: {report.meta_count}",
        "",
        "HEURISTIC WARNING CODES",
    ]
    lines.extend(_format_code_counts(heuristic) or ["- none"])
    lines.append("")
    lines.extend(_format_route_details("HEURISTIC QUEUE", heuristic))
    lines.append("")
    lines.extend(_format_route_details("WEB AI QUEUE", web_ai))
    lines.append("")
    lines.extend(_format_route_details("META / SUPPRESSION NOTICES", meta))
    lines.append("")
    lines.extend(_format_web_ai_handoff(web_ai))
    return "\n".join(lines).rstrip() + "\n"
