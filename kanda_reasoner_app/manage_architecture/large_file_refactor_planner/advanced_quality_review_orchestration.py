# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/advanced_quality_review_orchestration.py
"""Pure Python orchestration service for Advanced Quality Review."""
from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Callable

from .advanced_quality_cross_check_rules import (
    AdvancedQualityCrossCheckInputs,
    AdvancedQualityCrossCheckReport,
    evaluate_advanced_quality_cross_checks,
)
from .advanced_quality_evidence_models import (
    QualityReviewRunRecord,
    build_quality_review_run_record,
)
from .advanced_quality_evidence_store import (
    EvidencePersistenceReceipt,
    persist_quality_review_run,
)
from .advanced_quality_review_contract import (
    AnalysisExecutionStatus,
    AnalysisIdentity,
)
from .analyzer_adapter_contract import AdapterEvidenceBundle, build_adapter_input_pair
from .analyzer_capability_preflight import (
    AnalyzerCapabilityEvidence,
    preflight_analyzer_capabilities,
)
from .analyzer_environment_contract import (
    AnalyzerCapabilityMode,
    AnalyzerEnvironmentLock,
)
from .analyzer_environment_manifest import (
    AnalyzerEnvironmentManifest,
    load_analyzer_environment_manifest,
    validate_analyzer_environment_manifest,
)
from .analyzer_pinned_environment_spec import (
    ANALYZER_ENVIRONMENT_PROVISIONING_FEATURE_ID,
    PINNED_ANALYZERS,
    build_pinned_analyzer_environment_lock,
)
from .analyzer_process_runtime import CancellationToken, ProcessProgressEvent
from .analyzer_tool_runtime_paths import (
    analyzer_environment_python,
    analyzer_environment_script,
)
from .griffe_api_fitness_adapter import (
    GriffeAdapterOptions,
    run_griffe_api_fitness_review,
)
from .grimp_topology_fitness_adapter import (
    GrimpAdapterOptions,
    GrimpTopologyReviewResult,
    run_grimp_topology_review,
)
from .mypy_fitness_adapter import (
    MypyAdapterOptions,
    MypyFitnessReviewResult,
    run_mypy_fitness_review,
)
from .ruff_fitness_adapter import RuffAdapterOptions, run_ruff_fitness_review
from .vulture_fitness_adapter import (
    VultureAdapterOptions,
    VultureFitnessReviewResult,
    run_vulture_fitness_review,
)

__all__ = [
    "ADVANCED_QUALITY_REVIEW_ORCHESTRATION_FEATURE_ID",
    "AdvancedQualityReviewExecutionPlan",
    "AdvancedQualityReviewOutcome",
    "AdvancedQualityReviewRequest",
    "AdvancedQualityReviewStage",
    "build_pinned_review_execution_plan",
    "run_advanced_quality_review",
]

ADVANCED_QUALITY_REVIEW_ORCHESTRATION_FEATURE_ID = (
    "advanced-quality-review-cross-check-orchestration-qt-foundation-v1"
)

ProgressCallback = Callable[[str, str], None]


class AdvancedQualityReviewStage:
    """Canonical observable stage names without a GUI dependency."""

    ENVIRONMENT_PREFLIGHT = "ENVIRONMENT_PREFLIGHT"
    RUFF = "RUFF"
    API_REVIEW = "API_REVIEW"
    IMPORT_GRAPH = "IMPORT_GRAPH"
    TYPE_REVIEW = "TYPE_REVIEW"
    DEAD_CODE = "DEAD_CODE"
    DELTA = "DELTA"
    CROSS_CHECK = "CROSS_CHECK"
    PERSISTENCE = "PERSISTENCE"


@dataclass(frozen=True)
class AdvancedQualityReviewRequest:
    """Bind one orchestration run to exact Project and Preview identities."""

    active_project_root: str
    tool_root: str
    analysis_identity: AnalysisIdentity
    baseline_root: str
    preview_root: str
    package_name: str
    run_id: str
    created_at_utc: str
    mypy_capability_mode: AnalyzerCapabilityMode
    mypy_config_file: str = ""
    include_ruff_format_check: bool = False
    expected_new_import_edges: tuple[str, ...] = ()


@dataclass(frozen=True)
class AdvancedQualityReviewExecutionPlan:
    """Hold validated runtime and adapter options for one pure service run."""

    environment_manifest: AnalyzerEnvironmentManifest
    environment_lock: AnalyzerEnvironmentLock
    capabilities: tuple[AnalyzerCapabilityEvidence, ...]
    ruff_options: RuffAdapterOptions
    griffe_options: GriffeAdapterOptions
    grimp_options: GrimpAdapterOptions
    mypy_options: MypyAdapterOptions
    vulture_options: VultureAdapterOptions


