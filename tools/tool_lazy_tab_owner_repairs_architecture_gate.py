"""Architecture non-regression gate for Tool lazy-tab owner repairs."""

from __future__ import annotations

import re

__all__ = ["validate_lazy_tab_owner_repairs_architecture_non_regression"]

_ALLOWED_PATHS = (
    "kanda_prompt_workspace/prompt_tools/startup_kernel/constants.py",
    "kanda_prompt_workspace/prompt_tools/startup_kernel/generic_helpers.py",
    "kanda_prompt_workspace/prompt_tools/startup_kernel/source_resolution.py",
    "kanda_reasoner_app/daily_rfctr_report/daily_refactor_report.py",
    "kanda_reasoner_app/reasoner_context_collector/collector_runtime_scenarios_help/normalization.py",
    "kanda_reasoner_app/reasoner_context_collector/collector_widget_registry_help/_widget_registry_part1_layout.py",
    "kanda_reasoner_app/reasoner_context_collector/collector_widget_registry_help/_widget_registry_part1_registration.py",
    "kanda_reasoner_app/reasoner_context_collector/collector_widget_registry_help/widget_registry_methods_part_1_private_impl.py",
    "kanda_reasoner_app/reasoner_context_collector/collector_widget_ui_action_bridge_help/indexing.py",
    "kanda_reasoner_app/reasoner_context_collector/collector_widget_ui_action_bridge_help/matching.py",
    "kanda_reasoner_app/reasoner_runtime_collector/hooks/qt_connection_monitor.py",
    "kanda_reasoner_app/reasoner_runtime_collector/runtime_trace_decorators.py",
    "kanda_reasoner_app/reasoner_runtime_collector/runtime_trace_state.py",
    "kanda_reasoner_app/routing_signal_scorer/prompt_intake_boundary/prompt_artifact_contract.py",
    "kanda_reasoner_app/routing_signal_scorer/prompt_intake_boundary/prompt_output_firewall.py",
    "kanda_reasoner_app/runtime_scenarios/runtime_hotspot_hooks.py",
    "kanda_reasoner_app/runtime_scenarios/runtime_scenario_runtime.py",
    "kanda_reasoner_app/tab3_manual_review_runtime/scan_report_lifecycle_runtime.py",
    "scripts/merge_freeze_validation_evidence.py",
    "scripts/migrate_freeze_after_update_external_root.py",
)
_ALLOWED = frozenset(("WARNING", "DEAD_CODE_UNREACHABLE_FILE", path) for path in _ALLOWED_PATHS)


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def _issues(output: str) -> tuple[tuple[str, str, str], ...]:
    found = []
    for line in output.splitlines():
        match = re.match(r"^(WARNING|ERROR|OTHER)\s+(\S+)\s+(.*?)\s+::", line)
        if match:
            severity, code, path = match.groups()
            found.append((severity, code, path.strip().replace("\\", "/")))
    return tuple(found)


def validate_lazy_tab_owner_repairs_architecture_non_regression(output: str, touched_paths: frozenset[str]) -> None:
    match = re.search(
        r"Total issues:\s*(\d+)\s*\|\s*Errors:\s*(\d+)"
        r"\s*\|\s*Warnings:\s*(\d+)\s*\|\s*Other:\s*(\d+)",
        output,
    )
    _require(match is not None, "ARCHITECTURE_SUMMARY_MISSING")
    total, errors, warnings, other = (int(value) for value in match.groups())
    issues = _issues(output)
    _require(total == len(issues), "ARCHITECTURE_OUTPUT_INCOMPLETE")
    _require(errors == 0 and other == 0, "ARCHITECTURE_BLOCKING_ISSUES_PRESENT")
    _require(warnings == len(issues), "ARCHITECTURE_WARNING_COUNT_MISMATCH")
    current = set(issues)
    _require(len(current) == len(issues), "ARCHITECTURE_DUPLICATE_ISSUE_IDENTITY")
    unexpected = sorted(current - _ALLOWED)
    _require(not unexpected, "NEW_ARCHITECTURE_ISSUES: " + repr(unexpected))
    touched = sorted(issue for issue in issues if issue[2] in touched_paths)
    _require(not touched, "TOUCHED_PATH_ARCHITECTURE_ISSUES: " + repr(touched))
    print("ARCHITECTURE PREEXISTING BASELINE: " + str(len(_ALLOWED)))
    print("ARCHITECTURE CURRENT ISSUES: " + str(len(current)))
    print("NEW ARCHITECTURE ISSUES: 0")
    print("TOUCHED PATH ARCHITECTURE ISSUES: 0")
    print("ARCHITECTURE NON-REGRESSION: PASS")
