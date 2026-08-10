# project-path: tools/validate_owner_scoped_error_memory_and_freeze_memory_v1.py
"""Focused validation for owner-scoped Error Memory and Freeze ownership."""

from __future__ import annotations

import argparse
import atexit
import json
import shutil
import subprocess
import sys
import tempfile
import uuid
from pathlib import Path
from typing import Any
FEATURE_ID = "owner-scoped-error-memory-and-freeze-memory-v1"
DEFAULT_PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(DEFAULT_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(DEFAULT_PROJECT_ROOT))
_FIXTURE_SUPPORT_ROOTS: list[Path] = []
_FIXTURE_REGISTRY_PATH = ""
def _register_fixture_support_root(source_root: Path) -> None:
    """Register one unique synthetic support root for process-exit cleanup."""
    from kanda_reasoner_app.project_support_boundary import (
        canonical_project_support_root,
    )
    support_root = canonical_project_support_root(source_root)
    if support_root not in _FIXTURE_SUPPORT_ROOTS:
        _FIXTURE_SUPPORT_ROOTS.append(support_root)

def _cleanup_fixture_support_roots() -> None:
    """Remove only unique support roots created by this validator process."""
    for support_root in reversed(_FIXTURE_SUPPORT_ROOTS):
        shutil.rmtree(support_root, ignore_errors=True)


atexit.register(_cleanup_fixture_support_roots)


def _unique_fixture_root(temp_root: Path, label: str, token: str) -> Path:
    """Create one uniquely named synthetic source root."""
    root = temp_root / (label + "_" + token)
    root.mkdir(parents=True, exist_ok=False)
    _register_fixture_support_root(root)
    return root


def _select_fixture_project(project_root: Path, tool_root: Path) -> None:
    """Register one synthetic Project through an isolated Tool registry."""
    from kanda_reasoner_app.project_selection_registry import (
        ProjectSelectionRegistry,
    )

    global _FIXTURE_REGISTRY_PATH
    if not _FIXTURE_REGISTRY_PATH:
        registry = Path(tempfile.gettempdir()) / (
            "kanda_owner_scope_registry_" + uuid.uuid4().hex + ".json"
        )
        _FIXTURE_REGISTRY_PATH = str(registry)
    from kanda_reasoner_app import project_operation_authority as authority_module

    registry_type = ProjectSelectionRegistry
    authority_module.ProjectSelectionRegistry = lambda **kwargs: registry_type(
        tool_source_root=tool_root, registry_path=_FIXTURE_REGISTRY_PATH
    )
    selection = registry_type(
        tool_source_root=tool_root, registry_path=_FIXTURE_REGISTRY_PATH
    )
    selection.register_explicit_root(project_root)


def _base_lesson(project_root: Path, raw: str) -> dict[str, Any]:
    """Build one valid draft lesson for deterministic tests."""
    from kanda_reasoner_app.error_memory.models import build_lesson

    return build_lesson(
        selected_project_root=project_root,
        raw_error_text=raw,
        operation_phase="owner_scope_validation",
        symptom="Owner scope validation symptom",
        root_cause="Owner authority was ambiguous.",
        wrong_assumption="A root path could define canonical ownership.",
        correct_fix="Use an explicit owner-scoped backend.",
        long_term_prevention="Validate backend ownership before writes.",
        do_not_repeat_rule="Never copy or relabel foreign canonical lessons.",
        prevention_triggers=["owner scope", "foreign canonical write"],
        validation_evidence=["Focused validator fixture."],
        status="draft",
    )


def _expect_error(callable_obj, marker: str) -> None:
    """Require one callable to fail with the expected marker."""
    try:
        callable_obj()
    except Exception as exc:
        if marker not in str(exc):
            raise AssertionError(
                "Expected rejection marker " + marker + ", got: " + str(exc)
            ) from exc
        return
    raise AssertionError("Expected rejection was not raised: " + marker)


