"""Shared isolated-filesystem fixture support for Brick Wall Q20 validators."""

from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass
import hashlib
import os
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Iterable, Iterator

__all__ = [
    "FilesystemSignature",
    "IsolatedFilesystemLayout",
    "expected_external_root_read_only",
    "isolated_filesystem_fixture",
    "isolated_registered_project_fixture",
    "snapshot_path",
]


@dataclass(frozen=True)
class FilesystemSignature:
    """Deterministic signature for one protected path."""

    path: Path
    exists: bool
    kind: str
    digest: str


@dataclass(frozen=True)
class IsolatedFilesystemLayout:
    """All writable roots owned by one disposable validation fixture."""

    sandbox: Path
    source_root: Path
    support_root: Path
    transient_root: Path
    durable_evidence_root: Path

    @property
    def writable_roots(self) -> tuple[Path, ...]:
        """Return every writable fixture root."""
        return (
            self.source_root,
            self.support_root,
            self.transient_root,
            self.durable_evidence_root,
        )

    def assert_internal_and_distinct(self) -> None:
        """Require every fixture root to remain distinct and inside the sandbox."""
        resolved_sandbox = self.sandbox.resolve(strict=True)
        resolved_roots = tuple(path.resolve(strict=True) for path in self.writable_roots)
        if len(set(resolved_roots)) != len(resolved_roots):
            raise AssertionError("Q20_FIXTURE_ROOTS_NOT_PAIRWISE_DISTINCT")
        for root in resolved_roots:
            if not _is_relative_to(root, resolved_sandbox):
                raise AssertionError("Q20_FIXTURE_ROOT_OUTSIDE_SANDBOX:" + str(root))


def _is_relative_to(candidate: Path, owner: Path) -> bool:
    try:
        candidate.relative_to(owner)
    except ValueError:
        return False
    return True


def _hash_bytes(parts: Iterable[bytes]) -> str:
    digest = hashlib.sha256()
    for part in parts:
        digest.update(part)
    return digest.hexdigest()


def _path_parts(path: Path) -> Iterator[bytes]:
    if path.is_symlink():
        yield b"LINK\0"
        yield os.readlink(path).encode("utf-8", errors="surrogateescape")
        return
    if path.is_file():
        yield b"FILE\0"
        yield path.read_bytes()
        return
    if not path.is_dir():
        yield b"OTHER\0"
        stat = path.lstat()
        yield f"{stat.st_mode}:{stat.st_size}".encode("ascii")
        return
    yield b"DIR\0"
    for child in sorted(path.rglob("*"), key=lambda item: item.as_posix().casefold()):
        relative = child.relative_to(path).as_posix()
        yield relative.encode("utf-8", errors="surrogateescape")
        yield b"\0"
        if child.is_symlink():
            yield b"LINK\0"
            yield os.readlink(child).encode("utf-8", errors="surrogateescape")
        elif child.is_file():
            yield b"FILE\0"
            yield child.read_bytes()
        elif child.is_dir():
            yield b"DIR\0"
        else:
            stat = child.lstat()
            yield b"OTHER\0"
            yield f"{stat.st_mode}:{stat.st_size}".encode("ascii")


def snapshot_path(path: str | Path) -> FilesystemSignature:
    """Return an exact signature without creating or resolving a missing path."""
    candidate = Path(path).expanduser()
    if not candidate.exists() and not candidate.is_symlink():
        return FilesystemSignature(
            path=candidate,
            exists=False,
            kind="ABSENT",
            digest="ABSENT",
        )
    if candidate.is_symlink():
        kind = "SYMLINK"
    elif candidate.is_file():
        kind = "FILE"
    elif candidate.is_dir():
        kind = "DIRECTORY"
    else:
        kind = "OTHER"
    return FilesystemSignature(
        path=candidate,
        exists=True,
        kind=kind,
        digest=_hash_bytes(_path_parts(candidate)),
    )


def expected_external_root_read_only(project_root: str | Path, suffix: str) -> Path:
    """Derive the platform-specific external root without creating it."""
    root = Path(project_root).expanduser().resolve(strict=False)
    anchor = Path(root.anchor) if root.drive else root.parent
    return (anchor / (root.name + suffix)).resolve(strict=False)


def _assert_sandbox_separate(sandbox: Path, protected_paths: Iterable[Path]) -> None:
    resolved_sandbox = sandbox.resolve(strict=True)
    for protected in protected_paths:
        resolved = protected.expanduser().resolve(strict=False)
        if _is_relative_to(resolved_sandbox, resolved):
            raise AssertionError(
                "Q20_SANDBOX_INSIDE_PROTECTED_ROOT:" + str(protected)
            )
        if _is_relative_to(resolved, resolved_sandbox):
            raise AssertionError(
                "Q20_PROTECTED_ROOT_INSIDE_SANDBOX:" + str(protected)
            )


