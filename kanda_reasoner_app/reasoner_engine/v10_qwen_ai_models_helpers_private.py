# project-path: kanda_reasoner_app/reasoner_engine/v10_qwen_ai_models_helpers_private.py
"""Private local support helpers for V10 Qwen AI model access."""

from __future__ import annotations

import hashlib
import json
import queue
import threading
from pathlib import Path
from typing import Any, Callable

__all__: list[str] = []


class _LocalGovernanceStateReader:
    """Minimal local governance reader for V10 only."""

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
    """Tiny JSON-on-disk cache for V10 only."""

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
    """Tiny single-worker background queue for V10 only."""

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
