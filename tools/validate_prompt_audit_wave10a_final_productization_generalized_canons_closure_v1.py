"""Validate Wave 10A final productization/generalized-canon closure."""
from __future__ import annotations
import argparse,csv,json,re,zipfile
from pathlib import Path
from typing import Any

__all__ = ["main"]

FEATURE_ID="prompt-audit-wave10a-final-productization-generalized-canons-closure-v1"
LIB=Path("kanda_prompt_workspace/prompt_library")
CODES={
"kubernetes_deployment_operations":"KPR-11-001","productization_readiness_roadmap":"KPR-11-002",
"professional_ai_assisted_engineering_framework":"KPR-11-003","professional_infrastructure_roadmap":"KPR-11-004",
"python_lifecycle_versioning_deprecation":"KPR-11-005","python_site_reliability_engineering":"KPR-11-006",
"error_memory_active_ready_correction_blueprint":"KPR-12-002","error_memory_active_ready_json_template":"KPR-12-003",
"error_memory_model_template":"KPR-12-004","data_transform_pipeline_invariants":"KPR-12-009",
"desktop_help_document_layout_canon":"KPR-12-010","domain_decision_table_template":"KPR-12-011",
"plugin_package_import_canon":"KPR-12-012","shared_visual_render_engine_canon":"KPR-12-013",
"transform_resolver_architecture_contract":"KPR-12-014"}
CATEGORIES={pid:("11_productization_and_release_readiness" if code.startswith("KPR-11") else "12_generalized_project_canons") for pid,code in CODES.items()}
DEPRECATED={"productization_readiness_roadmap","professional_infrastructure_roadmap"}
MARKERS={
"kubernetes_deployment_operations":("Kubernetes Secrets as base64-encoded","immutable image digests","rollback does not automatically reverse database migrations"),
"professional_ai_assisted_engineering_framework":("thin, non-authoritative","smallest current owner","source-write authorization"),
"python_lifecycle_versioning_deprecation":("PEP 440","Semantic Versioning","public compatibility surface"),
"python_site_reliability_engineering":("allowed bad events","k6","Bottleneck NumPy library"),
"data_transform_pipeline_invariants":("incremental and streaming","transform-plan identity","nondeterminism"),
"desktop_help_document_layout_canon":("KANDA desktop-help","Do not store backup snapshots inside ACTIVE_PROMPTS","visual quality or no-overflow"),
"domain_decision_table_template":("stable rule ID","mutual exclusivity","decision trace"),
"error_memory_active_ready_correction_blueprint":("models.py","machine authority","does not memorize"),
"error_memory_active_ready_json_template":("marker-wrapped output envelope","does not define the authoritative field schema"),
"error_memory_model_template":("application schema wins","current machine authority"),
"plugin_package_import_canon":("traversal","Unsigned or unknown-publisher","installation, enablement and execution"),
"shared_visual_render_engine_canon":("one canonical visual semantic contract","stable visual IDs","Accessibility semantics"),
"transform_resolver_architecture_contract":("side-effect-free","RESOLVED, UNSUPPORTED, CONFLICT, AMBIGUOUS, INVALID and STALE","Do not execute operations")}

def load_json(p:Path)->dict[str,Any]:
 d=json.loads(p.read_text(encoding="utf-8-sig"));
 if not isinstance(d,dict): raise AssertionError("JSON root: "+str(p))
 return d

def fm(text:str)->dict[str,str]:
 m=re.match(r"\A---\n(.*?)\n---\n",text,re.S)
 if not m: raise AssertionError("Missing frontmatter")
 out={}
 for line in m.group(1).splitlines():
  if ":" in line:
   k,v=line.split(":",1); out[k.strip()]=v.strip()
 return out

