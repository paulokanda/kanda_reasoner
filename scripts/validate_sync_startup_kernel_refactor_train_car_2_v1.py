"""Validate startup kernel split refactor train car 2.

Train car 2 keeps sync_startup_routing_kernel_pack.py as a thin entrypoint and
splits the extracted start_here_text helper into smaller startup boot body/list
helpers without changing generated 00_START_HERE_FOR_AI.md content.
"""

from __future__ import annotations

import os
import py_compile
import subprocess
import sys
import tempfile
from pathlib import Path

__all__: list[str] = []


FEATURE_ID = "sync-startup-kernel-refactor-train-car-2-v1"
MAX_MODULE_LINES = 500
IDEAL_MODULE_LINES = 400

ROOT = Path(__file__).resolve().parents[1]
PROMPT_TOOLS = ROOT / "kanda_prompt_workspace" / "prompt_tools"
TARGET = PROMPT_TOOLS / "sync_startup_routing_kernel_pack.py"
HELPER_DIR = PROMPT_TOOLS / "startup_kernel"


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _line_count(path: Path) -> int:
    return len(_read(path).splitlines())


def _run(command: list[str], cwd: Path) -> str:
    env = os.environ.copy()
    existing_pythonpath = env.get("PYTHONPATH", "")
    paths = [str(PROMPT_TOOLS), str(ROOT)]
    if existing_pythonpath:
        paths.append(existing_pythonpath)
    env["PYTHONPATH"] = os.pathsep.join(paths)
    result = subprocess.run(
        command,
        cwd=str(cwd),
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if result.returncode != 0:
        raise AssertionError(
            "command failed with exit code "
            + str(result.returncode)
            + ": "
            + " ".join(command)
            + "\n"
            + result.stdout
        )
    return result.stdout


def validate_files_exist() -> list[Path]:
    expected = [
        TARGET,
        HELPER_DIR / "__init__.py",
        HELPER_DIR / "start_here_text.py",
        HELPER_DIR / "start_here_body_intro.py",
        HELPER_DIR / "start_here_body_routing.py",
        HELPER_DIR / "start_here_lists.py",
    ]
    for path in expected:
        _assert(path.exists(), "missing expected train car 2 file: " + str(path))
    return expected


def validate_module_sizes() -> None:
    for path in HELPER_DIR.glob("*.py"):
        count = _line_count(path)
        _assert(
            count <= MAX_MODULE_LINES,
            "module exceeds 500-line law: " + str(path) + " has " + str(count),
        )
    _assert(_line_count(TARGET) <= 200, "entrypoint should remain a thin wrapper")
    _assert(
        _line_count(HELPER_DIR / "start_here_text.py") <= 100,
        "start_here_text.py should be a small orchestrator after train car 2",
    )
    _assert(
        _line_count(HELPER_DIR / "start_here_body_routing.py") <= IDEAL_MODULE_LINES,
        "routing body helper should stay under the 400-line ideal",
    )


def validate_compile(paths: list[Path]) -> None:
    for path in list(HELPER_DIR.glob("*.py")) + [TARGET, Path(__file__)]:
        py_compile.compile(str(path), doraise=True)
    for path in paths:
        py_compile.compile(str(path), doraise=True)


def validate_start_here_split_shape() -> None:
    text = _read(HELPER_DIR / "start_here_text.py")
    required_fragments = [
        "make_start_here_intro_section",
        "make_start_here_routing_section",
        "build_active_bridge_report",
        "_append_prompt_authoring_overrides",
    ]
    for fragment in required_fragments:
        _assert(fragment in text, "start_here_text.py missing fragment: " + fragment)

    forbidden_fragments = [
        "## Prompt library ZIP direct retrieval rule",
        "## Startup delivery maintenance rule",
        "## Routing examiner mode",
    ]
    for fragment in forbidden_fragments:
        _assert(fragment not in text, "large body text still lives in start_here_text.py: " + fragment)


def validate_generated_start_here_content() -> None:
    sys.path.insert(0, str(PROMPT_TOOLS))
    from startup_kernel.start_here_text import make_start_here_file  # noqa: PLC0415

    filename, content = make_start_here_file("CERT", "GEN", ["01_a.md", "02_b.md"])
    _assert(filename == "00_START_HERE_FOR_AI.md", "stable boot filename regressed")

    required_fragments = [
        "STARTUP PACK LOAD CHECK",
        "Beginning-of-day active bridges:",
        "Code Module Size Bridge",
        "Terminal Cleanup Bridge",
        "Prompt library ZIP direct retrieval rule",
        "Startup delivery maintenance rule",
        "Routing examiner mode",
        "Mandatory prompt-authoring RG-015 exact response skeleton loaded.",
        "Mandatory prompt-authoring RG-015 hard override skeleton loaded.",
    ]
    for fragment in required_fragments:
        _assert(fragment in content, "generated boot file missing fragment: " + fragment)


def validate_real_sync_cycle() -> None:
    with tempfile.TemporaryDirectory(prefix="kanda_sync_kernel_refactor_car2_") as tmp_name:
        out_dir = Path(tmp_name) / "first_prompt_files"
        sync_output = _run(
            [
                sys.executable,
                str(TARGET),
                "--sync",
                "--yes",
                "--project-root",
                str(ROOT),
                "--output-dir",
                str(out_dir),
            ],
            cwd=ROOT,
        )
        _assert(
            "Workspace root: " + str(ROOT / "kanda_prompt_workspace") in sync_output,
            "auto-detected workspace root was not kanda_prompt_workspace",
        )
        _assert("startup_kernel" not in sync_output.split("Workspace root:", 1)[1].splitlines()[0],
                "workspace root still points inside startup_kernel")
        _assert("STATUS: IN_SYNC" in sync_output, "sync output did not finish in sync")
        _assert((out_dir / "first_prompts_to_ai.zip").exists(), "startup ZIP not generated")
        _assert((out_dir / "tell_AI_read_before_all.md").exists(), "read-before-all file not generated")

        check_output = _run(
            [
                sys.executable,
                str(TARGET),
                "--check",
                "--project-root",
                str(ROOT),
                "--output-dir",
                str(out_dir),
            ],
            cwd=ROOT,
        )
        _assert(
            "Workspace root: " + str(ROOT / "kanda_prompt_workspace") in check_output,
            "auto-detected workspace root regressed during check",
        )
        _assert("STATUS: IN_SYNC" in check_output, "post-sync check is not in sync")


def main() -> int:
    paths = validate_files_exist()
    validate_module_sizes()
    validate_compile(paths)
    validate_start_here_split_shape()
    validate_generated_start_here_content()
    validate_real_sync_cycle()
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
