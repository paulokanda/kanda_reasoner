"""Validation-only Brick Wall Q25 mutation-testing pilot contract."""
from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
import os
from pathlib import Path
import shutil
import subprocess
import sys
from typing import Mapping

from brick_wall_q20_isolated_filesystem_fixture import isolated_filesystem_fixture

__all__: list[str] = []
FEATURE_ID = "brick-wall-q25-mutation-testing-pilot-decision-enforcement-v1"
DEPENDENCY_SCOPE = "STANDARD_LIBRARY_VALIDATION_ONLY_SELECTED_GUARDS"
REPAIR_BEGIN = "    # Q25_MUTATION_GAP_REPAIR_BEGIN\n"
REPAIR_END = "    # Q25_MUTATION_GAP_REPAIR_END\n"
REQUIRED_FIELDS = (
    "pilot_applicable", "no_pilot_evidence", "q24_decision_complete", "primary_box",
    "selected_validators", "mutation_engine", "dependency_scope", "operators",
    "replay_strategy", "isolation_strategy", "bounds", "baseline_validators_passed",
    "mutants_generated", "mutants_killed_before_repair", "mutants_survived_before_repair",
    "equivalent_mutants", "mutants_killed_after_repair", "mutants_survived_after_repair",
    "mutation_score_before", "mutation_score_after", "meaningful_protection_gaps",
    "test_repairs", "measurable_gain", "operational_cost", "broader_adoption_decision",
    "unresolved_fields", "decision", "may_proceed_to_q26", "may_begin_coding",
    "may_write_source",
)

@dataclass(frozen=True)
class Mutant:
    mutant_id: str
    subject: str
    validator: str
    guard: str
    old: str
    new: str

MUTANTS = (
    Mutant("q16-relative-input-or-to-and", "tools/brick_wall_q16_resolved_path_containment_contract.py", "tools/validate_brick_wall_q16_resolved_path_containment_v1.py", "relative traversal input rejection", 'if path.is_absolute() or any(part in {"", ".", ".."} for part in path.parts):', 'if path.is_absolute() and any(part in {"", ".", ".."} for part in path.parts):'),
    Mutant("q16-disable-drive-match", "tools/brick_wall_q16_resolved_path_containment_contract.py", "tools/validate_brick_wall_q16_resolved_path_containment_v1.py", "drive/share match rejection", 'if candidate["drive_or_share_match"] is not True:', 'if False and candidate["drive_or_share_match"] is not True:'),
    Mutant("q18-disable-lifecycle-boolean-check", "tools/brick_wall_q18_stale_async_result_contract.py", "tools/validate_brick_wall_q18_stale_async_result_rejection_v1.py", "cancel/timeout/thread authority revocation", 'if route[field] is not True:', 'if False and route[field] is not True:'),
    Mutant("q18-disable-stale-effects-subset", "tools/brick_wall_q18_stale_async_result_contract.py", "tools/validate_brick_wall_q18_stale_async_result_rejection_v1.py", "stale-result effect blocking", 'if not REQUIRED_STALE_BLOCKS.issubset(blocked):', 'if False and not REQUIRED_STALE_BLOCKS.issubset(blocked):'),
    Mutant("q23-disable-stale-lifecycle-block", "tools/brick_wall_q23_mcard_transition_contract.py", "tools/validate_brick_wall_q23_deterministic_mcard_transition_tests_v1.py", "stale lifecycle generation rejection", 'if not case.get("lifecycle_generation_current"):', 'if False and not case.get("lifecycle_generation_current"):'),
    Mutant("q23-disable-eject-lock", "tools/brick_wall_q23_mcard_transition_contract.py", "tools/validate_brick_wall_q23_deterministic_mcard_transition_tests_v1.py", "open transaction/unresolved apply eject lock", 'if (case.get("open_transaction") or case.get("unresolved_apply_outcome")) and target == "CARD_EJECTED":', 'if False and (case.get("open_transaction") or case.get("unresolved_apply_outcome")) and target == "CARD_EJECTED":'),
)

def _text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())

def _texts(value: object, *, empty: bool = False) -> bool:
    return isinstance(value, list) and (empty or bool(value)) and all(_text(item) for item in value)

