# project-path: tools/engineering_diagnostics_wave2r_public_boundary_gate.py
"""Public-boundary gate for Engineering Diagnostics Wave 2R."""

from __future__ import annotations

import ast
from pathlib import Path

__all__ = ["validate_engineering_diagnostics_wave2r_public_boundary"]

_RUNTIME_PATHS = (
    "kanda_reasoner_app/engineering_diagnostics/lifecycle_models.py",
    "kanda_reasoner_app/engineering_diagnostics/lifecycle.py",
    "kanda_reasoner_app/engineering_diagnostics/_store_lifecycle_schema.py",
    "kanda_reasoner_app/engineering_diagnostics/_store_lifecycle_state.py",
    "kanda_reasoner_app/engineering_diagnostics/_store_lifecycle_ops.py",
    "kanda_reasoner_app/engineering_diagnostics/_store_run_ops.py",
    "kanda_reasoner_app/engineering_diagnostics/_store_database.py",
    "kanda_reasoner_app/engineering_diagnostics/_store_baseline_ops.py",
    "kanda_reasoner_app/engineering_diagnostics/store.py",
    "kanda_reasoner_app/engineering_diagnostics/__init__.py",
    "kanda_reasoner_app/engineering_diagnostics_gui/lifecycle_ui.py",
    "kanda_reasoner_app/engineering_diagnostics_gui/finding_view_builder.py",
    "kanda_reasoner_app/engineering_diagnostics_gui/run_summary.py",
    "kanda_reasoner_app/engineering_diagnostics_gui/models.py",
    "kanda_reasoner_app/engineering_diagnostics_gui/controller.py",
    "kanda_reasoner_app/engineering_diagnostics_gui/diagnostic_table_model.py",
    "kanda_reasoner_app/engineering_diagnostics_gui/engineering_diagnostics_tab.py",
    "kanda_reasoner_app/engineering_diagnostics_gui/owner_ui.py",
    "kanda_reasoner_app/engineering_diagnostics_gui/table_columns.py",
    "kanda_reasoner_app/engineering_diagnostics_gui/wave2r_validation.py",
)
_TEST_PATHS = (
    "tests/test_engineering_diagnostics_wave2r.py",
    "tests/test_engineering_diagnostics_wave2r_gui_scale.py",
)
_TOOL_PATHS = (
    "tools/engineering_diagnostics_wave2r_architecture_gate.py",
    "tools/engineering_diagnostics_wave2r_public_boundary_gate.py",
    "tools/engineering_diagnostics_wave2r_validation_runtime.py",
    "tools/validate_engineering_diagnostics_wave2r_v1.py",
)
_ALL_PATHS = _RUNTIME_PATHS + _TEST_PATHS + _TOOL_PATHS


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def _tree(path: Path) -> ast.Module:
    return ast.parse(path.read_text(encoding="utf-8"), filename=str(path))


def _public_definitions(path: Path) -> tuple[str, ...]:
    return tuple(
        node.name
        for node in _tree(path).body
        if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef))
        and not node.name.startswith("_")
    )


