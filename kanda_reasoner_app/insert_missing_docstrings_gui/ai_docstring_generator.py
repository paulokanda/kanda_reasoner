#!/usr/bin/env python3
"""AI-powered docstring generator with structured-output first generation."""

from __future__ import annotations

__all__ = [
    "AIDocstringGenerator",
    "GenerationResult",
    "GenerationStats",
]

import hashlib
import json
import re
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from .ai_config import AIConfig
from .context_builder import AttributeInfo, ParameterInfo, SymbolContext
from .docstring_policy import DocstringPolicy
from .docstring_validator import ValidationConfig, validate

from .ai_docstring_generator_help.heuristics import _heuristic_docstring
from .ai_docstring_generator_help.models import GenerationResult, GenerationStats
from .ai_docstring_generator_help.docstring_payloads import (
    _build_system_prompt,
    _build_user_prompt,
    _docstring_schema,
)
from .ai_docstring_generator_help.response_parsing import (
    _json_from_text,
    _render_structured_docstring,
)


_FAILURE_NONE = "none"
_FAILURE_MODEL_INVALID_JSON = "model_invalid_json"
_FAILURE_STRUCTURED_RENDER_ERROR = "structured_render_error"
_FAILURE_AI_CALL_FAILED = "ai_call_failed"
_FAILURE_VALIDATION_REJECTED = "validation_rejected"
_FAILURE_QUALITY_REJECTED = "quality_rejected"
_FAILURE_UNSUPPORTED_AI_CLAIM = "unsupported_ai_claim"
_FAILURE_PRIVATE_SYMBOL_SKIPPED = "private_symbol_skipped"

_SOURCE_AI_STRUCTURED_SCHEMA = "ai_structured_json_schema"
_SOURCE_AI_STRUCTURED_OBJECT = "ai_structured_json_object"
_SOURCE_AI_LEGACY_RAW = "ai_legacy_raw"
_SOURCE_HEURISTIC_FALLBACK = "heuristic_fallback"
_SOURCE_SKIPPED_PRIVATE = "skipped_private"
_SOURCE_CACHE = "cache"


class _AIOutputFailure(RuntimeError):
    """Represent an AI output failure with a canonical reason code."""

    def __init__(self, failure_reason: str, message: str) -> None:
        super().__init__(message)
        self.failure_reason = failure_reason


def _iter_payload_items(payload: dict[str, Any], key: str) -> list[dict[str, Any]]:
    """Return object items from a structured AI payload list field."""
    raw_items = payload.get(key, [])
    if not isinstance(raw_items, list):
        return []
    return [item for item in raw_items if isinstance(item, dict)]


def _detect_unsupported_structured_claims(
    ctx: SymbolContext,
    payload: dict[str, Any],
) -> list[str]:
    """Return structured AI claims that are not grounded in SymbolContext."""
    issues: list[str] = []

    valid_params = {param.name for param in ctx.parameters}
    for item in _iter_payload_items(payload, "parameters"):
        name = str(item.get("name", "")).lstrip("*").strip()
        if name and name not in valid_params:
            issues.append("unsupported parameter: " + name)

    valid_raises = set(ctx.raises_types)
    for item in _iter_payload_items(payload, "raises"):
        name = str(item.get("type", "")).strip()
        if name and name not in valid_raises:
            issues.append("unsupported raise: " + name)

    valid_attrs = {attr.name for attr in ctx.class_attributes}
    for item in _iter_payload_items(payload, "attributes"):
        name = str(item.get("name", "")).strip()
        if name and name not in valid_attrs:
            issues.append("unsupported attribute: " + name)

    return issues

_LOW_INFORMATION_SUMMARY_PREFIXES = (
    "describe ",
    "document ",
    "todo",
)

_LOW_INFORMATION_SUMMARY_VALUES = {
    "docstring",
    "documentation",
    "function",
    "method",
    "class",
    "module",
    "object",
    "value",
}


def _first_docstring_line(body: str) -> str:
    """Return the first non-empty rendered docstring line."""
    for line in body.splitlines():
        stripped = line.strip()
        if stripped:
            return stripped
    return ""


def _normalized_summary_key(summary: str) -> str:
    """Return a lowercase summary key without terminal punctuation."""
    return summary.strip().lower().rstrip(".!?:; ")


def _detect_low_information_docstring(ctx: SymbolContext, body: str) -> list[str]:
    """Return evidence-bound quality issues in a rendered AI docstring."""
    issues: list[str] = []
    summary = _first_docstring_line(body)
    summary_key = _normalized_summary_key(summary)

    if not summary:
        issues.append("missing summary")
    elif summary_key in _LOW_INFORMATION_SUMMARY_VALUES:
        issues.append("low-information summary: " + summary)
    elif any(summary_key.startswith(prefix) for prefix in _LOW_INFORMATION_SUMMARY_PREFIXES):
        issues.append("low-information summary: " + summary)
    elif len(summary_key.split()) < 3 and ctx.kind in {"module", "class", "function", "method"}:
        issues.append("too-short summary: " + summary)

    if "TODO:" in body:
        issues.append("contains TODO placeholder")

    return issues

