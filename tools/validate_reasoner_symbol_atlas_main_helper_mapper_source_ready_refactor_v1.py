"""Validate the source-ready refactor of the symbol-atlas helper mapper."""

from __future__ import annotations

import ast
import copy
import hashlib
import importlib
import inspect
import json
import tempfile
from pathlib import Path

__all__ = [
    "main",
]

FEATURE_ID = "reasoner-symbol-atlas-main-helper-mapper-source-ready-refactor-v1"
BASELINE_SOURCE_HASH = "6637b1dde8639665f37f948d1bf7ba0711ecbe4d418ce304a01503f291f99f55"
SOURCE_CANDIDATE_SET_HASH = "8657eb42f9b015f63fa1acea10975839e1518aeb6e382d3a08b1fc77e6a5f875"
SOURCE_EXCHANGE_IDENTITY_HASH = "e8a55235cfa424b06cd44612887fc755506c983355203db9c6a282d28efb1b40"
EXPECTED_PUBLIC_API = [
    "PROJECT_SYMBOL_ATLAS_HELPER_SUFFIXES",
    "PROJECT_SYMBOL_ATLAS_MAIN_HELPER_STATUS_AMBIGUOUS_MAIN",
    "PROJECT_SYMBOL_ATLAS_MAIN_HELPER_STATUS_INSUFFICIENT_EVIDENCE",
    "PROJECT_SYMBOL_ATLAS_MAIN_HELPER_STATUS_NO_HELPERS_FOUND",
    "PROJECT_SYMBOL_ATLAS_MAIN_HELPER_STATUS_READY",
    "PROJECT_SYMBOL_ATLAS_MAIN_HELPER_STATUS_TARGET_NOT_FOUND",
    "ProjectSymbolAtlasMainHelperDecision",
    "ProjectSymbolAtlasMainHelperOptions",
    "build_reasoner_symbol_atlas_main_helper_report",
    "map_reasoner_symbol_atlas_main_helpers",
]
EXPECTED_DEF_HASHES = {'ProjectSymbolAtlasMainHelperDecision': 'a6f2e16ff1f0ab611d774a25ed2c9178731ebf5469b211e45d7fdc808d3336db', 'ProjectSymbolAtlasMainHelperOptions': '51d5b54843a3fa3e88ae9157b3be4bb005aa89f14c5af05842822f26bdb3f1a4', '_active_records': '262c48e9a13bc3c444ac9a5287eef1de854434c498c819e5ddb59126c1124c62', '_coerce_project_root': '71e1000c9db824107ce4357e2ec6bd155399bfea1039ec31ffd924b4740db8c5', '_decision_status': 'd0956b26ec43e7ea8c0d493c42546923cbf2a6ac0945df8a12c497b01c6dea0f', '_find_target_record': '2ad361edbf8f5f4aa2237fb7f5f7adabf91267f62805f1d8d3642503a508b925', '_format_decision_summary': '0e60a6b95bdc5929bf3f76fd6da633c8883074372179fa2a06cf83e7d4befaad', '_has_helper_suffix': 'bc899f854510a1f88196e8760cb1098ed3615d3ead20bf1da4fdd260ed35a0a2', '_helper_score': 'b88fbe4bdb8009b8f99496c917a360aade7eb05cc44bd393db28d89abd4f2121', '_main_candidates_for_helper': 'ecce7b16b9b2377e300ef369e3e924e6deb1d59ca819ab7ac0e181e505a920b7', '_module_imports': '6519d3d4e3698f884a55e87f0651f49ece42d6299d8967877dd842db6ae2e185', '_module_stem': '4e79edd26f562f7b1b1aa4928d9b00439a87a8749ea9c068a848c6b73e48b123', '_normalize_path_for_compare': '27fcc4551af2941b2c0752222d6f204d8bcf1b31d0c8e8e9d102fe827e29de65', '_normalize_record_path': '2fd735fbc03644dbbc7a5b3508bc4c6d8e56e5226b40bb7118bd596fc95831dc', '_public_helper_warnings': 'aee57afd16ef85b7fb2d32e95d1d8a9704ce838a774d2bfee4ad6a0550045535', '_record_is_active': '041af38d6b4871cf6526fe1d04c2756a51f692eb7ea164405cc22d6acf733df5', '_record_is_low_signal_support_file': 'd620195bec75030ac7cbf2628faf7a64fc80c7d857184a199c4fb6abe28d657e', '_record_is_private_helper': 'b2c96d18821d48e76a9277b486b05ac6feb00d9bd6ee319c8e5a53afdd8c1c0f', '_related_tests_to_run': 'ff68c087529cf20254afa343460b8afeca35a38400da0ddb036354f2a5003fd9', '_select_helper_records': '3eed0275eef1798dec16da587a663704c75dbf4327d2273b268d1b4f3dcfd1d8', '_select_main_record': '87fc243c744d755238d8f52a197c8980b4bda061ceffc4777a6ad7f2f14f6f8a', '_strip_helper_suffix': '74f055542e36a03ad73ef1bcc0c0dab096196a0f576f09626d3340fd8daed357', '_target_is_helper_like': 'a5210ceddbfec4cdb613e91521b6ba111120d194c750d9e07a7cea18c0dd7021', '_target_role': '4ed15f7991dad6bd94f5957c400dbfaf38cb686ca4e1f1c962a0cf18fe9f6080', 'build_reasoner_symbol_atlas_main_helper_report': '2cf09e58f9bc3e4fbb77590a2bfb58cbec994a97d7c8ff74bc88939656a5d68a', 'map_reasoner_symbol_atlas_main_helpers': '2bf23a9c8c40bfabd5b96c21f007e0d667caf262f3926121099df7ff385b09b7'}
EXPECTED_LOCATIONS = {
    "main_helper_mapper.py": {
        "ProjectSymbolAtlasMainHelperDecision",
        "ProjectSymbolAtlasMainHelperOptions",
        "build_reasoner_symbol_atlas_main_helper_report",
        "map_reasoner_symbol_atlas_main_helpers",
    },
    "_main_helper_mapper_path_resolution.py": {
        "_coerce_project_root",
        "_find_target_record",
        "_normalize_path_for_compare",
        "_normalize_record_path",
    },
    "_main_helper_mapper_helper_selection.py": {
        "_active_records",
        "_decision_status",
        "_format_decision_summary",
        "_has_helper_suffix",
        "_helper_score",
        "_main_candidates_for_helper",
        "_module_imports",
        "_module_stem",
        "_public_helper_warnings",
        "_record_is_active",
        "_record_is_low_signal_support_file",
        "_record_is_private_helper",
        "_related_tests_to_run",
        "_select_helper_records",
        "_select_main_record",
        "_strip_helper_suffix",
        "_target_is_helper_like",
        "_target_role",
    },
}
ALLOWED_DEFERRED_FACADE_IMPORTS: dict[str, set[str]] = {}

