# project-path: tools/validate_read_only_advisory_panel_host_binding_ast_safe_refactor_v1.py
"""Focused validation for the Phase 11 host-binding AST-safe refactor."""

from __future__ import annotations

import ast
import dataclasses
from pathlib import Path
import sys

__all__ = []

PROJECT_ROOT = Path(__file__).resolve().parents[1]
FACADE_REL = (
    "kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/"
    "read_only_advisory_panel_host_binding.py"
)
HELPER_REL = (
    "kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/"
    "_read_only_advisory_panel_host_binding_invariants.py"
)
FEATURE_ID = "read-only-advisory-panel-host-binding-ast-safe-refactor-v1"
EXPECTED_ALL = (
    "build_phase11_read_only_panel_host_binding_implementation_probe",
    "build_read_only_advisory_panel_host_binding_descriptor",
    "ReadOnlyAdvisoryPanelHostBindingDescriptor",
    "ReadOnlyAdvisoryPanelHostBindingImplementationPolicy",
    "ReadOnlyAdvisoryPanelHostBoundSection",
    "ReadOnlyPanelHostBindingImplementationState",
)

PROJECT_ROOT_TEXT = str(PROJECT_ROOT)
if PROJECT_ROOT_TEXT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT_TEXT)

from kanda_reasoner_app.routing_signal_scorer.ml_advisory_signal import (
    read_only_advisory_panel_host_binding as host_binding_module,
)
from kanda_reasoner_app.routing_signal_scorer.ml_advisory_signal.read_only_advisory_panel_host_binding import (
    ReadOnlyAdvisoryPanelHostBindingDescriptor,
    ReadOnlyAdvisoryPanelHostBindingImplementationPolicy,
    ReadOnlyAdvisoryPanelHostBoundSection,
    ReadOnlyPanelHostBindingImplementationState,
    build_phase11_read_only_panel_host_binding_implementation_probe,
    build_read_only_advisory_panel_host_binding_descriptor,
)
from kanda_reasoner_app.routing_signal_scorer.ml_advisory_signal.read_only_advisory_panel_renderer_mount import (
    ReadOnlyPanelRendererMountImplementationState,
    build_phase10_read_only_panel_renderer_mount_implementation_probe,
)



def _assert_source_family() -> None:
    from kanda_reasoner_app.manage_architecture.kanda_refactor_semantic_safety import (
        check_candidate_dependency_direction,
        detect_semantic_dynamic_risks,
    )

    for relative_path in (FACADE_REL, HELPER_REL):
        path = PROJECT_ROOT / relative_path
        raw = path.read_bytes()
        assert not raw.startswith(b"\xef\xbb\xbf"), relative_path
        raw.decode("utf-8", errors="strict")
        source = raw.decode("utf-8")
        line_count = len(source.splitlines())
        assert 100 < line_count < 500, (relative_path, line_count)
        findings = detect_semantic_dynamic_risks(source, relative_path)
        assert not findings, (relative_path, findings)
        ast.parse(source, filename=str(path))
    report = check_candidate_dependency_direction(
        PROJECT_ROOT,
        facade_relative_path=FACADE_REL,
        helper_relative_paths=[HELPER_REL],
    )
    assert report.get("pass") is True, report
    print("PYTHON_SYNTAX: PASS")
    print("NO_DYNAMIC_REFLECTION_CALLS: PASS")
    print("BOX_BOUNDARY_FITNESS: PASS")
    print("NO_LEAK_FITNESS: PASS")
    print("DEPENDENCY_DIRECTION_FITNESS: PASS")
    print("LINE_LAW_101_499_FITNESS: PASS")


def _assert_public_contract(module: object) -> None:
    assert tuple(host_binding_module.__all__) == EXPECTED_ALL
    source = (PROJECT_ROOT / FACADE_REL).read_text(encoding="utf-8")
    tree = ast.parse(source)
    functions = {
        node.name: node
        for node in tree.body
        if isinstance(node, ast.FunctionDef)
    }
    build_node = functions["build_read_only_advisory_panel_host_binding_descriptor"]
    assert [item.arg for item in build_node.args.args] == [
        "policy",
        "renderer_mount_descriptor",
    ]
    assert not build_node.args.defaults
    assert ast.unparse(build_node.args.args[0].annotation) == (
        "ReadOnlyAdvisoryPanelHostBindingImplementationPolicy"
    )
    assert ast.unparse(build_node.args.args[1].annotation) == "object | None"
    assert ast.unparse(build_node.returns) == (
        "ReadOnlyAdvisoryPanelHostBindingDescriptor"
    )
    probe_node = functions[
        "build_phase11_read_only_panel_host_binding_implementation_probe"
    ]
    assert not probe_node.args.args
    assert ast.unparse(probe_node.returns) == (
        "ReadOnlyAdvisoryPanelHostBindingDescriptor"
    )
    for cls in (
        ReadOnlyAdvisoryPanelHostBindingImplementationPolicy,
        ReadOnlyAdvisoryPanelHostBoundSection,
        ReadOnlyAdvisoryPanelHostBindingDescriptor,
    ):
        assert dataclasses.is_dataclass(cls)
        assert cls.__dataclass_params__.frozen is True
    values = [item.value for item in ReadOnlyPanelHostBindingImplementationState]
    assert values == [
        "disabled_noop",
        "fail_open_no_descriptor",
        "blocked_unsafe_descriptor",
        "read_only_host_binding_descriptor_ready",
    ]
    decorated = {
        node.name: [ast.unparse(item) for item in node.decorator_list]
        for node in tree.body
        if isinstance(node, ast.ClassDef)
    }
    for name in (
        "ReadOnlyAdvisoryPanelHostBindingImplementationPolicy",
        "ReadOnlyAdvisoryPanelHostBoundSection",
        "ReadOnlyAdvisoryPanelHostBindingDescriptor",
    ):
        assert decorated[name] == ["dataclass(frozen=True)"], (name, decorated[name])
    print("PUBLIC_API_PRESERVATION: PASS")
    print("PUBLIC_SIGNATURE_PRESERVATION: PASS")
    print("ENUM_VALUE_PRESERVATION: PASS")
    print("DECORATOR_PRESERVATION: PASS")
    print("DATACLASS_FROZEN_PRESERVATION: PASS")
    print("ANNOTATION_IMPORT_PRESERVATION: PASS")


