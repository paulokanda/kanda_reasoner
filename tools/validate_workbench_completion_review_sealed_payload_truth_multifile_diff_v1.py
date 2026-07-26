# project-path: tools/validate_workbench_completion_review_sealed_payload_truth_multifile_diff_v1.py
"""Validate sealed-payload truth and multi-file Completion Review evidence."""
from __future__ import annotations

import hashlib
from pathlib import Path
import sys
from tempfile import TemporaryDirectory

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.visual_diff_ui import (
    build_multi_file_visual_diff_report,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_completion_payload_evidence import (
    plan_size_estimate_warnings,
    sealed_payload_dependency_warnings,
    sealed_payload_import_map,
    sealed_payload_size_map,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_sealed_payload import (
    SealedPayloadFile,
    WorkbenchSealedPayload,
)

FEATURE_ID = "workbench-completion-review-sealed-payload-truth-multifile-diff-v1"
PKG = (
    PROJECT_ROOT
    / "kanda_reasoner_app"
    / "manage_architecture"
    / "large_file_refactor_planner"
)


def _item(relative_path: str, payload_path: Path, destination_path: Path) -> SealedPayloadFile:
    raw = payload_path.read_bytes()
    return SealedPayloadFile(
        relative_path=relative_path,
        payload_path=str(payload_path),
        destination_path=str(destination_path),
        content_hash=hashlib.sha256(raw).hexdigest(),
        byte_size=len(raw),
        physical_lines=len(raw.decode("utf-8").splitlines()),
        role="fixture",
        symbols=(),
    )


def _payload(root: Path) -> tuple[WorkbenchSealedPayload, Path, Path, Path, Path]:
    source = root / "main.py"
    helper_destination = root / "_helper.py"
    sealed_facade = root / "sealed_main.py"
    sealed_helper = root / "sealed_helper.py"
    source.write_text(
        "from __future__ import annotations\n\ndef public():\n    return _private()\n\ndef _private():\n    return 1\n",
        encoding="utf-8",
    )
    sealed_facade.write_text(
        "from __future__ import annotations\nfrom ._helper import _private\n\ndef public():\n    return _private()\n",
        encoding="utf-8",
    )
    sealed_helper.write_text(
        "from typing import TYPE_CHECKING\n"
        "if TYPE_CHECKING:\n"
        "    from .main import PublicType\n\n"
        "def _private():\n"
        "    from .main import public\n"
        "    return 1\n",
        encoding="utf-8",
    )
    payload = WorkbenchSealedPayload(
        schema_version="1.0",
        feature_id="fixture",
        payload_id="fixture",
        contract_hash="fixture-contract",
        recipe_hash="fixture-recipe",
        source_content_hash="fixture-source",
        payload_root=str(root),
        manifest_path=str(root / "manifest.json"),
        transform_backend="fixture",
        files=(
            _item("main.py", sealed_facade, source),
            _item("_helper.py", sealed_helper, helper_destination),
        ),
        blockers=(),
        warnings=(),
        payload_hash="fixture-hash",
        source_mutation_enabled=False,
    )
    return payload, source, helper_destination, sealed_facade, sealed_helper


def _runtime_contract() -> None:
    with TemporaryDirectory() as raw:
        root = Path(raw)
        payload, source, helper_destination, sealed_facade, sealed_helper = _payload(root)
        sizes = sealed_payload_size_map(payload)
        assert dict(sizes)[str(source.resolve())] == len(
            sealed_facade.read_text(encoding="utf-8").splitlines()
        )
        print("SEMANTIC_SIZE_AFTER_FROM_SEALED_PAYLOAD: PASS")

        imports = dict(sealed_payload_import_map(payload))
        helper_imports = imports["_helper.py"]
        assert "type_checking:.main.PublicType" in helper_imports
        assert "deferred:.main.public" in helper_imports
        print("SEMANTIC_IMPORTS_AFTER_FROM_SEALED_BYTES: PASS")
        print("IMPORT_CATEGORY_RUNTIME_TYPECHECKING_DEFERRED: PASS")

        warnings = sealed_payload_dependency_warnings(payload, target_file=source)
        assert any(item.startswith("DEFERRED_FACADE_BACK_REFERENCE:") for item in warnings)
        assert any(item.startswith("TYPE_CHECKING_FACADE_BACK_REFERENCE:") for item in warnings)
        print("DEFERRED_AND_TYPECHECKING_BACK_REFERENCES_VISIBLE: PASS")

        estimate_warnings = plan_size_estimate_warnings(
            {
                str(source): 197,
                str(helper_destination): 452,
            },
            payload,
        )
        assert len(estimate_warnings) == 2
        print("PLAN_ESTIMATE_DIVERGENCE_REPORTED_NOT_USED_AS_TRUTH: PASS")

        report = build_multi_file_visual_diff_report(
            [
                (
                    source.read_text(encoding="utf-8"),
                    sealed_facade.read_text(encoding="utf-8"),
                    str(source),
                    "main.py",
                ),
                (
                    "",
                    sealed_helper.read_text(encoding="utf-8"),
                    str(helper_destination),
                    "_helper.py",
                ),
            ]
        )
        assert report.file_count == 2
        assert len(report.file_summaries) == 2
        assert any(
            item["target_label"] == "_helper.py" and item["created_file"]
            for item in report.file_summaries
        )
        assert any(row.kind == "add" and "def _private" in row.text for row in report.rows)
        print("TEXT_DIFF_COVERS_ALL_SEALED_FILES: PASS")
        print("CREATED_HELPER_FULL_ADD_DIFF_PRESENT: PASS")


def _static_contract() -> None:
    completion = (PKG / "workbench_completion_review.py").read_text(encoding="utf-8")
    assistant = (PKG / "workbench_diff_review_assistant.py").read_text(encoding="utf-8")
    gui = (PKG / "workbench_completion_gui.py").read_text(encoding="utf-8")
    visual = (PKG / "visual_diff_ui.py").read_text(encoding="utf-8")

    assert "after_sizes = sealed_payload_size_map(sealed_payload)" in completion
    assert "imports = sealed_payload_import_map(sealed_payload)" in completion
    assert "build_multi_file_visual_diff_report(comparisons)" in completion
    assert "Resulting sizes (sealed payload truth):" in completion
    assert "Exact sealed imports:" in completion
    assert "Exact local dependency graph:" in completion
    assert "file_summaries" in assistant
    assert "file_count" in assistant
    assert "Files covered:" in gui
    assert "def build_multi_file_visual_diff_report(" in visual
    print("COMPLETION_REVIEW_PRODUCER_USES_SEALED_TRUTH: PASS")
    print("ASSISTED_REVIEW_RECEIVES_MULTI_FILE_COVERAGE: PASS")
    print("GUI_RENDERS_MULTI_FILE_COVERAGE: PASS")


def _size_contract() -> None:
    names = (
        "workbench_completion_payload_evidence.py",
        "workbench_completion_review.py",
        "visual_diff_ui.py",
        "workbench_completion_gui.py",
        "workbench_diff_review_assistant.py",
    )
    for name in names:
        lines = len((PKG / name).read_text(encoding="utf-8").splitlines())
        assert lines < 500, f"TOUCHED_MODULE_SIZE_POLICY_FAILED:{name}:{lines}"
    print("TOUCHED_SOURCE_MODULES_UNDER_500_LINES: PASS")


def run_validation() -> None:
    _runtime_contract()
    _static_contract()
    _size_contract()
    print("WORKBENCH_COMPLETION_REVIEW_SEALED_PAYLOAD_TRUTH_MULTIFILE_DIFF: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")


if __name__ == "__main__":
    run_validation()
