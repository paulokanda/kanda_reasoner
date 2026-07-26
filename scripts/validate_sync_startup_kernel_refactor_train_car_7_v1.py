# project-path: scripts/validate_sync_startup_kernel_refactor_train_car_7_v1.py
"""Validate Sync Startup Routing Kernel Refactor Train Car 7 v1."""

from __future__ import annotations

import inspect
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROMPT_TOOLS = PROJECT_ROOT / "kanda_prompt_workspace" / "prompt_tools"


def _ensure_import_paths() -> None:
    """Add project import roots only when the validator is executed."""

    for path in (PROMPT_TOOLS, PROJECT_ROOT):
        path_text = str(path)
        if path_text not in sys.path:
            sys.path.insert(0, path_text)


_ensure_import_paths()

from startup_kernel import paste_readme_text
from startup_kernel.paste_after_uploading_body import build_paste_after_uploading_content
from startup_kernel.readme_body import build_readme_content
from sync_startup_routing_kernel_pack import make_paste_after_uploading_file, make_readme


def line_count(path: Path) -> int:
    """Support line count behavior.
    
    Parameters
    ----------
    path : Path
        The file or folder path.
    
    Returns
    -------
    int
        The integer result.
    """
    
    return len(path.read_text(encoding="utf-8").splitlines())


def require(condition: bool, message: str) -> None:
    """Support require behavior.
    
    Parameters
    ----------
    condition : bool
        The condition value.
    message : str
        The message text.
    """
    
    if not condition:
        raise AssertionError(message)


def main() -> int:
    """Support main behavior.
    
    Returns
    -------
    int
        The integer status code.
    """
    
    startup_kernel = PROMPT_TOOLS / "startup_kernel"
    wrapper = startup_kernel / "paste_readme_text.py"
    paste_body = startup_kernel / "paste_after_uploading_body.py"
    readme_body = startup_kernel / "readme_body.py"

    for path in (wrapper, paste_body, readme_body):
        require(path.exists(), f"missing expected file: {path}")
        require(line_count(path) <= 500, f"module exceeds 500-line maximum: {path}")

    require(line_count(wrapper) <= 80, "paste_readme_text.py must remain a small public wrapper")
    require(line_count(paste_body) <= 400, "paste_after_uploading_body.py should remain under the 400-line ideal")
    require(line_count(readme_body) <= 400, "readme_body.py should remain under the 400-line ideal")

    wrapper_source = wrapper.read_text(encoding="utf-8")
    require("build_paste_after_uploading_content" in wrapper_source, "wrapper must delegate paste artifact content")
    require("build_readme_content" in wrapper_source, "wrapper must delegate README content")
    require("Second-upload project handoff rule" not in wrapper_source, "wrapper must not regain long paste body text")
    require("Startup Prompt Request Kernel Upload Pack" not in wrapper_source, "wrapper must not regain README body text")

    paste_source = inspect.getsource(build_paste_after_uploading_content)
    require("Second-upload project handoff rule" in paste_source, "paste body must preserve second-upload handoff rule")
    require("Prompt-library ZIP direct retrieval rule" in paste_source, "paste body must preserve prompt-library on-demand rule")
    require("Startup delivery maintenance rule" in paste_source, "paste body must preserve startup maintenance rule")

    readme_source = inspect.getsource(build_readme_content)
    require("Startup Prompt Request Kernel Upload Pack" in readme_source, "README body must preserve upload pack title")
    require("Companion prompt library ZIP" in readme_source, "README body must preserve prompt library companion section")

    expected = ["00_START_HERE_FOR_AI.md", "01_ai_prompt_request_canon.md"]
    filename, paste_content = make_paste_after_uploading_file(
        "2026-06-29", "2026-06-29T00:00:00Z", "first_prompts_to_ai.zip", expected
    )
    require(filename == "tell_AI_read_before_all.md", "paste artifact filename changed")
    require("STARTUP DELIVERY READ ORDER - READ tell_AI_read_before_all.md FIRST" in paste_content, "read order block missing")
    require("STARTUP PACK LOAD CHECK" in paste_content, "startup load check contract missing")
    require("PROJECT READY CHECK" in paste_content, "project ready check contract missing")
    require("prompt_library.zip" in paste_content, "prompt-library ZIP contract missing")

    records = [
        {"generated_filename": "00_START_HERE_FOR_AI.md", "role": "boot"},
        {"generated_filename": "01_ai_prompt_request_canon.md", "role": "canon"},
    ]
    readme = make_readme(
        "2026-06-29", "2026-06-29T00:00:00Z", "first_prompts_to_ai.zip", records, filename
    )
    require("Startup Prompt Request Kernel Upload Pack" in readme, "README title missing")
    require("00_START_HERE_FOR_AI.md" in readme, "README file rows missing")
    require("Next action: WAIT_FOR_TASK" in readme, "README second-upload next action missing")

    for exported_name in ("make_paste_after_uploading_file", "make_readme"):
        require(hasattr(paste_readme_text, exported_name), f"startup_kernel.paste_readme_text missing {exported_name}")

    print("VALIDATION OK: sync-startup-kernel-refactor-train-car-7-v1")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