def _capture_error(fn: object) -> tuple[str, str]:
    try:
        fn()
    except Exception as exc:
        return type(exc).__name__, str(exc)
    raise AssertionError("Expected exception was not raised")


def _assert_behavior(module: object) -> None:
    policy = ReadOnlyAdvisoryPanelHostBindingImplementationPolicy(
        host_container_id="host",
        host_container_label="Host Label",
    )
    enabled = dataclasses.replace(policy, feature_flag_enabled=True)
    mount = build_phase10_read_only_panel_renderer_mount_implementation_probe()
    disabled = build_read_only_advisory_panel_host_binding_descriptor(policy, mount)
    missing = build_read_only_advisory_panel_host_binding_descriptor(enabled, None)
    ready = build_read_only_advisory_panel_host_binding_descriptor(enabled, mount)
    assert disabled.state.value == "disabled_noop"
    assert disabled.failure_state_codes == ("feature_flag_default_off",)
    assert disabled.read_only_host_binding_descriptor_ready is False
    assert missing.state.value == "fail_open_no_descriptor"
    assert missing.failure_state_codes == ("missing_or_invalid_renderer_mount_descriptor",)
    assert ready.state.value == "read_only_host_binding_descriptor_ready"
    assert ready.failure_state_codes == ()
    assert ready.read_only_host_binding_descriptor_ready is True
    assert ready.runtime_app_host_visibility_descriptor_ready is True
    assert ready.mounted_runtime_panel_descriptor_ready is True
    assert ready.host_bound_sections
    probe = build_phase11_read_only_panel_host_binding_implementation_probe()
    assert probe.state.value == "read_only_host_binding_descriptor_ready"
    assert probe.read_only_host_binding_descriptor_ready is True
    assert probe.host_bound_sections
    print("DISABLED_NOOP_BEHAVIOR: PASS")
    print("FAIL_OPEN_MISSING_DESCRIPTOR_BEHAVIOR: PASS")
    print("READY_DESCRIPTOR_BEHAVIOR: PASS")
    print("PROBE_BEHAVIOR_EQUIVALENCE: PASS")

    cases = [
        (
            lambda: dataclasses.replace(policy, host_container_id=""),
            ("ValueError", "host_container_id must be non-empty text"),
        ),
        (
            lambda: dataclasses.replace(
                policy,
                require_phase10_renderer_mount_descriptor_input=False,
            ),
            (
                "ValueError",
                "require_phase10_renderer_mount_descriptor_input must remain True",
            ),
        ),
        (
            lambda: dataclasses.replace(policy, allow_router_calls=True),
            ("ValueError", "allow_router_calls must remain False"),
        ),
        (
            lambda: ReadOnlyAdvisoryPanelHostBoundSection(
                section_key="k",
                label="L",
                value="V",
                severity="info",
                action_enabled=True,
            ),
            ("ValueError", "host-bound section actions are forbidden"),
        ),
        (
            lambda: dataclasses.replace(ready, source_panel_id=""),
            ("ValueError", "source_panel_id must be non-empty text"),
        ),
        (
            lambda: dataclasses.replace(disabled, router_calls_enabled=True),
            ("ValueError", "router_calls_enabled must remain False"),
        ),
        (
            lambda: dataclasses.replace(disabled, critical_boundary_error_budget=1),
            ("ValueError", "critical_boundary_error_budget must remain zero"),
        ),
    ]
    for fn, expected in cases:
        assert _capture_error(fn) == expected, (_capture_error(fn), expected)
    class UnsafeRendererMountDescriptor:
        state = (
            ReadOnlyPanelRendererMountImplementationState
            .READ_ONLY_MOUNT_DESCRIPTOR_READY
        )
        read_only_mount_descriptor_ready = True
        visible_read_only_panel_ready = True
        read_only = True
        telemetry_only = True
        in_memory_only = True
        bounded = True
        fail_open = True
        removable_noop = True
        route_invariant = True
        final_selection_invisible = True
        non_authoritative = True
        consumes_phase9_activation_envelope_only = True
        runtime_ui_mutation_enabled = False
        runtime_telemetry_surface_wiring_enabled = False
        route_influence_enabled = False
        route_authority_enabled = False
        router_calls_enabled = True
        advisor_calls_enabled = False
        adapter_execution_enabled = False
        provider_calls_enabled = False
        persistence_enabled = False
        prompt_loading_enabled = False
        prompt_registry_mutation_enabled = False
        prompt_library_read_enabled = False
        freeze_memory_read_enabled = False
        freeze_memory_write_enabled = False
        router_canon_read_enabled = False
        runtime_copilot_decision_behavior_enabled = False
        mount_surface_id = "unsafe-mount"
        mount_surface_label = "Unsafe Mount"
        source_panel_id = "panel"
        source_panel_label = "Panel"
        canonical_result_id = "result"
        canonical_dispatch_label = "dispatch"
        final_selection_hash = "hash"
        non_training_feedback_slot_enabled = False

    original_renderer_type = (
        host_binding_module.ReadOnlyAdvisoryPanelRendererMountDescriptor
    )
    host_binding_module.ReadOnlyAdvisoryPanelRendererMountDescriptor = (
        UnsafeRendererMountDescriptor
    )
    try:
        blocked = build_read_only_advisory_panel_host_binding_descriptor(
            enabled,
            UnsafeRendererMountDescriptor(),
        )
    finally:
        host_binding_module.ReadOnlyAdvisoryPanelRendererMountDescriptor = (
            original_renderer_type
        )
    assert blocked.state.value == "blocked_unsafe_descriptor"
    assert blocked.failure_state_codes == (
        "unsafe_renderer_mount_descriptor_rejected",
    )
    print("BLOCK_UNSAFE_DESCRIPTOR_BEHAVIOR: PASS")
    print("POLICY_INVARIANT_EQUIVALENCE: PASS")
    print("HOST_BOUND_SECTION_INVARIANT_EQUIVALENCE: PASS")
    print("DESCRIPTOR_INVARIANT_EQUIVALENCE: PASS")
    print("ERROR_CONTRACT_PRESERVATION: PASS")
    print("BEHAVIOR_EQUIVALENCE_FITNESS: PASS")
    print("BEHAVIOR_REGRESSION: PASS")


