# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_patch5_proof_status_gui.py
"""Read-only GUI projection for canonical Patch 5 executor proof status."""
from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from typing import Any

from .workbench_patch5_executor_proof import (
    ExecutorProofEvidence,
    find_patch5_executor_proof,
)

__all__ = [
    "format_patch5_executor_proof_status",
    "read_and_render_patch5_executor_proof_status",
    "render_patch5_executor_proof_status",
]

_STATUS_TITLE = "PATCH 5 EXECUTOR PROOF STATUS"


def format_patch5_executor_proof_status(
    proof: ExecutorProofEvidence | None,
    *,
    diagnostic: str = "",
) -> str:
    """Format current canonical Patch 5 proof state without mutating evidence."""
    if proof is None:
        lines = [
            _STATUS_TITLE,
            "",
            "Status: NOT_CHECKED",
            "Proof available: NO",
            "",
            "Gate effect: executor-proof prerequisite remains fail-closed.",
        ]
        if diagnostic:
            lines.extend(["", "Diagnostic:", f"- {diagnostic}"])
        return "\n".join(lines)

    status = "AVAILABLE" if proof.proof_available else "UNAVAILABLE"
    lines = [
        _STATUS_TITLE,
        "",
        f"Status: {status}",
        f"Proof available: {'YES' if proof.proof_available else 'NO'}",
        f"Feature ID: {proof.feature_id}",
        f"Project root: {proof.project_root}",
        f"Freeze memory root: {proof.freeze_memory_root}",
    ]
    if proof.matched_entry:
        lines.extend(
            [
                "",
                "Canonical frozen entry:",
                f"- {proof.matched_entry}",
            ]
        )
    if proof.blockers:
        lines.extend(["", "Blockers:", *[f"- {item}" for item in proof.blockers]])
    lines.extend(
        [
            "",
            "Gate effect:",
            "- This status satisfies only the canonical executor-proof prerequisite.",
            "- Immutable evidence, human review, warning acknowledgment, transaction",
            "  summary confirmation, source freshness, and transaction safety gates",
            "  remain independent and fail-closed.",
        ]
    )
    return "\n".join(lines)


def render_patch5_executor_proof_status(
    window: object,
    proof: ExecutorProofEvidence | None,
    *,
    diagnostic: str = "",
) -> None:
    """Render proof status into the existing read-only Stage 7 output widget."""
    output = getattr(
        window,
        "_large_file_refactor_workbench_refactor_gate_output",
        None,
    )
    if output is None:
        return
    output.setPlainText(
        format_patch5_executor_proof_status(proof, diagnostic=diagnostic)
    )


def read_and_render_patch5_executor_proof_status(
    window: object,
    root_text_callback: Callable[[object], Any],
) -> ExecutorProofEvidence | None:
    """Read canonical frozen memory and render current executor-proof availability."""
    try:
        root_text = str(root_text_callback(window)).strip()
    except Exception as exc:  # pragma: no cover - defensive GUI boundary
        render_patch5_executor_proof_status(
            window,
            None,
            diagnostic=f"project root callback failed: {exc}",
        )
        return None
    if not root_text:
        render_patch5_executor_proof_status(
            window,
            None,
            diagnostic="active project root is empty",
        )
        return None
    try:
        root = Path(root_text).resolve()
        proof = find_patch5_executor_proof(root)
    except (OSError, ValueError) as exc:
        render_patch5_executor_proof_status(
            window,
            None,
            diagnostic=f"proof lookup failed: {exc}",
        )
        return None
    render_patch5_executor_proof_status(window, proof)
    return proof


def _projection_contract_notes() -> tuple[str, ...]:
    """Return stable notes used by focused validators and architecture reviews."""
    return (
        "projection_is_read_only",
        "canonical_freeze_memory_is_source_of_proof",
        "not_checked_and_unavailable_remain_fail_closed",
        "available_does_not_bypass_human_or_transaction_gates",
        "stage7_page_code_reflects_current_proof_status",
    )
