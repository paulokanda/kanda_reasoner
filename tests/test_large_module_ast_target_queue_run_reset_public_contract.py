"""Public contract checks for AST target queue reset behavior."""
from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GUI = ROOT / "kanda_reasoner_app/manage_architecture/manage_architecture_gui.py"


def test_run_mode_resets_ast_queue_before_replacing_audit_results() -> None:
    text = GUI.read_text(encoding="utf-8")
    assert "def _reset_large_module_target_state_for_new_project_audit_run" in text
    assert "self._reset_large_module_target_state_for_new_project_audit_run(mode)" in text
    assert "self._large_module_targets = []" in text
    assert "self._large_module_target_index = -1" in text
    assert "self._last_large_module_split_handoff = ''" in text
    assert "Validate running - AST target queue will refresh from new results" in text
    assert "Run Validate to populate oversized module targets" in text
