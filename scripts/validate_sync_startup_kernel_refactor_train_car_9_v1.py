"""Validate Sync Startup Routing Kernel Refactor Train Car 9 v1."""

from __future__ import annotations

import importlib
import json
import sys
import tempfile
import zipfile
from pathlib import Path

__all__: list[str] = []


FEATURE_ID = "sync-startup-kernel-refactor-train-car-9-v1"
PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROMPT_TOOLS = PROJECT_ROOT / "kanda_prompt_workspace" / "prompt_tools"
STARTUP_KERNEL = PROMPT_TOOLS / "startup_kernel"
WORKSPACE_ROOT = PROJECT_ROOT / "kanda_prompt_workspace"


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


def validate_files_exist() -> None:
    required = [
        STARTUP_KERNEL / "prompt_library_zip.py",
        STARTUP_KERNEL / "prompt_library_payload.py",
        STARTUP_KERNEL / "prompt_library_manifest.py",
        PROMPT_TOOLS / "sync_startup_routing_kernel_pack.py",
    ]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        fail("missing required files: " + ", ".join(missing))


def validate_line_counts() -> None:
    for path in STARTUP_KERNEL.glob("*.py"):
        if line_count(path) > 500:
            fail(f"startup_kernel helper exceeds 500 lines: {path.name}")
    for filename in ("prompt_library_zip.py", "prompt_library_payload.py", "prompt_library_manifest.py"):
        if line_count(STARTUP_KERNEL / filename) > 400:
            fail(filename + " should remain under the 400-line ideal")


def validate_source_ownership() -> None:
    prompt_zip = read(STARTUP_KERNEL / "prompt_library_zip.py")
    payload = read(STARTUP_KERNEL / "prompt_library_payload.py")
    manifest = read(STARTUP_KERNEL / "prompt_library_manifest.py")

    for fragment in [
        "from startup_kernel.prompt_library_payload import",
        "from startup_kernel.prompt_library_manifest import",
        "def make_prompt_library_zip(",
        "def validate_prompt_library_zip_contract(",
    ]:
        if fragment not in prompt_zip:
            fail("prompt_library_zip.py missing fragment: " + fragment)

    for fragment in [
        "def _is_prompt_library_payload_file(",
        "def iter_prompt_library_payload_files(",
        "def _prompt_library_relpath(",
        "def prompt_library_source_fingerprint(",
    ]:
        if fragment not in payload:
            fail("prompt_library_payload.py missing fragment: " + fragment)

    for fragment in [
        "def _load_prompt_metadata_entries(",
        "def build_prompt_library_manifest(",
        "prompt_entries",
        "source_fingerprint",
    ]:
        if fragment not in manifest:
            fail("prompt_library_manifest.py missing fragment: " + fragment)

    forbidden_in_zip = [
        "def _is_prompt_library_payload_file(",
        "def iter_prompt_library_payload_files(",
        "def prompt_library_source_fingerprint(",
        "def _load_prompt_metadata_entries(",
    ]
    for fragment in forbidden_in_zip:
        if fragment in prompt_zip:
            fail("prompt_library_zip.py must re-export without owning body: " + fragment)


def validate_public_imports() -> None:
    ensure_import_path()
    prompt_zip = importlib.import_module("startup_kernel.prompt_library_zip")
    payload = importlib.import_module("startup_kernel.prompt_library_payload")
    manifest = importlib.import_module("startup_kernel.prompt_library_manifest")
    entry = importlib.import_module("sync_startup_routing_kernel_pack")

    expected = [
        "_is_prompt_library_payload_file",
        "_prompt_library_relpath",
        "iter_prompt_library_payload_files",
        "prompt_library_source_fingerprint",
        "_load_prompt_metadata_entries",
        "make_prompt_library_zip",
        "validate_prompt_library_zip_contract",
    ]
    for name in expected:
        if not hasattr(prompt_zip, name):
            fail("startup_kernel.prompt_library_zip missing compatibility export: " + name)

    for name in [
        "iter_prompt_library_payload_files",
        "make_prompt_library_zip",
        "prompt_library_source_fingerprint",
        "validate_prompt_library_zip_contract",
    ]:
        if not hasattr(entry, name):
            fail("sync_startup_routing_kernel_pack missing public helper: " + name)

    if prompt_zip.iter_prompt_library_payload_files is not payload.iter_prompt_library_payload_files:
        fail("prompt_library_zip must re-export iter_prompt_library_payload_files from prompt_library_payload")
    if prompt_zip.prompt_library_source_fingerprint is not payload.prompt_library_source_fingerprint:
        fail("prompt_library_zip must re-export prompt_library_source_fingerprint from prompt_library_payload")
    if prompt_zip._load_prompt_metadata_entries is not manifest._load_prompt_metadata_entries:
        fail("prompt_library_zip must re-export _load_prompt_metadata_entries from prompt_library_manifest")


