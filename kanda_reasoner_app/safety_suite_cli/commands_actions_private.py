# project-path: kanda_reasoner_app/safety_suite_cli/commands_actions_private.py
"""Private command implementations for the safety-suite CLI."""

from __future__ import annotations

import argparse
from typing import TextIO

from .commands_catalog_private import _available_cli_commands
from .commands_output_private import (
    _emit_report,
    _read_text_or_literal,
    _source_report_markdown,
)

__all__: list[str] = []

def _cmd_list_tools(args: argparse.Namespace, stdout: TextIO, stderr: TextIO) -> int:
    """Support cmd list tools behavior.
    
    Parameters
    ----------
    args : argparse.Namespace
        The positional arguments.
    stdout : TextIO
        The stdout value.
    stderr : TextIO
        The stderr value.
    
    Returns
    -------
    int
        The integer result.
    """
    
    del args, stderr
    for command in _available_cli_commands():
        stdout.write(command + "\n")
    return 0

def _cmd_risk_radar(args: argparse.Namespace, stdout: TextIO, stderr: TextIO) -> int:
    """Support cmd risk radar behavior.
    
    Parameters
    ----------
    args : argparse.Namespace
        The positional arguments.
    stdout : TextIO
        The stdout value.
    stderr : TextIO
        The stderr value.
    
    Returns
    -------
    int
        The integer result.
    """
    
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
    """Support cmd crash triage behavior.
    
    Parameters
    ----------
    args : argparse.Namespace
        The positional arguments.
    stdout : TextIO
        The stdout value.
    stderr : TextIO
        The stderr value.
    
    Returns
    -------
    int
        The integer result.
    """
    
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
    """Support cmd refactor playbook behavior.
    
    Parameters
    ----------
    args : argparse.Namespace
        The positional arguments.
    stdout : TextIO
        The stdout value.
    stderr : TextIO
        The stderr value.
    
    Returns
    -------
    int
        The integer result.
    """
    
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
    """Support cmd release notes behavior.
    
    Parameters
    ----------
    args : argparse.Namespace
        The positional arguments.
    stdout : TextIO
        The stdout value.
    stderr : TextIO
        The stderr value.
    
    Returns
    -------
    int
        The integer result.
    """
    
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
    """Support cmd push plan behavior.
    
    Parameters
    ----------
    args : argparse.Namespace
        The positional arguments.
    stdout : TextIO
        The stdout value.
    stderr : TextIO
        The stderr value.
    
    Returns
    -------
    int
        The integer result.
    """
    
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
    """Support cmd stack brief behavior.
    
    Parameters
    ----------
    args : argparse.Namespace
        The positional arguments.
    stdout : TextIO
        The stdout value.
    stderr : TextIO
        The stderr value.
    
    Returns
    -------
    int
        The integer result.
    """
    
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
    """Support cmd api contract behavior.
    
    Parameters
    ----------
    args : argparse.Namespace
        The positional arguments.
    stdout : TextIO
        The stdout value.
    stderr : TextIO
        The stderr value.
    
    Returns
    -------
    int
        The integer result.
    """
    
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
    """Support cmd property test behavior.
    
    Parameters
    ----------
    args : argparse.Namespace
        The positional arguments.
    stdout : TextIO
        The stdout value.
    stderr : TextIO
        The stderr value.
    
    Returns
    -------
    int
        The integer result.
    """
    
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
    """Support cmd bom scan behavior.
    
    Parameters
    ----------
    args : argparse.Namespace
        The positional arguments.
    stdout : TextIO
        The stdout value.
    stderr : TextIO
        The stderr value.
    
    Returns
    -------
    int
        The integer result.
    """
    
    del stderr
    from kanda_reasoner_app.source_hygiene.bom_scanner import scan_project_for_bom

    report = scan_project_for_bom(args.root, suffixes=tuple(args.suffix or []))
    return _emit_report(report.to_dict(), _source_report_markdown(report.to_dict()), args, stdout)


def _cmd_ruff_quality(args: argparse.Namespace, stdout: TextIO, stderr: TextIO) -> int:
    """Run the read-only project-wide Ruff quality check."""
    del stderr
    from kanda_reasoner_app.source_hygiene.ruff_quality import (
        build_ruff_quality_report,
    )

    report = build_ruff_quality_report(
        args.root,
        timeout_seconds=args.timeout_seconds,
    )
    return _emit_report(
        report.to_dict(),
        _source_report_markdown(report.to_dict()),
        args,
        stdout,
    )


def _cmd_shadow_audit(args: argparse.Namespace, stdout: TextIO, stderr: TextIO) -> int:
    """Support cmd shadow audit behavior.
    
    Parameters
    ----------
    args : argparse.Namespace
        The positional arguments.
    stdout : TextIO
        The stdout value.
    stderr : TextIO
        The stderr value.
    
    Returns
    -------
    int
        The integer result.
    """
    
    del stderr
    from kanda_reasoner_app.source_hygiene.shadow_audit import audit_project_for_shadow_conflicts

    report = audit_project_for_shadow_conflicts(args.root)
    return _emit_report(report.to_dict(), _source_report_markdown(report.to_dict()), args, stdout)

def _cmd_shadow_plan(args: argparse.Namespace, stdout: TextIO, stderr: TextIO) -> int:
    """Support cmd shadow plan behavior.
    
    Parameters
    ----------
    args : argparse.Namespace
        The positional arguments.
    stdout : TextIO
        The stdout value.
    stderr : TextIO
        The stderr value.
    
    Returns
    -------
    int
        The integer result.
    """
    
    del stderr
    from kanda_reasoner_app.source_hygiene.shadow_audit import audit_project_for_shadow_conflicts
    from kanda_reasoner_app.source_hygiene.shadow_planner import build_shadow_conflict_plan

    audit = audit_project_for_shadow_conflicts(args.root)
    report = build_shadow_conflict_plan(audit)
    return _emit_report(report.to_dict(), _source_report_markdown(report.to_dict()), args, stdout)

def _cmd_facade_fix_plan(args: argparse.Namespace, stdout: TextIO, stderr: TextIO) -> int:
    """Support cmd facade fix plan behavior.
    
    Parameters
    ----------
    args : argparse.Namespace
        The positional arguments.
    stdout : TextIO
        The stdout value.
    stderr : TextIO
        The stderr value.
    
    Returns
    -------
    int
        The integer result.
    """
    
    del stderr
    from kanda_reasoner_app.source_hygiene.shadow_fixer import build_safe_facade_fix_plan

    report = build_safe_facade_fix_plan(args.root)
    return _emit_report(report.to_dict(), _source_report_markdown(report.to_dict()), args, stdout)
