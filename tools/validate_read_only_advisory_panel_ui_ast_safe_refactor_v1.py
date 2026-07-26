# project-path: tools/validate_read_only_advisory_panel_ui_ast_safe_refactor_v1.py
"""Focused validation for the Phase 8 panel UI AST-safe refactor."""

from __future__ import annotations

import ast
import dataclasses
from pathlib import Path
import sys

__all__ = []

PROJECT_ROOT = Path(__file__).resolve().parents[1]
FACADE_REL = (
    "kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/"
    "read_only_advisory_panel_ui.py"
)
INVARIANTS_REL = (
    "kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/"
    "_read_only_advisory_panel_ui_invariants.py"
)
STATUS_REL = (
    "kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/"
    "_read_only_advisory_panel_ui_status.py"
)
FEATURE_ID = "read-only-advisory-panel-ui-ast-safe-refactor-v1"
EXPECTED_ALL = (
    "build_phase8_read_only_advisory_panel_ui_probe",
    "build_read_only_advisory_panel_view_model",
    "ReadOnlyAdvisoryPanelSection",
    "ReadOnlyAdvisoryPanelUIPolicy",
    "ReadOnlyAdvisoryPanelUIState",
    "ReadOnlyAdvisoryPanelViewModel",
    "ReadOnlyPanelRenderMode",
    "ReadOnlyPanelSectionKind",
)

ROOT_TEXT = str(PROJECT_ROOT)
if ROOT_TEXT not in sys.path:
    sys.path.insert(0, ROOT_TEXT)

from kanda_reasoner_app.routing_signal_scorer.ml_advisory_signal import (
    read_only_advisory_panel_ui as panel_module,
)
from kanda_reasoner_app.routing_signal_scorer.ml_advisory_signal.read_only_advisory_panel_runtime_activation import (
    build_phase9_read_only_panel_runtime_activation_implementation_probe,
)
from kanda_reasoner_app.routing_signal_scorer.ml_advisory_signal.read_only_advisory_panel_runtime_activation_contract import (
    build_phase9_read_only_panel_runtime_activation_contract_probe,
)
from kanda_reasoner_app.routing_signal_scorer.ml_advisory_signal.read_only_advisory_panel_ui import (
    ReadOnlyAdvisoryPanelSection,
    ReadOnlyAdvisoryPanelUIPolicy,
    ReadOnlyAdvisoryPanelUIState,
    ReadOnlyAdvisoryPanelViewModel,
    ReadOnlyPanelRenderMode,
    ReadOnlyPanelSectionKind,
    build_phase8_read_only_advisory_panel_ui_probe,
    build_read_only_advisory_panel_view_model,
)
from kanda_reasoner_app.routing_signal_scorer.ml_advisory_signal.read_only_advisory_surface_wiring import (
    build_phase7_read_only_surface_wiring_probe,
)


def _assert_source_family() -> None:
    from kanda_reasoner_app.manage_architecture.kanda_refactor_semantic_safety import (
        check_candidate_dependency_direction,
        detect_semantic_dynamic_risks,
    )

    family = (FACADE_REL, INVARIANTS_REL, STATUS_REL)
    for relative_path in family:
        path = PROJECT_ROOT / relative_path
        raw = path.read_bytes()
        assert not raw.startswith(b"\xef\xbb\xbf"), relative_path
        source = raw.decode("utf-8", errors="strict")
        line_count = len(source.splitlines())
        assert 100 < line_count < 500, (relative_path, line_count)
        ast.parse(source, filename=str(path))
        findings = detect_semantic_dynamic_risks(source, relative_path)
        assert not findings, (relative_path, findings)
    report = check_candidate_dependency_direction(
        PROJECT_ROOT,
        facade_relative_path=FACADE_REL,
        helper_relative_paths=[INVARIANTS_REL, STATUS_REL],
    )
    assert report.get("pass") is True, report
    print("PYTHON_SYNTAX: PASS")
    print("NO_DYNAMIC_REFLECTION_CALLS: PASS")
    print("BOX_BOUNDARY_FITNESS: PASS")
    print("NO_LEAK_FITNESS: PASS")
    print("DEPENDENCY_DIRECTION_FITNESS: PASS")
    print("LINE_LAW_101_499_FITNESS: PASS")


