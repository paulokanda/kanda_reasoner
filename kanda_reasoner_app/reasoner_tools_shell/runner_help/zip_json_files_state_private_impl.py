# project-path: kanda_reasoner_app/reasoner_tools_shell/runner_help/zip_json_files_state_private_impl.py
"""State and ZIP-size preference helpers for Tab 4 JSON ZIP export."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

__all__ = []


DEFAULT_ZIP_SIZE_MB = 500
EXTENDED_ZIP_SIZE_MB_OPTIONS = (100, 200, 300, 400, 500)
ALLOWED_ZIP_SIZE_MB_OPTIONS = EXTENDED_ZIP_SIZE_MB_OPTIONS
STATUS_FILE_NAME = '_RUN_COLLECTOR_STATUS.txt'

def _prefs_path() -> Path:
    """Support prefs path behavior.
    
    Returns
    -------
    Path
        The resolved path.
    """
    
    return Path(__file__).resolve().parent / '.zip_json_export_prefs.json'


def _load_prefs_payload() -> dict[str, Any]:
    """Support load prefs payload behavior.
    
    Returns
    -------
    dict[str, Any]
        The mapped values.
    """
    
    try:
        prefs_path = _prefs_path()
        if prefs_path.exists():
            payload = json.loads(prefs_path.read_text(encoding='utf-8'))
            if isinstance(payload, dict):
                return payload
    except Exception:
        pass
    return {}


def _save_prefs_payload(payload: dict[str, Any]) -> None:
    """Support save prefs payload behavior.
    
    Parameters
    ----------
    payload : dict[str, Any]
        The payload value.
    """
    
    try:
        prefs_path = _prefs_path()
        prefs_path.parent.mkdir(parents=True, exist_ok=True)
        prefs_path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding='utf-8')
    except Exception:
        pass


def _load_destination() -> str:
    """Support load destination behavior.
    
    Returns
    -------
    str
        The string result.
    """
    
    payload = _load_prefs_payload()
    destination = str(payload.get('destination_folder', '')).strip()
    return destination


def _save_destination(destination_folder: str) -> None:
    """Support save destination behavior.
    
    Parameters
    ----------
    destination_folder : str
        The destination folder value.
    """
    
    payload = _load_prefs_payload()
    payload['destination_folder'] = destination_folder
    _save_prefs_payload(payload)


def load_saved_part_size_mb() -> int:
    """Return the saved ZIP part-size preference or the default 500 MB."""
    payload = _load_prefs_payload()
    try:
        value = int(payload.get('part_size_mb', DEFAULT_ZIP_SIZE_MB))
    except Exception:
        value = DEFAULT_ZIP_SIZE_MB
    if value in ALLOWED_ZIP_SIZE_MB_OPTIONS:
        return value
    return DEFAULT_ZIP_SIZE_MB


def save_selected_part_size_mb(part_size_mb: int) -> None:
    """Persist the user's selected ZIP part-size option for next session."""
    value = int(part_size_mb)
    if value not in ALLOWED_ZIP_SIZE_MB_OPTIONS:
        value = DEFAULT_ZIP_SIZE_MB
    payload = _load_prefs_payload()
    payload['part_size_mb'] = value
    _save_prefs_payload(payload)


def selected_part_size_mb(window: Any) -> int:
    """Return and persist the selected ZIP size option for the collector tab."""
    radio_by_size = ((100, 'zip_size_100_radio'), (200, 'zip_size_200_radio'), (300, 'zip_size_300_radio'), (400, 'zip_size_400_radio'), (500, 'zip_size_500_radio'))
    for size_mb, attribute in radio_by_size:
        try:
            if bool(getattr(window, attribute).isChecked()):
                save_selected_part_size_mb(size_mb)
                return size_mb
        except Exception:
            pass
    saved = load_saved_part_size_mb()
    save_selected_part_size_mb(saved)
    return saved


def _selected_part_size_mb(window: Any) -> int:
    """Support selected part size mb behavior.
    
    Parameters
    ----------
    window : Any
        The window value.
    
    Returns
    -------
    int
        The integer result.
    """
    
    return selected_part_size_mb(window)

