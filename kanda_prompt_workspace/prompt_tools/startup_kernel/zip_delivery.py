"""Generated startup ZIP orchestration and contract validation."""

from __future__ import annotations

import json
import tempfile
import zipfile
from pathlib import Path
from typing import Any

from startup_freeze_context import (
    ACTIVE_FREEZE_CONTEXT_FILENAME,
    build_active_project_freeze_context,
)
from startup_kernel.constants import (
    DEFAULT_ZIP_NAME,
    FIRST_UPLOAD_PROJECT_FILES_WAIT_ACTION,
    MANIFEST_FILENAME,
    PASTE_AFTER_UPLOAD_FILENAME,
    MODIFY_STARTUP_DELIVERY_FILENAME,
    PROMPT_LIBRARY_ZIP_NAME,
    README_FILENAME,
    READ_BEFORE_ANY_STARTUP_ARTIFACT_FILENAME,
    SCRIPT_NAME,
    STABLE_BOOT_FILENAME,
    STARTUP_ARTIFACT_READ_ORDER_MARKER,
    TOOLS_DIR_NAME,
)
from startup_kernel.core_helpers import (
    clean_delivery_folder,
    collect_status,
    date_certificate,
    generated_header,
    load_source_map,
    now_utc,
    read_text_utf8,
    sha256_bytes,
    sha256_file,
)
from startup_kernel.maintenance_text import make_modify_startup_delivery_protocol
from startup_kernel.paste_readme_text import make_paste_after_uploading_file, make_readme
from startup_kernel.prompt_library_zip import make_prompt_library_zip
from startup_kernel.read_order import add_read_order_block, make_startup_artifact_read_order_notice
from startup_kernel.start_here_text import make_start_here_file

from startup_kernel.zip_contract import (
    read_manifest_from_zip,
    validate_generated_zip_contract,
)


__all__ = [
    "find_delivery_zip",
    "make_zip",
]

def find_delivery_zip(output_dir: Path) -> Path | None:
    zip_path = output_dir / DEFAULT_ZIP_NAME
    return zip_path if zip_path.exists() else None

