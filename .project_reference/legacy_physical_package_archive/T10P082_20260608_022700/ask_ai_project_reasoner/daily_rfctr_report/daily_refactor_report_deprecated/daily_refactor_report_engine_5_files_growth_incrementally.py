"""
Daily AI Structural Awareness Engine - v12.8
============================================
Changes from v12.7:
  - Step 1 now asks for a FOLDER, not a .py file.
    Uses getExistingDirectory — user picks the project folder directly.
    All .py files in that folder are scanned automatically.
  - _selected_file removed; domain_root is set directly from the chosen folder.
  - All prior v12.7 logic preserved.

Structural State Compiler - v12.8
==================================

PURPOSE:
--------
The Structural State Compiler is an Advanced AI Architectural Awareness tool designed
to bridge the gap between raw source code and Large Language Model (LLM) context windows.
It performs deep static analysis of Python projects to generate a "Canonical State Vector"—
a highly compressed, structured JSON representation of a project's logic, complexity,
and governance status.

By maintaining a rolling history of these vectors, the engine provides the AI with
temporal awareness, allowing it to understand not just what the code is, but how
it is evolving (refactor pressure, symbol churn, and architectural stability).



KEY FEATURES:
-------------
1.  DEEP AST SCANNING: Parses entire folder trees recursively, extracting functions,
    classes, imports, and try-blocks while ignoring non-Python assets and caches.
2.  SAFETY ISOLATION: Automatically identifies "broken" Python files with syntax errors,
    reporting them to the user without halting the overall project analysis.
3.  DUAL-MODE PIPELINE:
    - Mode A (Scanned): Generates data from physical files in Step 1.
    - Mode B (Paste-only): Validates and increments history based on manual JSON input.
4.  ATOMIC PERSISTENCE: Ensures data integrity during writes using temporary sibling
    files and atomic replacement, preventing JSON corruption during power/system failure.
5.  AI UPLOAD BUNDLE: Consolidates current state, historical vectors, and derived
    dependency graphs into a single file for easy LLM context injection.



OPERATIONAL WORKFLOW (HOW TO USE):
----------------------------------
STEP 1: DEFINE THE SOURCE (OPTIONAL)
    Click '📂 Browse Folder…' to select your Python project root. The engine will
    automatically prepare to scan every .py file in the directory and sub-directories.

STEP 2: CONFIGURE OUTPUT
    - NAME: Enter a unique stem (e.g., 'auth_module'). This names all generated files.
    - FOLDER: Choose where the engine should store its internal databases and logs.
    - (Optional) BUNDLE PATH: Set a specific redirection path for the final AI report.

STEP 3: EXECUTE THE COMPILATION
    - If Step 3 is empty: Click '▶ Compile State Vector'. The engine scans the folder
      from Step 1, detects broken files, generates a baseline JSON, and populates the area.
    - If Step 3 has JSON: Edit the fields manually if desired, then click '▶ Compile'
      to merge the scan data with your manual updates and append to the history.

STEP 4: UPLOAD
    Locate the '<prefix>_daily_refactor_report_bundle.json' in your Step 2 folder.
    This is the only file you need to provide to the AI for full project awareness.

ENGINEERING NOTES:
------------------
- The engine enforces 'state_vector_version': '2.0'.
- Logic ensures 'structural_change' magnitudes are automatically capped at 20
  to maintain high signal-to-noise ratios for LLM interpretation.
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
from typing import Any, Dict, List, Optional, Set, Tuple

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


def normalize_report_base_name(filename_stem: str) -> str:
    """Return the base chosen report name from a known engine filename."""
    suffixes = (
        "_daily_refactor_report_bundle",
        "_current_state",
        "_state_history",
    )
    for suffix in suffixes:
        if filename_stem.endswith(suffix):
            return filename_stem[: -len(suffix)]
    return filename_stem


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
    """
    Write JSON atomically.  Uses a sibling .tmp file then os.replace()
    which is atomic on POSIX and as close as possible on Windows.
    os.replace() works even when the destination already exists (unlike
    Path.rename() on some Windows configurations).
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    try:
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, sort_keys=True)
        os.replace(str(tmp), str(path))   # atomic on POSIX; best-effort on Windows
    except Exception:
        # Clean up temp file if anything went wrong
        try:
            if tmp.exists():
                tmp.unlink()
        except Exception:
            pass
        raise


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
        bundle_path = output_folder / f"{prefix}_daily_refactor_report_bundle.json"

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

    rotate_backups(config["current"])
    rotate_backups(config["history"])

    write_atomic(config["history"], history)
    write_atomic(config["current"], merged)

    if previous:
        show_diff_dialog(compute_structural_diff(previous, merged))


