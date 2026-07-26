# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/human_confirmed_import_rewrite_contract_formatting.py
"""Formatting helpers for human-confirmed import rewrite contract evidence."""
from __future__ import annotations

from .human_confirmed_import_rewrite_contract import HumanConfirmedImportRewriteContractResult

__all__ = ["format_human_confirmed_import_rewrite_contract"]


def format_human_confirmed_import_rewrite_contract(
    contract: HumanConfirmedImportRewriteContractResult,
) -> str:
    """Return a review-only human import rewrite contract report."""
    lines = [
        "HUMAN-CONFIRMED IMPORT REWRITE CONTRACT",
        "Status: " + contract.status,
        "Target: " + contract.target_file,
        "Preview root: " + contract.preview_root,
        "Human confirmation valid: " + str(contract.human_confirmation_valid),
        "rewrite_enabled: " + str(contract.rewrite_enabled),
        "apply_enabled: " + str(contract.apply_enabled),
        "Manifest: " + contract.human_contract_manifest_path,
    ]
    if contract.blockers:
        lines.append("Blockers:")
        lines.extend("- " + blocker for blocker in contract.blockers)
    if contract.warnings:
        lines.append("Warnings:")
        lines.extend("- " + warning for warning in contract.warnings)
    return "\n".join(lines)
