# project-path: tools/validate_complete_engineering_review_tool_project_boundary_shield_v1.py
"""Focused bidirectional Tool/Project boundary validator for Engineering Safety."""
from __future__ import annotations
import argparse, hashlib, importlib, os, subprocess, sys, tempfile, types
from pathlib import Path
FEATURE_ID="kanda-reasoner-complete-engineering-review-tool-project-bidirectional-boundary-shield-v1"
TOUCHED={
    '_reasoner_tools_gui_engineering_safety_boundary.py': '61e7a3533334d89350ba2f6e977cf222c635d031893e6e6f2a2bd249e8f02a38',
    '_reasoner_tools_gui_engineering_safety_panel_commands.py': '0be128ee84f91e75c60954029a05252baf3d8ad1d3ecadf3429e9210c77ffa35',
    '_reasoner_tools_gui_engineering_safety_review_signals.py': '98b48ec84964e5122ba2722234682e2f04bd17b40feeb3c4ce42fabc386ac3bf',
    'reasoner_tools_gui_engineering_safety_panel.py': '7e9d83f64080f94a817b7c43a13188622461127a2b02cc16449967fcdb76b829',
}
FORBIDDEN={"reasoner_tools_gui.py","reasoner_tools_gui_engineering_safety_panel.py","build_reasoner_symbol_atlas_reports","create_engineering_safety_panel","build_engineering_safety_panel_cli_args"}
def digest(path:Path)->str:
 h=hashlib.sha256()
 with path.open("rb") as f:
  for c in iter(lambda:f.read(1024*1024),b""): h.update(c)
 return h.hexdigest()
def req(value:bool,marker:str):
 if not value: raise RuntimeError(marker+": FAIL")
 print(marker+": PASS")
def state_hash(path:Path)->str: return digest(path) if path.is_file() else "<missing>"
def tree_hash(root:Path)->str:
 h=hashlib.sha256()
 if not root.exists(): return "<missing>"
 for p in sorted(x for x in root.rglob("*") if x.is_file()):
  h.update(str(p.relative_to(root)).replace("\\","/").encode("utf-8")); h.update(p.read_bytes())
 return h.hexdigest()
def source_inventory(paths:list[Path],root:Path)->str:
 h=hashlib.sha256()
 for p in sorted(set(paths)):
  if not p.is_file(): continue
  h.update(str(p.relative_to(root)).replace("\\","/").encode("utf-8")); h.update(p.read_bytes())
 return h.hexdigest()
def import_current(tool:Path):
 tool_text=str(tool)
 sys.path[:]=[tool_text,*[p for p in sys.path if p!=tool_text]]
 boundary=importlib.import_module("_reasoner_tools_gui_engineering_safety_boundary")
 commands=importlib.import_module("_reasoner_tools_gui_engineering_safety_panel_commands")
 signals=importlib.import_module("_reasoner_tools_gui_engineering_safety_review_signals")
 panel=importlib.import_module("reasoner_tools_gui_engineering_safety_panel")
 return boundary,commands,signals,panel
def source_contract(tool:Path,boundary,commands,signals,panel):
 for rel,expected in TOUCHED.items(): req((tool/rel).is_file() and digest(tool/rel)==expected,"SOURCE_HASH:"+rel)
 print("BOUNDARY_SHIELD_TOUCHED_SOURCE_HASHES: PASS")
 for rel in TOUCHED:
  req(len((tool/rel).read_text(encoding="utf-8").splitlines())<=499,"SOURCE_MAX499:"+rel)
 print("BOUNDARY_SHIELD_MODULE_MAX_499: PASS")
 for rel in TOUCHED: compile((tool/rel).read_text(encoding="utf-8"),str(tool/rel),"exec")
 print("BOUNDARY_SHIELD_PYTHON_COMPILE: PASS")
 req(Path(__file__).resolve().is_file(),"DURABLE_BOUNDARY_VALIDATOR_PRESENT")
 collector=boundary.import_tool_module("kanda_reasoner_app.reasoner_context_collector","reasoner_context_collector")
 req(callable(getattr(collector,"collect_canonical_project_python_files",None)),"CANONICAL_PROJECT_SCOPE_PUBLIC_FACADE_PRESENT")
 names=[str(x.command_name) for x in panel.get_engineering_safety_panel_catalog()]
 req(len(names)==23 and len(set(names))==23,"COMPLETE_REVIEW_CATALOG_23_OF_23_PRESERVED")
 return collector,names
