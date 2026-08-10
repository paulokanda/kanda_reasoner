"""Clear active Project authority before a KANDA Reasoner Tool Portable build."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path
from typing import Any, MutableMapping

PROJECT_ENV_NAMES = (
    "kanda_reasoner_project_root",
    "KANDA_REASONER_PROJECT_ROOT",
    "KANDA_RUNTIME_PROJECT_ROOT",
    "PROJECT_REASONER_PROJECT_ROOT",
    "PROJECT_REASONER_SCAN_ROOT",
    "KANDA_REASONER_SCAN_ROOT",
)
PROJECT_ENV_PREFIXES = ("KANDA_", "PROJECT_REASONER_")


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _read_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise RuntimeError("TOOL_PROJECT_REGISTRY_UNREADABLE:" + str(path)) from exc
    if not isinstance(payload, dict):
        raise RuntimeError("TOOL_PROJECT_REGISTRY_NOT_OBJECT:" + str(path))
    return payload


def scrub_project_environment(
    environment: MutableMapping[str, str],
) -> tuple[str, ...]:
    """Remove Project-selection and inherited KANDA runtime overrides."""
    removed: list[str] = []
    for name in list(environment):
        if name in PROJECT_ENV_NAMES or any(
            name.startswith(prefix) for prefix in PROJECT_ENV_PREFIXES
        ):
            environment.pop(name, None)
            removed.append(name)
    return tuple(sorted(set(removed), key=str.casefold))


def clear_active_project(
    tool_root: Path,
    *,
    registry_path: Path | None = None,
) -> dict[str, Any]:
    """Clear current selection atomically while preserving registry history."""
    root = tool_root.expanduser().resolve(strict=False)
    if not root.is_dir():
        raise RuntimeError("TOOL_ROOT_MISSING:" + str(root))
    sys.path.insert(0, str(root))
    try:
        from kanda_reasoner_app.project_selection_registry import (
            ProjectSelectionRegistry,
        )
    finally:
        try:
            sys.path.remove(str(root))
        except ValueError:
            pass

    registry = ProjectSelectionRegistry(
        tool_source_root=root,
        registry_path=registry_path,
    )
    path = registry.registry_path.resolve(strict=False)
    before_payload = _read_json(path) if path.is_file() else {
        "schema_version": "1.0",
        "current_project_id": "",
        "projects": {},
    }
    before_projects = before_payload.get("projects", {})
    if not isinstance(before_projects, dict):
        raise RuntimeError("TOOL_PROJECT_REGISTRY_PROJECTS_NOT_OBJECT")
    before_current = str(before_payload.get("current_project_id") or "").strip()
    before_hash = _sha256(path) if path.is_file() else None

    registry.clear_current_selection()

    after_payload = _read_json(path)
    after_projects = after_payload.get("projects", {})
    after_current = str(after_payload.get("current_project_id") or "").strip()
    if after_current:
        raise RuntimeError("PROJECT_UNLOAD_FAILED_CURRENT_ID_REMAINS:" + after_current)
    if after_projects != before_projects:
        raise RuntimeError("PROJECT_UNLOAD_CHANGED_PROJECT_HISTORY")

    return {
        "schema_version": "1.0",
        "tool_root": str(root),
        "registry_path": str(path),
        "registry_sha256_before": before_hash,
        "registry_sha256_after": _sha256(path),
        "selected_project_id_before": before_current or None,
        "selected_project_id_after": None,
        "registered_project_count": len(after_projects),
        "project_history_preserved": True,
        "self_hosting_after": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tool-root", type=Path, required=True)
    parser.add_argument("--registry-path", type=Path)
    parser.add_argument("--json-output", type=Path)
    args = parser.parse_args()

    evidence = clear_active_project(
        args.tool_root,
        registry_path=args.registry_path,
    )
    removed = scrub_project_environment(os.environ)
    evidence["scrubbed_environment_names"] = list(removed)
    if args.json_output is not None:
        output = args.json_output.expanduser().resolve(strict=False)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(
            json.dumps(evidence, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
            newline="\n",
        )

    print(f"TOOL ROOT: {evidence['tool_root']}")
    print("SELECTED PROJECT: NONE")
    print("SELF-HOSTING MODE: OFF")
    print("PROJECT HISTORY PRESERVED: PASS")
    print("PROJECT ENVIRONMENT OVERRIDES: ABSENT")
    print("TOOL PORTABLE BUILD CONTEXT: ISOLATED")
    print("UNLOAD PROJECT FOR TOOL PORTABLE: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
