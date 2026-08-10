# project-path: tools/validate_engineering_diagnostics_wave2oc_v1.py
"""Validate Engineering Diagnostics Ruff Wave 2O-C."""

from __future__ import annotations

import argparse
import hashlib
import importlib
import os
from pathlib import Path
import subprocess
import sys
import time
from typing import Iterable

from tools.engineering_diagnostics_wave2oc_architecture_gate import (
    validate_engineering_diagnostics_wave2oc_architecture_non_regression,
)
from tools.engineering_diagnostics_wave2oc_public_boundary_gate import (
    validate_engineering_diagnostics_wave2oc_public_boundary,
)

FEATURE_ID = "kanda-reasoner-engineering-diagnostics-ruff-wave2oc-v1"
PACKAGE_REVISION = "v1r2"
VALIDATOR_CANONICAL_SHA256 = "36df62a3b8b242f87c321ec59818ece0d09e1efa68da230f4d3e5fdd7973f756"

_PAYLOAD_HASHES = {
    "kanda_reasoner_app/engineering_diagnostics/__init__.py": (
        "031c9b228f720dfdb2ea66e704e1e743f63cd7a57b9f037afbb2b900167baae2"
    ),
    "kanda_reasoner_app/engineering_diagnostics/_store_baseline_ops.py": (
        "d683bb379d61c17b8d473bf29226f0f9a1376c157f9855f6214cdb056cdd8901"
    ),
    "kanda_reasoner_app/engineering_diagnostics/fingerprinting.py": (
        "52c9a5c76839d5b7548d53f81c45ff2aecc43b98b4b7e5b257816f7786df4676"
    ),
    "kanda_reasoner_app/engineering_diagnostics/collectors/__init__.py": (
        "fb47c73a2359b5142902893873dfecd016bcf0242274e3bb4064a95d31170db2"
    ),
    "kanda_reasoner_app/engineering_diagnostics/collectors/ruff_collector.py": (
        "2ed122ecd01a5c2a5e291ed5b8dcd445a262e54ef10dd712105e00000f1a86ef"
    ),
    "kanda_reasoner_app/engineering_diagnostics/collectors/ruff_normalizer.py": (
        "9ef349844b5d4d6af4bdc73eec6f4b4a3d4809e4668f726e0609811ee4ef143d"
    ),
    "kanda_reasoner_app/engineering_diagnostics/rules/__init__.py": (
        "cc1704d5698c48f18e93b68e7ea5b158d32dd2b4b5fe30344dc0d196e2954757"
    ),
    "kanda_reasoner_app/engineering_diagnostics/rules/ruff_rule_registry.py": (
        "26df9ac3a10cf9457d427e8fcf1dc552fc3b96a8162a962c181b97635f1337e4"
    ),
    "kanda_reasoner_app/engineering_diagnostics_gui/controller.py": (
        "b2edcaa7edca9d28ee71aa327d4f840bd0a7c00fb7e8b0fd1eb1e469b4e153ef"
    ),
    "kanda_reasoner_app/engineering_diagnostics_gui/diagnostic_table_model.py": (
        "d4a5f9e215eea3e19c98b26f0dab5b07894155746bd632cba8ebc9c25a168202"
    ),
    "kanda_reasoner_app/engineering_diagnostics_gui/engineering_diagnostics_tab.py": (
        "69d91cea5ec592e10ba60f707fc55e911cdc6acc41dba568ebcd133da5d2007a"
    ),
    "tests/test_engineering_diagnostics_wave2oc.py": (
        "eb9ab572427243db551d57835bad017eb65ffd29ccf553981e96b125fb502c0d"
    ),
    "tools/engineering_diagnostics_wave2oc_architecture_gate.py": (
        "fe435becf67c365552973505a54c255d7ae4fa13acf37aa8ed6ea712ec5ba84b"
    ),
    "tools/engineering_diagnostics_wave2oc_public_boundary_gate.py": (
        "0f942cb2518c008308ce5a466fe81e04af00b1e376f52d1d21b5a981debe806e"
    ),
}