def check_args(boundary,commands,names,root:Path,prefix:str):
 context=boundary.project_command_context(root)
 original=commands._project_command_context
 commands._project_command_context=lambda _root: context
 try:
  all_args={name:list(commands._build_cli_args(name,str(root))) for name in names}
 finally:
  commands._project_command_context=original
 for name,args in all_args.items():
  joined="\n".join(map(str,args))
  tool_physical=Path(boundary.tool_root()).resolve(strict=False)
  project_physical=root.resolve(strict=False)
  if project_physical==tool_physical:
   req(True,prefix+"_SELF_HOSTING_PHYSICAL_ROOT_ALLOWED_LOGICAL_ROLE_SEPARATION:"+name)
  else:
   req(str(tool_physical).casefold() not in joined.casefold(),prefix+"_NO_ABSOLUTE_TOOL_ROOT:"+name)
  req(not(FORBIDDEN & set(map(str,args))),prefix+"_NO_TOOL_SEEDS:"+name)
  for flag in ("--target","--changed-file"):
   for i,value in enumerate(args[:-1]):
    if value==flag: req(boundary.is_within((root/args[i+1]).resolve(strict=False),root),prefix+"_TARGET_INSIDE_PROJECT:"+name+":"+flag)
 return context,all_args

def ambiguous_tool_guidance(text:str)->list[str]:
 bad=[]
 for line in text.splitlines():
  if "python kanda_reasoner_app" in line:
   bad.append(line)
  if "import reasoner_tools_gui" in line:
   bad.append(line)
  if ("kanda_reasoner_app" in line or "reasoner_tools_gui" in line) and "[KANDA TOOL EXECUTION PROVIDER]" not in line:
   if line not in bad: bad.append(line)
 return bad
def guidance_contract(tool:Path,project:Path,commands):
 sample=(
  "## Tests to run\n"
  "- python kanda_reasoner_app\\manage_architecture\\manage_architecture.py --root <PROJECT_ROOT> --validate\n"
  "- python kanda_reasoner_app\\manage_workflows\\manage_workflows.py --root \"$PROJECT_ROOT\" --validate\n"
  "- python -c \"import kanda_reasoner_app; import reasoner_tools_gui; print('import smoke ok')\"\n"
  "- project_target=kanda_plot/kanda_plot_templates.py\n"
 )
 with tempfile.TemporaryDirectory(prefix="kanda_boundary_guidance_external_") as td:
  external=Path(td).resolve()
  shielded=commands._shield_external_project_guidance(sample,str(external))
  req("python kanda_reasoner_app" not in shielded,"EXTERNAL_PROJECT_TOOL_GUIDANCE_RELATIVE_PATHS_ABSENT")
  req("import reasoner_tools_gui" not in shielded,"EXTERNAL_PROJECT_TOOL_IMPORT_SMOKE_NOT_PROJECT_LOCAL")
  provider=[line for line in shielded.splitlines() if "[KANDA TOOL EXECUTION PROVIDER]" in line]
  req(len(provider)==3 and all(str(tool) in line or "not emitted as a Project-local" in line for line in provider),"EXTERNAL_PROJECT_TOOL_GUIDANCE_EXPLICIT_PROVIDER")
  req(str(external) in provider[0] and str(external) in provider[1],"EXTERNAL_PROJECT_TOOL_GUIDANCE_TARGETS_ACTIVE_PROJECT")
  req("project_target=kanda_plot/kanda_plot_templates.py" in shielded,"PROJECT_GUIDANCE_PROJECT_CONTENT_PRESERVED")
  req(not ambiguous_tool_guidance(shielded),"PROJECT_TO_TOOL_GUIDANCE_SHADOW_ROUTE_ABSENT")
 self_hosted=commands._shield_external_project_guidance(sample,str(tool))
 req("python kanda_reasoner_app" not in self_hosted,"SELF_HOSTING_TOOL_GUIDANCE_RELATIVE_PATHS_ABSENT")
 req("import reasoner_tools_gui" not in self_hosted,"SELF_HOSTING_TOOL_IMPORT_SMOKE_NOT_PROJECT_LOCAL")
 req(self_hosted.count("[KANDA TOOL EXECUTION PROVIDER]")==3,"SELF_HOSTING_TOOL_GUIDANCE_EXPLICIT_PROVIDER")