def main(root:Path)->None:
 for pid,code in CODES.items():
  cat=CATEGORIES[pid]; p=root/LIB/"ACTIVE_PROMPTS"/cat/(pid+".md"); mp=root/LIB/"METADATA"/(pid+".meta.json")
  text=p.read_text(encoding="utf-8-sig"); meta=load_json(mp); front=fm(text)
  if front.get("prompt_id")!=pid or front.get("prompt_code")!=code: raise AssertionError("Identity: "+pid)
  for k,v in (("prompt_id",pid),("prompt_code",code),("category",cat),("version","2.0.0"),("source_stage",FEATURE_ID),("updated_for",FEATURE_ID)):
   if str(meta.get(k) or "")!=v: raise AssertionError("Metadata "+k+": "+pid)
  if meta.get("required_companion_prompts")!=[]: raise AssertionError("Forced companion: "+pid)
  if pid in DEPRECATED:
   if meta.get("status")!="deprecated" or meta.get("load_type")!="never" or meta.get("trigger_phrases")!=[]: raise AssertionError("Deprecation: "+pid)
   if "Global active route: `NO`" not in text: raise AssertionError("Tombstone marker: "+pid)
  for marker in MARKERS.get(pid,()):
   if marker not in text: raise AssertionError("Marker "+pid+": "+marker)
 print("WAVE10A_PROMPT_METADATA_ALIGNMENT: PASS")
 for name in ("desktop_help_document_layout_canon.backup_20260620_before_1_5_strict_books_summary_cartoon.md","desktop_help_document_layout_canon.backup_20260620_before_2_1.md"):
  if (root/LIB/"ACTIVE_PROMPTS/12_generalized_project_canons"/name).exists(): raise AssertionError("Active backup remains: "+name)
 print("WAVE10A_DESKTOP_HELP_BACKUP_RETIREMENT: PASS")
 for rel in ("kanda_reasoner_app/error_memory/models.py","kanda_reasoner_app/error_memory/schema.py","kanda_reasoner_app/error_memory/intake_json_parser.py"):
  if not (root/rel).is_file(): raise AssertionError("Error Memory owner missing: "+rel)
 print("WAVE10A_ERROR_MEMORY_MACHINE_AUTHORITY: PASS")
 nav=load_json(root/LIB/"ROUTING/prompt_navigation_index.json"); entries={e["prompt_id"]:e for e in nav.get("entries") or []}
 for pid,code in CODES.items():
  e=entries.get(pid)
  if not isinstance(e,dict) or e.get("prompt_code")!=code: raise AssertionError("Route identity: "+pid)
  if e.get("required_companion_prompts")!=[]: raise AssertionError("Route companion: "+pid)
  if pid in DEPRECATED and (e.get("status")!="deprecated" or e.get("load_type")!="never"): raise AssertionError("Route deprecation: "+pid)
 print("WAVE10A_ROUTING_COMPLETENESS: PASS")
 active_nav=(root/LIB/"ACTIVE_PROMPTS/02_prompt_routing_and_indexing/prompt_navigation_index.md").read_text(encoding="utf-8-sig")
 for marker in ("Wave 10A final prompt-audit closure routes","KPR-11-006","KPR-12-014","119-prompt program"):
  if marker not in active_nav: raise AssertionError("Navigation marker: "+marker)
 sub=(root/LIB/"ACTIVE_PROMPTS/02_prompt_routing_and_indexing/prompt_substitution_map.md").read_text(encoding="utf-8-sig")
 for marker in ("professional_infrastructure_roadmap","KPR-12-009","KPR-12-014"):
  if marker not in sub: raise AssertionError("Substitution marker: "+marker)
 print("WAVE10A_OWNER_BOUNDARIES: PASS")
 startup=root.parent/(root.name+"_show_project_to_AI")/"first_prompt_files/first_prompts_to_ai.zip"
 if startup.is_file():
  with zipfile.ZipFile(startup) as z: names=set(z.namelist())
  for pid in CODES:
   if any(name.endswith("/"+pid+".md") or name==pid+".md" for name in names): raise AssertionError("Startup promotion: "+pid)
 print("WAVE10A_NO_STARTUP_PROMOTION: PASS")
 print("WAVE10A_NO_FORCED_COMPANIONS: PASS")
 print("WAVE10A_FINAL_PRODUCTIZATION_GENERALIZED_CANONS_CLOSURE_REGRESSION_SET: PASS")
 print("VALIDATION OK: "+FEATURE_ID)
 print("STATUS: IN_SYNC")
if __name__=="__main__":
 ap=argparse.ArgumentParser(); ap.add_argument("--project-root",default="."); a=ap.parse_args(); main(Path(a.project_root).resolve())
