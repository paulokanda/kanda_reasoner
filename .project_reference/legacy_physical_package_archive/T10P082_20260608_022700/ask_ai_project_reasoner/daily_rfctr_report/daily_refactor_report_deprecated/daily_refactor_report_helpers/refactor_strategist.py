from dev_tools.daily_refactor_report_helpers.analysis_contracts import AnalysisInputs, AnalyzerResult


def _safe_int(x, default=0):
    try:
        return int(x)
    except Exception:
        return default


def analyze_refactor_strategy(inputs: AnalysisInputs) -> AnalyzerResult:
    snapshot = inputs.snapshot or {}
    churn = inputs.symbol_churn or {}
    dep_graph = inputs.dependency_graph or {}

    symbol_count_by_module = snapshot.get("symbols_by_module", {})
    centrality = dep_graph.get("centrality", {})
    churn_by_module = churn.get("by_module", {})

    overloaded = []
    unstable_central = []

    for module, count in symbol_count_by_module.items():
        count = _safe_int(count)

        if count > 50:  # heuristic threshold
            overloaded.append(module)

    for module, churn_data in churn_by_module.items():
        module_churn = _safe_int(churn_data.get("added", 0)) + _safe_int(churn_data.get("removed", 0))
        cent = centrality.get(module, {}).get("total_degree", 0)

        if module_churn > 5 and cent > 5:
            unstable_central.append(module)

    optimization_priority = "low"
    if len(unstable_central) > 3:
        optimization_priority = "high"
    elif len(overloaded) > 3:
        optimization_priority = "medium"

    payload = {
        "overloaded_modules": sorted(overloaded),
        "unstable_central_modules": sorted(unstable_central),
        "optimization_priority": optimization_priority,
        "metrics_used": {
            "symbol_density_threshold": 50,
            "centrality_threshold": 5,
            "churn_threshold": 5
        }
    }

    return AnalyzerResult(
        name="refactor_strategist",
        version="1.0",
        result=payload
    )