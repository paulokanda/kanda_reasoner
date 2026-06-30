# project-path: kanda_reasoner_app/json_splitter/json_splitter_8_validate_manifests.py
"""Validate the json_splitter_8 helper split."""

from __future__ import annotations

import json
from pathlib import Path

__all__ = ["main"]


def _line_count(path: Path) -> int:
    """Support line count behavior.
    
    Parameters
    ----------
    path : Path
        The file or folder path.
    
    Returns
    -------
    int
        The integer result.
    """
    
    if not path.exists():
        return 0
    text = path.read_text(encoding="utf-8", errors="replace")
    if not text:
        return 0
    return len(text.splitlines())


def main() -> int:
    """Support main behavior.
    
    Returns
    -------
    int
        The integer status code.
    """
    
    root = Path(__file__).resolve().parent
    manifest_path = root / "json_splitter_8_help.json"
    helper_dir = root / "json_splitter_8_help"
    errors = []

    if not manifest_path.exists():
        errors.append("missing manifest: " + str(manifest_path))
    if not helper_dir.exists():
        errors.append("missing helper directory: " + str(helper_dir))

    if manifest_path.exists():
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
        for filename in data.get("files", []):
            path = helper_dir / filename
            if not path.exists():
                errors.append("missing helper file: " + str(path))
            elif _line_count(path) >= 500:
                errors.append("helper file has 500 or more lines: " + str(path))

    origin = root / "json_splitter_8.py"
    if not origin.exists():
        errors.append("missing origin file: " + str(origin))
    elif _line_count(origin) >= 500:
        errors.append("origin file has 500 or more lines: " + str(origin))

    if errors:
        for error in errors:
            print("FAIL " + error)
        return 1

    print("PASS json_splitter_8 helper manifest")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
