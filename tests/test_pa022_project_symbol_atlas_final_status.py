"""PA022 final hardening/status tests."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from kanda_reasoner_app.reasoner_symbol_atlas.final_status import (  # noqa: E402
    ProjectSymbolAtlasFinalStatusOptions,
    build_reasoner_symbol_atlas_final_status,
)


def test_pa022_final_status_runs_on_current_project() -> None:
    result = build_reasoner_symbol_atlas_final_status(
        ProjectSymbolAtlasFinalStatusOptions(project_root=ROOT)
    )
    assert result.status in {"complete", "incomplete"}
    assert result.legacy_evidence_required is False
    assert result.canonical_evidence_dir.endswith("project_analysis_evidence")
    assert "pre-patch-gate" in result.expected_cli_commands
    assert "pre-patch-gate" in result.expected_gui_commands


def main() -> int:
    test_pa022_final_status_runs_on_current_project()
    print("PA022 Project Symbol Atlas final status tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
