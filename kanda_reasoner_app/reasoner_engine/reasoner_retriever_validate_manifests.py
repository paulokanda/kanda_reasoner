# project-path: kanda_reasoner_app/reasoner_engine/reasoner_retriever_validate_manifests.py
"""Validate the canonical reasoner_retriever helper manifest.

This validator is intentionally scoped to the reasoner_retriever owner box.
It avoids scanning unrelated migrated manifests while the broader
reasoner_engine migration is still staged.
"""

from __future__ import annotations

import json
from pathlib import Path

OWNER_DIR = Path(__file__).resolve().parent
MANIFEST_PATH = OWNER_DIR / "reasoner_retriever_help.json"
HELP_DIR = OWNER_DIR / "reasoner_retriever_help"


def _read_json(path: Path) -> object:
    """Read JSON with BOM tolerance for compatibility with copied files."""
    return json.loads(path.read_text(encoding="utf-8-sig"))


def _collect_manifest_file_names(payload: object) -> set[str]:
    """Return helper file names listed by common manifest shapes."""
    names: set[str] = set()

    if isinstance(payload, dict):
        for key in ("helpers", "files", "helper_files", "modules"):
            value = payload.get(key)
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, str):
                        names.add(Path(item).name)
                    elif isinstance(item, dict):
                        for item_key in ("path", "file", "module", "name"):
                            item_value = item.get(item_key)
                            if isinstance(item_value, str) and item_value.endswith(".py"):
                                names.add(Path(item_value).name)
                                break

        # Fallback for manifests that map file names to descriptions.
        for key in payload:
            if isinstance(key, str) and key.endswith(".py"):
                names.add(Path(key).name)

    return names


def validate_manifest() -> list[str]:
    """Validate that the canonical manifest exists and references existing helpers."""
    errors: list[str] = []

    if not MANIFEST_PATH.is_file():
        return [f"Missing manifest: {MANIFEST_PATH}"]

    if not HELP_DIR.is_dir():
        return [f"Missing helper folder: {HELP_DIR}"]

    try:
        payload = _read_json(MANIFEST_PATH)
    except Exception as exc:  # pragma: no cover - defensive CLI reporting
        return [f"Manifest JSON could not be parsed: {exc.__class__.__name__}: {exc}"]

    names = _collect_manifest_file_names(payload)
    existing_names = {
        path.name
        for path in HELP_DIR.rglob("*.py")
        if "__pycache__" not in path.parts
    }

    missing = sorted(name for name in names if name not in existing_names)
    for name in missing:
        errors.append(f"Helper file listed in manifest is missing: {name}")

    if not existing_names:
        errors.append(f"No helper Python files found in: {HELP_DIR}")

    return errors


def main() -> int:
    """CLI entry point."""
    errors = validate_manifest()

    if errors:
        print(f"FAIL - {MANIFEST_PATH}")
        for error in errors:
            print(f"  - {error}")
        return 1

    print(f"PASS - {MANIFEST_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
