# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_plan_snapshot.py
"""Workbench-owned immutable plan snapshot and typed materializers."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from pathlib import Path
from typing import Any

from .models import (
    DocstringProposal,
    ImportRecord,
    ModuleAnalysisReport,
    ProposedModule,
    RefactorPlan,
    RefactorSymbol,
)
from .planner_workbench_handoff import (
    PlannerWorkbenchHandoff,
    planner_workbench_handoff_hash_valid,
)

__all__ = [
    "WORKBENCH_PLAN_SNAPSHOT_FEATURE_ID",
    "WorkbenchPlanSnapshot",
    "build_workbench_plan_snapshot",
    "write_workbench_plan_snapshot",
    "load_workbench_plan_snapshot",
]

WORKBENCH_PLAN_SNAPSHOT_FEATURE_ID = (
    "large-file-refactor-workbench-owned-plan-snapshot-v1"
)


@dataclass(frozen=True)
class WorkbenchPlanSnapshot:
    """Immutable Workbench-owned copy of one Planner handoff."""

    schema_version: str
    feature_id: str
    planner_handoff_hash: str
    plan_json: str
    analysis_json: str
    candidate_paths: tuple[str, ...]
    target_file: str
    source_content_hash: str
    planner_status: str
    snapshot_hash: str

    def integrity_valid(self) -> bool:
        """Return whether immutable fields match the stored hash."""

        return self.snapshot_hash == _snapshot_hash(
            planner_handoff_hash=self.planner_handoff_hash,
            plan_json=self.plan_json,
            analysis_json=self.analysis_json,
            candidate_paths=self.candidate_paths,
            target_file=self.target_file,
            source_content_hash=self.source_content_hash,
            planner_status=self.planner_status,
        )

    def materialize_plan(self) -> RefactorPlan:
        """Return a fresh typed plan copy for one Workbench operation."""

        _require_integrity(self)
        return _plan_from_dict(_load_object(self.plan_json, "plan"))

    def materialize_analysis(self) -> ModuleAnalysisReport:
        """Return a fresh typed analysis copy for Workbench intake."""

        _require_integrity(self)
        return _analysis_from_dict(_load_object(self.analysis_json, "analysis"))


def build_workbench_plan_snapshot(
    handoff: PlannerWorkbenchHandoff,
) -> WorkbenchPlanSnapshot:
    """Convert public Planner handoff into Workbench-owned immutable state."""

    if not planner_workbench_handoff_hash_valid(handoff):
        raise ValueError("PLANNER_HANDOFF_HASH_MISMATCH")
    plan = _plan_from_dict(_load_object(handoff.plan_json, "plan"))
    analysis = _analysis_from_dict(
        _load_object(handoff.analysis_json, "analysis")
    )
    if analysis.source_content_hash != plan.source_content_hash:
        raise ValueError("ANALYSIS_PLAN_HASH_MISMATCH")
    snapshot_hash = _snapshot_hash(
        planner_handoff_hash=handoff.handoff_hash,
        plan_json=handoff.plan_json,
        analysis_json=handoff.analysis_json,
        candidate_paths=handoff.candidate_paths,
        target_file=plan.target_file,
        source_content_hash=plan.source_content_hash,
        planner_status=plan.status,
    )
    return WorkbenchPlanSnapshot(
        schema_version="1.0",
        feature_id=WORKBENCH_PLAN_SNAPSHOT_FEATURE_ID,
        planner_handoff_hash=handoff.handoff_hash,
        plan_json=handoff.plan_json,
        analysis_json=handoff.analysis_json,
        candidate_paths=tuple(handoff.candidate_paths),
        target_file=plan.target_file,
        source_content_hash=plan.source_content_hash,
        planner_status=plan.status,
        snapshot_hash=snapshot_hash,
    )



def write_workbench_plan_snapshot(
    snapshot: WorkbenchPlanSnapshot,
    destination: str | Path,
) -> Path:
    """Persist one integrity-checked snapshot as canonical UTF-8 JSON."""

    _require_integrity(snapshot)
    path = Path(destination).resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = asdict(snapshot)
    payload["candidate_paths"] = list(snapshot.candidate_paths)
    text = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    ) + "\n"
    path.write_text(text, encoding="utf-8", newline="\n")
    return path


def load_workbench_plan_snapshot(source: str | Path) -> WorkbenchPlanSnapshot:
    """Load one persisted snapshot and reject integrity drift."""

    path = Path(source).resolve()
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(payload, dict):
        raise ValueError("WORKBENCH_SNAPSHOT_PAYLOAD_NOT_OBJECT")
    payload["candidate_paths"] = tuple(payload.get("candidate_paths", []))
    snapshot = WorkbenchPlanSnapshot(**payload)
    _require_integrity(snapshot)
    return snapshot

def _require_integrity(snapshot: WorkbenchPlanSnapshot) -> None:
    if not snapshot.integrity_valid():
        raise ValueError("WORKBENCH_SNAPSHOT_HASH_MISMATCH")


def _load_object(text: str, label: str) -> dict[str, Any]:
    if not text:
        raise ValueError(label.upper() + "_MISSING")
    value = json.loads(text)
    if not isinstance(value, dict):
        raise ValueError(label.upper() + "_PAYLOAD_NOT_OBJECT")
    return value


def _plan_from_dict(data: dict[str, Any]) -> RefactorPlan:
    payload = dict(data)
    payload["symbols"] = [
        RefactorSymbol(**dict(item)) for item in payload.get("symbols", [])
    ]
    payload["proposed_modules"] = [
        ProposedModule(**dict(item))
        for item in payload.get("proposed_modules", [])
    ]
    payload["docstring_proposals"] = [
        DocstringProposal(**dict(item))
        for item in payload.get("docstring_proposals", [])
    ]
    return RefactorPlan(**payload)


def _analysis_from_dict(data: dict[str, Any]) -> ModuleAnalysisReport:
    payload = dict(data)
    imports: list[ImportRecord] = []
    for item in payload.get("imports", []):
        record = dict(item)
        if "line_span" in record:
            record["line_span"] = tuple(record["line_span"])
        imports.append(ImportRecord(**record))
    payload["imports"] = imports
    payload["symbols"] = [
        RefactorSymbol(**dict(item)) for item in payload.get("symbols", [])
    ]
    return ModuleAnalysisReport(**payload)


def _snapshot_hash(
    *,
    planner_handoff_hash: str,
    plan_json: str,
    analysis_json: str,
    candidate_paths: tuple[str, ...],
    target_file: str,
    source_content_hash: str,
    planner_status: str,
) -> str:
    payload = json.dumps(
        {
            "planner_handoff_hash": planner_handoff_hash,
            "plan_json": plan_json,
            "analysis_json": analysis_json,
            "candidate_paths": list(candidate_paths),
            "target_file": target_file,
            "source_content_hash": source_content_hash,
            "planner_status": planner_status,
        },
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()
