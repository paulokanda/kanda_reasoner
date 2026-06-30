# project-path: kanda_reasoner_app/reasoner_engine/ai_bridge.py
"""
Local AI bridge for Kanda Reasoner engine.

--"---------------------------------------------------------------------------------------------------------------------------------------------------------------------
--'  -s -,-  AI CONTEXT - REFACTORED MODULE                  --'
--'                                                      --'
--'  This module has been decomposed into submodules.    --'
--'  MANIFEST : kanda_reasoner_app/reasoner_engine/ai_bridge_help.json          --'
--'  FOLDER   : kanda_reasoner_app/reasoner_engine/ai_bridge_help              --'
--'                                                      --'
--'  -zoe Read the manifest before editing any logic here.  --'
--s---------------------------------------------------------------------------------------------------------------------------------------------------------------------
"""
from __future__ import annotations

from pathlib import Path

from kanda_reasoner_app.reasoner_engine.v10_qwen_ai_models import V9QwenAIModels
from kanda_reasoner_app.reasoner_engine.ai_bridge_help.bridge_signals import (
    AIWorkerBridge,
)
from kanda_reasoner_app.reasoner_engine.ai_bridge_help.deterministic_answers import (
    answer_deterministic_from_prompt,
    answer_one_line_from_prompt,
    repair_one_line_symbol_ids,
)
from kanda_reasoner_app.reasoner_engine.ai_bridge_help.focus_snippets import (
    build_generative_focus_message,
)
from kanda_reasoner_app.reasoner_engine.ai_bridge_help.grounding_checks import (
    grounding_failure_reason,
    sanitize_invalid_ids,
)
from kanda_reasoner_app.reasoner_engine.ai_bridge_help.prompt_extraction import (
    extract_one_line_triplet,
)
from kanda_reasoner_app.reasoner_engine.ai_bridge_help.prompt_modes import (
    is_deterministic_prompt,
    is_generative_prompt,
    is_one_line_prompt,
)

__all__ = ["AIWorkerBridge", "LocalAIReasoner"]


