# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/docstring_formatting.py
"""Text formatting for deterministic docstring proposal contracts."""
from __future__ import annotations

from .models import DocstringProposal

__all__ = ["format_docstring_proposals"]


def format_docstring_proposals(proposals: list[DocstringProposal]) -> str:
    """Return a readable docstring proposal summary for the GUI."""
    lines = [
        "Docstring proposal contract generated.",
        f"Proposal count: {len(proposals)}",
        "",
        "Important:",
        "- This train does not insert docstrings.",
        "- Existing docstrings are not overwritten.",
        "- Low-confidence proposals require review before preview writing.",
        "- No preview files or project patch payload files are generated.",
        "",
        "Proposals:",
    ]
    if not proposals:
        lines.append("- none")
        return "\n".join(lines)
    for proposal in proposals:
        lines.extend(_proposal_lines(proposal))
    return "\n".join(lines)


def _proposal_lines(proposal: DocstringProposal) -> list[str]:
    """Return compact lines for one proposal."""
    risks = ", ".join(proposal.risk_flags) or "<none>"
    return [
        f"- {proposal.target_kind}: {proposal.target_name}",
        f"  Provenance: {proposal.provenance}",
        f"  Confidence: {proposal.confidence}",
        f"  Status: {proposal.status}",
        f"  Reason: {proposal.reason}",
        f"  Risks: {risks}",
        "  Proposed docstring:",
        _indent(proposal.proposed_docstring),
    ]


def _indent(text: str) -> str:
    """Indent proposal text for the plain text panel."""
    return "\n".join("    " + line for line in text.splitlines())
