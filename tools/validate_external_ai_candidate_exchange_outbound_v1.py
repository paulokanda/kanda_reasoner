"""Validate Release 9 outbound External AI Candidate Exchange contracts."""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import shutil
import sys
from types import SimpleNamespace
from unittest.mock import patch
import zipfile

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.project_support_boundary import (
    canonical_transient_garbage_root,
)

from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.advanced_quality_review_contract import build_analysis_identity
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.external_ai_candidate_exchange_service import (
    clean_external_ai_exchange_folder,
    create_external_ai_candidate_exchange,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner import (
    workbench_project_support_paths as support_paths,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_project_support_paths import (
    ai_refactoring_exchange_root,
)

FEATURE_ID = "external-ai-candidate-exchange-outbound-v1"


@dataclass(frozen=True)
class _CrossCheckReport:
    identity_hash: str

    def to_dict(self) -> dict[str, object]:
        return {
            "analysis_identity_hash": self.identity_hash,
            "quality_decision": "PASS_WITH_WARNINGS",
            "rule_results": [
                {
                    "rule_id": "TEST_RULE",
                    "decision": "PASS",
                    "rationale": "controlled evidence",
                    "evidence_keys": [],
                }
            ],
        }


def main() -> None:
    fixture = (
        canonical_transient_garbage_root(PROJECT_ROOT)
        / "validation_fixtures"
        / "release9_exchange"
    )
    controlled_support_root = fixture / "controlled_project_support"
    _clean(fixture)
    try:
        with patch.object(
            support_paths,
            "project_support_root",
            return_value=controlled_support_root,
        ):
            _validate_fixture(fixture)
        print("AI_EXCHANGE_VALIDATION_SUPPORT_ISOLATED: PASS")
    finally:
        _clean(fixture)


def _validate_fixture(fixture: Path) -> None:
    project_root = fixture / "sample_project"
    project_root.mkdir(parents=True)
    target = project_root / "pkg" / "module.py"
    target.parent.mkdir(parents=True)
    target.write_text("def original():\n    return 1\n", encoding="utf-8")
    before = _hash_tree(project_root)

    preview_root = fixture / "preview_support"
    preview_root.mkdir(parents=True)
    candidates = {
        "module.py": "from .helper import helper\n\ndef original():\n    return helper()\n",
        "helper.py": "def helper():\n    return 1\n",
    }
    preview_files = []
    for relative, content in candidates.items():
        path = preview_root / relative
        path.write_text(content, encoding="utf-8")
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
    snapshot_hash = "card-identity-001"
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
        baseline_hash="baseline-hash-001",
        preview_hash="preview-hash-001",
        refactor_plan_hash="plan-hash-001",
        analyzer_lock_hash="lock-hash-001",
        analyzer_config_hash="config-hash-001",
    )
    aqr_context = SimpleNamespace(
        request=SimpleNamespace(analysis_identity=identity)
    )
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

    result = create_external_ai_candidate_exchange(
        active_project_root=project_root,
        plan_snapshot=snapshot,
        preview_result=preview,
        aqr_context=aqr_context,
        aqr_outcome=outcome,
        completion_evidence=completion,
    )
    exchange_root = Path(result.exchange_root)
    zip_path = Path(result.zip_path)
    assert exchange_root.is_dir()
    assert zip_path.is_file()
    assert result.candidate_files == ("helper.py", "module.py")
    assert (exchange_root / "candidate_family" / "helper.py").is_file()
    assert (exchange_root / "candidate_family" / "module.py").is_file()
    print("AI_EXCHANGE_COMPLETE_CANDIDATE_FAMILY: PASS")

    assert result.exchange_identity.project_card_identity == snapshot_hash
    assert result.exchange_identity.target_relative_path == "pkg/module.py"
    assert result.exchange_identity.source_preview_hash == identity.preview_hash
    assert (
        result.exchange_identity.source_candidate_set_hash
        == result.candidate_identity.candidate_set_hash
    )
    print("AI_EXCHANGE_LINEAGE_CARD_TARGET_PREVIEW_CANDIDATE_SET: PASS")

    required = {
        "workbench/_bundle_temp/BUNDLE_MANIFEST_EXTERNAL_AI_CANDIDATE_EXCHANGE.txt",
        "EXTERNAL_AI_TASK.md",
        "EXCHANGE_MANIFEST.json",
        "lineage/CANDIDATE_SET_IDENTITY.json",
        "lineage/EXCHANGE_IDENTITY.json",
        "candidate_family/module.py",
        "candidate_family/helper.py",
        "baseline_target/pkg/module.py",
        "context/workbench_plan.json",
        "context/module_analysis.json",
        "context/preview_manifest.json",
        "context/advanced_quality_review.json",
        "context/completion_review.json",
    }
    with zipfile.ZipFile(zip_path) as archive:
        names = set(archive.namelist())
        assert required <= names
        task = archive.read("EXTERNAL_AI_TASK.md").decode("utf-8")
        assert "complete cumulative governed KANDA patch ZIP" in task
        assert "Never directly write canonical Project source from this exchange" in task
        bundle_manifest = archive.read(
            "workbench/_bundle_temp/"
            "BUNDLE_MANIFEST_EXTERNAL_AI_CANDIDATE_EXCHANGE.txt"
        ).decode("utf-8")
        assert "SCOPE:" in bundle_manifest
        assert "VALIDATION:" in bundle_manifest
        assert "ROLLBACK:" in bundle_manifest
        plan_text = archive.read("context/workbench_plan.json").decode("utf-8")
        assert str(project_root) not in plan_text
        assert "pkg/module.py" in plan_text
    print("AI_EXCHANGE_BUNDLE_MANIFEST: PASS")
    print("AI_EXCHANGE_BOUNDED_CONTEXT_ZIP: PASS")
    print("AI_EXCHANGE_DEFAULT_RETURN_ROUTE_GOVERNED_PATCH_ZIP: PASS")
    print("AI_EXCHANGE_MACHINE_PATHS_REDACTED_TO_PROJECT_RELATIVE: PASS")

    expected_exchange_base = ai_refactoring_exchange_root(project_root).resolve()
    exchange_root.resolve().relative_to(expected_exchange_base)
    try:
        exchange_root.resolve().relative_to(project_root.resolve())
    except ValueError:
        pass
    else:
        raise AssertionError("exchange root must not be inside Project source")
    print("AI_EXCHANGE_PROJECT_SUPPORT_OWNERSHIP: PASS")

    assert _hash_tree(project_root) == before
    print("AI_EXCHANGE_SOURCE_IMMUTABLE: PASS")

    try:
        clean_external_ai_exchange_folder(
            active_project_root=project_root,
            exchange_root=project_root,
        )
    except ValueError:
        pass
    else:
        raise AssertionError("wrong-root clean must fail closed")
    removed = clean_external_ai_exchange_folder(
        active_project_root=project_root,
        exchange_root=exchange_root,
    )
    assert removed
    assert exchange_root.is_dir()
    assert list(exchange_root.iterdir()) == []
    assert zip_path.is_file()
    print("AI_EXCHANGE_CLEAN_DESCENDANT_ONLY: PASS")

    module_root = Path(__file__).resolve().parents[1] / "kanda_reasoner_app" / "manage_architecture" / "large_file_refactor_planner"
    gui_text = (module_root / "external_ai_candidate_exchange_gui.py").read_text(encoding="utf-8")
    completion_text = (module_root / "workbench_completion_gui.py").read_text(encoding="utf-8")
    for label in (
        "Path Candidates to AI",
        "Refactoring Folder",
        "Refactoring Folder Path",
        "Clean Refactoring Folder",
    ):
        assert label in gui_text
    assert "build_external_ai_candidate_exchange_box" in completion_text
    assert "Import AI Answer" in gui_text
    assert "new candidate generation only" in gui_text
    assert "never applies AI output to canonical source" in gui_text
    print("AI_EXCHANGE_GUI_CONTROLS_PRESENT: PASS")
    print("AI_EXCHANGE_RETURN_IMPORT_APPEND_ONLY_NO_APPLY: PASS")

    touched = (
        module_root / "external_ai_candidate_exchange_service.py",
        module_root / "external_ai_candidate_exchange_gui.py",
        module_root / "workbench_completion_gui.py",
    )
    for path in touched:
        data = path.read_bytes()
        assert data.isascii(), path
        lines = data.decode("ascii").splitlines()
        assert 101 <= len(lines) <= 499, (path, len(lines))
    print("SOURCE_ASCII_UTF8_NO_BOM: PASS")
    print("MODULE_SIZE_POLICY_101_499: PASS")
    print("EXTERNAL_AI_CANDIDATE_EXCHANGE_OUTBOUND: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")


def _hash_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _hash_tree(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(root).as_posix().encode("utf-8")
        data = path.read_bytes()
        digest.update(relative)
        digest.update(data)
    return digest.hexdigest()


def _clean(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)


if __name__ == "__main__":
    main()
