"""Validate path handoff, short workspaces, text return, and full workspace cleaning."""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import shutil
from types import SimpleNamespace
import zipfile

from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.advanced_quality_review_contract import build_analysis_identity
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.external_ai_candidate_exchange_service import create_external_ai_candidate_exchange
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.external_ai_candidate_return_text_intake import import_external_ai_candidate_answer_text
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.external_ai_exchange_workspace import clean_external_ai_exchange_workspace

FEATURE_ID = "external-ai-candidate-exchange-path-handoff-text-return-cleaner-v1"


@dataclass(frozen=True)
class _CrossCheckReport:
    identity_hash: str

    def to_dict(self) -> dict[str, object]:
        return {
            "analysis_identity_hash": self.identity_hash,
            "quality_decision": "PASS_WITH_WARNINGS",
            "rule_results": [],
        }


def main() -> None:
    repository_root = Path(__file__).resolve().parents[1]
    fixture = repository_root / "_external_ai_exchange_path_handoff_fixture"
    _clean(fixture)
    project_root = fixture / "sample_project"
    project_root.mkdir(parents=True)
    target = project_root / "pkg" / "main_helper_mapper.py"
    target.parent.mkdir(parents=True)
    target.write_text("def original():\n    return 1\n", encoding="utf-8")
    source_before = _hash_tree(project_root)

    preview_root = fixture / "preview_support"
    preview_root.mkdir(parents=True)
    candidates = {
        "main_helper_mapper.py": "from ._helper import helper\n\ndef original():\n    return helper()\n",
        "_helper.py": "def helper():\n    return 1\n",
    }
    preview_files = []
    for relative, content in candidates.items():
        path = preview_root / relative
        path.write_text(content, encoding="utf-8")
        preview_files.append(SimpleNamespace(
            relative_path=relative,
            content_hash=_hash_file(path),
            role="facade" if relative == "main_helper_mapper.py" else "helper",
            symbols=[],
            physical_lines=len(content.splitlines()),
        ))

    card_identity = "b9a3459bbdc98849ff0c6bfd761aaa3200050444f383f18a0db662ab0cd644e9"
    plan_payload = {
        "target_file": str(target),
        "status": "ready",
        "source_content_hash": _hash_file(target),
        "symbols": [],
        "proposed_modules": [],
        "docstring_proposals": [],
    }
    analysis_payload = {
        "source_path": str(target),
        "source_content_hash": _hash_file(target),
        "imports": [],
        "symbols": [],
    }
    snapshot = SimpleNamespace(
        integrity_valid=lambda: True,
        snapshot_hash=card_identity,
        plan_json=json.dumps(plan_payload),
        analysis_json=json.dumps(analysis_payload),
    )
    preview = SimpleNamespace(
        status="real_preview_written",
        blockers=[],
        preview_root=str(preview_root),
        source_content_hash=_hash_file(target),
        files=preview_files,
        warnings=[],
    )
    identity = build_analysis_identity(
        project_card_identity=card_identity,
        target_relative_path="pkg/main_helper_mapper.py",
        baseline_hash="baseline-hash-001",
        preview_hash="preview-hash-001",
        refactor_plan_hash="plan-hash-001",
        analyzer_lock_hash="lock-hash-001",
        analyzer_config_hash="config-hash-001",
    )
    aqr_context = SimpleNamespace(request=SimpleNamespace(analysis_identity=identity))
    outcome = SimpleNamespace(
        analysis_identity_hash=identity.identity_hash,
        cross_check_report=_CrossCheckReport(identity.identity_hash),
    )
    completion = SimpleNamespace(
        semantic_review={"status": "semantic_diff_ready", "warnings": []},
        text_diff=SimpleNamespace(status="ready", rows=(), warnings=()),
        shadow_validation=SimpleNamespace(status="passed"),
        contract=SimpleNamespace(contract_id="contract-001"),
        sealed_payload=SimpleNamespace(payload_hash="payload-001"),
    )

    first = create_external_ai_candidate_exchange(
        active_project_root=project_root,
        plan_snapshot=snapshot,
        preview_result=preview,
        aqr_context=aqr_context,
        aqr_outcome=outcome,
        completion_evidence=completion,
    )
    workspace = Path(first.workspace_root)
    assert workspace.name == "main_helper_mapper__b9a3459bbdc9", workspace
    assert card_identity not in str(workspace)
    assert Path(first.zip_path).parent == workspace
    print("AI_EXCHANGE_SHORT_TARGET_READABLE_WORKSPACE: PASS")

    with zipfile.ZipFile(first.zip_path) as archive:
        task = archive.read("EXTERNAL_AI_TASK.md").decode("utf-8")
    for marker in (
        "ZIP -> INSTALL -> VALIDATE -> Error Memory intake -> FREEZE evidence preparation",
        "pending AI-assisted Error Memory intake",
        "KANDA_AI_CANDIDATE_RETURN_BEGIN",
        "candidate_generation_text",
        "content_utf8",
        first.exchange_identity.identity_hash,
    ):
        assert marker in task, marker
    print("AI_EXCHANGE_TASK_TEACHES_GOVERNED_PATCH_AND_OPTIONAL_TEXT_RETURN: PASS")

    second = create_external_ai_candidate_exchange(
        active_project_root=project_root,
        plan_snapshot=snapshot,
        preview_result=preview,
        aqr_context=aqr_context,
        aqr_outcome=outcome,
        completion_evidence=completion,
    )
    assert second.exchange_id == "EXCH-0002"
    assert Path(second.workspace_root) == workspace
    print("AI_EXCHANGE_GENERATIONS_SHARE_INTUITIVE_WORKSPACE: PASS")

    returned = {
        "main_helper_mapper.py": "from ._helper import helper\n\ndef original():\n    return helper()\n",
        "_helper.py": "def helper():\n    return 2\n",
    }
    structured = _structured_text(first, returned)
    imported = import_external_ai_candidate_answer_text(
        active_project_root=project_root,
        exchange_result=first,
        answer_text=structured,
        active_project_card_identity=identity.project_card_identity,
        active_target_relative_path=identity.target_relative_path,
        active_preview_hash=identity.preview_hash,
    )
    assert imported.return_id == "RETURN-0001"
    assert Path(imported.return_root).is_dir()
    assert _hash_tree(project_root) == source_before
    staging = project_root.parent / f"{project_root.name}_delete_after_daily_work" / "ai_candidate_text_return_staging" / first.exchange_id
    assert not staging.exists()
    print("AI_RETURN_STRUCTURED_TEXT_REUSES_ZIP_INTAKE_AND_CLEANS_STAGING: PASS")
    print("AI_RETURN_STRUCTURED_TEXT_SOURCE_IMMUTABLE: PASS")

    bad_payload = json.loads(structured.split("\n", 1)[1].rsplit("\n", 1)[0])
    bad_payload["source_lineage"]["source_preview_hash"] = "stale"
    bad = "KANDA_AI_CANDIDATE_RETURN_BEGIN\n" + json.dumps(bad_payload) + "\nKANDA_AI_CANDIDATE_RETURN_END"
    try:
        import_external_ai_candidate_answer_text(
            active_project_root=project_root,
            exchange_result=first,
            answer_text=bad,
            active_project_card_identity=identity.project_card_identity,
            active_target_relative_path=identity.target_relative_path,
            active_preview_hash=identity.preview_hash,
        )
    except ValueError as error:
        assert "AI_RETURN_TEXT_LINEAGE_MISMATCH" in str(error)
    else:
        raise AssertionError("stale structured text must fail closed")
    print("AI_RETURN_STRUCTURED_TEXT_LINEAGE_FAILS_CLOSED: PASS")

    removed = clean_external_ai_exchange_workspace(
        active_project_root=project_root,
        project_card_identity=card_identity,
        target_relative_path=identity.target_relative_path,
    )
    assert removed
    assert workspace.is_dir()
    assert list(workspace.iterdir()) == []
    print("AI_EXCHANGE_CLEANER_REMOVES_ALL_EXCHANGES_RETURNS_AND_ZIPS: PASS")

    gui_path = repository_root / "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/external_ai_candidate_exchange_gui.py"
    gui_text = gui_path.read_text(encoding="utf-8")
    assert 'QPushButton("Path Canditates to AI")' in gui_text
    path_handler = gui_text.split("def _path_candidates_to_ai", 1)[1].split("def _import_ai_answer", 1)[0]
    assert "clipboard().setText(result.workspace_root)" in path_handler
    assert "openUrl" not in path_handler
    assert "choose_external_ai_return_input" in gui_text
    assert "import_external_ai_candidate_answer_text" in gui_text
    print("AI_EXCHANGE_PATH_BUTTON_CLIPBOARD_ONLY_NO_AUTO_OPEN: PASS")
    print("AI_RETURN_IMPORT_TEXT_WINDOW_AND_ZIP_ROUTE_PRESENT: PASS")

    module_root = repository_root / "kanda_reasoner_app/manage_architecture/large_file_refactor_planner"
    touched = (
        module_root / "external_ai_candidate_exchange_service.py",
        module_root / "external_ai_candidate_exchange_gui.py",
        module_root / "external_ai_candidate_exchange_prompt.py",
        module_root / "external_ai_candidate_return_dialog.py",
        module_root / "external_ai_candidate_return_text_intake.py",
        module_root / "external_ai_exchange_workspace.py",
    )
    for path in touched:
        assert len(path.read_text(encoding="utf-8").splitlines()) <= 500, path
    print("TOUCHED_SOURCE_MODULES_MAX_500_LINES: PASS")
    print("EXTERNAL_AI_CANDIDATE_EXCHANGE_PATH_HANDOFF_TEXT_RETURN_CLEANER: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    _clean(fixture)


def _structured_text(exchange, candidates: dict[str, str]) -> str:
    payload = {
        "schema_version": "1.0",
        "return_kind": "candidate_generation_text",
        "source_lineage": {
            "exchange_id": exchange.exchange_identity.exchange_id,
            "project_card_identity": exchange.exchange_identity.project_card_identity,
            "target_relative_path": exchange.exchange_identity.target_relative_path,
            "source_preview_hash": exchange.exchange_identity.source_preview_hash,
            "source_candidate_set_hash": exchange.exchange_identity.source_candidate_set_hash,
            "source_exchange_identity_hash": exchange.exchange_identity.identity_hash,
        },
        "candidate_family": [
            {"relative_path": name, "content_utf8": candidates[name]}
            for name in sorted(candidates)
        ],
    }
    return "KANDA_AI_CANDIDATE_RETURN_BEGIN\n" + json.dumps(payload) + "\nKANDA_AI_CANDIDATE_RETURN_END"


def _hash_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _hash_tree(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(root.rglob("*")):
        if path.is_file():
            digest.update(path.relative_to(root).as_posix().encode("utf-8"))
            digest.update(path.read_bytes())
    return digest.hexdigest()


def _clean(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)


if __name__ == "__main__":
    main()
