"""Support static evidence collection for Project Reasoner."""

# kanda_reasoner/kanda_reasoner_app/reasoner_context_collector/collector_runtime_trace.py

from __future__ import annotations

"""
collector_runtime_trace.py
--------------------------
Reads the runtime_trace.json produced by
reasoner_runtime_collector/runtime_runner.py
and converts its three data streams into index structures
that plug directly into collector_main.run_collector().

Output keys
-----------
signal_connections  : list[dict]
    Live-verified Qt signal connections captured at runtime by
    qt_connection_monitor.  Each record carries sender type/name,
    signal name, receiver type/name, slot name, caller location,
    and whether the connection was matched against the static
    qt_signal_map (field: "static_match").

state_snapshots     : list[dict]
    Widget-state snapshots captured by trace_state_snapshot() /
    collect_visualizer_state().  Each record carries a timestamp,
    context label, and a flat dict of attribute -> value pairs.
    Enriched with the owning file from attribute_state_map where
    possible (field: "owner_file").

call_stack_index    : dict[str, list[dict]]
    Per-source-file list of events that had a call stack recorded
    by _build_stack_context().  Keyed by the source_file field of
    the TraceEvent so callers can look up "what events touched
    this file and what was the stack at that moment."

summary             : dict
    Scalar counts consumed by project_summary in collector_main.

Returns an empty structure (all keys present, all values empty)
when runtime_trace_json is None or the file does not exist, so
collector_main never needs to guard against None.
"""

import json
from pathlib import Path
from typing import Any


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def build_runtime_trace_index(
    project_root: Path,
    runtime_trace_json: str | None,
    symbol_index: dict,
    qt_signal_map: dict,
    attribute_state_map: dict,
) -> dict:
    """
    Read runtime_trace.json and return enriched index structures.

    Parameters
    ----------
    project_root        : resolved project root (used for path normalisation)
    runtime_trace_json  : absolute path string to runtime_trace.json, or None
    symbol_index        : from collector_main._build_symbol_index()
    qt_signal_map       : from collector_qt.extract_qt_signal_map()
    attribute_state_map : from collector_state.build_attribute_state_map()

    Returns
    -------
    dict with keys: signal_connections, state_snapshots,
                    call_stack_index, summary
    """
    empty = _empty_result()

    if not runtime_trace_json:
        return empty

    trace_path = Path(runtime_trace_json).expanduser()
    if not trace_path.exists():
        return empty

    try:
        raw = json.loads(trace_path.read_text(encoding="utf-8"))
    except Exception:
        return empty

    if not isinstance(raw, dict):
        return empty

    events             = raw.get("events",             []) or []
    signal_connections = raw.get("signal_connections", []) or []
    state_snapshots    = raw.get("state_snapshots",    []) or []

    # Build a flat set of static signal keys for fast lookup
    # qt_signal_map is keyed by file -> list of signal records
    static_signal_keys = _build_static_signal_keys(qt_signal_map)

    # Build owner-file lookup from attribute_state_map
    # attribute_state_map is keyed by file -> list of {attr, ...} dicts
    attr_owner_map = _build_attr_owner_map(attribute_state_map)

    enriched_signals    = _enrich_signal_connections(signal_connections, static_signal_keys, project_root)
    enriched_snapshots  = _enrich_state_snapshots(state_snapshots, attr_owner_map, project_root)
    call_stack_index    = _build_call_stack_index(events, project_root)

    summary = {
        "signal_connection_count":         len(enriched_signals),
        "static_matched_signal_count":     sum(1 for s in enriched_signals if s.get("static_match")),
        "dynamic_only_signal_count":       sum(1 for s in enriched_signals if not s.get("static_match")),
        "state_snapshot_count":            len(enriched_snapshots),
        "owned_snapshot_count":            sum(1 for s in enriched_snapshots if s.get("owner_file")),
        "call_stack_indexed_file_count":   len(call_stack_index),
        "total_stacked_event_count":       sum(len(v) for v in call_stack_index.values()),
        "runtime_trace_path":              str(trace_path),
    }

    return {
        "signal_connections": enriched_signals,
        "state_snapshots":    enriched_snapshots,
        "call_stack_index":   call_stack_index,
        "summary":            summary,
    }


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _empty_result() -> dict:
    return {
        "signal_connections": [],
        "state_snapshots":    [],
        "call_stack_index":   {},
        "summary":            {},
    }


# ------------------------------------------------------------------
# Static signal key set
# ------------------------------------------------------------------

def _build_static_signal_keys(qt_signal_map: dict | list) -> set:
    """
    Build a set of (signal_name, slot_fragment) tuples from the
    static qt_signal_map so we can mark runtime connections as
    "static_match": True / False.

    Supports both shapes:
        { file_path: [ {signal_name, target, source_symbol, ...}, ... ] }
        [ {signal_name, target, source_symbol, ...}, ... ]
    """
    keys: set = set()

    if isinstance(qt_signal_map, dict):
        record_groups = qt_signal_map.values()
    elif isinstance(qt_signal_map, list):
        record_groups = [qt_signal_map]
    else:
        return keys

    for records in record_groups:
        if not isinstance(records, list):
            continue
        for rec in records:
            if not isinstance(rec, dict):
                continue
            sig = _safe_str(rec.get("signal_name", ""))
            slot = _safe_str(rec.get("target", ""))
            if sig:
                keys.add((sig, slot))

    return keys


# ------------------------------------------------------------------
# Attribute owner map
# ------------------------------------------------------------------

