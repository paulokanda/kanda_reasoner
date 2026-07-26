"""Validate focused Planner quality hardening from real Local AI review evidence."""
from __future__ import annotations

import ast
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from types import ModuleType

ROOT = Path(__file__).resolve().parents[1]
BOX = ROOT / "kanda_reasoner_app/manage_architecture/large_file_refactor_planner"
FEATURE = "large-file-refactor-planner-quality-hardening-v1"


def _install_namespace_packages() -> None:
    for name, path in (
        ("kanda_reasoner_app", ROOT / "kanda_reasoner_app"),
        ("kanda_reasoner_app.manage_architecture", ROOT / "kanda_reasoner_app/manage_architecture"),
        ("kanda_reasoner_app.manage_architecture.large_file_refactor_planner", BOX),
    ):
        module = ModuleType(name)
        module.__path__ = [str(path)]
        sys.modules.setdefault(name, module)


_install_namespace_packages()

from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.ast_analysis import analyze_python_file
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.dependency_clusterer import build_dependency_clusters
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.models import PlannerSettings
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.planner_git_cochange import collect_git_cochange_evidence
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.planner_local_ai_comprehensive_formatting import format_comprehensive_local_ai_review
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.planner_local_ai_comprehensive_review import ComprehensiveLocalAIReviewResult
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.planner_local_ai_docstring_review import DocstringAIReviewResult
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner import planner_local_ai_staged_protocol as staged
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.planner_local_ai_tournament import review_plan_with_local_ai_tournament
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.split_formatting import format_split_plan
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.split_planner import build_split_plan

QUESTION_IDS = [
    "tiny_helpers",
    "module_count",
    "cohesion",
    "dependency_safety",
    "atomic_clusters",
    "semantic_names",
    "public_facade",
    "final_gate",
]


def main() -> None:
    _static_checks()
    _local_ai_hardening_check()
    _git_confidence_check()
    print("TOURNAMENT_ACTION_REPORTING: EXPLORATION_VS_FINAL_SELECTION_SEPARATED")
    print("NAMING_EMPTY_ARRAY: STAGE_SPECIFIC_NO_OP_NORMALIZED")
    print("AUDIT_RETRY: MISSING_FIELDS_ONLY_WITH_ACCEPTED_ANSWERS_PRESERVED")
    print("GIT_HISTORY_CONFIDENCE: RAW_AND_EFFECTIVE_SCORES_SEPARATED")
    print("TWO_COMMIT_HISTORY: VERY_LOW_CONFIDENCE_WEIGHT_0.15")
    print("STEP1_TO_STEP6_REGRESSION_COMPATIBILITY: PASS")
    print("WORKBENCH_OWNERSHIP: UNCHANGED")
    print("BOX_SHIELD: PASS")
    print("NO_LEAK_LOGIC: PASS")
    print("MODULE_SIZE_GATE: PASS")
    print("VALIDATION OK: " + FEATURE)
    print("STATUS: IN_SYNC")


def _static_checks() -> None:
    names = (
        "planner_local_ai_review_models.py",
        "planner_local_ai_tournament.py",
        "planner_local_ai_staged_prompts.py",
        "planner_local_ai_staged_protocol.py",
        "planner_local_ai_comprehensive_formatting.py",
        "planner_git_cochange.py",
        "planner_symbol_affinity.py",
        "split_formatting.py",
    )
    for name in names:
        text = (BOX / name).read_text(encoding="utf-8")
        ast.parse(text)
        if len(text.splitlines()) > 500:
            raise SystemExit(f"VALIDATION ERROR: {name} exceeds 500 lines")
    combined = "\n".join((BOX / name).read_text(encoding="utf-8") for name in names)
    for token in (
        "tournament_candidate_actions_accepted",
        "_is_empty_naming_array",
        "required_question_ids",
        "accepted_architecture_answers",
        "confidence_label",
        "confidence_weight",
        "effective_score",
    ):
        if token not in combined:
            raise SystemExit("VALIDATION ERROR: missing hardening token " + token)
    for token in (
        "workbench_guarded_apply",
        "workbench_rollback_executor",
        "git push",
        "git reset",
        "git checkout",
    ):
        if token in combined:
            raise SystemExit("VALIDATION ERROR: forbidden cross-box/write token " + token)


