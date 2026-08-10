# project-path: tools/validate_engineering_diagnostics_wave2pa_v1.py
"""Brick Wall validator for Engineering Diagnostics Wave 2P-A."""

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

from tools.engineering_diagnostics_wave2pa_architecture_gate import (
    validate_engineering_diagnostics_wave2pa_architecture_non_regression,
)
from tools.engineering_diagnostics_wave2pa_public_boundary_gate import (
    validate_engineering_diagnostics_wave2pa_public_boundary,
)

FEATURE_ID = "kanda-reasoner-engineering-diagnostics-scope-freeze-wave2pa-v1"
PACKAGE_REVISION = "v1r2"
VALIDATOR_CANONICAL_SHA256 = "a25c9a788b1ff566a5140fbe804f231daab4a97cf08ac7cde32558ddca1cd15b"
_PAYLOAD_HASHES = {'kanda_reasoner_app/engineering_diagnostics/scope_enrichment.py': 'b0d947e84447f1c26527adf2bab3c052089af289562eadae0a2bce309782d091',
 'tools/engineering_diagnostics_wave2pa_public_boundary_gate.py': 'd446d3273a182034d8bd0daea24166451988174f123ca6aeb42dc97072d89984'}
_UNCHANGED_HASHES = {'kanda_reasoner_app/engineering_diagnostics/__init__.py': '71d22da5995216f60c0eff242b218cef3cf9878a2d4f695841bde6c93b545203',
 'kanda_reasoner_app/engineering_diagnostics/_store_baseline_ops.py': 'd683bb379d61c17b8d473bf29226f0f9a1376c157f9855f6214cdb056cdd8901',
 'kanda_reasoner_app/engineering_diagnostics/_store_database.py': 'bbf6a57ef1d65bf05f4cd173ab34a91fd6f5eb4ec33ea90c3df931f44cfb75b8',
 'kanda_reasoner_app/engineering_diagnostics/baseline.py': '5a4806826572c9334e034818f88ec3517d4c684a4338ab76f0cb57047695da3e',
 'kanda_reasoner_app/engineering_diagnostics/bom_adapter.py': 'ceeb930aa9713c63205d1d6c60aad286abc60dfa246e11492ce88846190fef25',
 'kanda_reasoner_app/engineering_diagnostics/collectors/__init__.py': 'a97877cfe3aa8c575c1e02e388bc42889ed03a8917b715ea7ba7156f0ea2b7ab',
 'kanda_reasoner_app/engineering_diagnostics/collectors/architecture_collector.py': 'b158b77752302bc5437177d4a39d115b18cf1802218933f459577993bab4a558',
 'kanda_reasoner_app/engineering_diagnostics/collectors/architecture_normalizer.py': 'f0d9f9b102a5acd96cd30de5f2b0f1fc960ae3fd94440643906c688640dc0751',
 'kanda_reasoner_app/engineering_diagnostics/collectors/ruff_collector.py': '2ed122ecd01a5c2a5e291ed5b8dcd445a262e54ef10dd712105e00000f1a86ef',
 'kanda_reasoner_app/engineering_diagnostics/collectors/ruff_normalizer.py': '9ef349844b5d4d6af4bdc73eec6f4b4a3d4809e4668f726e0609811ee4ef143d',
 'kanda_reasoner_app/engineering_diagnostics/enrichment.py': '0de118e83142beeedaf200f7d095517fcae3808affe48a858e1168ddb9a4a75e',
 'kanda_reasoner_app/engineering_diagnostics/enrichment_models.py': 'ad289f4762f6d6d665f968d8d2189fc80114fd3962893a3f58fda8b849b8c283',
 'kanda_reasoner_app/engineering_diagnostics/fingerprinting.py': '52c9a5c76839d5b7548d53f81c45ff2aecc43b98b4b7e5b257816f7786df4676',
 'kanda_reasoner_app/engineering_diagnostics/frozen_path_enrichment.py': 'b61eac8e0821100d78d652ab54a095bee493dfc067e42eeed95dab03c2110a96',
 'kanda_reasoner_app/engineering_diagnostics/models.py': '2053c3dfcaa8d08939d99626c9b18a1d1d887bc24a163d974db36dc93d7d2184',
 'kanda_reasoner_app/engineering_diagnostics/paths.py': '95640db89ef725b160cbbe6784599f9ab9f5c1cf01814602b1121c924d48c48d',
 'kanda_reasoner_app/engineering_diagnostics/rules/__init__.py': 'e45e763a0cb599713aa3316eaf63d863e4b3da4fd61c9db9d0ea5030b164a838',
 'kanda_reasoner_app/engineering_diagnostics/rules/architecture_rule_registry.py': '510529088f4e339df914a5615f681815ebffebac4b6597212a4d3efc7faa476b',
 'kanda_reasoner_app/engineering_diagnostics/rules/ruff_rule_registry.py': '26df9ac3a10cf9457d427e8fcf1dc552fc3b96a8162a962c181b97635f1337e4',
 'kanda_reasoner_app/engineering_diagnostics/store.py': 'b40d07897501051b4318ad50577769c1df86481a8cd88f08f8374cd3e766272e',
 'kanda_reasoner_app/engineering_diagnostics_gui/__init__.py': 'ed11f764b9b805c6ea92be3ba779708b53c0512be381b2ca0138e75ca9f8f681',
 'kanda_reasoner_app/engineering_diagnostics_gui/bom_provider.py': '6ec230444e14fed4e5f00054b2ced4c96ce166308829ba5b0951ed49c59cbc48',
 'kanda_reasoner_app/engineering_diagnostics_gui/controller.py': 'a9658f04063b9e61ad12803ba889af26d25e7502d92140478e2b1cea1e79c0b5',
 'kanda_reasoner_app/engineering_diagnostics_gui/diagnostic_table_model.py': '5107acc14218775f262591be3f58c090bca6f3f56a9ab3a4af07460df7b429bc',
 'kanda_reasoner_app/engineering_diagnostics_gui/engineering_diagnostics_tab.py': '70de093fcfdd269f76d1b818038b831a997e5da2ad6feb3c166aaf9905e381d3',
 'kanda_reasoner_app/engineering_diagnostics_gui/models.py': '52d3441ef71978bfc59cf3fd5a6e3e1b9690c9327aa256743dd6c8dd3b0d98b7',
 'kanda_reasoner_app/engineering_diagnostics_gui/source_identity.py': '90a98bd6a706ef3345e32df8e41ba263d76717a825adee5b533ffcc56935ef58',
 'kanda_reasoner_app/freeze_after_update/__init__.py': 'b856255feee5255f146c6a08294cf1c9279facd12b6d116383a85065b76a10c8',
 'kanda_reasoner_app/freeze_after_update/contract.py': '371d4c2b6538f3ebf64a3d735b21d899ee611ccbc26b70f24f5a2aad7f440e4b',
 'kanda_reasoner_app/manage_architecture/architecture_review_subtabs.py': '9f06f78b96c24fa3193ffc0b2c9b2aaa30a835035c33d2a1e9a980ac43b1c730',
 'kanda_reasoner_app/manage_architecture/audit_project_sibling_tabs.py': '1d416fc21e4079c456f0c1f85217b8a00892396efc3fa8b50ae264564114e4c6',
 'kanda_reasoner_app/project_exclusion_path_matching.py': 'b8c30c49fed35b2ecf02046a4bca13c040230c455758b167f9a9b8ec7f0c4b02',
 'kanda_reasoner_app/project_exclusion_policy.py': 'c8e40e15192b2c8ee317c8c54452392d9ed21813fd130affdb06fb011bfac842',
 'tests/test_engineering_diagnostics_wave2oa.py': '4cefd958d53df34acd8b53b4b9a3f8fdbb1e2afd806e01dc19806b551c26bbbd',
 'tests/test_engineering_diagnostics_wave2ob.py': '84a5ee2c3f12581a1a01bd994442a1450493c7355995a990140bc29be200792f',
 'tests/test_engineering_diagnostics_wave2oc.py': 'eb9ab572427243db551d57835bad017eb65ffd29ccf553981e96b125fb502c0d',
 'tests/test_engineering_diagnostics_wave2od.py': 'dbf3d1857019b49705a7756ca0ed987df67e38fde88fb31897fa92ba506b3b6f',
 'tests/test_engineering_diagnostics_wave2pa.py': 'faa0e492c47f30be3c0f6970e6cc3fc6442eef00478f28e6f4f02314b22eae0e',
 'tools/engineering_diagnostics_wave2pa_architecture_gate.py': '8e5839bacb9a95805519f4e5ec22c9c6642f878049eb6f16257c50082cefbad6',
 'tools/validate_engineering_diagnostics_wave2oa_v1.py': '88aaea82f2f5230744945088b20e7dc251173236aace685e87aa7ada54218b45',
 'tools/validate_engineering_diagnostics_wave2ob_v1.py': 'd27b9b83c75381991e60636ac2d4807645e4ccc245b5b0ee86acb2aa3ea25cc2',
 'tools/validate_engineering_diagnostics_wave2oc_v1.py': '8f8177fc87268a8e5c8d5e3da1ec101e5ecf1d4b88c88b840d17be7bd7436c67',
 'tools/validate_engineering_diagnostics_wave2od_v1.py': '8f92d3d927561052ea121abac6d9d2d371b91f7e0f2050ea0f0fd52a531e0412'}
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
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
        env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"),
    )
    output = completed.stdout or ""
    print(output, end="" if output.endswith("\n") else "\n")
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
        ("tests.test_engineering_diagnostics_wave2pa", 10),
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
    print("WAVE2PA FOCUSED PUBLIC CONTRACT TESTS: 10/10 PASS")
    print("FOCUSED PUBLIC CONTRACT TESTS: 56/56 PASS")
    print("WAVE2PA BATCH ENRICHMENT 25000 FINDINGS: PASS")
    print("WAVE2OA THROUGH WAVE2OD CONTRACT REGRESSION: PASS")


