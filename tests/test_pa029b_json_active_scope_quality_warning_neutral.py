"""PA029B warning-neutral JSON active-scope quality tests."""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.reasoner_symbol_atlas.json_active_scope_quality import (
    PROJECT_SYMBOL_ATLAS_JSON_QUALITY_STATUS_ACTIVE_LEAK,
    PROJECT_SYMBOL_ATLAS_JSON_QUALITY_STATUS_TEXT_ONLY,
    ProjectSymbolAtlasJsonActiveScopeQualityOptions,
    check_reasoner_symbol_atlas_json_active_scope_quality,
)


def _write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def test_pa029b_text_mentions_are_not_active_path_leaks() -> None:
    """Source/documentation text may mention reference folders truthfully."""

    with tempfile.TemporaryDirectory() as tmp_dir:
        root = Path(tmp_dir)
        json_path = root / "project_analysis_evidence" / "json_complete" / "sample__complete.json"
        _write_json(
            json_path,
            {
                "source_file_index": {
                    'ask_' 'ai_project_reasoner' '/example.py': {
                        "path": 'ask_' 'ai_project_reasoner' '/example.py',
                        "full_source": "# Memo text mentions _project_reference/old_note.py",
                    }
                },
                "primary_definition_index": {
                    "build_example": 'ask_' 'ai_project_reasoner' '/example.py'
                },
            },
        )

        summary = check_reasoner_symbol_atlas_json_active_scope_quality(
            ProjectSymbolAtlasJsonActiveScopeQualityOptions(
                project_root=str(root),
                json_path=str(json_path),
            )
        )

    assert summary.status == PROJECT_SYMBOL_ATLAS_JSON_QUALITY_STATUS_TEXT_ONLY
    assert summary.active_path_occurrence_count == 0
    assert summary.text_occurrence_count >= 1


def test_pa029b_active_reference_paths_are_detected() -> None:
    """Active indexes must still detect inactive reference-folder leaks."""

    with tempfile.TemporaryDirectory() as tmp_dir:
        root = Path(tmp_dir)
        json_path = root / "project_analysis_evidence" / "json_complete" / "sample__complete.json"
        _write_json(
            json_path,
            {
                "primary_definition_index": {
                    "build_example": "_project_reference/old_owner.py"
                },
                "web_ai_test_protection_index": {
                    "build_example": {
                        "test_to_run": "python tests_archive/test_old_owner.py"
                    }
                },
            },
        )

        summary = check_reasoner_symbol_atlas_json_active_scope_quality(
            ProjectSymbolAtlasJsonActiveScopeQualityOptions(
                project_root=str(root),
                json_path=str(json_path),
            )
        )

    assert summary.status == PROJECT_SYMBOL_ATLAS_JSON_QUALITY_STATUS_ACTIVE_LEAK
    assert summary.active_path_occurrence_count >= 2


def main() -> int:
    test_pa029b_text_mentions_are_not_active_path_leaks()
    test_pa029b_active_reference_paths_are_detected()
    print("PA029B JSON active-scope quality warning-neutral tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
