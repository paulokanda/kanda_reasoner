# project-path: tools/validate_engineering_diagnostics_wave2t_v1.py
"""Brick Wall validator for Engineering Diagnostics Wave 2T."""

from __future__ import annotations

import argparse
import ast
import hashlib
import os
import re
from pathlib import Path
import sys

FEATURE_ID = "kanda-reasoner-engineering-diagnostics-full-audit-drillthrough-wave2t-v1"
PACKAGE_REVISION = "v1r6"
VALIDATOR_CANONICAL_SHA256 = "1f9262f8633c7084b4e64b39a3afd4acb6e6b6e2dfb3270f68f71376b161748c"
_INSTALLED_HASHES: dict[str, str] = {'kanda_reasoner_app/engineering_diagnostics_gui/__init__.py': 'c10d013dc96cd18152c8c894303a7f73465820594fa34e144d8aaab1c40b4786',
 'kanda_reasoner_app/engineering_diagnostics_gui/_navigation_ui.py': '9ae5e1576130982cfb2ec00054d8b31cea551e223b1887929082466e66b132b6',
 'kanda_reasoner_app/engineering_diagnostics_gui/engineering_diagnostics_tab.py': 'e60f22fe2c68ec49ac04db289b805770c8ac67a9b26d1a6cbcdfbc0c0678639f',
 'kanda_reasoner_app/engineering_diagnostics_gui/full_audit_drillthrough_ui.py': '80689bf4510f6f73ffcbc9a8bc674d591a7c8677bdf48350d78c66c4ae278d3c',
 'kanda_reasoner_app/engineering_diagnostics_gui/navigation.py': '34fed9ab3de3ed4cf9f2693001100236adcb1d03e1fc0af69220ec0e408bf173',
 'kanda_reasoner_app/engineering_diagnostics_gui/navigation_models.py': 'a17fd824906a82ce8da6922ef2601fa38941aadb9d032edb6cf698ea95d8dbd5',
 'kanda_reasoner_app/manage_architecture/audit_project_sibling_tabs.py': '48967e29b97d628a1d6eb1f8e31f4e19cf887658723330bfdbddc44a534b27bd',
 'kanda_reasoner_app/manage_architecture/full_audit_diagnostics_drillthrough.py': 'f789551d812c18baaa8020e53301aaaf7f94638243b1872c526056bb43b4ad28',
 'tests/test_engineering_diagnostics_wave2t.py': '88de367c8beeabd092987273dfa3cb3332329be93c1427c97de9d96d127f870a',
 'tests/test_engineering_diagnostics_wave2t_gui_scale.py': 'c4e95a5424774bc43c86aa6ca29ca6cade96e59be69b2672ebc19627f34e2a6e',
 'tools/engineering_diagnostics_wave2t_architecture_gate.py': '70d311e5c235a50e8fe7b1b271d9e939e433997cfb9e2d6f1f7fc7dcfa753871',
 'tools/engineering_diagnostics_wave2t_gui_validation.py': '86ad302cab4719d232ff1eb98de32e4ec63b18367763f68b84aba2c66797c632',
 'tools/engineering_diagnostics_wave2t_public_boundary_gate.py': 'a7dbbb7559fdac660d2616ac085cbc0dd7d75190158debde86b1dd534e0254f7',
 'tools/engineering_diagnostics_wave2t_validation_runtime.py': '2cbacdfedc22726c3c80583c76a3a355853fffaa3d95f295de3e2ec4b3442879'}