class LocalAIReasoner:
    """Represent local aireasoner."""
    
    def __init__(self) -> None:
        """Support init behavior.
        """
        
        self.wrapper = V9QwenAIModels()
        self.bridge = AIWorkerBridge()

    def _handle_done(self, prompt: str, answer_text: str) -> None:
        """Support handle done behavior.
        
        Parameters
        ----------
        prompt : str
            The prompt value.
        answer_text : str
            The answer text value.
        """
        
        if is_one_line_prompt(prompt):
            answer_text = extract_one_line_triplet(answer_text)
            answer_text = repair_one_line_symbol_ids(prompt, answer_text)

        if is_generative_prompt(prompt):
            answer_text = sanitize_invalid_ids(prompt, answer_text)

        failure_reason = grounding_failure_reason(prompt, answer_text)
        if failure_reason:
            self.bridge.status_ready.emit("Grounding rejection: " + failure_reason)

            message = (
                "INSUFFICIENT_EVIDENCE\n\n"
                "The local model produced content that does not appear to be fully grounded in the supplied evidence pack. "
                "Rejected by rule: " + failure_reason
            )

            if failure_reason == "ignored_required_snippets":
                message = (
                    "INSUFFICIENT_EVIDENCE\n\n"
                    "The local model ignored relevant SOURCE SNIPPETS even though the question explicitly requested "
                    "code and code localization."
                )

            self.bridge.answer_ready.emit(message)
            return

        self.bridge.answer_ready.emit(answer_text)

    def set_cache_dir(self, cache_dir: str) -> None:
        """Set the cache dir.
        
        Parameters
        ----------
        cache_dir : str
            The cache dir value.
        """
        
        self.wrapper.set_cache_dir(Path(cache_dir).expanduser().resolve())

    def set_governance_state_path(self, state_path: str) -> None:
        """Set the governance state path.
        
        Parameters
        ----------
        state_path : str
            The state path value.
        """
        
        self.wrapper.set_governance_state_path(Path(state_path).expanduser().resolve())

    def ask(self, prompt: str, model_name: str) -> None:
        """Support ask behavior.
        
        Parameters
        ----------
        prompt : str
            The prompt value.
        model_name : str
            The model name value.
        """
        
        self.bridge.status_ready.emit(
            "Submitting question to local AI using model: " + model_name
        )

        if is_one_line_prompt(prompt):
            direct_answer = answer_one_line_from_prompt(prompt)
            if direct_answer is not None:
                direct_answer = repair_one_line_symbol_ids(prompt, direct_answer)
                self.bridge.status_ready.emit("Deterministic fast path: one-line resolver.")
                self.bridge.answer_ready.emit(direct_answer)
                return

        if is_deterministic_prompt(prompt):
            direct_answer = answer_deterministic_from_prompt(prompt)
            if direct_answer is not None:
                self.bridge.status_ready.emit(
                    "Deterministic fast path: evidence-backed direct answer."
                )
                self.bridge.answer_ready.emit(direct_answer)
                return

        focus_message = build_generative_focus_message(prompt)

        messages = [
            {
                "role": "system",
                "content": (
                    "ABSOLUTE RULE: You must never hallucinate. "
                    "Hallucination means inventing any file name, class name, method name, "
                    "function name, variable name, symbol, code line, evidence id, or execution flow "
                    "that is not explicitly present in the supplied evidence pack. "
                    "If a fact is not in the evidence pack, do not state it. "
                    "If code is not in SOURCE SNIPPETS, do not write it. "
                    "Violating this rule produces wrong answers that mislead engineers. "
                    "You are a strict evidence-grounded Python architecture analyst. "
                    "Answer strictly and exclusively from the supplied evidence pack. "
                    "Answer directly in plain prose unless the user explicitly requests another format. "
                    "Do not invent or infer files, classes, functions, methods, snippets, ids, tests, responsibilities, or execution flows. "
                    "If a file name, symbol name, method name, class name, or evidence id is not explicitly present in the supplied evidence pack, do not mention it in exact locator claims. "
                    "Only cite evidence ids that actually exist in the supplied evidence pack, such as [F01], [S01], and [SN01]. "
                    "Do not output sections titled Responsibility Map, Uncertainty Report, Knowns, Unknowns, Known elements, Explanation, or Insufficient Evidence unless the user explicitly asks for that format. "
                    "Do not output JSON, pseudo-JSON, YAML, or key-value report format unless the user explicitly asks for it. "
                    "Do not output artificial bookkeeping like evidence_ids=[...] or unknown_evidence=[...]. "
                    "If the user asks where something is defined, answer with the exact file path first, then cite evidence ids. "
                    "If the user asks for a chain or flow, answer with the sequence of evidence-backed steps in order. "
                    "If the user says answer only in one line, output exactly one line and nothing else. "
                    "If the user asks for exact file path, symbol, or evidence ids only, do not provide explanation, report, summary, or uncertainty sections. "
                    "If the top-ranked evidence already identifies a matching file or symbol, prefer that exact file or symbol instead of refusing. "
                    "Do not claim absence of evidence when the retrieved evidence explicitly contains the matching file or symbol. "
                    "For explanatory questions, summarize only from retrieved evidence and avoid introducing uncited exact symbol claims that are not present in the evidence pack. "
                    "If evidence is partial, state the missing link in one sentence at the end. "
                    "Do not discuss unrelated domains such as image processing unless explicitly supported by the evidence pack. "
                    "Never fabricate placeholder examples like test_module.py or test_class_method. "
                    "If the prompt indicates prefer_code mode for an implementation explanation and the evidence pack contains SOURCE SNIPPETS, include short real code excerpts copied from those snippets. "
                    "CRITICAL: When showing code, copy lines VERBATIM from SOURCE SNIPPETS only. "
                    "Do NOT reconstruct, paraphrase, or synthesize code from descriptions. "
                    "Do NOT invent function calls, variable names, or method bodies not present in SOURCE SNIPPETS. "
                    "If no relevant SOURCE SNIPPET exists for a code detail, describe it in prose instead of inventing code. "
                    "Do not replace code-backed explanation with prose-only explanation when relevant snippets exist. "
                ),
            },
        ]
        if focus_message:
            messages.append(
                {
                    "role": "system",
                    "content": focus_message,
                }
            )

        messages.append(
            {
                "role": "user",
                "content": prompt,
            }
        )

        cache_key_data = {
            "task": "v10_reasoner_chat",
            "model": model_name,
            "prompt": prompt,
        }

        self.wrapper.stream_chat(
            messages,
            model=model_name,
            temperature=0.05,
            max_tokens=2200,
            use_cache=False,
            cache_key_data=cache_key_data,
            on_token=self.bridge.token_ready.emit,
            on_done=lambda text: self._handle_done(prompt, text),
            on_error=self.bridge.error_ready.emit,
        )



