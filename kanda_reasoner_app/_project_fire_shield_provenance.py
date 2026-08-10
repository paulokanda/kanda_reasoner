# project-path: kanda_reasoner_app/_project_fire_shield_provenance.py
"""Internal deterministic provenance and Tool immutability enforcement."""

from __future__ import annotations

import ast
import hashlib
import os
import stat
from pathlib import Path
from typing import Iterable

from kanda_reasoner_app._project_fire_shield_types import (
    FireShieldContext,
    FireShieldError,
    FireShieldMode,
    ToolFileState,
    ToolSnapshot,
 )

__all__: tuple[str, ...] = ()

_SKIP_TOOL_DIR_NAMES = {
    ".git",
    ".idea",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    ".vscode",
    "__pycache__",
    "build",
    "dist",
    "env",
    "htmlcov",
    "node_modules",
    "site-packages",
    "venv",
}
_FORBIDDEN_PROJECT_IMPORT_PREFIXES = (
    "kanda_reasoner_app",
    "reasoner_tools_gui",
    "_reasoner_tools_gui",
)


def capture_tool_snapshot(tool_root: str | Path) -> ToolSnapshot:
    """Capture deterministic protected Tool files before external mutation."""
    root = Path(tool_root).expanduser().resolve(strict=True)
    entries: list[ToolFileState] = []
    for path in _iter_protected_tool_files(root):
        stat_result = path.stat()
        entries.append(
            ToolFileState(
                relative_path=path.relative_to(root).as_posix(),
                size=int(stat_result.st_size),
                sha256=_sha256_file(path),
                device=int(getattr(stat_result, "st_dev", 0) or 0),
                inode=int(getattr(stat_result, "st_ino", 0) or 0),
            )
        )
    entries.sort(key=lambda item: item.relative_path.casefold())
    digest = hashlib.sha256()
    for item in entries:
        line = (
            item.relative_path
            + "\0"
            + str(item.size)
            + "\0"
            + item.sha256
            + "\n"
        )
        digest.update(line.encode("utf-8"))
    return ToolSnapshot(
        tool_root=root,
        entries=tuple(entries),
        digest_sha256=digest.hexdigest(),
    )


def verify_tool_snapshot_unchanged(context: FireShieldContext) -> None:
    """Fail closed when protected Tool content changed during external work."""
    if context.mode is FireShieldMode.KANDA_SELF_HOSTING:
        return
    before = context.tool_snapshot
    if before is None:
        raise FireShieldError("FIRE_SHIELD_TOOL_PRE_STATE_MISSING")
    after = capture_tool_snapshot(before.tool_root)
    if after.digest_sha256 != before.digest_sha256:
        raise FireShieldError("FIRE_SHIELD_TOOL_MUTATION_DETECTED")


def assert_existing_destination_not_tool_alias(
    context: FireShieldContext,
    target: Path,
) -> None:
    """Reject an existing Project path that aliases a protected Tool file."""
    snapshot = context.tool_snapshot
    if snapshot is None or not target.exists() or not target.is_file():
        return
    try:
        target_stat = target.stat()
    except OSError as exc:
        raise FireShieldError(
            "FIRE_SHIELD_DESTINATION_IDENTITY_UNREADABLE:" + str(target)
        ) from exc
    device = int(getattr(target_stat, "st_dev", 0) or 0)
    inode = int(getattr(target_stat, "st_ino", 0) or 0)
    if device or inode:
        for item in snapshot.entries:
            if item.device == device and item.inode == inode:
                raise FireShieldError(
                    "FIRE_SHIELD_TOOL_FILE_ALIAS_BLOCKED:" + str(target)
                )
        return
    target_hash = _sha256_file(target)
    for item in snapshot.entries:
        if item.size != target_stat.st_size or item.sha256 != target_hash:
            continue
        tool_file = snapshot.tool_root / Path(item.relative_path)
        try:
            same = os.path.samefile(target, tool_file)
        except OSError:
            same = False
        if same:
            raise FireShieldError(
                "FIRE_SHIELD_TOOL_FILE_ALIAS_BLOCKED:" + str(target)
            )


def assert_payload_bytes_not_tool_copy(
    context: FireShieldContext,
    raw: bytes,
    label: str,
) -> None:
    """Reject an exact protected Tool file copied under another name."""
    if context.mode is FireShieldMode.KANDA_SELF_HOSTING:
        return
    snapshot = context.tool_snapshot
    if snapshot is None:
        raise FireShieldError("FIRE_SHIELD_TOOL_PRE_STATE_MISSING")
    digest = hashlib.sha256(raw).hexdigest()
    size = len(raw)
    for item in snapshot.entries:
        if item.size == size and item.sha256 == digest:
            raise FireShieldError(
                "FIRE_SHIELD_EXACT_TOOL_FILE_COPY_BLOCKED:"
                + label
                + ":"
                + item.relative_path
            )


