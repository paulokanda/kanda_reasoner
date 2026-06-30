# project-path: kanda_reasoner_app/reasoner_context_collector/collector_edit_ready_source.py
"""Support static evidence collection for Project Reasoner."""

# =====================================================
# collector_edit_ready_source - Build edit-ready source indexes
# =====================================================

from __future__ import annotations

from typing import Any

from .collector_config import CollectorConfig
from .collector_utils import short_hash


def _infer_bucket_name(file_record: dict[str, Any]) -> str:
    """Support infer bucket name behavior.
    
    Parameters
    ----------
    file_record : dict[str, Any]
        The file record value.
    
    Returns
    -------
    str
        The string result.
    """
    
    path = str(file_record.get("path", "") or "").strip("/")
    module_name = str(file_record.get("module_name", "") or "").strip(".")

    if path:
        return path.split("/", 1)[0]

    if module_name:
        return module_name.split(".", 1)[0]

    return ""


def _truncate_source(source: str, max_chars: int) -> tuple[str, bool]:
    """Support truncate source behavior.
    
    Parameters
    ----------
    source : str
        The source value.
    max_chars : int
        The max chars value.
    
    Returns
    -------
    tuple[str, bool]
        The tuple of values.
    """
    
    if max_chars <= 0:
        return source, False

    if len(source) <= max_chars:
        return source, False

    return source[:max_chars], True


def _count_method_records(classes: list[dict[str, Any]]) -> int:
    """Support count method records behavior.
    
    Parameters
    ----------
    classes : list[dict[str, Any]]
        The classes value.
    
    Returns
    -------
    int
        The integer result.
    """
    
    total = 0

    for class_record in classes:
        total += len(class_record.get("methods", []))

    return total


def build_source_file_index(
    files_payload: list[dict[str, Any]],
    config: CollectorConfig,
) -> dict[str, dict[str, Any]]:
    """
    Build a file-level source index for edit-ready harvesting.

    This function is intentionally additive and read-only over files_payload.
    It does not walk the filesystem or mutate existing collector records.
    """
    if not config.enable_edit_ready_source_index:
        return {}

    source_file_index: dict[str, dict[str, Any]] = {}

    for file_record in files_payload:
        path = str(file_record.get("path", "") or "")
        module_name = str(file_record.get("module_name", "") or "")
        source = str(file_record.get("source", "") or "")

        classes = file_record.get("classes", [])
        functions = file_record.get("functions", [])

        class_count = len(classes)
        function_count = len(functions)
        method_count = _count_method_records(classes)
        symbol_count = class_count + function_count + method_count

        stored_source = ""
        source_truncated = False

        if config.include_full_source_in_file_index:
            stored_source, source_truncated = _truncate_source(
                source,
                config.max_full_source_chars,
            )

        source_file_index[path] = {
            "file": path,
            "module_name": module_name,
            "bucket": _infer_bucket_name(file_record),
            "sha12": short_hash(source),
            "line_count": len(source.splitlines()),
            "char_count": len(source),
            "has_source": bool(source),
            "full_source": stored_source,
            "source_truncated": source_truncated,
            "symbol_count": symbol_count,
            "class_count": class_count,
            "function_count": function_count,
            "method_count": method_count,
        }

    return source_file_index

def _slice_lines(
        lines: list[str],
        line_start: int,
        line_end: int,
) -> str:
    """Support slice lines behavior.
    
    Parameters
    ----------
    lines : list[str]
        The line values.
    line_start : int
        The line start value.
    line_end : int
        The line end value.
    
    Returns
    -------
    str
        The string result.
    """
    
    if not lines or line_start <= 0 or line_end <= 0 or line_end < line_start:
        return ""

    start_index = max(0, line_start - 1)
    end_index = min(len(lines), line_end)

    return "\n".join(lines[start_index:end_index])

