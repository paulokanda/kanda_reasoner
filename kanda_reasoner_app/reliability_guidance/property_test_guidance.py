# project-path: kanda_reasoner_app/reliability_guidance/property_test_guidance.py
"""Build reviewable property-test guidance without editing source files."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

__all__ = [
    "PropertyTestDraft",
    "default_property_test_output_dir",
    "render_property_test_draft_markdown",
]


@dataclass(frozen=True)
class PropertyTestDraft:
    """Reviewable draft describing possible property-based tests."""

    module_path: str
    function_name: str
    properties: tuple[str, ...] = field(default_factory=tuple)
    input_strategies: tuple[str, ...] = field(default_factory=tuple)
    invariants: tuple[str, ...] = field(default_factory=tuple)
    edge_cases: tuple[str, ...] = field(default_factory=tuple)
    tests_to_add: tuple[str, ...] = field(default_factory=tuple)
    limitations: tuple[str, ...] = field(default_factory=tuple)

    def normalized_properties(self) -> tuple[str, ...]:
        """Return explicit properties or conservative default properties."""
        if self.properties:
            return self.properties
        defaults = [
            "Function handles representative valid inputs without raising.",
            "Function rejects or reports invalid inputs predictably.",
        ]
        if self.invariants:
            defaults.extend(self.invariants)
        return tuple(defaults)

    def normalized_tests_to_add(self) -> tuple[str, ...]:
        """Return explicit test ideas or conservative draft-only defaults."""
        if self.tests_to_add:
            return self.tests_to_add
        return (
            "Create a focused property test draft in workbench before promotion.",
            "Review generated strategies before adding test dependencies.",
        )


def default_property_test_output_dir(project_root: Path) -> Path:
    """Return the default folder for property-test guidance drafts."""
    return Path(project_root) / "workbench" / "drafts" / "property_tests"


def render_property_test_draft_markdown(draft: PropertyTestDraft) -> str:
    """Render property-test guidance as Markdown."""
    lines = [
        "# Property Test Draft",
        "",
        f"Module: {draft.module_path}",
        f"Function: {draft.function_name}",
        "",
        "## Properties",
    ]
    lines.extend(f"- {item}" for item in draft.normalized_properties())

    lines.extend(["", "## Input Strategies"])
    if draft.input_strategies:
        lines.extend(f"- {item}" for item in draft.input_strategies)
    else:
        lines.append("- Draft strategies manually before adding new dependencies.")

    lines.extend(["", "## Invariants"])
    if draft.invariants:
        lines.extend(f"- {item}" for item in draft.invariants)
    else:
        lines.append("- No invariants provided.")

    lines.extend(["", "## Edge Cases"])
    if draft.edge_cases:
        lines.extend(f"- {item}" for item in draft.edge_cases)
    else:
        lines.append("- Include empty, boundary, malformed, and repeated inputs when relevant.")

    lines.extend(["", "## Tests To Add"])
    lines.extend(f"- {item}" for item in draft.normalized_tests_to_add())

    lines.extend(["", "## Limitations"])
    if draft.limitations:
        lines.extend(f"- {item}" for item in draft.limitations)
    else:
        lines.append("- Draft only. Do not add production tests without review.")

    return "\n".join(lines) + "\n"
