# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_completion_gui.py
"""Patch 4 completion review GUI and fail-closed Refactor Large Module button."""
from __future__ import annotations


from kanda_reasoner_app.manage_architecture.architecture_review_card_lifecycle import (
    release_completed_architecture_review_card,
    tool_source_root,
)

from PySide6.QtWidgets import (
    QCheckBox,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QVBoxLayout,
)

from .workbench_completion_review import (
    format_refactor_large_module_gate,
    format_semantic_diff_review,
    format_transaction_summary,
)
from .workbench_completion_apply_bridge import (
    execute_completion_transaction,
    format_completion_apply_outcome,
    rollback_completion_transaction,
)
from .workbench_completion_workflow import (
    CompletionEvidenceBundle,
    CompletionTransactionBundle,
    prepare_completion_evidence,
    prepare_completion_transaction,
    refresh_completion_review_state,
)
from .workbench_patch5_proof_status_gui import (
    read_and_render_patch5_executor_proof_status,
)
from .workbench_stage_correction_gui import (
    build_workbench_stage_correction_row,
    sync_workbench_stage_correction_controls_from_window,
)
from .workbench_diff_review_assistant_gui import (
    build_diff_review_assistant_box,
    sync_diff_review_assistant_controls,
)
from .external_ai_candidate_exchange_gui import (
    build_external_ai_candidate_exchange_box,
    sync_external_ai_candidate_exchange_controls,
)
from .workbench_external_source_stale_gui import sync_completion_external_source_stale_state
__all__ = ["build_workbench_completion_section"]


