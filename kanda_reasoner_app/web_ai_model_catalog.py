# project-path: kanda_reasoner_app/web_ai_model_catalog.py
"""Dynamic and provider-owned model catalog loading for KANDA Web AI."""

from __future__ import annotations

import urllib.request
from datetime import datetime, timezone
from typing import Callable, Mapping

from kanda_reasoner_app.python_coding_ai_catalog import approved_direct_model_ids
from kanda_reasoner_app.web_ai_provider_contracts import (
    GatewayProfile,
    ModelDescriptor,
    ProviderCatalogError,
    ProviderError,
)
from kanda_reasoner_app.web_ai_provider_runtime import request_json_payload

__all__ = ["fetch_gateway_models"]

UrlOpenCallable = Callable[..., object]
MAX_CATALOG_BYTES = 16 * 1024 * 1024


def _utc_now_text() -> str:
    """Return an ISO UTC timestamp without microseconds."""
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _float_or_none(value: object) -> float | None:
    """Return a finite float when possible."""
    try:
        result = float(str(value).strip())
    except (TypeError, ValueError):
        return None
    if result != result or result in (float("inf"), float("-inf")):
        return None
    return result


def _int_or_zero(value: object) -> int:
    """Return a non-negative integer or zero."""
    try:
        return max(0, int(value))
    except (TypeError, ValueError):
        return 0


def _catalog_items(payload: Mapping[str, object]) -> list[Mapping[str, object]]:
    """Return model entries from common OpenAI-compatible catalog shapes."""
    items = payload.get("data", payload.get("models", []))
    if not isinstance(items, list):
        raise ProviderCatalogError("Model catalog did not contain a data list.")
    return [item for item in items if isinstance(item, dict)]


def _supported_parameters(item: Mapping[str, object]) -> tuple[str, ...]:
    """Return normalized supported parameter names."""
    raw = item.get("supported_parameters", ())
    if not isinstance(raw, (list, tuple)):
        return ()
    return tuple(
        sorted({str(value).strip() for value in raw if str(value).strip()})
    )


def _pricing(item: Mapping[str, object]) -> tuple[float | None, float | None]:
    """Return prompt and completion prices from a model item."""
    pricing = item.get("pricing")
    if not isinstance(pricing, dict):
        return None, None
    input_price = _float_or_none(pricing.get("prompt", pricing.get("input")))
    output_price = _float_or_none(
        pricing.get("completion", pricing.get("output"))
    )
    return input_price, output_price


def _supports_streaming(
    item: Mapping[str, object],
    parameters: tuple[str, ...],
) -> bool:
    """Return streaming support from metadata or OpenAI compatibility."""
    for key in ("supports_streaming", "streaming"):
        value = item.get(key)
        if isinstance(value, bool):
            return value
    return "stream" in parameters


def _catalog_zero_price(
    model_id: str,
    input_price: float | None,
    output_price: float | None,
) -> bool:
    """Return whether gateway metadata proves zero price."""
    lower_id = model_id.lower()
    if lower_id.endswith(":free") or lower_id in {
        "openrouter/free",
        "kilo-auto/free",
        "kilo-auto:free",
    }:
        return True
    return input_price == 0.0 and output_price == 0.0


def _free_access(
    profile: GatewayProfile,
    model_id: str,
    input_price: float | None,
    output_price: float | None,
) -> tuple[bool, str]:
    """Return provider-specific free eligibility and a truthful label."""
    if model_id not in set(approved_direct_model_ids(profile.gateway_id)):
        return False, ""
    if profile.free_access_kind == "catalog_zero_price":
        proven = _catalog_zero_price(model_id, input_price, output_price)
        return proven, "free according to current gateway catalog" if proven else ""
    if profile.free_access_kind == "provider_free_tier":
        return True, "requires an unbilled provider Free Tier project"
    if profile.free_access_kind == "account_free_mode":
        return True, "requires provider Free mode confirmation; limits may apply"
    if profile.free_access_kind == "time_limited_free_quota":
        return True, "requires remaining free quota and Free Quota Only"
    if profile.free_access_kind == "account_free_plan":
        return True, "requires the provider Free Plan; rate limits apply"
    return False, ""


