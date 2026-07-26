# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/planner_local_ai_staged_prompts.py
"""Small JSON-only prompts for staged local-AI architecture correction."""
from __future__ import annotations

import json
from typing import Any

from .models import ModuleAnalysisReport, RefactorPlan
from .planner_ai_architecture_questions import architecture_review_payload

__all__ = [
    "audit_messages",
    "naming_messages",
    "repair_messages",
    "responsibility_messages",
]


def responsibility_messages(report: ModuleAnalysisReport, plan: RefactorPlan) -> list[dict[str, str]]:
    payload = _plan_payload(report, plan)
    system = (
        "Analyze responsibilities only. Return JSON only. Do not propose merges, moves, "
        "renames, source code, or new modules. Schema: {\"module_responsibilities\":{"
        "\"known_helper.py\":{\"primary\":\"short label\","
        "\"secondary\":[\"label\"],\"outliers\":[\"known_symbol\"]}}}. "
        "Use only helpers and symbols supplied in the payload."
    )
    return _messages(system, payload)


def repair_messages(
    report: ModuleAnalysisReport,
    plan: RefactorPlan,
    responsibilities: dict[str, Any],
    rejection: str = "",
    candidate_strategy: str = "",
    strategy_instruction: str = "",
) -> list[dict[str, str]]:
    payload = _plan_payload(report, plan)
    payload["responsibility_analysis"] = responsibilities
    payload["targeted_rejection_to_fix"] = rejection
    payload["candidate_strategy"] = candidate_strategy
    payload["strategy_instruction"] = strategy_instruction
    system = (
        "Return architecture actions only as JSON. Solve current deterministic blockers or "
        "meaningful mixed-responsibility pressure using the smallest safe change. Do not answer "
        "audit questions and do not rename modules in this stage. Use only known helpers and "
        "known movable symbols. Preserve atomic clusters and public facade ownership. Schema: "
        "{\"verdict\":\"valid|needs_correction\","
        "\"module_merges\":[{\"source_module\":\"known.py\","
        "\"target_module\":\"known.py\"}],"
        "\"reassignments\":[{\"symbol\":\"known_symbol\","
        "\"target_module\":\"known.py\"}],\"rationale\":\"short text\"}. "
        "If targeted_rejection_to_fix is non-empty, correct only that rejected action pattern. "
        "Follow candidate_strategy and strategy_instruction to produce a distinct bounded alternative."
    )
    return _messages(system, payload)


def naming_messages(
    report: ModuleAnalysisReport,
    plan: RefactorPlan,
    responsibilities: dict[str, Any],
) -> list[dict[str, str]]:
    payload = _plan_payload(report, plan)
    payload["responsibility_analysis"] = responsibilities
    system = (
        "Review semantic helper filenames only. Return JSON only. Do not merge or move symbols. "
        "Rename only surviving known helpers. Keep names private underscore-prefixed Python "
        "basenames and describe the real responsibility. Schema: {\"module_renames\":["
        "{\"module\":\"known.py\",\"new_filename\":\"_semantic_name.py\"}]}. "
        "Use an empty list when current names are already meaningful."
    )
    return _messages(system, payload)


def audit_messages(
    report: ModuleAnalysisReport,
    plan: RefactorPlan,
    responsibilities: dict[str, Any],
    *,
    required_question_ids: list[str] | None = None,
    accepted_answers: dict[str, str] | None = None,
) -> list[dict[str, str]]:
    payload = _plan_payload(report, plan)
    payload["responsibility_analysis"] = responsibilities
    payload["architecture_review"] = architecture_review_payload(plan)
    payload["required_question_ids"] = list(required_question_ids or [])
    payload["accepted_architecture_answers"] = dict(accepted_answers or {})
    system = (
        "Audit the already-deterministically-validated candidate. Return JSON only. Answer only "
        "the required_question_ids supplied in the payload; do not repeat accepted answers and do "
        "not propose actions. Schema: "
        "{\"architecture_answers\":{\"question_id\":\"answer\"},"
        "\"rationale\":\"short truthful summary\",\"warnings\":[\"text\"]}. "
        "Your final_gate answer must match the supplied deterministic plan status and blockers."
    )
    return _messages(system, payload)


def _plan_payload(report: ModuleAnalysisReport, plan: RefactorPlan) -> dict[str, Any]:
    helpers = [module for module in plan.proposed_modules if module.role != "public_facade"]
    movable = sorted({name for module in helpers for name in module.symbols})
    evidence = plan.import_migration if isinstance(plan.import_migration, dict) else {}
    return {
        "target_name": report.target_file.rsplit("/", 1)[-1].rsplit("\\", 1)[-1],
        "plan_status": plan.status,
        "validation_blockers": list(plan.validation_blockers),
        "risks": list(plan.risks),
        "allowed_helper_modules": [module.filename for module in helpers],
        "movable_symbols": movable,
        "proposed_modules": [module.to_dict() for module in plan.proposed_modules],
        "responsibility_labeling": evidence.get("responsibility_labeling", {}),
        "projected_dependency_topology": evidence.get("projected_dependency_topology", {}),
        "heuristic_candidate_selection": evidence.get("heuristic_candidate_selection", {}),
        "symbol_evidence": [
            {
                "name": symbol.name,
                "physical_lines": symbol.physical_lines,
                "references": symbol.references,
                "atomic_cluster_id": symbol.atomic_cluster_id,
            }
            for symbol in report.symbols
            if symbol.name in set(movable)
        ],
    }


def _messages(system: str, payload: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": json.dumps(payload, sort_keys=True, ensure_ascii=True)},
    ]
