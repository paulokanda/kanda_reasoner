# project-path: kanda_reasoner_app/reasoner_context_collector/collector_active_code.py
"""Support static evidence collection for Project Reasoner."""

from __future__ import annotations

from typing import Any


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
    
    return str(value or "").strip()


def _safe_lower(value: Any) -> str:
    """Support safe lower behavior.
    
    Parameters
    ----------
    value : Any
        The input value.
    
    Returns
    -------
    str
        The string result.
    """
    
    return _safe_text(value).lower()


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


def _payload(mapping: dict[str, dict[str, Any]], file_path: str) -> dict[str, Any]:
    """Support payload behavior.
    
    Parameters
    ----------
    mapping : dict[str, dict[str, Any]]
        The mapping value.
    file_path : str
        The file path.
    
    Returns
    -------
    dict[str, Any]
        The mapped values.
    """
    
    value = mapping.get(file_path, {})
    if isinstance(value, dict):
        return value
    return {}


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
    
    return _safe_lower(file_record.get("subsystem_bucket", "")) or "general"


def _feature_count_by_file(
    feature_registry: dict[str, dict[str, Any]],
) -> dict[str, int]:
    """Support feature count by file behavior.
    
    Parameters
    ----------
    feature_registry : dict[str, dict[str, Any]]
        The feature registry value.
    
    Returns
    -------
    dict[str, int]
        The mapped values.
    """
    
    counts: dict[str, int] = {}

    for payload in feature_registry.values():
        if not isinstance(payload, dict):
            continue
        for item in payload.get("files", []):
            if not isinstance(item, dict):
                continue
            file_path = _safe_text(item.get("file", ""))
            if not file_path:
                continue
            counts[file_path] = counts.get(file_path, 0) + 1

    return counts


