# project-path: tools/validate_project_web_ai_governed_apply_v1.py
"""Validate Project Web AI Phase 3 governed source apply boundaries."""

from __future__ import annotations

import argparse
from dataclasses import replace
import os
import sys
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path
def require(condition: bool, message: str) -> None:
    """Raise one deterministic assertion when a gate fails."""
    if not condition:
        raise AssertionError(message)
def _context(root: Path, *, generated_at: str) -> object:
    """Build one current registry-backed synthetic Project context."""
    from kanda_reasoner_app.project_selection_registry import (
        ProjectSelectionRegistry,
    )
    from kanda_reasoner_app.web_ai_provider_contracts import ContextSnapshot
    registry_path = root.parent / "tool_support" / "projects.json"
    from kanda_reasoner_app import project_operation_authority as authority_module
    registry_type = ProjectSelectionRegistry
    authority_module.ProjectSelectionRegistry = lambda **kwargs: registry_type(
        registry_path=registry_path
    )
    registry = registry_type(registry_path=registry_path)
    boundary = registry.register_explicit_root(root)
    boundary.active_project_support_root.mkdir(parents=True, exist_ok=True)
    boundary.active_project_daily_work_root.mkdir(parents=True, exist_ok=True)
    return ContextSnapshot(
        tool_project_slug=boundary.tool_project_slug,
        tool_source_root=str(boundary.tool_source_root),
        project_slug=boundary.active_project_slug,
        project_id=boundary.active_project_id,
        project_root=str(boundary.active_project_root),
        project_root_fingerprint=boundary.active_project_root_fingerprint,
        support_root=str(boundary.active_project_support_root),
        daily_work_root=str(boundary.active_project_daily_work_root),
        self_hosting_mode=boundary.self_hosting_mode,
        support_identity_status="VERIFIED",
        collector_status="CURRENT",
        snapshot_id="snapshot-1",
        context_hash="context-1",
        generated_at_utc=generated_at,
        trusted_boundary_text="trusted",
        context_text="bounded",
        context_bytes=7,
        artifacts_loaded=("fixture",),
    )


def _operation_preview(root: Path, *, new_value: int) -> tuple[object, object, object]:
    """Build one exact current operation and validated Shadow Preview."""
    from kanda_reasoner_app.reasoner_engine.project_web_ai_change_contracts import (
        ProjectWebAIChangeProposal,
        ProjectWebAIChangeTarget,
        new_change_operation,
    )
    from kanda_reasoner_app.reasoner_engine.project_web_ai_session import (
        ProjectWebAISessionLifecycle,
    )
    from kanda_reasoner_app.reasoner_engine.project_web_ai_shadow import (
        build_shadow_preview,
    )
    from kanda_reasoner_app.reasoner_engine.project_web_ai_source_reader import (
        read_exact_project_sources,
    )
    from kanda_reasoner_app.web_ai_provider_contracts import (
        ProjectWebAIRequestIdentity,
    )

    now = datetime.now(timezone.utc).isoformat()
    context = _context(root, generated_at=now)
    session = ProjectWebAISessionLifecycle()
    decision = session.request_switch(str(root), worker_running=False)
    require(decision.reload_allowed, "fixture Project switch was not reloadable")
    session_identity = session.bind_snapshot(context)
    source_file = root / "sample.py"
    source = read_exact_project_sources(root, (source_file,))[0]
    request = ProjectWebAIRequestIdentity(
        request_id="request-1",
        session_id="chat-1",
        project_id=context.project_id,
        project_slug=context.project_slug,
        project_root_fingerprint=context.project_root_fingerprint,
        support_root=context.support_root,
        snapshot_id=context.snapshot_id,
        context_hash=context.context_hash,
        gateway_id="fixture",
        model_id="fixture",
        privacy_approval_id="approval-1",
        created_at_utc=now,
        project_epoch=session_identity.project_epoch,
    )
    operation = new_change_operation(
        request_identity=request,
        session_identity=session_identity,
        context=context,
        question="Change the value.",
        advisory_answer="Use a one-line correction.",
        source_files=(source,),
    )
    diff = (
        "--- a/sample.py\n"
        "+++ b/sample.py\n"
        "@@ -1,1 +1,1 @@\n"
        "-value = 1\n"
        "+value = " + str(new_value) + "\n"
    )
    proposal = ProjectWebAIChangeProposal(
        operation_id=operation.operation_id,
        project_id=request.project_id,
        project_root_fingerprint=request.project_root_fingerprint,
        project_epoch=request.project_epoch,
        snapshot_id=request.snapshot_id,
        summary="Change one fixture value.",
        targets=(
            ProjectWebAIChangeTarget(
                relative_path="sample.py",
                expected_sha256=source.sha256,
                unified_diff=diff,
            ),
        ),
        affected_public_contracts=(),
        required_validators=(),
        known_risks=(),
    )
    preview = build_shadow_preview(operation, proposal)
    return context, session, (operation, preview)


