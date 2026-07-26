"""Prepare immutable GUI review context for Advanced Quality Review."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
from pathlib import Path
import shutil
import uuid

from kanda_reasoner_app.source_hygiene.ruff_policy_identity import (
    resolve_ruff_policy_identity,
)

from .advanced_quality_review_contract import build_analysis_identity
from .advanced_quality_review_orchestration import AdvancedQualityReviewRequest
from .analyzer_adapter_contract import hash_python_tree
from .analyzer_environment_contract import AnalyzerCapabilityMode
from .analyzer_pinned_environment_spec import build_pinned_analyzer_environment_lock
from .aqr_expected_topology import derive_expected_preview_import_edges
from .workbench_project_support_paths import daily_work_root, preview_root_blockers

__all__ = [
    "AdvancedQualityReviewGuiRunContext",
    "prepare_advanced_quality_review_gui_run",
]

_VIEW_ROOT_NAME = "advanced_quality_review_views"
_EXCLUDED_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    "__pycache__",
    "node_modules",
    "venv",
    ".venv",
}
_CONFIG_NAMES = (
    "pyproject.toml",
    "ruff.toml",
    ".ruff.toml",
    "mypy.ini",
    ".mypy.ini",
    "setup.cfg",
)


@dataclass(frozen=True)
class AdvancedQualityReviewGuiRunContext:
    """Bind one GUI generation to sealed daily-work analysis views."""

    request: AdvancedQualityReviewRequest
    baseline_view_root: str
    preview_view_root: str
    active_project_root: str
    target_relative_path: str
    package_name: str


def prepare_advanced_quality_review_gui_run(
    window: object,
    *,
    active_project_root: str,
    tool_root: str,
) -> AdvancedQualityReviewGuiRunContext:
    """Prepare sealed baseline/Preview views and one immutable review request."""
    project_root = Path(active_project_root).expanduser().resolve(strict=True)
    tool_path = Path(tool_root).expanduser().resolve(strict=True)
    intake = getattr(window, "_large_file_refactor_workbench_intake", None)
    preview = getattr(window, "_large_file_refactor_workbench_real_preview", None)
    structural = getattr(
        window,
        "_large_file_refactor_workbench_structural_validation",
        None,
    )
    snapshot = getattr(window, "_large_file_refactor_workbench_plan_snapshot", None)
    blockers = _entry_blockers(intake, preview, structural, snapshot)
    if blockers:
        raise ValueError("AQR_GUI_CONTEXT_BLOCKED:" + "|".join(blockers))

    target = Path(str(intake.target_file)).expanduser().resolve(strict=True)
    try:
        target_relative = target.relative_to(project_root)
    except ValueError as error:
        raise ValueError("AQR_TARGET_OUTSIDE_ACTIVE_PROJECT") from error

    preview_root = Path(str(preview.preview_root)).expanduser().resolve(strict=True)
    ownership_blockers = preview_root_blockers(project_root, preview_root)
    if ownership_blockers:
        raise ValueError(
            "AQR_PREVIEW_OWNERSHIP_BLOCKED:" + "|".join(ownership_blockers)
        )

    generation_id = uuid.uuid4().hex
    views_root = daily_work_root(project_root) / _VIEW_ROOT_NAME / generation_id
    baseline_view = views_root / "baseline"
    preview_view = views_root / "preview"
    _materialize_python_view(project_root, baseline_view)
    _materialize_python_view(project_root, preview_view)
    _overlay_preview(
        project_root=project_root,
        target=target,
        preview_root=preview_root,
        preview_result=preview,
        preview_view=preview_view,
    )

    baseline_hash = hash_python_tree(baseline_view)
    preview_hash = hash_python_tree(preview_view)
    lock = build_pinned_analyzer_environment_lock(tool_path)
    config_hash, mypy_config, mypy_mode = _analyzer_config_identity(project_root)
    project_card_identity = str(
        getattr(intake, "snapshot_hash", "") or getattr(snapshot, "snapshot_hash", "")
    ).strip()
    if not project_card_identity:
        raise ValueError("AQR_PROJECT_CARD_IDENTITY_MISSING")
    plan_json = str(getattr(snapshot, "plan_json", "") or "")
    if not plan_json:
        raise ValueError("AQR_REFACTOR_PLAN_JSON_MISSING")
    refactor_plan_hash = hashlib.sha256(plan_json.encode("utf-8")).hexdigest()
    identity = build_analysis_identity(
        project_card_identity=project_card_identity,
        target_relative_path=target_relative.as_posix(),
        baseline_hash=baseline_hash,
        preview_hash=preview_hash,
        refactor_plan_hash=refactor_plan_hash,
        analyzer_lock_hash=lock.lock_hash,
        analyzer_config_hash=config_hash,
    )
    package_name = _package_name(target_relative)
    now = datetime.now(timezone.utc)
    run_id = "aqr-" + now.strftime("%Y%m%dT%H%M%SZ") + "-" + identity.identity_hash[:12]
    request = AdvancedQualityReviewRequest(
        active_project_root=str(project_root),
        tool_root=str(tool_path),
        analysis_identity=identity,
        baseline_root=str(baseline_view),
        preview_root=str(preview_view),
        package_name=package_name,
        run_id=run_id,
        created_at_utc=now.isoformat().replace("+00:00", "Z"),
        mypy_capability_mode=mypy_mode,
        mypy_config_file=mypy_config,
        include_ruff_format_check=True,
        expected_new_import_edges=derive_expected_preview_import_edges(
            target_relative_path=target_relative.as_posix(),
            preview_result=preview,
        ),
    )
    return AdvancedQualityReviewGuiRunContext(
        request=request,
        baseline_view_root=str(baseline_view),
        preview_view_root=str(preview_view),
        active_project_root=str(project_root),
        target_relative_path=target_relative.as_posix(),
        package_name=package_name,
    )


def _entry_blockers(intake, preview, structural, snapshot) -> list[str]:
    blockers: list[str] = []
    if intake is None or getattr(intake, "status", "") != "plan_intake_ready":
        blockers.append("AQR_PLAN_INTAKE_NOT_READY")
    if not getattr(intake, "source_hash_fresh", False):
        blockers.append("AQR_BASELINE_SOURCE_STALE")
    if preview is None or getattr(preview, "status", "") != "real_preview_written":
        blockers.append("AQR_REAL_PREVIEW_NOT_READY")
    if preview is not None and getattr(preview, "blockers", ()):
        blockers.append("AQR_REAL_PREVIEW_BLOCKED")
    structural_status = str(getattr(structural, "status", "") or "")
    if not structural_status.startswith("passed"):
        blockers.append("AQR_STRUCTURAL_VALIDATION_NOT_PASSED")
    if structural is not None and getattr(structural, "blockers", ()):
        blockers.append("AQR_STRUCTURAL_VALIDATION_BLOCKED")
    if snapshot is None or not callable(getattr(snapshot, "integrity_valid", None)):
        blockers.append("AQR_WORKBENCH_SNAPSHOT_MISSING")
    elif not snapshot.integrity_valid():
        blockers.append("AQR_WORKBENCH_SNAPSHOT_INTEGRITY_INVALID")
    return sorted(set(blockers))


def _materialize_python_view(source_root: Path, destination_root: Path) -> None:
    """Copy Python source into a disposable analysis view without metadata leakage."""
    if destination_root.exists():
        shutil.rmtree(destination_root)
    destination_root.mkdir(parents=True, exist_ok=True)
    _copy_canonical_ruff_policy(source_root, destination_root)
    for source in sorted(source_root.rglob("*.py")):
        if not source.is_file() or _excluded(source, source_root):
            continue
        relative = source.relative_to(source_root)
        destination = destination_root / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(source.read_bytes())


def _copy_canonical_ruff_policy(
    source_root: Path,
    destination_root: Path,
) -> None:
    """Copy canonical Ruff policy bytes into one disposable analysis view."""
    try:
        identity = resolve_ruff_policy_identity(source_root)
    except ValueError as error:
        if str(error) == "RUFF_POLICY_CONFIG_MISSING":
            return
        raise
    source = Path(identity.config_path).resolve(strict=True)
    destination = destination_root / identity.config_relative_path
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(source.read_bytes())


def _overlay_preview(
    *,
    project_root: Path,
    target: Path,
    preview_root: Path,
    preview_result,
    preview_view: Path,
) -> None:
    target_parent_relative = target.parent.relative_to(project_root)
    for item in tuple(getattr(preview_result, "files", ()) or ()):
        relative = _safe_relative(str(getattr(item, "relative_path", "") or ""))
        source = (preview_root / relative).resolve(strict=True)
        try:
            source.relative_to(preview_root)
        except ValueError as error:
            raise ValueError("AQR_PREVIEW_FILE_ESCAPES_ROOT") from error
        destination = (preview_view / target_parent_relative / relative).resolve()
        try:
            destination.relative_to(preview_view.resolve())
        except ValueError as error:
            raise ValueError("AQR_PREVIEW_OVERLAY_ESCAPES_VIEW") from error
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(source.read_bytes())


def _analyzer_config_identity(
    project_root: Path,
) -> tuple[str, str, AnalyzerCapabilityMode]:
    digest = hashlib.sha256()
    mypy_config = ""
    for name in _CONFIG_NAMES:
        path = project_root / name
        if not path.is_file():
            continue
        relative = path.relative_to(project_root).as_posix().encode("utf-8")
        data = path.read_bytes()
        digest.update(len(relative).to_bytes(8, "big"))
        digest.update(relative)
        digest.update(len(data).to_bytes(8, "big"))
        digest.update(data)
        if name in {"mypy.ini", ".mypy.ini"}:
            mypy_config = str(path)
        elif name == "pyproject.toml" and b"[tool.mypy]" in data:
            mypy_config = str(path)
        elif name == "setup.cfg" and b"[mypy" in data:
            mypy_config = str(path)
    digest.update(b"AQR_GUI_CONFIG_POLICY_V1")
    mode = (
        AnalyzerCapabilityMode.AUTHORITATIVE
        if mypy_config
        else AnalyzerCapabilityMode.AVAILABLE_NON_AUTHORITATIVE
    )
    return digest.hexdigest(), mypy_config, mode


def _package_name(target_relative: Path) -> str:
    parts = target_relative.parts
    if len(parts) > 1:
        return str(parts[0])
    stem = target_relative.stem
    if not stem or not stem.isidentifier():
        raise ValueError("AQR_PACKAGE_NAME_UNRESOLVED")
    return stem


def _safe_relative(text: str) -> Path:
    path = Path(str(text or "").replace("\\", "/"))
    if not str(text).strip() or path.is_absolute() or ".." in path.parts:
        raise ValueError("AQR_PREVIEW_RELATIVE_PATH_INVALID")
    return path


def _excluded(path: Path, root: Path) -> bool:
    relative = path.relative_to(root)
    return bool(set(relative.parts) & _EXCLUDED_DIRS)
