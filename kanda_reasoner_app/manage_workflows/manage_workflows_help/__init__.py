# project-path: kanda_reasoner_app/manage_workflows/manage_workflows_help/__init__.py
"""Facade for workflow manager helper modules."""

from __future__ import annotations

from .workflow_cli import (
    main,
    run_workflow_detector_results,
    validate_project,
)
from .workflow_command_runner import (
    command_list_results,
    run_tests,
)
from .workflow_generation import (
    collect_generated_outputs,
    generate_manifest,
    generate_workflows_md,
    load_manifest_or_default,
)
from .workflow_history import (
    clear_history,
    get_history_roots,
    print_history,
    record_root,
)
from .workflow_import_checks import (
    run_import_checks,
)
from .workflow_models import (
    CheckResult,
)
from .workflow_project_scan import (
    scan_project,
)
from .workflow_reporting import (
    print_results,
    summarize_results,
)
from .workflow_detector_context import (
    WorkflowDetectorContext,
)
from .workflow_detector_registry import (
    DEFAULT_WORKFLOW_DETECTOR_REGISTRY,
    WorkflowDetector,
    WorkflowDetectorRegistry,
    register_workflow_detector,
    run_workflow_detectors,
)
from .workflow_issue_models import (
    WorkflowIssue,
    workflow_issue_to_check_result,
)
from .workflow_step_target_detectors import (
    detect_workflow_step_target_integrity,
)

__all__ = [
    "CheckResult",
    "DEFAULT_WORKFLOW_DETECTOR_REGISTRY",
    "WorkflowDetector",
    "WorkflowDetectorContext",
    "WorkflowDetectorRegistry",
    "WorkflowIssue",
    "clear_history",
    "collect_generated_outputs",
    "command_list_results",
    "detect_workflow_step_target_integrity",
    "generate_manifest",
    "generate_workflows_md",
    "get_history_roots",
    "load_manifest_or_default",
    "main",
    "print_history",
    "print_results",
    "record_root",
    "register_workflow_detector",
    "run_import_checks",
    "run_tests",
    "run_workflow_detector_results",
    "run_workflow_detectors",
    "scan_project",
    "summarize_results",
    "validate_project",
    "workflow_issue_to_check_result",
]