def _authorization(context: object, session: object, operation: object, preview: object):
    """Build one exact one-use human authorization."""
    from kanda_reasoner_app.reasoner_engine.project_web_ai_apply_contracts import (
        build_apply_authorization,
        required_confirmation_phrase,
    )
    identity = session.identity
    require(identity is not None, "fixture session identity is missing")
    return build_apply_authorization(
        operation=operation,
        preview=preview,
        session_identity=identity,
        context=context,
        typed_phrase=required_confirmation_phrase(operation, preview),
    )


def validate_success_and_one_use(root: Path) -> None:
    """Prove bounded apply, backup, receipt, and one-use rejection."""
    from kanda_reasoner_app.reasoner_engine.project_web_ai_write_broker import (
        ProjectWebAIApplyError,
        execute_project_web_ai_apply,
    )

    project = root / "success_project"
    project.mkdir()
    source_path = project / "sample.py"
    source_path.write_text("value = 1\n", encoding="utf-8")
    original = source_path.read_bytes()
    context, session, pair = _operation_preview(project, new_value=2)
    operation, preview = pair
    authorization = _authorization(context, session, operation, preview)
    session.begin_write_transaction(authorization.transaction_id)
    receipt = execute_project_web_ai_apply(
        operation=operation,
        preview=preview,
        authorization=authorization,
        session_identity=session.identity,
        context=context,
    )
    session.finish_write_transaction(authorization.transaction_id, receipt.status)
    require(receipt.status == "APPLIED_SOURCE_VERIFIED", "apply did not verify")
    require(source_path.read_text(encoding="utf-8") == "value = 2\n", "source not changed")
    require(Path(receipt.receipt_path).is_file(), "durable receipt missing")
    from kanda_reasoner_app.reasoner_engine.project_web_ai_apply_receipts import (
        ProjectWebAIApplyReceiptError,
        assert_project_web_ai_handoff_fresh,
    )
    old_handoff = (
        datetime.fromisoformat(receipt.completed_at_utc) - timedelta(seconds=1)
    ).isoformat()
    new_handoff = (
        datetime.fromisoformat(receipt.completed_at_utc) + timedelta(seconds=1)
    ).isoformat()
    try:
        assert_project_web_ai_handoff_fresh(context.support_root, old_handoff)
    except ProjectWebAIApplyReceiptError:
        pass
    else:
        raise AssertionError("stale handoff was accepted after successful apply")
    assert_project_web_ai_handoff_fresh(context.support_root, new_handoff)
    backup = Path(receipt.backup_root) / "sample.py"
    require(backup.read_bytes() == original, "rollback backup is not exact")
    try:
        execute_project_web_ai_apply(
            operation=operation,
            preview=preview,
            authorization=authorization,
            session_identity=session.identity,
            context=context,
        )
    except ProjectWebAIApplyError as exc:
        require("ALREADY_CONSUMED" in str(exc), "one-use rejection marker missing")
    else:
        raise AssertionError("authorization was reusable")
    print("ONE_USE_HUMAN_AUTHORIZATION: PASS")
    print("BOUNDED_PROJECT_SOURCE_WRITE: PASS")
    print("EXACT_BACKUP_AND_DURABLE_RECEIPT: PASS")
    print("POST_APPLY_HANDOFF_REFRESH_REQUIRED: PASS")

