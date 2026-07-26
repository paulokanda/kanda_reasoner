# project-path: kanda_reasoner_app/refactor_report_evidence.py
"""Compact Refactor Report evidence for audit clipboard payloads."""

from __future__ import annotations

import ast
import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from kanda_reasoner_app.project_analysis_evidence_paths import (
    project_analysis_evidence_root,
)


@dataclass(frozen=True)
class RefactorReportEvidence:
    """Result from a headless Refactor Report evidence refresh."""

    summary: dict[str, Any]
    summary_text: str
    bundle_path: Path
    report_root: Path


def build_refactor_report_evidence_text(project_root: str | Path) -> str:
    """Run Refactor Report for ``project_root`` and return compact evidence text."""

    evidence = refresh_refactor_report_evidence(project_root)
    return evidence.summary_text


def refresh_refactor_report_evidence(project_root: str | Path) -> RefactorReportEvidence:
    """Force a fresh Refactor Report run and return a compact AI payload."""

    root = Path(project_root).expanduser().resolve()
    if not root.exists() or not root.is_dir():
        raise FileNotFoundError(f"Project root not found: {root}")

    from kanda_reasoner_app.daily_rfctr_report import daily_refactor_report as engine

    output_root = project_analysis_evidence_root(root)
    report_name = root.name.strip() or "project"
    bundle_path = (
        output_root
        / "daily_refactor"
        / f"{report_name}_daily_rfctr_report_bundle.json"
    )
    config = engine.build_config_named(
        root,
        output_root,
        report_name,
        ai_bundle_path=bundle_path,
    )
    config["source_mode"] = "scan_only"

    lock_created = False
    try:
        engine.phase_lock(config)
        lock_created = True
        derived_data, was_skipped = engine.phase_extraction(config, root, force=True)
        analysis_outputs = engine.phase_analysis(
            config,
            root,
            derived_data,
            skipped_extraction=was_skipped,
        )
        state_vector = _build_scan_state_vector(root, engine)
        state_vector = engine.recompute_fields(state_vector)
        state_vector.update(analysis_outputs)
        engine.ensure_expected_derived_files(
            config,
            source_mode="scan_only",
            domain_root=root,
        )
        _write_current_state_without_history_dump(engine, config, state_vector)
        engine.phase_archive(config)
        engine.phase_ai_bundle(config)
    finally:
        if lock_created:
            engine.remove_lock(config["lock"])

    bundle = json.loads(bundle_path.read_text(encoding="utf-8"))
    summary = _compact_refactor_bundle(bundle)
    summary_text = _format_summary_text(summary, bundle_path)
    return RefactorReportEvidence(
        summary=summary,
        summary_text=summary_text,
        bundle_path=bundle_path,
        report_root=Path(config["root"]),
    )


def _write_current_state_without_history_dump(
    engine: Any,
    config: dict[str, Any],
    current_state: dict[str, Any],
) -> None:
    """Persist current/history files without opening Refactor Report diff UI."""

    history = engine.safe_load_with_recovery(config["history"], config["log"]) or []
    if not isinstance(history, list):
        history = []
    history.append(current_state)
    engine.write_atomic(config["current"], current_state)
    engine.write_atomic(config["history"], history)


