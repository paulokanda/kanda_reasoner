"""Command runner for startup prompt candidate audits."""

from __future__ import annotations
__all__: list[str] = []


import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

from .audit_startup_candidates_models import (
    MAX_STARTUP_SOURCES_WARNING,
    REPORT_FILENAME,
    SOURCE_MAP_FILENAME,
    SYNC_SCRIPT_FILENAME,
    TOOLS_DIR_NAME,
    AuditResult,
    SourceMapEntry,
    StartupCandidate,
    read_text_utf8_strict,
    sha256_file,
    write_text_utf8,
)
from .audit_startup_candidates_paths import detect_workspace_root
from .audit_startup_candidates_source_map import (
    detect_stale_entries,
    load_source_map_object,
    parse_source_map,
    suggested_next_load_order,
)
from .audit_startup_candidates_sidecars import compare_candidates_to_source_map, find_sidecar_candidates
from .audit_startup_candidates_report import (
    ask_yes_no,
    create_report,
    explain_missing_candidates,
    proposed_entry_for_candidate,
)

def atomic_write_text(path: Path, text: str) -> None:
    tmp_path = path.with_name(path.name + ".tmp")
    write_text_utf8(tmp_path, text)
    os.replace(tmp_path, path)

def run_audit(workspace_root: Path, report_filename: str) -> tuple[int, str, Path, list[SourceMapEntry], AuditResult]:
    source_map_path = workspace_root / TOOLS_DIR_NAME / SOURCE_MAP_FILENAME
    report_path = workspace_root / TOOLS_DIR_NAME / report_filename
    source_map_sha256 = sha256_file(source_map_path)

    entries, source_errors, source_warnings = parse_source_map(source_map_path)
    stale_entries = detect_stale_entries(workspace_root, entries)

    candidates: list[StartupCandidate] = []
    candidate_errors: list[str] = []
    sidecar_warnings: list[str] = []
    ignored_sidecars: list[str] = []
    candidate_warnings: list[str] = []
    existing_candidates: list[StartupCandidate] = []
    missing_candidates: list[StartupCandidate] = []

    if not source_errors:
        candidates, candidate_errors, sidecar_warnings, ignored_sidecars = find_sidecar_candidates(workspace_root)
        existing_candidates, missing_candidates, compare_warnings = compare_candidates_to_source_map(entries, candidates)
        candidate_warnings.extend(compare_warnings)

        if len(entries) + len(missing_candidates) > MAX_STARTUP_SOURCES_WARNING:
            candidate_warnings.append(
                "Adding all missing candidates would exceed the recommended startup source count "
                f"of {MAX_STARTUP_SOURCES_WARNING}."
            )

    result = AuditResult(
        source_map_errors=source_errors,
        source_map_warnings=source_warnings,
        sidecar_warnings=sidecar_warnings,
        candidate_errors=candidate_errors,
        candidate_warnings=candidate_warnings,
        stale_entries=stale_entries,
        existing_candidates=existing_candidates,
        missing_candidates=missing_candidates,
        ignored_sidecars=ignored_sidecars,
        source_map_sha256=source_map_sha256,
        report_path=report_path,
    )

    report = create_report(workspace_root, source_map_path, entries, result)
    write_text_utf8(report_path, report)

    if source_errors or candidate_errors:
        return 2, "AUDIT_ERRORS", report_path, entries, result
    if missing_candidates:
        return 1, "UPDATE_CANDIDATE_FOUND", report_path, entries, result
    return 0, "NO_UPDATE_NEEDED", report_path, entries, result

def update_source_map_with_candidates(
    workspace_root: Path,
    entries: list[SourceMapEntry],
    candidates: list[StartupCandidate],
) -> Path:
    source_map_path = workspace_root / TOOLS_DIR_NAME / SOURCE_MAP_FILENAME
    original_text = read_text_utf8_strict(source_map_path)
    source_map = load_source_map_object(source_map_path)
    source_map.setdefault("schema_version", 1)
    sources = list(source_map["startup_sources"])
    next_order = suggested_next_load_order(entries)

    for index, candidate in enumerate(candidates, start=0):
        sources.append(proposed_entry_for_candidate(candidate, next_order + index))

    source_map["startup_sources"] = sources
    new_text = json.dumps(source_map, indent=2, ensure_ascii=False) + "\n"

    atomic_write_text(source_map_path, new_text)
    try:
        _new_entries, new_errors, _new_warnings = parse_source_map(source_map_path)
        if new_errors:
            raise ValueError("Updated source map failed validation: " + "; ".join(new_errors))
    except Exception:
        atomic_write_text(source_map_path, original_text)
        raise

    return source_map_path