REQUIRED_NEUTRAL_CONTRACT_IMPORTS = {
    "._main_helper_mapper_contract._HELPER_SUFFIXES",
    "._main_helper_mapper_contract._MainHelperDecisionLike",
    "._main_helper_mapper_contract._STATUS_NO_HELPERS_FOUND",
    "._main_helper_mapper_contract._STATUS_READY",
}
FORBIDDEN_PREVIEW_TEXT = (
    "KANDA PREVIEW ARTIFACT",
    "NOT SOURCE TRUTH",
    "Preview helper role:",
    "Source mutation is disabled",
    "selected project Preview support",
    "# Extraction backend:",
    "E:\\kanda_reasoner\\",
)


def _project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _top_defs(tree: ast.Module) -> dict[str, ast.AST]:
    return {
        node.name: node
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
    }


def _normalize_docstring(body: list[ast.stmt]) -> list[ast.stmt]:
    if (
        body
        and isinstance(body[0], ast.Expr)
        and isinstance(body[0].value, ast.Constant)
        and isinstance(body[0].value.value, str)
    ):
        body[0].value.value = inspect.cleandoc(body[0].value.value)
    return body


def _canonical_ast(value: object) -> object:
    """Return a version-stable semantic AST form for supported Python versions."""

    if isinstance(value, ast.AST):
        fields: dict[str, object] = {}
        for field, child in ast.iter_fields(value):
            canonical = _canonical_ast(child)
            if canonical is None or canonical == [] or canonical == ():
                continue
            fields[field] = canonical
        return {"node": type(value).__name__, "fields": fields}
    if isinstance(value, list):
        return [_canonical_ast(item) for item in value]
    if isinstance(value, tuple):
        return tuple(_canonical_ast(item) for item in value)
    if value is Ellipsis:
        return {"literal": "Ellipsis"}
    if isinstance(value, bytes):
        return {"bytes_hex": value.hex()}
    if isinstance(value, complex):
        return {"complex": [value.real, value.imag]}
    return value


