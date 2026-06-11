"""Validate file_retrieval helper manifest artifacts."""

from __future__ import annotations

__all__ = []

import ast
import json
import py_compile
from pathlib import Path


MAX_LINES = 499


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def _line_count(path: Path) -> int:
    text = _read_text(path)
    if not text:
        return 0
    return text.count("\n") + (0 if text.endswith("\n") else 1)


def main() -> int:
    root = Path(__file__).resolve().parent
    manifest_path = root / "file_retrieval_help.json"
    helper_dir = root / "file_retrieval_help"
    origin = root / "file_retrieval.py"

    errors: list[str] = []

    if not manifest_path.exists():
        errors.append("missing manifest: " + str(manifest_path))
    if not helper_dir.exists():
        errors.append("missing helper dir: " + str(helper_dir))
    if not origin.exists():
        errors.append("missing origin file: " + str(origin))

    if errors:
        for error in errors:
            print("FAIL " + error)
        return 1

    try:
        manifest = json.loads(_read_text(manifest_path))
    except (OSError, json.JSONDecodeError) as exc:
        print("FAIL could not read manifest: " + str(exc))
        return 1

    helper_names = sorted(manifest.get("helpers", {}).keys())
    for name in helper_names:
        helper_path = helper_dir / name
        if not helper_path.exists():
            errors.append("missing helper file: " + str(helper_path))
            continue
        if _line_count(helper_path) > MAX_LINES:
            errors.append("helper file has 500 or more lines: " + str(helper_path))
        try:
            ast.parse(_read_text(helper_path), filename=str(helper_path))
            py_compile.compile(str(helper_path), doraise=True)
        except (OSError, SyntaxError, py_compile.PyCompileError) as exc:
            errors.append("helper compile/parse failed: " + str(helper_path) + " :: " + str(exc))

    if _line_count(origin) > MAX_LINES:
        errors.append("origin file has 500 or more lines: " + str(origin))

    try:
        py_compile.compile(str(origin), doraise=True)
    except (OSError, py_compile.PyCompileError) as exc:
        errors.append("origin compile failed: " + str(exc))

    if errors:
        for error in errors:
            print("FAIL " + error)
        return 1

    print("PASS file_retrieval helper manifest")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
