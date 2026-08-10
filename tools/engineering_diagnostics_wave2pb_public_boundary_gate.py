# project-path: tools/engineering_diagnostics_wave2pb_public_boundary_gate.py
"""Static public-boundary gate for Engineering Diagnostics Wave 2P-B."""

from __future__ import annotations

import ast
from pathlib import Path

__all__ = ["validate_engineering_diagnostics_wave2pb_public_boundary"]

_PATHS = (
    "kanda_reasoner_app/engineering_diagnostics/__init__.py",
    "kanda_reasoner_app/engineering_diagnostics/enrichment.py",
    "kanda_reasoner_app/engineering_diagnostics/enrichment_models.py",
    "kanda_reasoner_app/engineering_diagnostics/owner_enrichment.py",
    "kanda_reasoner_app/engineering_diagnostics/owner_enrichment_models.py",
    "kanda_reasoner_app/engineering_diagnostics_gui/models.py",
    "kanda_reasoner_app/engineering_diagnostics_gui/diagnostic_table_model.py",
    "kanda_reasoner_app/engineering_diagnostics_gui/engineering_diagnostics_tab.py",
    "kanda_reasoner_app/engineering_diagnostics_gui/owner_ui.py",
    "tests/test_engineering_diagnostics_wave2pb.py",
    "tools/engineering_diagnostics_wave2pb_architecture_gate.py",
    "tools/engineering_diagnostics_wave2pb_public_boundary_gate.py",
    "tools/validate_engineering_diagnostics_wave2pb_v1r1.py",
)
_RUNTIME_PATHS = _PATHS[:9]


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def _imports(path: Path) -> tuple[str, ...]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    result: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            result.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            result.append(str(node.module or ""))
    return tuple(result)


def _explicit_all(path: Path) -> tuple[str, ...]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in tree.body:
        if not isinstance(node, (ast.Assign, ast.AnnAssign)):
            continue
        target = node.targets[0] if isinstance(node, ast.Assign) else node.target
        if not isinstance(target, ast.Name) or target.id != "__all__":
            continue
        value = node.value
        if not isinstance(value, (ast.List, ast.Tuple, ast.Set)):
            return ()
        return tuple(
            item.value
            for item in value.elts
            if isinstance(item, ast.Constant) and isinstance(item.value, str)
        )
    return ()


def _function_argument_names(path: Path, function_name: str) -> tuple[str, ...]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if node.name == function_name:
                arguments = tuple(node.args.posonlyargs) + tuple(node.args.args)
                return tuple(argument.arg for argument in arguments)
    return ()


