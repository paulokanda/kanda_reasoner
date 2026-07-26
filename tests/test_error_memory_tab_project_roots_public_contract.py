"""Characterization tests for Error Memory project-root helpers."""
from __future__ import annotations

from pathlib import Path

from kanda_reasoner_app.error_memory_gui import _project_roots


def test_project_roots_helper_is_private_non_gui_contract() -> None:
    source = Path(_project_roots.__file__).read_text(encoding="utf-8")

    assert "PySide" not in source
    assert "Qt" not in source
    assert "error_memory_tab" not in source
    assert "ErrorMemoryTab" not in source


def test_existing_source_root_is_accepted(tmp_path: Path) -> None:
    project = tmp_path / "kanda_reasoner"
    project.mkdir()

    assert _project_roots.existing_directory_from_text(str(project)) == project.resolve(strict=False)


def test_generated_show_project_root_resolves_to_existing_source_peer(tmp_path: Path) -> None:
    project = tmp_path / "kanda_reasoner"
    show = tmp_path / "kanda_reasoner_show_project_to_AI"
    project.mkdir()
    show.mkdir()

    assert _project_roots.source_root_peer_from_generated_output(show) == project.resolve(strict=False)
    assert _project_roots.existing_directory_from_text(str(show)) == project.resolve(strict=False)


def test_generated_child_hint_resolves_to_source_peer(tmp_path: Path) -> None:
    project = tmp_path / "kanda_reasoner"
    show = tmp_path / "kanda_reasoner_show_project_to_AI"
    pending = show / "project_error_memory" / "pending_ai_assisted_error_lesson_intake"
    project.mkdir()
    pending.mkdir(parents=True)

    assert _project_roots.source_root_from_directory_hint(pending) == project.resolve(strict=False)
    assert _project_roots.existing_directory_from_text(str(pending)) == project.resolve(strict=False)


def test_generated_names_without_source_peer_are_rejected(tmp_path: Path) -> None:
    show = tmp_path / "missing_project_show_project_to_AI"
    delete_after = tmp_path / "missing_project_delete_after_daily_work"
    child = tmp_path / "project_error_memory"
    show.mkdir()
    delete_after.mkdir()
    child.mkdir()

    assert _project_roots.existing_directory_from_text(str(show)) is None
    assert _project_roots.existing_directory_from_text(str(delete_after)) is None
    assert _project_roots.existing_directory_from_text(str(child)) is None
