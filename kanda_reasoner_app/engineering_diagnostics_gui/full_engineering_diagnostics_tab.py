# project-path: kanda_reasoner_app/engineering_diagnostics_gui/full_engineering_diagnostics_tab.py
"""Full Engineering Diagnostics orchestration over public collector contracts."""

from __future__ import annotations

from concurrent.futures import Future, ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path
from threading import Event
import time
import traceback
from typing import Callable

from .ai_correction_handoff import (
    AiCorrectionHandoffArtifact,
    build_full_ai_correction_handoff,
)
from .ai_correction_report import AiCorrectionCollectorResult
from .controller import EngineeringDiagnosticsController
from .engineering_diagnostics_sonar import create_engineering_diagnostics_sonar
from .models import DiagnosticScanCandidate, EngineeringDiagnosticsGuiCancelled

__all__ = [
    "FULL_ENGINEERING_DIAGNOSTIC_COLLECTORS",
    "collect_full_engineering_diagnostics_candidates",
    "create_full_engineering_diagnostics_panel",
]


@dataclass(frozen=True)
class _CollectorOutcome:
    label: str
    candidate: DiagnosticScanCandidate | None
    error_text: str
    elapsed_seconds: float = 0.0


FULL_ENGINEERING_DIAGNOSTIC_COLLECTORS: tuple[tuple[str, str], ...] = (
    ("BOM", "collect_bom_candidate"),
    ("Ruff", "collect_ruff_candidate"),
    ("Architecture", "collect_architecture_candidate"),
    ("Shadow", "collect_shadow_candidate"),
)


def _tool_root() -> Path:
    return Path(__file__).resolve().parents[2]


def collect_full_engineering_diagnostics_candidates(
    controller: EngineeringDiagnosticsController,
    project_root: str,
    generation: int,
    cancellation: Event,
) -> tuple[_CollectorOutcome, ...]:
    outcomes: list[_CollectorOutcome] = []
    for label, method_name in FULL_ENGINEERING_DIAGNOSTIC_COLLECTORS:
        if cancellation.is_set():
            raise EngineeringDiagnosticsGuiCancelled("full diagnostics cancelled")
        collector = getattr(controller, method_name)
        started = time.perf_counter()
        try:
            candidate = collector(project_root, generation, cancellation)
        except EngineeringDiagnosticsGuiCancelled:
            raise
        except Exception:  # noqa: BLE001
            outcomes.append(
                _CollectorOutcome(
                    label=label,
                    candidate=None,
                    error_text=traceback.format_exc(),
                    elapsed_seconds=time.perf_counter() - started,
                )
            )
        else:
            outcomes.append(
                _CollectorOutcome(
                    label=label,
                    candidate=candidate,
                    error_text="",
                    elapsed_seconds=time.perf_counter() - started,
                )
            )
    return tuple(outcomes)


