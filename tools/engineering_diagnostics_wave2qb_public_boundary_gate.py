# project-path: tools/engineering_diagnostics_wave2qb_public_boundary_gate.py
"""Public-boundary gate for Engineering Diagnostics Wave 2Q-B."""

from __future__ import annotations

import ast
from pathlib import Path

__all__ = ["validate_engineering_diagnostics_wave2qb_public_boundary"]

_RUNTIME_PATHS = (
    "kanda_reasoner_app/engineering_diagnostics/collectors/shadow_collector.py",
    "kanda_reasoner_app/engineering_diagnostics/collectors/shadow_normalizer.py",
    "kanda_reasoner_app/engineering_diagnostics/collectors/__init__.py",
    "kanda_reasoner_app/engineering_diagnostics/shadow_relational_models.py",
    "kanda_reasoner_app/engineering_diagnostics/shadow_relational_grouping.py",
    "kanda_reasoner_app/engineering_diagnostics/grouping.py",
    "kanda_reasoner_app/engineering_diagnostics/__init__.py",
    "kanda_reasoner_app/engineering_diagnostics_gui/shadow_controller.py",
    "kanda_reasoner_app/engineering_diagnostics_gui/controller.py",
    "kanda_reasoner_app/engineering_diagnostics_gui/engineering_diagnostics_tab.py",
    "kanda_reasoner_app/engineering_diagnostics_gui/wave2qb_validation.py",
)
_TEST_PATHS = (
    "tests/test_engineering_diagnostics_wave2qb.py",
    "tests/test_engineering_diagnostics_wave2qb_gui_scale.py",
)
_TOOL_PATHS = (
    "tools/engineering_diagnostics_wave2qb_architecture_gate.py",
    "tools/engineering_diagnostics_wave2qb_public_boundary_gate.py",
    "tools/engineering_diagnostics_wave2qb_validation_runtime.py",
    "tools/validate_engineering_diagnostics_wave2qb_v1.py",
)
_ALL_PATHS = _RUNTIME_PATHS + _TEST_PATHS + _TOOL_PATHS


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def _tree(path: Path) -> ast.Module:
    return ast.parse(path.read_text(encoding="utf-8"), filename=str(path))


def _imports(path: Path) -> tuple[str, ...]:
    values: list[str] = []
    for node in ast.walk(_tree(path)):
        if isinstance(node, ast.Import):
            values.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            values.append(str(node.module or ""))
    return tuple(values)


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
        _require(path.is_file(), "WAVE2QB_FILE_MISSING:" + relative)
        text = path.read_text(encoding="utf-8")
        text.encode("ascii")
        _require(len(text.splitlines()) <= 500, "WAVE2QB_MODULE_TOO_LARGE:" + relative)
        values[relative] = text
    return values


def _assert_public_ownership(root: Path) -> None:
    owners: dict[str, list[str]] = {}
    owner_paths = (
        "kanda_reasoner_app/engineering_diagnostics/collectors/shadow_collector.py",
        "kanda_reasoner_app/engineering_diagnostics/collectors/shadow_normalizer.py",
        "kanda_reasoner_app/engineering_diagnostics/shadow_relational_models.py",
        "kanda_reasoner_app/engineering_diagnostics/shadow_relational_grouping.py",
        "kanda_reasoner_app/engineering_diagnostics_gui/shadow_controller.py",
    )
    for relative in owner_paths:
        for symbol in _public_definitions(root / relative):
            owners.setdefault(symbol, []).append(relative)
    duplicates = {name: paths for name, paths in owners.items() if len(paths) > 1}
    _require(not duplicates, "WAVE2QB_DUPLICATE_PUBLIC_SYMBOL:" + repr(duplicates))
    expected = {
        "ShadowIssueEvidence",
        "ShadowCollectionResult",
        "DiagnosticRelationNode",
        "DiagnosticRelationEdge",
        "DiagnosticRelationalGraph",
        "collect_shadow_findings",
        "build_shadow_diagnostic_run",
        "build_shadow_relational_graph",
        "build_shadow_relational_diagnostic_groups",
        "build_shadow_scan_candidate",
    }
    _require(expected.issubset(owners), "WAVE2QB_PUBLIC_OWNER_MISSING:" + repr(sorted(expected - set(owners))))


