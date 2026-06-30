# project-path: kanda_reasoner_app/engineering_safety/crash_triage.py
"""Read-only Crash Triage report builder."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from .risk_radar import (
    CANONICAL_PACKAGE_PATH,
    LEGACY_PACKAGE_PATH,
    infer_risk_change_affected_boxes,
    normalize_risk_change_path,
)
from .schemas import EngineeringSafetyReport, normalize_report_sequence

ENGINEERING_SAFETY_TRACEBACK_FILE_RE = re.compile(
    r"File \"(?P<file>[^\"]+)\", line (?P<line>[0-9]+), in (?P<function>[^\n]+)"
)

ENGINEERING_SAFETY_CRASH_CLASS_HINTS = (
    ("ImportError", "import_error"),
    ("ModuleNotFoundError", "import_error"),
    ("NameError", "name_error"),
    ("AttributeError", "attribute_error"),
    ("TypeError", "type_error"),
    ("ValueError", "value_error"),
    ("KeyError", "key_error"),
    ("FileNotFoundError", "file_not_found"),
    ("RecursionError", "recursion_error"),
    ("RuntimeError", "runtime_error"),
    ("AssertionError", "assertion_error"),
)

__all__ = [
    "CrashTriageInput",
    "ENGINEERING_SAFETY_CRASH_CLASS_HINTS",
    "ENGINEERING_SAFETY_TRACEBACK_FILE_RE",
    "build_crash_triage_report",
    "extract_crash_traceback_frames",
    "infer_crash_class",
    "infer_crash_implicated_files",
]


@dataclass(slots=True)
class CrashTriageInput:
    """Input data for a read-only crash triage report."""

    project_root: str
    traceback_text: str = ""
    log_text: str = ""
    runtime_trace_text: str = ""
    extra_evidence: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Normalize all text and list-like fields."""
        self.project_root = str(Path(self.project_root)) if self.project_root else ""
        self.traceback_text = str(self.traceback_text or "")
        self.log_text = str(self.log_text or "")
        self.runtime_trace_text = str(self.runtime_trace_text or "")
        self.extra_evidence = normalize_report_sequence(self.extra_evidence)


def _combined_crash_text(input_data: CrashTriageInput) -> str:
    """Support combined crash text behavior.
    
    Parameters
    ----------
    input_data : CrashTriageInput
        The input data value.
    
    Returns
    -------
    str
        The string result.
    """
    
    parts = [
        input_data.traceback_text,
        input_data.log_text,
        input_data.runtime_trace_text,
    ]
    return "\n".join(part for part in parts if part)


def _project_relative_path(path_text: str, project_root: str) -> str:
    """Support project relative path behavior.
    
    Parameters
    ----------
    path_text : str
        The path text value.
    project_root : str
        The project root path.
    
    Returns
    -------
    str
        The string result.
    """
    
    normalized_input = normalize_risk_change_path(path_text)
    for marker in (
        CANONICAL_PACKAGE_PATH,
        LEGACY_PACKAGE_PATH,
        "reasoner_tools_gui/",
        "tests/",
        "workbench/",
        "project_freeze_ledger/",
    ):
        marker_index = normalized_input.find(marker)
        if marker_index >= 0:
            return normalized_input[marker_index:]
    raw_path = Path(path_text)
    if project_root:
        try:
            relative = raw_path.resolve().relative_to(Path(project_root).resolve())
            return normalize_risk_change_path(relative.as_posix())
        except (OSError, ValueError):
            pass
    return normalized_input


def extract_crash_traceback_frames(
    traceback_text: str,
    project_root: str = "",
) -> list[str]:
    """Extract project-friendly traceback frame strings."""
    frames: list[str] = []
    for match in ENGINEERING_SAFETY_TRACEBACK_FILE_RE.finditer(str(traceback_text or "")):
        file_path = _project_relative_path(match.group("file"), project_root)
        frame = file_path + ":" + match.group("line") + " in " + match.group("function").strip()
        if frame not in frames:
            frames.append(frame)
    return frames


