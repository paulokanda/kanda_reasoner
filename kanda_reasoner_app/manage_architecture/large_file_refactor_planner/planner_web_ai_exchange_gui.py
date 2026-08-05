# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/planner_web_ai_exchange_gui.py
"""Qt bridge for export-to-Web-AI and installed-version import review."""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from typing import Any

from PySide6.QtWidgets import (
    QDialog,
    QLabel,
    QPlainTextEdit,
    QPushButton,
    QVBoxLayout,
)

from kanda_reasoner_app.external_ai_workflow import (
    handoff_to_selected_external_ai,
)

from .docstring_formatting import format_docstring_proposals
from .models import PlannerState
from .planner_web_ai_exchange import (
    build_comprehensive_web_ai_planning_prompt,
    format_web_ai_proposal,
    parse_and_validate_web_ai_planning_response,
)
from .planner_web_ai_import_artifact import (
    build_web_ai_import_contract,
    read_installed_web_ai_response,
    stage_validated_web_ai_response,
    web_ai_import_artifact_path,
)
from .planner_version_selector_gui import (
    refresh_planner_version_selector,
    render_selected_planner_version,
)
from .planner_version_state import (
    PLANNER_VERSION_HEURISTIC,
    PLANNER_VERSION_LOCAL_AI,
    PLANNER_VERSION_WEB_AI,
    get_last_generated_native_bundle,
    get_planner_version_bundle,
    select_planner_version,
    store_web_ai_version,
)
from .split_formatting import format_split_plan

__all__ = [
    "copy_comprehensive_planning_for_web_ai",
    "copy_web_ai_refactor_version_how_to",
    "copy_web_ai_split_file_wrapper",
    "open_pasted_planning_from_web_ai",
    "open_receive_planning_from_web_ai",
    "open_view_web_ai_proposal",
]


WEB_AI_BUNDLE_BLUEPRINT_PROMPT_RELATIVE_PATH = (
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/"
    "06_refactor_and_architecture_hardening/"
    "web_ai_planning_response_bundle_blueprint.md"
)


WEB_AI_REFACTOR_HOWTO_PROMPT_RELATIVE_PATH = (
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/"
    "06_refactor_and_architecture_hardening/"
    "web_ai_large_module_refactor_exchange_protocol.md"
)



def copy_web_ai_split_file_wrapper(window: object) -> None:
    """Copy the canonical bundle blueprint plus current target planning package."""

    prompt_path = _prompt_library_source_path(
        window, WEB_AI_BUNDLE_BLUEPRINT_PROMPT_RELATIVE_PATH
    )
    if not prompt_path.is_file():
        _show_plan_message(
            window,
            "WEB AI PLANNING RESPONSE BUNDLE BLUEPRINT NOT FOUND\n\n"
            + str(prompt_path),
        )
        return
    try:
        report, bundle = _required_export_state(window)
    except ValueError as exc:
        _show_plan_message(window, "WEB AI SPLIT WRAPPER NOT READY\n\n" + str(exc))
        return
    local_result = getattr(window, "_large_file_refactor_plan_ai_review_result", None)
    project_root = _project_root_text(window)
    planning_package = build_comprehensive_web_ai_planning_prompt(
        report,
        bundle.plan,
        list(bundle.docstring_proposals),
        local_ai_summary=_local_review_summary(local_result),
        import_contract=build_web_ai_import_contract(project_root),
        base_version_name=bundle.version_name,
    )
    blueprint = prompt_path.read_text(encoding="utf-8").rstrip()
    clipboard_text = (
        blueprint
        + "\n\n# CURRENT TARGET-SPECIFIC PLANNING PACKAGE\n\n"
        + planning_package
    )
    handoff = handoff_to_selected_external_ai(clipboard_text)
    if not handoff.ok:
        _show_plan_message(window, "EXTERNAL AI HANDOFF BLOCKED\n\n" + handoff.error)
        return
    status = getattr(window, "_large_file_refactor_status_label", None)
    if status is not None:
        status.setText(
            "Web AI split wrapper copied and opened in " + handoff.display_name
        )


