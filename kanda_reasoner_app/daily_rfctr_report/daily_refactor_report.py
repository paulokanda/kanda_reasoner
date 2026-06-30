# project-path: kanda_reasoner_app/daily_rfctr_report/daily_refactor_report.py
"""Public facade for the daily refactor report module."""

from __future__ import annotations

from .daily_refactor_report_help.source_loader_private_impl import (
    load_daily_refactor_report_source as _load_daily_refactor_report_source,
)

_DAILY_REFACTOR_REPORT_SOURCE = _load_daily_refactor_report_source()
exec(compile(_DAILY_REFACTOR_REPORT_SOURCE, __file__, "exec"), globals())
del _DAILY_REFACTOR_REPORT_SOURCE
del _load_daily_refactor_report_source
