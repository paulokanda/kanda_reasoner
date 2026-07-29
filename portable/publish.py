"""Validated cross-volume publication to the selected folder."""

from __future__ import annotations

import os
import shutil
import uuid
from pathlib import Path

from portable.archive import validate_zip
from portable.errors import PortableBuildError
from portable.models import BuildPaths, ZipEvidence


def publish_candidate(
    paths: BuildPaths,
    candidate_evidence: ZipEvidence,
) -> ZipEvidence:
    """Copy, revalidate, and atomically publish in the selected folder."""

    temporary = paths.final_zip.with_name(
        f".{paths.final_zip.name}.{uuid.uuid4().hex}.partial"
    )
    try:
        shutil.copyfile(paths.candidate_zip, temporary)
        copied_evidence = validate_zip(temporary)
        if copied_evidence.sha256 != candidate_evidence.sha256:
            raise PortableBuildError(
                "Publication copy SHA-256 differs from the validated candidate."
            )
        if copied_evidence.size_bytes != candidate_evidence.size_bytes:
            raise PortableBuildError(
                "Publication copy size differs from the validated candidate."
            )

        os.replace(temporary, paths.final_zip)
        final_evidence = validate_zip(paths.final_zip)
        if final_evidence.sha256 != candidate_evidence.sha256:
            raise PortableBuildError(
                "Published Portable SHA-256 differs from the candidate."
            )
        print("PORTABLE SELECTED-FOLDER ATOMIC PUBLICATION: PASS")
        return final_evidence
    finally:
        temporary.unlink(missing_ok=True)
