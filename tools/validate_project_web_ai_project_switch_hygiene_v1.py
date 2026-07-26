# project-path: tools/validate_project_web_ai_project_switch_hygiene_v1.py
"""Focused validation for disposable Project Web AI session switching."""

from __future__ import annotations

import argparse
import os
import sys
import tempfile
from pathlib import Path

FEATURE_ID = "project-web-ai-project-switch-hygiene-v1"
TOUCHED_CODE = (
    "kanda_reasoner_app/reasoner_engine/project_web_ai_session.py",
    "kanda_reasoner_app/reasoner_engine/project_web_ai_tab.py",
    "kanda_reasoner_app/reasoner_engine/project_web_ai_switch_guard.py",
    "kanda_reasoner_app/reasoner_engine/project_web_ai_conversations.py",
    "kanda_reasoner_app/web_ai_provider_contracts.py",
    "tools/validate_project_web_ai_project_switch_hygiene_v1.py",
)


def require(condition: bool, message: str) -> None:
    """Raise one focused validation failure."""
    if not condition:
        raise AssertionError(message)


def fake_snapshot(root: Path, *, suffix: str):
    """Return one immutable selected-Project snapshot fixture."""
    from kanda_reasoner_app.web_ai_provider_contracts import ContextSnapshot

    resolved = root.resolve(strict=False)
    return ContextSnapshot(
        tool_project_slug="kanda_reasoner",
        tool_source_root=str(resolved.parent / "kanda_reasoner_tool"),
        project_slug=resolved.name,
        project_id="project-id-" + suffix,
        project_root=str(resolved),
        project_root_fingerprint="root-fingerprint-" + suffix,
        support_root=str(resolved.parent / (resolved.name + "_show_project_to_AI")),
        daily_work_root=str(
            resolved.parent / (resolved.name + "_delete_after_daily_work")
        ),
        self_hosting_mode=False,
        support_identity_status="VERIFIED",
        collector_status="complete",
        snapshot_id="snapshot-" + suffix,
        context_hash=(suffix * 64)[:64],
        generated_at_utc="2026-07-22T00:00:00Z",
        trusted_boundary_text="Tool and Project identities remain separate.",
        context_text="Compact Project evidence for " + resolved.name,
        context_bytes=64,
        artifacts_loaded=(resolved.name + "__ai_briefing.json",),
        omitted_sections=("exact source files",),
    )


def fake_request(snapshot, project_epoch: int, session_id: str = "session-1"):
    """Return one complete immutable request identity fixture."""
    from kanda_reasoner_app.web_ai_provider_contracts import (
        ProjectWebAIRequestIdentity,
    )

    return ProjectWebAIRequestIdentity(
        request_id="request-" + str(project_epoch),
        session_id=session_id,
        project_id=snapshot.project_id,
        project_slug=snapshot.project_slug,
        project_root_fingerprint=snapshot.project_root_fingerprint,
        support_root=snapshot.support_root,
        snapshot_id=snapshot.snapshot_id,
        context_hash=snapshot.context_hash,
        gateway_id="openrouter",
        model_id="fixture/model",
        privacy_approval_id="approval-" + str(project_epoch),
        created_at_utc="2026-07-22T00:00:00Z",
        project_epoch=project_epoch,
    )


