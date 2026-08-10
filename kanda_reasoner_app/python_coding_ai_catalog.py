# project-path: kanda_reasoner_app/python_coding_ai_catalog.py
"""Canonical free Python-coding AI catalog for direct and manual routes.

The catalog is Tool-owned and deliberately contains no active Project state,
credentials, payloads, browser automation, or provider request execution.
"""

from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import urlsplit

from kanda_reasoner_app.web_ai_provider_contracts import ModelDescriptor

__all__ = [
    "ExternalPythonCodingAssistant",
    "approved_direct_model_ids",
    "external_python_coding_assistants",
    "get_external_python_coding_assistant",
    "is_approved_free_python_coding_model",
    "validate_official_assistant_url",
]

_VERIFIED_DATE = "2026-08-02"
_MAX_OFFICIAL_URL_LENGTH = 2048


@dataclass(frozen=True, slots=True)
class ExternalPythonCodingAssistant:
    """Describe one manual free web assistant suitable for Python coding."""

    assistant_id: str
    display_name: str
    official_url: str
    allowed_hosts: tuple[str, ...]
    free_status: str
    python_coding_summary: str
    privacy_summary: str
    last_verified_date: str = _VERIFIED_DATE

    def validated_url(self) -> str:
        """Return the official URL after strict HTTPS and host validation."""
        return validate_official_assistant_url(
            self.official_url,
            allowed_hosts=self.allowed_hosts,
        )


_APPROVED_DIRECT_MODELS: dict[str, tuple[str, ...]] = {
    "openrouter": (
        "openai/gpt-oss-120b:free",
        "openai/gpt-oss-20b:free",
        "cohere/north-mini-code:free",
    ),
    "kilo": (
        "kilo-auto/free",
        "openai/gpt-oss-120b:free",
        "openai/gpt-oss-20b:free",
        "cohere/north-mini-code:free",
    ),
    "gemini": (
        "gemini-3.5-flash",
        "gemini-3.5-flash-lite",
    ),
    "mistral": (
        "mistral-medium-3-5",
        "mistral-small-2603",
    ),
    "qwen": (
        "qwen3-coder-flash",
        "qwen3-coder-next",
        "qwen3-coder-plus",
    ),
    "groq": (
        "openai/gpt-oss-120b",
        "openai/gpt-oss-20b",
        "qwen/qwen3.6-27b",
    ),
}

_EXTERNAL_ASSISTANTS: tuple[ExternalPythonCodingAssistant, ...] = (
    ExternalPythonCodingAssistant(
        assistant_id="deepseek_chat",
        display_name="DeepSeek Chat Free",
        official_url="https://chat.deepseek.com/",
        allowed_hosts=("chat.deepseek.com",),
        free_status="VERIFIED FREE WEB ACCESS",
        python_coding_summary=(
            "Manual web chat for Python generation, debugging, review, and refactoring."
        ),
        privacy_summary=(
            "Remote service. Review current terms before sending private source or data."
        ),
    ),
    ExternalPythonCodingAssistant(
        assistant_id="qwen_studio",
        display_name="Qwen Studio Free",
        official_url="https://qwen.ai/qwenchat",
        allowed_hosts=("qwen.ai", "chat.qwen.ai"),
        free_status="VERIFIED FREE WEB ACCESS",
        python_coding_summary=(
            "Manual web assistant with coding support for Python and technical tasks."
        ),
        privacy_summary=(
            "Remote service. Review current terms before sending private source or data."
        ),
    ),
    ExternalPythonCodingAssistant(
        assistant_id="claude_free",
        display_name="Claude Free",
        official_url="https://claude.ai/",
        allowed_hosts=("claude.ai",),
        free_status="LIMITED FREE WEB ACCESS",
        python_coding_summary=(
            "Manual web assistant for Python explanation, debugging, and code review."
        ),
        privacy_summary=(
            "Remote service with usage limits. Review current data controls before use."
        ),
    ),
    ExternalPythonCodingAssistant(
        assistant_id="chatgpt_free",
        display_name="ChatGPT Free",
        official_url="https://chatgpt.com/",
        allowed_hosts=("chatgpt.com", "chat.openai.com"),
        free_status="LIMITED FREE WEB ACCESS",
        python_coding_summary=(
            "Manual web assistant for Python generation, debugging, and general coding."
        ),
        privacy_summary=(
            "Remote service with changing limits. Review current data controls before use."
        ),
    ),
    ExternalPythonCodingAssistant(
        assistant_id="mistral_vibe_free",
        display_name="Mistral Vibe Free",
        official_url="https://chat.mistral.ai/chat",
        allowed_hosts=("chat.mistral.ai",),
        free_status="LIMITED FREE WEB ACCESS",
        python_coding_summary=(
            "Manual web assistant for simple Python coding and technical questions."
        ),
        privacy_summary=(
            "Remote service with limited free access. Review current terms before use."
        ),
    ),
)


def approved_direct_model_ids(gateway_id: str) -> tuple[str, ...]:
    """Return the exact approved free Python-coding model IDs for a gateway."""
    return _APPROVED_DIRECT_MODELS.get(str(gateway_id or "").strip().lower(), ())


def is_approved_free_python_coding_model(model: ModelDescriptor) -> bool:
    """Return whether a live descriptor matches the approved zero-cost catalog."""
    approved = set(approved_direct_model_ids(model.gateway_id))
    return bool(model.free_status and model.model_id in approved)


def external_python_coding_assistants() -> tuple[ExternalPythonCodingAssistant, ...]:
    """Return the immutable manual web-assistant catalog."""
    return _EXTERNAL_ASSISTANTS


def get_external_python_coding_assistant(
    assistant_id: str,
) -> ExternalPythonCodingAssistant:
    """Return one assistant by stable ID or raise a clear error."""
    clean = str(assistant_id or "").strip().lower()
    for assistant in _EXTERNAL_ASSISTANTS:
        if assistant.assistant_id == clean:
            assistant.validated_url()
            return assistant
    raise ValueError("Unknown external Python-coding assistant: " + clean)


def validate_official_assistant_url(
    url: str,
    *,
    allowed_hosts: tuple[str, ...],
) -> str:
    """Validate one official HTTPS URL without following it or using credentials."""
    clean = str(url or "").strip()
    if not clean or len(clean) > _MAX_OFFICIAL_URL_LENGTH:
        raise ValueError("External assistant URL is empty or too long.")
    parsed = urlsplit(clean)
    if parsed.scheme.lower() != "https":
        raise ValueError("External assistant URL must use HTTPS.")
    if parsed.username or parsed.password:
        raise ValueError("External assistant URL must not contain credentials.")
    host = str(parsed.hostname or "").lower()
    normalized_hosts = {str(value).strip().lower() for value in allowed_hosts}
    if not host or host not in normalized_hosts:
        raise ValueError("External assistant URL host is not allowlisted: " + host)
    if parsed.port not in (None, 443):
        raise ValueError("External assistant URL must not use a custom port.")
    return clean
