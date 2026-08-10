# project-path: tools/
# validate_complete_json_stale_response_protection_routing_v1.py
"""Validate exact stale-response protection routing for Project Web AI."""

from __future__ import annotations

import argparse
import ast
import json
import sys
from pathlib import Path

FEATURE_ID = "complete-json-stale-response-protection-routing-v1"
QUESTION = (
    "Search the current Project evidence for ProjectWebAIRequestIdentity, "
    "_active_request_identity, project_epoch, context_hash, "
    "evidence_context_hash, and stale Web AI worker behavior. KANDA uses "
    "governed validators under tools/validate_*.py rather than only "
    "conventional test files. List the exact validator files that protect "
    "stale-response behavior and explain the specific condition protected "
    "by each one."
)
EXPECTED_PRODUCTION_RECORDS = {
    "kanda_reasoner_app/reasoner_engine/project_web_ai_change_preparation.py",
    "kanda_reasoner_app/reasoner_engine/project_web_ai_tab.py",
    "kanda_reasoner_app/web_ai_provider_contracts.py",
}
EXPECTED_VALIDATORS = {
    "tools/validate_project_web_ai_tool_project_boundary_v1.py",
    "tools/validate_project_web_ai_project_switch_hygiene_v1.py",
    "tools/validate_project_web_ai_prepare_changes_v1.py",
    "tools/validate_global_project_switch_settlement_safe_eject_v1.py",
    "tools/validate_project_web_ai_smart_complete_json_context_v1.py",
}
EXPECTED_IDENTIFIERS = {
    "projectwebairequestidentity",
    "_active_request_identity",
    "project_epoch",
    "context_hash",
    "evidence_context_hash",
}


def require(condition: bool, message: str) -> None:
    """Raise one deterministic validation failure."""
    if not condition:
        raise AssertionError(message)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def validate_static(root: Path) -> None:
    """Validate the exact source contract without executing Project code."""
    analysis_path = (
        root
        / "kanda_reasoner_app"
        / "reasoner_context_collector"
        / "_complete_json_web_ai_enrichment_analysis.py"
    )
    router_path = (
        root
        / "kanda_reasoner_app"
        / "reasoner_engine"
        / "project_web_ai_complete_json_router.py"
    )
    analysis = _read(analysis_path)
    router = _read(router_path)
    ast.parse(analysis, filename=str(analysis_path))
    ast.parse(router, filename=str(router_path))
    require(
        "if _protection_kind(production_path):" in analysis,
        "validator/test production records are not excluded",
    )
    require(
        '"protected_identifiers": protected_identifiers[:80]' in analysis,
        "protected identifier evidence is missing",
    )
    require(
        'reason.startswith("state_identifier:")' in analysis,
        "state identifier evidence is missing",
    )
    require(
        "def _exact_identifiers(" in router,
        "exact identifier query routing is missing",
    )
    require(
        "def _is_protection_source_record(" in router,
        "protection-source record filter is missing",
    )
    require(
        'section == "web_ai_test_protection_index"' in router,
        "protection section filter is not applied",
    )
    require(
        '"web_ai_test_protection_index": 6' in router,
        "protection routing limit is not the approved value",
    )
    require(
        len(analysis.splitlines()) <= 500 and len(router.splitlines()) <= 500,
        "touched source module exceeds 500 lines",
    )
    print("STALE_PROTECTION_ROUTING_STATIC: PASS")
    print("STALE_PROTECTION_ROUTING_MODULE_SIZE: PASS")


def _is_protection_path(path: str) -> bool:
    normalized = path.replace("\\", "/").casefold()
    return (
        normalized.startswith("tools/validate_")
        or "/tests/" in "/" + normalized
        or "test" in Path(normalized).name
    )


def validate_live(root: Path) -> None:
    """Build current sections and prove the demonstrated query is routed."""
    root_text = str(root)
    if root_text not in sys.path:
        sys.path.insert(0, root_text)
    from kanda_reasoner_app.reasoner_context_collector.complete_json_web_ai_enrichment import (  # noqa: E501
        build_web_ai_sections,
    )
    from kanda_reasoner_app.reasoner_engine.project_web_ai_complete_json_router import (  # noqa: E501
        _exact_identifiers,
        _select_records,
    )

    sections = build_web_ai_sections(root)
    protection = sections.get("web_ai_test_protection_index")
    require(isinstance(protection, list), "protection index is not a list")
    require(protection, "protection index is empty")
    require(
        all(
            isinstance(record, dict)
            and not _is_protection_path(str(record.get("file", "")))
            for record in protection
        ),
        "validator/test file was emitted as a protected production record",
    )
    print("PROTECTION_INDEX_PRODUCTION_RECORDS_ONLY: PASS")

    exact_identifiers = set(_exact_identifiers(QUESTION))
    require(
        EXPECTED_IDENTIFIERS.issubset(exact_identifiers),
        "exact query identifiers were not preserved",
    )
    print("STALE_QUERY_EXACT_IDENTIFIERS: PASS")

    selected = _select_records(sections, QUESTION)
    routed = selected.get("web_ai_test_protection_index")
    require(isinstance(routed, list) and routed, "no protection records routed")
    routed_paths = {
        str(record.get("key", ""))
        for record in routed
        if isinstance(record, dict)
    }
    require(
        EXPECTED_PRODUCTION_RECORDS.issubset(routed_paths),
        "required stale-response production records were not routed",
    )
    require(
        all(not _is_protection_path(path) for path in routed_paths),
        "protection source record survived routed filtering",
    )
    payload = json.dumps(selected, sort_keys=True)
    require(
        "brick_wall_q18_stale_async_result_contract.py" not in payload,
        "generic Brick Wall contract displaced exact Web AI protection",
    )
    print("STALE_RESPONSE_PRODUCTION_RECORDS_ROUTED: PASS")
    print("GENERIC_BRICK_WALL_ROUTE_DISPLACEMENT_ABSENT: PASS")

    validators: set[str] = set()
    protected_identifiers: set[str] = set()
    for record in routed:
        evidence = record.get("evidence", {})
        if not isinstance(evidence, dict):
            continue
        validators.update(
            str(item) for item in evidence.get("related_validators", [])
        )
        protected_identifiers.update(
            str(item) for item in evidence.get("protected_identifiers", [])
        )
    require(
        EXPECTED_VALIDATORS.issubset(validators),
        "exact stale-response validators were not routed",
    )
    require(
        EXPECTED_IDENTIFIERS.issubset(protected_identifiers),
        "exact stale-response identifiers were not routed",
    )
    print("EXACT_STALE_RESPONSE_VALIDATORS_ROUTED: PASS")
    print("EXACT_STALE_RESPONSE_IDENTIFIERS_ROUTED: PASS")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    args = parser.parse_args()
    root = Path(args.root).resolve()
    validate_static(root)
    validate_live(root)
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
