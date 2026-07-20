# project-path: reasoner_tools_gui_engineering_safety_panel.py
"""Engineering Safety panel for the Reasoner tools GUI.

This module owns the Engineering Safety panel factory only. It is intentionally
import-safe: PySide6 is imported only inside create_engineering_safety_panel.
The backend logic is reached through the canonical kanda_reasoner_app
safety_suite_cli facade during the staged package migration.
"""

from __future__ import annotations
import _reasoner_tools_gui_engineering_safety_panel_commands as _panel_commands
from _reasoner_tools_gui_engineering_safety_panel_catalog import (
    _build_engineering_safety_panel_catalog,
)
from _reasoner_tools_gui_engineering_safety_full_audit import (
    _install_complete_engineering_review,
)

from contextlib import redirect_stderr, redirect_stdout
from dataclasses import dataclass
from io import StringIO
import traceback
from typing import Callable, Iterable

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
    _build_engineering_safety_panel_catalog(EngineeringSafetyPanelTool)
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


def create_engineering_safety_panel(
    project_root_provider: Callable[[], object] | None = None,
):
    """Create the Engineering Safety tab panel.

    PySide6 is imported lazily so importing this module remains safe in tests and
    non-GUI workflows.
    """
    from PySide6.QtCore import QTimer  # type: ignore[import-not-found]
    from PySide6.QtWidgets import (  # type: ignore[import-not-found]
        QGridLayout,
        QGroupBox,
        QLabel,
        QPushButton,
        QScrollArea,
        QSizePolicy,
        QTabWidget,
        QTextEdit,
        QVBoxLayout,
        QWidget,
    )

    panel = QWidget()
    outer = QVBoxLayout(panel)
    outer.setContentsMargins(0, 0, 0, 0)
    outer.setSpacing(8)

    audit_tabs = QTabWidget(panel)
    audit_tabs.setObjectName("engineering_safety_audit_tabs")
    pontual_audit_page = QWidget(audit_tabs)
    pontual_audit_page.setObjectName("engineering_safety_pontual_audit_page")
    pontual_audit_layout = QVBoxLayout(pontual_audit_page)
    pontual_audit_layout.setContentsMargins(0, 0, 0, 0)
    pontual_audit_layout.setSpacing(8)
    audit_tabs.addTab(pontual_audit_page, "Pontual Audit")
    outer.addWidget(audit_tabs, 1)

    panel.engineering_safety_audit_tabs = audit_tabs
    panel.engineering_safety_pontual_audit_page = pontual_audit_page
    panel.engineering_safety_project_root_provider = project_root_provider

    status_label = QLabel("")
    status_label.setVisible(False)

    output_box = QTextEdit()
    output_box.setReadOnly(True)
    output_box.setPlainText("Click a tool button to run a safe default smoke command.")

    scroll = QScrollArea()
    scroll.setWidgetResizable(True)
    button_host = QWidget()
    button_layout = QGridLayout(button_host)
    button_layout.setContentsMargins(0, 0, 0, 0)
    button_layout.setHorizontalSpacing(12)
    button_layout.setVerticalSpacing(10)
    button_layout.setColumnStretch(0, 1)
    button_layout.setColumnStretch(1, 1)

    def current_project_root_text() -> str:
        """Return the project root selected by the shared Audit Project header."""
        if project_root_provider is not None:
            try:
                selected = str(project_root_provider() or "").strip()
            except Exception:  # noqa: BLE001
                selected = ""
            if selected:
                return selected
        return str(resolve_active_project_root())

    # BEGIN PA021B2_ENGINEERING_SAFETY_PYSIDE6_ASYNC_RUNNER
    from concurrent.futures import ThreadPoolExecutor

    command_executor = ThreadPoolExecutor(max_workers=1)
    running_commands: set[str] = set()

    def set_tool_buttons_enabled(enabled: bool) -> None:
        """Enable or disable all tool buttons while a command is running."""
        for button in panel.findChildren(QPushButton):
            button.setEnabled(enabled)

    _install_complete_engineering_review(
        panel,
        audit_tabs,
        command_executor,
        running_commands,
        set_tool_buttons_enabled,
        current_project_root_text,
        get_engineering_safety_panel_catalog,
        run_engineering_safety_panel_command,
        status_label,
    )

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

    correction_dialog_state: dict[str, object | None] = {"dialog": None}

    def open_ruff_correction_dialog() -> None:
        """Open the reviewed Ruff correction dialog for the active project."""
        existing = correction_dialog_state.get("dialog")
        if existing is not None and existing.isVisible():  # type: ignore[attr-defined]
            existing.raise_()  # type: ignore[attr-defined]
            existing.activateWindow()  # type: ignore[attr-defined]
            return
        from _reasoner_tools_gui_ruff_correction_dialog import (
            create_ruff_correction_dialog,
        )

        dialog = create_ruff_correction_dialog(
            panel,
            current_project_root_text(),
        )
        correction_dialog_state["dialog"] = dialog
        dialog.finished.connect(
            lambda _result: correction_dialog_state.__setitem__("dialog", None)
        )
        dialog.show()

    def run_command(command_name: str) -> None:
        """Start a panel command without blocking the GUI event loop."""
        if command_name == "ruff-correction-dialog":
            open_ruff_correction_dialog()
            return
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
            current_project_root_text(),
        )
        QTimer.singleShot(150, lambda: poll_command(command_name, future))

    # END PA021B2_ENGINEERING_SAFETY_PYSIDE6_ASYNC_RUNNER

    def run_ai_review_first_check() -> None:
        """Run the first Engineering Safety check exposed in the tab header."""
        run_command("pre-patch-gate")

    panel.run_ai_review_first_check = run_ai_review_first_check

    button_width = 170
    grouped_sections = _group_tools_by_section(get_engineering_safety_panel_catalog())

    def build_group(section: str, tools: list[EngineeringSafetyPanelTool]) -> QGroupBox:
        """Build one symmetric two-column tool group."""
        group = QGroupBox(section)
        group_layout = QGridLayout(group)
        group_layout.setContentsMargins(8, 8, 8, 8)
        group_layout.setHorizontalSpacing(8)
        group_layout.setVerticalSpacing(6)
        group_layout.setColumnStretch(0, 1)
        group_layout.setColumnStretch(1, 1)

        for index, tool in enumerate(tools):
            button = QPushButton(tool.label)
            button.setToolTip(tool.description)
            button.setMinimumWidth(button_width)
            button.setMaximumWidth(button_width)
            button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            button.clicked.connect(
                lambda checked=False, name=tool.command_name: run_command(name)
            )
            group_layout.addWidget(button, index // 2, index % 2)

        return group

    def build_stack(sections_to_stack: tuple[str, ...]) -> QWidget:
        """Build a compact vertical stack used to balance the two columns."""
        host = QWidget()
        stack = QVBoxLayout(host)
        stack.setContentsMargins(0, 0, 0, 0)
        stack.setSpacing(10)
        for section_name in sections_to_stack:
            stack.addWidget(build_group(section_name, grouped_sections[section_name]))
        stack.addStretch(1)
        return host

    button_layout.addWidget(
        build_group("Source Hygiene", grouped_sections["Source Hygiene"]),
        0,
        0,
    )
    button_layout.addWidget(
        build_group("Engineering Safety", grouped_sections["Engineering Safety"]),
        0,
        1,
    )
    button_layout.addWidget(
        build_group(
            "Governance Automation",
            grouped_sections["Governance Automation"],
        ),
        1,
        0,
    )
    button_layout.addWidget(
        build_group(
            "Stack Compatibility",
            grouped_sections["Stack Compatibility"],
        ),
        1,
        1,
    )
    button_layout.addWidget(build_stack(("Draft Reliability", "Utilities")), 2, 0)
    button_layout.addWidget(
        build_group(
            "Project Symbol Atlas",
            grouped_sections["Project Symbol Atlas"],
        ),
        2,
        1,
    )

    button_layout.setRowStretch(3, 1)
    scroll.setWidget(button_host)
    pontual_audit_layout.addWidget(scroll, 1)
    pontual_audit_layout.addWidget(output_box)
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
