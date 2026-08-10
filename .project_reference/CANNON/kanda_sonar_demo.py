"""
Kanda Reasoner — Sonar Tab Monitor Demo
Military-grade sonar aesthetic: rotating sweep, pulse rings, phosphor glow.

Run:  python kanda_sonar_demo.py
Deps: pip install PySide6
"""

import sys
import math
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QLabel, QPushButton, QSizePolicy,
)
from PySide6.QtCore import Qt, QTimer, QPointF, QRectF
from PySide6.QtGui import (
    QPainter, QColor, QPen, QBrush, QRadialGradient,
    QFont, QPainterPath,
)

# ─────────────────────────────────────────────────────────────────────────────
# PHOSPHOR PALETTE  — classic green CRT sonar
# ─────────────────────────────────────────────────────────────────────────────
BG          = QColor("#040a06")
PHGR_BRIGHT = QColor("#00ff88")   # hot phosphor
PHGR_MID    = QColor("#00cc66")   # mid glow
PHGR_DIM    = QColor("#00441e")   # decayed trace
PHGR_GHOST  = QColor("#001a0c")   # faintest ring
GRID_LINE   = QColor("#003318")
TEXT_LO     = QColor("#004a22")
TEXT_HI     = QColor("#00cc66")
SWEEP_HEAD  = QColor("#aaffcc")
AMBER_HIT   = QColor("#ffcc44")   # contact blip
RED_HIT     = QColor("#ff4444")   # error blip

TAB_LABELS = [
    "Collector", "Parser", "Manual Review",
    "ZIP Export", "Evidence", "Reasoner",
    "Ollama", "Atlas", "Prompts",
]
N_TABS = 9

# angles where tab blips live — evenly spaced on the dial
TAB_ANGLES = [i * (360 / N_TABS) for i in range(N_TABS)]
# radii for each tab blip (slightly varied for depth)
TAB_RADII  = [0.55, 0.68, 0.48, 0.72, 0.61, 0.79, 0.44, 0.65, 0.58]

STATES = ["idle", "running", "done", "error"]


# ─────────────────────────────────────────────────────────────────────────────
# CONTACT BLIP  — a detected contact on the scope
# ─────────────────────────────────────────────────────────────────────────────
class Blip:
    def __init__(self, angle_deg, radius_frac, label, idx):
        self.angle  = angle_deg
        self.radius = radius_frac
        self.label  = label
        self.idx    = idx
        self.state  = "idle"
        self.brightness = 0.0   # 0..1, decays over time
        self.last_sweep = -999.0

    def hit_by_sweep(self, sweep_angle):
        """Returns True when the sweep pointer passes over this blip."""
        diff = (sweep_angle - self.angle) % 360
        return diff < 6.0   # within 6° arc of sweep head

    def decay(self, dt):
        self.brightness = max(0.0, self.brightness - dt * 0.35)

    def energise(self):
        self.brightness = 1.0


