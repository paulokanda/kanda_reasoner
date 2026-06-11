"""Support static evidence collection for Project Reasoner."""

from __future__ import annotations

__all__ = [
    "PERSISTENCE_HINTS",
    "READ_HINTS",
    "WRITE_HINTS",
    "build_persistence_io_hotspots",
    "build_persistence_io_index",
    "build_persistence_io_summary",
]

from typing import Any


READ_HINTS = (
    "read",
    "load",
    "open",
    "from_json",
    "from_csv",
    "from_file",
    "loadtxt",
    "read_csv",
    "read_json",
    "read_excel",
    "read_hdf",
    "read_edf",
    "loadmat",
    "load_workbook",
)

WRITE_HINTS = (
    "write",
    "save",
    "dump",
    "export",
    "to_json",
    "to_csv",
    "to_excel",
    "to_hdf",
    "write_text",
    "write_bytes",
    "savefig",
    "to_parquet",
)

PERSISTENCE_HINTS = (
    "json",
    "csv",
    "excel",
    "xlsx",
    "hdf",
    "h5",
    "hdf5",
    "edf",
    "parquet",
    "yaml",
    "yml",
    "pickle",
    "pkl",
    "sqlite",
    "sql",
    "config",
    "settings",
    "cache",
    "file",
    "path",
    "folder",
    "directory",
)


def _safe_bucket_for_file(
    file_path: str,
    files_payload: list[dict[str, Any]],
) -> str:
    for record in files_payload:
        if str(record.get("path", "")) == file_path:
            bucket = str(record.get("subsystem_bucket", "")).strip()
            if bucket:
                return bucket
            break
    return "general"


def _safe_role_for_file(
    file_path: str,
    boundary_index: dict[str, dict[str, Any]],
) -> str:
    payload = boundary_index.get(file_path, {})
    if not isinstance(payload, dict):
        return "unclassified"
    return str(payload.get("boundary_role", "unclassified") or "unclassified")


def _safe_centrality_score(
    file_path: str,
    module_centrality_index: dict[str, dict[str, Any]],
) -> float:
    payload = module_centrality_index.get(file_path, {})
    if not isinstance(payload, dict):
        return 0.0

    for key in ("centrality_score", "score", "total_score"):
        value = payload.get(key)
        try:
            return float(value)
        except Exception:
            continue
    return 0.0


def _iter_symbols(file_record: dict[str, Any]) -> list[dict[str, Any]]:
    symbols: list[dict[str, Any]] = []

    for fn in file_record.get("functions", []):
        if isinstance(fn, dict):
            symbols.append(fn)

    for cls in file_record.get("classes", []):
        if not isinstance(cls, dict):
            continue
        for method in cls.get("methods", []):
            if isinstance(method, dict):
                symbols.append(method)

    return symbols


def _classify_call_name(call_name: str) -> tuple[bool, bool, bool]:
    lowered = call_name.lower()

    is_read = any(token in lowered for token in READ_HINTS)
    is_write = any(token in lowered for token in WRITE_HINTS)
    is_persistence = is_read or is_write or any(
        token in lowered for token in PERSISTENCE_HINTS
    )
    return is_read, is_write, is_persistence


