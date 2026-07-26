# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/main_workbench_state_store.py
"""Project-owned terminal seals for automatic Main Workbench generations."""

from __future__ import annotations

from dataclasses import asdict, dataclass, is_dataclass
import hashlib
import json
from pathlib import Path
from typing import Any

from .workbench_project_support_paths import workbench_support_root

__all__ = [
    "MainWorkbenchTerminalSeal",
    "build_main_workbench_terminal_seal",
    "load_main_workbench_terminal_seal",
    "terminal_seal_is_current",
    "terminal_seal_matches_evidence",
    "write_main_workbench_terminal_seal",
]

_SCHEMA_VERSION = "1.0"


@dataclass(frozen=True)
class MainWorkbenchTerminalSeal:
    """Immutable Project-owned evidence that one pipeline generation terminated."""

    schema_version: str
    generation: int
    terminal_status: str
    active_project_root: str
    target_file: str
    source_content_hash: str
    snapshot_hash: str
    preview_hash: str
    structural_hash: str
    aqr_hash: str
    blocker_hash: str
    blockers: tuple[str, ...]
    seal_hash: str

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["blockers"] = list(self.blockers)
        return payload

    def integrity_valid(self) -> bool:
        return self.seal_hash == _seal_hash(
            generation=self.generation,
            terminal_status=self.terminal_status,
            active_project_root=self.active_project_root,
            target_file=self.target_file,
            source_content_hash=self.source_content_hash,
            snapshot_hash=self.snapshot_hash,
            preview_hash=self.preview_hash,
            structural_hash=self.structural_hash,
            aqr_hash=self.aqr_hash,
            blocker_hash=self.blocker_hash,
            blockers=self.blockers,
        )


def build_main_workbench_terminal_seal(
    window: object,
    *,
    active_project_root: str,
    generation: int,
    terminal_status: str,
    blockers: tuple[str, ...],
) -> MainWorkbenchTerminalSeal:
    """Capture one immutable terminal identity from current Workbench evidence."""
    snapshot = getattr(window, "_large_file_refactor_workbench_plan_snapshot", None)
    preview = getattr(window, "_large_file_refactor_workbench_real_preview", None)
    structural = getattr(
        window,
        "_large_file_refactor_workbench_structural_validation",
        None,
    )
    aqr = getattr(window, "_large_file_refactor_workbench_advanced_quality_review", None)
    normalized_blockers = tuple(sorted(set(str(item) for item in blockers)))
    values = {
        "generation": int(generation),
        "terminal_status": str(terminal_status),
        "active_project_root": str(Path(active_project_root).resolve()),
        "target_file": str(getattr(snapshot, "target_file", "") or ""),
        "source_content_hash": str(
            getattr(snapshot, "source_content_hash", "") or ""
        ),
        "snapshot_hash": str(getattr(snapshot, "snapshot_hash", "") or ""),
        "preview_hash": _preview_hash(preview),
        "structural_hash": _canonical_hash(_json_ready(structural)),
        "aqr_hash": _canonical_hash(_json_ready(aqr)),
        "blocker_hash": _canonical_hash(list(normalized_blockers)),
        "blockers": normalized_blockers,
    }
    return MainWorkbenchTerminalSeal(
        schema_version=_SCHEMA_VERSION,
        seal_hash=_seal_hash(**values),
        **values,
    )


def write_main_workbench_terminal_seal(
    seal: MainWorkbenchTerminalSeal,
) -> Path:
    """Persist one seal atomically under the selected Project support owner."""
    if not seal.integrity_valid():
        raise ValueError("MAIN_WORKBENCH_TERMINAL_SEAL_INVALID")
    path = _terminal_seal_path(seal.active_project_root)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(".json.partial")
    text = json.dumps(
        seal.to_dict(),
        indent=2,
        sort_keys=True,
        ensure_ascii=True,
    ) + "\n"
    temporary.write_text(text, encoding="utf-8", newline="\n")
    temporary.replace(path)
    return path


