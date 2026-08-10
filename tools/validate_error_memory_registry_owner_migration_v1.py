# project-path: tools/validate_error_memory_registry_owner_migration_v1.py
"""Validate fail-closed migration from legacy Project IDs to registry IDs."""

from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from kanda_reasoner_app.error_memory.backend import (
    ErrorMemoryBackend,
    ErrorMemoryBackendError,
)
from kanda_reasoner_app.error_memory.owner_migration import (
    restore_error_memory_owner_migration,
)
from kanda_reasoner_app.memory_ownership import MemoryOwnerContext, OwnerScope
from kanda_reasoner_app.project_support_boundary import (
    legacy_physical_project_identity,
)

OWNER_FIELDS = (
    "owner_scope",
    "owner_id",
    "owner_slug",
    "owner_root_fingerprint",
    "affected_box",
)


def _write(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def _owner(source: Path, support: Path, stable_id: str) -> MemoryOwnerContext:
    _legacy, fingerprint = legacy_physical_project_identity(source)
    return MemoryOwnerContext(
        owner_scope=OwnerScope.PROJECT,
        owner_id=stable_id,
        owner_slug=source.name,
        owner_root_fingerprint=fingerprint,
        affected_box="Project Error Memory",
        source_root=source,
        support_root=support,
    )


def _manifest(backend: ErrorMemoryBackend, owner_id: str) -> dict:
    payload = {
        "schema_version": "1.0",
        "artifact_type": "error_memory_backend_owner",
        **backend.canonical_owner_fields(),
        "store_root": str(backend.root),
    }
    payload["owner_id"] = owner_id
    return payload


def _lesson(backend: ErrorMemoryBackend, lesson_id: str, owner_id: str | None) -> dict:
    payload = {
        "schema_version": "1.0",
        "lesson_id": lesson_id,
        "status": "active",
        "symptom": "synthetic migration validation",
        "root_cause": "synthetic migration validation",
        "do_not_repeat_rule": "synthetic migration validation",
    }
    if owner_id is not None:
        payload.update(backend.canonical_owner_fields())
        payload["owner_id"] = owner_id
    return payload


def _index(backend: ErrorMemoryBackend, legacy_id: str) -> dict:
    payload = {
        "schema_version": "1.0",
        "artifact_type": "error_memory_lesson_index",
        **backend.canonical_owner_fields(),
        "lessons": [
            {
                "lesson_id": "lesson-legacy",
                "owner_scope": "PROJECT",
                "owner_id": legacy_id,
            },
            {
                "lesson_id": "lesson-ownerless",
                "owner_scope": "",
                "owner_id": "",
            },
        ],
    }
    payload["owner_id"] = legacy_id
    return payload


def _create_legacy_store(base: Path) -> tuple[ErrorMemoryBackend, str, dict[str, bytes]]:
    source = base / "kanda_reasoner"
    support = base / "kanda_reasoner_show_project_to_AI"
    source.mkdir(parents=True)
    stable_id = "stable-project-id-0001"
    backend = ErrorMemoryBackend(
        owner=_owner(source, support, stable_id),
        root=support / "project_error_memory",
    )
    backend.ensure_dirs()
    legacy_id, _fingerprint = legacy_physical_project_identity(source)
    _write(backend.root / "owner_manifest.json", _manifest(backend, legacy_id))
    _write(
        backend.lessons_dir / "lesson-legacy.json",
        _lesson(backend, "lesson-legacy", legacy_id),
    )
    _write(
        backend.lessons_dir / "lesson-ownerless.json",
        _lesson(backend, "lesson-ownerless", None),
    )
    _write(backend.index_path, _index(backend, legacy_id))
    originals = {
        path.relative_to(backend.root).as_posix(): path.read_bytes()
        for path in (
            backend.root / "owner_manifest.json",
            backend.lessons_dir / "lesson-legacy.json",
            backend.lessons_dir / "lesson-ownerless.json",
            backend.index_path,
        )
    }
    return backend, legacy_id, originals


def _latest_receipt(backend: ErrorMemoryBackend) -> Path:
    receipts = sorted(
        (backend.root / "owner_migration_history").glob("*/migration_receipt.json")
    )
    if len(receipts) != 1:
        raise AssertionError("expected exactly one migration receipt")
    return receipts[0]


def _validate_safe_migration() -> None:
    with tempfile.TemporaryDirectory(prefix="kanda-owner-migration-") as tmp:
        backend, legacy_id, originals = _create_legacy_store(Path(tmp))
        backend.write_backend_manifest()
        manifest = json.loads(
            (backend.root / "owner_manifest.json").read_text(encoding="utf-8")
        )
        if manifest["owner_id"] != backend.owner.owner_id:
            raise AssertionError("manifest stable owner ID was not installed")
        legacy_lesson = json.loads(
            (backend.lessons_dir / "lesson-legacy.json").read_text(encoding="utf-8")
        )
        if legacy_lesson["owner_id"] != backend.owner.owner_id:
            raise AssertionError("legacy lesson owner ID was not migrated")
        ownerless = json.loads(
            (backend.lessons_dir / "lesson-ownerless.json").read_text(encoding="utf-8")
        )
        if any(str(ownerless.get(key) or "") for key in OWNER_FIELDS):
            raise AssertionError("ownerless legacy lesson was relabeled")
        index = json.loads(backend.index_path.read_text(encoding="utf-8"))
        if index["owner_id"] != backend.owner.owner_id:
            raise AssertionError("index top-level owner ID was not migrated")
        if index["lessons"][0]["owner_id"] != backend.owner.owner_id:
            raise AssertionError("index lesson owner ID was not migrated")
        receipt = _latest_receipt(backend)
        receipt_payload = json.loads(receipt.read_text(encoding="utf-8"))
        if receipt_payload["legacy_owner_id"] != legacy_id:
            raise AssertionError("migration receipt legacy owner mismatch")
        if receipt_payload["migrated_lesson_count"] != 1:
            raise AssertionError("migration receipt lesson count mismatch")
        print("LEGACY_MANIFEST_REGISTRY_OWNER_MIGRATED: PASS")
        print("LEGACY_LESSON_OWNER_ID_MIGRATED: PASS")
        print("OWNERLESS_LESSON_PRESERVED: PASS")
        print("LESSON_INDEX_OWNER_RECONCILED: PASS")
        print("OWNER_MIGRATION_RECEIPT_WRITTEN: PASS")
        backend.write_backend_manifest()
        if len(list((backend.root / "owner_migration_history").glob("*/migration_receipt.json"))) != 1:
            raise AssertionError("idempotent bootstrap created another migration")
        print("OWNER_MIGRATION_IDEMPOTENT: PASS")
        restore_error_memory_owner_migration(receipt)
        for relative, original in originals.items():
            path = backend.root / Path(relative)
            if path.read_bytes() != original:
                raise AssertionError("rollback did not restore " + relative)
        print("OWNER_MIGRATION_ROLLBACK_EXACT: PASS")


def _validate_fail_closed() -> None:
    with tempfile.TemporaryDirectory(prefix="kanda-owner-migration-foreign-") as tmp:
        backend, _legacy_id, originals = _create_legacy_store(Path(tmp))
        foreign = json.loads(
            (backend.lessons_dir / "lesson-legacy.json").read_text(encoding="utf-8")
        )
        foreign["owner_id"] = "foreign-project-id"
        _write(backend.lessons_dir / "lesson-legacy.json", foreign)
        before_manifest = (backend.root / "owner_manifest.json").read_bytes()
        try:
            backend.write_backend_manifest()
        except ErrorMemoryBackendError as exc:
            if "MIGRATION_BLOCKED" not in str(exc):
                raise AssertionError("foreign lesson rejection marker missing") from exc
        else:
            raise AssertionError("foreign lesson was not rejected")
        if (backend.root / "owner_manifest.json").read_bytes() != before_manifest:
            raise AssertionError("blocked migration modified manifest")
        if originals["lessons/lesson-ownerless.json"] != (
            backend.lessons_dir / "lesson-ownerless.json"
        ).read_bytes():
            raise AssertionError("blocked migration modified unrelated lesson")
        print("FOREIGN_OR_MIXED_LESSON_MIGRATION_REJECTED: PASS")
        print("BLOCKED_MIGRATION_ZERO_PARTIAL_WRITE: PASS")



def _validate_live_project(project_root: Path) -> None:
    from kanda_reasoner_app.error_memory.backend import (
        project_error_memory_backend,
    )
    from kanda_reasoner_app.error_memory.store import (
        bootstrap_error_memory_store,
    )
    from kanda_reasoner_app.project_selection_registry import (
        ProjectSelectionRegistry,
    )

    backend = project_error_memory_backend(
        project_root,
        tool_source_root=project_root,
    )
    registry = ProjectSelectionRegistry(tool_source_root=project_root)
    record = registry.load_current_record()
    if record is None:
        raise AssertionError("live Project registry record missing")
    bootstrap_error_memory_store(backend)
    manifest = json.loads(
        (backend.root / "owner_manifest.json").read_text(encoding="utf-8-sig")
    )
    if manifest.get("owner_id") != record.stable_project_id:
        raise AssertionError("live manifest does not use registry stable ID")
    legacy_id, _fingerprint = legacy_physical_project_identity(project_root)
    legacy_count = 0
    foreign_count = 0
    ownerless_count = 0
    for path in sorted(backend.lessons_dir.glob("lesson-*.json")):
        payload = json.loads(path.read_text(encoding="utf-8-sig"))
        supplied = {
            key: str(payload.get(key) or "").strip()
            for key in OWNER_FIELDS
        }
        if not any(supplied.values()):
            ownerless_count += 1
            continue
        if supplied.get("owner_id") == legacy_id:
            legacy_count += 1
            continue
        if any(
            supplied.get(key) != backend.canonical_owner_fields()[key]
            for key in OWNER_FIELDS
        ):
            foreign_count += 1
    if legacy_count:
        raise AssertionError(f"live legacy owner lessons remain: {legacy_count}")
    if foreign_count:
        raise AssertionError(f"live foreign owner lessons found: {foreign_count}")
    index = json.loads(backend.index_path.read_text(encoding="utf-8-sig"))
    if index.get("owner_id") != record.stable_project_id:
        raise AssertionError("live index does not use registry stable ID")
    receipts = sorted(
        (backend.root / "owner_migration_history").glob("*/migration_receipt.json")
    )
    if not receipts:
        raise AssertionError("live migration receipt missing")
    latest = json.loads(receipts[-1].read_text(encoding="utf-8-sig"))
    if latest.get("stable_owner_id") != record.stable_project_id:
        raise AssertionError("live migration receipt stable ID mismatch")
    print("LIVE_OWNER_MANIFEST_REGISTRY_ID: PASS")
    print("LIVE_LEGACY_OWNER_LESSON_COUNT_ZERO: PASS")
    print("LIVE_FOREIGN_OWNER_LESSON_COUNT_ZERO: PASS")
    print(f"LIVE_OWNERLESS_LESSON_COUNT: {ownerless_count}")
    print("LIVE_LESSON_INDEX_REGISTRY_ID: PASS")
    print("LIVE_OWNER_MIGRATION_RECEIPT: PASS")

    if os.name == "nt":
        os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
        windows_fonts = Path(os.environ.get("WINDIR", "C:/Windows")) / "Fonts"
        if windows_fonts.is_dir():
            os.environ.setdefault("QT_QPA_FONTDIR", str(windows_fonts))
        from PySide6.QtWidgets import QApplication
        from kanda_reasoner_app.error_memory_gui.error_memory_tab import (
            ErrorMemoryTab,
        )

        app = QApplication.instance() or QApplication([])
        widget = ErrorMemoryTab()
        app.processEvents()
        widget.close()
        widget.deleteLater()
        app.processEvents()
        print("LIVE_ERROR_MEMORY_TAB_BOOTSTRAP: PASS")


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--live-project-root", default="")
    return parser.parse_args()

def _validate_source_contract() -> None:
    source_files = (
        ROOT / "kanda_reasoner_app/error_memory/owner_migration.py",
        ROOT / "kanda_reasoner_app/error_memory/backend.py",
        ROOT / "kanda_reasoner_app/project_support_boundary.py",
        Path(__file__).resolve(),
    )
    for path in source_files:
        line_count = len(path.read_text(encoding="utf-8").splitlines())
        if not 101 <= line_count <= 499:
            raise AssertionError(f"module size out of range: {path}:{line_count}")
    print("TOUCHED_SOURCE_MODULES_STRICTLY_101_TO_499: PASS")


def main() -> int:
    args = _parse_args()
    _validate_safe_migration()
    _validate_fail_closed()
    _validate_source_contract()
    if str(args.live_project_root).strip():
        _validate_live_project(Path(args.live_project_root).resolve())
    print("VALIDATION OK: error-memory-registry-owner-migration-v1")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
