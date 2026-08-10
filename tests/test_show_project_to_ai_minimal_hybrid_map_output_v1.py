"""Regression coverage for minimal Hybrid Source Archive map output.

Second Prompt Files must not generate the old heavy complete.json or
active_snapshot.json payloads.  The normal output is lightweight map JSON plus
source_archive_manifest/source_archive_part ZIPs.
"""

from __future__ import annotations

import json
import shutil
import tempfile
from pathlib import Path
from zipfile import ZipFile

from kanda_reasoner_app.reasoner_context_bundle.bundle_orchestrator import (
    generate_ai_context_bundle,
)
from kanda_reasoner_app.reasoner_context_bundle.handoff_zip_exporter import (
    export_json_handoff_zip_parts,
)


def _make_project(base: Path) -> Path:
    project = base / "sample_project"
    (project / "app").mkdir(parents=True)
    (project / ".git").mkdir()
    (project / "__pycache__").mkdir()
    (project / "app" / "main.py").write_text("print('hello')\n", encoding="utf-8")
    (project / "README.md").write_text("# sample\n", encoding="utf-8")
    (project / ".git" / "config").write_text("ignored\n", encoding="utf-8")
    (project / "__pycache__" / "x.pyc").write_bytes(b"ignored")
    return project


def test_minimal_bundle_does_not_create_complete_or_active_snapshot(monkeypatch) -> None:
    with tempfile.TemporaryDirectory() as tmp_text:
        tmp = Path(tmp_text)
        project = _make_project(tmp)

        # On non-Windows test hosts the dynamic evidence helper uses an anchor
        # level sibling such as /sample_project_show_project_to_AI. Ensure the
        # regression cleans it even when a previous failing run left it behind.
        default_show_root = Path(project.anchor) / (project.name + "_show_project_to_AI")
        shutil.rmtree(default_show_root, ignore_errors=True)

        try:
            result = generate_ai_context_bundle(
                project,
                command_results={},
                check_bundle=True,
                commands_run_by_bundle=False,
            )
            assert result["ok"] is True, result

            output_dir = default_show_root / "second_prompt_files"
            names = {path.name for path in output_dir.iterdir() if path.is_file()}
            assert "sample_project__complete.json" not in names
            assert "sample_project__active_snapshot.json" not in names
            assert "sample_project__reconstruction_payload.json" not in names
            assert "sample_project__ai_briefing.json" in names
            assert "sample_project__routing_manifest.json" in names
            assert "sample_project__bundle_manifest.json" in names

            bundle_manifest = json.loads(
                (output_dir / "sample_project__bundle_manifest.json").read_text(encoding="utf-8")
            )
            artifact_names = {item["name"] for item in bundle_manifest["artifacts"]}
            assert "complete_json" not in artifact_names
            assert "active_snapshot_json" not in artifact_names
            assert bundle_manifest["source_context_contract"]["complete_json_removed_from_normal_output"] is True
            assert bundle_manifest["source_context_contract"]["active_snapshot_removed_from_normal_output"] is True
        finally:
            shutil.rmtree(default_show_root, ignore_errors=True)


def test_export_uses_source_archive_manifest_without_heavy_json(monkeypatch) -> None:
    with tempfile.TemporaryDirectory() as tmp_text:
        tmp = Path(tmp_text)
        project = _make_project(tmp)
        destination = tmp / "dest"
        destination.mkdir()
        default_show_root = Path(project.anchor) / (project.name + "_show_project_to_AI")
        shutil.rmtree(default_show_root, ignore_errors=True)

        try:
            result = generate_ai_context_bundle(
                project,
                command_results={},
                check_bundle=True,
                commands_run_by_bundle=False,
            )
            assert result["ok"] is True, result

            export_result = export_json_handoff_zip_parts(
                project,
                destination,
                part_size_mb=25,
                include_runtime_trace=False,
            )
            assert export_result["ok"] is True, export_result

            names = {path.name for path in destination.iterdir()}
            assert "sample_project__source_archive_manifest.json" in names
            assert any(name.startswith("sample_project__source_archive_part") for name in names)
            assert all("reconstruction_payload" not in name for name in names)
            assert all("active_snapshot" not in name for name in names)
            assert all(not name.endswith("__complete.json") for name in names)

            for zip_path in destination.glob("*.zip"):
                assert zip_path.stat().st_size <= 25 * 1024 * 1024
                with ZipFile(zip_path) as archive:
                    members = archive.namelist()
                assert all("reconstruction_payload" not in member for member in members)
                assert all("active_snapshot" not in member for member in members)
                assert all(not member.endswith("__complete.json") for member in members)
                assert all("CHUNK_MANIFEST.json" not in member for member in members)
                assert all("/chunks/" not in member for member in members)
        finally:
            shutil.rmtree(default_show_root, ignore_errors=True)


def test_gui_run_collector_skips_legacy_heavy_stages() -> None:
    source = Path("kanda_reasoner_app/reasoner_tools_shell/runner_help/window_process_private_impl.py").read_text(encoding="utf-8")
    run_collector = source.split("def _run_collector", 1)[1]
    assert "old heavy complete.json and active_snapshot.json generation" in run_collector
    assert "_start_ai_context_bundle_process(self)" in run_collector
    assert "self._start_ai_context_bundle_process()" not in run_collector
    tail = run_collector.split("_start_ai_context_bundle_process(self)", 1)[1]
    assert "self._start_runtime_trace_process()" not in tail
    assert "_start_collector_process()" not in tail
    assert '"--skip-validation"' in source


def test_auto_zip_process_inherits_second_prompt_build_env() -> None:
    source = Path("kanda_reasoner_app/reasoner_tools_shell/runner_help/zip_json_files_private_impl.py").read_text(encoding="utf-8")
    start_zip = source.split("def _start_zip_process", 1)[1].split("def _existing_dialog_start_folder", 1)[0]
    assert "_tab4_apply_second_prompt_build_env(window, env)" in start_zip
    assert "bundle_manifest artifact is missing" in start_zip
    assert start_zip.index("_tab4_apply_second_prompt_build_env(window, env)") < start_zip.index("_tab4_apply_qprocess_env")


if __name__ == "__main__":
    test_minimal_bundle_does_not_create_complete_or_active_snapshot(None)
    test_export_uses_source_archive_manifest_without_heavy_json(None)
    test_gui_run_collector_skips_legacy_heavy_stages()
    test_auto_zip_process_inherits_second_prompt_build_env()
    print("VALIDATION OK: show_project_to_ai_minimal_hybrid_map_output_v1")
    print("VALIDATION OK: show project to AI minimal hybrid map output")
