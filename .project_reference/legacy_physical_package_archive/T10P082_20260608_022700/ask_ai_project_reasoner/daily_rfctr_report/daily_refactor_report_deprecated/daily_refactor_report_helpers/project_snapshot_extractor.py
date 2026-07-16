"""
Project Snapshot Extractor - v1.1 (App-Level Shared)
====================================================

Purpose
-------
This module provides a read-only, deterministic structural snapshot of a
selected "domain root" (e.g., Tab1 or Tab3 folder).

It is designed to be called by the app-level engine:
    dev_tools/daily_refactor_report_engine.py

The snapshot is saved under:
    <domain_structural_state_reports>/derived/<prefix>_project_snapshot.json

What it measures (safe, fast, deterministic)
--------------------------------------------
- python_file_count
- module_count (same as python_file_count, kept for clarity)
- total_lines
- avg_lines_per_module
- max_module_size_lines
- ast_node_count_total
- avg_ast_nodes_per_module
- parse_error_count (how many files failed AST parse)
- read_error_count (how many files failed to read)

Non-goals (deliberately excluded for stability)
-----------------------------------------------
- No dependency graph extraction (later step)
- No call graph extraction (later step)
- No writes outside derived snapshot path
- No mutation of your canonical state vector or histories

Usage
-----
Call extract_project_snapshot(domain_root, output_path, prefix)

Where:
- domain_root: Path to tab1_ai_code_refiner OR tab3_memory_map
- output_path: Path to .../structural_state_reports/derived/<prefix>_project_snapshot.json
- prefix: "tab1" or "tab3"
"""

from __future__ import annotations

import ast
import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, Any


@dataclass(frozen=True)
class SnapshotResult:
    snapshot: Dict[str, Any]
    output_path: Path


def _safe_read_text(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return None


def _count_lines(text: str) -> int:
    # Deterministic newline count (works for files without trailing newline)
    if not text:
        return 0
    return text.count("\n") + 1


def _count_ast_nodes(text: str) -> int | None:
    try:
        tree = ast.parse(text)
        return sum(1 for _ in ast.walk(tree))
    except Exception:
        return None


def extract_project_snapshot(domain_root: Path, output_path: Path, prefix: str) -> SnapshotResult:
    if not domain_root.exists() or not domain_root.is_dir():
        raise ValueError(f"domain_root must be an existing directory: {domain_root}")

    py_files = list(domain_root.rglob("*.py"))

    module_count = 0
    total_lines = 0
    max_module_size_lines = 0

    ast_nodes_total = 0
    parse_error_count = 0
    read_error_count = 0

    for file_path in py_files:
        text = _safe_read_text(file_path)
        if text is None:
            read_error_count += 1
            continue

        module_count += 1
        lines = _count_lines(text)
        total_lines += lines
        if lines > max_module_size_lines:
            max_module_size_lines = lines

        ast_nodes = _count_ast_nodes(text)
        if ast_nodes is None:
            parse_error_count += 1
        else:
            ast_nodes_total += ast_nodes

    snapshot = {
        "snapshot_version": "1.1",
        "domain_prefix": prefix,
        "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "domain_root": str(domain_root),
        "python_file_count": len(py_files),
        "module_count": module_count,
        "total_lines": total_lines,
        "avg_lines_per_module": round(total_lines / module_count, 2) if module_count else 0.0,
        "max_module_size_lines": max_module_size_lines,
        "ast_node_count_total": ast_nodes_total,
        "avg_ast_nodes_per_module": round(ast_nodes_total / module_count, 2) if module_count else 0.0,
        "parse_error_count": parse_error_count,
        "read_error_count": read_error_count,
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(snapshot, f, indent=4, sort_keys=True)

    return SnapshotResult(snapshot=snapshot, output_path=output_path)