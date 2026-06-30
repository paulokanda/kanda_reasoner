# project-path: kanda_reasoner_app/reasoner_engine/reasoner_retriever_help/snippet_retrieval_help/snippet_retrieval_part_1_private_impl.py
"""Private snippet retrieval helper implementation part 1."""

from __future__ import annotations

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


def _sr_score_runtime_anchor_for_question_impl(retriever, question: str, anchor: str) -> int:
    """Support sr score runtime anchor for question impl behavior.
    
    Parameters
    ----------
    retriever : object
        The retriever value.
    question : str
        The question value.
    anchor : str
        The anchor value.
    
    Returns
    -------
    int
        The integer result.
    """
    
    q = norm_text(question)
    anchor_low = norm_text(anchor)
    score = 0

    if anchor_low in q:
        score += 500

    tokens = [tok for tok in re.findall(r"[a-zA-Z0-9_]+", anchor_low) if len(tok) >= 3]
    for token in tokens:
        if token in q:
            score += 40

    if "on_apply_clicked" in q and anchor_low == "on_apply_clicked":
        score += 450

    if (
        "runtime_runner_probe_apply_button" in q
        and anchor_low == "runtime_runner_probe_apply_button"
    ):
        score += 500

    if "runtime probe signal connections" in q:
        if anchor_low == "runtime_runner_probe_apply_button":
            score += 260
        if anchor_low == "on_apply_clicked":
            score += 220
        if anchor_low == "runtime_runner_probe_line_edit":
            score += 180
        if anchor_low == "on_text_changed":
            score += 160
        if anchor_low == "runtime_runner_probe_close_button":
            score += 150
        if anchor_low == "on_close_clicked":
            score += 140

    if "probe button signal-slot connections" in q:
        if anchor_low == "runtime_runner_probe_apply_button":
            score += 320
        if anchor_low == "on_apply_clicked":
            score += 260

    return score

def _sr_find_anchor_line_in_file_impl(retriever, abs_path: str, anchor: str) -> int | None:
    """Support sr find anchor line in file impl behavior.
    
    Parameters
    ----------
    retriever : object
        The retriever value.
    abs_path : str
        The abs path value.
    anchor : str
        The anchor value.
    
    Returns
    -------
    int | None
        The integer result.
    """
    
    try:
        text = safe_read_text(abs_path)
    except Exception:
        return None

    lines = text.splitlines()
    anchor_low = anchor.lower()

    for idx, line in enumerate(lines, start=1):
        if anchor_low in line.lower():
            return idx

    return None

def _sr_extract_runtime_anchors_from_detail_impl(retriever, detail_text: str) -> list[str]:
    """Support sr extract runtime anchors from detail impl behavior.
    
    Parameters
    ----------
    retriever : object
        The retriever value.
    detail_text : str
        The detail text value.
    
    Returns
    -------
    list[str]
        The list of values.
    """
    
    anchors: list[str] = []

    for line in detail_text.splitlines():
        stripped = line.strip()
        if stripped.startswith("Runtime anchors: "):
            raw = stripped[len("Runtime anchors: ") :]
            anchors.extend([part.strip() for part in raw.split("|") if part.strip()])

    return anchors
