# project-path: kanda_reasoner_app/reasoner_context_collector/collector_web_ai_file_responsibility_index.py
"""Build web-AI file responsibility records for Project Reasoner.

This module creates an additive file-level responsibility index for web AI. It
uses existing collector data such as file records, web_ai_symbol_index,
primary_definition_index, and entry_points_detail.

It does not replace files, symbol_index, web_ai_symbol_index,
primary_definition_index, entry_points_detail, or any existing collector output.
"""

from __future__ import annotations

from typing import Any

__all__ = [
    "build_web_ai_file_responsibility_index",
    "build_web_ai_file_responsibility_summary",
]


BOX_RULES = (
    (
        "Prompt Builder Box",
        ("prompt_builder", "prompt construction", "evidence-grounded prompt"),
    ),
    (
        "Retrieval Box",
        ("retriever", "retrieval", "evidence bundle"),
    ),
    (
        "AI Bridge Box",
        ("ai_bridge", "local ai", "model answer"),
    ),
    (
        "AI Bridge Grounding Box",
        ("grounding", "forbidden_paths", "insufficient_evidence"),
    ),
    (
        "AI Bridge Deterministic Answer Box",
        ("deterministic", "deterministic answer", "fast path"),
    ),
    (
        "Step 4 Collector Box",
        ("data_collector", "collector", "collect project structure"),
    ),
    (
        "JSON Splitter Box",
        ("json_splitter", "splitter", "split json"),
    ),
    (
        "V10 GUI Box",
        ("main_window", "ui_builder", "runtime_controller", "signal_wiring"),
    ),
    (
        "Live Source Verification Box",
        ("live_source_verification", "verify live source", "snippet extracted"),
    ),
    (
        "Local-AI JSON Working Copy Box",
        ("local_ai_json_working_copy", "working copy", "local-ai copy"),
    ),
    (
        "Local-AI JSON Enrichment Box",
        ("local_ai_json_enrichment", "enrichment", "local_ai_enrichment"),
    ),
)


def _safe_text(value: Any) -> str:
    """Return a safe stripped string."""
    return str(value or "").strip()


def _normalize_path(value: Any) -> str:
    """Normalize file paths to forward slashes."""
    text = _safe_text(value).replace("\\", "/")
    while "//" in text:
        text = text.replace("//", "/")
    return text.strip("/")


def _first_line(value: Any) -> str:
    """Return the first non-empty line from a string."""
    for line in _safe_text(value).splitlines():
        stripped = line.strip()
        if stripped:
            return stripped
    return ""


def _iter_file_symbols(file_record: dict[str, Any]) -> list[str]:
    """Return symbol names collected for one file."""
    names: list[str] = []

    for function_record in file_record.get("functions", []):
        if isinstance(function_record, dict):
            names.append(_safe_text(function_record.get("qualname") or function_record.get("name")))

    for class_record in file_record.get("classes", []):
        if not isinstance(class_record, dict):
            continue
        names.append(_safe_text(class_record.get("qualname") or class_record.get("name")))
        for method_record in class_record.get("methods", []):
            if isinstance(method_record, dict):
                names.append(_safe_text(method_record.get("qualname") or method_record.get("name")))

    return [name for name in names if name]


def _file_blob(
    file_path: str,
    file_record: dict[str, Any],
    symbols: list[str],
) -> str:
    """Build a lowercase responsibility search blob."""
    strings = file_record.get("strings", [])
    if not isinstance(strings, list):
        strings = []
    comments = file_record.get("comments", [])
    if not isinstance(comments, list):
        comments = []

    parts = [
        file_path,
        file_record.get("module_name", ""),
        file_record.get("docstring", ""),
        " ".join(strings[:40]),
        " ".join(comments[:40]),
        " ".join(symbols[:40]),
    ]
    return " ".join(_safe_text(item) for item in parts).lower()


