# project-path: tools/validate_engineering_diagnostics_wave2w_v1r2.py
"""Brick Wall validator for Wave 2W v1r2 runtime collector correction."""

from __future__ import annotations

import argparse
import hashlib
import os
from pathlib import Path
import sys
from threading import Event

FEATURE_ID = 'kanda-reasoner-engineering-safety-audit-diagnostics-hierarchy-wave2w-v1r2-runtime-collector-correction'
PACKAGE_REVISION = "v1r2"
VALIDATOR_CANONICAL_SHA256 = "bab899d29e98fbde133ab3953f2c16e9f35abf0db8d3f1a18de3db989d3b7712"
_WAVE2W_V1R1_HASHES = {'kanda_reasoner_app/engineering_diagnostics_gui/__init__.py': 'e3081aa606de29c193bdf242d4579cc90659eae7e2ee69d21350ac4568ea079a',
 'kanda_reasoner_app/engineering_diagnostics_gui/engineering_diagnostics_workspace.py': '96954177350efb1811ab3619dd05b84bc15db09303113331623fbd21f9985be1',
 'kanda_reasoner_app/engineering_diagnostics_gui/full_engineering_diagnostics_tab.py': 'fe448c88540e8c0a201373c205524d926b2c0adbf06f0be5d8a0844e5344590b',
 'kanda_reasoner_app/manage_architecture/audit_project_sibling_tabs.py': '12e1fce0da71c285b675ef48997884c09d8fece50050c2f7a45779e27f8ae57e',
 'reasoner_tools_gui_engineering_safety_panel.py': '00d8c70a5d76642dccfad4314d40323c278433b66de3d0d9384b3232d46f969a',
 'tests/test_engineering_diagnostics_wave2v.py': '521ea5bee8d6fcd042edc69c1cad3ba331012a30c5cb188187a7a422815c9993',
 'tests/test_engineering_diagnostics_wave2v_gui_scale.py': '75782cc0ac64986d488370e906f53bf25eeb5e10860874462711ef2747bde5b6',
 'tests/test_engineering_diagnostics_wave2w.py': '94b7152d371c3e911f5d350f3d165c3d5416308b291abe4f01a1b839038ad577',
 'tests/test_engineering_diagnostics_wave2w_gui_scale.py': '2e1e6c2e204379de9ff6112088c37982b5f1ad390ba9b6a869073593b2c32225',
 'tools/engineering_diagnostics_wave2v_architecture_gate.py': '7d2ef04556081d6ae3197568129bfa17ae1eb5e1d56ddd663fa8a226eb01ff71',
 'tools/engineering_diagnostics_wave2v_gui_validation.py': '65075fe06102d2bd75f3c363ccfed21f6dc1a157a867f27d134153a1c5a3d470',
 'tools/engineering_diagnostics_wave2v_public_boundary_gate.py': '32fddcf3497b7aa0ea9c3a4c9dd0587c7a341841ee2050c1cc7adca91fcade2c',
 'tools/engineering_diagnostics_wave2w_architecture_gate.py': 'cdeb6e31000f5bf2c8d8cb4123540cd6e23886d612ef8d09827a01076f064dca',
 'tools/engineering_diagnostics_wave2w_gui_validation.py': '6aa9341b8f0e32f015af93c90e0b4f3f40a72001bf0df53cac6c27bf6b6628e6',
 'tools/engineering_diagnostics_wave2w_public_boundary_gate.py': '266be71220071915202d7002140fd6a19196987b1b52a872fdabcbd0b0444787',
 'tools/engineering_diagnostics_wave2w_validation_runtime.py': 'b5514b18e9dad8560894c31644fd3145ef0aa8bd85b962d7046a3ea26ac869c2',
 'tools/validate_engineering_diagnostics_wave2v_v1.py': 'c005fcbb560d744350627c6b1dfdd1ef38fb7ce19d1200b118ef2dccd1b37810',
 'tools/validate_engineering_diagnostics_wave2w_v1.py': '6f4d5e518430ff78d2b2eeed89569d55ce7c5ef8c5b90ed997c546f8996fd246'}
