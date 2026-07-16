"""
Daily AI Structural Awareness Engine - v11.0
============================================
Single-file edition — all helper logic inlined, no external imports.

Changes from v10.0:
  - All helper modules inlined (project_snapshot_extractor, symbol_index_extractor,
    symbol_churn_analyzer, dependency_graph_extractor, stability_analyzer,
    constitution_enforcer, refactor_strategist, analysis_contracts)
  - Radio buttons removed
  - Domain is now selected by picking ANY .py file inside the target domain folder.
    The engine derives domain_root from the selected file's parent directory.
  - JSON output (current_state, history, archive, ai_upload_bundle) is created
    inside a  "daily_refactor_report/"  sub-folder next to the selected file.
  - State vector JSON is still pasted into the text area and compiled as before.
  - All other logic (lock, backup rotation, corruption recovery, diff viewer,
    archive retention, AI upload bundle, integrity hash) is fully preserved.
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
    if set(obj.keys()) != CANONICAL_KEYS:
        raise ValueError("Schema mismatch.")
    if obj["state_vector_version"] != "2.0":
        raise ValueError("Invalid version.")
    if obj["incremental"] is not True:
        raise ValueError("incremental must be true.")


def recompute_fields(v: Dict) -> Dict:
    v    = copy.deepcopy(v)
    mag  = v["structural_change"]["magnitude"]
    debt = v["refactor_pressure"]["debt_index"]

    if mag <= 3:
        risk = "low"
    elif mag <= 10:
        risk = "medium"
    else:
        risk = "high"

    v["complexity_state"]["risk_level"] = risk
    v["governance_state"]["score"]      = max(0, 100 - debt)
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
    domain_root:   Path,
    output_folder: Path,
    json_name:     str,
) -> Dict[str, Any]:
    """
    Build all engine paths.
    output_folder : where the report sub-folder is created
    json_name     : stem for filenames, e.g. "my_report"
                    -> folder: <output_folder>/my_report_report/
                    -> files:  my_report_current_state.json
    """
    prefix     = json_name or domain_root.name
    report_dir = output_folder / f"{prefix}_report"
    report_dir.mkdir(parents=True, exist_ok=True)
    archive_dir = report_dir / "archive"
    archive_dir.mkdir(exist_ok=True)

    return {
        "prefix":  prefix,
        "root":    report_dir,
        "current": report_dir / f"{prefix}_current_state.json",
        "history": report_dir / f"{prefix}_state_history.json",
        "log":     report_dir / "corruption_alert.log",
        "lock":    report_dir / "engine.lock",
        "archive": archive_dir,
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
    config: Dict, domain_root: Path
) -> Dict[str, Any]:
    derived = config["root"] / "derived"
    derived.mkdir(parents=True, exist_ok=True)

    snap_path    = derived / "project_snapshot.json"
    idx_path     = derived / "symbol_index.json"
    prev_path    = derived / "symbol_index.previous.json"
    churn_path   = derived / "symbol_churn.json"

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

    return {
        "snapshot":     safe_load_with_recovery(snap_path,  config["log"]) or {},
        "symbol_index": safe_load_with_recovery(idx_path,   config["log"]) or {},
        "symbol_churn": safe_load_with_recovery(churn_path, config["log"]) or {},
    }


def phase_analysis(
    config: Dict, domain_root: Path, derived_data: Dict
) -> Dict[str, Any]:
    derived   = config["root"] / "derived"
    dep_graph = extract_dependency_graph(domain_root)
    write_atomic(derived / "dependency_graph.json", dep_graph)

    gov_path = domain_root / "governance_rules.json"
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

    stab   = analyze_stability(inputs)
    const  = analyze_constitution(inputs)
    strat  = analyze_refactor_strategy(inputs)

    write_atomic(derived / "stability_analysis.json", stab.result)

    return {
        "dependency_state":  dep_graph,
        "stability_state":   stab.result,
        "constitution_state":const.result,
        "strategy_state":    strat.result,
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
            "engine_version": "v11.0",
            "domain":         config["prefix"],
            "bundle_type":    "ai_upload",
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
    write_atomic(config["root"] / "ai_upload_bundle.json", bundle)


# ═════════════════════════════════════════════════════════════════════════════
# MAIN WINDOW
# ═════════════════════════════════════════════════════════════════════════════

class StateVectorCompiler(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Structural State Compiler  v11.0")
        self.resize(900, 680)

        self._domain_root:  Optional[Path] = None
        self._config:       Optional[Dict] = None
        self._json_folder:  Optional[Path] = None   # user-chosen output folder
        self._json_name:    str            = ""     # user-chosen json file stem

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

        # ── Step 1 — Domain folder ───────────────────────────────
        dg = QGroupBox("Step 1 — Domain  (select any .py file inside the target folder)")
        dl = QHBoxLayout(dg)
        self.domain_edit = QLineEdit()
        self.domain_edit.setReadOnly(True)
        self.domain_edit.setPlaceholderText("No domain selected…")
        btn_browse = QPushButton("📂  Browse Domain…")
        btn_browse.clicked.connect(self._browse_domain)
        self.domain_label = QLabel("No domain loaded")
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
        self.json_folder_edit.setPlaceholderText("Output folder — defaults to domain folder…")

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

        # ── Step 3 — State vector paste area ────────────────────
        sv_group = QGroupBox("Step 3 — State Vector JSON  (paste here, then Compile)")
        sv_layout = QVBoxLayout(sv_group)
        self.text_area = QTextEdit()
        self.text_area.setFont(QFont("Courier New", 9))
        self.text_area.setPlaceholderText(
            '{\n'
            '  "state_vector_version": "2.0",\n'
            '  "incremental": true,\n'
            '  "structural_change": {"magnitude": 0},\n'
            '  "complexity_state": {},\n'
            '  "governance_state": {},\n'
            '  "refactor_pressure": {"debt_index": 0},\n'
            '  "pattern_dynamics": {},\n'
            '  "forward_projection": {},\n'
            '  "architectural_snapshot": {}\n'
            '}'
        )
        sv_layout.addWidget(self.text_area)
        root.addWidget(sv_group)

        # ── Compile button ───────────────────────────────────────
        btn_compile = QPushButton("▶   Compile State Vector")
        btn_compile.setFixedHeight(42)
        f = btn_compile.font(); f.setBold(True); f.setPointSize(f.pointSize() + 1)
        btn_compile.setFont(f)
        btn_compile.clicked.connect(self._compile)
        root.addWidget(btn_compile)

        # ── Status bar ───────────────────────────────────────────
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage(
            "Step 1: select domain  →  Step 2: name/load JSON  →  Step 3: paste & Compile"
        )

    # ─────────────────────────────────────────────────────────────
    # DOMAIN BROWSE
    # ─────────────────────────────────────────────────────────────

    def _browse_domain(self) -> None:
        """Pick any .py file → its parent becomes domain_root."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select any .py file inside the domain folder",
            "",
            "Python Files (*.py)",
        )
        if not file_path:
            return

        domain_root       = Path(file_path).resolve().parent
        self._domain_root = domain_root

        # If no custom JSON folder chosen yet, default to domain folder
        if self._json_folder is None:
            self._json_folder = domain_root
            self.json_folder_edit.setText(str(domain_root))

        self._refresh_config()
        self.domain_edit.setText(str(domain_root))
        self.domain_label.setText(
            f"Domain: {domain_root.name}   │   Output: {self._config['root']}"
        )
        self.domain_label.setStyleSheet("color: #2ecc71;")
        self.status_bar.showMessage(
            f"Domain: {domain_root.name}  →  output in {self._config['root'].name}/"
        )

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
        """Rebuild config whenever domain or JSON output settings change."""
        if self._domain_root is None:
            return
        folder = self._json_folder or self._domain_root
        name   = self.json_name_edit.text().strip() or self._domain_root.name
        name   = name.replace(".json", "")          # strip extension if pasted with it
        self._json_name = name
        self._config    = build_config_named(self._domain_root, folder, name)

    # ─────────────────────────────────────────────────────────────
    # COMPILE
    # ─────────────────────────────────────────────────────────────

    def _compile(self) -> None:
        if self._domain_root is None:
            QMessageBox.warning(
                self, "No Domain",
                "Please select a domain folder first (Step 1 — Browse button)."
            )
            return

        # Always re-read name field in case user typed it after browsing
        self._refresh_config()

        if self._config is None:
            QMessageBox.warning(self, "Config Error", "Could not build config. Check domain.")
            return

        config = self._config

        try:
            # Phase 1 — Lock
            phase_lock(config)

            # Phase 2 — Extraction
            self.status_bar.showMessage("Phase 2/7 — Extracting project snapshot…")
            QApplication.processEvents()
            derived_data = phase_extraction(config, self._domain_root)

            # Phase 3 — Analysis
            self.status_bar.showMessage("Phase 3/7 — Running analyzers…")
            QApplication.processEvents()
            analysis_outputs = phase_analysis(config, self._domain_root, derived_data)

            # Phase 4 — Parse + validate state vector
            self.status_bar.showMessage("Phase 4/7 — Parsing state vector…")
            QApplication.processEvents()
            raw    = self.text_area.toPlainText().strip()
            parsed = json.loads(raw)
            vectors = parsed if isinstance(parsed, list) else [parsed]
            validated = []
            for v in vectors:
                validate_schema(v)
                validated.append(recompute_fields(v))
            merged = validated[0]
            merged.update(analysis_outputs)

            # Phase 5 — Persistence
            self.status_bar.showMessage("Phase 5/7 — Persisting state…")
            QApplication.processEvents()
            phase_persistence(config, merged)

            # Phase 6 — Archive
            self.status_bar.showMessage("Phase 6/7 — Archiving snapshot…")
            QApplication.processEvents()
            phase_archive(config)

            # Phase 7 — AI upload bundle
            self.status_bar.showMessage("Phase 7/7 — Building AI upload bundle…")
            QApplication.processEvents()
            phase_ai_bundle(config)

            self.text_area.clear()
            self.status_bar.showMessage(
                f"✓ Compiled successfully — {config['prefix']}  →  {config['root']}"
            )
            QMessageBox.information(
                self, "Success",
                f"'{config['prefix']}' state compiled successfully.\n\n"
                f"Output folder:\n{config['root']}"
            )

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            self.status_bar.showMessage(f"Error: {e}")

        finally:
            remove_lock(config["lock"])


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
