"""Validate startup kernel split refactor train car 1.

This validation checks that sync_startup_routing_kernel_pack.py was reduced to a
thin entrypoint and that extracted helper modules remain below the 500-line
large-module ceiling. It also runs a real startup sync/check cycle in a temporary
output directory.
"""

from __future__ import annotations

import os
import py_compile
import subprocess
import sys
import tempfile
from pathlib import Path

__all__: list[str] = []


FEATURE_ID = "sync-startup-kernel-refactor-train-car-1-v1"
MAX_MODULE_LINES = 500

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
        HELPER_DIR / "boot_text.py",
        HELPER_DIR / "cli.py",
        HELPER_DIR / "constants.py",
        HELPER_DIR / "core_helpers.py",
        HELPER_DIR / "maintenance_text.py",
        HELPER_DIR / "paste_readme_text.py",
        HELPER_DIR / "prompt_library_zip.py",
        HELPER_DIR / "read_order.py",
        HELPER_DIR / "start_here_text.py",
        HELPER_DIR / "zip_delivery.py",
    ]
    for path in expected:
        _assert(path.exists(), "missing expected refactor file: " + str(path))
    return expected


def validate_module_sizes(paths: list[Path]) -> None:
    for path in paths:
        count = _line_count(path)
        _assert(
            count <= MAX_MODULE_LINES,
            "module exceeds 500-line law: " + str(path) + " has " + str(count),
        )
    _assert(
        _line_count(TARGET) <= 200,
        "entrypoint should remain a thin wrapper after refactor",
    )


def validate_compile(paths: list[Path]) -> None:
    for path in paths + [Path(__file__)]:
        py_compile.compile(str(path), doraise=True)


def validate_entrypoint_shape() -> None:
    text = _read(TARGET)
    required_fragments = [
        "from startup_kernel.cli import",
        "from startup_kernel.zip_delivery import",
        "raise SystemExit(main(sys.argv[1:]))",
        "__all__ = [",
    ]
    for fragment in required_fragments:
        _assert(fragment in text, "entrypoint missing fragment: " + fragment)

    forbidden_fragments = [
        "def make_zip(",
        "def make_start_here_file(",
        "def validate_generated_zip_contract(",
        "def make_prompt_library_zip(",
    ]
    for fragment in forbidden_fragments:
        _assert(fragment not in text, "entrypoint still owns moved function: " + fragment)


def validate_import_surface() -> None:
    sys.path.insert(0, str(PROMPT_TOOLS))
    import sync_startup_routing_kernel_pack as module  # noqa: PLC0415

    expected_names = [
        "make_zip",
        "make_start_here_file",
        "make_prompt_library_zip",
        "validate_generated_zip_contract",
        "make_startup_artifact_read_order_notice",
    ]
    for name in expected_names:
        _assert(hasattr(module, name), "public import surface missing: " + name)

    notice = module.make_startup_artifact_read_order_notice("test.md")
    _assert("READ tell_AI_read_before_all.md FIRST" in notice, "read-order notice regressed")


def validate_real_sync_cycle() -> None:
    with tempfile.TemporaryDirectory(prefix="kanda_sync_kernel_refactor_") as tmp_name:
        out_dir = Path(tmp_name) / "first_prompt_files"
        sync_output = _run(
            [
                sys.executable,
                str(TARGET),
                "--sync",
                "--yes",
                "--workspace",
                str(ROOT / "kanda_prompt_workspace"),
                "--project-root",
                str(ROOT),
                "--output-dir",
                str(out_dir),
            ],
            cwd=ROOT,
        )
        _assert("STATUS: IN_SYNC" in sync_output, "sync output did not finish in sync")
        _assert((out_dir / "first_prompts_to_ai.zip").exists(), "startup ZIP not generated")
        _assert((out_dir / "prompt_library.zip").exists(), "prompt library ZIP not generated")
        _assert((out_dir / "tell_AI_read_before_all.md").exists(), "read-before-all file not generated")

        check_output = _run(
            [
                sys.executable,
                str(TARGET),
                "--check",
                "--workspace",
                str(ROOT / "kanda_prompt_workspace"),
                "--project-root",
                str(ROOT),
                "--output-dir",
                str(out_dir),
            ],
            cwd=ROOT,
        )
        _assert("STATUS: IN_SYNC" in check_output, "post-sync check is not in sync")


def main() -> int:
    paths = validate_files_exist()
    validate_module_sizes(paths)
    validate_compile(paths)
    validate_entrypoint_shape()
    validate_import_surface()
    validate_real_sync_cycle()
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
