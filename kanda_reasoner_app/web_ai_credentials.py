# project-path: kanda_reasoner_app/web_ai_credentials.py
"""Session-only credential resolution for KANDA web AI gateways."""

from __future__ import annotations

import os

__all__ = ["resolve_environment_key"]


def resolve_environment_key(name: str) -> tuple[str, str]:
    """Return one credential from process or Windows User environment.

    The current-process value always wins. On Windows, the User environment
    registry is a session-only fallback for GUI processes launched before an
    environment-variable update. The resolved value is copied only into the
    current process and is never written to disk by this helper.
    """
    clean_name = str(name or "").strip()
    if not clean_name:
        return "", ""

    value = os.environ.get(clean_name, "").strip()
    if value:
        return value, "current process"
    if os.name != "nt":
        return "", ""

    try:
        import winreg

        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as key:
            raw_value, _value_type = winreg.QueryValueEx(key, clean_name)
    except (FileNotFoundError, ImportError, OSError):
        return "", ""

    value = str(raw_value or "").strip()
    if not value:
        return "", ""
    os.environ[clean_name] = value
    return value, "Windows User environment"
