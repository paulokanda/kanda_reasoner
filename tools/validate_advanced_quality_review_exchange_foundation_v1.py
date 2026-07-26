# project-path: tools/validate_advanced_quality_review_exchange_foundation_v1.py
"""Validate Advanced Quality Review and external AI exchange foundation contracts."""

from __future__ import annotations

from pathlib import Path
import sys
from tempfile import TemporaryDirectory

FEATURE_ID = "advanced-quality-review-exchange-foundation-v1"
PROJECT_ROOT = Path(__file__).resolve().parents[1]
SOURCE_FILES = (
    PROJECT_ROOT
    / "kanda_reasoner_app"
    / "manage_architecture"
    / "large_file_refactor_planner"
    / "advanced_quality_review_contract.py",
    PROJECT_ROOT
    / "kanda_reasoner_app"
    / "manage_architecture"
    / "large_file_refactor_planner"
    / "external_ai_candidate_exchange_contract.py",
    PROJECT_ROOT
    / "kanda_reasoner_app"
    / "manage_architecture"
    / "large_file_refactor_planner"
    / "workbench_review_stage_contract.py",
    PROJECT_ROOT
    / "kanda_reasoner_app"
    / "manage_architecture"
    / "large_file_refactor_planner"
    / "workbench_project_support_paths.py",
)


def _bootstrap_imports() -> None:
    """Make the exact project root importable for standalone validation."""
    root_text = str(PROJECT_ROOT)
    if root_text not in sys.path:
        sys.path.insert(0, root_text)


def _assert_ascii_utf8_no_bom(path: Path) -> None:
    """Require plain UTF-8 source with ASCII-only content and no BOM."""
    raw = path.read_bytes()
    assert not raw.startswith(b"\xef\xbb\xbf"), "BOM_PRESENT:" + str(path)
    text = raw.decode("utf-8")
    assert all(ord(character) < 128 for character in text), "NON_ASCII_SOURCE:" + str(path)


def _validate_analysis_identity() -> None:
    """Prove immutable analysis identity and scenario completeness behavior."""
    from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.advanced_quality_review_contract import (
        REQUIRED_ARCHITECTURE_QUALITY_SCENARIOS,
        analysis_identity_matches,
        build_analysis_identity,
        validate_architecture_quality_scenarios,
    )

    first = build_analysis_identity(
        project_card_identity="card-001",
        target_relative_path="pkg/large_module.py",
        baseline_hash="b" * 64,
        preview_hash="p" * 64,
        refactor_plan_hash="r" * 64,
        analyzer_lock_hash="l" * 64,
        analyzer_config_hash="c" * 64,
    )
    same = build_analysis_identity(
        project_card_identity="card-001",
        target_relative_path="pkg\\large_module.py",
        baseline_hash="b" * 64,
        preview_hash="p" * 64,
        refactor_plan_hash="r" * 64,
        analyzer_lock_hash="l" * 64,
        analyzer_config_hash="c" * 64,
    )
    changed = build_analysis_identity(
        project_card_identity="card-001",
        target_relative_path="pkg/large_module.py",
        baseline_hash="b" * 64,
        preview_hash="q" * 64,
        refactor_plan_hash="r" * 64,
        analyzer_lock_hash="l" * 64,
        analyzer_config_hash="c" * 64,
    )
    assert analysis_identity_matches(first, same)
    assert not analysis_identity_matches(first, changed)
    assert not validate_architecture_quality_scenarios()
    assert len(REQUIRED_ARCHITECTURE_QUALITY_SCENARIOS) >= 10
    print("ANALYSIS_IDENTITY_IMMUTABLE: PASS")
    print("ARCHITECTURE_QUALITY_SCENARIOS_COMPLETE: PASS")


