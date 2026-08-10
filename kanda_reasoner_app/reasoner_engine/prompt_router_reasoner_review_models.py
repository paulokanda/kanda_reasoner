# project-path: kanda_reasoner_app/reasoner_engine/prompt_router_reasoner_review_models.py
"""Persistent review store for Prompt Router Reasoner.

This module is intentionally backend-only. It records heuristic versus ML
prompt-selection review items in a project-local folder and never grants ML
route authority. It does not import or write to freeze memory, prompt canon, or
router mutation modules.
"""

from __future__ import annotations


__all__ = [
    'AGREEMENT_AGREE',
    'AGREEMENT_DISAGREE',
    'LABEL_BOTH_ACCEPTABLE_UNCLEAR',
    'LABEL_HEURISTICS_CORRECT',
    'LABEL_ML_CORRECT',
    'PromptRouterReasonerItemNotFoundError',
    'PromptRouterReasonerStoreError',
    'PromptRouterReasonerValidationError',
    'PromptSnapshot',
    'REVIEW_FOLDER_NAME',
    'ROUTER_WITH_HELP_OF_ML',
    'ROUTER_WITH_HEURISTICS',
    'ROUTER_WITH_ML',
    'STATUS_REVIEWED',
    'VALID_ROUTER_MODES',
    'compact_generator_text',
    'compute_ai_human_agreement',
    'detect_ai_second_opinion_label',
    'normalize_agreement_status',
    'normalize_human_label',
    'normalize_router_mode',
    'sha256_text',
    'utc_now_iso',
]
from dataclasses import dataclass, field
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
from typing import Any, Iterable, Mapping

SCHEMA_VERSION = "1.0"
REVIEW_FOLDER_NAME = "prompt_router_reasoner_reviews"
REVIEW_LOG_FILENAME = "prompt_router_reasoner_reviews.jsonl"
REVIEW_INDEX_FILENAME = "prompt_router_reasoner_index.json"
REVIEW_STATS_FILENAME = "prompt_router_reasoner_stats.json"
ASK_AI_REQUESTS_FOLDER_NAME = "ask_ai_requests"
ASK_AI_ANSWERS_FOLDER_NAME = "ask_ai_answers"
EXPORT_DATASETS_FOLDER_NAME = "export_review_datasets"
IMPORT_DATASETS_FOLDER_NAME = "import_review_datasets"

EVENT_PENDING_CREATED = "pending_created"
EVENT_REVIEW_SAVED = "review_saved"
EVENT_REVIEW_UNDONE = "review_undone"
EVENT_ASK_AI_REQUEST_SAVED = "ask_ai_request_saved"
EVENT_AI_SECOND_OPINION_SAVED = "ai_second_opinion_saved"
EVENT_REVIEW_DATASET_IMPORTED = "review_dataset_imported"

STATUS_PENDING = "pending"
STATUS_REVIEWED = "reviewed"

AGREEMENT_AGREE = "agree"
AGREEMENT_DISAGREE = "disagree"

LABEL_HEURISTICS_CORRECT = "heuristics_correct"
LABEL_ML_CORRECT = "ml_correct"
LABEL_BOTH_ACCEPTABLE_UNCLEAR = "both_acceptable_unclear"

ROUTER_WITH_HEURISTICS = "router_with_heuristics"
ROUTER_WITH_HELP_OF_ML = "router_with_help_of_ml"
ROUTER_WITH_ML = "router_with_ml"

VALID_EVENT_TYPES = {
    EVENT_PENDING_CREATED,
    EVENT_REVIEW_SAVED,
    EVENT_REVIEW_UNDONE,
    EVENT_ASK_AI_REQUEST_SAVED,
    EVENT_AI_SECOND_OPINION_SAVED,
    EVENT_REVIEW_DATASET_IMPORTED,
}

VALID_REVIEW_STATUSES = {
    STATUS_PENDING,
    STATUS_REVIEWED,
}

VALID_AGREEMENT_STATUSES = {
    AGREEMENT_AGREE,
    AGREEMENT_DISAGREE,
}

VALID_HUMAN_LABELS = {
    LABEL_HEURISTICS_CORRECT,
    LABEL_ML_CORRECT,
    LABEL_BOTH_ACCEPTABLE_UNCLEAR,
}

VALID_ROUTER_MODES = {
    ROUTER_WITH_HEURISTICS,
    ROUTER_WITH_HELP_OF_ML,
    ROUTER_WITH_ML,
}

FORBIDDEN_REVIEW_STORE_PATH_FRAGMENTS = (
    "project_freeze_after_update",
    "project_freeze_ledger",
    "frozen_features_memory",
    "freeze_hint_intake",
)


class PromptRouterReasonerStoreError(RuntimeError):
    """Raised when the Prompt Router Reasoner store cannot complete an operation."""


class PromptRouterReasonerValidationError(ValueError):
    """Raised when a review record violates the local review schema."""


