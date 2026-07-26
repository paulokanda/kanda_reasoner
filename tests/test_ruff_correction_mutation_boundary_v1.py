"""Behavior tests for Ruff correction storage and guarded apply boundaries."""
from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
import sys
import unittest
from unittest import mock

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

import kanda_reasoner_app.source_hygiene.ruff_correction_apply as ruff_apply
import kanda_reasoner_app.source_hygiene.ruff_correction_storage as ruff_storage
from kanda_reasoner_app.source_hygiene.ruff_correction_errors import (
    RuffCorrectionApplyError,
)


class RuffCorrectionMutationBoundaryTests(unittest.TestCase):
    """Verify deterministic storage and explicit confirmation before mutation."""

    def test_storage_round_trip_is_atomic_and_project_contained(self) -> None:
        with TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "project"
            project_root.mkdir()
            source = project_root / "pkg" / "module.py"
            ruff_storage.atomic_write_text(source, "VALUE = 1\r\n")
            self.assertEqual(source.read_bytes(), b"VALUE = 1\n")

            metadata = project_root / "metadata" / "preview.json"
            ruff_storage.atomic_write_json(
                metadata,
                {"preview_id": "preview-001", "count": 1},
            )
            self.assertEqual(
                ruff_storage.load_json_object(metadata),
                {"count": 1, "preview_id": "preview-001"},
            )
            self.assertEqual(
                ruff_storage.sha256_file(source),
                ruff_storage.sha256_bytes(source.read_bytes()),
            )

            copy = project_root / "copy" / "module.py"
            ruff_storage.copy_file(source, copy)
            self.assertEqual(copy.read_bytes(), source.read_bytes())

            resolved, relative = ruff_storage.ensure_project_relative_file(
                project_root,
                source,
            )
            self.assertEqual(resolved, source.resolve())
            self.assertEqual(relative, "pkg/module.py")

            outside = Path(temp_dir) / "outside.py"
            outside.write_text("VALUE = 2\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "OUTSIDE_PROJECT_ROOT"):
                ruff_storage.ensure_project_relative_file(project_root, outside)

    def test_apply_rejects_wrong_confirmation_before_any_write(self) -> None:
        with TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "project"
            project_root.mkdir()
            paths = ruff_storage.resolve_ruff_correction_paths(project_root)
            record = SimpleNamespace(
                status="PREVIEW_READY",
                files=(SimpleNamespace(relative_path="pkg/module.py"),),
                confirm_token="APPLY_RUFF_CORRECTION_PREVIEW-001",
            )

            with (
                mock.patch.object(
                    ruff_apply,
                    "resolve_ruff_correction_paths",
                    return_value=paths,
                ),
                mock.patch.object(
                    ruff_apply,
                    "load_ruff_correction_preview",
                    return_value=record,
                ),
                mock.patch.object(ruff_apply, "_write_backups") as write_backups,
                mock.patch.object(ruff_apply, "_apply_payload") as apply_payload,
            ):
                with self.assertRaisesRegex(
                    RuffCorrectionApplyError,
                    "CONFIRMATION_TOKEN_MISMATCH",
                ):
                    ruff_apply.apply_ruff_correction_preview(
                        project_root,
                        "preview-001",
                        confirm_token="WRONG_TOKEN",
                    )

            write_backups.assert_not_called()
            apply_payload.assert_not_called()


if __name__ == "__main__":
    unittest.main()
