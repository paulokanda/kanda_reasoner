# project-path: tools/validate_engineering_diagnostics_wave2qa_v1.py
"""Brick Wall validator for Engineering Diagnostics Wave 2Q-A."""

from __future__ import annotations

import argparse
import hashlib
import os
from pathlib import Path
import sys

FEATURE_ID = "kanda-reasoner-engineering-diagnostics-grouping-wave2qa-v1"
PACKAGE_REVISION = "v1r3"
VALIDATOR_CANONICAL_SHA256 = "227462fbb4dd56e125deb190f3efdaa1f029f1fc8121a4f0c8ee258dfe482708"
_INSTALLED_HASHES: dict[str, str] = {
    'kanda_reasoner_app/engineering_diagnostics/__init__.py': '0e3c8808e9fcf0bdf81273a3e9d26aef5bab0ae299c15fdb2aa4e2bc38f4b544',
    'kanda_reasoner_app/engineering_diagnostics/_store_database.py': 'c13fd012a5f7cb59d48ee7b0ea81c7d34cce53677a523e17112d86fcc34fa505',
    'kanda_reasoner_app/engineering_diagnostics/_store_grouping_ops.py': 'da190986a4cf7c6c198dfd506099c489e97f58146ddaf612121f4fddfa72a5b9',
    'kanda_reasoner_app/engineering_diagnostics/_store_grouping_schema.py': 'b312bf22bfa20bafc643f11135c52c1660e2d633cbf5708d1fea8387baeab4db',
    'kanda_reasoner_app/engineering_diagnostics/_store_grouping_state.py': '1369ab62b62b34d8a218c3a20068e6d6ef2a27686f2f0a76a5d3c5ee63364232',
    'kanda_reasoner_app/engineering_diagnostics/grouping.py': '651a9055ba7b24f840df1153994f37464ac0187ccf629af5917b56dc44cb9b8d',
    'kanda_reasoner_app/engineering_diagnostics/grouping_models.py': 'ef927f4ee4683323f4258413be9d9a703a208bb3660e3bf8cbb45f2d52a3f00b',
    'kanda_reasoner_app/engineering_diagnostics/store.py': '0cc6a6100b2e98228301a3d1790e48e78c550dec01191abc218f3e6b0b072e29',
    'kanda_reasoner_app/engineering_diagnostics_gui/controller.py': 'a652947dbbd39a5489c744cce94d1577f8c555cee7f00d36dd52869d158c7d58',
    'kanda_reasoner_app/engineering_diagnostics_gui/diagnostic_table_model.py': '64640a38eaff0de4f3949aad12a8abf682da465cfbc202ed36a69ec192141d24',
    'kanda_reasoner_app/engineering_diagnostics_gui/engineering_diagnostics_tab.py': 'f6a81f510139607d996ca785d3e2e8b6714be70cc806ae6078475bc047afd40d',
    'kanda_reasoner_app/engineering_diagnostics_gui/grouping_ui.py': '1da871eeb0c1d7d19158d016196d56ccc058d89c0a2ca7b668e0f5f5abdd1287',
    'kanda_reasoner_app/engineering_diagnostics_gui/models.py': 'c278091a994b7036d37bd87588a26bac486462521d01f0acaa7fa221c7a93476',
    'kanda_reasoner_app/engineering_diagnostics_gui/owner_ui.py': 'ea79b9b61a8c9228256dc9417f085774c84658f448b3d26d82657a6f39c9bc16',
    'kanda_reasoner_app/engineering_diagnostics_gui/table_columns.py': '0899366f3e455f1a09cd1eede4e068c921fea7d4f764e6ab83ba79dba10032bc',
    'kanda_reasoner_app/engineering_diagnostics_gui/wave2qa_validation.py': 'fe6ddf1d070018d293eb8cbec005a2f8111593c2c0cf24d25f3fb45c62ec17d6',
    'tests/test_engineering_diagnostics_wave2qa.py': '11b1cc24cea82691e90d9bd0c520496f040fe5d98c652f73a204234ea53c3c66',
    'tests/test_engineering_diagnostics_wave2qa_gui_scale.py': '5714ca17296f842c895d251e8463d13a2d1e9bfe2cc13bcd53f2c54609e3ea66',
    'tools/engineering_diagnostics_wave2qa_architecture_gate.py': 'f302a75f1158d82fa8e6678b44822a185912b4a6232d4576f135fa63fb4389aa',
    'tools/engineering_diagnostics_wave2qa_fixture_support.py': '4affbdf195785ce7b3bec08a5676e1c4a3a88c78f82550e1fd48dc672bdaaa10',
    'tools/engineering_diagnostics_wave2qa_public_boundary_gate.py': '88c0458e0bb144ad03cea1b4c883768dcb02d72d6ac3a80409542cfc5707f407',
    'tools/engineering_diagnostics_wave2qa_validation_runtime.py': '6ec83a2c430e8435e81c433e570def5b404a5e22d0c479fb65a0cd00dcd896b1',
}
_PROTECTED_HASHES: dict[str, str] = {
    'kanda_reasoner_app/engineering_diagnostics/baseline.py': '5a4806826572c9334e034818f88ec3517d4c684a4338ab76f0cb57047695da3e',
    'kanda_reasoner_app/engineering_diagnostics/enrichment.py': '6fb18f70cad172db542908f7f3d9484c902328e69026dd3c4df7e48899f6c524',
    'kanda_reasoner_app/engineering_diagnostics/enrichment_models.py': '806ff2124f91d100c534046b3a4aad1f6c965f17f8c9974e2226c455729d9acd',
    'kanda_reasoner_app/engineering_diagnostics/fingerprinting.py': '52c9a5c76839d5b7548d53f81c45ff2aecc43b98b4b7e5b257816f7786df4676',
    'kanda_reasoner_app/engineering_diagnostics/models.py': '2053c3dfcaa8d08939d99626c9b18a1d1d887bc24a163d974db36dc93d7d2184',
    'kanda_reasoner_app/engineering_diagnostics/owner_enrichment.py': 'a962caa1cdcfc29120b6e151768e3d23f88a10cafe900afc1bde11a6fb2718ae',
    'kanda_reasoner_app/engineering_diagnostics/owner_enrichment_models.py': 'ff3b6aadd3576ae3d63343c548226ce34d41f114601edce7f18f159fe2e62d8d',
    'kanda_reasoner_app/reasoner_symbol_atlas/__init__.py': '9fae48b6bbb357b67c0aa2a683ef1e9ccad04f37048c5997f3860757bf6c1af7',
    'kanda_reasoner_app/reasoner_symbol_atlas/existing_code_finder.py': '77387d6c6b8d3fca0aa067fe6a456d3f567c32f07bf4b1d8cb71e8c05a22ed5a',
    'kanda_reasoner_app/reasoner_symbol_atlas/owner_classifier.py': '8e806e5751420885b3ce8fd90ddd6e7d1b2d51fbef31775d3ff8b1db7b7e6266',
    'kanda_reasoner_app/reasoner_symbol_atlas/output_policy.py': '63eb29a659782ae56c57be513ea69987bbd2321fb0edc3c6b6bc1bf7ddfeb14c',
    'tests/test_engineering_diagnostics_wave2pb.py': '99e15e47605ab76b27351b327c4276046b6334cefe14b5134e55104e3ff3ae84',
    'tools/engineering_diagnostics_wave2pb_architecture_gate.py': '3d591b6dc43b8da7836bad8983311c1a4ceb606f9aa91301ebb567e6921e8922',
    'tools/engineering_diagnostics_wave2pb_public_boundary_gate.py': 'ee1f5082551427a06c78eff36b424b1c68202a4323a0afb34261e267a2419735',
    'tools/validate_engineering_diagnostics_wave2pb_v1r1.py': 'c899aaaced7efe60df22bf6eadbb0f7546d8676d917e781e84081555da8285b4',
    'tools/validate_engineering_diagnostics_wave2oa_v1.py': '88aaea82f2f5230744945088b20e7dc251173236aace685e87aa7ada54218b45',
    'tools/validate_engineering_diagnostics_wave2ob_v1.py': 'd27b9b83c75381991e60636ac2d4807645e4ccc245b5b0ee86acb2aa3ea25cc2',
    'tools/validate_engineering_diagnostics_wave2oc_v1.py': '8f8177fc87268a8e5c8d5e3da1ec101e5ecf1d4b88c88b840d17be7bd7436c67',
    'tools/validate_engineering_diagnostics_wave2od_v1.py': '8f92d3d927561052ea121abac6d9d2d371b91f7e0f2050ea0f0fd52a531e0412',
    'tools/validate_engineering_diagnostics_wave2pa_v1.py': 'be9595ad0685da176e6be6fc6871d974feb0eefc03239359f5c28e9b55c00332',
    'tools/validate_reasoner_symbol_atlas_active_owner_filtering_wave2n_v1r2.py': '3636ab0616a5ac4112a137e6d7f167584859cb9f9ce1f8e5e7c6643fa6251e2a',
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
        _require(
            _sha256(path) == digest,
            "VALIDATED_FILE_HASH_MISMATCH:" + relative,
        )
    print(marker)


def _validator_hash() -> str:
    source = Path(__file__).read_text(encoding="utf-8")
    canonical = source.replace(
        'VALIDATOR_CANONICAL_SHA256 = "' + VALIDATOR_CANONICAL_SHA256 + '"',
        'VALIDATOR_CANONICAL_SHA256 = "' + ("0" * 64) + '"',
        1,
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _validate_disposable_boundary_fixture(root: Path) -> None:
    fixture = (
        root
        / "tools"
        / "engineering_diagnostics_wave2qa_fixture_support.py"
    ).read_text(encoding="utf-8")
    required = (
        "wave2qa_disposable_boundary_fixture",
        "canonical_project_support_root",
        "canonical_transient_garbage_root",
        "PORTABLE_SMOKE_ENABLED_ENV",
        "PORTABLE_SMOKE_ROOT_ENV",
        "PORTABLE_SMOKE_TOKEN_ENV",
        "patch.dict(os.environ, environment, clear=False)",
        "WAVE2QA_FIXTURE_SUPPORT_ROOT_MISMATCH",
        "WAVE2QA_FIXTURE_DAILY_ROOT_MISMATCH",
    )
    for token in required:
        _require(token in fixture, "WAVE2QA_FIXTURE_CONTRACT_MISSING:" + token)
    _require(
        'root.parent / (root.name + "_show_project_to_AI")' not in fixture,
        "WAVE2QA_NONCANONICAL_SUPPORT_ROOT_HEURISTIC_PRESENT",
    )
    print("WAVE2QA WINDOWS CANONICAL SUPPORT FIXTURE: PASS")


def _validate_gui_scale_disposable_fixture(root: Path) -> None:
    test_source = (
        root / "tests" / "test_engineering_diagnostics_wave2qa_gui_scale.py"
    ).read_text(encoding="utf-8")
    _require(
        "wave2qa_disposable_boundary_fixture" in test_source,
        "WAVE2QA_GUI_SCALE_DISPOSABLE_FIXTURE_MISSING",
    )
    _require(
        "wave2qa_boundary_fixture" not in test_source,
        "WAVE2QA_GUI_SCALE_DIRECT_BOUNDARY_FIXTURE_PRESENT",
    )
    _require(
        "tempfile.TemporaryDirectory" not in test_source,
        "WAVE2QA_GUI_SCALE_RAW_TEMPORARY_DIRECTORY_PRESENT",
    )
    _require(
        test_source.count("with wave2qa_disposable_boundary_fixture() as boundary:")
        == 3,
        "WAVE2QA_GUI_SCALE_DISPOSABLE_FIXTURE_COUNT_INVALID",
    )
    _require(
        "from contextlib import closing" in test_source,
        "WAVE2QA_SQLITE_CLOSING_IMPORT_MISSING",
    )
    _require(
        "with sqlite3.connect(" not in test_source,
        "WAVE2QA_SQLITE_TRANSACTION_CONTEXT_USED_AS_LIFETIME_OWNER",
    )
    _require(
        test_source.count("with closing(sqlite3.connect(") == 5,
        "WAVE2QA_SQLITE_CLOSING_COUNT_INVALID",
    )
    print("WAVE2QA GUI-SCALE DISPOSABLE DATABASE FIXTURE: PASS")
    print("WAVE2QA SQLITE TEST CONNECTION DETERMINISTIC CLOSE: PASS")


def _validate_sqlite_connection_closure_runtime(root: Path) -> None:
    from tools.engineering_diagnostics_wave2qa_validation_runtime import (
        run_wave2qa_command,
    )

    run_wave2qa_command(
        [
            sys.executable,
            "-W",
            "error::ResourceWarning",
            "-m",
            "unittest",
            "-v",
            "tests.test_engineering_diagnostics_wave2qa_gui_scale",
        ],
        cwd=root,
        markers=("Ran 7 tests", "OK"),
    )
    print("WAVE2QA SQLITE RESOURCEWARNING VALIDATION: PASS")


def _run_architecture(root: Path) -> None:
    from tools.engineering_diagnostics_wave2qa_architecture_gate import (
        validate_engineering_diagnostics_wave2qa_architecture_non_regression,
    )
    from tools.engineering_diagnostics_wave2qa_validation_runtime import (
        run_wave2qa_command,
    )

    output = run_wave2qa_command(
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
    validate_engineering_diagnostics_wave2qa_architecture_non_regression(output)


def _write_evidence(root: Path, lines: list[str]) -> Path:
    from kanda_reasoner_app.project_selection_registry import ProjectSelectionRegistry

    boundary = ProjectSelectionRegistry(
        tool_source_root=root
    ).resolve_boundary_for_root(root)
    target = (
        boundary.active_project_support_root
        / "project_validation_evidence"
        / "engineering_diagnostics_wave2qa"
        / "engineering_diagnostics_wave2qa_v1r3.txt"
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

    from tools.engineering_diagnostics_wave2qa_public_boundary_gate import (
        validate_engineering_diagnostics_wave2qa_public_boundary,
    )
    from tools.engineering_diagnostics_wave2qa_validation_runtime import (
        run_wave2qa_focused_tests,
        validate_wave2qa_deterministic_read_only,
        validate_wave2qa_manual_grouping_disposable,
    )
    from kanda_reasoner_app.engineering_diagnostics_gui.wave2qa_validation import (
        validate_wave2qa_gui,
    )

    print("PACKAGE REVISION: " + PACKAGE_REVISION)
    print("VALIDATOR TOOL ROOT IMPORT PATH: PASS")
    _require(
        _validator_hash() == VALIDATOR_CANONICAL_SHA256,
        "WAVE2QA_VALIDATOR_CANONICAL_HASH_MISMATCH",
    )
    print("WAVE2QA VALIDATOR CANONICAL HASH: PASS")
    _validate_disposable_boundary_fixture(root)
    _validate_gui_scale_disposable_fixture(root)
    _validate_sqlite_connection_closure_runtime(root)
    _check_hashes(root, _INSTALLED_HASHES, "WAVE2QA INSTALLED HASHES: PASS")
    _check_hashes(
        root,
        _PROTECTED_HASHES,
        "WAVE2N THROUGH WAVE2PB PROTECTED HASHES: PASS",
    )
    validate_engineering_diagnostics_wave2qa_public_boundary(root)
    run_wave2qa_focused_tests(root)
    validate_wave2qa_deterministic_read_only(root)
    validate_wave2qa_manual_grouping_disposable(root)
    panel_ms, rows_ms, filter_ms = validate_wave2qa_gui(root)
    _run_architecture(root)

    lines = [
        "PACKAGE REVISION: " + PACKAGE_REVISION,
        "FOCUSED PUBLIC CONTRACT TESTS: 91/91 PASS",
        "WAVE2QA WINDOWS CANONICAL SUPPORT FIXTURE: PASS",
        "WAVE2QA GUI-SCALE DISPOSABLE DATABASE FIXTURE: PASS",
        "WAVE2QA SQLITE TEST CONNECTION DETERMINISTIC CLOSE: PASS",
        "WAVE2QA SQLITE RESOURCEWARNING VALIDATION: PASS",
        "WAVE2QA DETERMINISTIC GROUPING: PASS",
        "WAVE2QA MANUAL GROUPING DISPOSABLE STATE: PASS",
        "WAVE2QA APPEND-ONLY DECISION HISTORY: PASS",
        "WAVE2QA STALE GENERATION REJECTION: PASS",
        "WAVE2QA FINDING AND SCAN IDENTITIES MODIFIED: NO",
        "WAVE2QA LIVE DIAGNOSTIC DATABASE MUTATED: NO",
        "WAVE2QA LIVE FREEZE MEMORY MUTATED: NO",
        "WAVE2QA GUI 25000 ROW INITIALIZATION MS: " + f"{rows_ms:.1f}",
        "WAVE2QA GUI FILTER UPDATE MS: " + f"{filter_ms:.1f}",
        "WAVE2QA GUI PANEL CREATION MS: " + f"{panel_ms:.1f}",
        "WAVE2QA GUI HIGH-VOLUME PERFORMANCE: PASS",
        "WAVE2QA NEW ARCHITECTURE ISSUES: 0",
        "WAVE2QA TOUCHED PATH ARCHITECTURE ISSUES: 0",
        "PROJECT SELECTION REGISTRY MUTATED: NO",
        "TOOL PROJECT LOGICAL ROLE SEPARATION: PASS",
        "MCARD LIFECYCLE GATE: NOT_APPLICABLE",
        "VALIDATION OK: " + FEATURE_ID,
        "STATUS: IN_SYNC",
    ]
    evidence = _write_evidence(root, lines)
    print("VALIDATION EVIDENCE WRITTEN: " + str(evidence))
    for line in lines[-5:]:
        print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
