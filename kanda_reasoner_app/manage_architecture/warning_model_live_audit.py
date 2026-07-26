# project-path: kanda_reasoner_app/manage_architecture/warning_model_live_audit.py
"""Fresh live audit and verified-apply orchestration for Warning Local AI Resolver."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
import os
import subprocess
import sys

from kanda_reasoner_app.manage_architecture.warning_heuristic_resolver import (
    WarningFinding,
    resolve_warning_audit,
)
from kanda_reasoner_app.manage_architecture.warning_model_test_apply import (
    ModelTestProtectionApplyResult,
)

__all__ = [
    "FreshTestProtectionAudit",
    "ModelApplyVerificationResult",
    "apply_and_verify_model_plan",
    "run_fresh_test_protection_audit",
]

Runner = Callable[..., subprocess.CompletedProcess[str]]
ProgressCallback = Callable[[int, int, int, int, str, str], None]


@dataclass(frozen=True, slots=True)
class FreshTestProtectionAudit:
    """Hold one fresh Architecture Review result and its exact gap identities."""

    audit_text: str
    findings: tuple[WarningFinding, ...]
    source_paths: frozenset[str]
    return_code: int


@dataclass(frozen=True, slots=True)
class ModelApplyVerificationResult:
    """Report actual live writes and exact-path verification from fresh audits."""

    apply_result: ModelTestProtectionApplyResult
    before_gap_paths: tuple[str, ...]
    after_gap_paths: tuple[str, ...]
    requested_source_paths: tuple[str, ...]
    resolved_source_paths: tuple[str, ...]
    still_present_source_paths: tuple[str, ...]
    newly_surfaced_paths: tuple[str, ...]

    @property
    def verified_resolved_count(self) -> int:
        return len(self.resolved_source_paths)


def _audit_cli(project_root: Path) -> Path:
    return (
        project_root
        / "kanda_reasoner_app"
        / "manage_architecture"
        / "manage_architecture.py"
    )


def _normalize_path(value: str) -> str:
    return str(value or "").replace("\\", "/").strip()


def run_fresh_test_protection_audit(
    project_root: str | Path,
    *,
    runner: Runner = subprocess.run,
    timeout_seconds: int = 300,
) -> FreshTestProtectionAudit:
    """Run a fresh Architecture Review and extract exact TEST_PROTECTION_GAP paths."""
    root = Path(project_root).expanduser().resolve()
    cli = _audit_cli(root)
    if not cli.is_file():
        raise RuntimeError("Architecture Review CLI missing: " + str(cli))
    env = dict(os.environ)
    env["PYTHONPATH"] = str(root)
    try:
        completed = runner(
            [sys.executable, str(cli), "--root", str(root), "--validate"],
            cwd=str(root),
            env=env,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout_seconds,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError("Fresh Architecture Review timed out.") from exc
    text = (completed.stdout or "")
    if completed.stderr:
        text += "\n" + completed.stderr
    if "ARCHITECTURE VALIDATION SUMMARY" not in text:
        raise RuntimeError(
            "Fresh Architecture Review produced no recognizable validation summary."
        )
    report = resolve_warning_audit(text)
    findings = tuple(
        item.finding
        for item in report.decisions
        if item.finding.code == "TEST_PROTECTION_GAP"
        and item.finding.path != "."
    )
    source_paths = frozenset(_normalize_path(item.path) for item in findings)
    return FreshTestProtectionAudit(
        audit_text=text,
        findings=findings,
        source_paths=source_paths,
        return_code=int(completed.returncode),
    )


def _apply_source_paths(plan: object) -> tuple[str, ...]:
    decisions = tuple(getattr(plan, "decisions", ()) or ())
    accepted_actions = {"link_existing_test", "model_test_change"}
    return tuple(
        sorted(
            {
                _normalize_path(getattr(item, "source_path", ""))
                for item in decisions
                if getattr(item, "action", "") in accepted_actions
                and _normalize_path(getattr(item, "source_path", ""))
            }
        )
    )


def apply_and_verify_model_plan(
    plan: object,
    *,
    audit_func: Callable[[str | Path], FreshTestProtectionAudit] = run_fresh_test_protection_audit,
    apply_func: Callable[[object], ModelTestProtectionApplyResult] | None = None,
    progress_callback: ProgressCallback | None = None,
) -> ModelApplyVerificationResult:
    """Apply one confirmed plan only against fresh state and verify exact resolved paths."""
    if apply_func is None:
        from kanda_reasoner_app.manage_architecture.warning_model_test_protection_resolver import (
            apply_model_test_protection_plan,
        )

        apply_func = apply_model_test_protection_plan
    project_root = str(getattr(plan, "project_root", "") or "").strip()
    if not project_root:
        raise RuntimeError("Local AI plan has no project_root.")
    requested = _apply_source_paths(plan)
    if progress_callback is not None:
        progress_callback(len(requested), len(requested), 0, 0, "Architecture Review", "fresh_audit_before_apply")
    before = audit_func(project_root)
    stale = sorted(set(requested) - set(before.source_paths))
    if stale:
        raise RuntimeError(
            "MODEL PLAN STALE - source gap no longer present: " + ", ".join(stale[:8])
        )
    if progress_callback is not None:
        progress_callback(len(requested), len(requested), 0, 0, "Live project", "guarded_apply")
    apply_result = apply_func(plan)
    if progress_callback is not None:
        progress_callback(len(requested), 0, 0, 0, "Architecture Review", "fresh_audit_after_apply")
    after = audit_func(project_root)
    requested_set = set(requested)
    resolved = tuple(sorted(requested_set & set(before.source_paths) - set(after.source_paths)))
    still_present = tuple(sorted(requested_set & set(after.source_paths)))
    newly_surfaced = tuple(sorted(set(after.source_paths) - set(before.source_paths)))
    return ModelApplyVerificationResult(
        apply_result=apply_result,
        before_gap_paths=tuple(sorted(before.source_paths)),
        after_gap_paths=tuple(sorted(after.source_paths)),
        requested_source_paths=requested,
        resolved_source_paths=resolved,
        still_present_source_paths=still_present,
        newly_surfaced_paths=newly_surfaced,
    )
