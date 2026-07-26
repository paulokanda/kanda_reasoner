"""Validate the v1r1 delivery repair for stale-variant classification."""

from __future__ import annotations

import argparse
import json
import zipfile
from pathlib import Path
from typing import Sequence

__all__ = [
    "main",
]


FEATURE_ID = "stale-variant-governed-validation-artifact-policy-v1r1"
PATCH_NAME = "kanda_stale_variant_governed_validation_artifact_policy_v1r1.zip"
MAX_MODULE_LINES = 500

REQUIRED_MEMBERS = {
    "INSTALL.ps1",
    "VALIDATE.ps1",
    "FREEZE.ps1",
    "PATCH_README.txt",
    "KANDA_FREEZE_HINT.json",
    (
        "tools/"
        "validate_stale_variant_governed_validation_artifact_policy_delivery_v1r1.py"
    ),
}

PYTHON_MEMBERS = {
    name for name in REQUIRED_MEMBERS if name.endswith(".py")
}

PREREQUISITE_PROJECT_FILES = {
    (
        "kanda_reasoner_app/manage_architecture/manage_architecture_help/"
        "source_loader_private_impl.py"
    ),
    (
        "kanda_reasoner_app/manage_architecture/manage_architecture_help/"
        "source_loader_warning_policy_private_impl.py"
    ),
    "tools/validate_cleanup_batch_11_test_internal_contract_policy_v1.py",
    "tools/validate_stale_variant_governed_validation_artifact_policy_v1.py",
}

ACTIVE_READY_KEYS = {
    "schema_version",
    "project_slug",
    "lesson_id",
    "status",
    "superseded_by",
    "operation_phase",
    "created_at_utc",
    "updated_at_utc",
    "source_patch_zip",
    "raw_error_text",
    "raw_error_snapshot_scrubbed",
    "symptom",
    "root_cause",
    "wrong_assumption",
    "correct_fix",
    "do_not_repeat_rule",
    "long_term_prevention",
    "redaction",
    "exception",
    "fingerprint",
    "prevention_triggers",
    "regression_check",
    "validation_command_summary",
    "validation_evidence",
    "install_command_summary",
    "notes",
}


def _assert(condition: bool, message: str) -> None:
    """Raise a deterministic validation error when a condition fails."""
    if not condition:
        raise AssertionError(message)


def _read_zip_text(archive: zipfile.ZipFile, name: str) -> str:
    """Read one ZIP member as strict ASCII text."""
    try:
        raw = archive.read(name)
    except KeyError as exc:
        raise AssertionError(f"ZIP_MEMBER_MISSING: {name}") from exc
    try:
        return raw.decode("ascii")
    except UnicodeDecodeError as exc:
        raise AssertionError(f"NON_ASCII_ZIP_MEMBER: {name}: {exc}") from exc


def _normalized_members(archive: zipfile.ZipFile) -> list[str]:
    """Return normalized file members without directory records."""
    return sorted(
        name.replace("\\", "/")
        for name in archive.namelist()
        if name and not name.endswith("/")
    )


def _extract_lesson(text: str, name: str) -> dict[str, object]:
    """Parse one exact marker-wrapped Error Memory lesson."""
    begin = "KANDA_ERROR_LESSON_JSON_BEGIN"
    end = "KANDA_ERROR_LESSON_JSON_END"
    _assert(text.count(begin) == 1, f"LESSON_BEGIN_MARKER_CHANGED: {name}")
    _assert(text.count(end) == 1, f"LESSON_END_MARKER_CHANGED: {name}")
    before, remainder = text.split(begin, 1)
    body, after = remainder.split(end, 1)
    _assert(not before.strip(), f"LESSON_PROSE_BEFORE_MARKER: {name}")
    _assert(not after.strip(), f"LESSON_PROSE_AFTER_MARKER: {name}")
    payload = json.loads(body.strip())
    _assert(isinstance(payload, dict), f"LESSON_NOT_OBJECT: {name}")
    return payload


