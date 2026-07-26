# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/batch_refactor_queue.py
"""Preview-only batch queue evidence for large-file refactor plans."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

from .workbench_project_support_paths import preview_runs_root

__all__ = [
    "BATCH_REFACTOR_QUEUE_DIFF_FILENAME",
    "BATCH_REFACTOR_QUEUE_FILENAME",
    "BatchRefactorQueueItem",
    "BatchRefactorQueueResult",
    "DEFAULT_MAX_QUEUE_ITEMS",
    "PROTECTED_RELATIVE_PREFIXES",
    "build_batch_refactor_queue",
    "write_batch_refactor_queue",
]


BATCH_REFACTOR_QUEUE_FILENAME = "BATCH_REFACTOR_QUEUE.json"
BATCH_REFACTOR_QUEUE_DIFF_FILENAME = "BATCH_REFACTOR_QUEUE_ORDER.txt"
DEFAULT_MAX_QUEUE_ITEMS = 8
PROTECTED_RELATIVE_PREFIXES = (
    ".project_reference/",
    "_project_reference/",
    "project_freeze_after_update/",
    "frozen_features_memory/",
)


@dataclass(frozen=True)
class BatchRefactorQueueItem:
    """One queued refactor plan candidate."""

    index: int
    target_relpath: str
    plan_relpath: str
    source_sha256: str
    plan_sha256: str
    priority: int
    status: str
    blockers: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class BatchRefactorQueueResult:
    """Batch queue evidence written under the project-support Preview root."""

    status: str
    project_root: str
    preview_root: str
    queue_file: str
    order_file: str
    queue_token: str
    queued_items: list[BatchRefactorQueueItem]
    blocked_items: list[BatchRefactorQueueItem]
    warnings: list[str]
    blockers: list[str]
    source_mutation_enabled: bool = False
    batch_apply_enabled: bool = False
    import_rewrite_apply_enabled: bool = False

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-stable representation."""

        data = asdict(self)
        data["queued_items"] = [asdict(item) for item in self.queued_items]
        data["blocked_items"] = [asdict(item) for item in self.blocked_items]
        return data


def _project_root(path: str | Path) -> Path:
    """Resolve the selected project root."""

    root = Path(path).expanduser().resolve()
    if not root.exists():
        raise FileNotFoundError(f"Project root not found: {root}")
    return root


def _is_under(child: Path, parent: Path) -> bool:
    """Return whether child is inside parent or equal to parent."""

    try:
        child.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def _default_preview_root(root: Path) -> Path:
    """Return the selected project's persistent Workbench Preview support root."""
    return preview_runs_root(root)


def _normal_relpath(value: Any) -> str:
    """Normalize user or plan supplied relative paths."""

    text = str(value or "").strip().replace("\\", "/")
    while text.startswith("./"):
        text = text[2:]
    return text.strip("/")


def _safe_relpath(relpath: str) -> bool:
    """Return whether relpath is a normal source-tree relative path."""

    path = Path(relpath)
    if not relpath or path.is_absolute():
        return False
    if any(part in {"", ".", ".."} for part in path.parts):
        return False
    lowered = relpath.lower()
    return not any(lowered.startswith(prefix) for prefix in PROTECTED_RELATIVE_PREFIXES)


def _allowed_preview_root(root: Path, preview_root: str | Path | None) -> Path:
    """Resolve and validate a project-support Preview root."""

    expected = _default_preview_root(root).resolve()
    chosen = expected if preview_root is None else Path(preview_root).expanduser().resolve()
    if _is_under(chosen, root):
        raise ValueError("Batch queue preview root must not be inside project source.")
    if chosen == expected or _is_under(chosen, expected):
        return chosen
    raise ValueError("Batch queue Preview root must stay under selected project support.")


def _sha256_file(path: Path) -> str:
    """Return sha256 for a file."""

    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _read_plan_target(plan_path: Path) -> str:
    """Extract a target source path hint from a JSON plan when present."""

    if plan_path.suffix.lower() != ".json":
        return ""
    try:
        loaded = json.loads(plan_path.read_text(encoding="utf-8"))
    except Exception:
        return ""
    if not isinstance(loaded, Mapping):
        return ""
    for key in ("target_relpath", "target_path", "source_relpath", "source_path"):
        value = loaded.get(key)
        if value:
            return _normal_relpath(value)
    target = loaded.get("target")
    if isinstance(target, Mapping):
        for key in ("relpath", "path", "source_relpath"):
            value = target.get(key)
            if value:
                return _normal_relpath(value)
    return ""


def _queue_token(items: Sequence[BatchRefactorQueueItem]) -> str:
    """Derive a stable token for future batch review, not execution."""

    payload = [
        {
            "target": item.target_relpath,
            "plan": item.plan_relpath,
            "source_sha256": item.source_sha256,
            "plan_sha256": item.plan_sha256,
        }
        for item in items
    ]
    digest = hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()[:16]
    return f"CONFIRM_BATCH_REFACTOR_QUEUE_{digest}"


