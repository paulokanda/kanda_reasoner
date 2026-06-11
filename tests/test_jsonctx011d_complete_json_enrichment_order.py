from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.reasoner_context_collector.complete_json_web_ai_enrichment import (
    REQUIRED_WEB_AI_SECTIONS,
    enrich_complete_json_for_web_ai,
    main as enrichment_main,
)


HELPER_PATH = Path(
    'ask_' 'ai_project_reasoner' '/reasoner_tools_shell/runner_help/window_process_private_impl.py'
)


def _source() -> str:
    return HELPER_PATH.read_text(encoding="utf-8")


def test_tab4_runs_complete_json_enrichment_before_companion_bundle() -> None:
    source = _source()

    assert "def _start_complete_json_enrichment_process(self)" in source
    assert "_start_complete_json_enrichment_process(self)" in source
    assert "kanda_reasoner_app.reasoner_context_collector.complete_json_web_ai_enrichment" in source
    assert "Enriching complete JSON" in source

    collector_done = source.index("event_type=\"collector_run_finished\"")
    enrichment_start = source.index("_start_complete_json_enrichment_process(self)")
    enrichment_handler = source.index('self._active_stage == "Enriching complete JSON"')
    bundle_start = source.index("_start_ai_context_bundle_process(self)", enrichment_handler)

    assert collector_done < enrichment_start
    assert enrichment_handler < bundle_start


def test_complete_json_enrichment_cli_adds_required_sections() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        package_dir = root / "sample_package"
        package_dir.mkdir()
        (package_dir / "__init__.py").write_text("", encoding="utf-8")
        (package_dir / "app.py").write_text(
            "def main():\n"
            "    return 0\n\n"
            "if __name__ == '__main__':\n"
            "    raise SystemExit(main())\n",
            encoding="utf-8",
        )
        complete_json = root / "project_analysis_evidence" / "json_complete" / "sample__complete.json"
        complete_json.parent.mkdir(parents=True)
        complete_json.write_text(
            json.dumps({"files": [], "errors": [], "project_summary": {}}),
            encoding="utf-8",
        )

        result = enrich_complete_json_for_web_ai(complete_json, root)
        assert result["missing_after"] == []

        data = json.loads(complete_json.read_text(encoding="utf-8"))
        for section in REQUIRED_WEB_AI_SECTIONS:
            assert section in data

        exit_code = enrichment_main(
            ["--root", str(root), "--complete-json", str(complete_json), "--compact"]
        )
        assert exit_code == 0


if __name__ == "__main__":
    test_tab4_runs_complete_json_enrichment_before_companion_bundle()
    test_complete_json_enrichment_cli_adds_required_sections()
    print("JSONCTX011D complete JSON enrichment order tests passed.")
