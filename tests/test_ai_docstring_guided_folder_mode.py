
from __future__ import annotations

import tempfile
from pathlib import Path
import unittest

from kanda_reasoner_app.insert_missing_docstrings_gui.guided_folder_mode import (
    FOLDER_STATE_APPLIED_CLEAN,
    FOLDER_STATE_BLOCKED_BY_SYNTAX_ERROR,
    create_guided_session,
    discover_python_folders,
    load_guided_session,
    mark_folder_state,
    save_guided_session,
    with_current_index,
    with_folder_queue,
)


class GuidedFolderModeTests(unittest.TestCase):
    """Validate isolated guided folder mode primitives."""

    def test_discover_python_folders_ignores_cache_and_virtualenv_dirs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            (root / "pkg").mkdir()
            (root / "pkg" / "__init__.py").write_text("", encoding="utf-8")
            (root / "pkg" / "module.py").write_text("VALUE = 1\n", encoding="utf-8")
            (root / "pkg" / "__pycache__").mkdir()
            (root / "pkg" / "__pycache__" / "ignored.py").write_text("", encoding="utf-8")
            (root / ".venv" / "lib").mkdir(parents=True)
            (root / ".venv" / "lib" / "ignored.py").write_text("", encoding="utf-8")

            queue = discover_python_folders(root)

            self.assertEqual(1, len(queue))
            self.assertEqual("pkg", queue[0].relative_path)
            self.assertEqual(("pkg/__init__.py", "pkg/module.py"), queue[0].python_files)

    def test_session_save_load_roundtrip_preserves_queue_state(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            (root / "alpha").mkdir()
            (root / "alpha" / "a.py").write_text("A = 1\n", encoding="utf-8")
            (root / "beta").mkdir()
            (root / "beta" / "b.py").write_text("B = 1\n", encoding="utf-8")

            session = create_guided_session(root, settings={"fallback": True})
            queue = mark_folder_state(
                session.folder_queue,
                0,
                FOLDER_STATE_APPLIED_CLEAN,
            )
            session = with_folder_queue(session, queue)
            session = with_current_index(session, 1)

            path = save_guided_session(session)
            loaded = load_guided_session(path)

            self.assertEqual(str(root.resolve()), loaded.project_root)
            self.assertEqual(2, len(loaded.folder_queue))
            self.assertEqual(FOLDER_STATE_APPLIED_CLEAN, loaded.folder_queue[0].state)
            self.assertEqual(1, loaded.current_index)
            self.assertTrue(loaded.settings["fallback"])

    def test_current_folder_must_be_resolved_before_continue(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            (root / "pkg").mkdir()
            (root / "pkg" / "module.py").write_text("VALUE = 1\n", encoding="utf-8")

            session = create_guided_session(root)
            self.assertFalse(session.can_continue_to_next_folder())

            blocked_queue = mark_folder_state(
                session.folder_queue,
                0,
                FOLDER_STATE_BLOCKED_BY_SYNTAX_ERROR,
                error="invalid syntax",
            )
            blocked_session = with_folder_queue(session, blocked_queue)
            self.assertFalse(blocked_session.can_continue_to_next_folder())
            self.assertTrue(blocked_session.current_folder().is_blocked())

            resolved_queue = mark_folder_state(
                session.folder_queue,
                0,
                FOLDER_STATE_APPLIED_CLEAN,
            )
            resolved_session = with_folder_queue(session, resolved_queue)
            self.assertTrue(resolved_session.can_continue_to_next_folder())


if __name__ == "__main__":
    unittest.main()
