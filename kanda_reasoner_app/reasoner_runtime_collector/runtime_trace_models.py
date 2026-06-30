# project-path: kanda_reasoner_app/reasoner_runtime_collector/runtime_trace_models.py
"""Support runtime evidence collection for Project Reasoner."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class TraceEvent:
    """Represent trace event."""
    
    event_id: int
    time: str
    event_type: str
    source_file: str
    source_symbol: str
    message: str = ""
    object_name: str = ""
    object_type: str = ""
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass
class TraceStateSnapshot:
    """Represent trace state snapshot."""
    
    snapshot_id: int
    time: str
    label: str
    state: dict[str, Any] = field(default_factory=dict)


@dataclass
class TraceIssue:
    """Represent trace issue."""
    
    issue_id: int
    time: str
    source_file: str
    source_symbol: str
    message: str
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass
class TraceSignalConnection:
    """Represent trace signal connection."""
    
    connection_id: int
    time: str
    sender_type: str
    sender_name: str
    signal_name: str
    receiver_type: str
    receiver_name: str
    slot_name: str
    source_file: str = ""
    source_line: int | None = None
    extra: dict[str, Any] = field(default_factory=dict)
