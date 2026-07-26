from __future__ import annotations

import sys
from pathlib import Path
from tempfile import TemporaryDirectory

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.project_analysis_evidence_paths import analysis_json_complete_dir
from kanda_reasoner_app.reasoner_context_bundle.bundle_orchestrator import generate_ai_context_bundle
from kanda_reasoner_app.reasoner_context_bundle.handoff_zip_exporter import export_json_handoff_zip_parts
from kanda_reasoner_app.reasoner_context_bundle.output_paths import bundle_artifact_paths


def _make_generated_bundle(project_root: Path) -> None:
    project_root.mkdir(parents=True, exist_ok=True)
    source_dir = project_root / "src"
    source_dir.mkdir(parents=True, exist_ok=True)
    (source_dir / "main.py").write_text('print("hello")\n', encoding="utf-8")

    paths = bundle_artifact_paths(project_root)
    paths.complete_json.parent.mkdir(parents=True, exist_ok=True)
    paths.complete_json.write_text('{"bundle_kind":"complete_graph"}', encoding="utf-8")
    paths.complete_json.with_name(project_root.name + "__complete_runtime_trace.json").write_text(
        '{"trace_info":{"trace_version":"test"}}',
        encoding="utf-8",
    )

    result = generate_ai_context_bundle(
        project_root,
        command_results={
            "architecture_validate": {
                "ran": True,
                "exit_code": 0,
                "status": "pass",
                "summary": "Architecture validation passed.",
            }
        },
        commands_run_by_bundle=True,
    )
    assert result["ok"] is True, result


def test_show_project_to_ai_artifacts_can_emit_oversize_warnings_without_project_root_failure() -> None:
    with TemporaryDirectory(ignore_cleanup_errors=True) as temp_name:
        temp_root = Path(temp_name)
        project_root = temp_root / "demo_project"
        _make_generated_bundle(project_root)

        destination = analysis_json_complete_dir(project_root)
        destination.mkdir(parents=True, exist_ok=True)
        result = export_json_handoff_zip_parts(
            project_root,
            destination,
            part_size_mb=40,
            part_size_bytes=1,
        )

        assert result["ok"] is True, result
        warnings = result.get("warnings", [])
        assert warnings, result
        assert any("show_project_to_AI" in warning for warning in warnings), warnings
        assert not any("Path is outside the project root" in warning for warning in warnings), warnings


def main() -> int:
    test_show_project_to_ai_artifacts_can_emit_oversize_warnings_without_project_root_failure()
    print("VALIDATION OK: handoff_zip_exporter_external_artifact_warning_v1")
    print("VALIDATION OK: handoff zip exporter external artifact warning")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
