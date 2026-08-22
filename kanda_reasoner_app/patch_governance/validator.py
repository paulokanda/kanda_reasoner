# project-path: kanda_reasoner_app/patch_governance/validator.py
"""Deterministic contract validator for installable patch ZIPs."""

from __future__ import annotations


__all__ = ['PatchZipContractError', 'validate_install_script_text', 'validate_patch_zip']
import argparse
import json
from pathlib import Path
from typing import Any, Mapping
import zipfile

from .delivery_provenance_contract import (
    DeliveryProvenanceContractError,
    validate_delivery_provenance_contract,
)
from .models import (
    FREEZE_HINT_FILENAME,
    MANDATORY_FREEZE_FIELDS,
    PLACEHOLDER_FRAGMENTS,
)
from .zip_member_contract import (
    ZipMemberContractError,
    validate_zip_member_contract,
)
from .error_memory_intake_contract import pending_intake_payload_failures

FORBIDDEN_INSTALL_FRAGMENTS = (
    "downloads",
    "desktop",
    "getfolderpath",
    "specialfolder",
)

REQUIRED_INSTALL_FRAGMENTS = (
    "_delete_after_daily_work",
    "[system.io.path]::getpathroot",
    "clear-host",
    "expand-archive",
    "install ok. terminal will clear in 2 seconds",
    "start-sleep -seconds 2",
    "press enter to clear terminal",
    "press enter again to clear",
)
FORBIDDEN_TERMINAL_FRAGMENTS = (
    "start-sleep -seconds 5",
    "press enter again to finish",
    "exit 1",
    "stop-process",
)


class PatchZipContractError(RuntimeError):
    """Raised when a patch ZIP or installer violates delivery contract."""


def _raise(message: str) -> None:
    """Support raise behavior.
    
    Parameters
    ----------
    message : str
        The message text.
    """
    
    raise PatchZipContractError(message)


def _is_empty(value: Any) -> bool:
    """Support is empty behavior.
    
    Parameters
    ----------
    value : Any
        The input value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    return value is None or value == "" or value == [] or value == {}


def _has_placeholder(value: Any) -> bool:
    """Support has placeholder behavior.
    
    Parameters
    ----------
    value : Any
        The input value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    text = json.dumps(value, ensure_ascii=True).lower() if not isinstance(value, str) else value.lower()
    return any(fragment in text for fragment in PLACEHOLDER_FRAGMENTS)


def _payload_roots(names: list[str]) -> set[str]:
    """Support payload roots behavior.
    
    Parameters
    ----------
    names : list[str]
        The name values.
    
    Returns
    -------
    set[str]
        The set result.
    """
    
    roots: set[str] = set()
    for name in names:
        clean = name.strip("/")
        if not clean or "/" not in clean:
            continue
        root = clean.split("/", 1)[0]
        if root:
            roots.add(root)
    return roots


def _validate_hint_data(hint: Mapping[str, Any]) -> None:
    """Support validate hint data behavior.
    
    Parameters
    ----------
    hint : Mapping[str, Any]
        The hint value.
    """
    
    missing = [field for field in MANDATORY_FREEZE_FIELDS if field not in hint]
    if missing:
        _raise("KANDA_FREEZE_HINT.json missing mandatory fields: " + ", ".join(missing))

    for field in MANDATORY_FREEZE_FIELDS:
        value = hint.get(field)
        if _is_empty(value):
            _raise(f"KANDA_FREEZE_HINT.json field is empty: {field}")
        if _has_placeholder(value):
            _raise(f"KANDA_FREEZE_HINT.json field contains placeholder text: {field}")

    if str(hint.get("kind")) != "kanda_freeze_hint":
        _raise("KANDA_FREEZE_HINT.json kind must be kanda_freeze_hint.")

    if not isinstance(hint.get("validated_files"), list):
        _raise("KANDA_FREEZE_HINT.json validated_files must be a JSON list.")
    if not hint.get("validated_files"):
        _raise("KANDA_FREEZE_HINT.json validated_files is empty.")
    if not isinstance(hint.get("generated_files"), list):
        _raise("KANDA_FREEZE_HINT.json generated_files must be a JSON list.")
    if not isinstance(hint.get("protected_paths"), list) or not hint.get("protected_paths"):
        _raise("KANDA_FREEZE_HINT.json protected_paths must be a non-empty JSON list.")
    if not isinstance(hint.get("do_not_regress_rules"), list) or not hint.get("do_not_regress_rules"):
        _raise("KANDA_FREEZE_HINT.json do_not_regress_rules must be a non-empty JSON list.")



