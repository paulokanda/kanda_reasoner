"""
Elegant 3D Buttons Gallery
===========================
Python >= 3.12 | PySide6

15 numbered elegant 3D button models:
  1-3   Grey elegant
  4-6   Blue elegant
  7-9   Green elegant
  10    Fancy but discrete (neutral)
  11-15 Elegant animated buttons

Run:
    pip install PySide6
    python elegant_3d_buttons_demo.py

Pick a number, tell me which one(s) you want to keep, and I'll turn it
into a standalone reusable widget / QSS file for your project.
"""

from __future__ import annotations

import sys

from PySide6.QtCore import (
    QEasingCurve,
    QPoint,
    QPropertyAnimation,
    QRect,
    QSequentialAnimationGroup,
    Qt,
    QVariantAnimation,
)
from PySide6.QtGui import QColor, QFont
from PySide6.QtWidgets import (
    QApplication,
    QGraphicsDropShadowEffect,
    QGridLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

# --------------------------------------------------------------------------
# Fonts (elegant "mockup" font stacks -> falls back gracefully per OS)
# --------------------------------------------------------------------------

FONT_SERIF = "Georgia, 'Cormorant Garamond', 'Times New Roman', serif"
FONT_DISCREET = "'Segoe UI Semilight', 'Helvetica Neue', 'Avenir Next', sans-serif"
FONT_MODERN = "'Century Gothic', 'Montserrat', 'Segoe UI', sans-serif"


def elegant_font(size: int = 11, weight: QFont.Weight = QFont.Weight.DemiBold) -> QFont:
    f = QFont("Segoe UI", size)
    f.setWeight(weight)
    f.setLetterSpacing(QFont.SpacingType.PercentageSpacing, 104)
    return f


# --------------------------------------------------------------------------
# Static QSS-based elegant 3D buttons (models 1-10)
# --------------------------------------------------------------------------

def make_static_button(label: str, qss: str, shadow_color: str, font_family: str) -> QPushButton:
    btn = QPushButton(label)
    btn.setMinimumSize(220, 52)
    btn.setCursor(Qt.CursorShape.PointingHandCursor)
    btn.setFont(elegant_font())
    btn.setStyleSheet(qss + f"font-family: {font_family};")

    shadow = QGraphicsDropShadowEffect(btn)
    shadow.setBlurRadius(18)
    shadow.setOffset(0, 5)
    shadow.setColor(QColor(shadow_color))
    btn.setGraphicsEffect(shadow)
    return btn


STATIC_MODELS: list[tuple[str, str, str, str]] = [
    # (label, qss, shadow color, font)
    (
        "1. Grey Graphite",
        """
        QPushButton {
            border-radius: 0px;
            padding: 10px 22px;
            color: #eef0f2;
            background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
                stop:0 #5b6168, stop:0.5 #43474d, stop:1 #33363b);
            border: 1px solid #2a2c2f;
        }
        QPushButton:hover { background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
            stop:0 #656b73, stop:0.5 #4b4f56, stop:1 #3a3d42); }
        QPushButton:pressed { background: #2f3236; padding-top: 12px; }
        """,
        "#00000090",
        FONT_MODERN,
    ),
    (
        "2. Grey Silver Matte",
        """
        QPushButton {
            border-radius: 0px;
            padding: 10px 22px;
            color: #2b2e33;
            background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
                stop:0 #f4f5f6, stop:0.5 #dfe1e3, stop:1 #c9cbce);
            border: 1px solid #b7b9bc;
        }
        QPushButton:hover { background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
            stop:0 #fbfbfc, stop:1 #d6d8da); }
        QPushButton:pressed { background: #c3c5c8; padding-top: 12px; }
        """,
        "#00000050",
        FONT_DISCREET,
    ),
    (
        "3. Grey Charcoal Glossy",
        """
        QPushButton {
            border-radius: 0px;
            padding: 10px 22px;
            color: #f2f2f2;
            background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
                stop:0 #3a3d42, stop:0.45 #202226, stop:0.46 #17181b, stop:1 #26282c);
            border: 1px solid #101113;
        }
        QPushButton:hover { border: 1px solid #4c4f54; }
        QPushButton:pressed { background: #17181b; padding-top: 12px; }
        """,
        "#000000a0",
        FONT_MODERN,
    ),
    (
        "4. Blue Sapphire",
        """
        QPushButton {
            border-radius: 0px;
            padding: 10px 22px;
            color: #eef4ff;
            background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
                stop:0 #3f6fc4, stop:0.5 #2a4f9c, stop:1 #1c3872);
            border: 1px solid #16305f;
        }
        QPushButton:hover { background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
            stop:0 #4a7bd2, stop:1 #22437f); }
        QPushButton:pressed { background: #1c3872; padding-top: 12px; }
        """,
        "#0a1f4d90",
        FONT_MODERN,
    ),
    (
        "5. Blue Steel Elegant",
        """
        QPushButton {
            border-radius: 0px;
            padding: 10px 22px;
            color: #e8edf5;
            background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
                stop:0 #5c7692, stop:0.5 #435c78, stop:1 #33465e);
            border: 1px solid #2a3a4d;
        }
        QPushButton:hover { background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
            stop:0 #67819d, stop:1 #3a4f68); }
        QPushButton:pressed { background: #2c3c50; padding-top: 12px; }
        """,
        "#00102590",
        FONT_DISCREET,
    ),
    (
        "6. Blue Midnight Glossy",
        """
        QPushButton {
            border-radius: 0px;
            padding: 10px 22px;
            color: #eaf1ff;
            background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
                stop:0 #2b3f66, stop:0.45 #16233d, stop:0.46 #0e1729, stop:1 #1c2c4a);
            border: 1px solid #0a1120;
        }
        QPushButton:hover { border: 1px solid #33507f; }
        QPushButton:pressed { background: #0e1729; padding-top: 12px; }
        """,
        "#000000a0",
        FONT_SERIF,
    ),
    (
        "7. Green Emerald",
        """
        QPushButton {
            border-radius: 0px;
            padding: 10px 22px;
            color: #eafff2;
            background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
                stop:0 #3fa06d, stop:0.5 #2c7d51, stop:1 #1f5c3b);
            border: 1px solid #184a2f;
        }
        QPushButton:hover { background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
            stop:0 #48af78, stop:1 #24693f); }
        QPushButton:pressed { background: #1f5c3b; padding-top: 12px; }
        """,
        "#0a3a2090",
        FONT_MODERN,
    ),
    (
        "8. Green Forest Matte",
        """
        QPushButton {
            border-radius: 0px;
            padding: 10px 22px;
            color: #eef4ee;
            background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
                stop:0 #5c7a63, stop:0.5 #445f4b, stop:1 #334736);
            border: 1px solid #2a3a2d;
        }
        QPushButton:hover { background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
            stop:0 #678868, stop:1 #3a5240); }
        QPushButton:pressed { background: #2c3c2f; padding-top: 12px; }
        """,
        "#0a1a0f90",
        FONT_DISCREET,
    ),
    (
        "9. Green Mint Glossy",
        """
        QPushButton {
            border-radius: 0px;
            padding: 10px 22px;
            color: #eafff5;
            background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
                stop:0 #3d8f6c, stop:0.45 #1f5c44, stop:0.46 #164632, stop:1 #276b4d);
            border: 1px solid #0f3324;
        }
        QPushButton:hover { border: 1px solid #3d8060; }
        QPushButton:pressed { background: #164632; padding-top: 12px; }
        """,
        "#000000a0",
        FONT_SERIF,
    ),
    (
        "10. Fancy but Discreet",
        """
        QPushButton {
            border-radius: 0px;
            padding: 10px 26px;
            color: #4a4a4a;
            background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
                stop:0 #fbfaf7, stop:1 #f0eee9);
            border: 1px solid #d9d6cf;
            letter-spacing: 1px;
        }
        QPushButton:hover { color: #1f1f1f; border: 1px solid #b8a97e; }
        QPushButton:pressed { background: #ece9e2; padding-top: 12px; }
        """,
        "#00000030",
        FONT_SERIF,
    ),
]


# --------------------------------------------------------------------------
# Animated elegant buttons (models 11-15)
# --------------------------------------------------------------------------

class LiftHoverButton(QPushButton):
    """11. Grey elegant — lifts up with growing shadow on hover."""

    def __init__(self, text: str) -> None:
        super().__init__(text)
        self.setMinimumSize(220, 52)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFont(elegant_font())
        self.setStyleSheet(f"""
            QPushButton {{
                border-radius: 0px; padding: 10px 22px; color: #eef0f2;
                font-family: {FONT_MODERN};
                background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
                    stop:0 #63696f, stop:0.5 #494d53, stop:1 #383b40);
                border: 1px solid #2a2c2f;
            }}
        """)
        self._shadow = QGraphicsDropShadowEffect(self)
        self._shadow.setColor(QColor("#00000090"))
        self._shadow.setOffset(0, 4)
        self._shadow.setBlurRadius(14)
        self.setGraphicsEffect(self._shadow)

        self._pos_anim = QPropertyAnimation(self, b"pos")
        self._pos_anim.setDuration(160)
        self._pos_anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._blur_anim = QPropertyAnimation(self._shadow, b"blurRadius")
        self._blur_anim.setDuration(160)
        self._base_pos: QPoint | None = None

    def enterEvent(self, event) -> None:  # noqa: N802
        if self._base_pos is None:
            self._base_pos = self.pos()
        self._animate(self._base_pos + QPoint(0, -4), 26)
        super().enterEvent(event)

    def leaveEvent(self, event) -> None:  # noqa: N802
        if self._base_pos is not None:
            self._animate(self._base_pos, 14)
        super().leaveEvent(event)

    def _animate(self, target_pos: QPoint, target_blur: int) -> None:
        self._pos_anim.stop()
        self._pos_anim.setStartValue(self.pos())
        self._pos_anim.setEndValue(target_pos)
        self._pos_anim.start()
        self._blur_anim.stop()
        self._blur_anim.setStartValue(self._shadow.blurRadius())
        self._blur_anim.setEndValue(target_blur)
        self._blur_anim.start()


class PressDepthButton(QPushButton):
    """12. Blue elegant — presses inward (depth) on click."""

    def __init__(self, text: str) -> None:
        super().__init__(text)
        self.setMinimumSize(220, 52)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFont(elegant_font())
        self.setStyleSheet(f"""
            QPushButton {{
                border-radius: 0px; padding: 10px 22px; color: #eef4ff;
                font-family: {FONT_MODERN};
                background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
                    stop:0 #4a7bd2, stop:0.5 #2a4f9c, stop:1 #1c3872);
                border: 1px solid #16305f;
            }}
        """)
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setColor(QColor("#0a1f4d90"))
        shadow.setOffset(0, 5)
        shadow.setBlurRadius(16)
        self.setGraphicsEffect(shadow)
        self._shadow = shadow
        self._anim = QPropertyAnimation(self, b"geometry")
        self._anim.setDuration(90)
        self._anim.setEasingCurve(QEasingCurve.Type.OutQuad)
        self._base_geom: QRect | None = None

    def mousePressEvent(self, event) -> None:  # noqa: N802
        if self._base_geom is None:
            self._base_geom = self.geometry()
        g = self._base_geom
        pressed = QRect(g.x(), g.y() + 3, g.width(), g.height())
        self._anim.stop()
        self._anim.setStartValue(self.geometry())
        self._anim.setEndValue(pressed)
        self._anim.start()
        self._shadow.setBlurRadius(8)
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event) -> None:  # noqa: N802
        if self._base_geom is not None:
            self._anim.stop()
            self._anim.setStartValue(self.geometry())
            self._anim.setEndValue(self._base_geom)
            self._anim.start()
            self._shadow.setBlurRadius(16)
        super().mouseReleaseEvent(event)