def _normalized_model_id(profile: GatewayProfile, value: object) -> str:
    """Normalize provider model IDs without weakening exact allowlists."""
    model_id = str(value or "").strip()
    if profile.gateway_id == "gemini" and model_id.startswith("models/"):
        model_id = model_id.split("/", 1)[1]
    return model_id


def _normalize_model(
    profile: GatewayProfile,
    item: Mapping[str, object],
    timestamp: str,
) -> ModelDescriptor | None:
    """Normalize one remote catalog item."""
    model_id = _normalized_model_id(
        profile,
        item.get("id") or item.get("model") or item.get("name") or "",
    )
    if not model_id:
        return None
    display_name = str(
        item.get("display_name") or item.get("name") or model_id
    ).strip()
    context_window = _int_or_zero(
        item.get(
            "context_length",
            item.get("context_window", item.get("context_length_tokens", 0)),
        )
    )
    input_price, output_price = _pricing(item)
    parameters = _supported_parameters(item)
    free_status, free_label = _free_access(
        profile,
        model_id,
        input_price,
        output_price,
    )
    return ModelDescriptor(
        gateway_id=profile.gateway_id,
        model_id=model_id,
        display_name=display_name,
        context_window=context_window,
        input_price=input_price,
        output_price=output_price,
        supports_streaming=_supports_streaming(item, parameters),
        supports_tools="tools" in parameters or "tool_choice" in parameters,
        free_status=free_status,
        free_access_label=free_label,
        catalog_timestamp=timestamp,
        owned_by=str(item.get("owned_by") or item.get("provider") or "").strip(),
        supported_parameters=parameters,
        raw_metadata=dict(item),
    )


def _static_models(
    profile: GatewayProfile,
    timestamp: str,
) -> list[ModelDescriptor]:
    """Build a reviewed direct-provider catalog when no list endpoint exists."""
    results: list[ModelDescriptor] = []
    for model_id, display_name, context_window in profile.static_models:
        free_status, free_label = _free_access(profile, model_id, None, None)
        results.append(
            ModelDescriptor(
                gateway_id=profile.gateway_id,
                model_id=model_id,
                display_name=display_name,
                context_window=context_window,
                supports_streaming=True,
                supports_tools=False,
                free_status=free_status,
                free_access_label=free_label,
                catalog_timestamp=timestamp,
                owned_by=profile.display_name,
                supported_parameters=("stream",),
                raw_metadata={"catalog_source": "reviewed provider documentation"},
            )
        )
    return results


def fetch_gateway_models(
    profile: GatewayProfile,
    api_key: str = "",
    *,
    timeout_seconds: float = 20.0,
    opener: UrlOpenCallable | None = None,
) -> list[ModelDescriptor]:
    """Fetch or construct the approved catalog for one remote provider."""
    timestamp = _utc_now_text()
    if profile.static_models:
        models = _static_models(profile, timestamp)
    else:
        models_url = profile.models_url()
        if not models_url:
            raise ProviderCatalogError("Provider does not define a model catalog.")
        request = urllib.request.Request(
            models_url,
            headers=profile.headers(api_key),
            method="GET",
        )
        try:
            payload = request_json_payload(
                request,
                timeout_seconds=timeout_seconds,
                opener=opener or urllib.request.urlopen,
                maximum_bytes=MAX_CATALOG_BYTES,
            )
        except ProviderError as exc:
            raise ProviderCatalogError(str(exc)) from exc
        models = [
            normalized
            for item in _catalog_items(payload)
            if (normalized := _normalize_model(profile, item, timestamp))
            is not None
        ]
    if not models:
        raise ProviderCatalogError("Provider returned no usable models.")
    return sorted(
        models,
        key=lambda model: (
            not model.free_status,
            model.display_name.casefold(),
            model.model_id,
        ),
    )