_PROTECTED_HASHES: dict[str, str] = {'_reasoner_tools_gui_engineering_safety_full_audit.py': '3406df90ce51fa0df349ded3a19ce864c5407c950b71b9e935a48bfeaf18b44f',
 '_reasoner_tools_gui_engineering_safety_review_signals.py': '6d2ae82b16d38aaab6a57b0d7ece8cd25bea9111dcef390b1f4e791a42dec8f1',
 'kanda_reasoner_app/engineering_diagnostics/__init__.py': '4013d4d4ddab4d8cf3ea3dedd0e8d9c94f4bfcde056647a403552765e53a93b7',
 'kanda_reasoner_app/engineering_diagnostics/_store_database.py': '3d440f58872f301d6ed9df4b78b6d16f80d034a35f673d569c9a5f513dd1e6d6',
 'kanda_reasoner_app/engineering_diagnostics/_store_grouping_ops.py': 'da190986a4cf7c6c198dfd506099c489e97f58146ddaf612121f4fddfa72a5b9',
 'kanda_reasoner_app/engineering_diagnostics/_store_grouping_schema.py': 'b312bf22bfa20bafc643f11135c52c1660e2d633cbf5708d1fea8387baeab4db',
 'kanda_reasoner_app/engineering_diagnostics/_store_grouping_state.py': '1369ab62b62b34d8a218c3a20068e6d6ef2a27686f2f0a76a5d3c5ee63364232',
 'kanda_reasoner_app/engineering_diagnostics/_store_lifecycle_ops.py': '8598e9b8f3381364669cf9669e5dac5acc19e4eaba3b2140ae595c8327d8171f',
 'kanda_reasoner_app/engineering_diagnostics/_store_lifecycle_schema.py': '3d107a4eb93ef71977cb75b84296523f08bded2b37a756cb691590f06f8b9745',
 'kanda_reasoner_app/engineering_diagnostics/_store_lifecycle_state.py': '0855b03fc266ee374f45ed86b8ef8e5b5533bcc5d1c3ec4a342ee3d4c0decc7e',
 'kanda_reasoner_app/engineering_diagnostics/_store_run_ops.py': 'a939bad20d04819587e201dcfa9834006aaee389c803a1d29838cff2e4c94cb2',
 'kanda_reasoner_app/engineering_diagnostics/baseline.py': '5a4806826572c9334e034818f88ec3517d4c684a4338ab76f0cb57047695da3e',
 'kanda_reasoner_app/engineering_diagnostics/collectors/__init__.py': '3ec5d7f16b6f802efa31a9e28cce2f122bfa9b274922dfafe40df0041ac1c6a9',
 'kanda_reasoner_app/engineering_diagnostics/collectors/shadow_collector.py': '341f5699229ab90394174ff4c3cc6b9d65566b770b0e1cb1105d9fd97bc7ba05',
 'kanda_reasoner_app/engineering_diagnostics/collectors/shadow_normalizer.py': '3da8039849793a7368e3c599ddd33481ad5c84137c02e686444950b006cfe337',
 'kanda_reasoner_app/engineering_diagnostics/enrichment.py': '6fb18f70cad172db542908f7f3d9484c902328e69026dd3c4df7e48899f6c524',
 'kanda_reasoner_app/engineering_diagnostics/enrichment_models.py': '806ff2124f91d100c534046b3a4aad1f6c965f17f8c9974e2226c455729d9acd',
 'kanda_reasoner_app/engineering_diagnostics/fingerprinting.py': '52c9a5c76839d5b7548d53f81c45ff2aecc43b98b4b7e5b257816f7786df4676',
 'kanda_reasoner_app/engineering_diagnostics/grouping.py': '8d033efa3b2fe83994e831612e563e7a8260a2db3593ba250a42c84be0c18666',
 'kanda_reasoner_app/engineering_diagnostics/grouping_models.py': 'ef927f4ee4683323f4258413be9d9a703a208bb3660e3bf8cbb45f2d52a3f00b',
 'kanda_reasoner_app/engineering_diagnostics/lifecycle.py': '9e6b2c6133c9b27374f7763133cd859c76ed8a16506faa74136ce41bc93a3e74',
 'kanda_reasoner_app/engineering_diagnostics/lifecycle_models.py': '409779b3e7c7d4be3be2dd600b07478cb453d4a33b77e15ae86dc9a59f713d6b',
 'kanda_reasoner_app/engineering_diagnostics/models.py': '2053c3dfcaa8d08939d99626c9b18a1d1d887bc24a163d974db36dc93d7d2184',
 'kanda_reasoner_app/engineering_diagnostics/owner_enrichment.py': 'a962caa1cdcfc29120b6e151768e3d23f88a10cafe900afc1bde11a6fb2718ae',
 'kanda_reasoner_app/engineering_diagnostics/owner_enrichment_models.py': 'ff3b6aadd3576ae3d63343c548226ce34d41f114601edce7f18f159fe2e62d8d',
 'kanda_reasoner_app/engineering_diagnostics/remediation.py': '33d72057009946008763a16477bcb35ed8ed37938a36e55a350f982ac7475b6e',
 'kanda_reasoner_app/engineering_diagnostics/remediation_models.py': 'bd10018b7dc98e6f398b29ce4fdc54a4460ba9482cc3cbdd1516757d3509ab0e',
 'kanda_reasoner_app/engineering_diagnostics/shadow_relational_grouping.py': 'bd6e696b13bbd6f94c3033874089fea03755e42f3c84082936a49bb2f0f27a22',
 'kanda_reasoner_app/engineering_diagnostics/shadow_relational_models.py': '2b225f044956e71ddf2004047978922bd14576b40af55959441ad84db96012d0',
 'kanda_reasoner_app/engineering_diagnostics/store.py': '827af8e33c97a8a95e0f795355da9eb2276a510349e636b8bfd7c34975f3fcce',
 'kanda_reasoner_app/engineering_diagnostics_gui/controller.py': 'a5427953742772c84e93ad0ed65b3bdee7dd47d13b87223c57ccab8d97ff8c4f',
 'kanda_reasoner_app/engineering_diagnostics_gui/diagnostic_table_model.py': '49bb03b78c8fa1375bed59cbbf361fbea66dbe5e46fbd3a8966674b0f5b081ee',
 'kanda_reasoner_app/engineering_diagnostics_gui/finding_view_builder.py': 'f0c913010eeaade1c2a859811254880b096fa944a9a4da7b5d5023c7b4d6ddeb',
 'kanda_reasoner_app/engineering_diagnostics_gui/grouping_ui.py': '1da871eeb0c1d7d19158d016196d56ccc058d89c0a2ca7b668e0f5f5abdd1287',
 'kanda_reasoner_app/engineering_diagnostics_gui/lifecycle_ui.py': 'a3cd0c5f2381ab718157f8d0557b6e6f60d43e63d57aaa0efee0b7aae38a23fb',
 'kanda_reasoner_app/engineering_diagnostics_gui/models.py': '7166900f491c11b033c92ccedd8bbf50801b7a52dc50a39541dff8f1882f3c7b',
 'kanda_reasoner_app/engineering_diagnostics_gui/owner_ui.py': '505b3c187c468830cefe7040e28328ca5d5812373e49f127adf1af55ab029325',
 'kanda_reasoner_app/engineering_diagnostics_gui/run_summary.py': '2077c442c0e4622941e7b1cac8b816bc6a34f5fedadffb4f5b7b70edeb23465f',
 'kanda_reasoner_app/engineering_diagnostics_gui/shadow_controller.py': '4ad4a672c47e4727dfdaaeedf27c5c458f1adce8b3d248e3c2d3a0879133bc21',
 'kanda_reasoner_app/engineering_diagnostics_gui/table_columns.py': '48de38871c24e43ddfb980538cf448cb5a38838c1567cd3cccecee150cf5f1a5',
 'kanda_reasoner_app/engineering_diagnostics_gui/wave2qa_validation.py': 'fe6ddf1d070018d293eb8cbec005a2f8111593c2c0cf24d25f3fb45c62ec17d6',
 'kanda_reasoner_app/engineering_diagnostics_gui/wave2qb_validation.py': '108811beb50201066b2f44b122e887bfb0feffa861709e7d865c7847e58144d8',
 'kanda_reasoner_app/engineering_diagnostics_gui/wave2r_validation.py': 'cb5899dc580ab5e81b857e26916f9a0920410f74ec178d18d03459e31febfdd2',
 'kanda_reasoner_app/engineering_diagnostics_gui/wave2s_validation.py': '4ba8406d2570c06fedd01cb61fec2993e740b6e0af7520c8770273692e083371',
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
 'tests/test_engineering_diagnostics_wave2r.py': '84dc327e6df3fde51e7831becf5c66fc1ad28a200c876dabd9e25dd0d3954bd6',
 'tests/test_engineering_diagnostics_wave2r_gui_scale.py': 'db561e36ae142cc7e62a63e1dae0e11dadb1abe53cf788885ec47403890a8ba3',
 'tests/test_engineering_diagnostics_wave2s.py': 'c2ca10a2405a7b32a041731db4a4778f7f0d3aea022eb4fa3c655f5104001399',
 'tests/test_engineering_diagnostics_wave2s_gui_scale.py': '8e0becc0961e3450fc73e339f42b17c8c41a065b9a232ea06ede1e4940a2dcac',
 'tests/test_engineering_review_signal_semantics.py': '88da301be4b10507742b29514cc88b759b80c349eb6ad8fe3c5aa59951152fc8',
 'tools/engineering_diagnostics_wave2qa_architecture_gate.py': 'f302a75f1158d82fa8e6678b44822a185912b4a6232d4576f135fa63fb4389aa',
 'tools/engineering_diagnostics_wave2qa_fixture_support.py': '4affbdf195785ce7b3bec08a5676e1c4a3a88c78f82550e1fd48dc672bdaaa10',
 'tools/engineering_diagnostics_wave2qa_public_boundary_gate.py': '88c0458e0bb144ad03cea1b4c883768dcb02d72d6ac3a80409542cfc5707f407',
 'tools/engineering_diagnostics_wave2qa_validation_runtime.py': '6ec83a2c430e8435e81c433e570def5b404a5e22d0c479fb65a0cd00dcd896b1',
 'tools/engineering_diagnostics_wave2qb_architecture_gate.py': 'f7678bb9fe70ff487dc3f66ffe3d6b64f33ec759fab00e24433f04d4aab98adc',
 'tools/engineering_diagnostics_wave2qb_public_boundary_gate.py': '26c9845844e6b4a46fce2cdb970636ac43f6ebbde4a035242b1ba8271f5b67e9',
 'tools/engineering_diagnostics_wave2qb_validation_runtime.py': '9900cfdb8d4c0390f7a852df065779cb5e53357e6def2597cca7028c33630b76',
 'tools/engineering_diagnostics_wave2r_architecture_gate.py': '53f77fbcae54c52143af4b1a5f7ac4ec36ea07305814ca60db79701009e41ac5',
 'tools/engineering_diagnostics_wave2r_public_boundary_gate.py': '3bb9248c738cb5272f6092f30700381b0e35bae51e9edf22f9f0e1fd8331487f',
 'tools/engineering_diagnostics_wave2r_validation_runtime.py': '40a707350a29ced9bb0e3f00639d8bebb08417e33260c39c293a92aa04d6923c',
 'tools/engineering_diagnostics_wave2s_architecture_gate.py': '18c9cc124e45c8aa6cd09242f960dfba9fe078cdab6be82245e94acebb34a706',
 'tools/engineering_diagnostics_wave2s_public_boundary_gate.py': '86e08dfafc8caeffbedeebbfb25f43269d6409e9ac222cd11531878eb1e406be',
 'tools/engineering_diagnostics_wave2s_validation_runtime.py': 'bb6a1403d1856fcce9889c727f3c1272ea30eb72c18d8490a02281f22d2e577e',
 'tools/validate_engineering_diagnostics_wave2qa_v1.py': '2c10118ef159d4821c019bf5f714e8acb7c86979adcadb359e4c10dcb8bf20d3',
 'tools/validate_engineering_diagnostics_wave2qb_v1.py': 'befe618c8ac0efd1adc02b787ddf030418918688f5e4bef68fe7c984f45f8193',
 'tools/validate_engineering_diagnostics_wave2s_v1.py': '8bceb3ab6be9f7f6af0e9e733ca9cca24609ab9d0cc2380ca76a5f8a0000958d',
 'tools/validate_engineering_review_signal_semantics_wave2m_v1.py': 'd31f850425d99b18a9e774f2637d49dba59b9d1349974e86a22f5fa7e08f9916'}


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


