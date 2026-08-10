# project-path: kanda_reasoner_app/safety_suite_cli/commands.py
"""CLI facade for Kanda Reasoner safety-suite tools.

The CLI owns argument parsing and presentation only. Tool logic remains in the
backend boxes: source_hygiene, engineering_safety, governance_automation,
stack_compatibility, and reliability_guidance.
"""

from __future__ import annotations

import argparse
import sys
from typing import TextIO

__all__ = [
    "available_cli_commands",
    "build_safety_suite_parser",
    "main",
    "run_cli",
]


def available_cli_commands() -> tuple[str, ...]:
    """Return stable command names exposed by the safety-suite CLI."""
    return _available_cli_commands()


def build_safety_suite_parser() -> argparse.ArgumentParser:
    """Build the top-level safety-suite argument parser."""
    parser = argparse.ArgumentParser(
        prog="kanda-safety-suite",
        description="Run Kanda Reasoner safety tools without opening the GUI.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    _add_list_tools_parser(subparsers)
    _add_risk_radar_parser(subparsers)
    _add_crash_triage_parser(subparsers)
    _add_refactor_playbook_parser(subparsers)
    _add_release_notes_parser(subparsers)
    _add_push_plan_parser(subparsers)
    _add_stack_brief_parser(subparsers)
    _add_api_contract_parser(subparsers)
    _add_property_test_parser(subparsers)
    _add_bom_scan_parser(subparsers)
    _add_ruff_quality_parser(subparsers)
    _add_shadow_audit_parser(subparsers)
    _add_shadow_plan_parser(subparsers)
    _add_facade_fix_plan_parser(subparsers)
    from kanda_reasoner_app.safety_suite_cli.project_symbol_atlas_commands import add_reasoner_symbol_atlas_parsers
    add_reasoner_symbol_atlas_parsers(subparsers)
    return parser


def run_cli(
    argv: list[str] | None = None,
    stdout: TextIO | None = None,
    stderr: TextIO | None = None,
) -> int:
    """Run the safety-suite CLI and return a process-style status code."""
    out = stdout or sys.stdout
    err = stderr or sys.stderr
    parser = build_safety_suite_parser()
    try:
        args = parser.parse_args(argv)
        return int(args.func(args, out, err))
    except BrokenPipeError:
        return 1
    except Exception as exc:  # noqa: BLE001 - CLI boundary converts exceptions.
        err.write("ERROR: " + str(exc) + "\n")
        return 2


def main(argv: list[str] | None = None) -> int:
    """Console-script compatible entry point."""
    return run_cli(argv)

from .commands_catalog_private import _available_cli_commands
from .commands_parsers_private import (
    _add_list_tools_parser,
    _add_risk_radar_parser,
    _add_crash_triage_parser,
    _add_refactor_playbook_parser,
    _add_release_notes_parser,
    _add_push_plan_parser,
    _add_stack_brief_parser,
    _add_api_contract_parser,
    _add_property_test_parser,
    _add_bom_scan_parser,
    _add_ruff_quality_parser,
    _add_shadow_audit_parser,
    _add_shadow_plan_parser,
    _add_facade_fix_plan_parser,
)
