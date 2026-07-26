"""Validate Show Project to AI and Error Memory path guards.

This script is intentionally standard-library only. It validates that generated
output hints resolve back to the canonical project root and that partial or
misspelled root text does not become an active project root.
"""

from __future__ import annotations

import sys
import tempfile
import types
from pathlib import Path


def _install_storage_policy_package_stub() -> None:
    """Avoid executing the broad storage_policy package initializer in tests."""
    package_name = "kanda_reasoner_app.storage_policy"
    if package_name in sys.modules:
        return
    source_root = Path(__file__).resolve().parents[1]
    package = types.ModuleType(package_name)
    package.__path__ = [str(source_root / "kanda_reasoner_app" / "storage_policy")]
    sys.modules[package_name] = package


def _install_pyside_stubs() -> None:
    """Install minimal PySide6 stubs for importing GUI mixins in validation."""
    if "PySide6" in sys.modules:
        return

    pyside = types.ModuleType("PySide6")
    qt_widgets = types.ModuleType("PySide6.QtWidgets")

    class QWidget:
        pass

    class QLineEdit(QWidget):
        pass

    class QComboBox(QWidget):
        pass

    qt_widgets.QWidget = QWidget
    qt_widgets.QLineEdit = QLineEdit
    qt_widgets.QComboBox = QComboBox
    pyside.QtWidgets = qt_widgets
    sys.modules["PySide6"] = pyside
    sys.modules["PySide6.QtWidgets"] = qt_widgets


def _assert_equal(actual: Path | None, expected: Path | None, label: str) -> None:
    if actual != expected:
        raise AssertionError(label + ": expected " + str(expected) + ", got " + str(actual))


def _assert_not_exists(path: Path, label: str) -> None:
    if path.exists():
        raise AssertionError(label + " should not exist: " + str(path))


def main() -> int:
    _install_storage_policy_package_stub()

    from kanda_reasoner_app.error_memory.store import bootstrap_error_memory_store
    from kanda_reasoner_app.error_memory.paths import resolve_project_error_memory_root
    from kanda_reasoner_app.project_analysis_evidence_paths import (
        project_analysis_evidence_root,
        show_project_to_ai_root_from_hint,
    )

    _install_pyside_stubs()
    from kanda_reasoner_app.reasoner_tools_gui_shell.main_window_help.window_project_root import (  # noqa: E501
        _WindowProjectRootMixin,
    )

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_root = Path(temp_dir)
        project_root = temp_root / "kanda_reasoner"
        project_root.mkdir()
        show_root = temp_root / "kanda_reasoner_show_project_to_AI"
        nested_show_root = project_root / "kanda_reasoner_show_project_to_AI"
        nested_error_root = nested_show_root / "project_error_memory"
        nested_pending_dir = nested_error_root / "pending_ai_assisted_error_lesson_intake"
        error_root = show_root / "project_error_memory"
        pending_dir = error_root / "pending_ai_assisted_error_lesson_intake"
        lessons_dir = error_root / "lessons"
        second_prompt_dir = show_root / "second_prompt_files"
        daily_work = temp_root / "kanda_reasoner_delete_after_daily_work"
        wrong_partial_root = temp_root / "kanda_reasoner_error_me"
        wrong_show_root = temp_root / "kanda_reasoner_error_me_show_project_to_AI"

        for path in (pending_dir, lessons_dir, second_prompt_dir, daily_work, wrong_show_root, nested_pending_dir):
            path.mkdir(parents=True, exist_ok=True)

        expected_show = show_root.resolve(strict=False)
        expected_project = project_root.resolve(strict=False)

        _assert_equal(project_analysis_evidence_root(project_root), expected_show, "project root show path")
        _assert_equal(show_project_to_ai_root_from_hint(show_root), expected_show, "show root hint")
        _assert_equal(show_project_to_ai_root_from_hint(error_root), expected_show, "error root hint")
        _assert_equal(show_project_to_ai_root_from_hint(pending_dir), expected_show, "pending dir hint")
        _assert_equal(show_project_to_ai_root_from_hint(lessons_dir), expected_show, "lessons dir hint")
        _assert_equal(show_project_to_ai_root_from_hint(second_prompt_dir), expected_show, "second prompt hint")
        _assert_equal(show_project_to_ai_root_from_hint(daily_work), expected_show, "daily work hint")
        _assert_equal(show_project_to_ai_root_from_hint(nested_show_root), expected_show, "nested show root hint")
        _assert_equal(show_project_to_ai_root_from_hint(nested_error_root), expected_show, "nested error root hint")
        _assert_equal(show_project_to_ai_root_from_hint(nested_pending_dir), expected_show, "nested pending dir hint")
        _assert_equal(resolve_project_error_memory_root(project_root), error_root.resolve(strict=False), "canonical EM root")
        _assert_equal(resolve_project_error_memory_root(nested_show_root), error_root.resolve(strict=False), "nested show EM root")
        _assert_equal(resolve_project_error_memory_root(nested_error_root), error_root.resolve(strict=False), "nested error EM root")
        _assert_equal(resolve_project_error_memory_root(project_root / "project_error_memory"), error_root.resolve(strict=False), "legacy in-source EM root")

        result = bootstrap_error_memory_store(project_root)
        if "project_error_memory" not in result["paths"]["root"]:
            raise AssertionError("bootstrap did not target project_error_memory")

        _assert_equal(_WindowProjectRootMixin._normalize_project_root(str(project_root)), expected_project, "normalize source")
        _assert_equal(_WindowProjectRootMixin._normalize_project_root(str(show_root)), expected_project, "normalize show root")
        _assert_equal(_WindowProjectRootMixin._normalize_project_root(str(error_root)), expected_project, "normalize error root")
        _assert_equal(_WindowProjectRootMixin._normalize_project_root(str(second_prompt_dir)), expected_project, "normalize second prompt")
        _assert_equal(_WindowProjectRootMixin._normalize_project_root(str(daily_work)), expected_project, "normalize daily work")
        _assert_equal(_WindowProjectRootMixin._normalize_project_root(str(nested_show_root)), expected_project, "normalize nested show root")
        _assert_equal(_WindowProjectRootMixin._normalize_project_root(str(nested_error_root)), expected_project, "normalize nested error root")
        _assert_equal(_WindowProjectRootMixin._normalize_project_root(str(wrong_partial_root)), None, "reject partial root")
        _assert_equal(_WindowProjectRootMixin._normalize_project_root(str(wrong_show_root)), None, "reject orphan typo show root")

        _assert_not_exists(wrong_partial_root, "partial typo project root")
        _assert_not_exists(temp_root / "kanda_reasoner_error_me_show_project_to_AI" / "project_error_memory" / "schemas", "typo EM schema")

    print("VALIDATION OK: show-project-error-memory-path-guard-v1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
