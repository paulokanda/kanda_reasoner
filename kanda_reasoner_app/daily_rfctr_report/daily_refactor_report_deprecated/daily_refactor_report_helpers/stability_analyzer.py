import copy
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Set, Tuple


@dataclass(frozen=True)
class AnalysisResult:
    ok: bool
    result: Dict[str, Any]
    errors: List[str]


def analyze_stability(inputs) -> AnalysisResult:
    """
    Read-only analyzer.

    Inputs (expected on AnalysisInputs):
      - snapshot: dict
      - symbol_index: dict
      - symbol_churn: dict
      - dependency_graph: dict or None
      - governance_rules: dict or None

    Output:
      - stability_state: dict with instability metrics and risk summary
    """
    errors: List[str] = []

    snapshot = _safe_dict(getattr(inputs, "snapshot", None))
    symbol_index = _safe_dict(getattr(inputs, "symbol_index", None))
    symbol_churn = _safe_dict(getattr(inputs, "symbol_churn", None))
    dependency_graph = _safe_dict(getattr(inputs, "dependency_graph", None))

    instability_state = _compute_instability_state(dependency_graph, errors)
    churn_state = _compute_churn_state(symbol_churn, errors)
    snapshot_state = _compute_snapshot_state(snapshot, errors)
    symbol_state = _compute_symbol_state(symbol_index, errors)

    combined_risk = _combine_risk(instability_state, churn_state)

    result = {
        "layer": "stability_analyzer_v1",
        "ok": len(errors) == 0,
        "summary": {
            "combined_risk_score": combined_risk["score"],
            "combined_risk_level": combined_risk["level"],
            "notes": combined_risk["notes"],
        },
        "instability": instability_state,
        "churn": churn_state,
        "snapshot": snapshot_state,
        "symbol_index": symbol_state,
    }

    return AnalysisResult(ok=len(errors) == 0, result=result, errors=errors)


def _safe_dict(obj: Any) -> Dict[str, Any]:
    if isinstance(obj, dict):
        return obj
    return {}


def _compute_instability_state(dependency_graph: Dict[str, Any], errors: List[str]) -> Dict[str, Any]:
    if not dependency_graph:
        return {
            "available": False,
            "note": "dependency_graph missing",
            "stats": {},
            "modules": [],
            "top_unstable": [],
            "top_stable": [],
        }

    nodes = dependency_graph.get("nodes", [])
    edges = dependency_graph.get("edges", [])
    cyclic_components = dependency_graph.get("cyclic_components", [])

    internal_modules: Set[str] = set()
    for n in nodes:
        if isinstance(n, str) and n.strip():
            internal_modules.add(n)

    ca: Dict[str, int] = {m: 0 for m in internal_modules}
    ce: Dict[str, int] = {m: 0 for m in internal_modules}

    # Count only internal-to-internal imports to define couplings.
    for e in edges:
        frm = e.get("from")
        to = e.get("to")
        if not isinstance(frm, str) or not isinstance(to, str):
            continue
        if frm not in internal_modules:
            continue
        if to not in internal_modules:
            continue
        if frm == to:
            continue

        ce[frm] += 1
        ca[to] += 1

    modules_out: List[Dict[str, Any]] = []
    for m in sorted(internal_modules):
        denom = ca[m] + ce[m]
        instability = float(ce[m]) / float(denom) if denom > 0 else 0.0

        modules_out.append(
            {
                "module": m,
                "ca": ca[m],
                "ce": ce[m],
                "instability": round(instability, 6),
            }
        )

    # Rank unstable (highest I) and stable (lowest I but non-trivial coupling)
    unstable_sorted = sorted(modules_out, key=lambda x: (x["instability"], x["ce"]), reverse=True)
    stable_sorted = sorted(modules_out, key=lambda x: (x["instability"], x["ca"], x["ce"]))

    # Cycle penalty summary
    cycle_count = 0
    cyclic_module_count = 0
    if isinstance(cyclic_components, list):
        cycle_count = len(cyclic_components)
        seen: Set[str] = set()
        for comp in cyclic_components:
            if isinstance(comp, list):
                for item in comp:
                    if isinstance(item, str):
                        seen.add(item)
        cyclic_module_count = len(seen)

    return {
        "available": True,
        "stats": {
            "internal_module_count": len(internal_modules),
            "internal_edge_count": _count_internal_edges(edges, internal_modules),
            "cyclic_component_count": cycle_count,
            "cyclic_module_count": cyclic_module_count,
        },
        "modules": modules_out,
        "top_unstable": unstable_sorted[:15],
        "top_stable": stable_sorted[:15],
    }


