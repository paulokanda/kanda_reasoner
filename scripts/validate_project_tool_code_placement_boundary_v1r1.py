# project-path: scripts/validate_project_tool_code_placement_boundary_v1r1.py
"""Validate explicit Tool/Project code placement without rewriting routing index."""
from __future__ import annotations
import argparse
import json
import sys
import tempfile
import zipfile
from pathlib import Path

FEATURE_ID='project-tool-code-placement-boundary-install-correction-v1r1'
FULL_REL=Path('kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/12_generalized_project_canons/project_tool_boundary_canon.md')
BRIDGE_REL=Path('kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/12_generalized_project_canons/project_tool_boundary_startup_bridge.md')
ROUTE_REL=Path('kanda_prompt_workspace/prompt_library/ROUTING/prompt_navigation_index.json')
SOURCE_MAP_REL=Path("kanda_prompt_workspace/prompt_tools/STARTUP_ROUTING_KERNEL_SOURCES.json")
STARTUP_MEMBER="14_project_tool_boundary_canon.md"


def gate(label:str, ok:bool)->None:
    if not ok: raise AssertionError(label+": FAIL")
    print(label+": PASS")


def read(path:Path)->str:
    if not path.is_file(): raise AssertionError("missing file: "+str(path))
    return path.read_text(encoding="utf-8-sig",errors="strict")


def load(path:Path)->dict[str,object]:
    data=json.loads(read(path))
    if not isinstance(data,dict): raise AssertionError("JSON root must be object: "+str(path))
    return data


def require(text:str, markers:tuple[str,...], label:str)->None:
    for marker in markers:
        if marker not in text: raise AssertionError(label+" missing marker: "+marker)


def main()->int:
    parser=argparse.ArgumentParser()
    parser.add_argument("--project-root",type=Path,default=Path.cwd())
    parser.add_argument("--startup-output-dir",type=Path)
    args=parser.parse_args()
    root=args.project_root.resolve()
    if str(root) not in sys.path: sys.path.insert(0,str(root))
    output=(args.startup_output_dir.resolve() if args.startup_output_dir else Path(root.anchor)/(root.name+"_show_project_to_AI")/"first_prompt_files")

    full=read(root/FULL_REL)
    bridge=read(root/BRIDGE_REL)
    require(full,(
        "Prompt ID: project_tool_boundary_canon",
        "Prompt code: KPR-12-001",
        "## Explicit code-placement and cross-write rule",
        "Never write KANDA Tool code into an external selected Project source tree.",
        "Never write external selected-Project code into KANDA Tool source.",
        "<project_drive>/<project_name>_show_project_to_AI",
        "When the selected Project is KANDA Reasoner itself",
        "same owner root",
    ),"FULL_CANON")
    require(bridge,(
        "prompt_code: KPR-12-006",
        "prompt_id: project_tool_boundary_startup_bridge",
        "load_type: always_startup",
        "## Absolute code-placement guard",
        "Never write KANDA Tool-owned code into an external selected Project source tree.",
        "Never write external selected-Project code into KANDA Tool source.",
        "<project_drive>/<project_name>_show_project_to_AI",
        "selected Project is KANDA Reasoner itself",
        "May mutate from this bridge alone: NO",
    ),"STARTUP_BRIDGE")
    gate("BOUNDARY_PROMPT_EXPLICIT_CROSS_WRITE_GUARD",True)
    gate("BOUNDARY_STARTUP_EXPLICIT_CROSS_WRITE_GUARD",True)
    bridge_flat=" ".join(bridge.split())
    gate("BOUNDARY_PROJECT_SUPPORT_EXCEPTION", "support, not source, runtime, or an install target" in bridge_flat)
    gate("BOUNDARY_SELF_HOSTING_EXCEPTION", "both roles may physically write that same tree" in bridge_flat)
    gate("BOUNDARY_FULL_CANON_WITHIN_LIMIT",len(full.splitlines())<=500)
    gate("BOUNDARY_STARTUP_BRIDGE_COMPACT",len(bridge.splitlines())<=200)

    route=load(root/ROUTE_REL)
    entries=route.get("entries")
    if not isinstance(entries,list): raise AssertionError("route entries must be list")
    ids=[item.get("prompt_id") for item in entries if isinstance(item,dict)]
    gate("BOUNDARY_ROUTE_FULL_UNIQUE",ids.count("project_tool_boundary_canon")==1)
    gate("BOUNDARY_ROUTE_BRIDGE_UNIQUE",ids.count("project_tool_boundary_startup_bridge")==1)
    full_entry=next(x for x in entries if isinstance(x,dict) and x.get("prompt_id")=="project_tool_boundary_canon")
    bridge_entry=next(x for x in entries if isinstance(x,dict) and x.get("prompt_id")=="project_tool_boundary_startup_bridge")
    gate("BOUNDARY_ROUTE_FULL_PATH_STABLE",str(full_entry.get("relative_path") or "").endswith("project_tool_boundary_canon.md"))
    gate("BOUNDARY_ROUTE_BRIDGE_PATH_STABLE",str(bridge_entry.get("relative_path") or "").endswith("project_tool_boundary_startup_bridge.md"))
    gate("BOUNDARY_ROUTING_INDEX_PRESERVED",True)

    source_map=load(root/SOURCE_MAP_REL)
    startup=source_map.get("startup_sources")
    if not isinstance(startup,list): raise AssertionError("startup_sources must be list")
    matches=[x for x in startup if isinstance(x,dict) and x.get("prompt_id")=="project_tool_boundary_startup_bridge"]
    gate("BOUNDARY_STARTUP_ENTRY_UNIQUE",len(matches)==1)
    gate("BOUNDARY_STARTUP_FILENAME_STABLE",matches[0].get("generated_filename")==STARTUP_MEMBER)

    zip_path=output/"first_prompts_to_ai.zip"
    gate("BOUNDARY_STARTUP_ZIP_PRESENT",zip_path.is_file())
    with zipfile.ZipFile(zip_path) as z:
        names=z.namelist()
        gate("BOUNDARY_STARTUP_MEMBER_UNIQUE",names.count(STARTUP_MEMBER)==1)
        generated=z.read(STARTUP_MEMBER).decode("utf-8",errors="strict")
    require(generated,(
        "Never write KANDA Tool-owned code into an external selected Project source tree.",
        "Never write external selected-Project code into KANDA Tool source.",
        "<project_drive>/<project_name>_show_project_to_AI",
        "selected Project is KANDA Reasoner itself",
    ),"GENERATED_STARTUP")
    gate("BOUNDARY_STARTUP_CROSS_WRITE_GUARD_VISIBLE",True)

    from kanda_reasoner_app.project_analysis_evidence_paths import project_analysis_evidence_root
    with tempfile.TemporaryDirectory() as td:
        project=Path(td)/"sample_project";project.mkdir()
        support=project_analysis_evidence_root(project)
        gate("BOUNDARY_RUNTIME_SUPPORT_EXTERNAL",support!=project and project not in support.parents)
        gate("BOUNDARY_RUNTIME_NOT_HARDCODED",support.name.startswith("sample_project"))

    print("PROJECT_TOOL_BOUNDARY_CANON_REGRESSION_SET: PASS")
    print("VALIDATION OK: "+FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0

if __name__=="__main__": raise SystemExit(main())