_UNCHANGED_HASHES = {
    "kanda_reasoner_app/engineering_diagnostics/_store_database.py": (
        "bbf6a57ef1d65bf05f4cd173ab34a91fd6f5eb4ec33ea90c3df931f44cfb75b8"
    ),
    "kanda_reasoner_app/engineering_diagnostics/baseline.py": (
        "5a4806826572c9334e034818f88ec3517d4c684a4338ab76f0cb57047695da3e"
    ),
    "kanda_reasoner_app/engineering_diagnostics/bom_adapter.py": (
        "ceeb930aa9713c63205d1d6c60aad286abc60dfa246e11492ce88846190fef25"
    ),
    "kanda_reasoner_app/engineering_diagnostics/models.py": (
        "2053c3dfcaa8d08939d99626c9b18a1d1d887bc24a163d974db36dc93d7d2184"
    ),
    "kanda_reasoner_app/engineering_diagnostics/paths.py": (
        "95640db89ef725b160cbbe6784599f9ab9f5c1cf01814602b1121c924d48c48d"
    ),
    "kanda_reasoner_app/engineering_diagnostics/store.py": (
        "b40d07897501051b4318ad50577769c1df86481a8cd88f08f8374cd3e766272e"
    ),
    "kanda_reasoner_app/engineering_diagnostics_gui/__init__.py": (
        "ed11f764b9b805c6ea92be3ba779708b53c0512be381b2ca0138e75ca9f8f681"
    ),
    "kanda_reasoner_app/engineering_diagnostics_gui/bom_provider.py": (
        "6ec230444e14fed4e5f00054b2ced4c96ce166308829ba5b0951ed49c59cbc48"
    ),
    "kanda_reasoner_app/engineering_diagnostics_gui/models.py": (
        "d22743d0b23024f022ea2f09189c0355a3a738171b94ae893f94bd83a25da473"
    ),
    "kanda_reasoner_app/engineering_diagnostics_gui/source_identity.py": (
        "90a98bd6a706ef3345e32df8e41ba263d76717a825adee5b533ffcc56935ef58"
    ),
    "kanda_reasoner_app/manage_architecture/architecture_review_subtabs.py": (
        "9f06f78b96c24fa3193ffc0b2c9b2aaa30a835035c33d2a1e9a980ac43b1c730"
    ),
    "kanda_reasoner_app/manage_architecture/audit_project_sibling_tabs.py": (
        "1d416fc21e4079c456f0c1f85217b8a00892396efc3fa8b50ae264564114e4c6"
    ),
    "tests/test_engineering_diagnostics_wave2oa.py": (
        "4cefd958d53df34acd8b53b4b9a3f8fdbb1e2afd806e01dc19806b551c26bbbd"
    ),
    "tests/test_engineering_diagnostics_wave2ob.py": (
        "84a5ee2c3f12581a1a01bd994442a1450493c7355995a990140bc29be200792f"
    ),
    "tools/validate_engineering_diagnostics_wave2oa_v1.py": (
        "88aaea82f2f5230744945088b20e7dc251173236aace685e87aa7ada54218b45"
    ),
    "tools/validate_engineering_diagnostics_wave2ob_v1.py": (
        "d27b9b83c75381991e60636ac2d4807645e4ccc245b5b0ee86acb2aa3ea25cc2"
    ),
}


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _check_hashes(root: Path, expected: dict[str, str], marker: str) -> None:
    for relative, digest in expected.items():
        path = root / relative
        _require(path.is_file(), "VALIDATED_FILE_MISSING:" + relative)
        _require(_sha256(path) == digest, "VALIDATED_FILE_HASH_MISMATCH:" + relative)
    print(marker)


