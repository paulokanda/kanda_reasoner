# project-path: kanda_reasoner_app/manage_architecture/ast_split_web_ai_gui.py
"""Web AI risk-repair wrapper controls for AST Split Audit.

The wrapper preserves the frozen single-window UI contract while enriching the
clipboard handoff with bounded read-only preflight evidence from the subordinate
AST-safe refactor infrastructure.
"""
from __future__ import annotations

from hashlib import sha256
from importlib import import_module
from pathlib import Path

from kanda_reasoner_app.external_ai_workflow import (
    handoff_to_selected_external_ai,
)
from kanda_reasoner_app.manage_architecture.kanda_ast_safe_refactor_orchestrator import (
    build_preflight_evidence_text,
)

__all__ = [
    "add_ast_split_web_ai_risk_repair_button",
    "bind_ast_split_web_ai_single_output",
    "build_ast_split_web_ai_risk_repair_wrapper",
    "build_safe_refactor_how_to_bundle",
    "copy_ast_split_web_ai_risk_repair_wrapper",
    "copy_safe_refactor_how_to_bundle",
]

PROMPT_RELATIVE_PATH = Path(
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/"
    "06_refactor_and_architecture_hardening/"
    "web_ai_ast_split_risk_repair_protocol.md"
)

SAFE_REFACTOR_HOW_TO_PROMPT_RELATIVE_PATH = Path(
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/"
    "06_refactor_and_architecture_hardening/"
    "safe_refactor_how_to.md"
)

SAFE_REFACTOR_SUPPORT_ARTIFACTS = (
    (
        "CURRENT_CANONICAL_ROUTINE_GUIDE",
        "Current canonical process guide; use as active support context.",
        Path("kanda_reasoner_app/manage_architecture/AST_SAFE_REFACTOR_ROUTINE.md"),
    ),
    (
        "CURRENT_CANONICAL_ROUTINE_IMPLEMENTATION",
        "Current canonical read-only helper implementation; do not treat as a source writer.",
        Path("kanda_reasoner_app/manage_architecture/kanda_ast_safe_refactor_routine.py"),
    ),
    (
        "NON_AUTHORITATIVE_WORKED_REPORT_EXAMPLE",
        "Historical evidence-shape example only; never reuse its paths, hashes, or audit truth.",
        Path(
            "kanda_reasoner_app/manage_architecture/"
            "runtime_activation_refactor_routine_report_example.json"
        ),
    ),
)


def add_ast_split_web_ai_risk_repair_button(
    window: object,
    action_row: object,
) -> None:
    """Add the Web AI SAFE-repair action after the split handoff button."""
    QtWidgets = import_module("PySide6.QtWidgets")
    button = QtWidgets.QPushButton("Send Web AI to make SAFE")
    button.setObjectName("architectureReviewAstSplitSendWebAiMakeSafeButton")
    button.setStyleSheet("color: #FF8C00; font-weight: bold;")
    button.setToolTip(
        "Copy KPR-06-003 with exact source, AST audit, and bounded preflight evidence."
    )
    button.clicked.connect(
        lambda: copy_ast_split_web_ai_risk_repair_wrapper(window)
    )
    action_row.addWidget(button)

    how_to_button = QtWidgets.QPushButton("Safe Refactor How To")
    how_to_button.setObjectName("architectureReviewAstSplitSafeRefactorHowToButton")
    how_to_button.setStyleSheet("color: #FF8C00; font-weight: bold;")
    how_to_button.setToolTip(
        "Copy the canonical safe-refactor runbook plus current routine support artifacts."
    )
    how_to_button.clicked.connect(
        lambda: copy_safe_refactor_how_to_bundle(window)
    )
    action_row.addWidget(how_to_button)


def bind_ast_split_web_ai_single_output(window: object) -> None:
    """Use the existing AST output as the only audit and Web AI response window."""
    output = getattr(window, "_large_module_split_output", None)
    if output is None:
        raise ValueError("Large Module AST Split Audit output widget is missing.")
    output.setReadOnly(False)
    output.setPlaceholderText(
        "Run AST Split Audit, or replace this text with the complete Web AI "
        "Large Module AST Split Audit Markdown report."
    )
    target_edit = getattr(window, "_large_module_target_edit", None)
    if target_edit is not None:
        target_edit.textChanged.connect(
            lambda _text="": _clear_single_output_for_target_change(window)
        )


