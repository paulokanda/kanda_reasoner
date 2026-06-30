# project-path: kanda_reasoner_app/engineering_safety/risk_radar.py
"""Read-only Risk Change Radar report builder."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from .schemas import EngineeringSafetyReport, normalize_report_sequence

CANONICAL_PACKAGE_PATH = "kanda_reasoner_app/"
LEGACY_PACKAGE_PATH = "ask_ai" + "_project_reasoner/"

ENGINEERING_SAFETY_RISK_BOX_HINTS = (
    (CANONICAL_PACKAGE_PATH + "source_hygiene", "source_hygiene"),
    (LEGACY_PACKAGE_PATH + "source_hygiene", "source_hygiene"),
    (CANONICAL_PACKAGE_PATH + "engineering_safety", "engineering_safety"),
    (LEGACY_PACKAGE_PATH + "engineering_safety", "engineering_safety"),
    (CANONICAL_PACKAGE_PATH + "prompt_library", "tab_9_prompt_library"),
    (LEGACY_PACKAGE_PATH + "prompt_library", "tab_9_prompt_library"),
    (CANONICAL_PACKAGE_PATH + "insert_missing_docstrings_gui", "tab_3_docstring_tool"),
    (LEGACY_PACKAGE_PATH + "insert_missing_docstrings_gui", "tab_3_docstring_tool"),
    (CANONICAL_PACKAGE_PATH + "tab3_manual_review_runtime", "tab_3_manual_review_runtime"),
    (LEGACY_PACKAGE_PATH + "tab3_manual_review_runtime", "tab_3_manual_review_runtime"),
    ("reasoner_tools_gui", "gui_shell"),
    ("tests/", "tests"),
    ("project_freeze_ledger/ACTIVE_PROJECT_ GOVERNANCE", "active_governance"),
)

ENGINEERING_SAFETY_HIGH_RISK_TOKENS = (
    "governance",
    "runtime",
    "gui",
    "workflow",
    "architecture",
    "collector",
    "json_splitter",
)

ENGINEERING_SAFETY_CRITICAL_PATH_TOKENS = (
    "accepted_warning_baseline.json",
    "REASONER_PROJECT_CANON.json",
    "REASONER_PROJECT_CANON.md",
    "check_reasoner_project_canon.py",
    "test_reasoner_project_canon.py",
)

__all__ = [
    "CANONICAL_PACKAGE_PATH",
    "ENGINEERING_SAFETY_CRITICAL_PATH_TOKENS",
    "ENGINEERING_SAFETY_HIGH_RISK_TOKENS",
    "ENGINEERING_SAFETY_RISK_BOX_HINTS",
    "LEGACY_PACKAGE_PATH",
    "RiskChangeRadarInput",
    "build_risk_change_radar_report",
    "infer_risk_change_affected_boxes",
    "normalize_risk_change_path",
    "score_risk_change",
]


@dataclass(slots=True)
class RiskChangeRadarInput:
    """Input data for a read-only risk change report."""

    project_root: str
    changed_files: list[str] = field(default_factory=list)
    bundle_manifest_text: str = ""
    validation_output_text: str = ""
    extra_evidence: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Normalize all list-like fields."""
        self.project_root = str(Path(self.project_root)) if self.project_root else ""
        self.changed_files = [normalize_risk_change_path(value) for value in self.changed_files]
        self.changed_files = [value for value in self.changed_files if value]
        self.bundle_manifest_text = str(self.bundle_manifest_text or "")
        self.validation_output_text = str(self.validation_output_text or "")
        self.extra_evidence = normalize_report_sequence(self.extra_evidence)


def normalize_risk_change_path(path: object) -> str:
    """Return a project-relative path using forward slashes."""
    text = str(path or "").strip().replace("\\", "/")
    while text.startswith("./"):
        text = text[2:]
    return text


def infer_risk_change_affected_boxes(changed_files: list[str]) -> list[str]:
    """Infer architecture boxes from changed file paths."""
    boxes: list[str] = []
    for path in changed_files:
        normalized = normalize_risk_change_path(path)
        for prefix, box_name in ENGINEERING_SAFETY_RISK_BOX_HINTS:
            if normalized.startswith(prefix) and box_name not in boxes:
                boxes.append(box_name)
    if not boxes and changed_files:
        boxes.append("unknown")
    return boxes


