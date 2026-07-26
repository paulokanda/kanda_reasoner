# project-path: tools/project_structure_3d_test_environment.py
"""Shared isolated Project Support fixtures for Project Structure 3D tests."""

from __future__ import annotations

import os
import shutil
import tempfile
import uuid
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

from kanda_reasoner_app.project_analysis_evidence_paths import (
    show_project_to_ai_root_from_hint,
)

__all__ = [
    "environment_snapshot",
    "isolated_project_fixture",
    "isolated_show_project_environment",
]

_SHOW_PROJECT_ENV_KEYS = (
    "KANDA_SHOW_PROJECT_TO_AI_JSON_COMPLETE_DIR",
    "KANDA_SHOW_PROJECT_TO_AI_PROJECT_ROOT",
)


def environment_snapshot() -> dict[str, str | None]:
    """Return exact ambient show-project override values."""
    return {key: os.environ.get(key) for key in _SHOW_PROJECT_ENV_KEYS}


@contextmanager
def isolated_show_project_environment() -> Iterator[None]:
    """Remove ambient output overrides and restore them exactly afterward."""
    previous = environment_snapshot()
    try:
        for key in _SHOW_PROJECT_ENV_KEYS:
            os.environ.pop(key, None)
        yield
    finally:
        for key, value in previous.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value


@contextmanager
def isolated_project_fixture(prefix: str) -> Iterator[tuple[Path, Path]]:
    """Create one unique project and clean its external Project Support root."""
    unique_name = prefix.rstrip("_") + "_" + uuid.uuid4().hex
    with tempfile.TemporaryDirectory(prefix=prefix) as folder:
        project_root = Path(folder) / unique_name
        project_root.mkdir()
        support_root = show_project_to_ai_root_from_hint(project_root)
        expected_prefix = unique_name.casefold() + "_show_project_to_ai"
        if not support_root.name.casefold().startswith(expected_prefix):
            raise AssertionError("unexpected fixture support root: " + str(support_root))
        if support_root.exists():
            shutil.rmtree(support_root)
        try:
            yield project_root, support_root
        finally:
            if support_root.exists():
                shutil.rmtree(support_root)