def build_workbench_completion_section(
    window: object,
    root_text_callback: object,
) -> QGroupBox:
    """Build semantic-first review, summary confirmation, and final button gate."""
    _initialize_completion_state(window)
    box = QGroupBox("7. Completion Review and Refactor Authorization")
    layout = QVBoxLayout(box)
    layout.addWidget(
        QLabel(
            "This is the final governed workflow stage. Prepare Completion Evidence "
            "after Source Apply Payload readiness, review Semantic Diff first and Text "
            "Diff second, acknowledge warnings, confirm the exact transaction summary, "
            "then use Refactor Large Module only when every gate passes."
        )
    )
    prepare_row = QHBoxLayout()
    prepare_btn = QPushButton("Prepare Completion Evidence")
    prepare_btn.setEnabled(False)
    prepare_btn.clicked.connect(
        lambda: _prepare_completion_evidence(window, root_text_callback)
    )
    window._large_file_refactor_workbench_completion_prepare_button = prepare_btn
    prepare_row.addWidget(prepare_btn)
    transaction_btn = QPushButton("Prepare Transaction Summary")
    transaction_btn.setEnabled(False)
    transaction_btn.clicked.connect(
        lambda: _prepare_transaction_summary(window, root_text_callback)
    )
    window._large_file_refactor_workbench_transaction_prepare_button = transaction_btn
    prepare_row.addWidget(transaction_btn)
    prepare_row.addStretch(1)
    layout.addLayout(prepare_row)

    window._large_file_refactor_workbench_completion_status_output = QPlainTextEdit()
    window._large_file_refactor_workbench_completion_status_output.setReadOnly(True)
    window._large_file_refactor_workbench_completion_status_output.setPlainText(
        "Prepare Completion Evidence after source payload readiness. This step "
        "builds execution, seal, Shadow, provenance, and review evidence without "
        "writing active project source."
    )
    layout.addWidget(window._large_file_refactor_workbench_completion_status_output, 1)
    layout.addWidget(build_workbench_stage_correction_row(window, "COMPLETION_EVIDENCE", root_text_callback, _sync_final_button))

    layout.addWidget(QLabel("Semantic Diff - primary review"))
    window._large_file_refactor_workbench_semantic_diff_output = QPlainTextEdit()
    window._large_file_refactor_workbench_semantic_diff_output.setReadOnly(True)
    window._large_file_refactor_workbench_semantic_diff_output.setPlainText(
        "Semantic review becomes available after completion evidence passes."
    )
    layout.addWidget(window._large_file_refactor_workbench_semantic_diff_output, 1)

    layout.addWidget(QLabel("Text Diff - secondary inspection"))
    window._large_file_refactor_workbench_text_diff_output = QPlainTextEdit()
    window._large_file_refactor_workbench_text_diff_output.setReadOnly(True)
    window._large_file_refactor_workbench_text_diff_output.setPlainText(
        "Raw text diff is secondary to the semantic review."
    )
    layout.addWidget(window._large_file_refactor_workbench_text_diff_output, 1)
    layout.addWidget(
        build_diff_review_assistant_box(window, root_text_callback)
    )
    layout.addWidget(
        build_external_ai_candidate_exchange_box(window, root_text_callback)
    )

    review_row = QHBoxLayout()
    review_check = QCheckBox("I reviewed the semantic diff")
    review_check.setEnabled(False)
    review_check.stateChanged.connect(
        lambda _state: _refresh_human_review_gate(window)
    )
    window._large_file_refactor_workbench_semantic_review_check = review_check
    review_row.addWidget(review_check)
    warning_check = QCheckBox("I acknowledge all listed warnings")
    warning_check.setEnabled(False)
    warning_check.stateChanged.connect(
        lambda _state: _refresh_human_review_gate(window)
    )
    window._large_file_refactor_workbench_warning_ack_check = warning_check
    review_row.addWidget(warning_check)
    review_row.addStretch(1)
    layout.addLayout(review_row)

    layout.addWidget(QLabel("Final Transaction Summary"))
    window._large_file_refactor_workbench_transaction_summary_output = QPlainTextEdit()
    window._large_file_refactor_workbench_transaction_summary_output.setReadOnly(True)
    window._large_file_refactor_workbench_transaction_summary_output.setPlainText(
        "Prepare completion evidence first, review it, then prepare the durable "
        "transaction summary."
    )
    layout.addWidget(window._large_file_refactor_workbench_transaction_summary_output, 1)

    confirm_check = QCheckBox("I confirm this exact transaction summary")
    confirm_check.setEnabled(False)
    confirm_check.stateChanged.connect(
        lambda _state: _refresh_human_review_gate(window)
    )
    window._large_file_refactor_workbench_transaction_confirm_check = confirm_check
    layout.addWidget(confirm_check)

    window._large_file_refactor_workbench_refactor_gate_output = QPlainTextEdit()
    window._large_file_refactor_workbench_refactor_gate_output.setReadOnly(True)
    read_and_render_patch5_executor_proof_status(
        window,
        root_text_callback,
    )
    layout.addWidget(window._large_file_refactor_workbench_refactor_gate_output, 1)

    final_btn = QPushButton("Refactor Large Module")
    final_btn.setEnabled(False)
    final_btn.setToolTip(
        "Enabled only when canonical Patch 5 freeze proof exists and all immutable "
        "review, payload, Shadow, transaction, and freshness gates pass."
    )
    final_btn.clicked.connect(
        lambda: _refactor_large_module_clicked(window, root_text_callback)
    )
    window._large_file_refactor_workbench_refactor_large_module_button = final_btn
    layout.addWidget(final_btn)

    rollback_btn = QPushButton("Rollback Journaled Transaction")
    rollback_btn.setEnabled(False)
    rollback_btn.clicked.connect(lambda: _rollback_journaled_transaction_clicked(window))
    window._large_file_refactor_workbench_transaction_rollback_button = rollback_btn
    layout.addWidget(rollback_btn)
    return box


def _initialize_completion_state(window: object) -> None:
    """Install GUI projection state without making widgets transaction truth owners."""
    window._large_file_refactor_workbench_completion_evidence = None
    window._large_file_refactor_workbench_completion_transaction = None
    window._large_file_refactor_workbench_transaction_apply_executor_proven = False
    window._large_file_refactor_workbench_completion_apply_outcome = None
    window._large_file_refactor_workbench_completion_rollback_result = None


