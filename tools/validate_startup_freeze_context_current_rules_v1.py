#!/usr/bin/env python3
# project-path: tools/validate_startup_freeze_context_current_rules_v1.py
"""Validate startup freeze context gives current rules explicit precedence."""

from __future__ import annotations

import hashlib
import importlib.util
import os
from pathlib import Path
import sys
import tempfile

FEATURE_ID = "startup-freeze-context-current-rules-v1"


def _fail(message: str) -> int:
    """Print one deterministic failure and return a nonzero status."""
    print("VALIDATION FAILED: " + FEATURE_ID)
    print(str(message))
    return 1


def _load_module(path: Path, name: str):
    """Load one module from an exact source path."""
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError("Could not load module: " + str(path))
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _sha256(path: Path) -> str:
    """Return the SHA-256 digest for one file."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _write_entry(
    path: Path,
    *,
    freeze_id: str,
    title: str,
    date_text: str,
    rule: str,
) -> None:
    """Write one deterministic freeze-entry fixture."""
    path.write_text(
        "---\n"
        f"freeze_id: \"{freeze_id}\"\n"
        f"feature_title: \"{title}\"\n"
        "box: \"sample.box\"\n"
        "status: \"frozen\"\n"
        f"date: \"{date_text}\"\n"
        "do_not_touch_summary:\n"
        f"  - \"{rule}\"\n"
        "superseded_by: null\n"
        "---\n\n"
        f"# {freeze_id}\n\n"
        "## do-not-regress rules\n\n"
        f"- {rule}\n",
        encoding="utf-8",
    )


def main() -> int:
    """Run current-rule precedence and read-only fixture validation."""
    project_root = (
        Path(sys.argv[1]).expanduser().resolve(strict=False)
        if len(sys.argv) > 1
        else Path.cwd().resolve(strict=False)
    )
    try:
        main_path = (
            project_root
            / "kanda_prompt_workspace"
            / "prompt_tools"
            / "startup_freeze_context.py"
        )
        helper_path = (
            project_root
            / "kanda_prompt_workspace"
            / "prompt_tools"
            / "startup_freeze_entry_summary.py"
        )
        main_text = main_path.read_text(encoding="utf-8")
        helper_text = helper_path.read_text(encoding="utf-8")
        required_main_fragments = [
            "## Historical compact freeze inventory",
            "HISTORICAL_COMPACT_REPORT_AUTHORITY: inventory-only when conflicts exist",
            "## Current freeze rules - newest first",
            "render_latest_freeze_rules_summary",
        ]
        missing_main = [
            value for value in required_main_fragments if value not in main_text
        ]
        if missing_main:
            return _fail("Missing main renderer fragment(s): " + str(missing_main))
        required_helper_fragments = [
            "CURRENT_FREEZE_RULES_ORDER: newest freeze entries first.",
            "CURRENT_FREEZE_RULES_PRECEDENCE:",
            "def render_latest_freeze_rules_summary",
        ]
        missing_helper = [
            value for value in required_helper_fragments if value not in helper_text
        ]
        if missing_helper:
            return _fail("Missing helper fragment(s): " + str(missing_helper))

        helper = _load_module(helper_path, "startup_freeze_entry_summary_validation")
        with tempfile.TemporaryDirectory() as temp_dir:
            memory_root = Path(temp_dir) / "frozen_features_memory"
            entries_root = memory_root / "entries"
            entries_root.mkdir(parents=True)
            stale_rule = (
                "Generated upload files must live inside "
                "<project_root>/project_freeze_after_update/files_to_send_ai/."
            )
            current_rule = (
                "Project-specific frozen memory remains under the external "
                "<project>_show_project_to_AI support root."
            )
            old_entry = entries_root / "freeze-20260613-old.md"
            new_entry = entries_root / "freeze-20260721-new.md"
            _write_entry(
                old_entry,
                freeze_id="freeze-20260613-old",
                title="Old Project-Local Delivery Rule",
                date_text="2026-06-13",
                rule=stale_rule,
            )
            _write_entry(
                new_entry,
                freeze_id="freeze-20260721-new",
                title="Current External Support Rule",
                date_text="2026-07-21",
                rule=current_rule,
            )
            os.utime(old_entry, (1_000_000_000, 1_000_000_000))
            os.utime(new_entry, (1_000_000_100, 1_000_000_100))
            old_before = _sha256(old_entry)
            new_before = _sha256(new_entry)

            report = helper.render_latest_freeze_rules_summary(
                memory_root,
                limit=1,
            )
            if "CURRENT_FREEZE_RULES_PRECEDENCE:" not in report:
                return _fail("Current-rule report lacks precedence marker.")
            if current_rule not in report:
                return _fail("Newest current rule was not exposed: " + report)
            if stale_rule in report:
                return _fail("Older conflicting rule entered the newest-only view.")
            if report.count(current_rule) != 1:
                return _fail("Duplicate current rule was not deduplicated.")
            if _sha256(old_entry) != old_before or _sha256(new_entry) != new_before:
                return _fail(
                    "Read-only current-rule rendering mutated a fixture entry."
                )

        if len(main_path.read_text(encoding="utf-8").splitlines()) > 500:
            return _fail("startup_freeze_context.py exceeds 500 physical lines.")
        if len(helper_path.read_text(encoding="utf-8").splitlines()) > 500:
            return _fail("startup_freeze_entry_summary.py exceeds 500 physical lines.")

        print("HISTORICAL_COMPACT_INVENTORY_LABELED: PASS")
        print("CURRENT_FREEZE_RULES_NEWEST_FIRST: PASS")
        print("CURRENT_FREEZE_RULES_PRECEDENCE: PASS")
        print("CURRENT_FREEZE_ENTRY_READ_ONLY: PASS")
        print("TOUCHED_SOURCE_MODULES_MAX_500_LINES: PASS")
        print("VALIDATION OK: " + FEATURE_ID)
        print("STATUS: IN_SYNC")
        return 0
    except Exception as exc:
        return _fail(str(exc))


if __name__ == "__main__":
    raise SystemExit(main())
