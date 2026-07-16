"""Support static evidence collection for Project Reasoner."""

from __future__ import annotations

from collections import Counter


def _safe_list(value: object) -> list:
    if isinstance(value, list):
        return value
    return []


def build_module_centrality_index(import_graph: dict, call_edges: list[dict], symbol_index: dict) -> dict:
    module_scores: dict[str, dict] = {}

    for module_name, imports in import_graph.items():
        entry = module_scores.setdefault(
            module_name,
            {
                "imports_out": 0,
                "imports_in": 0,
                "calls_out": 0,
                "calls_in": 0,
                "score": 0,
            },
        )
        entry["imports_out"] = len(_safe_list(imports))

    for module_name, imports in import_graph.items():
        for imported_module in _safe_list(imports):
            if imported_module in module_scores:
                module_scores.setdefault(
                    imported_module,
                    {
                        "imports_out": 0,
                        "imports_in": 0,
                        "calls_out": 0,
                        "calls_in": 0,
                        "score": 0,
                    },
                )
                module_scores[imported_module]["imports_in"] += 1

    symbol_to_module: dict[str, str] = {}
    for symbol_name, meta in symbol_index.items():
        if isinstance(meta, dict):
            file_path = str(meta.get("file", ""))
            module_name = file_path[:-3].replace("/", ".") if file_path.endswith(".py") else file_path
            symbol_to_module[symbol_name] = module_name

    for edge in _safe_list(call_edges):
        if not isinstance(edge, dict):
            continue

        from_symbol = str(edge.get("from_symbol", ""))
        to_call = str(edge.get("to_call", ""))

        from_module = symbol_to_module.get(from_symbol, "")
        to_module = symbol_to_module.get(to_call, "")

        if from_module:
            module_scores.setdefault(
                from_module,
                {
                    "imports_out": 0,
                    "imports_in": 0,
                    "calls_out": 0,
                    "calls_in": 0,
                    "score": 0,
                },
            )
            module_scores[from_module]["calls_out"] += 1

        if to_module:
            module_scores.setdefault(
                to_module,
                {
                    "imports_out": 0,
                    "imports_in": 0,
                    "calls_out": 0,
                    "calls_in": 0,
                    "score": 0,
                },
            )
            module_scores[to_module]["calls_in"] += 1

    for module_name, metrics in module_scores.items():
        metrics["score"] = (
            metrics["imports_out"]
            + metrics["imports_in"]
            + metrics["calls_out"]
            + metrics["calls_in"]
        )

    return dict(sorted(module_scores.items(), key=lambda item: item[1]["score"], reverse=True))


def build_symbol_centrality_index(call_edges: list[dict]) -> dict:
    outgoing = Counter()
    incoming = Counter()

    for edge in _safe_list(call_edges):
        if not isinstance(edge, dict):
            continue

        from_symbol = str(edge.get("from_symbol", ""))
        to_call = str(edge.get("to_call", ""))

        if from_symbol:
            outgoing[from_symbol] += 1
        if to_call:
            incoming[to_call] += 1

    all_symbols = sorted(set(outgoing.keys()) | set(incoming.keys()))
    output: dict[str, dict] = {}

    for symbol_name in all_symbols:
        calls_out = outgoing.get(symbol_name, 0)
        calls_in = incoming.get(symbol_name, 0)
        output[symbol_name] = {
            "calls_out": calls_out,
            "calls_in": calls_in,
            "score": calls_out + calls_in,
        }

    return dict(sorted(output.items(), key=lambda item: item[1]["score"], reverse=True))


def build_top_project_hotspots(
    module_centrality_index: dict,
    symbol_centrality_index: dict,
    limit: int = 20,
) -> dict:
    top_modules = []
    top_symbols = []

    for module_name, metrics in list(module_centrality_index.items())[:limit]:
        top_modules.append(
            {
                "module": module_name,
                "score": metrics.get("score", 0),
            }
        )

    for symbol_name, metrics in list(symbol_centrality_index.items())[:limit]:
        top_symbols.append(
            {
                "symbol": symbol_name,
                "score": metrics.get("score", 0),
            }
        )

    return {
        "top_modules": top_modules,
        "top_symbols": top_symbols,
    }