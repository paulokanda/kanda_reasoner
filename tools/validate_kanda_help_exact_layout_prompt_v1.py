"""Validate the KANDA desktop help exact-layout prompt registration."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
FEATURE_ID = "kanda-help-exact-layout-prompt-v1"
PID = "kanda_desktop_help_exact_layout_blueprint"
CODE = "KPR-12-015"

def req(ok: bool, msg: str) -> None:
    if not ok: raise AssertionError(msg)

def load(path: Path): return json.loads(path.read_text(encoding="utf-8-sig"))

def main() -> int:
    ap=argparse.ArgumentParser(); ap.add_argument("--root",type=Path,required=True); ns=ap.parse_args(); root=ns.root.resolve()
    lib=root/"kanda_prompt_workspace/prompt_library"
    prompt=lib/f"ACTIVE_PROMPTS/12_generalized_project_canons/{PID}.md"
    meta=lib/f"METADATA/{PID}.meta.json"
    req(prompt.is_file(),"new prompt missing"); req(meta.is_file(),"new metadata missing")
    text=prompt.read_text(encoding="utf-8")
    for token in (CODE,"Exact HTML skeleton","book_help.css","QWebEngineView","QTextBrowser","Reuse unchanged PNG archives"):
        req(token in text,"prompt contract missing: "+token)
    md=load(meta); req(md["prompt_code"]==CODE,"prompt code mismatch"); req(md["required_companion_prompts"]==["desktop_help_document_layout_canon"],"companion mismatch")
    owner=(lib/"ACTIVE_PROMPTS/12_generalized_project_canons/desktop_help_document_layout_canon.md").read_text(encoding="utf-8")
    req(PID in owner and CODE in owner,"owner bridge missing")
    owner_meta=load(lib/"METADATA/desktop_help_document_layout_canon.meta.json")
    req(PID in owner_meta.get("required_companion_prompts",[]),"owner metadata bridge missing")
    groups=load(lib/"GROUPS/PROMPT_GROUPS_DRAFT.json")
    group=next(g for g in groups["groups"] if g["group_id"]=="12_generalized_project_canons")
    req(PID in group["prompt_ids"],"canonical group registration missing"); req(group["prompt_count"]==len(group["prompt_ids"]),"group count mismatch")
    mirror=load(root/"kanda_reasoner_app/prompt_library/groups/PROMPT_GROUPS.json")
    mg=next(g for g in mirror["groups"] if g["group_id"]=="12_generalized_project_canons")
    req(group==mg,"group mirror mismatch")
    nav=load(lib/"ROUTING/prompt_navigation_index.json")
    matches=[e for e in nav["entries"] if e.get("prompt_id")==PID]
    req(len(matches)==1,"navigation registration must be unique")
    req(nav["prompt_count"]==len(nav["entries"]),"navigation count mismatch")
    folder=(lib/"ACTIVE_PROMPTS/12_generalized_project_canons/_FOLDER_ASSIMILATION.md").read_text(encoding="utf-8")
    req(CODE in folder and PID in folder,"folder card registration missing")
    subst=(lib/"ACTIVE_PROMPTS/02_prompt_routing_and_indexing/prompt_substitution_map.md").read_text(encoding="utf-8")
    req(CODE in subst and PID in subst,"routing bridge missing")
    print("HELP_EXACT_LAYOUT_PROMPT_SOURCE: PASS")
    print("HELP_EXACT_LAYOUT_COMPANION_BRIDGE: PASS")
    print("PROMPT_LIBRARY_REGISTRATION: PASS")
    print("PROMPT_GROUP_MIRROR: PASS")
    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")
    return 0
if __name__=="__main__": raise SystemExit(main())