def validate_rollback(root: Path) -> None:
    """Force post-write validation failure and require exact rollback."""
    import kanda_reasoner_app.reasoner_engine.project_web_ai_write_broker as broker
    project = root / "rollback_project"
    project.mkdir()
    source_path = project / "sample.py"
    source_path.write_text("value = 1\n", encoding="utf-8")
    original = source_path.read_bytes()
    context, session, pair = _operation_preview(project, new_value=3)
    operation, preview = pair
    authorization = _authorization(context, session, operation, preview)
    original_validator = broker._validate_installed_source

    def fail_after_write(*_args, **_kwargs):
        raise RuntimeError("FORCED_POST_WRITE_VALIDATION_FAILURE")

    broker._validate_installed_source = fail_after_write
    try:
        session.begin_write_transaction(authorization.transaction_id)
        try:
            broker.execute_project_web_ai_apply(
                operation=operation,
                preview=preview,
                authorization=authorization,
                session_identity=session.identity,
                context=context,
            )
        except broker.ProjectWebAIApplyError as exc:
            session.finish_write_transaction(authorization.transaction_id, exc.status)
            require(exc.status == "ROLLED_BACK", "failure did not roll back")
            require(exc.receipt is not None, "rollback receipt missing")
        else:
            raise AssertionError("forced validation failure did not fail apply")
    finally:
        broker._validate_installed_source = original_validator
    require(source_path.read_bytes() == original, "rollback did not restore source")
    print("POST_WRITE_FAILURE_ROLLBACK: PASS")
    print("ROLLBACK_ORIGINAL_HASH_RESTORED: PASS")


def validate_session_and_freshness(root: Path) -> None:
    """Prove transaction switching lock and post-apply handoff freshness."""
    from kanda_reasoner_app.reasoner_engine.project_web_ai_apply_receipts import (
        assert_project_web_ai_handoff_fresh,
    )
    from kanda_reasoner_app.reasoner_engine.project_web_ai_session import (
        ProjectWebAISessionStateError,
    )

    project = root / "session_project"
    project.mkdir()
    (project / "sample.py").write_text("value = 1\n", encoding="utf-8")
    context, session, pair = _operation_preview(project, new_value=4)
    operation, preview = pair
    authorization = _authorization(context, session, operation, preview)
    session.begin_write_transaction(authorization.transaction_id)
    try:
        session.request_switch(str(root / "other"), worker_running=False)
    except ProjectWebAISessionStateError:
        pass
    else:
        raise AssertionError("open transaction did not block Project switch")
    session.finish_write_transaction(authorization.transaction_id, "ROLLED_BACK")
    print("OPEN_TRANSACTION_BLOCKS_PROJECT_SWITCH: PASS")

    support = Path(context.support_root)
    old = (datetime.now(timezone.utc) - timedelta(days=1)).isoformat()
    new = (datetime.now(timezone.utc) + timedelta(days=1)).isoformat()
    # No successful receipt exists in this fixture, so both must remain admissible.
    assert_project_web_ai_handoff_fresh(support, old)
    assert_project_web_ai_handoff_fresh(support, new)
    print("ROLLED_BACK_TRANSACTION_DOES_NOT_STALE_HANDOFF: PASS")

def validate_stale_source_and_unresolved_switch(root: Path) -> None:
    """Reject stale source and retain fail-closed unresolved switch state."""
    from kanda_reasoner_app.reasoner_engine.project_web_ai_session import (
        ProjectWebAISessionStateError,
    )
    from kanda_reasoner_app.reasoner_engine.project_web_ai_write_broker import (
        ProjectWebAIApplyError,
        execute_project_web_ai_apply,
    )

    project = root / "stale_project"
    project.mkdir()
    source_path = project / "sample.py"
    source_path.write_text("value = 1\n", encoding="utf-8")
    context, session, pair = _operation_preview(project, new_value=5)
    operation, preview = pair
    authorization = _authorization(context, session, operation, preview)
    source_path.write_text("value = 99\n", encoding="utf-8")
    session.begin_write_transaction(authorization.transaction_id)
    try:
        execute_project_web_ai_apply(
            operation=operation,
            preview=preview,
            authorization=authorization,
            session_identity=session.identity,
            context=context,
        )
    except ProjectWebAIApplyError as exc:
        session.finish_write_transaction(authorization.transaction_id, exc.status)
        require("FRESHNESS_MISMATCH" in str(exc), "stale hash marker missing")
    else:
        raise AssertionError("stale source was overwritten")
    require(source_path.read_text(encoding="utf-8") == "value = 99\n",
            "stale source changed during rejection")
    print("IMMEDIATE_PREWRITE_SOURCE_FRESHNESS: PASS")
    print("STALE_SOURCE_REJECTED_WITHOUT_OVERWRITE: PASS")

    session.begin_write_transaction("unresolved-fixture")
    session.finish_write_transaction("unresolved-fixture", "UNRESOLVED")
    try:
        session.request_switch(str(root / "other"), worker_running=False)
    except ProjectWebAISessionStateError:
        pass
    else:
        raise AssertionError("unresolved transaction did not block Project switch")
    print("UNRESOLVED_TRANSACTION_BLOCKS_PROJECT_SWITCH: PASS")

