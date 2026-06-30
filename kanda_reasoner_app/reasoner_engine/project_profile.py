# project-path: kanda_reasoner_app/reasoner_engine/project_profile.py
"""
Project profile public API.

This module keeps the public project-profile contract stable while the
implementation lives in project_profile_help/.
"""

from __future__ import annotations

from .project_profile_help import (
    ARCHITECTURE_HEAVY_PYTHON_PROJECT_PROFILE,
    EEG_PROJECT_PROFILE,
    GENERIC_PROJECT_PROFILE,
    GENERIC_PYTHON_PROJECT_PROFILE,
    PROJECT_PROFILES,
    QT_PYTHON_PROJECT_PROFILE,
    ProjectProfile,
    get_project_profile,
    infer_project_profile,
    infer_project_profile_name_from_metadata,
    iter_project_profiles,
)

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
