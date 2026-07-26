# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/analyzer_adapter_contract.py
"""Shared immutable contracts for Advanced Quality Review analyzer adapters."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
import hashlib
from pathlib import Path
from typing import Iterable, Mapping, Protocol, runtime_checkable

from .advanced_quality_evidence_models import NormalizedFinding
from .advanced_quality_review_contract import (
    AnalysisExecutionStatus,
    AnalysisIdentity,
)
from .analyzer_environment_contract import AnalyzerCapabilityMode
from .analyzer_process_runtime import ProcessExecutionEvidence
from .analyzer_specific_delta_strategies import (
    GraphTopologyDelta,
    MypyFindingDelta,
    VultureCandidateDelta,
)

__all__ = [
    "ANALYZER_ADAPTER_FOUNDATION_FEATURE_ID",
    "AdapterDeltaState",
    "AdapterEvidenceBundle",
    "AdapterFindingDelta",
    "AdapterInputPair",
    "AdapterSnapshot",
    "GrimpTopologyResultView",
    "MypyFitnessResultView",
    "VultureFitnessResultView",
    "build_adapter_input_pair",
    "build_finding_deltas",
    "hash_python_tree",
    "validate_adapter_postconditions",
    "validate_adapter_preconditions",
]

ANALYZER_ADAPTER_FOUNDATION_FEATURE_ID = (
    "advanced-quality-review-ruff-griffe-fitness-adapters-v1"
)


class AdapterDeltaState(str, Enum):
    """Describe baseline-to-Preview finding movement without quality compression."""

    NEW = "NEW"
    RESOLVED = "RESOLVED"
    PERSISTENT = "PERSISTENT"


@dataclass(frozen=True)
class AdapterSnapshot:
    """Bind one analyzer input root to a deterministic Python-tree hash."""

    label: str
    root_path: str
    tree_hash: str

    def to_dict(self) -> dict[str, str]:
        """Return stable JSON-ready snapshot identity."""
        return asdict(self)


@dataclass(frozen=True)
class AdapterInputPair:
    """Bind one analyzer review to baseline, Preview, and analysis identity."""

    analysis_identity: AnalysisIdentity
    baseline: AdapterSnapshot
    preview: AdapterSnapshot

    def to_dict(self) -> dict[str, object]:
        """Return stable JSON-ready input-pair evidence."""
        return {
            "analysis_identity": self.analysis_identity.to_dict(),
            "analysis_identity_hash": self.analysis_identity.identity_hash,
            "baseline": self.baseline.to_dict(),
            "preview": self.preview.to_dict(),
        }


@dataclass(frozen=True)
class AdapterFindingDelta:
    """Record one analyzer-specific finding delta while preserving evidence."""

    state: AdapterDeltaState
    finding: NormalizedFinding

    def to_dict(self) -> dict[str, object]:
        """Return stable JSON-ready finding-delta evidence."""
        return {
            "state": self.state.value,
            "finding": self.finding.to_dict(),
            "semantic_key": self.finding.semantic_key,
        }


@dataclass(frozen=True)
class AdapterEvidenceBundle:
    """Collect one adapter result without hiding baseline/Preview disagreement."""

    engine_id: str
    engine_version: str
    protected_characteristic: str
    analysis_identity_hash: str
    execution_status: AnalysisExecutionStatus
    baseline_execution: ProcessExecutionEvidence
    preview_execution: ProcessExecutionEvidence
    baseline_findings: tuple[NormalizedFinding, ...]
    preview_findings: tuple[NormalizedFinding, ...]
    deltas: tuple[AdapterFindingDelta, ...]
    raw_evidence: tuple[tuple[str, bytes], ...]
    diagnostics: tuple[str, ...] = ()

    def raw_evidence_map(self) -> dict[str, bytes]:
        """Return a defensive raw-evidence mapping for persistence integration."""
        return {path: bytes(data) for path, data in self.raw_evidence}


@runtime_checkable
class GrimpTopologyResultView(Protocol):
    """Expose only policy-relevant Grimp topology evidence to the policy core."""

    bundle: AdapterEvidenceBundle
    topology_deltas: tuple[GraphTopologyDelta, ...]


@runtime_checkable
class MypyFitnessResultView(Protocol):
    """Expose only policy-relevant mypy evidence to the policy core."""

    capability_mode: AnalyzerCapabilityMode
    bundle: AdapterEvidenceBundle | None
    relocation_deltas: tuple[MypyFindingDelta, ...]


@runtime_checkable
class VultureFitnessResultView(Protocol):
    """Expose only policy-relevant Vulture evidence to the policy core."""

    bundle: AdapterEvidenceBundle
    candidate_deltas: tuple[VultureCandidateDelta, ...]



def build_adapter_input_pair(
    analysis_identity: AnalysisIdentity,
    *,
    baseline_root: str | Path,
    preview_root: str | Path,
) -> AdapterInputPair:
    """Build immutable input evidence from exact baseline and Preview roots."""
    baseline = Path(baseline_root).expanduser().resolve(strict=True)
    preview = Path(preview_root).expanduser().resolve(strict=True)
    if not baseline.is_dir():
        raise ValueError("ADAPTER_BASELINE_ROOT_NOT_DIRECTORY")
    if not preview.is_dir():
        raise ValueError("ADAPTER_PREVIEW_ROOT_NOT_DIRECTORY")
    if baseline == preview:
        raise ValueError("ADAPTER_BASELINE_PREVIEW_ROOT_SAME")
    return AdapterInputPair(
        analysis_identity=analysis_identity,
        baseline=AdapterSnapshot(
            label="baseline",
            root_path=str(baseline),
            tree_hash=hash_python_tree(baseline),
        ),
        preview=AdapterSnapshot(
            label="preview",
            root_path=str(preview),
            tree_hash=hash_python_tree(preview),
        ),
    )



def validate_adapter_preconditions(
    inputs: AdapterInputPair,
    *,
    engine_id: str,
    engine_version: str,
) -> tuple[str, ...]:
    """Return deterministic blockers before one adapter may start execution."""
    blockers: list[str] = []
    if not str(engine_id or "").strip():
        blockers.append("ADAPTER_ENGINE_ID_EMPTY")
    if not str(engine_version or "").strip():
        blockers.append("ADAPTER_ENGINE_VERSION_EMPTY")
    for snapshot in (inputs.baseline, inputs.preview):
        root = Path(snapshot.root_path).resolve(strict=False)
        if not root.is_dir():
            blockers.append("ADAPTER_INPUT_ROOT_MISSING:" + snapshot.label)
            continue
        observed = hash_python_tree(root)
        if observed != snapshot.tree_hash:
            blockers.append("ADAPTER_INPUT_DRIFT_BEFORE_RUN:" + snapshot.label)
    if inputs.analysis_identity.identity_hash == "":
        blockers.append("ADAPTER_ANALYSIS_IDENTITY_EMPTY")
    if inputs.analysis_identity.baseline_hash != inputs.baseline.tree_hash:
        blockers.append("ADAPTER_BASELINE_IDENTITY_HASH_MISMATCH")
    if inputs.analysis_identity.preview_hash != inputs.preview.tree_hash:
        blockers.append("ADAPTER_PREVIEW_IDENTITY_HASH_MISMATCH")
    return tuple(sorted(set(blockers)))



def validate_adapter_postconditions(
    inputs: AdapterInputPair,
    *,
    raw_evidence: Mapping[str, bytes],
) -> tuple[str, ...]:
    """Return blockers after execution, including mutation and evidence checks."""
    blockers: list[str] = []
    for snapshot in (inputs.baseline, inputs.preview):
        root = Path(snapshot.root_path).resolve(strict=False)
        if not root.is_dir():
            blockers.append("ADAPTER_INPUT_ROOT_MISSING_AFTER_RUN:" + snapshot.label)
            continue
        observed = hash_python_tree(root)
        if observed != snapshot.tree_hash:
            blockers.append("ANALYZER_MUTATION_DETECTED:" + snapshot.label)
    for relative_path, data in raw_evidence.items():
        text = str(relative_path or "").replace("\\", "/").strip()
        if not text or text.startswith("/") or ".." in text.split("/"):
            blockers.append("ADAPTER_RAW_EVIDENCE_PATH_INVALID:" + text)
        if not isinstance(data, bytes):
            blockers.append("ADAPTER_RAW_EVIDENCE_NOT_BYTES:" + text)
    return tuple(sorted(set(blockers)))



def build_finding_deltas(
    baseline_findings: Iterable[NormalizedFinding],
    preview_findings: Iterable[NormalizedFinding],
) -> tuple[AdapterFindingDelta, ...]:
    """Build semantic-key deltas while keeping both sides individually visible."""
    baseline_map = {item.semantic_key: item for item in baseline_findings}
    preview_map = {item.semantic_key: item for item in preview_findings}
    deltas: list[AdapterFindingDelta] = []
    for key in sorted(set(baseline_map) | set(preview_map)):
        if key in baseline_map and key in preview_map:
            deltas.append(
                AdapterFindingDelta(AdapterDeltaState.PERSISTENT, preview_map[key])
            )
        elif key in preview_map:
            deltas.append(AdapterFindingDelta(AdapterDeltaState.NEW, preview_map[key]))
        else:
            deltas.append(
                AdapterFindingDelta(AdapterDeltaState.RESOLVED, baseline_map[key])
            )
    return tuple(deltas)



def hash_python_tree(root: str | Path) -> str:
    """Hash relative paths and exact bytes for every Python source file in a tree."""
    base = Path(root).expanduser().resolve(strict=True)
    digest = hashlib.sha256()
    files = sorted(path for path in base.rglob("*.py") if path.is_file())
    for path in files:
        relative = path.relative_to(base).as_posix().encode("utf-8")
        data = path.read_bytes()
        digest.update(len(relative).to_bytes(8, "big"))
        digest.update(relative)
        digest.update(len(data).to_bytes(8, "big"))
        digest.update(data)
    return digest.hexdigest()
