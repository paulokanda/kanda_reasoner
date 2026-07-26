"""Validation for Error Memory second-prompt export integration v1."""

from __future__ import annotations

import json
import sys
import tempfile
import zipfile
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from kanda_reasoner_app.error_memory.models import build_lesson
from kanda_reasoner_app.error_memory.store import save_lesson
from kanda_reasoner_app.reasoner_context_bundle import handoff_zip_exporter as exporter
from kanda_reasoner_app.reasoner_context_bundle.schema_models import ProjectContext


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _active_exportable_lesson(project_root: Path) -> dict[str, Any]:
    return build_lesson(
        selected_project_root=project_root,
        raw_error_text="KeyError: 'ml_pilot_activation_state'",
        operation_phase="validation",
        symptom="Validation failed with KeyError for missing ml_pilot_activation_state.",
        root_cause="GUI state producer did not include the validation-visible key.",
        wrong_assumption="The validation expectation was updated without updating the GUI state producer.",
        correct_fix="Update the GUI readiness/state producer so ml_pilot_activation_state is always returned.",
        long_term_prevention="When adding a validation-visible GUI state key, update producer, consumer, and validation together.",
        do_not_repeat_rule="Do not add validation-visible GUI keys only to tests or validation logic.",
        prevention_triggers=[
            "KeyError for missing GUI state key",
            "missing ml_pilot_activation_state",
        ],
        validation_evidence=[
            "VALIDATION OK: gui-state-key-repair-v1",
            "STATUS: IN_SYNC",
            "ZIP CONTRACT: PASS",
        ],
        status="active",
    )


def _zip_members(zip_path: Path) -> list[str]:
    with zipfile.ZipFile(zip_path, "r") as archive:
        return sorted(archive.namelist())


def _install_monkeypatches(dummy_artifact: Path):
    original_source_archive = exporter.write_source_archive_parts
    original_finalize = exporter._finalize_ai_context_artifacts_for_handoff
    original_check_bundle = exporter._check_bundle_if_requested
    original_ordered_export_paths = exporter.ordered_export_paths

    def fake_source_archive(context, output_stage, temp_root, **_kwargs):
        manifest = output_stage / (context.project_slug + "__source_archive_manifest.json")
        manifest.write_text(
            json.dumps({"artifact_type": "source_archive_manifest", "project_slug": context.project_slug}, indent=2),
            encoding="utf-8",
        )
        return {
            "created_paths": [],
            "manifest_path": str(manifest),
            "source_zip_parts": [],
            "png_asset_zip_parts": [],
            "zip_parts": [],
        }

    exporter.write_source_archive_parts = fake_source_archive
    exporter._finalize_ai_context_artifacts_for_handoff = lambda _context, _destination: None
    exporter._check_bundle_if_requested = lambda _context, _check_bundle: None
    exporter.ordered_export_paths = lambda _context, _include_runtime_trace: [dummy_artifact]

    def restore() -> None:
        exporter.write_source_archive_parts = original_source_archive
        exporter._finalize_ai_context_artifacts_for_handoff = original_finalize
        exporter._check_bundle_if_requested = original_check_bundle
        exporter.ordered_export_paths = original_ordered_export_paths

    return restore


