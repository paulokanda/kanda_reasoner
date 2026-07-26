
"""Validate startup artifact read-order guard v3."""

from __future__ import annotations

import subprocess
import sys
import zipfile
from pathlib import Path

EXPECTED_MARKER = "STARTUP DELIVERY READ ORDER - READ tell_AI_read_before_all.md FIRST"
NOTICE_FILE = "000_READ_TELL_AI_READ_BEFORE_ALL_FIRST.md"
TELL_FILE = "tell_AI_read_before_all.md"
STARTUP_ZIP = "first_prompts_to_ai.zip"
PROMPT_LIBRARY_ZIP = "prompt_library.zip"
MAINTENANCE_FILE = "zz_read_only_if_modifying_startup_delivery.md"
OLD_MAINTENANCE_FILE = "paste_if_modify_startup_delivery.md"


def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def default_first_prompt_output_dir(root: Path) -> Path:
    anchor = root.anchor or str(root.parent)
    slug = root.name.strip().lower() or "project"
    if anchor.endswith(":\\") or anchor.endswith(":/"):
        base = Path(anchor) / f"{slug}_show_project_to_AI"
    elif anchor.endswith(":"):
        base = Path(f"{anchor}\\{slug}_show_project_to_AI")
    else:
        base = Path(anchor) / f"{slug}_show_project_to_AI"
    return base / "first_prompt_files"


def run_checked(args: list[str], cwd: Path) -> str:
    proc = subprocess.run(args, cwd=str(cwd), text=True, capture_output=True)
    output = (proc.stdout or "") + (proc.stderr or "")
    if proc.returncode != 0:
        raise AssertionError(
            "Command failed with code " + str(proc.returncode) + ": " + " ".join(args) + "\n" + output
        )
    return output


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def assert_read_order_text(text: str, label: str) -> None:
    require(EXPECTED_MARKER in text, f"Missing read-order marker in {label}.")
    require("1. tell_AI_read_before_all.md" in text, f"Missing first read step in {label}.")
    require("2. first_prompts_to_ai.zip" in text, f"Missing startup ZIP second step in {label}.")
    require("3. prompt_library.zip" in text, f"Missing prompt library third step in {label}.")
    require("4. zz_read_only_if_modifying_startup_delivery.md" in text, f"Missing maintenance fourth step in {label}.")
    require("optional" in text.lower(), f"Maintenance file is not marked optional in {label}.")
    require(
        "If this file is missing, continue" in text or "If missing, pass" in text,
        f"Maintenance missing-pass rule not explicit in {label}.",
    )


def inspect_zip(path: Path, label: str) -> None:
    with zipfile.ZipFile(path, "r") as z:
        names = z.namelist()
        require(names, f"{label} is empty.")
        require(names[0] == NOTICE_FILE, f"{label} first ZIP entry must be {NOTICE_FILE}, got {names[0]!r}.")
        notice = z.read(NOTICE_FILE).decode("utf-8-sig")
        assert_read_order_text(notice, f"{label}:{NOTICE_FILE}")
        if label == STARTUP_ZIP:
            require("00_START_HERE_FOR_AI.md" in names, "startup ZIP missing 00_START_HERE_FOR_AI.md.")
            require("STARTUP_PROMPT_REQUEST_KERNEL_MANIFEST.json" in names, "startup ZIP missing manifest.")
        if label == PROMPT_LIBRARY_ZIP:
            require("PROMPT_LIBRARY_ZIP_MANIFEST.json" in names, "prompt_library.zip missing manifest.")
            require(
                "ACTIVE_PROMPTS/02_prompt_routing_and_indexing/prompt_navigation_index.md" in names,
                "prompt_library.zip missing prompt_navigation_index.md.",
            )


