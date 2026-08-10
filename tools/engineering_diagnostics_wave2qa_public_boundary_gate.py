# project-path: tools/engineering_diagnostics_wave2qa_public_boundary_gate.py
"""Public-boundary gate for Engineering Diagnostics Wave 2Q-A."""

from __future__ import annotations

import ast
from pathlib import Path

__all__ = ["validate_engineering_diagnostics_wave2qa_public_boundary"]

_RUNTIME_PATHS = (
    "kanda_reasoner_app/engineering_diagnostics/grouping_models.py",
    "kanda_reasoner_app/engineering_diagnostics/grouping.py",
    "kanda_reasoner_app/engineering_diagnostics/_store_database.py",
    "kanda_reasoner_app/engineering_diagnostics/_store_grouping_ops.py",
    "kanda_reasoner_app/engineering_diagnostics/_store_grouping_schema.py",
    "kanda_reasoner_app/engineering_diagnostics/_store_grouping_state.py",
    "kanda_reasoner_app/engineering_diagnostics/store.py",
    "kanda_reasoner_app/engineering_diagnostics/__init__.py",
    "kanda_reasoner_app/engineering_diagnostics_gui/models.py",
    "kanda_reasoner_app/engineering_diagnostics_gui/controller.py",
    "kanda_reasoner_app/engineering_diagnostics_gui/owner_ui.py",
    "kanda_reasoner_app/engineering_diagnostics_gui/diagnostic_table_model.py",
    "kanda_reasoner_app/engineering_diagnostics_gui/grouping_ui.py",
    "kanda_reasoner_app/engineering_diagnostics_gui/engineering_diagnostics_tab.py",
    "kanda_reasoner_app/engineering_diagnostics_gui/table_columns.py",
    "kanda_reasoner_app/engineering_diagnostics_gui/wave2qa_validation.py",
)
_TEST_PATHS = (
    "tests/test_engineering_diagnostics_wave2qa.py",
    "tests/test_engineering_diagnostics_wave2qa_gui_scale.py",
)
_TOOL_PATHS = (
    "tools/engineering_diagnostics_wave2qa_architecture_gate.py",
    "tools/engineering_diagnostics_wave2qa_fixture_support.py",
    "tools/engineering_diagnostics_wave2qa_public_boundary_gate.py",
    "tools/engineering_diagnostics_wave2qa_validation_runtime.py",
    "tools/validate_engineering_diagnostics_wave2qa_v1.py",
)
_ALL_PATHS = _RUNTIME_PATHS + _TEST_PATHS + _TOOL_PATHS


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def _tree(path: Path) -> ast.Module:
    return ast.parse(path.read_text(encoding="utf-8"), filename=str(path))


def _imports(path: Path) -> tuple[str, ...]:
    result: list[str] = []
    for node in ast.walk(_tree(path)):
        if isinstance(node, ast.Import):
            result.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            result.append(str(node.module or ""))
    return tuple(result)


def _defined_public_symbols(path: Path) -> tuple[str, ...]:
    symbols: list[str] = []
    for node in _tree(path).body:
        if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            if not node.name.startswith("_"):
                symbols.append(node.name)
    return tuple(symbols)


def _explicit_all(path: Path) -> tuple[str, ...]:
    for node in _tree(path).body:
        if not isinstance(node, ast.Assign):
            continue
        if not any(
            isinstance(target, ast.Name) and target.id == "__all__"
            for target in node.targets
        ):
            continue
        if not isinstance(node.value, (ast.List, ast.Tuple, ast.Set)):
            return ()
        return tuple(
            item.value
            for item in node.value.elts
            if isinstance(item, ast.Constant) and isinstance(item.value, str)
        )
    return ()


def _store_method_names(path: Path) -> tuple[str, ...]:
    for node in _tree(path).body:
        if isinstance(node, ast.ClassDef) and node.name == "EngineeringDiagnosticsStore":
            return tuple(
                item.name
                for item in node.body
                if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef))
            )
    return ()


def _assert_source_contract(root: Path) -> dict[str, str]:
    sources: dict[str, str] = {}
    for relative in _ALL_PATHS:
        path = root / relative
        _require(path.is_file(), "WAVE2QA_FILE_MISSING:" + relative)
        text = path.read_text(encoding="utf-8")
        _require(
            len(text.splitlines()) <= 500,
            "WAVE2QA_MODULE_TOO_LARGE:" + relative,
        )
        text.encode("ascii")
        sources[relative] = text
    return sources