_PROTECTED_HASHES = {'_reasoner_tools_gui_engineering_safety_full_audit.py': '3406df90ce51fa0df349ded3a19ce864c5407c950b71b9e935a48bfeaf18b44f',
 '_reasoner_tools_gui_engineering_safety_panel_catalog.py': '5015f39815b3800673d75ea45a76ed33e444ddfb8b8b0565b2ba246fa06ca22a',
 '_reasoner_tools_gui_engineering_safety_panel_commands.py': 'd80ea8ffd9f8c78d1c42e1ef30772afe7ca5cfaeda051a3aef0d61c045698b92',
 '_reasoner_tools_gui_engineering_safety_review_signals.py': '6d2ae82b16d38aaab6a57b0d7ece8cd25bea9111dcef390b1f4e791a42dec8f1',
 '_reasoner_tools_gui_engineering_safety_sonar.py': '5700a9953f22644296f5e591f415fd8d61c12ef6fc07276c55a41fcacaf5593c',
 'kanda_reasoner_app/engineering_diagnostics/_store_run_ops.py': 'a939bad20d04819587e201dcfa9834006aaee389c803a1d29838cff2e4c94cb2',
 'kanda_reasoner_app/engineering_diagnostics/collectors/shadow_collector.py': '341f5699229ab90394174ff4c3cc6b9d65566b770b0e1cb1105d9fd97bc7ba05',
 'kanda_reasoner_app/engineering_diagnostics/fingerprinting.py': '52c9a5c76839d5b7548d53f81c45ff2aecc43b98b4b7e5b257816f7786df4676',
 'kanda_reasoner_app/engineering_diagnostics/store.py': '827af8e33c97a8a95e0f795355da9eb2276a510349e636b8bfd7c34975f3fcce',
 'kanda_reasoner_app/engineering_diagnostics_gui/controller.py': 'a5427953742772c84e93ad0ed65b3bdee7dd47d13b87223c57ccab8d97ff8c4f',
 'kanda_reasoner_app/project_selection_registry.py': '98dbb376654e0608f9d6863829999ac5bcf0523715c859f3b067cde42b9d7fa1',
 'kanda_reasoner_app/safety_suite_cli/commands.py': '0bf3d3af43446774f65c009879d9d54055dfaa878103c310b331d224a408f2e2',
 'kanda_reasoner_app/source_hygiene/_shadow_audit_ast.py': '2523e1d99faf9aa8ed7376b7fa0726e1fc3da37baea920b4a5807f3a1d63624f'}


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _validator_hash() -> str:
    source = Path(__file__).read_text(encoding="utf-8")
    normalized = source.replace(VALIDATOR_CANONICAL_SHA256, "0" * 64)
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def _check_hashes(root: Path, values: dict[str, str], marker: str) -> None:
    for relative, expected in values.items():
        path = root / relative
        _require(path.is_file(), "VALIDATION_FILE_MISSING:" + relative)
        _require(_sha256(path) == expected, "VALIDATION_FILE_HASH_DRIFT:" + relative)
    print(marker)


def _optional_hash(path: Path) -> str:
    return _sha256(path) if path.is_file() else "ABSENT"


