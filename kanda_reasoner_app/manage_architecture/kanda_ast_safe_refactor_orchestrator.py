# project-path: kanda_reasoner_app/manage_architecture/kanda_ast_safe_refactor_orchestrator.py
"""Governed coordinator for AST-safe refactor evidence and verification stages.

The orchestrator is subordinate to Architecture Review -> Large Module AST Split
Audit. It sequences read-only evidence gathering and candidate verification. It
does not choose architecture, rewrite source, mutate queues, install patches, or
write frozen memory.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any, Mapping

from kanda_reasoner_app.manage_architecture.kanda_ast_safe_refactor_routine import (
    verify_candidate_family,
)
from kanda_reasoner_app.manage_architecture.kanda_refactor_probe_engine import (
    compare_probe_sets,
)
from kanda_reasoner_app.manage_architecture.kanda_refactor_project_index import (
    build_project_refactor_index,
)
from kanda_reasoner_app.manage_architecture.kanda_refactor_semantic_safety import (
    build_semantic_safety_evidence,
    evaluate_box_shielding,
)

__all__ = [
    "build_preflight_evidence",
    "build_preflight_evidence_text",
    "orchestrate_candidate_verification",
]

LINE_LAW = {
    "minimum_exclusive": 100,
    "maximum_exclusive": 500,
    "allowed_physical_lines": "101-499",
    "anti_gaming": "merge tiny responsibilities; split oversized responsibilities; never pad files",
}

ARCHITECTURE_OPTIONS = (
    "smallest_in_place_explicit_repair",
    "public_facade_plus_evaluation_helper",
    "public_facade_plus_invariants_helper",
    "public_facade_plus_evaluation_and_invariants_helpers",
    "domain_specific_alternative",
)

QUALITY_ATTRIBUTES = (
    "behavior_preservation",
    "modifiability",
    "auditability",
    "box_boundary_integrity",
    "installability",
    "recoverability",
    "determinism",
    "validation_portability",
)


def _sha256_text(text: str) -> str:
    """Return lowercase SHA-256 for UTF-8 text."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _audit_label(audit_text: str) -> str:
    """Extract the visible AST safety label from Markdown evidence."""
    match = re.search(r"^Label:\s*\*\*(.+?)\*\*\s*$", audit_text, re.MULTILINE)
    return match.group(1).strip() if match else "UNKNOWN"


def _audit_hard_blockers(audit_text: str) -> list[str]:
    """Extract bounded hard-blocker bullet text from AST audit Markdown."""
    marker = "Hard blockers:"
    if marker not in audit_text:
        return []
    tail = audit_text.split(marker, 1)[1]
    section = tail.split("\n\n", 1)[0].strip()
    if section.startswith("`none detected`") or section == "none detected":
        return []
    blockers = [
        line[2:].strip()
        for line in section.splitlines()
        if line.startswith("- ")
    ]
    return blockers[:25]


def _bounded_consumers(project_index: dict[str, Any]) -> dict[str, Any]:
    """Bound clipboard evidence while preserving counts and review warnings."""
    consumers = dict(project_index.get("consumers", {}))
    records = list(consumers.get("records", []))
    max_clipboard_records = 80
    consumers["records"] = records[:max_clipboard_records]
    consumers["clipboard_records_truncated"] = len(records) > max_clipboard_records
    return consumers


def _architecture_review_contract(
    semantic_evidence: dict[str, Any],
    project_index: dict[str, Any],
) -> dict[str, Any]:
    """Describe required AI judgment without automating architecture authority."""
    advisory_patterns = list(semantic_evidence.get("advisory_patterns", []))
    public_contract = dict(project_index.get("public_contract", {}))
    all_state = dict(public_contract.get("all_state", {}))
    review_warnings: list[str] = []
    if all_state.get("mode") == "UNRESOLVED_DYNAMIC":
        review_warnings.append("dynamic___all___requires_explicit_review")
    consumer_count = int(project_index.get("consumers", {}).get("record_count", 0))
    if consumer_count == 0:
        review_warnings.append("zero_consumers_found_requires_human_ai_confirmation")
    return {
        "architecture_authority": "web_ai_reasoning_plus_human_strategic_confirmation",
        "options_to_compare_when_nontrivial": list(ARCHITECTURE_OPTIONS),
        "quality_attributes_to_assess": list(QUALITY_ATTRIBUTES),
        "advisory_patterns": advisory_patterns,
        "review_warnings": review_warnings,
        "required_decision_record_fields": [
            "problem",
            "forces",
            "options_considered",
            "chosen_option",
            "rejected_options",
            "boundary_owner",
            "dependency_direction",
            "trade_offs",
            "line_size_forecast",
            "validation_obligations",
        ],
        "required_transformation_plan": True,
        "prerequisite_graph": "required_only_for_multi_prerequisite_refactors",
    }