class PromptRouterReasonerItemNotFoundError(KeyError):
    """Raised when a review item does not exist in the review index."""


def utc_now_iso() -> str:
    """Return a stable UTC timestamp string with sub-second ordering.

    Prompt Router Reasoner can capture several review rows during the same
    visible second on Windows. Keeping microseconds prevents newest-row
    selection from depending on random UUID order.
    """
    return datetime.now(timezone.utc).isoformat(timespec="microseconds").replace("+00:00", "Z")


def sha256_text(text: str) -> str:
    """Return a SHA-256 hex digest for a UTF-8 text string."""
    return hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()


def compact_generator_text(text: str, *, max_chars: int = 96) -> str:
    """Return a single-line compact preview for a generator text."""
    collapsed = " ".join(str(text).replace("\r", " ").replace("\n", " ").split())
    if len(collapsed) <= max_chars:
        return collapsed
    return collapsed[: max_chars - 3].rstrip() + "..."


def normalize_router_mode(value: str | None) -> str:
    """Normalize router mode values accepted by this review store."""
    if value is None or value == "":
        return ROUTER_WITH_HEURISTICS
    text = str(value).strip().lower()
    aliases = {
        "heuristics": ROUTER_WITH_HEURISTICS,
        "router_with_heuristics": ROUTER_WITH_HEURISTICS,
        "help_ml": ROUTER_WITH_HELP_OF_ML,
        "with_help_of_ml": ROUTER_WITH_HELP_OF_ML,
        "router_with_help_of_ml": ROUTER_WITH_HELP_OF_ML,
        "ml": ROUTER_WITH_ML,
        "router_with_ml": ROUTER_WITH_ML,
    }
    if text in aliases:
        return aliases[text]
    raise PromptRouterReasonerValidationError("Invalid router mode: " + str(value))


def normalize_human_label(label: str) -> str:
    """Normalize and validate a human review label."""
    text = str(label).strip().lower()
    if text not in VALID_HUMAN_LABELS:
        raise PromptRouterReasonerValidationError("Invalid human label: " + str(label))
    return text


def normalize_agreement_status(value: str | None) -> str:
    """Normalize the agreement status between heuristic and ML prompt choices."""
    text = str(value or "").strip().lower()
    if text in VALID_AGREEMENT_STATUSES:
        return text
    raise PromptRouterReasonerValidationError("Invalid agreement status: " + str(value))


def _json_dumps(data: Mapping[str, Any], *, indent: int | None = None) -> str:
    """Support json dumps behavior.
    
    Parameters
    ----------
    data : Mapping[str, Any]
        The input data.
    indent : int | None, optional
        The optional indent value.
    
    Returns
    -------
    str
        The string result.
    """
    
    return json.dumps(dict(data), ensure_ascii=False, sort_keys=True, indent=indent) + "\n"


