# project-path: tools/engineering_diagnostics_wave2w_public_boundary_gate.py
"""Public-boundary gate for Engineering Safety hierarchy Wave 2W."""

from __future__ import annotations

import ast
from pathlib import Path

__all__ = ["validate_engineering_diagnostics_wave2w_public_boundary"]

_TOUCHED_PATHS = (
    "reasoner_tools_gui_engineering_safety_panel.py",
    "kanda_reasoner_app/manage_architecture/audit_project_sibling_tabs.py",
    "kanda_reasoner_app/engineering_diagnostics_gui/__init__.py",
    "kanda_reasoner_app/engineering_diagnostics_gui/engineering_diagnostics_workspace.py",
    "kanda_reasoner_app/engineering_diagnostics_gui/full_engineering_diagnostics_tab.py",
    "tests/test_engineering_diagnostics_wave2v.py",
    "tests/test_engineering_diagnostics_wave2v_gui_scale.py",
    "tests/test_engineering_diagnostics_wave2w.py",
    "tests/test_engineering_diagnostics_wave2w_gui_scale.py",
    "tools/engineering_diagnostics_wave2v_architecture_gate.py",
    "tools/engineering_diagnostics_wave2v_gui_validation.py",
    "tools/engineering_diagnostics_wave2v_public_boundary_gate.py",
    "tools/validate_engineering_diagnostics_wave2v_v1.py",
    "tools/engineering_diagnostics_wave2w_architecture_gate.py",
    "tools/engineering_diagnostics_wave2w_gui_validation.py",
    "tools/engineering_diagnostics_wave2w_public_boundary_gate.py",
    "tools/engineering_diagnostics_wave2w_validation_runtime.py",
    "tools/validate_engineering_diagnostics_wave2w_v1.py",
)


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def _imports(path: Path) -> frozenset[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    values: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            values.add(node.module)
        elif isinstance(node, ast.Import):
            values.update(alias.name for alias in node.names)
    return frozenset(values)


def validate_engineering_diagnostics_wave2w_public_boundary(root: Path) -> None:
    """Validate two-level tabs, shared controller, and no private reach-in."""
    root = root.expanduser().resolve(strict=True)
    for relative in _TOUCHED_PATHS:
        path = root / relative
        _require(path.is_file(), "WAVE2W_TOUCHED_FILE_MISSING:" + relative)
        raw = path.read_bytes()
        _require(all(byte < 128 for byte in raw), "WAVE2W_NON_ASCII_SOURCE:" + relative)
        text = raw.decode("ascii")
        _require(
            len(text.splitlines()) <= 500,
            "WAVE2W_MODULE_EXCEEDS_500_LINES:" + relative,
        )
        ast.parse(text, filename=relative)
    print("WAVE2W MODULE SIZE MAXIMUM 500: PASS")
    print("WAVE2W ASCII SOURCE CONTRACT: PASS")

    safety = (root / _TOUCHED_PATHS[0]).read_text(encoding="utf-8")
    host = (root / _TOUCHED_PATHS[1]).read_text(encoding="utf-8")
    workspace = (root / _TOUCHED_PATHS[3]).read_text(encoding="utf-8")
    full = (root / _TOUCHED_PATHS[4]).read_text(encoding="utf-8")
    _require(
        'section_tabs.addTab(engineering_audit_page, "Engineering Audit")' in safety,
        "WAVE2W_ENGINEERING_AUDIT_SECTION_MISSING",
    )
    _require(
        "section_tabs.addTab(workspace, _ENGINEERING_DIAGNOSTICS_LABEL)" in host,
        "WAVE2W_ENGINEERING_DIAGNOSTICS_SECTION_MISSING",
    )
    _require(
        'tabs.addTab(full_page, "Full Engineering Diagnostics")' in workspace,
        "WAVE2W_FULL_DIAGNOSTICS_TAB_MISSING",
    )
    _require(
        'tabs.addTab(pontual_page, "Pontual Engineering Diagnostics")' in workspace,
        "WAVE2W_PONTUAL_DIAGNOSTICS_TAB_MISSING",
    )
    _require(
        workspace.count("controller=active_controller") == 2,
        "WAVE2W_SHARED_CONTROLLER_CONTRACT_MISSING",
    )
    print("WAVE2W TWO-LEVEL ENGINEERING SAFETY HIERARCHY: PASS")
    print("WAVE2W SHARED DIAGNOSTICS CONTROLLER: PASS")

    for fragment in (
        'QPushButton("Run All Engineering Diagnostics")',
        'QPushButton("Cancel Diagnostics")',
        'setObjectName("full_engineering_diagnostics_run_button")',
        'setObjectName("full_engineering_diagnostics_cancel_button")',
        'sonar.start("All collectors")',
        "panel.start_full_engineering_diagnostics = start_run",
        "panel.cancel_full_engineering_diagnostics = cancel_run",
        "FULL_ENGINEERING_DIAGNOSTIC_COLLECTORS",
    ):
        _require(fragment in full, "WAVE2W_FULL_RUN_FRAGMENT_MISSING:" + fragment)
    for label in ("BOM", "Ruff", "Architecture", "Shadow"):
        _require('("' + label + '",' in full, "WAVE2W_COLLECTOR_MISSING:" + label)
    cancel_start = full.index("    def cancel_run() -> None:")
    cancel_end = full.index("    def set_project_root", cancel_start)
    cancel_block = full[cancel_start:cancel_end]
    _require(
        'state["future"] = None' not in cancel_block,
        "WAVE2W_CANCEL_PRETENDS_WORKER_SETTLED",
    )
    _require(
        "set_busy(False)" not in cancel_block,
        "WAVE2W_CANCEL_REENABLES_RUN_BEFORE_SETTLEMENT",
    )
    _require(
        "engineering_audit_page.findChildren(QPushButton)" in safety,
        "WAVE2W_AUDIT_BUTTON_SCOPE_NOT_ISOLATED",
    )
    _require(
        "panel.findChildren(QPushButton)" not in safety,
        "WAVE2W_AUDIT_BUTTON_SCOPE_LEAKS_TO_DIAGNOSTICS",
    )
    print("WAVE2W FULL DIAGNOSTICS RUN-ALL CONTRACT: PASS")
    print("WAVE2W COOPERATIVE CANCEL SETTLEMENT CONTRACT: PASS")
    print("WAVE2W AUDIT-DIAGNOSTICS BUTTON ISOLATION: PASS")

    product_paths = tuple(root / relative for relative in _TOUCHED_PATHS[:5])
    cross_box_paths = product_paths[1:]
    imports = frozenset().union(*(_imports(path) for path in cross_box_paths))
    _require(
        "_reasoner_tools_gui_engineering_safety_full_audit" not in imports,
        "WAVE2W_FULL_AUDIT_PRIVATE_IMPORT",
    )
    _require(
        not any("pontual" in value.lower() for value in imports),
        "WAVE2W_PONTUAL_AUDIT_PRIVATE_IMPORT",
    )
    combined = "\n".join(path.read_text(encoding="utf-8") for path in product_paths)
    for token in ("sqlite3", "EngineeringDiagnosticsStore(", "apply_patch"):
        _require(token not in combined, "WAVE2W_FORBIDDEN_SURFACE:" + token)
    print("WAVE2W FULL AUDIT PRIVATE IMPORTS: 0")
    print("WAVE2W PONTUAL AUDIT PRIVATE IMPORTS: 0")
    print("WAVE2W DIRECT SQLITE ACCESS: 0")
    print("WAVE2W COMPETING STORE OWNERS: 0")
    print("WAVE2W PUBLIC-CONTRACT-ONLY COMMUNICATION: PASS")
