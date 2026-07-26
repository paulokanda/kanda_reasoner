#!/usr/bin/env python3
# project-path: tools/validate_frozen_memory_integrity_compatibility_v1.py
"""Validate frozen-memory compatibility, authority, and read-only repair."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from types import SimpleNamespace

FEATURE_ID = "frozen-memory-integrity-compatibility-recovery-v1"


def _require(condition: bool, message: str) -> None:
    """Raise one deterministic assertion failure."""
    if not condition:
        raise AssertionError(message)


def _read(path: Path) -> str:
    """Read one UTF-8 source file."""
    return path.read_text(encoding="utf-8-sig")


def _synthetic_old_entry() -> str:
    """Return the historical body-only compatibility fixture."""
    return (
        "---\n"
        "freeze_id: freeze-20260613-freeze-after-update-bom-index-tolerance-v1\n"
        "status: frozen\n"
        "project: kanda_reasoner\n"
        "box: project_freeze_ledger/freeze_tools + project_freeze_after_update/frozen_features_memory\n"
        "date: 2026-06-13\n"
        "validated: true\n"
        "---\n\n"
        "# Freeze\n\n"
        "## Protected paths\n\n"
        "- project_freeze_ledger/freeze_tools/freeze_after_update_generator.py\n"
        "- project_freeze_after_update/frozen_features_memory/freeze_index.json\n\n"
        "## Do not touch summary\n\n"
        "- Do not change BOM-tolerant JSON reads back to plain utf-8.\n"
        "- Do not allow BOM in regenerated freeze_index.json.\n"
    )


def _synthetic_alias_entry() -> str:
    """Return the alternate frontmatter-key compatibility fixture."""
    return (
        "---\n"
        "freeze_id: \"freeze-20260616-freeze-formulary-current-feature-autofill-regression-v1\"\n"
        "feature_title: \"Freeze Formulary Current-Feature Autofill Regression Repair\"\n"
        "primary_box: \"kanda_reasoner_app/freeze_after_update_gui\"\n"
        "box_type: \"GUI / Freeze Formulary / Local Freeze Workflow\"\n"
        "status: \"frozen\"\n"
        "date: \"2026-06-16\"\n"
        "entry: \"project_freeze_after_update/frozen_features_memory/entries/sample.md\"\n"
        "protected_paths:\n"
        "  - \"kanda_reasoner_app/freeze_after_update_gui/freeze_after_update_tab.py\"\n"
        "do_not_regress_rules:\n"
        "  - \"Preview Freeze Entry must remain read-only.\"\n"
        "superseded_by: null\n"
        "---\n\n"
        "# Freeze\n"
    )


def _run_repair_check(root: Path) -> str:
    """Run the installed read-only index check."""
    command = [
        sys.executable,
        str(root / "tools" / "repair_frozen_memory_index_compatibility_v1.py"),
        "--project-root",
        str(root),
        "--check",
    ]
    completed = subprocess.run(
        command,
        cwd=str(root),
        text=True,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    output = (completed.stdout or "") + (completed.stderr or "")
    if output.strip():
        print(output.rstrip())
    _require(completed.returncode == 0, "Installed freeze-index check failed.")
    for marker in (
        "FREEZE_INDEX_IN_SYNC: PASS",
        "FREEZE_INDEX_BOM_READ_COMPATIBILITY: PASS",
        "FROZEN_ENTRIES_READ_ONLY: PASS",
        "VALIDATION OK: " + FEATURE_ID,
        "STATUS: IN_SYNC",
    ):
        _require(marker in output, "Repair check missed marker: " + marker)
    return output


def validate_static(root: Path) -> None:
    """Validate exact installed source contracts."""
    freeze_state_path = (
        root / "kanda_reasoner_app" / "freeze_after_update" / "freeze_state.py"
    )
    models_path = (
        root / "kanda_reasoner_app" / "freeze_hint_intake" / "models.py"
    )
    startup_path = (
        root
        / "kanda_prompt_workspace"
        / "prompt_tools"
        / "startup_freeze_entry_summary.py"
    )
    exports_path = (
        root
        / "kanda_reasoner_app"
        / "freeze_after_update_gui"
        / "_freeze_memory_exports.py"
    )

    freeze_state_text = _read(freeze_state_path)
    models_text = _read(models_path)
    startup_text = _read(startup_path)
    exports_text = _read(exports_path)

    _require(
        'read_text(encoding="utf-8-sig")' in freeze_state_text,
        "freeze_state.py lacks BOM-tolerant reads.",
    )
    _require(
        'meta.get("primary_box")' in freeze_state_text,
        "freeze_state.py lacks primary_box compatibility.",
    )
    _require(
        '"do_not_touch_summary", "do_not_regress_rules"' in freeze_state_text,
        "freeze_state.py lacks rule-key compatibility.",
    )
    _require(
        '"Protected paths"' in freeze_state_text
        and '"Do not touch summary"' in freeze_state_text,
        "freeze_state.py lacks historical Markdown fallback sections.",
    )
    _require(
        '"pre-validation sidecar"' in models_text,
        "Freeze hint pending patterns do not reject generic pre-validation sidecars.",
    )
    _require(
        "FROZEN_ENTRY_AUTHORITY_RULE:" in startup_text,
        "Startup freeze summary lacks frozen-entry authority clarification.",
    )
    _require(
        'metadata.get("primary_box")' in startup_text,
        "Startup freeze summary lacks primary_box compatibility.",
    )
    _require(
        '_frontmatter_list(text, "do_not_regress_rules")' in startup_text,
        "Startup freeze summary lacks rule-key compatibility.",
    )
    _require(
        "Authority: Frontmatter status and superseded_by" in exports_text,
        "Frozen-memory snippets lack authority clarification.",
    )
    _require(
        exports_text.count('read_text(encoding="utf-8-sig")') >= 2,
        "Frozen-memory snippet reads are not BOM tolerant.",
    )

    for path in (freeze_state_path, models_path, startup_path, exports_path):
        _require(
            len(_read(path).splitlines()) <= 500,
            path.name + " exceeds 500 physical lines.",
        )

    print("FREEZE_INDEX_BOM_SOURCE_CONTRACT: PASS")
    print("HISTORICAL_FRONTMATTER_COMPATIBILITY_SOURCE: PASS")
    print("PREVALIDATION_SIDECAR_PENDING_PATTERN: PASS")
    print("FROZEN_SNIPPET_AUTHORITY_NOTE: PASS")
    print("TOUCHED_SOURCE_MODULES_MAX_500_LINES: PASS")


def validate_runtime(root: Path) -> None:
    """Validate synthetic and current-project runtime behavior."""
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))

    from kanda_reasoner_app.freeze_after_update import freeze_state
    from kanda_reasoner_app.freeze_hint_intake.form_text_validation import (
        _has_safe_validation_evidence_marker,
    )
    from kanda_prompt_workspace.prompt_tools import startup_freeze_entry_summary

    old_text = _synthetic_old_entry()
    old_meta = freeze_state.parse_frontmatter(old_text)
    _require(
        freeze_state._compatible_protected_paths(old_meta, old_text),
        "Historical body protected paths were not recovered.",
    )
    _require(
        freeze_state._compatible_do_not_touch_summary(old_meta, old_text),
        "Historical body rules were not recovered.",
    )
    print("HISTORICAL_BODY_PROTECTED_PATH_RECOVERY: PASS")
    print("HISTORICAL_BODY_RULE_RECOVERY: PASS")

    alias_text = _synthetic_alias_entry()
    alias_meta = freeze_state.parse_frontmatter(alias_text)
    _require(
        freeze_state._compatible_box(alias_meta)
        == "kanda_reasoner_app/freeze_after_update_gui",
        "Historical primary_box alias was not recovered.",
    )
    _require(
        freeze_state._compatible_do_not_touch_summary(alias_meta, alias_text)
        == ["Preview Freeze Entry must remain read-only."],
        "Historical do_not_regress_rules alias was not recovered.",
    )
    print("HISTORICAL_FRONTMATTER_BOX_ALIAS: PASS")
    print("HISTORICAL_FRONTMATTER_RULE_ALIAS: PASS")

    pending = (
        "Pre-validation sidecar. Require VALIDATION OK: sample-feature, "
        "STATUS: IN_SYNC, and ZIP CONTRACT: PASS before Freeze."
    )
    _require(
        not _has_safe_validation_evidence_marker(pending),
        "Pre-validation sidecar was incorrectly accepted as completed validation.",
    )
    completed = "VALIDATION OK: sample-feature\nSTATUS: IN_SYNC\nZIP CONTRACT: PASS"
    _require(
        _has_safe_validation_evidence_marker(completed),
        "Real local validation markers were rejected.",
    )
    print("PREVALIDATION_SIDECAR_REJECTED: PASS")
    print("REAL_VALIDATION_MARKER_ACCEPTED: PASS")

    with tempfile.TemporaryDirectory(prefix="kanda_freeze_integrity_") as temp_dir:
        temp = Path(temp_dir)
        index_path = temp / "freeze_index.json"
        index_path.write_text(
            json.dumps(
                {"schema_version": "1.0", "freezes": []},
                ensure_ascii=False,
            ),
            encoding="utf-8-sig",
        )
        original_build_paths = freeze_state.build_paths
        original_legacy_index = freeze_state._legacy_freeze_index
        freeze_state.build_paths = lambda project_root: SimpleNamespace(
            freeze_index=index_path,
        )
        freeze_state._legacy_freeze_index = lambda project_root: index_path
        try:
            loaded = freeze_state.load_freeze_index(temp)
        finally:
            freeze_state.build_paths = original_build_paths
            freeze_state._legacy_freeze_index = original_legacy_index
        _require(loaded.get("schema_version") == "1.0", "BOM index read failed.")
        print("FREEZE_INDEX_BOM_READ: PASS")

        memory_root = temp / "memory"
        entries_root = memory_root / "entries"
        entries_root.mkdir(parents=True)
        alias_entry = entries_root / "freeze-20260616-alias.md"
        alias_entry.write_bytes(b"\xef\xbb\xbf" + alias_text.encode("utf-8"))
        summary = startup_freeze_entry_summary.render_latest_freeze_entries_summary(
            memory_root,
            limit=1,
        )
        rules = startup_freeze_entry_summary.render_latest_freeze_rules_summary(
            memory_root,
            limit=1,
        )
        _require(
            "box=kanda_reasoner_app/freeze_after_update_gui" in summary,
            "Startup summary did not recover primary_box.",
        )
        _require(
            "Preview Freeze Entry must remain read-only." in rules,
            "Startup summary did not recover do_not_regress_rules.",
        )
        _require(
            "FROZEN_ENTRY_AUTHORITY_RULE:" in summary
            and "FROZEN_ENTRY_AUTHORITY_RULE:" in rules,
            "Startup summary lacks authority rule.",
        )
        print("STARTUP_FREEZE_SUMMARY_HISTORICAL_COMPATIBILITY: PASS")

    _run_repair_check(root)


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    return parser.parse_args()


def main() -> int:
    """Run the focused integrity validation."""
    args = parse_args()
    root = Path(args.root).expanduser().resolve(strict=False)
    validate_static(root)
    validate_runtime(root)
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print("VALIDATION HELPER ERROR")
        print("ERROR TYPE: " + exc.__class__.__name__)
        print("ERROR MESSAGE: " + str(exc))
        raise SystemExit(1)