@dataclass(frozen=True)
class AdvancedQualityReviewOutcome:
    """Return immutable review, cross-check, and persistence evidence."""

    analysis_identity_hash: str
    cross_check_report: AdvancedQualityCrossCheckReport
    run_record: QualityReviewRunRecord
    persistence_receipt: EvidencePersistenceReceipt
    ruff: AdapterEvidenceBundle
    griffe: AdapterEvidenceBundle
    grimp: GrimpTopologyReviewResult
    mypy: MypyFitnessReviewResult
    vulture: VultureFitnessReviewResult


def build_pinned_review_execution_plan(
    request: AdvancedQualityReviewRequest,
) -> AdvancedQualityReviewExecutionPlan:
    """Load and verify the frozen pinned environment without provisioning it."""
    tool_root = Path(request.tool_root).expanduser().resolve(strict=False)
    lock = build_pinned_analyzer_environment_lock(tool_root)
    manifest = load_analyzer_environment_manifest(tool_root)
    expected_versions = {
        item.engine_id: item.version for item in PINNED_ANALYZERS
    }
    blockers = validate_analyzer_environment_manifest(
        tool_root,
        manifest,
        expected_feature_id=ANALYZER_ENVIRONMENT_PROVISIONING_FEATURE_ID,
        environment_lock=lock,
        expected_versions=expected_versions,
    )
    if blockers:
        raise ValueError("AQR_ENVIRONMENT_MANIFEST_BLOCKED:" + "|".join(blockers))
    if request.analysis_identity.analyzer_lock_hash != lock.lock_hash:
        raise ValueError("AQR_ANALYSIS_LOCK_IDENTITY_MISMATCH")
    capabilities = preflight_analyzer_capabilities(
        lock,
        cwd=request.active_project_root,
    )
    capabilities = _apply_project_capability_modes(
        capabilities,
        mypy_mode=request.mypy_capability_mode,
    )
    _validate_capabilities(capabilities)
    versions = {item.engine_id: item.expected_version for item in capabilities}
    python_path = analyzer_environment_python(tool_root)
    config_hash = request.analysis_identity.analyzer_config_hash
    analysis_key = request.analysis_identity.identity_hash
    probe_path = Path(__file__).resolve(strict=True).parent / "grimp_graph_probe.py"
    return AdvancedQualityReviewExecutionPlan(
        environment_manifest=manifest,
        environment_lock=lock,
        capabilities=capabilities,
        ruff_options=RuffAdapterOptions(
            argv_prefix=(str(analyzer_environment_script(tool_root, "ruff")),),
            engine_version=versions["ruff"],
            extra_check_args=("--no-cache",),
            include_format_check=request.include_ruff_format_check,
        ),
        griffe_options=GriffeAdapterOptions(
            argv_prefix=(str(analyzer_environment_script(tool_root, "griffe")),),
            engine_version=versions["griffe"],
            package_name=request.package_name,
        ),
        grimp_options=GrimpAdapterOptions(
            argv_prefix=(str(python_path), str(probe_path)),
            engine_version=versions["grimp"],
            package_name=request.package_name,
            active_project_root=request.active_project_root,
            config_hash=config_hash,
            analysis_key=analysis_key,
        ),
        mypy_options=MypyAdapterOptions(
            argv_prefix=(str(analyzer_environment_script(tool_root, "mypy")),),
            engine_version=versions["mypy"],
            capability_mode=next(
                item.capability_mode for item in capabilities
                if item.engine_id == "mypy"
            ),
            active_project_root=request.active_project_root,
            config_hash=config_hash,
            analysis_key=analysis_key,
            config_file=request.mypy_config_file or None,
        ),
        vulture_options=VultureAdapterOptions(
            argv_prefix=(str(analyzer_environment_script(tool_root, "vulture")),),
            engine_version=versions["vulture"],
        ),
    )


