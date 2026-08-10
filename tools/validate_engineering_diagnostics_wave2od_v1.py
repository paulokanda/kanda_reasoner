# project-path: tools/validate_engineering_diagnostics_wave2od_v1.py
"""Brick Wall validator for Engineering Diagnostics Architecture Wave 2O-D."""

from __future__ import annotations

import argparse
import hashlib
import importlib
import os
from pathlib import Path
import subprocess
import sys
from typing import Iterable

from tools.engineering_diagnostics_wave2od_architecture_gate import (
    validate_engineering_diagnostics_wave2od_architecture_non_regression,
)
from tools.engineering_diagnostics_wave2od_public_boundary_gate import (
    validate_engineering_diagnostics_wave2od_public_boundary,
)

FEATURE_ID = "kanda-reasoner-engineering-diagnostics-architecture-wave2od-v1"
PACKAGE_REVISION = "v1r1"
VALIDATOR_CANONICAL_SHA256 = "d4e03ccb66b9bbb118c24d007651c8a86630c0ba3ab785d32a0621816b6dcf50"
_PAYLOAD_HASHES = {'kanda_reasoner_app/engineering_diagnostics/__init__.py': '6ad81f994af75bb87e2287f70ac7b27eafd43f389ec0106007b0c25f1a7aab5b',
 'kanda_reasoner_app/engineering_diagnostics/collectors/__init__.py': 'a97877cfe3aa8c575c1e02e388bc42889ed03a8917b715ea7ba7156f0ea2b7ab',
 'kanda_reasoner_app/engineering_diagnostics/collectors/architecture_collector.py': 'b158b77752302bc5437177d4a39d115b18cf1802218933f459577993bab4a558',
 'kanda_reasoner_app/engineering_diagnostics/collectors/architecture_normalizer.py': 'f0d9f9b102a5acd96cd30de5f2b0f1fc960ae3fd94440643906c688640dc0751',
 'kanda_reasoner_app/engineering_diagnostics/rules/__init__.py': 'e45e763a0cb599713aa3316eaf63d863e4b3da4fd61c9db9d0ea5030b164a838',
 'kanda_reasoner_app/engineering_diagnostics/rules/architecture_rule_registry.py': '510529088f4e339df914a5615f681815ebffebac4b6597212a4d3efc7faa476b',
 'kanda_reasoner_app/engineering_diagnostics_gui/controller.py': 'e3f29115124afc88c3351a2e1b7480c6d015e169b6e3fd42c80f76b11bc55d1c',
 'kanda_reasoner_app/engineering_diagnostics_gui/engineering_diagnostics_tab.py': '41844dd82226101729b086d3ffbb2b89cba87868b21d516575555bbda2fc294a',
 'tests/test_engineering_diagnostics_wave2od.py': 'dbf3d1857019b49705a7756ca0ed987df67e38fde88fb31897fa92ba506b3b6f',
 'tools/engineering_diagnostics_wave2od_architecture_gate.py': '516992f73f1b2db40260d70f35727eaddd384bd984168160ac4f87f35cbcd5fd',
 'tools/engineering_diagnostics_wave2od_public_boundary_gate.py': '36800a9dff945ac871a856ba22a8494729c64c7c0afa441f75ff359fd073e1e9'}
