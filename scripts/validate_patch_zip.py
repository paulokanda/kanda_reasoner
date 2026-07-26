# project-path: scripts/validate_patch_zip.py
"""Command-line wrapper for the KANDA patch ZIP contract validator."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Sequence


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _ensure_project_root_on_path() -> None:
    """Add the project root only when this command is executed."""
    project_root_text = str(PROJECT_ROOT)
    if project_root_text not in sys.path:
        sys.path.insert(0, project_root_text)


def main(argv: Sequence[str] | None = None) -> int:
    """Run the patch ZIP validator without mutating import state at import time."""
    _ensure_project_root_on_path()
    from kanda_reasoner_app.patch_governance.validator import main as validator_main

    return int(validator_main(argv))


if __name__ == "__main__":
    raise SystemExit(main())