def _prepare_completion_evidence(window: object, root_text_callback: object) -> None:
    """Assemble frozen Patch 1-3 evidence and render semantic/text review."""
    snapshot = getattr(window, "_large_file_refactor_workbench_plan_snapshot", None)
    preview = getattr(window, "_large_file_refactor_workbench_real_preview", None)
    preflight = getattr(window, "_large_file_refactor_workbench_preflight_backup", None)
    payload = getattr(window, "_large_file_refactor_workbench_source_payload", None)
    if not all((snapshot, preview, preflight, payload)):
        _set_status(
            window,
            "COMPLETION EVIDENCE BLOCKED\nMissing snapshot, preview, preflight, or source payload.",
        )
        return
    try:
        bundle = prepare_completion_evidence(
            snapshot=snapshot,
            preview=preview,
            preflight=preflight,
            source_payload=payload,
            active_project_root=str(root_text_callback(window)),
        )
    except Exception as exc:
        _set_status(window, "COMPLETION EVIDENCE BLOCKED\n" + str(exc))
        return
    window._large_file_refactor_workbench_completion_evidence = bundle
    window._large_file_refactor_workbench_completion_transaction = None
    _render_completion_evidence(window, bundle)
    transaction_btn = getattr(
        window,
        "_large_file_refactor_workbench_transaction_prepare_button",
        None,
    )
    if transaction_btn is not None:
        transaction_btn.setEnabled(True)
    review_check = getattr(window, "_large_file_refactor_workbench_semantic_review_check", None)
    warning_check = getattr(window, "_large_file_refactor_workbench_warning_ack_check", None)
    if review_check is not None:
        review_check.setEnabled(True)
    if warning_check is not None:
        warning_check.setEnabled(True)
    _set_status(
        window,
        "COMPLETION EVIDENCE READY\n"
        f"contract: {bundle.contract.contract_id}\n"
        f"payload: {bundle.sealed_payload.payload_hash}\n"
        f"shadow: {bundle.shadow_validation.status}\n"
        "No active project source mutation occurred.",
    )
    sync_diff_review_assistant_controls(window)
    sync_external_ai_candidate_exchange_controls(window)
    _sync_final_button(window)


def _prepare_transaction_summary(window: object, root_text_callback: object) -> None:
    """Create exactly one durable prepared transaction and render its summary."""
    evidence = _completion_evidence(window)
    if evidence is None:
        _set_status(window, "Prepare Completion Evidence first.")
        return
    existing = _completion_transaction(window)
    if existing is not None:
        _refresh_human_review_gate(window)
        return
    snapshot = getattr(window, "_large_file_refactor_workbench_plan_snapshot", None)
    preflight = getattr(window, "_large_file_refactor_workbench_preflight_backup", None)
    payload = getattr(window, "_large_file_refactor_workbench_source_payload", None)
    if not all((snapshot, preflight, payload)):
        _set_status(window, "TRANSACTION PREPARATION BLOCKED\nRequired evidence is missing.")
        return
    try:
        proof = read_and_render_patch5_executor_proof_status(
            window,
            root_text_callback,
        )
        window._large_file_refactor_workbench_transaction_apply_executor_proven = bool(
            proof and proof.proof_available
        )
        bundle = prepare_completion_transaction(
            snapshot=snapshot,
            evidence=evidence,
            preflight=preflight,
            source_payload=payload,
            acknowledged_warning_codes=_acknowledged_warning_codes(window, evidence),
            semantic_review_confirmed=_checked(window, "_large_file_refactor_workbench_semantic_review_check"),
            transaction_summary_confirmed=False,
            tool_root=tool_source_root(),
            transaction_apply_executor_proven=bool(
                proof and proof.proof_available
            ),
        )
    except Exception as exc:
        _set_status(window, "TRANSACTION PREPARATION BLOCKED\n" + str(exc))
        return
    window._large_file_refactor_workbench_completion_transaction = bundle
    confirm = getattr(window, "_large_file_refactor_workbench_transaction_confirm_check", None)
    if confirm is not None:
        confirm.setEnabled(True)
    _render_transaction_bundle(window, bundle)
    _sync_final_button(window)


