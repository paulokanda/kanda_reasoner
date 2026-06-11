"""Hashing helpers for reasoner context bundle artifacts."""

from __future__ import annotations

import hashlib
from pathlib import Path

__all__ = ["sha256_bytes", "sha256_file", "sha256_text_normalized"]


def sha256_bytes(data: bytes) -> str:
    """Return the SHA-256 hex digest for bytes."""
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: str | Path) -> str:
    """Return the SHA-256 hex digest for a file read in binary mode."""
    return sha256_bytes(Path(path).read_bytes())


def sha256_text_normalized(text: str) -> str:
    """Return the SHA-256 digest for text with normalized newlines."""
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    return sha256_bytes(normalized.encode("utf-8"))