def _build_attr_owner_map(attribute_state_map: dict) -> dict:
    """
    Build { attr_name: file_path } from attribute_state_map.

    attribute_state_map schema (from collector_state):
        { file_path: [ {attr, ...}, ... ] }
    """
    owner: dict = {}
    for file_path, records in attribute_state_map.items():
        if not isinstance(records, list):
            continue
        for rec in records:
            if not isinstance(rec, dict):
                continue
            attr = _safe_str(rec.get("attr", ""))
            if attr and attr not in owner:
                owner[attr] = file_path
    return owner


# ------------------------------------------------------------------
# Signal connection enrichment
# ------------------------------------------------------------------

def _enrich_signal_connections(
    raw_connections: list,
    static_signal_keys: set,
    project_root: Path,
) -> list[dict]:
    """
    Normalise and enrich each TraceSignalConnection record.

    TraceSignalConnection fields (from runtime_trace_writer.py lines 177-188):
        timestamp, sender_type, sender_name, signal_name,
        receiver_type, receiver_name, slot_name,
        caller_file, caller_line, extra (dict with call-stack data)
    """
    out: list[dict] = []
    for raw in raw_connections:
        if not isinstance(raw, dict):
            continue

        sig        = _safe_str(raw.get("signal_name",   ""))
        slot       = _safe_str(raw.get("slot_name",     ""))
        caller_file = _safe_str(raw.get("caller_file",  ""))

        # Normalise caller_file to a project-relative path
        rel_caller = _rel_path(caller_file, project_root)

        # Check whether this connection was visible to static analysis
        static_match = (sig, slot) in static_signal_keys or (sig, "") in static_signal_keys

        out.append({
            "timestamp":     _safe_str(raw.get("timestamp",     "")),
            "sender_type":   _safe_str(raw.get("sender_type",   "")),
            "sender_name":   _safe_str(raw.get("sender_name",   "")),
            "signal_name":   sig,
            "receiver_type": _safe_str(raw.get("receiver_type", "")),
            "receiver_name": _safe_str(raw.get("receiver_name", "")),
            "slot_name":     slot,
            "caller_file":   rel_caller,
            "caller_line":   raw.get("caller_line", None),
            "extra":         raw.get("extra", {}) or {},
            "static_match":  static_match,
        })
    return out


# ------------------------------------------------------------------
# State snapshot enrichment
# ------------------------------------------------------------------

def _enrich_state_snapshots(
    raw_snapshots: list,
    attr_owner_map: dict,
    project_root: Path,
) -> list[dict]:
    """
    Normalise and enrich each TraceStateSnapshot record.

    TraceStateSnapshot fields (from runtime_trace_writer.py lines 113-118):
        timestamp, context, state (dict of attr -> value)
    """
    out: list[dict] = []
    for raw in raw_snapshots:
        if not isinstance(raw, dict):
            continue

        state = raw.get("state", {}) or {}
        if not isinstance(state, dict):
            state = {}

        # Find the most likely owner file by matching any attr key
        owner_file = ""
        for attr in state:
            candidate = attr_owner_map.get(_safe_str(attr), "")
            if candidate:
                owner_file = candidate
                break

        out.append({
            "timestamp":  _safe_str(raw.get("timestamp", "")),
            "context":    _safe_str(raw.get("context",   "")),
            "state":      state,
            "owner_file": owner_file,
        })
    return out


# ------------------------------------------------------------------
# Call-stack index
# ------------------------------------------------------------------

def _build_call_stack_index(
    raw_events: list,
    project_root: Path,
) -> dict[str, list[dict]]:
    """
    Build { source_file: [ event_summary, ... ] } for every event
    that has a non-empty call stack stored in its extra dict.

    TraceEvent fields (from runtime_trace_writer.py lines 92-102):
        timestamp, event_type, source_file, source_symbol,
        message, tags, extra (merged with call-stack frames)

    Call-stack frames (from _build_stack_context lines 48-67):
        list of { file, function } dicts appended to extra["stack"]
    """
    index: dict[str, list] = {}

    for raw in raw_events:
        if not isinstance(raw, dict):
            continue

        extra = raw.get("extra", {}) or {}
        stack = extra.get("stack", []) if isinstance(extra, dict) else []
        if not stack:
            continue

        source_file = _safe_str(raw.get("source_file", ""))
        rel_source  = _rel_path(source_file, project_root)
        if not rel_source:
            continue

        # Normalise stack frame paths
        clean_stack = []
        for frame in stack:
            if not isinstance(frame, dict):
                continue
            clean_stack.append({
                "file":     _rel_path(_safe_str(frame.get("file", "")), project_root),
                "function": _safe_str(frame.get("function", "")),
            })

        event_summary = {
            "timestamp":     _safe_str(raw.get("timestamp",     "")),
            "event_type":    _safe_str(raw.get("event_type",    "")),
            "source_symbol": _safe_str(raw.get("source_symbol", "")),
            "message":       _safe_str(raw.get("message",       "")),
            "tags":          raw.get("tags", []) or [],
            "stack":         clean_stack,
        }

        if rel_source not in index:
            index[rel_source] = []
        index[rel_source].append(event_summary)

    return index


# ------------------------------------------------------------------
# Utilities
# ------------------------------------------------------------------

def _safe_str(value: Any) -> str:
    if value is None:
        return ""
    try:
        return str(value).strip()
    except Exception:
        return ""


def _rel_path(file_str: str, project_root: Path) -> str:
    """
    Convert an absolute path string to a project-relative forward-slash path.
    Returns the original string (normalised) if it cannot be made relative.
    """
    if not file_str:
        return ""
    try:
        p = Path(file_str).resolve()
        rel = p.relative_to(project_root)
        return str(rel).replace("\\", "/")
    except Exception:
        # Already relative, or outside project root - just normalise separators
        return file_str.replace("\\", "/").strip()
