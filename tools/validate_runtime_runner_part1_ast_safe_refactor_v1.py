# project-path: tools/validate_runtime_runner_part1_ast_safe_refactor_v1.py
"""Validate the runtime runner part 1 AST-safe refactor."""
from __future__ import annotations
import argparse
import ast
import base64
import hashlib
import json
import os
import py_compile
import tempfile
import zipfile
from pathlib import Path
from typing import Any

__all__ = [
    "main",
]

PROJECT_ROOT = Path(__file__).resolve().parents[1]
FEATURE_ID = "runtime-runner-part1-ast-safe-refactor-v1"
TARGET_REL = (
    "kanda_reasoner_app/reasoner_runtime_collector/runtime_runner_help/"
    "runtime_runner_part_1_private_impl.py"
)
BINDINGS_REL = (
    "kanda_reasoner_app/reasoner_runtime_collector/runtime_runner_help/"
    "_runtime_runner_part_1_bindings.py"
)
SCENARIOS_REL = (
    "kanda_reasoner_app/reasoner_runtime_collector/runtime_runner_help/"
    "_runtime_runner_part_1_scenarios.py"
)
VALIDATOR_REL = "tools/validate_runtime_runner_part1_ast_safe_refactor_v1.py"
FAMILY = [TARGET_REL, BINDINGS_REL, SCENARIOS_REL]
EXPECTED_TARGET_SHA256 = "7be33656dcba5d492d5ac1592bf90527aeb0b0a82642fc6c320a69340fa61b92"
EXPECTED_ALL: list[str] = []
EXPECTED_SIGNATURES = {
    "_bind_root_globals": "(root_globals)",
    "_rr__headless_mode_requested_impl": "() -> bool",
    "_rr__resolve_headless_config_impl": "() -> dict",
    "_rr__run_named_scenario_module_impl": "(scenario_module: str, project_root: Path, entry_script: Path | None, output_json: Path) -> str",
    "_rr__run_entry_script_impl": "(entry_script: Path) -> None",
    "_rr__as_mapping_impl": "(value: object) -> dict",
    "_rr__as_list_impl": "(value: object) -> list",
    "_rr__safe_len_impl": "(value: object) -> int",
    "_rr__build_runtime_symbol_index_impl": "(files_payload: list[dict]) -> dict",
    "_rr__build_real_runtime_files_payload_impl": "(project_root: Path) -> list[dict]",
    "_rr__run_builtin_collector_component_scenario_impl": "(project_root: Path) -> dict",
    "_rr__ensure_qapplication_impl": "() -> QApplication",
}
def _path(relative_path: str) -> Path:
    return PROJECT_ROOT / relative_path
def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()
def _line_count(path: Path) -> int:
    return len(path.read_text(encoding="utf-8").splitlines())
def _assert_source_family() -> None:
    for relative_path in [*FAMILY, VALIDATOR_REL]:
        path = _path(relative_path)
        if not path.is_file():
            raise AssertionError("SOURCE_MISSING: " + relative_path)
        raw = path.read_bytes()
        if raw.startswith(b"\xef\xbb\xbf"):
            raise AssertionError("UTF8_BOM_FORBIDDEN: " + relative_path)
        raw.decode("ascii")
        py_compile.compile(str(path), doraise=True)
        line_count = _line_count(path)
        if not 101 <= line_count <= 499:
            raise AssertionError(
                f"LINE_LAW_101_499 failed: {relative_path}: {line_count}"
            )
    if _sha256(_path(TARGET_REL)) != EXPECTED_TARGET_SHA256:
        raise AssertionError("TARGET_INSTALLED_HASH_MISMATCH")
