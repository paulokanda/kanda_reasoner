# project-path: kanda_reasoner_app/reasoner_context_collector/collector_bucket_insights.py
"""Support static evidence collection for Project Reasoner."""

from __future__ import annotations

from typing import Any


def _safe_float(value: Any) -> float:
    """Support safe float behavior.
    
    Parameters
    ----------
    value : Any
        The input value.
    
    Returns
    -------
    float
        The floating-point result.
    """
    
    try:
        return float(value)
    except Exception:
        return 0.0


def _safe_int(value: Any) -> int:
    """Support safe int behavior.
    
    Parameters
    ----------
    value : Any
        The input value.
    
    Returns
    -------
    int
        The integer result.
    """
    
    try:
        return int(value)
    except Exception:
        return 0


def build_bucket_hotspots(
    bucket_summary: dict[str, dict[str, Any]],
    module_centrality_index: dict[str, dict[str, Any]],
    limit: int = 10,
) -> list[dict[str, Any]]:
    """Build a bucket hotspots.
    
    Parameters
    ----------
    bucket_summary : dict[str, dict[str, Any]]
        The bucket summary value.
    module_centrality_index : dict[str, dict[str, Any]]
        The module centrality index value.
    limit : int, optional
        The optional limit value.
    
    Returns
    -------
    list[dict[str, Any]]
        The list of values.
    """
    
    rows: list[dict[str, Any]] = []

    for bucket_name, bucket_payload in bucket_summary.items():
        files = bucket_payload.get("files", [])
        centrality_values: list[float] = []

        for file_path in files:
            module_payload = module_centrality_index.get(file_path, {})
            centrality_values.append(
                _safe_float(module_payload.get("centrality_score", 0.0))
            )

        total_centrality = sum(centrality_values)
        average_centrality = (
            total_centrality / len(centrality_values)
            if centrality_values
            else 0.0
        )

        rows.append(
            {
                "bucket": bucket_name,
                "file_count": len(files),
                "total_centrality": round(total_centrality, 4),
                "average_centrality": round(average_centrality, 4),
            }
        )

    rows.sort(
        key=lambda item: (
            -_safe_float(item.get("total_centrality", 0.0)),
            -_safe_float(item.get("average_centrality", 0.0)),
            item.get("bucket", ""),
        )
    )
    return rows[:limit]


def build_bucket_priority_summary(
    bucket_summary: dict[str, dict[str, Any]],
    file_priority_index: dict[str, dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    """Build a bucket priority summary.
    
    Parameters
    ----------
    bucket_summary : dict[str, dict[str, Any]]
        The bucket summary value.
    file_priority_index : dict[str, dict[str, Any]]
        The file priority index value.
    
    Returns
    -------
    dict[str, dict[str, Any]]
        The mapped values.
    """
    
    output: dict[str, dict[str, Any]] = {}

    for bucket_name, bucket_payload in bucket_summary.items():
        files = bucket_payload.get("files", [])
        scores: list[float] = []

        for file_path in files:
            priority_payload = file_priority_index.get(file_path, {})
            scores.append(_safe_float(priority_payload.get("priority_score", 0.0)))

        output[bucket_name] = {
            "file_count": len(files),
            "total_priority_score": round(sum(scores), 4),
            "average_priority_score": round(
                (sum(scores) / len(scores)) if scores else 0.0,
                4,
            ),
            "top_files": sorted(
                files,
                key=lambda path: -_safe_float(
                    file_priority_index.get(path, {}).get("priority_score", 0.0)
                ),
            )[:10],
        }

    return dict(sorted(output.items()))


def build_bucket_warning_summary(
    bucket_summary: dict[str, dict[str, Any]],
    warning_index: dict[str, list[dict[str, Any]]],
) -> dict[str, dict[str, Any]]:
    """Build a bucket warning summary.
    
    Parameters
    ----------
    bucket_summary : dict[str, dict[str, Any]]
        The bucket summary value.
    warning_index : dict[str, list[dict[str, Any]]]
        The warning index value.
    
    Returns
    -------
    dict[str, dict[str, Any]]
        The mapped values.
    """
    
    output: dict[str, dict[str, Any]] = {}

    for bucket_name, bucket_payload in bucket_summary.items():
        files = bucket_payload.get("files", [])
        warning_count = 0
        files_with_warnings: list[str] = []

        for file_path in files:
            warning_items = warning_index.get(file_path, [])
            if warning_items:
                files_with_warnings.append(file_path)
                warning_count += len(warning_items)

        output[bucket_name] = {
            "file_count": len(files),
            "warning_file_count": len(files_with_warnings),
            "warning_count": warning_count,
            "files_with_warnings": sorted(files_with_warnings),
        }

    return dict(sorted(output.items()))


def build_bucket_insights(
    bucket_summary: dict[str, dict[str, Any]],
    module_centrality_index: dict[str, dict[str, Any]],
    file_priority_index: dict[str, dict[str, Any]],
    warning_index: dict[str, list[dict[str, Any]]],
) -> dict[str, Any]:
    """Build a bucket insights.
    
    Parameters
    ----------
    bucket_summary : dict[str, dict[str, Any]]
        The bucket summary value.
    module_centrality_index : dict[str, dict[str, Any]]
        The module centrality index value.
    file_priority_index : dict[str, dict[str, Any]]
        The file priority index value.
    warning_index : dict[str, list[dict[str, Any]]]
        The warning index value.
    
    Returns
    -------
    dict[str, Any]
        The mapped values.
    """
    
    bucket_hotspots = build_bucket_hotspots(
        bucket_summary,
        module_centrality_index,
        limit=10,
    )
    bucket_priority_summary = build_bucket_priority_summary(
        bucket_summary,
        file_priority_index,
    )
    bucket_warning_summary = build_bucket_warning_summary(
        bucket_summary,
        warning_index,
    )

    hottest_bucket = bucket_hotspots[0]["bucket"] if bucket_hotspots else ""
    noisiest_bucket = ""
    highest_warning_count = -1

    for bucket_name, payload in bucket_warning_summary.items():
        warning_count = _safe_int(payload.get("warning_count", 0))
        if warning_count > highest_warning_count:
            highest_warning_count = warning_count
            noisiest_bucket = bucket_name

    return {
        "bucket_hotspots": bucket_hotspots,
        "bucket_priority_summary": bucket_priority_summary,
        "bucket_warning_summary": bucket_warning_summary,
        "top_bucket_overview": {
            "hottest_bucket": hottest_bucket,
            "noisiest_bucket": noisiest_bucket,
        },
    }
