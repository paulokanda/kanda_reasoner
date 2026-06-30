# project-path: kanda_reasoner_app/reasoner_engine/help_index_help/help_index_data.py
"""
Normalized help payload for Reasoner Engine.
"""

from __future__ import annotations

from .help_index_normalization import normalize_help_payload
from .help_index_raw import RAW_HELP_INDEX

HELP_INDEX = normalize_help_payload(RAW_HELP_INDEX)

__all__ = ["HELP_INDEX"]



