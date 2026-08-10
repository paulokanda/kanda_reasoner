# project-path: kanda_reasoner_app/python_coding_ai_readiness.py
"""Local readiness checks for the free Python-coding AI catalog.

The checks are deterministic and network-free. They validate the approved
model IDs, manual assistant identities, official HTTPS destinations, and the
age of the last human-reviewed free-access metadata.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Mapping, Sequence

from kanda_reasoner_app.python_coding_ai_catalog import (
    ExternalPythonCodingAssistant,
    approved_direct_model_ids,
    external_python_coding_assistants,
)

__all__ = [
    "PythonCodingAIReadiness",
    "PythonCodingAIReadinessError",
    "evaluate_python_coding_ai_readiness",
]

_REVIEW_AFTER_DAYS = 30
_STALE_AFTER_DAYS = 90
_EXPECTED_GATEWAYS = ("openrouter", "kilo")


class PythonCodingAIReadinessError(ValueError):
    """Raised when the canonical free Python-coding catalog is inconsistent."""


@dataclass(frozen=True, slots=True)
class PythonCodingAIReadiness:
    """Summarize deterministic catalog health and verification age."""

    status: str
    openrouter_model_count: int
    kilo_model_count: int
    external_assistant_count: int
    validated_url_count: int
    oldest_verified_date: str
    verification_age_days: int
    review_after_days: int = _REVIEW_AFTER_DAYS
    stale_after_days: int = _STALE_AFTER_DAYS

    def summary(self) -> str:
        """Return a compact GUI-ready status line."""
        return (
            self.status
            + " | OpenRouter IDs: "
            + str(self.openrouter_model_count)
            + " | Kilo IDs: "
            + str(self.kilo_model_count)
            + " | External assistants: "
            + str(self.external_assistant_count)
            + " | HTTPS URLs: "
            + str(self.validated_url_count)
        )

    def age_summary(self) -> str:
        """Return a human-readable verification-age description."""
        return (
            "Oldest free-access review: "
            + self.oldest_verified_date
            + " ("
            + str(self.verification_age_days)
            + " days old). Review due after "
            + str(self.review_after_days)
            + " days; stale after "
            + str(self.stale_after_days)
            + " days."
        )


def evaluate_python_coding_ai_readiness(
    *,
    today: date | None = None,
    assistants: Sequence[ExternalPythonCodingAssistant] | None = None,
    direct_models: Mapping[str, Sequence[str]] | None = None,
) -> PythonCodingAIReadiness:
    """Validate the local catalog and return its current readiness state."""
    check_date = today or date.today()
    assistant_items = tuple(assistants or external_python_coding_assistants())
    model_map = direct_models or {
        gateway_id: approved_direct_model_ids(gateway_id)
        for gateway_id in _EXPECTED_GATEWAYS
    }

    normalized_models = _validate_direct_models(model_map)
    verification_dates = _validate_assistants(assistant_items)
    oldest_date = min(verification_dates)
    age_days = (check_date - oldest_date).days
    if age_days < 0:
        raise PythonCodingAIReadinessError(
            "Catalog verification date cannot be in the future."
        )
    if age_days <= _REVIEW_AFTER_DAYS:
        status = "CURRENT"
    elif age_days <= _STALE_AFTER_DAYS:
        status = "REVIEW_DUE"
    else:
        status = "STALE"

    return PythonCodingAIReadiness(
        status=status,
        openrouter_model_count=len(normalized_models["openrouter"]),
        kilo_model_count=len(normalized_models["kilo"]),
        external_assistant_count=len(assistant_items),
        validated_url_count=len(assistant_items),
        oldest_verified_date=oldest_date.isoformat(),
        verification_age_days=age_days,
    )


def _validate_direct_models(
    direct_models: Mapping[str, Sequence[str]],
) -> dict[str, tuple[str, ...]]:
    normalized: dict[str, tuple[str, ...]] = {}
    for gateway_id in _EXPECTED_GATEWAYS:
        values = tuple(
            str(value or "").strip()
            for value in direct_models.get(gateway_id, ())
            if str(value or "").strip()
        )
        if not values:
            raise PythonCodingAIReadinessError(
                "Approved direct model set is empty for " + gateway_id + "."
            )
        if len(values) != len(set(values)):
            raise PythonCodingAIReadinessError(
                "Approved direct model IDs contain duplicates for " + gateway_id + "."
            )
        if "openrouter/free" in {value.casefold() for value in values}:
            raise PythonCodingAIReadinessError(
                "The generic OpenRouter free router is not approved."
            )
        if any(not _is_zero_cost_route(value) for value in values):
            raise PythonCodingAIReadinessError(
                "Approved direct model ID is not an explicit free route."
            )
        normalized[gateway_id] = values
    return normalized


def _validate_assistants(
    assistants: Sequence[ExternalPythonCodingAssistant],
) -> tuple[date, ...]:
    if not assistants:
        raise PythonCodingAIReadinessError(
            "External Python-coding assistant catalog is empty."
        )
    assistant_ids: set[str] = set()
    verification_dates: list[date] = []
    for assistant in assistants:
        if assistant.assistant_id in assistant_ids:
            raise PythonCodingAIReadinessError(
                "External assistant IDs contain duplicates."
            )
        assistant_ids.add(assistant.assistant_id)
        assistant.validated_url()
        if "FREE" not in assistant.free_status.upper():
            raise PythonCodingAIReadinessError(
                "External assistant is not marked as a free-access route."
            )
        if "PYTHON" not in assistant.python_coding_summary.upper():
            raise PythonCodingAIReadinessError(
                "External assistant lacks an explicit Python-coding summary."
            )
        try:
            verification_dates.append(date.fromisoformat(assistant.last_verified_date))
        except ValueError as exc:
            raise PythonCodingAIReadinessError(
                "External assistant verification date is invalid."
            ) from exc
    return tuple(verification_dates)


def _is_zero_cost_route(model_id: str) -> bool:
    clean = str(model_id or "").strip().casefold()
    return clean.endswith(":free") or clean == "kilo-auto/free"
