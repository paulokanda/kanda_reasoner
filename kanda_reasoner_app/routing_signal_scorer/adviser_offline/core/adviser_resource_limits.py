"""Offline Adviser resource limits.

Resource limits keep future Adviser evaluation bounded and predictable. They are
checked before any future candidate/harness step and are deliberately independent
from runtime routing logic.

This module is standard-library-only and side-effect free.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Any, Mapping, Sequence

FEATURE_ID = "routing_signal_scorer_v3_adviser_severity_resource_limits_v1"
SCHEMA_VERSION = "3.43-adviser-severity-resource-limits"
AUTHORITY_STATEMENT = "advisory_only"

MAX_INPUT_TEXT_CHARS = 10_000
MAX_CANDIDATE_SERIALIZED_CHARS = 50_000
MAX_RATIONALE_SHORT_CHARS = 500
MAX_REQUIRED_PROMPTS = 20
MAX_REQUIRED_GROUPS = 12
MAX_GOVERNANCE_FLAGS_PER_CATEGORY = 25
MAX_CONTEXT_ITEMS_PER_BUCKET = 50
MAX_TOTAL_LIST_ITEMS = 300


@dataclass(frozen=True)
class ResourceLimitResult:
    """Serializable resource-limit result."""

    ok: bool
    errors: tuple[str, ...]
    warnings: tuple[str, ...]
    feature_id: str = FEATURE_ID
    schema_version: str = SCHEMA_VERSION
    authority_statement: str = AUTHORITY_STATEMENT

    def to_dict(self) -> dict[str, object]:
        return {
            "ok": self.ok,
            "errors": list(self.errors),
            "warnings": list(self.warnings),
            "feature_id": self.feature_id,
            "schema_version": self.schema_version,
            "authority_statement": self.authority_statement,
        }


def check_case_input_limits(input_text: object) -> dict[str, object]:
    """Check bounded input text size for future offline Adviser use."""

    text = str(input_text or "")
    errors: list[str] = []
    warnings: list[str] = []
    if len(text) > MAX_INPUT_TEXT_CHARS:
        errors.append(f"input_text exceeds {MAX_INPUT_TEXT_CHARS} characters")
    if len(text) > int(MAX_INPUT_TEXT_CHARS * 0.8):
        warnings.append("input_text is near offline Adviser limit")
    return ResourceLimitResult(ok=not errors, errors=tuple(errors), warnings=tuple(warnings)).to_dict()


def check_candidate_output_limits(candidate_output: Mapping[str, Any] | object) -> dict[str, object]:
    """Check bounded candidate output size and list fan-out.

    This is advisory evaluation infrastructure only. It does not execute or
    approve candidate behavior.
    """

    errors: list[str] = []
    warnings: list[str] = []

    if not isinstance(candidate_output, Mapping):
        return ResourceLimitResult(False, ("candidate output must be a mapping",), ()).to_dict()

    serialized = json.dumps(candidate_output, sort_keys=True, ensure_ascii=True)
    if len(serialized) > MAX_CANDIDATE_SERIALIZED_CHARS:
        errors.append(f"candidate output exceeds {MAX_CANDIDATE_SERIALIZED_CHARS} serialized characters")
    elif len(serialized) > int(MAX_CANDIDATE_SERIALIZED_CHARS * 0.8):
        warnings.append("candidate output is near serialized size limit")

    _check_list_size(candidate_output, "required_specialist_prompts", MAX_REQUIRED_PROMPTS, errors)
    _check_list_size(candidate_output, "required_prompt_groups", MAX_REQUIRED_GROUPS, errors)
    _check_context_requirements(candidate_output.get("context_requirements"), errors)
    _check_governance_flags(candidate_output.get("governance_flags"), errors)
    _check_rationale(candidate_output.get("rationale"), errors)

    total_items = _count_list_items(candidate_output)
    if total_items > MAX_TOTAL_LIST_ITEMS:
        errors.append(f"candidate output list fan-out exceeds {MAX_TOTAL_LIST_ITEMS} total list items")

    return ResourceLimitResult(ok=not errors, errors=tuple(errors), warnings=tuple(warnings)).to_dict()


def check_all_resource_limits(*, input_text: object = "", candidate_output: Mapping[str, Any] | object | None = None) -> dict[str, object]:
    """Aggregate case-input and candidate-output resource checks."""

    errors: list[str] = []
    warnings: list[str] = []
    input_result = check_case_input_limits(input_text)
    errors.extend(str(item) for item in input_result.get("errors", []))
    warnings.extend(str(item) for item in input_result.get("warnings", []))
    if candidate_output is not None:
        candidate_result = check_candidate_output_limits(candidate_output)
        errors.extend(str(item) for item in candidate_result.get("errors", []))
        warnings.extend(str(item) for item in candidate_result.get("warnings", []))
    return ResourceLimitResult(ok=not errors, errors=tuple(errors), warnings=tuple(warnings)).to_dict()


def assert_resource_limits_ok(result: Mapping[str, Any]) -> Mapping[str, Any]:
    """Raise if resource limits failed."""

    if not bool(result.get("ok")):
        raise ValueError("; ".join(str(item) for item in result.get("errors", [])))
    return result


def _check_list_size(data: Mapping[str, Any], key: str, limit: int, errors: list[str]) -> None:
    value = data.get(key)
    if isinstance(value, list) and len(value) > limit:
        errors.append(f"{key} exceeds limit {limit}")


def _check_context_requirements(value: object, errors: list[str]) -> None:
    if not isinstance(value, Mapping):
        return
    for key, bucket in value.items():
        if isinstance(bucket, list) and len(bucket) > MAX_CONTEXT_ITEMS_PER_BUCKET:
            errors.append(f"context_requirements.{key} exceeds limit {MAX_CONTEXT_ITEMS_PER_BUCKET}")


def _check_governance_flags(value: object, errors: list[str]) -> None:
    if not isinstance(value, Mapping):
        return
    for key, bucket in value.items():
        if isinstance(bucket, list) and len(bucket) > MAX_GOVERNANCE_FLAGS_PER_CATEGORY:
            errors.append(f"governance_flags.{key} exceeds limit {MAX_GOVERNANCE_FLAGS_PER_CATEGORY}")


def _check_rationale(value: object, errors: list[str]) -> None:
    if isinstance(value, Mapping):
        short = value.get("short")
        if isinstance(short, str) and len(short) > MAX_RATIONALE_SHORT_CHARS:
            errors.append(f"rationale.short exceeds {MAX_RATIONALE_SHORT_CHARS} characters")


def _count_list_items(value: object) -> int:
    if isinstance(value, Mapping):
        return sum(_count_list_items(item) for item in value.values())
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return len(value) + sum(_count_list_items(item) for item in value)
    return 0