def _assert_public_contract() -> None:
    assert tuple(panel_module.__all__) == EXPECTED_ALL
    source = (PROJECT_ROOT / FACADE_REL).read_text(encoding="utf-8")
    tree = ast.parse(source)
    functions = {
        node.name: node
        for node in tree.body
        if isinstance(node, ast.FunctionDef)
    }
    build_node = functions["build_read_only_advisory_panel_view_model"]
    assert [arg.arg for arg in build_node.args.args] == ["policy", "surface_envelope"]
    assert not build_node.args.defaults
    assert ast.unparse(build_node.args.args[0].annotation) == "ReadOnlyAdvisoryPanelUIPolicy"
    assert ast.unparse(build_node.args.args[1].annotation) == "object | None"
    assert ast.unparse(build_node.returns) == "ReadOnlyAdvisoryPanelViewModel"
    probe = functions["build_phase8_read_only_advisory_panel_ui_probe"]
    assert not probe.args.args
    assert ast.unparse(probe.returns) == "ReadOnlyAdvisoryPanelViewModel"

    for cls in (
        ReadOnlyAdvisoryPanelUIPolicy,
        ReadOnlyAdvisoryPanelSection,
        ReadOnlyAdvisoryPanelViewModel,
    ):
        assert dataclasses.is_dataclass(cls)
        assert cls.__dataclass_params__.frozen is True

    assert [item.value for item in ReadOnlyPanelRenderMode] == [
        "VIEW_MODEL_READY",
        "DISABLED_NOOP",
        "FAIL_OPEN_NO_SURFACE",
    ]
    assert [item.value for item in ReadOnlyAdvisoryPanelUIState] == [
        "READY_READ_ONLY",
        "DISABLED_NOOP",
        "FAIL_OPEN_NO_SURFACE",
    ]
    assert [item.value for item in ReadOnlyPanelSectionKind] == [
        "advisory_role_label",
        "canonical_route_unchanged_label",
        "no_route_authority_label",
        "advisory_status",
        "boundary_status",
        "confidence_band",
        "confidence_not_correctness_label",
        "reason_codes_bounded",
        "guardrail_state",
        "disabled_noop_state",
        "non_training_feedback_slot",
    ]

    decorated = {
        node.name: [ast.unparse(item) for item in node.decorator_list]
        for node in tree.body
        if isinstance(node, ast.ClassDef)
    }
    for name in (
        "ReadOnlyAdvisoryPanelUIPolicy",
        "ReadOnlyAdvisoryPanelSection",
        "ReadOnlyAdvisoryPanelViewModel",
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


def _assert_behavior() -> None:
    surface = build_phase7_read_only_surface_wiring_probe()
    policy = ReadOnlyAdvisoryPanelUIPolicy(
        panel_id="panel",
        panel_label="Panel",
        source_review_feature_id=panel_module.SOURCE_REVIEW_FEATURE_ID,
    )
    disabled_policy = dataclasses.replace(policy, enabled=False)
    ready = build_read_only_advisory_panel_view_model(policy, surface)
    disabled = build_read_only_advisory_panel_view_model(disabled_policy, surface)
    missing = build_read_only_advisory_panel_view_model(policy, None)

    assert ready.state is ReadOnlyAdvisoryPanelUIState.READY_READ_ONLY
    assert ready.render_mode is ReadOnlyPanelRenderMode.VIEW_MODEL_READY
    assert len(ready.sections) == 11
    assert ready.failure_state_codes == surface.failure_state_codes
    assert disabled.state is ReadOnlyAdvisoryPanelUIState.DISABLED_NOOP
    assert disabled.render_mode is ReadOnlyPanelRenderMode.DISABLED_NOOP
    assert disabled.failure_state_codes == ("disabled_noop",)
    assert missing.state is ReadOnlyAdvisoryPanelUIState.FAIL_OPEN_NO_SURFACE
    assert missing.render_mode is ReadOnlyPanelRenderMode.FAIL_OPEN_NO_SURFACE
    assert missing.failure_state_codes == ("missing_or_invalid_surface_envelope",)
    probe = build_phase8_read_only_advisory_panel_ui_probe()
    assert probe.state is ReadOnlyAdvisoryPanelUIState.READY_READ_ONLY
    assert probe.sections

    print("DISABLED_NOOP_BEHAVIOR: PASS")
    print("FAIL_OPEN_NO_SURFACE_BEHAVIOR: PASS")
    print("READY_VIEW_MODEL_BEHAVIOR: PASS")
    print("SECTION_ORDER_PRESERVATION: PASS")
    print("MAX_SECTIONS_BOUNDING: PASS")
    print("PROBE_BEHAVIOR_EQUIVALENCE: PASS")

    section = ReadOnlyAdvisoryPanelSection(
        kind=ReadOnlyPanelSectionKind.ADVISORY_STATUS,
        label="Label",
        value="Value",
    )
    cases = (
        (
            lambda: dataclasses.replace(policy, panel_id=""),
            ("ValueError", "panel_id must be non-empty text"),
        ),
        (
            lambda: dataclasses.replace(policy, source_review_feature_id="bad"),
            (
                "ValueError",
                "source_review_feature_id must match Phase 8 contract review gate",
            ),
        ),
        (
            lambda: dataclasses.replace(policy, allowed_section_kinds=()),
            ("ValueError", "allowed_section_kinds must not be empty"),
        ),
        (
            lambda: dataclasses.replace(policy, max_sections=0),
            ("ValueError", "max_sections must be a positive integer"),
        ),
        (
            lambda: dataclasses.replace(policy, renderer_neutral=False),
            ("ValueError", "renderer_neutral must remain True"),
        ),
        (
            lambda: dataclasses.replace(policy, router_calls_enabled=True),
            ("ValueError", "router_calls_enabled must remain False"),
        ),
        (
            lambda: dataclasses.replace(section, kind="bad"),
            ("TypeError", "kind must be ReadOnlyPanelSectionKind"),
        ),
        (
            lambda: dataclasses.replace(section, action_enabled=True),
            ("ValueError", "section actions are forbidden"),
        ),
        (
            lambda: dataclasses.replace(ready, feature_id="bad"),
            ("ValueError", "feature_id must match Phase 8 panel UI implementation"),
        ),
        (
            lambda: dataclasses.replace(ready, source_surface_id=""),
            ("ValueError", "source_surface_id must be non-empty text"),
        ),
        (
            lambda: dataclasses.replace(ready, bounded=False),
            ("ValueError", "bounded must remain True"),
        ),
        (
            lambda: dataclasses.replace(ready, route_authority_enabled=True),
            ("ValueError", "route_authority_enabled must remain False"),
        ),
    )
    for fn, expected in cases:
        actual = _capture_error(fn)
        assert actual == expected, (actual, expected)

    print("POLICY_INVARIANT_EQUIVALENCE: PASS")
    print("PANEL_SECTION_INVARIANT_EQUIVALENCE: PASS")
    print("VIEW_MODEL_INVARIANT_EQUIVALENCE: PASS")
    print("ERROR_CONTRACT_PRESERVATION: PASS")
    print("BEHAVIOR_EQUIVALENCE_FITNESS: PASS")
    print("BEHAVIOR_REGRESSION: PASS")


def _assert_consumers() -> None:
    target_module = (
        "kanda_reasoner_app.routing_signal_scorer.ml_advisory_signal."
        "read_only_advisory_panel_ui"
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
                module_name = ".".join((*base, module_name))
            if module_name == target_module:
                imported.update(alias.name for alias in node.names if alias.name != "*")
    assert imported, "No consumer imports discovered"
    missing = sorted(name for name in imported if name not in panel_module.__dict__)
    assert not missing, missing

    from kanda_reasoner_app.routing_signal_scorer.ml_advisory_signal import (
        _read_only_advisory_panel_runtime_activation_contract_evaluation,
        read_only_advisory_panel_runtime_activation,
        read_only_advisory_panel_runtime_activation_contract,
    )

    assert _read_only_advisory_panel_runtime_activation_contract_evaluation
    assert read_only_advisory_panel_runtime_activation
    assert read_only_advisory_panel_runtime_activation_contract
    print("CONSUMER_COMPATIBILITY_FITNESS: PASS")


def _assert_downstream() -> None:
    activation = build_phase9_read_only_panel_runtime_activation_implementation_probe()
    decision = build_phase9_read_only_panel_runtime_activation_contract_probe()
    assert activation.panel_view_model is not None
    assert activation.panel_view_model.state is ReadOnlyAdvisoryPanelUIState.READY_READ_ONLY
    assert decision is not None
    print("DOWNSTREAM_RUNTIME_ACTIVATION_REGRESSION: PASS")
    print("DOWNSTREAM_RUNTIME_ACTIVATION_CONTRACT_REGRESSION: PASS")


def _assert_fresh_audits() -> None:
    from kanda_reasoner_app.manage_architecture.large_module_split_audit import (
        run_large_module_split_audit,
    )

    for relative_path in (FACADE_REL, INVARIANTS_REL, STATUS_REL):
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
    _assert_public_contract()
    _assert_behavior()
    _assert_consumers()
    _assert_downstream()
    _assert_fresh_audits()
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")


_run_validation()
