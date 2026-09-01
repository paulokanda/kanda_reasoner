"""Generated startup ZIP orchestration and transactional publication."""

from __future__ import annotations

import json
import shutil
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
    MANIFEST_FILENAME,
    MODIFY_STARTUP_DELIVERY_FILENAME,
    PASTE_AFTER_UPLOAD_FILENAME,
    PROMPT_LIBRARY_ZIP_NAME,
    README_FILENAME,
    READ_BEFORE_ANY_STARTUP_ARTIFACT_FILENAME,
    SCRIPT_NAME,
    TOOLS_DIR_NAME,
)
from startup_kernel.core_helpers import (
    collect_status,
    fault_checkpoint,
    date_certificate,
    generated_header,
    load_source_map,
    make_stage_dir,
    now_utc,
    publish_complete_delivery,
    read_text_utf8,
    remove_completed_backup,
    sha256_bytes,
    sha256_file,
    validate_complete_delivery,
)
from startup_kernel.maintenance_text import (
    make_modify_startup_delivery_protocol,
)
from startup_kernel.paste_readme_text import (
    make_paste_after_uploading_file,
    make_readme,
)
from startup_kernel.prompt_library_zip import make_prompt_library_zip
from startup_kernel.read_order import (
    add_read_order_block,
    make_startup_artifact_read_order_notice,
)
from startup_kernel.start_here_text import make_start_here_file


__all__ = [
    "find_delivery_zip",
    "make_zip",
]

def find_delivery_zip(output_dir: Path) -> Path | None:
    zip_path = output_dir / DEFAULT_ZIP_NAME
    return zip_path if zip_path.exists() else None


