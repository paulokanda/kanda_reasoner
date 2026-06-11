"""Tests for Kanda Reasoner evidence manifest writer."""

from __future__ import annotations

from datetime import datetime
import json
from pathlib import Path
import tempfile
import unittest

from kanda_reasoner_app.storage_policy.evidence_manifest_writer import (
    EVIDENCE_GENERATOR_APP_NAME,
    EVIDENCE_MANIFEST_FILENAME,
    EVIDENCE_MANIFEST_SCHEMA_VERSION,
    EVIDENCE_README_FILENAME,
    EvidenceManifest,
    build_evidence_manifest,
    evidence_manifest_to_dict,
    get_default_evidence_artifact_names,
    get_evidence_manifest_path,
    get_evidence_readme_path,
    render_evidence_manifest_json,
    render_evidence_readme,
    write_evidence_manifest,
    write_evidence_readme,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = (
    PROJECT_ROOT
    / "kanda_reasoner_app"
    / "storage_policy"
    / "evidence_manifest_writer.py"
)


class StoragePolicyEvidenceManifestWriterTests(unittest.TestCase):
    """Validate evidence manifest and README generation helpers."""

    def test_public_surface_is_declared(self) -> None:
        import kanda_reasoner_app.storage_policy.evidence_manifest_writer as module

        expected = {
            "EVIDENCE_CURRENT_LABEL",
            "EVIDENCE_DEFAULT_APP_VERSION",
            "EVIDENCE_GENERATOR_APP_NAME",
            "EVIDENCE_MANIFEST_FILENAME",
            "EVIDENCE_MANIFEST_SCHEMA_VERSION",
            "EVIDENCE_README_FILENAME",
            "EVIDENCE_RUN_LABEL",
            "EvidenceManifest",
            "build_evidence_manifest",
            "evidence_manifest_to_dict",
            "get_default_evidence_artifact_names",
            "get_evidence_manifest_path",
            "get_evidence_readme_path",
            "render_evidence_manifest_json",
            "render_evidence_readme",
            "write_evidence_manifest",
            "write_evidence_readme",
        }

        self.assertEqual(set(module.__all__), expected)
        for name in expected:
            self.assertTrue(hasattr(module, name))

    def test_build_manifest_uses_dynamic_project_slug_and_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "My Project"
            project_root.mkdir()

            manifest = build_evidence_manifest(
                project_root,
                generated_by_version="1.2.3",
                generated_at=datetime(2026, 1, 1, 12, 30, 45),
            )

        self.assertIsInstance(manifest, EvidenceManifest)
        self.assertEqual(manifest.schema_version, EVIDENCE_MANIFEST_SCHEMA_VERSION)
        self.assertEqual(manifest.generated_by_app, EVIDENCE_GENERATOR_APP_NAME)
        self.assertEqual(manifest.generated_by_version, "1.2.3")
        self.assertEqual(manifest.generated_at, "2026-01-01T12:30:45")
        self.assertEqual(manifest.source_project_slug, "my_project")
        self.assertEqual(manifest.artifact_domain, "architecture_audit")
        self.assertIn("my_project__complete.json", manifest.artifact_list)
        self.assertTrue(manifest.can_regenerate)

    def test_default_artifact_names_use_double_underscore(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "Clinic AI"
            project_root.mkdir()

            artifacts = get_default_evidence_artifact_names(project_root)

        self.assertIn("clinic_ai__complete.json", artifacts)
        self.assertIn("clinic_ai__validation_state.json", artifacts)
        for name in artifacts:
            self.assertIn("__", name)
            self.assertTrue(name.endswith(".json"))

    def test_manifest_to_dict_and_json_are_stable(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "Demo"
            project_root.mkdir()
            manifest = build_evidence_manifest(
                project_root,
                artifact_list=("demo__complete.json",),
                generated_at=datetime(2026, 1, 1, 0, 0, 0),
            )

        data = evidence_manifest_to_dict(manifest)
        rendered = render_evidence_manifest_json(manifest)
        parsed = json.loads(rendered)

        self.assertEqual(data["artifact_list"], ["demo__complete.json"])
        self.assertEqual(parsed["artifact_list"], ["demo__complete.json"])
        self.assertTrue(rendered.endswith("\n"))

    def test_readme_contains_human_readable_context(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "Demo"
            project_root.mkdir()
            manifest = build_evidence_manifest(
                project_root,
                artifact_list=("demo__complete.json",),
                generated_at=datetime(2026, 1, 1, 0, 0, 0),
            )

        text = render_evidence_readme(manifest)

        self.assertIn("Kanda Reasoner Architecture Audit Evidence", text)
        self.assertIn("demo__complete.json", text)
        self.assertIn("These files are generated evidence", text)
        self.assertIn("Can regenerate: true", text)

    def test_paths_are_named_without_creating_files(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output_root = Path(temp_dir) / "audit"
            manifest_path = get_evidence_manifest_path(output_root)
            readme_path = get_evidence_readme_path(output_root)

            self.assertEqual(manifest_path.name, EVIDENCE_MANIFEST_FILENAME)
            self.assertEqual(readme_path.name, EVIDENCE_README_FILENAME)
            self.assertFalse(output_root.exists())

    def test_write_functions_are_explicit_and_respect_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "Demo"
            output_root = Path(temp_dir) / "audit"
            project_root.mkdir()
            manifest = build_evidence_manifest(
                project_root,
                artifact_list=("demo__complete.json",),
                generated_at=datetime(2026, 1, 1, 0, 0, 0),
            )

            manifest_path = write_evidence_manifest(output_root, manifest)
            readme_path = write_evidence_readme(output_root, manifest)

            self.assertTrue(manifest_path.exists())
            self.assertTrue(readme_path.exists())
            with self.assertRaises(FileExistsError):
                write_evidence_manifest(output_root, manifest, overwrite=False)
            with self.assertRaises(FileExistsError):
                write_evidence_readme(output_root, manifest, overwrite=False)

    def test_import_does_not_create_evidence_files(self) -> None:
        before = set(PROJECT_ROOT.glob("EVIDENCE_*"))

        __import__("kanda_reasoner_app.storage_policy.evidence_manifest_writer")

        after = set(PROJECT_ROOT.glob("EVIDENCE_*"))
        self.assertEqual(after, before)

    def test_source_has_no_hardcoded_project_paths(self) -> None:
        text = MODULE_PATH.read_text(encoding="utf-8")

        forbidden_fragments = [
            "E:\\",
            "E:/",
            "_kanda_reasoner_temp",
            "kanda_reasoner_architecture_audit",
            "project_analysis_evidence",
        ]
        for fragment in forbidden_fragments:
            self.assertNotIn(fragment, text)


if __name__ == "__main__":
    unittest.main()