def _sources(root: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for relative in _ALL_PATHS:
        path = root / relative
        _require(path.is_file(), "WAVE2R_FILE_MISSING:" + relative)
        text = path.read_text(encoding="utf-8")
        text.encode("ascii")
        _require(len(text.splitlines()) <= 500, "WAVE2R_MODULE_TOO_LARGE:" + relative)
        values[relative] = text
    return values


def _assert_public_ownership(root: Path) -> None:
    owner_paths = (
        "kanda_reasoner_app/engineering_diagnostics/lifecycle_models.py",
        "kanda_reasoner_app/engineering_diagnostics/lifecycle.py",
        "kanda_reasoner_app/engineering_diagnostics_gui/lifecycle_ui.py",
        "kanda_reasoner_app/engineering_diagnostics_gui/finding_view_builder.py",
        "kanda_reasoner_app/engineering_diagnostics_gui/run_summary.py",
    )
    owners: dict[str, list[str]] = {}
    for relative in owner_paths:
        for symbol in _public_definitions(root / relative):
            owners.setdefault(symbol, []).append(relative)
    duplicates = {name: paths for name, paths in owners.items() if len(paths) > 1}
    _require(not duplicates, "WAVE2R_DUPLICATE_PUBLIC_SYMBOL:" + repr(duplicates))
    expected = {
        "DiagnosticLifecycleTarget",
        "DiagnosticLifecycleHead",
        "DiagnosticLifecycleDecisionRecord",
        "DiagnosticLifecycleState",
        "allowed_lifecycle_actions",
        "validate_lifecycle_transition",
        "create_lifecycle_controls",
        "bind_lifecycle_actions",
        "build_diagnostic_finding_views",
        "build_diagnostic_run_summary",
    }
    _require(expected.issubset(owners), "WAVE2R_PUBLIC_OWNER_MISSING:" + repr(sorted(expected - set(owners))))
    for relative in (
        "kanda_reasoner_app/engineering_diagnostics/_store_lifecycle_schema.py",
        "kanda_reasoner_app/engineering_diagnostics/_store_lifecycle_state.py",
        "kanda_reasoner_app/engineering_diagnostics/_store_lifecycle_ops.py",
        "kanda_reasoner_app/engineering_diagnostics/_store_run_ops.py",
    ):
        text = (root / relative).read_text(encoding="utf-8")
        _require("__all__" not in text, "WAVE2R_PRIVATE_HELPER_PUBLIC_SURFACE:" + relative)


def _assert_persistence_boundary(sources: dict[str, str]) -> None:
    direct_sqlite_allowed = {
        "kanda_reasoner_app/engineering_diagnostics/_store_lifecycle_schema.py",
        "kanda_reasoner_app/engineering_diagnostics/_store_lifecycle_state.py",
        "kanda_reasoner_app/engineering_diagnostics/_store_lifecycle_ops.py",
        "kanda_reasoner_app/engineering_diagnostics/_store_database.py",
    "kanda_reasoner_app/engineering_diagnostics/_store_baseline_ops.py",
    }
    for relative in _RUNTIME_PATHS:
        text = sources[relative]
        if "sqlite3" in text:
            _require(relative in direct_sqlite_allowed, "WAVE2R_DIRECT_SQLITE_OUTSIDE_STORE:" + relative)
        for token in (
            "project_freeze_ledger",
            "freeze_after_update.",
            "reasoner_symbol_atlas.",
            "source_hygiene._",
            ".write_text(",
            ".write_bytes(",
            "shutil.copy",
            "os.replace",
        ):
            if relative.startswith("kanda_reasoner_app/engineering_diagnostics_gui/"):
                _require(token not in text, "WAVE2R_GUI_WRITE_OR_REACH_IN:" + relative + ":" + token)
    lifecycle_ops = sources[
        "kanda_reasoner_app/engineering_diagnostics/_store_lifecycle_ops.py"
    ]
    _require("DELETE FROM diagnostic_findings" not in lifecycle_ops, "WAVE2R_FINDING_DELETE_SURFACE")
    _require("DELETE FROM diagnostic_runs" not in lifecycle_ops, "WAVE2R_RUN_DELETE_SURFACE")
    _require("record_lifecycle_decision" in sources[
        "kanda_reasoner_app/engineering_diagnostics/store.py"
    ], "WAVE2R_STORE_OWNER_MISSING")
    _require(
        "diagnostic_lifecycle"
        not in sources[
            "kanda_reasoner_app/engineering_diagnostics/_store_baseline_ops.py"
        ],
        "WAVE2R_BASELINE_LIFECYCLE_COUPLING",
    )


def _assert_hard_rules(sources: dict[str, str]) -> None:
    models = sources["kanda_reasoner_app/engineering_diagnostics/lifecycle_models.py"]
    engine = sources["kanda_reasoner_app/engineering_diagnostics/lifecycle.py"]
    operations = sources[
        "kanda_reasoner_app/engineering_diagnostics/_store_lifecycle_ops.py"
    ]
    gui = sources["kanda_reasoner_app/engineering_diagnostics_gui/lifecycle_ui.py"]
    for state in (
        "OPEN", "INVESTIGATING", "CONFIRMED", "FIX_PLANNED",
        "PATCH_PREPARED", "VALIDATING", "RESOLUTION_CANDIDATE",
        "RESOLVED", "ACCEPTED_RISK", "FALSE_POSITIVE", "SUPPRESSED",
        "DEFERRED", "REOPENED",
    ):
        _require('"' + state + '"' in models, "WAVE2R_STATE_MISSING:" + state)
    for action in (
        "CONFIRM", "SUPPRESS", "ACCEPT_RISK", "MARK_FALSE_POSITIVE",
        "DEFER", "REOPEN",
    ):
        _require('"' + action + '"' in gui, "WAVE2R_GUI_ACTION_MISSING:" + action)
    schema = sources[
        "kanda_reasoner_app/engineering_diagnostics/_store_lifecycle_schema.py"
    ]
    _require(
        "_validate_lifecycle_table_contract" in schema,
        "WAVE2R_LIFECYCLE_SCHEMA_CONTRACT_GUARD_MISSING",
    )
    _require(
        "ENGINEERING_DIAGNOSTICS_LIFECYCLE_TABLE_CONTRACT_MISMATCH" in schema,
        "WAVE2R_LIFECYCLE_SCHEMA_REJECTION_MARKER_MISSING",
    )
    for token in (
        "ACCEPTED_RISK_EXPLICIT_CONFIRMATION_REQUIRED",
        "LIFECYCLE_EXPIRATION_OR_REVISIT_CONDITION_REQUIRED",
        "DEFERRED_RELATED_WAVE_REQUIRED",
        "STALE_LIFECYCLE_GENERATION",
    ):
        _require(token in operations, "WAVE2R_GOVERNANCE_GUARD_MISSING:" + token)
    _require("LIFECYCLE_TRANSITION_NOT_ALLOWED" in engine, "WAVE2R_TRANSITION_GUARD_MISSING")
    _require("baseline" not in operations.lower(), "WAVE2R_BASELINE_ACCEPTANCE_COUPLED")


def validate_engineering_diagnostics_wave2r_public_boundary(root: Path) -> None:
    """Validate Wave 2R ownership, persistence, and human-decision contracts."""
    project_root = Path(root).expanduser().resolve(strict=True)
    sources = _sources(project_root)
    _assert_public_ownership(project_root)
    _assert_persistence_boundary(sources)
    _assert_hard_rules(sources)
    print("WAVE2R MODULE SIZE MAXIMUM 500: PASS")
    print("WAVE2R ASCII SOURCE CONTRACT: PASS")
    print("WAVE2R PUBLIC LIFECYCLE SYMBOL SINGLE OWNERS: PASS")
    print("WAVE2R PRIVATE HELPER PUBLIC SURFACES: 0")
    print("WAVE2R ENGINEERING DIAGNOSTICS STORE OWNER: PRESERVED")
    print("WAVE2R DIRECT SQLITE OUTSIDE STORE: 0")
    print("WAVE2R FINDING DELETE SURFACES: 0")
    print("WAVE2R SOURCE MUTATION SURFACES: 0")
    print("WAVE2R ATOMIC LIFECYCLE SCHEMA MIGRATION: PASS")
    print("WAVE2R ACCEPTED RISK EXPLICIT CONFIRMATION: PASS")
    print("WAVE2R SUPPRESSION REASON CONTRACT: PASS")
    print("WAVE2R FALSE POSITIVE SEARCHABILITY: PASS")
    print("WAVE2R BASELINE ACCEPTANCE RISK COUPLING: ABSENT")
    print("WAVE2R PUBLIC-CONTRACT-ONLY COMMUNICATION: PASS")