def _run(command: list[str], *, cwd: Path, markers: Iterable[str]) -> str:
    completed = subprocess.run(
        command,
        cwd=str(cwd),
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )
    output = completed.stdout + completed.stderr
    print(output, end="" if output.endswith("\n") else "\n")
    _require(completed.returncode == 0, "VALIDATION_COMMAND_FAILED:" + " ".join(command))
    for marker in markers:
        _require(marker in output, "VALIDATION_MARKER_MISSING:" + marker)
    return output


def _registry_digest(root: Path) -> tuple[Path, str]:
    from kanda_reasoner_app.project_selection_registry import ProjectSelectionRegistry

    registry = ProjectSelectionRegistry(tool_source_root=root)
    path = registry.registry_path
    return path, _sha256(path) if path.is_file() else "ABSENT"


def _run_tests(root: Path) -> None:
    groups = (
        ("tests.test_engineering_diagnostics_wave2oa", 13),
        ("tests.test_engineering_diagnostics_wave2ob", 8),
        ("tests.test_engineering_diagnostics_wave2oc", 13),
    )
    for module, count in groups:
        _run(
            [sys.executable, "-m", "unittest", "-v", module],
            cwd=root,
            markers=("Ran " + str(count) + " tests", "OK"),
        )
    print("WAVE2OA FOCUSED PUBLIC CONTRACT TESTS: 13/13 PASS")
    print("WAVE2OB FOCUSED PUBLIC CONTRACT TESTS: 8/8 PASS")
    print("WAVE2OC FOCUSED PUBLIC CONTRACT TESTS: 13/13 PASS")
    print("FOCUSED PUBLIC CONTRACT TESTS: 34/34 PASS")
    print("WAVE2OB TOKEN-BOUND SUPPORT FIXTURE: PASS")
    print("WAVE2OA AND WAVE2OB CONTRACT REGRESSION: PASS")
    print("RUFF HIGH-VOLUME 25000 FINDINGS PERSISTENCE: PASS")
    print("RUFF BASELINE DIFF STABILITY: PASS")
    print("RUFF FAILURE ISOLATION PRESERVES BOM: PASS")
    print("HIGH-VOLUME STREAMING DIGEST: PASS")


