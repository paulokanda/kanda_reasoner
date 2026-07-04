# project-path: kanda_reasoner_app/reasoner_engine/prompt_builder.py
"""Prompt builder public entry point for Project Reasoner.

This module owns final evidence-pack assembly for the local AI prompt. Helper
functions live under prompt_builder_help.
"""

from __future__ import annotations

from typing import Any

from .v10_models import ConversationTurn, RetrievalBundle
from .prompt_builder_help.answer_style import build_answer_style_instructions
from .prompt_builder_help.callsite_evidence import (
    append_callsite_evidence_section,
    prioritize_callsite_snippets,
)
from .prompt_builder_help.prompt_classification import (
    is_which_method_calls_question,
    norm_text,
    tokenize_query,
)
from .prompt_builder_help.prompt_sections import (
    append_file_evidence_section,
    append_live_source_evidence_section,
    append_memory_section,
    append_project_summary,
    append_source_snippets_section,
    append_symbol_evidence_section,
)
from .prompt_builder_help.widget_registry_section import append_widget_registry_section

__all__ = [
    "PROJECT_SCOPE_GUARDRAIL",
    "TOOL_PROJECT_BOUNDARY_GUARDRAIL",
    "PromptBuilder",
    "is_which_method_calls_question",
]

PROJECT_SCOPE_GUARDRAIL = (
    "SYSTEM CONSTRAINTS:\n"
    "- Use only the evidence items shown below.\n"
    "- Do not answer from memory when the evidence pack does not support the claim.\n"
    "- If evidence is partial, report uncertainty explicitly.\n"
    "- Do not invent files, classes, functions, methods, snippets, ids, tests, responsibilities, or execution flows.\n"
)

TOOL_PROJECT_BOUNDARY_GUARDRAIL = (
    "TOOL / ACTIVE PROJECT BOUNDARY:\n"
    "- Project Q&A is a KANDA Reasoner tool feature, but this prompt answers about "
    "the active selected project loaded from PROJECT_ROOT and the evidence pack.\n"
    "- Treat PROJECT_ROOT as the project being analyzed, even when the selected "
    "project name is kanda_reasoner.\n"
    "- Do not answer about KANDA Reasoner as a reusable tool/runtime unless the "
    "retrieved evidence explicitly shows tool-owned code or the user asks about "
    "the tool layer.\n"
    "- Do not assume kanda_reasoner_app, *_show_project_to_AI, or "
    "*_delete_after_daily_work is the target for every question; target ownership "
    "follows the selected project root and retrieved evidence.\n"
    "- Generated evidence, local-AI JSON, freeze hints, handoff output, and "
    "daily-work files are project-support/evidence artifacts, not reusable tool "
    "source truth.\n"
)

# Backward-compatible aliases for existing callers/tests.
_norm = norm_text
_tokenize_query = tokenize_query
_build_answer_style_instructions = build_answer_style_instructions


