# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/main_workbench_web_ai_package_io.py
"""Filesystem and canonical serialization support for Main Workbench packages."""

from __future__ import annotations

from dataclasses import asdict, dataclass, is_dataclass
import hashlib
import json
from pathlib import Path
from typing import Any
import zipfile

from .workbench_project_support_paths import project_support_root

__all__ = [
    "build_package_manifest",
    "canonical_hash",
    "candidate_hashes",
    "collect_project_context",
    "copy_baseline_target",
    "copy_candidate_family",
    "copy_project_context",
    "hash_file",
    "preview_identity_hash",
    "project_context_identity",
    "sanitize_project_paths",
    "verify_package_manifest",
    "verify_package_zip",
    "write_json",
    "write_package_zip",
]


_CONTEXT_CONFIG_NAMES = (
    "pyproject.toml",
    "ruff.toml",
    ".ruff.toml",
    "mypy.ini",
    ".mypy.ini",
    "setup.cfg",
    "pytest.ini",
)
_CONTEXT_EXCLUDED_PARTS = {
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
_MAX_CONTEXT_FILES = 6000
_MAX_CONTEXT_BYTES = 80 * 1024 * 1024
_MAX_GOVERNANCE_ENTRIES = 20


@dataclass(frozen=True)
class ProjectContextFile:
    """Bind one bounded context member to its exact source bytes."""

    package_relative_path: str
    source_path: str
    sha256: str
    size_bytes: int


def collect_project_context(project_root: Path) -> tuple[ProjectContextFile, ...]:
    """Collect complete Python and bounded governance context for the next AI."""
    root = project_root.expanduser().resolve(strict=True)
    items: list[ProjectContextFile] = []
    for source in sorted(root.rglob("*.py")):
        if not source.is_file() or _excluded_context_path(source, root):
            continue
        relative = source.relative_to(root).as_posix()
        items.append(_context_file("project_source/" + relative, source))
    for name in _CONTEXT_CONFIG_NAMES:
        source = root / name
        if source.is_file():
            items.append(_context_file("project_source/" + name, source))
    support_root = project_support_root(root)
    items.extend(_active_error_memory_context(support_root))
    items.extend(_recent_frozen_feature_context(support_root))
    items = sorted(items, key=lambda item: item.package_relative_path)
    if len(items) > _MAX_CONTEXT_FILES:
        raise ValueError("MAIN_WORKBENCH_PROJECT_CONTEXT_FILE_LIMIT_EXCEEDED")
    if sum(item.size_bytes for item in items) > _MAX_CONTEXT_BYTES:
        raise ValueError("MAIN_WORKBENCH_PROJECT_CONTEXT_BYTE_LIMIT_EXCEEDED")
    return tuple(items)


def copy_project_context(
    context_files: tuple[ProjectContextFile, ...],
    root: Path,
) -> list[str]:
    """Copy verified context bytes into package staging without changing owners."""
    copied: list[str] = []
    for item in context_files:
        relative = _safe_relative(item.package_relative_path)
        source = Path(item.source_path).expanduser().resolve(strict=True)
        if source.is_symlink() or hash_file(source) != item.sha256:
            raise ValueError(
                "MAIN_WORKBENCH_PROJECT_CONTEXT_CHANGED:"
                + relative.as_posix()
            )
        destination = root / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(source.read_bytes())
        copied.append(relative.as_posix())
    return copied


def project_context_identity(
    context_files: tuple[ProjectContextFile, ...],
) -> str:
    """Return one deterministic content identity for bounded Project context."""
    return canonical_hash(
        {item.package_relative_path: item.sha256 for item in context_files}
    )


def candidate_hashes(preview_root: Path, preview: Any) -> dict[str, str]:
    """Return verified relative-path hashes for one complete candidate family."""
    hashes: dict[str, str] = {}
    for item in tuple(getattr(preview, "files", ()) or ()):
        relative = _safe_relative(str(getattr(item, "relative_path", "")))
        source = (preview_root / relative).resolve(strict=True)
        _require_descendant(
            source,
            preview_root,
            "MAIN_WORKBENCH_CANDIDATE_ESCAPES_PREVIEW",
        )
        observed = hash_file(source)
        expected = str(getattr(item, "content_hash", ""))
        if observed != expected:
            raise ValueError(
                "MAIN_WORKBENCH_CANDIDATE_HASH_MISMATCH:"
                + relative.as_posix()
            )
        hashes[relative.as_posix()] = observed
    if not hashes:
        raise ValueError("MAIN_WORKBENCH_CANDIDATE_FAMILY_EMPTY")
    return dict(sorted(hashes.items()))


def copy_candidate_family(preview_root: Path, preview: Any, root: Path) -> list[str]:
    """Copy one verified complete candidate family into package staging."""
    copied: list[str] = []
    destination_root = root / "candidate_family"
    for item in sorted(preview.files, key=lambda value: value.relative_path):
        relative = _safe_relative(str(item.relative_path))
        source = (preview_root / relative).resolve(strict=True)
        _require_descendant(
            source,
            preview_root,
            "MAIN_WORKBENCH_CANDIDATE_ESCAPES_PREVIEW",
        )
        observed = hash_file(source)
        expected = str(getattr(item, "content_hash", ""))
        if observed != expected:
            raise ValueError(
                "MAIN_WORKBENCH_CANDIDATE_HASH_MISMATCH:"
                + relative.as_posix()
            )
        destination = destination_root / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(source.read_bytes())
        copied.append(relative.as_posix())
    if not copied:
        raise ValueError("MAIN_WORKBENCH_CANDIDATE_FAMILY_EMPTY")
    return copied


def copy_baseline_target(
    project_root: Path,
    target_relative_path: str,
    root: Path,
) -> None:
    """Copy the exact current baseline target after Project-root shielding."""
    relative = _safe_relative(target_relative_path)
    source = (project_root / relative).resolve(strict=True)
    _require_descendant(
        source,
        project_root,
        "MAIN_WORKBENCH_BASELINE_ESCAPES_PROJECT",
    )
    destination = root / "baseline_target" / relative
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(source.read_bytes())


def build_package_manifest(
    *,
    root: Path,
    schema_version: str,
    feature_id: str,
    package_content_hash: str,
    candidate_identity_hash: str,
    exchange_identity_hash: str,
) -> dict[str, Any]:
    """Build a complete file-hash manifest before ZIP publication."""
    files = []
    candidate_files = []
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(root).as_posix()
        entry = {
            "relative_path": relative,
            "sha256": hash_file(path),
            "size_bytes": path.stat().st_size,
        }
        files.append(entry)
        if relative.startswith("candidate_family/"):
            candidate_files.append(
                {
                    "relative_path": relative[len("candidate_family/"):],
                    "sha256": entry["sha256"],
                }
            )
    return {
        "schema_version": schema_version,
        "feature_id": feature_id,
        "package_content_hash": package_content_hash,
        "candidate_identity_hash": candidate_identity_hash,
        "exchange_identity_hash": exchange_identity_hash,
        "candidate_files": candidate_files,
        "files": files,
    }



def verify_package_manifest(root: Path, manifest: dict[str, Any]) -> None:
    """Require manifest hashes and candidate membership to match staging bytes."""
    entries = tuple(manifest.get("files") or ())
    expected: dict[str, tuple[str, int]] = {}
    for entry in entries:
        if not isinstance(entry, dict):
            raise ValueError("MAIN_WORKBENCH_MANIFEST_ENTRY_INVALID")
        relative = _safe_relative(str(entry.get("relative_path") or ""))
        key = relative.as_posix()
        if key in expected:
            raise ValueError("MAIN_WORKBENCH_MANIFEST_PATH_DUPLICATE:" + key)
        expected[key] = (
            str(entry.get("sha256") or ""),
            int(entry.get("size_bytes") or 0),
        )
    observed_paths = {
        path.relative_to(root).as_posix()
        for path in root.rglob("*")
        if path.is_file() and path.name != "EXCHANGE_MANIFEST.json"
    }
    if observed_paths != set(expected):
        raise ValueError("MAIN_WORKBENCH_MANIFEST_CONTENT_SCOPE_MISMATCH")
    for relative_text, (expected_hash, expected_size) in expected.items():
        path = (root / _safe_relative(relative_text)).resolve(strict=True)
        _require_descendant(path, root, "MAIN_WORKBENCH_MANIFEST_PATH_ESCAPE")
        if path.stat().st_size != expected_size or hash_file(path) != expected_hash:
            raise ValueError(
                "MAIN_WORKBENCH_MANIFEST_FILE_MISMATCH:" + relative_text
            )
    candidates = {
        str(item.get("relative_path") or ""): str(item.get("sha256") or "")
        for item in tuple(manifest.get("candidate_files") or ())
        if isinstance(item, dict)
    }
    actual_candidates = {
        relative[len("candidate_family/"):]: expected[relative][0]
        for relative in expected
        if relative.startswith("candidate_family/")
    }
    if candidates != actual_candidates or not candidates:
        raise ValueError("MAIN_WORKBENCH_MANIFEST_CANDIDATE_SCOPE_MISMATCH")

def write_package_zip(root: Path, destination: Path) -> None:
    """Write one deterministic relative-path ZIP from verified staging."""
    with zipfile.ZipFile(
        destination,
        "w",
        compression=zipfile.ZIP_DEFLATED,
    ) as archive:
        for path in sorted(root.rglob("*")):
            if path.is_file():
                archive.write(path, path.relative_to(root).as_posix())


def verify_package_zip(root: Path, path: Path) -> None:
    """Reopen the ZIP and require exact member hashes before publication."""
    expected = {
        item.relative_to(root).as_posix(): hash_file(item)
        for item in root.rglob("*")
        if item.is_file()
    }
    with zipfile.ZipFile(path) as archive:
        observed = {
            info.filename: hashlib.sha256(archive.read(info.filename)).hexdigest()
            for info in archive.infolist()
            if not info.is_dir()
        }
    if observed != expected:
        raise ValueError("MAIN_WORKBENCH_ZIP_REOPEN_HASH_MISMATCH")


def write_json(path: Path, payload: Any) -> None:
    """Write canonical readable ASCII JSON as UTF-8 without BOM."""
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(
        json_ready(payload),
        indent=2,
        sort_keys=True,
        ensure_ascii=True,
    ) + "\n"
    path.write_text(text, encoding="utf-8", newline="\n")


def preview_identity_hash(preview: Any) -> str:
    """Return a stable content identity for one complete Preview family."""
    files = [
        {
            "relative_path": str(item.relative_path),
            "content_hash": str(item.content_hash),
        }
        for item in tuple(getattr(preview, "files", ()) or ())
    ]
    return canonical_hash(sorted(files, key=lambda item: item["relative_path"]))


def sanitize_project_paths(value: Any, project_root: Path) -> Any:
    """Replace absolute Active Project paths with stable relative paths."""
    if isinstance(value, dict):
        return {
            str(key): sanitize_project_paths(item, project_root)
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [sanitize_project_paths(item, project_root) for item in value]
    if isinstance(value, str):
        try:
            path = Path(value)
            if path.is_absolute():
                return path.resolve(strict=False).relative_to(project_root).as_posix()
        except (OSError, ValueError):
            return value
    return value


def canonical_hash(value: Any) -> str:
    """Return canonical SHA-256 for JSON-ready evidence."""
    text = json.dumps(
        json_ready(value),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    )
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def json_ready(value: Any) -> Any:
    """Normalize dataclasses, enums, paths, and containers for JSON output."""
    if is_dataclass(value):
        return json_ready(asdict(value))
    to_dict = getattr(value, "to_dict", None)
    if callable(to_dict):
        return json_ready(to_dict())
    if hasattr(value, "value") and isinstance(
        getattr(value, "value"),
        (str, int, float, bool),
    ):
        return value.value
    if isinstance(value, dict):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [json_ready(item) for item in value]
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return str(value)


def hash_file(path: Path) -> str:
    """Return the SHA-256 of one exact file."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _context_file(package_relative_path: str, source: Path) -> ProjectContextFile:
    return ProjectContextFile(
        package_relative_path=package_relative_path,
        source_path=str(source),
        sha256=hash_file(source),
        size_bytes=source.stat().st_size,
    )


def _active_error_memory_context(support_root: Path) -> list[ProjectContextFile]:
    lessons_root = support_root / "project_error_memory" / "lessons"
    candidates: list[tuple[str, Path]] = []
    if lessons_root.is_dir():
        for source in lessons_root.glob("*.json"):
            if not source.is_file():
                continue
            try:
                payload = json.loads(source.read_text(encoding="utf-8-sig"))
            except (OSError, json.JSONDecodeError):
                continue
            if str(payload.get("status") or "").casefold() != "active":
                continue
            order = str(payload.get("updated_at_utc") or source.name)
            candidates.append((order, source))
    selected = sorted(candidates, reverse=True)[:_MAX_GOVERNANCE_ENTRIES]
    return [
        _context_file(
            "governance/error_memory/active_lessons/" + source.name,
            source,
        )
        for _order, source in selected
    ]


def _recent_frozen_feature_context(support_root: Path) -> list[ProjectContextFile]:
    entries_root = (
        support_root
        / "project_freeze_after_update"
        / "frozen_features_memory"
        / "entries"
    )
    if not entries_root.is_dir():
        return []
    selected = sorted(
        (path for path in entries_root.glob("*.md") if path.is_file()),
        key=lambda path: path.name,
        reverse=True,
    )[:_MAX_GOVERNANCE_ENTRIES]
    return [
        _context_file(
            "governance/frozen_features/entries/" + source.name,
            source,
        )
        for source in selected
    ]


def _excluded_context_path(path: Path, root: Path) -> bool:
    relative = path.relative_to(root)
    return bool(_CONTEXT_EXCLUDED_PARTS.intersection(relative.parts))


def _safe_relative(value: str) -> Path:
    path = Path(str(value or "").replace("\\", "/"))
    if not str(value or "").strip() or path.is_absolute() or ".." in path.parts:
        raise ValueError("MAIN_WORKBENCH_RELATIVE_PATH_INVALID")
    return path


def _require_descendant(path: Path, root: Path, marker: str) -> None:
    try:
        path.resolve(strict=False).relative_to(root.resolve(strict=False))
    except ValueError as error:
        raise ValueError(marker) from error