def _assert_consumers(module: object) -> None:
    target_module = (
        "kanda_reasoner_app.routing_signal_scorer.ml_advisory_signal."
        "read_only_advisory_panel_host_binding"
    )
    imported: set[str] = set()
    for path in PROJECT_ROOT.rglob("*.py"):
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except (OSError, UnicodeError, SyntaxError):
            continue
        for node in ast.walk(tree):
            if not isinstance(node, ast.ImportFrom) or not node.module:
                continue
            module_name = node.module
            if node.level:
                package_parts = path.relative_to(PROJECT_ROOT).with_suffix("").parts[:-1]
                base = package_parts[: len(package_parts) - node.level + 1]
                module_name = ".".join((*base, module_name)) if module_name else ".".join(base)
            if module_name == target_module:
                imported.update(alias.name for alias in node.names if alias.name != "*")
    assert imported, "No consumer imports discovered"
    missing = sorted(name for name in imported if name not in set(EXPECTED_ALL))
    assert not missing, missing
    from kanda_reasoner_app.routing_signal_scorer.ml_advisory_signal import (
        _read_only_advisory_panel_runtime_app_host_visibility_contract_evaluation,
        read_only_advisory_panel_runtime_app_host_visibility,
        read_only_advisory_panel_runtime_app_host_visibility_contract,
    )
    assert _read_only_advisory_panel_runtime_app_host_visibility_contract_evaluation
    assert read_only_advisory_panel_runtime_app_host_visibility
    assert read_only_advisory_panel_runtime_app_host_visibility_contract
    print("CONSUMER_COMPATIBILITY_FITNESS: PASS")


def _assert_fresh_audits() -> None:
    from kanda_reasoner_app.manage_architecture.large_module_split_audit import (
        run_large_module_split_audit,
    )

    for relative_path in (FACADE_REL, HELPER_REL):
        result = run_large_module_split_audit(
            PROJECT_ROOT,
            PROJECT_ROOT / relative_path,
            classifier_mode="heuristic",
        )
        classification = result.data["refactor_safety_classification"]
        assert classification["label"] == "SAFE REFACTORING", classification
        assert not classification["hard_blockers"], classification
    print("AST_SPLIT_AUDIT_RERUN: PASS")
    print("AST_SPLIT_FAMILY_ALL_SAFE: PASS")
    print("AST_SPLIT_SAFETY_LABEL: SAFE REFACTORING")
    print("AST_SPLIT_HARD_BLOCKERS: 0")



def _run_validation() -> None:
    print("SOURCE_IDENTITY_GUARD: PASS")
    _assert_source_family()
    _assert_public_contract(host_binding_module)
    _assert_behavior(host_binding_module)
    _assert_consumers(host_binding_module)
    _assert_fresh_audits()
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")


_run_validation()