def make_zip(workspace_root: Path, output_dir: Path, active_project_root: Path, dry_run: bool = False) -> tuple[int, Path | None]:
    generated_dt = now_utc()
    generated_at = generated_dt.isoformat().replace("+00:00", "Z")
    cert = date_certificate(generated_dt)

    entries = load_source_map(workspace_root)
    records, failures = collect_status(workspace_root, entries)
    if failures:
        print("SYNC ABORTED: MISSING_SOURCE")
        for failure in failures:
            print(f"- {failure}")
        return 2, None

    zip_name = DEFAULT_ZIP_NAME
    zip_path = output_dir / zip_name
    source_files_for_paste = [str(record["generated_filename"]) for record in records] + [ACTIVE_FREEZE_CONTEXT_FILENAME]
    paste_name, paste_content = make_paste_after_uploading_file(cert, generated_at, zip_name, source_files_for_paste)
    paste_path = output_dir / paste_name
    maintenance_path = output_dir / MODIFY_STARTUP_DELIVERY_FILENAME
    maintenance_content = make_modify_startup_delivery_protocol(generated_at, zip_name)

    print("STARTUP PROMPT REQUEST KERNEL SYNC")
    print(f"Workspace root: {workspace_root}")
    print(f"Delivery directory: {output_dir}")
    print(f"Active project root for freeze context: {active_project_root}")
    prompt_library_zip_path = output_dir / PROMPT_LIBRARY_ZIP_NAME
    print(f"Output ZIP: {zip_path}")
    print(f"Prompt library ZIP: {prompt_library_zip_path}")
    print(f"Read-before-all file: {paste_path}")
    print(f"Startup delivery maintenance file: {maintenance_path}")
    print("")
    print("Files to include in ZIP:")
    for record in records:
        print(f"- {record['generated_filename']} <= {record['resolved_source']}")
    print(f"- {ACTIVE_FREEZE_CONTEXT_FILENAME} <= active project frozen memory context")

    if dry_run:
        print("")
        print("DRY RUN COMPLETE: no files were written.")
        return 0, None

    output_dir.mkdir(parents=True, exist_ok=True)
    clean_delivery_folder(output_dir)

    with tempfile.TemporaryDirectory(prefix="kanda_startup_kernel_") as tmp_name:
        tmp_dir = Path(tmp_name)
        file_manifest_records: list[dict[str, Any]] = []
        generated_payloads: list[tuple[str, bytes]] = []

        source_files = []
        for entry, record in zip(entries, records):
            source_path = workspace_root / record["resolved_source"]
            source_hash = sha256_file(source_path)
            original_text = read_text_utf8(source_path)
            generated_text = generated_header(entry, source_path, workspace_root, generated_at, source_hash) + original_text
            generated_bytes = generated_text.encode("utf-8")
            generated_hash = sha256_bytes(generated_bytes)
            generated_payloads.append((entry.generated_filename, generated_bytes))
            source_files.append(entry.generated_filename)

            file_manifest_records.append({
                "load_order": entry.load_order,
                "prompt_id": entry.prompt_id,
                "load_mode": entry.load_mode,
                "role": entry.role,
                "canonical_source": entry.canonical_source,
                "resolved_source": record["resolved_source"],
                "generated_filename": entry.generated_filename,
                "canonical_sha256": source_hash,
                "generated_sha256": generated_hash,
                "size_bytes_source": source_path.stat().st_size,
                "size_bytes_generated": len(generated_bytes),
                "in_sync_at_generation": True,
            })

        freeze_context_name, freeze_context_bytes, freeze_context_record = build_active_project_freeze_context(
            workspace_root=workspace_root,
            active_project_root=active_project_root,
            generated_at=generated_at,
        )
        generated_payloads.append((freeze_context_name, freeze_context_bytes))
        file_manifest_records.append(freeze_context_record)
        source_files.append(freeze_context_name)

        start_here_name, start_here_text = make_start_here_file(cert, generated_at, source_files)
        start_here_bytes = start_here_text.encode("utf-8")
        generated_payloads.insert(0, (start_here_name, start_here_bytes))
        read_order_notice_bytes = make_startup_artifact_read_order_notice(zip_name).encode("utf-8")
        generated_payloads.insert(0, (READ_BEFORE_ANY_STARTUP_ARTIFACT_FILENAME, read_order_notice_bytes))

        readme_text = make_readme(cert, generated_at, zip_name, file_manifest_records, paste_name)
        readme_bytes = readme_text.encode("utf-8")
        generated_payloads.append((README_FILENAME, readme_bytes))

        manifest = {
            "manifest_version": "1.1",
            "pack_type": "startup_prompt_request_kernel",
            "generated_at": generated_at,
            "date_certificate": cert,
            "generated_by": f"{TOOLS_DIR_NAME}/{SCRIPT_NAME}",
            "workspace_root_name": workspace_root.name,
            "delivery_directory": str(output_dir.relative_to(workspace_root)).replace("\\", "/") if output_dir.is_relative_to(workspace_root) else str(output_dir),
            "zip_filename": zip_name,
            "tell_AI_read_before_all_filename": paste_name,
            "startup_instruction_filename": paste_name,
            "canonical_rule": "Canonical source files live under prompt_library/. Files in this ZIP are generated delivery copies only.",
            "files": file_manifest_records,
            "boot_file": {
                "generated_filename": start_here_name,
                "sha256": sha256_bytes(start_here_bytes),
                "role": "Stable AI entrypoint and mandatory startup load-check instruction.",
            },
            "readme_file": {
                "generated_filename": README_FILENAME,
                "sha256": sha256_bytes(readme_bytes),
            },
            "active_project_freeze_context": freeze_context_record,
        }
        manifest_bytes = json.dumps(manifest, indent=2, ensure_ascii=False).encode("utf-8")
        generated_payloads.append((MANIFEST_FILENAME, manifest_bytes))

        for name, payload in generated_payloads:
            (tmp_dir / name).write_bytes(payload)

        with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as z:
            for name, _payload in generated_payloads:
                z.write(tmp_dir / name, arcname=name)

    validate_generated_zip_contract(zip_path, source_files)
    prompt_library_zip_path = make_prompt_library_zip(workspace_root, output_dir, generated_at, cert)

    zip_hash = sha256_file(zip_path)
    prompt_library_zip_hash = sha256_file(prompt_library_zip_path)
    paste_path.write_text(add_read_order_block(paste_content, PASTE_AFTER_UPLOAD_FILENAME), encoding="utf-8", newline="\n")
    maintenance_path.write_text(add_read_order_block(maintenance_content, MODIFY_STARTUP_DELIVERY_FILENAME), encoding="utf-8", newline="\n")

    print("")
    print("SYNC COMPLETE")
    print(f"Best startup ZIP to send: {zip_path}")
    print(f"Prompt library ZIP to send: {prompt_library_zip_path}")
    print(f"Read-before-all file: {paste_path}")
    print(f"Startup delivery maintenance file: {maintenance_path}")
    print(f"Startup ZIP SHA-256: {zip_hash}")
    print(f"Prompt library ZIP SHA-256: {prompt_library_zip_hash}")
    print("Use all three normal startup files: tell_AI_read_before_all.md, first_prompts_to_ai.zip, and prompt_library.zip. Read/paste tell_AI_read_before_all.md before the AI opens ZIP contents. Open prompt_library.zip only when a specific prompt is needed and is not already in first_prompts_to_ai.zip. The zz_read_only_if_modifying_startup_delivery.md maintenance file is generated too, but it is optional to read and used only when modifying startup delivery.")
    print(f"Use {MODIFY_STARTUP_DELIVERY_FILENAME} only when asking AI to modify the startup delivery system.")
    return 0, zip_path

