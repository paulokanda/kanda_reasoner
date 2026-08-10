# project-path: kanda_reasoner_app/engineering_diagnostics_gui/ai_correction_handoff.py
"""Read-only artifact writer for the Full Engineering Diagnostics AI handoff."""

from __future__ import annotations

from dataclasses import dataclass
from threading import Event
from typing import Callable
import hashlib
from pathlib import Path
import time

from kanda_reasoner_app.project_selection_registry import ProjectSelectionRecord

from ._engineering_capability_models import EngineeringCapabilityCoverage

from .engineering_capability_coverage import (
    collect_engineering_capability_coverage,
)
from .ai_correction_report import (
    AiCorrectionCollectorResult,
    build_full_ai_correction_report,
)

__all__ = [
    "AiCorrectionHandoffArtifact",
    "build_full_ai_correction_handoff",
]


@dataclass(frozen=True, slots=True)
class AiCorrectionHandoffArtifact:
    """One transient Project-owned AI correction handoff artifact."""

    report_path: str
    sha256: str
    finding_count: int
    correction_group_count: int
    correction_ready_count: int
    blocked_count: int
    review_required_count: int
    byte_count: int
    console_summary: str
    capability_surface_count: int
    capability_error_count: int
    capability_warning_count: int


def _daily_work_root(project_root: Path) -> Path:
    anchor = Path(project_root.anchor)
    if not str(project_root.anchor).strip():
        raise RuntimeError("PROJECT_DRIVE_ROOT_UNRESOLVED")
    return anchor / (project_root.name + "_delete_after_daily_work")


def _report_path(
    project_root: Path,
    run_ids: tuple[str, ...],
    project_daily_work_root: str | None = None,
) -> Path:
    identity = "\n".join(run_ids).encode("utf-8")
    digest = hashlib.sha256(identity).hexdigest()[:16]
    daily_root = (
        Path(project_daily_work_root).expanduser().resolve(strict=False)
        if str(project_daily_work_root or "").strip()
        else _daily_work_root(project_root)
    )
    return (
        daily_root
        / "engineering_diagnostics_ai_correction_handoff"
        / ("full_engineering_diagnostics_ai_correction_" + digest + ".txt")
    )


def build_full_ai_correction_handoff(
    controller: object,
    project_root: str,
    collector_results: tuple[AiCorrectionCollectorResult, ...],
    cancellation: Event | None = None,
    *,
    capability_coverage: EngineeringCapabilityCoverage | None = None,
    project_card: ProjectSelectionRecord | None = None,
    tool_root: str | None = None,
    complete_review_sha256: str = "",
    complete_review_item_count: int = 0,
    project_daily_work_root: str | None = None,
    publish_guard: Callable[[], None] | None = None,
    performance_lines: tuple[str, ...] = (),
    performance_started_at: float | None = None,
) -> AiCorrectionHandoffArtifact:
    """Load run views and publish one guarded Project-owned handoff artifact."""
    timings = list(performance_lines)
    root = Path(project_root).expanduser().resolve(strict=True)
    run_ids = tuple(
        result.run_id
        for result in collector_results
        if result.status == "STORED" and result.run_id
    )
    load_views_started = time.perf_counter()
    run_views_list = []
    stored_results = tuple(
        result
        for result in collector_results
        if result.status == "STORED" and result.run_id
    )
    for result in stored_results:
        load_started = time.perf_counter()
        run_views_list.append(controller.load_run_view(str(root), result.run_id))
        timings.append(
            "Diagnostics run view "
            + result.label
            + ": "
            + f"{time.perf_counter() - load_started:.3f}s"
        )
    run_views = tuple(run_views_list)
    timings.append(
        "Diagnostics run views total: "
        + f"{time.perf_counter() - load_views_started:.3f}s"
    )
    if capability_coverage is None:
        coverage_started = time.perf_counter()
        capability_coverage = collect_engineering_capability_coverage(
            str(root),
            collector_results,
            cancellation,
        )
        timings.append(
            "Diagnostics capability coverage: "
            + f"{time.perf_counter() - coverage_started:.3f}s"
        )
    report_started = time.perf_counter()
    report = build_full_ai_correction_report(
        str(root),
        collector_results,
        run_views,
        capability_coverage,
        project_card=project_card,
        tool_root=tool_root,
        complete_review_sha256=complete_review_sha256,
        complete_review_item_count=complete_review_item_count,
    )
    timings.append(
        "AI correction report build: "
        + f"{time.perf_counter() - report_started:.3f}s"
    )
    if publish_guard is not None:
        publish_guard()
    path = _report_path(root, run_ids, project_daily_work_root)
    path.parent.mkdir(parents=True, exist_ok=True)
    write_started = time.perf_counter()
    path.write_text(report.text, encoding="utf-8", errors="strict")
    timings.append(
        "AI correction report write: "
        + f"{time.perf_counter() - write_started:.3f}s"
    )
    try:
        if publish_guard is not None:
            publish_guard()
    except Exception:
        path.unlink(missing_ok=True)
        raise
    hash_started = time.perf_counter()
    payload = path.read_bytes()
    payload_sha256 = hashlib.sha256(payload).hexdigest()
    timings.append(
        "AI correction report reread and SHA256: "
        + f"{time.perf_counter() - hash_started:.3f}s"
    )
    if performance_started_at is not None:
        timings.append(
            "AI correction handoff BUILDING total: "
            + f"{time.perf_counter() - performance_started_at:.3f}s"
        )
    performance_summary = "PERFORMANCE PROFILE\n" + "\n".join(timings)
    return AiCorrectionHandoffArtifact(
        report_path=str(path),
        sha256=payload_sha256,
        finding_count=report.finding_count,
        correction_group_count=report.correction_group_count,
        correction_ready_count=report.correction_ready_count,
        blocked_count=report.blocked_count,
        review_required_count=report.review_required_count,
        byte_count=len(payload),
        console_summary=report.console_summary + "\n\n" + performance_summary,
        capability_surface_count=report.capability_surface_count,
        capability_error_count=report.capability_error_count,
        capability_warning_count=report.capability_warning_count,
    )
