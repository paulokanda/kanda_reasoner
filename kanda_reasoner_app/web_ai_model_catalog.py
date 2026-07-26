# project-path: kanda_reasoner_app/web_ai_model_catalog.py
"""Dynamic model catalog loading for KANDA web AI gateways.

The catalog layer is separate from chat execution because model metadata has a
different schema, cache lifetime, and failure contract.  It reuses the shared
bounded HTTP reader and performs no Qt or project-context work.
"""

from __future__ import annotations

import urllib.request
from datetime import datetime, timezone
from typing import Callable, Mapping

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
    return tuple(sorted({str(value).strip() for value in raw if str(value).strip()}))


def _pricing(item: Mapping[str, object]) -> tuple[float | None, float | None]:
    """Return prompt and completion prices from a model item."""
    pricing = item.get("pricing")
    if not isinstance(pricing, dict):
        return None, None
    input_price = _float_or_none(pricing.get("prompt", pricing.get("input")))
    output_price = _float_or_none(pricing.get("completion", pricing.get("output")))
    return input_price, output_price


def _supports_streaming(
    item: Mapping[str, object],
    parameters: tuple[str, ...],
) -> bool:
    """Return streaming support only when catalog metadata proves it."""
    for key in ("supports_streaming", "streaming"):
        value = item.get(key)
        if isinstance(value, bool):
            return value
    return "stream" in parameters


def _is_free_model(
    model_id: str,
    input_price: float | None,
    output_price: float | None,
) -> bool:
    """Return whether current metadata describes a zero-cost model."""
    lower_id = model_id.lower()
    if lower_id.endswith(":free") or lower_id in {
        "openrouter/free",
        "kilo-auto:free",
    }:
        return True
    return input_price == 0.0 and output_price == 0.0


def _normalize_model(
    profile: GatewayProfile,
    item: Mapping[str, object],
    timestamp: str,
) -> ModelDescriptor | None:
    """Normalize one remote catalog item."""
    model_id = str(
        item.get("id") or item.get("model") or item.get("name") or ""
    ).strip()
    if not model_id:
        return None
    display_name = str(
        item.get("name") or item.get("display_name") or model_id
    ).strip()
    context_window = _int_or_zero(
        item.get(
            "context_length",
            item.get("context_window", item.get("context_length_tokens", 0)),
        )
    )
    input_price, output_price = _pricing(item)
    parameters = _supported_parameters(item)
    return ModelDescriptor(
        gateway_id=profile.gateway_id,
        model_id=model_id,
        display_name=display_name,
        context_window=context_window,
        input_price=input_price,
        output_price=output_price,
        supports_streaming=_supports_streaming(item, parameters),
        supports_tools="tools" in parameters or "tool_choice" in parameters,
        free_status=_is_free_model(model_id, input_price, output_price),
        catalog_timestamp=timestamp,
        owned_by=str(item.get("owned_by") or item.get("provider") or "").strip(),
        supported_parameters=parameters,
        raw_metadata=dict(item),
    )


def fetch_gateway_models(
    profile: GatewayProfile,
    api_key: str = "",
    *,
    timeout_seconds: float = 20.0,
    opener: UrlOpenCallable | None = None,
) -> list[ModelDescriptor]:
    """Fetch and normalize the current model catalog for one gateway."""
    request = urllib.request.Request(
        profile.models_url(),
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

    timestamp = _utc_now_text()
    models = [
        normalized
        for item in _catalog_items(payload)
        if (normalized := _normalize_model(profile, item, timestamp)) is not None
    ]
    if not models:
        raise ProviderCatalogError("Gateway returned no usable models.")
    return sorted(
        models,
        key=lambda model: (
            not model.free_status,
            model.display_name.casefold(),
            model.model_id,
        ),
    )