@contextmanager
def isolated_filesystem_fixture(
    *,
    protected_paths: Iterable[str | Path],
    prefix: str = "kanda_q20_fixture_",
    fixture_parent: str | Path | None = None,
) -> Iterator[IsolatedFilesystemLayout]:
    """Create one disposable sandbox and prove protected paths stay unchanged."""
    protected = tuple(Path(path).expanduser() for path in protected_paths)
    before = tuple(snapshot_path(path) for path in protected)
    parent = None if fixture_parent is None else str(Path(fixture_parent))
    sandbox_path: Path | None = None
    with TemporaryDirectory(prefix=prefix, dir=parent) as raw:
        sandbox_path = Path(raw).resolve(strict=True)
        _assert_sandbox_separate(sandbox_path, protected)
        layout = IsolatedFilesystemLayout(
            sandbox=sandbox_path,
            source_root=sandbox_path / "synthetic_source",
            support_root=sandbox_path / "synthetic_project_support",
            transient_root=sandbox_path / "synthetic_transient_garbage",
            durable_evidence_root=sandbox_path / "synthetic_durable_evidence",
        )
        for root in layout.writable_roots:
            root.mkdir(parents=True, exist_ok=False)
        layout.assert_internal_and_distinct()
        yield layout
        after = tuple(snapshot_path(path) for path in protected)
        if after != before:
            changed = [
                str(old.path)
                for old, new in zip(before, after, strict=True)
                if old != new
            ]
            raise AssertionError(
                "Q20_PROTECTED_PATH_MUTATED:" + ",".join(changed)
            )
    if sandbox_path is None or sandbox_path.exists():
        raise AssertionError("Q20_FIXTURE_CLEANUP_FAILED")

@contextmanager
def isolated_registered_project_fixture(
    *,
    tool_source_root: str | Path,
    protected_paths: Iterable[str | Path] = (),
    prefix: str = "kanda_q20_registered_fixture_",
) -> Iterator[IsolatedFilesystemLayout]:
    """Create one isolated registered Project without touching live authority."""
    from kanda_reasoner_app import project_operation_authority as authority_module
    from kanda_reasoner_app import project_support_boundary as boundary_module
    from kanda_reasoner_app.project_selection_registry import (
        ProjectSelectionRegistry,
    )

    tool_root = Path(tool_source_root).expanduser().resolve(strict=True)
    live_tool_support = boundary_module.canonical_tool_support_root(tool_root)
    protected = tuple(protected_paths) + (
        live_tool_support / "tool_project_registry" / "projects.json",
        live_tool_support / "project_error_memory",
    )
    with isolated_filesystem_fixture(
        protected_paths=protected,
        prefix=prefix,
    ) as layout:
        source_key = os.path.normcase(str(layout.source_root.resolve(strict=True)))
        original_support = boundary_module.canonical_project_support_root
        original_transient = boundary_module.canonical_transient_garbage_root
        original_registry_type = authority_module.ProjectSelectionRegistry

        def fixture_support(owner_root: str | Path) -> Path:
            candidate = Path(owner_root).expanduser().resolve(strict=False)
            if os.path.normcase(str(candidate)) == source_key:
                return layout.support_root.resolve(strict=True)
            return original_support(candidate)

        def fixture_transient(owner_root: str | Path) -> Path:
            candidate = Path(owner_root).expanduser().resolve(strict=False)
            if os.path.normcase(str(candidate)) == source_key:
                return layout.transient_root.resolve(strict=True)
            return original_transient(candidate)

        registry_path = layout.sandbox / "tool_support" / "projects.json"
        boundary_module.canonical_project_support_root = fixture_support
        boundary_module.canonical_transient_garbage_root = fixture_transient
        try:
            registry = ProjectSelectionRegistry(
                tool_source_root=tool_root,
                registry_path=registry_path,
            )
            boundary = registry.register_explicit_root(layout.source_root)
            if boundary.active_project_support_root != layout.support_root:
                raise AssertionError("Q20_REGISTERED_FIXTURE_SUPPORT_MISMATCH")
            if boundary.active_project_daily_work_root != layout.transient_root:
                raise AssertionError("Q20_REGISTERED_FIXTURE_TRANSIENT_MISMATCH")
            authority_module.ProjectSelectionRegistry = lambda **_kwargs: (
                ProjectSelectionRegistry(
                    tool_source_root=tool_root,
                    registry_path=registry_path,
                )
            )
            yield layout
        finally:
            authority_module.ProjectSelectionRegistry = original_registry_type
            boundary_module.canonical_project_support_root = original_support
            boundary_module.canonical_transient_garbage_root = original_transient

