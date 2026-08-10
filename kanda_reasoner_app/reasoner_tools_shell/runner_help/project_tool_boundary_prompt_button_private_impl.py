# project-path: kanda_reasoner_app/reasoner_tools_shell/runner_help/project_tool_boundary_prompt_button_private_impl.py
"""Show Project clipboard controls for canonical governance prompts."""

from __future__ import annotations

from pathlib import Path
from typing import Any

__all__ = [
    "build_project_tool_boundary_wrapper",
    "copy_project_tool_boundary_to_clipboard",
    "install_control",
]

_PROMPT_ROOT = Path(
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS"
)
_PROMPT_REL = _PROMPT_ROOT / Path(
    "12_generalized_project_canons/project_tool_boundary_canon.md"
)
_BEGIN_MARKER = "KANDA_PROJECT_TOOL_BOUNDARY_BEGIN"
_END_MARKER = "KANDA_PROJECT_TOOL_BOUNDARY_END"

_GUARDRAILS = (
    {
        "key": "fire_shield",
        "label": "Fire Shield",
        "prompt_code": "KPR-12-001",
        "prompt_id": "project_tool_boundary_canon",
        "relative_path": _PROMPT_REL,
        "purpose": "apply the canonical Fire Shield Tool/Project protection rules",
        "sections": (
            "## Explicit code-placement and cross-write rule",
            "## Fire Shield programmatic authority",
        ),
    },
    {
        "key": "brick_wall",
        "label": "Brick Wall",
        "prompt_code": "KPR-03-001",
        "prompt_id": "brick_wall_comprehensive_quality_gate",
        "relative_path": _PROMPT_ROOT
        / "03_governance_freeze_and_handoff/brick_wall_comprehensive_quality_gate.md",
        "purpose": "apply the canonical Brick Wall comprehensive quality gate",
        "sections": (),
    },
    {
        "key": "no_leak",
        "label": "No-Leak",
        "prompt_code": "KPR-04-001",
        "prompt_id": "box_architecture_canon",
        "relative_path": _PROMPT_ROOT
        / "04_box_architecture_and_boundaries/box_architecture_canon.md",
        "purpose": "apply the canonical Box Architecture No-Leak ownership rules",
        "sections": (
            "## Public contract and private internals",
            "## NO_LEAK ownership split",
            "## Anti-pattern identities",
        ),
    },
    {
        "key": "box_logic",
        "label": "Box Logic",
        "prompt_code": "KPR-04-001",
        "prompt_id": "box_architecture_canon",
        "relative_path": _PROMPT_ROOT
        / "04_box_architecture_and_boundaries/box_architecture_canon.md",
        "purpose": "apply the canonical Box Architecture ownership and boundary rules",
        "sections": (),
    },
    {
        "key": "module_size",
        "label": "Module Size",
        "prompt_code": "KPR-06-007",
        "prompt_id": "large_module_refactor_protocol",
        "relative_path": _PROMPT_ROOT
        / "06_refactor_and_architecture_hardening/large_module_refactor_protocol.md",
        "purpose": "apply the canonical module-size and cohesion rules",
        "sections": (),
    },
    {
        "key": "runtime_evidence",
        "label": "Runtime Evidence",
        "prompt_code": "KPR-01-014",
        "prompt_id": "ai_prompt_request_canon",
        "relative_path": _PROMPT_ROOT
        / "01_session_start_and_navigation/ai_prompt_request_canon.md",
        "purpose": "apply the canonical Runtime Evidence Escalation contract",
        "sections": ("## Runtime Evidence Escalation",),
    },
)


def build_project_tool_boundary_wrapper() -> str:
    """Build a wrapper containing the exact canonical Tool/Project prompt."""
    prompt_path = _resolve_tool_prompt_path(_PROMPT_REL)
    prompt_text = prompt_path.read_text(encoding="utf-8-sig").rstrip()
    parts = [
        _BEGIN_MARKER,
        "Prompt code: KPR-12-001",
        "Prompt id: project_tool_boundary_canon",
        "Purpose: enforce KANDA Tool versus selected-Project code placement.",
        "Source: canonical KANDA prompt-library file.",
        "",
        "KANDA_PROJECT_TOOL_PROMPT_FILE_BEGIN project_tool_boundary_canon.md",
        prompt_text,
        "KANDA_PROJECT_TOOL_PROMPT_FILE_END project_tool_boundary_canon.md",
        "",
        _END_MARKER,
    ]
    return "\n".join(parts) + "\n"


def copy_project_tool_boundary_to_clipboard(window: Any) -> None:
    """Copy the canonical Tool/Project boundary wrapper to the clipboard."""
    try:
        from PySide6.QtWidgets import QApplication

        QApplication.clipboard().setText(build_project_tool_boundary_wrapper())
        message = "Copied Tool x Project boundary prompt to clipboard."
        _set_status(window, message)
        _append_log(window, message)
    except Exception as exc:
        message = "[ERROR] Could not copy Tool x Project prompt: " + str(exc)
        _set_status(window, message)
        _append_log(window, message)


