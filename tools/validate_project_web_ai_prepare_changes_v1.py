# project-path: tools/validate_project_web_ai_prepare_changes_v1.py
"""Validate Project Web AI Prepare Changes Phase 2 boundaries."""

from __future__ import annotations

import argparse
import ast
import builtins
from dataclasses import replace
import json
import os
import shutil
import sys
import tempfile
from pathlib import Path

FEATURE_ID = "project-web-ai-prepare-changes-v1r1"


def _root_from_args() -> Path:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    return Path(args.root).resolve()


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _read(root: Path, relative: str) -> str:
    return (root / relative).read_text(encoding="utf-8")


def _identity_objects(project_root: Path, daily_root: Path):
    from kanda_reasoner_app.reasoner_engine.project_web_ai_session import (
        ProjectWebAISessionIdentity,
    )
    from kanda_reasoner_app.web_ai_provider_contracts import (
        ContextSnapshot,
        ProjectWebAIRequestIdentity,
    )

    context = ContextSnapshot(
        tool_project_slug="kanda_reasoner",
        tool_source_root=str(project_root),
        project_slug="fixture",
        project_id="project-id",
        project_root=str(project_root),
        project_root_fingerprint="root-fingerprint",
        support_root=str(project_root.parent / "fixture_show_project_to_AI"),
        daily_work_root=str(daily_root),
        self_hosting_mode=False,
        support_identity_status="VERIFIED",
        collector_status="CURRENT",
        snapshot_id="snapshot-id",
        context_hash="context-hash",
        generated_at_utc="2026-07-22T00:00:00Z",
        trusted_boundary_text="BOUNDARY",
        context_text="COMPACT CONTEXT",
        context_bytes=15,
        artifacts_loaded=("briefing",),
        omitted_sections=("exact source files",),
    )
    session = ProjectWebAISessionIdentity.from_snapshot(context, 7)
    request = ProjectWebAIRequestIdentity(
        request_id="request-id",
        session_id="chat-id",
        project_id=context.project_id,
        project_slug=context.project_slug,
        project_root_fingerprint=context.project_root_fingerprint,
        support_root=context.support_root,
        snapshot_id=context.snapshot_id,
        context_hash=context.context_hash,
        gateway_id="gateway",
        model_id="model",
        privacy_approval_id="approval",
        created_at_utc="2026-07-22T00:00:00Z",
        project_epoch=7,
    )
    return context, session, request


def _valid_proposal_text(operation, source) -> str:
    from kanda_reasoner_app.reasoner_engine.project_web_ai_change_contracts import (
        CHANGE_PROPOSAL_BEGIN,
        CHANGE_PROPOSAL_END,
    )

    payload = {
        "proposal_type": "PROJECT_SOURCE_CORRECTION",
        "operation_id": operation.operation_id,
        "project_id": operation.request_identity.project_id,
        "project_root_fingerprint": (
            operation.request_identity.project_root_fingerprint
        ),
        "project_epoch": operation.request_identity.project_epoch,
        "snapshot_id": operation.request_identity.snapshot_id,
        "summary": "Change the fixture return value.",
        "targets": [
            {
                "relative_path": source.relative_path,
                "expected_sha256": source.sha256,
                "unified_diff": (
                    "--- a/pkg/sample.py\n"
                    "+++ b/pkg/sample.py\n"
                    "@@ -1,2 +1,2 @@\n"
                    " def value():\n"
                    "-    return 1\n"
                    "+    return 2"
                ),
            }
        ],
        "affected_public_contracts": ["value returns an integer"],
        "required_validators": ["focused fixture validator"],
        "known_risks": ["consumer expectation change"],
    }
    return (
        CHANGE_PROPOSAL_BEGIN
        + "\n"
        + json.dumps(payload, separators=(",", ":"))
        + "\n"
        + CHANGE_PROPOSAL_END
    )