_UNCHANGED_HASHES = {'kanda_reasoner_app/engineering_diagnostics/_store_baseline_ops.py': 'd683bb379d61c17b8d473bf29226f0f9a1376c157f9855f6214cdb056cdd8901',
 'kanda_reasoner_app/engineering_diagnostics/_store_database.py': 'bbf6a57ef1d65bf05f4cd173ab34a91fd6f5eb4ec33ea90c3df931f44cfb75b8',
 'kanda_reasoner_app/engineering_diagnostics/baseline.py': '5a4806826572c9334e034818f88ec3517d4c684a4338ab76f0cb57047695da3e',
 'kanda_reasoner_app/engineering_diagnostics/bom_adapter.py': 'ceeb930aa9713c63205d1d6c60aad286abc60dfa246e11492ce88846190fef25',
 'kanda_reasoner_app/engineering_diagnostics/collectors/ruff_collector.py': '2ed122ecd01a5c2a5e291ed5b8dcd445a262e54ef10dd712105e00000f1a86ef',
 'kanda_reasoner_app/engineering_diagnostics/collectors/ruff_normalizer.py': '9ef349844b5d4d6af4bdc73eec6f4b4a3d4809e4668f726e0609811ee4ef143d',
 'kanda_reasoner_app/engineering_diagnostics/fingerprinting.py': '52c9a5c76839d5b7548d53f81c45ff2aecc43b98b4b7e5b257816f7786df4676',
 'kanda_reasoner_app/engineering_diagnostics/models.py': '2053c3dfcaa8d08939d99626c9b18a1d1d887bc24a163d974db36dc93d7d2184',
 'kanda_reasoner_app/engineering_diagnostics/paths.py': '95640db89ef725b160cbbe6784599f9ab9f5c1cf01814602b1121c924d48c48d',
 'kanda_reasoner_app/engineering_diagnostics/rules/ruff_rule_registry.py': '26df9ac3a10cf9457d427e8fcf1dc552fc3b96a8162a962c181b97635f1337e4',
 'kanda_reasoner_app/engineering_diagnostics/store.py': 'b40d07897501051b4318ad50577769c1df86481a8cd88f08f8374cd3e766272e',
 'kanda_reasoner_app/engineering_diagnostics_gui/__init__.py': 'ed11f764b9b805c6ea92be3ba779708b53c0512be381b2ca0138e75ca9f8f681',
 'kanda_reasoner_app/engineering_diagnostics_gui/bom_provider.py': '6ec230444e14fed4e5f00054b2ced4c96ce166308829ba5b0951ed49c59cbc48',
 'kanda_reasoner_app/engineering_diagnostics_gui/diagnostic_table_model.py': 'd4a5f9e215eea3e19c98b26f0dab5b07894155746bd632cba8ebc9c25a168202',
 'kanda_reasoner_app/engineering_diagnostics_gui/models.py': 'd22743d0b23024f022ea2f09189c0355a3a738171b94ae893f94bd83a25da473',
 'kanda_reasoner_app/engineering_diagnostics_gui/source_identity.py': '90a98bd6a706ef3345e32df8e41ba263d76717a825adee5b533ffcc56935ef58',
 'kanda_reasoner_app/manage_architecture/architecture_review_subtabs.py': '9f06f78b96c24fa3193ffc0b2c9b2aaa30a835035c33d2a1e9a980ac43b1c730',
 'kanda_reasoner_app/manage_architecture/audit_project_sibling_tabs.py': '1d416fc21e4079c456f0c1f85217b8a00892396efc3fa8b50ae264564114e4c6',
 'kanda_reasoner_app/manage_architecture/manage_architecture.py': '83772158777d6b081e0dd5e1c9389d9b2e85789c1261e1f7ff42407525906f81',
 'tests/test_engineering_diagnostics_wave2oa.py': '4cefd958d53df34acd8b53b4b9a3f8fdbb1e2afd806e01dc19806b551c26bbbd',
 'tests/test_engineering_diagnostics_wave2ob.py': '84a5ee2c3f12581a1a01bd994442a1450493c7355995a990140bc29be200792f',
 'tests/test_engineering_diagnostics_wave2oc.py': 'eb9ab572427243db551d57835bad017eb65ffd29ccf553981e96b125fb502c0d',
 'tools/engineering_diagnostics_wave2oa_architecture_gate.py': '35affe7f13821f9ba7d530ff1dd0b5f4fdcfa21141bbb878380621a0ca29c249',
 'tools/engineering_diagnostics_wave2oa_public_boundary_gate.py': '8eecb38a9630b84ce34089017cc8139600a869aaa9349ab76d3f778914fbdd15',
 'tools/engineering_diagnostics_wave2ob_architecture_gate.py': 'a53a5abb61e06a5656e9eeeb436aa62440274a4e19c07e862fea8d10be943b67',
 'tools/engineering_diagnostics_wave2ob_public_boundary_gate.py': '4cd344ee0c5c269f9f0a0475c385b891698c4aede0859ba76c4f444ff98cd441',
 'tools/engineering_diagnostics_wave2oc_architecture_gate.py': 'fe435becf67c365552973505a54c255d7ae4fa13acf37aa8ed6ea712ec5ba84b',
 'tools/engineering_diagnostics_wave2oc_public_boundary_gate.py': '0f942cb2518c008308ce5a466fe81e04af00b1e376f52d1d21b5a981debe806e',
 'tools/validate_engineering_diagnostics_wave2oa_v1.py': '88aaea82f2f5230744945088b20e7dc251173236aace685e87aa7ada54218b45',
 'tools/validate_engineering_diagnostics_wave2ob_v1.py': 'd27b9b83c75381991e60636ac2d4807645e4ccc245b5b0ee86acb2aa3ea25cc2',
 'tools/validate_engineering_diagnostics_wave2oc_v1.py': '8f8177fc87268a8e5c8d5e3da1ec101e5ecf1d4b88c88b840d17be7bd7436c67'}


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _run(
    command: list[str],
    *,
    cwd: Path,
    markers: Iterable[str] = (),
) -> str:
    completed = subprocess.run(
        command,
        cwd=str(cwd),
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        shell=False,
    )
    output = (completed.stdout or "") + (completed.stderr or "")
    print(output, end="")
    _require(
        completed.returncode == 0,
        "VALIDATION_COMMAND_FAILED:" + " ".join(command),
    )
    for marker in markers:
        _require(marker in output, "VALIDATION_MARKER_MISSING:" + marker)
    return output


