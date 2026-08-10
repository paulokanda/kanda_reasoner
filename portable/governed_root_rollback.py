"""Exact backup, mutation detection, and rollback for governed owner roots."""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import stat
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from portable.constants import PROJECT_SNAPSHOT_IGNORES
from portable.errors import PortableBuildError
from portable.models import BuildPaths, ProtectedRoot
from portable.registry_boundary import assert_registry_unchanged

_BLOCK_SIZE = 1024 * 1024
_TOOL_TRANSIENT_ALLOWED_TOP_LEVEL = {"portable_build"}


@dataclass(frozen=True)
class RootViewPolicy:
    """One protected root plus the bounded paths excluded from its guarded view."""

    protected_root: ProtectedRoot
    ignored_names: frozenset[str]
    excluded_top_level: frozenset[str]


@dataclass(frozen=True)
class RootBackupEvidence:
    """Verified baseline and archive identity for one governed root view."""

    policy: RootViewPolicy
    baseline: dict[str, Any]
    archive_path: Path | None
    archive_sha256: str


@dataclass
class GovernedRootRollbackGuard:
    """Verified exact backups for every registered governed root view."""

    paths: BuildPaths
    backups: tuple[RootBackupEvidence, ...]
    manifest_path: Path

    def checkpoint(self, label: str) -> dict[str, Any]:
        """Restore every changed governed view and fail closed on any mutation."""

        assert_registry_unchanged(self.paths.registry_boundary)
        changed = self._changed_backups()
        if not changed:
            print(f"{label}: PASS")
            return {
                "label": label,
                "status": "UNCHANGED",
                "changed_root_count": 0,
                "restored_root_count": 0,
            }

        restored = self._restore_changed(changed)
        assert_registry_unchanged(self.paths.registry_boundary)
        names = ", ".join(item.policy.protected_root.label for item in changed)
        print("PORTABLE GOVERNED ROOT MUTATION DETECTED: PASS")
        print("PORTABLE GOVERNED ROOT EXACT ROLLBACK: PASS")
        raise PortableBuildError(
            f"{label} detected governed-root mutation and restored the exact "
            f"baseline tree: {names}; restored={restored}"
        )

    def restore_if_changed(self, label: str) -> dict[str, Any]:
        """Best-effort exception-path rollback with exact post-restore verification."""

        changed = self._changed_backups()
        if not changed:
            print(f"{label}: NO GOVERNED ROOT MUTATION")
            return {
                "label": label,
                "status": "UNCHANGED",
                "changed_root_count": 0,
                "restored_root_count": 0,
            }
        restored = self._restore_changed(changed)
        print(f"{label}: PASS")
        print("PORTABLE FAILURE-PATH GOVERNED ROOT ROLLBACK: PASS")
        return {
            "label": label,
            "status": "RESTORED",
            "changed_root_count": len(changed),
            "restored_root_count": restored,
        }

    def evidence(self) -> dict[str, Any]:
        """Return receipt-safe baseline and backup identities."""

        return {
            "schema_version": "1.0",
            "manifest_path": str(self.manifest_path),
            "manifest_sha256": _sha256_file(self.manifest_path),
            "registered_projects_snapshot": True,
            "protected_root_count": len(self.backups),
            "roots": [
                {
                    "label": item.policy.protected_root.label,
                    "owner_id": item.policy.protected_root.owner_id,
                    "owner_slug": item.policy.protected_root.owner_slug,
                    "root_kind": item.policy.protected_root.root_kind,
                    "path": str(item.policy.protected_root.path),
                    "baseline_tree_sha256": item.baseline["tree_sha256"],
                    "baseline_file_count": item.baseline["file_count"],
                    "baseline_directory_count": item.baseline["directory_count"],
                    "archive_path": str(item.archive_path) if item.archive_path else "",
                    "archive_sha256": item.archive_sha256,
                    "ignored_names": sorted(item.policy.ignored_names),
                    "excluded_top_level": sorted(item.policy.excluded_top_level),
                }
                for item in self.backups
            ],
        }

    def _changed_backups(self) -> list[RootBackupEvidence]:
        changed: list[RootBackupEvidence] = []
        for backup in self.backups:
            current = _inventory(backup.policy)
            if current != backup.baseline:
                changed.append(backup)
        return changed

    def _restore_changed(self, changed: list[RootBackupEvidence]) -> int:
        restored = 0
        for backup in changed:
            _restore_backup(backup)
            current = _inventory(backup.policy)
            if current != backup.baseline:
                raise PortableBuildError(
                    "Exact governed-root rollback verification failed: "
                    + backup.policy.protected_root.label
                )
            restored += 1
        return restored


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(_BLOCK_SIZE), b""):
            digest.update(block)
    return digest.hexdigest()


def _is_reparse_point(path: Path) -> bool:
    if path.is_symlink():
        return True
    try:
        attributes = os.lstat(path).st_file_attributes
    except (AttributeError, OSError):
        return False
    return bool(attributes & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400))