def _candidate_from_mapping(root: Path, entry: Mapping[str, Any], index: int) -> BatchRefactorQueueItem:
    """Build one queue item from a mapping."""

    plan_rel = _normal_relpath(entry.get("plan_relpath") or entry.get("plan_path") or entry.get("plan"))
    target_rel = _normal_relpath(entry.get("target_relpath") or entry.get("target_path") or entry.get("source_relpath"))
    priority = int(entry.get("priority", index))
    blockers: list[str] = []
    warnings: list[str] = []

    if not _safe_relpath(plan_rel):
        blockers.append("INVALID_OR_PROTECTED_PLAN_RELPATH")
    plan_path = (root / plan_rel).resolve() if plan_rel else root
    if plan_rel and (not _is_under(plan_path, root) or not plan_path.is_file()):
        blockers.append("PLAN_FILE_NOT_FOUND_UNDER_PROJECT")
    if plan_rel and not target_rel:
        target_rel = _read_plan_target(plan_path)
    if not _safe_relpath(target_rel):
        blockers.append("INVALID_OR_PROTECTED_TARGET_RELPATH")
    if target_rel and not target_rel.endswith(".py"):
        blockers.append("TARGET_IS_NOT_PYTHON_SOURCE")
    target_path = (root / target_rel).resolve() if target_rel else root
    if target_rel and (not _is_under(target_path, root) or not target_path.is_file()):
        blockers.append("TARGET_FILE_NOT_FOUND_UNDER_PROJECT")
    if plan_rel == target_rel:
        blockers.append("PLAN_FILE_MUST_NOT_BE_TARGET_SOURCE")

    source_sha = _sha256_file(target_path) if target_rel and target_path.is_file() else ""
    plan_sha = _sha256_file(plan_path) if plan_rel and plan_path.is_file() else ""
    status = "queued" if not blockers else "blocked"
    if not plan_sha:
        warnings.append("PLAN_HASH_UNAVAILABLE")
    return BatchRefactorQueueItem(
        index=index,
        target_relpath=target_rel,
        plan_relpath=plan_rel,
        source_sha256=source_sha,
        plan_sha256=plan_sha,
        priority=priority,
        status=status,
        blockers=blockers,
        warnings=warnings,
    )


def build_batch_refactor_queue(
    project_root: str | Path,
    entries: Iterable[Mapping[str, Any]],
    *,
    preview_root: str | Path | None = None,
    max_items: int = DEFAULT_MAX_QUEUE_ITEMS,
) -> BatchRefactorQueueResult:
    """Build read-only batch queue evidence for multiple refactor plans."""

    root = _project_root(project_root)
    preview = _allowed_preview_root(root, preview_root)
    queued: list[BatchRefactorQueueItem] = []
    blocked: list[BatchRefactorQueueItem] = []
    warnings: list[str] = []
    blockers: list[str] = []
    seen_targets: set[str] = set()

    for index, raw in enumerate(entries):
        item = _candidate_from_mapping(root, raw, index)
        if item.status == "queued" and item.target_relpath in seen_targets:
            item = BatchRefactorQueueItem(
                **{**asdict(item), "status": "blocked", "blockers": item.blockers + ["DUPLICATE_TARGET_IN_QUEUE"]}
            )
        if item.status == "queued":
            seen_targets.add(item.target_relpath)
            queued.append(item)
        else:
            blocked.append(item)

    queued.sort(key=lambda item: (item.priority, item.target_relpath))
    if len(queued) > max_items:
        overflow = queued[max_items:]
        queued = queued[:max_items]
        blocked.extend(
            BatchRefactorQueueItem(
                **{**asdict(item), "status": "blocked", "blockers": item.blockers + ["QUEUE_MAX_ITEMS_EXCEEDED"]}
            )
            for item in overflow
        )
        warnings.append("QUEUE_TRUNCATED_TO_MAX_ITEMS")
    if not queued:
        blockers.append("NO_QUEUEABLE_REFACTOR_PLANS")

    status = "batch_queue_ready" if queued and not blockers else "blocked"
    queue_file = preview / BATCH_REFACTOR_QUEUE_FILENAME
    order_file = preview / BATCH_REFACTOR_QUEUE_DIFF_FILENAME
    return BatchRefactorQueueResult(
        status=status,
        project_root=str(root),
        preview_root=str(preview),
        queue_file=str(queue_file),
        order_file=str(order_file),
        queue_token=_queue_token(queued),
        queued_items=queued,
        blocked_items=blocked,
        warnings=warnings,
        blockers=blockers,
    )


def write_batch_refactor_queue(
    project_root: str | Path,
    entries: Iterable[Mapping[str, Any]],
    *,
    preview_root: str | Path | None = None,
    max_items: int = DEFAULT_MAX_QUEUE_ITEMS,
) -> BatchRefactorQueueResult:
    """Write batch queue evidence to the project-support Preview root."""

    result = build_batch_refactor_queue(project_root, entries, preview_root=preview_root, max_items=max_items)
    preview = Path(result.preview_root)
    preview.mkdir(parents=True, exist_ok=True)
    Path(result.queue_file).write_text(json.dumps(result.to_dict(), indent=2, sort_keys=True), encoding="utf-8")
    lines = ["Batch Refactor Queue", "====================", ""]
    lines.append(f"status: {result.status}")
    lines.append(f"queue_token: {result.queue_token}")
    lines.append("")
    for item in result.queued_items:
        lines.append(f"{item.index}: {item.target_relpath} <- {item.plan_relpath}")
    if result.blocked_items:
        lines.append("")
        lines.append("Blocked items:")
        for item in result.blocked_items:
            lines.append(f"{item.index}: {item.target_relpath or '<missing>'} blockers={','.join(item.blockers)}")
    Path(result.order_file).write_text("\n".join(lines) + "\n", encoding="utf-8")
    return result

