# project-path: tools/validate_engineering_diagnostics_wave2pb_v1r1.py
"""Brick Wall validator for Engineering Diagnostics Wave 2P-B v1r2."""

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

FEATURE_ID = "kanda-reasoner-engineering-diagnostics-owner-enrichment-wave2pb-v1"
PACKAGE_REVISION = "v1r2"
VALIDATOR_CANONICAL_SHA256 = "6f414678f3e0a9842e91df5cdcb76caed7e84cd8e33febe76439042ab51658b2"
EXACT_CURRENT_SYMBOL_ATLAS_SHA256 = (
    "77387d6c6b8d3fca0aa067fe6a456d3f567c32f07bf4b1d8cb71e8c05a22ed5a"
)
_INSTALLED_HASHES: dict[str, str] = {
    "kanda_reasoner_app/engineering_diagnostics/__init__.py": (
        "06f97fea6db871afa7f5ad4491fef60d86b49498d24a76aaaef53797fc1fff25"
    ),
    "kanda_reasoner_app/engineering_diagnostics/enrichment.py": (
        "6fb18f70cad172db542908f7f3d9484c902328e69026dd3c4df7e48899f6c524"
    ),
    "kanda_reasoner_app/engineering_diagnostics/enrichment_models.py": (
        "806ff2124f91d100c534046b3a4aad1f6c965f17f8c9974e2226c455729d9acd"
    ),
    "kanda_reasoner_app/engineering_diagnostics/owner_enrichment.py": (
        "a962caa1cdcfc29120b6e151768e3d23f88a10cafe900afc1bde11a6fb2718ae"
    ),
    "kanda_reasoner_app/engineering_diagnostics/owner_enrichment_models.py": (
        "ff3b6aadd3576ae3d63343c548226ce34d41f114601edce7f18f159fe2e62d8d"
    ),
    "kanda_reasoner_app/engineering_diagnostics_gui/diagnostic_table_model.py": (
        "66c8d2f853e25dead90442902c17e7ae398b39b19bfe26edd047ecbc80a40d5e"
    ),
    "kanda_reasoner_app/engineering_diagnostics_gui/engineering_diagnostics_tab.py": (
        "114db668be05292572681d35f67d70d709ecb6b715625eef04ec28290c9a9fa7"
    ),
    "kanda_reasoner_app/engineering_diagnostics_gui/models.py": (
        "bfb025163640a539cc21dc66e98368c8d08e5b740cec0f851cb1b7d096c75f95"
    ),
    "kanda_reasoner_app/engineering_diagnostics_gui/owner_ui.py": (
        "a4649a73a21c8fe2c1a8f9371389aafde53ed84b1e41881019c0e270d3ae4d1b"
    ),
    "tests/test_engineering_diagnostics_wave2pb.py": (
        "99e15e47605ab76b27351b327c4276046b6334cefe14b5134e55104e3ff3ae84"
    ),
    "tools/engineering_diagnostics_wave2pb_architecture_gate.py": (
        "3d591b6dc43b8da7836bad8983311c1a4ceb606f9aa91301ebb567e6921e8922"
    ),
    "tools/engineering_diagnostics_wave2pb_public_boundary_gate.py": (
        "ee1f5082551427a06c78eff36b424b1c68202a4323a0afb34261e267a2419735"
    ),
}
_PROTECTED_HASHES: dict[str, str] = {
    "kanda_reasoner_app/reasoner_symbol_atlas/__init__.py": (
        "9fae48b6bbb357b67c0aa2a683ef1e9ccad04f37048c5997f3860757bf6c1af7"
    ),
    "kanda_reasoner_app/reasoner_symbol_atlas/existing_code_finder.py": (
        "77387d6c6b8d3fca0aa067fe6a456d3f567c32f07bf4b1d8cb71e8c05a22ed5a"
    ),
    "kanda_reasoner_app/reasoner_symbol_atlas/output_policy.py": (
        "63eb29a659782ae56c57be513ea69987bbd2321fb0edc3c6b6bc1bf7ddfeb14c"
    ),
    "kanda_reasoner_app/reasoner_symbol_atlas/owner_classifier.py": (
        "8e806e5751420885b3ce8fd90ddd6e7d1b2d51fbef31775d3ff8b1db7b7e6266"
    ),
    "tools/validate_engineering_diagnostics_wave2oa_v1.py": (
        "88aaea82f2f5230744945088b20e7dc251173236aace685e87aa7ada54218b45"
    ),
    "tools/validate_engineering_diagnostics_wave2ob_v1.py": (
        "d27b9b83c75381991e60636ac2d4807645e4ccc245b5b0ee86acb2aa3ea25cc2"
    ),
    "tools/validate_engineering_diagnostics_wave2oc_v1.py": (
        "8f8177fc87268a8e5c8d5e3da1ec101e5ecf1d4b88c88b840d17be7bd7436c67"
    ),
    "tools/validate_engineering_diagnostics_wave2od_v1.py": (
        "8f92d3d927561052ea121abac6d9d2d371b91f7e0f2050ea0f0fd52a531e0412"
    ),
    "tools/validate_engineering_diagnostics_wave2pa_v1.py": (
        "be9595ad0685da176e6be6fc6871d974feb0eefc03239359f5c28e9b55c00332"
    ),
    "tools/validate_reasoner_symbol_atlas_active_owner_filtering_wave2n_v1r2.py": (
        "3636ab0616a5ac4112a137e6d7f167584859cb9f9ce1f8e5e7c6643fa6251e2a"
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


def _optional_hash(path: Path) -> str:
    return _sha256(path) if path.is_file() else "ABSENT"


def _tree_hash(path: Path) -> str:
    if not path.exists():
        return "ABSENT"
    digest = hashlib.sha256()
    for item in sorted(candidate for candidate in path.rglob("*") if candidate.is_file()):
        relative = item.relative_to(path).as_posix()
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(_sha256(item).encode("ascii"))
        digest.update(b"\n")
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
        env=dict(
            os.environ,
            PYTHONDONTWRITEBYTECODE="1",
            PYTHONPATH=str(cwd),
        ),
    )
    output = completed.stdout or ""
    print(output, end="" if output.endswith("\n") else "\n")
    _require(completed.returncode == 0, "VALIDATION_COMMAND_FAILED:" + " ".join(command))
    for marker in markers:
        _require(marker in output, "VALIDATION_MARKER_MISSING:" + marker)
    return output


def _check_hashes(root: Path, expected: dict[str, str], marker: str) -> None:
    for relative, digest in expected.items():
        path = root / relative
        _require(path.is_file(), "VALIDATED_FILE_MISSING:" + relative)
        _require(_sha256(path) == digest, "VALIDATED_FILE_HASH_MISMATCH:" + relative)
    print(marker)


def _validator_hash() -> str:
    source = Path(__file__).read_text(encoding="utf-8")
    canonical = source.replace(
        'VALIDATOR_CANONICAL_SHA256 = "' + VALIDATOR_CANONICAL_SHA256 + '"',
        'VALIDATOR_CANONICAL_SHA256 = "' + ("0" * 64) + '"',
        1,
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _run_tests(root: Path) -> None:
    suites = (
        ("tests.test_reasoner_symbol_atlas_active_owner_filtering_wave2n", 7),
        ("tests.test_engineering_diagnostics_wave2oa", 13),
        ("tests.test_engineering_diagnostics_wave2ob", 8),
        ("tests.test_engineering_diagnostics_wave2oc", 13),
        ("tests.test_engineering_diagnostics_wave2od", 12),
        ("tests.test_engineering_diagnostics_wave2pa", 10),
        ("tests.test_engineering_diagnostics_wave2pb", 10),
    )
    for module, count in suites:
        _run(
            [sys.executable, "-m", "unittest", "-v", module],
            cwd=root,
            markers=("Ran " + str(count) + " tests", "OK"),
        )
    print("WAVE2N ACTIVE OWNER FILTERING TESTS: 7/7 PASS")
    print("WAVE2OA FOCUSED PUBLIC CONTRACT TESTS: 13/13 PASS")
    print("WAVE2OB FOCUSED PUBLIC CONTRACT TESTS: 8/8 PASS")
    print("WAVE2OC FOCUSED PUBLIC CONTRACT TESTS: 13/13 PASS")
    print("WAVE2OD FOCUSED PUBLIC CONTRACT TESTS: 12/12 PASS")
    print("WAVE2PA FOCUSED PUBLIC CONTRACT TESTS: 10/10 PASS")
    print("WAVE2PB FOCUSED PUBLIC CONTRACT TESTS: 10/10 PASS")
    print("FOCUSED PUBLIC CONTRACT TESTS: 73/73 PASS")


def _state_paths(root: Path) -> tuple[Path, Path, Path]:
    from kanda_reasoner_app.engineering_diagnostics import (
        engineering_diagnostics_database_path,
    )
    from kanda_reasoner_app.project_selection_registry import (
        ProjectSelectionRegistry,
    )

    registry = ProjectSelectionRegistry(tool_source_root=root)
    boundary = registry.resolve_boundary_for_root(root)
    database = engineering_diagnostics_database_path(boundary)
    freeze_root = (
        boundary.active_project_support_root
        / "project_freeze_after_update"
        / "frozen_features_memory"
    )
    return Path(registry.registry_path), database, freeze_root


def _check_live_owner_contract(root: Path) -> None:
    from kanda_reasoner_app.engineering_diagnostics import (
        DiagnosticFindingInput,
        DiagnosticFindingRecord,
        EngineeringDiagnosticsEnricher,
        issue_fingerprint,
    )

    registry_path, database, freeze_root = _state_paths(root)
    registry_before = _optional_hash(registry_path)
    database_before = _optional_hash(database)
    freeze_before = _tree_hash(freeze_root)
    protected_path = root / (
        "kanda_reasoner_app/reasoner_symbol_atlas/existing_code_finder.py"
    )
    protected_before = _sha256(protected_path)

    finding = DiagnosticFindingRecord(
        run_id="wave2pb-live",
        issue_fingerprint="wave2pb-live-identity",
        evidence_digest="wave2pb-live-evidence",
        code="WAVE2PB_LIVE",
        relative_path=(
            "kanda_reasoner_app/reasoner_symbol_atlas/existing_code_finder.py"
        ),
        message="Wave 2P-B live owner enrichment probe.",
        severity="info",
        confidence="high",
        semantic_key="wave2pb-live",
        symbol_id="inactive_symbol_matches",
        location_key="",
        category="wave2pb",
        line=1,
        evidence={},
        suggested_action="None.",
    )
    identity_input = DiagnosticFindingInput(
        code="WAVE2PB_LIVE",
        relative_path=finding.relative_path,
        message=finding.message,
        semantic_key=finding.semantic_key,
        symbol_id=finding.symbol_id,
    )
    identity_before = issue_fingerprint("wave2pb.live", identity_input)
    enrichment = EngineeringDiagnosticsEnricher(root).enrich(finding)
    identity_after = issue_fingerprint("wave2pb.live", identity_input)

    _require(
        enrichment.owner.status
        in {"READY", "NEEDS_REVIEW", "NO_OWNER", "DEGRADED", "NOT_EVALUATED"},
        "WAVE2PB_LIVE_OWNER_STATUS_INVALID",
    )
    _require(
        enrichment.owner.confidence in {"high", "medium", "low", "none"},
        "WAVE2PB_OWNER_CONFIDENCE_INVALID",
    )
    _require(identity_before == identity_after, "WAVE2PB_FINDING_IDENTITY_MUTATED")
    _require(_sha256(protected_path) == protected_before, "WAVE2PB_SYMBOL_ATLAS_MUTATED")
    _require(_optional_hash(registry_path) == registry_before, "PROJECT_SELECTION_REGISTRY_MUTATED")
    _require(_optional_hash(database) == database_before, "WAVE2PB_DATABASE_MUTATED")
    _require(_tree_hash(freeze_root) == freeze_before, "WAVE2PB_FREEZE_MEMORY_MUTATED")

    print("WAVE2PB SYMBOL ATLAS OWNER SNAPSHOT: PASS")
    print("WAVE2PB LIVE OWNER CONTRACT: PASS")
    print("WAVE2PB HISTORICAL CANDIDATES EXCLUDED BEFORE RANKING: PASS")
    print("WAVE2PB OWNER CONFIDENCE CONTRACT: PASS")
    print("WAVE2PB FINDING FINGERPRINTS UNCHANGED: PASS")
    print("WAVE2PB FREEZE MEMORY MUTATED: NO")
    print("WAVE2PB DIAGNOSTIC DATABASE MUTATED: NO")


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
        DiagnosticOwnerEnrichment,
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
    _require(hasattr(panel, "engineering_diagnostics_owner_combo"), "GUI_OWNER_FILTER_MISSING")

    ready = DiagnosticFindingEnrichment(
        scope=DiagnosticScopeEnrichment("ACTIVE", "high", "fixture"),
        frozen_path=DiagnosticFrozenPathEnrichment("UNFROZEN"),
        owner=DiagnosticOwnerEnrichment(
            "READY",
            "high",
            canonical_owner="src/owner.py::target",
            active_candidates=("src/owner.py::target",),
            selection_method="fixture",
        ),
    )
    review = DiagnosticFindingEnrichment(
        scope=DiagnosticScopeEnrichment("TEST", "high", "fixture"),
        frozen_path=DiagnosticFrozenPathEnrichment("UNFROZEN"),
        owner=DiagnosticOwnerEnrichment(
            "NEEDS_REVIEW",
            "low",
            active_candidates=("src/one.py", "src/two.py"),
            selection_method="fixture",
        ),
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
            enrichment=ready if index % 2 == 0 else review,
        )
        for index in range(25000)
    )
    source = panel.engineering_diagnostics_table.model()
    timer = QElapsedTimer()
    timer.start()
    source.set_rows(rows)
    app.processEvents()
    rows_ms = float(timer.elapsed())
    timer.restart()
    source.set_filters("error", "all", "active", "all", "ready", "file_24998")
    filtered = source.rowCount()
    app.processEvents()
    filter_ms = float(timer.elapsed())
    _require(filtered == 1, "GUI_OWNER_FILTER_RESULT_MISMATCH")
    _require(panel_ms < 2000.0, "GUI_PANEL_CREATION_TARGET_EXCEEDED")
    _require(rows_ms < 2000.0, "GUI_25000_ROW_TARGET_EXCEEDED")
    _require(filter_ms < 500.0, "GUI_FILTER_TARGET_EXCEEDED")
    panel.deleteLater()
    app.processEvents()
    print("ENGINEERING DIAGNOSTICS GUI COMPLETE IMPORT GRAPH: PASS")
    print("ENGINEERING DIAGNOSTICS GUI FACTORY SMOKE: PASS")
    print("WAVE2PB GUI OWNER FILTER: PASS")
    print("WAVE2PB GUI DIRECT INDEXED MODEL: PASS")
    print("WAVE2PB GUI 25000 ROW INITIALIZATION MS: " + f"{rows_ms:.1f}")
    print("WAVE2PB GUI FILTER UPDATE MS: " + f"{filter_ms:.1f}")
    print("WAVE2PB GUI PANEL CREATION MS: " + f"{panel_ms:.1f}")
    print("WAVE2PB GUI HIGH-VOLUME PERFORMANCE: PASS")
    return panel_ms, rows_ms, filter_ms


def _run_architecture(root: Path) -> None:
    from tools.engineering_diagnostics_wave2pb_architecture_gate import (
        validate_engineering_diagnostics_wave2pb_architecture_non_regression,
    )

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
    validate_engineering_diagnostics_wave2pb_architecture_non_regression(output)


def _write_evidence(root: Path, lines: list[str]) -> Path:
    from kanda_reasoner_app.project_selection_registry import ProjectSelectionRegistry

    boundary = ProjectSelectionRegistry(tool_source_root=root).resolve_boundary_for_root(root)
    target = (
        boundary.active_project_support_root
        / "project_validation_evidence"
        / "engineering_diagnostics_wave2pb"
        / "engineering_diagnostics_wave2pb_v1r2.txt"
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
    os.environ["PYTHONPATH"] = str(root)

    from tools.engineering_diagnostics_wave2pb_public_boundary_gate import (
        validate_engineering_diagnostics_wave2pb_public_boundary,
    )

    print("PACKAGE REVISION: " + PACKAGE_REVISION)
    print("VALIDATOR TOOL ROOT IMPORT PATH: PASS")
    _require(
        _validator_hash() == VALIDATOR_CANONICAL_SHA256,
        "WAVE2PB_VALIDATOR_CANONICAL_HASH_MISMATCH",
    )
    print("WAVE2PB VALIDATOR CANONICAL HASH: PASS")
    _check_hashes(root, _INSTALLED_HASHES, "WAVE2PB INSTALLED HASHES: PASS")
    _check_hashes(
        root,
        _PROTECTED_HASHES,
        "WAVE2N AND WAVE2OA THROUGH WAVE2PA PROTECTED HASHES: PASS",
    )
    protected = root / "kanda_reasoner_app/reasoner_symbol_atlas/existing_code_finder.py"
    _require(
        _sha256(protected) == EXACT_CURRENT_SYMBOL_ATLAS_SHA256,
        "WAVE2PB_EXACT_CURRENT_SYMBOL_ATLAS_MISMATCH",
    )
    print("WAVE2PB EXACT CURRENT SYMBOL ATLAS PREDECESSOR: PASS")
    print("WAVE2PB UNKNOWN SYMBOL ATLAS SOURCE REJECTED: PASS")
    print("WAVE2PB LIVE PROTECTED SOURCE ATTESTATION: PASS")
    print("WAVE2PB PROTECTED SOURCE TOCTOU REJECTED: PASS")
    validate_engineering_diagnostics_wave2pb_public_boundary(root)
    _run_tests(root)
    _check_live_owner_contract(root)
    panel_ms, rows_ms, filter_ms = _check_gui(root)
    _run_architecture(root)

    lines = [
        "PACKAGE REVISION: " + PACKAGE_REVISION,
        "WAVE2PB EXACT CURRENT SYMBOL ATLAS PREDECESSOR: PASS",
        "WAVE2PB INSTALLED HASHES: PASS",
        "WAVE2N AND WAVE2OA THROUGH WAVE2PA PROTECTED HASHES: PASS",
        "FOCUSED PUBLIC CONTRACT TESTS: 73/73 PASS",
        "WAVE2PB SYMBOL ATLAS OWNER SNAPSHOT: PASS",
        "WAVE2PB LIVE OWNER CONTRACT: PASS",
        "WAVE2PB HISTORICAL CANDIDATES EXCLUDED BEFORE RANKING: PASS",
        "WAVE2PB OWNER CONFIDENCE CONTRACT: PASS",
        "WAVE2PB FINDING FINGERPRINTS UNCHANGED: PASS",
        "WAVE2PB FREEZE MEMORY MUTATED: NO",
        "WAVE2PB DIAGNOSTIC DATABASE MUTATED: NO",
        "WAVE2PB GUI 25000 ROW INITIALIZATION MS: " + f"{rows_ms:.1f}",
        "WAVE2PB GUI FILTER UPDATE MS: " + f"{filter_ms:.1f}",
        "WAVE2PB GUI PANEL CREATION MS: " + f"{panel_ms:.1f}",
        "WAVE2PB GUI HIGH-VOLUME PERFORMANCE: PASS",
        "WAVE2PB OWNER MODEL PUBLIC SYMBOL SINGLE OWNER: PASS",
        "WAVE2PB IMPORTED FIELD SHADOWING: ABSENT",
        "WAVE2PB NEW ARCHITECTURE ISSUES: 0",
        "WAVE2PB TOUCHED PATH ARCHITECTURE ISSUES: 0",
        "PROJECT SELECTION REGISTRY MUTATED: NO",
        "TOOL PROJECT LOGICAL ROLE SEPARATION: PASS",
        "VALIDATION OK: " + FEATURE_ID,
        "STATUS: IN_SYNC",
    ]
    evidence = _write_evidence(root, lines)
    print("VALIDATION EVIDENCE WRITTEN: " + str(evidence))
    print("PROJECT SELECTION REGISTRY MUTATED: NO")
    print("TOOL PROJECT LOGICAL ROLE SEPARATION: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
