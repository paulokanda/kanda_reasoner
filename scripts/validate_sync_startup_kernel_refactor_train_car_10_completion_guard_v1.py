"""Validate Sync Startup Routing Kernel refactor completion guard v1.

This guard is intentionally not another source split.  It freezes the final
post-train-car startup_kernel shape after the formerly large
sync_startup_routing_kernel_pack.py module was reduced to a thin entrypoint and
its helpers were separated into cohesive modules.
"""

from __future__ import annotations

import importlib
import sys
from pathlib import Path

__all__: list[str] = []


FEATURE_ID = "sync-startup-kernel-refactor-train-car-10-completion-guard-v1"
PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROMPT_TOOLS = PROJECT_ROOT / "kanda_prompt_workspace" / "prompt_tools"
STARTUP_KERNEL = PROMPT_TOOLS / "startup_kernel"
WORKSPACE_ROOT = PROJECT_ROOT / "kanda_prompt_workspace"
ENTRYPOINT = PROMPT_TOOLS / "sync_startup_routing_kernel_pack.py"

MAX_NORMAL_LINES = 500
IDEAL_LINES = 400
THIN_ENTRYPOINT_MAX_LINES = 200

EXPECTED_MODULES = {
    "boot_text.py",
    "cli.py",
    "cli_check.py",
    "cli_sync.py",
    "constants.py",
    "core_helpers.py",
    "generic_helpers.py",
    "maintenance_body.py",
    "maintenance_text.py",
    "paste_after_uploading_body.py",
    "paste_readme_text.py",
    "prompt_library_manifest.py",
    "prompt_library_payload.py",
    "prompt_library_zip.py",
    "read_order.py",
    "readme_body.py",
    "source_resolution.py",
    "start_here_body_intro.py",
    "start_here_body_routing.py",
    "start_here_lists.py",
    "start_here_text.py",
    "startup_literal_texts.py",
    "startup_names.py",
    "startup_source_map.py",
    "zip_contract.py",
    "zip_delivery.py",
}

ENTRYPOINT_PUBLIC_NAMES = [
    "SourceEntry",
    "add_read_order_block",
    "clean_delivery_folder",
    "collect_status",
    "command_check",
    "command_ensure_sync",
    "confirm_sync",
    "date_certificate",
    "default_first_prompt_output_dir",
    "detect_workspace_root",
    "find_delivery_zip",
    "generated_header",
    "iter_prompt_library_payload_files",
    "load_source_map",
    "make_boot_command_text",
    "make_modify_startup_delivery_protocol",
    "make_paste_after_uploading_file",
    "make_prompt_library_zip",
    "make_readme",
    "make_start_here_file",
    "make_startup_artifact_read_order_notice",
    "make_zip",
    "main",
    "now_utc",
    "parse_args",
    "prompt_library_source_fingerprint",
    "read_manifest_from_zip",
    "read_text_utf8",
    "resolve_source",
    "sha256_bytes",
    "sha256_file",
    "strip_startup_artifact_read_order_block",
    "validate_generated_zip_contract",
    "validate_prompt_library_zip_contract",
]

COMPATIBILITY_SURFACES = {
    "startup_kernel.cli": [
        "command_check",
        "command_ensure_sync",
        "confirm_sync",
        "main",
        "parse_args",
    ],
    "startup_kernel.constants": [
        "DEFAULT_SOURCE_MAP",
        "DEFAULT_ZIP_NAME",
        "PROMPT_LIBRARY_ZIP_NAME",
        "SourceEntry",
    ],
    "startup_kernel.core_helpers": [
        "clean_delivery_folder",
        "collect_status",
        "date_certificate",
        "default_first_prompt_output_dir",
        "detect_workspace_root",
        "generated_header",
        "load_source_map",
        "now_utc",
        "read_text_utf8",
        "resolve_source",
        "sha256_bytes",
        "sha256_file",
    ],
    "startup_kernel.maintenance_text": ["make_modify_startup_delivery_protocol"],
    "startup_kernel.paste_readme_text": ["make_paste_after_uploading_file", "make_readme"],
    "startup_kernel.prompt_library_zip": [
        "_is_prompt_library_payload_file",
        "_load_prompt_metadata_entries",
        "_prompt_library_relpath",
        "iter_prompt_library_payload_files",
        "make_prompt_library_zip",
        "prompt_library_source_fingerprint",
        "validate_prompt_library_zip_contract",
    ],
    "startup_kernel.start_here_text": ["make_start_here_file"],
    "startup_kernel.zip_delivery": [
        "find_delivery_zip",
        "make_zip",
        "read_manifest_from_zip",
        "validate_generated_zip_contract",
    ],
}

