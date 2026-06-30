# project-path: tools/kanda_cleanup_audit.py
"""Read-only cleanup candidate audit for Kanda Reasoner.

This script prints cleanup candidates but does not delete anything.
It is intentionally conservative.
"""

from __future__ import annotations

import argparse
import json
import os
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


__all__ = [
    "CleanupCandidate",
    "build_report",
    "iter_canonical_status",
    "iter_cleanup_candidates",
    "main",
    "print_report",
]


SAFE_CACHE_DIR_NAMES = {
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "htmlcov",
    "build",
    "dist",
}

SAFE_FILE_NAMES = {
    ".coverage",
    "coverage.xml",
}

SAFE_FILE_SUFFIXES = {
    ".pyc",
    ".pyo",
}

PATCH_ARCHIVE_MARKERS = (
    "kanda_reasoner_",
    "_patch_",
    "_repair",
    "_rename",
    "_deletion",
    "_migration",
    "_audit",
)

LEGACY_FOLDER_RELATIVES = (
    "ask_ai_project_reasoner",
    "kanda_reasoner_app/project_reasoner_v10",
    "kanda_reasoner_app/project_reasoner_v10_data_collector",
    "kanda_reasoner_app/project_reasoner_v10_runtime_collector",
    "kanda_reasoner_app/project_symbol_atlas",
)

CANONICAL_FOLDER_RELATIVES = (
    "kanda_reasoner_app/reasoner_engine",
    "kanda_reasoner_app/reasoner_context_collector",
    "kanda_reasoner_app/reasoner_runtime_collector",
    "kanda_reasoner_app/reasoner_symbol_atlas",
)


@dataclass(frozen=True)
class CleanupCandidate:
    """A single read-only cleanup candidate."""

    category: str
    relative_path: str
    reason: str
    action: str


def _normalize_relative(path: Path, root: Path) -> str:
    """Support normalize relative behavior.
    
    Parameters
    ----------
    path : Path
        The file or folder path.
    root : Path
        The root path.
    
    Returns
    -------
    str
        The string result.
    """
    
    return path.relative_to(root).as_posix()


def _is_inside_ignored_directory(path: Path, root: Path) -> bool:
    """Support is inside ignored directory behavior.
    
    Parameters
    ----------
    path : Path
        The file or folder path.
    root : Path
        The root path.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    try:
        relative_parts = path.relative_to(root).parts
    except ValueError:
        return True

    ignored_names = {
        ".git",
        "_kanda_patch_backups",
    }

    return any(part in ignored_names for part in relative_parts)


def _looks_like_patch_archive(path: Path, root: Path) -> bool:
    """Support looks like patch archive behavior.
    
    Parameters
    ----------
    path : Path
        The file or folder path.
    root : Path
        The root path.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    if path.suffix.lower() != ".zip":
        return False

    try:
        relative_parts = path.relative_to(root).parts
    except ValueError:
        return False

    if len(relative_parts) != 1:
        return False

    name = path.name.lower()

    if name.startswith("kanda_reasoner_"):
        return True

    return any(marker in name for marker in PATCH_ARCHIVE_MARKERS)