def copy_web_ai_refactor_version_how_to(window: object) -> None:
    """Copy the canonical external Web AI refactor exchange protocol."""

    prompt_path = _prompt_library_source_path(
        window, WEB_AI_REFACTOR_HOWTO_PROMPT_RELATIVE_PATH
    )
    if not prompt_path.is_file():
        output = getattr(window, "_large_file_refactor_plan_output", None)
        if output is not None:
            output.setPlainText(
                "WEB AI REFACTOR VERSION HOW TO NOT FOUND\n\n"
                + str(prompt_path)
            )
        return
    handoff = handoff_to_selected_external_ai(
        prompt_path.read_text(encoding="utf-8")
    )
    if not handoff.ok:
        _show_plan_message(window, "EXTERNAL AI HANDOFF BLOCKED\n\n" + handoff.error)
        return
    status = getattr(window, "_large_file_refactor_status_label", None)
    if status is not None:
        status.setText(
            "Web AI Refactor Version How To copied and opened in "
            + handoff.display_name
        )


def _prompt_library_source_path(window: object, relative_path: str) -> Path:
    """Resolve one canonical Prompt Library source from the KANDA Tool root."""

    _ = window
    return Path(__file__).resolve().parents[3] / relative_path

def copy_comprehensive_planning_for_web_ai(window: object) -> None:
    """Copy the most recently generated native plan for external Web AI work."""

    report, bundle = _required_export_state(window)
    local_result = getattr(window, "_large_file_refactor_plan_ai_review_result", None)
    project_root = _project_root_text(window)
    text = build_comprehensive_web_ai_planning_prompt(
        report,
        bundle.plan,
        list(bundle.docstring_proposals),
        local_ai_summary=_local_review_summary(local_result),
        import_contract=build_web_ai_import_contract(project_root),
        base_version_name=bundle.version_name,
    )
    handoff = handoff_to_selected_external_ai(text)
    if not handoff.ok:
        _show_plan_message(window, "EXTERNAL AI HANDOFF BLOCKED\n\n" + handoff.error)
        return
    window._large_file_refactor_plan_output.setPlainText(
        "COMPREHENSIVE PLANNING COPIED AND EXTERNAL AI OPENED\n\n"
        "Assistant: " + handoff.display_name + "\n\n"
        "Export base version: " + _display_version_name(bundle.version_name) + "\n\n"
        "The external Web AI should return a governed ZIP by default. Install, "
        "validate, and prepare freeze evidence, then select Imported Web AI "
        "Version to validate and review the installed artifact. Alternative: "
        "paste the exact marker-wrapped response directly into Panel 4: "
        "Proposed split plan."
    )


def open_receive_planning_from_web_ai(
    window: object,
    *,
    refresh_callback: Callable[[object], None],
    base_plan: object | None = None,
    base_docstring_proposals: list[object] | None = None,
) -> None:
    """Load canonical installed ZIP artifact, validate it, and open review."""

    report = getattr(window, "_large_file_refactor_last_analysis", None)
    if report is None:
        _show_plan_message(
            window,
            "Run Analyze File before receiving an imported Web AI version.",
        )
        return
    project_root = _project_root_text(window)
    try:
        raw_text = read_installed_web_ai_response(project_root)
        proposal, base_version_name = _validate_raw_web_ai_response(
            window,
            report,
            raw_text,
            base_plan=base_plan,
            base_docstring_proposals=base_docstring_proposals,
        )
    except (FileNotFoundError, ValueError, OSError, UnicodeError) as exc:
        artifact = web_ai_import_artifact_path(project_root)
        _show_plan_message(
            window,
            "IMPORTED WEB AI VERSION NOT READY\n\n"
            + str(exc)
            + "\n\nExpected installed artifact:\n"
            + str(artifact)
            + "\n\nAlternative: paste the complete marker-wrapped response "
            "directly into Panel 4: Proposed split plan.",
        )
        refresh_callback(window)
        return
    window._large_file_refactor_web_ai_proposal_applied = False
    _open_web_ai_review_dialog(
        window,
        proposal,
        base_version_name,
        refresh_callback,
        intake_label="Installed ZIP artifact",
    )


