"""Focused tests for Tab 2 generated-artifact route detectors."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_artifact_route_detectors import (  # noqa: E501
    detect_workflow_artifact_route_issues,
)
from kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_detector_context import (  # noqa: E501
    WorkflowDetectorContext,
)
from kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_detector_registry import (  # noqa: E501
    DEFAULT_WORKFLOW_DETECTOR_REGISTRY,
)
from kanda_reasoner_app.project_analysis_evidence_paths import (
    analysis_json_parts_dir,
    project_name_from_root,
    relative_primary_evidence_json_path,
    relative_route_manifest_file_path,
    relative_working_copy_json_path,
)


SPLIT_DIR = Path("project_analysis_evidence/json_splitted")


def _context(root: Path, manifest: dict[str, object]) -> WorkflowDetectorContext:
    return WorkflowDetectorContext(
        project_root=root,
        workflow_manifest=manifest,
        workflows_doc="",
    )


def _manifest_with_command(command: dict[str, object]) -> dict[str, object]:
    return {
        "workflows": {
            "integration": {
                "enabled": True,
                "commands": [command],
            }
        }
    }


def _clean_manifest() -> dict[str, object]:
    return {
        "workflows": {
            "integration": {
                "enabled": False,
                "commands": [],
            }
        }
    }


def _project_names(root: Path) -> tuple[str, str, str]:
    name = project_name_from_root(root)
    route_name = Path(relative_route_manifest_file_path(name)).name
    split_manifest = f"{name}_split_manifest.json"
    return name, route_name, split_manifest


def _write_route_files(root: Path, *, route_hash: str = "abc") -> None:
    name, route_name, split_manifest = _project_names(root)
    split_dir = analysis_json_parts_dir(root)
    split_dir.mkdir(parents=True, exist_ok=True)
    (split_dir / split_manifest).write_text(
        json.dumps({"source_sha256": route_hash, "part_count": 1}),
        encoding="utf-8",
    )
    (split_dir / f"001_{name}__complete.chunk.json").write_text(
        json.dumps({"part": 1}),
        encoding="utf-8",
    )
    route_payload = {
        "source_sha256": route_hash,
        "question_routes": {
            "web_ai_readme": [1],
            "symbol_lookup": [1],
            "file_or_box_responsibility": [1],
            "test_protection": [1],
            "local_ai_answer_flow": [1],
            "ui_flow": [1],
        },
    }
    (split_dir / route_name).write_text(
        json.dumps(route_payload),
        encoding="utf-8",
    )


class WorkflowArtifactRouteDetectorTests(unittest.TestCase):
    """Protect generated-artifact route and dual JSON workflow detectors."""

    def test_clean_disabled_manifest_has_no_issues(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "alpha_project"
            root.mkdir()
            _write_route_files(root)

            issues = detect_workflow_artifact_route_issues(
                _context(root, _clean_manifest())
            )

        self.assertEqual(issues, [])

    def test_wrong_output_folder_name_is_error(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "beta_project"
            root.mkdir()
            name = project_name_from_root(root)
            manifest = _manifest_with_command(
                {
                    "name": "wrong output folder",
                    "args": [
                        "{python}",
                        "tool.py",
                        "project_analysis_evidence/json_split/"
                        + f"{name}_split_manifest.json",
                    ],
                }
            )

            issues = detect_workflow_artifact_route_issues(_context(root, manifest))

        self.assertIn(
            "WORKFLOW_OUTPUT_FOLDER_NAMING_MISMATCH",
            {issue.issue_id for issue in issues},
        )

    def test_dual_json_track_in_one_command_is_error(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "gamma_project"
            root.mkdir()
            name = project_name_from_root(root)
            manifest = _manifest_with_command(
                {
                    "name": "mixed tracks",
                    "args": [
                        "compare.py",
                        relative_primary_evidence_json_path(name),
                        relative_working_copy_json_path(name),
                    ],
                }
            )

            issues = detect_workflow_artifact_route_issues(_context(root, manifest))

        self.assertIn(
            "WORKFLOW_DUAL_JSON_TRACK_MISMATCH",
            {issue.issue_id for issue in issues},
        )

    def test_upload_command_without_route_manifest_is_error(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "delta_project"
            root.mkdir()
            name = project_name_from_root(root)
            manifest = _manifest_with_command(
                {
                    "name": "web_ai upload",
                    "args": [
                        "upload.py",
                        "project_analysis_evidence/json_splitted/"
                        + f"001_{name}__complete.chunk.json",
                        "web_ai_readme",
                    ],
                }
            )

            issues = detect_workflow_artifact_route_issues(_context(root, manifest))

        self.assertIn(
            "WORKFLOW_ROUTE_MANIFEST_IGNORED_BY_UPLOAD",
            {issue.issue_id for issue in issues},
        )

    def test_upload_command_without_web_ai_readme_is_error(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "epsilon_project"
            root.mkdir()
            name, route_name, _split_manifest = _project_names(root)
            manifest = _manifest_with_command(
                {
                    "name": "web_ai upload",
                    "args": [
                        "upload.py",
                        "project_analysis_evidence/json_splitted/"
                        + f"001_{name}__complete.chunk.json",
                        "project_analysis_evidence/json_splitted/"
                        + route_name,
                    ],
                }
            )

            issues = detect_workflow_artifact_route_issues(_context(root, manifest))

        self.assertIn(
            "WORKFLOW_WEB_AI_README_IGNORED",
            {issue.issue_id for issue in issues},
        )

    def test_route_manifest_missing_required_route_is_error(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "zeta_project"
            root.mkdir()
            _write_route_files(root)
            _name, route_name, _split_manifest = _project_names(root)
            route_path = root / SPLIT_DIR / route_name
            route_payload = json.loads(route_path.read_text(encoding="utf-8"))
            del route_payload["question_routes"]["local_ai_answer_flow"]
            route_path.write_text(json.dumps(route_payload), encoding="utf-8")

            issues = detect_workflow_artifact_route_issues(
                _context(root, _clean_manifest())
            )

        self.assertIn(
            "WORKFLOW_DETERMINISTIC_ROUTE_MISSING",
            {issue.issue_id for issue in issues},
        )

    def test_route_manifest_hash_mismatch_is_error(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "eta_project"
            root.mkdir()
            _write_route_files(root, route_hash="abc")
            _name, _route_name, split_manifest = _project_names(root)
            split_path = root / SPLIT_DIR / split_manifest
            split_path.write_text(
                json.dumps({"source_sha256": "different", "part_count": 1}),
                encoding="utf-8",
            )

            issues = detect_workflow_artifact_route_issues(
                _context(root, _clean_manifest())
            )

        self.assertIn(
            "WORKFLOW_ROUTE_MANIFEST_STALE",
            {issue.issue_id for issue in issues},
        )

    def test_default_registry_includes_artifact_route_detector(self) -> None:
        names = [
            name
            for name, _detector in DEFAULT_WORKFLOW_DETECTOR_REGISTRY.items()
        ]

        self.assertIn("detect_workflow_artifact_route_issues", names)


if __name__ == "__main__":
    raise SystemExit(unittest.main())
