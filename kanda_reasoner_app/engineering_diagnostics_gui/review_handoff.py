# project-path: kanda_reasoner_app/engineering_diagnostics_gui/review_handoff.py
"""Public Project-bound bridge from Complete Review to AI correction handoff."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from threading import Event
import hashlib
import time
import traceback

from kanda_reasoner_app.engineering_safety.complete_review_contract import (
    CompleteEngineeringReviewResult,
)
from kanda_reasoner_app.project_selection_registry import (
    ProjectSelectionRecord,
    ProjectSelectionRegistry,
)

from .ai_correction_handoff import build_full_ai_correction_handoff
from .ai_correction_report import AiCorrectionCollectorResult
from .controller import EngineeringDiagnosticsController
from .complete_review_coverage import (
    coverage_from_complete_engineering_review,
)
from .full_engineering_diagnostics_tab import (
    collect_full_engineering_diagnostics_candidates,
)
from .models import EngineeringDiagnosticsGuiCancelled

__all__ = ["build_complete_review_ai_correction_handoff"]


def _record_identity(record: ProjectSelectionRecord) -> tuple[str, ...]:
    return (
        record.stable_project_id,
        record.project_root,
        record.project_root_fingerprint,
        record.project_support_root,
        record.selection_mode.value,
        record.updated_at_utc,
    )


@dataclass(frozen=True)
class _ProjectObservationGuard:
    """Observe one expected Project record through one explicit registry handle."""

    registry: ProjectSelectionRegistry
    expected: ProjectSelectionRecord

    @classmethod
    def capture(
        cls,
        tool_root: Path,
        expected: ProjectSelectionRecord,
    ) -> "_ProjectObservationGuard":
        """Capture one explicit registry observer and verify the initial record."""
        guard = cls(
            registry=ProjectSelectionRegistry(tool_source_root=tool_root),
            expected=expected,
        )
        guard.require_current()
        return guard

    def require_current(self) -> object:
        """Reject a switch/eject without creating another registry owner."""
        current = self.registry.load_current_record()
        if current is None or _record_identity(current) != _record_identity(
            self.expected
        ):
            raise RuntimeError("ACTIVE_PROJECT_OBSERVATION_CHANGED")
        boundary = self.registry.resolve_boundary_for_root(
            self.expected.project_root
        )
        if boundary.active_project_id != self.expected.stable_project_id:
            raise RuntimeError("ACTIVE_PROJECT_OBSERVATION_ID_MISMATCH")
        return boundary


def _review_sha256(review: CompleteEngineeringReviewResult) -> str:
    return hashlib.sha256(review.rendered_log.encode("utf-8")).hexdigest()


def build_complete_review_ai_correction_handoff(
    tool_root: str | Path,
    project_card: ProjectSelectionRecord,
    review: CompleteEngineeringReviewResult,
    cancellation: Event | None = None,
    *,
    performance_lines: tuple[str, ...] = (),
):
    """Build one AI handoff for the exact selected-Project observation record."""
    handoff_started = time.perf_counter()
    timings = list(performance_lines)
    tool = Path(tool_root).expanduser().resolve(strict=True)
    root = Path(project_card.project_root).expanduser().resolve(strict=True)
    if Path(review.project_root).expanduser().resolve(strict=True) != root:
        raise RuntimeError("COMPLETE_REVIEW_PROJECT_OBSERVATION_MISMATCH")

    observation_guard = _ProjectObservationGuard.capture(tool, project_card)
    boundary = observation_guard.require_current()
    controller = EngineeringDiagnosticsController(tool_root=tool)
    cancel = cancellation or Event()
    generation = int(time.monotonic_ns())
    collectors_started = time.perf_counter()
    outcomes = collect_full_engineering_diagnostics_candidates(
        controller,
        str(root),
        generation,
        cancel,
    )
    timings.append(
        "Diagnostics collectors total: "
        + f"{time.perf_counter() - collectors_started:.3f}s"
    )
    for outcome in outcomes:
        timings.append(
            "Diagnostics collector "
            + outcome.label
            + ": "
            + f"{outcome.elapsed_seconds:.3f}s"
        )
    collector_results: list[AiCorrectionCollectorResult] = []
    commits_started = time.perf_counter()

    for outcome in outcomes:
        if cancel.is_set():
            raise EngineeringDiagnosticsGuiCancelled(
                "complete review AI handoff cancelled"
            )
        observation_guard.require_current()
        if outcome.candidate is None:
            collector_results.append(
                AiCorrectionCollectorResult(
                    label=outcome.label,
                    status="FAILED",
                    finding_count=0,
                    error_text=outcome.error_text,
                )
            )
            continue
        commit_started = time.perf_counter()
        try:
            run = controller.commit_candidate(
                str(root),
                outcome.candidate,
                current_generation=generation,
            )
        except Exception:  # noqa: BLE001 - preserve collector isolation.
            collector_results.append(
                AiCorrectionCollectorResult(
                    label=outcome.label,
                    status="COMMIT_FAILED",
                    finding_count=0,
                    error_text=traceback.format_exc(),
                )
            )
            timings.append(
                "Diagnostics commit "
                + outcome.label
                + ": "
                + f"{time.perf_counter() - commit_started:.3f}s"
            )
            continue
        timings.append(
            "Diagnostics commit "
            + outcome.label
            + ": "
            + f"{time.perf_counter() - commit_started:.3f}s"
        )
        collector_results.append(
            AiCorrectionCollectorResult(
                label=outcome.label,
                status="STORED",
                run_id=run.run_id,
                finding_count=run.finding_count,
            )
        )

    timings.append(
        "Diagnostics commits total: "
        + f"{time.perf_counter() - commits_started:.3f}s"
    )
    collector_tuple = tuple(collector_results)
    observation_guard.require_current()
    coverage_started = time.perf_counter()
    coverage = coverage_from_complete_engineering_review(
        review,
        collector_tuple,
        cancel,
    )

    timings.append(
        "Complete Review coverage adaptation: "
        + f"{time.perf_counter() - coverage_started:.3f}s"
    )

    def publish_guard() -> None:
        observation_guard.require_current()

    return build_full_ai_correction_handoff(
        controller,
        str(root),
        collector_tuple,
        cancel,
        capability_coverage=coverage,
        project_card=project_card,
        tool_root=str(tool),
        complete_review_sha256=_review_sha256(review),
        complete_review_item_count=review.total,
        project_daily_work_root=str(boundary.active_project_daily_work_root),
        publish_guard=publish_guard,
        performance_lines=tuple(timings),
        performance_started_at=handoff_started,
    )
