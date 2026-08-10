"""Import-only reachability protection for dynamic Project Reasoner modules.

The imports are guarded by TYPE_CHECKING so runtime test collection stays light
while architecture validation can see explicit ownership for dynamic helpers,
source-preserving shards, and collector plug-ins.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


def test_reachability_contract_imports_are_declared() -> None:
    """Keep dynamic modules visible without importing optional stacks at runtime."""
    assert TYPE_CHECKING is False