def _validate_exchange_lineage() -> None:
    """Prove cumulative candidate identity and cross-card mismatch blocking."""
    from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.external_ai_candidate_exchange_contract import (
        ai_response_identity_blockers,
        build_ai_response_identity,
        build_candidate_set_identity,
        build_exchange_identity,
    )

    candidate = build_candidate_set_identity(
        project_card_identity="card-001",
        target_relative_path="pkg/large_module.py",
        baseline_hash="b" * 64,
        preview_hash="p" * 64,
        plan_hash="r" * 64,
        candidate_file_hashes={
            "pkg/large_module.py": "1" * 64,
            "pkg/helper_module.py": "2" * 64,
        },
    )
    exchange = build_exchange_identity(
        exchange_id="EXCH-0001",
        candidate_identity=candidate,
        exchange_generation=1,
    )
    response = build_ai_response_identity(
        exchange_identity=exchange,
        return_candidate_set_hash="3" * 64,
        return_schema_version="1.0",
    )
    assert not ai_response_identity_blockers(
        exchange,
        response,
        active_project_card_identity="card-001",
        active_target_relative_path="pkg/large_module.py",
        active_preview_hash="p" * 64,
    )
    blockers = ai_response_identity_blockers(
        exchange,
        response,
        active_project_card_identity="card-002",
        active_target_relative_path="pkg/other_module.py",
        active_preview_hash="z" * 64,
    )
    assert "AI_RESPONSE_NOT_FOR_ACTIVE_CARD" in blockers
    assert "AI_RESPONSE_NOT_FOR_ACTIVE_TARGET" in blockers
    assert "AI_RESPONSE_SOURCE_PREVIEW_STALE" in blockers
    print("CANDIDATE_SET_CUMULATIVE_IDENTITY: PASS")
    print("EXCHANGE_LINEAGE_MISMATCH_BLOCKS: PASS")


def _validate_project_support_ownership() -> None:
    """Prove Tool mechanisms resolve durable state under the selected Project."""
    from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_project_support_paths import (
        ai_refactoring_card_exchange_root,
        ai_refactoring_exchange_root,
        exchange_root_blockers,
        quality_evidence_root,
        workbench_path_class,
    )

    with TemporaryDirectory() as temp_dir:
        root = Path(temp_dir).resolve()
        tool_root = root / "kanda_reasoner_tool"
        project_root = root / "patient_project"
        tool_root.mkdir()
        project_root.mkdir()
        quality_root = quality_evidence_root(project_root)
        exchange_root = ai_refactoring_exchange_root(project_root)
        card_root = ai_refactoring_card_exchange_root(project_root, "card:001")
        expected_support = root / "patient_project_show_project_to_AI"
        assert quality_root == (
            expected_support / "large_file_refactor_workbench" / "quality_evidence"
        )
        assert exchange_root == (
            expected_support / "large_file_refactor_workbench" / "ai_refactoring_exchange"
        )
        assert card_root.parent == exchange_root
        assert not exchange_root_blockers(project_root, card_root)
        assert workbench_path_class(project_root, card_root) == "active_project_workbench_support"
        assert tool_root not in card_root.parents
    print("DYNAMIC_PROJECT_SUPPORT_OWNERSHIP: PASS")
    print("TOOL_PROJECT_CONTAINER_SEPARATION: PASS")


def _validate_stage_contract() -> None:
    """Prove stage placement and human authorization protections."""
    from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_review_stage_contract import (
        build_workbench_review_stage_contract,
        validate_workbench_review_stage_contract,
    )

    contract = build_workbench_review_stage_contract()
    assert not validate_workbench_review_stage_contract(contract)
    stages = contract.ordered_stages
    assert stages.index("STRUCTURAL_VALIDATION") < stages.index("ADVANCED_QUALITY_REVIEW")
    assert stages.index("ADVANCED_QUALITY_REVIEW") < stages.index("PREFLIGHT_BACKUP")
    assert stages.index("ASSISTED_REVIEW") < stages.index("EXTERNAL_AI_CANDIDATE_REVIEW")
    assert stages.index("EXTERNAL_AI_CANDIDATE_REVIEW") < stages.index("HUMAN_AUTHORIZATION")
    assert contract.external_ai_stage_optional
    assert not contract.analyzer_source_mutation_allowed
    assert not contract.external_ai_direct_apply_allowed
    assert contract.human_authorization_required
    print("CANONICAL_REVIEW_STAGE_ORDER: PASS")
    print("HUMAN_AUTHORIZATION_PRESERVED: PASS")


def _validate_source_hygiene_and_size() -> None:
    """Enforce the active source hygiene and module-size gates."""
    for path in SOURCE_FILES:
        assert path.is_file(), "MISSING_SOURCE:" + str(path)
        _assert_ascii_utf8_no_bom(path)
        line_count = len(path.read_text(encoding="utf-8").splitlines())
        assert line_count <= 500, "MODULE_TOO_LARGE:" + str(path) + ":" + str(line_count)
    print("SOURCE_ASCII_UTF8_NO_BOM: PASS")
    print("MODULE_SIZE_MAX_500: PASS")


def main() -> int:
    """Run all foundation validations and emit freeze-recognizable markers."""
    _bootstrap_imports()
    _validate_analysis_identity()
    _validate_exchange_lineage()
    _validate_project_support_ownership()
    _validate_stage_contract()
    _validate_source_hygiene_and_size()
    print("ADVANCED_QUALITY_REVIEW_EXCHANGE_FOUNDATION: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