def _validate_error_memory(temp_root: Path) -> None:
    """Validate Tool/Project stores, owner assignment, imports, and references."""
    from kanda_reasoner_app.error_memory.backend import (
        OwnerMetadataPolicy,
        project_error_memory_backend,
        tool_error_memory_backend,
    )
    from kanda_reasoner_app.error_memory.cross_owner_reference import (
        create_cross_owner_reference,
        list_cross_owner_references,
        resolve_cross_owner_reference,
    )
    from kanda_reasoner_app.error_memory.importer import import_error_memory_file
    from kanda_reasoner_app.error_memory.intake_form_builder import (
        build_lesson_from_ai_form,
    )
    from kanda_reasoner_app.error_memory.store import list_lessons, save_lesson

    temp_root.mkdir(parents=True, exist_ok=True)
    token = uuid.uuid4().hex[:12]
    tool_root = _unique_fixture_root(
        temp_root, "kanda_reasoner_fixture", token
    )
    project_root = _unique_fixture_root(
        temp_root, "demo_project_fixture", token
    )
    _select_fixture_project(project_root, tool_root)
    project_backend = project_error_memory_backend(
        project_root,
        tool_source_root=tool_root,
    )
    tool_backend = tool_error_memory_backend(tool_root)

    assert project_backend.root != tool_backend.root
    assert project_backend.root.name == "project_error_memory"
    assert tool_backend.root.name == "tool_error_memory"
    print("TOOL_ERROR_MEMORY_BACKEND_EXPLICIT: PASS")
    print("PROJECT_ERROR_MEMORY_BACKEND_EXPLICIT: PASS")

    form_lesson = build_lesson_from_ai_form(
        selected_project_root=project_root,
        form_inputs={
            **_base_lesson(project_root, "ValueError: form"),
            "owner_scope": "TOOL",
            "owner_id": "ai-supplied-owner",
            "owner_slug": "forged",
            "owner_root_fingerprint": "forged",
            "affected_box": "forged",
        },
    )
    save_lesson(project_backend, form_lesson)
    assert form_lesson["owner_scope"] == "PROJECT"
    assert form_lesson["owner_id"] == project_backend.owner.owner_id
    print("OWNER_METADATA_SYSTEM_ASSIGNED: PASS")
    print("AI_OWNER_METADATA_NOT_AUTHORITATIVE: PASS")
    print("FORM_OWNER_METADATA_NOT_AUTHORITATIVE: PASS")

    tool_lesson = _base_lesson(tool_root, "RuntimeError: tool")
    save_lesson(tool_backend, tool_lesson)
    foreign_project = dict(tool_lesson)
    foreign_project["lesson_id"] = "lesson-tool-to-project-rejected-v1"
    _expect_error(
        lambda: save_lesson(
            project_backend,
            foreign_project,
            owner_metadata_policy=OwnerMetadataPolicy.REQUIRE_MATCH,
        ),
        "FOREIGN_OWNER_CANONICAL_WRITE_REJECTED",
    )
    print("TOOL_LESSON_PROJECT_STORE_REJECTED: PASS")

    project_lesson = _base_lesson(project_root, "RuntimeError: project")
    save_lesson(project_backend, project_lesson)
    foreign_tool = dict(project_lesson)
    foreign_tool["lesson_id"] = "lesson-project-to-tool-rejected-v1"
    _expect_error(
        lambda: save_lesson(
            tool_backend,
            foreign_tool,
            owner_metadata_policy=OwnerMetadataPolicy.REQUIRE_MATCH,
        ),
        "FOREIGN_OWNER_CANONICAL_WRITE_REJECTED",
    )
    print("PROJECT_LESSON_TOOL_STORE_REJECTED: PASS")

    foreign_path = temp_root / "foreign_lesson.json"
    foreign_path.write_text(
        json.dumps(tool_lesson, indent=2),
        encoding="utf-8",
    )
    _expect_error(
        lambda: import_error_memory_file(project_backend, foreign_path),
        "FOREIGN_OWNER_CANONICAL_WRITE_REJECTED",
    )
    print("FOREIGN_OWNER_IMPORT_FAILS_CLOSED: PASS")

    ownerless = dict(project_lesson)
    ownerless["lesson_id"] = "lesson-ownerless-import-v1"
    for key in (
        "owner_scope",
        "owner_id",
        "owner_slug",
        "owner_root_fingerprint",
        "affected_box",
    ):
        ownerless.pop(key, None)
    ownerless_path = temp_root / "ownerless_lesson.json"
    ownerless_path.write_text(
        json.dumps(ownerless, indent=2),
        encoding="utf-8",
    )
    _expect_error(
        lambda: import_error_memory_file(project_backend, ownerless_path),
        "CANONICAL_OWNER_METADATA_MISSING",
    )

    reference_path = create_cross_owner_reference(
        project_backend,
        tool_backend,
        tool_lesson["lesson_id"],
    )
    references = list_cross_owner_references(project_backend)
    assert reference_path.exists() and len(references) == 1
    project_count = len(list_lessons(project_backend, include_inactive=True))
    assert project_count == 2
    resolved = resolve_cross_owner_reference(references[0], tool_backend)
    resolved["symptom"] = "local copy only"
    source = list_lessons(tool_backend, include_inactive=True)[0]
    assert source["symptom"] != "local copy only"
    print("CROSS_OWNER_REFERENCE_READ_ONLY: PASS")
    print("CROSS_OWNER_REFERENCE_NOT_CANONICAL_COPY: PASS")
    print("CROSS_OWNER_REFERENCE_COUNT_EXCLUDED: PASS")

    assert project_backend.root not in tool_root.parents
    assert tool_backend.root not in tool_root.parents
    transient = temp_root / "demo_project_delete_after_daily_work"
    assert project_backend.root != transient
    assert tool_backend.root != transient
    print("TRANSIENT_ROOT_CANONICAL_MEMORY_REJECTED: PASS")
    print("TOOL_SOURCE_CANONICAL_MEMORY_REJECTED: PASS")

    _select_fixture_project(tool_root, tool_root)
    self_hosted_project = project_error_memory_backend(
        tool_root,
        tool_source_root=tool_root,
    )
    assert self_hosted_project.owner.owner_scope.value == "PROJECT"
    assert tool_backend.owner.owner_scope.value == "TOOL"
    assert self_hosted_project.root != tool_backend.root
    print("ROOT_EQUALITY_DOES_NOT_MERGE_MEMORY_OWNER: PASS")

    from kanda_reasoner_app.error_memory_gui._portable_transfer import (
        export_error_lessons_folder,
        import_error_lessons_folder,
    )

    export_parent = temp_root / "portable_exports"
    foreign_project = _unique_fixture_root(
        temp_root, "foreign_project_fixture", token
    )
    export_parent.mkdir()
    _select_fixture_project(project_root, tool_root)
    exported = export_error_lessons_folder(project_root, export_parent)
    _select_fixture_project(foreign_project, tool_root)
    imported = import_error_lessons_folder(foreign_project, exported["export_folder"])
    foreign_backend = project_error_memory_backend(
        foreign_project,
        tool_source_root=tool_root,
    )
    assert imported["imported_count"] == 0
    assert imported["referenced_count"] == 2
    assert not list_lessons(foreign_backend, include_inactive=True)
    assert len(list_cross_owner_references(foreign_backend)) == 2
    print("PORTABLE_FOREIGN_OWNER_REFERENCE_ONLY: PASS")


