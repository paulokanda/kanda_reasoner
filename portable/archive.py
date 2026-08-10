"""Windows ZIP creation, validation, and smoke testing."""

from __future__ import annotations

import hashlib
import subprocess
import sys
import time
import zipfile
from pathlib import Path

from kanda_reasoner_app.archive_safety import (
    ArchiveSafetyError,
    safe_extract_zip,
    validate_archive_members,
)

from portable.constants import (
    MAX_ARCHIVE_PATH_BYTES,
    FIRST_SMOKE_CONFIRMATION,
    SMOKE_CONFIRMATION,
)
from portable.errors import PortableBuildError
from portable.models import BuildPaths, ZipEvidence
from portable.smoke_isolation import (
    prepared_smoke_isolation,
    verify_isolated_registry,
)
from portable.policy import (
    is_generated_handoff_or_release_path,
    is_forbidden_tool_capture_path,
    is_non_runtime_debris_path,
)


def create_windows_zip(
    paths: BuildPaths,
    stage_app: Path,
) -> None:
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
        raise PortableBuildError(
            "Windows ZIP helper failed."
        )
    if (
        "WINDOWS_EXPLORER_ZIP_CHECK=PASS"
        not in result.stdout
    ):
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
        for block in iter(
            lambda: handle.read(1024 * 1024),
            b"",
        ):
            digest.update(block)
    return digest.hexdigest()


def validate_zip(path: Path) -> ZipEvidence:
    """Validate CRC, layout, paths, boundaries, and hash."""

    with zipfile.ZipFile(path, "r") as archive_file:
        bad_member = archive_file.testzip()
        if bad_member:
            raise PortableBuildError(
                f"ZIP CRC failed: {bad_member}"
            )

        names = [
            item.filename.replace("\\", "/")
            for item in archive_file.infolist()
        ]
        try:
            member_plans = validate_archive_members(
                archive_file,
                path.parent / ".portable_zip_preflight_destination",
            )
        except ArchiveSafetyError as exc:
            raise PortableBuildError(str(exc)) from exc
        top_level = member_plans[0].relative_path.parts[0]

        maximum = 0
        for name in names:
            maximum = max(
                maximum,
                len(name.encode("utf-8")),
            )
            if is_non_runtime_debris_path(name):
                raise PortableBuildError(
                    f"Non-runtime debris ZIP member: {name}"
                )
            if is_generated_handoff_or_release_path(name):
                raise PortableBuildError(
                    f"Generated handoff/release ZIP member: {name}"
                )
            if is_forbidden_tool_capture_path(name):
                raise PortableBuildError(
                    f"Forbidden external-Project capture ZIP member: {name}"
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
    print("PORTABLE ZIP NON-RUNTIME DEBRIS ABSENT: PASS")
    print("PORTABLE SHOW PROJECT OUTPUT EXCLUSION: PASS")
    return ZipEvidence(
        size_bytes=path.stat().st_size,
        sha256=_sha256_file(path),
        member_count=len(names),
        maximum_path_bytes=maximum,
        top_level_name=top_level,
    )


def _stop_process(process: subprocess.Popen[bytes]) -> None:
    """Best-effort cleanup used only after a failed smoke test."""

    if process.poll() is not None:
        return
    process.terminate()
    try:
        process.wait(timeout=15)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait(timeout=15)


def _launch_and_require_natural_close(
    executable: Path,
    app_root: Path,
    prompt: str,
    expected: str,
    environment: dict[str, str],
) -> None:
    """Require a responsive launch followed by a normal human close."""

    process = subprocess.Popen(
        [str(executable)],
        cwd=str(app_root),
        env=environment,
    )
    succeeded = False
    try:
        time.sleep(10)
        if process.poll() is not None:
            raise PortableBuildError(
                "Packaged application exited with code "
                f"{process.returncode} before human validation."
            )

        answer = input(prompt).strip()
        if answer.casefold() != expected.casefold():
            raise PortableBuildError(
                "Manual packaged-GUI validation was denied."
            )

        try:
            return_code = process.wait(timeout=30)
        except subprocess.TimeoutExpired as exc:
            raise PortableBuildError(
                "The application was still open after confirmation. "
                "Close it normally before typing the confirmation phrase."
            ) from exc

        if return_code != 0:
            raise PortableBuildError(
                "Packaged application did not close cleanly; "
                f"exit code {return_code}."
            )
        succeeded = True
    finally:
        if not succeeded:
            _stop_process(process)


def extract_and_smoke(
    paths: BuildPaths,
    evidence: ZipEvidence,
) -> dict[str, object]:
    """Extract and launch the exact ZIP only inside disposable state."""

    with prepared_smoke_isolation(
        paths,
        evidence.top_level_name,
    ) as isolation:
        try:
            extraction_report = safe_extract_zip(
                paths.candidate_zip,
                isolation.extract_root,
                expected_top_level=evidence.top_level_name,
            )
        except ArchiveSafetyError as exc:
            raise PortableBuildError(str(exc)) from exc

        print("PORTABLE ARCHIVE POST-EXTRACTION SCOPE: PASS")
        print("PORTABLE ARCHIVE REPARSE-POINT CHECK: PASS")
        if extraction_report.member_count != evidence.member_count:
            raise PortableBuildError(
                "Clean extraction member count does not match ZIP evidence."
            )

        app_root = isolation.app_root
        direct_executables = sorted(app_root.glob("*.exe"))
        if len(direct_executables) != 1:
            raise PortableBuildError(
                "Clean extraction did not contain exactly one direct executable."
            )
        executable = direct_executables[0]

        print("PORTABLE CLEAN ZIP EXTRACTION: PASS")
        print("PORTABLE SMOKE LIVE TOOL REGISTRY BYPASSED: PASS")
        print("Launching the clean extracted Portable in disposable state...")
        print("Check:")
        print("- main window is responsive")
        print("- Project Structure 3D loads")
        print("- Show Project to AI loads")
        print("- Audit Project loads")
        print("- Config Web AI starts with no automatic credential display")
        print("- changed or important visible tabs open")
        _launch_and_require_natural_close(
            executable,
            app_root,
            (
                "Close the application normally, then type "
                f"{FIRST_SMOKE_CONFIRMATION}: "
            ),
            FIRST_SMOKE_CONFIRMATION,
            isolation.environment,
        )
        verify_isolated_registry(isolation)
        print("PORTABLE APPLICATION FIRST LAUNCH: PASS")
        print("PORTABLE APPLICATION FIRST NATURAL CLOSE: PASS")

        print("Relaunching the exact clean extracted Portable...")
        _launch_and_require_natural_close(
            executable,
            app_root,
            (
                "Close the relaunched application normally, then type "
                f"{SMOKE_CONFIRMATION}: "
            ),
            SMOKE_CONFIRMATION,
            isolation.environment,
        )
        verify_isolated_registry(isolation)
        print("PORTABLE APPLICATION RELAUNCH: PASS")
        print("PORTABLE APPLICATION RELAUNCH NATURAL CLOSE: PASS")
        print("PORTABLE CLEAN SHUTDOWN: PASS")
        print("PORTABLE HUMAN GUI SMOKE TEST: PASS")
        print("PORTABLE PACKAGED GUI SMOKE ISOLATION: PASS")
        return {
            "disposable_state": True,
            "live_tool_registry_bypassed": True,
            "isolated_tool_support": True,
            "isolated_project_support": True,
            "isolated_project_transient": True,
            "isolated_profile_and_temp": True,
            "credentials_scrubbed": True,
        }

