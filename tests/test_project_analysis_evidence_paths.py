"""Regression tests for generated project-analysis evidence paths."""

from __future__ import annotations

from pathlib import Path
import sys
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.project_analysis_evidence_paths import (  # noqa: E402
    analysis_json_complete_dir,
    analysis_json_parts_dir,
    analysis_project_error_memory_dir,
    ensure_project_analysis_evidence_dirs,
    normalize_evidence_artifact_path,
    parts_index_file_path,
    parts_manifest_file_path,
    primary_evidence_json_path,
    project_analysis_evidence_root,
    project_name_from_root,
    relative_primary_evidence_json_path,
    secondary_evidence_json_path,
    show_project_to_ai_root_from_hint,
)


def _as_posix(path: Path) -> str:
    return path.as_posix().replace("\\", "/")


def _expected_show_root(project_root: Path) -> Path:
    if project_root.drive:
        return Path(project_root.anchor) / "kanda_reasoner_show_project_to_AI"
    return project_root.parent / "kanda_reasoner_show_project_to_AI"


class ProjectAnalysisEvidencePathsTests(unittest.TestCase):
    def test_project_analysis_evidence_root_lives_outside_project_root(self) -> None:
        """The active generated evidence root must be outside project source."""
        root = Path("/tmp/any_project")

        evidence_root = project_analysis_evidence_root(root)

        self.assertTrue(
            _as_posix(evidence_root).endswith(
                "any_project_show_project_to_AI"
            )
        )
        self.assertNotIn("project_analysis_evidence", _as_posix(evidence_root))
        self.assertNotIn("architecture_audit", _as_posix(evidence_root))
        self.assertEqual(analysis_json_complete_dir(root), evidence_root / "second_prompt_files")
        self.assertEqual(analysis_json_parts_dir(root), evidence_root / "json_splitted")

    def test_generated_file_names_follow_selected_project_root(self) -> None:
        """Generated JSON filenames must use the selected project root name."""
        root = Path("/tmp/some_other_project")

        self.assertTrue(
            _as_posix(primary_evidence_json_path(root)).endswith(
                "some_other_project_show_project_to_AI/second_prompt_files/"
                "some_other_project__complete.json"
            )
        )
        self.assertTrue(
            _as_posix(secondary_evidence_json_path(root)).endswith(
                "some_other_project_show_project_to_AI/second_prompt_files/"
                "some_other_project__complete_runtime_trace.json"
            )
        )
        self.assertTrue(
            _as_posix(parts_manifest_file_path(root)).endswith(
                "some_other_project_show_project_to_AI/json_splitted/"
                "some_other_project_split_manifest.json"
            )
        )
        self.assertTrue(
            _as_posix(parts_index_file_path(root)).endswith(
                "some_other_project_show_project_to_AI/json_splitted/"
                "some_other_project_split_index.json"
            )
        )

    def test_relative_primary_evidence_json_path_is_name_parameterized(self) -> None:
        """Relative helpers remain stable for manifests and compatibility."""
        self.assertEqual(
            relative_primary_evidence_json_path("alpha_project"),
            "show_project_to_AI/second_prompt_files/alpha_project__complete.json",
        )

    def test_project_name_from_root_sanitizes_unstable_characters(self) -> None:
        """Project names used in filenames should be stable on Windows."""
        self.assertEqual(project_name_from_root(r"E:\My Project 01"), "My_Project_01")

    def test_evidence_dirs_are_created_outside_project_when_requested(self) -> None:
        """The resolver can create external evidence child output folders."""
        import tempfile

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "new_project"
            root.mkdir()

            evidence_root = ensure_project_analysis_evidence_dirs(root)

            self.assertTrue(evidence_root.is_dir())
            self.assertTrue(analysis_json_complete_dir(root).is_dir())
            self.assertTrue(analysis_json_parts_dir(root).is_dir())
            self.assertFalse((root / "project_analysis_evidence").exists())
            self.assertFalse((root / "_project_reference" / "project_analysis_evidence").exists())

    def test_normalize_empty_evidence_artifact_path_uses_dynamic_default(self) -> None:
        """Empty path normalization should fall back to the dynamic default."""
        root = Path("/tmp/another_project")

        path = normalize_evidence_artifact_path(root, "")

        self.assertEqual(path, primary_evidence_json_path(root))

    def test_nested_show_project_hint_canonicalizes_to_external_sibling(self) -> None:
        """A show-project folder inside the source root is never canonical."""
        import tempfile

        with tempfile.TemporaryDirectory() as temp_dir:
            drive_root = Path(temp_dir)
            project_root = drive_root / "kanda_reasoner"
            project_root.mkdir()
            nested_show_root = project_root / "kanda_reasoner_show_project_to_AI"
            nested_error_root = nested_show_root / "project_error_memory"
            nested_pending = nested_error_root / "pending_ai_assisted_error_lesson_intake"
            nested_pending.mkdir(parents=True)
            expected_show_root = _expected_show_root(project_root)

            self.assertEqual(show_project_to_ai_root_from_hint(nested_show_root), expected_show_root)
            self.assertEqual(show_project_to_ai_root_from_hint(nested_error_root), expected_show_root)
            self.assertEqual(show_project_to_ai_root_from_hint(nested_pending), expected_show_root)
            self.assertEqual(
                analysis_project_error_memory_dir(nested_pending),
                expected_show_root / "project_error_memory",
            )

    def test_in_source_project_error_memory_hint_canonicalizes_to_external_sibling(self) -> None:
        """A project_error_memory folder inside source root maps to external memory."""
        import tempfile

        with tempfile.TemporaryDirectory() as temp_dir:
            drive_root = Path(temp_dir)
            project_root = drive_root / "kanda_reasoner"
            project_root.mkdir()
            legacy_error_root = project_root / "project_error_memory"
            legacy_pending = legacy_error_root / "pending_ai_assisted_error_lesson_intake"
            legacy_pending.mkdir(parents=True)
            expected_show_root = _expected_show_root(project_root)

            self.assertEqual(show_project_to_ai_root_from_hint(legacy_error_root), expected_show_root)
            self.assertEqual(show_project_to_ai_root_from_hint(legacy_pending), expected_show_root)
            self.assertEqual(
                analysis_project_error_memory_dir(legacy_error_root),
                expected_show_root / "project_error_memory",
            )


if __name__ == "__main__":
    unittest.main()