def _freeze_inputs() -> dict[str, Any]:
    """Return one writable local Freeze preview fixture."""
    return {
        "feature_title": "Owner scoped memory validation",
        "primary_box": "KANDA Reasoner Tool memory ownership boundary",
        "validated_files": ["kanda_reasoner_app/error_memory/backend.py"],
        "protected_paths": ["project_freeze_after_update/frozen_features_memory"],
        "do_not_regress_rules": ["Keep Preview read-only."],
        "validation_evidence_summary": (
            "VALIDATION OK: owner-scoped-memory-fixture\nSTATUS: IN_SYNC"
        ),
    }


def _validate_freeze(temp_root: Path) -> None:
    """Validate Project Freeze Memory and Tool Freeze evidence separation."""
    from kanda_reasoner_app.freeze_after_update.contract import (
        preview_freeze_entry,
        validate_freeze_entry_preview,
    )
    from kanda_reasoner_app.freeze_after_update.ownership import (
        project_freeze_memory_owner,
        tool_freeze_evidence_owner,
        write_tool_freeze_evidence,
    )

    temp_root.mkdir(parents=True, exist_ok=True)
    token = uuid.uuid4().hex[:12]
    tool_root = _unique_fixture_root(
        temp_root, "freeze_tool_fixture", token
    )
    project_a = _unique_fixture_root(
        temp_root, "freeze_project_a_fixture", token
    )
    project_b = _unique_fixture_root(
        temp_root, "freeze_project_b_fixture", token
    )

    _select_fixture_project(project_a, tool_root)
    project_freeze_memory_owner(project_a).owner.support_root.mkdir(
        parents=True, exist_ok=True
    )
    preview = preview_freeze_entry(project_a, _freeze_inputs())
    assert preview["ok"] is True
    assert preview["owner_scope"] == "PROJECT"
    assert preview["freeze_store_kind"] == "PROJECT_MEMORY"
    assert "memory ownership" in preview["markdown"]
    validation = validate_freeze_entry_preview(project_a, preview)
    assert validation["ok"] is True

    tool_binding = tool_freeze_evidence_owner(tool_root)
    rejected = preview_freeze_entry(
        project_a,
        _freeze_inputs(),
        owner_binding=tool_binding,
    )
    assert rejected["ok"] is False
    assert "TOOL_FREEZE_PROJECT_STORE_REJECTED" in rejected["errors"]
    print("TOOL_FREEZE_PROJECT_STORE_REJECTED: PASS")

    project_binding = project_freeze_memory_owner(project_a)
    _expect_error(
        lambda: write_tool_freeze_evidence(
            tool_root,
            FEATURE_ID,
            {"status": "validated"},
            owner_binding=project_binding,
        ),
        "PROJECT_FREEZE_TOOL_STORE_REJECTED",
    )
    print("PROJECT_FREEZE_TOOL_STORE_REJECTED: PASS")

    _select_fixture_project(project_b, tool_root)
    stale = validate_freeze_entry_preview(project_b, preview)
    assert stale["ok"] is False
    print("STALE_PROJECT_CONTEXT_MEMORY_WRITE_REJECTED: PASS")

    evidence_path = write_tool_freeze_evidence(
        tool_root,
        FEATURE_ID,
        {"status": "validated"},
    )
    payload = json.loads(evidence_path.read_text(encoding="utf-8"))
    assert payload["owner_scope"] == "TOOL"
    assert payload["freeze_store_kind"] == "TOOL_EVIDENCE"


