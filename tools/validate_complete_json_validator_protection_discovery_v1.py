# project-path: tools/validate_complete_json_validator_protection_discovery_v1.py
"""Validate validator-aware complete-JSON protection discovery."""

from __future__ import annotations

import argparse
import ast
import json
import sys
import tempfile
from pathlib import Path

FEATURE_ID = "complete-json-validator-protection-discovery-v1"


def require(condition: bool, message: str) -> None:
    """Raise one focused validation failure."""
    if not condition:
        raise AssertionError(message)


def _load_helper(root: Path):
    """Import the current helper after explicit Project-root bootstrap."""
    root_text = str(root)
    if root_text not in sys.path:
        sys.path.insert(0, root_text)
    from kanda_reasoner_app.reasoner_context_collector import (
        _complete_json_web_ai_enrichment_analysis as helper,
    )

    return helper


def _record_by_file(records: list[dict[str, object]], relative: str):
    for record in records:
        if record.get("file") == relative:
            return record
    raise AssertionError("PROTECTION_RECORD_MISSING: " + relative)


def validate_static(root: Path) -> None:
    """Validate source syntax and the validator-aware contract."""
    relative = (
        "kanda_reasoner_app/reasoner_context_collector/"
        "_complete_json_web_ai_enrichment_analysis.py"
    )
    path = root / relative
    require(path.is_file(), "ANALYSIS_HELPER_MISSING")
    text = path.read_text(encoding="utf-8")
    require(text.isascii(), "ANALYSIS_HELPER_NON_ASCII")
    ast.parse(text, filename=str(path))
    require(len(text.splitlines()) <= 500, "ANALYSIS_HELPER_OVER_500_LINES")
    for marker in (
        'lowered.startswith("tools/validate_")',
        '"has_related_validator"',
        '"related_validators"',
        '"has_related_protection"',
        '"protection_matches"',
        '"source_path"',
        '"symbol:"',
    ):
        require(marker in text, "VALIDATOR_DISCOVERY_MARKER_MISSING: " + marker)
    print("COMPLETE_JSON_VALIDATOR_DISCOVERY_STATIC: PASS")
    print("COMPLETE_JSON_VALIDATOR_DISCOVERY_MODULE_SIZE: PASS")


def validate_fixture(root: Path) -> None:
    """Prove conventional tests and tools/validate_ files are both indexed."""
    helper = _load_helper(root)
    with tempfile.TemporaryDirectory(
        prefix="kanda_validator_protection_fixture_"
    ) as temporary:
        fixture = Path(temporary)
        source = fixture / "package" / "request_identity.py"
        validator = fixture / "tools" / "validate_request_identity_v1.py"
        test_file = fixture / "tests" / "test_request_identity.py"
        unrelated = fixture / "tools" / "validate_unrelated_v1.py"
        for path in (source, validator, test_file, unrelated):
            path.parent.mkdir(parents=True, exist_ok=True)
        source.write_text(
            "class ProjectWebAIRequestIdentity:\n    pass\n",
            encoding="utf-8",
        )
        validator.write_text(
            "from package.request_identity import "
            "ProjectWebAIRequestIdentity\n"
            "SOURCE = 'package/request_identity.py'\n"
            "ACTIVE = '_active_request_identity'\n",
            encoding="utf-8",
        )
        test_file.write_text(
            "from package.request_identity import "
            "ProjectWebAIRequestIdentity\n",
            encoding="utf-8",
        )
        unrelated.write_text("VALUE = 'unrelated'\n", encoding="utf-8")
        records = helper._test_protection_index(
            fixture,
            [
                {
                    "file": "package/request_identity.py",
                    "public_symbols": ["ProjectWebAIRequestIdentity"],
                }
            ],
        )
    record = _record_by_file(records, "package/request_identity.py")
    require(record["has_related_test"] is True, "FIXTURE_TEST_NOT_FOUND")
    require(
        record["has_related_validator"] is True,
        "FIXTURE_VALIDATOR_NOT_FOUND",
    )
    require(
        record["has_related_protection"] is True,
        "FIXTURE_PROTECTION_FLAG_FALSE",
    )
    require(
        "tests/test_request_identity.py" in record["related_tests"],
        "FIXTURE_TEST_PATH_MISSING",
    )
    require(
        "tools/validate_request_identity_v1.py"
        in record["related_validators"],
        "FIXTURE_VALIDATOR_PATH_MISSING",
    )
    require(
        "tools/validate_unrelated_v1.py"
        not in record["related_validators"],
        "UNRELATED_VALIDATOR_FALSE_POSITIVE",
    )
    print("COMPLETE_JSON_CONVENTIONAL_TEST_DISCOVERY: PASS")
    print("COMPLETE_JSON_TOOLS_VALIDATOR_DISCOVERY: PASS")
    print("COMPLETE_JSON_UNRELATED_VALIDATOR_REJECTED: PASS")


