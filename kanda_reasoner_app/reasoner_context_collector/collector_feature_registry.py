# project-path: kanda_reasoner_app/reasoner_context_collector/collector_feature_registry.py
"""Support static evidence collection for Project Reasoner."""

from __future__ import annotations

from typing import Any


FEATURE_RULES = {
    "startup": {
        "tokens": {
            "startup",
            "bootstrap",
            "launch",
            "main",
            "init",
            "initialize",
            "entry",
            "application",
            "qapplication",
        },
    },
    "timeline": {
        "tokens": {
            "timeline",
            "time_window",
            "timewindow",
            "timebar",
            "time_bar",
            "scroll_to_time",
            "time selection",
            "time navigation",
        },
    },
    "topomap": {
        "tokens": {
            "topomap",
            "amplitude_map",
            "amplitudemap",
            "topo",
            "topographic",
            "sensor map",
            "head map",
        },
    },
    "loading": {
        "tokens": {
            "load",
            "loader",
            "open_file",
            "read_file",
            "import",
            "edf",
            "recording_loader",
            "open",
        },
    },
    "saving_export": {
        "tokens": {
            "save",
            "export",
            "write",
            "dump",
            "persist",
            "to_json",
            "to_csv",
            "to_hdf",
            "savefig",
        },
    },
    "tabs_navigation": {
        "tokens": {
            "tab",
            "tabs",
            "notebook",
            "tabfactory",
            "tab switch",
            "handle_tab_switch",
        },
    },
    "dropdowns_filters": {
        "tokens": {
            "dropdown",
            "combobox",
            "combo",
            "filter",
            "selector",
            "sensitivity",
            "time window",
        },
    },
    "plot_visualization": {
        "tokens": {
            "plot",
            "render",
            "canvas",
            "visualizer",
            "visualization",
            "draw",
            "graph",
            "heatmap",
            "spectrogram",
            "connectivity",
        },
    },
    "state_reset_cleanup": {
        "tokens": {
            "reset",
            "cleanup",
            "clear",
            "restore",
            "close",
            "hide_amplitude_map_elements",
            "reset_to_initial_eeg_state",
        },
    },
    "ui_actions_signals": {
        "tokens": {
            "clicked",
            "connect",
            "signal",
            "slot",
            "emit",
            "button",
            "action",
        },
    },
    "persistence_config": {
        "tokens": {
            "config",
            "settings",
            "schema",
            "json",
            "csv",
            "hdf",
            "hdf5",
            "cache",
            "path",
            "folder",
        },
    },
    "project_reasoner": {
        "tokens": {
            "project_reasoner",
            "collector",
            "reasoner",
            "index",
            "inspection",
            "structural",
            "hotspot",
            "overlap",
            "canonical",
        },
    },
}


def _safe_text(value: Any) -> str:
    """Support safe text behavior.
    
    Parameters
    ----------
    value : Any
        The input value.
    
    Returns
    -------
    str
        The string result.
    """
    
    return str(value or "").strip().lower()


def _normalize_text_parts(text: str) -> set[str]:
    """Support normalize text parts behavior.
    
    Parameters
    ----------
    text : str
        The text value.
    
    Returns
    -------
    set[str]
        The set result.
    """
    
    cleaned = (
        _safe_text(text)
        .replace("\\", " ")
        .replace("/", " ")
        .replace("-", " ")
        .replace("_", " ")
        .replace(".", " ")
        .replace("(", " ")
        .replace(")", " ")
        .replace(",", " ")
        .replace(":", " ")
        .replace(";", " ")
    )
    return {part for part in cleaned.split() if part}


def _record_text_corpus(file_record: dict[str, Any]) -> set[str]:
    """Support record text corpus behavior.
    
    Parameters
    ----------
    file_record : dict[str, Any]
        The file record value.
    
    Returns
    -------
    set[str]
        The set result.
    """
    
    out: set[str] = set()

    for field in (
        "path",
        "module_name",
        "docstring",
        "summary",
        "primary_role",
    ):
        out.update(_normalize_text_parts(_safe_text(file_record.get(field, ""))))

    for value in file_record.get("secondary_roles", []):
        out.update(_normalize_text_parts(_safe_text(value)))

    for value in file_record.get("semantic_roles", []):
        out.update(_normalize_text_parts(_safe_text(value)))

    for value in file_record.get("semantic_hints", []):
        out.update(_normalize_text_parts(_safe_text(value)))

    summary_payload = file_record.get("module_responsibility_summary", {})
    if isinstance(summary_payload, dict):
        for key in (
            "primary_responsibilities",
            "secondary_responsibilities",
            "keywords",
            "responsibility_terms",
        ):
            values = summary_payload.get(key, [])
            if isinstance(values, list):
                for value in values:
                    out.update(_normalize_text_parts(_safe_text(value)))

    for fn in file_record.get("functions", []):
        if not isinstance(fn, dict):
            continue
        out.update(_normalize_text_parts(_safe_text(fn.get("name", ""))))
        out.update(_normalize_text_parts(_safe_text(fn.get("qualname", ""))))
        out.update(_normalize_text_parts(_safe_text(fn.get("docstring", ""))))
        for call in fn.get("calls", []):
            if isinstance(call, dict):
                out.update(_normalize_text_parts(_safe_text(call.get("call_name", ""))))

    for cls in file_record.get("classes", []):
        if not isinstance(cls, dict):
            continue
        out.update(_normalize_text_parts(_safe_text(cls.get("name", ""))))
        out.update(_normalize_text_parts(_safe_text(cls.get("docstring", ""))))
        for method in cls.get("methods", []):
            if not isinstance(method, dict):
                continue
            out.update(_normalize_text_parts(_safe_text(method.get("name", ""))))
            out.update(_normalize_text_parts(_safe_text(method.get("qualname", ""))))
            out.update(_normalize_text_parts(_safe_text(method.get("docstring", ""))))
            for call in method.get("calls", []):
                if isinstance(call, dict):
                    out.update(_normalize_text_parts(_safe_text(call.get("call_name", ""))))

    return out