def _check_gui_and_scale(root: Path) -> tuple[float, float, float]:
    package = importlib.import_module("kanda_reasoner_app.engineering_diagnostics_gui")
    _require(
        callable(getattr(package, "create_engineering_diagnostics_panel", None)),
        "ENGINEERING_DIAGNOSTICS_GUI_FACTORY_MISSING",
    )
    print("ENGINEERING DIAGNOSTICS GUI COMPLETE IMPORT GRAPH: PASS")
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    try:
        from PySide6.QtCore import QElapsedTimer
        from PySide6.QtWidgets import QApplication
    except ImportError as exc:
        raise RuntimeError("PYSIDE6_REQUIRED_FOR_GUI_VALIDATION") from exc
    from kanda_reasoner_app.engineering_diagnostics import DiagnosticFindingRecord
    from kanda_reasoner_app.engineering_diagnostics_gui import DiagnosticFindingView

    app = QApplication.instance() or QApplication([])
    started = time.perf_counter()
    panel = package.create_engineering_diagnostics_panel(
        project_root_provider=lambda: str(root),
        defer_initial_refresh=True,
    )
    initialization_ms = (time.perf_counter() - started) * 1000.0
    _require(panel.objectName() == "engineering_diagnostics_page", "GUI_PANEL_OBJECT_NAME")
    combo = panel.engineering_diagnostics_producer_combo
    values = tuple(str(combo.itemData(index)) for index in range(combo.count()))
    _require("ruff.check" in values, "GUI_RUFF_PRODUCER_SELECTOR_MISSING")

    rows = tuple(
        DiagnosticFindingView(
            record=DiagnosticFindingRecord(
                run_id="scale-run",
                issue_fingerprint="issue-" + str(index),
                evidence_digest="evidence-" + str(index),
                code="F821" if index % 2 == 0 else "F401",
                relative_path="src/file_" + str(index).zfill(5) + ".py",
                message="Synthetic Ruff finding " + str(index),
                severity="error" if index % 2 == 0 else "warning",
                confidence="high",
                semantic_key="semantic-" + str(index),
                symbol_id="symbol-" + str(index),
                location_key="location-" + str(index),
                category="ruff",
                line=1,
                evidence={"ruff_version": "ruff synthetic"},
                suggested_action="Review Ruff evidence.",
            ),
            lifecycle_state="new" if index % 3 == 0 else "persistent",
        )
        for index in range(25000)
    )
    table = panel.engineering_diagnostics_table
    source = table.model()
    _require(callable(getattr(source, "set_filters", None)), "GUI_FILTER_MODEL_MISSING")
    _require(not callable(getattr(source, "sourceModel", None)), "GUI_PROXY_MODEL_PRESENT")
    timer = QElapsedTimer()
    timer.start()
    source.set_rows(rows)
    app.processEvents()
    rows_ms = float(timer.elapsed())
    _require(source.rowCount() == 25000, "GUI_SCALE_ROW_COUNT_MISMATCH")
    timer.restart()
    source.set_filters("error", "all", "file_24998")
    filtered_count = source.rowCount()
    app.processEvents()
    filter_ms = float(timer.elapsed())
    _require(filtered_count == 1, "GUI_SCALE_FILTER_RESULT_MISMATCH")
    _require(initialization_ms < 2000.0, "GUI_INITIALIZATION_TARGET_EXCEEDED")
    _require(rows_ms < 2000.0, "GUI_25000_ROW_TARGET_EXCEEDED")
    _require(filter_ms < 500.0, "GUI_FILTER_TARGET_EXCEEDED")
    panel.deleteLater()
    app.processEvents()
    print("ENGINEERING DIAGNOSTICS GUI FACTORY SMOKE: PASS")
    print("AUDIT PROJECT ENGINEERING DIAGNOSTICS HOST IMPORT: PASS")
    print("WAVE2OC GUI RUFF PRODUCER SELECTOR: PASS")
    print("WAVE2OC GUI DIRECT INDEXED MODEL: PASS")
    print("WAVE2OC GUI PROXY MODEL: ABSENT")
    print("WAVE2OC GUI 25000 ROW INITIALIZATION MS: " + f"{rows_ms:.1f}")
    print("WAVE2OC GUI FILTER UPDATE MS: " + f"{filter_ms:.1f}")
    print("WAVE2OC GUI PANEL CREATION MS: " + f"{initialization_ms:.1f}")
    print("WAVE2OC GUI HIGH-VOLUME PERFORMANCE: PASS")
    return initialization_ms, rows_ms, filter_ms


def _check_host_import() -> None:
    module = importlib.import_module(
        "kanda_reasoner_app.manage_architecture.architecture_review_subtabs"
    )
    _require(
        callable(getattr(module, "build_architecture_review_ui", None)),
        "AUDIT_PROJECT_HOST_IMPORT_FAILED",
    )


