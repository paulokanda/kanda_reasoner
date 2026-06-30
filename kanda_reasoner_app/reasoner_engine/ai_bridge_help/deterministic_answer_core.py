# project-path: kanda_reasoner_app/reasoner_engine/ai_bridge_help/deterministic_answer_core.py
"""Core deterministic answer orchestration."""

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

from .deterministic_answer_parts import (
    _answer_one_line_from_prompt_impl,
    _repair_one_line_symbol_ids_impl,
    _score_file_locator_candidate_impl,
)

from .deterministic_answer_core_parts import (
    _extract_direct_responsibility_target,
    _extract_docstring_from_snippet,
    _find_best_runtime_anchor,
)

def _answer_deterministic_from_prompt_impl(prompt: str) -> str | None:
        """Support answer deterministic from prompt impl behavior.
        
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

        if is_one_line_prompt(prompt):
            return _answer_one_line_from_prompt_impl(prompt)

        file_blocks = extract_file_evidence_blocks(prompt)
        symbol_blocks = extract_symbol_evidence_blocks(prompt)
        snippet_blocks = extract_snippet_blocks(prompt)

        if not file_blocks and not symbol_blocks and not snippet_blocks:
            return None


        def answer_direct_responsibility_question(question_text: str) -> str | None:
            """Return deterministic responsibility answer from snippet docstring."""
            target = _extract_direct_responsibility_target(question_text)
            if not target:
                return None

            target_low = target.lower()
            target_short = target.split(".")[-1]
            target_short_low = target_short.lower()

            best_snippet: dict[str, Any] | None = None
            best_docstring = ""
            best_display_name = target_short

            for snippet_block in snippet_blocks:
                anchor = str(snippet_block.get("anchor", "")).strip()
                anchor_plain = anchor
                if anchor_plain.startswith("LIVE_SOURCE:"):
                    anchor_plain = anchor_plain[len("LIVE_SOURCE:"):].strip()

                text = str(snippet_block.get("text", "")).strip()
                haystack = (anchor + "\n" + text).lower()

                if (
                    anchor_plain.lower() != target_low
                    and anchor_plain.lower() != target_short_low
                    and ("class " + target_short_low) not in haystack
                    and ("def " + target_short_low) not in haystack
                    and ("async def " + target_short_low) not in haystack
                ):
                    continue

                docstring = _extract_docstring_from_snippet(text, target_short)
                if docstring:
                    best_snippet = snippet_block
                    best_docstring = docstring
                    if anchor_plain:
                        best_display_name = anchor_plain.split(".")[-1]
                    break

            if best_snippet is None or not best_docstring:
                return None

            snippet_id = str(best_snippet.get("snippet_id", "")).strip()
            snippet_path = str(best_snippet.get("path", "")).strip()
            snippet_line = int(best_snippet.get("line", 0))

            citation = "[" + snippet_id + "]" if snippet_id else ""
            location = snippet_path
            if snippet_line:
                location = location + ":" + str(snippet_line)

            return (
                best_display_name
                + " is responsible for "
                + best_docstring.rstrip(".")
                + ". Evidence: "
                + location
                + " "
                + citation
                + "."
            )

        direct_responsibility_answer = answer_direct_responsibility_question(q)
        if direct_responsibility_answer is not None:
            return direct_responsibility_answer

        is_symbol_locator = any(
            term in q
            for term in [
                "which symbol owns",
                "what symbol owns",
                "which symbol handles",
                "what symbol handles",
                "which method owns",
                "what method owns",
                "which function owns",
                "what function owns",
                "which symbol directly calls",
            ]
        )

        if is_symbol_locator:
            target = extract_locator_target(q)

            if target:
                target_low = target.lower()

                for symbol_block in symbol_blocks:
                    symbol_name = str(symbol_block.get("symbol_name", "")).strip()
                    symbol_name_low = symbol_name.lower()
                    symbol_path = str(symbol_block.get("path", "")).strip()
                    symbol_line = int(symbol_block.get("line", 0))
                    symbol_id = str(symbol_block.get("symbol_id", "")).strip()

                    if (
                            symbol_name_low == target_low
                            or symbol_name_low.endswith("." + target_low)
                            or target_low in symbol_name_low
                    ):
                        for file_block in file_blocks:
                            if str(file_block.get("path", "")).strip() == symbol_path:
                                file_id = str(file_block.get("file_id", "")).strip()
                                return (
                                        "The strongest evidence-backed symbol is "
                                        + symbol_name
                                        + " at "
                                        + symbol_path
                                        + ":"
                                        + str(symbol_line)
                                        + " ["
                                        + file_id
                                        + "]["
                                        + symbol_id
                                        + "]."
                                )

                        return (
                                "The strongest evidence-backed symbol is "
                                + symbol_name
                                + " at "
                                + symbol_path
                                + ":"
                                + str(symbol_line)
                                + " ["
                                + symbol_id
                                + "]."
                        )

                for snippet_block in snippet_blocks:
                    anchor = str(snippet_block.get("anchor", "")).strip()
                    anchor_low = anchor.lower()
                    snippet_path = str(snippet_block.get("path", "")).strip()
                    snippet_line = int(snippet_block.get("line", 0))
                    snippet_id = str(snippet_block.get("snippet_id", "")).strip()

                    if (
                            anchor_low == target_low
                            or anchor_low.endswith("." + target_low)
                            or target_low in anchor_low
                    ):
                        return (
                                "The strongest evidence-backed symbol is "
                                + anchor
                                + " at "
                                + snippet_path
                                + ":"
                                + str(snippet_line)
                                + " ["
                                + snippet_id
                                + "]."
                        )

                for file_block in file_blocks:
                    file_detail = str(file_block.get("detail", "")).strip()
                    file_path = str(file_block.get("path", "")).strip()
                    file_id = str(file_block.get("file_id", "")).strip()

                    runtime_anchor = _find_best_runtime_anchor(file_detail, q)
                    if runtime_anchor and target_low in runtime_anchor.lower():
                        return (
                                "The strongest runtime-backed symbol is "
                                + runtime_anchor
                                + " in "
                                + file_path
                                + " ["
                                + file_id
                                + "]. "
                                + "This symbol was captured from runtime signal connections, "
                                + "not from the static symbol index."
                        )

        is_file_locator = any(
            term in q
            for term in [
                "where is",
                "in which file is",
                "what file defines",
                "which file defines",
                "what file contains",
                "which file contains",
                "what file records",
                "which file records",
                "what file has",
                "which file has",
                "what file includes",
                "which file includes",
                "what file is the source of",
                "which file is the source of",
                "which file owns",
                "what file owns",
                "where implemented",
                "where is implemented",
            ]
        )

        if is_file_locator and file_blocks:
            target = extract_locator_target(q)

            best_file = max(
                file_blocks,
                key=lambda block: _score_file_locator_candidate_impl(q, target, block),
            )

            file_path = str(best_file.get("path", "")).strip()
            file_id = str(best_file.get("file_id", "")).strip()
            file_detail = str(best_file.get("detail", "")).strip()

            matching_symbol = None
            if target:
                for symbol_block in symbol_blocks:
                    symbol_name = str(symbol_block.get("symbol_name", "")).strip().lower()
                    symbol_path = str(symbol_block.get("path", "")).strip()
                    if symbol_path == file_path and symbol_name and symbol_name in target:
                        matching_symbol = symbol_block
                        break

            if matching_symbol is not None:
                symbol_name = str(matching_symbol.get("symbol_name", "")).strip()
                symbol_id = str(matching_symbol.get("symbol_id", "")).strip()
                line = int(matching_symbol.get("line", 0))
                return (
                        "The exact file is "
                        + file_path
                        + " ["
                        + file_id
                        + "]. The matching symbol is "
                        + symbol_name
                        + " at line "
                        + str(line)
                        + " ["
                        + symbol_id
                        + "]."
                )

            runtime_anchor = _find_best_runtime_anchor(file_detail, q)
            if runtime_anchor:
                return (
                        "The exact file is "
                        + file_path
                        + " ["
                        + file_id
                        + "]. The strongest runtime anchor is "
                        + runtime_anchor
                        + "."
                )

            return "The exact file is " + file_path + " [" + file_id + "]."

        is_calls_question = any(
            term in q
            for term in [
                "which method calls",
                "what method calls",
                "which function calls",
                "what function calls",
                "who calls",
                "directly calls",
            ]
        )

        if is_calls_question and symbol_blocks:
            best_symbol = max(symbol_blocks, key=lambda block: int(block.get("score", 0)))
            symbol_name = str(best_symbol.get("symbol_name", "")).strip()
            symbol_path = str(best_symbol.get("path", "")).strip()
            symbol_line = int(best_symbol.get("line", 0))
            symbol_id = str(best_symbol.get("symbol_id", "")).strip()

            for file_block in file_blocks:
                if str(file_block.get("path", "")).strip() == symbol_path:
                    file_id = str(file_block.get("file_id", "")).strip()
                    return (
                            "The best evidence-backed caller is "
                            + symbol_name
                            + " at "
                            + symbol_path
                            + ":"
                            + str(symbol_line)
                            + " ["
                            + file_id
                            + "]["
                            + symbol_id
                            + "]."
                    )

            return (
                    "The best evidence-backed caller is "
                    + symbol_name
                    + " at "
                    + symbol_path
                    + ":"
                    + str(symbol_line)
                    + " ["
                    + symbol_id
                    + "]."
            )

        # Runtime signal connection fallback.
        # Slot names like on_apply_clicked exist only in runtime_signal_connections,
        # not in the static symbol index. Surface them from file evidence detail.
        is_slot_owner_question = any(
            term in q
            for term in [
                "which symbol owns",
                "what symbol owns",
                "which symbol handles",
                "what symbol handles",
                "which slot",
                "what slot",
                "which handler",
                "what handler",
            ]
        )

        if is_slot_owner_question and file_blocks:
            import re as _re
            for file_block in file_blocks:
                detail = str(file_block.get("detail", "")).lower()
                file_id = str(file_block.get("file_id", "")).strip()
                file_path = str(file_block.get("path", "")).strip()

                slot_matches = _re.findall(
                    r'slot[_\s]*[=:"\s]+([a-z_][a-z0-9_]*)',
                    detail,
                )
                for slot in slot_matches:
                    if slot in q:
                        return (
                                "The slot '"
                                + slot
                                + "' is a runtime signal handler captured at runtime. "
                                + "It appears in the runtime signal connections of "
                                + file_path
                                + " ["
                                + file_id
                                + "]. "
                                + "This symbol was not found in the static symbol index "
                                + "because it is defined inside a runtime collector scenario."
                        )

        return None

__all__ = [

]