def test_second_prompt_export_includes_compact_error_memory_and_separate_full_zip() -> None:
    with tempfile.TemporaryDirectory(prefix="kanda_error_memory_second_prompt_export_") as tmp:
        tmp_root = Path(tmp)
        project_root = tmp_root / "kanda_export_contract_project"
        project_root.mkdir(parents=True, exist_ok=True)
        evidence_root = tmp_root / "kanda_export_contract_project_show_project_to_AI"
        destination = evidence_root / "second_prompt_files_building"
        destination.mkdir(parents=True, exist_ok=True)

        lesson = _active_exportable_lesson(project_root)
        save_lesson(project_root, lesson)
        _assert(lesson["status"] == "active", "test lesson must be active for export")

        dummy_artifact = destination / (project_root.name + "__validation_state.json")
        dummy_artifact.write_text(
            json.dumps(
                {
                    "bundle_kind": "validation_state",
                    "project": {"project_root_marker": "<PROJECT_ROOT>", "evidence_root_relative": "show_project_to_AI"},
                    "capture_mode": {"runs_commands": False, "mode": "not_run", "internet_or_ai_contact": False},
                },
                indent=2,
            ),
            encoding="utf-8",
        )

        context = ProjectContext(
            root=project_root,
            project_slug=project_root.name,
            evidence_root=evidence_root,
            json_complete_dir=destination,
        )
        restore = _install_monkeypatches(dummy_artifact)
        try:
            result = exporter.export_json_handoff_zip_parts(
                context,
                destination,
                part_size_bytes=20 * 1024 * 1024,
                check_bundle=True,
            )
        finally:
            restore()

        _assert(result.get("ok") is True, "export should succeed: " + json.dumps(result, indent=2))
        error_memory_export = result.get("error_memory_export")
        _assert(isinstance(error_memory_export, dict), "result must expose error_memory_export metadata")
        _assert(error_memory_export.get("status") == "included", "Error Memory export status must be included")
        _assert(error_memory_export.get("active_lesson_count_exported") == 1, "one active lesson should export")
        _assert(error_memory_export.get("full_zip_in_upload_package") is False, "full Error Memory ZIP must stay separate")

        compact_json = destination / (project_root.name + "__error_lessons_compact.json")
        prompt_md = destination / (project_root.name + "__error_memory_ai_prompt.md")
        manifest_json = destination / (project_root.name + "__error_memory_manifest.json")
        full_zip = destination / (project_root.name + "__error_memory_full.zip")
        for path in (compact_json, prompt_md, manifest_json, full_zip):
            _assert(path.exists(), "missing Error Memory export artifact: " + str(path))

        compact_payload = json.loads(compact_json.read_text(encoding="utf-8-sig"))
        _assert(compact_payload["lessons"][0]["lesson_id"] == lesson["lesson_id"], "compact export lost lesson_id")
        manifest_payload = json.loads(manifest_json.read_text(encoding="utf-8-sig"))
        _assert(manifest_payload["compact_error_memory_always_read"] is True, "manifest must declare compact always-read")
        _assert(manifest_payload["full_error_memory_zip"] == full_zip.name, "manifest must name full ZIP sibling")

        upload_records = [item for item in result.get("zip_parts", []) if item.get("package") == "upload"]
        _assert(upload_records, "upload ZIP record missing")
        upload_zip = Path(str(upload_records[0]["path"]))
        _assert(upload_zip.exists(), "upload ZIP missing: " + str(upload_zip))
        members = _zip_members(upload_zip)
        required_suffixes = [
            project_root.name + "__error_memory_ai_prompt.md",
            project_root.name + "__error_lessons_compact.json",
            project_root.name + "__error_memory_manifest.json",
        ]
        for suffix in required_suffixes:
            _assert(any(member.endswith(suffix) for member in members), "upload ZIP missing compact Error Memory file: " + suffix)
        _assert(
            not any(member.endswith(project_root.name + "__error_memory_full.zip") for member in members),
            "full Error Memory ZIP must not be nested inside the upload ZIP",
        )


def test_exporter_source_declares_error_memory_contract() -> None:
    source = Path("kanda_reasoner_app/reasoner_context_bundle/handoff_zip_exporter.py").read_text(encoding="utf-8-sig")
    for fragment in [
        "write_error_memory_ai_send_files",
        "compact_files_in_upload_package",
        "full_zip_policy",
        "sibling_file_open_only_when_needed",
        "error_memory_export",
    ]:
        _assert(fragment in source, "handoff exporter missing Error Memory contract fragment: " + fragment)


def main() -> None:
    test_second_prompt_export_includes_compact_error_memory_and_separate_full_zip()
    test_exporter_source_declares_error_memory_contract()
    print("VALIDATION OK: error-memory-second-prompt-export-v1")
    print("STATUS: IN_SYNC")


if __name__ == "__main__":
    main()
