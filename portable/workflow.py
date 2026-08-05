"""End-to-end independent Portable workflow with an atomic result receipt."""

from __future__ import annotations

import json
import os
import shutil
import sys
import uuid
from argparse import Namespace
from datetime import datetime, timezone
from pathlib import Path

from portable.archive import (
    create_windows_zip,
    extract_and_smoke,
    validate_zip,
)
from portable.build import build_application, stage_application
from portable.constants import (
    BUILDER_VERSION,
    FEATURE_ID,
    PORTABLE_HARDENING_STAGE,
    PRODUCTION_PORTABLE_ENABLED,
)
from portable.destination import select_output_directory
from portable.environment import (
    check_output_collision,
    confirm_explicit_request,
    print_builder_identity,
    require_environment,
)
from portable.errors import PortableBuildError
from portable.governed_root_rollback import (
    GovernedRootRollbackGuard,
    prepare_governed_root_rollback,
)
from portable.models import BuildPaths, RegistryBoundary, ZipEvidence
from portable.paths import print_identity, resolve_paths
from portable.publish import publish_candidate
from portable.registry_boundary import (
    assert_registry_unchanged,
    load_registry_boundary,
    validate_result_path,
)
from portable.snapshots import (
    assert_unchanged,
    metadata_snapshot,
    project_snapshot,
)


