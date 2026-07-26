"""Validate Brick Wall Q25 mutation-testing pilot decision governance."""
from __future__ import annotations
import argparse, json, re
from copy import deepcopy
from pathlib import Path
from typing import Callable, Sequence
from brick_wall_q25_mutation_testing_pilot_contract import mutated_record, run_bounded_mutation_pilot, validate_record, valid_not_applicable_record, valid_rejected_record, valid_retained_record

__all__: list[str] = []
FEATURE_ID="brick-wall-q25-mutation-testing-pilot-decision-enforcement-v1"
PLIB=Path("kanda_prompt_workspace/prompt_library")
BRICK_REL=PLIB/"ACTIVE_PROMPTS/03_governance_freeze_and_handoff/brick_wall_comprehensive_quality_gate.md"
BRIDGE_REL=PLIB/"ACTIVE_PROMPTS/05_patch_delivery_and_validation/router_bridge_governed_implementation.md"
BRICK_META_REL=PLIB/"METADATA/brick_wall_comprehensive_quality_gate.meta.json"
BRIDGE_META_REL=PLIB/"METADATA/router_bridge_governed_implementation.meta.json"
Q16_REL=Path("tools/validate_brick_wall_q16_resolved_path_containment_v1.py")
Q24_REL=Path("tools/validate_brick_wall_q24_property_based_mcard_pilot_decision_v1.py")
Q25_CONTRACT_REL=Path("tools/brick_wall_q25_mutation_testing_pilot_contract.py")
Q25_VALIDATOR_REL=Path("tools/validate_brick_wall_q25_mutation_testing_pilot_decision_v1.py")
BRICK_MARKERS=("### Mutation-testing pilot decision (Q25)","MUTATION-TESTING PILOT DECISION RECORD","selected critical guards only","full-project/default execution forbidden","PILOT_RETAINED/PILOT_REJECTED/NOT_APPLICABLE/BLOCKED","proceed to Q26 ZIP containment/collision hardening YES/NO")
BRIDGE_MARKERS=("## Mutation-testing pilot decision gate (Q25)","Q25 mutation-testing pilot decision record complete: YES / NO","Mutation-testing pilot decision: PILOT_RETAINED / PILOT_REJECTED / NOT_APPLICABLE / BLOCKED","May proceed to Q26 ZIP containment and collision hardening gate: YES / NO","## Mutation-testing pilot bridge","full-project default execution is forbidden")

def _read(path: Path) -> str:
    if not path.is_file(): raise AssertionError("missing file: "+str(path))
    return path.read_text(encoding="utf-8-sig")
def _load(path: Path) -> dict[str, object]: return json.loads(_read(path))
def _gate(label: str, ok: bool, detail: str="") -> None:
    if not ok: raise AssertionError(label+": FAIL"+(" - "+detail if detail else ""))
    print(label+": PASS"+(" - "+detail if detail else ""))
def _require(text: str, markers: Sequence[str], label: str) -> None:
    missing=[m for m in markers if m not in text]; _gate(label,not missing,", ".join(missing))
def _version(value: object) -> tuple[int,...]:
    try: return tuple(int(x) for x in str(value).split("."))
    except ValueError: return ()
def _precode(text: str, minimum: int) -> bool:
    match=re.search(r"After Q(\d+), all applicable pre-code items.*?Q01-Q(\d+) complete YES/NO",text,re.DOTALL)
    return bool(match and match.group(1)==match.group(2) and int(match.group(1))>=minimum)

def validate_source(root: Path) -> None:
    brick=_read(root/BRICK_REL); bridge=_read(root/BRIDGE_REL); bm=_load(root/BRICK_META_REL); rm=_load(root/BRIDGE_META_REL)
    _require(brick,BRICK_MARKERS,"Q25_BRICK_WALL_CONTRACT"); _require(bridge,BRIDGE_MARKERS,"Q25_ROUTER_BRIDGE_CONTRACT")
    _gate("Q25_BRICK_VERSION",_version(bm.get("version"))>=(3,5)); _gate("Q25_BRIDGE_VERSION",_version(rm.get("version"))>=(3,9))
    for label,meta in (("brick",bm),("bridge",rm)):
        stage=str(meta.get("source_stage", "")); updated=str(meta.get("updated_for", ""))
        match=re.search(r"brick-wall-q(\d+)-", stage)
        _gate("Q25_METADATA_ALIGNMENT",stage==updated and bool(match) and int(match.group(1))>=25,label)
    _gate("Q25_PRECODE_PROGRESSION",_precode(brick,25))
    _gate("Q25_FORWARD_COMPATIBLE_Q26_PRECODE_PROGRESSION",_precode(brick,26))
    _gate("Q24_FORWARD_COMPATIBLE_Q25_PROGRESSION","Q24_FORWARD_COMPATIBLE_Q25_PRECODE_PROGRESSION" in _read(root/Q24_REL))
    q16=_read(root/Q16_REL); _require(q16,("Q25_MUTATION_GAP_REPAIR_BEGIN","Q16_NEGATIVE_TRAVERSAL_GUARD_ISOLATED","Q16_NEGATIVE_DRIVE_MATCH_FLAG_ISOLATED","Q25_MUTATION_GAP_REPAIR_END"),"Q25_Q16_MUTATION_GAP_REPAIR")
    for rel in (BRICK_REL,BRIDGE_REL,Q16_REL,Q24_REL,Q25_CONTRACT_REL,Q25_VALIDATOR_REL): _gate("Q25_MODULE_SIZE",len(_read(root/rel).splitlines())<=500,str(rel))

def _reject(root: Path, result: dict[str, object], label: str, mutate: Callable[[dict[str, object]],None]) -> None:
    record=mutated_record(root, result); mutate(record)
    try: validate_record(record)
    except AssertionError: _gate(label,True)
    else: _gate(label,False)