class GlowPulseButton(QPushButton):
    """13. Green elegant — soft glow pulses while hovered."""

    def __init__(self, text: str) -> None:
        super().__init__(text)
        self.setMinimumSize(220, 52)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFont(elegant_font())
        self.setStyleSheet(f"""
            QPushButton {{
                border-radius: 0px; padding: 10px 22px; color: #eafff2;
                font-family: {FONT_SERIF};
                background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
                    stop:0 #48af78, stop:0.5 #2c7d51, stop:1 #1f5c3b);
                border: 1px solid #184a2f;
            }}
        """)
        self._shadow = QGraphicsDropShadowEffect(self)
        self._shadow.setColor(QColor("#2fdc8ea0"))
        self._shadow.setOffset(0, 0)
        self._shadow.setBlurRadius(10)
        self.setGraphicsEffect(self._shadow)

        # Real ping-pong "breathing" glow: grow (10->34) then shrink (34->10),
        # looped forever, using a sequential group instead of a single
        # animation restarting abruptly (which read as "not visible").
        grow = QPropertyAnimation(self._shadow, b"blurRadius")
        grow.setDuration(750)
        grow.setStartValue(10)
        grow.setEndValue(34)
        grow.setEasingCurve(QEasingCurve.Type.InOutSine)

        shrink = QPropertyAnimation(self._shadow, b"blurRadius")
        shrink.setDuration(750)
        shrink.setStartValue(34)
        shrink.setEndValue(10)
        shrink.setEasingCurve(QEasingCurve.Type.InOutSine)

        self._pulse = QSequentialAnimationGroup(self)
        self._pulse.addAnimation(grow)
        self._pulse.addAnimation(shrink)
        self._pulse.setLoopCount(-1)

        # Also pulse the glow color's alpha alongside blur, so the effect is
        # unmistakably visible even on light/grey backgrounds.
        self._color_pulse = QVariantAnimation(self)
        self._color_pulse.setDuration(1500)
        self._color_pulse.setStartValue(QColor("#2fdc8e40"))
        self._color_pulse.setKeyValueAt(0.5, QColor("#5cffb0ff"))
        self._color_pulse.setEndValue(QColor("#2fdc8e40"))
        self._color_pulse.setLoopCount(-1)
        self._color_pulse.setEasingCurve(QEasingCurve.Type.InOutSine)
        self._color_pulse.valueChanged.connect(self._shadow.setColor)

    def enterEvent(self, event) -> None:  # noqa: N802
        self._pulse.stop()
        self._pulse.start()
        self._color_pulse.stop()
        self._color_pulse.start()
        super().enterEvent(event)

    def leaveEvent(self, event) -> None:  # noqa: N802
        self._pulse.stop()
        self._color_pulse.stop()
        self._shadow.setBlurRadius(10)
        self._shadow.setColor(QColor("#2fdc8ea0"))
        super().leaveEvent(event)



