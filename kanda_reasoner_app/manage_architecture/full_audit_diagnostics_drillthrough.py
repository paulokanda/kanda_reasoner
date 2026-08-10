# project-path: kanda_reasoner_app/manage_architecture/full_audit_diagnostics_drillthrough.py
"""Public sibling-Box bridge from Full Audit to Engineering Diagnostics."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
import re

__all__ = [
    "FullAuditDiagnosticLink",
    "build_full_audit_diagnostic_links",
    "install_full_audit_diagnostics_drillthrough",
]

_SEPARATOR = "-" * 72
_COMMAND_TO_PRODUCER = {
    "bom-scan": "source_hygiene.bom_scan",
    "ruff-quality": "ruff.check",
    "shadow-audit": "source_hygiene.shadow_conflict_audit",
}
_HEADER = re.compile(r"^\[\d{2}/\d{2}\]\s+(.+?)\s+-\s+(.+)$")


@dataclass(frozen=True, slots=True)
class FullAuditDiagnosticLink:
    """One Full Audit row that has an exact Engineering Diagnostics producer."""

    section: str
    label: str
    command_name: str
    execution: str
    assessment: str
    assessment_reason: str
    producer_id: str


def build_full_audit_diagnostic_links(report_text: str) -> tuple[FullAuditDiagnosticLink, ...]:
    """Parse recognized Full Audit blocks without changing assessment semantics."""
    links: list[FullAuditDiagnosticLink] = []
    for raw_block in str(report_text or "").split(_SEPARATOR):
        lines = [line.strip() for line in raw_block.splitlines() if line.strip()]
        if not lines:
            continue
        header_index = next(
            (index for index, line in enumerate(lines) if _HEADER.match(line)),
            -1,
        )
        if header_index < 0:
            continue
        match = _HEADER.match(lines[header_index])
        if match is None:
            continue
        fields: dict[str, str] = {}
        for line in lines[header_index + 1 :]:
            name, separator, value = line.partition(":")
            if separator and name in {
                "Command",
                "Execution",
                "Assessment",
                "Assessment reason",
            }:
                fields[name] = value.strip()
        command_name = fields.get("Command", "")
        producer_id = _COMMAND_TO_PRODUCER.get(command_name, "")
        if not producer_id:
            continue
        links.append(
            FullAuditDiagnosticLink(
                section=match.group(1).strip(),
                label=match.group(2).strip(),
                command_name=command_name,
                execution=fields.get("Execution", ""),
                assessment=fields.get("Assessment", ""),
                assessment_reason=fields.get("Assessment reason", ""),
                producer_id=producer_id,
            )
        )
    return tuple(links)


def install_full_audit_diagnostics_drillthrough(
    safety_panel: object,
    diagnostics_panel: object,
    *,
    project_root_provider: Callable[[], str],
    select_diagnostics_tab: Callable[[], None],
) -> object:
    """Delegate Qt binding through the public Engineering Diagnostics GUI facade."""
    from kanda_reasoner_app.engineering_diagnostics_gui import (
        install_full_audit_diagnostics_drillthrough_ui,
    )

    return install_full_audit_diagnostics_drillthrough_ui(
        safety_panel,
        diagnostics_panel,
        project_root_provider=project_root_provider,
        select_diagnostics_tab=select_diagnostics_tab,
        diagnostic_links_provider=build_full_audit_diagnostic_links,
    )
