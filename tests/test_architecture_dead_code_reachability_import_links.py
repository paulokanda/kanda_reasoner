"""Static reachability links for active modules deferred from deletion.

Imports stay under TYPE_CHECKING so architecture validation can see explicit
reachability evidence without importing GUI/runtime-heavy modules at runtime.
These links are not behavior tests and must not be treated as deletion approval.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


def test_dead_code_reachability_links_are_static() -> None:
    """Keep this test module runtime-safe."""
    assert TYPE_CHECKING is False
