"""Support runtime evidence collection for Project Reasoner."""

from __future__ import annotations

import inspect
from pathlib import Path
from typing import Any

from .runtime_trace_models import (
    TraceEvent,
    TraceIssue,
    TraceSignalConnection,
    TraceStateSnapshot,
)
from .runtime_trace_utils import now_iso, safe_json_dump, sanitize_data, sanitize_text


class RuntimeTraceWriter:
    def __init__(self) -> None:
        self.project_root: str = ""
        self.entry_script: str = ""
        self.output_path: Path | None = None
        self._reset_buffers()

    def _reset_buffers(self) -> None:
        """Reset all per-run counters and in-memory trace buffers."""
        self._event_counter = 0
        self._snapshot_counter = 0
        self._issue_counter = 0
        self._connection_counter = 0

        self.events: list[TraceEvent] = []
        self.state_snapshots: list[TraceStateSnapshot] = []
        self.errors: list[TraceIssue] = []
        self.warnings: list[TraceIssue] = []
        self.signal_connections: list[TraceSignalConnection] = []

    def configure(
        self,
        *,
        project_root: str,
        output_path: str,
        entry_script: str = "",
    ) -> None:
        """
        Configure the writer for a new run.

        Important behavior:
        - Fully resets prior in-memory state.
        - Updates current project/session information.
        - Normalizes and prepares the output path.
        """
        self._reset_buffers()

        self.project_root = sanitize_text(str(Path(project_root).expanduser().resolve()))
        self.entry_script = sanitize_text(
            str(Path(entry_script).expanduser().resolve()) if str(entry_script).strip() else ""
        )
        self.output_path = Path(output_path).expanduser().resolve()
        self.output_path.parent.mkdir(parents=True, exist_ok=True)

    def _build_stack_context(self, max_frames: int = 8) -> list[dict[str, Any]]:
        frames_out: list[dict[str, Any]] = []

        try:
            stack = inspect.stack()
            for frame_info in stack[2:]:
                file_name = sanitize_text(frame_info.filename)
                function_name = sanitize_text(frame_info.function)

                if not file_name:
                    continue

                if file_name.endswith("runtime_trace_writer.py"):
                    continue

                frames_out.append(
                    {
                        "file": file_name,
                        "line": frame_info.lineno,
                        "function": function_name,
                    }
                )

                if len(frames_out) >= max_frames:
                    break
        except Exception:
            return []

        return frames_out

    def _merge_extra_with_stack(self, extra: dict[str, Any] | None) -> dict[str, Any]:
        merged = dict(extra or {})
        if "stack" not in merged:
            merged["stack"] = self._build_stack_context()
        return sanitize_data(merged)

    def trace_event(
        self,
        *,
        event_type: str,
        source_file: str,
        source_symbol: str,
        message: str = "",
        object_name: str = "",
        object_type: str = "",
        extra: dict[str, Any] | None = None,
    ) -> None:
        self._event_counter += 1
        self.events.append(
            TraceEvent(
                event_id=self._event_counter,
                time=now_iso(),
                event_type=sanitize_text(event_type),
                source_file=sanitize_text(source_file),
                source_symbol=sanitize_text(source_symbol),
                message=sanitize_text(message),
                object_name=sanitize_text(object_name),
                object_type=sanitize_text(object_type),
                extra=self._merge_extra_with_stack(extra),
            )
        )

    def trace_state_snapshot(
        self,
        *,
        label: str,
        state: dict[str, Any],
    ) -> None:
        self._snapshot_counter += 1
        self.state_snapshots.append(
            TraceStateSnapshot(
                snapshot_id=self._snapshot_counter,
                time=now_iso(),
                label=sanitize_text(label),
                state=sanitize_data(state),
            )
        )

    def trace_error(
        self,
        *,
        source_file: str,
        source_symbol: str,
        message: str,
        extra: dict[str, Any] | None = None,
    ) -> None:
        self._issue_counter += 1
        self.errors.append(
            TraceIssue(
                issue_id=self._issue_counter,
                time=now_iso(),
                source_file=sanitize_text(source_file),
                source_symbol=sanitize_text(source_symbol),
                message=sanitize_text(message),
                extra=self._merge_extra_with_stack(extra),
            )
        )

    def trace_warning(
        self,
        *,
        source_file: str,
        source_symbol: str,
        message: str,
        extra: dict[str, Any] | None = None,
    ) -> None:
        self._issue_counter += 1
        self.warnings.append(
            TraceIssue(
                issue_id=self._issue_counter,
                time=now_iso(),
                source_file=sanitize_text(source_file),
                source_symbol=sanitize_text(source_symbol),
                message=sanitize_text(message),
                extra=self._merge_extra_with_stack(extra),
            )
        )

    def trace_signal_connection(
        self,
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
        self._connection_counter += 1
        self.signal_connections.append(
            TraceSignalConnection(
                connection_id=self._connection_counter,
                time=now_iso(),
                sender_type=sanitize_text(sender_type),
                sender_name=sanitize_text(sender_name),
                signal_name=sanitize_text(signal_name),
                receiver_type=sanitize_text(receiver_type),
                receiver_name=sanitize_text(receiver_name),
                slot_name=sanitize_text(slot_name),
                source_file=sanitize_text(source_file),
                source_line=source_line,
                extra=self._merge_extra_with_stack(extra),
            )
        )

    def build_payload(self) -> dict[str, Any]:
        return {
            "trace_info": {
                "trace_version": "1.2",
                "generated_at": now_iso(),
            },
            "session_info": {
                "project_root": self.project_root,
                "entry_script": self.entry_script,
                "output_path": str(self.output_path) if self.output_path is not None else "",
            },
            "events": [
                {
                    "id": item.event_id,
                    "time": item.time,
                    "timestamp": item.time,
                    "type": item.event_type,
                    "event_type": item.event_type,
                    "source_file": item.source_file,
                    "source_symbol": item.source_symbol,
                    "message": item.message,
                    "object_name": item.object_name,
                    "object_type": item.object_type,
                    "tags": (
                        item.extra.get("tags", [])
                        if isinstance(item.extra, dict)
                        and isinstance(item.extra.get("tags", []), list)
                        else []
                    ),
                    "extra": item.extra,
                }
                for item in self.events
            ],
            "signal_connections": [
                {
                    "id": item.connection_id,
                    "time": item.time,
                    "timestamp": item.time,
                    "sender_type": item.sender_type,
                    "sender_name": item.sender_name,
                    "signal_name": item.signal_name,
                    "receiver_type": item.receiver_type,
                    "receiver_name": item.receiver_name,
                    "slot_name": item.slot_name,
                    "source_file": item.source_file,
                    "caller_file": item.source_file,
                    "source_line": item.source_line,
                    "caller_line": item.source_line,
                    "extra": item.extra,

                    # Compatibility aliases for downstream consumers
                    "widget": item.sender_name,
                    "widget_name": item.sender_name,
                    "widget_type": item.sender_type,
                    "signal": item.signal_name,
                    "handler": item.slot_name,
                    "target": item.slot_name,
                    "target_kind": item.receiver_type,
                    "line": item.source_line,
                }
                for item in self.signal_connections
            ],
            "state_snapshots": [
                {
                    "id": item.snapshot_id,
                    "time": item.time,
                    "timestamp": item.time,
                    "label": item.label,
                    "context": item.label,
                    "state": item.state,
                }
                for item in self.state_snapshots
            ],
            "errors": [
                {
                    "id": item.issue_id,
                    "time": item.time,
                    "source_file": item.source_file,
                    "source_symbol": item.source_symbol,
                    "message": item.message,
                    "extra": item.extra,
                }
                for item in self.errors
            ],
            "warnings": [
                {
                    "id": item.issue_id,
                    "time": item.time,
                    "source_file": item.source_file,
                    "source_symbol": item.source_symbol,
                    "message": item.message,
                    "extra": item.extra,
                }
                for item in self.warnings
            ],
        }

    def save(self) -> Path:
        if self.output_path is None:
            raise RuntimeError("RuntimeTraceWriter is not configured.")

        payload = self.build_payload()
        safe_json_dump(payload, self.output_path)
        return self.output_path