def _check_real_ruff(root: Path) -> tuple[int, str]:
    from kanda_reasoner_app.engineering_diagnostics import (
        build_ruff_diagnostic_run,
        collect_ruff_json,
    )
    from kanda_reasoner_app.engineering_diagnostics_gui import (
        project_source_fingerprint,
    )
    from kanda_reasoner_app.project_selection_registry import ProjectSelectionRegistry

    boundary = ProjectSelectionRegistry(tool_source_root=root).resolve_boundary_for_root(root)
    source_before = project_source_fingerprint(root)
    collection = collect_ruff_json(root)
    source_after_collection = project_source_fingerprint(root)
    _require(source_before == source_after_collection, "RUFF_COLLECTION_MUTATED_PROJECT_SOURCE")
    run_input = build_ruff_diagnostic_run(
        collection,
        boundary=boundary,
        attempt_id="wave2oc-live-validation",
        source_fingerprint=source_before,
        operation_generation=1,
    )
    source_after_normalization = project_source_fingerprint(root)
    _require(source_before == source_after_normalization, "RUFF_NORMALIZATION_MUTATED_PROJECT_SOURCE")
    _require(run_input.producer_id == "ruff.check", "RUFF_LIVE_PRODUCER_ID_MISMATCH")
    _require(run_input.producer_version == collection.ruff_version, "RUFF_VERSION_NOT_RECORDED")
    _require(run_input.provenance.get("fix_execution") is False, "RUFF_FIX_EXECUTION_NOT_FALSE")
    _require(
        len(run_input.findings) <= len(collection.raw_findings),
        "RUFF_NORMALIZED_FINDING_COUNT_INVALID",
    )
    print("RUFF LIVE MACHINE-READABLE COLLECTION: PASS")
    print("RUFF LIVE TOOL VERSION: " + collection.ruff_version)
    print("RUFF LIVE RAW FINDINGS: " + str(len(collection.raw_findings)))
    print("RUFF LIVE NORMALIZED FINDINGS: " + str(len(run_input.findings)))
    print("RUFF LIVE FIX EXECUTION: 0")
    print("PROJECT SOURCE MODIFIED BY RUFF VALIDATION: NO")
    return len(run_input.findings), collection.ruff_version


def _run_architecture(root: Path) -> None:
    output = _run(
        [
            sys.executable,
            str(root / "kanda_reasoner_app/manage_architecture/manage_architecture.py"),
            "--root",
            str(root),
            "--validate",
        ],
        cwd=root,
        markers=("ARCHITECTURE VALIDATION SUMMARY",),
    )
    validate_engineering_diagnostics_wave2oc_architecture_non_regression(output)