def copy_ast_split_web_ai_risk_repair_wrapper(window: object) -> None:
    """Copy canonical prompt, source, audit, and bounded refactor evidence."""
    QtWidgets = import_module("PySide6.QtWidgets")
    try:
        root = _project_root(window)
        target = _target_path(window, root)
        prompt_path = _prompt_path(window, root)
        audit_text = _audit_text(window)
        source_text = target.read_text(encoding="utf-8", errors="strict")
        safety_label = _safety_label_text(window)
        target_relative_path = target.relative_to(root).as_posix()
        preflight_evidence = build_preflight_evidence_text(
            root,
            target_relative_path=target_relative_path,
            source_text=source_text,
            audit_text=audit_text,
        )
        wrapper = build_ast_split_web_ai_risk_repair_wrapper(
            prompt_text=prompt_path.read_text(encoding="utf-8", errors="strict"),
            target_relative_path=target_relative_path,
            source_text=source_text,
            audit_text=audit_text,
            safety_label=safety_label,
            preflight_evidence_text=preflight_evidence,
        )
        handoff = handoff_to_selected_external_ai(wrapper)
        if not handoff.ok:
            raise RuntimeError(handoff.error)
    except (OSError, RuntimeError, UnicodeError, ValueError) as exc:
        QtWidgets.QMessageBox.warning(
            window,
            "Web AI SAFE repair wrapper not ready",
            str(exc),
        )
        return

    status_bar = getattr(window, "statusBar", None)
    if callable(status_bar):
        status_bar().showMessage(
            "Copied AST risk-repair evidence and opened "
            + handoff.display_name
        )


def copy_safe_refactor_how_to_bundle(window: object) -> None:
    """Copy Safe Refactor How To plus three separated support artifacts."""
    QtWidgets = import_module("PySide6.QtWidgets")
    try:
        root = _project_root(window)
        prompt_path = _resolve_project_or_app_file(
            root, SAFE_REFACTOR_HOW_TO_PROMPT_RELATIVE_PATH
        )
        support_artifacts: list[tuple[str, str, str, str]] = []
        for name, role, relative_path in SAFE_REFACTOR_SUPPORT_ARTIFACTS:
            path = _resolve_project_or_app_file(root, relative_path)
            support_artifacts.append(
                (
                    name,
                    role,
                    relative_path.as_posix(),
                    path.read_text(encoding="utf-8", errors="strict"),
                )
            )
        clipboard_text = build_safe_refactor_how_to_bundle(
            prompt_text=prompt_path.read_text(encoding="utf-8", errors="strict"),
            support_artifacts=support_artifacts,
        )
        handoff = handoff_to_selected_external_ai(clipboard_text)
        if not handoff.ok:
            raise RuntimeError(handoff.error)
    except (OSError, RuntimeError, UnicodeError, ValueError) as exc:
        QtWidgets.QMessageBox.warning(
            window,
            "Safe Refactor How To not ready",
            str(exc),
        )
        return

    status_bar = getattr(window, "statusBar", None)
    if callable(status_bar):
        status_bar().showMessage(
            "Copied Safe Refactor How To bundle and opened "
            + handoff.display_name
        )


def build_safe_refactor_how_to_bundle(
    *,
    prompt_text: str,
    support_artifacts: list[tuple[str, str, str, str]],
) -> str:
    """Build one deterministic prompt-plus-support clipboard payload."""
    if not prompt_text.strip():
        raise ValueError("Safe Refactor How To prompt is empty.")
    if len(support_artifacts) != 3:
        raise ValueError("Safe Refactor How To requires exactly three support artifacts.")

    parts = [
        prompt_text.rstrip(),
        "",
        "# SAFE REFACTOR HOW TO SUPPORT BUNDLE",
        "",
        "SAFE_REFACTOR_HOW_TO_SUPPORT_BUNDLE_BEGIN",
    ]
    for name, role, relative_path, content in support_artifacts:
        if not name.strip() or not role.strip() or not relative_path.strip() or not content:
            raise ValueError("Safe Refactor support artifact is incomplete: " + name)
        parts.extend(
            [
                "",
                "SAFE_REFACTOR_SUPPORT_ARTIFACT_BEGIN",
                "NAME: " + name,
                "ROLE: " + role,
                "RELATIVE_PATH: " + relative_path,
                "CONTENT_BEGIN",
                content.rstrip(),
                "CONTENT_END",
                "SAFE_REFACTOR_SUPPORT_ARTIFACT_END",
            ]
        )
    parts.extend(["", "SAFE_REFACTOR_HOW_TO_SUPPORT_BUNDLE_END", ""])
    return "\n".join(parts)


def _source_block(source_text: str) -> str:
    """Serialize exact source text with one delimiter newline outside its identity."""
    delimiter = "" if source_text.endswith("\n") else "\n"
    return (
        "TARGET_SOURCE_BEGIN\n"
        + source_text
        + delimiter
        + "TARGET_SOURCE_END\n"
    )