def _utc_now() -> str:
    return (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def _resolve_result_path(
    requested: Path | None,
    boundary: RegistryBoundary,
) -> Path | None:
    """Validate result path before parent creation or any temporary write."""

    if requested is None:
        return None

    result_path = validate_result_path(requested, boundary)
    assert_registry_unchanged(boundary)
    result_path.parent.mkdir(parents=True, exist_ok=True)
    print("PORTABLE RESULT JSON REGISTRY BOUNDARY: PASS")
    return result_path


def _write_result(
    result_path: Path | None,
    payload: dict[str, object],
) -> None:
    if result_path is None:
        return

    temporary = result_path.with_name(
        f".{result_path.name}.{uuid.uuid4().hex}.partial"
    )
    encoded = json.dumps(
        payload,
        indent=2,
        sort_keys=True,
    ) + "\n"
    try:
        temporary.write_text(
            encoded,
            encoding="utf-8",
            newline="\n",
        )
        json.loads(temporary.read_text(encoding="utf-8"))
        os.replace(temporary, result_path)
    finally:
        temporary.unlink(missing_ok=True)


def _print_result(
    paths: BuildPaths,
    evidence: ZipEvidence,
    result_path: Path | None,
) -> None:
    print("PORTABLE ATOMIC PUBLICATION: PASS")
    print("PORTABLE OWNER SEPARATION: PASS")
    print("PORTABLE EXPLICIT SELF-HOSTING AUTHORITY: PASS")
    print("PORTABLE ALL REGISTERED OWNER ROOTS PROTECTED: PASS")
    print("PORTABLE DESTINATION PROBE AFTER BOUNDARY CHECK: PASS")
    print("PORTABLE OUTPUT USER-SELECTED FOLDER: PASS")
    print("PORTABLE OUTPUT OUTSIDE PROJECT ROOT: PASS")
    print("PORTABLE OUTPUT OUTSIDE PROJECT SUPPORT: PASS")
    print("PORTABLE BUILD RESULTS NOT MERGED INTO PROJECT: PASS")
    print("SHOW PROJECT WORKFLOW NOT INVOKED: PASS")
    print("SHOW PROJECT SUPPORT UNCHANGED BY PORTABLE BUILD: PASS")
    print(f"PORTABLE OUTPUT: {paths.final_zip}")
    print(f"PORTABLE ZIP SIZE: {evidence.size_bytes} bytes")
    print(f"PORTABLE ZIP SHA256: {evidence.sha256}")
    print(f"PORTABLE ZIP MEMBER COUNT: {evidence.member_count}")
    print(
        "PORTABLE MAXIMUM MEMBER PATH: "
        f"{evidence.maximum_path_bytes} bytes"
    )
    if result_path is not None:
        print(f"PORTABLE RESULT JSON: {result_path}")
    print("STATUS: PORTABLE READY")


def run(*, project_root: Path, args: Namespace) -> int:
    """Run the complete build and publication lifecycle."""

    paths: BuildPaths | None = None
    result_path: Path | None = None
    project_before: dict[str, object] | None = None
    support_before: dict[str, object] | None = None
    boundary: RegistryBoundary | None = None
    smoke_evidence: dict[str, object] | None = None
    governed_guard: GovernedRootRollbackGuard | None = None
    governed_checkpoints: list[dict[str, object]] = []
    governed_failure_rollback: dict[str, object] | None = None
    external_control_evidence: dict[str, object] | None = None

    try:
        boundary = load_registry_boundary(project_root)
        print_builder_identity()
        print(f"PORTABLE HARDENING STAGE: {PORTABLE_HARDENING_STAGE}")
        print("PORTABLE EXPLICIT SELF-HOSTING AUTHORITY: PASS")
        print("PORTABLE ALL REGISTERED OWNER ROOTS LOADED: PASS")
        if not PRODUCTION_PORTABLE_ENABLED:
            raise PortableBuildError(
                "Production Portable creation remains intentionally blocked until "
                "the final readiness authorization is explicitly validated after all "
                "hardening stages are frozen and memorized."
            )
        confirm_explicit_request(args.yes)
        result_path = _resolve_result_path(
            args.result_json,
            boundary,
        )
        output_directory = select_output_directory(
            project_root,
            args.output_dir,
            boundary,
        )
        paths = resolve_paths(
            project_root,
            output_directory,
            boundary,
        )
        print_identity(paths)
        external_control_evidence = require_environment(paths)
        check_output_collision(paths, args.replace_existing)

        project_before = project_snapshot(paths.project_root)
        support_before = metadata_snapshot(
            paths.project_support_root
        )
        governed_guard = prepare_governed_root_rollback(paths)
        governed_checkpoints.append(
            governed_guard.checkpoint(
                "PORTABLE GOVERNED ROOTS UNCHANGED BEFORE BUILD"
            )
        )

        application = build_application(paths)
        stage_app = stage_application(paths, application)
        create_windows_zip(paths, stage_app)
        candidate_evidence = validate_zip(paths.candidate_zip)
        governed_checkpoints.append(
            governed_guard.checkpoint(
                "PORTABLE GOVERNED ROOTS UNCHANGED AFTER BUILD"
            )
        )
        smoke_evidence = extract_and_smoke(paths, candidate_evidence)
        governed_checkpoints.append(
            governed_guard.checkpoint(
                "PORTABLE GOVERNED ROOTS UNCHANGED AFTER SMOKE"
            )
        )

        project_after_smoke = project_snapshot(
            paths.project_root
        )
        support_after_smoke = metadata_snapshot(
            paths.project_support_root
        )
        assert_unchanged(
            "PORTABLE PROJECT SOURCE UNCHANGED",
            project_before,
            project_after_smoke,
        )
        assert_unchanged(
            "SHOW PROJECT SUPPORT UNCHANGED",
            support_before,
            support_after_smoke,
        )

        final_evidence = publish_candidate(
            paths,
            candidate_evidence,
        )
        governed_checkpoints.append(
            governed_guard.checkpoint(
                "PORTABLE GOVERNED ROOTS UNCHANGED AFTER PUBLICATION"
            )
        )

        project_after_publication = project_snapshot(
            paths.project_root
        )
        support_after_publication = metadata_snapshot(
            paths.project_support_root
        )
        assert_unchanged(
            "PORTABLE PROJECT SOURCE UNCHANGED AFTER PUBLICATION",
            project_before,
            project_after_publication,
        )
        assert_unchanged(
            "SHOW PROJECT SUPPORT UNCHANGED AFTER PUBLICATION",
            support_before,
            support_after_publication,
        )

        result_payload = {
            "schema_version": "1.0",
            "status": "portable_ready",
            "completed_at_utc": _utc_now(),
            "builder_version": BUILDER_VERSION,
            "feature_id": FEATURE_ID,
            "project_root": str(paths.project_root),
            "project_support_root": str(
                paths.project_support_root
            ),
            "registry_path": str(
                paths.registry_boundary.registry_path
            ),
            "registry_sha256": (
                paths.registry_boundary.registry_sha256
            ),
            "active_project_id": (
                paths.registry_boundary.current_project_id
            ),
            "selection_mode": (
                paths.registry_boundary.selection_mode
            ),
            "protected_registered_root_count": len(
                paths.registry_boundary.protected_roots
            ),
            "governed_root_rollback": governed_guard.evidence(),
            "external_build_controls": external_control_evidence,
            "governed_root_checkpoints": governed_checkpoints,
            "transient_root": str(paths.transient_root),
            "diagnostic_root": str(paths.run_root),
            "staging_retained": bool(args.keep_staging),
            "final_zip": str(paths.final_zip),
            "zip_sha256": final_evidence.sha256,
            "zip_size_bytes": final_evidence.size_bytes,
            "zip_member_count": final_evidence.member_count,
            "zip_maximum_path_bytes": (
                final_evidence.maximum_path_bytes
            ),
            "zip_top_level_name": (
                final_evidence.top_level_name
            ),
            "smoke_isolation": smoke_evidence,
            "smoke_tests": {
                "clean_extraction": True,
                "first_launch": True,
                "first_natural_close": True,
                "relaunch": True,
                "second_natural_close": True,
            },
            "project_snapshot_before": project_before,
            "project_snapshot_after_smoke": (
                project_after_smoke
            ),
            "project_snapshot_after_publication": (
                project_after_publication
            ),
            "smoke_isolation": smoke_evidence,
            "support_snapshot_before": support_before,
            "support_snapshot_after_smoke": (
                support_after_smoke
            ),
            "support_snapshot_after_publication": (
                support_after_publication
            ),
        }
        _write_result(result_path, result_payload)
        _print_result(paths, final_evidence, result_path)

        if args.keep_staging:
            print(f"PORTABLE STAGING RETAINED: {paths.run_root}")
        else:
            shutil.rmtree(paths.run_root, ignore_errors=True)
        return 0
    except Exception as exc:
        if governed_guard is not None:
            try:
                governed_failure_rollback = governed_guard.restore_if_changed(
                    "PORTABLE FAILURE GOVERNED ROOT EXACT ROLLBACK"
                )
            except Exception as rollback_exc:
                governed_failure_rollback = {
                    "status": "FAILED",
                    "error_type": type(rollback_exc).__name__,
                    "error_message": str(rollback_exc),
                }
                print("PORTABLE GOVERNED ROOT ROLLBACK FAILURE", file=sys.stderr)
                print(
                    f"ERROR TYPE: {type(rollback_exc).__name__}",
                    file=sys.stderr,
                )
                print(f"ERROR MESSAGE: {rollback_exc}", file=sys.stderr)
        failure_payload: dict[str, object] = {
            "schema_version": "1.0",
            "status": "failed",
            "completed_at_utc": _utc_now(),
            "builder_version": BUILDER_VERSION,
            "feature_id": FEATURE_ID,
            "error_type": type(exc).__name__,
            "error_message": str(exc),
            "project_root": str(project_root.resolve()),
            "registry_path": (
                str(boundary.registry_path)
                if boundary is not None
                else None
            ),
            "registry_sha256": (
                boundary.registry_sha256
                if boundary is not None
                else None
            ),
            "selection_mode": (
                boundary.selection_mode
                if boundary is not None
                else None
            ),
            "external_build_controls": external_control_evidence,
            "diagnostic_root": (
                str(paths.run_root)
                if paths is not None
                else None
            ),
            "project_snapshot_before": project_before,
            "support_snapshot_before": support_before,
            "governed_root_rollback": (
                governed_guard.evidence()
                if governed_guard is not None
                else None
            ),
            "governed_root_checkpoints": governed_checkpoints,
            "governed_failure_rollback": governed_failure_rollback,
        }
        try:
            _write_result(result_path, failure_payload)
        except Exception as result_exc:
            print(
                "PORTABLE RESULT JSON WRITE ERROR",
                file=sys.stderr,
            )
            print(
                f"ERROR TYPE: {type(result_exc).__name__}",
                file=sys.stderr,
            )
            print(
                f"ERROR MESSAGE: {result_exc}",
                file=sys.stderr,
            )

        print("PORTABLE BUILD ERROR", file=sys.stderr)
        print(
            f"ERROR TYPE: {type(exc).__name__}",
            file=sys.stderr,
        )
        print(f"ERROR MESSAGE: {exc}", file=sys.stderr)
        if paths is not None:
            print(
                f"DIAGNOSTIC ROOT RETAINED: {paths.run_root}",
                file=sys.stderr,
            )
        else:
            print(
                "DIAGNOSTIC ROOT: NOT CREATED",
                file=sys.stderr,
            )
        return 1
