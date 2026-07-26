# project-path: kanda_reasoner_app/reasoner_engine/ai_reasoner_main_window_help/project_qa_analysis_runner.py
"""Run Project Q&A analysis into the dynamic Show Project local-AI JSON.

This command is used by the Project Q&A tab. It intentionally writes generated
analysis evidence outside the selected source tree under
``<project>_show_project_to_AI/second_prompt_files`` and refreshes the local-AI
working copy used for local questions.
"""

from __future__ import annotations

import argparse
import inspect
from pathlib import Path

from kanda_reasoner_app.local_ai_json_contract import refresh_local_ai_copy
from kanda_reasoner_app.project_analysis_evidence_paths import (
    ensure_project_analysis_evidence_dirs,
    primary_evidence_json_path,
    secondary_evidence_json_path,
    working_copy_json_path,
)
from kanda_reasoner_app.reasoner_context_collector.collector_main import run_collector

__all__ = ["main", "run_project_qa_analysis"]


def _resolve_project_root(project_root: str | Path) -> Path:
    """Return a selected project source root and reject generated roots."""
    root = Path(project_root).expanduser().resolve(strict=False)
    if not root.is_dir():
        raise ValueError("Selected project root does not exist: " + str(root))
    if root.name.endswith("_show_project_to_AI"):
        raise ValueError("Select project source, not *_show_project_to_AI: " + str(root))
    if root.name.endswith("_delete_after_daily_work"):
        raise ValueError("Select project source, not *_delete_after_daily_work: " + str(root))
    if root.name in {".project_reference", "_project_reference"}:
        raise ValueError("Reference roots are not active Project Q&A source roots: " + str(root))
    return root


def run_project_qa_analysis(project_root: str | Path) -> dict[str, str]:
    """Generate Project Q&A evidence and refresh the local-AI JSON."""
    root = _resolve_project_root(project_root)
    ensure_project_analysis_evidence_dirs(root)
    canonical_json = primary_evidence_json_path(root)
    runtime_trace_json = secondary_evidence_json_path(root)
    local_ai_json = working_copy_json_path(root)
    canonical_json.parent.mkdir(parents=True, exist_ok=True)
    collector_parameters = inspect.signature(run_collector).parameters
    if len(collector_parameters) >= 3:
        run_collector(str(root), str(canonical_json), str(runtime_trace_json))
    else:
        run_collector(str(root), str(canonical_json))
    if not canonical_json.is_file():
        raise FileNotFoundError("Collector did not create canonical JSON: " + str(canonical_json))
    result = refresh_local_ai_copy(root)
    if not local_ai_json.is_file():
        raise FileNotFoundError("Local-AI JSON was not created: " + str(local_ai_json))
    if not bool(getattr(result, "hashes_match", False)):
        raise RuntimeError("Local-AI JSON hash does not match canonical JSON after refresh.")
    return {
        "project_root": str(root),
        "canonical_json": str(canonical_json),
        "local_ai_json": str(local_ai_json),
        "metadata_json": str(getattr(result, "metadata_json", "")),
        "runtime_trace_json": str(runtime_trace_json),
    }


def _parser() -> argparse.ArgumentParser:
    """Build the CLI parser."""
    parser = argparse.ArgumentParser(description="Run Project Q&A dynamic local-AI analysis")
    parser.add_argument("--project-root", required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the CLI entry point."""
    args = _parser().parse_args(argv)
    result = run_project_qa_analysis(args.project_root)
    print("PROJECT_QA_ANALYSIS_OK")
    print("project_root: " + result["project_root"])
    print("canonical_json: " + result["canonical_json"])
    print("local_ai_json: " + result["local_ai_json"])
    print("metadata_json: " + result["metadata_json"])
    print("runtime_trace_json: " + result["runtime_trace_json"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
