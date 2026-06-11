"""
Daily AI Structural Awareness Engine - v12.3
============================================
Changes from v12.2:
  - Step 1 renamed from "Domain" to "File to Scan" — optional, not required.
  - Two-mode compile:
      MODE A (file selected): full 7-phase pipeline — extraction, analysis,
        validate state vector, persist, archive, AI bundle.
      MODE B (no file selected): paste-only — validates pasted JSON against
        canonical schema, recomputes auto-derived fields, saves only
        current_state.json + state_history.json. No extraction, no bundle.
  - Removed blocking error "Please select a domain folder" — compile now
    works without a file selection.
  - Force Re-extract button now shows a clear warning if no file is selected
    instead of silently failing.
  - All v12.2 logic preserved.

OUTPUT FILE LAYOUT
==================
Everything is written into one folder auto-created under the output folder
chosen in Step 2.  The bundle can be redirected to a separate path via the
"AI Bundle Path" field (Step 2b).

    <output_folder>/<prefix>_daily_refactor_engine/
    │
    ├── <prefix>_current_state.json                ← latest compiled state vector
    ├── <prefix>_state_history.json                ← rolling window of last 7 vectors
    ├── <prefix>_daily_refactor_report_bundle.json ← single file to give the AI
    │                                                 (may live elsewhere if overridden)
    ├── engine.lock                                ← temporary; deleted after each run
    ├── corruption_alert.log                       ← written only when a file fails to load
    │
    ├── derived/
    │   ├── project_snapshot.json        ← file count, line count, AST stats
    │   ├── symbol_index.json            ← every class/function/constant + location
    │   ├── symbol_index.previous.json   ← previous run's index (for churn diff)
    │   ├── symbol_churn.json            ← added/removed symbols since last run
    │   ├── dependency_graph.json        ← imports, cycles, SCCs
    │   ├── stability_analysis.json      ← Martin instability metrics, risk score
    │   └── domain_fingerprint.json      ← SHA-256 cache key (skip-logic)
    │
    └── archive/
        ├── current_state_YYYYMMDD_HHMMSS.json   ← timestamped snapshot per run
        └── ...                                   ← capped at 50 entries

WHY EACH FILE EXISTS
====================
  current_state.json      — read by phase_persistence() to compute the
                            structural diff dialog; also loaded by the
                            "Load Existing JSON" button.
  state_history.json      — source for the rolling 7-run window; read and
                            appended every compile.
  derived/*.json          — read by phase_extraction() skip-logic to decide
                            whether re-extraction is needed; also consumed
                            by phase_analysis() when cached.
  domain_fingerprint.json — the entire cache/skip system depends on this;
                            deleting it forces a full re-extraction on next run.
  archive/*.json          — human-readable history; not read by the engine.
  corruption_alert.log    — append-only diagnostic; zero cost when healthy.
  <prefix>_daily_refactor_report_bundle.json
                          — the single file to upload to the AI; contains
                            current_state, state_history, and all derived data
                            plus an integrity SHA-256 hash.
"""

from __future__ import annotations

import ast
import copy
import hashlib
import json
import os
import shutil
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QStatusBar,
    QTextEdit,
    QVBoxLayout,
    QWidget,
    QGroupBox,
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt


# ═════════════════════════════════════════════════════════════════════════════
# CONSTANTS
# ═════════════════════════════════════════════════════════════════════════════

LOCK_TIMEOUT_SECONDS = 300
ARCHIVE_RETENTION    = 50
ROLLING_WINDOW       = 7

CANONICAL_KEYS = {
    "state_vector_version",
    "timestamp",
    "incremental",
    "structural_change",
    "complexity_state",
    "governance_state",
    "refactor_pressure",
    "pattern_dynamics",
    "forward_projection",
    "architectural_snapshot",
}

# Required sub-keys per top-level object (enforcement rules)
CANONICAL_STRUCTURAL_CHANGE_KEYS = {
    "magnitude", "surface_area", "acceleration", "modules_touched",
    "files_modified", "functions_added", "functions_modified", "functions_removed",
    "classes_added", "classes_modified", "lines_added", "lines_removed",
}
CANONICAL_COMPLEXITY_KEYS = {
    "risk_level", "volatility", "stability_trajectory",
    "cyclomatic_complexity_delta", "nesting_depth_max", "coupling_degree",
}
CANONICAL_GOVERNANCE_KEYS = {
    "score", "mode_impact",
    "breaking_changes", "backward_compatible", "test_coverage_impact",
}
CANONICAL_REFACTOR_KEYS = {
    "debt_index", "hotspots", "duplication_factor",
    "refactor_inevitability_horizon", "technical_debt_notes",
}
CANONICAL_PATTERN_KEYS = {
    "dominant_patterns", "new_patterns", "deprecated_patterns",
    "design_patterns_detected", "anti_patterns_detected",
}
CANONICAL_PROJECTION_KEYS = {
    "expected_next_stress", "regression_risk_probability",
    "next_likely_hotspot", "suggested_next_action",
}
CANONICAL_SNAPSHOT_KEYS = {
    "node_count", "layer_distribution",
    "dependencies_introduced", "dependencies_removed",
    "imports_added", "constants_added", "global_state_mutations",
    "integration_points_touched", "localization_changes",
    "side_effects_introduced", "exception_handling_changes",
    "docstrings_added", "type_hints_added",
    "async_changes", "summary_narrative",
}
CANONICAL_INTEGRATION_KEYS = {
    "file_io", "network", "database", "subprocess",
    "env_access", "serialisation", "concurrency", "logging",
}
CANONICAL_ASYNC_KEYS       = {"async_functions_added", "async_functions_removed"}
CANONICAL_EXCEPTION_KEYS   = {"try_blocks_added", "new_exceptions_caught", "new_exceptions_raised"}
CANONICAL_LOCALIZATION_KEYS = {"strings_added", "hardcoded_urls_added", "translation_calls_added"}

_STDLIB: frozenset = frozenset(getattr(sys, "stdlib_module_names", set()))


# ═════════════════════════════════════════════════════════════════════════════
# ANALYSIS CONTRACTS  (was analysis_contracts.py)
# ═════════════════════════════════════════════════════════════════════════════

@dataclass(frozen=True)
class AnalysisInputs:
    snapshot:          Dict[str, Any]
    symbol_index:      Dict[str, Any]
    symbol_churn:      Dict[str, Any]
    dependency_graph:  Optional[Dict[str, Any]] = None
    governance_rules:  Optional[Dict[str, Any]] = None


@dataclass(frozen=True)
class AnalyzerResult:
    name:    str
    version: str
    result:  Dict[str, Any]


# ═════════════════════════════════════════════════════════════════════════════
# ATOMIC I/O & BACKUP UTILITIES
# ═════════════════════════════════════════════════════════════════════════════

def write_atomic(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, sort_keys=True)
    tmp.replace(path)


# ═════════════════════════════════════════════════════════════════════════════
# DOMAIN FINGERPRINT  (skip-logic for unchanged domains)
# ═════════════════════════════════════════════════════════════════════════════

def _compute_domain_fingerprint(domain_root: Path) -> str:
    """
    SHA-256 over the sorted list of (relative_path, file_size, mtime) for
    every .py file in the domain. Fast — no file reads needed.
    If any file is added, removed, resized, or touched, the fingerprint changes.
    """
    entries = []
    for fp in sorted(domain_root.rglob("*.py")):
        if "__pycache__" in fp.parts:
            continue
        try:
            st = fp.stat()
            entries.append(f"{fp.relative_to(domain_root)}|{st.st_size}|{st.st_mtime_ns}")
        except Exception:
            entries.append(str(fp.relative_to(domain_root)))
    digest = hashlib.sha256("\n".join(entries).encode("utf-8")).hexdigest()
    return digest


def _load_saved_fingerprint(fingerprint_path: Path) -> Optional[str]:
    if not fingerprint_path.exists():
        return None
    try:
        data = json.loads(fingerprint_path.read_text(encoding="utf-8"))
        return data.get("fingerprint")
    except Exception:
        return None