def _build_scan_state_vector(project_root: Path, engine: Any) -> dict[str, Any]:
    """Build the canonical state vector from scannable Python files."""

    functions_added: list[str] = []
    classes_added: list[str] = []
    imports_added: list[str] = []
    files_modified: list[str] = []
    async_funcs: list[str] = []
    node_count = 0
    lines_added = 0
    try_blocks = 0
    broken_files: list[str] = []

    for path in engine._iter_scannable_python_files(project_root):
        if "__pycache__" in path.parts:
            continue
        rel_path = str(path.relative_to(project_root))
        try:
            source = path.read_text(encoding="utf-8", errors="replace")
            tree = ast.parse(source)
        except SyntaxError as exc:
            broken_files.append(f"{rel_path}: line {exc.lineno}: {exc.msg}")
            continue
        except Exception as exc:
            broken_files.append(f"{rel_path}: {exc}")
            continue

        files_modified.append(rel_path)
        lines_added += source.count("\n") + 1
        node_count += sum(1 for _ in ast.walk(tree))

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                functions_added.append(node.name)
            elif isinstance(node, ast.AsyncFunctionDef):
                functions_added.append(node.name)
                async_funcs.append(node.name)
            elif isinstance(node, ast.ClassDef):
                classes_added.append(node.name)
            elif isinstance(node, ast.Import):
                imports_added.extend(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imports_added.append(node.module)
            elif isinstance(node, ast.Try):
                try_blocks += 1

    functions_added = sorted(set(functions_added))
    classes_added = sorted(set(classes_added))
    imports_added = sorted(set(imports_added))
    async_funcs = sorted(set(async_funcs))

    summary = (
        f"Auto-generated Refactor Report from {len(files_modified)} healthy "
        f"Python file(s). Skipped {len(broken_files)} broken file(s)."
    )

    return {
        "state_vector_version": "2.0",
        "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "incremental": True,
        "structural_change": {
            "magnitude": min(len(files_modified), 20),
            "surface_area": len(files_modified),
            "acceleration": 1,
            "modules_touched": len(files_modified),
            "files_modified": files_modified,
            "functions_added": functions_added,
            "functions_modified": [],
            "functions_removed": [],
            "classes_added": classes_added,
            "classes_modified": [],
            "lines_added": lines_added,
            "lines_removed": 0,
        },
        "complexity_state": {
            "risk_level": "low" if len(files_modified) <= 3 else "medium",
            "volatility": 0.0,
            "stability_trajectory": "stable",
            "cyclomatic_complexity_delta": 0,
            "nesting_depth_max": 0,
            "coupling_degree": "low",
        },
        "governance_state": {
            "score": 100,
            "mode_impact": "none",
            "breaking_changes": False,
            "backward_compatible": True,
            "test_coverage_impact": "unknown",
        },
        "refactor_pressure": {
            "debt_index": 0,
            "hotspots": 0,
            "duplication_factor": 0.0,
            "refactor_inevitability_horizon": None,
            "technical_debt_notes": broken_files[:25],
        },
        "pattern_dynamics": {
            "dominant_patterns": [],
            "new_patterns": [],
            "deprecated_patterns": [],
            "design_patterns_detected": [],
            "anti_patterns_detected": [],
        },
        "forward_projection": {
            "expected_next_stress": "low",
            "regression_risk_probability": 0.0,
            "next_likely_hotspot": project_root.name,
            "suggested_next_action": "Use audit findings plus compact Refactor Report evidence.",
        },
        "architectural_snapshot": {
            "node_count": node_count,
            "layer_distribution": {
                "tab1": 0,
                "tab3": 0,
                "cortex": 0,
                "dev_tools": 0,
            },
            "dependencies_introduced": [],
            "dependencies_removed": [],
            "imports_added": imports_added,
            "constants_added": [],
            "global_state_mutations": [],
            "integration_points_touched": {
                "file_io": False,
                "network": False,
                "database": False,
                "subprocess": False,
                "env_access": False,
                "serialisation": False,
                "concurrency": False,
                "logging": False,
            },
            "localization_changes": {
                "strings_added": 0,
                "hardcoded_urls_added": [],
                "translation_calls_added": 0,
            },
            "side_effects_introduced": [],
            "exception_handling_changes": {
                "try_blocks_added": try_blocks,
                "new_exceptions_caught": [],
                "new_exceptions_raised": [],
            },
            "docstrings_added": len(functions_added) + len(classes_added),
            "type_hints_added": 0,
            "async_changes": {
                "async_functions_added": async_funcs,
                "async_functions_removed": [],
            },
            "summary_narrative": summary,
        },
    }


def _compact_refactor_bundle(bundle: dict[str, Any]) -> dict[str, Any]:
    """Return the fields worth sending with architecture/workflow audits."""

    current_state = _as_dict(bundle.get("current_state"))
    derived = _as_dict(bundle.get("derived"))
    metadata = _as_dict(bundle.get("metadata"))
    return {
        "metadata": _compact_value(
            {
                key: metadata.get(key)
                for key in (
                    "generated_at",
                    "engine_version",
                    "domain",
                    "bundle_type",
                    "source_mode",
                    "project_root",
                    "report_folder",
                    "bundle_path",
                    "integrity_hash",
                    "load_status",
                )
                if key in metadata
            }
        ),
        "project_snapshot": _compact_value(derived.get("project_snapshot")),
        "symbol_churn": _compact_value(derived.get("symbol_churn")),
        "dependency_graph": _compact_value(derived.get("dependency_graph")),
        "stability_analysis": _compact_value(derived.get("stability_analysis")),
        "refactor_pressure": _compact_value(current_state.get("refactor_pressure")),
    }


def _as_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _compact_value(value: Any, *, depth: int = 0, max_items: int = 25) -> Any:
    """Compact nested data while preserving counts and useful samples."""

    if depth >= 5:
        return _compact_scalar(value)
    if isinstance(value, dict):
        return {
            str(key): _compact_value(item, depth=depth + 1, max_items=max_items)
            for key, item in value.items()
        }
    if isinstance(value, list):
        sample = [
            _compact_value(item, depth=depth + 1, max_items=max_items)
            for item in value[:max_items]
        ]
        if len(value) <= max_items:
            return sample
        return {
            "count": len(value),
            "sample": sample,
            "omitted_count": len(value) - max_items,
        }
    return _compact_scalar(value)


def _compact_scalar(value: Any) -> Any:
    if isinstance(value, str) and len(value) > 600:
        return value[:600] + "... [truncated]"
    return value


def _format_summary_text(summary: dict[str, Any], bundle_path: Path) -> str:
    summary_json = json.dumps(summary, indent=2, sort_keys=True, ensure_ascii=True)
    return (
        "\n\n---\n"
        "Refactor Report Evidence (compact, auto-generated before copy)\n"
        f"Bundle path: {bundle_path}\n"
        "Full state_history is intentionally omitted. Included fields: "
        "metadata, project_snapshot, symbol_churn, dependency_graph, "
        "stability_analysis, refactor_pressure.\n\n"
        "```json\n"
        f"{summary_json}\n"
        "```\n"
    )
