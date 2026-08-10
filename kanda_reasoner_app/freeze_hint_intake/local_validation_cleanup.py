"""Public cleanup contract for completed local Freeze validation evidence."""

from __future__ import annotations

from typing import Any, Mapping

from .form_text_validation import (
    _clean_stale_pending_text_after_local_validation,
)

__all__ = ["clean_stale_pending_text_after_local_validation"]


def clean_stale_pending_text_after_local_validation(
    inputs: Mapping[str, Any],
) -> dict[str, str]:
    """Return normalized form inputs after completed local validation."""
    return _clean_stale_pending_text_after_local_validation(inputs)