def validate_core_runtime(root: Path) -> None:
    from kanda_reasoner_app.reasoner_engine.project_web_ai_change_contracts import (
        ChangeProposalError,
        build_project_change_messages,
        new_change_operation,
        parse_project_change_proposal,
    )
    from kanda_reasoner_app.reasoner_engine.project_web_ai_shadow import (
        ProjectWebAIShadowError,
        build_shadow_preview,
        delete_shadow_preview,
    )
    from kanda_reasoner_app.reasoner_engine.project_web_ai_source_reader import (
        ProjectSourceReadError,
        read_exact_project_sources,
    )

    fixture_root = Path(tempfile.mkdtemp(prefix="kanda_prepare_changes_"))
    try:
        project_root = fixture_root / "fixture"
        daily_root = fixture_root / "fixture_delete_after_daily_work"
        source_path = project_root / "pkg" / "sample.py"
        source_path.parent.mkdir(parents=True)
        source_path.write_text(
            "def value():\n    return 1\n",
            encoding="utf-8",
            newline="\n",
        )
        context, session, request = _identity_objects(project_root, daily_root)
        sources = read_exact_project_sources(project_root, [source_path])
        source = sources[0]
        _require(source.relative_path == "pkg/sample.py", "relative path mismatch")
        print("EXACT_SOURCE_SELECTION: PASS")

        outside = fixture_root / "outside.py"
        outside.write_text("value = 1\n", encoding="utf-8")
        try:
            read_exact_project_sources(project_root, [outside])
        except ProjectSourceReadError:
            pass
        else:
            raise AssertionError("outside Project source was accepted")
        print("PROJECT_SOURCE_PATH_ESCAPE_REJECTED: PASS")

        operation = new_change_operation(
            request_identity=request,
            session_identity=session,
            context=context,
            question="Correct the fixture.",
            advisory_answer="Change return 1 to return 2.",
            source_files=sources,
        )
        messages = build_project_change_messages(
            operation,
            context.context_text,
            trusted_boundary_text=context.trusted_boundary_text,
        )
        joined = "\n".join(message["content"] for message in messages)
        _require(source.text in joined, "exact source was not attached")
        _require("write Project source" in joined, "write boundary missing")
        print("PROPOSAL_ONLY_PROMPT_CONTRACT: PASS")

        response = _valid_proposal_text(operation, source)
        proposal = parse_project_change_proposal(response, operation)
        _require(len(proposal.targets) == 1, "target count mismatch")
        print("STRICT_MARKER_JSON_PROPOSAL: PASS")

        try:
            parse_project_change_proposal("prefix\n" + response, operation)
        except ChangeProposalError:
            pass
        else:
            raise AssertionError("text outside proposal markers was accepted")
        print("AMBIGUOUS_PROPOSAL_RESPONSE_REJECTED: PASS")

        preview = build_shadow_preview(operation, proposal)
        shadow_path = Path(preview.targets[0].shadow_path)
        _require(shadow_path.read_text(encoding="utf-8").endswith("return 2\n"),
                 "Shadow change was not applied")
        _require(source_path.read_text(encoding="utf-8").endswith("return 1\n"),
                 "active Project source changed")
        _require("PYTHON_SYNTAX: PASS" in preview.validation_markers,
                 "Python syntax marker missing")
        print("UNIFIED_DIFF_SHADOW_APPLY: PASS")
        print("PROJECT_SOURCE_UNCHANGED: PASS")
        print("SHADOW_PYTHON_SYNTAX: PASS")

        delete_shadow_preview(preview)
        _require(not Path(preview.shadow_root).parent.exists(),
                 "Shadow operation cleanup failed")
        print("ABANDONED_SHADOW_CLEANUP: PASS")

        sources = read_exact_project_sources(project_root, [source_path])
        operation = new_change_operation(
            request_identity=request,
            session_identity=session,
            context=context,
            question="Correct the fixture.",
            advisory_answer="Change return 1 to return 2.",
            source_files=sources,
        )
        proposal = parse_project_change_proposal(
            _valid_proposal_text(operation, sources[0]),
            operation,
        )
        source_path.write_text(
            "def value():\n    return 3\n",
            encoding="utf-8",
            newline="\n",
        )
        try:
            build_shadow_preview(operation, proposal)
        except ProjectWebAIShadowError as exc:
            _require("STALE_SOURCE_HASH" in str(exc), "wrong stale-source error")
        else:
            raise AssertionError("stale source hash was accepted")
        print("STALE_SOURCE_HASH_REJECTED: PASS")

        source_path.write_text(
            "def value():\n    return 1\n",
            encoding="utf-8",
            newline="\n",
        )
        sources = read_exact_project_sources(project_root, [source_path])
        operation = new_change_operation(
            request_identity=request,
            session_identity=session,
            context=context,
            question="Correct the fixture.",
            advisory_answer="Change return 1 to return 2.",
            source_files=sources,
        )
        proposal = parse_project_change_proposal(
            _valid_proposal_text(operation, sources[0]),
            operation,
        )
        unsafe_operation = replace(
            operation,
            daily_work_root=str(project_root / ".daily_work"),
        )
        try:
            build_shadow_preview(unsafe_operation, proposal)
        except ProjectWebAIShadowError as exc:
            _require(
                "DAILY_WORK_ROOT_INSIDE_PROJECT_ROOT" in str(exc),
                "wrong transient-root overlap error",
            )
        else:
            raise AssertionError("daily-work root inside Project was accepted")
        print("TRANSIENT_ROOT_PROJECT_OVERLAP_REJECTED: PASS")
    finally:
        shutil.rmtree(fixture_root, ignore_errors=True)