def validate_contract(root: Path, result: dict[str, object]) -> None:
    validate_record(valid_retained_record(root, result)); _gate("Q25_PILOT_RETAINED_RECORD_ACCEPTED",True)
    validate_record(valid_rejected_record(root, result)); _gate("Q25_PILOT_REJECTED_RECORD_ACCEPTED",True)
    validate_record(valid_not_applicable_record(root, result)); _gate("Q25_NOT_APPLICABLE_RECORD_ACCEPTED",True)
    tests=[
        ("Q25_NEGATIVE_Q24_BASELINE_INCOMPLETE",lambda r:r.update(q24_decision_complete=False)),
        ("Q25_NEGATIVE_GLOBAL_DEPENDENCY",lambda r:r.update(dependency_scope="GLOBAL_RUNTIME_MUTATION_ENGINE")),
        ("Q25_NEGATIVE_VALIDATOR_SCOPE_EMPTY",lambda r:r.update(selected_validators=[])),
        ("Q25_NEGATIVE_OPERATOR_INVENTORY",lambda r:r.update(operators=[])),
        ("Q25_NEGATIVE_UNBOUNDED_MUTANTS",lambda r:r["bounds"].update(max_mutants=1000)),
        ("Q25_NEGATIVE_REPLAY_MISSING",lambda r:r.update(replay_strategy="")),
        ("Q25_NEGATIVE_ISOLATION_MISSING",lambda r:r.update(isolation_strategy="")),
        ("Q25_NEGATIVE_CLASSIFICATION_INCOMPLETE",lambda r:r["mutants_killed_before_repair"].pop()),
        ("Q25_NEGATIVE_RETAIN_WITHOUT_GAP",lambda r:r.update(meaningful_protection_gaps=[],test_repairs=[])),
        ("Q25_NEGATIVE_SURVIVOR_AFTER_REPAIR",lambda r:r.update(mutants_survived_after_repair=["q16-disable-drive-match"],mutants_killed_after_repair=r["mutants_killed_after_repair"][:-1])),
        ("Q25_NEGATIVE_NO_SCORE_GAIN",lambda r:r.update(mutation_score_after=r["mutation_score_before"])),
        ("Q25_NEGATIVE_FULL_PROJECT_ADOPTION",lambda r:r.update(broader_adoption_decision="FULL_PROJECT_DEFAULT_MUTATION")),
        ("Q25_NEGATIVE_Q26_PROGRESSION",lambda r:r.update(may_proceed_to_q26=False)),
        ("Q25_NEGATIVE_CODING_AUTHORIZATION",lambda r:r.update(may_begin_coding=True)),
        ("Q25_NEGATIVE_SOURCE_WRITE_AUTHORIZATION",lambda r:r.update(may_write_source=True)),
    ]
    for label,mutate in tests: _reject(root,result,label,mutate)
    record=valid_not_applicable_record(root,result); record["no_pilot_evidence"]=[]
    try: validate_record(record)
    except AssertionError: _gate("Q25_NEGATIVE_EMPTY_NOT_APPLICABLE_EVIDENCE",True)
    else: _gate("Q25_NEGATIVE_EMPTY_NOT_APPLICABLE_EVIDENCE",False)
    print("Q25_MUTATION_TESTING_PILOT_DECISION_REGRESSION_SET: PASS")

def validate_runtime(root: Path, first: dict[str, object]) -> None:
    _gate("Q25_MUTATION_PILOT_BASELINES_PASS",all(item["passed"] for item in first["baseline"].values()))
    _gate("Q25_MUTATION_PILOT_REPLAY_DETERMINISTIC", first["killed_before"] == ["q18-disable-lifecycle-boolean-check", "q18-disable-stale-effects-subset", "q23-disable-stale-lifecycle-block", "q23-disable-eject-lock"] and first["survived_before"] == ["q16-relative-input-or-to-and", "q16-disable-drive-match"] and first["survived_after"] == [])
    _gate("Q25_MUTANTS_GENERATED",first["mutants_generated"]==6)
    _gate("Q25_PRE_REPAIR_SURVIVING_MUTANTS",first["survived_before"]==["q16-relative-input-or-to-and","q16-disable-drive-match"])
    _gate("Q25_PRE_REPAIR_MUTATION_SCORE",first["score_before"]==66.67)
    _gate("Q25_POST_REPAIR_ALL_MUTANTS_KILLED",first["killed_after"] and not first["survived_after"])
    _gate("Q25_POST_REPAIR_MUTATION_SCORE",first["score_after"]==100.0)
    record=valid_retained_record(root,first); validate_record(record)
    _gate("Q25_BOUNDED_CRITICAL_GUARD_PILOT_RETAINED",record["broader_adoption_decision"]=="RETAIN_BOUNDED_CRITICAL_GUARD_PILOT")
    _gate("Q25_NO_FULL_PROJECT_OR_GLOBAL_MUTATION_DEPENDENCY",record["dependency_scope"]=="STANDARD_LIBRARY_VALIDATION_ONLY_SELECTED_GUARDS")
    print("Q25_RUNTIME_MUTATION_TESTING_PILOT: PASS")

def run_validation(root: Path) -> None:
    first=run_bounded_mutation_pilot(root); validate_source(root); validate_contract(root,first); validate_runtime(root,first); print("VALIDATION OK: "+FEATURE_ID); print("STATUS: IN_SYNC")
def main() -> int:
    p=argparse.ArgumentParser(); p.add_argument("--project-root",type=Path,default=Path.cwd()); a=p.parse_args(); run_validation(a.project_root.expanduser().resolve()); return 0
if __name__=="__main__": raise SystemExit(main())
