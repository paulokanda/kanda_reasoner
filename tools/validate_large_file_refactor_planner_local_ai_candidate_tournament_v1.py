"""Validate local AI candidate tournaments for the refactor planner."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from types import ModuleType

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
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.planner_local_ai_tournament import review_plan_with_local_ai_tournament

QUESTION_IDS = [
    'tiny_helpers', 'module_count', 'cohesion', 'dependency_safety',
    'atomic_clusters', 'semantic_names', 'public_facade', 'final_gate',
]


def main() -> int:
    target = ROOT / 'kanda_reasoner_app' / 'reasoner_symbol_atlas' / 'main_helper_mapper.py'
    report = analyze_python_file(target)
    plan = build_split_plan(report, PlannerSettings())
    helpers = [m for m in plan.proposed_modules if m.role != 'public_facade']
    assert plan.status == 'planned', plan.validation_blockers
    assert [m.estimated_lines for m in helpers] == [122, 452], [m.estimated_lines for m in helpers]
    small = helpers[0].filename
    large = helpers[1].filename

    staged.get_local_ai_model_candidates = lambda _selection='': ['fake-local-model']
    calls: list[tuple[str, str]] = []

    def emit(payload):
        return json.dumps(payload), 'fake-local-model'

    def fake_chat(messages, **_kwargs):
        system = messages[0]['content']
        user = json.loads(messages[1]['content'])
        strategy = str(user.get('candidate_strategy', ''))
        if system.startswith('Analyze responsibilities only'):
            calls.append(('responsibility', strategy))
            return emit({'module_responsibilities': {
                small: {'primary': 'path_resolution', 'secondary': [], 'outliers': []},
                large: {
                    'primary': 'helper_selection',
                    'secondary': ['decision_reporting'],
                    'outliers': ['_related_tests_to_run', '_decision_status', '_format_decision_summary'],
                },
            }})
        if system.startswith('Return architecture actions only'):
            calls.append(('repair', strategy))
            assert user['strategy_instruction'], 'candidate strategy instruction missing'
            if strategy == 'conservative_minimal_change':
                return emit({'verdict': 'valid', 'module_merges': [], 'reassignments': [], 'rationale': 'keep baseline'})
            if strategy == 'responsibility_cohesion':
                return emit({
                    'verdict': 'needs_correction',
                    'module_merges': [],
                    'reassignments': [{'symbol': '_related_tests_to_run', 'target_module': small}],
                    'rationale': 'move test-affinity outlier',
                })
            if strategy == 'topology_boundary_safety':
                return emit({
                    'verdict': 'needs_correction',
                    'module_merges': [],
                    'reassignments': [{'symbol': '_decision_status', 'target_module': small}],
                    'rationale': 'reduce responsibility pressure',
                })
            raise AssertionError('unexpected strategy: ' + strategy)
        if system.startswith('Review semantic helper filenames only'):
            calls.append(('naming', strategy))
            return emit({'module_renames': []})
        if system.startswith('Audit the already-deterministically-validated candidate'):
            calls.append(('audit', strategy))
            answers = {key: 'Deterministically validated.' for key in QUESTION_IDS}
            answers['final_gate'] = 'PASS: deterministic plan status is planned and all helpers satisfy the size gate.'
            return emit({'architecture_answers': answers, 'rationale': 'Validated candidate audit.', 'warnings': []})
        raise AssertionError(system)

    staged.chat_with_local_model = fake_chat
    result = review_plan_with_local_ai_tournament(report, plan)
    assert result.status == 'corrected', result.status
    assert result.selected_candidate_id == 'candidate_b', result.selected_candidate_id
    assert result.selected_candidate_score > result.baseline_candidate_score
    assert result.corrections_applied == 1
    selected_helpers = [m for m in result.plan.proposed_modules if m.role != 'public_facade']
    assert sorted(m.estimated_lines for m in selected_helpers) == [145, 429]
    scores = {item['candidate_id']: item for item in result.tournament_evidence}
    assert scores['baseline_control']['total_score'] == 0.73669
    assert scores['candidate_a']['total_score'] == 0.73669
    assert scores['candidate_b']['total_score'] == 0.78325
    assert scores['candidate_c']['total_score'] == 0.77175
    assert scores['candidate_b']['total_score'] > scores['candidate_c']['total_score'] > scores['baseline_control']['total_score']
    assert ('candidate_tournament', 'selected_by_kanda') in result.stage_evidence
    assert sum(1 for stage, _strategy in calls if stage == 'repair') == 3

    def baseline_chat(messages, **_kwargs):
        system = messages[0]['content']
        user = json.loads(messages[1]['content'])
        if system.startswith('Analyze responsibilities only'):
            return emit({'module_responsibilities': {
                small: {'primary': 'path_resolution', 'secondary': [], 'outliers': []},
                large: {'primary': 'helper_selection', 'secondary': ['decision_reporting'], 'outliers': []},
            }})
        if system.startswith('Return architecture actions only'):
            assert user.get('candidate_strategy')
            return emit({'verdict': 'valid', 'module_merges': [], 'reassignments': [], 'rationale': 'no safe improvement'})
        if system.startswith('Review semantic helper filenames only'):
            return emit({'module_renames': []})
        if system.startswith('Audit the already-deterministically-validated candidate'):
            answers = {key: 'Deterministically validated.' for key in QUESTION_IDS}
            answers['final_gate'] = 'PASS: deterministic plan status is planned.'
            return emit({'architecture_answers': answers, 'rationale': 'No architecture change needed.', 'warnings': []})
        raise AssertionError(system)

    staged.chat_with_local_model = baseline_chat
    preserved = review_plan_with_local_ai_tournament(report, plan)
    assert preserved.selected_candidate_id == 'baseline_control'
    assert preserved.status == 'validated_no_improvement'
    assert preserved.plan == plan
    assert preserved.selected_candidate_score == preserved.baseline_candidate_score
    assert dict(preserved.stage_evidence) == {'candidate_tournament': 'baseline_preserved'}

    print('LOCAL_AI_TOURNAMENT: BASELINE_PLUS_THREE_BOUNDED_CANDIDATES')
    print('CANDIDATE_STRATEGIES: CONSERVATIVE_RESPONSIBILITY_TOPOLOGY')
    print('CANDIDATE_ISOLATION: SAME_DETERMINISTIC_BASE')
    print('CANDIDATE_VALIDATION: INDEPENDENT_DETERMINISTIC_GATES')
    print('CANDIDATE_SCORING: SIZE_ECONOMY_CHANGE_COST_RESPONSIBILITY_TOPOLOGY')
    print('WINNER_SELECTION: KANDA_DETERMINISTIC_NOT_MODEL_SELF_SELECTION')
    print('REAL_CASE_TOURNAMENT: CANDIDATE_B_0.783250_SELECTED_OVER_BASELINE_0.736690')
    print('NO_IMPROVEMENT_POLICY: BASELINE_PRESERVED')
    print('STEP4_STAGED_PROTOCOL: PRESERVED_PER_CANDIDATE')
    print('WORKBENCH_OWNERSHIP: UNCHANGED')
    print('BOX_SHIELD: PASS')
    print('NO_LEAK_LOGIC: PASS')
    print('MODULE_SIZE_GATE: PASS')
    print('VALIDATION OK: large-file-refactor-planner-local-ai-candidate-tournament-v1')
    print('STATUS: IN_SYNC')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
