# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/grimp_graph_probe.py
"""Adapter-side Grimp probe that emits one deterministic JSON topology snapshot."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

__all__ = ["build_probe_payload", "main", "validate_probe_payload"]


def build_probe_payload(
    *,
    root: str | Path,
    package_name: str,
    cache_dir: str | Path | None,
    exclude_type_checking_imports: bool,
) -> dict[str, object]:
    """Build a deterministic graph payload using Grimp inside analyzer runtime."""
    project_root = Path(root).expanduser().resolve(strict=True)
    if not project_root.is_dir():
        raise ValueError("GRIMP_PROBE_ROOT_NOT_DIRECTORY")
    package = str(package_name or "").strip()
    if not package:
        raise ValueError("GRIMP_PROBE_PACKAGE_EMPTY")
    project_root_text = str(project_root)
    if project_root_text not in sys.path:
        sys.path.insert(0, project_root_text)

    import grimp

    resolved_cache = None
    if cache_dir is not None:
        cache_path = Path(cache_dir).expanduser().resolve(strict=False)
        cache_path.mkdir(parents=True, exist_ok=True)
        resolved_cache = str(cache_path)
    graph = grimp.build_graph(
        package,
        include_external_packages=False,
        exclude_type_checking_imports=bool(exclude_type_checking_imports),
        cache_dir=resolved_cache,
    )
    modules = tuple(sorted(str(item) for item in graph.modules))
    edges: list[dict[str, str]] = []
    for importer in modules:
        imported_modules = graph.find_modules_directly_imported_by(importer)
        for imported in sorted(str(item) for item in imported_modules):
            edges.append({"importer": importer, "imported": imported})
    cycle_breakers = [
        {"importer": importer, "imported": imported}
        for importer, imported in sorted(graph.nominate_cycle_breakers(package))
    ]
    return {
        "schema_version": "1.0",
        "engine": "grimp",
        "package_name": package,
        "module_count": len(modules),
        "edge_count": len(edges),
        "modules": list(modules),
        "edges": edges,
        "cycle_breakers": cycle_breakers,
        "exclude_type_checking_imports": bool(exclude_type_checking_imports),
    }


def validate_probe_payload(payload: dict[str, object]) -> tuple[str, ...]:
    """Return deterministic blockers for one generated topology payload."""
    blockers: list[str] = []
    if payload.get("schema_version") != "1.0":
        blockers.append("GRIMP_PROBE_SCHEMA_VERSION_INVALID")
    if payload.get("engine") != "grimp":
        blockers.append("GRIMP_PROBE_ENGINE_INVALID")
    if not str(payload.get("package_name") or "").strip():
        blockers.append("GRIMP_PROBE_PACKAGE_EMPTY")
    modules = payload.get("modules")
    edges = payload.get("edges")
    cycle_breakers = payload.get("cycle_breakers")
    if not isinstance(modules, list):
        blockers.append("GRIMP_PROBE_MODULES_NOT_LIST")
    if not isinstance(edges, list):
        blockers.append("GRIMP_PROBE_EDGES_NOT_LIST")
    if not isinstance(cycle_breakers, list):
        blockers.append("GRIMP_PROBE_CYCLE_BREAKERS_NOT_LIST")
    if isinstance(edges, list):
        for index, item in enumerate(edges):
            if not isinstance(item, dict):
                blockers.append(f"GRIMP_PROBE_EDGE_{index}_NOT_OBJECT")
                continue
            if not str(item.get("importer") or "").strip():
                blockers.append(f"GRIMP_PROBE_EDGE_{index}_IMPORTER_EMPTY")
            if not str(item.get("imported") or "").strip():
                blockers.append(f"GRIMP_PROBE_EDGE_{index}_IMPORTED_EMPTY")
    return tuple(sorted(set(blockers)))


def main(argv: list[str] | None = None) -> int:
    """Parse bounded probe arguments and emit canonical JSON to stdout."""
    parser = argparse.ArgumentParser(description="Emit Grimp topology JSON evidence.")
    parser.add_argument("--root", required=True)
    parser.add_argument("--package", required=True)
    parser.add_argument("--cache-dir", default="")
    parser.add_argument(
        "--exclude-type-checking-imports",
        action="store_true",
    )
    args = parser.parse_args(argv)
    payload = build_probe_payload(
        root=args.root,
        package_name=args.package,
        cache_dir=args.cache_dir or None,
        exclude_type_checking_imports=args.exclude_type_checking_imports,
    )
    blockers = validate_probe_payload(payload)
    if blockers:
        raise ValueError("GRIMP_PROBE_PAYLOAD_INVALID:" + "|".join(blockers))
    print(
        json.dumps(
            payload,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