def validate_lifecycle_state_machine() -> None:
    """Prove current-root, worker lock, and stale-result transitions."""
    from kanda_reasoner_app.reasoner_engine.project_web_ai_session import (
        ProjectWebAISessionLifecycle,
        ProjectWebAISessionStateError,
    )

    with tempfile.TemporaryDirectory(prefix="kanda_project_switch_state_") as temp:
        base = Path(temp)
        roots = tuple(base / name for name in ("project_a", "project_b", "project_c"))
        for root in roots:
            root.mkdir()
        snapshot_a = fake_snapshot(roots[0], suffix="a")
        snapshot_b = fake_snapshot(roots[1], suffix="b")
        snapshot_c = fake_snapshot(roots[2], suffix="c")

        lifecycle = ProjectWebAISessionLifecycle()
        first = lifecycle.request_switch(str(roots[0]), worker_running=False)
        require(first.project_epoch == 1, "first Project epoch is not one")
        require(first.reload_allowed, "settled first root cannot reload")
        require(
            lifecycle.reload_is_current(first.project_epoch, str(roots[0])),
            "current first reload was rejected",
        )
        identity_a = lifecycle.bind_snapshot(snapshot_a)
        request_a = fake_request(snapshot_a, identity_a.project_epoch)
        require(
            lifecycle.request_is_current(request_a, snapshot_a),
            "current Project A request was rejected",
        )
        print("CURRENT_PROJECT_REQUEST_ACCEPTED: PASS")

        second = lifecycle.request_switch(str(roots[1]), worker_running=True)
        require(second.wait_for_worker, "active worker did not block Project B")
        require(not second.reload_allowed, "Project B reloaded before settlement")
        require(lifecycle.identity is None, "old Project identity survived switch")
        require(
            not lifecycle.request_is_current(request_a, snapshot_a),
            "old Project A request remained authoritative",
        )
        print("ACTIVE_REQUEST_BLOCKS_PROJECT_RELOAD_UNTIL_SETTLED: PASS")

        third = lifecycle.request_switch(str(roots[2]), worker_running=True)
        require(third.project_epoch == 3, "latest Project epoch was not advanced")
        require(
            lifecycle.pending_root == str(roots[2].resolve(strict=False)),
            "latest pending root did not supersede Project B",
        )
        settled = lifecycle.worker_settled()
        require(settled.reload_allowed, "latest Project did not reload after settlement")
        require(
            lifecycle.reload_is_current(settled.project_epoch, str(roots[2])),
            "latest Project C reload was rejected",
        )
        try:
            lifecycle.bind_snapshot(snapshot_b)
        except ProjectWebAISessionStateError:
            print("STALE_PROJECT_SNAPSHOT_REJECTED: PASS")
        else:
            raise AssertionError("stale Project B snapshot was accepted")

        identity_c = lifecycle.bind_snapshot(snapshot_c)
        request_c = fake_request(snapshot_c, identity_c.project_epoch)
        require(
            lifecycle.request_is_current(request_c, snapshot_c),
            "current Project C request was rejected",
        )
        require(
            not lifecycle.request_is_current(request_a, snapshot_c),
            "late Project A result reached Project C",
        )
        print("LATE_PREVIOUS_PROJECT_RESULT_REJECTED: PASS")

        lifecycle.invalidate_for_disposal()
        require(lifecycle.identity is None, "dispose retained Project identity")
        require(
            not lifecycle.request_is_current(request_c, snapshot_c),
            "disposed session still accepted results",
        )
        print("DISPOSE_INVALIDATES_PROJECT_AUTHORITY: PASS")


