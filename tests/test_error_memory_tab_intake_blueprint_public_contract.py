"""Characterization tests for Error Memory intake blueprint helpers."""
from __future__ import annotations

from pathlib import Path

from kanda_reasoner_app.error_memory_gui import _intake_blueprint


def _write_templates(project_root: Path) -> Path:
    template_dir = (
        project_root
        / "kanda_prompt_workspace"
        / "prompt_library"
        / "ACTIVE_PROMPTS"
        / "12_generalized_project_canons"
    )
    template_dir.mkdir(parents=True, exist_ok=True)
    (template_dir / "error_memory_active_ready_json_template.md").write_text(
        "ACTIVE READY TEMPLATE BODY\n",
        encoding="utf-8",
    )
    (template_dir / "error_memory_model_template.md").write_text(
        "MODEL TEMPLATE BODY\n",
        encoding="utf-8",
    )
    return template_dir


def test_intake_blueprint_helper_is_private_non_gui_contract() -> None:
    source = Path(_intake_blueprint.__file__).read_text(encoding="utf-8")

    assert "PySide" not in source
    assert "Qt" not in source
    assert "error_memory_tab" not in source
    assert "ErrorMemoryTab" not in source


def test_error_memory_prompt_template_dir_prefers_project_root(tmp_path: Path) -> None:
    template_dir = _write_templates(tmp_path)

    assert _intake_blueprint.error_memory_prompt_template_dir(
        tmp_path,
        module_file=__file__,
    ) == template_dir


def test_error_lesson_intake_blueprint_clipboard_text_includes_templates_and_context(tmp_path: Path) -> None:
    _write_templates(tmp_path)

    text = _intake_blueprint.error_lesson_intake_blueprint_clipboard_text(
        tmp_path,
        context_text="RAW ERROR CONTEXT",
        module_file=__file__,
    )

    assert text.startswith("ERROR MEMORY AI INTAKE REQUEST")
    assert "Return exactly one KANDA_ERROR_LESSON_JSON_BEGIN / KANDA_ERROR_LESSON_JSON_END block" in text
    assert "ERROR OR DRAFT CONTEXT TO CONVERT:" in text
    assert "RAW ERROR CONTEXT" in text
    assert "--- BEGIN error_memory_active_ready_json_template.md ---" in text
    assert "ACTIVE READY TEMPLATE BODY" in text
    assert "--- BEGIN error_memory_model_template.md ---" in text
    assert "MODEL TEMPLATE BODY" in text
    assert text.endswith("\n")
