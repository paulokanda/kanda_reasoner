"""Regression test for AI briefing self-hash metadata in Show Project to AI."""

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


def _load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def _assert_ai_briefing_self_record(payload: dict[str, object], label: str) -> None:
    evidence_files = payload.get("evidence_files")
    if not isinstance(evidence_files, dict):
        raise AssertionError(label + " missing evidence_files object")
    record = evidence_files.get("ai_briefing_json")
    if not isinstance(record, dict):
        raise AssertionError(label + " missing ai_briefing_json record")
    if record.get("exists") is not True:
        raise AssertionError(label + " ai_briefing_json must exist")
    if record.get("hash_status") != "self_hash_not_embedded":
        raise AssertionError(label + " embedded an AI briefing self-hash")
    if record.get("sha256") != "":
        raise AssertionError(label + " AI briefing self sha256 must be empty")
    if record.get("size_status") != "self_size_not_embedded":
        raise AssertionError(label + " AI briefing self size status missing")
    if record.get("size_bytes") != 0:
        raise AssertionError(label + " AI briefing self size must not be embedded")


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="kanda_ai_briefing_self_hash_") as temp_text:
        temp_root = Path(temp_text).resolve()
        project_root = temp_root / "sample_project"
        _write_text(project_root / "pkg" / "__init__.py", "")
        _write_text(project_root / "pkg" / "main.py", "def hello():\n    return 'ok'\n")
        _write_text(project_root / "README.md", "sample project\n")

        from kanda_reasoner_app.project_analysis_evidence_paths import analysis_json_building_dir
        from kanda_reasoner_app.reasoner_context_bundle import generate_ai_context_bundle
        from kanda_reasoner_app.reasoner_context_bundle.handoff_zip_exporter import (
            export_json_handoff_zip_parts,
        )
        from kanda_reasoner_app.reasoner_context_bundle.hashing import sha256_file

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
        briefing_path = building / (slug + "__ai_briefing.json")
        manifest_path = building / (slug + "__bundle_manifest.json")
        briefing = _load_json(briefing_path)
        _assert_ai_briefing_self_record(briefing, "loose ai_briefing")

        dynamic_policy = briefing.get("project", {}).get("dynamic_path_policy")
        if "_architecture_audit" in str(dynamic_policy):
            raise AssertionError("AI briefing dynamic path policy is stale")
        if "_show_project_to_AI" not in str(dynamic_policy):
            raise AssertionError("AI briefing dynamic path policy missing show_project_to_AI")

        manifest = _load_json(manifest_path)
        ai_records = [
            item
            for item in manifest.get("artifacts", [])
            if isinstance(item, dict) and item.get("name") == "ai_briefing_json"
        ]
        if not ai_records:
            raise AssertionError("Bundle manifest missing ai_briefing_json record")
        if ai_records[0].get("sha256") != sha256_file(briefing_path):
            raise AssertionError("Bundle manifest is not the AI briefing hash authority")

        upload_zips = sorted(building.glob(slug + "__ai_handoff_upload*.zip"))
        if not upload_zips:
            raise AssertionError("No AI handoff upload ZIP generated")
        found_briefing = False
        for zip_path in upload_zips:
            with zipfile.ZipFile(zip_path) as archive:
                for member_name in archive.namelist():
                    if member_name.endswith(slug + "__ai_briefing.json"):
                        member_payload = json.loads(
                            archive.read(member_name).decode("utf-8")
                        )
                        _assert_ai_briefing_self_record(
                            member_payload,
                            "ZIP ai_briefing " + member_name,
                        )
                        found_briefing = True
        if not found_briefing:
            raise AssertionError("AI briefing not found inside upload ZIP")

    print("VALIDATION OK: show_project_to_ai_ai_briefing_self_hash_contract_v1")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