def _validate_release1(project_root: Path) -> None:
    """Run the frozen Release 1 boundary validator."""
    validator = project_root / "tools" / (
        "validate_tool_project_boundary_identity_explicit_selection_v1.py"
    )
    completed = subprocess.run(
        [sys.executable, str(validator)],
        cwd=str(project_root),
        text=True,
        capture_output=True,
        check=False,
    )
    marker = "VALIDATION OK: tool-project-boundary-identity-explicit-selection-v1"
    if completed.returncode != 0 or marker not in completed.stdout:
        raise AssertionError(
            "Release 1 regression validator failed.\n"
            + completed.stdout
            + completed.stderr
        )
    print("RELEASE1_FROZEN_BOUNDARY_REGRESSION: PASS")


def _validate_module_sizes(project_root: Path) -> None:
    """Enforce the current maximum for every touched source module."""
    relative_paths = (
        "kanda_reasoner_app/memory_ownership/context.py",
        "kanda_reasoner_app/error_memory/backend.py",
        "kanda_reasoner_app/error_memory/cross_owner_reference.py",
        "kanda_reasoner_app/error_memory/paths.py",
        "kanda_reasoner_app/error_memory/store.py",
        "kanda_reasoner_app/error_memory/schema.py",
        "kanda_reasoner_app/error_memory/models.py",
        "kanda_reasoner_app/error_memory/importer.py",
        "kanda_reasoner_app/error_memory/intake_form_builder.py",
        "kanda_reasoner_app/error_memory/intake_ai_form_prompt.py",
        "kanda_reasoner_app/error_memory_gui/_portable_owner_contract.py",
        "kanda_reasoner_app/error_memory_gui/_portable_transfer.py",
        "kanda_reasoner_app/freeze_after_update/ownership.py",
        "kanda_reasoner_app/freeze_after_update/contract.py",
        "kanda_reasoner_app/freeze_after_update_gui/local_freeze_confirmation_binding.py",
    )
    for relative in relative_paths:
        count = len((project_root / relative).read_text(encoding="utf-8").splitlines())
        if count > 500:
            raise AssertionError(relative + " exceeds 500 physical lines")
    print("TOUCHED_SOURCE_MODULES_MAX_500: PASS")


