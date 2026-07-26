# project-path: kanda_reasoner_app/local_ai_runtime_state.py
"""Qt-free immutable Local AI runtime state shared by request infrastructure."""

from __future__ import annotations

from dataclasses import dataclass

__all__ = [
    "LocalAIConfigurationSnapshot",
    "publish_runtime_local_ai_configuration_snapshot",
    "runtime_local_ai_configuration_snapshot",
]


@dataclass(frozen=True, slots=True, kw_only=True)
class LocalAIConfigurationSnapshot:
    """Carry one non-Project endpoint/model revision into a Local AI request."""

    revision: str
    base_url: str
    model_id: str
    catalog_status: str
    catalog_timestamp: str
    available_models: tuple[str, ...]
    ready_for_chat: bool


_RUNTIME_SNAPSHOT: LocalAIConfigurationSnapshot | None = None


def publish_runtime_local_ai_configuration_snapshot(
    snapshot: LocalAIConfigurationSnapshot,
) -> None:
    """Publish one immutable snapshot without importing Qt or Project state."""
    global _RUNTIME_SNAPSHOT
    _RUNTIME_SNAPSHOT = snapshot


def runtime_local_ai_configuration_snapshot() -> LocalAIConfigurationSnapshot | None:
    """Return the latest immutable runtime snapshot."""
    return _RUNTIME_SNAPSHOT