@dataclass


@dataclass


class AIDocstringGenerator:
    def __init__(
        self,
        *,
        config: AIConfig,
        project_root: Path,
        policy: DocstringPolicy | None = None,
        on_fallback: Callable[[str, str], None] | None = None,
        on_low_confidence: Callable[[str, list[str]], None] | None = None,
    ) -> None:
        self._config = config
        self._project_root = Path(project_root)
        self._policy = policy or DocstringPolicy.load_for_project(project_root)
        self._on_fallback = on_fallback
        self._on_low_confidence = on_low_confidence
        self._cache_path = self._project_root / self._config.cache_path
        self._cache: dict[str, dict] = self._load_cache() if self._config.cache_enabled else {}
        self.stats = GenerationStats()

    def _load_cache(self) -> dict[str, dict]:
        if not self._cache_path.exists():
            return {}
        try:
            return json.loads(self._cache_path.read_text(encoding="utf-8"))
        except Exception:
            return {}

    def flush_cache(self) -> None:
        if not self._config.cache_enabled:
            return
        self._cache_path.write_text(
            json.dumps(self._cache, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    def _cache_key(self, ctx: SymbolContext) -> str:
        payload = {
            "module_id": ctx.module_id,
            "kind": ctx.kind,
            "name": ctx.name,
            "signature": ctx.signature,
            "source": ctx.source_lines,
            "module_summary_block": ctx.module_summary_block,
            "model": self._config.model,
            "style": self._config.docstring_style,
            "policy_style": self._policy.style,
            "structured": self._config.use_structured_outputs,
        }
        return hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()

    def _build_validation_config(self) -> ValidationConfig:
        return ValidationConfig(
            max_line_length=self._config.max_line_length,
            max_todo_ratio=self._config.max_todo_ratio,
            min_confidence=self._config.min_confidence,
            max_length=self._config.max_docstring_length,
            allow_invented_params=self._config.allow_invented_params,
            allow_invented_raises=self._config.allow_invented_raises,
        )

    def _request_content(self, payload: dict[str, Any]) -> str:
        url = self._config.base_url.rstrip("/") + "/chat/completions"
        if self._config.seed is not None:
            payload.setdefault("seed", self._config.seed)
        request = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=self._config.timeout_seconds) as response:
            data = json.loads(response.read().decode("utf-8"))
        return data["choices"][0]["message"]["content"]

    def _call_model(self, ctx: SymbolContext) -> tuple[str, str]:
        base_payload = {
            "model": self._config.model,
            "messages": [],
            "temperature": self._config.temperature,
            "max_tokens": self._config.max_tokens,
            "stream": False,
        }

        if self._config.use_structured_outputs:
            structured_system = _build_system_prompt(self._policy, structured=True)
            structured_user = _build_user_prompt(ctx, self._policy, structured=True)
            schema = _docstring_schema()

            attempts: list[tuple[str, dict[str, Any]]] = [
                (
                    _SOURCE_AI_STRUCTURED_SCHEMA,
                    {
                        **base_payload,
                        "messages": [
                            {"role": "system", "content": structured_system},
                            {"role": "user", "content": structured_user},
                        ],
                        "response_format": {
                            "type": "json_schema",
                            "json_schema": {
                                "name": "docstring_payload",
                                "schema": schema,
                            },
                        },
                    },
                ),
                (
                    _SOURCE_AI_STRUCTURED_OBJECT,
                    {
                        **base_payload,
                        "messages": [
                            {"role": "system", "content": structured_system},
                            {"role": "user", "content": structured_user},
                        ],
                        "response_format": {"type": "json_object"},
                    },
                ),
            ]

            last_json_error: Exception | None = None
            for generation_source, payload in attempts:
                content = self._request_content(payload)
                try:
                    parsed = _json_from_text(content)
                except (ValueError, json.JSONDecodeError) as exc:
                    last_json_error = exc
                    continue
                unsupported_claims = _detect_unsupported_structured_claims(ctx, parsed)
                if unsupported_claims:
                    raise _AIOutputFailure(
                        _FAILURE_UNSUPPORTED_AI_CLAIM,
                        "Structured AI payload included unsupported claims: "
                        + "; ".join(unsupported_claims),
                    )
                try:
                    return _render_structured_docstring(ctx, self._policy, parsed), generation_source
                except Exception as exc:
                    raise _AIOutputFailure(
                        _FAILURE_STRUCTURED_RENDER_ERROR,
                        "Structured docstring rendering failed: " + str(exc),
                    ) from exc

            detail = str(last_json_error) if last_json_error is not None else "No structured response returned."
            raise _AIOutputFailure(_FAILURE_MODEL_INVALID_JSON, detail)

        legacy_payload = {
            **base_payload,
            "messages": [
                {"role": "system", "content": _build_system_prompt(self._policy, structured=False)},
                {"role": "user", "content": _build_user_prompt(ctx, self._policy, structured=False)},
            ],
        }
        return self._request_content(legacy_payload), _SOURCE_AI_LEGACY_RAW

    def _fallback(
        self,
        ctx: SymbolContext,
        reason: str,
        *,
        failure_reason: str,
    ) -> GenerationResult:
        self.stats.fallback += 1
        self.stats.record_failure(failure_reason)
        if self._on_fallback is not None:
            self._on_fallback(ctx.full_name, reason)
        return GenerationResult(
            body=_heuristic_docstring(ctx, self._policy),
            source="heuristic",
            confidence="low",
            issues=[reason],
            used_fallback=True,
            generation_source=_SOURCE_HEURISTIC_FALLBACK,
            failure_reason=failure_reason,
            failure_detail=reason,
        )

    def generate(self, ctx: SymbolContext) -> GenerationResult:
        self.stats.total += 1
        is_private = ctx.name.startswith("_")
        if is_private and not self._config.include_private:
            self.stats.skipped_private += 1
            self.stats.record_failure(_FAILURE_PRIVATE_SYMBOL_SKIPPED)
            reason = "Private symbols are configured to skip AI generation."
            return GenerationResult(
                body=_heuristic_docstring(ctx, self._policy),
                source="heuristic",
                confidence="low",
                issues=[reason],
                used_fallback=True,
                generation_source=_SOURCE_SKIPPED_PRIVATE,
                failure_reason=_FAILURE_PRIVATE_SYMBOL_SKIPPED,
                failure_detail=reason,
            )

        cache_key = self._cache_key(ctx)
        if self._config.cache_enabled and cache_key in self._cache:
            cached = self._cache[cache_key]
            self.stats.cached += 1
            return GenerationResult(
                body=cached.get("body", ""),
                source="cache",
                confidence=cached.get("confidence", "high"),
                issues=list(cached.get("issues", [])),
                cache_hit=True,
                uncertain=cached.get("confidence") == "low",
                uncertain_comment="# AI-UNCERTAIN" if cached.get("confidence") == "low" else "",
                generation_source=str(cached.get("generation_source", _SOURCE_CACHE) or _SOURCE_CACHE),
                failure_reason=str(cached.get("failure_reason", _FAILURE_NONE) or _FAILURE_NONE),
                failure_detail=str(cached.get("failure_detail", "") or ""),
            )

        try:
            raw, generation_source = self._call_model(ctx)
        except _AIOutputFailure as exc:
            if self._config.fallback_to_heuristic:
                return self._fallback(ctx, str(exc), failure_reason=exc.failure_reason)
            raise RuntimeError(str(exc)) from exc
        except (urllib.error.URLError, TimeoutError, OSError, KeyError, ValueError, json.JSONDecodeError) as exc:
            reason = f"AI call failed: {exc}"
            if self._config.fallback_to_heuristic:
                return self._fallback(ctx, reason, failure_reason=_FAILURE_AI_CALL_FAILED)
            raise RuntimeError(reason) from exc

        result = validate(raw, ctx, self._build_validation_config())
        if not result.ok:
            reason = result.fatal_reason or "Validation rejected AI output."
            if self._config.fallback_to_heuristic:
                return self._fallback(ctx, reason, failure_reason=_FAILURE_VALIDATION_REJECTED)
            raise ValueError(reason)

        quality_issues = _detect_low_information_docstring(ctx, result.cleaned)
        if quality_issues:
            reason = (
                "Docstring quality gate rejected AI output: "
                + "; ".join(quality_issues)
            )
            if self._config.fallback_to_heuristic:
                return self._fallback(ctx, reason, failure_reason=_FAILURE_QUALITY_REJECTED)
            raise ValueError(reason)

        self.stats.ai_ok += 1
        if result.confidence == "medium":
            self.stats.medium_confidence += 1
        elif result.confidence == "low":
            self.stats.low_confidence += 1
            if self._on_low_confidence is not None:
                self._on_low_confidence(ctx.full_name, result.issues)

        if self._config.cache_enabled:
            self._cache[cache_key] = {
                "body": result.cleaned,
                "confidence": result.confidence,
                "issues": result.issues,
                "generation_source": generation_source,
                "failure_reason": _FAILURE_NONE,
                "failure_detail": "",
            }

        uncertain_comment = ""
        if result.confidence == "low" and self._config.uncertain_annotation:
            uncertain_comment = result.ai_uncertain_comment or "# AI-UNCERTAIN"

        return GenerationResult(
            body=result.cleaned,
            source="ai",
            confidence=result.confidence,
            issues=result.issues,
            uncertain=result.confidence == "low",
            uncertain_comment=uncertain_comment,
            generation_source=generation_source,
            failure_reason=_FAILURE_NONE,
            failure_detail="",
        )