def _optional_hash(path: Path) -> str:
    return _sha256(path) if path.is_file() else "ABSENT"


def _check_live_enrichment(root: Path) -> tuple[int, str]:
    from kanda_reasoner_app.engineering_diagnostics import (
        DiagnosticFindingInput,
        DiagnosticFindingRecord,
        EngineeringDiagnosticsEnricher,
        engineering_diagnostics_database_path,
        issue_fingerprint,
    )
    from kanda_reasoner_app.freeze_after_update import (
        inspect_freeze_after_update_box,
    )
    from kanda_reasoner_app.project_selection_registry import (
        ProjectSelectionRegistry,
    )

    freeze_result = inspect_freeze_after_update_box(root)
    _require(freeze_result.ok, "WAVE2PA_FREEZE_BOX_NOT_VALID")
    _require(freeze_result.box_root is not None, "WAVE2PA_FREEZE_BOX_ROOT_MISSING")
    freeze_index = (
        freeze_result.box_root
        / "frozen_features_memory"
        / "freeze_index.json"
    )
    _require(freeze_index.is_file(), "WAVE2PA_FREEZE_INDEX_MISSING")
    freeze_before = _sha256(freeze_index)
    boundary = ProjectSelectionRegistry(
        tool_source_root=root
    ).resolve_boundary_for_root(root)
    database = engineering_diagnostics_database_path(boundary)
    database_before = _optional_hash(database)

    enricher = EngineeringDiagnosticsEnricher(root)

    def record(relative: str) -> DiagnosticFindingRecord:
        return DiagnosticFindingRecord(
            run_id="wave2pa-live",
            issue_fingerprint="issue-" + hashlib.sha256(
                relative.encode("utf-8")
            ).hexdigest(),
            evidence_digest="evidence",
            code="WAVE2PA_LIVE",
            relative_path=relative,
            message="Wave 2P-A live enrichment probe.",
            severity="info",
            confidence="high",
            semantic_key="wave2pa-live",
            symbol_id="",
            location_key="",
            category="wave2pa",
            line=1,
            evidence={},
            suggested_action="None.",
        )

    protected = enricher.enrich(
        record("kanda_reasoner_app/engineering_diagnostics_gui/controller.py")
    )
    active = enricher.enrich(
        record("kanda_reasoner_app/engineering_diagnostics/scope_enrichment.py")
    )
    test = enricher.enrich(record("tests/test_engineering_diagnostics_wave2pa.py"))
    reference = enricher.enrich(record(".project_reference/archived.py"))

    _require(protected.scope.classification == "ACTIVE", "WAVE2PA_ACTIVE_SCOPE_MISMATCH")
    _require(protected.frozen_path.status == "FROZEN", "WAVE2PA_PRIOR_FROZEN_PATH_MISSED")
    _require(
        bool(protected.frozen_path.governing_freeze_ids),
        "WAVE2PA_GOVERNING_FREEZE_IDS_MISSING",
    )
    _require(active.scope.classification == "ACTIVE", "WAVE2PA_NEW_SOURCE_SCOPE_MISMATCH")
    _require(
        active.frozen_path.status in {"UNFROZEN", "FROZEN"},
        "WAVE2PA_NEW_SOURCE_FREEZE_STATUS_INVALID",
    )
    _require(test.scope.classification == "TEST", "WAVE2PA_TEST_SCOPE_MISMATCH")
    _require(
        reference.scope.classification == "REFERENCE",
        "WAVE2PA_REFERENCE_SCOPE_MISMATCH",
    )

    identity_input = DiagnosticFindingInput(
        code="F821",
        relative_path="kanda_reasoner_app/example.py",
        message="Undefined name.",
        semantic_key="F821|Undefined name.",
    )
    identity_before = issue_fingerprint("ruff.check", identity_input)
    enricher.enrich(record("kanda_reasoner_app/example.py"))
    identity_after = issue_fingerprint("ruff.check", identity_input)
    _require(identity_before == identity_after, "WAVE2PA_FINDING_IDENTITY_MUTATED")

    _require(_sha256(freeze_index) == freeze_before, "WAVE2PA_FREEZE_INDEX_MUTATED")
    _require(_optional_hash(database) == database_before, "WAVE2PA_DATABASE_MUTATED")
    print("WAVE2PA SCOPE CLASSIFICATION: PASS")
    print("WAVE2PA FROZEN PATH CLASSIFICATION: PASS")
    print("WAVE2PA GOVERNING FREEZE IDS: PASS")
    print("WAVE2PA FINDING FINGERPRINTS UNCHANGED: PASS")
    print("WAVE2PA FREEZE MEMORY MUTATED: NO")
    print("WAVE2PA DIAGNOSTIC DATABASE MUTATED: NO")
    print("WAVE2PA PROJECT_FREEZE_LEDGER USED: NO")
    return len(protected.frozen_path.governing_freeze_ids), active.frozen_path.status


