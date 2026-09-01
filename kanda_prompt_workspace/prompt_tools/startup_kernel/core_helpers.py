"""Core startup delivery path and status helpers.

This module remains the public compatibility surface for helpers that were
historically exported by sync_startup_routing_kernel_pack.py.  Pure generic
helpers and source-map resolution now live in focused modules, but are
re-exported here so existing imports keep working.
"""

from __future__ import annotations

import ctypes
import os
import shutil
import uuid
from pathlib import Path
from typing import Any

from startup_kernel.constants import (
    DEFAULT_ZIP_NAME,
    FIRST_PROMPT_FILES_DIR_NAME,
    LEGACY_MODIFY_STARTUP_DELIVERY_FILENAME,
    LEGACY_PASTE_AFTER_FIRST_PROMPTS_FILENAME,
    MODIFY_STARTUP_DELIVERY_FILENAME,
    OLD_PASTE_AFTER_UPLOAD_FILENAME,
    PASTE_AFTER_UPLOAD_FILENAME,
    PROMPT_LIBRARY_ZIP_NAME,
    STARTUP_ARTIFACT_READ_ORDER_MARKER,
    SourceEntry,
)
from startup_kernel.generic_helpers import (
    _safe_slug_for_delivery,
    date_certificate,
    generated_header,
    now_utc,
    read_text_utf8,
    sha256_bytes,
    sha256_file,
)
from startup_kernel.source_resolution import load_source_map, resolve_source

__all__ = [
    "clean_delivery_folder",
    "collect_status",
    "date_certificate",
    "default_first_prompt_output_dir",
    "detect_workspace_root",
    "generated_header",
    "fault_checkpoint",
    "load_source_map",
    "make_stage_dir",
    "now_utc",
    "read_text_utf8",
    "publish_complete_delivery",
    "remove_completed_backup",
    "resolve_source",
    "sha256_bytes",
    "sha256_file",
    "validate_complete_delivery",
]


def detect_workspace_root(script_path: Path, explicit_workspace: Path | None) -> Path:
    """Return the prompt workspace root containing prompt_library/.

    The startup generator can be launched through the thin public entrypoint in
    prompt_tools or through helper modules inside prompt_tools/startup_kernel.
    After the train-car refactor, looking only one or two parents above
    __file__ is not enough. Walk upward from both the script path and current
    working directory so the helper package does not mistake startup_kernel for
    the workspace root.
    """
    if explicit_workspace is not None:
        return explicit_workspace.expanduser().resolve(strict=False)

    candidates: list[Path] = []
    anchors = [script_path.expanduser().resolve(strict=False), Path.cwd().resolve(strict=False)]
    for anchor in anchors:
        start = anchor if anchor.is_dir() else anchor.parent
        for candidate in (start, *start.parents):
            if candidate not in candidates:
                candidates.append(candidate)

    for candidate in candidates:
        if (candidate / "prompt_library").exists():
            return candidate.resolve(strict=False)
    return script_path.parent.resolve(strict=False)


def default_first_prompt_output_dir(active_project_root: Path) -> Path:
    """Return <project_drive>/<project>_show_project_to_AI/first_prompt_files."""
    root = Path(active_project_root).expanduser().resolve(strict=False)
    anchor = root.anchor or str(root.parent)
    slug = _safe_slug_for_delivery(root)
    if anchor.endswith(":\\") or anchor.endswith(":/"):
        base = Path(anchor) / f"{slug}_show_project_to_AI"
    elif anchor.endswith(":"):
        base = Path(f"{anchor}\\{slug}_show_project_to_AI")
    else:
        base = Path(anchor) / f"{slug}_show_project_to_AI"
    return base / FIRST_PROMPT_FILES_DIR_NAME


def collect_status(workspace_root: Path, entries: list[SourceEntry]) -> tuple[list[dict[str, Any]], list[str]]:
    records: list[dict[str, Any]] = []
    failures: list[str] = []
    for entry in entries:
        source_path, resolution = resolve_source(workspace_root, entry)
        record: dict[str, Any] = {
            "load_order": entry.load_order,
            "prompt_id": entry.prompt_id,
            "load_mode": entry.load_mode,
            "role": entry.role,
            "canonical_source": entry.canonical_source,
            "generated_filename": entry.generated_filename,
            "resolution": resolution,
            "exists": source_path is not None,
        }
        if source_path is None:
            failures.append(f"{entry.generated_filename}: {resolution} ({entry.canonical_source})")
        else:
            try:
                resolved_source = str(source_path.relative_to(workspace_root)).replace("\\", "/")
            except ValueError:
                resolved_source = str(source_path)
            record["resolved_source"] = resolved_source
            record["canonical_sha256_current"] = sha256_file(source_path)
            record["size_bytes"] = source_path.stat().st_size
        records.append(record)
    return records, failures