def open_pasted_planning_from_web_ai(
    window: object,
    raw_text: str,
    *,
    refresh_callback: Callable[[object], None],
) -> None:
    """Validate direct panel paste through the same external artifact boundary."""

    report = getattr(window, "_large_file_refactor_last_analysis", None)
    if report is None:
        _show_plan_message(
            window,
            "PASTED WEB AI RESPONSE REJECTED\n\n"
            "Run Analyze File before pasting a Web AI planning response.",
        )
        return
    if not isinstance(raw_text, str) or not raw_text.strip():
        _show_plan_message(
            window,
            "PASTED WEB AI RESPONSE REJECTED\n\nClipboard text is empty.",
        )
        return
    project_root = _project_root_text(window)
    try:
        proposal, base_version_name = _validate_raw_web_ai_response(
            window,
            report,
            raw_text,
            base_plan=None,
            base_docstring_proposals=None,
        )
        stage_validated_web_ai_response(project_root, raw_text)
        installed_text = read_installed_web_ai_response(project_root)
        if installed_text != raw_text:
            raise OSError("Staged Web AI response differs from validated paste.")
        installed_proposal, installed_base = _validate_raw_web_ai_response(
            window,
            report,
            installed_text,
            base_plan=None,
            base_docstring_proposals=None,
        )
        if installed_proposal.response_hash != proposal.response_hash:
            raise ValueError("Web AI response hash changed after stage/read-back.")
        if installed_base != base_version_name:
            raise ValueError("Web AI base version changed after stage/read-back.")
    except (ValueError, OSError, UnicodeError) as exc:
        _show_plan_message(
            window,
            "PASTED WEB AI RESPONSE REJECTED\n\n" + str(exc),
        )
        refresh_callback(window)
        return
    window._large_file_refactor_web_ai_proposal_applied = False
    _open_web_ai_review_dialog(
        window,
        installed_proposal,
        installed_base,
        refresh_callback,
        intake_label="Direct Panel 4 paste",
    )


def _validate_raw_web_ai_response(
    window: object,
    report: object,
    raw_text: str,
    *,
    base_plan: object | None,
    base_docstring_proposals: list[object] | None,
) -> tuple[Any, str]:
    """Validate one response against native Planner or explicit Workbench base."""

    if base_plan is None:
        return _validate_against_native_versions(window, report, raw_text)
    proposal = parse_and_validate_web_ai_planning_response(
        raw_text,
        report,
        base_plan,
        list(
            base_docstring_proposals
            or getattr(base_plan, "docstring_proposals", ())
            or ()
        ),
    )
    return proposal, "current_workbench"


def _open_web_ai_review_dialog(
    window: object,
    proposal: Any,
    base_version_name: str,
    refresh_callback: Callable[[object], None],
    *,
    intake_label: str,
) -> None:
    """Review one validated proposal before explicit Imported Web AI activation."""

    window._large_file_refactor_web_ai_proposal = proposal
    dialog = QDialog(window)
    dialog.setWindowTitle("Review Imported Web AI Version")
    dialog.resize(980, 720)
    layout = QVBoxLayout(dialog)
    layout.addWidget(
        QLabel(
            intake_label
            + " validated against "
            + _display_version_name(base_version_name)
            + ". Review the resulting plan before loading it into Planner state."
        )
    )
    review_output = QPlainTextEdit()
    review_output.setReadOnly(True)
    review_output.setPlainText(
        format_split_plan(proposal.proposed_plan)
        + "\n\n"
        + format_docstring_proposals(list(proposal.proposed_docstrings))
        + "\n\n"
        + format_web_ai_proposal(proposal)
    )
    layout.addWidget(review_output, 1)
    load_btn = QPushButton("Load as Imported Web AI Version")
    close_btn = QPushButton("Close Without Loading")
    layout.addWidget(load_btn)
    layout.addWidget(close_btn)

    def load_imported_version() -> None:
        store_web_ai_version(
            window,
            proposal.proposed_plan,
            list(proposal.proposed_docstrings),
        )
        select_planner_version(window, PLANNER_VERSION_WEB_AI)
        window._large_file_refactor_web_ai_proposal_applied = True
        window._large_file_refactor_planner_state = (
            PlannerState.BLOCKED.value
            if proposal.proposed_plan.status == "blocked"
            else PlannerState.DOCSTRING_READY.value
        )
        refresh_planner_version_selector(window)
        render_selected_planner_version(window)
        refresh_callback(window)
        dialog.accept()

    load_btn.clicked.connect(load_imported_version)
    close_btn.clicked.connect(dialog.reject)
    refresh_callback(window)
    dialog.exec()


