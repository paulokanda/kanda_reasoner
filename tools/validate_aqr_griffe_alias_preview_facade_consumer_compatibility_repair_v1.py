# project-path: tools/validate_aqr_griffe_alias_preview_facade_consumer_compatibility_repair_v1.py
"""Validate Griffe alias policy and Preview facade consumer compatibility."""
from __future__ import annotations

import ast
import json
from pathlib import Path
import sys
from types import SimpleNamespace
from tempfile import TemporaryDirectory

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT_TEXT = str(PROJECT_ROOT)
if PROJECT_ROOT_TEXT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT_TEXT)

from kanda_reasoner_app.manage_architecture.large_file_refactor_planner import (
    griffe_api_fitness_adapter as griffe,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.advanced_quality_evidence_models import (
    FindingSeverity,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.advanced_quality_review_contract import (
    AnalysisExecutionStatus,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.cst_preview_rendering import (
    render_preview_facade,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.facade_consumer_compatibility import (
    build_facade_consumer_compatibility_report,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.griffe_public_surface import (
    child_public_override,
    griffe_public_state,
)

FEATURE_ID = "aqr-griffe-alias-preview-facade-consumer-compatibility-repair-v1"


def main() -> int:
    _validate_griffe_alias_policy()
    _validate_consumer_compatibility()
    _validate_current_routing_signal_scorer_contract()
    _validate_module_size_policy()
    print("AQR_GRIFFE_ALIAS_PREVIEW_FACADE_CONSUMER_COMPATIBILITY_REPAIR: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


def _validate_griffe_alias_policy() -> None:
    parent_without_exports = {"kind": "module"}
    assert child_public_override(parent_without_exports, "ImportedAlias") is None
    assert griffe_public_state({"kind": "alias"}, "ImportedAlias") is False
    assert griffe_public_state({"kind": "function"}, "public_function") is True
    assert griffe_public_state({"kind": "function"}, "_private_function") is False
    print("GRIFFE_NO_ALL_IMPORTED_ALIAS_DEFAULTS_NON_PUBLIC: PASS")

    parent_with_exports = {"exports": ["ExplicitAlias", "public_function"]}
    assert child_public_override(parent_with_exports, "ExplicitAlias") is True
    assert child_public_override(parent_with_exports, "ImportedAlias") is False
    assert griffe_public_state(
        {"kind": "alias"},
        "ExplicitAlias",
        explicit_export=True,
    ) is True
    print("GRIFFE_EXPLICIT_ALIAS_EXPORT_REMAINS_PUBLIC: PASS")

    payload = {
        "pkg": {
            "kind": "module",
            "name": "pkg",
            "members": {
                "mod": {
                    "kind": "module",
                    "name": "mod",
                    "members": {
                        "ImportedAlias": {
                            "kind": "alias",
                            "name": "ImportedAlias",
                            "target_path": "pkg.dep.ImportedAlias",
                        },
                        "public_function": {
                            "kind": "function",
                            "name": "public_function",
                            "parameters": [],
                            "returns": None,
                        },
                    },
                }
            },
        }
    }
    execution = SimpleNamespace(
        status=AnalysisExecutionStatus.SUCCEEDED,
        stdout_text=json.dumps(payload),
        engine_id="griffe_baseline",
    )
    diagnostics: list[str] = []
    model = griffe._parse_api_model(
        execution,
        package_name="pkg",
        diagnostics=diagnostics,
    )
    assert not diagnostics, diagnostics
    assert model["pkg.mod.ImportedAlias"].public is False
    assert model["pkg.mod.public_function"].public is True
    preview_model = {
        path: symbol
        for path, symbol in model.items()
        if path != "pkg.mod.public_function"
    }
    findings = griffe._compare_models(
        model,
        preview_model,
        engine_version="test",
        raw_bytes=b"{}",
        diagnostics=[],
    )
    blockers = {
        item.symbol_identity
        for item in findings
        if item.severity is FindingSeverity.BLOCKER
    }
    assert blockers == {"pkg.mod.public_function"}, blockers
    print("GRIFFE_REAL_PARSER_PATH_ALIAS_FALSE_BLOCK_REMOVED: PASS")
    print("GRIFFE_REAL_PUBLIC_FUNCTION_REMOVAL_STILL_BLOCKED: PASS")


def _validate_consumer_compatibility() -> None:
    with TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        package = root / "pkg"
        package.mkdir(parents=True)
        (package / "__init__.py").write_text("", encoding="utf-8")
        target = package / "mod.py"
        target.write_text(
            "def public_function():\n"
            "    return _used_helper()\n\n"
            "def _used_helper():\n"
            "    return 1\n\n"
            "def _unused_helper():\n"
            "    return 2\n",
            encoding="utf-8",
        )
        (package / "consumer.py").write_text(
            "from .mod import _used_helper\n",
            encoding="utf-8",
        )
        (package / "module_consumer.py").write_text(
            "from . import mod as runtime\n"
            "VALUE = runtime._used_helper()\n",
            encoding="utf-8",
        )

        report = build_facade_consumer_compatibility_report(
            active_project_root=root,
            target_file=target,
            moved_symbols={"_used_helper", "_unused_helper"},
        )
        assert report.status == "facade_consumer_compatibility_ready"
        assert report.blockers == ()
        assert report.imported_moved_symbols == ("_used_helper",)
        assert report.importer_files == (
            "pkg/consumer.py",
            "pkg/module_consumer.py",
        )
        print("FACADE_CONSUMER_IMPORT_SCAN_RELATIVE_AND_MODULE_ALIAS: PASS")

        plan = SimpleNamespace(
            public_api_after_expected=["public_function"],
            target_file=str(target),
            source_content_hash="a" * 64,
        )
        rendered = render_preview_facade(
            plan,
            "mod.py",
            [],
            [
                '"""Facade fixture."""',
                "def public_function():\n    return _used_helper()",
            ],
            {
                "_used_helper": "_mod_operations.py",
                "_unused_helper": "_mod_operations.py",
            },
            "fixture",
            compatibility_import_names=set(report.imported_moved_symbols),
        )
        namespace = _top_level_names(rendered)
        assert "_used_helper" in namespace
        assert "_unused_helper" not in namespace
        tree = ast.parse(rendered)
        all_values = _all_values(tree)
        assert all_values == ["public_function"], all_values
        print("PREVIEW_FACADE_PRESERVES_IMPORTED_MOVED_PRIVATE_SYMBOL: PASS")
        print("PREVIEW_FACADE_COMPATIBILITY_REEXPORT_NOT_PUBLIC_ALL: PASS")

        (package / "star_consumer.py").write_text(
            "from .mod import *\n",
            encoding="utf-8",
        )
        star_report = build_facade_consumer_compatibility_report(
            active_project_root=root,
            target_file=target,
            moved_symbols={"_used_helper", "_unused_helper"},
        )
        assert star_report.status == "blocked"
        assert any(
            item.startswith("FACADE_CONSUMER_STAR_IMPORT_REQUIRES_MANUAL_REVIEW:")
            for item in star_report.blockers
        )
        print("FACADE_CONSUMER_STAR_IMPORT_FAILS_CLOSED: PASS")


def _validate_current_routing_signal_scorer_contract() -> None:
    project_root = Path(__file__).resolve().parents[1]
    target = (
        project_root
        / "kanda_reasoner_app"
        / "routing_signal_scorer"
        / "similarity_runtime.py"
    )
    if not target.exists():
        raise AssertionError("CURRENT_ROUTING_SIGNAL_SCORER_TARGET_MISSING")
    expected = {
        "_containment",
        "_jaccard",
        "_similarity_advisory_only_reason",
        "_similarity_rule_hook_independence_reason",
        "_tokenize_for_similarity",
    }
    report = build_facade_consumer_compatibility_report(
        active_project_root=project_root,
        target_file=target,
        moved_symbols=expected,
    )
    assert not report.blockers, report.blockers
    assert expected <= set(report.imported_moved_symbols), report.imported_moved_symbols
    assert (
        "kanda_reasoner_app/routing_signal_scorer/contract.py"
        in report.importer_files
    )
    print("CURRENT_AQR_MYPY_FIVE_MISSING_FACADE_SYMBOLS_DISCOVERED: PASS")


def _validate_module_size_policy() -> None:
    project_root = Path(__file__).resolve().parents[1]
    planner = (
        project_root
        / "kanda_reasoner_app"
        / "manage_architecture"
        / "large_file_refactor_planner"
    )
    touched = [
        planner / "griffe_public_surface.py",
        planner / "facade_consumer_compatibility.py",
        planner / "cst_preview_rendering.py",
        planner / "cst_real_preview_writer.py",
    ]
    for path in touched:
        line_count = len(path.read_text(encoding="utf-8").splitlines())
        assert line_count <= 500, (path.name, line_count)
    print("TOUCHED_SOURCE_MODULES_MAX_500_LINES: PASS")


def _top_level_names(source: str) -> set[str]:
    names: set[str] = set()
    for node in ast.parse(source).body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            names.add(node.name)
        elif isinstance(node, ast.Import):
            names.update(alias.asname or alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            names.update(alias.asname or alias.name for alias in node.names)
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    names.add(target.id)
    return names


def _all_values(tree: ast.Module) -> list[str]:
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        if not any(
            isinstance(target, ast.Name) and target.id == "__all__"
            for target in node.targets
        ):
            continue
        if isinstance(node.value, (ast.List, ast.Tuple)):
            values: list[str] = []
            for item in node.value.elts:
                if isinstance(item, ast.Constant) and isinstance(item.value, str):
                    values.append(item.value)
            return values
    return []


if __name__ == "__main__":
    raise SystemExit(main())
