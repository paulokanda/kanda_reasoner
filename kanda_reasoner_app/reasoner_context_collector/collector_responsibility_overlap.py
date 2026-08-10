# project-path: kanda_reasoner_app/reasoner_context_collector/collector_responsibility_overlap.py
"""Support static evidence collection for Project Reasoner."""

from __future__ import annotations

from .collector_responsibility_overlap_help.extraction import (
    _call_name_roots,
    _file_record_map,
    _symbol_name_set,
)
from .collector_responsibility_overlap_help.scoring import (
    _jaccard,
    _passes_gate,
    _strong_signal_count,
)
__all__ = [
    'build_overlap_hotspots',
    'build_responsibility_overlap_index',
    'build_responsibility_overlap_summary',
]

from itertools import combinations
from typing import Any
from .collector_responsibility_overlap_helpers_private import (
    _safe_float,
    _safe_bucket,
    _safe_role,
    _basename_tokens,
    _semantic_role_set,
    _summary_terms,
)


GENERIC_TOKENS = {
    "ui",
    "widget",
    "button",
    "dialog",
    "window",
    "tab",
    "panel",
    "bar",
    "menu",
    "layout",
    "tool",
    "tools",
    "template",
    "templates",
    "base",
    "common",
    "utils",
    "util",
    "helper",
    "helpers",
    "core",
    "main",
    "app",
    "manager",
    "controller",
    "service",
    "data",
    "file",
    "files",
    "module",
    "modules",
    "test",
    "tests",
    "view",
    "builder",
    "handler",
}

GENERIC_CALL_ROOTS = {
    "connect",
    "emit",
    "show",
    "hide",
    "update",
    "refresh",
    "clear",
    "reset",
    "close",
    "open",
    "load",
    "save",
    "append",
    "remove",
    "settext",
    "setvalue",
    "setenabled",
    "setvisible",
    "addwidget",
    "addlayout",
    "addtab",
    "setlayout",
    "setcentralwidget",
    "resize",
    "move",
    "exec",
    "exec_",
    "start",
    "stop",
    "plot",
    "render",
    "draw",
}

GENERIC_ROLE_TOKENS = {
    "ui",
    "service",
    "controller",
    "domain",
    "general",
    "visualization",
}

MIN_OVERLAP_SCORE = 1.55
MIN_HOTSPOT_SCORE = 1.95
















