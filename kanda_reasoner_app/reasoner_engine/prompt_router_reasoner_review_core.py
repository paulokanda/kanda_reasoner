"""Core review logic for prompt-router reasoner records."""

from __future__ import annotations

import csv
import io
import json
from pathlib import Path
from typing import Any, Mapping
from uuid import uuid4

from .prompt_router_reasoner_review_models import (
    AGREEMENT_AGREE,
    AGREEMENT_DISAGREE,
    ASK_AI_ANSWERS_FOLDER_NAME,
    ASK_AI_REQUESTS_FOLDER_NAME,
    EVENT_AI_SECOND_OPINION_SAVED,
    EVENT_ASK_AI_REQUEST_SAVED,
    EVENT_PENDING_CREATED,
    EVENT_REVIEW_DATASET_IMPORTED,
    EVENT_REVIEW_SAVED,
    EVENT_REVIEW_UNDONE,
    EXPORT_DATASETS_FOLDER_NAME,
    IMPORT_DATASETS_FOLDER_NAME,
    FORBIDDEN_REVIEW_STORE_PATH_FRAGMENTS,
    LABEL_BOTH_ACCEPTABLE_UNCLEAR,
    LABEL_HEURISTICS_CORRECT,
    LABEL_ML_CORRECT,
    REVIEW_FOLDER_NAME,
    REVIEW_INDEX_FILENAME,
    REVIEW_LOG_FILENAME,
    REVIEW_STATS_FILENAME,
    ROUTER_WITH_HELP_OF_ML,
    ROUTER_WITH_HEURISTICS,
    ROUTER_WITH_ML,
    SCHEMA_VERSION,
    STATUS_PENDING,
    STATUS_REVIEWED,
    VALID_AGREEMENT_STATUSES,
    VALID_EVENT_TYPES,
    VALID_HUMAN_LABELS,
    VALID_REVIEW_STATUSES,
    _atomic_write_text,
    _ensure_prompt_snapshot,
    _json_dumps,
    _read_json_object,
    compact_generator_text,
    compute_ai_human_agreement,
    detect_ai_second_opinion_label,
    normalize_human_label,
    normalize_agreement_status,
    normalize_router_mode,
    sha256_text,
    utc_now_iso,
    PromptRouterReasonerItemNotFoundError,
    PromptRouterReasonerStoreError,
    PromptRouterReasonerValidationError,
    PromptSnapshot,
)

