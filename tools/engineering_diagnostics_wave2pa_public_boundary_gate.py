# project-path: tools/engineering_diagnostics_wave2pa_public_boundary_gate.py
"""Static public-boundary gate for Engineering Diagnostics Wave 2P-A."""

from __future__ import annotations

import ast
from pathlib import Path

__all__ = ["validate_engineering_diagnostics_wave2pa_public_boundary"]

_PATHS = (
    "kanda_reasoner_app/engineering_diagnostics/__init__.py",
    "kanda_reasoner_app/engineering_diagnostics/enrichment.py",
    "kanda_reasoner_app/engineering_diagnostics/enrichment_models.py",
    "kanda_reasoner_app/engineering_diagnostics/frozen_path_enrichment.py",
    "kanda_reasoner_app/engineering_diagnostics/scope_enrichment.py",
    "kanda_reasoner_app/engineering_diagnostics_gui/controller.py",
    "kanda_reasoner_app/engineering_diagnostics_gui/diagnostic_table_model.py",
    "kanda_reasoner_app/engineering_diagnostics_gui/engineering_diagnostics_tab.py",
    "kanda_reasoner_app/engineering_diagnostics_gui/models.py",
    "tests/test_engineering_diagnostics_wave2pa.py",
    "tools/engineering_diagnostics_wave2pa_architecture_gate.py",
    "tools/engineering_diagnostics_wave2pa_public_boundary_gate.py",
    "tools/validate_engineering_diagnostics_wave2pa_v1.py",
)
_RUNTIME_PATHS = _PATHS[:9]


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def _imports(path: Path) -> tuple[str, ...]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    found: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            found.extend(alias.name for alias in node.names)
        if isinstance(node, ast.ImportFrom):
            found.append(str(node.module or ""))
    return tuple(found)


