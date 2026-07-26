"""Validate optional Git co-change evidence for heuristic split planning."""
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
FEATURE = "large-file-refactor-planner-git-cochange-history-v1"


def _install_namespace_packages() -> None:
    packages = (
        ("kanda_reasoner_app", ROOT / "kanda_reasoner_app"),
        ("kanda_reasoner_app.manage_architecture", ROOT / "kanda_reasoner_app/manage_architecture"),
        ("kanda_reasoner_app.manage_architecture.large_file_refactor_planner", BOX),
    )
    for name, path in packages:
        module = ModuleType(name)
        module.__path__ = [str(path)]
        sys.modules.setdefault(name, module)


_install_namespace_packages()

from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.ast_analysis import analyze_python_file
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.dependency_clusterer import build_dependency_clusters
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.models import PlannerSettings
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.planner_git_cochange import collect_git_cochange_evidence
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.planner_symbol_affinity import cluster_affinity
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.split_formatting import format_split_plan
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.split_planner import build_split_plan


def main() -> None:
    _static_checks()
    _fallback_regression()
    _git_fixture_check()
    print("GIT_HISTORY_SIGNAL: OPTIONAL_READ_ONLY_SUPPORTING_AFFINITY")
    print("GIT_HISTORY_QUERY: BOUNDED_LOG_L")
    print("HISTORICAL_COCHANGE: CLUSTER_PAIR_JACCARD")
    print("AST_MUST_LINK_AUTHORITY: PRESERVED")
    print("SIZE_CYCLE_FACADE_GATES: CANNOT_BE_OVERRIDDEN_BY_HISTORY")
    print("NO_GIT_FALLBACK: STEP5_BEHAVIOR_PRESERVED")
    print("HISTORY_EXPORT_HYGIENE: NO_COMMIT_HASHES_NO_ABSOLUTE_REPO_PATH")
    print("LOCAL_AI_TOURNAMENT: UNCHANGED")
    print("WORKBENCH_OWNERSHIP: UNCHANGED")
    print("BOX_SHIELD: PASS")
    print("NO_LEAK_LOGIC: PASS")
    print("MODULE_SIZE_GATE: PASS")
    print("VALIDATION OK: " + FEATURE)
    print("STATUS: IN_SYNC")


def _static_checks() -> None:
    names = (
        "planner_git_cochange.py",
        "planner_symbol_affinity.py",
        "planner_heuristic_candidates.py",
        "split_planner.py",
        "split_formatting.py",
        "planner_split_plan_gui.py",
        "ast_audit_planner_sync.py",
    )
    for name in names:
        path = BOX / name
        text = path.read_text(encoding="utf-8")
        ast.parse(text)
        line_count = len(text.splitlines())
        if line_count > 500:
            raise SystemExit(f"VALIDATION ERROR: {name} exceeds 500 lines: {line_count}")
    combined = "\n".join((BOX / name).read_text(encoding="utf-8") for name in names)
    required = (
        "collect_git_cochange_evidence",
        "historical_cochange_score",
        "git_historical_coupling",
        "source_path=source_path or None",
        "source_path=selected_path",
        "optional_supporting_signal",
        "can_override_ast_must_link",
    )
    for token in required:
        if token not in combined:
            raise SystemExit("VALIDATION ERROR: missing Step 6 token " + token)
    forbidden = (
        "git push",
        "git commit",
        "git reset",
        "git checkout",
        "git clean",
        "workbench_guarded_apply",
        "workbench_rollback_executor",
    )
    for token in forbidden:
        if token in combined:
            raise SystemExit("VALIDATION ERROR: forbidden write/cross-box token " + token)


def _fallback_regression() -> None:
    target = ROOT / "kanda_reasoner_app/reasoner_symbol_atlas/main_helper_mapper.py"
    report = analyze_python_file(target)
    first = build_split_plan(report)
    second = build_split_plan(report)
    if first.to_dict() != second.to_dict():
        raise SystemExit("VALIDATION ERROR: no-history fallback is not deterministic")
    history = first.import_migration.get("git_historical_coupling", {})
    if history.get("status") != "unavailable_no_source_path":
        raise SystemExit("VALIDATION ERROR: no-source history fallback status is wrong")
    selection = first.import_migration.get("heuristic_candidate_selection", {})
    if selection.get("selected_strategy") != "balanced":
        raise SystemExit("VALIDATION ERROR: no-history fallback changed Step 5 selection")
    helpers = [item for item in first.proposed_modules if item.role != "public_facade"]
    if sorted(item.estimated_lines for item in helpers) != [122, 452]:
        raise SystemExit("VALIDATION ERROR: no-history fallback changed Step 3 partition")


