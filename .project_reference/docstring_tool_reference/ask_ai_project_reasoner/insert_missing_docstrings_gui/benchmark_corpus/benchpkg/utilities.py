"""Support missing-docstring insertion workflows."""

import re
from pathlib import Path

DEFAULT_SUFFIX = ".txt"

def normalize_name(raw: str) -> str:
    cleaned = re.sub(r"\s+", " ", raw).strip()
    return cleaned.lower()

def build_path(root: Path, name: str, *, suffix: str = DEFAULT_SUFFIX) -> Path:
    return root / f"{name}{suffix}"

def is_supported_extension(path: Path) -> bool:
    return path.suffix.lower() in {".txt", ".md"}
