#!/usr/bin/env python3
# project-path: tools/validate_freeze_list_frozen_manager_v1.py
"""Compatibility validator for the responsive List Frozen manager."""

from __future__ import annotations

import argparse
from pathlib import Path

from validate_freeze_list_frozen_manager_responsive_v1 import run_validation


def main() -> int:
    """Run current validation under the original feature identity."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--static-only", action="store_true")
    parser.add_argument("--skip-real-qt", action="store_true")
    args = parser.parse_args()
    return run_validation(
        root=Path(args.root).expanduser().resolve(),
        static_only=args.static_only,
        skip_real_qt=args.skip_real_qt,
        feature_id="freeze-list-frozen-manager-v1",
    )


if __name__ == "__main__":
    raise SystemExit(main())
