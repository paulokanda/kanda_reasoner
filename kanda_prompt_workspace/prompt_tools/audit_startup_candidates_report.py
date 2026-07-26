"""Report rendering helpers for startup prompt candidate audits."""

from __future__ import annotations
__all__: list[str] = []


import json
from pathlib import Path

from .audit_startup_candidates_models import AuditResult, SourceMapEntry, StartupCandidate, utc_now_iso
from .audit_startup_candidates_paths import normalize_rel_path
from .audit_startup_candidates_source_map import suggested_next_filename_number, suggested_next_load_order

def append_items(lines: list[str], items: list[str]) -> None:
    if items:
        for item in items:
            lines.append(f"- {item}")
    else:
        lines.append("- None")

def proposed_entry_for_candidate(candidate: StartupCandidate, load_order: int) -> dict[str, Any]:
    return {
        "load_order": load_order,
        "canonical_source": candidate.canonical_source,
        "generated_filename": candidate.generated_filename,
        "prompt_id": candidate.prompt_id,
        "load_mode": candidate.load_mode,
        "role": candidate.role,
    }

def create_report(
    workspace_root: Path,
    source_map_path: Path,
    entries: list[SourceMapEntry],
    result: AuditResult,
) -> str:
    now = utc_now_iso()
    next_order = suggested_next_load_order(entries)
    next_number = suggested_next_filename_number(entries)

    lines: list[str] = []
    lines.append("# STARTUP_ROUTING_KERNEL_SOURCES Update Candidate Report")
    lines.append("")
    lines.append(f"Generated: {now}")
    lines.append(f"Workspace root: {workspace_root}")
    lines.append(f"Source map: {source_map_path}")
    lines.append(f"Source map SHA-256: {result.source_map_sha256}")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Current source-map entries: {len(entries)}")
    lines.append(f"- Existing marked candidates already mapped: {len(result.existing_candidates)}")
    lines.append(f"- Missing marked candidates: {len(result.missing_candidates)}")
    lines.append(f"- Stale source-map entries: {len(result.stale_entries)}")
    lines.append(f"- Source-map errors: {len(result.source_map_errors)}")
    lines.append(f"- Candidate errors: {len(result.candidate_errors)}")
    lines.append(f"- Warnings: {len(result.source_map_warnings) + len(result.sidecar_warnings) + len(result.candidate_warnings)}")
    lines.append(f"- Suggested next load_order: {next_order}")
    lines.append(f"- Suggested next filename number: {next_number:02d}")
    lines.append("")
    lines.append("## Status meaning")
    lines.append("")
    lines.append("- NO_UPDATE_NEEDED means no marked candidate is missing from the source map.")
    lines.append("- UPDATE_CANDIDATE_FOUND means one or more marked candidates need human review.")
    lines.append("- AUDIT_ERRORS means source-map or candidate errors must be fixed before changes.")
    lines.append("")
    lines.append("## Source-map errors")
    lines.append("")
    append_items(lines, result.source_map_errors)
    lines.append("")
    lines.append("## Candidate errors")
    lines.append("")
    append_items(lines, result.candidate_errors)
    lines.append("")
    lines.append("## Source-map warnings")
    lines.append("")
    append_items(lines, result.source_map_warnings)
    lines.append("")
    lines.append("## Sidecar warnings")
    lines.append("")
    append_items(lines, result.sidecar_warnings)
    lines.append("")
    lines.append("## Candidate warnings")
    lines.append("")
    append_items(lines, result.candidate_warnings)
    lines.append("")
    lines.append("## Stale source-map entries")
    lines.append("")
    append_items(lines, result.stale_entries)
    lines.append("")
    lines.append("## Existing marked candidates already in source map")
    lines.append("")
    if result.existing_candidates:
        for candidate in result.existing_candidates:
            lines.append(f"- {candidate.prompt_id}: {candidate.canonical_source}")
    else:
        lines.append("- None")
    lines.append("")
    lines.append("## Missing startup candidates")
    lines.append("")
    if result.missing_candidates:
        for index, candidate in enumerate(result.missing_candidates, start=0):
            proposed_order = next_order + index
            lines.append(f"### {candidate.prompt_id}")
            lines.append("")
            lines.append(f"- canonical_source: `{candidate.canonical_source}`")
            lines.append(f"- generated_filename: `{candidate.generated_filename}`")
            lines.append(f"- prompt_id: `{candidate.prompt_id}`")
            lines.append(f"- load_mode: `{candidate.load_mode}`")
            lines.append(f"- role: `{candidate.role}`")
            lines.append(f"- sidecar: `{normalize_rel_path(candidate.sidecar_path, workspace_root)}`")
            lines.append(f"- size_bytes: {candidate.size_bytes}")
            lines.append(f"- suggested load_order if accepted: {proposed_order}")
            lines.append("")
            lines.append("Suggested JSON entry for manual review:")
            lines.append("")
            lines.append("```json")
            lines.append(json.dumps(
                {
                    "load_order": proposed_order,
                    "canonical_source": candidate.canonical_source,
                    "generated_filename": candidate.generated_filename,
                    "prompt_id": candidate.prompt_id,
                    "load_mode": candidate.load_mode,
                    "role": candidate.role,
                },
                indent=2,
                ensure_ascii=False,
            ))
            lines.append("```")
            lines.append("")
    else:
        lines.append("- None")
    lines.append("")
    lines.append("## Ignored sidecars")
    lines.append("")
    append_items(lines, result.ignored_sidecars)
    lines.append("")
    lines.append("## Required human workflow")
    lines.append("")
    lines.append("1. Review this report.")
    lines.append("2. If a missing candidate should be startup-loaded, manually edit STARTUP_ROUTING_KERNEL_SOURCES.json.")
    lines.append("3. Re-run this auditor until no unexpected missing candidates remain.")
    lines.append("4. Then run sync_startup_routing_kernel_pack.py --ensure-sync --yes.")
    lines.append("")
    return "\n".join(lines) + "\n"

def explain_missing_candidates(workspace_root: Path, entries: list[SourceMapEntry], result: AuditResult) -> None:
    next_order = suggested_next_load_order(entries)
    print("")
    print("STARTUP CANDIDATES FOUND")
    print("These prompts have explicit .meta.json startup sidecars but are not in STARTUP_ROUTING_KERNEL_SOURCES.json.")
    print("Only answer YES if they should be loaded in every future startup ZIP.")
    print("")
    for index, candidate in enumerate(result.missing_candidates, start=0):
        proposed_order = next_order + index
        print(f"Candidate {index + 1}:")
        print(f"  canonical_source: {candidate.canonical_source}")
        print(f"  generated_filename: {candidate.generated_filename}")
        print(f"  prompt_id: {candidate.prompt_id}")
        print(f"  load_mode: {candidate.load_mode}")
        print(f"  role: {candidate.role}")
        print(f"  sidecar: {normalize_rel_path(candidate.sidecar_path, workspace_root)}")
        print(f"  size_bytes: {candidate.size_bytes}")
        print(f"  proposed load_order: {proposed_order}")
        print("  proposed source-map entry:")
        print(json.dumps(proposed_entry_for_candidate(candidate, proposed_order), indent=2, ensure_ascii=False))
        print("")

def ask_yes_no() -> bool:
    try:
        answer = input("Update STARTUP_ROUTING_KERNEL_SOURCES.json with these candidates and regenerate startup delivery? Type YES to proceed: ")
    except EOFError:
        print("No interactive answer was provided. No changes were applied.")
        return False
    return answer.strip() == "YES"
