# project-path: tools/validate_brick_wall_q30_human_confirmation_freeze_protection_real_qt_v1.py
"""Real-Qt Q30 confirmation invalidation validation."""
from __future__ import annotations

import argparse
import os
from pathlib import Path
from types import SimpleNamespace

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

try:
    from PySide6.QtWidgets import QApplication, QLineEdit, QPushButton, QTextEdit
except Exception as exc:
    raise SystemExit("Q30_REAL_QT_PYSIDE6_REQUIRED: FAIL - " + str(exc))

from kanda_reasoner_app.freeze_after_update_gui.local_freeze_confirmation_binding import (
    FreezeActionStateController,
    bind_freeze_confirmation_invalidation,
    build_freeze_confirmation_binding,
    collect_freeze_form_inputs,
    freeze_confirmation_binding_matches,
)


def gate(label: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(label + ": FAIL")
    print(label + ": PASS")


def main() -> int:
    parser=argparse.ArgumentParser()
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    args=parser.parse_args()
    root=args.project_root.expanduser().resolve(strict=True)
    app=QApplication.instance() or QApplication([])
    line_names=("feature_title","primary_box","box_type")
    text_names=("validated_files","generated_files","protected_paths","do_not_regress","validation_evidence","known_warnings","planned_next_step","notes")
    values={name+"_edit":QLineEdit(name) for name in line_names}
    values.update({name+"_edit":QTextEdit(name) for name in text_names})
    widgets=SimpleNamespace(**values)
    project_root_edit=QLineEdit(str(root))
    confirm=QPushButton(); ignore=QPushButton()
    state=FreezeActionStateController(confirm_button=confirm,ignore_button=ignore,confirm_enabled_style="on",ignore_enabled_style="ignore",disabled_style="off")
    invalidations=[]
    def invalidate(*_args):
        invalidations.append(True)
        state.disable("changed")
    count=bind_freeze_confirmation_invalidation(widgets, project_root_edit, invalidate)
    inputs=collect_freeze_form_inputs(widgets)
    binding=build_freeze_confirmation_binding(project_root_edit.text(), inputs)
    state.set_state(True, True)
    gate("Q30_REAL_QT_INITIAL_CONFIRM_ENABLED", confirm.isEnabled())
    widgets.validation_evidence_edit.setPlainText("changed evidence")
    app.processEvents()
    gate("Q30_REAL_QT_SOURCE_EVIDENCE_INVALIDATES", not confirm.isEnabled() and bool(invalidations))
    inputs=collect_freeze_form_inputs(widgets)
    binding=build_freeze_confirmation_binding(project_root_edit.text(), inputs)
    state.set_state(True, True)
    project_root_edit.setText(str(root / "other"))
    app.processEvents()
    gate("Q30_REAL_QT_PROJECT_ROOT_INVALIDATES", not confirm.isEnabled())
    gate("Q30_REAL_QT_ALL_REVIEWED_SIGNALS_BOUND", count == 12)
    gate("Q30_REAL_QT_STALE_BINDING_REJECTED", not freeze_confirmation_binding_matches(binding, project_root_edit.text(), collect_freeze_form_inputs(widgets))[0])
    gate("Q30_REAL_QT_CONFIRMATION_INVALIDATION", True)
    print("VALIDATION OK: brick-wall-q30-human-confirmation-freeze-protection-real-qt-v1")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
