"""Validate Stage 5 Griffe exports and mypy scope repair behavior."""

from __future__ import annotations

import hashlib
from pathlib import Path

from kanda_reasoner_app.manage_architecture.large_file_refactor_planner import griffe_api_fitness_adapter as griffe
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.advanced_quality_evidence_models import FindingSeverity, RawEvidenceReference
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.griffe_public_surface import child_public_override, griffe_public_state
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.mypy_fitness_adapter import _analysis_target_relative

FEATURE_ID = "advanced-quality-review-stage5-runtime-cumulative-correction-repair-v1"


def main() -> int:
    parent = {"exports": ["PublicOwner", "public_function"]}
    assert child_public_override(parent, "PublicOwner") is True
    assert child_public_override(parent, "ImportedAlias") is False
    assert griffe_public_state({}, "ImportedAlias", explicit_export=False) is False
    assert griffe_public_state({}, "PublicOwner", explicit_export=True) is True
    print("GRIFFE_EXPLICIT_EXPORTS_OVERRIDE_NAME_FALLBACK: PASS")

    ref = RawEvidenceReference(
        engine_id="griffe",
        relative_path="griffe/preview.json",
        sha256=hashlib.sha256(b"{}").hexdigest(),
        byte_size=2,
    )
    baseline = {
        "pkg.mod.ImportedAlias": griffe._ApiSymbol(
            path="pkg.mod.ImportedAlias", kind="alias", public=False,
            parameters=(), returns="null", alias_target="pkg.dep.ImportedAlias",
        ),
        "pkg.mod.PublicOwner": griffe._ApiSymbol(
            path="pkg.mod.PublicOwner", kind="class", public=True,
            parameters=(), returns="null", alias_target="",
        ),
    }
    findings = griffe._compare_models(
        baseline, {}, engine_version="2.1.0", raw_bytes=b"{}", diagnostics=[]
    )
    blocked = {item.symbol_identity for item in findings if item.severity is FindingSeverity.BLOCKER}
    assert blocked == {"pkg.mod.PublicOwner"}
    print("GRIFFE_INCIDENTAL_IMPORTED_ALIAS_NOT_PUBLIC_CONTRACT: PASS")
    print("GRIFFE_DECLARED_EXPORT_REMOVAL_REMAINS_BLOCKED: PASS")

    target = "kanda_reasoner_app/reasoner_symbol_atlas/main_helper_mapper.py"
    assert _analysis_target_relative(target) == "kanda_reasoner_app/reasoner_symbol_atlas"
    print("MYPY_TARGET_PACKAGE_SCOPE_DERIVED_FROM_ANALYSIS_IDENTITY: PASS")

    project_root = Path(__file__).resolve().parents[1]
    planner = project_root / "kanda_reasoner_app" / "manage_architecture" / "large_file_refactor_planner"
    mypy_source = (planner / "mypy_fitness_adapter.py").read_text(encoding="utf-8")
    assert "argv.append(analysis_target)" in mypy_source
    assert "argv.append(str(root))" not in mypy_source
    print("MYPY_FULL_SEALED_PROJECT_ROOT_ARGUMENT_REMOVED: PASS")

    griffe_source = (planner / "griffe_api_fitness_adapter.py").read_text(encoding="utf-8")
    assert "child_public_override(node, child_name)" in griffe_source
    assert "explicit_export=public_override" in griffe_source
    print("GRIFFE_PARENT_EXPORT_SURFACE_PROPAGATES_TO_CHILD_MODEL: PASS")

    touched = [
        planner / "griffe_api_fitness_adapter.py",
        planner / "griffe_public_surface.py",
        planner / "mypy_fitness_adapter.py",
    ]
    for path in touched:
        lines = len(path.read_text(encoding="utf-8").splitlines())
        assert lines <= 500, (path.name, lines)
    print("TOUCHED_MODULES_MAX_500_LINES: PASS")

    print("AQR_STAGE5_GRIFFE_EXPORTS_AND_MYPY_SCOPE_REPAIR: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
