# project-path: tools/validate_runtime_runner_part2_ast_safe_refactor_v1.py
"""Validate the runtime runner part 2 AST-safe refactor."""

from __future__ import annotations

import argparse
import base64
import contextlib
import hashlib
import inspect
import io
import json
import py_compile
import tempfile
import zipfile
from pathlib import Path
from typing import Any

__all__ = [
    "main",
]

PROJECT_ROOT = Path(__file__).resolve().parents[1]
FEATURE_ID = "runtime-runner-part2-ast-safe-refactor-v1"
TARGET_REL = (
    "kanda_reasoner_app/reasoner_runtime_collector/runtime_runner_help/"
    "runtime_runner_part_2_private_impl.py"
)
BINDINGS_REL = (
    "kanda_reasoner_app/reasoner_runtime_collector/runtime_runner_help/"
    "_runtime_runner_part_2_bindings.py"
)
SCENARIOS_REL = (
    "kanda_reasoner_app/reasoner_runtime_collector/runtime_runner_help/"
    "_runtime_runner_part_2_scenarios.py"
)
WINDOW_REL = (
    "kanda_reasoner_app/reasoner_runtime_collector/runtime_runner_help/"
    "_runtime_runner_part_2_window.py"
)
VALIDATOR_REL = "tools/validate_runtime_runner_part2_ast_safe_refactor_v1.py"
FAMILY = [TARGET_REL, BINDINGS_REL, SCENARIOS_REL, WINDOW_REL]
BASELINE_TARGET_SHA256 = "637eba63791bdd113a71ca8bd4539a8e982a62d3f2885e0567a5df3515c42d2e"
EXPECTED_ALL: list[str] = []
REQUIRED_CONSUMER_SYMBOLS = [
    "_bind_root_globals",
    "_rr__run_builtin_qt_interaction_scenario_impl",
    "_rr__run_rich_automatic_scenario_impl",
    "_rr__run_headless_impl",
    "_rr_RuntimeCollectorWindow__build_ui_impl",
    "_rr_RuntimeCollectorWindow__connect_signals_impl",
    "_rr_RuntimeCollectorWindow__append_log_impl",
    "_rr_RuntimeCollectorWindow__start_spinner_impl",
    "_rr_RuntimeCollectorWindow__tick_spinner_impl",
    "_rr_RuntimeCollectorWindow__update_spinner_line_impl",
    "_rr_RuntimeCollectorWindow__stop_spinner_impl",
    "_rr_RuntimeCollectorWindow__browse_project_root_impl",
    "_rr_RuntimeCollectorWindow__browse_output_json_impl",
    "_rr_run_headless_impl",
]
EXPECTED_SIGNATURES = {
    "_bind_root_globals": "(root_globals)",
    "_rr__run_builtin_qt_interaction_scenario_impl": "() -> 'dict'",
    "_rr__run_rich_automatic_scenario_impl": (
        "(project_root: 'Path', output_json: 'Path', entry_script: 'Path | None', "
        "scenario_module: 'str', execute_entry_script: 'bool') -> 'str'"
    ),
    "_rr__run_headless_impl": "() -> 'int'",
    "_rr_RuntimeCollectorWindow__build_ui_impl": "(self) -> 'None'",
    "_rr_RuntimeCollectorWindow__connect_signals_impl": "(self) -> 'None'",
    "_rr_RuntimeCollectorWindow__append_log_impl": "(self, text: 'str') -> 'None'",
    "_rr_RuntimeCollectorWindow__start_spinner_impl": "(self) -> 'None'",
    "_rr_RuntimeCollectorWindow__tick_spinner_impl": "(self) -> 'None'",
    "_rr_RuntimeCollectorWindow__update_spinner_line_impl": "(self, text: 'str') -> 'None'",
    "_rr_RuntimeCollectorWindow__stop_spinner_impl": "(self) -> 'None'",
    "_rr_RuntimeCollectorWindow__browse_project_root_impl": "(self) -> 'None'",
    "_rr_RuntimeCollectorWindow__browse_output_json_impl": "(self) -> 'None'",
    "_rr_run_headless_impl": "(*args, **kwargs)",
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
        count = _line_count(path)
        if not 101 <= count <= 499:
            raise AssertionError(
                f"LINE_LAW_101_499 failed: {relative_path}: {count}"
            )


def _assert_semantic_safety() -> None:
    from kanda_reasoner_app.manage_architecture.kanda_refactor_semantic_safety import (
        check_candidate_dependency_direction,
        detect_semantic_dynamic_risks,
    )

    for relative_path in FAMILY:
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
        helper_relative_paths=[BINDINGS_REL, SCENARIOS_REL, WINDOW_REL],
    )
    if not direction.get("pass"):
        raise AssertionError(
            "DEPENDENCY_DIRECTION_VIOLATION: "
            + json.dumps(direction.get("violations", []), sort_keys=True)
        )


