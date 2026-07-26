"""Validate Error Memory pending intake host-trigger autoload v13 without launching PySide."""
from __future__ import annotations

import sys
from pathlib import Path

FEATURE_ID = "error-memory-gui-pending-intake-host-trigger-v13"
PENDING_NAME = "KANDA_ERROR_LESSON_JSON_freeze_intake_script_syntaxerror_exitcode_guard_v13.txt"


def _read(path: Path) -> str:
    if not path.exists():
        raise AssertionError(f"Missing file: {path}")
    return path.read_text(encoding="utf-8", errors="replace")


def _show_project_root(project_root: Path) -> Path:
    if project_root.drive:
        return Path(project_root.drive + "\\") / (project_root.name + "_show_project_to_AI")
    return project_root.parent / (project_root.name + "_show_project_to_AI")


def main(argv: list[str]) -> int:
    project_root = Path(argv[1]).expanduser().resolve(strict=False) if len(argv) > 1 else Path.cwd().resolve(strict=False)
    em_tab = project_root / "kanda_reasoner_app" / "error_memory_gui" / "error_memory_tab.py"
    lazy_tabs = project_root / "kanda_reasoner_app" / "reasoner_tools_gui_shell" / "lazy_tabs.py"

    em_text = _read(em_tab)
    lazy_text = _read(lazy_tabs)

    required_em_markers = [
        "from PySide6.QtCore import Qt, QTimer, QUrl",
        "def _pending_intake_dirs_for_root_hint",
        "def _candidate_pending_ai_assisted_intake_dirs",
        "def load_pending_ai_assisted_error_lesson_intake_now",
        "Path(__file__).resolve(strict=False).parents[2]",
        "root.name.endswith(\"_show_project_to_AI\")",
        "root / \"project_error_memory\" / PENDING_AI_ASSISTED_INTAKE_DIR_NAME",
        "resolve_project_error_memory_root(root) / PENDING_AI_ASSISTED_INTAKE_DIR_NAME",
        "self.raw_error_edit.setPlainText(formatted_text)",
        "self.received_preview_edit.setPlainText(json.dumps(lesson",
        "QTimer.singleShot(250, self.load_pending_ai_assisted_error_lesson_intake_now)",
    ]
    for marker in required_em_markers:
        if marker not in em_text:
            raise AssertionError(f"Missing Error Memory tab marker: {marker}")

    required_lazy_markers = [
        "pending_loader = getattr(widget, \"load_pending_ai_assisted_error_lesson_intake_now\", None)",
        "self._on_loaded(self.spec, widget)",
        "QTimer.singleShot(0, pending_loader)",
        "QTimer.singleShot(250, pending_loader)",
    ]
    for marker in required_lazy_markers:
        if marker not in lazy_text:
            raise AssertionError(f"Missing lazy tab host marker: {marker}")

    # This validation verifies the installed pending file is in the dynamic per-project folder.
    show_root = _show_project_root(project_root)
    dynamic_pending = show_root / "project_error_memory" / "pending_ai_assisted_error_lesson_intake" / PENDING_NAME
    local_fallback = project_root / "project_error_memory" / "pending_ai_assisted_error_lesson_intake" / PENDING_NAME

    if not dynamic_pending.exists():
        raise AssertionError(f"Missing dynamic pending intake file: {dynamic_pending}")
    if not local_fallback.exists():
        raise AssertionError(f"Missing local fallback pending intake file: {local_fallback}")

    pending_text = dynamic_pending.read_text(encoding="utf-8-sig", errors="replace")
    for marker in [
        "KANDA_ERROR_LESSON_JSON_BEGIN",
        "KANDA_ERROR_LESSON_JSON_END",
        "validation_evidence =",
        "SyntaxError: invalid syntax",
        "FREEZE INTAKE PREP OK",
    ]:
        if marker not in pending_text:
            raise AssertionError(f"Pending lesson does not preserve marker: {marker}")

    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: HOST_TRIGGER_AUTOLOAD_READY")
    print("Dynamic pending intake file:")
    print(dynamic_pending)
    print("Expected GUI result after full app restart/open Error Memory tab:")
    print("- AI-assisted error lesson intake is populated first")
    print("- Error Editor is populated second")
    print("- Lessons is unchanged until Memorize Error is clicked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
