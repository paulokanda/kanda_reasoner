# project-path: kanda_reasoner_app/prompt_library_gui/library_catalog.py
"""Read-only catalog loader for current Prompt Library text assets."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from .library_paths import prompt_library_root, prompt_template_root

__all__ = [
    "PromptLibraryItem",
    "load_prompt_library_items",
]

_TEXT_SUFFIXES = {".md", ".txt"}
_METADATA_SUFFIX = ".json"
_SKIP_FILENAMES = {"README.md", "_FOLDER_ASSIMILATION.md"}
_HIDDEN_STATUSES = {
    "archived",
    "deprecated",
    "inactive",
    "retired",
    "superseded",
}


@dataclass(frozen=True)
class PromptLibraryItem:
    """Describe one read-only prompt-library text asset."""

    title: str
    relative_path: str
    path: Path
    category: str
    metadata_path: Path | None
    metadata: dict[str, object]

    def read_text(self) -> str:
        """Return the prompt text using UTF-8 with replacement for bad bytes."""
        return self.path.read_text(encoding="utf-8", errors="replace")


def _metadata_directories(root: Path) -> tuple[Path, ...]:
    """Return supported centralized metadata directories for one library."""
    candidates = (root / "METADATA", root / "metadata")
    return tuple(path for path in candidates if path.is_dir())


def _metadata_candidates(root: Path, text_path: Path) -> list[Path]:
    """Return likely metadata sidecar paths for a text asset."""
    candidates = [text_path.with_suffix(text_path.suffix + ".meta.json")]
    candidates.append(text_path.with_suffix(".meta.json"))

    stem = _normalize_identifier(text_path.stem)
    for metadata_dir in _metadata_directories(root):
        candidates.extend(sorted(metadata_dir.glob(stem + "*.meta.json")))
    return candidates


def _normalize_identifier(value: str) -> str:
    """Normalize a prompt title or filename into a metadata-style identifier."""
    chars: list[str] = []
    last_was_sep = False
    for char in value.lower():
        if char.isalnum():
            chars.append(char)
            last_was_sep = False
        elif not last_was_sep:
            chars.append("_")
            last_was_sep = True
    return "".join(chars).strip("_")


def _read_metadata_file(path: Path) -> dict[str, object]:
    """Read one metadata file and return an object dictionary if valid."""
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError):
        return {}
    if isinstance(data, dict):
        return data
    return {}


def _metadata_matches_text(text_path: Path, metadata: dict[str, object]) -> bool:
    """Return whether metadata appears to describe a text asset."""
    text_name = _normalize_identifier(text_path.stem)
    filename = metadata.get("filename")
    if isinstance(filename, str) and filename.strip() == text_path.name:
        return True
    for key in ("display_name", "prompt_id"):
        value = metadata.get(key)
        if not isinstance(value, str) or not value.strip():
            continue
        normalized = _normalize_identifier(value)
        if normalized and (normalized in text_name or text_name in normalized):
            return True
    return False


def _load_metadata(root: Path, text_path: Path) -> tuple[Path | None, dict[str, object]]:
    """Load the first valid metadata sidecar for a text asset."""
    for candidate in _metadata_candidates(root, text_path):
        if not candidate.exists() or candidate.suffix != _METADATA_SUFFIX:
            continue
        data = _read_metadata_file(candidate)
        if data:
            return candidate, data

    for metadata_dir in _metadata_directories(root):
        for candidate in sorted(metadata_dir.glob("*.meta.json")):
            data = _read_metadata_file(candidate)
            if data and _metadata_matches_text(text_path, data):
                return candidate, data

    return None, {}


def _item_title(text_path: Path, metadata: dict[str, object]) -> str:
    """Return a user-facing title for a prompt-library item."""
    display_name = metadata.get("display_name")
    if isinstance(display_name, str) and display_name.strip():
        return display_name.strip()
    title = metadata.get("title")
    if isinstance(title, str) and title.strip():
        return title.strip()
    return text_path.stem.replace("_", " ").strip()


def _is_current_item(metadata: dict[str, object]) -> bool:
    """Return whether metadata permits the prompt in the current GUI catalog."""
    status = str(metadata.get("status", "")).strip().lower()
    load_type = str(metadata.get("load_type", "")).strip().lower()
    if status in _HIDDEN_STATUSES:
        return False
    if load_type == "never":
        return False
    return True


def _iter_scan_roots(root: Path | None) -> list[tuple[Path, str, Path]]:
    """Return scan roots, display prefixes, and metadata-owner roots."""
    selected_root = root or prompt_library_root()
    active_root = selected_root / "ACTIVE_PROMPTS"
    if active_root.is_dir():
        return [(active_root, "ACTIVE_PROMPTS", selected_root)]

    if root is not None:
        return [(selected_root, "", selected_root)]

    roots = [(selected_root, "", selected_root)]
    template_root = prompt_template_root()
    if template_root.exists():
        roots.append(
            (
                template_root,
                "templates/prompt_library_templates",
                template_root,
            )
        )
    return roots


def _relative_prompt_path(base: Path, prefix: str, path: Path) -> str:
    """Return a stable display path for a scanned prompt asset."""
    local_relative = path.relative_to(base).as_posix()
    if prefix:
        return prefix.rstrip("/") + "/" + local_relative
    return local_relative


def load_prompt_library_items(root: Path | None = None) -> list[PromptLibraryItem]:
    """Load current read-only Prompt Library text assets.

    Canonical workspace scans are limited to ACTIVE_PROMPTS and hide metadata
    entries marked deprecated, retired, inactive, archived, superseded, or
    load_type=never. Legacy package scans remain available as a fallback.
    """
    items: list[PromptLibraryItem] = []
    for scan_root, prefix, metadata_root in _iter_scan_roots(root):
        if not scan_root.exists():
            continue
        for path in sorted(scan_root.rglob("*")):
            if not path.is_file():
                continue
            if path.name in _SKIP_FILENAMES:
                continue
            if path.suffix.lower() not in _TEXT_SUFFIXES:
                continue
            metadata_path, metadata = _load_metadata(metadata_root, path)
            if not _is_current_item(metadata):
                continue
            relative = _relative_prompt_path(scan_root, prefix, path)
            local_relative = path.relative_to(scan_root).as_posix()
            category = (
                local_relative.split("/", 1)[0]
                if "/" in local_relative
                else "root"
            )
            items.append(
                PromptLibraryItem(
                    title=_item_title(path, metadata),
                    relative_path=relative,
                    path=path,
                    category=category,
                    metadata_path=metadata_path,
                    metadata=metadata,
                )
            )

    return sorted(items, key=lambda item: (item.category.lower(), item.title.lower()))
