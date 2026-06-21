"""Engineering Safety panel for the Reasoner tools GUI.

This module owns the Engineering Safety panel factory only. It is intentionally
import-safe: PySide6 is imported only inside create_engineering_safety_panel.
The backend logic is reached through the canonical kanda_reasoner_app
safety_suite_cli facade during the staged package migration.
"""
from __future__ import annotations
import _reasoner_tools_gui_engineering_safety_panel_commands as _panel_commands

from contextlib import redirect_stderr, redirect_stdout
from dataclasses import dataclass
from io import StringIO
from pathlib import Path
import sys
import traceback
from typing import Iterable

from kanda_reasoner_app.project_root_resolver import resolve_active_project_root

DEFAULT_PROJECT_ROOT = str(resolve_active_project_root())
@dataclass(frozen=True)
class EngineeringSafetyPanelTool:
    """Description for one Engineering Safety panel action."""
    section: str
    label: str
    command_name: str
    description: str
    @property
    def command(self) -> str:
        """Backward-compatible alias for older tests or UI code."""
        return self.command_name
ENGINEERING_SAFETY_PANEL_CATALOG: tuple[EngineeringSafetyPanelTool, ...] = (
    EngineeringSafetyPanelTool(
        section="Source Hygiene",
        label="Scan BOM",
        command_name="bom-scan",
        description="Dry-run scan for UTF-8 BOM and decoding issues.",
    ),
    EngineeringSafetyPanelTool(
        section="Source Hygiene",
        label="Shadow Audit",
        command_name="shadow-audit",
        description="Read-only audit for public-symbol and facade conflicts.",
    ),
    EngineeringSafetyPanelTool(
        section="Source Hygiene",
        label="Plan Shadow Fix",
        command_name="shadow-plan",
        description="Build a read-only correction plan for shadow findings.",
    ),
    EngineeringSafetyPanelTool(
        section="Source Hygiene",
        label="Facade Fix Plan",
        command_name="facade-fix-plan",
        description="Plan safe mechanical facade cleanup without applying edits.",
    ),
    EngineeringSafetyPanelTool(
        section="Engineering Safety",
        label="Risk Change Radar",
        command_name="risk-radar",
        description="Estimate what can break before a patch.",
    ),
    EngineeringSafetyPanelTool(
        section="Engineering Safety",
        label="Crash Triage",
        command_name="crash-triage",
        description="Summarize a crash or traceback and first files to inspect.",
    ),
    EngineeringSafetyPanelTool(
        section="Engineering Safety",
        label="Refactor Playbook",
        command_name="refactor-playbook",
        description="Create a staged refactor plan with validation steps.",
    ),
    EngineeringSafetyPanelTool(
        section="Governance Automation",
        label="Release Notes",
        command_name="release-notes",
        description="Draft release notes from explicit bundle evidence.",
    ),
    EngineeringSafetyPanelTool(
        section="Governance Automation",
        label="Push Plan",
        command_name="push-plan",
        description="Show the default validation plan for every push.",
    ),
    EngineeringSafetyPanelTool(
        section="Stack Compatibility",
        label="Stack Brief",
        command_name="stack-brief",
        description="Draft dependency and runtime compatibility notes.",
    ),
    EngineeringSafetyPanelTool(
        section="Draft Reliability",
        label="API Contract",
        command_name="api-contract",
        description="Draft input/output guard recommendations.",
    ),
    EngineeringSafetyPanelTool(
        section="Draft Reliability",
        label="Property Test",
        command_name="property-test",
        description="Draft property-test guidance for a function.",
    ),
    # BEGIN PA021_PROJECT_SYMBOL_ATLAS_GUI_TOOLS
    EngineeringSafetyPanelTool(
        section="Project Symbol Atlas",
        label="Atlas Report",
        command_name="atlas-report",
        description="Build Project Symbol Atlas reports for the current project.",
    ),
    EngineeringSafetyPanelTool(
        section="Project Symbol Atlas",
        label="Evidence Freshness",
        command_name="evidence-freshness",
        description="Check whether Project Analysis Evidence still matches live source.",
    ),
    EngineeringSafetyPanelTool(
        section="Project Symbol Atlas",
        label="Find Symbol",
        command_name="find-symbol",
        description="Find an existing symbol before creating new code.",
    ),
    EngineeringSafetyPanelTool(
        section="Project Symbol Atlas",
        label="Find Owner",
        command_name="find-owner",
        description="Find the likely owner file for a symbol.",
    ),
    EngineeringSafetyPanelTool(
        section="Project Symbol Atlas",
        label="Facade Owner",
        command_name="facade-owner",
        description="Resolve whether a target file is a facade and identify the owner.",
    ),
    EngineeringSafetyPanelTool(
        section="Project Symbol Atlas",
        label="Main and Helpers",
        command_name="main-helpers",
        description="Map main file, helper files, and public API owner.",
    ),
    EngineeringSafetyPanelTool(
        section="Project Symbol Atlas",
        label="Related Files",
        command_name="related-files",
        description="Find tests, helpers, manifests, diagnostics, and related support files.",
    ),
    EngineeringSafetyPanelTool(
        section="Project Symbol Atlas",
        label="Pre-Patch Gate",
        command_name="pre-patch-gate",
        description="Run ownership checks before editing source files.",
    ),
    # END PA021_PROJECT_SYMBOL_ATLAS_GUI_TOOLS
    EngineeringSafetyPanelTool(
        section="Utilities",
        label="List Tools",
        command_name="list-tools",
        description="List available Safety Suite CLI commands.",
    ),
)
def get_engineering_safety_panel_catalog() -> tuple[EngineeringSafetyPanelTool, ...]:
    """Return the immutable panel action catalog."""
    return ENGINEERING_SAFETY_PANEL_CATALOG
