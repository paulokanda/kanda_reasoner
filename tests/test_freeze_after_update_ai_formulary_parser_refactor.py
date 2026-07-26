"""Characterization tests for tolerant AI formulary response parsing."""
from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.freeze_after_update_gui._ai_formulary_response_parser import (
    parse_ai_formulary_response,
)


BASE_INPUTS = {
    "feature_title": "Old Feature",
    "primary_box": "old_box",
    "box_type": "Module Box",
    "validated_files": "old.py",
    "generated_files": "",
    "protected_paths": "project_freeze_after_update/frozen_features_memory/",
    "do_not_regress_rules": "Keep old behavior stable.",
    "validation_evidence_summary": "VALIDATION OK: old",
    "known_warnings": "",
    "planned_next_step": "",
    "notes": "",
}


def test_parser_accepts_marker_payload_and_reports_unknown_fields() -> None:
    text = """prose before
KANDA_FREEZE_FORM_JSON_BEGIN
{
  "feature_title": "Demo Feature",
  "validated_files": ["src/demo.py", "tests/test_demo.py"],
  "unknown_extra": "ignored"
}
KANDA_FREEZE_FORM_JSON_END
prose after
"""

    parsed = parse_ai_formulary_response(text, BASE_INPUTS)

    assert parsed.inputs["feature_title"] == "Demo Feature"
    assert parsed.inputs["validated_files"] == "src/demo.py\ntests/test_demo.py"
    assert parsed.ignored_fields == ["unknown_extra"]


def test_parser_repairs_trailing_commas_and_markdown_damage() -> None:
    text = """```json
{
  "feature_title": "Fixed Feature",
  "generated_files": ["kanda_reasoner_app/**init**.py",],
}
```"""

    parsed = parse_ai_formulary_response(text, BASE_INPUTS)

    assert parsed.inputs["feature_title"] == "Fixed Feature"
    assert parsed.inputs["generated_files"] == "kanda_reasoner_app/__init__.py"


def test_parser_raises_when_no_payload_exists() -> None:
    try:
        parse_ai_formulary_response("no json here", BASE_INPUTS)
    except ValueError as exc:
        assert "Could not find a usable freeze-form JSON object" in str(exc)
    else:
        raise AssertionError("parser accepted text without JSON")


def main() -> int:
    test_parser_accepts_marker_payload_and_reports_unknown_fields()
    test_parser_repairs_trailing_commas_and_markdown_damage()
    test_parser_raises_when_no_payload_exists()
    print("VALIDATION OK: freeze-after-update-ai-formulary-parser-refactor")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
