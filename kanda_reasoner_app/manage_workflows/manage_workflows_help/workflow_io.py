# project-path: kanda_reasoner_app/manage_workflows/manage_workflows_help/workflow_io.py
"""Own text IO, preferences loading, and generated-output comparison helpers."""

from __future__ import annotations

import difflib
import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path

from .workflow_constants import (
    MANAGED_BY,
    WORKFLOW_MANIFEST_NAME,
)

__all__ = [
]

def _get_prefs_path() -> Path | None:
    """Locate .reasoner_tools_gui_prefs.json by walking up from this file."""
    current = Path(__file__).resolve().parent
    for _ in range(10):  # limit ascent
        candidate = current / ".reasoner_tools_gui_prefs.json"
        if candidate.exists():
            return candidate
        if current.parent == current:
            break
        current = current.parent
    return None

def load_ignore_rules() -> tuple[list[str], list[str], list[str]]:
    """Load ignore folders, files, extensions from the GUI prefs file."""
    prefs_path = _get_prefs_path()
    if not prefs_path:
        return [], [], []
    try:
        data = json.loads(prefs_path.read_text(encoding="utf-8"))
        rules = data.get("ignore_rules", {})
        folders = rules.get("folders", [])
        files = rules.get("files", [])
        extensions = rules.get("extensions", [])
        return folders, files, extensions
    except Exception:
        return [], [], []

def utc_now_iso() -> str:
    """Support utc now iso behavior.
    
    Returns
    -------
    str
        The string result.
    """
    
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()

def read_text(path: Path) -> str:
    """Return the text.
    
    Parameters
    ----------
    path : Path
        The file or folder path.
    
    Returns
    -------
    str
        The string result.
    """
    
    return path.read_text(encoding="utf-8-sig")

def write_text_if_changed(path: Path, content: str) -> bool:
    """Atomically write changed managed text after validating JSON payloads."""
    current = read_text(path) if path.exists() else None
    if current == content:
        return False

    if path.name == WORKFLOW_MANIFEST_NAME:
        try:
            payload = json.loads(content)
        except json.JSONDecodeError as exc:
            raise ValueError(
                f"Refusing to write invalid {WORKFLOW_MANIFEST_NAME}: {exc}"
            ) from exc
        if not isinstance(payload, dict):
            raise ValueError(
                f"Refusing to write {WORKFLOW_MANIFEST_NAME}: root must be an object."
            )

    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            newline="\n",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
            temporary_path = Path(handle.name)

        if path.name == WORKFLOW_MANIFEST_NAME:
            validated = json.loads(read_text(temporary_path))
            if not isinstance(validated, dict):
                raise ValueError(
                    f"Temporary {WORKFLOW_MANIFEST_NAME} root must be an object."
                )

        os.replace(temporary_path, path)
        temporary_path = None
        return True
    finally:
        if temporary_path is not None and temporary_path.exists():
            temporary_path.unlink()


def diff_text(current: str, desired: str, fromfile: str, tofile: str) -> str:
    """Support diff text behavior.
    
    Parameters
    ----------
    current : str
        The current value.
    desired : str
        The desired value.
    fromfile : str
        The fromfile value.
    tofile : str
        The tofile value.
    
    Returns
    -------
    str
        The string result.
    """
    
    return "".join(
        difflib.unified_diff(
            current.splitlines(keepends=True),
            desired.splitlines(keepends=True),
            fromfile=fromfile,
            tofile=tofile,
        )
    )

def normalize_generated_output_for_diff(path: Path, text: str) -> str:
    """Normalize the generated output for diff.
    
    Parameters
    ----------
    path : Path
        The file or folder path.
    text : str
        The text value.
    
    Returns
    -------
    str
        The string result.
    """
    
    if path.name != WORKFLOW_MANIFEST_NAME:
        return text
    try:
        data = json.loads(text)
    except Exception:
        return text
    if isinstance(data, dict) and "generated_at_utc" in data:
        data["generated_at_utc"] = "<normalized>"
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n"

def should_generate_json_manifest(path: Path) -> bool:
    """Support should generate json manifest behavior.
    
    Parameters
    ----------
    path : Path
        The file or folder path.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    if not path.exists():
        return True
    try:
        data = json.loads(read_text(path))
    except Exception:
        return False
    return isinstance(data, dict) and data.get("managed_by") == MANAGED_BY

def should_generate_workflows_doc(path: Path) -> bool:
    """Support should generate workflows doc behavior.
    
    Parameters
    ----------
    path : Path
        The file or folder path.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    if not path.exists():
        return True
    text = read_text(path)
    return text.lstrip().startswith("# WORKFLOWS") and "Generated by manage_workflows.py." in text