def _project_root_text(project_root: str | None = None) -> str:
    """Return a non-empty project root text for default GUI commands."""
    if project_root is not None:
        return str(project_root)
    return str(resolve_active_project_root())
def _call_safety_suite_cli(args: list[str]) -> tuple[int, str, str]:
    """Call the Safety Suite CLI in-process and capture text output."""
    stdout_buffer = StringIO()
    stderr_buffer = StringIO()
    status = 0
    try:
        from kanda_reasoner_app.safety_suite_cli import commands
        cli_main = getattr(commands, "main", None)
        if cli_main is None:
            raise RuntimeError("safety_suite_cli.commands.main is not available")
        with redirect_stdout(stdout_buffer), redirect_stderr(stderr_buffer):
            result = cli_main(args)
        if isinstance(result, int):
            status = result
        elif result is None:
            status = 0
        else:
            try:
                status = int(result)
            except (TypeError, ValueError):
                status = 0
    except SystemExit as exc:
        code = exc.code
        if isinstance(code, int):
            status = code
        elif code is None:
            status = 0
        else:
            status = 1
            stderr_buffer.write(str(code))
    except Exception:
        status = 1
        stderr_buffer.write(traceback.format_exc())
    return status, stdout_buffer.getvalue(), stderr_buffer.getvalue()
def run_engineering_safety_panel_cli_command(
    command_name: str,
    project_root: str | None = None,
) -> str:
    """Run a panel command and return the formatted display text."""
    args = build_engineering_safety_panel_cli_args(command_name, project_root)
    status, stdout_text, stderr_text = _call_safety_suite_cli(args)
    lines = [
        f"Command: {command_name}",
        f"Status: {status}",
        f"Arguments: {' '.join(args)}",
        "",
        "STDOUT:",
        stdout_text.strip() or "(no stdout)",
    ]
    if stderr_text.strip():
        lines.extend(["", "STDERR:", stderr_text.strip()])
    return "\n".join(lines)
def _group_tools_by_section(
    tools: Iterable[EngineeringSafetyPanelTool],
) -> dict[str, list[EngineeringSafetyPanelTool]]:
    """Group tools while preserving their original order."""
    grouped: dict[str, list[EngineeringSafetyPanelTool]] = {}
    for tool in tools:
        grouped.setdefault(tool.section, []).append(tool)
    return grouped