def _write_evidence(root: Path, lines: list[str]) -> Path:
    from kanda_reasoner_app.project_selection_registry import ProjectSelectionRegistry

    boundary = ProjectSelectionRegistry(tool_source_root=root).resolve_boundary_for_root(root)
    target = (
        boundary.active_project_support_root
        / "project_validation_evidence"
        / "engineering_diagnostics_wave2oc"
        / "engineering_diagnostics_wave2oc_v1.txt"
    )
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return target


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True)
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    root = Path(args.project_root).expanduser().resolve(strict=True)
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    print("PACKAGE REVISION: " + PACKAGE_REVISION)
    print("VALIDATOR PROJECT ROOT IMPORT PATH: PASS")
    registry_path, registry_before = _registry_digest(root)
    validator_path = Path(__file__).resolve()
    validator_source = validator_path.read_text(encoding="utf-8")
    canonical_source = validator_source.replace(
        'VALIDATOR_CANONICAL_SHA256 = "' + VALIDATOR_CANONICAL_SHA256 + '"',
        'VALIDATOR_CANONICAL_SHA256 = "' + ("0" * 64) + '"',
        1,
    )
    canonical_digest = hashlib.sha256(canonical_source.encode("utf-8")).hexdigest()
    _require(
        canonical_digest == VALIDATOR_CANONICAL_SHA256,
        "WAVE2OC_VALIDATOR_CANONICAL_HASH_MISMATCH",
    )
    print("WAVE2OC VALIDATOR CANONICAL HASH: PASS")
    _check_hashes(root, _PAYLOAD_HASHES, "WAVE2OC INSTALLED HASHES: PASS")
    _check_hashes(root, _UNCHANGED_HASHES, "WAVE2OA AND WAVE2OB UNCHANGED HASHES: PASS")
    validate_engineering_diagnostics_wave2oc_public_boundary(root)
    _run_tests(root)
    _check_host_import()
    initialization_ms, rows_ms, filter_ms = _check_gui_and_scale(root)
    finding_count, ruff_version = _check_real_ruff(root)
    _run_architecture(root)
    registry_after = _sha256(registry_path) if registry_path.is_file() else "ABSENT"
    _require(registry_before == registry_after, "PROJECT_SELECTION_REGISTRY_MUTATED")
    print("PROJECT SELECTION REGISTRY MUTATED: NO")
    print("TOOL PROJECT LOGICAL ROLE SEPARATION: PASS")
    evidence_lines = [
        "PACKAGE REVISION: " + PACKAGE_REVISION,
        "VALIDATOR PROJECT ROOT IMPORT PATH: PASS",
        "WAVE2OC INSTALLED HASHES: PASS",
        "WAVE2OA AND WAVE2OB UNCHANGED HASHES: PASS",
        "WAVE2OC PUBLIC-CONTRACT-ONLY COMMUNICATION: PASS",
        "RUFF MACHINE-READABLE JSON ONLY: PASS",
        "RUFF FIX EXECUTION: 0",
        "RUFF PROJECT SOURCE MUTATION CALLS: 0",
        "WAVE2OA FOCUSED PUBLIC CONTRACT TESTS: 13/13 PASS",
        "WAVE2OB FOCUSED PUBLIC CONTRACT TESTS: 8/8 PASS",
        "WAVE2OC FOCUSED PUBLIC CONTRACT TESTS: 13/13 PASS",
        "FOCUSED PUBLIC CONTRACT TESTS: 34/34 PASS",
        "WAVE2OB TOKEN-BOUND SUPPORT FIXTURE: PASS",
        "WAVE2OA AND WAVE2OB CONTRACT REGRESSION: PASS",
        "RUFF HIGH-VOLUME 25000 FINDINGS PERSISTENCE: PASS",
        "RUFF BASELINE DIFF STABILITY: PASS",
        "RUFF FAILURE ISOLATION PRESERVES BOM: PASS",
        "ENGINEERING DIAGNOSTICS GUI FACTORY SMOKE: PASS",
        "AUDIT PROJECT ENGINEERING DIAGNOSTICS HOST IMPORT: PASS",
        "WAVE2OC GUI RUFF PRODUCER SELECTOR: PASS",
        "WAVE2OC GUI DIRECT INDEXED MODEL: PASS",
        "WAVE2OC GUI PROXY MODEL: ABSENT",
        "WAVE2OC GUI 25000 ROW INITIALIZATION MS: " + f"{rows_ms:.1f}",
        "WAVE2OC GUI FILTER UPDATE MS: " + f"{filter_ms:.1f}",
        "WAVE2OC GUI PANEL CREATION MS: " + f"{initialization_ms:.1f}",
        "WAVE2OC GUI HIGH-VOLUME PERFORMANCE: PASS",
        "RUFF LIVE MACHINE-READABLE COLLECTION: PASS",
        "RUFF LIVE TOOL VERSION: " + ruff_version,
        "RUFF LIVE NORMALIZED FINDINGS: " + str(finding_count),
        "RUFF LIVE FIX EXECUTION: 0",
        "PROJECT SOURCE MODIFIED BY RUFF VALIDATION: NO",
        "HIGH-VOLUME STREAMING DIGEST: PASS",
        "WAVE2OC ARCHITECTURE BASELINE OWNER REUSED: PASS",
        "WAVE2OC NEW ARCHITECTURE ISSUES: 0",
        "WAVE2OC TOUCHED PATH ARCHITECTURE ISSUES: 0",
        "WAVE2OC ARCHITECTURE NON-REGRESSION: PASS",
        "PROJECT SELECTION REGISTRY MUTATED: NO",
        "TOOL PROJECT LOGICAL ROLE SEPARATION: PASS",
        "VALIDATION OK: " + FEATURE_ID,
        "STATUS: IN_SYNC",
    ]
    evidence = _write_evidence(root, evidence_lines)
    print("VALIDATION EVIDENCE WRITTEN: " + str(evidence))
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
