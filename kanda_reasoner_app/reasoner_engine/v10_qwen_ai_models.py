"""Support V10 project reasoning and evidence handling."""
from __future__ import annotations


__all__ = [
    "V9QwenAIModels",
]

import json
from pathlib import Path
from typing import Any, Callable

import requests

from .v10_qwen_ai_models_helpers_private import (
    _LocalAIRequestQueue,
    _LocalDiskCache,
    _LocalGovernanceStateReader,
)


DEFAULT_OLLAMA_BASE_URL = "http://127.0.0.1:11434/v1"

FAST_MODEL = "qwen2.5-coder:7b"
SMART_MODEL = "qwen2.5-coder:32b"

AUTO_THRESHOLD = 3000
TIMEOUT = 600


class V9QwenAIModels:
    """
    V10-exclusive local AI connector.

    Responsibilities:
    - generic non-stream chat
    - generic stream chat
    - model override support
    - governance modifier injection
    - optional persistent disk cache
    - async execution through a local single-worker queue
    """

    def __init__(self, *, base_url: str = "") -> None:
        """Support init behavior.
        """
        
        self._base_url = _runtime_base_url(base_url)
        self._chat_url = self._base_url.rstrip("/") + "/chat/completions"
        self._governance_state_path = (
            Path(__file__).resolve().parent / "governance_state.json"
        )
        self._cache = _LocalDiskCache()
        self._request_queue = _LocalAIRequestQueue()

    def set_base_url(self, base_url: str) -> None:
        """Update the OpenAI-compatible endpoint for future requests."""
        self._base_url = _normalize_base_url(base_url)
        self._chat_url = self._base_url.rstrip("/") + "/chat/completions"

    def set_cache_dir(self, cache_dir: Path) -> None:
        """Set the cache dir.
        
        Parameters
        ----------
        cache_dir : Path
            The cache dir value.
        """
        
        self._cache.set_cache_dir(Path(cache_dir).expanduser().resolve())

    def set_governance_state_path(self, state_path: Path) -> None:
        """Set the governance state path.
        
        Parameters
        ----------
        state_path : Path
            The state path value.
        """
        
        self._governance_state_path = Path(state_path).expanduser().resolve()

    def _choose_model(self, text: Any) -> str:
        """Support choose model behavior.
        
        Parameters
        ----------
        text : Any
            The text value.
        
        Returns
        -------
        str
            The string result.
        """
        
        if isinstance(text, list):
            content_len = sum(len(str(message.get("content", ""))) for message in text if isinstance(message, dict))
        else:
            content_len = len(str(text))
        return FAST_MODEL if content_len < AUTO_THRESHOLD else SMART_MODEL

    def _post(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Support post behavior.
        
        Parameters
        ----------
        payload : dict[str, Any]
            The payload value.
        
        Returns
        -------
        dict[str, Any]
            The mapped values.
        """
        
        response = requests.post(self._chat_url, json=payload, timeout=TIMEOUT)
        response.raise_for_status()
        return response.json()

    def _get_governance_modifier(self) -> str:
        """Support get governance modifier behavior.
        
        Returns
        -------
        str
            The string result.
        """
        
        state_reader = _LocalGovernanceStateReader(self._governance_state_path)
        mode = state_reader.get_mode()

        if mode == 0:
            return (
                "Operate normally. Prefer clarity and modularity. "
                "Allow reasonable refactoring."
            )

        if mode == 1:
            return (
                "Operate under elevated architectural caution. "
                "Avoid speculative refactors. "
                "Prioritize safety and stability."
            )

        if mode == 2:
            return (
                "SYSTEM IS IN FREEZE MODE. "
                "Do NOT propose structural changes. "
                "Only analyze and explain. "
                "No refactoring or architectural modification."
            )

        return ""

    def _prepare_messages(
        self,
        messages: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        """Support prepare messages behavior.
        
        Parameters
        ----------
        messages : list[dict[str, Any]]
            The message values.
        
        Returns
        -------
        list[dict[str, Any]]
            The list of values.
        """
        
        modifier = self._get_governance_modifier()
        prepared_messages = [dict(message) for message in messages]

        if prepared_messages and prepared_messages[0].get("role") == "system":
            original_content = prepared_messages[0].get("content", "")
            prepared_messages[0]["content"] = f"{original_content}\n\n{modifier}"
        else:
            prepared_messages.insert(
                0,
                {
                    "role": "system",
                    "content": modifier,
                },
            )

        return prepared_messages

    def chat(
        self,
        messages: list[dict[str, Any]],
        *,
        model: str | None = None,
        temperature: float = 0.2,
        max_tokens: int | None = None,
        use_cache: bool = False,
        cache_key_data: dict[str, Any] | None = None,
    ) -> str:
        """
        Synchronous generic chat.
        """

        if use_cache and cache_key_data:
            cached = self._cache.get(cache_key_data)
            if cached is not None:
                return str(cached)

        model_to_use = model or self._choose_model(messages)
        prepared_messages = self._prepare_messages(messages)

        payload: dict[str, Any] = {
            "model": model_to_use,
            "messages": prepared_messages,
            "options": {
                "temperature": temperature,
            },
        }

        if max_tokens is not None:
            payload["max_tokens"] = max_tokens

        response = self._post(payload)

        text = (
            response.get("choices", [{}])[0]
            .get("message", {})
            .get("content", "")
        )

        if use_cache and cache_key_data:
            self._cache.set_value(cache_key_data, text)

        return text

    def chat_async(
        self,
        messages: list[dict[str, Any]],
        *,
        model: str | None = None,
        temperature: float = 0.2,
        max_tokens: int | None = None,
        use_cache: bool = False,
        cache_key_data: dict[str, Any] | None = None,
        on_success: Callable[[str], None] | None = None,
        on_error: Callable[[str], None] | None = None,
    ) -> None:
        """
        Async generic chat.
        """

        def task() -> None:
            try:
                text = self.chat(
                    messages,
                    model=model,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    use_cache=use_cache,
                    cache_key_data=cache_key_data,
                )
                if on_success:
                    on_success(text)
            except Exception as exc:
                if on_error:
                    on_error(str(exc))

        self._request_queue.submit(task)

    def stream_chat(
        self,
        messages: list[dict[str, Any]],
        *,
        model: str | None = None,
        temperature: float = 0.2,
        max_tokens: int | None = None,
        use_cache: bool = False,
        cache_key_data: dict[str, Any] | None = None,
        on_token: Callable[[str], None] | None = None,
        on_done: Callable[[str], None] | None = None,
        on_error: Callable[[str], None] | None = None,
    ) -> None:
        """
        Async streamed generic chat.
        Emits text chunks through on_token and the final full text through on_done.
        """

        def task() -> None:
            try:
                if use_cache and cache_key_data:
                    cached = self._cache.get(cache_key_data)
                    if cached is not None:
                        cached_text = str(cached)
                        if on_token:
                            on_token(cached_text)
                        if on_done:
                            on_done(cached_text)
                        return

                model_to_use = model or self._choose_model(messages)
                prepared_messages = self._prepare_messages(messages)

                payload: dict[str, Any] = {
                    "model": model_to_use,
                    "messages": prepared_messages,
                    "stream": True,
                    "options": {
                        "temperature": temperature,
                    },
                }

                if max_tokens is not None:
                    payload["max_tokens"] = max_tokens

                full = ""

                with requests.post(
                    self._chat_url,
                    json=payload,
                    stream=True,
                    timeout=TIMEOUT,
                ) as response:
                    response.raise_for_status()

                    for line in response.iter_lines():
                        if not line:
                            continue

                        if isinstance(line, (bytes, bytearray)):
                            line_str = line.decode("utf-8", errors="ignore").strip()
                        else:
                            line_str = str(line).strip()

                        if not line_str:
                            continue

                        if line_str.startswith("data:"):
                            line_str = line_str[len("data:"):].strip()

                        if not line_str or line_str == "[DONE]":
                            continue

                        try:
                            data = json.loads(line_str)
                        except Exception:
                            continue

                        token = (
                            data.get("choices", [{}])[0]
                            .get("delta", {})
                            .get("content", "")
                            or ""
                        )

                        if token:
                            full += token
                            if on_token:
                                on_token(token)

                if use_cache and cache_key_data:
                    self._cache.set_value(cache_key_data, full)

                if on_done:
                    on_done(full)

            except Exception as exc:
                if on_error:
                    on_error(str(exc))

        self._request_queue.submit(task)


def _normalize_base_url(value: str) -> str:
    clean = str(value or DEFAULT_OLLAMA_BASE_URL).strip().rstrip("/")
    if clean.endswith("/chat/completions"):
        clean = clean[: -len("/chat/completions")]
    if not clean.endswith("/v1"):
        clean += "/v1"
    return clean


def _runtime_base_url(explicit: str) -> str:
    if str(explicit or "").strip():
        return _normalize_base_url(explicit)
    from kanda_reasoner_app.local_ai_runtime_state import (
        runtime_local_ai_configuration_snapshot,
    )

    snapshot = runtime_local_ai_configuration_snapshot()
    return DEFAULT_OLLAMA_BASE_URL if snapshot is None else snapshot.base_url