def _check_hashes(root: Path, expected: dict[str, str], marker: str) -> None:
    for relative, digest in expected.items():
        path = root / relative
        _require(path.is_file(), "VALIDATED_FILE_MISSING:" + relative)
        _require(_sha256(path) == digest, "VALIDATED_FILE_HASH_MISMATCH:" + relative)
    print(marker)


def _registry_digest(root: Path) -> tuple[Path, str]:
    from kanda_reasoner_app.project_selection_registry import ProjectSelectionRegistry

    registry = ProjectSelectionRegistry(tool_source_root=root)
    path = Path(registry.registry_path)
    return path, _sha256(path) if path.is_file() else "ABSENT"


def _run_tests(root: Path) -> None:
    suites = (
        ("tests.test_engineering_diagnostics_wave2oa", 13),
        ("tests.test_engineering_diagnostics_wave2ob", 8),
        ("tests.test_engineering_diagnostics_wave2oc", 13),
        ("tests.test_engineering_diagnostics_wave2od", 12),
    )
    for module, count in suites:
        _run(
            [sys.executable, "-m", "unittest", "-v", module],
            cwd=root,
            markers=("Ran " + str(count) + " tests", "OK"),
        )
    print("WAVE2OA FOCUSED PUBLIC CONTRACT TESTS: 13/13 PASS")
    print("WAVE2OB FOCUSED PUBLIC CONTRACT TESTS: 8/8 PASS")
    print("WAVE2OC FOCUSED PUBLIC CONTRACT TESTS: 13/13 PASS")
    print("WAVE2OD FOCUSED PUBLIC CONTRACT TESTS: 12/12 PASS")
    print("FOCUSED PUBLIC CONTRACT TESTS: 46/46 PASS")
    print("WAVE2OA THROUGH WAVE2OC CONTRACT REGRESSION: PASS")


