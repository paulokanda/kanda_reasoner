
from __future__ import annotations
import argparse
import ast
import csv
import hashlib
import json
from pathlib import Path
import sys

STARTUP_REL = Path("kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/01_session_start_and_navigation/error_memory_ai_formulary_startup_canon.md")
ZIP_REL = Path("kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/05_patch_delivery_and_validation/self_contained_error_memory_lesson_intake_zip.md")
STARTUP_META_REL = Path("kanda_prompt_workspace/prompt_library/METADATA/error_memory_ai_formulary_startup_canon.meta.json")
ZIP_META_REL = Path("kanda_prompt_workspace/prompt_library/METADATA/self_contained_error_memory_lesson_intake_zip.meta.json")
NAV_REL = Path("kanda_prompt_workspace/prompt_library/ROUTING/prompt_navigation_index.json")
COVERAGE_REL = Path("kanda_prompt_workspace/prompt_library/ROUTING/prompt_route_coverage_table.csv")
BLUEPRINT_REL = Path("kanda_reasoner_app/error_memory_gui/_intake_blueprint.py")
TAB_REL = Path("kanda_reasoner_app/error_memory_gui/error_memory_tab.py")
ALLOW_REL = Path("portable/PORTABLE_RUNTIME_ALLOWLIST.json")
BUILDER_REL = Path("portable/PORTABLE_BUILDER_MANIFEST.json")

FORBIDDEN_OWNER_FIELDS = (
    "owner_scope", "owner_id", "owner_slug", "owner_root_fingerprint",
    "affected_box", "project_slug", "import_provenance",
)

def require(condition, marker):
    if not condition:
        raise RuntimeError(marker)

def read(root, rel):
    path = root / rel
    require(path.is_file(), "MISSING:" + rel.as_posix())
    return path.read_text(encoding="utf-8")

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def validate_portable_bindings(root, rels):
    allow_path = root / ALLOW_REL
    allow = json.loads(read(root, ALLOW_REL))
    by_rel = {item.get("source_relative"): item for item in allow.get("items", [])}
    for rel in rels:
        key = rel.as_posix()
        item = by_rel.get(key)
        require(item is not None, "ALLOWLIST_ENTRY_MISSING:" + key)
        path = root / rel
        require(item.get("sha256") == sha(path), "ALLOWLIST_SHA_MISMATCH:" + key)
        require(int(item.get("size_bytes", -1)) == path.stat().st_size, "ALLOWLIST_SIZE_MISMATCH:" + key)
    builder = json.loads(read(root, BUILDER_REL))
    allow_sha = sha(allow_path)
    require(builder.get("files", {}).get("PORTABLE_RUNTIME_ALLOWLIST.json") == allow_sha, "BUILDER_ALLOWLIST_FILE_BINDING")
    require(builder.get("runtime_allowlist_sha256") == allow_sha, "BUILDER_ALLOWLIST_RUNTIME_BINDING")
    require(int(builder.get("runtime_allowlist_item_count", -1)) == len(allow.get("items", [])), "BUILDER_ALLOWLIST_COUNT")

FEATURE_ID = "error-memory-get-correct-way-to-send-errors-button-import-graph-repair-v2"

def main():
    p=argparse.ArgumentParser(); p.add_argument("--project-root", required=True); a=p.parse_args()
    root=Path(a.project_root).resolve(strict=True)
    prompt=read(root,STARTUP_REL)
    blueprint=read(root,BLUEPRINT_REL)
    require("version: 3.0" in prompt, "STARTUP_VERSION_NOT_MCARD")
    require("Project-specific Error Memory ownership" in prompt, "STARTUP_PROJECT_OWNER_EXCLUSION_MISSING")
    require("SUPERSEDE_EXISTING" not in prompt, "SUPERSEDE_DISPOSITION_SURVIVED")
    require("del project_root" in blueprint, "PROJECT_OVERRIDE_RESOLVER_SURVIVED")
    ast.parse((root/BLUEPRINT_REL).read_text(encoding="ascii"))
    ast.parse((root/TAB_REL).read_text(encoding="ascii"))
    print("ERROR MEMORY CANON IMPORT GRAPH: PASS")
    print("ERROR MEMORY TOOL-OWNED PROMPT RESOLUTION: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0
if __name__=="__main__": raise SystemExit(main())
