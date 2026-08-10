"""Tool-owned registry authority for Portable direct-write boundaries."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path
from typing import Any

from portable.errors import PortableBuildError
from portable.models import ProtectedRoot, RegistryBoundary


__all__ = [
    "EXPLICIT_SELF_HOSTING",
    "load_registry_boundary",
    "assert_registry_unchanged",
    "assert_outside_protected_roots",
    "validate_publication_directory",
    "validate_result_path",
]

EXPLICIT_SELF_HOSTING = "EXPLICIT_SELF_HOSTING"


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _canonical(path: Path) -> Path:
    return path.expanduser().resolve()


def _path_key(path: Path) -> str:
    return str(_canonical(path)).replace("/", "\\").rstrip("\\").casefold()


def _is_within(path: Path, parent: Path) -> bool:
    try:
        _canonical(path).relative_to(_canonical(parent))
    except ValueError:
        return False
    return True


def _is_reparse_point(path: Path) -> bool:
    if path.is_symlink():
        return True
    try:
        attributes = os.lstat(path).st_file_attributes
    except (AttributeError, OSError):
        return False
    return bool(
        attributes
        & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
    )


def assert_no_reparse_ancestor(path: Path, *, purpose: str) -> None:
    """Reject existing symlink/junction ancestors before any direct write."""

    candidate = path.expanduser()
    existing = candidate
    while not existing.exists() and existing.parent != existing:
        existing = existing.parent

    chain: list[Path] = []
    current = existing
    while True:
        chain.append(current)
        if current.parent == current:
            break
        current = current.parent

    for item in reversed(chain):
        if _is_reparse_point(item):
            raise PortableBuildError(
                f"{purpose} uses a symlink or reparse-point ancestor: {item}"
            )


def _read_registry(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise PortableBuildError(
            f"Tool-owned Project registry is unreadable: {path}"
        ) from exc
    if not isinstance(value, dict):
        raise PortableBuildError(
            "Tool-owned Project registry root must be a JSON object."
        )
    return value


def _record_path(
    record: dict[str, Any],
    key: str,
    fallback: Path,
    *,
    record_id: str,
    required: bool = False,
) -> Path:
    raw = str(record.get(key) or "").strip()
    if required and not raw:
        raise PortableBuildError(
            f"Registry record {record_id} is missing required {key}."
        )
    candidate = _canonical(Path(raw)) if raw else _canonical(fallback)
    if not candidate.anchor:
        raise PortableBuildError(
            f"Registry record {record_id} has a non-absolute {key}: {candidate}"
        )
    return candidate


def _append_root(
    roots: list[ProtectedRoot],
    seen: dict[str, ProtectedRoot],
    *,
    label: str,
    owner_id: str,
    owner_slug: str,
    root_kind: str,
    path: Path,
) -> None:
    canonical = _canonical(path)
    key = _path_key(canonical)
    existing = seen.get(key)
    if existing is not None:
        if existing.owner_id != owner_id or existing.root_kind != root_kind:
            raise PortableBuildError(
                "Ambiguous registry ownership for protected root "
                f"{canonical}: {existing.owner_id}/{existing.root_kind} and "
                f"{owner_id}/{root_kind}"
            )
        return
    protected = ProtectedRoot(
        label=label,
        owner_id=owner_id,
        owner_slug=owner_slug,
        root_kind=root_kind,
        path=canonical,
    )
    roots.append(protected)
    seen[key] = protected


def load_registry_boundary(
    project_root: Path,
    *,
    registry_path: Path | None = None,
) -> RegistryBoundary:
    """Require explicit self-hosting and collect every registered owner root."""

    tool_root = _canonical(project_root)
    if os.name != "nt" or not tool_root.anchor:
        raise PortableBuildError(
            "Portable registry-boundary validation requires Windows."
        )

    drive = Path(tool_root.anchor).resolve()
    tool_support = (drive / f"{tool_root.name}_show_project_to_AI").resolve()
    tool_transient = (
        drive / f"{tool_root.name}_delete_after_daily_work"
    ).resolve()
    registry = (
        registry_path.resolve()
        if registry_path is not None
        else tool_support / "tool_project_registry" / "projects.json"
    )
    if not registry.is_file():
        raise PortableBuildError(
            f"Tool-owned Project registry is missing: {registry}"
        )

    payload = _read_registry(registry)
    current_id = str(payload.get("current_project_id") or "").strip()
    projects = payload.get("projects")
    if not current_id or not isinstance(projects, dict):
        raise PortableBuildError(
            "Tool-owned registry has no valid current_project_id/projects map."
        )

    current = projects.get(current_id)
    if not isinstance(current, dict):
        raise PortableBuildError(
            f"Active registry record is missing: {current_id}"
        )

    active_root = _record_path(
        current,
        "project_root",
        tool_root,
        record_id=current_id,
        required=True,
    )
    active_mode = str(current.get("selection_mode") or "").strip()
    if active_root != tool_root:
        raise PortableBuildError(
            "Portable creation requires the KANDA Reasoner Tool to be the "
            "active Project. Select E:\\kanda_reasoner in the global "
            f"Project Root widget; active root is {active_root}."
        )
    if active_mode != EXPLICIT_SELF_HOSTING:
        raise PortableBuildError(
            "Portable creation requires explicit self-hosting authority; "
            f"selection_mode is {active_mode or '<missing>'}."
        )

    roots: list[ProtectedRoot] = []
    seen: dict[str, ProtectedRoot] = {}

    for record_id, raw_record in sorted(projects.items(), key=lambda item: str(item[0])):
        if not isinstance(raw_record, dict):
            raise PortableBuildError(
                f"Registry Project record is not an object: {record_id}"
            )
        owner_id = str(
            raw_record.get("stable_project_id") or record_id
        ).strip()
        project_path = _record_path(
            raw_record,
            "project_root",
            tool_root,
            record_id=str(record_id),
            required=True,
        )
        owner_slug = str(
            raw_record.get("owner_slug") or project_path.name
        ).strip() or project_path.name
        record_drive = Path(project_path.anchor).resolve()
        support_path = _record_path(
            raw_record,
            "project_support_root",
            record_drive / f"{project_path.name}_show_project_to_AI",
            record_id=str(record_id),
        )
        transient_path = _record_path(
            raw_record,
            "project_transient_root",
            record_drive / f"{project_path.name}_delete_after_daily_work",
            record_id=str(record_id),
        )

        _append_root(
            roots,
            seen,
            label=f"{owner_slug} Project source",
            owner_id=owner_id,
            owner_slug=owner_slug,
            root_kind="PROJECT_ROOT",
            path=project_path,
        )
        _append_root(
            roots,
            seen,
            label=f"{owner_slug} Project Support",
            owner_id=owner_id,
            owner_slug=owner_slug,
            root_kind="PROJECT_SUPPORT_ROOT",
            path=support_path,
        )
        _append_root(
            roots,
            seen,
            label=f"{owner_slug} transient root",
            owner_id=owner_id,
            owner_slug=owner_slug,
            root_kind="PROJECT_TRANSIENT_ROOT",
            path=transient_path,
        )

    required_keys = {
        _path_key(tool_root),
        _path_key(tool_support),
        _path_key(tool_transient),
    }
    if not required_keys.issubset(seen):
        raise PortableBuildError(
            "Active self-hosting registry record does not resolve all Tool roots."
        )

    return RegistryBoundary(
        registry_path=registry,
        registry_sha256=_sha256(registry),
        current_project_id=current_id,
        selection_mode=active_mode,
        tool_root=tool_root,
        tool_support_root=tool_support,
        tool_transient_root=tool_transient,
        protected_roots=tuple(
            sorted(roots, key=lambda item: (_path_key(item.path), item.root_kind))
        ),
    )



def assert_registry_unchanged(boundary: RegistryBoundary) -> None:
    """Fail closed when registry authority changes after boundary loading."""

    if not boundary.registry_path.is_file():
        raise PortableBuildError(
            f"Tool-owned Project registry disappeared: {boundary.registry_path}"
        )
    current_hash = _sha256(boundary.registry_path)
    if current_hash != boundary.registry_sha256:
        raise PortableBuildError(
            "Tool-owned Project registry changed during Portable boundary "
            "validation; restart the operation."
        )

def assert_outside_protected_roots(
    path: Path,
    boundary: RegistryBoundary,
    *,
    purpose: str,
) -> Path:
    """Fail before a direct write when path enters any protected owner root."""

    candidate = _canonical(path)
    for root in boundary.protected_roots:
        if _is_within(candidate, root.path):
            raise PortableBuildError(
                f"{purpose} is inside protected {root.label}: {candidate}"
            )
    return candidate


def validate_publication_directory(
    directory: Path,
    boundary: RegistryBoundary,
    *,
    final_zip_name: str,
) -> Path:
    """Validate the final ZIP target before the destination write probe."""

    assert_registry_unchanged(boundary)
    selected = _canonical(directory)
    assert_no_reparse_ancestor(
        selected,
        purpose="Portable destination",
    )
    assert_outside_protected_roots(
        selected / final_zip_name,
        boundary,
        purpose="Portable final ZIP",
    )
    return selected


def validate_result_path(
    path: Path,
    boundary: RegistryBoundary,
) -> Path:
    """Validate result JSON before parent creation or temporary writes."""

    assert_registry_unchanged(boundary)
    candidate = _canonical(path)
    assert_no_reparse_ancestor(
        candidate.parent,
        purpose="Portable result JSON parent",
    )
    assert_outside_protected_roots(
        candidate,
        boundary,
        purpose="Portable result JSON",
    )
    return candidate
