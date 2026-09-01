"""Small builders for 00_START_HERE_FOR_AI.md lists."""

from __future__ import annotations

from startup_kernel.constants import (
    MANIFEST_FILENAME,
    README_FILENAME,
    STABLE_BOOT_FILENAME,
)


__all__ = [
    "build_numbered_startup_file_list",
    "build_required_report_list",
    "build_active_bridge_report",
]


def build_numbered_startup_file_list(expected: list[str]) -> str:
    """Return numbered startup file lines excluding the stable boot file."""
    return "\n".join(
        f"{index}. {name}"
        for index, name in enumerate(expected, start=1)
    )


def build_required_report_list(expected: list[str]) -> str:
    """Return the required startup-pack file report lines."""
    required_report_lines = [
        f"0. {STABLE_BOOT_FILENAME} - loaded/missing - one-line role"
    ]
    required_report_lines.extend(
        f"{index}. {name} - loaded/missing - one-line role"
        for index, name in enumerate(expected, start=1)
    )
    required_report_lines.append(
        f"{len(expected) + 1}. {README_FILENAME} - loaded/missing - "
        "one-line role"
    )
    required_report_lines.append(
        f"{len(expected) + 2}. {MANIFEST_FILENAME} - loaded/missing - "
        "one-line role"
    )
    return "\n".join(required_report_lines)


def build_active_bridge_report() -> str:
    """Return short beginning-of-day bridge visibility lines."""
    return (
        "1. Codex Project Governance Bridge - loaded/missing - "
        "in Codex, first_prompt_files and second_prompt_files are the first "
        "KANDA project-governance context after higher-priority "
        "Codex/system/developer rules; do not skip, weaken, reorder, or "
        "bypass their gates; use KANDA Reasoner bridge logic to select exact "
        "prompt IDs, prompt paths, folder cards, and specialist owners when "
        "deeper context is needed\n"
        "2. Code Module Size Bridge - loaded/missing - "
        "hard gate: ideal <=400 code lines; maximum <=500 physical lines; "
        "PEP 8, SOLID, and DRY are canonical; never compress formatting or "
        "duplicate logic to fit; create cohesive helpers when needed; "
        "every new or touched code/source module must be <=500 lines after "
        "PEP 8 formatting and create, update, modify, refactor, or split work; "
        "route above-limit code work to large_module_refactor_protocol on "
        "demand\n"
        "3. Box Logic Startup Bridge - loaded/missing - "
        "hard gate: identify active box, owner paths, allowed files, "
        "out-of-scope files, cross-box touches, public contracts, validation "
        "scope, and boundary risks before project work; route boundary-risk "
        "work to box_architecture_canon on demand\n"
        "4. No-Leak Logic Bridge - loaded/missing - "
        "hard gate: NO_LEAK_LOGIC_V1 prevents wrong-root writes, tool/project "
        "leakage, cross-box leakage, private reach-in, hidden mutable state, "
        "generated-artifact-as-source leakage, and evidence leakage\n"
        "5. Class 04 Architecture Owner Dispatch - loaded/missing - "
        "Brick Wall remains final coding authority; do not load the retired "
        "compiled companion; route only the smallest current Box Architecture, "
        "Boundary-First, Shielding, Folder Placement, or Stateful Control owner "
        "set\n"
        "6. Durable Documentation Artifact Routing Bridge - loaded/missing - "
        "daily-work is transient; durable project documents and successful "
        "validation evidence belong under the selected project sibling "
        "_show_project_to_AI support root\n"
        "7. Terminal Cleanup Bridge - loaded/missing - "
        "install success and all other interactive terminal flows use Enter, "
        "Enter, then one final Clear-Host; automatic timed clearing is retired; "
        "keep terminal open; freeze-prep "
        "evidence merge must use a temp .py helper, not python -c\n"
        "8. Runtime Evidence Escalation Bridge - loaded/missing - "
        "request the smallest scenario-specific trace, focused test, logs, or "
        "terminal evidence package when actual execution behavior matters; "
        "prefer current evidence, do not over-request for source-sufficient "
        "questions, and keep static-only conclusions labeled as inference"
    )
