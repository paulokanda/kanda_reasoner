# project-path: kanda_reasoner_app/reliability_guidance/api_contract_guidance.py
"""Build reviewable API contract guard guidance without editing source files."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

__all__ = [
    "ApiContractGuardDraft",
    "default_api_contract_output_dir",
    "render_api_contract_guard_draft_markdown",
]


@dataclass(frozen=True)
class ApiContractGuardDraft:
    """Reviewable draft describing possible API contract guards."""

    module_path: str
    function_name: str
    parameters: tuple[str, ...] = field(default_factory=tuple)
    return_hint: str = ""
    known_failure_modes: tuple[str, ...] = field(default_factory=tuple)
    guard_suggestions: tuple[str, ...] = field(default_factory=tuple)
    tests_to_add: tuple[str, ...] = field(default_factory=tuple)
    limitations: tuple[str, ...] = field(default_factory=tuple)

    def normalized_suggestions(self) -> tuple[str, ...]:
        """Return explicit suggestions or conservative parameter checks."""
        if self.guard_suggestions:
            return self.guard_suggestions
        suggestions: list[str] = []
        for name in self.parameters:
            clean_name = name.strip()
            if clean_name:
                suggestions.append(f"Validate parameter '{clean_name}' before use.")
        if self.return_hint:
            suggestions.append(f"Document and test return contract: {self.return_hint}.")
        if not suggestions:
            suggestions.append("Review the function signature before adding guards.")
        return tuple(suggestions)


def default_api_contract_output_dir(project_root: Path) -> Path:
    """Return the default folder for API contract guidance drafts."""
    return Path(project_root) / "workbench" / "drafts" / "api_contracts"


def render_api_contract_guard_draft_markdown(draft: ApiContractGuardDraft) -> str:
    """Render API contract guard guidance as Markdown."""
    lines = [
        "# API Contract Guard Draft",
        "",
        f"Module: {draft.module_path}",
        f"Function: {draft.function_name}",
        "",
        "## Parameters",
    ]
    if draft.parameters:
        lines.extend(f"- {name}" for name in draft.parameters)
    else:
        lines.append("- No parameters provided.")

    lines.extend(["", "## Suggested Guards"])
    lines.extend(f"- {item}" for item in draft.normalized_suggestions())

    lines.extend(["", "## Known Failure Modes"])
    if draft.known_failure_modes:
        lines.extend(f"- {item}" for item in draft.known_failure_modes)
    else:
        lines.append("- None provided.")

    lines.extend(["", "## Tests To Add"])
    if draft.tests_to_add:
        lines.extend(f"- {item}" for item in draft.tests_to_add)
    else:
        lines.append("- Add focused tests before promoting guards into source.")

    lines.extend(["", "## Limitations"])
    if draft.limitations:
        lines.extend(f"- {item}" for item in draft.limitations)
    else:
        lines.append("- Draft only. Do not modify production source without review.")

    return "\n".join(lines) + "\n"
