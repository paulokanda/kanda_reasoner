"""File helpers for prompt-router reasoner review advisory artifacts."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping
from uuid import uuid4

from .prompt_router_reasoner_review_models import (
    ASK_AI_ANSWERS_FOLDER_NAME,
    ASK_AI_REQUESTS_FOLDER_NAME,
    EVENT_AI_SECOND_OPINION_SAVED,
    EVENT_ASK_AI_REQUEST_SAVED,
    SCHEMA_VERSION,
    VALID_HUMAN_LABELS,
    _atomic_write_text,
    _json_dumps,
    compute_ai_human_agreement,
    detect_ai_second_opinion_label,
    normalize_router_mode,
    utc_now_iso,
    PromptRouterReasonerValidationError,
)

class PromptRouterReasonerReviewStoreAdvisoryFilesMixin:
    """Mixin extracted from PromptRouterReasonerReviewStore during v7.2 refactor."""

    def save_ask_ai_request(
        self,
        review_item_id: str,
        request_text: str,
        *,
        router_mode_at_time: str | None = None,
    ) -> dict[str, Any]:
        """Save an editable Ask AI request for later external advisory review.

        This writes only to prompt_router_reasoner_reviews/ask_ai_requests and
        updates the compact review index with a relative request filename. It
        does not set or infer the human_label and does not touch router state,
        prompt libraries, freeze memory, or provider calls.
        """
        item = self.get_review_item(review_item_id)
        text = str(request_text or "").strip()
        if not text:
            raise PromptRouterReasonerValidationError("Ask AI request text is required")
        mode = normalize_router_mode(router_mode_at_time or item.get("router_mode_at_capture"))
        now = utc_now_iso()
        safe_timestamp = now.replace(":", "").replace("-", "").replace("Z", "Z")
        short_id = str(review_item_id).replace("prr_", "")[:12] or "review"
        base_name = "ask_ai_review_" + short_id + "_" + safe_timestamp
        text_relative = ASK_AI_REQUESTS_FOLDER_NAME + "/" + base_name + ".txt"
        json_relative = ASK_AI_REQUESTS_FOLDER_NAME + "/" + base_name + ".json"
        text_path = self.review_dir / text_relative
        json_path = self.review_dir / json_relative
        metadata = {
            "schema_version": SCHEMA_VERSION,
            "kind": "prompt_router_reasoner_ask_ai_request",
            "review_item_id": review_item_id,
            "generator_text_id": str(item.get("generator_text_id", "")),
            "generator_text_hash": str(item.get("generator_text_hash", "")),
            "heuristic_prompt_id": str((item.get("heuristic_prompt") or {}).get("prompt_id", "")),
            "heuristic_prompt_hash": str((item.get("heuristic_prompt") or {}).get("prompt_hash", "")),
            "ml_prompt_id": str((item.get("ml_prompt") or {}).get("prompt_id", "")),
            "ml_prompt_hash": str((item.get("ml_prompt") or {}).get("prompt_hash", "")),
            "current_human_label": item.get("human_label"),
            "router_mode_at_time": mode,
            "created_at": now,
            "saved_by_user": True,
            "copied_by_user": False,
            "ask_ai_prompt_file": text_relative,
            "ask_ai_metadata_file": json_relative,
            "related_ai_answer_file": None,
        }
        _atomic_write_text(text_path, text + "\n")
        _atomic_write_text(json_path, _json_dumps(metadata, indent=2))
        event_id = "evt_" + uuid4().hex
        event = {
            "schema_version": SCHEMA_VERSION,
            "event_id": event_id,
            "event_type": EVENT_ASK_AI_REQUEST_SAVED,
            "review_item_id": review_item_id,
            "created_at": now,
            "text_file": text_relative,
            "metadata_file": json_relative,
            "router_mode_at_time": mode,
        }
        self._append_event(event)
        current_files = list(item.get("ask_ai_request_files") or [])
        if text_relative not in current_files:
            current_files.append(text_relative)
        item.update(
            {
                "ask_ai_request_files": current_files,
                "updated_at": now,
                "last_event_id": event_id,
            }
        )
        self._index["items"][review_item_id] = item
        self._write_index()
        return {
            "text_file": text_relative,
            "metadata_file": json_relative,
            "text_path": str(text_path),
            "metadata_path": str(json_path),
            "metadata": metadata,
        }

    def save_ai_second_opinion(
        self,
        review_item_id: str,
        answer_text: str,
        *,
        source: str = "manual_paste",
        ai_answer_label_detected: str | None = None,
        ai_confidence_if_present: str | float | None = None,
    ) -> dict[str, Any]:
        """Save a pasted external AI answer as advisory second-opinion evidence.

        This writes only to prompt_router_reasoner_reviews/ask_ai_answers and
        updates ai_second_opinion_files in the compact review index. It never
        sets human_label, never changes review_status, never changes router
        mode, and never gives the pasted AI answer authority over routing.
        """
        item = self.get_review_item(review_item_id)
        text = str(answer_text or "").strip()
        if not text:
            raise PromptRouterReasonerValidationError("AI second-opinion answer text is required")
        detected_label = ai_answer_label_detected or detect_ai_second_opinion_label(text)
        if detected_label not in VALID_HUMAN_LABELS and detected_label != "unknown":
            detected_label = "unknown"
        human_label = item.get("human_label")
        agreement = compute_ai_human_agreement(detected_label, human_label)
        now = utc_now_iso()
        safe_timestamp = now.replace(":", "").replace("-", "").replace("Z", "Z")
        short_id = str(review_item_id).replace("prr_", "")[:12] or "review"
        base_name = "ai_second_opinion_" + short_id + "_" + safe_timestamp
        text_relative = ASK_AI_ANSWERS_FOLDER_NAME + "/" + base_name + ".txt"
        json_relative = ASK_AI_ANSWERS_FOLDER_NAME + "/" + base_name + ".json"
        text_path = self.review_dir / text_relative
        json_path = self.review_dir / json_relative
        metadata = {
            "schema_version": SCHEMA_VERSION,
            "kind": "prompt_router_reasoner_ai_second_opinion",
            "review_item_id": review_item_id,
            "generator_text_id": str(item.get("generator_text_id", "")),
            "generator_text_hash": str(item.get("generator_text_hash", "")),
            "heuristic_prompt_id": str((item.get("heuristic_prompt") or {}).get("prompt_id", "")),
            "heuristic_prompt_hash": str((item.get("heuristic_prompt") or {}).get("prompt_hash", "")),
            "ml_prompt_id": str((item.get("ml_prompt") or {}).get("prompt_id", "")),
            "ml_prompt_hash": str((item.get("ml_prompt") or {}).get("prompt_hash", "")),
            "ai_answer_label_detected": detected_label,
            "human_final_label": human_label,
            "ai_agrees_with_human": agreement,
            "ai_confidence_if_present": ai_confidence_if_present,
            "source": str(source or "manual_paste"),
            "created_at": now,
            "ai_answer_file": text_relative,
            "ai_answer_metadata_file": json_relative,
            "advisory_only": True,
        }
        _atomic_write_text(text_path, text + "\n")
        _atomic_write_text(json_path, _json_dumps(metadata, indent=2))
        event_id = "evt_" + uuid4().hex
        event = {
            "schema_version": SCHEMA_VERSION,
            "event_id": event_id,
            "event_type": EVENT_AI_SECOND_OPINION_SAVED,
            "review_item_id": review_item_id,
            "created_at": now,
            "text_file": text_relative,
            "metadata_file": json_relative,
            "ai_answer_label_detected": detected_label,
            "ai_agrees_with_human": agreement,
            "source": str(source or "manual_paste"),
        }
        self._append_event(event)
        current_files = list(item.get("ai_second_opinion_files") or [])
        if text_relative not in current_files:
            current_files.append(text_relative)
        item.update(
            {
                "ai_second_opinion_files": current_files,
                "latest_ai_second_opinion_label": detected_label,
                "latest_ai_agrees_with_human": agreement,
                "updated_at": now,
                "last_event_id": event_id,
            }
        )
        self._index["items"][review_item_id] = item
        self._write_index()
        return {
            "text_file": text_relative,
            "metadata_file": json_relative,
            "text_path": str(text_path),
            "metadata_path": str(json_path),
            "metadata": metadata,
        }

    def write_stats_cache(self, stats: Mapping[str, Any]) -> None:
        """Persist a stats snapshot without mutating review history."""
        payload = {
            "schema_version": SCHEMA_VERSION,
            "kind": "prompt_router_reasoner_stats_cache",
            "updated_at": utc_now_iso(),
            "stats": dict(stats),
        }
        _atomic_write_text(self.stats_file, _json_dumps(payload, indent=2))

    def expected_storage_paths(self) -> tuple[Path, ...]:
        """Return the only project paths this store is expected to create or write."""
        return (
            self.review_dir,
            self.log_file,
            self.index_file,
            self.stats_file,
            self.ask_ai_requests_dir,
            self.ask_ai_answers_dir,
            self.export_datasets_dir,
            self.import_datasets_dir,
        )
