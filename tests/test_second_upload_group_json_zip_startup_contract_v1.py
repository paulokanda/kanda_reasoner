"""Regression test for two-stage startup and zipped JSON handoff delivery."""

from __future__ import annotations

import os
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _load_startup_generator(repo_root: Path):
    prompt_tools = repo_root / "kanda_prompt_workspace" / "prompt_tools"
    sys.path.insert(0, str(prompt_tools))
    try:
        import sync_startup_routing_kernel_pack as startup_generator
    finally:
        try:
            sys.path.remove(str(prompt_tools))
        except ValueError:
            pass
    return startup_generator


def _assert_contains(text: str, token: str, label: str) -> None:
    if token not in text:
        raise AssertionError(label + " missing token: " + token)


def _assert_not_contains(text: str, token: str, label: str) -> None:
    if token in text:
        raise AssertionError(label + " contains forbidden token: " + token)


def test_startup_read_before_all_announces_second_upload_group(repo_root: Path) -> None:
    startup_generator = _load_startup_generator(repo_root)
    _name, content = startup_generator.make_paste_after_uploading_file(
        "cert",
        "2026-06-24T00:00:00Z",
        "first_prompts_to_ai.zip",
        ["01_ai_prompt_request_canon.md"],
    )

    _assert_contains(content, "Second-upload project handoff rule", "tell_AI_read_before_all")
    _assert_contains(content, "_RUN_COLLECTOR_STATUS.txt", "tell_AI_read_before_all")
    _assert_contains(content, "__ai_handoff_upload_readme.txt", "tell_AI_read_before_all")
    _assert_contains(content, "__ai_handoff_upload*.zip", "tell_AI_read_before_all")
    _assert_contains(content, "UPLOAD_README.txt first, then ai_briefing", "tell_AI_read_before_all")
    _assert_contains(content, "__source_archive_partXX_of_YY.zip only", "tell_AI_read_before_all")
    _assert_contains(content, "The JSON handoff should be consumed from the ZIP package", "tell_AI_read_before_all")


def test_second_prompt_external_readme_declares_json_zip_read_order() -> None:
    from kanda_reasoner_app.reasoner_context_bundle.handoff_zip_exporter_support import external_readme_text
    from kanda_reasoner_app.reasoner_context_bundle.schema_models import ProjectContext

    context = ProjectContext(
        root=Path("/project/sample_project"),
        project_slug="sample_project",
        evidence_root=Path("/tmp/sample_project_show_project_to_AI"),
        json_complete_dir=Path("/tmp/sample_project_show_project_to_AI/second_prompt_files"),
    )
    text = external_readme_text(context, 25)

    _assert_contains(text, "Kanda Reasoner second upload group - read this first", "external README")
    _assert_contains(text, "_RUN_COLLECTOR_STATUS.txt", "external README")
    _assert_contains(text, "sample_project__ai_handoff_upload*.zip", "external README")
    _assert_contains(text, "zipped JSON handoff package", "external README")
    _assert_contains(text, "source_archive_partXX_of_YY.zip only", "external README")
    _assert_contains(text, "respect the selected Show Project to AI size cap", "external README")


def test_json_handoff_upload_zip_respects_explicit_size_cap(repo_root: Path) -> None:
    with tempfile.TemporaryDirectory(prefix="kanda_second_upload_zip_cap_") as temp_text:
        temp_root = Path(temp_text).resolve()
        project_root = temp_root / "sample_project"
        _write_text(project_root / "README.md", "sample\n")
        for index in range(12):
            _write_text(
                project_root / "pkg" / ("module_" + str(index).zfill(2) + ".py"),
                "def value():\n    return " + repr(index) + "\n",
            )

        from kanda_reasoner_app.project_analysis_evidence_paths import analysis_json_building_dir
        from kanda_reasoner_app.reasoner_context_bundle import generate_ai_context_bundle
        from kanda_reasoner_app.reasoner_context_bundle.handoff_zip_exporter import export_json_handoff_zip_parts

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
                part_size_bytes=25000,
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

        upload_zips = sorted(building.glob("sample_project__ai_handoff_upload*.zip"))
        if not upload_zips:
            raise AssertionError("No JSON handoff upload ZIP was generated")
        for path in upload_zips:
            if path.stat().st_size > 25000:
                raise AssertionError("JSON handoff ZIP exceeds selected cap: " + path.name)
            with zipfile.ZipFile(path) as archive:
                names = archive.namelist()
                if not any(name.endswith("UPLOAD_README.txt") for name in names):
                    raise AssertionError("UPLOAD_README.txt missing from " + path.name)
                if any("second_prompt_files_building" in name for name in names):
                    raise AssertionError("Build folder leaked into ZIP member: " + path.name)

        readme = (building / "sample_project__ai_handoff_upload_readme.txt").read_text(encoding="utf-8")
        _assert_contains(readme, "sample_project__ai_handoff_upload*.zip", "second upload README")
        _assert_not_contains(readme, "second_prompt_files_building", "second upload README")


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    test_startup_read_before_all_announces_second_upload_group(repo_root)
    test_second_prompt_external_readme_declares_json_zip_read_order()
    test_json_handoff_upload_zip_respects_explicit_size_cap(repo_root)
    print("VALIDATION OK: startup_second_upload_json_handoff_zip_contract_v1")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
