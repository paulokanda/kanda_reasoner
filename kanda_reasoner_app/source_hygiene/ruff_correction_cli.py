# project-path: kanda_reasoner_app/source_hygiene/ruff_correction_cli.py
"""Standalone CLI for reviewed Ruff correction preview and apply transactions."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Sequence

from .ruff_correction_apply import (
    apply_ruff_correction_preview,
    load_ruff_correction_preview,
)
from .ruff_correction_errors import (
    RuffCorrectionApplyError,
    RuffCorrectionPreviewError,
)
from .ruff_correction_preview import create_ruff_correction_preview

__all__ = ["build_parser", "main"]


def build_parser() -> argparse.ArgumentParser:
    """Build the standalone Ruff correction workflow parser."""
    parser = argparse.ArgumentParser(
        prog="kanda-ruff-correction",
        description=(
            "Create reviewed Ruff-safe correction previews and apply one "
            "preview only after exact human confirmation."
        ),
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    preview = subparsers.add_parser(
        "preview",
        help="Create a durable diff without modifying active project source.",
    )
    preview.add_argument("--project-root", required=True)
    preview.add_argument(
        "--path",
        action="append",
        default=[],
        help="Optional project-relative file or directory. Repeat as needed.",
    )
    preview.add_argument("--max-files", type=int, default=100)
    preview.add_argument("--timeout-seconds", type=float, default=180.0)
    preview.add_argument("--ruff-executable", default="")
    preview.set_defaults(handler=_run_preview)

    show = subparsers.add_parser(
        "show",
        help="Show one durable preview manifest and exact unified diff.",
    )
    show.add_argument("--project-root", required=True)
    show.add_argument("--preview-id", required=True)
    show.set_defaults(handler=_run_show)

    apply_parser = subparsers.add_parser(
        "apply",
        help="Apply one reviewed preview with backup, validation, and rollback.",
    )
    apply_parser.add_argument("--project-root", required=True)
    apply_parser.add_argument("--preview-id", required=True)
    apply_parser.add_argument("--confirm-token", required=True)
    apply_parser.add_argument("--timeout-seconds", type=float, default=180.0)
    apply_parser.add_argument("--ruff-executable", default="")
    apply_parser.set_defaults(handler=_run_apply)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the standalone command and return an operating-system exit code."""
    parser = build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)
    try:
        return int(args.handler(args))
    except (RuffCorrectionPreviewError, RuffCorrectionApplyError, ValueError) as exc:
        print("RUFF CORRECTION BLOCKED", file=sys.stderr)
        print(str(exc), file=sys.stderr)
        return 2
    except Exception as exc:
        print("RUFF CORRECTION FAILED", file=sys.stderr)
        print(str(exc), file=sys.stderr)
        return 1


def _run_preview(args: argparse.Namespace) -> int:
    """Create and print one correction preview record."""
    record = create_ruff_correction_preview(
        args.project_root,
        scope_paths=tuple(args.path or ()),
        max_files=args.max_files,
        ruff_argv_prefix=_ruff_prefix(args.ruff_executable),
        timeout_seconds=args.timeout_seconds,
    )
    _print_json(record.to_dict())
    if record.status == "PREVIEW_READY":
        print("\nREVIEW REQUIRED")
        print("Preview ID: " + record.preview_id)
        print("Diff: " + record.diff_path)
        print("Confirm token: " + record.confirm_token)
    else:
        print("\nNo Ruff-safe correction changes were found.")
    return 0


def _run_show(args: argparse.Namespace) -> int:
    """Print one preview manifest followed by its exact diff."""
    record = load_ruff_correction_preview(args.project_root, args.preview_id)
    _print_json(record.to_dict())
    diff_path = Path(record.diff_path)
    print("\nEXACT DIFF")
    print(diff_path.read_text(encoding="utf-8", errors="strict"), end="")
    return 0


def _run_apply(args: argparse.Namespace) -> int:
    """Apply one preview and print the durable transaction receipt."""
    receipt = apply_ruff_correction_preview(
        args.project_root,
        args.preview_id,
        confirm_token=args.confirm_token,
        ruff_argv_prefix=_ruff_prefix(args.ruff_executable),
        timeout_seconds=args.timeout_seconds,
    )
    _print_json(receipt.to_dict())
    print("\nRUFF CORRECTION APPLY STATUS: " + receipt.status)
    print("Receipt: " + receipt.receipt_path)
    if receipt.status == "PROPOSAL_ONLY":
        print("Project source was not mutated.")
        return 0
    return 0 if receipt.status == "APPLIED" else 2


def _ruff_prefix(executable: str) -> tuple[str, ...] | None:
    """Return an explicit Ruff command prefix when supplied."""
    value = str(executable or "").strip()
    return (value,) if value else None


def _print_json(value: dict[str, object]) -> None:
    """Print stable ASCII JSON for review and automation."""
    print(json.dumps(value, ensure_ascii=True, indent=2, sort_keys=True))


if __name__ == "__main__":
    raise SystemExit(main())