def _excluded(relative: Path, policy: RootViewPolicy) -> bool:
    if relative.parts and relative.parts[0].casefold() in policy.excluded_top_level:
        return True
    return any(part.casefold() in policy.ignored_names for part in relative.parts)


def _records(policy: RootViewPolicy) -> list[dict[str, Any]]:
    root = policy.protected_root.path
    if not root.exists():
        return []
    if not root.is_dir() or _is_reparse_point(root):
        raise PortableBuildError(
            f"Governed root is not a normal directory: {root}"
        )

    result: list[dict[str, Any]] = []
    for current_root, directories, files in os.walk(root, topdown=True):
        current = Path(current_root)
        kept_directories: list[str] = []
        for name in sorted(directories, key=str.casefold):
            path = current / name
            relative = path.relative_to(root)
            if _excluded(relative, policy):
                continue
            if _is_reparse_point(path):
                raise PortableBuildError(
                    f"Governed root contains a reparse point: {path}"
                )
            kept_directories.append(name)
            result.append({"kind": "D", "path": relative.as_posix()})
        directories[:] = kept_directories

        for name in sorted(files, key=str.casefold):
            path = current / name
            relative = path.relative_to(root)
            if _excluded(relative, policy):
                continue
            if _is_reparse_point(path):
                raise PortableBuildError(
                    f"Governed root contains a reparse point: {path}"
                )
            result.append(
                {
                    "kind": "F",
                    "path": relative.as_posix(),
                    "size": path.stat().st_size,
                    "sha256": _sha256_file(path),
                }
            )
    return sorted(result, key=lambda item: (item["path"].casefold(), item["kind"]))


