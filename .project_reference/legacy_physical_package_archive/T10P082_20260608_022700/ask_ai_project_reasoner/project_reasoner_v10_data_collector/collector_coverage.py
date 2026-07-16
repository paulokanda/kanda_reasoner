"""Support static evidence collection for Project Reasoner."""

from __future__ import annotations

import logging

from pathlib import Path


def collect_coverage_for_file(repo_root: Path, file_path: Path) -> dict:
    """
    Collect per-file coverage metadata from a .coverage database.

    The collector searches under repo_root for a .coverage file, opens that
    exact database, and then tries to match file_path against measured files.
    """
    try:
        from coverage import CoverageData
    except Exception:
        return {
            "available": False,
            "coverage_percent": None,
            "executed_lines": 0,
            "tests_covering_file": [],
            "reason": "coverage package not installed",
        }

    coverage_files = list(repo_root.rglob(".coverage"))
    if not coverage_files:
        return {
            "available": False,
            "coverage_percent": None,
            "executed_lines": 0,
            "tests_covering_file": [],
            "reason": "coverage data file not found",
        }

    coverage_path = coverage_files[0]

    try:
        data = CoverageData(basename=str(coverage_path))
        data.read()
    except Exception as exc:
        return {
            "available": False,
            "coverage_percent": None,
            "executed_lines": 0,
            "tests_covering_file": [],
            "reason": f"failed to read coverage data: {exc}",
        }

    try:
        target_path = str(file_path.resolve())
    except Exception:
        logging.exception("Boundary failure in collect_coverage_for_file")
        target_path = str(file_path)

    measured_files = list(data.measured_files())
    matched_file = ""

    for measured in measured_files:
        try:
            measured_resolved = str(Path(measured).resolve())
        except Exception:
            logging.exception("Boundary failure in collect_coverage_for_file")
            measured_resolved = str(measured)

        if measured_resolved == target_path:
            matched_file = measured
            break

    if not matched_file:
        return {
            "available": True,
            "coverage_percent": 0.0,
            "executed_lines": 0,
            "tests_covering_file": [],
            "reason": "file not present in coverage data",
        }

    try:
        executed_lines_list = list(data.lines(matched_file) or [])
    except Exception as exc:
        return {
            "available": False,
            "coverage_percent": None,
            "executed_lines": 0,
            "tests_covering_file": [],
            "reason": f"failed to read executed lines: {exc}",
        }

    try:
        source_lines = file_path.read_text(
            encoding="utf-8",
            errors="ignore",
        ).splitlines()
        executable_line_count = sum(1 for line in source_lines if line.strip())
    except Exception:
        logging.exception("Boundary failure in collect_coverage_for_file")
        executable_line_count = 0

    executed_lines = len(executed_lines_list)
    coverage_percent = 0.0
    if executable_line_count > 0:
        coverage_percent = round(
            (executed_lines / executable_line_count) * 100.0,
            3,
        )

    return {
        "available": True,
        "coverage_percent": coverage_percent,
        "executed_lines": executed_lines,
        "tests_covering_file": [],
        "reason": "",
    }
