"""Offline Adviser contract validator.

This module validates JSON-like dictionaries against the Adviser v0 candidate
answer contract created by the schema-family design milestone. It is deliberately
small, deterministic, and standard-library-only.

Authority boundary:
- It does not route.
- It does not load prompts.
- It does not call providers, networks, vector stores, or embeddings.
- It does not write files.
- It does not import runtime router modules.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any, Mapping

FEATURE_ID = "routing_signal_scorer_v3_adviser_contract_validator_output_guard_v1"
SCHEMA_VERSION = "3.42-adviser-contract-validator-output-guard"
CONTRACT_SCHEMA_VERSION = "3.41-adviser-schema-family-design"
AUTHORITY_STATEMENT = "advisory_only"
MAX_RATIONALE_SHORT_CHARS = 500

CONTRACTS_DIR = Path(__file__).resolve().parents[1] / "contracts"
CANDIDATE_SCHEMA_FILE = "adviser_candidate_answer_schema.json"

UNAUTHORIZED_ACTION_FIELDS = frozenset(
    {
        "final_route",
        "route_override",
        "router_authority",
        "may_proceed_now",
        "may_proceed_now_decision",
        "load_prompt",
        "prompt_to_load",
        "auto_load_prompt",
        "write_memory",
        "freeze_write",
        "confirm_and_write",
        "artifact_path",
        "generated_artifact",
        "provider_call",
        "embedding_request",
        "vector_index_write",
        "source_scan_request",
        "runtime_integration",
    }
)


@dataclass(frozen=True)
class ContractValidationResult:
    """Structured result for candidate-answer contract validation."""

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


def load_contract_schema(schema_file: str = CANDIDATE_SCHEMA_FILE) -> dict[str, Any]:
    """Load an Adviser JSON contract schema artifact.

    Only local contracts under adviser_offline/contracts are read. This function
    does not scan source trees or runtime project state.
    """

    if Path(schema_file).name != schema_file:
        raise ValueError("schema_file must be a simple filename inside contracts")
    path = CONTRACTS_DIR / schema_file
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema_version") != CONTRACT_SCHEMA_VERSION:
        raise ValueError("unexpected Adviser contract schema version")
    return data


def validate_candidate_answer(answer: Mapping[str, Any] | object) -> dict[str, object]:
    """Validate an Adviser candidate answer dictionary.

    Returns a serializable result. It never raises for ordinary validation
    failures; use assert_candidate_answer_valid when exceptions are preferred.
    """

    errors: list[str] = []
    warnings: list[str] = []

    if not isinstance(answer, Mapping):
        return ContractValidationResult(
            ok=False,
            errors=("candidate answer must be a mapping",),
            warnings=(),
        ).to_dict()

    schema = load_contract_schema()
    required = tuple(str(item) for item in schema.get("required_fields", []))
    enums = schema.get("enums", {})
    explicitly_forbidden = schema.get("explicitly_forbidden_values", {})

    for field in required:
        if field not in answer:
            errors.append(f"missing required field: {field}")

    unexpected_action_fields = sorted(UNAUTHORIZED_ACTION_FIELDS.intersection(answer.keys()))
    for field in unexpected_action_fields:
        errors.append(f"unauthorized action field present: {field}")

    _validate_enum(answer, "governance_domain", enums, errors)
    _validate_enum(answer, "path_recommendation", enums, errors)
    _validate_enum(answer, "advisory_proceed_recommendation", enums, errors)
    _validate_enum(answer, "requires_human_confirmation", enums, errors)
    _validate_enum(answer, "authority_statement", enums, errors)

    proceed = str(answer.get("advisory_proceed_recommendation", ""))
    forbidden_proceed = {str(item) for item in explicitly_forbidden.get("advisory_proceed_recommendation", [])}
    if proceed in forbidden_proceed:
        errors.append(f"forbidden advisory proceed recommendation: {proceed}")

    authority = str(answer.get("authority_statement", ""))
    if authority != AUTHORITY_STATEMENT:
        errors.append("authority_statement must be advisory_only")

    _validate_list_field(answer, "required_prompt_groups", errors)
    _validate_list_field(answer, "required_specialist_prompts", errors)
    _validate_list_field(answer, "recommended_prompt_groups", errors)
    _validate_list_field(answer, "recommended_specialist_prompts", errors)
    _validate_context_requirements(answer.get("context_requirements"), errors)
    _validate_risk_assessment(answer.get("risk_assessment"), errors)
    _validate_governance_flags(answer.get("governance_flags"), errors)
    _validate_rationale(answer.get("rationale"), errors, warnings)

    return ContractValidationResult(ok=not errors, errors=tuple(errors), warnings=tuple(warnings)).to_dict()


def assert_candidate_answer_valid(answer: Mapping[str, Any]) -> Mapping[str, Any]:
    """Raise ValueError if a candidate answer violates the contract."""

    result = validate_candidate_answer(answer)
    if not result["ok"]:
        raise ValueError("; ".join(str(item) for item in result["errors"]))
    return answer


def _validate_enum(answer: Mapping[str, Any], field: str, enums: Mapping[str, object], errors: list[str]) -> None:
    if field not in answer:
        return
    allowed_obj = enums.get(field)
    if not isinstance(allowed_obj, list):
        return
    allowed = {str(item) for item in allowed_obj}
    value = str(answer.get(field))
    if value not in allowed:
        errors.append(f"invalid enum for {field}: {value}")


def _validate_list_field(answer: Mapping[str, Any], field: str, errors: list[str]) -> None:
    if field not in answer:
        return
    value = answer.get(field)
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        errors.append(f"{field} must be a list of strings")


def _validate_context_requirements(value: object, errors: list[str]) -> None:
    required_keys = ("required", "recommended", "optional", "missing_required", "missing_recommended")
    if not isinstance(value, Mapping):
        errors.append("context_requirements must be a mapping")
        return
    for key in required_keys:
        if key not in value:
            errors.append(f"context_requirements missing key: {key}")
        elif not isinstance(value.get(key), list):
            errors.append(f"context_requirements.{key} must be a list")


def _validate_risk_assessment(value: object, errors: list[str]) -> None:
    if not isinstance(value, Mapping):
        errors.append("risk_assessment must be a mapping")
        return
    if value.get("severity") not in {"none", "low", "medium", "high", "critical"}:
        errors.append("risk_assessment.severity must be none|low|medium|high|critical")
    for key in ("flags", "critical_risks"):
        if not isinstance(value.get(key), list):
            errors.append(f"risk_assessment.{key} must be a list")


def _validate_governance_flags(value: object, errors: list[str]) -> None:
    required_keys = ("freeze", "box", "startup", "prompt_library", "patch_delivery", "authority", "adversarial")
    if not isinstance(value, Mapping):
        errors.append("governance_flags must be a mapping")
        return
    for key in required_keys:
        if key not in value:
            errors.append(f"governance_flags missing key: {key}")
        elif not isinstance(value.get(key), list):
            errors.append(f"governance_flags.{key} must be a list")


def _validate_rationale(value: object, errors: list[str], warnings: list[str]) -> None:
    if not isinstance(value, Mapping):
        errors.append("rationale must be a mapping")
        return
    short = value.get("short")
    if not isinstance(short, str):
        errors.append("rationale.short must be a string")
        return
    if len(short) > MAX_RATIONALE_SHORT_CHARS:
        errors.append("rationale.short exceeds bounded length")
    lowered = short.lower()
    if any(phrase in lowered for phrase in ("load prompt now", "write freeze", "final route", "you may proceed")):
        warnings.append("rationale contains action-like wording and should be reviewed")
    if "evidence" in value and not isinstance(value.get("evidence"), list):
        errors.append("rationale.evidence must be a list when present")
