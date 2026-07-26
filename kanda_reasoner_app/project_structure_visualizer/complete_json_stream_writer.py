"""Direct-to-ZIP streaming writer for Project Structure 3D complete JSON."""

from __future__ import annotations

import hashlib
import json
import os
import zipfile
from pathlib import Path
from typing import Any

from .complete_json_artifacts import (
    COMPLETE_JSON_PART_LIMIT_BYTES,
    COMPLETE_JSON_STREAM_ROTATE_BYTES,
)

__all__ = ["CompleteJsonZipStreamWriter"]


class CompleteJsonZipStreamWriter:
    """Write one logical JSON byte stream directly into bounded ZIP parts."""

    def __init__(self, output_dir: Path, project_slug: str) -> None:
        self.output_dir = Path(output_dir)
        self.project_slug = str(project_slug)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.original_filename = self.project_slug + "__complete.json"
        self._archive: zipfile.ZipFile | None = None
        self._member = None
        self._part_index = 0
        self._part_uncompressed = 0
        self._part_digest = hashlib.sha256()
        self._whole_digest = hashlib.sha256()
        self._whole_size = 0
        self._temporary_records: list[dict[str, Any]] = []
        self._open_part()

    def _temporary_part_path(self, index: int) -> Path:
        return self.output_dir / (
            "." + self.project_slug + "__complete_json_part" + str(index).zfill(4) + ".zip.tmp"
        )

    def _member_name(self, index: int) -> str:
        return self.original_filename + ".part" + str(index).zfill(4)

    def _open_part(self) -> None:
        self._part_index += 1
        path = self._temporary_part_path(self._part_index)
        self._archive = zipfile.ZipFile(
            path,
            "w",
            compression=zipfile.ZIP_DEFLATED,
            compresslevel=6,
            allowZip64=True,
        )
        self._member = self._archive.open(
            self._member_name(self._part_index),
            "w",
            force_zip64=True,
        )
        self._part_uncompressed = 0
        self._part_digest = hashlib.sha256()

    def _close_part(self) -> None:
        if self._member is None or self._archive is None:
            return
        self._member.close()
        self._archive.close()
        temp_path = self._temporary_part_path(self._part_index)
        size = temp_path.stat().st_size
        if size > COMPLETE_JSON_PART_LIMIT_BYTES:
            raise ValueError(
                "Complete JSON ZIP part exceeds 450 MB: " + temp_path.name
            )
        self._temporary_records.append(
            {
                "temp_path": temp_path,
                "member_name": self._member_name(self._part_index),
                "member_size_bytes": self._part_uncompressed,
                "member_sha256": self._part_digest.hexdigest(),
            }
        )
        self._member = None
        self._archive = None

    def write(self, data: bytes | str) -> None:
        """Write bytes, rotating before the uncompressed safety threshold."""
        payload = data.encode("utf-8") if isinstance(data, str) else bytes(data)
        offset = 0
        while offset < len(payload):
            remaining = COMPLETE_JSON_STREAM_ROTATE_BYTES - self._part_uncompressed
            if remaining <= 0:
                self._close_part()
                self._open_part()
                remaining = COMPLETE_JSON_STREAM_ROTATE_BYTES
            chunk = payload[offset : offset + remaining]
            assert self._member is not None
            self._member.write(chunk)
            self._part_digest.update(chunk)
            self._whole_digest.update(chunk)
            self._part_uncompressed += len(chunk)
            self._whole_size += len(chunk)
            offset += len(chunk)

    def write_json(self, value: Any) -> None:
        """Serialize one bounded value without materializing the full document."""
        self.write(
            json.dumps(
                value,
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
            )
        )

    def finish(self) -> dict[str, Any]:
        """Close, rename, and return manifest-ready part records."""
        self._close_part()
        total = len(self._temporary_records)
        records: list[dict[str, Any]] = []
        for index, item in enumerate(self._temporary_records, start=1):
            final_name = (
                self.project_slug
                + "__complete_json_part"
                + str(index).zfill(2)
                + "_of_"
                + str(total).zfill(2)
                + ".zip"
            )
            final_path = self.output_dir / final_name
            os.replace(item["temp_path"], final_path)
            digest = hashlib.sha256()
            with final_path.open("rb") as handle:
                for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                    digest.update(chunk)
            records.append(
                {
                    "package": "complete_json",
                    "filename": final_name,
                    "size_bytes": final_path.stat().st_size,
                    "sha256": digest.hexdigest(),
                    "member_name": item["member_name"],
                    "member_size_bytes": item["member_size_bytes"],
                    "member_sha256": item["member_sha256"],
                }
            )
        return {
            "original_filename": self.original_filename,
            "original_size_bytes": self._whole_size,
            "original_sha256": self._whole_digest.hexdigest(),
            "parts": records,
        }

    def abort(self) -> None:
        """Close handles and remove temporary ZIP files after failure."""
        try:
            if self._member is not None:
                self._member.close()
        finally:
            if self._archive is not None:
                self._archive.close()
        for path in self.output_dir.glob(".*__complete_json_part*.zip.tmp"):
            try:
                path.unlink()
            except OSError:
                pass