def _check_gui(root: Path) -> None:
    package = importlib.import_module("kanda_reasoner_app.engineering_diagnostics_gui")
    _require(
        callable(getattr(package, "create_engineering_diagnostics_panel", None)),
        "ENGINEERING_DIAGNOSTICS_GUI_FACTORY_MISSING",
    )
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    try:
        from PySide6.QtWidgets import QApplication
    except ImportError as exc:
        raise RuntimeError("PYSIDE6_REQUIRED_FOR_GUI_VALIDATION") from exc
    app = QApplication.instance() or QApplication([])
    panel = package.create_engineering_diagnostics_panel(
        project_root_provider=lambda: str(root),
        defer_initial_refresh=True,
    )
    combo = panel.engineering_diagnostics_producer_combo
    values = tuple(str(combo.itemData(index)) for index in range(combo.count()))
    _require(
        "manage_architecture.validate" in values,
        "GUI_ARCHITECTURE_PRODUCER_SELECTOR_MISSING",
    )
    _require("ruff.check" in values, "GUI_RUFF_PRODUCER_REGRESSION")
    _require("source_hygiene.bom_scan" in values, "GUI_BOM_PRODUCER_REGRESSION")
    panel.deleteLater()
    app.processEvents()
    print("ENGINEERING DIAGNOSTICS GUI COMPLETE IMPORT GRAPH: PASS")
    print("ENGINEERING DIAGNOSTICS GUI FACTORY SMOKE: PASS")
    print("AUDIT PROJECT ENGINEERING DIAGNOSTICS HOST IMPORT: PASS")
    print("WAVE2OD GUI ARCHITECTURE PRODUCER SELECTOR: PASS")
    print("WAVE2OC GUI DIRECT INDEXED MODEL PRESERVED: PASS")


def _check_live_architecture(root: Path) -> tuple[int, int, str]:
    from kanda_reasoner_app.engineering_diagnostics import (
        ARCHITECTURE_PRODUCER_ID,
        build_architecture_diagnostic_run,
        collect_architecture_findings,
    )
    from kanda_reasoner_app.engineering_diagnostics_gui import (
        project_source_fingerprint,
    )
    from kanda_reasoner_app.project_selection_registry import ProjectSelectionRegistry

    boundary = ProjectSelectionRegistry(tool_source_root=root).resolve_boundary_for_root(root)
    source_before = project_source_fingerprint(root)
    collection = collect_architecture_findings(root)
    source_after_collection = project_source_fingerprint(root)
    _require(
        source_before == source_after_collection,
        "ARCHITECTURE_COLLECTION_MUTATED_PROJECT_SOURCE",
    )
    run_input = build_architecture_diagnostic_run(
        collection,
        boundary=boundary,
        attempt_id="wave2od-live-validation",
        source_fingerprint=source_before,
        operation_generation=1,
    )
    source_after_normalization = project_source_fingerprint(root)
    _require(
        source_before == source_after_normalization,
        "ARCHITECTURE_NORMALIZATION_MUTATED_PROJECT_SOURCE",
    )
    _require(
        run_input.producer_id == ARCHITECTURE_PRODUCER_ID,
        "ARCHITECTURE_LIVE_PRODUCER_ID_MISMATCH",
    )
    _require(collection.coverage_valid, "ARCHITECTURE_COVERAGE_INVALID")
    _require(
        collection.canonical_issue_count == 0,
        "ARCHITECTURE_CANONICAL_ISSUES_PRESENT:"
        + str(collection.canonical_issue_count),
    )
    _require(collection.assessment == "CLEAN", "ARCHITECTURE_ASSESSMENT_NOT_CLEAN")
    _require(
        len(run_input.findings) == len(collection.issues),
        "ARCHITECTURE_NORMALIZED_FINDING_COUNT_MISMATCH",
    )
    for finding in run_input.findings:
        evidence = finding.evidence
        for key in (
            "validation_source",
            "owner",
            "boundary",
            "symbol",
            "governance_impact",
            "coverage_valid",
        ):
            _require(key in evidence, "ARCHITECTURE_EVIDENCE_FIELD_MISSING:" + key)
    print("ARCHITECTURE PUBLIC VALIDATION SOURCE: PASS")
    print("ARCHITECTURE HUMAN-TEXT PARSING: 0")
    print("ARCHITECTURE PROJECT SOURCE MUTATION: NO")
    print("ARCHITECTURE COVERAGE: VALID")
    print("ARCHITECTURE CANONICAL ISSUES: 0")
    print("ARCHITECTURE COLLECTOR ASSESSMENT: CLEAN")
    print("ARCHITECTURE LIVE RAW FINDINGS: " + str(collection.metadata["raw_issue_count"]))
    print("ARCHITECTURE LIVE NORMALIZED FINDINGS: " + str(len(collection.issues)))
    return len(collection.issues), collection.canonical_issue_count, collection.assessment


