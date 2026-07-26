"""Clipboard wrappers for split Show Project bridge-list buttons."""

from __future__ import annotations

from pathlib import Path

from kanda_reasoner_app.reasoner_tools_shell.runner_help import (
    complete_bridge_list_private_impl as _complete_bridge_list,
)

__all__ = [
    "build_startup_bridge_list",
    "build_on_demand_bridge_list",
    "copy_startup_bridge_list_to_clipboard",
    "copy_on_demand_bridge_list_to_clipboard",
]

_STARTUP_BEGIN = "KANDA_STARTUP_BRIDGE_LIST_BEGIN"
_STARTUP_END = "KANDA_STARTUP_BRIDGE_LIST_END"
_ON_DEMAND_BEGIN = "KANDA_ON_DEMAND_BRIDGE_LIST_BEGIN"
_ON_DEMAND_END = "KANDA_ON_DEMAND_BRIDGE_LIST_END"


def build_startup_bridge_list(project_root: str | Path) -> str:
    """Build a wrapper that copies only startup / beginning-of-day bridges."""
    complete = _complete_bridge_list.build_complete_bridge_list(project_root)
    return _build_split_bridge_list(
        complete,
        begin_marker=_STARTUP_BEGIN,
        end_marker=_STARTUP_END,
        section_title="ACTIVE STARTUP BRIDGES",
        next_section_title="ON-DEMAND BRIDGES",
        purpose="startup / beginning-of-day bridge list",
    )


def build_on_demand_bridge_list(project_root: str | Path) -> str:
    """Build a wrapper that copies only on-demand / routed bridges."""
    complete = _complete_bridge_list.build_complete_bridge_list(project_root)
    return _build_split_bridge_list(
        complete,
        begin_marker=_ON_DEMAND_BEGIN,
        end_marker=_ON_DEMAND_END,
        section_title="ON-DEMAND BRIDGES",
        next_section_title="FROZEN BRIDGE MEMORIES",
        purpose="on-demand / routed bridge list",
    )


def copy_startup_bridge_list_to_clipboard(window: object) -> None:
    """Copy startup bridge wrapper text to the clipboard."""
    _copy_bridge_list_to_clipboard(
        window,
        label="Startup",
        builder=build_startup_bridge_list,
        section_title="ACTIVE STARTUP BRIDGES",
    )


def copy_on_demand_bridge_list_to_clipboard(window: object) -> None:
    """Copy on-demand bridge wrapper text to the clipboard."""
    _copy_bridge_list_to_clipboard(
        window,
        label="On Demand",
        builder=build_on_demand_bridge_list,
        section_title="ON-DEMAND BRIDGES",
    )


def _copy_bridge_list_to_clipboard(window: object, *, label: str, builder, section_title: str) -> None:
    try:
        QApplication = _complete_bridge_list._load_qapplication()
        raw_root = str(getattr(window, "project_root_edit").text()).strip()
        if not raw_root:
            raise ValueError("Project root field is empty.")
        text = builder(Path(raw_root).expanduser().resolve(strict=False))
        QApplication.clipboard().setText(text)
        count = _count_section_items(text, section_title)
        message = "Copied " + label + " Bridges: " + str(count) + " items."
        _complete_bridge_list._set_status(window, message)
        _complete_bridge_list._append_log(window, message)
    except Exception as exc:
        message = "[ERROR] Could not copy " + label + " Bridges: " + str(exc)
        _complete_bridge_list._set_status(window, message)
        _complete_bridge_list._append_log(window, message)


def _build_split_bridge_list(
    complete: str,
    *,
    begin_marker: str,
    end_marker: str,
    section_title: str,
    next_section_title: str,
    purpose: str,
) -> str:
    lines = complete.splitlines()
    header = _copy_complete_header(lines)
    section = _extract_section(lines, section_title, next_section_title)
    output = [begin_marker]
    output.append("Purpose: " + purpose + ".")
    output.append("Source: dynamic complete bridge list, filtered for this wrapper button.")
    output.extend(header)
    output.append("")
    output.extend(section)
    output.append("")
    output.append(end_marker)
    return "\n".join(output) + "\n"


def _copy_complete_header(lines: list[str]) -> list[str]:
    keep_prefixes = (
        "Project root:",
        "First prompt files:",
        "Generated UTC:",
    )
    return [line for line in lines if line.startswith(keep_prefixes)]


def _extract_section(lines: list[str], section_title: str, next_section_title: str) -> list[str]:
    try:
        start = lines.index(section_title)
    except ValueError as exc:
        raise ValueError("Missing bridge section: " + section_title) from exc
    try:
        end = lines.index(next_section_title, start + 1)
    except ValueError:
        end = len(lines)
    section = lines[start:end]
    while section and section[-1] == "":
        section.pop()
    return section


def _count_section_items(text: str, section_title: str) -> int:
    lines = text.splitlines()
    try:
        start = lines.index(section_title) + 1
    except ValueError:
        return 0
    count = 0
    for line in lines[start:]:
        if not line:
            continue
        if line.startswith("KANDA_") or line.isupper():
            break
        if line.startswith("-"):
            count += 1
    return count
