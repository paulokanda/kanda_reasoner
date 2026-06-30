# project-path: kanda_reasoner_app/insert_missing_docstrings_gui/gui_scope_helpers.py
"""Support missing-docstring insertion workflows."""

from __future__ import annotations

from pathlib import Path


SCOPE_FULL = "Full project"
SCOPE_PACKAGE = "Package/folder"
SCOPE_MODULE = "Module/file"


def is_blank_scope_target(value: str) -> bool:
    """Return whether blank scope target.
    
    Parameters
    ----------
    value : str
        The input value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    stripped = value.strip()
    return not stripped or stripped == "*"


def is_test_like_scope_target(value: str) -> bool:
    """Return whether test like scope target.
    
    Parameters
    ----------
    value : str
        The input value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    lowered = value.strip().replace("\\", "/").lower()
    if not lowered:
        return False
    if lowered == "tests" or lowered.startswith("tests/"):
        return True
    if lowered == "test" or lowered.startswith("test/"):
        return True
    if lowered.endswith("/tests") or "/tests/" in lowered:
        return True
    name = Path(lowered).name
    if name == "conftest.py":
        return True
    if name.startswith("test_") and name.endswith(".py"):
        return True
    if name.endswith("_test.py"):
        return True
    return False
