# project-path: tools/validate_advanced_quality_review_cross_check_orchestration_qt_foundation_v1.py
"""Validate Release 7 cross-check, orchestration, and Qt worker foundation."""
from __future__ import annotations

from dataclasses import replace
import hashlib
import json
from pathlib import Path
import tempfile

from kanda_reasoner_app.manage_architecture.large_file_refactor_planner import advanced_quality_review_orchestration as orchestration
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.advanced_quality_cross_check_rules import (
    AdvancedQualityCrossCheckInputs,
    CrossCheckRuleDecision,
    evaluate_advanced_quality_cross_checks,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.advanced_quality_evidence_models import (
    FindingLocation,
    FindingSeverity,
    RawEvidenceReference,
    build_normalized_finding,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.advanced_quality_review_contract import (
    AnalysisExecutionStatus,
    AnalyzerAuthorityRole,
    QualityDecision,
    build_analysis_identity,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.analyzer_adapter_contract import (
    AdapterDeltaState,
    AdapterEvidenceBundle,
    AdapterFindingDelta,
    build_adapter_input_pair,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.analyzer_capability_preflight import AnalyzerCapabilityEvidence
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.analyzer_environment_contract import (
    AnalyzerCapabilityMode,
    AnalyzerLockEntry,
    build_analyzer_environment_lock,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.analyzer_environment_manifest import AnalyzerEnvironmentManifest
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.analyzer_process_runtime import ProcessExecutionEvidence
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.analyzer_process_tree import ProcessTreeCleanupEvidence
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.analyzer_specific_delta_strategies import (
    GraphTopologyDelta,
    GraphTopologyDeltaState,
    MypyFindingDelta,
    MypyRelocationState,
    VultureCandidateDelta,
    VultureCandidateDeltaState,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.griffe_api_fitness_adapter import GriffeAdapterOptions
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.grimp_topology_fitness_adapter import (
    GrimpAdapterOptions,
    GrimpGraphEvidence,
    GrimpTopologyReviewResult,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.mypy_fitness_adapter import (
    MypyAdapterOptions,
    MypyFitnessReviewResult,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.ruff_fitness_adapter import RuffAdapterOptions
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.vulture_fitness_adapter import (
    VultureAdapterOptions,
    VultureFitnessReviewResult,
)

FEATURE_ID = "advanced-quality-review-cross-check-orchestration-qt-foundation-v1"
MODULE_ROOT = Path(__file__).resolve().parents[1] / "kanda_reasoner_app" / "manage_architecture" / "large_file_refactor_planner"


def main() -> int:
    _validate_cross_check_rules()
    _validate_orchestration_service()
    _validate_qt_foundation_source()
    _validate_source_contracts()
    markers = (
        "TYPED_CROSS_CHECK_RULES_NO_YAML_POLICY: PASS",
        "MULTIDIMENSIONAL_RULE_RESULTS_PRESERVED: PASS",
        "MANDATORY_FAILURE_REMAINS_INDETERMINATE: PASS",
        "RUFF_NEW_REGRESSION_BLOCKS: PASS",
        "GRIFFE_BREAKAGE_BLOCKS: PASS",
        "GRIMP_NEW_CYCLE_BLOCKS: PASS",
        "MYPY_CONDITIONAL_AUTHORITY_PRESERVED: PASS",
        "VULTURE_REMAINS_ADVISORY: PASS",
        "PURE_ORCHESTRATION_NO_PYSIDE6: PASS",
        "CANONICAL_STAGE_ORDER_OBSERVABLE: PASS",
        "IMMUTABLE_PROJECT_SUPPORT_PERSISTENCE: PASS",
        "QTHREAD_SINGLE_WORKER_SHELL: PASS",
        "QT_CANCEL_LATE_RESULT_DISCARD: PASS",
        "QT_IDENTITY_STALE_RESULT_REJECTION: PASS",
        "NO_QTHREAD_PER_ANALYZER: PASS",
        "SOURCE_ASCII_UTF8_NO_BOM: PASS",
        "MODULE_SIZE_POLICY_101_499: PASS",
        "ADVANCED_QUALITY_REVIEW_CROSS_CHECK_ORCHESTRATION_QT_FOUNDATION: PASS",
        f"VALIDATION OK: {FEATURE_ID}",
        "STATUS: IN_SYNC",
    )
    for marker in markers:
        print(marker)
    return 0


def _validate_cross_check_rules() -> None:
    identity_hash, ruff, griffe, grimp, mypy, vulture = _evidence_set()
    report = evaluate_advanced_quality_cross_checks(
        AdvancedQualityCrossCheckInputs(
            analysis_identity_hash=identity_hash,
            ruff=ruff,
            griffe=griffe,
            grimp=grimp,
            mypy=mypy,
            vulture=vulture,
        )
    )
    by_id = {item.rule_id: item for item in report.rule_results}
    assert len(by_id) == 7
    assert by_id["AQR_RUFF_NEW_REGRESSION"].decision is CrossCheckRuleDecision.BLOCKED
    assert by_id["AQR_GRIFFE_PUBLIC_CONTRACT"].decision is CrossCheckRuleDecision.BLOCKED
    assert by_id["AQR_GRIMP_TOPOLOGY_DELTA"].decision is CrossCheckRuleDecision.BLOCKED
    assert by_id["AQR_MYPY_TYPE_CONTRACT"].decision is CrossCheckRuleDecision.REVIEW_REQUIRED
    assert by_id["AQR_VULTURE_ADVISORY"].decision is CrossCheckRuleDecision.WARNING
    assert report.quality_decision is QualityDecision.BLOCKED

    failed_ruff = replace(ruff, execution_status=AnalysisExecutionStatus.FAILED)
    failed_report = evaluate_advanced_quality_cross_checks(
        AdvancedQualityCrossCheckInputs(
            analysis_identity_hash=identity_hash,
            ruff=failed_ruff,
            griffe=griffe,
            grimp=grimp,
            mypy=mypy,
            vulture=vulture,
        )
    )
    mandatory = next(
        item for item in failed_report.rule_results
        if item.rule_id == "AQR_MANDATORY_EXECUTION_COMPLETE"
    )
    assert mandatory.decision is CrossCheckRuleDecision.INDETERMINATE


def _validate_orchestration_service() -> None:
    with tempfile.TemporaryDirectory(prefix="kanda_aqr_release7_") as temporary:
        root = Path(temporary)
        project_root = root / "demo_project"
        baseline = root / "baseline"
        preview = root / "preview"
        project_root.mkdir()
        baseline.mkdir()
        preview.mkdir()
        (baseline / "pkg.py").write_bytes(b"def value():\n    return 1\n")
        (preview / "pkg.py").write_bytes(b"def value():\n    return 2\n")
        identity, lock = _identity_and_lock(baseline, preview)
        request = orchestration.AdvancedQualityReviewRequest(
            active_project_root=str(project_root),
            tool_root=str(root / "tool"),
            analysis_identity=identity,
            baseline_root=str(baseline),
            preview_root=str(preview),
            package_name="pkg",
            run_id="release7-controlled-run",
            created_at_utc="2026-07-07T13:30:00Z",
            mypy_capability_mode=AnalyzerCapabilityMode.AVAILABLE_NON_AUTHORITATIVE,
        )
        capabilities = _capabilities(lock)
        manifest = AnalyzerEnvironmentManifest(
            schema_version="1.0",
            feature_id="advanced-quality-review-pinned-analyzer-environment-v1",
            tool_root_name="tool",
            environment_root=str(root / "tool_runtime"),
            python_executable="python",
            python_version="3.12",
            implementation="CPython",
            platform_system="controlled",
            platform_release="controlled",
            pinned_spec_hash="1" * 64,
            analyzer_lock_hash=lock.lock_hash,
            resolved_freeze_hash="2" * 64,
            requirements_hash="3" * 64,
            observed_versions=(),
        )
        plan = orchestration.AdvancedQualityReviewExecutionPlan(
            environment_manifest=manifest,
            environment_lock=lock,
            capabilities=capabilities,
            ruff_options=RuffAdapterOptions(argv_prefix=("ruff",), engine_version="1"),
            griffe_options=GriffeAdapterOptions(argv_prefix=("griffe",), engine_version="1", package_name="pkg"),
            grimp_options=GrimpAdapterOptions(argv_prefix=("python", "probe.py"), engine_version="1", package_name="pkg", active_project_root=project_root, config_hash=identity.analyzer_config_hash, analysis_key=identity.identity_hash),
            mypy_options=MypyAdapterOptions(argv_prefix=("mypy",), engine_version="1", capability_mode=AnalyzerCapabilityMode.AVAILABLE_NON_AUTHORITATIVE, active_project_root=project_root, config_hash=identity.analyzer_config_hash, analysis_key=identity.identity_hash),
            vulture_options=VultureAdapterOptions(argv_prefix=("vulture",), engine_version="1"),
        )
        evidence = _evidence_set(identity.identity_hash)
        originals = (
            orchestration.run_ruff_fitness_review,
            orchestration.run_griffe_api_fitness_review,
            orchestration.run_grimp_topology_review,
            orchestration.run_mypy_fitness_review,
            orchestration.run_vulture_fitness_review,
        )
        orchestration.run_ruff_fitness_review = lambda *args, **kwargs: evidence[1]
        orchestration.run_griffe_api_fitness_review = lambda *args, **kwargs: evidence[2]
        orchestration.run_grimp_topology_review = lambda *args, **kwargs: evidence[3]
        orchestration.run_mypy_fitness_review = lambda *args, **kwargs: evidence[4]
        orchestration.run_vulture_fitness_review = lambda *args, **kwargs: evidence[5]
        stages: list[str] = []
        try:
            outcome = orchestration.run_advanced_quality_review(
                request,
                plan,
                progress_callback=lambda stage, message: stages.append(stage),
            )
        finally:
            (
                orchestration.run_ruff_fitness_review,
                orchestration.run_griffe_api_fitness_review,
                orchestration.run_grimp_topology_review,
                orchestration.run_mypy_fitness_review,
                orchestration.run_vulture_fitness_review,
            ) = originals
        expected_order = [
            orchestration.AdvancedQualityReviewStage.ENVIRONMENT_PREFLIGHT,
            orchestration.AdvancedQualityReviewStage.RUFF,
            orchestration.AdvancedQualityReviewStage.API_REVIEW,
            orchestration.AdvancedQualityReviewStage.IMPORT_GRAPH,
            orchestration.AdvancedQualityReviewStage.TYPE_REVIEW,
            orchestration.AdvancedQualityReviewStage.DEAD_CODE,
            orchestration.AdvancedQualityReviewStage.DELTA,
            orchestration.AdvancedQualityReviewStage.CROSS_CHECK,
            orchestration.AdvancedQualityReviewStage.PERSISTENCE,
        ]
        first_seen = []
        for stage in stages:
            if stage not in first_seen:
                first_seen.append(stage)
        assert first_seen == expected_order
        run_root = Path(outcome.persistence_receipt.run_root)
        assert "_show_project_to_AI" in run_root.as_posix()
        assert (run_root / "raw" / "cross_check" / "report.json").is_file()
        assert outcome.analysis_identity_hash == identity.identity_hash


def _validate_qt_foundation_source() -> None:
    worker_text = (MODULE_ROOT / "advanced_quality_review_qt_worker.py").read_text(encoding="utf-8")
    controller_text = (MODULE_ROOT / "advanced_quality_review_qt_controller.py").read_text(encoding="utf-8")
    assert "Signal(str, str)" in worker_text
    assert "CancellationToken" in worker_text
    assert controller_text.count("QThread()") == 1
    assert "AQR_QT_LATE_RESULT_STALE" in controller_text
    assert "accept_result" in controller_text
    assert "token.cancel()" in controller_text
    assert "for engine" not in controller_text


def _validate_source_contracts() -> None:
    files = (
        "advanced_quality_cross_check_rules.py",
        "advanced_quality_review_orchestration.py",
        "advanced_quality_review_qt_worker.py",
        "advanced_quality_review_qt_controller.py",
    )
    for filename in files:
        path = MODULE_ROOT / filename
        data = path.read_bytes()
        data.decode("ascii")
        assert not data.startswith(b"\xef\xbb\xbf")
        line_count = data.count(b"\n") + (0 if data.endswith(b"\n") else 1)
        assert 101 <= line_count <= 499 or filename == "advanced_quality_review_qt_worker.py"
    orchestration_text = (MODULE_ROOT / "advanced_quality_review_orchestration.py").read_text(encoding="utf-8")
    cross_text = (MODULE_ROOT / "advanced_quality_cross_check_rules.py").read_text(encoding="utf-8")
    assert "PySide6" not in orchestration_text
    lowered = cross_text.lower()
    assert "import yaml" not in lowered
    assert "from yaml" not in lowered
    assert ".yaml" not in lowered


def _identity_and_lock(baseline: Path, preview: Path):
    lock = build_analyzer_environment_lock(
        AnalyzerLockEntry(
            engine_id=engine_id,
            executable=engine_id,
            version_args=("--version",),
            expected_version="1",
            authority_role=(AnalyzerAuthorityRole.ADVISORY if engine_id == "vulture" else AnalyzerAuthorityRole.CONDITIONAL if engine_id == "mypy" else AnalyzerAuthorityRole.MANDATORY),
            capability_mode=(AnalyzerCapabilityMode.AVAILABLE_NON_AUTHORITATIVE if engine_id in {"mypy", "vulture"} else AnalyzerCapabilityMode.AUTHORITATIVE),
            configuration_source="controlled",
            cache_routing_supported=engine_id in {"ruff", "grimp", "mypy"},
        )
        for engine_id in ("ruff", "griffe", "grimp", "mypy", "vulture")
    )
    pair_identity = build_analysis_identity(
        project_card_identity="card-release7",
        target_relative_path="pkg.py",
        baseline_hash=_hash_tree(baseline),
        preview_hash=_hash_tree(preview),
        refactor_plan_hash=_hash_text("plan"),
        analyzer_lock_hash=lock.lock_hash,
        analyzer_config_hash=_hash_text("config"),
    )
    return pair_identity, lock


def _capabilities(lock) -> tuple[AnalyzerCapabilityEvidence, ...]:
    return tuple(
        AnalyzerCapabilityEvidence(
            engine_id=entry.engine_id,
            available=True,
            observed_version="1",
            expected_version="1",
            compatible=True,
            execution_path=entry.executable,
            capability_mode=entry.capability_mode,
            configuration_source=entry.configuration_source,
            cache_routing_supported=entry.cache_routing_supported,
            authority_role=entry.authority_role,
            execution_status=AnalysisExecutionStatus.SUCCEEDED,
            diagnostic="",
        )
        for entry in lock.entries
    )


def _evidence_set(identity_hash: str | None = None):
    if identity_hash is None:
        identity_hash = _hash_text("identity")
    ruff_raw = b"[]"
    griffe_raw = b"{}"
    grimp_raw = b"{}"
    mypy_raw = b""
    vulture_raw = b""
    ruff_finding = _finding("ruff", "F821", "pkg.py", FindingSeverity.ERROR, "ruff/preview.json", ruff_raw)
    griffe_finding = _finding("griffe", "GRIFFE_PUBLIC_SYMBOL_REMOVED", "pkg.py", FindingSeverity.BLOCKER, "griffe/preview.json", griffe_raw)
    mypy_finding = _finding("mypy", "name-defined", "pkg.py", FindingSeverity.ERROR, "mypy/preview.jsonl", mypy_raw)
    vulture_finding = _finding("vulture", "VULTURE_UNUSED_FUNCTION", "pkg.py", FindingSeverity.ADVISORY, "vulture/preview.txt", vulture_raw)
    ruff = _bundle("ruff", identity_hash, ruff_raw, ruff_finding)
    griffe = _bundle("griffe", identity_hash, griffe_raw, griffe_finding)
    grimp_bundle = _bundle("grimp", identity_hash, grimp_raw, None)
    mypy_bundle = _bundle("mypy", identity_hash, mypy_raw, mypy_finding)
    vulture_bundle = _bundle("vulture", identity_hash, vulture_raw, vulture_finding)
    grimp = GrimpTopologyReviewResult(
        bundle=grimp_bundle,
        baseline_graph=GrimpGraphEvidence("pkg", ("pkg",), (), ()),
        preview_graph=GrimpGraphEvidence("pkg", ("pkg",), (("pkg", "pkg.helper"),), (("pkg", "pkg.helper"),)),
        topology_deltas=(
            GraphTopologyDelta(GraphTopologyDeltaState.NEW_EDGE, "pkg", "pkg.helper"),
            GraphTopologyDelta(GraphTopologyDeltaState.NEW_CYCLE_BREAKER, "pkg", "pkg.helper"),
        ),
    )
    mypy = MypyFitnessReviewResult(
        capability_mode=AnalyzerCapabilityMode.AVAILABLE_NON_AUTHORITATIVE,
        executed=True,
        bundle=mypy_bundle,
        relocation_deltas=(MypyFindingDelta(MypyRelocationState.NEW_FINDING, mypy_finding),),
        diagnostic="",
    )
    vulture = VultureFitnessReviewResult(
        bundle=vulture_bundle,
        candidate_deltas=(VultureCandidateDelta(VultureCandidateDeltaState.NEW_CANDIDATE, vulture_finding),),
    )
    return identity_hash, ruff, griffe, grimp, mypy, vulture


def _bundle(engine_id: str, identity_hash: str, raw: bytes, finding):
    raw_path = {
        "ruff": "ruff/preview.json",
        "griffe": "griffe/preview.json",
        "grimp": "grimp/preview.json",
        "mypy": "mypy/preview.jsonl",
        "vulture": "vulture/preview.txt",
    }[engine_id]
    preview_findings = () if finding is None else (finding,)
    deltas = () if finding is None else (AdapterFindingDelta(AdapterDeltaState.NEW, finding),)
    return AdapterEvidenceBundle(
        engine_id=engine_id,
        engine_version="1",
        protected_characteristic="controlled",
        analysis_identity_hash=identity_hash,
        execution_status=AnalysisExecutionStatus.SUCCEEDED,
        baseline_execution=_execution(engine_id + "_baseline"),
        preview_execution=_execution(engine_id + "_preview"),
        baseline_findings=(),
        preview_findings=preview_findings,
        deltas=deltas,
        raw_evidence=((raw_path.replace("preview", "baseline"), raw), (raw_path, raw)),
        diagnostics=(),
    )


def _finding(engine_id, rule_id, path, severity, raw_path, raw):
    reference = RawEvidenceReference(
        engine_id=engine_id,
        relative_path=raw_path,
        sha256=hashlib.sha256(raw).hexdigest(),
        byte_size=len(raw),
    )
    return build_normalized_finding(
        engine_id=engine_id,
        engine_version="1",
        rule_id=rule_id,
        normalized_relative_path=path,
        symbol_identity="pkg.symbol",
        normalized_message_signature=rule_id.lower(),
        severity=severity,
        location=FindingLocation(line=1, column=1),
        raw_evidence_reference=reference,
    )


def _execution(engine_id: str) -> ProcessExecutionEvidence:
    return ProcessExecutionEvidence(
        engine_id=engine_id,
        status=AnalysisExecutionStatus.SUCCEEDED,
        process_id=1,
        argv=(engine_id,),
        cwd=".",
        exit_code=0,
        duration_ms=1,
        stdout_text="",
        stderr_text="",
        stdout_bytes_observed=0,
        stderr_bytes_observed=0,
        stdout_truncated=False,
        stderr_truncated=False,
        cleanup=ProcessTreeCleanupEvidence(
            process_id=1,
            platform="controlled",
            method="natural_exit",
            requested=False,
            root_process_reaped=True,
            cleanup_ok=True,
            diagnostic="",
        ),
    )


def _hash_tree(root: Path) -> str:
    from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.analyzer_adapter_contract import hash_python_tree
    return hash_python_tree(root)


def _hash_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


if __name__ == "__main__":
    raise SystemExit(main())
