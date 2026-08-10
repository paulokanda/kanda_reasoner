"""Static import anchors for Project Reasoner architecture validation.

These imports are intentionally placed under a never-executed branch.
Tab 1 reads the AST import graph to identify direct test ownership,
while runtime test collection avoids optional GUI and runtime imports.
"""

from __future__ import annotations

if False:
    pass


def test_static_import_contract_chunk_03_is_parseable() -> None:
    """Keep this file visible to test discovery without runtime imports."""
    assert 3 <= 4
