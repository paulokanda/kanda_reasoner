"""Direct protection tests for Brain Navigator extracted brain mesh data."""

from __future__ import annotations

import unittest

from kanda_reasoner_app.reasoner_tools_gui_shell.brain_navigator.assets.brain_mesh_data import get_brain_mesh_data_js, get_brain_mesh_data_summary


class BrainMeshDataDirectTests(unittest.TestCase):
    """Protect the inert extracted mesh asset module."""

    def test_summary_and_constants_are_available(self) -> None:
        """The extracted mesh asset should expose stable source metadata."""

        summary = get_brain_mesh_data_summary()
        self.assertEqual(2605, summary.source_vertex_count)
        self.assertEqual(4850, summary.source_face_count)
        self.assertEqual(9255, summary.surface_dot_count)
        self.assertEqual(3724, summary.visible_edge_count)
        self.assertIn("const TEL_PTS", get_brain_mesh_data_js())


if __name__ == "__main__":
    unittest.main()
