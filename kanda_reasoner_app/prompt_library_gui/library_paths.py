# project-path: kanda_reasoner_app/prompt_library_gui/library_paths.py
"""Path helpers for canonical and legacy Prompt Library assets."""

from __future__ import annotations

from pathlib import Path

__all__ = [
    "canonical_prompt_library_root",
    "legacy_prompt_library_root",
    "package_root",
    "prompt_library_root",
    "prompt_template_root",
    "tool_root",
]


def package_root() -> Path:
    """Return the current product package root directory."""
    return Path(__file__).resolve().parents[1]


def tool_root() -> Path:
    """Return the KANDA Tool root that owns the Prompt Library workspace."""
    return package_root().parent


def canonical_prompt_library_root() -> Path:
    """Return the governed workspace Prompt Library source root."""
    return tool_root() / "kanda_prompt_workspace" / "prompt_library"


def legacy_prompt_library_root() -> Path:
    """Return the package-owned compatibility Prompt Library root."""
    return package_root() / "prompt_library"


def prompt_library_root() -> Path:
    """Return canonical Prompt Library source, with a legacy fallback."""
    canonical_root = canonical_prompt_library_root()
    if (canonical_root / "ACTIVE_PROMPTS").is_dir():
        return canonical_root
    return legacy_prompt_library_root()


def prompt_template_root() -> Path:
    """Return the package-owned prompt template library directory."""
    return package_root() / "templates" / "prompt_library_templates"