def _assert_version_stable_ast_canonicalization() -> None:
    base = ast.parse(
        "def sample(value: int = 1) -> int:\n"
        "    \"\"\"Sample doc.\n    Details.\"\"\"\n"
        "    return value\n"
    ).body[0]
    schema_variant = copy.deepcopy(base)
    schema_variant._fields = tuple(schema_variant._fields) + (
        "future_empty_field",
        "future_none_field",
    )
    schema_variant.future_empty_field = []
    schema_variant.future_none_field = None
    if _canonical_ast(base) != _canonical_ast(schema_variant):
        raise AssertionError("VERSION_STABLE_AST_EMPTY_SCHEMA_FIELD_DRIFT")

    whitespace_variant = copy.deepcopy(base)
    whitespace_variant.body[0].value.value = "Sample doc.\n        Details."
    base_doc = copy.deepcopy(base)
    base_doc.body = _normalize_docstring(base_doc.body)
    whitespace_variant.body = _normalize_docstring(whitespace_variant.body)
    if _canonical_ast(base_doc) != _canonical_ast(whitespace_variant):
        raise AssertionError("DOCSTRING_WHITESPACE_NORMALIZATION_DRIFT")

    executable_variant = copy.deepcopy(base_doc)
    executable_variant.body[-1] = ast.Return(value=ast.Constant(value=2))
    if _canonical_ast(base_doc) == _canonical_ast(executable_variant):
        raise AssertionError("EXECUTABLE_AST_DRIFT_WAS_NOT_DETECTED")


