"""Dashboard widgets for launching Prompt Library group windows."""

from __future__ import annotations

import math

from PySide6.QtCore import QPointF, Qt, QTimer, Signal
from PySide6.QtGui import QColor, QFont, QPainter, QPen, QPolygonF
from PySide6.QtWidgets import QFrame, QGridLayout, QLabel, QScrollArea, QVBoxLayout, QWidget

from .group_catalog import PromptGroup


_COLOR_STYLES = {
    "blue": ("#4c7fd1", "#244c89", "#83afe8", "#eaf2ff", "#12355d"),
    "green": ("#4d9b63", "#2c6840", "#7bc08f", "#effaf1", "#173d25"),
    "gold": ("#c6a24a", "#8a6d1f", "#e1c57a", "#fff8e7", "#5c4305"),
    "orange": ("#cf8a45", "#915623", "#e1ab74", "#fff3ea", "#5e3614"),
    "purple": ("#8460c5", "#5a3f91", "#ae95e2", "#f6f2ff", "#34215f"),
    "red": ("#c66565", "#913f3f", "#e39a9a", "#fff1f1", "#5b2323"),
    "teal": ("#4aa3a0", "#2d6f6d", "#7acac7", "#ecfaf9", "#144443"),
    "gray": ("#8f99a7", "#5a6471", "#bac2ce", "#f5f7fa", "#2b3440"),
    "neutral": ("#7a8797", "#50606f", "#acb8c7", "#f5f7fa", "#253241"),
}


_CUBE_SOURCE_WIDTH = 210.0
_CUBE_SOURCE_HEIGHT = 170.0
_CUBE_VISUAL_SCALE = 2.0 / 3.0
_CUBE_WIDGET_WIDTH = int(round(_CUBE_SOURCE_WIDTH * _CUBE_VISUAL_SCALE))
_CUBE_WIDGET_HEIGHT = int(math.ceil(_CUBE_SOURCE_HEIGHT * _CUBE_VISUAL_SCALE))
_CUBE_HALF_SIZE = 0.78
_CUBE_CAMERA_DISTANCE = 3.6
_CUBE_PROJECTION_SCALE = 122.0


