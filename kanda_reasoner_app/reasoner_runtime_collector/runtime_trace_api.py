# project-path: kanda_reasoner_app/reasoner_runtime_collector/runtime_trace_api.py
"""Support runtime evidence collection for Project Reasoner."""

from __future__ import annotations

__all__ = [
    "configure_runtime_trace",
    "get_runtime_trace_writer",
    "is_runtime_trace_configured",
    "reset_runtime_trace",
    "save_runtime_trace",
    "trace_error",
    "trace_event",
    "trace_signal_connection",
    "trace_state_snapshot",
]

from pathlib import Path
from typing import Any

from .runtime_trace_writer import RuntimeTraceWriter

_TRACE_WRITER: RuntimeTraceWriter | None = None


def _normalize_required_path(raw_path: str) -> str:
    """Return a normalized absolute path string for required path inputs."""
    return str(Path(raw_path).expanduser().resolve())


def _normalize_optional_path(raw_path: str) -> str:
    """Return a normalized absolute path string, or an empty string."""
    raw_path = str(raw_path or "").strip()
    if not raw_path:
        return ""
    return str(Path(raw_path).expanduser().resolve())


def configure_runtime_trace(
    *,
    project_root: str,
    output_path: str,
    entry_script: str = "",
) -> RuntimeTraceWriter:
    """
    Create and configure a brand-new runtime trace writer for the current run.

    Important behavior:
    - Replaces any previously active writer.
    - Normalizes current project/session paths before logic depends on them.
    - Ensures the output directory exists up front.
    """
    global _TRACE_WRITER

    normalized_project_root = _normalize_required_path(project_root)
    normalized_output_path = _normalize_required_path(output_path)
    normalized_entry_script = _normalize_optional_path(entry_script)

    output_path_obj = Path(normalized_output_path)
    output_path_obj.parent.mkdir(parents=True, exist_ok=True)

    writer = RuntimeTraceWriter()
    writer.configure(
        project_root=normalized_project_root,
        output_path=normalized_output_path,
        entry_script=normalized_entry_script,
    )

    _TRACE_WRITER = writer
    return writer


def get_runtime_trace_writer() -> RuntimeTraceWriter | None:
    """Return the currently active runtime trace writer, if configured."""
    return _TRACE_WRITER


def is_runtime_trace_configured() -> bool:
    """Return True when a runtime trace writer is currently active."""
    return _TRACE_WRITER is not None


def reset_runtime_trace() -> None:
    """Drop the active runtime trace writer reference."""
    global _TRACE_WRITER
    _TRACE_WRITER = None


def trace_event(
    *,
    event_type: str,
    source_file: str,
    source_symbol: str,
    message: str = "",
    object_name: str = "",
    object_type: str = "",
    extra: dict[str, Any] | None = None,
) -> None:
    """Support trace event behavior.
    
    Parameters
    ----------
    event_type : str
        The event type value.
    source_file : str
        The source file value.
    source_symbol : str
        The source symbol value.
    message : str, optional
        The message text.
    object_name : str, optional
        The optional object name value.
    object_type : str, optional
        The optional object type value.
    extra : dict[str, Any] | None, optional
        The optional extra value.
    """
    
    writer = get_runtime_trace_writer()
    if writer is None:
        return

    writer.trace_event(
        event_type=event_type,
        source_file=source_file,
        source_symbol=source_symbol,
        message=message,
        object_name=object_name,
        object_type=object_type,
        extra=extra,
    )


def trace_signal_connection(
    *,
    sender_type: str,
    sender_name: str,
    signal_name: str,
    receiver_type: str,
    receiver_name: str,
    slot_name: str,
    source_file: str = "",
    source_line: int | None = None,
    extra: dict[str, Any] | None = None,
) -> None:
    """Support trace signal connection behavior.
    
    Parameters
    ----------
    sender_type : str
        The sender type value.
    sender_name : str
        The sender name value.
    signal_name : str
        The signal name value.
    receiver_type : str
        The receiver type value.
    receiver_name : str
        The receiver name value.
    slot_name : str
        The slot name value.
    source_file : str, optional
        The optional source file value.
    source_line : int | None, optional
        The optional source line value.
    extra : dict[str, Any] | None, optional
        The optional extra value.
    """
    
    writer = get_runtime_trace_writer()
    if writer is None:
        return

    writer.trace_signal_connection(
        sender_type=sender_type,
        sender_name=sender_name,
        signal_name=signal_name,
        receiver_type=receiver_type,
        receiver_name=receiver_name,
        slot_name=slot_name,
        source_file=source_file,
        source_line=source_line,
        extra=extra,
    )


def trace_state_snapshot(
    *,
    label: str,
    state: dict[str, Any],
) -> None:
    """Support trace state snapshot behavior.
    
    Parameters
    ----------
    label : str
        The label value.
    state : dict[str, Any]
        The state value.
    """
    
    writer = get_runtime_trace_writer()
    if writer is None:
        return

    writer.trace_state_snapshot(
        label=label,
        state=state,
    )


def trace_error(
    *,
    source_file: str,
    source_symbol: str,
    message: str,
    extra: dict[str, Any] | None = None,
) -> None:
    """Support trace error behavior.
    
    Parameters
    ----------
    source_file : str
        The source file value.
    source_symbol : str
        The source symbol value.
    message : str
        The message text.
    extra : dict[str, Any] | None, optional
        The optional extra value.
    """
    
    writer = get_runtime_trace_writer()
    if writer is None:
        return

    writer.trace_error(
        source_file=source_file,
        source_symbol=source_symbol,
        message=message,
        extra=extra,
    )


def trace_warning(
    *,
    source_file: str,
    source_symbol: str,
    message: str,
    extra: dict[str, Any] | None = None,
) -> None:
    """Support trace warning behavior.
    
    Parameters
    ----------
    source_file : str
        The source file value.
    source_symbol : str
        The source symbol value.
    message : str
        The message text.
    extra : dict[str, Any] | None, optional
        The optional extra value.
    """
    
    writer = get_runtime_trace_writer()
    if writer is None:
        return

    writer.trace_warning(
        source_file=source_file,
        source_symbol=source_symbol,
        message=message,
        extra=extra,
    )


def save_runtime_trace() -> Path | None:
    """Save the runtime trace.
    
    Returns
    -------
    Path | None
        The resolved path.
    """
    
    writer = get_runtime_trace_writer()
    if writer is None:
        return None

    return writer.save()
