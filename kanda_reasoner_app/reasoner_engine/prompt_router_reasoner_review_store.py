# project-path: kanda_reasoner_app/reasoner_engine/prompt_router_reasoner_review_store.py
"""Persistent review store for Prompt Router Reasoner.

Thin compatibility facade after v7.2 large-module refactor. Runtime logic
lives in ordinary importable modules in this package; this module preserves the
original public API and selected private helper imports for existing callers.
"""

from __future__ import annotations

# Public ownership belongs here only for the review store facade class.
# Compatibility imports below remain explicit and directly importable, but they
# are not re-declared as public owners here because prompt_router_reasoner_review_models.py
# is the stable public owner for model/helper records.
__all__ = ["PromptRouterReasonerReviewStore"]

from .prompt_router_reasoner_review_advisory_files import (
    PromptRouterReasonerReviewStoreAdvisoryFilesMixin,
)
from .prompt_router_reasoner_review_core import PromptRouterReasonerReviewStoreCoreMixin
from .prompt_router_reasoner_review_export import PromptRouterReasonerReviewStoreExportMixin
from .prompt_router_reasoner_review_import import PromptRouterReasonerReviewStoreImportMixin
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
    FORBIDDEN_REVIEW_STORE_PATH_FRAGMENTS,
    IMPORT_DATASETS_FOLDER_NAME,
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
    VALID_ROUTER_MODES,
    PromptRouterReasonerItemNotFoundError,
    PromptRouterReasonerStoreError,
    PromptRouterReasonerValidationError,
    PromptSnapshot,
    _atomic_write_text,
    _ensure_prompt_snapshot,
    _json_dumps,
    _optional_float,
    _read_json_object,
    compact_generator_text,
    compute_ai_human_agreement,
    detect_ai_second_opinion_label,
    normalize_agreement_status,
    normalize_human_label,
    normalize_router_mode,
    sha256_text,
    utc_now_iso,
)


class PromptRouterReasonerReviewStore(
    PromptRouterReasonerReviewStoreCoreMixin,
    PromptRouterReasonerReviewStoreAdvisoryFilesMixin,
    PromptRouterReasonerReviewStoreExportMixin,
    PromptRouterReasonerReviewStoreImportMixin,
):
    """Project-local persistent store for heuristic versus ML review items."""