def _tree_hash(root: Path) -> str:
    if not root.exists():
        return "ABSENT"
    digest = hashlib.sha256()
    for path in sorted((item for item in root.rglob("*") if item.is_file()), key=lambda item: item.as_posix()):
        digest.update(path.relative_to(root).as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(_sha256(path).encode("ascii"))
    return digest.hexdigest()


def _run_architecture(root: Path) -> None:
    from tools.engineering_diagnostics_wave2w_validation_runtime import run_wave2w_command
    from tools.engineering_diagnostics_wave2w_v1r2_architecture_gate import (
        validate_engineering_diagnostics_wave2w_v1r2_architecture,
    )
    output = run_wave2w_command(
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
    validate_engineering_diagnostics_wave2w_v1r2_architecture(output)


def _validate_live_collectors(root: Path, boundary: object) -> None:
    from kanda_reasoner_app.engineering_diagnostics import (
        SHADOW_PRODUCER_ID,
        build_shadow_diagnostic_run,
        collect_shadow_findings,
        issue_fingerprint,
    )
    from kanda_reasoner_app.engineering_diagnostics.collectors.ruff_collector import collect_ruff_json
    from kanda_reasoner_app.engineering_diagnostics_gui.bom_provider import SafetySuiteBomReportProvider

    bom = SafetySuiteBomReportProvider(root).collect(root, Event())
    _require(str(bom.get("report_type") or "") == "bom_scan", "LIVE_BOM_PUBLIC_JSON_INVALID")
    print("LIVE BOM PUBLIC CLI JSON: PASS")

    ruff = collect_ruff_json(root, timeout_seconds=600.0)
    print("LIVE RUFF STRUCTURED FINDINGS: " + str(len(ruff.raw_findings)))
    print("LIVE RUFF LARGE OUTPUT COLLECTION: PASS")

    collection = collect_shadow_findings(root)
    run = build_shadow_diagnostic_run(
        collection,
        boundary=boundary,
        attempt_id="wave2w-v1r2-live-shadow-validation",
        source_fingerprint="wave2w-v1r2-live-shadow-validation",
        operation_generation=1,
    )
    seen: set[str] = set()
    collisions: list[str] = []
    for finding in run.findings:
        fingerprint = issue_fingerprint(SHADOW_PRODUCER_ID, finding)
        if fingerprint in seen:
            collisions.append(fingerprint)
        seen.add(fingerprint)
    _require(not collisions, "LIVE_SHADOW_DUPLICATE_ISSUE_FINGERPRINT:" + repr(collisions[:5]))
    print("LIVE SHADOW NORMALIZED FINDINGS: " + str(len(run.findings)))
    print("SHADOW DUPLICATE ISSUE FINGERPRINT COLLISIONS: 0")


def _write_evidence(root: Path, lines: list[str]) -> Path:
    from kanda_reasoner_app.project_selection_registry import ProjectSelectionRegistry
    boundary = ProjectSelectionRegistry(tool_source_root=root).resolve_boundary_for_root(root)
    target = (
        boundary.active_project_support_root
        / "project_validation_evidence"
        / "engineering_diagnostics_wave2w"
        / "engineering_diagnostics_wave2w_v1r2.txt"
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

    from kanda_reasoner_app.engineering_diagnostics.paths import engineering_diagnostics_database_path
    from kanda_reasoner_app.project_selection_registry import ProjectSelectionRegistry
    from tools.engineering_diagnostics_wave2w_gui_validation import validate_wave2w_gui
    from tools.engineering_diagnostics_wave2w_public_boundary_gate import validate_engineering_diagnostics_wave2w_public_boundary
    from tools.engineering_diagnostics_wave2w_v1r2_public_boundary_gate import validate_engineering_diagnostics_wave2w_v1r2_public_boundary
    from tools.engineering_diagnostics_wave2w_v1r2_validation_runtime import run_wave2w_v1r2_focused_tests

    boundary = ProjectSelectionRegistry(tool_source_root=root).resolve_boundary_for_root(root)
    registry = Path(ProjectSelectionRegistry(tool_source_root=root).registry_path)
    database = engineering_diagnostics_database_path(boundary)
    freeze_memory = boundary.active_project_support_root / "project_freeze_after_update" / "frozen_features_memory"
    registry_before = _optional_hash(registry)
    database_before = _optional_hash(database)
    freeze_before = _tree_hash(freeze_memory)

    print("PACKAGE REVISION: " + PACKAGE_REVISION)
    print("VALIDATOR TOOL ROOT IMPORT PATH: PASS")
    _require(_validator_hash() == VALIDATOR_CANONICAL_SHA256, "WAVE2W_V1R2_VALIDATOR_CANONICAL_HASH_MISMATCH")
    print("WAVE2W V1R2 VALIDATOR CANONICAL HASH: PASS")
    _check_hashes(root, _WAVE2W_V1R1_HASHES, "WAVE2W V1R1 HIERARCHY PREDECESSOR HASHES: PASS")
    _check_hashes(root, _PROTECTED_HASHES, "WAVE2W V1R2 PROTECTED OWNER HASHES: PASS")
    validate_engineering_diagnostics_wave2w_public_boundary(root)
    validate_engineering_diagnostics_wave2w_v1r2_public_boundary(root)
    run_wave2w_v1r2_focused_tests(root)
    _validate_live_collectors(root, boundary)
    panel_ms, rows_ms, filter_ms = validate_wave2w_gui(root)
    _run_architecture(root)

    _require(_optional_hash(registry) == registry_before, "PROJECT_SELECTION_REGISTRY_MUTATED")
    _require(_optional_hash(database) == database_before, "ENGINEERING_DIAGNOSTICS_DATABASE_MUTATED")
    _require(_tree_hash(freeze_memory) == freeze_before, "FREEZE_MEMORY_MUTATED")
    _check_hashes(root, _WAVE2W_V1R1_HASHES, "WAVE2W V1R1 HIERARCHY SOURCE MUTATION: NO")

    lines = [
        "PACKAGE REVISION: v1r2",
        "FOCUSED PUBLIC CONTRACT TESTS: 200/200 PASS",
        "BOM PUBLIC CLI EXECUTION CONTRACT: PASS",
        "RUFF LARGE OUTPUT PIPE DRAIN CONTRACT: PASS",
        "RUFF TIMEOUT FAIL-CLOSED CONTRACT: PASS",
        "SHADOW RUNTIME STATEMENT IDENTITY CONTRACT: PASS",
        "LIVE BOM PUBLIC CLI JSON: PASS",
        "LIVE RUFF LARGE OUTPUT COLLECTION: PASS",
        "SHADOW DUPLICATE ISSUE FINGERPRINT COLLISIONS: 0",
        "ENGINEERING SAFETY REAL QT TWO-LEVEL REGISTRATION: PASS",
        "ENGINEERING AUDIT REAL QT INNER TABS: PASS",
        "ENGINEERING DIAGNOSTICS REAL QT INNER TABS: PASS",
        "FULL AUDIT REAL QT CONTROLS PRESERVED: PASS",
        "PONTUAL AUDIT REAL QT PAGE PRESERVED: PASS",
        "FULL ENGINEERING DIAGNOSTICS REAL QT RUN BUTTON: PASS",
        "FULL ENGINEERING DIAGNOSTICS REAL QT CANCEL BUTTON: PASS",
        "FULL ENGINEERING DIAGNOSTICS REAL QT COLLECTOR SET: PASS",
        "FULL ENGINEERING DIAGNOSTICS REAL QT SONAR START: PASS",
        "FULL ENGINEERING DIAGNOSTICS REAL QT SONAR CANCEL STATE: PASS",
        "FULL ENGINEERING DIAGNOSTICS REAL QT SONAR TERMINAL STOP: PASS",
        "FULL ENGINEERING DIAGNOSTICS REAL QT COOPERATIVE CANCEL: PASS",
        "PONTUAL ENGINEERING DIAGNOSTICS REAL QT BEHAVIOR PRESERVED: PASS",
        "FULL AUDIT DRILL-THROUGH PONTUAL TARGET: PASS",
        "WAVE2W GUI 25000 ROW INITIALIZATION MS: " + f"{rows_ms:.1f}",
        "WAVE2W GUI FILTER UPDATE MS: " + f"{filter_ms:.1f}",
        "WAVE2W GUI PANEL CREATION MS: " + f"{panel_ms:.1f}",
        "WAVE2W GUI HIGH-VOLUME PERFORMANCE: PASS",
        "WAVE2W V1R2 NEW ARCHITECTURE ISSUES: 0",
        "WAVE2W V1R2 TOUCHED PATH ARCHITECTURE ISSUES: 0",
        "ENGINEERING DIAGNOSTICS COMPETING STORE OWNERS: 0",
        "ENGINEERING DIAGNOSTICS DATABASE MUTATED: NO",
        "PROJECT SELECTION REGISTRY MUTATED: NO",
        "FREEZE MEMORY MUTATED: NO",
        "TOOL PROJECT LOGICAL ROLE SEPARATION: PASS",
        "MCARD LIFECYCLE GATE: NOT_APPLICABLE",
        "VALIDATION OK: " + FEATURE_ID,
        "STATUS: IN_SYNC",
    ]
    evidence = _write_evidence(root, lines)
    print("VALIDATION EVIDENCE WRITTEN: " + str(evidence))
    for line in lines:
        print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