def validate_prompt_library_zip_behavior() -> None:
    ensure_import_path()
    prompt_zip = importlib.import_module("startup_kernel.prompt_library_zip")
    payload = importlib.import_module("startup_kernel.prompt_library_payload")
    manifest_mod = importlib.import_module("startup_kernel.prompt_library_manifest")

    files = payload.iter_prompt_library_payload_files(WORKSPACE_ROOT)
    if not files:
        fail("iter_prompt_library_payload_files returned no files")
    if any(path.suffix.lower() in {".zip", ".pyc", ".pyo", ".tmp", ".bak"} for path in files):
        fail("prompt library payload included forbidden generated/temp file")

    fingerprint = payload.prompt_library_source_fingerprint(WORKSPACE_ROOT)
    if not fingerprint or len(fingerprint) != 64:
        fail("prompt_library_source_fingerprint did not return a sha256 hex string")

    manifest = manifest_mod.build_prompt_library_manifest(WORKSPACE_ROOT, "2026-06-29T00:00:00Z", "20260629_000000Z")
    if manifest.get("kind") != "prompt_library_zip_manifest":
        fail("build_prompt_library_manifest returned wrong kind")
    if manifest.get("source_fingerprint") != fingerprint:
        fail("build_prompt_library_manifest returned stale source fingerprint")
    if manifest.get("file_count") != len(manifest.get("files", [])):
        fail("build_prompt_library_manifest file_count mismatch")
    if not isinstance(manifest.get("prompt_entries"), list):
        fail("build_prompt_library_manifest prompt_entries must be a list")

    with tempfile.TemporaryDirectory() as tmp:
        output_dir = Path(tmp)
        zip_path = prompt_zip.make_prompt_library_zip(WORKSPACE_ROOT, output_dir, "2026-06-29T00:00:00Z", "20260629_000000Z")
        prompt_zip.validate_prompt_library_zip_contract(zip_path, WORKSPACE_ROOT)
        with zipfile.ZipFile(zip_path, "r") as z:
            names = set(z.namelist())
            if any(name.startswith("prompt_library/") for name in names):
                fail("prompt_library.zip used forbidden prompt_library/ prefix")
            manifest_from_zip = json.loads(z.read("PROMPT_LIBRARY_ZIP_MANIFEST.json").decode("utf-8-sig"))
            if manifest_from_zip.get("source_fingerprint") != fingerprint:
                fail("prompt_library.zip manifest source_fingerprint mismatch")


def validate_no_forbidden_touch() -> None:
    sync_text = read(PROMPT_TOOLS / "sync_startup_routing_kernel_pack.py")
    if "from startup_kernel.prompt_library_zip import" not in sync_text:
        fail("thin entrypoint must continue importing prompt library helpers through prompt_library_zip")
    if "from startup_kernel.prompt_library_payload" in sync_text:
        fail("thin entrypoint should not bypass prompt_library_zip compatibility surface")
    if "from startup_kernel.prompt_library_manifest" in sync_text:
        fail("thin entrypoint should not bypass prompt_library_zip compatibility surface")


def main() -> int:
    validate_files_exist()
    validate_line_counts()
    validate_source_ownership()
    validate_public_imports()
    validate_prompt_library_zip_behavior()
    validate_no_forbidden_touch()
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
