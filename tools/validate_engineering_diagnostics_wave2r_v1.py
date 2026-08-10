# project-path: tools/validate_engineering_diagnostics_wave2r_v1.py
"""Brick Wall validator for Engineering Diagnostics Wave 2R."""

from __future__ import annotations

import argparse
import hashlib
import os
from pathlib import Path
import sys

FEATURE_ID = "kanda-reasoner-engineering-diagnostics-lifecycle-governance-wave2r-v1"
PACKAGE_REVISION = "v1"
VALIDATOR_CANONICAL_SHA256 = "b7fff8cbfa6e44b0616bccf9c3e03e160e79b158a12557f629d9bf74412be04c"
_INSTALLED_HASHES: dict[str, str] = {
    'kanda_reasoner_app/engineering_diagnostics/__init__.py': 'd6e72e0126755eca6a4c28be05b517387ed8c12b27c2c7d827ba5c3a5d770cb1',
    'kanda_reasoner_app/engineering_diagnostics/_store_database.py': '3d440f58872f301d6ed9df4b78b6d16f80d034a35f673d569c9a5f513dd1e6d6',
    'kanda_reasoner_app/engineering_diagnostics/_store_lifecycle_ops.py': '8598e9b8f3381364669cf9669e5dac5acc19e4eaba3b2140ae595c8327d8171f',
    'kanda_reasoner_app/engineering_diagnostics/_store_lifecycle_schema.py': '3d107a4eb93ef71977cb75b84296523f08bded2b37a756cb691590f06f8b9745',
    'kanda_reasoner_app/engineering_diagnostics/_store_lifecycle_state.py': '0855b03fc266ee374f45ed86b8ef8e5b5533bcc5d1c3ec4a342ee3d4c0decc7e',
    'kanda_reasoner_app/engineering_diagnostics/_store_run_ops.py': 'a939bad20d04819587e201dcfa9834006aaee389c803a1d29838cff2e4c94cb2',
    'kanda_reasoner_app/engineering_diagnostics/lifecycle.py': '9e6b2c6133c9b27374f7763133cd859c76ed8a16506faa74136ce41bc93a3e74',
    'kanda_reasoner_app/engineering_diagnostics/lifecycle_models.py': '409779b3e7c7d4be3be2dd600b07478cb453d4a33b77e15ae86dc9a59f713d6b',
    'kanda_reasoner_app/engineering_diagnostics/store.py': '827af8e33c97a8a95e0f795355da9eb2276a510349e636b8bfd7c34975f3fcce',
    'kanda_reasoner_app/engineering_diagnostics_gui/controller.py': '7b260f5ee02887ed09428e684c893bcf4d82da02de202f577b1db105823f77a9',
    'kanda_reasoner_app/engineering_diagnostics_gui/diagnostic_table_model.py': '0d402353aad2a9d3be1a876f4a2a3852cda959491b5dc08745e6fedcf306f3f6',
    'kanda_reasoner_app/engineering_diagnostics_gui/engineering_diagnostics_tab.py': '6860e85d1af26ce18aacdfa4257977a4e76b6f631b636fd1aed26744352ec8f2',
    'kanda_reasoner_app/engineering_diagnostics_gui/finding_view_builder.py': 'e15f3b13ff14184bf2e15719a51546482f1bdbad9b1cf01baf567e06d933bfe8',
    'kanda_reasoner_app/engineering_diagnostics_gui/lifecycle_ui.py': 'a3cd0c5f2381ab718157f8d0557b6e6f60d43e63d57aaa0efee0b7aae38a23fb',
    'kanda_reasoner_app/engineering_diagnostics_gui/models.py': 'de2ad0f08be5465ab00e39fd3c749cfa66628f595f747d08544c3db7bca4afab',
    'kanda_reasoner_app/engineering_diagnostics_gui/owner_ui.py': 'fb3add7aaebba2c604850399c07820634e3ace39cd01d2f37b0e701772785b99',
    'kanda_reasoner_app/engineering_diagnostics_gui/run_summary.py': '5015f752c7037b53ebf2074e7f87c9378abefea95dac6f352e8e88350c496c6a',
    'kanda_reasoner_app/engineering_diagnostics_gui/table_columns.py': 'cc4d671c225f6518b522118a7c413adecad0b70a5f4f0b633663a6815e7a9816',
    'kanda_reasoner_app/engineering_diagnostics_gui/wave2r_validation.py': 'cb5899dc580ab5e81b857e26916f9a0920410f74ec178d18d03459e31febfdd2',
    'tests/test_engineering_diagnostics_wave2r.py': '84dc327e6df3fde51e7831becf5c66fc1ad28a200c876dabd9e25dd0d3954bd6',
    'tests/test_engineering_diagnostics_wave2r_gui_scale.py': 'db561e36ae142cc7e62a63e1dae0e11dadb1abe53cf788885ec47403890a8ba3',
    'tools/engineering_diagnostics_wave2r_architecture_gate.py': '53f77fbcae54c52143af4b1a5f7ac4ec36ea07305814ca60db79701009e41ac5',
    'tools/engineering_diagnostics_wave2r_public_boundary_gate.py': '3bb9248c738cb5272f6092f30700381b0e35bae51e9edf22f9f0e1fd8331487f',
    'tools/engineering_diagnostics_wave2r_validation_runtime.py': '40a707350a29ced9bb0e3f00639d8bebb08417e33260c39c293a92aa04d6923c',
}
_PROTECTED_HASHES: dict[str, str] = {
    'kanda_reasoner_app/engineering_diagnostics/_store_grouping_ops.py': 'da190986a4cf7c6c198dfd506099c489e97f58146ddaf612121f4fddfa72a5b9',
    'kanda_reasoner_app/engineering_diagnostics/_store_grouping_schema.py': 'b312bf22bfa20bafc643f11135c52c1660e2d633cbf5708d1fea8387baeab4db',
    'kanda_reasoner_app/engineering_diagnostics/_store_grouping_state.py': '1369ab62b62b34d8a218c3a20068e6d6ef2a27686f2f0a76a5d3c5ee63364232',
    'kanda_reasoner_app/engineering_diagnostics/baseline.py': '5a4806826572c9334e034818f88ec3517d4c684a4338ab76f0cb57047695da3e',
    'kanda_reasoner_app/engineering_diagnostics/collectors/__init__.py': '3ec5d7f16b6f802efa31a9e28cce2f122bfa9b274922dfafe40df0041ac1c6a9',
    'kanda_reasoner_app/engineering_diagnostics/collectors/shadow_collector.py': '341f5699229ab90394174ff4c3cc6b9d65566b770b0e1cb1105d9fd97bc7ba05',
    'kanda_reasoner_app/engineering_diagnostics/collectors/shadow_normalizer.py': '3da8039849793a7368e3c599ddd33481ad5c84137c02e686444950b006cfe337',
    'kanda_reasoner_app/engineering_diagnostics/enrichment.py': '6fb18f70cad172db542908f7f3d9484c902328e69026dd3c4df7e48899f6c524',
    'kanda_reasoner_app/engineering_diagnostics/enrichment_models.py': '806ff2124f91d100c534046b3a4aad1f6c965f17f8c9974e2226c455729d9acd',
    'kanda_reasoner_app/engineering_diagnostics/fingerprinting.py': '52c9a5c76839d5b7548d53f81c45ff2aecc43b98b4b7e5b257816f7786df4676',
    'kanda_reasoner_app/engineering_diagnostics/grouping.py': '8d033efa3b2fe83994e831612e563e7a8260a2db3593ba250a42c84be0c18666',
    'kanda_reasoner_app/engineering_diagnostics/grouping_models.py': 'ef927f4ee4683323f4258413be9d9a703a208bb3660e3bf8cbb45f2d52a3f00b',
    'kanda_reasoner_app/engineering_diagnostics/models.py': '2053c3dfcaa8d08939d99626c9b18a1d1d887bc24a163d974db36dc93d7d2184',
    'kanda_reasoner_app/engineering_diagnostics/owner_enrichment.py': 'a962caa1cdcfc29120b6e151768e3d23f88a10cafe900afc1bde11a6fb2718ae',
    'kanda_reasoner_app/engineering_diagnostics/owner_enrichment_models.py': 'ff3b6aadd3576ae3d63343c548226ce34d41f114601edce7f18f159fe2e62d8d',
    'kanda_reasoner_app/engineering_diagnostics/shadow_relational_grouping.py': 'bd6e696b13bbd6f94c3033874089fea03755e42f3c84082936a49bb2f0f27a22',
    'kanda_reasoner_app/engineering_diagnostics/shadow_relational_models.py': '2b225f044956e71ddf2004047978922bd14576b40af55959441ad84db96012d0',
    'kanda_reasoner_app/engineering_diagnostics_gui/grouping_ui.py': '1da871eeb0c1d7d19158d016196d56ccc058d89c0a2ca7b668e0f5f5abdd1287',
    'kanda_reasoner_app/engineering_diagnostics_gui/shadow_controller.py': '4ad4a672c47e4727dfdaaeedf27c5c458f1adce8b3d248e3c2d3a0879133bc21',
    'kanda_reasoner_app/engineering_diagnostics_gui/wave2qa_validation.py': 'fe6ddf1d070018d293eb8cbec005a2f8111593c2c0cf24d25f3fb45c62ec17d6',
    'kanda_reasoner_app/engineering_diagnostics_gui/wave2qb_validation.py': '108811beb50201066b2f44b122e887bfb0feffa861709e7d865c7847e58144d8',
    'kanda_reasoner_app/project_selection_registry.py': '98dbb376654e0608f9d6863829999ac5bcf0523715c859f3b067cde42b9d7fa1',
    'kanda_reasoner_app/reasoner_symbol_atlas/__init__.py': '9fae48b6bbb357b67c0aa2a683ef1e9ccad04f37048c5997f3860757bf6c1af7',
    'kanda_reasoner_app/reasoner_symbol_atlas/existing_code_finder.py': '77387d6c6b8d3fca0aa067fe6a456d3f567c32f07bf4b1d8cb71e8c05a22ed5a',
    'kanda_reasoner_app/reasoner_symbol_atlas/output_policy.py': '63eb29a659782ae56c57be513ea69987bbd2321fb0edc3c6b6bc1bf7ddfeb14c',
    'kanda_reasoner_app/reasoner_symbol_atlas/owner_classifier.py': '8e806e5751420885b3ce8fd90ddd6e7d1b2d51fbef31775d3ff8b1db7b7e6266',
    'kanda_reasoner_app/source_hygiene/_active_scope.py': 'ecc7017f6f7607f34fb5bb7e513d1fe2a59fea50878c5bc1ac1efa5a92087c44',
    'kanda_reasoner_app/source_hygiene/_shadow_audit_ast.py': '2523e1d99faf9aa8ed7376b7fa0726e1fc3da37baea920b4a5807f3a1d63624f',
    'kanda_reasoner_app/source_hygiene/shadow_audit.py': 'cdf5efc3717c0a29365467f65eda914ad86df93d7c9feb6f25f3a251835fa91f',
    'tests/test_engineering_diagnostics_wave2qa.py': '11b1cc24cea82691e90d9bd0c520496f040fe5d98c652f73a204234ea53c3c66',
    'tests/test_engineering_diagnostics_wave2qa_gui_scale.py': '5714ca17296f842c895d251e8463d13a2d1e9bfe2cc13bcd53f2c54609e3ea66',
    'tests/test_engineering_diagnostics_wave2qb.py': '62564355446659e653fcf5cda2bf0166862c7c8358305f6d3e2897cd213fb024',
    'tests/test_engineering_diagnostics_wave2qb_gui_scale.py': '7c94327dd030a247025e7156801f8917522510bbd3c85fe235c1cd27f5b5c2dd',
    'tools/engineering_diagnostics_wave2qa_architecture_gate.py': 'f302a75f1158d82fa8e6678b44822a185912b4a6232d4576f135fa63fb4389aa',
    'tools/engineering_diagnostics_wave2qa_fixture_support.py': '4affbdf195785ce7b3bec08a5676e1c4a3a88c78f82550e1fd48dc672bdaaa10',
    'tools/engineering_diagnostics_wave2qa_public_boundary_gate.py': '88c0458e0bb144ad03cea1b4c883768dcb02d72d6ac3a80409542cfc5707f407',
    'tools/engineering_diagnostics_wave2qa_validation_runtime.py': '6ec83a2c430e8435e81c433e570def5b404a5e22d0c479fb65a0cd00dcd896b1',
    'tools/engineering_diagnostics_wave2qb_architecture_gate.py': 'f7678bb9fe70ff487dc3f66ffe3d6b64f33ec759fab00e24433f04d4aab98adc',
    'tools/engineering_diagnostics_wave2qb_public_boundary_gate.py': '26c9845844e6b4a46fce2cdb970636ac43f6ebbde4a035242b1ba8271f5b67e9',
    'tools/engineering_diagnostics_wave2qb_validation_runtime.py': '9900cfdb8d4c0390f7a852df065779cb5e53357e6def2597cca7028c33630b76',
    'tools/validate_engineering_diagnostics_wave2qa_v1.py': '2c10118ef159d4821c019bf5f714e8acb7c86979adcadb359e4c10dcb8bf20d3',
    'tools/validate_engineering_diagnostics_wave2qb_v1.py': 'befe618c8ac0efd1adc02b787ddf030418918688f5e4bef68fe7c984f45f8193',
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
    for member in sorted(item for item in path.rglob("*") if item.is_file()):
        digest.update(member.relative_to(path).as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(_sha256(member).encode("ascii"))
        digest.update(b"\n")
    return digest.hexdigest()


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


def _run_architecture(root: Path) -> None:
    from tools.engineering_diagnostics_wave2r_architecture_gate import (
        validate_engineering_diagnostics_wave2r_architecture_non_regression,
    )
    from tools.engineering_diagnostics_wave2r_validation_runtime import (
        run_wave2r_command,
    )

    output = run_wave2r_command(
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
    validate_engineering_diagnostics_wave2r_architecture_non_regression(output)


def _write_evidence(root: Path, lines: list[str]) -> Path:
    from kanda_reasoner_app.project_selection_registry import ProjectSelectionRegistry

    boundary = ProjectSelectionRegistry(tool_source_root=root).resolve_boundary_for_root(root)
    target = (
        boundary.active_project_support_root
        / "project_validation_evidence"
        / "engineering_diagnostics_wave2r"
        / "engineering_diagnostics_wave2r_v1.txt"
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

    from kanda_reasoner_app.engineering_diagnostics.paths import (
        engineering_diagnostics_database_path,
    )
    from kanda_reasoner_app.engineering_diagnostics_gui.wave2r_validation import (
        validate_wave2r_gui,
    )
    from kanda_reasoner_app.project_selection_registry import ProjectSelectionRegistry
    from tools.engineering_diagnostics_wave2r_public_boundary_gate import (
        validate_engineering_diagnostics_wave2r_public_boundary,
    )
    from tools.engineering_diagnostics_wave2r_validation_runtime import (
        run_wave2r_focused_tests,
    )

    boundary = ProjectSelectionRegistry(tool_source_root=root).resolve_boundary_for_root(root)
    registry = Path(ProjectSelectionRegistry(tool_source_root=root).registry_path)
    database = engineering_diagnostics_database_path(boundary)
    freeze_memory = (
        boundary.active_project_support_root
        / "project_freeze_after_update"
        / "frozen_features_memory"
    )
    registry_before = _optional_hash(registry)
    database_before = _optional_hash(database)
    freeze_before = _tree_hash(freeze_memory)

    print("PACKAGE REVISION: " + PACKAGE_REVISION)
    print("VALIDATOR TOOL ROOT IMPORT PATH: PASS")
    _require(
        _validator_hash() == VALIDATOR_CANONICAL_SHA256,
        "WAVE2R_VALIDATOR_CANONICAL_HASH_MISMATCH",
    )
    print("WAVE2R VALIDATOR CANONICAL HASH: PASS")
    _check_hashes(root, _INSTALLED_HASHES, "WAVE2R INSTALLED HASHES: PASS")
    _check_hashes(root, _PROTECTED_HASHES, "WAVE2N THROUGH WAVE2QB PROTECTED HASHES: PASS")
    validate_engineering_diagnostics_wave2r_public_boundary(root)
    run_wave2r_focused_tests(root)
    panel_ms, rows_ms, filter_ms = validate_wave2r_gui(root)
    _run_architecture(root)

    _require(_optional_hash(registry) == registry_before, "PROJECT_SELECTION_REGISTRY_MUTATED")
    _require(_optional_hash(database) == database_before, "WAVE2R_LIVE_DIAGNOSTIC_DATABASE_MUTATED")
    _require(_tree_hash(freeze_memory) == freeze_before, "WAVE2R_LIVE_FREEZE_MEMORY_MUTATED")

    lines = [
        "PACKAGE REVISION: " + PACKAGE_REVISION,
        "FOCUSED PUBLIC CONTRACT TESTS: 125/125 PASS",
        "WAVE2R HUMAN LIFECYCLE TRANSITIONS: PASS",
        "WAVE2R APPEND-ONLY DECISION HISTORY: PASS",
        "WAVE2R STALE GENERATION REJECTION: PASS",
        "WAVE2R SUPPRESSION REASON CONTRACT: PASS",
        "WAVE2R ACCEPTED RISK EXPLICIT CONFIRMATION: PASS",
        "WAVE2R FALSE POSITIVE SEARCHABILITY: PASS",
        "WAVE2R DEFERRED GOVERNED WAVE CONTRACT: PASS",
        "WAVE2R ATOMIC LIFECYCLE SCHEMA MIGRATION: PASS",
        "WAVE2R BASELINE ACCEPTANCE RISK COUPLING: ABSENT",
        "WAVE2R FINDINGS SILENTLY DELETED: NO",
        "WAVE2R SOURCE MUTATION EXECUTED: NO",
        "WAVE2R LIVE DIAGNOSTIC DATABASE MUTATED: NO",
        "WAVE2R LIVE FREEZE MEMORY MUTATED: NO",
        "WAVE2R GUI 25000 ROW INITIALIZATION MS: " + f"{rows_ms:.1f}",
        "WAVE2R GUI FILTER UPDATE MS: " + f"{filter_ms:.1f}",
        "WAVE2R GUI PANEL CREATION MS: " + f"{panel_ms:.1f}",
        "WAVE2R GUI HIGH-VOLUME PERFORMANCE: PASS",
        "WAVE2R NEW ARCHITECTURE ISSUES: 0",
        "WAVE2R TOUCHED PATH ARCHITECTURE ISSUES: 0",
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