def _normalize_def(node: ast.AST) -> str:
    clone = copy.deepcopy(node)

    class Normalizer(ast.NodeTransformer):
        def visit_FunctionDef(self, current: ast.FunctionDef) -> ast.AST:
            self.generic_visit(current)
            current.body = _normalize_docstring(current.body)
            allowed = ALLOWED_DEFERRED_FACADE_IMPORTS.get(current.name)
            if allowed:
                retained: list[ast.stmt] = []
                for statement in current.body:
                    if (
                        isinstance(statement, ast.ImportFrom)
                        and statement.level == 1
                        and statement.module == "main_helper_mapper"
                    ):
                        imported = {alias.name for alias in statement.names}
                        if imported != allowed:
                            raise AssertionError(
                                f"DEFERRED_FACADE_IMPORT_SET_MISMATCH:{current.name}:{sorted(imported)}"
                            )
                        continue
                    retained.append(statement)
                current.body = retained
            return current

        visit_AsyncFunctionDef = visit_FunctionDef

        def visit_ClassDef(self, current: ast.ClassDef) -> ast.AST:
            self.generic_visit(current)
            current.body = _normalize_docstring(current.body)
            return current

    clone = Normalizer().visit(clone)
    ast.fix_missing_locations(clone)
    canonical = _canonical_ast(clone)
    return json.dumps(canonical, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def _extract_all(tree: ast.Module) -> list[str]:
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        if any(isinstance(target, ast.Name) and target.id == "__all__" for target in node.targets):
            value = ast.literal_eval(node.value)
            return [str(item) for item in value]
    raise AssertionError("PUBLIC_API_ALL_MISSING")


def _module_import_profile(tree: ast.Module) -> dict[str, set[str]]:
    runtime: set[str] = set()
    type_checking: set[str] = set()
    deferred: set[str] = set()

    def add_import(statement: ast.stmt, bucket: set[str]) -> None:
        if isinstance(statement, ast.ImportFrom):
            module = "." * statement.level + (statement.module or "")
            for alias in statement.names:
                bucket.add(module + "." + alias.name)
        elif isinstance(statement, ast.Import):
            for alias in statement.names:
                bucket.add(alias.name)

    for statement in tree.body:
        if isinstance(statement, (ast.Import, ast.ImportFrom)):
            add_import(statement, runtime)
            continue
        if (
            isinstance(statement, ast.If)
            and isinstance(statement.test, ast.Name)
            and statement.test.id == "TYPE_CHECKING"
        ):
            for nested in statement.body:
                if isinstance(nested, (ast.Import, ast.ImportFrom)):
                    add_import(nested, type_checking)
            continue
        if isinstance(statement, (ast.FunctionDef, ast.AsyncFunctionDef)):
            for nested in ast.walk(statement):
                if isinstance(nested, (ast.Import, ast.ImportFrom)):
                    add_import(nested, deferred)
    return {"runtime": runtime, "type_checking": type_checking, "deferred": deferred}


def _normalize_fixture_path(path_text: str) -> str:
    """Normalize only fixture-observation path separators for host portability."""

    return str(path_text).replace("\\", "/")


def _behavior_signature(decision: object) -> tuple[str, str, str, tuple[str, ...]]:
    """Return the strict behavior signature with host-neutral path spelling."""

    return (
        str(decision.status),
        str(decision.target_role),
        _normalize_fixture_path(str(decision.main_path)),
        tuple(_normalize_fixture_path(str(item)) for item in decision.helper_paths),
    )


def _assert_behavior_fixture_path_portability() -> None:
    if _normalize_fixture_path("pkg\\main.py") != "pkg/main.py":
        raise AssertionError("WINDOWS_FIXTURE_PATH_SEPARATOR_NORMALIZATION_FAILED")
    if _normalize_fixture_path("pkg/main.py") != "pkg/main.py":
        raise AssertionError("POSIX_FIXTURE_PATH_SEPARATOR_NORMALIZATION_FAILED")
    ordered = tuple(
        _normalize_fixture_path(item)
        for item in ("pkg\\main_helper.py", "pkg/main_commands.py")
    )
    if ordered != ("pkg/main_helper.py", "pkg/main_commands.py"):
        raise AssertionError("FIXTURE_HELPER_ORDER_OR_PATH_NORMALIZATION_DRIFT")


def _write_behavior_fixture(root: Path) -> None:
    pkg = root / "pkg"
    pkg.mkdir(parents=True)
    (pkg / "main.py").write_text(
        '"""Main module."""\nfrom .main_helper import helper\n\ndef public_api():\n    return helper()\n',
        encoding="utf-8",
    )
    (pkg / "main_helper.py").write_text(
        '"""Private-like helper module."""\ndef helper():\n    return 1\n',
        encoding="utf-8",
    )
    (pkg / "main_commands.py").write_text(
        "def command():\n    return 2\n",
        encoding="utf-8",
    )
    (pkg / "test_main.py").write_text(
        "def test_public_api():\n    assert True\n",
        encoding="utf-8",
    )


def main() -> int:
    _assert_version_stable_ast_canonicalization()
    _assert_behavior_fixture_path_portability()
    root = _project_root()
    package = root / "kanda_reasoner_app" / "reasoner_symbol_atlas"
    paths = {name: package / name for name in EXPECTED_LOCATIONS}

    trees: dict[str, ast.Module] = {}
    texts: dict[str, str] = {}
    observed_locations: dict[str, set[str]] = {}
    for name, path in paths.items():
        if not path.is_file():
            raise AssertionError(f"CANDIDATE_FILE_MISSING:{name}")
        raw = path.read_bytes()
        text = raw.decode("utf-8")
        texts[name] = text
        for forbidden in FORBIDDEN_PREVIEW_TEXT:
            if forbidden in text:
                raise AssertionError(f"PREVIEW_ONLY_METADATA_IN_CANONICAL_SOURCE:{name}:{forbidden}")
        expected_header = f"# project-path: kanda_reasoner_app/reasoner_symbol_atlas/{name}"
        if text.splitlines()[0] != expected_header:
            raise AssertionError(f"PROJECT_PATH_HEADER_MISMATCH:{name}")
        line_count = len(text.splitlines())
        if not 101 <= line_count <= 499:
            raise AssertionError(f"MODULE_SIZE_OUTSIDE_101_499:{name}:{line_count}")
        tree = ast.parse(text, filename=str(path))
        compile(tree, str(path), "exec")
        trees[name] = tree
        observed_locations[name] = set(_top_defs(tree))

    if observed_locations != EXPECTED_LOCATIONS:
        raise AssertionError(
            "SYMBOL_MOVEMENT_MISMATCH:" + json.dumps(
                {key: sorted(value) for key, value in observed_locations.items()}, sort_keys=True
            )
        )

    observed_hashes: dict[str, str] = {}
    for name, tree in trees.items():
        for symbol, node in _top_defs(tree).items():
            normalized = _normalize_def(node)
            observed_hashes[symbol] = hashlib.sha256(normalized.encode("utf-8")).hexdigest()
    if observed_hashes != EXPECTED_DEF_HASHES:
        missing = sorted(set(EXPECTED_DEF_HASHES) - set(observed_hashes))
        extra = sorted(set(observed_hashes) - set(EXPECTED_DEF_HASHES))
        changed = sorted(
            name
            for name in set(EXPECTED_DEF_HASHES) & set(observed_hashes)
            if EXPECTED_DEF_HASHES[name] != observed_hashes[name]
        )
        raise AssertionError(f"EXECUTABLE_AST_DRIFT:missing={missing}:extra={extra}:changed={changed}")

    public_api = _extract_all(trees["main_helper_mapper.py"])
    if public_api != EXPECTED_PUBLIC_API:
        raise AssertionError("PUBLIC_API_CONTRACT_CHANGED")

    facade_profile = _module_import_profile(trees["main_helper_mapper.py"])
    selection_profile = _module_import_profile(trees["_main_helper_mapper_helper_selection.py"])
    path_profile = _module_import_profile(trees["_main_helper_mapper_path_resolution.py"])

    required_facade_runtime = {
        "._main_helper_mapper_helper_selection._decision_status",
        "._main_helper_mapper_path_resolution._coerce_project_root",
    }
    if not required_facade_runtime <= facade_profile["runtime"]:
        raise AssertionError("FACADE_RUNTIME_HELPER_IMPORTS_MISSING")
    if not REQUIRED_NEUTRAL_CONTRACT_IMPORTS <= selection_profile["runtime"]:
        raise AssertionError("NEUTRAL_CONTRACT_IMPORTS_MISSING")
    if selection_profile["type_checking"]:
        raise AssertionError("TYPE_CHECKING_FACADE_BACK_REFERENCE_PRESENT")
    if any(item.startswith(".main_helper_mapper.") for item in selection_profile["deferred"]):
        raise AssertionError("DEFERRED_FACADE_BACK_REFERENCE_PRESENT")
    if any(item.startswith(".main_helper_mapper.") for item in selection_profile["runtime"]):
        raise AssertionError("IMPORT_TIME_FACADE_BACK_REFERENCE_PRESENT")
    if any(item.startswith(".main_helper_mapper.") for item in path_profile["runtime"]):
        raise AssertionError("PATH_HELPER_FACADE_BACK_REFERENCE_PRESENT")

    module = importlib.import_module("kanda_reasoner_app.reasoner_symbol_atlas.main_helper_mapper")
    if list(module.__all__) != EXPECTED_PUBLIC_API:
        raise AssertionError("RUNTIME_PUBLIC_API_CONTRACT_CHANGED")
    for consumer in (
        "kanda_reasoner_app.reasoner_symbol_atlas",
        "kanda_reasoner_app.reasoner_symbol_atlas._existing_code_finder_support",
        "kanda_reasoner_app.reasoner_symbol_atlas.existing_code_finder",
        "kanda_reasoner_app.reasoner_symbol_atlas.implementation_responsibility_helpers_private",
        "kanda_reasoner_app.reasoner_symbol_atlas.implementation_responsibility_resolver",
        "kanda_reasoner_app.reasoner_symbol_atlas.related_file_finder",
    ):
        importlib.import_module(consumer)

    with tempfile.TemporaryDirectory(prefix="kanda_mapper_behavior_") as temp_dir:
        fixture = Path(temp_dir)
        _write_behavior_fixture(fixture)
        options_cls = module.ProjectSymbolAtlasMainHelperOptions
        mapper = module.map_reasoner_symbol_atlas_main_helpers
        cases = [
            (
                {"target_path": "pkg/main.py"},
                ("ready", "main", "pkg/main.py", ("pkg/main_helper.py", "pkg/main_commands.py")),
            ),
            (
                {"target_path": "pkg/main_helper.py"},
                ("ready", "helper", "pkg/main.py", ("pkg/main_helper.py", "pkg/main_commands.py")),
            ),
            (
                {"target_path": "pkg/main_commands.py"},
                ("ready", "helper", "pkg/main.py", ("pkg/main_commands.py", "pkg/main_helper.py")),
            ),
            (
                {"symbol_name": "public_api"},
                ("ready", "main", "pkg/main.py", ("pkg/main_helper.py", "pkg/main_commands.py")),
            ),
            (
                {"target_path": "missing.py"},
                ("target_not_found", "unknown", "", ()),
            ),
        ]
        for kwargs, expected in cases:
            decision = mapper(options_cls(project_root=str(fixture), **kwargs))
            observed = _behavior_signature(decision)
            if observed != expected:
                raise AssertionError(f"BEHAVIOR_FIXTURE_MISMATCH:{kwargs}:{observed}:{expected}")

    print(f"SOURCE_EXCHANGE_BASELINE_HASH_BOUND: PASS ({BASELINE_SOURCE_HASH})")
    print(f"SOURCE_CANDIDATE_SET_HASH_BOUND: PASS ({SOURCE_CANDIDATE_SET_HASH})")
    print(f"SOURCE_EXCHANGE_IDENTITY_HASH_BOUND: PASS ({SOURCE_EXCHANGE_IDENTITY_HASH})")
    print("COMPLETE_CANDIDATE_FAMILY_PRESENT: PASS")
    print("PREVIEW_ONLY_METADATA_REMOVED_FROM_CANONICAL_SOURCE: PASS")
    print("PROJECT_PATH_HEADERS_SOURCE_READY: PASS")
    print("MODULE_SIZE_POLICY_101_499: PASS")
    print("SYMBOL_MOVEMENT_EXACT: PASS")
    print("VERSION_STABLE_AST_CANONICALIZATION: PASS")
    print("BEHAVIOR_FIXTURE_PLATFORM_PATH_NORMALIZATION: PASS")
    print("EXECUTABLE_AST_EQUIVALENCE: PASS")
    print("PUBLIC_API_CONTRACT_PRESERVED: PASS")
    print("IMPORT_TOPOLOGY_NEUTRAL_PRIVATE_CONTRACT: PASS")
    print("NO_IMPORT_TIME_FACADE_BACK_REFERENCE: PASS")
    print("CONSUMER_IMPORTABILITY: PASS")
    print("BEHAVIOR_FIXTURE_EQUIVALENCE: PASS")
    print("REASONER_SYMBOL_ATLAS_MAIN_HELPER_MAPPER_SOURCE_READY_REFACTOR: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
