"""Validate Error Memory dynamic project_error_memory autoload v12."""

from __future__ import annotations

import sys
from pathlib import Path


FEATURE_ID = "error-memory-gui-dynamic-project-error-memory-autoload-v12"
PENDING_DIR_NAME = "pending_ai_assisted_error_lesson_intake"
PENDING_FILE_NAME = "KANDA_ERROR_LESSON_JSON_freeze_intake_script_syntaxerror_exitcode_guard_v12.txt"


def _project_root_from_arg() -> Path:
    if len(sys.argv) >= 2:
        return Path(sys.argv[1]).expanduser().resolve(strict=False)
    return Path.cwd().resolve(strict=False)


def _expected_show_project_root(project_root: Path) -> Path:
    if project_root.name.endswith("_show_project_to_AI"):
        return project_root
    if project_root.drive:
        return Path(project_root.anchor) / (project_root.name + "_show_project_to_AI")
    return project_root.parent / (project_root.name + "_show_project_to_AI")


def main() -> int:
    project_root = _project_root_from_arg()
    tab_path = project_root / "kanda_reasoner_app" / "error_memory_gui" / "error_memory_tab.py"
    paths_path = project_root / "kanda_reasoner_app" / "error_memory" / "paths.py"
    if not tab_path.exists():
        raise AssertionError(f"Missing Error Memory GUI source: {tab_path}")
    if not paths_path.exists():
        raise AssertionError(f"Missing Error Memory paths source: {paths_path}")

    tab_source = tab_path.read_text(encoding="utf-8")
    paths_source = paths_path.read_text(encoding="utf-8")

    tab_fragments = [
        "def _show_project_to_ai_root_for_pending_intake",
        "folder_name = resolved.name + \"_show_project_to_AI\"",
        "show_root / \"project_error_memory\" / PENDING_AI_ASSISTED_INTAKE_DIR_NAME",
        "for pending_dir in self._pending_ai_assisted_error_lesson_intake_dirs()",
        "self.raw_error_edit.setPlainText(formatted_text)",
        "self.received_preview_edit.setPlainText(json.dumps(lesson",
    ]
    for fragment in tab_fragments:
        if fragment not in tab_source:
            raise AssertionError(f"Missing v12 GUI fragment: {fragment}")

    paths_fragments = [
        "def resolve_show_project_to_ai_root",
        "project_name_from_root(root) + \"_show_project_to_AI\"",
        "return resolve_show_project_to_ai_root(selected_project_root) / PROJECT_ERROR_MEMORY_DIR",
        "return resolve_show_project_to_ai_root(selected_project_root) / SECOND_PROMPT_FILES_DIR",
    ]
    for fragment in paths_fragments:
        if fragment not in paths_source:
            raise AssertionError(f"Missing v12 paths fragment: {fragment}")

    forbidden_paths = [
        "return project_analysis_evidence_root(selected_project_root) / PROJECT_ERROR_MEMORY_DIR",
        "return project_analysis_evidence_root(selected_project_root) / SECOND_PROMPT_FILES_DIR",
    ]
    for fragment in forbidden_paths:
        if fragment in paths_source:
            raise AssertionError("Old project_analysis_evidence Error Memory path remains active.")

    external_pending = (
        _expected_show_project_root(project_root)
        / "project_error_memory"
        / PENDING_DIR_NAME
        / PENDING_FILE_NAME
    )
    local_pending = project_root / "project_error_memory" / PENDING_DIR_NAME / PENDING_FILE_NAME

    missing = [str(path) for path in (external_pending, local_pending) if not path.exists()]
    if missing:
        raise AssertionError("Missing staged pending intake file(s): " + "; ".join(missing))

    for path in (external_pending, local_pending):
        text = path.read_text(encoding="utf-8-sig", errors="replace")
        checks = [
            "KANDA_ERROR_LESSON_JSON_BEGIN",
            "KANDA_ERROR_LESSON_JSON_END",
            "validation_evidence =",
            "SyntaxError: invalid syntax",
            "FREEZE INTAKE PREP OK",
            '"status": "active"',
            '"operation_phase": "install"',
        ]
        for check in checks:
            if check not in text:
                raise AssertionError(f"Pending intake file {path} missing content: {check}")

    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: DYNAMIC_PROJECT_ERROR_MEMORY_AUTOLOAD_READY")
    print("Dynamic project_error_memory pending intake staged here:")
    print(str(external_pending))
    print("Local fallback pending intake staged here:")
    print(str(local_pending))
    print("Expected GUI result after restart/opening Error Memory tab:")
    print("- AI-assisted error lesson intake is populated")
    print("- Error Editor is populated")
    print("- Lessons is unchanged until Memorize Error is clicked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