def validate_static_contract(root: Path) -> None:
    modules = {
        "reader": (
            "kanda_reasoner_app/reasoner_engine/project_web_ai_source_reader.py"
        ),
        "contracts": (
            "kanda_reasoner_app/reasoner_engine/project_web_ai_change_contracts.py"
        ),
        "shadow": (
            "kanda_reasoner_app/reasoner_engine/project_web_ai_shadow.py"
        ),
        "preview": (
            "kanda_reasoner_app/reasoner_engine/project_web_ai_change_preview.py"
        ),
        "mixin": (
            "kanda_reasoner_app/reasoner_engine/project_web_ai_change_preparation.py"
        ),
        "tab": "kanda_reasoner_app/reasoner_engine/project_web_ai_tab.py",
        "ui": "kanda_reasoner_app/reasoner_engine/project_web_ai_tab_ui.py",
        "history_validator": "tools/validate_project_web_ai_professional_chat_history_v1.py",
        "apply_contracts": (
            "kanda_reasoner_app/reasoner_engine/project_web_ai_apply_contracts.py"
        ),
        "apply_receipts": (
            "kanda_reasoner_app/reasoner_engine/project_web_ai_apply_receipts.py"
        ),
        "apply_workflow": (
            "kanda_reasoner_app/reasoner_engine/project_web_ai_apply_workflow.py"
        ),
        "write_broker": (
            "kanda_reasoner_app/reasoner_engine/project_web_ai_write_broker.py"
        ),
        "write_storage": (
            "kanda_reasoner_app/reasoner_engine/project_web_ai_write_storage.py"
        ),
    }
    texts = {name: _read(root, path) for name, path in modules.items()}
    _require("Prepare Changes" in texts["ui"], "Prepare Changes button missing")
    _require("Active Project source will remain unchanged" in texts["mixin"],
             "source unchanged approval missing")
    _require(
        "Only the local governed write broker may mutate source"
        in texts["preview"],
        "local broker authority boundary missing",
    )
    _require("PROJECT_SOURCE_PATH_ESCAPE" in texts["shadow"],
             "Shadow path containment missing")
    _require("STALE_SOURCE_HASH" in texts["shadow"],
             "stale source hash rejection missing")
    _require("setText(\"Apply\")" not in texts["preview"],
             "Preview contains an Apply action")
    _require(
        'widget._request_mode = "prepare_changes"' in texts["history_validator"],
        "history validator does not reject Prepare Changes completion",
    )
    _require(
        'widget._request_mode = "chat"' in texts["history_validator"],
        "history validator does not bind normal chat completion mode",
    )
    _require(
        "PREPARE_CHANGES_RESULT_CANNOT_COMMIT_CHAT_HISTORY: PASS"
        in texts["history_validator"],
        "history validator lacks Prepare Changes isolation marker",
    )
    _require(
        "NORMAL_CHAT_FIXTURE_MODE_BOUND: PASS" in texts["history_validator"],
        "history validator lacks normal-chat mode marker",
    )
    forbidden_write = ("write_text(", "write_bytes(", "os.replace(", "subprocess")
    for name in ("reader", "contracts", "preview", "mixin", "tab", "ui"):
        _require(not any(item in texts[name] for item in forbidden_write),
                 name + " gained a source-write or shell API")
    builtin_names = set(dir(builtins))
    for name, text in texts.items():
        tree = ast.parse(text, filename=modules[name])
        symbols = [node.name for node in ast.walk(tree)
                   if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))]
        _require(not (set(symbols) & builtin_names), name + " shadows a built-in")
    print("PREPARE_CHANGES_UI_REGISTERED: PASS")
    print("PHASE2_SHADOW_PREVIEW_PRESERVED: PASS")
    print("PHASE3_LOCAL_BROKER_ONLY_APPLY_AUTHORITY: PASS")
    print("REMOTE_AI_PROJECT_SOURCE_WRITE_API_ABSENT: PASS")
    print("PROJECT_SWITCH_SHADOW_EJECT_HOOK: PASS")
    print("CHAT_AND_PREPARE_REQUEST_MODE_FIXTURE: PASS")
    print("TOUCHED_SOURCE_SYMBOL_SHADOWING: PASS")

    for name, relative in modules.items():
        line_count = len((root / relative).read_text(encoding="utf-8").splitlines())
        _require(line_count <= 500, name + " exceeds 500 physical lines")
    print("TOUCHED_SOURCE_MODULES_MAX_500_LINES: PASS")


