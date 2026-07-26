"""Validate Warning Local AI Resolver v2r1 fresh-queue and verified-apply repair."""

from __future__ import annotations

import ast
from pathlib import Path
import subprocess
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]

FEATURE_ID = "architecture-review-warning-local-ai-resolver-v2r1-state-refresh-verified-apply"
OWNERS = (
    "kanda_reasoner_app/manage_architecture/architecture_audit_actions_gui.py",
    "kanda_reasoner_app/manage_architecture/warning_heuristic_resolver_qt_controller.py",
    "kanda_reasoner_app/manage_architecture/warning_heuristic_resolver_qt_worker.py",
    "kanda_reasoner_app/manage_architecture/warning_model_live_audit.py",
    "kanda_reasoner_app/manage_architecture/warning_model_test_apply.py",
    "kanda_reasoner_app/manage_architecture/warning_model_test_protection_formatting.py",
)


def marker(name: str) -> None:
    print(name + ": PASS")


def main() -> int:
    project_root_text = str(PROJECT_ROOT)
    if project_root_text not in sys.path:
        sys.path.insert(0, project_root_text)
    for relative in OWNERS:
        path = PROJECT_ROOT / relative
        ast.parse(path.read_text(encoding="utf-8-sig"), filename=relative)
        if len(path.read_text(encoding="utf-8-sig").splitlines()) > 500:
            raise AssertionError("MODULE_SIZE_GATE failed: " + relative)
    marker("WARNING_MODEL_V2R1_PYTHON_SYNTAX")
    marker("WARNING_MODEL_V2R1_MODULE_SIZE_GATE")

    gui = (PROJECT_ROOT / OWNERS[0]).read_text(encoding="utf-8-sig")
    assert "self._output.toPlainText()" not in gui[gui.index("def run_warning_model_resolver"):gui.index("def _on_warning_model_progress")]
    assert "queue_model_apply_verify(plan)" in gui
    assert "format_model_apply_verification_result" in gui
    marker("WARNING_MODEL_FRESH_QUEUE_NOT_GUI_TEXT")
    marker("WARNING_MODEL_BACKGROUND_APPLY_VERIFY_QUEUE")

    worker = (PROJECT_ROOT / OWNERS[2]).read_text(encoding="utf-8-sig")
    assert "run_fresh_test_protection_audit" in worker
    assert "apply_and_verify_model_plan" in worker
    marker("WARNING_MODEL_SHARED_QTHREAD_FRESH_AUDIT_AND_VERIFY")

    apply_text = (PROJECT_ROOT / OWNERS[4]).read_text(encoding="utf-8-sig")
    assert "changed_paths & link_paths" in apply_text
    assert "changed_paths & mutation_paths" in apply_text
    marker("WARNING_MODEL_ACTUAL_WRITE_COUNTS_ONLY")

    test_path = PROJECT_ROOT / "tests/test_warning_model_state_refresh_verified_apply.py"
    completed = subprocess.run(
        [sys.executable, str(test_path)],
        cwd=str(PROJECT_ROOT),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if completed.returncode != 0:
        print(completed.stdout)
        print(completed.stderr)
        raise AssertionError("Focused state refresh tests failed")
    marker("WARNING_MODEL_STATE_REFRESH_VERIFIED_APPLY_TESTS")
    print("VALIDATION OK: " + FEATURE_ID)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