def validate_engineering_diagnostics_wave2pa_public_boundary(root: Path) -> None:
    """Reject private Box reach-ins, writes, or duplicate persistence ownership."""
    sources: dict[str, str] = {}
    for relative in _PATHS:
        path = root / relative
        _require(path.is_file(), "WAVE2PA_FILE_MISSING:" + relative)
        text = path.read_text(encoding="utf-8")
        _require(len(text.splitlines()) <= 500, "WAVE2PA_MODULE_TOO_LARGE:" + relative)
        text.encode("ascii")
        sources[relative] = text

    scope_path = root / (
        "kanda_reasoner_app/engineering_diagnostics/scope_enrichment.py"
    )
    freeze_path = root / (
        "kanda_reasoner_app/engineering_diagnostics/frozen_path_enrichment.py"
    )
    scope_imports = _imports(scope_path)
    freeze_imports = _imports(freeze_path)
    _require(
        "kanda_reasoner_app.project_exclusion_policy" in scope_imports,
        "WAVE2PA_PROJECT_EXCLUSION_PUBLIC_CONTRACT_MISSING",
    )
    _require(
        "kanda_reasoner_app.project_exclusion_path_matching" in scope_imports,
        "WAVE2PA_PROJECT_PATH_MATCHING_PUBLIC_CONTRACT_MISSING",
    )
    _require(
        "kanda_reasoner_app.freeze_after_update" in freeze_imports,
        "WAVE2PA_FREEZE_PUBLIC_CONTRACT_MISSING",
    )
    forbidden_import_tokens = (
        "source_hygiene._active_scope",
        "freeze_after_update.freeze_state",
        "freeze_after_update.paths",
        "project_freeze_ledger",
        "reasoner_symbol_atlas._",
    )
    all_imports = scope_imports + freeze_imports
    _require(
        not any(
            token in imported
            for imported in all_imports
            for token in forbidden_import_tokens
        ),
        "WAVE2PA_PRIVATE_BOX_IMPORT",
    )

    runtime = "\n".join(sources[relative] for relative in _RUNTIME_PATHS)
    lowered = runtime.lower()
    _require("sqlite3" not in lowered, "WAVE2PA_DIRECT_SQLITE_ACCESS")
    _require("project_freeze_ledger" not in runtime, "WAVE2PA_PROJECT_FREEZE_LEDGER_REACH_IN")
    _require("reasoner_symbol_atlas" not in runtime, "WAVE2PA_OWNER_ENRICHMENT_PREMATURE")
    write_tokens = (
        ".write_text(",
        ".write_bytes(",
        ".mkdir(",
        ".unlink(",
        "shutil.copy",
        "os.replace",
    )
    freeze_source = sources[
        "kanda_reasoner_app/engineering_diagnostics/frozen_path_enrichment.py"
    ]
    _require(
        not any(token in freeze_source for token in write_tokens),
        "WAVE2PA_FREEZE_MEMORY_WRITE_SURFACE",
    )
    scope_source = sources[
        "kanda_reasoner_app/engineering_diagnostics/scope_enrichment.py"
    ]
    _require(
        not any(token in scope_source for token in write_tokens),
        "WAVE2PA_SCOPE_SOURCE_WRITE_SURFACE",
    )
    _require("os.scandir" in scope_source, "WAVE2PA_SCOPE_DIRECTORY_CACHE_MISSING")
    _require("_directory_names" in scope_source, "WAVE2PA_SCOPE_DIRECTORY_INDEX_MISSING")
    _require("_marker_cache" in scope_source, "WAVE2PA_SCOPE_MARKER_CACHE_MISSING")
    _require("_parent_excluded_cache" in scope_source, "WAVE2PA_PARENT_POLICY_CACHE_MISSING")
    _require("_excluded_relative_file" in scope_source, "WAVE2PA_RELATIVE_POLICY_MATCHER_MISSING")
    _require(
        "should_exclude_reasoner_project_path" not in scope_source,
        "WAVE2PA_PER_FINDING_POLICY_RESOLVE_PRESENT",
    )
    _require("path.is_file()" not in scope_source, "WAVE2PA_PER_FINDING_FILE_PROBE_PRESENT")

    facade = sources["kanda_reasoner_app/engineering_diagnostics/__init__.py"]
    for symbol in (
        "EngineeringDiagnosticsEnricher",
        "DiagnosticFindingEnrichment",
        "DiagnosticScopeEnrichment",
        "DiagnosticFrozenPathEnrichment",
    ):
        _require(symbol in facade, "WAVE2PA_PUBLIC_FACADE_MISSING:" + symbol)
    controller = sources[
        "kanda_reasoner_app/engineering_diagnostics_gui/controller.py"
    ]
    _require("EngineeringDiagnosticsEnricher" in controller, "WAVE2PA_GUI_ENRICHER_MISSING")
    _require("EngineeringDiagnosticsStore" in controller, "WAVE2PA_STORE_OWNER_NOT_REUSED")
    tab = sources[
        "kanda_reasoner_app/engineering_diagnostics_gui/engineering_diagnostics_tab.py"
    ]
    _require("scope_combo" in tab, "WAVE2PA_SCOPE_FILTER_MISSING")
    _require("frozen_combo" in tab, "WAVE2PA_FROZEN_FILTER_MISSING")
    table = sources[
        "kanda_reasoner_app/engineering_diagnostics_gui/diagnostic_table_model.py"
    ]
    _require("QSortFilterProxyModel" not in table, "WAVE2PA_PROXY_MODEL_REGRESSION")
    _require("filterAcceptsRow" not in table, "WAVE2PA_PYTHON_FILTER_CALLBACK_REGRESSION")

    print("WAVE2PA MODULE SIZE MAXIMUM 500: PASS")
    print("WAVE2PA ASCII SOURCE CONTRACT: PASS")
    print("WAVE2PA PROJECT EXCLUSION PUBLIC CONTRACT: PASS")
    print("WAVE2PA FREEZE INDEX PUBLIC CONTRACT: PASS")
    print("WAVE2PA SOURCE HYGIENE PRIVATE IMPORTS: 0")
    print("WAVE2PA FREEZE PRIVATE IMPORTS: 0")
    print("WAVE2PA SYMBOL ATLAS IMPORTS: 0")
    print("WAVE2PA DIRECT SQLITE ACCESS: 0")
    print("WAVE2PA FREEZE MEMORY WRITE SURFACES: 0")
    print("WAVE2PA PROJECT SOURCE MUTATION SURFACES: 0")
    print("WAVE2PA SCOPE MARKER DIRECTORY CACHE: PASS")
    print("WAVE2PA RELATIVE EXCLUSION POLICY FAST PATH: PASS")
    print("WAVE2PA ENGINEERING DIAGNOSTICS PUBLIC FACADE: PASS")
    print("WAVE2PA GUI PUBLIC BACKEND CONTRACT: PASS")
    print("WAVE2PA GUI DIRECT INDEXED MODEL PRESERVED: PASS")
    print("WAVE2PA PUBLIC-CONTRACT-ONLY COMMUNICATION: PASS")
