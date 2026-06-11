"""PA023 JSON-canonical Atlas output quality public contract tests."""

from __future__ import annotations

from kanda_reasoner_app.reasoner_symbol_atlas.evidence_freshness import (
    check_reasoner_symbol_atlas_evidence_freshness,
)
from kanda_reasoner_app.reasoner_symbol_atlas.evidence_merger import (
    build_reasoner_symbol_atlas_live_json_merge_report,
)
from kanda_reasoner_app.reasoner_symbol_atlas.output_policy import (
    sanitize_atlas_markdown_text,
)
from kanda_reasoner_app.safety_suite_cli.reasoner_symbol_atlas_commands import (
    add_reasoner_symbol_atlas_parsers,
    reasoner_symbol_atlas_cli_commands,
)


def test_pa023_uses_public_cli_contract_only() -> None:
    assert callable(add_reasoner_symbol_atlas_parsers)
    assert callable(reasoner_symbol_atlas_cli_commands)


def test_pa023_canonical_support_public_imports() -> None:
    assert callable(check_reasoner_symbol_atlas_evidence_freshness)
    assert callable(build_reasoner_symbol_atlas_live_json_merge_report)


def test_pa023_output_policy_filters_archived_paths() -> None:
    text = "\n".join(
        [
            "## Decision Details",
            "- primary_edit_target=_project_reference/ACTIVE_PROJECT_ GOVERNANCE/check_reasoner_project_canon.py",
            "- related_file=reasoner_tools_gui_engineering_safety_panel.py",
            "- related_file=_project_reference/tests_archive/old/test_x.py",
            "- test_to_run=python tests/test_pa021_reasoner_symbol_atlas_gui_integration.py",
            "- test_to_run=python _project_reference/tests_archive/old/test_y.py",
            "## Symbols",
            "- existing_code_finder_decision (unknown) in  -> reasoner_tools_gui_engineering_safety_panel.py",
        ]
    )
    cleaned = sanitize_atlas_markdown_text(text)
    assert "_project_reference" not in cleaned
    assert "reasoner_tools_gui_engineering_safety_panel.py" in cleaned
    assert "existing_code_finder_decision (decision)" in cleaned
    assert "output_policy=json_canonical_active_scope" in cleaned


def main() -> int:
    test_pa023_uses_public_cli_contract_only()
    test_pa023_canonical_support_public_imports()
    test_pa023_output_policy_filters_archived_paths()
    print("PA023 JSON-canonical Atlas output quality tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