def validate_path_and_static_contracts(project_root: Path, fixture_root: Path) -> None:
    """Prove path-link rejection and remote-AI non-authority contracts."""
    from kanda_reasoner_app.reasoner_engine.project_web_ai_write_storage import (
        contained_project_file,
    )

    project = fixture_root / "link_project"
    project.mkdir()
    target = project / "target.py"
    target.write_text("value = 1\n", encoding="utf-8")
    link = project / "link.py"
    try:
        link.symlink_to(target.name)
    except OSError:
        print("SYMLINK_COMPONENT_REJECTION: NOT_APPLICABLE")
    else:
        try:
            contained_project_file(project.resolve(), "link.py")
        except RuntimeError:
            print("SYMLINK_COMPONENT_REJECTION: PASS")
        else:
            raise AssertionError("symlink target was accepted for source write")

    engine = project_root / "kanda_reasoner_app" / "reasoner_engine"
    contracts = (engine / "project_web_ai_change_contracts.py").read_text(encoding="utf-8")
    workers = (engine / "project_web_ai_workers.py").read_text(encoding="utf-8")
    broker = (engine / "project_web_ai_write_broker.py").read_text(encoding="utf-8")
    require("execute_project_web_ai_apply" not in contracts, "remote proposal owns broker")
    require("execute_project_web_ai_apply" not in workers, "remote worker owns broker")
    require("os.path, \"isjunction\"" in (engine / "project_web_ai_write_storage.py").read_text(encoding="utf-8"), "junction guard missing")
    storage = (engine / "project_web_ai_write_storage.py").read_text(encoding="utf-8")
    require("_reject_link_components(shadow_root, lexical)" in storage,
            "Shadow link-component guard missing")

    unsafe = fixture_root / "unsafe_id_project"
    unsafe.mkdir()
    (unsafe / "sample.py").write_text("value = 1\n", encoding="utf-8")
    context, session, pair = _operation_preview(unsafe, new_value=8)
    operation, preview = pair
    authorization = replace(
        _authorization(context, session, operation, preview),
        transaction_id="../escape",
    )
    from kanda_reasoner_app.reasoner_engine.project_web_ai_write_broker import (
        ProjectWebAIApplyError, execute_project_web_ai_apply,
    )
    try:
        execute_project_web_ai_apply(
            operation=operation, preview=preview, authorization=authorization,
            session_identity=session.identity, context=context,
        )
    except ProjectWebAIApplyError as exc:
        require("UNSAFE_TRANSACTION_ID" in str(exc), "unsafe ID marker missing")
    else:
        raise AssertionError("unsafe transaction identity was accepted")
    require(not (Path(context.daily_work_root).parent / "escape").exists(),
            "unsafe transaction identity escaped daily-work")
    print("UNTRUSTED_AUTHORIZATION_ID_REJECTED: PASS")
    print("SHADOW_LINK_COMPONENT_REJECTION: PASS")
    print("REMOTE_AI_HAS_NO_WRITE_BROKER_CAPABILITY: PASS")
    print("WINDOWS_JUNCTION_GUARD_PRESENT: PASS")

