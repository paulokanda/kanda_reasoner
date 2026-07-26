"""Validate rollback of Show Project prompt export to the lightweight-map path."""

from __future__ import annotations

import argparse
import ast
import tempfile
from pathlib import Path
from types import SimpleNamespace

FEATURE_ID = "show-project-lightweight-map-rollback-v1"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def read_python(root: Path, relative: str) -> str:
    path = root / relative
    require(path.is_file(), "Required source file is missing: " + str(path))
    text = path.read_text(encoding="utf-8")
    ast.parse(text, filename=str(path))
    return text


def function_body(text: str, name: str, next_name: str | None = None) -> str:
    start = text.index("def " + name)
    if next_name is None:
        return text[start:]
    end = text.index("def " + next_name, start + 1)
    return text[start:end]


def validate_lightweight_prompt_path(root: Path) -> None:
    relative = (
        "kanda_reasoner_app/reasoner_tools_shell/runner_help/"
        "window_process_private_impl.py"
    )
    text = read_python(root, relative)
    run_body = function_body(text, "_run_collector")

    required = (
        "project_slug + '__source_archive_manifest.json'",
        "project_slug + '__validation_state.json'",
        "step='starting lightweight map generation'",
        "Starting lightweight map generation for hybrid source archive export...",
        "skipped: old complete.json and active_snapshot.json generation",
        "_start_ai_context_bundle_process(self)",
    )
    for marker in required:
        require(marker in run_body, "Lightweight rollback marker missing: " + marker)

    forbidden = (
        "project_slug + '__complete.json'",
        "project_slug + '__complete_runtime_trace.json'",
        "Starting canonical complete JSON generation before companion files...",
        "_start_collector_process(self)",
    )
    for marker in forbidden:
        require(marker not in run_body, "Complete JSON path still active: " + marker)

    collector_body = function_body(
        text,
        "_start_collector_process",
        "_start_complete_json_enrichment_process",
    )
    enrichment_body = function_body(
        text,
        "_start_complete_json_enrichment_process",
        "_start_ai_context_bundle_process",
    )
    require("QProcess" in collector_body, "Separate collector owner was removed.")
    require("--collector-child" in collector_body, "Collector compatibility path changed.")
    require("QProcess" in enrichment_body, "Separate enrichment owner was removed.")
    require(
        "complete_json_web_ai_enrichment" in enrichment_body,
        "Separate enrichment owner changed unexpectedly.",
    )
    require(len(text.splitlines()) <= 500, relative + " exceeds 500 lines.")

    print("LIGHTWEIGHT_MAP_PATH_RESTORED: PASS")
    print("PROMPT_WORKFLOW_COMPLETE_JSON_NOT_INVOKED: PASS")
    print("SEPARATE_COMPLETE_JSON_OWNER_PRESERVED: PASS")


def validate_handoff_contract(root: Path) -> None:
    handoff = read_python(
        root,
        "kanda_reasoner_app/reasoner_context_bundle/handoff_zip_exporter.py",
    )
    orchestrator = read_python(
        root,
        "kanda_reasoner_app/reasoner_context_bundle/bundle_orchestrator.py",
    )
    manifest = read_python(
        root,
        "kanda_reasoner_app/reasoner_context_bundle/bundle_manifest_builder.py",
    )
    support = read_python(
        root,
        "kanda_reasoner_app/reasoner_context_bundle/handoff_zip_exporter_support.py",
    )

    require("write_complete_json_zip_family" not in handoff, "Complete JSON ZIP writer remains active.")
    require('"name": "complete_json"' not in handoff, "Complete JSON package remains active.")
    require("png_assets_reuse_method" in handoff, "PNG reuse observability was lost.")
    require(
        '"complete_json_generated_by_second_prompt_files": False' in orchestrator,
        "Orchestrator contract still claims complete JSON generation.",
    )
    require(
        '"complete_json_generated_by_second_prompt_files": False' in manifest,
        "Bundle manifest still claims complete JSON generation.",
    )
    require(
        '"complete_json_removed_from_normal_output": True' in manifest,
        "Bundle manifest output contract is inconsistent.",
    )
    require(
        "Complete JSON is intentionally excluded from this workflow" in support,
        "Second-upload readme does not describe the rollback.",
    )

    for relative in (
        "kanda_reasoner_app/reasoner_context_bundle/handoff_zip_exporter.py",
        "kanda_reasoner_app/reasoner_context_bundle/bundle_orchestrator.py",
        "kanda_reasoner_app/reasoner_context_bundle/bundle_manifest_builder.py",
        "kanda_reasoner_app/reasoner_context_bundle/handoff_zip_exporter_support.py",
    ):
        path = root / relative
        require(len(path.read_text(encoding="utf-8").splitlines()) <= 500, relative + " exceeds 500 lines.")

    print("COMPLETE_JSON_ZIP_REQUIREMENT_REMOVED: PASS")
    print("LIGHTWEIGHT_HANDOFF_CONTRACT_IN_SYNC: PASS")
    print("PNG_REUSE_RESULT_PRESERVED: PASS")


