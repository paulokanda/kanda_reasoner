#!/usr/bin/env python3
# project-path: kanda_reasoner_app/insert_missing_docstrings_gui/ai_docstring_generator.py
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
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from kanda_reasoner_app.project_support_boundary import canonical_project_support_root
from kanda_reasoner_app.tab3_manual_review_runtime.ai_openai_compatible_provider_runtime import (
    local_openai_compatible_profile,
)
from kanda_reasoner_app.web_ai_provider_contracts import (
    GatewayProfile,
    ProviderError,
    get_gateway_profile,
)
from kanda_reasoner_app.web_ai_provider_runtime import request_chat_completion

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
from .ai_docstring_generator_help.generation_guardrails import (
    _AIOutputFailure as _AIOutputFailure,
    _LOW_INFORMATION_SUMMARY_PREFIXES as _LOW_INFORMATION_SUMMARY_PREFIXES,
    _LOW_INFORMATION_SUMMARY_VALUES as _LOW_INFORMATION_SUMMARY_VALUES,
    _detect_low_information_docstring as _detect_low_information_docstring,
    _detect_unsupported_structured_claims as _detect_unsupported_structured_claims,
    _first_docstring_line as _first_docstring_line,
    _iter_payload_items as _iter_payload_items,
    _normalized_summary_key as _normalized_summary_key,
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


class AIDocstringGenerator:
    """Represent aidocstring generator."""
    
    def __init__(
        self,
        *,
        config: AIConfig,
        project_root: Path,
        policy: DocstringPolicy | None = None,
        on_fallback: Callable[[str, str], None] | None = None,
        on_low_confidence: Callable[[str, list[str]], None] | None = None,
    ) -> None:
        """Support init behavior.
        
        Parameters
        ----------
        config : AIConfig
            The configuration data.
        project_root : Path
            The project root path.
        policy : DocstringPolicy | None, optional
            The optional policy value.
        on_fallback : Callable[[str, str], None] | None, optional
            The optional on fallback value.
        on_low_confidence : Callable[[str, list[str]], None] | None, optional
            The optional on low confidence value.
        """
        
        self._config = config
        self._project_root = Path(project_root)
        self._policy = policy or DocstringPolicy.load_for_project(project_root)
        self._on_fallback = on_fallback
        self._on_low_confidence = on_low_confidence
        cache_name = Path(self._config.cache_path).name or "docstring_cache.json"
        self._cache_path = (
            canonical_project_support_root(self._project_root)
            / "docstring_assistant"
            / cache_name
        )
        self._cache: dict[str, dict] = self._load_cache() if self._config.cache_enabled else {}
        self.stats = GenerationStats()

    def _load_cache(self) -> dict[str, dict]:
        """Support load cache behavior.
        
        Returns
        -------
        dict[str, dict]
            The mapped values.
        """
        
        if not self._cache_path.exists():
            return {}
        try:
            return json.loads(self._cache_path.read_text(encoding="utf-8"))
        except Exception:
            return {}

    def flush_cache(self) -> None:
        """Support flush cache behavior.
        """
        
        if not self._config.cache_enabled:
            return
        self._cache_path.parent.mkdir(parents=True, exist_ok=True)
        self._cache_path.write_text(
            json.dumps(self._cache, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    def _cache_key(self, ctx: SymbolContext) -> str:
        """Support cache key behavior.
        
        Parameters
        ----------
        ctx : SymbolContext
            The ctx value.
        
        Returns
        -------
        str
            The string result.
        """
        
        payload = {
            "module_id": ctx.module_id,
            "kind": ctx.kind,
            "name": ctx.name,
            "signature": ctx.signature,
            "source": ctx.source_lines,
            "module_summary_block": ctx.module_summary_block,
            "provider_mode": self._config.provider_mode,
            "gateway_id": self._config.gateway_id,
            "model": self._config.model,
            "style": self._config.docstring_style,
            "policy_style": self._policy.style,
            "structured": self._config.use_structured_outputs,
        }
        return hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()

    def _build_validation_config(self) -> ValidationConfig:
        """Support build validation config behavior.
        
        Returns
        -------
        ValidationConfig
            The validation config result.
        """
        
        return ValidationConfig(
            max_line_length=self._config.max_line_length,
            max_todo_ratio=self._config.max_todo_ratio,
            min_confidence=self._config.min_confidence,
            max_length=self._config.max_docstring_length,
            allow_invented_params=self._config.allow_invented_params,
            allow_invented_raises=self._config.allow_invented_raises,
        )

    def _request_content(self, payload: dict[str, Any]) -> str:
        """Return one model response through KANDA's shared transport."""
        messages = payload.get("messages")
        if not isinstance(messages, list):
            raise ValueError("AI payload messages must be a list.")
        profile = self._provider_profile()
        request_options: dict[str, object] = {}
        if payload.get("response_format") is not None:
            request_options["response_format"] = payload["response_format"]
        if self._config.seed is not None:
            request_options["seed"] = self._config.seed
        if profile.gateway_id == "openrouter":
            request_options["provider"] = {
                "allow_fallbacks": False,
                "data_collection": "deny",
                "require_parameters": True,
            }
        result = request_chat_completion(
            profile,
            self._config.model,
            messages,
            self._config._api_key,
            request_id="docstring-generator",
            timeout_seconds=self._config.timeout_seconds,
            max_tokens=self._config.max_tokens,
            temperature=self._config.temperature,
            request_options=request_options,
        )
        return result.content

    def _provider_profile(self) -> GatewayProfile:
        """Return the configured local or web provider profile."""
        if str(self._config.provider_mode or "").strip().lower() == "web":
            return get_gateway_profile(self._config.gateway_id)
        return local_openai_compatible_profile(self._config.base_url)

    def _call_model(self, ctx: SymbolContext) -> tuple[str, str]:
        """Support call model behavior.
        
        Parameters
        ----------
        ctx : SymbolContext
            The ctx value.
        
        Returns
        -------
        tuple[str, str]
            The tuple of values.
        """
        
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
                                "strict": True,
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
            if str(self._config.provider_mode).strip().lower() == "web":
                attempts = attempts[:1]

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
        """Support fallback behavior.
        
        Parameters
        ----------
        ctx : SymbolContext
            The ctx value.
        reason : str
            The reason value.
        failure_reason : str
            The failure reason value.
        
        Returns
        -------
        GenerationResult
            The generation result result.
        """
        
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
        """Support generate behavior.
        
        Parameters
        ----------
        ctx : SymbolContext
            The ctx value.
        
        Returns
        -------
        GenerationResult
            The generation result result.
        """
        
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
        except (
            ProviderError,
            TimeoutError,
            OSError,
            KeyError,
            ValueError,
            json.JSONDecodeError,
        ) as exc:
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
