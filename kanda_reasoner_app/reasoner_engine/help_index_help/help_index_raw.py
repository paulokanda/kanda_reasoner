"""Public facade for the raw help index payload."""

from __future__ import annotations

from .help_index_raw_parts.raw_part_1_private_impl import RAW_HELP_INDEX_PART_1 as _RAW_HELP_INDEX_PART_1
from .help_index_raw_parts.raw_part_2_private_impl import RAW_HELP_INDEX_PART_2 as _RAW_HELP_INDEX_PART_2

RAW_HELP_INDEX = {}
RAW_HELP_INDEX.update(_RAW_HELP_INDEX_PART_1)
RAW_HELP_INDEX.update(_RAW_HELP_INDEX_PART_2)

__all__ = ['RAW_HELP_INDEX']
