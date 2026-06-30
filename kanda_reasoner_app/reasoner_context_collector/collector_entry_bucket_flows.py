# project-path: kanda_reasoner_app/reasoner_context_collector/collector_entry_bucket_flows.py
"""Support static evidence collection for Project Reasoner."""

from __future__ import annotations

from typing import Any


NOISE_BUCKETS = {"tests", "legacy"}


def _sorted_frequency_items(bucket_frequency: dict[str, int]) -> list[tuple[str, int]]:
    """Support sorted frequency items behavior.
    
    Parameters
    ----------
    bucket_frequency : dict[str, int]
        The bucket frequency value.
    
    Returns
    -------
    list[tuple[str, int]]
        The list of values.
    """
    
    return sorted(
        bucket_frequency.items(),
        key=lambda item: (-item[1], item[0]),
    )


def _pick_dominant_bucket(bucket_frequency: dict[str, int]) -> str:
    """Support pick dominant bucket behavior.
    
    Parameters
    ----------
    bucket_frequency : dict[str, int]
        The bucket frequency value.
    
    Returns
    -------
    str
        The string result.
    """
    
    if not bucket_frequency:
        return ""
    return _sorted_frequency_items(bucket_frequency)[0][0]


def _pick_dominant_bucket_clean(bucket_frequency: dict[str, int]) -> str:
    """Support pick dominant bucket clean behavior.
    
    Parameters
    ----------
    bucket_frequency : dict[str, int]
        The bucket frequency value.
    
    Returns
    -------
    str
        The string result.
    """
    
    clean_frequency = {
        bucket: count
        for bucket, count in bucket_frequency.items()
        if bucket not in NOISE_BUCKETS
    }
    if clean_frequency:
        return _pick_dominant_bucket(clean_frequency)
    return _pick_dominant_bucket(bucket_frequency)


def _safe_bucket_for_file(
    file_path: str,
    files_payload: list[dict[str, Any]],
) -> str:
    """Support safe bucket for file behavior.
    
    Parameters
    ----------
    file_path : str
        The file path.
    files_payload : list[dict[str, Any]]
        The files payload value.
    
    Returns
    -------
    str
        The string result.
    """
    
    for record in files_payload:
        if str(record.get("path", "")) == file_path:
            bucket = str(record.get("subsystem_bucket", "")).strip()
            if bucket:
                return bucket
            break
    return "general"


def _normalize_chain_step(step: Any) -> dict[str, Any]:
    """Support normalize chain step behavior.
    
    Parameters
    ----------
    step : Any
        The step value.
    
    Returns
    -------
    dict[str, Any]
        The mapped values.
    """
    
    if not isinstance(step, dict):
        return {}
    return {
        "file": str(step.get("file", "") or ""),
        "symbol": str(step.get("symbol", "") or ""),
        "line": step.get("line"),
        "step": step.get("step"),
        "why": str(step.get("why", "") or ""),
    }


def build_entry_bucket_flows(
    execution_chains: dict[str, Any],
    files_payload: list[dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    """Build a entry bucket flows.
    
    Parameters
    ----------
    execution_chains : dict[str, Any]
        The execution chains value.
    files_payload : list[dict[str, Any]]
        The files payload value.
    
    Returns
    -------
    dict[str, dict[str, Any]]
        The mapped values.
    """
    
    output: dict[str, dict[str, Any]] = {}

    for chain_name, raw_steps in execution_chains.items():
        steps = raw_steps if isinstance(raw_steps, list) else []

        bucket_sequence: list[str] = []
        bucket_frequency: dict[str, int] = {}
        file_sequence: list[str] = []
        unique_files: set[str] = set()

        for raw_step in steps:
            step = _normalize_chain_step(raw_step)
            file_path = step.get("file", "")
            if not file_path:
                continue

            unique_files.add(file_path)
            file_sequence.append(file_path)

            bucket = _safe_bucket_for_file(file_path, files_payload)

            if not bucket_sequence or bucket_sequence[-1] != bucket:
                bucket_sequence.append(bucket)

            bucket_frequency[bucket] = bucket_frequency.get(bucket, 0) + 1

        first_bucket = bucket_sequence[0] if bucket_sequence else ""
        dominant_bucket = _pick_dominant_bucket(bucket_frequency)
        dominant_bucket_clean = _pick_dominant_bucket_clean(bucket_frequency)
        noise_buckets_present = sorted(
            [bucket for bucket in bucket_frequency.keys() if bucket in NOISE_BUCKETS]
        )

        output[str(chain_name)] = {
            "chain_name": str(chain_name),
            "step_count": len(steps),
            "file_count": len(unique_files),
            "bucket_sequence": bucket_sequence,
            "unique_buckets": sorted(set(bucket_sequence)),
            "bucket_frequency": dict(
                sorted(
                    bucket_frequency.items(),
                    key=lambda item: (-item[1], item[0]),
                )
            ),
            "first_bucket": first_bucket,
            "dominant_bucket": dominant_bucket,
            "dominant_bucket_clean": dominant_bucket_clean,
            "noise_buckets_present": noise_buckets_present,
            "noise_bucket_count": len(noise_buckets_present),
            "first_file": file_sequence[0] if file_sequence else "",
            "sample_files": file_sequence[:15],
        }

    return dict(sorted(output.items()))


def build_entry_bucket_flow_summary(
    entry_bucket_flows: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    """Build a entry bucket flow summary.
    
    Parameters
    ----------
    entry_bucket_flows : dict[str, dict[str, Any]]
        The entry bucket flows value.
    
    Returns
    -------
    dict[str, Any]
        The mapped values.
    """
    
    summary_rows: list[dict[str, Any]] = []

    for chain_name, payload in entry_bucket_flows.items():
        summary_rows.append(
            {
                "chain_name": chain_name,
                "step_count": int(payload.get("step_count", 0)),
                "file_count": int(payload.get("file_count", 0)),
                "unique_bucket_count": len(payload.get("unique_buckets", [])),
                "first_bucket": str(payload.get("first_bucket", "")),
                "dominant_bucket": str(payload.get("dominant_bucket", "")),
                "dominant_bucket_clean": str(payload.get("dominant_bucket_clean", "")),
                "first_file": str(payload.get("first_file", "")),
                "noise_buckets_present": payload.get("noise_buckets_present", []),
                "noise_bucket_count": int(payload.get("noise_bucket_count", 0)),
                "unique_buckets": payload.get("unique_buckets", []),
            }
        )

    summary_rows.sort(
        key=lambda item: (
            -int(item.get("step_count", 0)),
            -int(item.get("unique_bucket_count", 0)),
            int(item.get("noise_bucket_count", 0)),
            item.get("chain_name", ""),
        )
    )

    return {
        "entry_count": len(summary_rows),
        "entries": summary_rows,
    }
