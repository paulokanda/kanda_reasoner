"""
Kanda Reasoner — Tab Process Animation Demo
Elegant PySide6 animation showing active process state per tab.

Run:  python kanda_tab_animation_demo.py
Deps: pip install PySide6
"""

import sys
import math
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QLabel, QPushButton, QSizePolicy,
)
from PySide6.QtCore import (
    Qt, QTimer, QPropertyAnimation, QEasingCurve,
    Property, QObject, Signal, QPoint, QRect, QSize,
)
from PySide6.QtGui import (
    QPainter, QColor, QPen, QBrush, QLinearGradient,
    QRadialGradient, QFont, QPainterPath, QFontDatabase,
    QConicalGradient,
)

# ─────────────────────────────────────────────────────────────────────────────
# PALETTE  — deep dark base, sharp jewel accents
# ─────────────────────────────────────────────────────────────────────────────
DARK_BG      = QColor("#0d0f14")
PANEL_BG     = QColor("#13161e")
BORDER       = QColor("#1e2330")
TEXT_DIM     = QColor("#4a5068")
TEXT_MID     = QColor("#8892aa")
TEXT_BRIGHT  = QColor("#d4daf0")

TAB_COLORS = [
    ("#4fc3f7", "#0288d1"),   # 0 ice blue
    ("#a78bfa", "#6d28d9"),   # 1 violet
    ("#34d399", "#059669"),   # 2 emerald
    ("#fb923c", "#c2410c"),   # 3 amber
    ("#f472b6", "#be185d"),   # 4 rose
    ("#38bdf8", "#0369a1"),   # 5 sky
    ("#facc15", "#b45309"),   # 6 gold
    ("#a3e635", "#4d7c0f"),   # 7 lime
    ("#e879f9", "#a21caf"),   # 8 fuchsia
]

TAB_LABELS = [
    "Collector", "Parser", "Manual Review",
    "ZIP Export", "Evidence", "Reasoner",
    "Ollama", "Atlas", "Prompts",
]

STATES = ["idle", "running", "done", "error"]