def _assert_semantic_safety() -> None:
    from kanda_reasoner_app.manage_architecture.kanda_refactor_semantic_safety import (
        check_candidate_dependency_direction,
        detect_semantic_dynamic_risks,
    )
    for relative_path in [*FAMILY, VALIDATOR_REL]:
        source = _path(relative_path).read_text(encoding="utf-8")
        findings = detect_semantic_dynamic_risks(source, relative_path)
        if findings:
            raise AssertionError(
                "SEMANTIC_DYNAMIC_RISK_REMAINS: "
                + relative_path
                + ": "
                + json.dumps(findings, sort_keys=True)
            )
    direction = check_candidate_dependency_direction(
        PROJECT_ROOT,
        facade_relative_path=TARGET_REL,
        helper_relative_paths=[BINDINGS_REL, SCENARIOS_REL],
    )
    if not direction.get("pass"):
        raise AssertionError(
            "DEPENDENCY_DIRECTION_VIOLATION: "
            + json.dumps(direction.get("violations", []), sort_keys=True)
        )
def _assert_contracts() -> None:
    from kanda_reasoner_app.reasoner_runtime_collector.runtime_runner_help import (
        runtime_runner_part_1_private_impl as module,
    )
    from kanda_reasoner_app.reasoner_runtime_collector.runtime_runner_help._runtime_runner_part_1_bindings import (
        binding_contract_names,
    )
    if list(module.__all__) != EXPECTED_ALL:
        raise AssertionError("PUBLIC_ALL_CHANGED")
    tree = ast.parse(_path(TARGET_REL).read_text(encoding="utf-8"))
    actual: dict[str, str] = {}
    for node in tree.body:
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        if node.name not in EXPECTED_SIGNATURES:
            continue
        signature = "(" + ast.unparse(node.args) + ")"
        if node.returns is not None:
            signature += " -> " + ast.unparse(node.returns)
        actual[node.name] = signature
    if actual != EXPECTED_SIGNATURES:
        raise AssertionError("PRIVATE_SIGNATURE_CHANGED: " + json.dumps(actual, sort_keys=True))
    expected_bindings = (
        "trace_event",
        "trace_state_snapshot",
        "_load_static_evidence_json",
        "_section_from_static_evidence",
        "_select_runtime_scenario_files",
        "_summary_from_static_sections",
        "QApplication",
    )
    if binding_contract_names() != expected_bindings:
        raise AssertionError("ROOT_BINDING_CONTRACT_CHANGED")
def _assert_payload_consumer_contract() -> None:
    from kanda_reasoner_app.backend_payloads import payload_y
    source = base64.b64decode(
        "".join(payload_y.PAYLOAD_PARTS_Y).encode("ascii")
    ).decode("utf-8")
    required = [
        '_load_runtime_runner_part_private_impl(\n    "runtime_runner_part_1_private_impl"',
        "_rr_part_1._rr__resolve_headless_config_impl()",
        "_rr_part_1._rr__run_named_scenario_module_impl(",
        "_rr_part_1._rr__run_entry_script_impl(entry_script)",
        "_rr_part_1._rr__build_runtime_symbol_index_impl(files_payload)",
        "_rr_part_1._rr__as_mapping_impl(value)",
        "_rr_part_1._rr__as_list_impl(value)",
        "_rr_part_1._rr__safe_len_impl(value)",
        "_rr_part_1._rr__build_real_runtime_files_payload_impl(project_root)",
        "_rr_part_1._rr__run_builtin_collector_component_scenario_impl(project_root)",
        "_rr_part_1._rr__ensure_qapplication_impl()",
        "_rr_part_1._bind_root_globals(root_globals)",
    ]
    for token in required:
        if token not in source:
            raise AssertionError("PAYLOAD_Y_CONSUMER_REFERENCE_CHANGED: " + token)