def _infer_box(file_path: str, blob: str) -> tuple[str, str]:
    """Infer a conservative owner box from path and source hints."""
    normalized = _normalize_path(file_path).lower()
    combined = normalized + " " + blob

    best_box = "Unclassified Box"
    best_score = 0
    best_reason = "no_box_rule_match"

    for box_name, markers in BOX_RULES:
        score = 0
        matched: list[str] = []
        for marker in markers:
            if marker in combined:
                score += 1
                matched.append(marker)
        if score > best_score:
            best_box = box_name
            best_score = score
            best_reason = "matched_" + "_and_".join(matched[:3])

    return best_box, best_reason


def _responsibility_from_docstring(file_record: dict[str, Any]) -> tuple[str, str, str]:
    """Return responsibility summary from source-derived docstring if present."""
    docstring = _first_line(file_record.get("docstring", ""))
    if docstring:
        return docstring.rstrip("."), "module_docstring", "high"
    return "", "", ""


def _responsibility_from_symbols(
    file_path: str,
    web_ai_symbol_index: dict[str, dict[str, Any]],
) -> tuple[str, str, str, list[str]]:
    """Infer file responsibility from high-confidence symbol docstrings."""
    normalized = _normalize_path(file_path)
    candidates: list[dict[str, Any]] = []

    for symbol_name, record in web_ai_symbol_index.items():
        if not isinstance(record, dict):
            continue
        if _normalize_path(record.get("file", "")) != normalized:
            continue
        doc = _first_line(record.get("docstring_first_line", ""))
        if not doc:
            continue
        confidence = _safe_text(record.get("confidence", ""))
        kind = _safe_text(record.get("kind", ""))
        line_start = int(record.get("line_start", 0) or 0)
        score = 0
        if confidence == "high":
            score += 4
        elif confidence == "medium":
            score += 2
        if kind == "class":
            score += 3
        elif kind == "function":
            score += 2
        elif kind == "method":
            score += 1
        if line_start:
            score += max(0, 2 - min(line_start, 200) // 100)

        candidates.append(
            {
                "symbol": _safe_text(record.get("symbol", symbol_name)),
                "doc": doc.rstrip("."),
                "score": score,
                "line_start": line_start,
            }
        )

    candidates.sort(
        key=lambda item: (
            -int(item.get("score", 0)),
            int(item.get("line_start", 0)),
            str(item.get("symbol", "")),
        )
    )

    important = [str(item["symbol"]) for item in candidates[:8]]
    if candidates:
        return candidates[0]["doc"], "symbol_docstring", "high", important
    return "", "", "", important


def _responsibility_from_path(file_path: str) -> tuple[str, str, str]:
    """Return low-confidence path-derived responsibility fallback."""
    normalized = _normalize_path(file_path)
    basename = normalized.rsplit("/", 1)[-1]
    stem = basename.rsplit(".", 1)[0]
    if not stem:
        return "", "", ""

    phrase = stem.replace("_", " ").replace("-", " ").strip()
    if not phrase:
        return "", "", ""

    return "Support " + phrase, "path_heuristic", "low"


def _entry_detail_for_file(
    file_path: str,
    entry_points_detail: list[dict[str, Any]],
) -> dict[str, Any] | None:
    """Return entry detail record for a file if present."""
    normalized = _normalize_path(file_path)
    for item in entry_points_detail:
        if isinstance(item, dict) and _normalize_path(item.get("path", "")) == normalized:
            return item
    return None


def _symbols_for_file_from_index(
    file_path: str,
    web_ai_symbol_index: dict[str, dict[str, Any]],
) -> list[str]:
    """Return important symbols for one file from web_ai_symbol_index."""
    normalized = _normalize_path(file_path)
    rows: list[tuple[int, str]] = []
    for symbol, record in web_ai_symbol_index.items():
        if not isinstance(record, dict):
            continue
        if _normalize_path(record.get("file", "")) != normalized:
            continue
        rows.append((int(record.get("line_start", 0) or 0), _safe_text(record.get("symbol", symbol))))
    return [symbol for _line, symbol in sorted(rows) if symbol][:12]


def build_web_ai_file_responsibility_summary(
    web_ai_file_responsibility_index: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    """Build compact summary for web_ai_file_responsibility_index."""
    box_frequency: dict[str, int] = {}
    confidence_frequency: dict[str, int] = {}
    source_frequency: dict[str, int] = {}

    for record in web_ai_file_responsibility_index.values():
        box = _safe_text(record.get("owner_box", "")) or "unknown"
        confidence = _safe_text(record.get("confidence", "")) or "unknown"
        source = _safe_text(record.get("responsibility_source", "")) or "unknown"

        box_frequency[box] = box_frequency.get(box, 0) + 1
        confidence_frequency[confidence] = confidence_frequency.get(confidence, 0) + 1
        source_frequency[source] = source_frequency.get(source, 0) + 1

    return {
        "file_responsibility_count": len(web_ai_file_responsibility_index),
        "box_frequency": dict(sorted(box_frequency.items())),
        "confidence_frequency": dict(sorted(confidence_frequency.items())),
        "responsibility_source_frequency": dict(sorted(source_frequency.items())),
    }


def build_web_ai_file_responsibility_index(
    files_payload: list[dict[str, Any]],
    web_ai_symbol_index: dict[str, dict[str, Any]],
    primary_definition_index: dict[str, dict[str, Any]],
    entry_points_detail: list[dict[str, Any]],
    *,
    enabled: bool = True,
) -> dict[str, dict[str, Any]]:
    """Build additive file-level responsibility records for web AI."""
    if not enabled:
        return {}

    primary_files: dict[str, list[str]] = {}
    for symbol, payload in primary_definition_index.items():
        if not isinstance(payload, dict):
            continue
        primary = payload.get("primary", {})
        if not isinstance(primary, dict):
            continue
        path = _normalize_path(primary.get("file", ""))
        if path:
            primary_files.setdefault(path, []).append(_safe_text(symbol))

    output: dict[str, dict[str, Any]] = {}

    for file_record in files_payload:
        if not isinstance(file_record, dict):
            continue

        file_path = _normalize_path(file_record.get("path", ""))
        if not file_path:
            continue

        collected_symbols = _iter_file_symbols(file_record)
        blob = _file_blob(file_path, file_record, collected_symbols)
        owner_box, owner_reason = _infer_box(file_path, blob)

        responsibility, source, confidence = _responsibility_from_docstring(file_record)
        important_symbols = _symbols_for_file_from_index(file_path, web_ai_symbol_index)
        if not responsibility:
            responsibility, source, confidence, symbol_docs = _responsibility_from_symbols(
                file_path,
                web_ai_symbol_index,
            )
            if symbol_docs and not important_symbols:
                important_symbols = symbol_docs

        if not responsibility:
            responsibility, source, confidence = _responsibility_from_path(file_path)

        entry_detail = _entry_detail_for_file(file_path, entry_points_detail)
        is_entry_point = entry_detail is not None
        entry_role = _safe_text(entry_detail.get("role", "")) if entry_detail else ""

        record = {
            "file": file_path,
            "module_name": _safe_text(file_record.get("module_name", "")),
            "owner_box": owner_box,
            "owner_reason": owner_reason,
            "primary_responsibility": responsibility,
            "responsibility_source": source,
            "confidence": confidence,
            "source_truth": "source_derived" if source in {"module_docstring", "symbol_docstring"} else "heuristic",
            "is_entry_point": is_entry_point,
            "entry_role": entry_role,
            "important_symbols": important_symbols or collected_symbols[:12],
            "primary_symbols": sorted(primary_files.get(file_path, [])),
        }
        output[file_path] = record

    return dict(sorted(output.items()))