def validate_export_without_complete_json(root: Path) -> None:
    import sys

    if str(root) not in sys.path:
        sys.path.insert(0, str(root))

    import kanda_reasoner_app.reasoner_context_bundle.handoff_zip_exporter as exporter

    with tempfile.TemporaryDirectory(prefix="kanda_lightweight_rollback_") as temp_text:
        temp = Path(temp_text)
        project = temp / "sample_project"
        project.mkdir()
        destination = temp / "delivery"
        destination.mkdir()
        context = SimpleNamespace(root=project, project_slug="sample_project")

        names = (
            "context_from_project",
            "_validate_destination",
            "_resolve_part_size",
            "_check_bundle_if_requested",
            "_previous_second_prompt_files_for_reuse",
            "write_source_archive_parts",
            "_finalize_ai_context_artifacts_for_handoff",
            "ordered_export_paths",
            "package_specs",
            "write_external_readme",
            "_assert_no_forbidden_outputs",
            "_publish_stage_outputs",
            "_retarget_record_paths",
        )
        original = {name: getattr(exporter, name) for name in names}

        def source_archive(_context, output_stage, _temp_root, **_kwargs):
            source_zip = output_stage / "sample_project__source_archive_part01_of_01.zip"
            source_zip.write_bytes(b"SOURCE")
            manifest_path = output_stage / "sample_project__source_archive_manifest.json"
            manifest_path.write_text("{}", encoding="utf-8")
            record = {
                "filename": source_zip.name,
                "package": "source_archive",
                "artifact_count": 1,
            }
            return {
                "created_paths": [source_zip, manifest_path],
                "manifest_path": str(manifest_path),
                "source_zip_parts": [record],
                "png_asset_zip_parts": [],
                "png_assets_reused": True,
                "png_assets_reuse_method": "hardlink",
            }

        def write_readme(output_stage, _context, _part_size_mb):
            path = output_stage / "sample_project__ai_handoff_upload_readme.txt"
            path.write_text("README", encoding="utf-8")
            return path

        def publish(output_stage, target):
            published = []
            for source in output_stage.iterdir():
                target_path = target / source.name
                target_path.write_bytes(source.read_bytes())
                published.append(target_path)
            return published

        try:
            exporter.context_from_project = lambda _project: context
            exporter._validate_destination = lambda _context, _destination: None
            exporter._resolve_part_size = lambda *_args, **_kwargs: (1024 * 1024, None)
            exporter._check_bundle_if_requested = lambda *_args, **_kwargs: None
            exporter._previous_second_prompt_files_for_reuse = lambda _destination: destination
            exporter.write_source_archive_parts = source_archive
            exporter._finalize_ai_context_artifacts_for_handoff = lambda *_args: None
            exporter.ordered_export_paths = lambda *_args: []
            exporter.package_specs = lambda *_args: []
            exporter.write_external_readme = write_readme
            exporter._assert_no_forbidden_outputs = lambda *_args: None
            exporter._publish_stage_outputs = publish
            exporter._retarget_record_paths = lambda value, *_args: value

            result = exporter.export_json_handoff_zip_parts(
                project,
                destination,
                part_size_mb=1,
                part_size_bytes=1024 * 1024,
                check_bundle=False,
            )
        finally:
            for name, value in original.items():
                setattr(exporter, name, value)

        require(result["ok"] is True, "Export failed without complete JSON: " + repr(result))
        require(result["png_assets_reused"] is True, "PNG reuse result was not preserved.")
        require(result["png_assets_reuse_method"] == "hardlink", "PNG reuse method was lost.")
        require(
            all(item.get("name") != "complete_json" for item in result["packages"]),
            "Complete JSON package was emitted.",
        )
        require(not list(destination.glob("*complete_json*")), "Complete JSON output was created.")

    print("EXPORT_SUCCEEDS_WITHOUT_COMPLETE_JSON: PASS")


def validate_preserved_features(root: Path) -> None:
    window = read_python(
        root,
        "kanda_reasoner_app/reasoner_tools_shell/runner_help/window_methods_private_impl.py",
    )
    controls = read_python(
        root,
        "kanda_reasoner_app/reasoner_tools_shell/runner_help/png_reuse_cancel_controls_private_impl.py",
    )
    inventory = read_python(
        root,
        "kanda_reasoner_app/reasoner_context_bundle/source_tree_exporter_inventory.py",
    )
    archive_io = read_python(
        root,
        "kanda_reasoner_app/reasoner_context_bundle/source_tree_exporter_archive_io.py",
    )
    writer = read_python(
        root,
        "kanda_reasoner_app/reasoner_context_bundle/source_tree_exporter_writer.py",
    )

    require('QPushButton("Logic")' in window, "Logic button rename was lost.")
    require("AI answer Routine Blueprint" not in window, "Removed label returned.")
    require('QPushButton("Cancel")' in controls, "Cancel button was lost.")
    require('QPushButton("Reuse PNG")' in controls, "Reuse PNG button was lost.")
    require("process.terminate()" in controls and "process.kill()" in controls, "Cancel process logic changed.")
    require("content_signature_sha256" in writer, "PNG content identity was lost.")
    require("metadata_identity_matches" in inventory, "PNG fast verification was lost.")
    require("os.link(source_path, destination_zip)" in archive_io, "PNG hard-link reuse was lost.")

    print("TOOLBAR_SURGICAL_UI_PRESERVED: PASS")
    print("CANCEL_AND_REUSE_PNG_CONTROLS_PRESERVED: PASS")
    print("PNG_FAST_REUSE_PRESERVED: PASS")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    require(root.is_dir(), "Project root does not exist: " + str(root))

    validate_lightweight_prompt_path(root)
    validate_handoff_contract(root)
    validate_export_without_complete_json(root)
    validate_preserved_features(root)
    print("MODULE_SIZE_GATE: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
