# project-path: tools/workbench_post_apply_ruff_v4_support.py
"""Runtime fixtures for Workbench post-apply Ruff validation."""

from __future__ import annotations

import hashlib
from importlib import import_module
import os
from pathlib import Path
import shutil
import sys
import tempfile

_PACKAGE_PREFIX = "kanda_reasoner_app.manage_architecture.large_file_refactor_planner."
_MODELS = import_module(_PACKAGE_PREFIX + "models")
_GUARDED = import_module(_PACKAGE_PREFIX + "workbench_guarded_source_apply")
_PAYLOAD = import_module(_PACKAGE_PREFIX + "workbench_source_payload_builder")
_POST_APPLY = import_module(_PACKAGE_PREFIX + "workbench_post_apply_validator")
_POST_APPLY_RUFF = import_module(
    _PACKAGE_PREFIX + "workbench_post_apply_ruff_validation"
)

SCHEMA_VERSION = _MODELS.SCHEMA_VERSION
GUARDED_SOURCE_APPLY_FEATURE_ID = _GUARDED.GUARDED_SOURCE_APPLY_FEATURE_ID
GuardedSourceApplyResult = _GUARDED.GuardedSourceApplyResult
SOURCE_PAYLOAD_READINESS_FEATURE_ID = _PAYLOAD.SOURCE_PAYLOAD_READINESS_FEATURE_ID
SourceApplyPayloadFile = _PAYLOAD.SourceApplyPayloadFile
SourceApplyPayloadReadinessResult = _PAYLOAD.SourceApplyPayloadReadinessResult
PostApplyValidationResult = _POST_APPLY.PostApplyValidationResult
validate_and_write_post_apply = _POST_APPLY.validate_and_write_post_apply
validate_and_write_post_apply_ruff = _POST_APPLY_RUFF.validate_and_write_post_apply_ruff

__all__ = ["validate_runtime"]


def validate_runtime(root: Path, ruff: Path) -> None:
    """Run cross-platform runtime fixtures for the Phase 4 contract."""
    project_root = root
    if not ruff.is_file():
        raise AssertionError("RUFF_EXECUTABLE_MISSING")
    with tempfile.TemporaryDirectory(prefix="kanda_phase4_") as tmp:
        fixture = Path(tmp) / "fixture_project"
        fixture.mkdir()
        shutil.copy2(root / "ruff.toml", fixture / "ruff.toml")
        package = fixture / "pkg"
        package.mkdir()
        clean = package / "clean.py"
        clean.write_text(
            _integration_fixture_source("Clean fixture.", "VALUE = 1"),
            encoding="utf-8",
        )
        preview = fixture.parent / (
            fixture.name + "_show_project_to_AI/large_file_refactor_workbench/"
            "preview/phase4"
        )
        preview.mkdir(parents=True)

        note = package / "note.txt"
        note.write_text("not Python\n", encoding="utf-8")
        before = _sha256(clean)
        passed = validate_and_write_post_apply_ruff(
            active_project_root=fixture,
            preview_root=preview,
            checked_files=[Path("pkg/clean.py"), clean, note],
            ruff_argv_prefix=(str(ruff),),
        )
        if passed.status != "passed":
            raise AssertionError(
                "CLEAN_RUFF_CHECK_BLOCKED:" + "|".join(passed.blockers)
            )
        if passed.ruff_version != "0.15.21":
            raise AssertionError("RUFF_VERSION_EVIDENCE_CHANGED")
        if passed.checked_files != [str(clean.resolve())]:
            raise AssertionError("TOUCHED_FILE_SCOPE_CHANGED")
        if _sha256(clean) != before or not passed.source_hashes_unchanged:
            raise AssertionError("RUFF_MUTATED_CLEAN_SOURCE")
        if not Path(passed.report_path).is_file():
            raise AssertionError("RUFF_REPORT_MISSING")

        lint_bad = package / "lint_bad.py"
        lint_bad.write_text(
            _integration_fixture_source("Lint fixture.", "import os"),
            encoding="utf-8",
        )
        lint_before = _sha256(lint_bad)
        lint_result = validate_and_write_post_apply_ruff(
            active_project_root=fixture,
            preview_root=preview,
            checked_files=[lint_bad],
            ruff_argv_prefix=(str(ruff),),
        )
        if "POST_APPLY_RUFF_LINT_BLOCKED" not in lint_result.blockers:
            raise AssertionError("RUFF_LINT_DID_NOT_BLOCK")
        if _sha256(lint_bad) != lint_before or not lint_result.source_hashes_unchanged:
            raise AssertionError("RUFF_LINT_MUTATED_SOURCE")

        format_bad = package / "format_bad.py"
        format_bad.write_text(
            _integration_fixture_source("Format fixture.", 'VALUE={"a":1}'),
            encoding="utf-8",
        )
        format_before = _sha256(format_bad)
        format_result = validate_and_write_post_apply_ruff(
            active_project_root=fixture,
            preview_root=preview,
            checked_files=[format_bad],
            ruff_argv_prefix=(str(ruff),),
        )
        if "POST_APPLY_RUFF_FORMAT_BLOCKED" not in format_result.blockers:
            raise AssertionError("RUFF_FORMAT_DID_NOT_BLOCK")
        if (
            _sha256(format_bad) != format_before
            or not format_result.source_hashes_unchanged
        ):
            raise AssertionError("RUFF_FORMAT_CHECK_MUTATED_SOURCE")

        _validate_version_mismatch(fixture, preview, clean)
        _validate_evidence_root_shield(fixture, clean, ruff)
        _validate_optional_policy(fixture, preview, clean, project_root)
        _validate_workbench_integration(fixture, preview, clean, lint_bad, ruff)
        if (fixture / ".ruff_cache").exists():
            raise AssertionError("RUFF_PROJECT_CACHE_CREATED")


