# project-path: kanda_reasoner_app/project_fire_shield_cli.py
"""Command-line provider for the public Fire Shield authority."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from kanda_reasoner_app.project_fire_shield import (
    FIRE_SHIELD_FEATURE_ID,
    FireShieldError,
    FireShieldPhase,
    build_fire_shield_context,
    capture_tool_snapshot,
    preflight_fire_shield_archive,
    verify_project_import_isolation,
)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="KANDA Fire Shield provider")
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--tool-root", required=True)
    parser.add_argument("--registry-path")
    subparsers = parser.add_subparsers(dest="command", required=True)

    preflight = subparsers.add_parser("preflight")
    preflight.add_argument("--phase", required=True, choices=[item.value for item in FireShieldPhase])
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
    context = _context(args, FireShieldPhase.PROJECT_SOURCE_MUTATION)
    _print_context(context)
    report = preflight_fire_shield_archive(context, args.archive_path)
    print("FIRE_SHIELD_ARCHIVE_CONTAINMENT: PASS")
    print("FIRE_SHIELD_TOOL_SOURCE_TRANSFER: ZERO")
    print("FIRE_SHIELD_PROJECT_TOOL_PRIVATE_IMPORTS: ZERO")
    print("FIRE_SHIELD_PROJECT_PAYLOAD_FILES: " + str(report.project_payload_count))
    print("FIRE_SHIELD_PACKAGE_PREFLIGHT: PASS")


def _run_isolation(args: argparse.Namespace) -> None:
    context = _context(args, FireShieldPhase.VALIDATE_READ_ONLY)
    verify_project_import_isolation(context, tuple(args.search_path))
    _print_context(context)
    print("FIRE_SHIELD_PROJECT_TOOL_PATH_LEAK: ZERO")
    print("FIRE_SHIELD_PROJECT_IMPORT_ISOLATION: PASS")


def _run_tool_digest(args: argparse.Namespace) -> None:
    context = _context(args, FireShieldPhase.PROJECT_SOURCE_MUTATION)
    snapshot = context.tool_snapshot
    if snapshot is None:
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
    """Run one Fire Shield provider operation."""
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
    except (FireShieldError, OSError, ValueError) as exc:
        print("FIRE_SHIELD_STATUS: BLOCKED", file=sys.stderr)
        print(str(exc), file=sys.stderr)
        return 2
    print("FIRE_SHIELD_STATUS: PASS")
    print("FIRE_SHIELD_FEATURE_ID: " + FIRE_SHIELD_FEATURE_ID)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