class ColorShiftButton(QPushButton):
    """14. Fancy discreet — background gradient shifts smoothly on hover."""

    def __init__(self, text: str) -> None:
        super().__init__(text)
        self.setMinimumSize(220, 52)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFont(elegant_font())
        self._base = QColor("#f0eee9")
        self._highlight = QColor("#e8dcc0")
        self._current = QColor(self._base)
        self._apply_style()

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setColor(QColor("#00000030"))
        shadow.setOffset(0, 3)
        shadow.setBlurRadius(12)
        self.setGraphicsEffect(shadow)

        self._anim = QVariantAnimation(self)
        self._anim.setDuration(220)
        self._anim.valueChanged.connect(self._on_value_changed)

    def _apply_style(self) -> None:
        c = self._current.name()
        self.setStyleSheet(f"""
            QPushButton {{
                border-radius: 0px; padding: 10px 26px; color: #3a3a3a;
                font-family: {FONT_SERIF}; letter-spacing: 1px;
                background-color: {c};
                border: 1px solid #d9d6cf;
            }}
        """)

    def _on_value_changed(self, value: QColor) -> None:
        self._current = value
        self._apply_style()

    def enterEvent(self, event) -> None:  # noqa: N802
        self._anim.stop()
        self._anim.setStartValue(self._current)
        self._anim.setEndValue(self._highlight)
        self._anim.start()
        super().enterEvent(event)

    def leaveEvent(self, event) -> None:  # noqa: N802
        self._anim.stop()
        self._anim.setStartValue(self._current)
        self._anim.setEndValue(self._base)
        self._anim.start()
        super().leaveEvent(event)


