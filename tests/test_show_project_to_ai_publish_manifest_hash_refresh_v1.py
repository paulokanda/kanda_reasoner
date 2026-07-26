"""Regression for post-publish bundle-manifest hash refresh in Show Project to AI."""
from __future__ import annotations

import json
import os
import shutil
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.project_analysis_evidence_paths import (
    SHOW_PROJECT_TO_AI_JSON_COMPLETE_DIR_ENV,
    SHOW_PROJECT_TO_AI_PROJECT_ROOT_ENV,
    analysis_json_building_dir,
    analysis_json_complete_dir,
    primary_evidence_json_path,
    project_analysis_evidence_root,
)
from kanda_reasoner_app.reasoner_context_bundle import generate_ai_context_bundle
from kanda_reasoner_app.reasoner_context_bundle.bundle_checker import check_ai_context_bundle
from kanda_reasoner_app.reasoner_tools_shell.runner_help import zip_json_files_private_impl


def _restore_env(key: str, value: str | None) -> None:
    if value is None:
        os.environ.pop(key, None)
    else:
        os.environ[key] = value


def test_publish_refreshes_bundle_manifest_hashes_after_rewriting_build_paths() -> None:
    project_root = Path("/tmp/kanda_manifest_refresh_v1_project")
    evidence_root = project_analysis_evidence_root(project_root)
    if project_root.exists():
        shutil.rmtree(project_root)
    if evidence_root.exists():
        shutil.rmtree(evidence_root)
    project_root.mkdir(parents=True)

    build_dir = analysis_json_building_dir(project_root)
    final_dir = analysis_json_complete_dir(project_root)
    build_dir.mkdir(parents=True)
    final_dir.mkdir(parents=True)

    old_project_root = os.environ.get(SHOW_PROJECT_TO_AI_PROJECT_ROOT_ENV)
    old_output_dir = os.environ.get(SHOW_PROJECT_TO_AI_JSON_COMPLETE_DIR_ENV)
    try:
        os.environ[SHOW_PROJECT_TO_AI_PROJECT_ROOT_ENV] = str(project_root)
        os.environ[SHOW_PROJECT_TO_AI_JSON_COMPLETE_DIR_ENV] = str(build_dir)

        complete_json = primary_evidence_json_path(project_root)
        complete_json.write_text(
            json.dumps(
                {
                    "bundle_kind": "complete_graph",
                    "project": {
                        "project_root_marker": "<PROJECT_ROOT>",
                        "evidence_root_relative": "show_project_to_AI",
                    },
                    "temporary_path_note": "show_project_to_AI/second_prompt_files_building",
                    "files": [],
                },
                sort_keys=True,
            ),
            encoding="utf-8",
        )

        generated = generate_ai_context_bundle(project_root)
        assert generated["ok"] is True, generated.get("failures")
    finally:
        _restore_env(SHOW_PROJECT_TO_AI_PROJECT_ROOT_ENV, old_project_root)
        _restore_env(SHOW_PROJECT_TO_AI_JSON_COMPLETE_DIR_ENV, old_output_dir)

    publish_result = zip_json_files_private_impl.publish_second_prompt_files_building_dir(
        build_dir,
        final_dir,
        project_root=project_root,
    )
    assert publish_result["refreshed_bundle_manifest"]

    check_result = check_ai_context_bundle(project_root)
    assert check_result["ok"] is True, check_result.get("failures")

    manifest_text = (final_dir / "kanda_manifest_refresh_v1_project__bundle_manifest.json").read_text(
        encoding="utf-8"
    )
    assert "second_prompt_files_building" not in manifest_text
    assert "show_project_to_AI/second_prompt_files/" in manifest_text

    try:
        shutil.rmtree(project_root)
        shutil.rmtree(evidence_root)
    except Exception:
        pass


def main() -> int:
    test_publish_refreshes_bundle_manifest_hashes_after_rewriting_build_paths()
    print("VALIDATION OK: show_project_to_ai_publish_manifest_hash_refresh_v1")
    print("VALIDATION OK: show project to AI publish manifest hash refresh")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
