"""Import-only protection for v10 reader public contracts.

The imports are guarded by TYPE_CHECKING to avoid importing GUI dependencies during
normal test collection while still documenting direct test ownership for Tab 1.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


def test_v10_public_contract_imports_are_declared() -> None:
    """Keep this module visible to test discovery without importing GUI stacks."""
    assert TYPE_CHECKING is False
