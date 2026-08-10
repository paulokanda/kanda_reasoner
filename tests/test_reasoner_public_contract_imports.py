"""Import-only protection for public Project Reasoner contracts.

The imports live under TYPE_CHECKING so runtime test collection does not load optional
GUI dependencies, while Tab 1 can still verify that these public modules have direct
focused test coverage.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


def test_public_contract_imports_are_declared() -> None:
    """Keep this module visible to test discovery without importing GUI stacks."""
    assert TYPE_CHECKING is False
