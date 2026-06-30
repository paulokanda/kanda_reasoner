# project-path: kanda_reasoner_app/reasoner_context_bundle/cli.py
"""Command-line entry point for additive AI context bundle generation."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Sequence

from .bundle_orchestrator import generate_ai_context_bundle
from .validation_state_builder import run_validation_commands

__all__ = ["main"]


def _build_parser() -> argparse.ArgumentParser:
    """Build the reasoner-context-bundle command-line parser."""
    parser = argparse.ArgumentParser(
        description="Generate additive AI context bundle companion JSON files."
    )
    parser.add_argument(
        "--root",
        default=".",
        help="Active project root. Defaults to the current directory.",
    )
    parser.add_argument(
        "--write",
        action="store_true",
        help="Generate the companion JSON bundle.",
    )
    parser.add_argument(
        "--no-check",
        action="store_true",
        help="Skip the bundle checker after writing companion files.",
    )
    parser.add_argument(
        "--compact",
        action="store_true",
        help="Print compact JSON instead of indented JSON.",
    )
    parser.add_argument(
        "--run-validation",
        action="store_true",
        help="Run local deterministic validation commands and record their results. This is now the default for handoff generation.",
    )
    parser.add_argument(
        "--skip-validation",
        action="store_true",
        help="Skip local validation capture and write validation_state as not_run.",
    )
    parser.add_argument(
        "--include-optional-validation",
        action="store_true",
        help="Also run optional validation commands such as architecture diff.",
    )
    return parser


def _print_result(result: dict[str, object], compact: bool) -> None:
    """Support print result behavior.
    
    Parameters
    ----------
    result : dict[str, object]
        The result value.
    compact : bool
        The compact value.
    """
    
    if compact:
        print(json.dumps(result, sort_keys=True), flush=True)
    else:
        print(json.dumps(result, indent=2, sort_keys=True), flush=True)


def main(argv: Sequence[str] | None = None) -> int:
    """Run the reasoner-context-bundle CLI."""
    parser = _build_parser()
    args = parser.parse_args(argv)

    if not args.write:
        parser.print_help()
        return 2

    try:
        project_root = Path(args.root).expanduser().resolve()
        command_results = None
        commands_run_by_bundle = False
        should_run_validation = bool(args.run_validation) or not bool(args.skip_validation)
        if should_run_validation:
            command_results = run_validation_commands(
                project_root,
                include_optional=bool(args.include_optional_validation),
            )
            commands_run_by_bundle = True
        result = generate_ai_context_bundle(
            project_root,
            command_results=command_results,
            check_bundle=not bool(args.no_check),
            commands_run_by_bundle=commands_run_by_bundle,
        )
    except Exception as exc:
        result = {
            "ok": False,
            "project_root_marker": "<PROJECT_ROOT>",
            "error": str(exc),
            "failures": [str(exc)],
        }
        _print_result(result, bool(args.compact))
        return 1

    _print_result(result, bool(args.compact))
    return 0 if bool(result.get("ok")) else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
