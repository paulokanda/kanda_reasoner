"""Validate Routing Signal Scorer contract refactor train car 1."""

from __future__ import annotations

import ast
import sys
from pathlib import Path

__all__: list[str] = []


PROJECT_ROOT = Path(__file__).resolve().parents[1]

def _ensure_project_root_on_path() -> None:
    """Add the project root to sys.path only for direct script execution."""
    root_text = str(PROJECT_ROOT)
    if root_text not in sys.path:
        sys.path.insert(0, root_text)

PKG = PROJECT_ROOT / "kanda_reasoner_app" / "routing_signal_scorer"

PUBLIC_NAMES = [
    "build_routing_advisory",
    "build_similarity_box_shield_status",
    "build_similarity_prompt_context_preview",
    "build_similarity_runtime_lite_advisory",
    "build_similarity_ui_preview_adapter",
    "render_similarity_box_shield_status_text",
    "render_similarity_prompt_context_preview_text",
    "render_similarity_ui_preview_text",
    "score_routing_signals",
    "SignalRule",
    "summarize_advisory",
    "summarize_signal_result",
    "summarize_similarity_runtime_lite_advisory",
]

PRIVATE_COMPAT_NAMES = [
    "_rules",
    "_route_family_suggestions",
    "_candidate_prompt_contexts_for_route_families",
    "_similarity_ui_preview_lines",
    "_similarity_prompt_context_preview_lines",
    "_load_similarity_corpus",
    "_text_profile",
    "_similarity_decision_report",
    "_merge_route_family_suggestions",
]

EXPECTED_MODULES = {
    "contract.py": "facade",
    "models.py": "constants seam",
    "scoring.py": "diagnostic scoring",
    "advisory.py": "route-family advisory",
    "similarity_runtime.py": "runtime-lite similarity",
    "similarity_preview.py": "presentation adapters",
    "shield.py": "similarity box shield",
}


def _line_count(path: Path) -> int:
    return len(path.read_text(encoding="utf-8").splitlines())


def _parse(path: Path) -> ast.Module:
    return ast.parse(path.read_text(encoding="utf-8"), filename=str(path))


def _top_level_functions(path: Path) -> set[str]:
    return {node.name for node in _parse(path).body if isinstance(node, ast.FunctionDef)}


