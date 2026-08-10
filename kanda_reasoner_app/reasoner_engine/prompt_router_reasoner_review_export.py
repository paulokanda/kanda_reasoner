"""Export helpers for prompt-router reasoner review records."""

from __future__ import annotations

import csv
import io
import json
from typing import Any, Mapping

from .prompt_router_reasoner_review_models import (
    EXPORT_DATASETS_FOLDER_NAME,
    REVIEW_INDEX_FILENAME,
    SCHEMA_VERSION,
    STATUS_PENDING,
    STATUS_REVIEWED,
    VALID_HUMAN_LABELS,
    _atomic_write_text,
    _json_dumps,
    utc_now_iso,
)

class PromptRouterReasonerReviewStoreExportMixin:
    """Mixin extracted from PromptRouterReasonerReviewStore during v7.2 refactor."""

    def export_review_dataset(self) -> dict[str, Any]:
        """Export a project-local review dataset snapshot as JSONL, CSV, and metadata.

        Exporting is read-only with respect to review history: it does not
        append review events, does not change labels, and does not mutate router
        behavior. Files are written only under prompt_router_reasoner_reviews/
        export_review_datasets for manual inspection, backup, or later ML
        analysis.
        """
        items = self.list_review_items()
        rows = [self._review_item_to_export_row(item) for item in items]
        exported_at = utc_now_iso()
        safe_timestamp = exported_at.replace(":", "").replace("-", "").replace("Z", "Z")
        base_name = "prompt_router_reasoner_review_dataset_" + safe_timestamp
        jsonl_relative = EXPORT_DATASETS_FOLDER_NAME + "/" + base_name + ".jsonl"
        csv_relative = EXPORT_DATASETS_FOLDER_NAME + "/" + base_name + ".csv"
        metadata_relative = EXPORT_DATASETS_FOLDER_NAME + "/" + base_name + ".json"
        jsonl_path = self.review_dir / jsonl_relative
        csv_path = self.review_dir / csv_relative
        metadata_path = self.review_dir / metadata_relative

        jsonl_text = "".join(_json_dumps(row, indent=None) for row in rows)
        fields = list(self._export_fieldnames())
        csv_buffer = io.StringIO(newline="")
        writer = csv.DictWriter(csv_buffer, fieldnames=fields, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})

        reviewed_count = sum(1 for row in rows if row.get("review_status") == STATUS_REVIEWED)
        pending_count = sum(1 for row in rows if row.get("review_status") == STATUS_PENDING)
        training_ready_count = sum(1 for row in rows if row.get("is_training_ready") is True)
        label_counts: dict[str, int] = {}
        agreement_counts: dict[str, int] = {}
        for row in rows:
            label = str(row.get("human_label") or "unlabeled")
            label_counts[label] = label_counts.get(label, 0) + 1
            agreement = str(row.get("agreement_status") or "unknown")
            agreement_counts[agreement] = agreement_counts.get(agreement, 0) + 1

        latest_metadata_relative = EXPORT_DATASETS_FOLDER_NAME + "/latest_prompt_router_reasoner_review_dataset.json"
        latest_metadata_path = self.review_dir / latest_metadata_relative
        export_folder_relative = EXPORT_DATASETS_FOLDER_NAME
        artifact_files = (jsonl_relative, csv_relative, metadata_relative, latest_metadata_relative)
        summary_text = (
            "Prompt Router Reasoner review dataset export: "
            + str(len(rows))
            + " row(s), "
            + str(reviewed_count)
            + " reviewed, "
            + str(pending_count)
            + " pending, "
            + str(training_ready_count)
            + " training-ready."
        )
        metadata = {
            "schema_version": SCHEMA_VERSION,
            "kind": "prompt_router_reasoner_export_review_dataset",
            "exported_at": exported_at,
            "row_count": len(rows),
            "reviewed_count": reviewed_count,
            "pending_count": pending_count,
            "training_ready_count": training_ready_count,
            "label_counts": label_counts,
            "agreement_counts": agreement_counts,
            "jsonl_file": jsonl_relative,
            "csv_file": csv_relative,
            "metadata_file": metadata_relative,
            "latest_metadata_file": latest_metadata_relative,
            "export_folder": export_folder_relative,
            "artifact_files": list(artifact_files),
            "fields": fields,
            "advisory_only": True,
            "source_index_file": REVIEW_INDEX_FILENAME,
            "history_unchanged": True,
            "labels_overwritten": False,
            "router_changed": False,
            "summary_text": summary_text,
        }
        _atomic_write_text(jsonl_path, jsonl_text)
        _atomic_write_text(csv_path, csv_buffer.getvalue())
        _atomic_write_text(metadata_path, _json_dumps(metadata, indent=2))
        _atomic_write_text(latest_metadata_path, _json_dumps(metadata, indent=2))
        return {
            "jsonl_file": jsonl_relative,
            "csv_file": csv_relative,
            "metadata_file": metadata_relative,
            "latest_metadata_file": latest_metadata_relative,
            "export_folder": export_folder_relative,
            "artifact_files": tuple(artifact_files),
            "jsonl_path": str(jsonl_path),
            "csv_path": str(csv_path),
            "metadata_path": str(metadata_path),
            "latest_metadata_path": str(latest_metadata_path),
            "export_folder_path": str(self.export_datasets_dir),
            "artifact_paths": (str(jsonl_path), str(csv_path), str(metadata_path), str(latest_metadata_path)),
            "summary_text": summary_text,
            "metadata": metadata,
            "rows": rows,
        }

    def list_exported_review_datasets(self, *, limit: int = 20) -> tuple[dict[str, Any], ...]:
        """Return recent export metadata records without mutating review history."""
        if not self.export_datasets_dir.exists():
            return ()
        records: list[dict[str, Any]] = []
        for metadata_path in self.export_datasets_dir.glob("*.json"):
            if metadata_path.name == "latest_prompt_router_reasoner_review_dataset.json":
                continue
            try:
                metadata = json.loads(metadata_path.read_text(encoding="utf-8-sig"))
            except Exception:
                continue
            if not isinstance(metadata, Mapping):
                continue
            if metadata.get("kind") != "prompt_router_reasoner_export_review_dataset":
                continue
            record = {
                "metadata_file": self._relative_review_path(metadata_path),
                "metadata_path": str(metadata_path),
                "jsonl_file": str(metadata.get("jsonl_file", "")),
                "csv_file": str(metadata.get("csv_file", "")),
                "exported_at": str(metadata.get("exported_at", "")),
                "row_count": int(metadata.get("row_count", 0) or 0),
                "reviewed_count": int(metadata.get("reviewed_count", 0) or 0),
                "pending_count": int(metadata.get("pending_count", 0) or 0),
                "training_ready_count": int(metadata.get("training_ready_count", 0) or 0),
                "summary_text": str(metadata.get("summary_text", "")),
            }
            records.append(record)
        records.sort(key=lambda value: (str(value.get("exported_at", "")), str(value.get("metadata_file", ""))), reverse=True)
        return tuple(records[: max(0, int(limit))])

    def _review_item_to_export_row(self, item: Mapping[str, Any]) -> dict[str, Any]:
        heuristic = item.get("heuristic_prompt") if isinstance(item.get("heuristic_prompt"), Mapping) else {}
        ml = item.get("ml_prompt") if isinstance(item.get("ml_prompt"), Mapping) else {}
        human_label = item.get("human_label")
        review_status = str(item.get("review_status", ""))
        row: dict[str, Any] = {
            "schema_version": SCHEMA_VERSION,
            "review_item_id": str(item.get("review_item_id", "")),
            "generator_text_id": str(item.get("generator_text_id", "")),
            "generator_text_hash": str(item.get("generator_text_hash", "")),
            "short_generator_text": str(item.get("short_generator_text", "")),
            "full_generator_text": str(item.get("full_generator_text", "")),
            "created_at": str(item.get("created_at", "")),
            "updated_at": str(item.get("updated_at", "")),
            "review_sequence": item.get("review_sequence", ""),
            "reviewed_at": str(item.get("reviewed_at") or ""),
            "review_status": review_status,
            "agreement_status": str(item.get("agreement_status", "")),
            "router_mode_at_capture": str(item.get("router_mode_at_capture", "")),
            "router_mode_at_review": str(item.get("router_mode_at_review") or ""),
            "human_label": str(human_label or ""),
            "training_label": str(human_label or "") if review_status == STATUS_REVIEWED else "",
            "is_training_ready": bool(review_status == STATUS_REVIEWED and human_label in VALID_HUMAN_LABELS),
            "undo_available": bool(item.get("undo_available", False)),
            "safety_violation": bool(item.get("safety_violation", False)),
            "app_version": str(item.get("app_version", "")),
            "router_version": str(item.get("router_version", "")),
            "retriever_version": str(item.get("retriever_version", "")),
            "ml_version": str(item.get("ml_version", "")),
            "prompt_library_version": str(item.get("prompt_library_version", "")),
            "ask_ai_request_count": len(list(item.get("ask_ai_request_files") or [])),
            "ai_second_opinion_count": len(list(item.get("ai_second_opinion_files") or [])),
            "latest_ai_second_opinion_label": str(item.get("latest_ai_second_opinion_label") or ""),
            "latest_ai_agrees_with_human": str(item.get("latest_ai_agrees_with_human") or ""),
            "notes": str(item.get("notes", "")),
        }
        row.update(self._prompt_export_fields(heuristic, "heuristic"))
        row.update(self._prompt_export_fields(ml, "ml"))
        return row

    @staticmethod
    def _prompt_export_fields(prompt: Mapping[str, Any], prefix: str) -> dict[str, Any]:
        keywords = prompt.get("keywords") or []
        if isinstance(keywords, (list, tuple)):
            keyword_text = ", ".join(str(value) for value in keywords)
        else:
            keyword_text = str(keywords)
        return {
            prefix + "_prompt_id": str(prompt.get("prompt_id", "")),
            prefix + "_prompt_name": str(prompt.get("prompt_name", "")),
            prefix + "_prompt_path": str(prompt.get("prompt_path", "")),
            prefix + "_prompt_hash": str(prompt.get("prompt_hash", "")),
            prefix + "_prompt_summary": str(prompt.get("prompt_summary", "")),
            prefix + "_prompt_group": str(prompt.get("prompt_group", "")),
            prefix + "_prompt_version": str(prompt.get("prompt_version", "")),
            prefix + "_score": "" if prompt.get("score") is None else prompt.get("score"),
            prefix + "_confidence": "" if prompt.get("confidence") is None else prompt.get("confidence"),
            prefix + "_explanation": str(prompt.get("explanation", "")),
            prefix + "_keywords": keyword_text,
            prefix + "_route": str(prompt.get("route", "")),
            prefix + "_semantic_match": str(prompt.get("semantic_match", "")),
            prefix + "_inferred_intent": str(prompt.get("inferred_intent", "")),
            prefix + "_disagreement_reason": str(prompt.get("disagreement_reason", "")),
            prefix + "_safety_status": str(prompt.get("safety_status", "")),
        }

    @staticmethod
    def _export_fieldnames() -> tuple[str, ...]:
        base_fields = (
            "schema_version",
            "review_item_id",
            "generator_text_id",
            "generator_text_hash",
            "short_generator_text",
            "full_generator_text",
            "created_at",
            "updated_at",
            "review_sequence",
            "reviewed_at",
            "review_status",
            "agreement_status",
            "router_mode_at_capture",
            "router_mode_at_review",
            "human_label",
            "training_label",
            "is_training_ready",
            "undo_available",
            "safety_violation",
            "app_version",
            "router_version",
            "retriever_version",
            "ml_version",
            "prompt_library_version",
            "ask_ai_request_count",
            "ai_second_opinion_count",
            "latest_ai_second_opinion_label",
            "latest_ai_agrees_with_human",
            "notes",
        )
        prompt_fields = (
            "prompt_id",
            "prompt_name",
            "prompt_path",
            "prompt_hash",
            "prompt_summary",
            "prompt_group",
            "prompt_version",
            "score",
            "confidence",
            "explanation",
            "keywords",
            "route",
            "semantic_match",
            "inferred_intent",
            "disagreement_reason",
            "safety_status",
        )
        return base_fields + tuple("heuristic_" + field for field in prompt_fields) + tuple("ml_" + field for field in prompt_fields)