ERROR_LESSON_JSON_BEGIN = "KANDA_ERROR_LESSON_JSON_BEGIN"
ERROR_LESSON_JSON_END = "KANDA_ERROR_LESSON_JSON_END"
ERROR_MEMORY_LESSON_PREFIX = "KANDA_ERROR_LESSON_JSON_"
ERROR_MEMORY_LESSON_SUFFIXES = (".txt", ".md", ".json")
ERROR_MEMORY_MEMBER_MAX_BYTES = 2_000_000

ERROR_MEMORY_BASE_REQUIRED_KEYS = (
    "schema_version",
    "lesson_id",
    "status",
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
    "long_term_prevention",
    "do_not_repeat_rule",
    "prevention_triggers",
    "exception",
    "fingerprint",
    "regression_check",
    "validation_command_summary",
    "validation_evidence",
    "redaction",
    "install_command_summary",
    "notes",
)

ERROR_MEMORY_ACTIVE_REQUIRED_KEYS = ERROR_MEMORY_BASE_REQUIRED_KEYS
ERROR_MEMORY_ACTIVE_NONEMPTY_KEYS = (
    "raw_error_text",
    "raw_error_snapshot_scrubbed",
    "symptom",
    "root_cause",
    "wrong_assumption",
    "correct_fix",
    "long_term_prevention",
    "do_not_repeat_rule",
    "validation_command_summary",
    "validation_evidence",
    "prevention_triggers",
)
ERROR_MEMORY_EXCEPTION_REQUIRED_KEYS = (
    "type",
    "phase",
    "relative_file_path",
    "function_or_test_name",
    "message_normalized",
    "stacktrace_scrubbed",
)
ERROR_MEMORY_FINGERPRINT_REQUIRED_KEYS = (
    "strategy",
    "components",
    "fingerprint_hash",
)
ERROR_MEMORY_REGRESSION_REQUIRED_KEYS = (
    "type",
    "command",
    "expected_marker",
    "required_before_freeze",
)


def _is_error_memory_lesson_member(member_name: str) -> bool:
    """Return whether an archive member is a packaged Error Memory lesson block."""
    normalized = str(member_name or "").replace("\\", "/").strip()
    if not normalized or normalized.endswith("/"):
        return False
    base = Path(normalized).name
    if not base.startswith(ERROR_MEMORY_LESSON_PREFIX):
        return False
    return Path(base).suffix.lower() in ERROR_MEMORY_LESSON_SUFFIXES


def _lesson_block_json_text(raw_text: str, member_name: str) -> str:
    """Extract JSON text from a marker-wrapped or plain JSON lesson block."""
    text = str(raw_text or "").strip()
    if ERROR_LESSON_JSON_BEGIN in text or ERROR_LESSON_JSON_END in text:
        if ERROR_LESSON_JSON_BEGIN not in text or ERROR_LESSON_JSON_END not in text:
            _raise("Error Memory lesson block markers are incomplete: " + member_name)
        text = text.split(ERROR_LESSON_JSON_BEGIN, 1)[1].split(ERROR_LESSON_JSON_END, 1)[0].strip()
    if not text:
        _raise("Error Memory lesson block is empty: " + member_name)
    return text


def _error_memory_value_missing(value: Any) -> bool:
    """Return whether an Error Memory lesson value is missing for schema-gate purposes."""
    return value is None or value == "" or value == [] or value == {}