def _collect_symbol_records(
        file_record: dict[str, Any],
) -> list[dict[str, Any]]:
    """Support collect symbol records behavior.
    
    Parameters
    ----------
    file_record : dict[str, Any]
        The file record value.
    
    Returns
    -------
    list[dict[str, Any]]
        The list of values.
    """
    
    records: list[dict[str, Any]] = []

    for function_record in file_record.get("functions", []):
        record = dict(function_record)
        record["_resolved_kind"] = record.get("symbol_kind") or "function"
        records.append(record)

    for class_record in file_record.get("classes", []):
        class_copy = dict(class_record)
        class_copy["_resolved_kind"] = class_copy.get("symbol_kind") or "class"
        records.append(class_copy)

        for method_record in class_record.get("methods", []):
            method_copy = dict(method_record)
            method_copy["_resolved_kind"] = method_copy.get("symbol_kind") or "method"
            records.append(method_copy)

    return records

def _build_symbol_excerpt_record(
        symbol_record: dict[str, Any],
        path: str,
        source: str,
        config: CollectorConfig,
) -> dict[str, Any]:
    """Support build symbol excerpt record behavior.
    
    Parameters
    ----------
    symbol_record : dict[str, Any]
        The symbol record value.
    path : str
        The file or folder path.
    source : str
        The source value.
    config : CollectorConfig
        The configuration data.
    
    Returns
    -------
    dict[str, Any]
        The mapped values.
    """
    
    lines = source.splitlines()

    symbol_name = str(
        symbol_record.get("qualname")
        or symbol_record.get("name")
        or ""
    )
    line_start = symbol_record.get("lineno")
    line_end = symbol_record.get("line_end")
    resolved_kind = str(symbol_record.get("_resolved_kind") or "unknown")
    parent_symbol = str(symbol_record.get("parent_symbol") or "")

    has_complete_span = bool(
        isinstance(line_start, int)
        and isinstance(line_end, int)
        and line_start > 0
        and line_end >= line_start
    )

    span_fallback_used = False

    if not isinstance(line_start, int) or line_start <= 0:
        line_start = 0

    if not isinstance(line_end, int) or line_end < line_start:
        line_end = line_start
        span_fallback_used = True

    if has_complete_span and config.max_source_excerpt_lines > 0:
        max_end = line_start + config.max_source_excerpt_lines - 1
        if line_end > max_end:
            line_end = max_end
            span_fallback_used = True

    source_excerpt = _slice_lines(lines, line_start, line_end)

    anchor_context = max(0, config.max_anchor_context_lines)

    if line_start > 0 and anchor_context > 0:
        anchor_above = _slice_lines(
            lines,
            max(1, line_start - anchor_context),
            line_start - 1,
        )
    else:
        anchor_above = ""

    if line_end > 0 and anchor_context > 0:
        anchor_below = _slice_lines(
            lines,
            line_end + 1,
            min(len(lines), line_end + anchor_context),
        )
    else:
        anchor_below = ""

    return {
        "symbol": symbol_name,
        "file": path,
        "kind": resolved_kind,
        "line_start": line_start,
        "line_end": line_end,
        "parent_symbol": parent_symbol,
        "source_sha12": short_hash(source),
        "symbol_sha12": short_hash(
            f"{path}|{symbol_name}|{line_start}|{line_end}|{resolved_kind}"
        ),
        "source_excerpt": source_excerpt,
        "anchor_above": anchor_above,
        "anchor_below": anchor_below,
        "excerpt_line_count": len(source_excerpt.splitlines()) if source_excerpt else 0,
        "has_complete_span": has_complete_span,
        "span_fallback_used": span_fallback_used,
    }

def build_edit_ready_symbol_index(
    files_payload: list[dict[str, Any]],
    config: CollectorConfig,
) -> dict[str, dict[str, Any]]:
    """
    Build a symbol-level source index using true symbol spans when available.

    This function is additive and read-only over files_payload.
    """
    if not config.enable_edit_ready_source_index:
        return {}

    symbol_index: dict[str, dict[str, Any]] = {}

    for file_record in files_payload:
        path = str(file_record.get("path", "") or "")
        source = str(file_record.get("source", "") or "")

        for symbol_record in _collect_symbol_records(file_record):
            symbol_name = str(
                symbol_record.get("qualname")
                or symbol_record.get("name")
                or ""
            )
            if not symbol_name:
                continue

            symbol_index[symbol_name] = _build_symbol_excerpt_record(
                symbol_record,
                path,
                source,
                config,
            )

    return symbol_index