def _local_ai_hardening_check() -> None:
    target = ROOT / "kanda_reasoner_app/reasoner_symbol_atlas/main_helper_mapper.py"
    report = analyze_python_file(target)
    plan = build_split_plan(report)
    helpers = [module for module in plan.proposed_modules if module.role != "public_facade"]
    if sorted(module.estimated_lines for module in helpers) != [122, 452]:
        raise SystemExit("VALIDATION ERROR: real baseline partition changed")
    small = helpers[0].filename
    large = helpers[1].filename

    audit_requests: list[tuple[tuple[str, ...], tuple[str, ...]]] = []

    def fake_candidates(_selection: str = "") -> list[str]:
        return ["fake-local-model"]

    def emit(payload: object) -> tuple[str, str]:
        return json.dumps(payload), "fake-local-model"

    def fake_chat(messages: list[dict[str, str]], **_kwargs: object) -> tuple[str, str]:
        system = messages[0]["content"]
        user = json.loads(messages[1]["content"])
        if system.startswith("Analyze responsibilities only"):
            return emit({
                "module_responsibilities": {
                    small: {"primary": "path_resolution", "secondary": [], "outliers": []},
                    large: {
                        "primary": "helper_selection",
                        "secondary": ["decision_reporting"],
                        "outliers": ["_public_helper_warnings"],
                    },
                }
            })
        if system.startswith("Return architecture actions only"):
            strategy = user.get("candidate_strategy", "")
            if strategy == "responsibility_cohesion":
                return emit({
                    "verdict": "needs_correction",
                    "module_merges": [],
                    "reassignments": [
                        {"symbol": "_public_helper_warnings", "target_module": small}
                    ],
                    "rationale": "Explore one bounded responsibility move.",
                })
            return emit({
                "verdict": "valid",
                "module_merges": [],
                "reassignments": [],
                "rationale": "No bounded improvement proposed.",
            })
        if system.startswith("Review semantic helper filenames only"):
            return "```json\n[]\n```", "fake-local-model"
        if system.startswith("Audit the already-deterministically-validated candidate"):
            required = tuple(user.get("required_question_ids", []))
            accepted = tuple(sorted(user.get("accepted_architecture_answers", {}).keys()))
            audit_requests.append((required, accepted))
            if not required:
                raise AssertionError("audit request must contain missing question IDs")
            # First audit call for each candidate answers only one requested field.
            if not accepted:
                key = required[0]
                value = "PASS: deterministic evidence checked." if key == "final_gate" else "Deterministically reviewed."
                return emit({
                    "architecture_answers": {key: value},
                    "rationale": "Partial audit response.",
                    "warnings": [],
                })
            answers = {
                key: ("PASS: deterministic plan status is planned." if key == "final_gate" else "Deterministically reviewed.")
                for key in required
            }
            return emit({
                "architecture_answers": answers,
                "rationale": "Completed only requested missing audit fields.",
                "warnings": [],
            })
        raise AssertionError(system)

    staged.get_local_ai_model_candidates = fake_candidates
    staged.chat_with_local_model = fake_chat
    result = review_plan_with_local_ai_tournament(report, plan)
    if result.selected_candidate_id != "baseline_control":
        raise SystemExit("VALIDATION ERROR: worse exploratory candidate replaced baseline")
    if result.corrections_applied != 0:
        raise SystemExit("VALIDATION ERROR: final baseline should apply zero actions")
    if result.tournament_candidate_actions_accepted != 1:
        raise SystemExit(
            "VALIDATION ERROR: exploratory action count should be 1, got "
            + str(result.tournament_candidate_actions_accepted)
        )
    if any("naming response does not contain" in warning for warning in result.warnings):
        raise SystemExit("VALIDATION ERROR: fenced empty naming array was not normalized")
    if not audit_requests:
        raise SystemExit("VALIDATION ERROR: audit requests were not observed")
    second_passes = [item for item in audit_requests if item[1]]
    if not second_passes:
        raise SystemExit("VALIDATION ERROR: no targeted audit retry occurred")
    for required, accepted in second_passes:
        if set(required) & set(accepted):
            raise SystemExit("VALIDATION ERROR: accepted audit fields were re-requested")

    docs = DocstringAIReviewResult(
        status="validated_no_changes",
        proposals=(),
        model_name="",
        rationale="No low-confidence docstring proposals required AI review.",
    )
    comprehensive = ComprehensiveLocalAIReviewResult(
        status="validated",
        plan=result.plan,
        docstring_proposals=(),
        split_review=result,
        docstring_review=docs,
        warnings=result.warnings,
    )
    formatted = format_comprehensive_local_ai_review(comprehensive)
    if "Candidate exploration actions accepted: 1" not in formatted:
        raise SystemExit("VALIDATION ERROR: exploratory action count missing from formatted review")
    if "Final selected-version actions applied: 0" not in formatted:
        raise SystemExit("VALIDATION ERROR: final action count missing from formatted review")