def _validate_error_memory_lesson_payload(payload: Mapping[str, Any], member_name: str) -> None:
    """Validate the package-time schema contract for one Error Memory lesson block."""
    missing = [key for key in ERROR_MEMORY_BASE_REQUIRED_KEYS if key not in payload]
    if missing:
        _raise(
            "Error Memory lesson block missing required keys in "
            + member_name
            + ": "
            + ", ".join(missing)
        )

    if str(payload.get("schema_version", "")).strip() != "1.0":
        _raise("Error Memory lesson block schema_version must be 1.0 in " + member_name)

    status = str(payload.get("status", "")).strip().lower()
    if status not in {"draft", "active", "deprecated", "superseded"}:
        _raise("Error Memory lesson block status is invalid in " + member_name)

    if not isinstance(payload.get("prevention_triggers"), list) or not payload.get("prevention_triggers"):
        _raise("Error Memory lesson block prevention_triggers must be a non-empty list in " + member_name)

    exception = payload.get("exception")
    if not isinstance(exception, Mapping):
        _raise("Error Memory lesson block exception must be an object in " + member_name)
    exception_missing = [key for key in ERROR_MEMORY_EXCEPTION_REQUIRED_KEYS if key not in exception]
    if exception_missing:
        _raise("Error Memory lesson block exception missing keys in " + member_name + ": " + ", ".join(exception_missing))
    for key in ("type", "phase", "message_normalized"):
        if _error_memory_value_missing(exception.get(key)):
            _raise("Error Memory lesson block exception." + key + " is empty in " + member_name)

    fingerprint = payload.get("fingerprint")
    if not isinstance(fingerprint, Mapping):
        _raise("Error Memory lesson block fingerprint must be an object in " + member_name)
    fingerprint_missing = [key for key in ERROR_MEMORY_FINGERPRINT_REQUIRED_KEYS if key not in fingerprint]
    if fingerprint_missing:
        _raise("Error Memory lesson block fingerprint missing keys in " + member_name + ": " + ", ".join(fingerprint_missing))
    if _error_memory_value_missing(fingerprint.get("strategy")):
        _raise("Error Memory lesson block fingerprint.strategy is empty in " + member_name)
    if not isinstance(fingerprint.get("components"), list) or not fingerprint.get("components"):
        _raise("Error Memory lesson block fingerprint.components must be a non-empty list in " + member_name)
    if _error_memory_value_missing(fingerprint.get("fingerprint_hash")):
        _raise("Error Memory lesson block fingerprint.fingerprint_hash is empty in " + member_name)

    redaction = payload.get("redaction")
    if not isinstance(redaction, Mapping):
        _raise("Error Memory lesson block redaction must be an object in " + member_name)
    if not redaction.get("applied") or not redaction.get("export_safe"):
        _raise("Error Memory lesson block redaction.applied and redaction.export_safe must be true in " + member_name)
    if not isinstance(redaction.get("rules"), list) or not redaction.get("rules"):
        _raise("Error Memory lesson block redaction.rules must be a non-empty list in " + member_name)

    regression_check = payload.get("regression_check")
    if not isinstance(regression_check, Mapping):
        _raise("Error Memory lesson block regression_check must be an object in " + member_name)
    regression_missing = [key for key in ERROR_MEMORY_REGRESSION_REQUIRED_KEYS if key not in regression_check]
    if regression_missing:
        _raise("Error Memory lesson block regression_check missing keys in " + member_name + ": " + ", ".join(regression_missing))
    if str(regression_check.get("type", "")).strip() == "validation_command":
        if not str(regression_check.get("command", "")).strip():
            _raise("Error Memory lesson block regression_check.command is empty for validation_command in " + member_name)
        if not str(regression_check.get("expected_marker", "")).strip():
            _raise("Error Memory lesson block regression_check.expected_marker is empty for validation_command in " + member_name)

    if status == "active":
        active_missing = [key for key in ERROR_MEMORY_ACTIVE_REQUIRED_KEYS if key not in payload]
        active_empty = [
            key
            for key in ERROR_MEMORY_ACTIVE_NONEMPTY_KEYS
            if _error_memory_value_missing(payload.get(key))
        ]
        failures = active_missing + [key + " is empty" for key in active_empty]
        if failures:
            _raise(
                "Active Error Memory lesson block is not active-ready in "
                + member_name
                + ": "
                + ", ".join(failures)
            )


def _validate_error_memory_lesson_blocks(archive: zipfile.ZipFile, *, intake_mode: bool = False) -> list[str]:
    """Validate every packaged KANDA_ERROR_LESSON_JSON block inside a patch ZIP."""
    checked: list[str] = []
    for info in archive.infolist():
        if info.is_dir():
            continue
        member_name = info.filename.replace("\\", "/")
        if not _is_error_memory_lesson_member(member_name):
            continue
        if info.file_size > ERROR_MEMORY_MEMBER_MAX_BYTES:
            _raise("Error Memory lesson block is too large: " + member_name)
        raw_text = archive.read(info).decode("utf-8-sig", errors="replace")
        json_text = _lesson_block_json_text(raw_text, member_name)
        try:
            loaded = json.loads(json_text)
        except json.JSONDecodeError as exc:
            _raise("Error Memory lesson block is not valid JSON in " + member_name + ": " + str(exc))
        if not isinstance(loaded, Mapping):
            _raise("Error Memory lesson block must contain one JSON object in " + member_name)
        if intake_mode:
            failures = pending_intake_payload_failures(loaded)
            if failures:
                _raise("Pending Error Memory intake lesson invalid in " + member_name + ": " + "; ".join(failures))
        else:
            _validate_error_memory_lesson_payload(loaded, member_name)
        checked.append(member_name)
    return checked