OWNERSHIP_FRAGMENTS = {
    "cli.py": [
        "from startup_kernel.cli_check import command_check",
        "from startup_kernel.cli_sync import command_ensure_sync, confirm_sync",
    ],
    "constants.py": [
        "from startup_kernel.startup_literal_texts import",
        "from startup_kernel.startup_names import",
        "from startup_kernel.startup_source_map import",
    ],
    "core_helpers.py": [
        "from startup_kernel.generic_helpers import",
        "from startup_kernel.source_resolution import load_source_map, resolve_source",
        "def detect_workspace_root(",
        "def clean_delivery_folder(",
    ],
    "maintenance_text.py": ["from startup_kernel.maintenance_body import make_modify_startup_delivery_protocol"],
    "paste_readme_text.py": [
        "from startup_kernel.paste_after_uploading_body import build_paste_after_uploading_content",
        "from startup_kernel.readme_body import build_readme_content",
    ],
    "prompt_library_zip.py": [
        "from startup_kernel.prompt_library_manifest import",
        "from startup_kernel.prompt_library_payload import",
    ],
    "start_here_text.py": [
        "from startup_kernel.start_here_body_intro import",
        "from startup_kernel.start_here_body_routing import",
        "from startup_kernel.start_here_lists import",
    ],
    "zip_delivery.py": ["from startup_kernel.zip_contract import"],
}

FORBIDDEN_ENTRYPOINT_BODIES = [
    "def clean_delivery_folder(",
    "def make_prompt_library_zip(",
    "def validate_generated_zip_contract(",
    "def make_start_here_file(",
    "def make_modify_startup_delivery_protocol(",
]


def fail(message: str) -> None:
    raise AssertionError(message)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def line_count(path: Path) -> int:
    return len(read(path).splitlines())


def ensure_import_path() -> None:
    for item in (str(PROJECT_ROOT), str(PROMPT_TOOLS)):
        if item not in sys.path:
            sys.path.insert(0, item)


def validate_required_files() -> None:
    missing = [name for name in sorted(EXPECTED_MODULES) if not (STARTUP_KERNEL / name).is_file()]
    if missing:
        fail("missing startup_kernel helper modules: " + ", ".join(missing))
    if not ENTRYPOINT.is_file():
        fail("missing thin public entrypoint: " + str(ENTRYPOINT))


def validate_line_counts() -> None:
    entry_lines = line_count(ENTRYPOINT)
    if entry_lines > THIN_ENTRYPOINT_MAX_LINES:
        fail(f"thin entrypoint exceeds {THIN_ENTRYPOINT_MAX_LINES} lines: {entry_lines}")

    violations: list[str] = []
    ideal_warnings: list[str] = []
    for path in sorted(STARTUP_KERNEL.glob("*.py")):
        count = line_count(path)
        if count > MAX_NORMAL_LINES:
            violations.append(f"{path.name}={count}")
        if count > IDEAL_LINES:
            ideal_warnings.append(f"{path.name}={count}")
    if violations:
        fail("startup_kernel helper exceeds 500-line maximum: " + ", ".join(violations))
    if ideal_warnings:
        fail("startup_kernel helper exceeds 400-line ideal after completion guard: " + ", ".join(ideal_warnings))


