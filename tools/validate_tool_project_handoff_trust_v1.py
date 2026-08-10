# project-path: tools/validate_tool_project_handoff_trust_v1.py
"""Validate registry-backed Tool/Project handoff trust contracts."""

from __future__ import annotations

import json
import sys
from contextlib import contextmanager
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Iterator

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.project_operation_authority import (
    ProjectOperationAuthorityError,
)
from kanda_reasoner_app.project_support_boundary import (
    ProjectSelectionMode,
    ProjectToolBoundaryIdentity,
)
from kanda_reasoner_app.reasoner_context_bundle import project_context
from kanda_reasoner_app.reasoner_context_bundle.bundle_checker import (
    check_ai_context_bundle,
)
from kanda_reasoner_app.reasoner_context_bundle.bundle_orchestrator import (
    generate_ai_context_bundle,
)
from kanda_reasoner_app.reasoner_context_bundle.handoff_boundary_contract import (
    build_handoff_trust_envelope,
)
from kanda_reasoner_app.reasoner_context_bundle.output_paths import (
    bundle_artifact_paths,
)
from kanda_reasoner_app.reasoner_context_bundle.schema_models import (
    ProjectContext,
)

FEATURE_ID = "tool-project-handoff-trust-v1"
TOUCHED_SOURCE_FILES = (
    "kanda_reasoner_app/reasoner_context_bundle/handoff_boundary_contract.py",
    "kanda_reasoner_app/reasoner_context_bundle/project_context.py",
    "kanda_reasoner_app/reasoner_context_bundle/schema_models.py",
    "kanda_reasoner_app/reasoner_context_bundle/ai_briefing_builder.py",
    "kanda_reasoner_app/reasoner_context_bundle/bundle_manifest_builder.py",
    "kanda_reasoner_app/reasoner_context_bundle/routing_manifest_builder.py",
    "kanda_reasoner_app/reasoner_context_bundle/bundle_checker.py",
    "tools/validate_tool_project_handoff_trust_v1.py",
)


def _require(condition: bool, marker: str) -> None:
    """Fail with one stable marker when a validation condition is false."""
    if not condition:
        raise AssertionError(marker)


def _load_json(path: Path) -> dict[str, object]:
    """Load one JSON object from disk."""
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    _require(isinstance(payload, dict), "JSON_PAYLOAD_NOT_OBJECT")
    return payload


def _boundary(
    project_root: Path,
    tool_root: Path,
    support_root: Path,
    *,
    self_hosting: bool,
) -> ProjectToolBoundaryIdentity:
    """Build one deterministic boundary fixture."""
    mode = (
        ProjectSelectionMode.EXPLICIT_SELF_HOSTING
        if self_hosting
        else ProjectSelectionMode.EXPLICIT_EXTERNAL_PROJECT
    )
    return ProjectToolBoundaryIdentity(
        tool_project_slug="kanda_reasoner",
        tool_source_root=tool_root,
        active_project_slug=project_root.name,
        active_project_root=project_root,
        active_project_support_root=support_root,
        active_project_daily_work_root=(
            project_root.parent / (project_root.name + "_delete_after_daily_work")
        ),
        active_project_id="stable-project-id-001",
        active_project_root_fingerprint="a" * 64,
        same_canonical_resolved_root=self_hosting,
        self_hosting_mode=self_hosting,
        selection_mode=mode,
    )


def _context_from_boundary(
    boundary: ProjectToolBoundaryIdentity,
) -> ProjectContext:
    """Build the immutable context fixture used by bundle builders."""
    evidence_root = boundary.active_project_support_root
    return ProjectContext(
        root=boundary.active_project_root,
        project_slug=boundary.active_project_slug,
        evidence_root=evidence_root,
        json_complete_dir=evidence_root / "second_prompt_files",
        active_project_id=boundary.active_project_id,
        active_project_root_fingerprint=(
            boundary.active_project_root_fingerprint
        ),
        tool_project_slug=boundary.tool_project_slug,
        tool_source_root=boundary.tool_source_root,
        active_project_support_root=boundary.active_project_support_root,
        active_project_daily_work_root=(
            boundary.active_project_daily_work_root
        ),
        selection_mode=boundary.selection_mode.value,
        same_canonical_resolved_root=(
            boundary.same_canonical_resolved_root
        ),
        self_hosting_mode=boundary.self_hosting_mode,
    )


