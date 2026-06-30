# project-path: kanda_reasoner_app/reasoner_engine/project_profile_help/__init__.py
"""
Helper package for project profile definitions and inference.
"""

from __future__ import annotations

from .built_in_profiles import (
    ARCHITECTURE_HEAVY_PYTHON_PROJECT_PROFILE,
    EEG_PROJECT_PROFILE,
    GENERIC_PROJECT_PROFILE,
    GENERIC_PYTHON_PROJECT_PROFILE,
    QT_PYTHON_PROJECT_PROFILE,
)
from .inference import (
    infer_project_profile,
    infer_project_profile_name_from_metadata,
)
from .profile_types import ProjectProfile
from .registry import PROJECT_PROFILES, get_project_profile, iter_project_profiles

__all__ = [
    "ProjectProfile",
    "GENERIC_PROJECT_PROFILE",
    "GENERIC_PYTHON_PROJECT_PROFILE",
    "ARCHITECTURE_HEAVY_PYTHON_PROJECT_PROFILE",
    "QT_PYTHON_PROJECT_PROFILE",
    "EEG_PROJECT_PROFILE",
    "PROJECT_PROFILES",
    "get_project_profile",
    "iter_project_profiles",
    "infer_project_profile_name_from_metadata",
    "infer_project_profile",
]