class PromptRouterReasonerReviewStoreCoreMixin:
    """Mixin extracted from PromptRouterReasonerReviewStore during v7.2 refactor."""

    def __init__(self, project_root: str | Path) -> None:
        self.project_root = Path(project_root).expanduser().resolve()
        self.review_dir = self.project_root / REVIEW_FOLDER_NAME
        self.log_file = self.review_dir / REVIEW_LOG_FILENAME
        self.index_file = self.review_dir / REVIEW_INDEX_FILENAME
        self.stats_file = self.review_dir / REVIEW_STATS_FILENAME
        self.ask_ai_requests_dir = self.review_dir / ASK_AI_REQUESTS_FOLDER_NAME
        self.ask_ai_answers_dir = self.review_dir / ASK_AI_ANSWERS_FOLDER_NAME
        self.export_datasets_dir = self.review_dir / EXPORT_DATASETS_FOLDER_NAME
        self.import_datasets_dir = self.review_dir / IMPORT_DATASETS_FOLDER_NAME
        self._validate_storage_boundary()
        self._ensure_storage()
        self._index = self._load_or_rebuild_index()

    def _validate_storage_boundary(self) -> None:
        relative = self.review_dir.relative_to(self.project_root)
        relative_lowered = str(relative).replace("\\", "/").lower()
        absolute_parts = {part.lower() for part in self.review_dir.parts}
        for fragment in FORBIDDEN_REVIEW_STORE_PATH_FRAGMENTS:
            fragment_lowered = fragment.lower()
            if fragment_lowered in relative_lowered or fragment_lowered in absolute_parts:
                raise PromptRouterReasonerStoreError(
                    "Prompt Router Reasoner review data must not be stored in: " + fragment
                )

    def _ensure_storage(self) -> None:
        self.review_dir.mkdir(parents=True, exist_ok=True)
        self.ask_ai_requests_dir.mkdir(parents=True, exist_ok=True)
        self.ask_ai_answers_dir.mkdir(parents=True, exist_ok=True)
        self.export_datasets_dir.mkdir(parents=True, exist_ok=True)
        self.import_datasets_dir.mkdir(parents=True, exist_ok=True)
        if not self.log_file.exists():
            self.log_file.write_text("", encoding="utf-8", newline="\n")
        if not self.index_file.exists():
            self._write_index({})
        if not self.stats_file.exists():
            _atomic_write_text(
                self.stats_file,
                _json_dumps(
                    {
                        "schema_version": SCHEMA_VERSION,
                        "kind": "prompt_router_reasoner_stats_cache",
                        "updated_at": utc_now_iso(),
                        "stats": {},
                    },
                    indent=2,
                ),
            )

    def _load_or_rebuild_index(self) -> dict[str, Any]:
        try:
            index = _read_json_object(self.index_file)
        except PromptRouterReasonerStoreError:
            index = {}
        if not index.get("items") and self.log_file.exists() and self.log_file.stat().st_size > 0:
            return self.rebuild_index_from_log()
        return self._normalize_index(index)

    def _normalize_index(self, index: Mapping[str, Any]) -> dict[str, Any]:
        items = index.get("items", {})
        if not isinstance(items, dict):
            items = {}
        return {
            "schema_version": SCHEMA_VERSION,
            "kind": "prompt_router_reasoner_review_index",
            "updated_at": str(index.get("updated_at", utc_now_iso())),
            "items": dict(items),
        }

    def _write_index(self, index: Mapping[str, Any] | None = None) -> None:
        if index is None:
            index = self._index
        normalized = self._normalize_index(index)
        normalized["updated_at"] = utc_now_iso()
        _atomic_write_text(self.index_file, _json_dumps(normalized, indent=2))

    def _append_event(self, event: Mapping[str, Any]) -> None:
        with self.log_file.open("a", encoding="utf-8", newline="\n") as handle:
            handle.write(_json_dumps(event, indent=None))

    def iter_events(self) -> list[dict[str, Any]]:
        """Return all valid events from the JSONL log."""
        events: list[dict[str, Any]] = []
        if not self.log_file.exists():
            return events
        for line_number, line in enumerate(self.log_file.read_text(encoding="utf-8-sig").splitlines(), 1):
            text = line.strip()
            if not text:
                continue
            try:
                loaded = json.loads(text)
            except json.JSONDecodeError as exc:
                raise PromptRouterReasonerStoreError(
                    "Invalid JSONL event at line " + str(line_number)
                ) from exc
            if not isinstance(loaded, dict):
                raise PromptRouterReasonerStoreError(
                    "JSONL event is not an object at line " + str(line_number)
                )
            events.append(dict(loaded))
        return events

    def rebuild_index_from_log(self) -> dict[str, Any]:
        """Rebuild the compact current-state index from append-only events."""
        items: dict[str, Any] = {}
        for event in self.iter_events():
            event_type = str(event.get("event_type", ""))
            review_item_id = str(event.get("review_item_id", ""))
            if not review_item_id:
                continue
            if event_type == EVENT_PENDING_CREATED:
                item = dict(event.get("review_item", {}))
                if item:
                    items[review_item_id] = item
            elif event_type == EVENT_REVIEW_DATASET_IMPORTED:
                item = dict(event.get("review_item", {}))
                if item:
                    items[review_item_id] = item
            elif event_type == EVENT_REVIEW_SAVED and review_item_id in items:
                items[review_item_id].update(
                    {
                        "review_status": STATUS_REVIEWED,
                        "human_label": str(event.get("human_label", "")),
                        "router_mode_at_review": str(event.get("router_mode_at_review", "")),
                        "reviewed_at": str(event.get("created_at", "")),
                        "updated_at": str(event.get("created_at", "")),
                        "undo_available": True,
                        "last_event_id": str(event.get("event_id", "")),
                    }
                )
            elif event_type == EVENT_REVIEW_UNDONE and review_item_id in items:
                items[review_item_id].update(
                    {
                        "review_status": STATUS_PENDING,
                        "human_label": None,
                        "router_mode_at_review": None,
                        "reviewed_at": None,
                        "updated_at": str(event.get("created_at", "")),
                        "undo_available": False,
                        "last_event_id": str(event.get("event_id", "")),
                    }
                )
            elif event_type == EVENT_ASK_AI_REQUEST_SAVED and review_item_id in items:
                current_files = list(items[review_item_id].get("ask_ai_request_files") or [])
                text_file = str(event.get("text_file", ""))
                if text_file and text_file not in current_files:
                    current_files.append(text_file)
                items[review_item_id].update(
                    {
                        "ask_ai_request_files": current_files,
                        "updated_at": str(event.get("created_at", "")),
                        "last_event_id": str(event.get("event_id", "")),
                    }
                )
            elif event_type == EVENT_AI_SECOND_OPINION_SAVED and review_item_id in items:
                current_files = list(items[review_item_id].get("ai_second_opinion_files") or [])
                text_file = str(event.get("text_file", ""))
                if text_file and text_file not in current_files:
                    current_files.append(text_file)
                items[review_item_id].update(
                    {
                        "ai_second_opinion_files": current_files,
                        "latest_ai_second_opinion_label": event.get("ai_answer_label_detected"),
                        "latest_ai_agrees_with_human": event.get("ai_agrees_with_human"),
                        "updated_at": str(event.get("created_at", "")),
                        "last_event_id": str(event.get("event_id", "")),
                    }
                )
        self._index = {
            "schema_version": SCHEMA_VERSION,
            "kind": "prompt_router_reasoner_review_index",
            "updated_at": utc_now_iso(),
            "items": items,
        }
        self._write_index(self._index)
        return self._index

    def create_pending_review(
        self,
        *,
        full_generator_text: str,
        heuristic_prompt: PromptSnapshot | Mapping[str, Any],
        ml_prompt: PromptSnapshot | Mapping[str, Any],
        generator_text_id: str | None = None,
        short_generator_text: str | None = None,
        router_mode_at_capture: str | None = None,
        app_version: str = "",
        router_version: str = "",
        retriever_version: str = "",
        ml_version: str = "",
        prompt_library_version: str = "",
        safety_violation: bool = False,
        notes: str = "",
    ) -> str:
        """Create a pending review item and return its stable review item id."""
        text = str(full_generator_text or "")
        if not text.strip():
            raise PromptRouterReasonerValidationError("full_generator_text is required")

        heuristic = _ensure_prompt_snapshot(heuristic_prompt, "heuristic_prompt")
        ml = _ensure_prompt_snapshot(ml_prompt, "ml_prompt")
        agreement_status = (
            AGREEMENT_AGREE
            if heuristic.prompt_hash == ml.prompt_hash or heuristic.prompt_id == ml.prompt_id
            else AGREEMENT_DISAGREE
        )
        created_at = utc_now_iso()
        review_sequence = self._next_review_sequence()
        review_item_id = "prr_" + uuid4().hex
        generator_id = str(generator_text_id or "gen_" + uuid4().hex).strip()
        compact_text = str(short_generator_text or compact_generator_text(text)).strip()
        item = {
            "schema_version": SCHEMA_VERSION,
            "review_item_id": review_item_id,
            "generator_text_id": generator_id,
            "full_generator_text": text,
            "short_generator_text": compact_text,
            "generator_text_hash": sha256_text(text),
            "created_at": created_at,
            "updated_at": created_at,
            "review_sequence": review_sequence,
            "reviewed_at": None,
            "review_status": STATUS_PENDING,
            "agreement_status": agreement_status,
            "heuristic_prompt": heuristic.to_dict(),
            "ml_prompt": ml.to_dict(),
            "router_mode_at_capture": normalize_router_mode(router_mode_at_capture),
            "router_mode_at_review": None,
            "human_label": None,
            "undo_available": False,
            "safety_violation": bool(safety_violation),
            "app_version": str(app_version),
            "router_version": str(router_version),
            "retriever_version": str(retriever_version),
            "ml_version": str(ml_version),
            "prompt_library_version": str(prompt_library_version),
            "ask_ai_request_files": [],
            "ai_second_opinion_files": [],
            "latest_ai_second_opinion_label": None,
            "latest_ai_agrees_with_human": None,
            "notes": str(notes),
            "last_event_id": "",
        }
        self._validate_review_item(item)
        event_id = "evt_" + uuid4().hex
        item["last_event_id"] = event_id
        event = {
            "schema_version": SCHEMA_VERSION,
            "event_id": event_id,
            "event_type": EVENT_PENDING_CREATED,
            "review_item_id": review_item_id,
            "created_at": created_at,
            "review_item": item,
        }
        self._append_event(event)
        self._index["items"][review_item_id] = item
        self._write_index()
        return review_item_id

    def save_review(
        self,
        review_item_id: str,
        human_label: str,
        *,
        router_mode_at_review: str | None = None,
    ) -> dict[str, Any]:
        """Save a human label for a review item and keep undo available."""
        item = self.get_review_item(review_item_id)
        label = normalize_human_label(human_label)
        mode = normalize_router_mode(router_mode_at_review or item.get("router_mode_at_capture"))
        now = utc_now_iso()
        event_id = "evt_" + uuid4().hex
        event = {
            "schema_version": SCHEMA_VERSION,
            "event_id": event_id,
            "event_type": EVENT_REVIEW_SAVED,
            "review_item_id": review_item_id,
            "created_at": now,
            "human_label": label,
            "router_mode_at_review": mode,
        }
        self._append_event(event)
        item.update(
            {
                "review_status": STATUS_REVIEWED,
                "human_label": label,
                "router_mode_at_review": mode,
                "reviewed_at": now,
                "updated_at": now,
                "undo_available": True,
                "last_event_id": event_id,
            }
        )
        self._index["items"][review_item_id] = item
        self._write_index()
        return dict(item)

    def undo_last_save(self, review_item_id: str) -> dict[str, Any]:
        """Undo the latest saved label for one review item."""
        item = self.get_review_item(review_item_id)
        if item.get("review_status") != STATUS_REVIEWED or not item.get("undo_available"):
            raise PromptRouterReasonerStoreError("Review item is not undoable: " + review_item_id)
        now = utc_now_iso()
        event_id = "evt_" + uuid4().hex
        event = {
            "schema_version": SCHEMA_VERSION,
            "event_id": event_id,
            "event_type": EVENT_REVIEW_UNDONE,
            "review_item_id": review_item_id,
            "created_at": now,
            "undone_label": item.get("human_label"),
        }
        self._append_event(event)
        item.update(
            {
                "review_status": STATUS_PENDING,
                "human_label": None,
                "router_mode_at_review": None,
                "reviewed_at": None,
                "updated_at": now,
                "undo_available": False,
                "last_event_id": event_id,
            }
        )
        self._index["items"][review_item_id] = item
        self._write_index()
        return dict(item)

    def get_review_item(self, review_item_id: str) -> dict[str, Any]:
        """Return a current-state review item from the compact index."""
        item = self._index.get("items", {}).get(str(review_item_id))
        if not isinstance(item, dict):
            raise PromptRouterReasonerItemNotFoundError(review_item_id)
        return dict(item)

    def list_review_items(
        self,
        *,
        review_status: str | None = None,
        agreement_status: str | None = None,
        human_label: str | None = None,
    ) -> list[dict[str, Any]]:
        """List current-state review items with optional filters."""
        items = list(self._index.get("items", {}).values())
        result: list[dict[str, Any]] = []
        for item in items:
            if review_status is not None and item.get("review_status") != review_status:
                continue
            if agreement_status is not None and item.get("agreement_status") != agreement_status:
                continue
            if human_label is not None and item.get("human_label") != human_label:
                continue
            result.append(dict(item))
        result.sort(key=self._review_item_order_key)
        return result

    def _next_review_sequence(self) -> int:
        """Return the next monotonic local review sequence for tie-safe display order."""
        values: list[int] = []
        for existing in self._index.get("items", {}).values():
            if not isinstance(existing, Mapping):
                continue
            try:
                values.append(int(existing.get("review_sequence", 0)))
            except (TypeError, ValueError):
                continue
        return (max(values) if values else 0) + 1

    @staticmethod
    def _review_item_order_key(item: Mapping[str, Any]) -> tuple[str, int, str]:
        """Sort review rows by capture time, then monotonic store sequence, then ID."""
        try:
            sequence = int(item.get("review_sequence", 0))
        except (TypeError, ValueError):
            sequence = 0
        return (str(item.get("created_at", "")), sequence, str(item.get("review_item_id", "")))

    def _validate_review_item(self, item: Mapping[str, Any]) -> None:
        required = (
            "schema_version",
            "review_item_id",
            "generator_text_id",
            "full_generator_text",
            "short_generator_text",
            "generator_text_hash",
            "review_status",
            "agreement_status",
            "heuristic_prompt",
            "ml_prompt",
            "router_mode_at_capture",
        )
        missing = [name for name in required if item.get(name) in (None, "", {}, [])]
        if missing:
            raise PromptRouterReasonerValidationError(
                "Review item missing required fields: " + ", ".join(missing)
            )
        if item.get("schema_version") != SCHEMA_VERSION:
            raise PromptRouterReasonerValidationError("Unsupported schema_version")
        if item.get("review_status") not in VALID_REVIEW_STATUSES:
            raise PromptRouterReasonerValidationError("Invalid review_status")
        if item.get("agreement_status") not in VALID_AGREEMENT_STATUSES:
            raise PromptRouterReasonerValidationError("Invalid agreement_status")
        normalize_router_mode(str(item.get("router_mode_at_capture")))
