"""Support static evidence collection for Project Reasoner."""

from __future__ import annotations

from typing import Any


def _safe_text(value: Any) -> str:
    return str(value or "").strip()


def _safe_lower(value: Any) -> str:
    return _safe_text(value).lower()


def _safe_float(value: Any) -> float:
    try:
        return float(value)
    except Exception:
        return 0.0


def _safe_int(value: Any) -> int:
    try:
        return int(value)
    except Exception:
        return 0


def _payload(mapping: dict[str, dict[str, Any]], file_path: str) -> dict[str, Any]:
    value = mapping.get(file_path, {})
    if isinstance(value, dict):
        return value
    return {}


def _safe_bucket(file_record: dict[str, Any]) -> str:
    return _safe_lower(file_record.get("subsystem_bucket", "")) or "general"


def build_change_impact_index(
    files_payload: list[dict[str, Any]],
    module_centrality_index: dict[str, dict[str, Any]],
    file_priority_index: dict[str, dict[str, Any]],
    boundary_violation_index: dict[str, dict[str, Any]],
    orchestration_index: dict[str, dict[str, Any]],
    state_mutation_index: dict[str, dict[str, Any]],
    persistence_io_index: dict[str, dict[str, Any]],
    event_propagation_index: dict[str, dict[str, Any]],
    canonical_conflict_index: dict[str, dict[str, Any]],
    responsibility_overlap_index: dict[str, dict[str, Any]],
    feature_registry: dict[str, dict[str, Any]],
    implementation_chronology_index: dict[str, dict[str, Any]],
    config_schema_registry: dict[str, dict[str, Any]],
    state_lifecycle_index: dict[str, dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    output: dict[str, dict[str, Any]] = {}

    feature_count_by_file: dict[str, int] = {}
    for payload in feature_registry.values():
        if not isinstance(payload, dict):
            continue
        for item in payload.get("files", []):
            if not isinstance(item, dict):
                continue
            file_path = _safe_text(item.get("file", ""))
            if not file_path:
                continue
            feature_count_by_file[file_path] = feature_count_by_file.get(file_path, 0) + 1

    for file_record in files_payload:
        file_path = _safe_text(file_record.get("path", ""))
        if not file_path:
            continue

        centrality_payload = _payload(module_centrality_index, file_path)
        priority_payload = _payload(file_priority_index, file_path)
        violation_payload = _payload(boundary_violation_index, file_path)
        orchestration_payload = _payload(orchestration_index, file_path)
        mutation_payload = _payload(state_mutation_index, file_path)
        persistence_payload = _payload(persistence_io_index, file_path)
        propagation_payload = _payload(event_propagation_index, file_path)
        canonical_payload = _payload(canonical_conflict_index, file_path)
        overlap_payload = _payload(responsibility_overlap_index, file_path)
        chronology_payload = _payload(implementation_chronology_index, file_path)
        schema_payload = _payload(config_schema_registry, file_path)
        lifecycle_payload = _payload(state_lifecycle_index, file_path)

        centrality_score = 0.0
        for key in ("centrality_score", "score", "total_score"):
            if key in centrality_payload:
                centrality_score = _safe_float(centrality_payload.get(key))
                break

        priority_score = 0.0
        for key in ("priority_score", "score", "total_score"):
            if key in priority_payload:
                priority_score = _safe_float(priority_payload.get(key))
                break

        violation_count = _safe_int(
            violation_payload.get("violation_count", violation_payload.get("count", 0))
        )
        orchestration_score = _safe_float(
            orchestration_payload.get("orchestration_score", 0.0)
        )
        state_like_target_count = _safe_int(
            mutation_payload.get("state_like_target_count", 0)
        )
        persistence_score = _safe_float(
            persistence_payload.get("persistence_score", 0.0)
        )
        propagation_score = _safe_float(
            propagation_payload.get("propagation_score", 0.0)
        )
        shadow_severity = _safe_float(canonical_payload.get("shadow_severity", 0.0))
        overlap_score = _safe_float(overlap_payload.get("max_overlap_score", 0.0))
        chronology_score = _safe_float(chronology_payload.get("chronology_score", 0.0))
        schema_term_count = _safe_int(schema_payload.get("schema_term_count", 0))
        lifecycle_score = _safe_float(lifecycle_payload.get("lifecycle_score", 0.0))
        feature_count = _safe_int(feature_count_by_file.get(file_path, 0))

        impact_score = (
            (centrality_score * 1.2)
            + (priority_score * 1.3)
            + (violation_count * 2.5)
            + (orchestration_score * 1.2)
            + (state_like_target_count * 1.8)
            + (persistence_score * 1.0)
            + (propagation_score * 1.0)
            + (overlap_score * 1.0)
            + (feature_count * 1.2)
            + (schema_term_count * 0.3)
            + (lifecycle_score * 0.8)
            + (chronology_score * 0.4)
            - (shadow_severity * 0.5)
        )

        is_high_risk = bool(
            impact_score >= 25.0
            or violation_count >= 2
            or (
                orchestration_score >= 8.0
                and state_like_target_count >= 2
            )
            or (
                persistence_score >= 8.0
                and propagation_score >= 8.0
            )
        )

        output[file_path] = {
            "file": file_path,
            "bucket": _safe_bucket(file_record),
            "impact_score": round(impact_score, 3),
            "centrality_score": round(centrality_score, 3),
            "priority_score": round(priority_score, 3),
            "violation_count": violation_count,
            "orchestration_score": round(orchestration_score, 3),
            "state_like_target_count": state_like_target_count,
            "persistence_score": round(persistence_score, 3),
            "propagation_score": round(propagation_score, 3),
            "overlap_score": round(overlap_score, 3),
            "feature_count": feature_count,
            "schema_term_count": schema_term_count,
            "lifecycle_score": round(lifecycle_score, 3),
            "chronology_score": round(chronology_score, 3),
            "shadow_severity": round(shadow_severity, 3),
            "is_high_risk_edit": is_high_risk,
        }

    return dict(sorted(output.items()))


def build_change_impact_summary(
    change_impact_index: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    high_risk_count = 0

    for file_path, payload in change_impact_index.items():
        is_high_risk = bool(payload.get("is_high_risk_edit", False))
        if is_high_risk:
            high_risk_count += 1

        rows.append(
            {
                "file": file_path,
                "bucket": _safe_text(payload.get("bucket", "general")) or "general",
                "impact_score": _safe_float(payload.get("impact_score", 0.0)),
                "violation_count": _safe_int(payload.get("violation_count", 0)),
                "feature_count": _safe_int(payload.get("feature_count", 0)),
                "schema_term_count": _safe_int(payload.get("schema_term_count", 0)),
                "is_high_risk_edit": is_high_risk,
            }
        )

    rows.sort(
        key=lambda item: (
            -_safe_float(item.get("impact_score", 0.0)),
            item.get("file", ""),
        )
    )

    return {
        "file_count": len(rows),
        "high_risk_edit_file_count": high_risk_count,
        "files": rows,
    }


def build_high_risk_edit_hotspots(
    change_impact_index: dict[str, dict[str, Any]],
    limit: int = 25,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for file_path, payload in change_impact_index.items():
        if not bool(payload.get("is_high_risk_edit", False)):
            continue

        rows.append(
            {
                "file": file_path,
                "bucket": _safe_text(payload.get("bucket", "general")) or "general",
                "impact_score": _safe_float(payload.get("impact_score", 0.0)),
                "centrality_score": _safe_float(payload.get("centrality_score", 0.0)),
                "priority_score": _safe_float(payload.get("priority_score", 0.0)),
                "violation_count": _safe_int(payload.get("violation_count", 0)),
                "orchestration_score": _safe_float(payload.get("orchestration_score", 0.0)),
                "persistence_score": _safe_float(payload.get("persistence_score", 0.0)),
                "propagation_score": _safe_float(payload.get("propagation_score", 0.0)),
                "lifecycle_score": _safe_float(payload.get("lifecycle_score", 0.0)),
            }
        )

    rows.sort(
        key=lambda item: (
            -_safe_float(item.get("impact_score", 0.0)),
            item.get("file", ""),
        )
    )

    return rows[:limit]