"""Build bounded Workbench blocker context for correction routes."""
from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from typing import Any

from .workbench_aqr_correction_session import (
    activate_aqr_correction_session,
    current_aqr_correction_session,
)

__all__ = [
    "WORKBENCH_CORRECTABLE_STAGES",
    "WorkbenchStageCorrectionContext",
    "build_stage_correction_context",
    "stage_correction_needed",
]

WORKBENCH_CORRECTABLE_STAGES = (
    "PLAN_INTAKE",
    "DEPENDENCY_READINESS",
    "REAL_PREVIEW",
    "STRUCTURAL_VALIDATION",
    "ADVANCED_QUALITY_REVIEW",
    "PREFLIGHT_BACKUP",
    "SOURCE_PAYLOAD",
    "COMPLETION_EVIDENCE",
)

_STAGE_RESULT_ATTR = {
    "PLAN_INTAKE": "_large_file_refactor_workbench_intake",
    "DEPENDENCY_READINESS": "_large_file_refactor_workbench_dependency_readiness",
    "REAL_PREVIEW": "_large_file_refactor_workbench_real_preview",
    "STRUCTURAL_VALIDATION": "_large_file_refactor_workbench_structural_validation",
    "ADVANCED_QUALITY_REVIEW": "_large_file_refactor_workbench_advanced_quality_review",
    "PREFLIGHT_BACKUP": "_large_file_refactor_workbench_preflight_backup",
    "SOURCE_PAYLOAD": "_large_file_refactor_workbench_source_payload",
    "COMPLETION_EVIDENCE": "_large_file_refactor_workbench_completion_evidence",
}

_STAGE_OUTPUT_ATTR = {
    "PLAN_INTAKE": "_large_file_refactor_workbench_intake_output",
    "DEPENDENCY_READINESS": "_large_file_refactor_workbench_dependency_output",
    "REAL_PREVIEW": "_large_file_refactor_workbench_real_preview_output",
    "STRUCTURAL_VALIDATION": "_large_file_refactor_workbench_validation_output",
    "ADVANCED_QUALITY_REVIEW": "_large_file_refactor_workbench_aqr_output",
    "PREFLIGHT_BACKUP": "_large_file_refactor_workbench_preflight_output",
    "SOURCE_PAYLOAD": "_large_file_refactor_workbench_source_payload_output",
    "COMPLETION_EVIDENCE": "_large_file_refactor_workbench_completion_status_output",
}

_READY_STATUS = {
    "PLAN_INTAKE": {"plan_intake_ready"},
    "DEPENDENCY_READINESS": {"dependency_readiness_ready"},
    "REAL_PREVIEW": {"real_preview_written"},
    "STRUCTURAL_VALIDATION": {"passed", "passed_with_warnings"},
    "PREFLIGHT_BACKUP": {"preflight_backup_ready"},
    "SOURCE_PAYLOAD": {"source_apply_payload_ready"},
}