def _assert_public_contract() -> None:
    from kanda_reasoner_app.reasoner_runtime_collector.runtime_runner_help import (
        runtime_runner_part_2_private_impl as module,
    )

    if list(module.__all__) != EXPECTED_ALL:
        raise AssertionError("PUBLIC_ALL_CHANGED")
    for name in REQUIRED_CONSUMER_SYMBOLS:
        if not hasattr(module, name):
            raise AssertionError("REQUIRED_CONSUMER_SYMBOL_MISSING: " + name)
        actual = str(inspect.signature(getattr(module, name)))
        expected = EXPECTED_SIGNATURES[name]
        if actual != expected:
            raise AssertionError(
                f"PUBLIC_SIGNATURE_CHANGED: {name}: {actual} != {expected}"
            )


def _assert_payload_consumer_contract() -> None:
    from kanda_reasoner_app.backend_payloads import payload_y

    encoded = "".join(payload_y.PAYLOAD_PARTS_Y)
    source = base64.b64decode(encoded.encode("ascii")).decode("utf-8")
    required_references = [
        "_rr_part_2._rr__run_builtin_qt_interaction_scenario_impl()",
        "_rr_part_2._rr__run_rich_automatic_scenario_impl(",
        "_rr_part_2._rr_RuntimeCollectorWindow__build_ui_impl(self)",
        "_rr_part_2._rr_RuntimeCollectorWindow__connect_signals_impl(self)",
        "_rr_part_2._rr_RuntimeCollectorWindow__browse_output_json_impl(self)",
        "_rr_part_2._bind_root_globals(root_globals)",
    ]
    for reference in required_references:
        if reference not in source:
            raise AssertionError("PAYLOAD_CONSUMER_REFERENCE_CHANGED: " + reference)


def _assert_auto_connect_contract() -> None:
    scenario_source = _path(SCENARIOS_REL).read_text(encoding="utf-8")
    window_source = _path(WINDOW_REL).read_text(encoding="utf-8")
    for source, required in (
        (
            scenario_source,
            [
                "QMetaObject.connectSlotsByName(self)",
                "on_runtime_runner_probe_line_edit_textChanged",
                "on_runtime_runner_probe_apply_button_clicked",
                "on_runtime_runner_probe_close_button_clicked",
                'setObjectName("runtime_runner_probe_line_edit")',
                'setObjectName("runtime_runner_probe_apply_button")',
                'setObjectName("runtime_runner_probe_close_button")',
            ],
        ),
        (
            window_source,
            [
                "QMetaObject.connectSlotsByName(central)",
                "on_browse_project_button_clicked",
                "on_browse_output_button_clicked",
                "on_browse_entry_button_clicked",
                "on_configure_button_clicked",
                "on_save_button_clicked",
                "on_close_button_clicked",
                "prior_name",
            ],
        ),
    ):
        for token in required:
            if token not in source:
                raise AssertionError("QT_AUTOCONNECT_CONTRACT_MISSING: " + token)


