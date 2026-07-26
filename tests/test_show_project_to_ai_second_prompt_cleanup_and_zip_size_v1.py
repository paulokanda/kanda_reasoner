from __future__ import annotations

import json
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from kanda_reasoner_app.reasoner_context_bundle.handoff_zip_exporter import (  # noqa: E402
    ALLOWED_PART_SIZE_MB_OPTIONS,
    DEFAULT_PART_SIZE_MB,
)
from kanda_reasoner_app.reasoner_tools_shell.runner_help.zip_json_files_private_impl import (  # noqa: E402
    ALLOWED_ZIP_SIZE_MB_OPTIONS,
    DEFAULT_ZIP_SIZE_MB,
    cleanup_loose_json_files_after_success,
    cleanup_transient_daily_refactor_folders,
    load_saved_part_size_mb,
    save_selected_part_size_mb,
)


def test_zip_size_options_are_large_and_default_to_500() -> None:
    assert DEFAULT_PART_SIZE_MB == 500
    assert ALLOWED_PART_SIZE_MB_OPTIONS == (100, 200, 300, 400, 500)
    assert DEFAULT_ZIP_SIZE_MB == 500
    assert ALLOWED_ZIP_SIZE_MB_OPTIONS == (100, 200, 300, 400, 500)


def test_zip_size_preference_round_trips(tmp_path: Path, monkeypatch=None) -> None:
    import kanda_reasoner_app.reasoner_tools_shell.runner_help.zip_json_files_private_impl as module

    original = module._prefs_path
    module._prefs_path = lambda: tmp_path / "prefs.json"
    try:
        assert load_saved_part_size_mb() == 500
        save_selected_part_size_mb(300)
        assert load_saved_part_size_mb() == 300
        payload = json.loads((tmp_path / "prefs.json").read_text(encoding="utf-8"))
        assert payload["part_size_mb"] == 300
    finally:
        module._prefs_path = original


def test_cleanup_removes_loose_json_only_after_upload_zip_exists(tmp_path: Path) -> None:
    final_dir = tmp_path / "demo_show_project_to_AI" / "second_prompt_files"
    final_dir.mkdir(parents=True)
    (final_dir / "demo__ai_briefing.json").write_text("{}", encoding="utf-8")
    (final_dir / "demo__bundle_manifest.json").write_text("{}", encoding="utf-8")
    (final_dir / "_RUN_COLLECTOR_STATUS.txt").write_text("ok", encoding="utf-8")
    zip_path = final_dir / "demo__ai_handoff_upload.zip"
    with zipfile.ZipFile(zip_path, "w") as archive:
        archive.writestr("UPLOAD_README.txt", "ok")

    removed = cleanup_loose_json_files_after_success(final_dir)

    assert len(removed) == 2
    assert not any(final_dir.glob("*.json"))
    assert (final_dir / "_RUN_COLLECTOR_STATUS.txt").exists()
    assert zip_path.exists()


def test_cleanup_transient_daily_refactor_is_scoped_to_show_project_root(tmp_path: Path) -> None:
    project_root = tmp_path / "demo"
    project_root.mkdir(parents=True)
    source_folder = project_root / "daily_refactor"
    source_folder.mkdir()
    show_root = tmp_path / "demo_show_project_to_AI"
    show_root.mkdir()
    transient = show_root / "demo_daily_refactor_engine"
    transient.mkdir()

    removed = cleanup_transient_daily_refactor_folders(project_root, final_dir=show_root)

    assert str(transient) in removed
    assert not transient.exists()
    assert source_folder.exists()


def main() -> int:
    import tempfile

    test_zip_size_options_are_large_and_default_to_500()
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as name:
        root = Path(name)
        test_zip_size_preference_round_trips(root / "prefs")
        test_cleanup_removes_loose_json_only_after_upload_zip_exists(root / "cleanup")
        test_cleanup_transient_daily_refactor_is_scoped_to_show_project_root(root / "daily")
    print("VALIDATION OK: show_project_to_ai_second_prompt_cleanup_and_zip_size_v1")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