def _top_level_classes(path: Path) -> set[str]:
    return {node.name for node in _parse(path).body if isinstance(node, ast.ClassDef)}


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    _ensure_project_root_on_path()
    for name in EXPECTED_MODULES:
        _assert((PKG / name).exists(), f"missing module: {name}")

    counts = {name: _line_count(PKG / name) for name in EXPECTED_MODULES}
    _assert(counts["contract.py"] <= 160, f"contract.py is not a thin facade: {counts['contract.py']} lines")
    for name, count in counts.items():
        _assert(count <= 500, f"{name} exceeds v7.2 500-line maximum: {count}")
    for name in ["scoring.py", "advisory.py", "similarity_runtime.py", "similarity_preview.py", "shield.py"]:
        _assert(counts[name] >= 100, f"substantive helper too small under v7.2: {name}={counts[name]}")
    _assert(counts["models.py"] >= 50, "models.py constants seam unexpectedly tiny")

    contract_text = (PKG / "contract.py").read_text(encoding="utf-8")
    _assert("Public compatibility facade" in contract_text, "contract facade docstring missing")
    _assert("from .scoring import" in contract_text, "contract does not re-export scoring module")
    _assert("from .advisory import" in contract_text, "contract does not re-export advisory module")
    _assert("from .similarity_runtime import" in contract_text, "contract does not re-export similarity runtime module")
    _assert("from .similarity_preview import" in contract_text, "contract does not re-export similarity preview module")
    _assert("from .shield import" in contract_text, "contract does not re-export shield module")

    import kanda_reasoner_app.routing_signal_scorer.contract as contract

    for name in PUBLIC_NAMES:
        _assert(hasattr(contract, name), f"missing public API from contract facade: {name}")
        _assert(name in contract.__all__, f"public API missing from __all__: {name}")
    for name in PRIVATE_COMPAT_NAMES:
        _assert(hasattr(contract, name), f"missing compatibility private helper: {name}")

    # Ownership checks.
    _assert("score_routing_signals" in _top_level_functions(PKG / "scoring.py"), "score_routing_signals not owned by scoring.py")
    _assert("_rules" in _top_level_functions(PKG / "scoring.py"), "rules not owned by scoring.py")
    _assert("build_routing_advisory" in _top_level_functions(PKG / "advisory.py"), "build_routing_advisory not owned by advisory.py")
    _assert("build_similarity_runtime_lite_advisory" in _top_level_functions(PKG / "similarity_runtime.py"), "runtime-lite advisory not owned by similarity_runtime.py")
    _assert("_load_similarity_corpus" in _top_level_functions(PKG / "similarity_runtime.py"), "similarity corpus loader not owned by similarity_runtime.py")
    _assert("build_similarity_ui_preview_adapter" in _top_level_functions(PKG / "similarity_preview.py"), "UI preview adapter not owned by similarity_preview.py")
    _assert("build_similarity_prompt_context_preview" in _top_level_functions(PKG / "similarity_preview.py"), "prompt context preview not owned by similarity_preview.py")
    _assert("build_similarity_box_shield_status" in _top_level_functions(PKG / "shield.py"), "shield status not owned by shield.py")
    _assert("SignalRule" in _top_level_classes(PKG / "models.py"), "SignalRule not owned by models.py")

    # Behavioral safety smoke checks.
    sample = "Create a patch ZIP with install and validation commands after local validation passes."
    score = contract.score_routing_signals(sample)
    _assert(score["feature_id"] == "routing_signal_scorer_v1_diagnostic", "scoring feature id changed")
    _assert(score["authority"] == "diagnostic_only", "scoring authority changed")
    _assert(score["does_not_override_router"] is True, "scoring router override guard changed")
    _assert("pre_output_contract_gates" in score["recommended_hooks"], "pre-output hook missing for patch signal")

    advisory = contract.build_routing_advisory(sample)
    _assert(advisory["authority"] == "advisory_only", "advisory authority changed")
    _assert(advisory["may_proceed_now_decision"] == "not_provided_by_advisory", "advisory May-proceed guard changed")
    _assert(advisory["route_override"] is None, "advisory route override guard changed")

    similarity = contract.build_similarity_runtime_lite_advisory(sample)
    _assert(similarity["authority"] == "advisory_only", "similarity authority changed")
    _assert(similarity["runtime_status"] == "RUNTIME_LITE", "similarity runtime status changed")
    _assert(similarity["self_learning_enabled"] is False, "similarity self-learning guard changed")
    _assert(similarity["automatic_prompt_loading"] is False, "similarity prompt-loading guard changed")
    _assert(similarity["external_dependencies"] == [], "similarity dependency guard changed")

    ui_preview = contract.build_similarity_ui_preview_adapter(sample)
    _assert(ui_preview["adapter_scope"] == "gui_log_preview_only", "UI preview scope changed")
    _assert(ui_preview["automatic_prompt_loading"] is False, "UI preview prompt-loading guard changed")
    _assert("Routing Signal Scorer v2 Similarity Preview" in contract.render_similarity_ui_preview_text(ui_preview), "UI preview text missing header")

    prompt_preview = contract.build_similarity_prompt_context_preview(sample)
    _assert(prompt_preview["candidate_contexts_only"] is True, "prompt preview candidate-only guard changed")
    _assert(prompt_preview["required_prompts_final_decision"] == "not_provided_by_similarity", "prompt final-decision guard changed")
    _assert("candidate contexts are not final required prompts" in contract.render_similarity_prompt_context_preview_text(prompt_preview), "prompt preview guard text missing")

    shield = contract.build_similarity_box_shield_status(sample)
    _assert(shield["authority"] == "shield_contract_only", "shield authority changed")
    _assert(shield["automatic_prompt_loading"] is False, "shield prompt-loading guard changed")
    _assert(shield["stronger_ml_enabled"] is False, "shield stronger-ML guard changed")
    _assert(shield["external_dependencies"] == [], "shield dependency guard changed")
    _assert("Routing Signal Scorer v2 Similarity Box Shield" in contract.render_similarity_box_shield_status_text(shield), "shield text missing header")

    print("VALIDATION OK: routing-signal-scorer-contract-refactor-train-car-1-v1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
