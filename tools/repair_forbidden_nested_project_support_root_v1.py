# project-path: tools/repair_forbidden_nested_project_support_root_v1.py
"""Migrate and remove one forbidden nested Project support root safely."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import shutil
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.project_support_boundary import (
    canonical_project_support_root,
    forbidden_nested_support_root,
    project_support_root_blockers,
)

FEATURE_ID = "project-tool-boundary-nested-support-root-canon-startup-guard-v1r3"
LEGACY_SOURCE_FIXTURE_NAME = "_release9_exchange_validation_fixture"


def _hash_file(path: Path) -> str:
    """Return a SHA-256 digest for one regular file."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _members(root: Path) -> tuple[Path, ...]:
    """Return deterministic descendants while rejecting links."""
    members = tuple(sorted(root.rglob("*"), key=lambda item: item.as_posix()))
    links = [item for item in members if item.is_symlink()]
    if links:
        raise RuntimeError(
            "FORBIDDEN_NESTED_SUPPORT_ROOT_SYMLINK_BLOCKED:"
            + ",".join(str(item) for item in links)
        )
    return members


def remove_legacy_source_validation_fixture(project_root: str | Path) -> bool:
    """Remove the obsolete Release 9 fixture from Project source."""
    source_root = Path(project_root).expanduser().resolve(strict=True)
    fixture = source_root / LEGACY_SOURCE_FIXTURE_NAME
    if fixture.is_symlink():
        raise RuntimeError(
            "LEGACY_SOURCE_VALIDATION_FIXTURE_SYMLINK_BLOCKED:" + str(fixture)
        )
    if not fixture.exists():
        return False
    if not fixture.is_dir():
        raise RuntimeError(
            "LEGACY_SOURCE_VALIDATION_FIXTURE_NOT_DIRECTORY:" + str(fixture)
        )
    shutil.rmtree(fixture)
    return True


def migrate_nested_support_tree(
    forbidden_root: str | Path,
    canonical_root: str | Path,
) -> int:
    """Move one already-resolved nested tree to a conflict-free target."""
    forbidden = Path(forbidden_root).expanduser().resolve(strict=False)
    canonical = Path(canonical_root).expanduser().resolve(strict=False)
    if canonical == forbidden:
        raise RuntimeError("SUPPORT_ROOT_MIGRATION_TARGET_EQUALS_SOURCE")
    try:
        canonical.relative_to(forbidden)
    except ValueError:
        pass
    else:
        raise RuntimeError("SUPPORT_ROOT_MIGRATION_TARGET_INSIDE_SOURCE")
    if not forbidden.exists():
        return 0
    if not forbidden.is_dir() or forbidden.is_symlink():
        raise RuntimeError(
            "FORBIDDEN_NESTED_SUPPORT_ROOT_NOT_DIRECTORY:" + str(forbidden)
        )

    members = _members(forbidden)
    conflicts: list[str] = []
    for source in members:
        if not source.is_file():
            continue
        relative = source.relative_to(forbidden)
        destination = canonical / relative
        if destination.exists():
            if (
                not destination.is_file()
                or _hash_file(source) != _hash_file(destination)
            ):
                conflicts.append(relative.as_posix())
    if conflicts:
        raise RuntimeError(
            "FORBIDDEN_NESTED_SUPPORT_ROOT_CONFLICT:" + "|".join(conflicts)
        )

    canonical.mkdir(parents=True, exist_ok=True)
    moved = 0
    for source in members:
        if not source.is_file():
            continue
        relative = source.relative_to(forbidden)
        destination = canonical / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        if destination.exists():
            source.unlink()
        else:
            shutil.move(str(source), str(destination))
            moved += 1
    for directory in sorted(
        (item for item in members if item.is_dir()),
        key=lambda item: len(item.parts),
        reverse=True,
    ):
        directory.rmdir()
    forbidden.rmdir()
    return moved


def repair_nested_support_root(project_root: str | Path) -> tuple[Path, Path, int]:
    """Move conflict-free content to canonical support and remove nested root."""
    source_root = Path(project_root).expanduser().resolve(strict=True)
    forbidden = forbidden_nested_support_root(source_root)
    canonical = canonical_project_support_root(source_root)
    blockers = project_support_root_blockers(source_root, canonical)
    if blockers:
        raise RuntimeError("CANONICAL_SUPPORT_ROOT_BLOCKED:" + "|".join(blockers))
    moved = migrate_nested_support_tree(forbidden, canonical)
    return forbidden, canonical, moved


def main() -> int:
    """Run the conflict-safe repair command."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True)
    args = parser.parse_args()
    try:
        forbidden, canonical, moved = repair_nested_support_root(args.project_root)
        fixture_removed = remove_legacy_source_validation_fixture(args.project_root)
    except (OSError, RuntimeError, ValueError) as exc:
        print("PROJECT_SUPPORT_ROOT_REPAIR: FAIL - " + str(exc))
        return 1
    print("FORBIDDEN_NESTED_SUPPORT_ROOT: " + str(forbidden))
    print("CANONICAL_PROJECT_SUPPORT_ROOT: " + str(canonical))
    print("MIGRATED_FILE_COUNT: " + str(moved))
    print("LEGACY_SOURCE_VALIDATION_FIXTURE_REMOVED: " + str(fixture_removed).upper())
    print("FORBIDDEN_NESTED_SUPPORT_ROOT_REMOVED: PASS")
    print("SOURCE_ROOT_VALIDATION_FIXTURE_ABSENT: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
