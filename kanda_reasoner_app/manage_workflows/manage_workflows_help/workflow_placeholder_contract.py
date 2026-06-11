"""Own private workflow command placeholder contract helpers."""

from __future__ import annotations

import re
from typing import Any

__all__: list[str] = []

_ALLOWED_COMMAND_PLACEHOLDERS = {"python", "root"}
_ALLOWED_PATH_PLACEHOLDERS = {"root"}

_COMMAND_FIELD_NAMES = {"command"}
_ARGS_FIELD_NAMES = {"args"}
_ENV_FIELD_NAMES = {"env", "extra_env"}
_PATH_FIELD_NAMES = {
    "cwd",
    "expected_files",
    "expected_paths",
    "expected_output_files",
    "expected_json_files",
    "expected_json_paths",
    "expected_json_output_files",
}

_PLACEHOLDER_RE = re.compile(r"\{([A-Za-z_][A-Za-z0-9_]*)\}")
_ALLOWED_LEFT_FRAGMENT_RE = re.compile(r"\{(?:python|root)(?![A-Za-z0-9_])")
_ALLOWED_RIGHT_FRAGMENT_RE = re.compile(r"(?<![A-Za-z0-9_])(?:python|root)\}")


def placeholder_command_name(category: str, spec: Any) -> str:
    """Return the command name without building or running the command."""
    if isinstance(spec, dict) and spec.get("name"):
        return str(spec["name"])
    return f"{category} command"


def placeholder_command_preview(spec: Any) -> str:
    """Return a compact raw command preview for placeholder failures."""
    if isinstance(spec, str):
        return spec
    if not isinstance(spec, dict):
        return ""
    if "command" in spec:
        return str(spec.get("command") or "")
    if "args" in spec:
        args = spec.get("args")
        if isinstance(args, list):
            return " ".join(str(item) for item in args)
    return ""


def _string_items_from_value(field: str, value: Any) -> list[tuple[str, str]]:
    """Return inspectable string items from a scalar, list, or mapping value."""
    if value is None:
        return []
    if isinstance(value, str):
        return [(field, value)]
    if isinstance(value, list):
        return [
            (field + "[" + str(index) + "]", str(item))
            for index, item in enumerate(value)
        ]
    if isinstance(value, dict):
        items: list[tuple[str, str]] = []
        for key, item in value.items():
            items.append((field + "." + str(key), str(item)))
        return items
    return [(field, str(value))]


def _iter_placeholder_fields(
    spec: Any,
    extra_env: dict[str, str] | None,
) -> list[tuple[str, str, str]]:
    """Return fields whose placeholders affect workflow command execution."""
    fields: list[tuple[str, str, str]] = []

    if isinstance(spec, str):
        fields.append(("command", "command", spec))
    elif isinstance(spec, dict):
        for field in sorted(_COMMAND_FIELD_NAMES | _ARGS_FIELD_NAMES | _PATH_FIELD_NAMES):
            if field in spec:
                kind = "path" if field in _PATH_FIELD_NAMES else "command"
                for label, value in _string_items_from_value(field, spec.get(field)):
                    fields.append((kind, label, value))

        env_spec = spec.get("env")
        if isinstance(env_spec, dict):
            for label, value in _string_items_from_value("env", env_spec):
                fields.append(("env", label, value))

    if extra_env:
        for label, value in _string_items_from_value("extra_env", extra_env):
            fields.append(("env", label, value))

    return fields


def _allowed_placeholders_for_kind(kind: str) -> set[str]:
    """Return allowed placeholder names for a field kind."""
    if kind == "path":
        return set(_ALLOWED_PATH_PLACEHOLDERS)
    return set(_ALLOWED_COMMAND_PLACEHOLDERS)


def _malformed_placeholder_fragments(value: str) -> list[str]:
    """Return malformed fragments for supported placeholders only.

    Literal braces are common inside inline Python, JSON, regex, and shell
    snippets. Treating any ``{word`` fragment as a placeholder makes Tab 2
    reject valid commands before downstream output/file contracts can run.
    This check is intentionally narrow: it only reports malformed fragments
    that look like the supported workflow placeholders, such as ``{root`` or
    ``python}``. Unsupported complete placeholders, such as ``{project_root}``,
    are still reported by the full-placeholder check.
    """
    masked = _PLACEHOLDER_RE.sub("", value)
    fragments = []
    fragments.extend(_ALLOWED_LEFT_FRAGMENT_RE.findall(masked))
    fragments.extend(_ALLOWED_RIGHT_FRAGMENT_RE.findall(masked))
    return sorted(dict.fromkeys(fragments))


def validate_placeholder_contract(
    *,
    spec: Any,
    extra_env: dict[str, str] | None = None,
) -> dict[str, list[dict[str, str]]]:
    """Return placeholder contract violations for a workflow command spec."""
    unsupported: list[dict[str, str]] = []
    wrong_field: list[dict[str, str]] = []
    malformed: list[dict[str, str]] = []

    for kind, field, value in _iter_placeholder_fields(spec, extra_env):
        allowed = _allowed_placeholders_for_kind(kind)
        for placeholder in _PLACEHOLDER_RE.findall(value):
            payload = {
                "field": field,
                "placeholder": placeholder,
                "value": value,
            }
            if placeholder not in _ALLOWED_COMMAND_PLACEHOLDERS:
                unsupported.append(payload)
            elif placeholder not in allowed:
                wrong_field.append(payload)

        for fragment in _malformed_placeholder_fragments(value):
            malformed.append(
                {
                    "field": field,
                    "fragment": fragment,
                    "value": value,
                }
            )

    details: dict[str, list[dict[str, str]]] = {}
    if unsupported:
        details["unsupported_placeholders"] = unsupported
    if wrong_field:
        details["wrong_field_placeholders"] = wrong_field
    if malformed:
        details["malformed_placeholders"] = malformed
    return details


def placeholder_contract_failure_message(
    *,
    spec: Any,
    extra_env: dict[str, str] | None = None,
) -> tuple[str | None, dict[str, list[dict[str, str]]]]:
    """Return a failure message when a workflow command misuses placeholders."""
    details = validate_placeholder_contract(spec=spec, extra_env=extra_env)
    if details:
        return "Command placeholder contract was not satisfied.", details
    return None, {}