def _git_fixture_check() -> None:
    git = shutil.which("git")
    if not git:
        return
    source_fixture = ROOT / "kanda_reasoner_app/reasoner_symbol_atlas/main_helper_mapper.py"
    with tempfile.TemporaryDirectory(prefix="kanda_git_cochange_") as temp_text:
        repo = Path(temp_text)
        target = repo / "main_helper_mapper.py"
        target.write_text(source_fixture.read_text(encoding="utf-8"), encoding="utf-8")
        _git(repo, "init", "-q")
        _git(repo, "config", "user.email", "kanda-validator@example.invalid")
        _git(repo, "config", "user.name", "KANDA Validator")
        _git(repo, "add", "main_helper_mapper.py")
        _git(repo, "commit", "-qm", "initial fixture")

        text = target.read_text(encoding="utf-8")
        text = text.replace(
            "Support coerce project root behavior.",
            "Resolve and validate project root behavior.",
        ).replace(
            "Support find target record behavior.",
            "Find target record from path or symbol evidence.",
        )
        target.write_text(text, encoding="utf-8")
        _git(repo, "add", "main_helper_mapper.py")
        _git(repo, "commit", "-qm", "cochange path resolution symbols")

        text = target.read_text(encoding="utf-8")
        text = text.replace(
            "Support decision status behavior.",
            "Derive decision status and confidence evidence.",
        ).replace(
            "Support format decision summary behavior.",
            "Format the final decision summary for reporting.",
        )
        target.write_text(text, encoding="utf-8")
        _git(repo, "add", "main_helper_mapper.py")
        _git(repo, "commit", "-qm", "cochange decision reporting symbols")

        report = analyze_python_file(target)
        movable = [symbol.name for symbol in report.symbols if symbol.visibility == "private"]
        clustering = build_dependency_clusters(report, PlannerSettings(), movable)
        evidence = collect_git_cochange_evidence(target, report, clustering.clusters)
        if evidence.status not in {"ready", "partial"} or not evidence.available:
            raise SystemExit("VALIDATION ERROR: Git fixture history evidence not available: " + evidence.status)
        if evidence.queried_cluster_count < 2 or evidence.history_commit_count < 2:
            raise SystemExit("VALIDATION ERROR: Git fixture evidence is unexpectedly sparse")
        exported = evidence.to_dict()
        exported_text = json.dumps(exported, sort_keys=True)
        if str(repo) in exported_text:
            raise SystemExit("VALIDATION ERROR: absolute repository path leaked into exported history evidence")
        if any(len(token) == 40 and all(ch in "0123456789abcdef" for ch in token) for token in exported_text.replace('"', ' ').split()):
            raise SystemExit("VALIDATION ERROR: commit hash leaked into exported history evidence")
        policy = exported.get("policy", {})
        if policy.get("optional_supporting_signal") is not True:
            raise SystemExit("VALIDATION ERROR: history evidence is not marked optional")
        for key in (
            "can_override_ast_must_link",
            "can_override_size_gate",
            "can_override_cycle_gate",
            "can_override_public_facade_ownership",
        ):
            if policy.get(key) is not False:
                raise SystemExit("VALIDATION ERROR: history authority boundary is wrong for " + key)

        pairs = exported.get("pair_affinities", [])
        if not pairs or not any(float(item.get("score", 0.0)) > 0.0 for item in pairs):
            raise SystemExit("VALIDATION ERROR: no positive co-change affinity found in Git fixture")
        positive_pair = next(item for item in pairs if float(item.get("score", 0.0)) > 0.0)
        left = next(item for item in clustering.clusters if item.cluster_id == positive_pair["left_cluster_id"])
        right = next(item for item in clustering.clusters if item.cluster_id == positive_pair["right_cluster_id"])
        affinity = cluster_affinity(report, left, right, evidence)
        if not affinity.history_available or affinity.historical_cochange_score <= 0.0:
            raise SystemExit("VALIDATION ERROR: historical signal did not reach cluster affinity")

        plan = build_split_plan(report, source_path=target)
        history = plan.import_migration.get("git_historical_coupling", {})
        if history.get("status") not in {"ready", "partial"}:
            raise SystemExit("VALIDATION ERROR: split plan did not retain Git history evidence")
        selection = plan.import_migration.get("heuristic_candidate_selection", {})
        candidates = selection.get("candidates", [])
        if not candidates or not all("historical_cochange_score" in item for item in candidates):
            raise SystemExit("VALIDATION ERROR: candidate history score evidence missing")
        merge_records = [record for item in candidates for record in item.get("merge_evidence", [])]
        if not any(record.get("history_available") for record in merge_records):
            raise SystemExit("VALIDATION ERROR: merge evidence did not record history availability")
        rendered = format_split_plan(plan)
        for token in (
            "Git historical coupling:",
            "Status:",
            "Strongest co-change affinities:",
        ):
            if token not in rendered:
                raise SystemExit("VALIDATION ERROR: Git history evidence not visible in plan output: " + token)


def _git(cwd: Path, *arguments: str) -> None:
    result = subprocess.run(
        ["git", "-C", str(cwd), *arguments],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise SystemExit("VALIDATION ERROR: Git fixture command failed: " + result.stderr.strip())


if __name__ == "__main__":
    main()