def build_active_code_index(
    files_payload: list[dict[str, Any]],
    change_impact_index: dict[str, dict[str, Any]],
    implementation_chronology_index: dict[str, dict[str, Any]],
    canonical_conflict_index: dict[str, dict[str, Any]],
    feature_registry: dict[str, dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    """Build a active code index.
    
    Parameters
    ----------
    files_payload : list[dict[str, Any]]
        The files payload value.
    change_impact_index : dict[str, dict[str, Any]]
        The change impact index value.
    implementation_chronology_index : dict[str, dict[str, Any]]
        The implementation chronology index value.
    canonical_conflict_index : dict[str, dict[str, Any]]
        The canonical conflict index value.
    feature_registry : dict[str, dict[str, Any]]
        The feature registry value.
    
    Returns
    -------
    dict[str, dict[str, Any]]
        The mapped values.
    """
    
    output: dict[str, dict[str, Any]] = {}
    feature_counts = _feature_count_by_file(feature_registry)

    for file_record in files_payload:
        file_path = _safe_text(file_record.get("path", ""))
        if not file_path:
            continue

        coverage_payload = file_record.get("coverage_metadata", {})
        if not isinstance(coverage_payload, dict):
            coverage_payload = {}

        coverage_value = 0.0
        for key in (
            "coverage_percent",
            "line_coverage",
            "coverage",
            "executed_percent",
        ):
            if key in coverage_payload:
                coverage_value = _safe_float(coverage_payload.get(key))
                break

        executed_lines = 0
        for key in ("executed_lines", "covered_lines", "lines_executed"):
            if key in coverage_payload:
                executed_lines = _safe_int(coverage_payload.get(key))
                break

        change_payload = _payload(change_impact_index, file_path)
        chronology_payload = _payload(implementation_chronology_index, file_path)
        canonical_payload = _payload(canonical_conflict_index, file_path)

        impact_score = _safe_float(change_payload.get("impact_score", 0.0))
        feature_count = _safe_int(feature_counts.get(file_path, 0))
        chronology_score = _safe_float(chronology_payload.get("chronology_score", 0.0))
        is_current_candidate = bool(chronology_payload.get("is_current_candidate", False))
        is_canonical_candidate = bool(canonical_payload.get("is_canonical_candidate", False))
        shadow_severity = _safe_float(canonical_payload.get("shadow_severity", 0.0))

        activity_score = (
            (coverage_value * 0.6)
            + (executed_lines * 0.2)
            + (impact_score * 0.6)
            + (feature_count * 1.5)
            + (chronology_score * 0.3)
            + (3.0 if is_current_candidate else 0.0)
            + (3.0 if is_canonical_candidate else 0.0)
            - (shadow_severity * 0.5)
        )

        activity_status = "present_but_weakly_evidenced"
        if coverage_value > 0 or executed_lines > 0:
            activity_status = "coverage_confirmed"
        elif impact_score >= 20.0 or (feature_count >= 2 and is_current_candidate):
            activity_status = "active_but_untested"
        elif is_canonical_candidate or chronology_score >= 8.0:
            activity_status = "likely_active"
        elif shadow_severity >= 4.0:
            activity_status = "likely_dormant"

        is_untested_critical = bool(
            activity_status in {"active_but_untested", "likely_active"}
            and (coverage_value <= 0 and executed_lines <= 0)
            and impact_score >= 20.0
        )

        output[file_path] = {
            "file": file_path,
            "bucket": _safe_bucket(file_record),
            "coverage_percent": round(coverage_value, 3),
            "executed_lines": executed_lines,
            "impact_score": round(impact_score, 3),
            "feature_count": feature_count,
            "chronology_score": round(chronology_score, 3),
            "is_current_candidate": is_current_candidate,
            "is_canonical_candidate": is_canonical_candidate,
            "shadow_severity": round(shadow_severity, 3),
            "activity_score": round(activity_score, 3),
            "activity_status": activity_status,
            "is_untested_critical": is_untested_critical,
            "is_coverage_confirmed": bool(coverage_value > 0 or executed_lines > 0),
        }

    return dict(sorted(output.items()))


def build_active_code_summary(
    active_code_index: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    """Build a active code summary.
    
    Parameters
    ----------
    active_code_index : dict[str, dict[str, Any]]
        The active code index value.
    
    Returns
    -------
    dict[str, Any]
        The mapped values.
    """
    
    rows: list[dict[str, Any]] = []
    status_frequency: dict[str, int] = {}
    coverage_confirmed_file_count = 0
    untested_critical_file_count = 0

    for file_path, payload in active_code_index.items():
        status = _safe_text(payload.get("activity_status", "")) or "unknown"
        status_frequency[status] = status_frequency.get(status, 0) + 1

        if bool(payload.get("is_coverage_confirmed", False)):
            coverage_confirmed_file_count += 1
        if bool(payload.get("is_untested_critical", False)):
            untested_critical_file_count += 1

        rows.append(
            {
                "file": file_path,
                "bucket": _safe_text(payload.get("bucket", "general")) or "general",
                "activity_status": status,
                "activity_score": _safe_float(payload.get("activity_score", 0.0)),
                "coverage_percent": _safe_float(payload.get("coverage_percent", 0.0)),
                "impact_score": _safe_float(payload.get("impact_score", 0.0)),
                "is_untested_critical": bool(payload.get("is_untested_critical", False)),
            }
        )

    rows.sort(
        key=lambda item: (
            -_safe_float(item.get("activity_score", 0.0)),
            item.get("file", ""),
        )
    )

    return {
        "file_count": len(rows),
        "coverage_confirmed_file_count": coverage_confirmed_file_count,
        "untested_critical_file_count": untested_critical_file_count,
        "status_frequency": dict(sorted(status_frequency.items())),
        "files": rows,
    }


def build_untested_critical_hotspots(
    active_code_index: dict[str, dict[str, Any]],
    limit: int = 25,
) -> list[dict[str, Any]]:
    """Build a untested critical hotspots.
    
    Parameters
    ----------
    active_code_index : dict[str, dict[str, Any]]
        The active code index value.
    limit : int, optional
        The optional limit value.
    
    Returns
    -------
    list[dict[str, Any]]
        The list of values.
    """
    
    rows: list[dict[str, Any]] = []

    for file_path, payload in active_code_index.items():
        if not bool(payload.get("is_untested_critical", False)):
            continue

        rows.append(
            {
                "file": file_path,
                "bucket": _safe_text(payload.get("bucket", "general")) or "general",
                "activity_status": _safe_text(payload.get("activity_status", "")),
                "activity_score": _safe_float(payload.get("activity_score", 0.0)),
                "coverage_percent": _safe_float(payload.get("coverage_percent", 0.0)),
                "executed_lines": _safe_int(payload.get("executed_lines", 0)),
                "impact_score": _safe_float(payload.get("impact_score", 0.0)),
                "feature_count": _safe_int(payload.get("feature_count", 0)),
            }
        )

    rows.sort(
        key=lambda item: (
            -_safe_float(item.get("activity_score", 0.0)),
            item.get("file", ""),
        )
    )

    return rows[:limit]