def _read_json_object(path: Path) -> dict[str, Any]:
    """Support read json object behavior.
    
    Parameters
    ----------
    path : Path
        The file or folder path.
    
    Returns
    -------
    dict[str, Any]
        The mapped values.
    """
    
    if not path.exists():
        return {}
    try:
        loaded = json.loads(path.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as exc:
        raise PromptRouterReasonerStoreError("Invalid JSON file: " + str(path)) from exc
    if not isinstance(loaded, dict):
        raise PromptRouterReasonerStoreError("JSON file is not an object: " + str(path))
    return dict(loaded)


def _atomic_write_text(path: Path, text: str) -> None:
    """Support atomic write text behavior.
    
    Parameters
    ----------
    path : Path
        The file or folder path.
    text : str
        The text value.
    """
    
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = path.with_name(path.name + ".tmp")
    temp_path.write_text(text, encoding="utf-8", newline="\n")
    os.replace(temp_path, path)


@dataclass(frozen=True)
class PromptSnapshot:
    """Snapshot of a prompt candidate selected by one router/prompt-selector path."""

    prompt_id: str
    prompt_name: str
    prompt_path: str
    prompt_hash: str
    prompt_summary: str
    prompt_group: str = ""
    prompt_version: str = ""
    score: float | None = None
    confidence: float | None = None
    explanation: str = ""
    keywords: tuple[str, ...] = field(default_factory=tuple)
    route: str = ""
    semantic_match: str = ""
    inferred_intent: str = ""
    disagreement_reason: str = ""
    safety_status: str = "not_evaluated"

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "PromptSnapshot":
        """Build a prompt snapshot from a mapping with minimal validation."""
        keywords_raw = data.get("keywords", ())
        if isinstance(keywords_raw, str):
            keywords = tuple(item.strip() for item in keywords_raw.split(",") if item.strip())
        elif isinstance(keywords_raw, Iterable):
            keywords = tuple(str(item).strip() for item in keywords_raw if str(item).strip())
        else:
            keywords = ()

        return cls(
            prompt_id=str(data.get("prompt_id", "")).strip(),
            prompt_name=str(data.get("prompt_name", "")).strip(),
            prompt_path=str(data.get("prompt_path", "")).strip().replace("\\", "/"),
            prompt_hash=str(data.get("prompt_hash", "")).strip(),
            prompt_summary=str(data.get("prompt_summary", "")).strip(),
            prompt_group=str(data.get("prompt_group", data.get("group", ""))).strip(),
            prompt_version=str(data.get("prompt_version", data.get("version", ""))).strip(),
            score=_optional_float(data.get("score")),
            confidence=_optional_float(data.get("confidence")),
            explanation=str(data.get("explanation", "")).strip(),
            keywords=keywords,
            route=str(data.get("route", data.get("matched_route", ""))).strip(),
            semantic_match=str(data.get("semantic_match", "")).strip(),
            inferred_intent=str(data.get("inferred_intent", "")).strip(),
            disagreement_reason=str(data.get("disagreement_reason", "")).strip(),
            safety_status=str(data.get("safety_status", "not_evaluated")).strip() or "not_evaluated",
        )

    def validate(self, *, field_name: str) -> None:
        """Validate required prompt snapshot fields."""
        missing = []
        if not self.prompt_id:
            missing.append("prompt_id")
        if not self.prompt_name:
            missing.append("prompt_name")
        if not self.prompt_path:
            missing.append("prompt_path")
        if not self.prompt_hash:
            missing.append("prompt_hash")
        if not self.prompt_summary:
            missing.append("prompt_summary")
        if missing:
            raise PromptRouterReasonerValidationError(
                field_name + " missing required fields: " + ", ".join(missing)
            )

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable snapshot dict."""
        return {
            "prompt_id": self.prompt_id,
            "prompt_name": self.prompt_name,
            "prompt_path": self.prompt_path,
            "prompt_hash": self.prompt_hash,
            "prompt_summary": self.prompt_summary,
            "prompt_group": self.prompt_group,
            "prompt_version": self.prompt_version,
            "score": self.score,
            "confidence": self.confidence,
            "explanation": self.explanation,
            "keywords": list(self.keywords),
            "route": self.route,
            "semantic_match": self.semantic_match,
            "inferred_intent": self.inferred_intent,
            "disagreement_reason": self.disagreement_reason,
            "safety_status": self.safety_status,
        }


def _optional_float(value: Any) -> float | None:
    """Support optional float behavior.
    
    Parameters
    ----------
    value : Any
        The input value.
    
    Returns
    -------
    float | None
        The floating-point result.
    """
    
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError) as exc:
        raise PromptRouterReasonerValidationError("Expected numeric value: " + str(value)) from exc


def detect_ai_second_opinion_label(answer_text: str) -> str:
    """Detect an advisory label from pasted AI answer text.

    The result is only metadata. It must never set the human review label.
    """
    lowered = " ".join(str(answer_text or "").lower().replace("/", " ").split())
    both_markers = (
        "both acceptable",
        "acceptable unclear",
        "both are acceptable",
        "both options are acceptable",
        "both choices are acceptable",
        "unclear",
    )
    ml_markers = (
        "ml correct",
        "machine learning correct",
        "ml selection is better",
        "ml selected prompt is better",
        "best answer: ml",
        "choice: ml",
    )
    heuristic_markers = (
        "heuristics correct",
        "heuristic correct",
        "heuristic selection is better",
        "heuristic selected prompt is better",
        "best answer: heuristic",
        "choice: heuristic",
    )
    if any(marker in lowered for marker in both_markers):
        return LABEL_BOTH_ACCEPTABLE_UNCLEAR
    if any(marker in lowered for marker in ml_markers):
        return LABEL_ML_CORRECT
    if any(marker in lowered for marker in heuristic_markers):
        return LABEL_HEURISTICS_CORRECT
    return "unknown"


def compute_ai_human_agreement(ai_label: str | None, human_label: Any) -> str:
    """Return yes/no/unknown agreement metadata for advisory AI answers."""
    if ai_label not in VALID_HUMAN_LABELS or human_label not in VALID_HUMAN_LABELS:
        return "unknown"
    return "yes" if ai_label == human_label else "no"



def _ensure_prompt_snapshot(data: PromptSnapshot | Mapping[str, Any], field_name: str) -> PromptSnapshot:
    """Support ensure prompt snapshot behavior.
    
    Parameters
    ----------
    data : PromptSnapshot | Mapping[str, Any]
        The input data.
    field_name : str
        The field name value.
    
    Returns
    -------
    PromptSnapshot
        The prompt snapshot result.
    """
    
    if isinstance(data, PromptSnapshot):
        snapshot = data
    elif isinstance(data, Mapping):
        snapshot = PromptSnapshot.from_mapping(data)
    else:
        raise PromptRouterReasonerValidationError(field_name + " must be a PromptSnapshot or mapping")
    snapshot.validate(field_name=field_name)
    return snapshot