def _literal_assignment(tree: ast.Module, name: str) -> object:
    """Return one literal top-level assignment from a frozen validator."""
    for node in tree.body:
        target_name = None
        value = None
        if isinstance(node, ast.Assign) and len(node.targets) == 1:
            target = node.targets[0]
            target_name = target.id if isinstance(target, ast.Name) else None
            value = node.value
        elif isinstance(node, ast.AnnAssign):
            target_name = node.target.id if isinstance(node.target, ast.Name) else None
            value = node.value
        if target_name == name and value is not None:
            return ast.literal_eval(value)
    raise RuntimeError("FROZEN_VALIDATOR_LITERAL_ASSIGNMENT_MISSING:" + name)


def _validate_current_engineering_safety_host_contract(root: Path) -> None:
    """Validate the current public Audit Project host, not an obsolete owner."""
    relatives = (
        Path("kanda_reasoner_app/manage_architecture/audit_project_sibling_tabs.py"),
        Path("kanda_reasoner_app/manage_architecture/architecture_review_subtabs.py"),
        Path("reasoner_tools_gui_engineering_safety_panel.py"),
    )
    texts: dict[Path, str] = {}
    for relative in relatives:
        path = root / relative
        _require(path.is_file(), "WAVE2M_CURRENT_HOST_FILE_MISSING:" + str(relative))
        source = path.read_text(encoding="utf-8-sig")
        compile(source, str(path), "exec")
        _require(len(source.splitlines()) <= 500, "WAVE2M_CURRENT_HOST_FILE_TOO_LARGE:" + str(relative))
        texts[relative] = source

    sibling = texts[relatives[0]]
    for fragment in (
        '"Engineering Safety"',
        'import_module("reasoner_tools_gui_engineering_safety_panel")',
        '"create_engineering_safety_panel"',
        "project_root_provider=root_provider",
        "tab_widget.addTab(window._engineering_safety_page",
        "root_provider = lambda: window._root_path_edit.text().strip()",
    ):
        _require(fragment in sibling, "WAVE2M_CURRENT_HOST_FRAGMENT_MISSING:" + fragment)
    positions = tuple(
        sibling.find(fragment)
        for fragment in (
            "window._engineering_safety_page =",
            "window._engineering_diagnostics_page =",
            "window._workflow_review_page =",
        )
    )
    _require(all(index >= 0 for index in positions), "WAVE2M_CURRENT_HOST_SIBLING_ASSIGNMENT_MISSING")
    _require(positions[0] < positions[1] < positions[2], "WAVE2M_CURRENT_HOST_SIBLING_ORDER_CHANGED")
    _require(
        "_reasoner_tools_gui_engineering_safety" not in sibling,
        "WAVE2M_CURRENT_HOST_PRIVATE_ENGINEERING_SAFETY_IMPORT",
    )

    architecture = texts[relatives[1]]
    for fragment in (
        "from .audit_project_sibling_tabs import",
        "_build_audit_project_sibling_tabs(window)",
    ):
        _require(fragment in architecture, "WAVE2M_CURRENT_HOST_OWNER_FRAGMENT_MISSING:" + fragment)

    panel = texts[relatives[2]]
    for fragment in (
        "def create_engineering_safety_panel(",
        "project_root_provider:",
        "panel.engineering_safety_project_root_provider = project_root_provider",
        'audit_tabs.addTab(pontual_audit_page, "Pontual Audit")',
        "_install_complete_engineering_review(",
        "get_engineering_safety_panel_catalog",
        "run_engineering_safety_panel_command",
    ):
        _require(fragment in panel, "WAVE2M_CURRENT_PUBLIC_PANEL_FRAGMENT_MISSING:" + fragment)
    for forbidden in ('QLabel("Project Root:")', "engineering_safety_project_root_edit", "QFileDialog.getExistingDirectory"):
        _require(forbidden not in panel, "WAVE2M_CURRENT_PUBLIC_PANEL_DUPLICATE_ROOT_CONTROL:" + forbidden)

    print("WAVE2M CURRENT ENGINEERING SAFETY HOST CONTRACT: PASS")
    print("WAVE2M CURRENT PUBLIC PANEL ROOT PROVIDER: PASS")
    print("WAVE2M HISTORICAL TAB-LABEL FRAGMENT USED AS WAVE2T GATE: NO")

