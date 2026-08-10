"""Validate safe external-root migration for project_freeze_after_update."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
import tempfile

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
PROMPT_TOOLS = PROJECT_ROOT / "kanda_prompt_workspace" / "prompt_tools"
if str(PROMPT_TOOLS) not in sys.path:
    sys.path.insert(0, str(PROMPT_TOOLS))

from kanda_reasoner_app.freeze_after_update.contract import (  # noqa: E402
    preview_freeze_entry,
    validate_freeze_entry_preview,
    write_confirmed_freeze_entry,
)
from kanda_reasoner_app.freeze_after_update.freeze_state import (  # noqa: E402
    build_freezes,
    load_freeze_index,
)
from kanda_reasoner_app.freeze_after_update.migration import (  # noqa: E402
    migrate_freeze_after_update_state,
)
from kanda_reasoner_app.freeze_after_update.paths import build_paths  # noqa: E402
from kanda_reasoner_app.project_analysis_evidence_paths import (  # noqa: E402
    PROJECT_FREEZE_AFTER_UPDATE_DIR,
    analysis_project_freeze_after_update_dir,
    ensure_show_project_lifecycle_manifest,
    legacy_project_freeze_after_update_dir,
    load_show_project_lifecycle_manifest,
    project_analysis_evidence_root,
)
from kanda_reasoner_app.reasoner_tools_shell.runner_help.zip_json_files_private_impl import (  # noqa: E402
    cleanup_show_project_to_ai_root_after_success,
)
import startup_freeze_context  # noqa: E402


def assert_true(condition: bool, message: str) -> None:
    """Raise AssertionError when condition is false."""
    if not condition:
        raise AssertionError(message)


def write_sample_legacy_freeze(project_root: Path, freeze_id: str = "freeze-sample") -> Path:
    """Create a sample legacy freeze root for migration tests."""
    legacy_root = legacy_project_freeze_after_update_dir(project_root)
    entries_root = legacy_root / "frozen_features_memory" / "entries"
    entries_root.mkdir(parents=True, exist_ok=True)
    entry = entries_root / (freeze_id + ".md")
    entry.write_text(
        """---
freeze_id: "freeze-sample"
box: "sample_box"
status: "frozen"
date: "2026-06-27"
entry: "project_freeze_after_update/frozen_features_memory/entries/freeze-sample.md"
protected_paths:
  - "sample.py"
do_not_touch_summary:
  - "Preserve sample behavior."
superseded_by: null
---

