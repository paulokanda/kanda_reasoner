#!/usr/bin/env python3
"""Validate the runtime runner helper manifest contract."""

from __future__ import annotations

import ast
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
_STAGED_PACKAGE_DIR = "_".join(("ask", "ai", "project", "reasoner"))
BASE = ROOT / _STAGED_PACKAGE_DIR / "reasoner_runtime_collector"
ORIGIN = BASE / "runtime_runner.py"
HELP_DIR = BASE / "runtime_runner_help"
MANIFEST = BASE / "runtime_runner_help.json"
HELPERS = ['runtime_runner_part_1_private_impl.py', 'runtime_runner_part_2_private_impl.py', 'runtime_runner_part_3_private_impl.py']


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def _line_count(path: Path) -> int:
    text = _read(path)
    if not text:
        return 0
    return len(text.splitlines())


def main() -> int:
    errors = []
    if not ORIGIN.exists():
        errors.append(f"missing origin file: {ORIGIN}")
    elif _line_count(ORIGIN) >= 500:
        errors.append("origin file has 500 or more lines")

    if not HELP_DIR.exists():
        errors.append(f"missing helper directory: {HELP_DIR}")

    if not MANIFEST.exists():
        errors.append(f"missing manifest: {MANIFEST}")
    else:
        try:
            payload = json.loads(_read(MANIFEST))
            listed = payload.get("helpers", [])
            if listed != HELPERS:
                errors.append("manifest helper list does not match expected helpers")
        except json.JSONDecodeError as exc:
            errors.append(f"manifest parse failed: {exc}")

    for name in HELPERS:
        helper = HELP_DIR / name
        if not helper.exists():
            errors.append(f"missing helper file: {helper}")
            continue
        if _line_count(helper) >= 500:
            errors.append(f"helper file has 500 or more lines: {helper}")
        try:
            ast.parse(_read(helper), filename=str(helper))
        except SyntaxError as exc:
            errors.append(f"helper syntax error: {helper}: {exc}")

    if errors:
        for error in errors:
            print("FAIL " + error)
        return 1

    print("PASS runtime_runner helper manifest")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
