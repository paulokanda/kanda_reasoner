"""Validate Wave 9A Python specialist-stack reconciliation."""

from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path
from typing import Any

__all__ = ["main"]


FEATURE_ID = "prompt-audit-wave9a-python-specialist-stack-reconciliation-v1"
STAGE = FEATURE_ID
LIB = Path("kanda_prompt_workspace/prompt_library")

CODES = {
    "python_pragmatic_programmer": "KPR-08-008",
    "python_refactoring": "KPR-08-009",
    "software_engineering_books_master": "KPR-08-010",
    "anti_hallucination_full_group": "KPR-09-001",
    "anti_hallucination_short_group": "KPR-09-002",
    "anti_hallucination_independent_ai_audit_full": "KPR-09-003",
    "anti_hallucination_web_evidence_audit_full": "KPR-09-004",
    "anti_hallucination_book_literature_audit_full": "KPR-09-005",
    "anti_hallucination_master_protocol_full": "KPR-09-006",
    "anti_hallucination_independent_ai_audit_short": "KPR-09-007",
    "anti_hallucination_web_evidence_audit_short": "KPR-09-008",
    "anti_hallucination_book_literature_audit_short": "KPR-09-009",
    "anti_hallucination_protocol_short": "KPR-09-010",
    "python_documentation_developer_experience": "KPR-09-011",
    "python_observability_logging_metrics_tracing": "KPR-09-012",
    "python_resilience_error_handling": "KPR-09-013",
    "python_security_threat_prevention": "KPR-09-014",
    "python_testing_pytest": "KPR-09-015",
    "python_validation_serialisation_type_safety": "KPR-09-016",
    "tab4_docstring_quality_roadmap": "KPR-09-017",
    "python_api_design": "KPR-10-001",
    "python_async_parallel_distributed": "KPR-10-002",
    "python_configuration_feature_flags": "KPR-10-003",
    "python_database_design_optimisation": "KPR-10-004",
}

CATEGORIES = {
    **{key: "08_python_engineering_core" for key in (
        "python_pragmatic_programmer", "python_refactoring", "software_engineering_books_master")},
    **{key: "10_python_api_data_async_config" for key in (
        "python_api_design", "python_async_parallel_distributed",
        "python_configuration_feature_flags", "python_database_design_optimisation")},
}
for key in CODES:
    CATEGORIES.setdefault(key, "09_python_quality_security_observability")

DERIVED = {
    "anti_hallucination_independent_ai_audit_short": "KPR-09-003",
    "anti_hallucination_web_evidence_audit_short": "KPR-09-004",
    "anti_hallucination_book_literature_audit_short": "KPR-09-005",
    "anti_hallucination_protocol_short": "KPR-09-006",
}

REQUIRED_MARKERS = {
    "python_pragmatic_programmer": ("reversible", "prototype", "tracer-bullet", "source-write authorization"),
    "python_refactoring": ("public-contract preservation", "KPR-08-007", "stopping criteria", "source-write authorization"),
    "software_engineering_books_master": ("non-authoritative", "Book-to-specialist map", "KPR-08-009", "current Prompt Navigation Index"),
    "anti_hallucination_full_group": ("operation ID", "stage", "Agreement between AIs is not proof", "Search for disconfirming evidence"),
    "anti_hallucination_short_group": ("operation ID", "Escalate", "Agreement between AIs is not proof", "Search for disconfirming evidence"),
    "anti_hallucination_independent_ai_audit_full": ("claim and assumption ledger", "Do not require an arbitrary number", "self-review"),
    "anti_hallucination_web_evidence_audit_full": ("privacy-safe", "disconfirming evidence", "WEB_UNAVAILABLE"),
    "anti_hallucination_book_literature_audit_full": ("Never attribute a claim to an uninspected book", "bibliographic provenance", "ADOPT/ADAPT/REJECT"),
    "anti_hallucination_master_protocol_full": ("VERIFIED", "PARTIALLY_VERIFIED", "INCONCLUSIVE", "BLOCKED", "REJECTED"),
    "python_documentation_developer_experience": ("audience", "freshness", "Unix"),
    "python_observability_logging_metrics_tracing": ("cardinality", "secrets", "smallest telemetry stack"),
    "python_resilience_error_handling": ("Never retry every exception", "deadline", "partial-completion"),
    "python_security_threat_prevention": ("Do not invent standard-library APIs", "Archive extraction", "argument arrays"),
    "python_testing_pytest": ("Do not impose fixed coverage", "NOT_RUN", "FLAKY"),
    "python_validation_serialisation_type_safety": ("resource limits", "Do not conflate type hints", "coercion"),
    "tab4_docstring_quality_roadmap": ("status: deprecated", "load_type: never", "Global active route: `NO`"),
    "python_api_design": ("Do not equate HTTP method with idempotent implementation", "compatibility", "conditional requests"),
    "python_async_parallel_distributed": ("structured concurrency", "Windows spawn", "Bound concurrency"),
    "python_configuration_feature_flags": ("Do not construct effectful settings at import time", "SIGHUP", "effective provenance"),
    "python_database_design_optimisation": ("Bind advice to the real database engine", "SQLAlchemy", "query-plan evidence"),
}

BROAD_ALIASES = {"code", "quality", "security", "api", "data", "books", "engineering", "software design", "python engineering"}


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict):
        raise AssertionError("JSON root must be object: " + str(path))
    return data


def parse_frontmatter(text: str) -> dict[str, str]:
    match = re.match(r"\A---\n(.*?)\n---\n", text, flags=re.S)
    if not match:
        raise AssertionError("Missing frontmatter")
    result: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        result[key.strip()] = value.strip()
    return result


