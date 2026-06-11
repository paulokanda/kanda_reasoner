"""Regression tests for the Tab 9 uncropped full-rotation cube dashboard."""

from __future__ import annotations

import math
import re
from pathlib import Path


SOURCE = (
    Path(__file__).resolve().parents[1]
    / 'ask_' 'ai_project_reasoner'
    / "prompt_library_gui"
    / "group_dashboard.py"
)


def _source_text() -> str:
    return SOURCE.read_text(encoding="utf-8")


def _float_constant(text: str, name: str) -> float:
    pattern = "^" + re.escape(name) + r" = ([0-9.]+)"
    match = re.search(pattern, text, re.MULTILINE)
    if not match:
        raise AssertionError("Missing constant: " + name)
    return float(match.group(1))


def test_cube_uses_normalized_3d_space_not_pixel_depth() -> None:
    text = _source_text()

    assert "_CUBE_HALF_SIZE = 0.78" in text
    assert "_CUBE_CAMERA_DISTANCE = 3.6" in text
    assert "_CUBE_PROJECTION_SCALE = 122.0" in text
    assert "_CUBE_HALF_SIZE = 34.0" not in text
    assert "depth = 0.001" not in text


def test_projected_vertices_stay_inside_source_canvas() -> None:
    text = _source_text()
    half_size = _float_constant(text, "_CUBE_HALF_SIZE")
    camera_distance = _float_constant(text, "_CUBE_CAMERA_DISTANCE")
    projection_scale = _float_constant(text, "_CUBE_PROJECTION_SCALE")
    width = _float_constant(text, "_CUBE_SOURCE_WIDTH")
    height = _float_constant(text, "_CUBE_SOURCE_HEIGHT")

    vertices = [
        (x, y, z)
        for x in (-half_size, half_size)
        for y in (-half_size, half_size)
        for z in (-half_size, half_size)
    ]

    min_x = width
    max_x = 0.0
    min_y = height
    max_y = 0.0

    for step in range(0, 64):
        phase = (math.pi * 2.0) * (step / 64.0)
        angle_y = phase
        angle_x = math.sin(phase * 0.5) * 0.35
        angle_z = math.cos(phase * 0.3) * 0.16

        for x, y, z in vertices:
            cos_x = math.cos(angle_x)
            sin_x = math.sin(angle_x)
            y1 = (y * cos_x) - (z * sin_x)
            z1 = (y * sin_x) + (z * cos_x)

            cos_y = math.cos(angle_y)
            sin_y = math.sin(angle_y)
            x2 = (x * cos_y) + (z1 * sin_y)
            z2 = (-x * sin_y) + (z1 * cos_y)

            cos_z = math.cos(angle_z)
            sin_z = math.sin(angle_z)
            x3 = (x2 * cos_z) - (y1 * sin_z)
            y3 = (x2 * sin_z) + (y1 * cos_z)

            depth = camera_distance - z2
            assert depth > 0.0

            scale = projection_scale / depth
            screen_x = (x3 * scale) + (width / 2.0)
            screen_y = (y3 * scale) + (height / 2.0)
            min_x = min(min_x, screen_x)
            max_x = max(max_x, screen_x)
            min_y = min(min_y, screen_y)
            max_y = max(max_y, screen_y)

    assert min_x > 12.0
    assert max_x < width - 12.0
    assert min_y > 6.0
    assert max_y < height - 6.0


def test_previous_full_rotation_behavior_remains() -> None:
    text = _source_text()

    assert "def _rotate_vertex(" in text
    assert "def _project_vertex(" in text
    assert "angle_y = self.rotation_phase" in text
    assert "for start_index, end_index in self._CUBE_EDGES:" in text
    assert "self.animation_timer.setInterval(80)" in text


if __name__ == "__main__":
    test_cube_uses_normalized_3d_space_not_pixel_depth()
    test_projected_vertices_stay_inside_source_canvas()
    test_previous_full_rotation_behavior_remains()
    print("T9G008 uncropped full rotation cube dashboard tests passed.")