def _refresh_human_review_gate(window: object) -> None:
    """Recompute review evidence from checkboxes without creating a new transaction."""
    evidence = _completion_evidence(window)
    transaction = _completion_transaction(window)
    if evidence is None:
        return
    reviewed = _checked(window, "_large_file_refactor_workbench_semantic_review_check")
    warning_codes = _acknowledged_warning_codes(window, evidence)
    if transaction is None:
        review = format_semantic_diff_review(
            evidence.semantic_review.__class__(
                **{**evidence.semantic_review.__dict__, "reviewed": reviewed, "status": "semantic_diff_reviewed" if reviewed else "semantic_diff_ready"}
            )
        )
        window._large_file_refactor_workbench_semantic_diff_output.setPlainText(review)
        return
    snapshot = getattr(window, "_large_file_refactor_workbench_plan_snapshot", None)
    preflight = getattr(window, "_large_file_refactor_workbench_preflight_backup", None)
    payload = getattr(window, "_large_file_refactor_workbench_source_payload", None)
    updated = refresh_completion_review_state(
        snapshot=snapshot,
        evidence=evidence,
        transaction_bundle=transaction,
        preflight=preflight,
        source_payload=payload,
        semantic_review_confirmed=reviewed,
        acknowledged_warning_codes=warning_codes,
        transaction_summary_confirmed=_checked(window, "_large_file_refactor_workbench_transaction_confirm_check"),
        transaction_apply_executor_proven=bool(
            getattr(window, "_large_file_refactor_workbench_transaction_apply_executor_proven", False)
        ),
    )
    window._large_file_refactor_workbench_completion_transaction = updated
    _render_transaction_bundle(window, updated)
    _sync_final_button(window)


def _render_completion_evidence(window: object, bundle: CompletionEvidenceBundle) -> None:
    window._large_file_refactor_workbench_semantic_diff_output.setPlainText(
        format_semantic_diff_review(bundle.semantic_review)
    )
    window._large_file_refactor_workbench_text_diff_output.setPlainText(
        _format_text_diff(bundle.text_diff)
    )


def _render_transaction_bundle(window: object, bundle: CompletionTransactionBundle) -> None:
    window._large_file_refactor_workbench_transaction_summary_output.setPlainText(
        format_transaction_summary(bundle.transaction_summary)
    )
    window._large_file_refactor_workbench_refactor_gate_output.setPlainText(
        format_refactor_large_module_gate(bundle.gate)
    )

def _sync_final_button(window: object) -> None:
    if sync_completion_external_source_stale_state(window):
        return
    button = getattr(window, "_large_file_refactor_workbench_refactor_large_module_button", None)
    transaction = _completion_transaction(window)
    enabled = bool(transaction and transaction.gate.enabled)
    if button is not None:
        button.setEnabled(enabled)

def _refactor_large_module_clicked(window: object, root_text_callback: object) -> None:
    """Execute the exact reviewed Patch 5 transaction after canonical proof recheck."""
    if sync_completion_external_source_stale_state(window):
        return
    evidence = _completion_evidence(window)
    transaction = _completion_transaction(window)
    preflight = getattr(window, "_large_file_refactor_workbench_preflight_backup", None)
    payload = getattr(window, "_large_file_refactor_workbench_source_payload", None)
    if not all((evidence, transaction, preflight, payload)):
        QMessageBox.warning(None, "Refactor Large Module - blocked", "Completion transaction evidence is incomplete.")
        return
    proof = read_and_render_patch5_executor_proof_status(
        window,
        root_text_callback,
    )
    if proof is None or not proof.proof_available:
        QMessageBox.warning(
            None,
            "Refactor Large Module - blocked",
            "Canonical Patch 5 executor proof is not available.\n\n"
            + ("\n".join(proof.blockers) if proof is not None else "PROOF_LOOKUP_FAILED"),
        )
        return
    try:
        outcome = execute_completion_transaction(
            evidence=evidence,
            transaction_bundle=transaction,
            preflight=preflight,
            source_payload=payload,
            executor_proof_available=True,
            behavior_test_command="",
        )
    except Exception as exc:
        _set_status(window, "REFACTOR LARGE MODULE FAILED\n" + str(exc))
        QMessageBox.critical(None, "Refactor Large Module", str(exc))
        return
    window._large_file_refactor_workbench_completion_apply_outcome = outcome
    rendered_outcome = format_completion_apply_outcome(outcome)
    _set_status(window, rendered_outcome)
    if outcome.status == "completed":
        release_completed_architecture_review_card(window)
        _set_status(
            window,
            rendered_outcome
            + "\n\nCARD RELEASED: Tool GUI memory forgot this module; durable "
            "project source, Preview evidence, transaction receipt, and generated "
            "helper files remain project-owned.",
        )
    rollback_btn = getattr(window, "_large_file_refactor_workbench_transaction_rollback_button", None)
    if rollback_btn is not None:
        rollback_btn.setEnabled(outcome.final_transaction_state in {"RECOVERY_PENDING", "APPLIED_VALIDATION_FAILED"})
    _sync_final_button(window)


