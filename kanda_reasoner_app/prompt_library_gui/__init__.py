"""Read-only GUI components for the Prompt Engineering Library.

The package facade avoids importing PySide6 until GUI classes are explicitly
requested, allowing headless catalog tests to run in environments without Qt.
"""

from __future__ import annotations

from .group_catalog import PromptGroup, load_prompt_groups

__all__ = [
    "PromptGroup",
    "PromptLibraryTab",
    "load_prompt_groups",
]


def __getattr__(name: str) -> object:
    """Lazily expose GUI classes that require PySide6."""
    if name == "PromptLibraryTab":
        from .prompt_library_tab import PromptLibraryTab

        return PromptLibraryTab
    raise AttributeError(name)
