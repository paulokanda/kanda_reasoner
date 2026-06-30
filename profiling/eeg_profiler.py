# project-path: profiling/eeg_profiler.py
"""Support profiling workflows for developer tooling."""

import time
import psutil
import threading
from collections import deque
from statistics import mean
from importlib import import_module as _qtcore_import_module


def _qt_core_attr(name: str):
    """Return a PySide6.QtCore attribute without a static QtCore import."""
    return getattr(_qtcore_import_module("PySide6.QtCore"), name)

from PySide6.QtWidgets import QLabel

class RealTimePerformanceProfiler:
    """Represent real time performance profiler."""
    
    def __init__(self, max_samples=60, interval_ms=1000, overlay_widget=None):
        """Support init behavior.
        
        Parameters
        ----------
        max_samples : object, optional
            The optional max samples value.
        interval_ms : object, optional
            The optional interval ms value.
        overlay_widget : object, optional
            The optional overlay widget value.
        """
        
        self.durations = deque(maxlen=max_samples)
        self.process = psutil.Process()
        self.last_time = None
        self.overlay = overlay_widget
        self.last_memory = 0

        self.timer = _qt_core_attr("QTimer")()
        self.timer.timeout.connect(self._report)
        self.timer.start(interval_ms)

    def before_render(self):
        """Support before render behavior.
        """
        
        self.last_time = time.perf_counter()

    def after_render(self):
        """Support after render behavior.
        """
        
        if self.last_time is None:
            return
        now = time.perf_counter()
        self.durations.append(now - self.last_time)
        self.last_time = None

    def _report(self):
        """Support report behavior.
        """
        
        if not self.durations:
            return

        fps = 1.0 / mean(self.durations)
        memory = self.process.memory_info().rss / (1024 ** 2)
        self.last_memory = memory

        text = f"[Profiler] FPS: {fps:.1f} | Memory: {memory:.1f} MB"

        print(text)
        if self.overlay:
            self.overlay.setText(text)

    def attach_overlay(self, parent):
        """Support attach overlay behavior.
        
        Parameters
        ----------
        parent : object
            The parent value.
        """
        
        if self.overlay is None:
            self.overlay = QLabel(parent)
            self.overlay.setStyleSheet("color: lime; background: black; padding: 5px;")
            self.overlay.move(10, 10)
            self.overlay.show()