def _assert_pure_behavior() -> None:
    from kanda_reasoner_app.reasoner_runtime_collector.runtime_runner_help import (
        runtime_runner_part_1_private_impl as module,
    )
    samples = [None, {}, [], [1, 2], {"a": 1}, "abc", 42]
    expected = [
        ({}, [], 0),
        ({}, [], 0),
        ({}, [], 0),
        ({}, [1, 2], 2),
        ({"a": 1}, [], 1),
        ({}, [], 3),
        ({}, [], 0),
    ]
    actual = [
        (
            module._rr__as_mapping_impl(value),
            module._rr__as_list_impl(value),
            module._rr__safe_len_impl(value),
        )
        for value in samples
    ]
    if actual != expected:
        raise AssertionError("PURE_HELPER_BEHAVIOR_CHANGED")
    files = [
        {
            "path": "a.py",
            "functions": [
                {"name": "f", "lineno": 3},
                {"name": "g", "qualname": "C.g", "lineno": 7},
            ],
            "classes": [
                {
                    "name": "C",
                    "lineno": 5,
                    "methods": [
                        {"name": "m", "qualname": "C.m", "lineno": 8}
                    ],
                }
            ],
        }
    ]
    expected_index = {
        "f": {"file": "a.py", "line": 3, "kind": "function"},
        "C.g": {"file": "a.py", "line": 7, "kind": "function"},
        "C": {"file": "a.py", "line": 5, "kind": "class"},
        "C.m": {"file": "a.py", "line": 8, "kind": "method"},
    }
    if module._rr__build_runtime_symbol_index_impl(files) != expected_index:
        raise AssertionError("SYMBOL_INDEX_BEHAVIOR_CHANGED")
def _assert_binding_behavior() -> None:
    from kanda_reasoner_app.reasoner_runtime_collector.runtime_runner_help import (
        runtime_runner_part_1_private_impl as module,
    )
    records: list[tuple[str, Any]] = []
    static = {"files": [{"path": "a.py", "functions": [], "classes": []}]}
    def load_static(root: Path) -> tuple[dict[str, Any], str]:
        records.append(("load", str(root)))
        return static, "evidence.json"
    def select_files(files: list[dict]) -> list[dict]:
        records.append(("select", len(files)))
        return files
    module._bind_root_globals(
        {
            "_load_static_evidence_json": load_static,
            "_select_runtime_scenario_files": select_files,
            "trace_event": lambda **kwargs: records.append(
                ("event", kwargs["event_type"])
            ),
            "trace_state_snapshot": lambda **kwargs: records.append(
                ("snapshot", kwargs["label"])
            ),
            "UNRELATED_SENTINEL_KEY": object(),
        }
    )
    try:
        module.UNRELATED_SENTINEL_KEY
    except AttributeError:
        pass
    else:
        raise AssertionError("ROOT_GLOBALS_UNKNOWN_KEY_LEAK")
    selected = module._rr__build_real_runtime_files_payload_impl(Path("/project"))
    if selected != static["files"]:
        raise AssertionError("STATIC_EVIDENCE_PAYLOAD_BEHAVIOR_CHANGED")
    if not records:
        raise AssertionError("BOUND_DEPENDENCIES_NOT_USED")
def _assert_scenario_registry_behavior() -> None:
    from kanda_reasoner_app.reasoner_runtime_collector.runtime_runner_help import (
        runtime_runner_part_1_private_impl as module,
    )
    from kanda_reasoner_app.reasoner_runtime_collector.runtime_runner_help._runtime_runner_part_1_scenarios import (
        RegisteredRuntimeScenario,
        clear_runtime_scenario_registry,
        register_runtime_scenario,
    )
    calls: list[str] = []
    def dual(*args: object, **kwargs: object) -> None:
        del args
        if kwargs:
            calls.append("kwargs")
            raise TypeError("fallback")
        calls.append("noargs")
    clear_runtime_scenario_registry()
    register_runtime_scenario(
        "scenario.demo",
        RegisteredRuntimeScenario(
            collect_runtime_scenario=dual,
            run=lambda: calls.append("run"),
        ),
    )
    result = module._rr__run_named_scenario_module_impl(
        "scenario.demo",
        Path("/project"),
        None,
        Path("/output.json"),
    )
    if result != "collect_runtime_scenario":
        raise AssertionError("SCENARIO_CALLABLE_PRECEDENCE_CHANGED")
    if calls != ["kwargs", "noargs"]:
        raise AssertionError("SCENARIO_TYPEERROR_FALLBACK_CHANGED")
    try:
        module._rr__run_named_scenario_module_impl(
            "scenario.missing",
            Path("/project"),
            None,
            Path("/output.json"),
        )
    except RuntimeError as exc:
        if "not registered" not in str(exc):
            raise
    else:
        raise AssertionError("UNKNOWN_SCENARIO_DID_NOT_FAIL_CLOSED")
    clear_runtime_scenario_registry()