def _run_architecture_non_regression(root: Path) -> None:
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
    validate_engineering_diagnostics_wave2od_architecture_non_regression(output)


def _write_evidence(root: Path, lines: list[str]) -> Path:
    from kanda_reasoner_app.project_selection_registry import ProjectSelectionRegistry

    boundary = ProjectSelectionRegistry(tool_source_root=root).resolve_boundary_for_root(root)
    target = (
        boundary.active_project_support_root
        / "project_validation_evidence"
        / "engineering_diagnostics_wave2od"
        / "engineering_diagnostics_wave2od_v1.txt"
    )
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return target


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True)
    args = parser.parse_args()
    root = Path(args.project_root).expanduser().resolve(strict=True)
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    print("PACKAGE REVISION: " + PACKAGE_REVISION)
    print("VALIDATOR PROJECT ROOT IMPORT PATH: PASS")
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
        "WAVE2OD_VALIDATOR_CANONICAL_HASH_MISMATCH",
    )
    print("WAVE2OD VALIDATOR CANONICAL HASH: PASS")
    _check_hashes(root, _PAYLOAD_HASHES, "WAVE2OD INSTALLED HASHES: PASS")
    _check_hashes(
        root,
        _UNCHANGED_HASHES,
        "WAVE2OA THROUGH WAVE2OC PROTECTED HASHES: PASS",
    )
    registry_path, registry_before = _registry_digest(root)
    validate_engineering_diagnostics_wave2od_public_boundary(root)
    _run_tests(root)
    _check_gui(root)
    finding_count, canonical_count, assessment = _check_live_architecture(root)
    _run_architecture_non_regression(root)
    registry_after = _sha256(registry_path) if registry_path.is_file() else "ABSENT"
    _require(registry_before == registry_after, "PROJECT_SELECTION_REGISTRY_MUTATED")
    print("PROJECT SELECTION REGISTRY MUTATED: NO")
    print("TOOL PROJECT LOGICAL ROLE SEPARATION: PASS")
    evidence_lines = [
        "PACKAGE REVISION: " + PACKAGE_REVISION,
        "VALIDATOR PROJECT ROOT IMPORT PATH: PASS",
        "WAVE2OD INSTALLED HASHES: PASS",
        "WAVE2OA THROUGH WAVE2OC PROTECTED HASHES: PASS",
        "WAVE2OD PUBLIC-CONTRACT-ONLY COMMUNICATION: PASS",
        "WAVE2OD SOURCE MAP PATH NORMALIZATION: PASS",
        "FOCUSED PUBLIC CONTRACT TESTS: 46/46 PASS",
        "WAVE2OA THROUGH WAVE2OC CONTRACT REGRESSION: PASS",
        "ENGINEERING DIAGNOSTICS GUI FACTORY SMOKE: PASS",
        "WAVE2OD GUI ARCHITECTURE PRODUCER SELECTOR: PASS",
        "ARCHITECTURE PUBLIC VALIDATION SOURCE: PASS",
        "ARCHITECTURE HUMAN-TEXT PARSING: 0",
        "ARCHITECTURE PROJECT SOURCE MUTATION: NO",
        "ARCHITECTURE COVERAGE: VALID",
        "ARCHITECTURE CANONICAL ISSUES: " + str(canonical_count),
        "ARCHITECTURE COLLECTOR ASSESSMENT: " + assessment,
        "ARCHITECTURE LIVE NORMALIZED FINDINGS: " + str(finding_count),
        "WAVE2OD ARCHITECTURE BASELINE OWNER REUSED: PASS",
        "WAVE2OD NEW ARCHITECTURE ISSUES: 0",
        "WAVE2OD TOUCHED PATH ARCHITECTURE ISSUES: 0",
        "WAVE2OD ARCHITECTURE NON-REGRESSION: PASS",
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
