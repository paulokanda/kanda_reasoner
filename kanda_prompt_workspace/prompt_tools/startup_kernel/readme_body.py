"""README body generation for the startup upload ZIP."""

from __future__ import annotations

from typing import Any

from startup_kernel.constants import (
    MANIFEST_FILENAME,
    PROJECT_READY_CHECK_TITLE,
    PROJECT_IN_USE_TEMPLATE,
    PROMPT_LIBRARY_ZIP_NAME,
    SECOND_UPLOAD_READY_ACTION,
)


__all__ = [
    "build_readme_content",
]


def build_readme_content(
    date_cert: str,
    generated_at: str,
    zip_name: str,
    file_records: list[dict[str, Any]],
    paste_after_uploading_name: str,
) -> str:
    """Build README content for the generated startup upload pack."""
    rows = "\n".join(
        f"- `{rec['generated_filename']}` - {rec.get('role', '')}" for rec in file_records
    )
    return f"""# Startup Prompt Request Kernel Upload Pack

Certificate: `{date_cert}`
Generated: `{generated_at}`
ZIP: `{zip_name}`

## Purpose

This ZIP is a generated human-upload convenience pack for the KANDA prompt system.
It contains separated Markdown startup files that help an AI route tasks and request the correct prompt files at the correct time.

## Canonical source rule

The files inside this ZIP are generated copies.
Do not edit them as canonical source.
Edit the original files under `prompt_library/`, then regenerate or verify this ZIP with:

```powershell
python .\\prompt_tools\\sync_startup_routing_kernel_pack.py --ensure-sync --yes
```

Use `--sync --yes` when you intentionally want to force regeneration even if the pack is already in sync.

## Upload workflow

1. Open `{paste_after_uploading_name}` in `first_prompt_files/` and paste/read its boot command first.
2. Upload this ZIP to ChatGPT.
3. Upload `{PROMPT_LIBRARY_ZIP_NAME}` to the same ChatGPT session.
4. The AI reads `{paste_after_uploading_name}` before opening ZIP contents, then opens this startup ZIP.
5. Wait for `STARTUP PACK LOAD CHECK`.
6. After the first load check completes, upload the project handoff files from `second_prompt_files`.
7. Wait for `{PROJECT_READY_CHECK_TITLE}` to end with `Next action:`, `{PROJECT_IN_USE_TEMPLATE}`, and `{SECOND_UPLOAD_READY_ACTION}` in that order.
8. Only then provide the project task.

## Companion prompt library ZIP

`{PROMPT_LIBRARY_ZIP_NAME}` and `{paste_after_uploading_name}` are generated next to this startup ZIP. Together with this ZIP they form the three-file startup delivery. `{paste_after_uploading_name}` must be read before ZIP contents. The prompt library ZIP contains the canonical prompt library for on-demand lookup. The AI should not read all prompts at startup and should not open prompt_library.zip until a specific prompt is needed and not already present in the startup ZIP.

## Files

{rows}

## Integrity

See `{MANIFEST_FILENAME}` for source paths, hashes, generated filenames, and ZIP certificate data.
"""
