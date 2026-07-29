"""Windows ZIP creation, validation, and smoke testing."""

from __future__ import annotations

import hashlib
import shutil
import subprocess
import sys
import time
import zipfile
from pathlib import Path

from portable.constants import (
    FORBIDDEN_GENERATED_TOKENS,
    MAX_ARCHIVE_PATH_BYTES,
)
from portable.errors import PortableBuildError
from portable.models import BuildPaths, ZipEvidence


def create_windows_zip(paths: BuildPaths, stage_app: Path) -> None:
    """Create the candidate ZIP with the validated .NET method."""

    command = [
        "powershell.exe",
        "-NoProfile",
        "-ExecutionPolicy",
        "Bypass",
        "-File",
        str(paths.zip_helper),
        "-SourceDirectory",
        str(stage_app),
        "-DestinationZip",
        str(paths.candidate_zip),
    ]
    result = subprocess.run(
        command,
        cwd=str(paths.run_root),
        capture_output=True,
        text=True,
        check=False,
    )

    if result.stdout:
        print(result.stdout.rstrip())
    if result.stderr:
        print(result.stderr.rstrip(), file=sys.stderr)
    if result.returncode != 0:
        raise PortableBuildError("Windows ZIP helper failed.")
    if "WINDOWS_EXPLORER_ZIP_CHECK=PASS" not in result.stdout:
        raise PortableBuildError(
            "Windows Explorer did not accept the ZIP."
        )
    if "TOP_LEVEL_ENTRIES=1" not in result.stdout:
        raise PortableBuildError(
            "ZIP does not have exactly one top-level entry."
        )
    print("PORTABLE WINDOWS EXPLORER ZIP CHECK: PASS")


def _unsafe_member(name: str) -> bool:
    normalized = name.replace("\\", "/")
    if normalized.startswith("/"):
        return True
    if len(normalized) >= 2 and normalized[1] == ":":
        return True
    return ".." in Path(normalized).parts


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def validate_zip(path: Path) -> ZipEvidence:
    """Validate CRC, layout, paths, boundaries, and hash."""

    with zipfile.ZipFile(path, "r") as archive:
        bad_member = archive.testzip()
        if bad_member:
            raise PortableBuildError(f"ZIP CRC failed: {bad_member}")

        names = [
            item.filename.replace("\\", "/")
            for item in archive.infolist()
        ]
        folded = [name.casefold() for name in names]
        if len(folded) != len(set(folded)):
            raise PortableBuildError(
                "ZIP contains duplicate case-insensitive members."
            )
        if any(_unsafe_member(name) for name in names):
            raise PortableBuildError("ZIP contains an unsafe member path.")

        top_levels = {
            name.rstrip("/").split("/", 1)[0]
            for name in names
            if name.rstrip("/")
        }
        if len(top_levels) != 1:
            raise PortableBuildError(
                "ZIP top-level contract failed: "
                f"{sorted(top_levels)}"
            )
        top_level = next(iter(top_levels))

        maximum = 0
        for name in names:
            maximum = max(maximum, len(name.encode("utf-8")))
            lowered = name.casefold()
            if any(
                token in lowered
                for token in FORBIDDEN_GENERATED_TOKENS
            ):
                raise PortableBuildError(
                    f"Generated handoff/release ZIP member: {name}"
                )
            if Path(name).name.casefold().startswith(".env"):
                raise PortableBuildError(
                    f"Environment credential ZIP member: {name}"
                )

        if maximum > MAX_ARCHIVE_PATH_BYTES:
            raise PortableBuildError(
                "ZIP member path exceeds "
                f"{MAX_ARCHIVE_PATH_BYTES} bytes."
            )

        direct_executables = [
            name
            for name in names
            if name.casefold().endswith(".exe")
            and name.rstrip("/").count("/") == 1
        ]
        if len(direct_executables) != 1:
            raise PortableBuildError(
                "Expected one direct application executable; found: "
                f"{direct_executables}"
            )

    print("PORTABLE ZIP INTEGRITY: PASS")
    print("PORTABLE ZIP PATH SAFETY: PASS")
    print("PORTABLE SHOW PROJECT OUTPUT EXCLUSION: PASS")
    return ZipEvidence(
        size_bytes=path.stat().st_size,
        sha256=_sha256_file(path),
        member_count=len(names),
        maximum_path_bytes=maximum,
        top_level_name=top_level,
    )


def extract_and_smoke(paths: BuildPaths, evidence: ZipEvidence) -> None:
    """Extract and launch the exact candidate for human validation."""

    if paths.clean_extract_root.exists():
        shutil.rmtree(paths.clean_extract_root)
    paths.clean_extract_root.mkdir(parents=True)

    with zipfile.ZipFile(paths.candidate_zip, "r") as archive:
        archive.extractall(paths.clean_extract_root)

    app_root = paths.clean_extract_root / evidence.top_level_name
    direct_executables = sorted(app_root.glob("*.exe"))
    if len(direct_executables) != 1:
        raise PortableBuildError(
            "Clean extraction did not contain exactly one direct executable."
        )
    executable = direct_executables[0]

    print("PORTABLE CLEAN ZIP EXTRACTION: PASS")
    print("Launching the clean extracted Portable...")
    process = subprocess.Popen([str(executable)], cwd=str(app_root))
    try:
        time.sleep(10)
        if process.poll() is not None:
            raise PortableBuildError(
                "Packaged application exited with code "
                f"{process.returncode}."
            )

        print("Check the main window, Project Structure 3D, Show Project,")
        print("Audit Project, and that Web AI credentials start blank.")
        answer = input(
            "Type YES after the extracted GUI works: "
        ).strip()
        if answer.casefold() != "yes":
            raise PortableBuildError(
                "Manual packaged-GUI validation was denied."
            )

        print("PORTABLE APPLICATION LAUNCH: PASS")
        print("PORTABLE HUMAN GUI SMOKE TEST: PASS")
    finally:
        if process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=15)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=15)
