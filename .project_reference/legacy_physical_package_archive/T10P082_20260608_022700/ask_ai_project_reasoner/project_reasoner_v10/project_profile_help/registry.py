"""Support V10 project reasoning and evidence handling."""

from __future__ import annotations

from .built_in_profiles import (
    ARCHITECTURE_HEAVY_PYTHON_PROJECT_PROFILE,
    EEG_PROJECT_PROFILE,
    GENERIC_PROJECT_PROFILE,
    GENERIC_PYTHON_PROJECT_PROFILE,
    QT_PYTHON_PROJECT_PROFILE,
)
from .profile_types import ProjectProfile


PROJECT_PROFILES: dict[str, ProjectProfile] = {
    GENERIC_PROJECT_PROFILE.name: GENERIC_PROJECT_PROFILE,
    GENERIC_PYTHON_PROJECT_PROFILE.name: GENERIC_PYTHON_PROJECT_PROFILE,
    ARCHITECTURE_HEAVY_PYTHON_PROJECT_PROFILE.name: ARCHITECTURE_HEAVY_PYTHON_PROJECT_PROFILE,
    QT_PYTHON_PROJECT_PROFILE.name: QT_PYTHON_PROJECT_PROFILE,
    EEG_PROJECT_PROFILE.name: EEG_PROJECT_PROFILE,
}


def get_project_profile(name: str | None) -> ProjectProfile:
    normalized = str(name or "").strip().lower()
    if not normalized:
        return GENERIC_PROJECT_PROFILE

    for profile_name, profile in PROJECT_PROFILES.items():
        if profile_name.lower() == normalized:
            return profile

    return GENERIC_PROJECT_PROFILE


def iter_project_profiles() -> tuple[ProjectProfile, ...]:
    return tuple(PROJECT_PROFILES.values())


__all__ = [
    "PROJECT_PROFILES",
    "get_project_profile",
    "iter_project_profiles",
]
