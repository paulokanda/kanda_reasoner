"""Private file-record helpers for file_manifest_builder."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .hashing import sha256_bytes, sha256_text_normalized
from .path_normalization import relative_posix_path
from .schema_models import ProjectContext

__all__: list[str] = []

_TEXT_FILE_EXTENSIONS = (
    ".bat",
    ".cmd",
    ".css",
    ".csv",
    ".html",
    ".ini",
    ".json",
    ".md",
    ".ps1",
    ".py",
    ".qss",
    ".toml",
    ".txt",
    ".ui",
    ".xml",
    ".yaml",
    ".yml",
)

_TEXT_READ_ENCODINGS = ("utf-8", "utf-8-sig")

def _is_probable_binary(raw: bytes) -> bool:
    """Support is probable binary behavior.
    
    Parameters
    ----------
    raw : bytes
        The raw input value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    if b"\x00" in raw[:4096]:
        return True
    return False


def _newline_style(text: str) -> str:
    """Support newline style behavior.
    
    Parameters
    ----------
    text : str
        The text value.
    
    Returns
    -------
    str
        The string result.
    """
    
    has_crlf = "\r\n" in text
    text_without_crlf = text.replace("\r\n", "")
    has_lf = "\n" in text_without_crlf
    has_cr = "\r" in text_without_crlf
    if has_crlf and not has_lf and not has_cr:
        return "crlf"
    if has_lf and not has_crlf and not has_cr:
        return "lf"
    if has_cr and not has_crlf and not has_lf:
        return "cr"
    if has_crlf or has_lf or has_cr:
        return "mixed"
    return "none"


def _decode_text(raw: bytes, suffix: str) -> tuple[bool, str, str]:
    """Support decode text behavior.
    
    Parameters
    ----------
    raw : bytes
        The raw input value.
    suffix : str
        The suffix value.
    
    Returns
    -------
    tuple[bool, str, str]
        The tuple of values.
    """
    
    if _is_probable_binary(raw):
        return False, "", ""
    suffix_low = suffix.lower()
    should_try_text = suffix_low in _TEXT_FILE_EXTENSIONS or not suffix_low
    if not should_try_text:
        try:
            raw.decode("utf-8")
        except UnicodeDecodeError:
            return False, "", ""
    for encoding in _TEXT_READ_ENCODINGS:
        try:
            return True, raw.decode(encoding), encoding
        except UnicodeDecodeError:
            continue
    return False, "", ""



def _is_snapshot_text_extension(path: Path) -> bool:
    """Support is snapshot text extension behavior.
    
    Parameters
    ----------
    path : Path
        The file or folder path.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    suffix = path.suffix.lower()
    return bool(suffix) and suffix in _TEXT_FILE_EXTENSIONS


def _kind_and_text_metadata(path: Path, raw: bytes) -> dict[str, Any]:
    """Support kind and text metadata behavior.
    
    Parameters
    ----------
    path : Path
        The file or folder path.
    raw : bytes
        The raw input value.
    
    Returns
    -------
    dict[str, Any]
        The mapped values.
    """
    
    is_text, text, encoding = _decode_text(raw, path.suffix)
    if not is_text:
        return {
            "kind": "binary",
            "encoding": "binary",
            "newline": "not_applicable",
            "sha256_normalized": "",
            "included_in_active_snapshot": False,
            "snapshot_omission_reason": "binary_file_omitted",
        }
    included_in_snapshot = _is_snapshot_text_extension(path)
    omission_reason = ""
    if not included_in_snapshot:
        omission_reason = "extension_not_in_snapshot_text_policy"
    return {
        "kind": "text",
        "encoding": encoding,
        "newline": _newline_style(text),
        "sha256_normalized": sha256_text_normalized(text),
        "included_in_active_snapshot": included_in_snapshot,
        "snapshot_omission_reason": omission_reason,
    }


def _file_record(path: Path, context: ProjectContext) -> dict[str, Any]:
    """Support file record behavior.
    
    Parameters
    ----------
    path : Path
        The file or folder path.
    context : ProjectContext
        The context value.
    
    Returns
    -------
    dict[str, Any]
        The mapped values.
    """
    
    raw = path.read_bytes()
    relative_path = relative_posix_path(path, context.root)
    metadata = _kind_and_text_metadata(path, raw)
    stat = path.stat()
    return {
        "path": relative_path,
        "name": path.name,
        "extension": path.suffix.lower(),
        "kind": metadata["kind"],
        "size_bytes": stat.st_size,
        "mtime_ns": stat.st_mtime_ns,
        "encoding": metadata["encoding"],
        "newline": metadata["newline"],
        "sha256_raw": sha256_bytes(raw),
        "sha256_normalized": metadata["sha256_normalized"],
        "included_in_active_snapshot": metadata["included_in_active_snapshot"],
        "snapshot_omission_reason": metadata.get("snapshot_omission_reason", ""),
    }


def safe_file_record(path: Path, context: ProjectContext) -> dict[str, Any]:
    """Support safe file record behavior.
    
    Parameters
    ----------
    path : Path
        The file or folder path.
    context : ProjectContext
        The context value.
    
    Returns
    -------
    dict[str, Any]
        The mapped values.
    """
    
    try:
        return _file_record(path, context)
    except OSError as exc:
        relative_path = relative_posix_path(path, context.root)
        return {
            "path": relative_path,
            "name": path.name,
            "extension": path.suffix.lower(),
            "kind": "unreadable",
            "size_bytes": 0,
            "mtime_ns": 0,
            "encoding": "unreadable",
            "newline": "unknown",
            "sha256_raw": "",
            "sha256_normalized": "",
            "included_in_active_snapshot": False,
            "snapshot_omission_reason": "unreadable_file_omitted",
            "read_error": str(exc),
        }