def load_main_workbench_terminal_seal(
    active_project_root: str | Path,
) -> MainWorkbenchTerminalSeal | None:
    """Load the latest integrity-valid terminal seal, if one exists."""
    path = _terminal_seal_path(active_project_root)
    if not path.is_file():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8-sig"))
        payload["blockers"] = tuple(payload.get("blockers", ()))
        seal = MainWorkbenchTerminalSeal(**payload)
    except (OSError, TypeError, ValueError, json.JSONDecodeError):
        return None
    return seal if seal.integrity_valid() else None


def terminal_seal_is_current(
    window: object,
    seal: MainWorkbenchTerminalSeal | None,
) -> bool:
    """Recheck current GUI card evidence before export or result adoption."""
    if seal is None:
        return False
    current_root = _window_project_root(window)
    return terminal_seal_matches_evidence(
        seal=seal,
        active_project_root=current_root or seal.active_project_root,
        snapshot=getattr(
            window,
            "_large_file_refactor_workbench_plan_snapshot",
            None,
        ),
        preview=getattr(
            window,
            "_large_file_refactor_workbench_real_preview",
            None,
        ),
        structural=getattr(
            window,
            "_large_file_refactor_workbench_structural_validation",
            None,
        ),
        aqr=getattr(
            window,
            "_large_file_refactor_workbench_advanced_quality_review",
            None,
        ),
    )


def terminal_seal_matches_evidence(
    *,
    seal: MainWorkbenchTerminalSeal | None,
    active_project_root: str | Path,
    snapshot: object | None,
    preview: object | None,
    structural: object | None,
    aqr: object | None,
) -> bool:
    """Verify one immutable seal against non-GUI evidence and source bytes."""
    if seal is None or not seal.integrity_valid():
        return False
    project_root = Path(active_project_root).expanduser().resolve(strict=False)
    if project_root != Path(seal.active_project_root).resolve(strict=False):
        return False
    if snapshot is None or preview is None:
        return False
    if str(getattr(snapshot, "snapshot_hash", "")) != seal.snapshot_hash:
        return False
    if _preview_hash(preview) != seal.preview_hash:
        return False
    if _canonical_hash(_json_ready(structural)) != seal.structural_hash:
        return False
    if _canonical_hash(_json_ready(aqr)) != seal.aqr_hash:
        return False
    target = Path(str(getattr(snapshot, "target_file", "") or "")).resolve(
        strict=False
    )
    try:
        target.relative_to(project_root)
    except ValueError:
        return False
    if not target.is_file():
        return False
    return _hash_file(target) == seal.source_content_hash


def _window_project_root(window: object) -> Path | None:
    edit = getattr(window, "_root_path_edit", None)
    if edit is None or not callable(getattr(edit, "text", None)):
        return None
    value = str(edit.text() or "").strip()
    if not value:
        return None
    return Path(value).expanduser().resolve(strict=False)


def _terminal_seal_path(active_project_root: str | Path) -> Path:
    return (
        workbench_support_root(active_project_root)
        / "main_workbench"
        / "latest_terminal.json"
    )


def _seal_hash(**values: Any) -> str:
    return _canonical_hash(values)


def _preview_hash(preview: object | None) -> str:
    files = [
        {
            "relative_path": str(getattr(item, "relative_path", "")),
            "content_hash": str(getattr(item, "content_hash", "")),
        }
        for item in tuple(getattr(preview, "files", ()) or ())
    ]
    return _canonical_hash(sorted(files, key=lambda item: item["relative_path"]))


def _canonical_hash(value: Any) -> str:
    text = json.dumps(
        _json_ready(value),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    )
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _json_ready(value: Any) -> Any:
    if is_dataclass(value):
        return _json_ready(asdict(value))
    to_dict = getattr(value, "to_dict", None)
    if callable(to_dict):
        return _json_ready(to_dict())
    if hasattr(value, "value") and isinstance(
        getattr(value, "value"),
        (str, int, float, bool),
    ):
        return value.value
    if isinstance(value, dict):
        return {str(key): _json_ready(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [_json_ready(item) for item in value]
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return str(value)


def _hash_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()
