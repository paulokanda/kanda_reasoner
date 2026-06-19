"""Offline Adviser active-review queue package.

This package is not part of runtime routing and exposes only pure in-memory
queue builders for caller-supplied evaluation reports.
"""

from .active_review_queue import (
    AUTHORITY_STATEMENT,
    FEATURE_ID,
    QUEUE_KIND,
    SCHEMA_VERSION,
    build_active_review_queue,
)

__all__ = [
    "AUTHORITY_STATEMENT",
    "FEATURE_ID",
    "QUEUE_KIND",
    "SCHEMA_VERSION",
    "build_active_review_queue",
]