def make_zip(
    workspace_root: Path,
    output_dir: Path,
    active_project_root: Path,
    dry_run: bool = False,
) -> tuple[int, Path | None]:
    """Build the complete startup projection off-side, then commit it."""
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
    prompt_library_zip_path = output_dir / PROMPT_LIBRARY_ZIP_NAME
    source_files_for_paste = [
        str(record["generated_filename"]) for record in records
    ] + [ACTIVE_FREEZE_CONTEXT_FILENAME]
    paste_name, paste_content = make_paste_after_uploading_file(
        cert,
        generated_at,
        zip_name,
        source_files_for_paste,
    )
    paste_path = output_dir / paste_name
    maintenance_path = output_dir / MODIFY_STARTUP_DELIVERY_FILENAME
    maintenance_content = make_modify_startup_delivery_protocol(
        generated_at,
        zip_name,
    )

    print("STARTUP PROMPT REQUEST KERNEL SYNC")
    print(f"Workspace root: {workspace_root}")
    print(f"Delivery directory: {output_dir}")
    print(f"Active project root for freeze context: {active_project_root}")
    print(f"Output ZIP: {zip_path}")
    print(f"Prompt library ZIP: {prompt_library_zip_path}")
    print(f"Read-before-all file: {paste_path}")
    print(f"Startup delivery maintenance file: {maintenance_path}")
    print("")
    print("Files to include in ZIP:")
    for record in records:
        print(
            f"- {record['generated_filename']} <= "
            f"{record['resolved_source']}"
        )
    print(
        f"- {ACTIVE_FREEZE_CONTEXT_FILENAME} <= "
        "active project frozen memory context"
    )
    if dry_run:
        print("")
        print("DRY RUN COMPLETE: no files were written.")
        return 0, None

    output_dir.parent.mkdir(parents=True, exist_ok=True)
    stage_dir = make_stage_dir(output_dir)
    backup_dir: Path | None = None
    source_files: list[str] = []
    try:
        with tempfile.TemporaryDirectory(
            prefix="kanda_startup_kernel_"
        ) as tmp_name:
            tmp_dir = Path(tmp_name)
            manifest_records: list[dict[str, Any]] = []
            payloads: list[tuple[str, bytes]] = []
            for entry, record in zip(entries, records):
                source_path = workspace_root / record["resolved_source"]
                source_hash = sha256_file(source_path)
                source_text = read_text_utf8(source_path)
                generated_text = (
                    generated_header(
                        entry,
                        source_path,
                        workspace_root,
                        generated_at,
                        source_hash,
                    )
                    + source_text
                )
                generated_bytes = generated_text.encode("utf-8")
                payloads.append((entry.generated_filename, generated_bytes))
                source_files.append(entry.generated_filename)
                manifest_records.append(
                    {
                        "load_order": entry.load_order,
                        "prompt_id": entry.prompt_id,
                        "load_mode": entry.load_mode,
                        "role": entry.role,
                        "canonical_source": entry.canonical_source,
                        "resolved_source": record["resolved_source"],
                        "generated_filename": entry.generated_filename,
                        "canonical_sha256": source_hash,
                        "generated_sha256": sha256_bytes(generated_bytes),
                        "size_bytes_source": source_path.stat().st_size,
                        "size_bytes_generated": len(generated_bytes),
                        "in_sync_at_generation": True,
                    }
                )
            freeze_name, freeze_bytes, freeze_record = (
                build_active_project_freeze_context(
                    workspace_root=workspace_root,
                    active_project_root=active_project_root,
                    generated_at=generated_at,
                )
            )
            payloads.append((freeze_name, freeze_bytes))
            manifest_records.append(freeze_record)
            source_files.append(freeze_name)
            start_name, start_text = make_start_here_file(
                cert,
                generated_at,
                source_files,
            )
            start_bytes = start_text.encode("utf-8")
            payloads.insert(0, (start_name, start_bytes))
            notice = make_startup_artifact_read_order_notice(zip_name).encode(
                "utf-8"
            )
            payloads.insert(
                0,
                (READ_BEFORE_ANY_STARTUP_ARTIFACT_FILENAME, notice),
            )
            readme_bytes = make_readme(
                cert,
                generated_at,
                zip_name,
                manifest_records,
                paste_name,
            ).encode("utf-8")
            payloads.append((README_FILENAME, readme_bytes))
            manifest = {
                "manifest_version": "1.1",
                "pack_type": "startup_prompt_request_kernel",
                "generated_at": generated_at,
                "date_certificate": cert,
                "generated_by": f"{TOOLS_DIR_NAME}/{SCRIPT_NAME}",
                "workspace_root_name": workspace_root.name,
                "delivery_directory": (
                    str(output_dir.relative_to(workspace_root)).replace(
                        "\\", "/"
                    )
                    if output_dir.is_relative_to(workspace_root)
                    else str(output_dir)
                ),
                "zip_filename": zip_name,
                "tell_AI_read_before_all_filename": paste_name,
                "startup_instruction_filename": paste_name,
                "canonical_rule": (
                    "Canonical source files live under prompt_library/. Files "
                    "in this ZIP are generated delivery copies only."
                ),
                "files": manifest_records,
                "boot_file": {
                    "generated_filename": start_name,
                    "sha256": sha256_bytes(start_bytes),
                    "role": (
                        "Stable AI entrypoint and mandatory startup "
                        "load-check instruction."
                    ),
                },
                "readme_file": {
                    "generated_filename": README_FILENAME,
                    "sha256": sha256_bytes(readme_bytes),
                },
                "active_project_freeze_context": freeze_record,
            }
            payloads.append(
                (
                    MANIFEST_FILENAME,
                    json.dumps(
                        manifest,
                        indent=2,
                        ensure_ascii=False,
                    ).encode("utf-8"),
                )
            )
            for name, payload in payloads:
                (tmp_dir / name).write_bytes(payload)
            with zipfile.ZipFile(
                stage_dir / zip_name,
                "w",
                compression=zipfile.ZIP_DEFLATED,
            ) as archive:
                for name, _payload in payloads:
                    archive.write(tmp_dir / name, arcname=name)
        fault_checkpoint("after_primary_staged")

        make_prompt_library_zip(
            workspace_root,
            stage_dir,
            generated_at,
            cert,
        )
        (stage_dir / paste_name).write_text(
            add_read_order_block(
                paste_content,
                PASTE_AFTER_UPLOAD_FILENAME,
            ),
            encoding="utf-8",
            newline="\n",
        )
        (stage_dir / MODIFY_STARTUP_DELIVERY_FILENAME).write_text(
            add_read_order_block(
                maintenance_content,
                MODIFY_STARTUP_DELIVERY_FILENAME,
            ),
            encoding="utf-8",
            newline="\n",
        )
        fault_checkpoint("after_stage_complete")
        staged_hashes = validate_complete_delivery(
            stage_dir,
            workspace_root,
            source_files,
            flush=True,
        )
        fault_checkpoint("after_stage_validation")
        backup_dir = publish_complete_delivery(stage_dir, output_dir)
        live_hashes = validate_complete_delivery(
            output_dir,
            workspace_root,
            source_files,
        )
        if live_hashes != staged_hashes:
            raise ValueError(
                "Published startup delivery differs from validated staged bytes."
            )
        fault_checkpoint("after_live_validation")
        remove_completed_backup(backup_dir)
        backup_dir = None
    finally:
        if stage_dir.exists() and stage_dir != backup_dir:
            shutil.rmtree(stage_dir, ignore_errors=True)

    print("")
    print("SYNC COMPLETE")
    print(f"Best startup ZIP to send: {zip_path}")
    print(f"Prompt library ZIP to send: {prompt_library_zip_path}")
    print(f"Read-before-all file: {paste_path}")
    print(f"Startup delivery maintenance file: {maintenance_path}")
    print(f"Startup ZIP SHA-256: {sha256_file(zip_path)}")
    print(
        "Prompt library ZIP SHA-256: "
        + sha256_file(prompt_library_zip_path)
    )
    print(
        "Use all three normal startup files: tell_AI_read_before_all.md, "
        "first_prompts_to_ai.zip, and prompt_library.zip. Read/paste "
        "tell_AI_read_before_all.md before the AI opens ZIP contents. Open "
        "prompt_library.zip only when a specific prompt is needed and is not "
        "already in first_prompts_to_ai.zip. The "
        "zz_read_only_if_modifying_startup_delivery.md maintenance file is "
        "generated too, but it is optional to read and used only when "
        "modifying startup delivery."
    )
    print(
        f"Use {MODIFY_STARTUP_DELIVERY_FILENAME} only when asking AI to "
        "modify the startup delivery system."
    )
    return 0, zip_path