def _integration_fixture_source(docstring: str, final_line: str) -> str:
    """Build a 101-line module that satisfies Workbench line-law fixtures."""
    comments = [f"# fixture padding {index:03d}" for index in range(1, 99)]
    return "\n".join([f'"""{docstring}"""', "", *comments, final_line, ""])


def _validate_version_mismatch(
    fixture: Path,
    preview: Path,
    clean: Path,
) -> None:
    """Prove an available but mismatched Ruff command fails closed."""
    fake_ruff = fixture / "fake_ruff.py"
    fake_ruff.write_text('print("ruff 0.15.20")\n', encoding="utf-8")
    previous_path = os.environ.get("PATH")
    previous_env = os.environ.pop("KANDA_RUFF_EXECUTABLE", None)
    os.environ["PATH"] = ""
    try:
        result = validate_and_write_post_apply_ruff(
            active_project_root=fixture,
            preview_root=preview,
            checked_files=[clean],
            ruff_argv_prefix=(sys.executable, str(fake_ruff)),
        )
    finally:
        if previous_path is None:
            os.environ.pop("PATH", None)
        else:
            os.environ["PATH"] = previous_path
        if previous_env is not None:
            os.environ["KANDA_RUFF_EXECUTABLE"] = previous_env
    if result.status != "blocked":
        raise AssertionError("RUFF_VERSION_MISMATCH_DID_NOT_BLOCK")
    if "POST_APPLY_RUFF_EXACT_VERSION_NOT_AVAILABLE" not in result.blockers:
        raise AssertionError("RUFF_VERSION_MISMATCH_BLOCKER_MISSING")


def _validate_evidence_root_shield(
    fixture: Path,
    clean: Path,
    ruff: Path,
) -> None:
    """Prove Ruff evidence cannot be written into active project source."""
    invalid_root = fixture / "invalid_preview"
    result = validate_and_write_post_apply_ruff(
        active_project_root=fixture,
        preview_root=invalid_root,
        checked_files=[clean],
        ruff_argv_prefix=(str(ruff),),
    )
    if result.status != "blocked":
        raise AssertionError("INVALID_EVIDENCE_ROOT_DID_NOT_BLOCK")
    expected = "POST_APPLY_RUFF_PREVIEW_ROOT_INSIDE_PROJECT_SOURCE"
    if expected not in result.blockers:
        raise AssertionError("INVALID_EVIDENCE_ROOT_BLOCKER_MISSING")
    if Path(result.report_path).exists():
        raise AssertionError("INVALID_EVIDENCE_ROOT_WAS_WRITTEN")


def _validate_optional_policy(
    fixture: Path,
    preview: Path,
    clean: Path,
    project_root: Path,
) -> None:
    (fixture / "ruff.toml").unlink()
    result = validate_and_write_post_apply_ruff(
        active_project_root=fixture,
        preview_root=preview,
        checked_files=[clean],
    )
    if result.status != "not_configured":
        raise AssertionError("MISSING_POLICY_DID_NOT_REMAIN_COMPATIBLE")
    if result.blockers:
        raise AssertionError("MISSING_POLICY_CREATED_BLOCKER")
    if "POST_APPLY_RUFF_POLICY_NOT_CONFIGURED" not in result.warnings:
        raise AssertionError("MISSING_POLICY_WARNING_MISSING")
    if "ruff_lint_read_only" in result.checked_rules:
        raise AssertionError("MISSING_POLICY_FALSELY_CLAIMED_LINT_EXECUTION")
    if "ruff_format_check_read_only" in result.checked_rules:
        raise AssertionError("MISSING_POLICY_FALSELY_CLAIMED_FORMAT_EXECUTION")
    skipped = validate_and_write_post_apply_ruff(
        active_project_root=fixture,
        preview_root=preview,
        checked_files=[clean],
        skip_due_to_prior_blockers=True,
    )
    if "ruff_lint_read_only" in skipped.checked_rules:
        raise AssertionError("SKIPPED_RUFF_FALSELY_CLAIMED_LINT_EXECUTION")
    if "ruff_format_check_read_only" in skipped.checked_rules:
        raise AssertionError("SKIPPED_RUFF_FALSELY_CLAIMED_FORMAT_EXECUTION")
    integrated = _integrated_result(fixture, preview, clean)
    if integrated.status != "post_apply_validated":
        raise AssertionError("MISSING_POLICY_BLOCKED_WORKBENCH_INTEGRATION")
    if "POST_APPLY_RUFF_POLICY_NOT_CONFIGURED" not in integrated.warnings:
        raise AssertionError("MISSING_POLICY_INTEGRATION_WARNING_MISSING")
    shutil.copy2(project_root / "ruff.toml", fixture / "ruff.toml")