def _path_score(path: str) -> int:
    """Support path score behavior.
    
    Parameters
    ----------
    path : str
        The file or folder path.
    
    Returns
    -------
    int
        The integer result.
    """
    
    normalized = normalize_risk_change_path(path)
    score = 0
    if normalized.endswith(".py"):
        score += 1
    if normalized.startswith("tests/"):
        score -= 1
    if normalized.startswith("workbench/"):
        score -= 1
    if normalized.startswith(CANONICAL_PACKAGE_PATH) or normalized.startswith(LEGACY_PACKAGE_PATH):
        score += 1
    if normalized.startswith("reasoner_tools_gui/"):
        score += 2
    if normalized.startswith("_project_reference/ACTIVE_PROJECT_ GOVERNANCE"):
        score += 4
    if any(token in normalized.lower() for token in ENGINEERING_SAFETY_HIGH_RISK_TOKENS):
        score += 2
    if any(token in normalized for token in ENGINEERING_SAFETY_CRITICAL_PATH_TOKENS):
        score += 4
    return max(score, 0)


def score_risk_change(input_data: RiskChangeRadarInput) -> tuple[str, int, list[str]]:
    """Score a potential change and return risk level, score, and evidence."""
    score = 0
    evidence: list[str] = []
    for path in input_data.changed_files:
        path_score = _path_score(path)
        score += path_score
        if path_score >= 4:
            evidence.append("Critical or governance-sensitive path changed: " + path)
        elif path_score >= 2:
            evidence.append("Higher-risk active source path changed: " + path)
    if len(input_data.changed_files) >= 5:
        score += 2
        evidence.append("Multiple files changed in one bundle.")
    if input_data.validation_output_text:
        lowered = input_data.validation_output_text.lower()
        if "error" in lowered or "fail" in lowered:
            score += 3
            evidence.append("Recent validation output contains error or fail text.")
        elif "warning" in lowered:
            score += 1
            evidence.append("Recent validation output contains warning text.")
    if input_data.bundle_manifest_text:
        lowered_manifest = input_data.bundle_manifest_text.lower()
        if "gui" in lowered_manifest or "runtime" in lowered_manifest:
            score += 2
            evidence.append("Bundle manifest mentions GUI or runtime behavior.")
        if "governance" in lowered_manifest:
            score += 2
            evidence.append("Bundle manifest mentions governance behavior.")
    evidence.extend(input_data.extra_evidence)
    if score >= 10:
        return "critical", score, evidence
    if score >= 6:
        return "high", score, evidence
    if score >= 3:
        return "medium", score, evidence
    return "low", score, evidence or ["No high-risk signals detected."]


def _recommended_tests(changed_files: list[str], risk_level: str) -> list[str]:
    """Support recommended tests behavior.
    
    Parameters
    ----------
    changed_files : list[str]
        The changed files value.
    risk_level : str
        The risk level value.
    
    Returns
    -------
    list[str]
        The list of values.
    """
    
    tests = [
        'python kanda_reasoner_app\\manage_architecture\\manage_architecture.py --root "$PROJECT_ROOT" --validate',
        'python kanda_reasoner_app\\manage_workflows\\manage_workflows.py --root "$PROJECT_ROOT" --validate',
    ]
    if any(path.startswith("tests/") for path in changed_files):
        tests.insert(0, "python <focused changed test file>")
    if any(path.startswith("reasoner_tools_gui/") for path in changed_files):
        tests.append("python -c \"import reasoner_tools_gui; print('gui import smoke ok')\"")
    if risk_level in ("high", "critical"):
        tests.append("Run focused tests for each touched owner box before continuing.")
    return tests


def build_risk_change_radar_report(input_data: RiskChangeRadarInput) -> EngineeringSafetyReport:
    """Build a read-only Risk Change Radar report."""
    risk_level, score, evidence = score_risk_change(input_data)
    boxes = infer_risk_change_affected_boxes(input_data.changed_files)
    owning_box = ", ".join(boxes) if boxes else "unknown"
    if risk_level in ("high", "critical"):
        first_action = "Stop feature expansion and run focused owner-box validation first."
    elif risk_level == "medium":
        first_action = "Run the focused test for the changed files before global validation."
    else:
        first_action = "Proceed with normal bundle-gated validation."
    return EngineeringSafetyReport(
        report_type="risk_change_radar",
        project_root=input_data.project_root,
        risk_level=risk_level,
        owning_box=owning_box,
        affected_files=input_data.changed_files,
        root_cause_or_risk_hypothesis="Risk score " + str(score) + " from changed-file and validation signals.",
        suggested_first_action=first_action,
        tests_to_run=_recommended_tests(input_data.changed_files, risk_level),
        rollback_plan="Revert the current bundle or restore touched files from the previous validated baseline.",
        confidence="medium" if input_data.changed_files else "low",
        input_sources=["changed_files", "bundle_manifest", "validation_output"],
        evidence=evidence,
    )