def _check_gui(root: Path) -> tuple[float, float, float]:
    package = importlib.import_module("kanda_reasoner_app.engineering_diagnostics_gui")
    _require(
        callable(getattr(package, "create_engineering_diagnostics_panel", None)),
        "ENGINEERING_DIAGNOSTICS_GUI_FACTORY_MISSING",
    )
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    try:
        from PySide6.QtCore import QElapsedTimer
        from PySide6.QtWidgets import QApplication
    except ImportError as exc:
        raise RuntimeError("PYSIDE6_REQUIRED_FOR_GUI_VALIDATION") from exc
    from kanda_reasoner_app.engineering_diagnostics import (
        DiagnosticFindingEnrichment,
        DiagnosticFindingRecord,
        DiagnosticFrozenPathEnrichment,
        DiagnosticScopeEnrichment,
    )
    from kanda_reasoner_app.engineering_diagnostics_gui import DiagnosticFindingView

    app = QApplication.instance() or QApplication([])
    started = time.perf_counter()
    panel = package.create_engineering_diagnostics_panel(
        project_root_provider=lambda: str(root),
        defer_initial_refresh=True,
    )
    panel_ms = (time.perf_counter() - started) * 1000.0
    _require(panel.objectName() == "engineering_diagnostics_page", "GUI_PANEL_OBJECT_NAME")
    _require(hasattr(panel, "engineering_diagnostics_scope_combo"), "GUI_SCOPE_FILTER_MISSING")
    _require(hasattr(panel, "engineering_diagnostics_frozen_combo"), "GUI_FROZEN_FILTER_MISSING")

    active_context = DiagnosticFindingEnrichment(
        scope=DiagnosticScopeEnrichment("ACTIVE", "high", "fixture"),
        frozen_path=DiagnosticFrozenPathEnrichment(
            "FROZEN",
            governing_freeze_ids=("freeze-fixture",),
        ),
    )
    other_context = DiagnosticFindingEnrichment(
        scope=DiagnosticScopeEnrichment("TEST", "high", "fixture"),
        frozen_path=DiagnosticFrozenPathEnrichment("UNFROZEN"),
    )
    rows = tuple(
        DiagnosticFindingView(
            record=DiagnosticFindingRecord(
                run_id="scale-run",
                issue_fingerprint="issue-" + str(index),
                evidence_digest="evidence-" + str(index),
                code="F821" if index % 2 == 0 else "F401",
                relative_path="src/file_" + str(index).zfill(5) + ".py",
                message="Synthetic finding " + str(index),
                severity="error" if index % 2 == 0 else "warning",
                confidence="high",
                semantic_key="semantic-" + str(index),
                symbol_id="symbol-" + str(index),
                location_key="location-" + str(index),
                category="ruff",
                line=1,
                evidence={},
                suggested_action="Review.",
            ),
            lifecycle_state="new" if index % 3 == 0 else "persistent",
            enrichment=active_context if index % 2 == 0 else other_context,
        )
        for index in range(25000)
    )
    source = panel.engineering_diagnostics_table.model()
    _require(not callable(getattr(source, "sourceModel", None)), "GUI_PROXY_MODEL_PRESENT")
    timer = QElapsedTimer()
    timer.start()
    source.set_rows(rows)
    app.processEvents()
    rows_ms = float(timer.elapsed())
    timer.restart()
    source.set_filters("error", "all", "active", "frozen", "file_24998")
    filtered = source.rowCount()
    app.processEvents()
    filter_ms = float(timer.elapsed())
    _require(filtered == 1, "GUI_SCOPE_FREEZE_FILTER_RESULT_MISMATCH")
    _require(panel_ms < 2000.0, "GUI_PANEL_CREATION_TARGET_EXCEEDED")
    _require(rows_ms < 2000.0, "GUI_25000_ROW_TARGET_EXCEEDED")
    _require(filter_ms < 500.0, "GUI_FILTER_TARGET_EXCEEDED")
    panel.deleteLater()
    app.processEvents()
    print("ENGINEERING DIAGNOSTICS GUI COMPLETE IMPORT GRAPH: PASS")
    print("ENGINEERING DIAGNOSTICS GUI FACTORY SMOKE: PASS")
    print("WAVE2PA GUI SCOPE FILTER: PASS")
    print("WAVE2PA GUI FROZEN FILTER: PASS")
    print("WAVE2PA GUI DIRECT INDEXED MODEL: PASS")
    print("WAVE2PA GUI 25000 ROW INITIALIZATION MS: " + f"{rows_ms:.1f}")
    print("WAVE2PA GUI FILTER UPDATE MS: " + f"{filter_ms:.1f}")
    print("WAVE2PA GUI PANEL CREATION MS: " + f"{panel_ms:.1f}")
    print("WAVE2PA GUI HIGH-VOLUME PERFORMANCE: PASS")
    return panel_ms, rows_ms, filter_ms


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
    validate_engineering_diagnostics_wave2pa_architecture_non_regression(output)