def infer_crash_class(crash_text: str) -> str:
    """Infer a broad crash class from traceback or log text."""
    text = str(crash_text or "")
    for token, crash_class in ENGINEERING_SAFETY_CRASH_CLASS_HINTS:
        if token in text:
            return crash_class
    lowered = text.lower()
    if "traceback" in lowered:
        return "python_traceback"
    if "error" in lowered or "failed" in lowered or "exception" in lowered:
        return "runtime_error"
    if text.strip():
        return "unclassified_crash"
    return "no_crash_text"


def infer_crash_implicated_files(frames: list[str]) -> list[str]:
    """Infer implicated files from traceback frame strings."""
    files: list[str] = []
    for frame in frames:
        path = frame.split(":", 1)[0]
        normalized = normalize_risk_change_path(path)
        if normalized and normalized not in files:
            files.append(normalized)
    return files


def _risk_level_for_crash(crash_class: str, files: list[str]) -> str:
    """Support risk level for crash behavior.
    
    Parameters
    ----------
    crash_class : str
        The crash class value.
    files : list[str]
        The files value.
    
    Returns
    -------
    str
        The string result.
    """
    
    if crash_class == "no_crash_text":
        return "unknown"
    if any(path.startswith("_project_reference/ACTIVE_PROJECT_ GOVERNANCE") for path in files):
        return "critical"
    if crash_class in {"import_error", "python_traceback", "runtime_error"}:
        return "high"
    if files:
        return "medium"
    return "low"


def _first_action_for_crash(crash_class: str, files: list[str]) -> str:
    """Support first action for crash behavior.
    
    Parameters
    ----------
    crash_class : str
        The crash class value.
    files : list[str]
        The files value.
    
    Returns
    -------
    str
        The string result.
    """
    
    if crash_class == "no_crash_text":
        return "Provide traceback text, a crash log, or runtime trace evidence before patching."
    if files:
        return "Open the first implicated file and inspect the failing frame before proposing a patch."
    return "Classify the log manually and add traceback evidence before changing source code."


def _tests_for_crash(files: list[str]) -> list[str]:
    """Support tests for crash behavior.
    
    Parameters
    ----------
    files : list[str]
        The files value.
    
    Returns
    -------
    list[str]
        The list of values.
    """
    
    tests = [
        'python kanda_reasoner_app\\manage_architecture\\manage_architecture.py --root "$PROJECT_ROOT" --validate',
        'python kanda_reasoner_app\\manage_workflows\\manage_workflows.py --root "$PROJECT_ROOT" --validate',
    ]
    if files:
        compile_targets = " ".join(path.replace("/", "\\") for path in files if path.endswith(".py"))
        if compile_targets:
            tests.insert(0, "python -m py_compile " + compile_targets)
    if any(path.startswith("reasoner_tools_gui/") for path in files):
        tests.append("python -c \"import reasoner_tools_gui; print('gui import smoke ok')\"")
    return tests


def build_crash_triage_report(input_data: CrashTriageInput) -> EngineeringSafetyReport:
    """Build a read-only Crash Triage report."""
    crash_text = _combined_crash_text(input_data)
    frames = extract_crash_traceback_frames(crash_text, input_data.project_root)
    implicated_files = infer_crash_implicated_files(frames)
    crash_class = infer_crash_class(crash_text)
    boxes = infer_risk_change_affected_boxes(implicated_files)
    evidence = []
    if frames:
        evidence.extend("Traceback frame: " + frame for frame in frames[:10])
    else:
        evidence.append("No traceback frames were detected.")
    evidence.append("Crash class: " + crash_class)
    evidence.extend(input_data.extra_evidence)
    return EngineeringSafetyReport(
        report_type="crash_triage",
        project_root=input_data.project_root,
        risk_level=_risk_level_for_crash(crash_class, implicated_files),
        owning_box=", ".join(boxes) if boxes else "unknown",
        affected_files=implicated_files,
        root_cause_or_risk_hypothesis="Crash class inferred as " + crash_class + ".",
        suggested_first_action=_first_action_for_crash(crash_class, implicated_files),
        tests_to_run=_tests_for_crash(implicated_files),
        rollback_plan="Do not patch broadly; revert any attempted repair if focused crash reproduction still fails.",
        confidence="medium" if frames else "low",
        input_sources=["traceback_text", "log_text", "runtime_trace_text"],
        evidence=evidence,
    )