def validate_prompts(root: Path) -> None:
    for prompt_id, code in CODES.items():
        category = CATEGORIES[prompt_id]
        prompt = root / LIB / "ACTIVE_PROMPTS" / category / (prompt_id + ".md")
        meta_path = root / LIB / "METADATA" / (prompt_id + ".meta.json")
        text = prompt.read_text(encoding="utf-8-sig")
        meta = load_json(meta_path)
        front = parse_frontmatter(text)
        if front.get("prompt_id") != prompt_id or front.get("prompt_code") != code:
            raise AssertionError("Prompt identity mismatch: " + prompt_id)
        for key, expected in (("prompt_code", code), ("prompt_id", prompt_id), ("category", category), ("version", "2.0.0"), ("source_stage", STAGE), ("updated_for", STAGE)):
            if str(meta.get(key) or "") != expected:
                raise AssertionError("Metadata mismatch " + key + ": " + prompt_id)
        if meta.get("required_companion_prompts") != []:
            raise AssertionError("Forced companions remain: " + prompt_id)
        aliases = {str(value).lower() for value in meta.get("aliases") or []}
        if aliases & BROAD_ALIASES:
            raise AssertionError("Broad alias remains: " + prompt_id)
        for marker in REQUIRED_MARKERS.get(prompt_id, ("source mutation",)):
            if marker not in text:
                raise AssertionError("Missing marker for " + prompt_id + ": " + marker)
        if prompt_id in DERIVED:
            if front.get("derived_from") != DERIVED[prompt_id]:
                raise AssertionError("Derived binding mismatch: " + prompt_id)
            if "does not own an independent canon" not in text:
                raise AssertionError("Derived ownership marker missing: " + prompt_id)
    print("WAVE9A_PROMPT_METADATA_ALIGNMENT: PASS")


def validate_deprecation(root: Path) -> None:
    pid = "tab4_docstring_quality_roadmap"
    meta = load_json(root / LIB / "METADATA" / (pid + ".meta.json"))
    if meta.get("status") != "deprecated" or meta.get("load_type") != "never":
        raise AssertionError("Prompt 098 deprecation metadata mismatch")
    if meta.get("trigger_phrases") != []:
        raise AssertionError("Deprecated Prompt 098 still has triggers")
    print("WAVE9A_PROMPT098_GLOBAL_DEPRECATION: PASS")


def validate_routing(root: Path) -> None:
    nav = load_json(root / LIB / "ROUTING/prompt_navigation_index.json")
    entries = {entry["prompt_id"]: entry for entry in nav.get("entries") or []}
    for pid, code in CODES.items():
        entry = entries.get(pid)
        if not isinstance(entry, dict) or entry.get("prompt_code") != code:
            raise AssertionError("Navigation entry mismatch: " + pid)
        if entry.get("required_companion_prompts") != []:
            raise AssertionError("Navigation forced companions: " + pid)
        aliases = {str(value).lower() for value in entry.get("aliases") or []}
        if aliases & BROAD_ALIASES:
            raise AssertionError("Navigation broad alias: " + pid)
        if pid == "tab4_docstring_quality_roadmap" and entry.get("status") != "deprecated":
            raise AssertionError("Deprecated navigation status missing")
    active_nav = (root / LIB / "ACTIVE_PROMPTS/02_prompt_routing_and_indexing/prompt_navigation_index.md").read_text(encoding="utf-8-sig")
    for marker in ("Wave 9A Python specialist stack routes", "KPR-08-010", "KPR-09-016", "KPR-10-004", "Search for disconfirming evidence"):
        if marker not in active_nav:
            raise AssertionError("Active navigation marker missing: " + marker)
    print("WAVE9A_ROUTING_COMPLETENESS: PASS")


def validate_coverage(root: Path) -> None:
    path = root / LIB / "ROUTING/prompt_route_coverage_table.csv"
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = {row["prompt_id"]: row for row in csv.DictReader(handle)}
    for pid in CODES:
        row = rows.get(pid)
        if not row or row.get("companions"):
            raise AssertionError("Coverage row or companion mismatch: " + pid)
        if pid == "tab4_docstring_quality_roadmap" and row.get("trigger_phrases"):
            raise AssertionError("Deprecated Prompt 098 coverage triggers remain")
    print("WAVE9A_NO_FORCED_COMPANIONS: PASS")


def validate_folder_cards(root: Path) -> None:
    for category in set(CATEGORIES.values()):
        card = (root / LIB / "ACTIVE_PROMPTS" / category / "_FOLDER_ASSIMILATION.md").read_text(encoding="utf-8-sig")
        if "Do not load all specialists as a bundle" not in card:
            raise AssertionError("Folder smallest-owner rule missing: " + category)
        meta = load_json(root / LIB / "METADATA" / ("folder_assimilation_" + category + ".meta.json"))
        if meta.get("version") != "3.0" or meta.get("status") != "active":
            raise AssertionError("Folder metadata mismatch: " + category)
    print("WAVE9A_FOLDER_OWNER_BOUNDARIES: PASS")


def validate_no_startup_promotion(root: Path) -> None:
    startup = root / "kanda_prompt_workspace/prompt_tools/sync_startup_routing_kernel_pack.py"
    text = startup.read_text(encoding="utf-8-sig")
    for pid in CODES:
        if (pid + ".md") in text:
            raise AssertionError("Direct startup promotion: " + pid)
    print("WAVE9A_NO_STARTUP_PROMOTION: PASS")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True)
    args = parser.parse_args()
    root = Path(args.project_root).expanduser().resolve()
    validate_prompts(root)
    validate_deprecation(root)
    validate_folder_cards(root)
    validate_routing(root)
    validate_coverage(root)
    validate_no_startup_promotion(root)
    print("WAVE9A_PYTHON_SPECIALIST_STACK_RECONCILIATION_REGRESSION_SET: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
