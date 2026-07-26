"""Regression test for Show Project to AI final artifact consistency cleanup."""

from __future__ import annotations

import json
import os
import shutil
import tempfile
import zipfile
from pathlib import Path


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _assert_no_bad_text(text: str, bad_tokens: tuple[str, ...], label: str) -> None:
    for token in bad_tokens:
        if token in text:
            raise AssertionError(label + " contains forbidden token: " + token)


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="kanda_show_ai_audit_") as temp_text:
        temp_root = Path(temp_text).resolve()
        project_root = temp_root / "sample_project"
        _write_text(project_root / "pkg" / "__init__.py", "")
        _write_text(project_root / "pkg" / "main.py", "def hello():\n    return 'ok'\n")
        _write_text(project_root / "README.md", "sample project\n")
        _write_text(
            project_root
            / "kanda_prompt_workspace"
            / "prompt_library"
            / "_bundle_temp"
            / "old_manifest.json",
            "{}\n",
        )
        _write_text(
            project_root
            / "kanda_prompt_workspace"
            / "_temp_archived_installers"
            / "old_installer.md",
            "old\n",
        )
        _write_text(project_root / (project_root.name + ".zip"), "not a real zip\n")

        from kanda_reasoner_app.project_analysis_evidence_paths import analysis_json_building_dir
        from kanda_reasoner_app.reasoner_context_bundle import generate_ai_context_bundle
        from kanda_reasoner_app.reasoner_context_bundle.handoff_zip_exporter import (
            export_json_handoff_zip_parts,
        )

        building = analysis_json_building_dir(project_root).resolve(strict=False)
        if building.parent.exists():
            shutil.rmtree(building.parent)
        building.mkdir(parents=True, exist_ok=True)

        old_output = os.environ.get("KANDA_SHOW_PROJECT_TO_AI_JSON_COMPLETE_DIR")
        old_project = os.environ.get("KANDA_SHOW_PROJECT_TO_AI_PROJECT_ROOT")
        try:
            os.environ["KANDA_SHOW_PROJECT_TO_AI_PROJECT_ROOT"] = str(project_root)
            os.environ["KANDA_SHOW_PROJECT_TO_AI_JSON_COMPLETE_DIR"] = str(building)

            bundle_result = generate_ai_context_bundle(project_root)
            if not bundle_result.get("ok"):
                raise AssertionError("Bundle generation failed: " + repr(bundle_result))

            export_result = export_json_handoff_zip_parts(
                project_root,
                building,
                part_size_mb=40,
            )
            if not export_result.get("ok"):
                raise AssertionError("ZIP export failed: " + repr(export_result))
        finally:
            if old_output is None:
                os.environ.pop("KANDA_SHOW_PROJECT_TO_AI_JSON_COMPLETE_DIR", None)
            else:
                os.environ["KANDA_SHOW_PROJECT_TO_AI_JSON_COMPLETE_DIR"] = old_output
            if old_project is None:
                os.environ.pop("KANDA_SHOW_PROJECT_TO_AI_PROJECT_ROOT", None)
            else:
                os.environ["KANDA_SHOW_PROJECT_TO_AI_PROJECT_ROOT"] = old_project

        slug = project_root.name
        bad_stage_tokens = (
            "second_prompt_files_building",
            ".json_handoff_zip_stage_",
            ".json_handoff_zip_work_",
        )

        ai_briefing = json.loads((building / (slug + "__ai_briefing.json")).read_text(encoding="utf-8"))
        false_missing = [
            name
            for name, record in ai_briefing["evidence_files"].items()
            if record.get("exists") is not True
        ]
        if false_missing:
            raise AssertionError("AI briefing reports missing files: " + repr(false_missing))

        bundle_manifest = json.loads((building / (slug + "__bundle_manifest.json")).read_text(encoding="utf-8"))
        self_records = [
            item
            for item in bundle_manifest["artifacts"]
            if item.get("name") == "bundle_manifest_json"
        ]
        if not self_records:
            raise AssertionError("Bundle manifest self-record missing")
        if self_records[0].get("size_status") != "self_size_not_embedded":
            raise AssertionError("Bundle manifest self-size status missing")

        source_manifest = json.loads(
            (building / (slug + "__source_archive_manifest.json")).read_text(encoding="utf-8")
        )
        manifest_text = json.dumps(source_manifest, sort_keys=True)
        _assert_no_bad_text(manifest_text, bad_stage_tokens, "source archive manifest")

        included_paths = [str(item.get("path", "")) for item in source_manifest["included_files"]]
        for token in ("_bundle_temp", "_temp_archived_installers"):
            if any(token in item for item in included_paths):
                raise AssertionError("Legacy temp path included in source archive: " + token)

        handoff_zips = sorted(building.glob(slug + "__ai_handoff*.zip"))
        if not handoff_zips:
            raise AssertionError("No AI handoff ZIPs were generated")
        for zip_path in handoff_zips:
            with zipfile.ZipFile(zip_path) as archive:
                for member_name in archive.namelist():
                    _assert_no_bad_text(member_name, bad_stage_tokens, "ZIP member path")
                    if member_name.endswith((".json", ".txt", ".md")):
                        member_text = archive.read(member_name).decode("utf-8", "replace")
                        _assert_no_bad_text(
                            member_text,
                            bad_stage_tokens,
                            "ZIP member content " + zip_path.name + ":" + member_name,
                        )
    print("VALIDATION OK: show_project_to_ai_final_artifact_consistency_cleanup_v1")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