def _inventory(policy: RootViewPolicy) -> dict[str, Any]:
    root = policy.protected_root.path
    records = _records(policy)
    encoded = json.dumps(
        records,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return {
        "exists": root.exists(),
        "tree_sha256": hashlib.sha256(encoded).hexdigest(),
        "file_count": sum(item["kind"] == "F" for item in records),
        "directory_count": sum(item["kind"] == "D" for item in records),
        "records": records,
    }


def _policy(paths: BuildPaths, protected_root: ProtectedRoot) -> RootViewPolicy:
    ignored_names: set[str] = set()
    excluded_top_level: set[str] = set()
    if protected_root.root_kind == "PROJECT_ROOT":
        ignored_names.update(item.casefold() for item in PROJECT_SNAPSHOT_IGNORES)
    if protected_root.path == paths.transient_root:
        excluded_top_level.update(_TOOL_TRANSIENT_ALLOWED_TOP_LEVEL)
    return RootViewPolicy(
        protected_root=protected_root,
        ignored_names=frozenset(ignored_names),
        excluded_top_level=frozenset(excluded_top_level),
    )


def _write_archive(policy: RootViewPolicy, destination: Path) -> str:
    root = policy.protected_root.path
    destination.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(
        destination,
        mode="w",
        compression=zipfile.ZIP_DEFLATED,
        compresslevel=9,
    ) as archive:
        for record in _records(policy):
            relative = record["path"]
            if record["kind"] == "D":
                info = zipfile.ZipInfo(relative.rstrip("/") + "/")
                archive.writestr(info, b"")
            else:
                archive.write(root / relative, relative)
    with zipfile.ZipFile(destination, "r") as archive:
        bad = archive.testzip()
        if bad:
            raise PortableBuildError(f"Governed-root backup CRC failed: {bad}")
    return _sha256_file(destination)


def _safe_member(name: str) -> Path:
    normalized = name.replace("\\", "/")
    relative = Path(normalized)
    if not normalized or normalized.startswith("/") or ".." in relative.parts:
        raise PortableBuildError(f"Unsafe governed-root backup member: {name}")
    if len(normalized) >= 2 and normalized[1] == ":":
        raise PortableBuildError(f"Absolute governed-root backup member: {name}")
    return relative


def _verification_inventory(archive_path: Path, root: Path) -> dict[str, Any]:
    if root.exists():
        shutil.rmtree(root)
    root.mkdir(parents=True)
    with zipfile.ZipFile(archive_path, "r") as archive:
        for info in archive.infolist():
            relative = _safe_member(info.filename)
            target = root / relative
            if info.is_dir():
                target.mkdir(parents=True, exist_ok=True)
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                with archive.open(info, "r") as source, target.open("wb") as output:
                    shutil.copyfileobj(source, output)
    policy = RootViewPolicy(
        protected_root=ProtectedRoot(
            label="backup verification",
            owner_id="verification",
            owner_slug="verification",
            root_kind="PROJECT_ROOT",
            path=root,
        ),
        ignored_names=frozenset(),
        excluded_top_level=frozenset(),
    )
    return _inventory(policy)


def _remove_guarded_view(policy: RootViewPolicy) -> None:
    root = policy.protected_root.path
    if not root.exists():
        return
    files: list[Path] = []
    directories: list[Path] = []
    for current_root, directory_names, file_names in os.walk(root, topdown=True):
        current = Path(current_root)
        kept: list[str] = []
        for name in directory_names:
            path = current / name
            relative = path.relative_to(root)
            if _excluded(relative, policy):
                continue
            kept.append(name)
            directories.append(path)
        directory_names[:] = kept
        for name in file_names:
            path = current / name
            relative = path.relative_to(root)
            if not _excluded(relative, policy):
                files.append(path)
    for path in files:
        path.unlink(missing_ok=True)
    for path in sorted(directories, key=lambda item: len(item.parts), reverse=True):
        try:
            path.rmdir()
        except OSError:
            pass


def _restore_backup(backup: RootBackupEvidence) -> None:
    policy = backup.policy
    root = policy.protected_root.path
    _remove_guarded_view(policy)
    if not backup.baseline["exists"]:
        if root.exists() and not any(root.iterdir()):
            root.rmdir()
        return
    root.mkdir(parents=True, exist_ok=True)
    if backup.archive_path is None or not backup.archive_path.is_file():
        raise PortableBuildError(
            f"Governed-root backup archive is missing: {policy.protected_root.label}"
        )
    if _sha256_file(backup.archive_path) != backup.archive_sha256:
        raise PortableBuildError(
            f"Governed-root backup archive hash changed: {policy.protected_root.label}"
        )
    with zipfile.ZipFile(backup.archive_path, "r") as archive:
        for info in archive.infolist():
            relative = _safe_member(info.filename)
            target = root / relative
            if info.is_dir():
                target.mkdir(parents=True, exist_ok=True)
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                with archive.open(info, "r") as source, target.open("wb") as output:
                    shutil.copyfileobj(source, output)


def prepare_governed_root_rollback(paths: BuildPaths) -> GovernedRootRollbackGuard:
    """Back up all registered_projects governed views and prove exact restoration data."""

    boundary = paths.registry_boundary
    if boundary is None:
        raise PortableBuildError("Registry boundary is required for governed-root backup.")
    assert_registry_unchanged(boundary)
    backup_root = paths.run_root / "governed_root_rollback"
    verification_root = backup_root / "verification"
    backup_root.mkdir(parents=True, exist_ok=True)

    backups: list[RootBackupEvidence] = []
    manifest_roots: list[dict[str, Any]] = []
    for index, protected_root in enumerate(boundary.protected_roots, start=1):
        policy = _policy(paths, protected_root)
        before = _inventory(policy)
        archive_path: Path | None = None
        archive_sha = ""
        if before["exists"]:
            archive_path = backup_root / f"root_{index:03d}.zip"
            archive_sha = _write_archive(policy, archive_path)
            after_backup = _inventory(policy)
            if after_backup != before:
                raise PortableBuildError(
                    "Governed root changed while its rollback archive was created: "
                    + protected_root.label
                )
            verification = _verification_inventory(
                archive_path,
                verification_root / f"root_{index:03d}",
            )
            if verification["records"] != before["records"]:
                raise PortableBuildError(
                    "Governed-root rollback archive verification failed: "
                    + protected_root.label
                )
        evidence = RootBackupEvidence(
            policy=policy,
            baseline=before,
            archive_path=archive_path,
            archive_sha256=archive_sha,
        )
        backups.append(evidence)
        manifest_roots.append(
            {
                "label": protected_root.label,
                "owner_id": protected_root.owner_id,
                "owner_slug": protected_root.owner_slug,
                "root_kind": protected_root.root_kind,
                "path": str(protected_root.path),
                "baseline_tree_sha256": before["tree_sha256"],
                "archive_path": str(archive_path) if archive_path else "",
                "archive_sha256": archive_sha,
                "ignored_names": sorted(policy.ignored_names),
                "excluded_top_level": sorted(policy.excluded_top_level),
            }
        )

    shutil.rmtree(verification_root, ignore_errors=True)
    manifest_path = backup_root / "governed_root_rollback_manifest.json"
    manifest_path.write_text(
        json.dumps(
            {
                "schema_version": "1.0",
                "artifact_type": "portable_governed_root_rollback_manifest",
                "registry_path": str(boundary.registry_path),
                "registry_sha256": boundary.registry_sha256,
                "registered_projects_snapshot": True,
                "protected_root_count": len(backups),
                "roots": manifest_roots,
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
        newline="\n",
    )
    json.loads(manifest_path.read_text(encoding="utf-8"))
    assert_registry_unchanged(boundary)
    print("PORTABLE GOVERNED ROOT BASELINE SNAPSHOTS: PASS")
    print("PORTABLE GOVERNED ROOT EXACT BACKUPS: PASS")
    print("PORTABLE GOVERNED ROOT BACKUP RESTORE PROOF: PASS")
    print("PORTABLE TOOL TRANSIENT BUILD LANE EXCLUSION: PASS")
    return GovernedRootRollbackGuard(
        paths=paths,
        backups=tuple(backups),
        manifest_path=manifest_path,
    )