def validate_live_project(root: Path) -> None:
    """Prove the exact Project Web AI protections are discoverable."""
    helper = _load_helper(root)
    production = [
        {
            "file": "kanda_reasoner_app/web_ai_provider_contracts.py",
            "public_symbols": [
                "ProjectWebAIRequestIdentity",
                "ProjectWebAIRequest",
                "ProjectWebAIResponse",
            ],
        },
        {
            "file": (
                "kanda_reasoner_app/reasoner_engine/"
                "project_web_ai_tab.py"
            ),
            "public_symbols": ["ProjectWebAITab"],
        },
    ]
    records = helper._test_protection_index(root, production)
    contracts = _record_by_file(
        records,
        "kanda_reasoner_app/web_ai_provider_contracts.py",
    )
    tab = _record_by_file(
        records,
        "kanda_reasoner_app/reasoner_engine/project_web_ai_tab.py",
    )
    required_contract_validators = {
        "tools/validate_project_web_ai_project_switch_hygiene_v1.py",
        "tools/validate_project_web_ai_tool_project_boundary_v1.py",
        "tools/validate_project_web_ai_prepare_changes_v1.py",
        "tools/validate_project_web_ai_professional_chat_history_v1.py",
        "tools/validate_project_web_ai_agent_empty_response_recovery_v1.py",
        "tools/validate_project_web_ai_smart_complete_json_context_v1.py",
    }
    missing_contracts = required_contract_validators.difference(
        contracts["related_validators"]
    )
    require(
        not missing_contracts,
        "REQUEST_IDENTITY_VALIDATORS_MISSING: "
        + json.dumps(sorted(missing_contracts)),
    )
    required_tab_validators = {
        "tools/validate_project_web_ai_tool_project_boundary_v1.py",
        "tools/validate_project_web_ai_project_switch_hygiene_v1.py",
        "tools/validate_project_web_ai_professional_chat_history_v1.py",
    }
    missing_tab = required_tab_validators.difference(tab["related_validators"])
    require(
        not missing_tab,
        "ACTIVE_REQUEST_VALIDATORS_MISSING: "
        + json.dumps(sorted(missing_tab)),
    )
    from kanda_reasoner_app.reasoner_engine import (
        project_web_ai_complete_json_router as router,
    )

    selected = router._select_records(
        {"web_ai_test_protection_index": records},
        (
            "Find validators protecting ProjectWebAIRequestIdentity, "
            "_active_request_identity, project_epoch, and stale responses."
        ),
    )
    routed_text = json.dumps(selected, sort_keys=True)
    require(
        "validate_project_web_ai_project_switch_hygiene_v1.py"
        in routed_text,
        "SMART_ROUTER_DID_NOT_SURFACE_VALIDATOR_EVIDENCE",
    )
    require(
        "validate_project_web_ai_tool_project_boundary_v1.py"
        in routed_text,
        "SMART_ROUTER_DID_NOT_SURFACE_BOUNDARY_VALIDATOR",
    )
    print("PROJECT_WEB_AI_REQUEST_IDENTITY_VALIDATORS_DISCOVERED: PASS")
    print("PROJECT_WEB_AI_ACTIVE_REQUEST_VALIDATORS_DISCOVERED: PASS")
    print("SMART_CONTEXT_VALIDATOR_EVIDENCE_ROUTED: PASS")


def main() -> int:
    """Run focused validator-aware complete-JSON checks."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    args = parser.parse_args()
    root = Path(args.root).expanduser().resolve()
    validate_static(root)
    validate_fixture(root)
    validate_live_project(root)
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
