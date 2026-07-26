"""Validate Error Memory pending-intake live refresh v1."""

from __future__ import annotations

import argparse
import py_compile
import subprocess
import sys
from pathlib import Path

FEATURE_ID = "error-memory-gui-pending-intake-live-refresh-v1"
PATCH_NAME = "kanda_error_memory_pending_intake_live_refresh_v1_patch.zip"
VALIDATED_FILES = (
    "kanda_reasoner_app/error_memory_gui/error_memory_tab.py",
    "kanda_reasoner_app/error_memory_gui/_pending_live_refresh.py",
    "validation/test_error_memory_gui_pending_intake_live_refresh_v1.py",
    "tools/validate_error_memory_gui_pending_intake_live_refresh_v1.py",
)


def _default_zip_path(project_root: Path) -> Path:
    drive_root = Path(project_root.anchor or str(project_root))
    return drive_root / (project_root.name + "_delete_after_daily_work") / PATCH_NAME


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--zip-path", default="")
    args = parser.parse_args()

    project_root = Path(args.project_root).expanduser().resolve(strict=False)
    if not project_root.is_dir():
        raise SystemExit("Project root not found: " + str(project_root))

    for relative in VALIDATED_FILES:
        path = project_root / relative
        if not path.is_file():
            raise SystemExit("Missing validated file: " + relative)
        if path.suffix == ".py":
            py_compile.compile(str(path), doraise=True)
        if path.suffix == ".py" and len(path.read_text(encoding="utf-8").splitlines()) > 500:
            raise SystemExit("Module line limit exceeded: " + relative)

    test_path = project_root / "validation" / "test_error_memory_gui_pending_intake_live_refresh_v1.py"
    completed = subprocess.run(
        [sys.executable, str(test_path)],
        cwd=str(project_root),
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    output = completed.stdout or ""
    if output:
        print(output, end="" if output.endswith("\n") else "\n")
    if completed.returncode != 0:
        return completed.returncode

    zip_path = Path(args.zip_path).expanduser().resolve(strict=False) if args.zip_path else _default_zip_path(project_root)
    if not zip_path.is_file():
        raise SystemExit("Staged patch ZIP not found: " + str(zip_path))

    sys.path.insert(0, str(project_root))
    from kanda_reasoner_app.patch_governance.validator import validate_patch_zip

    report = validate_patch_zip(zip_path)
    if not report.get("ok"):
        raise SystemExit("ZIP contract validation failed.")

    print("PY_COMPILE: PASS")
    print("MODULE_SIZE_GATE: PASS")
    print("ZIP CONTRACT: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
