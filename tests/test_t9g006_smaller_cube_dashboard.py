"""Regression tests for the Tab 9 smaller cube dashboard visual constants."""

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


def test_cube_widget_uses_one_third_smaller_fixed_size() -> None:
    text = _source_text()

    assert "_CUBE_SOURCE_WIDTH = 210.0" in text
    assert "_CUBE_SOURCE_HEIGHT = 170.0" in text
    assert "_CUBE_VISUAL_SCALE = 2.0 / 3.0" in text
    assert "self.setFixedSize(_CUBE_WIDGET_WIDTH, _CUBE_WIDGET_HEIGHT)" in text
    assert "self.setMinimumSize(210, 170)" not in text


def test_cube_painting_scales_existing_geometry() -> None:
    text = _source_text()

    assert "painter.save()" in text
    assert "painter.translate(x_offset, y_offset)" in text
    assert "painter.scale(_CUBE_VISUAL_SCALE, _CUBE_VISUAL_SCALE)" in text
    assert "painter.restore()" in text


if __name__ == "__main__":
    test_cube_widget_uses_one_third_smaller_fixed_size()
    test_cube_painting_scales_existing_geometry()
    print("T9G006 smaller cube dashboard tests passed.")