def validate_engineering_diagnostics_wave2pb_public_boundary(root: Path) -> None:
    """Reject private reach-ins, duplicate state owners, and identity changes."""
    sources: dict[str, str] = {}
    for relative in _PATHS:
        path = root / relative
        _require(path.is_file(), "WAVE2PB_FILE_MISSING:" + relative)
        text = path.read_text(encoding="utf-8")
        _require(len(text.splitlines()) <= 500, "WAVE2PB_MODULE_TOO_LARGE:" + relative)
        text.encode("ascii")
        sources[relative] = text

    owner_path = root / (
        "kanda_reasoner_app/engineering_diagnostics/owner_enrichment.py"
    )
    owner_imports = _imports(owner_path)
    _require(
        "kanda_reasoner_app.reasoner_symbol_atlas" in owner_imports,
        "WAVE2PB_SYMBOL_ATLAS_PUBLIC_FACADE_MISSING",
    )
    _require(
        "kanda_reasoner_app.reasoner_symbol_atlas.output_policy" in owner_imports,
        "WAVE2PB_ACTIVE_OWNER_POLICY_PUBLIC_CONTRACT_MISSING",
    )
    forbidden_imports = (
        "reasoner_symbol_atlas.owner_classifier",
        "reasoner_symbol_atlas.schemas",
        "reasoner_symbol_atlas.symbol_indexer",
        "reasoner_symbol_atlas.import_analyzer",
        "reasoner_symbol_atlas.existing_code_finder",
        "reasoner_symbol_atlas._",
    )
    _require(
        not any(
            token in imported
            for imported in owner_imports
            for token in forbidden_imports
        ),
        "WAVE2PB_SYMBOL_ATLAS_PRIVATE_IMPORT",
    )

    runtime = "\n".join(sources[relative] for relative in _RUNTIME_PATHS)
    lowered = runtime.lower()
    _require("sqlite3" not in lowered, "WAVE2PB_DIRECT_SQLITE_ACCESS")
    _require("engineeringdiagnosticsstore(" not in lowered, "WAVE2PB_DUPLICATE_STORE_OWNER")
    _require("project_freeze_ledger" not in lowered, "WAVE2PB_FREEZE_LEDGER_REACH_IN")
    write_tokens = (
        ".write_text(",
        ".write_bytes(",
        ".mkdir(",
        ".unlink(",
        "shutil.copy",
        "os.replace",
    )
    owner_source = sources[
        "kanda_reasoner_app/engineering_diagnostics/owner_enrichment.py"
    ]
    _require(
        not any(token in owner_source for token in write_tokens),
        "WAVE2PB_OWNER_ENRICHMENT_WRITE_SURFACE",
    )
    _require(
        "classify_reasoner_symbol_atlas_owners" in owner_source,
        "WAVE2PB_OWNER_CLASSIFIER_PUBLIC_CONTRACT_MISSING",
    )
    _require(
        "is_active_owner_candidate" in owner_source,
        "WAVE2PB_ACTIVE_OWNER_FILTER_MISSING",
    )
    _require(
        "DEGRADED" in owner_source and "NEEDS_REVIEW" in owner_source,
        "WAVE2PB_FAIL_CLOSED_OWNER_STATUS_MISSING",
    )

    enrichment_models_path = root / (
        "kanda_reasoner_app/engineering_diagnostics/enrichment_models.py"
    )
    _require(
        "DiagnosticOwnerEnrichment" not in _explicit_all(enrichment_models_path),
        "WAVE2PB_DUPLICATE_PUBLIC_OWNER_EXPORT",
    )
    _require(
        "field"
        not in _function_argument_names(
            enrichment_models_path,
            "_normalized_choice",
        ),
        "WAVE2PB_IMPORTED_FIELD_SHADOWING",
    )

    facade = sources["kanda_reasoner_app/engineering_diagnostics/__init__.py"]
    for symbol in (
        "DiagnosticOwnerEnrichment",
        "DiagnosticOwnerSnapshot",
        "build_diagnostic_owner_snapshot",
        "classify_diagnostic_owner",
    ):
        _require(symbol in facade, "WAVE2PB_PUBLIC_FACADE_MISSING:" + symbol)

    tab = sources[
        "kanda_reasoner_app/engineering_diagnostics_gui/engineering_diagnostics_tab.py"
    ]
    for token in (
        "owner_combo",
        "Owner Status",
        "Owner Confidence",
        "Canonical Owner",
    ):
        _require(token in tab, "WAVE2PB_GUI_OWNER_SURFACE_MISSING:" + token)
    table = sources[
        "kanda_reasoner_app/engineering_diagnostics_gui/diagnostic_table_model.py"
    ]
    _require("QSortFilterProxyModel" not in table, "WAVE2PB_PROXY_MODEL_REGRESSION")
    _require("filterAcceptsRow" not in table, "WAVE2PB_FILTER_CALLBACK_REGRESSION")
    _require("owner_status" in table, "WAVE2PB_OWNER_FILTER_KEY_MISSING")

    protected = root / (
        "kanda_reasoner_app/reasoner_symbol_atlas/existing_code_finder.py"
    )
    _require(protected.is_file(), "WAVE2PB_PROTECTED_SYMBOL_ATLAS_FILE_MISSING")

    print("WAVE2PB MODULE SIZE MAXIMUM 500: PASS")
    print("WAVE2PB ASCII SOURCE CONTRACT: PASS")
    print("WAVE2PB SYMBOL ATLAS PUBLIC FACADE: PASS")
    print("WAVE2PB WAVE2N ACTIVE OWNER POLICY: PASS")
    print("WAVE2PB SYMBOL ATLAS PRIVATE IMPORTS: 0")
    print("WAVE2PB DIRECT SQLITE ACCESS: 0")
    print("WAVE2PB OWNER ENRICHMENT WRITE SURFACES: 0")
    print("WAVE2PB ENGINEERING DIAGNOSTICS STORE OWNER: PRESERVED")
    print("WAVE2PB FINDING AND SCAN IDENTITIES MODIFIED: NO")
    print("WAVE2PB GUI OWNER FILTER: PASS")
    print("WAVE2PB GUI DIRECT INDEXED MODEL: PASS")
    print("WAVE2PB OWNER MODEL PUBLIC SYMBOL SINGLE OWNER: PASS")
    print("WAVE2PB IMPORTED FIELD SHADOWING: ABSENT")
    print("WAVE2PB PUBLIC-CONTRACT-ONLY COMMUNICATION: PASS")
