# project-path: kanda_reasoner_app/safety_suite_cli/commands_parsers_private.py
"""Private parser builders for the safety-suite CLI."""

from __future__ import annotations

import argparse

from .commands_actions_private import (
    _cmd_list_tools,
    _cmd_risk_radar,
    _cmd_crash_triage,
    _cmd_refactor_playbook,
    _cmd_release_notes,
    _cmd_push_plan,
    _cmd_stack_brief,
    _cmd_api_contract,
    _cmd_property_test,
    _cmd_bom_scan,
    _cmd_ruff_quality,
    _cmd_shadow_audit,
    _cmd_shadow_plan,
    _cmd_facade_fix_plan,
)

__all__: list[str] = []

def _add_common_output_arguments(parser: argparse.ArgumentParser) -> None:
    """Support add common output arguments behavior.
    
    Parameters
    ----------
    parser : argparse.ArgumentParser
        The parser value.
    """
    
    parser.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
        help="Output format. Default: markdown.",
    )
    parser.add_argument(
        "--output",
        default="",
        help="Optional file path. If omitted, output is printed to stdout.",
    )

def _add_list_tools_parser(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    """Support add list tools parser behavior.
    
    Parameters
    ----------
    subparsers : argparse._SubParsersAction[argparse.ArgumentParser]
        The subparsers value.
    """
    
    parser = subparsers.add_parser("list-tools", help="List available safety tools.")
    parser.set_defaults(func=_cmd_list_tools)

def _add_risk_radar_parser(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    """Support add risk radar parser behavior.
    
    Parameters
    ----------
    subparsers : argparse._SubParsersAction[argparse.ArgumentParser]
        The subparsers value.
    """
    
    parser = subparsers.add_parser("risk-radar", help="Build a Risk Change Radar report.")
    parser.add_argument("--root", required=True, help="Project root.")
    parser.add_argument("--changed-file", action="append", default=[], help="Changed file path.")
    parser.add_argument("--bundle-manifest", default="", help="Bundle manifest text or file path.")
    parser.add_argument("--validation-output", default="", help="Validation output text or file path.")
    parser.add_argument("--evidence", action="append", default=[], help="Extra evidence line.")
    _add_common_output_arguments(parser)
    parser.set_defaults(func=_cmd_risk_radar)

def _add_crash_triage_parser(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    """Support add crash triage parser behavior.
    
    Parameters
    ----------
    subparsers : argparse._SubParsersAction[argparse.ArgumentParser]
        The subparsers value.
    """
    
    parser = subparsers.add_parser("crash-triage", help="Build a Crash Triage report.")
    parser.add_argument("--root", required=True, help="Project root.")
    parser.add_argument("--traceback", default="", help="Traceback text or file path.")
    parser.add_argument("--log", default="", help="Log text or file path.")
    parser.add_argument("--runtime-trace", default="", help="Runtime trace text or file path.")
    parser.add_argument("--evidence", action="append", default=[], help="Extra evidence line.")
    _add_common_output_arguments(parser)
    parser.set_defaults(func=_cmd_crash_triage)

def _add_refactor_playbook_parser(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    """Support add refactor playbook parser behavior.
    
    Parameters
    ----------
    subparsers : argparse._SubParsersAction[argparse.ArgumentParser]
        The subparsers value.
    """
    
    parser = subparsers.add_parser("refactor-playbook", help="Build a Refactor Playbook report.")
    parser.add_argument("--root", required=True, help="Project root.")
    parser.add_argument("--target", required=True, help="Target file to refactor.")
    parser.add_argument("--goal", default="", help="Refactor goal.")
    parser.add_argument("--warning", action="append", default=[], help="Architecture warning.")
    parser.add_argument("--public-symbol", action="append", default=[], help="Public symbol to preserve.")
    parser.add_argument("--dependency", action="append", default=[], help="Known dependency.")
    parser.add_argument("--existing-test", action="append", default=[], help="Existing focused test.")
    parser.add_argument("--constraint", action="append", default=[], help="Box boundary constraint.")
    parser.add_argument("--do-not-touch", action="append", default=[], help="Path or symbol not to touch.")
    parser.add_argument("--evidence", action="append", default=[], help="Extra evidence line.")
    _add_common_output_arguments(parser)
    parser.set_defaults(func=_cmd_refactor_playbook)

def _add_release_notes_parser(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    """Support add release notes parser behavior.
    
    Parameters
    ----------
    subparsers : argparse._SubParsersAction[argparse.ArgumentParser]
        The subparsers value.
    """
    
    parser = subparsers.add_parser("release-notes", help="Build release notes from explicit evidence.")
    parser.add_argument("--bundle-name", required=True, help="Bundle or release name.")
    parser.add_argument("--title", default="", help="Release title.")
    parser.add_argument("--summary", required=True, help="Release summary.")
    parser.add_argument("--status", default="validated", help="Release status.")
    parser.add_argument("--changed-file", action="append", default=[], help="Changed file path.")
    parser.add_argument("--validation-line", action="append", default=[], help="Validation evidence line.")
    _add_common_output_arguments(parser)
    parser.set_defaults(func=_cmd_release_notes)

def _add_push_plan_parser(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    """Support add push plan parser behavior.
    
    Parameters
    ----------
    subparsers : argparse._SubParsersAction[argparse.ArgumentParser]
        The subparsers value.
    """
    
    parser = subparsers.add_parser("push-plan", help="Build an On Every Push validation report.")
    parser.add_argument("--root", required=True, help="Project root.")
    parser.add_argument("--check-output", action="append", default=[], help="name::output evidence.")
    _add_common_output_arguments(parser)
    parser.set_defaults(func=_cmd_push_plan)

def _add_stack_brief_parser(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    """Support add stack brief parser behavior.
    
    Parameters
    ----------
    subparsers : argparse._SubParsersAction[argparse.ArgumentParser]
        The subparsers value.
    """
    
    parser = subparsers.add_parser("stack-brief", help="Build a Stack Compatibility Brief.")
    parser.add_argument("--requirement", action="append", default=[], help="Requirement line.")
    parser.add_argument("--runtime", action="append", default=[], help="Runtime context line.")
    _add_common_output_arguments(parser)
    parser.set_defaults(func=_cmd_stack_brief)

def _add_api_contract_parser(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    """Support add api contract parser behavior.
    
    Parameters
    ----------
    subparsers : argparse._SubParsersAction[argparse.ArgumentParser]
        The subparsers value.
    """
    
    parser = subparsers.add_parser("api-contract", help="Build an API Contract Guard draft.")
    parser.add_argument("--module", required=True, help="Target module path.")
    parser.add_argument("--function", required=True, help="Target function name.")
    parser.add_argument("--param", action="append", default=[], help="Function parameter name.")
    parser.add_argument("--return-hint", default="", help="Return contract hint.")
    parser.add_argument("--failure", action="append", default=[], help="Known failure mode.")
    parser.add_argument("--guard", action="append", default=[], help="Suggested guard.")
    parser.add_argument("--test", action="append", default=[], help="Test to add.")
    _add_common_output_arguments(parser)
    parser.set_defaults(func=_cmd_api_contract)

def _add_property_test_parser(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    """Support add property test parser behavior.
    
    Parameters
    ----------
    subparsers : argparse._SubParsersAction[argparse.ArgumentParser]
        The subparsers value.
    """
    
    parser = subparsers.add_parser("property-test", help="Build a Property Test draft.")
    parser.add_argument("--module", required=True, help="Target module path.")
    parser.add_argument("--function", required=True, help="Target function name.")
    parser.add_argument("--property", action="append", default=[], help="Property to test.")
    parser.add_argument("--strategy", action="append", default=[], help="Input strategy idea.")
    parser.add_argument("--invariant", action="append", default=[], help="Invariant.")
    parser.add_argument("--edge-case", action="append", default=[], help="Edge case.")
    parser.add_argument("--test", action="append", default=[], help="Test to add.")
    _add_common_output_arguments(parser)
    parser.set_defaults(func=_cmd_property_test)

def _add_bom_scan_parser(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    """Support add bom scan parser behavior.
    
    Parameters
    ----------
    subparsers : argparse._SubParsersAction[argparse.ArgumentParser]
        The subparsers value.
    """
    
    parser = subparsers.add_parser("bom-scan", help="Run a read-only BOM scan.")
    parser.add_argument("--root", required=True, help="Project root.")
    parser.add_argument("--suffix", action="append", default=[], help="File suffix to include.")
    _add_common_output_arguments(parser)
    parser.set_defaults(func=_cmd_bom_scan)


def _add_ruff_quality_parser(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
) -> None:
    """Add the read-only Ruff quality command parser."""
    parser = subparsers.add_parser(
        "ruff-quality",
        help="Run read-only Ruff lint and format checks.",
    )
    parser.add_argument("--root", required=True, help="Project root.")
    parser.add_argument(
        "--timeout-seconds",
        type=float,
        default=180.0,
        help="Per-command timeout in seconds. Default: 180.",
    )
    _add_common_output_arguments(parser)
    parser.set_defaults(func=_cmd_ruff_quality)


def _add_shadow_audit_parser(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    """Support add shadow audit parser behavior.
    
    Parameters
    ----------
    subparsers : argparse._SubParsersAction[argparse.ArgumentParser]
        The subparsers value.
    """
    
    parser = subparsers.add_parser("shadow-audit", help="Run a read-only shadow conflict audit.")
    parser.add_argument("--root", required=True, help="Project root.")
    _add_common_output_arguments(parser)
    parser.set_defaults(func=_cmd_shadow_audit)

def _add_shadow_plan_parser(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    """Support add shadow plan parser behavior.
    
    Parameters
    ----------
    subparsers : argparse._SubParsersAction[argparse.ArgumentParser]
        The subparsers value.
    """
    
    parser = subparsers.add_parser("shadow-plan", help="Build a read-only shadow correction plan.")
    parser.add_argument("--root", required=True, help="Project root.")
    _add_common_output_arguments(parser)
    parser.set_defaults(func=_cmd_shadow_plan)

def _add_facade_fix_plan_parser(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    """Support add facade fix plan parser behavior.
    
    Parameters
    ----------
    subparsers : argparse._SubParsersAction[argparse.ArgumentParser]
        The subparsers value.
    """
    
    parser = subparsers.add_parser("facade-fix-plan", help="Build a safe facade-fix dry-run plan.")
    parser.add_argument("--root", required=True, help="Project root.")
    _add_common_output_arguments(parser)
    parser.set_defaults(func=_cmd_facade_fix_plan)