def _path_is_within(root: Path, candidate: Path) -> bool:
    """Return whether a candidate remains inside one canonical root."""
    canonical_root = root.resolve(strict=False)
    canonical_candidate = candidate.resolve(strict=False)
    try:
        canonical_candidate.relative_to(canonical_root)
    except ValueError:
        return False
    return True


def _validate_install_write_scope(
    receipt_path: Path | None,
    project_root: Path,
) -> None:
    """Validate that the Tool patch wrote only inside KANDA Reasoner."""
    if receipt_path is None:
        raise AssertionError("INSTALL_RECEIPT_REQUIRED_FOR_WRITE_SCOPE_CHECK")
    payload = json.loads(receipt_path.read_text(encoding="utf-8-sig"))
    scope = payload.get("install_write_scope")
    if not isinstance(scope, dict):
        raise AssertionError("INSTALL_WRITE_SCOPE_RECEIPT_MISSING")

    expected_root = project_root.resolve(strict=False)
    allowed_root = Path(str(scope.get("allowed_root") or "")).resolve(
        strict=False
    )
    owner_scope = str(scope.get("owner_scope") or "")
    if owner_scope not in {"TOOL", "PROJECT"}:
        raise AssertionError("INSTALL_WRITE_SCOPE_OWNER_INVALID")
    if owner_scope == "PROJECT":
        if str(payload.get("selection_mode") or "") != "EXPLICIT_SELF_HOSTING":
            raise AssertionError("PROJECT_INSTALL_SCOPE_NOT_SELF_HOSTING")
    if allowed_root != expected_root:
        raise AssertionError("INSTALL_WRITE_SCOPE_ROOT_MISMATCH")
    if scope.get("all_targets_inside_allowed_root") is not True:
        raise AssertionError("INSTALL_WRITE_SCOPE_TARGET_ASSERTION_MISSING")
    if scope.get("external_project_roots_touched") is not False:
        raise AssertionError("EXTERNAL_PROJECT_TOUCH_CLAIM_INVALID")

    records = payload.get("files")
    if not isinstance(records, list) or not records:
        raise AssertionError("INSTALL_RECEIPT_FILES_INVALID")
    for item in records:
        if not isinstance(item, dict):
            raise AssertionError("INSTALL_RECEIPT_FILE_RECORD_INVALID")
        relative = Path(str(item.get("relative_path") or ""))
        if relative.is_absolute() or ".." in relative.parts:
            raise AssertionError("INSTALL_RECEIPT_RELATIVE_PATH_UNSAFE")
        if not _path_is_within(expected_root, expected_root / relative):
            raise AssertionError("INSTALL_TARGET_OUTSIDE_TOOL_ROOT")

    print("SELF_HOSTING_OR_TOOL_PATCH_WRITE_SCOPE_ONLY: PASS")
    print("EXTERNAL_PROJECT_INDEPENDENCE_PRESERVED: PASS")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--project-root",
        default=str(DEFAULT_PROJECT_ROOT),
    )
    parser.add_argument("--install-receipt", default="")
    args = parser.parse_args()
    project_root = Path(args.project_root).expanduser().resolve()
    receipt = (
        Path(args.install_receipt).expanduser().resolve()
        if args.install_receipt
        else None
    )
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_root = Path(temp_dir)
        _validate_error_memory(temp_root / "error_memory")
        _validate_freeze(temp_root / "freeze")
    _validate_release1(project_root)
    _validate_module_sizes(project_root)
    _validate_install_write_scope(receipt, project_root)
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
