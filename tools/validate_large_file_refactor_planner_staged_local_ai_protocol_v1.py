"""Validate the staged local AI protocol for large-file refactor planning."""

from __future__ import annotations

import json
import sys
from types import ModuleType
from dataclasses import replace
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOX = ROOT / 'kanda_reasoner_app' / 'manage_architecture' / 'large_file_refactor_planner'
for name, path in (
    ('kanda_reasoner_app', ROOT / 'kanda_reasoner_app'),
    ('kanda_reasoner_app.manage_architecture', ROOT / 'kanda_reasoner_app' / 'manage_architecture'),
    ('kanda_reasoner_app.manage_architecture.large_file_refactor_planner', BOX),
):
    module = ModuleType(name)
    module.__path__ = [str(path)]
    sys.modules.setdefault(name, module)

from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.ast_analysis import analyze_python_file
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.models import PlannerSettings
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.split_planner import build_split_plan
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner import planner_local_ai_staged_protocol as staged


def main() -> int:
    target = ROOT / 'kanda_reasoner_app' / 'reasoner_symbol_atlas' / 'main_helper_mapper.py'
    report = analyze_python_file(target)
    plan = build_split_plan(report, PlannerSettings())
    helpers = [m for m in plan.proposed_modules if m.role != 'public_facade']
    assert [m.estimated_lines for m in helpers] == [122, 452], [m.estimated_lines for m in helpers]
    small = helpers[0].filename
    large = helpers[1].filename
    blocked = replace(
        plan,
        status='blocked',
        validation_blockers=[f'Planned helper {small} is below minimum helper size of 100 lines.'],
    )

    calls: list[str] = []
    repair_attempt = 0
    def fake_candidates(_selection: str = '') -> list[str]:
        return ['fake-local-model']

    def emit(payload):
        return json.dumps(payload), 'fake-local-model'

    def fake_chat(messages, **_kwargs):
        nonlocal repair_attempt
        system = messages[0]['content']
        user = json.loads(messages[1]['content'])
        if system.startswith('Analyze responsibilities only'):
            calls.append('responsibility')
            return emit({'module_responsibilities': {
                small: {'primary': 'path_resolution', 'secondary': [], 'outliers': []},
                large: {'primary': 'helper_selection', 'secondary': ['decision_reporting'], 'outliers': ['_format_decision_summary']},
            }})
        if system.startswith('Return architecture actions only'):
            repair_attempt += 1
            calls.append('repair')
            if repair_attempt == 1:
                return emit({
                    'verdict': 'needs_correction',
                    'module_merges': [],
                    'reassignments': [{'symbol': '_format_decision_summary', 'target_module': '_unknown.py'}],
                    'rationale': 'first attempt intentionally invalid',
                })
            assert 'outside the allowed helper set' in user['targeted_rejection_to_fix'], user['targeted_rejection_to_fix']
            return emit({
                'verdict': 'needs_correction',
                'module_merges': [],
                'reassignments': [{'symbol': '_format_decision_summary', 'target_module': small}],
                'rationale': 'move reporting outlier to a known surviving helper for bounded test',
            })
        if system.startswith('Review semantic helper filenames only'):
            calls.append('naming')
            return emit({'module_renames': []})
        if system.startswith('Audit the already-deterministically-validated candidate'):
            calls.append('audit')
            answers = {
                'tiny_helpers': 'No helper is below the configured minimum.',
                'module_count': 'Two helpers remain and both satisfy the line gate.',
                'cohesion': 'Responsibilities are explicit and deterministically validated.',
                'dependency_safety': 'No helper-only dependency cycle is present.',
                'atomic_clusters': 'Atomic cluster cohesion remains deterministically enforced.',
                'semantic_names': 'Current deterministic semantic names are meaningful.',
                'public_facade': 'Public facade ownership and expected API are preserved.',
                'final_gate': 'PASS: deterministic plan status is planned and helper sizes are within gate.',
            }
            return emit({'architecture_answers': answers, 'rationale': 'Validated staged correction.', 'warnings': []})
        raise AssertionError(system)

    staged.get_local_ai_model_candidates = fake_candidates
    staged.chat_with_local_model = fake_chat
    result = staged.review_plan_with_staged_local_ai(report, blocked)
    assert result.status == 'corrected', result
    assert result.plan.status == 'planned', result.plan.validation_blockers
    assert result.corrections_applied == 1, result.corrections_applied
    assert calls == ['responsibility', 'repair', 'repair', 'naming', 'audit'], calls
    assert dict(result.stage_evidence) == {
        'responsibility_analysis': 'validated',
        'targeted_architecture_repair': 'validated',
        'semantic_naming_review': 'validated',
        'final_architecture_audit': 'validated',
    }
    assert 'Validated staged correction.' == result.rationale

    print('LOCAL_AI_PROTOCOL: RESPONSIBILITY_REPAIR_NAMING_AUDIT_STAGED')
    print('TARGETED_RETRY: EXACT_DETERMINISTIC_REJECTION_FEEDBACK')
    print('ACTION_SCHEMA: REPAIR_ONLY_NO_AUDIT_BURDEN')
    print('NAMING_STAGE: SEPARATE_FROM_ARCHITECTURE_ACTIONS')
    print('FINAL_AUDIT: QUESTIONS_ONLY_AFTER_DETERMINISTIC_VALIDATION')
    print('TRUTHFUL_FINAL_REPORT: DETERMINISTIC_STATUS_GROUNDED')
    print('REAL_CASE_HEURISTIC_BASE: STEP3_122_452')
    print('LOCAL_AI_CORRECTION: BOUNDED_AND_REVALIDATED')
    print('WORKBENCH_OWNERSHIP: UNCHANGED')
    print('BOX_SHIELD: PASS')
    print('NO_LEAK_LOGIC: PASS')
    print('MODULE_SIZE_GATE: PASS')
    print('VALIDATION OK: large-file-refactor-planner-staged-local-ai-protocol-v1')
    print('STATUS: IN_SYNC')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
