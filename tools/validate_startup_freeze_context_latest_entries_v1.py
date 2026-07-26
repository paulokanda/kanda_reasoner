#!/usr/bin/env python3
# project-path: tools/validate_startup_freeze_context_latest_entries_v1.py
"""Validate startup freeze context exposes newest frozen entries first."""

from __future__ import annotations

import importlib.util
import os
from pathlib import Path
import shutil
import sys
import tempfile
import uuid

FEATURE_ID = "startup-freeze-context-latest-entries-v1"
FIXTURE_PREFIX = "startup_freeze_context_validation_"


def _fail(message: str) -> int:
    """Print one deterministic validation failure."""
    print("VALIDATION FAILED: " + FEATURE_ID)
    print(message)
    return 1


def _load_module(project_root: Path):
    """Load the exact installed startup freeze-context module."""
    module_path = (
        project_root
        / "kanda_prompt_workspace"
        / "prompt_tools"
        / "startup_freeze_context.py"
    )
    if not module_path.is_file():
        raise FileNotFoundError(str(module_path))
    spec = importlib.util.spec_from_file_location(
        "startup_freeze_context_validation_target",
        module_path,
    )
    if spec is None or spec.loader is None:
        raise ImportError("Could not load startup_freeze_context.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _write_entry(
    path: Path,
    freeze_id: str,
    title: str,
    date_text: str,
    box: str,
) -> None:
    """Write one deterministic frozen-entry fixture."""
    path.write_text(
        "---\n"
        f"freeze_id: \"{freeze_id}\"\n"
        f"feature_title: \"{title}\"\n"
        f"box: \"{box}\"\n"
        "status: \"frozen\"\n"
        f"date: \"{date_text}\"\n"
        "superseded_by: null\n"
        "---\n\n"
        f"# {freeze_id}\n",
        encoding="utf-8",
    )


def _remove_fixture_support_root(path: Path) -> None:
    """Remove only the uniquely named validator-owned support fixture."""
    if not path.name.startswith(FIXTURE_PREFIX):
        raise RuntimeError(
            "Refusing to remove non-validator support root: " + str(path)
        )
    if path.exists():
        shutil.rmtree(path)
    if path.exists():
        raise RuntimeError("Fixture support cleanup failed: " + str(path))


def _validate_fixture_identity(
    module,
    project_root: Path,
    fixture_project_root: Path,
    fixture_slug: str,
) -> tuple[Path, Path]:
    """Resolve and validate the exact canonical external fixture roots."""
    support_root = module.freeze_state_owner_root(fixture_project_root)
    memory_root = module.freeze_memory_root(fixture_project_root)
    active_support_root = module.freeze_state_owner_root(project_root)
    expected_name = fixture_slug + "_show_project_to_AI"
    if support_root.name != expected_name:
        raise RuntimeError(
            "Canonical fixture support root had unexpected identity: "
            + str(support_root)
        )
    if support_root.resolve(strict=False) == active_support_root.resolve(
        strict=False
    ):
        raise RuntimeError("Fixture support root matched the active Project root.")
    if memory_root.parent.parent != support_root:
        raise RuntimeError(
            "Fixture memory root is not owned by its canonical support root."
        )
    return support_root, memory_root


def main() -> int:
    """Run newest-first validation against the canonical external owner."""
    project_root = (
        Path(sys.argv[1]).expanduser().resolve(strict=False)
        if len(sys.argv) > 1
        else Path.cwd().resolve(strict=False)
    )
    support_root: Path | None = None
    try:
        module_path = (
            project_root
            / "kanda_prompt_workspace"
            / "prompt_tools"
            / "startup_freeze_context.py"
        )
        text = module_path.read_text(encoding="utf-8")
        required_fragments = [
            "render_latest_freeze_entries_summary",
            "## Latest freeze entries - newest first",
            "It remains available even when the compact freeze exposure tool fails.",
        ]
        missing = [
            fragment for fragment in required_fragments if fragment not in text
        ]
        if missing:
            return _fail(
                "startup_freeze_context.py missing recency-shield fragment(s): "
                + str(missing)
            )

        module = _load_module(project_root)
        fixture_slug = FIXTURE_PREFIX + uuid.uuid4().hex
        with tempfile.TemporaryDirectory() as temp_dir:
            fixture_project_root = Path(temp_dir) / fixture_slug
            fixture_project_root.mkdir()
            support_root, memory_root = _validate_fixture_identity(
                module,
                project_root,
                fixture_project_root,
                fixture_slug,
            )
            _remove_fixture_support_root(support_root)
            try:
                entries_root = memory_root / "entries"
                entries_root.mkdir(parents=True)
                old_entry = entries_root / "freeze-20260628-old.md"
                new_entry = entries_root / "freeze-20260629-new.md"
                _write_entry(
                    old_entry,
                    "freeze-20260628-old",
                    "Old Freeze",
                    "2026-06-28",
                    "old.box",
                )
                _write_entry(
                    new_entry,
                    "freeze-20260629-new",
                    "New Freeze",
                    "2026-06-29",
                    "new.box",
                )
                os.utime(old_entry, (1_000_000_000, 1_000_000_000))
                os.utime(new_entry, (1_000_000_100, 1_000_000_100))

                report = module.render_latest_freeze_entries_summary(
                    memory_root,
                    limit=2,
                )
                new_pos = report.find("freeze-20260629-new")
                old_pos = report.find("freeze-20260628-old")
                if new_pos < 0 or old_pos < 0:
                    return _fail(
                        "Newest-first summary did not include both "
                        "validation entries: "
                        + report
                    )
                if new_pos > old_pos:
                    return _fail(
                        "Newest freeze entry did not appear before older "
                        "entry: "
                        + report
                    )
                if "newest first" not in report:
                    return _fail(
                        "Newest-first summary lacks explicit ordering marker."
                    )
            finally:
                _remove_fixture_support_root(support_root)

        if support_root is None or support_root.exists():
            return _fail("Canonical external fixture support root was not cleaned.")

        print("CANONICAL_EXTERNAL_FREEZE_FIXTURE_PATH: PASS")
        print("UNIQUE_EXTERNAL_SUPPORT_FIXTURE: PASS")
        print("FIXTURE_EXTERNAL_SUPPORT_CLEANUP: PASS")
        print("VALIDATION OK: " + FEATURE_ID)
        print("STATUS: IN_SYNC")
        return 0
    except Exception as exc:
        if support_root is not None:
            try:
                _remove_fixture_support_root(support_root)
            except Exception as cleanup_exc:
                return _fail(str(exc) + " | cleanup error: " + str(cleanup_exc))
        return _fail(str(exc))


if __name__ == "__main__":
    raise SystemExit(main())