class ScaleBounceButton(QPushButton):
    """15. Elegant blue/grey combo — subtle bounce-scale animation on click."""

    def __init__(self, text: str) -> None:
        super().__init__(text)
        self.setMinimumSize(220, 52)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFont(elegant_font())
        self.setStyleSheet(f"""
            QPushButton {{
                border-radius: 0px; padding: 10px 22px; color: #eef0f5;
                font-family: {FONT_MODERN};
                background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
                    stop:0 #5a7396, stop:0.5 #435c78, stop:1 #2e405a);
                border: 1px solid #24344a;
            }}
        """)
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setColor(QColor("#00102590"))
        shadow.setOffset(0, 5)
        shadow.setBlurRadius(16)
        self.setGraphicsEffect(shadow)
        self._base_geom: QRect | None = None
        self.clicked.connect(self._bounce)

    def resizeEvent(self, event) -> None:  # noqa: N802
        if self._base_geom is None:
            self._base_geom = self.geometry()
        super().resizeEvent(event)

    def _bounce(self) -> None:
        if self._base_geom is None:
            self._base_geom = self.geometry()
        g = self._base_geom
        grow = QRect(g.x() - 4, g.y() - 3, g.width() + 8, g.height() + 6)

        grow_anim = QPropertyAnimation(self, b"geometry")
        grow_anim.setDuration(110)
        grow_anim.setStartValue(self.geometry())
        grow_anim.setEndValue(grow)
        grow_anim.setEasingCurve(QEasingCurve.Type.OutQuad)

        settle_anim = QPropertyAnimation(self, b"geometry")
        settle_anim.setDuration(140)
        settle_anim.setStartValue(grow)
        settle_anim.setEndValue(g)
        settle_anim.setEasingCurve(QEasingCurve.Type.OutBack)

        group = QSequentialAnimationGroup(self)
        group.addAnimation(grow_anim)
        group.addAnimation(settle_anim)
        self._bounce_group = group  # keep reference alive
        group.start()