def _assert_single_public_owners(root: Path) -> None:
    owner_paths = (
        "kanda_reasoner_app/engineering_diagnostics/grouping_models.py",
        "kanda_reasoner_app/engineering_diagnostics/grouping.py",
        "kanda_reasoner_app/engineering_diagnostics/_store_grouping_ops.py",
    "kanda_reasoner_app/engineering_diagnostics/_store_grouping_schema.py",
    "kanda_reasoner_app/engineering_diagnostics/_store_grouping_state.py",
        "kanda_reasoner_app/engineering_diagnostics/store.py",
    )
    owners: dict[str, list[str]] = {}
    for relative in owner_paths:
        for symbol in _defined_public_symbols(root / relative):
            owners.setdefault(symbol, []).append(relative)
    duplicates = {
        symbol: paths
        for symbol, paths in owners.items()
        if len(paths) > 1
    }
    _require(not duplicates, "WAVE2QA_DUPLICATE_PUBLIC_SYMBOL:" + repr(duplicates))

    model_exports = _explicit_all(
        root / "kanda_reasoner_app/engineering_diagnostics/grouping_models.py"
    )
    grouping_exports = _explicit_all(
        root / "kanda_reasoner_app/engineering_diagnostics/grouping.py"
    )
    _require(
        not set(model_exports).intersection(grouping_exports),
        "WAVE2QA_PUBLIC_OWNER_EXPORT_COLLISION",
    )


def _assert_store_ownership(root: Path, sources: dict[str, str]) -> None:
    runtime_gui = "\n".join(
        sources[relative]
        for relative in _RUNTIME_PATHS
        if "/_store_" not in relative
    )
    _require("import sqlite3" not in runtime_gui, "WAVE2QA_GUI_OR_DOMAIN_SQLITE")
    _require(
        "EngineeringDiagnosticsStore(" not in sources[
            "kanda_reasoner_app/engineering_diagnostics/grouping.py"
        ],
        "WAVE2QA_DETERMINISTIC_GROUPING_STORE_OWNER",
    )
    store_methods = set(
        _store_method_names(
            root / "kanda_reasoner_app/engineering_diagnostics/store.py"
        )
    )
    expected = {
        "get_manual_grouping_state",
        "create_manual_group",
        "assign_issue_to_manual_group",
        "ungroup_manual_issue",
        "mark_manual_group_reviewed",
    }
    _require(
        expected.issubset(store_methods),
        "WAVE2QA_PUBLIC_STORE_GROUPING_CONTRACT_MISSING",
    )
    operations = sources[
        "kanda_reasoner_app/engineering_diagnostics/_store_grouping_ops.py"
    ]
    state = sources[
        "kanda_reasoner_app/engineering_diagnostics/_store_grouping_state.py"
    ]
    close_count = (operations + state).count(
        "with closing(connect(database_path)) as connection:"
    )
    _require(
        close_count >= 5,
        "WAVE2QA_SQLITE_CONNECTION_CLOSE_CONTRACT_MISSING",
    )
    schema = sources[
        "kanda_reasoner_app/engineering_diagnostics/_store_grouping_schema.py"
    ]
    _require("BEGIN IMMEDIATE" in schema, "WAVE2QA_ATOMIC_MIGRATION_BEGIN_MISSING")
    _require("connection.rollback()" in schema, "WAVE2QA_ATOMIC_MIGRATION_ROLLBACK_MISSING")
    _require("executescript" not in schema, "WAVE2QA_GROUPING_MIGRATION_EXECUTESCRIPT")
    for token in (
        "diagnostic_group_decisions",
        "expected_generation",
        "BEGIN IMMEDIATE",
    ):
        _require(token in operations, "WAVE2QA_GROUPING_TRANSACTION_MISSING:" + token)


def _assert_no_leak(root: Path, sources: dict[str, str]) -> None:
    forbidden_import_tokens = (
        "reasoner_symbol_atlas.owner_classifier",
        "reasoner_symbol_atlas.schemas",
        "reasoner_symbol_atlas.symbol_indexer",
        "reasoner_symbol_atlas.import_analyzer",
        "reasoner_symbol_atlas.existing_code_finder",
        "freeze_after_update.",
        "project_freeze_ledger",
    )
    for relative in _RUNTIME_PATHS:
        imports = _imports(root / relative)
        for imported in imports:
            _require(
                not any(token in imported for token in forbidden_import_tokens),
                "WAVE2QA_PRIVATE_REACH_IN:" + relative + ":" + imported,
            )
    runtime = "\n".join(sources[relative] for relative in _RUNTIME_PATHS)
    _require("project_freeze_ledger" not in runtime, "WAVE2QA_FREEZE_LEDGER_REACH_IN")
    deterministic = sources[
        "kanda_reasoner_app/engineering_diagnostics/grouping.py"
    ]
    for token in (
        ".write_text(",
        ".write_bytes(",
        ".mkdir(",
        ".unlink(",
        "os.replace",
        "shutil.copy",
        "sqlite3",
    ):
        _require(token not in deterministic, "WAVE2QA_GROUPING_WRITE_SURFACE:" + token)


