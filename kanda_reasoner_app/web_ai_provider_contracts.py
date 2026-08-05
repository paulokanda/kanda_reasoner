# project-path: kanda_reasoner_app/web_ai_provider_contracts.py
"""Shared contracts for KANDA remote Web AI providers.

This module is intentionally free of Qt and network imports. It defines the
stable provider, model, context, usage, and failure shapes shared by Project
Web AI and all OpenAI-compatible gateway or direct-provider transports.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping, Sequence

__all__ = [
    "ChatResult",
    "ChatUsage",
    "ContextSnapshot",
    "ProjectWebAIRequestIdentity",
    "GatewayProfile",
    "ModelDescriptor",
    "ProviderAuthenticationError",
    "ProviderCancelledError",
    "ProviderCatalogError",
    "ProviderConfigurationError",
    "ProviderConnectionError",
    "ProviderError",
    "ProviderRateLimitError",
    "ProviderResponseError",
    "ProviderTimeoutError",
    "ContextBudgetExceededError",
    "CollectorIncompleteError",
    "CollectorStatusMissingError",
    "HandoffCorruptError",
    "HandoffMemberMissingError",
    "HandoffMemberTooLargeError",
    "HandoffMissingError",
    "ProjectNotSelectedError",
    "ProjectRootInvalidError",
    "ProjectSupportRootMissingError",
    "SupportContextError",
    "SupportIdentityMismatchError",
    "SupportIdentityMissingError",
    "UnsafeArchiveMemberError",
    "gateway_profiles",
    "get_gateway_profile",
    "provider_profiles",
]


class ProviderError(RuntimeError):
    """Base class for explicit provider failures."""


class ProviderConfigurationError(ProviderError):
    """Raised when a provider profile or request is incomplete."""


class ProviderAuthenticationError(ProviderError):
    """Raised when a provider rejects the supplied credential."""


class ProviderCatalogError(ProviderError):
    """Raised when a remote model catalog cannot be loaded or normalized."""


class ProviderRateLimitError(ProviderError):
    """Raised when a provider reports a rate-limit response."""


class ProviderTimeoutError(ProviderError):
    """Raised when a provider request exceeds its timeout."""


class ProviderConnectionError(ProviderError):
    """Raised for DNS, TLS, socket, or connection failures."""


class ProviderResponseError(ProviderError):
    """Raised when a provider returns malformed or explicit error content."""


class ProviderCancelledError(ProviderError):
    """Raised when the current request is cancelled by the user."""


class SupportContextError(RuntimeError):
    """Raised when the selected project's AI handoff cannot be loaded safely."""


class ProjectNotSelectedError(SupportContextError):
    """Raised when no active Project source root was selected."""


class ProjectRootInvalidError(SupportContextError):
    """Raised when the selected Project root is missing or not source-owned."""


class ProjectSupportRootMissingError(SupportContextError):
    """Raised when canonical external Project Support is unavailable."""


class CollectorStatusMissingError(SupportContextError):
    """Raised when collector status evidence is missing."""


class CollectorIncompleteError(SupportContextError):
    """Raised when the selected Project handoff is not fully published."""


class HandoffMissingError(SupportContextError):
    """Raised when the selected Project's handoff package is absent."""


class HandoffCorruptError(SupportContextError):
    """Raised when a selected Project handoff ZIP cannot be read safely."""


class HandoffMemberMissingError(SupportContextError):
    """Raised when required handoff members are absent."""


class HandoffMemberTooLargeError(SupportContextError):
    """Raised when a handoff member exceeds its bounded read contract."""


class UnsafeArchiveMemberError(SupportContextError):
    """Raised when ZIP member spelling or metadata is unsafe."""


class ContextBudgetExceededError(SupportContextError):
    """Raised when compact Project context exceeds the transmission budget."""


class SupportIdentityMissingError(SupportContextError):
    """Raised when handoff identity fields required by canon are absent."""


class SupportIdentityMismatchError(SupportContextError):
    """Raised when Project Support belongs to a different active Project."""


