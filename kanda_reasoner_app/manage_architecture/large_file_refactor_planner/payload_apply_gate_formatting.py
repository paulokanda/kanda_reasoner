# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/payload_apply_gate_formatting.py
"""Formatting helpers for payload apply gate evidence."""
from __future__ import annotations

from .payload_apply_gate import PayloadApplyGateResult

__all__ = ["format_payload_apply_gate_result"]


def format_payload_apply_gate_result(result: PayloadApplyGateResult) -> str:
    """Return a compact review-only apply gate report."""
    lines = [
        "Payload Apply Gate",
        "==================",
        f"Status: {result.status}",
        f"Apply enabled: {result.apply_enabled}",
        f"Human confirmation present: {result.human_confirmation_present}",
        f"Source hash verified: {result.source_hash_verified}",
        f"Payload ZIP: {result.payload_zip_path}",
        f"Apply gate manifest: {result.apply_gate_manifest_path}",
        "Blockers: " + (", ".join(result.blockers) if result.blockers else "none"),
        "Warnings: " + (", ".join(result.warnings) if result.warnings else "none"),
    ]
    return "\n".join(lines)