def clean_delivery_folder(output_dir: Path) -> None:
    """Clear approved first_prompt_files or remove legacy generated files only."""
    if not output_dir.exists():
        return
    resolved_dir = output_dir.expanduser().resolve(strict=False)
    if (
        resolved_dir.name == FIRST_PROMPT_FILES_DIR_NAME
        and resolved_dir.parent.name.endswith("_show_project_to_AI")
    ):
        for child in list(resolved_dir.iterdir()):
            if child.is_dir():
                shutil.rmtree(child)
            else:
                child.unlink()
        return
    patterns = [
        "first_prompts_to_ai*.zip",
        "prompt_library*.zip",
        "startup_prompt_request_kernel_upload_pack*.zip",
        "send" + "_this_first__CERT_" + "*.md",  # obsolete pre-rename boot command files
        "send_ai" + "_just_if_modify" + "_startup_delivery.md",  # obsolete pre-rename maintenance file
        PASTE_AFTER_UPLOAD_FILENAME,
    PROMPT_LIBRARY_ZIP_NAME,
    STARTUP_ARTIFACT_READ_ORDER_MARKER,
        OLD_PASTE_AFTER_UPLOAD_FILENAME,
        LEGACY_PASTE_AFTER_FIRST_PROMPTS_FILENAME,
        LEGACY_MODIFY_STARTUP_DELIVERY_FILENAME,
        MODIFY_STARTUP_DELIVERY_FILENAME,
    ]
    for pattern in patterns:
        for path in output_dir.glob(pattern):
            if path.is_file():
                path.unlink()

_FAULT_ENV = "KANDA_STARTUP_TX_TEST_HARD_EXIT"
_MOVEFILE_WRITE_THROUGH = 0x00000008
_RENAME_EXCHANGE = 0x00000002
_AT_FDCWD = -100


def fault_checkpoint(name: str) -> None:
    """Terminate only when the focused C2 fault test requests it."""
    if os.environ.get(_FAULT_ENV) == name:
        os._exit(82)


def _expected_delivery_names() -> set[str]:
    return {
        DEFAULT_ZIP_NAME,
        PROMPT_LIBRARY_ZIP_NAME,
        PASTE_AFTER_UPLOAD_FILENAME,
        MODIFY_STARTUP_DELIVERY_FILENAME,
    }


def validate_complete_delivery(
    delivery_dir: Path,
    workspace_root: Path,
    source_files: list[str],
    *,
    flush: bool = False,
) -> dict[str, str]:
    """Validate a complete startup projection and return exact hashes."""
    from startup_kernel.prompt_library_zip import (
        validate_prompt_library_zip_contract,
    )
    from startup_kernel.zip_contract import validate_generated_zip_contract

    expected = _expected_delivery_names()
    if not delivery_dir.is_dir():
        raise ValueError("Startup delivery is missing: " + str(delivery_dir))
    actual = {path.name for path in delivery_dir.iterdir()}
    if actual != expected:
        raise ValueError(
            "Startup delivery member set mismatch. Expected "
            + str(sorted(expected))
            + "; found "
            + str(sorted(actual))
        )
    validate_generated_zip_contract(
        delivery_dir / DEFAULT_ZIP_NAME,
        source_files,
    )
    validate_prompt_library_zip_contract(
        delivery_dir / PROMPT_LIBRARY_ZIP_NAME,
        workspace_root,
    )
    for filename in (
        PASTE_AFTER_UPLOAD_FILENAME,
        MODIFY_STARTUP_DELIVERY_FILENAME,
    ):
        text = (delivery_dir / filename).read_text(encoding="utf-8-sig")
        if STARTUP_ARTIFACT_READ_ORDER_MARKER not in text:
            raise ValueError(filename + " is missing the read-order marker.")
    if flush:
        for name in sorted(expected):
            with (delivery_dir / name).open("r+b") as handle:
                handle.flush()
                os.fsync(handle.fileno())
        if os.name != "nt":
            descriptor = os.open(delivery_dir, os.O_RDONLY)
            try:
                os.fsync(descriptor)
            finally:
                os.close(descriptor)
    return {
        name: sha256_file(delivery_dir / name)
        for name in sorted(expected)
    }


def _transaction_path(output_dir: Path, kind: str) -> Path:
    token = uuid.uuid4().hex
    return output_dir.parent / f".{output_dir.name}.c2-{kind}-{token}"


def make_stage_dir(output_dir: Path) -> Path:
    """Create an off-side complete-replacement staging directory."""
    output_dir.parent.mkdir(parents=True, exist_ok=True)
    stage_dir = _transaction_path(output_dir, "stage")
    stage_dir.mkdir(parents=False, exist_ok=False)
    return stage_dir