@dataclass(frozen=True)
class GatewayProfile:
    """Describe one OpenAI-compatible gateway or direct provider."""

    gateway_id: str
    display_name: str
    base_url: str
    models_path: str
    chat_path: str
    api_key_env: str
    api_key_required: bool
    anonymous_free_allowed: bool
    privacy_summary: str
    static_headers: tuple[tuple[str, str], ...] = ()
    provider_class: str = "gateway"
    free_access_kind: str = "catalog_zero_price"
    free_access_summary: str = ""
    requires_free_confirmation: bool = False
    supports_stream_options: bool = True
    static_models: tuple[tuple[str, str, int], ...] = ()

    def models_url(self) -> str:
        """Return the absolute model-catalog URL."""
        if not self.models_path:
            return ""
        return self.base_url.rstrip("/") + "/" + self.models_path.lstrip("/")

    def chat_url(self) -> str:
        """Return the absolute chat-completions URL."""
        return self.base_url.rstrip("/") + "/" + self.chat_path.lstrip("/")

    def headers(self, api_key: str = "") -> dict[str, str]:
        """Return safe request headers without logging the key elsewhere."""
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": "KANDA-Reasoner/Project-Web-AI",
        }
        headers.update(dict(self.static_headers))
        clean_key = str(api_key or "").strip()
        if clean_key:
            headers["Authorization"] = "Bearer " + clean_key
        return headers


@dataclass(frozen=True)
class ModelDescriptor:
    """Normalized model-catalog entry for a remote provider."""

    gateway_id: str
    model_id: str
    display_name: str
    context_window: int = 0
    input_price: float | None = None
    output_price: float | None = None
    supports_streaming: bool = True
    supports_tools: bool = False
    free_status: bool = False
    free_access_label: str = ""
    catalog_timestamp: str = ""
    owned_by: str = ""
    supported_parameters: tuple[str, ...] = ()
    raw_metadata: Mapping[str, object] = field(
        default_factory=dict,
        compare=False,
        repr=False,
    )

    def price_label(self) -> str:
        """Return a compact human-readable access or price label."""
        if self.free_access_label:
            return self.free_access_label
        if self.free_status:
            return "free according to current catalog"
        if self.input_price is None and self.output_price is None:
            return "price unknown"
        input_value = 0.0 if self.input_price is None else self.input_price
        output_value = 0.0 if self.output_price is None else self.output_price
        return f"input {input_value:g} / output {output_value:g} per token"


@dataclass(frozen=True)
class ContextSnapshot:
    """Immutable compact context loaded for one active Project."""

    tool_project_slug: str
    tool_source_root: str
    project_slug: str
    project_id: str
    project_root: str
    project_root_fingerprint: str
    support_root: str
    daily_work_root: str
    self_hosting_mode: bool
    support_identity_status: str
    collector_status: str
    snapshot_id: str
    context_hash: str
    generated_at_utc: str
    trusted_boundary_text: str
    context_text: str
    context_bytes: int
    artifacts_loaded: tuple[str, ...]
    omitted_sections: tuple[str, ...] = ()

    def short_hash(self) -> str:
        """Return a short display hash."""
        return self.context_hash[:12]


@dataclass(frozen=True)
class ProjectWebAIRequestIdentity:
    """Bind one remote request to one Project, chat, model, and approval."""

    request_id: str
    session_id: str
    project_id: str
    project_slug: str
    project_root_fingerprint: str
    support_root: str
    snapshot_id: str
    context_hash: str
    gateway_id: str
    model_id: str
    privacy_approval_id: str
    created_at_utc: str
    project_epoch: int = 0
    evidence_context_hash: str = ""


@dataclass(frozen=True)
class ChatUsage:
    """Normalized usage and cost metadata returned by a provider."""

    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    cost_usd: float | None = None
    provider_name: str = ""


@dataclass(frozen=True)
class ChatResult:
    """Final response returned by a shared OpenAI-compatible runtime."""

    request_id: str
    gateway_id: str
    requested_model: str
    returned_model: str
    content: str
    finish_reason: str
    response_id: str
    usage: ChatUsage
    raw_metadata: Mapping[str, object] = field(
        default_factory=dict,
        compare=False,
        repr=False,
    )


