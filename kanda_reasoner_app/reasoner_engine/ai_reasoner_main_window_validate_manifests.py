# project-path: kanda_reasoner_app/reasoner_engine/ai_reasoner_main_window_validate_manifests.py
"""Validate the canonical main window helper manifest contract.

This validator is intentionally scoped to ai_reasoner_main_window only. It avoids
validating unrelated helper manifests while the reasoner_engine migration is still
being completed in small gates.
"""

from __future__ import annotations

import json
from pathlib import Path

MANIFEST_RELATIVE_PATH = Path(
    "kanda_reasoner_app/reasoner_engine/ai_reasoner_main_window_help.json"
)


__all__ = ["main", "validate_main_window_manifest"]


def _project_root() -> Path:
    """Support project root behavior.
    
    Returns
    -------
    Path
        The resolved path.
    """
    
    return Path(__file__).resolve().parents[2]


def _read_json(path: Path) -> dict:
    """Support read json behavior.
    
    Parameters
    ----------
    path : Path
        The file or folder path.
    
    Returns
    -------
    dict
        The mapped values.
    """
    
    return json.loads(path.read_text(encoding="utf-8-sig"))


def validate_main_window_manifest(project_root: Path | None = None) -> list[str]:
    """Return validation errors for the canonical main window manifest."""
    root = project_root or _project_root()
    manifest_path = root / MANIFEST_RELATIVE_PATH
    errors: list[str] = []

    if not manifest_path.exists():
        return [f"Manifest file missing: {manifest_path}"]

    try:
        manifest = _read_json(manifest_path)
    except json.JSONDecodeError as exc:
        return [f"Invalid JSON in {manifest_path}: {exc}"]

    origin = root / str(manifest.get("origin", ""))
    help_folder = root / str(manifest.get("help_folder", ""))
    helpers = manifest.get("helpers", {})

    if not origin.exists():
        errors.append(f"Origin file missing: {origin}")

    if not help_folder.exists():
        errors.append(f"Help folder missing: {help_folder}")
        return errors

    if not isinstance(helpers, dict) or not helpers:
        errors.append("Manifest helpers section is missing or empty.")
        return errors

    for helper_name in sorted(helpers):
        helper_path = help_folder / helper_name
        if not helper_path.exists():
            errors.append(f"Helper file listed in manifest is missing: {helper_path}")

    return errors


def main() -> int:
    """Support main behavior.
    
    Returns
    -------
    int
        The integer status code.
    """
    
    errors = validate_main_window_manifest()
    manifest_path = _project_root() / MANIFEST_RELATIVE_PATH

    if errors:
        print(f"FAIL - {manifest_path}")
        for error in errors:
            print(f"  - {error}")
        return 1

    print(f"PASS - {manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
