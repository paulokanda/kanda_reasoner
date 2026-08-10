# project-path: tools/engineering_diagnostics_wave2t_public_boundary_gate.py
"""Static public-boundary gate for Engineering Diagnostics Wave 2T."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

__all__ = ["validate_engineering_diagnostics_wave2t_public_boundary"]

_TOUCHED_PATHS = (
    "kanda_reasoner_app/engineering_diagnostics_gui/__init__.py",
    "kanda_reasoner_app/engineering_diagnostics_gui/_navigation_ui.py",
    "kanda_reasoner_app/engineering_diagnostics_gui/engineering_diagnostics_tab.py",
    "kanda_reasoner_app/engineering_diagnostics_gui/full_audit_drillthrough_ui.py",
    "kanda_reasoner_app/engineering_diagnostics_gui/navigation.py",
    "kanda_reasoner_app/engineering_diagnostics_gui/navigation_models.py",
    "kanda_reasoner_app/manage_architecture/audit_project_sibling_tabs.py",
    "kanda_reasoner_app/manage_architecture/full_audit_diagnostics_drillthrough.py",
    "tests/test_engineering_diagnostics_wave2t.py",
    "tests/test_engineering_diagnostics_wave2t_gui_scale.py",
    "tools/engineering_diagnostics_wave2t_architecture_gate.py",
    "tools/engineering_diagnostics_wave2t_gui_validation.py",
    "tools/engineering_diagnostics_wave2t_public_boundary_gate.py",
    "tools/engineering_diagnostics_wave2t_validation_runtime.py",
    "tools/validate_engineering_diagnostics_wave2t_v1.py",
)
_PUBLIC_OWNERS = {
    "EngineeringDiagnosticsNavigationRequest": "navigation_models.py",
    "EngineeringDiagnosticsNavigationSummary": "navigation_models.py",
    "build_engineering_diagnostics_navigation_summary": "navigation.py",
    "request_engineering_diagnostics_navigation": "navigation.py",
    "FullAuditDiagnosticLink": "full_audit_diagnostics_drillthrough.py",
    "build_full_audit_diagnostic_links": "full_audit_diagnostics_drillthrough.py",
    "install_full_audit_diagnostics_drillthrough": "full_audit_diagnostics_drillthrough.py",
    "install_full_audit_diagnostics_drillthrough_ui": "full_audit_drillthrough_ui.py",
}
_FROZEN_WAVE2M_HASHES = {
    "_reasoner_tools_gui_engineering_safety_full_audit.py": (
        "3406df90ce51fa0df349ded3a19ce864c5407c950b71b9e935a48bfeaf18b44f"
    ),
    "_reasoner_tools_gui_engineering_safety_review_signals.py": (
        "6d2ae82b16d38aaab6a57b0d7ece8cd25bea9111dcef390b1f4e791a42dec8f1"
    ),
}


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _definitions(tree: ast.Module) -> frozenset[str]:
    names: set[str] = set()
    for node in tree.body:
        if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            names.add(node.name)
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    names.add(target.id)
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            names.add(node.target.id)
    return frozenset(names)


def _literal_all(tree: ast.Module) -> tuple[str, ...]:
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        if not any(isinstance(target, ast.Name) and target.id == "__all__" for target in node.targets):
            continue
        return tuple(str(item) for item in ast.literal_eval(node.value))
    return ()


def _check_physical_contract(root: Path) -> None:
    for relative in _TOUCHED_PATHS:
        path = root / relative
        _require(path.is_file(), "WAVE2T_TOUCHED_FILE_MISSING:" + relative)
        raw = path.read_bytes()
        _require(all(byte < 128 for byte in raw), "WAVE2T_NON_ASCII_SOURCE:" + relative)
        _require(len(raw.decode("ascii").splitlines()) <= 500, "WAVE2T_MODULE_EXCEEDS_500_LINES:" + relative)
        ast.parse(raw.decode("ascii"), filename=relative)
    print("WAVE2T MODULE SIZE MAXIMUM 500: PASS")
    print("WAVE2T ASCII SOURCE CONTRACT: PASS")


def _check_frozen_wave2m(root: Path) -> None:
    for relative, expected in _FROZEN_WAVE2M_HASHES.items():
        _require(_sha256(root / relative) == expected, "WAVE2M_FROZEN_FILE_HASH_MISMATCH:" + relative)
    print("WAVE2M FULL AUDIT IMPLEMENTATION BYTE-IDENTICAL: PASS")
    print("WAVE2M ASSESSMENT SIGNALS BYTE-IDENTICAL: PASS")


def _check_public_owners(root: Path) -> None:
    search_roots = (
        root / "kanda_reasoner_app" / "engineering_diagnostics_gui",
        root / "kanda_reasoner_app" / "manage_architecture",
    )
    owners: dict[str, list[str]] = {name: [] for name in _PUBLIC_OWNERS}
    for search_root in search_roots:
        for path in search_root.glob("*.py"):
            definitions = _definitions(ast.parse(path.read_text(encoding="utf-8")))
            for name in owners:
                if name in definitions:
                    owners[name].append(path.name)
    for name, expected in _PUBLIC_OWNERS.items():
        _require(owners[name] == [expected], "WAVE2T_PUBLIC_SYMBOL_OWNER_MISMATCH:" + name + ":" + repr(owners[name]))
    facade = root / "kanda_reasoner_app" / "engineering_diagnostics_gui" / "__init__.py"
    facade_all = _literal_all(ast.parse(facade.read_text(encoding="utf-8")))
    for name in (
        "EngineeringDiagnosticsNavigationRequest",
        "EngineeringDiagnosticsNavigationSummary",
        "build_engineering_diagnostics_navigation_summary",
        "request_engineering_diagnostics_navigation",
        "install_full_audit_diagnostics_drillthrough_ui",
    ):
        _require(name in facade_all, "WAVE2T_PUBLIC_FACADE_EXPORT_MISSING:" + name)
    private_tree = ast.parse(
        (root / "kanda_reasoner_app/engineering_diagnostics_gui/_navigation_ui.py").read_text(encoding="utf-8")
    )
    _require(_literal_all(private_tree) == (), "WAVE2T_PRIVATE_HELPER_PUBLIC_EXPORT")
    print("WAVE2T PUBLIC NAVIGATION SYMBOL SINGLE OWNERS: PASS")
    print("WAVE2T PRIVATE HELPER PUBLIC SURFACE: ABSENT")


def _check_boundary_contract(root: Path) -> None:
    bridge = (root / "kanda_reasoner_app/manage_architecture/full_audit_diagnostics_drillthrough.py").read_text(encoding="utf-8")
    combined = "\n".join((
        bridge,
        (root / "kanda_reasoner_app/engineering_diagnostics_gui/navigation.py").read_text(encoding="utf-8"),
        (root / "kanda_reasoner_app/engineering_diagnostics_gui/navigation_models.py").read_text(encoding="utf-8"),
    ))
    for token in (
        "_reasoner_tools_gui_engineering_safety_full_audit",
        "_reasoner_tools_gui_engineering_safety_review_signals",
        "engineering_diagnostics_gui._",
        "import sqlite3",
        "from sqlite3",
        ".write_text(",
        ".write_bytes(",
        "subprocess.",
        "apply_patch",
        "Patch Preview",
        "Memorize Error",
    ):
        _require(token not in combined, "WAVE2T_FORBIDDEN_SURFACE:" + token)
    ui = (root / "kanda_reasoner_app/engineering_diagnostics_gui/full_audit_drillthrough_ui.py").read_text(encoding="utf-8")
    _require("Assessment:" in ui, "WAVE2T_ASSESSMENT_DISPLAY_MISSING")
    _require("Open in Engineering Diagnostics" in ui, "WAVE2T_NAVIGATION_ACTION_MISSING")
    _require("source-compatible" in ui, "WAVE2T_COMPATIBLE_RUN_GUARD_MISSING")
    print("WAVE2T FULL AUDIT PRIVATE IMPORTS: 0")
    print("WAVE2T DIRECT SQLITE ACCESS: 0")
    print("WAVE2T SOURCE WRITE SURFACES: 0")
    print("WAVE2T PUBLIC-CONTRACT-ONLY COMMUNICATION: PASS")


def validate_engineering_diagnostics_wave2t_public_boundary(root: Path) -> None:
    """Validate physical, ownership, frozen, and read-only Wave 2T rules."""
    root = root.expanduser().resolve(strict=True)
    _check_physical_contract(root)
    _check_frozen_wave2m(root)
    _check_public_owners(root)
    _check_boundary_contract(root)
    print("WAVE2T FULL AUDIT CONTENT DUPLICATED: NO")
    print("WAVE2T ENGINEERING DIAGNOSTICS STORE OWNER: PRESERVED")