ANIMATED_MODELS: list[tuple[str, type[QPushButton]]] = [
    ("11. Lift on Hover (grey)", LiftHoverButton),
    ("12. Press Depth (blue)", PressDepthButton),
    ("13. Glow Pulse (green)", GlowPulseButton),
    ("14. Color Shift (fancy discreet)", ColorShiftButton),
    ("15. Scale Bounce (blue/grey)", ScaleBounceButton),
]


# --------------------------------------------------------------------------
# Gallery window
# --------------------------------------------------------------------------

class ButtonGallery(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Elegant 3D Buttons — Gallery (choose a number)")
        self.resize(980, 780)
        self.setStyleSheet("QMainWindow { background: #1e2023; }")

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: #1e2023; }")
        self.setCentralWidget(scroll)

        container = QWidget()
        container.setStyleSheet("background: #1e2023;")
        scroll.setWidget(container)

        outer = QVBoxLayout(container)
        outer.setContentsMargins(28, 24, 28, 28)
        outer.setSpacing(18)

        title = QLabel("Elegant 3D Button Models — 15 numbered options")
        title.setStyleSheet(f"color:#f0f0f0; font-size:18px; font-family:{FONT_SERIF};")
        outer.addWidget(title)

        subtitle = QLabel(
            "1-3 grey  •  4-6 blue  •  7-9 green  •  10 fancy/discreet  •  11-15 animated (hover/click)"
        )
        subtitle.setStyleSheet(f"color:#9aa0a6; font-size:12px; font-family:{FONT_DISCREET};")
        outer.addWidget(subtitle)

        grid = QGridLayout()
        grid.setHorizontalSpacing(28)
        grid.setVerticalSpacing(26)
        outer.addLayout(grid)

        row, col = 0, 0
        for label, qss, shadow_color, font in STATIC_MODELS:
            grid.addWidget(make_static_button(label, qss, shadow_color, font), row, col)
            col += 1
            if col == 3:
                col = 0
                row += 1

        if col != 0:
            row += 1
            col = 0

        for label, cls in ANIMATED_MODELS:
            grid.addWidget(cls(label), row, col)
            col += 1
            if col == 3:
                col = 0
                row += 1

        outer.addStretch(1)


def main() -> None:
    app = QApplication(sys.argv)
    win = ButtonGallery()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