def _rollback_journaled_transaction_clicked(window: object) -> None:
    """Rollback current transaction only through Patch 5 journaled recovery ownership."""
    transaction = _completion_transaction(window)
    if transaction is None:
        _set_status(window, "ROLLBACK BLOCKED\nCompletion transaction is not prepared.")
        return
    try:
        result = rollback_completion_transaction(transaction)
        window._large_file_refactor_workbench_completion_rollback_result = result
    except Exception as exc:
        _set_status(window, "ROLLBACK FAILED\n" + str(exc))
        return
    lines = [
        "Journaled Transaction Rollback",
        "==============================",
        f"status: {result.status}",
        f"transaction_state: {result.transaction_state}",
        f"lane_state: {result.lane_state}",
        f"restored_files: {len(result.restored_files)}",
        f"removed_files: {len(result.removed_files)}",
    ]
    if result.blockers:
        lines.extend(["", "Blockers:", *[f"- {item}" for item in result.blockers]])
    _set_status(window, "\n".join(lines))
    rollback_btn = getattr(window, "_large_file_refactor_workbench_transaction_rollback_button", None)
    if rollback_btn is not None:
        rollback_btn.setEnabled(result.status == "rollback_conflict")
def _completion_evidence(window: object) -> CompletionEvidenceBundle | None:
    return getattr(window, "_large_file_refactor_workbench_completion_evidence", None)

def _completion_transaction(window: object) -> CompletionTransactionBundle | None:
    return getattr(window, "_large_file_refactor_workbench_completion_transaction", None)


def _checked(window: object, attribute: str) -> bool:
    widget = getattr(window, attribute, None)
    return bool(widget and widget.isChecked())


def _acknowledged_warning_codes(
    window: object,
    evidence: CompletionEvidenceBundle,
) -> tuple[str, ...]:
    acknowledged = _checked(window, "_large_file_refactor_workbench_warning_ack_check")
    return evidence.semantic_review.warnings if acknowledged else ()


def _set_status(window: object, text: str) -> None:
    output = getattr(window, "_large_file_refactor_workbench_completion_status_output", None)
    if output is not None:
        output.setPlainText(text)
    sync_workbench_stage_correction_controls_from_window(window)


def _format_text_diff(report: object) -> str:
    """Render bounded secondary text diff for the GUI without writing artifacts."""
    lines = [
        "Text Diff Review",
        "================",
        f"status: {getattr(report, 'status', 'unknown')}",
        f"file_count: {int(getattr(report, 'file_count', 1) or 0)}",
        "",
    ]
    summaries = list(getattr(report, "file_summaries", ()) or ())
    if summaries:
        lines.append("Files covered:")
        for item in summaries:
            lines.append(
                "- "
                + str(item.get("target_label", ""))
                + " status="
                + str(item.get("status", ""))
                + " created="
                + str(bool(item.get("created_file", False))).lower()
            )
        lines.append("")
    for row in getattr(report, "rows", ()):
        marker = {"add": "+", "remove": "-", "hunk": "@", "header": "#"}.get(row.kind, " ")
        old = "" if row.old_lineno is None else str(row.old_lineno)
        new = "" if row.new_lineno is None else str(row.new_lineno)
        lines.append(f"{marker} {old:>5} {new:>5} | {row.text}")
    warnings = getattr(report, "warnings", ())
    if warnings:
        lines.extend(["", "Warnings:"])
        lines.extend(f"- {item}" for item in warnings)
    return "\n".join(lines)