# freeze-sample
""",
        encoding="utf-8",
    )
    index_path = legacy_root / "frozen_features_memory" / "freeze_index.json"
    index_path.write_text(
        json.dumps(
            {
                "schema_version": "1.0",
                "generated_by": "test",
                "freezes": [
                    {
                        "freeze_id": "freeze-sample",
                        "status": "frozen",
                        "entry": "project_freeze_after_update/frozen_features_memory/entries/freeze-sample.md",
                    }
                ],
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return legacy_root


def test_resolver_and_lifecycle() -> None:
    """Validate dynamic external resolver and lifecycle manifest."""
    with tempfile.TemporaryDirectory(prefix="freeze_external_root_") as tmp:
        project_root = Path(tmp) / "sample_project"
        project_root.mkdir()
        show_root = project_analysis_evidence_root(project_root)
        freeze_root = analysis_project_freeze_after_update_dir(project_root)
        paths = build_paths(project_root)

        assert_true(show_root.name == "sample_project_show_project_to_AI", "wrong show-project root name")
        assert_true(freeze_root == show_root / PROJECT_FREEZE_AFTER_UPDATE_DIR, "wrong freeze root")
        assert_true(paths.box_root == freeze_root, "build_paths does not use external root")
        assert_true(paths.legacy_box_root == project_root / PROJECT_FREEZE_AFTER_UPDATE_DIR, "legacy path mismatch")

        manifest_path = ensure_show_project_lifecycle_manifest(project_root)
        assert_true(manifest_path.is_file(), "lifecycle manifest missing")
        manifest = load_show_project_lifecycle_manifest(project_root)
        assert_true(PROJECT_FREEZE_AFTER_UPDATE_DIR in manifest["persistent"], "freeze root not persistent")
        assert_true("project_error_memory" in manifest["persistent"], "error memory not persistent")
        assert_true("second_prompt_files_building" in manifest["disposable"], "building dir not disposable")


def test_legacy_fallback_and_clean_migration() -> None:
    """Validate read fallback, copy-not-move migration, backup, and cleanup."""
    with tempfile.TemporaryDirectory(prefix="freeze_external_migrate_") as tmp:
        project_root = Path(tmp) / "project_with_legacy"
        project_root.mkdir()
        legacy_root = write_sample_legacy_freeze(project_root)
        canonical_root = analysis_project_freeze_after_update_dir(project_root)

        assert_true(not canonical_root.exists(), "canonical root should start absent")
        freezes = build_freezes(project_root)
        assert_true(len(freezes) == 1, "legacy fallback did not find sample freeze")
        assert_true(
            freezes[0]["entry"] == "project_freeze_after_update/frozen_features_memory/entries/freeze-sample.md",
            "legacy entry did not keep logical path",
        )
        index = load_freeze_index(project_root)
        assert_true(len(index["freezes"]) == 1, "legacy freeze index fallback failed")

        result = migrate_freeze_after_update_state(project_root, clean_legacy=True)
        assert_true(result.ok, "migration failed: " + str(result.errors))
        assert_true(result.migrated_to_canonical, "migration did not copy legacy to canonical")
        assert_true(result.legacy_backup_created, "legacy backup missing")
        assert_true(result.legacy_removed, "legacy root was not removed")
        assert_true(not legacy_root.exists(), "legacy root still exists after clean migration")
        assert_true((canonical_root / "frozen_features_memory" / "entries" / "freeze-sample.md").is_file(), "canonical entry missing")
        assert_true((canonical_root / "migration_report.json").is_file(), "migration report missing")
        assert_true(Path(result.backup_root).is_dir(), "backup root missing")
        _assert_no_tool_logic_inside_freeze_root(canonical_root)


def test_conflict_does_not_merge() -> None:
    """Validate both-roots conflict is reported and not silently merged."""
    with tempfile.TemporaryDirectory(prefix="freeze_external_conflict_") as tmp:
        project_root = Path(tmp) / "project_with_conflict"
        project_root.mkdir()
        legacy_root = write_sample_legacy_freeze(project_root)
        canonical_root = analysis_project_freeze_after_update_dir(project_root)
        (canonical_root / "frozen_features_memory" / "entries").mkdir(parents=True)
        (canonical_root / "frozen_features_memory" / "freeze_index.json").write_text(
            '{"schema_version":"1.0","freezes":[]}\n',
            encoding="utf-8",
        )

        result = migrate_freeze_after_update_state(project_root, clean_legacy=False)
        assert_true(result.ok, "conflict report should be non-destructive and ok")
        assert_true(result.conflict_detected, "conflict was not detected")
        assert_true(legacy_root.is_dir(), "legacy root should be preserved when clean_legacy is false")
        assert_true(not (canonical_root / "frozen_features_memory" / "entries" / "freeze-sample.md").exists(), "legacy entry was silently merged")


def test_cleanup_preserves_persistent_children() -> None:
    """Validate Show Project to AI cleanup keeps persistent state."""
    with tempfile.TemporaryDirectory(prefix="freeze_external_cleanup_") as tmp:
        project_root = Path(tmp) / "project_cleanup"
        project_root.mkdir()
        show_root = project_analysis_evidence_root(project_root)
        freeze_root = analysis_project_freeze_after_update_dir(project_root)
        error_root = show_root / "project_error_memory"
        building_root = show_root / "second_prompt_files_building"
        unknown_root = show_root / "unknown_user_folder"
        final_root = show_root / "second_prompt_files"
        for path in (freeze_root, error_root, building_root, unknown_root, final_root):
            path.mkdir(parents=True, exist_ok=True)
        (building_root / "stale.txt").write_text("stale\n", encoding="utf-8")
        (freeze_root / "keep.txt").write_text("keep\n", encoding="utf-8")
        (error_root / "keep.txt").write_text("keep\n", encoding="utf-8")

        result = cleanup_show_project_to_ai_root_after_success(project_root, final_dir=final_root)
        assert_true(not building_root.exists(), "stale building folder was not removed")
        assert_true(freeze_root.is_dir(), "persistent freeze root was removed")
        assert_true(error_root.is_dir(), "persistent error memory root was removed")
        assert_true(unknown_root.is_dir(), "unknown folder should be skipped")
        assert_true(str(freeze_root) in result["skipped"], "freeze root not reported as skipped")


def test_startup_freeze_context_uses_external_root() -> None:
    """Validate startup freeze context fingerprints external memory."""
    with tempfile.TemporaryDirectory(prefix="freeze_external_startup_") as tmp:
        project_root = Path(tmp) / "project_startup"
        project_root.mkdir()
        canonical_memory = analysis_project_freeze_after_update_dir(project_root) / "frozen_features_memory"
        (canonical_memory / "entries").mkdir(parents=True)
        (canonical_memory / "freeze_index.json").write_text('{"schema_version":"1.0","freezes":[]}\n', encoding="utf-8")
        resolved_memory = startup_freeze_context.freeze_memory_root(project_root)
        assert_true(resolved_memory == canonical_memory, "startup context uses wrong memory root")
        fingerprint = startup_freeze_context.freeze_context_source_fingerprint(project_root)
        assert_true(len(fingerprint) == 64, "invalid startup fingerprint")





def _write_fake_local_freeze_writer(fake_root: Path) -> None:
    """Create a fake ledger engine that enforces project_root equality."""
    module_path = fake_root / "project_freeze_ledger" / "freeze_tools" / "local_freeze_writer.py"
    module_path.parent.mkdir(parents=True, exist_ok=True)
    (fake_root / "project_freeze_ledger" / "__init__.py").write_text("", encoding="utf-8")
    (fake_root / "project_freeze_ledger" / "freeze_tools" / "__init__.py").write_text("", encoding="utf-8")
    module_path.write_text('from __future__ import annotations\n\n\ndef preview_freeze_entry(project_root, inputs):\n    return {\n        "ok": True,\n        "is_writable": True,\n        "project_root": str(project_root),\n        "freeze_id": "freeze-fake",\n        "feature_title": "Fake Freeze",\n        "markdown": "# fake\\n",\n        "write_targets": ["project_freeze_after_update/frozen_features_memory/entries/freeze-fake.md"],\n        "errors": [],\n        "warnings": [],\n    }\n\n\ndef validate_freeze_entry_preview(project_root, preview):\n    preview_root = str(preview.get("project_root") or "")\n    active_root = str(project_root)\n    if preview_root != active_root:\n        return {\n            "ok": False,\n            "errors": ["project_root mismatch: preview has " + preview_root + "; active root is " + active_root],\n            "warnings": [],\n        }\n    return {"ok": True, "errors": [], "warnings": []}\n\n\ndef write_confirmed_freeze_entry(project_root, preview, *, confirmation=False):\n    validation = validate_freeze_entry_preview(project_root, preview)\n    if not validation.get("ok"):\n        return validation\n    if confirmation is not True:\n        return {"ok": False, "errors": ["confirmation required"], "warnings": []}\n    return {\n        "ok": True,\n        "freeze_id": preview.get("freeze_id"),\n        "project_root": str(project_root),\n        "written_files": ["project_freeze_after_update/frozen_features_memory/entries/freeze-fake.md"],\n        "errors": [],\n        "warnings": [],\n    }\n', encoding="utf-8")


def test_local_freeze_writer_preview_root_adapter() -> None:
    """Validate preview displays source root while engine validates owner root."""
    with tempfile.TemporaryDirectory(prefix="freeze_external_contract_") as tmp:
        fake_root = Path(tmp) / "fake_engine"
        _write_fake_local_freeze_writer(fake_root)
        sys.path.insert(0, str(fake_root))
        try:
            project_root = Path(tmp) / "contract_project"
            project_root.mkdir()
            owner_root = project_analysis_evidence_root(project_root)

            preview = preview_freeze_entry(project_root, {"feature_title": "Fake"})
            assert_true(preview.get("ok") is True, "preview failed: " + str(preview.get("errors")))
            assert_true(preview.get("project_root") == str(project_root.resolve(strict=False)), "preview should report selected source project root")
            assert_true(preview.get("freeze_state_owner_root") == str(owner_root), "preview should expose external owner root")

            validation = validate_freeze_entry_preview(project_root, preview)
            assert_true(validation.get("ok") is True, "adapter did not prevent project_root mismatch: " + str(validation.get("errors")))
            assert_true(validation.get("project_root") == str(project_root.resolve(strict=False)), "validation should report selected source project root")
            assert_true(validation.get("freeze_state_owner_root") == str(owner_root), "validation should expose external owner root")

            write_result = write_confirmed_freeze_entry(project_root, preview, confirmation=True)
            assert_true(write_result.get("ok") is True, "write adapter failed: " + str(write_result.get("errors")))
            assert_true(write_result.get("project_root") == str(project_root.resolve(strict=False)), "write should report selected source project root")
            assert_true(write_result.get("freeze_state_owner_root") == str(owner_root), "write should expose external owner root")
        finally:
            if str(fake_root) in sys.path:
                sys.path.remove(str(fake_root))
            for name in list(sys.modules):
                if name == "project_freeze_ledger" or name.startswith("project_freeze_ledger."):
                    sys.modules.pop(name, None)


def _assert_no_tool_logic_inside_freeze_root(freeze_root: Path) -> None:
    """Validate that the freeze root contains project-state data, not tool source."""
    forbidden_children = [
        "kanda_reasoner_app",
        "kanda_prompt_workspace",
        "payload",
        "validation",
        "scripts",
        "install_freeze_state_external_root_migration_v1.py",
        "install_freeze_state_external_root_migration_v2.py",
        "PATCH_MANIFEST.json",
        "KANDA_FREEZE_HINT.json",
    ]
    for child in forbidden_children:
        assert_true(not (freeze_root / child).exists(), "tool/source artifact was copied into freeze state: " + child)



def test_tool_logic_never_lands_in_freeze_state() -> None:
    """Validate canonical boundary: tool code is not project freeze-state data."""
    with tempfile.TemporaryDirectory(prefix="freeze_external_boundary_") as tmp:
        project_root = Path(tmp) / "project_boundary"
        project_root.mkdir()
        canonical_root = analysis_project_freeze_after_update_dir(project_root)
        canonical_root.mkdir(parents=True)
        _assert_no_tool_logic_inside_freeze_root(canonical_root)


def test_current_project_post_install_contract() -> None:
    """Validate installed project uses canonical external freeze root only."""
    project_root = PROJECT_ROOT
    show_root = project_analysis_evidence_root(project_root)
    canonical_root = analysis_project_freeze_after_update_dir(project_root)
    legacy_root = legacy_project_freeze_after_update_dir(project_root)
    ensure_show_project_lifecycle_manifest(project_root)
    manifest = load_show_project_lifecycle_manifest(project_root)
    assert_true(PROJECT_FREEZE_AFTER_UPDATE_DIR in manifest["persistent"], "installed manifest does not protect freeze root")
    assert_true(show_root.name.endswith("_show_project_to_AI"), "installed show-project root mismatch")
    assert_true(canonical_root == show_root / PROJECT_FREEZE_AFTER_UPDATE_DIR, "installed canonical freeze root mismatch")
    _assert_no_tool_logic_inside_freeze_root(canonical_root)
    assert_true(not legacy_root.exists(), "legacy in-source project_freeze_after_update still exists after migration")

def main(argv: list[str] | None = None) -> int:
    """Run validation suite."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check-installed-project", action="store_true")
    args = parser.parse_args(argv)
    tests = [
        test_resolver_and_lifecycle,
        test_legacy_fallback_and_clean_migration,
        test_conflict_does_not_merge,
        test_cleanup_preserves_persistent_children,
        test_startup_freeze_context_uses_external_root,
        test_local_freeze_writer_preview_root_adapter,
        test_tool_logic_never_lands_in_freeze_state,
    ]
    if args.check_installed_project:
        tests.append(test_current_project_post_install_contract)
    for test in tests:
        print("RUN " + test.__name__)
        test()
        print("PASS " + test.__name__)
    print("VALIDATION OK: freeze-state-external-root-migration-v3")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