def build_edit_ready_source_summary(
    source_file_index: dict[str, dict[str, Any]],
    edit_ready_symbol_index: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    """
    Build a compact summary for the edit-ready source harvesting layer.
    """
    file_count = len(source_file_index)
    symbol_count = len(edit_ready_symbol_index)

    class_count = 0
    function_count = 0
    method_count = 0
    anchored_symbol_count = 0
    fallback_symbol_count = 0
    max_symbol_excerpt_lines = 0

    files_with_full_source_count = sum(
        1
        for record in source_file_index.values()
        if bool(record.get("full_source"))
    )
    truncated_file_count = sum(
        1
        for record in source_file_index.values()
        if bool(record.get("source_truncated"))
    )

    for symbol_record in edit_ready_symbol_index.values():
        kind = str(symbol_record.get("kind") or "")

        if kind == "class":
            class_count += 1
        elif symbol_record.get("parent_symbol"):
            method_count += 1
        else:
            function_count += 1

        if symbol_record.get("source_excerpt"):
            anchored_symbol_count += 1

        if symbol_record.get("span_fallback_used"):
            fallback_symbol_count += 1

        excerpt_line_count = int(symbol_record.get("excerpt_line_count") or 0)
        if excerpt_line_count > max_symbol_excerpt_lines:
            max_symbol_excerpt_lines = excerpt_line_count

    return {
        "file_count": file_count,
        "symbol_count": symbol_count,
        "class_count": class_count,
        "function_count": function_count,
        "method_count": method_count,
        "files_with_full_source_count": files_with_full_source_count,
        "truncated_file_count": truncated_file_count,
        "anchored_symbol_count": anchored_symbol_count,
        "fallback_symbol_count": fallback_symbol_count,
        "max_symbol_excerpt_lines": max_symbol_excerpt_lines,
    }

def _format_numbered_snippet_block(
    line_start: int,
    anchor_above: str,
    source_excerpt: str,
    anchor_below: str,
    max_lines: int,
) -> str:
    """Support format numbered snippet block behavior.
    
    Parameters
    ----------
    line_start : int
        The line start value.
    anchor_above : str
        The anchor above value.
    source_excerpt : str
        The source excerpt value.
    anchor_below : str
        The anchor below value.
    max_lines : int
        The max lines value.
    
    Returns
    -------
    str
        The string result.
    """
    
    _ = anchor_below
    block_lines: list[tuple[int, str]] = []

    above_lines = anchor_above.splitlines() if anchor_above else []
    excerpt_lines = source_excerpt.splitlines() if source_excerpt else []

    above_start = max(1, line_start - len(above_lines))

    for offset, text in enumerate(above_lines):
        block_lines.append((above_start + offset, text))

    for offset, text in enumerate(excerpt_lines):
        block_lines.append((line_start + offset, text))

    if max_lines > 0 and len(block_lines) > max_lines:
        block_lines = block_lines[:max_lines]

    return "\n".join(
        f"{line_no:>5} | {text}"
        for line_no, text in block_lines
    )

def build_legacy_snippet_index_from_edit_ready(
        edit_ready_symbol_index: dict[str, dict[str, Any]],
        max_lines: int,
) -> dict[str, dict[str, Any]]:
    """
    Build the legacy snippet_index shape from validated edit-ready span records.

    This preserves the legacy output contract while upgrading snippets to use
    true line_start/line_end spans and excerpt/anchor content.
    """
    snippet_index: dict[str, dict[str, Any]] = {}

    for symbol, record in edit_ready_symbol_index.items():
        line_start = int(record.get("line_start") or 0)
        line_end = int(record.get("line_end") or line_start or 0)

        snippet_index[symbol] = {
            "file": str(record.get("file", "") or ""),
            "line_start": line_start,
            "line_end": line_end,
            "snippet": _format_numbered_snippet_block(
                line_start=line_start,
                anchor_above=str(record.get("anchor_above", "") or ""),
                source_excerpt=str(record.get("source_excerpt", "") or ""),
                anchor_below=str(record.get("anchor_below", "") or ""),
                max_lines=max_lines,
            ),
        }

    return snippet_index
