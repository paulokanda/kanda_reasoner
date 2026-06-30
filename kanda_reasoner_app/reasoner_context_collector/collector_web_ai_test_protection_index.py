# project-path: kanda_reasoner_app/reasoner_context_collector/collector_web_ai_test_protection_index.py
"""Build web-AI test protection records for Project Reasoner.

This module creates an additive test-protection index that helps web AI answer
which tests protect a file, symbol, or behavior.

It consumes existing collector data and does not replace test_links, files,
symbol_index, web_ai_symbol_index, primary_definition_index, or file
responsibility records.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

__all__ = [
    "build_web_ai_test_protection_index",
    "build_web_ai_test_protection_summary",
]


def _safe_text(value: Any) -> str:
    """Return a safe stripped string."""
    return str(value or "").strip()


def _normalize_path(value: Any) -> str:
    """Normalize file paths to forward slashes."""
    text = _safe_text(value).replace("\\", "/")
    while "//" in text:
        text = text.replace("//", "/")
    return text.strip("/")


def _stem(path: str) -> str:
    """Return lowercase file stem."""
    return Path(_normalize_path(path)).stem.lower()


def _module_from_path(path: str) -> str:
    """Return a dotted module-like string from a project-relative path."""
    normalized = _normalize_path(path)
    if normalized.endswith(".py"):
        normalized = normalized[:-3]
    return normalized.replace("/", ".")


def _is_test_path(path: str) -> bool:
    """Return True if a path appears to be a Python test file."""
    normalized = "/" + _normalize_path(path).lower().lstrip("/")
    name = normalized.rsplit("/", 1)[-1]
    return "/tests/" in normalized or name.startswith("test_") or name.endswith("_test.py")


def _iter_symbols(file_record: dict[str, Any]) -> list[str]:
    """Return function/class/method names from one file record."""
    names: list[str] = []

    for function_record in file_record.get("functions", []):
        if isinstance(function_record, dict):
            names.append(_safe_text(function_record.get("name", "")))
            names.append(_safe_text(function_record.get("qualname", "")))

    for class_record in file_record.get("classes", []):
        if not isinstance(class_record, dict):
            continue

        names.append(_safe_text(class_record.get("name", "")))
        names.append(_safe_text(class_record.get("qualname", "")))

        for method_record in class_record.get("methods", []):
            if isinstance(method_record, dict):
                names.append(_safe_text(method_record.get("name", "")))
                names.append(_safe_text(method_record.get("qualname", "")))

    return [name for name in names if name]


def _file_text_blob(file_record: dict[str, Any]) -> str:
    """Build a lowercase text blob from already-collected metadata."""
    strings = file_record.get("strings", [])
    if not isinstance(strings, list):
        strings = []
    comments = file_record.get("comments", [])
    if not isinstance(comments, list):
        comments = []
    imports = file_record.get("imports", [])
    if not isinstance(imports, list):
        imports = []

    parts = [
        file_record.get("path", ""),
        file_record.get("module_name", ""),
        file_record.get("docstring", ""),
        " ".join(imports[:80]),
        " ".join(strings[:80]),
        " ".join(comments[:80]),
        " ".join(_iter_symbols(file_record)),
        file_record.get("source", "")[:12000],
    ]
    return " ".join(_safe_text(item) for item in parts).lower()


def _symbols_for_source(
    source_path: str,
    web_ai_symbol_index: dict[str, dict[str, Any]],
) -> list[str]:
    """Return symbols belonging to one source file."""
    normalized = _normalize_path(source_path)
    symbols: list[str] = []

    for symbol_name, record in web_ai_symbol_index.items():
        if not isinstance(record, dict):
            continue
        if _normalize_path(record.get("file", "")) != normalized:
            continue

        for value in (
            record.get("symbol", ""),
            record.get("qualified_name", ""),
            symbol_name,
        ):
            text = _safe_text(value)
            if text:
                symbols.append(text)
                symbols.append(text.split(".")[-1])

    return sorted(set(item for item in symbols if item))


def _existing_test_link_map(test_links: list[dict[str, Any]]) -> dict[str, set[str]]:
    """Return source path to linked test paths from existing test_links."""
    mapping: dict[str, set[str]] = {}

    for item in test_links:
        if not isinstance(item, dict):
            continue

        source = _normalize_path(item.get("source_file", ""))
        if not source:
            continue

        raw_tests = item.get("linked_tests", [])
        if not isinstance(raw_tests, list):
            continue

        for test_path in raw_tests:
            normalized_test = _normalize_path(test_path)
            if normalized_test:
                mapping.setdefault(source, set()).add(normalized_test)

    return mapping


def _score_test_link(
    *,
    source_path: str,
    source_module: str,
    source_symbols: list[str],
    test_path: str,
    test_record: dict[str, Any],
    linked_by_existing_test_links: bool,
) -> tuple[float, list[str], list[str]]:
    """Score whether a test file protects a source file."""
    test_blob = _file_text_blob(test_record)
    source_stem = _stem(source_path)
    test_stem = _stem(test_path)
    source_module_lower = source_module.lower()
    source_path_lower = _normalize_path(source_path).lower()

    score = 0.0
    reasons: list[str] = []
    matched_symbols: list[str] = []

    if linked_by_existing_test_links:
        score += 3.0
        reasons.append("existing_test_links")

    if source_stem and source_stem in test_stem:
        score += 2.0
        reasons.append("test_filename_matches_source_stem")

    if source_module_lower and source_module_lower in test_blob:
        score += 4.0
        reasons.append("test_references_source_module")

    if source_path_lower and source_path_lower in test_blob:
        score += 4.0
        reasons.append("test_references_source_path")

    symbol_score_count = 0
    for symbol in source_symbols:
        symbol_text = _safe_text(symbol)
        if not symbol_text:
            continue
        if symbol_text.lower() in test_blob:
            if symbol_score_count < 6:
                score += 1.5
                symbol_score_count += 1
            reasons.append("test_references_symbol")
            matched_symbols.append(symbol_text)

    # Being located in a tests folder is only supporting evidence, not a link by
    # itself. Add this boost only after a real source/test relationship exists.
    if reasons and "/tests/" in ("/" + _normalize_path(test_path).lower().lstrip("/")):
        score += 0.5
        reasons.append("test_folder")

    if not reasons:
        return 0.0, [], []

    return round(score, 3), sorted(set(reasons)), sorted(set(matched_symbols))[:8]


def _confidence_from_score(score: float) -> float:
    """Convert score into stable confidence."""
    if score >= 7.0:
        return 0.95
    if score >= 5.0:
        return 0.9
    if score >= 3.0:
        return 0.75
    return 0.6


def _reason_from_parts(parts: list[str]) -> str:
    """Return compact reason string."""
    if not parts:
        return "weak_test_link"
    return "_and_".join(parts[:5])


def build_web_ai_test_protection_summary(
    web_ai_test_protection_index: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    """Build compact summary for web_ai_test_protection_index."""
    protected_count = 0
    unprotected_count = 0
    confidence_frequency: dict[str, int] = {}

    for record in web_ai_test_protection_index.values():
        linked_tests = record.get("linked_tests", [])
        if isinstance(linked_tests, list) and linked_tests:
            protected_count += 1
            for item in linked_tests:
                if not isinstance(item, dict):
                    continue
                label = str(item.get("confidence", "unknown"))
                confidence_frequency[label] = confidence_frequency.get(label, 0) + 1
        else:
            unprotected_count += 1

    return {
        "source_file_count": len(web_ai_test_protection_index),
        "protected_source_file_count": protected_count,
        "unprotected_source_file_count": unprotected_count,
        "test_link_confidence_frequency": dict(sorted(confidence_frequency.items())),
    }


def build_web_ai_test_protection_index(
    files_payload: list[dict[str, Any]],
    test_links: list[dict[str, Any]],
    web_ai_symbol_index: dict[str, dict[str, Any]],
    web_ai_file_responsibility_index: dict[str, dict[str, Any]],
    *,
    enabled: bool = True,
) -> dict[str, dict[str, Any]]:
    """Build additive web-AI test protection records."""
    if not enabled:
        return {}

    files_by_path: dict[str, dict[str, Any]] = {}
    test_files: dict[str, dict[str, Any]] = {}

    for file_record in files_payload:
        if not isinstance(file_record, dict):
            continue
        path = _normalize_path(file_record.get("path", ""))
        if not path:
            continue
        files_by_path[path] = file_record
        if _is_test_path(path):
            test_files[path] = file_record

    existing_links = _existing_test_link_map(test_links)
    output: dict[str, dict[str, Any]] = {}

    for source_path, source_record in sorted(files_by_path.items()):
        if source_path in test_files:
            continue

        source_module = (
            _safe_text(source_record.get("module_name", ""))
            or _module_from_path(source_path)
        )
        source_symbols = _symbols_for_source(source_path, web_ai_symbol_index)
        if not source_symbols:
            source_symbols = _iter_symbols(source_record)

        linked_tests: list[dict[str, Any]] = []
        candidates = set(test_files.keys()) | existing_links.get(source_path, set())

        for test_path in sorted(candidates):
            test_record = files_by_path.get(test_path, {"path": test_path})
            score, reason_parts, matched_symbols = _score_test_link(
                source_path=source_path,
                source_module=source_module,
                source_symbols=source_symbols,
                test_path=test_path,
                test_record=test_record,
                linked_by_existing_test_links=test_path in existing_links.get(source_path, set()),
            )
            if score <= 0:
                continue

            linked_tests.append(
                {
                    "test_file": test_path,
                    "confidence": _confidence_from_score(score),
                    "score": score,
                    "reason": _reason_from_parts(reason_parts),
                    "reason_parts": reason_parts,
                    "matched_symbols": matched_symbols,
                }
            )

        linked_tests.sort(
            key=lambda item: (
                -float(item.get("confidence", 0.0)),
                -float(item.get("score", 0.0)),
                str(item.get("test_file", "")),
            )
        )

        responsibility = web_ai_file_responsibility_index.get(source_path, {})
        if not isinstance(responsibility, dict):
            responsibility = {}

        output[source_path] = {
            "source_file": source_path,
            "owner_box": _safe_text(responsibility.get("owner_box", "")),
            "primary_responsibility": _safe_text(
                responsibility.get("primary_responsibility", "")
            ),
            "important_symbols": source_symbols[:12],
            "linked_tests": linked_tests,
            "linked_test_count": len(linked_tests),
            "is_protected_by_tests": bool(linked_tests),
            "source_index": "web_ai_test_protection_index",
        }

    return dict(sorted(output.items()))
