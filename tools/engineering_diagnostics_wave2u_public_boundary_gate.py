# project-path: tools/engineering_diagnostics_wave2u_public_boundary_gate.py
"""Static public-boundary gate for Engineering Diagnostics Wave 2U."""

from __future__ import annotations

import ast
from pathlib import Path

__all__ = ["validate_engineering_diagnostics_wave2u_public_boundary"]

_TOUCHED_PATHS = (
    "kanda_reasoner_app/engineering_diagnostics_patch_preview/__init__.py",
    "kanda_reasoner_app/engineering_diagnostics_patch_preview/models.py",
    "kanda_reasoner_app/engineering_diagnostics_patch_preview/policy.py",
    "kanda_reasoner_app/engineering_diagnostics_patch_preview/preview.py",
    "kanda_reasoner_app/engineering_diagnostics_patch_preview/storage.py",
    "kanda_reasoner_app/engineering_diagnostics_patch_preview/transformations.py",
    "kanda_reasoner_app/engineering_diagnostics_gui/engineering_diagnostics_tab.py",
    "kanda_reasoner_app/engineering_diagnostics_gui/patch_preview_ui.py",
    "tests/test_engineering_diagnostics_wave2u.py",
    "tests/test_engineering_diagnostics_wave2u_gui_scale.py",
    "tools/engineering_diagnostics_wave2u_architecture_gate.py",
    "tools/engineering_diagnostics_wave2u_gui_validation.py",
    "tools/engineering_diagnostics_wave2u_public_boundary_gate.py",
    "tools/engineering_diagnostics_wave2u_validation_runtime.py",
    "tools/validate_engineering_diagnostics_wave2u_v1.py",
)
_PUBLIC_OWNERS = {
    "GovernedPatchPreviewPlan": "models.py",
    "GovernedPatchPreviewFile": "models.py",
    "GovernedPatchPreviewRecord": "models.py",
    "build_governed_patch_preview_plan": "policy.py",
    "patch_preview_approval_token": "policy.py",
    "create_governed_patch_preview": "preview.py",
    "render_governed_patch_preview": "preview.py",
}


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def _definitions(tree: ast.Module) -> frozenset[str]:
    values: set[str] = set()
    for node in tree.body:
        if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            values.add(node.name)
    return frozenset(values)


def _literal_all(tree: ast.Module) -> tuple[str, ...]:
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        if any(
            isinstance(target, ast.Name) and target.id == "__all__"
            for target in node.targets
        ):
            return tuple(str(item) for item in ast.literal_eval(node.value))
    return ()


def validate_engineering_diagnostics_wave2u_public_boundary(root: Path) -> None:
    """Validate physical, ownership, isolation, and non-installable contracts."""
    root = root.expanduser().resolve(strict=True)
    for relative in _TOUCHED_PATHS:
        path = root / relative
        _require(path.is_file(), "WAVE2U_TOUCHED_FILE_MISSING:" + relative)
        raw = path.read_bytes()
        _require(all(byte < 128 for byte in raw), "WAVE2U_NON_ASCII_SOURCE:" + relative)
        _require(
            len(raw.decode("ascii").splitlines()) <= 500,
            "WAVE2U_MODULE_EXCEEDS_500_LINES:" + relative,
        )
        ast.parse(raw.decode("ascii"), filename=relative)
    print("WAVE2U MODULE SIZE MAXIMUM 500: PASS")
    print("WAVE2U ASCII SOURCE CONTRACT: PASS")

    package_root = root / "kanda_reasoner_app/engineering_diagnostics_patch_preview"
    owners: dict[str, list[str]] = {name: [] for name in _PUBLIC_OWNERS}
    for path in package_root.glob("*.py"):
        definitions = _definitions(ast.parse(path.read_text(encoding="utf-8")))
        for name in owners:
            if name in definitions:
                owners[name].append(path.name)
    for name, expected in _PUBLIC_OWNERS.items():
        _require(
            owners[name] == [expected],
            "WAVE2U_PUBLIC_SYMBOL_OWNER_MISMATCH:" + name + ":" + repr(owners[name]),
        )
    facade = ast.parse((package_root / "__init__.py").read_text(encoding="utf-8"))
    facade_all = _literal_all(facade)
    for name in _PUBLIC_OWNERS:
        _require(name in facade_all, "WAVE2U_PUBLIC_FACADE_EXPORT_MISSING:" + name)
    print("WAVE2U PUBLIC PATCH PREVIEW SYMBOL SINGLE OWNERS: PASS")

    combined = "\n".join(path.read_text(encoding="utf-8") for path in package_root.glob("*.py"))
    for token in (
        "sqlite3",
        "apply_ruff_correction_preview",
        "Authorize Project Update",
        "Memorize Error",
        "Confirm and Write",
        "engineering_diagnostics_gui._",
        "source_hygiene._",
    ):
        _require(token not in combined, "WAVE2U_FORBIDDEN_SURFACE:" + token)
    _require('"--select",\n        plan.code' in combined, "WAVE2U_RUFF_RULE_SCOPE_MISSING")
    _require('"--fix-only"' in combined, "WAVE2U_ISOLATED_RUFF_FIX_MISSING")
    _require("ruff format" not in combined.lower(), "WAVE2U_GLOBAL_FORMATTER_SURFACE")
    _require("PREVIEW_READY_FOR_GOVERNED_VALIDATION" in combined, "WAVE2U_PREVIEW_STATUS_MISSING")
    _require("source_mutation_allowed=False" in combined, "WAVE2U_NON_MUTATION_CONTRACT_MISSING")
    _require("installable=False" in combined, "WAVE2U_NON_INSTALLABLE_CONTRACT_MISSING")
    print("WAVE2U DIRECT SQLITE ACCESS: 0")
    print("WAVE2U SOURCE APPLY SURFACES: 0")
    print("WAVE2U GLOBAL RUFF FIX SURFACES: 0")
    print("WAVE2U PUBLIC-CONTRACT-ONLY COMMUNICATION: PASS")
    print("WAVE2U SEPARATE GOVERNED BOX: PASS")
