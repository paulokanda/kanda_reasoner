"""Support V10 project reasoning and evidence handling."""
from __future__ import annotations


__all__ = [
    "V9QwenAIModels",
]

# developer_tools/kanda_reasoner_app/project_reasoner_v10/v10_qwen_ai_models.py

import hashlib
import json
import queue
import threading
from pathlib import Path
from typing import Any, Callable

import requests


OLLAMA_URL = "http://127.0.0.1:11434/v1/chat/completions"

FAST_MODEL = "qwen2.5-coder:7b"
SMART_MODEL = "qwen2.5-coder:32b"

AUTO_THRESHOLD = 3000
TIMEOUT = 600


class _LocalGovernanceStateReader:
    """
    Minimal local governance reader for V10 only.

    Expected JSON shape:
    {
        "mode": 0
    }

    If file is missing or invalid, mode 0 is used.
    """

    def __init__(self, state_path: Path) -> None:
        self.state_path = Path(state_path).expanduser().resolve()

    def get_mode(self) -> int:
        try:
            if not self.state_path.exists():
                return 0

            with open(self.state_path, "r", encoding="utf-8", errors="replace") as handle:
                data = json.load(handle)

            mode = data.get("mode", 0)
            return int(mode)
        except Exception:
            return 0


class _LocalDiskCache:
    """
    Tiny JSON-on-disk cache for V10 only.
    """

    def __init__(self) -> None:
        self._cache_dir = Path(__file__).resolve().parent / "_v10_cache"
        self._cache_dir.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()

    def set_cache_dir(self, cache_dir: Path) -> None:
        resolved = Path(cache_dir).expanduser().resolve()
        resolved.mkdir(parents=True, exist_ok=True)
        self._cache_dir = resolved

    def _key_to_path(self, key_data: dict[str, Any]) -> Path:
        stable_text = json.dumps(key_data, sort_keys=True, ensure_ascii=True)
        digest = hashlib.sha256(stable_text.encode("utf-8", errors="replace")).hexdigest()
        return self._cache_dir / (digest + ".json")

    def get(self, key_data: dict[str, Any]) -> Any | None:
        try:
            cache_path = self._key_to_path(key_data)
            if not cache_path.exists():
                return None

            with self._lock:
                with open(cache_path, "r", encoding="utf-8", errors="replace") as handle:
                    payload = json.load(handle)

            return payload.get("value")
        except Exception:
            return None

    def set_value(self, key_data: dict[str, Any], value: Any) -> None:
        try:
            cache_path = self._key_to_path(key_data)
            payload = {
                "key": key_data,
                "value": value,
            }

            with self._lock:
                with open(cache_path, "w", encoding="utf-8", errors="replace") as handle:
                    json.dump(payload, handle, ensure_ascii=False, indent=2)
        except Exception:
            pass


class _LocalAIRequestQueue:
    """
    Tiny single-worker background queue for V10 only.
    Prevents GUI freeze and serializes model calls.
    """

    _instance = None
    _instance_lock = threading.Lock()

    def __new__(cls):
        with cls._instance_lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._init_once()
        return cls._instance

    def _init_once(self) -> None:
        self._queue: queue.Queue[Callable[[], None]] = queue.Queue()
        self._worker = threading.Thread(target=self._worker_loop, daemon=True)
        self._worker.start()

    def _worker_loop(self) -> None:
        while True:
            task = self._queue.get()
            try:
                task()
            except Exception:
                pass
            finally:
                self._queue.task_done()

    def submit(self, task: Callable[[], None]) -> None:
        self._queue.put(task)


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

    def __init__(self) -> None:
        self._governance_state_path = (
            Path(__file__).resolve().parent / "governance_state.json"
        )
        self._cache = _LocalDiskCache()
        self._request_queue = _LocalAIRequestQueue()

    def set_cache_dir(self, cache_dir: Path) -> None:
        self._cache.set_cache_dir(Path(cache_dir).expanduser().resolve())

    def set_governance_state_path(self, state_path: Path) -> None:
        self._governance_state_path = Path(state_path).expanduser().resolve()

    def _choose_model(self, text: Any) -> str:
        if isinstance(text, list):
            content_len = sum(len(str(message.get("content", ""))) for message in text if isinstance(message, dict))
        else:
            content_len = len(str(text))
        return FAST_MODEL if content_len < AUTO_THRESHOLD else SMART_MODEL

    def _post(self, payload: dict[str, Any]) -> dict[str, Any]:
        response = requests.post(OLLAMA_URL, json=payload, timeout=TIMEOUT)
        response.raise_for_status()
        return response.json()

    def _get_governance_modifier(self) -> str:
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
                    OLLAMA_URL,
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