# ─────────────────────────────────────────────────────────────────────────────
# SONAR SCOPE WIDGET
# ─────────────────────────────────────────────────────────────────────────────
class SonarScope(QWidget):
    """The main circular sonar display."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._sweep_angle = 0.0        # degrees, clockwise from 12-o'clock
        self._sweep_speed = 22.0       # degrees per second
        self._blips: list[Blip] = []
        self._selected = -1
        self._pulse_rings: list[dict] = []  # active outward pulse rings
        self._trail_segments = []      # list of (angle, alpha) for sweep trail
        self._time = 0.0
        self.setMinimumSize(440, 440)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setCursor(Qt.CrossCursor)

    def add_blip(self, blip: Blip):
        self._blips.append(blip)

    def set_selected(self, idx):
        self._selected = idx
        self.update()

    def set_state(self, idx, state):
        for b in self._blips:
            if b.idx == idx:
                b.state = state
                if state == "running":
                    # emit a pulse ring from that blip
                    angle_rad = math.radians(b.angle - 90)
                    cx = 0.5 + b.radius * 0.5 * math.cos(angle_rad)
                    cy = 0.5 + b.radius * 0.5 * math.sin(angle_rad)
                    self._pulse_rings.append({
                        "cx": cx, "cy": cy, "r": 0.02, "alpha": 1.0,
                        "color": "green",
                    })
                break
        self.update()

    def tick(self, dt):
        self._time += dt
        old_angle = self._sweep_angle

        # advance sweep
        self._sweep_angle = (self._sweep_angle + self._sweep_speed * dt) % 360

        # check blips
        for b in self._blips:
            # did the sweep cross this blip?
            prev = old_angle
            curr = self._sweep_angle
            # handle wrap-around
            b_a = b.angle
            crossed = False
            if curr >= prev:
                crossed = prev <= b_a < curr
            else:
                crossed = b_a >= prev or b_a < curr
            if crossed:
                b.energise()
                b.last_sweep = self._time
            else:
                b.decay(dt)

        # decay pulse rings
        for ring in self._pulse_rings:
            ring["r"] += dt * 0.18
            ring["alpha"] -= dt * 0.9
        self._pulse_rings = [r for r in self._pulse_rings if r["alpha"] > 0]

        self.update()

    # ── coordinate helpers
    def _centre(self):
        w, h = self.width(), self.height()
        return QPointF(w / 2, h / 2)

    def _radius(self):
        return min(self.width(), self.height()) / 2 - 12

    def _polar_to_xy(self, angle_deg, radius_frac):
        """Convert (angle from north, 0..1 fraction of scope radius) → QPointF."""
        c = self._centre()
        R = self._radius()
        a = math.radians(angle_deg - 90)
        x = c.x() + radius_frac * R * math.cos(a)
        y = c.y() + radius_frac * R * math.sin(a)
        return QPointF(x, y)

    # ── paint
    def paintEvent(self, _):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        self._draw_bg(p)
        self._draw_grid(p)
        self._draw_sweep_trail(p)
        self._draw_sweep_line(p)
        self._draw_pulse_rings(p)
        self._draw_blips(p)
        self._draw_overlay(p)
        self._draw_bezel(p)
        p.end()

    def _draw_bg(self, p: QPainter):
        c = self._centre()
        R = self._radius()
        # deep radial gradient background
        grad = QRadialGradient(c, R)
        grad.setColorAt(0.0, QColor("#051209"))
        grad.setColorAt(0.7, QColor("#030a05"))
        grad.setColorAt(1.0, QColor("#020705"))
        p.setPen(Qt.NoPen)
        p.setBrush(QBrush(grad))
        p.drawEllipse(c, R, R)

    def _draw_grid(self, p: QPainter):
        c = self._centre()
        R = self._radius()
        pen = QPen(GRID_LINE, 0.6)
        p.setPen(pen)

        # range rings
        for frac in [0.25, 0.50, 0.75, 1.0]:
            r = R * frac
            p.drawEllipse(c, r, r)

        # bearing lines every 30°
        for deg in range(0, 360, 30):
            a = math.radians(deg - 90)
            x1 = c.x() + 0.0 * math.cos(a)
            y1 = c.y() + 0.0 * math.sin(a)
            x2 = c.x() + R * math.cos(a)
            y2 = c.y() + R * math.sin(a)
            p.drawLine(QPointF(x1, y1), QPointF(x2, y2))

        # bearing labels
        fnt = QFont("Consolas", 8)
        p.setFont(fnt)
        p.setPen(TEXT_LO)
        for deg in range(0, 360, 30):
            pt = self._polar_to_xy(deg, 1.10)
            label = f"{deg:03d}"
            p.drawText(QRectF(pt.x() - 16, pt.y() - 7, 32, 14),
                       Qt.AlignCenter, label)

        # centre cross
        p.setPen(QPen(PHGR_DIM, 0.8))
        s = 5
        p.drawLine(QPointF(c.x() - s, c.y()), QPointF(c.x() + s, c.y()))
        p.drawLine(QPointF(c.x(), c.y() - s), QPointF(c.x(), c.y() + s))

    def _draw_sweep_trail(self, p: QPainter):
        """Fill the swept arc behind the pointer with a fading phosphor glow."""
        c  = self._centre()
        R  = self._radius()
        sw = self._sweep_angle

        # we draw 120° trail behind the sweep head
        TRAIL_DEG = 120
        STEPS     = 48

        for i in range(STEPS):
            frac   = i / STEPS            # 0 = oldest, 1 = newest
            offset = (1.0 - frac) * TRAIL_DEG
            a_deg  = (sw - offset) % 360
            a_rad  = math.radians(a_deg - 90)
            a_next = math.radians(a_deg - 90 + (TRAIL_DEG / STEPS))

            alpha = frac * 0.22           # fades to transparent at tail
            c_glow = QColor(PHGR_MID)
            c_glow.setAlphaF(alpha)

            path = QPainterPath()
            path.moveTo(c)
            path.arcTo(QRectF(c.x() - R, c.y() - R, R * 2, R * 2),
                       -math.degrees(a_rad),
                       -(TRAIL_DEG / STEPS))
            path.lineTo(c)
            p.setPen(Qt.NoPen)
            p.setBrush(QBrush(c_glow))
            p.drawPath(path)

    def _draw_sweep_line(self, p: QPainter):
        """The bright rotating sweep arm."""
        c  = self._centre()
        R  = self._radius()
        a  = math.radians(self._sweep_angle - 90)
        tip = QPointF(c.x() + R * math.cos(a), c.y() + R * math.sin(a))

        # glow layer
        for width, alpha in [(8, 0.06), (4, 0.14), (1.5, 0.90)]:
            glow = QColor(PHGR_BRIGHT if width == 1.5 else SWEEP_HEAD)
            glow.setAlphaF(alpha)
            p.setPen(QPen(glow, width, Qt.SolidLine, Qt.RoundCap))
            p.drawLine(c, tip)

        # bright tip dot
        tip_c = QColor(SWEEP_HEAD)
        tip_c.setAlphaF(0.95)
        p.setPen(Qt.NoPen)
        p.setBrush(QBrush(tip_c))
        p.drawEllipse(tip, 3.5, 3.5)

    def _draw_pulse_rings(self, p: QPainter):
        c = self._centre()
        R = self._radius()
        for ring in self._pulse_rings:
            cx = c.x() + (ring["cx"] - 0.5) * R * 2
            cy = c.y() + (ring["cy"] - 0.5) * R * 2
            r  = ring["r"] * R * 2
            col = QColor(PHGR_BRIGHT)
            col.setAlphaF(ring["alpha"] * 0.7)
            p.setPen(QPen(col, 1.0))
            p.setBrush(Qt.NoBrush)
            p.drawEllipse(QPointF(cx, cy), r, r)

    def _draw_blips(self, p: QPainter):
        for b in self._blips:
            pt = self._polar_to_xy(b.angle, b.radius)
            br = b.brightness
            sel = (b.idx == self._selected)

            # pick color by state
            if b.state == "error":
                base_c = RED_HIT
            elif b.state == "done":
                base_c = PHGR_BRIGHT
            elif b.state == "running":
                base_c = AMBER_HIT
            else:
                base_c = PHGR_MID

            # glow halo
            if br > 0.05 or sel:
                halo_r = 18 + (6 if sel else 0)
                glow = QRadialGradient(pt, halo_r)
                c1 = QColor(base_c)
                c1.setAlphaF(min(1.0, br * 0.45 + (0.2 if sel else 0)))
                c2 = QColor(base_c)
                c2.setAlphaF(0)
                glow.setColorAt(0, c1)
                glow.setColorAt(1, c2)
                p.setPen(Qt.NoPen)
                p.setBrush(QBrush(glow))
                p.drawEllipse(pt, halo_r, halo_r)

            # core blip dot
            dot_r = 4.5 if sel else 3.5
            dot_c = QColor(base_c)
            dot_c.setAlphaF(max(0.2, br * 0.8 + (0.5 if sel else 0)))
            p.setBrush(QBrush(dot_c))
            p.setPen(Qt.NoPen)
            p.drawEllipse(pt, dot_r, dot_r)

            # label
            label_alpha = max(0.15, br * 0.75 + (0.6 if sel else 0))
            lc = QColor(base_c)
            lc.setAlphaF(label_alpha)
            p.setPen(lc)
            fnt = QFont("Consolas", 7 if not sel else 8,
                        QFont.Bold if sel else QFont.Normal)
            p.setFont(fnt)
            # offset label to avoid cluttering the dot
            a_rad = math.radians(b.angle - 90)
            ox = 12 * math.cos(a_rad)
            oy = 12 * math.sin(a_rad)
            p.drawText(
                QRectF(pt.x() + ox - 36, pt.y() + oy - 8, 72, 14),
                Qt.AlignCenter,
                b.label,
            )

            # running indicator: tiny pulsing ring
            if b.state == "running":
                t = self._time
                pulse_r = 6 + 3 * abs(math.sin(t * 3.5))
                rc = QColor(AMBER_HIT)
                rc.setAlphaF(0.5 * abs(math.sin(t * 3.5)))
                p.setPen(QPen(rc, 1.0))
                p.setBrush(Qt.NoBrush)
                p.drawEllipse(pt, pulse_r, pulse_r)

    def _draw_overlay(self, p: QPainter):
        """HUD data overlay — top-left corner readouts."""
        c  = self._centre()
        R  = self._radius()
        fnt_sm = QFont("Consolas", 8)
        fnt_md = QFont("Consolas", 9, QFont.Bold)
        p.setFont(fnt_sm)

        # bearing readout
        bearing = int(self._sweep_angle) % 360
        p.setPen(TEXT_HI)
        p.setFont(fnt_md)
        p.drawText(
            QRectF(c.x() - R, c.y() - R + 6, R * 2, 20),
            Qt.AlignCenter,
            f"BRG  {bearing:03d}°",
        )

        # range rings legend (bottom)
        p.setFont(fnt_sm)
        p.setPen(TEXT_LO)
        for i, label in enumerate(["25%", "50%", "75%", "100%"]):
            pt = self._polar_to_xy(180, (i + 1) * 0.25)
            p.drawText(
                QRectF(pt.x() + 4, pt.y() - 6, 28, 12),
                Qt.AlignLeft | Qt.AlignVCenter,
                label,
            )

    def _draw_bezel(self, p: QPainter):
        """Outer bezel ring."""
        c = self._centre()
        R = self._radius()
        pen = QPen(PHGR_DIM, 1.5)
        p.setPen(pen)
        p.setBrush(Qt.NoBrush)
        p.drawEllipse(c, R, R)

        # tick marks every 5°
        for deg in range(0, 360, 5):
            a = math.radians(deg - 90)
            inner = R - (5 if deg % 30 == 0 else 3)
            outer = R + 0
            x1 = c.x() + inner * math.cos(a)
            y1 = c.y() + inner * math.sin(a)
            x2 = c.x() + outer * math.cos(a)
            y2 = c.y() + outer * math.sin(a)
            col = PHGR_MID if deg % 30 == 0 else PHGR_DIM
            p.setPen(QPen(col, 0.8))
            p.drawLine(QPointF(x1, y1), QPointF(x2, y2))

    def mousePressEvent(self, event):
        """Click to select nearest blip."""
        pos = QPointF(event.position())
        c   = self._centre()
        R   = self._radius()
        best_idx  = -1
        best_dist = 999
        for b in self._blips:
            pt   = self._polar_to_xy(b.angle, b.radius)
            dist = math.hypot(pos.x() - pt.x(), pos.y() - pt.y())
            if dist < best_dist and dist < 28:
                best_dist = dist
                best_idx  = b.idx
        if best_idx >= 0:
            self._selected = best_idx
            self.update()


# ─────────────────────────────────────────────────────────────────────────────
# CONTACT LIST  — sidebar with tab status
# ─────────────────────────────────────────────────────────────────────────────
class ContactList(QWidget):
    def __init__(self, blips: list[Blip], parent=None):
        super().__init__(parent)
        self._blips = blips
        self._selected = -1
        self.setFixedWidth(180)
        self.setMinimumHeight(440)

    def set_selected(self, idx):
        self._selected = idx
        self.update()

    def paintEvent(self, _):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        w, h = self.width(), self.height()

        # dark bg
        p.fillRect(0, 0, w, h, QColor("#030b05"))

        # header
        fnt_hdr = QFont("Consolas", 8, QFont.Bold)
        p.setFont(fnt_hdr)
        p.setPen(PHGR_DIM)
        p.drawText(QRectF(0, 6, w, 16), Qt.AlignCenter, "CONTACT LIST")

        p.setPen(QPen(GRID_LINE, 0.5))
        p.drawLine(8, 26, w - 8, 26)

        # rows
        row_h = 38
        y0 = 32
        fnt_lbl = QFont("Consolas", 8, QFont.Bold)
        fnt_sub = QFont("Consolas", 7)

        state_symbols = {
            "idle":    ("●", TEXT_LO),
            "running": ("◎", AMBER_HIT),
            "done":    ("✓", PHGR_BRIGHT),
            "error":   ("✗", RED_HIT),
        }

        for b in self._blips:
            y = y0 + b.idx * row_h
            sel = (b.idx == self._selected)

            if sel:
                sel_c = QColor(PHGR_GHOST)
                p.fillRect(0, y, w, row_h, sel_c)
                p.setPen(QPen(PHGR_DIM, 0.5))
                p.drawLine(0, y, 0, y + row_h)

            sym, sym_c = state_symbols.get(b.state, ("●", TEXT_LO))

            # status symbol
            p.setFont(fnt_lbl)
            p.setPen(sym_c)
            p.drawText(QRectF(6, y + 4, 14, 16), Qt.AlignCenter, sym)

            # tab index
            p.setPen(TEXT_LO if not sel else TEXT_HI)
            p.setFont(fnt_sub)
            p.drawText(QRectF(6, y + 20, 14, 12), Qt.AlignCenter, f"T{b.idx + 1}")

            # label
            p.setPen(TEXT_HI if sel else PHGR_MID)
            p.setFont(fnt_lbl)
            p.drawText(QRectF(22, y + 4, w - 28, 16), Qt.AlignLeft | Qt.AlignVCenter, b.label)

            # state text
            p.setFont(fnt_sub)
            sc = sym_c
            sc_fade = QColor(sc)
            sc_fade.setAlphaF(0.65)
            p.setPen(sc_fade)
            p.drawText(QRectF(22, y + 20, w - 28, 12), Qt.AlignLeft | Qt.AlignVCenter, b.state.upper())

            # separator
            p.setPen(QPen(GRID_LINE, 0.4))
            p.drawLine(4, y + row_h - 1, w - 4, y + row_h - 1)

        p.end()


# ─────────────────────────────────────────────────────────────────────────────
# MAIN WINDOW
# ─────────────────────────────────────────────────────────────────────────────
class KandaSonarDemo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kanda Reasoner — Sonar Monitor")
        self.resize(740, 560)
        self.setMinimumSize(680, 520)

        self._selected = 0
        self._auto_active = False
        self._auto_idx = 0
        self._auto_phase = 0

        self._blips = []
        for i in range(N_TABS):
            b = Blip(TAB_ANGLES[i], TAB_RADII[i], TAB_LABELS[i], i)
            self._blips.append(b)

        self._build_ui()
        self._build_timers()

        # initial selection
        self._select(0)

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        central.setStyleSheet("background: #020704;")

        main_lay = QVBoxLayout(central)
        main_lay.setContentsMargins(0, 0, 0, 0)
        main_lay.setSpacing(0)

        # ── header bar
        hdr = QWidget()
        hdr.setFixedHeight(44)
        hdr.setStyleSheet("background: #030a05; border-bottom: 1px solid #003318;")
        hdr_lay = QHBoxLayout(hdr)
        hdr_lay.setContentsMargins(16, 0, 16, 0)
        hdr_lay.setSpacing(10)

        title = QLabel("◉  KANDA SONAR — PROCESS MONITOR")
        fnt_t = QFont("Consolas", 10, QFont.Bold)
        title.setFont(fnt_t)
        title.setStyleSheet("color: #00aa55; letter-spacing: 2px;")
        hdr_lay.addWidget(title)
        hdr_lay.addStretch()

        btn_style = """
            QPushButton {
                background: #030f06;
                color: #007733;
                border: 1px solid #003318;
                border-radius: 3px;
                padding: 0 10px;
                font-family: Consolas;
                font-size: 8pt;
                min-height: 24px;
            }
            QPushButton:hover {
                background: #041508;
                color: #00cc55;
                border-color: #005522;
            }
            QPushButton:pressed { background: #020b04; }
        """
        for lbl, slot in [
            ("▶ RUN",    self._run_selected),
            ("■ STOP",   self._stop_selected),
            ("✓ DONE",   self._done_selected),
            ("✗ ERROR",  self._error_selected),
            ("AUTO",     self._toggle_auto),
            ("+ SPEED",  self._speed_up),
            ("− SPEED",  self._speed_down),
        ]:
            btn = QPushButton(lbl)
            btn.setStyleSheet(btn_style)
            btn.clicked.connect(slot)
            hdr_lay.addWidget(btn)

        main_lay.addWidget(hdr)

        # ── body
        body = QHBoxLayout()
        body.setContentsMargins(0, 0, 0, 0)
        body.setSpacing(0)

        # sonar scope
        self._scope = SonarScope()
        for b in self._blips:
            self._scope.add_blip(b)
        self._scope.set_selected(self._selected)
        body.addWidget(self._scope, 1)

        # separator
        sep = QWidget()
        sep.setFixedWidth(1)
        sep.setStyleSheet("background: #003318;")
        body.addWidget(sep)

        # contact list
        self._contact_list = ContactList(self._blips)
        body.addWidget(self._contact_list)

        main_lay.addLayout(body, 1)

        # ── status bar
        status_bar = QWidget()
        status_bar.setFixedHeight(28)
        status_bar.setStyleSheet("background: #030a05; border-top: 1px solid #003318;")
        sb_lay = QHBoxLayout(status_bar)
        sb_lay.setContentsMargins(16, 0, 16, 0)
        self._status_lbl = QLabel("Click a contact on scope or list · Use buttons to set state · AUTO cascades all tabs")
        fnt_s = QFont("Consolas", 7)
        self._status_lbl.setFont(fnt_s)
        self._status_lbl.setStyleSheet("color: #004422;")
        sb_lay.addWidget(self._status_lbl)
        main_lay.addWidget(status_bar)

    def _build_timers(self):
        # ~40 fps animation
        self._anim_timer = QTimer(self)
        self._anim_timer.timeout.connect(self._tick)
        self._anim_timer.start(25)

        # auto-cycle
        self._auto_timer = QTimer(self)
        self._auto_timer.timeout.connect(self._auto_step)

    def _tick(self):
        dt = 0.025
        self._scope.tick(dt)
        # keep contact list in sync
        self._contact_list.update()

    # ── selection
    def _select(self, idx):
        self._selected = idx
        self._scope.set_selected(idx)
        self._contact_list.set_selected(idx)

    # ── state controls
    def _set_state(self, idx, state):
        self._blips[idx].state = state
        self._scope.set_state(idx, state)
        self._contact_list.update()
        tab = TAB_LABELS[idx]
        self._status_lbl.setText(f"T{idx+1} {tab}: {state.upper()}")

    def _run_selected(self):    self._set_state(self._selected, "running")
    def _stop_selected(self):   self._set_state(self._selected, "idle")
    def _done_selected(self):   self._set_state(self._selected, "done")
    def _error_selected(self):  self._set_state(self._selected, "error")

    def _speed_up(self):
        self._scope._sweep_speed = min(90, self._scope._sweep_speed + 8)
        self._status_lbl.setText(f"Sweep speed: {self._scope._sweep_speed:.0f}°/s")

    def _speed_down(self):
        self._scope._sweep_speed = max(6, self._scope._sweep_speed - 8)
        self._status_lbl.setText(f"Sweep speed: {self._scope._sweep_speed:.0f}°/s")

    # ── auto cascade
    def _toggle_auto(self):
        self._auto_active = not self._auto_active
        if self._auto_active:
            self._auto_idx   = 0
            self._auto_phase = 0
            for b in self._blips:
                b.state = "idle"
            self._auto_timer.start(900)
            self._status_lbl.setText("AUTO mode — cascading contacts …")
        else:
            self._auto_timer.stop()
            self._status_lbl.setText("AUTO stopped")

    def _auto_step(self):
        n = N_TABS
        ph = self._auto_phase
        idx = self._auto_idx

        if ph == 0:
            self._select(idx)
            self._set_state(idx, "running")
            self._auto_phase = 1
        elif ph == 1:
            # occasional error for realism
            state = "error" if idx in (3, 6) else "done"
            self._set_state(idx, state)
            self._auto_idx += 1
            self._auto_phase = 0
            if self._auto_idx >= n:
                self._auto_idx = 0
                for b in self._blips:
                    b.state = "idle"
                self._status_lbl.setText("AUTO — new sweep cycle …")


# ─────────────────────────────────────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    win = KandaSonarDemo()
    win.show()
    sys.exit(app.exec())
