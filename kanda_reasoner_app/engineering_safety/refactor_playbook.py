"""Read-only Refactor Playbook report builder."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from .risk_radar import infer_risk_change_affected_boxes, normalize_risk_change_path
from .schemas import EngineeringSafetyReport, normalize_report_sequence, normalize_report_text

ENGINEERING_SAFETY_REFACTOR_PLAYBOOK_PHASES = (
    "inspect",
    "scope",
    "extract",
    "validate",
    "rollback",
)

ENGINEERING_SAFETY_REFACTOR_HIGH_RISK_TOKENS = (
    "gui",
    "runtime",
    "governance",
    "workflow",
    "architecture",
    "collector",
    "facade",
    "__init__.py",
)

__all__ = [
    "ENGINEERING_SAFETY_REFACTOR_HIGH_RISK_TOKENS",
    "ENGINEERING_SAFETY_REFACTOR_PLAYBOOK_PHASES",
    "RefactorPlaybookInput",
    "build_refactor_playbook_report",
    "build_refactor_playbook_steps",
    "infer_refactor_playbook_risk_level",
    "normalize_refactor_target_path",
]


@dataclass(slots=True)
class RefactorPlaybookInput:
    """Input data for a read-only refactor playbook."""

    project_root: str
    target_file: str
    refactor_goal: str = ""
    architecture_warnings: list[str] = field(default_factory=list)
    public_symbols: list[str] = field(default_factory=list)
    dependencies: list[str] = field(default_factory=list)
    existing_tests: list[str] = field(default_factory=list)
    box_boundary_constraints: list[str] = field(default_factory=list)
    do_not_touch: list[str] = field(default_factory=list)
    extra_evidence: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Normalize string and sequence fields."""
        self.project_root = str(Path(self.project_root)) if self.project_root else ""
        self.target_file = normalize_refactor_target_path(self.target_file)
        self.refactor_goal = normalize_report_text(self.refactor_goal)
        self.architecture_warnings = normalize_report_sequence(self.architecture_warnings)
        self.public_symbols = normalize_report_sequence(self.public_symbols)
        self.dependencies = normalize_report_sequence(self.dependencies)
        self.existing_tests = normalize_report_sequence(self.existing_tests)
        self.box_boundary_constraints = normalize_report_sequence(
            self.box_boundary_constraints
        )
        self.do_not_touch = normalize_report_sequence(self.do_not_touch)
        self.extra_evidence = normalize_report_sequence(self.extra_evidence)


def normalize_refactor_target_path(path_text: str) -> str:
    """Normalize a refactor target path to a project-friendly path."""
    return normalize_risk_change_path(path_text)


def infer_refactor_playbook_risk_level(input_data: RefactorPlaybookInput) -> str:
    """Infer a conservative risk level for a refactor target."""
    combined = "\n".join(
        [
            input_data.target_file,
            input_data.refactor_goal,
            "\n".join(input_data.architecture_warnings),
            "\n".join(input_data.dependencies),
        ]
    ).lower()
    if "active_project_ governance" in combined or "accepted_warning_baseline" in combined:
        return "critical"
    if any(token in combined for token in ENGINEERING_SAFETY_REFACTOR_HIGH_RISK_TOKENS):
        return "high"
    if len(input_data.public_symbols) >= 8 or len(input_data.dependencies) >= 8:
        return "high"
    if input_data.architecture_warnings or input_data.public_symbols or input_data.dependencies:
        return "medium"
    return "low"


def _default_goal(input_data: RefactorPlaybookInput) -> str:
    if input_data.refactor_goal:
        return input_data.refactor_goal
    if input_data.target_file:
        return "Refactor " + input_data.target_file + " without changing public behavior."
    return "Create a scoped refactor plan after a target file is provided."


def build_refactor_playbook_steps(input_data: RefactorPlaybookInput) -> list[str]:
    """Build a safe staged refactor sequence."""
    target = input_data.target_file or "<target file>"
    steps = [
        "Inspect " + target + " and identify the canonical owner box before editing.",
        "Record public symbols and imports that must remain compatible.",
        "Create or confirm focused tests for the behavior being preserved.",
        "Make one small structural change at a time; avoid broad rewrites.",
        "Run py_compile on touched Python files after each change.",
        "Run architecture validation after the focused test passes.",
        "Run workflow validation before accepting the bundle.",
        "Rollback the current bundle if validation introduces errors or new warnings.",
    ]
    if input_data.box_boundary_constraints:
        steps.insert(
            2,
            "Respect declared box constraints: "
            + "; ".join(input_data.box_boundary_constraints),
        )
    if input_data.do_not_touch:
        steps.insert(3, "Do not touch: " + "; ".join(input_data.do_not_touch))
    return steps


def _playbook_tests(input_data: RefactorPlaybookInput) -> list[str]:
    tests = []
    if input_data.target_file.endswith(".py"):
        tests.append("python -m py_compile " + input_data.target_file.replace("/", "\\"))
    tests.extend(input_data.existing_tests)
    tests.extend(
        [
            'python kanda_reasoner_app\\manage_architecture\\manage_architecture.py --root "$PROJECT_ROOT" --validate',
            'python kanda_reasoner_app\\manage_workflows\\manage_workflows.py --root "$PROJECT_ROOT" --validate',
        ]
    )
    unique_tests = []
    for command in tests:
        if command and command not in unique_tests:
            unique_tests.append(command)
    return unique_tests


def _playbook_evidence(input_data: RefactorPlaybookInput, steps: list[str]) -> list[str]:
    evidence = [
        "Refactor goal: " + _default_goal(input_data),
        "Target file: " + (input_data.target_file or "not provided"),
        "Step count: " + str(len(steps)),
    ]
    if input_data.architecture_warnings:
        evidence.extend("Architecture warning: " + item for item in input_data.architecture_warnings)
    if input_data.public_symbols:
        evidence.append("Public symbols: " + ", ".join(input_data.public_symbols))
    if input_data.dependencies:
        evidence.append("Dependencies: " + ", ".join(input_data.dependencies))
    evidence.extend(input_data.extra_evidence)
    return evidence


def build_refactor_playbook_report(
    input_data: RefactorPlaybookInput,
) -> EngineeringSafetyReport:
    """Build a read-only Refactor Playbook report."""
    steps = build_refactor_playbook_steps(input_data)
    affected_files = [input_data.target_file] if input_data.target_file else []
    boxes = infer_risk_change_affected_boxes(affected_files)
    risk_level = infer_refactor_playbook_risk_level(input_data)
    return EngineeringSafetyReport(
        report_type="refactor_playbook",
        project_root=input_data.project_root,
        risk_level=risk_level,
        owning_box=", ".join(boxes) if boxes else "unknown",
        affected_files=affected_files,
        root_cause_or_risk_hypothesis=_default_goal(input_data),
        suggested_first_action=steps[0],
        tests_to_run=_playbook_tests(input_data),
        rollback_plan=(
            "Rollback the bundle if focused tests, architecture validation, or workflow "
            "validation regress. Keep changes one bundle at a time."
        ),
        confidence="medium" if input_data.target_file else "low",
        input_sources=[
            "target_file",
            "architecture_warnings",
            "public_symbols",
            "dependencies",
            "existing_tests",
        ],
        evidence=_playbook_evidence(input_data, steps),
    )
