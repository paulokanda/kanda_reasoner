# project-path: kanda_reasoner_app/source_hygiene/ruff_correction_errors.py
"""Typed errors for Ruff correction preview and apply workflows."""

from __future__ import annotations

__all__ = ["RuffCorrectionApplyError", "RuffCorrectionPreviewError"]


class RuffCorrectionPreviewError(RuntimeError):
    """Raised when a correction preview cannot be created safely."""


class RuffCorrectionApplyError(RuntimeError):
    """Raised when an apply transaction is blocked or rolled back."""
