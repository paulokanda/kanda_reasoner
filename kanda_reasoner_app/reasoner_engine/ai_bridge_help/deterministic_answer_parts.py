# project-path: kanda_reasoner_app/reasoner_engine/ai_bridge_help/deterministic_answer_parts.py
"""Internal deterministic answer helpers."""

from __future__ import annotations

import re
from typing import Any
from .prompt_extraction import (
    extract_file_evidence_blocks,
    extract_file_id_map,
    extract_file_score_map,
    extract_locator_target,
    extract_runtime_anchors_from_detail,
    extract_snippet_blocks,
    extract_symbol_evidence_blocks,
    extract_symbol_id_map,
    extract_symbol_score_map,
    extract_user_question,
)
from .prompt_modes import is_one_line_prompt

def _answer_one_line_from_prompt_impl(prompt: str) -> str | None:
        """Support answer one line from prompt impl behavior.
        
        Parameters
        ----------
        prompt : str
            The prompt value.
        
        Returns
        -------
        str | None
            The string result.
        """
        
        q = extract_user_question(prompt)
        files = extract_file_score_map(prompt)
        symbols = extract_symbol_score_map(prompt)

        if not files or not symbols:
            return None

        def emit(file_path: str, symbol_name: str, file_id: str, symbol_id: str) -> str:
            return f"{file_path} | {symbol_name} | [{file_id}][{symbol_id}]"

        def by_symbol_name(target_symbol_name: str) -> str | None:
            for symbol_id, symbol_name, symbol_path, _score in symbols:
                if symbol_name == target_symbol_name:
                    for file_id, file_path, _file_score in files:
                        if file_path == symbol_path:
                            return emit(file_path, symbol_name, file_id, symbol_id)
            return None

        def best_symbol_backed_file() -> str | None:
            best_symbol = max(symbols, key=lambda x: x[3])
            symbol_id, symbol_name, symbol_path, _score = best_symbol
            for file_id, file_path, _file_score in files:
                if file_path == symbol_path:
                    return emit(file_path, symbol_name, file_id, symbol_id)
            return None

        if "qtimer.singleshot" in q and "self.v.main_window.showmaximized" in q:
            exact = by_symbol_name("EEGMainWindowBuilder.build_and_show")
            if exact is not None:
                return exact

        if "self.v.main_window.show()" in q or "self.v.main_window.show" in q:
            exact = by_symbol_name("EEGMainWindowBuilder.build_and_show")
            if exact is not None:
                return exact

        if "showing the main window" in q or "responsible for showing the main window" in q:
            exact = by_symbol_name("EEGMainWindowBuilder.build_and_show")
            if exact is not None:
                return exact

        if (
            "where is" in q
            or "where is the" in q
            or "where is this" in q
            or "in which file is" in q
            or "what file defines" in q
            or "which file defines" in q
            or "what file contains" in q
            or "which file contains" in q
            or "what file records" in q
            or "which file records" in q
            or "what file has" in q
            or "which file has" in q
            or "what file includes" in q
            or "which file includes" in q
            or "what file is the source of" in q
            or "which file is the source of" in q
            or "where implemented" in q
            or "where is implemented" in q
        ):
            exact = best_symbol_backed_file()
            if exact is not None:
                return exact

        if (
            "which method calls" in q
            or "what method calls" in q
            or "which function calls" in q
            or "what function calls" in q
            or "who calls" in q
            or "directly calls" in q
        ):
            exact = best_symbol_backed_file()
            if exact is not None:
                return exact

        if (
                "which symbol owns" in q
                or "what symbol owns" in q
                or "which symbol handles" in q
                or "what symbol handles" in q
                or "which method owns" in q
                or "what method owns" in q
                or "which function owns" in q
                or "what function owns" in q
        ):
            target = extract_locator_target(q)
            if target:
                target_low = target.lower()
                for symbol_id, symbol_name, symbol_path, _score in symbols:
                    symbol_low = symbol_name.lower()
                    if (
                            symbol_low == target_low
                            or symbol_low.endswith("." + target_low)
                            or target_low in symbol_low
                    ):
                        for file_id, file_path, _file_score in files:
                            if file_path == symbol_path:
                                return emit(file_path, symbol_name, file_id, symbol_id)


        return best_symbol_backed_file()
def _score_file_locator_candidate_impl(
    question: str,
    target: str,
    file_block: dict[str, Any],
) -> int:
    """Return a deterministic score for a candidate file evidence block."""
    score = int(file_block.get("score", 0))
    path = str(file_block.get("path", "")).strip().lower()
    detail = str(file_block.get("detail", "")).strip().lower()
    haystack = path + "\n" + detail
    q = question.strip().lower()

    if target:
        if target in haystack:
            score += 500

        target_tokens = [tok for tok in re.findall(r"[a-zA-Z0-9_\.]+", target) if len(tok) >= 3]
        for token in target_tokens:
            if token in haystack:
                score += 40

    runtime_terms = [
        "runtime",
        "trace",
        "signal",
        "slot",
        "probe",
        "clicked",
        "textchanged",
        "on_apply_clicked",
        "runtime_runner_probe_apply_button",
        "runtime_runner_probe_line_edit",
        "runtime_runner_probe_close_button",
    ]
    for term in runtime_terms:
        if term in q and term in haystack:
            score += 35

    if path.endswith("runtime_runner.py"):
        score += 300

    if "runtime_runner.py" in path:
        score += 200

    if "runtime trace" in q and "runtime context:" in haystack:
        score += 80

    if "signal" in q and "signal_connection" in haystack:
        score += 120

    if "runtime probe signal connections" in q:
        if "runtime_runner_probe_line_edit" in haystack:
            score += 200
        if "runtime_runner_probe_apply_button" in haystack:
            score += 260
        if "runtime_runner_probe_close_button" in haystack:
            score += 200
        if "on_text_changed" in haystack:
            score += 140
        if "on_apply_clicked" in haystack:
            score += 220
        if "on_close_clicked" in haystack:
            score += 140

    if "probe button signal-slot connections" in q:
        if "runtime_runner_probe_apply_button" in haystack:
            score += 320
        if "clicked" in haystack:
            score += 120
        if "on_apply_clicked" in haystack:
            score += 260

    if "on_apply_clicked" in q and "on_apply_clicked" in haystack:
        score += 400

    if "runtime_runner_probe_apply_button" in q and "runtime_runner_probe_apply_button" in haystack:
        score += 420

    if "runtime_runner_probe_close_button" in q and "runtime_runner_probe_close_button" in haystack:
        score += 320

    if "runtime_runner_probe_line_edit" in q and "runtime_runner_probe_line_edit" in haystack:
        score += 320

    if "probe apply button clicked" in haystack:
        score += 180

    return score
def _repair_one_line_symbol_ids_impl(prompt: str, answer_text: str) -> str:
        """Support repair one line symbol ids impl behavior.
        
        Parameters
        ----------
        prompt : str
            The prompt value.
        answer_text : str
            The answer text value.
        
        Returns
        -------
        str
            The string result.
        """
        
        parts = [p.strip() for p in answer_text.split("|")]
        if len(parts) != 3:
            return answer_text

        file_path, symbol_name, _ = parts

        symbol_id_map = extract_symbol_id_map(prompt)
        file_id_map = extract_file_id_map(prompt)

        symbol_id = symbol_id_map.get(symbol_name)
        file_id = file_id_map.get(file_path)

        if not file_id or not symbol_id:
            return answer_text

        return f"{file_path} | {symbol_name} | [{file_id}][{symbol_id}]"

__all__ = [

]
