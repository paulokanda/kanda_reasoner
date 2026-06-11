"""Parse-only contract anchors for residual Project Reasoner warnings."""

from __future__ import annotations

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    pass


def test_remaining_warning_contract_anchor_file_compiles() -> None:
    """Keep this file executable without importing GUI/runtime modules."""
    assert TYPE_CHECKING is False