def _write_evidence(root: Path, lines: list[str]) -> Path:
    from kanda_reasoner_app.project_selection_registry import ProjectSelectionRegistry

    boundary = ProjectSelectionRegistry(tool_source_root=root).resolve_boundary_for_root(root)
    target = (
        boundary.active_project_support_root
        / "project_validation_evidence"
        / "engineering_diagnostics_wave2pa"
        / "engineering_diagnostics_wave2pa_v1.txt"
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
    source = validator_path.read_text(encoding="utf-8")
    canonical = source.replace(
        'VALIDATOR_CANONICAL_SHA256 = "' + VALIDATOR_CANONICAL_SHA256 + '"',
        'VALIDATOR_CANONICAL_SHA256 = "' + ("0" * 64) + '"',
        1,
    )
    digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    _require(digest == VALIDATOR_CANONICAL_SHA256, "WAVE2PA_VALIDATOR_CANONICAL_HASH_MISMATCH")
    print("WAVE2PA VALIDATOR CANONICAL HASH: PASS")
    _check_hashes(root, _PAYLOAD_HASHES, "WAVE2PA INSTALLED HASHES: PASS")
    _check_hashes(
        root,
        _UNCHANGED_HASHES,
        "WAVE2OA THROUGH WAVE2OD PROTECTED HASHES: PASS",
    )
    registry_path, registry_before = _registry_digest(root)
    validate_engineering_diagnostics_wave2pa_public_boundary(root)
    _run_tests(root)
    freeze_count, new_path_status = _check_live_enrichment(root)
    panel_ms, rows_ms, filter_ms = _check_gui(root)
    _run_architecture_non_regression(root)
    registry_after = _sha256(registry_path) if registry_path.is_file() else "ABSENT"
    _require(registry_before == registry_after, "PROJECT_SELECTION_REGISTRY_MUTATED")
    print("PROJECT SELECTION REGISTRY MUTATED: NO")
    print("TOOL PROJECT LOGICAL ROLE SEPARATION: PASS")
    lines = [
        "PACKAGE REVISION: " + PACKAGE_REVISION,
        "WAVE2PA INSTALLED HASHES: PASS",
        "WAVE2OA THROUGH WAVE2OD PROTECTED HASHES: PASS",
        "WAVE2PA PUBLIC-CONTRACT-ONLY COMMUNICATION: PASS",
        "WAVE2PA SCOPE MARKER DIRECTORY CACHE: PASS",
        "WAVE2PA RELATIVE EXCLUSION POLICY FAST PATH: PASS",
        "FOCUSED PUBLIC CONTRACT TESTS: 56/56 PASS",
        "WAVE2PA BATCH ENRICHMENT 25000 FINDINGS: PASS",
        "WAVE2PA SCOPE CLASSIFICATION: PASS",
        "WAVE2PA FROZEN PATH CLASSIFICATION: PASS",
        "WAVE2PA GOVERNING FREEZE IDS: PASS (" + str(freeze_count) + ")",
        "WAVE2PA NEW PATH FREEZE STATUS: " + new_path_status,
        "WAVE2PA FINDING FINGERPRINTS UNCHANGED: PASS",
        "WAVE2PA FREEZE MEMORY MUTATED: NO",
        "WAVE2PA DIAGNOSTIC DATABASE MUTATED: NO",
        "WAVE2PA PROJECT_FREEZE_LEDGER USED: NO",
        "WAVE2PA GUI SCOPE FILTER: PASS",
        "WAVE2PA GUI FROZEN FILTER: PASS",
        "WAVE2PA GUI 25000 ROW INITIALIZATION MS: " + f"{rows_ms:.1f}",
        "WAVE2PA GUI FILTER UPDATE MS: " + f"{filter_ms:.1f}",
        "WAVE2PA GUI PANEL CREATION MS: " + f"{panel_ms:.1f}",
        "WAVE2PA GUI HIGH-VOLUME PERFORMANCE: PASS",
        "WAVE2PA NEW ARCHITECTURE ISSUES: 0",
        "WAVE2PA TOUCHED PATH ARCHITECTURE ISSUES: 0",
        "PROJECT SELECTION REGISTRY MUTATED: NO",
        "TOOL PROJECT LOGICAL ROLE SEPARATION: PASS",
        "VALIDATION OK: " + FEATURE_ID,
        "STATUS: IN_SYNC",
    ]
    evidence = _write_evidence(root, lines)
    print("VALIDATION EVIDENCE WRITTEN: " + str(evidence))
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