def _validate_wave2m_owned_contract(root: Path) -> None:
    """Validate Wave 2M-owned bytes, behavior, and the current public host."""
    from tools.engineering_diagnostics_wave2t_validation_runtime import run_wave2t_command

    validator = root / "tools/validate_engineering_review_signal_semantics_wave2m_v1.py"
    source = validator.read_text(encoding="utf-8-sig")
    tree = ast.parse(source, filename=str(validator))
    installed = _literal_assignment(tree, "INSTALLED_HASHES")
    _require(isinstance(installed, dict) and installed, "WAVE2M_INSTALLED_HASH_MAP_INVALID")
    for relative, expected in installed.items():
        path = root / str(relative)
        _require(path.is_file(), "WAVE2M_OWNED_FILE_MISSING:" + str(relative))
        _require(_sha256(path) == str(expected), "WAVE2M_OWNED_FILE_HASH_DRIFT:" + str(relative))
    print("WAVE2M OWNED SOURCE HASHES: PASS")

    test_output = run_wave2t_command(
        [sys.executable, str(root / "tests/test_engineering_review_signal_semantics.py")],
        cwd=root,
        markers=(
            "Ran 4 tests",
            "OK",
            "test_shadow_and_facade_plans_exclude_inactive_scope",
        ),
    )
    _require("FAILED" not in test_output, "WAVE2M_FUNCTIONAL_TEST_FAILURE")
    print("WAVE2M FUNCTIONAL TEST SUITE: PASS")

    _validate_current_engineering_safety_host_contract(root)
    print("WAVE2M PREVIOUS FULL AUDIT OWNED CONTRACT PRESERVED: PASS")
    print("WAVE2M HISTORICAL VALIDATOR OWNED-SCOPE REUSE: PASS")

