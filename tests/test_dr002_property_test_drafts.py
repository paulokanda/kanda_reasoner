"""Tests for the property-test guidance module."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.reliability_guidance import (  # noqa: E402
    PropertyTestDraft,
    default_property_test_output_dir,
    render_property_test_draft_markdown,
)
from kanda_reasoner_app.reliability_guidance.property_test_guidance import (  # noqa: E402
    __all__ as guidance_all,
)


def test_property_test_draft_renders_markdown() -> None:
    draft = PropertyTestDraft(
        module_path="kanda_reasoner_app.example",
        function_name="normalize_items",
        properties=("Output is stable for repeated equal inputs.",),
        input_strategies=("small lists of strings",),
        invariants=("Does not mutate input collection.",),
        edge_cases=("empty input",),
        tests_to_add=("test repeated equal inputs",),
    )

    markdown = render_property_test_draft_markdown(draft)

    assert "# Property Test Draft" in markdown
    assert "Function: normalize_items" in markdown
    assert "Output is stable for repeated equal inputs." in markdown
    assert "small lists of strings" in markdown
    assert "test repeated equal inputs" in markdown


def test_default_output_dir_uses_workbench_drafts() -> None:
    output_dir = default_property_test_output_dir(Path("E:/developer_tools"))

    assert output_dir.as_posix().endswith("workbench/drafts/property_tests")


def test_public_contract_is_explicit() -> None:
    assert "PropertyTestDraft" in guidance_all
    assert "render_property_test_draft_markdown" in guidance_all
    assert "default_property_test_output_dir" in guidance_all


if __name__ == "__main__":
    test_property_test_draft_renders_markdown()
    test_default_output_dir_uses_workbench_drafts()
    test_public_contract_is_explicit()
    print("DR002 Property Test Drafts tests passed.")