def validate_source_contracts(root: Path) -> None:
    """Validate ownership, module size, and no-write boundaries."""
    session = (
        root / "kanda_reasoner_app/reasoner_engine/project_web_ai_session.py"
    ).read_text(encoding="utf-8")
    tab = (
        root / "kanda_reasoner_app/reasoner_engine/project_web_ai_tab.py"
    ).read_text(encoding="utf-8")
    conversations = (
        root / "kanda_reasoner_app/reasoner_engine/project_web_ai_conversations.py"
    ).read_text(encoding="utf-8")
    contracts = (root / "kanda_reasoner_app/web_ai_provider_contracts.py").read_text(
        encoding="utf-8"
    )
    switch_guard = (
        root / "kanda_reasoner_app/reasoner_engine/project_web_ai_switch_guard.py"
    ).read_text(encoding="utf-8")

    for token in (
        "class ProjectWebAISessionLifecycle",
        "def request_switch(",
        "def worker_settled(",
        "def reload_is_current(",
        "def request_is_current(",
        "def invalidate_for_disposal(",
    ):
        require(token in session, "session lifecycle contract missing: " + token)
    for forbidden in ("write_text(", "write_bytes(", "unlink(", "rmtree("):
        require(forbidden not in session, "session owner gained file-write authority")
    print("PROJECT_SESSION_OWNER_IS_TRANSIENT_AND_WRITE_FREE: PASS")

    for token in (
        "request_guarded_project_switch(self, text)",
        "self._project_session.worker_settled()",
        "self._project_session.reload_is_current(",
        "self._project_session.request_is_current(identity, context)",
        "self._clear_project_session_ui()",
        "Project switch is blocked until the previous request settles.",
        "catalog_changed.connect(self._on_web_catalog_changed)",
        "if self._chat_thread is not None:",
        "event.ignore()",
    ):
        require(token in tab, "Project Web AI tab lifecycle route missing: " + token)
    require(
        "owner._project_session.request_switch(" in switch_guard,
        "guarded Project switch does not delegate to the session owner",
    )
    require(
        "PROJECT_SWITCH_BLOCKED_BY_APPLY_TRANSACTION" in session,
        "source-write transaction does not block Project switching",
    )
    require("project_epoch=session_identity.project_epoch" in tab,
            "request identity lacks current Project epoch")
    require("lambda _models" not in tab,
            "application-scoped catalog signal retains a page lambda")
    require("project_epoch: int = 0" in contracts,
            "request contract lacks backwards-compatible Project epoch")
    require("def all(self)" not in conversations,
            "_ChatStore still shadows the all built-in")
    require("def all_sessions(self)" in conversations,
            "renamed chat-store accessor is missing")
    print("PROJECT_SWITCH_ROUTE_AND_REQUEST_EPOCH: PASS")
    print("OWNED_WEB_CONFIG_CALLBACK_LIFECYCLE: PASS")
    print("CLOSE_WAITS_FOR_ACTIVE_REQUEST_SETTLEMENT: PASS")
    print("CHAT_STORE_SYMBOL_SHADOWING_REMOVED: PASS")

    for relative in TOUCHED_CODE:
        lines = len((root / relative).read_text(encoding="utf-8").splitlines())
        require(lines <= 500, relative + " exceeds 500 physical lines")
    print("TOUCHED_SOURCE_MODULES_MAX_500_LINES: PASS")



def validate_live_architecture_scan(root: Path) -> None:
    """Require the current strict architecture detector to accept touched code."""
    import importlib

    architecture = importlib.import_module(
        "kanda_reasoner_app.manage_architecture.manage_architecture"
    )
    modules = {}
    for relative in TOUCHED_CODE:
        module, warnings = architecture.scan_module(
            root,
            root / relative,
            set(),
        )
        require(not warnings, relative + " produced architecture scan warnings")
        modules[module.module_id] = module
    issues = architecture.detect_symbol_shadowing_issues(root, modules)
    if issues:
        details = "\n".join(
            str(issue.path) + " :: " + str(issue.message)
            for issue in issues
        )
        raise AssertionError("TOUCHED_SOURCE_SYMBOL_SHADOWING_REMAINS:\n" + details)
    print("TOUCHED_SOURCE_SYMBOL_SHADOWING: PASS")