def assert_missing_maintenance_passes(generator: Path, workspace: Path, output_dir: Path) -> None:
    maintenance_path = output_dir / MAINTENANCE_FILE
    if maintenance_path.exists():
        temp_path = maintenance_path.with_suffix(maintenance_path.suffix + ".validation_tmp")
        if temp_path.exists():
            temp_path.unlink()
        maintenance_path.rename(temp_path)
        try:
            check_output = run_checked([sys.executable, str(generator), "--check"], cwd=workspace)
        finally:
            temp_path.rename(maintenance_path)
    else:
        check_output = run_checked([sys.executable, str(generator), "--check"], cwd=workspace)
    require("STATUS: IN_SYNC" in check_output, "Missing optional maintenance file did not pass --check.")
    require("STATUS: STALE" not in check_output, "Missing optional maintenance file marked startup stale.")


def main() -> int:
    root = project_root()
    workspace = root / "kanda_prompt_workspace"
    generator = workspace / "prompt_tools" / "sync_startup_routing_kernel_pack.py"
    startup_freeze_context = workspace / "prompt_tools" / "startup_freeze_context.py"

    require(generator.exists(), f"Generator not found: {generator}")
    require(startup_freeze_context.exists(), f"Startup freeze context helper not found: {startup_freeze_context}")
    generator_text = read_text(generator)
    require(NOTICE_FILE in generator_text, "Generator does not define the ZIP read-order notice file.")
    require(MAINTENANCE_FILE in generator_text, "Generator does not use the new maintenance filename.")
    require(OLD_MAINTENANCE_FILE not in generator_text, "Generator still references the old maintenance filename.")
    require("optional" in generator_text.lower(), "Generator does not mark the maintenance file optional.")
    require(
        "normal startup may continue" in generator_text or "If missing, pass" in generator_text,
        "Generator does not allow missing maintenance file to pass.",
    )
    require(
        "required.add(READ_BEFORE_ANY_STARTUP_ARTIFACT_FILENAME)" in generator_text,
        "Generator does not treat old ZIPs missing the read-order notice as stale output.",
    )
    require(
        "except (ValueError, KeyError) as exc:" in generator_text,
        "Generator does not catch KeyError as stale/invalid generated ZIP output.",
    )

    run_checked([sys.executable, "-m", "py_compile", str(generator), str(startup_freeze_context)], cwd=root)
    sync_output = run_checked([sys.executable, str(generator), "--ensure-sync", "--yes"], cwd=workspace)
    require(
        "STATUS: IN_SYNC" in sync_output or "ENSURE SYNC RESULT: IN_SYNC_AFTER_SYNC" in sync_output,
        "Startup sync did not report in-sync status.",
    )
    require("KeyError" not in sync_output, "Startup sync still crashed with KeyError.")
    require("Traceback" not in sync_output, "Startup sync produced a traceback.")

    output_dir = default_first_prompt_output_dir(root)
    require(output_dir.exists(), f"Delivery folder not found: {output_dir}")

    normal_required_files = [STARTUP_ZIP, PROMPT_LIBRARY_ZIP, TELL_FILE]
    for name in normal_required_files:
        require((output_dir / name).exists(), f"Generated normal startup file missing: {name}")
    require(not (output_dir / OLD_MAINTENANCE_FILE).exists(), "Old maintenance file still exists in first_prompt_files.")

    sorted_names = [p.name for p in sorted(output_dir.iterdir()) if p.is_file()]
    require(
        sorted_names[:3] == normal_required_files,
        "Generated normal startup file sort order is not expected: " + str(sorted_names[:3]),
    )

    tell_text = read_text(output_dir / TELL_FILE)
    require(tell_text.startswith("# " + EXPECTED_MARKER), "tell_AI_read_before_all.md does not start with read-order guard.")
    assert_read_order_text(tell_text, TELL_FILE)

    maintenance_path = output_dir / MAINTENANCE_FILE
    if maintenance_path.exists():
        maintenance_text = read_text(maintenance_path)
        require(maintenance_text.startswith("# " + EXPECTED_MARKER), "maintenance file does not start with read-order guard.")
        assert_read_order_text(maintenance_text, MAINTENANCE_FILE)

    assert_missing_maintenance_passes(generator, workspace, output_dir)
    inspect_zip(output_dir / STARTUP_ZIP, STARTUP_ZIP)
    inspect_zip(output_dir / PROMPT_LIBRARY_ZIP, PROMPT_LIBRARY_ZIP)

    print("VALIDATION OK: startup-artifact-read-order-guard-v3")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