def run_advanced_quality_review(
    request: AdvancedQualityReviewRequest,
    plan: AdvancedQualityReviewExecutionPlan,
    *,
    cancellation_token: CancellationToken | None = None,
    progress_callback: ProgressCallback | None = None,
) -> AdvancedQualityReviewOutcome:
    """Run analyzers sequentially, cross-check evidence, and persist one immutable run."""
    token = cancellation_token or CancellationToken()
    _validate_request_plan(request, plan)
    _emit(progress_callback, AdvancedQualityReviewStage.ENVIRONMENT_PREFLIGHT, "PASS")
    inputs = build_adapter_input_pair(
        request.analysis_identity,
        baseline_root=request.baseline_root,
        preview_root=request.preview_root,
    )

    _emit(progress_callback, AdvancedQualityReviewStage.RUFF, "START")
    ruff = run_ruff_fitness_review(
        inputs,
        plan.ruff_options,
        cancellation_token=token,
        progress_callback=_process_progress(progress_callback, AdvancedQualityReviewStage.RUFF),
    )
    _emit(progress_callback, AdvancedQualityReviewStage.RUFF, ruff.execution_status.value)

    _emit(progress_callback, AdvancedQualityReviewStage.API_REVIEW, "START")
    griffe = run_griffe_api_fitness_review(
        inputs,
        plan.griffe_options,
        cancellation_token=token,
        progress_callback=_process_progress(progress_callback, AdvancedQualityReviewStage.API_REVIEW),
    )
    _emit(progress_callback, AdvancedQualityReviewStage.API_REVIEW, griffe.execution_status.value)

    _emit(progress_callback, AdvancedQualityReviewStage.IMPORT_GRAPH, "START")
    grimp = run_grimp_topology_review(
        inputs,
        plan.grimp_options,
        cancellation_token=token,
        progress_callback=_process_progress(progress_callback, AdvancedQualityReviewStage.IMPORT_GRAPH),
    )
    _emit(progress_callback, AdvancedQualityReviewStage.IMPORT_GRAPH, grimp.bundle.execution_status.value)

    _emit(progress_callback, AdvancedQualityReviewStage.TYPE_REVIEW, "START")
    mypy = run_mypy_fitness_review(
        inputs,
        plan.mypy_options,
        cancellation_token=token,
        progress_callback=_process_progress(progress_callback, AdvancedQualityReviewStage.TYPE_REVIEW),
    )
    mypy_status = mypy.bundle.execution_status.value if mypy.bundle else mypy.capability_mode.value
    _emit(progress_callback, AdvancedQualityReviewStage.TYPE_REVIEW, mypy_status)

    _emit(progress_callback, AdvancedQualityReviewStage.DEAD_CODE, "START")
    vulture = run_vulture_fitness_review(
        inputs,
        plan.vulture_options,
        cancellation_token=token,
        progress_callback=_process_progress(progress_callback, AdvancedQualityReviewStage.DEAD_CODE),
    )
    _emit(progress_callback, AdvancedQualityReviewStage.DEAD_CODE, vulture.bundle.execution_status.value)

    _emit(progress_callback, AdvancedQualityReviewStage.DELTA, "PASS")
    cross_inputs = AdvancedQualityCrossCheckInputs(
        analysis_identity_hash=request.analysis_identity.identity_hash,
        ruff=ruff,
        griffe=griffe,
        grimp=grimp,
        mypy=mypy,
        vulture=vulture,
        expected_new_import_edges=request.expected_new_import_edges,
    )
    _emit(progress_callback, AdvancedQualityReviewStage.CROSS_CHECK, "START")
    report = evaluate_advanced_quality_cross_checks(cross_inputs)
    _emit(progress_callback, AdvancedQualityReviewStage.CROSS_CHECK, report.quality_decision.value)

    bundles = [ruff, griffe, grimp.bundle, vulture.bundle]
    if mypy.bundle is not None:
        bundles.append(mypy.bundle)
    record = build_quality_review_run_record(
        run_id=request.run_id,
        created_at_utc=request.created_at_utc or _utc_now_text(),
        analysis_identity=request.analysis_identity,
        analyzer_environment_identity_hash=plan.environment_manifest.manifest_hash,
        capabilities=plan.capabilities,
        executions=_executions(bundles),
        findings=_preview_findings(bundles),
        execution_status=_overall_execution_status(bundles),
        quality_decision=report.quality_decision,
    )
    raw_evidence = _raw_evidence(bundles, report)
    _emit(progress_callback, AdvancedQualityReviewStage.PERSISTENCE, "START")
    receipt = persist_quality_review_run(
        request.active_project_root,
        record,
        raw_evidence=raw_evidence,
    )
    _emit(progress_callback, AdvancedQualityReviewStage.PERSISTENCE, "PASS")
    return AdvancedQualityReviewOutcome(
        analysis_identity_hash=request.analysis_identity.identity_hash,
        cross_check_report=report,
        run_record=record,
        persistence_receipt=receipt,
        ruff=ruff,
        griffe=griffe,
        grimp=grimp,
        mypy=mypy,
        vulture=vulture,
    )



