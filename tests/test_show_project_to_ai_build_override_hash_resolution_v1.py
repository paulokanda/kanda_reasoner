"""Regression test for build-folder hash resolution during JSON handoff ZIP export."""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path

from kanda_reasoner_app.reasoner_context_bundle.hashing import sha256_file
from kanda_reasoner_app.reasoner_context_bundle.path_normalization import (
    resolve_logical_artifact_path,
)
from kanda_reasoner_app.reasoner_context_bundle.schema_models import ProjectContext


def test_show_project_to_ai_build_override_wins_over_stale_final_artifact() -> None:
    """Logical final paths resolve to building files while build override is active."""
    with tempfile.TemporaryDirectory() as temp_dir:
        base = Path(temp_dir)
        project_root = base / "kanda_reasoner"
        evidence_root = base / "kanda_reasoner_show_project_to_AI"
        final_dir = evidence_root / "second_prompt_files"
        building_dir = evidence_root / "second_prompt_files_building"
        project_root.mkdir()
        final_dir.mkdir(parents=True)
        building_dir.mkdir(parents=True)

        final_briefing = final_dir / "kanda_reasoner__ai_briefing.json"
        build_briefing = building_dir / "kanda_reasoner__ai_briefing.json"
        bundle_manifest = building_dir / "kanda_reasoner__bundle_manifest.json"

        final_briefing.write_text('{"version": "stale-final"}\n', encoding="utf-8")
        build_briefing.write_text('{"version": "current-building"}\n', encoding="utf-8")
        bundle_manifest.write_text(
            json.dumps(
                {
                    "artifacts": [
                        {
                            "path": "show_project_to_AI/second_prompt_files/kanda_reasoner__ai_briefing.json",
                            "sha256": sha256_file(build_briefing),
                            "required": True,
                        }
                    ]
                },
                indent=2,
            ),
            encoding="utf-8",
        )

        context = ProjectContext(
            root=project_root,
            project_slug="kanda_reasoner",
            evidence_root=evidence_root,
            json_complete_dir=building_dir,
        )

        old_override = os.environ.get("KANDA_SHOW_PROJECT_TO_AI_JSON_COMPLETE_DIR")
        os.environ["KANDA_SHOW_PROJECT_TO_AI_JSON_COMPLETE_DIR"] = str(building_dir)
        try:
            resolved = resolve_logical_artifact_path(
                context,
                "show_project_to_AI/second_prompt_files/kanda_reasoner__ai_briefing.json",
            )
            assert resolved == build_briefing.resolve(strict=False)

            assert sha256_file(resolved) == sha256_file(build_briefing)
            assert sha256_file(resolved) != sha256_file(final_briefing)
        finally:
            if old_override is None:
                os.environ.pop("KANDA_SHOW_PROJECT_TO_AI_JSON_COMPLETE_DIR", None)
            else:
                os.environ["KANDA_SHOW_PROJECT_TO_AI_JSON_COMPLETE_DIR"] = old_override


if __name__ == "__main__":
    test_show_project_to_ai_build_override_wins_over_stale_final_artifact()