def build_persistence_io_index(
    files_payload: list[dict[str, Any]],
    boundary_index: dict[str, dict[str, Any]],
    module_centrality_index: dict[str, dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    output: dict[str, dict[str, Any]] = {}

    for file_record in files_payload:
        file_path = str(file_record.get("path", "") or "")
        if not file_path:
            continue

        read_calls: list[str] = []
        write_calls: list[str] = []
        persistence_calls: list[str] = []
        touched_symbols: list[str] = []

        for symbol in _iter_symbols(file_record):
            symbol_name = str(symbol.get("qualname", symbol.get("name", "")) or "")
            if symbol_name:
                touched_symbols.append(symbol_name)

            for call in symbol.get("calls", []):
                if not isinstance(call, dict):
                    continue

                call_name = str(call.get("call_name", "") or "").strip()
                if not call_name:
                    continue

                is_read, is_write, is_persistence = _classify_call_name(call_name)

                if is_read:
                    read_calls.append(call_name)
                if is_write:
                    write_calls.append(call_name)
                if is_persistence:
                    persistence_calls.append(call_name)

        unique_read_calls = sorted(set(read_calls))
        unique_write_calls = sorted(set(write_calls))
        unique_persistence_calls = sorted(set(persistence_calls))
        centrality_score = _safe_centrality_score(file_path, module_centrality_index)

        persistence_score = (
            (len(read_calls) * 1.0)
            + (len(write_calls) * 1.5)
            + (len(unique_persistence_calls) * 2.0)
            + (3.0 if len(unique_write_calls) > 0 else 0.0)
            + (centrality_score * 0.5)
        )

        output[file_path] = {
            "file": file_path,
            "bucket": _safe_bucket_for_file(file_path, files_payload),
            "boundary_role": _safe_role_for_file(file_path, boundary_index),
            "centrality_score": centrality_score,
            "symbol_count": len(sorted(set(touched_symbols))),
            "read_call_count": len(read_calls),
            "write_call_count": len(write_calls),
            "persistence_call_count": len(persistence_calls),
            "unique_read_call_count": len(unique_read_calls),
            "unique_write_call_count": len(unique_write_calls),
            "unique_persistence_call_count": len(unique_persistence_calls),
            "sample_read_calls": unique_read_calls[:25],
            "sample_write_calls": unique_write_calls[:25],
            "sample_persistence_calls": unique_persistence_calls[:25],
            "persistence_score": round(persistence_score, 3),
            "is_persistence_owner_candidate": bool(
                len(unique_write_calls) >= 2
                or len(unique_persistence_calls) >= 4
                or len(write_calls) >= 5
            ),
            "is_read_heavy": bool(
                len(read_calls) > len(write_calls) and len(read_calls) >= 3
            ),
            "is_write_heavy": bool(
                len(write_calls) >= len(read_calls) and len(write_calls) >= 3
            ),
        }

    return dict(sorted(output.items()))


def build_persistence_io_summary(
    persistence_io_index: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    bucket_frequency: dict[str, int] = {}
    role_frequency: dict[str, int] = {}

    for file_path, payload in persistence_io_index.items():
        bucket = str(payload.get("bucket", "general") or "general")
        role = str(payload.get("boundary_role", "unclassified") or "unclassified")

        bucket_frequency[bucket] = bucket_frequency.get(bucket, 0) + 1
        role_frequency[role] = role_frequency.get(role, 0) + 1

        rows.append(
            {
                "file": file_path,
                "bucket": bucket,
                "boundary_role": role,
                "read_call_count": int(payload.get("read_call_count", 0)),
                "write_call_count": int(payload.get("write_call_count", 0)),
                "persistence_call_count": int(payload.get("persistence_call_count", 0)),
                "unique_persistence_call_count": int(
                    payload.get("unique_persistence_call_count", 0)
                ),
                "persistence_score": float(payload.get("persistence_score", 0.0)),
                "is_persistence_owner_candidate": bool(
                    payload.get("is_persistence_owner_candidate", False)
                ),
                "is_read_heavy": bool(payload.get("is_read_heavy", False)),
                "is_write_heavy": bool(payload.get("is_write_heavy", False)),
            }
        )

    rows.sort(
        key=lambda item: (
            -float(item.get("persistence_score", 0.0)),
            -int(item.get("write_call_count", 0)),
            -int(item.get("persistence_call_count", 0)),
            item.get("file", ""),
        )
    )

    persistence_owner_candidate_count = sum(
        1 for row in rows if bool(row.get("is_persistence_owner_candidate", False))
    )

    return {
        "file_count": len(rows),
        "persistence_owner_candidate_count": persistence_owner_candidate_count,
        "bucket_frequency": dict(sorted(bucket_frequency.items())),
        "role_frequency": dict(sorted(role_frequency.items())),
        "files": rows,
    }


def build_persistence_io_hotspots(
    persistence_io_index: dict[str, dict[str, Any]],
    limit: int = 25,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for file_path, payload in persistence_io_index.items():
        rows.append(
            {
                "file": file_path,
                "bucket": str(payload.get("bucket", "general") or "general"),
                "boundary_role": str(
                    payload.get("boundary_role", "unclassified") or "unclassified"
                ),
                "read_call_count": int(payload.get("read_call_count", 0)),
                "write_call_count": int(payload.get("write_call_count", 0)),
                "persistence_call_count": int(payload.get("persistence_call_count", 0)),
                "unique_persistence_call_count": int(
                    payload.get("unique_persistence_call_count", 0)
                ),
                "persistence_score": float(payload.get("persistence_score", 0.0)),
                "is_persistence_owner_candidate": bool(
                    payload.get("is_persistence_owner_candidate", False)
                ),
                "is_read_heavy": bool(payload.get("is_read_heavy", False)),
                "is_write_heavy": bool(payload.get("is_write_heavy", False)),
            }
        )

    rows.sort(
        key=lambda item: (
            -float(item.get("persistence_score", 0.0)),
            -int(item.get("write_call_count", 0)),
            -int(item.get("persistence_call_count", 0)),
            item.get("file", ""),
        )
    )

    return rows[:limit]