def run_sync_generator(workspace_root: Path) -> int:
    sync_script = workspace_root / TOOLS_DIR_NAME / SYNC_SCRIPT_FILENAME
    if not sync_script.exists():
        print(f"SYNC FAILED: missing generator: {sync_script}")
        return 3

    command = [
        sys.executable,
        str(sync_script),
        "--ensure-sync",
        "--yes",
    ]
    print("")
    print("RUNNING STARTUP DELIVERY SYNC")
    print("Command: python .\\prompt_tools\\sync_startup_routing_kernel_pack.py --ensure-sync --yes")
    sys.stdout.flush()
    completed = subprocess.run(command, cwd=str(workspace_root), text=True, check=False)
    return int(completed.returncode)

def handle_interactive_update(
    workspace_root: Path,
    entries: list[SourceMapEntry],
    result: AuditResult,
) -> int:
    explain_missing_candidates(workspace_root, entries, result)
    if not ask_yes_no():
        print("UPDATE CANCELLED BY HUMAN")
        print("No source-map or delivery files were changed.")
        print("EXIT_CODE: 1")
        return 1

    try:
        updated_path = update_source_map_with_candidates(workspace_root, entries, result.missing_candidates)
    except (OSError, ValueError, json.JSONDecodeError, UnicodeDecodeError) as exc:
        print("SOURCE MAP UPDATE FAILED")
        print(f"ERROR: {exc}")
        print("EXIT_CODE: 3")
        return 3

    print("")
    print("SOURCE MAP UPDATE OK")
    print(f"Updated: {updated_path}")
    sys.stdout.flush()

    sync_code = run_sync_generator(workspace_root)
    if sync_code != 0:
        print("SYNC FAILED")
        print("STARTUP_ROUTING_KERNEL_SOURCES.json was updated, but startup delivery regeneration failed.")
        print(f"EXIT_CODE: {sync_code}")
        return sync_code

    print("")
    print("SYNC OK")
    print("STARTUP ROUTING KERNEL SOURCE MAP UPDATE COMPLETE")
    print("EXIT_CODE: 0")
    return 0

def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Audit explicit startup routing kernel candidates and optionally update after YES confirmation."
    )
    parser.add_argument(
        "--workspace",
        type=Path,
        default=None,
        help="Workspace root containing prompt_library and prompt_tools.",
    )
    parser.add_argument(
        "--report-filename",
        default=REPORT_FILENAME,
        help="Report filename written inside prompt_tools.",
    )
    parser.add_argument(
        "--report",
        action="store_true",
        help="Report-only mode. Do not ask to update the source map.",
    )
    parser.add_argument(
        "--no-interactive",
        action="store_true",
        help="Do not ask to update candidates; write report and return status only.",
    )
    return parser.parse_args(argv)

def main(argv: list[str]) -> int:
    args = parse_args(argv)

    try:
        workspace_root = detect_workspace_root(Path(__file__).resolve(), args.workspace)
        code, status, report_path, entries, result = run_audit(workspace_root, args.report_filename)

        print("STARTUP ROUTING KERNEL CANDIDATE AUDIT")
        print(f"Workspace root: {workspace_root}")
        print(f"Report: {report_path}")
        print(f"STATUS: {status}")
        print(f"EXIT_CODE: {code}")

        if status == "UPDATE_CANDIDATE_FOUND" and not args.report and not args.no_interactive:
            return handle_interactive_update(workspace_root, entries, result)

        return code

    except (OSError, ValueError, json.JSONDecodeError, UnicodeDecodeError) as exc:
        print("STARTUP ROUTING KERNEL CANDIDATE AUDIT")
        print("STATUS: AUDIT_FATAL_ERROR")
        print(f"ERROR: {exc}")
        print("EXIT_CODE: 2")
        return 2