# ─────────────────────────────────────────────────────────────────────────────
# ARC SPINNER  — custom widget, single animated arc
# ─────────────────────────────────────────────────────────────────────────────
class ArcSpinner(QWidget):
    def __init__(self, color_pair, size=38, parent=None):
        super().__init__(parent)
        self._color_hi = QColor(color_pair[0])
        self._color_lo = QColor(color_pair[1])
        self._angle = 0.0
        self._pulse = 0.0
        self._active = False
        self._done = False
        self._error = False
        self.setFixedSize(size, size)
        self._sz = size

    def set_angle(self, a):
        self._angle = a
        self.update()

    def set_pulse(self, p):
        self._pulse = p
        self.update()

    def set_state(self, state):
        self._active = state == "running"
        self._done   = state == "done"
        self._error  = state == "error"
        self.update()

    def paintEvent(self, _):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        sz = self._sz
        cx = cy = sz / 2
        r  = sz / 2 - 3

        # ── track ring
        pen = QPen(BORDER, 2.5)
        p.setPen(pen)
        p.drawEllipse(QRect(3, 3, sz - 6, sz - 6))

        if self._done:
            # checkmark fill
            p.setPen(Qt.NoPen)
            grad = QRadialGradient(cx, cy, r)
            grad.setColorAt(0, self._color_hi.lighter(120))
            grad.setColorAt(1, self._color_lo)
            p.setBrush(QBrush(grad))
            p.drawEllipse(QRect(3, 3, sz - 6, sz - 6))
            # tick
            pen2 = QPen(QColor("#0d0f14"), 2.2, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
            p.setPen(pen2)
            path = QPainterPath()
            path.moveTo(cx - r * 0.35, cy + 0.05 * r)
            path.lineTo(cx - 0.05 * r, cy + r * 0.38)
            path.lineTo(cx + r * 0.42, cy - r * 0.30)
            p.drawPath(path)

        elif self._error:
            # red X
            p.setPen(Qt.NoPen)
            p.setBrush(QBrush(QColor("#3d1015")))
            p.drawEllipse(QRect(3, 3, sz - 6, sz - 6))
            pen2 = QPen(QColor("#f87171"), 2.2, Qt.SolidLine, Qt.RoundCap)
            p.setPen(pen2)
            d = r * 0.32
            p.drawLine(QPoint(int(cx - d), int(cy - d)), QPoint(int(cx + d), int(cy + d)))
            p.drawLine(QPoint(int(cx + d), int(cy - d)), QPoint(int(cx - d), int(cy + d)))

        elif self._active:
            # animated spinning arc
            pulse_boost = 1 + 0.18 * math.sin(self._pulse * math.pi * 2)
            arc_color = QColor(self._color_hi)
            arc_color.setAlphaF(min(1.0, 0.85 * pulse_boost))

            pen_arc = QPen(arc_color, 2.8, Qt.SolidLine, Qt.RoundCap)
            p.setPen(pen_arc)
            span = int(260 * pulse_boost)
            start = int(-self._angle * 16)
            p.drawArc(QRect(3, 3, sz - 6, sz - 6), start, -span * 16)

            # inner glow dot
            glow = QColor(self._color_hi)
            glow.setAlphaF(0.35 * pulse_boost)
            p.setPen(Qt.NoPen)
            p.setBrush(QBrush(glow))
            p.drawEllipse(QRect(int(cx - 4), int(cy - 4), 8, 8))

        else:
            # idle — faint dot
            p.setPen(Qt.NoPen)
            p.setBrush(QBrush(TEXT_DIM))
            p.drawEllipse(QRect(int(cx - 2), int(cy - 2), 4, 4))

        p.end()


# ─────────────────────────────────────────────────────────────────────────────
# ACTIVITY BAR  — mini waveform bar chart
# ─────────────────────────────────────────────────────────────────────────────
class ActivityBar(QWidget):
    def __init__(self, color, parent=None):
        super().__init__(parent)
        self._color = QColor(color)
        self._bars = [0.0] * 5
        self._phase = 0.0
        self._active = False
        self.setFixedSize(32, 18)

    def set_phase(self, ph, active):
        self._phase = ph
        self._active = active
        if active:
            for i in range(5):
                offset = i * 0.18
                self._bars[i] = 0.25 + 0.75 * abs(math.sin((ph + offset) * math.pi * 2.2))
        else:
            self._bars = [0.12] * 5
        self.update()

    def paintEvent(self, _):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        bar_w = 4
        gap   = 2
        total = 5 * bar_w + 4 * gap
        x0 = (self.width() - total) / 2
        for i, h_frac in enumerate(self._bars):
            h = max(2, int(h_frac * self.height() * 0.88))
            x = x0 + i * (bar_w + gap)
            y = (self.height() - h) / 2
            c = QColor(self._color)
            c.setAlphaF(0.25 + 0.75 * h_frac if self._active else 0.18)
            p.setPen(Qt.NoPen)
            p.setBrush(QBrush(c))
            p.drawRoundedRect(int(x), int(y), bar_w, h, 1.5, 1.5)
        p.end()


# ─────────────────────────────────────────────────────────────────────────────
# PULSE BADGE  — glowing count / label badge
# ─────────────────────────────────────────────────────────────────────────────
class PulseBadge(QWidget):
    def __init__(self, color, parent=None):
        super().__init__(parent)
        self._color = QColor(color)
        self._text = ""
        self._glow = 0.0
        self.setFixedSize(52, 18)

    def set_content(self, text, glow):
        self._text = text
        self._glow = glow
        self.update()

    def paintEvent(self, _):
        if not self._text:
            return
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        w, h = self.width(), self.height()

        # glow halo
        if self._glow > 0:
            glow_c = QColor(self._color)
            glow_c.setAlphaF(0.18 * self._glow)
            p.setPen(Qt.NoPen)
            p.setBrush(QBrush(glow_c))
            p.drawRoundedRect(0, 0, w, h, 5, 5)

        # badge bg
        bg = QColor(self._color)
        bg.setAlphaF(0.13 + 0.12 * self._glow)
        p.setBrush(QBrush(bg))
        border_c = QColor(self._color)
        border_c.setAlphaF(0.4 + 0.4 * self._glow)
        p.setPen(QPen(border_c, 0.8))
        p.drawRoundedRect(1, 1, w - 2, h - 2, 4, 4)

        # text
        font = QFont("Consolas", 8, QFont.Medium)
        p.setFont(font)
        tc = QColor(self._color)
        tc.setAlphaF(0.75 + 0.25 * self._glow)
        p.setPen(tc)
        p.drawText(QRect(0, 0, w, h), Qt.AlignCenter, self._text)
        p.end()


# ─────────────────────────────────────────────────────────────────────────────
# TAB ROW ITEM
# ─────────────────────────────────────────────────────────────────────────────
class TabRow(QWidget):
    clicked = Signal(int)

    def __init__(self, idx, label, color_pair, parent=None):
        super().__init__(parent)
        self._idx = idx
        self._label = label
        self._color_hi = color_pair[0]
        self._color_lo = color_pair[1]
        self._state = "idle"
        self._selected = False
        self._hover = False
        self._anim_angle = 0.0
        self._anim_pulse = 0.0
        self._anim_bar_phase = 0.0
        self._badge_glow = 0.0
        self._elapsed_s = 0

        self.setFixedHeight(54)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setMouseTracking(True)
        self.setCursor(Qt.PointingHandCursor)

        lay = QHBoxLayout(self)
        lay.setContentsMargins(14, 0, 14, 0)
        lay.setSpacing(10)

        # tab number
        self._num_lbl = QLabel(f"{idx + 1:02d}")
        self._num_lbl.setFixedWidth(22)
        fnt_num = QFont("Consolas", 9)
        self._num_lbl.setFont(fnt_num)
        self._num_lbl.setStyleSheet(f"color: {self._color_hi}; opacity: 0.5;")
        lay.addWidget(self._num_lbl)

        # spinner
        self._spinner = ArcSpinner(color_pair, 34)
        lay.addWidget(self._spinner)

        # label + status text
        txt_col = QVBoxLayout()
        txt_col.setSpacing(2)
        fnt_label = QFont("Segoe UI", 10, QFont.Medium)
        self._label_w = QLabel(label)
        self._label_w.setFont(fnt_label)
        self._label_w.setStyleSheet("color: #d4daf0;")
        fnt_sub = QFont("Consolas", 8)
        self._sub_w = QLabel("idle")
        self._sub_w.setFont(fnt_sub)
        self._sub_w.setStyleSheet("color: #4a5068;")
        txt_col.addWidget(self._label_w)
        txt_col.addWidget(self._sub_w)
        lay.addLayout(txt_col, 1)

        # activity bar
        self._bar = ActivityBar(self._color_hi)
        lay.addWidget(self._bar)

        # badge
        self._badge = PulseBadge(self._color_hi)
        lay.addWidget(self._badge)

    # ── state machine
    def set_state(self, state, sub_text=""):
        self._state = state
        self._spinner.set_state(state)

        labels = {
            "idle":    ("idle",    "#4a5068"),
            "running": ("running …", self._color_hi),
            "done":    ("done",    "#34d399"),
            "error":   ("error",   "#f87171"),
        }
        txt, col = labels.get(state, ("idle", "#4a5068"))
        display = sub_text if sub_text else txt
        self._sub_w.setText(display)
        self._sub_w.setStyleSheet(f"color: {col};")

        if state == "running":
            self._badge.set_content("LIVE", 1.0)
        elif state == "done":
            self._badge.set_content("DONE", 0.4)
        elif state == "error":
            self._badge.set_content("ERR", 0.6)
        else:
            self._badge.set_content("", 0)

    def tick(self, dt, phase):
        """Called every animation frame."""
        if self._state == "running":
            self._anim_angle = (self._anim_angle + dt * 280) % 360
            self._anim_pulse = phase
            self._anim_bar_phase = (self._anim_bar_phase + dt * 0.9) % 1.0
            self._badge_glow = abs(math.sin(phase * math.pi * 2))
            self._spinner.set_angle(self._anim_angle)
            self._spinner.set_pulse(self._anim_pulse)
            self._bar.set_phase(self._anim_bar_phase, True)
            self._badge.set_content("LIVE", self._badge_glow)
        else:
            self._bar.set_phase(0, False)

    def set_selected(self, sel):
        self._selected = sel
        self.update()

    # ── paint background
    def paintEvent(self, _):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        w, h = self.width(), self.height()

        if self._selected:
            grad = QLinearGradient(0, 0, w, 0)
            c1 = QColor(self._color_hi)
            c1.setAlphaF(0.10)
            c2 = QColor(self._color_hi)
            c2.setAlphaF(0.0)
            grad.setColorAt(0, c1)
            grad.setColorAt(1, c2)
            p.setPen(Qt.NoPen)
            p.setBrush(QBrush(grad))
            p.drawRect(0, 0, w, h)
            # left accent bar
            bar_c = QColor(self._color_hi)
            p.setBrush(QBrush(bar_c))
            p.drawRoundedRect(0, 8, 3, h - 16, 1.5, 1.5)

        elif self._hover:
            hov = QColor(self._color_hi)
            hov.setAlphaF(0.04)
            p.setPen(Qt.NoPen)
            p.setBrush(QBrush(hov))
            p.drawRect(0, 0, w, h)

        # bottom separator
        p.setPen(QPen(BORDER, 0.5))
        p.drawLine(14, h - 1, w - 14, h - 1)
        p.end()

    def mousePressEvent(self, _):
        self.clicked.emit(self._idx)

    def enterEvent(self, _):
        self._hover = True
        self.update()

    def leaveEvent(self, _):
        self._hover = False
        self.update()


# ─────────────────────────────────────────────────────────────────────────────
# HEADER GLOW BAR
# ─────────────────────────────────────────────────────────────────────────────
class GlowBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(2)
        self._phase = 0.0

    def set_phase(self, ph):
        self._phase = ph
        self.update()

    def paintEvent(self, _):
        p = QPainter(self)
        w, h = self.width(), self.height()
        grad = QLinearGradient(0, 0, w, 0)
        colors = [c[0] for c in TAB_COLORS]
        n = len(colors)
        shift = self._phase
        for i, col in enumerate(colors):
            pos = ((i / n) + shift) % 1.0
            c = QColor(col)
            c.setAlphaF(0.85)
            grad.setColorAt(pos, c)
        p.setPen(Qt.NoPen)
        p.setBrush(QBrush(grad))
        p.drawRect(0, 0, w, h)
        p.end()


# ─────────────────────────────────────────────────────────────────────────────
# DETAIL PANEL  — right side
# ─────────────────────────────────────────────────────────────────────────────
class DetailPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._idx = 0
        self._state = "idle"
        self._phase = 0.0
        self.setMinimumWidth(220)

    def update_state(self, idx, state, phase):
        self._idx = idx
        self._state = state
        self._phase = phase
        self.update()

    def paintEvent(self, _):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        w, h = self.width(), self.height()

        # bg
        p.setPen(Qt.NoPen)
        p.setBrush(QBrush(PANEL_BG))
        p.drawRect(0, 0, w, h)

        color_hi = QColor(TAB_COLORS[self._idx][0])
        color_lo = QColor(TAB_COLORS[self._idx][1])
        label = TAB_LABELS[self._idx]

        # big radial glow behind number
        if self._state == "running":
            alpha = 0.07 + 0.04 * abs(math.sin(self._phase * math.pi * 2))
        else:
            alpha = 0.03

        glow = QRadialGradient(w / 2, h * 0.38, w * 0.55)
        c_glow = QColor(color_hi)
        c_glow.setAlphaF(alpha)
        glow.setColorAt(0, c_glow)
        glow.setColorAt(1, QColor(0, 0, 0, 0))
        p.setBrush(QBrush(glow))
        p.drawRect(0, 0, w, h)

        # big tab number
        fnt_big = QFont("Consolas", 72, QFont.Bold)
        p.setFont(fnt_big)
        nc = QColor(color_hi)
        nc.setAlphaF(0.08 + 0.04 * abs(math.sin(self._phase * math.pi * 2)) if self._state == "running" else 0.05)
        p.setPen(nc)
        p.drawText(QRect(0, int(h * 0.12), w, int(h * 0.5)), Qt.AlignCenter, f"{self._idx + 1:02d}")

        # tab name
        fnt_name = QFont("Segoe UI", 15, QFont.Medium)
        p.setFont(fnt_name)
        p.setPen(TEXT_BRIGHT)
        p.drawText(QRect(0, int(h * 0.38), w, 40), Qt.AlignCenter, label)

        # state pill
        state_labels = {
            "idle": ("IDLE", TEXT_DIM),
            "running": ("● RUNNING", color_hi),
            "done": ("✓ DONE", QColor("#34d399")),
            "error": ("✗ ERROR", QColor("#f87171")),
        }
        stxt, scol = state_labels.get(self._state, ("IDLE", TEXT_DIM))
        fnt_state = QFont("Consolas", 9, QFont.Medium)
        p.setFont(fnt_state)
        p.setPen(scol)
        p.drawText(QRect(0, int(h * 0.52), w, 28), Qt.AlignCenter, stxt)

        # animated arc ring (large)
        if self._state == "running":
            cx, cy = w // 2, int(h * 0.68)
            ring_r = 38
            angle_deg = (self._phase * 360 * 1.7) % 360
            arc_pen = QPen(color_hi, 2.0, Qt.SolidLine, Qt.RoundCap)
            arc_pen.setColor(color_hi)
            p.setPen(arc_pen)
            span = 200
            p.drawArc(
                QRect(cx - ring_r, cy - ring_r, ring_r * 2, ring_r * 2),
                int(-angle_deg * 16), -span * 16
            )
            # counter arc
            c2 = QColor(color_lo)
            c2.setAlphaF(0.4)
            pen2 = QPen(c2, 1.0, Qt.DotLine, Qt.RoundCap)
            p.setPen(pen2)
            p.drawArc(
                QRect(cx - ring_r, cy - ring_r, ring_r * 2, ring_r * 2),
                int(-angle_deg * 16 + 180 * 16), -120 * 16
            )

        # bottom color bar
        bar_h = 3
        grad_b = QLinearGradient(0, 0, w, 0)
        grad_b.setColorAt(0, color_lo)
        grad_b.setColorAt(1, color_hi)
        p.setPen(Qt.NoPen)
        p.setBrush(QBrush(grad_b))
        p.drawRect(0, h - bar_h, w, bar_h)

        p.end()


# ─────────────────────────────────────────────────────────────────────────────
# MAIN WINDOW
# ─────────────────────────────────────────────────────────────────────────────
class KandaTabAnimDemo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kanda Reasoner — Tab Process Animation")
        self.setMinimumSize(720, 560)
        self.resize(820, 620)
        self._phase = 0.0
        self._last_ms = 0
        self._selected = 0
        self._tab_states = ["idle"] * 9
        self._auto_idx = 0
        self._auto_timer_count = 0

        self._build_ui()
        self._build_timers()

    def _build_ui(self):
        root = QWidget()
        self.setCentralWidget(root)
        root.setStyleSheet(f"background: {DARK_BG.name()};")

        outer = QVBoxLayout(root)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        # ── glow bar
        self._glow_bar = GlowBar()
        outer.addWidget(self._glow_bar)

        # ── header
        hdr = QWidget()
        hdr.setFixedHeight(52)
        hdr.setStyleSheet(f"background: {PANEL_BG.name()}; border-bottom: 1px solid {BORDER.name()};")
        hdr_lay = QHBoxLayout(hdr)
        hdr_lay.setContentsMargins(18, 0, 18, 0)
        lbl_title = QLabel("KANDA REASONER")
        fnt_title = QFont("Consolas", 12, QFont.Bold)
        lbl_title.setFont(fnt_title)
        lbl_title.setStyleSheet(f"color: {TEXT_BRIGHT.name()}; letter-spacing: 3px;")
        lbl_sub = QLabel("tab process monitor")
        fnt_sub = QFont("Consolas", 8)
        lbl_sub.setFont(fnt_sub)
        lbl_sub.setStyleSheet("color: #4a5068; letter-spacing: 1px;")
        hdr_lay.addWidget(lbl_title)
        hdr_lay.addSpacing(10)
        hdr_lay.addWidget(lbl_sub)
        hdr_lay.addStretch()

        # control buttons
        for label, slot in [("▶ Start", self._start_selected),
                             ("■ Stop",  self._stop_selected),
                             ("✓ Done",  self._done_selected),
                             ("✗ Error", self._error_selected),
                             ("Auto",    self._toggle_auto)]:
            btn = QPushButton(label)
            btn.setFixedHeight(28)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet("""
                QPushButton {
                    background: #1a1e2a;
                    color: #8892aa;
                    border: 1px solid #1e2330;
                    border-radius: 4px;
                    padding: 0 12px;
                    font-family: Consolas;
                    font-size: 9pt;
                }
                QPushButton:hover {
                    background: #21263a;
                    color: #d4daf0;
                    border-color: #2e3550;
                }
                QPushButton:pressed {
                    background: #181c28;
                }
            """)
            btn.clicked.connect(slot)
            hdr_lay.addWidget(btn)

        outer.addWidget(hdr)

        # ── body: tab list + detail panel
        body = QHBoxLayout()
        body.setContentsMargins(0, 0, 0, 0)
        body.setSpacing(0)

        # tab list
        tab_col = QWidget()
        tab_col.setStyleSheet(f"background: {DARK_BG.name()};")
        tab_col.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        tab_vlay = QVBoxLayout(tab_col)
        tab_vlay.setContentsMargins(0, 0, 0, 0)
        tab_vlay.setSpacing(0)

        self._rows = []
        for i in range(9):
            row = TabRow(i, TAB_LABELS[i], TAB_COLORS[i])
            row.clicked.connect(self._on_tab_clicked)
            tab_vlay.addWidget(row)
            self._rows.append(row)

        tab_vlay.addStretch()

        # status bar at bottom
        status_bar = QWidget()
        status_bar.setFixedHeight(32)
        status_bar.setStyleSheet(f"background: {PANEL_BG.name()}; border-top: 1px solid {BORDER.name()};")
        sb_lay = QHBoxLayout(status_bar)
        sb_lay.setContentsMargins(18, 0, 18, 0)
        self._status_lbl = QLabel("Click a tab row to select · Use buttons to change state · Auto cycles automatically")
        fnt_s = QFont("Consolas", 8)
        self._status_lbl.setFont(fnt_s)
        self._status_lbl.setStyleSheet("color: #4a5068;")
        sb_lay.addWidget(self._status_lbl)
        tab_vlay.addWidget(status_bar)

        body.addWidget(tab_col, 3)

        # separator
        sep = QWidget()
        sep.setFixedWidth(1)
        sep.setStyleSheet(f"background: {BORDER.name()};")
        body.addWidget(sep)

        # detail panel
        self._detail = DetailPanel()
        body.addWidget(self._detail, 1)

        outer.addLayout(body, 1)

        # initial selection
        self._rows[0].set_selected(True)

    def _build_timers(self):
        # animation tick — 30 fps
        self._anim_timer = QTimer(self)
        self._anim_timer.timeout.connect(self._tick)
        self._anim_timer.start(33)

        # auto demo timer
        self._auto_active = False
        self._auto_seq_timer = QTimer(self)
        self._auto_seq_timer.timeout.connect(self._auto_step)

    # ── animation tick
    def _tick(self):
        dt = 0.033
        self._phase = (self._phase + dt * 0.38) % 1.0
        self._glow_bar.set_phase(self._phase)
        for row in self._rows:
            row.tick(dt, self._phase)
        self._detail.update_state(self._selected, self._tab_states[self._selected], self._phase)

    # ── tab selection
    def _on_tab_clicked(self, idx):
        self._rows[self._selected].set_selected(False)
        self._selected = idx
        self._rows[idx].set_selected(True)

    # ── state controls
    def _set_state(self, idx, state, sub=""):
        self._tab_states[idx] = state
        self._rows[idx].set_state(state, sub)

    def _start_selected(self):
        self._set_state(self._selected, "running", "processing …")
        self._status_lbl.setText(f"Tab {self._selected + 1} — {TAB_LABELS[self._selected]}: running")

    def _stop_selected(self):
        self._set_state(self._selected, "idle")
        self._status_lbl.setText(f"Tab {self._selected + 1} — {TAB_LABELS[self._selected]}: stopped")

    def _done_selected(self):
        self._set_state(self._selected, "done", "completed")
        self._status_lbl.setText(f"Tab {self._selected + 1} — {TAB_LABELS[self._selected]}: done ✓")

    def _error_selected(self):
        self._set_state(self._selected, "error", "validation failed")
        self._status_lbl.setText(f"Tab {self._selected + 1} — {TAB_LABELS[self._selected]}: error ✗")

    # ── auto demo
    def _toggle_auto(self):
        self._auto_active = not self._auto_active
        if self._auto_active:
            self._auto_idx = 0
            self._auto_phase = 0
            # reset all
            for i in range(9):
                self._set_state(i, "idle")
            self._auto_seq_timer.start(1400)
            self._status_lbl.setText("Auto demo running — cascading through all tabs …")
        else:
            self._auto_seq_timer.stop()
            self._status_lbl.setText("Auto demo stopped")

    def _auto_step(self):
        n = 9
        # state machine per auto step
        # phase 0: start tab i running
        # phase 1: mark done, start next
        phase = self._auto_phase

        if phase == 0:
            self._on_tab_clicked(self._auto_idx)
            self._set_state(self._auto_idx, "running", "processing …")
            self._auto_phase = 1

        elif phase == 1:
            # sometimes produce error for variety
            if self._auto_idx in (3, 7):
                self._set_state(self._auto_idx, "error", "validation failed")
            else:
                self._set_state(self._auto_idx, "done", "completed")
            self._auto_idx += 1
            self._auto_phase = 0
            if self._auto_idx >= n:
                # restart cycle
                self._auto_idx = 0
                for i in range(n):
                    self._set_state(i, "idle")
                self._status_lbl.setText("Auto demo — new cycle starting …")


# ─────────────────────────────────────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    win = KandaTabAnimDemo()
    win.show()
    sys.exit(app.exec())
