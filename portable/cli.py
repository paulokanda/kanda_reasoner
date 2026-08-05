"""Command-line facade for KANDA Reasoner Portable creation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from portable.constants import (
    BUILDER_MEMBER_FEATURE_ID,
    BUILDER_VERSION,
    EXTERNAL_CONTROL_FEATURE_ID,
    FEATURE_ID,
    PORTABLE_HARDENING_FEATURES,
    PORTABLE_HARDENING_STAGE,
    PRODUCTION_PORTABLE_ENABLED,
)
from portable.workflow import run


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Create KANDA Reasoner Windows Portable outside the project "
            "and outside Show Project to AI."
        )
    )
    parser.add_argument(
        "--version",
        action="version",
        version=(
            f"PORTABLE BUILDER VERSION: {BUILDER_VERSION}\n"
            f"PORTABLE BUILDER FEATURE ID: {FEATURE_ID}"
        ),
    )
    parser.add_argument(
        "--identity-json",
        action="store_true",
        help=(
            "Print one compact machine-readable identity JSON object "
            "and exit without building."
        ),
    )
    parser.add_argument(
        "--result-json",
        type=Path,
        help=(
            "Write an atomic machine-readable build result outside the "
            "project and Project Support."
        ),
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
        help=(
            "Keep transient build files after successful publication."
        ),
    )
    return parser.parse_args()


def _identity_json() -> str:
    return json.dumps(
        {
            "schema_version": "1.0",
            "builder_member_feature_id": BUILDER_MEMBER_FEATURE_ID,
            "builder_version": BUILDER_VERSION,
            "external_control_feature_id": EXTERNAL_CONTROL_FEATURE_ID,
            "feature_id": FEATURE_ID,
            "hardening_features": list(PORTABLE_HARDENING_FEATURES),
            "hardening_stage": PORTABLE_HARDENING_STAGE,
            "production_portable_enabled": PRODUCTION_PORTABLE_ENABLED,
        },
        separators=(",", ":"),
        sort_keys=True,
    )


def main(*, project_root: Path) -> int:
    """Run the public Portable command."""

    args = _parse_args()
    if args.identity_json:
        print(_identity_json())
        return 0
    return run(
        project_root=project_root,
        args=args,
    )
