"""CLI facade for Kanda Reasoner safety-suite tools.

The CLI owns argument parsing and presentation only. Tool logic remains in the
backend boxes: source_hygiene, engineering_safety, governance_automation,
stack_compatibility, and reliability_guidance.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, TextIO

__all__ = [
    "available_cli_commands",
    "build_safety_suite_parser",
    "main",
    "run_cli",
]


def available_cli_commands() -> tuple[str, ...]:
    """Return stable command names exposed by the safety-suite CLI."""
    return (
        "api-contract",
        "bom-scan",
        "crash-triage",
        "atlas-report",
        "evidence-freshness",
        "facade-fix-plan",
        "facade-owner",
        "find-owner",
        "find-symbol",
        "list-tools",
        "logic-placement",
        "main-helpers",
        "pre-patch-gate",
        "property-test",
        "push-plan",
        "refactor-playbook",
        "release-notes",
        "risk-radar",
        "shadow-audit",
        "related-files",
        "shadow-plan",
        "stack-brief",
        "symbol-atlas",
    )


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


def _add_common_output_arguments(parser: argparse.ArgumentParser) -> None:
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
    parser = subparsers.add_parser("list-tools", help="List available safety tools.")
    parser.set_defaults(func=_cmd_list_tools)


def _add_risk_radar_parser(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    parser = subparsers.add_parser("risk-radar", help="Build a Risk Change Radar report.")
    parser.add_argument("--root", required=True, help="Project root.")
    parser.add_argument("--changed-file", action="append", default=[], help="Changed file path.")
    parser.add_argument("--bundle-manifest", default="", help="Bundle manifest text or file path.")
    parser.add_argument("--validation-output", default="", help="Validation output text or file path.")
    parser.add_argument("--evidence", action="append", default=[], help="Extra evidence line.")
    _add_common_output_arguments(parser)
    parser.set_defaults(func=_cmd_risk_radar)


def _add_crash_triage_parser(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    parser = subparsers.add_parser("crash-triage", help="Build a Crash Triage report.")
    parser.add_argument("--root", required=True, help="Project root.")
    parser.add_argument("--traceback", default="", help="Traceback text or file path.")
    parser.add_argument("--log", default="", help="Log text or file path.")
    parser.add_argument("--runtime-trace", default="", help="Runtime trace text or file path.")
    parser.add_argument("--evidence", action="append", default=[], help="Extra evidence line.")
    _add_common_output_arguments(parser)
    parser.set_defaults(func=_cmd_crash_triage)


def _add_refactor_playbook_parser(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
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
    parser = subparsers.add_parser("push-plan", help="Build an On Every Push validation report.")
    parser.add_argument("--root", required=True, help="Project root.")
    parser.add_argument("--check-output", action="append", default=[], help="name::output evidence.")
    _add_common_output_arguments(parser)
    parser.set_defaults(func=_cmd_push_plan)


def _add_stack_brief_parser(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    parser = subparsers.add_parser("stack-brief", help="Build a Stack Compatibility Brief.")
    parser.add_argument("--requirement", action="append", default=[], help="Requirement line.")
    parser.add_argument("--runtime", action="append", default=[], help="Runtime context line.")
    _add_common_output_arguments(parser)
    parser.set_defaults(func=_cmd_stack_brief)


def _add_api_contract_parser(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
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
    parser = subparsers.add_parser("bom-scan", help="Run a read-only BOM scan.")
    parser.add_argument("--root", required=True, help="Project root.")
    parser.add_argument("--suffix", action="append", default=[], help="File suffix to include.")
    _add_common_output_arguments(parser)
    parser.set_defaults(func=_cmd_bom_scan)


def _add_shadow_audit_parser(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    parser = subparsers.add_parser("shadow-audit", help="Run a read-only shadow conflict audit.")
    parser.add_argument("--root", required=True, help="Project root.")
    _add_common_output_arguments(parser)
    parser.set_defaults(func=_cmd_shadow_audit)


def _add_shadow_plan_parser(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    parser = subparsers.add_parser("shadow-plan", help="Build a read-only shadow correction plan.")
    parser.add_argument("--root", required=True, help="Project root.")
    _add_common_output_arguments(parser)
    parser.set_defaults(func=_cmd_shadow_plan)


def _add_facade_fix_plan_parser(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    parser = subparsers.add_parser("facade-fix-plan", help="Build a safe facade-fix dry-run plan.")
    parser.add_argument("--root", required=True, help="Project root.")
    _add_common_output_arguments(parser)
    parser.set_defaults(func=_cmd_facade_fix_plan)


def _cmd_list_tools(args: argparse.Namespace, stdout: TextIO, stderr: TextIO) -> int:
    del args, stderr
    for command in available_cli_commands():
        stdout.write(command + "\n")
    return 0


def _cmd_risk_radar(args: argparse.Namespace, stdout: TextIO, stderr: TextIO) -> int:
    del stderr
    from kanda_reasoner_app.engineering_safety.report_writer import (
        format_engineering_safety_markdown,
    )
    from kanda_reasoner_app.engineering_safety.risk_radar import (
        RiskChangeRadarInput,
        build_risk_change_radar_report,
    )

    report = build_risk_change_radar_report(
        RiskChangeRadarInput(
            project_root=args.root,
            changed_files=list(args.changed_file or []),
            bundle_manifest_text=_read_text_or_literal(args.bundle_manifest),
            validation_output_text=_read_text_or_literal(args.validation_output),
            extra_evidence=list(args.evidence or []),
        )
    )
    return _emit_report(report.to_dict(), format_engineering_safety_markdown(report), args, stdout)


def _cmd_crash_triage(args: argparse.Namespace, stdout: TextIO, stderr: TextIO) -> int:
    del stderr
    from kanda_reasoner_app.engineering_safety.crash_triage import (
        CrashTriageInput,
        build_crash_triage_report,
    )
    from kanda_reasoner_app.engineering_safety.report_writer import (
        format_engineering_safety_markdown,
    )

    report = build_crash_triage_report(
        CrashTriageInput(
            project_root=args.root,
            traceback_text=_read_text_or_literal(args.traceback),
            log_text=_read_text_or_literal(args.log),
            runtime_trace_text=_read_text_or_literal(args.runtime_trace),
            extra_evidence=list(args.evidence or []),
        )
    )
    return _emit_report(report.to_dict(), format_engineering_safety_markdown(report), args, stdout)


def _cmd_refactor_playbook(args: argparse.Namespace, stdout: TextIO, stderr: TextIO) -> int:
    del stderr
    from kanda_reasoner_app.engineering_safety.refactor_playbook import (
        RefactorPlaybookInput,
        build_refactor_playbook_report,
    )
    from kanda_reasoner_app.engineering_safety.report_writer import (
        format_engineering_safety_markdown,
    )

    report = build_refactor_playbook_report(
        RefactorPlaybookInput(
            project_root=args.root,
            target_file=args.target,
            refactor_goal=args.goal,
            architecture_warnings=list(args.warning or []),
            public_symbols=list(args.public_symbol or []),
            dependencies=list(args.dependency or []),
            existing_tests=list(args.existing_test or []),
            box_boundary_constraints=list(args.constraint or []),
            do_not_touch=list(args.do_not_touch or []),
            extra_evidence=list(args.evidence or []),
        )
    )
    return _emit_report(report.to_dict(), format_engineering_safety_markdown(report), args, stdout)


def _cmd_release_notes(args: argparse.Namespace, stdout: TextIO, stderr: TextIO) -> int:
    del stderr
    from kanda_reasoner_app.governance_automation.release_notes_generator import (
        GovernanceReleaseNoteInput,
        build_release_notes_report,
        render_release_notes_markdown,
    )

    item = GovernanceReleaseNoteInput(
        bundle_name=args.bundle_name,
        title=args.title or args.bundle_name,
        summary=args.summary,
        changed_files=tuple(args.changed_file or []),
        validation_lines=tuple(args.validation_line or []),
        status=args.status,
    )
    report = build_release_notes_report(args.title or args.bundle_name, (item,))
    return _emit_report(report.to_dict(), render_release_notes_markdown(report), args, stdout)


def _cmd_push_plan(args: argparse.Namespace, stdout: TextIO, stderr: TextIO) -> int:
    del stderr
    from kanda_reasoner_app.governance_automation.on_every_push_validator import (
        build_check_result_from_output,
        build_default_push_commands,
        build_on_every_push_report,
        render_on_every_push_markdown,
    )

    commands = build_default_push_commands(args.root)
    results = []
    for raw in args.check_output or []:
        name, _, output = str(raw).partition("::")
        results.append(build_check_result_from_output(name or "manual_check", "manual", output))
    report = build_on_every_push_report(args.root, results)
    return _emit_report({"report_type": "on_every_push", **report.to_dict()}, render_on_every_push_markdown(report), args, stdout)


def _cmd_stack_brief(args: argparse.Namespace, stdout: TextIO, stderr: TextIO) -> int:
    del stderr
    from kanda_reasoner_app.stack_compatibility.stack_briefs import (
        build_stack_compatibility_brief,
        render_stack_compatibility_markdown,
    )

    report = build_stack_compatibility_brief(
        tuple(args.requirement or []),
    )
    return _emit_report(report.as_dict(), render_stack_compatibility_markdown(report), args, stdout)


def _cmd_api_contract(args: argparse.Namespace, stdout: TextIO, stderr: TextIO) -> int:
    del stderr
    from kanda_reasoner_app.reliability_guidance.api_contract_guidance import (
        ApiContractGuardDraft,
        render_api_contract_guard_draft_markdown,
    )

    draft = ApiContractGuardDraft(
        module_path=args.module,
        function_name=args.function,
        parameters=tuple(args.param or []),
        return_hint=args.return_hint,
        known_failure_modes=tuple(args.failure or []),
        guard_suggestions=tuple(args.guard or []),
        tests_to_add=tuple(args.test or []),
    )
    data = {"report_type": "api_contract_guard_draft", **draft.__dict__}
    return _emit_report(data, render_api_contract_guard_draft_markdown(draft), args, stdout)


def _cmd_property_test(args: argparse.Namespace, stdout: TextIO, stderr: TextIO) -> int:
    del stderr
    from kanda_reasoner_app.reliability_guidance.property_test_guidance import (
        PropertyTestDraft,
        render_property_test_draft_markdown,
    )

    draft = PropertyTestDraft(
        module_path=args.module,
        function_name=args.function,
        properties=tuple(args.property or []),
        input_strategies=tuple(args.strategy or []),
        invariants=tuple(args.invariant or []),
        edge_cases=tuple(args.edge_case or []),
        tests_to_add=tuple(args.test or []),
    )
    data = {"report_type": "property_test_draft", **draft.__dict__}
    return _emit_report(data, render_property_test_draft_markdown(draft), args, stdout)


def _cmd_bom_scan(args: argparse.Namespace, stdout: TextIO, stderr: TextIO) -> int:
    del stderr
    from kanda_reasoner_app.source_hygiene.bom_scanner import scan_project_for_bom

    report = scan_project_for_bom(args.root, suffixes=tuple(args.suffix or []))
    return _emit_report(report.to_dict(), _source_report_markdown(report.to_dict()), args, stdout)


def _cmd_shadow_audit(args: argparse.Namespace, stdout: TextIO, stderr: TextIO) -> int:
    del stderr
    from kanda_reasoner_app.source_hygiene.shadow_audit import audit_project_for_shadow_conflicts

    report = audit_project_for_shadow_conflicts(args.root)
    return _emit_report(report.to_dict(), _source_report_markdown(report.to_dict()), args, stdout)


def _cmd_shadow_plan(args: argparse.Namespace, stdout: TextIO, stderr: TextIO) -> int:
    del stderr
    from kanda_reasoner_app.source_hygiene.shadow_audit import audit_project_for_shadow_conflicts
    from kanda_reasoner_app.source_hygiene.shadow_planner import build_shadow_conflict_plan

    audit = audit_project_for_shadow_conflicts(args.root)
    report = build_shadow_conflict_plan(audit)
    return _emit_report(report.to_dict(), _source_report_markdown(report.to_dict()), args, stdout)


def _cmd_facade_fix_plan(args: argparse.Namespace, stdout: TextIO, stderr: TextIO) -> int:
    del stderr
    from kanda_reasoner_app.source_hygiene.shadow_fixer import build_safe_facade_fix_plan

    report = build_safe_facade_fix_plan(args.root)
    return _emit_report(report.to_dict(), _source_report_markdown(report.to_dict()), args, stdout)


def _emit_report(data: dict[str, Any], markdown: str, args: argparse.Namespace, stdout: TextIO) -> int:
    text = json.dumps(_json_ready(data), indent=2, sort_keys=True) + "\n"
    if getattr(args, "format", "markdown") == "markdown":
        text = markdown
    output_path = str(getattr(args, "output", "") or "").strip()
    if output_path:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        Path(output_path).write_text(text, encoding="utf-8")
    else:
        stdout.write(text)
    return 0


def _read_text_or_literal(value: str) -> str:
    text = str(value or "")
    if not text:
        return ""
    path = Path(text)
    if path.exists() and path.is_file():
        return path.read_text(encoding="utf-8", errors="replace")
    return text


def _source_report_markdown(data: dict[str, Any]) -> str:
    lines = [
        "# Source Hygiene Report",
        "",
        "Report type: " + str(data.get("report_type", "unknown")),
        "Summary: " + str(data.get("summary", "")),
        "Finding count: " + str(data.get("finding_count", 0)),
        "",
        "## Findings",
    ]
    findings = data.get("findings", [])
    if isinstance(findings, list) and findings:
        for finding in findings:
            if isinstance(finding, dict):
                path = str(finding.get("path", ""))
                code = str(finding.get("code", ""))
                message = str(finding.get("message", ""))
                lines.append("- " + code + " :: " + path + " :: " + message)
    else:
        lines.append("- No findings.")
    return "\n".join(lines) + "\n"


def _json_ready(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): _json_ready(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_ready(item) for item in value]
    if isinstance(value, Path):
        return str(value)
    return value
