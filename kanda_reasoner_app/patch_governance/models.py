# project-path: kanda_reasoner_app/patch_governance/models.py
"""Canonical freeze payload model for patch delivery.

The same payload dictionary is used for both the root-level
KANDA_FREEZE_HINT.json sidecar and the user-facing freeze-form JSON. This keeps
patch metadata from drifting into placeholder or stale feature data.
"""

from __future__ import annotations


__all__ = [
    'build_freeze_payload',
    'dump_freeze_payload_json',
    'freeze_form_json_text',
    'FreezePayload',
    'FreezePayloadError',
    'mandatory_freeze_fields',
    'build_bound_freeze_payload',
    'derive_freeze_ownership_binding',
    'validate_freeze_ownership_binding',
]
from dataclasses import dataclass
import json
from typing import Any, Iterable, Mapping

from .freeze_ownership_binding import (
    FREEZE_HINT_SCHEMA_WITH_BINDING,
    FreezeOwnershipBindingError,
    derive_freeze_ownership_binding,
    validate_freeze_ownership_binding,
)

FREEZE_HINT_FILENAME = "KANDA_FREEZE_HINT.json"
SCHEMA_VERSION = "1.0"
KIND = "kanda_freeze_hint"

MANDATORY_FREEZE_FIELDS = (
    "schema_version",
    "kind",
    "patch_name",
    "feature_id",
    "feature_title",
    "primary_box",
    "box_type",
    "validated_files",
    "generated_files",
    "protected_paths",
    "do_not_regress_rules",
    "validation_evidence_summary",
    "known_warnings",
    "planned_next_step",
    "notes",
)

FREEZE_FORM_FIELDS = (
    "feature_title",
    "primary_box",
    "box_type",
    "validated_files",
    "generated_files",
    "protected_paths",
    "do_not_regress_rules",
    "validation_evidence_summary",
    "known_warnings",
    "planned_next_step",
    "notes",
)

PLACEHOLDER_FRAGMENTS = (
    "replace with",
    "placeholder",
    "current validated feature",
    "starter draft",
    "tbd",
    "todo",
)


class FreezePayloadError(ValueError):
    """Raised when a freeze payload cannot be serialized safely."""


@dataclass(frozen=True)
class FreezePayload:
    """Validated metadata for one freeze-capable patch delivery."""

    data: Mapping[str, Any]

    def as_dict(self) -> dict[str, Any]:
        """Return a plain dict copy of the payload."""
        return dict(self.data)

    def as_freeze_form_dict(self) -> dict[str, Any]:
        """Return the form subset derived from the same canonical payload."""
        return {key: self.data[key] for key in FREEZE_FORM_FIELDS}


def mandatory_freeze_fields() -> tuple[str, ...]:
    """Return mandatory root sidecar fields in stable order."""
    return MANDATORY_FREEZE_FIELDS


def _as_list(value: Iterable[str] | str | None, *, field_name: str) -> list[str]:
    """Support as list behavior.
    
    Parameters
    ----------
    value : Iterable[str] | str | None
        The input value.
    field_name : str
        The field name value.
    
    Returns
    -------
    list[str]
        The list of values.
    """
    
    if value is None:
        return []
    if isinstance(value, str):
        value = [value]
    result: list[str] = []
    for item in value:
        text = str(item).strip()
        if text:
            result.append(text.replace("\\", "/"))
    return result


def _as_text(value: str | Iterable[str] | None, *, field_name: str) -> str:
    """Support as text behavior.
    
    Parameters
    ----------
    value : str | Iterable[str] | None
        The input value.
    field_name : str
        The field name value.
    
    Returns
    -------
    str
        The string result.
    """
    
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    lines = [str(item).strip() for item in value if str(item).strip()]
    return "\n".join(lines).strip()


