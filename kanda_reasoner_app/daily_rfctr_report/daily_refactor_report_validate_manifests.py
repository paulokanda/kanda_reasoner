"""Validate daily_refactor_report helper manifest."""

from __future__ import annotations

import ast
import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
MANIFEST_PATH = BASE_DIR / "daily_refactor_report_help.json"


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def _extract_all(path: Path) -> list[str]:
    tree = ast.parse(_read_text(path), filename=str(path))
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "__all__":
                    value = ast.literal_eval(node.value)
                    if isinstance(value, list):
                        return [str(item) for item in value]
    return []


def main() -> int:
    if not MANIFEST_PATH.exists():
        print(f"FAIL missing manifest: {MANIFEST_PATH}")
        return 1

    manifest = json.loads(_read_text(MANIFEST_PATH))
    helper_folder = manifest.get("helper_folder")
    if helper_folder != "daily_refactor_report_help":
        print("FAIL unexpected helper_folder")
        return 1

    errors: list[str] = []
    seen_exports: dict[str, str] = {}

    for helper in manifest.get("helpers", []):
        rel_path = str(helper.get("path", ""))
        helper_path = BASE_DIR / rel_path
        expected_exports = [str(item) for item in helper.get("exports", [])]

        if not helper_path.exists():
            errors.append(f"missing helper file: {helper_path}")
            continue

        actual_exports = _extract_all(helper_path)
        if actual_exports != expected_exports:
            errors.append(
                f"__all__ mismatch for {helper_path}: "
                f"expected {expected_exports!r}, got {actual_exports!r}"
            )

        for exported in actual_exports:
            previous = seen_exports.get(exported)
            if previous is not None:
                errors.append(
                    f"duplicate helper export {exported!r}: {previous} and {helper_path}"
                )
            seen_exports[exported] = str(helper_path)

    if errors:
        for error in errors:
            print(f"FAIL {error}")
        return 1

    print("PASS daily_refactor_report helper manifest")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