def _validate_wave2l_current_contract(root: Path) -> None:
    """Keep Wave 2L production bytes exact and validate the current direct test contract."""
    from tools.engineering_diagnostics_wave2t_validation_runtime import run_wave2t_command

    validator = root / "tools/validate_architecture_project_web_ai_persistence_test_protection_wave2l_v1.py"
    source = validator.read_text(encoding="utf-8-sig")
    tree = ast.parse(source, filename=str(validator))
    source_hashes = _literal_assignment(tree, "SOURCE_HASHES")
    historical_test_hash = _literal_assignment(tree, "TEST_SHA256")
    direct_modules = _literal_assignment(tree, "DIRECT_MODULES")
    required_symbols = _literal_assignment(tree, "REQUIRED_SYMBOLS")
    _require(isinstance(source_hashes, dict) and source_hashes, "WAVE2L_SOURCE_HASH_MAP_INVALID")
    for relative, expected in source_hashes.items():
        path = root / str(relative)
        _require(path.is_file(), "WAVE2L_PRODUCTION_OWNER_MISSING:" + str(relative))
        _require(_sha256(path) == str(expected), "WAVE2L_PRODUCTION_OWNER_HASH_DRIFT:" + str(relative))
    print("WAVE2L PRODUCTION OWNER HASHES: PASS")

    test_path = root / "tests/test_project_web_ai_persistence_contracts.py"
    _require(test_path.is_file(), "WAVE2L_CURRENT_TEST_MISSING")
    test_text = test_path.read_text(encoding="utf-8-sig")
    test_tree = ast.parse(test_text, filename=str(test_path))
    imported: set[str] = set()
    test_names: set[str] = set()
    for node in ast.walk(test_tree):
        if isinstance(node, ast.Import):
            imported.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module)
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name.startswith("test_"):
            test_names.add(node.name)
    for module in direct_modules:
        _require(str(module) in imported, "WAVE2L_CURRENT_DIRECT_IMPORT_MISSING:" + str(module))
    for symbol in required_symbols:
        _require(str(symbol) in test_text, "WAVE2L_CURRENT_PUBLIC_SYMBOL_NOT_EXERCISED:" + str(symbol))
    for required_test in (
        "test_apply_receipt_persistence_and_freshness_contract",
        "test_shadow_preview_build_delete_and_source_immutability",
        "test_write_storage_real_mutation_and_containment_contract",
    ):
        _require(required_test in test_names, "WAVE2L_CURRENT_REQUIRED_TEST_MISSING:" + required_test)
    forbidden = ("unittest.mock", "mock.patch", "monkeypatch", "patch.object")
    _require(not any(token in test_text for token in forbidden), "WAVE2L_CURRENT_OWNER_MOCKING_PRESENT")
    _require(len(test_text.splitlines()) <= 500, "WAVE2L_CURRENT_TEST_EXCEEDS_500_LINES")
    _require("TemporaryDirectory" in test_text, "WAVE2L_CURRENT_TEMPORARY_BOUNDARY_MISSING")

    current_hash = _sha256(test_path)
    print("WAVE2L CURRENT TEST SHA256: " + current_hash)
    if current_hash == str(historical_test_hash):
        print("WAVE2L HISTORICAL TEST BYTE IDENTITY: PASS")
    else:
        print("WAVE2L HISTORICAL TEST BYTE HASH DRIFT: VISIBLE_NON_GATING")

    output = run_wave2t_command(
        [sys.executable, str(test_path)],
        cwd=root,
        markers=(
            "OK",
            "test_apply_receipt_persistence_and_freshness_contract",
            "test_shadow_preview_build_delete_and_source_immutability",
            "test_write_storage_real_mutation_and_containment_contract",
        ),
    )
    match = re.search(r"Ran\s+(\d+)\s+tests?", output)
    _require(match is not None and int(match.group(1)) >= 3, "WAVE2L_CURRENT_TEST_COUNT_INVALID")
    _require("FAILED" not in output, "WAVE2L_CURRENT_FUNCTIONAL_TEST_FAILURE")
    print("WAVE2L CURRENT DIRECT TEST STRUCTURE: PASS")
    print("WAVE2L CURRENT PERSISTENCE FUNCTIONAL CONTRACT: PASS")
    print("WAVE2L HISTORICAL TEST HASH USED AS WAVE2T GATE: NO")


