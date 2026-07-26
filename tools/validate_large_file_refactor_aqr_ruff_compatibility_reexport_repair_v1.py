"""Validate Ruff-safe explicit facade compatibility reexports."""
from __future__ import annotations

import ast
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
from types import SimpleNamespace

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT_TEXT = str(PROJECT_ROOT)
if PROJECT_ROOT_TEXT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT_TEXT)

from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.analyzer_tool_runtime_paths import (
    analyzer_environment_script,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.ast_analysis import (
    analyze_python_file,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.cst_real_preview_writer import (
    build_and_write_real_preview,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.planner_workbench_handoff import (
    export_latest_planner_workbench_handoff,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.real_preview_structural_validator import (
    validate_real_preview_structure,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.split_planner import (
    build_split_plan,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_dependency_readiness import (
    build_workbench_dependency_readiness,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_plan_intake import (
    build_workbench_plan_intake,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_plan_snapshot import (
    build_workbench_plan_snapshot,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_project_support_paths import (
    resolve_workbench_preview_root,
)
from kanda_reasoner_app.manage_architecture.large_module_split_audit import (
    run_large_module_split_audit,
)

FEATURE_ID = 'large-file-refactor-aqr-ruff-compatibility-reexport-repair-v1'
TARGET_RELATIVE = Path('kanda_reasoner_app/routing_signal_scorer/similarity_runtime.py')
TARGET_HASH = '1aa8b65f8138d95efd5ce55c8ca7027b0604164727246df04e5499dcc9fd2406'
ENGINE_RELATIVE = Path(
    'kanda_reasoner_app/manage_architecture/large_file_refactor_planner/'
    'cst_preview_rendering.py'
)
EXPECTED_COMPATIBILITY_ONLY = {
    '_containment',
    '_jaccard',
    '_similarity_advisory_only_reason',
    '_similarity_rule_hook_independence_reason',
    '_tokenize_for_similarity',
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _ruff_executable(project_root: Path) -> Path:
    override = os.environ.get('KANDA_VALIDATION_RUFF_EXECUTABLE', '').strip()
    if override:
        candidate = Path(override).expanduser().resolve(strict=False)
        if candidate.is_file():
            return candidate
        raise AssertionError('RUFF_OVERRIDE_NOT_FOUND')
    pinned = analyzer_environment_script(project_root, 'ruff')
    if pinned.is_file():
        return pinned
    discovered = shutil.which('ruff')
    if discovered:
        return Path(discovered).resolve()
    raise AssertionError('RUFF_EXECUTABLE_NOT_FOUND')


def _run_ruff(preview_root: Path, project_root: Path) -> list[dict[str, object]]:
    ruff = _ruff_executable(project_root)
    completed = subprocess.run(
        [
            str(ruff),
            'check',
            str(preview_root),
            '--output-format',
            'json',
            '--exit-zero',
        ],
        cwd=str(preview_root),
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='replace',
        check=False,
    )
    if completed.returncode != 0:
        raise AssertionError('RUFF_PROCESS_FAILED:' + completed.stderr.strip())
    payload = json.loads(completed.stdout or '[]')
    if not isinstance(payload, list):
        raise AssertionError('RUFF_OUTPUT_NOT_LIST')
    return payload


def _explicit_self_aliases(source: str) -> set[str]:
    names: set[str] = set()
    tree = ast.parse(source)
    for node in tree.body:
        if not isinstance(node, ast.ImportFrom):
            continue
        for alias in node.names:
            if alias.asname and alias.asname == alias.name:
                names.add(alias.name)
    return names


def _all_values(source: str) -> set[str]:
    tree = ast.parse(source)
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        if not any(isinstance(target, ast.Name) and target.id == '__all__' for target in node.targets):
            continue
        if isinstance(node.value, (ast.List, ast.Tuple)):
            return {
                str(item.value)
                for item in node.value.elts
                if isinstance(item, ast.Constant) and isinstance(item.value, str)
            }
    return set()


def main() -> int:
    project_root = PROJECT_ROOT.resolve()
    target = (project_root / TARGET_RELATIVE).resolve()
    engine = (project_root / ENGINE_RELATIVE).resolve()

    if _sha256(target) != TARGET_HASH:
        raise AssertionError('EXACT_TARGET_HASH_MISMATCH')

    analysis = analyze_python_file(target)
    plan = build_split_plan(
        analysis,
        source_path=target,
        preferred_strategy='responsibility_dominant',
    )
    if plan.status != 'planned' or plan.validation_blockers:
        raise AssertionError('PLANNER_PLAN_NOT_READY:' + '|'.join(plan.validation_blockers))

    window = SimpleNamespace(
        _large_file_refactor_last_plan=plan,
        _large_file_refactor_last_analysis=analysis,
        _large_file_refactor_planner_candidates=[SimpleNamespace(path=str(target))],
    )
    handoff = export_latest_planner_workbench_handoff(window)
    snapshot = build_workbench_plan_snapshot(handoff)
    intake = build_workbench_plan_intake(
        snapshot=snapshot,
        active_project_root=str(project_root),
    )
    if intake.status != 'plan_intake_ready' or intake.blockers:
        raise AssertionError('PLAN_INTAKE_BLOCKED:' + '|'.join(intake.blockers))

    readiness = build_workbench_dependency_readiness(intake)
    if readiness.status != 'dependency_readiness_ready' or readiness.blockers:
        raise AssertionError('DEPENDENCY_READINESS_BLOCKED:' + '|'.join(readiness.blockers))

    preview_root = resolve_workbench_preview_root(
        project_root,
        'validation_aqr_ruff_compatibility_reexport_repair_v1',
    )
    preview = build_and_write_real_preview(
        plan=plan,
        intake=intake,
        dependency_readiness=readiness,
        active_project_root=str(project_root),
        preview_root=str(preview_root),
    )
    if preview.status != 'real_preview_written' or preview.blockers:
        raise AssertionError('REAL_PREVIEW_BLOCKED:' + '|'.join(preview.blockers))

    facade = preview_root / 'similarity_runtime.py'
    facade_text = facade.read_text(encoding='utf-8', errors='strict')
    aliases = _explicit_self_aliases(facade_text)
    if not EXPECTED_COMPATIBILITY_ONLY <= aliases:
        missing = sorted(EXPECTED_COMPATIBILITY_ONLY - aliases)
        raise AssertionError('EXPLICIT_COMPATIBILITY_REEXPORTS_MISSING:' + ','.join(missing))
    if EXPECTED_COMPATIBILITY_ONLY & _all_values(facade_text):
        raise AssertionError('PRIVATE_COMPATIBILITY_REEXPORT_LEAKED_TO_ALL')

    findings = _run_ruff(preview_root, project_root)
    if findings:
        details = [
            str(item.get('code')) + ':' + str(item.get('message'))
            for item in findings
            if isinstance(item, dict)
        ]
        raise AssertionError('RUFF_PREVIEW_FINDINGS:' + '|'.join(details))

    structural = validate_real_preview_structure(
        plan=plan,
        preview_result=preview,
        active_project_root=str(project_root),
    )
    if structural.status not in {'passed', 'passed_with_warnings'} or structural.blockers:
        raise AssertionError('STRUCTURAL_VALIDATION_BLOCKED:' + '|'.join(structural.blockers))

    if _sha256(target) != TARGET_HASH:
        raise AssertionError('TARGET_SOURCE_MUTATED_DURING_VALIDATION')

    line_count = len(engine.read_text(encoding='utf-8').splitlines())
    if not 100 < line_count < 500:
        raise AssertionError('TOUCHED_ENGINE_LINE_LAW:' + str(line_count))

    audit = run_large_module_split_audit(
        project_root,
        engine,
        classifier_mode='heuristic',
    )
    classification = audit.data.get('refactor_safety_classification', {})
    if classification.get('label') != 'SAFE REFACTORING':
        raise AssertionError('TOUCHED_ENGINE_AST_NOT_SAFE')
    if classification.get('hard_blockers'):
        raise AssertionError('TOUCHED_ENGINE_AST_HARD_BLOCKERS')

    print('EXACT_TARGET_HASH_MATCH: PASS')
    print('PLAN_INTAKE_AND_DEPENDENCY_READINESS: PASS')
    print('REAL_PREVIEW_WRITTEN: PASS')
    print('FIVE_COMPATIBILITY_ONLY_REEXPORTS_EXPLICIT: PASS')
    print('PRIVATE_COMPATIBILITY_REEXPORTS_STAY_OUTSIDE_ALL: PASS')
    print('RUFF_PREVIEW_ZERO_FINDINGS: PASS')
    print('AQR_RUFF_FIVE_F401_REGRESSIONS_REMOVED: PASS')
    print('STRUCTURAL_VALIDATION: PASS')
    print('TARGET_SOURCE_MUTATION_DISABLED: PASS')
    print('TOUCHED_ENGINE_LINE_LAW_101_499: PASS')
    print('FRESH_TOUCHED_ENGINE_AST_SAFE: PASS')
    print('VALIDATION OK: ' + FEATURE_ID)
    print('STATUS: IN_SYNC')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
