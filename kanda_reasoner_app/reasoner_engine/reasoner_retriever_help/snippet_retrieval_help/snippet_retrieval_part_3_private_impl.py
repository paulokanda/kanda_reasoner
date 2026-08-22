# project-path: kanda_reasoner_app/reasoner_engine/reasoner_retriever_help/snippet_retrieval_help/snippet_retrieval_part_3_private_impl.py
"""Private snippet retrieval helper implementation part 3."""

from __future__ import annotations

from kanda_reasoner_app.reasoner_engine.v10_models import (
    EvidenceItem,
    SymbolEvidenceItem,
)
from kanda_reasoner_app.reasoner_engine.reasoner_retriever_help.query_text import (
    is_allowed_project_path,
    is_auxiliary_ui_path,
    safe_read_text,
)

__all__ = []


def _bind_root_globals(root_globals):
    """Support bind root globals behavior.
    
    Parameters
    ----------
    root_globals : object
        The root globals value.
    """
    
    skipped = {
        '__name__',
        '__package__',
        '__loader__',
        '__spec__',
        '__file__',
        '__cached__',
        '__builtins__',
    }
    for name, value in root_globals.items():
        if name not in skipped and name not in globals():
            globals()[name] = value


def _sr_score_symbol_snippet_candidate_impl(
    retriever,
    q: str,
    intents: dict[str, bool],
    item: SymbolEvidenceItem,
    file_rank: dict[str, int],
) -> int:
    """Support sr score symbol snippet candidate impl behavior.
    
    Parameters
    ----------
    retriever : object
        The retriever value.
    q : str
        The q value.
    intents : dict[str, bool]
        The intents value.
    item : SymbolEvidenceItem
        The item value.
    file_rank : dict[str, int]
        The file rank value.
    
    Returns
    -------
    int
        The integer result.
    """
    
    score = int(item.score)
    symbol_low = item.symbol_name.lower()
    last_part = symbol_low.split(".")[-1]
    normalized_path = item.path.replace("\\", "/").lower()

    rank_bonus = max(0, 40 - (file_rank.get(item.path, 20) * 5))
    score += rank_bonus

    if any(
        marker in symbol_low
        for marker in [
            "build",
            "build_and_show",
            "init",
            "initialize",
            "connect",
            "load",
            "show",
            "update",
            "refresh",
            "render",
            "plot",
            "draw",
            "attach",
            "create",
            "main",
            "run",
        ]
    ):
        score += 90

    if last_part.startswith("on_"):
        score += 70

    record = retriever.idx.symbol_details.get(item.symbol_name, {}).get("record", {})
    if isinstance(record, dict):
        call_count = len(record.get("calls", []))
        score += min(50, call_count * 5)

    if intents["runtime_heavy"]:
        if last_part in {"on_apply_clicked", "on_text_changed", "on_close_clicked"}:
            score += 220
        if any(
            marker in symbol_low
            for marker in [
                "runtime_runner_probe_apply_button",
                "runtime_runner_probe_line_edit",
                "runtime_runner_probe_close_button",
            ]
        ):
            score += 160

    if (
        retriever._question_has_profile_alias(q, "topomap_explanation")
        or intents["topomap_explanation"]
    ):
        if any(
            term in symbol_low
            for term in ["topomap", "amplitude", "render", "plot", "draw"]
        ):
            score += 140

    if retriever._question_has_profile_alias(q, "timeline"):
        if any(
            term in symbol_low
            for term in retriever._profile_alias_terms("timeline_symbol_terms")
        ):
            score += 140

        if any(
            owner_path in normalized_path
            for owner_path in retriever._profile_owner_paths("timeline_owner_paths")
        ):
            score += 80

    if (
        "line numbers" in q
        or "with code" in q
        or "show code" in q
        or "code localization" in q
    ):
        score += 30

    return score

def _sr_score_file_snippet_candidate_impl(
    retriever,
    q: str,
    intents: dict[str, bool],
    item: EvidenceItem,
) -> int:
    """Support sr score file snippet candidate impl behavior.
    
    Parameters
    ----------
    retriever : object
        The retriever value.
    q : str
        The q value.
    intents : dict[str, bool]
        The intents value.
    item : EvidenceItem
        The item value.
    
    Returns
    -------
    int
        The integer result.
    """
    
    score = int(item.score)
    path_low = item.path.replace("\\", "/").lower()
    entry_files = {
        path
        for path in retriever.idx.project_summary.get("entry_files", [])
        if is_allowed_project_path(path)
    }

    if item.path in entry_files:
        score += 140

    if any(
        term in path_low
        for term in [
            "main",
            "builder",
            "launcher",
            "initializer",
            "manager",
            "controller",
            "runner",
            "viewer",
            "interface_manager",
        ]
    ):
        score += 60

    if intents["runtime_heavy"] and "runtime_runner.py" in path_low:
        score += 220

    if (
        retriever._question_has_profile_alias(q, "topomap_explanation")
        or intents["topomap_explanation"]
    ) and any(
        term in path_low
        for term in ["topomap", "amplitude_map", "render", "controller"]
    ):
        score += 160

    if retriever._question_has_profile_alias(q, "timeline"):
        if any(
            term in path_low
            for term in retriever._profile_alias_terms("timeline_symbol_terms")
        ):
            score += 140

        if any(
            owner_path in path_low
            for owner_path in retriever._profile_owner_paths("timeline_owner_paths")
        ):
            score += 80

    if is_auxiliary_ui_path(item.path) and "help" not in q:
        score -= 50

    return score

def _sr_snippet_radius_for_symbol_impl(
    retriever,
    q: str,
    intents: dict[str, bool],
    item: SymbolEvidenceItem,
) -> int:
    """Support sr snippet radius for symbol impl behavior.
    
    Parameters
    ----------
    retriever : object
        The retriever value.
    q : str
        The q value.
    intents : dict[str, bool]
        The intents value.
    item : SymbolEvidenceItem
        The item value.
    
    Returns
    -------
    int
        The integer result.
    """
    
    anchor_low = item.symbol_name.lower()

    if any(
        term in anchor_low
        for term in ["topomap", "draw", "render", "plot", "topography"]
    ):
        return 28

    if any(
        term in anchor_low
        for term in [
            "build",
            "init",
            "initialize",
            "connect",
            "load",
            "show",
            "update",
            "refresh",
            "attach",
        ]
    ):
        return 24 if (intents["explanatory"] or intents["code_localized_explanation"]) else 20

    if anchor_low.split(".")[-1].startswith("on_"):
        return 22 if intents["runtime_heavy"] else 20

    if intents["runtime_heavy"] and any(
        term in anchor_low for term in ["apply", "clicked", "text_changed", "close"]
    ):
        return 22

    if (
        "line numbers" in q
        or "with code" in q
        or "show code" in q
        or "code localization" in q
    ):
        return 24

    return 20

def _sr_read_snippet_impl(retriever, abs_path: str, line: int, radius: int) -> str:
    """Support sr read snippet impl behavior.
    
    Parameters
    ----------
    retriever : object
        The retriever value.
    abs_path : str
        The abs path value.
    line : int
        The line value.
    radius : int
        The radius value.
    
    Returns
    -------
    str
        The string result.
    """
    
    text = safe_read_text(abs_path)
    lines = text.splitlines()
    if not lines:
        return ""

    start = max(1, line - radius)
    end = min(len(lines), line + radius)
    out: list[str] = []

    for idx in range(start, end + 1):
        out.append(str(idx).rjust(5) + " | " + lines[idx - 1])

    return "\n".join(out)