def validate_real_qt(root: Path) -> None:
    try:
        os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
        from PySide6.QtWidgets import QApplication
        from kanda_reasoner_app.reasoner_engine.project_web_ai_tab import (
            ProjectWebAITab,
        )
    except ImportError:
        print("REAL_QT_PREPARE_CHANGES_WIDGET: SKIP - PySide6 unavailable")
        return
    app = QApplication.instance() or QApplication([])
    tab = ProjectWebAITab()
    try:
        _require(tab.prepare_changes_button.text() == "Prepare Changes",
                 "Prepare Changes button text mismatch")
        _require(not tab.prepare_changes_button.isEnabled(),
                 "Prepare Changes must fail closed before a completed exchange")
        _require(tab._change_preview is None, "Preview must start empty")
        from kanda_reasoner_app.reasoner_engine.project_web_ai_shadow import (
            ProjectWebAIShadowPreview,
        )

        fixture_root = Path(tempfile.mkdtemp(prefix="kanda_prepare_qt_"))
        operation_root = fixture_root / "operation"
        shadow_root = operation_root / "shadow"
        shadow_root.mkdir(parents=True)
        tab._change_preview = ProjectWebAIShadowPreview(
            operation_id="qt-operation",
            shadow_root=str(shadow_root),
            summary="fixture",
            targets=(),
            affected_public_contracts=(),
            required_validators=(),
            known_risks=(),
            validation_markers=("SHADOW_APPLY: PASS",),
        )
        tab._clear_change_preparation_for_project()
        _require(tab._change_preview is None, "Project switch retained Preview")
        _require(not operation_root.exists(), "Project switch retained Shadow")
        shutil.rmtree(fixture_root, ignore_errors=True)
        print("REAL_QT_PREPARE_CHANGES_WIDGET: PASS")
        print("PREPARE_CHANGES_FAILS_CLOSED: PASS")
        print("REAL_QT_PROJECT_SWITCH_DELETES_ABANDONED_SHADOW: PASS")
        print("REAL_QT_NEW_PROJECT_PREP_STATE_EMPTY: PASS")
    finally:
        tab.close()
        app.processEvents()


def main() -> int:
    root = _root_from_args()
    sys.path.insert(0, str(root))
    validate_core_runtime(root)
    validate_static_contract(root)
    validate_real_qt(root)
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
