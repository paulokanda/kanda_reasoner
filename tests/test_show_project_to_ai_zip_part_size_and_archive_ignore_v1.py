from __future__ import annotations

import json
import random
import shutil
import sys
import zipfile
from pathlib import Path
from tempfile import TemporaryDirectory

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.project_analysis_evidence_paths import (  # noqa: E402
    analysis_json_complete_dir,
    project_analysis_evidence_root,
)
from kanda_reasoner_app.reasoner_context_bundle.bundle_orchestrator import (  # noqa: E402
    generate_ai_context_bundle,
)
from kanda_reasoner_app.reasoner_context_bundle.file_manifest_builder import (  # noqa: E402
    build_file_manifest_payload,
)
from kanda_reasoner_app.reasoner_context_bundle.handoff_zip_exporter import (  # noqa: E402
    export_json_handoff_zip_parts,
)
from kanda_reasoner_app.reasoner_context_bundle.output_paths import (  # noqa: E402
    bundle_artifact_paths,
)


def _deterministic_bytes(size: int) -> bytes:
    rng = random.Random(12345)
    return rng.randbytes(size)


def _make_project_with_stray_archive(project_root: Path) -> Path:
    project_root.mkdir(parents=True, exist_ok=True)
    (project_root / "src").mkdir()
    (project_root / "src" / "main.py").write_text('print("hello")\n', encoding="utf-8")
    (project_root / "src" / "large_payload.bin").write_bytes(_deterministic_bytes(120_000))
    (project_root / (project_root.name + ".zip")).write_bytes(_deterministic_bytes(80_000))

    destination = analysis_json_complete_dir(project_root)
    destination.mkdir(parents=True, exist_ok=True)
    paths = bundle_artifact_paths(project_root)
    paths.complete_json.parent.mkdir(parents=True, exist_ok=True)
    paths.complete_json.write_text('{"bundle_kind":"complete_graph"}', encoding="utf-8")
    paths.complete_json.with_name(project_root.name + "__complete_runtime_trace.json").write_text(
        '{"trace_info":{"trace_version":"test"}}',
        encoding="utf-8",
    )
    return destination


def test_project_slug_zip_is_ignored_before_source_archive_export() -> None:
    with TemporaryDirectory(ignore_cleanup_errors=True) as temp_name:
        temp_root = Path(temp_name)
        project_root = temp_root / "demo_project"
        evidence_root = project_analysis_evidence_root(project_root)
        try:
            _make_project_with_stray_archive(project_root)
            manifest = build_file_manifest_payload(project_root)
            paths = [str(item.get("path", "")) for item in manifest.get("files", [])]
            excluded = manifest.get("excluded_path_samples", [])

            assert "demo_project.zip" not in paths
            assert any(
                item.get("path") == "demo_project.zip"
                and item.get("matched_rule") == "show_project_to_ai_recursive_archive_guard"
                for item in excluded
            )

            result = generate_ai_context_bundle(project_root, commands_run_by_bundle=True)
            assert result["ok"] is True, result
            assert not bundle_artifact_paths(project_root).reconstruction_payload_json.exists()
        finally:
            shutil.rmtree(evidence_root, ignore_errors=True)


def test_zip_export_obeys_selected_part_size_without_byte_chunking() -> None:
    with TemporaryDirectory(ignore_cleanup_errors=True) as temp_name:
        temp_root = Path(temp_name)
        project_root = temp_root / "demo_project"
        evidence_root = project_analysis_evidence_root(project_root)
        try:
            destination = _make_project_with_stray_archive(project_root)
            bundle_result = generate_ai_context_bundle(project_root, commands_run_by_bundle=True)
            assert bundle_result["ok"] is True, bundle_result

            max_part_size = 200_000
            result = export_json_handoff_zip_parts(
                project_root,
                destination,
                part_size_mb=40,
                part_size_bytes=max_part_size,
            )

            assert result["ok"] is True, result
            assert result.get("warnings") == []
            zip_paths = [Path(str(item["path"])) for item in result["zip_parts"]]
            assert zip_paths
            assert all(path.stat().st_size <= max_part_size for path in zip_paths)
            assert any(path.name.startswith("demo_project__source_archive_part") for path in zip_paths)
            assert not any(item.get("chunked_artifact") is True for item in result["zip_parts"])

            manifest_path = destination / "demo_project__source_archive_manifest.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            included_paths = {str(item.get("path", "")) for item in manifest.get("included_files", [])}
            assert "demo_project.zip" not in included_paths
            assert "src/main.py" in included_paths
            assert manifest["archive_contract"]["selected_size_cap_bytes"] == max_part_size
            assert manifest["archive_contract"]["planning_target_bytes"] == int(max_part_size * 0.90)
            assert manifest["archive_contract"]["byte_chunking_allowed"] is False

            for path in zip_paths:
                assert zipfile.is_zipfile(path), path
                with zipfile.ZipFile(path) as archive:
                    names = archive.namelist()
                assert not any(name.endswith("CHUNK_MANIFEST.json") for name in names)
                assert not any("/chunks/" in name or name.startswith("chunks/") for name in names)
        finally:
            shutil.rmtree(evidence_root, ignore_errors=True)

def main() -> int:
    test_project_slug_zip_is_ignored_before_source_archive_export()
    test_zip_export_obeys_selected_part_size_without_byte_chunking()
    print("VALIDATION OK: show_project_to_ai_zip_part_size_split_v1")
    print("VALIDATION OK: show project to AI zip part size split")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
