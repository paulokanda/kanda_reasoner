"""Remove stale active-tree folders left after Kanda Reasoner renames.

This tool is intentionally narrow. It only targets exact stale folder paths in the
active project tree and never deletes project_freeze_ledger archives.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
from dataclasses import asdict, dataclass
from pathlib import Path


__all__ = [
    "StaleFolderResult",
    "STALE_ACTIVE_FOLDERS",
    "build_stale_folder_report",
    "delete_stale_folders",
    "main",
    "parse_stale_folder_cleanup_args",
]


STALE_ACTIVE_FOLDERS = (
    "ask_ai_project_reasoner",
    "kanda_reasoner_app/project_reasoner_v10",
    "kanda_reasoner_app/project_reasoner_v10_data_collector",
    "kanda_reasoner_app/project_reasoner_v10_runtime_collector",
    "kanda_reasoner_app/project_symbol_atlas",
)

CANONICAL_REQUIRED_FOLDERS = (
    "kanda_reasoner_app/reasoner_engine",
    "kanda_reasoner_app/reasoner_context_collector",
    "kanda_reasoner_app/reasoner_runtime_collector",
    "kanda_reasoner_app/reasoner_symbol_atlas",
)


@dataclass(frozen=True)
class StaleFolderResult:
    """A stale folder cleanup result."""

    relative_path: str
    status: str
    reason: str


def _safe_relative_path(relative_path: str) -> Path:
    path = Path(relative_path)

    if path.is_absolute():
        raise ValueError(f"Absolute path is not allowed: {relative_path}")

    if any(part == ".." for part in path.parts):
        raise ValueError(f"Parent traversal is not allowed: {relative_path}")

    if path.parts and path.parts[0] == "project_freeze_ledger":
        raise ValueError(f"Reference archive path is not allowed: {relative_path}")

    return path


def _validate_project_root(root: Path) -> None:
    if not root.exists():
        raise FileNotFoundError(f"Project root not found: {root}")

    for relative_path in CANONICAL_REQUIRED_FOLDERS:
        canonical_path = root / Path(relative_path)
        if not canonical_path.exists():
            raise FileNotFoundError(
                f"Canonical required folder is missing: {relative_path}"
            )


def build_stale_folder_report(root: Path) -> dict[str, object]:
    """Build a read-only stale active folder report."""

    root = root.resolve()
    _validate_project_root(root)

    results: list[StaleFolderResult] = []

    for relative_path in STALE_ACTIVE_FOLDERS:
        safe_path = _safe_relative_path(relative_path)
        target = root / safe_path

        if target.exists():
            status = "present"
            reason = "Stale active-tree folder should be deleted after backup."
        else:
            status = "absent"
            reason = "Stale active-tree folder is already absent."

        results.append(
            StaleFolderResult(
                relative_path=relative_path,
                status=status,
                reason=reason,
            )
        )

    return {
        "project_root": str(root),
        "mode": "stale_active_folder_cleanup_report",
        "present_count": sum(1 for item in results if item.status == "present"),
        "absent_count": sum(1 for item in results if item.status == "absent"),
        "stale_folders": [asdict(item) for item in results],
    }


def delete_stale_folders(root: Path, backup_dir: Path) -> dict[str, object]:
    """Delete stale active folders after copying them to a backup directory."""

    root = root.resolve()
    backup_dir = backup_dir.resolve()
    _validate_project_root(root)

    if root == backup_dir or root in backup_dir.parents:
        raise ValueError("Backup directory cannot be inside the project root.")

    backup_dir.mkdir(parents=True, exist_ok=True)

    results: list[StaleFolderResult] = []

    for relative_path in STALE_ACTIVE_FOLDERS:
        safe_path = _safe_relative_path(relative_path)
        target = root / safe_path

        if not target.exists():
            results.append(
                StaleFolderResult(
                    relative_path=relative_path,
                    status="already_absent",
                    reason="No deletion needed.",
                )
            )
            continue

        if not target.is_dir():
            raise NotADirectoryError(
                f"Stale target exists but is not a directory: {relative_path}"
            )

        backup_target = backup_dir / safe_path
        backup_target.parent.mkdir(parents=True, exist_ok=True)

        if backup_target.exists():
            raise FileExistsError(f"Backup target already exists: {backup_target}")

        shutil.copytree(target, backup_target)
        shutil.rmtree(target)

        results.append(
            StaleFolderResult(
                relative_path=relative_path,
                status="deleted_with_backup",
                reason=f"Backed up to {backup_target}",
            )
        )

    return {
        "project_root": str(root),
        "backup_dir": str(backup_dir),
        "mode": "stale_active_folder_cleanup_delete",
        "deleted_count": sum(
            1 for item in results if item.status == "deleted_with_backup"
        ),
        "already_absent_count": sum(
            1 for item in results if item.status == "already_absent"
        ),
        "stale_folders": [asdict(item) for item in results],
    }


def _print_report(report: dict[str, object]) -> None:
    print("KANDA STALE RENAMED FOLDERS CLEANUP")
    print(f"Mode: {report['mode']}")
    print(f"Project root: {report['project_root']}")

    if "backup_dir" in report:
        print(f"Backup dir: {report['backup_dir']}")

    if "present_count" in report:
        print(f"Present count: {report['present_count']}")
        print(f"Absent count: {report['absent_count']}")

    if "deleted_count" in report:
        print(f"Deleted count: {report['deleted_count']}")
        print(f"Already absent count: {report['already_absent_count']}")

    print("")
    print("Stale folders:")

    for item in report["stale_folders"]:
        print(f"  [{item['status']}] {item['relative_path']}")
        print(f"    {item['reason']}")


def parse_stale_folder_cleanup_args() -> argparse.Namespace:
    """Parse command line arguments."""

    parser = argparse.ArgumentParser(
        description="Remove stale active-tree Kanda Reasoner folders."
    )
    parser.add_argument(
        "--root",
        default=os.environ.get("kanda_reasoner_project_root") or ".",
        help="Project root path.",
    )
    parser.add_argument(
        "--backup-dir",
        default=None,
        help="Backup directory for deleted stale folders.",
    )
    parser.add_argument(
        "--delete",
        action="store_true",
        help="Actually delete stale active-tree folders after backup.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print machine-readable JSON.",
    )
    return parser.parse_args()


def main() -> int:
    """Run stale folder cleanup report or deletion."""

    args = parse_stale_folder_cleanup_args()
    root = Path(args.root).resolve()

    if args.delete:
        if not args.backup_dir:
            print("--backup-dir is required with --delete")
            return 2

        report = delete_stale_folders(root, Path(args.backup_dir))
    else:
        report = build_stale_folder_report(root)

    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        _print_report(report)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