def build_responsibility_overlap_index(
    files_payload: list[dict[str, Any]],
    boundary_index: dict[str, dict[str, Any]],
    canonical_conflict_index: dict[str, dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    """Build a responsibility overlap index.
    
    Parameters
    ----------
    files_payload : list[dict[str, Any]]
        The files payload value.
    boundary_index : dict[str, dict[str, Any]]
        The boundary index value.
    canonical_conflict_index : dict[str, dict[str, Any]]
        The canonical conflict index value.
    
    Returns
    -------
    dict[str, dict[str, Any]]
        The mapped values.
    """
    
    record_map = _file_record_map(files_payload)
    file_paths = sorted(record_map.keys())
    pair_rows: list[dict[str, Any]] = []

    for left_file, right_file in combinations(file_paths, 2):
        left = record_map[left_file]
        right = record_map[right_file]

        left_bucket = _safe_bucket(left_file, files_payload)
        right_bucket = _safe_bucket(right_file, files_payload)

        left_role = _safe_role(left_file, boundary_index)
        right_role = _safe_role(right_file, boundary_index)

        left_roles = _semantic_role_set(left)
        right_roles = _semantic_role_set(right)

        left_terms = _summary_terms(left)
        right_terms = _summary_terms(right)

        left_symbols = _symbol_name_set(left)
        right_symbols = _symbol_name_set(right)

        left_calls = _call_name_roots(left)
        right_calls = _call_name_roots(right)

        base_name_score = _jaccard(_basename_tokens(left_file), _basename_tokens(right_file))
        semantic_role_score = _jaccard(left_roles, right_roles)
        summary_term_score = _jaccard(left_terms, right_terms)
        symbol_score = _jaccard(left_symbols, right_symbols)
        call_score = _jaccard(left_calls, right_calls)

        same_bucket_bonus = 0.03 if left_bucket == right_bucket and summary_term_score >= 0.20 else 0.0
        same_role_bonus = 0.03 if left_role == right_role and summary_term_score >= 0.20 else 0.0

        left_shadow = bool(canonical_conflict_index.get(left_file, {}).get("shadow_severity", 0))
        right_shadow = bool(canonical_conflict_index.get(right_file, {}).get("shadow_severity", 0))
        shadow_bonus = 0.08 if (left_shadow or right_shadow) and base_name_score >= 0.40 else 0.0

        overlap_score = (
            (base_name_score * 2.8)
            + (semantic_role_score * 1.8)
            + (summary_term_score * 3.4)
            + (symbol_score * 1.7)
            + (call_score * 1.6)
            + same_bucket_bonus
            + same_role_bonus
            + shadow_bonus
        )

        strong_signal_count = _strong_signal_count(
            base_name_score,
            semantic_role_score,
            summary_term_score,
            symbol_score,
            call_score,
        )

        if not _passes_gate(
            base_name_score,
            semantic_role_score,
            summary_term_score,
            symbol_score,
            call_score,
            overlap_score,
            strong_signal_count,
        ):
            continue

        overlap_type = "general_overlap"
        if base_name_score >= 0.60 and summary_term_score >= 0.30:
            overlap_type = "name_and_responsibility_overlap"
        elif semantic_role_score >= 0.60 and summary_term_score >= 0.35 and call_score >= 0.25:
            overlap_type = "behavioral_overlap"
        elif symbol_score >= 0.40 and summary_term_score >= 0.25:
            overlap_type = "symbol_overlap"

        pair_rows.append(
            {
                "left_file": left_file,
                "right_file": right_file,
                "left_bucket": left_bucket,
                "right_bucket": right_bucket,
                "left_role": left_role,
                "right_role": right_role,
                "base_name_score": round(base_name_score, 3),
                "semantic_role_score": round(semantic_role_score, 3),
                "summary_term_score": round(summary_term_score, 3),
                "symbol_score": round(symbol_score, 3),
                "call_score": round(call_score, 3),
                "strong_signal_count": strong_signal_count,
                "overlap_score": round(overlap_score, 3),
                "overlap_type": overlap_type,
                "same_bucket": left_bucket == right_bucket,
                "same_role": left_role == right_role,
            }
        )

    pair_rows.sort(
        key=lambda item: (
            -_safe_float(item.get("overlap_score", 0.0)),
            item.get("left_file", ""),
            item.get("right_file", ""),
        )
    )

    file_index: dict[str, dict[str, Any]] = {}
    for file_path in file_paths:
        file_index[file_path] = {
            "file": file_path,
            "bucket": _safe_bucket(file_path, files_payload),
            "boundary_role": _safe_role(file_path, boundary_index),
            "overlap_pair_count": 0,
            "max_overlap_score": 0.0,
            "overlap_types": [],
            "overlap_files": [],
            "pairs": [],
        }

    for row in pair_rows:
        left_file = row["left_file"]
        right_file = row["right_file"]
        score = _safe_float(row.get("overlap_score", 0.0))
        overlap_type = str(row.get("overlap_type", "")).strip()

        for current_file, other_file in ((left_file, right_file), (right_file, left_file)):
            payload = file_index[current_file]
            payload["overlap_pair_count"] += 1
            payload["max_overlap_score"] = max(payload["max_overlap_score"], score)

            if overlap_type and overlap_type not in payload["overlap_types"]:
                payload["overlap_types"].append(overlap_type)
            if other_file not in payload["overlap_files"]:
                payload["overlap_files"].append(other_file)

            payload["pairs"].append(row)

    for payload in file_index.values():
        payload["max_overlap_score"] = round(payload["max_overlap_score"], 3)
        payload["overlap_types"] = sorted(payload["overlap_types"])
        payload["overlap_files"] = sorted(payload["overlap_files"])
        payload["is_overlap_hotspot"] = bool(
            payload["overlap_pair_count"] >= 2 and payload["max_overlap_score"] >= MIN_HOTSPOT_SCORE
        )

    return dict(sorted(file_index.items()))


def build_responsibility_overlap_summary(
    responsibility_overlap_index: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    """Build a responsibility overlap summary.
    
    Parameters
    ----------
    responsibility_overlap_index : dict[str, dict[str, Any]]
        The responsibility overlap index value.
    
    Returns
    -------
    dict[str, Any]
        The mapped values.
    """
    
    rows: list[dict[str, Any]] = []
    overlap_type_frequency: dict[str, int] = {}
    overlap_pair_count = 0

    for file_path, payload in responsibility_overlap_index.items():
        pair_count = int(payload.get("overlap_pair_count", 0))
        overlap_pair_count += pair_count

        overlap_types = list(payload.get("overlap_types", []))
        for overlap_type in overlap_types:
            overlap_type_frequency[overlap_type] = overlap_type_frequency.get(overlap_type, 0) + 1

        rows.append(
            {
                "file": file_path,
                "bucket": str(payload.get("bucket", "general") or "general"),
                "boundary_role": str(
                    payload.get("boundary_role", "unclassified") or "unclassified"
                ),
                "overlap_pair_count": pair_count,
                "max_overlap_score": _safe_float(payload.get("max_overlap_score", 0.0)),
                "overlap_types": overlap_types,
                "is_overlap_hotspot": bool(payload.get("is_overlap_hotspot", False)),
            }
        )

    rows.sort(
        key=lambda item: (
            -int(item.get("overlap_pair_count", 0)),
            -_safe_float(item.get("max_overlap_score", 0.0)),
            item.get("file", ""),
        )
    )

    hotspot_count = sum(1 for row in rows if bool(row.get("is_overlap_hotspot", False)))

    return {
        "file_count": len(rows),
        "responsibility_overlap_pair_count": overlap_pair_count // 2,
        "overlap_hotspot_count": hotspot_count,
        "overlap_type_frequency": dict(sorted(overlap_type_frequency.items())),
        "files": rows,
    }


def build_overlap_hotspots(
    responsibility_overlap_index: dict[str, dict[str, Any]],
    limit: int = 25,
) -> list[dict[str, Any]]:
    """Build a overlap hotspots.
    
    Parameters
    ----------
    responsibility_overlap_index : dict[str, dict[str, Any]]
        The responsibility overlap index value.
    limit : int, optional
        The optional limit value.
    
    Returns
    -------
    list[dict[str, Any]]
        The list of values.
    """
    
    rows: list[dict[str, Any]] = []

    for file_path, payload in responsibility_overlap_index.items():
        if not bool(payload.get("is_overlap_hotspot", False)):
            continue

        rows.append(
            {
                "file": file_path,
                "bucket": str(payload.get("bucket", "general") or "general"),
                "boundary_role": str(
                    payload.get("boundary_role", "unclassified") or "unclassified"
                ),
                "overlap_pair_count": int(payload.get("overlap_pair_count", 0)),
                "max_overlap_score": _safe_float(payload.get("max_overlap_score", 0.0)),
                "overlap_types": list(payload.get("overlap_types", [])),
                "overlap_files": list(payload.get("overlap_files", []))[:15],
                "is_overlap_hotspot": bool(payload.get("is_overlap_hotspot", False)),
            }
        )

    rows.sort(
        key=lambda item: (
            -int(item.get("overlap_pair_count", 0)),
            -_safe_float(item.get("max_overlap_score", 0.0)),
            item.get("file", ""),
        )
    )

    return rows[:limit]
