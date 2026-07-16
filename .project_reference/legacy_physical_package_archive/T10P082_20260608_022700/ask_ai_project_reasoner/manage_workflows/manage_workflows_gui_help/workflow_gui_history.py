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
            json.dumps(data, indent=2, ensure_ascii=False) + "\n",
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


def get_recent_roots() -> list[str]:
    """Merge recent roots from both CLI history files, most recent first."""
    wf = _get_roots_from_file(_WORKFLOW_HISTORY_FILE)
    arch = _get_roots_from_file(_ARCHITECTURE_HISTORY_FILE)
    gui = _get_roots_from_file(_GUI_HISTORY_FILE)
    seen: set[str] = set()
    merged: list[str] = []
    for r in gui + wf + arch:
        if r not in seen:
            seen.add(r)
            merged.append(r)
    return merged[:_HISTORY_MAX]


def record_root(root: str) -> None:
    _record_root_to_file(_GUI_HISTORY_FILE, root)


def get_recent_scripts() -> list[str]:
    return _load_json_file(_GUI_HISTORY_FILE).get("scripts", [])


def record_script(script: str) -> None:
    data = _load_json_file(_GUI_HISTORY_FILE)
    scripts: list[str] = [s for s in data.get("scripts", []) if s != script]
    scripts.insert(0, script)
    data["scripts"] = scripts[:_HISTORY_MAX]
    _save_json_file(_GUI_HISTORY_FILE, data)