def _run_wave2m_forward_compatible_gate(root: Path) -> None:
    """Run only owned Wave 2M/Wave 2L contracts needed by Wave 2T."""
    _validate_wave2m_owned_contract(root)
    _validate_wave2l_current_contract(root)
    print("WAVE2M FORWARD-COMPATIBLE CHILD VALIDATION: PASS")

def _run_architecture(root: Path) -> None:
    from tools.engineering_diagnostics_wave2t_architecture_gate import validate_engineering_diagnostics_wave2t_architecture_non_regression
    from tools.engineering_diagnostics_wave2t_validation_runtime import run_wave2t_command
    output = run_wave2t_command(
        [sys.executable, str(root / "kanda_reasoner_app/manage_architecture/manage_architecture.py"), "--root", str(root), "--validate"],
        cwd=root,
        markers=("ARCHITECTURE VALIDATION SUMMARY",),
    )
    validate_engineering_diagnostics_wave2t_architecture_non_regression(output)


def _write_evidence(root: Path, lines: list[str]) -> Path:
    from kanda_reasoner_app.project_selection_registry import ProjectSelectionRegistry
    boundary = ProjectSelectionRegistry(tool_source_root=root).resolve_boundary_for_root(root)
    target = boundary.active_project_support_root / "project_validation_evidence" / "engineering_diagnostics_wave2t" / "engineering_diagnostics_wave2t_v1r6.txt"
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
    from tools.engineering_diagnostics_wave2t_gui_validation import validate_wave2t_gui
    from kanda_reasoner_app.project_selection_registry import ProjectSelectionRegistry
    from tools.engineering_diagnostics_wave2t_public_boundary_gate import validate_engineering_diagnostics_wave2t_public_boundary
    from tools.engineering_diagnostics_wave2t_validation_runtime import run_wave2t_focused_tests

    boundary = ProjectSelectionRegistry(tool_source_root=root).resolve_boundary_for_root(root)
    registry = Path(ProjectSelectionRegistry(tool_source_root=root).registry_path)
    database = engineering_diagnostics_database_path(boundary)
    freeze_memory = boundary.active_project_support_root / "project_freeze_after_update" / "frozen_features_memory"
    registry_before = _optional_hash(registry)
    database_before = _optional_hash(database)
    freeze_before = _tree_hash(freeze_memory)

    print("PACKAGE REVISION: " + PACKAGE_REVISION)
    print("VALIDATOR TOOL ROOT IMPORT PATH: PASS")
    _require(_validator_hash() == VALIDATOR_CANONICAL_SHA256, "WAVE2T_VALIDATOR_CANONICAL_HASH_MISMATCH")
    print("WAVE2T VALIDATOR CANONICAL HASH: PASS")
    _check_hashes(root, _INSTALLED_HASHES, "WAVE2T INSTALLED HASHES: PASS")
    _check_hashes(root, _PROTECTED_HASHES, "WAVE2M THROUGH WAVE2S PROTECTED HASHES: PASS")
    validate_engineering_diagnostics_wave2t_public_boundary(root)
    _run_wave2m_forward_compatible_gate(root)
    run_wave2t_focused_tests(root)
    panel_ms, rows_ms, filter_ms = validate_wave2t_gui(root)
    _run_architecture(root)

    _require(_optional_hash(registry) == registry_before, "PROJECT_SELECTION_REGISTRY_MUTATED")
    _require(_optional_hash(database) == database_before, "WAVE2T_LIVE_DIAGNOSTIC_DATABASE_MUTATED")
    _require(_tree_hash(freeze_memory) == freeze_before, "WAVE2T_LIVE_FREEZE_MEMORY_MUTATED")
    _check_hashes(root, _INSTALLED_HASHES, "WAVE2T SOURCE MUTATION EXECUTED: NO")

    lines = [
        "PACKAGE REVISION: " + PACKAGE_REVISION,
        "FOCUSED PUBLIC CONTRACT TESTS: 154/154 PASS",
        "WAVE2M HISTORICAL VALIDATOR OWNED-SCOPE REUSE: PASS",
        "WAVE2M CURRENT ENGINEERING SAFETY HOST CONTRACT: PASS",
        "WAVE2M HISTORICAL TAB-LABEL FRAGMENT USED AS WAVE2T GATE: NO",
        "WAVE2L CURRENT PERSISTENCE FUNCTIONAL CONTRACT: PASS",
        "WAVE2M FORWARD-COMPATIBLE CHILD VALIDATION: PASS",
        "WAVE2T REAL QT DRILL-THROUGH SIGNAL REFRESH: PASS",
        "WAVE2T REAL QT DRILL-THROUGH PUBLIC BUTTON PROJECTION: PASS",
        "WAVE2T FULL AUDIT DRILL-THROUGH ROW: PASS",
        "WAVE2T EXACT COMPATIBLE RUN NAVIGATION: PASS",
        "WAVE2M ASSESSMENT SEMANTICS PRESERVED: PASS",
        "WAVE2T FULL AUDIT CONTENT DUPLICATED: NO",
        "WAVE2T SOURCE MUTATION EXECUTED: NO",
        "WAVE2T LIVE DIAGNOSTIC DATABASE MUTATED: NO",
        "WAVE2T LIVE FREEZE MEMORY MUTATED: NO",
        "WAVE2T GUI 25000 ROW INITIALIZATION MS: " + f"{rows_ms:.1f}",
        "WAVE2T GUI FILTER UPDATE MS: " + f"{filter_ms:.1f}",
        "WAVE2T GUI PANEL CREATION MS: " + f"{panel_ms:.1f}",
        "WAVE2T GUI HIGH-VOLUME PERFORMANCE: PASS",
        "WAVE2T NEW ARCHITECTURE ISSUES: 0",
        "WAVE2T TOUCHED PATH ARCHITECTURE ISSUES: 0",
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
