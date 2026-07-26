
from __future__ import annotations

import subprocess
import sys
import zipfile
from pathlib import Path

FEATURE_ID = "startup-creator-canonical-zz-maintenance-v11"
MARKER = "VALIDATION OK: startup-creator-canonical-zz-maintenance-v11"
STATUS = "STATUS: IN_SYNC"
ZZ = "zz_read_only_if_modifying_startup_delivery.md"
PASTE = "paste_if_modify_startup_delivery.md"
NOTICE = "000_READ_TELL_AI_READ_BEFORE_ALL_FIRST.md"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def run_checked(args: list[str], cwd: Path) -> str:
    proc = subprocess.run(args, cwd=str(cwd), text=True, capture_output=True)
    output = (proc.stdout or "") + (proc.stderr or "")
    if proc.returncode != 0:
        raise AssertionError("Command failed with code " + str(proc.returncode) + ": " + " ".join(args) + "\n" + output)
    return output


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def check_zip_notice(zip_path: Path) -> None:
    require(zip_path.is_file(), "Missing ZIP: " + str(zip_path))
    with zipfile.ZipFile(zip_path, "r") as z:
        names = z.namelist()
        require(NOTICE in names, zip_path.name + " is missing " + NOTICE)
        notice = z.read(NOTICE).decode("utf-8-sig")
        require("tell_AI_read_before_all.md" in notice, zip_path.name + " notice does not mention tell_AI_read_before_all.md")
        require(ZZ in notice, zip_path.name + " notice does not mention canonical zz maintenance file")
        require("optional" in notice.lower(), zip_path.name + " notice does not mark maintenance file optional")
        require("If this file is missing, pass" in notice, zip_path.name + " notice does not include pass-if-missing rule")


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    workspace = root / "kanda_prompt_workspace"
    generator = workspace / "prompt_tools" / "sync_startup_routing_kernel_pack.py"
    startup_freeze_context = workspace / "prompt_tools" / "startup_freeze_context.py"
    wrapper = root / "kanda_reasoner_app" / "reasoner_tools_shell" / "runner_help" / "first_prompt_files_private_impl.py"

    for path in (generator, startup_freeze_context, wrapper):
        require(path.is_file(), "Missing required source file: " + str(path))

    run_checked([sys.executable, "-m", "py_compile", str(generator), str(startup_freeze_context), str(wrapper)], cwd=root)

    gen_text = read_text(generator)
    wrap_text = read_text(wrapper)
    require('MODIFY_STARTUP_DELIVERY_FILENAME = "' + ZZ + '"' in gen_text, "Generator does not assign canonical zz maintenance filename")
    require(ZZ in gen_text, "Generator does not contain canonical zz maintenance filename")
    require(ZZ in wrap_text, "Wrapper required-file check does not contain canonical zz maintenance filename")
    require(PASTE not in wrap_text, "Wrapper still requires old paste_if_modify filename")

    output_dir = root.parent / (root.name + "_show_project_to_AI") / "first_prompt_files"
    sync_output = run_checked([
        sys.executable,
        str(generator),
        "--sync",
        "--yes",
        "--workspace",
        str(workspace),
        "--output-dir",
        str(output_dir),
        "--project-root",
        str(root),
    ], cwd=workspace)
    require("SYNC COMPLETE" in sync_output, "Sync did not complete")
    require("Startup delivery maintenance file" in sync_output and ZZ in sync_output, "Sync output does not report zz maintenance file")

    expected_files = [
        "tell_AI_read_before_all.md",
        "first_prompts_to_ai.zip",
        "prompt_library.zip",
        ZZ,
    ]
    for name in expected_files:
        require((output_dir / name).is_file(), "Generated file is missing: " + name)
    require(not (output_dir / PASTE).exists(), "Old paste_if_modify maintenance file should not be generated")

    tell = read_text(output_dir / "tell_AI_read_before_all.md")
    require(tell.startswith("# STARTUP DELIVERY READ ORDER - READ tell_AI_read_before_all.md FIRST"), "tell_AI_read_before_all.md does not start with read-order guard")
    require(ZZ in tell, "tell_AI_read_before_all.md does not mention canonical zz maintenance file")
    require("optional" in tell.lower(), "tell_AI_read_before_all.md does not mark maintenance file optional")
    require("If this file is missing, pass" in tell, "tell_AI_read_before_all.md does not include pass-if-missing rule")
    require("prompt_library.zip - keep available" in tell, "tell_AI_read_before_all.md does not preserve prompt_library on-demand rule")

    maintenance = read_text(output_dir / ZZ)
    require("modifying startup delivery" in maintenance.lower(), "zz maintenance file does not describe startup-delivery maintenance use")
    require("normal startup" in maintenance.lower(), "zz maintenance file does not distinguish normal startup")

    check_zip_notice(output_dir / "first_prompts_to_ai.zip")
    check_zip_notice(output_dir / "prompt_library.zip")

    check_output = run_checked([
        sys.executable,
        str(generator),
        "--check",
        "--workspace",
        str(workspace),
        "--output-dir",
        str(output_dir),
        "--project-root",
        str(root),
    ], cwd=workspace)
    require(STATUS in check_output, "Post-sync check did not report STATUS: IN_SYNC\n" + check_output)

    # The GUI wrapper's required-file list must agree with the four generated files.
    for name in expected_files:
        require(name in wrap_text, "Wrapper does not require generated file: " + name)

    print(MARKER)
    print(STATUS)
    print("Generated canonical files:")
    for name in expected_files:
        print("- " + str(output_dir / name))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