def iter_cleanup_candidates(root: Path) -> Iterable[CleanupCandidate]:
    """Yield cleanup candidates from a project root."""

    root = root.resolve()

    for legacy_relative in LEGACY_FOLDER_RELATIVES:
        legacy_path = root / Path(legacy_relative)

        if legacy_path.exists():
            yield CleanupCandidate(
                category="legacy_leftover",
                relative_path=legacy_relative,
                reason="Legacy folder should be absent after validated migration.",
                action=(
                    "Review and delete only after confirming latest validation "
                    "remains clean."
                ),
            )

    for path in root.rglob("*"):
        if _is_inside_ignored_directory(path, root):
            continue

        relative_path = _normalize_relative(path, root)

        if path.is_dir() and path.name in SAFE_CACHE_DIR_NAMES:
            yield CleanupCandidate(
                category="safe_cache_directory",
                relative_path=relative_path,
                reason="Generated cache/build directory; usually safe to delete.",
                action="Delete only if no process is currently running.",
            )
            continue

        if not path.is_file():
            continue

        if path.name in SAFE_FILE_NAMES:
            yield CleanupCandidate(
                category="safe_coverage_file",
                relative_path=relative_path,
                reason="Generated coverage output file; safe to regenerate.",
                action="Delete if not needed for reporting.",
            )
            continue

        if path.suffix.lower() in SAFE_FILE_SUFFIXES:
            yield CleanupCandidate(
                category="safe_compiled_python_file",
                relative_path=relative_path,
                reason="Compiled Python cache file; safe to regenerate.",
                action="Delete if desired.",
            )
            continue

        if _looks_like_patch_archive(path, root):
            yield CleanupCandidate(
                category="patch_archive_in_project_root",
                relative_path=relative_path,
                reason="Patch delivery archive in project root; not runtime source.",
                action=(
                    "Move outside project or delete after confirming backups "
                    "are no longer needed."
                ),
            )


def iter_canonical_status(root: Path) -> Iterable[CleanupCandidate]:
    """Yield canonical folder status entries."""

    root = root.resolve()

    for canonical_relative in CANONICAL_FOLDER_RELATIVES:
        canonical_path = root / Path(canonical_relative)
        if canonical_path.exists():
            status = "present"
            reason = "Canonical folder is present and should be kept."
        else:
            status = "missing"
            reason = "Canonical folder is missing and should not be cleaned."

        yield CleanupCandidate(
            category=f"canonical_{status}",
            relative_path=canonical_relative,
            reason=reason,
            action="Keep.",
        )


def build_report(root: Path) -> dict[str, object]:
    """Build the read-only cleanup audit report."""

    candidates = list(iter_cleanup_candidates(root))
    canonical_status = list(iter_canonical_status(root))

    category_counts: dict[str, int] = {}
    for candidate in candidates:
        category_counts[candidate.category] = (
            category_counts.get(candidate.category, 0) + 1
        )

    return {
        "project_root": str(root.resolve()),
        "mode": "read_only_cleanup_candidates_audit",
        "candidate_count": len(candidates),
        "category_counts": category_counts,
        "canonical_status": [asdict(item) for item in canonical_status],
        "cleanup_candidates": [asdict(item) for item in candidates],
    }


def print_report(report: dict[str, object]) -> None:
    """Print a human-readable report."""

    print("KANDA CLEANUP CANDIDATES AUDIT")
    print("Mode: read-only")
    print(f"Project root: {report['project_root']}")
    print(f"Candidate count: {report['candidate_count']}")
    print("")

    print("Canonical folders:")
    for item in report["canonical_status"]:
        print(f"  {item['category']}: {item['relative_path']}")

    print("")
    print("Candidate counts:")
    category_counts = report["category_counts"]
    if category_counts:
        for category, count in sorted(category_counts.items()):
            print(f"  {category}: {count}")
    else:
        print("  none")

    print("")
    print("Cleanup candidates:")
    candidates = report["cleanup_candidates"]
    if not candidates:
        print("  none")
        return

    for item in candidates:
        print(f"  [{item['category']}] {item['relative_path']}")
        print(f"    Reason: {item['reason']}")
        print(f"    Action: {item['action']}")


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""

    parser = argparse.ArgumentParser(
        description="Read-only cleanup candidate audit for Kanda Reasoner."
    )
    parser.add_argument(
        "--root",
        default=os.environ.get("kanda_reasoner_project_root") or ".",
        help="Project root path.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print machine-readable JSON instead of text.",
    )
    return parser.parse_args()


def main() -> int:
    """Run the cleanup audit."""

    args = parse_args()
    root = Path(args.root).resolve()

    if not root.exists():
        print(f"Project root not found: {root}")
        return 2

    report = build_report(root)

    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print_report(report)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
