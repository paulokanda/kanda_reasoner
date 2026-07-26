# project-path: scripts/migrate_freeze_after_update_external_root.py
"""CLI for safe Freeze Feature After Update external-state migration."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


def _project_root_from_script() -> Path:
    """Return project root when this script runs from scripts/."""
    return Path(__file__).resolve().parents[1]


def _ensure_project_on_path(project_root: Path) -> None:
    """Ensure local project modules can be imported."""
    text = str(project_root)
    if text not in sys.path:
        sys.path.insert(0, text)


def main(argv: list[str] | None = None) -> int:
    """Run safe freeze-state migration."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=None)
    parser.add_argument("--clean-legacy", action="store_true")
    args = parser.parse_args(argv)

    project_root = args.project_root.expanduser().resolve(strict=False) if args.project_root else _project_root_from_script()
    _ensure_project_on_path(project_root)

    from kanda_reasoner_app.freeze_after_update.migration import migrate_freeze_after_update_state

    result = migrate_freeze_after_update_state(project_root, clean_legacy=bool(args.clean_legacy))
    print(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))
    if not result.ok:
        print("VALIDATION FAILED: freeze-state external root migration")
        return 1
    print("VALIDATION OK: freeze-state external root migration")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
