"""Path helpers for the package-owned Prompt Library assets."""

from __future__ import annotations

from pathlib import Path

__all__ = [
    "package_root",
    "prompt_library_root",
    "prompt_template_root",
]


def package_root() -> Path:
    """Return the current product package root directory."""
    return Path(__file__).resolve().parents[1]


def prompt_library_root() -> Path:
    """Return the package-owned prompt_library directory."""
    return package_root() / "prompt_library"


def prompt_template_root() -> Path:
    """Return the package-owned prompt template library directory."""
    return package_root() / "templates" / "prompt_library_templates"