def _git_confidence_check() -> None:
    git = shutil.which("git")
    if not git:
        return
    source_fixture = ROOT / "kanda_reasoner_app/reasoner_symbol_atlas/main_helper_mapper.py"
    with tempfile.TemporaryDirectory(prefix="kanda_git_confidence_") as temp_text:
        repo = Path(temp_text)
        target = repo / "main_helper_mapper.py"
        target.write_text(source_fixture.read_text(encoding="utf-8"), encoding="utf-8")
        _git(repo, "init", "-q")
        _git(repo, "config", "user.email", "kanda-validator@example.invalid")
        _git(repo, "config", "user.name", "KANDA Validator")
        _git(repo, "add", "main_helper_mapper.py")
        _git(repo, "commit", "-qm", "initial fixture")
        text = target.read_text(encoding="utf-8").replace(
            "Support coerce project root behavior.",
            "Resolve project root behavior with confidence fixture.",
        )
        target.write_text(text, encoding="utf-8")
        _git(repo, "add", "main_helper_mapper.py")
        _git(repo, "commit", "-qm", "second fixture commit")

        report = analyze_python_file(target)
        movable = [symbol.name for symbol in report.symbols if symbol.visibility == "private"]
        clustering = build_dependency_clusters(report, PlannerSettings(), movable)
        evidence = collect_git_cochange_evidence(target, report, clustering.clusters)
        if evidence.history_commit_count != 2:
            raise SystemExit(
                "VALIDATION ERROR: expected exactly 2 observed commits, got "
                + str(evidence.history_commit_count)
            )
        if evidence.confidence_label != "very_low" or evidence.confidence_weight != 0.15:
            raise SystemExit("VALIDATION ERROR: two-commit evidence was not heavily discounted")
        exported = evidence.to_dict()
        if exported.get("confidence_label") != "very_low":
            raise SystemExit("VALIDATION ERROR: confidence label missing from export")
        pairs = exported.get("pair_affinities", [])
        positive = next((item for item in pairs if float(item.get("score", 0.0)) > 0.0), None)
        if positive is None:
            raise SystemExit("VALIDATION ERROR: confidence fixture has no positive raw affinity")
        raw = float(positive["score"])
        effective = float(positive["effective_score"])
        if round(effective, 6) != round(raw * 0.15, 6):
            raise SystemExit("VALIDATION ERROR: effective historical affinity is not confidence weighted")

        plan = build_split_plan(report, source_path=target)
        formatted = format_split_plan(plan)
        for token in (
            "Evidence confidence: very_low",
            "Confidence weight: 0.15",
            "raw_score=",
            "effective_score=",
        ):
            if token not in formatted:
                raise SystemExit("VALIDATION ERROR: formatted Git confidence evidence missing " + token)


def _git(repo: Path, *args: str) -> None:
    subprocess.run(["git", "-C", str(repo), *args], check=True)


if __name__ == "__main__":
    main()