def synthetic_contract(tool:Path,boundary,commands,signals,panel,names):
 with tempfile.TemporaryDirectory(prefix="kanda_boundary_external_") as td:
  root=Path(td).resolve(); (root/"main.py").write_text("def eeg_entry(value=None):\n    return value\n",encoding="utf-8"); (root/"pkg").mkdir(); (root/"pkg"/"worker.py").write_text("def process_signal(x):\n    return x\n",encoding="utf-8")
  shadow=root/"kanda_reasoner_app"/"safety_suite_cli"; shadow.mkdir(parents=True); (root/"kanda_reasoner_app"/"__init__.py").write_text("",encoding="utf-8"); (shadow/"__init__.py").write_text("",encoding="utf-8"); (shadow/"commands.py").write_text("def main(args=None):\n    print('MALICIOUS_PROJECT_SHADOW_EXECUTED')\n    return 0\n",encoding="utf-8")
  before=digest(root/"main.py"); context,args=check_args(boundary,commands,names,root,"SYNTHETIC_EXTERNAL")
  print("EXTERNAL_PROJECT_ARGS_TOOL_SEEDS_ABSENT: PASS"); print("EXTERNAL_PROJECT_TARGETS_INSIDE_ACTIVE_PROJECT: PASS")
  req(args["find-symbol"][args["find-symbol"].index("--symbol")+1]=="eeg_entry" and args["api-contract"][args["api-contract"].index("--module")+1]=="main","EXTERNAL_PROJECT_SYMBOL_AND_MODULE_DERIVED")
  req(root.name in args["release-notes"][args["release-notes"].index("--bundle-name")+1],"EXTERNAL_PROJECT_RELEASE_CONTEXT_PROJECT_OWNED")
  text=panel.run_engineering_safety_panel_cli_command("api-contract",str(root)); req("MALICIOUS_PROJECT_SHADOW_EXECUTED" not in text,"PONTUAL_AUDIT_USES_SAME_BOUNDARY_SHIELD")
  result=panel.run_engineering_safety_panel_command("property-test",str(root)); req(result.status_code==0 and "MALICIOUS_PROJECT_SHADOW_EXECUTED" not in (result.stdout+result.stderr),"FULL_AUDIT_COMMAND_RUNNER_TOOL_PROVENANCE")
  req(before==digest(root/"main.py"),"SYNTHETIC_EXTERNAL_PROJECT_SOURCE_MUTATED: NO")
  real=sys.modules.get("kanda_reasoner_app.safety_suite_cli.commands"); fake=types.ModuleType("kanda_reasoner_app.safety_suite_cli.commands"); fake.__file__=str(shadow/"commands.py"); fake.main=lambda args=None: (_ for _ in ()).throw(RuntimeError("MALICIOUS_EXECUTED")); sys.modules["kanda_reasoner_app.safety_suite_cli.commands"]=fake
  try:
   attacked=commands._run_cli_in_process(["list-tools"]); req(attacked.status_code==1 and "TOOL_MODULE_PROVENANCE_VIOLATION" in attacked.stderr and "MALICIOUS_EXECUTED" not in attacked.stderr,"PROJECT_SHADOW_TOOL_MODULE_REJECTED_BEFORE_EXECUTION")
  finally:
   if real is None: sys.modules.pop("kanda_reasoner_app.safety_suite_cli.commands",None)
   else: sys.modules["kanda_reasoner_app.safety_suite_cli.commands"]=real
  collector=boundary.import_tool_module("kanda_reasoner_app.reasoner_context_collector","reasoner_context_collector"); original_collect=collector.collect_canonical_project_python_files; collector.collect_canonical_project_python_files=lambda _root:[root/"main.py",tool/"reasoner_tools_gui.py"]
  try:
   try: boundary.project_command_context(root)
   except RuntimeError as exc: req("CANONICAL_PROJECT_SCOPE_ESCAPED_ACTIVE_ROOT" in str(exc),"CANONICAL_PROJECT_SCOPE_ESCAPE_REJECTED")
   else: raise RuntimeError("CANONICAL_PROJECT_SCOPE_ESCAPE_REJECTED: FAIL")
  finally: collector.collect_canonical_project_python_files=original_collect
 with tempfile.TemporaryDirectory(prefix="kanda_boundary_empty_") as td:
  result=commands._run_command("find-symbol",td); sig=signals.classify_engineering_review_signal("find-symbol",result.status_code,result.stdout,result.stderr); req(result.status_code==0 and "PROJECT_CONTEXT_UNAVAILABLE:" in result.stdout and sig.assessment==signals.ASSESSMENT_NOT_RUN,"NO_SAFE_PROJECT_CONTEXT_FAILS_CLOSED_NOT_RUN")
 with tempfile.TemporaryDirectory(prefix="kanda_boundary_import_shadow_") as td:
  project=Path(td).resolve(); package=project/"kanda_reasoner_app"; package.mkdir(); marker=project/"malicious_import_marker.txt"; (package/"__init__.py").write_text("from pathlib import Path\nPath("+repr(str(marker))+ ").write_text('executed')\n",encoding="utf-8"); (package/"project_root_resolver.py").write_text("def resolve_active_project_root(x=None):\n    return 'MALICIOUS'\n",encoding="utf-8")
  code="import sys; sys.path.insert(0,"+repr(str(project))+ "); sys.path.insert(1,"+repr(str(tool))+ "); import _reasoner_tools_gui_engineering_safety_panel_commands; print('IMPORT_OK')"
  proc=subprocess.run([sys.executable,"-c",code],cwd=str(project),capture_output=True,text=True,check=False); req(proc.returncode==0 and "IMPORT_OK" in proc.stdout and not marker.exists(),"TOOL_IMPORT_PRECEDENCE_BLOCKS_PROJECT_PACKAGE_EXECUTION")
