"""Tests for the API contract guard guidance module."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.reliability_guidance import (  # noqa: E402
    ApiContractGuardDraft,
    default_api_contract_output_dir,
    render_api_contract_guard_draft_markdown,
)
from kanda_reasoner_app.reliability_guidance.api_contract_guidance import (  # noqa: E402
    __all__ as guidance_all,
)


def test_api_contract_guard_draft_renders_markdown() -> None:
    draft = ApiContractGuardDraft(
        module_path="kanda_reasoner_app.example",
        function_name="build_report",
        parameters=("project_root", "items"),
        return_hint="dict[str, object]",
        known_failure_modes=("missing project root",),
        tests_to_add=("test missing project root",),
    )

    markdown = render_api_contract_guard_draft_markdown(draft)

    assert "# API Contract Guard Draft" in markdown
    assert "Function: build_report" in markdown
    assert "Validate parameter 'project_root' before use." in markdown
    assert "test missing project root" in markdown


def test_default_output_dir_uses_workbench_drafts() -> None:
    output_dir = default_api_contract_output_dir(Path("<PROJECT_ROOT>"))

    assert output_dir.as_posix().endswith("workbench/drafts/api_contracts")


def test_public_contract_is_explicit() -> None:
    assert "ApiContractGuardDraft" in guidance_all
    assert "render_api_contract_guard_draft_markdown" in guidance_all
    assert "default_api_contract_output_dir" in guidance_all


if __name__ == "__main__":
    test_api_contract_guard_draft_renders_markdown()
    test_default_output_dir_uses_workbench_drafts()
    test_public_contract_is_explicit()
    print("DR001B API Contract Guard Drafts owner-path repair tests passed.")