def _windows_filesystem_name(path: Path) -> str:
    if str(path).startswith("\\\\"):
        raise ValueError("Startup transaction requires a local NTFS volume.")
    root = path.resolve(strict=False).anchor
    if not root:
        raise ValueError("Could not resolve startup delivery volume root.")
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    function = kernel32.GetVolumeInformationW
    function.argtypes = [
        ctypes.c_wchar_p,
        ctypes.c_wchar_p,
        ctypes.c_uint32,
        ctypes.c_void_p,
        ctypes.c_void_p,
        ctypes.c_void_p,
        ctypes.c_wchar_p,
        ctypes.c_uint32,
    ]
    function.restype = ctypes.c_int
    filesystem = ctypes.create_unicode_buffer(64)
    if not function(root, None, 0, None, None, None, filesystem, 64):
        raise OSError(ctypes.get_last_error(), "GetVolumeInformationW failed.")
    return filesystem.value.upper()


def _windows_transactional_swap(
    stage_dir: Path,
    output_dir: Path,
) -> Path:
    if _windows_filesystem_name(output_dir.parent) != "NTFS":
        raise ValueError("Startup transaction requires a local NTFS volume.")
    backup_dir = _transaction_path(output_dir, "backup")
    ktm = ctypes.WinDLL("KtmW32", use_last_error=True)
    kernel32 = ctypes.WinDLL("Kernel32", use_last_error=True)
    create = ktm.CreateTransaction
    create.argtypes = [
        ctypes.c_void_p, ctypes.c_void_p, ctypes.c_uint32,
        ctypes.c_uint32, ctypes.c_uint32, ctypes.c_uint32,
        ctypes.c_wchar_p,
    ]
    create.restype = ctypes.c_void_p
    commit = ktm.CommitTransaction
    commit.argtypes = [ctypes.c_void_p]
    commit.restype = ctypes.c_int
    rollback = ktm.RollbackTransaction
    rollback.argtypes = [ctypes.c_void_p]
    rollback.restype = ctypes.c_int
    move = kernel32.MoveFileTransactedW
    move.argtypes = [
        ctypes.c_wchar_p,
        ctypes.c_wchar_p,
        ctypes.c_void_p,
        ctypes.c_void_p,
        ctypes.c_uint32,
        ctypes.c_void_p,
    ]
    move.restype = ctypes.c_int
    close = kernel32.CloseHandle
    close.argtypes = [ctypes.c_void_p]
    close.restype = ctypes.c_int
    transaction = create(
        None, None, 0, 0, 0, 0,
        "KANDA startup delivery transactional cutover",
    )
    invalid = ctypes.c_void_p(-1).value
    if transaction in (None, 0, invalid):
        raise OSError(ctypes.get_last_error(), "CreateTransaction failed.")
    committed = False
    try:
        for source, destination, checkpoint in (
            (output_dir, backup_dir, "after_old_move_enlisted"),
            (stage_dir, output_dir, "after_new_move_enlisted"),
        ):
            if not move(
                str(source), str(destination), None, None,
                _MOVEFILE_WRITE_THROUGH, transaction,
            ):
                raise OSError(
                    ctypes.get_last_error(),
                    "MoveFileTransactedW failed: " + str(source),
                )
            fault_checkpoint(checkpoint)
        fault_checkpoint("before_commit")
        if not commit(transaction):
            raise OSError(ctypes.get_last_error(), "CommitTransaction failed.")
        committed = True
        fault_checkpoint("after_commit")
        return backup_dir
    finally:
        if not committed:
            rollback(transaction)
        close(transaction)


def _posix_exchange(stage_dir: Path, output_dir: Path) -> Path:
    libc = ctypes.CDLL(None, use_errno=True)
    renameat2 = getattr(libc, "renameat2", None)
    if renameat2 is None:
        raise ValueError("Atomic directory exchange is unavailable.")
    renameat2.argtypes = [
        ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p,
        ctypes.c_uint,
    ]
    renameat2.restype = ctypes.c_int
    fault_checkpoint("before_commit")
    if renameat2(
        _AT_FDCWD, os.fsencode(stage_dir),
        _AT_FDCWD, os.fsencode(output_dir),
        _RENAME_EXCHANGE,
    ) != 0:
        code = ctypes.get_errno()
        raise OSError(code, os.strerror(code))
    fault_checkpoint("after_commit")
    return stage_dir


def publish_complete_delivery(
    stage_dir: Path,
    output_dir: Path,
) -> Path | None:
    """Expose complete-new atomically or preserve complete-old."""
    if not output_dir.exists():
        fault_checkpoint("before_commit")
        os.replace(stage_dir, output_dir)
        fault_checkpoint("after_commit")
        return None
    if os.name == "nt":
        return _windows_transactional_swap(stage_dir, output_dir)
    if os.name == "posix":
        return _posix_exchange(stage_dir, output_dir)
    raise ValueError("Transactional startup publication is unsupported.")


def remove_completed_backup(path: Path | None) -> None:
    """Delete old non-authoritative delivery only after live validation."""
    if path is not None and path.exists():
        shutil.rmtree(path)