def _apply_project_capability_modes(
    capabilities: tuple[AnalyzerCapabilityEvidence, ...],
    *,
    mypy_mode: AnalyzerCapabilityMode,
) -> tuple[AnalyzerCapabilityEvidence, ...]:
    """Project conditional mypy authority onto observed capability evidence."""
    result = []
    for item in capabilities:
        if item.engine_id != "mypy":
            result.append(item)
            continue
        if not item.available or not item.compatible:
            effective = AnalyzerCapabilityMode.UNAVAILABLE
        elif mypy_mode is AnalyzerCapabilityMode.NOT_CONFIGURED:
            effective = AnalyzerCapabilityMode.NOT_CONFIGURED
        elif mypy_mode is AnalyzerCapabilityMode.AUTHORITATIVE:
            effective = AnalyzerCapabilityMode.AUTHORITATIVE
        else:
            effective = AnalyzerCapabilityMode.AVAILABLE_NON_AUTHORITATIVE
        result.append(replace(item, capability_mode=effective))
    return tuple(sorted(result, key=lambda item: item.engine_id))

def _validate_request_plan(
    request: AdvancedQualityReviewRequest,
    plan: AdvancedQualityReviewExecutionPlan,
) -> None:
    if request.analysis_identity.analyzer_lock_hash != plan.environment_lock.lock_hash:
        raise ValueError("AQR_REQUEST_PLAN_LOCK_HASH_MISMATCH")
    if not str(request.package_name or "").strip():
        raise ValueError("AQR_PACKAGE_NAME_EMPTY")
    _validate_capabilities(plan.capabilities)


def _validate_capabilities(capabilities: tuple[AnalyzerCapabilityEvidence, ...]) -> None:
    capability_map = {item.engine_id: item for item in capabilities}
    expected = {item.engine_id for item in PINNED_ANALYZERS}
    if set(capability_map) != expected:
        raise ValueError("AQR_CAPABILITY_ENGINE_SET_MISMATCH")
    for engine_id in ("ruff", "griffe", "grimp"):
        item = capability_map[engine_id]
        if not item.available or not item.compatible:
            raise ValueError("AQR_MANDATORY_CAPABILITY_BLOCKED:" + engine_id)


def _executions(bundles: list[AdapterEvidenceBundle]) -> tuple:
    executions = []
    for bundle in bundles:
        executions.extend((bundle.baseline_execution, bundle.preview_execution))
    return tuple(executions)


def _preview_findings(bundles: list[AdapterEvidenceBundle]) -> tuple:
    findings = []
    for bundle in bundles:
        findings.extend(bundle.preview_findings)
    return tuple(findings)


def _raw_evidence(
    bundles: list[AdapterEvidenceBundle],
    report: AdvancedQualityCrossCheckReport,
) -> dict[str, bytes]:
    result: dict[str, bytes] = {}
    for bundle in bundles:
        for path, data in bundle.raw_evidence:
            if path in result:
                raise ValueError("AQR_RAW_EVIDENCE_PATH_COLLISION:" + path)
            result[path] = bytes(data)
    report_bytes = (
        json.dumps(report.to_dict(), sort_keys=True, indent=2, ensure_ascii=True) + "\n"
    ).encode("utf-8")
    result["cross_check/report.json"] = report_bytes
    return result


def _overall_execution_status(
    bundles: list[AdapterEvidenceBundle],
) -> AnalysisExecutionStatus:
    statuses = {item.execution_status for item in bundles}
    for status in (
        AnalysisExecutionStatus.CANCELLED,
        AnalysisExecutionStatus.TIMED_OUT,
        AnalysisExecutionStatus.FAILED,
        AnalysisExecutionStatus.UNAVAILABLE,
        AnalysisExecutionStatus.STALE,
    ):
        if status in statuses:
            return status
    return AnalysisExecutionStatus.SUCCEEDED


def _process_progress(callback: ProgressCallback | None, stage: str):
    if callback is None:
        return None

    def forward(event: ProcessProgressEvent) -> None:
        callback(stage, event.phase + ":" + event.engine_id)

    return forward


def _emit(callback: ProgressCallback | None, stage: str, message: str) -> None:
    if callback is not None:
        callback(stage, message)


def _utc_now_text() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