class PromptGroupCubeWidget(QWidget):
    """Paint a low-cost animated 3D cube with full native Qt rotation."""

    _CUBE_EDGES = (
        (0, 1), (1, 2), (2, 3), (3, 0),
        (4, 5), (5, 6), (6, 7), (7, 4),
        (0, 4), (1, 5), (2, 6), (3, 7),
    )
    _CUBE_FACES = (
        (0, 1, 2, 3),
        (4, 5, 6, 7),
        (0, 1, 5, 4),
        (1, 2, 6, 5),
        (2, 3, 7, 6),
        (3, 0, 4, 7),
    )

    def __init__(self, color_role: str, parent: QWidget | None = None) -> None:
        """Create a native Qt cube widget.

        Args:
            color_role: Named color role from the prompt group catalog.
            parent: Optional Qt parent widget.
        """
        super().__init__(parent)
        self.color_role = color_role if color_role in _COLOR_STYLES else "neutral"
        self.rotation_phase = 0.0
        self.setFixedSize(_CUBE_WIDGET_WIDTH, _CUBE_WIDGET_HEIGHT)

    def set_rotation_phase(self, phase: float) -> None:
        """Set the full-rotation phase and repaint."""
        self.rotation_phase = phase
        self.update()

    @staticmethod
    def _rotate_vertex(
        x: float,
        y: float,
        z: float,
        angle_x: float,
        angle_y: float,
        angle_z: float,
    ) -> tuple[float, float, float]:
        """Rotate one cube vertex in 3D space."""
        cos_x = math.cos(angle_x)
        sin_x = math.sin(angle_x)
        y, z = (y * cos_x) - (z * sin_x), (y * sin_x) + (z * cos_x)

        cos_y = math.cos(angle_y)
        sin_y = math.sin(angle_y)
        x, z = (x * cos_y) + (z * sin_y), (-x * sin_y) + (z * cos_y)

        cos_z = math.cos(angle_z)
        sin_z = math.sin(angle_z)
        x, y = (x * cos_z) - (y * sin_z), (x * sin_z) + (y * cos_z)
        return x, y, z

    @staticmethod
    def _project_vertex(x: float, y: float, z: float) -> tuple[float, float, float]:
        """Project one normalized 3D vertex into widget space."""
        depth = _CUBE_CAMERA_DISTANCE - z
        scale = _CUBE_PROJECTION_SCALE / depth
        screen_x = (x * scale) + (_CUBE_SOURCE_WIDTH / 2.0)
        screen_y = (y * scale) + (_CUBE_SOURCE_HEIGHT / 2.0)
        return screen_x, screen_y, z

    def _build_cube_points(self) -> list[tuple[float, float, float]]:
        """Return the projected cube vertices for the current phase."""
        angle_y = self.rotation_phase
        angle_x = math.sin(self.rotation_phase * 0.5) * 0.35
        angle_z = math.cos(self.rotation_phase * 0.3) * 0.16
        points: list[tuple[float, float, float]] = []
        for x in (-_CUBE_HALF_SIZE, _CUBE_HALF_SIZE):
            for y in (-_CUBE_HALF_SIZE, _CUBE_HALF_SIZE):
                for z in (-_CUBE_HALF_SIZE, _CUBE_HALF_SIZE):
                    rx, ry, rz = self._rotate_vertex(x, y, z, angle_x, angle_y, angle_z)
                    points.append(self._project_vertex(rx, ry, rz))
        # Reorder from binary loop order to a cube-friendly fixed vertex order.
        # Coordinates stay normalized so perspective cannot crop the cube.
        reorder = (0, 4, 6, 2, 1, 5, 7, 3)
        return [points[index] for index in reorder]

    def paintEvent(self, _event) -> None:  # pragma: no cover - paint path
        """Paint a fully rotating wireframe-first cube using QPainter only."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)

        base_hex, dark_hex, light_hex, _glow_hex, _text_hex = _COLOR_STYLES[self.color_role]
        base = QColor(base_hex)
        dark = QColor(dark_hex)
        light = QColor(light_hex)
        edge = QColor(light_hex)
        edge.setAlpha(215)
        face_fill = QColor(base)
        face_fill.setAlpha(24)
        back_face_fill = QColor(dark)
        back_face_fill.setAlpha(12)

        painter.fillRect(self.rect(), QColor("#00000000"))
        painter.save()
        x_offset = max(
            0.0,
            (float(self.width()) - (_CUBE_SOURCE_WIDTH * _CUBE_VISUAL_SCALE)) / 2.0,
        )
        y_offset = max(
            0.0,
            (float(self.height()) - (_CUBE_SOURCE_HEIGHT * _CUBE_VISUAL_SCALE)) / 2.0,
        )
        painter.translate(x_offset, y_offset)
        painter.scale(_CUBE_VISUAL_SCALE, _CUBE_VISUAL_SCALE)

        projected_points = self._build_cube_points()
        polygons: list[tuple[float, QPolygonF, float]] = []
        for face in self._CUBE_FACES:
            polygon = QPolygonF([
                QPointF(projected_points[index][0], projected_points[index][1])
                for index in face
            ])
            average_z = sum(projected_points[index][2] for index in face) / float(len(face))
            polygons.append((average_z, polygon, average_z))
        polygons.sort(key=lambda item: item[0])

        shadow_pen = Qt.NoPen
        painter.setPen(shadow_pen)
        shadow_color = QColor(12, 19, 30, 46)
        painter.setBrush(shadow_color)
        painter.drawEllipse(QPointF(_CUBE_SOURCE_WIDTH / 2.0, 130.0), 52.0, 14.0)

        for _sort_key, polygon, average_z in polygons:
            painter.setPen(Qt.NoPen)
            if average_z < 0:
                painter.setBrush(back_face_fill)
            else:
                painter.setBrush(face_fill)
            painter.drawPolygon(polygon)

        edge_pen = QPen(edge)
        edge_pen.setWidth(2)
        painter.setPen(edge_pen)
        painter.setBrush(Qt.NoBrush)
        for start_index, end_index in self._CUBE_EDGES:
            start = projected_points[start_index]
            end = projected_points[end_index]
            painter.drawLine(
                QPointF(start[0], start[1]),
                QPointF(end[0], end[1]),
            )

        vertex_pen = QPen(light)
        vertex_pen.setWidth(1)
        painter.setPen(vertex_pen)
        painter.setBrush(QColor(light.red(), light.green(), light.blue(), 180))
        for x_pos, y_pos, _z_pos in projected_points:
            painter.drawEllipse(QPointF(x_pos, y_pos), 2.6, 2.6)

        painter.setPen(QColor(255, 255, 255, 176))
        symbol_font = QFont()
        symbol_font.setPointSize(18)
        symbol_font.setBold(True)
        painter.setFont(symbol_font)
        painter.drawText(
            0,
            int((_CUBE_SOURCE_HEIGHT / 2.0) + 36),
            int(_CUBE_SOURCE_WIDTH),
            24,
            Qt.AlignCenter,
            "AI",
        )
        painter.restore()


class PromptGroupCube(QFrame):
    """Clickable dashboard cube for one prompt group."""

    activated = Signal(object)

    def __init__(self, group: PromptGroup, prompt_count: int) -> None:
        """Create a group cube card.

        Args:
            group: Group descriptor.
            prompt_count: Number of currently resolved prompts in the group.
        """
        super().__init__()
        self.group = group
        _base_hex, _dark_hex, _light_hex, panel_hex, text_hex = _COLOR_STYLES.get(
            group.color_role,
            _COLOR_STYLES["neutral"],
        )
        self.setFrameShape(QFrame.NoFrame)
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet(
            "QFrame {"
            + "background: "
            + panel_hex
            + "; border: 1px solid rgba(40,60,80,0.12); border-radius: 12px;}"
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(8)

        name = QLabel(group.display_name)
        name.setWordWrap(True)
        name.setAlignment(Qt.AlignCenter)
        name.setStyleSheet(
            "font-weight: bold; font-size: 14px; color: " + text_hex + ";"
        )
        layout.addWidget(name)

        self.cube = PromptGroupCubeWidget(group.color_role)
        layout.addWidget(self.cube, 0, Qt.AlignHCenter)

        description = QLabel(group.description)
        description.setWordWrap(True)
        description.setAlignment(Qt.AlignCenter)
        description.setStyleSheet("color: " + text_hex + "; font-size: 12px;")
        layout.addWidget(description)

        count_label = QLabel("Prompts: " + str(prompt_count))
        count_label.setAlignment(Qt.AlignCenter)
        count_label.setStyleSheet(
            "color: " + text_hex + "; font-weight: 600; font-size: 12px;"
        )
        layout.addWidget(count_label)

        hint = QLabel("Click cube to open")
        hint.setAlignment(Qt.AlignCenter)
        hint.setStyleSheet(
            "color: " + text_hex + "; font-size: 11px; font-style: italic;"
        )
        layout.addWidget(hint)

    def set_rotation_phase(self, phase: float) -> None:
        """Update the embedded cube animation phase."""
        self.cube.set_rotation_phase(phase)

    def mousePressEvent(self, event) -> None:  # pragma: no cover - GUI interaction
        """Open the group window when the cube card is clicked."""
        if event.button() == Qt.LeftButton:
            self.activated.emit(self.group)
        super().mousePressEvent(event)


class PromptGroupDashboard(QWidget):
    """Scrollable dashboard of prompt-group cubes."""

    group_activated = Signal(object)

    def __init__(self) -> None:
        """Create an empty prompt-group dashboard."""
        super().__init__()
        self.cube_cards: list[PromptGroupCube] = []
        self.animation_phase = 0.0

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.NoFrame)
        layout.addWidget(self.scroll_area, 1)

        self.card_host = QWidget()
        self.grid = QGridLayout(self.card_host)
        self.grid.setContentsMargins(6, 6, 6, 6)
        self.grid.setSpacing(16)
        self.scroll_area.setWidget(self.card_host)

        self.animation_timer = QTimer(self)
        self.animation_timer.setInterval(80)
        self.animation_timer.timeout.connect(self._advance_animation)
        self.animation_timer.start()

    def set_groups(self, groups: list[PromptGroup], prompt_counts: dict[str, int]) -> None:
        """Replace the dashboard cubes.

        Args:
            groups: Prompt groups to display.
            prompt_counts: Resolved prompt counts keyed by group_id.
        """
        self._clear_grid()
        self.cube_cards = []
        columns = 2
        for index, group in enumerate(groups):
            card = PromptGroupCube(group, prompt_counts.get(group.group_id, 0))
            card.activated.connect(self.group_activated.emit)
            row = index // columns
            column = index % columns
            self.grid.addWidget(card, row, column)
            self.cube_cards.append(card)
        self.grid.setRowStretch((len(groups) + 1) // columns, 1)

    def showEvent(self, event) -> None:  # pragma: no cover - GUI lifecycle
        """Restart the low-frequency animation timer when the dashboard is visible."""
        super().showEvent(event)
        if not self.animation_timer.isActive():
            self.animation_timer.start()

    def hideEvent(self, event) -> None:  # pragma: no cover - GUI lifecycle
        """Stop animation when the dashboard is hidden to avoid idle work."""
        self.animation_timer.stop()
        super().hideEvent(event)

    def _advance_animation(self) -> None:
        """Advance all cubes using one shared timer."""
        if not self.isVisible():
            self.animation_timer.stop()
            return
        self.animation_phase = (self.animation_phase + 0.14) % (math.pi * 2.0)
        for index, card in enumerate(self.cube_cards):
            card.set_rotation_phase(self.animation_phase + (index * 0.32))

    def _clear_grid(self) -> None:
        """Remove all cards from the dashboard grid."""
        while self.grid.count():
            item = self.grid.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
                widget.deleteLater()
