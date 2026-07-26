"""Retire stale AQR runtime and presentation state on snapshot replacement."""
from __future__ import annotations

from typing import Any

from .advanced_quality_review_gui_formatting import (
    format_advanced_quality_review_progress,
)
from .advanced_quality_review_orchestration import AdvancedQualityReviewStage

__all__ = ["retire_aqr_for_snapshot_replacement"]

_STAGE_ORDER = (
    AdvancedQualityReviewStage.ENVIRONMENT_PREFLIGHT,
    AdvancedQualityReviewStage.RUFF,
    AdvancedQualityReviewStage.API_REVIEW,
    AdvancedQualityReviewStage.IMPORT_GRAPH,
    AdvancedQualityReviewStage.TYPE_REVIEW,
    AdvancedQualityReviewStage.DEAD_CODE,
    AdvancedQualityReviewStage.DELTA,
    AdvancedQualityReviewStage.CROSS_CHECK,
    AdvancedQualityReviewStage.PERSISTENCE,
)


def retire_aqr_for_snapshot_replacement(window: Any) -> None:
    """Retire old AQR lineage without clearing unresolved correction-session authority."""
    controller = getattr(
        window,
        "_large_file_refactor_workbench_aqr_controller",
        None,
    )
    abandoned = False
    abandon = getattr(controller, "abandon_current_generation", None)
    if callable(abandon):
        abandoned = bool(abandon())

    progress = getattr(
        window,
        "_large_file_refactor_workbench_aqr_progress_output",
        None,
    )
    if progress is not None:
        progress.setPlainText(
            format_advanced_quality_review_progress({}, _STAGE_ORDER)
        )
    bar = getattr(
        window,
        "_large_file_refactor_workbench_aqr_progress_bar",
        None,
    )
    if bar is not None:
        bar.setValue(0)

    if abandoned:
        monitor = getattr(
            window,
            "_large_file_refactor_workbench_aqr_sonar_monitor",
            None,
        )
        finish_error = getattr(monitor, "finish_error", None)
        if callable(finish_error):
            finish_error(
                "Advanced Quality Review retired",
                (
                    "Previous AQR generation belonged to a replaced snapshot",
                    "Late progress and terminal output are discarded",
                    "Run a fresh AQR after deterministic stages are rebuilt",
                ),
            )

    window._large_file_refactor_workbench_aqr_stage_states = {}
    window._large_file_refactor_workbench_aqr_identity_hash = ""
    window._large_file_refactor_workbench_aqr_context = None
    window._large_file_refactor_workbench_aqr_terminal_status = ""
    window._large_file_refactor_workbench_aqr_terminal_diagnostic = ""