def predecessor_contract(tool:Path,boundary,commands):
 context=boundary.project_command_context(tool); req(context.root==tool and boundary.is_within(tool/context.target,tool),"SELF_HOSTING_PHYSICAL_EQUALITY_LOGICAL_SEPARATION")
 full=(tool/"_reasoner_tools_gui_engineering_safety_full_audit.py").read_text(encoding="utf-8"); handoff=(tool/"_reasoner_tools_gui_engineering_safety_full_audit_handoff.py").read_text(encoding="utf-8")
 req("result = command_runner(command_name, project_root)" in full and "project_card = capture_active_project_card(project_root)" in handoff and "project_card.project_root," in handoff and "project_card_is_current" in handoff,"PREDECESSOR_COMPLETE_REVIEW_ORCHESTRATION_PRESERVED")
def architecture(tool:Path):
 script=tool/"kanda_reasoner_app/manage_architecture/manage_architecture.py"; r=subprocess.run([sys.executable,str(script),"--root",str(tool),"--validate"],capture_output=True,text=True,check=False); text=(r.stdout or "")+"\n"+(r.stderr or ""); names={Path(x).name for x in TOUCHED}; bad=[line for line in text.splitlines() if line.lstrip().startswith(("ERROR ","WARNING ")) and any(name in line for name in names)]; req(not bad,"BOUNDARY_SHIELD_ARCHITECTURE_TOUCHED_PATH_ISSUES_ZERO"); print("ARCHITECTURE VALIDATOR EXIT CODE: "+str(r.returncode))
def active_project(tool:Path,project:Path,boundary):
 m=boundary.import_tool_module("kanda_reasoner_app.project_selection_registry","project_selection_registry"); reg=m.ProjectSelectionRegistry(tool_source_root=tool); rec=reg.load_current_record(); req(rec is not None,"ACTIVE_PROJECT_SELECTION_PRESENT"); b=reg.resolve_boundary_for_root(project); req(Path(rec.project_root).resolve(strict=False)==project,"ACTIVE_PROJECT_ROOT_MATCHES_VALIDATION_TARGET"); req(b.active_project_id==rec.stable_project_id,"ACTIVE_PROJECT_ID_MATCHES_MCARD"); req(b.active_project_root_fingerprint==rec.project_root_fingerprint,"ACTIVE_PROJECT_FINGERPRINT_MATCHES_MCARD"); print("ACTIVE PROJECT IS AUDIT MCARD: PASS"); print("TOOL ROOT USED AS AUDIT TARGET: NO"); print("TOOL PROJECT LOGICAL ROLE SEPARATION: PASS")
