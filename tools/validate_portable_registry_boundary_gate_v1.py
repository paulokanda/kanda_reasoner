"""Validate the Portable registry boundary gate without building a Portable."""

from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
import uuid
from pathlib import Path
from typing import Callable


def _project_root_from_args() -> Path:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--project-root",
        type=Path,
        default=Path(r"E:\kanda_reasoner"),
    )
    return parser.parse_args().project_root.resolve()


PROJECT_ROOT = _project_root_from_args()
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from portable import destination  # noqa: E402
from portable.constants import (  # noqa: E402
    FINAL_ZIP_NAME,
    PORTABLE_HARDENING_FEATURES,
    PRODUCTION_PORTABLE_ENABLED,
)
from portable.errors import PortableBuildError  # noqa: E402
from portable.paths import resolve_paths  # noqa: E402
from portable.registry_boundary import (  # noqa: E402
    EXPLICIT_SELF_HOSTING,
    assert_outside_protected_roots,
    load_registry_boundary,
    validate_publication_directory,
    validate_result_path,
)


def require(condition: bool, code: str) -> None:
    if not condition:
        raise RuntimeError(code)


def expect_blocked(
    label: str,
    action: Callable[[], object],
    *,
    message_fragment: str | None = None,
) -> None:
    try:
        action()
    except PortableBuildError as exc:
        if message_fragment is not None:
            require(
                message_fragment.casefold() in str(exc).casefold(),
                f"{label}_WRONG_ERROR:{exc}",
            )
        print(f"{label}: PASS")
        return
    raise RuntimeError(f"{label}_NOT_BLOCKED")