def scan_project_python_source(
    context: FireShieldContext,
    raw: bytes,
    relative_path: str,
) -> None:
    """Reject private Tool imports and absolute Tool-root references."""
    if context.mode is FireShieldMode.KANDA_SELF_HOSTING:
        return
    try:
        text = raw.decode("utf-8-sig", errors="strict")
    except UnicodeDecodeError as exc:
        raise FireShieldError(
            "FIRE_SHIELD_PROJECT_PYTHON_ENCODING_INVALID:" + relative_path
        ) from exc
    try:
        tree = ast.parse(text, filename=relative_path)
    except SyntaxError as exc:
        raise FireShieldError(
            "FIRE_SHIELD_PROJECT_PYTHON_PARSE_FAILED:" + relative_path
        ) from exc
    if _source_references_tool_root(
        text,
        tree,
        context.boundary.tool_source_root,
    ):
        raise FireShieldError(
            "FIRE_SHIELD_PROJECT_TOOL_PATH_LEAK_BLOCKED:" + relative_path
        )
    for node in ast.walk(tree):
        names: list[str] = []
        if isinstance(node, ast.Import):
            names.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.append(node.module)
        for name in names:
            if _forbidden_tool_import(name):
                raise FireShieldError(
                    "FIRE_SHIELD_PROJECT_TOOL_PRIVATE_IMPORT_BLOCKED:"
                    + relative_path
                    + ":"
                    + name
                )



def _source_references_tool_root(
    text: str,
    tree: ast.AST,
    tool_root: Path,
) -> bool:
    """Detect Tool-root references across Python source representations."""
    tool_text = str(tool_root)
    if not tool_text:
        return False
    folded_source = text.casefold()
    raw_variants = {
        tool_text.casefold(),
        tool_text.replace("\\", "/").casefold(),
        tool_text.replace("\\", "\\\\").casefold(),
    }
    for variant in raw_variants:
        if variant and _contains_root_reference(folded_source, variant):
            return True
    normalized_tool = tool_text.replace("\\", "/").casefold()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Constant) or not isinstance(node.value, str):
            continue
        normalized_value = node.value.replace("\\", "/").casefold()
        if _contains_root_reference(normalized_value, normalized_tool):
            return True
    return False


def _contains_root_reference(text: str, root: str) -> bool:
    """Return whether text contains one boundary-aware root reference."""
    start = 0
    while True:
        index = text.find(root, start)
        if index < 0:
            return False
        end = index + len(root)
        if end == len(text) or text[end] in "/\\'\"` \t\r\n)]},;:":
            return True
        start = index + 1

def verify_project_import_isolation(
    context: FireShieldContext,
    search_paths: Iterable[str | Path],
) -> None:
    """Reject Tool-root search-path leakage in external Project execution."""
    if context.mode is FireShieldMode.KANDA_SELF_HOSTING:
        return
    tool_root = context.boundary.tool_source_root.resolve(strict=False)
    project_root = context.boundary.active_project_root.resolve(strict=False)
    for raw in search_paths:
        text = str(raw or "").strip()
        candidate = project_root if not text else Path(text).expanduser()
        if not candidate.is_absolute():
            candidate = (project_root / candidate).resolve(strict=False)
        else:
            candidate = candidate.resolve(strict=False)
        if _is_within(candidate, tool_root):
            raise FireShieldError(
                "FIRE_SHIELD_PROJECT_TOOL_PATH_LEAK_BLOCKED:" + str(candidate)
            )


def _forbidden_tool_import(name: str) -> bool:
    normalized = str(name or "").strip()
    return any(
        normalized == prefix or normalized.startswith(prefix + ".")
        for prefix in _FORBIDDEN_PROJECT_IMPORT_PREFIXES
    )


def _iter_protected_tool_files(root: Path) -> Iterable[Path]:
    for current_raw, directories, files in os.walk(
        root,
        topdown=True,
        followlinks=False,
    ):
        current = Path(current_raw)
        kept: list[str] = []
        for name in directories:
            if name.casefold() in _SKIP_TOOL_DIR_NAMES:
                continue
            candidate = current / name
            if candidate.is_symlink() or _is_reparse_point(candidate):
                continue
            kept.append(name)
        directories[:] = kept
        for name in files:
            path = current / name
            if path.is_symlink() or _is_reparse_point(path):
                continue
            try:
                if path.is_file():
                    yield path
            except OSError as exc:
                raise FireShieldError(
                    "FIRE_SHIELD_TOOL_SNAPSHOT_UNREADABLE:" + str(path)
                ) from exc


def _is_reparse_point(path: Path) -> bool:
    try:
        info = path.lstat()
    except OSError:
        return False
    attributes = int(getattr(info, "st_file_attributes", 0) or 0)
    flag = int(getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0) or 0)
    return bool(flag and attributes & flag)


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _is_within(path: Path, root: Path) -> bool:
    try:
        path.resolve(strict=False).relative_to(root.resolve(strict=False))
        return True
    except ValueError:
        return False
