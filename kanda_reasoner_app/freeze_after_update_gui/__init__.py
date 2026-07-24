# project-path: kanda_reasoner_app/freeze_after_update_gui/__init__.py
"""GUI exports for the Freeze Feature After Update tab."""

from __future__ import annotations

from typing import Any

__all__ = ["FreezeAfterUpdateTab"]


def __getattr__(name: str) -> Any:
    """Load the Qt tab only when a GUI consumer requests it."""
    if name == "FreezeAfterUpdateTab":
        from .freeze_after_update_tab import FreezeAfterUpdateTab

        return FreezeAfterUpdateTab
    raise AttributeError(name)
