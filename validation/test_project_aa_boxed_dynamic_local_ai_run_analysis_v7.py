# project-path: validation/test_project_aa_boxed_dynamic_local_ai_run_analysis_v7.py
"""Validate boxed Project A&A dynamic local-AI Run Analysis v2."""

from __future__ import annotations

import json
import os
import py_compile
import shutil
import sys
import tempfile
from pathlib import Path

__all__: list[str] = []

FEATURE_ID = "project-aa-boxed-dynamic-local-ai-run-analysis-v7"
MARKER = "VALIDATION OK: " + FEATURE_ID


def _project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _compile_targets(root: Path) -> None:
    targets = [
        "kanda_reasoner_app/reasoner_engine/ai_reasoner_main_window_help/analysis_controller.py",
        "kanda_reasoner_app/reasoner_engine/ai_reasoner_main_window_help/project_qa_analysis_runner.py",
        "kanda_reasoner_app/reasoner_tools_shell/runner_help/zip_json_files_publish_private_impl.py",
        "kanda_reasoner_app/reasoner_context_bundle/handoff_zip_exporter_support.py",
        "kanda_reasoner_app/reasoner_engine/ai_reasoner_main_window_help/project_json_path_resolver.py",
        "kanda_reasoner_app/local_ai_json_contract.py",
    ]
    for relative in targets:
        py_compile.compile(str(root / relative), doraise=True)


def _assert_static_contracts(root: Path) -> None:
    analysis_text = (
        root / "kanda_reasoner_app/reasoner_engine/ai_reasoner_main_window_help/analysis_controller.py"
    ).read_text(encoding="utf-8")
    runner_text = (
        root / "kanda_reasoner_app/reasoner_engine/ai_reasoner_main_window_help/project_qa_analysis_runner.py"
    ).read_text(encoding="utf-8")
    local_ai_text = (root / "kanda_reasoner_app/local_ai_json_contract.py").read_text(encoding="utf-8")
    runtime_text = (
        root / "kanda_reasoner_app/reasoner_engine/ai_reasoner_main_window_help/runtime_controller.py"
    ).read_text(encoding="utf-8")
    publish_text = (
        root / "kanda_reasoner_app/reasoner_tools_shell/runner_help/zip_json_files_publish_private_impl.py"
    ).read_text(encoding="utf-8")
    readme_text = (
        root / "kanda_reasoner_app/reasoner_context_bundle/handoff_zip_exporter_support.py"
    ).read_text(encoding="utf-8")
    resolver_text = (
        root / "kanda_reasoner_app/reasoner_engine/ai_reasoner_main_window_help/project_json_path_resolver.py"
    ).read_text(encoding="utf-8")

    if "reasoner_engine_data_collector" in analysis_text:
        raise AssertionError("Project A&A Run Analysis still references deleted collector package.")
    if "waitForStarted" in analysis_text:
        raise AssertionError("Project A&A Run Analysis must not block the GUI with waitForStarted.")
    for fragment in (
        "working_copy_json_path(project_root)",
        "project_qa_analysis_runner",
        "process.started.connect",
        "args = ['-m', module_name, '--project-root', project_root]",
    ):
        if fragment not in analysis_text:
            raise AssertionError("Missing analysis-controller fragment: " + fragment)

    for fragment in (
        "inspect.signature(run_collector).parameters",
        "run_collector(str(root), str(canonical_json), str(runtime_trace_json))",
        "run_collector(str(root), str(canonical_json))",
        "refresh_local_ai_copy(root)",
        "primary_evidence_json_path(root)",
        "working_copy_json_path(root)",
        "*_show_project_to_AI",
        "_delete_after_daily_work",
        ".project_reference",
    ):
        if fragment not in runner_text:
            raise AssertionError("Missing project-qa runner fragment: " + fragment)

    for fragment in (
        "tempfile.NamedTemporaryFile",
        "os.replace(temp_path, paths.local_ai_json)",
        "shutil.copyfileobj(source, handle, length=1024 * 1024)",
        "os.fsync(handle.fileno())",
    ):
        if fragment not in local_ai_text:
            raise AssertionError("Missing atomic local-AI copy fragment: " + fragment)

    if "current_project_root_from_window(window)" not in runtime_text:
        raise AssertionError("Runtime controller must use the selected project root resolver.")
    if "resolve_project_json_path(project_root)" not in runtime_text:
        raise AssertionError("Runtime controller must resolve dynamic Project JSON paths.")

    for fragment in (
        "refresh_local_ai_copy",
        "_refresh_project_qa_local_ai_json_before_cleanup",
        "refreshed_project_qa_local_ai_json",
        "name_lower.endswith('__complete_local_ai.json')",
        "name_lower.endswith('__complete_local_ai.meta.json')",
    ):
        if fragment not in publish_text:
            raise AssertionError("Missing publish contract fragment: " + fragment)
    if "Project A&A local-AI working JSON may be retained" not in readme_text:
        raise AssertionError("Upload README wording must disclose local-AI JSON retention.")
    if "if local_ai_json.is_file()" not in resolver_text:
        raise AssertionError("Project JSON resolver must prefer dynamic local-AI JSON when present.")



def _validation_scratch_root(root: Path, label: str) -> Path:
    """Return a validation project source root under canonical daily-work."""
    if root.drive:
        base = Path(root.anchor) / (root.name + "_delete_after_daily_work")
    else:
        base = Path(tempfile.gettempdir()) / (root.name + "_delete_after_daily_work")
    scratch = base / (FEATURE_ID + "_validation") / label
    if scratch.exists():
        shutil.rmtree(scratch, ignore_errors=True)
    scratch.mkdir(parents=True, exist_ok=True)
    return scratch


