"""Validate Release 10 external AI return contract and optional candidate import."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import shutil
import sys
from types import SimpleNamespace
import zipfile

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.advanced_quality_review_contract import (
    build_analysis_identity,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.external_ai_candidate_exchange_contract import (
    build_ai_response_identity,
    build_candidate_set_identity,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.external_ai_candidate_exchange_service import (
    create_external_ai_candidate_exchange,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.external_ai_candidate_return_intake import (
    build_optional_ai_return_instructions,
    import_external_ai_candidate_answer,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_project_support_paths import (
    ai_refactoring_exchange_root,
    daily_work_root,
    resolve_workbench_preview_root,
)

FEATURE_ID = "external-ai-return-contract-optional-candidate-import-v1"


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
    repository_root = PROJECT_ROOT
    fixture = daily_work_root(repository_root) / "release10_return_validation_fixture"
    _clean(fixture)
    fixture.mkdir(parents=True)
    project_root = fixture / "sample_project"
    target = project_root / "pkg" / "module.py"
    target.parent.mkdir(parents=True)
    target.write_text("def original():\n    return 1\n", encoding="utf-8", newline="\n")
    source_before = _hash_tree(project_root)

    preview_root = resolve_workbench_preview_root(project_root, "release10-preview")
    preview_root.mkdir(parents=True)
    preview_candidates = {
        "module.py": "from .helper import helper\n\ndef original():\n    return helper()\n",
        "helper.py": "def helper():\n    return 1\n",
    }
    preview_files = []
    for relative, content in sorted(preview_candidates.items()):
        path = preview_root / relative
        path.write_text(content, encoding="utf-8", newline="\n")
        preview_files.append(
            SimpleNamespace(
                relative_path=relative,
                content_hash=_hash_file(path),
                role="facade" if relative == "module.py" else "helper",
                symbols=[],
                physical_lines=len(content.splitlines()),
            )
        )

    plan_payload = {
        "target_file": str(target),
        "status": "ready",
        "source_content_hash": _hash_file(target),
    }
    analysis_payload = {
        "source_path": str(target),
        "source_content_hash": _hash_file(target),
    }
    snapshot_hash = "release10-card-identity-001"
    snapshot = SimpleNamespace(
        integrity_valid=lambda: True,
        snapshot_hash=snapshot_hash,
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
        project_card_identity=snapshot_hash,
        target_relative_path="pkg/module.py",
        baseline_hash="baseline-hash-release10",
        preview_hash="preview-hash-release10",
        refactor_plan_hash="plan-hash-release10",
        analyzer_lock_hash="lock-hash-release10",
        analyzer_config_hash="config-hash-release10",
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
        contract=SimpleNamespace(contract_id="contract-release10"),
        sealed_payload=SimpleNamespace(payload_hash="payload-release10"),
    )
    exchange = create_external_ai_candidate_exchange(
        active_project_root=project_root,
        plan_snapshot=snapshot,
        preview_result=preview,
        aqr_context=aqr_context,
        aqr_outcome=outcome,
        completion_evidence=completion,
    )

    returned_candidates = {
        "helper.py": b"def helper():\n    return 2\n",
        "module.py": b"from .helper import helper\n\ndef original():\n    return helper()\n",
    }
    answer_zip = fixture / "valid_ai_answer.zip"
    _write_return_zip(answer_zip, exchange, returned_candidates)
    imported = import_external_ai_candidate_answer(
        active_project_root=project_root,
        exchange_result=exchange,
        answer_zip_path=answer_zip,
        active_project_card_identity=identity.project_card_identity,
        active_target_relative_path=identity.target_relative_path,
        active_preview_hash=identity.preview_hash,
    )
    assert imported.return_id == "RETURN-0001"
    assert imported.candidate_files == ("helper.py", "module.py")
    assert Path(imported.return_root).is_dir()
    print("AI_RETURN_SCHEMA_EXACT_AND_BOUNDED: PASS")
    print("AI_RETURN_LINEAGE_EXCHANGE_CARD_TARGET_PREVIEW_CANDIDATE_SET: PASS")

    _expect_blocked(
        lambda: import_external_ai_candidate_answer(
            active_project_root=project_root,
            exchange_result=exchange,
            answer_zip_path=answer_zip,
            active_project_card_identity="different-card",
            active_target_relative_path=identity.target_relative_path,
            active_preview_hash=identity.preview_hash,
        ),
        "AI_RETURN_LINEAGE_BLOCKED",
    )
    _expect_blocked(
        lambda: import_external_ai_candidate_answer(
            active_project_root=project_root,
            exchange_result=exchange,
            answer_zip_path=answer_zip,
            active_project_card_identity=identity.project_card_identity,
            active_target_relative_path=identity.target_relative_path,
            active_preview_hash="stale-preview-hash",
        ),
        "AI_RETURN_LINEAGE_BLOCKED",
    )
    print("AI_RETURN_STALE_OR_CROSS_LINEAGE_FAILS_CLOSED: PASS")

    incomplete_zip = fixture / "incomplete_ai_answer.zip"
    _write_return_zip(
        incomplete_zip,
        exchange,
        {"module.py": returned_candidates["module.py"]},
        expected_paths_override=("module.py",),
    )
    _expect_blocked(
        lambda: import_external_ai_candidate_answer(
            active_project_root=project_root,
            exchange_result=exchange,
            answer_zip_path=incomplete_zip,
            active_project_card_identity=identity.project_card_identity,
            active_target_relative_path=identity.target_relative_path,
            active_preview_hash=identity.preview_hash,
        ),
        "AI_RETURN_ARCHIVE_CONTENT_MISMATCH",
    )
    print("AI_RETURN_COMPLETE_CANDIDATE_FAMILY_REQUIRED: PASS")

    malicious_zip = fixture / "path_escape_ai_answer.zip"
    _write_return_zip(malicious_zip, exchange, returned_candidates, extra_name="../escape.py")
    _expect_blocked(
        lambda: import_external_ai_candidate_answer(
            active_project_root=project_root,
            exchange_result=exchange,
            answer_zip_path=malicious_zip,
            active_project_card_identity=identity.project_card_identity,
            active_target_relative_path=identity.target_relative_path,
            active_preview_hash=identity.preview_hash,
        ),
        "AI_RETURN_ARCHIVE_PATH_INVALID",
    )
    print("AI_RETURN_ZIP_PATH_TRAVERSAL_REJECTED: PASS")

    expected_support_root = ai_refactoring_exchange_root(project_root).resolve()
    Path(imported.return_root).resolve().relative_to(expected_support_root)
    try:
        Path(imported.return_root).resolve().relative_to(project_root.resolve())
    except ValueError:
        pass
    else:
        raise AssertionError("AI return generation must not be inside Project source")
    assert _hash_tree(project_root) == source_before
    assert preview_root.joinpath("helper.py").read_text(encoding="utf-8").endswith("return 1\n")
    print("AI_RETURN_IMPORT_PROJECT_SUPPORT_ONLY: PASS")
    print("AI_RETURN_IMPORT_SOURCE_IMMUTABLE: PASS")
    print("AI_RETURN_NEW_CANDIDATE_GENERATION_ONLY: PASS")

    second = import_external_ai_candidate_answer(
        active_project_root=project_root,
        exchange_result=exchange,
        answer_zip_path=answer_zip,
        active_project_card_identity=identity.project_card_identity,
        active_target_relative_path=identity.target_relative_path,
        active_preview_hash=identity.preview_hash,
    )
    assert second.return_id == "RETURN-0002"
    assert Path(imported.return_root).is_dir()
    print("AI_RETURN_IMPORT_GENERATION_APPEND_ONLY: PASS")

    default_task = Path(exchange.prompt_path).read_text(encoding="utf-8")
    optional = build_optional_ai_return_instructions(exchange)
    assert "complete cumulative governed KANDA patch ZIP" in default_task
    assert "default and preferred return route remains" in optional
    assert "Import AI Answer" in optional
    assert "new Project Support candidate generation" in optional
    print("AI_RETURN_DEFAULT_GOVERNED_PATCH_ROUTE_PRESERVED: PASS")

    receipt = json.loads(Path(imported.receipt_path).read_text(encoding="utf-8"))
    assert receipt["canonical_source_mutated"] is False
    assert receipt["preview_replaced"] is False
    assert receipt["transaction_prepared"] is False
    assert receipt["human_authorization_changed"] is False
    gui_text = (
        repository_root
        / "kanda_reasoner_app"
        / "manage_architecture"
        / "large_file_refactor_planner"
        / "external_ai_candidate_exchange_gui.py"
    ).read_text(encoding="utf-8")
    assert "Import AI Answer" in gui_text
    assert "new candidate generation only" in gui_text
    print("AI_RETURN_NO_PREVIEW_OR_TRANSACTION_AUTO_PROMOTION: PASS")

    touched = (
        repository_root
        / "kanda_reasoner_app"
        / "manage_architecture"
        / "large_file_refactor_planner"
        / "external_ai_candidate_return_intake.py",
        repository_root
        / "kanda_reasoner_app"
        / "manage_architecture"
        / "large_file_refactor_planner"
        / "external_ai_candidate_exchange_gui.py",
    )
    for path in touched:
        data = path.read_bytes()
        assert data.isascii(), path
        lines = data.decode("ascii").splitlines()
        assert 101 <= len(lines) <= 499, (path, len(lines))
    print("SOURCE_ASCII_UTF8_NO_BOM: PASS")
    print("MODULE_SIZE_POLICY_101_499: PASS")
    print("EXTERNAL_AI_RETURN_CONTRACT_OPTIONAL_CANDIDATE_IMPORT: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")

    _clean(fixture)


def _write_return_zip(
    path: Path,
    exchange: object,
    candidates: dict[str, bytes],
    *,
    expected_paths_override: tuple[str, ...] | None = None,
    extra_name: str = "",
) -> None:
    candidate_hashes = {
        relative: hashlib.sha256(data).hexdigest()
        for relative, data in sorted(candidates.items())
    }
    return_identity = build_candidate_set_identity(
        project_card_identity=exchange.candidate_identity.project_card_identity,
        target_relative_path=exchange.candidate_identity.target_relative_path,
        baseline_hash=exchange.candidate_identity.baseline_hash,
        preview_hash=exchange.candidate_identity.preview_hash,
        plan_hash=exchange.candidate_identity.plan_hash,
        candidate_file_hashes=candidate_hashes,
    )
    response = build_ai_response_identity(
        exchange_identity=exchange.exchange_identity,
        return_candidate_set_hash=return_identity.candidate_set_hash,
        return_schema_version="1.0",
    )
    manifest_paths = expected_paths_override or tuple(sorted(candidates))
    manifest = {
        "schema_version": "1.0",
        "return_schema_version": "1.0",
        "return_kind": "candidate_generation",
        "exchange_id": exchange.exchange_id,
        "source_exchange_identity_hash": exchange.exchange_identity.identity_hash,
        "response_identity_hash": response.identity_hash,
        "candidate_files": [
            {
                "relative_path": relative,
                "sha256": candidate_hashes[relative],
                "size_bytes": len(candidates[relative]),
            }
            for relative in manifest_paths
        ],
    }
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("AI_RETURN_MANIFEST.json", _json_text(manifest))
        archive.writestr(
            "lineage/AI_RESPONSE_IDENTITY.json",
            _json_text(response.to_dict()),
        )
        for relative, data in sorted(candidates.items()):
            archive.writestr("candidate_family/" + relative, data)
        if extra_name:
            archive.writestr(extra_name, b"forbidden")


def _expect_blocked(callback, marker: str) -> None:
    try:
        callback()
    except Exception as error:
        if marker not in str(error):
            raise AssertionError((marker, type(error).__name__, str(error))) from error
        return
    raise AssertionError("Expected blocker was not raised: " + marker)


def _json_text(payload: object) -> str:
    return json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=True) + "\n"


def _hash_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _hash_tree(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        digest.update(path.relative_to(root).as_posix().encode("utf-8"))
        digest.update(path.read_bytes())
    return digest.hexdigest()


def _clean(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)


if __name__ == "__main__":
    main()