def write_registry(
    path: Path,
    *,
    active_root: Path,
    active_mode: str,
) -> None:
    drive = Path(PROJECT_ROOT.anchor).resolve()
    tool_support = drive / f"{PROJECT_ROOT.name}_show_project_to_AI"
    eeg_root = drive / "eeg_kanda"
    eeg_support = drive / "eeg_kanda_show_project_to_AI"
    payload = {
        "current_project_id": "tool-project-id",
        "projects": {
            "tool-project-id": {
                "stable_project_id": "tool-project-id",
                "owner_slug": "kanda_reasoner",
                "project_root": str(active_root),
                "project_support_root": str(tool_support),
                "selection_mode": active_mode,
            },
            "eeg-project-id": {
                "stable_project_id": "eeg-project-id",
                "owner_slug": "eeg_kanda",
                "project_root": str(eeg_root),
                "project_support_root": str(eeg_support),
                "selection_mode": "EXPLICIT_EXTERNAL_PROJECT",
            },
        },
    }
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def main() -> int:
    require(os.name == "nt", "WINDOWS_REQUIRED")
    require(PROJECT_ROOT.name.casefold() == "kanda_reasoner", "TOOL_ROOT_NAME")
    require(
        "registry-boundary-gate" in PORTABLE_HARDENING_FEATURES,
        "REGISTRY_BOUNDARY_CAPABILITY_MISSING",
    )
    print("PORTABLE REGISTRY BOUNDARY CAPABILITY IDENTITY: PASS")
    require(
        PRODUCTION_PORTABLE_ENABLED is False,
        "PRODUCTION_PORTABLE_MUST_REMAIN_BLOCKED",
    )
    print("PORTABLE PRODUCTION BUILD GATE CLOSED: PASS")

    live = load_registry_boundary(PROJECT_ROOT)
    require(live.selection_mode == EXPLICIT_SELF_HOSTING, "LIVE_MODE_MISMATCH")
    require(live.tool_root == PROJECT_ROOT, "LIVE_TOOL_ROOT_MISMATCH")
    require(len(live.protected_roots) >= 3, "LIVE_PROTECTED_ROOTS_MISSING")
    print("PORTABLE LIVE EXPLICIT SELF-HOSTING AUTHORITY: PASS")
    print("PORTABLE LIVE REGISTERED OWNER ROOTS LOADED: PASS")

    with tempfile.TemporaryDirectory(
        prefix="kanda_portable_registry_boundary_v1_"
    ) as raw_temp:
        temp_root = Path(raw_temp).resolve()
        registry_path = temp_root / "projects.json"
        write_registry(
            registry_path,
            active_root=PROJECT_ROOT,
            active_mode=EXPLICIT_SELF_HOSTING,
        )
        boundary = load_registry_boundary(
            PROJECT_ROOT,
            registry_path=registry_path,
        )

        drive = Path(PROJECT_ROOT.anchor).resolve()
        tool_support = drive / "kanda_reasoner_show_project_to_AI"
        tool_transient = drive / "kanda_reasoner_delete_after_daily_work"
        eeg_root = drive / "eeg_kanda"
        eeg_support = drive / "eeg_kanda_show_project_to_AI"
        eeg_transient = drive / "eeg_kanda_delete_after_daily_work"

        expected_roots = {
            str(path.resolve()).casefold()
            for path in (
                PROJECT_ROOT,
                tool_support,
                tool_transient,
                eeg_root,
                eeg_support,
                eeg_transient,
            )
        }
        actual_roots = {
            str(item.path.resolve()).casefold()
            for item in boundary.protected_roots
        }
        require(expected_roots.issubset(actual_roots), "REGISTERED_ROOT_SET_MISMATCH")
        print("PORTABLE ALL REGISTERED SOURCE SUPPORT TRANSIENT ROOTS: PASS")

        for label, root in (
            ("PORTABLE TOOL SOURCE DESTINATION BLOCKED", PROJECT_ROOT),
            ("PORTABLE TOOL SUPPORT DESTINATION BLOCKED", tool_support),
            ("PORTABLE TOOL TRANSIENT DESTINATION BLOCKED", tool_transient),
            ("PORTABLE OTHER PROJECT SOURCE DESTINATION BLOCKED", eeg_root),
            ("PORTABLE OTHER PROJECT SUPPORT DESTINATION BLOCKED", eeg_support),
            ("PORTABLE OTHER PROJECT TRANSIENT DESTINATION BLOCKED", eeg_transient),
        ):
            expect_blocked(
                label,
                lambda root=root: validate_publication_directory(
                    root,
                    boundary,
                    final_zip_name=FINAL_ZIP_NAME,
                ),
                message_fragment="protected",
            )

        safe_output = temp_root / "safe_output"
        safe_output.mkdir()
        validated = validate_publication_directory(
            safe_output,
            boundary,
            final_zip_name=FINAL_ZIP_NAME,
        )
        require(validated == safe_output, "SAFE_DESTINATION_CHANGED")
        print("PORTABLE OUTSIDE-OWNER DESTINATION ACCEPTED: PASS")

        probe_calls: list[Path] = []
        original_probe = destination._verify_writable

        def tracked_probe(path: Path) -> None:
            probe_calls.append(path.resolve())

        destination._verify_writable = tracked_probe
        try:
            expect_blocked(
                "PORTABLE PROTECTED DESTINATION REJECTED BEFORE WRITE PROBE",
                lambda: destination.select_output_directory(
                    PROJECT_ROOT,
                    PROJECT_ROOT,
                    boundary,
                ),
                message_fragment="protected",
            )
            require(not probe_calls, "PROBE_RAN_BEFORE_PROTECTED_REJECTION")

            selected = destination.select_output_directory(
                PROJECT_ROOT,
                safe_output,
                boundary,
            )
            require(selected == safe_output, "SAFE_SELECTED_OUTPUT_MISMATCH")
            require(probe_calls == [safe_output], "SAFE_PROBE_CALL_COUNT_MISMATCH")
        finally:
            destination._verify_writable = original_probe
        print("PORTABLE DESTINATION PROBE ORDERING: PASS")

        unique_parent = (
            eeg_support
            / f"__portable_boundary_must_not_create_{uuid.uuid4().hex}"
        )
        blocked_result = unique_parent / "result.json"
        require(not unique_parent.exists(), "RESULT_TEST_PARENT_PREEXISTS")
        expect_blocked(
            "PORTABLE OTHER PROJECT RESULT JSON BLOCKED",
            lambda: validate_result_path(blocked_result, boundary),
            message_fragment="protected",
        )
        require(not unique_parent.exists(), "RESULT_PARENT_CREATED_BEFORE_REJECTION")
        print("PORTABLE RESULT JSON REJECTED BEFORE PARENT CREATION: PASS")

        safe_result = validate_result_path(
            temp_root / "safe_result" / "result.json",
            boundary,
        )
        require(
            safe_result == temp_root / "safe_result" / "result.json",
            "SAFE_RESULT_PATH_MISMATCH",
        )
        print("PORTABLE OUTSIDE-OWNER RESULT JSON ACCEPTED: PASS")

        original_registry_text = registry_path.read_text(encoding="utf-8")
        registry_path.write_text(
            original_registry_text + " ",
            encoding="utf-8",
        )
        expect_blocked(
            "PORTABLE REGISTRY TOCTOU CHANGE REJECTED",
            lambda: validate_result_path(
                temp_root / "changed_registry_result.json",
                boundary,
            ),
            message_fragment="changed during",
        )
        registry_path.write_text(
            original_registry_text,
            encoding="utf-8",
            newline="\n",
        )
        boundary = load_registry_boundary(
            PROJECT_ROOT,
            registry_path=registry_path,
        )

        resolved = resolve_paths(PROJECT_ROOT, safe_output, boundary)
        require(
            resolved.registry_boundary == boundary,
            "BUILD_PATHS_REGISTRY_BOUNDARY_MISSING",
        )
        require(
            str(resolved.run_root).casefold().startswith(
                str(tool_transient.resolve()).casefold()
            ),
            "RUN_ROOT_OUTSIDE_TOOL_TRANSIENT",
        )
        assert_outside_protected_roots(
            resolved.final_zip,
            boundary,
            purpose="validator final ZIP",
        )
        print("PORTABLE RESOLVED BUILD PATHS BOUNDARY: PASS")

        write_registry(
            registry_path,
            active_root=drive / "eeg_kanda",
            active_mode="EXPLICIT_EXTERNAL_PROJECT",
        )
        expect_blocked(
            "PORTABLE EXTERNAL ACTIVE PROJECT REJECTED",
            lambda: load_registry_boundary(
                PROJECT_ROOT,
                registry_path=registry_path,
            ),
            message_fragment="active Project",
        )

        write_registry(
            registry_path,
            active_root=PROJECT_ROOT,
            active_mode="",
        )
        expect_blocked(
            "PORTABLE IMPLICIT SELF-HOSTING REJECTED",
            lambda: load_registry_boundary(
                PROJECT_ROOT,
                registry_path=registry_path,
            ),
            message_fragment="explicit self-hosting",
        )

    print("VALIDATION OK: portable-registry-boundary-gate-v1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
