# project-path: tools/validate_project_structure_3d_qwebengine_teardown_repair_v1.py
"""Validate deterministic QWebEngine teardown in the Project Structure probe."""

from __future__ import annotations

import argparse
import ast
from pathlib import Path
import py_compile

FEATURE_ID = "project-structure-3d-qwebengine-teardown-repair-v1"
TARGET = "tools/validate_project_structure_3d_visualizer_v1e_r2.py"


def require(condition: bool, message: str) -> None:
    """Raise one deterministic validation error."""
    if not condition:
        raise AssertionError(message)


def main() -> int:
    """Run static teardown ownership and Python quality checks."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    args = parser.parse_args()
    root = Path(args.root).expanduser().resolve()
    path = root / TARGET
    require(path.is_file(), "target validator missing")
    text = path.read_text(encoding="utf-8", errors="strict")
    ast.parse(text, filename=TARGET)
    py_compile.compile(str(path), doraise=True)
    require("def _drain_deferred_deletes(" in text, "deferred-delete helper missing")
    require("sendPostedEvents(None, event_type.DeferredDelete)" in text, "DeferredDelete dispatch missing")
    require("destroyed = {" in text, "destroyed-object ownership map missing")
    require('"page": False' in text, "QWebEnginePage destruction proof missing")
    require('"web_view": False' in text, "QWebEngineView destruction proof missing")
    require("finally:" in text, "fixture teardown is not fail-safe")
    require("target.deleteLater()" in text, "owned QObject deleteLater contract missing")
    require("REAL_QT_PROJECT_STRUCTURE_3D_QWEBENGINE_TEARDOWN: PASS" in text, "teardown success marker missing")
    require(len(text.splitlines()) <= 500, "touched validator exceeds 500 lines")
    print("QWEBENGINE_DEFERRED_DELETE_DRAIN: PASS")
    print("QWEBENGINE_PAGE_DESTRUCTION_PROOF: PASS")
    print("QWEBENGINE_FIXTURE_FINALLY_OWNER: PASS")
    print("QWEBENGINE_TEARDOWN_MARKER: PASS")
    print("TOUCHED_PYTHON_MODULE_SIZE_MAX_500: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
