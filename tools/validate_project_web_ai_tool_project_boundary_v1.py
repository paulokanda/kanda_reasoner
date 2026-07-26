# project-path: tools/validate_project_web_ai_tool_project_boundary_v1.py
"""Validate complete Tool-versus-Project separation in Project Web AI."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path

FEATURE_ID = "project-web-ai-tool-project-boundary-v1"


def _assert(condition: bool, message: str) -> None:
    """Raise one focused boundary validation failure."""
    if not condition:
        raise AssertionError(message)


def _identity_project(identity) -> dict[str, str]:
    """Return canonical selected-Project metadata for fixture handoffs."""
    return {
        "project_slug": identity.active_project_slug,
        "project_root_marker": "<PROJECT_ROOT>",
        "active_project_id": identity.active_project_id,
        "active_project_root_fingerprint": identity.active_project_root_fingerprint,
    }


def _fixture_payloads(identity) -> dict[str, bytes]:
    """Return one compact identity-bound Project handoff."""
    project = _identity_project(identity)
    payloads: dict[str, object] = {
        "__ai_briefing.json": {
            "bundle_kind": "ai_briefing",
            "generated_at_utc": "2026-07-20T12:00:00Z",
            "project": project,
        },
        "__routing_manifest.json": {
            "bundle_kind": "routing_manifest",
            "project": project,
        },
        "__bundle_manifest.json": {
            "bundle_kind": "bundle_manifest",
            "project": project,
            "artifacts": [],
        },
        "__patch_safety_routes.json": {
            "bundle_kind": "patch_safety_routes",
            "project": project,
        },
        "__validation_state.json": {
            "bundle_kind": "validation_state",
            "project": project,
            "overall": {"status": "not_run"},
        },
        "__error_lessons_compact.json": {
            "artifact_type": "error_memory_ai_export",
            "derived_from": {"project_slug": identity.active_project_slug},
            "lessons": [],
        },
        "__error_memory_manifest.json": {
            "artifact_type": "error_memory_manifest",
            "project_slug": identity.active_project_slug,
            "included_lesson_ids": [],
        },
    }
    members = {
        "__error_memory_ai_prompt.md": b"Error Memory prevention guidance.",
    }
    for suffix, payload in payloads.items():
        members[suffix] = json.dumps(payload).encode("utf-8")
    return members


def _write_handoff(identity, *, archive_slug: str | None = None, mutate=None) -> Path:
    """Write one exact-slug handoff under canonical Project Support."""
    second = identity.active_project_support_root / "second_prompt_files"
    second.mkdir(parents=True, exist_ok=True)
    (second / "_RUN_COLLECTOR_STATUS.txt").write_text(
        "Status: complete\nPublished after ZIP: True\n",
        encoding="utf-8",
    )
    slug = archive_slug or identity.active_project_slug
    archive_path = second / (slug + "__ai_handoff_upload.zip")
    members = _fixture_payloads(identity)
    if mutate is not None:
        mutate(members)
    with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as archive:
        for suffix, data in members.items():
            name = slug + suffix
            archive.writestr(slug + "__ai_handoff_upload/" + name, data)
    return archive_path


def _expect_failure(callable_, error_type, marker: str) -> None:
    """Require one exact fail-closed boundary error."""
    try:
        callable_()
    except error_type:
        print(marker + ": PASS")
    else:
        raise AssertionError(marker + " did not fail closed")


def _validate_runtime_boundaries(root: Path) -> None:
    """Validate canonical support, identity, and cross-project gates."""
    from kanda_reasoner_app.project_support_boundary import (
        canonical_project_support_root,
        resolve_project_tool_boundary_identity,
    )
    from kanda_reasoner_app.reasoner_engine.project_web_ai_bridge import (
        load_project_web_ai_context,
    )
    from kanda_reasoner_app.web_ai_provider_contracts import (
        HandoffMissingError,
        SupportIdentityMismatchError,
        SupportIdentityMissingError,
    )

    base = Path(tempfile.mkdtemp(prefix="kanda_tool_project_boundary_"))
    try:
        project = base / "workspace" / "demo"
        project.mkdir(parents=True)
        identity = resolve_project_tool_boundary_identity(project)
        _assert(
            identity.active_project_support_root
            == canonical_project_support_root(project),
            "Project Web AI does not use canonical Project Support owner",
        )
        _write_handoff(identity)
        snapshot = load_project_web_ai_context(project)
        _assert(snapshot.project_id == identity.active_project_id, "Project ID lost")
        _assert(
            snapshot.project_root_fingerprint
            == identity.active_project_root_fingerprint,
            "Project root fingerprint lost",
        )
        _assert(snapshot.support_identity_status == "VERIFIED", "support unverified")
        _assert(snapshot.tool_project_slug == "kanda_reasoner", "Tool identity lost")
        print("PROJECT_WEB_AI_CANONICAL_SUPPORT_OWNER: PASS")
        print("PROJECT_SUPPORT_IDENTITY_VERIFIED: PASS")

        shutil.rmtree(identity.active_project_support_root)
        _write_handoff(identity, archive_slug="another_project")
        _expect_failure(
            lambda: load_project_web_ai_context(project),
            HandoffMissingError,
            "CROSS_PROJECT_HANDOFF_FALLBACK_BLOCKED",
        )

        shutil.rmtree(identity.active_project_support_root)

        def remove_identity(members: dict[str, bytes]) -> None:
            for suffix in ("__ai_briefing.json", "__bundle_manifest.json"):
                payload = json.loads(members[suffix].decode("utf-8"))
                payload["project"].pop("active_project_id", None)
                payload["project"].pop("active_project_root_fingerprint", None)
                members[suffix] = json.dumps(payload).encode("utf-8")

        _write_handoff(identity, mutate=remove_identity)
        _expect_failure(
            lambda: load_project_web_ai_context(project),
            SupportIdentityMissingError,
            "PROJECT_SUPPORT_MISSING_IDENTITY_BLOCKED",
        )

        shutil.rmtree(identity.active_project_support_root)

        def mismatch_identity(members: dict[str, bytes]) -> None:
            payload = json.loads(members["__ai_briefing.json"].decode("utf-8"))
            payload["project"]["active_project_id"] = "wrong-project-id"
            members["__ai_briefing.json"] = json.dumps(payload).encode("utf-8")

        _write_handoff(identity, mutate=mismatch_identity)
        _expect_failure(
            lambda: load_project_web_ai_context(project),
            SupportIdentityMismatchError,
            "PROJECT_SUPPORT_IDENTITY_MISMATCH_BLOCKED",
        )

        self_hosted = resolve_project_tool_boundary_identity(
            project,
            tool_source_root=project,
        )
        _assert(self_hosted.self_hosting_mode, "self-hosting mode not detected")
        _assert(
            self_hosted.tool_project_slug == "kanda_reasoner"
            and self_hosted.active_project_slug == "demo",
            "logical Tool and Project identities collapsed",
        )
        print("SELF_HOSTING_LOGICAL_SEPARATION: PASS")
    finally:
        shutil.rmtree(base, ignore_errors=True)


def _validate_source_contracts(root: Path) -> None:
    """Validate request cards, export barriers, and no duplicate owners."""
    bridge = (root / "kanda_reasoner_app/reasoner_engine/project_web_ai_bridge.py").read_text(
        encoding="utf-8"
    )
    reader = (
        root
        / "kanda_reasoner_app/reasoner_engine/project_web_ai_handoff_reader.py"
    ).read_text(encoding="utf-8")
    tab = (root / "kanda_reasoner_app/reasoner_engine/project_web_ai_tab.py").read_text(
        encoding="utf-8"
    )
    workers = (
        root / "kanda_reasoner_app/reasoner_engine/project_web_ai_workers.py"
    ).read_text(encoding="utf-8")
    conversations = (
        root / "kanda_reasoner_app/reasoner_engine/project_web_ai_conversations.py"
    ).read_text(encoding="utf-8")
    _assert(
        "resolve_project_tool_boundary_identity" in bridge,
        "canonical Tool/Project identity owner not reused",
    )
    _assert(
        'root.parent / (root.name + "_show_project_to_AI")' not in bridge,
        "duplicate Project Support constructor remains",
    )
    _assert(
        'glob("*__ai_handoff_upload*.zip")' not in reader,
        "cross-project wildcard handoff fallback remains",
    )
    print("NO_DUPLICATE_PROJECT_SUPPORT_RESOLVER: PASS")

    required_card_fields = (
        "session_id",
        "project_id",
        "project_root_fingerprint",
        "support_root",
        "snapshot_id",
        "context_hash",
        "gateway_id",
        "model_id",
        "privacy_approval_id",
        "project_epoch",
    )
    for field in required_card_fields:
        _assert(field + "=" in tab, "request card field missing: " + field)
    _assert("Signal(object, str)" in workers, "token event lacks request card")
    _assert("identity == self._active_request_identity" in tab, "card equality missing")
    _assert("identity.session_id == self._active_chat().session_id" in tab, "chat guard missing")
    _assert(
        "self._project_session.request_is_current(identity, context)" in tab,
        "Project epoch and session guard missing",
    )
    print("FULL_REQUEST_IDENTITY_BOUNDARY: PASS")
    print("PROJECT_SESSION_EPOCH_BOUNDARY: PASS")

    for field in (
        "tool_source_root",
        "project_root",
        "support_root",
        "daily_work_root",
    ):
        _assert("self._context." + field in tab, "protected root missing: " + field)
    _assert("self._protected_export_roots()" in conversations, "export guard owner missing")
    print("TOOL_AND_PROJECT_EXPORT_ROOTS_PROTECTED: PASS")

    source_files = (
        "kanda_reasoner_app/project_support_boundary.py",
        "kanda_reasoner_app/reasoner_engine/project_web_ai_bridge.py",
        "kanda_reasoner_app/reasoner_engine/project_web_ai_handoff_reader.py",
        "kanda_reasoner_app/reasoner_engine/project_web_ai_tab.py",
        "kanda_reasoner_app/reasoner_engine/project_web_ai_workers.py",
        "kanda_reasoner_app/reasoner_engine/project_web_ai_session.py",
        "kanda_reasoner_app/reasoner_engine/project_web_ai_conversations.py",
        "kanda_reasoner_app/web_ai_provider_contracts.py",
    )
    for relative in source_files:
        lines = len((root / relative).read_text(encoding="utf-8").splitlines())
        _assert(lines <= 500, relative + " exceeds 500 physical lines")
    print("TOUCHED_SOURCE_MODULES_MAX_500_LINES: PASS")


def main() -> int:
    """Run complete Tool-versus-Project boundary validation."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=str(Path.cwd()))
    args = parser.parse_args()
    root = Path(args.root).expanduser().resolve(strict=True)
    sys.path.insert(0, str(root))
    _validate_runtime_boundaries(root)
    _validate_source_contracts(root)
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
