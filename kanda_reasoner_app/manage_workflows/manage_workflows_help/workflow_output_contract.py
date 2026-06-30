# project-path: kanda_reasoner_app/manage_workflows/manage_workflows_help/workflow_output_contract.py
"""Own private workflow command output contract helpers."""

from __future__ import annotations

import re
from typing import Any

__all__ = [
    "validate_command_output_content",
]

DEFAULT_FORBIDDEN_OUTPUT_REGEX = [
    r"(?im)^\s*traceback \(most recent call last\):",
    r"(?im)^\s*(?:fatal|critical)\b",
    r"(?im)^\s*(?:error|failed)\b",
    r"(?im)\b(?:ModuleNotFoundError|ImportError|SyntaxError|NameError|TypeError|ValueError|RuntimeError|AssertionError)\b",
    r"(?im)\bFAILED\b",
]


def bool_from_spec(value: Any) -> bool:
    """Return a conservative boolean value for command spec flags."""
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "y", "on"}
    return bool(value)


def expected_output_stream_from_spec(spec: dict[str, Any]) -> str:
    """Return the output stream expected to contain useful text."""
    stream = str(
        spec.get("expected_output_stream")
        or spec.get("expect_output_stream")
        or spec.get("require_output_stream")
        or "any"
    ).strip().lower()
    if stream not in {"any", "stdout", "stderr", "both"}:
        raise ValueError(
            "expected_output_stream must be one of: any, stdout, stderr, both."
        )
    return stream


def command_expects_output(spec: Any) -> tuple[bool, str]:
    """Return whether a command spec requires useful output."""
    if not isinstance(spec, dict):
        return False, "any"
    expects_output = bool_from_spec(
        spec.get("expect_output")
        or spec.get("require_output")
        or spec.get("expect_nonempty_output")
    )
    return expects_output, expected_output_stream_from_spec(spec)


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


def default_forbidden_output_regex_from_spec(spec: Any) -> list[str]:
    """Return default hidden-error regex patterns for command output."""
    if not isinstance(spec, dict):
        return list(DEFAULT_FORBIDDEN_OUTPUT_REGEX)

    if bool_from_spec(spec.get("allow_error_output")):
        return []
    if bool_from_spec(spec.get("allow_forbidden_output")):
        return []

    if "forbid_default_error_output" in spec:
        if not bool_from_spec(spec.get("forbid_default_error_output")):
            return []
    if "forbid_error_output" in spec:
        if not bool_from_spec(spec.get("forbid_error_output")):
            return []

    return list(DEFAULT_FORBIDDEN_OUTPUT_REGEX)


def output_contract_from_spec(spec: Any) -> dict[str, list[str]]:
    """Return opt-in output content requirements from a command spec."""
    default_forbidden_regex = default_forbidden_output_regex_from_spec(spec)
    if not isinstance(spec, dict):
        return {
            "any_contains": [],
            "stdout_contains": [],
            "stderr_contains": [],
            "any_regex": [],
            "stdout_regex": [],
            "stderr_regex": [],
            "forbidden_any_contains": [],
            "forbidden_stdout_contains": [],
            "forbidden_stderr_contains": [],
            "forbidden_any_regex": default_forbidden_regex,
            "forbidden_stdout_regex": [],
            "forbidden_stderr_regex": [],
        }
    return {
        "any_contains": string_list_from_spec(spec.get("expected_output_contains")),
        "stdout_contains": string_list_from_spec(spec.get("expected_stdout_contains")),
        "stderr_contains": string_list_from_spec(spec.get("expected_stderr_contains")),
        "any_regex": string_list_from_spec(spec.get("expected_output_regex")),
        "stdout_regex": string_list_from_spec(spec.get("expected_stdout_regex")),
        "stderr_regex": string_list_from_spec(spec.get("expected_stderr_regex")),
        "forbidden_any_contains": string_list_from_spec(
            spec.get("forbidden_output_contains")
        ),
        "forbidden_stdout_contains": string_list_from_spec(
            spec.get("forbidden_stdout_contains")
        ),
        "forbidden_stderr_contains": string_list_from_spec(
            spec.get("forbidden_stderr_contains")
        ),
        "forbidden_any_regex": default_forbidden_regex
        + string_list_from_spec(spec.get("forbidden_output_regex")),
        "forbidden_stdout_regex": string_list_from_spec(
            spec.get("forbidden_stdout_regex")
        ),
        "forbidden_stderr_regex": string_list_from_spec(
            spec.get("forbidden_stderr_regex")
        ),
    }


def normalize_output_contract(contract: dict[str, list[str]] | None) -> dict[str, list[str]]:
    """Return a complete output contract with all expected keys present."""
    defaults = output_contract_from_spec(None)
    if not isinstance(contract, dict):
        return defaults
    normalized: dict[str, list[str]] = {}
    for key, default_value in defaults.items():
        normalized[key] = string_list_from_spec(contract.get(key, default_value))
    return normalized


