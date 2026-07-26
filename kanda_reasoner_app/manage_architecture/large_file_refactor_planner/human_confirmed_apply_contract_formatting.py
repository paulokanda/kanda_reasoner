# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/human_confirmed_apply_contract_formatting.py
"""Formatting helpers for human-confirmed payload apply contract evidence."""
from __future__ import annotations

from .human_confirmed_apply_contract import HumanConfirmedApplyContractResult

__all__ = ["format_human_confirmed_apply_contract"]


def format_human_confirmed_apply_contract(contract: HumanConfirmedApplyContractResult) -> str:
    """Return a review-only human apply contract report."""
    lines = [
        "HUMAN-CONFIRMED APPLY CONTRACT",
        "Status: " + contract.status,
        "Target: " + contract.target_file,
        "Payload ZIP: " + contract.payload_zip_path,
        "Preview root: " + contract.preview_root,
        "Human confirmation valid: " + str(contract.human_confirmation_valid),
        "rewrite_enabled: " + str(contract.rewrite_enabled),
        "apply_enabled: " + str(contract.apply_enabled),
        "Manifest: " + contract.human_apply_contract_manifest_path,
    ]
    if contract.blockers:
        lines.append("Blockers:")
        lines.extend("- " + blocker for blocker in contract.blockers)
    if contract.warnings:
        lines.append("Warnings:")
        lines.extend("- " + warning for warning in contract.warnings)
    return "\n".join(lines)