def _contains_placeholder(value: Any) -> bool:
    """Support contains placeholder behavior.
    
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


def _require_non_placeholder(payload: Mapping[str, Any], field_name: str) -> None:
    """Support require non placeholder behavior.
    
    Parameters
    ----------
    payload : Mapping[str, Any]
        The payload value.
    field_name : str
        The field name value.
    """
    
    value = payload.get(field_name)
    if value in (None, "", [], {}):
        raise FreezePayloadError(f"Mandatory field is empty: {field_name}")
    if _contains_placeholder(value):
        raise FreezePayloadError(f"Placeholder text is not allowed in: {field_name}")


def build_freeze_payload(
    *,
    patch_name: str,
    feature_id: str,
    feature_title: str,
    primary_box: str,
    box_type: str,
    validated_files: Iterable[str] | str,
    generated_files: Iterable[str] | str | None,
    protected_paths: Iterable[str] | str,
    do_not_regress_rules: Iterable[str] | str,
    validation_evidence_summary: str | Iterable[str],
    known_warnings: str | Iterable[str],
    planned_next_step: str,
    notes: str | Iterable[str],
    freeze_readiness: str = "pre_validation_hint",
    requires_user_validation: bool = True,
    source_patch_zip: str | None = None,
    patch_provenance_required: bool = False,
    delivery_manifest_name: str = "KANDA_PATCH_DELIVERY_MANIFEST.json",
    patch_trace_name: str = "KANDA_PATCH_TRACE.json",
    schema_version: str = SCHEMA_VERSION,
    kind: str = KIND,
) -> dict[str, Any]:
    """Build and validate the single source freeze payload.

    Use this function for both the root-level KANDA_FREEZE_HINT.json and the
    canonical raw 11-field freeze-form JSON shown to the user. The function refuses
    missing mandatory fields and obvious placeholder strings.
    """
    payload: dict[str, Any] = {
        "schema_version": schema_version.strip(),
        "kind": kind.strip(),
        "patch_name": patch_name.strip(),
        "feature_id": feature_id.strip(),
        "feature_title": feature_title.strip(),
        "primary_box": primary_box.strip().replace("\\", "/"),
        "box_type": box_type.strip(),
        "validated_files": _as_list(validated_files, field_name="validated_files"),
        "generated_files": _as_list(generated_files, field_name="generated_files"),
        "protected_paths": _as_list(protected_paths, field_name="protected_paths"),
        "do_not_regress_rules": _as_list(do_not_regress_rules, field_name="do_not_regress_rules"),
        "validation_evidence_summary": _as_text(
            validation_evidence_summary,
            field_name="validation_evidence_summary",
        ),
        "known_warnings": _as_text(known_warnings, field_name="known_warnings"),
        "planned_next_step": planned_next_step.strip(),
        "notes": _as_text(notes, field_name="notes"),
        "freeze_readiness": freeze_readiness.strip(),
        "requires_user_validation": bool(requires_user_validation),
    }
    if source_patch_zip:
        payload["source_patch_zip"] = source_patch_zip.strip()
    if patch_provenance_required:
        payload["patch_provenance_required"] = True
        payload["delivery_manifest_name"] = delivery_manifest_name.strip()
        payload["patch_trace_name"] = patch_trace_name.strip()
        if not payload["delivery_manifest_name"] or not payload["patch_trace_name"]:
            raise FreezePayloadError("Patch provenance filenames must be non-empty.")

    for field_name in MANDATORY_FREEZE_FIELDS:
        _require_non_placeholder(payload, field_name)

    if not payload["validated_files"]:
        raise FreezePayloadError("validated_files must contain at least one file.")
    if not payload["protected_paths"]:
        raise FreezePayloadError("protected_paths must contain at least one path.")
    if not payload["do_not_regress_rules"]:
        raise FreezePayloadError("do_not_regress_rules must contain at least one rule.")

    return payload


def build_bound_freeze_payload(
    *,
    patch_name: str,
    feature_id: str,
    feature_title: str,
    validated_files: Iterable[str] | str,
    generated_files: Iterable[str] | str | None,
    protected_paths: Iterable[str] | str,
    do_not_regress_rules: Iterable[str] | str,
    validation_evidence_summary: str | Iterable[str],
    known_warnings: str | Iterable[str],
    planned_next_step: str,
    notes: str | Iterable[str],
    freeze_readiness: str = "pre_validation_hint",
    requires_user_validation: bool = True,
    source_patch_zip: str | None = None,
    patch_provenance_required: bool = False,
    delivery_manifest_name: str = "KANDA_PATCH_DELIVERY_MANIFEST.json",
    patch_trace_name: str = "KANDA_PATCH_TRACE.json",
) -> dict[str, Any]:
    """Build a schema-v1.1 Freeze payload with machine-derived ownership.

    This is the canonical builder for new KANDA Tool patch releases. The legacy
    build_freeze_payload API remains available for historical compatibility.
    """

    normalized_validated_files = _as_list(
        validated_files,
        field_name="validated_files",
    )
    try:
        binding = derive_freeze_ownership_binding(normalized_validated_files)
    except FreezeOwnershipBindingError as exc:
        raise FreezePayloadError(str(exc)) from exc

    payload = build_freeze_payload(
        patch_name=patch_name,
        feature_id=feature_id,
        feature_title=feature_title,
        primary_box=str(binding["primary_box"]),
        box_type=str(binding["box_type"]),
        validated_files=normalized_validated_files,
        generated_files=generated_files,
        protected_paths=protected_paths,
        do_not_regress_rules=do_not_regress_rules,
        validation_evidence_summary=validation_evidence_summary,
        known_warnings=known_warnings,
        planned_next_step=planned_next_step,
        notes=notes,
        freeze_readiness=freeze_readiness,
        requires_user_validation=requires_user_validation,
        source_patch_zip=source_patch_zip,
        patch_provenance_required=patch_provenance_required,
        delivery_manifest_name=delivery_manifest_name,
        patch_trace_name=patch_trace_name,
        schema_version=FREEZE_HINT_SCHEMA_WITH_BINDING,
    )
    payload["ownership_binding"] = binding
    try:
        validate_freeze_ownership_binding(payload)
    except FreezeOwnershipBindingError as exc:
        raise FreezePayloadError(str(exc)) from exc
    return payload


def dump_freeze_payload_json(payload: Mapping[str, Any], *, indent: int | None = 2) -> str:
    """Serialize a freeze payload as stable UTF-8 JSON text."""
    for field_name in MANDATORY_FREEZE_FIELDS:
        if field_name not in payload:
            raise FreezePayloadError(f"Mandatory field is missing: {field_name}")
        _require_non_placeholder(payload, field_name)
    try:
        validate_freeze_ownership_binding(payload)
    except FreezeOwnershipBindingError as exc:
        raise FreezePayloadError(str(exc)) from exc
    return json.dumps(dict(payload), ensure_ascii=False, indent=indent) + "\n"


def freeze_form_json_text(payload: Mapping[str, Any]) -> str:
    """Return canonical raw 11-field Freeze-form JSON from the same payload."""
    form = {key: payload[key] for key in FREEZE_FORM_FIELDS}
    return json.dumps(form, ensure_ascii=False, indent=2) + "\n"