SEMANTIC_COMMANDS = {
    "tools/validate_brick_wall_q16_resolved_path_containment_v1.py": "import validate_brick_wall_q16_resolved_path_containment_v1 as v; v.validate_semantics()",
    "tools/validate_brick_wall_q18_stale_async_result_rejection_v1.py": "import validate_brick_wall_q18_stale_async_result_rejection_v1 as v; v.validate_semantics()",
    "tools/validate_brick_wall_q23_deterministic_mcard_transition_tests_v1.py": "import validate_brick_wall_q23_deterministic_mcard_transition_tests_v1 as v; v.validate_contract(); v.validate_runtime_matrix()",
}
REQUIRED_TOOL_FILES = tuple(sorted({
    *(mutant.subject for mutant in MUTANTS),
    *(mutant.validator for mutant in MUTANTS),
    "tools/validate_brick_wall_q11_mcard_applicability_lifecycle_v1.py",
}))

def _run(project: Path, validator: str, timeout: int) -> tuple[bool, str]:
    tools = project / "tools"
    result = subprocess.run([sys.executable, "-c", SEMANTIC_COMMANDS[validator]], cwd=tools, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1", "PYTHONPATH": str(tools)}, text=True, capture_output=True, timeout=timeout, check=False)
    output = (result.stdout or "") + (result.stderr or "")
    return result.returncode == 0, output

def _without_q25_repair(text: str) -> str:
    start = text.find(REPAIR_BEGIN); end = text.find(REPAIR_END)
    if start < 0 or end < 0 or end < start:
        raise AssertionError("Q25 mutation-gap repair markers missing")
    return text[:start] + text[end + len(REPAIR_END):]

def _apply_mutant(project: Path, mutant: Mutant) -> str:
    path = project / mutant.subject
    original = path.read_text(encoding="utf-8")
    if original.count(mutant.old) != 1:
        raise AssertionError("mutation subject drift: " + mutant.mutant_id)
    path.write_text(original.replace(mutant.old, mutant.new, 1), encoding="utf-8")
    return original

def run_bounded_mutation_pilot(project_root: Path) -> dict[str, object]:
    project_root = project_root.resolve()
    validators = sorted({mutant.validator for mutant in MUTANTS})
    protected = [project_root / relative for relative in REQUIRED_TOOL_FILES]
    with isolated_filesystem_fixture(protected_paths=protected, prefix="kanda_q25_mutation_") as layout:
        copied = layout.source_root / "project"
        tools = copied / "tools"
        tools.mkdir(parents=True)
        for relative in REQUIRED_TOOL_FILES:
            source = project_root / relative
            target = copied / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
        timeout = 30
        baseline = {}
        for validator in validators:
            ok, output = _run(copied, validator, timeout)
            baseline[validator] = {"passed": ok, "tail": output.splitlines()[-3:]}
            if not ok:
                raise AssertionError("mutation baseline failed: " + validator)
        q16_path = copied / "tools/validate_brick_wall_q16_resolved_path_containment_v1.py"
        repaired_q16 = q16_path.read_text(encoding="utf-8")
        q16_path.write_text(_without_q25_repair(repaired_q16), encoding="utf-8")
        before = []
        for mutant in MUTANTS:
            subject = copied / mutant.subject
            original = _apply_mutant(copied, mutant)
            ok, output = _run(copied, mutant.validator, timeout)
            before.append({"mutant_id": mutant.mutant_id, "guard": mutant.guard, "killed": not ok, "validator": mutant.validator, "tail": output.splitlines()[-4:]})
            subject.write_text(original, encoding="utf-8")
        q16_path.write_text(repaired_q16, encoding="utf-8")
        after = []
        for mutant in MUTANTS:
            subject = copied / mutant.subject
            original = _apply_mutant(copied, mutant)
            ok, output = _run(copied, mutant.validator, timeout)
            after.append({"mutant_id": mutant.mutant_id, "guard": mutant.guard, "killed": not ok, "validator": mutant.validator, "tail": output.splitlines()[-4:]})
            subject.write_text(original, encoding="utf-8")
        killed_before = [item["mutant_id"] for item in before if item["killed"]]
        survived_before = [item["mutant_id"] for item in before if not item["killed"]]
        killed_after = [item["mutant_id"] for item in after if item["killed"]]
        survived_after = [item["mutant_id"] for item in after if not item["killed"]]
        total = len(MUTANTS)
        return {"baseline": baseline, "before": before, "after": after, "mutants_generated": total, "killed_before": killed_before, "survived_before": survived_before, "killed_after": killed_after, "survived_after": survived_after, "score_before": round(100 * len(killed_before) / total, 2), "score_after": round(100 * len(killed_after) / total, 2)}

def validate_record(record: Mapping[str, object]) -> None:
    missing = [field for field in REQUIRED_FIELDS if field not in record]
    if missing: raise AssertionError("record missing fields: " + ", ".join(missing))
    for field in ("pilot_applicable", "q24_decision_complete", "baseline_validators_passed", "may_proceed_to_q26", "may_begin_coding", "may_write_source"):
        if not isinstance(record[field], bool): raise AssertionError("invalid boolean field: " + field)
    if record["decision"] not in {"PILOT_RETAINED", "PILOT_REJECTED", "NOT_APPLICABLE", "BLOCKED"}: raise AssertionError("invalid Q25 decision")
    if record["may_begin_coding"] or record["may_write_source"]: raise AssertionError("Q25 cannot authorize coding or source writes")
    if record["decision"] == "BLOCKED" or record["unresolved_fields"]: raise AssertionError("Q25 remains blocked")
    if not record["may_proceed_to_q26"]: raise AssertionError("Q26 progression not approved")
    if not record["pilot_applicable"]:
        if record["decision"] != "NOT_APPLICABLE" or not _texts(record["no_pilot_evidence"]): raise AssertionError("Q25 N/A evidence incomplete")
        if record["mutants_generated"] or record["meaningful_protection_gaps"]: raise AssertionError("N/A record carries pilot results")
        return
    if not record["q24_decision_complete"] or not record["baseline_validators_passed"]: raise AssertionError("Q24 or baseline incomplete")
    if record["decision"] not in {"PILOT_RETAINED", "PILOT_REJECTED"} or record["no_pilot_evidence"]: raise AssertionError("applicable pilot decision incomplete")
    if not all(_text(record[field]) for field in ("primary_box", "mutation_engine", "dependency_scope", "replay_strategy", "isolation_strategy", "measurable_gain", "operational_cost", "broader_adoption_decision")): raise AssertionError("Q25 method/evidence incomplete")
    if record["dependency_scope"] != DEPENDENCY_SCOPE: raise AssertionError("mutation testing escaped selected validation-only scope")
    if not _texts(record["selected_validators"]) or len(record["selected_validators"]) > 5: raise AssertionError("selected validator scope invalid")
    if not _texts(record["operators"]): raise AssertionError("mutation operator inventory missing")
    bounds = record["bounds"]
    if not isinstance(bounds, Mapping) or not all(isinstance(bounds.get(x), int) and bounds[x] > 0 for x in ("max_mutants", "max_validators", "timeout_per_validator_seconds")): raise AssertionError("mutation bounds invalid")
    if bounds["max_mutants"] > 25 or bounds["max_validators"] > 5 or bounds["timeout_per_validator_seconds"] > 120: raise AssertionError("mutation pilot unbounded")
    total = record["mutants_generated"]
    if not isinstance(total, int) or total <= 0 or total > bounds["max_mutants"]: raise AssertionError("mutant count invalid")
    for field in ("mutants_killed_before_repair", "mutants_survived_before_repair", "equivalent_mutants", "mutants_killed_after_repair", "mutants_survived_after_repair", "meaningful_protection_gaps", "test_repairs"):
        if not _texts(record[field], empty=True): raise AssertionError("invalid mutation evidence: " + field)
    if len(record["mutants_killed_before_repair"]) + len(record["mutants_survived_before_repair"]) + len(record["equivalent_mutants"]) != total: raise AssertionError("before-repair mutant classification incomplete")
    if len(record["mutants_killed_after_repair"]) + len(record["mutants_survived_after_repair"]) + len(record["equivalent_mutants"]) != total: raise AssertionError("after-repair mutant classification incomplete")
    if not isinstance(record["mutation_score_before"], (int, float)) or not isinstance(record["mutation_score_after"], (int, float)): raise AssertionError("mutation scores invalid")
    if record["decision"] == "PILOT_RETAINED":
        if not record["meaningful_protection_gaps"] or not record["test_repairs"]: raise AssertionError("pilot retained without meaningful repaired gap")
        if record["mutants_survived_after_repair"]: raise AssertionError("retained pilot leaves surviving mutants")
        if record["mutation_score_after"] <= record["mutation_score_before"]: raise AssertionError("retained pilot has no measurable score gain")
        if record["broader_adoption_decision"] != "RETAIN_BOUNDED_CRITICAL_GUARD_PILOT": raise AssertionError("retained decision scope invalid")
    if record["decision"] == "PILOT_REJECTED":
        if record["meaningful_protection_gaps"] or record["test_repairs"]: raise AssertionError("rejected pilot contains repaired meaningful gap")
        if record["broader_adoption_decision"] != "REJECT_BROADER_ADOPTION": raise AssertionError("rejected adoption decision invalid")

def valid_retained_record(project_root: Path, result: Mapping[str, object] | None = None) -> dict[str, object]:
    result = run_bounded_mutation_pilot(project_root) if result is None else result
    return {"pilot_applicable": True, "no_pilot_evidence": [], "q24_decision_complete": True, "primary_box": "kanda_prompt_workspace/prompt_library", "selected_validators": sorted(result["baseline"]), "mutation_engine": "STANDARD_LIBRARY_TEXT_MUTATION_WITH_CANONICAL_VALIDATOR_REPLAY", "dependency_scope": DEPENDENCY_SCOPE, "operators": ["boolean connector weakening", "guard disabling", "subset check disabling"], "replay_strategy": "Exact mutant ID, source replacement, validator command, and captured failure tail", "isolation_strategy": "Q20 disposable sandbox with copied source and protected production-root snapshot", "bounds": {"max_mutants": 10, "max_validators": 5, "timeout_per_validator_seconds": 60}, "baseline_validators_passed": all(item["passed"] for item in result["baseline"].values()), "mutants_generated": result["mutants_generated"], "mutants_killed_before_repair": result["killed_before"], "mutants_survived_before_repair": result["survived_before"], "equivalent_mutants": [], "mutants_killed_after_repair": result["killed_after"], "mutants_survived_after_repair": result["survived_after"], "mutation_score_before": result["score_before"], "mutation_score_after": result["score_after"], "meaningful_protection_gaps": ["Q16 traversal-input rejection was not independently isolated", "Q16 drive/share-match flag rejection was masked by another path failure"], "test_repairs": ["Added Q16_NEGATIVE_TRAVERSAL_GUARD_ISOLATED", "Added Q16_NEGATIVE_DRIVE_MATCH_FLAG_ISOLATED"], "measurable_gain": "Two reproducible non-equivalent surviving mutants were converted to killed mutants; selected-guard score improved from 66.67% to 100.0%.", "operational_cost": "Six mutants across three focused validators; no full-project scan or external dependency.", "broader_adoption_decision": "RETAIN_BOUNDED_CRITICAL_GUARD_PILOT", "unresolved_fields": [], "decision": "PILOT_RETAINED", "may_proceed_to_q26": True, "may_begin_coding": False, "may_write_source": False}

def valid_rejected_record(project_root: Path, result: Mapping[str, object] | None = None) -> dict[str, object]:
    record = valid_retained_record(project_root, result)
    record.update(mutants_survived_before_repair=[], meaningful_protection_gaps=[], test_repairs=[], mutation_score_before=100.0, measurable_gain="No surviving non-equivalent mutant or focused test gap was found.", broader_adoption_decision="REJECT_BROADER_ADOPTION", decision="PILOT_REJECTED")
    record["mutants_killed_before_repair"] = list(record["mutants_killed_after_repair"])
    return record

def valid_not_applicable_record(project_root: Path, result: Mapping[str, object] | None = None) -> dict[str, object]:
    record = valid_rejected_record(project_root, result)
    record.update(pilot_applicable=False, no_pilot_evidence=["No selected critical validator or guard is in scope."], baseline_validators_passed=False, mutants_generated=0, mutants_killed_before_repair=[], mutants_survived_before_repair=[], equivalent_mutants=[], mutants_killed_after_repair=[], mutants_survived_after_repair=[], mutation_score_before=0.0, mutation_score_after=0.0, broader_adoption_decision="NOT_APPLICABLE", decision="NOT_APPLICABLE")
    return record

def mutated_record(project_root: Path, result: Mapping[str, object] | None = None) -> dict[str, object]:
    return deepcopy(valid_retained_record(project_root, result))