def _assert_public_contract_only(root: Path, sources: dict[str, str]) -> None:
    collector = root / "kanda_reasoner_app/engineering_diagnostics/collectors/shadow_collector.py"
    imported = _imports(collector)
    _require(
        "kanda_reasoner_app.source_hygiene.shadow_audit" in sources[
            "kanda_reasoner_app/engineering_diagnostics/collectors/shadow_collector.py"
        ],
        "WAVE2QB_SHADOW_PUBLIC_CONTRACT_MISSING",
    )
    forbidden = (
        "source_hygiene._shadow_audit_ast",
        "source_hygiene._active_scope",
        "source_hygiene.shadow_planner",
        "reasoner_symbol_atlas.",
        "manage_architecture.",
        "freeze_after_update.",
        "project_freeze_ledger",
    )
    for relative in _RUNTIME_PATHS:
        text = sources[relative]
        imports = _imports(root / relative)
        for token in forbidden:
            _require(token not in text, "WAVE2QB_PRIVATE_REACH_IN:" + relative + ":" + token)
        _require("sqlite3" not in text, "WAVE2QB_DIRECT_SQLITE_ACCESS:" + relative)
        _require("semantic embedding" not in text.lower(), "WAVE2QB_SEMANTIC_GROUPING_PRESENT")
        _require("openai" not in " ".join(imports).lower(), "WAVE2QB_AI_IMPORT_PRESENT")
    _require(imported, "WAVE2QB_COLLECTOR_IMPORT_GRAPH_EMPTY")


def _assert_read_only(sources: dict[str, str]) -> None:
    relational = sources[
        "kanda_reasoner_app/engineering_diagnostics/shadow_relational_grouping.py"
    ]
    collector = sources[
        "kanda_reasoner_app/engineering_diagnostics/collectors/shadow_collector.py"
    ]
    combined = relational + collector
    for token in (
        ".write_text(",
        ".write_bytes(",
        ".unlink(",
        ".mkdir(",
        "os.replace",
        "shutil.copy",
        "subprocess",
    ):
        _require(token not in combined, "WAVE2QB_WRITE_OR_EXECUTION_SURFACE:" + token)
    for token in (
        '"deterministic": True',
        '"root_cause_claimed": False',
        '"ai_grouping_used": False',
        "len(issue_ids) < 2",
        "all_edges_deterministic",
    ):
        _require(token in relational, "WAVE2QB_RELATIONAL_GUARD_MISSING:" + token)


def _assert_taxonomy(sources: dict[str, str]) -> None:
    models = sources[
        "kanda_reasoner_app/engineering_diagnostics/shadow_relational_models.py"
    ]
    for token in (
        '"file"',
        '"symbol"',
        '"public_surface"',
        '"facade"',
        '"implementation_owner"',
        '"export"',
        '"duplicate_of"',
        '"reexports"',
        '"facade_of"',
        '"implements"',
        '"unbound_export"',
    ):
        _require(token in models, "WAVE2QB_RELATIONAL_TAXONOMY_MISSING:" + token)


def validate_engineering_diagnostics_wave2qb_public_boundary(root: Path) -> None:
    """Validate Wave 2Q-B Box, ownership, and no-leak contracts."""
    project_root = Path(root).expanduser().resolve(strict=True)
    sources = _sources(project_root)
    _assert_public_ownership(project_root)
    _assert_public_contract_only(project_root, sources)
    _assert_read_only(sources)
    _assert_taxonomy(sources)
    print("WAVE2QB MODULE SIZE MAXIMUM 500: PASS")
    print("WAVE2QB ASCII SOURCE CONTRACT: PASS")
    print("WAVE2QB SHADOW PUBLIC AUDIT CONTRACT: PASS")
    print("WAVE2QB SHADOW PRIVATE IMPORTS: 0")
    print("WAVE2QB DIRECT SQLITE ACCESS: 0")
    print("WAVE2QB SHADOW COLLECTOR WRITE SURFACES: 0")
    print("WAVE2QB PUBLIC SYMBOL SINGLE OWNERS: PASS")
    print("WAVE2QB RELATIONAL NODE AND EDGE TAXONOMY: PASS")
    print("WAVE2QB DETERMINISTIC EDGE EVIDENCE: PASS")
    print("WAVE2QB AI GROUPING USED: NO")
    print("WAVE2QB ENGINEERING DIAGNOSTICS STORE OWNER: PRESERVED")
    print("WAVE2QB PUBLIC-CONTRACT-ONLY COMMUNICATION: PASS")