def phase_archive(config: Dict) -> None:
    snap = config["archive"] / f"current_state_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    shutil.copy2(config["current"], snap)
    # No deletion – keep all archived snapshots


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
    <prefix>_daily_refactor_report_bundle.json.
    Written to config["ai_bundle"] — default inside report folder, or
    any user-chosen override path set in Step 2b.
    """
    derived     = config["root"] / "derived"
    log         = config["log"]
    bundle_path = Path(config["ai_bundle"])   # always coerce to Path

    # Guarantee the destination folder exists regardless of override
    bundle_path.parent.mkdir(parents=True, exist_ok=True)

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
            "engine_version": "v12.6",
            "domain":         config["prefix"],
            "bundle_type":    "ai_upload",
            "report_folder":  str(config["root"]),
            "bundle_path":    str(bundle_path),
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

    # Write — any exception propagates up to the caller's isolated try/except
    write_atomic(bundle_path, bundle)


# ═════════════════════════════════════════════════════════════════════════════
# MAIN WINDOW
# ═════════════════════════════════════════════════════════════════════════════

def is_canonical_state_vector(obj: Any) -> bool:
    """Return True only if obj looks like a canonical state vector."""
    return isinstance(obj, dict) and set(obj.keys()) == CANONICAL_KEYS


def extract_canonical_state_vector(data: Any) -> Dict[str, Any]:
    """
    Extract a canonical state vector from:
    - direct canonical JSON
    - a list whose first item is canonical
    - a bundle JSON containing current_state
    """
    if is_canonical_state_vector(data):
        return data

    if isinstance(data, list) and data:
        first = data[0]
        if is_canonical_state_vector(first):
            return first

    if isinstance(data, dict):
        current_state = data.get("current_state")
        if is_canonical_state_vector(current_state):
            return current_state

        if isinstance(current_state, dict):
            stripped = {k: v for k, v in current_state.items() if k in CANONICAL_KEYS}
            if set(stripped.keys()) == CANONICAL_KEYS:
                return stripped

    raise ValueError(
        "The selected JSON does not contain a canonical state vector. "
        "Expected a direct state vector or a bundle with 'current_state'."
    )


class StateVectorCompiler(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Structural State Compiler  v12.8")
        self.resize(900, 680)

        self._domain_root: Optional[Path] = None
        self._selected_file: Optional[Path] = None  # kept for compat, always None in v12.8
        self._config: Optional[Dict] = None
        self._json_folder: Optional[Path] = None
        self._json_name: str = ""
        self._ai_bundle_path: Optional[Path] = None
        self._loaded_history_path: Optional[Path] = None
        self._build_ui()
        self._update_ui_for_mode()


    def _clear_loaded_history(self) -> None:
        """Break link to the loaded history file when user changes folder/name."""
        self._loaded_history_path = None
        self._refresh_config()

    def _get_state_vector_input(self) -> Optional[str]:
        """
        Resolve the canonical state vector input.

        Priority:
        1. If Step 3 has JSON, use it.
        2. If Step 1 has a selected .py file, auto-build a compatible JSON from that file.
        3. Otherwise, ask the user to create or load a JSON.
        """
        raw = self.text_area.toPlainText().strip()
        if raw:
            return raw

        if self._domain_root is not None:
            auto_vector = self._build_state_vector_from_selected_file()
            auto_json = json.dumps(auto_vector, indent=4)
            self.text_area.setPlainText(auto_json)
            self.status_bar.showMessage(
                f"Auto-generated canonical state vector from folder: {self._domain_root.name}"
            )
            return auto_json

        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Question)
        msg.setWindowTitle("Missing State Vector")
        msg.setText(
            "No folder selected in Step 1 and no canonical JSON in Step 3.\n\n"
            "Choose what to do next."
        )

        create_btn = msg.addButton("Create New Template", QMessageBox.AcceptRole)
        load_btn = msg.addButton("Load Existing JSON", QMessageBox.ActionRole)
        msg.addButton("Cancel", QMessageBox.RejectRole)

        msg.exec()

        clicked = msg.clickedButton()
        if clicked == create_btn:
            self.text_area.setPlainText(json.dumps({
                "state_vector_version": "2.0",
                "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
                "incremental": True,
                "structural_change": {
                    "magnitude": 0,
                    "surface_area": 0,
                    "acceleration": 0,
                    "modules_touched": 0,
                    "files_modified": [],
                    "functions_added": [],
                    "functions_modified": [],
                    "functions_removed": [],
                    "classes_added": [],
                    "classes_modified": [],
                    "lines_added": 0,
                    "lines_removed": 0
                },
                "complexity_state": {
                    "risk_level": "low",
                    "volatility": 0.0,
                    "stability_trajectory": "stable",
                    "cyclomatic_complexity_delta": 0,
                    "nesting_depth_max": 0,
                    "coupling_degree": "low"
                },
                "governance_state": {
                    "score": 100,
                    "mode_impact": "none",
                    "breaking_changes": False,
                    "backward_compatible": True,
                    "test_coverage_impact": "unchanged"
                },
                "refactor_pressure": {
                    "debt_index": 0,
                    "hotspots": 0,
                    "duplication_factor": 0.0,
                    "refactor_inevitability_horizon": None,
                    "technical_debt_notes": []
                },
                "pattern_dynamics": {
                    "dominant_patterns": [],
                    "new_patterns": [],
                    "deprecated_patterns": [],
                    "design_patterns_detected": [],
                    "anti_patterns_detected": []
                },
                "forward_projection": {
                    "expected_next_stress": "low",
                    "regression_risk_probability": 0.0,
                    "next_likely_hotspot": "none_identified",
                    "suggested_next_action": "Fill in the state vector fields before compiling."
                },
                "architectural_snapshot": {
                    "node_count": 0,
                    "layer_distribution": {
                        "tab1": 0,
                        "tab3": 0,
                        "cortex": 0,
                        "dev_tools": 0
                    },
                    "dependencies_introduced": [],
                    "dependencies_removed": [],
                    "imports_added": [],
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
                        "logging": False
                    },
                    "localization_changes": {
                        "strings_added": 0,
                        "hardcoded_urls_added": [],
                        "translation_calls_added": 0
                    },
                    "side_effects_introduced": [],
                    "exception_handling_changes": {
                        "try_blocks_added": 0,
                        "new_exceptions_caught": [],
                        "new_exceptions_raised": []
                    },
                    "docstrings_added": 0,
                    "type_hints_added": 0,
                    "async_changes": {
                        "async_functions_added": [],
                        "async_functions_removed": []
                    },
                    "summary_narrative": "Fill in the implementation summary before compiling."
                }
            }, indent=4))
            self.status_bar.showMessage(
                "A new canonical state vector template was created in the editor."
            )
            return None

        if clicked == load_btn:
            self._load_existing_json()
            return None

        return None

    # ─────────────────────────────────────────────────────────────
    # UI
    # ─────────────────────────────────────────────────────────────

    def _build_ui(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setSpacing(8)
        root.setContentsMargins(12, 12, 12, 12)

        # ── Step 1 — Folder to scan (optional) ──────────────────
        dg = QGroupBox("Step 1 — Folder to Scan  (optional — all .py files inside will be scanned)")
        dl = QHBoxLayout(dg)
        self.domain_edit = QLineEdit()
        self.domain_edit.setReadOnly(True)
        self.domain_edit.setPlaceholderText(
            "No folder selected — Compile will validate paste window only…")
        btn_browse = QPushButton("📂  Browse Folder…")
        btn_browse.clicked.connect(self._browse_domain)
        self.domain_label = QLabel("No folder selected — paste-only mode")
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
        self.json_folder_edit.setReadOnly(False)  # allow typing
        self.json_folder_edit.setPlaceholderText("Output folder — type a path or use 📁 (created if it does not exist)")
        self.json_folder_edit.textChanged.connect(self._on_json_folder_edited)

        # --- NEW: Clear loaded history when name or folder changes ---
        self.json_name_edit.textChanged.connect(self._clear_loaded_history)
        self.json_folder_edit.textChanged.connect(self._clear_loaded_history)

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
            "Step 2b — AI Bundle Path  (optional — only used when a folder is selected)"
        )
        ag.setToolTip(
            "When set, <prefix>_daily_refactor_report_bundle.json is written to this exact\n"
            "path instead of the default <prefix>_daily_refactor_engine/ folder.\n"
            "This field is only active when a file is selected in Step 1."
        )
        al = QHBoxLayout(ag)

        self.ai_bundle_edit = QLineEdit()
        self.ai_bundle_edit.setPlaceholderText(
            "Leave blank → saved inside <prefix>_daily_refactor_engine/ …"
        )
        # Allow manual typing as well as browse
        self.ai_bundle_edit.textChanged.connect(self._on_bundle_path_edited)

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
        btn_force.setToolTip("Bypass cache and force full extraction + analysis even if folder is unchanged.")
        btn_force.clicked.connect(self._compile_force)

        self.btn_bundle = QPushButton("🗂  Save Bundle Now")
        self.btn_bundle.setFixedHeight(42)
        self.btn_bundle.setToolTip(
            "Write the AI bundle immediately from the last compiled state.\n"
            "Use this if the bundle file is missing without re-running the full pipeline."
        )
        self.btn_bundle.clicked.connect(self._save_bundle_now)

        btn_row.addWidget(btn_compile, 4)
        btn_row.addWidget(btn_force, 1)
        btn_row.addWidget(self.btn_bundle, 1)
        root.addLayout(btn_row)

        # ── Status bar ───────────────────────────────────────────
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage(
            "Step 1 (optional): select a folder to enable extraction  →  Step 2: configure output  →  Step 3: paste canonical vector & Compile"
        )

    # ─────────────────────────────────────────────────────────────
    # UI state management
    # ─────────────────────────────────────────────────────────────

    def _update_ui_for_mode(self) -> None:
        """Enable/disable bundle‑related controls based on whether a file is selected."""
        has_file = self._domain_root is not None
        self.ai_bundle_edit.setEnabled(has_file)
        self.btn_bundle.setEnabled(has_file)
        # The browse and clear buttons remain enabled, but the edit field will be read‑only if no file.
        # Actually, we want them to be usable only when has_file, otherwise they are pointless.
        # Let's disable the whole group box? But we'll keep it simple: just the edit field and the
        # "Save Bundle Now" button.
        # However, the user might want to set the bundle path before selecting a file, so we keep
        # the browse button enabled but the edit field disabled.
        for child in self.findChildren(QPushButton):
            if child.text() in ("💾  Set Bundle Path…", "✕  Clear"):
                child.setEnabled(has_file)

    # ─────────────────────────────────────────────────────────────
    # DOMAIN BROWSE
    # ─────────────────────────────────────────────────────────────

    def _build_state_vector_from_selected_file(self) -> Dict[str, Any]:
        """
        Build a canonical state vector from ALL .py files in domain_root.
        Skips broken files and reports errors to the user.
        """
        if self._domain_root is None:
            raise RuntimeError("No folder selected in Step 1.")

        domain_root = self._domain_root
        module_name = domain_root.name

        functions_added: List[str] = []
        classes_added: List[str] = []
        imports_added: List[str] = []
        files_modified: List[str] = []
        node_count = 0
        lines_added = 0
        try_blocks = 0
        async_funcs: List[str] = []

        # --- Safety Logic: Error Tracking ---
        broken_files: List[str] = []

        py_files = sorted(domain_root.rglob("*.py"))
        for fp in py_files:
            if "__pycache__" in fp.parts:
                continue

            rel_path = str(fp.relative_to(domain_root))

            try:
                source = fp.read_text(encoding="utf-8", errors="replace")
                # Attempt to parse. This will trigger SyntaxError if file is 'broken'
                tree = ast.parse(source)

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
                        for alias in node.names:
                            imports_added.append(alias.name)
                    elif isinstance(node, ast.ImportFrom) and node.module:
                        imports_added.append(node.module)
                    elif isinstance(node, ast.Try):
                        try_blocks += 1

            except SyntaxError as se:
                broken_files.append(f"❌ SYNTAX ERROR: {rel_path}\n   Line {se.lineno}: {se.msg}")
            except Exception as e:
                broken_files.append(f"❌ READ ERROR: {rel_path}\n   {str(e)}")

        # --- Report Broken Files to User ---
        if broken_files:
            error_report = "\n\n".join(broken_files)
            QMessageBox.warning(
                self,
                "Broken Files Detected",
                f"The following files are broken and were skipped from analysis:\n\n{error_report}"
            )

        # De-duplicate healthy results
        functions_added = sorted(set(functions_added))
        classes_added = sorted(set(classes_added))
        imports_added = sorted(set(imports_added))
        async_funcs = sorted(set(async_funcs))

        summary = (
            f"Auto-generated from {len(files_modified)} healthy file(s). "
            f"Skipped {len(broken_files)} broken file(s)."
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
            # ... (the rest of the dictionary keys remain exactly as in v12.8)
            "complexity_state": {
                "risk_level": "low" if len(files_modified) <= 3 else "medium",
                "volatility": 0.0,
                "stability_trajectory": "stable",
                "cyclomatic_complexity_delta": 0,
                "nesting_depth_max": 0,
                "coupling_degree": "low",
            },
            "governance_state": {
                "score": 100, "mode_impact": "none", "breaking_changes": False,
                "backward_compatible": True, "test_coverage_impact": "unknown",
            },
            "refactor_pressure": {
                "debt_index": 0, "hotspots": 0, "duplication_factor": 0.0,
                "refactor_inevitability_horizon": None, "technical_debt_notes": [],
            },
            "pattern_dynamics": {
                "dominant_patterns": [], "new_patterns": [], "deprecated_patterns": [],
                "design_patterns_detected": [], "anti_patterns_detected": [],
            },
            "forward_projection": {
                "expected_next_stress": "low", "regression_risk_probability": 0.0,
                "next_likely_hotspot": module_name,
                "suggested_next_action": "Review healthy baseline and compile.",
            },
            "architectural_snapshot": {
                "node_count": node_count,
                "layer_distribution": {"tab1": 0, "tab3": 0, "cortex": 0, "dev_tools": 0},
                "dependencies_introduced": [], "dependencies_removed": [],
                "imports_added": imports_added, "constants_added": [], "global_state_mutations": [],
                "integration_points_touched": {
                    "file_io": False, "network": False, "database": False, "subprocess": False,
                    "env_access": False, "serialisation": False, "concurrency": False, "logging": False
                },
                "localization_changes": {"strings_added": 0, "hardcoded_urls_added": [], "translation_calls_added": 0},
                "side_effects_introduced": [],
                "exception_handling_changes": {"try_blocks_added": try_blocks, "new_exceptions_caught": [],
                                               "new_exceptions_raised": []},
                "docstrings_added": len(functions_added) + len(classes_added), "type_hints_added": 0,
                "async_changes": {"async_functions_added": async_funcs, "async_functions_removed": []},
                "summary_narrative": summary,
            }
        }

    def _browse_domain(self) -> None:
        """Pick a folder — all .py files inside become the scan target."""
        folder_path = QFileDialog.getExistingDirectory(
            self,
            "Select the folder to scan (all .py files inside will be processed)",
            str(self._domain_root or Path.home()),
        )
        if not folder_path:
            return

        domain_root           = Path(folder_path).resolve()
        self._domain_root     = domain_root
        self._selected_file   = None   # no single file — whole folder mode
        self._clear_loaded_history()

        # Default Step 2 output folder to domain folder if not set yet
        if self._json_folder is None:
            self._json_folder = domain_root
            self.json_folder_edit.setText(str(domain_root))

        self._refresh_config()
        self.domain_edit.setText(str(domain_root))
        self.domain_label.setText(
            f"Scanning folder: {domain_root}   │   Output: {self._config['root']}"
        )
        self.domain_label.setStyleSheet("color: #2ecc71;")
        self.status_bar.showMessage(
            f"Folder to scan: {domain_root.name}  →  output: {self._config['root'].name}/"
        )
        self._update_ui_for_mode()

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

    def _on_bundle_path_edited(self, text: str) -> None:
        """Handle manual typing in the bundle path edit."""
        if text.strip():
            self._ai_bundle_path = Path(text.strip())
        else:
            self._ai_bundle_path = None
        self._refresh_config()

    def _on_json_folder_edited(self, text: str) -> None:
        """Sync _json_folder whenever the user types a path directly into the folder field."""
        stripped = text.strip()
        if stripped:
            self._json_folder = Path(stripped)
        else:
            self._json_folder = None
        # Don't call _refresh_config on every keystroke — only when domain is set
        if self._domain_root is not None:
            self._refresh_config()

    def _choose_json_folder(self) -> None:
        """
        Choose the output folder for Step 2.
        Uses the standard folder picker; if the folder does not exist yet,
        it is created immediately so the engine can write to it.
        """
        folder = QFileDialog.getExistingDirectory(
            self,
            "Choose Output Folder for JSON (folder will be created if it does not exist)",
            str(self._json_folder or Path.home()),
        )
        if not folder:
            return
        chosen = Path(folder)
        try:
            chosen.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            QMessageBox.critical(self, "Folder Error", f"Could not create folder:\n{chosen}\n\n{e}")
            return

        self._json_folder = chosen
        self.json_folder_edit.setText(str(chosen))
        self._clear_loaded_history()
        self._refresh_config()
        self.status_bar.showMessage(f"Output folder set: {chosen}")

    def _load_existing_json(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Load Existing State JSON",
            "",
            "JSON Files (*.json)",
        )
        if not path:
            return

        try:
            p = Path(path)
            data = json.loads(p.read_text(encoding="utf-8"))

            # Ensure data is a list of state vectors
            if isinstance(data, dict) and set(data.keys()) == CANONICAL_KEYS:
                history_list = [data]
            elif isinstance(data, list) and all(isinstance(item, dict) for item in data):
                history_list = data
            else:
                raise ValueError("File does not contain a canonical state vector or list thereof.")

            # Display the first vector in the editor (most recent or only one)
            self.text_area.setPlainText(json.dumps(history_list[0], indent=4))

            # Set output folder and name based on the loaded file
            self._json_folder = p.parent
            base_name = normalize_report_base_name(p.stem)
            self._json_name = base_name
            self.json_folder_edit.setText(str(p.parent))
            self.json_name_edit.setText(base_name)

            # Remember this path as the history file
            self._loaded_history_path = p

            self._refresh_config()

            self.status_bar.showMessage(f"Loaded history from '{p.name}'. Compiling will append to it.")
        except Exception as e:
            QMessageBox.critical(self, "Load Error", f"Could not load JSON:\n{e}")

    def _refresh_config(self) -> None:
        """
        Rebuild config whenever domain, JSON output, or AI bundle settings change.
        Always resolves the current ai_bundle_path so Step 2b override is never lost.
        Skips building the full engine config when no domain_root is set (paste-only
        mode builds its own config at compile time).
        If a history file was loaded via Step 2 (self._loaded_history_path is set),
        that path overrides the default history file location.
        """
        # Sync bundle path with the edit field
        bundle_text = self.ai_bundle_edit.text().strip()
        if bundle_text:
            self._ai_bundle_path = Path(bundle_text)
        elif not bundle_text and self._ai_bundle_path is not None:
            # Field cleared – handled by _clear_ai_bundle_path()
            pass

        if self._domain_root is None:
            return  # paste‑only mode builds its own config later

        folder = self._json_folder or self._domain_root
        name = self.json_name_edit.text().strip() or self._domain_root.name
        name = name.replace(".json", "")
        self._json_name = name
        self._config = build_config_named(
            self._domain_root,
            folder,
            name,
            ai_bundle_path=self._ai_bundle_path,
        )

        # If a history file was explicitly loaded, replace the default history path
        if self._loaded_history_path is not None:
            self._config["history"] = self._loaded_history_path

    # ─────────────────────────────────────────────────────────────
    # COMPILE
    # ─────────────────────────────────────────────────────────────

    def _save_bundle_now(self) -> None:
        """
        Write the AI bundle immediately from the last compiled state files,
        without re-running extraction or analysis.  Useful when the bundle
        file is missing but current_state.json and derived/ are intact.
        """
        if self._domain_root is None:
            QMessageBox.warning(
                self, "No Folder Selected",
                "Select a folder in Step 1 first so the engine knows which report folder to read from."
            )
            return

        # Rebuild config fresh from current field values
        folder      = self._json_folder or self._domain_root
        name        = self.json_name_edit.text().strip() or self._domain_root.name
        name        = name.replace(".json", "")
        bundle_text = self.ai_bundle_edit.text().strip()
        ai_bundle   = Path(bundle_text) if bundle_text else None

        config      = build_config_named(
            self._domain_root, folder, name, ai_bundle_path=ai_bundle,
        )

        # Apply loaded history override if any
        if self._loaded_history_path is not None:
            config["history"] = self._loaded_history_path

        try:
            config["ai_bundle"].parent.mkdir(parents=True, exist_ok=True)
            phase_ai_bundle(config)
            self.status_bar.showMessage(f"✓ Bundle written → {config['ai_bundle']}")
            # Verify file exists
            if not config["ai_bundle"].exists():
                raise RuntimeError(f"File was not created at {config['ai_bundle']}")
            QMessageBox.information(
                self, "✓ Bundle Saved",
                f"AI bundle written successfully.\n\n{config['ai_bundle']}"
            )
        except Exception as e:
            QMessageBox.critical(
                self, "Bundle Write Failed",
                f"Could not write bundle:\n{e}\n\nAttempted path:\n{config['ai_bundle']}"
            )
            self.status_bar.showMessage(f"Bundle write failed: {e}")

    def _compile_force(self) -> None:
        """Force full extraction + analysis, bypassing the file-scan cache."""
        if self._domain_root is None:
            QMessageBox.warning(
                self, "No Folder Selected",
                "Force Re-extract requires a folder to be selected in Step 1."
            )
            return
        self._compile(force=True)

    def _compile(self, force: bool = False) -> None:
        """
        Compile using:
        - selected .py file as analysis source, if present
        - canonical JSON from editor/load as state vector source
        """
        raw = self._get_state_vector_input()
        if raw is None:
            return

        if self._domain_root is not None:
            self._compile_full(raw, force=force)
        else:
            self._compile_paste_only(raw)

    # ─────────────────────────────────────────────────────────────
    # MODE A  — full 7-phase pipeline
    # ─────────────────────────────────────────────────────────────

    def _compile_full(self, raw: str, force: bool = False) -> None:
        """Full pipeline: extraction + analysis + state vector + persist + archive + bundle."""
        # Rebuild config fresh from all current field values — source of truth
        folder      = self._json_folder or self._domain_root
        name        = self.json_name_edit.text().strip() or self._domain_root.name
        name        = name.replace(".json", "")
        bundle_text = self.ai_bundle_edit.text().strip()
        ai_bundle   = Path(bundle_text) if bundle_text else None

        # Ensure output folder exists — create it if the user typed a new path
        try:
            folder.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            QMessageBox.critical(self, "Output Folder Error", f"Cannot create output folder:\n{folder}\n\n{e}")
            return

        config      = build_config_named(
            self._domain_root, folder, name, ai_bundle_path=ai_bundle,
        )
        self._config = config

        # Apply loaded history override if any
        if self._loaded_history_path is not None:
            config["history"] = self._loaded_history_path

        # ── Phases 1-6 ───────────────────────────────────────────
        try:
            phase_lock(config)

            self.status_bar.showMessage("Phase 2/7 — Checking file-scan fingerprint…")
            QApplication.processEvents()
            derived_data, was_skipped = phase_extraction(config, self._domain_root, force=force)

            if was_skipped:
                self.status_bar.showMessage("Phase 2/7 — CACHED: folder unchanged…")
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

            self.status_bar.showMessage("Phase 4/7 — Parsing & validating state vector…")
            QApplication.processEvents()
            parsed   = json.loads(raw)
            vectors  = parsed if isinstance(parsed, list) else [parsed]
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

        except Exception as e:
            QMessageBox.critical(self, "Pipeline Error (Phases 1-6)", str(e))
            self.status_bar.showMessage(f"Pipeline error: {e}")
            remove_lock(config["lock"])
            return   # ← stop here; don't attempt bundle write

        # ── Phase 7 — AI bundle (separate try so failure is always visible) ──
        bundle_error = None
        try:
            self.status_bar.showMessage(
                f"Phase 7/7 — Writing AI bundle → {config['ai_bundle']} …"
            )
            QApplication.processEvents()
            # Ensure destination folder exists (belt-and-suspenders)
            config["ai_bundle"].parent.mkdir(parents=True, exist_ok=True)
            phase_ai_bundle(config)
            # Verify existence
            if not config["ai_bundle"].exists():
                raise RuntimeError(f"File was not created at {config['ai_bundle']}")
        except Exception as e:
            bundle_error = str(e)
        finally:
            remove_lock(config["lock"])

        self.text_area.clear()
        cache_note = "  [CACHED]" if was_skipped else "  [full extraction]"

        if bundle_error:
            self.status_bar.showMessage(f"⚠ Phases 1-6 OK — bundle FAILED: {bundle_error}")
            QMessageBox.warning(
                self, "Phases 1-6 OK — Bundle Write Failed",
                f"State vector compiled and saved successfully.\n\n"
                f"BUT the AI bundle could not be written:\n{bundle_error}\n\n"
                f"Attempted path:\n{config['ai_bundle']}\n\n"
                f"Check the path in Step 2b is valid and the folder is writable."
            )
        else:
            self.status_bar.showMessage(
                f"✓ All 7 phases complete — {config['prefix']}{cache_note}"
            )
            QMessageBox.information(
                self, "✓ Success — Full Pipeline",
                f"'{config['prefix']}' compiled successfully.\n\n"
                f"Report folder:\n  {config['root']}\n\n"
                f"AI bundle written to:\n  {config['ai_bundle']}\n\n"
                f"{'⚡ Extraction CACHED (folder unchanged)' if was_skipped else '🔄 Full extraction ran (folder changed)'}"
            )

    # ─────────────────────────────────────────────────────────────
    # MODE B  — paste-only (no file selected)
    # ─────────────────────────────────────────────────────────────

    def _compile_paste_only(self, raw: str) -> None:
        """
        Validate + recompute the pasted state vector and save current_state +
        state_history. Now also attempts to generate an AI bundle if possible.
        """
        # Resolve output folder and name from Step 2 fields
        folder = self._json_folder or Path.home()
        name = self.json_name_edit.text().strip() or "state_vector"
        name = name.replace(".json", "")

        bundle_text = self.ai_bundle_edit.text().strip()
        ai_bundle = Path(bundle_text) if bundle_text else None

        config = build_config_named(domain_root=folder, output_folder=folder,
                                    json_name=name, ai_bundle_path=ai_bundle)

        if self._loaded_history_path is not None:
            config["history"] = self._loaded_history_path

        try:
            parsed = json.loads(raw)
            vectors = parsed if isinstance(parsed, list) else [parsed]
            validated = []
            for v in vectors:
                validate_schema(v)
                validated.append(recompute_fields(v))
            merged = validated[0]

            # 1. Persist the state and history
            phase_persistence(config, merged)

            # 2. Attempt to create the AI Bundle even in paste-only mode
            # Ensure the derived directory exists so phase_ai_bundle doesn't fail on path checks
            (config["root"] / "derived").mkdir(parents=True, exist_ok=True)
            phase_ai_bundle(config)

            self.text_area.clear()
            self.status_bar.showMessage(
                f"✓ Compiled & Bundled (paste-only) — saved to {config['root']}"
            )

            bundle_status = f"\nAI bundle written to:\n  {config['ai_bundle']}" if config["ai_bundle"].exists() else ""

            QMessageBox.information(
                self, "Success — Paste-Only Mode",
                f"State vector validated and saved.{bundle_status}\n\n"
                f"Note: Extraction was skipped because no source file was selected in Step 1."
            )
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Paste-only compilation failed:\n{e}")
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