# project-path: kanda_reasoner_app/manage_architecture/warning_heuristic_resolver_sonar.py
"""Green sonar projection for Warning Heuristic Resolver progress."""

from __future__ import annotations

from typing import Any

from kanda_reasoner_app.templates.green_sonar_monitor import (
    GreenSonarActivityMonitor,
)

__all__ = [
    "finish_warning_resolver_sonar_error",
    "finish_warning_resolver_sonar_success",
    "start_warning_resolver_sonar",
    "update_warning_resolver_sonar",
]

_MONITOR_OBJECT_NAME = "warningHeuristicResolverSonarMonitor"


def start_warning_resolver_sonar(window: Any, total: int) -> None:
    """Start animated resolver feedback with deterministic counters."""
    monitor = _monitor(window)
    if monitor is None:
        return
    monitor.start(
        "Resolver running",
        (
            f"Resolver: total {total} | to go {total}",
            "done 0 | Web AI 0 (AI necessary)",
            "Preparing TEST_PROTECTION_GAP evidence",
        ),
    )


def update_warning_resolver_sonar(
    window: Any,
    total: int,
    to_go: int,
    done: int,
    web_ai: int,
    source_path: str,
    action: str,
) -> None:
    """Project real worker progress into the reusable sonar animation."""
    monitor = _monitor(window)
    if monitor is None:
        return
    current = _current_line(source_path, action)
    monitor.start(
        "Resolver running",
        (
            f"Resolver: total {total} | to go {to_go}",
            f"done {done} | Web AI {web_ai} (AI necessary)",
            current,
        ),
    )


def finish_warning_resolver_sonar_success(
    window: Any,
    *,
    total: int,
    done: int,
    web_ai: int,
) -> None:
    """Settle sonar after one completed specialist plan."""
    monitor = _monitor(window)
    if monitor is None:
        return
    monitor.finish_success(
        "Resolver complete",
        (
            f"Resolver: total {total} | to go 0",
            f"done {done} | Web AI {web_ai} (AI necessary)",
            "Review safe links before any confirmed write",
        ),
    )


def finish_warning_resolver_sonar_error(window: Any, message: str) -> None:
    """Settle sonar after one worker failure."""
    monitor = _monitor(window)
    if monitor is None:
        return
    monitor.finish_error(
        "Resolver stopped",
        (
            "No correction plan was accepted",
            "Web AI counters are not final",
            _single_line(message, "Resolver worker failed"),
        ),
    )


def _monitor(window: Any) -> GreenSonarActivityMonitor | None:
    finder = getattr(window, "findChild", None)
    monitor = None
    if callable(finder):
        monitor = finder(GreenSonarActivityMonitor, _MONITOR_OBJECT_NAME)
    if monitor is not None:
        return monitor
    try:
        monitor = GreenSonarActivityMonitor(
            window,
            title="Warning Heuristic Resolver",
        )
    except (RuntimeError, TypeError):
        return None
    monitor.setObjectName(_MONITOR_OBJECT_NAME)
    return monitor


def _current_line(source_path: str, action: str) -> str:
    compact = str(source_path or "starting").replace("\\", "/")
    if len(compact) > 92:
        compact = ".../" + compact[-88:]
    if str(action) == "web_ai":
        return "AI necessary: " + compact
    if str(action) == "starting":
        return "Indexing existing tests"
    return "Resolved locally: " + compact


def _single_line(message: str, fallback: str) -> str:
    lines = str(message or "").strip().splitlines()
    return lines[0][:120] if lines else fallback
