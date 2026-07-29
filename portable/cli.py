"""Command-line facade for KANDA Reasoner Portable creation."""

from __future__ import annotations

import argparse
from pathlib import Path

from portable.workflow import run


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Create KANDA Reasoner Windows Portable outside the project "
            "and outside Show Project to AI."
        )
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        help=(
            "Use this existing destination folder instead of opening the "
            "native Windows folder picker."
        ),
    )
    parser.add_argument(
        "--replace-existing",
        action="store_true",
        help=(
            "Replace an existing selected-folder Portable only after an "
            "additional typed confirmation."
        ),
    )
    parser.add_argument(
        "--yes",
        action="store_true",
        help=(
            "Treat this explicit invocation as the initial build "
            "authorization. GUI smoke confirmation remains required."
        ),
    )
    parser.add_argument(
        "--keep-staging",
        action="store_true",
        help="Keep transient build files after successful publication.",
    )
    return parser.parse_args()


def main(*, project_root: Path) -> int:
    """Run the public Portable command."""

    return run(project_root=project_root, args=_parse_args())
