# project-path: kanda_reasoner_app/project_fire_shield_cli.py
"""Command-line provider for spectator-only Fire Shield checks."""

from __future__ import annotations

import argparse
import sys
import zipfile
from pathlib import Path

from kanda_reasoner_app.archive_safety import (
    ArchiveSafetyError,
    validate_archive_members,
)
from kanda_reasoner_app.project_fire_shield import (
    FIRE_SHIELD_FEATURE_ID,
    FireShieldError,
    FireShieldPhase,
    assert_fire_shield_payload_bytes_allowed,
    build_fire_shield_context,
    capture_tool_snapshot,
    verify_project_import_isolation,
)

_SPECTATOR_PHASE_CHOICES = (
    "PROJECT_TRANSIENT_WRITE",
    "FREEZE_WRITE",
    "ERROR_MEMORY_WRITE",
    "VALIDATE_READ_ONLY",
)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="KANDA Fire Shield spectator provider")
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--tool-root", required=True)
    parser.add_argument("--registry-path")
    subparsers = parser.add_subparsers(dest="command", required=True)

    preflight = subparsers.add_parser("preflight")
    preflight.add_argument("--phase", required=True, choices=_SPECTATOR_PHASE_CHOICES)
    preflight.add_argument("--operation-id", required=True)

    scan = subparsers.add_parser("scan-package")
    scan.add_argument("--zip", required=True, dest="archive_path")
    scan.add_argument("--operation-id", required=True)

    isolation = subparsers.add_parser("verify-project-isolation")
    isolation.add_argument("--search-path", action="append", default=[])
    isolation.add_argument("--operation-id", required=True)

    digest = subparsers.add_parser("tool-digest")
    digest.add_argument("--operation-id", required=True)

    verify = subparsers.add_parser("verify-tool")
    verify.add_argument("--expected-digest", required=True)
    verify.add_argument("--operation-id", required=True)
    return parser


def _context(args: argparse.Namespace, phase: FireShieldPhase):
    return build_fire_shield_context(
        Path(args.project_root),
        phase=phase,
        operation_id=args.operation_id,
        tool_source_root=Path(args.tool_root),
        registry_path=(Path(args.registry_path) if args.registry_path else None),
    )


def _print_context(context) -> None:
    for marker in context.markers():
        print(marker)


def _run_preflight(args: argparse.Namespace) -> None:
    context = _context(args, FireShieldPhase(args.phase))
    _print_context(context)
    print("FIRE_SHIELD_PREFLIGHT: PASS")


def _run_scan(args: argparse.Namespace) -> None:
    context = _context(args, FireShieldPhase.VALIDATE_READ_ONLY)
    _print_context(context)
    archive_path = Path(args.archive_path).expanduser().resolve(strict=True)
    payload_count = _scan_archive_payload_read_only(context, archive_path)
    print("FIRE_SHIELD_ARCHIVE_CONTAINMENT: PASS")
    print("FIRE_SHIELD_TOOL_SOURCE_TRANSFER: ZERO")
    print("FIRE_SHIELD_PROJECT_TOOL_PRIVATE_IMPORTS: ZERO")
    print("FIRE_SHIELD_PROJECT_PAYLOAD_FILES: " + str(payload_count))
    print("FIRE_SHIELD_PACKAGE_PREFLIGHT: SPECTATOR_READ_ONLY_PASS")


def _scan_archive_payload_read_only(context, archive_path: Path) -> int:
    """Validate package structure and payload bytes without write authority."""
    payload_count = 0
    try:
        with zipfile.ZipFile(archive_path, "r") as archive:
            bad_member = archive.testzip()
            if bad_member is not None:
                raise FireShieldError("FIRE_SHIELD_ARCHIVE_CRC_FAILED:" + bad_member)
            plans = validate_archive_members(
                archive,
                context.boundary.active_project_root,
                require_single_top_level=False,
                reject_windows_ambiguous_names=True,
            )
            for plan in plans:
                name = plan.normalized_name
                if plan.is_directory or not name.startswith("payload/"):
                    continue
                relative = name[len("payload/") :]
                if not relative:
                    continue
                assert_fire_shield_payload_bytes_allowed(
                    context,
                    archive.read(plan.info),
                    relative,
                )
                payload_count += 1
    except ArchiveSafetyError as exc:
        raise FireShieldError(str(exc)) from exc
    return payload_count


def _run_isolation(args: argparse.Namespace) -> None:
    context = _context(args, FireShieldPhase.VALIDATE_READ_ONLY)
    verify_project_import_isolation(context, tuple(args.search_path))
    _print_context(context)
    print("FIRE_SHIELD_PROJECT_TOOL_PATH_LEAK: ZERO")
    print("FIRE_SHIELD_PROJECT_IMPORT_ISOLATION: PASS")


def _run_tool_digest(args: argparse.Namespace) -> None:
    context = _context(args, FireShieldPhase.VALIDATE_READ_ONLY)
    snapshot = capture_tool_snapshot(context.boundary.tool_source_root)
    _print_context(context)
    print("FIRE_SHIELD_TOOL_SNAPSHOT_FILES: " + str(len(snapshot.entries)))
    print("FIRE_SHIELD_TOOL_SNAPSHOT_SHA256: " + snapshot.digest_sha256)


def _run_verify_tool(args: argparse.Namespace) -> None:
    context = _context(args, FireShieldPhase.VALIDATE_READ_ONLY)
    current = capture_tool_snapshot(context.boundary.tool_source_root)
    expected = str(args.expected_digest or "").strip().lower()
    if not expected or current.digest_sha256.lower() != expected:
        raise FireShieldError("FIRE_SHIELD_TOOL_MUTATION_DETECTED")
    _print_context(context)
    print("FIRE_SHIELD_TOOL_POST_STATE_UNCHANGED: PASS")


def main(argv: list[str] | None = None) -> int:
    """Run one spectator-only Fire Shield provider operation."""
    args = _parser().parse_args(argv)
    handlers = {
        "preflight": _run_preflight,
        "scan-package": _run_scan,
        "verify-project-isolation": _run_isolation,
        "tool-digest": _run_tool_digest,
        "verify-tool": _run_verify_tool,
    }
    try:
        handlers[args.command](args)
    except (FireShieldError, OSError, ValueError, zipfile.BadZipFile) as exc:
        print("FIRE_SHIELD_STATUS: BLOCKED", file=sys.stderr)
        print(str(exc), file=sys.stderr)
        return 2
    print("FIRE_SHIELD_STATUS: PASS")
    print("FIRE_SHIELD_FEATURE_ID: " + FIRE_SHIELD_FEATURE_ID)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