def _validate_workbench_integration(
    fixture: Path,
    preview: Path,
    clean: Path,
    lint_bad: Path,
    ruff: Path,
) -> None:
    previous = os.environ.get("KANDA_RUFF_EXECUTABLE")
    os.environ["KANDA_RUFF_EXECUTABLE"] = str(ruff)
    try:
        clean_result = _integrated_result(fixture, preview, clean)
        if clean_result.status != "post_apply_validated":
            raise AssertionError(
                "CLEAN_INTEGRATION_BLOCKED:" + "|".join(clean_result.blockers)
            )
        if "ruff_lint_read_only" not in clean_result.checked_rules:
            raise AssertionError("RUFF_RULES_NOT_MERGED")

        blocked_result = _integrated_result(fixture, preview, lint_bad)
        if blocked_result.status != "blocked":
            raise AssertionError("LINT_FAILURE_DID_NOT_BLOCK_POST_APPLY")
        if "POST_APPLY_RUFF_LINT_BLOCKED" not in blocked_result.blockers:
            raise AssertionError("LINT_BLOCKER_NOT_PROPAGATED")
        rollback = preview / "SOURCE_APPLY_ROLLBACK_MANIFEST.json"
        if not rollback.is_file():
            raise AssertionError("ROLLBACK_MANIFEST_LOST_AFTER_RUFF_BLOCK")
    finally:
        if previous is None:
            os.environ.pop("KANDA_RUFF_EXECUTABLE", None)
        else:
            os.environ["KANDA_RUFF_EXECUTABLE"] = previous


def _integrated_result(
    fixture: Path,
    preview: Path,
    source: Path,
) -> PostApplyValidationResult:
    digest = _sha256(source)
    rollback = preview / "SOURCE_APPLY_ROLLBACK_MANIFEST.json"
    rollback.write_text("{}\n", encoding="utf-8")
    payload_manifest = preview / "SOURCE_APPLY_PAYLOAD_MANIFEST.json"
    payload_manifest.write_text("{}\n", encoding="utf-8")
    execution = preview / "SOURCE_APPLY_EXECUTION_MANIFEST.json"
    execution.write_text("{}\n", encoding="utf-8")
    apply_result = GuardedSourceApplyResult(
        schema_version=SCHEMA_VERSION,
        feature_id=GUARDED_SOURCE_APPLY_FEATURE_ID,
        status="applied",
        target_file=str(source),
        source_content_hash_before=digest,
        source_content_hash_after=digest,
        preview_root=str(preview),
        payload_manifest_path=str(payload_manifest),
        rollback_manifest_path=str(rollback),
        execution_manifest_path=str(execution),
        expected_confirmation_token="TOKEN",
        confirmation_token_present=True,
        confirmation_token_valid=True,
        source_mutation_enabled=True,
        import_rewrite_enabled=False,
        written_files=[str(source)],
    )
    file_record = SourceApplyPayloadFile(
        payload_path=str(preview / source.name),
        destination_path=str(source),
        relative_path=source.name,
        content_hash=digest,
        physical_lines=len(source.read_text(encoding="utf-8").splitlines()),
        compile_ok=True,
        ast_parse_ok=True,
        role="facade",
    )
    payload = SourceApplyPayloadReadinessResult(
        schema_version=SCHEMA_VERSION,
        feature_id=SOURCE_PAYLOAD_READINESS_FEATURE_ID,
        status="source_apply_payload_ready",
        target_file=str(source),
        source_content_hash=digest,
        preview_root=str(preview),
        payload_root=str(preview / "source_apply_payload"),
        payload_manifest_path=str(payload_manifest),
        structural_validation_status="passed",
        behavior_status="BEHAVIOR_VALIDATION_NOT_RUN",
        preflight_backup_status="preflight_backup_ready",
        source_hash_verified=True,
        files=[file_record],
    )
    return validate_and_write_post_apply(
        apply_result=apply_result,
        source_payload=payload,
        active_project_root=str(fixture),
    )


def _sha256(path: Path) -> str:
    """Return one file SHA-256 digest."""
    return hashlib.sha256(path.read_bytes()).hexdigest()