def _safe_bucket(file_record: dict[str, Any]) -> str:
    """Support safe bucket behavior.
    
    Parameters
    ----------
    file_record : dict[str, Any]
        The file record value.
    
    Returns
    -------
    str
        The string result.
    """
    
    bucket = _safe_text(file_record.get("subsystem_bucket", ""))
    return bucket or "general"


def _safe_boundary_role(
    file_record: dict[str, Any],
    boundary_index: dict[str, dict[str, Any]],
) -> str:
    """Support safe boundary role behavior.
    
    Parameters
    ----------
    file_record : dict[str, Any]
        The file record value.
    boundary_index : dict[str, dict[str, Any]]
        The boundary index value.
    
    Returns
    -------
    str
        The string result.
    """
    
    path = str(file_record.get("path", "")).strip()
    payload = boundary_index.get(path, {})
    if not isinstance(payload, dict):
        return "unclassified"
    role = _safe_text(payload.get("boundary_role", ""))
    return role or "unclassified"


def build_feature_registry(
    files_payload: list[dict[str, Any]],
    boundary_index: dict[str, dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    """Build a feature registry.
    
    Parameters
    ----------
    files_payload : list[dict[str, Any]]
        The files payload value.
    boundary_index : dict[str, dict[str, Any]]
        The boundary index value.
    
    Returns
    -------
    dict[str, dict[str, Any]]
        The mapped values.
    """
    
    feature_registry: dict[str, dict[str, Any]] = {}

    for feature_name in FEATURE_RULES:
        feature_registry[feature_name] = {
            "feature": feature_name,
            "file_count": 0,
            "files": [],
            "buckets": [],
            "boundary_roles": [],
            "match_scores": {},
        }

    for file_record in files_payload:
        path = str(file_record.get("path", "")).strip()
        if not path:
            continue

        corpus = _record_text_corpus(file_record)
        bucket = _safe_bucket(file_record)
        boundary_role = _safe_boundary_role(file_record, boundary_index)

        for feature_name, rule in FEATURE_RULES.items():
            tokens = rule["tokens"]
            matched_tokens = sorted(token for token in tokens if token in corpus)
            match_score = len(matched_tokens)

            if match_score <= 0:
                continue

            feature_payload = feature_registry[feature_name]
            feature_payload["files"].append(
                {
                    "file": path,
                    "bucket": bucket,
                    "boundary_role": boundary_role,
                    "match_score": match_score,
                    "matched_tokens": matched_tokens,
                }
            )
            feature_payload["match_scores"][path] = match_score

            if bucket not in feature_payload["buckets"]:
                feature_payload["buckets"].append(bucket)

            if boundary_role not in feature_payload["boundary_roles"]:
                feature_payload["boundary_roles"].append(boundary_role)

    for feature_name, payload in feature_registry.items():
        payload["files"].sort(
            key=lambda item: (
                -int(item.get("match_score", 0)),
                item.get("file", ""),
            )
        )
        payload["file_count"] = len(payload["files"])
        payload["buckets"] = sorted(payload["buckets"])
        payload["boundary_roles"] = sorted(payload["boundary_roles"])

    return dict(sorted(feature_registry.items()))


def build_feature_summary(
    feature_registry: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    """Build a feature summary.
    
    Parameters
    ----------
    feature_registry : dict[str, dict[str, Any]]
        The feature registry value.
    
    Returns
    -------
    dict[str, Any]
        The mapped values.
    """
    
    rows: list[dict[str, Any]] = []
    mapped_file_count = 0
    unique_files: set[str] = set()

    for feature_name, payload in feature_registry.items():
        file_count = int(payload.get("file_count", 0))
        mapped_file_count += file_count

        for item in payload.get("files", []):
            if isinstance(item, dict):
                file_path = str(item.get("file", "")).strip()
                if file_path:
                    unique_files.add(file_path)

        rows.append(
            {
                "feature": feature_name,
                "file_count": file_count,
                "bucket_count": len(payload.get("buckets", [])),
                "boundary_role_count": len(payload.get("boundary_roles", [])),
                "top_files": [item.get("file", "") for item in payload.get("files", [])[:10]],
            }
        )

    rows.sort(
        key=lambda item: (
            -int(item.get("file_count", 0)),
            item.get("feature", ""),
        )
    )

    return {
        "feature_count": len(rows),
        "feature_mapped_file_count": mapped_file_count,
        "unique_feature_file_count": len(unique_files),
        "features": rows,
    }


def build_feature_hotspots(
    feature_registry: dict[str, dict[str, Any]],
    limit: int = 25,
) -> list[dict[str, Any]]:
    """Build a feature hotspots.
    
    Parameters
    ----------
    feature_registry : dict[str, dict[str, Any]]
        The feature registry value.
    limit : int, optional
        The optional limit value.
    
    Returns
    -------
    list[dict[str, Any]]
        The list of values.
    """
    
    rows: list[dict[str, Any]] = []

    for feature_name, payload in feature_registry.items():
        rows.append(
            {
                "feature": feature_name,
                "file_count": int(payload.get("file_count", 0)),
                "bucket_count": len(payload.get("buckets", [])),
                "boundary_role_count": len(payload.get("boundary_roles", [])),
                "top_files": [item.get("file", "") for item in payload.get("files", [])[:10]],
            }
        )

    rows.sort(
        key=lambda item: (
            -int(item.get("file_count", 0)),
            item.get("feature", ""),
        )
    )

    return rows[:limit]