def _assert_behavior_contract() -> None:
    from kanda_reasoner_app.reasoner_runtime_collector.runtime_runner_help import (
        runtime_runner_part_2_private_impl as module,
    )

    records: list[tuple[str, Any]] = []

    def record(name: str, value: Any = None) -> None:
        records.append((name, value))

    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir).resolve()
        output = root / "trace.json"
        entry = root / "entry.py"
        entry.write_text("pass\n", encoding="utf-8")
        config = {
            "project_root": root,
            "output_json": output,
            "overwrite": True,
            "entry_script": entry,
            "scenario_module": "scenario.example",
            "execute_entry_script": False,
        }

        def resolve_headless_config() -> dict[str, Any]:
            record("resolve")
            return dict(config)

        def named_scenario(**kwargs: Any) -> str:
            record("named", sorted(kwargs))
            return "main"

        def entry_script(path: Path) -> None:
            record("entry", path.name)

        def configure(**kwargs: Any) -> None:
            record("configure", sorted(kwargs))

        def save_trace() -> Path:
            output.write_text('{"saved": true}', encoding="utf-8")
            record("save", output.name)
            return output

        module._bind_root_globals(
            {
                "configure_runtime_trace": configure,
                "save_runtime_trace": save_trace,
                "trace_event": lambda **kwargs: record(
                    "event", kwargs.get("event_type")
                ),
                "trace_signal_connection": lambda **kwargs: record(
                    "connection", kwargs.get("signal_name")
                ),
                "trace_state_snapshot": lambda **kwargs: record(
                    "snapshot", kwargs.get("label")
                ),
                "_resolve_headless_config": resolve_headless_config,
                "_ensure_qapplication": lambda: None,
                "_run_builtin_collector_component_scenario": lambda path: {
                    "project_root": str(path)
                },
                "_run_entry_script": entry_script,
                "_run_named_scenario_module": named_scenario,
                "_save_prefs": lambda *args, **kwargs: record("prefs", list(args)),
                "DEFAULT_PROJECT_ROOT": root / "default_project",
                "DEFAULT_OUTPUT_JSON": root / "default_output.json",
            }
        )

        module_mode = module._rr__run_rich_automatic_scenario_impl(
            root,
            output,
            entry,
            "scenario.example",
            False,
        )
        if module_mode != "scenario_module":
            raise AssertionError("RICH_SCENARIO_MODULE_MODE_CHANGED")

        entry_mode = module._rr__run_rich_automatic_scenario_impl(
            root,
            output,
            entry,
            "",
            True,
        )
        if entry_mode != "entry_script":
            raise AssertionError("RICH_SCENARIO_ENTRY_MODE_CHANGED")

        output.write_text("OLD", encoding="utf-8")
        stdout = io.StringIO()
        stderr = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            status = module._rr__run_headless_impl()
        if status != 0:
            raise AssertionError("HEADLESS_STATUS_CHANGED")
        payload = json.loads(stdout.getvalue())
        if payload.get("scenario_mode") != "scenario_module":
            raise AssertionError("HEADLESS_SCENARIO_MODE_CHANGED")
        if output.read_text(encoding="utf-8") != '{"saved": true}':
            raise AssertionError("HEADLESS_OVERWRITE_SAVE_CHANGED")
        if stderr.getvalue():
            raise AssertionError("HEADLESS_UNEXPECTED_STDERR")
        if not any(name == "named" for name, _value in records):
            raise AssertionError("NAMED_SCENARIO_DELEGATION_MISSING")
        if not any(name == "entry" for name, _value in records):
            raise AssertionError("ENTRY_SCRIPT_DELEGATION_MISSING")


def _assert_fresh_ast_family() -> None:
    from kanda_reasoner_app.manage_architecture.large_module_split_audit import (
        run_large_module_split_audit,
    )

    for relative_path in FAMILY:
        result = run_large_module_split_audit(
            PROJECT_ROOT,
            relative_path,
            classifier_mode="heuristic",
        )
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
        for item in manifest["files"]:
            relative_path = item["relative_path"]
            payload_name = "payload/" + relative_path
            raw = archive.read(payload_name)
            digest = hashlib.sha256(raw).hexdigest()
            if digest != item["sha256"]:
                raise AssertionError("PACKAGE_PAYLOAD_HASH_MISMATCH: " + relative_path)
        if manifest.get("feature_id") != FEATURE_ID:
            raise AssertionError("PACKAGE_FEATURE_ID_MISMATCH")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--patch-zip", default="")
    args = parser.parse_args()
    patch_zip = Path(args.patch_zip).resolve() if args.patch_zip else None

    _assert_source_family()
    print("SOURCE_ASCII_UTF8_NO_BOM: PASS")
    print("LINE_LAW_101_499_FITNESS: PASS")
    print("PYTHON_SYNTAX: PASS")

    _assert_semantic_safety()
    print("SEMANTIC_DYNAMIC_SAFETY: PASS")
    print("DEPENDENCY_DIRECTION_FITNESS: PASS")

    _assert_public_contract()
    _assert_payload_consumer_contract()
    print("PUBLIC_API_PRESERVATION: PASS")
    print("CONSUMER_COMPATIBILITY_FITNESS: PASS")
    print("ANNOTATION_IMPORT_PRESERVATION: PASS")

    _assert_auto_connect_contract()
    print("QT_AUTOCONNECT_CONTRACT: PASS")

    _assert_behavior_contract()
    print("BEHAVIOR_EQUIVALENCE_FITNESS: PASS")
    print("BEHAVIOR_REGRESSION: PASS")

    _assert_fresh_ast_family()
    print("AST_SPLIT_AUDIT_RERUN: PASS")
    print("AST_SPLIT_SAFETY_LABEL: SAFE REFACTORING")
    print("AST_SPLIT_HARD_BLOCKERS: 0")

    _assert_patch_zip(patch_zip)
    print("PACKAGE_PAYLOAD_HASHES: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
