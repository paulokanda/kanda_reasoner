"""Direct import tests for root public entry-point contracts."""

from __future__ import annotations

import _inject_missing_module_docstrings as _docstring_injector
import reasoner_tools_gui as _reasoner_tools_gui


def test_inject_missing_module_docstrings_public_contract() -> None:
    """Confirm the maintenance entry script keeps its public contract."""
    assert callable(_docstring_injector.build_docstring)
    assert callable(_docstring_injector.main)


def test_reasoner_tools_gui_public_contract() -> None:
    """Confirm the root GUI launcher facade keeps its public contract."""
    assert callable(_reasoner_tools_gui.main)
