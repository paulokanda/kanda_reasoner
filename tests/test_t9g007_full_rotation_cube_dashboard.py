"""Regression tests for the Tab 9 full-rotation native cube dashboard."""

from __future__ import annotations

from pathlib import Path


SOURCE = (
    Path(__file__).resolve().parents[1]
    / 'ask_' 'ai_project_reasoner'
    / "prompt_library_gui"
    / "group_dashboard.py"
)


def _source_text() -> str:
    return SOURCE.read_text(encoding="utf-8")


def test_cube_widget_keeps_smaller_fixed_size() -> None:
    text = _source_text()

    assert "_CUBE_SOURCE_WIDTH = 210.0" in text
    assert "_CUBE_SOURCE_HEIGHT = 170.0" in text
    assert "_CUBE_VISUAL_SCALE = 2.0 / 3.0" in text
    assert "self.setFixedSize(_CUBE_WIDGET_WIDTH, _CUBE_WIDGET_HEIGHT)" in text


def test_cube_widget_uses_native_full_rotation_projection() -> None:
    text = _source_text()

    assert "def _rotate_vertex(" in text
    assert "def _project_vertex(" in text
    assert "angle_y = self.rotation_phase" in text
    assert "painter.drawPolygon(polygon)" in text
    assert "for start_index, end_index in self._CUBE_EDGES:" in text


def test_dashboard_animation_is_faster_than_previous_slow_phase_shift() -> None:
    text = _source_text()

    assert "self.animation_timer.setInterval(80)" in text
    assert "self.animation_phase = (self.animation_phase + 0.14) % (math.pi * 2.0)" in text


if __name__ == "__main__":
    test_cube_widget_keeps_smaller_fixed_size()
    test_cube_widget_uses_native_full_rotation_projection()
    test_dashboard_animation_is_faster_than_previous_slow_phase_shift()
    print("T9G007 full rotation cube dashboard tests passed.")