def create_full_engineering_diagnostics_panel(
    project_root_provider: Callable[[], object] | None = None,
    *,
    controller: EngineeringDiagnosticsController | None = None,
):
    """Create the all-collector run console without duplicating the backend."""
    from PySide6.QtCore import QTimer
    from PySide6.QtWidgets import (
        QApplication,
        QHBoxLayout,
        QLabel,
        QPlainTextEdit,
        QPushButton,
        QVBoxLayout,
        QWidget,
    )

    active_controller = controller or EngineeringDiagnosticsController(
        tool_root=_tool_root()
    )
    panel = QWidget()
    panel.setObjectName("full_engineering_diagnostics_page")
    layout = QVBoxLayout(panel)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(8)

    toolbar = QHBoxLayout()
    run_button = QPushButton("Run All Engineering Diagnostics")
    run_button.setObjectName("full_engineering_diagnostics_run_button")
    cancel_button = QPushButton("Cancel Diagnostics")
    cancel_button.setObjectName("full_engineering_diagnostics_cancel_button")
    cancel_button.setEnabled(False)
    copy_ai_button = QPushButton("Copy AI Correction Handoff")
    copy_ai_button.setObjectName(
        "full_engineering_diagnostics_copy_ai_handoff_button"
    )
    copy_ai_button.setEnabled(False)
    toolbar.addWidget(run_button)
    toolbar.addWidget(cancel_button)
    toolbar.addWidget(copy_ai_button)
    toolbar.addStretch(1)
    layout.addLayout(toolbar)

    status_label = QLabel("Ready")
    status_label.setObjectName("full_engineering_diagnostics_status_label")
    output = QPlainTextEdit()
    output.setReadOnly(True)
    output.setPlainText(
        "Run all supported diagnostics. Detailed stored runs remain available "
        "under Pontual Engineering Diagnostics."
    )
    sonar = create_engineering_diagnostics_sonar(panel)
    layout.addWidget(status_label)
    layout.addWidget(output, 1)

    run_executor = ThreadPoolExecutor(max_workers=1)
    report_executor = ThreadPoolExecutor(max_workers=1)
    state: dict[str, object] = {
        "generation": 0,
        "future": None,
        "cancel": None,
        "project_root": "",
        "report_future": None,
        "report_artifact": None,
    }

    def current_project_root() -> str:
        if project_root_provider is not None:
            value = str(project_root_provider() or "").strip()
            if value:
                return value
        return str(Path.cwd())

    def set_busy(busy: bool) -> None:
        run_button.setEnabled(not busy)
        cancel_button.setEnabled(busy)

    def _append_output(lines: list[str]) -> None:
        current = output.toPlainText().rstrip()
        addition = "\n".join(lines).rstrip()
        output.setPlainText((current + "\n\n" + addition).strip())

    def finish_ai_handoff(
        generation: int,
        project_root: str,
        future: Future,
    ) -> None:
        if generation != state["generation"]:
            return
        if project_root != current_project_root():
            return
        state["report_future"] = None
        try:
            artifact = future.result()
        except Exception:  # noqa: BLE001
            state["report_artifact"] = None
            copy_ai_button.setEnabled(False)
            _append_output(
                [
                    "AI correction handoff: FAILED",
                    traceback.format_exc().rstrip(),
                ]
            )
            status_label.setText(
                "Diagnostics stored, but AI correction handoff generation failed."
            )
            return
        if not isinstance(artifact, AiCorrectionHandoffArtifact):
            raise RuntimeError("AI_CORRECTION_HANDOFF_ARTIFACT_INVALID")
        state["report_artifact"] = artifact
        copy_ai_button.setEnabled(True)
        _append_output(
            [
                "AI correction handoff: READY",
                *artifact.console_summary.splitlines(),
                "Path: " + artifact.report_path,
                "SHA256: " + artifact.sha256,
                "Findings: " + str(artifact.finding_count),
                "Correction groups: " + str(artifact.correction_group_count),
                "Engineering capability surfaces: "
                + str(artifact.capability_surface_count),
                "Capability errors: " + str(artifact.capability_error_count),
                "Capability warnings: " + str(artifact.capability_warning_count),
                "Correction context ready: "
                + str(artifact.correction_ready_count),
                "Blocked: " + str(artifact.blocked_count),
                "Review/evidence required: "
                + str(artifact.review_required_count),
                "Bytes: " + str(artifact.byte_count),
            ]
        )
        status_label.setText(
            "Full Engineering Diagnostics complete. "
            "AI correction handoff is ready."
        )

    def poll_ai_handoff(
        generation: int,
        project_root: str,
        future: Future,
    ) -> None:
        if generation != state["generation"]:
            return
        if project_root != current_project_root():
            return
        if future.done():
            finish_ai_handoff(generation, project_root, future)
            return
        QTimer.singleShot(
            100,
            lambda: poll_ai_handoff(generation, project_root, future),
        )

    def start_ai_handoff(
        generation: int,
        project_root: str,
        collector_results: tuple[AiCorrectionCollectorResult, ...],
    ) -> None:
        if generation != state["generation"]:
            return
        state["report_artifact"] = None
        copy_ai_button.setEnabled(False)
        raw_findings = sum(result.finding_count for result in collector_results)
        status_label.setText(
            "Diagnostics stored. Building grouped AI correction handoff off the GUI thread..."
        )
        _append_output(
            [
                "AI correction handoff: BUILDING",
                "Raw findings: " + str(raw_findings),
                "Mode: comprehensive Engineering Safety capability coverage plus deterministic correction groups",
                "Coverage includes 23 Pontual GUI actions, 24 Safety CLI commands, and Architecture Review.",
                "Targeted, planning, manual, and utility tools remain explicitly labelled; none are silently treated as project-wide clean.",
                "Raw findings remain in Diagnostics history; they are not duplicated line-by-line.",
            ]
        )
        future = report_executor.submit(
            build_full_ai_correction_handoff,
            active_controller,
            project_root,
            collector_results,
        )
        state["report_future"] = future
        QTimer.singleShot(
            100,
            lambda: poll_ai_handoff(generation, project_root, future),
        )

    def copy_ai_handoff() -> None:
        artifact = state.get("report_artifact")
        if not isinstance(artifact, AiCorrectionHandoffArtifact):
            status_label.setText("No AI correction handoff is ready yet.")
            return
        path = Path(artifact.report_path)
        if not path.is_file():
            status_label.setText("AI correction handoff file is no longer available.")
            copy_ai_button.setEnabled(False)
            return
        if artifact.byte_count <= 2_000_000:
            payload = path.read_text(encoding="utf-8", errors="replace")
            QApplication.clipboard().setText(payload)
            status_label.setText("Full AI correction handoff copied to clipboard.")
            return
        reference = "\n".join(
            (
                "FULL ENGINEERING DIAGNOSTICS AI CORRECTION HANDOFF",
                "Path: " + artifact.report_path,
                "SHA256: " + artifact.sha256,
                "Bytes: " + str(artifact.byte_count),
                "Findings: " + str(artifact.finding_count),
                "Correction groups: " + str(artifact.correction_group_count),
                "Engineering capability surfaces: "
                + str(artifact.capability_surface_count),
                "Capability errors: " + str(artifact.capability_error_count),
                "Capability warnings: " + str(artifact.capability_warning_count),
                "Instruction: Read this report before proposing corrections.",
            )
        )
        QApplication.clipboard().setText(reference)
        status_label.setText(
            "Report is larger than 2 MB; its path and SHA256 were copied."
        )

    def render_outcomes(
        generation: int,
        outcomes: tuple[_CollectorOutcome, ...],
    ) -> None:
        lines: list[str] = []
        collector_results: list[AiCorrectionCollectorResult] = []
        stored = 0
        failed = 0
        project_root = str(state.get("project_root") or current_project_root())
        for outcome in outcomes:
            if outcome.candidate is None:
                failed += 1
                lines.extend(
                    (
                        outcome.label + ": FAILED",
                        outcome.error_text.rstrip(),
                        "",
                    )
                )
                collector_results.append(
                    AiCorrectionCollectorResult(
                        label=outcome.label,
                        status="FAILED",
                        finding_count=0,
                        error_text=outcome.error_text,
                    )
                )
                continue
            try:
                run = active_controller.commit_candidate(
                    current_project_root(),
                    outcome.candidate,
                    current_generation=generation,
                )
            except Exception:  # noqa: BLE001
                failed += 1
                commit_error = traceback.format_exc()
                lines.extend(
                    (
                        outcome.label + ": COMMIT FAILED",
                        commit_error.rstrip(),
                        "",
                    )
                )
                collector_results.append(
                    AiCorrectionCollectorResult(
                        label=outcome.label,
                        status="COMMIT_FAILED",
                        finding_count=0,
                        error_text=commit_error,
                    )
                )
                continue
            stored += 1
            collector_results.append(
                AiCorrectionCollectorResult(
                    label=outcome.label,
                    status="STORED",
                    run_id=run.run_id,
                    finding_count=run.finding_count,
                )
            )
            lines.append(
                outcome.label
                + ": STORED | "
                + str(run.finding_count)
                + " findings | "
                + run.run_id[:12]
            )
        output.setPlainText("\n".join(lines).rstrip())
        status_label.setText(
            "Full Engineering Diagnostics complete: "
            + str(stored)
            + " stored, "
            + str(failed)
            + " failed."
        )
        start_ai_handoff(
            generation,
            project_root,
            tuple(collector_results),
        )

    def finish_run(generation: int, future: Future) -> None:
        if generation != state["generation"]:
            return
        state["future"] = None
        state["cancel"] = None
        sonar.stop()
        set_busy(False)
        try:
            outcomes = future.result()
        except EngineeringDiagnosticsGuiCancelled:
            status_label.setText("Full Engineering Diagnostics cancelled.")
            return
        except Exception as exc:  # noqa: BLE001
            status_label.setText("Full Engineering Diagnostics failed: " + str(exc))
            output.setPlainText(traceback.format_exc())
            return
        render_outcomes(generation, outcomes)

    def poll_run(generation: int, future: Future) -> None:
        if generation != state["generation"]:
            return
        if future.done():
            finish_run(generation, future)
            return
        QTimer.singleShot(100, lambda: poll_run(generation, future))

    def start_run() -> None:
        if state["future"] is not None:
            return
        root = current_project_root()
        state["generation"] = int(state["generation"]) + 1
        generation = int(state["generation"])
        cancellation = Event()
        state["cancel"] = cancellation
        state["project_root"] = root
        state["report_artifact"] = None
        copy_ai_button.setEnabled(False)
        set_busy(True)
        status_label.setText("Running all Engineering Diagnostics collectors...")
        output.setPlainText(
            "BOM, Ruff, Architecture, and Shadow collectors are running "
            "through their existing public contracts."
        )
        sonar.start("All collectors")
        future = run_executor.submit(
            collect_full_engineering_diagnostics_candidates,
            active_controller,
            root,
            generation,
            cancellation,
        )
        state["future"] = future
        QTimer.singleShot(100, lambda: poll_run(generation, future))

    def cancel_run() -> None:
        cancellation = state.get("cancel")
        if cancellation is None or state.get("future") is None:
            status_label.setText("No Full Engineering Diagnostics run is active.")
            return
        if cancellation.is_set():
            return
        cancellation.set()
        sonar.stop()
        cancel_button.setEnabled(False)
        status_label.setText(
            "Cancellation requested; the active collector will settle safely."
        )

    def set_project_root(_value: object = None) -> None:
        cancel_run()
        state["report_artifact"] = None
        copy_ai_button.setEnabled(False)
        output.setPlainText(
            "Project selection changed. Run Full Engineering Diagnostics again "
            "for the newly selected Project."
        )

    run_button.clicked.connect(start_run)
    cancel_button.clicked.connect(cancel_run)
    copy_ai_button.clicked.connect(copy_ai_handoff)
    panel.destroyed.connect(lambda _obj=None: run_executor.shutdown(wait=False))
    panel.destroyed.connect(lambda _obj=None: report_executor.shutdown(wait=False))

    panel.set_project_root = set_project_root
    panel.start_full_engineering_diagnostics = start_run
    panel.cancel_full_engineering_diagnostics = cancel_run
    panel.full_engineering_diagnostics_controller = active_controller
    panel.full_engineering_diagnostics_run_button = run_button
    panel.full_engineering_diagnostics_cancel_button = cancel_button
    panel.full_engineering_diagnostics_copy_ai_handoff_button = copy_ai_button
    panel.full_engineering_diagnostics_status_label = status_label
    panel.full_engineering_diagnostics_output = output
    panel.full_engineering_diagnostics_sonar = sonar
    panel.full_engineering_diagnostics_sonar_widget = sonar.widget()
    panel.full_engineering_diagnostics_collectors = tuple(
        label for label, _method in FULL_ENGINEERING_DIAGNOSTIC_COLLECTORS
    )
    return panel
