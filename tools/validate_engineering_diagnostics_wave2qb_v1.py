# project-path: tools/validate_engineering_diagnostics_wave2qb_v1.py
"""Brick Wall validator for Engineering Diagnostics Wave 2Q-B."""

from __future__ import annotations

import argparse
import hashlib
import os
from pathlib import Path
import sys

FEATURE_ID = "kanda-reasoner-engineering-diagnostics-shadow-relational-grouping-wave2qb-v1"
PACKAGE_REVISION = "v1"
VALIDATOR_CANONICAL_SHA256 = "f606df4e18aa28f37b201aa18d286e052f67b1f0a2b28d2ae78916e39a6a4ee6"
_INSTALLED_HASHES: dict[str, str] = {
    'kanda_reasoner_app/engineering_diagnostics/collectors/shadow_collector.py': '341f5699229ab90394174ff4c3cc6b9d65566b770b0e1cb1105d9fd97bc7ba05',
    'kanda_reasoner_app/engineering_diagnostics/collectors/shadow_normalizer.py': '3da8039849793a7368e3c599ddd33481ad5c84137c02e686444950b006cfe337',
    'kanda_reasoner_app/engineering_diagnostics/collectors/__init__.py': '3ec5d7f16b6f802efa31a9e28cce2f122bfa9b274922dfafe40df0041ac1c6a9',
    'kanda_reasoner_app/engineering_diagnostics/shadow_relational_models.py': '2b225f044956e71ddf2004047978922bd14576b40af55959441ad84db96012d0',
    'kanda_reasoner_app/engineering_diagnostics/shadow_relational_grouping.py': 'bd6e696b13bbd6f94c3033874089fea03755e42f3c84082936a49bb2f0f27a22',
    'kanda_reasoner_app/engineering_diagnostics/grouping.py': '8d033efa3b2fe83994e831612e563e7a8260a2db3593ba250a42c84be0c18666',
    'kanda_reasoner_app/engineering_diagnostics/__init__.py': '02a7d5af8a470ba6330f6424383aa79db1f7aa83c660dddd02b1a1aaa20c505d',
    'kanda_reasoner_app/engineering_diagnostics_gui/shadow_controller.py': '4ad4a672c47e4727dfdaaeedf27c5c458f1adce8b3d248e3c2d3a0879133bc21',
    'kanda_reasoner_app/engineering_diagnostics_gui/controller.py': '297bb2c5743695462f7068727d0c8f6e294091ccbc8e2ea1edfa1a6a97a441e5',
    'kanda_reasoner_app/engineering_diagnostics_gui/engineering_diagnostics_tab.py': 'bc720f4f775f33d1856882a564e792598ef9b3a4999a509d031fbfe935930879',
    'kanda_reasoner_app/engineering_diagnostics_gui/wave2qb_validation.py': '108811beb50201066b2f44b122e887bfb0feffa861709e7d865c7847e58144d8',
    'tests/test_engineering_diagnostics_wave2qb.py': '62564355446659e653fcf5cda2bf0166862c7c8358305f6d3e2897cd213fb024',
    'tests/test_engineering_diagnostics_wave2qb_gui_scale.py': '7c94327dd030a247025e7156801f8917522510bbd3c85fe235c1cd27f5b5c2dd',
    'tools/engineering_diagnostics_wave2qb_architecture_gate.py': 'f7678bb9fe70ff487dc3f66ffe3d6b64f33ec759fab00e24433f04d4aab98adc',
    'tools/engineering_diagnostics_wave2qb_public_boundary_gate.py': '26c9845844e6b4a46fce2cdb970636ac43f6ebbde4a035242b1ba8271f5b67e9',
    'tools/engineering_diagnostics_wave2qb_validation_runtime.py': '9900cfdb8d4c0390f7a852df065779cb5e53357e6def2597cca7028c33630b76',
}
_PROTECTED_HASHES: dict[str, str] = {
    'kanda_reasoner_app/engineering_diagnostics/_store_database.py': 'c13fd012a5f7cb59d48ee7b0ea81c7d34cce53677a523e17112d86fcc34fa505',
    'kanda_reasoner_app/engineering_diagnostics/_store_grouping_ops.py': 'da190986a4cf7c6c198dfd506099c489e97f58146ddaf612121f4fddfa72a5b9',
    'kanda_reasoner_app/engineering_diagnostics/_store_grouping_schema.py': 'b312bf22bfa20bafc643f11135c52c1660e2d633cbf5708d1fea8387baeab4db',
    'kanda_reasoner_app/engineering_diagnostics/_store_grouping_state.py': '1369ab62b62b34d8a218c3a20068e6d6ef2a27686f2f0a76a5d3c5ee63364232',
    'kanda_reasoner_app/engineering_diagnostics/grouping_models.py': 'ef927f4ee4683323f4258413be9d9a703a208bb3660e3bf8cbb45f2d52a3f00b',
    'kanda_reasoner_app/engineering_diagnostics/store.py': '0cc6a6100b2e98228301a3d1790e48e78c550dec01191abc218f3e6b0b072e29',
    'kanda_reasoner_app/engineering_diagnostics_gui/diagnostic_table_model.py': '64640a38eaff0de4f3949aad12a8abf682da465cfbc202ed36a69ec192141d24',
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
    'tools/validate_engineering_diagnostics_wave2qa_v1.py': '2c10118ef159d4821c019bf5f714e8acb7c86979adcadb359e4c10dcb8bf20d3',
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
    'kanda_reasoner_app/source_hygiene/shadow_audit.py': 'cdf5efc3717c0a29365467f65eda914ad86df93d7c9feb6f25f3a251835fa91f',
    'kanda_reasoner_app/source_hygiene/_shadow_audit_ast.py': '2523e1d99faf9aa8ed7376b7fa0726e1fc3da37baea920b4a5807f3a1d63624f',
    'kanda_reasoner_app/source_hygiene/_active_scope.py': 'ecc7017f6f7607f34fb5bb7e513d1fe2a59fea50878c5bc1ac1efa5a92087c44',
    'kanda_reasoner_app/project_selection_registry.py': '98dbb376654e0608f9d6863829999ac5bcf0523715c859f3b067cde42b9d7fa1',
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
    from tools.engineering_diagnostics_wave2qa_validation_runtime import run_wave2qa_command
    from tools.engineering_diagnostics_wave2qb_architecture_gate import (
        validate_engineering_diagnostics_wave2qb_architecture_non_regression,
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
    validate_engineering_diagnostics_wave2qb_architecture_non_regression(output)


def _write_evidence(root: Path, lines: list[str]) -> Path:
    from kanda_reasoner_app.project_selection_registry import ProjectSelectionRegistry

    boundary = ProjectSelectionRegistry(tool_source_root=root).resolve_boundary_for_root(root)
    target = (
        boundary.active_project_support_root
        / "project_validation_evidence"
        / "engineering_diagnostics_wave2qb"
        / "engineering_diagnostics_wave2qb_v1.txt"
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

    from kanda_reasoner_app.engineering_diagnostics_gui.wave2qb_validation import validate_wave2qb_gui
    from kanda_reasoner_app.project_selection_registry import ProjectSelectionRegistry
    from tools.engineering_diagnostics_wave2qb_public_boundary_gate import (
        validate_engineering_diagnostics_wave2qb_public_boundary,
    )
    from tools.engineering_diagnostics_wave2qb_validation_runtime import (
        run_wave2qb_focused_tests,
        validate_wave2qb_shadow_read_only,
    )

    registry = Path(ProjectSelectionRegistry(tool_source_root=root).registry_path)
    registry_before = _optional_hash(registry)
    print("PACKAGE REVISION: " + PACKAGE_REVISION)
    print("VALIDATOR TOOL ROOT IMPORT PATH: PASS")
    _require(_validator_hash() == VALIDATOR_CANONICAL_SHA256, "WAVE2QB_VALIDATOR_CANONICAL_HASH_MISMATCH")
    print("WAVE2QB VALIDATOR CANONICAL HASH: PASS")
    _check_hashes(root, _INSTALLED_HASHES, "WAVE2QB INSTALLED HASHES: PASS")
    _check_hashes(root, _PROTECTED_HASHES, "WAVE2N THROUGH WAVE2QA PROTECTED HASHES: PASS")
    validate_engineering_diagnostics_wave2qb_public_boundary(root)
    run_wave2qb_focused_tests(root)
    finding_count = validate_wave2qb_shadow_read_only(root)
    panel_ms, rows_ms, filter_ms = validate_wave2qb_gui(root)
    _run_architecture(root)
    _require(_optional_hash(registry) == registry_before, "PROJECT_SELECTION_REGISTRY_MUTATED")

    lines = [
        "PACKAGE REVISION: " + PACKAGE_REVISION,
        "FOCUSED PUBLIC CONTRACT TESTS: 108/108 PASS",
        "WAVE2QB LIVE SHADOW PUBLIC AUDIT: PASS",
        "WAVE2QB LIVE SHADOW FINDING COUNT: " + str(finding_count),
        "WAVE2QB DETERMINISTIC RELATIONAL GRAPH: PASS",
        "WAVE2QB CONNECTED COMPONENT GROUPING: PASS",
        "WAVE2QB 25000 FINDING RELATIONAL GROUPING: PASS",
        "WAVE2QB DETERMINISTIC EDGE EVIDENCE: PASS",
        "WAVE2QB AI GROUPING USED: NO",
        "WAVE2QB LIVE DIAGNOSTIC DATABASE MUTATED: NO",
        "WAVE2QB LIVE FREEZE MEMORY MUTATED: NO",
        "WAVE2QB GUI 25000 ROW INITIALIZATION MS: " + f"{rows_ms:.1f}",
        "WAVE2QB GUI FILTER UPDATE MS: " + f"{filter_ms:.1f}",
        "WAVE2QB GUI PANEL CREATION MS: " + f"{panel_ms:.1f}",
        "WAVE2QB GUI HIGH-VOLUME PERFORMANCE: PASS",
        "WAVE2QB NEW ARCHITECTURE ISSUES: 0",
        "WAVE2QB TOUCHED PATH ARCHITECTURE ISSUES: 0",
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