class PromptBuilder:
    """Build evidence-grounded prompts for local AI answers."""

    def build(
        self,
        question: str,
        bundle: RetrievalBundle,
        project_root: str,
        summary: dict,
        memory_turns: list[ConversationTurn],
        prefer_code: bool = True,
        widget_registry: dict | None = None,
        verbosity: str = "Detailed",
        debug: bool = False,
    ) -> str:
        """Build the complete prompt for one user question."""
        q = norm_text(question)
        which_calls_query = is_which_method_calls_question(q)

        prioritized_callsite_snippets = (
            prioritize_callsite_snippets(question, list(bundle.snippet_evidence))
            if which_calls_query
            else []
        )

        lines: list[str] = []

        lines.append(PROJECT_SCOPE_GUARDRAIL)
        lines.append("")

        lines.append(TOOL_PROJECT_BOUNDARY_GUARDRAIL)
        lines.append("")

        lines.append("PRIMARY TASK")
        lines.append(question)
        lines.append("")

        lines.append("USER QUESTION")
        lines.append(question)

        append_callsite_evidence_section(lines, prioritized_callsite_snippets)

        append_project_summary(lines, project_root, summary)

        lines.append("EVIDENCE INTERPRETATION RULES")
        lines.append(
            "- packaging_metadata = declared packaging facts from files such as pyproject.toml, requirements, setup.py, setup.cfg, Pipfile, poetry.lock, or uv.lock."
        )
        lines.append(
            "- documentation_intent = declared project purpose, workflows, architecture terms, run instructions, named features, and integrations extracted from README/docs."
        )
        lines.append(
            "- source snippets and line-level implementation evidence outrank documentation_intent for code-truth and implementation-truth."
        )
        lines.append(
            "- LIVE SOURCE EVIDENCE = current disk source verified under PROJECT_ROOT. "
            "For implementation truth, it outranks stale JSON, stale documentation, and stale metadata."
        )
        lines.append(
            "- If packaging_metadata or documentation_intent conflicts with code-level evidence, prefer code-level evidence and explain the mismatch."
        )
        lines.append("")

        append_memory_section(lines, memory_turns)
        append_file_evidence_section(lines, bundle.file_evidence)
        append_symbol_evidence_section(lines, bundle.symbol_evidence)
        append_live_source_evidence_section(lines, bundle.snippet_evidence)
        append_source_snippets_section(lines, bundle.snippet_evidence)
        append_widget_registry_section(lines, question, widget_registry)

        lines.append("STRICT GROUNDING RULE")
        lines.append(
            "Any file name, symbol name, class name, function name, or evidence id not explicitly present above is forbidden. "
            "When evidence is missing, answer exactly with INSUFFICIENT_EVIDENCE and explain what is missing."
        )
        lines.append("")

        lines.append("CITATION RULE")
        lines.append(
            "You may only cite evidence IDs that appear in the sections above. "
            "For example, if you see [F01] in FILE EVIDENCE, you may say 'According to [F01] ...'. "
            "If you see a file path but no ID, refer to it by path. "
            "Do not invent IDs like 'F99' or 'S15' that are not listed."
        )
        lines.append("")

        lines.append("PREFERENCE MODE")
        lines.append("prefer_code" if prefer_code else "prefer_prose")
        lines.append("")

        lines.append(build_answer_style_instructions(question, prefer_code))
        lines.append("")

        lines.append("FINAL TASK REMINDER")
        lines.append("Answer this exact question: " + question)
        lines.append("")

        lines.append("INSTRUCTIONS")
        lines.append(
            "Answer strictly and exclusively from the evidence above. "
            "Do not invent files, classes, methods, symbols, snippets, ids, tests, or flows. "
            "If a file, symbol, or snippet is not explicitly present in the evidence pack, do not mention it. "
            "Only cite evidence ids that actually exist in the evidence pack shown above. "
            "Answer directly in plain prose unless the user explicitly asks for another format. "
            "Do not output JSON, pseudo-JSON, YAML, or key-value report format unless explicitly requested. "
            "Do not output sections titled Responsibility Map, Uncertainty Report, Knowns, Unknowns, Known elements, "
            "or Explanation unless explicitly requested. "
            "If the user asks where something is defined, answer with the exact file path first, then cite evidence ids. "
            "If the user asks for a chain or flow, answer with the sequence of evidence-backed steps in order. "
            "If the user asks which method calls a callee, answer from CALL-SITE EVIDENCE "
            "first and do not answer from the callee definition. "
            "If the user says answer only in one line, output exactly one line and nothing else. "
            "When documentation_intent or packaging_metadata conflicts with source snippets, live-source evidence, or line-level code evidence, "
            "explicitly report both sides of the mismatch, state that code-level evidence wins for implementation truth, "
            "and describe the documentation or packaging claim as unverified, stale, or inconsistent with code rather than silently blending them. "
            "If the evidence is insufficient, answer exactly with INSUFFICIENT_EVIDENCE and explain what is missing."
        )

        prompt = "\n".join(lines)

        if debug:
            first_symbols = [
                {
                    "path": getattr(symbol, "path", None),
                    "symbol": getattr(symbol, "symbol_name", None),
                }
                for symbol in list(bundle.symbol_evidence)[:5]
            ]
            first_snippets = [
                {
                    "path": snippet.get("path"),
                    "anchor": snippet.get("anchor"),
                    "line": snippet.get("line"),
                    "preview": str(snippet.get("text", "")).splitlines()[:3],
                }
                for snippet in list(bundle.snippet_evidence)[:5]
            ]
            print(
                "[FINAL PROMPT DEBUG]",
                {
                    "question": question,
                    "first_symbols": first_symbols,
                    "first_snippets": first_snippets,
                    "prompt_head": prompt[:1800],
                },
            )

        return prompt