def build_preflight_evidence(
    project_root: Path | str,
    *,
    target_relative_path: str,
    source_text: str,
    audit_text: str,
) -> dict[str, Any]:
    """Build one bounded read-only evidence packet for the Web AI handoff."""
    root = Path(project_root).resolve()
    target = (root / target_relative_path).resolve()
    try:
        target.relative_to(root)
    except ValueError as exc:
        raise ValueError("TARGET_OUTSIDE_ACTIVE_PROJECT_ROOT") from exc
    if not target.is_file():
        raise FileNotFoundError(str(target))
    current_source = target.read_text(encoding="utf-8", errors="strict")
    if current_source != source_text:
        raise ValueError("SOURCE_CHANGED_DURING_PREFLIGHT_EVIDENCE_BUILD")
    project_index = build_project_refactor_index(root, target_relative_path)
    semantic = build_semantic_safety_evidence(
        source_text,
        target_relative_path=target_relative_path,
    )
    compact_project_index = {
        "schema_version": project_index["schema_version"],
        "kind": project_index["kind"],
        "index_identity_sha256": project_index["index_identity_sha256"],
        "public_contract": project_index["public_contract"],
        "consumers": _bounded_consumers(project_index),
        "authority": project_index["authority"],
    }
    return {
        "schema_version": "1.0",
        "kind": "ast_safe_refactor_web_ai_preflight_evidence",
        "ownership": {
            "tab": "Architecture Review",
            "subtab": "Large Module AST Split Audit",
            "service_role": "subordinate_read_only_evidence_provider",
        },
        "target": {
            "relative_path": target_relative_path.replace("\\", "/"),
            "source_sha256": _sha256_text(source_text),
            "source_byte_length": len(source_text.encode("utf-8")),
        },
        "audit": {
            "markdown_sha256": _sha256_text(audit_text),
            "current_label": _audit_label(audit_text),
            "hard_blockers": _audit_hard_blockers(audit_text),
        },
        "project_index": compact_project_index,
        "semantic_safety": semantic,
        "architecture_review": _architecture_review_contract(semantic, project_index),
        "line_law": dict(LINE_LAW),
        "release_law": {
            "change_kind": "structural_refactor_only",
            "behavior_change_expected": False,
            "fresh_touched_family_ast_audit_required": True,
            "governed_zip_required": True,
            "freeze_write_requires_human_preview_and_confirm": True,
        },
        "authority": "evidence_for_web_ai_not_architecture_decision",
    }


def build_preflight_evidence_text(
    project_root: Path | str,
    *,
    target_relative_path: str,
    source_text: str,
    audit_text: str,
) -> str:
    """Return deterministic JSON text for insertion into the KPR clipboard wrapper."""
    payload = build_preflight_evidence(
        project_root,
        target_relative_path=target_relative_path,
        source_text=source_text,
        audit_text=audit_text,
    )
    return json.dumps(payload, indent=2, sort_keys=True)


def orchestrate_candidate_verification(
    project_root: Path | str,
    *,
    family_relative_paths: list[str],
    facade_relative_path: str,
    helper_relative_paths: list[str],
    behavior_comparison: dict[str, Any] | None = None,
    audit_output_dir: Path | str | None = None,
) -> dict[str, Any]:
    """Sequence family verification and optional explicit behavior evidence."""
    verification = verify_candidate_family(
        project_root,
        family_relative_paths,
        facade_relative_path=facade_relative_path,
        helper_relative_paths=helper_relative_paths,
        audit_output_dir=audit_output_dir,
    )
    behavior = behavior_comparison or {
        "kind": "ast_safe_refactor_behavior_equivalence",
        "pass": False,
        "status": "not_supplied",
    }
    fitness = {
        "SOURCE_FAMILY_FITNESS": bool(verification.get("pass", False)),
        "BEHAVIOR_EQUIVALENCE_FITNESS": bool(behavior.get("pass", False)),
        "DEPENDENCY_DIRECTION_FITNESS": bool(
            verification.get("dependency_direction", {}).get("pass", False)
        ),
        "LINE_LAW_101_499_FITNESS": all(
            bool(item.get("pass", False))
            for item in verification.get("line_law", [])
        ),
        "FRESH_FAMILY_AST_FITNESS": all(
            item.get("label") == "SAFE REFACTORING" and not item.get("hard_blockers")
            for item in verification.get("fresh_audits", [])
        ),
    }
    return {
        "schema_version": "1.0",
        "kind": "ast_safe_refactor_orchestrated_verification",
        "family_verification": verification,
        "behavior_comparison": behavior,
        "fitness_functions": fitness,
        "pass": all(fitness.values()),
    }


def compare_existing_probe_observations(
    baseline: Mapping[str, Any],
    candidate: Mapping[str, Any],
) -> dict[str, Any]:
    """Delegate structured observation comparison for orchestrator callers."""
    return compare_probe_sets(baseline, candidate)


def _write_output(path: str, text: str) -> None:
    """Write explicit UTF-8 orchestrator output when a CLI caller requests it."""
    output = Path(path).expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(text + ("" if text.endswith("\n") else "\n"), encoding="utf-8", newline="\n")


def main() -> int:
    """CLI entry point for bounded preflight evidence generation."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--target", required=True)
    parser.add_argument("--audit-markdown", required=True)
    parser.add_argument("--output-json", default="")
    args = parser.parse_args()

    root = Path(args.project_root).expanduser().resolve()
    target = (root / args.target).resolve()
    source = target.read_text(encoding="utf-8", errors="strict")
    audit_text = Path(args.audit_markdown).expanduser().resolve().read_text(
        encoding="utf-8",
        errors="strict",
    )
    text = build_preflight_evidence_text(
        root,
        target_relative_path=args.target,
        source_text=source,
        audit_text=audit_text,
    )
    print(text)
    if args.output_json:
        _write_output(args.output_json, text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
