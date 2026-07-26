"""Validate Routing Signal Scorer contract refactor completion guard.

This guard intentionally performs no source split.  It freezes the post-Train-Car-1
state as complete under the v7.2 no-tiny-helper rule.
"""

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

REFACTOR_CORE_MODULES = {
    "contract.py": "thin public compatibility facade",
    "models.py": "justified constants/dataclass seam",
    "scoring.py": "rule-based diagnostic scoring",
    "advisory.py": "route-family advisory",
    "similarity_runtime.py": "deterministic runtime-lite lexical similarity",
    "similarity_preview.py": "candidate-only UI and prompt-context preview adapters",
    "shield.py": "similarity box shield status and rendering",
}

SUBSTANTIVE_HELPERS = [
    "scoring.py",
    "advisory.py",
    "similarity_runtime.py",
    "similarity_preview.py",
    "shield.py",
]

PUBLIC_API = [
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

PRIVATE_COMPAT = [
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

OWNERSHIP = {
    "scoring.py": ["score_routing_signals", "summarize_signal_result", "_rules", "_add_score", "_add_evidence"],
    "advisory.py": ["build_routing_advisory", "summarize_advisory", "_route_family_suggestions", "_caution_flags"],
    "similarity_runtime.py": ["build_similarity_runtime_lite_advisory", "_load_similarity_corpus", "_similarity_decision_report", "_text_profile"],
    "similarity_preview.py": ["build_similarity_ui_preview_adapter", "build_similarity_prompt_context_preview", "render_similarity_ui_preview_text"],
    "shield.py": ["build_similarity_box_shield_status", "render_similarity_box_shield_status_text"],
}


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _line_count(path: Path) -> int:
    return len(path.read_text(encoding="utf-8").splitlines())


def _parse(path: Path) -> ast.Module:
    return ast.parse(path.read_text(encoding="utf-8"), filename=str(path))


def _top_level_functions(path: Path) -> set[str]:
    return {node.name for node in _parse(path).body if isinstance(node, ast.FunctionDef)}


def _top_level_classes(path: Path) -> set[str]:
    return {node.name for node in _parse(path).body if isinstance(node, ast.ClassDef)}


def _module_text(name: str) -> str:
    return (PKG / name).read_text(encoding="utf-8")


def _assert_line_policy(counts: dict[str, int]) -> None:
    _assert(counts["contract.py"] <= 160, f"contract.py is no longer a thin facade: {counts['contract.py']} lines")
    for name in REFACTOR_CORE_MODULES:
        _assert(counts[name] <= 500, f"refactor-created core helper exceeds v7.2 500-line maximum: {name}={counts[name]}")
    for name in SUBSTANTIVE_HELPERS:
        _assert(counts[name] >= 100, f"substantive helper became suspiciously tiny under v7.2: {name}={counts[name]}")
    _assert(50 <= counts["models.py"] <= 100, f"models.py should remain a small justified constants/dataclass seam: {counts['models.py']}")


def _assert_facade_contract() -> None:
    text = _module_text("contract.py")
    _assert("Public compatibility facade" in text, "contract.py facade docstring missing")
    for import_marker in [
        "from .models import",
        "from .scoring import",
        "from .advisory import",
        "from .similarity_runtime import",
        "from .similarity_preview import",
        "from .shield import",
    ]:
        _assert(import_marker in text, f"contract.py missing facade re-export marker: {import_marker}")

    import kanda_reasoner_app.routing_signal_scorer.contract as contract

    for name in PUBLIC_API:
        _assert(hasattr(contract, name), f"missing public contract API: {name}")
        _assert(name in contract.__all__, f"public API missing from __all__: {name}")
    for name in PRIVATE_COMPAT:
        _assert(hasattr(contract, name), f"missing private compatibility helper: {name}")


def _assert_ownership() -> None:
    _assert("SignalRule" in _top_level_classes(PKG / "models.py"), "models.py no longer owns SignalRule")
    for module_name, expected_functions in OWNERSHIP.items():
        functions = _top_level_functions(PKG / module_name)
        for function_name in expected_functions:
            _assert(function_name in functions, f"{module_name} no longer owns {function_name}")


def _assert_authority_boundaries() -> None:
    import kanda_reasoner_app.routing_signal_scorer.contract as contract

    sample = "Create a patch ZIP with install and validation commands after local validation passes."

    score = contract.score_routing_signals(sample)
    _assert(score["authority"] == "diagnostic_only", "score authority changed")
    _assert(score["does_not_override_router"] is True, "score router override guard changed")

    advisory = contract.build_routing_advisory(sample)
    _assert(advisory["authority"] == "advisory_only", "advisory authority changed")
    _assert(advisory["may_proceed_now_decision"] == "not_provided_by_advisory", "advisory May-proceed guard changed")
    _assert(advisory["route_override"] is None, "advisory route override changed")

    similarity = contract.build_similarity_runtime_lite_advisory(sample)
    _assert(similarity["authority"] == "advisory_only", "similarity authority changed")
    _assert(similarity["runtime_status"] == "RUNTIME_LITE", "similarity runtime status changed")
    _assert(similarity["external_dependencies"] == [], "similarity dependency guard changed")
    _assert(similarity["self_learning_enabled"] is False, "similarity self-learning guard changed")
    _assert(similarity["automatic_prompt_loading"] is False, "similarity prompt-loading guard changed")

    ui_preview = contract.build_similarity_ui_preview_adapter(sample)
    _assert(ui_preview["adapter_scope"] == "gui_log_preview_only", "UI preview scope changed")
    _assert(ui_preview["automatic_prompt_loading"] is False, "UI preview prompt-loading guard changed")

    prompt_preview = contract.build_similarity_prompt_context_preview(sample)
    _assert(prompt_preview["candidate_contexts_only"] is True, "prompt preview candidate-only guard changed")
    _assert(prompt_preview["required_prompts_final_decision"] == "not_provided_by_similarity", "prompt preview final decision guard changed")

    shield = contract.build_similarity_box_shield_status(sample)
    _assert(shield["authority"] == "shield_contract_only", "shield authority changed")
    _assert(shield["automatic_prompt_loading"] is False, "shield prompt-loading guard changed")
    _assert(shield["stronger_ml_enabled"] is False, "shield stronger-ML guard changed")
    _assert(shield["external_dependencies"] == [], "shield dependency guard changed")
    shield_text = contract.render_similarity_box_shield_status_text(shield)
    _assert("no_authority_escalation" in shield_text.lower() or "no authority escalation" in shield_text.lower(), "shield text no longer reports no authority escalation")
    _assert("stronger_ml_enabled" in shield_text or "stronger ML" in shield_text or "stronger ml" in shield_text.lower(), "shield text no longer reports stronger-ML status")


def main() -> int:
    _ensure_project_root_on_path()
    for name in REFACTOR_CORE_MODULES:
        _assert((PKG / name).exists(), f"missing refactor core module: {name}")

    counts = {name: _line_count(PKG / name) for name in REFACTOR_CORE_MODULES}
    _assert_line_policy(counts)
    _assert_facade_contract()
    _assert_ownership()
    _assert_authority_boundaries()

    # Completion decision: created refactor core is cohesive and below the maximum.
    # Existing design/manifest files in this package are outside this contract.py
    # refactor train and are not used as pressure to split this already-complete island.
    print("VALIDATION OK: routing-signal-scorer-contract-refactor-completion-guard-v1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
