# project-path: tools/engineering_diagnostics_wave2v_public_boundary_gate.py
"""Corrected public-boundary gate for the Wave 2V Pontual run console."""

from __future__ import annotations

import ast
from pathlib import Path

__all__ = ["validate_engineering_diagnostics_wave2v_public_boundary"]

_TOUCHED_PATHS = (
    "reasoner_tools_gui_engineering_safety_panel.py",
    "kanda_reasoner_app/manage_architecture/audit_project_sibling_tabs.py",
    "kanda_reasoner_app/engineering_diagnostics_gui/engineering_diagnostics_tab.py",
    "kanda_reasoner_app/engineering_diagnostics_gui/engineering_diagnostics_sonar.py",
    "kanda_reasoner_app/engineering_diagnostics_gui/engineering_diagnostics_workspace.py",
    "tests/test_engineering_diagnostics_wave2v.py",
    "tests/test_engineering_diagnostics_wave2v_gui_scale.py",
    "tools/engineering_diagnostics_wave2v_architecture_gate.py",
    "tools/engineering_diagnostics_wave2v_gui_validation.py",
    "tools/engineering_diagnostics_wave2v_public_boundary_gate.py",
    "tools/engineering_diagnostics_wave2v_validation_runtime.py",
    "tools/validate_engineering_diagnostics_wave2v_v1.py",
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


def validate_engineering_diagnostics_wave2v_public_boundary(root: Path) -> None:
    """Validate retained Pontual run controls under the corrected hierarchy."""
    root = root.expanduser().resolve(strict=True)
    for relative in _TOUCHED_PATHS:
        path = root / relative
        _require(path.is_file(), "WAVE2V_TOUCHED_FILE_MISSING:" + relative)
        raw = path.read_bytes()
        _require(all(byte < 128 for byte in raw), "WAVE2V_NON_ASCII_SOURCE:" + relative)
        _require(
            len(raw.decode("ascii").splitlines()) <= 500,
            "WAVE2V_MODULE_EXCEEDS_500_LINES:" + relative,
        )
        ast.parse(raw.decode("ascii"), filename=relative)
    print("WAVE2V MODULE SIZE MAXIMUM 500: PASS")
    print("WAVE2V ASCII SOURCE CONTRACT: PASS")

    safety = (root / _TOUCHED_PATHS[0]).read_text(encoding="utf-8")
    host = (root / _TOUCHED_PATHS[1]).read_text(encoding="utf-8")
    panel = (root / _TOUCHED_PATHS[2]).read_text(encoding="utf-8")
    sonar = (root / _TOUCHED_PATHS[3]).read_text(encoding="utf-8")
    workspace = (root / _TOUCHED_PATHS[4]).read_text(encoding="utf-8")
    _require(
        'setObjectName("engineering_safety_section_tabs")' in safety,
        "WAVE2V_SECTION_TAB_PROJECTION_MISSING",
    )
    _require(
        "section_tabs.addTab(workspace" in host,
        "WAVE2V_DIAGNOSTICS_SECTION_MISSING",
    )
    _require(
        'tabs.addTab(pontual_page, "Pontual Engineering Diagnostics")' in workspace,
        "WAVE2V_PONTUAL_DIAGNOSTICS_MODE_MISSING",
    )
    _require(
        "workspace.select_pontual_engineering_diagnostics()" in host,
        "WAVE2V_DRILLTHROUGH_PONTUAL_TARGET_MISSING",
    )
    print("WAVE2V ENGINEERING SAFETY CORRECTED PLACEMENT: PASS")
    print("WAVE2V FULL AUDIT DRILL-THROUGH PONTUAL TARGET: PASS")

    for fragment in (
        'QPushButton("Run Engineering Diagnostics")',
        'QPushButton("Cancel Diagnostics")',
        'setObjectName("engineering_diagnostics_run_button")',
        'setObjectName("engineering_diagnostics_cancel_button")',
        "sonar.start(producer_label())",
        "panel.engineering_diagnostics_sonar = sonar",
        "panel.start_engineering_diagnostics = start_scan",
        "panel.cancel_engineering_diagnostics = cancel_scan",
    ):
        _require(fragment in panel, "WAVE2V_RUN_CONSOLE_FRAGMENT_MISSING:" + fragment)
    cancel_start = panel.index("    def cancel_scan() -> None:")
    cancel_end = panel.index("    def activate_baseline() -> None:", cancel_start)
    cancel_block = panel[cancel_start:cancel_end]
    _require(
        'state["future"] = None' not in cancel_block,
        "WAVE2V_CANCEL_PRETENDS_WORKER_SETTLED",
    )
    _require(
        "set_busy(False)" not in cancel_block,
        "WAVE2V_CANCEL_REENABLES_RUN_BEFORE_SETTLEMENT",
    )
    _require(
        "cancel_button.setEnabled(False)" in cancel_block,
        "WAVE2V_CANCEL_BUTTON_NOT_LATCHED",
    )
    print("WAVE2V COOPERATIVE CANCEL SETTLEMENT CONTRACT: PASS")

    _require("GreenSonarActivityMonitor" in sonar, "WAVE2V_PUBLIC_SONAR_OWNER_MISSING")
    _require("_green_sonar" not in sonar, "WAVE2V_PRIVATE_SONAR_REACH_IN")
    imports = frozenset().union(
        *(_imports(root / relative) for relative in _TOUCHED_PATHS[1:5])
    )
    _require(
        "_reasoner_tools_gui_engineering_safety_full_audit" not in imports,
        "WAVE2V_FULL_AUDIT_PRIVATE_IMPORT",
    )
    _require(
        not any("pontual" in value.lower() for value in imports),
        "WAVE2V_PONTUAL_PRIVATE_IMPORT",
    )
    combined = "\n".join((safety, host, panel, sonar, workspace))
    for token in ("sqlite3", "Confirm and Write", "Memorize Error", "apply_patch"):
        _require(token not in combined, "WAVE2V_FORBIDDEN_SURFACE:" + token)
    print("WAVE2V PUBLIC SONAR ADAPTER: PASS")
    print("WAVE2V FULL AUDIT PRIVATE IMPORTS: 0")
    print("WAVE2V PONTUAL AUDIT PRIVATE IMPORTS: 0")
    print("WAVE2V DIRECT SQLITE ACCESS: 0")
    print("WAVE2V SOURCE APPLY SURFACES: 0")
    print("WAVE2V PUBLIC-CONTRACT-ONLY COMMUNICATION: PASS")
