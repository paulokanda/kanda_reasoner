"""Validate Sync Startup Kernel Refactor Train Car 5 v1.

This validation keeps the refactor focused on CLI ownership cleanup.
It proves that cli.py remains the public command-line entrypoint while
read-only check and sync command helpers live in smaller focused modules.
"""

from __future__ import annotations

import importlib
import tempfile
from pathlib import Path
import sys

__all__: list[str] = []


FEATURE_ID = "sync-startup-kernel-refactor-train-car-5-v1"
MAX_MODULE_LINES = 500
IDEAL_MODULE_LINES = 400


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _line_count(path: Path) -> int:
    return len(_read_text(path).splitlines())


def validate_files() -> None:
    root = _repo_root()
    prompt_tools = root / "kanda_prompt_workspace" / "prompt_tools"
    startup_kernel = prompt_tools / "startup_kernel"
    entrypoint = prompt_tools / "sync_startup_routing_kernel_pack.py"
    cli = startup_kernel / "cli.py"
    cli_check = startup_kernel / "cli_check.py"
    cli_sync = startup_kernel / "cli_sync.py"

    for path in (entrypoint, cli, cli_check, cli_sync):
        _assert(path.exists(), "missing expected file: " + str(path))
        _assert(_line_count(path) <= MAX_MODULE_LINES, "module exceeds max line count: " + str(path))
        _assert(_line_count(path) <= IDEAL_MODULE_LINES, "module exceeds ideal line count: " + str(path))

    cli_text = _read_text(cli)
    check_text = _read_text(cli_check)
    sync_text = _read_text(cli_sync)
    entrypoint_text = _read_text(entrypoint)

    _assert("from startup_kernel.cli_check import command_check" in cli_text,
            "cli.py must import command_check from cli_check.py")
    _assert("from startup_kernel.cli_sync import command_ensure_sync, confirm_sync" in cli_text,
            "cli.py must import sync helpers from cli_sync.py")
    _assert("def command_check(" not in cli_text,
            "cli.py must not redefine command_check")
    _assert("def confirm_sync(" not in cli_text,
            "cli.py must not redefine confirm_sync")
    _assert("def command_ensure_sync(" not in cli_text,
            "cli.py must not redefine command_ensure_sync")
    _assert("def parse_args(" in cli_text, "cli.py must keep parse_args")
    _assert("def main(" in cli_text, "cli.py must keep main")

    _assert("def command_check(" in check_text,
            "cli_check.py must own command_check")
    _assert("def confirm_sync(" in sync_text,
            "cli_sync.py must own confirm_sync")
    _assert("def command_ensure_sync(" in sync_text,
            "cli_sync.py must own command_ensure_sync")
    _assert("from startup_kernel.cli_check import command_check" in sync_text,
            "cli_sync.py must reuse command_check from cli_check.py")

    _assert("from startup_kernel.cli import command_check, command_ensure_sync, confirm_sync, main, parse_args" in entrypoint_text,
            "sync_startup_routing_kernel_pack.py must keep the CLI compatibility import surface")
    _assert('"command_check"' in entrypoint_text,
            "entrypoint __all__ must keep command_check")
    _assert('"command_ensure_sync"' in entrypoint_text,
            "entrypoint __all__ must keep command_ensure_sync")
    _assert('"confirm_sync"' in entrypoint_text,
            "entrypoint __all__ must keep confirm_sync")
    _assert('"parse_args"' in entrypoint_text,
            "entrypoint __all__ must keep parse_args")
    _assert('"main"' in entrypoint_text,
            "entrypoint __all__ must keep main")


def validate_public_import_surface() -> None:
    root = _repo_root()
    prompt_tools = root / "kanda_prompt_workspace" / "prompt_tools"
    sys.path.insert(0, str(prompt_tools))

    cli = importlib.import_module("startup_kernel.cli")
    cli_check = importlib.import_module("startup_kernel.cli_check")
    cli_sync = importlib.import_module("startup_kernel.cli_sync")
    entrypoint = importlib.import_module("sync_startup_routing_kernel_pack")

    _assert(cli.command_check is cli_check.command_check,
            "cli.py must re-export command_check from cli_check.py")
    _assert(cli.command_ensure_sync is cli_sync.command_ensure_sync,
            "cli.py must re-export command_ensure_sync from cli_sync.py")
    _assert(cli.confirm_sync is cli_sync.confirm_sync,
            "cli.py must re-export confirm_sync from cli_sync.py")
    _assert(entrypoint.command_check is cli_check.command_check,
            "entrypoint must preserve command_check public import surface")
    _assert(entrypoint.command_ensure_sync is cli_sync.command_ensure_sync,
            "entrypoint must preserve command_ensure_sync public import surface")
    _assert(entrypoint.confirm_sync is cli_sync.confirm_sync,
            "entrypoint must preserve confirm_sync public import surface")

    args = cli.parse_args([])
    _assert(args.check is True, "parse_args([]) must keep the safe --check default")


def validate_cli_dry_run() -> None:
    root = _repo_root()
    prompt_tools = root / "kanda_prompt_workspace" / "prompt_tools"
    sys.path.insert(0, str(prompt_tools))

    entrypoint = importlib.import_module("sync_startup_routing_kernel_pack")
    with tempfile.TemporaryDirectory(prefix="kanda_train_car_5_validation_") as temp_name:
        output_dir = Path(temp_name) / "first_prompt_files"
        code = entrypoint.main(["--dry-run", "--output-dir", str(output_dir)])
        _assert(code == 0, "entrypoint dry-run command must return 0")


def main() -> int:
    validate_files()
    validate_public_import_surface()
    validate_cli_dry_run()
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