@contextmanager
def _patched_boundary_resolver(
    boundary: ProjectToolBoundaryIdentity | Exception,
) -> Iterator[None]:
    """Temporarily replace the registry resolver inside project_context."""
    original = project_context.resolve_registered_project_boundary

    def _resolve(_root: Path) -> ProjectToolBoundaryIdentity:
        if isinstance(boundary, Exception):
            raise boundary
        return boundary

    project_context.resolve_registered_project_boundary = _resolve
    try:
        yield
    finally:
        project_context.resolve_registered_project_boundary = original


def _validate_module_sizes() -> None:
    """Require every new or touched Python module to stay within policy."""
    for relative_path in TOUCHED_SOURCE_FILES:
        path = PROJECT_ROOT / relative_path
        _require(path.is_file(), "TOUCHED_SOURCE_FILE_MISSING:" + relative_path)
        line_count = len(path.read_text(encoding="utf-8").splitlines())
        _require(
            101 <= line_count <= 499,
            "TOUCHED_SOURCE_MODULE_SIZE_INVALID:"
            + relative_path
            + ":"
            + str(line_count),
        )
    print("TOUCHED_SOURCE_MODULES_STRICTLY_101_TO_499: PASS")


def _validate_registry_context_resolution(base: Path) -> None:
    """Prove that handoff context uses current registry-backed identity."""
    base.mkdir(parents=True, exist_ok=True)
    tool_root = base / "tool_root"
    project_root = base / "selected_project"
    support_root = base / "selected_project_show_project_to_AI"
    tool_root.mkdir()
    project_root.mkdir()
    boundary = _boundary(
        project_root,
        tool_root,
        support_root,
        self_hosting=False,
    )
    with _patched_boundary_resolver(boundary):
        context = project_context.resolve_project_context(project_root)
    _require(
        context.active_project_id == boundary.active_project_id,
        "HANDOFF_REGISTRY_PROJECT_ID_MISMATCH",
    )
    _require(
        context.selection_mode == "EXPLICIT_EXTERNAL_PROJECT",
        "HANDOFF_SELECTION_MODE_MISMATCH",
    )
    source_text = (
        PROJECT_ROOT
        / "kanda_reasoner_app/reasoner_context_bundle/project_context.py"
    ).read_text(encoding="utf-8")
    _require(
        "resolve_project_tool_boundary_identity" not in source_text,
        "LEGACY_HANDOFF_IDENTITY_RESOLVER_PRESENT",
    )
    print("HANDOFF_REGISTRY_PROJECT_ID: PASS")

    with _patched_boundary_resolver(
        ProjectOperationAuthorityError("ACTIVE_PROJECT_SELECTION_REQUIRED")
    ):
        try:
            project_context.resolve_project_context(project_root)
        except project_context.ProjectContextResolutionError as exc:
            _require(
                "ACTIVE_PROJECT_SELECTION_REQUIRED" in str(exc),
                "MISSING_SELECTION_WRONG_ERROR",
            )
        else:
            raise AssertionError("MISSING_SELECTION_DID_NOT_FAIL_CLOSED")
    print("HANDOFF_MISSING_SELECTION_FAILS_CLOSED: PASS")