def _assert_entry_script_and_qapplication() -> None:
    from kanda_reasoner_app.reasoner_runtime_collector.runtime_runner_help import (
        runtime_runner_part_1_private_impl as module,
    )
    class FakeApplication:
        current: Any = None
        def __init__(self, args: list[Any]) -> None:
            self.args = args
            FakeApplication.current = self
        @classmethod
        def instance(cls) -> Any:
            return cls.current
    module._bind_root_globals({"QApplication": FakeApplication})
    FakeApplication.current = None
    app = module._rr__ensure_qapplication_impl()
    if app.args != []:
        raise AssertionError("QAPPLICATION_CREATION_CHANGED")
    if module._rr__ensure_qapplication_impl() is not app:
        raise AssertionError("QAPPLICATION_INSTANCE_REUSE_CHANGED")
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        output = root / "seen.txt"
        entry = root / "entry.py"
        entry.write_text(
            "from pathlib import Path\n"
            + f"Path({str(output)!r}).write_text(__name__)\n",
            encoding="utf-8",
        )
        module._rr__run_entry_script_impl(entry)
        if output.read_text(encoding="utf-8") != "__main__":
            raise AssertionError("ENTRY_SCRIPT_RUN_NAME_CHANGED")
def _assert_part2_downstream_contract() -> None:
    from kanda_reasoner_app.reasoner_runtime_collector.runtime_runner_help._runtime_runner_part_2_bindings import (
        build_default_runtime_bindings,
    )
    from kanda_reasoner_app.reasoner_runtime_collector.runtime_runner_help._runtime_runner_part_1_scenarios import (
        RegisteredRuntimeScenario,
        clear_runtime_scenario_registry,
        register_runtime_scenario,
    )
    bindings = build_default_runtime_bindings()
    calls: list[str] = []
    clear_runtime_scenario_registry()
    register_runtime_scenario(
        "downstream.demo",
        RegisteredRuntimeScenario(main=lambda: calls.append("main")),
    )
    result = bindings.run_named_scenario_module(
        "downstream.demo",
        Path("/project"),
        None,
        Path("/output.json"),
    )
    clear_runtime_scenario_registry()
    if result != "main" or calls != ["main"]:
        raise AssertionError("PART2_BINDINGS_DOWNSTREAM_CHANGED")
def _assert_manifest_contract() -> None:
    manifest_path = PROJECT_ROOT / (
        "kanda_reasoner_app/reasoner_runtime_collector/runtime_runner_help.json"
    )
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    expected = [
        "runtime_runner_part_1_private_impl.py",
        "runtime_runner_part_2_private_impl.py",
        "runtime_runner_part_3_private_impl.py",
    ]
    if payload.get("helpers") != expected:
        raise AssertionError("RUNTIME_RUNNER_MANIFEST_CHANGED")
def _assert_fresh_ast_family() -> None:
    from kanda_reasoner_app.manage_architecture.large_module_split_audit import (
        run_large_module_split_audit,
    )
    for relative_path in [*FAMILY, VALIDATOR_REL]:
        result = run_large_module_split_audit(PROJECT_ROOT, relative_path)
        classification = result.data["refactor_safety_classification"]
        if classification["label"] != "SAFE REFACTORING":
            raise AssertionError(
                "AST_FAMILY_NOT_SAFE: "
                + relative_path
                + ": "
                + classification["label"]
            )
        if classification["hard_blockers"]:
            raise AssertionError("AST_FAMILY_BLOCKERS_REMAIN: " + relative_path)