def _count_internal_edges(edges: Any, internal_modules: Set[str]) -> int:
    if not isinstance(edges, list):
        return 0
    count = 0
    for e in edges:
        frm = e.get("from") if isinstance(e, dict) else None
        to = e.get("to") if isinstance(e, dict) else None
        if isinstance(frm, str) and isinstance(to, str) and frm in internal_modules and to in internal_modules and frm != to:
            count += 1
    return count


def _compute_churn_state(symbol_churn: Dict[str, Any], errors: List[str]) -> Dict[str, Any]:
    added = symbol_churn.get("added", [])
    removed = symbol_churn.get("removed", [])
    if not isinstance(added, list):
        added = []
    if not isinstance(removed, list):
        removed = []

    return {
        "added_count": len(added),
        "removed_count": len(removed),
        "delta": len(added) - len(removed),
        "note": symbol_churn.get("note", ""),
    }


def _compute_snapshot_state(snapshot: Dict[str, Any], errors: List[str]) -> Dict[str, Any]:
    # Keep this minimal and safe; you can expand later.
    return {
        "available": bool(snapshot),
        "keys": sorted(list(snapshot.keys()))[:50] if isinstance(snapshot, dict) else [],
    }


def _compute_symbol_state(symbol_index: Dict[str, Any], errors: List[str]) -> Dict[str, Any]:
    # Minimal signal: how many symbols total if present
    symbols = symbol_index.get("symbols")
    if isinstance(symbols, list):
        return {"available": True, "symbol_count": len(symbols)}
    if isinstance(symbol_index, dict) and symbol_index:
        # Some implementations store in different shapes
        return {"available": True, "symbol_count": _estimate_symbol_count(symbol_index)}
    return {"available": False, "symbol_count": 0}


def _estimate_symbol_count(symbol_index: Dict[str, Any]) -> int:
    # Conservative: count any list-valued fields as candidates
    count = 0
    for k, v in symbol_index.items():
        if isinstance(v, list):
            count += len(v)
    return count


def _combine_risk(instability_state: Dict[str, Any], churn_state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Deterministic scoring for v1.

    Heuristics:
      - More cyclic components -> higher risk
      - More unstable modules (I > 0.8 with meaningful coupling) -> higher risk
      - High churn (added+removed) increases risk
    """
    score = 0
    notes: List[str] = []

    if instability_state.get("available"):
        stats = instability_state.get("stats", {})
        cyc = int(stats.get("cyclic_component_count", 0) or 0)
        cyc_mod = int(stats.get("cyclic_module_count", 0) or 0)

        if cyc > 0:
            score += min(30, cyc * 10)
            notes.append("cycles_present")

        if cyc_mod > 0:
            score += min(20, cyc_mod * 2)
            notes.append("cyclic_modules_present")

        modules = instability_state.get("modules", [])
        high_unstable = 0
        for m in modules:
            i = m.get("instability")
            ce = m.get("ce", 0)
            if isinstance(i, float) and i >= 0.8 and int(ce) >= 2:
                high_unstable += 1

        if high_unstable > 0:
            score += min(30, high_unstable * 3)
            notes.append("high_instability_modules")

    churn_total = int(churn_state.get("added_count", 0) or 0) + int(churn_state.get("removed_count", 0) or 0)
    if churn_total >= 20:
        score += 20
        notes.append("high_churn")
    elif churn_total >= 10:
        score += 10
        notes.append("moderate_churn")
    elif churn_total > 0:
        score += 5
        notes.append("low_churn")

    score = max(0, min(100, score))

    if score >= 70:
        level = "high"
    elif score >= 35:
        level = "medium"
    else:
        level = "low"

    return {"score": score, "level": level, "notes": notes}