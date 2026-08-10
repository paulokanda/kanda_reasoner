"""Disposable state and environment for packaged-GUI Portable smoke tests."""

from __future__ import annotations

import hashlib
import json
import os
import secrets
import shutil
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator

from portable.errors import PortableBuildError
from portable.models import BuildPaths

__all__ = [
    "PreparedSmokeIsolation",
    "verify_isolated_registry",
    "prepared_smoke_isolation",
]

ENABLED_ENV = "KANDA_PORTABLE_SMOKE_ISOLATION_ENABLED"
ROOT_ENV = "KANDA_PORTABLE_SMOKE_ISOLATION_ROOT"
TOKEN_ENV = "KANDA_PORTABLE_SMOKE_ISOLATION_TOKEN"
PROJECT_ENV = "KANDA_REASONER_PROJECT_ROOT"
MARKER_NAME = "KANDA_PORTABLE_SMOKE_ISOLATION.json"

_SCRUB_PREFIXES = (
    "KANDA_",
    "PROJECT_REASONER_",
)
_SCRUB_NAMES = {
    "OPENAI_API_KEY",
    "ANTHROPIC_API_KEY",
    "GOOGLE_API_KEY",
    "GEMINI_API_KEY",
    "AZURE_OPENAI_API_KEY",
}


@dataclass(frozen=True)
class PreparedSmokeIsolation:
    """One disposable packaged-GUI runtime and its explicit environment."""

    root: Path
    extract_root: Path
    app_root: Path
    project_root: Path
    tool_support_root: Path
    project_support_root: Path
    project_transient_root: Path
    marker_path: Path
    environment: dict[str, str]


def _write_json(path: Path, payload: dict[str, object]) -> None:
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    json.loads(path.read_text(encoding="utf-8"))


def _inside(candidate: Path, root: Path) -> bool:
    try:
        candidate.resolve(strict=False).relative_to(root.resolve(strict=False))
    except ValueError:
        return False
    return True


def _isolated_environment(
    root: Path,
    project_root: Path,
    token: str,
) -> dict[str, str]:
    environment = {
        key: value
        for key, value in os.environ.items()
        if key not in _SCRUB_NAMES
        and not any(key.startswith(prefix) for prefix in _SCRUB_PREFIXES)
    }
    profile = root / "profile"
    appdata = profile / "AppData" / "Roaming"
    localappdata = profile / "AppData" / "Local"
    temp = root / "temp"
    cache = root / "cache"
    for directory in (profile, appdata, localappdata, temp, cache):
        directory.mkdir(parents=True, exist_ok=True)

    environment.update(
        {
            ENABLED_ENV: "1",
            ROOT_ENV: str(root),
            TOKEN_ENV: token,
            PROJECT_ENV: str(project_root),
            "APPDATA": str(appdata),
            "LOCALAPPDATA": str(localappdata),
            "USERPROFILE": str(profile),
            "HOME": str(profile),
            "TEMP": str(temp),
            "TMP": str(temp),
            "XDG_CONFIG_HOME": str(profile / "xdg_config"),
            "XDG_DATA_HOME": str(profile / "xdg_data"),
            "XDG_CACHE_HOME": str(cache),
            "PYTHONDONTWRITEBYTECODE": "1",
            "PYTHONPYCACHEPREFIX": str(cache / "pycache"),
        }
    )
    return environment


def _assert_paths(isolation: PreparedSmokeIsolation) -> None:
    governed = (
        isolation.extract_root,
        isolation.app_root,
        isolation.project_root,
        isolation.tool_support_root,
        isolation.project_support_root,
        isolation.project_transient_root,
        isolation.marker_path,
    )
    for path in governed:
        if not _inside(path, isolation.root):
            raise PortableBuildError(
                "Smoke-isolation path escaped the disposable root: " + str(path)
            )


def verify_isolated_registry(isolation: PreparedSmokeIsolation) -> None:
    """Require the packaged GUI to persist only the disposable Project selection."""
    registry = (
        isolation.tool_support_root
        / "tool_project_registry"
        / "projects.json"
    )
    if not registry.is_file():
        raise PortableBuildError(
            "Packaged GUI did not create the isolated Tool registry."
        )
    try:
        payload = json.loads(registry.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise PortableBuildError(
            "Isolated Tool registry is unreadable."
        ) from exc
    current_id = str(payload.get("current_project_id") or "")
    projects = payload.get("projects")
    if not current_id or not isinstance(projects, dict):
        raise PortableBuildError(
            "Isolated Tool registry has no active disposable Project."
        )
    record = projects.get(current_id)
    if not isinstance(record, dict):
        raise PortableBuildError(
            "Isolated Tool registry active record is missing."
        )
    actual_project = Path(str(record.get("project_root") or "")).resolve(strict=False)
    actual_support = Path(str(record.get("project_support_root") or "")).resolve(strict=False)
    if actual_project != isolation.project_root.resolve(strict=False):
        raise PortableBuildError(
            "Packaged GUI selected a non-disposable Project during smoke."
        )
    if actual_support != isolation.project_support_root.resolve(strict=False):
        raise PortableBuildError(
            "Packaged GUI selected non-isolated Project Support during smoke."
        )
    print("PORTABLE SMOKE ISOLATED TOOL REGISTRY: PASS")
    print("PORTABLE SMOKE DISPOSABLE PROJECT SELECTION: PASS")


@contextmanager
def prepared_smoke_isolation(
    paths: BuildPaths,
    top_level_name: str,
) -> Iterator[PreparedSmokeIsolation]:
    """Create and destroy one token-bound disposable smoke environment."""
    root = paths.run_root / "packaged_gui_smoke_isolation"
    if root.exists():
        shutil.rmtree(root)
    root.mkdir(parents=True)
    extract_root = root / "clean_extract"
    app_root = extract_root / top_level_name
    project_root = root / "projects" / "smoke_project"
    project_root.mkdir(parents=True)

    token = secrets.token_urlsafe(32)
    tool_support_root = root / "tool_support" / f"{top_level_name}_show_project_to_AI"
    project_support_root = root / "project_support" / "smoke_project_show_project_to_AI"
    project_transient_root = root / "transient" / "smoke_project_delete_after_daily_work"
    marker_path = root / MARKER_NAME
    _write_json(
        marker_path,
        {
            "schema_version": "1.0",
            "root": str(root.resolve(strict=False)),
            "runtime_root": str(app_root.resolve(strict=False)),
            "project_root": str(project_root.resolve(strict=False)),
            "token_sha256": hashlib.sha256(token.encode("utf-8")).hexdigest(),
        },
    )
    isolation = PreparedSmokeIsolation(
        root=root.resolve(strict=False),
        extract_root=extract_root.resolve(strict=False),
        app_root=app_root.resolve(strict=False),
        project_root=project_root.resolve(strict=False),
        tool_support_root=tool_support_root.resolve(strict=False),
        project_support_root=project_support_root.resolve(strict=False),
        project_transient_root=project_transient_root.resolve(strict=False),
        marker_path=marker_path.resolve(strict=False),
        environment=_isolated_environment(root, project_root, token),
    )
    _assert_paths(isolation)
    print("PORTABLE SMOKE DISPOSABLE ROOT: PASS")
    print("PORTABLE SMOKE CREDENTIAL ENVIRONMENT SCRUB: PASS")
    print("PORTABLE SMOKE PROFILE AND TEMP ISOLATION: PASS")
    try:
        yield isolation
    finally:
        shutil.rmtree(root, ignore_errors=True)
