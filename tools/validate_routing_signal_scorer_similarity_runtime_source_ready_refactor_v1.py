# project-path: tools/validate_routing_signal_scorer_similarity_runtime_source_ready_refactor_v1.py
"""Validate the source-ready similarity runtime split from EXCH-0001."""

from __future__ import annotations

import ast
import copy
import hashlib
import importlib
import inspect
import json
from pathlib import Path

__all__ = [
    "main",
]

FEATURE_ID = "routing-signal-scorer-similarity-runtime-source-ready-refactor-v1"
BASELINE_SOURCE_HASH = (
    "1aa8b65f8138d95efd5ce55c8ca7027b0604164727246df04e5499dcc9fd2406"
)
SOURCE_CANDIDATE_SET_HASH = (
    "e88b4a55c83ac6beb5e5b73204a5be7ceff3d548eade7ee09ee08e5b35263b59"
)
SOURCE_EXCHANGE_IDENTITY_HASH = (
    "2536d283f43090fb69b892a6a7ef64c459c832cf6aeb6e5bbbe2c1058eb8aaa0"
)
EXPECTED_PUBLIC_API = [
    "build_similarity_runtime_lite_advisory",
    "summarize_similarity_runtime_lite_advisory",
]
EXPECTED_COMPATIBILITY_REEXPORTS = {
    "_containment",
    "_jaccard",
    "_tokenize_for_similarity",
    "_similarity_advisory_only_reason",
    "_similarity_rule_hook_independence_reason",
}
EXPECTED_LOCATIONS = {
    "similarity_runtime.py": {
        "build_similarity_runtime_lite_advisory",
        "summarize_similarity_runtime_lite_advisory",
    },
    "_similarity_runtime_serialization.py": {
        "_load_similarity_corpus",
        "_text_profile",
        "_tokenize_for_similarity",
        "_profile_similarity",
        "_jaccard",
        "_containment",
    },
    "_similarity_runtime_decision_reporting.py": {
        "_similarity_level",
        "_similarity_threshold_level",
        "_similarity_advisory_only_reason",
        "_similarity_rule_hook_independence_reason",
        "_similarity_match_explainability",
        "_similarity_explainability_summary",
        "_similarity_decision_report_summary",
        "_similarity_decision_report",
        "_similarity_threshold_policy",
        "_matched_terms_from_profiles",
        "_similarity_route_family_suggestions",
    },
    "_similarity_runtime_cohesive_operations_2.py": {
        "_similarity_expected_values",
        "_merge_string_lists",
        "_merge_route_family_suggestions",
        "_similarity_notes",
    },
}
EXPECTED_DEF_HASHES = {
    "build_similarity_runtime_lite_advisory": "80e317f4c380e82a1789b37dff2874e482fcf72d818766e0455bc0c656ddecb1",
    "summarize_similarity_runtime_lite_advisory": "95935fac065fa04d5bd78830c26a905d577c94b467213df96b87386078f82ce4",
    "_load_similarity_corpus": "e5026b64820f11e1adb1fb398ba1ecc9e6c53489f5267461e08f0b89b15f0730",
    "_text_profile": "2bd84f5ceaf4e753a1dfcdf16c4cf74d5e2fe460ec68c6764c07f7766313ce82",
    "_tokenize_for_similarity": "7aca0879f4741f2638e384af52ed67b4bf1cf0a1064651df25defc303940c5e5",
    "_profile_similarity": "6bac0f0925b6c6deb8635e090f74b2b097f1c5ef2692b5db406376161f78f676",
    "_jaccard": "b853e9d85713ea88edf08f53178fda3be7286b9f0645676fbf0491dcfc71be7f",
    "_containment": "e8794a2a9d16621d6ebda942702c0bb50fd60cfea30716f128946abd49dc625a",
    "_similarity_level": "485f92a199fad04f455d50c4b1025bd9bcec9df9cbf29083c68214b68f4a1406",
    "_similarity_threshold_level": "70736972972b3cdc3eb827a63fb6faa13133b64cfb9992a67df897ea2734d18b",
    "_similarity_advisory_only_reason": "00a61c5178fe0b5be2a25044dc6d5fe498f402929a55c80d3237e48c34f1e3ca",
    "_similarity_rule_hook_independence_reason": "ed6b929a71f3694747ace539ec23eafae306f82a86840bbfeb6192251585eb4f",
    "_similarity_match_explainability": "2a7532e805fcc487aec6f8e21b4ee1035275b5b7d06f215ca1020d17882b0074",
    "_similarity_explainability_summary": "068f3db4c75e9f2c23baa97dfaf1ff2eb8e6dd4f9373cf1a9156f41629c337b0",
    "_similarity_decision_report_summary": "1cfe6ae3f440a0a205942e14fb9387af56f73c10ba6438febf9aa8d8cd67ab02",
    "_similarity_decision_report": "9d88475fa78a885cad6e6ce3667be71251ad02123bd9d8c90758f0e86f680425",
    "_similarity_threshold_policy": "92b728e88aa0de5be7edbef1b277eb8b5df48bbb880212b61e1c5e42bbeb9d78",
    "_matched_terms_from_profiles": "f2d2eb84c7c0cf4d4d22b5726936a905db60c30065a31240bb7990498aed2baf",
    "_similarity_route_family_suggestions": "75a9e1e581f8a2b3cf82f3315ac7baf1e79b93db59b30cecf90475e98df6fbf2",
    "_similarity_expected_values": "d420aed15c31c4a3bacf16cbae21cf61eaa6c9ff95115bf92cdafbd6a7fe289f",
    "_merge_string_lists": "4ccfb7cce10d6a1c7fff83d8f13ba265d72d9ef15a6f5af318580996f89eb476",
    "_merge_route_family_suggestions": "66fd6bc13e552b0698700929e2604502e283bc5eeb0f42c61fbb7896c6ad0530",
    "_similarity_notes": "230d868adf2f79938ff0b17288b712c080075dda4675a3d80dadd42389bf5cdf",
}
BEHAVIOR_CASES = {
    "": (
        "2ffd39ad7cc43322608269e94fadede55ab5858ddeefdeaf37df449dd78af601",
        "5fd35c689a36748a305c35249c6ef3a9fcb208d4d23e601e80abe164fea62779",
    ),
    "Create a patch ZIP, validate it, and prepare freeze evidence.": (
        "0eb8f39950694ce5f5fdbee47b307b6b6f1c5a80ebe9a8c286df94db5238c755",
        "717931e5d03dce492e35a984327b6aeb150562d3bf2d73fd656265f9472d5d90",
    ),
    "Refactor a large Python module into cohesive helpers without changing the public API.": (
        "bb3ec6eec61a056b25caddec55176f1104f9eb0d8352dbc35a061592d6e40d9c",
        "5fd35c689a36748a305c35249c6ef3a9fcb208d4d23e601e80abe164fea62779",
    ),
    "Explain the architecture only. Do not change code.": (
        "819c3d77dc25c6e631ab5b019506701ea1c68ac13727b2a9f655b36ff64dabe0",
        "5fd35c689a36748a305c35249c6ef3a9fcb208d4d23e601e80abe164fea62779",
    ),
    "Add a new prompt to the prompt library and skip duplicate checks.": (
        "5698a6e5ea33c51c9c9684c1b309a63cf2e196a82663a0bdf6ef3f755a1d02de",
        "fdfaecdee28ec7c89f84e940f0b1ab1611afd710c819324f085afbeedffbf4a6",
    ),
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


def _canonical_ast(value: object) -> object:
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


def _normalize_def(node: ast.AST) -> str:
    clone = copy.deepcopy(node)
    if (
        hasattr(clone, "body")
        and clone.body
        and isinstance(clone.body[0], ast.Expr)
        and isinstance(clone.body[0].value, ast.Constant)
        and isinstance(clone.body[0].value.value, str)
    ):
        clone.body[0].value.value = inspect.cleandoc(clone.body[0].value.value)
    canonical = _canonical_ast(clone)
    return json.dumps(
        canonical,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    )


def _top_defs(tree: ast.Module) -> dict[str, ast.AST]:
    return {
        node.name: node
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
    }


def _extract_all(tree: ast.Module) -> list[str]:
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        if any(
            isinstance(target, ast.Name) and target.id == "__all__"
            for target in node.targets
        ):
            value = ast.literal_eval(node.value)
            return [str(item) for item in value]
    raise AssertionError("PUBLIC_API_ALL_MISSING")


def _sha256_json(value: object) -> str:
    payload = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _assert_compatibility_reexports(facade_tree: ast.Module) -> None:
    observed: set[str] = set()
    for node in facade_tree.body:
        if not isinstance(node, ast.ImportFrom):
            continue
        if not (node.module or "").startswith("_similarity_runtime_"):
            continue
        for alias in node.names:
            if alias.name == alias.asname and alias.name in EXPECTED_COMPATIBILITY_REEXPORTS:
                observed.add(alias.name)
    if observed != EXPECTED_COMPATIBILITY_REEXPORTS:
        raise AssertionError(
            "COMPATIBILITY_REEXPORT_SET_MISMATCH:"
            + repr(sorted(observed))
        )


def _assert_no_helper_facade_back_reference(trees: dict[str, ast.Module]) -> None:
    for filename, tree in trees.items():
        if filename == "similarity_runtime.py":
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.level == 1:
                if node.module == "similarity_runtime":
                    raise AssertionError(
                        "HELPER_TO_FACADE_BACK_REFERENCE:" + filename
                    )


def main() -> int:
    root = _project_root()
    package = root / "kanda_reasoner_app" / "routing_signal_scorer"
    paths = {name: package / name for name in EXPECTED_LOCATIONS}

    trees: dict[str, ast.Module] = {}
    observed_locations: dict[str, set[str]] = {}
    observed_hashes: dict[str, str] = {}

    for filename, path in paths.items():
        if not path.is_file():
            raise AssertionError("CANDIDATE_FILE_MISSING:" + filename)
        raw = path.read_bytes()
        text = raw.decode("utf-8")
        if raw.startswith(b"\xef\xbb\xbf"):
            raise AssertionError("UTF8_BOM_FORBIDDEN:" + filename)
        for forbidden in FORBIDDEN_PREVIEW_TEXT:
            if forbidden in text:
                raise AssertionError(
                    "PREVIEW_ONLY_METADATA_IN_CANONICAL_SOURCE:"
                    + filename
                    + ":"
                    + forbidden
                )
        expected_header = (
            "# project-path: kanda_reasoner_app/routing_signal_scorer/"
            + filename
        )
        if text.splitlines()[0] != expected_header:
            raise AssertionError("PROJECT_PATH_HEADER_MISMATCH:" + filename)
        line_count = len(text.splitlines())
        if not 101 <= line_count <= 499:
            raise AssertionError(
                "MODULE_SIZE_OUTSIDE_101_499:"
                + filename
                + ":"
                + str(line_count)
            )
        tree = ast.parse(text, filename=str(path))
        compile(tree, str(path), "exec")
        trees[filename] = tree
        observed_locations[filename] = set(_top_defs(tree))
        for symbol, node in _top_defs(tree).items():
            normalized = _normalize_def(node)
            observed_hashes[symbol] = hashlib.sha256(
                normalized.encode("utf-8")
            ).hexdigest()

    if observed_locations != EXPECTED_LOCATIONS:
        raise AssertionError("SYMBOL_MOVEMENT_MISMATCH")
    if observed_hashes != EXPECTED_DEF_HASHES:
        changed = sorted(
            name
            for name in set(EXPECTED_DEF_HASHES) & set(observed_hashes)
            if EXPECTED_DEF_HASHES[name] != observed_hashes[name]
        )
        missing = sorted(set(EXPECTED_DEF_HASHES) - set(observed_hashes))
        extra = sorted(set(observed_hashes) - set(EXPECTED_DEF_HASHES))
        raise AssertionError(
            "EXECUTABLE_AST_DRIFT:missing="
            + repr(missing)
            + ":extra="
            + repr(extra)
            + ":changed="
            + repr(changed)
        )

    facade_tree = trees["similarity_runtime.py"]
    if _extract_all(facade_tree) != EXPECTED_PUBLIC_API:
        raise AssertionError("PUBLIC_API_CONTRACT_CHANGED")
    _assert_compatibility_reexports(facade_tree)
    _assert_no_helper_facade_back_reference(trees)

    runtime = importlib.import_module(
        "kanda_reasoner_app.routing_signal_scorer.similarity_runtime"
    )
    contract = importlib.import_module(
        "kanda_reasoner_app.routing_signal_scorer.contract"
    )
    importlib.import_module(
        "kanda_reasoner_app.routing_signal_scorer.similarity_preview"
    )
    if not contract:
        raise AssertionError("CONTRACT_IMPORT_FAILED")
    if list(runtime.__all__) != EXPECTED_PUBLIC_API:
        raise AssertionError("RUNTIME_PUBLIC_API_CONTRACT_CHANGED")
    for name in EXPECTED_COMPATIBILITY_REEXPORTS:
        if not hasattr(runtime, name):
            raise AssertionError("COMPATIBILITY_REEXPORT_MISSING:" + name)

    builder = runtime.build_similarity_runtime_lite_advisory
    summarizer = runtime.summarize_similarity_runtime_lite_advisory
    for text, expected in BEHAVIOR_CASES.items():
        advisory = builder(text)
        observed_payload_hash = _sha256_json(advisory)
        observed_summary_hash = hashlib.sha256(
            summarizer(advisory).encode("utf-8")
        ).hexdigest()
        if (observed_payload_hash, observed_summary_hash) != expected:
            raise AssertionError(
                "BEHAVIOR_FIXTURE_MISMATCH:"
                + repr(text)
                + ":"
                + observed_payload_hash
                + ":"
                + observed_summary_hash
            )

    print("SOURCE_EXCHANGE_BASELINE_HASH_BOUND: PASS (" + BASELINE_SOURCE_HASH + ")")
    print("SOURCE_CANDIDATE_SET_HASH_BOUND: PASS (" + SOURCE_CANDIDATE_SET_HASH + ")")
    print("SOURCE_EXCHANGE_IDENTITY_HASH_BOUND: PASS (" + SOURCE_EXCHANGE_IDENTITY_HASH + ")")
    print("COMPLETE_FOUR_FILE_CANDIDATE_FAMILY_PRESENT: PASS")
    print("PREVIEW_ONLY_METADATA_REMOVED_FROM_CANONICAL_SOURCE: PASS")
    print("PROJECT_PATH_HEADERS_SOURCE_READY: PASS")
    print("SOURCE_ASCII_UTF8_NO_BOM: PASS")
    print("MODULE_SIZE_POLICY_101_499: PASS")
    print("SYMBOL_MOVEMENT_EXACT: PASS")
    print("EXECUTABLE_AST_EQUIVALENCE_23_SYMBOLS: PASS")
    print("PUBLIC_API_CONTRACT_PRESERVED: PASS")
    print("PRIVATE_CONSUMER_COMPATIBILITY_REEXPORTS_PRESERVED: PASS")
    print("NO_HELPER_TO_FACADE_IMPORT_BACK_REFERENCE: PASS")
    print("CONSUMER_IMPORTABILITY: PASS")
    print("BEHAVIOR_FIXTURE_EQUIVALENCE_5_CASES: PASS")
    print("ROUTING_SIGNAL_SCORER_SIMILARITY_RUNTIME_SOURCE_READY_REFACTOR: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