def main():
 ap=argparse.ArgumentParser(); ap.add_argument("--tool-root",required=True); ap.add_argument("--project-root",required=True); ap.add_argument("--skip-active-registry-check",action="store_true"); ap.add_argument("--skip-architecture",action="store_true"); a=ap.parse_args(); tool=Path(a.tool_root).resolve(strict=True); project=Path(a.project_root).resolve(strict=True)
 before_touched={rel:digest(tool/rel) for rel in TOUCHED}; boundary,commands,signals,panel=import_current(tool); collector,names=source_contract(tool,boundary,commands,signals,panel)
 project_py=[Path(x).resolve(strict=False) for x in collector.collect_canonical_project_python_files(project) if Path(x).is_file()]; p0=source_inventory(project_py,project)
 drive=Path(project.anchor); project_support=drive/(project.name+"_show_project_to_AI"); tool_support=Path(tool.anchor)/(tool.name+"_show_project_to_AI"); reg_path=tool/"project_selection_registry.json"
 state0=(state_hash(reg_path),tree_hash(project_support/"project_freeze_after_update/frozen_features_memory"),tree_hash(project_support/"project_error_memory/lessons"),tree_hash(tool_support/"project_freeze_after_update/frozen_features_memory"),tree_hash(tool_support/"project_error_memory/lessons"))
 synthetic_contract(tool,boundary,commands,signals,panel,names); guidance_contract(tool,project,commands); predecessor_contract(tool,boundary,commands)
 real_context,real_args=check_args(boundary,commands,names,project,"REAL_PROJECT"); req(real_context.root==project and boundary.is_within(project/real_context.target,project),"REAL_PROJECT_COMMAND_CONTEXT_PROJECT_OWNED"); req(all(not(FORBIDDEN & set(map(str,args))) for args in real_args.values()),"REAL_PROJECT_TOOL_SEEDS_ABSENT"); req(project!=tool or real_context.root==tool,"REAL_PROJECT_SELF_HOSTING_PHYSICAL_EQUALITY_ROLE_AWARE")
 real_guidance=[]
 for command_name in ("push-plan","stack-brief"):
  outcome=commands._run_command(command_name,str(project)); req(outcome.status_code==0,"REAL_PROJECT_GUIDANCE_COMMAND_EXECUTION:"+command_name); real_guidance.append(outcome.stdout+"\n"+outcome.stderr)
 req(all(not ambiguous_tool_guidance(chunk) for chunk in real_guidance),"REAL_PROJECT_OUTPUT_GUIDANCE_SHIELDED")
 req(all("[KANDA TOOL EXECUTION PROVIDER]" in chunk for chunk in real_guidance),"REAL_PROJECT_OUTPUT_TOOL_PROVIDER_EXPLICIT")
 if not a.skip_architecture: architecture(tool)
 if not a.skip_active_registry_check: active_project(tool,project,boundary)
 p1=source_inventory([Path(x).resolve(strict=False) for x in collector.collect_canonical_project_python_files(project) if Path(x).is_file()],project); req(p0==p1,"PROJECT SOURCE MUTATED BY VALIDATOR: NO")
 state1=(state_hash(reg_path),tree_hash(project_support/"project_freeze_after_update/frozen_features_memory"),tree_hash(project_support/"project_error_memory/lessons"),tree_hash(tool_support/"project_freeze_after_update/frozen_features_memory"),tree_hash(tool_support/"project_error_memory/lessons"))
 labels=["PROJECT SELECTION REGISTRY MUTATED BY VALIDATOR: NO","ACTIVE PROJECT FREEZE MEMORY MUTATED BY VALIDATOR: NO","ACTIVE PROJECT ERROR MEMORY MUTATED BY VALIDATOR: NO","TOOL SELF-HOST PROJECT FREEZE MEMORY MUTATED BY VALIDATOR: NO","TOOL SELF-HOST PROJECT ERROR MEMORY MUTATED BY VALIDATOR: NO"]
 for x,y,label in zip(state0,state1,labels): req(x==y,label)
 req(before_touched=={rel:digest(tool/rel) for rel in TOUCHED},"TOUCHED SOURCE MUTATED BY VALIDATOR: NO")
 print("VALIDATION OK: "+FEATURE_ID); print("STATUS: IN_SYNC"); return 0
if __name__=="__main__": raise SystemExit(main())