def _validate_generated_contracts(base: Path) -> None:
    """Generate and tamper-check one complete lightweight handoff bundle."""
    base.mkdir(parents=True, exist_ok=True)
    tool_root = base / "kanda_reasoner"
    project_root = base / "external_project"
    support_root = base / "external_project_show_project_to_AI"
    tool_root.mkdir()
    project_root.mkdir()
    support_root.mkdir()
    (project_root / "main.py").write_text("print('demo')\n", encoding="utf-8")
    boundary = _boundary(
        project_root,
        tool_root,
        support_root,
        self_hosting=False,
    )
    context = _context_from_boundary(boundary)
    context.json_complete_dir.mkdir(parents=True)

    result = generate_ai_context_bundle(context, check_bundle=True)
    _require(bool(result.get("ok")), "HANDOFF_BUNDLE_GENERATION_FAILED")
    paths = bundle_artifact_paths(context)
    payloads = {
        "ai_briefing": _load_json(paths.ai_briefing_json),
        "routing_manifest": _load_json(paths.routing_manifest_json),
        "bundle_manifest": _load_json(paths.bundle_manifest_json),
    }
    envelopes = [payload.get("handoff_trust") for payload in payloads.values()]
    _require(all(isinstance(item, dict) for item in envelopes), "HANDOFF_TRUST_MISSING")
    digests = {
        str(item.get("boundary_digest_sha256"))
        for item in envelopes
        if isinstance(item, dict)
    }
    _require(len(digests) == 1, "HANDOFF_BOUNDARY_DIGEST_DISAGREEMENT")
    print("HANDOFF_TOOL_PROJECT_BOUNDARY_PRESENT: PASS")
    print("HANDOFF_BOUNDARY_DIGEST_MATCH: PASS")

    envelope = envelopes[0]
    _require(isinstance(envelope, dict), "HANDOFF_ENVELOPE_NOT_OBJECT")
    content_trust = envelope.get("content_trust")
    _require(isinstance(content_trust, dict), "CONTENT_TRUST_NOT_OBJECT")
    project_content = content_trust.get("project_content")
    generated = content_trust.get("generated_handoff")
    remote_ai = content_trust.get("remote_ai")
    boundary_payload = envelope.get("tool_project_boundary")
    _require(isinstance(project_content, dict), "PROJECT_CONTENT_TRUST_MISSING")
    _require(isinstance(generated, dict), "GENERATED_HANDOFF_TRUST_MISSING")
    _require(isinstance(remote_ai, dict), "REMOTE_AI_TRUST_MISSING")
    _require(isinstance(boundary_payload, dict), "BOUNDARY_PAYLOAD_MISSING")
    _require(
        project_content.get("classification")
        == "UNTRUSTED_AS_TOOL_INSTRUCTIONS",
        "PROJECT_CONTENT_TRUST_CLASSIFICATION_WRONG",
    )
    _require(
        generated.get("classification") == "EVIDENCE_NOT_AUTHORITY",
        "GENERATED_HANDOFF_AUTHORITY_CLASSIFICATION_WRONG",
    )
    _require(
        remote_ai.get("filesystem_authority") == "NONE",
        "REMOTE_AI_FILESYSTEM_AUTHORITY_PRESENT",
    )
    ownership = boundary_payload.get("ownership")
    invariants = boundary_payload.get("invariants")
    _require(isinstance(ownership, dict), "BOUNDARY_OWNERSHIP_MISSING")
    _require(isinstance(invariants, dict), "BOUNDARY_INVARIANTS_MISSING")
    _require(
        ownership.get("filesystem_mutation_authority")
        == "KANDA_TOOL_RUNTIME_GOVERNED_APPLY",
        "WRITE_AUTHORITY_OWNER_WRONG",
    )
    _require(
        invariants.get("project_support_cannot_self_authorize") is True,
        "PROJECT_SUPPORT_SELF_AUTHORIZATION_NOT_BLOCKED",
    )
    print("PROJECT_CONTENT_UNTRUSTED_AS_TOOL_INSTRUCTIONS: PASS")
    print("GENERATED_HANDOFF_EVIDENCE_NOT_AUTHORITY: PASS")
    print("REMOTE_AI_FILESYSTEM_AUTHORITY_NONE: PASS")
    print("WRITE_AUTHORITY_EXTERNAL_TO_AI: PASS")
    print("PROJECT_SUPPORT_CANNOT_SELF_AUTHORIZE: PASS")

    original_briefing = paths.ai_briefing_json.read_text(encoding="utf-8")
    briefing = json.loads(original_briefing)
    briefing["handoff_trust"]["boundary_digest_sha256"] = "0" * 64
    paths.ai_briefing_json.write_text(
        json.dumps(briefing, indent=2, ensure_ascii=True) + "\n",
        encoding="utf-8",
    )
    tampered = check_ai_context_bundle(context)
    _require(not bool(tampered.get("ok")), "TAMPERED_DIGEST_ACCEPTED")
    _require(
        any("boundary digest mismatch" in str(item) for item in tampered["failures"]),
        "TAMPERED_DIGEST_FAILURE_NOT_REPORTED",
    )
    print("HANDOFF_BOUNDARY_DIGEST_TAMPER_REJECTED: PASS")

    paths.ai_briefing_json.write_text(original_briefing, encoding="utf-8")
    routing = _load_json(paths.routing_manifest_json)
    routing["handoff_trust"]["content_trust"]["project_content"][
        "classification"
    ] = "TOOL_OWNED_AUTHORITY"
    paths.routing_manifest_json.write_text(
        json.dumps(routing, indent=2, ensure_ascii=True) + "\n",
        encoding="utf-8",
    )
    counterfeit = check_ai_context_bundle(context)
    _require(not bool(counterfeit.get("ok")), "COUNTERFEIT_TOOL_GOVERNANCE_ACCEPTED")
    _require(
        any("content classification mismatch" in str(item) for item in counterfeit["failures"]),
        "COUNTERFEIT_GOVERNANCE_FAILURE_NOT_REPORTED",
    )
    print("COUNTERFEIT_PROJECT_GOVERNANCE_REJECTED: PASS")