def create_engineering_safety_panel():
    """Create the Engineering Safety tab panel.

    PySide6 is imported lazily so importing this module remains safe in tests and
    non-GUI workflows.
    """
    from PySide6.QtCore import QTimer  # type: ignore[import-not-found]
    from PySide6.QtWidgets import (  # type: ignore[import-not-found]

        QGroupBox,
        QHBoxLayout,
        QLabel,
        QPushButton,
        QScrollArea,
        QTextEdit,
        QVBoxLayout,
        QWidget,
    )

    root = str(resolve_active_project_root())
    panel = QWidget()
    outer = QVBoxLayout(panel)

    heading = QLabel("Engineering Safety")
    outer.addWidget(heading)

    status_label = QLabel("Ready.")
    outer.addWidget(status_label)

    output_box = QTextEdit()
    output_box.setReadOnly(True)
    output_box.setPlainText("Click a tool button to run a safe default smoke command.")

    scroll = QScrollArea()
    scroll.setWidgetResizable(True)
    button_host = QWidget()
    button_layout = QVBoxLayout(button_host)

    # BEGIN PA021B2_ENGINEERING_SAFETY_PYSIDE6_ASYNC_RUNNER
    from concurrent.futures import ThreadPoolExecutor

    command_executor = ThreadPoolExecutor(max_workers=1)
    running_commands: set[str] = set()

    def set_tool_buttons_enabled(enabled: bool) -> None:
        """Enable or disable all tool buttons while a command is running."""
        for button in button_host.findChildren(QPushButton):
            button.setEnabled(enabled)

    def finish_command(command_name: str, future: object) -> None:
        """Collect a completed command result on the GUI thread."""
        try:
            output = future.result()  # type: ignore[attr-defined]
            output_box.setPlainText(str(output))
            status_label.setText(f"Finished: {command_name}")
        except Exception as exc:  # noqa: BLE001
            error_text = traceback.format_exc()
            output_box.setPlainText(error_text)
            status_label.setText(f"Failed: {command_name}: {exc}")
        finally:
            running_commands.discard(command_name)
            set_tool_buttons_enabled(True)

    def poll_command(command_name: str, future: object) -> None:
        """Poll a worker future without blocking the PySide6/Qt event loop."""
        if future.done():  # type: ignore[attr-defined]
            finish_command(command_name, future)
            return
        QTimer.singleShot(150, lambda: poll_command(command_name, future))

    def run_command(command_name: str) -> None:
        """Start a panel command without blocking the GUI event loop."""
        if running_commands:
            active = sorted(running_commands)[0]
            status_label.setText(f"Still running: {active}")
            return
        running_commands.add(command_name)
        set_tool_buttons_enabled(False)
        status_label.setText(f"Running: {command_name}")
        output_box.setPlainText(
            "Running command without blocking the GUI.\n"
            f"Command: {command_name}\n"
            "Output will appear here when the command finishes."
        )
        future = command_executor.submit(
            run_engineering_safety_panel_cli_command,
            command_name,
            root,
        )
        QTimer.singleShot(150, lambda: poll_command(command_name, future))
    # END PA021B2_ENGINEERING_SAFETY_PYSIDE6_ASYNC_RUNNER

    for section, tools in _group_tools_by_section(get_engineering_safety_panel_catalog()).items():
        group = QGroupBox(section)
        group_layout = QVBoxLayout(group)
        row = QHBoxLayout()
        for index, tool in enumerate(tools, start=1):
            button = QPushButton(tool.label)
            button.setToolTip(tool.description)
            button.clicked.connect(lambda checked=False, name=tool.command_name: run_command(name))
            row.addWidget(button)
            if index % 3 == 0:
                group_layout.addLayout(row)
                row = QHBoxLayout()
        group_layout.addLayout(row)
        button_layout.addWidget(group)

    button_layout.addStretch(1)
    scroll.setWidget(button_host)
    outer.addWidget(scroll)
    outer.addWidget(output_box)
    return panel



# GUI004W_PUBLIC_EXPORT_WRAPPERS_START
EngineeringSafetyPanelCommandResult = _panel_commands._PanelCommandResult


def build_engineering_safety_panel_command(command_name: str):
    "Return the Engineering Safety panel command object."
    if hasattr(_panel_commands, "_build_panel_command"):
        return _panel_commands._build_panel_command(command_name)
    return _panel_commands._build_display_command(command_name)


def build_engineering_safety_panel_cli_args(command_name: str, project_root=None):
    "Return runnable CLI arguments for a panel command."
    return _panel_commands._build_cli_args(command_name, project_root)


def run_engineering_safety_panel_command(command_name: str, project_root=None):
    "Run a panel command and return an explicit command result."
    return _panel_commands._run_command(command_name, project_root)
# GUI004W_PUBLIC_EXPORT_WRAPPERS_END

__all__ = [
    "ENGINEERING_SAFETY_PANEL_CATALOG",
    "EngineeringSafetyPanelTool",
    "build_engineering_safety_panel_cli_args",
    "build_engineering_safety_panel_command",
    "create_engineering_safety_panel",
    "get_engineering_safety_panel_catalog",
    "run_engineering_safety_panel_cli_command",
]

# BEGIN GUI004L_ENGINEERING_SAFETY_PANEL_COMMAND_DELEGATION
# END GUI004L_ENGINEERING_SAFETY_PANEL_COMMAND_DELEGATION
