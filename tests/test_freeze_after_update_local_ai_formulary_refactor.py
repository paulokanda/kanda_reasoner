"""Characterization tests for the Freeze tab local-AI formulary helper."""
from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.freeze_after_update_gui import _local_ai_formulary as helper
from kanda_reasoner_app.freeze_after_update_gui.freeze_after_update_tab import (
    LocalFreezeAIFormularyRunner,
)


def test_local_ai_formulary_helper_stays_qt_free() -> None:
    source = Path(helper.__file__).read_text(encoding="utf-8")

    assert "PySide6" not in source
    assert "freeze_after_update_tab" not in source
    assert "QDialog" not in source
    assert "QTimer" not in source


def test_public_facade_reexports_local_ai_runner() -> None:
    assert LocalFreezeAIFormularyRunner is helper.LocalFreezeAIFormularyRunner


def test_combo_model_name_normalization_keeps_auto_as_empty() -> None:
    assert helper.model_name_from_local_ai_combo_text("") == ""
    assert helper.model_name_from_local_ai_combo_text(helper.AUTO_LOCAL_AI_MODEL_LABEL) == ""
    assert helper.model_name_from_local_ai_combo_text("  qwen2.5-coder  ") == "qwen2.5-coder"


def test_quality_gate_rejects_lost_baseline_lines() -> None:
    heuristic = {
        "feature_title": "Demo Feature",
        "primary_box": "demo_box",
        "validated_files": "src/demo.py\ntests/test_demo.py",
        "generated_files": "workbench/demo.txt",
        "protected_paths": "src/demo.py",
        "do_not_regress_rules": "Keep demo behavior stable.\nDo not write outside project memory.",
        "validation_evidence_summary": "VALIDATION OK: demo",
    }
    candidate = dict(heuristic)
    candidate["validated_files"] = "src/demo.py"

    ok, reasons = helper.validate_local_ai_form_against_heuristic(candidate, heuristic)

    assert not ok
    assert any("validated_files lost baseline line" in reason for reason in reasons)


def test_prompt_echo_detection_requires_multiple_markers() -> None:
    assert not helper.local_ai_response_looks_like_prompt_echo("Critical rules:")
    assert helper.local_ai_response_looks_like_prompt_echo(
        "Critical rules:\nReturn format - strict copy/paste contract\n"
    )


def main() -> int:
    test_local_ai_formulary_helper_stays_qt_free()
    test_public_facade_reexports_local_ai_runner()
    test_combo_model_name_normalization_keeps_auto_as_empty()
    test_quality_gate_rejects_lost_baseline_lines()
    test_prompt_echo_detection_requires_multiple_markers()
    print("VALIDATION OK: freeze-after-update-local-ai-formulary-refactor")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