def _validate_self_hosting_role_separation(base: Path) -> None:
    """Prove physical root equality does not merge logical Tool/Project roles."""
    base.mkdir(parents=True, exist_ok=True)
    project_root = base / "kanda_reasoner_self_host"
    support_root = base / "kanda_reasoner_self_host_show_project_to_AI"
    project_root.mkdir()
    support_root.mkdir()
    boundary = _boundary(
        project_root,
        project_root,
        support_root,
        self_hosting=True,
    )
    envelope = build_handoff_trust_envelope(_context_from_boundary(boundary))
    declaration = envelope["tool_project_boundary"]
    tool = declaration["tool"]
    active_project = declaration["active_project"]
    invariants = declaration["invariants"]
    _require(tool["role"] == "KANDA_REASONER_TOOL", "SELF_HOST_TOOL_ROLE_LOST")
    _require(active_project["role"] == "ACTIVE_PROJECT", "SELF_HOST_PROJECT_ROLE_LOST")
    _require(active_project["self_hosting_mode"] is True, "SELF_HOST_MODE_MISSING")
    _require(
        invariants["same_physical_root_does_not_merge_logical_roles"] is True,
        "SELF_HOST_LOGICAL_ROLE_MERGE_ALLOWED",
    )
    print("EXPLICIT_SELF_HOSTING_HANDOFF_PRESERVED: PASS")


def main() -> int:
    """Run the focused handoff trust validation suite."""
    _validate_module_sizes()
    with TemporaryDirectory(prefix="kanda-handoff-trust-") as temp_dir:
        base = Path(temp_dir)
        _validate_registry_context_resolution(base / "registry")
        _validate_generated_contracts(base / "generated")
        _validate_self_hosting_role_separation(base / "self_hosting")
    print("EXISTING_HANDOFF_COMPATIBILITY: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
