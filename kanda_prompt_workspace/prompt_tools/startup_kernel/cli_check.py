# project-path: kanda_prompt_workspace/prompt_tools/startup_kernel/cli_check.py
"""Read-only startup delivery check command."""

from __future__ import annotations

from pathlib import Path

from startup_freeze_context import (
    ACTIVE_FREEZE_CONTEXT_FILENAME,
    freeze_context_source_fingerprint,
)
from startup_kernel.constants import (
    MODIFY_STARTUP_DELIVERY_FILENAME,
    PASTE_AFTER_UPLOAD_FILENAME,
    PROMPT_LIBRARY_ZIP_NAME,
)
from startup_kernel.core_helpers import collect_status, load_source_map
from startup_kernel.prompt_library_zip import validate_prompt_library_zip_contract
from startup_kernel.zip_delivery import (
    find_delivery_zip,
    read_manifest_from_zip,
    validate_generated_zip_contract,
)


def command_check(workspace_root: Path, output_dir: Path, active_project_root: Path) -> int:
    """Support command check behavior.
    
    Parameters
    ----------
    workspace_root : Path
        The workspace root value.
    output_dir : Path
        The output dir value.
    active_project_root : Path
        The active project root value.
    
    Returns
    -------
    int
        The integer result.
    """
    
    entries = load_source_map(workspace_root)
    records, failures = collect_status(workspace_root, entries)

    print("STARTUP PROMPT REQUEST KERNEL CHECK")
    print(f"Workspace root: {workspace_root}")
    print(f"Delivery directory: {output_dir}")
    print(f"Active project root for freeze context: {active_project_root}")
    print("")

    if failures:
        print("STATUS: MISSING_SOURCE")
        for failure in failures:
            print(f"- {failure}")
        return 2

    latest_zip = find_delivery_zip(output_dir)
    if latest_zip is None:
        print("STATUS: MISSING_ZIP")
        print("No generated startup prompt request kernel ZIP was found in first_prompt_files.")
        return 1

    manifest = read_manifest_from_zip(latest_zip)
    if manifest is None:
        print("STATUS: MANIFEST_MISSING_OR_INVALID")
        print(f"ZIP: {latest_zip}")
        return 1

    try:
        expected_generated = [entry.generated_filename for entry in entries] + [ACTIVE_FREEZE_CONTEXT_FILENAME]
        validate_generated_zip_contract(latest_zip, expected_generated)
    except (ValueError, KeyError) as exc:
        print("STATUS: ZIP_CONTRACT_INVALID")
        print(str(exc))
        return 1

    manifest_files = {f.get("generated_filename"): f for f in manifest.get("files", [])}
    stale: list[str] = []
    for record in records:
        generated = record["generated_filename"]
        manifest_record = manifest_files.get(generated)
        if manifest_record is None:
            stale.append(f"{generated}: missing from manifest")
            continue
        old_hash = manifest_record.get("canonical_sha256")
        new_hash = record.get("canonical_sha256_current")
        if old_hash != new_hash:
            stale.append(f"{generated}: source hash changed")

    freeze_context_manifest = manifest.get("active_project_freeze_context")
    if not isinstance(freeze_context_manifest, dict):
        stale.append(f"{ACTIVE_FREEZE_CONTEXT_FILENAME}: missing active_project_freeze_context manifest record")
    else:
        old_project_root = str(freeze_context_manifest.get("active_project_root") or "")
        if old_project_root != str(active_project_root.resolve(strict=False)):
            stale.append(f"{ACTIVE_FREEZE_CONTEXT_FILENAME}: active project root changed")
        old_fingerprint = str(freeze_context_manifest.get("source_fingerprint") or "")
        new_fingerprint = freeze_context_source_fingerprint(active_project_root)
        if old_fingerprint != new_fingerprint:
            stale.append(f"{ACTIVE_FREEZE_CONTEXT_FILENAME}: freeze memory source changed")

    if stale:
        print("STATUS: STALE")
        print(f"ZIP checked: {latest_zip.name}")
        for item in stale:
            print(f"- {item}")
        return 1

    paste_file = output_dir / PASTE_AFTER_UPLOAD_FILENAME
    if not paste_file.exists():
        print("STATUS: STALE")
        print(f"ZIP is in sync, but {PASTE_AFTER_UPLOAD_FILENAME} is missing from first_prompt_files.")
        return 1

    maintenance_file = output_dir / MODIFY_STARTUP_DELIVERY_FILENAME
    if not maintenance_file.exists():
        print(f"OPTIONAL: {MODIFY_STARTUP_DELIVERY_FILENAME} is missing from first_prompt_files; normal startup may continue.")

    prompt_library_zip = output_dir / PROMPT_LIBRARY_ZIP_NAME
    if not prompt_library_zip.exists():
        print("STATUS: STALE")
        print(f"ZIP is in sync, but {PROMPT_LIBRARY_ZIP_NAME} is missing from first_prompt_files.")
        return 1
    try:
        validate_prompt_library_zip_contract(prompt_library_zip, workspace_root)
    except Exception as exc:
        print("STATUS: STALE")
        print(f"{PROMPT_LIBRARY_ZIP_NAME} is missing, invalid, or stale: {exc}")
        return 1

    print("STATUS: IN_SYNC")
    print(f"ZIP checked: {latest_zip.name}")
    print(f"Read-before-all file: {PASTE_AFTER_UPLOAD_FILENAME}")
    print(f"Prompt library ZIP: {PROMPT_LIBRARY_ZIP_NAME}")
    print(f"Startup delivery maintenance file: {MODIFY_STARTUP_DELIVERY_FILENAME}")
    print(f"Manifest generated at: {manifest.get('generated_at', 'UNKNOWN')}")
    return 0
