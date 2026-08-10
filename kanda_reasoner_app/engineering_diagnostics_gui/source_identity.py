# project-path: kanda_reasoner_app/engineering_diagnostics_gui/source_identity.py
"""Read-only source identity helpers for stale diagnostic rejection."""

from __future__ import annotations

import hashlib
from pathlib import Path

__all__ = ["project_source_fingerprint"]

_EXCLUDED_DIR_NAMES = frozenset(
    {
        ".git",
        ".idea",
        ".mypy_cache",
        ".pytest_cache",
        ".ruff_cache",
        ".tox",
        ".venv",
        "__pycache__",
        "build",
        "dist",
        "node_modules",
        "venv",
    }
)
_EXCLUDED_FILE_SUFFIXES = frozenset({".pyc", ".pyo"})
_CHUNK_SIZE = 1024 * 1024


def _candidate_files(project_root: Path) -> tuple[Path, ...]:
    files: list[Path] = []
    for path in project_root.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(project_root)
        if any(part in _EXCLUDED_DIR_NAMES for part in relative.parts[:-1]):
            continue
        if path.suffix.lower() in _EXCLUDED_FILE_SUFFIXES:
            continue
        files.append(path)
    return tuple(sorted(files, key=lambda item: item.relative_to(project_root).as_posix()))


def project_source_fingerprint(project_root: str | Path) -> str:
    """Hash current Project source bytes without writing or following links."""
    root = Path(project_root).expanduser().resolve(strict=True)
    digest = hashlib.sha256()
    digest.update(b"engineering-diagnostics-gui-source-v1\0")
    for path in _candidate_files(root):
        relative = path.relative_to(root).as_posix()
        digest.update(relative.encode("utf-8", errors="surrogatepass"))
        digest.update(b"\0")
        try:
            with path.open("rb") as handle:
                while True:
                    chunk = handle.read(_CHUNK_SIZE)
                    if not chunk:
                        break
                    digest.update(chunk)
        except OSError as exc:
            raise RuntimeError("PROJECT_SOURCE_FINGERPRINT_READ_FAILED:" + relative) from exc
        digest.update(b"\0")
    return digest.hexdigest()