def validate_real_qt(project_root: Path) -> None:
    """Instantiate the real Preview dialog and require local authorization UI."""
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    if os.name == "nt" and Path("C:/Windows/Fonts").is_dir():
        os.environ.setdefault("QT_QPA_FONTDIR", "C:/Windows/Fonts")
        print("QT_OFFSCREEN_FONTDIR_READY: PASS")
    try:
        from PySide6.QtWidgets import QApplication, QPushButton
    except ImportError:
        print("REAL_QT_GOVERNED_APPLY_DIALOG: NOT_APPLICABLE")
        return
    from kanda_reasoner_app.reasoner_engine.project_web_ai_change_preview import (
        ProjectWebAIChangePreviewDialog,
    )
    from kanda_reasoner_app.reasoner_engine.project_web_ai_shadow import (
        ProjectWebAIShadowPreview,
        ShadowTargetPreview,
    )

    app = QApplication.instance() or QApplication([])
    preview = ProjectWebAIShadowPreview(
        operation_id="operation",
        shadow_root=str(project_root),
        summary="summary",
        targets=(
            ShadowTargetPreview(
                relative_path="sample.py",
                original_sha256="a" * 64,
                proposed_sha256="b" * 64,
                shadow_path=str(project_root / "sample.py"),
                unified_diff="--- a/sample.py\n+++ b/sample.py\n@@ -1 +1 @@\n-a\n+b\n",
                python_syntax_status="PASS",
            ),
        ),
        affected_public_contracts=(),
        required_validators=(),
        known_risks=(),
        validation_markers=("PASS",),
    )
    dialog = ProjectWebAIChangePreviewDialog(
        preview,
        delete_callback=lambda: None,
        apply_callback=lambda: None,
    )
    apply_buttons = [
        button
        for button in dialog.findChildren(QPushButton)
        if button.objectName() == "projectWebAIAuthorizeApplyButton"
    ]
    require(len(apply_buttons) == 1, "governed Apply button is missing or duplicated")
    require("Authorize Project Update" == apply_buttons[0].text(), "Apply label drift")
    dialog.close()
    app.processEvents()
    print("REAL_QT_GOVERNED_APPLY_DIALOG: PASS")


def validate_module_sizes(project_root: Path) -> None:
    """Require every new or touched Python owner to remain at most 500 lines."""
    paths = (
        "kanda_reasoner_app/reasoner_engine/project_web_ai_apply_contracts.py",
        "kanda_reasoner_app/reasoner_engine/project_web_ai_apply_receipts.py",
        "kanda_reasoner_app/reasoner_engine/project_web_ai_apply_workflow.py",
        "kanda_reasoner_app/reasoner_engine/project_web_ai_write_broker.py",
        "kanda_reasoner_app/reasoner_engine/project_web_ai_write_storage.py",
        "kanda_reasoner_app/reasoner_engine/project_web_ai_switch_guard.py",
        "kanda_reasoner_app/reasoner_engine/project_web_ai_bridge.py",
        "kanda_reasoner_app/reasoner_engine/project_web_ai_session.py",
        "kanda_reasoner_app/reasoner_engine/project_web_ai_change_preview.py",
        "kanda_reasoner_app/reasoner_engine/project_web_ai_change_preparation.py",
        "kanda_reasoner_app/reasoner_engine/project_web_ai_tab.py",
        "kanda_reasoner_app/reasoner_engine/project_web_ai_tab_ui.py",
        "tools/validate_project_web_ai_governed_apply_v1.py",
    )
    for relative in paths:
        count = len((project_root / relative).read_text(encoding="utf-8").splitlines())
        require(count <= 500, relative + " exceeds 500 physical lines")
    print("TOUCHED_SOURCE_MODULES_MAX_500_LINES: PASS")


def main() -> int:
    """Run deterministic Phase 3 source-write and UI validations."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=str(Path(__file__).resolve().parents[1]))
    args = parser.parse_args()
    project_root = Path(args.root).expanduser().resolve()
    sys.path.insert(0, str(project_root))
    with tempfile.TemporaryDirectory(prefix="kanda_web_ai_apply_") as temp:
        fixture_root = Path(temp)
        validate_success_and_one_use(fixture_root)
        validate_rollback(fixture_root)
        validate_session_and_freshness(fixture_root)
        validate_stale_source_and_unresolved_switch(fixture_root)
        validate_path_and_static_contracts(project_root, fixture_root)
    validate_real_qt(project_root)
    validate_module_sizes(project_root)
    print("VALIDATION OK: project-web-ai-governed-apply-v1")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