def install_control(window: Any) -> None:
    """Insert the right-aligned governance prompt row without widening the GUI."""
    if getattr(window, "copy_project_tool_boundary_button", None) is not None:
        return

    from PySide6.QtGui import QColor, QPalette
    from PySide6.QtWidgets import QHBoxLayout, QPushButton

    tabs = getattr(window, "tabs", None)
    if tabs is None or tabs.count() < 1:
        raise RuntimeError("Show Project tab container was not found.")
    collector_tab = tabs.widget(0)
    collector_layout = collector_tab.layout() if collector_tab is not None else None
    if collector_layout is None:
        raise RuntimeError("Show Project layout was not found.")

    row = QHBoxLayout()
    row.addStretch(1)

    for spec in _GUARDRAILS:
        button = _build_orange_button(
            QPushButton,
            QColor,
            QPalette,
            str(spec["label"]),
            "Copy canonical " + str(spec["label"]) + " prompt context.",
        )
        setattr(window, "copy_" + str(spec["key"]) + "_button", button)
        button.clicked.connect(
            lambda checked=False, current=spec: _copy_guardrail_to_clipboard(
                window,
                current,
            )
        )
        row.addWidget(button)

    button = QPushButton("Tool x Project")
    palette = button.palette()
    palette.setColor(QPalette.ButtonText, QColor("#ff4d00"))
    button.setPalette(palette)
    font = button.font()
    font.setBold(True)
    button.setFont(font)
    button.setToolTip(
        "Copy the canonical KANDA Tool versus selected-Project boundary prompt."
    )
    row.addWidget(button)
    collector_layout.insertLayout(1, row)
    window.copy_project_tool_boundary_button = button
    button.clicked.connect(
        lambda: copy_project_tool_boundary_to_clipboard(window)
    )


def _build_orange_button(
    button_class: Any,
    color_class: Any,
    palette_class: Any,
    label: str,
    tooltip: str,
) -> Any:
    """Create one orange, bold clipboard button using the existing GUI style."""
    button = button_class(label)
    palette = button.palette()
    palette.setColor(palette_class.ButtonText, color_class("#ff4d00"))
    button.setPalette(palette)
    font = button.font()
    font.setBold(True)
    button.setFont(font)
    button.setToolTip(tooltip)
    return button


def _copy_guardrail_to_clipboard(window: Any, spec: dict[str, object]) -> None:
    """Copy one canonical guardrail prompt wrapper to the clipboard."""
    try:
        from PySide6.QtWidgets import QApplication

        text = _build_guardrail_wrapper(spec)
        QApplication.clipboard().setText(text)
        message = "Copied " + str(spec["label"]) + " prompt context to clipboard."
        _set_status(window, message)
        _append_log(window, message)
    except Exception as exc:
        message = (
            "[ERROR] Could not copy "
            + str(spec["label"])
            + " prompt context: "
            + str(exc)
        )
        _set_status(window, message)
        _append_log(window, message)


def _build_guardrail_wrapper(spec: dict[str, object]) -> str:
    """Build a wrapper from one existing ACTIVE prompt-library source."""
    relative_path = Path(str(spec["relative_path"]))
    prompt_path = _resolve_tool_prompt_path(relative_path)
    prompt_text = prompt_path.read_text(encoding="utf-8-sig").rstrip()
    sections = tuple(str(item) for item in spec.get("sections", ()))
    if sections:
        prompt_text = _extract_sections(prompt_text, sections)

    key = str(spec["key"]).upper()
    filename = prompt_path.name
    parts = [
        "KANDA_" + key + "_PROMPT_CONTEXT_BEGIN",
        "Prompt code: " + str(spec["prompt_code"]),
        "Prompt id: " + str(spec["prompt_id"]),
        "Purpose: " + str(spec["purpose"]) + ".",
        "Source: canonical KANDA prompt-library file.",
        "Canonical source: " + relative_path.as_posix(),
        "",
        "KANDA_" + key + "_PROMPT_FILE_BEGIN " + filename,
        prompt_text,
        "KANDA_" + key + "_PROMPT_FILE_END " + filename,
        "",
        "KANDA_" + key + "_PROMPT_CONTEXT_END",
    ]
    return "\n".join(parts) + "\n"


def _extract_sections(prompt_text: str, headings: tuple[str, ...]) -> str:
    """Extract exact level-two Markdown sections from a canonical prompt."""
    lines = prompt_text.splitlines()
    selected: list[str] = []
    for heading in headings:
        try:
            start = lines.index(heading)
        except ValueError as exc:
            raise ValueError("Canonical prompt section not found: " + heading) from exc
        end = len(lines)
        for index in range(start + 1, len(lines)):
            if lines[index].startswith("## "):
                end = index
                break
        section = "\n".join(lines[start:end]).strip()
        if section:
            selected.append(section)
    if not selected:
        raise ValueError("Canonical prompt section selection was empty.")
    return "\n\n".join(selected)


def _resolve_tool_prompt_path(relative_path: Path) -> Path:
    """Resolve a canonical prompt only from the KANDA Tool root."""
    tool_root = Path(__file__).resolve().parents[3]
    prompt_path = tool_root / relative_path
    if prompt_path.is_file():
        return prompt_path
    raise FileNotFoundError(
        "Canonical Tool prompt not found: " + str(relative_path)
    )


def _set_status(window: Any, message: str) -> None:
    status = getattr(window, "first_prompt_status_label", None)
    if status is not None:
        try:
            status.setText(message)
        except Exception:
            pass


def _append_log(window: Any, message: str) -> None:
    try:
        getattr(window, "_append_log")(message)
    except Exception:
        pass