def _validate_freeze_hint(archive: zipfile.ZipFile) -> None:
    """Validate exact v1r1 freeze identity and delivery state."""
    payload = json.loads(_read_zip_text(archive, "KANDA_FREEZE_HINT.json"))
    _assert(payload.get("feature_id") == FEATURE_ID, "FREEZE_FEATURE_ID_CHANGED")
    _assert(payload.get("source_patch_zip") == PATCH_NAME, "FREEZE_ZIP_CHANGED")
    _assert(payload.get("frozen") is False, "FREEZE_PRECONFIRMED")
    _assert(
        payload.get("freeze_readiness") == "requires_local_validation",
        "FREEZE_READINESS_CHANGED",
    )
    print("ROOT_FREEZE_HINT_IDENTITY: PASS")


def _validate_python_members(archive: zipfile.ZipFile) -> None:
    """Validate Python syntax, ASCII, and module-size requirements."""
    for name in sorted(PYTHON_MEMBERS):
        text = _read_zip_text(archive, name)
        compile(text, name, "exec")
        line_count = len(text.splitlines())
        _assert(
            line_count <= MAX_MODULE_LINES,
            f"MODULE_TOO_LARGE: {name}: {line_count}",
        )
    print("PYTHON_SYNTAX_ASCII_MODULE_SIZE: PASS")


def _validate_install_script(archive: zipfile.ZipFile) -> None:
    """Validate the internal install script contract."""
    text = _read_zip_text(archive, "INSTALL.ps1")
    folded = text.casefold()
    _assert("finally" not in folded, "INSTALL_FORBIDDEN_FINALLY")
    _assert("python -c" not in folded, "INSTALL_INLINE_PYTHON")
    _assert("downloads" not in folded, "INSTALL_DOWNLOADS_FALLBACK")
    _assert("desktop" not in folded, "INSTALL_DESKTOP_FALLBACK")
    _assert("$psscriptroot" in folded, "INSTALL_PATCH_ROOT_NOT_OWNED")
    _assert("_delete_after_daily_work" in folded, "INSTALL_BACKUP_ROOT_CHANGED")
    print("INSTALL_SCRIPT_CONTRACT: PASS")


def _validate_validation_script(archive: zipfile.ZipFile) -> None:
    """Validate in-memory marker capture and output persistence."""
    text = _read_zip_text(archive, "VALIDATE.ps1")
    folded = text.casefold()
    _assert("finally" not in folded, "VALIDATE_FORBIDDEN_FINALLY")
    _assert("tee-object" not in folded, "VALIDATE_TEE_OBJECT_REGRESSION")
    _assert("python -c" not in folded, "VALIDATE_INLINE_PYTHON")
    _assert("validationlines" in folded, "VALIDATION_MEMORY_CAPTURE_MISSING")
    _assert(".contains($marker)" in folded, "VALIDATION_MEMORY_CHECK_MISSING")
    _assert("scripts\\validate_patch_zip.py" in folded, "ZIP_VALIDATOR_MISSING")
    _assert(
        "validate_stale_variant_governed_validation_artifact_policy_v1.py"
        in folded,
        "FEATURE_VALIDATOR_MISSING",
    )
    _assert(FEATURE_ID in text, "DELIVERY_VALIDATION_MARKER_MISSING")
    print("VALIDATION_CAPTURE_IN_MEMORY: PASS")


def _validate_freeze_script(archive: zipfile.ZipFile) -> None:
    """Validate canonical freeze merge and post-validation lesson staging."""
    text = _read_zip_text(archive, "FREEZE.ps1")
    folded = text.casefold()
    _assert("finally" not in folded, "FREEZE_FORBIDDEN_FINALLY")
    _assert("python -c" not in folded, "FREEZE_INLINE_PYTHON")
    _assert(
        "scripts\\merge_freeze_validation_evidence.py" in folded,
        "CANONICAL_FREEZE_MERGE_MISSING",
    )
    _assert("--patch-zip" in folded, "FREEZE_PATCH_ZIP_KEY_MISSING")
    _assert("--evidence-file" in folded, "FREEZE_EVIDENCE_FILE_MISSING")
    _assert(
        "kanda_error_lesson_json_" in folded,
        "ERROR_MEMORY_MARKER_FILE_FILTER_MISSING",
    )
    _assert(
        "preview -> confirm and write" in folded,
        "HUMAN_FREEZE_CONFIRMATION_MISSING",
    )
    print("CANONICAL_FREEZE_EVIDENCE_MERGE: PASS")


