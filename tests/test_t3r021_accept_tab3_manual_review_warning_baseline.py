"""Regression tests for T3R021 accepted warning baseline append."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASELINE = ROOT / "_project_reference" / "ACTIVE_PROJECT_ GOVERNANCE" / "accepted_warning_baseline.json"

PATHS = {
    'ask_' 'ai_project_reasoner' '/insert_missing_docstrings_gui/insert_missing_docstrings_gui_help/layout_builder.py',
    'ask_' 'ai_project_reasoner' '/insert_missing_docstrings_gui/insert_missing_docstrings_gui_help/manual_docstring_review_batch.py',
    'ask_' 'ai_project_reasoner' '/insert_missing_docstrings_gui/insert_missing_docstrings_gui_help/manual_docstring_review_editor.py',
    'ask_' 'ai_project_reasoner' '/insert_missing_docstrings_gui/insert_missing_docstrings_gui_help/manual_docstring_review_export.py',
    'ask_' 'ai_project_reasoner' '/insert_missing_docstrings_gui/insert_missing_docstrings_gui_help/manual_docstring_review_support.py',
    'ask_' 'ai_project_reasoner' '/insert_missing_docstrings_gui/insert_missing_docstrings_gui_help/report_review_panel.py',
}


def _data() -> dict:
    return json.loads(BASELINE.read_text(encoding="utf-8"))


def test_t3r021_appends_all_current_tab3_manual_review_warnings() -> None:
    warnings = _data()["accepted_warnings"]
    accepted = {
        item["path"]
        for item in warnings
        if item.get("classification") == "accepted_intentional_tab3_manual_review_gui_boundary"
        and item.get("code") == "MIXED_RESPONSIBILITY_FILE"
        and item.get("decision") == "suppressed"
    }

    assert PATHS.issubset(accepted)


def test_t3r021_entries_have_required_stable_matchers_and_rationale() -> None:
    for item in _data()["accepted_warnings"]:
        if item.get("path") not in PATHS:
            continue
        assert item.get("classification") == "accepted_intentional_tab3_manual_review_gui_boundary"
        assert item.get("message_prefix")
        assert item.get("message_sha256")
        assert item.get("rationale")
        assert "later design refactor" in item["rationale"]


def test_known_message_hashes_are_stable() -> None:
    message = (
        "Module appears to mix multiple responsibility domains: docstring tooling "
        "[insert_missing_docstrings, missing_docstrings]; GUI/UI behavior [gui]. "
        "Detected architecture box: docstring_tool. Risk: this file may be harder "
        "to test, refactor, and assign to a single owner. Move unrelated behavior "
        "behind a helper, adapter, or explicit handoff contract before adding correction logic."
    )

    assert hashlib.sha256(message.encode("utf-8")).hexdigest() == (
        "406804da0cf1dc29b0466dc758cb3af9636b90dc567268770fa33e7315d1bd7d"
    )


if __name__ == "__main__":
    test_t3r021_appends_all_current_tab3_manual_review_warnings()
    test_t3r021_entries_have_required_stable_matchers_and_rationale()
    test_known_message_hashes_are_stable()
    print("T3R021 accepted warning baseline tests passed.")