_GATEWAY_PROFILES: tuple[GatewayProfile, ...] = (
    GatewayProfile(
        gateway_id="openrouter",
        display_name="OpenRouter",
        base_url="https://openrouter.ai/api/v1",
        models_path="models",
        chat_path="chat/completions",
        api_key_env="OPENROUTER_API_KEY",
        api_key_required=True,
        anonymous_free_allowed=False,
        privacy_summary=(
            "Remote gateway. Provider retention and training rules vary by routed "
            "endpoint; review current OpenRouter privacy controls before sending "
            "sensitive source."
        ),
        static_headers=(("X-OpenRouter-Title", "KANDA Reasoner"),),
    ),
    GatewayProfile(
        gateway_id="kilo",
        display_name="Kilo AI Gateway",
        base_url="https://api.kilo.ai/api/gateway",
        models_path="models",
        chat_path="chat/completions",
        api_key_env="KILO_API_KEY",
        api_key_required=False,
        anonymous_free_allowed=True,
        privacy_summary=(
            "Remote gateway. Anonymous access is limited to current free models; "
            "data-collection rules may differ by organization and upstream provider."
        ),
    ),
    GatewayProfile(
        gateway_id="gemini",
        display_name="Google Gemini API",
        base_url="https://generativelanguage.googleapis.com/v1beta/openai",
        models_path="models",
        chat_path="chat/completions",
        api_key_env="GEMINI_API_KEY",
        api_key_required=True,
        anonymous_free_allowed=False,
        privacy_summary=(
            "Direct Google API. Free-tier prompts and responses may be used to improve "
            "Google products. Do not send sensitive Project source without accepting "
            "that free-tier data policy."
        ),
        provider_class="direct",
        free_access_kind="provider_free_tier",
        free_access_summary=(
            "Official Gemini Developer API free tier. Use an unbilled Free Tier "
            "project so quota exhaustion stops requests instead of creating charges."
        ),
        requires_free_confirmation=True,
        supports_stream_options=False,
    ),
    GatewayProfile(
        gateway_id="mistral",
        display_name="Mistral API Free Mode",
        base_url="https://api.mistral.ai/v1",
        models_path="models",
        chat_path="chat/completions",
        api_key_env="MISTRAL_API_KEY",
        api_key_required=True,
        anonymous_free_allowed=False,
        privacy_summary=(
            "Direct Mistral API. This KANDA mode requires a key from Mistral Free "
            "mode and never enables a paid fallback. Review Mistral data controls "
            "before sending private source."
        ),
        provider_class="direct",
        free_access_kind="account_free_mode",
        free_access_summary=(
            "Mistral Studio Free mode with limited usage and rate limits; explicit "
            "user confirmation is required before chat is enabled."
        ),
        requires_free_confirmation=True,
        supports_stream_options=False,
    ),
    GatewayProfile(
        gateway_id="qwen",
        display_name="Qwen API Free Quota",
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        models_path="",
        chat_path="chat/completions",
        api_key_env="DASHSCOPE_API_KEY",
        api_key_required=True,
        anonymous_free_allowed=False,
        privacy_summary=(
            "Direct Alibaba Cloud Model Studio API. Use a general-purpose API key "
            "with Free Quota Only enabled. Free quota is account, model, region, and "
            "time dependent."
        ),
        provider_class="direct",
        free_access_kind="time_limited_free_quota",
        free_access_summary=(
            "New-user Qwen model quota is time limited. KANDA requires confirmation "
            "that Free Quota Only is enabled to block automatic paid usage."
        ),
        requires_free_confirmation=True,
        supports_stream_options=False,
        static_models=(
            ("qwen3-coder-flash", "Qwen3 Coder Flash", 1_000_000),
            ("qwen3-coder-next", "Qwen3 Coder Next", 262_144),
            ("qwen3-coder-plus", "Qwen3 Coder Plus", 1_000_000),
        ),
    ),
    GatewayProfile(
        gateway_id="groq",
        display_name="Groq API Free Plan",
        base_url="https://api.groq.com/openai/v1",
        models_path="models",
        chat_path="chat/completions",
        api_key_env="GROQ_API_KEY",
        api_key_required=True,
        anonymous_free_allowed=False,
        privacy_summary=(
            "Direct Groq API. This KANDA mode requires an organization on the "
            "Groq Free Plan and never authorizes a paid-plan fallback."
        ),
        provider_class="direct",
        free_access_kind="account_free_plan",
        free_access_summary=(
            "Groq Free Plan with organization-level request and token limits. "
            "Explicit confirmation is required before chat is enabled."
        ),
        requires_free_confirmation=True,
        supports_stream_options=False,
    ),
)


def gateway_profiles() -> Sequence[GatewayProfile]:
    """Return all immutable remote-provider profiles for compatibility."""
    return _GATEWAY_PROFILES


def provider_profiles(provider_class: str = "") -> Sequence[GatewayProfile]:
    """Return all profiles or only one provider class."""
    clean = str(provider_class or "").strip().lower()
    if not clean:
        return _GATEWAY_PROFILES
    return tuple(
        profile
        for profile in _GATEWAY_PROFILES
        if profile.provider_class == clean
    )


def get_gateway_profile(gateway_id: str) -> GatewayProfile:
    """Return one provider profile or raise an explicit configuration error."""
    clean_id = str(gateway_id or "").strip().lower()
    for profile in _GATEWAY_PROFILES:
        if profile.gateway_id == clean_id:
            return profile
    raise ProviderConfigurationError("Unknown Web AI provider: " + clean_id)
