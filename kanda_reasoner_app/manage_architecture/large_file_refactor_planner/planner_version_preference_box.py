# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/planner_version_preference_box.py
"""Isolated persistence box for the Planner's last manually selected route.

This module has one responsibility: persist and restore one stable route ID.
It never receives the Architecture window, never caches settings on a shared
host, and never imports Workbench, AQR, Freeze, Project Support, or source-apply
code. The box deliberately exposes only bounded route-preference operations.
"""

from __future__ import annotations

from typing import Any, Callable

def _load_qsettings_type() -> object | None:
    """Return QSettings without rebinding an imported module symbol."""
    try:
        from PySide6.QtCore import QSettings as qsettings_type
    except ImportError:  # Headless validators may import Planner state without Qt.
        return None
    return qsettings_type


_QSETTINGS_TYPE = _load_qsettings_type()

__all__ = [
    "PLANNER_ROUTE_HEURISTIC",
    "PLANNER_ROUTE_LOCAL_AI",
    "PLANNER_ROUTE_WEB_AI",
    "PLANNER_ROUTE_PREFERENCE_KEY",
    "load_last_used_planner_route",
    "remember_last_used_planner_route",
]

PLANNER_ROUTE_HEURISTIC = "heuristic"
PLANNER_ROUTE_LOCAL_AI = "local_ai"
PLANNER_ROUTE_WEB_AI = "web_ai"
PLANNER_ROUTE_PREFERENCE_KEY = (
    "large_file_refactor_planner/version_preference_box/last_used_route_v1"
)

_SETTINGS_ORGANIZATION = "Kanda"
_SETTINGS_APPLICATION = "ProjectReasonerV10"
_LEGACY_PREFERENCE_KEY = "large_file_refactor_planner/selected_version"
_ALLOWED_ROUTES = frozenset(
    {
        PLANNER_ROUTE_HEURISTIC,
        PLANNER_ROUTE_LOCAL_AI,
        PLANNER_ROUTE_WEB_AI,
    }
)
_SettingsFactory = Callable[[], object]


def load_last_used_planner_route(
    *,
    settings_factory: _SettingsFactory | None = None,
) -> str:
    """Return the last valid manually selected route from isolated storage.

    The new box key is authoritative. A valid legacy value is migrated once so
    existing user preference survives this ownership correction. Missing,
    unreadable, or invalid values fail safely to Local AI.
    """

    settings = _open_settings(settings_factory)
    if settings is None:
        return PLANNER_ROUTE_LOCAL_AI

    current = _read_text(settings, PLANNER_ROUTE_PREFERENCE_KEY)
    if _is_known_route(current):
        return current

    legacy = _read_text(settings, _LEGACY_PREFERENCE_KEY)
    if _is_known_route(legacy):
        _write_route(settings, legacy)
        return legacy

    return PLANNER_ROUTE_LOCAL_AI


def remember_last_used_planner_route(
    route_id: str,
    *,
    settings_factory: _SettingsFactory | None = None,
) -> bool:
    """Persist one valid route ID and synchronously flush the settings endpoint."""

    normalized = str(route_id or "").strip()
    if not _is_known_route(normalized):
        raise ValueError("Unknown Planner route: " + normalized)

    settings = _open_settings(settings_factory)
    if settings is None:
        return False
    return _write_route(settings, normalized)


def _open_settings(
    settings_factory: _SettingsFactory | None,
) -> object | None:
    """Open one short-lived endpoint without attaching it to another box owner."""

    factory = settings_factory or _default_settings_factory
    try:
        settings = factory()
    except Exception:
        return None
    return settings


def _default_settings_factory() -> object:
    """Create the dedicated QSettings endpoint for this bounded preference box."""

    if _QSETTINGS_TYPE is None:
        raise RuntimeError("PySide6 QSettings is unavailable")
    return _QSETTINGS_TYPE(_SETTINGS_ORGANIZATION, _SETTINGS_APPLICATION)


def _read_text(settings: object, key: str) -> str:
    """Read one setting as stripped text and fail closed on endpoint errors."""

    try:
        value_method = settings.value
        value = value_method(key, "")
    except Exception:
        return ""
    return str(value or "").strip()


def _write_route(settings: object, route_id: str) -> bool:
    """Write exactly one route preference and require a synchronous flush."""

    try:
        settings.setValue(PLANNER_ROUTE_PREFERENCE_KEY, route_id)
        settings.sync()
    except Exception:
        return False
    return True


def _is_known_route(value: str) -> bool:
    """Return whether text is one of the three stable Planner route IDs."""

    return value in _ALLOWED_ROUTES


def _preference_box_contract() -> dict[str, Any]:
    """Return bounded diagnostic metadata without exposing a mutable endpoint."""

    return {
        "box": "planner_version_preference_box",
        "owner": "large_file_refactor_planner",
        "stored_value_kind": "stable_route_id_only",
        "allowed_routes": tuple(sorted(_ALLOWED_ROUTES)),
        "key": PLANNER_ROUTE_PREFERENCE_KEY,
        "legacy_read_migration": _LEGACY_PREFERENCE_KEY,
        "shared_host_cache": False,
        "workbench_access": False,
        "aqr_access": False,
        "freeze_access": False,
        "project_support_write": False,
    }