def validate_real_widget() -> None:
    """Exercise real Qt Project A to B and active-worker switch behavior."""
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    if os.name == "nt" and Path("C:/Windows/Fonts").is_dir():
        os.environ.setdefault("QT_QPA_FONTDIR", "C:/Windows/Fonts")

    try:
        from PySide6.QtTest import QTest
        from PySide6.QtWidgets import QApplication
    except ModuleNotFoundError:
        if os.environ.get("KANDA_ALLOW_STATIC_VALIDATION") == "1":
            print("REAL_QT_PROJECT_SWITCH_VALIDATION: SKIPPED_NO_PYSIDE6")
            return
        raise

    import kanda_reasoner_app.reasoner_engine.project_web_ai_tab as tab_module
    from kanda_reasoner_app.reasoner_engine.project_web_ai_tab import ProjectWebAITab

    class FakeWorker:
        """Record cooperative cancellation without starting a real thread."""

        def __init__(self) -> None:
            self.cancel_count = 0

        def cancel(self) -> None:
            self.cancel_count += 1

    app = QApplication.instance() or QApplication([])
    original_loader = tab_module.load_project_web_ai_context
    widget = ProjectWebAITab()
    widget.resize(1200, 760)
    widget.show()
    app.processEvents()

    with tempfile.TemporaryDirectory(prefix="kanda_project_switch_qt_") as temp:
        base = Path(temp)
        roots = tuple(base / name for name in ("project_a", "project_b", "project_c"))
        for root in roots:
            root.mkdir()
        snapshots = {
            str(roots[0].resolve(strict=False)): fake_snapshot(roots[0], suffix="a"),
            str(roots[1].resolve(strict=False)): fake_snapshot(roots[1], suffix="b"),
            str(roots[2].resolve(strict=False)): fake_snapshot(roots[2], suffix="c"),
        }

        def fixture_loader(root_text: str):
            key = str(Path(root_text).expanduser().resolve(strict=False))
            return snapshots[key]

        tab_module.load_project_web_ai_context = fixture_loader
        try:
            widget.project_root_edit.setText(str(roots[0]))
            QTest.qWait(130)
            app.processEvents()
            require(widget._context is snapshots[str(roots[0].resolve(strict=False))],
                    "Project A context did not load")

            widget._begin_chat_turn("Old Project question")
            widget.provenance_box.setPlainText("Old Project provenance")
            widget._history = [{"role": "user", "content": "old"}]
            widget.project_root_edit.setText(str(roots[1]))
            QTest.qWait(130)
            app.processEvents()

            require(widget._context is snapshots[str(roots[1].resolve(strict=False))],
                    "Project B context did not load")
            require(widget.chat_list.count() == 1,
                    "old Project chat entries survived switch")
            require(not widget._active_chat().messages,
                    "old Project transcript survived switch")
            require(not widget.question_edit.toPlainText(),
                    "old Project composer survived switch")
            require(not widget.provenance_box.toPlainText(),
                    "old Project provenance survived switch")
            require(not widget._history, "old Project model history survived switch")
            require("Old Project question" not in widget.answer_box.toPlainText(),
                    "old Project content remained visible")
            print("PROJECT_SWITCH_CLEARS_CHAT_AND_PROVENANCE: PASS")
            print("NEW_PROJECT_STARTS_WITH_EMPTY_AGENT_STATE: PASS")

            fake_worker = FakeWorker()
            widget._chat_thread = object()
            widget._chat_worker = fake_worker
            widget.project_root_edit.setText(str(roots[2]))
            QTest.qWait(130)
            app.processEvents()
            require(fake_worker.cancel_count == 1,
                    "active request was not cancelled on Project switch")
            require(widget._context is None,
                    "Project C loaded before prior worker settlement")
            require(widget._project_session.waiting_for_worker,
                    "worker-settlement lock was not retained")
            print("REAL_QT_PROJECT_SWITCH_WAITS_FOR_WORKER: PASS")

            widget._chat_thread_finished()
            QTest.qWait(130)
            app.processEvents()
            require(widget._context is snapshots[str(roots[2].resolve(strict=False))],
                    "Project C did not load after worker settlement")
            require(not widget._project_session.waiting_for_worker,
                    "worker-settlement lock survived completion")
            require(widget.chat_list.count() == 1 and not widget._active_chat().messages,
                    "Project C did not start with an empty session")
            print("REAL_QT_LATEST_PROJECT_RELOADS_AFTER_SETTLEMENT: PASS")
        finally:
            tab_module.load_project_web_ai_context = original_loader

    widget.close()
    widget.deleteLater()
    app.processEvents()


def main() -> int:
    """Run the complete focused Project-switch validation."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=str(Path.cwd()))
    args = parser.parse_args()
    root = Path(args.root).expanduser().resolve(strict=True)
    sys.path.insert(0, str(root))

    validate_lifecycle_state_machine()
    validate_source_contracts(root)
    validate_live_architecture_scan(root)
    validate_real_widget()
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