def _show_plan_message(window: object, text: str) -> None:
    """Write one intake status message without assuming a concrete panel class."""

    output = getattr(window, "_large_file_refactor_plan_output", None)
    if output is not None:
        output.setPlainText(text)

def open_view_web_ai_proposal(window: object) -> None:
    """Show the latest validated installed Web AI proposal without changing state."""

    proposal = getattr(window, "_large_file_refactor_web_ai_proposal", None)
    dialog = QDialog(window)
    dialog.setWindowTitle("Imported Web AI Version Review")
    dialog.resize(900, 620)
    layout = QVBoxLayout(dialog)
    output = QPlainTextEdit()
    output.setReadOnly(True)
    output.setPlainText(
        format_web_ai_proposal(proposal)
        if proposal is not None
        else "No installed Web AI version has been validated yet."
    )
    layout.addWidget(output, 1)
    close_btn = QPushButton("Close")
    close_btn.clicked.connect(dialog.accept)
    layout.addWidget(close_btn)
    dialog.exec()


def _required_export_state(window: object) -> tuple[Any, Any]:
    report = getattr(window, "_large_file_refactor_last_analysis", None)
    bundle = get_last_generated_native_bundle(window)
    if report is None or bundle is None or not bundle.docstring_proposals:
        raise ValueError(
            "Generate a Heuristic or Local AI split plan with docstrings before export."
        )
    return report, bundle


def _validate_against_native_versions(
    window: object,
    report: object,
    raw_text: str,
) -> tuple[Any, str]:
    """Validate the installed response against the native base it was exported from."""

    candidates: list[Any] = []
    latest = get_last_generated_native_bundle(window)
    if latest is not None:
        candidates.append(latest)
    for version_name in (PLANNER_VERSION_LOCAL_AI, PLANNER_VERSION_HEURISTIC):
        bundle = get_planner_version_bundle(window, version_name)
        if bundle is not None and all(
            item.version_name != bundle.version_name for item in candidates
        ):
            candidates.append(bundle)
    if not candidates:
        raise ValueError("No Heuristic or Local AI base version exists for validation.")
    errors: list[str] = []
    for bundle in candidates:
        try:
            proposal = parse_and_validate_web_ai_planning_response(
                raw_text,
                report,
                bundle.plan,
                list(bundle.docstring_proposals),
            )
        except ValueError as exc:
            errors.append(_display_version_name(bundle.version_name) + ": " + str(exc))
            continue
        return proposal, bundle.version_name
    raise ValueError(
        "Installed Web AI version did not match any available native base. "
        + " | ".join(errors)
    )


def _project_root_text(window: object) -> str:
    edit = getattr(window, "_root_path_edit", None)
    if edit is None:
        return str(Path.cwd())
    text = edit.text().strip()
    return text or str(Path.cwd())


def _local_review_summary(result: object | None) -> dict[str, Any]:
    if result is None:
        return {"status": "not_run"}
    return {
        "status": str(getattr(result, "status", "reviewed")),
        "warnings": [str(item) for item in getattr(result, "warnings", ())],
    }


def _display_version_name(version_name: str) -> str:
    return {
        PLANNER_VERSION_HEURISTIC: "Heuristic",
        PLANNER_VERSION_LOCAL_AI: "Local AI",
        PLANNER_VERSION_WEB_AI: "Imported Web AI Version",
    }.get(version_name, version_name)
