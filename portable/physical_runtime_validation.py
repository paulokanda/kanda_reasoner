"""Focused fixture support for committed physical runtime allowlisting."""

from __future__ import annotations

import shutil
from pathlib import Path

from portable.physical_runtime import (
    REQUIRED_RUNTIME_ROLES,
    RUNTIME_MANIFEST_RELATIVE,
    load_runtime_allowlist,
    validate_physical_runtime,
)


def populate_fixture_project(
    project_root: Path,
    *,
    reference_project_root: Path | None = None,
) -> None:
    """Copy the committed allowlisted source set into a fixture project."""

    reference = (
        reference_project_root.resolve()
        if reference_project_root is not None
        else Path(__file__).resolve().parents[1]
    )
    project_root.mkdir(parents=True, exist_ok=True)
    payload = load_runtime_allowlist()
    for item in payload["items"]:
        relative = Path(str(item["source_relative"]))
        source = reference / relative
        if not source.is_file():
            raise RuntimeError(
                f"Fixture reference runtime source is missing: {relative.as_posix()}"
            )
        destination = project_root / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)


def assert_fixture_stage(stage_app: Path) -> None:
    """Require a complete exact allowlist-backed runtime fixture manifest."""

    payload = validate_physical_runtime(stage_app)
    roles = {
        str(item.get("role", ""))
        for item in payload.get("items", [])
        if isinstance(item, dict)
    }
    if roles != set(REQUIRED_RUNTIME_ROLES):
        raise RuntimeError(
            f"Physical runtime fixture roles mismatch: {sorted(roles)}"
        )
    if not (stage_app / RUNTIME_MANIFEST_RELATIVE).is_file():
        raise RuntimeError("Physical runtime fixture manifest is missing.")