def has_informative_text(value: Any) -> bool:
    """Return True when captured process output contains non-whitespace text."""
    return bool(str(value or "").strip())


def output_requirement_is_met(
    *,
    stdout: str,
    stderr: str,
    expected_stream: str,
) -> bool:
    """Return True when the configured output requirement is satisfied."""
    has_stdout = has_informative_text(stdout)
    has_stderr = has_informative_text(stderr)
    if expected_stream == "stdout":
        return has_stdout
    if expected_stream == "stderr":
        return has_stderr
    if expected_stream == "both":
        return has_stdout and has_stderr
    return has_stdout or has_stderr


def missing_contains_markers(text: str, markers: list[str]) -> list[str]:
    """Return literal markers not found in the supplied text."""
    return [marker for marker in markers if marker not in text]


def matched_contains_markers(text: str, markers: list[str]) -> list[str]:
    """Return literal forbidden markers found in the supplied text."""
    return [marker for marker in markers if marker in text]


def missing_regex_markers(text: str, patterns: list[str]) -> list[str]:
    """Return regex patterns not found in the supplied text."""
    missing = []
    for pattern in patterns:
        try:
            matched = re.search(pattern, text, flags=re.MULTILINE) is not None
        except re.error:
            matched = False
        if not matched:
            missing.append(pattern)
    return missing


def matched_regex_markers(text: str, patterns: list[str]) -> list[str]:
    """Return forbidden regex patterns found in the supplied text."""
    matched_patterns = []
    for pattern in patterns:
        try:
            matched = re.search(pattern, text, flags=re.MULTILINE) is not None
        except re.error:
            matched = True
        if matched:
            matched_patterns.append(pattern)
    return matched_patterns


def forbidden_output_contract_violations(
    *,
    stdout: str,
    stderr: str,
    contract: dict[str, list[str]],
) -> dict[str, list[str]]:
    """Return forbidden output markers found in captured process output."""
    combined = stdout + "\n" + stderr
    violations: dict[str, list[str]] = {
        "forbidden_output_contains": matched_contains_markers(
            combined,
            contract["forbidden_any_contains"],
        ),
        "forbidden_stdout_contains": matched_contains_markers(
            stdout,
            contract["forbidden_stdout_contains"],
        ),
        "forbidden_stderr_contains": matched_contains_markers(
            stderr,
            contract["forbidden_stderr_contains"],
        ),
        "forbidden_output_regex": matched_regex_markers(
            combined,
            contract["forbidden_any_regex"],
        ),
        "forbidden_stdout_regex": matched_regex_markers(
            stdout,
            contract["forbidden_stdout_regex"],
        ),
        "forbidden_stderr_regex": matched_regex_markers(
            stderr,
            contract["forbidden_stderr_regex"],
        ),
    }
    return {key: value for key, value in violations.items() if value}


def missing_expected_output_contract(
    *,
    stdout: str,
    stderr: str,
    contract: dict[str, list[str]],
) -> dict[str, list[str]]:
    """Return expected output markers missing from captured process output."""
    combined = stdout + "\n" + stderr
    missing: dict[str, list[str]] = {
        "expected_output_contains": missing_contains_markers(
            combined,
            contract["any_contains"],
        ),
        "expected_stdout_contains": missing_contains_markers(
            stdout,
            contract["stdout_contains"],
        ),
        "expected_stderr_contains": missing_contains_markers(
            stderr,
            contract["stderr_contains"],
        ),
        "expected_output_regex": missing_regex_markers(
            combined,
            contract["any_regex"],
        ),
        "expected_stdout_regex": missing_regex_markers(
            stdout,
            contract["stdout_regex"],
        ),
        "expected_stderr_regex": missing_regex_markers(
            stderr,
            contract["stderr_regex"],
        ),
    }
    return {key: value for key, value in missing.items() if value}


def output_contract_failure_message(
    *,
    stdout: str,
    stderr: str,
    contract: dict[str, list[str]],
) -> tuple[str | None, dict[str, list[str]]]:
    """Return a failure message and contract details if output is wrong."""
    normalized_contract = normalize_output_contract(contract)
    violations = forbidden_output_contract_violations(
        stdout=stdout,
        stderr=stderr,
        contract=normalized_contract,
    )
    if violations:
        return "Command output matched forbidden content contract.", violations

    missing = missing_expected_output_contract(
        stdout=stdout,
        stderr=stderr,
        contract=normalized_contract,
    )
    if not missing:
        return None, {}
    return "Command output did not match expected content contract.", missing


def validate_command_output_content(
    *,
    stdout: str,
    stderr: str,
    spec: Any | None = None,
    contract: dict[str, list[str]] | None = None,
) -> tuple[str | None, dict[str, list[str]]]:
    """Validate captured output against a complete or partial output contract."""
    active_contract = contract
    if active_contract is None:
        active_contract = output_contract_from_spec(spec)
    return output_contract_failure_message(
        stdout=stdout,
        stderr=stderr,
        contract=normalize_output_contract(active_contract),
    )
