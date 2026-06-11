"""Tests for the Local-AI JSON Working Copy Box."""

from __future__ import annotations

import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from kanda_reasoner_app.local_ai_json_working_copy.copy_manager import (
    build_default_paths,
    ensure_local_ai_copy,
    get_local_ai_copy_status,
    refresh_local_ai_copy,
)


class LocalAIJsonWorkingCopyTests(unittest.TestCase):
    """Validate copy, refresh, and status-audit behavior."""

    def _make_project(self, root: Path, payload: dict) -> Path:
        paths = build_default_paths(root)
        canonical = paths.canonical_json
        canonical.parent.mkdir(parents=True, exist_ok=True)
        canonical.write_text(json.dumps(payload), encoding="utf-8")
        return canonical

    def test_ensure_creates_local_copy_without_modifying_canonical(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            canonical = self._make_project(root, {"value": "canonical"})

            before = canonical.read_text(encoding="utf-8")
            result = ensure_local_ai_copy(root)
            after = canonical.read_text(encoding="utf-8")

            local_copy = build_default_paths(root).local_ai_json
            metadata = build_default_paths(root).metadata_json
            self.assertEqual(result.action, "created")
            self.assertTrue(local_copy.exists())
            self.assertTrue(metadata.exists())
            self.assertEqual(before, after)
            self.assertEqual(local_copy.read_text(encoding="utf-8"), before)
            self.assertTrue(result.hashes_match)
            self.assertFalse(result.local_is_stale)
            self.assertGreater(result.canonical_size_bytes, 0)
            self.assertGreater(result.local_ai_size_bytes, 0)

    def test_ensure_does_not_overwrite_existing_local_copy(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._make_project(root, {"value": "canonical"})

            local_copy = build_default_paths(root).local_ai_json
            local_copy.parent.mkdir(parents=True, exist_ok=True)
            local_copy.write_text('{"value": "local"}', encoding="utf-8")

            result = ensure_local_ai_copy(root)

            self.assertEqual(result.action, "status")
            self.assertEqual(
                local_copy.read_text(encoding="utf-8"),
                '{"value": "local"}',
            )
            self.assertFalse(result.hashes_match)
            self.assertTrue(result.local_is_stale)

    def test_refresh_overwrites_only_local_copy(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            canonical = self._make_project(root, {"value": "canonical_v1"})

            local_copy = build_default_paths(root).local_ai_json
            local_copy.parent.mkdir(parents=True, exist_ok=True)
            local_copy.write_text('{"value": "local"}', encoding="utf-8")

            canonical.write_text('{"value": "canonical_v2"}', encoding="utf-8")
            result = refresh_local_ai_copy(root)

            self.assertEqual(result.action, "refreshed")
            self.assertEqual(
                local_copy.read_text(encoding="utf-8"),
                '{"value": "canonical_v2"}',
            )
            self.assertEqual(
                canonical.read_text(encoding="utf-8"),
                '{"value": "canonical_v2"}',
            )
            self.assertTrue(result.hashes_match)
            self.assertFalse(result.local_is_stale)

    def test_status_does_not_copy(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._make_project(root, {"value": "canonical"})

            result = get_local_ai_copy_status(root)

            self.assertEqual(result.action, "status")
            self.assertFalse((build_default_paths(root).local_ai_json).exists())
            self.assertFalse(result.local_ai_exists)
            self.assertEqual(result.local_ai_size_bytes, 0)
            self.assertFalse(result.hashes_match)
            self.assertFalse(result.local_is_stale)

    def test_status_reports_stale_existing_local_copy(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._make_project(root, {"value": "canonical"})

            local_copy = build_default_paths(root).local_ai_json
            local_copy.parent.mkdir(parents=True, exist_ok=True)
            local_copy.write_text('{"value": "local"}', encoding="utf-8")

            result = get_local_ai_copy_status(root)

            self.assertTrue(result.local_ai_exists)
            self.assertFalse(result.hashes_match)
            self.assertTrue(result.local_is_stale)
            self.assertGreater(result.canonical_size_bytes, 0)
            self.assertGreater(result.local_ai_size_bytes, 0)

    def test_missing_canonical_fails_on_ensure(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            with self.assertRaises(FileNotFoundError):
                ensure_local_ai_copy(root)


if __name__ == "__main__":
    unittest.main()