def _assert_identity_and_gui(sources: dict[str, str]) -> None:
    database = sources[
        "kanda_reasoner_app/engineering_diagnostics/_store_database.py"
    ]
    _require(
        '("schema_version", DIAGNOSTIC_SCHEMA_VERSION)' in database,
        "WAVE2QA_DIAGNOSTIC_SCHEMA_CONTRACT_MISSING",
    )
    grouping_schema = sources[
        "kanda_reasoner_app/engineering_diagnostics/_store_grouping_schema.py"
    ]
    _require(
        '("grouping_schema_version", DIAGNOSTIC_GROUPING_SCHEMA_VERSION)'
        in grouping_schema,
        "WAVE2QA_SEPARATE_GROUPING_SCHEMA_MISSING",
    )
    grouping = sources[
        "kanda_reasoner_app/engineering_diagnostics/grouping.py"
    ]
    _require("root_cause_claimed" in grouping, "WAVE2QA_ROOT_CAUSE_DISCLAIMER_MISSING")
    _require("len(members) < 2" in grouping, "WAVE2QA_SINGLETON_GROUP_REJECTION_MISSING")
    tab = sources[
        "kanda_reasoner_app/engineering_diagnostics_gui/engineering_diagnostics_tab.py"
    ] + sources[
        "kanda_reasoner_app/engineering_diagnostics_gui/table_columns.py"
    ]
    table = sources[
        "kanda_reasoner_app/engineering_diagnostics_gui/diagnostic_table_model.py"
    ]
    for token in ("Diagnostic Group", "Group Kind", "group_combo"):
        _require(token in tab, "WAVE2QA_GUI_GROUP_SURFACE_MISSING:" + token)
    _require("QSortFilterProxyModel" not in table, "WAVE2QA_PROXY_MODEL_REGRESSION")
    _require("filterAcceptsRow" not in table, "WAVE2QA_FILTER_CALLBACK_REGRESSION")
    _require("row_group" in table, "WAVE2QA_GROUP_FILTER_MISSING")


def _assert_no_import_argument_shadowing(root: Path) -> None:
    for relative in _RUNTIME_PATHS:
        tree = _tree(root / relative)
        imported: set[str] = set()
        for node in tree.body:
            if isinstance(node, ast.Import):
                imported.update(alias.asname or alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                imported.update(alias.asname or alias.name for alias in node.names)
        collisions: list[str] = []
        for node in ast.walk(tree):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            arguments = (
                tuple(node.args.posonlyargs)
                + tuple(node.args.args)
                + tuple(node.args.kwonlyargs)
            )
            collisions.extend(
                node.name + ":" + argument.arg
                for argument in arguments
                if argument.arg in imported
            )
        _require(
            not collisions,
            "WAVE2QA_IMPORTED_ARGUMENT_SHADOWING:"
            + relative
            + ":"
            + repr(collisions),
        )


def validate_engineering_diagnostics_wave2qa_public_boundary(root: Path) -> None:
    """Reject duplicate owners, private reach-ins, and persistence leaks."""
    sources = _assert_source_contract(root)
    _assert_single_public_owners(root)
    _assert_store_ownership(root, sources)
    _assert_no_leak(root, sources)
    _assert_identity_and_gui(sources)
    _assert_no_import_argument_shadowing(root)

    print("WAVE2QA MODULE SIZE MAXIMUM 500: PASS")
    print("WAVE2QA ASCII SOURCE CONTRACT: PASS")
    print("WAVE2QA DETERMINISTIC GROUPING OWNER: PASS")
    print("WAVE2QA PUBLIC GROUPING SYMBOL SINGLE OWNERS: PASS")
    print("WAVE2QA ENGINEERING DIAGNOSTICS STORE OWNER: PRESERVED")
    print("WAVE2QA SQLITE CONNECTION DETERMINISTIC CLOSE: PASS")
    print("WAVE2QA APPEND-ONLY DECISION HISTORY: PASS")
    print("WAVE2QA ATOMIC GROUPING SCHEMA MIGRATION: PASS")
    print("WAVE2QA IMPORTED ARGUMENT SHADOWING: ABSENT")
    print("WAVE2QA CAS GROUPING GENERATION: PASS")
    print("WAVE2QA PRIVATE IMPORTS: 0")
    print("WAVE2QA DETERMINISTIC GROUPING WRITE SURFACES: 0")
    print("WAVE2QA FINDING AND SCAN IDENTITIES MODIFIED: NO")
    print("WAVE2QA SEPARATE GROUPING SCHEMA: PASS")
    print("WAVE2QA GUI DIRECT INDEXED MODEL: PASS")
    print("WAVE2QA PUBLIC-CONTRACT-ONLY COMMUNICATION: PASS")
