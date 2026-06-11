"""Focused tests for JSONCTX011B/011D Tab 4 bundle runtime repair."""

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


def test_tab4_starts_bundle_with_module_helper_not_missing_instance_method() -> None:
    source = _source()
    old_runtime_call = "self._start_ai_context_bundle_process()"
    repaired_runtime_call = "_start_ai_context_bundle_process(self)"
    enrichment_stage = 'self._active_stage == "Enriching complete JSON"'

    assert enrichment_stage in source
    assert repaired_runtime_call in source
    assert old_runtime_call not in source
    assert source.index(enrichment_stage) < source.index(repaired_runtime_call, source.index(enrichment_stage))


def test_tab4_bundle_process_function_still_uses_child_cli() -> None:
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


def test_tab4_bundle_repair_keeps_dynamic_paths_and_no_inline_bundle_write() -> None:
    source = _source()

    assert "generate_ai_context_bundle(" not in source
    assert "PROJECT_ANALYSIS_EVIDENCE" not in source
    assert "E:\\developer_tools" not in source


if __name__ == "__main__":
    test_tab4_starts_bundle_with_module_helper_not_missing_instance_method()
    test_tab4_bundle_process_function_still_uses_child_cli()
    test_tab4_bundle_repair_keeps_dynamic_paths_and_no_inline_bundle_write()
    print("JSONCTX011B Tab 4 bundle runtime repair tests passed.")
