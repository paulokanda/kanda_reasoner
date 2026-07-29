"""End-to-end independent Portable workflow."""

from __future__ import annotations

import shutil
import sys
from argparse import Namespace
from pathlib import Path

from portable.archive import (
    create_windows_zip,
    extract_and_smoke,
    validate_zip,
)
from portable.build import build_application, stage_application
from portable.destination import select_output_directory
from portable.environment import (
    check_output_collision,
    confirm_explicit_request,
    require_environment,
)
from portable.models import BuildPaths, ZipEvidence
from portable.paths import print_identity, resolve_paths
from portable.publish import publish_candidate
from portable.snapshots import (
    assert_unchanged,
    metadata_snapshot,
    project_snapshot,
)


def _print_result(paths: BuildPaths, evidence: ZipEvidence) -> None:
    print("PORTABLE ATOMIC PUBLICATION: PASS")
    print("PORTABLE OWNER SEPARATION: PASS")
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
    print("STATUS: PORTABLE READY")


def run(*, project_root: Path, args: Namespace) -> int:
    """Run the complete build and publication lifecycle."""

    paths: BuildPaths | None = None
    try:
        confirm_explicit_request(args.yes)
        output_directory = select_output_directory(
            project_root,
            args.output_dir,
        )
        paths = resolve_paths(project_root, output_directory)
        print_identity(paths)
        require_environment(paths)
        check_output_collision(paths, args.replace_existing)

        project_before = project_snapshot(paths.project_root)
        support_before = metadata_snapshot(paths.project_support_root)

        application = build_application(paths)
        stage_app = stage_application(paths, application)
        create_windows_zip(paths, stage_app)
        candidate_evidence = validate_zip(paths.candidate_zip)
        extract_and_smoke(paths, candidate_evidence)

        assert_unchanged(
            "PORTABLE PROJECT SOURCE UNCHANGED",
            project_before,
            project_snapshot(paths.project_root),
        )
        assert_unchanged(
            "SHOW PROJECT SUPPORT UNCHANGED",
            support_before,
            metadata_snapshot(paths.project_support_root),
        )

        final_evidence = publish_candidate(paths, candidate_evidence)

        assert_unchanged(
            "PORTABLE PROJECT SOURCE UNCHANGED AFTER PUBLICATION",
            project_before,
            project_snapshot(paths.project_root),
        )
        assert_unchanged(
            "SHOW PROJECT SUPPORT UNCHANGED AFTER PUBLICATION",
            support_before,
            metadata_snapshot(paths.project_support_root),
        )

        _print_result(paths, final_evidence)

        if args.keep_staging:
            print(f"PORTABLE STAGING RETAINED: {paths.run_root}")
        else:
            shutil.rmtree(paths.run_root, ignore_errors=True)
        return 0
    except Exception as exc:
        print("PORTABLE BUILD ERROR", file=sys.stderr)
        print(f"ERROR TYPE: {type(exc).__name__}", file=sys.stderr)
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
