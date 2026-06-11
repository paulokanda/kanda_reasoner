"""Contract tests for the PA021B2 PySide6 async patch script."""

from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "workbench" / "_bundle_temp" / "PA021B2_APPLY_PROJECT_SYMBOL_ATLAS_PYSIDE6_ASYNC_REPAIR.py"


def _load_script_module():
    spec = importlib.util.spec_from_file_location("pa021b2_apply", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load PA021B2 patch script.")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_pa021b2_patch_script_contains_pyside6_async_block() -> None:
    text = SCRIPT.read_text(encoding="utf-8", errors="replace")
    assert "PA021B2_ENGINEERING_SAFETY_PYSIDE6_ASYNC_RUNNER" in text
    assert "from PySide6.QtCore import QTimer" in text
    assert "ThreadPoolExecutor" in text
    assert "tkinter" not in text.lower()


def test_pa021b2_patch_function_replaces_sync_runner() -> None:
    module = _load_script_module()
    sample = '''def create_engineering_safety_panel():\n    def run_command(command_name: str) -> None:\n        status_label.setText(f"Running: {command_name}")\n        output = run_engineering_safety_panel_cli_command(command_name, root)\n        output_box.setPlainText(output)\n\n    for section, tools in _group_tools_by_section(get_engineering_safety_panel_catalog()).items():\n        pass\n'''
    updated = module._patch_panel_text(sample)
    assert "PA021B2_ENGINEERING_SAFETY_PYSIDE6_ASYNC_RUNNER" in updated
    assert "command_executor.submit(" in updated
    assert "QTimer.singleShot" in updated


def main() -> int:
    test_pa021b2_patch_script_contains_pyside6_async_block()
    test_pa021b2_patch_function_replaces_sync_runner()
    print("PA021B2 PySide6 async patch script contract tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