def build_ast_split_web_ai_risk_repair_wrapper(
    *,
    prompt_text: str,
    target_relative_path: str,
    source_text: str,
    audit_text: str,
    safety_label: str,
    preflight_evidence_text: str = "",
) -> str:
    """Build one deterministic clipboard wrapper for external Web AI review."""
    if not prompt_text.strip():
        raise ValueError("Canonical AST risk-repair prompt is empty.")
    if not target_relative_path.strip():
        raise ValueError("Target path is empty.")
    if not source_text:
        raise ValueError("Target source is empty.")
    if not audit_text.strip():
        raise ValueError("Run AST Split Audit before sending the repair wrapper.")

    source_bytes = source_text.encode("utf-8")
    digest = sha256(source_bytes).hexdigest()
    evidence_block = ""
    if preflight_evidence_text.strip():
        evidence_block = (
            "\nAST_SAFE_REFACTOR_PREFLIGHT_EVIDENCE_BEGIN\n"
            + preflight_evidence_text.rstrip()
            + "\nAST_SAFE_REFACTOR_PREFLIGHT_EVIDENCE_END\n"
        )
    return (
        prompt_text.rstrip()
        + "\n\n# CURRENT AST SPLIT RISK REPAIR INPUT\n\n"
        + "KANDA_AST_SPLIT_RISK_REPAIR_INPUT_BEGIN\n"
        + "TARGET_RELATIVE_PATH: "
        + target_relative_path
        + "\nSOURCE_SHA256: "
        + digest
        + "\nSOURCE_BYTE_LENGTH: "
        + str(len(source_bytes))
        + "\nSOURCE_TEXT_ENDS_WITH_NEWLINE: "
        + ("true" if source_text.endswith("\n") else "false")
        + "\nCURRENT_SAFETY_LABEL: "
        + (safety_label.strip() or "UNKNOWN")
        + evidence_block
        + "\nAST_AUDIT_RESULT_BEGIN\n"
        + audit_text.rstrip()
        + "\nAST_AUDIT_RESULT_END\n\n"
        + _source_block(source_text)
        + "KANDA_AST_SPLIT_RISK_REPAIR_INPUT_END\n"
    )


def _clear_single_output_for_target_change(window: object) -> None:
    """Clear stale target-specific AST or Web AI text when the target changes."""
    output = getattr(window, "_large_module_split_output", None)
    if output is not None:
        output.clear()
    window._last_large_module_split_handoff = ""
    update_label = getattr(window, "_update_large_module_refactor_safety_label", None)
    if callable(update_label):
        update_label({})
    sync_controls = getattr(window, "_sync_large_module_target_controls", None)
    if callable(sync_controls):
        sync_controls()


def _project_root(window: object) -> Path:
    """Resolve the active Architecture Review project root."""
    edit = getattr(window, "_root_path_edit", None)
    text = edit.text().strip() if edit is not None else ""
    if not text:
        raise ValueError("Active project root is empty.")
    root = Path(text).resolve()
    if not root.is_dir():
        raise ValueError("Active project root does not exist: " + str(root))
    return root


def _target_path(window: object, root: Path) -> Path:
    """Resolve one active AST target and enforce project-root shielding."""
    edit = getattr(window, "_large_module_target_edit", None)
    text = edit.text().strip() if edit is not None else ""
    if not text:
        raise ValueError("Large Module AST Split Audit target is empty.")
    candidate = Path(text)
    target = (candidate if candidate.is_absolute() else root / candidate).resolve()
    try:
        target.relative_to(root)
    except ValueError as exc:
        raise ValueError("AST Split Audit target must stay inside active project root.") from exc
    if target.suffix.lower() != ".py" or not target.is_file():
        raise ValueError("AST Split Audit target must be an existing .py file.")
    return target


def _resolve_project_or_app_file(root: Path, relative_path: Path) -> Path:
    """Resolve one current project/app artifact without Downloads/Desktop fallback."""
    candidates = [
        root / relative_path,
        Path(__file__).resolve().parents[2] / relative_path,
    ]
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    raise ValueError("Required Safe Refactor artifact was not found: " + str(candidates[0]))


def _prompt_path(window: object, root: Path) -> Path:
    """Resolve the canonical routed KPR-06-003 prompt without fallback leakage."""
    candidates = [
        root / PROMPT_RELATIVE_PATH,
        Path(__file__).resolve().parents[2] / PROMPT_RELATIVE_PATH,
    ]
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    raise ValueError("Canonical AST risk-repair prompt was not found: " + str(candidates[0]))


def _audit_text(window: object) -> str:
    """Return current native AST Markdown evidence from the frozen single window."""
    handoff = str(getattr(window, "_last_large_module_split_handoff", "") or "")
    if handoff.strip():
        return handoff
    output = getattr(window, "_large_module_split_output", None)
    return output.toPlainText() if output is not None else ""


def _safety_label_text(window: object) -> str:
    """Return the current visible safety label without modifying classifier state."""
    label = getattr(window, "_large_module_refactor_safety_label", None)
    return label.text() if label is not None else "UNKNOWN"
