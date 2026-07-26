"""Validate Sync Startup Routing Kernel Refactor Train Car 8 v1."""

from __future__ import annotations

import importlib
import inspect
import sys
from pathlib import Path

__all__: list[str] = []


FEATURE_ID = "sync-startup-kernel-refactor-train-car-8-v1"
PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROMPT_TOOLS = PROJECT_ROOT / "kanda_prompt_workspace" / "prompt_tools"
STARTUP_KERNEL = PROMPT_TOOLS / "startup_kernel"


def fail(message: str) -> None:
    raise AssertionError(message)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def line_count(path: Path) -> int:
    return len(read(path).splitlines())


def ensure_import_path() -> None:
    prompt_tools_text = str(PROMPT_TOOLS)
    project_root_text = str(PROJECT_ROOT)
    for item in (project_root_text, prompt_tools_text):
        if item not in sys.path:
            sys.path.insert(0, item)


def validate_files_exist() -> None:
    required = [
        STARTUP_KERNEL / "core_helpers.py",
        STARTUP_KERNEL / "generic_helpers.py",
        STARTUP_KERNEL / "source_resolution.py",
        PROMPT_TOOLS / "sync_startup_routing_kernel_pack.py",
    ]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        fail("missing required files: " + ", ".join(missing))


def validate_line_counts() -> None:
    for path in STARTUP_KERNEL.glob("*.py"):
        if line_count(path) > 500:
            fail(f"startup_kernel helper exceeds 500 lines: {path.name}")
    if line_count(STARTUP_KERNEL / "core_helpers.py") > 400:
        fail("core_helpers.py should remain under the 400-line ideal after train car 8")
    if line_count(STARTUP_KERNEL / "generic_helpers.py") > 400:
        fail("generic_helpers.py should remain under the 400-line ideal")
    if line_count(STARTUP_KERNEL / "source_resolution.py") > 400:
        fail("source_resolution.py should remain under the 400-line ideal")


def validate_source_ownership() -> None:
    core = read(STARTUP_KERNEL / "core_helpers.py")
    generic = read(STARTUP_KERNEL / "generic_helpers.py")
    source_resolution = read(STARTUP_KERNEL / "source_resolution.py")

    for fragment in [
        "from startup_kernel.generic_helpers import",
        "from startup_kernel.source_resolution import load_source_map, resolve_source",
        "def detect_workspace_root(",
        "def clean_delivery_folder(",
        "shutil.rmtree(child)",
        "child.unlink()",
    ]:
        if fragment not in core:
            fail("core_helpers.py missing fragment: " + fragment)

    for fragment in [
        "def now_utc(",
        "def date_certificate(",
        "def sha256_file(",
        "def sha256_bytes(",
        "def read_text_utf8(",
        "def generated_header(",
        "def _safe_slug_for_delivery(",
    ]:
        if fragment not in generic:
            fail("generic_helpers.py missing fragment: " + fragment)

    for fragment in [
        "def load_source_map(",
        "def resolve_source(",
        "DEFAULT_SOURCE_MAP",
        "SOURCE_MAP_FILENAME",
    ]:
        if fragment not in source_resolution:
            fail("source_resolution.py missing fragment: " + fragment)

    if "def load_source_map(" in core or "def resolve_source(" in core:
        fail("core_helpers.py must re-export source resolution helpers without owning their bodies")
    if "import hashlib" in core or "from datetime import" in core:
        fail("core_helpers.py must not regain generic hashing/time ownership")


def validate_public_imports() -> None:
    ensure_import_path()
    core = importlib.import_module("startup_kernel.core_helpers")
    generic = importlib.import_module("startup_kernel.generic_helpers")
    source_resolution = importlib.import_module("startup_kernel.source_resolution")
    entry = importlib.import_module("sync_startup_routing_kernel_pack")

    expected = [
        "now_utc",
        "date_certificate",
        "sha256_file",
        "sha256_bytes",
        "read_text_utf8",
        "load_source_map",
        "detect_workspace_root",
        "resolve_source",
        "generated_header",
        "default_first_prompt_output_dir",
        "collect_status",
        "clean_delivery_folder",
    ]
    for name in expected:
        if not hasattr(core, name):
            fail("startup_kernel.core_helpers missing public helper: " + name)
        if not hasattr(entry, name):
            fail("sync_startup_routing_kernel_pack missing public helper: " + name)

    if core.now_utc is not generic.now_utc:
        fail("core_helpers.now_utc must re-export generic_helpers.now_utc")
    if core.sha256_file is not generic.sha256_file:
        fail("core_helpers.sha256_file must re-export generic_helpers.sha256_file")
    if core.load_source_map is not source_resolution.load_source_map:
        fail("core_helpers.load_source_map must re-export source_resolution.load_source_map")
    if core.resolve_source is not source_resolution.resolve_source:
        fail("core_helpers.resolve_source must re-export source_resolution.resolve_source")

    workspace = PROJECT_ROOT / "kanda_prompt_workspace"
    detected = core.detect_workspace_root(STARTUP_KERNEL / "core_helpers.py", None)
    if detected != workspace.resolve(strict=False):
        fail("detect_workspace_root did not find kanda_prompt_workspace from startup_kernel path")

    args = entry.parse_args([])
    if not getattr(args, "check", False):
        fail("parse_args([]) must keep safe read-only --check default")

    entries = core.load_source_map(workspace)
    if not entries:
        fail("load_source_map returned no entries")
    records, failures = core.collect_status(workspace, entries)
    if not records:
        fail("collect_status returned no records")
    if failures:
        first = failures[0]
        fail("collect_status found missing source in validation project: " + first)


def validate_no_forbidden_touch() -> None:
    sync_text = read(PROMPT_TOOLS / "sync_startup_routing_kernel_pack.py")
    if "from startup_kernel.core_helpers import" not in sync_text:
        fail("thin entrypoint must continue importing public helpers through core_helpers")
    if "from startup_kernel.generic_helpers" in sync_text:
        fail("thin entrypoint should not bypass core_helpers compatibility surface")
    if "from startup_kernel.source_resolution" in sync_text:
        fail("thin entrypoint should not bypass core_helpers compatibility surface")


def main() -> int:
    validate_files_exist()
    validate_line_counts()
    validate_source_ownership()
    validate_public_imports()
    validate_no_forbidden_touch()
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