@dataclass(frozen=True)
class WorkbenchStageCorrectionContext:
    """One stage failure package safe for heuristic and AI correctors."""

    stage: str
    next_phase_goal: str
    active_project_root: str
    target_file: str
    status: str
    blockers: tuple[str, ...]
    warnings: tuple[str, ...]
    stage_output: str
    evidence_chain: tuple[tuple[str, str], ...]
    correction_objective: str

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-ready correction package."""
        data = asdict(self)
        data["blockers"] = list(self.blockers)
        data["warnings"] = list(self.warnings)
        data["evidence_chain"] = [
            {"stage": stage, "status": status}
            for stage, status in self.evidence_chain
        ]
        return data

    def prompt_text(self) -> str:
        """Return strict correction instructions with the observed failure context."""
        payload = json.dumps(self.to_dict(), indent=2, sort_keys=True)
        return "\n".join(
            [
                "KANDA LARGE FILE REFACTOR WORKBENCH BLOCKER CORRECTION REQUEST",
                "",
                "OBJECTIVE:",
                self.correction_objective,
                "",
                "HARD RULES:",
                "- Do not force-enable the next phase.",
                "- Do not bypass validation, Preview, preflight, payload, Shadow, transaction, or Freeze gates.",
                "- The proposed correction must be re-run through deterministic validation.",
                "- KANDA Reasoner Tool is the reusable machine; the Active Project owns source and durable project results.",
                "- Do not write project source while correcting Planner or Preview-stage blockers.",
                "- Prefer bounded Planner corrections over ad-hoc mutation of generated evidence.",
                "- Preserve public facade ownership and source-content identity checks.",
                "- Explain the root cause, the exact correction surface, and the revalidation step that proves readiness.",
                "",
                "OBSERVED FAILURE CONTEXT:",
                payload,
                "",
                "REQUIRED RESULT:",
                f"Return a correction that allows {self.stage} to become ready and only then permits the next governed phase: {self.next_phase_goal}.",
            ]
        )


def build_stage_correction_context(
    window: object,
    stage: str,
    active_project_root: str,
) -> WorkbenchStageCorrectionContext:
    """Build a bounded context package from current public Workbench evidence."""
    if stage not in WORKBENCH_CORRECTABLE_STAGES:
        raise ValueError("Unsupported Workbench correction stage: " + str(stage))
    result = getattr(window, _STAGE_RESULT_ATTR[stage], None)
    status = _status_for_stage(stage, result, _output_text(window, stage))
    if stage == "ADVANCED_QUALITY_REVIEW" and result is None:
        retained = current_aqr_correction_session(window)
        terminal = str(
            getattr(window, "_large_file_refactor_workbench_aqr_terminal_status", "")
            or ""
        )
        if retained is not None and not terminal:
            return retained.context
    if stage == "ADVANCED_QUALITY_REVIEW" and result is None:
        terminal = str(
            getattr(
                window,
                "_large_file_refactor_workbench_aqr_terminal_status",
                "",
            )
            or ""
        )
        if terminal:
            status = terminal
    blockers = _string_tuple(getattr(result, "blockers", ()))
    warnings = _string_tuple(getattr(result, "warnings", ()))
    if stage == "ADVANCED_QUALITY_REVIEW":
        blockers = _aqr_blockers(window, result)
        warnings = _aqr_warnings(result)
    if stage == "COMPLETION_EVIDENCE" and result is None:
        blockers = _completion_output_blockers(_output_text(window, stage))
    target_file = _target_file(window, result)
    next_goal = _next_phase_goal(stage)
    return WorkbenchStageCorrectionContext(
        stage=stage,
        next_phase_goal=next_goal,
        active_project_root=str(active_project_root),
        target_file=target_file,
        status=status,
        blockers=blockers,
        warnings=warnings,
        stage_output=_output_text(window, stage),
        evidence_chain=_evidence_chain(window),
        correction_objective=(
            f"Correct the root cause of the {stage} failure so deterministic rerun evidence "
            f"becomes ready/PASS and {next_goal} can be enabled without bypassing any gate."
        ),
    )


def stage_correction_needed(
    window: object,
    stage: str,
    active_project_root: str,
) -> bool:
    """Return whether one attempted stage is blocked and needs a correction route."""
    context = build_stage_correction_context(window, stage, active_project_root)
    result = getattr(window, _STAGE_RESULT_ATTR[stage], None)
    if _stage_ready(stage, result):
        return False
    if stage == "ADVANCED_QUALITY_REVIEW":
        if _aqr_running(window):
            return False
        correctable = context.status.upper() in {
            "BLOCKED",
            "INDETERMINATE",
            "FAILED",
            "TIMED_OUT",
            "CONFIGURATION_ERROR",
            "REVIEW_REQUIRED",
            "ADVISORY_REVIEW_REQUIRED",
        } and bool(context.blockers)
        if correctable:
            activate_aqr_correction_session(window, context)
            return True
        return current_aqr_correction_session(window) is not None
    if stage == "COMPLETION_EVIDENCE":
        return "BLOCKED" in context.stage_output.upper() or bool(context.blockers)
    return result is not None and context.status not in {"", "missing", "not_run"}



def _stage_ready(stage: str, result: Any) -> bool:
    if result is None:
        return False
    status = str(getattr(result, "status", "") or "")
    if stage == "PLAN_INTAKE":
        return bool(
            status == "plan_intake_ready"
            and getattr(result, "ready_for_real_preview", False)
            and getattr(result, "source_hash_fresh", False)
        )
    if stage == "DEPENDENCY_READINESS":
        return bool(
            status == "dependency_readiness_ready"
            and getattr(result, "ready_for_real_preview_writer", False)
        )
    if stage == "REAL_PREVIEW":
        return bool(
            status == "real_preview_written"
            and getattr(result, "files", None)
            and getattr(result, "written_files", None)
            and not getattr(result, "blockers", ())
        )
    if stage == "STRUCTURAL_VALIDATION":
        return bool(
            status.startswith("passed")
            and getattr(result, "structural_status", "") != "STRUCTURAL_FAIL"
            and not getattr(result, "blockers", ())
        )
    if stage == "ADVANCED_QUALITY_REVIEW":
        report = getattr(result, "cross_check_report", None)
        decision = _enum_text(getattr(report, "quality_decision", ""))
        execution = _enum_text(
            getattr(getattr(result, "run_record", None), "execution_status", "")
        )
        return execution == "SUCCEEDED" and decision in {"PASS", "PASS_WITH_WARNINGS"}
    if stage == "COMPLETION_EVIDENCE":
        return result is not None
    return status in _READY_STATUS.get(stage, set())

def _status_for_stage(stage: str, result: Any, output: str) -> str:
    if stage == "ADVANCED_QUALITY_REVIEW":
        if result is not None:
            execution = _enum_text(
                getattr(getattr(result, "run_record", None), "execution_status", "")
            )
            decision = _enum_text(
                getattr(getattr(result, "cross_check_report", None), "quality_decision", "")
            )
            return decision if execution == "SUCCEEDED" else (execution or decision or "blocked")
        return "not_run"
    if stage == "COMPLETION_EVIDENCE":
        if result is not None:
            shadow = getattr(result, "shadow_validation", None)
            return str(getattr(shadow, "status", "completion_evidence_ready") or "completion_evidence_ready")
        return "blocked" if "BLOCKED" in output.upper() else "not_run"
    return str(getattr(result, "status", "missing") or "missing")


def _evidence_chain(window: object) -> tuple[tuple[str, str], ...]:
    stages = []
    for stage in WORKBENCH_CORRECTABLE_STAGES:
        result = getattr(window, _STAGE_RESULT_ATTR[stage], None)
        status = _status_for_stage(stage, result, _output_text(window, stage))
        if stage == "ADVANCED_QUALITY_REVIEW" and result is None:
            terminal = str(
                getattr(
                    window,
                    "_large_file_refactor_workbench_aqr_terminal_status",
                    "",
                )
                or ""
            )
            if terminal:
                status = terminal
        stages.append((stage, status))
    return tuple(stages)


def _target_file(window: object, result: Any) -> str:
    direct = str(getattr(result, "target_file", "") or "")
    if direct:
        return direct
    snapshot = getattr(window, "_large_file_refactor_workbench_plan_snapshot", None)
    materialize = getattr(snapshot, "materialize_plan", None)
    if callable(materialize):
        try:
            return str(getattr(materialize(), "target_file", "") or "")
        except Exception:
            return ""
    return ""


def _output_text(window: object, stage: str) -> str:
    widget = getattr(window, _STAGE_OUTPUT_ATTR[stage], None)
    to_plain = getattr(widget, "toPlainText", None)
    if callable(to_plain):
        return str(to_plain() or "")
    return ""


def _completion_output_blockers(output: str) -> tuple[str, ...]:
    if "BLOCKED" not in output.upper():
        return ()
    lines = [line.strip() for line in output.splitlines() if line.strip()]
    return tuple(lines[1:] or ["COMPLETION_EVIDENCE_BLOCKED"])


def _string_tuple(values: Any) -> tuple[str, ...]:
    return tuple(str(item) for item in (values or ()) if str(item))


def _next_phase_goal(stage: str) -> str:
    return {
        "PLAN_INTAKE": "Dependency and Scope Readiness",
        "DEPENDENCY_READINESS": "Real Moved-Code Preview Generation",
        "REAL_PREVIEW": "Structural Validation",
        "STRUCTURAL_VALIDATION": "Advanced Quality Review",
        "ADVANCED_QUALITY_REVIEW": "Preflight Backup Readiness",
        "PREFLIGHT_BACKUP": "Source Apply Payload",
        "SOURCE_PAYLOAD": "Completion Evidence",
        "COMPLETION_EVIDENCE": "Human Review and Transaction Summary",
    }[stage]

def _aqr_running(window: object) -> bool:
    controller = getattr(window, "_large_file_refactor_workbench_aqr_controller", None)
    state = getattr(controller, "state", None)
    if not callable(state):
        return False
    try:
        return bool(getattr(state(), "running", False))
    except Exception:
        return False


def _aqr_blockers(window: object, result: Any) -> tuple[str, ...]:
    blockers: list[str] = []
    stage_states = dict(
        getattr(window, "_large_file_refactor_workbench_aqr_stage_states", {}) or {}
    )
    for name, status in sorted(stage_states.items()):
        upper = str(status).upper()
        if any(token in upper for token in ("FAILED", "TIMED_OUT", "CONFIGURATION_ERROR")):
            blockers.append("AQR_STAGE:" + str(name) + ":" + str(status))
    if result is not None:
        execution = _enum_text(
            getattr(getattr(result, "run_record", None), "execution_status", "")
        )
        decision = _enum_text(
            getattr(getattr(result, "cross_check_report", None), "quality_decision", "")
        )
        if execution and execution != "SUCCEEDED":
            blockers.append("AQR_EXECUTION_STATUS:" + execution)
        if decision and decision not in {"PASS", "PASS_WITH_WARNINGS"}:
            blockers.append("AQR_QUALITY_DECISION:" + decision)
        report = getattr(result, "cross_check_report", None)
        for item in tuple(getattr(report, "rule_results", ()) or ()):
            rule_decision = _enum_text(getattr(item, "decision", ""))
            if rule_decision in {
                "BLOCKED",
                "INDETERMINATE",
                "REVIEW_REQUIRED",
                "ADVISORY_REVIEW_REQUIRED",
            }:
                blockers.append(
                    "AQR_RULE:"
                    + str(getattr(item, "rule_id", "<unknown>"))
                    + ":"
                    + rule_decision
                )
    else:
        terminal = str(
            getattr(window, "_large_file_refactor_workbench_aqr_terminal_status", "") or ""
        )
        if terminal:
            blockers.append("AQR_TERMINAL_STATUS:" + terminal)
        diagnostic = str(
            getattr(window, "_large_file_refactor_workbench_aqr_terminal_diagnostic", "") or ""
        ).strip()
        if diagnostic:
            blockers.append("AQR_FAILURE_DIAGNOSTIC:" + diagnostic[:1000])
    return tuple(dict.fromkeys(blockers))


def _aqr_warnings(result: Any) -> tuple[str, ...]:
    report = getattr(result, "cross_check_report", None)
    warnings: list[str] = []
    for item in tuple(getattr(report, "rule_results", ()) or ()):
        rationale = str(getattr(item, "rationale", "") or "").strip()
        if rationale:
            warnings.append(
                str(getattr(item, "rule_id", "<unknown>")) + ":" + rationale
            )
    return tuple(warnings)


def _enum_text(value: Any) -> str:
    return str(getattr(value, "value", value) or "")

