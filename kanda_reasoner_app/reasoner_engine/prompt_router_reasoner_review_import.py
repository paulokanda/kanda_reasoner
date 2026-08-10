"""Import helpers for prompt-router reasoner review records."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping
from uuid import uuid4

from .prompt_router_reasoner_review_models import (
    AGREEMENT_DISAGREE,
    EVENT_REVIEW_DATASET_IMPORTED,
    ROUTER_WITH_HEURISTICS,
    SCHEMA_VERSION,
    STATUS_PENDING,
    STATUS_REVIEWED,
    VALID_HUMAN_LABELS,
    VALID_REVIEW_STATUSES,
    compact_generator_text,
    normalize_human_label,
    normalize_agreement_status,
    normalize_router_mode,
    sha256_text,
    utc_now_iso,
    PromptRouterReasonerStoreError,
    PromptRouterReasonerValidationError,
    PromptSnapshot,
)

class PromptRouterReasonerReviewStoreImportMixin:
    """Mixin extracted from PromptRouterReasonerReviewStore during v7.2 refactor."""

    def preview_import_review_dataset(self, dataset_path: str | Path) -> dict[str, Any]:
        """Dry-run import of a project-local exported review dataset JSONL file."""
        return self.import_review_dataset(dataset_path, dry_run=True)

    def import_review_dataset(self, dataset_path: str | Path, *, dry_run: bool = True) -> dict[str, Any]:
        """Import missing review rows from a project-local JSONL export file.

        This importer is intentionally conservative. It accepts only JSONL files
        located under prompt_router_reasoner_reviews, skips existing review IDs,
        skips duplicate generator/prompt fingerprints, and never overwrites an
        existing human label or router state. Dry-run mode performs no writes.
        """
        source_path = self._resolve_import_dataset_path(dataset_path)
        rows = self._read_import_dataset_rows(source_path)
        existing_items = self._index.get("items", {}) if isinstance(self._index.get("items"), dict) else {}
        existing_ids = {str(key) for key in existing_items.keys()}
        existing_fingerprint_map = self._existing_review_fingerprint_map()
        existing_fingerprints = set(existing_fingerprint_map.keys())
        planned_items: list[dict[str, Any]] = []
        skipped_existing_ids: list[str] = []
        skipped_duplicate_ids: list[str] = []
        skipped_existing_conflicts: list[dict[str, Any]] = []
        skipped_duplicate_conflicts: list[dict[str, Any]] = []
        invalid_rows: list[dict[str, Any]] = []
        invalid_conflicts: list[dict[str, Any]] = []
        next_sequence = self._next_review_sequence()

        for row_number, row in enumerate(rows, 1):
            try:
                item = self._review_export_row_to_import_item(
                    row,
                    source_path=source_path,
                    review_sequence=next_sequence + len(planned_items),
                )
            except Exception as exc:
                invalid_row = {"row_number": row_number, "error": str(exc)}
                invalid_rows.append(invalid_row)
                invalid_conflicts.append(
                    self._import_conflict_record(
                        row_number=row_number,
                        review_item_id=str(row.get("review_item_id", "")),
                        reason="invalid_row",
                        incoming_row=row,
                        error=str(exc),
                    )
                )
                continue

            review_item_id = str(item.get("review_item_id", ""))
            if review_item_id in existing_ids:
                skipped_existing_ids.append(review_item_id)
                existing_item = existing_items.get(review_item_id, {})
                skipped_existing_conflicts.append(
                    self._import_conflict_record(
                        row_number=row_number,
                        review_item_id=review_item_id,
                        reason="existing_review_item_id",
                        incoming_item=item,
                        existing_item=existing_item if isinstance(existing_item, Mapping) else {},
                    )
                )
                continue
            fingerprint = self._review_item_import_fingerprint(item)
            if fingerprint in existing_fingerprints:
                skipped_duplicate_ids.append(review_item_id)
                matched_id = existing_fingerprint_map.get(fingerprint, "")
                existing_item = existing_items.get(matched_id, {})
                skipped_duplicate_conflicts.append(
                    self._import_conflict_record(
                        row_number=row_number,
                        review_item_id=review_item_id,
                        reason="duplicate_generator_prompt_fingerprint",
                        incoming_item=item,
                        existing_item=existing_item if isinstance(existing_item, Mapping) else {},
                        fingerprint=fingerprint,
                    )
                )
                continue
            planned_items.append(item)

        imported_count = 0
        if not dry_run and not invalid_rows:
            for item in planned_items:
                now = utc_now_iso()
                event_id = "evt_" + uuid4().hex
                item["last_event_id"] = event_id
                item["updated_at"] = str(item.get("updated_at") or now)
                event = {
                    "schema_version": SCHEMA_VERSION,
                    "event_id": event_id,
                    "event_type": EVENT_REVIEW_DATASET_IMPORTED,
                    "review_item_id": str(item.get("review_item_id", "")),
                    "created_at": now,
                    "source_file": self._relative_review_path(source_path),
                    "review_item": item,
                }
                self._append_event(event)
                self._index["items"][str(item.get("review_item_id", ""))] = item
                existing_fingerprints.add(self._review_item_import_fingerprint(item))
                imported_count += 1
            if imported_count:
                self._write_index()

        imported_or_would = len(planned_items) if dry_run else imported_count
        reviewed_count = sum(1 for item in planned_items if item.get("review_status") == STATUS_REVIEWED)
        pending_count = sum(1 for item in planned_items if item.get("review_status") == STATUS_PENDING)
        metadata = {
            "schema_version": SCHEMA_VERSION,
            "kind": "prompt_router_reasoner_import_review_dataset",
            "dry_run": bool(dry_run),
            "source_file": self._relative_review_path(source_path),
            "rows_seen": len(rows),
            "importable_count": len(planned_items),
            "imported_count": imported_count,
            "would_import_count": len(planned_items) if dry_run else 0,
            "skipped_existing_count": len(skipped_existing_ids),
            "skipped_duplicate_count": len(skipped_duplicate_ids),
            "invalid_count": len(invalid_rows),
            "conflict_count": len(skipped_existing_conflicts) + len(skipped_duplicate_conflicts) + len(invalid_conflicts),
            "skipped_existing_conflict_count": len(skipped_existing_conflicts),
            "skipped_duplicate_conflict_count": len(skipped_duplicate_conflicts),
            "invalid_conflict_count": len(invalid_conflicts),
            "reviewed_count": reviewed_count,
            "pending_count": pending_count,
            "history_changed": bool(imported_count),
            "labels_overwritten": False,
            "router_changed": False,
            "advisory_only": True,
            "import_policy": "missing_rows_only_skip_conflicts_never_overwrite",
        }
        conflict_records = skipped_existing_conflicts + skipped_duplicate_conflicts + invalid_conflicts
        return {
            "ok": not invalid_rows,
            "dry_run": bool(dry_run),
            "source_file": metadata["source_file"],
            "rows_seen": len(rows),
            "importable_count": len(planned_items),
            "imported_count": imported_count,
            "would_import_count": len(planned_items) if dry_run else 0,
            "skipped_existing_ids": skipped_existing_ids,
            "skipped_duplicate_ids": skipped_duplicate_ids,
            "skipped_existing_conflicts": skipped_existing_conflicts,
            "skipped_duplicate_conflicts": skipped_duplicate_conflicts,
            "invalid_rows": invalid_rows,
            "invalid_conflicts": invalid_conflicts,
            "conflict_records": conflict_records,
            "conflict_count": len(conflict_records),
            "metadata": metadata,
            "items": [dict(item) for item in planned_items],
        }

    def _resolve_import_dataset_path(self, dataset_path: str | Path) -> Path:
        raw_path = Path(dataset_path)
        candidate = raw_path if raw_path.is_absolute() else self.review_dir / raw_path
        resolved = candidate.expanduser().resolve()
        review_root = self.review_dir.resolve()
        try:
            resolved.relative_to(review_root)
        except ValueError as exc:
            raise PromptRouterReasonerStoreError(
                "Import dataset must be under prompt_router_reasoner_reviews"
            ) from exc
        if resolved.suffix.lower() != ".jsonl":
            raise PromptRouterReasonerValidationError("Import dataset must be a JSONL file")
        if not resolved.exists():
            raise PromptRouterReasonerStoreError("Import dataset file not found: " + str(resolved))
        return resolved

    def _read_import_dataset_rows(self, source_path: Path) -> list[dict[str, Any]]:
        rows: list[dict[str, Any]] = []
        for line_number, line in enumerate(source_path.read_text(encoding="utf-8-sig").splitlines(), 1):
            text = line.strip()
            if not text:
                continue
            try:
                loaded = json.loads(text)
            except json.JSONDecodeError as exc:
                raise PromptRouterReasonerStoreError(
                    "Invalid import JSONL at line " + str(line_number)
                ) from exc
            if not isinstance(loaded, dict):
                raise PromptRouterReasonerStoreError(
                    "Import JSONL row is not an object at line " + str(line_number)
                )
            rows.append(dict(loaded))
        return rows

    def _review_export_row_to_import_item(
        self,
        row: Mapping[str, Any],
        *,
        source_path: Path,
        review_sequence: int,
    ) -> dict[str, Any]:
        review_item_id = str(row.get("review_item_id", "")).strip()
        if not review_item_id:
            raise PromptRouterReasonerValidationError("Imported row missing review_item_id")
        full_text = str(row.get("full_generator_text", ""))
        short_text = str(row.get("short_generator_text", "")).strip() or compact_generator_text(full_text)
        if not full_text:
            raise PromptRouterReasonerValidationError("Imported row missing full_generator_text")
        review_status = str(row.get("review_status", STATUS_PENDING)).strip() or STATUS_PENDING
        if review_status not in VALID_REVIEW_STATUSES:
            raise PromptRouterReasonerValidationError("Invalid imported review_status: " + review_status)
        human_label_raw = str(row.get("human_label", "")).strip()
        human_label = normalize_human_label(human_label_raw) if human_label_raw else None
        if review_status == STATUS_REVIEWED and human_label not in VALID_HUMAN_LABELS:
            raise PromptRouterReasonerValidationError("Reviewed imported row requires a valid human_label")
        if review_status == STATUS_PENDING:
            human_label = None

        heuristic = self._prompt_snapshot_from_export_row(row, "heuristic")
        ml = self._prompt_snapshot_from_export_row(row, "ml")
        now = utc_now_iso()
        item = {
            "schema_version": SCHEMA_VERSION,
            "review_item_id": review_item_id,
            "generator_text_id": str(row.get("generator_text_id", "")).strip() or "imported_" + review_item_id,
            "full_generator_text": full_text,
            "short_generator_text": short_text,
            "generator_text_hash": str(row.get("generator_text_hash", "")).strip() or sha256_text(full_text),
            "created_at": str(row.get("created_at", "")).strip() or now,
            "updated_at": str(row.get("updated_at", "")).strip() or now,
            "review_sequence": int(review_sequence),
            "reviewed_at": str(row.get("reviewed_at", "")).strip() or None,
            "review_status": review_status,
            "agreement_status": normalize_agreement_status(str(row.get("agreement_status", AGREEMENT_DISAGREE))),
            "heuristic_prompt": heuristic.to_dict(),
            "ml_prompt": ml.to_dict(),
            "router_mode_at_capture": normalize_router_mode(str(row.get("router_mode_at_capture", ROUTER_WITH_HEURISTICS))),
            "router_mode_at_review": (
                normalize_router_mode(str(row.get("router_mode_at_review")))
                if str(row.get("router_mode_at_review", "")).strip()
                else None
            ),
            "human_label": human_label,
            "undo_available": False,
            "safety_violation": self._parse_import_bool(row.get("safety_violation")),
            "app_version": str(row.get("app_version", "")),
            "router_version": str(row.get("router_version", "")),
            "retriever_version": str(row.get("retriever_version", "")),
            "ml_version": str(row.get("ml_version", "")),
            "prompt_library_version": str(row.get("prompt_library_version", "")),
            "ask_ai_request_files": [],
            "ai_second_opinion_files": [],
            "latest_ai_second_opinion_label": str(row.get("latest_ai_second_opinion_label", "")).strip() or None,
            "latest_ai_agrees_with_human": str(row.get("latest_ai_agrees_with_human", "")).strip() or None,
            "notes": str(row.get("notes", "")),
            "imported_from_review_dataset": True,
            "import_source_file": self._relative_review_path(source_path),
            "last_event_id": "",
        }
        if review_status == STATUS_REVIEWED and not item.get("reviewed_at"):
            item["reviewed_at"] = item.get("updated_at")
        self._validate_review_item(item)
        return item

    @staticmethod
    def _prompt_snapshot_from_export_row(row: Mapping[str, Any], prefix: str) -> PromptSnapshot:
        keyword_text = str(row.get(prefix + "_keywords", ""))
        keywords = tuple(part.strip() for part in keyword_text.split(",") if part.strip())
        return PromptSnapshot.from_mapping(
            {
                "prompt_id": row.get(prefix + "_prompt_id", ""),
                "prompt_name": row.get(prefix + "_prompt_name", ""),
                "prompt_path": row.get(prefix + "_prompt_path", ""),
                "prompt_hash": row.get(prefix + "_prompt_hash", ""),
                "prompt_summary": row.get(prefix + "_prompt_summary", ""),
                "prompt_group": row.get(prefix + "_prompt_group", ""),
                "prompt_version": row.get(prefix + "_prompt_version", ""),
                "score": row.get(prefix + "_score", None),
                "confidence": row.get(prefix + "_confidence", None),
                "explanation": row.get(prefix + "_explanation", ""),
                "keywords": keywords,
                "route": row.get(prefix + "_route", ""),
                "semantic_match": row.get(prefix + "_semantic_match", ""),
                "inferred_intent": row.get(prefix + "_inferred_intent", ""),
                "disagreement_reason": row.get(prefix + "_disagreement_reason", ""),
                "safety_status": row.get(prefix + "_safety_status", "not_evaluated"),
            }
        )

    @staticmethod
    def _parse_import_bool(value: Any) -> bool:
        if isinstance(value, bool):
            return value
        return str(value).strip().lower() in {"1", "true", "yes", "y"}

    def _existing_review_fingerprints(self) -> set[str]:
        return set(self._existing_review_fingerprint_map().keys())

    def _existing_review_fingerprint_map(self) -> dict[str, str]:
        fingerprints: dict[str, str] = {}
        for item in self._index.get("items", {}).values():
            if not isinstance(item, Mapping):
                continue
            fingerprint = self._review_item_import_fingerprint(item)
            review_item_id = str(item.get("review_item_id", ""))
            if fingerprint and review_item_id and fingerprint not in fingerprints:
                fingerprints[fingerprint] = review_item_id
        return fingerprints

    @staticmethod
    def _import_conflict_record(
        *,
        row_number: int,
        review_item_id: str,
        reason: str,
        incoming_item: Mapping[str, Any] | None = None,
        existing_item: Mapping[str, Any] | None = None,
        incoming_row: Mapping[str, Any] | None = None,
        fingerprint: str = "",
        error: str = "",
    ) -> dict[str, Any]:
        incoming = incoming_item if isinstance(incoming_item, Mapping) else {}
        existing = existing_item if isinstance(existing_item, Mapping) else {}
        raw_row = incoming_row if isinstance(incoming_row, Mapping) else {}

        def prompt_value(item: Mapping[str, Any], prompt_key: str, value_key: str) -> str:
            prompt = item.get(prompt_key) if isinstance(item.get(prompt_key), Mapping) else {}
            return str(prompt.get(value_key, ""))

        return {
            "row_number": int(row_number),
            "reason": str(reason),
            "action": "skipped" if reason != "invalid_row" else "rejected",
            "safe_to_import": False,
            "review_item_id": str(review_item_id or incoming.get("review_item_id") or raw_row.get("review_item_id", "")),
            "existing_review_item_id": str(existing.get("review_item_id", "")),
            "generator_text_id": str(incoming.get("generator_text_id") or raw_row.get("generator_text_id", "")),
            "short_generator_text": str(incoming.get("short_generator_text") or raw_row.get("short_generator_text", "")),
            "incoming_review_status": str(incoming.get("review_status") or raw_row.get("review_status", "")),
            "existing_review_status": str(existing.get("review_status", "")),
            "incoming_human_label": str(incoming.get("human_label") or raw_row.get("human_label", "")),
            "existing_human_label": str(existing.get("human_label") or ""),
            "incoming_heuristic_prompt_id": prompt_value(incoming, "heuristic_prompt", "prompt_id") or str(raw_row.get("heuristic_prompt_id", "")),
            "existing_heuristic_prompt_id": prompt_value(existing, "heuristic_prompt", "prompt_id"),
            "incoming_ml_prompt_id": prompt_value(incoming, "ml_prompt", "prompt_id") or str(raw_row.get("ml_prompt_id", "")),
            "existing_ml_prompt_id": prompt_value(existing, "ml_prompt", "prompt_id"),
            "fingerprint": str(fingerprint),
            "error": str(error),
        }

    @staticmethod
    def _review_item_import_fingerprint(item: Mapping[str, Any]) -> str:
        heuristic = item.get("heuristic_prompt") if isinstance(item.get("heuristic_prompt"), Mapping) else {}
        ml = item.get("ml_prompt") if isinstance(item.get("ml_prompt"), Mapping) else {}
        parts = (
            str(item.get("generator_text_hash", "")),
            str(heuristic.get("prompt_id", "")),
            str(heuristic.get("prompt_hash", "")),
            str(ml.get("prompt_id", "")),
            str(ml.get("prompt_hash", "")),
        )
        return sha256_text("\n".join(parts)) if any(parts) else ""

    def _relative_review_path(self, path: Path) -> str:
        try:
            return path.resolve().relative_to(self.review_dir.resolve()).as_posix()
        except ValueError:
            return str(path)