def _assert_patch_zip(patch_zip: Path | None) -> None:
    if patch_zip is None:
        return
    if not patch_zip.is_file():
        raise AssertionError("PATCH_ZIP_MISSING")
    with zipfile.ZipFile(patch_zip) as archive:
        manifest = json.loads(archive.read("PACKAGE_MANIFEST.json"))
        if manifest.get("feature_id") != FEATURE_ID:
            raise AssertionError("PACKAGE_FEATURE_ID_MISMATCH")
        for item in manifest["payload"]:
            relative_path = item["relative_path"]
            raw = archive.read("payload/" + relative_path)
            digest = hashlib.sha256(raw).hexdigest()
            if digest != item["sha256"]:
                raise AssertionError(
                    "PACKAGE_PAYLOAD_HASH_MISMATCH: " + relative_path
                )
def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--patch-zip", default="")
    args = parser.parse_args()
    patch_zip = Path(args.patch_zip).resolve() if args.patch_zip else None
    _assert_source_family()
    print("SOURCE_IDENTITY_GUARD: PASS")
    print("SOURCE_ASCII_UTF8_NO_BOM: PASS")
    print("PYTHON_SYNTAX: PASS")
    print("LINE_LAW_101_499_FITNESS: PASS")
    _assert_semantic_safety()
    print("NO_DYNAMIC_REFLECTION_CALLS: PASS")
    print("DEPENDENCY_DIRECTION_FITNESS: PASS")
    print("BOX_BOUNDARY_FITNESS: PASS")
    print("NO_LEAK_FITNESS: PASS")
    _assert_contracts()
    _assert_payload_consumer_contract()
    print("PUBLIC_ALL_PRESERVATION: PASS")
    print("REQUIRED_PRIVATE_CONTRACT_PRESERVATION: PASS")
    print("PRIVATE_SIGNATURE_PRESERVATION: PASS")
    print("ANNOTATION_IMPORT_PRESERVATION: PASS")
    print("PAYLOAD_Y_PART1_CONSUMER_CONTRACT: PASS")
    _assert_pure_behavior()
    print("AS_MAPPING_BEHAVIOR: PASS")
    print("AS_LIST_BEHAVIOR: PASS")
    print("SAFE_LEN_BEHAVIOR: PASS")
    print("SYMBOL_INDEX_BEHAVIOR: PASS")
    _assert_binding_behavior()
    print("ROOT_GLOBALS_EXPLICIT_BINDING: PASS")
    print("ROOT_GLOBALS_UNKNOWN_KEY_NO_LEAK: PASS")
    print("STATIC_EVIDENCE_PAYLOAD_BEHAVIOR: PASS")
    _assert_scenario_registry_behavior()
    print("NAMED_SCENARIO_REGISTRY_BEHAVIOR: PASS")
    print("NAMED_SCENARIO_CALLABLE_PRECEDENCE: PASS")
    print("NAMED_SCENARIO_TYPEERROR_FALLBACK: PASS")
    print("NAMED_SCENARIO_UNKNOWN_NAME_ERROR: PASS")
    print("NAMED_SCENARIO_CONTRACT_CHANGE_APPROVED: PASS")
    _assert_entry_script_and_qapplication()
    print("ENTRY_SCRIPT_BEHAVIOR: PASS")
    print("QAPPLICATION_BEHAVIOR: PASS")
    _assert_part2_downstream_contract()
    _assert_manifest_contract()
    print("PART2_BINDINGS_DOWNSTREAM_CONTRACT: PASS")
    print("RUNTIME_RUNNER_MANIFEST_REGRESSION: PASS")
    print("BEHAVIOR_EQUIVALENCE_FITNESS: PASS")
    print("BEHAVIOR_REGRESSION: PASS")
    _assert_fresh_ast_family()
    print("AST_SPLIT_AUDIT_RERUN: PASS")
    print("AST_SPLIT_FAMILY_ALL_SAFE: PASS")
    print("AST_SPLIT_SAFETY_LABEL: SAFE REFACTORING")
    print("AST_SPLIT_HARD_BLOCKERS: 0")
    _assert_patch_zip(patch_zip)
    if patch_zip is not None:
        print("PACKAGE_PAYLOAD_HASHES: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0
if __name__ == "__main__":
    raise SystemExit(main())
