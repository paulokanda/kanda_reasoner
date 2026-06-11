"""Recent-root and worker-script history for the workflow manager GUI."""

from __future__ import annotations

import json
from pathlib import Path

_WORKFLOW_HISTORY_FILE = Path.home() / ".manage_workflows_history.json"
_ARCHITECTURE_HISTORY_FILE = Path.home() / ".manage_architecture_history.json"
_GUI_HISTORY_FILE = Path.home() / ".manage_gui_history.json"
_HISTORY_MAX = 10

__all__ = [
    "get_recent_roots",
    "get_default_script_path",
    "get_recent_scripts",
    "record_root",
    "record_script",
]


def _load_json_file(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def _save_json_file(path: Path, data: dict) -> None:
    try:
        path.write_text(
            json.dumps(data, indent=2, ensure_ascii=True) + "\n",
            encoding="utf-8",
        )
    except Exception:
        pass


def _get_roots_from_file(history_file: Path) -> list[str]:
    return _load_json_file(history_file).get("roots", [])


def _record_root_to_file(history_file: Path, root: str) -> None:
    data = _load_json_file(history_file)
    roots: list[str] = [r for r in data.get("roots", []) if r != root]
    roots.insert(0, root)
    data["roots"] = roots[:_HISTORY_MAX]
    _save_json_file(history_file, data)


def get_default_script_path() -> str:
    """Return the canonical Tab 2 workflow worker script path."""
    return str(Path(__file__).resolve().parents[1] / "manage_workflows.py")


def _existing_script_paths(paths: list[str]) -> list[str]:
    """Return existing Python script paths while preserving order."""
    existing: list[str] = []
    seen: set[str] = set()

    for item in paths:
        path_text = str(item).strip()
        if not path_text or path_text in seen:
            continue

        path = Path(path_text)
        if path.suffix.lower() != ".py":
            continue
        if not path.exists():
            continue

        seen.add(path_text)
        existing.append(path_text)

    return existing


def get_recent_roots() -> list[str]:
    """Merge recent roots from both CLI history files, most recent first."""
    wf = _get_roots_from_file(_WORKFLOW_HISTORY_FILE)
    arch = _get_roots_from_file(_ARCHITECTURE_HISTORY_FILE)
    gui = _get_roots_from_file(_GUI_HISTORY_FILE)
    seen: set[str] = set()
    merged: list[str] = []
    for root in gui + wf + arch:
        if root not in seen:
            seen.add(root)
            merged.append(root)
    return merged[:_HISTORY_MAX]


def record_root(root: str) -> None:
    _record_root_to_file(_GUI_HISTORY_FILE, root)


def get_recent_scripts(history_file: Path | None = None) -> list[str]:
    """Return canonical Tab 2 worker first, followed by valid history paths.

    Old absolute paths from previous projects must not become the default
    worker script. This keeps Tab 2 project-agnostic after folder renames.
    """
    source_file = history_file if history_file is not None else _GUI_HISTORY_FILE
    canonical_script = get_default_script_path()
    history_scripts = _load_json_file(source_file).get("scripts", [])
    ordered = [canonical_script] + [str(item) for item in history_scripts]
    return _existing_script_paths(ordered)[:_HISTORY_MAX]


def record_script(script: str) -> None:
    data = _load_json_file(_GUI_HISTORY_FILE)
    scripts: list[str] = [s for s in data.get("scripts", []) if s != script]
    scripts.insert(0, script)
    data["scripts"] = scripts[:_HISTORY_MAX]
    _save_json_file(_GUI_HISTORY_FILE, data)