def validate_thin_entrypoint() -> None:
    text = read(ENTRYPOINT)
    for fragment in [
        "from startup_kernel.boot_text import",
        "from startup_kernel.cli import",
        "from startup_kernel.constants import *",
        "from startup_kernel.core_helpers import",
        "from startup_kernel.maintenance_text import",
        "from startup_kernel.paste_readme_text import",
        "from startup_kernel.prompt_library_zip import",
        "from startup_kernel.read_order import",
        "from startup_kernel.start_here_text import",
        "from startup_kernel.zip_delivery import",
        "raise SystemExit(main(sys.argv[1:]))",
    ]:
        if fragment not in text:
            fail("thin entrypoint missing compatibility import/entry fragment: " + fragment)
    for fragment in FORBIDDEN_ENTRYPOINT_BODIES:
        if fragment in text:
            fail("thin entrypoint must not regain helper body: " + fragment)


def validate_ownership_boundaries() -> None:
    for filename, fragments in OWNERSHIP_FRAGMENTS.items():
        text = read(STARTUP_KERNEL / filename)
        for fragment in fragments:
            if fragment not in text:
                fail(f"{filename} missing ownership fragment: {fragment}")

    if "def make_modify_startup_delivery_protocol_body(" in read(STARTUP_KERNEL / "maintenance_body.py"):
        pass
    else:
        fail("maintenance_body.py must own make_modify_startup_delivery_protocol_body")
    if "def build_paste_after_uploading_content(" not in read(STARTUP_KERNEL / "paste_after_uploading_body.py"):
        fail("paste_after_uploading_body.py must own build_paste_after_uploading_content")
    if "def build_readme_content(" not in read(STARTUP_KERNEL / "readme_body.py"):
        fail("readme_body.py must own build_readme_content")
    if "def validate_generated_zip_contract(" not in read(STARTUP_KERNEL / "zip_contract.py"):
        fail("zip_contract.py must own validate_generated_zip_contract")
    if "def _load_prompt_metadata_entries(" not in read(STARTUP_KERNEL / "prompt_library_manifest.py"):
        fail("prompt_library_manifest.py must own _load_prompt_metadata_entries")
    if "def iter_prompt_library_payload_files(" not in read(STARTUP_KERNEL / "prompt_library_payload.py"):
        fail("prompt_library_payload.py must own iter_prompt_library_payload_files")


def validate_public_imports() -> None:
    ensure_import_path()
    entry = importlib.import_module("sync_startup_routing_kernel_pack")
    for name in ENTRYPOINT_PUBLIC_NAMES:
        if not hasattr(entry, name):
            fail("sync_startup_routing_kernel_pack missing public helper: " + name)

    for module_name, names in COMPATIBILITY_SURFACES.items():
        module = importlib.import_module(module_name)
        for name in names:
            if not hasattr(module, name):
                fail(module_name + " missing compatibility export: " + name)


def validate_path_detection_repair_still_active() -> None:
    ensure_import_path()
    core = importlib.import_module("startup_kernel.core_helpers")
    detected = core.detect_workspace_root(STARTUP_KERNEL / "core_helpers.py", None)
    if detected != WORKSPACE_ROOT.resolve(strict=False):
        fail("detect_workspace_root did not find kanda_prompt_workspace from startup_kernel")


def validate_safe_parse_default() -> None:
    ensure_import_path()
    cli = importlib.import_module("startup_kernel.cli")
    args = cli.parse_args([])
    if not getattr(args, "check", False):
        fail("parse_args([]) must keep safe read-only --check default")


def main() -> int:
    validate_required_files()
    validate_line_counts()
    validate_thin_entrypoint()
    validate_ownership_boundaries()
    validate_public_imports()
    validate_path_detection_repair_still_active()
    validate_safe_parse_default()
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
