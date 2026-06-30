# project-path: kanda_reasoner_app/reasoner_context_collector/collector_buckets.py
"""Support static evidence collection for Project Reasoner."""

from __future__ import annotations

from typing import Any


def _lower_items(values: list[str]) -> list[str]:
    """Support lower items behavior.
    
    Parameters
    ----------
    values : list[str]
        The input values.
    
    Returns
    -------
    list[str]
        The list of values.
    """
    
    out: list[str] = []
    for value in values:
        if isinstance(value, str):
            out.append(value.lower())
    return out


def classify_file_bucket(file_record: dict[str, Any]) -> str:
    """Support classify file bucket behavior.
    
    Parameters
    ----------
    file_record : dict[str, Any]
        The file record value.
    
    Returns
    -------
    str
        The string result.
    """
    
    path = str(file_record.get("path", "")).lower()
    module_name = str(file_record.get("module_name", "")).lower()
    imports = _lower_items(file_record.get("imports", []))
    semantic_roles = _lower_items(file_record.get("semantic_roles", []))
    primary_role = str(file_record.get("primary_role", "")).lower()
    summary = str(file_record.get("summary", "")).lower()

    combined_text = " ".join(
        [
            path,
            module_name,
            " ".join(imports),
            " ".join(semantic_roles),
            primary_role,
            summary,
        ]
    )

    if "/tests/" in path or path.startswith("tests/") or module_name.endswith(".tests"):
        return "tests"

    if "legacy" in combined_text or "deprecated" in combined_text or "old_" in path:
        return "legacy"

    if "qt" in combined_text or "pyside" in combined_text or "ui" in semantic_roles:
        return "ui_qt"

    if "runtime" in combined_text or "trace" in combined_text or "monitor" in combined_text:
        return "runtime_tracing"

    if "collector" in combined_text or "reasoner" in combined_text or "index" in combined_text:
        return "collector_indexing"

    if "eeg" in combined_text or "neuro" in combined_text:
        return "eeg_domain"

    if "util" in combined_text or "config" in combined_text or "helper" in combined_text:
        return "infrastructure_utils"

    return "general"


def build_bucket_index(files_payload: list[dict[str, Any]]) -> dict[str, list[str]]:
    """Build a bucket index.
    
    Parameters
    ----------
    files_payload : list[dict[str, Any]]
        The files payload value.
    
    Returns
    -------
    dict[str, list[str]]
        The mapped values.
    """
    
    bucket_index: dict[str, list[str]] = {}

    for file_record in files_payload:
        path = str(file_record.get("path", ""))
        bucket = classify_file_bucket(file_record)
        file_record["subsystem_bucket"] = bucket

        if bucket not in bucket_index:
            bucket_index[bucket] = []
        bucket_index[bucket].append(path)

    for bucket_name in bucket_index:
        bucket_index[bucket_name] = sorted(set(bucket_index[bucket_name]))

    return dict(sorted(bucket_index.items()))


def build_bucket_summary(files_payload: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """Build a bucket summary.
    
    Parameters
    ----------
    files_payload : list[dict[str, Any]]
        The files payload value.
    
    Returns
    -------
    dict[str, dict[str, Any]]
        The mapped values.
    """
    
    summary: dict[str, dict[str, Any]] = {}

    for file_record in files_payload:
        bucket = str(file_record.get("subsystem_bucket") or classify_file_bucket(file_record))
        path = str(file_record.get("path", ""))
        primary_role = str(file_record.get("primary_role", ""))

        if bucket not in summary:
            summary[bucket] = {
                "file_count": 0,
                "files": [],
                "primary_roles": {},
            }

        summary[bucket]["file_count"] += 1
        summary[bucket]["files"].append(path)

        if primary_role:
            roles = summary[bucket]["primary_roles"]
            roles[primary_role] = roles.get(primary_role, 0) + 1

    for bucket_name, bucket_payload in summary.items():
        bucket_payload["files"] = sorted(set(bucket_payload["files"]))
        bucket_payload["primary_roles"] = dict(
            sorted(
                bucket_payload["primary_roles"].items(),
                key=lambda item: (-item[1], item[0]),
            )
        )

    return dict(sorted(summary.items()))
