# project-path: kanda_reasoner_app/daily_rfctr_report/daily_refactor_report_help/source_loader_private_impl.py
"""Load the preserved daily_refactor_report implementation source."""

from __future__ import annotations

import base64

from .daily_refactor_report_source_part_1_private_impl import DAILY_REFACTOR_REPORT_SOURCE_PART_1
from .daily_refactor_report_source_part_2_private_impl import DAILY_REFACTOR_REPORT_SOURCE_PART_2
from .daily_refactor_report_source_part_3_private_impl import DAILY_REFACTOR_REPORT_SOURCE_PART_3
from .daily_refactor_report_source_part_4_private_impl import DAILY_REFACTOR_REPORT_SOURCE_PART_4
from .daily_refactor_report_source_part_5_private_impl import DAILY_REFACTOR_REPORT_SOURCE_PART_5
from .daily_refactor_report_source_part_6_private_impl import DAILY_REFACTOR_REPORT_SOURCE_PART_6
from .daily_refactor_report_source_part_7_private_impl import DAILY_REFACTOR_REPORT_SOURCE_PART_7
from .daily_refactor_report_source_part_8_private_impl import DAILY_REFACTOR_REPORT_SOURCE_PART_8
from .daily_refactor_report_source_part_9_private_impl import DAILY_REFACTOR_REPORT_SOURCE_PART_9
from .daily_refactor_report_source_part_10_private_impl import DAILY_REFACTOR_REPORT_SOURCE_PART_10


def load_daily_refactor_report_source() -> str:
    """Return the original daily_refactor_report implementation source."""
    encoded_source = "".join([
        DAILY_REFACTOR_REPORT_SOURCE_PART_1,
        DAILY_REFACTOR_REPORT_SOURCE_PART_2,
        DAILY_REFACTOR_REPORT_SOURCE_PART_3,
        DAILY_REFACTOR_REPORT_SOURCE_PART_4,
        DAILY_REFACTOR_REPORT_SOURCE_PART_5,
        DAILY_REFACTOR_REPORT_SOURCE_PART_6,
        DAILY_REFACTOR_REPORT_SOURCE_PART_7,
        DAILY_REFACTOR_REPORT_SOURCE_PART_8,
        DAILY_REFACTOR_REPORT_SOURCE_PART_9,
        DAILY_REFACTOR_REPORT_SOURCE_PART_10,
    ])
    return base64.b64decode(encoded_source.encode("ascii")).decode("utf-8")


__all__ = ["load_daily_refactor_report_source"]