def _save_fingerprint(fingerprint_path: Path, fingerprint: str, domain_root: Path) -> None:
    write_atomic(fingerprint_path, {
        "fingerprint":  fingerprint,
        "domain_root":  str(domain_root),
        "saved_at":     datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
    })


def domain_is_unchanged(domain_root: Path, fingerprint_path: Path) -> Tuple[bool, str]:
    """
    Returns (unchanged: bool, current_fingerprint: str).
    unchanged=True  → skip extraction/analysis, reuse cached derived data.
    unchanged=False → run full extraction/analysis.
    """
    current = _compute_domain_fingerprint(domain_root)
    saved   = _load_saved_fingerprint(fingerprint_path)
    return (current == saved), current


def rotate_backups(path: Path) -> None:
    back1 = path.with_suffix(path.suffix + ".back1")
    back2 = path.with_suffix(path.suffix + ".back2")
    if back2.exists():
        back2.unlink()
    if back1.exists():
        back1.rename(back2)
    if path.exists():
        shutil.copy2(path, back1)


def log_corruption(log_path: Path, message: str) -> None:
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now()} | {message}\n")


def safe_load_with_recovery(path: Path, log_path: Path) -> Optional[Any]:
    if not path.exists():
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        log_corruption(log_path, f"{path.name} corrupted. Attempting recovery.")
        _show_warning(f"{path.name} corrupted. Attempting recovery.")
        for backup in [
            path.with_suffix(path.suffix + ".back1"),
            path.with_suffix(path.suffix + ".back2"),
        ]:
            if backup.exists():
                try:
                    with open(backup, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    shutil.copy2(backup, path)
                    _show_warning(f"Recovered from {backup.name}.")
                    return data
                except Exception:
                    continue
        _show_warning(f"Recovery failed for {path.name}. Resetting.")
        return None


# ═════════════════════════════════════════════════════════════════════════════
# LOCK MANAGEMENT
# ═════════════════════════════════════════════════════════════════════════════

def create_lock(lock_path: Path) -> None:
    write_atomic(lock_path, {
        "pid":       os.getpid(),
        "timestamp": datetime.now().isoformat(),
    })


def remove_lock(lock_path: Path) -> None:
    if lock_path.exists():
        lock_path.unlink()


def check_and_cleanup_stale_lock(lock_path: Path) -> None:
    if not lock_path.exists():
        return
    try:
        with open(lock_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        age = (datetime.now() - datetime.fromisoformat(data["timestamp"])).total_seconds()
        if age > LOCK_TIMEOUT_SECONDS:
            remove_lock(lock_path)
            _show_warning("Stale engine lock removed.")
        else:
            raise RuntimeError("Another engine instance is running.")
    except RuntimeError:
        raise
    except Exception:
        remove_lock(lock_path)


# ═════════════════════════════════════════════════════════════════════════════
# DIALOGS
# ═════════════════════════════════════════════════════════════════════════════

def _show_warning(message: str) -> None:
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)
    msg.setWindowTitle("Structural State Warning")
    msg.setText(message)
    msg.exec()


def show_diff_dialog(diff: Dict) -> None:
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setWindowTitle("Structural Diff")
    msg.setText(json.dumps(diff, indent=4))
    msg.exec()


# ═════════════════════════════════════════════════════════════════════════════
# DIFF VIEWER
# ═════════════════════════════════════════════════════════════════════════════

def compute_structural_diff(old: Dict, new: Dict) -> Dict:
    return {
        "magnitude_delta": (
            new["structural_change"]["magnitude"]
            - old["structural_change"]["magnitude"]
        ),
        "debt_delta": (
            new["refactor_pressure"]["debt_index"]
            - old["refactor_pressure"]["debt_index"]
        ),
        "risk_change": (
            f"{old['complexity_state']['risk_level']}"
            f" -> {new['complexity_state']['risk_level']}"
        ),
    }


# ═════════════════════════════════════════════════════════════════════════════
# STATE VECTOR VALIDATION & RECOMPUTE
# ═════════════════════════════════════════════════════════════════════════════

def validate_schema(obj: Dict) -> None:
    # ── Top-level keys ────────────────────────────────────────────
    if set(obj.keys()) != CANONICAL_KEYS:
        missing = CANONICAL_KEYS - set(obj.keys())
        extra   = set(obj.keys()) - CANONICAL_KEYS
        raise ValueError(f"Schema mismatch. Missing: {missing}  Extra: {extra}")
    if obj["state_vector_version"] != "2.0":
        raise ValueError("state_vector_version must be '2.0'.")
    if obj["incremental"] is not True:
        raise ValueError("incremental must be true.")

    # ── Sub-object key enforcement ────────────────────────────────
    def _check_sub(block_name: str, required: set) -> None:
        block = obj.get(block_name, {})
        if not isinstance(block, dict):
            raise ValueError(f"'{block_name}' must be a dict.")
        missing = required - set(block.keys())
        if missing:
            raise ValueError(f"'{block_name}' missing keys: {missing}")

    _check_sub("structural_change",  CANONICAL_STRUCTURAL_CHANGE_KEYS)
    _check_sub("complexity_state",   CANONICAL_COMPLEXITY_KEYS)
    _check_sub("governance_state",   CANONICAL_GOVERNANCE_KEYS)
    _check_sub("refactor_pressure",  CANONICAL_REFACTOR_KEYS)
    _check_sub("pattern_dynamics",   CANONICAL_PATTERN_KEYS)
    _check_sub("forward_projection", CANONICAL_PROJECTION_KEYS)
    _check_sub("architectural_snapshot", CANONICAL_SNAPSHOT_KEYS)

    # ── Nested sub-object enforcement ─────────────────────────────
    snap = obj["architectural_snapshot"]

    ipt = snap.get("integration_points_touched", {})
    if not isinstance(ipt, dict):
        raise ValueError("'integration_points_touched' must be a dict.")
    missing_ipt = CANONICAL_INTEGRATION_KEYS - set(ipt.keys())
    if missing_ipt:
        raise ValueError(f"'integration_points_touched' missing keys: {missing_ipt}")
    for k, v in ipt.items():
        if not isinstance(v, bool):
            raise ValueError(f"'integration_points_touched.{k}' must be boolean.")

    for sub, keys in [
        ("async_changes",           CANONICAL_ASYNC_KEYS),
        ("exception_handling_changes", CANONICAL_EXCEPTION_KEYS),
        ("localization_changes",    CANONICAL_LOCALIZATION_KEYS),
    ]:
        block = snap.get(sub, {})
        if not isinstance(block, dict):
            raise ValueError(f"'architectural_snapshot.{sub}' must be a dict.")
        missing_k = keys - set(block.keys())
        if missing_k:
            raise ValueError(f"'architectural_snapshot.{sub}' missing keys: {missing_k}")

    # ── summary_narrative mandatory ────────────────────────────────
    narrative = snap.get("summary_narrative", "")
    if not narrative or not isinstance(narrative, str) or len(narrative.strip()) < 5:
        raise ValueError("'summary_narrative' is mandatory and must be a meaningful string.")

    # ── lines_added / lines_removed must be integers, never null ──
    sc = obj["structural_change"]
    for field in ("lines_added", "lines_removed"):
        if not isinstance(sc.get(field), int):
            raise ValueError(f"'structural_change.{field}' must be an integer (use 0 if unknown).")

    # ── files_modified non-empty when modules_touched > 0 ─────────
    if sc.get("modules_touched", 0) > 0 and not sc.get("files_modified"):
        raise ValueError("'files_modified' must not be empty when modules_touched > 0.")

    # ── docstrings_added assessed when functions/classes added ─────
    funcs_added   = sc.get("functions_added", [])
    classes_added = sc.get("classes_added", [])
    if (funcs_added or classes_added):
        if snap.get("docstrings_added") is None:
            raise ValueError(
                "'docstrings_added' must be assessed (not null) when functions or classes were added."
            )


def recompute_fields(v: Dict) -> Dict:
    v    = copy.deepcopy(v)
    sc   = v["structural_change"]
    mag  = sc["magnitude"]
    debt = v["refactor_pressure"]["debt_index"]

    # ── Risk level from magnitude ─────────────────────────────────
    if mag <= 3:
        risk = "low"
    elif mag <= 10:
        risk = "medium"
    else:
        risk = "high"

    v["complexity_state"]["risk_level"] = risk

    # ── Governance score ──────────────────────────────────────────
    v["governance_state"]["score"] = max(0, 100 - debt)

    # ── Refactor inevitability horizon rule ───────────────────────
    rp = v["refactor_pressure"]
    if (
        rp.get("debt_index", 0) > 15
        and sc.get("acceleration", 0) > 5
        and risk == "high"
        and rp.get("refactor_inevitability_horizon") is None
    ):
        rp["refactor_inevitability_horizon"] = 30   # default: 30 days

    # ── Regression rule ───────────────────────────────────────────
    cs = v["complexity_state"]
    if (
        cs.get("volatility", 0.0) > 0.6
        and cs.get("stability_trajectory") == "degrading"
    ):
        fp = v["forward_projection"]
        if fp.get("regression_risk_probability", 0.0) <= 0.5:
            fp["regression_risk_probability"] = 0.51

    # ── Cortex-awareness: constitutional_evolution pattern ────────
    snap    = v["architectural_snapshot"]
    ipt     = snap.get("integration_points_touched", {})
    cortex_signals = any([
        "governance" in str(v.get("governance_state", {})).lower(),
        snap.get("layer_distribution", {}).get("cortex", 0) > 0,
    ])
    if cortex_signals:
        pd = v["pattern_dynamics"]
        if "constitutional_evolution" not in pd.get("dominant_patterns", []):
            pd.setdefault("dominant_patterns", []).append("constitutional_evolution")

    # ── Timestamp ─────────────────────────────────────────────────
    v["timestamp"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    return v


# ═════════════════════════════════════════════════════════════════════════════
# PROJECT SNAPSHOT EXTRACTOR  (was project_snapshot_extractor.py)
# ═════════════════════════════════════════════════════════════════════════════

def _safe_read_text(path: Path) -> Optional[str]:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return None


def _count_ast_nodes(text: str) -> Optional[int]:
    try:
        return sum(1 for _ in ast.walk(ast.parse(text)))
    except Exception:
        return None


def extract_project_snapshot(
    domain_root: Path, output_path: Path, prefix: str
) -> Dict[str, Any]:
    py_files         = list(domain_root.rglob("*.py"))
    module_count     = 0
    total_lines      = 0
    max_lines        = 0
    ast_total        = 0
    parse_errors     = 0
    read_errors      = 0

    for fp in py_files:
        text = _safe_read_text(fp)
        if text is None:
            read_errors += 1
            continue
        module_count += 1
        lines = text.count("\n") + 1
        total_lines += lines
        if lines > max_lines:
            max_lines = lines
        nodes = _count_ast_nodes(text)
        if nodes is None:
            parse_errors += 1
        else:
            ast_total += nodes

    snapshot = {
        "snapshot_version":        "1.1",
        "domain_prefix":           prefix,
        "timestamp":               datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "domain_root":             str(domain_root),
        "python_file_count":       len(py_files),
        "module_count":            module_count,
        "total_lines":             total_lines,
        "avg_lines_per_module":    round(total_lines / module_count, 2) if module_count else 0.0,
        "max_module_size_lines":   max_lines,
        "ast_node_count_total":    ast_total,
        "avg_ast_nodes_per_module":round(ast_total / module_count, 2) if module_count else 0.0,
        "parse_error_count":       parse_errors,
        "read_error_count":        read_errors,
    }
    write_atomic(output_path, snapshot)
    return snapshot


# ═════════════════════════════════════════════════════════════════════════════
# SYMBOL INDEX EXTRACTOR  (was symbol_index_extractor.py)
# ═════════════════════════════════════════════════════════════════════════════

def extract_symbol_index(
    domain_root: Path, output_path: Path, prefix: str
) -> Dict[str, Any]:
    py_files = list(domain_root.rglob("*.py"))
    symbols: List[Dict[str, Any]] = []

    for fp in py_files:
        try:
            source = fp.read_text(encoding="utf-8", errors="replace")
            tree   = ast.parse(source)
        except Exception:
            continue

        for node in tree.body:
            base = {
                "module":     str(fp.relative_to(domain_root)),
                "line_start": node.lineno if hasattr(node, "lineno") else 0,
                "line_end":   getattr(node, "end_lineno", getattr(node, "lineno", 0)),
            }
            if isinstance(node, ast.ClassDef):
                symbols.append({**base, "name": node.name, "type": "class"})
            elif isinstance(node, ast.FunctionDef):
                symbols.append({**base, "name": node.name, "type": "function"})
            elif isinstance(node, ast.AsyncFunctionDef):
                symbols.append({**base, "name": node.name, "type": "async_function"})
            elif isinstance(node, ast.Assign):
                for t in node.targets:
                    if isinstance(t, ast.Name):
                        symbols.append({**base, "name": t.id, "type": "constant"})

    index = {
        "index_version": "1.0",
        "domain_prefix": prefix,
        "timestamp":     datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "symbol_count":  len(symbols),
        "symbols":       sorted(symbols, key=lambda s: (s["module"], s["name"])),
    }
    write_atomic(output_path, index)
    return index


# ═════════════════════════════════════════════════════════════════════════════
# SYMBOL CHURN ANALYZER  (was symbol_churn_analyzer.py)
# ═════════════════════════════════════════════════════════════════════════════

def _load_symbol_set(path: Path) -> Set[str]:
    if not path.exists():
        return set()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return {
            f"{s['module']}::{s['type']}::{s['name']}"
            for s in data.get("symbols", [])
        }
    except Exception:
        return set()


def analyze_symbol_churn(
    previous_path: Path,
    current_path:  Path,
    output_path:   Path,
    prefix:        str,
) -> Dict[str, Any]:
    prev = _load_symbol_set(previous_path)
    curr = _load_symbol_set(current_path)

    added   = sorted(curr - prev)
    removed = sorted(prev - curr)
    churn   = len(added) + len(removed)
    ratio   = round(churn / max(len(prev), 1), 4)

    result = {
        "churn_version":         "1.0",
        "domain_prefix":         prefix,
        "timestamp":             datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "previous_symbol_count": len(prev),
        "current_symbol_count":  len(curr),
        "added_count":           len(added),
        "removed_count":         len(removed),
        "churn_count":           churn,
        "churn_ratio":           ratio,
        "added_symbols":         added,
        "removed_symbols":       removed,
    }
    write_atomic(output_path, result)
    return result


# ═════════════════════════════════════════════════════════════════════════════
# DEPENDENCY GRAPH EXTRACTOR  (was dependency_graph_extractor.py)
# ═════════════════════════════════════════════════════════════════════════════

def _module_name_from_path(root: Path, fp: Path) -> str:
    return ".".join(fp.relative_to(root).with_suffix("").parts)


def _file_imports(fp: Path) -> List[str]:
    try:
        tree = ast.parse(fp.read_text(encoding="utf-8", errors="replace"), filename=str(fp))
    except Exception:
        return []
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.append(node.module)
    return imports


def _detect_cycles(graph: Dict[str, List[str]]) -> List[List[str]]:
    visited: Set[str] = set()
    stack:   Set[str] = set()
    cycles:  List     = []

    def dfs(node: str, path: List[str]) -> None:
        visited.add(node); stack.add(node)
        for nb in graph.get(node, []):
            if nb not in visited:
                dfs(nb, path + [nb])
            elif nb in stack:
                cycles.append(path + [nb])
        stack.remove(node)

    for n in graph:
        if n not in visited:
            dfs(n, [n])
    return cycles


def _tarjan_scc(graph: Dict[str, List[str]]) -> List[List[str]]:
    idx = 0
    stack: List[str] = []
    indices:  Dict[str, int] = {}
    lowlink:  Dict[str, int] = {}
    on_stack: Set[str]       = set()
    sccs:     List           = []

    def sc(v: str) -> None:
        nonlocal idx
        indices[v] = lowlink[v] = idx
        idx += 1
        stack.append(v); on_stack.add(v)
        for w in graph.get(v, []):
            if w not in indices:
                sc(w)
                lowlink[v] = min(lowlink[v], lowlink[w])
            elif w in on_stack:
                lowlink[v] = min(lowlink[v], indices[w])
        if lowlink[v] == indices[v]:
            comp = []
            while True:
                w = stack.pop(); on_stack.remove(w); comp.append(w)
                if w == v:
                    break
            sccs.append(comp)

    for v in graph:
        if v not in indices:
            sc(v)
    return sccs


def extract_dependency_graph(domain_root: Path) -> Dict[str, Any]:
    nodes:     Set[str]          = set()
    edges:     List[Dict]        = []
    adjacency: Dict[str, List]   = {}

    for fp in domain_root.rglob("*.py"):
        if "__pycache__" in fp.parts:
            continue
        mod = _module_name_from_path(domain_root, fp)
        nodes.add(mod)
        adjacency.setdefault(mod, [])
        for imp in _file_imports(fp):
            adjacency[mod].append(imp)
            edges.append({"from": mod, "to": imp, "kind": "import"})

    cycles = _detect_cycles(adjacency)
    sccs   = _tarjan_scc(adjacency)
    cyclic = [c for c in sccs if len(c) > 1]

    return {
        "root":                         str(domain_root),
        "nodes":                        sorted(nodes),
        "edges":                        sorted(edges, key=lambda e: (e["from"], e["to"])),
        "cycles_detected":              cycles,
        "strongly_connected_components":sccs,
        "cyclic_components":            cyclic,
        "stats": {
            "node_count":            len(nodes),
            "edge_count":            len(edges),
            "cycle_count":           len(cycles),
            "cyclic_component_count":len(cyclic),
        },
    }


# ═════════════════════════════════════════════════════════════════════════════
# STABILITY ANALYZER  (was stability_analyzer.py)
# ═════════════════════════════════════════════════════════════════════════════

def analyze_stability(inputs: AnalysisInputs) -> AnalyzerResult:
    dep   = inputs.dependency_graph or {}
    churn = inputs.symbol_churn     or {}

    # ── instability (Martin metric) ──────────────────────────────
    nodes    = dep.get("nodes", [])
    edges    = dep.get("edges", [])
    internal = set(n for n in nodes if isinstance(n, str))

    ca: Dict[str, int] = {m: 0 for m in internal}
    ce: Dict[str, int] = {m: 0 for m in internal}

    for e in edges:
        frm, to = e.get("from"), e.get("to")
        if frm in internal and to in internal and frm != to:
            ce[frm] += 1
            ca[to]  += 1

    modules_out = []
    for m in sorted(internal):
        d = ca[m] + ce[m]
        modules_out.append({
            "module":      m,
            "ca":          ca[m],
            "ce":          ce[m],
            "instability": round(ce[m] / d, 6) if d else 0.0,
        })

    top_unstable = sorted(modules_out, key=lambda x: (x["instability"], x["ce"]), reverse=True)
    top_stable   = sorted(modules_out, key=lambda x: (x["instability"], x["ca"], x["ce"]))

    cyclic     = dep.get("cyclic_components", [])
    cyc_count  = len(cyclic)
    cyc_mods: Set[str] = set()
    for comp in cyclic:
        if isinstance(comp, list):
            cyc_mods.update(str(x) for x in comp)

    # ── churn ─────────────────────────────────────────────────────
    added   = churn.get("added",   []) if isinstance(churn.get("added"),   list) else []
    removed = churn.get("removed", []) if isinstance(churn.get("removed"), list) else []
    churn_total = len(added) + len(removed)

    # ── combined risk score ───────────────────────────────────────
    score = 0; notes = []
    if cyc_count:
        score += min(30, cyc_count * 10); notes.append("cycles_present")
    if cyc_mods:
        score += min(20, len(cyc_mods) * 2); notes.append("cyclic_modules_present")

    high_unstable = sum(
        1 for m in modules_out
        if m["instability"] >= 0.8 and m["ce"] >= 2
    )
    if high_unstable:
        score += min(30, high_unstable * 3); notes.append("high_instability_modules")

    if churn_total >= 20:
        score += 20; notes.append("high_churn")
    elif churn_total >= 10:
        score += 10; notes.append("moderate_churn")
    elif churn_total > 0:
        score += 5;  notes.append("low_churn")

    score = max(0, min(100, score))
    level = "high" if score >= 70 else "medium" if score >= 35 else "low"

    return AnalyzerResult(
        name="stability_analyzer",
        version="1.0",
        result={
            "layer": "stability_analyzer_v1",
            "ok":    True,
            "summary": {
                "combined_risk_score": score,
                "combined_risk_level": level,
                "notes":               notes,
            },
            "instability": {
                "available": True,
                "stats": {
                    "internal_module_count":  len(internal),
                    "internal_edge_count":    sum(1 for e in edges
                                                  if e.get("from") in internal
                                                  and e.get("to") in internal
                                                  and e.get("from") != e.get("to")),
                    "cyclic_component_count": cyc_count,
                    "cyclic_module_count":    len(cyc_mods),
                },
                "modules":      modules_out,
                "top_unstable": top_unstable[:15],
                "top_stable":   top_stable[:15],
            },
            "churn": {
                "added_count":   len(added),
                "removed_count": len(removed),
                "delta":         len(added) - len(removed),
                "note":          churn.get("note", ""),
            },
            "snapshot": {
                "available": bool(inputs.snapshot),
                "keys": sorted(inputs.snapshot.keys())[:50],
            },
            "symbol_index": {
                "available":    bool(inputs.symbol_index),
                "symbol_count": len(inputs.symbol_index.get("symbols", [])),
            },
        },
    )


# ═════════════════════════════════════════════════════════════════════════════
# CONSTITUTION ENFORCER  (was constitution_enforcer.py)
# ═════════════════════════════════════════════════════════════════════════════

def analyze_constitution(inputs: AnalysisInputs) -> AnalyzerResult:
    dep_graph = inputs.dependency_graph or {}
    rules     = inputs.governance_rules or {}

    violations      = []
    violation_count = 0
    domains         = rules.get("domains", {})
    enforcement     = rules.get("enforcement", {})
    edges           = dep_graph.get("edges", [])

    for edge in edges:
        src = edge.get("from", "")
        tgt = edge.get("to",   "")
        for domain_rules in domains.values():
            root_pkg  = domain_rules.get("root_package", "")
            forbidden = domain_rules.get("forbidden_import_prefixes", [])
            if src.startswith(root_pkg):
                for fp in forbidden:
                    if tgt.startswith(fp):
                        violation_count += 1
                        violations.append({"type": "forbidden_import", "from": src, "to": tgt})

    max_forbidden = enforcement.get("max_forbidden_edges", 0)
    compliance    = "fail" if violation_count > max_forbidden else "pass"

    return AnalyzerResult(
        name="constitution_enforcer",
        version="1.0",
        result={
            "violation_count": violation_count,
            "violations":      violations,
            "compliance":      compliance,
        },
    )


# ═════════════════════════════════════════════════════════════════════════════
# REFACTOR STRATEGIST  (was refactor_strategist.py)
# ═════════════════════════════════════════════════════════════════════════════

def analyze_refactor_strategy(inputs: AnalysisInputs) -> AnalyzerResult:
    snapshot   = inputs.snapshot          or {}
    churn      = inputs.symbol_churn      or {}
    dep_graph  = inputs.dependency_graph  or {}

    sym_by_mod  = snapshot.get("symbols_by_module", {})
    centrality  = dep_graph.get("centrality", {})
    churn_by_mod= churn.get("by_module", {})

    overloaded:       List[str] = []
    unstable_central: List[str] = []

    for mod, count in sym_by_mod.items():
        try:
            if int(count) > 50:
                overloaded.append(mod)
        except Exception:
            pass

    for mod, cd in churn_by_mod.items():
        try:
            mc   = int(cd.get("added", 0)) + int(cd.get("removed", 0))
            cent = centrality.get(mod, {}).get("total_degree", 0)
            if mc > 5 and cent > 5:
                unstable_central.append(mod)
        except Exception:
            pass

    if len(unstable_central) > 3:
        priority = "high"
    elif len(overloaded) > 3:
        priority = "medium"
    else:
        priority = "low"

    return AnalyzerResult(
        name="refactor_strategist",
        version="1.0",
        result={
            "overloaded_modules":       sorted(overloaded),
            "unstable_central_modules": sorted(unstable_central),
            "optimization_priority":    priority,
            "metrics_used": {
                "symbol_density_threshold": 50,
                "centrality_threshold":     5,
                "churn_threshold":          5,
            },
        },
    )


# ═════════════════════════════════════════════════════════════════════════════
# DOMAIN CONFIG  (replaces radio buttons + hardcoded paths)
# ═════════════════════════════════════════════════════════════════════════════

def build_config_named(
    domain_root:    Path,
    output_folder:  Path,
    json_name:      str,
    ai_bundle_path: Optional[Path] = None,
) -> Dict[str, Any]:
    """
    Build all engine paths for one named report.

    Parameters
    ----------
    domain_root    : root folder of the Python project being analysed.
    output_folder  : parent folder under which <prefix>_report/ is created.
    json_name      : stem used for all filenames, e.g. "my_report"
                     → report folder : <output_folder>/my_report_daily_refactor_engine/
                     → state file    : my_report_current_state.json
                     → bundle file   : my_report_daily_refactor_report_bundle.json
    ai_bundle_path : optional override for the <prefix>_daily_refactor_report_bundle.json
                     destination.  When None (default) the bundle is written
                     inside the report folder alongside all other files.
                     When supplied, the bundle is written to that exact path
                     (parent directories are created automatically).

    Output file layout
    ------------------
    <output_folder>/<prefix>_daily_refactor_engine/
    │
    ├── <prefix>_current_state.json               ← latest compiled state vector
    ├── <prefix>_state_history.json               ← rolling window of last 7 vectors
    ├── <prefix>_daily_refactor_report_bundle.json ← single file to give the AI
    │                                                (redirected if ai_bundle_path set)
    ├── engine.lock                               ← temporary; deleted after each run
    ├── corruption_alert.log                      ← written only when a file fails to load
    │
    ├── derived/
    │   ├── project_snapshot.json        ← file count, line count, AST stats
    │   ├── symbol_index.json            ← every class/function/constant + location
    │   ├── symbol_index.previous.json   ← previous run's index (for churn diff)
    │   ├── symbol_churn.json            ← added/removed symbols since last run
    │   ├── dependency_graph.json        ← imports, cycles, SCCs
    │   ├── stability_analysis.json      ← Martin instability metrics, risk score
    │   └── domain_fingerprint.json      ← SHA-256 cache key (skip-logic)
    │
    └── archive/
        ├── current_state_YYYYMMDD_HHMMSS.json   ← timestamped snapshot per run
        └── ...                                   ← capped at 50 entries
    """
    prefix     = json_name or domain_root.name
    report_dir = output_folder / f"{prefix}_daily_refactor_engine"
    report_dir.mkdir(parents=True, exist_ok=True)
    archive_dir = report_dir / "archive"
    archive_dir.mkdir(exist_ok=True)

    # Bundle destination — override path or default inside report_dir
    if ai_bundle_path is not None:
        bundle_path = Path(ai_bundle_path)
        bundle_path.parent.mkdir(parents=True, exist_ok=True)  # guarantee folder exists
    else:
        bundle_path = report_dir / f"{prefix}_daily_refactor_report_bundle.json"

    return {
        "prefix":      prefix,
        "root":        report_dir,
        "current":     report_dir / f"{prefix}_current_state.json",
        "history":     report_dir / f"{prefix}_state_history.json",
        "log":         report_dir / "corruption_alert.log",
        "lock":        report_dir / "engine.lock",
        "archive":     archive_dir,
        "fingerprint": report_dir / "derived" / "domain_fingerprint.json",
        "ai_bundle":   bundle_path,
    }


def build_config(domain_root: Path) -> Dict[str, Any]:
    """Fallback wrapper -- output next to domain folder, prefix = folder name."""
    return build_config_named(domain_root, domain_root, domain_root.name)


# ═════════════════════════════════════════════════════════════════════════════
# ENGINE PIPELINE PHASES
# ═════════════════════════════════════════════════════════════════════════════

def phase_lock(config: Dict) -> None:
    check_and_cleanup_stale_lock(config["lock"])
    create_lock(config["lock"])


def phase_extraction(
    config: Dict, domain_root: Path, force: bool = False
) -> Tuple[Dict[str, Any], bool]:
    """
    Returns (derived_data, was_skipped).
    Skips re-extraction if domain fingerprint is unchanged and force=False.
    """
    derived = config["root"] / "derived"
    derived.mkdir(parents=True, exist_ok=True)

    snap_path  = derived / "project_snapshot.json"
    idx_path   = derived / "symbol_index.json"
    prev_path  = derived / "symbol_index.previous.json"
    churn_path = derived / "symbol_churn.json"
    fp_path    = config["fingerprint"]

    # ── Skip check ────────────────────────────────────────────────
    if not force:
        unchanged, current_fp = domain_is_unchanged(domain_root, fp_path)
        if unchanged and snap_path.exists() and idx_path.exists() and churn_path.exists():
            return {
                "snapshot":     safe_load_with_recovery(snap_path,  config["log"]) or {},
                "symbol_index": safe_load_with_recovery(idx_path,   config["log"]) or {},
                "symbol_churn": safe_load_with_recovery(churn_path, config["log"]) or {},
                "_skipped":     True,
                "_fingerprint": current_fp,
            }, True

    # ── Full extraction ───────────────────────────────────────────
    extract_project_snapshot(domain_root, snap_path, config["prefix"])

    if idx_path.exists():
        shutil.copy2(idx_path, prev_path)

    extract_symbol_index(domain_root, idx_path, config["prefix"])

    if prev_path.exists():
        analyze_symbol_churn(
            previous_path=prev_path,
            current_path=idx_path,
            output_path=churn_path,
            prefix=config["prefix"],
        )
    else:
        write_atomic(churn_path, {"added": [], "removed": [], "note": "Initial run"})

    # Save new fingerprint after successful extraction
    _, current_fp = domain_is_unchanged(domain_root, fp_path)  # recompute after writes
    _save_fingerprint(fp_path, current_fp, domain_root)

    return {
        "snapshot":     safe_load_with_recovery(snap_path,  config["log"]) or {},
        "symbol_index": safe_load_with_recovery(idx_path,   config["log"]) or {},
        "symbol_churn": safe_load_with_recovery(churn_path, config["log"]) or {},
        "_skipped":     False,
        "_fingerprint": current_fp,
    }, False


def phase_analysis(
    config: Dict, domain_root: Path, derived_data: Dict,
    skipped_extraction: bool = False
) -> Dict[str, Any]:
    derived  = config["root"] / "derived"
    dep_path = derived / "dependency_graph.json"
    sta_path = derived / "stability_analysis.json"

    # ── Skip analysis if extraction was skipped and cached files exist ──
    if skipped_extraction and dep_path.exists() and sta_path.exists():
        dep_graph = safe_load_with_recovery(dep_path, config["log"]) or {}
        stability = safe_load_with_recovery(sta_path, config["log"]) or {}

        gov_path  = domain_root / "governance_rules.json"
        gov_rules: Dict = {}
        if gov_path.exists():
            try:
                gov_rules = json.loads(gov_path.read_text(encoding="utf-8"))
            except Exception:
                pass

        inputs = AnalysisInputs(
            snapshot         = derived_data["snapshot"],
            symbol_index     = derived_data["symbol_index"],
            symbol_churn     = derived_data["symbol_churn"],
            dependency_graph = dep_graph,
            governance_rules = gov_rules,
        )
        const = analyze_constitution(inputs)
        strat = analyze_refactor_strategy(inputs)

        return {
            "dependency_state":  dep_graph,
            "stability_state":   stability,
            "constitution_state":const.result,
            "strategy_state":    strat.result,
            "_analysis_skipped": True,
        }

    # ── Full analysis ─────────────────────────────────────────────
    dep_graph = extract_dependency_graph(domain_root)
    write_atomic(dep_path, dep_graph)

    gov_path  = domain_root / "governance_rules.json"
    gov_rules: Dict = {}
    if gov_path.exists():
        try:
            gov_rules = json.loads(gov_path.read_text(encoding="utf-8"))
        except Exception:
            pass

    inputs = AnalysisInputs(
        snapshot         = derived_data["snapshot"],
        symbol_index     = derived_data["symbol_index"],
        symbol_churn     = derived_data["symbol_churn"],
        dependency_graph = dep_graph,
        governance_rules = gov_rules,
    )

    stab  = analyze_stability(inputs)
    const = analyze_constitution(inputs)
    strat = analyze_refactor_strategy(inputs)

    write_atomic(sta_path, stab.result)

    return {
        "dependency_state":  dep_graph,
        "stability_state":   stab.result,
        "constitution_state":const.result,
        "strategy_state":    strat.result,
        "_analysis_skipped": False,
    }


def phase_persistence(config: Dict, merged: Dict) -> None:
    history  = safe_load_with_recovery(config["history"], config["log"]) or []
    previous = history[-1] if history else None

    history.append(merged)
    history = history[-ROLLING_WINDOW:]

    rotate_backups(config["current"])
    rotate_backups(config["history"])

    write_atomic(config["history"], history)
    write_atomic(config["current"], merged)

    if previous:
        show_diff_dialog(compute_structural_diff(previous, merged))


def phase_archive(config: Dict) -> None:
    snap = config["archive"] / f"current_state_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    shutil.copy2(config["current"], snap)
    for old in sorted(
        config["archive"].glob("*.json"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )[ARCHIVE_RETENTION:]:
        old.unlink()


def _load_with_status(path: Path, log_path: Path):
    if not path.exists():
        return {}, "missing"
    try:
        return json.loads(path.read_text(encoding="utf-8")), "ok"
    except Exception:
        rec = safe_load_with_recovery(path, log_path)
        return (rec, "recovered") if rec is not None else ({}, "corrupted")


def phase_ai_bundle(config: Dict) -> None:
    """
    Assembles all derived data, current state, and history into a single
    <prefix>_daily_refactor_report_bundle.json — the one file to give the AI for full project
    awareness.  Written to config["ai_bundle"], which may be inside the
    report folder (default) or any user-chosen path.
    """
    derived = config["root"] / "derived"
    log     = config["log"]

    snapshot,   s_st  = _load_with_status(derived / "project_snapshot.json",  log)
    symbol_idx, si_st = _load_with_status(derived / "symbol_index.json",      log)
    churn,      c_st  = _load_with_status(derived / "symbol_churn.json",      log)
    dependency, d_st  = _load_with_status(derived / "dependency_graph.json",  log)
    stability,  st_st = _load_with_status(derived / "stability_analysis.json",log)
    current,    cu_st = _load_with_status(config["current"],                  log)
    history,    h_st  = _load_with_status(config["history"],                  log)

    core = {
        "current_state": current,
        "state_history": history,
        "derived": {
            "project_snapshot":  snapshot,
            "symbol_index":      symbol_idx,
            "symbol_churn":      churn,
            "dependency_graph":  dependency,
            "stability_analysis":stability,
        },
    }
    integrity = hashlib.sha256(
        json.dumps(core, sort_keys=True).encode("utf-8")
    ).hexdigest()

    bundle = {
        "metadata": {
            "generated_at":   datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            "engine_version": "v12.4",
            "domain":         config["prefix"],
            "bundle_type":    "ai_upload",
            "report_folder":  str(config["root"]),
            "bundle_path":    str(config["ai_bundle"]),
            "load_status": {
                "project_snapshot":  s_st,
                "symbol_index":      si_st,
                "symbol_churn":      c_st,
                "dependency_graph":  d_st,
                "stability_analysis":st_st,
                "current_state":     cu_st,
                "state_history":     h_st,
            },
            "integrity_hash": integrity,
        },
        **core,
    }
    write_atomic(config["ai_bundle"], bundle)


# ═════════════════════════════════════════════════════════════════════════════
# MAIN WINDOW
# ═════════════════════════════════════════════════════════════════════════════

class StateVectorCompiler(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Structural State Compiler  v12.4")
        self.resize(900, 680)

        self._domain_root:    Optional[Path] = None
        self._config:         Optional[Dict] = None
        self._json_folder:    Optional[Path] = None   # user-chosen output folder
        self._json_name:      str            = ""     # user-chosen json file stem
        self._ai_bundle_path: Optional[Path] = None   # optional AI bundle override

        self._build_ui()

    # ─────────────────────────────────────────────────────────────
    # UI
    # ─────────────────────────────────────────────────────────────

    def _build_ui(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setSpacing(8)
        root.setContentsMargins(12, 12, 12, 12)

        # ── Step 1 — File to scan (optional) ────────────────────
        dg = QGroupBox("Step 1 — File to Scan  (optional — select any .py file inside the target folder to enable extraction)")
        dl = QHBoxLayout(dg)
        self.domain_edit = QLineEdit()
        self.domain_edit.setReadOnly(True)
        self.domain_edit.setPlaceholderText("No file selected — Compile will validate paste window only…")
        btn_browse = QPushButton("📂  Browse File…")
        btn_browse.clicked.connect(self._browse_domain)
        self.domain_label = QLabel("No file selected — paste-only mode")
        self.domain_label.setStyleSheet("color: #888;")
        dl.addWidget(self.domain_edit, 1)
        dl.addWidget(btn_browse)
        root.addWidget(dg)
        root.addWidget(self.domain_label)

        # ── Step 2 — JSON output config ──────────────────────────
        jg = QGroupBox("Step 2 — Output JSON  (name it, choose folder, or load existing)")
        jl = QHBoxLayout(jg)

        self.json_name_edit = QLineEdit()
        self.json_name_edit.setPlaceholderText("report_name  (no .json needed)")

        self.json_folder_edit = QLineEdit()
        self.json_folder_edit.setReadOnly(True)
        self.json_folder_edit.setPlaceholderText("Output folder — defaults to scanned file's folder…")

        btn_json_folder = QPushButton("📁  Choose Folder")
        btn_json_folder.clicked.connect(self._choose_json_folder)

        btn_load = QPushButton("⬆  Load Existing JSON")
        btn_load.clicked.connect(self._load_existing_json)

        jl.addWidget(QLabel("Name:"))
        jl.addWidget(self.json_name_edit, 2)
        jl.addWidget(QLabel("Folder:"))
        jl.addWidget(self.json_folder_edit, 3)
        jl.addWidget(btn_json_folder)
        jl.addWidget(btn_load)
        root.addWidget(jg)

        # ── Step 2b — AI Bundle output path (optional) ───────────
        ag = QGroupBox(
            "Step 2b — AI Bundle Path  (optional — leave blank to save inside report folder)"
        )
        ag.setToolTip(
            "When set, <prefix>_daily_refactor_report_bundle.json is written to this exact\n"
            "path instead of the default <prefix>_daily_refactor_engine/ folder.\n"
            "Useful when you want to keep the AI context file in a dedicated folder\n"
            "separate from the engine's internal report files."
        )
        al = QHBoxLayout(ag)

        self.ai_bundle_edit = QLineEdit()
        self.ai_bundle_edit.setReadOnly(True)
        self.ai_bundle_edit.setPlaceholderText(
            "Leave blank → <prefix>_daily_refactor_report_bundle.json saved inside <prefix>_daily_refactor_engine/ …"
        )

        btn_ai_bundle_file   = QPushButton("💾  Set Bundle Path…")
        btn_ai_bundle_file.setToolTip("Choose the exact file path for <prefix>_daily_refactor_report_bundle.json")
        btn_ai_bundle_file.clicked.connect(self._choose_ai_bundle_path)

        btn_ai_bundle_clear  = QPushButton("✕  Clear")
        btn_ai_bundle_clear.setToolTip("Reset to default (save inside report folder)")
        btn_ai_bundle_clear.clicked.connect(self._clear_ai_bundle_path)

        al.addWidget(self.ai_bundle_edit, 1)
        al.addWidget(btn_ai_bundle_file)
        al.addWidget(btn_ai_bundle_clear)
        root.addWidget(ag)

        # ── Step 3 — State vector paste area ────────────────────
        sv_group = QGroupBox("Step 3 — State Vector JSON  (paste here, then Compile)")
        sv_layout = QVBoxLayout(sv_group)
        self.text_area = QTextEdit()
        self.text_area.setFont(QFont("Courier New", 9))
        self.text_area.setPlaceholderText(
            '{\n'
            '  "state_vector_version": "2.0",\n'
            '  "incremental": true,\n'
            '  "structural_change": {\n'
            '    "magnitude": 0, "surface_area": 0, "acceleration": 0, "modules_touched": 0,\n'
            '    "files_modified": [], "functions_added": [], "functions_modified": [],\n'
            '    "functions_removed": [], "classes_added": [], "classes_modified": [],\n'
            '    "lines_added": 0, "lines_removed": 0\n'
            '  },\n'
            '  "complexity_state": {\n'
            '    "risk_level": "low", "volatility": 0.0, "stability_trajectory": "stable",\n'
            '    "cyclomatic_complexity_delta": 0, "nesting_depth_max": 0, "coupling_degree": "low"\n'
            '  },\n'
            '  "governance_state": {\n'
            '    "score": 100, "mode_impact": "none",\n'
            '    "breaking_changes": false, "backward_compatible": true,\n'
            '    "test_coverage_impact": "unchanged"\n'
            '  },\n'
            '  "refactor_pressure": {\n'
            '    "debt_index": 0, "hotspots": 0, "duplication_factor": 0.0,\n'
            '    "refactor_inevitability_horizon": null, "technical_debt_notes": []\n'
            '  },\n'
            '  "pattern_dynamics": {\n'
            '    "dominant_patterns": [], "new_patterns": [], "deprecated_patterns": [],\n'
            '    "design_patterns_detected": [], "anti_patterns_detected": []\n'
            '  },\n'
            '  "forward_projection": {\n'
            '    "expected_next_stress": "low", "regression_risk_probability": 0.0,\n'
            '    "next_likely_hotspot": "", "suggested_next_action": ""\n'
            '  },\n'
            '  "architectural_snapshot": {\n'
            '    "node_count": 0,\n'
            '    "layer_distribution": {"tab1": 0, "tab3": 0, "cortex": 0, "dev_tools": 0},\n'
            '    "dependencies_introduced": [], "dependencies_removed": [],\n'
            '    "imports_added": [], "constants_added": [], "global_state_mutations": [],\n'
            '    "integration_points_touched": {\n'
            '      "file_io": false, "network": false, "database": false, "subprocess": false,\n'
            '      "env_access": false, "serialisation": false, "concurrency": false, "logging": false\n'
            '    },\n'
            '    "localization_changes": {\n'
            '      "strings_added": 0, "hardcoded_urls_added": [], "translation_calls_added": 0\n'
            '    },\n'
            '    "side_effects_introduced": [],\n'
            '    "exception_handling_changes": {\n'
            '      "try_blocks_added": 0, "new_exceptions_caught": [], "new_exceptions_raised": []\n'
            '    },\n'
            '    "docstrings_added": 0, "type_hints_added": 0,\n'
            '    "async_changes": {"async_functions_added": [], "async_functions_removed": []},\n'
            '    "summary_narrative": "Describe what this implementation did and why it matters."\n'
            '  }\n'
            '}'
        )
        sv_layout.addWidget(self.text_area)
        root.addWidget(sv_group)

        # ── Compile buttons ──────────────────────────────────────
        btn_row = QHBoxLayout()

        btn_compile = QPushButton("▶   Compile State Vector")
        btn_compile.setFixedHeight(42)
        f = btn_compile.font(); f.setBold(True); f.setPointSize(f.pointSize() + 1)
        btn_compile.setFont(f)
        btn_compile.clicked.connect(self._compile)

        btn_force = QPushButton("🔄  Force Re-extract")
        btn_force.setFixedHeight(42)
        btn_force.setToolTip("Bypass cache and force full extraction + analysis even if domain is unchanged.")
        btn_force.clicked.connect(self._compile_force)

        btn_row.addWidget(btn_compile, 4)
        btn_row.addWidget(btn_force, 1)
        root.addLayout(btn_row)

        # ── Status bar ───────────────────────────────────────────
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage(
            "Step 1 (optional): select a .py file to enable extraction  →  Step 2: configure output  →  Step 3: paste canonical vector & Compile"
        )

    # ─────────────────────────────────────────────────────────────
    # DOMAIN BROWSE
    # ─────────────────────────────────────────────────────────────

    def _browse_domain(self) -> None:
        """Pick any .py file → its parent folder becomes the scan root for extraction."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select any .py file inside the folder to scan",
            "",
            "Python Files (*.py)",
        )
        if not file_path:
            return

        domain_root       = Path(file_path).resolve().parent
        self._domain_root = domain_root

        # If no custom JSON folder chosen yet, default to scanned file's folder
        if self._json_folder is None:
            self._json_folder = domain_root
            self.json_folder_edit.setText(str(domain_root))

        self._refresh_config()
        self.domain_edit.setText(str(Path(file_path).resolve()))
        self.domain_label.setText(
            f"Scanning: {domain_root.name}   │   Output: {self._config['root']}"
        )
        self.domain_label.setStyleSheet("color: #2ecc71;")
        self.status_bar.showMessage(
            f"File to scan: {Path(file_path).name}  →  folder: {domain_root.name}  →  output: {self._config['root'].name}/"
        )

    def _choose_ai_bundle_path(self) -> None:
        """Let user pick the exact file path for <prefix>_daily_refactor_report_bundle.json."""
        name   = self.json_name_edit.text().strip() or "state_vector"
        name   = name.replace(".json", "")
        default_name = f"{name}_daily_refactor_report_bundle.json"
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Set AI Bundle output path",
            default_name,
            "JSON Files (*.json)",
        )
        if path:
            self._ai_bundle_path = Path(path)
            self.ai_bundle_edit.setText(path)
            self._refresh_config()
            self.status_bar.showMessage(f"AI bundle will be saved to: {path}")

    def _clear_ai_bundle_path(self) -> None:
        """Reset AI bundle path to default (inside report folder)."""
        self._ai_bundle_path = None
        self.ai_bundle_edit.clear()
        self._refresh_config()
        self.status_bar.showMessage("AI bundle path cleared — will save inside report folder.")

    def _choose_json_folder(self) -> None:
        folder = QFileDialog.getExistingDirectory(self, "Choose Output Folder for JSON")
        if folder:
            self._json_folder = Path(folder)
            self.json_folder_edit.setText(folder)
            self._refresh_config()
            self.status_bar.showMessage(f"Output folder set: {folder}")

    def _load_existing_json(self) -> None:
        """Load an existing current_state.json to pre-fill the text area for editing."""
        path, _ = QFileDialog.getOpenFileName(
            self, "Load Existing State JSON", "", "JSON Files (*.json)"
        )
        if not path:
            return
        try:
            p    = Path(path)
            data = json.loads(p.read_text(encoding="utf-8"))

            # Pre-fill name + folder from the loaded file
            self._json_folder = p.parent
            self._json_name   = p.stem
            self.json_folder_edit.setText(str(p.parent))
            self.json_name_edit.setText(p.stem)

            # If it looks like a full compiled state, extract just the
            # canonical state-vector keys so the user can edit and re-compile
            sv_keys = CANONICAL_KEYS
            if isinstance(data, list):
                sv_data = data[0]
            else:
                sv_data = data

            # Strip any analysis outputs that were merged in; keep only canonical
            stripped = {k: v for k, v in sv_data.items() if k in sv_keys}
            if stripped:
                self.text_area.setPlainText(json.dumps(stripped, indent=4))
                self.status_bar.showMessage(
                    f"Loaded '{p.name}' — canonical keys extracted, ready to edit & Compile."
                )
            else:
                # File may be a raw state vector already — paste as-is
                self.text_area.setPlainText(json.dumps(data, indent=4))
                self.status_bar.showMessage(f"Loaded '{p.name}' — pasted as-is into editor.")

            self._refresh_config()
            QMessageBox.information(
                self, "JSON Loaded",
                f"Loaded: {p.name}\n\n"
                "The state vector keys have been placed in the editor.\n"
                "Edit as needed, then click Compile."
            )
        except Exception as e:
            QMessageBox.critical(self, "Load Error", f"Could not load JSON:\n{e}")

    def _refresh_config(self) -> None:
        """Rebuild config whenever domain, JSON output, or AI bundle settings change."""
        if self._domain_root is None:
            return
        folder = self._json_folder or self._domain_root
        name   = self.json_name_edit.text().strip() or self._domain_root.name
        name   = name.replace(".json", "")          # strip extension if pasted with it
        self._json_name = name
        self._config    = build_config_named(
            self._domain_root,
            folder,
            name,
            ai_bundle_path=self._ai_bundle_path,
        )

    # ─────────────────────────────────────────────────────────────
    # COMPILE
    # ─────────────────────────────────────────────────────────────

    def _compile_force(self) -> None:
        """Force full extraction + analysis, bypassing the file-scan cache."""
        if self._domain_root is None:
            QMessageBox.warning(
                self, "No File Selected",
                "Force Re-extract requires a file to be selected in Step 1."
            )
            return
        self._compile(force=True)

    def _compile(self, force: bool = False) -> None:
        """
        Two-mode compile:

        MODE A — File selected (Step 1):
            Runs full 7-phase pipeline: extraction → analysis → validate
            state vector → persist → archive → AI bundle.

        MODE B — No file selected:
            Validates the pasted state vector against the canonical schema,
            recomputes auto-derived fields, and saves ONLY:
              • <name>_current_state.json
              • <name>_state_history.json
            No extraction, no analysis, no AI bundle, no archive.
            Output folder must be set in Step 2 (or defaults to user home).
        """
        raw = self.text_area.toPlainText().strip()
        if not raw:
            QMessageBox.warning(
                self, "Empty",
                "Nothing pasted in Step 3.\n\nPaste a canonical state vector JSON and try again."
            )
            return

        # ── MODE A: file selected — full pipeline ─────────────────
        if self._domain_root is not None:
            self._compile_full(raw, force=force)
        else:
            # ── MODE B: no file — paste-only ──────────────────────
            self._compile_paste_only(raw)

    # ─────────────────────────────────────────────────────────────
    # MODE A  — full 7-phase pipeline
    # ─────────────────────────────────────────────────────────────

    def _compile_full(self, raw: str, force: bool = False) -> None:
        """Full pipeline: extraction + analysis + state vector + persist + archive + bundle."""
        self._refresh_config()
        if self._config is None:
            QMessageBox.warning(self, "Config Error", "Could not build config. Check file selection.")
            return
        config = self._config

        try:
            phase_lock(config)

            self.status_bar.showMessage("Phase 2/7 — Checking file-scan fingerprint…")
            QApplication.processEvents()
            derived_data, was_skipped = phase_extraction(config, self._domain_root, force=force)

            if was_skipped:
                self.status_bar.showMessage(
                    "Phase 2/7 — CACHED: folder unchanged, skipping extraction & analysis…"
                )
            else:
                self.status_bar.showMessage("Phase 2/7 — Extracting project snapshot…")
            QApplication.processEvents()

            if not was_skipped:
                self.status_bar.showMessage("Phase 3/7 — Running analyzers…")
                QApplication.processEvents()
            analysis_outputs = phase_analysis(
                config, self._domain_root, derived_data,
                skipped_extraction=was_skipped,
            )

            self.status_bar.showMessage("Phase 4/7 — Parsing state vector…")
            QApplication.processEvents()
            parsed  = json.loads(raw)
            vectors = parsed if isinstance(parsed, list) else [parsed]
            validated = []
            for v in vectors:
                validate_schema(v)
                validated.append(recompute_fields(v))
            merged = validated[0]
            merged.update(analysis_outputs)

            self.status_bar.showMessage("Phase 5/7 — Persisting state…")
            QApplication.processEvents()
            phase_persistence(config, merged)

            self.status_bar.showMessage("Phase 6/7 — Archiving snapshot…")
            QApplication.processEvents()
            phase_archive(config)

            self.status_bar.showMessage("Phase 7/7 — Building AI bundle…")
            QApplication.processEvents()
            phase_ai_bundle(config)

            self.text_area.clear()
            cache_note = "  [CACHED]" if was_skipped else "  [full extraction]"
            self.status_bar.showMessage(
                f"✓ Compiled (full pipeline) — {config['prefix']}  →  {config['root']}{cache_note}"
            )
            QMessageBox.information(
                self, "Success — Full Pipeline",
                f"'{config['prefix']}' compiled successfully.\n\n"
                f"Report folder:\n{config['root']}\n\n"
                f"AI bundle saved to:\n{config['ai_bundle']}\n\n"
                f"{'⚡ Extraction CACHED (folder unchanged)' if was_skipped else '🔄 Full extraction ran (folder changed)'}"
            )
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            self.status_bar.showMessage(f"Error: {e}")
        finally:
            remove_lock(config["lock"])

    # ─────────────────────────────────────────────────────────────
    # MODE B  — paste-only (no file selected)
    # ─────────────────────────────────────────────────────────────

    def _compile_paste_only(self, raw: str) -> None:
        """
        Validate + recompute the pasted state vector and save current_state +
        state_history only.  No file scanning, no AI bundle, no archive.
        Output folder comes from Step 2; if unset, defaults to user home.
        """
        # Resolve output folder — use Step 2 folder or fallback to home
        folder = self._json_folder or Path.home()
        name   = self.json_name_edit.text().strip() or "state_vector"
        name   = name.replace(".json", "")

        # Build a minimal config (no domain_root — use folder itself as placeholder)
        config = build_config_named(
            domain_root    = folder,
            output_folder  = folder,
            json_name      = name,
            ai_bundle_path = self._ai_bundle_path,
        )

        try:
            parsed  = json.loads(raw)
            vectors = parsed if isinstance(parsed, list) else [parsed]
            validated = []
            for v in vectors:
                validate_schema(v)
                validated.append(recompute_fields(v))
            merged = validated[0]

            phase_persistence(config, merged)

            self.text_area.clear()
            self.status_bar.showMessage(
                f"✓ Compiled (paste-only) — saved to {config['root']}"
            )
            QMessageBox.information(
                self, "Success — Paste-Only Mode",
                "State vector validated and saved.\n\n"
                "No file was selected so extraction, analysis, and AI bundle were skipped.\n\n"
                f"Files written:\n"
                f"  {config['current'].name}\n"
                f"  {config['history'].name}\n\n"
                f"Folder:\n{config['root']}\n\n"
                "To enable full extraction + AI bundle, select a .py file in Step 1."
            )
        except json.JSONDecodeError as e:
            QMessageBox.critical(self, "JSON Parse Error", f"Invalid JSON in paste window:\n{e}")
            self.status_bar.showMessage(f"JSON parse error: {e}")
        except ValueError as e:
            QMessageBox.critical(
                self, "Schema Validation Error",
                f"Pasted JSON does not match canonical structure:\n\n{e}"
            )
            self.status_bar.showMessage(f"Validation error: {e}")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            self.status_bar.showMessage(f"Error: {e}")


# ═════════════════════════════════════════════════════════════════════════════
# ENTRY POINT
# ═════════════════════════════════════════════════════════════════════════════

def main() -> None:
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = StateVectorCompiler()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