def _cleanup_dynamic_show_project_root(project_root: Path) -> None:
    """Remove the dynamic Show Project output root created by validation."""
    try:
        from kanda_reasoner_app.project_analysis_evidence_paths import (
            project_analysis_evidence_root,
        )

        show_root = project_analysis_evidence_root(project_root)
    except Exception:
        return
    if show_root.exists() and show_root.name.endswith("_show_project_to_AI"):
        shutil.rmtree(show_root, ignore_errors=True)


def _exercise_project_qa_runner(root: Path) -> None:
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    from kanda_reasoner_app.project_analysis_evidence_paths import (
        primary_evidence_json_path,
        working_copy_json_path,
    )
    from kanda_reasoner_app.reasoner_engine.ai_reasoner_main_window_help import (
        project_qa_analysis_runner as runner,
    )
    from kanda_reasoner_app.reasoner_engine.ai_reasoner_main_window_help.project_json_path_resolver import (
        resolve_project_json_path,
    )

    temp_root = _validation_scratch_root(root, "runner")
    original_run_collector = runner.run_collector
    project_root = temp_root / "sample_project"
    try:
        project_root.mkdir()
        _cleanup_dynamic_show_project_root(project_root)
        (project_root / "app.py").write_text("print(\'ok\')\n", encoding="utf-8")

        def fake_run_collector(project_root_text: str, output_json: str, runtime_trace_json: str | None = None) -> dict:
            payload = {
                "project_summary": {
                    "project_root": project_root_text,
                    "python_file_count": 1,
                    "entry_file_count": 1,
                },
                "files": [{"path": "app.py", "text": "print('ok')\n"}],
                "runtime_trace_json": runtime_trace_json,
            }
            out = Path(output_json)
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
            return payload

        runner.run_collector = fake_run_collector
        result = runner.run_project_qa_analysis(project_root)
        canonical = primary_evidence_json_path(project_root)
        local_ai = working_copy_json_path(project_root)
        if result["canonical_json"] != str(canonical):
            raise AssertionError("Runner wrote canonical JSON outside dynamic Show Project path.")
        if result["local_ai_json"] != str(local_ai):
            raise AssertionError("Runner did not return the dynamic local-AI JSON path.")
        if not canonical.is_file() or not local_ai.is_file():
            raise AssertionError("Runner did not create canonical and local-AI JSON files.")
        if list(local_ai.parent.glob(local_ai.name + ".*.tmp")):
            raise AssertionError("Atomic local-AI JSON refresh left temp files behind.")
        if json.loads(local_ai.read_text(encoding="utf-8"))["project_summary"]["project_root"] != str(project_root):
            raise AssertionError("Local-AI JSON does not describe the selected project.")
        resolution = resolve_project_json_path(project_root)
        if resolution.selected_kind != "local-ai" or resolution.selected_json != local_ai:
            raise AssertionError("Resolver did not select the local-AI working JSON.")
        if "_show_project_to_AI/second_prompt_files" not in str(local_ai).replace("\\", "/"):
            raise AssertionError("Local-AI JSON is not under dynamic Show Project second_prompt_files.")
    finally:
        runner.run_collector = original_run_collector
        _cleanup_dynamic_show_project_root(project_root)
        shutil.rmtree(temp_root, ignore_errors=True)


def _exercise_publish_retention(root: Path) -> None:
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    from kanda_reasoner_app.project_analysis_evidence_paths import (
        analysis_json_building_dir,
        analysis_json_complete_dir,
        primary_evidence_json_path,
        working_copy_json_path,
        working_copy_metadata_path,
    )
    from kanda_reasoner_app.reasoner_tools_shell.runner_help.zip_json_files_publish_private_impl import (
        publish_second_prompt_files_building_dir,
    )

    temp_root = _validation_scratch_root(root, "publish")
    project_root = temp_root / "sample_project"
    try:
        project_root.mkdir()
        _cleanup_dynamic_show_project_root(project_root)
        build_dir = analysis_json_building_dir(project_root)
        final_dir = analysis_json_complete_dir(project_root)
        build_dir.mkdir(parents=True)
        payload = {
            "project_summary": {"project_root": str(project_root), "python_file_count": 1},
            "files": [{"path": "app.py", "text": "print('ok')"}],
        }
        (build_dir / "sample_project__complete.json").write_text(json.dumps(payload), encoding="utf-8")
        (build_dir / "sample_project__ai_handoff_upload.zip").write_bytes(bytes.fromhex("504b0506") + (bytes([0]) * 18))
        (build_dir / "sample_project__file_manifest.json").write_text("{}", encoding="utf-8")
        result = publish_second_prompt_files_building_dir(build_dir, final_dir, project_root=project_root)
        if primary_evidence_json_path(project_root).exists():
            raise AssertionError("Loose canonical complete JSON should be removed after ZIP export.")
        local_ai = working_copy_json_path(project_root)
        meta = working_copy_metadata_path(project_root)
        if not local_ai.is_file() or not meta.is_file():
            raise AssertionError("Publish did not retain local-AI JSON and metadata.")
        refreshed = result.get("refreshed_project_qa_local_ai_json", [])
        if str(local_ai) not in refreshed:
            raise AssertionError("Publish result did not report local-AI JSON refresh.")
        removed = "\n".join(result.get("removed_loose_json_files", []))
        if "complete_local_AI" in removed or "complete_local_ai" in removed.lower():
            raise AssertionError("Loose JSON cleanup reported removal of local-AI working JSON.")
    finally:
        _cleanup_dynamic_show_project_root(project_root)
        shutil.rmtree(temp_root, ignore_errors=True)


def main() -> int:
    root = _project_root()
    _compile_targets(root)
    _assert_static_contracts(root)
    _exercise_project_qa_runner(root)
    _exercise_publish_retention(root)
    print(MARKER)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
