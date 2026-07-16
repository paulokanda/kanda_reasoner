"""Own workflow command expected-file and public contract adapters."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

__all__ = [
    "validate_expected_json_files",
    "validate_expected_output_files",
]


def bool_from_spec(value: Any) -> bool:
    """Return a conservative boolean value for command spec flags."""
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "y", "on"}
    return bool(value)


def string_list_from_spec(value: Any) -> list[str]:
    """Return a normalized list of non-empty strings from a spec value."""
    if value is None:
        return []
    if isinstance(value, str):
        text = value.strip()
        return [text] if text else []
    if isinstance(value, list):
        items = []
        for item in value:
            text = str(item).strip()
            if text:
                items.append(text)
        return items
    text = str(value).strip()
    return [text] if text else []


def expected_files_from_spec(spec: Any) -> list[str]:
    """Return all expected file/path entries configured for a command spec."""
    if not isinstance(spec, dict):
        return []
    paths: list[str] = []
    paths.extend(string_list_from_spec(spec.get("expected_files")))
    paths.extend(string_list_from_spec(spec.get("expected_paths")))
    paths.extend(string_list_from_spec(spec.get("expected_output_files")))
    paths.extend(expected_json_files_from_spec(spec))
    return sorted(dict.fromkeys(paths))


def expected_json_files_from_spec(spec: Any) -> list[str]:
    """Return all expected JSON file/path entries configured for a command spec."""
    if not isinstance(spec, dict):
        return []
    paths: list[str] = []
    paths.extend(string_list_from_spec(spec.get("expected_json_files")))
    paths.extend(string_list_from_spec(spec.get("expected_json_paths")))
    paths.extend(string_list_from_spec(spec.get("expected_json_output_files")))
    return sorted(dict.fromkeys(paths))


def expected_json_required_keys_from_spec(spec: Any) -> list[str]:
    """Return required top-level JSON keys configured for expected JSON files."""
    if not isinstance(spec, dict):
        return []
    keys: list[str] = []
    keys.extend(string_list_from_spec(spec.get("expected_json_required_keys")))
    keys.extend(string_list_from_spec(spec.get("expected_json_keys")))
    return sorted(dict.fromkeys(keys))


def expected_min_bytes_from_spec(spec: Any) -> int | None:
    """Return the expected minimum file size for expected files."""
    if not isinstance(spec, dict):
        return None
    raw = spec.get("expected_file_min_bytes")
    if raw is not None:
        try:
            minimum = int(raw)
        except (TypeError, ValueError):
            return None
        return max(0, minimum)
    if bool_from_spec(spec.get("expected_file_nonempty")):
        return 1
    return None


def resolve_expected_file(root: Path, raw_path: str) -> Path:
    """Resolve an expected file path against the workflow root."""
    text = raw_path.replace("{root}", str(root))
    path = Path(text)
    if path.is_absolute():
        return path
    return root / path


def validate_expected_file_presence(
    *,
    spec: Any,
    root: Path,
) -> tuple[list[str], list[dict[str, Any]]]:
    """Validate expected file presence and optional minimum size."""
    expected_files = expected_files_from_spec(spec)
    min_bytes = expected_min_bytes_from_spec(spec)
    missing: list[str] = []
    too_small: list[dict[str, Any]] = []

    for raw_path in expected_files:
        path = resolve_expected_file(root, raw_path)
        if not path.exists():
            missing.append(raw_path)
            continue
        if not path.is_file():
            too_small.append(
                {
                    "path": raw_path,
                    "actual_bytes": None,
                    "minimum_bytes": min_bytes,
                    "reason": "path is not a file",
                }
            )
            continue
        if min_bytes is not None:
            try:
                actual_size = path.stat().st_size
            except OSError:
                actual_size = -1
            if actual_size < min_bytes:
                too_small.append(
                    {
                        "path": raw_path,
                        "actual_bytes": actual_size,
                        "minimum_bytes": min_bytes,
                        "reason": "file is smaller than expected",
                    }
                )

    return missing, too_small


def validate_expected_output_files(
    *,
    spec: Any,
    root: Path,
) -> tuple[list[str], list[dict[str, Any]]]:
    """Validate expected output-file paths configured for a workflow command."""
    return validate_expected_file_presence(spec=spec, root=root)


def validate_expected_json_files(
    *,
    spec: Any,
    root: Path,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Validate expected JSON files and required top-level keys."""
    expected_json_files = expected_json_files_from_spec(spec)
    required_keys = expected_json_required_keys_from_spec(spec)
    invalid_json: list[dict[str, Any]] = []
    missing_keys: list[dict[str, Any]] = []

    for raw_path in expected_json_files:
        path = resolve_expected_file(root, raw_path)
        if not path.exists() or not path.is_file():
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8", errors="replace"))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            invalid_json.append(
                {
                    "path": raw_path,
                    "error": type(exc).__name__ + ": " + str(exc),
                }
            )
            continue

        if required_keys:
            if not isinstance(data, dict):
                invalid_json.append(
                    {
                        "path": raw_path,
                        "error": "JSON top level is not an object.",
                    }
                )
                continue
            absent = [key for key in required_keys if key not in data]
            if absent:
                missing_keys.append(
                    {
                        "path": raw_path,
                        "missing_keys": absent,
                    }
                )

    return invalid_json, missing_keys


def validate_command_output_content(
    *,
    stdout: str,
    stderr: str,
    spec: Any | None = None,
    contract: dict[str, list[str]] | None = None,
) -> tuple[str | None, dict[str, list[str]]]:
    """Validate command output against the public output-content contract."""
    from .workflow_output_contract import (
        output_contract_failure_message,
        output_contract_from_spec,
    )

    active_contract = contract
    if active_contract is None:
        active_contract = output_contract_from_spec(spec)
    return output_contract_failure_message(
        stdout=stdout,
        stderr=stderr,
        contract=active_contract,
    )


def detect_workflow_structure_issues(context: Any) -> list[Any]:
    """Delegate workflow-structure issue detection through the public facade."""
    from .workflow_structure_detectors import (
        detect_workflow_structure_issues as _detect_workflow_structure_issues,
    )

    return _detect_workflow_structure_issues(context)


def validate_file_contract(
    *,
    spec: Any,
    root: Path,
) -> tuple[str | None, dict[str, Any]]:
    """Validate expected files after a successful command run."""
    expected_files = expected_files_from_spec(spec)
    expected_json_files = expected_json_files_from_spec(spec)
    if not expected_files and not expected_json_files:
        return None, {}

    missing, too_small = validate_expected_file_presence(spec=spec, root=root)
    invalid_json, missing_json_keys = validate_expected_json_files(spec=spec, root=root)

    details: dict[str, Any] = {}
    if missing:
        details["missing_expected_files"] = missing
    if too_small:
        details["undersized_expected_files"] = too_small
    if invalid_json:
        details["invalid_expected_json_files"] = invalid_json
    if missing_json_keys:
        details["missing_expected_json_keys"] = missing_json_keys

    if details:
        return "Command output file contract was not satisfied.", details
    return None, {}