def _validate_lessons(archive: zipfile.ZipFile, members: list[str]) -> None:
    """Validate packaged Error Memory lessons and correction identity."""
    lesson_names = [
        name
        for name in members
        if name.startswith("error_memory_receive_blocks/KANDA_ERROR_LESSON_JSON_")
    ]
    _assert(len(lesson_names) >= 2, "DELIVERY_CORRECTION_LESSON_MISSING")
    correction_found = False
    for name in lesson_names:
        payload = _extract_lesson(_read_zip_text(archive, name), name)
        missing = sorted(ACTIVE_READY_KEYS.difference(payload))
        _assert(not missing, f"LESSON_FIELDS_MISSING: {name}: {missing}")
        regression = payload.get("regression_check")
        _assert(isinstance(regression, dict), f"LESSON_REGRESSION_INVALID: {name}")
        command = str(regression.get("command") or "")
        _assert("\\" not in command, f"LESSON_COMMAND_BACKSLASH: {name}")
        if payload.get("lesson_id") == (
            "lesson-powershell-validation-wrapper-marker-and-finally-v1"
        ):
            correction_found = True
            _assert(
                payload.get("source_patch_zip") == PATCH_NAME,
                "CORRECTION_LESSON_PATCH_IDENTITY_CHANGED",
            )
            _assert(
                payload.get("status") == "draft",
                "CORRECTION_LESSON_PREMATURELY_ACTIVE",
            )
    _assert(correction_found, "DELIVERY_CORRECTION_LESSON_NOT_FOUND")
    print("ERROR_MEMORY_CORRECTION_INTAKE: PASS")


def _validate_patch_zip(path: Path) -> None:
    """Validate the exact final v1r1 patch archive."""
    _assert(path.is_file(), f"PATCH_ZIP_MISSING: {path}")
    _assert(path.name == PATCH_NAME, f"PATCH_ZIP_NAME_CHANGED: {path.name}")
    with zipfile.ZipFile(path, "r") as archive:
        members = _normalized_members(archive)
        missing = sorted(REQUIRED_MEMBERS.difference(members))
        _assert(not missing, "PATCH_REQUIRED_MEMBERS_MISSING: " + repr(missing))
        _assert(
            members.count("KANDA_FREEZE_HINT.json") == 1,
            "ROOT_FREEZE_HINT_COUNT_CHANGED",
        )
        _validate_freeze_hint(archive)
        _validate_python_members(archive)
        _validate_install_script(archive)
        _validate_validation_script(archive)
        _validate_freeze_script(archive)
        _validate_lessons(archive, members)
    print("PATCH_DELIVERY_REQUIRED_MEMBERS: PASS")


def _validate_installed_files(project_root: Path) -> None:
    """Validate installed delivery and prerequisite project files."""
    for relative_text in sorted(PYTHON_MEMBERS):
        path = project_root / Path(relative_text)
        _assert(path.is_file(), f"INSTALLED_FILE_MISSING: {relative_text}")
        text = path.read_text(encoding="ascii")
        compile(text, str(path), "exec")
        _assert(
            len(text.splitlines()) <= MAX_MODULE_LINES,
            f"INSTALLED_MODULE_TOO_LARGE: {relative_text}",
        )

    for relative_text in sorted(PREREQUISITE_PROJECT_FILES):
        path = project_root / Path(relative_text)
        _assert(path.is_file(), f"PREREQUISITE_FILE_MISSING: {relative_text}")
        compile(path.read_text(encoding="ascii"), str(path), "exec")

    print("INSTALLED_DELIVERY_FILES: PASS")
    print("V1_FEATURE_PREREQUISITES: PASS")


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line parser."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--patch-zip", required=True)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the focused delivery repair validator."""
    args = build_parser().parse_args(argv)
    project_root = Path(args.project_root).expanduser().resolve()
    patch_zip = Path(args.patch_zip).expanduser().resolve()
    _assert(project_root.is_dir(), f"PROJECT_ROOT_MISSING: {project_root}")
    _validate_patch_zip(patch_zip)
    _validate_installed_files(project_root)
    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
