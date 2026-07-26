"""Human-facing startup paste file and README generation."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from startup_kernel.constants import PASTE_AFTER_UPLOAD_FILENAME
from startup_kernel.paste_after_uploading_body import build_paste_after_uploading_content
from startup_kernel.readme_body import build_readme_content


__all__ = [
    "make_paste_after_uploading_file",
    "make_readme",
]


def make_paste_after_uploading_file(
    date_cert: str,
    generated_at: str,
    zip_filename: str,
    expected_filenames: Iterable[str],
) -> tuple[str, str]:
    """Return the read-before-all startup artifact filename and content."""
    filename = PASTE_AFTER_UPLOAD_FILENAME
    content = build_paste_after_uploading_content(
        filename=filename,
        zip_filename=zip_filename,
        expected_filenames=expected_filenames,
    )
    return filename, content


def make_readme(
    date_cert: str,
    generated_at: str,
    zip_name: str,
    file_records: list[dict[str, Any]],
    paste_after_uploading_name: str,
) -> str:
    """Return the README content for the generated startup upload pack."""
    return build_readme_content(
        date_cert=date_cert,
        generated_at=generated_at,
        zip_name=zip_name,
        file_records=file_records,
        paste_after_uploading_name=paste_after_uploading_name,
    )
