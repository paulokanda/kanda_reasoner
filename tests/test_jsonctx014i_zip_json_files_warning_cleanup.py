from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.reasoner_tools_shell.runner_help.zip_json_files_private_impl import (  # noqa: E402
    ALLOWED_ZIP_SIZE_MB_OPTIONS,
    DEFAULT_ZIP_SIZE_MB,
    resolve_zip_dialog_start_folder,
    run_zip_json_files,
)


def test_zip_json_files_public_contract_is_directly_protected() -> None:
    assert DEFAULT_ZIP_SIZE_MB == 500
    assert ALLOWED_ZIP_SIZE_MB_OPTIONS == (100, 200, 300, 400, 500)
    assert callable(run_zip_json_files)


def test_zip_json_files_helper_avoids_direct_qtcore_import() -> None:
    source_path = (
        PROJECT_ROOT
        / 'kanda_reasoner_app'
        / "reasoner_tools_shell"
        / "runner_help"
        / "zip_json_files_private_impl.py"
    )
    source = source_path.read_text(encoding="utf-8")

    assert "from PySide6.QtCore import QProcess" not in source
    assert "helpers.QProcess(window)" in source
    assert "QFileDialog.getExistingDirectory" in source
    assert "QMessageBox" in source
    assert "Selected ZIP destination folder does not exist" in source


def test_stale_saved_zip_destination_is_not_used_as_dialog_start(tmp_path: Path) -> None:
    project_root = tmp_path / "developer_tools"
    project_root.mkdir(parents=True)
    missing_destination = tmp_path / "deleted_export_folder"

    start_folder = Path(
        resolve_zip_dialog_start_folder(
            project_root,
            last_destination=str(missing_destination),
        )
    )

    assert start_folder.exists()
    assert start_folder.is_dir()
    assert start_folder != missing_destination


def test_saved_zip_file_path_uses_existing_parent_as_dialog_start(tmp_path: Path) -> None:
    project_root = tmp_path / "developer_tools"
    project_root.mkdir(parents=True)
    saved_file_path = tmp_path / "previous_export.zip"
    saved_file_path.write_text("not a folder", encoding="utf-8")

    start_folder = Path(
        resolve_zip_dialog_start_folder(
            project_root,
            last_destination=str(saved_file_path),
        )
    )

    assert start_folder == tmp_path.resolve()


def main() -> int:
    import tempfile

    test_zip_json_files_public_contract_is_directly_protected()
    test_zip_json_files_helper_avoids_direct_qtcore_import()
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        test_stale_saved_zip_destination_is_not_used_as_dialog_start(root / "case1")
        test_saved_zip_file_path_uses_existing_parent_as_dialog_start(root / "case2")
    print("JSONCTX014I ZIP JSON files warning cleanup tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
