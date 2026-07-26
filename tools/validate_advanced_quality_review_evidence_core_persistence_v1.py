# project-path: tools/validate_advanced_quality_review_evidence_core_persistence_v1.py
"""Validate Release 3 Advanced Quality Review evidence and persistence contracts."""
from __future__ import annotations

import hashlib
from pathlib import Path
import tempfile

from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.advanced_quality_evidence_models import (
    EvidenceAuthorizationState,
    FindingLocation,
    FindingSeverity,
    RawEvidenceReference,
    build_normalized_finding,
    build_quality_review_run_record,
    evaluate_authorization_state,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.advanced_quality_evidence_store import (
    append_evidence_authorization_event,
    latest_evidence_authorization_state,
    persist_quality_review_run,
    verify_persisted_quality_review_run,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.advanced_quality_review_contract import (
    AnalysisExecutionStatus,
    AnalyzerAuthorityRole,
    QualityDecision,
    build_analysis_identity,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.analyzer_capability_preflight import (
    AnalyzerCapabilityEvidence,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.analyzer_environment_contract import (
    AnalyzerCapabilityMode,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.analyzer_process_runtime import (
    ProcessExecutionEvidence,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.analyzer_process_tree import (
    ProcessTreeCleanupEvidence,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_project_support_paths import (
    daily_work_root,
    quality_evidence_root,
    quality_evidence_root_blockers,
)

FEATURE_ID = "advanced-quality-review-evidence-core-persistence-v1"
ROOT = Path(__file__).resolve().parents[1]
SOURCE_FILES = (
    ROOT
    / "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/advanced_quality_evidence_models.py",
    ROOT
    / "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/advanced_quality_evidence_store.py",
    ROOT
    / "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_project_support_paths.py",
)


def main() -> int:
    """Run focused Release 3 validation and print deterministic markers."""
    with tempfile.TemporaryDirectory(prefix="kanda_release3_") as temporary:
        temp_root = Path(temporary)
        project_root = temp_root / "sample_project"
        project_root.mkdir(parents=True)
        raw = b'{"engine":"ruff","findings":[]}\n'
        h1 = _identity(preview_seed="h1", card="card-c1")
        h2 = _identity(preview_seed="h2", card="card-c1")
        c2 = _identity(preview_seed="h2", card="card-c2")
        record_h1 = _record(h1, raw, run_id="run-h1-001", line=10)

        _assert_immutable_models(record_h1)
        print("QUALITY_EVIDENCE_MODELS_IMMUTABLE: PASS")

        _assert_finding_identity_ignores_location(raw)
        print("FINDING_SEMANTIC_IDENTITY_LOCATION_INDEPENDENT: PASS")

        receipt_h1 = persist_quality_review_run(
            project_root,
            record_h1,
            raw_evidence={"ruff/output.json": raw},
        )
        _assert_project_support_ownership(project_root, Path(receipt_h1.run_root))
        print("DURABLE_QUALITY_EVIDENCE_PROJECT_SUPPORT_ONLY: PASS")

        blockers = verify_persisted_quality_review_run(project_root, receipt_h1)
        _require(not blockers, "PERSISTED_EVIDENCE_VERIFY_FAILED:" + "|".join(blockers))
        print("IMMUTABLE_RUN_MANIFEST_HASH_VERIFICATION: PASS")

        _assert_utf8_json_contract(Path(receipt_h1.run_root))
        print("QUALITY_EVIDENCE_UTF8_NO_BOM: PASS")

        _assert_staging_clean(project_root)
        print("QUALITY_EVIDENCE_STAGING_TRANSIENT_GARBAGE_ONLY: PASS")

        _assert_duplicate_run_rejected(project_root, record_h1, raw)
        print("IMMUTABLE_RUN_OVERWRITE_REJECTED: PASS")

        _require(
            evaluate_authorization_state(h1, h1) == EvidenceAuthorizationState.CURRENT,
            "MATCHING_IDENTITY_NOT_CURRENT",
        )
        _require(
            evaluate_authorization_state(h1, h2) == EvidenceAuthorizationState.STALE,
            "H1_TO_H2_NOT_STALE",
        )
        _require(
            evaluate_authorization_state(h1, c2) == EvidenceAuthorizationState.STALE,
            "CROSS_CARD_IDENTITY_NOT_STALE",
        )
        print("STALE_AND_CROSS_CARD_IDENTITY_REJECTION: PASS")

        review_record_path = Path(receipt_h1.run_root) / "review_record.json"
        immutable_hash_before = _sha256(review_record_path.read_bytes())
        event = append_evidence_authorization_event(
            project_root,
            record_h1,
            current_identity=h2,
            reason="Preview H2 replaced H1 after accepted correction.",
            event_id="stale-h1-after-h2",
            created_at_utc="2026-07-07T12:00:00Z",
        )
        _require(event.new_state == EvidenceAuthorizationState.STALE, "STALE_EVENT_NOT_STALE")
        _require(
            latest_evidence_authorization_state(receipt_h1.run_root)
            == EvidenceAuthorizationState.STALE,
            "LATEST_AUTHORIZATION_STATE_NOT_STALE",
        )
        immutable_hash_after = _sha256(review_record_path.read_bytes())
        _require(
            immutable_hash_before == immutable_hash_after,
            "IMMUTABLE_RUN_RECORD_REWRITTEN_BY_STALE_EVENT",
        )
        print("APPEND_ONLY_STALE_AUTHORIZATION_EVENT: PASS")

        record_h2 = _record(h2, raw, run_id="run-h2-001", line=20)
        receipt_h2 = persist_quality_review_run(
            project_root,
            record_h2,
            raw_evidence={"ruff/output.json": raw},
        )
        _require(receipt_h1.run_root != receipt_h2.run_root, "H1_H2_RUN_ROOT_COLLISION")
        _require(Path(receipt_h1.run_root).is_dir(), "H1_HISTORY_MISSING")
        _require(Path(receipt_h2.run_root).is_dir(), "H2_HISTORY_MISSING")
        print("H1_H2_IMMUTABLE_HISTORY_SEPARATION: PASS")

        _assert_raw_reference_fail_closed(project_root, h2, raw)
        print("RAW_EVIDENCE_PROVENANCE_FAILS_CLOSED: PASS")

        _assert_path_traversal_rejected(raw)
        print("EVIDENCE_PATH_TRAVERSAL_REJECTED: PASS")

        _assert_no_pydantic_dependency()
        print("EVIDENCE_CORE_STANDARD_LIBRARY_MODEL_CONTRACT: PASS")

        _assert_module_size_policy()
        print("MODULE_SIZE_POLICY_101_499: PASS")

    print("ADVANCED_QUALITY_REVIEW_EVIDENCE_CORE_PERSISTENCE: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0



def _identity(*, preview_seed: str, card: str):
    return build_analysis_identity(
        project_card_identity=card,
        target_relative_path="pkg/large_module.py",
        baseline_hash=_hash_seed("baseline"),
        preview_hash=_hash_seed(preview_seed),
        refactor_plan_hash=_hash_seed("plan"),
        analyzer_lock_hash=_hash_seed("lock"),
        analyzer_config_hash=_hash_seed("config"),
    )



def _record(identity, raw: bytes, *, run_id: str, line: int):
    capability = AnalyzerCapabilityEvidence(
        engine_id="ruff",
        available=True,
        observed_version="ruff 0.6.9",
        expected_version="0.6.9",
        compatible=True,
        execution_path="C:/tool/analyzers/ruff.exe",
        capability_mode=AnalyzerCapabilityMode.AUTHORITATIVE,
        configuration_source="project:pyproject.toml",
        cache_routing_supported=True,
        authority_role=AnalyzerAuthorityRole.MANDATORY,
        execution_status=AnalysisExecutionStatus.SUCCEEDED,
        diagnostic="",
    )
    cleanup = ProcessTreeCleanupEvidence(
        process_id=1234,
        platform="test",
        method="natural_exit",
        requested=False,
        root_process_reaped=True,
        cleanup_ok=True,
        diagnostic="Process exited normally.",
    )
    execution = ProcessExecutionEvidence(
        engine_id="ruff",
        status=AnalysisExecutionStatus.SUCCEEDED,
        process_id=1234,
        argv=("ruff", "check", "--output-format", "json"),
        cwd="C:/controlled_view",
        exit_code=0,
        duration_ms=25,
        stdout_text=raw.decode("utf-8"),
        stderr_text="",
        stdout_bytes_observed=len(raw),
        stderr_bytes_observed=0,
        stdout_truncated=False,
        stderr_truncated=False,
        cleanup=cleanup,
    )
    reference = RawEvidenceReference(
        engine_id="ruff",
        relative_path="ruff/output.json",
        sha256=_sha256(raw),
        byte_size=len(raw),
    )
    finding = build_normalized_finding(
        engine_id="ruff",
        engine_version="0.6.9",
        rule_id="F821",
        normalized_relative_path="pkg/large_module.py",
        symbol_identity="pkg.large_module:target",
        normalized_message_signature="undefined-name:target",
        severity=FindingSeverity.ERROR,
        location=FindingLocation(line=line, column=4, end_line=line, end_column=10),
        raw_evidence_reference=reference,
        metadata=(("source", "preview"),),
    )
    return build_quality_review_run_record(
        run_id=run_id,
        created_at_utc="2026-07-07T12:00:00Z",
        analysis_identity=identity,
        analyzer_environment_identity_hash=_hash_seed("environment"),
        capabilities=(capability,),
        executions=(execution,),
        findings=(finding,),
        execution_status=AnalysisExecutionStatus.SUCCEEDED,
        quality_decision=QualityDecision.REVIEW_REQUIRED,
    )



def _assert_immutable_models(record) -> None:
    try:
        record.run_id = "changed"
    except Exception:
        return
    raise AssertionError("QUALITY_REVIEW_RUN_RECORD_MUTABLE")



def _assert_finding_identity_ignores_location(raw: bytes) -> None:
    record_a = _record(_identity(preview_seed="h1", card="card-c1"), raw, run_id="a", line=10)
    record_b = _record(_identity(preview_seed="h1", card="card-c1"), raw, run_id="b", line=99)
    _require(
        record_a.findings[0].semantic_key == record_b.findings[0].semantic_key,
        "FINDING_SEMANTIC_KEY_CHANGED_WITH_LOCATION",
    )



def _assert_project_support_ownership(project_root: Path, run_root: Path) -> None:
    support = quality_evidence_root(project_root).resolve(strict=False)
    _require(_is_relative_to(run_root, support), "RUN_NOT_UNDER_QUALITY_EVIDENCE_ROOT")
    _require(not _is_relative_to(run_root, project_root), "RUN_INSIDE_PROJECT_SOURCE")
    _require(
        not _is_relative_to(run_root, daily_work_root(project_root)),
        "DURABLE_RUN_INSIDE_DAILY_WORK",
    )
    blockers = quality_evidence_root_blockers(project_root, run_root)
    _require(not blockers, "QUALITY_EVIDENCE_OWNERSHIP_BLOCKERS:" + "|".join(blockers))



def _assert_utf8_json_contract(run_root: Path) -> None:
    for path in run_root.rglob("*.json"):
        raw = path.read_bytes()
        _require(not raw.startswith(b"\xef\xbb\xbf"), "JSON_UTF8_BOM_PRESENT:" + str(path))
        raw.decode("utf-8", errors="strict")



def _assert_staging_clean(project_root: Path) -> None:
    staging = daily_work_root(project_root) / "quality_evidence_staging"
    if not staging.exists():
        return
    leftovers = [item for item in staging.iterdir()]
    _require(not leftovers, "QUALITY_EVIDENCE_STAGING_LEFTOVER")



def _assert_duplicate_run_rejected(project_root: Path, record, raw: bytes) -> None:
    try:
        persist_quality_review_run(
            project_root,
            record,
            raw_evidence={"ruff/output.json": raw},
        )
    except FileExistsError:
        return
    raise AssertionError("IMMUTABLE_RUN_OVERWRITE_NOT_REJECTED")



def _assert_raw_reference_fail_closed(project_root: Path, identity, raw: bytes) -> None:
    record = _record(identity, raw, run_id="missing-raw", line=1)
    try:
        persist_quality_review_run(project_root, record, raw_evidence={})
    except ValueError as exc:
        _require("RAW_EVIDENCE_REFERENCE_MISSING" in str(exc), "WRONG_RAW_REFERENCE_ERROR")
        return
    raise AssertionError("MISSING_RAW_REFERENCE_NOT_REJECTED")



def _assert_path_traversal_rejected(raw: bytes) -> None:
    reference = RawEvidenceReference(
        engine_id="ruff",
        relative_path="ruff/output.json",
        sha256=_sha256(raw),
        byte_size=len(raw),
    )
    try:
        build_normalized_finding(
            engine_id="ruff",
            engine_version="0.6.9",
            rule_id="F821",
            normalized_relative_path="../outside.py",
            symbol_identity="",
            normalized_message_signature="bad",
            severity=FindingSeverity.ERROR,
            location=FindingLocation(),
            raw_evidence_reference=reference,
        )
    except ValueError as exc:
        _require("EVIDENCE_RELATIVE_PATH_INVALID" in str(exc), "WRONG_PATH_TRAVERSAL_ERROR")
        return
    raise AssertionError("EVIDENCE_PATH_TRAVERSAL_NOT_REJECTED")



def _assert_no_pydantic_dependency() -> None:
    for path in SOURCE_FILES[:2]:
        text = path.read_text(encoding="utf-8", errors="strict")
        _require("pydantic" not in text.lower(), "PYDANTIC_DEPENDENCY_PRESENT:" + path.name)



def _assert_module_size_policy() -> None:
    for path in SOURCE_FILES:
        count = len(path.read_text(encoding="utf-8", errors="strict").splitlines())
        _require(101 <= count <= 499, f"MODULE_SIZE_OUT_OF_RANGE:{path.name}:{count}")



def _hash_seed(seed: str) -> str:
    return hashlib.sha256(seed.encode("utf-8")).hexdigest()



def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()



def _is_relative_to(path: Path, base: Path) -> bool:
    try:
        path.resolve(strict=False).relative_to(base.resolve(strict=False))
        return True
    except ValueError:
        return False



def _require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


if __name__ == "__main__":
    raise SystemExit(main())