def validate_patch_zip(zip_path: str | Path, *, expect_freeze_hint: bool = True, error_memory_intake: bool = False) -> dict[str, Any]:
    """Validate structural release contract for a patch ZIP.

    The validator fails closed when a freeze-ready ZIP lacks root-level
    KANDA_FREEZE_HINT.json, when mandatory hint fields are empty, or when the
    sidecar is duplicated inside the payload folder where it could be installed
    as source.
    """
    path = Path(zip_path).expanduser().resolve()
    if not path.is_file():
        _raise(f"Patch ZIP not found: {path}")
    if path.suffix.lower() != ".zip":
        _raise(f"Patch file is not a .zip archive: {path}")

    try:
        with zipfile.ZipFile(path, "r") as archive:
            try:
                member_inventory = validate_zip_member_contract(archive)
            except ZipMemberContractError as exc:
                _raise(str(exc))
            names = list(member_inventory.names)
            root_names = {name for name in names if "/" not in name.strip("/")}
            if expect_freeze_hint and FREEZE_HINT_FILENAME not in root_names:
                _raise(f"Missing root-level {FREEZE_HINT_FILENAME}.")
            for root in _payload_roots(names):
                if f"{root}/{FREEZE_HINT_FILENAME}" in names:
                    _raise(
                        f"{FREEZE_HINT_FILENAME} must not be duplicated inside payload folder: {root}/"
                    )
            hint: dict[str, Any] | None = None
            if FREEZE_HINT_FILENAME in root_names:
                raw = archive.read(FREEZE_HINT_FILENAME).decode("utf-8-sig", errors="replace")
                try:
                    loaded = json.loads(raw)
                except json.JSONDecodeError as exc:
                    _raise(f"KANDA_FREEZE_HINT.json is not valid JSON: {exc}")
                if not isinstance(loaded, dict):
                    _raise("KANDA_FREEZE_HINT.json must contain a JSON object.")
                _validate_hint_data(loaded)
                hint = dict(loaded)
            error_memory_lesson_blocks = _validate_error_memory_lesson_blocks(archive, intake_mode=error_memory_intake)
            provenance_required = bool(hint and hint.get("patch_provenance_required"))
            try:
                provenance_report = validate_delivery_provenance_contract(
                    archive,
                    actual_zip_name=path.name,
                    freeze_hint=hint,
                    required=provenance_required,
                )
            except DeliveryProvenanceContractError as exc:
                _raise(str(exc))
    except zipfile.BadZipFile as exc:
        raise PatchZipContractError(f"Invalid ZIP archive: {path}") from exc

    return {
        "ok": True,
        "zip_path": str(path),
        "zip_name": path.name,
        "root_freeze_hint": bool(hint),
        "feature_id": hint.get("feature_id") if hint else "",
        "feature_title": hint.get("feature_title") if hint else "",
        "error_memory_lesson_blocks_checked": len(error_memory_lesson_blocks),
        "error_memory_intake_mode": bool(error_memory_intake),
        "zip_member_contract": True,
        "zip_member_count": len(member_inventory.names),
        "declared_payload_member_count": len(member_inventory.declared_payload_members),
        "patch_provenance_contract": bool(provenance_report),
        "receiver_classification": (
            provenance_report.receiver_classification if provenance_report else ""
        ),
    }


def validate_install_script_text(script_text: str) -> dict[str, Any]:
    """Validate the canonical installer does not drift into generic paths."""
    lowered = script_text.lower()
    forbidden = [item for item in FORBIDDEN_INSTALL_FRAGMENTS if item in lowered]
    if forbidden:
        _raise("Installer contains forbidden generic path fragments: " + ", ".join(forbidden))
    terminal_forbidden = [item for item in FORBIDDEN_TERMINAL_FRAGMENTS if item in lowered]
    if terminal_forbidden:
        _raise("Installer contains forbidden terminal cleanup fragments: " + ", ".join(terminal_forbidden))
    missing = [item for item in REQUIRED_INSTALL_FRAGMENTS if item not in lowered]
    if missing:
        _raise("Installer is missing required staging fragments: " + ", ".join(missing))
    if "move-item" not in lowered and "copy-item" not in lowered:
        _raise("Installer must stage the root-drive ZIP into the work folder.")
    if "remove-item" not in lowered:
        _raise("Installer must remove stale extraction or root-drive ZIP copies.")
    return {"ok": True, "forbidden_fragments": [], "missing_fragments": []}


def main(argv: list[str] | None = None) -> int:
    """CLI entry point for local release validation."""
    parser = argparse.ArgumentParser(description="Validate a KANDA patch ZIP contract.")
    parser.add_argument("zip_path", help="Path to the patch ZIP to validate.")
    parser.add_argument(
        "--non-freezeable",
        action="store_true",
        help="Allow a ZIP without KANDA_FREEZE_HINT.json when explicitly non-freezeable.",
    )
    parser.add_argument("--error-memory-intake", action="store_true")
    args = parser.parse_args(argv)

    try:
        report = validate_patch_zip(
            args.zip_path,
            expect_freeze_hint=not (args.non_freezeable or args.error_memory_intake),
            error_memory_intake=args.error_memory_intake,
        )
    except PatchZipContractError as exc:
        print(f"ZIP CONTRACT: FAIL - {exc}")
        return 1

    print("ZIP CONTRACT: PASS")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
