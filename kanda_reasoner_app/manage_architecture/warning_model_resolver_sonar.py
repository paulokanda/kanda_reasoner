# project-path: kanda_reasoner_app/manage_architecture/warning_model_resolver_sonar.py
"""Green sonar projection for Warning Local AI Resolver progress."""

from __future__ import annotations

from typing import Any

from kanda_reasoner_app.templates.green_sonar_monitor import GreenSonarActivityMonitor

__all__ = [
    "finish_warning_model_sonar_error",
    "finish_warning_model_sonar_success",
    "start_warning_model_sonar",
    "update_warning_model_sonar",
]

_MONITOR_OBJECT_NAME = "warningLocalAIResolverSonarMonitor"


def start_warning_model_sonar(window: Any, total: int, model_name: str) -> None:
    monitor = _monitor(window)
    if monitor is None:
        return
    monitor.start(
        "Local AI Resolver running",
        (
            f"Resolver: total {total} | to go {total}",
            "done 0 | Web AI 0 (AI necessary)",
            "Ollama: " + (model_name or "Auto selection from top model dropdown"),
        ),
    )


def update_warning_model_sonar(
    window: Any,
    total: int,
    to_go: int,
    done: int,
    web_ai: int,
    source_path: str,
    action: str,
) -> None:
    monitor = _monitor(window)
    if monitor is None:
        return
    compact = str(source_path or "starting").replace("\\", "/")
    if len(compact) > 92:
        compact = ".../" + compact[-88:]
    labels = {
        "web_ai": "Web AI necessary",
        "local_ai_reviewing": "Local AI reviewing",
        "sandbox_pytest": "Disposable project pytest",
        "sandbox_audit": "Disposable Architecture Review",
        "sandbox_validating": "Disposable project validating",
        "model_test_change": "Validated Local AI test change",
    }
    current = labels.get(action, "Resolved") + ": " + compact
    monitor.start(
        "Local AI Resolver running",
        (
            f"Resolver: total {total} | to go {to_go}",
            f"done {done} | Web AI {web_ai} (AI necessary)",
            current,
        ),
    )


def finish_warning_model_sonar_success(
    window: Any,
    *,
    total: int,
    done: int,
    web_ai: int,
    model_name: str,
) -> None:
    monitor = _monitor(window)
    if monitor is None:
        return
    monitor.finish_success(
        "Local AI Resolver complete",
        (
            f"Resolver: total {total} | to go 0",
            f"done {done} | Web AI {web_ai} (AI necessary)",
            "Ollama model: " + model_name,
        ),
    )


def finish_warning_model_sonar_error(window: Any, message: str) -> None:
    monitor = _monitor(window)
    if monitor is None:
        return
    first_line = str(message or "Local AI resolver failed").strip().splitlines()[0][:120]
    monitor.finish_error(
        "Local AI Resolver stopped",
        (
            "No Local AI correction plan was accepted",
            "Web AI counters are not final",
            first_line,
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
        monitor = GreenSonarActivityMonitor(window, title="Warning Local AI Resolver")
    except (RuntimeError, TypeError):
        return None
    monitor.setObjectName(_MONITOR_OBJECT_NAME)
    return monitor
