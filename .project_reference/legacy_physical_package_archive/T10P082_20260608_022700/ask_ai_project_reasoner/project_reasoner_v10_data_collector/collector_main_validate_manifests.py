"""Validate Pass 059C collector_main helper-manifest artifacts."""

from __future__ import annotations

import ast
import json
from pathlib import Path

MAX_LINES = 499


def _line_count(path: Path) -> int:
    text = path.read_text(encoding="utf-8", errors="replace")
    if not text:
        return 0
    return text.count("\n") + (0 if text.endswith("\n") else 1)


def _public_assignments(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8", errors="replace"), filename=str(path))
    names = set()
    for node in tree.body:
        if not isinstance(node, (ast.Assign, ast.AnnAssign)):
            continue
        targets = node.targets if isinstance(node, ast.Assign) else [node.target]
        for target in targets:
            if isinstance(target, ast.Name) and not target.id.startswith("_"):
                names.add(target.id)
    return names


def main() -> int:
    base_dir = Path(__file__).resolve().parent
    origin = base_dir / "collector_main.py"
    manifest_path = base_dir / "collector_main_help.json"
    if not origin.exists():
        print(f"FAIL missing origin file: {origin}")
        return 1
    if not manifest_path.exists():
        print(f"FAIL missing manifest file: {manifest_path}")
        return 1
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    helper_dir = base_dir / manifest.get("helper_dir", "")
    if not helper_dir.is_dir():
        print(f"FAIL missing helper directory: {helper_dir}")
        return 1
    failures = []
    checked = [origin]
    seen_public = {}
    for helper_name in manifest.get("helpers", []):
        helper_path = helper_dir / helper_name
        checked.append(helper_path)
        if not helper_path.exists():
            failures.append(f"missing helper file: {helper_path}")
            continue
        for symbol in _public_assignments(helper_path):
            seen_public.setdefault(symbol, []).append(str(helper_path))
    for symbol, paths in seen_public.items():
        if len(paths) > 1:
            failures.append(f"duplicate public helper symbol {symbol}: {paths}")
    for path in checked:
        if path.exists() and path.suffix == ".py":
            lines = _line_count(path)
            if lines > MAX_LINES:
                failures.append(f"{path} has more than {MAX_LINES} lines: {lines}")
    if failures:
        for failure in failures:
            print(f"FAIL {failure}")
        return 1
    print("PASS collector_main helper manifest")
    return 0


__all__ = ["main"]


if __name__ == "__main__":
    raise SystemExit(main())
