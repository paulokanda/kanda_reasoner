"""Architecture non-regression gate for Symbol Atlas wave 2N."""

from __future__ import annotations

import re

__all__ = ["validate_architecture_non_regression"]

_ALLOWED_DEAD_CODE_PATHS = (
    "kanda_prompt_workspace/prompt_tools/startup_kernel/constants.py",
    "kanda_prompt_workspace/prompt_tools/startup_kernel/generic_helpers.py",
    "kanda_prompt_workspace/prompt_tools/startup_kernel/source_resolution.py",
    "kanda_reasoner_app/daily_rfctr_report/daily_refactor_report.py",
    (
        "kanda_reasoner_app/reasoner_context_collector/"
        "collector_runtime_scenarios_help/normalization.py"
    ),
    (
        "kanda_reasoner_app/reasoner_context_collector/"
        "collector_widget_registry_help/_widget_registry_part1_layout.py"
    ),
    (
        "kanda_reasoner_app/reasoner_context_collector/"
        "collector_widget_registry_help/_widget_registry_part1_registration.py"
    ),
    (
        "kanda_reasoner_app/reasoner_context_collector/"
        "collector_widget_registry_help/"
        "widget_registry_methods_part_1_private_impl.py"
    ),
    (
        "kanda_reasoner_app/reasoner_context_collector/"
        "collector_widget_ui_action_bridge_help/indexing.py"
    ),
    (
        "kanda_reasoner_app/reasoner_context_collector/"
        "collector_widget_ui_action_bridge_help/matching.py"
    ),
    (
        "kanda_reasoner_app/reasoner_runtime_collector/hooks/"
        "qt_connection_monitor.py"
    ),
    "kanda_reasoner_app/reasoner_runtime_collector/runtime_trace_decorators.py",
    "kanda_reasoner_app/reasoner_runtime_collector/runtime_trace_state.py",
    (
        "kanda_reasoner_app/routing_signal_scorer/prompt_intake_boundary/"
        "prompt_artifact_contract.py"
    ),
    (
        "kanda_reasoner_app/routing_signal_scorer/prompt_intake_boundary/"
        "prompt_output_firewall.py"
    ),
    "kanda_reasoner_app/runtime_scenarios/runtime_hotspot_hooks.py",
    "kanda_reasoner_app/runtime_scenarios/runtime_scenario_runtime.py",
    (
        "kanda_reasoner_app/tab3_manual_review_runtime/"
        "scan_report_lifecycle_runtime.py"
    ),
    "scripts/merge_freeze_validation_evidence.py",
    "scripts/migrate_freeze_after_update_external_root.py",
)

_ALLOWED_BASELINE = frozenset(
    ("WARNING", "DEAD_CODE_UNREACHABLE_FILE", path)
    for path in _ALLOWED_DEAD_CODE_PATHS
)

_TOUCHED_PATHS = frozenset(
    {
        "kanda_reasoner_app/reasoner_symbol_atlas/output_policy.py",
        "kanda_reasoner_app/reasoner_symbol_atlas/existing_code_finder.py",
        (
            "kanda_reasoner_app/reasoner_symbol_atlas/"
            "existing_code_finder_matching_private.py"
        ),
        "kanda_reasoner_app/reasoner_symbol_atlas/facade_owner_resolver.py",
        (
            "kanda_reasoner_app/reasoner_symbol_atlas/"
            "facade_owner_resolver_helpers_private.py"
        ),
        "tests/test_reasoner_symbol_atlas_active_owner_filtering_wave2n.py",
        (
            "tools/validate_reasoner_symbol_atlas_active_owner_filtering_"
            "wave2n_v1r2.py"
        ),
        "tools/reasoner_symbol_atlas_wave2n_architecture_gate.py",
        "tools/reasoner_symbol_atlas_wave2n_public_boundary_gate.py",
    }
)


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def _parse_issues(output: str) -> tuple[tuple[str, str, str], ...]:
    issues: list[tuple[str, str, str]] = []
    for line in output.splitlines():
        match = re.match(r"^(WARNING|ERROR|OTHER)\s+(\S+)\s+(.*?)\s+::", line)
        if match is None:
            continue
        severity, code, relative_path = match.groups()
        issues.append((severity, code, relative_path.strip().replace("\\", "/")))
    return tuple(issues)


def validate_architecture_non_regression(output: str) -> None:
    """Require only the observed pre-Wave-2N warning identities."""

    summary_match = re.search(
        r"Total issues:\s*(\d+)\s*\|\s*Errors:\s*(\d+)"
        r"\s*\|\s*Warnings:\s*(\d+)\s*\|\s*Other:\s*(\d+)",
        output,
    )
    _require(summary_match is not None, "ARCHITECTURE_SUMMARY_MISSING")
    total, errors, warnings, other = (int(value) for value in summary_match.groups())
    issues = _parse_issues(output)
    _require(total == len(issues), "ARCHITECTURE_OUTPUT_INCOMPLETE")
    _require(errors == 0, "ARCHITECTURE_ERRORS_PRESENT")
    _require(other == 0, "ARCHITECTURE_OTHER_ISSUES_PRESENT")
    _require(warnings == len(issues), "ARCHITECTURE_WARNING_COUNT_MISMATCH")

    touched = sorted(issue for issue in issues if issue[2] in _TOUCHED_PATHS)
    _require(
        not touched,
        "WAVE2N_TOUCHED_PATH_ARCHITECTURE_ISSUES: " + repr(touched),
    )

    current = set(issues)
    _require(len(current) == len(issues), "ARCHITECTURE_DUPLICATE_ISSUE_IDENTITY")
    unexpected = sorted(current - _ALLOWED_BASELINE)
    _require(
        not unexpected,
        "WAVE2N_NEW_ARCHITECTURE_ISSUES: " + repr(unexpected),
    )

    print("WAVE2N ARCHITECTURE PREEXISTING BASELINE: " + str(len(_ALLOWED_BASELINE)))
    print("WAVE2N ARCHITECTURE CURRENT ISSUES: " + str(len(current)))
    print("WAVE2N NEW ARCHITECTURE ISSUES: 0")
    print("WAVE2N TOUCHED PATH ARCHITECTURE ISSUES: 0")
    print("WAVE2N ARCHITECTURE NON-REGRESSION: PASS")
