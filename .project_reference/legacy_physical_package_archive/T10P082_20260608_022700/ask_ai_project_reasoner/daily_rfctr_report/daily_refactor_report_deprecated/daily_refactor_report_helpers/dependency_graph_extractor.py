import ast
from pathlib import Path
from typing import Dict, List, Set


def _module_name_from_path(root: Path, file_path: Path) -> str:
    rel = file_path.relative_to(root)
    parts = list(rel.with_suffix("").parts)
    return ".".join(parts)


def _extract_imports(file_path: Path) -> List[str]:
    try:
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            tree = ast.parse(f.read(), filename=str(file_path))
    except Exception:
        return []

    imports = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append(node.module)

    return imports


# ==========================================================
# Cycle Detection (DFS)
# ==========================================================

def _detect_cycles(graph: Dict[str, List[str]]) -> List[List[str]]:
    visited = set()
    stack = set()
    cycles = []

    def dfs(node, path):
        visited.add(node)
        stack.add(node)

        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                dfs(neighbor, path + [neighbor])
            elif neighbor in stack:
                cycles.append(path + [neighbor])

        stack.remove(node)

    for node in graph:
        if node not in visited:
            dfs(node, [node])

    return cycles


# ==========================================================
# Strongly Connected Components (Tarjan)
# ==========================================================

def _tarjan_scc(graph: Dict[str, List[str]]) -> List[List[str]]:
    index = 0
    stack = []
    indices = {}
    lowlink = {}
    on_stack = set()
    sccs = []

    def strongconnect(v):
        nonlocal index
        indices[v] = index
        lowlink[v] = index
        index += 1
        stack.append(v)
        on_stack.add(v)

        for w in graph.get(v, []):
            if w not in indices:
                strongconnect(w)
                lowlink[v] = min(lowlink[v], lowlink[w])
            elif w in on_stack:
                lowlink[v] = min(lowlink[v], indices[w])

        if lowlink[v] == indices[v]:
            component = []
            while True:
                w = stack.pop()
                on_stack.remove(w)
                component.append(w)
                if w == v:
                    break
            sccs.append(component)

    for v in graph:
        if v not in indices:
            strongconnect(v)

    return sccs


# ==========================================================
# Main Extractor
# ==========================================================

def extract_dependency_graph(domain_root: Path) -> Dict:
    nodes: Set[str] = set()
    edges = []

    adjacency = {}

    for file_path in domain_root.rglob("*.py"):
        if "__pycache__" in file_path.parts:
            continue

        module_name = _module_name_from_path(domain_root, file_path)
        nodes.add(module_name)

        imports = _extract_imports(file_path)

        adjacency.setdefault(module_name, [])

        for imp in imports:
            adjacency[module_name].append(imp)
            edges.append({
                "from": module_name,
                "to": imp,
                "kind": "import"
            })

    nodes_list = sorted(nodes)
    edges_sorted = sorted(edges, key=lambda e: (e["from"], e["to"]))

    # -------------------------
    # New Intelligence Layer
    # -------------------------

    cycles = _detect_cycles(adjacency)
    sccs = _tarjan_scc(adjacency)

    cyclic_components = [c for c in sccs if len(c) > 1]

    return {
        "root": str(domain_root),
        "nodes": nodes_list,
        "edges": edges_sorted,
        "cycles_detected": cycles,
        "strongly_connected_components": sccs,
        "cyclic_components": cyclic_components,
        "stats": {
            "node_count": len(nodes_list),
            "edge_count": len(edges_sorted),
            "cycle_count": len(cycles),
            "cyclic_component_count": len(cyclic_components)
        }
    }