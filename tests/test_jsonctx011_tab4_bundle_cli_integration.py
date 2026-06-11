"""Focused tests for Tab 4 companion bundle process integration.

Updated by JSONCTX011D: complete JSON deterministic evidence enrichment must
run after the legacy collector and before companion bundle generation.
"""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

PROCESS_HELPER = (
    PROJECT_ROOT
    / 'ask_' 'ai_project_reasoner'
    / "reasoner_tools_shell"
    / "runner_help"
    / "window_process_private_impl.py"
)


def _source() -> str:
    return PROCESS_HELPER.read_text(encoding="utf-8")


def test_tab4_runs_enrichment_then_ai_context_bundle_after_collector_success() -> None:
    source = _source()
    collector_marker = "event_type=\"collector_run_finished\""
    enrichment_start_marker = "_start_complete_json_enrichment_process(self)"
    bundle_start_marker = "_start_ai_context_bundle_process(self)"
    old_instance_call = "self._start_ai_context_bundle_process()"

    assert collector_marker in source
    assert enrichment_start_marker in source
    assert bundle_start_marker in source
    assert old_instance_call not in source

    collector_index = source.index(collector_marker)
    enrichment_start_index = source.index(enrichment_start_marker, collector_index)
    enrichment_handler_index = source.index('self._active_stage == "Enriching complete JSON"')
    bundle_start_index = source.index(bundle_start_marker, enrichment_handler_index)

    assert collector_index < enrichment_start_index
    assert enrichment_handler_index < bundle_start_index


def test_tab4_enrichment_process_uses_deterministic_complete_json_cli() -> None:
    source = _source()

    assert "def _start_complete_json_enrichment_process(self) -> None:" in source
    assert '"-m"' in source
    assert '"kanda_reasoner_app.reasoner_context_collector.complete_json_web_ai_enrichment"' in source
    assert '"--root"' in source
    assert '"--complete-json"' in source
    assert "self._pending_output_json" in source
    assert '"--compact"' in source
    assert 'self._active_stage == "Enriching complete JSON"' in source
    assert "Complete JSON deterministic evidence sections verified" in source


def test_tab4_bundle_process_uses_project_context_bundle_cli() -> None:
    source = _source()

    assert "def _start_ai_context_bundle_process(self) -> None:" in source
    assert '"-m"' in source
    assert '"kanda_reasoner_app.reasoner_context_bundle"' in source
    assert '"--root"' in source
    assert "self._pending_project_root" in source
    assert '"--write"' in source
    assert '"--compact"' in source
    assert "_tab4_build_child_env(project_root)" in source
    assert "_tab4_apply_qprocess_env" in source


def test_tab4_bundle_process_has_finish_branch_and_status_log() -> None:
    source = _source()

    assert 'self._active_stage == "Generating AI context bundle"' in source
    assert '"[OK] AI context bundle generated."' in source
    assert 'event_type="ai_context_bundle_generated"' in source
    assert 'tags=["collector", "ai_context_bundle", "finish"]' in source


def test_tab4_integration_preserves_dynamic_paths_and_no_inline_bundle_write() -> None:
    source = _source()

    assert "generate_ai_context_bundle(" not in source
    assert "PROJECT_ANALYSIS_EVIDENCE" not in source
    assert "E:\\developer_tools" not in source


if __name__ == "__main__":
    test_tab4_runs_enrichment_then_ai_context_bundle_after_collector_success()
    test_tab4_enrichment_process_uses_deterministic_complete_json_cli()
    test_tab4_bundle_process_uses_project_context_bundle_cli()
    test_tab4_bundle_process_has_finish_branch_and_status_log()
    test_tab4_integration_preserves_dynamic_paths_and_no_inline_bundle_write()
    print("JSONCTX011 Tab 4 bundle CLI integration tests passed.")
