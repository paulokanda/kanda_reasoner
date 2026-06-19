"""Inventory active references to the legacy implementation package.

This module is intentionally non-mutating. It helps staged package migration by
reporting files that still mention the legacy package token.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

LEGACY_TOKEN_PARTS = ("ask", "ai", "project", "reasoner")
LEGACY_TOKEN = "_".join(LEGACY_TOKEN_PARTS)
CANONICAL_TOKEN = "kanda_reasoner_app"

EXCLUDED_DIR_NAMES = {
    ".git",
    ".hg",
    ".idea",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "__pycache__",
    "project_freeze_ledger",
    ".project_reference",
    "_project_reference",
    "workbench",
}

TEXT_SUFFIXES = {
    ".md",
    ".txt",
    ".json",
    ".yaml",
    ".yml",
    ".toml",
    ".ini",
    ".cfg",
    ".ps1",
}

__all__ = [
    "CANONICAL_TOKEN",
    "InventoryEntry",
    "LEGACY_TOKEN",
    "LEGACY_TOKEN_PARTS",
    "OwnerBoxSummary",
    "build_argument_parser",
    "classify_owner_box",
    "collect_inventory",
    "collect_owner_box_summary",
    "iter_candidate_files",
    "main",
]


@dataclass(frozen=True)
class InventoryEntry:
    """A file containing one or more legacy package references."""

    relative_path: str
    count: int


@dataclass(frozen=True)
class OwnerBoxSummary:
    """Reference count summary for one migration owner box."""

    owner_box: str
    python_files: int
    python_references: int
    text_files: int
    text_references: int


def classify_owner_box(relative_path: str) -> str:
    """Return a stable owner-box label for a project-relative path."""

    normalized = relative_path.replace("\\", "/")
    parts = normalized.split("/")

    if not parts or parts[0] == "":
        return "root"

    first = parts[0]

    if first == LEGACY_TOKEN and len(parts) >= 2:
        return first + "/" + parts[1]

    if first == "kanda_reasoner_app" and len(parts) >= 2:
        return first + "/" + parts[1]

    if first == "tests":
        return "tests"

    return first


def _is_excluded(path: Path, root: Path) -> bool:
    try:
        relative_parts = path.relative_to(root).parts
    except ValueError:
        return True

    return any(part in EXCLUDED_DIR_NAMES for part in relative_parts)


def iter_candidate_files(root: Path) -> Iterable[Path]:
    """Yield candidate text files below root, excluding generated/reference areas."""

    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if _is_excluded(path, root):
            continue
        if path.suffix == ".py" or path.suffix.lower() in TEXT_SUFFIXES:
            yield path


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def collect_inventory(root: Path, legacy_token: str = LEGACY_TOKEN) -> tuple[list[InventoryEntry], list[InventoryEntry]]:
    """Collect Python and text-file legacy token references under root."""

    root = root.resolve()
    python_entries: list[InventoryEntry] = []
    text_entries: list[InventoryEntry] = []

    for path in iter_candidate_files(root):
        text = _read_text(path)
        count = text.count(legacy_token)
        if count <= 0:
            continue

        relative_path = path.relative_to(root).as_posix()
        entry = InventoryEntry(relative_path=relative_path, count=count)

        if path.suffix == ".py":
            python_entries.append(entry)
        else:
            text_entries.append(entry)

    python_entries.sort(key=lambda item: item.relative_path.lower())
    text_entries.sort(key=lambda item: item.relative_path.lower())
    return python_entries, text_entries


def collect_owner_box_summary(
    python_entries: list[InventoryEntry],
    text_entries: list[InventoryEntry],
) -> list[OwnerBoxSummary]:
    """Summarize legacy references by migration owner box."""

    summary_by_owner: dict[str, dict[str, int]] = {}

    def ensure_owner(owner_box: str) -> dict[str, int]:
        if owner_box not in summary_by_owner:
            summary_by_owner[owner_box] = {
                "python_files": 0,
                "python_references": 0,
                "text_files": 0,
                "text_references": 0,
            }
        return summary_by_owner[owner_box]

    for entry in python_entries:
        owner = ensure_owner(classify_owner_box(entry.relative_path))
        owner["python_files"] += 1
        owner["python_references"] += entry.count

    for entry in text_entries:
        owner = ensure_owner(classify_owner_box(entry.relative_path))
        owner["text_files"] += 1
        owner["text_references"] += entry.count

    summaries = [
        OwnerBoxSummary(
            owner_box=owner_box,
            python_files=values["python_files"],
            python_references=values["python_references"],
            text_files=values["text_files"],
            text_references=values["text_references"],
        )
        for owner_box, values in summary_by_owner.items()
    ]
    summaries.sort(
        key=lambda item: (
            -(item.python_files + item.text_files),
            -(item.python_references + item.text_references),
            item.owner_box.lower(),
        )
    )
    return summaries


def _print_entries(title: str, entries: list[InventoryEntry], limit: int) -> None:
    print(title + ":")

    if not entries:
        print("  none")
        return

    for entry in entries[:limit]:
        print(f"  {entry.relative_path} ({entry.count})")

    if len(entries) > limit:
        print(f"  ... truncated, total {len(entries)}")


def _print_owner_summary(entries: list[OwnerBoxSummary], limit: int) -> None:
    print("owner box summary:")

    if not entries:
        print("  none")
        return

    for entry in entries[:limit]:
        print(
            "  "
            + entry.owner_box
            + " | py_files="
            + str(entry.python_files)
            + " py_refs="
            + str(entry.python_references)
            + " text_files="
            + str(entry.text_files)
            + " text_refs="
            + str(entry.text_references)
        )

    if len(entries) > limit:
        print("  ... truncated, total " + str(len(entries)))


def build_argument_parser() -> argparse.ArgumentParser:
    """Build the command-line parser."""

    parser = argparse.ArgumentParser(
        description="Inventory active references to the legacy implementation package."
    )
    parser.add_argument("--root", required=True, help="Project root to scan.")
    parser.add_argument("--limit", type=int, default=80, help="Maximum entries to print per section.")
    parser.add_argument("--owner-limit", type=int, default=40, help="Maximum owner-box summary entries to print.")
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the inventory command."""

    args = build_argument_parser().parse_args(argv)
    root = Path(args.root)

    if not root.exists():
        print("Project root not found: " + str(root))
        return 2

    python_entries, text_entries = collect_inventory(root)
    owner_summary = collect_owner_box_summary(python_entries, text_entries)

    print("T10P006 legacy package inventory")
    print("legacy token: " + LEGACY_TOKEN)
    print("canonical token: " + CANONICAL_TOKEN)
    print("root: " + str(root))
    print("active python files with legacy references: " + str(len(python_entries)))
    print("text assets with legacy references: " + str(len(text_entries)))
    _print_owner_summary(owner_summary, args.owner_limit)
    _print_entries("active python references", python_entries, args.limit)
    _print_entries("text asset references", text_entries, args.limit)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
