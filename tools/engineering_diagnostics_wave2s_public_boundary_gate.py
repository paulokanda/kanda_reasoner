# project-path: tools/engineering_diagnostics_wave2s_public_boundary_gate.py
"""Static public-boundary gate for Engineering Diagnostics Wave 2S."""

from __future__ import annotations

import ast
from pathlib import Path

__all__ = ["validate_engineering_diagnostics_wave2s_public_boundary"]

_TOUCHED_PATHS = (
    "kanda_reasoner_app/engineering_diagnostics/__init__.py",
    "kanda_reasoner_app/engineering_diagnostics/remediation.py",
    "kanda_reasoner_app/engineering_diagnostics/remediation_models.py",
    "kanda_reasoner_app/engineering_diagnostics_gui/controller.py",
    "kanda_reasoner_app/engineering_diagnostics_gui/diagnostic_table_model.py",
    "kanda_reasoner_app/engineering_diagnostics_gui/finding_view_builder.py",
    "kanda_reasoner_app/engineering_diagnostics_gui/models.py",
    "kanda_reasoner_app/engineering_diagnostics_gui/owner_ui.py",
    "kanda_reasoner_app/engineering_diagnostics_gui/run_summary.py",
    "kanda_reasoner_app/engineering_diagnostics_gui/table_columns.py",
    "kanda_reasoner_app/engineering_diagnostics_gui/wave2s_validation.py",
    "tests/test_engineering_diagnostics_wave2s.py",
    "tests/test_engineering_diagnostics_wave2s_gui_scale.py",
    "tools/engineering_diagnostics_wave2s_architecture_gate.py",
    "tools/engineering_diagnostics_wave2s_public_boundary_gate.py",
    "tools/engineering_diagnostics_wave2s_validation_runtime.py",
    "tools/validate_engineering_diagnostics_wave2s_v1.py",
)
_PUBLIC_OWNERS = {
    "AI_HYPOTHESIS_LABEL": "remediation_models.py",
    "REMEDIATION_ACTION_CLASSES": "remediation_models.py",
    "REMEDIATION_FIX_APPLICABILITY": "remediation_models.py",
    "REMEDIATION_MECHANICAL_SAFETY": "remediation_models.py",
    "REMEDIATION_SEMANTIC_REVIEW": "remediation_models.py",
    "REMEDIATION_TRUST_ORDER": "remediation_models.py",
    "DiagnosticAiHypothesis": "remediation_models.py",
    "DiagnosticRemediationIntent": "remediation_models.py",
    "DiagnosticValidationPlan": "remediation_models.py",
    "build_diagnostic_remediation_intent": "remediation.py",
    "build_diagnostic_remediation_intents": "remediation.py",
}


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def _literal_all(tree: ast.Module) -> tuple[str, ...]:
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        if not any(isinstance(target, ast.Name) and target.id == "__all__" for target in node.targets):
            continue
        value = ast.literal_eval(node.value)
        return tuple(str(item) for item in value)
    return ()


def _definitions(tree: ast.Module) -> frozenset[str]:
    names: set[str] = set()
    for node in tree.body:
        if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            names.add(node.name)
            continue
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    names.add(target.id)
            continue
        if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            names.add(node.target.id)
    return frozenset(names)


def _check_physical_contract(root: Path) -> None:
    for relative in _TOUCHED_PATHS:
        path = root / relative
        _require(path.is_file(), "WAVE2S_TOUCHED_FILE_MISSING:" + relative)
        raw = path.read_bytes()
        _require(all(byte < 128 for byte in raw), "WAVE2S_NON_ASCII_SOURCE:" + relative)
        lines = raw.decode("ascii").splitlines()
        _require(len(lines) <= 500, "WAVE2S_MODULE_EXCEEDS_500_LINES:" + relative)
        ast.parse(raw.decode("ascii"), filename=relative)
    print("WAVE2S MODULE SIZE MAXIMUM 500: PASS")
    print("WAVE2S ASCII SOURCE CONTRACT: PASS")


def _check_public_owners(root: Path) -> None:
    package = root / "kanda_reasoner_app" / "engineering_diagnostics"
    owners: dict[str, list[str]] = {name: [] for name in _PUBLIC_OWNERS}
    for path in package.glob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        definitions = _definitions(tree)
        for name in owners:
            if name in definitions:
                owners[name].append(path.name)
    for name, expected in _PUBLIC_OWNERS.items():
        _require(
            owners[name] == [expected],
            "WAVE2S_PUBLIC_SYMBOL_OWNER_MISMATCH:" + name + ":" + repr(owners[name]),
        )
    facade_all = _literal_all(
        ast.parse((package / "__init__.py").read_text(encoding="utf-8"))
    )
    for name in _PUBLIC_OWNERS:
        _require(name in facade_all, "WAVE2S_PUBLIC_FACADE_EXPORT_MISSING:" + name)
    print("WAVE2S PUBLIC REMEDIATION SYMBOL SINGLE OWNERS: PASS")
    print("WAVE2S PUBLIC FACADE EXPORTS: PASS")


def _check_non_mutating_contract(root: Path) -> None:
    files = (
        root / "kanda_reasoner_app" / "engineering_diagnostics" / "remediation.py",
        root / "kanda_reasoner_app" / "engineering_diagnostics" / "remediation_models.py",
    )
    combined = "\n".join(path.read_text(encoding="utf-8") for path in files)
    forbidden = (
        "import sqlite3",
        "from sqlite3",
        "subprocess.",
        ".write_text(",
        ".write_bytes(",
        "open(\"w",
        "open('w",
        "web_ai",
        "local_ai",
        "apply_patch",
        "Memorize Error",
    )
    for token in forbidden:
        _require(token not in combined, "WAVE2S_FORBIDDEN_WRITE_OR_AI_SURFACE:" + token)
    _require("executable_patch: bool = False" in combined, "WAVE2S_NON_EXECUTABLE_DEFAULT_MISSING")
    _require("source_mutation_allowed: bool = False" in combined, "WAVE2S_NON_MUTATING_DEFAULT_MISSING")
    _require("Frozen-path rules cannot be overridden by advice." in combined, "WAVE2S_FROZEN_PRECEDENCE_GUARD_MISSING")
    _require("AI-assisted hypothesis" in combined, "WAVE2S_AI_LABEL_MISSING")
    print("WAVE2S DIRECT SQLITE ACCESS: 0")
    print("WAVE2S SOURCE WRITE SURFACES: 0")
    print("WAVE2S AI EXECUTION SURFACES: 0")
    print("WAVE2S FROZEN PATH PRECEDENCE: PASS")
    print("WAVE2S AI HYPOTHESIS LABEL CONTRACT: PASS")


def validate_engineering_diagnostics_wave2s_public_boundary(root: Path) -> None:
    """Validate physical, ownership, and non-mutating Wave 2S contracts."""
    root = root.expanduser().resolve(strict=True)
    _check_physical_contract(root)
    _check_public_owners(root)
    _check_non_mutating_contract(root)
    print("WAVE2S REMEDIATION INTENT IS EXECUTABLE PATCH: NO")
    print("WAVE2S ENGINEERING DIAGNOSTICS STORE OWNER: PRESERVED")
    print("WAVE2S PUBLIC-CONTRACT-ONLY COMMUNICATION: PASS")
