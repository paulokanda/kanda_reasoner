
"""Own workflow detector registration and execution."""

from __future__ import annotations

from .workflow_reader_ai_contract_detectors import (
    detect_workflow_reader_ai_contract_issues,
)

from .workflow_environment_contract_detectors import (
    detect_workflow_environment_contract_issues,
)

from .workflow_cross_project_generalization_detectors import (
    detect_workflow_cross_project_generalization_issues,
)

from .workflow_documentation_drift_detectors import (
    detect_workflow_documentation_drift_issues,
)

from .workflow_rollback_fail_safe_detectors import (
    detect_workflow_rollback_fail_safe_issues,
)

from .workflow_idempotency_detectors import (
    detect_workflow_idempotency_issues as _detect_workflow_idempotency_issues,
)
import importlib
from typing import Protocol

from .workflow_detector_context import WorkflowDetectorContext
from .workflow_issue_models import WorkflowIssue

__all__ = [
    "DEFAULT_WORKFLOW_DETECTOR_REGISTRY",
    "WorkflowDetector",
    "WorkflowDetectorRegistry",
    "register_workflow_detector",
    "run_workflow_detectors",
]

_DETECTOR_ERROR_TYPES = (
    AttributeError,
    KeyError,
    LookupError,
    OSError,
    RuntimeError,
    TypeError,
    ValueError,
)

_IMPORT_ERROR_TYPES = (
    AttributeError,
    ImportError,
    ModuleNotFoundError,
    OSError,
    RuntimeError,
    TypeError,
    ValueError,
)


class WorkflowDetector(Protocol):
    """Protocol for additive workflow detectors."""

    def __call__(self, context: WorkflowDetectorContext) -> list[WorkflowIssue]:
        """Return workflow issues for the supplied detector context."""


class WorkflowDetectorRegistry:
    """Small ordered registry for additive workflow detectors."""

    def __init__(self) -> None:
        self._detectors: list[tuple[str, WorkflowDetector]] = []

    def register(self, name: str, detector: WorkflowDetector) -> WorkflowDetector:
        """Register a detector and return it for decorator-style use."""
        detector_name = str(name).strip()
        if not detector_name:
            raise ValueError("Workflow detector name must not be empty.")
        self._detectors = [
            item for item in self._detectors if item[0] != detector_name
        ]
        self._detectors.append((detector_name, detector))
        return detector

    def items(self) -> tuple[tuple[str, WorkflowDetector], ...]:
        """Return registered detector items in execution order."""
        return tuple(self._detectors)

    def run(self, context: WorkflowDetectorContext) -> list[WorkflowIssue]:
        """Run registered detectors and return typed workflow issues."""
        return _run_detector_items(context=context, detector_items=self.items())


def _execution_error_issue(name: str, exc: BaseException) -> WorkflowIssue:
    """Build a typed workflow issue for detector execution errors."""
    return WorkflowIssue(
        issue_id="WORKFLOW_DETECTOR_EXECUTION_ERROR",
        category="workflow_detectors",
        severity="error",
        workflow_step=name,
        evidence="Workflow detector raised " + type(exc).__name__ + ": " + str(exc),
        expected="Workflow detectors should return WorkflowIssue lists without raising.",
        actual=type(exc).__name__ + ": " + str(exc),
    )


def _run_detector_items(
    *,
    context: WorkflowDetectorContext,
    detector_items: tuple[tuple[str, WorkflowDetector], ...],
) -> list[WorkflowIssue]:
    """Run detector items and convert common execution failures to issues."""
    issues: list[WorkflowIssue] = []
    for name, detector in detector_items:
        try:
            detector_issues = detector(context)
        except _DETECTOR_ERROR_TYPES as exc:
            issues.append(_execution_error_issue(name, exc))
        else:
            if detector_issues:
                issues.extend(detector_issues)
    return issues


def run_workflow_detectors(
    context: WorkflowDetectorContext,
    registry: WorkflowDetectorRegistry | None = None,
) -> list[WorkflowIssue]:
    """Run registered workflow detectors and return accumulated issues."""
    active_registry = registry or DEFAULT_WORKFLOW_DETECTOR_REGISTRY
    return active_registry.run(context)


def register_workflow_detector(name: str, detector: WorkflowDetector) -> WorkflowDetector:
    """Register a detector in the default workflow detector registry."""
    return DEFAULT_WORKFLOW_DETECTOR_REGISTRY.register(name, detector)


DEFAULT_WORKFLOW_DETECTOR_REGISTRY = WorkflowDetectorRegistry()


def _register_public_detector(module_name: str, detector_name: str) -> None:
    """Register one public detector if its module is available."""
    try:
        module = importlib.import_module(module_name, package=__package__)
    except _IMPORT_ERROR_TYPES:
        return
    detector = getattr(module, detector_name, None)
    if callable(detector):
        DEFAULT_WORKFLOW_DETECTOR_REGISTRY.register(detector_name, detector)


_register_public_detector(
    ".workflow_structure_detectors",
    "detect_workflow_structure_issues",
)
_register_public_detector(
    ".workflow_step_target_detectors",
    "detect_workflow_step_target_integrity",
)
_register_public_detector(
    ".workflow_step_order_detectors",
    "detect_workflow_step_order_issues",
)
_register_public_detector(
    ".workflow_interaction_contract_detectors",
    "detect_workflow_interaction_contract_issues",
)
_register_public_detector(
    ".workflow_artifact_route_detectors",
    "detect_workflow_artifact_route_issues",
)

_register_public_detector(
    ".workflow_reader_ai_contract_detectors",
    "detect_workflow_reader_ai_contract_issues",
)

# W016: register idempotency detector for Tab 2 workflow validation.
register_workflow_detector(
    "workflow_idempotency_contract",
    _detect_workflow_idempotency_issues,
)

from .workflow_validation_reference_detectors import (
    detect_validation_reference_misroutes as _detect_validation_reference_misroutes,
)

DEFAULT_WORKFLOW_DETECTOR_REGISTRY.register(
    "validation_reference_misroutes",
    _detect_validation_reference_misroutes,
)

# W018 rollback/fail-safe workflow detector registration.
try:
    register_workflow_detector(
        "workflow_rollback_fail_safe",
        detect_workflow_rollback_fail_safe_issues,
    )
except ValueError:
    pass

# W019 workflow documentation drift detector registration.
try:
    register_workflow_detector(
        "workflow_documentation_drift",
        detect_workflow_documentation_drift_issues,
    )
except ValueError:
    pass

# W020 cross-project generalization detector registration.
try:
    register_workflow_detector(
        "workflow_cross_project_generalization",
        detect_workflow_cross_project_generalization_issues,
    )
except ValueError:
    pass

# W021-T2 remaining Tab 2 help parity detector registration.
try:
    register_workflow_detector(
        "workflow_environment_contract",
        detect_workflow_environment_contract_issues,
    )
except ValueError:
    pass

# W021-T2B reader AI workflow contract detector registration.
try:
    register_workflow_detector(
        "workflow_reader_ai_contract",
        detect_workflow_reader_ai_contract_issues,
    )
except ValueError:
    pass
# Later Patch I: guard active evidence output routing during workflow validation.
_register_public_detector(
    ".workflow_evidence_output_route_guard_detectors",
    "detect_evidence_output_route_guard_issues",
)
