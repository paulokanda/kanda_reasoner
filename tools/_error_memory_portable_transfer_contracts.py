#!/usr/bin/env python3
"""Functional contracts for portable Error Memory backup and merge."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import tempfile

from tools._error_memory_portable_transfer_fixtures import (
    expected_dynamic_lessons_dir,
    isolated_project_roots,
    lesson_fixture,
)


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _saved_bytes(root: Path) -> dict[str, bytes]:
    from kanda_reasoner_app.error_memory.paths import (
        resolve_error_memory_lessons_dir,
    )

    return {
        path.name: path.read_bytes()
        for path in resolve_error_memory_lessons_dir(root).glob(
            "lesson-*.json"
        )
        if path.is_file()
    }


def run_complete_backup_contract() -> None:
    """Prove backup is uncapped, complete, byte-preserving, and atomic."""
    from kanda_reasoner_app.error_memory.paths import (
        resolve_error_memory_lessons_dir,
    )
    from kanda_reasoner_app.error_memory.store import save_lesson
    from kanda_reasoner_app.error_memory_gui._portable_transfer import (
        ERROR_MEMORY_EXPORT_MANIFEST,
        export_error_lessons_folder,
    )

    with tempfile.TemporaryDirectory(
        prefix="kanda_error_memory_backup_"
    ) as temp:
        base = Path(temp)
        destination = base / "backup_exports"
        destination.mkdir()
        with isolated_project_roots(
            base,
            "backup_source_project",
        ) as roots:
            source_root = roots[0]
            statuses = (
                "active",
                "draft",
                "deprecated",
                "superseded",
            )
            for index in range(12):
                status = statuses[index % len(statuses)]
                lesson = lesson_fixture(
                    source_root,
                    lesson_id=(
                        "lesson-complete-backup-"
                        + str(index).zfill(2)
                        + "-v1"
                    ),
                    raw_error=(
                        "Complete backup fixture "
                        + str(index).zfill(2)
                    ),
                    status=status,
                )
                if status == "superseded":
                    lesson["superseded_by"] = (
                        "lesson-complete-backup-00-v1"
                    )
                save_lesson(source_root, lesson)

            source_before = _saved_bytes(source_root)
            exported = export_error_lessons_folder(
                source_root,
                destination,
            )
            export_root = Path(exported["export_folder"])
            manifest_path = export_root / ERROR_MEMORY_EXPORT_MANIFEST
            manifest = json.loads(
                manifest_path.read_text(encoding="utf-8")
            )
            _require(
                exported["exported_count"] == 12,
                "backup export was capped below all lessons",
            )
            _require(
                exported["source_lesson_count"] == 12,
                "source lesson count mismatch",
            )
            _require(
                exported["backup_complete"] is True,
                "backup incomplete",
            )
            _require(
                exported["compact_limit_applied"] is False,
                "compact cap reached backup export",
            )
            _require(
                manifest["lesson_count"] == 12,
                "backup manifest lost lessons",
            )
            _require(
                manifest["backup_contract"]
                == {
                    "compact_limit_applied": False,
                    "partial_success_allowed": False,
                    "preserve_source_bytes": True,
                    "scope": "all_valid_saved_lessons",
                    "status_filter": "none",
                },
                "backup manifest contract mismatch",
            )
            statuses_found = {
                entry["status"] for entry in manifest["lessons"]
            }
            _require(
                statuses_found
                == {"active", "draft", "deprecated", "superseded"},
                "backup did not include every lesson status",
            )
            for entry in manifest["lessons"]:
                filename = entry["file"]
                backup_bytes = (
                    export_root / "lessons" / filename
                ).read_bytes()
                _require(
                    backup_bytes == source_before[filename],
                    "backup changed lesson bytes: " + filename,
                )
            _require(
                _saved_bytes(source_root) == source_before,
                "backup changed source lessons",
            )

            lessons_dir = resolve_error_memory_lessons_dir(source_root)
            _require(
                lessons_dir == expected_dynamic_lessons_dir(source_root),
                "fixture did not use the dynamic support root",
            )
            invalid_path = next(
                iter(lessons_dir.glob("lesson-*.json")),
                None,
            )
            _require(
                invalid_path is not None,
                "fixture lesson was not written to the dynamic store",
            )
            original = invalid_path.read_bytes()
            invalid_path.write_text("{}", encoding="utf-8")
            existing_exports = {
                path.name for path in destination.iterdir()
            }
            try:
                export_error_lessons_folder(source_root, destination)
            except ValueError:
                pass
            else:
                raise AssertionError(
                    "invalid lesson produced a partial backup"
                )
            finally:
                invalid_path.write_bytes(original)
            _require(
                {path.name for path in destination.iterdir()}
                == existing_exports,
                "failed backup left a partial export folder",
            )

        print("ERROR_MEMORY_EXPORT_COMPLETE_BACKUP_ALL_LESSONS: PASS")
        print("ERROR_MEMORY_EXPORT_NO_COMPACT_CAP: PASS")
        print("ERROR_MEMORY_EXPORT_ALL_OR_NOTHING: PASS")
        print("ERROR_MEMORY_FIXTURE_DYNAMIC_PATH: PASS")
        print("ERROR_MEMORY_FIXTURE_SUPPORT_CLEANUP: PASS")


def run_functional_contract() -> None:
    """Prove merge-only import, duplicate rejection, and dynamic ownership."""
    from kanda_reasoner_app.error_memory.paths import (
        resolve_error_memory_lessons_dir,
    )
    from kanda_reasoner_app.error_memory.store import list_lessons, save_lesson
    from kanda_reasoner_app.error_memory_gui._portable_transfer import (
        ERROR_MEMORY_EXPORT_MANIFEST,
        export_error_lessons_folder,
        import_error_lessons_folder,
    )

    with tempfile.TemporaryDirectory(
        prefix="kanda_error_memory_transfer_"
    ) as temp:
        base = Path(temp)
        destination = base / "portable_exports"
        destination.mkdir()
        with isolated_project_roots(
            base,
            "source_project",
            "target_project",
        ) as roots:
            source_root, target_root = roots
            alpha = lesson_fixture(
                source_root,
                lesson_id="lesson-portable-alpha-v1",
                raw_error="Portable alpha unique source error.",
            )
            beta = lesson_fixture(
                source_root,
                lesson_id="lesson-portable-beta-v1",
                raw_error="Portable beta source error.",
                status="deprecated",
            )
            gamma = lesson_fixture(
                source_root,
                lesson_id="lesson-portable-gamma-v1",
                raw_error="Portable gamma source error.",
                fingerprint_hash="portable-shared-fingerprint-v1",
            )
            family_duplicate = lesson_fixture(
                source_root,
                lesson_id="lesson-portable-family-source-v1",
                raw_error="Portable canonical family duplicate error.",
                fingerprint_hash=(
                    "portable-family-source-fingerprint-v1"
                ),
            )
            for lesson in (alpha, beta, gamma, family_duplicate):
                save_lesson(source_root, lesson)

            current_beta = lesson_fixture(
                target_root,
                lesson_id="lesson-portable-beta-v1",
                raw_error="Target project owns the current beta lesson.",
            )
            current_fingerprint = lesson_fixture(
                target_root,
                lesson_id="lesson-target-current-fingerprint-v1",
                raw_error=(
                    "Target project owns the current fingerprint lesson."
                ),
                fingerprint_hash="portable-shared-fingerprint-v1",
            )
            current_only = lesson_fixture(
                target_root,
                lesson_id="lesson-target-current-only-v1",
                raw_error="Target-only lesson must remain byte identical.",
            )
            current_family = lesson_fixture(
                target_root,
                lesson_id="lesson-target-current-family-v1",
                raw_error="Portable canonical family duplicate error.",
                fingerprint_hash=(
                    "portable-family-target-fingerprint-v1"
                ),
            )
            for lesson in (
                current_beta,
                current_fingerprint,
                current_only,
                current_family,
            ):
                save_lesson(target_root, lesson)

            source_before = _saved_bytes(source_root)
            target_before = _saved_bytes(target_root)
            exported = export_error_lessons_folder(
                source_root,
                destination,
            )
            export_root = Path(exported["export_folder"])
            manifest_path = export_root / ERROR_MEMORY_EXPORT_MANIFEST
            manifest = json.loads(
                manifest_path.read_text(encoding="utf-8")
            )
            _require(
                exported["exported_count"] == 4,
                "export did not include every valid status",
            )
            _require(
                manifest["lesson_count"] == 4,
                "manifest count mismatch",
            )
            _require(
                {
                    entry["status"]
                    for entry in manifest["lessons"]
                }
                == {"draft", "deprecated"},
                "export did not preserve lesson statuses",
            )
            for entry in manifest["lessons"]:
                filename = entry["file"]
                exported_bytes = (
                    export_root / "lessons" / filename
                ).read_bytes()
                _require(
                    exported_bytes == source_before[filename],
                    "export did not preserve exact lesson bytes: "
                    + filename,
                )
            _require(
                _saved_bytes(source_root) == source_before,
                "export modified source lessons",
            )
            print("ERROR_MEMORY_EXPORT_FOLDER_CONTRACT: PASS")
            print("ERROR_MEMORY_EXPORT_ALL_STATUSES: PASS")
            print("ERROR_MEMORY_EXPORT_SOURCE_READ_ONLY: PASS")

            imported = import_error_lessons_folder(
                target_root,
                export_root,
            )
            _require(
                imported["imported_count"] == 1,
                "unique import count wrong",
            )
            _require(
                imported["duplicate_count"] == 3,
                "duplicate count wrong",
            )
            _require(
                imported["current_lessons_deleted"] == 0,
                "lessons deleted",
            )
            _require(
                imported["current_lessons_replaced"] == 0,
                "lessons replaced",
            )
            target_after = _saved_bytes(target_root)
            for filename, raw in target_before.items():
                _require(
                    target_after.get(filename) == raw,
                    "current lesson changed: " + filename,
                )
            lessons = list_lessons(target_root, include_inactive=True)
            by_id = {
                str(item.get("lesson_id") or ""): item
                for item in lessons
            }
            imported_alpha = by_id.get("lesson-portable-alpha-v1")
            _require(
                imported_alpha is not None,
                "unique lesson was not imported",
            )
            _require(
                imported_alpha.get("project_slug") == target_root.name,
                "imported lesson is not target-owned",
            )
            provenance = imported_alpha.get("transfer_provenance")
            _require(
                isinstance(provenance, dict),
                "transfer provenance missing",
            )
            _require(
                provenance.get("source_project_slug") == source_root.name,
                "source project provenance missing",
            )
            reasons = {
                item.get("reason") for item in imported["duplicates"]
            }
            _require(
                "same lesson_id" in reasons,
                "same-ID duplicate missed",
            )
            _require(
                "same fingerprint.fingerprint_hash" in reasons,
                "same-fingerprint duplicate missed",
            )
            _require(
                "canonical duplicate-family match" in reasons,
                "canonical-family duplicate missed",
            )
            print("ERROR_MEMORY_IMPORT_MERGE_ONLY: PASS")
            print("ERROR_MEMORY_IMPORT_DUPLICATE_ID_SKIPPED: PASS")
            print(
                "ERROR_MEMORY_IMPORT_DUPLICATE_FINGERPRINT_SKIPPED: PASS"
            )
            print("ERROR_MEMORY_IMPORT_DUPLICATE_FAMILY_SKIPPED: PASS")
            print("ERROR_MEMORY_IMPORT_CURRENT_LESSONS_UNCHANGED: PASS")
            print("ERROR_MEMORY_IMPORT_TARGET_PROJECT_OWNERSHIP: PASS")

            second = import_error_lessons_folder(
                target_root,
                export_root / "lessons",
            )
            _require(
                second["imported_count"] == 0,
                "re-import created duplicates",
            )
            _require(
                second["duplicate_count"] == 4,
                "re-import skip count wrong",
            )
            _require(
                _saved_bytes(target_root) == target_after,
                "re-import changed target lessons",
            )
            print("ERROR_MEMORY_IMPORT_REIMPORT_IDEMPOTENT: PASS")

            invalid_export = (
                export_root / "lessons" / "lesson-invalid.json"
            )
            invalid_export.write_text("{}", encoding="utf-8")
            manifest["lessons"].append(
                {
                    "lesson_id": "lesson-invalid",
                    "status": "draft",
                    "file": invalid_export.name,
                    "sha256": _sha256(invalid_export),
                    "size_bytes": invalid_export.stat().st_size,
                }
            )
            manifest["lesson_count"] = len(manifest["lessons"])
            manifest_path.write_text(
                json.dumps(manifest, indent=2, sort_keys=True),
                encoding="utf-8",
            )
            invalid_result = import_error_lessons_folder(
                target_root,
                export_root,
            )
            _require(
                invalid_result["invalid_count"] == 1,
                "invalid lesson not skipped",
            )
            _require(
                invalid_result["imported_count"] == 0,
                "invalid lesson imported",
            )
            _require(
                _saved_bytes(target_root) == target_after,
                "invalid import changed target lessons",
            )
            print("ERROR_MEMORY_IMPORT_INVALID_LESSON_SKIPPED: PASS")

            target_dir = resolve_error_memory_lessons_dir(target_root)
            _require(
                target_dir == expected_dynamic_lessons_dir(target_root),
                "dynamic target folder is wrong",
            )
            _require(
                not (target_root / "project_error_memory").exists(),
                "import wrote Error Memory inside selected project source",
            )
            _require(
                len(list(target_dir.glob("lesson-*.json"))) == 5,
                "target lesson count is wrong",
            )
            print("ERROR_MEMORY_IMPORT_DYNAMIC_SHOW_PROJECT_TARGET: PASS")
            print("ERROR_MEMORY_IMPORT_NO_PROJECT_SOURCE_WRITE: PASS")
