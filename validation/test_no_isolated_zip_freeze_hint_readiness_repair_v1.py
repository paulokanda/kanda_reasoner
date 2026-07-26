"""Validation for No Isolated ZIP freeze hint readiness repair v1."""

from __future__ import annotations

import json
import py_compile
import subprocess
import sys
import tempfile
from pathlib import Path

FEATURE_ID = "no-isolated-zip-freeze-hint-readiness-repair-v1"
EXPECTED_MARKER = "FREEZE HINT UPDATE OK: no-isolated-zip-gate-v1"

REQUIRED_MARKERS = [
    "VALIDATION OK: kanda-router-bridge-no-isolated-zip-gate-v1",
    "PATCH DELIVERY RESPONSE CONTRACT: PASS",
    "ZIP CONTRACT: PASS",
    "STATUS: IN_SYNC",
]


def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def assert_exists(path: Path) -> None:
    if not path.exists():
        raise AssertionError(f"Missing required file: {path}")


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def run_update_script(root: Path, transcript: Path) -> str:
    script = project_root() / "scripts" / "update_no_isolated_zip_freeze_hint_after_validation.py"
    cmd = [
        sys.executable,
        str(script),
        "--project-root",
        str(root),
        "--validation-transcript",
        str(transcript),
    ]
    completed = subprocess.run(cmd, capture_output=True, text=True, check=False)
    output = (completed.stdout or "") + (completed.stderr or "")
    if completed.returncode != 0:
        raise AssertionError(output)
    return output


def test_update_script() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        hint_path = (
            root
            / "project_freeze_after_update"
            / "freeze_hint_intake"
            / "kanda-router-bridge-no-isolated-zip-gate-v1__KANDA_FREEZE_HINT.json"
        )
        write_json(
            hint_path,
            {
                "schema_version": "1.0",
                "kind": "kanda_freeze_hint",
                "feature_id": "kanda-router-bridge-no-isolated-zip-gate-v1",
                "feature_title": "No Isolated ZIP Patch Delivery Gate v1",
                "validation_evidence_summary": "User-local validation remains required after install.",
                "freeze_readiness": "pre_validation_hint",
                "requires_user_validation": True,
            },
        )
        transcript = root / "validation_transcript.txt"
        transcript.write_text("\n".join(REQUIRED_MARKERS) + "\n", encoding="utf-8")

        output = run_update_script(root, transcript)
        if EXPECTED_MARKER not in output:
            raise AssertionError("Expected update marker missing from script output.")

        updated = json.loads(hint_path.read_text(encoding="utf-8"))
        if updated.get("freeze_readiness") != "local_validation_passed":
            raise AssertionError("freeze_readiness was not updated.")
        if updated.get("requires_user_validation") is not False:
            raise AssertionError("requires_user_validation was not cleared.")
        summary = updated.get("validation_evidence_summary", "")
        for marker in REQUIRED_MARKERS:
            if marker not in summary:
                raise AssertionError(f"Marker missing from evidence summary: {marker}")
        if "remains required" in summary.lower():
            raise AssertionError("Stale pending wording remains in evidence summary.")


def test_negative_missing_marker() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        hint_path = (
            root
            / "project_freeze_after_update"
            / "freeze_hint_intake"
            / "kanda-router-bridge-no-isolated-zip-gate-v1__KANDA_FREEZE_HINT.json"
        )
        write_json(
            hint_path,
            {
                "schema_version": "1.0",
                "kind": "kanda_freeze_hint",
                "feature_id": "kanda-router-bridge-no-isolated-zip-gate-v1",
            },
        )
        transcript = root / "validation_transcript.txt"
        transcript.write_text("VALIDATION OK: kanda-router-bridge-no-isolated-zip-gate-v1\n", encoding="utf-8")

        script = project_root() / "scripts" / "update_no_isolated_zip_freeze_hint_after_validation.py"
        cmd = [
            sys.executable,
            str(script),
            "--project-root",
            str(root),
            "--validation-transcript",
            str(transcript),
        ]
        completed = subprocess.run(cmd, capture_output=True, text=True, check=False)
        output = (completed.stdout or "") + (completed.stderr or "")
        if completed.returncode == 0:
            raise AssertionError("Script succeeded despite missing markers.")
        if "missing required marker" not in output.lower():
            raise AssertionError("Missing-marker error was not reported.")


def main() -> int:
    root = project_root()
    script = root / "scripts" / "update_no_isolated_zip_freeze_hint_after_validation.py"
    assert_exists(script)
    py_compile.compile(str(script), doraise=True)
    test_update_script()
    test_negative_missing_marker()
    print("VALIDATION OK: no-isolated-zip-freeze-hint-readiness-repair-v1")
    print("FREEZE HINT UPDATE CONTRACT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
