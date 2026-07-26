# project-path: tools/validate_project_structure_3d_project_support_boundary_v1.py
"""Validate Project Structure 3D Tool/Project Support ownership boundaries."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from project_structure_3d_test_environment import (
    environment_snapshot,
    isolated_project_fixture,
    isolated_show_project_environment,
)
from project_structure_3d_v1c_fixture import write_semantic_complete_json

FEATURE_ID = "project-structure-3d-project-support-boundary-v1"


def require(condition: bool, message: str) -> None:
    """Raise one deterministic boundary error."""
    if not condition:
        raise AssertionError(message)


def write_in_source_decoy(project_root: Path) -> Path:
    """Write evidence that must never be consumed from selected Project source."""
    folder = project_root / "project_analysis_evidence"
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / (project_root.name + "__complete.json")
    payload = {
        "source_file_index": {
            "decoy/wrong_owner.py": {
                "file": "decoy/wrong_owner.py",
                "module_name": "decoy.wrong_owner",
                "line_count": 1,
                "symbol_count": 0,
            }
        },
        "symbol_index": {},
        "primary_definition_index": {},
        "import_graph": {},
    }
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def validate_runtime_boundary(root: Path) -> None:
    """Prove dynamic support ownership and rejection of in-source evidence."""
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    from kanda_reasoner_app.project_analysis_evidence_paths import (
        project_analysis_evidence_root,
    )
    from kanda_reasoner_app.project_structure_visualizer.complete_json_artifacts import (
        complete_json_artifact_dir,
    )
    from kanda_reasoner_app.project_structure_visualizer.graph_snapshot_builder import (
        build_project_graph_snapshot,
    )

    ambient = environment_snapshot()
    with isolated_show_project_environment():
        with isolated_project_fixture(
            "kanda_visualizer_boundary_"
        ) as (project_root, support_root):
            resolved_support = project_analysis_evidence_root(project_root)
            complete_dir = complete_json_artifact_dir(project_root)
            require(resolved_support == support_root, "Project Support root mismatch")
            require(support_root != project_root, "Project Support collapsed into Project source")
            require(
                not support_root.is_relative_to(project_root),
                "Project Support is nested inside Project source",
            )
            require(
                complete_dir.is_relative_to(support_root),
                "complete JSON directory escaped Project Support",
            )
            decoy = write_in_source_decoy(project_root)
            evidence = write_semantic_complete_json(project_root)
            require(decoy.is_relative_to(project_root), "decoy is not in Project source")
            require(evidence.is_relative_to(support_root), "evidence is not in Project Support")

            build = build_project_graph_snapshot(project_root)
            require(not build.is_fixture, "Project Support evidence unexpectedly fell back")
            node_ids = {str(node.get("id")) for node in build.snapshot["nodes"]}
            require("module:app/child.py" in node_ids, "Project Support evidence was not read")
            require(
                "module:decoy/wrong_owner.py" not in node_ids,
                "in-source evidence leaked into the graph",
            )
            provenance = build.snapshot.get("source_provenance", {})
            require(provenance.get("authoritative") is False, "generated evidence authority")
            require(
                provenance.get("support_owner") == "project_support.project_structure_3d_json",
                "Project Structure 3D JSON owner missing",
            )
            evidence.unlink()
            fallback = build_project_graph_snapshot(project_root)
            require(fallback.is_fixture, "in-source decoy was used as fallback evidence")
            require(
                "Project Support" in fallback.fallback_reason,
                "fallback reason did not identify Project Support",
            )
    require(environment_snapshot() == ambient, "caller environment was not restored")
    print("PROJECT_STRUCTURE_3D_TOOL_CODE_OWNER: PASS")
    print("PROJECT_STRUCTURE_3D_PROJECT_SUPPORT_DATA_OWNER: PASS")
    print("PROJECT_STRUCTURE_3D_INDEPENDENT_JSON_OWNER: PASS")
    print("PROJECT_STRUCTURE_3D_NO_IN_SOURCE_EVIDENCE_FALLBACK: PASS")
    print("PROJECT_STRUCTURE_3D_GENERATED_EVIDENCE_NON_AUTHORITATIVE: PASS")


def validate_source_contract(root: Path) -> None:
    """Validate the runtime builder calls the public Project Support owners."""
    path = root / "kanda_reasoner_app/project_structure_visualizer/graph_snapshot_builder.py"
    source = path.read_text(encoding="utf-8", errors="strict")
    require("resolve_complete_json_evidence" in source, "complete JSON resolver missing")
    require("project_analysis_evidence_root" in source, "support containment owner missing")
    require(
        '"support_owner": "project_support.project_structure_3d_json"' in source,
        "independent Project Structure 3D owner missing",
    )
    require(
        'root / "project_analysis_evidence"' not in source,
        "in-source evidence path remains in runtime builder",
    )
    print("PROJECT_STRUCTURE_3D_PROJECT_TOOL_BOUNDARY_SOURCE: PASS")


def main() -> int:
    """Run the focused boundary validator."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    args = parser.parse_args()
    root = Path(args.root).resolve()
    validate_source_contract(root)
    validate_runtime_boundary(root)
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
